#!/usr/bin/env python3
"""Hodnocení dojmu (návrh v CTENAR.md, oddíl Hodnocení dojmu): jak moc text zní jako AI, před přepisem a po něm.

Čtenářský test o 2–3 větách neprošel kalibrací K2 (člověk určil autora jen náhodou a model
ho zastoupit nemohl). Cílem skillu není, aby čtenář uhodl autora, ale aby text na čtenáře
nepůsobil jako AI. Proto se hodnotí dojem z jednoho textu naslepo na škále 1–4.

Kroky (každý jde přerušit a pustit znovu, hotové se přeskočí):
  generuj  – AI texty ve čtyřech žánrech, ve kterých se skill používá (e-mail, LinkedIn,
             blog, komentář), na témata z TEMATA; generující model se střídá (Haiku, Sonnet, Opus).
  prepis   – přepis každého textu skilly z konfigurace benchmarku (stejné adaptéry a zadání).
  list     – verze textů (originál a přepisy) bez názvů skillů, shodné texty jednou, náhodné
             pořadí bez dvou verzí téhož tématu za sebou; klíč zvlášť.
  vyhodnot – hodnocení {id: 1–4} proti klíči: průměr po verzích, rozdíl proti originálu.
Použití (z kořene repozitáře):
    python -I -X utf8 tools/benchmark/dojem.py generuj --stitek dojem-1
Data v DATA/dojem/<stitek>/, souhrny v tools/benchmark/vysledky/<stitek>/.
"""
import argparse
import collections
import concurrent.futures
import datetime
import json
import os
import random
import re
import sys
import threading

KOREN = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, KOREN)
import adaptery  # noqa: E402
import spoustec  # noqa: E402
import statistika  # noqa: E402
from cli import s_opakovanim, zavolej  # noqa: E402
from generuj import SYSTEM, ocisti  # noqa: E402
from korpus import slov  # noqa: E402

MODELY = ["claude-haiku-5-5", "claude-sonnet-5-5", "claude-opus-5-5"]
ZANRY = {
    "email": ("pracovní e-mail", 90),
    "linkedin": ("příspěvek na LinkedIn", 110),
    "blog": ("blogový článek", 150),
    "komentar": ("novinový komentář", 150),
}
ZADANI = ("Napiš {zanr} na téma: {tema}. Rozsah asi {n} slov. Vypiš jen samotný text, bez nadpisu. "
          "Nepoužívej zástupné značky v hranatých závorkách; jména a údaje, které potřebuješ, si vymysli.")
TEMATA = [
    ("email", "posunutí termínu odevzdání podkladů ke grantu o týden kvůli nemoci kolegyně"),
    ("email", "pozvánka kolegům na úterní poradu k novému docházkovému systému"),
    ("email", "žádost dodavateli o opravenou fakturu se špatnou sazbou DPH"),
    ("email", "poděkování týmu po víkendovém stěhování serverovny"),
    ("email", "odpověď zákazníkovi, proč se mu zpozdila dodávka kuchyňské linky"),
    ("linkedin", "co mě naučil první rok vedení malého týmu"),
    ("linkedin", "přechod z korporátu do neziskové organizace"),
    ("linkedin", "proč jsme ve firmě zrušili pondělní porady"),
    ("linkedin", "firma hledá juniorního testera"),
    ("linkedin", "postřeh z konference o veřejných zakázkách"),
    ("blog", "jak jsem přestal jezdit do práce v Brně autem"),
    ("blog", "pěstování rajčat na balkoně v paneláku"),
    ("blog", "domácí kvašení zelí"),
    ("blog", "rekonstrukce koupelny svépomocí a co bych příště udělal jinak"),
    ("blog", "týden bez sociálních sítí"),
    ("komentar", "rostoucí ceny obědů ve školních jídelnách"),
    ("komentar", "zavírání venkovských poboček pošty"),
    ("komentar", "zákaz mobilních telefonů ve školách"),
    ("komentar", "nedostatek praktických lékařů v menších městech"),
    ("komentar", "plánované zdražení jízdného v MHD"),
]
SKALA = {1: "zní jako člověk", 2: "spíš člověk", 3: "spíš AI", 4: "zní jako AI"}

_ZAMEK = threading.Lock()


def jsonl(cesta):
    return [json.loads(r) for r in open(cesta, encoding="utf-8")] if os.path.exists(cesta) else []


def pripis(cesta, z):
    with _ZAMEK:
        with open(cesta, "a", encoding="utf-8") as f:
            f.write(json.dumps(z, ensure_ascii=False) + "\n")


def norm(t):
    return " ".join((t or "").split())


# ---------------------------------------------------------------------------

