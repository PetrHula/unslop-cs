"""Vytáhne položky ze `slova.md` a zlemmatizuje je stejným modelem jako korpus.

  python3 -I slova.py extract slova.md slova_polozky.json
  python3 -I slova.py lemmatize MODEL.udpipe slova_polozky.json slova_lemmata.json

Extrakce je heuristická (lomítka rozvine po slovech, závorky zahodí).
Výsledný seznam je potřeba jednou projít očima; ruční opravy jsou v
slova_opravy.json vedle skriptu (klíče platí pro slova.md 1.0.0) ve tvaru {"id": "nový text" | null}, null položku vyřadí.
"""
import itertools
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import lex_lemma  # noqa: E402

QUOTE_RE = re.compile(r"„([^“]+)“")
PAREN_RE = re.compile(r"\([^)]*\)")


def clean(s):
    s = PAREN_RE.sub("", s)
    s = s.replace("…", " ").replace("*", "")
    s = re.sub(r"[?!:.,]+$", "", s.strip())
    return re.sub(r"\s+", " ", s).strip()


def expand_slashes(s):
    """„posunout na další / novou úroveň“ → dvě varianty (střídá se jedno slovo)."""
    if "/" not in s:
        return [s]
    toks = s.replace(" / ", " / ").split()
    groups, i = [], 0
    while i < len(toks):
        if toks[i] == "/" and groups:
            i += 1
            if i < len(toks):
                groups[-1].append(toks[i])
        else:
            groups.append([toks[i]])
        i += 1
    return [" ".join(p) for p in itertools.product(*groups)]


def items_from_list(text):
    out = []
    text = PAREN_RE.sub("", text)
    for part in text.split(","):
        part = clean(part)
        if part and "X" not in part.split() and "Y" not in part.split():
            out += expand_slashes(part)
    return out


def extract(md):
    items, section, level = [], None, None
    lines = open(md, encoding="utf-8").read().split("\n")
    for line in lines:
        if line.startswith("## "):
            section = line[3:].strip()
            if section.startswith("Úroveň 1"):
                level = "U1"
            elif section.startswith("Úroveň 2"):
                level = "U2"
            elif section.startswith("Úroveň 3"):
                level = "U3"
            elif section.startswith("Kalky"):
                level = "KALK"
            elif section.startswith("Ustálené"):
                level = "FRAZE"
            elif section.startswith("Chatbotí"):
                level = "P0"
            else:
                level = None
            continue
        if level is None:
            continue
        cat = section
        if line.startswith("|") and level in ("U1", "KALK"):
            cells = [c.strip() for c in line.strip("|").split("|")]
            if not cells or cells[0] in ("Místo", "Kalk") or set(cells[0]) <= set("-"):
                continue
            for it in items_from_list(cells[0]):
                items.append((level, cat, it))
        elif level in ("U2", "U3") and line and not line.startswith("#"):
            for it in items_from_list(line):
                items.append((level, cat, it))
        elif level == "KALK" and line.startswith("**"):
            m = re.match(r"\*\*(.+?):\*\*(.*)", line)
            if not m:
                continue
            sub, rest = m.groups()
            if "Anglicismy" in sub:
                inner = re.search(r"\*(.+?)\*", rest)
                lst = inner.group(1) if inner else ""
            elif "stupňování" in sub:
                lst = ", ".join(QUOTE_RE.findall(rest))
            else:
                lst = rest.split(". ")[0]
            for it in items_from_list(lst):
                items.append(("KALK", sub, it))
        elif level in ("FRAZE", "P0"):
            m = re.match(r"\*\*(.+?):\*\*", line)
            sub = m.group(1) if m else cat
            for q in QUOTE_RE.findall(line):
                for it in expand_slashes(clean(q)):
                    if it:
                        items.append((level, sub, it))
    seen, out = set(), []
    for lvl, cat, it in items:
        key = (lvl, it.lower())
        if key in seen:
            continue
        seen.add(key)
        out.append({"id": f"{lvl}-{len(out) + 1:03d}", "level": lvl, "category": cat, "text": it})
    return out


def lemmatize(model_path, items):
    from ufal.udpipe import Model, Pipeline, ProcessingError
    m = Model.load(model_path)
    pipe = Pipeline(m, "tokenize", Pipeline.DEFAULT, Pipeline.NONE, "conllu")
    for it in items:
        err = ProcessingError()
        out = pipe.process(it["text"], err)
        lem = []
        for line in out.split("\n"):
            cols = line.split("\t")
            if len(cols) == 10 and cols[0].isdigit() and cols[3] not in ("PUNCT", "SYM"):
                feats = dict(kv.split("=", 1) for kv in cols[5].split("|") if "=" in kv)
                lem.append(lex_lemma({"lemma": cols[2], "form": cols[1], "upos": cols[3], "feats": feats}))
        it["lemmas"] = lem
        if it["level"] in ("FRAZE", "P0"):
            it["forms"] = [line.split("\t")[1].lower() for line in out.split("\n")
                           if len(line.split("\t")) == 10 and line.split("\t")[0].isdigit()
                           and line.split("\t")[3] not in ("PUNCT", "SYM")]
    return items


def main():
    cmd = sys.argv[1]
    if cmd == "extract":
        items = extract(sys.argv[2])
        fixes_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "slova_opravy.json")
        if os.path.exists(fixes_path):
            fixes = json.load(open(fixes_path, encoding="utf-8"))
            items = [dict(i, text=fixes[i["id"]]) if i["id"] in fixes and fixes[i["id"]] else i
                     for i in items if not (i["id"] in fixes and fixes[i["id"]] is None)]
        json.dump(items, open(sys.argv[3], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(f"položek: {len(items)}", file=sys.stderr)
    elif cmd == "lemmatize":
        items = json.load(open(sys.argv[3], encoding="utf-8"))
        json.dump(lemmatize(sys.argv[2], items), open(sys.argv[4], "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1)
    else:
        raise SystemExit(__doc__)


if __name__ == "__main__":
    main()
