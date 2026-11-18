#!/usr/bin/env python3
"""Pouští případy 31 a 32 (formát výstupu přepisu) a měří tokeny.

Hlavní runner je přeskakuje, protože nekontrolují nálezy, ale tvar výstupu, a
ten se hodnotí ručně podle řádků OČEKÁVÁNO v evals/pripady.md.
Tento skript jen pustí skill se stejným zadáním a omezením nástrojů, uloží úplné
výstupy k ruční kontrole a spočítá tokeny stejným způsobem jako runner.py, aby
šlo výchozí stav a změněný skill srovnat i na těchto případech.

  31: agent bez shellu a bez souborů (povolené nástroje: Skill, Read)
  32: agent s Pythonem a gitem, text v souboru vstup.txt

Použití (z kořene repozitáře):
    python3 tools/evaly/format_vystupu.py --stitek format --model claude-sonnet-5-5

Výstup: tools/evaly/vysledky/<stitek>/format-vystupu.json a format-vystupu.md.
"""

import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import runner  # noqa: E402

NASTROJE = {
    31: "Skill Read",
    32: runner.NASTROJE_SKILLU + " Bash(git *)",
}

ZADANI_31 = """Použij skill unslop-cs (unslop-cs:unslop-cs). Přepiš to lidsky, profil registru „blog“ (blog).

<text>
{vstup}
</text>"""

ZADANI_32 = """Použij skill unslop-cs (unslop-cs:unslop-cs). Přepiš to lidsky, profil registru „blog“ (blog).
Stejný text je uložený v souboru vstup.txt (UTF-8) v pracovním adresáři.

<text>
{vstup}
</text>"""


def vstup_pripadu_31():
    """Text případu 31 z pripady.md (řádky „> “ před prvním OČEKÁVÁNO)."""
    with open(runner.PRIPADY, encoding="utf-8") as f:
        radky = f.read().splitlines()
    i = next(k for k, r in enumerate(radky) if r.startswith("## Případ 31"))
    vstup = []
    for r in radky[i + 1:]:
        if r.startswith("OČEKÁVÁNO"):
            break
        if r.startswith(">"):
            vstup.append(r[2:] if r.startswith("> ") else r[1:])
    if not vstup:
        raise SystemExit("V případu 31 chybí VSTUP.")
    return "\n".join(vstup).strip()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--stitek", required=True)
    ap.add_argument("--pripady", default="31,32")
    ap.add_argument("--behy", type=int, default=1)
    ap.add_argument("--model")
    ap.add_argument("--udpipe")
    ap.add_argument("--timeout", type=int, default=900)
    ap.add_argument("--opakovani", type=int, default=3)
    ap.add_argument("--pauza", type=int, default=30)
    a = ap.parse_args()

    vstup = vstup_pripadu_31()
    zaznamy = []
    for cislo in (int(x) for x in a.pripady.split(",")):
        for beh in range(1, a.behy + 1):
            zadani = (ZADANI_31 if cislo == 31 else ZADANI_32).format(vstup=vstup)
            s, pokusy, infra = runner._s_opakovanim(
                runner.spust_skill, a, zadani, a, vstup if cislo == 32 else None, NASTROJE[cislo])
            z = {"pripad": cislo, "beh": beh, "pokusy": pokusy, "infra_chyby": infra}
            if s is None:
                z["chyba"] = "INFRA: " + (infra[-1] if infra else "?")
            else:
                z.update(model=s["model"], skill=s["skill"], nastroje=s["nastroje"], prikazy=s["prikazy"],
                         zamitnuto=s["zamitnuto"], cteni=s["cteni"], cena=s["cena"], tokeny=s["tokeny"], vystup=s["text"])
            zaznamy.append(z)
            print(f"případ {cislo} běh {beh}: tokeny {z.get('tokeny')}", file=sys.stderr)

    cil = os.path.join(runner.VYSLEDKY, a.stitek)
    os.makedirs(cil, exist_ok=True)
    with open(os.path.join(cil, "format-vystupu.json"), "w", encoding="utf-8") as f:
        json.dump({"commit": runner._git("rev-parse", "--short", "HEAD"), "otisk": runner._otisk_skillu(),
                   "behy": zaznamy}, f, ensure_ascii=False, indent=1)
    md = [f"# Případy o formátu výstupu: {a.stitek}\n",
          f"Commit `{runner._git('rev-parse', '--short', 'HEAD')}`, otisk skillu `{runner._otisk_skillu()}`. "
          "Tvar výstupu se kontroluje ručně podle OČEKÁVÁNO v `pripady.md`.\n"]
    for z in zaznamy:
        t = z.get("tokeny") or {}
        md.append(f"## Případ {z['pripad']}, běh {z['beh']}\n")
        md.append(f"Tokeny: vstup celkem {t.get('vstup_celkem')}, výstup {t.get('vystup')}, kroků {t.get('kroku')}; "
                  f"nástroje: {', '.join(z.get('nastroje', [])) or '–'}\n")
        md.append(re.sub(r"^", "> ", z.get("vystup") or z.get("chyba") or "", flags=re.M) + "\n")
    with open(os.path.join(cil, "format-vystupu.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(md))
    print(f"Uloženo do {cil}", file=sys.stderr)


if __name__ == "__main__":
    main()