def generuj(a, cfg, cil):
    p = os.path.join(cil, "ai.jsonl")
    hotovo = {z["id"] for z in jsonl(p)}
    ulohy = []
    for i, (zanr, tema) in enumerate(TEMATA, 1):
        tid = f"t{i:02d}"
        if tid not in hotovo:
            ulohy.append((tid, zanr, tema, MODELY[(i - 1) % len(MODELY)]))

    def jedna(tid, zanr, tema, model):
        nazev, n = ZANRY[zanr]
        r, chyby = s_opakovanim(zavolej, ZADANI.format(zanr=nazev, tema=tema, n=n), model, SYSTEM)
        if r is None:
            return {"id": tid, "chyba": chyby}
        text = ocisti(r["text"]).strip()
        z = {"id": tid, "zanr": zanr, "tema": tema, "model": model, "text": text, "slov": slov(text),
             "zastupne": bool(re.search(r"\[[^\]]{1,40}\]", text)), "cena": r["cena"]}
        pripis(p, z)
        return z

    with concurrent.futures.ThreadPoolExecutor(max_workers=a.jobs) as ex:
        for z in ex.map(lambda u: jedna(*u), ulohy):
            print(f"{z['id']}: {z.get('slov')} slov, {z.get('model')}, cena {z.get('cena', 0):.3f}"
                  + (" ZÁSTUPNÉ ZNAČKY" if z.get("zastupne") else "") + (f" CHYBA {z['chyba']}" if z.get("chyba") else ""),
                  file=sys.stderr)
    vse = jsonl(p)
    print(f"textů {len(vse)}, cena celkem {sum(z['cena'] for z in vse):.2f} USD", file=sys.stderr)


def prepis(a, cfg, cil):
    texty = {z["id"]: z for z in jsonl(os.path.join(cil, "ai.jsonl"))}
    p = os.path.join(cil, "prepisy.jsonl")
    hotovo = {(z["skill"], z["id"]) for z in jsonl(p) if z.get("finalni_text") is not None}
    utraceno = [sum(z.get("cena") or 0 for z in jsonl(p))]
    skilly = [adaptery.nacti(s) for s in cfg["skilly"] if not a.skilly or s["nazev"] in a.skilly.split(",")]
    b = cfg["behy"]
    ulohy = [(s, t) for t in texty.values() for s in skilly if (s.nazev, t["id"]) not in hotovo]
    print(f"úloh {len(ulohy)}, dosud {utraceno[0]:.2f} USD, strop {a.max_usd} USD", file=sys.stderr)
    stop = threading.Event()

    def jedna(s, t):
        if stop.is_set():
            return None
        r, chyby = s_opakovanim(spoustec.spust, s, t["text"], b["model_skillu"],
                                timeout=b.get("timeout_s", 900), effort=b.get("effort_skillu"))
        z = {"skill": s.nazev, "id": t["id"], "infra_chyby": chyby,
             "cas": datetime.datetime.now().astimezone().isoformat(timespec="seconds"), "otisk": s.otisk()}
        if r is not None:
            z.update({k: r.get(k) for k in ("vystup", "skill_nacten", "nastroje", "model", "cena", "tokeny",
                                            "kroku", "chyba", "zamitnuto")})
            z["finalni_text"] = spoustec.finalni_text(r["vystup"])
        with _ZAMEK:
            utraceno[0] += z.get("cena") or 0
            if utraceno[0] > a.max_usd:
                stop.set()
        pripis(p, z)
        return z

    with concurrent.futures.ThreadPoolExecutor(max_workers=a.jobs) as ex:
        for i, f in enumerate(concurrent.futures.as_completed([ex.submit(jedna, s, t) for s, t in ulohy]), 1):
            z = f.result()
            if z:
                stav = "bez verze" if z.get("finalni_text") is None else (
                    "beze změny" if norm(z["finalni_text"]) == norm(texty[z["id"]]["text"]) else "přepsáno")
                print(f"[{i}/{len(ulohy)}] {z['skill']} {z['id']}: {stav}, skill načten {z.get('skill_nacten')} "
                      f"({utraceno[0]:.2f} USD)", file=sys.stderr)
    if stop.is_set():
        print(f"Strop {a.max_usd} USD dosažen, zbytek nespuštěn.", file=sys.stderr)


