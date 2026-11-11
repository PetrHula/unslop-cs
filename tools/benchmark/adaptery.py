"""Adaptéry skillů pro benchmark (krok 4 PLAN.md).

Každý skill dostane stejné zadání (SPOLECNE). Adaptér ho převede do přirozené podoby
skillu (jak ho vyvolat, kde má plugin, jaké nástroje smí) a určí převod jeho závažností
na společnou škálu vysoka / stredni / nizka / neuvedena.

Záznam skillu v konfiguraci:
  {"nazev": "unslop-cs", "adapter": "unslop_cs", "plugin_dir": "."}
  {"nazev": "bez-skillu", "adapter": "bez_skillu"}
  {"nazev": "jiny", "adapter": "obecny", "plugin_dir": "~/skilly/jiny", "skill": "jiny:jiny",
   "nastroje": "Skill Read Glob Grep", "zavaznost": {"vysoká": "vysoka", "střední": "stredni"}}
Cesty se berou relativně ke kořeni repozitáře.
"""
import hashlib
import os

KOREN_REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SPOLECNE = """Zkontroluj následující český text: vypiš, co v něm zní jako psané AI, a u každého nálezu uveď závažnost. Potom dej opravenou verzi celého textu mezi dva samostatné řádky <<<VERZE a VERZE>>>. Když není co opravit, dej mezi ně původní text beze změny.
{soubor}
<text>
{text}
</text>"""

SOUBOR = "Stejný text je uložený v souboru vstup.txt (UTF-8) v pracovním adresáři.\n"

UROVNE = ("vysoka", "stredni", "nizka", "neuvedena")


def otisk_adresare(cesta, vynechat=("evals", "__pycache__", ".git")):
    """sha256 obsahu adresáře (názvy a obsahy souborů), prvních 12 znaků."""
    h = hashlib.sha256()
    for koren, adresare, soubory in sorted(os.walk(cesta)):
        adresare[:] = sorted(d for d in adresare if d not in vynechat)
        for s in sorted(soubory):
            with open(os.path.join(koren, s), "rb") as f:
                h.update(os.path.relpath(os.path.join(koren, s), cesta).encode() + f.read())
    return h.hexdigest()[:12]


class Adapter:
    nazev = None
    plugin_dir = None      # adresář pluginu pro --plugin-dir, nebo None
    skill = None           # podřetězec vstupu nástroje Skill, podle kterého se pozná načtení
    nastroje = None        # --allowedTools; None = bez nástrojů
    vstup_v_souboru = False
    zavaznost = {}         # štítek skillu (malými písmeny) -> společná úroveň
    otisk_cesta = None

    def zadani(self, text):
        return SPOLECNE.format(text=text, soubor=SOUBOR if self.vstup_v_souboru else "")

    def uroven(self, stitek):
        s = (stitek or "").strip().lower()
        for k, v in self.zavaznost.items():
            if s == k.lower() or s.startswith(k.lower()):
                return v
        return "neuvedena"

    def otisk(self):
        return otisk_adresare(self.otisk_cesta) if self.otisk_cesta else None


class UnslopCs(Adapter):
    skill = "unslop-cs"
    vstup_v_souboru = True
    # stejné nástroje jako regresní evaly (tools/evaly/runner.py, NASTROJE_SKILLU)
    nastroje = "Skill Read Write Glob Grep Bash(python3 *)"
    zavaznost = {"P0": "vysoka", "P1": "stredni", "P2": "nizka"}

    def __init__(self, spec):
        self.nazev = spec.get("nazev", "unslop-cs")
        self.plugin_dir = os.path.normpath(os.path.join(KOREN_REPO, spec.get("plugin_dir", ".")))
        self.otisk_cesta = os.path.join(self.plugin_dir, "skills", "unslop-cs")

    def zadani(self, text):
        return "Použij skill unslop-cs (unslop-cs:unslop-cs).\n" + super().zadani(text)


class BezSkillu(Adapter):
    """Stejné zadání bez pluginu a bez nástrojů: co udělá model sám."""

    def __init__(self, spec):
        self.nazev = spec.get("nazev", "bez-skillu")
        self.zavaznost = {"vysoká": "vysoka", "vysoka": "vysoka", "high": "vysoka", "kritick": "vysoka",
                          "střední": "stredni", "stredni": "stredni", "medium": "stredni",
                          "nízká": "nizka", "nizka": "nizka", "low": "nizka", "drobn": "nizka"}


class Obecny(Adapter):
    """Skill dodaný uživatelem: plugin, název skillu, nástroje a převod závažností z konfigurace."""

    def __init__(self, spec):
        self.nazev = spec["nazev"]
        self.plugin_dir = os.path.normpath(os.path.join(KOREN_REPO, os.path.expanduser(spec["plugin_dir"])))
        self.skill = spec["skill"]
        self.nastroje = spec.get("nastroje", "Skill Read Glob Grep")
        self.vstup_v_souboru = spec.get("vstup_v_souboru", False)
        self.zavaznost = spec.get("zavaznost", {})
        self.vyvolani = spec.get("vyvolani", f"Použij skill {self.skill}.")
        self.otisk_cesta = os.path.normpath(os.path.join(KOREN_REPO, os.path.expanduser(
            spec.get("otisk", spec["plugin_dir"]))))

    def zadani(self, text):
        return self.vyvolani + "\n" + super().zadani(text)


ADAPTERY = {"unslop_cs": UnslopCs, "bez_skillu": BezSkillu, "obecny": Obecny}


def nacti(spec):
    return ADAPTERY[spec["adapter"]](spec)
