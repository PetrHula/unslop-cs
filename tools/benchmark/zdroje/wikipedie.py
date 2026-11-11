#!/usr/bin/env python3
"""Stáhne souvislou prózu z článků české Wikipedie, poslední revize před datem (vrstva wiki).

Výběr: články (jmenný prostor 0) z kategorií Dobré a Nejlepší články, losované se
seedem; článek bez revize před datem se přeskočí a losuje se další. Z revize se přes
action=parse vezme HTML a uloží se jen odstavce <p> mimo tabulky a infoboxy, bez
odkazů na reference. Celé HTML se neukládá.

Licence: CC BY-SA 4.0 (revize před 2023 částečně CC BY-SA 3.0); autoři = historie revize.

Použití:
    python3 -I wikipedie.py ~/unslop-cs-data/benchmark/surove/wikipedie \\
        --stazeni ~/unslop-cs-data/benchmark/stazeni.json --pocet 30 --seed 20261111
Opakování se stejnými revizemi: --revize OUTDIR/revize.json
"""
import argparse
import datetime
import hashlib
import html.parser
import json
import os
import random
import re
import time
import urllib.error
import urllib.parse
import urllib.request

API = "https://cs.wikipedia.org/w/api.php"
UA = {"User-Agent": "unslop-benchmark/0.1 (research; low request rate)"}
KATEGORIE = ["Kategorie:Wikipedie:Dobré články", "Kategorie:Wikipedie:Nejlepší články"]
LICENCE = "CC BY-SA (3.0/4.0 podle data revize)"
LICENCE_URL = "https://cs.wikipedia.org/wiki/Wikipedie:Licence_Creative_Commons_Uveďte_původ-Zachovejte_licenci_4.0_Mezinárodní"
PAUZA = 1.0


def api(**p):
    p.update(format="json", formatversion="2", maxlag="5")
    data = urllib.parse.urlencode(p).encode()
    for pokus in range(6):
        time.sleep(PAUZA * (pokus + 1) ** 2)
        try:
            return json.load(urllib.request.urlopen(urllib.request.Request(API, data=data, headers=UA),
                                                    timeout=90))
        except urllib.error.HTTPError as e:
            if e.code not in (429, 503):
                raise
        except (TimeoutError, urllib.error.URLError, OSError):
            pass
    raise SystemExit("API opakovaně selhalo")


def clenove(kat):
    tituly, dalsi = [], {}
    while True:
        d = api(action="query", list="categorymembers", cmtitle=kat, cmnamespace=0, cmlimit=500, **dalsi)
        tituly += [p["title"] for p in d["query"]["categorymembers"]]
        if "continue" not in d:
            return tituly
        dalsi = {"cmcontinue": d["continue"]["cmcontinue"]}


def revize_pred(titul, datum):
    d = api(action="query", prop="revisions", titles=titul, rvlimit=1, rvdir="older",
            rvstart=datum + "T00:00:00Z", rvprop="ids|timestamp")
    p = d["query"]["pages"][0]
    rv = (p.get("revisions") or [None])[0]
    return (rv["revid"], rv["timestamp"]) if rv else None


