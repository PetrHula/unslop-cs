# Výsledky evalů: k17-pomlcka-nazor

- Datum: 2026-11-23 16:27 +0100
- Commit: `fb5c2bc (neuložené změny)`, otisk skillu (bez evals): `00dbe39a329d`
- Model skillu: claude-sonnet-5-5; hodnotitel: claude-sonnet-5-5
- Běhů na případ: 3 (rozhoduje většina); UDPipe: vypnutý
- Kritérium: nejvýš 1 nález P0/P1 mimo OČEKÁVÁNO
- Opakování chyb infrastruktury: 0 navíc; nevyhodnocené běhy: 0
- Povolené nástroje skillu: `Skill Read Write Glob Grep Bash(python3 *) Bash(python *) Bash(py *)`; vstup.txt s textem případu vytváří runner
- Zamítnuté nástroje: 9 běhů z 30 (podrobnosti v `behy.json`, pole `zamitnuto`)
- Cena celkem: 5.49 USD
- Tokeny skillu na běh (medián / průměr, 30 běhů, bez hodnotitele): vstup celkem 105 050 / 127 975 (z toho zápis do cache 28 704 / 29 948, čtení z cache 76 354 / 98 020), výstup 2 469 / 4 045, kroků 3 / 3
- Tokeny hodnotitele na běh (zvlášť): vstup celkem 6 551 / 6 490, výstup 394 / 459
- Výchozí běh (`--srovnat`): vstup celkem 103 668 / 121 202, výstup 1 845 / 2 824; změna mediánu: vstup +1 %, výstup +34 %

**Prošlo 5 z 10** (čisté 1/5, ostatní 4/5).

| Případ | Typ | Výsledek | Výchozí stav | Běhy | Důvod |
|---|---|---|---|---|---|
| 2 – Blogový odstavec s kalky | kontrola | prošlo | – | 3/3 | – |
| 17 – Dvojtečkové odhalení a heslovitá kadence | kontrola | prošlo | – | 3/3 | – |
| 22 – Výhled místo výsledku | kontrola | prošlo | – | 3/3 | – |
| 25 – PŘEPIS: sloučení vět bez nových chyb | přepis | prošlo | – | 3/3 | – |
| 29 – Blok kódu v návodu | kontrola | **neprošlo** | – | 1/3 | ř. 3 „NESMÍ dát závažnost (P0–P2) ani navrhnout náhradu: nic z bl…“ (2/3) |
| 36 – ČISTÝ: lidský názorový článek z roku 2015 | čistý | **neprošlo** | neprošlo | 0/3 | P0=1 P1=1 (2/3); P0=1 P1=2 (1/3) |
| 43 – ČISTÝ: lidská glosa o SEO z roku 2014 | čistý | **neprošlo** | neprošlo | 0/3 | P0=0 P1=3 (2/3); P0=0 P1=8 (1/3) |
| 44 – ČISTÝ: lidský rozhovor se šéfem akcelerátoru… | čistý | prošlo | neprošlo ⇄ | 3/3 | – |
| 45 – ČISTÝ: lidský sloupek o startupech z roku 20… | čistý | **neprošlo** | neprošlo | 1/3 | P0=0 P1=1 (2/3) |
| 46 – ČISTÝ: lidská zpráva o paywallu z roku 2014 | čistý | **neprošlo** | neprošlo | 0/3 | P0=0 P1=1 (3/3) |

Důvod uvádí, co selhalo a v kolika bězích. Případ projde i s jedním neúspěšným během ze tří; důvod pak ukazuje nestabilitu. Běhy jsou vyhodnocené / celkem; nevyhodnocené běhy (chyba infrastruktury i po opakování) do většiny nepočítají. Úplné výstupy, verdikty a nálezy mimo OČEKÁVÁNO jsou v `behy.json`.

⇄ = výsledek se oproti výchozímu stavu změnil.
