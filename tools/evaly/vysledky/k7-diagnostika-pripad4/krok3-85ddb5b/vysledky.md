# Výsledky evalů: diag4-krok3-85ddb5b

- Datum: 2026-10-27 20:20 +0100
- Commit: `85ddb5b (neuložené změny)`, otisk skillu (bez evals): `b23883cb82c9`
- Model skillu: claude-sonnet-5-5; hodnotitel: claude-sonnet-5-5
- Běhů na případ: 6 (rozhoduje většina); UDPipe: vypnutý
- Kritérium: nejvýš 1 nález P0/P1 mimo OČEKÁVÁNO
- Opakování chyb infrastruktury: 0 navíc; nevyhodnocené běhy: 0
- Povolené nástroje skillu: `Skill Read Write Glob Grep Bash(python3 *)`; vstup.txt s textem případu vytváří runner
- Zamítnuté nástroje: 0 běhů z 6 (podrobnosti v `behy.json`, pole `zamitnuto`)
- Cena celkem: 1.63 USD
- Tokeny skillu na běh (medián / průměr, 6 běhů, bez hodnotitele): vstup celkem 222 250 / 222 258 (z toho zápis do cache 50 156 / 50 190, čtení z cache 172 016 / 172 061), výstup 2 828 / 2 850, kroků 6 / 6
- Tokeny hodnotitele na běh (zvlášť): vstup celkem 18 786 / 18 838, výstup 474 / 476
- Čtení referencí (běhů z 6, nástroj Read): `slova.md` 6, `vzorce.md` 6

**Prošlo 1 z 1** (čisté 0/0, ostatní 1/1).

| Případ | Typ | Výsledek | Běhy | Důvod |
|---|---|---|---|---|
| 4 – Pracovní e-mail | kontrola | prošlo | 4/6 | ř. 1 „P1: kalkovaný úvod („doufám, že vás tento e-mail zastihne v…“ (2/6) |

Důvod uvádí, co selhalo a v kolika bězích. Případ projde i s jedním neúspěšným během ze tří; důvod pak ukazuje nestabilitu. Běhy jsou vyhodnocené / celkem; nevyhodnocené běhy (chyba infrastruktury i po opakování) do většiny nepočítají. Úplné výstupy, verdikty a nálezy mimo OČEKÁVÁNO jsou v `behy.json`.
