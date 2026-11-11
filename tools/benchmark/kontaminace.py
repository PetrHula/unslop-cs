#!/usr/bin/env python3
"""Filtr kontaminace AI protějšků (krok 2 PLAN.md).

AI text se vyřadí také, když model odmítl, přiznal neznalost tématu nebo nechal zástupné
značky typu [datum]; markdown se jen označí (patří k chatbotím výstupům).

AI text se vyřadí, když s lidským textem (u pokračování s celým lidským úsekem včetně
začátku, který model dostal) sdílí souvislý úsek aspoň `max_shoda_ngram` slov, nebo víc
než `max_podil_8gramu` svých slovních 8-gramů. Slova se porovnávají malými písmeny bez
interpunkce.

Výstup: DATA/ai/kontaminace.json {soubor: {nejdelsi_shoda, podil_8gramu, vyrazeno}}
a souhrn po vrstvách, metodách a modelech.

Použití:
    python3 -I tools/benchmark/kontaminace.py --konfigurace tools/benchmark/konfigurace.json
"""
import argparse
import collections
import json
import os
import re


def slova(t):
    return re.findall(r"\w+", t.lower())


def ngramy(w, n):
    return {tuple(w[i:i + n]) for i in range(len(w) - n + 1)}


def nejdelsi_shoda(a, b, strop=60):
    """Délka nejdelšího společného souvislého úseku slov (nejvýš strop)."""
    n, sb = 0, None
    for d in range(4, strop + 1):
        sb = ngramy(b, d)
        if any(tuple(a[i:i + d]) in sb for i in range(len(a) - d + 1)):
            n = d
        else:
            break
    return n


# Výstupy, které nejsou protějškem: odmítnutí, přiznání neznalosti, zástupné značky.
_ODMITNUTI = re.compile(r"(?i)\b(nenapíšu|nemohu napsat|nemám (ověřené|spolehlivé|dostatečné) informace|"
                        r"neznám (kapelu|album|dílo))")
_ZASTUPNE = re.compile(r"\[(datum|název|jméno|počet|číslo|doplnit|obec|okres)[^\]]{0,40}\]", re.I)
_MARKDOWN = re.compile(r"\*\*[^*\n]+\*\*|^\s*(#{1,6}\s|---\s*$|[-*]\s)|(?<!\w)\*[^*\n]+\*(?!\w)", re.M)


def posud(ai_text, lidsky, k):
    a, b = slova(ai_text), slova(lidsky)
    g8 = ngramy(a, 8)
    podil = len(g8 & ngramy(b, 8)) / len(g8) if g8 else 0.0
    shoda = nejdelsi_shoda(a, b)
    duvody = []
    if shoda >= k["max_shoda_ngram"] or podil > k["max_podil_8gramu"]:
        duvody.append("kontaminace")
    if _ODMITNUTI.search(ai_text):
        duvody.append("odmítnutí nebo neznalost")
    if _ZASTUPNE.search(ai_text):
        duvody.append("zástupné značky")
    return {"nejdelsi_shoda": shoda, "podil_8gramu": round(podil, 4), "vyrazeno": bool(duvody),
            "duvody": duvody, "markdown": bool(_MARKDOWN.search(ai_text))}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--konfigurace", required=True)
    a = ap.parse_args()
    cfg = json.load(open(a.konfigurace, encoding="utf-8"))
    data = os.path.expanduser(cfg["data"])
    vysledek, souhrn = {}, collections.defaultdict(lambda: [0, 0])
    for r in open(os.path.join(data, "ai", "zaznamy.jsonl"), encoding="utf-8"):
        z = json.loads(r)
        if z["metoda"] == "tema" or not z.get("soubor"):
            continue
        ai_text = open(os.path.join(data, z["soubor"]), encoding="utf-8").read()
        lidsky = open(os.path.join(data, "texty", z["id"] + ".txt"), encoding="utf-8").read()
        v = posud(ai_text, lidsky, cfg["kontaminace"])
        vysledek[z["soubor"]] = v
        for klic in (("vrstva", z["vrstva"]), ("metoda", z["metoda"]), ("model", z["model_pozadovany"])):
            souhrn[klic][0] += 1
            souhrn[klic][1] += v["vyrazeno"]
        for d in v["duvody"]:
            souhrn[("důvod", d)][1] += 1
        souhrn[("markdown", z["metoda"])][1] += v["markdown"]
    with open(os.path.join(data, "ai", "kontaminace.json"), "w", encoding="utf-8") as f:
        json.dump(vysledek, f, ensure_ascii=False, indent=1)
    print(f"posouzeno {len(vysledek)}, vyřazeno {sum(v['vyrazeno'] for v in vysledek.values())}")
    for (druh, hodnota), (n, vyr) in sorted(souhrn.items()):
        print(f"  {druh} {hodnota}: vyřazeno {vyr} z {n}")


if __name__ == "__main__":
    main()
