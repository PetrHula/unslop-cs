"""Soudce: zachování významu a slepé párové srovnání A/B (krok 5 PLAN.md).

Soudce je jiný model než ten, který spouští skill (konfigurace behy.model_soudce), běží bez
nástrojů a odpovídá podle schématu JSON. Párové srovnání se pouští v obou pořadích; výhra
platí, jen když se obě pořadí shodnou, jinak je to remíza.
"""
from cli import zavolej

SYSTEM = "Jsi pečlivý redaktor českých textů. Odpovídáš jen podle zadání."

ZADANI_VYZNAM = """Porovnej originál a přepis českého textu. Posuzuj jen obsah, ne styl: přeformulování, jiný slovosled, škrty opakování nebo prázdných frází a jiná slova pro totéž nejsou změnou obsahu.

Vypiš:
- „pridano“: věcná tvrzení, která jsou v přepisu, ale v originálu nejsou (nová fakta, čísla, jména, příčiny, hodnocení, která originál neobsahuje).
- „vynechano“: věcná tvrzení z originálu, která v přepisu chybějí nebo jsou změněná (jiné číslo, jiné jméno, opačný smysl).
Každé tvrzení jednou krátkou větou. Když nic takového není, vrať prázdné pole.

<original>
{original}
</original>

<prepis>
{prepis}
</prepis>"""

SCHEMA_VYZNAM = {
    "type": "object",
    "properties": {"pridano": {"type": "array", "items": {"type": "string"}},
                   "vynechano": {"type": "array", "items": {"type": "string"}}},
    "required": ["pridano", "vynechano"],
}

ZADANI_AB = """Dostaneš originál českého textu a dva jeho přepisy, A a B. Rozhodni, který přepis je lepší: čte se jako text, který napsal člověk, ne jazykový model, je přirozený a srozumitelný, a přitom zachovává obsah originálu (nic nepřidává, nic podstatného nevynechává). Když jsou oba stejně dobré, odpověz „nerozhodne“.

<original>
{original}
</original>

<prepis_A>
{a}
</prepis_A>

<prepis_B>
{b}
</prepis_B>"""

SCHEMA_AB = {
    "type": "object",
    "properties": {"lepsi": {"type": "string", "enum": ["A", "B", "nerozhodne"]},
                   "duvod": {"type": "string"}},
    "required": ["lepsi", "duvod"],
}


def vyznam(original, prepis, model, timeout=300):
    """Vrátí (dict pridano/vynechano/poruseni, cena)."""
    r = zavolej(ZADANI_VYZNAM.format(original=original, prepis=prepis), model, SYSTEM, timeout=timeout,
                schema=SCHEMA_VYZNAM)
    s = r.get("structured") or {}
    pridano, vynechano = s.get("pridano") or [], s.get("vynechano") or []
    return {"pridano": pridano, "vynechano": vynechano, "poruseni": bool(pridano or vynechano)}, r["cena"]


def ab(original, prepis_x, prepis_y, model, timeout=300):
    """Slepé srovnání x proti y v obou pořadích. Vrátí ('x' | 'y' | 'remiza', detail, cena)."""
    r1 = zavolej(ZADANI_AB.format(original=original, a=prepis_x, b=prepis_y), model, SYSTEM,
                 timeout=timeout, schema=SCHEMA_AB)
    r2 = zavolej(ZADANI_AB.format(original=original, a=prepis_y, b=prepis_x), model, SYSTEM,
                 timeout=timeout, schema=SCHEMA_AB)
    v1 = (r1.get("structured") or {}).get("lepsi")
    v2 = (r2.get("structured") or {}).get("lepsi")
    prvni = {"A": "x", "B": "y"}.get(v1, "remiza")
    druhe = {"A": "y", "B": "x"}.get(v2, "remiza")
    vysledek = prvni if prvni == druhe else "remiza"
    detail = {"poradi_xy": v1, "poradi_yx": v2,
              "duvody": [(r1.get("structured") or {}).get("duvod"), (r2.get("structured") or {}).get("duvod")]}
    return vysledek, detail, r1["cena"] + r2["cena"]
