#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Slovní diff po větách a kontrola tiché ztráty pro přepis českého textu.

    python3 diff.py pred.txt po.txt [--format md|json|oboje] [--metriky]
                    [--profil blog] [--udpipe cesta] [--prisne]

Jen standardní knihovna. Nezávisí na locale ani na gitu. Věty, maskování kódu a citací,
kmeny pro skloňovaná jména a seznamy slov bere z metriky.py ve stejné složce.

Výstup md: slovní diff (jen změněné věty, značky [-smazáno-] a {+přidáno+}), oddíl
Tichá ztráta a s --metriky řádek metrik před → po. Výstup json: zmeny, ztraty, metriky.
Návratový kód je 0; s --prisne 1, když ztraty nejsou prázdné.

Kontrola ztráty porovnává počty výskytů ve zdroji a v nové verzi: čísla (přesná shoda),
vlastní jména (shoda kmene, bez modelu jen přibližně), částice a jištění ze seznamů
metriky.py a markery síly tvrzení (příčina, míra, absolutnost; jen info). Co leží v kódu,
citacích „>“ a URL, se nepočítá.
"""
import argparse
import difflib
import json
import os
import re
import sys
from collections import Counter

TADY = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, TADY)
import metriky  # noqa: E402

SLOVO = re.compile(r"\w+(?:[.,]\d+)*|\S|\s+")
CISLO = re.compile(r"\d")
NAHRAZKA = {" ": " "}

# Markery síly tvrzení (příčina, míra, absolutnost). Jen info: ztráta tu může být záměrná.
SILA = {"způsobuje", "způsobil", "způsobují", "protože", "kvůli", "třikrát", "dvakrát",
        "čtyřikrát", "vždy", "nikdy", "nesmí", "musí", "každý", "žádný", "všichni", "výhradně",
        "pouze", "jedině"}
CASTICE_JISTENI = (set(metriky.CASTICE) | set(metriky.MODALNI) | set(metriky.OSLABUJICI))


def _maskuj(text, vse=False):
    masked, _ = metriky.maskuj(text, vse)
    return masked


def deleni_na_vety(text):
    """Věty z textu bez kódu a citací; masku nahradí prázdným místem, takže věty jsou čisté."""
    masked = _maskuj(text)
    vety = []
    for a, b in metriky.deleni_vet_pravidla(masked, 0, len(masked)):
        v = re.sub(r"[ \t\r\n]+", " ", masked[a:b]).strip()
        if v:
            vety.append(v)
    return vety


def _spoj(tokeny):
    return "".join(tokeny)


def _zmeny(x, y):
    """Opkódy difflib; mezera mezi dvěma změnami patří ke změně, sousední změny se slučují."""
    ops = difflib.SequenceMatcher(None, x, y, autojunk=False).get_opcodes()
    for n, (o, k1, k2, l1, l2) in enumerate(ops):
        if 0 < n < len(ops) - 1 and o == "equal" and _spoj(x[k1:k2]).isspace():
            ops[n] = ("replace", k1, k2, l1, l2)
    sloucene = []
    for o, k1, k2, l1, l2 in ops:
        if sloucene and o != "equal" and sloucene[-1][0] != "equal":
            sloucene[-1] = ("replace", sloucene[-1][1], k2, sloucene[-1][3], l2)
        else:
            sloucene.append((o, k1, k2, l1, l2))
    return sloucene


def slovni_diff(pred, po):
    """Vrátí seznam změn: {veta_pred, veta_po, diff, useky:[{pred, po}]}."""
    a, b = deleni_na_vety(pred), deleni_na_vety(po)
    vysledek = []
    for o, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if o == "equal":
            continue
        if i2 - i1 == j2 - j1:  # stejný počet vět: změnu přiřaď každé větě zvlášť
            dvojice = [(a[i1 + k], b[j1 + k]) for k in range(i2 - i1)]
        else:
            dvojice = [("\n".join(a[i1:i2]), "\n".join(b[j1:j2]))]
        for vp, vn in dvojice:
            vysledek.append(_diff_vety(vp, vn))
    return vysledek


def _diff_vety(vp, vn):
    x, y = SLOVO.findall(vp), SLOVO.findall(vn)
    radek, useky = [], []
    for o2, k1, k2, l1, l2 in _zmeny(x, y):
        if o2 == "equal":
            radek.append(_spoj(x[k1:k2]))
            continue
        smaz, pridej = _spoj(x[k1:k2]), _spoj(y[l1:l2])
        if smaz:
            radek.append("[-" + smaz + "-]")
        if pridej:
            radek.append("{+" + pridej + "+}")
        useky.append({"pred": smaz, "po": pridej})
    return {"veta_pred": vp, "veta_po": vn, "diff": "".join(radek), "useky": useky}


def _tokeny(text):
    """Slova a čísla z textu bez kódu a citací; vrací (token, je_na_zacatku_vety)."""
    masked = _maskuj(text)
    out = []
    for a, b in metriky.deleni_vet_pravidla(masked, 0, len(masked)):
        prvni = True
        for m in re.finditer(r"\w+(?:[.,]\d+)*", masked[a:b]):
            out.append((m.group(0), prvni))
            prvni = False
    return out


def _je_jmeno(tok, zacatek):
    return (not zacatek and tok[:1].isupper() and not tok.isupper()
            and not CISLO.search(tok) and len(tok) > 1)


def _shoda_jmena(a, b):
    """Shoda kmene z metriky.py, rozšířená o střídání koncovky (Praha/Praze, Brno/Brně):
    společný začátek aspoň ze tří znaků a rozdíl nejvýš dva znaky na konci."""
    if metriky.shoda_kmenu(a, b):
        return True
    cp = 0
    for x, y in zip(a, b):
        if x != y:
            break
        cp += 1
    n = min(len(a), len(b))
    return cp >= 3 and cp >= n - 2 and abs(len(a) - len(b)) <= 2


def _chybi_podle_kmene(zdroj, nova):
    """Jména ze zdroje, ke kterým v nové verzi nezbývá jméno se shodným kmenem."""
    volna = [metriky.kmen(t) for t in nova]
    chybi = []
    for t in zdroj:
        k = metriky.kmen(t)
        for i, n in enumerate(volna):
            if _shoda_jmena(k, n):
                del volna[i]
                break
        else:
            chybi.append(t)
    return chybi


def _ubylo(zdroj, nova, filtr):
    a = Counter(t for t in zdroj if filtr(t))
    b = Counter(t for t in nova if filtr(t))
    return sorted((a - b).elements())


def ztraty(pred, po, model=False):
    tp, tn = _tokeny(pred), _tokeny(po)
    slova_p, slova_n = [t.lower() for t, _ in tp], [t.lower() for t, _ in tn]
    jmena_p = [t for t, z in tp if _je_jmeno(t, z)]
    jmena_n = [t for t, z in tn if _je_jmeno(t, z)]
    return {
        "cisla": _ubylo([t for t, _ in tp], [t for t, _ in tn], CISLO.search),
        "jmena": _chybi_podle_kmene(jmena_p, jmena_n),
        "castice": _ubylo(slova_p, slova_n, lambda t: t in CASTICE_JISTENI),
        "zesilovace_sily": _ubylo(slova_p, slova_n, lambda t: t in SILA),
        "priblizne_jmena": not model,
    }


def _prazdne(z):
    return not any(z[k] for k in ("cisla", "jmena", "castice"))


def _radek_metrik(mp, mn):
    def hodnota(m, oddil, klic):
        return m["metriky"][oddil][klic]
    polozky = [("částice", "postoj", "modalni_na_1000_slov"),
               ("jištění", "postoj", "oslabujici_na_1000_slov"),
               ("otázky", "postoj", "otazniky_na_100_vet"),
               ("čísla", "konkretnost", "cisla_na_1000_slov"),
               ("jména", "konkretnost", "vlastni_jmena_na_1000_slov")]

    def fmt(x):
        return ("%g" % x).replace(".", ",")
    return "Metriky před → po: " + " · ".join(
        "%s %s → %s" % (n, fmt(hodnota(mp, o, k)), fmt(hodnota(mn, o, k)))
        for n, o, k in polozky)


def metriky_pred_po(pred, po, profil, udpipe):
    mp = metriky.analyzuj(pred, profil, udpipe)
    mn = metriky.analyzuj(po, profil, udpipe)
    return {"pred": {o: mp["metriky"][o] for o in ("postoj", "konkretnost")},
            "po": {o: mn["metriky"][o] for o in ("postoj", "konkretnost")},
            "radek": _radek_metrik(mp, mn)}


def md(zmeny, z, met):
    out = []
    if zmeny:
        out += ["```text"]
        out += ["[%d] %s" % (i, s["diff"]) for i, s in enumerate(zmeny, 1)]
        out += ["```"]
    else:
        out += ["Beze změny."]
    out += ["", "**Tichá ztráta**", ""]
    if _prazdne(z):
        out += ["Nic nechybí: čísla, jména, částice ani jištění."]
    else:
        for klic, popis in (("cisla", "čísla"), ("jmena", "jména"),
                            ("castice", "částice a jištění")):
            if z[klic]:
                out += ["- %s: %s" % (popis, ", ".join(z[klic]))]
        if z["jmena"] and z["priblizne_jmena"]:
            out += ["- jména jsou bez modelu přibližná, ověř v diffu"]
    if z["zesilovace_sily"]:
        out += ["- info, síla tvrzení: ubylo %s (ověř, že změna není oslabení)"
                % ", ".join(z["zesilovace_sily"])]
    if met:
        out += ["", met["radek"]]
    return "\n".join(out) + "\n"


def main(argv=None):
    metriky.utf8_stdio()
    ap = argparse.ArgumentParser(description="Slovní diff po větách a tichá ztráta.")
    ap.add_argument("pred", help="zdrojový text")
    ap.add_argument("po", help="nová verze")
    ap.add_argument("--format", choices=["md", "json", "oboje"], default="md")
    ap.add_argument("--metriky", action="store_true", help="přidá metriky před → po")
    ap.add_argument("--profil", default="blog")
    ap.add_argument("--udpipe", default=os.environ.get("UNSLOP_UDPIPE"))
    ap.add_argument("--prisne", action="store_true", help="návratový kód 1 při ztrátě")
    a = ap.parse_args(argv)
    pred = open(a.pred, encoding="utf-8").read()
    po = open(a.po, encoding="utf-8").read()
    zmeny = slovni_diff(pred, po)
    z = ztraty(pred, po, bool(a.udpipe))
    met = metriky_pred_po(pred, po, a.profil, a.udpipe) if a.metriky else None
    if a.format in ("md", "oboje"):
        sys.stdout.write(md(zmeny, z, met))
    if a.format in ("json", "oboje"):
        print(json.dumps({"zmeny": zmeny, "ztraty": z, "metriky": met},
                         ensure_ascii=False, indent=2))
    return 1 if a.prisne and not _prazdne(z) else 0


if __name__ == "__main__":
    sys.exit(main())
