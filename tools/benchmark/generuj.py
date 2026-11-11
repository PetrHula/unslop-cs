#!/usr/bin/env python3
"""AI protějšky k lidským textům korpusu (krok 2 PLAN.md).

Ke každému textu z DATA/manifest.json a každému modelu z konfigurace:
  (a) pokracovani – začátek lidského textu (~100 slov, konec věty) a pokyn pokračovat
      stejným stylem v délce zbytku; porovnává se se skutečným pokračováním autora;
  (b) chatbot – „Napiš <žánr> na téma X, asi N slov“; téma X do 10 slov napíše levný model.
Výstup: DATA/ai/<metoda>/<model>/<id>.txt, DATA/ai/temata.json, DATA/ai/zaznamy.jsonl
(záznam na volání: zadání, verze modelu, cena, tokeny, čas, sha256).
Běh jde přerušit a pustit znovu: hotové soubory se přeskočí.

Rozpočet: po prvních 12 voláních odhadne cenu celku; když přesáhne max_usd, skončí.

Použití:
    python3 -I tools/benchmark/generuj.py --konfigurace tools/benchmark/konfigurace.json [--jen 5]
"""
import argparse
import concurrent.futures
import datetime
import hashlib
import json
import os
import random
import re
import sys
import threading

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cli import s_opakovanim, zavolej  # noqa: E402
from korpus import slov, vety  # noqa: E402

SYSTEM = "Jsi pomocník, který píše česky."
SYSTEM_TEMA = "Odpovídáš stručně česky."

ZADANI_POKRACOVANI = """Tady je začátek českého textu. Pokračuj v něm tak, aby přirozeně navazoval: stejný styl, tón, žánr i doba. Napiš asi {n} slov. Vypiš jen pokračování, bez opakování začátku, bez nadpisu a bez komentáře.

<zacatek>
{prefix}
</zacatek>"""

ZADANI_CHATBOT = "Napiš {zanr} na téma: {tema}. Rozsah asi {n} slov. Vypiš jen samotný text, bez nadpisu."

ZADANI_TEMA = """Napiš téma následujícího textu nejvýš deseti slovy, jako by sis ho zadával pro psaní podobného textu. Necituj z textu, neuváděj autora ani žánr. Odpověz jen tématem, bez tečky.

<text>
{text}
</text>"""

ZANRY = {"fejeton": "fejeton", "sloupek": "novinový sloupek", "humoreska": "humoresku",
         "povídka": "povídku", "publicistika": "novinový komentář", "novinový": "novinový článek",
         "odborný": "odborný text", "administrativní": "úřední text", "beletrie": "úryvek z románu",
         "encyklopedický": "encyklopedické heslo", "tisková zpráva": "tiskovou zprávu"}

_ZAMEK = threading.Lock()


def rozdel_prefix(text, cil):
    """Vrátí (prefix, zbytek) jako texty s odstavci; prefix končí na konci věty od `cil` slov."""
    odstavce = [o for o in text.strip().split("\n\n") if o.strip()]
    prefix, zbytek, pocet = [], [], 0
    for i, o in enumerate(odstavce):
        if pocet >= cil:
            zbytek.extend(odstavce[i:])
            break
        vv = vety(o)
        for k, v in enumerate(vv):
            if pocet >= cil:
                prefix.append(" ".join(vv[:k]))
                zbytek.append(" ".join(vv[k:]))
                zbytek.extend(odstavce[i + 1:])
                return "\n\n".join(prefix), "\n\n".join(zbytek)
            pocet += slov(v)
        prefix.append(o)
    return "\n\n".join(prefix), "\n\n".join(zbytek)


