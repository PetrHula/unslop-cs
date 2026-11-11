#!/usr/bin/env python3
"""Sestaví lidský korpus benchmarku z dat v DATA/surove/ (krok 1 PLAN.md).

Čistí texty, dělí je na úseky 200–600 slov, vybírá úseky po vrstvách se seedem a zapíše:
  DATA/texty/<id>.txt          normalizovaný text úseku (odstavce oddělené prázdným řádkem)
  DATA/manifest.json           záznam na text (zdroj, URL, licence, sha256, žánr, období…)
  tools/benchmark/manifest_hashe.json   jen id, vrstva, dílo, sha256, slov (do repozitáře)

Dokument o 200–600 slovech se bere celý. Jinak úsek začíná na začátku odstavce a končí
na konci odstavce, jakmile má aspoň 350 slov (nebo dřív, když by další odstavec přetekl
600 a úsek už má 200); v dlouhém odstavci (a v CAC, které odstavce nemá) na konci věty
od 400 slov; nikdy nepřekročí 600. Další úsek téhož dokumentu začíná dalším odstavcem.

Použití:
    python3 -I tools/benchmark/korpus.py ~/unslop-cs-data/benchmark [--seed 20261111]
"""
import argparse
import collections
import hashlib
import html
import json
import os
import random
import re
import unicodedata

KOREN = os.path.dirname(os.path.abspath(__file__))
MIN, CIL, MEKKY, MAX = 200, 350, 400, 600

KVOTY = {"klasika": 60, "cac": 30, "fictree": 20, "wiki": 30, "uredni": 20}
KVOTY_KLASIKA = {"Karel Čapek": 20, "Jaroslav Hašek": 15, "Arne Novák": 10, "Karel Poláček": 6,
                 "Jan Neruda": 4, None: 5}
KVOTY_CAC = {"n": 12, "s": 12, "a": 6}
ZANR_CAC = {"n": "novinový", "s": "odborný", "a": "administrativní"}
ZANR_SBIRKY = {"Kritika slov": "sloupek", "Kalendář": "fejeton", "Měl jsem psa a kočku": "fejeton",
               "Jak se co dělá": "fejeton", "Hovory okamžiků": "fejeton",
               "Povídky pana Kočkodana": "povídka"}
ZANR_AUTORA = {"Jaroslav Hašek": "humoreska", "Karel Čapek": "publicistika", "Jan Neruda": "fejeton",
               "Arne Novák": "fejeton", None: "fejeton"}
# stránky, které nejsou souvislá próza
VYNECHAT = {"Žurnalistický slovník": "slovníková hesla"}
LIMIT_DILA = 0.2  # nejvýš 20 % vrstvy z jednoho díla

UD_COMMIT = {"ud_cac": ("UD_Czech-CAC", "c8806b26bdc5993c151bfae0bc2643904dba65b1", "CC BY-SA 4.0"),
             "ud_fictree": ("UD_Czech-FicTree", "121f0e321fd38d9304fbef39d90345cb8c81e43f",
                            "CC BY-NC-SA (LICENSE.txt 4.0, README 3.0)")}


# ---------------------------------------------------------------------------
# Normalizace a úseky

def norm(s):
    """NFC a sjednocené bílé znaky; nezlomitelná mezera (typografie) zůstává."""
    return re.sub(r"[ \t\r\n\f\v]+", " ", unicodedata.normalize("NFC", s)).strip(" ")


def slov(s):
    return sum(1 for t in s.split() if re.search(r"\w", t))


_VETA = re.compile(r"(?<=[.!?…])[\"“”»]?\s+(?=[„\"«(]?[A-ZÁČĎÉĚÍŇÓŘŠŤÚŮÝŽ0-9])")
_ZKRATKA = re.compile(r"(\b\w{1,3}|\b[A-ZÁČĎÉĚÍŇÓŘŠŤÚŮÝŽ]|tzv|např|atd|resp|mil|tis|mld|str|č)\.$", re.I)


