#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
metriky.py – měřitelné kontroly AI slopu v českém textu (skill unslop-cs).

Skript počítá to, co jde spočítat: typografii, rytmus vět, nálezy ze seznamů
slov (`references/slova.md`), kontrastní obraty, trojice, přívěsky,
spojovací výrazy, osobu a částice a s modelem UDPipe i jmenný styl, pasivum
a skladbu. O autorství textu nic neříká a nenahrazuje úsudek: nález je
důvod se na místo podívat.

Použití:
    python3 metriky.py text.txt --profil blog
    python3 metriky.py text.txt --udpipe czech-pdt-ud-2.5-191206.udpipe --format json
    cat text.txt | python3 metriky.py - --profil email
    python3 metriky.py text.txt --vse    # i blokové citace „>“, tabulky a „…“ naplno

Bloky kódu (``` ~~~, odsazené, <pre>, <code>), inline kód, URL, e-maily a blokové
citace „>“ se neměří a nepočítají do slov, pomlček ani rytmu; nálezy v tabulkách
a uvnitř „…“ jsou jen info. Výstup hlásí vynechaný text v souhrn.vylouceno.

Bez modelu běží v omezeném režimu: dělení vět podle pravidel, seznamy slov
přes kmeny (výsledek je přibližný), bez nominalizace, pasiva a skladby.
Model UDPipe má licenci CC BY-NC-SA, do repozitáře nepatří; skript ho jen
načítá z cesty (přepínač --udpipe nebo proměnná UNSLOP_UDPIPE).

Jen standardní knihovna Pythonu 3.8+, bez sítě. S modelem navíc balíček
`ufal.udpipe` (pip install ufal.udpipe).
"""

import argparse
import json
import math
import os
import re
import statistics
import sys
from dataclasses import dataclass, field

VERZE = "0.3.0"

# ---------------------------------------------------------------------------
# Prahy. "puvod": SKILL = převzato ze SKILL.md / slova.md beze změny,
# NAVRH = nový práh skriptu, který SKILL.md neurčuje; kde není i KALIBRACE, je to
# odhad k ověření na AI-Koditexu proti lidským textům,
# KALIBRACE = odvozeno z lidských textů (UD Czech-CAC, FicTree, úseky po ~190
# slovech): práh leží zhruba u 95.–99. percentilu lidských úseků, takže omezuje
# falešné poplachy; citlivost na AI text neměří. Data a postup: references/zdroje.md
# (oddíl Kalibrace skriptu) a tools/kalibrace/kalibrace_ud.py.
# ---------------------------------------------------------------------------
PRAHY = {
    "pomlcky_na_300_slov": {"hodnota": 1, "puvod": "SKILL"},
    "pomlcky_socialni_v_textu": {"hodnota": 2, "puvod": "SKILL"},
    "vykricniky_na_1000_slov": {"hodnota": 1, "puvod": "SKILL (slova.md)"},
    "emoji_socialni": {"hodnota": 2, "puvod": "SKILL"},
    "hashtagy": {"hodnota": 5, "puvod": "SKILL (slova.md: pět a víc)"},
    "uroven2_v_odstavci": {"hodnota": 2, "puvod": "SKILL (slova.md)"},
    "uroven2_dlouhy_odstavec_slov": {"hodnota": 120, "puvod": "F5 + KALIBRACE"},
    "uroven2_v_dlouhem_odstavci": {"hodnota": 3, "puvod": "F5 + KALIBRACE (CAC: 12,6 % → 5,3 % "
                                   "úseků po 190 slovech)"},
    "uroven3_v_odstavci": {"hodnota": 4, "puvod": "NAVRH + KALIBRACE"},
    "rytmus_podobna_delka_slov": {"hodnota": 2, "puvod": "NAVRH"},
    "rytmus_podobna_delka_podil": {"hodnota": 0.15, "puvod": "NAVRH"},
    "rytmus_beh_p2": {"hodnota": 5, "puvod": "NAVRH + KALIBRACE"},
    "rytmus_cv_min": {"hodnota": 0.25, "puvod": "NAVRH + KALIBRACE"},
    "rytmus_cv_min_vet": {"hodnota": 6, "puvod": "NAVRH"},
    "kratka_veta_slov": {"hodnota": 5, "puvod": "NAVRH"},
    "retez_kratkych_vet": {"hodnota": 3, "puvod": "SKILL"},
    "heslo_slov": {"hodnota": 3, "puvod": "NAVRH"},
    "heslovita_kadence_mist": {"hodnota": 3, "puvod": "SKILL"},
    "kontrast_na_text": {"hodnota": 1, "puvod": "SKILL"},
    "trojice_prid_jmen_na_text": {"hodnota": 1, "puvod": "SKILL"},
    "privesky_na_100_vet": {"hodnota": 6.0, "puvod": "NAVRH + KALIBRACE"},
    "konektory_na_100_vet": {"hodnota": 12.0, "puvod": "NAVRH + KALIBRACE"},
    "konektory_retez": {"hodnota": 3, "puvod": "SKILL (slova.md)"},
    "nicmene_rituál": {"hodnota": 2, "puvod": "NAVRH"},
    "jmenne_vety_podil_p1": {"hodnota": 0.5, "puvod": "SKILL (většina vět)"},
    "slovesna_subst_na_1000_slov": {"hodnota": 60.0, "puvod": "NAVRH + KALIBRACE"},
    "opisne_pasivum_p2": {"hodnota": 2, "puvod": "SKILL (jedno je slabé samo o sobě)"},
    "opisne_pasivum_podil_p2": {"hodnota": 0.2, "puvod": "NAVRH + KALIBRACE"},
    "zajmena_podmet_svuj_okno": {"hodnota": 4, "puvod": "NAVRH + KALIBRACE"},
    "ukazovaci_zacatky": {"hodnota": 3, "puvod": "NAVRH"},
    "ukazovaci_zacatky_podil": {"hodnota": 0.25, "puvod": "NAVRH"},
    "prechody_p1": {"hodnota": 2, "puvod": "F5 (kalibrace F3: jediný přechod v 4 % lidských úseků)"},
}


def prah(jmeno):
    return PRAHY[jmeno]["hodnota"]


# ---------------------------------------------------------------------------
# Lidská reference: psaný Koditex, 5,08 mil. slov, proti AI-Koditexu v2 (25 modelů,
# stejných 150 textů); zdroje v references/zdroje.md, výpočet v tools/koditex/README.md.
# Jen pro informativní metriky; AI v AI-Koditexu má u postoje a konkrétnosti
# zhruba polovinu, u soudržnosti víc. Přepis nemá hodnoty postoje a konkrétnosti
# snižovat (SKILL.md, pojistky).
# ---------------------------------------------------------------------------
REFERENCE = {
    "ktery_na_1000_slov": {"lide": 7.7, "ai": 11.8},
    "coz_na_100_vet": {"lide": 0.59, "ai": 1.16},
    "modalni_na_1000_slov": {"lide": 3.3, "ai": 1.3},
    "oslabujici_na_1000_slov": {"lide": 1.9, "ai": 1.0},
    "osoba2_zajmena_na_1000_slov": {"lide": 3.2, "ai": 1.6},
    "otazniky_na_100_vet": {"lide": 5.38, "ai": 2.65},
    "cisla_na_1000_slov": {"lide": 16.3, "ai": 8.8},
    "vlastni_jmena_na_1000_slov": {"lide": 42.4, "ai": 24.1},
    "tento_na_zacatku_podil_vet": {"lide": 0.007, "ai": 0.03},
}


# ---------------------------------------------------------------------------
# Profily registrů (tabulka v SKILL.md, oddíl Profily registrů)
# ---------------------------------------------------------------------------
PROFILY = {
    "socialni": dict(seznamy="prisne", pomlcky="socialni", spojovnik_nalez=False,
                     rytmus=False, kratke_vety=False, jmenny_styl=True, pasivum=True,
                     emoji=prah("emoji_socialni"), tech_vyjimky=False, uredni=True,
                     odhaleni=True, vykricniky=False, titulky_upoutavka="P2"),
    "blog": dict(seznamy="prisne", pomlcky="prisne", spojovnik_nalez=True,
                 rytmus=True, kratke_vety=True, jmenny_styl=True, pasivum=True,
                 emoji=0, tech_vyjimky=False, uredni=True, odhaleni=True,
                 vykricniky=True, titulky_upoutavka="P2"),
    "email": dict(seznamy="p0p1", pomlcky="prisne", spojovnik_nalez=False,
                  rytmus=False, kratke_vety=False, jmenny_styl=True, pasivum=True,
                  emoji=0, tech_vyjimky=False, uredni=True, odhaleni=False,
                  vykricniky=True, titulky_upoutavka="P2"),
    "dokumentace": dict(seznamy="castecne", pomlcky="volne", spojovnik_nalez=False,
                        rytmus=False, kratke_vety=False, jmenny_styl=False, pasivum=False,
                        emoji=0, tech_vyjimky=True, uredni=False, odhaleni=False,
                        vykricniky=True, titulky_upoutavka="P2"),
    "odborny": dict(seznamy="prisne", pomlcky="prisne", spojovnik_nalez=True,
                    rytmus=True, kratke_vety=True, jmenny_styl=False, pasivum=False,
                    emoji=0, tech_vyjimky=True, uredni=True, odhaleni=True,
                    vykricniky=True, titulky_upoutavka="P2"),
    "prezentace": dict(seznamy="prisne", pomlcky="prisne", spojovnik_nalez=True,
                       rytmus=True, kratke_vety=False, jmenny_styl=False, pasivum=True,
                       emoji=0, tech_vyjimky=False, uredni=True, odhaleni=True,
                       vykricniky=True, titulky_upoutavka="P1"),
}
ALIASY_PROFILU = {
    "soc": "socialni", "socialni-site": "socialni", "sociální": "socialni",
    "linkedin": "socialni", "esej": "blog", "clanek": "blog", "článek": "blog",
    "e-mail": "email", "zprava": "email", "zpráva": "email", "slack": "email",
    "dok": "dokumentace", "tech": "dokumentace", "pravni": "dokumentace",
    "právní": "dokumentace", "odb": "odborny", "odborný": "odborny",
    "prez": "prezentace", "slajdy": "prezentace",
}

PORADI_ZAV = {"P0": 0, "P1": 1, "P2": 2, "info": 3}

# ---------------------------------------------------------------------------
# Pomocné seznamy (gramatika, ne slovník slopu – ten je v slova.md)
# ---------------------------------------------------------------------------
ZKRATKY_NIKDY_KONEC = {
    "tj", "např", "tzv", "resp", "cca", "popř", "příp", "mj", "č", "čís", "s", "str",
    "obr", "tab", "kap", "odst", "písm", "ing", "mgr", "bc", "mudr", "judr", "phdr",
    "rndr", "paeddr", "mvdr", "mddr", "doc", "prof", "dr", "pí", "sv", "ul", "nám",
    "tel", "vč", "zvl", "tř", "roč", "sb", "hod", "min", "max", "tis", "mil", "mld",
    "st", "zejm", "tzn", "srov", "pozn", "kupř", "event", "ev", "p", "et", "al", "vs",
    "mn", "jr", "sr", "arch", "bc", "dipl", "csc", "drsc", "mba", "o", "r",
}
ZKRATKY_MOZNA_KONEC = {"atd", "apod", "aj", "etc", "spol", "a.s", "s.r.o"}

ZVRATNA = {"se", "si"}
OSOBNI_ZAJMENA = {
    "já", "mě", "mne", "mi", "mně", "mnou", "ty", "tě", "tebe", "ti", "tobě", "tebou",
    "my", "nás", "nám", "námi", "vy", "vás", "vám", "vámi", "on", "ona", "ono", "oni",
    "ony", "jeho", "jej", "ho", "mu", "jemu", "jím", "něj", "něho", "němu", "ní", "jí",
    "ji", "ni", "jich", "jim", "jimi", "nich", "nim", "nimi",
}
ZAJMENA_1OS = {"já", "mě", "mne", "mi", "mně", "mnou", "my", "nás", "nám", "námi",
               "můj", "moje", "mého", "mému", "mým", "mých", "mými", "mojí", "mou", "má",
               "náš", "naše", "našeho", "našemu", "naším", "našich", "našimi", "naší"}
ZAJMENA_2OS = {"ty", "tě", "tebe", "ti", "tobě", "tebou", "vy", "vás", "vám", "vámi",
               "tvůj", "tvoje", "tvého", "tvému", "tvým", "tvých", "tvými", "tvojí", "tvou",
               "váš", "vaše", "vašeho", "vašemu", "vaším", "vašich", "vašimi", "vaší"}
TVARY_SVUJ = {"svůj", "svoje", "své", "svého", "svému", "svým", "svých", "svými",
              "svou", "svojí", "svá", "svoji", "svým"}
TVARY_TENTO = {"tento", "tato", "toto", "tyto", "tito", "této", "tohoto", "tomuto",
               "tomto", "touto", "tímto", "těchto", "těmto", "těmito", "tuto"}
CASTICE = ["přece", "vždyť", "snad", "asi", "prý", "totiž", "vlastně", "copak", "jo", "no",
           "teda", "ostatně", "beztak", "stejně"]
# definice z F2 (tools/koditex/features.py), aby šlo srovnat s referencí
MODALNI = {"přece", "vždyť", "prý", "totiž", "vlastně", "no", "copak", "ostatně", "beztak",
           "stejně", "aspoň", "alespoň", "hlavně", "teda"}
OSLABUJICI = {"snad", "asi", "možná", "zřejmě", "patrně", "nejspíš", "nejspíše",
              "pravděpodobně", "údajně"}
KONEKTORY = ["v neposlední řadě", "kromě toho", "díky tomu", "navíc", "zároveň",
             "nicméně", "tudíž", "dále", "rovněž", "současně", "celkově"]
# na začátku věty nejsou u AI častější než u lidí (F2), vadí jen v řetězu
KONEKTORY_JEN_RETEZ = {"navíc", "dále"}
POMOCNE_PRIKLONKY = {"jsem", "jsi", "jsme", "jste", "bych", "bys", "by", "bychom", "byste"}
STOP = {"být", "o", "v", "ve", "na", "a", "se", "si", "ten", "to", "že", "do", "s", "z",
        "k", "u", "je", "i", "jako", "pro", "po", "za", "jsou", "tak", "toho", "tom"}
ZASTUPCE = {"x", "y", "z", "někým", "někoho", "něco", "něčeho", "někdo", "něčem", "…", "..."}
VNOUN_NEJSOU = {"náměstí", "štěstí", "neštěstí", "pití", "zboží", "ústí", "listí",
                "kamení", "loubí", "smetí", "uhlí", "jmění", "mládí", "napětí", "hnutí",
                "století", "dění", "znamení", "pokolení", "umění", "vědění", "stavení",
                "pobřeží", "zátiší", "území", "nádraží", "prostředí", "období", "údolí"}
NEJSOU_CLENY = {"a", "i", "ale", "nebo", "či", "ani", "však", "tedy", "že", "jak", "což",
                "který", "která", "které", "když", "aby", "protože", "ne", "jen", "pak"}
CISLOVKY_SLOVY = r"(?:jeden|jedna|jedno|dva|dvě|tři|čtyři|pět|šest|sedm|osm|devět|deset|\d+)"

RE_SLOVO = re.compile(r"[^\W_]+(?:[-'’][^\W_]+)*")
RE_EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-➿\U0001F000-\U0001F2FF]")


# ---------------------------------------------------------------------------
# Datové struktury
# ---------------------------------------------------------------------------
@dataclass
class Tok:
    form: str
    lemma: str
    upos: str
    feats: dict
    head: int
    deprel: str
    start: int
    end: int
    idx: int  # pořadí ve větě od 0

    @property
    def low(self):
        return self.form.lower()

    def je_slovo(self):
        if self.upos:
            return self.upos not in ("PUNCT", "SYM")
        return any(c.isalnum() for c in self.form)


@dataclass
class Veta:
    start: int
    end: int
    tokens: list
    blok: int
    druh: str  # veta | titulek | radek
    text: str = ""

    def slova(self):
        return [t for t in self.tokens if t.je_slovo()]

    def pocet_slov(self):
        return len(self.slova())


@dataclass
class Nalez:
    metrika: str
    kategorie: str
    zavaznost: str
    start: int
    end: int
    text: str
    poznamka: str = ""
    priblizne: bool = False
    zdroj: str = ""

    def jako_dict(self, radky):
        r, s = radky(self.start)
        d = dict(metrika=self.metrika, kategorie=self.kategorie, zavaznost=self.zavaznost,
                 text=self.text, pozice=[self.start, self.end], radek=r, sloupec=s)
        if self.poznamka:
            d["poznamka"] = self.poznamka
        if self.zdroj:
            d["zdroj"] = self.zdroj
        if self.priblizne:
            d["priblizne"] = True
        return d


# ---------------------------------------------------------------------------
# Kmenování bez modelu (lehký kmenovač; výsledek je přibližný)
# ---------------------------------------------------------------------------
_PRIPONY = sorted(set("""
ovat ující ujete ujeme ovali ovala ovalo ovaly uješ ují uje ých ými ého ému ími ích ách ech ami emi ěmi ata aty atům atech ům ou
ám em ěm ím ým at it ít ět át al ala alo ali aly il ila ilo ili ily ěl ěla ěli el ela eli
ete eme íte íme ime nout nul nula nuli a e ě i í o u ů y ý á é
""".split()), key=len, reverse=True)


def kmen(slovo):
    w = slovo.lower()
    for p in _PRIPONY:
        if w.endswith(p) and len(w) - len(p) >= 3:
            return w[: -len(p)]
    return w


def shoda_kmenu(a, b):
    if a == b:
        return True
    n = min(len(a), len(b))
    if n < 5 or max(len(a), len(b)) - n > 1:
        return False
    cp = 0
    for x, y in zip(a, b):
        if x != y:
            break
        cp += 1
    return cp >= n - 1


# ---------------------------------------------------------------------------
# UDPipe
# ---------------------------------------------------------------------------
class UDPipe:
    def __init__(self, cesta):
        try:
            from ufal.udpipe import Model, Pipeline, ProcessingError  # noqa
        except ImportError:
            raise SystemExit("Chybí balíček ufal.udpipe (pip install ufal.udpipe).")
        self._PE = ProcessingError
        self.model = Model.load(cesta)
        if not self.model:
            raise SystemExit(f"Model UDPipe se nepodařilo načíst: {cesta}")
        self.pipe = Pipeline(self.model, "tokenizer=ranges", Pipeline.DEFAULT,
                             Pipeline.DEFAULT, "conllu")
        self.pipe_preseg = Pipeline(self.model, "tokenizer=ranges;presegmented",
                                    Pipeline.DEFAULT, Pipeline.DEFAULT, "conllu")

    def zpracuj(self, text, presegmented=False):
        """Vrátí seznam vět; každá věta je seznam Tok s offsety vůči `text`."""
        err = self._PE()
        out = (self.pipe_preseg if presegmented else self.pipe).process(text, err)
        if err.occurred():
            raise RuntimeError(err.message)
        vety, akt, mwt = [], [], {}
        for line in out.split("\n"):
            if not line:
                if akt:
                    vety.append(akt)
                akt, mwt = [], {}
                continue
            if line.startswith("#"):
                continue
            c = line.split("\t")
            if len(c) < 10:
                continue
            rng = re.search(r"TokenRange=(\d+):(\d+)", c[9])
            if "-" in c[0]:
                a, b = map(int, c[0].split("-"))
                for i in range(a, b + 1):
                    mwt[i] = (int(rng.group(1)), int(rng.group(2))) if rng else None
                continue
            if "." in c[0]:
                continue
            i = int(c[0])
            if rng:
                s, e = int(rng.group(1)), int(rng.group(2))
            elif mwt.get(i):
                s, e = mwt[i]
            else:
                s = e = akt[-1].end if akt else 0
            feats = {}
            if c[5] != "_":
                for f in c[5].split("|"):
                    if "=" in f:
                        k, v = f.split("=", 1)
                        feats[k] = v
            akt.append(Tok(c[1], c[2], c[3], feats, int(c[6]) if c[6].isdigit() else 0,
                           c[7], s, e, len(akt)))
        if akt:
            vety.append(akt)
        return vety


# ---------------------------------------------------------------------------
# Příprava textu: maskování chráněných míst a bloky
# ---------------------------------------------------------------------------
RE_OHRAZENI = re.compile(r"^ {0,3}(`{3,}|~{3,})")
RE_CITACE_RADEK = re.compile(r"^ {0,3}>")
RE_UPOZORNENI = re.compile(r"\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]", re.I)
RE_TAB_ODDELOVAC = re.compile(r"^ {0,3}\|?[ \t]*:?-+:?[ \t]*(\|[ \t]*:?-+:?[ \t]*)*\|?[ \t]*$")
RE_ODSAZENY_KOD = re.compile(r"^( {4}|\t)[ \t]*\S")
RE_POLOZKA_RADEK = re.compile(r"^ {0,3}([-*+•]|\d{1,2}[.)])[ \t]+\S")
RE_HTML_KOD = re.compile(r"<(pre|code)\b[^>]*>.*?</\1\s*>", re.S | re.I)
RE_INLINE_KOD = re.compile(r"(`+)(?!`)[^\n]*?[^`\n](?<!`)\1(?!`)")
RE_URL_MAIL = re.compile(r"\bhttps?://\S+|\bwww\.\S+|\b[\w.+-]+@[\w-]+\.[\w.]+")


