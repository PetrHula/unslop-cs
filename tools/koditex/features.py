"""Spočítá četnosti a gramatické rysy pro každou skupinu (model × teplota).

Vstup: složka s podsložkami po skupinách a soubory *.conllu (výstup parse.py)
nebo jedna skupina lidské reference zpracovaná stejným modelem.
Výstup: OUTDIR/<skupina>.json.gz

Použití:
  python3 -I features.py CONLLU_DIR OUTDIR [--phrases slova_lemmata.json] [--min-ngram 3]

Úplně první věta souboru (fragment po promptu) se vynechává.
"""
import argparse
import gzip
import json
import os
import re
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import (is_word, lex_lemma, norm_lemma, pdt_is_word, pdt_tag_features,  # noqa: E402
                    read_conllu, vnoun_lemma)

# --- seznamy pro hypotézy (H1–H13 z F1) ---------------------------------------

# spojovací výrazy na začátku věty (H1, jev zvlášť od rysů D3), jako sekvence lemmat
START_CONNECTIVES = [
    "navíc", "zároveň", "kromě ten", "nicméně", "tudíž", "dále", "proto", "díky ten",
    "v neposlední řada", "celkově", "tedy", "také", "rovněž", "současně", "přitom",
    "naopak", "avšak", "ovšem", "konečně", "závěrem", "stejně tak", "v neposlední",
    "ačkoli", "i když", "a", "ale", "pak", "potom", "tak", "takže",
]
START_CONNECTIVES = [tuple(x.split()) for x in START_CONNECTIVES]

PARTICLES = {
    # H6 – postoj (D8): oslabující, zesilující, restriktory, modální a členicí
    "hedge": ["snad", "asi", "možná", "zřejmě", "patrně", "nejspíš", "nejspíše", "pravděpodobně", "údajně"],
    "booster": ["zcela", "naprosto", "opravdu", "skutečně", "velmi", "absolutně", "rozhodně", "nesmírně",
                "mimořádně", "extrémně", "obzvlášť", "obzvláště", "zvlášť", "velice"],
    "restrictor": ["jen", "pouze", "jenom", "výhradně", "právě"],
    "modal": ["přece", "vždyť", "prý", "totiž", "vlastně", "no", "copak", "ostatně", "beztak",
              "stejně", "aspoň", "alespoň", "hlavně", "teda"],
}

OPIS_JE = ["představovat", "sloužit", "fungovat", "vyznačovat", "disponovat", "pyšnit", "nabízet"]
OUTLOOK = ["budoucnost", "budoucí", "umožnit", "umožňovat", "otevírat", "otevřít", "potenciál",
           "perspektiva", "výhled", "nadcházející", "příležitost", "směřovat", "rozvoj", "vývoj"]
KALKY = ["adresovat", "báze", "realizovat", "zrealizovat", "eventuálně", "aktuálně", "doručit",
         "sdílet", "dedikovaný", "kompetitivní"]

# Model UD 2.5 (czech-pdt-ud-2.5-191206) VerbForm=Vnoun nezná, slovesná substantiva
# jsou prostý NOUN. Heuristika (common.vnoun_lemma): středorodé NOUN na -ní/-tí bez výjimek.
def is_vnoun_heur(t):
    return t["upos"] == "NOUN" and t["feats"].get("Gender") == "Neut" and vnoun_lemma(t["lemma"])


RE_NEJDE = re.compile(r"\bne(jde|šlo|půjde|jedná se|jednalo se) o\b")
RE_NENI_TO = re.compile(r"\bne(ní|bylo|bude|byl|byla) to\b")


def children_index(toks):
    ch = defaultdict(list)
    for t in toks:
        ch[t["head"]].append(t)
    return ch


