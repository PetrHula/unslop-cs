"""Převede exporty z KonTextu (lidská reference, Koditex) na skupinu pro compare.py.

  python3 -I kontext_ref.py OUT.json.gz --lemma-tag lemma_tag.csv --sents N
         [--starts starts.csv] [--queries dotazy.json] [--phrases slova_lemmata.json]
         [--name koditex_human]

lemma_tag.csv: export víceúrovňové frekvence dotazu [] (lemma, tag, četnost).
starts.csv:    export frekvence dotazu <s>[] podle lemmatu.
dotazy.json:   {"kx_coz": n, "kx_cimz": n, "kx_byt_adj_ze": n, "kx_korel": n, "kx_qmark": n}

Rysy z UD závislostí (adj_pred, koordinace, zvratné pasivum) z KonTextu spočítat
nejde; srovnávají se jen rysy kx_* a rysy z lemmat, definované stejně na obou stranách.
"""
import argparse
import csv
import gzip
import json
import os
import re
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import pdt_is_word, pdt_lex_lemma, pdt_norm_lemma, pdt_tag_features, vnoun_lemma  # noqa: E402
from features import KALKY, OPIS_JE, OUTLOOK, PARTICLES  # noqa: E402

TAG_RE = re.compile(r"^[A-Z][A-Za-z0-9=\-^:,~.!?*#%@}{\[\]]{14}$")
PDT2UPOS = {"N": "NOUN", "A": "ADJ", "P": "PRON", "C": "NUM", "V": "VERB", "D": "ADV", "R": "ADP",
            "J": "CCONJ", "T": "PART", "I": "INTJ", "Z": "PUNCT", "X": "X"}


def rows(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        sample = f.read(4096)
        f.seek(0)
        try:
            dialect = csv.Sniffer().sniff(sample, delimiters=",;\t")
        except csv.Error:
            dialect = csv.excel
        for row in csv.reader(f, dialect):
            row = [x.strip() for x in row]
            nums = [x for x in row if re.fullmatch(r"\d[\d\s]*", x)]
            if nums:
                yield row, int(nums[-1].replace(" ", ""))  # poslední celé číslo = abs. četnost


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("--lemma-tag", required=True)
    ap.add_argument("--sents", type=int, required=True)
    ap.add_argument("--starts")
    ap.add_argument("--queries")
    ap.add_argument("--phrases")
    ap.add_argument("--name", default="koditex_human_kontext")
    a = ap.parse_args()

    c, lem, lem_pos, lex = Counter(), Counter(), {}, Counter()
    bad = 0
    for row, n in rows(a.lemma_tag):
        tags = [x for x in row if TAG_RE.match(x)]
        if not tags:
            bad += 1
            continue
        tag = tags[0]
        ti = row.index(tag)
        lemma = row[ti - 1] if ti > 0 else (row[ti + 1] if ti + 1 < len(row) else "")
        if not lemma or not pdt_is_word(tag, lemma):
            continue
        c["kx_words"] += n
        c["words"] += n
        pdt_tag_features(tag, c, n)
        if tag.startswith("NNN") and vnoun_lemma(lemma):
            c["kx_vnoun"] += n
        key = pdt_norm_lemma(lemma, tag)
        lem[key] += n
        lem_pos.setdefault(key, PDT2UPOS.get(tag[0], "X"))
        lex[pdt_lex_lemma(lemma, tag)] += n
    print(f"slov {c['words']}, lemmat {len(lem)}, řádků bez značky {bad}", file=sys.stderr)

    # rysy z lemmat, stejné seznamy jako features.py
    for grp, lst in PARTICLES.items():
        for l in lst:
            c["part_" + grp] += lex.get(l, 0)
            c["lem:" + l] += lex.get(l, 0)
    for l in OPIS_JE:
        c["opis_je"] += lex.get(l, 0)
        c["lem:" + l] += lex.get(l, 0)
    for l in OUTLOOK:
        c["outlook"] += lex.get(l, 0)
        c["lem:" + l] += lex.get(l, 0)
    for l in KALKY + ["být", "mít"]:
        c["lem:" + l] += lex.get(l, 0)
    c["ktery"] = lex.get("který", 0)
    c["jenz"] = lex.get("jenž", 0)
    c["svuj"] = lex.get("svůj", 0)
    c["nejen"] = lex.get("nejen", 0)
    c["sents"] = a.sents
    c["docs"] = 0
    if a.queries:
        for k, v in json.load(open(a.queries, encoding="utf-8")).items():
            c[k] = v

    starts = {"0": {}}
    if a.starts:
        sc = Counter()
        for row, n in rows(a.starts):
            txt = [x for x in row if x and not re.fullmatch(r"[\d\s.,%]+", x)]
            if txt:
                sc[txt[0].lower()] += n
        starts["0"] = dict(sc)

    phrases = {}
    if a.phrases:
        for p in json.load(open(a.phrases, encoding="utf-8")):
            if len(p["lemmas"]) == 1:
                phrases[p["id"]] = lex.get(p["lemmas"][0], 0)

    res = {"group": a.name, "counts": dict(c), "lemmas": dict(lem), "lemma_df": {}, "lemma_pos": lem_pos,
           "bigrams": {}, "trigrams": {}, "starts": starts, "sent_len_hist": {}, "sttr_lemma": None,
           "sttr_noun100": None, "phrases": phrases, "phrases_df": {}, "per_doc": {}}
    with gzip.open(a.out, "wt", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False)


if __name__ == "__main__":
    main()
