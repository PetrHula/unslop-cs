#!/usr/bin/env python3
"""Rysy F0 a skóre AI-ovosti (krok 5 PLAN.md, hlavní metrika).

F0 je slepá k pravidlům srovnávaných skillů: četnosti funkčních slov (seznam zmrazený
z lidské reference KonText, `funkcni_slova.json`), podíly slovních druhů (UPOS) a dvojic
slovních druhů, délka vět (průměr, směrodatná odchylka), délka slov, STTR po 100 slovech,
interpunkce na 1000 slov. Nic ze `slova.md`, `vzorce.md` ani `metriky.py`.

Text se zpracuje modelem UDPipe (tokenizace a značkování, bez syntaxe); CoNLL-U se ukládá
do mezipaměti podle sha256 textu.

Podpříkazy:
  funkcni KONTEXT_CSV            zmrazí seznam funkčních slov do funkcni_slova.json
  trenuj  --konfigurace K        natrénuje logistickou regresi na dev sadě (lidské × AI),
                                 vypíše AUC křížové validace po vrstvách, uloží model
                                 do DATA/modely/ai_skore.json
"""
import argparse
import collections
import csv
import hashlib
import json
import os
import random
import re
import statistics
import sys

KOREN = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(KOREN), "koditex"))
from common import unify_lemma  # noqa: E402

UPOS = ["ADJ", "ADP", "ADV", "AUX", "CCONJ", "DET", "INTJ", "NOUN", "NUM", "PART", "PRON", "PROPN",
        "PUNCT", "SCONJ", "SYM", "VERB", "X"]
INTERPUNKCE = {"carka": ",", "tecka": ".", "strednik": ";", "dvojtecka": ":", "otaznik": "?",
               "vykricnik": "!", "pomlcka": "–", "dlouha_pomlcka": "—", "zavorka": "(", "uvozovky": "„",
               "tri_tecky": "…"}
FUNKCNI_P = os.path.join(KOREN, "funkcni_slova.json")
TRIDY_FUNKCNICH = "JRPT"  # spojky, předložky, zájmena, částice (poziční značka PDT)


# ---------------------------------------------------------------------------
# UDPipe

class Analyzator:
    def __init__(self, model_cesta, cache_dir):
        from ufal.udpipe import Model, Pipeline  # noqa: PLC0415
        self.model = Model.load(model_cesta)
        if not self.model:
            raise SystemExit(f"Nelze načíst model UDPipe: {model_cesta}")
        self.pipeline = Pipeline(self.model, "tokenize", Pipeline.DEFAULT, Pipeline.NONE, "conllu")
        self.cache = cache_dir
        os.makedirs(cache_dir, exist_ok=True)

    def vety(self, text):
        """Vrátí seznam vět; věta = seznam (form, lemma, upos)."""
        h = hashlib.sha256(text.encode("utf-8")).hexdigest()
        p = os.path.join(self.cache, h + ".conllu")
        if os.path.exists(p):
            conllu = open(p, encoding="utf-8").read()
        else:
            conllu = self.pipeline.process(text)
            with open(p, "w", encoding="utf-8", newline="\n") as f:
                f.write(conllu)
        vety, veta = [], []
        for line in conllu.split("\n"):
            if not line:
                if veta:
                    vety.append(veta)
                veta = []
            elif not line.startswith("#"):
                c = line.split("\t")
                if len(c) == 10 and c[0].isdigit():
                    veta.append((c[1], unify_lemma(c[2]).lower(), c[3]))
        if veta:
            vety.append(veta)
        return vety


# ---------------------------------------------------------------------------
# Rysy F0

def je_slovo(tok):
    return tok[2] not in ("PUNCT", "SYM") and re.search(r"\w", tok[0])


def rysy_f0(vety, funkcni, bigramy):
    toks = [t for v in vety for t in v]
    slova = [t for t in toks if je_slovo(t)]
    n = max(1, len(slova))
    r = {}
    lem = collections.Counter(t[1] for t in slova)
    for f in funkcni:
        r[f"fw:{f}"] = 1000 * lem[f] / n
    up = collections.Counter(t[2] for t in toks)
    for u in UPOS:
        r[f"upos:{u}"] = up[u] / max(1, len(toks))
    bg = collections.Counter((a[2], b[2]) for v in vety for a, b in zip(v, v[1:]))
    nbg = max(1, sum(bg.values()))
    for a, b in bigramy:
        r[f"bigram:{a}_{b}"] = bg[(a, b)] / nbg
    delky = [sum(1 for t in v if je_slovo(t)) for v in vety]
    delky = [d for d in delky if d] or [0]
    r["veta:prumer"] = statistics.mean(delky)
    r["veta:sd"] = statistics.pstdev(delky)
    r["slovo:delka"] = statistics.mean(len(t[0]) for t in slova) if slova else 0.0
    okna = [slova[i:i + 100] for i in range(0, len(slova) - 99, 100)]
    r["sttr100"] = statistics.mean(len({t[1] for t in o}) / 100 for o in okna) if okna else \
        len({t[1] for t in slova}) / n
    formy = collections.Counter(t[0] for t in toks)
    for k, z in INTERPUNKCE.items():
        r[f"interp:{k}"] = 1000 * formy[z] / n
    return r


