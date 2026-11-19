# Výsledky evalů: k13-1.0.1-publicistika

- Datum: 2026-11-19 14:05 +0100
- Commit: `1ea2dea (neuložené změny)`, otisk skillu (bez evals): `eeedf9621927`
- Model skillu: claude-opus-5-5, claude-sonnet-5-5; hodnotitel: výchozí model claude
- Běhů na případ: 3 (rozhoduje většina); UDPipe: vypnutý
- Kritérium: nejvýš 1 nález P0/P1 mimo OČEKÁVÁNO
- Opakování chyb infrastruktury: 0 navíc; nevyhodnocené běhy: 0
- Povolené nástroje skillu: `Skill Read Write Glob Grep Bash(python3 *)`; vstup.txt s textem případu vytváří runner
- Zamítnuté nástroje: 0 běhů z 6 (podrobnosti v `behy.json`, pole `zamitnuto`)
- Cena celkem: 1.54 USD
- Tokeny skillu na běh (medián / průměr, 6 běhů, bez hodnotitele): vstup celkem 174 456 / 153 969 (z toho zápis do cache 33 318 / 32 728, čtení z cache 141 131 / 121 234), výstup 4 172 / 4 212, kroků 4 / 4

**Prošlo 1 z 2** (čisté 1/2, ostatní 0/0).

| Případ | Typ | Výsledek | Běhy | Důvod |
|---|---|---|---|---|
| 35 – ČISTÝ: lidský sloupek z roku 2008 | čistý | prošlo | 3/3 | – |
| 36 – ČISTÝ: lidský názorový článek z roku 2015 | čistý | **neprošlo** | 1/3 | P0=1 P1=1 (1/3); P0=1 P1=0 (1/3) |

Důvod uvádí, co selhalo a v kolika bězích. Případ projde i s jedním neúspěšným během ze tří; důvod pak ukazuje nestabilitu. Běhy jsou vyhodnocené / celkem; nevyhodnocené běhy (chyba infrastruktury i po opakování) do většiny nepočítají. Úplné výstupy, verdikty a nálezy mimo OČEKÁVÁNO jsou v `behy.json`.