def vety(odstavec):
    """Hrubé dělení na věty; spojí kusy po zkratkách a iniciálách."""
    kusy, out = _VETA.split(odstavec), []
    for k in kusy:
        if out and _ZKRATKA.search(out[-1]) and not re.search(r"[!?…]$", out[-1]):
            out[-1] += " " + k
        else:
            out.append(k)
    return [k for k in out if k.strip()]


def useky(odstavce):
    """odstavce: seznam seznamů vět. Vrátí seznam úseků; úsek = seznam odstavců (text)."""
    odstavce = [o for o in odstavce if o]
    if MIN <= sum(slov(v) for o in odstavce for v in o) <= MAX:
        return [[" ".join(o) for o in odstavce]]  # krátký dokument celý
    vysledek, i = [], 0
    while i < len(odstavce):
        usek, pocet, j = [], 0, i
        while j < len(odstavce):
            vety_j = odstavce[j]
            w_odst = sum(slov(v) for v in vety_j)
            if pocet + w_odst <= MAX:  # celý odstavec se vejde
                usek.append(" ".join(vety_j))
                pocet += w_odst
                j += 1
                if pocet >= CIL:
                    break
                continue
            if pocet >= MIN:
                break  # radši konec na předchozím odstavci než uprostřed dalšího
            j += 1
            cast = []  # dlouhý odstavec: konec na větě od MEKKY slov, nejvýš MAX
            for v in vety_j:
                w = slov(v)
                if pocet + w > MAX or pocet >= MEKKY:
                    break
                cast.append(v)
                pocet += w
            if cast:
                usek.append(" ".join(cast))
            break
        if pocet >= MIN:
            vysledek.append(usek)
        i = max(j, i + 1)
    return vysledek


# ---------------------------------------------------------------------------
# Wikitext (Wikizdroje)

PONECHAT_OBSAH = {"prostrkaně", "proložit", "verzálky", "kapitálky", "uprostřed", "podpis"}


def wikitext_na_odstavce(w):
    w = re.sub(r"(?s)<!--.*?-->", "", w)
    w = re.sub(r"(?is)<ref[^>/]*/>|<ref[^>]*>.*?</ref>", "", w)
    w = re.sub(r"(?is)<(poem|math)[^>]*>.*?</\1>", "\n\n", w)
    w = re.sub(r"(?s)\{\|.*?\|\}", "\n\n", w)
    while True:  # nejvnitřnější šablony
        m = re.search(r"\{\{([^{}]*)\}\}", w)
        if not m:
            break
        casti = m.group(1).split("|")
        jmeno = casti[0].strip().lower()
        if jmeno in PONECHAT_OBSAH and len(casti) > 1:
            nahrada = next((c for c in casti[1:] if "=" not in c), "")
        elif jmeno == "oddělovač":
            nahrada = "\n\n"
        else:
            nahrada = ""
        w = w[:m.start()] + nahrada + w[m.end():]
    w = re.sub(r"\[\[(Soubor|File|Kategorie|Category|Obrázek):[^\]]*\]\]", "", w, flags=re.I)
    w = re.sub(r"\[\[[^\]|]*\|([^\]]*)\]\]", r"\1", w)
    w = re.sub(r"\[\[([^\]]*)\]\]", r"\1", w)
    w = re.sub(r"\[https?://\S+ ([^\]]*)\]", r"\1", w)
    w = re.sub(r"'{2,}", "", w)
    w = re.sub(r"(?i)<br\s*/?>", " ", w)
    w = html.unescape(re.sub(r"<[^>]+>", "", w))
    radky = []
    for r in w.split("\n"):
        if re.match(r"\s*(=+.*=+|[*#;]|__\w+__)\s*$", r) or re.match(r"\s*[*#;]", r):
            radky.append("")  # nadpisy a seznamy nejsou próza
        else:
            radky.append(r.lstrip(":"))
    odst = [norm(" ".join(b.split("\n"))) for b in "\n".join(radky).split("\n\n")]
    return [o for o in odst if re.search(r"[a-záčďéěíňóřšťúůýž]", o)]