def maskuj(text, vse=False):
    """Připraví text k měření. Vrátí (masked, pasma).

    masked: kopie textu, v níž jsou kód, URL, e-mailové adresy a blokové citace „>“
    nahrazené mezerami (délka a konce řádků zůstávají, pozice nálezů sedí na původní
    text). Vyloučený text se nepočítá do ničeho: do slov, pomlček, vět ani rytmu.

    pasma: [(start, end, druh)] bloků mimo měření pro hlášení ve výstupu a hranice
    rytmu. Druh kod a citace je vymazaný; druh tabulka zůstává, jen bez svislítek
    a oddělovacího řádku: místní nálezy v buňkách jdou do info a buňky se nepočítají
    do slov, pomlček ani rytmu (Dokument.slova).

    Kód (ohrazení ``` a ~~~, odsazený blok, <pre>, <code>, inline `kód`), URL
    a e-maily se maskují vždy. S vse=True se citace a tabulky měří jako běžný text.
    Upozornění GitHubu („> [!NOTE]“) jsou text autora a měří se i bez vse."""
    chars = list(text)

    def vymaz(a, b):
        for i in range(a, b):
            if chars[i] != "\n":
                chars[i] = " "

    radky = []
    pos = 0
    for line in text.split("\n"):
        radky.append((pos, pos + len(line), line))
        pos += len(line) + 1
    n = len(radky)
    obsazeno = [False] * n
    pasma = []

    def pridej_pasmo(i, j, druh):
        """Řádky i..j (včetně) jako jedno pásmo."""
        for k in range(i, j + 1):
            obsazeno[k] = True
        pasma.append((radky[i][0], radky[j][1], druh))

    # 1. ohrazené bloky ``` a ~~~ (neuzavřený blok sahá do konce textu)
    i = 0
    while i < n:
        m = RE_OHRAZENI.match(radky[i][2])
        if m and not (m.group(1)[0] == "`" and "`" in radky[i][2][m.end():]):
            zn = m.group(1)
            zav = re.compile(r"^ {0,3}" + re.escape(zn[0]) + "{" + str(len(zn)) + r",}[ \t]*$")
            j = i + 1
            while j < n and not zav.match(radky[j][2]):
                j += 1
            j = min(j, n - 1)
            pridej_pasmo(i, j, "kod")
            vymaz(radky[i][0], radky[j][1])
            i = j + 1
        else:
            i += 1

    def radek_na(p):
        lo, hi = 0, n - 1
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if radky[mid][0] <= p:
                lo = mid
            else:
                hi = mid - 1
        return lo

    # 2. HTML <pre> a <code>; víceřádkový se hlásí jako blok kódu, jednořádkový jako inline
    for m in RE_HTML_KOD.finditer(text):
        i, j = radek_na(m.start()), radek_na(m.end())
        if any(obsazeno[k] for k in range(i, j + 1)):
            continue
        vymaz(m.start(), m.end())
        if m.group(1).lower() == "pre" or i != j:
            for k in range(i, j + 1):
                obsazeno[k] = True
            pasma.append((m.start(), m.end(), "kod"))

    # 3. blokové citace „>“; upozornění GitHubu zůstávají, maže se jen značka [!NOTE]
    i = 0
    while i < n:
        if obsazeno[i] or not RE_CITACE_RADEK.match(radky[i][2]):
            i += 1
            continue
        j = i
        while j + 1 < n and not obsazeno[j + 1] and RE_CITACE_RADEK.match(radky[j + 1][2]):
            j += 1
        prvni = radky[i][2].lstrip(" >\t")
        upoz = RE_UPOZORNENI.match(prvni)
        if upoz:
            s = radky[i][0] + radky[i][2].index(upoz.group(0))
            vymaz(s, s + len(upoz.group(0)))
        elif not vse:
            pridej_pasmo(i, j, "citace")
            vymaz(radky[i][0], radky[j][1])
        i = j + 1

    # 4. tabulky Markdownu: řádek se svislítkem a pod ním oddělovací řádek
    if not vse:
        i = 0
        while i + 1 < n:
            if obsazeno[i] or obsazeno[i + 1] or "|" not in radky[i][2] or \
                    "|" not in radky[i + 1][2] or not RE_TAB_ODDELOVAC.match(radky[i + 1][2]):
                i += 1
                continue
            j = i + 1
            while j + 1 < n and not obsazeno[j + 1] and "|" in radky[j + 1][2] and \
                    radky[j + 1][2].strip():
                j += 1
            pridej_pasmo(i, j, "tabulka")
            vymaz(radky[i + 1][0], radky[i + 1][1])
            for k in range(i, j + 1):
                a, b, _ = radky[k]
                for p in range(a, b):
                    if chars[p] == "|":
                        chars[p] = " "
            i = j + 1

    # 5. odsazený kód (CommonMark): před blokem prázdný řádek a nejde o pokračování
    # položky seznamu. Když je odsazená víc než polovina odstavců, jde o odsazení
    # prvního řádku (text z Wordu), ne o kód.
    kandidati = []
    odstavcu = 0
    i = 0
    predchozi_neprazdny = None  # index posledního neprázdného řádku
    while i < n:
        line = radky[i][2]
        if not line.strip() or obsazeno[i]:
            if line.strip():
                predchozi_neprazdny = i
            i += 1
            continue
        odstavcu += 1
        zacatek_odstavce = i
        if RE_ODSAZENY_KOD.match(line) and (i == 0 or not radky[i - 1][2].strip()) and (
                predchozi_neprazdny is None or
                not (RE_POLOZKA_RADEK.match(radky[predchozi_neprazdny][2]) or
                     re.match(r"^[ \t]{2,}\S", radky[predchozi_neprazdny][2]))):
            j = i
            while True:
                k = j + 1
                while k < n and not radky[k][2].strip() and not obsazeno[k]:
                    k += 1
                if k < n and not obsazeno[k] and RE_ODSAZENY_KOD.match(radky[k][2]):
                    j = k
                else:
                    break
            kandidati.append((i, j))
            predchozi_neprazdny = j
            i = j + 1
            continue
        while i < n and radky[i][2].strip() and not obsazeno[i]:
            i += 1
        predchozi_neprazdny = i - 1 if i > zacatek_odstavce else predchozi_neprazdny
    if kandidati and len(kandidati) * 2 <= odstavcu:
        for i, j in kandidati:
            pridej_pasmo(i, j, "kod")
            vymaz(radky[i][0], radky[j][1])

    # 6. inline kód, URL a e-maily (vždy, mimo už vymazané bloky)
    for k, (a, b, line) in enumerate(radky):
        if obsazeno[k]:
            continue
        for m in RE_INLINE_KOD.finditer(line):
            vymaz(a + m.start(), a + m.end())
    for m in RE_URL_MAIL.finditer(text):
        vymaz(m.start(), m.end())
    pasma.sort()
    return "".join(chars), pasma


