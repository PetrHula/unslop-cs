# Výsledky evalů: k19-sirsi-nova

- Datum: 2026-11-23 18:45 +0100
- Commit: `fb5c2bc (neuložené změny)`, otisk skillu (bez evals): `00dbe39a329d`
- Model skillu: claude-sonnet-5-5; hodnotitel: claude-sonnet-5-5
- Běhů na případ: 3 (rozhoduje většina); UDPipe: vypnutý
- Kritérium: nejvýš 1 nález P0/P1 mimo OČEKÁVÁNO
- Opakování chyb infrastruktury: 0 navíc; nevyhodnocené běhy: 0
- Povolené nástroje skillu: `Skill Read Write Glob Grep Bash(python3 *) Bash(python *) Bash(py *)`; vstup.txt s textem případu vytváří runner
- Zamítnuté nástroje: 7 běhů z 30 (podrobnosti v `behy.json`, pole `zamitnuto`)
- Cena celkem: 4.93 USD
- Tokeny skillu na běh (medián / průměr, 30 běhů, bez hodnotitele): vstup celkem 106 794 / 121 091 (z toho zápis do cache 29 383 / 29 812, čtení z cache 77 172 / 91 273), výstup 2 922 / 3 600, kroků 3 / 3
- Výchozí běh (`--srovnat`): vstup celkem 106 075 / 124 451, výstup 2 890 / 3 746; změna mediánu: vstup +1 %, výstup +1 %

**Prošlo 6 z 10** (čisté 6/10, ostatní 0/0).

| Případ | Typ | Výsledek | Výchozí stav | Běhy | Důvod |
|---|---|---|---|---|---|
| 48 – ČISTÝ: zpráva ČT24 z roku 2013 | čistý | prošlo | prošlo | 3/3 | – |
| 49 – ČISTÝ: zpráva ČT24 z roku 2014 | čistý | prošlo | prošlo | 3/3 | – |
| 50 – ČISTÝ: rozhlasový komentář z roku 2014 | čistý | prošlo | prošlo | 3/3 | – |
| 51 – ČISTÝ: rozhlasový komentář z roku 2014 | čistý | **neprošlo** | neprošlo | 0/3 | P0=0 P1=1 (2/3); P0=0 P1=2 (1/3) |
| 52 – ČISTÝ: popularizace vědy z roku 2013 | čistý | **neprošlo** | neprošlo | 0/3 | P0=0 P1=1 (2/3); P0=1 P1=0 (1/3) |
| 53 – ČISTÝ: fejetonový monolog z roku 2014 | čistý | prošlo | prošlo | 3/3 | – |
| 54 – ČISTÝ: vývojářský článek z roku 2013 | čistý | **neprošlo** | neprošlo | 0/3 | P0=0 P1=3 (1/3); P0=1 P1=1 (1/3); P0=0 P1=4 (1/3) |
| 55 – ČISTÝ: vývojářský komentář z roku 2014 | čistý | **neprošlo** | prošlo ⇄ | 1/3 | P0=0 P1=1 (2/3) |
| 56 – ČISTÝ: e-mail do konference z roku 2013 | čistý | prošlo | prošlo | 3/3 | – |
| 57 – ČISTÝ: e-mail do konference z roku 2014 | čistý | prošlo | prošlo | 3/3 | – |

Důvod uvádí, co selhalo a v kolika bězích. Případ projde i s jedním neúspěšným během ze tří; důvod pak ukazuje nestabilitu. Běhy jsou vyhodnocené / celkem; nevyhodnocené běhy (chyba infrastruktury i po opakování) do většiny nepočítají. Úplné výstupy, verdikty a nálezy mimo OČEKÁVÁNO jsou v `behy.json`.

⇄ = výsledek se oproti výchozímu stavu změnil.
