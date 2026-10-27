# Výsledky evalů: diag4-krok1-07afb71

- Datum: 2026-10-27 20:20 +0100
- Commit: `07afb71 (neuložené změny)`, otisk skillu (bez evals): `046a670926b9`
- Model skillu: claude-sonnet-5-5; hodnotitel: claude-sonnet-5-5
- Běhů na případ: 6 (rozhoduje většina); UDPipe: vypnutý
- Kritérium: nejvýš 1 nález P0/P1 mimo OČEKÁVÁNO
- Opakování chyb infrastruktury: 0 navíc; nevyhodnocené běhy: 0
- Povolené nástroje skillu: `Skill Read Write Glob Grep Bash(python3 *)`; vstup.txt s textem případu vytváří runner
- Zamítnuté nástroje: 3 běhů z 6 (podrobnosti v `behy.json`, pole `zamitnuto`)
- Cena celkem: 1.52 USD
- Tokeny skillu na běh (medián / průměr, 6 běhů, bez hodnotitele): vstup celkem 181 812 / 191 043 (z toho zápis do cache 51 164 / 46 076, čtení z cache 130 670 / 144 961), výstup 2 838 / 2 864, kroků 6 / 6
- Tokeny hodnotitele na běh (zvlášť): vstup celkem 18 885 / 18 922, výstup 480 / 489
- Čtení referencí (běhů z 6, nástroj Read): `slova.md` 5, `vzorce.md` 5

**Prošlo 0 z 1** (čisté 0/0, ostatní 0/1).

| Případ | Typ | Výsledek | Běhy | Důvod |
|---|---|---|---|---|
| 4 – Pracovní e-mail | kontrola | **neprošlo** | 3/6 | ř. 1 „P1: kalkovaný úvod („doufám, že vás tento e-mail zastihne v…“ (3/6) |

Důvod uvádí, co selhalo a v kolika bězích. Případ projde i s jedním neúspěšným během ze tří; důvod pak ukazuje nestabilitu. Běhy jsou vyhodnocené / celkem; nevyhodnocené běhy (chyba infrastruktury i po opakování) do většiny nepočítají. Úplné výstupy, verdikty a nálezy mimo OČEKÁVÁNO jsou v `behy.json`.