def list_(a, cfg, cil):
    texty = {z["id"]: z for z in jsonl(os.path.join(cil, "ai.jsonl"))}
    prepisy = {}
    for z in jsonl(os.path.join(cil, "prepisy.jsonl")):
        if z.get("finalni_text") is not None:
            prepisy[(z["skill"], z["id"])] = z["finalni_text"].strip()
    skilly = [s["nazev"] for s in cfg["skilly"]]
    polozky = []  # (tid, text, [verze])
    for tid, t in sorted(texty.items()):
        po_textu = collections.OrderedDict()
        po_textu.setdefault(norm(t["text"]), (t["text"], []))[1].append("original")
        for s in skilly:
            if (s, tid) in prepisy:
                txt = prepisy[(s, tid)]
                po_textu.setdefault(norm(txt), (txt, []))[1].append(s)
        for txt, verze in po_textu.values():
            polozky.append((tid, txt, verze))
    rnd = random.Random(f"{cfg['seed']}:dojem:{a.stitek}")
    for _ in range(1000):  # žádné dvě verze téhož tématu za sebou
        rnd.shuffle(polozky)
        if all(polozky[i][0] != polozky[i + 1][0] for i in range(len(polozky) - 1)):
            break
    list_out, klic = [], {}
    for i, (tid, txt, verze) in enumerate(polozky, 1):
        iid = f"i{i:03d}"
        list_out.append({"id": iid, "zanr": ZANRY[texty[tid]["zanr"]][0], "text": txt})
        klic[iid] = {"tema": tid, "verze": verze}
    json.dump(list_out, open(os.path.join(cil, "list.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(klic, open(os.path.join(cil, "klic.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    slova = sum(slov(x["text"]) for x in list_out)
    print(f"{len(list_out)} položek ({len(texty)} témat), {slova} slov k přečtení; klíč v klic.json", file=sys.stderr)


def vyhodnot(a, cfg, cil):
    klic = json.load(open(os.path.join(cil, "klic.json"), encoding="utf-8"))
    hodn = json.load(open(a.hodnoceni, encoding="utf-8"))
    skilly = ["original"] + [s["nazev"] for s in cfg["skilly"]]
    po = collections.defaultdict(dict)  # verze -> {tema: hodnoceni}
    for iid, k in klic.items():
        h = hodn.get(iid)
        if isinstance(h, dict):
            h = h.get("hodnoceni")
        if h not in (1, 2, 3, 4):
            continue
        for v in k["verze"]:
            po[v][k["tema"]] = float(h)
    shluky = {t: t for t in {k["tema"] for k in klic.values()}}
    vys = {"hodnoceno": sum(1 for i in klic if hodn.get(i) is not None), "polozek": len(klic), "verze": {}}
    for v in skilly:
        h = po.get(v, {})
        if not h:
            continue
        r = {"n": len(h), "prumer": sum(h.values()) / len(h),
             "podil_ai": sum(1 for x in h.values() if x >= 3) / len(h)}
        if v != "original":
            d = statistika.bootstrap_rozdil(po["original"], h, shluky, seed=cfg["seed"])
            if d:
                r["pokles_proti_originalu"] = {"bod": d[0], "dolni": d[1], "horni": d[2]}
            r["beze_zmeny"] = sum(1 for k in klic.values() if v in k["verze"] and "original" in k["verze"])
        vys["verze"][v] = r
    for v in skilly[1:]:
        for w in skilly[1:]:
            if v < w and po.get(v) and po.get(w):
                d = statistika.bootstrap_rozdil(po[w], po[v], shluky, seed=cfg["seed"])
                vys.setdefault("dvojice", {})[f"{w} − {v}"] = {"bod": d[0], "dolni": d[1], "horni": d[2]}
    out = os.path.join(KOREN, "vysledky", a.stitek)
    os.makedirs(out, exist_ok=True)
    json.dump(vys, open(os.path.join(out, "souhrn.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps(vys, ensure_ascii=False, indent=1))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("krok", choices=["generuj", "prepis", "list", "vyhodnot"])
    ap.add_argument("--stitek", required=True)
    ap.add_argument("--konfigurace", default=os.path.join(KOREN, "konfigurace.json"))
    ap.add_argument("--skilly", help="prepis: jen tyto skilly (čárkami)")
    ap.add_argument("--jobs", type=int, default=6)
    ap.add_argument("--max-usd", type=float, default=12.0, help="prepis: strop útraty včetně dřívějších běhů")
    ap.add_argument("--hodnoceni", help="vyhodnot: JSON {id: 1–4}")
    a = ap.parse_args()
    cfg = json.load(open(a.konfigurace, encoding="utf-8"))
    cil = os.path.join(os.path.expanduser(cfg["data"]), "dojem", a.stitek)
    os.makedirs(cil, exist_ok=True)
    {"generuj": generuj, "prepis": prepis, "list": list_, "vyhodnot": vyhodnot}[a.krok](a, cfg, cil)


if __name__ == "__main__":
    main()
