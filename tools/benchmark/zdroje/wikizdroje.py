#!/usr/bin/env python3
"""Stáhne wikitext vybraných stránek z cs.wikisource.org (vrstva klasika, krok 1 PLAN.md).

Výběr je v wikizdroje_vyber.json: sbírky (stáhnou se i s podstránkami), jednotlivé
stránky a kategorie (bere se jen zbytek mimo ostatní skupiny). Každá stránka se uloží
jako JSON (titul, revid, časová značka revize, wikitext) do OUTDIR/stranky/ a záznam
o stažení (URL připnutá na revizi, licence, sha256) se připíše do STAZENI.

Obsah Wikizdrojů je pod CC BY-SA 4.0; vybrané texty mají šablonu PD old 70.
Opakované stažení stejných revizí: --revize OUTDIR/revize.json.

Použití:
    python3 -I wikizdroje.py wikizdroje_vyber.json ~/unslop-cs-data/benchmark/surove/wikizdroje \\
        --stazeni ~/unslop-cs-data/benchmark/stazeni.json
"""
import argparse
import datetime
import hashlib
import json
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request

API = "https://cs.wikisource.org/w/api.php"
UA = {"User-Agent": "unslop-benchmark/0.1 (research; low request rate)"}
LICENCE = "CC BY-SA 4.0 (Wikizdroje); text PD old 70"
LICENCE_URL = "https://creativecommons.org/licenses/by-sa/4.0/deed.cs"  # rightsinfo API
PAUZA = 2.0


def api(**p):
    p.update(format="json", formatversion="2", maxlag="5")
    data = urllib.parse.urlencode(p).encode()
    for pokus in range(6):
        time.sleep(PAUZA * (pokus + 1) ** 2)
        try:
            r = urllib.request.Request(API, data=data, headers=UA)
            return json.load(urllib.request.urlopen(r, timeout=90))
        except urllib.error.HTTPError as e:
            if e.code not in (429, 503):
                raise
        except (TimeoutError, urllib.error.URLError, OSError):
            pass
    raise SystemExit("API opakovaně selhalo")


def podstranky(prefix):
    tituly, pokracovani = [], {}
    while True:
        d = api(action="query", list="allpages", apprefix=prefix + "/", aplimit=500, **pokracovani)
        tituly += [p["title"] for p in d["query"]["allpages"]]
        if "continue" not in d:
            return tituly
        pokracovani = {"apcontinue": d["continue"]["apcontinue"]}


def kategorie(nazev):
    d = api(action="query", list="categorymembers", cmtitle=nazev, cmlimit=500, cmnamespace=0)
    return [p["title"] for p in d["query"]["categorymembers"]]


def stahni(tituly=None, revize=None):
    """Vrátí {titul: {revid, cas, wikitext}}; po 50 titulech nebo revizích."""
    out = {}
    klic, polozky = ("revids", revize) if revize else ("titles", tituly)
    for i in range(0, len(polozky), 50):
        d = api(action="query", prop="revisions", rvprop="ids|timestamp|content", rvslots="main",
                redirects=1, **{klic: "|".join(map(str, polozky[i:i + 50]))})
        presm = {}
        for k in ("normalized", "redirects"):
            for r in d["query"].get(k, []):
                presm[r["to"]] = presm.get(r["from"], r["from"])
        for p in d["query"].get("pages", []):
            if p.get("missing") or not p.get("revisions"):
                print("chybí:", p.get("title"))
                continue
            rv = p["revisions"][0]
            out[p["title"]] = {"revid": rv["revid"], "cas": rv["timestamp"],
                               "wikitext": rv["slots"]["main"]["content"],
                               "pozadovano": presm.get(p["title"], p["title"])}
    return out


def nazev_souboru(titul):
    bezpecny = re.sub(r"[^\w.-]+", "_", titul, flags=re.UNICODE).strip("_")[:120]
    return f"{bezpecny}-{hashlib.sha1(titul.encode()).hexdigest()[:8]}.json"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("vyber")
    ap.add_argument("outdir")
    ap.add_argument("--stazeni", required=True, help="stazeni.json, záznamy se připíšou")
    ap.add_argument("--revize", help="revize.json z dřívějšího běhu: stáhne stejné revize")
    a = ap.parse_args()

    vyber = json.load(open(a.vyber, encoding="utf-8"))
    os.makedirs(os.path.join(a.outdir, "stranky"), exist_ok=True)

    skupina = {}  # titul -> autor ze seznamu (None u kategorie)
    if a.revize:
        rev = json.load(open(a.revize, encoding="utf-8"))
        skupina = {t: v["autor"] for t, v in rev.items()}
        stranky = stahni(revize=[v["revid"] for v in rev.values()])
    else:
        kat = []
        for g in vyber["skupiny"]:
            for s in g["sbirky"]:
                for t in [s] + podstranky(s):
                    skupina[t] = g["autor"]
            for t in g["stranky"]:
                skupina[t] = g["autor"]
            if g.get("kategorie"):
                kat.append((g, kategorie(g["kategorie"])))
        for g, tituly in kat:
            for t in tituly:
                if t not in skupina and not any(t.startswith(s + "/") for s in skupina):
                    skupina[t] = g["autor"]
        stranky = stahni(tituly=sorted(skupina))

    datum = datetime.date.today().isoformat()
    zaznamy, revize = [], {}
    for titul, s in sorted(stranky.items()):
        soubor = nazev_souboru(titul)
        autor = skupina.get(titul, skupina.get(s["pozadovano"]))
        obsah = json.dumps({"titul": titul, "autor_vyber": autor, **s},
                           ensure_ascii=False, indent=1).encode("utf-8")
        with open(os.path.join(a.outdir, "stranky", soubor), "wb") as f:
            f.write(obsah)
        revize[titul] = {"revid": s["revid"], "autor": autor}
        zaznamy.append({"zdroj": "Wikizdroje", "titul": titul,
                        "soubor": f"surove/wikizdroje/stranky/{soubor}",
                        "url": f"https://cs.wikisource.org/w/index.php?oldid={s['revid']}",
                        "revid": s["revid"], "licence": LICENCE, "licence_overeni": LICENCE_URL,
                        "datum_stazeni": datum, "bajtu": len(obsah),
                        "sha256": hashlib.sha256(obsah).hexdigest()})
    with open(os.path.join(a.outdir, "revize.json"), "w", encoding="utf-8") as f:
        json.dump(revize, f, ensure_ascii=False, indent=1)
    stare = json.load(open(a.stazeni, encoding="utf-8")) if os.path.exists(a.stazeni) else []
    stare = [z for z in stare if z.get("zdroj") != "Wikizdroje"] + zaznamy
    with open(a.stazeni, "w", encoding="utf-8") as f:
        json.dump(stare, f, ensure_ascii=False, indent=1)
    print(f"staženo {len(stranky)} stránek z {len(skupina)} titulů, "
          f"{sum(z['bajtu'] for z in zaznamy) / 1e6:.2f} MB")


if __name__ == "__main__":
    main()
