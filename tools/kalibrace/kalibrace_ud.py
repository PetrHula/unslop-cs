#!/usr/bin/env python3
"""Kalibrace metriky.py na lidských textech z Universal Dependencies.

Měří falešné poplachy: podíl lidských úseků, kde skript hlásí nález P0 nebo P1,
a které položky slova.md je spouštějí. Citlivost na AI text neměří.

Data (CC BY-NC-SA, do repozitáře nepatří) stáhněte z GitHubu UniversalDependencies:
  UD_Czech-CAC/cs_cac-ud-test.conllu, UD_Czech-FicTree/cs_fictree-ud-test.conllu

Režimy:
  --gold          zlatá anotace z CoNLL-U místo modelu UDPipe (lemmata, slovní druhy,
                  závislosti). Položky slova.md se lemmatizují slovníkem tvar → lemma
                  ze zadaných souborů (a z --slovnik), takže párování je přibližné.
  --udpipe CESTA  model UDPipe jako v běžném provozu.
  bez obojího     režim bez modelu.

Příklad:
  python3 tools/kalibrace/kalibrace_ud.py --gold --slovnik cs_cac-ud-dev.conllu \\
      cs_cac-ud-test.conllu cs_fictree-ud-test.conllu
"""
import argparse
import collections
import json
import os
import re
import sys

KOREN = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(KOREN, "skills", "unslop-cs", "scripts"))
import metriky  # noqa: E402


