# Výsledky evalů: k18-lide-nova

- Datum: 2026-11-23 18:04 +0100
- Commit: `fb5c2bc (neuložené změny)`, otisk skillu (bez evals): `00dbe39a329d`
- Model skillu: claude-sonnet-5-5; hodnotitel: claude-sonnet-5-5
- Běhů na případ: 3 (rozhoduje většina); UDPipe: vypnutý
- Kritérium: nejvýš 1 nález P0/P1 mimo OČEKÁVÁNO
- Opakování chyb infrastruktury: 0 navíc; nevyhodnocené běhy: 0
- Povolené nástroje skillu: `Skill Read Write Glob Grep Bash(python3 *) Bash(python *) Bash(py *)`; vstup.txt s textem případu vytváří runner
- Zamítnuté nástroje: 5 běhů z 21 (podrobnosti v `behy.json`, pole `zamitnuto`)
- Cena celkem: 4.23 USD
- Tokeny skillu na běh (medián / průměr, 21 běhů, bez hodnotitele): vstup celkem 110 895 / 141 243 (z toho zápis do cache 31 658 / 32 424, čtení z cache 79 253 / 108 811), výstup 5 225 / 6 090, kroků 3 / 3
- Výchozí běh (`--srovnat`): vstup celkem 170 463 / 148 242, výstup 5 095 / 5 108; změna mediánu: vstup −35 %, výstup +3 %

**Prošlo 3 z 7** (čisté 3/7, ostatní 0/0).

| Případ | Typ | Výsledek | Výchozí stav | Běhy | Důvod |
|---|---|---|---|---|---|
| 35 – ČISTÝ: lidský sloupek z roku 2008 | čistý | prošlo | prošlo | 3/3 | – |
| 36 – ČISTÝ: lidský názorový článek z roku 2015 | čistý | **neprošlo** | neprošlo | 1/3 | P0=1 P1=0 (1/3); P0=1 P1=1 (1/3) |
| 43 – ČISTÝ: lidská glosa o SEO z roku 2014 | čistý | **neprošlo** | neprošlo | 0/3 | P0=0 P1=6 (2/3); P0=0 P1=3 (1/3) |
| 44 – ČISTÝ: lidský rozhovor se šéfem akcelerátoru… | čistý | prošlo | neprošlo ⇄ | 3/3 | – |
| 45 – ČISTÝ: lidský sloupek o startupech z roku 20… | čistý | **neprošlo** | neprošlo | 1/3 | P0=0 P1=1 (1/3); P0=0 P1=4 (1/3) |
| 46 – ČISTÝ: lidská zpráva o paywallu z roku 2014 | čistý | prošlo | neprošlo ⇄ | 3/3 | – |
| 47 – ČISTÝ: lidský vývojářský návod z roku 2012 | čistý | **neprošlo** | neprošlo | 0/3 | P0=0 P1=1 (2/3); P0=0 P1=2 (1/3) |

Důvod uvádí, co selhalo a v kolika bězích. Případ projde i s jedním neúspěšným během ze tří; důvod pak ukazuje nestabilitu. Běhy jsou vyhodnocené / celkem; nevyhodnocené běhy (chyba infrastruktury i po opakování) do většiny nepočítají. Úplné výstupy, verdikty a nálezy mimo OČEKÁVÁNO jsou v `behy.json`.

⇄ = výsledek se oproti výchozímu stavu změnil.
