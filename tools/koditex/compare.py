"""Porovná skupiny AI-Koditexu s referencí a vypíše tabulky pro F2.

Reference (jedno z):
  --ref-group G [G ...]   skupiny z FEAT_DIR, sečtou se (lidská reference zpracovaná
                          stejným modelem, nebo zástupně základní modely complete_*)
  --ref-csv SOUBOR        frekvenční seznam lemmat z KonTextu (CSV) + --ref-tokens N
                          (jen lemmata; n-gramy a rysy z něj spočítat nejde)
  --ref-features SOUBOR   JSON {rys: hodnota na 1 000 slov} z dotazů v KonTextu (volitelně)

Použití:
  python3 -I compare.py FEAT_DIR OUTDIR --ref-group koditex_complete_davinci-002__100 ...
  python3 -I compare.py FEAT_DIR OUTDIR --ref-csv koditex_lemmata.csv --ref-tokens 9000000

Statistika: log-ratio (Hardie 2014, +0,5 k četnostem) a log-likelihood G2 (Rayson);
lemma je nadreprezentované u modelu, když LR >= 1 (2× častěji) a G2 >= 15,13 (p < 0,0001).
"""
import argparse
import csv
import gzip
import json
import math
import os
import random
import re
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import parse_group  # noqa: E402

G2_CRIT = 15.13
SENT_LEVEL = re.compile(r"^(start_|question|exclam|adj_coz|adj_cimz|adj_a_tim|contrast_|sent_|kx_qmark|kx_coz|kx_cimz)")


def load(path):
    with gzip.open(path, "rt", encoding="utf-8") as f:
        return json.load(f)


def lr(a, n1, b, n2):
    return math.log2(((a + 0.5) / n1) / ((b + 0.5) / n2))


def g2(a, n1, b, n2):
    e1 = n1 * (a + b) / (n1 + n2)
    e2 = n2 * (a + b) / (n1 + n2)
    s = 0.0
    if a:
        s += a * math.log(a / e1)
    if b:
        s += b * math.log(b / e2)
    return 2 * s


def pool(groups, key):
    c = Counter()
    for g in groups:
        c.update(g[key])
    return c


def read_kontext_csv(path):
    """Robustní čtení exportu frekvenčního seznamu: bere řádky, kde je poslední
    číselný sloupec četnost a první nečíselný sloupec položka."""
    c = Counter()
    with open(path, encoding="utf-8-sig", newline="") as f:
        sample = f.read(4096)
        f.seek(0)
        try:
            dialect = csv.Sniffer().sniff(sample, delimiters=",;\t")
        except csv.Error:
            dialect = csv.excel
        for row in csv.reader(f, dialect):
            nums = [x for x in row if re.fullmatch(r"\d+", x.strip().replace(" ", ""))]
            txt = [x for x in row if x.strip() and not re.fullmatch(r"[\d.,\s]+", x.strip())]
            if nums and txt:
                c[txt[0].strip().lower()] += int(nums[0].replace(" ", ""))
    return c


