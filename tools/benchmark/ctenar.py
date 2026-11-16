#!/usr/bin/env python3
"""Čtenářský test (návrh v CTENAR.md): pozná čtenář, který ze dvou krátkých úryvků napsal člověk?

Dvojice: lidský úryvek a AI úryvek o 2–3 větách (20–60 slov), délky ve dvojici nejvýš 1,5×.
  pokracovani – první okno za začátkem (~100 slov), u autora i u modelu na stejném místě;
  chatbot     – okno od věty nejblíž 40 % délky textu, u obou stran.
Čtenář (model) dostane každou dvojici dvakrát s prohozeným pořadím; skóre dvojice je podíl
správných odpovědí (1, 0,5, nebo 0).

Režim `kalibrace` (K1): jen AI originály z dev sady, rozhodovací vrstvy. Test sadu nečte.
Běh jde přerušit a pustit znovu se stejným štítkem: hotové odpovědi se přeskočí, takže
`--pocet 10` (pilot) a potom `--pocet 120` (K1) dají jeden běh.

Použití (z kořene repozitáře):
    python -I -X utf8 tools/benchmark/ctenar.py kalibrace --stitek ctenar-k1 --pocet 10 [--nanecisto]
Výstupy: DATA/ctenar/<stitek>/dvojice.jsonl a odpovedi.jsonl (texty a odpovědi),
tools/benchmark/vysledky/<stitek>/souhrn.json a vysledky.md (jen souhrnná čísla).
"""
import argparse
import collections
import concurrent.futures
import datetime
import hashlib
import json
import os
import random
import re
import sys
import threading

KOREN = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, KOREN)
from cli import s_opakovanim, zavolej  # noqa: E402
from generuj import rozdel_prefix  # noqa: E402
from korpus import slov, vety  # noqa: E402
import statistika  # noqa: E402

ROZHODOVACI = ("klasika", "wiki", "uredni")
MIN_SLOV, MAX_SLOV, MAX_POMER = 20, 60, 1.5
CTENAR = "claude-opus-5-5"

SYSTEM = "Čteš české texty a odpovídáš jen ve formátu, o který tě někdo požádá."
ZADANI = """Jeden z úryvků napsal člověk, druhý jazykový model. Který napsal člověk?

<A>
{a}
</A>

<B>
{b}
</B>

Odpověz jen JSON: {{"clovek": "A" nebo "B", "jistota": 1 až 3, "proc": "nejvýš 15 slov"}}."""
SCHEMA = {"type": "object", "additionalProperties": False,
          "required": ["clovek", "jistota", "proc"],
          "properties": {"clovek": {"type": "string", "enum": ["A", "B"]},
                         "jistota": {"type": "integer", "minimum": 1, "maximum": 3},
                         "proc": {"type": "string"}}}

# jako kontaminace.py: tučné, nadpis, oddělovač, odrážka, kurzíva
_MARKDOWN = re.compile(r"\*\*[^*\n]+\*\*|^\s*(#{1,6}\s|---\s*$|[-*•]\s)|(?<!\w)\*[^*\n]+\*(?!\w)", re.M)
_KONEC_VETY = re.compile(r"[.!?…][\"“”»)]*$")
_PRIMA_REC = re.compile(r"^[„\"»«–—-]")

_ZAMEK = threading.Lock()


# ---------------------------------------------------------------------------
# Okna

def seznam_vet(text):
    """Věty textu v pořadí, napříč odstavci."""
    out = []
    for o in text.strip().split("\n\n"):
        o = " ".join(o.split())
        if o:
            out.extend(v.strip() for v in vety(o) if v.strip())
    return out


def platne_okno(vv):
    """Okno o 2–3 větách: každá věta končí interpunkcí, bez markdownu, ne jen přímá řeč."""
    if not all(_KONEC_VETY.search(v) for v in vv):
        return False
    if any(_MARKDOWN.search(v) for v in vv):
        return False
    if all(_PRIMA_REC.match(v) for v in vv):
        return False
    return True


