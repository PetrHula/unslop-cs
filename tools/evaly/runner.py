#!/usr/bin/env python3
"""Runner regresních případů skillu unslop-cs.

Čte skills/unslop-cs/evals/pripady.md a každý případ pouští přes `claude -p`
s pluginem načteným z tohoto repozitáře (--plugin-dir). Každý případ běží
několikrát (výchozí 3×) a o výsledku rozhoduje většina běhů.

Jak se rozhoduje o jednom běhu:
  - Skill se musí načíst (ve výstupu je volání nástroje Skill na unslop-cs).
  - ČISTÝ případ (režim kontroly): projde, když výstup nemá žádné P0 ani P1.
    Počty čte z řádku `SOUHRN: P0=… P1=… P2=…`, který runner v zadání
    vyžaduje; když řádek chybí, rozhodne hodnotitel.
  - Ostatní případy: druhé volání `claude -p` jako hodnotitel odpoví u každého
    řádku OČEKÁVÁNO (včetně NESMÍ) ano/ne. Řádky „Volitelně“ se hodnotí, ale
    do výsledku se nepočítají. Hodnotitel navíc vypíše nálezy P0/P1 ve
    výstupu, které žádnému řádku neodpovídají („mimo OČEKÁVÁNO“); běh
    neprojde, když jich je víc než --max-mimo (výchozí 1, -1 vypne).
  - Chyby infrastruktury (limit session nebo použití, přetížení API, timeout,
    prázdný výstup, rozbitá odpověď hodnotitele) se opakují (--opakovani,
    výchozí 3, s rostoucí pauzou). Když se nepodaří ani tak, běh je
    „nevyhodnocený“: do většiny se nepočítá a ve zprávě je vidět zvlášť.
  - PŘEPIS: režim přepisu; opravenou verzi runner žádá mezi řádky <<<VERZE
    a VERZE>>>. Věty z bloku BEZE ZMĚNY se v ní hledají přesně jako řetězec
    (sjednocují se jen běhy bílých znaků), bez hodnotitele.

UDPipe je vypnutý: runner proměnnou UNSLOP_UDPIPE z prostředí odstraní.
Zapnete ho přepínačem --udpipe CESTA.

Použití (z kořene repozitáře):
    python3 tools/evaly/runner.py --stitek vychozi-1.1.0
    python3 tools/evaly/runner.py --pripady 1,6,20 --behy 1 --stitek zkouska
    python3 tools/evaly/runner.py --stitek po-prestavbe \\
        --srovnat tools/evaly/vysledky/vychozi-1.1.0/behy.json

Výstup: tools/evaly/vysledky/<stitek>/vysledky.md (tabulka) a behy.json
(všechny výstupy a verdikty). Jen standardní knihovna Pythonu 3.8+.
"""

import argparse
import collections
import concurrent.futures
import datetime
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import time

KOREN = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SKILL_DIR = os.path.join(KOREN, "skills", "unslop-cs")
PRIPADY = os.path.join(SKILL_DIR, "evals", "pripady.md")
VYSLEDKY = os.path.join(KOREN, "tools", "evaly", "vysledky")

# Čisté případy podle hlavičky pripady.md; parser je ověřuje proti titulkům.
CISTE = {6, 9, 11, 12, 14, 15, 19, 24, 26, 28}

PROFILY = {
    "sociální sítě": "socialni",
    "blog": "blog",
    "e-mail": "email",
    "dokumentace": "dokumentace",
    "odborný text": "odborny",
    "prezentace": "prezentace",
}

# Model ukládá vstup skriptu často příkazem `mkdir -p X && cd X && cat > v.txt <<EOF`.
# Režim dontAsk ho zamítá i s pravidly Bash(cat *), Bash(mkdir *), Bash(cd *): zúžená
# pravidla nepokrývají přesměrování ani cd mimo pracovní adresář (ověřeno, jen plné
# `Bash` je pustí, to runner nepovoluje). Model pak skript nespustil (4 až 10 běhů z 90
# v k5). Runner proto text sám uloží do vstup.txt v pracovním adresáři; model ho jen
# předá skriptu, což pravidlo Bash(python3 *) pustí.
NASTROJE_SKILLU = "Skill Read Write Glob Grep Bash(python3 *)"

# Výstupy, které nejsou prací skillu, ale selháním prostředí. claude -p je
# vrací i s podtypem „success“ (limit session v k5-1.3.0-final).
_INFRA = re.compile(
    r"^\W*(you'?ve hit your|claude (ai )?usage limit|session limit|usage limit|rate.?limit"
    r"|api error|overloaded|internal server error|request timed out|credit balance"
    r"|(error|http)\W*(429|500|502|503|529))", re.I)


