"""Skriptové metriky přepisu bez LLM (krok 5 PLAN.md).

- cisla_a_data(original, prepis): podíl čísel a dat z originálu, která v přepisu zůstala
  (porovnává se normalizovaný řetězec čísla; datum „17. června 1775“ i „17. 6. 1775“
  se rozloží na čísla). Zástupný znak „#“ z UD CAC (anonymizovaná čísla) se počítá jako číslo.
- jmena(orig_vety, prepis_vety): podíl lemmat vlastních jmen (UPOS PROPN) z originálu,
  která jsou i v přepisu; potřebuje větné rozbory z rysy.Analyzator.
- zmeneny_podil(original, prepis): 1 − podíl shodných slov podle difflib.SequenceMatcher
  (0 = beze změny, 1 = vše jinak).
"""
import difflib
import re

_CISLO = re.compile(r"(?<![\w#])(\d+(?:[  ]\d{3})*(?:[,.]\d+)?|#)(?![\w])")


def _cisla(text):
    out = []
    for m in _CISLO.finditer(text):
        c = re.sub(r"[  ]", "", m.group(1)).replace(",", ".")
        out.append(c)
    return out


def cisla_a_data(original, prepis):
    """Vrátí (zachováno, celkem); vícenásobný výskyt se počítá jako multimnožina."""
    o, p = _cisla(original), _cisla(prepis)
    zbyva = list(p)
    zachovano = 0
    for c in o:
        if c in zbyva:
            zbyva.remove(c)
            zachovano += 1
    return zachovano, len(o)


def jmena(orig_vety, prepis_vety):
    """orig_vety, prepis_vety: výstup rysy.Analyzator.vety. Vrátí (zachováno, celkem) nad
    množinou lemmat PROPN."""
    o = {t[1] for v in orig_vety for t in v if t[2] == "PROPN"}
    p = {t[1] for v in prepis_vety for t in v if t[2] == "PROPN"}
    return len(o & p), len(o)


def zmeneny_podil(original, prepis):
    a, b = original.split(), prepis.split()
    if not a:
        return 0.0
    sm = difflib.SequenceMatcher(a=a, b=b, autojunk=False)
    shodnych = sum(bl.size for bl in sm.get_matching_blocks())
    return round(1 - shodnych / max(len(a), len(b)), 4)