def sentence_features(toks, c, starts, sent_lens):
    words = [t for t in toks if is_word(t)]
    n = len(words)
    if n == 0:
        return
    c["words"] += n
    c["sents"] += 1
    sent_lens[min(n, 120)] += 1
    if n <= 8:
        c["sent_short_le8"] += 1
    if n >= 25:
        c["sent_long_ge25"] += 1

    ch = children_index(toks)
    forms_l = [t["form"].lower() for t in toks]
    text_l = " ".join(forms_l)

    # začátky vět
    first = [t for t in toks if is_word(t)][:3]
    for k in (1, 2, 3):
        if len(first) >= k:
            starts[k][" ".join(t["form"].lower() for t in first[:k])] += 1
    f0 = first[0]
    if f0["upos"] == "PRON" and f0["feats"].get("PronType") == "Prs":
        c["start_prs_pron"] += 1
    if f0["upos"] in ("DET", "PRON") and f0["feats"].get("PronType") == "Dem":
        c["start_dem"] += 1
        if f0["form"].lower() != "to":
            c["start_dem_no_to"] += 1
    lem_first = tuple(t["lemma"].lower() for t in first)
    for seq in START_CONNECTIVES:
        if lem_first[: len(seq)] == seq:
            c["start_conn"] += 1 if seq not in (("a",), ("ale",), ("pak",), ("potom",), ("tak",), ("takže",)) else 0
            c["start_conn:" + " ".join(seq)] += 1
            break

    if toks[-1]["form"] == "?":
        c["question"] += 1
    if toks[-1]["form"] == "!":
        c["exclam"] += 1

    if RE_NEJDE.search(text_l):
        c["contrast_nejde_o"] += 1
    if RE_NENI_TO.search(text_l):
        c["contrast_neni_to"] += 1

    # --- rysy definované stejně jako dotazy v KonTextu (značky PDT) ---
    for i, t in enumerate(toks):
        tag, lem_raw = t.get("xpos", ""), t["lemma"]
        if pdt_is_word(tag, lem_raw):
            c["kx_words"] += 1
            pdt_tag_features(tag, c)
            if tag.startswith("NNN") and vnoun_lemma(lem_raw):
                c["kx_vnoun"] += 1
        if t["form"] == "?":
            c["kx_qmark"] += 1
        if t["form"] == "," and i + 1 < len(toks):
            nx = forms_l[i + 1]
            if nx == "což":
                c["kx_coz"] += 1
            if nx == "čímž":
                c["kx_cimz"] += 1
        if (t["lemma"].lower() == "být" and i + 3 < len(toks) and toks[i + 1].get("xpos", "")[:1] == "A"
                and toks[i + 2]["form"] == "," and forms_l[i + 3] in ("že", "aby")):
            c["kx_byt_adj_ze"] += 1
        if (t["lemma"].lower() in ("ten", "tento", "takový") and i + 2 < len(toks) and toks[i + 1]["form"] == ","
                and toks[i + 2]["lemma"].lower() in ("co", "kdo", "který", "jenž", "aby", "že", "jak", "kde", "kdy")):
            c["kx_korel"] += 1
    starts[0][toks[0]["lemma"].lower()] += 1

    for i, t in enumerate(toks):
        f, lem, up, ft, dr = t["form"], t["lemma"].lower(), t["upos"], t["feats"], t["deprel"]
        fl = f.lower()
        # typografie
        if f == "—":
            c["emdash"] += 1
        elif f == "–":
            c["endash"] += 1
        elif f == '"':
            c["straight_quote"] += 1
        elif f in ("„", "“"):
            c["cz_quote"] += 1
        # přívěsky
        if f == "," and i + 1 < len(toks):
            nx = forms_l[i + 1]
            if nx == "což":
                c["adj_coz"] += 1
            elif nx == "čímž":
                c["adj_cimz"] += 1
            elif nx == "a" and i + 2 < len(toks) and forms_l[i + 2] == "tím":
                c["adj_a_tim"] += 1
        if not is_word(t):
            continue
        # jmenný styl a pasivum (H4)
        if ft.get("VerbForm") == "Vnoun" or is_vnoun_heur(t):
            c["vnoun"] += 1
            c["vn:" + lem] += 1
        if ft.get("Voice") == "Pass" and ft.get("VerbForm") == "Part":
            c["pass_periph"] += 1
        if dr == "expl:pass":
            c["pass_refl"] += 1
        if ft.get("VerbForm") == "Conv":
            c["conv"] += 1
        # čas, osoba, způsob (H3, H5)
        if up in ("VERB", "AUX"):
            tense, vf = ft.get("Tense"), ft.get("VerbForm")
            if tense == "Fut":
                c["fut"] += 1
            elif tense == "Pres" and vf == "Fin":
                c["pres"] += 1
            elif tense == "Past" and vf == "Part" and ft.get("Voice") == "Act":
                c["past"] += 1
            if ft.get("Mood") == "Imp":
                c["imp"] += 1
            if ft.get("Person") == "1":
                c["p1_verb"] += 1
            elif ft.get("Person") == "2":
                c["p2_verb"] += 1
        if up == "PRON" and ft.get("PronType") == "Prs":
            if ft.get("Person") == "2":
                c["p2_pron"] += 1
            elif ft.get("Person") == "1":
                c["p1_pron"] += 1
        # konkrétnost (H2)
        if up == "PROPN":
            c["propn"] += 1
        if up == "NUM":
            c["num"] += 1
        if up == "ADJ":
            c["adj"] += 1
        if up == "NOUN":
            c["noun"] += 1
        if up == "VERB":
            c["verb"] += 1
        if dr == "conj":
            c["conj"] += 1
        conjs = [x for x in ch.get(t["id"], []) if x["deprel"] == "conj"]
        if len(conjs) >= 2:
            c["coord3plus"] += 1
            if len(conjs) == 2:
                c["coord3"] += 1
            if all(x["upos"] == up for x in conjs):
                c["coord3plus_same_pos"] += 1
        # soudržnost D3 (H1)
        if lem == "který" and ft.get("PronType") in ("Rel", "Int,Rel", None):
            c["ktery"] += 1
        if lem == "jenž":
            c["jenz"] += 1
        if ft.get("Poss") == "Yes" and ft.get("PronType") == "Prs":
            c["poss_pron"] += 1
            if lem == "svůj":
                c["svuj"] += 1
        if up in ("PRON", "DET") and ft.get("PronType") == "Dem" and i + 2 < len(toks) and toks[i + 1]["form"] == ",":
            nx = toks[i + 2]
            if nx["feats"].get("PronType") in ("Rel", "Int,Rel") or nx["upos"] == "SCONJ":
                c["korelativ"] += 1
        # „je + ADJ + že/aby“ (H3, D7)
        if up == "ADJ":
            kids = ch.get(t["id"], [])
            if any(k["deprel"] == "cop" for k in kids):
                c["adj_pred"] += 1
                for k in kids:
                    if k["deprel"] in ("csubj", "ccomp"):
                        marks = [m["lemma"].lower() for m in ch.get(k["id"], []) if m["deprel"] == "mark"]
                        if "že" in marks or "aby" in marks:
                            c["je_adj_ze_aby"] += 1
                            break
        if lem == "být" and dr == "cop":
            c["cop_byt"] += 1
        # postoj (H6)
        for grp, lst in PARTICLES.items():
            if lem in lst:
                c["part_" + grp] += 1
                c["lem:" + lem] += 1
        if up == "PART":
            c["part_upos"] += 1
        if up == "ADV":
            c["adv"] += 1
        # opisy pro je/má (H10), výhled (H3), kalky (H8)
        if lem in OPIS_JE:
            c["opis_je"] += 1
            c["lem:" + lem] += 1
        if lem in ("být", "mít"):
            c["lem:" + lem] += 1
        if lem in OUTLOOK:
            c["outlook"] += 1
            c["lem:" + lem] += 1
        if lem in KALKY:
            c["lem:" + lem] += 1
        if lem == "nejen" or fl == "nejen":
            c["nejen"] += 1