_ZAMEK = threading.Lock()
OPAKOVANI_HODNOTITELE = [0]


class InfraChyba(Exception):
    """Selhání prostředí, ne skillu; volání se opakuje."""


def infra_chyba(text):
    """Vrátí popis chyby infrastruktury, nebo None. Hlášky claude -p jsou
    krátké a začínají textem chyby; delší výstup nebo výstup s řádkem SOUHRN
    je práce skillu, i když slovo „limit“ obsahuje."""
    t = (text or "").strip()
    if len(t) > 400 or "SOUHRN:" in t or "<<<VERZE" in t:
        return None
    m = _INFRA.search(t)
    return _bile(t)[:160] if m else None


# ---------------------------------------------------------------------------
# Načtení případů

Pripad = collections.namedtuple("Pripad", "cislo nazev typ profil vstup radky beze_zmeny")
Radek = collections.namedtuple("Radek", "id text volitelny")

_HLAVICKA = re.compile(r"^## Případ (\d+) – (.*?)\s*\(profil: ([^)]+)\)\s*$")


def nacti_pripady(cesta=PRIPADY):
    with open(cesta, encoding="utf-8") as f:
        radky = f.read().splitlines()
    pripady, aktualni = [], None
    for r in radky:
        m = _HLAVICKA.match(r)
        if r.startswith("## ") and (not m or "Formát výstupu" in m.group(2)):
            aktualni = None  # případy o formátu výstupu (31–34) se pouští ručně
        elif m:
            aktualni = {"cislo": int(m.group(1)), "nazev": m.group(2),
                        "profil": m.group(3).strip(), "radky": []}
            pripady.append(aktualni)
        elif aktualni is not None:
            aktualni["radky"].append(r)
    return [_rozeber(p) for p in pripady]


def _rozeber(p):
    nazev = p["nazev"]
    if nazev.startswith("ČISTÝ:"):
        typ = "cisty"
    elif nazev.startswith("PŘEPIS:"):
        typ = "prepis"
    else:
        typ = "kontrola"
    vstup, ocekavano, beze, blok = [], [], [], None
    for r in p["radky"]:
        if re.match(r"^VSTUP\b.*:\s*$", r):
            blok = "vstup"
        elif r.startswith("OČEKÁVÁNO:"):
            blok = "ocekavano"
            zbytek = r[len("OČEKÁVÁNO:"):].strip()
            if zbytek:
                ocekavano.append(zbytek)
        elif r.startswith("BEZE ZMĚNY:"):
            blok = "beze"
        elif blok == "vstup" and r.startswith(">"):
            vstup.append(r[2:] if r.startswith("> ") else r[1:])
        elif blok == "ocekavano" and r.startswith("- "):
            ocekavano.append(r[2:].strip())
        elif blok == "beze" and r.startswith("- "):
            m = re.match(r"^- „(.*)“\s*$", r)
            if not m:
                raise SystemExit(f"Případ {p['cislo']}: neznámý řádek BEZE ZMĚNY: {r}")
            beze.append(m.group(1))
    if not vstup:
        raise SystemExit(f"Případ {p['cislo']}: chybí VSTUP")
    if p["profil"] not in PROFILY:
        raise SystemExit(f"Případ {p['cislo']}: neznámý profil {p['profil']}")
    radky = [Radek(i + 1, t, t.lower().startswith("volitelně")) for i, t in enumerate(ocekavano)]
    return Pripad(p["cislo"], nazev, typ, p["profil"], "\n".join(vstup).strip(), radky, beze)


# ---------------------------------------------------------------------------
# Zadání

ZADANI_KONTROLA = """Použij skill unslop-cs (unslop-cs:unslop-cs) v režimu kontroly: úplný audit (P0, P1 i P2), profil registru „{profil}“ ({profil_id}).
Zkontroluj text mezi značkami <text> a </text>. Text nepřepisuj, jen ho posuď.
Stejný text je uložený v souboru vstup.txt (UTF-8) v pracovním adresáři.

Na úplný konec odpovědi přidej samostatný řádek přesně v tomto tvaru:
SOUHRN: P0=<počet> P1=<počet> P2=<počet>
Počítej jen nálezy, které po posouzení zůstávají jako vady; místa, která jsou v kontextu obhajitelná, nepočítej.

<text>
{vstup}
</text>"""

ZADANI_PREPIS = """Použij skill unslop-cs (unslop-cs:unslop-cs) v režimu přepisu, profil registru „{profil}“ ({profil_id}).
Přepiš text mezi značkami <text> a </text> podle skillu.
Stejný text je uložený v souboru vstup.txt (UTF-8) v pracovním adresáři.
Celou opravenou verzi textu dej mezi dva samostatné řádky <<<VERZE a VERZE>>>. Audit a seznam změn napiš mimo ně.

<text>
{vstup}
</text>"""