def varianty_okna(vv, start, posunu=3):
    """Kandidátní okna (2 a 3 věty) od `start`, případně o pár vět dál. Vrátí [(start, n, text, slov)]."""
    out = []
    for s in range(start, min(start + posunu + 1, len(vv))):
        for n in (3, 2):
            if s + n > len(vv):
                continue
            okno = vv[s:s + n]
            w = sum(slov(v) for v in okno)
            if MIN_SLOV <= w <= MAX_SLOV and platne_okno(okno):
                out.append((s, n, " ".join(okno), w))
        if out:
            return out  # nejbližší možný začátek
    return out


def start_40(vv):
    celkem = sum(slov(v) for v in vv)
    cil, k = 0.4 * celkem, 0
    for i, v in enumerate(vv):
        if k + slov(v) / 2 >= cil:
            return i
        k += slov(v)
    return 0


def dvojice_oken(lidske_vv, ai_vv, metoda):
    """Vybere okna obou stran s nejmenším poměrem délek (≤ 1,5). Vrátí dict, nebo důvod vyřazení."""
    if metoda == "pokracovani":
        sl, sa = 0, 0
    else:
        sl, sa = start_40(lidske_vv), start_40(ai_vv)
    kl, ka = varianty_okna(lidske_vv, sl), varianty_okna(ai_vv, sa)
    if not kl:
        return "lidské okno"
    if not ka:
        return "AI okno"
    nej = min(((max(l[3], a[3]) / min(l[3], a[3]), l, a) for l in kl for a in ka), key=lambda x: x[0])
    if nej[0] > MAX_POMER:
        return "poměr délek"
    _, l, a = nej
    return {"lidsky": l[2], "lidsky_slov": l[3], "lidsky_okno": [l[0], l[1]],
            "ai": a[2], "ai_slov": a[3], "ai_okno": [a[0], a[1]]}


# ---------------------------------------------------------------------------
# Data

def nacti_dev(data, prefix_slov):
    manifest = {z["id"]: z for z in json.load(open(os.path.join(data, "manifest.json"),
                                                   encoding="utf-8"))["texty"]}
    koren = os.path.join(data, "dev")
    lidske = {}
    for f in sorted(os.listdir(os.path.join(koren, "texty"))):
        id_ = f[:-4]
        if manifest[id_]["vrstva"] in ROZHODOVACI:
            lidske[id_] = open(os.path.join(koren, "texty", f), encoding="utf-8").read()
    kand, vyrazeno = [], collections.Counter()
    for metoda in ("pokracovani", "chatbot"):
        for model in sorted(os.listdir(os.path.join(koren, "ai", metoda))):
            for f in sorted(os.listdir(os.path.join(koren, "ai", metoda, model))):
                id_ = f[:-4]
                if id_ not in lidske:
                    continue
                ai_text = open(os.path.join(koren, "ai", metoda, model, f), encoding="utf-8").read()
                lidsky = lidske[id_]
                if metoda == "pokracovani":
                    lidsky = rozdel_prefix(lidsky, prefix_slov)[1]
                d = dvojice_oken(seznam_vet(lidsky), seznam_vet(ai_text), metoda)
                if isinstance(d, str):
                    vyrazeno[(metoda, d)] += 1
                    continue
                d.update({"klic": f"{metoda}/{model}/{id_}", "metoda": metoda, "model": model,
                          "id_lidsky": id_, "vrstva": manifest[id_]["vrstva"], "shluk": manifest[id_]["dilo"]})
                kand.append(d)
    return kand, vyrazeno


def vyber_kalibrace(kand, pocet, seed):
    """Polovina pokračování, polovina chatbotů; nejvýš 2 dvojice na zdroj a metodu.
    Pořadí je pevné (seed), takže menší počet je začátkem většího."""
    rnd = random.Random(f"{seed}:ctenar:kalibrace")
    po_metode = {}
    for m in ("pokracovani", "chatbot"):
        k = sorted((d for d in kand if d["metoda"] == m), key=lambda d: d["klic"])
        rnd.shuffle(k)
        pocty, out = collections.Counter(), []
        for d in k:
            if pocty[d["id_lidsky"]] < 2:
                out.append(d)
                pocty[d["id_lidsky"]] += 1
        po_metode[m] = out
    vyb = []
    for i in range(max(len(v) for v in po_metode.values())):
        for m in ("pokracovani", "chatbot"):
            if i < len(po_metode[m]):
                vyb.append(po_metode[m][i])
    return vyb[:pocet]


