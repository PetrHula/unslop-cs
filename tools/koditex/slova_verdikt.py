"""Porovná položky `slova.md` s lidskou referencí a přiřadí verdikt.

  python3 -I slova_verdikt.py FEAT_DIR slova_lemmata.json OUT.csv [--ref koditex_human_kontext]

Jednoslovné položky se srovnávají na lemmatech (AI skupiny chat_* proti referenci).
Víceslovné položky mají jen četnost na AI straně (reference z KonTextu n-gramy nemá).

Verdikt: potvrzeno = LR celkem >= 1 a nad u >= 13 z 25 modelů;
náznak = LR >= 0,58 (1,5×) a vyšší u >= 17 modelů; opačně = LR <= -0,58;
málo dat = součet výskytů na obou stranách < 20.
"""
import argparse
import csv
import glob
import gzip
import json
import math
import os


def lr(a, n1, b, n2):
    return math.log2(((a + 0.5) / n1) / ((b + 0.5) / n2))


def g2(a, n1, b, n2):
    e1, e2 = n1 * (a + b) / (n1 + n2), n2 * (a + b) / (n1 + n2)
    return 2 * ((a * math.log(a / e1) if a else 0) + (b * math.log(b / e2) if b else 0))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("feat_dir")
    ap.add_argument("items")
    ap.add_argument("out")
    ap.add_argument("--ref", default="koditex_human_kontext")
    a = ap.parse_args()
    with gzip.open(os.path.join(a.feat_dir, a.ref + ".json.gz"), "rt", encoding="utf-8") as f:
        ref = json.load(f)
    R = ref["lemmas"]
    RN = sum(R.values())
    G = []
    for p in sorted(glob.glob(os.path.join(a.feat_dir, "koditex_chat_*.json.gz"))):
        with gzip.open(p, "rt", encoding="utf-8") as f:
            G.append(json.load(f))
    NA = sum(g["counts"]["words"] for g in G)
    out = []
    for it in json.load(open(a.items, encoding="utf-8")):
        key = it["id"] + ("#tvar" if it["level"] in ("FRAZE", "P0") else "")
        n_ai = sum(g["phrases"].get(key, 0) for g in G)
        row = {"id": it["id"], "level": it["level"], "text": it["text"], "lemmas": " ".join(it["lemmas"]),
               "ai_n": n_ai, "ai_ipm": n_ai / NA * 1e6,
               "n_models_present": sum(1 for g in G if g["phrases"].get(key, 0) > 0)}
        if len(it["lemmas"]) == 1:
            b = R.get(it["lemmas"][0], 0)
            per = [(lr(g["phrases"].get(key, 0), g["counts"]["words"], b, RN),
                    g2(g["phrases"].get(key, 0), g["counts"]["words"], b, RN)) for g in G]
            row.update(ref_ipm=b / RN * 1e6, lr_pooled=lr(n_ai, NA, b, RN),
                       n_over=sum(1 for x, s in per if x >= 1 and s >= 15.13),
                       n_under=sum(1 for x, s in per if x <= -1 and s >= 15.13),
                       n_higher=sum(1 for x, _ in per if x > 0))
            if n_ai + b < 20:
                v = "málo dat"
            elif row["lr_pooled"] >= 1 and row["n_over"] >= 13:
                v = "potvrzeno"
            elif row["lr_pooled"] >= 0.58 and row["n_higher"] >= 17:
                v = "náznak"
            elif row["lr_pooled"] <= -0.58:
                v = "opačně"
            else:
                v = "nepotvrzeno"
        else:
            v = "bez reference" if n_ai else "v korpusu není"
        row["verdikt"] = v
        out.append(row)
    fields = ["id", "level", "text", "lemmas", "ai_n", "ai_ipm", "ref_ipm", "lr_pooled", "n_over", "n_under",
              "n_higher", "n_models_present", "verdikt"]
    with open(a.out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(out)


if __name__ == "__main__":
    main()