def funkcni_z_kontextu(csv_cesta, pocet=100):
    c = collections.Counter()
    with open(csv_cesta, encoding="utf-8") as f:
        rd = csv.reader(f, delimiter=";")
        next(rd)
        for row in rd:
            if len(row) < 4:
                continue
            lemma, tag, freq = row[1], row[2], int(row[3])
            if tag[:1] in TRIDY_FUNKCNICH or unify_lemma(lemma) == "být":
                lemma = unify_lemma(lemma).lower()
                if re.fullmatch(r"\w+", lemma):
                    c[lemma] += freq
    return [l for l, _ in c.most_common(pocet)]


# ---------------------------------------------------------------------------
# Logistická regrese (numpy) a AUC

def auc(skore, y):
    """AUC = pravděpodobnost, že náhodný AI text má vyšší skóre než náhodný lidský."""
    pos = [s for s, t in zip(skore, y) if t == 1]
    neg = [s for s, t in zip(skore, y) if t == 0]
    if not pos or not neg:
        return None
    vyhry = sum((p > q) + 0.5 * (p == q) for p in pos for q in neg)
    return vyhry / (len(pos) * len(neg))


def trenuj_lr(X, y, l2=1.0, iteraci=3000, krok=0.1):
    """Vyvážené váhy tříd, standardizace, gradientní sestup. Vrátí model jako dict."""
    import numpy as np  # noqa: PLC0415
    X = np.asarray(X, dtype=float)
    y = np.asarray(y, dtype=float)
    mu, sd = X.mean(0), X.std(0)
    sd[sd == 0] = 1.0
    Z = (X - mu) / sd
    w_tridy = np.where(y == 1, 0.5 / max(1, y.sum()), 0.5 / max(1, (1 - y).sum()))
    w, b = np.zeros(Z.shape[1]), 0.0
    for _ in range(iteraci):
        p = 1 / (1 + np.exp(-(Z @ w + b)))
        g = p - y
        w -= krok * (Z.T @ (w_tridy * g) + l2 * w / len(y))
        b -= krok * float((w_tridy * g).sum())
    return {"mu": mu.tolist(), "sd": sd.tolist(), "w": w.tolist(), "b": b, "l2": l2}


def predikuj(model, X):
    import numpy as np  # noqa: PLC0415
    Z = (np.asarray(X, dtype=float) - np.asarray(model["mu"])) / np.asarray(model["sd"])
    return (1 / (1 + np.exp(-(Z @ np.asarray(model["w"]) + model["b"])))).tolist()


# ---------------------------------------------------------------------------
# Data dev sady

def dev_texty(data):
    """Vrátí seznam záznamů {soubor, text, y, vrstva, shluk, puvod} z DATA/dev/."""
    manifest = {z["id"]: z for z in json.load(open(os.path.join(data, "manifest.json"),
                                                   encoding="utf-8"))["texty"]}
    out = []
    koren = os.path.join(data, "dev")
    for dirpath, _, soubory in os.walk(koren):
        for f in soubory:
            if not f.endswith(".txt"):
                continue
            rel = os.path.relpath(os.path.join(dirpath, f), koren).replace(os.sep, "/")
            id_ = f[:-4]
            if rel.startswith("texty/"):
                z = manifest[id_]
                out.append({"soubor": rel, "y": 0, "vrstva": z["vrstva"], "shluk": z["dilo"], "puvod": "člověk"})
            elif rel.startswith("ai/aikoditex/"):
                out.append({"soubor": rel, "y": 1, "vrstva": "aikoditex", "shluk": f"aikoditex:{id_}",
                            "puvod": rel.split("/")[2]})
            elif rel.startswith("ai/"):
                _, metoda, model, _ = rel.split("/")
                z = manifest[id_]
                out.append({"soubor": rel, "y": 1, "vrstva": z["vrstva"], "shluk": z["dilo"],
                            "puvod": f"{metoda}/{model}"})
    for z in out:
        z["text"] = open(os.path.join(koren, z["soubor"]), encoding="utf-8").read()
    return out