def nacti_conllu(cesta):
    """Vrátí seznam dokumentů; dokument = seznam vět; věta = (text, tokeny, mwt)."""
    docs, doc, text, toks, mwt = [], [], None, [], []
    with open(cesta, encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if line.startswith("# newdoc"):
                if doc:
                    docs.append(doc)
                doc = []
            elif line.startswith("# text = "):
                text = line[9:]
            elif not line:
                if toks:
                    doc.append((text, toks, mwt))
                text, toks, mwt = None, [], []
            elif not line.startswith("#"):
                c = line.split("\t")
                if "-" in c[0]:
                    a, b = map(int, c[0].split("-"))
                    mwt.append((a, b, c[1]))
                elif "." not in c[0]:
                    toks.append(c)
    if toks:
        doc.append((text, toks, mwt))
    if doc:
        docs.append(doc)
    return docs


def featy(s):
    out = {}
    if s != "_":
        for f in s.split("|"):
            if "=" in f:
                k, v = f.split("=", 1)
                out[k] = v
    return out


class GoldUD:
    """Náhrada za metriky.UDPipe: pro registrované úseky vrací zlatou anotaci."""

    def __init__(self, slovnik):
        self.slovnik = slovnik      # tvar → (lemma, upos, feats)
        self.useky = {}             # text úseku → seznam vět (text, tokeny, mwt)

    def registruj(self, text, vety):
        self.useky[text] = vety

    def _zarovnej(self, text, vety):
        vys, kurzor = [], 0
        for _, toks, mwt in vety:
            povrch = {}
            for a, b, form in mwt:
                for i in range(a, b + 1):
                    povrch[i] = form
            akt, mwt_rozsah = [], {}
            for c in toks:
                i = int(c[0])
                form = povrch.get(i, c[1])
                if i in povrch and form in mwt_rozsah:
                    s, e = mwt_rozsah[form]
                else:
                    s = text.find(form, kurzor)
                    if s < 0 or s - kurzor > 40:
                        continue
                    e = s + len(form)
                    kurzor = e
                    if i in povrch:
                        mwt_rozsah = {form: (s, e)}
                akt.append(metriky.Tok(c[1], c[2], c[3], featy(c[5]),
                                       int(c[6]) if c[6].isdigit() else 0, c[7], s, e,
                                       len(akt)))
            if akt:
                vys.append(akt)
        return vys

    def zpracuj(self, text, presegmented=False):
        if text in self.useky:
            return self._zarovnej(text, self.useky[text])
        # položky slova.md a neznámé úseky: pravidla + slovník tvar → lemma
        vety = []
        radky = text.split("\n") if presegmented else [text]
        pos = 0
        for r in radky:
            toks = metriky.tokeny_pravidla(text, pos, pos + len(r))
            for i, t in enumerate(toks):
                lem, upos, ft = self.slovnik.get(t.form.lower(), (t.form.lower(), "", {}))
                if not upos:
                    upos = "PUNCT" if not any(ch.isalnum() for ch in t.form) else "X"
                t.lemma, t.upos, t.feats, t.idx = lem, upos, dict(ft), i
            vety.append(toks)
            pos += len(r) + 1
        return vety


def slovnik_z(cesty):
    cet = collections.defaultdict(collections.Counter)
    for c in cesty:
        for doc in nacti_conllu(c):
            for _, toks, _ in doc:
                for t in toks:
                    cet[t[1].lower()][(t[2], t[3], t[5])] += 1
    return {k: (v.most_common(1)[0][0][0], v.most_common(1)[0][0][1],
                featy(v.most_common(1)[0][0][2])) for k, v in cet.items()}


def useky(docs, slov):
    """Souvislé úseky po aspoň `slov` slovech, nepřesahují hranice dokumentu."""
    for doc in docs:
        akt, n = [], 0
        for v in doc:
            akt.append(v)
            n += sum(1 for t in v[1] if t[3] != "PUNCT")
            if n >= slov:
                yield akt
                akt, n = [], 0
        if n >= slov * 0.6:
            yield akt


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("conllu", nargs="+")
    ap.add_argument("--gold", action="store_true")
    ap.add_argument("--udpipe")
    ap.add_argument("--slovnik", action="append", default=[],
                    help="další CoNLL-U jen pro slovník tvar → lemma (režim --gold)")
    ap.add_argument("--slova", default=metriky.vychozi_slova())
    ap.add_argument("--profil", default="blog")
    ap.add_argument("--slov", type=int, default=190)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)

    gold = GoldUD(slovnik_z(a.conllu + a.slovnik)) if a.gold else None
    model = metriky.nacti_udpipe(a.udpipe) if a.udpipe else None
    vysledky = {}
    for cesta in a.conllu:
        jm = os.path.basename(cesta).replace(".conllu", "")
        poc_useku, slov_celkem = 0, 0
        s_nalezem = collections.Counter()
        polozky = collections.Counter()
        p2 = collections.Counter()
        hodnoty = collections.defaultdict(list)
        for u in useky(nacti_conllu(cesta), a.slov):
            text = " ".join(v[0] for v in u)
            if gold:
                gold.registruj(text, u)
            an = metriky.Analyza(text, a.profil, gold or model, a.slova).spust()
            poc_useku += 1
            slov_celkem += an.doc.pocet_slov()
            kat = set()
            for n in an.nalezy:
                if n.zavaznost in ("P0", "P1"):
                    kat.add((n.zavaznost, n.metrika, n.kategorie))
                    if n.zdroj:
                        polozky[(n.zavaznost, n.zdroj)] += 1
                elif n.zavaznost == "P2":
                    p2[(n.metrika, n.kategorie)] += 1
            for k in kat:
                s_nalezem[k] += 1
            m = an.metriky
            for klic, cesta_m in (("ktery_na_1000", ("soudrznost", "ktery_na_1000_slov")),
                                  ("coz_na_100", ("soudrznost", "coz_na_100_vet")),
                                  ("cisla_na_1000", ("konkretnost", "cisla_na_1000_slov")),
                                  ("castice_mod_na_1000", ("postoj", "modalni_na_1000_slov"))):
                x = m.get(cesta_m[0], {}).get(cesta_m[1])
                if x is not None:
                    hodnoty[klic].append(x)
        vysledky[jm] = {
            "useku": poc_useku, "slov": slov_celkem,
            "p0p1_podil_useku": {f"{z} {me}/{ka}": round(c / poc_useku, 3)
                                 for (z, me, ka), c in s_nalezem.most_common()},
            "p0p1_polozky": {f"{z} {zd}": c for (z, zd), c in polozky.most_common()},
            "p2_vyskyty": {f"{me}/{ka}": c for (me, ka), c in p2.most_common(15)},
            "mediany": {k: sorted(v)[len(v) // 2] for k, v in hodnoty.items() if v},
        }
    if a.json:
        print(json.dumps(vysledky, ensure_ascii=False, indent=1))
        return
    for jm, r in vysledky.items():
        print(f"== {jm}: {r['useku']} úseků, {r['slov']} slov")
        print("  podíl úseků s nálezem P0/P1:")
        for k, v in r["p0p1_podil_useku"].items():
            print(f"    {v:6.1%}  {k}")
        if r["p0p1_polozky"]:
            print("  položky slova.md s P0/P1:")
            for k, v in r["p0p1_polozky"].items():
                print(f"    {v:3d}×  {k}")
        print("  nejčastější P2:", ", ".join(f"{k} {v}" for k, v in r["p2_vyskyty"].items()))
        if r["mediany"]:
            print("  mediány:", r["mediany"])


if __name__ == "__main__":
    main()
