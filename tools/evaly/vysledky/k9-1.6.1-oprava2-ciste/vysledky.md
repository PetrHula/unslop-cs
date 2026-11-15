# Výsledky evalů: k9-1.6.1-oprava2-ciste

- Datum: 2026-11-15 18:50 +0100
- Commit: `ef951a3 (neuložené změny)`, otisk skillu (bez evals): `273f03acd74d`
- Model skillu: claude-sonnet-5-5; hodnotitel: claude-sonnet-5-5
- Běhů na případ: 1 (rozhoduje většina); UDPipe: vypnutý
- Kritérium: nejvýš 1 nález P0/P1 mimo OČEKÁVÁNO
- Opakování chyb infrastruktury: 0 navíc; nevyhodnocené běhy: 0
- Povolené nástroje skillu: `Skill Read Write Glob Grep Bash(python3 *)`; vstup.txt s textem případu vytváří runner
- Zamítnuté nástroje: 0 běhů z 10 (podrobnosti v `behy.json`, pole `zamitnuto`)
- Cena celkem: 1.17 USD
- Tokeny skillu na běh (medián / průměr, 10 běhů, bez hodnotitele): vstup celkem 98 660 / 98 681 (z toho zápis do cache 24 644 / 24 663, čtení z cache 74 020 / 74 012), výstup 1 142 / 1 085, kroků 3 / 3
- Výchozí běh (`--srovnat`): vstup celkem 98 284 / 103 812, výstup 1 459 / 1 502; změna mediánu: vstup +0 %, výstup −22 %

**Prošlo 10 z 10** (čisté 10/10, ostatní 0/0).

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
| 26 – ČISTÝ: jedno jištění a samostatné zesilovače | čistý | prošlo | prošlo | 1/1 | – |
| 28 – ČISTÝ: obchodní datum a doslovné „otevřel dv… | čistý | prošlo | prošlo | 1/1 | – |

Důvod uvádí, co selhalo a v kolika bězích. Případ projde i s jedním neúspěšným během ze tří; důvod pak ukazuje nestabilitu. Běhy jsou vyhodnocené / celkem; nevyhodnocené běhy (chyba infrastruktury i po opakování) do většiny nepočítají. Úplné výstupy, verdikty a nálezy mimo OČEKÁVÁNO jsou v `behy.json`.

⇄ = výsledek se oproti výchozímu stavu změnil.