# ---------------------------------------------------------------------------
# Čtenář

def precti(d, poradi):
    """poradi 'LA' = lidský úryvek jako A. Vrátí záznam odpovědi."""
    a, b = (d["lidsky"], d["ai"]) if poradi == "LA" else (d["ai"], d["lidsky"])
    r, chyby = s_opakovanim(zavolej, ZADANI.format(a=a, b=b), CTENAR, SYSTEM, schema=SCHEMA)
    z = {"klic": d["klic"], "podminka": d.get("podminka", "original"), "poradi": poradi,
         "chyby": chyby, "cas": datetime.datetime.now().astimezone().isoformat(timespec="seconds")}
    if r is None:
        z.update({"nevyhodnoceno": True, "cena": 0.0})
        return z
    o = r.get("structured")
    if not isinstance(o, dict):
        try:
            o = json.loads(re.search(r"\{.*\}", r["text"], re.S).group(0))
        except (AttributeError, ValueError):
            o = {}
    spravne = {"LA": "A", "AL": "B"}[poradi]
    z.update({"odpoved": o, "spravne": o.get("clovek") == spravne if o.get("clovek") in ("A", "B") else None,
              "cena": r["cena"], "model": r["model"], "tokeny": r["tokeny"]})
    return z


def skore_dvojic(odpovedi):
    """{(klic, podminka): skóre} ze dvou pořadí; dvojice bez obou platných odpovědí se vynechá."""
    po = collections.defaultdict(dict)
    for z in odpovedi:
        if z.get("spravne") is not None:
            po[(z["klic"], z["podminka"])][z["poradi"]] = z["spravne"]
    return {k: (v["LA"] + v["AL"]) / 2 for k, v in po.items() if len(v) == 2}


def interval_prumeru(hodnoty, shluky, seed):
    nuly = {k: 0.0 for k in hodnoty}
    return statistika.bootstrap_rozdil(hodnoty, nuly, shluky, seed=seed)


# ---------------------------------------------------------------------------
# Zpráva

