# Výsledky evalů: k12-1.7.0-ciste

- Datum: 2026-11-19 12:14 +0100
- Commit: `6ab0b41`, otisk skillu (bez evals): `eeedf9621927`
- Model skillu: claude-sonnet-5-5; hodnotitel: claude-sonnet-5-5
- Běhů na případ: 2 (rozhoduje většina); UDPipe: vypnutý
- Kritérium: nejvýš 1 nález P0/P1 mimo OČEKÁVÁNO
- Opakování chyb infrastruktury: 0 navíc; nevyhodnocené běhy: 0
- Povolené nástroje skillu: `Skill Read Write Glob Grep Bash(python3 *)`; vstup.txt s textem případu vytváří runner
- Zamítnuté nástroje: 0 běhů z 26 (podrobnosti v `behy.json`, pole `zamitnuto`)
- Cena celkem: 3.45 USD
- Tokeny skillu na běh (medián / průměr, 26 běhů, bez hodnotitele): vstup celkem 101 488 / 103 641 (z toho zápis do cache 25 900 / 25 878, čtení z cache 75 599 / 77 757), výstup 1 420 / 1 476, kroků 3 / 3
- Tokeny hodnotitele na běh (zvlášť): vstup celkem 6 372 / 6 485, výstup 498 / 652
- Výchozí běh (`--srovnat`): vstup celkem 99 613 / 100 220, výstup 1 480 / 1 502; změna mediánu: vstup +2 %, výstup −4 %

**Prošlo 12 z 13** (čisté 9/10, ostatní 3/3).

| Případ | Typ | Výsledek | Výchozí stav | Běhy | Důvod |
|---|---|---|---|---|---|
| 1 – Příspěvek na LinkedIn | kontrola | prošlo | prošlo | 2/2 | – |
| 6 – ČISTÝ: věcný odstavec s českou typografií | čistý | prošlo | prošlo | 2/2 | – |
| 7 – Anglický otisk ve skladbě | kontrola | prošlo | prošlo | 2/2 | – |
| 9 – ČISTÝ: neformální zpráva | čistý | prošlo | prošlo | 2/2 | – |
| 11 – ČISTÝ: technická dokumentace | čistý | prošlo | prošlo | 2/2 | – |
| 12 – ČISTÝ: slabé signály jednotlivě | čistý | prošlo | prošlo | 2/2 | – |
| 13 – Typografie a mikroformáty | kontrola | prošlo | prošlo | 2/2 | – |
| 14 – ČISTÝ: odborný abstrakt | čistý | prošlo | prošlo | 2/2 | – |
| 15 – ČISTÝ: právní text | čistý | prošlo | prošlo | 2/2 | – |
| 19 – ČISTÝ: legitimní kontrast a trojice | čistý | prošlo | prošlo | 2/2 | – |
| 24 – ČISTÝ: částice, odbočka a otázka | čistý | prošlo | prošlo | 2/2 | – |
| 26 – ČISTÝ: jedno jištění a samostatné zesilovače | čistý | **neprošlo** | prošlo ⇄ | 0/2 | P0=0 P1=1 (2/2) |
| 28 – ČISTÝ: obchodní datum a doslovné „otevřel dv… | čistý | prošlo | prošlo | 2/2 | – |

Důvod uvádí, co selhalo a v kolika bězích. Případ projde i s jedním neúspěšným během ze tří; důvod pak ukazuje nestabilitu. Běhy jsou vyhodnocené / celkem; nevyhodnocené běhy (chyba infrastruktury i po opakování) do většiny nepočítají. Úplné výstupy, verdikty a nálezy mimo OČEKÁVÁNO jsou v `behy.json`.

⇄ = výsledek se oproti výchozímu stavu změnil.
