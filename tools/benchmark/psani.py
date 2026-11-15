#!/usr/bin/env python3
"""Test režimu psaní: skill píše nový text podle zadání (PLAN.md, krok 9).

Hlavní benchmark měří kontrolu a přepis hotového textu. To je úloha, pro kterou je stavěný
unslop-cs; anti-ai-slop-cz je hlavně návod, jak psát. Tady dostane každý skill stejné chatbotí
zadání z dev sady („Napiš <žánr> na téma X, asi N slov“, stejná témata jako AI protějšky (b))
a výstup se hodnotí stejným nezávislým skóre AI-ovosti (rysy F0, rysy.py) jako přepisy.
humanizer-czech se netestuje: podle svého popisu text jen upravuje, nepíše.

Metriky na text:
  skore          skóre AI-ovosti výstupu (0 = jako lidský text, 1 = jako AI); hlavní metrika
  delka          počet slov / požadovaný počet
  cisla          výstup obsahuje číslo nebo datum (zadání žádné nemá, takže jde o doplněné údaje;
                 u tiskové zprávy nebo hesla bývají namístě, proto jen k výkladu)
  znacky         výstup obsahuje zástupnou značku typu [datum] nebo markdown
Srovnání A − B na stejných tématech, bootstrap po shlucích (zdrojové dílo). Do rozhodovacího
pravidla v kroku 7 nevstupuje; vykazuje se zvlášť.

Použití (z kořene repozitáře; spouštět `python -E -P`, rysy potřebují ufal.udpipe a numpy):
  python -E -P tools/benchmark/psani.py --konfigurace tools/benchmark/konfigurace-160.json \\
      --stitek psani-1 [--jen 3] [--max-usd 20] [--prevzit psani-0]
Výstupy: DATA/psani/<stitek>/behy.jsonl (texty) a tools/benchmark/vysledky/<stitek>/
(souhrn.json, vysledky.md, bez textů). Běh jde přerušit a pustit znovu se stejným štítkem.
"""
import argparse
import collections
import concurrent.futures
import copy
import datetime
import json
import os
import random
import re
import sys

KOREN = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, KOREN)
import adaptery  # noqa: E402
import spoustec  # noqa: E402
import statistika  # noqa: E402
from benchmark import DOMACI, Rozpocet, Zapisovac, git  # noqa: E402
from cli import s_opakovanim  # noqa: E402
from generuj import ZADANI_CHATBOT, ZANRY  # noqa: E402
from korpus import slov  # noqa: E402
from zachovani import _cisla  # noqa: E402

SKILLY = ("unslop-cs", "anti-ai-slop-cz", "bez-skillu")
VYVOLANI = {
    "unslop-cs": "Použij skill unslop-cs (unslop-cs:unslop-cs) v režimu psaní.",
    "anti-ai-slop-cz": "Použij skill anti-ai-slop-cz (anti-ai-slop-cz:anti-ai-slop-cz).",
    "bez-skillu": "",
}
KONEC = "\nHotový text dej mezi dva samostatné řádky <<<VERZE a VERZE>>>."
_ZNACKA = re.compile(r"\[[^\]\n]{1,40}\]|\*\*|^#+ |^\s*[-*] ", re.M)


class Psani:
    """Obal adaptéru: stejný plugin, nástroje a název skillu, jiné zadání a bez vstupního souboru."""

    def __init__(self, adapter):
        self.__dict__.update(copy.copy(adapter.__dict__))
        for k in ("nazev", "plugin_dir", "skill", "nastroje", "otisk_cesta"):
            setattr(self, k, getattr(adapter, k))
        self.vstup_v_souboru = False
        self._adapter = adapter

    def zadani(self, zadani_psani):
        vyv = VYVOLANI[self.nazev]
        return (vyv + "\n" if vyv else "") + zadani_psani + KONEC

    def otisk(self):
        return self._adapter.otisk()


