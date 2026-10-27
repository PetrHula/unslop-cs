# Výsledky evalů: diag-8fd9af6

- Datum: 2026-10-27 16:33 +0100
- Commit: `8fd9af6 (neuložené změny)`, otisk skillu (bez evals): `edb8edd7fa1a`
- Model skillu: claude-sonnet-5-5; hodnotitel: claude-sonnet-5-5
- Běhů na případ: 5 (rozhoduje většina); UDPipe: vypnutý
- Kritérium: nejvýš 1 nález P0/P1 mimo OČEKÁVÁNO
- Opakování chyb infrastruktury: 0 navíc; nevyhodnocené běhy: 0
- Povolené nástroje skillu: `Skill Read Write Glob Grep Bash(python3 *)`; vstup.txt s textem případu vytváří runner
- Zamítnuté nástroje: 2 běhů z 15 (podrobnosti v `behy.json`, pole `zamitnuto`)
- Cena celkem: 3.30 USD
- Tokeny skillu na běh (medián / průměr, 15 běhů, bez hodnotitele): vstup celkem 180 909 / 183 364 (z toho zápis do cache 50 390 / 42 005, čtení z cache 130 512 / 141 353), výstup 2 053 / 2 141, kroků 5 / 5
- Tokeny hodnotitele na běh (zvlášť): vstup celkem 18 784 / 18 778, výstup 474 / 473
- Čtení referencí (běhů z 15, nástroj Read): `slova.md` 12, `vzorce.md` 10

**Prošlo 3 z 3** (čisté 1/1, ostatní 2/2).

| Případ | Typ | Výsledek | Běhy | Důvod |
|---|---|---|---|---|
| 3 – Titulky slajdů | kontrola | prošlo | 5/5 | – |
| 13 – Typografie a mikroformáty | kontrola | prošlo | 5/5 | – |
| 28 – ČISTÝ: obchodní datum a doslovné „otevřel dv… | čistý | prošlo | 5/5 | – |

Důvod uvádí, co selhalo a v kolika bězích. Případ projde i s jedním neúspěšným během ze tří; důvod pak ukazuje nestabilitu. Běhy jsou vyhodnocené / celkem; nevyhodnocené běhy (chyba infrastruktury i po opakování) do většiny nepočítají. Úplné výstupy, verdikty a nálezy mimo OČEKÁVÁNO jsou v `behy.json`.
