"""Vybere vzorek textů z AI_Koditex_plain_texts.zip.

Ve všech vybraných skupinách (model × teplota) bere stejná ID textů, aby se
obsah mezi modely nelišil. Tím se dá odfiltrovat slovník konkrétních témat.

Použití:
  python3 -I sample.py ZIP OUTDIR --per-group 120 [--temps 0,100] [--seed 1]
  python3 -I sample.py ZIP --list            # jen vypíše skupiny a počty

--temps: které teploty brát (×100). Skupina, která preferovanou teplotu nemá
(např. o3, gpt-54 jen T=1), se vezme s tou, kterou má.
"""
import argparse
import os
import random
import sys
import zipfile
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import parse_group  # noqa: E402


def scan(zf):
    groups = defaultdict(dict)  # group -> {id: member}
    for info in zf.infolist():
        if info.is_dir() or not info.filename.lower().endswith(".txt"):
            continue
        parts = info.filename.replace("\\", "/").split("/")
        if len(parts) < 2:
            continue
        g, fname = parts[-2], parts[-1]
        if ".." in parts or info.filename.startswith("/"):
            continue  # bezpečnost: žádné cesty ven
        groups[g][os.path.splitext(fname)[0]] = info
    return groups


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("zip")
    ap.add_argument("outdir", nargs="?")
    ap.add_argument("--per-group", type=int, default=120)
    ap.add_argument("--temps", default="0,100", help="pořadí preference teplot ×100")
    ap.add_argument("--all-temps", action="store_true", help="vzít všechny teploty")
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--list", action="store_true")
    a = ap.parse_args()

    zf = zipfile.ZipFile(a.zip)
    groups = scan(zf)
    meta = {g: parse_group(g) for g in groups}
    if a.list:
        for g in sorted(groups):
            print(f"{g}\t{len(groups[g])}\t{meta[g]}")
        return

    pref = [int(x) for x in a.temps.split(",")]
    # vyber skupiny: pro každý (mode, model) jednu teplotu podle preference, nebo všechny
    chosen = []
    by_model = defaultdict(list)
    for g, m in meta.items():
        if m is None:
            print(f"přeskakuji neznámou složku {g}", file=sys.stderr)
            continue
        by_model[(m["mode"], m["model"])].append(g)
    for key, gs in sorted(by_model.items()):
        if a.all_temps:
            chosen += gs
            continue
        gs.sort(key=lambda g: (pref.index(round(meta[g]["temp"] * 100))
                               if round(meta[g]["temp"] * 100) in pref else 99))
        chosen.append(gs[0])

    common_ids = set.intersection(*(set(groups[g]) for g in chosen))
    ids = sorted(common_ids, key=lambda x: (len(x), x))
    random.Random(a.seed).shuffle(ids)
    ids = sorted(ids[: a.per_group], key=lambda x: (len(x), x))
    print(f"skupin: {len(chosen)}, společných ID: {len(common_ids)}, vybráno: {len(ids)}")

    os.makedirs(a.outdir, exist_ok=True)
    with open(os.path.join(a.outdir, "_ids.txt"), "w") as f:
        f.write("\n".join(ids) + "\n")
    for g in sorted(chosen):
        d = os.path.join(a.outdir, g)
        os.makedirs(d, exist_ok=True)
        for i in ids:
            data = zf.read(groups[g][i]).decode("utf-8", errors="replace")
            data = data.replace("\r\n", "\n").replace("\r", "\n")
            with open(os.path.join(d, f"{i}.txt"), "w", encoding="utf-8") as out:
                out.write(data)
    print("hotovo:", a.outdir)


if __name__ == "__main__":
    main()