ZADANI_HODNOTITEL = """Jsi hodnotitel regresních testů skillu, který v českém textu hledá vzorce typické pro AI (závažnost P0 > P1 > P2). Dostaneš vstupní text případu, výstup skillu a očíslované požadavky. U každého požadavku rozhodni, jestli ho výstup splňuje (true / false), a jednou větou česky zdůvodni.

Jak požadavky číst:
- „P0: X“, „P1: X“, „P2: X“ je splněn, když výstup X označí jako nález a jeho závažnost se od uvedené liší nejvýš o jeden stupeň. Nezáleží na formulaci ani na tom, jak výstup nálezy rozdělí nebo sloučí; rozhoduje, jestli je vzorec na daném místě označený jako vada. Výčet v závorce ukazuje, o která místa jde; stačí, když výstup označí podstatnou část z nich.
- „NESMÍ označit: X“ je splněn, když výstup X jako vadu neoznačí. Zmínka, že X je v pořádku, nevadí.
- „Upozornit: X“ je splněn, když výstup na X upozorní (v nálezu, v posouzení nebo značkou [OVĚŘIT]).
- Požadavky na přepis („Přepis musí…“, „Přepis selže, když…“, „Nová verze NESMÍ…“, „Výstup obsahuje značky…“, „Pojistka: …“) posuzuj podle opravené verze mezi řádky <<<VERZE a VERZE>>>. Když výstup opravenou verzi nemá, posuď, jestli ji porušují návrhy oprav ve výstupu; když žádné nejsou, je požadavek splněný.
- Věta „žádný nález“ je splněna, když výstup nemá žádný nález P0 ani P1, který by po posouzení zůstal jako vada.

Potom vypiš do pole „mimo“ každý nález, který výstup označil jako vadu se závažností P0 nebo P1 a který žádný požadavek nepokrývá. Nález je pokrytý, když se týká místa nebo vzorce, o kterém mluví kterýkoli požadavek jakéhokoli typu: řádek „P0/P1/P2: X“, „Upozornit: X“, „NESMÍ označit: X“ i požadavek na přepis (například značky [OVĚŘIT] u uvedených míst nebo zachování uvedené věty). Požadavky na přepis nevyjmenovávají všechny nálezy, jen ty, na kterých případ stojí; nález na místě, které požadavek zmiňuje nebo které přepis podle něj musí opravit, proto není „mimo“. Závažnost ber tak, jak ji uvádí výstup. Nepočítej nálezy P2, místa, která výstup sám označil za obhajitelná, a návrhy bez označení vady. Jeden vzorec na více místech je jeden nález. Když takový nález není, vrať prázdné pole.

Profil registru: {profil}

<vstup>
{vstup}
</vstup>

<vystup>
{vystup}
</vystup>

Požadavky:
{pozadavky}"""

SCHEMA_HODNOTITEL = {
    "type": "object",
    "properties": {
        "hodnoceni": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "splneno": {"type": "boolean"},
                    "duvod": {"type": "string"},
                },
                "required": ["id", "splneno", "duvod"],
            },
        },
        "mimo": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "misto": {"type": "string"},
                    "zavaznost": {"type": "string", "enum": ["P0", "P1"]},
                    "duvod": {"type": "string"},
                },
                "required": ["misto", "zavaznost", "duvod"],
            },
        },
    },
    "required": ["hodnoceni", "mimo"],
}


# ---------------------------------------------------------------------------
# Volání claude -p

def _prostredi(udpipe):
    env = dict(os.environ)
    env.pop("UNSLOP_UDPIPE", None)
    if udpipe:
        env["UNSLOP_UDPIPE"] = os.path.abspath(udpipe)
    return env


def _s_opakovanim(fn, a, *args):
    """Zavolá fn; při InfraChyba počká a zkusí znovu. Vrátí (výsledek, pokusy,
    seznam chyb infrastruktury). Když se nepodaří, výsledek je None."""
    chyby = []
    for pokus in range(1, a.opakovani + 2):
        try:
            return fn(*args), pokus, chyby
        except InfraChyba as e:
            chyby.append(str(e))
            if pokus <= a.opakovani:
                time.sleep(a.pauza * pokus)
    return None, a.opakovani + 1, chyby