def bigramy_z(vety_seznam, pocet=40):
    c = collections.Counter((a[2], b[2]) for vety in vety_seznam for v in vety for a, b in zip(v, v[1:]))
    return [list(k) for k, _ in c.most_common(pocet)]


def cmd_trenuj(a):
    cfg = json.load(open(a.konfigurace, encoding="utf-8"))
    data = os.path.expanduser(cfg["data"])
    an = Analyzator(os.path.expanduser(cfg["udpipe"]), os.path.join(data, "cache_udpipe"))
    funkcni = json.load(open(FUNKCNI_P, encoding="utf-8"))["lemmata"]
    zaznamy = dev_texty(data)
    for z in zaznamy:
        z["vety"] = an.vety(z["text"])
    bigramy = bigramy_z([z["vety"] for z in zaznamy])
    nazvy = None
    X, y = [], []
    for z in zaznamy:
        r = rysy_f0(z["vety"], funkcni, bigramy)
        nazvy = nazvy or sorted(r)
        X.append([r[k] for k in nazvy])
        y.append(z["y"])

    # křížová validace po shlucích (5 skupin)
    rnd = random.Random(f"{cfg['seed']}:cv")
    shluky = sorted({z["shluk"] for z in zaznamy})
    rnd.shuffle(shluky)
    skupina = {s: i % 5 for i, s in enumerate(shluky)}
    cv = [None] * len(zaznamy)
    for k in range(5):
        tr = [i for i, z in enumerate(zaznamy) if skupina[z["shluk"]] != k]
        te = [i for i, z in enumerate(zaznamy) if skupina[z["shluk"]] == k]
        m = trenuj_lr([X[i] for i in tr], [y[i] for i in tr])
        for i, p in zip(te, predikuj(m, [X[i] for i in te])):
            cv[i] = p
    vysledky = {"celkem": auc(cv, y)}
    lidske = [i for i, z in enumerate(zaznamy) if z["y"] == 0]
    for vrstva in sorted({z["vrstva"] for z in zaznamy}):
        idx = [i for i, z in enumerate(zaznamy) if z["vrstva"] == vrstva]
        if vrstva == "aikoditex":  # bez páru: proti všem lidským
            idx = idx + lidske
        vysledky[vrstva] = auc([cv[i] for i in idx], [y[i] for i in idx])
    for puvod in sorted({z["puvod"] for z in zaznamy if z["y"] == 1}):
        idx = [i for i, z in enumerate(zaznamy) if z["puvod"] == puvod] + lidske
        vysledky[f"puvod:{puvod}"] = auc([cv[i] for i in idx], [y[i] for i in idx])

    model = trenuj_lr(X, y)
    model.update(rysy=nazvy, funkcni=funkcni, bigramy=bigramy, auc_cv=vysledky,
                 pocet={"lidske": y.count(0), "ai": y.count(1)}, sada="dev")
    os.makedirs(os.path.join(data, "modely"), exist_ok=True)
    with open(os.path.join(data, "modely", "ai_skore.json"), "w", encoding="utf-8") as f:
        json.dump(model, f, ensure_ascii=False)
    vahy = sorted(zip(nazvy, model["w"]), key=lambda x: -abs(x[1]))[:15]
    print(json.dumps({"auc_cv": {k: (round(v, 3) if v is not None else None) for k, v in vysledky.items()},
                      "pocet": model["pocet"], "nejvetsi_vahy": [(n, round(w, 3)) for n, w in vahy]},
                     ensure_ascii=False, indent=1))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    f = sub.add_parser("funkcni")
    f.add_argument("kontext_csv")
    f.add_argument("--pocet", type=int, default=100)
    t = sub.add_parser("trenuj")
    t.add_argument("--konfigurace", required=True)
    a = ap.parse_args()
    if a.cmd == "funkcni":
        lemmata = funkcni_z_kontextu(a.kontext_csv, a.pocet)
        with open(FUNKCNI_P, "w", encoding="utf-8", newline="\n") as fh:
            json.dump({"popis": "Funkční slova pro rysy F0: nejčastější lemmata spojek, předložek, zájmen "
                                "a částic (+ být) v lidském Koditexu (KonText, psané originály).",
                       "zdroj": "~/unslop-cs-data/korpusy/kontext/A_lemma_tag_freq.csv",
                       "lemmata": lemmata}, fh, ensure_ascii=False, indent=1)
        print(len(lemmata), lemmata[:30])
    else:
        cmd_trenuj(a)


if __name__ == "__main__":
    main()
