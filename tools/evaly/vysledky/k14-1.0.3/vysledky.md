# Výsledky evalů: k14-1.0.3

- Datum: 2026-11-19 20:35 +0100
- Commit: `9a9aee9 (neuložené změny)`, otisk skillu (bez evals): `88cd94d1f839`
- Model skillu: claude-sonnet-5-5; hodnotitel: claude-sonnet-5-5
- Běhů na případ: 1 (rozhoduje většina); UDPipe: vypnutý
- Kritérium: nejvýš 1 nález P0/P1 mimo OČEKÁVÁNO
- Opakování chyb infrastruktury: 0 navíc; nevyhodnocené běhy: 0
- Povolené nástroje skillu: `Skill Read Write Glob Grep Bash(python3 *) Bash(python *) Bash(py *)`; vstup.txt s textem případu vytváří runner
- Zamítnuté nástroje: 1 běhů z 12 (podrobnosti v `behy.json`, pole `zamitnuto`)
- Cena celkem: 1.71 USD
- Tokeny skillu na běh (medián / průměr, 12 běhů, bez hodnotitele): vstup celkem 102 925 / 109 573 (z toho zápis do cache 27 310 / 28 070, čtení z cache 75 620 / 81 498), výstup 1 422 / 2 188, kroků 3 / 3
- Výchozí běh (`--srovnat`): vstup celkem 159 598 / 185 234, výstup 2 022 / 2 147; změna mediánu: vstup −36 %, výstup −30 %

**Prošlo 10 z 12** (čisté 10/12, ostatní 0/0).

| Případ | Typ | Výsledek | Výchozí stav | Běhy | Důvod |
|---|---|---|---|---|---|
| 6 – ČISTÝ: věcný odstavec s českou typografií | čistý | prošlo | prošlo | 1/1 | – |
| 9 – ČISTÝ: neformální zpráva | čistý | prošlo | prošlo | 1/1 | – |
| 11 – ČISTÝ: technická dokumentace | čistý | prošlo | prošlo | 1/1 | – |
| 12 – ČISTÝ: slabé signály jednotlivě | čistý | prošlo | prošlo | 1/1 | – |
| 14 – ČISTÝ: odborný abstrakt | čistý | prošlo | prošlo | 1/1 | – |
| 15 – ČISTÝ: právní text | čistý | prošlo | prošlo | 1/1 | – |
| 19 – ČISTÝ: legitimní kontrast a trojice | čistý | prošlo | prošlo | 1/1 | – |
| 24 – ČISTÝ: částice, odbočka a otázka | čistý | prošlo | prošlo | 1/1 | – |
| 26 – ČISTÝ: jedno jištění a samostatné zesilovače | čistý | **neprošlo** | prošlo ⇄ | 0/1 | P0=0 P1=1 (1/1) |
| 28 – ČISTÝ: obchodní datum a doslovné „otevřel dv… | čistý | prošlo | prošlo | 1/1 | – |
| 35 – ČISTÝ: lidský sloupek z roku 2008 | čistý | prošlo | prošlo | 1/1 | – |
| 36 – ČISTÝ: lidský názorový článek z roku 2015 | čistý | **neprošlo** | neprošlo | 0/1 | P0=1 P1=1 (1/1) |

Důvod uvádí, co selhalo a v kolika bězích. Případ projde i s jedním neúspěšným během ze tří; důvod pak ukazuje nestabilitu. Běhy jsou vyhodnocené / celkem; nevyhodnocené běhy (chyba infrastruktury i po opakování) do většiny nepočítají. Úplné výstupy, verdikty a nálezy mimo OČEKÁVÁNO jsou v `behy.json`.

⇄ = výsledek se oproti výchozímu stavu změnil.
