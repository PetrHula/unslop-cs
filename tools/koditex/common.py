"""Společné funkce pro analýzu AI-Koditexu (F2, unslop-cs 1.1).

Skripty nečtou síť a nepotřebují nic mimo standardní knihovnu a ufal.udpipe.
Data ani model UDPipe do repozitáře nepatří (licence CC BY-NC-SA).
"""
import re

# koditex_chat_claude-3-opus__0, koditex_complete_davinci-002__100,
# koditex_chat_gpt-35-turbo_default-system__100 (případně s jedním podtržítkem)
GROUP_RE = re.compile(r"^koditex_(chat|complete)_(.+?)(_default-system)?_{1,2}(\d+)$")


def parse_group(name):
    """Z názvu složky vrátí slovník mode, model, temp, default_system. None, když nesedí."""
    m = GROUP_RE.match(name)
    if not m:
        return None
    mode, model, ds, temp = m.groups()
    return {
        "group": name,
        "mode": mode,
        "model": model + ("+default-system" if ds else ""),
        "temp": int(temp) / 100,
        "default_system": bool(ds),
    }


def model_family(model):
    for fam in ("claude", "gpt", "o3", "davinci", "gemini", "llama", "deep-seek"):
        if model.startswith(fam):
            return {"o3": "gpt", "davinci": "gpt"}.get(fam, fam)
    return "other"


def read_conllu(path):
    """Generátor vět: (comments, tokens). Token = dict se základními sloupci.
    Víceslovné tokeny (1-2) a prázdné uzly (1.1) přeskakuje."""
    comments, toks = [], []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line:
                if toks:
                    yield comments, toks
                comments, toks = [], []
                continue
            if line.startswith("#"):
                comments.append(line)
                continue
            cols = line.split("\t")
            if len(cols) != 10 or "-" in cols[0] or "." in cols[0]:
                continue
            feats = {}
            if cols[5] != "_":
                for kv in cols[5].split("|"):
                    if "=" in kv:
                        k, v = kv.split("=", 1)
                        feats[k] = v
            toks.append({
                "id": int(cols[0]), "form": cols[1], "lemma": cols[2], "upos": cols[3], "xpos": cols[4],
                "feats": feats, "head": int(cols[6]) if cols[6].isdigit() else 0,
                "deprel": cols[7], "misc": cols[9],
            })
    if toks:
        yield comments, toks


def is_word(t):
    return t["upos"] not in ("PUNCT", "SYM", "X") and any(ch.isalnum() for ch in t["form"])


def lex_lemma(t):
    """Lemma malými písmeny se záporem. UD lemmatizace PDT zápor odstraňuje
    (nezbytný → zbytný, neposlední → poslední) a nese ho jen v Polarity=Neg;
    pro slovník jde o jiná slova, proto se „ne“ vrací do lemmatu."""
    lem = t["lemma"].lower()
    form = t["form"].lower()
    if (t["feats"].get("Polarity") == "Neg" and form.startswith("ne")
            and not lem.startswith("ne") and t["upos"] in ("ADJ", "ADV", "NOUN", "VERB")):
        lem = "ne" + lem
    if t["feats"].get("Degree") == "Sup" and form.startswith("nej") and t["upos"] in ("ADJ", "ADV"):
        lem = "nej" + lem
    return lem


def norm_lemma(t):
    """lex_lemma; vlastní jména a čísla jako zástupné značky."""
    if t["upos"] == "PROPN":
        return "<PROPN>"
    if t["upos"] == "NUM" and any(ch.isdigit() for ch in t["form"]):
        return "<NUM>"
    return lex_lemma(t)


# --- Definice přes poziční značky PDT -------------------------------------
# Stejné definice se počítají na AI straně (XPOS z UDPipe) i z exportů KonTextu,
# aby se srovnávaly stejně definované rysy. Pozice: 1 druh, 2 poddruh, 3 rod,
# 4 číslo, 5 pád, 8 osoba, 9 čas, 11 zápor, 12 slovesný rod.

def pdt_is_word(tag, lemma):
    return bool(tag) and tag[0] != "Z" and any(ch.isalnum() for ch in lemma)


def pdt_lex_lemma(lemma, tag, form=""):
    lem = lemma.lower()
    if len(tag) >= 11 and tag[10] == "N" and tag[0] in "ADNV" and not lem.startswith("ne") and lem != "být":
        if not form or form.lower().startswith("ne"):
            lem = "ne" + lem
    if len(tag) >= 10 and tag[9] == "3" and tag[0] in "AD":
        lem = "nej" + lem
    return lem


def pdt_norm_lemma(lemma, tag, form=""):
    if tag[:1] == "N" and lemma[:1].isupper():
        return "<PROPN>"
    if tag[:2] == "C=":
        return "<NUM>"
    return pdt_lex_lemma(lemma, tag, form)


VNOUN_STOP = {"století", "náměstí", "štěstí", "neštěstí", "pondělí", "příští", "předměstí", "území",
              "zátiší", "pobřeží", "podnebí", "počasí", "dědictví", "bohatství", "zdraví", "koření",
              "kamení", "listí", "uhlí", "dříví", "přízemí", "podkroví", "nádraží", "zboží", "umění",
              "znamení", "vědomí", "svědomí", "jmění", "výročí", "povodí", "rozhraní", "prostředí"}


def vnoun_lemma(lemma):
    lem = lemma.lower()
    return ((lem.endswith("ní") or lem.endswith("tí")) and len(lem) > 4
            and not lem.endswith(("ství", "stí", "ctví", "letí")) and lem not in VNOUN_STOP)


def pdt_tag_features(tag, c, n=1):
    """Přičte do Counteru c rysy odvozené ze značky (n = četnost)."""
    if len(tag) < 12:
        return
    pos, sub, person, tense = tag[0], tag[1], tag[7], tag[8]
    c["kx_" + pos] += n
    if pos == "V":
        if sub == "s":
            c["kx_pass_periph"] += n
        if sub in "em":
            c["kx_conv"] += n
        if sub == "p":
            c["kx_past"] += n
        if sub == "i":
            c["kx_imp"] += n
        if tense == "F":
            c["kx_fut"] += n
        if sub == "B" and tense == "P":
            c["kx_pres"] += n
        if person == "1":
            c["kx_p1_verb"] += n
        if person == "2":
            c["kx_p2_verb"] += n
    if pos == "P" and person == "2":
        c["kx_p2_pron"] += n
    if pos == "P" and person == "1":
        c["kx_p1_pron"] += n
