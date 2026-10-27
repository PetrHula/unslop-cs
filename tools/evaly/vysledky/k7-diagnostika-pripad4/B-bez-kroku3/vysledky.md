# Výsledky evalů: diag4-B-bez-kroku3

- Datum: 2026-10-27 20:25 +0100
- Commit: `4e774e8 (neuložené změny)`, otisk skillu (bez evals): `df50af307fac`
- Model skillu: claude-sonnet-5-5; hodnotitel: claude-sonnet-5-5
- Běhů na případ: 10 (rozhoduje většina); UDPipe: vypnutý
- Kritérium: nejvýš 1 nález P0/P1 mimo OČEKÁVÁNO
- Opakování chyb infrastruktury: 0 navíc; nevyhodnocené běhy: 0
- Povolené nástroje skillu: `Skill Read Write Glob Grep Bash(python3 *)`; vstup.txt s textem případu vytváří runner
- Zamítnuté nástroje: 1 běhů z 10 (podrobnosti v `behy.json`, pole `zamitnuto`)
- Cena celkem: 2.75 USD
- Tokeny skillu na běh (medián / průměr, 10 běhů, bez hodnotitele): vstup celkem 182 824 / 208 216 (z toho zápis do cache 51 418 / 51 482, čtení z cache 131 086 / 156 727), výstup 2 776 / 2 862, kroků 6 / 6
- Tokeny hodnotitele na běh (zvlášť): vstup celkem 18 834 / 18 827, výstup 470 / 470
- Čtení referencí (běhů z 10, nástroj Read): `slova.md` 10, `vzorce.md` 10

**Prošlo 1 z 1** (čisté 0/0, ostatní 1/1).

| Případ | Typ | Výsledek | Běhy | Důvod |
|---|---|---|---|---|
| 4 – Pracovní e-mail | kontrola | prošlo | 10/10 | – |

Důvod uvádí, co selhalo a v kolika bězích. Případ projde i s jedním neúspěšným během ze tří; důvod pak ukazuje nestabilitu. Běhy jsou vyhodnocené / celkem; nevyhodnocené běhy (chyba infrastruktury i po opakování) do většiny nepočítají. Úplné výstupy, verdikty a nálezy mimo OČEKÁVÁNO jsou v `behy.json`.