def textinfo(w, pole):
    m = re.search(r"\|\s*" + pole + r"\s*=([^\n]*)", w)
    return m.group(1).strip() if m else ""


# ---------------------------------------------------------------------------
# Načtení zdrojů

def stazeni(data):
    p = os.path.join(data, "stazeni.json")
    return {z["soubor"]: z for z in json.load(open(p, encoding="utf-8"))}


def klasika(data, st, vyber):
    autor_umrti = {g["autor"]: g["umrti"] for g in vyber["skupiny"]}
    sbirky = [s for g in vyber["skupiny"] for s in g["sbirky"]]
    d = os.path.join(data, "surove", "wikizdroje", "stranky")
    dokumenty = []
    for f in sorted(os.listdir(d)):
        p = json.load(open(os.path.join(d, f), encoding="utf-8"))
        titul, w = p["titul"], p["wikitext"]
        if titul in VYNECHAT:
            continue
        sbirka = next((s for s in sbirky if titul == s or titul.startswith(s + "/")), None)
        autor = p["autor_vyber"]
        rok = re.findall(r"\b(1[89]\d\d)\b", textinfo(w, "ZDROJ"))
        z = st.get(f"surove/wikizdroje/stranky/{f}", {})
        odst = [vety(o) for o in wikitext_na_odstavce(w)]
        dokumenty.append({
            "vrstva": "klasika", "klic": f"wikizdroje:{titul}", "dilo": sbirka or titul, "skupina": autor,
            "titul": titul, "autor": autor or re.sub(r"\[\[Autor:|\]\].*|\|.*", "", textinfo(w, "AUTOR")),
            "zdroj": "Wikizdroje", "url": z.get("url"), "licence": "public domain (PD old/anon 70); "
            "přepis Wikizdroje CC BY-SA 4.0", "licence_overeni": z.get("licence_overeni"),
            "datum_stazeni": z.get("datum_stazeni"),
            "zanr": ZANR_SBIRKY.get(sbirka) or ZANR_AUTORA.get(autor, "fejeton"),
            "obdobi": f"vydání {rok[-1]}" if rok else (f"do {autor_umrti.get(autor)}" if autor_umrti.get(autor)
                                                       else None),
            "odstavce": odst})
    return dokumenty


def conllu_dokumenty(cesta, odstavce_z_newpar):
    """Vrátí OrderedDict id -> seznam (id_odstavce, [věty])."""
    docs, doc, par = collections.OrderedDict(), None, None
    for line in open(cesta, encoding="utf-8"):
        line = line.rstrip("\n")
        if line.startswith("# newdoc"):
            doc = re.search(r"id\s*=\s*(\S+)", line).group(1)
            docs[doc] = []
            par = None
        elif line.startswith("# newpar") and odstavce_z_newpar:
            par = re.search(r"id\s*=\s*(\S+)", line).group(1)
            docs[doc].append((par, []))
        elif line.startswith("# text ="):
            if not docs[doc]:
                docs[doc].append((par, []))
            docs[doc][-1][1].append(norm(line[len("# text ="):]))
    return docs


def cac(data, st):
    soubor = "surove/ud_cac/cs_cac-ud-train.conllu"
    z = st[soubor]
    repo, commit, lic = UD_COMMIT["ud_cac"]
    out = []
    for doc, pars in conllu_dokumenty(os.path.join(data, soubor), False).items():
        out.append({"vrstva": "cac", "klic": f"cac:{doc}", "dilo": doc, "skupina": doc[0], "titul": doc,
                    "autor": None, "zdroj": f"{repo} (train)", "url": f"{z['url']}#{doc}", "licence": lic,
                    "licence_overeni": z["licence_overeni"], "datum_stazeni": z["datum_stazeni"],
                    "zanr": ZANR_CAC.get(doc[0], "?"), "obdobi": "1970–1989",
                    "odstavce": [p[1] for p in pars]})
    return out