def keyness(ai_groups, ref_c, ref_n, key, min_freq, min_df_share, exclude):
    """Vrátí seznam řádků s LR a G2 pro každý model zvlášť a souhrnem."""
    pooled = pool(ai_groups, key)
    pooled_n = sum(g["counts"]["words"] for g in ai_groups)
    docs = sum(g["counts"]["docs"] for g in ai_groups)
    df = pool(ai_groups, "lemma_df") if key == "lemmas" else None
    rows = []
    items = set(pooled) | (set(ref_c) if key == "lemmas" else set())
    for it in items:
        if any(e in it for e in exclude):
            continue
        a_tot, b = pooled.get(it, 0), ref_c.get(it, 0)
        if a_tot + b < min_freq:
            continue
        if df is not None and a_tot and df.get(it, 0) / docs < min_df_share and a_tot > b:
            continue
        per = []
        for g in ai_groups:
            a, n = g[key].get(it, 0), g["counts"]["words"]
            per.append((lr(a, n, b, ref_n), g2(a, n, b, ref_n), a))
        lrs = sorted(p[0] for p in per)
        rows.append({
            "item": it,
            "ai_ipm": a_tot / pooled_n * 1e6,
            "ref_ipm": b / ref_n * 1e6,
            "lr_pooled": lr(a_tot, pooled_n, b, ref_n),
            "g2_pooled": g2(a_tot, pooled_n, b, ref_n),
            "lr_median": lrs[len(lrs) // 2],
            "n_over": sum(1 for x, s, _ in per if x >= 1 and s >= G2_CRIT),
            "n_under": sum(1 for x, s, _ in per if x <= -1 and s >= G2_CRIT),
            "n_models": len(per),
            "df_share": (df.get(it, 0) / docs) if df is not None else None,
        })
    return rows


def sd_from_hist(h):
    n = sum(h.values())
    if not n:
        return None, None
    m = sum(int(k) * v for k, v in h.items()) / n
    var = sum(v * (int(k) - m) ** 2 for k, v in h.items()) / n
    return m, math.sqrt(var)


def feature_rates(counts):
    w, s = counts.get("words", 0), counts.get("sents", 0)
    out = {}
    for k, v in counts.items():
        if k in ("words", "sents", "docs") or k.startswith(("lem:", "start_conn:", "vn:")):
            continue
        if SENT_LEVEL.match(k):
            out[k] = v / s * 100 if s else None
        elif k.startswith("kx_"):
            kw = counts.get("kx_words") or w
            out[k] = v / kw * 1000 if kw else None
        else:
            out[k] = v / w * 1000 if w else None
    for k, v in counts.items():
        if k.startswith("lem:"):
            out[k] = v / w * 1000
        if k.startswith("start_conn:"):
            out[k] = v / s * 100
    out["words_per_sent"] = w / s if s else 0
    return out


def bootstrap_ratio(ai_docs, ref_docs, feat, sent_level, iters=500, seed=1):
    rnd = random.Random(seed)

    def rate(docs):
        num = sum(d.get(feat, 0) for d in docs)
        den = sum(d.get("sents" if sent_level else "words", 0) for d in docs)
        return num / den if den else 0

    vals = []
    for _ in range(iters):
        a = [rnd.choice(ai_docs) for _ in ai_docs]
        b = [rnd.choice(ref_docs) for _ in ref_docs]
        rb = rate(b)
        if rb:
            vals.append(rate(a) / rb)
    if not vals:
        return None, None
    vals.sort()
    return vals[int(0.025 * len(vals))], vals[int(0.975 * len(vals)) - 1]


def fmt(x, d=2):
    if x is None:
        return "–"
    if isinstance(x, float):
        return f"{x:.{d}f}".replace(".", ",")
    return str(x)


def md_table(rows, cols, headers):
    out = ["| " + " | ".join(headers) + " |", "|" + "---|" * len(headers)]
    for r in rows:
        out.append("| " + " | ".join(fmt(r.get(c)) for c in cols) + " |")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("feat_dir")
    ap.add_argument("outdir")
    ap.add_argument("--ref-group", nargs="*", default=[])
    ap.add_argument("--ref-csv")
    ap.add_argument("--ref-tokens", type=int)
    ap.add_argument("--ref-features")
    ap.add_argument("--ai-mode", default="chat", help="chat | complete | all")
    ap.add_argument("--min-freq", type=int, default=50)
    ap.add_argument("--min-df", type=float, default=0.10, help="lemma musí být aspoň v takovém podílu textů")
    ap.add_argument("--top", type=int, default=100)
    ap.add_argument("--label", default="reference")
    a = ap.parse_args()

    feats = {}
    for fn in sorted(os.listdir(a.feat_dir)):
        if fn.endswith(".json.gz"):
            d = load(os.path.join(a.feat_dir, fn))
            d["meta"] = parse_group(d["group"]) or {"group": d["group"], "mode": "ref", "model": d["group"]}
            feats[d["group"]] = d
    ref_groups = [feats[g] for g in a.ref_group]
    ai = [d for g, d in feats.items() if g not in a.ref_group
          and (a.ai_mode == "all" or d["meta"]["mode"] == a.ai_mode)]
    if not ai:
        raise SystemExit("žádné AI skupiny")
    os.makedirs(a.outdir, exist_ok=True)
    rep = [f"# F2 srovnání: AI ({a.ai_mode}, {len(ai)} skupin) proti {a.label}", ""]
    rep.append("Skupiny AI: " + ", ".join(sorted(d["group"] for d in ai)))
    rep.append("")

    exclude = ("<PROPN>", "<NUM>")
    if ref_groups:
        ref_lem = pool(ref_groups, "lemmas")
        ref_n = sum(g["counts"]["words"] for g in ref_groups)
    elif a.ref_csv:
        ref_lem = read_kontext_csv(a.ref_csv)
        ref_n = a.ref_tokens or sum(ref_lem.values())
    else:
        raise SystemExit("chybí reference")
    rep.append(f"Reference: {a.label}, {ref_n:,} slov".replace(",", " "))
    rep.append("")

    # 1) lemmata
    rows = keyness(ai, ref_lem, ref_n, "lemmas", a.min_freq, a.min_df, exclude)
    pos = {}
    for d in ai:
        for k, v in d["lemma_pos"].items():
            pos.setdefault(k, v)
    for r in rows:
        r["upos"] = pos.get(r["item"], "")
    over = sorted([r for r in rows if r["n_over"] > 0],
                  key=lambda r: (-r["n_over"], -r["lr_median"]))[: a.top]
    under = sorted([r for r in rows if r["n_under"] > 0],
                   key=lambda r: (-r["n_under"], r["lr_median"]))[: a.top]
    cols = ["item", "upos", "ai_ipm", "ref_ipm", "lr_pooled", "lr_median", "n_over", "n_under", "df_share"]
    hdr = ["lemma", "UPOS", "AI na mil.", "ref na mil.", "LR celkem", "LR medián", "modelů nad", "modelů pod", "podíl textů"]
    rep += ["## Nadreprezentovaná lemmata", "", md_table(over, cols, hdr), ""]
    rep += ["## Podreprezentovaná lemmata", "", md_table(under, cols, hdr), ""]
    with open(os.path.join(a.outdir, "lemmata.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols + ["g2_pooled", "n_models"])
        w.writeheader()
        for r in sorted(rows, key=lambda r: -r["lr_pooled"]):
            w.writerow({k: r.get(k) for k in cols + ["g2_pooled", "n_models"]})

    # 2) n-gramy a začátky vět (jen se skupinovou referencí)
    if ref_groups:
        for key, title in (("bigrams", "bigramy lemmat"), ("trigrams", "trigramy lemmat")):
            ref_c = pool(ref_groups, key)
            if not ref_c:
                continue
            nr = keyness(ai, ref_c, ref_n, key, max(20, a.min_freq // 2), 0, exclude)
            nr = sorted([r for r in nr if r["n_over"] > 0], key=lambda r: (-r["n_over"], -r["lr_median"]))[: a.top]
            rep += [f"## Nadreprezentované {title}", "",
                    md_table(nr, cols[:1] + cols[2:8], ["spojení"] + hdr[2:8]), ""]
        for k in ("0", "1", "2", "3"):
            if not any(g["starts"].get(k) for g in ref_groups):
                continue
            ai_s = [{"counts": {"words": g["counts"]["sents"], "docs": g["counts"]["docs"]},
                     "s": g["starts"].get(k, {})} for g in ai]
            ref_s = Counter()
            for g in ref_groups:
                ref_s.update(g["starts"].get(k, {}))
            ref_sn = sum(g["counts"]["sents"] for g in ref_groups)
            sr = keyness(ai_s, ref_s, ref_sn, "s", 20, 0, ())
            sr = sorted([r for r in sr if r["n_over"] > 0], key=lambda r: (-r["n_over"], -r["lr_median"]))[:40]
            label = "první token věty podle lemmatu (jako <s>[] v KonTextu)" if k == "0" else f"prvních {k} slov"
            rep += [f"## Začátky vět, {label} (na milion vět)", "",
                    md_table(sr, cols[:1] + cols[2:8], ["začátek"] + hdr[2:8]), ""]

    # 3) gramatické rysy
    ref_rates = {}
    if ref_groups:
        rc = Counter()
        for g in ref_groups:
            rc.update(g["counts"])
        ref_rates = feature_rates(rc)
        ref_sl = sd_from_hist(pool(ref_groups, "sent_len_hist"))
        ref_rates["sent_len_sd"] = ref_sl[1]
        ref_rates["sttr_lemma"] = sum(g["sttr_lemma"] or 0 for g in ref_groups) / len(ref_groups)
        ref_rates["sttr_noun100"] = sum(g["sttr_noun100"] or 0 for g in ref_groups) / len(ref_groups)
    if a.ref_features:
        ref_rates.update(json.load(open(a.ref_features, encoding="utf-8")))
    per_group = {}
    for g in ai:
        r = feature_rates(g["counts"])
        r["sent_len_sd"] = sd_from_hist(g["sent_len_hist"])[1]
        r["sttr_lemma"] = g["sttr_lemma"]
        r["sttr_noun100"] = g["sttr_noun100"]
        per_group[g["group"]] = r
    pc_all = Counter()
    for g in ai:
        pc_all.update(g["counts"])
    pooled_rates = feature_rates(pc_all)
    feat_names = sorted({k for r in per_group.values() for k in r})
    frows = []
    ai_docs = [d for g in ai for d in g["per_doc"].values()]
    ref_docs = [d for g in ref_groups for d in g["per_doc"].values()]
    for fname in feat_names:
        vals = [r.get(fname, 0) or 0 for r in per_group.values()
                if not (fname.startswith("sttr") and r.get(fname) is None)]
        vals_s = sorted(vals)
        refv = ref_rates.get(fname)
        row = {"feature": fname, "ai_median": vals_s[len(vals_s) // 2], "ai_min": vals_s[0], "ai_max": vals_s[-1],
               "ref": refv}
        if refv:
            row["ratio"] = row["ai_median"] / refv
            if fname in pooled_rates and pooled_rates[fname] is not None:
                row["ratio_pooled"] = pooled_rates[fname] / refv
            row["n_above"] = sum(1 for v in vals if v > refv)
            row["n_models"] = len(vals)
            if ref_docs and not fname.startswith(("lem:", "start_conn:")) and fname not in (
                    "words_per_sent", "sent_len_sd", "sttr_lemma", "sttr_noun100"):
                lo, hi = bootstrap_ratio(ai_docs, ref_docs, fname, bool(SENT_LEVEL.match(fname)))
                row["ci"] = f"{fmt(lo)}–{fmt(hi)}" if lo else None
        frows.append(row)
    rep += ["## Gramatické a postojové rysy",
            "", "Token-level rysy na 1 000 slov, větné (start_, question, adj_, contrast_, sent_) na 100 vět. "
            "Poměr (medián) = medián modelů / reference. Poměr (sloučeně) = všechny AI texty dohromady / reference, k němu 95% bootstrap interval po dokumentech.", "",
            md_table(frows, ["feature", "ai_median", "ai_min", "ai_max", "ref", "ratio", "ratio_pooled", "ci", "n_above", "n_models"],
                     ["rys", "AI medián", "AI min", "AI max", "reference", "poměr (medián)", "poměr (sloučeně)", "95% IS sloučeně", "modelů nad", "modelů"]), ""]
    with open(os.path.join(a.outdir, "rysy_po_modelech.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        groups = sorted(per_group)
        w.writerow(["rys", "reference"] + groups)
        for fname in feat_names:
            w.writerow([fname, ref_rates.get(fname)] + [per_group[g].get(fname) for g in groups])

    # 4) slova.md
    ph_ai = pool(ai, "phrases")
    if ph_ai or ref_groups:
        ph_ref = pool(ref_groups, "phrases") if ref_groups else Counter()
        ai_n = sum(g["counts"]["words"] for g in ai)
        prow = []
        pids = sorted(set(ph_ai) | set(ph_ref))
        if ref_groups and all(not g["per_doc"] for g in ref_groups):
            pids = [p for p in pids if p in ph_ref]  # KonText reference má jen jednoslovné položky
        for pid in pids:
            per = [lr(g["phrases"].get(pid, 0), g["counts"]["words"], ph_ref.get(pid, 0), ref_n) for g in ai]
            prow.append({"item": pid, "ai_ipm": ph_ai.get(pid, 0) / ai_n * 1e6,
                         "ref_ipm": ph_ref.get(pid, 0) / ref_n * 1e6 if ref_groups else None,
                         "ai_n": ph_ai.get(pid, 0), "ref_n": ph_ref.get(pid, 0),
                         "lr_pooled": lr(ph_ai.get(pid, 0), ai_n, ph_ref.get(pid, 0), ref_n) if ref_groups else None,
                         "g2_pooled": g2(ph_ai.get(pid, 0), ai_n, ph_ref.get(pid, 0), ref_n) if ref_groups else None,
                         "n_over": sum(1 for x in per if x >= 1) if ref_groups else None})
        with open(os.path.join(a.outdir, "slova_md.csv"), "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(prow[0].keys()) if prow else ["item"])
            w.writeheader()
            w.writerows(prow)

    with open(os.path.join(a.outdir, "report.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(rep))
    print("hotovo:", a.outdir, file=sys.stderr)


if __name__ == "__main__":
    main()
