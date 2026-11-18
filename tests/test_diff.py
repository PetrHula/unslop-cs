#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Testy pro diff.py: python3 tests/test_diff.py"""
import os
import sys
import unittest

TADY = os.path.dirname(os.path.abspath(__file__))
SKRIPTY = os.path.join(TADY, "..", "plugins", "unslop-cs", "skills", "unslop-cs", "scripts")
sys.path.insert(0, SKRIPTY)
import diff  # noqa: E402

NB = " "


def d(pred, po):
    return diff.slovni_diff(pred, po)


class SlovniDiff(unittest.TestCase):
    def test_beze_zmeny(self):
        self.assertEqual(d("Praha je velká.", "Praha je velká."), [])

    def test_interpunkce_a_uvozovky_zustanou_v_kontextu(self):
        z = d("Projekt „Nový most“ je hotový.", "Projekt „Most“ je hotový.")
        self.assertEqual(z[0]["diff"], "Projekt „[-Nový most-]{+Most+}“ je hotový.")

    def test_desetinne_cislo_jako_celek(self):
        z = d("Podíl byl 1,3" + NB + "%.", "Podíl byl 1,5" + NB + "%.")
        self.assertEqual(z[0]["diff"], "Podíl byl [-1,3-]{+1,5+}" + NB + "%.")

    def test_nezlomitelna_mezera_zustane(self):
        z = d("V" + NB + "Praze žije 3 miliony.", "V" + NB + "Brně žije 3 miliony.")
        self.assertIn("V" + NB + "[-Praze-]{+Brně+}", z[0]["diff"])

    def test_pomlcka_se_nemeni(self):
        z = d("Byl to rok 2019 – a pak 2020.", "Byl to rok 2021 – a pak 2020.")
        self.assertIn(" – a pak", z[0]["diff"])

    def test_kazda_zmenena_veta_ma_vlastni_zaznam(self):
        z = d("Jedna věta. Druhá věta.", "Jiná věta. Třetí věta.")
        self.assertEqual(len(z), 2)

    def test_kod_se_neporovnava(self):
        z = d("Text.\n\n```\na = 1\n```\n", "Text.\n\n```\nb = 2\n```\n")
        self.assertEqual(z, [])

    def test_bez_locale_nezavisi(self):
        # Diff je čistý Python, v kódu není volání locale ani gitu.
        zdroj = open(os.path.join(SKRIPTY, "diff.py"), encoding="utf-8").read()
        self.assertNotIn("subprocess", zdroj)
        self.assertNotIn("setlocale", zdroj)


class Ztraty(unittest.TestCase):
    def test_ztrata_cisla(self):
        z = diff.ztraty("Ušetřili jsme 12 tisíc.", "Ušetřili jsme hodně.")
        self.assertEqual(z["cisla"], ["12"])

    def test_cislo_zustalo(self):
        z = diff.ztraty("Ušetřili jsme 12 tisíc.", "Šetří se 12 tisíc.")
        self.assertEqual(z["cisla"], [])

    def test_sklonovane_jmeno_se_nehlasi(self):
        z = diff.ztraty("Žijeme v Praze.", "Pracuji v Praha.")
        self.assertEqual(z["jmena"], [])

    def test_chybejici_jmeno(self):
        z = diff.ztraty("Jel do Brna.", "Jel do města.")
        self.assertEqual(z["jmena"], ["Brna"])

    def test_zacatek_vety_neni_jmeno(self):
        z = diff.ztraty("Dnes prší.", "Venku prší.")
        self.assertEqual(z["jmena"], [])

    def test_smazana_castice_a_jisteni(self):
        z = diff.ztraty("Je to asi pravda, přece.", "Je to pravda.")
        self.assertEqual(sorted(z["castice"]), ["asi", "přece"])

    def test_pocet_vyskytu(self):
        z = diff.ztraty("Asi ano, asi ne.", "Asi ano, ne.")
        self.assertEqual(z["castice"], ["asi"])

    def test_sila_tvrzeni_jen_info(self):
        z = diff.ztraty("To způsobuje růst.", "To ovlivňuje růst.")
        self.assertEqual(z["zesilovace_sily"], ["způsobuje"])
        self.assertTrue(diff._prazdne(z))

    def test_kod_a_citace_se_nepocitaji(self):
        zdroj = "Text.\n\n```\n42 Brno\n```\n\n> Citace 7 Ostrava.\n"
        z = diff.ztraty(zdroj, "Text.\n")
        self.assertEqual((z["cisla"], z["jmena"]), ([], []))


class Rozhrani(unittest.TestCase):
    def _soubory(self, a, b):
        import tempfile
        self.tmp = tempfile.mkdtemp()
        pa, pb = os.path.join(self.tmp, "a.txt"), os.path.join(self.tmp, "b.txt")
        open(pa, "w", encoding="utf-8").write(a)
        open(pb, "w", encoding="utf-8").write(b)
        return pa, pb

    def test_prisne_vraci_1_pri_ztrate(self):
        pa, pb = self._soubory("Je to 12 %.", "Je to málo.")
        import io
        import contextlib
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(diff.main([pa, pb, "--prisne"]), 1)
            self.assertEqual(diff.main([pa, pb]), 0)

    def test_prisne_vraci_0_bez_ztraty(self):
        pa, pb = self._soubory("Je to 12 %.", "Činí to 12 %.")
        import io
        import contextlib
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(diff.main([pa, pb, "--prisne"]), 0)

    def test_json_a_metriky(self):
        import io
        import json
        import contextlib
        pa, pb = self._soubory("Praha je asi velká. Žije tu 3 lidé.", "Praha je velká.")
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            diff.main([pa, pb, "--format", "json", "--metriky"])
        v = json.loads(buf.getvalue())
        self.assertEqual(set(v), {"zmeny", "ztraty", "metriky"})
        self.assertIn("radek", v["metriky"])
        self.assertTrue(v["metriky"]["radek"].startswith("Metriky před → po:"))

    def test_md_bez_zmeny(self):
        pa, pb = self._soubory("Stejné.", "Stejné.")
        import io
        import contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            diff.main([pa, pb])
        self.assertIn("Beze změny.", buf.getvalue())


if __name__ == "__main__":
    unittest.main()