def ocisti(vystup, prefix=None):
    t = vystup.strip().strip("`").strip()
    radky = t.split("\n")
    if radky and re.match(r"^(#+\s|\*\*[^*]{1,80}\*\*\s*$)", radky[0]):
        t = "\n".join(radky[1:]).strip()  # nadpis navzdory pokynu
    if prefix:
        zac = " ".join(prefix.split()[:10])
        if zac and " ".join(t.split()[:10]) == zac:
            t = t[len(prefix):].strip() if t.startswith(prefix) else t
    return re.sub(r"\n{3,}", "\n\n", t) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--konfigurace", required=True)
    ap.add_argument("--jen", type=int, help="jen prvních N textů (zkouška)")
    a = ap.parse_args()
    k = json.load(open(a.konfigurace, encoding="utf-8"))
    g = k["generovani"]
    data = os.path.expanduser(k["data"])
    manifest = json.load(open(os.path.join(data, "manifest.json"), encoding="utf-8"))["texty"]
    texty = [z for z in manifest if not z.get("soukromy")]
    if a.jen:
        texty = texty[:a.jen]
    ai = os.path.join(data, "ai")
    os.makedirs(ai, exist_ok=True)
    zaznamy_p = os.path.join(ai, "zaznamy.jsonl")
    hotovo = set()
    utraceno = 0.0
    if os.path.exists(zaznamy_p):
        for r in open(zaznamy_p, encoding="utf-8"):
            z = json.loads(r)
            utraceno += z.get("cena") or 0
            if z.get("soubor") and os.path.exists(os.path.join(data, z["soubor"])):
                hotovo.add((z["metoda"], z["model_pozadovany"], z["id"]))
    print(f"z dřívějška utraceno {utraceno:.2f} USD, hotových volání {len(hotovo)}")

    def zapis(z):
        with _ZAMEK:
            with open(zaznamy_p, "a", encoding="utf-8") as f:
                f.write(json.dumps(z, ensure_ascii=False) + "\n")

    text_of = {z["id"]: open(os.path.join(data, "texty", z["id"] + ".txt"), encoding="utf-8").read()
               for z in texty}

    # 1) témata
    temata_p = os.path.join(ai, "temata.json")
    temata = json.load(open(temata_p, encoding="utf-8")) if os.path.exists(temata_p) else {}
    stav = {"cena": utraceno, "volani": 0, "stop": False}

    def tema(z):
        r, chyby = s_opakovanim(zavolej, ZADANI_TEMA.format(text=text_of[z["id"]]), g["model_temat"],
                                SYSTEM_TEMA, timeout=g["timeout_s"])
        if r is None:
            return z["id"], None, chyby
        t = r["text"].strip().strip(".").strip("„“\"")
        zapis({"id": z["id"], "metoda": "tema", "model_pozadovany": g["model_temat"], "model": r["model"],
               "cena": r["cena"], "tokeny": r["tokeny"], "cas_s": r["cas_s"], "vystup": t})
        return z["id"], (t, r["cena"]), chyby

    chybi = [z for z in texty if z["id"] not in temata]
    with concurrent.futures.ThreadPoolExecutor(max_workers=g["jobs"]) as ex:
        for id_, v, chyby in ex.map(tema, chybi):
            if v is None:
                print(f"téma {id_}: selhalo {chyby[-1:]}")
                continue
            temata[id_] = v[0]
            stav["cena"] += v[1]
    with open(temata_p, "w", encoding="utf-8") as f:
        json.dump(temata, f, ensure_ascii=False, indent=1)
    print(f"témata: {len(temata)}; utraceno {stav['cena']:.2f} USD")

    # 2) protějšky
    ulohy = [(m, metoda, z) for z in texty for m in g["modely"] for metoda in ("pokracovani", "chatbot")
             if (metoda, m, z["id"]) not in hotovo and (metoda == "pokracovani" or z["id"] in temata)]
    random.Random(k["seed"]).shuffle(ulohy)  # promíchat kvůli odhadu ceny
    celkem = len(ulohy)
    print(f"úloh: {celkem}")

    def uloha(m, metoda, z):
        if stav["stop"]:
            return None
        text = text_of[z["id"]]
        if metoda == "pokracovani":
            prefix, zbytek = rozdel_prefix(text, g["prefix_slov"])
            n = max(50, round(slov(zbytek), -1))
            zadani = ZADANI_POKRACOVANI.format(n=n, prefix=prefix)
        else:
            prefix, n = None, round(z["slov"], -1)
            zadani = ZADANI_CHATBOT.format(zanr=ZANRY.get(z["zanr"], "text"), tema=temata[z["id"]], n=n)
        r, chyby = s_opakovanim(zavolej, zadani, m, SYSTEM, timeout=g["timeout_s"])
        zaznam = {"id": z["id"], "vrstva": z["vrstva"], "metoda": metoda, "model_pozadovany": m,
                  "zadani": zadani, "pozadovano_slov": n, "infra_chyby": chyby,
                  "datum": datetime.date.today().isoformat()}
        if r is None:
            zaznam["selhalo"] = True
            zapis(zaznam)
            return zaznam
        vystup = ocisti(r["text"], prefix)
        soubor = f"ai/{metoda}/{m}/{z['id']}.txt"
        os.makedirs(os.path.join(data, os.path.dirname(soubor)), exist_ok=True)
        with open(os.path.join(data, soubor), "w", encoding="utf-8", newline="\n") as f:
            f.write(vystup)
        zaznam.update(model=r["model"], cena=r["cena"], tokeny=r["tokeny"], cas_s=r["cas_s"], soubor=soubor,
                      slov=slov(vystup), sha256=hashlib.sha256(vystup.encode("utf-8")).hexdigest(),
                      prefix_slov=slov(prefix) if prefix else None)
        zapis(zaznam)
        with _ZAMEK:
            stav["cena"] += r["cena"]
            stav["volani"] += 1
            if stav["volani"] == 12:
                odhad = utraceno + (stav["cena"] - utraceno) / 12 * celkem
                print(f"odhad ceny celku: {odhad:.2f} USD")
                if odhad > g["max_usd"]:
                    stav["stop"] = True
                    print(f"STOP: odhad přes {g['max_usd']} USD")
            if stav["cena"] > g["max_usd"]:
                stav["stop"] = True
        return zaznam

    hotove = selhane = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=g["jobs"]) as ex:
        fut = [ex.submit(uloha, *u) for u in ulohy]
        for i, f in enumerate(concurrent.futures.as_completed(fut), 1):
            z = f.result()
            if z is None:
                continue
            if z.get("selhalo"):
                selhane += 1
            else:
                hotove += 1
            if i % 50 == 0:
                print(f"[{i}/{celkem}] hotovo {hotove}, selhalo {selhane}, {stav['cena']:.2f} USD", flush=True)
    print(f"hotovo {hotove}, selhalo {selhane}, přeskočeno kvůli rozpočtu {celkem - hotove - selhane}; "
          f"utraceno celkem {stav['cena']:.2f} USD")


if __name__ == "__main__":
    main()