RE_ZNACKA = re.compile(r"^([ \t]*)(#{1,6}[ \t]+|>[ \t]?|[-*•][ \t]+|\d{1,2}[.)][ \t]+)")
RE_KONCOVA = re.compile(r"[.!?:;…]\s*[\"“”»)]*\s*$")


def bloky(masked, tabulky=()):
    """Rozdělí text na bloky: (start, end, druh) s druhem odstavec | nadpis | polozka |
    tabulka (každý řádek tabulky je samostatný blok). Značky seznamů, nadpisů
    a citací v `masked` nahradí mezerami (vrací nový masked). `tabulky` jsou rozsahy
    (start, end) tabulek z maskuj()."""
    chars = list(masked)
    out = []
    pos = 0
    odst = None  # [start, end]
    for line in masked.split("\n"):
        ls, le = pos, pos + len(line)
        pos = le + 1
        if any(a <= ls and le <= b for a, b in tabulky):
            if odst:
                out.append((odst[0], odst[1], "odstavec"))
                odst = None
            if line.strip():
                out.append((ls, le, "tabulka"))
            continue
        m = RE_ZNACKA.match(line)
        druh = "text"
        if m:
            zn = m.group(2)
            for i in range(ls + len(m.group(1)), ls + m.end()):
                chars[i] = " "
            if zn.startswith("#"):
                druh = "nadpis"
            elif zn.startswith(">"):
                druh = "text"
            else:
                druh = "polozka"
        obsah = "".join(chars[ls:le]).strip()
        if not obsah:
            if odst:
                out.append((odst[0], odst[1], "odstavec"))
                odst = None
            continue
        if druh in ("nadpis", "polozka"):
            if odst:
                out.append((odst[0], odst[1], "odstavec"))
                odst = None
            out.append((ls, le, druh))
            continue
        if odst:
            odst[1] = le
        else:
            odst = [ls, le]
    if odst:
        out.append((odst[0], odst[1], "odstavec"))
    return "".join(chars), out


def segmenty(masked, start, end):
    """Odstavec rozdělí na řádkové úseky: zalomení řádku je hranice, když řádek
    nekončí interpunkcí a další začíná velkým písmenem (podpis, oslovení, titulek)."""
    text = masked[start:end]
    radky = []
    p = start
    for line in text.split("\n"):
        radky.append((p, p + len(line)))
        p += len(line) + 1
    seg = []
    akt = None
    for i, (a, b) in enumerate(radky):
        obsah = masked[a:b].strip()
        if not obsah:
            continue
        if akt is None:
            akt = [a, b]
        else:
            predchozi = masked[akt[0]:akt[1]].rstrip()
            zacatek = obsah[:1]
            if not RE_KONCOVA.search(predchozi) and zacatek.isupper():
                seg.append(tuple(akt))
                akt = [a, b]
            else:
                akt[1] = b
    if akt:
        seg.append(tuple(akt))
    return seg


# ---------------------------------------------------------------------------
# Dělení na věty bez modelu
# ---------------------------------------------------------------------------
RE_KANDIDAT = re.compile(r"[.!?…]+[\"“”»’)\]]*(?=\s|$)")


def deleni_vet_pravidla(text, a, b):
    """Vrátí seznam (start, end) vět v text[a:b]."""
    vety = []
    s = a
    while s < b and text[s].isspace():
        s += 1
    for m in RE_KANDIDAT.finditer(text, s, b):
        if m.start() < s:
            continue
        interp = m.group(0)
        konec = m.end()
        # další znak po mezerách
        j = konec
        while j < b and text[j].isspace():
            j += 1
        dalsi = text[j] if j < b else ""
        dalsi_n = dalsi
        k = j
        while dalsi_n and dalsi_n in "„\"“‚'(«»[" and k + 1 < b:
            k += 1
            dalsi_n = text[k]
        pred = re.search(r"([^\W_]+)[\W_]*$", text[s:m.start() + 1]) if m.start() >= s else None
        slovo = pred.group(1) if pred else ""
        tecka_jen = set(interp.rstrip("\"“”»’)]")) <= {"."}
        if not dalsi:
            je_konec = True
        elif not tecka_jen:
            # ! ? … ukončují větu, pokud nepokračuje malé písmeno po výpustce
            # česká věta nezačíná malým písmenem („Co?“ zeptala se.)
            je_konec = not dalsi_n.islower()
        elif dalsi_n.islower():
            je_konec = False
        elif dalsi_n.isdigit():
            je_konec = not (slovo.isdigit() or slovo.lower() in ZKRATKY_NIKDY_KONEC)
        else:
            lo = slovo.lower()
            if lo in ZKRATKY_NIKDY_KONEC:
                je_konec = False
            elif len(slovo) == 1 and slovo.isupper():
                je_konec = False  # iniciála
            elif re.search(r"\b(?:Ph|Th|Dr|Mgr|Ing|Bc)\.\s*[A-Z]?$", text[s:m.start()]):
                je_konec = False
            else:
                je_konec = True
        if je_konec:
            vety.append((s, konec))
            s = j
    if s < b and text[s:b].strip():
        e = b
        while e > s and text[e - 1].isspace():
            e -= 1
        vety.append((s, e))
    return vety


def tokeny_pravidla(text, a, b):
    toks = []
    for m in re.finditer(r"[^\W_]+(?:[-'’][^\W_]+)*|[^\w\s]", text[a:b]):
        f = m.group(0)
        toks.append(Tok(f, kmen(f) if f[0].isalnum() else f, "", {}, 0, "",
                        a + m.start(), a + m.end(), len(toks)))
    return toks


# ---------------------------------------------------------------------------
# Analýza textu: věty a tokeny
# ---------------------------------------------------------------------------
class Dokument:
    def __init__(self, text, udpipe=None, vse=False):
        self.text = text
        self.udpipe = udpipe
        self.masked0, self.pasma = maskuj(text, vse)
        self.masked, self.bloky = bloky(self.masked0, [(a, b) for a, b, d in self.pasma
                                                       if d == "tabulka"])
        self.vety = []
        self._radky = [0]
        for i, ch in enumerate(text):
            if ch == "\n":
                self._radky.append(i + 1)
        self._analyzuj()

    def radek(self, pos):
        import bisect
        r = bisect.bisect_right(self._radky, pos) - 1
        return r + 1, pos - self._radky[r] + 1

    def _vety_z_useku(self, a, b, blok, titulek):
        useky = []
        if self.udpipe:
            usek = self.masked[a:b]
            for toks in self.udpipe.zpracuj(usek.replace("\n", " "), presegmented=titulek):
                for t in toks:
                    t.start += a
                    t.end += a
                if toks:
                    useky.append(toks)
        else:
            rozsahy = [(a, b)] if titulek else deleni_vet_pravidla(self.masked, a, b)
            for s, e in rozsahy:
                toks = tokeny_pravidla(self.masked, s, e)
                if toks:
                    useky.append(toks)
        for toks in useky:
            s, e = toks[0].start, toks[-1].end
            text = self.masked[s:e]
            n = sum(1 for t in toks if t.je_slovo())
            if titulek:
                druh = "titulek"
            else:
                druh = "veta"
            self.vety.append(Veta(s, e, toks, blok, druh, text))

    def _analyzuj(self):
        for bi, (a, b, druh) in enumerate(self.bloky):
            obsah = self.masked[a:b].strip()
            if not obsah:
                continue
            n_slov = len(RE_SLOVO.findall(obsah))
            if druh == "tabulka":
                n0 = len(self.vety)
                self._vety_z_useku(a, b, bi, True)
                for v in self.vety[n0:]:
                    v.druh = "tabulka"
                continue
            if druh == "nadpis" or (druh == "polozka" and not RE_KONCOVA.search(obsah)
                                     and n_slov <= 12):
                self._vety_z_useku(a, b, bi, True)
                continue
            for sa, sb in segmenty(self.masked, a, b):
                seg = self.masked[sa:sb].strip()
                ns = len(RE_SLOVO.findall(seg))
                samostatny = (len(self.bloky) > 1 and (sa, sb) == (a, b) and
                              not RE_KONCOVA.search(seg) and ns <= 10)
                if samostatny:
                    self._vety_z_useku(sa, sb, bi, True)
                elif not RE_KONCOVA.search(seg) and ns <= 4 and (sa, sb) != (a, b):
                    # krátký řádek bez interpunkce uvnitř odstavce (podpis, oslovení)
                    n0 = len(self.vety)
                    self._vety_z_useku(sa, sb, bi, False)
                    for v in self.vety[n0:]:
                        v.druh = "radek"
                else:
                    self._vety_z_useku(sa, sb, bi, False)

    def slova(self):
        """Slova textu bez buněk tabulek (ty jsou mimo počet slov, pomlčky i rytmus)."""
        return [t for v in self.vety if v.druh != "tabulka" for t in v.tokens if t.je_slovo()]

    def pocet_slov(self):
        return len(self.slova())

    def prozni_vety(self):
        return [v for v in self.vety if v.druh == "veta"]

    def vylouceno(self):
        """Souhrn textu mimo měření: kolik slov a kolik bloků podle druhu."""
        slov, useku = 0, {}
        for a, b, druh in self.pasma:
            useku[druh] = useku.get(druh, 0) + 1
            if druh == "tabulka":
                slov += sum(v.pocet_slov() for v in self.vety
                            if v.druh == "tabulka" and a <= v.start < b)
            else:
                slov += len(RE_SLOVO.findall(self.text[a:b]))
        return {"slov": slov, "useku": useku}

    def preruseno(self, a, b):
        """True, když mezi pozicemi a < b leží blok mimo měření (kód, citace, tabulka)."""
        return any(a <= s and e <= b for s, e, _ in self.pasma)


# ---------------------------------------------------------------------------
# Parsování references/slova.md
# ---------------------------------------------------------------------------
@dataclass
class Polozka:
    sekce: str          # uroven1 | uroven2 | uroven3 | kalk | fraze | chatbot | anglicismus | opis | jmenny | uredni
    kategorie: str      # podrobnější kategorie (např. Úvody)
    zavaznost: str      # výchozí závažnost
    raw: str
    varianty: list
    poznamka: str = ""
    podminka: bool = False   # poznámka omezuje platnost (skript ji neumí ověřit)
    tech: bool = False       # neplatí v technickém/odborném profilu
    privesek: bool = False   # platí jen jako přívěsek (což/čímž/a tím)
    vzory: list = field(default_factory=list)


PREPISY_POLOZEK = {
    # Položky, kde čárka neodděluje alternativy, ale předměty jednoho slovesa.
    "kontrolovat proces, tým, rozpočet": ["kontrolovat proces", "kontrolovat tým",
                                          "kontrolovat rozpočet"],
    "sdílet s někým novinku, aktualizaci": ["sdílet novinku", "sdílet aktualizaci"],
}

KATEGORIE_FRAZI = {
    "úvody": ("uvod", "P1"), "přechody": ("prechod", "P1"), "závěry": ("zaver", "P2"),
    "falešné prozření": ("prozreni", "P1"), "mravoučné pointy": ("pointa", "P1"),
    "okřídlené metafory": ("metafora-ai", "P1"), "plastová lidskost": ("hrana-upřímnost", "P1"),
    "ohrané trojice": ("ohrana-trojice", "P1"), "sociální sítě": ("socialni-site", "P1"),
}

RE_PODMINKA = re.compile(r"\b(jako|mimo|u|bez|když|v přeneseném|přeneseně|inflačně|ve smyslu|"
                         r"místo)\b")
RE_TECH = re.compile(r"mimo (techni|obor|statisti|popis technického)")


def _split_mimo_zavorky(s, sep=","):
    parts, d, akt = [], 0, ""
    for ch in s:
        if ch in "([":
            d += 1
        elif ch in ")]":
            d -= 1
        if ch == sep and d == 0:
            parts.append(akt)
            akt = ""
        else:
            akt += ch
    parts.append(akt)
    return [p.strip() for p in parts if p.strip()]


def _rozepis_lomitka(s):
    """Rozepíše alternativy s lomítkem podle konvence zápisu slova.md: „posunout na
    další / novou úroveň“ střídá jedno slovo, „odemknout / uvolnit / naplno využít
    potenciál“ střídá hlavu před společným posledním slovem."""
    if "/" not in s:
        return [s]
    segs = [x.strip() for x in s.split("/")]
    vys = set()

    def slova(x):
        w = x.split()
        # zvratné se/si drž s následujícím slovem
        out, i = [], 0
        while i < len(w):
            if w[i].lower() in ZVRATNA and i + 1 < len(w):
                out.append(w[i] + " " + w[i + 1])
                i += 2
            else:
                out.append(w[i])
                i += 1
        return out

    sw = [slova(x) for x in segs]
    if len(sw[0]) == 1:
        # „odemknout / uvolnit / naplno využít potenciál“: hlavy sdílí poslední slovo
        posl = sw[-1][-1]
        for x in sw[:-1]:
            vys.add(" ".join(x + [posl]))
        vys.add(" ".join(sw[-1]))
    else:
        # „posunout na další / novou úroveň“: střídá se jedno slovo
        prefix = sw[0][:-1]
        suffix = sw[-1][1:]
        alt = [sw[0][-1]] + [" ".join(x) for x in sw[1:-1]] + [sw[-1][0]]
        for a in alt:
            vys.add(" ".join(prefix + [a] + suffix))
    for x in segs:  # celé úseky, které jsou samy větou
        if len(x.split()) >= 4:
            vys.add(x)
    return sorted(vys)


def _rozepis_volitelne(s):
    """„V dnešní (rychle se měnící / digitální) době“ → bez závorky a s každou alternativou."""
    m = re.search(r"\(([^)]*)\)", s)
    if not m:
        return [s]
    pred, za = s[: m.start()], s[m.end():]
    out = [re.sub(r"\s+", " ", pred + " " + za).strip()]
    for alt in m.group(1).split("/"):
        out.append(re.sub(r"\s+", " ", pred + " " + alt.strip() + " " + za).strip())
    vys = []
    for o in out:
        vys.extend(_rozepis_volitelne(o))
    return vys