def souhrn(dvojice, odpovedi, seed):
    sk = skore_dvojic(odpovedi)
    d_of = {d["klic"]: d for d in dvojice}
    sk = {k: v for k, v in sk.items() if k[0] in d_of}
    shluky = {k: d_of[k[0]]["shluk"] for k in sk}

    def skupina(filtr):
        h = {k: v for k, v in sk.items() if filtr(d_of[k[0]])}
        if not h:
            return None
        bod, dol, hor = interval_prumeru(h, shluky, seed)
        return {"dvojic": len(h), "uspesnost": bod, "dolni": dol, "horni": hor,
                "rozporne": sum(1 for v in h.values() if v == 0.5)}

    odp = [z for z in odpovedi if z["klic"] in d_of]
    jistota = collections.Counter((z.get("odpoved") or {}).get("jistota") for z in odp if z.get("spravne") is not None)
    s = {"vse": skupina(lambda d: True)}
    for m in ("pokracovani", "chatbot"):
        s[f"metoda:{m}"] = skupina(lambda d, m=m: d["metoda"] == m)
    for v in ROZHODOVACI:
        s[f"vrstva:{v}"] = skupina(lambda d, v=v: d["vrstva"] == v)
    for mod in sorted({d["model"] for d in dvojice}):
        s[f"model:{mod}"] = skupina(lambda d, mod=mod: d["model"] == mod)
    return {"skupiny": s,
            "odpovedi": len(odp),
            "nevyhodnoceno": sum(1 for z in odp if z.get("nevyhodnoceno")),
            "bez_platne_odpovedi": sum(1 for z in odp if not z.get("nevyhodnoceno") and z.get("spravne") is None),
            "uspesnost_podle_jistoty": {str(j): {"odpovedi": n, "spravne": sum(
                1 for z in odp if (z.get("odpoved") or {}).get("jistota") == j and z.get("spravne"))}
                for j, n in sorted(jistota.items(), key=lambda x: str(x[0]))},
            "cena": sum(z.get("cena") or 0 for z in odp),
            "slov_median": {"lidsky": sorted(d["lidsky_slov"] for d in dvojice)[len(dvojice) // 2],
                            "ai": sorted(d["ai_slov"] for d in dvojice)[len(dvojice) // 2]}}


def zprava(meta, s):
    def f(x):
        return f"{x * 100:.0f} %".replace(".", ",")
    r = [f"# Čtenářský test: {meta['stitek']}\n",
         f"- Datum: {meta['datum']}; režim: {meta['rezim']}; sada: dev, vrstvy {', '.join(ROZHODOVACI)}",
         f"- Čtenář: {meta['ctenar']}, každá dvojice ve dvou pořadích; commit `{meta['commit']}`",
         f"- Dvojic: {meta['dvojic']} (kandidátů {meta['kandidatu']}); úryvky 2–3 věty, {MIN_SLOV}–{MAX_SLOV} slov, "
         f"medián slov lidský {s['slov_median']['lidsky']}, AI {s['slov_median']['ai']}",
         f"- Odpovědí: {s['odpovedi']}; nevyhodnoceno: {s['nevyhodnoceno']}; bez platné odpovědi: "
         f"{s['bez_platne_odpovedi']}; cena {s['cena']:.2f} USD",
         f"- Vyřazené kandidátní dvojice: {meta['vyrazeno'] or 'žádné'}", "",
         "Úspěšnost = podíl dvojic, ve kterých čtenář správně určil lidský úryvek (rozporná pořadí 0,5). "
         "Interval: bootstrap 95 % po shlucích (dílo).", "",
         "| skupina | dvojic | úspěšnost | interval | rozporná pořadí |", "|---|---|---|---|---|"]
    for k, v in s["skupiny"].items():
        if v:
            r.append(f"| {k} | {v['dvojic']} | {f(v['uspesnost'])} | [{f(v['dolni'])}; {f(v['horni'])}] | {v['rozporne']} |")
    v = s["skupiny"]["vse"]
    if v:
        ok = v["uspesnost"] >= 0.70 and v["dolni"] >= 0.60
        r += ["", f"**K1 (úspěšnost ≥ 70 % a dolní mez ≥ 60 %): {'splněno' if ok else 'nesplněno'}.**"]
    r += ["", "Úspěšnost podle jistoty čtenáře (jednotlivé odpovědi): " + "; ".join(
        f"{j}: {x['spravne']}/{x['odpovedi']}" for j, x in s["uspesnost_podle_jistoty"].items())]
    return "\n".join(r) + "\n"


# ---------------------------------------------------------------------------

def k2_list(a, cfg, data):
    """30 dvojic z běhu --z (K1) pro uživatele: list bez klíče a klíč zvlášť (DATA/ctenar/<stitek>/)."""
    zdroj = os.path.join(data, "ctenar", a.z)
    dvojice = [json.loads(r) for r in open(os.path.join(zdroj, "dvojice.jsonl"), encoding="utf-8")]
    rnd = random.Random(f"{cfg['seed']}:ctenar:k2")
    vyber = sorted(dvojice, key=lambda d: d["klic"])
    rnd.shuffle(vyber)
    vyber = vyber[:a.pocet]
    list_, klic = [], {}
    for i, d in enumerate(vyber, 1):
        pid = f"p{i:02d}"
        lidsky = rnd.choice("AB")
        a_text, b_text = (d["lidsky"], d["ai"]) if lidsky == "A" else (d["ai"], d["lidsky"])
        list_.append({"id": pid, "a": a_text, "b": b_text})
        klic[pid] = {"klic": d["klic"], "lidsky": lidsky, "metoda": d["metoda"], "vrstva": d["vrstva"],
                     "shluk": d["shluk"]}
    cil = os.path.join(data, "ctenar", a.stitek)
    os.makedirs(cil, exist_ok=True)
    json.dump(list_, open(os.path.join(cil, "list.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(klic, open(os.path.join(cil, "klic.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"{len(list_)} dvojic: {os.path.join(cil, 'list.json')} (bez klíče), klíč v klic.json", file=sys.stderr)


def k2_vyhodnot(a, cfg, data):
    """Odpovědi uživatele (JSON {pid: "A"|"B"}) proti klíči a proti modelu z běhu --z."""
    cil = os.path.join(data, "ctenar", a.stitek)
    klic = json.load(open(os.path.join(cil, "klic.json"), encoding="utf-8"))
    volby = json.load(open(a.odpovedi, encoding="utf-8"))
    odp_modelu = [json.loads(r) for r in open(os.path.join(data, "ctenar", a.z, "odpovedi.jsonl"), encoding="utf-8")]
    model = skore_dvojic(odp_modelu)
    radky, uziv, shoda, shluky = [], {}, {}, {}
    for pid, k in sorted(klic.items()):
        v = volby.get(pid)
        if v not in ("A", "B"):
            continue
        u = 1.0 if v == k["lidsky"] else 0.0
        m = model.get((k["klic"], "original"))
        uziv[pid] = u
        shluky[pid] = k["shluk"]
        if m is not None:
            shoda[pid] = 1 - abs(u - m)
        radky.append({"id": pid, "uzivatel": u, "model": m, **{x: k[x] for x in ("metoda", "vrstva")}})
    vys = {"dvojic": len(uziv)}
    for nazev, h in (("uspesnost_uzivatele", uziv), ("shoda_s_modelem", shoda)):
        if h:
            bod, dol, hor = interval_prumeru(h, shluky, cfg["seed"])
            vys[nazev] = {"bod": bod, "dolni": dol, "horni": hor, "n": len(h)}
    m_na_listu = [r["model"] for r in radky if r["model"] is not None]
    vys["uspesnost_modelu_na_listu"] = sum(m_na_listu) / len(m_na_listu) if m_na_listu else None
    vys["k2_splneno"] = bool(vys.get("shoda_s_modelem") and vys["shoda_s_modelem"]["bod"] >= 0.70)
    for metoda in ("pokracovani", "chatbot"):
        rr = [r for r in radky if r["metoda"] == metoda]
        vys[f"uzivatel:{metoda}"] = {"n": len(rr), "spravne": sum(r["uzivatel"] for r in rr)}
    json.dump({"souhrn": vys, "dvojice": radky}, open(os.path.join(cil, "vyhodnoceni.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    out = os.path.join(KOREN, "vysledky", a.stitek)
    os.makedirs(out, exist_ok=True)
    json.dump(vys, open(os.path.join(out, "souhrn.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps(vys, ensure_ascii=False, indent=1))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("rezim", choices=["kalibrace", "k2-list", "k2-vyhodnot"])
    ap.add_argument("--z", default="ctenar-k1", help="k2: běh K1, ze kterého se berou dvojice a odpovědi modelu")
    ap.add_argument("--odpovedi", help="k2-vyhodnot: JSON {pid: 'A'|'B'} s volbami uživatele")
    ap.add_argument("--stitek", required=True)
    ap.add_argument("--konfigurace", default=os.path.join(KOREN, "konfigurace.json"))
    ap.add_argument("--pocet", type=int, default=120, help="dvojic (výchozí 120)")
    ap.add_argument("--jobs", type=int, default=6)
    ap.add_argument("--max-usd", type=float, default=8.0, help="strop útraty běhu včetně dřívějších odpovědí")
    ap.add_argument("--nanecisto", action="store_true", help="jen sestaví dvojice, čtenáře nevolá")
    a = ap.parse_args()

    cfg = json.load(open(a.konfigurace, encoding="utf-8"))
    data = os.path.expanduser(cfg["data"])
    if a.rezim == "k2-list":
        return k2_list(a, cfg, data)
    if a.rezim == "k2-vyhodnot":
        return k2_vyhodnot(a, cfg, data)
    kand, vyrazeno = nacti_dev(data, cfg["generovani"]["prefix_slov"])
    dvojice = vyber_kalibrace(kand, a.pocet, cfg["seed"])
    print(f"kandidátů {len(kand)}, vybráno {len(dvojice)}; vyřazeno {dict(vyrazeno)}", file=sys.stderr)

    cil_data = os.path.join(data, "ctenar", a.stitek)
    os.makedirs(cil_data, exist_ok=True)
    with open(os.path.join(cil_data, "dvojice.jsonl"), "w", encoding="utf-8") as f:
        for d in dvojice:
            f.write(json.dumps(d, ensure_ascii=False) + "\n")
    if a.nanecisto:
        for d in dvojice[:4]:
            print(f"\n[{d['klic']}] {d['vrstva']}, lidský {d['lidsky_slov']} slov, AI {d['ai_slov']} slov\n"
                  f"  L: {d['lidsky']}\n  AI: {d['ai']}")
        return

    p_odp = os.path.join(cil_data, "odpovedi.jsonl")
    odpovedi = [json.loads(r) for r in open(p_odp, encoding="utf-8")] if os.path.exists(p_odp) else []
    hotovo = {(z["klic"], z["podminka"], z["poradi"]) for z in odpovedi if not z.get("nevyhodnoceno")}
    ulohy = [(d, p) for d in dvojice for p in ("LA", "AL") if (d["klic"], "original", p) not in hotovo]
    utraceno = sum(z.get("cena") or 0 for z in odpovedi)
    print(f"úloh {len(ulohy)}, dosud utraceno {utraceno:.2f} USD", file=sys.stderr)
    stop = threading.Event()

    def jedna(d, p):
        if stop.is_set():
            return None
        z = precti(d, p)
        with _ZAMEK:
            nonlocal utraceno
            utraceno += z.get("cena") or 0
            if utraceno > a.max_usd:
                stop.set()
            with open(p_odp, "a", encoding="utf-8") as f:
                f.write(json.dumps(z, ensure_ascii=False) + "\n")
        return z

    with concurrent.futures.ThreadPoolExecutor(max_workers=a.jobs) as ex:
        for i, fu in enumerate(concurrent.futures.as_completed([ex.submit(jedna, d, p) for d, p in ulohy]), 1):
            z = fu.result()
            if z:
                odpovedi.append(z)
                print(f"[{i}/{len(ulohy)}] {z['klic']} {z['poradi']}: "
                      f"{'nevyhodnoceno' if z.get('nevyhodnoceno') else z.get('spravne')} ({utraceno:.2f} USD)",
                      file=sys.stderr)
    if stop.is_set():
        print(f"Strop {a.max_usd} USD dosažen, zbytek nespuštěn.", file=sys.stderr)

    s = souhrn(dvojice, odpovedi, cfg["seed"])
    import subprocess
    commit = subprocess.run(["git", "-C", KOREN, "rev-parse", "--short", "HEAD"], capture_output=True,
                            text=True).stdout.strip()
    meta = {"stitek": a.stitek, "rezim": a.rezim, "ctenar": CTENAR, "commit": commit,
            "datum": datetime.datetime.now().astimezone().strftime("%Y-%m-%d %H:%M %z"),
            "dvojic": len(dvojice), "kandidatu": len(kand),
            "vyrazeno": ", ".join(f"{m} {d} {n}" for (m, d), n in sorted(vyrazeno.items())),
            "dvojice_sha256": hashlib.sha256(open(os.path.join(cil_data, "dvojice.jsonl"), "rb").read()).hexdigest()}
    cil = os.path.join(KOREN, "vysledky", a.stitek)
    os.makedirs(cil, exist_ok=True)
    with open(os.path.join(cil, "souhrn.json"), "w", encoding="utf-8") as f:
        json.dump({"meta": meta, "souhrn": s}, f, ensure_ascii=False, indent=1)
    md = zprava(meta, s)
    with open(os.path.join(cil, "vysledky.md"), "w", encoding="utf-8") as f:
        f.write(md)
    print(md)


if __name__ == "__main__":
    main()
