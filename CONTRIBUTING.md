# Jak skill upravovat

Soubor popisuje údržbu skillu `skills/unslop-cs`. Do 1.1.1 byl součástí `SKILL.md` jako oddíl Údržba skillu.

## Kde co je

- `SKILL.md` – jádro, které model čte vždy: description, princip, režimy, postup kontroly a přepisu, měření skriptem, profily registrů, závažnost, pojistky, sebekontrola a formáty výstupu. Cíl je kolem 2 500 slov; nové podrobnosti patří do referencí.
- `references/vzorce.md` – pravidla úrovní 1–3, česká skladba, vyprávění a registry, ke každému vzorci příklad před a po a chráněný podobný případ; úplné výčty tvarů P1 a P2.
- `references/slova.md` – seznamy slov s prahy, kalky, ustálené fráze, vágní autority, chatbotí artefakty, typografie a mikroformáty.
- `references/vystup.md` – úrovně výstupu a diff; `references/psani.md` – krátká verze pravidel pro režim psaní (načítá se jen v režimu Psaní).
- `references/zdroje.md` – opora pravidel.
- `scripts/metriky.py` – měřitelné kontroly; prahy převzaté ze `SKILL.md` a `slova.md` musí s nimi souhlasit; testy `python3 skills/unslop-cs/scripts/test_metriky.py`.
- `scripts/diff.py` – diff a tichá ztráta při přepisu; testy `python3 skills/unslop-cs/scripts/test_diff.py`.

Postup v `SKILL.md` výslovně říká, kdy model reference čte a kdy spouští skript (kroky 2 a 3). Když přesouváš obsah, ověř po běhu evalů v `behy.json` (pole `nastroje`), že se `Read` na reference a `Bash` se skriptem v bězích objevují.

## Pravidla úprav

- **Uč se z oprav.** Když uživatel opraví výstup nebo zreviduje dokument, zobecni každou opravu na pravidlo nebo dvojici před a po a zapracuj ji do `vzorce.md` nebo `slova.md`, výjimečně do jádra. Úpravy od lidských autorů text zlepšily víc než úpravy od modelu (Chakrabarty, Laban, Wu), proto mají skutečné opravy přednost před obecnými pravidly.
- **Jen vymyšlené příklady.** Nikdy necituj zdrojový materiál doslova v pravidlech ani příkladech; každý vzorec postav znovu s vymyšleným obsahem z jiné oblasti. Důvěrné vstupy do skillu nepatří, ani do historie gitu.
- **Opora.** Nové pravidlo potřebuje oporu v českých datech, v normě ÚJČ nebo ve výzkumu nezávislém na jazyce (`references/zdroje.md`). Anglická jazyková zjištění jsou jen hypotéza k ověření.
- **Dva příklady na vzorec.** Každý nový vzorec přichází s příkladem, který má chytit, a s podobným případem, který má nechat být. Pravidlo bez chráněného protějšku vede k přehnanému označování.
- **Verze a záznam.** Zvyš verzi (v `.claude-plugin/marketplace.json` na obou místech a v `.claude-plugin/plugin.json`) a zapiš změnu do `CHANGELOG.md`.

## Regresní kontrola

Po každé změně spusť případy z `skills/unslop-cs/evals/pripady.md` a porovnej výsledek s posledním uloženým během. Čisté případy musí zůstat čisté; přehnané označování je taky regrese.

```
python3 tools/evaly/runner.py --stitek <nazev> --model claude-sonnet-5-5 \
    --hodnotitel-model claude-sonnet-5-5 --jobs 6 \
    --srovnat tools/evaly/vysledky/<predchozi>/behy.json
```

Runner ukládá text každého případu do `vstup.txt` v pracovním adresáři modelu, protože režim `dontAsk` zamítá zápis přesměrováním a složené příkazy. Po běhu zkontroluj ve zprávě řádek „Zamítnuté nástroje“; když je počet vysoký, model skript nespustil kvůli prostředí, ne kvůli skillu (příkazy jsou v `behy.json`, pole `zamitnuto`). Chování bez připraveného souboru ověříš přepínačem `--bez-vstupu`.

Běh neprojde ani tehdy, když výstup má víc než jeden nález P0/P1 mimo řádky OČEKÁVÁNO (`--max-mimo`); srovnávej jen běhy se stejným kritériem. Chyby infrastruktury (limit session, přetížení API, timeout) runner opakuje a běhy, které ani tak neproběhnou, vede jako nevyhodnocené. Když jich je víc, počkej na obnovení limitu a pusť dotčené případy znovu.

Celý běh (30 případů × 3) stojí zhruba 23 USD a trvá kolem pěti minut. Pro rychlou zkoušku vyber případy přepínačem `--pripady 1,6,13 --behy 1`.

Po změně `references/slova.md` nebo skriptu spusť i testy skriptu (`python3 skills/unslop-cs/scripts/test_metriky.py`) a kalibraci na lidských textech (`tools/kalibrace/kalibrace_ud.py`; data UD v repozitáři nejsou, postup je v hlavičce skriptu). Položka, která dává P1 ve víc než 5 % lidských úseků, jde o úroveň níž.