def ulohy(data, rnd, jen):
    manifest = {z["id"]: z for z in json.load(open(os.path.join(data, "manifest.json"),
                                                   encoding="utf-8"))["texty"]}
    temata = json.load(open(os.path.join(data, "ai", "temata.json"), encoding="utf-8"))
    ids = sorted(f[:-4] for f in os.listdir(os.path.join(data, "dev", "texty")) if f.endswith(".txt"))
    out = []
    for id_ in ids:
        if id_ not in temata:
            continue
        z = manifest[id_]
        n = round(z["slov"], -1)
        out.append({"id": id_, "vrstva": z["vrstva"], "shluk": z["dilo"], "n": n,
                    "zadani": ZADANI_CHATBOT.format(zanr=ZANRY.get(z["zanr"], "text"), tema=temata[id_], n=n),
                    "lidsky": open(os.path.join(data, "dev", "texty", id_ + ".txt"), encoding="utf-8").read()})
    if jen:
        rnd.shuffle(out)
        out = sorted(out[:jen], key=lambda u: u["id"])
    return out


def beh(adapter, u, cfg, rozpocet):
    if rozpocet.stop:
        return None
    b = cfg["behy"]
    r, chyby = s_opakovanim(spoustec.spust, adapter, u["zadani"], b["model_skillu"],
                            timeout=b.get("timeout_s", 900), effort=b.get("effort_skillu"))
    z = {"klic": f"{adapter.nazev}|{u['id']}", "skill": adapter.nazev, "id": u["id"], "infra_chyby": chyby,
         "zadani": adapter.zadani(u["zadani"]), "otisk": adapter.otisk(), "model_pozadovany": b["model_skillu"],
         "effort": b.get("effort_skillu")}
    if r is None:
        z["nevyhodnoceno"] = True
        return z
    rozpocet.pridej(r["cena"])
    z.update({k: r.get(k) for k in ("vystup", "skill_nacten", "nastroje", "model", "cena", "tokeny", "kroku",
                                "cas_s", "chyba", "zamitnuto", "verze_cli")})
    z["text"] = spoustec.finalni_text(r["vystup"])
    return z


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--konfigurace", required=True)
    ap.add_argument("--stitek", required=True)
    ap.add_argument("--jen", type=int, help="jen N náhodných témat (pilot)")
    ap.add_argument("--max-usd", type=float, default=20.0)
    ap.add_argument("--prevzit", metavar="STITEK",
                    help="převzít běhy z dřívějšího štítku, když sedí otisk skillu, zadání, model a effort")
    a = ap.parse_args()
    cfg = json.load(open(a.konfigurace, encoding="utf-8"))
    data = os.path.expanduser(cfg["data"])
    spec = {s["nazev"]: s for s in cfg["skilly"]}
    skilly = [Psani(adaptery.nacti(spec.get(n) or {"nazev": n, "adapter": "bez_skillu"})) for n in SKILLY]
    uu = ulohy(data, random.Random(f"{cfg['seed']}:{a.stitek}:psani"), a.jen)
    print(f"témat {len(uu)}, skillů {len(skilly)}", flush=True)

    behy_dir = os.path.join(data, "psani", a.stitek)
    os.makedirs(behy_dir, exist_ok=True)
    zb = Zapisovac(os.path.join(behy_dir, "behy.jsonl"))
    if a.prevzit:
        otisky = {s.nazev: s.otisk() for s in skilly}
        zadani = {f"{s.nazev}|{u['id']}": s.zadani(u["zadani"]) for u in uu for s in skilly}
        prevzato = 0
        for radek in open(os.path.join(data, "psani", a.prevzit, "behy.jsonl"), encoding="utf-8"):
            z = json.loads(radek)
            if (z["klic"] in zadani and z["klic"] not in zb.hotove and not z.get("nevyhodnoceno")
                    and z["skill"] in otisky and z.get("otisk") == otisky[z["skill"]]
                    and z.get("zadani") == zadani[z["klic"]]
                    and z.get("model_pozadovany") == cfg["behy"]["model_skillu"]
                    and z.get("effort") == cfg["behy"].get("effort_skillu")):
                zb.zapis({**z, "prevzato": a.prevzit})
                prevzato += 1
        print(f"převzato {prevzato} běhů z {a.prevzit}", flush=True)
    rozpocet = Rozpocet(a.max_usd, sum(z.get("cena") or 0 for z in zb.hotove.values() if not z.get("prevzato")))
    prace = [(s, u) for u in uu for s in skilly if f"{s.nazev}|{u['id']}" not in zb.hotove]
    with concurrent.futures.ThreadPoolExecutor(max_workers=cfg["behy"].get("jobs", 4)) as ex:
        for i, fut in enumerate(concurrent.futures.as_completed(
                [ex.submit(beh, s, u, cfg, rozpocet) for s, u in prace]), 1):
            z = fut.result()
            if z:
                zb.zapis(z)
                print(f"[{i}/{len(prace)}] {z['klic']} {'nevyhodnoceno' if z.get('nevyhodnoceno') else 'ok'} "
                      f"{rozpocet.cena:.2f} USD", flush=True)
    if rozpocet.stop:
        print(f"POZOR: strop {rozpocet.max} USD, výsledky jsou neúplné", flush=True)

    import numpy  # noqa: F401,PLC0415  (rysy potřebují numpy; chyba dřív než po placených bězích nevadí)
    from rysy import Analyzator, skore  # noqa: PLC0415
    model = json.load(open(os.path.join(data, "modely", "ai_skore.json"), encoding="utf-8"))
    an = Analyzator(os.path.expanduser(cfg["udpipe"]), os.path.join(data, "cache_udpipe"))
    u_of = {u["id"]: u for u in uu}
    lidske_skore = dict(zip(u_of, skore([u["lidsky"] for u in uu], model, an)))
    met = {}
    for z in zb.hotove.values():
        if z["id"] not in u_of or z.get("nevyhodnoceno") or not z.get("text"):
            continue
        u = u_of[z["id"]]
        met[(z["skill"], z["id"])] = {
            "skore": skore([z["text"]], model, an)[0], "delka": slov(z["text"]) / u["n"],
            "cisla": int(bool(_cisla(z["text"]))), "znacky": int(bool(_ZNACKA.search(z["text"]))),
            "cena": z.get("cena") or 0, "kroku": z.get("kroku"), "skill_nacten": int(bool(z.get("skill_nacten")))}

    def prumer(x):
        x = [v for v in x if v is not None]
        return sum(x) / len(x) if x else None

    def median(x):
        x = sorted(v for v in x if v is not None)
        return x[len(x) // 2] if x else None

    souhrn = {}
    for vrstva in ("vse", "rozhodovaci"):
        ids = [i for i in u_of if vrstva == "vse" or u_of[i]["vrstva"] not in DOMACI]
        souhrn[f"lidsky|{vrstva}"] = {"textu": len(ids), "skore": prumer([lidske_skore[i] for i in ids])}
        for s in SKILLY:
            mm = [met[(s, i)] for i in ids if (s, i) in met]
            souhrn[f"{s}|{vrstva}"] = {"textu": len(mm), **{k: (median if k in ("cena", "kroku") else prumer)(
                [m[k] for m in mm]) for k in ("skore", "delka", "cisla", "znacky", "cena", "kroku", "skill_nacten")}}
    shluky = {i: u["shluk"] for i, u in u_of.items()}
    srovnani = []
    for x, y in (("unslop-cs", "bez-skillu"), ("anti-ai-slop-cz", "bez-skillu"), ("unslop-cs", "anti-ai-slop-cz")):
        r = {"a": x, "b": y}
        for vrstva in ("vse", "rozhodovaci"):
            ids = [i for i in u_of if vrstva == "vse" or u_of[i]["vrstva"] not in DOMACI]
            for k in ("skore", "cisla"):
                r[f"{k}|{vrstva}"] = statistika.bootstrap_rozdil(
                    {i: met[(x, i)][k] for i in ids if (x, i) in met},
                    {i: met[(y, i)][k] for i in ids if (y, i) in met}, shluky, seed=cfg["seed"])
        srovnani.append(r)

    cil = os.path.join(KOREN, "vysledky", a.stitek)
    os.makedirs(cil, exist_ok=True)
    meta = {"stitek": a.stitek, "datum": datetime.datetime.now().astimezone().strftime("%Y-%m-%d %H:%M %z"),
            "temat": len(uu), "commit": git("rev-parse", "--short", "HEAD"),
            "otisky": {s.nazev: s.otisk() for s in skilly}, "model_skillu": cfg["behy"]["model_skillu"],
            "effort_skillu": cfg["behy"].get("effort_skillu"), "cena": rozpocet.cena,
            "prevzato": sum(bool(z.get("prevzato")) for z in zb.hotove.values()),
            "nevyhodnoceno": sum(bool(z.get("nevyhodnoceno")) for z in zb.hotove.values()),
            "bez_textu": sum(1 for z in zb.hotove.values() if not z.get("nevyhodnoceno") and not z.get("text"))}
    with open(os.path.join(cil, "souhrn.json"), "w", encoding="utf-8", newline="\n") as fh:
        json.dump({"meta": meta, "souhrn": souhrn, "srovnani": srovnani}, fh, ensure_ascii=False, indent=1)

    def f(v, n=3):
        return "–" if v is None else (f"{v:.{n}f}" if isinstance(v, float) else str(v))

    r = [f"# Režim psaní: {a.stitek}", "",
         f"- Datum: {meta['datum']}; dev sada, témat {len(uu)}; commit `{meta['commit']}`",
         f"- Model skillu: {meta['model_skillu']} (effort {meta['effort_skillu']}); otisky: "
         + ", ".join(f"{k} `{v}`" for k, v in meta["otisky"].items()),
         f"- Cena celkem: {meta['cena']:.2f} USD; nevyhodnoceno {meta['nevyhodnoceno']}, "
         f"bez textu mezi značkami {meta['bez_textu']}", "",
         "Skóre AI-ovosti: 0 = jako lidský text, 1 = jako AI (rysy F0, nezávislé na pravidlech skillů). "
         "Řádek „lidský originál“ je skóre lidského textu, ze kterého je téma. Do rozhodovacího pravidla "
         "nevstupuje.", ""]
    for vrstva in ("rozhodovaci", "vse"):
        r += [f"## Vrstva: {vrstva}", "", "| | textů | skóre AI | délka/zadání | s čísly | značky/markdown | "
              "skill načten | cena/text | kroků |", "|---|---|---|---|---|---|---|---|---|"]
        lid = souhrn[f"lidsky|{vrstva}"]
        r.append(f"| lidský originál | {lid['textu']} | {f(lid['skore'])} | | | | | | |")
        for s in SKILLY:
            x = souhrn[f"{s}|{vrstva}"]
            r.append(f"| {s} | {x['textu']} | {f(x['skore'])} | {f(x['delka'], 2)} | {f(x['cisla'], 2)} | "
                     f"{f(x['znacky'], 2)} | {f(x['skill_nacten'], 2)} | {f(x['cena'])} | {f(x['kroku'])} |")
        r.append("")
        for sc in srovnani:
            for k, popis in (("skore", "skóre AI"), ("cisla", "s čísly")):
                iv = sc.get(f"{k}|{vrstva}")
                if iv:
                    r.append(f"- {sc['a']} − {sc['b']}, {popis}: {iv[0]:+.3f} [{iv[1]:+.3f}, {iv[2]:+.3f}]")
        r.append("")
    md = "\n".join(r) + "\n"
    with open(os.path.join(cil, "vysledky.md"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(md)
    print(md)


if __name__ == "__main__":
    main()