class Odstavce(html.parser.HTMLParser):
    """Text odstavců <p>, které neleží v tabulce, infoboxu, poznámce ani navigaci."""
    PRESKOC = {"table", "style", "script", "figure", "math"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.zasobnik, self.odstavce, self.p = [], [], None

    def _preskakuje(self):
        return any(t in self.PRESKOC or skip for t, skip in self.zasobnik)

    def handle_starttag(self, tag, attrs):
        if tag in ("br", "img", "wbr", "meta", "link", "input"):
            return
        a = dict(attrs)
        trida = a.get("class") or ""
        skip = (tag == "sup" and "reference" in trida) or "mw-editsection" in trida \
            or "noprint" in trida or "mwe-math" in trida or (tag == "span" and "mw-ref" in trida)
        self.zasobnik.append((tag, skip))
        if tag == "p" and not self._preskakuje():
            self.p = []

    def handle_endtag(self, tag):
        while self.zasobnik:
            t, _ = self.zasobnik.pop()
            if t == tag:
                break
        if tag == "p" and self.p is not None:
            text = re.sub(r"\s+", " ", "".join(self.p)).strip()
            if text:
                self.odstavce.append(text)
            self.p = None

    def handle_data(self, data):
        if self.p is not None and not self._preskakuje():
            self.p.append(data)


def proza(revid):
    d = api(action="parse", oldid=revid, prop="text", disablelimitreport=1, disableeditsection=1)
    o = Odstavce()
    o.feed(d["parse"]["text"])
    return [re.sub(r"\[\d+\]|\[pozn\. \d+\]", "", x).strip() for x in o.odstavce]


def nazev_souboru(titul):
    bezpecny = re.sub(r"[^\w.-]+", "_", titul, flags=re.UNICODE).strip("_")[:120]
    return f"{bezpecny}-{hashlib.sha1(titul.encode()).hexdigest()[:8]}.json"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("outdir")
    ap.add_argument("--stazeni", required=True)
    ap.add_argument("--pocet", type=int, default=30)
    ap.add_argument("--seed", type=int, default=20261111)
    ap.add_argument("--pred", default="2022-01-01", help="brát poslední revizi před tímto datem")
    ap.add_argument("--min-slov", type=int, default=300, help="minimum slov prózy v článku")
    ap.add_argument("--revize", help="revize.json z dřívějšího běhu")
    a = ap.parse_args()
    os.makedirs(os.path.join(a.outdir, "clanky"), exist_ok=True)

    vybrano = {}
    if a.revize:
        for t, v in json.load(open(a.revize, encoding="utf-8")).items():
            vybrano[t] = (v["revid"], v["cas"], v["kategorie"])
            vybrano[t] += (proza(v["revid"]),)
    else:
        kandidati = []
        for k in KATEGORIE:
            kandidati += [(t, k) for t in clenove(k)]
        kandidati = sorted(set(kandidati))
        random.Random(a.seed).shuffle(kandidati)
        print(f"kandidátů {len(kandidati)}")
        for t, k in kandidati:
            if len(vybrano) >= a.pocet:
                break
            if t in vybrano:
                continue
            rv = revize_pred(t, a.pred)
            if not rv:
                print("bez revize před datem:", t)
                continue
            odst = proza(rv[0])
            if sum(len(x.split()) for x in odst) < a.min_slov:
                print("málo prózy:", t)
                continue
            vybrano[t] = (rv[0], rv[1], k, odst)

    datum = datetime.date.today().isoformat()
    zaznamy, revize = [], {}
    for t, (revid, cas, kat, odst) in sorted(vybrano.items()):
        soubor = nazev_souboru(t)
        obsah = json.dumps({"titul": t, "revid": revid, "cas": cas, "kategorie": kat, "odstavce": odst},
                           ensure_ascii=False, indent=1).encode("utf-8")
        with open(os.path.join(a.outdir, "clanky", soubor), "wb") as f:
            f.write(obsah)
        revize[t] = {"revid": revid, "cas": cas, "kategorie": kat}
        zaznamy.append({"zdroj": "Wikipedie", "titul": t, "soubor": f"surove/wikipedie/clanky/{soubor}",
                        "url": f"https://cs.wikipedia.org/w/index.php?oldid={revid}", "revid": revid,
                        "cas_revize": cas, "licence": LICENCE, "licence_overeni": LICENCE_URL,
                        "datum_stazeni": datum, "bajtu": len(obsah),
                        "sha256": hashlib.sha256(obsah).hexdigest()})
    with open(os.path.join(a.outdir, "revize.json"), "w", encoding="utf-8") as f:
        json.dump(revize, f, ensure_ascii=False, indent=1)
    stare = json.load(open(a.stazeni, encoding="utf-8")) if os.path.exists(a.stazeni) else []
    stare = [z for z in stare if z.get("zdroj") != "Wikipedie"] + zaznamy
    with open(a.stazeni, "w", encoding="utf-8") as f:
        json.dump(stare, f, ensure_ascii=False, indent=1)
    print(f"uloženo {len(zaznamy)} článků, {sum(z['bajtu'] for z in zaznamy) / 1e6:.2f} MB")


if __name__ == "__main__":
    main()
