# Výsledky evalů: diag4-krok2-2ca2bc4

- Datum: 2026-10-27 20:20 +0100
- Commit: `2ca2bc4 (neuložené změny)`, otisk skillu (bez evals): `b5a61550bbc0`
- Model skillu: claude-sonnet-5-5; hodnotitel: claude-sonnet-5-5
- Běhů na případ: 6 (rozhoduje většina); UDPipe: vypnutý
- Kritérium: nejvýš 1 nález P0/P1 mimo OČEKÁVÁNO
- Opakování chyb infrastruktury: 0 navíc; nevyhodnocené běhy: 0
- Povolené nástroje skillu: `Skill Read Write Glob Grep Bash(python3 *)`; vstup.txt s textem případu vytváří runner
- Zamítnuté nástroje: 0 běhů z 6 (podrobnosti v `behy.json`, pole `zamitnuto`)
- Cena celkem: 1.65 USD
- Tokeny skillu na běh (medián / průměr, 6 běhů, bez hodnotitele): vstup celkem 225 270 / 225 018 (z toho zápis do cache 51 288 / 51 253, čtení z cache 173 825 / 173 758), výstup 2 640 / 2 783, kroků 6 / 6
- Tokeny hodnotitele na běh (zvlášť): vstup celkem 18 822 / 18 827, výstup 464 / 462
- Čtení referencí (běhů z 6, nástroj Read): `slova.md` 6, `vzorce.md` 6

**Prošlo 1 z 1** (čisté 0/0, ostatní 1/1).

| Případ | Typ | Výsledek | Běhy | Důvod |
|---|---|---|---|---|
| 4 – Pracovní e-mail | kontrola | prošlo | 6/6 | – |

Důvod uvádí, co selhalo a v kolika bězích. Případ projde i s jedním neúspěšným během ze tří; důvod pak ukazuje nestabilitu. Běhy jsou vyhodnocené / celkem; nevyhodnocené běhy (chyba infrastruktury i po opakování) do většiny nepočítají. Úplné výstupy, verdikty a nálezy mimo OČEKÁVÁNO jsou v `behy.json`.