def fictree(data, st):
    """Běhy po sobě jdoucích kousků (newpar id roste o 1) jsou souvislý text."""
    soubor = "surove/ud_fictree/cs_fictree-ud-train.conllu"
    z = st[soubor]
    repo, commit, lic = UD_COMMIT["ud_fictree"]
    out = []
    for doc, pars in conllu_dokumenty(os.path.join(data, soubor), True).items():
        beh, predchozi = [], None
        behy = []
        for pid, vv in pars:
            n = int(re.search(r"(\d+)$", pid).group(1))
            if predchozi is not None and n != predchozi + 1:
                behy.append(beh)
                beh = []
            beh.append((pid, vv))
            predchozi = n
        behy.append(beh)
        for b in behy:
            out.append({"vrstva": "fictree", "klic": f"fictree:{b[0][0]}", "dilo": doc, "skupina": doc,
                        "titul": f"{doc} {b[0][0]}–{b[-1][0]}", "autor": None,
                        "zdroj": f"{repo} (train)", "url": f"{z['url']}#{b[0][0]}", "licence": lic,
                        "licence_overeni": z["licence_overeni"], "datum_stazeni": z["datum_stazeni"],
                        "zanr": "beletrie", "obdobi": "1969–2007 (README)",
                        "poznamka": "hranice odstavců = kousky FicTree po ≤ 100 slovech, ne původní "
                                    "odstavce; 20 % děl FicTree jsou překlady z němčiny a slovenštiny",
                        "odstavce": [vv for _, vv in b]})
    return out


def wiki(data, st):
    d = os.path.join(data, "surove", "wikipedie", "clanky")
    out = []
    for f in sorted(os.listdir(d)):
        p = json.load(open(os.path.join(d, f), encoding="utf-8"))
        z = st[f"surove/wikipedie/clanky/{f}"]
        odst = []
        for o in p["odstavce"]:
            o = re.sub(r"\[[^\[\]]{1,25}\?\]|\[pozn\.[^\]]*\]", "", o)
            if "{{" in o or "}}" in o:
                continue
            pismen = sum(c.isalpha() for c in o)
            if pismen < 0.6 * max(1, len(o.replace(" ", ""))):
                continue  # kód, vzorce
            odst.append(vety(norm(o)))
        out.append({"vrstva": "wiki", "klic": f"wiki:{p['titul']}", "dilo": p["titul"], "skupina": p["kategorie"],
                    "titul": p["titul"], "autor": "autoři Wikipedie (historie revize)", "zdroj": "Wikipedie",
                    "url": z["url"], "licence": z["licence"], "licence_overeni": z["licence_overeni"],
                    "datum_stazeni": z["datum_stazeni"], "zanr": "encyklopedický",
                    "obdobi": f"revize {p['cas'][:10]}", "odstavce": odst})
    return out


def uredni(data, st):
    d = os.path.join(data, "surove", "csu", "zpravy")
    out = []
    for f in sorted(os.listdir(d)):
        p = json.load(open(os.path.join(d, f), encoding="utf-8"))
        z = st[f"surove/csu/zpravy/{f}"]
        rok = re.search(r"_(\d{4})\d{4}$", f[:-5])
        odst = list(p["odstavce"])
        while odst and odst[-1].rstrip().endswith(":"):
            odst.pop()  # „Více informací najdete…:“ bez odkazů, které csu.py vyřadil
        out.append({"vrstva": "uredni", "klic": f"csu:{f[:-5]}", "dilo": f[:-5], "skupina": None,
                    "titul": p["titul"], "autor": "Český statistický úřad", "zdroj": "ČSÚ, tiskové zprávy",
                    "url": p["url"], "licence": z["licence"], "licence_overeni": z["licence_overeni"],
                    "datum_stazeni": z["datum_stazeni"], "zanr": "tisková zpráva",
                    "obdobi": rok.group(1) if rok else None,
                    "odstavce": [vety(norm(o)) for o in odst]})
    return out


# ---------------------------------------------------------------------------
# Výběr

