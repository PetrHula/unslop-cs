"""Společné funkce pro analýzu AI-Koditexu (F2).

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


# Sjednocení lemmatizace UDPipe (UD 2.5 / PDT) a KonTextu (Koditex, MorfFlex).
# Klíč i hodnota jsou lemmata malými písmeny; cíl je schéma PDT/UD.
LEMMA_UNIFY = {
    # zájmena: PDT slučuje množné tvary s jednotnými
    "my": "já", "vy": "ty", "oni": "on", "ono": "on", "náš": "můj", "váš": "tvůj",
    "její": "jeho", "jejich": "jeho",
    # stupňovaná a variantní příslovce
    "víc": "hodně", "více": "hodně", "méně": "málo", "míň": "málo",
    "spíš": "spíše", "nejspíš": "nejspíše", "dál": "dále", "taky": "také", "teda": "tedy",
    "trošku": "trochu", "kdyby": "když", "prostřednictví": "prostřednictvím",
    # varianty a chyby lemmatizace UDPipe
    "myslit": "myslet", "začnout": "začít", "datum": "data",
    # zkratky: ČNK je nechává, UD rozvádí
    "tzv": "takzvaný", "č": "číslo", "obr": "obrázek", "odst": "odstavec", "resp": "respektive",
    "sv": "svatý", "str": "strana", "viz": "vidět", "tj": "to", "např": "například",
}


def unify_lemma(lem):
    """Odstraní technické přípony PDT (m`metr, and_^(…)) a sjednotí varianty."""
    if "`" in lem:  # zkratka`plný tvar → plný tvar (jako ČNK: mm → milimetr)
        lem = lem.split("`")[1].split("_")[0] or lem.split("`")[0]
    if "_" in lem.strip("_"):
        lem = lem.strip("_").split("_")[0]
    if lem in ("„", "“", "”", "‚", "‘", "»", "«"):
        return '"'
    if lem.endswith("koliv"):
        lem = lem[:-1]
    return LEMMA_UNIFY.get(lem, lem)


def lex_lemma(t):
    """Lemma malými písmeny se záporem. UD lemmatizace PDT zápor odstraňuje
    (nezbytný → zbytný, neposlední → poslední) a nese ho jen v Polarity=Neg;
    pro slovník jde o jiná slova, proto se „ne“ vrací do lemmatu."""
    lem = unify_lemma(t["lemma"].lower())
    form = t["form"].lower()
    if (t["feats"].get("Polarity") == "Neg" and form.startswith("ne") and lem != "být"
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
    if t.get("xpos", "").startswith("Vs"):
        return "<VPASS>"  # krátká příčestí trpná: UD dává lemma přídavného jména, ČNK slovesa
    return lex_lemma(t)


# --- Definice přes poziční značky PDT -------------------------------------
# Stejné definice se počítají na AI straně (XPOS z UDPipe) i z exportů KonTextu,
# aby se srovnávaly stejně definované rysy. Pozice: 1 druh, 2 poddruh, 3 rod,
# 4 číslo, 5 pád, 8 osoba, 9 čas, 11 zápor, 12 slovesný rod.

def pdt_is_word(tag, lemma):
    return bool(tag) and tag[0] != "Z" and any(ch.isalnum() for ch in lemma)


# zvláštní lemmata Koditexu v KonTextu (pomocné „být“, kondicionálové „by“)
CNK_LEMMA_MAP = {"_být": "být", "_být**": "být", "_by": "být"}


def pdt_lex_lemma(lemma, tag, form=""):
    lem = unify_lemma(CNK_LEMMA_MAP.get(lemma, lemma).lower())
    grade = tag[9] if len(tag) >= 10 else "-"
    # ČNK lemmatizuje „dále“ jako 2. stupeň „daleko“ a „raději“ jako 2. stupeň „rád“, UD ne
    if lem == "daleko" and grade == "2":
        return "dále"
    if lem == "rád" and grade in "23" and tag[0] == "D":
        return "raději" if grade == "2" else "nejraději"
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
    if tag[:2] == "Vs":
        return "<VPASS>"
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
        # osoba jen u určitých tvarů: tagset ČNK dává osobu i příčestí minulému
        # („dělal jsem“ by se jinak počítalo dvakrát), PDT z UDPipe ne
        if sub not in "pfsem":
            if person == "1":
                c["kx_p1_verb"] += n
            if person == "2":
                c["kx_p2_verb"] += n
    if pos == "P" and person == "2":
        c["kx_p2_pron"] += n
    if pos == "P" and person == "1":
        c["kx_p1_pron"] += n