def _cisti(s):
    s = s.replace("*", "").replace("„", "").replace("“", "")
    s = re.sub(r"\s+", " ", s)
    return s.strip(" .;:")


def _polozky_z_bunky(cell, sekce, kategorie, zav, bunka=False):
    """Buňka nebo položka výčtu → Polozka se seznamem variant. V buňce tabulky platí
    závorka na konci pro všechny položky („revoluční, průlomový (u běžné věci)“)."""
    vys = []
    kusy = []
    for k in _split_mimo_zavorky(cell):  # „je důkazem toho, že“: „že“ patří k předchozímu
        if kusy and re.match(r"(že|aby|jak|kde|kdy)\b", k):
            kusy[-1] += ", " + k
        else:
            kusy.append(k)
    if bunka and len(kusy) > 1:
        m = re.search(r"\(([^()]*)\)\s*$", kusy[-1])
        if m and not any("(" in k for k in kusy[:-1]):
            kusy = [k if k is kusy[-1] else f"{k} ({m.group(1)})" for k in kusy]
    for kus in kusy:
        pozn = " ".join(re.findall(r"\(([^)]*)\)", kus))
        zaklad = re.sub(r"\([^)]*\)", " ", kus)
        if re.search(r"\bjako \*[^*]+\*", zaklad):
            # „prostředí jako *landscape*“ popisuje význam, ne tvar; skript ho neověří
            vys.append(Polozka(sekce, kategorie, zav, kus.strip(), [], "význam: " +
                               re.search(r"\*([^*]+)\*", zaklad).group(1)))
            continue
        zaklad = _cisti(zaklad)
        if not zaklad:
            continue
        # závorka bez „=“ a bez podmínky obsahuje předměty („krajina (trhu, technologií)“)
        predmety = []
        if pozn and "=" not in pozn and not RE_PODMINKA.search(pozn) and "„" not in kus:
            predmety = [p.strip() for p in pozn.split(",") if p.strip()]
        p = Polozka(sekce, kategorie, zav, kus.strip(), [], pozn.strip())
        p.tech = bool(RE_TECH.search(pozn))
        p.privesek = "přívěsek" in pozn
        p.podminka = bool(pozn) and not predmety and not p.tech and not p.privesek
        if "=" in pozn:
            p.podminka = True
        klic = zaklad.lower()
        varianty = PREPISY_POLOZEK.get(klic) or _rozepis_lomitka(zaklad)
        if predmety:
            varianty = [v + " " + o for v in varianty for o in predmety]
        p.varianty = varianty
        vys.append(p)
    # „kontrolovat proces, tým, rozpočet“ – přepis platí pro celou buňku
    celek = _cisti(re.sub(r"\([^)]*\)", " ", cell)).lower()
    if celek in PREPISY_POLOZEK:
        p = Polozka(sekce, kategorie, zav, cell.strip(), PREPISY_POLOZEK[celek],
                    " ".join(re.findall(r"\(([^)]*)\)", cell)))
        p.podminka = "=" in p.poznamka
        return [p]
    return vys


def _fraze_z_textu(text, sekce, kategorie, zav):
    """Vytáhne fráze v „…“ s případnou poznámkou v závorce hned za nimi."""
    vys = []
    for m in re.finditer(r"„([^“]+)“(\s*\(([^)]*)\))?", text):
        fr = m.group(1).strip()
        if fr.lower().strip(" .…") in KONEKTORY:
            continue  # spojovací výrazy na začátku vět měří metrika soudržnosti
        pozn = (m.group(3) or "").strip()
        varianty = []
        for v in _rozepis_volitelne(fr):
            varianty.extend(_rozepis_lomitka(v))
        p = Polozka(sekce, kategorie, zav, fr, varianty, pozn)
        p.podminka = bool(pozn) and "rozpětí" not in pozn
        vys.append(p)
    return vys


def nacti_slova(cesta):
    """Robustní parser references/slova.md. Vrací (položky, varování)."""
    with open(cesta, encoding="utf-8") as f:
        md = f.read()
    polozky, varovani = [], []
    sekce = re.split(r"^## +", md, flags=re.M)
    for s in sekce[1:]:
        nadpis, _, telo = s.partition("\n")
        n = nadpis.lower()
        if "úroveň 1" in n:
            for row in re.findall(r"^\|(.+)\|\s*$", telo, flags=re.M):
                cells = [c.strip() for c in row.split("|")]
                if not cells or set(cells[0]) <= set("-: ") or cells[0].lower() == "místo":
                    continue
                polozky += _polozky_z_bunky(cells[0], "uroven1", "úroveň 1", "P1", bunka=True)
        elif "úroveň 2" in n or "úroveň 3" in n:
            u = "uroven2" if "úroveň 2" in n else "uroven3"
            odst = [o for o in telo.strip().split("\n\n") if o.strip()]
            if odst:
                polozky += _polozky_z_bunky(odst[0].replace("\n", " "), u,
                                            "úroveň 2" if u == "uroven2" else "úroveň 3",
                                            "P1" if u == "uroven2" else "P2")
        elif "kalk" in n:
            for row in re.findall(r"^\|(.+)\|\s*$", telo, flags=re.M):
                cells = [c.strip() for c in row.split("|")]
                if not cells or set(cells[0]) <= set("-: ") or cells[0].lower() == "kalk":
                    continue
                for p in _polozky_z_bunky(cells[0], "kalk", "kalk", "P2", bunka=True):
                    if len(cells) > 2 and re.search(r"slabé samo o sobě", cells[2], re.I):
                        p.zavaznost = "info"
                    if len(cells) > 2 and cells[2]:
                        p.poznamka = (p.poznamka + "; " if p.poznamka else "") + \
                            "česky: " + re.sub(r"\s+", " ", cells[2])[:80]
                    polozky.append(p)
            for m in re.finditer(r"^\*\*([^*]+)\*\*\s*(.+?)(?=\n\n|\Z)", telo, flags=re.M | re.S):
                stitek, obsah = m.group(1).lower(), m.group(2).replace("\n", " ")
                if "anglicism" in stitek:
                    it = re.search(r"\*([^*]+)\*", obsah)
                    if it:
                        polozky += _polozky_z_bunky(it.group(1), "anglicismus", "anglicismus",
                                                    "info")
                    continue
                if "stupňování" in stitek:
                    continue  # řeší regulární výraz
                vycet = re.split(r"\.\s+(?=[A-ZÁČĎÉĚÍŇÓŘŠŤÚŮÝŽ])", obsah)[0]
                if "opisy" in stitek:
                    polozky += _polozky_z_bunky(vycet, "opis", "opis pro je/má", "P2")
                elif "jmenný" in stitek:
                    polozky += _polozky_z_bunky(vycet, "jmenny", "jmenný styl", "P2")
                elif "úřední" in stitek:
                    polozky += _polozky_z_bunky(vycet, "uredni", "úřední výraz", "P2")
                else:
                    varovani.append(f"slova.md: neznámý odstavec „{m.group(1)}“ v sekci {nadpis}")
        elif "ustálené fráze" in n:
            for m in re.finditer(r"^\*\*([^*]+?):?\*\*:?\s*(.+?)(?=\n\n|\Z)", telo,
                                 flags=re.M | re.S):
                stitek = m.group(1).strip().rstrip(":").lower()
                klic = next((k for k in KATEGORIE_FRAZI if stitek.startswith(k)), None)
                kat, zav = KATEGORIE_FRAZI.get(klic, (stitek, "P2"))
                if klic is None:
                    varovani.append(f"slova.md: neznámá kategorie frází „{m.group(1)}“ → P2")
                polozky += _fraze_z_textu(m.group(2), "fraze", kat, zav)
        elif "vágní autorit" in n:
            odst = [o for o in telo.strip().split("\n\n") if o.strip()]
            if odst:
                polozky += _fraze_z_textu(odst[0], "vagni", "vágní autorita", "P0")
        elif "chatbot" in n:
            for o in telo.strip().split("\n\n"):
                if re.search(r"\bnejsou\b", o):
                    continue  # chráněné fráze (oslovení, rozloučení)
                zav = "info" if "(P1)" in o else "P0"
                polozky += _fraze_z_textu(o, "chatbot", "chatbot", zav)
        elif "typografie" in n:
            continue  # typografii řeší metrika 1
        else:
            varovani.append(f"slova.md: neznámá sekce „{nadpis.strip()}“ přeskočena")
    return polozky, varovani


# ---------------------------------------------------------------------------
# Párování vzorů
# ---------------------------------------------------------------------------
@dataclass
class VzorTok:
    klic: str
    zvratne: str = ""     # vyžadované se/si
    mezera: int = 2       # povolená mezera před tímto tokenem


def _klic(t, model):
    """S modelem: lemma (se záporem) + stupeň a |tvar pro záložní shodu; bez modelu kmen."""
    if model:
        k = t.lemma.lower()
        if t.feats.get("Polarity") == "Neg" and not k.startswith("ne"):
            k = "ne" + k  # zápor: „nejde“ (jít) → „nejít“; „nedílný“ zůstává
        if t.feats.get("Degree") in ("Cmp", "Sup"):
            k += "^" + t.feats["Degree"].lower()
        return k + "|" + t.form.lower()
    return kmen(t.form)


def _shoda(klic_t, klic_v, model):
    if model:
        lt, ft = klic_t.split("|", 1)
        lv, fv = klic_v.split("|", 1)
        if lt == lv or ft == fv:
            return True
        # vidové dvojice a cizí slova, která model lemmatizuje různě (odemknout/odemykat)
        if "^" in lt or "^" in lv:
            return False
        return shoda_kmenu(kmen(lt), kmen(lv))
    return shoda_kmenu(klic_t, klic_v)


def priprav_vzory(polozky, udpipe):
    """Převede varianty na posloupnosti klíčů (lemmata s modelem, kmeny bez něj)."""
    vsechny = []
    for p in polozky:
        for v in p.varianty:
            vsechny.append((p, v))
    tokenizace = []
    if udpipe:
        text = "\n".join(_cisti(v) for _, v in vsechny)
        vety = udpipe.zpracuj(text, presegmented=True)
        if len(vety) != len(vsechny):  # pojistka: zpracuj jednotlivě
            vety = [sum(udpipe.zpracuj(_cisti(v), presegmented=True), []) for _, v in vsechny]
        tokenizace = vety
    else:
        tokenizace = [tokeny_pravidla(_cisti(v), 0, len(_cisti(v))) for _, v in vsechny]
    nepar = [f"{p.raw} → jen význam ({p.poznamka})" for p in polozky if not p.varianty]
    for (p, v), toks in zip(vsechny, tokenizace):
        vz, zvr, mez = [], "", 2
        for t in toks:
            lo = t.form.lower()
            if not t.je_slovo():
                continue
            if lo in ZASTUPCE:
                mez = 6
                continue
            if lo in ZVRATNA:
                zvr = lo
                continue
            je_prs = (t.upos == "PRON" and t.feats.get("PronType") == "Prs") if udpipe \
                else lo in OSOBNI_ZAJMENA
            if je_prs:
                mez += 1
                continue
            vz.append(VzorTok(_klic(t, bool(udpipe)), "", mez))
            mez = 2
        if vz and zvr:
            vz[0].zvratne = zvr
        obsah = [x for x in vz if not _je_stop(x.klic, True)]
        if not udpipe:
            obsah = [x for x in vz if not any(shoda_kmenu(x.klic, kmen(s)) for s in STOP)
                     and x.klic not in STOP]
        if not obsah:
            nepar.append(f"{p.raw} → „{v}“")
            continue
        p.vzory.append((v, vz))
    return nepar


def _je_stop(klic, model):
    k = klic.split("|")[0]
    if model:
        return k in STOP
    return k in STOP or any(k == kmen(x) for x in STOP)


def najdi_vzor(veta, vz, model, prisne=False):
    """Vrátí seznam (i_start, i_end) indexů tokenů věty, kde vzor sedí."""
    toks = [t for t in veta.tokens if t.je_slovo() and t.low not in ZVRATNA]
    klice = [_klic(t, model) for t in toks]
    vysl = []
    obsahove = [v for v in vz if not _je_stop(v.klic, model)]
    volitelne = len(obsahove) >= 2 and not prisne  # spojky smí chybět, když vzor má obsah
    for i in range(len(toks)):
        if not _shoda(klice[i], vz[0].klic, model):
            continue
        pos, ok, posl = i, True, i
        for v in vz[1:]:
            nasel = None
            for j in range(pos + 1, min(len(toks), pos + 2 + v.mezera)):
                if _shoda(klice[j], v.klic, model):
                    nasel = j
                    break
            if nasel is None:
                if volitelne and _je_stop(v.klic, model):
                    continue
                ok = False
                break
            pos = posl = nasel
        if not ok:
            continue
        if vz[0].zvratne:
            a, b = toks[i].idx - 3, toks[posl].idx + 3
            if not any(t.low == vz[0].zvratne and a <= t.idx <= b for t in veta.tokens):
                continue
        vysl.append((toks[i], toks[posl]))
    return vysl


