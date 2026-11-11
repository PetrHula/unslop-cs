#!/usr/bin/env python3
"""Stáhne prózu tiskových zpráv ČSÚ z ročních archivů (vrstva uredni, krok 1 PLAN.md).

Archiv: https://csu.gov.cz/tiskove_zpravy_a_informace-opendocument--RRRR (staticky 2003–2014).
Zprávy se losují se seedem ze zadaných let; ze stránky zprávy se vezme jen blok
div.odsazeni (datum, perex, odstavce), rozdělený na odstavce podle <br><br> a <p>.
Celé HTML ani přílohy se neukládají.

Licence: podle „Podmínek pro využívání a další zveřejňování statistických údajů ČSÚ“
jsou statistické informace na csu.gov.cz pod CC BY 4.0; upravené údaje se musí označit
jako upravené. Zda licence kryje i text zpráv, stránka výslovně neříká.

Použití:
    python3 -I csu.py ~/unslop-cs-data/benchmark/surove/csu \\
        --stazeni ~/unslop-cs-data/benchmark/stazeni.json --roky 2010-2014 --pocet 20 --seed 20261111
Opakování stejného výběru: --urls OUTDIR/vyber.json
"""
import argparse
import datetime
import hashlib
import html
import json
import os
import random
import re
import time
import urllib.error
import urllib.request

ARCHIV = "https://csu.gov.cz/tiskove_zpravy_a_informace-opendocument--{rok}"
UA = {"User-Agent": "unslop-benchmark/0.1 (research; low request rate)"}
LICENCE = "CC BY 4.0 (Podmínky ČSÚ); upraveno"
LICENCE_URL = "https://csu.gov.cz/podminky_pro_vyuzivani_a_dalsi_zverejnovani_statistickych_udaju_csu"
PAUZA = 2.0


def stahni(url):
    for pokus in range(5):
        time.sleep(PAUZA * (pokus + 1) ** 2)
        try:
            r = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=90)
            return r.read().decode("utf-8", errors="replace")
        except urllib.error.HTTPError as e:
            if e.code not in (429, 500, 502, 503):
                raise
        except (TimeoutError, urllib.error.URLError, OSError):
            pass
    raise SystemExit(f"opakovaně selhalo: {url}")


def zpravy_roku(rok):
    h = stahni(ARCHIV.format(rok=rok))
    return sorted({u for u in re.findall(r'href="(https://csu\.gov\.cz/[a-z0-9_]+_(\d{8}))/?"', h)
                   for u in [u[0]] if u.rsplit("_", 1)[1].startswith(str(rok))})


def _blok(h):
    """Vnitřek prvního div.odsazeni (s vnořenými div)."""
    m = re.search(r'<div class="odsazeni">', h)
    if not m:
        return None
    i, hloubka = m.end(), 1
    for t in re.finditer(r"<(/?)div\b[^>]*>", h[i:]):
        hloubka += -1 if t.group(1) else 1
        if hloubka == 0:
            return h[i:i + t.start()]
    return h[i:]


def proza(h):
    b = _blok(h)
    if b is None:
        return None, None
    b = re.sub(r"(?is)<(script|style|table)\b.*?</\1>", " ", b)
    b = re.sub(r"(?i)</?(p|div|h[1-6]|li|ul|ol)\b[^>]*>", "\n\n", b)
    b = re.sub(r"(?i)<br\s*/?>", "\n\n", b)  # i jedno <br> odděluje mezititulek od textu
    b = html.unescape(re.sub(r"<[^>]+>", "", b))
    odst = [re.sub(r"\s+", " ", x).strip() for x in b.split("\n\n")]
    odst = [x for x in odst if x]
    # kontakty (jména, telefony, e-maily úředníků) a odkazy se neukládají
    for i, x in enumerate(odst):
        if re.match(r"(?i)kontakt|tel\.|e-mail", x):
            odst = odst[:i]
            break
    odst = [x for x in odst if not re.search(r"www\.|https?://|@", x)]
    datum = odst.pop(0) if odst and re.fullmatch(r"\d{1,2}\. ?\d{1,2}\. ?\d{4}", odst[0]) else None
    return datum, odst


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("outdir")
    ap.add_argument("--stazeni", required=True)
    ap.add_argument("--roky", default="2010-2014")
    ap.add_argument("--pocet", type=int, default=20)
    ap.add_argument("--seed", type=int, default=20261111)
    ap.add_argument("--min-slov", type=int, default=200)
    ap.add_argument("--urls", help="vyber.json z dřívějšího běhu")
    a = ap.parse_args()
    os.makedirs(os.path.join(a.outdir, "zpravy"), exist_ok=True)

    if a.urls:
        kandidati, cil = json.load(open(a.urls, encoding="utf-8")), None
    else:
        od, do = map(int, a.roky.split("-"))
        kandidati = []
        for rok in range(od, do + 1):
            z = zpravy_roku(rok)
            print(f"{rok}: {len(z)} zpráv")
            kandidati += z
        random.Random(a.seed).shuffle(kandidati)
        cil = a.pocet

    datum_st = datetime.date.today().isoformat()
    zaznamy, vybrano = [], []
    for url in kandidati:
        if cil is not None and len(vybrano) >= cil:
            break
        h = stahni(url)
        titul = re.search(r"<h1[^>]*>(.*?)</h1>", h, re.S)
        datum, odst = proza(h)
        if not odst or sum(len(x.split()) for x in odst) < a.min_slov:
            print("málo prózy:", url)
            continue
        slug = url.rsplit("/", 1)[1]
        obsah = json.dumps({"url": url, "titul": html.unescape(re.sub(r"<[^>]+>", "", titul.group(1))).strip()
                            if titul else None, "datum": datum, "odstavce": odst},
                           ensure_ascii=False, indent=1).encode("utf-8")
        with open(os.path.join(a.outdir, "zpravy", slug + ".json"), "wb") as f:
            f.write(obsah)
        vybrano.append(url)
        zaznamy.append({"zdroj": "ČSÚ", "titul": slug, "soubor": f"surove/csu/zpravy/{slug}.json", "url": url,
                        "licence": LICENCE, "licence_overeni": LICENCE_URL, "datum_stazeni": datum_st,
                        "bajtu": len(obsah), "sha256": hashlib.sha256(obsah).hexdigest()})
    with open(os.path.join(a.outdir, "vyber.json"), "w", encoding="utf-8") as f:
        json.dump(vybrano, f, ensure_ascii=False, indent=1)
    stare = json.load(open(a.stazeni, encoding="utf-8")) if os.path.exists(a.stazeni) else []
    stare = [z for z in stare if z.get("zdroj") != "ČSÚ"] + zaznamy
    with open(a.stazeni, "w", encoding="utf-8") as f:
        json.dump(stare, f, ensure_ascii=False, indent=1)
    print(f"uloženo {len(zaznamy)} zpráv, {sum(z['bajtu'] for z in zaznamy) / 1e3:.0f} kB")


if __name__ == "__main__":
    main()
