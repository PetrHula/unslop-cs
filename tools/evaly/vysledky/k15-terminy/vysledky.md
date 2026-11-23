# Výsledky evalů: k15-terminy

- Datum: 2026-11-21 22:51 +0100
- Commit: `fb5c2bc (neuložené změny)`, otisk skillu (bez evals): `f8f27a096147`
- Model skillu: claude-sonnet-5-5; hodnotitel: claude-sonnet-5-5
- Běhů na případ: 3 (rozhoduje většina); UDPipe: vypnutý
- Kritérium: nejvýš 1 nález P0/P1 mimo OČEKÁVÁNO
- Opakování chyb infrastruktury: 0 navíc; nevyhodnocené běhy: 0
- Povolené nástroje skillu: `Skill Read Write Glob Grep Bash(python3 *) Bash(python *) Bash(py *)`; vstup.txt s textem případu vytváří runner
- Zamítnuté nástroje: 12 běhů z 69 (podrobnosti v `behy.json`, pole `zamitnuto`)
- Cena celkem: 10.95 USD
- Tokeny skillu na běh (medián / průměr, 69 běhů, bez hodnotitele): vstup celkem 103 668 / 121 202 (z toho zápis do cache 28 055 / 29 279, čtení z cache 75 624 / 91 916), výstup 1 845 / 2 824, kroků 3 / 3
- Tokeny hodnotitele na běh (zvlášť): vstup celkem 6 355 / 6 323, výstup 271 / 312
- Výchozí běh (`--srovnat`): vstup celkem 102 925 / 109 573, výstup 1 422 / 2 188; změna mediánu: vstup +1 %, výstup +30 %

**Prošlo 15 z 23** (čisté 13/19, ostatní 2/4).

| Případ | Typ | Výsledek | Výchozí stav | Běhy | Důvod |
|---|---|---|---|---|---|
| 6 – ČISTÝ: věcný odstavec s českou typografií | čistý | prošlo | prošlo | 3/3 | – |
| 9 – ČISTÝ: neformální zpráva | čistý | prošlo | prošlo | 3/3 | – |
| 11 – ČISTÝ: technická dokumentace | čistý | prošlo | prošlo | 3/3 | – |
| 12 – ČISTÝ: slabé signály jednotlivě | čistý | prošlo | prošlo | 3/3 | – |
| 14 – ČISTÝ: odborný abstrakt | čistý | prošlo | prošlo | 3/3 | – |
| 15 – ČISTÝ: právní text | čistý | prošlo | prošlo | 3/3 | – |
| 19 – ČISTÝ: legitimní kontrast a trojice | čistý | prošlo | prošlo | 3/3 | – |
| 24 – ČISTÝ: částice, odbočka a otázka | čistý | prošlo | prošlo | 2/3 | P0=0 P1=1 (1/3) |
| 26 – ČISTÝ: jedno jištění a samostatné zesilovače | čistý | **neprošlo** | neprošlo | 0/3 | P0=0 P1=1 (3/3) |
| 28 – ČISTÝ: obchodní datum a doslovné „otevřel dv… | čistý | prošlo | prošlo | 3/3 | – |
| 35 – ČISTÝ: lidský sloupek z roku 2008 | čistý | prošlo | prošlo | 3/3 | – |
| 36 – ČISTÝ: lidský názorový článek z roku 2015 | čistý | **neprošlo** | neprošlo | 1/3 | P0=1 P1=2 (2/3) |
| 37 – PŘEPIS: termíny zůstávají i v textu pro obec… | přepis | prošlo | – | 3/3 | – |
| 38 – ČISTÝ: e-mail plný vývojářských termínů | čistý | prošlo | – | 3/3 | – |
| 39 – Vymyšlený termín vedle zavedené české podoby | kontrola | **neprošlo** | – | 0/3 | ř. 2 „NESMÍ označit „platební zeď“ (česká podoba, kterou píše i l…“ (3/3) |
| 40 – Reklamní slova v dokumentaci | kontrola | prošlo | – | 3/3 | – |
| 41 – Smíšená interpunkce ve výčtu | kontrola | **neprošlo** | – | 0/3 | ř. 1 „P2: smíšená interpunkce a velká písmena v jednom výčtu (vět…“ (3/3) |
| 42 – ČISTÝ: jmenný výčet bez interpunkce | čistý | prošlo | – | 3/3 | – |
| 43 – ČISTÝ: lidská glosa o SEO z roku 2014 | čistý | **neprošlo** | – | 0/3 | P0=0 P1=1 (1/3); P0=0 P1=5 (1/3); P0=0 P1=6 (1/3) |
| 44 – ČISTÝ: lidský rozhovor se šéfem akcelerátoru… | čistý | **neprošlo** | – | 0/3 | P0=0 P1=1 (3/3) |
| 45 – ČISTÝ: lidský sloupek o startupech z roku 20… | čistý | **neprošlo** | – | 0/3 | P0=0 P1=2 (1/3); P0=0 P1=1 (1/3); P0=0 P1=3 (1/3) |
| 46 – ČISTÝ: lidská zpráva o paywallu z roku 2014 | čistý | **neprošlo** | – | 1/3 | P0=0 P1=1 (2/3) |
| 47 – ČISTÝ: lidský vývojářský návod z roku 2012 | čistý | prošlo | – | 2/3 | P0=0 P1=2 (1/3) |

Důvod uvádí, co selhalo a v kolika bězích. Případ projde i s jedním neúspěšným během ze tří; důvod pak ukazuje nestabilitu. Běhy jsou vyhodnocené / celkem; nevyhodnocené běhy (chyba infrastruktury i po opakování) do většiny nepočítají. Úplné výstupy, verdikty a nálezy mimo OČEKÁVÁNO jsou v `behy.json`.

⇄ = výsledek se oproti výchozímu stavu změnil.
