# Výsledky evalů: k18-lide-stara

- Datum: 2026-11-23 17:59 +0100
- Commit: `fb5c2bc (neuložené změny)`, otisk skillu (bez evals): `14e8d5895fcf`
- Varianta skillu: `unslop-cs` z `../../Users/PETR~1.HUL/AppData/Local/Temp/claude/57194403cb7bd791/1370a78d-a5eb-47f5-bd0b-589d8a3debf9/scratchpad/stara-1.0.3/plugins/unslop-cs/skills/unslop-cs` (`--skill-dir`); případy z `evals/pripady.md`
- Model skillu: claude-sonnet-5-5; hodnotitel: claude-sonnet-5-5
- Běhů na případ: 3 (rozhoduje většina); UDPipe: vypnutý
- Kritérium: nejvýš 1 nález P0/P1 mimo OČEKÁVÁNO
- Opakování chyb infrastruktury: 0 navíc; nevyhodnocené běhy: 0
- Povolené nástroje skillu: `Skill Read Write Glob Grep Bash(python3 *) Bash(python *) Bash(py *)`; vstup.txt s textem případu vytváří runner
- Zamítnuté nástroje: 9 běhů z 21 (podrobnosti v `behy.json`, pole `zamitnuto`)
- Cena celkem: 3.95 USD
- Tokeny skillu na běh (medián / průměr, 21 běhů, bez hodnotitele): vstup celkem 170 463 / 148 242 (z toho zápis do cache 30 985 / 31 372, čtení z cache 139 548 / 116 863), výstup 5 095 / 5 108, kroků 4 / 4

**Prošlo 1 z 7** (čisté 1/7, ostatní 0/0).

| Případ | Typ | Výsledek | Běhy | Důvod |
|---|---|---|---|---|
| 35 – ČISTÝ: lidský sloupek z roku 2008 | čistý | prošlo | 3/3 | – |
| 36 – ČISTÝ: lidský názorový článek z roku 2015 | čistý | **neprošlo** | 1/3 | P0=1 P1=0 (2/3) |
| 43 – ČISTÝ: lidská glosa o SEO z roku 2014 | čistý | **neprošlo** | 0/3 | P0=0 P1=3 (1/3); P0=0 P1=2 (1/3); P0=0 P1=1 (1/3) |
| 44 – ČISTÝ: lidský rozhovor se šéfem akcelerátoru… | čistý | **neprošlo** | 0/3 | P0=0 P1=1 (3/3) |
| 45 – ČISTÝ: lidský sloupek o startupech z roku 20… | čistý | **neprošlo** | 1/3 | P0=0 P1=2 (1/3); P0=0 P1=1 (1/3) |
| 46 – ČISTÝ: lidská zpráva o paywallu z roku 2014 | čistý | **neprošlo** | 1/3 | P0=0 P1=1 (2/3) |
| 47 – ČISTÝ: lidský vývojářský návod z roku 2012 | čistý | **neprošlo** | 1/3 | P0=0 P1=2 (2/3) |

Důvod uvádí, co selhalo a v kolika bězích. Případ projde i s jedním neúspěšným během ze tří; důvod pak ukazuje nestabilitu. Běhy jsou vyhodnocené / celkem; nevyhodnocené běhy (chyba infrastruktury i po opakování) do většiny nepočítají. Úplné výstupy, verdikty a nálezy mimo OČEKÁVÁNO jsou v `behy.json`.
