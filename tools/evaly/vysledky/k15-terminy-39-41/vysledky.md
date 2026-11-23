# Výsledky evalů: k15-terminy-39-41

- Datum: 2026-11-21 22:53 +0100
- Commit: `fb5c2bc (neuložené změny)`, otisk skillu (bez evals): `4d7053db7564`
- Model skillu: claude-sonnet-5-5; hodnotitel: claude-sonnet-5-5
- Běhů na případ: 3 (rozhoduje většina); UDPipe: vypnutý
- Kritérium: nejvýš 1 nález P0/P1 mimo OČEKÁVÁNO
- Opakování chyb infrastruktury: 0 navíc; nevyhodnocené běhy: 0
- Povolené nástroje skillu: `Skill Read Write Glob Grep Bash(python3 *) Bash(python *) Bash(py *)`; vstup.txt s textem případu vytváří runner
- Zamítnuté nástroje: 0 běhů z 6 (podrobnosti v `behy.json`, pole `zamitnuto`)
- Cena celkem: 0.95 USD
- Tokeny skillu na běh (medián / průměr, 6 běhů, bez hodnotitele): vstup celkem 103 648 / 103 633 (z toho zápis do cache 28 044 / 28 023, čtení z cache 75 604 / 75 604), výstup 1 714 / 1 632, kroků 3 / 3
- Tokeny hodnotitele na běh (zvlášť): vstup celkem 6 104 / 6 108, výstup 240 / 235

**Prošlo 2 z 2** (čisté 0/0, ostatní 2/2).

| Případ | Typ | Výsledek | Běhy | Důvod |
|---|---|---|---|---|
| 39 – Vymyšlený termín vedle zavedené české podoby | kontrola | prošlo | 3/3 | – |
| 41 – Smíšená interpunkce ve výčtu je jiná vada | kontrola | prošlo | 3/3 | – |

Důvod uvádí, co selhalo a v kolika bězích. Případ projde i s jedním neúspěšným během ze tří; důvod pak ukazuje nestabilitu. Běhy jsou vyhodnocené / celkem; nevyhodnocené běhy (chyba infrastruktury i po opakování) do většiny nepočítají. Úplné výstupy, verdikty a nálezy mimo OČEKÁVÁNO jsou v `behy.json`.
