#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Testy pro metriky.py.

    python3 test_metriky.py                       # bez modelu
    UNSLOP_UDPIPE=/cesta/model.udpipe python3 test_metriky.py   # i s modelem
    python3 test_metriky.py --udpipe /cesta/model.udpipe -v

Testy z evals/pripady.md: čisté případy (6, 9, 11, 12, 14, 15, 19, 24, 26, 28) nemají nález
P0 ani P1, zašpiněné mají aspoň jeden nález v očekávané kategorii. Případy,
které skript měřením zachytit neumí, jsou v OCEKAVANE_SELHANI s důvodem.
"""
import os
import re
import sys
import unittest

TADY = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, TADY)
import metriky  # noqa: E402

PRIPADY_MD = os.path.join(TADY, "..", "evals", "pripady.md")
CISTE = {6, 9, 11, 12, 14, 15, 19, 24, 26, 28}

# Pro každý zašpiněný případ: seznam (metrika, kategorie-prefix) – aspoň jeden musí
# padnout se závažností P0–P2. Kategorie odpovídají očekávání v pripady.md.
OCEKAVANO = {
    1: [("seznamy_slov", "fraze-uvod"), ("kontrast", "kontrastni-obrat"),
        ("trojice", "trojice"), ("seznamy_slov", "uroven-1")],
    2: [("seznamy_slov", "uroven-1"), ("seznamy_slov", "kalk"),
        ("typografie", "dlouha-pomlcka"), ("vestavene", "vagni-autorita")],
    3: [("typografie", "title-case"), ("titulky", "upoutavkovy-titulek")],
    4: [("seznamy_slov", "kalk"), ("seznamy_slov", "chatbot")],
    5: [("seznamy_slov", "jmenny"), ("skladba", "jmenny-styl")],
    7: [("skladba", "nadbytecna-zajmena"), ("skladba", "ukazovaci-ritual"),
        ("skladba", "priklonka")],
    8: [("vestavene", "vagni-autorita")],
    10: [("seznamy_slov", "fraze-prozreni"), ("kontrast", "kontrastni-obrat"),
         ("seznamy_slov", "fraze-pointa")],
    13: [("typografie", "procenta"), ("typografie", "datum"),
         ("typografie", "oddelovac-radu"), ("typografie", "rozsah"), ("typografie", "cas")],
    16: [("seznamy_slov", "fraze-uvod"), ("seznamy_slov", "fraze-prechod")],
    17: [("vestavene", "otazka-s-odpovedi"), ("vestavene", "dvojteckove-odhaleni"),
         ("rytmus", "heslovita-kadence"), ("rytmus", "retez-kratkych-vet")],
    18: [("skladba", "jmenny-styl"), ("seznamy_slov", "jmenny")],
    20: [("vestavene", "vlozeny-pokyn"), ("seznamy_slov", "fraze-uvod"),
         ("seznamy_slov", "uroven-1")],
    21: [("skladba", "ukazovaci-ritual")],
    22: [("seznamy_slov", "uroven-2")],
    23: [("seznamy_slov", "fraze-hrana")],
    25: [("typografie", "dlouha-pomlcka")],
    27: [("seznamy_slov", "uroven-1"), ("seznamy_slov", "uroven-2")],
}

# Kategorie, které musí padnout všechny (ne jen jedna) – kontrolují konkrétní metriky.
POVINNE = {
    1: [("kontrast", "kontrastni-obrat")],
    2: [("typografie", "dlouha-pomlcka")],
    3: [("typografie", "title-case")],
    10: [("kontrast", "kontrastni-obrat")],
    13: [("typografie", "datum"), ("typografie", "oddelovac-radu"), ("typografie", "cas")],
    20: [("vestavene", "vlozeny-pokyn")],
    21: [("skladba", "ukazovaci-ritual")],
    22: [("seznamy_slov", "uroven-2")],
    25: [("typografie", "dlouha-pomlcka")],
    27: [("seznamy_slov", "uroven-2")],
}

# Případy, které měření nezachytí (struktura, význam). Podrobnosti v
# vystupy/F3-metriky.md, oddíl Pro F5.
OCEKAVANE_SELHANI = {
    18: "rekapitulace kontextu a „po zvážení všech možností jsem dospěl k závěru“ nejsou "
        "v slova.md; jde o strukturu odpovědi, ne o měřitelný vzorec",
}

PROFIL_Z_NADPISU = {
    "sociální sítě": "socialni", "blog": "blog", "prezentace": "prezentace",
    "e-mail": "email", "dokumentace": "dokumentace", "odborný text": "odborny",
}


def nacti_pripady(cesta=PRIPADY_MD):
    with open(cesta, encoding="utf-8") as f:
        md = f.read()
    pripady = {}
    for blok in re.split(r"^## ", md, flags=re.M)[1:]:
        hlava, _, telo = blok.partition("\n")
        m = re.match(r"Případ (\d+)", hlava)
        if not m:
            continue
        cislo = int(m.group(1))
        pm = re.search(r"profil: ([^)]+)\)", hlava)
        profil = PROFIL_Z_NADPISU.get(pm.group(1).strip(), "blog") if pm else "blog"
        vstup = telo.split("OČEKÁVÁNO")[0]
        radky = [re.sub(r"^> ?", "", r) for r in vstup.split("\n") if r.startswith(">")]
        pripady[cislo] = (profil, "\n".join(radky).strip())
    return pripady


def nalezy(v, minimalni="P2"):
    mez = metriky.PORADI_ZAV[minimalni]
    return [n for n in v["nalezy"] if metriky.PORADI_ZAV[n["zavaznost"]] <= mez]


def ma(v, metrika, kat, minimalni="P2"):
    return any(n["metrika"] == metrika and n["kategorie"].startswith(kat)
               for n in nalezy(v, minimalni))


class _Zaklad:
    UDPIPE = None

    @classmethod
    def setUpClass(cls):
        cls.pripady = nacti_pripady()

    def analyzuj(self, text, profil="blog"):
        return metriky.analyzuj(text, profil, self.UDPIPE)

    # -- evals ---------------------------------------------------------------
    def test_pocet_pripadu(self):
        self.assertEqual(len(self.pripady), 28)

    def test_ciste_pripady_bez_p0_p1(self):
        for c in sorted(CISTE):
            profil, text = self.pripady[c]
            v = self.analyzuj(text, profil)
            vadne = nalezy(v, "P1")
            with self.subTest(pripad=c):
                self.assertEqual(vadne, [], f"případ {c}: {vadne}")

    def test_zaspinene_pripady(self):
        for c, ocek in OCEKAVANO.items():
            profil, text = self.pripady[c]
            v = self.analyzuj(text, profil)
            with self.subTest(pripad=c):
                if c in OCEKAVANE_SELHANI:
                    continue
                self.assertTrue(any(ma(v, m, k) for m, k in ocek),
                                f"případ {c}: žádný nález z {ocek}; nalezeno "
                                f"{[(n['metrika'], n['kategorie']) for n in nalezy(v)]}")
                for m, k in POVINNE.get(c, []):
                    self.assertTrue(ma(v, m, k), f"případ {c}: chybí {m}/{k}")

    def test_vsechny_bezi(self):
        for c, (profil, text) in self.pripady.items():
            v = self.analyzuj(text, profil)
            self.assertIn("nalezy", v)
            self.assertGreater(v["souhrn"]["slov"], 0)

    # -- dělení vět ----------------------------------------------------------
    def vety(self, text):
        d = metriky.Dokument(text, metriky.nacti_udpipe(self.UDPIPE) if self.UDPIPE else None)
        return [v.text.strip() for v in d.vety]

    def test_vety_zkratky(self):
        t = ("Firma Alfa, s. r. o., dodá zboží, tj. stoly, židle atd. do konce měsíce. "
             "Ing. Jana Nová, Ph.D., to potvrdila. Platí to např. pro tzv. velké zakázky, "
             "resp. pro zakázky nad cca 1 mil. Kč. Další věta.")
        self.assertEqual(len(self.vety(t)), 4, self.vety(t))

    def test_vety_data_a_cislovky(self):
        t = ("Schůzka bude 4. 5. 2026 v 10.30. Druhé kolo začne 5. května a 2. kolo skončí "
             "v červnu. V roce 2026. Pak nic.")
        self.assertEqual(len(self.vety(t)), 4, self.vety(t))

    def test_vety_zakonceni(self):
        t = "Opravdu? Ano! Uvidíme… Možná zítra. Poslední věta bez tečky"
        self.assertEqual(len(self.vety(t)), 5, self.vety(t))

    def test_vety_radky(self):
        t = "Dobrý den,\n\nposílám podklady.\n\nS pozdravem\nMartin Kos"
        v = self.vety(t)
        self.assertIn("posílám podklady.", v)

    # -- jednotlivé metriky --------------------------------------------------
    def test_dlouha_pomlcka(self):
        v = self.analyzuj("Projekt skončil včas—a v rozpočtu.")
        self.assertTrue(ma(v, "typografie", "dlouha-pomlcka", "P1"))

    def test_jedna_pomlcka_neni_nalez(self):
        v = self.analyzuj("Projekt skončil včas – a v rozpočtu. Tým byl spokojený.")
        self.assertFalse(ma(v, "typografie", "rozpocet-pomlcek"))

    def test_rozpocet_pomlcek(self):
        v = self.analyzuj("Projekt – jak víme – skončil včas – a v rozpočtu.")
        self.assertTrue(ma(v, "typografie", "rozpocet-pomlcek", "P1"))

    def test_cas_neni_desetinne_cislo(self):
        v = self.analyzuj("Otevřeno je 9.00–18.00 a v sobotu do 12.30.")
        self.assertFalse(ma(v, "typografie", "desetinna-tecka"))

    def test_desetinna_tecka(self):
        v = self.analyzuj("Růst byl 2.5 procenta.")
        self.assertTrue(ma(v, "typografie", "desetinna-tecka"))

    def test_procenta_pridavne_jmeno(self):
        if not self.UDPIPE:
            self.skipTest("rozlišení „25% sleva“ jen s modelem")
        v = self.analyzuj("Dostanete 25% slevu na všechno.")
        self.assertFalse(ma(v, "typografie", "procenta"))

    def test_title_case(self):
        v = self.analyzuj("# Strategické Partnerství A Globální Řešení\n\nText odstavce je tady.")
        self.assertTrue(ma(v, "typografie", "title-case", "P1"))

    def test_nadpis_bez_title_case(self):
        v = self.analyzuj("# Vývoj tržeb 2024–2026\n\nText odstavce je tady.")
        self.assertFalse(ma(v, "typografie", "title-case"))

    def test_seznam_slov_tvary(self):
        v = self.analyzuj("Školení je nedílnou součástí nástupu do firmy.")
        self.assertTrue(ma(v, "seznamy_slov", "uroven-1"))

    def test_seznam_slov_slovesne_tvary(self):
        if not self.UDPIPE:
            self.skipTest("slovesné tvary („hrála“ ← „hrát“) páruje jen model")
        v = self.analyzuj("Tato změna hrála klíčovou roli v celém projektu.")
        self.assertTrue(ma(v, "seznamy_slov", "uroven-1"))

    def test_seznam_slov_v_kodu_ne(self):
        v = self.analyzuj("Proměnná `game_changer` se nastaví v konfiguraci.")
        self.assertFalse(ma(v, "seznamy_slov", "uroven-1"))

    def test_kontrast_tvary(self):
        v = self.analyzuj("Nešlo o peníze. Šlo o čas.")
        self.assertTrue(ma(v, "kontrast", "kontrastni-obrat", "P1"))
        v = self.analyzuj("Nebude to snadné, bude to ale stát za to.")
        self.assertTrue(ma(v, "kontrast", "kontrastni-obrat"))

    def test_kontrast_oprava_neni_nalez(self):
        v = self.analyzuj("Vezměte verzi 3, ne 2. Podíl klesl o 40 %, ne o 4 %.")
        self.assertFalse(ma(v, "kontrast", "kontrastni-obrat"))

    def test_misto_v_nadpisu(self):
        v = self.analyzuj("# Dialog místo přednášky\n\nNa kurzu se hlavně mluví.")
        self.assertTrue(ma(v, "kontrast", "kontrastni-obrat", "P1"))

    def test_trojice_bez_carky_pred_a(self):
        v = self.analyzuj("Nový program je praktický, flexibilní a udržitelný.")
        self.assertTrue(ma(v, "trojice", "trojice", "P1"))

    def test_privesky(self):
        v = self.analyzuj("Firma zavedla nový systém, což podtrhuje její ambice. Tým rostl, "
                          "čímž přispěl k růstu.")
        self.assertTrue(ma(v, "privesky", "privesek"))

    def test_konektory_retez(self):
        v = self.analyzuj("Systém je rychlý. Navíc je levný. Kromě toho je spolehlivý. "
                          "Dále nabízí podporu.")
        self.assertTrue(ma(v, "soudrznost", "konektory-retez", "P1"))

    def test_postoj_informativne(self):
        v = self.analyzuj("Vždyť to přece víte. My jsme to prý zkoušeli.")
        self.assertGreater(v["metriky"]["postoj"]["castice_na_100_slov"], 0)
        self.assertFalse(any(n["metrika"] == "postoj" for n in v["nalezy"]))

    # -- F5 (verze 1.1) -----------------------------------------------------
    def test_prechod_jeden_p2_dva_p1(self):
        v = self.analyzuj("Pokud jde o rozpočet, nic se nemění. Tým zůstává stejný.")
        self.assertTrue(ma(v, "seznamy_slov", "fraze-prechod"))
        self.assertFalse(ma(v, "seznamy_slov", "fraze-prechod", "P1"))
        v = self.analyzuj("Pokud jde o rozpočet, nic se nemění. Co se týče týmu, zůstává.")
        self.assertTrue(ma(v, "seznamy_slov", "fraze-prechod", "P1"))

    def test_uvod_uprostred_odstavce_p2(self):
        v = self.analyzuj("Firma vznikla v Brně. V současné době má třicet lidí.")
        self.assertFalse(ma(v, "seznamy_slov", "fraze-uvod", "P1"))
        v = self.analyzuj("V současné době má firma třicet lidí. Vznikla v Brně.")
        self.assertTrue(ma(v, "seznamy_slov", "fraze-uvod", "P1"))

    def test_preneseně_snizuje_na_p2(self):
        v = self.analyzuj("Potápěč se pomalu ponořil do jezera.")
        self.assertFalse(ma(v, "seznamy_slov", "uroven-1", "P1"))

    def test_vagni_autorita_ze_slova_md(self):
        v = self.analyzuj("Odborníci se shodují, že to funguje.")
        self.assertTrue(ma(v, "vestavene", "vagni-autorita", "P0"))
        self.assertEqual(sum(1 for n in v["nalezy"] if n["kategorie"] == "vagni-autorita"), 1)

    def test_datum_bez_mezer(self):
        v = self.analyzuj("Smlouvu jsme podepsali 4.5.2026 v Praze.")
        self.assertTrue(ma(v, "typografie", "datum"))
        self.assertFalse(ma(v, "typografie", "desetinna-tecka"))
        v = self.analyzuj("Smlouvu jsme podepsali 04.05.2026 v Praze.")
        self.assertFalse(ma(v, "typografie", "datum"))

    def test_zesilovac_neni_nalez(self):
        v = self.analyzuj("Bylo to opravdu velmi těžké a zcela nečekané. Výsledek nás naprosto "
                          "překvapil a výrazně změnil plán.")
        self.assertFalse(any(n["zdroj"].endswith(w) for n in v["nalezy"] if n.get("zdroj")
                             for w in ("zcela", "naprosto", "opravdu", "velmi", "výrazně")))

    def test_uroven2_dlouhy_odstavec(self):
        kratky = "Tento inovativní přístup je flexibilní. Tým ho zavedl v březnu."
        self.assertTrue(ma(self.analyzuj(kratky), "seznamy_slov", "uroven-2", "P1"))
        vypln = " ".join(["Tým pracoval na zakázce celý měsíc a výsledek předal zákazníkovi "
                          "v pondělí ráno."] * 9)
        dlouhy = kratky + " " + vypln
        self.assertFalse(ma(self.analyzuj(dlouhy), "seznamy_slov", "uroven-2", "P1"))

    def test_postoj_a_konkretnost_s_referenci(self):
        v = self.analyzuj("Asi to vyjde. Přijdete v 9.30? Jana Nová poslala 3 návrhy.")
        po, ko = v["metriky"]["postoj"], v["metriky"]["konkretnost"]
        self.assertGreater(po["oslabujici_na_1000_slov"], 0)
        self.assertGreater(po["otazniky_na_100_vet"], 0)
        self.assertGreater(ko["cisla_na_1000_slov"], 0)
        self.assertIn("lide", po["reference"]["modalni_na_1000_slov"])
        self.assertFalse(any(n["metrika"] in ("postoj", "konkretnost") for n in v["nalezy"]))

    def test_navic_dale_se_nepocitaji_do_cetnosti(self):
        v = self.analyzuj("Systém je rychlý. Navíc je levný. Tým je malý. Dále nabízí podporu.")
        self.assertEqual(v["metriky"]["soudrznost"]["konektory_na_zacatku"], 0)

    def test_json_vystup(self):
        import io
        import contextlib
        import json
        import tempfile
        with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False,
                                         encoding="utf-8") as f:
            f.write("V dnešní době je to game changer.")
        buf = io.StringIO()
        args = [f.name, "--format", "json"] + (["--udpipe", self.UDPIPE] if self.UDPIPE
                                               else ["--bez-modelu"])
        with contextlib.redirect_stdout(buf):
            metriky.main(args)
        os.unlink(f.name)
        d = json.loads(buf.getvalue())
        self.assertEqual(d["rezim"], "udpipe" if self.UDPIPE else "pravidla")


class BezModelu(_Zaklad, unittest.TestCase):
    UDPIPE = None


_MODEL = os.environ.get("UNSLOP_UDPIPE")


@unittest.skipUnless(_MODEL and os.path.exists(_MODEL), "model UDPipe není k dispozici "
                     "(nastav UNSLOP_UDPIPE nebo --udpipe)")
class SModelem(_Zaklad, unittest.TestCase):
    UDPIPE = _MODEL

    def test_pasivum_opisne_a_zvratne(self):
        v = self.analyzuj("Bylo rozhodnuto o změně. Systém bude spuštěn v pondělí. "
                          "Poplatky se platí předem.")
        sk = v["metriky"]["skladba"]
        self.assertEqual(sk["opisne_pasivum"], 2)
        self.assertGreaterEqual(sk["zvratne_pasivum"], 1)

    def test_nominalizace_ne_pridavna_jmena(self):
        v = self.analyzuj("Denní a národní vnitřní most a host. Informace o situaci.")
        self.assertEqual(v["metriky"]["skladba"]["slovesna_substantiva"], 0)

    def test_priklonka(self):
        v = self.analyzuj("Tento problém řešili jsme už minulý týden.")
        self.assertTrue(ma(v, "skladba", "priklonka", "P1"))
        v = self.analyzuj("Tento problém jsme řešili už minulý týden.")
        self.assertFalse(ma(v, "skladba", "priklonka"))


if __name__ == "__main__":
    argv = sys.argv[:]
    if "--udpipe" in argv:
        i = argv.index("--udpipe")
        os.environ["UNSLOP_UDPIPE"] = argv[i + 1]
        SModelem.UDPIPE = argv[i + 1]
        del argv[i:i + 2]
        SModelem.__unittest_skip__ = False
    unittest.main(argv=argv)