# ---------------------------------------------------------------------------
# Analyzátor
# ---------------------------------------------------------------------------
class Analyza:
    def __init__(self, text, profil="blog", udpipe=None, slova_cesta=None, vse=False):
        self.profil_jm = profil
        self.p = PROFILY[profil]
        self.model = udpipe is not None
        self.vse = vse
        self.doc = Dokument(text, udpipe, vse)
        self.text = text
        self.m = self.doc.masked
        self.nalezy = []
        self.metriky = {}
        self.varovani = []
        self.udpipe = udpipe
        self.slova_cesta = slova_cesta
        self.uvozovky = [] if vse else self._uvozovky()
        self.tabulky = [(a, b) for a, b, d in self.doc.pasma if d == "tabulka"]

    # -- pomocné ----------------------------------------------------------
    # Nálezy, které platí i uvnitř citace „…“ a tabulky: uniklý citační token je chyba
    # vždy, nikdy citace.
    VZDY_PLATI = {"citacni-token"}

    def pridej(self, metrika, kategorie, zav, a, b, poznamka="", priblizne=False, zdroj=""):
        if zav is None:
            return
        if zav != "info" and kategorie not in self.VZDY_PLATI:
            pasmo = self.info_pasmo(a, b)
            if pasmo:
                zav = "info"
                poznamka += ("; " if poznamka else "") + pasmo
        self.nalezy.append(Nalez(metrika, kategorie, zav, a, b, self.text[a:b].strip(),
                                 poznamka, priblizne or (not self.model and metrika in
                                                          ("seznamy_slov", "trojice")), zdroj))

    def _uvozovky(self):
        rozsahy = []
        for m in re.finditer(r"„[^“\n]*“|‚[^‘\n]*‘|»[^«\n]*«|\"[^\"\n]*\"", self.m):
            rozsahy.append((m.start(), m.end()))
        return rozsahy

    def v_uvozovkach(self, a, b):
        return any(s <= a and b <= e for s, e in self.uvozovky)

    def info_pasmo(self, a, b):
        """Poznámka pro nález celý uvnitř citace „…“ nebo tabulky (takový nález jde do
        info: přímá řeč v AI textu je legitimní cíl, ale nemá dávat P0–P2), jinak None.
        S --vse se uvozovky ani tabulky nehledají."""
        if any(s <= a and b <= e for s, e in self.tabulky):
            return "v tabulce"
        if self.v_uvozovkach(a, b):
            return "v uvozovkách – citace?"
        return None

    def veta_na(self, pos):
        for v in self.doc.vety:
            if v.start <= pos < v.end + 1:
                return v
        return None

    # -- spuštění ---------------------------------------------------------
    def spust(self):
        self.m_typografie()
        self.m_seznamy()
        self.m_vestavene()
        self.m_kontrast()
        self.m_rytmus()
        self.m_trojice()
        self.m_privesky()
        self.m_soudrznost()
        self.m_postoj()
        self.m_titulky()
        if self.model:
            self.m_skladba()
        self._dedup()
        return self

    def _dedup(self):
        """Překrývající se nálezy ze seznamů slov: ponech nejzávažnější a nejdelší."""
        vys = []
        serazene = sorted(self.nalezy, key=lambda n: (PORADI_ZAV[n.zavaznost],
                                                      -(n.end - n.start)))
        for n in serazene:
            if n.metrika == "seznamy_slov" and any(
                    x.metrika == "seznamy_slov" and x.start < n.end and n.start < x.end
                    for x in vys):
                continue
            vys.append(n)
        self.nalezy = sorted(vys, key=lambda n: (n.start, PORADI_ZAV[n.zavaznost]))

    # -- 1 typografie -----------------------------------------------------
    def m_typografie(self):
        t, p = self.m, self.p
        slov = self.doc.pocet_slov()
        met = {}
        dlouhe = list(re.finditer("—", t))
        met["dlouha_pomlcka"] = len(dlouhe)
        for m in dlouhe:
            bez = not (m.start() > 0 and t[m.start() - 1] == " ")
            self.pridej("typografie", "dlouha-pomlcka", "P1", m.start(), m.end(),
                        "anglická dlouhá pomlčka „—“" + (" bez mezer" if bez else "") +
                        "; česky „–“ s mezerami")
        # pomlčky mezi větnými členy (ne rozsahy)
        pomlcky = []
        for m in re.finditer(r"(?<=\S) ([–-]) (?=\S)", t):
            pred = t[max(0, m.start() - 4):m.start()]
            za = t[m.end():m.end() + 2]
            if re.search(r"\d\.?$", pred) and re.match(r"\d", za):
                if m.group(1) == "-":
                    self.pridej("typografie", "rozsah", "P2", m.start() - 1, m.end() + 1,
                                "rozsah s mezerami a spojovníkem; česky bez mezer „2–3“"
                                " (s mezerami jen u data „1. 5. – 3. 5.“)")
                continue
            if not self.info_pasmo(m.start(), m.end()):
                pomlcky.append(m)  # pomlčky v citacích a tabulkách mimo rozpočet
            if m.group(1) == "-" and p["spojovnik_nalez"]:
                self.pridej("typografie", "spojovnik-misto-pomlcky", "P2", m.start(),
                            m.end(), "v textu k publikaci pomlčka „–“")
        for m in re.finditer(r"\b(\d{4}) ?- ?(\d{4})\b", t):
            if " - " not in m.group(0) and "-" in m.group(0):
                self.pridej("typografie", "rozsah", "P2", m.start(), m.end(),
                            "rozsah letopočtů s pomlčkou „–“")
        dlouhe = [m for m in dlouhe if not self.info_pasmo(m.start(), m.end())]
        met["pomlcky"] = len(pomlcky) + len(dlouhe)
        if p["pomlcky"] == "socialni":
            limit = prah("pomlcky_socialni_v_textu")
        elif p["pomlcky"] == "volne":
            limit = max(2, math.ceil(slov / 300) * 2)
        else:
            limit = max(1, math.ceil(slov / 300) * prah("pomlcky_na_300_slov"))
        met["pomlcky_limit"] = limit
        if met["pomlcky"] > limit:
            vse = sorted([m.start(1) for m in pomlcky] + [m.start() for m in dlouhe])
            self.pridej("typografie", "rozpocet-pomlcek", "P1", vse[limit], vse[limit] + 1,
                        f"{met['pomlcky']} pomlček na {slov} slov (limit {limit})")
        # uvozovky
        rovne = re.findall(r"\"[^\"\n]+\"", t)
        met["rovne_uvozovky"] = len(rovne)
        for m in re.finditer(r"\"[^\"\n]+\"", t):
            self.pridej("typografie", "rovne-uvozovky", "info", m.start(), m.end(),
                        "rovné uvozovky (slabé samo o sobě); česky „…“")
        # čísla
        for m in re.finditer(r"(?<![\d.,])(\d{1,3})((?:,\d{3})+)(?![\d,])(\s?(Kč|€|\$|CZK|EUR|USD|"
                             r"korun|eur|dolarů))?", t):
            vic = m.group(2).count(",") > 1
            if m.group(3) or vic:
                self.pridej("typografie", "oddelovac-radu", "P1", m.start(), m.end(),
                            "anglický oddělovač řádů mění význam; česky „1 500“")
            else:
                self.pridej("typografie", "oddelovac-radu", "info", m.start(), m.end(),
                            "desetinná čárka se třemi místy, nebo anglický oddělovač řádů?")
        cesky_des = re.search(r"(?<![\d,])\d+,\d{1,2}(?!\d)", t)
        anglicke = []
        for m in re.finditer(r"(?<![\d.,])(\d+)\.(\d+)(?![\d.])", t):
            a, b = m.group(1), m.group(2)
            pred = t[max(0, m.start() - 8):m.start()].lower()
            if len(b) == 2 and int(a) <= 24 and int(b) < 60:
                continue  # čas 9.00, 14.30
            if re.search(r"(verze|v|ver\.|python|ios|android)\s*$", pred):
                continue
            if len(b) == 1 or len(b) == 2 or len(b) == 3:
                anglicke.append(m)
                self.pridej("typografie", "desetinna-tecka", "P2", m.start(), m.end(),
                            "desetinná tečka; česky „2,5“")
        if anglicke and cesky_des:
            self.pridej("typografie", "smisene-formaty", "P1", anglicke[0].start(),
                        anglicke[0].end(), "v textu jsou české i anglické formáty čísel")
        for m in re.finditer(r"\b\d{1,2}/\d{1,2}/\d{2,4}\b", t):
            self.pridej("typografie", "datum", "P1", m.start(), m.end(),
                        "anglický formát data je dvojznačný; česky „4. 5. 2026“")
        for m in re.finditer(r"(?<![\d.])(\d{1,2})\.(\d{1,2})\.(\d{4})\b", t):
            if len(m.group(1)) == 1 or len(m.group(2)) == 1:
                self.pridej("typografie", "datum", "P2", m.start(), m.end(),
                            "datum bez mezer; česky „4. 5. 2026“ (v obchodní korespondenci "
                            "i „04.05.2026“)")
        for m in re.finditer(r"\b(January|February|March|April|May|June|July|August|September|"
                             r"October|November|December|Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Oct|"
                             r"Nov|Dec)\.? \d{1,2}\b", t):
            self.pridej("typografie", "datum", "P1", m.start(), m.end(), "anglický zápis data")
        for m in re.finditer(r"\b\d{1,2}(:\d{2})?\s?(AM|PM|am|pm|a\.m\.|p\.m\.)", t):
            self.pridej("typografie", "cas", "P1", m.start(), m.end(),
                        "čas AM/PM; česky „14.30“ nebo „14:30“")
        for m in re.finditer(r"\b\d{1,2}(st|nd|rd|th)\b", t):
            self.pridej("typografie", "radova-cislovka", "P1", m.start(), m.end(),
                        "anglická řadová číslovka; česky „1.“")
        for m in re.finditer(r"(\d+)%(?=(\s+([^\W\d_]+))|[^\w]|$)", t):
            dalsi = m.group(3)
            zav = "P2"
            pozn = "procenta jako podstatné jméno píšou s mezerou: „25 %“"
            if dalsi and dalsi[0].islower():
                if self.model:
                    v = self.veta_na(m.start())
                    tok = None
                    if v:
                        za = [x for x in v.tokens if x.start >= m.end() and x.je_slovo()]
                        tok = za[0] if za else None
                    if tok is not None and tok.upos in ("NOUN", "ADJ"):
                        continue  # „25% sleva“ = pětadvacetiprocentní
                else:
                    zav = "info"
                    pozn += " (bez modelu nelze odlišit „25% sleva“)"
            self.pridej("typografie", "procenta", zav, m.start(), m.end() + 1, pozn)
        # vykřičníky, emoji, hashtagy
        vykr_poz = [i for i, ch in enumerate(t) if ch == "!" and not self.info_pasmo(i, i + 1)]
        vykr = len(vykr_poz)
        met["vykricniky"] = vykr
        if p["vykricniky"] and slov and vykr >= 2 and vykr * 1000 / slov > prah(
                "vykricniky_na_1000_slov"):
            i = vykr_poz[0]
            self.pridej("typografie", "vykricniky", "P2", i, i + 1,
                        f"{vykr} vykřičníků na {slov} slov")
        emoji = list(RE_EMOJI.finditer(t))
        met["emoji"] = len(emoji)
        if len(emoji) > p["emoji"]:
            m = emoji[p["emoji"]]
            self.pridej("typografie", "emoji", "P2", m.start(), m.end(),
                        f"{len(emoji)} emoji (profil {self.profil_jm} snese {p['emoji']})")
        hasht = list(re.finditer(r"(?<!\w)#[^\W\d_]\w+", t))
        met["hashtagy"] = len(hasht)
        if len(hasht) >= prah("hashtagy"):
            self.pridej("typografie", "hashtagy", "P1", hasht[0].start(), hasht[-1].end(),
                        f"{len(hasht)} hashtagů")
        for m in re.finditer(r"↓|👇", t):
            self.pridej("typografie", "hacek-sipka", "P1", m.start(), m.end(),
                        "háček se šipkou")
        self.metriky["typografie"] = met

    # -- 3 seznamy slov ---------------------------------------------------
    def m_seznamy(self):
        cesta = self.slova_cesta
        if not cesta or not os.path.exists(cesta):
            self.varovani.append(f"slova.md nenalezen ({cesta}); seznamy slov přeskočeny")
            self.metriky["seznamy_slov"] = {"nacteno": 0}
            return
        polozky, var = nacti_slova(cesta)
        self.varovani += var
        nepar = priprav_vzory(polozky, self.udpipe)
        p = self.p
        nalezy_l2 = {}   # blok -> {raw: (a,b,polozka)}
        nalezy_l3 = {}
        pocty = {}
        prechody = []    # (a, b, zav, pozn, raw, polozka): jeden v textu P2, dva a víc P1
        prvni_ve_bloku = {}
        for v in self.doc.vety:
            prvni_ve_bloku.setdefault(v.blok, v.start)
        for pol in polozky:
            if pol.tech and p["tech_vyjimky"]:
                continue
            if pol.sekce == "uredni" and not p["uredni"]:
                continue
            if pol.sekce == "jmenny" and not p["jmenny_styl"]:
                continue
            for v in self.doc.vety:
                for var, vz in pol.vzory:
                    for t0, t1 in najdi_vzor(v, vz, self.model, pol.sekce == "chatbot"):
                        a, b = t0.start, t1.end
                        if pol.privesek:
                            pred = self.m[max(v.start, a - 40):a].lower()
                            if not re.search(r"\b(což|čímž|tím)\b[^.]*$", pred):
                                continue
                        pocty[pol.sekce] = pocty.get(pol.sekce, 0) + 1
                        zav = pol.zavaznost
                        if pol.sekce in ("uroven2", "uroven3"):
                            # jedno slovo, které odpovídá dvěma položkám (efektivní,
                            # efektivně), se počítá jednou
                            cil = nalezy_l2 if pol.sekce == "uroven2" else nalezy_l3
                            bl = cil.setdefault(v.blok, {})
                            if not any(x[0] < b and a < x[1] for x in bl.values()):
                                bl.setdefault(pol.raw, (a, b, pol))
                            continue
                        if pol.podminka and zav in ("P1", "P2") and pol.sekce != "chatbot":
                            zav = "P2" if zav == "P1" else "info"
                        if pol.sekce == "kalk" and zav == "P2" and len(var.split()) >= 3 \
                                and not pol.podminka:
                            zav = "P1"
                        pozn = pol.kategorie
                        if pol.poznamka:
                            pozn += f" ({pol.poznamka})"
                        if pol.sekce == "fraze" and pol.kategorie == "uvod" and zav == "P1" \
                                and prvni_ve_bloku.get(v.blok) != v.start:
                            zav, pozn = "P2", pozn + "; uprostřed odstavce"
                        if self.v_uvozovkach(a, b):
                            zav, pozn = "info", pozn + "; v uvozovkách – citace?"
                        zav = self._filtr_profilu(zav, pol)
                        if pol.sekce == "fraze" and pol.kategorie == "prechod" and zav == "P1":
                            prechody.append((a, b, pozn, pol))
                            continue
                        self.pridej("vestavene" if pol.sekce == "vagni" else "seznamy_slov",
                                    self._kat_seznamu(pol), zav, a, b, pozn,
                                    zdroj=f"slova.md: {pol.raw}")
        ruzne = {pol.raw for *_, pol in prechody}
        for a, b, pozn, pol in prechody:
            zav = "P1" if len(ruzne) >= prah("prechody_p1") else "P2"
            self.pridej("seznamy_slov", self._kat_seznamu(pol), zav, a, b,
                        pozn + f"; přechodů v textu: {len(ruzne)}", zdroj=f"slova.md: {pol.raw}")
        slov_v_bloku = {}
        for v in self.doc.vety:
            slov_v_bloku[v.blok] = slov_v_bloku.get(v.blok, 0) + v.pocet_slov()
        for blok, nal in nalezy_l2.items():
            hranice = prah("uroven2_v_dlouhem_odstavci") if slov_v_bloku.get(blok, 0) > \
                prah("uroven2_dlouhy_odstavec_slov") else prah("uroven2_v_odstavci")
            zav = "P1" if len(nal) >= hranice else "info"
            for raw, (a, b, pol) in nal.items():
                z = self._filtr_profilu(zav, pol)
                if self.v_uvozovkach(a, b):
                    z = "info"
                self.pridej("seznamy_slov", "uroven-2", z, a, b,
                            f"úroveň 2: {len(nal)} různých v odstavci (práh {hranice})" +
                            (f"; {pol.poznamka}" if pol.poznamka else ""),
                            zdroj=f"slova.md: {raw}")
        for blok, nal in nalezy_l3.items():
            zav = "P2" if len(nal) >= prah("uroven3_v_odstavci") else "info"
            for raw, (a, b, pol) in nal.items():
                z = self._filtr_profilu(zav, pol)
                self.pridej("seznamy_slov", "uroven-3", z, a, b,
                            f"úroveň 3: {len(nal)} různých v odstavci (práh "
                            f"{prah('uroven3_v_odstavci')})", zdroj=f"slova.md: {raw}")
        self.metriky["seznamy_slov"] = {"polozek": len(polozky),
                                        "vzoru": sum(len(x.vzory) for x in polozky),
                                        "neparovatelne": nepar, "vyskyty": pocty}

    def _kat_seznamu(self, pol):
        if pol.sekce == "uroven1":
            return "uroven-1"
        if pol.sekce == "fraze":
            return "fraze-" + pol.kategorie
        if pol.sekce == "vagni":
            return "vagni-autorita"
        return pol.sekce

    def _filtr_profilu(self, zav, pol):
        p = self.p
        if p["seznamy"] == "p0p1":
            if pol.sekce in ("uroven2", "uroven3") or (pol.sekce == "kalk" and zav != "P1"):
                return "info"
        return zav

    # -- vestavěné P0 (návrh doplnit do slova.md) --------------------------
    def m_vestavene(self):
        t = self.m
        # uniklé citační tokeny hledá v původním textu: jsou chybou i v kódu a v URL
        for m in re.finditer(r"oaicite|contentReference|turn\d+search\d+|utm_source=chatgpt\.com"
                             r"|:contentReference\[", self.text):
            self.pridej("vestavene", "citacni-token", "P0", m.start(), m.end(),
                        "uniklý citační token")
        for m in re.finditer(r"\[(?!OVĚŘIT)(Jméno|Název|Firma|Datum|Doplnit|Vaše jméno|jméno|"
                             r"název|firma|datum|doplnit|Your Name|Name)[^\]]*\]", t):
            self.pridej("vestavene", "zastupny-text", "P0", m.start(), m.end(),
                        "nevyplněný zástupný text")
        for m in re.finditer(r"(?i)\b(ignoruj|ignorujte|zapomeň|zapomeňte|nedbej)\b[^.\n]{0,40}?"
                             r"\b(pravidl|pokyn|instrukc|výše|předchozí)\w*|\bignore (all )?"
                             r"(previous|prior|above)\b", t):
            self.pridej("vestavene", "vlozeny-pokyn", "P0", m.start(), m.end(),
                        "pokyn vložený do kontrolovaného textu – označit, neplnit")
        for m in re.finditer(r"(?i)\b(studie|výzkumy|průzkumy|odborníci|experti|vědci)\s+"
                             r"(ukazují|ukazuje|dokazují|potvrzují|tvrdí|se shodují|"
                             r"naznačují|zjistili|prokázali)\b|\b(podle|dle)\s+(odborníků|"
                             r"expertů|vědců|studií|výzkumů)\b|\bje\s+(vědecky\s+)?"
                             r"(prokázáno|dokázáno)\b", t):
            if any(n.kategorie == "vagni-autorita" and n.start < m.end() and m.start() < n.end
                   for n in self.nalezy):
                continue
            citace = self.v_uvozovkach(m.start(), m.end())
            self.pridej("vestavene", "vagni-autorita", "info" if citace else "P0", m.start(),
                        m.end(), "vágní autorita bez zdroje (neplatí, když hned následuje "
                                 "pojmenovaný zdroj)" + ("; v uvozovkách – citace?" if citace
                                                         else ""))
        for m in re.finditer(r"\[OVĚŘIT[^\]]*\]", t):
            self.pridej("vestavene", "znacka-overit", "info", m.start(), m.end(),
                        "značka skillu pro chybějící fakt")
        if self.p["odhaleni"]:
            vety = self.doc.prozni_vety()
            for i, v in enumerate(vety):
                n = v.pocet_slov()
                txt = v.text.strip()
                puvodni = self.text[v.start:v.end]
                if "`" in puvodni or "**" in puvodni:
                    continue  # kód nebo formátovaný štítek, ne inscenovaná pauza
                dalsi = vety[i + 1] if i + 1 < len(vety) else None
                bez_slovesa = not any(t.upos in ("VERB", "AUX") for t in v.tokens) \
                    if self.model else n <= 3
                if txt.endswith("?") and n <= 4 and bez_slovesa and dalsi and \
                        dalsi.blok == v.blok and dalsi.pocet_slov() <= 8 and \
                        not re.search(r"[\"„“”»«]", txt + dalsi.text):
                    self.pridej("vestavene", "otazka-s-odpovedi", "P1", v.start, v.end,
                                "otázka s okamžitou odpovědí inscenuje pauzu")
                m = re.match(r"^([^\W\d_]+(?:\s+[^\W\d_]+){0,2}):\s+(.+)$", txt)
                if m and n <= 8 and not re.search(r"\d", m.group(2)) and \
                        not re.match(r"[„\"“»‚']", m.group(2)):  # dvojtečka před citací
                    self.pridej("vestavene", "dvojteckove-odhaleni", "P1", v.start, v.end,
                                "dvojtečkové odhalení; dvojtečka před výčtem nebo citací "
                                "je v pořádku")

    # -- 2 rytmus ---------------------------------------------------------
    def m_rytmus(self):
        vety = self.doc.prozni_vety()
        delky = [v.pocet_slov() for v in vety]
        met = {"vet": len(delky)}
        if delky:
            met["prumer"] = round(statistics.mean(delky), 1)
            met["median"] = statistics.median(delky)
            met["min"], met["max"] = min(delky), max(delky)
        if len(delky) >= 2:
            sd = statistics.pstdev(delky)
            met["smerodatna_odchylka"] = round(sd, 1)
            met["variacni_koeficient"] = round(sd / met["prumer"], 2) if met["prumer"] else 0
        met["delky"] = delky
        # věty oddělené blokem mimo měření (kód, citace, tabulka) nejsou sousední
        predel = [False] + [self.doc.preruseno(vety[k - 1].end, vety[k].start)
                            for k in range(1, len(vety))]
        # běhy podobné délky
        behy = []
        if len(delky) >= 3:
            tol = max(prah("rytmus_podobna_delka_slov"),
                      round(prah("rytmus_podobna_delka_podil") * statistics.mean(delky)))
            i = 0
            while i < len(delky):
                j = i + 1
                while j < len(delky) and max(delky[i:j + 1]) - min(delky[i:j + 1]) <= tol \
                        and delky[j] > 3 and not predel[j]:
                    j += 1
                if j - i >= 3 and delky[i] > 3:
                    behy.append((i, j))
                    i = j
                else:
                    i += 1
        met["behy_podobne_delky"] = [[a, b - a] for a, b in behy]
        # řetězy krátkých vět
        kr = prah("kratka_veta_slov")
        retezy = []
        i = 0
        while i < len(delky):
            j = i
            while j < len(delky) and delky[j] <= kr and (j == i or not predel[j]):
                j += 1
            if j - i >= prah("retez_kratkych_vet"):
                retezy.append((i, j))
            i = max(j, i + 1)
        met["retezy_kratkych_vet"] = [[a, b - a] for a, b in retezy]
        # heslovitá kadence
        hesla = []
        for i, v in enumerate(vety):
            txt = v.text.strip()
            n = delky[i]
            cis = re.match(rf"(?i)^{CISLOVKY_SLOVY}\s+[^\W\d_]+,\s+{CISLOVKY_SLOVY}\s+[^\W\d_]+[.!]?$",
                           txt)
            je = False
            if cis:
                je = "par"
            elif n <= prah("heslo_slov") and not txt.endswith("?") and \
                    not re.search(r"[\"„“”»«]", txt) and \
                    not any(a <= v.start and v.end <= b for a, b in self._kontrast_rozsahy):
                if self.model:
                    je = not any(t.upos in ("VERB", "AUX") for t in v.tokens)
                else:
                    je = True
            hesla.append(je)
        mista, i = 0, 0
        while i < len(hesla):
            if hesla[i] == "par":
                mista += 1
                i += 1
                continue
            if hesla[i]:
                j = i
                while j < len(hesla) and hesla[j] is True:
                    j += 1
                mista += math.ceil((j - i) / 2) if j - i >= 2 else 0
                i = j
            else:
                i += 1
        met["heslovita_mista"] = mista
        self.metriky["rytmus"] = met
        if mista >= prah("heslovita_kadence_mist") and self.p["odhaleni"]:
            prvni = next(k for k, h in enumerate(hesla) if h)
            self.pridej("rytmus", "heslovita-kadence", "P1", vety[prvni].start, vety[-1].end,
                        f"{mista} heslovitých míst v textu (práh "
                        f"{prah('heslovita_kadence_mist')})")
        if not self.p["rytmus"]:
            return
        for a, b in behy:
            zav = "P2" if b - a >= prah("rytmus_beh_p2") else "info"
            self.pridej("rytmus", "podobna-delka", zav, vety[a].start, vety[b - 1].end,
                        f"{b - a} vět za sebou o délce {delky[a:b]} slov")
        if len(delky) >= prah("rytmus_cv_min_vet") and \
                met.get("variacni_koeficient", 1) < prah("rytmus_cv_min"):
            self.pridej("rytmus", "jednotvarny-rytmus", "P2", vety[0].start, vety[-1].end,
                        f"variační koeficient délky vět {met['variacni_koeficient']} "
                        f"(práh {prah('rytmus_cv_min')})")
        if self.p["kratke_vety"]:
            for a, b in retezy:
                self.pridej("rytmus", "retez-kratkych-vet", "P2", vety[a].start,
                            vety[b - 1].end, f"{b - a} vět za sebou do {kr} slov")

    # -- 4 kontrastní obraty ---------------------------------------------
    def m_kontrast(self):
        vety = [v for v in self.doc.vety if v.druh in ("veta", "titulek")]
        texty = [v.text.lower() for v in vety]
        nalezy = []
        neg_a = re.compile(r"\b(?:nejde|nešlo|nepůjde|nejedná se|nejednalo se|nešlo by)"
                           r"(?:\s+(?:tu|už|jen|přece|vůbec|tolik))?\s+o\b")
        poz_a = re.compile(r"^(?:ale\s+|a\s+)?(?:jde|šlo|půjde|jedná se|jednalo se)"
                           r"(?:\s+(?:tu|hlavně|především|spíš|o to))?\s+o\b")
        neg_b = re.compile(r"\b(?:není|nebylo|nebude)\s+to\b")
        poz_b = re.compile(r"^(?:ale\s+)?(?:je|bylo|bude)\s+to\b|^to\s+je\b")
        i = 0
        while i < len(vety):
            t = texty[i]
            m = neg_a.search(t)
            if m:
                if re.search(r",\s*(?:ale|nýbrž)\s+(?:(?:jde|šlo)\s+)?o\b", t[m.end():]):
                    nalezy.append((vety[i].start, vety[i].end, "nejde o X, ale o Y", "A"))
                    i += 1
                    continue
                negs, j = 1, i + 1
                while j < len(vety) and j <= i + 3 and neg_a.search(texty[j]) and \
                        not poz_a.search(texty[j]):
                    negs += 1
                    j += 1
                if j < len(vety) and poz_a.search(texty[j]):
                    pozn = "nejde o X. Jde o Y." + (" s nahromaděnými zápory" if negs > 1
                                                    else "")
                    nalezy.append((vety[i].start, vety[j].end, pozn, "A"))
                    i = j + 1
                    continue
            m = neg_b.search(t)
            if m:
                if re.search(r",\s*(?:ale\s+|nýbrž\s+)?(?:je|bylo|bude)\s+to\b", t[m.end():]):
                    nalezy.append((vety[i].start, vety[i].end, "není to X, je to Y", "B"))
                    i += 1
                    continue
                if i + 1 < len(vety) and poz_b.search(texty[i + 1]):
                    nalezy.append((vety[i].start, vety[i + 1].end, "není to X. Je to Y.", "B"))
                    i += 2
                    continue
            m = re.search(r"\bnejen\b.{1,120}?\b(?:ale|nýbrž|alebrž)\b(?:\s+(?:i|také|taky|"
                          r"zároveň|hlavně))?", t)
            if m:
                nalezy.append((vety[i].start + m.start(), vety[i].start + m.end(),
                               "nejen X, ale i Y", "C"))
            if (vety[i].druh == "titulek" or vety[i].pocet_slov() <= 5) and \
                    re.match(r"^[^\W\d_]+(?:\s+[^\W\d_]+)?\s+místo\s+[^\W\d_]+(?:\s+[^\W\d_]+)?"
                             r"[.!]?$", t.strip()):
                nalezy.append((vety[i].start, vety[i].end, "zkrácené „A místo B“", "D"))
            i += 1
        celkem = len(nalezy)
        self._kontrast_rozsahy = [(a, b) for a, b, _, _ in nalezy]
        self.metriky["kontrast"] = {"pocet": celkem}
        for a, b, pozn, typ in nalezy:
            if typ in ("A", "B", "D"):
                zav = "P1"
            else:
                zav = "P1" if celkem > prah("kontrast_na_text") else "P2"
            if celkem > prah("kontrast_na_text"):
                pozn += f"; {celkem} kontrastní obraty v textu (limit "\
                        f"{prah('kontrast_na_text')})"
            elif typ == "C":
                pozn += "; posuď, zda jde o řečnickou figuru"
            self.pridej("kontrast", "kontrastni-obrat", zav, a, b, pozn)

    # -- 5 trojice --------------------------------------------------------
    def m_trojice(self):
        slovnik = self._slovnik_klicu()
        pocet, prid = 0, []
        vys = []
        for v in self.doc.vety:
            for m in re.finditer(r"(?<!, )(?<!,)\b([^\W\d_]+), ([^\W\d_]+) (a|i|či|nebo|"
                                 r"ani) ([^\W\d_]+)\b(?!,? [^\W\d_]+,)", v.text):
                a, b = v.start + m.start(), v.start + m.end()
                pred = self.m[max(0, a - 3):a]
                if re.search(r",\s?$", pred):
                    continue  # delší výčet
                clenove = [m.group(1), m.group(2), m.group(4)]
                if any(c.lower() in NEJSOU_CLENY for c in clenove):
                    continue
                upos = None
                if self.model:
                    toks = []
                    for c, g in ((clenove[0], 1), (clenove[1], 2), (clenove[2], 4)):
                        s = v.start + m.start(g)
                        tk = next((t for t in v.tokens if t.start == s), None)
                        toks.append(tk)
                    if None in toks:
                        continue
                    uposy = {t.upos for t in toks}
                    if len(uposy) != 1:
                        continue
                    upos = uposy.pop()
                    if upos in ("PROPN", "NUM", "PRON", "DET"):
                        continue
                    klice = [_klic(t, True) for t in toks]
                else:
                    klice = [kmen(c) for c in clenove]
                ze_slovniku = [c for c, k in zip(clenove, klice) if self._ve_slovniku(k, slovnik)]
                pocet += 1
                vys.append((a, b, upos, ze_slovniku))
                if upos in ("ADJ", "ADV"):
                    prid.append(a)
        for a, b, upos, zs in vys:
            if zs:
                zav = "P1"
                pozn = "ozdobná trojice: " + ", ".join(zs) + " ze seznamu slov"
            elif upos in ("ADJ", "ADV"):
                zav = "P1" if len(prid) > prah("trojice_prid_jmen_na_text") else "P2"
                pozn = f"trojice přídavných jmen/příslovcí ({len(prid)} v textu, limit " \
                       f"{prah('trojice_prid_jmen_na_text')})"
            elif pocet >= 3:
                zav = "P2"
                pozn = f"{pocet} trojic v textu"
            else:
                zav = "info"
                pozn = "trojice; zůstává, když má obsah tři části"
            if upos:
                pozn += f" [{upos}]"
            self.pridej("trojice", "trojice", zav, a, b, pozn)
        self.metriky["trojice"] = {"pocet": pocet, "pridavna_jmena": len(prid)}

    def _slovnik_klicu(self):
        if not hasattr(self, "_slovnik"):
            self._slovnik = []
            if self.slova_cesta and os.path.exists(self.slova_cesta):
                polozky, _ = nacti_slova(self.slova_cesta)
                polozky = [p for p in polozky if p.sekce in ("uroven1", "uroven2")]
                priprav_vzory(polozky, self.udpipe)
                for p in polozky:
                    if p.tech and self.p["tech_vyjimky"]:
                        continue
                    for _, vz in p.vzory:
                        if len(vz) == 1:
                            self._slovnik.append(vz[0].klic)
        return self._slovnik

    def _ve_slovniku(self, k, slovnik):
        return any(_shoda(k, s, self.model) for s in slovnik)

    # -- 6 přívěsky -------------------------------------------------------
    def m_privesky(self):
        vety = len(self.doc.prozni_vety()) or 1
        pr = list(re.finditer(r",\s*(což|čímž|a\s+tím)\b", self.m, flags=re.I))
        na100 = len(pr) * 100 / vety
        self.metriky["privesky"] = {"pocet": len(pr), "na_100_vet": round(na100, 1)}
        for m in pr:
            za = self.m[m.end():m.end() + 40].lower()
            obecne = re.match(r"\s+(?:\w+\s+){0,2}?(přispív|zajišť|umožň|posil|demonstr|"
                              r"dokazuj|svědč|podtrh|zdůrazň|odráž|přináš|vytváří)\w*", za)
            if obecne:
                self.pridej("privesky", "privesek", "P2", m.start(), m.end() + len(obecne.group(0)),
                            "přívěsek s obecným slovesem; škrtni, nebo z něj udělej větu "
                            "s doloženým faktem")
        if len(pr) >= 2 and na100 > prah("privesky_na_100_vet"):
            self.pridej("privesky", "privesky-cetnost", "P2", pr[0].start(), pr[0].end(),
                        f"{len(pr)} přívěsků s což/čímž/a tím, {na100:.1f} na 100 vět "
                        f"(práh {prah('privesky_na_100_vet')})")

    # -- 7 soudržnost -----------------------------------------------------
    def m_soudrznost(self):
        vety = self.doc.prozni_vety()
        zac = []
        for v in vety:
            t = v.text.strip().lower()
            t = re.sub(r"^(a|ale)\s+", "", t)
            k = next((x for x in KONEKTORY if re.match(rf"{x}\b", t)), None)
            zac.append(k)
        pocet = sum(1 for k in zac if k and k not in KONEKTORY_JEN_RETEZ)
        na100 = pocet * 100 / (len(vety) or 1)
        slov = self.doc.pocet_slov() or 1
        if self.model:
            ktery = sum(1 for t in self.doc.slova() if t.lemma == "který")
        else:
            ktery = len(re.findall(r"(?i)\b(kter[ýáéíou]\w*)\b", self.m))
        coz = len(re.findall(r",\s*což\b", self.m, flags=re.I))
        self.metriky["soudrznost"] = {
            "konektory_na_zacatku": pocet, "na_100_vet": round(na100, 1),
            "vyskyty": {k: zac.count(k) for k in set(zac) if k},
            "ktery_na_1000_slov": round(ktery * 1000 / slov, 1),
            "coz_na_100_vet": round(coz * 100 / (len(vety) or 1), 2),
            "reference": {k: REFERENCE[k] for k in ("ktery_na_1000_slov", "coz_na_100_vet")},
            "poznamka": "který a což jen informativně; navíc a dále se do četnosti nepočítají",
        }
        # ukazovací „tento“ na začátku věty jen jako hodnota; nález dává metrika skladby
        uk = [v for v in vety if v.slova() and v.slova()[0].low in TVARY_TENTO]
        self.metriky["soudrznost"]["tento_na_zacatku_podil_vet"] = round(
            len(uk) / (len(vety) or 1), 3)

        # v neposlední řadě kdekoli
        for m in re.finditer(r"(?i)\bv neposlední řadě\b", self.m):
            self.pridej("soudrznost", "prechod", "P1", m.start(), m.end(),
                        "šablonovitý přechod")
        # řetěz tří vět s konektorem
        i = 0
        while i < len(zac):
            j = i
            while j < len(zac) and zac[j]:
                j += 1
            if j - i >= prah("konektory_retez"):
                self.pridej("soudrznost", "konektory-retez", "P1", vety[i].start,
                            vety[j - 1].end, f"{j - i} věty za sebou začínají spojovacím "
                                             f"výrazem")
            i = max(j, i + 1)
        nic = [i for i, k in enumerate(zac) if k == "nicméně"]
        if len(nic) >= prah("nicmene_rituál"):
            v = vety[nic[1]]
            self.pridej("soudrznost", "nicmene", "P2", v.start, v.start + 8,
                        f"„Nicméně“ na začátku {len(nic)} vět")
        if pocet >= 3 and na100 > prah("konektory_na_100_vet"):
            v = vety[next(i for i, k in enumerate(zac) if k)]
            self.pridej("soudrznost", "konektory-cetnost", "P2", v.start, v.end,
                        f"{pocet} vět začíná spojovacím výrazem, {na100:.1f} na 100 vět "
                        f"(práh {prah('konektory_na_100_vet')})")

    # -- 8 postoj a oslovení (jen informativně) ----------------------------
    def m_postoj(self):
        slova = self.doc.slova()
        n = len(slova) or 1
        if self.model:
            os1 = sum(1 for t in slova if t.feats.get("Person") == "1")
            os2 = sum(1 for t in slova if t.feats.get("Person") == "2")
        else:
            os1 = sum(1 for t in slova if t.low in ZAJMENA_1OS or
                      re.search(r"(?:ujeme|íme|áme|eme|jsme|ím|uji|ám)$", t.low) and False)
            os2 = sum(1 for t in slova if t.low in ZAJMENA_2OS)
        cast = {}
        for c in CASTICE:
            k = sum(1 for t in slova if t.low == c)
            if k:
                cast[c] = k
        modalni = sum(1 for t in slova if t.low in MODALNI)
        oslab = sum(1 for t in slova if t.low in OSLABUJICI)
        zaj2 = sum(1 for t in slova if t.low in ZAJMENA_2OS)
        vety = self.doc.prozni_vety()
        otazky = sum(1 for v in vety if v.text.rstrip().endswith("?"))
        self.metriky["postoj"] = {
            "osoba1": os1, "osoba2": os2, "osoba1_na_100_slov": round(os1 * 100 / n, 2),
            "osoba2_na_100_slov": round(os2 * 100 / n, 2), "castice": cast,
            "castice_na_100_slov": round(sum(cast.values()) * 100 / n, 2),
            "modalni_na_1000_slov": round(modalni * 1000 / n, 1),
            "oslabujici_na_1000_slov": round(oslab * 1000 / n, 1),
            "osoba2_zajmena_na_1000_slov": round(zaj2 * 1000 / n, 1),
            "otazniky_na_100_vet": round(otazky * 100 / (len(vety) or 1), 1),
            "reference": {k: REFERENCE[k] for k in (
                "modalni_na_1000_slov", "oslabujici_na_1000_slov",
                "osoba2_zajmena_na_1000_slov", "otazniky_na_100_vet")},
            "poznamka": "jen informativně: AI v češtině má zhruba polovinu lidské hodnoty; "
                        "přepis ji nemá snižovat ani uměle zvyšovat",
        }
        # konkrétnost (D6): čísla a vlastní jména
        cisla = sum(1 for t in slova if re.search(r"\d", t.form))
        if self.model:
            jmena = sum(1 for t in slova if t.upos == "PROPN")
        else:
            jmena = sum(1 for v in self.doc.vety for t in v.slova()[1:]
                        if t.form[:1].isupper() and not t.form.isupper())
        self.metriky["konkretnost"] = {
            "cisla_na_1000_slov": round(cisla * 1000 / n, 1),
            "vlastni_jmena_na_1000_slov": round(jmena * 1000 / n, 1),
            "reference": {k: REFERENCE[k] for k in ("cisla_na_1000_slov",
                                                     "vlastni_jmena_na_1000_slov")},
            "priblizne": not self.model,
            "poznamka": "jen informativně; přepis nesmí čísla ani jména ubrat",
        }

    # -- titulky (návrh) --------------------------------------------------
    def m_titulky(self):
        for v in self.doc.vety:
            if v.druh != "titulek":
                continue
            txt = v.text.strip().rstrip(".")
            slova = [m for m in RE_SLOVO.finditer(txt)]
            if len(slova) >= 3 and not txt.isupper():
                dalsi = slova[1:]
                if self.model:
                    propn = {t.start - v.start for t in v.tokens if t.upos == "PROPN"}
                else:
                    propn = set()
                velka = [s for s in dalsi if s.group(0)[0].isupper() and s.start() not in propn]
                mala_obsah = [s for s in dalsi if s.group(0)[0].islower() and len(s.group(0)) > 2]
                if len(velka) >= 2 and len(velka) >= len(dalsi) * 2 / 3 and not mala_obsah:
                    self.pridej("typografie", "title-case", "P1", v.start, v.end,
                                "anglický title case; česky velké jen první písmeno a vlastní "
                                "jména")
            lo = txt.lower()
            if re.fullmatch(r"(úvod|přehled|závěr|závěrem|shrnutí|klíčové poznatky.*|"
                            r"co si odnést|další kroky)", lo):
                self.pridej("titulky", "sablonovity-titulek", "P2", v.start, v.end,
                            "šablonovitý titulek; pojmenuj obsah")
            elif re.match(r"(co|jak|proč|kdo|kde|kdy|takhle|takto|tohle|pohled na|"
                          r"představení|pojďme|podívejme)\b", lo):
                self.pridej("titulky", "upoutavkovy-titulek", self.p["titulky_upoutavka"],
                            v.start, v.end, "upoutávkový nebo hovorový titulek; jmenné spojení "
                                            "pojmenuje obsah")

    # -- 9 skladba (jen s modelem) -----------------------------------------
    def m_skladba(self):
        vety = self.doc.prozni_vety()
        slova = sum(v.pocet_slov() for v in vety) or 1
        vnoun, opisne, zvratne = [], [], []
        jmenne_vety = 0
        for v in vety:
            vn = [t for t in v.tokens if self._je_vnoun(t)]
            op = [t for t in v.tokens if t.deprel == "aux:pass"]
            zv = [t for t in v.tokens if t.deprel == "expl:pass"]
            dojit = any(t.lemma == "dojít" for t in v.tokens) and vn
            vnoun += vn
            opisne += op
            zvratne += zv
            if len(vn) >= 2 or op or dojit:
                jmenne_vety += 1
        n = len(vety) or 1
        na1000 = len(vnoun) * 1000 / slova
        podil = jmenne_vety / n
        met = {"slovesna_substantiva": len(vnoun),
               "slovesna_substantiva_na_1000_slov": round(na1000, 1),
               "opisne_pasivum": len(opisne), "zvratne_pasivum": len(zvratne),
               "jmenne_vety": jmenne_vety, "jmenne_vety_podil": round(podil, 2),
               "poznamka_vnoun": "model UD 2.5 neznačí VerbForm=Vnoun; odhad: neutrum "
                                 "s lemmatem na -ní/-tí"}
        if self.p["jmenny_styl"] or self.p["pasivum"]:
            if len(vety) >= 2 and podil > prah("jmenne_vety_podil_p1") and \
                    self.p["jmenny_styl"] and self.p["pasivum"]:
                self.pridej("skladba", "jmenny-styl", "P1", vety[0].start, vety[-1].end,
                            f"jmenný styl nebo opisné pasivum ve {jmenne_vety} z {len(vety)} vět")
            elif self.p["jmenny_styl"] and len(vnoun) >= 3 and \
                    na1000 > prah("slovesna_subst_na_1000_slov"):
                self.pridej("skladba", "jmenny-styl", "P2", vnoun[0].start, vnoun[-1].end,
                            f"{len(vnoun)} slovesných substantiv, {na1000:.0f} na 1 000 slov "
                            f"(práh {prah('slovesna_subst_na_1000_slov')})")
        if self.p["pasivum"]:
            podil_op = sum(1 for v in vety if any(t.deprel == "aux:pass" for t in v.tokens)) / n
            met["opisne_pasivum_podil_vet"] = round(podil_op, 2)
            if len(opisne) >= prah("opisne_pasivum_p2") and \
                    podil_op > prah("opisne_pasivum_podil_p2"):
                for t in opisne:
                    self.pridej("skladba", "opisne-pasivum", "P2", t.start, t.end + 12,
                                "opisné pasivum: pojmenuj aktéra, když ho zdroj zná")
            else:
                for t in opisne:
                    self.pridej("skladba", "opisne-pasivum", "info", t.start, t.end,
                                "opisné pasivum ojediněle je slabé samo o sobě")
        # podmětová zájmena a svůj
        po_vetach = []
        for v in vety:
            po_vetach.append([t for t in v.tokens if (
                t.deprel.startswith("nsubj") and t.upos == "PRON" and
                t.feats.get("PronType") == "Prs" and t.feats.get("Reflex") != "Yes")
                or t.lemma == "svůj"])
        self._zajmena_v_rade(po_vetach, met, False)
        # ukazovací zájmena na začátku vět
        uk = [v for v in vety if v.tokens and v.tokens[0].lemma == "tento"]
        met["ukazovaci_na_zacatku"] = len(uk)
        if len(uk) >= prah("ukazovaci_zacatky") and len(uk) / n >= prah("ukazovaci_zacatky_podil"):
            for v in uk:
                self.pridej("skladba", "ukazovaci-ritual", "P2", v.tokens[0].start,
                            v.tokens[0].end, f"{len(uk)} vět začíná tvarem „tento“")
        # příklonky za slovesem
        for v in vety:
            for t in v.tokens:
                if t.low in POMOCNE_PRIKLONKY and t.deprel.startswith("aux") and t.head:
                    h = v.tokens[t.head - 1] if t.head - 1 < len(v.tokens) else None
                    if not h or h.upos != "VERB" or h.idx >= t.idx or h.idx == 0:
                        continue
                    pred = v.tokens[h.idx - 1]
                    if pred.upos in ("PUNCT", "CCONJ", "SCONJ") or \
                            pred.feats.get("PronType") in ("Rel", "Int"):
                        continue
                    self.pridej("skladba", "priklonka", "P1", h.start, t.end,
                                "příklonka patří za první větný člen („Tento problém jsme "
                                "řešili“)")
        self.metriky["skladba"] = met

    def _je_vnoun(self, t):
        if t.feats.get("VerbForm") == "Vnoun":
            return True
        lem = t.lemma.lower()
        return (t.upos == "NOUN" and t.feats.get("Gender") == "Neut" and
                (lem.endswith("ní") or lem.endswith("tí")) and len(lem) >= 5 and
                lem not in VNOUN_NEJSOU)

    def _zajmena_v_rade(self, po_vetach, met, priblizne):
        """Podmětová zájmena a „svůj“ v řadě: součet ve dvou po sobě jdoucích větách."""
        met["podmetova_zajmena_a_svuj"] = sum(len(x) for x in po_vetach)
        okno = 0
        hit = set()
        for i in range(len(po_vetach)):
            o = po_vetach[i] + (po_vetach[i + 1] if i + 1 < len(po_vetach) else [])
            okno = max(okno, len(o))
            if len(o) >= prah("zajmena_podmet_svuj_okno"):
                hit.update(id(t) for t in o)
                for t in o:
                    if not any(n.start == t.start and n.kategorie == "nadbytecna-zajmena"
                               for n in self.nalezy):
                        self.pridej("skladba", "nadbytecna-zajmena", "P1", t.start, t.end,
                                    f"{len(o)} podmětových zájmen nebo „svůj“ ve dvou "
                                    f"větách za sebou (práh "
                                    f"{prah('zajmena_podmet_svuj_okno')})", priblizne=priblizne)
        met["zajmena_max_ve_dvou_vetach"] = okno

    # -- výstup -----------------------------------------------------------
    def vysledek(self):
        if not self.model:
            vety = self.doc.prozni_vety()
            po_vetach = [[t for t in v.tokens if t.low in ("já", "my") or t.low in TVARY_SVUJ]
                         for v in vety]
            uk = [v for v in vety if v.tokens and v.tokens[0].low in TVARY_TENTO]
            n = len(vety) or 1
            self.metriky["skladba"] = {"ukazovaci_na_zacatku": len(uk),
                                       "poznamka": "bez modelu: jen „já“, „my“, tvary „svůj“ a "
                                                   "„tento“; nominalizace a pasivum vynechány"}
            self._zajmena_v_rade(po_vetach, self.metriky["skladba"], True)
            if len(uk) >= prah("ukazovaci_zacatky") and \
                    len(uk) / n >= prah("ukazovaci_zacatky_podil"):
                for v in uk:
                    self.pridej("skladba", "ukazovaci-ritual", "P2", v.tokens[0].start,
                                v.tokens[0].end, f"{len(uk)} vět začíná tvarem „tento“")
            self.nalezy.sort(key=lambda n: (n.start, PORADI_ZAV[n.zavaznost]))
        pocty = {k: 0 for k in PORADI_ZAV}
        for n in self.nalezy:
            pocty[n.zavaznost] += 1
        return {
            "verze": VERZE,
            "rezim": "udpipe" if self.model else "pravidla",
            "vse": self.vse,
            "priblizne": not self.model,
            "profil": self.profil_jm,
            "slova_md": self.slova_cesta,
            "souhrn": {"slov": self.doc.pocet_slov(), "vet": len(self.doc.prozni_vety()),
                       "titulku": sum(1 for v in self.doc.vety if v.druh == "titulek"),
                       "nalezy": pocty, "vylouceno": self.doc.vylouceno()},
            "metriky": self.metriky,
            "nalezy": [n.jako_dict(self.doc.radek) for n in self.nalezy],
            "prahy": PRAHY,
            "varovani": self.varovani,
        }


