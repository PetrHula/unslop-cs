# Výsledky evalů: diag4-vychozi-8fd9af6

- Datum: 2026-10-27 20:20 +0100
- Commit: `8fd9af6 (neuložené změny)`, otisk skillu (bez evals): `edb8edd7fa1a`
- Model skillu: claude-sonnet-5-5; hodnotitel: claude-sonnet-5-5
- Běhů na případ: 6 (rozhoduje většina); UDPipe: vypnutý
- Kritérium: nejvýš 1 nález P0/P1 mimo OČEKÁVÁNO
- Opakování chyb infrastruktury: 0 navíc; nevyhodnocené běhy: 0
- Povolené nástroje skillu: `Skill Read Write Glob Grep Bash(python3 *)`; vstup.txt s textem případu vytváří runner
- Zamítnuté nástroje: 1 běhů z 6 (podrobnosti v `behy.json`, pole `zamitnuto`)
- Cena celkem: 1.61 USD
- Tokeny skillu na běh (medián / průměr, 6 běhů, bez hodnotitele): vstup celkem 185 328 / 208 727 (z toho zápis do cache 54 587 / 49 637, čtení z cache 130 575 / 159 084), výstup 2 836 / 2 788, kroků 6 / 6
- Tokeny hodnotitele na běh (zvlášť): vstup celkem 18 836 / 18 891, výstup 481 / 476
- Čtení referencí (běhů z 6, nástroj Read): `slova.md` 6, `vzorce.md` 5

**Prošlo 1 z 1** (čisté 0/0, ostatní 1/1).

| Případ | Typ | Výsledek | Běhy | Důvod |
|---|---|---|---|---|
| 4 – Pracovní e-mail | kontrola | prošlo | 6/6 | – |

Důvod uvádí, co selhalo a v kolika bězích. Případ projde i s jedním neúspěšným během ze tří; důvod pak ukazuje nestabilitu. Běhy jsou vyhodnocené / celkem; nevyhodnocené běhy (chyba infrastruktury i po opakování) do většiny nepočítají. Úplné výstupy, verdikty a nálezy mimo OČEKÁVÁNO jsou v `behy.json`.