def vyber(dokumenty, kvota, kvoty_skupin, rnd):
    """Round-robin přes dokumenty v náhodném pořadí: nejdřív první úsek každého
    dokumentu, pak druhý atd.; drží kvóty skupin a limit úseků z jednoho díla."""
    limit_dila = max(1, int(kvota * LIMIT_DILA))
    kandidati = []
    for d in dokumenty:
        for i, u in enumerate(useky(d["odstavce"])):
            kandidati.append((i, rnd.random(), d, u))
    kandidati.sort(key=lambda x: (x[0], x[1]))
    vybrane, na_dilo, na_skupinu = [], collections.Counter(), collections.Counter()
    for i, _, d, u in kandidati:
        if len(vybrane) >= kvota:
            break
        sk = d["skupina"]
        if kvoty_skupin is not None and na_skupinu[sk] >= kvoty_skupin.get(sk, 0):
            continue
        if na_dilo[d["dilo"]] >= limit_dila:
            continue
        vybrane.append((d, i, u))
        na_dilo[d["dilo"]] += 1
        na_skupinu[sk] += 1
    return vybrane


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("data", help="~/unslop-cs-data/benchmark")
    ap.add_argument("--seed", type=int, default=20261111)
    a = ap.parse_args()

    st = stazeni(a.data)
    vyber_wz = json.load(open(os.path.join(KOREN, "zdroje", "wikizdroje_vyber.json"), encoding="utf-8"))
    vrstvy = {"klasika": (klasika(a.data, st, vyber_wz), KVOTY_KLASIKA),
              "cac": (cac(a.data, st), KVOTY_CAC),
              "fictree": (fictree(a.data, st), None),
              "wiki": (wiki(a.data, st), None),
              "uredni": (uredni(a.data, st), None)}

    texty_dir = os.path.join(a.data, "texty")
    os.makedirs(texty_dir, exist_ok=True)
    for f in os.listdir(texty_dir):  # sestavuje se vždy celé znovu
        if f.endswith(".txt"):
            os.remove(os.path.join(texty_dir, f))
    manifest, hashe = [], []
    for vrstva, (dokumenty, kvoty) in vrstvy.items():
        rnd = random.Random(f"{a.seed}:{vrstva}")
        vybrane = vyber(dokumenty, KVOTY[vrstva], kvoty, rnd)
        if len(vybrane) < KVOTY[vrstva]:
            print(f"POZOR {vrstva}: jen {len(vybrane)} z {KVOTY[vrstva]}")
        for d, i, u in vybrane:
            text = "\n\n".join(u) + "\n"
            klic = "{}#{}".format(d["klic"], i)
            id_ = "{}-{}".format(vrstva, hashlib.sha1(klic.encode()).hexdigest()[:8])
            with open(os.path.join(texty_dir, id_ + ".txt"), "w", encoding="utf-8", newline="\n") as f:
                f.write(text)
            sha = hashlib.sha256(text.encode("utf-8")).hexdigest()
            zaznam = {k: v for k, v in d.items() if k not in ("odstavce", "klic", "skupina")}
            zaznam.update(id=id_, vrstva=vrstva, usek=i, slov=slov(text), sha256=sha, soukromy=False,
                          zdroj_klic=d["klic"])
            manifest.append(zaznam)
            hashe.append({"id": id_, "vrstva": vrstva, "dilo": hashlib.sha1(d["dilo"].encode()).hexdigest()[:10],
                          "sha256": sha, "slov": zaznam["slov"]})
    manifest.sort(key=lambda z: z["id"])
    hashe.sort(key=lambda z: z["id"])
    meta = {"seed": a.seed, "min_slov": MIN, "max_slov": MAX, "kvoty": KVOTY, "pocet": len(manifest)}
    with open(os.path.join(a.data, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump({"meta": meta, "texty": manifest}, f, ensure_ascii=False, indent=1)
    with open(os.path.join(KOREN, "manifest_hashe.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump({"meta": meta, "texty": hashe}, f, ensure_ascii=False, indent=1)
    po_vrstvach = collections.Counter(z["vrstva"] for z in manifest)
    print(f"{len(manifest)} textů: " + ", ".join(f"{k} {n}" for k, n in po_vrstvach.items()))


if __name__ == "__main__":
    main()
