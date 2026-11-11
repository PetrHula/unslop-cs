#!/usr/bin/env python3
"""Rozdělení na dev a test sadu a zámek test sady (krok 3 PLAN.md).

Jednotkou je shluk: dílo z manifestu (lidský text i všechny jeho AI protějšky), u vrstvy
aikoditex id textu Koditexu. Shluky se v každé vrstvě losují se seedem a přidávají do dev,
dokud dev nemá aspoň `dev_podil` textů vrstvy; zbytek je test.

Soubory se přesunou do DATA/dev/ a DATA/test/ (texty/, ai/<metoda>/<model>/,
ai/aikoditex/<model>/); vyřazené kontaminací se nepřesouvají a zůstanou v DATA/ai/.
Do repozitáře jde tools/benchmark/zamek.json: seed, datum, počty, sha256 seřazeného seznamu
testových souborů a sha256 každého z nich. Obsah test sady se při ladění pravidel nečte.

Použití:
    python3 -I tools/benchmark/rozdel.py --konfigurace tools/benchmark/konfigurace.json
"""
import argparse
import collections
import datetime
import hashlib
import json
import os
import random
import shutil

KOREN = os.path.dirname(os.path.abspath(__file__))


def sha(cesta):
    return hashlib.sha256(open(cesta, "rb").read()).hexdigest()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--konfigurace", required=True)
    a = ap.parse_args()
    cfg = json.load(open(a.konfigurace, encoding="utf-8"))
    data = os.path.expanduser(cfg["data"])
    podil = cfg["rozdeleni"]["dev_podil"]
    zamek_p = os.path.join(KOREN, "zamek.json")
    if os.path.exists(zamek_p):
        raise SystemExit("zamek.json už existuje: rozdělení je hotové a nemění se.")

    manifest = json.load(open(os.path.join(data, "manifest.json"), encoding="utf-8"))
    kontaminace = json.load(open(os.path.join(data, "ai", "kontaminace.json"), encoding="utf-8"))
    aikod = json.load(open(os.path.join(data, "ai", "aikoditex.json"), encoding="utf-8"))

    # shluky: (vrstva, klíč) -> [id lidských textů] ; aikoditex zvlášť
    shluky = collections.defaultdict(list)
    for z in manifest["texty"]:
        shluky[(z["vrstva"], z["dilo"])].append(z["id"])
    for z in aikod:
        shluky[("aikoditex", z["koditex_id"])].append(z["id"])

    sada = {}
    for vrstva in sorted({v for v, _ in shluky}):
        klice = sorted(k for k in shluky if k[0] == vrstva)
        random.Random(f"{cfg['seed']}:rozdeleni:{vrstva}").shuffle(klice)
        celkem = sum(len(shluky[k]) for k in klice)
        dev = 0
        for k in klice:
            s = "dev" if dev < podil * celkem else "test"
            for id_ in shluky[k]:
                sada[id_] = s
            dev += len(shluky[k]) if s == "dev" else 0

    # přesun souborů
    presuny = []  # (z, do, sada)
    for z in manifest["texty"]:
        presuny.append((f"texty/{z['id']}.txt", sada[z["id"]]))
    for r in open(os.path.join(data, "ai", "zaznamy.jsonl"), encoding="utf-8"):
        z = json.loads(r)
        if z.get("soubor") and not kontaminace.get(z["soubor"], {}).get("vyrazeno"):
            presuny.append((z["soubor"], sada[z["id"]]))
    for z in aikod:
        presuny.append((z["soubor"], sada[z["id"]]))
    test_soubory = {}
    for rel, s in presuny:
        src = os.path.join(data, rel)
        dst = os.path.join(data, s, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.move(src, dst)
        if s == "test":
            test_soubory[f"{s}/{rel}"] = sha(dst)

    for z in manifest["texty"]:
        z["sada"] = sada[z["id"]]
    with open(os.path.join(data, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=1)
    with open(os.path.join(data, "rozdeleni.json"), "w", encoding="utf-8") as f:
        json.dump(sada, f, ensure_ascii=False, indent=1, sort_keys=True)

    pocty = collections.Counter()
    for (vrstva, _), ids in shluky.items():
        for id_ in ids:
            pocty[f"{vrstva}:{sada[id_]}"] += 1
    seznam = "\n".join(sorted(test_soubory))
    zamek = {"popis": "Zámek test sady (PLAN.md, krok 3). Obsah test sady se při ladění pravidel nečte.",
             "seed": cfg["seed"], "dev_podil": podil, "datum": datetime.date.today().isoformat(),
             "pocty_textu": dict(sorted(pocty.items())),
             "test_souboru": len(test_soubory),
             "sha256_seznamu": hashlib.sha256(seznam.encode("utf-8")).hexdigest(),
             "soubory": dict(sorted(test_soubory.items()))}
    with open(zamek_p, "w", encoding="utf-8", newline="\n") as f:
        json.dump(zamek, f, ensure_ascii=False, indent=1)
    print("textů po vrstvách a sadách:", dict(sorted(pocty.items())))
    print(f"přesunuto {len(presuny)} souborů, testových {len(test_soubory)}")


if __name__ == "__main__":
    main()