def spust_skill(zadani, a, vstup=None):
    """Vrátí dict: text, skill (bool), nastroje, model, cena, chyba.
    Selhání prostředí hlásí výjimkou InfraChyba."""
    cmd = ["claude", "-p", zadani, "--output-format", "stream-json", "--verbose",
           "--no-session-persistence", "--strict-mcp-config", "--setting-sources", "project",
           "--plugin-dir", KOREN, "--permission-mode", "dontAsk",
           "--allowedTools", NASTROJE_SKILLU]
    if a.model:
        cmd += ["--model", a.model]
    cwd = tempfile.mkdtemp(prefix="unslop-eval-")
    if vstup is not None:
        with open(os.path.join(cwd, "vstup.txt"), "w", encoding="utf-8") as f:
            f.write(vstup + "\n")
    try:
        p = subprocess.run(cmd, cwd=cwd, env=_prostredi(a.udpipe), capture_output=True,
                           text=True, timeout=a.timeout)
    except subprocess.TimeoutExpired:
        raise InfraChyba(f"timeout {a.timeout} s")
    finally:
        shutil.rmtree(cwd, ignore_errors=True)
    out = {"text": "", "skill": False, "nastroje": [], "model": None, "cena": 0.0, "chyba": None,
           "prikazy": [], "zamitnuto": []}
    volani = {}  # id volání nástroje -> (nástroj, vstup)
    for radek in p.stdout.splitlines():
        try:
            u = json.loads(radek)
        except ValueError:
            continue
        if u.get("type") == "system" and u.get("subtype") == "init":
            out["model"] = u.get("model")
        elif u.get("type") == "assistant":
            for c in (u.get("message") or {}).get("content") or []:
                if c.get("type") == "tool_use":
                    nazev = c.get("name")
                    out["nastroje"].append(nazev)
                    volani[c.get("id")] = (nazev, c.get("input") or {})
                    if nazev == "Bash":
                        out["prikazy"].append(str((c.get("input") or {}).get("command", ""))[:400])
                    if nazev == "Skill" and "unslop-cs" in json.dumps(c.get("input"), ensure_ascii=False):
                        out["skill"] = True
        elif u.get("type") == "user":
            for c in (u.get("message") or {}).get("content") or []:
                if isinstance(c, dict) and c.get("type") == "tool_result" and c.get("is_error"):
                    obsah = c.get("content")
                    if isinstance(obsah, list):
                        obsah = " ".join(x.get("text", "") for x in obsah if isinstance(x, dict))
                    if re.search(r"permission|denied|not allowed|zamítn", str(obsah), re.I):
                        nazev, vstup = volani.get(c.get("tool_use_id"), ("?", {}))
                        out["zamitnuto"].append({"nastroj": nazev, "chyba": _bile(str(obsah))[:160],
                                                 "vstup": str(vstup.get("command") or vstup.get("file_path")
                                                              or vstup)[:300]})
        elif u.get("type") == "result":
            out["text"] = u.get("result") or ""
            out["cena"] = u.get("total_cost_usd") or 0.0
            if u.get("is_error"):
                out["chyba"] = u.get("subtype") or "chyba"
    infra = infra_chyba(out["text"]) or (infra_chyba(p.stderr) if not out["text"] else None)
    if infra:
        raise InfraChyba(infra)
    if not out["text"]:
        raise InfraChyba(f"prázdný výstup (kód {p.returncode}): {p.stderr.strip()[:200]}")
    return out


def spust_hodnotitele(pripad, vystup, radky, a):
    """Vrátí (verdikty, mimo, cena, chyba). Selhání prostředí opakuje."""
    v, pokusy, infra = _s_opakovanim(_hodnotitel, a, pripad, vystup, radky, a)
    with _ZAMEK:
        OPAKOVANI_HODNOTITELE[0] += pokusy - 1
    if v is None:
        return None, None, 0.0, "INFRA " + (infra[-1] if infra else "hodnotitel: ?")
    return v


