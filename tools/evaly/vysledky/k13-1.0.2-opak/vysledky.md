# Výsledky evalů: k13-1.0.2-opak

- Datum: 2026-11-19 14:16 +0100
- Commit: `1ea2dea (neuložené změny)`, otisk skillu (bez evals): `ba1b920c227e`
- Model skillu: claude-opus-5-5; hodnotitel: výchozí model claude
- Běhů na případ: 3 (rozhoduje většina); UDPipe: vypnutý
- Kritérium: nejvýš 1 nález P0/P1 mimo OČEKÁVÁNO
- Opakování chyb infrastruktury: 0 navíc; nevyhodnocené běhy: 0
- Povolené nástroje skillu: `Skill Read Write Glob Grep Bash(python3 *)`; vstup.txt s textem případu vytváří runner
- Zamítnuté nástroje: 10 běhů z 15 (podrobnosti v `behy.json`, pole `zamitnuto`)
- Cena celkem: 5.85 USD
- Tokeny skillu na běh (medián / průměr, 15 běhů, bez hodnotitele): vstup celkem 216 501 / 221 323 (z toho zápis do cache 31 560 / 32 327, čtení z cache 189 453 / 188 987), výstup 2 440 / 3 017, kroků 5 / 5
- Tokeny hodnotitele na běh (zvlášť): vstup celkem 6 764 / 6 553, výstup 536 / 617
- Čtení referencí (běhů z 15, nástroj Read): `vystup.md` 1, `vzorce.md` 1

**Prošlo 4 z 5** (čisté 1/2, ostatní 3/3).

| Případ | Typ | Výsledek | Běhy | Důvod |
|---|---|---|---|---|
| 4 – Pracovní e-mail | kontrola | prošlo | 3/3 | – |
| 21 – Začátky „Tento…“ a hustá síť odkazů | kontrola | prošlo | 3/3 | – |
| 23 – PŘEPIS: postoj a konkrétnost zůstávají | přepis | prošlo | 3/3 | – |
| 35 – ČISTÝ: lidský sloupek z roku 2008 | čistý | prošlo | 3/3 | – |
| 36 – ČISTÝ: lidský názorový článek z roku 2015 | čistý | **neprošlo** | 0/3 | P0=1 P1=1 (3/3) |

Důvod uvádí, co selhalo a v kolika bězích. Případ projde i s jedním neúspěšným během ze tří; důvod pak ukazuje nestabilitu. Běhy jsou vyhodnocené / celkem; nevyhodnocené běhy (chyba infrastruktury i po opakování) do většiny nepočítají. Úplné výstupy, verdikty a nálezy mimo OČEKÁVÁNO jsou v `behy.json`.