def sttr(lemmas, win=1000):
    vals = []
    for s in range(0, len(lemmas) - win + 1, win):
        w = lemmas[s:s + win]
        vals.append(len(set(w)) / win)
    return vals


def match_phrases(lems, phrases_by_first, pc):
    for i, l in enumerate(lems):
        for pid, seq in phrases_by_first.get(l, ()):
            if tuple(lems[i:i + len(seq)]) == seq:
                pc[pid] += 1


def process_group(gdir, phrases, min_ngram):
    c = Counter()
    lemma_c, lemma_df = Counter(), Counter()
    lemma_pos = defaultdict(Counter)
    bi, tri = Counter(), Counter()
    starts = {0: Counter(), 1: Counter(), 2: Counter(), 3: Counter()}
    sent_lens = Counter()
    pc, pdf = Counter(), Counter()
    sttr_all, sttr_noun = [], []
    per_doc = {}
    pfirst, ffirst = defaultdict(list), defaultdict(list)
    for p in phrases:
        seq = tuple(p["lemmas"])
        if seq:
            pfirst[seq[0]].append((p["id"], seq))
        fseq = tuple(p.get("forms") or ())
        if fseq:  # ustálené fráze se navíc počítají v přesném tvaru (klíč id#tvar)
            ffirst[fseq[0]].append((p["id"] + "#tvar", fseq))

    files = sorted(f for f in os.listdir(gdir) if f.endswith(".conllu"))
    for fn in files:
        dc = Counter()
        doc_lemmas, doc_nouns, doc_set = [], [], set()
        dpc = Counter()
        seen_sents = set()
        for comments, toks in read_conllu(os.path.join(gdir, fn)):
            if "# fragment = 1" in comments:
                continue
            # zacyklené výstupy (DeepSeek, Llama při T=0): opakovanou větu počítej jednou
            key = " ".join(t["form"].lower() for t in toks)
            if len(toks) > 3 and key in seen_sents:
                dc["dup_sents"] += 1
                continue
            seen_sents.add(key)
            sentence_features(toks, dc, starts, sent_lens)
            words = [t for t in toks if is_word(t)]
            lems = [norm_lemma(t) for t in words]
            for t, l in zip(words, lems):
                lemma_c[l] += 1
                lemma_pos[l][t["upos"]] += 1
                doc_set.add(l)
            doc_lemmas += lems
            doc_nouns += [l for t, l in zip(words, lems) if t["upos"] == "NOUN"]
            for k in range(len(lems) - 1):
                bi[(lems[k], lems[k + 1])] += 1
            for k in range(len(lems) - 2):
                tri[(lems[k], lems[k + 1], lems[k + 2])] += 1
            if pfirst:
                match_phrases([lex_lemma(t) for t in words], pfirst, dpc)
            if ffirst:
                match_phrases([t["form"].lower() for t in words], ffirst, dpc)
        for l in doc_set:
            lemma_df[l] += 1
        for pid in dpc:
            pdf[pid] += 1
        pc.update(dpc)
        sttr_all += sttr(doc_lemmas, 300)
        sttr_noun += sttr(doc_nouns, 100)
        c.update(dc)
        c["docs"] += 1
        per_doc[fn[:-7]] = {k: v for k, v in dc.items() if not k.startswith(("lem:", "vn:"))}

    prune = lambda cnt: {" ".join(k): v for k, v in cnt.items() if v >= min_ngram}  # noqa: E731
    return {
        "group": os.path.basename(gdir.rstrip("/")),
        "counts": dict(c),
        "lemmas": dict(lemma_c),
        "lemma_df": dict(lemma_df),
        "lemma_pos": {l: pc_.most_common(1)[0][0] for l, pc_ in lemma_pos.items()},
        "bigrams": prune(bi),
        "trigrams": prune(tri),
        "starts": {k: {s: v for s, v in cnt.items() if v >= 2} for k, cnt in starts.items()},
        "sent_len_hist": dict(sent_lens),
        "sttr_lemma": sum(sttr_all) / len(sttr_all) if sttr_all else None,
        "sttr_noun100": sum(sttr_noun) / len(sttr_noun) if sttr_noun else None,
        "phrases": dict(pc),
        "phrases_df": dict(pdf),
        "per_doc": per_doc,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("conllu_dir")
    ap.add_argument("outdir")
    ap.add_argument("--phrases")
    ap.add_argument("--min-ngram", type=int, default=3)
    ap.add_argument("--only", help="zpracovat jen skupiny obsahující tento řetězec")
    a = ap.parse_args()
    phrases = json.load(open(a.phrases, encoding="utf-8")) if a.phrases else []
    os.makedirs(a.outdir, exist_ok=True)
    for g in sorted(os.listdir(a.conllu_dir)):
        gd = os.path.join(a.conllu_dir, g)
        if not os.path.isdir(gd) or (a.only and a.only not in g):
            continue
        res = process_group(gd, phrases, a.min_ngram)
        with gzip.open(os.path.join(a.outdir, g + ".json.gz"), "wt", encoding="utf-8") as f:
            json.dump(res, f, ensure_ascii=False)
        cc = res["counts"]
        print(f"{g}: docs {cc.get('docs')}, slov {cc.get('words')}, vět {cc.get('sents')}", file=sys.stderr)


if __name__ == "__main__":
    main()