def _hodnotitel(pripad, vystup, radky, a):
    pozadavky = "\n".join(f"{r.id}. {r.text}" for r in radky)
    zadani = ZADANI_HODNOTITEL.format(profil=pripad.profil, vstup=pripad.vstup,
                                      vystup=vystup, pozadavky=pozadavky)
    cmd = ["claude", "-p", zadani, "--output-format", "json", "--no-session-persistence",
           "--strict-mcp-config", "--setting-sources", "project", "--disable-slash-commands",
           "--tools", "", "--json-schema", json.dumps(SCHEMA_HODNOTITEL)]
    if a.hodnotitel_model:
        cmd += ["--model", a.hodnotitel_model]
    cwd = tempfile.mkdtemp(prefix="unslop-hodn-")
    try:
        p = subprocess.run(cmd, cwd=cwd, env=_prostredi(None), capture_output=True,
                           text=True, timeout=a.timeout)
    except subprocess.TimeoutExpired:
        raise InfraChyba(f"hodnotitel: timeout {a.timeout} s")
    finally:
        shutil.rmtree(cwd, ignore_errors=True)
    try:
        d = json.loads(p.stdout)
    except ValueError:
        raise InfraChyba("hodnotitel: " + (infra_chyba(p.stdout + " " + p.stderr)
                                           or f"nečitelná odpověď (kód {p.returncode})"))
    if d.get("is_error") or not d.get("structured_output"):
        raise InfraChyba("hodnotitel: " + (infra_chyba(d.get("result") or "")
                                           or f"bez strukturované odpovědi ({d.get('subtype')})"))
    so = d.get("structured_output") or {}
    verdikty = {h["id"]: h for h in so.get("hodnoceni", []) if isinstance(h, dict) and "id" in h}
    mimo = [m for m in so.get("mimo") or [] if isinstance(m, dict)]
    chybi = [r.id for r in radky if r.id not in verdikty]
    chyba = f"hodnotitel nevrátil řádky {chybi}" if chybi else None
    return verdikty, mimo, d.get("total_cost_usd") or 0.0, chyba


# ---------------------------------------------------------------------------
# Jeden běh

_SOUHRN = re.compile(r"SOUHRN:\s*P0\s*=\s*(\d+)\s*,?\s*P1\s*=\s*(\d+)\s*,?\s*P2\s*=\s*(\d+)")
_VERZE = re.compile(r"<<<VERZE\s*\n(.*?)\n\s*VERZE>>>", re.S)


def _bile(s):
    return re.sub(r"\s+", " ", s).strip()


def jeden_beh(pripad, beh, a):
    vzor = ZADANI_PREPIS if pripad.typ == "prepis" else ZADANI_KONTROLA
    zadani = vzor.format(profil=pripad.profil, profil_id=PROFILY[pripad.profil], vstup=pripad.vstup)
    s, pokusy, infra = _s_opakovanim(spust_skill, a, zadani, a, pripad.vstup)
    zaznam = {"pripad": pripad.cislo, "beh": beh, "model": None, "skill": False,
              "nastroje": [], "vystup": "", "cena": 0.0, "souhrn": None, "verdikty": {},
              "mimo": [], "beze_zmeny": [], "chyby": [], "proslo": False,
              "prikazy": [], "zamitnuto": [],
              "pokusy": pokusy, "infra_chyby": infra, "nevyhodnoceno": False}
    if s is None:
        zaznam["nevyhodnoceno"] = True
        zaznam["chyby"].append("INFRA: " + infra[-1])
        return zaznam
    zaznam.update(model=s["model"], skill=s["skill"], nastroje=s["nastroje"],
                  vystup=s["text"], cena=s["cena"], prikazy=s["prikazy"], zamitnuto=s["zamitnuto"])
    if s["chyba"]:
        zaznam["chyby"].append(s["chyba"])
        return zaznam
    if not s["skill"]:
        zaznam["chyby"].append("skill se nenačetl")

    m = _SOUHRN.findall(s["text"])
    if m:
        zaznam["souhrn"] = dict(zip(("P0", "P1", "P2"), map(int, m[-1])))

    ok = s["skill"]
    if pripad.typ == "cisty":
        if zaznam["souhrn"] is not None:
            if zaznam["souhrn"]["P0"] or zaznam["souhrn"]["P1"]:
                ok = False
                zaznam["chyby"].append(f"P0={zaznam['souhrn']['P0']} P1={zaznam['souhrn']['P1']}")
        else:
            radek = Radek(1, "žádný nález (výstup nemá P0 ani P1, které by po posouzení zůstaly jako vady)", False)
            v, _, cena, chyba = spust_hodnotitele(pripad, s["text"], [radek], a)
            zaznam["cena"] += cena
            zaznam["chyby"].append("chybí řádek SOUHRN, rozhodl hodnotitel")
            if chyba and chyba.startswith("INFRA"):
                zaznam["nevyhodnoceno"] = True
                zaznam["chyby"].append(chyba)
            elif chyba or not v:
                ok = False
                zaznam["chyby"].append(chyba or "hodnotitel nevrátil verdikt")
            else:
                zaznam["verdikty"] = {"1": v[1]}
                if not v[1]["splneno"]:
                    ok = False
    else:
        if pripad.radky:
            v, mimo, cena, chyba = spust_hodnotitele(pripad, s["text"], pripad.radky, a)
            zaznam["cena"] += cena
            if chyba and chyba.startswith("INFRA"):
                zaznam["nevyhodnoceno"] = True
                zaznam["chyby"].append(chyba)
                return zaznam
            zaznam["mimo"] = mimo or []
            if a.max_mimo >= 0 and len(zaznam["mimo"]) > a.max_mimo:
                ok = False
                zaznam["chyby"].append(f"mimo OČEKÁVÁNO: {len(zaznam['mimo'])} nálezy P0/P1")
            if chyba or v is None:
                ok = False
                zaznam["chyby"].append(chyba or "hodnotitel nevrátil verdikt")
            v = v or {}
            zaznam["verdikty"] = {str(k): x for k, x in v.items()}
            for r in pripad.radky:
                if r.volitelny or r.id not in v:
                    continue
                if not v[r.id]["splneno"]:
                    ok = False
        if pripad.typ == "prepis":
            mv = _VERZE.search(s["text"])
            verze = _bile(mv.group(1)) if mv else None
            if verze is None:
                ok = False
                zaznam["chyby"].append("chybí opravená verze mezi <<<VERZE a VERZE>>>")
            for veta in pripad.beze_zmeny:
                nalezeno = verze is not None and _bile(veta) in verze
                zaznam["beze_zmeny"].append({"veta": veta, "nalezeno": nalezeno})
                if not nalezeno:
                    ok = False
    zaznam["proslo"] = ok
    return zaznam


