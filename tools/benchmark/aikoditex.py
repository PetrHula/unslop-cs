#!/usr/bin/env python3
"""Vrstva aikoditex: AI texty z AI-Koditexu v2 bez lidského páru (krok 2 PLAN.md).

Bere jen instruované modely (složky koditex_chat_*) a teploty z konfigurace. Vzorek je
vyvážený přes modely a každé id textu Koditexu se použije nejvýš jednou (různý obsah).
První věta souboru je useknutá promptem, proto se vynechá (jako v tools/koditex/parse.py);
zbytek se zkrátí na úsek 200–600 slov pravidly korpus.py.

Výstup: DATA/ai/aikoditex/<model>__<teplota>/<id>.txt a DATA/ai/aikoditex.json.

Použití:
    python3 -I tools/benchmark/aikoditex.py --konfigurace tools/benchmark/konfigurace.json
"""
import argparse
import collections
import hashlib
import json
import os
import random
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from korpus import norm, slov, useky, vety  # noqa: E402

ZDROJ_URL = "http://hdl.handle.net/11234/1-6189"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--konfigurace", required=True)
    a = ap.parse_args()
    k = json.load(open(a.konfigurace, encoding="utf-8"))
    c = k["aikoditex"]
    zdroj = os.path.expanduser(c["zdroj"])
    data = os.path.expanduser(k["data"])
    rnd = random.Random(f"{k['seed']}:aikoditex")

    skupiny = collections.defaultdict(list)  # model -> [(slozka, id)]
    for slozka in sorted(os.listdir(zdroj)):
        m = re.fullmatch(r"koditex_chat_(.+)__(\w+)", slozka)
        if not m or m.group(2) not in c["teploty"] or "default-system" in m.group(1):
            continue
        for f in sorted(os.listdir(os.path.join(zdroj, slozka))):
            skupiny[m.group(1)].append((slozka, f[:-4]))
    modely = sorted(skupiny)
    for m in modely:
        rnd.shuffle(skupiny[m])
    print(f"modelů {len(modely)}")

    vybrane, pouzita_id, kurzor = [], set(), collections.Counter()
    while len(vybrane) < c["pocet"]:
        pridano = False
        for m in modely:
            if len(vybrane) >= c["pocet"]:
                break
            while kurzor[m] < len(skupiny[m]):
                slozka, id_ = skupiny[m][kurzor[m]]
                kurzor[m] += 1
                if id_ in pouzita_id:
                    continue
                text = open(os.path.join(zdroj, slozka, id_ + ".txt"), encoding="utf-8").read()
                vv = vety(norm(text))[1:]  # první věta je useknutá promptem
                u = useky([vv])
                if not u:
                    continue
                vybrane.append((m, slozka, id_, "\n\n".join(u[0]) + "\n"))
                pouzita_id.add(id_)
                pridano = True
                break
        if not pridano:
            break

    zaznamy = []
    for m, slozka, id_, text in vybrane:
        teplota = slozka.rsplit("__", 1)[1]
        rel = f"ai/aikoditex/{m}__{teplota}/{id_}.txt"
        os.makedirs(os.path.join(data, os.path.dirname(rel)), exist_ok=True)
        with open(os.path.join(data, rel), "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
        zaznamy.append({"id": f"aikoditex-{id_}", "koditex_id": id_, "model": m, "teplota": teplota,
                        "soubor": rel, "slov": slov(text), "sha256": hashlib.sha256(text.encode()).hexdigest(),
                        "zdroj": "AI-Koditex v2", "url": ZDROJ_URL, "licence": "viz LINDAT 11234/1-6189"})
    with open(os.path.join(data, "ai", "aikoditex.json"), "w", encoding="utf-8") as f:
        json.dump(zaznamy, f, ensure_ascii=False, indent=1)
    print(f"vybráno {len(zaznamy)} textů z {len({z['model'] for z in zaznamy})} modelů")


if __name__ == "__main__":
    main()