# ---------------------------------------------------------------------------
# Čitelný přehled
# ---------------------------------------------------------------------------
def prehled(v):
    r = []
    s = v["souhrn"]
    rezim = "s modelem UDPipe" if v["rezim"] == "udpipe" else "bez modelu (přibližně)"
    r.append(f"unslop-cs metriky {v['verze']} · profil {v['profil']} · {rezim}")
    r.append(f"{s['slov']} slov, {s['vet']} vět, {s['titulku']} titulků · nálezy: " +
             ", ".join(f"{k} {n}" for k, n in s["nalezy"].items()))
    vyl = s.get("vylouceno", {})
    if vyl.get("useku"):
        nazvy = {"kod": "kód", "citace": "citace", "tabulka": "tabulka"}
        r.append(f"vyloučeno z měření: {vyl['slov']} slov (" +
                 ", ".join(f"{nazvy[k]} {vyl['useku'][k]}" for k in nazvy if k in vyl["useku"]) +
                 ")" + ("" if v.get("vse") or not ({"citace", "tabulka"} & set(vyl["useku"]))
                        else "; --vse změří citace a tabulky"))
    ry = v["metriky"].get("rytmus", {})
    if ry.get("vet"):
        r.append(f"rytmus: průměr {ry.get('prumer')} slov, sd {ry.get('smerodatna_odchylka', 0)}, "
                 f"cv {ry.get('variacni_koeficient', 0)}")
    sk = v["metriky"].get("skladba", {})
    if "slovesna_substantiva_na_1000_slov" in sk:
        r.append(f"skladba: slovesná substantiva {sk['slovesna_substantiva_na_1000_slov']}/1000 "
                 f"slov, opisné pasivum {sk['opisne_pasivum']}, zvratné {sk['zvratne_pasivum']}")
    po, ko = v["metriky"].get("postoj", {}), v["metriky"].get("konkretnost", {})
    if po and ko:
        ref = {**po.get("reference", {}), **ko.get("reference", {})}

        def h(m, k):
            return f"{m.get(k)} (lidé {ref[k]['lide']})"
        r.append("postoj a konkrétnost (info, přepis je nemá snižovat): modální částice "
                 f"{h(po, 'modalni_na_1000_slov')}, oslabující {h(po, 'oslabujici_na_1000_slov')}"
                 f"/1000 slov, otazníky {h(po, 'otazniky_na_100_vet')}/100 vět, čísla "
                 f"{h(ko, 'cisla_na_1000_slov')}, vlastní jména "
                 f"{h(ko, 'vlastni_jmena_na_1000_slov')}/1000 slov")
    for zav in ("P0", "P1", "P2"):
        nal = [n for n in v["nalezy"] if n["zavaznost"] == zav]
        if not nal:
            continue
        r.append("")
        r.append(f"{zav}:")
        for n in nal:
            txt = n["text"].replace("\n", " ")
            if len(txt) > 70:
                txt = txt[:67] + "…"
            pozn = f" – {n['poznamka']}" if n.get("poznamka") else ""
            r.append(f"  ř. {n['radek']}: [{n['metrika']}/{n['kategorie']}] „{txt}“{pozn}")
    info = [n for n in v["nalezy"] if n["zavaznost"] == "info"]
    if info:
        r.append("")
        r.append(f"info ({len(info)} slabých signálů, samy o sobě nejsou nález):")
        for n in info:
            txt = n["text"].replace("\n", " ")
            if len(txt) > 50:
                txt = txt[:47] + "…"
            pozn = f" – {n['poznamka']}" if n.get("poznamka") else ""
            r.append(f"  ř. {n['radek']}: [{n['metrika']}/{n['kategorie']}] „{txt}“{pozn}")
    for w in v["varovani"]:
        r.append(f"varování: {w}")
    return "\n".join(r)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def vychozi_slova():
    tady = os.path.dirname(os.path.abspath(__file__))
    return os.path.normpath(os.path.join(tady, "..", "references", "slova.md"))