# ---------------------------------------------------------------------------
# Souhrn a zpráva

def _zkrat(t, n=60):
    t = _bile(t)
    return t if len(t) <= n else t[:n - 1] + "…"


def duvody(pripad, behy):
    """Krátký důvod z neúspěšných běhů: co selhalo a v kolika bězích."""
    pocet = collections.Counter()
    for b in behy:
        if b["proslo"] or b.get("nevyhodnoceno"):
            continue
        for ch in b["chyby"]:
            if ch.startswith("chybí řádek SOUHRN"):
                continue
            pocet[ch] += 1
        for r in pripad.radky:
            v = b["verdikty"].get(str(r.id))
            if v and not v["splneno"] and not r.volitelny:
                pocet[f"ř. {r.id} „{_zkrat(r.text)}“"] += 1
        for z in b["beze_zmeny"]:
            if not z["nalezeno"]:
                pocet[f"BEZE ZMĚNY „{_zkrat(z['veta'], 40)}“"] += 1
    nevyh = sum(bool(b.get("nevyhodnoceno")) for b in behy)
    if nevyh:
        pocet[f"nevyhodnoceno (infrastruktura) {nevyh}"] = 0
    return "; ".join(k if n == 0 else f"{k} ({n}/{len(behy)})" for k, n in pocet.most_common())


def _git(*args):
    try:
        return subprocess.run(["git", "-C", KOREN] + list(args), capture_output=True,
                              text=True, timeout=30).stdout.strip()
    except Exception:  # noqa: BLE001
        return ""


def _otisk_skillu():
    h = hashlib.sha256()
    for koren, _, soubory in sorted(os.walk(SKILL_DIR)):
        if "evals" in koren.split(os.sep) or "__pycache__" in koren:
            continue
        for s in sorted(soubory):
            with open(os.path.join(koren, s), "rb") as f:
                h.update(s.encode() + f.read())
    return h.hexdigest()[:12]


TYPY = {"cisty": "čistý", "kontrola": "kontrola", "prepis": "přepis"}