_UDPIPE_CACHE = {}


def nacti_udpipe(cesta):
    if not cesta:
        return None
    if cesta not in _UDPIPE_CACHE:
        _UDPIPE_CACHE[cesta] = UDPipe(cesta)
    return _UDPIPE_CACHE[cesta]


def analyzuj(text, profil="blog", udpipe=None, slova=None, vse=False):
    """API pro testy a jiné skripty. `udpipe` je cesta k modelu, objekt UDPipe, nebo None.
    `vse`: citace „>“, tabulky a „…“ měřit jako běžný text (kód se nevyloučí nikdy)."""
    if isinstance(udpipe, str):
        udpipe = nacti_udpipe(udpipe)
    profil = ALIASY_PROFILU.get(profil, profil)
    return Analyza(text, profil, udpipe, slova or vychozi_slova(), vse).spust().vysledek()


def main(argv=None):
    ap = argparse.ArgumentParser(description="Měřitelné kontroly AI slopu v českém textu.")
    ap.add_argument("vstup", nargs="?", default="-", help="soubor s textem, nebo - pro stdin")
    ap.add_argument("--profil", default="blog",
                    help="socialni | blog | email | dokumentace | odborny | prezentace")
    ap.add_argument("--udpipe", default=os.environ.get("UNSLOP_UDPIPE"),
                    help="cesta k modelu czech-pdt-ud-2.5-191206.udpipe")
    ap.add_argument("--bez-modelu", action="store_true",
                    help="omezený režim i při nastavené proměnné UNSLOP_UDPIPE")
    ap.add_argument("--slova", default=vychozi_slova(), help="cesta k references/slova.md")
    ap.add_argument("--format", choices=["text", "json", "oboje"], default="text",
                    help="text (výchozí) je stručný přehled včetně slabých signálů; "
                         "json je úplný výstup bez prahů")
    ap.add_argument("--prahy", action="store_true",
                    help="přidat do JSON pole prahy (konstantní data, výchozí výstup je nemá)")
    ap.add_argument("--vse", action="store_true",
                    help="měřit i blokové citace „>“, tabulky a citace v „…“ s plnou závažností "
                         "(kód, URL a e-maily zůstávají vyloučené)")
    ap.add_argument("--prah", choices=["P0", "P1", "P2"],
                    help="návratový kód 1, když existuje nález této nebo vyšší závažnosti")
    a = ap.parse_args(argv)
    profil = ALIASY_PROFILU.get(a.profil, a.profil)
    if profil not in PROFILY:
        ap.error(f"neznámý profil {a.profil}")
    if a.vstup == "-":
        text = sys.stdin.read()
    else:
        with open(a.vstup, encoding="utf-8") as f:
            text = f.read()
    v = analyzuj(text, profil, None if a.bez_modelu else a.udpipe, a.slova, a.vse)
    if not a.prahy:
        v.pop("prahy", None)
    if a.format in ("json", "oboje"):
        print(json.dumps(v, ensure_ascii=False, indent=2))
    if a.format in ("text", "oboje"):
        print(prehled(v), file=sys.stderr if a.format == "oboje" else sys.stdout)
    if a.prah:
        mez = PORADI_ZAV[a.prah]
        if any(PORADI_ZAV[n["zavaznost"]] <= mez for n in v["nalezy"]):
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