def zprava(pripady, vysledky, meta, srovnani):
    r = []
    r.append(f"# Výsledky evalů: {meta['stitek']}\n")
    r.append(f"- Datum: {meta['datum']}")
    r.append(f"- Commit: `{meta['commit']}`, otisk skillu (bez evals): `{meta['otisk']}`")
    r.append(f"- Model skillu: {meta['modely']}; hodnotitel: {meta['hodnotitel']}")
    r.append(f"- Běhů na případ: {meta['behy']} (rozhoduje většina); UDPipe: {meta['udpipe']}")
    r.append(f"- Kritérium: nejvýš {meta['max_mimo']} nález P0/P1 mimo OČEKÁVÁNO"
             if meta["max_mimo"] >= 0 else "- Kritérium: nálezy mimo OČEKÁVÁNO se nepočítají")
    r.append(f"- Opakování chyb infrastruktury: {meta['opakovani_celkem']} navíc; "
             f"nevyhodnocené běhy: {meta['nevyhodnoceno']}")
    r.append(f"- Povolené nástroje skillu: `{meta['nastroje_skillu']}`; vstup.txt s textem případu "
             "vytváří runner")
    r.append(f"- Zamítnuté nástroje: {meta['zamitnuto']} běhů z {meta['behu_celkem']} "
             f"(podrobnosti v `behy.json`, pole `zamitnuto`)")
    r.append(f"- Cena celkem: {meta['cena']:.2f} USD\n")
    cis = [p for p in pripady if p.typ == "cisty"]
    ost = [p for p in pripady if p.typ != "cisty"]
    ok = lambda ps: sum(vysledky[p.cislo]["proslo"] is True for p in ps)  # noqa: E731
    r.append(f"**Prošlo {ok(pripady)} z {len(pripady)}** (čisté {ok(cis)}/{len(cis)}, "
             f"ostatní {ok(ost)}/{len(ost)}).\n")
    hlav = "| Případ | Typ | Výsledek | Běhy | Důvod |"
    del_ = "|---|---|---|---|---|"
    if srovnani:
        hlav = "| Případ | Typ | Výsledek | Výchozí stav | Běhy | Důvod |"
        del_ = "|---|---|---|---|---|---|"
    r += [hlav, del_]
    for p in pripady:
        v = vysledky[p.cislo]
        vys = ("nevyhodnoceno" if v["proslo"] is None
               else "prošlo" if v["proslo"] else "**neprošlo**")
        behy = f"{v['proslych']}/{v['behu']}"
        nazev = f"{p.cislo} – {_zkrat(p.nazev, 45)}"
        duvod = v["duvod"] or "–"
        if srovnani:
            puv = srovnani.get(p.cislo)
            puv_t = "–" if puv is None else ("prošlo" if puv else "neprošlo")
            if puv is not None and v["proslo"] is not None and puv != v["proslo"]:
                puv_t += " ⇄"
            r.append(f"| {nazev} | {TYPY[p.typ]} | {vys} | {puv_t} | {behy} | {duvod} |")
        else:
            r.append(f"| {nazev} | {TYPY[p.typ]} | {vys} | {behy} | {duvod} |")
    r.append("\nDůvod uvádí, co selhalo a v kolika bězích. Případ projde i s jedním neúspěšným "
             "během ze tří; důvod pak ukazuje nestabilitu. Běhy jsou vyhodnocené / celkem; "
             "nevyhodnocené běhy (chyba infrastruktury i po opakování) do většiny nepočítají. "
             "Úplné výstupy, verdikty a nálezy mimo OČEKÁVÁNO jsou v `behy.json`.")
    if srovnani and meta.get("srovnani_kriterium") != meta["max_mimo"]:
        r.append("\n**Pozor:** srovnávací běh má jiné kritérium nálezů mimo OČEKÁVÁNO "
                 f"({meta.get('srovnani_kriterium')}), výsledky nejsou přímo srovnatelné.")
    if srovnani:
        r.append("\n⇄ = výsledek se oproti výchozímu stavu změnil.")
    return "\n".join(r) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--stitek", required=True, help="název běhu, složka ve vysledky/")
    ap.add_argument("--pripady", help="jen vybrané případy, např. 1,6,20")
    ap.add_argument("--behy", type=int, default=3, help="běhů na případ (výchozí 3)")
    ap.add_argument("--jobs", type=int, default=4, help="souběžných běhů (výchozí 4)")
    ap.add_argument("--model", help="model pro běh skillu (výchozí podle claude)")
    ap.add_argument("--hodnotitel-model", help="model hodnotitele (výchozí podle claude)")
    ap.add_argument("--udpipe", help="cesta k modelu UDPipe; bez ní běží skript bez modelu")
    ap.add_argument("--timeout", type=int, default=900, help="limit jednoho volání v s")
    ap.add_argument("--opakovani", type=int, default=3,
                    help="kolikrát zopakovat volání po chybě infrastruktury (výchozí 3)")
    ap.add_argument("--pauza", type=int, default=30,
                    help="pauza před opakováním v s, roste s pokusem (výchozí 30)")
    ap.add_argument("--max-mimo", type=int, default=1,
                    help="nejvýš nálezů P0/P1 mimo OČEKÁVÁNO na běh (výchozí 1, -1 vypne)")
    ap.add_argument("--srovnat", help="behy.json dřívějšího běhu pro sloupec Výchozí stav")
    ap.add_argument("--vystup", help="složka pro výsledky (výchozí tools/evaly/vysledky/<stitek>)")
    a = ap.parse_args()

    if not shutil.which("claude"):
        raise SystemExit("Nenašel jsem příkaz claude (Claude Code CLI).")
    pripady = nacti_pripady()
    nalezene_ciste = {p.cislo for p in pripady if p.typ == "cisty"}
    if nalezene_ciste != CISTE:
        raise SystemExit(f"Čisté případy v titulcích {sorted(nalezene_ciste)} "
                         f"nesedí s hlavičkou {sorted(CISTE)}.")
    if a.pripady:
        vyber = {int(x) for x in a.pripady.split(",")}
        pripady = [p for p in pripady if p.cislo in vyber]
    if not pripady:
        raise SystemExit("Žádné případy k běhu.")

    ulohy = [(p, b) for p in pripady for b in range(1, a.behy + 1)]
    behy = collections.defaultdict(list)
    print(f"{len(pripady)} případů × {a.behy} běhů = {len(ulohy)} volání skillu", file=sys.stderr)
    with concurrent.futures.ThreadPoolExecutor(max_workers=a.jobs) as ex:
        fut = {ex.submit(jeden_beh, p, b, a): (p, b) for p, b in ulohy}
        for i, f in enumerate(concurrent.futures.as_completed(fut), 1):
            p, b = fut[f]
            try:
                z = f.result()
            except Exception as e:  # noqa: BLE001
                z = {"pripad": p.cislo, "beh": b, "proslo": False, "chyby": [f"výjimka: {e!r}"],
                     "verdikty": {}, "mimo": [], "beze_zmeny": [], "cena": 0.0, "model": None,
                     "skill": False, "nastroje": [], "vystup": "", "souhrn": None,
                     "pokusy": 1, "infra_chyby": [], "nevyhodnoceno": False,
                     "prikazy": [], "zamitnuto": []}
            behy[p.cislo].append(z)
            stav = ("nevyhodnoceno" if z.get("nevyhodnoceno")
                    else "prošlo" if z["proslo"] else "neprošlo")
            print(f"[{i}/{len(ulohy)}] případ {p.cislo} běh {b}: {stav} "
                  f"(pokusů {z.get('pokusy', 1)}) {'; '.join(z['chyby'])}",
                  file=sys.stderr)

    vysledky = {}
    for p in pripady:
        bb = sorted(behy[p.cislo], key=lambda z: z["beh"])
        hodnocene = [z for z in bb if not z.get("nevyhodnoceno")]
        proslych = sum(z["proslo"] for z in hodnocene)
        vysledky[p.cislo] = {"proslo": proslych > len(hodnocene) / 2 if hodnocene else None,
                             "proslych": proslych, "behu": len(hodnocene),
                             "nevyhodnoceno": len(bb) - len(hodnocene),
                             "duvod": duvody(p, bb), "behy": bb}

    srovnani, srovnani_kriterium = None, None
    if a.srovnat:
        with open(a.srovnat, encoding="utf-8") as f:
            puvodni = json.load(f)
        srovnani = {int(k): v["proslo"] for k, v in puvodni["pripady"].items()
                    if v["proslo"] is not None}
        srovnani_kriterium = puvodni.get("meta", {}).get("max_mimo", "bez kritéria")

    modely = sorted({z["model"] for v in vysledky.values() for z in v["behy"] if z.get("model")})
    meta = {
        "stitek": a.stitek,
        "datum": datetime.datetime.now().astimezone().strftime("%Y-%m-%d %H:%M %z"),
        "commit": _git("rev-parse", "--short", "HEAD") + (" (neuložené změny)" if _git("status", "--porcelain", "--", ".", ":!tools/evaly/vysledky") else ""),
        "otisk": _otisk_skillu(),
        "modely": ", ".join(modely) or "?",
        "hodnotitel": a.hodnotitel_model or "výchozí model claude",
        "behy": a.behy,
        "udpipe": a.udpipe or "vypnutý",
        "cena": sum(z.get("cena") or 0 for v in vysledky.values() for z in v["behy"]),
        "max_mimo": a.max_mimo,
        "nastroje_skillu": NASTROJE_SKILLU,
        "vstup_v_souboru": True,
        "zamitnuto": sum(bool(z.get("zamitnuto")) for v in vysledky.values() for z in v["behy"]),
        "behu_celkem": sum(len(v["behy"]) for v in vysledky.values()),
        "srovnani_kriterium": srovnani_kriterium,
        "opakovani_celkem": sum(z.get("pokusy", 1) - 1 for v in vysledky.values() for z in v["behy"])
                            + OPAKOVANI_HODNOTITELE[0],
        "nevyhodnoceno": sum(v["nevyhodnoceno"] for v in vysledky.values()),
    }

    cil = a.vystup or os.path.join(VYSLEDKY, a.stitek)
    os.makedirs(cil, exist_ok=True)
    with open(os.path.join(cil, "behy.json"), "w", encoding="utf-8") as f:
        json.dump({"meta": meta, "pripady": {str(k): v for k, v in vysledky.items()}},
                  f, ensure_ascii=False, indent=1)
    md = zprava(pripady, vysledky, meta, srovnani)
    with open(os.path.join(cil, "vysledky.md"), "w", encoding="utf-8") as f:
        f.write(md)
    print(md)
    print(f"Uloženo do {cil}", file=sys.stderr)


if __name__ == "__main__":
    main()
