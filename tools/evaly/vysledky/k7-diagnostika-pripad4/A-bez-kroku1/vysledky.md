# Výsledky evalů: diag4-A-bez-kroku1

- Datum: 2026-10-27 20:25 +0100
- Commit: `4e774e8 (neuložené změny)`, otisk skillu (bez evals): `db7215b1733b`
- Model skillu: claude-sonnet-5-5; hodnotitel: claude-sonnet-5-5
- Běhů na případ: 10 (rozhoduje většina); UDPipe: vypnutý
- Kritérium: nejvýš 1 nález P0/P1 mimo OČEKÁVÁNO
- Opakování chyb infrastruktury: 0 navíc; nevyhodnocené běhy: 0
- Povolené nástroje skillu: `Skill Read Write Glob Grep Bash(python3 *)`; vstup.txt s textem případu vytváří runner
- Zamítnuté nástroje: 0 běhů z 10 (podrobnosti v `behy.json`, pole `zamitnuto`)
- Cena celkem: 2.83 USD
- Tokeny skillu na běh (medián / průměr, 10 běhů, bez hodnotitele): vstup celkem 183 918 / 216 460 (z toho zápis do cache 53 773 / 52 756, čtení z cache 129 865 / 163 697), výstup 3 056 / 2 991, kroků 6 / 6
- Tokeny hodnotitele na běh (zvlášť): vstup celkem 18 858 / 18 854, výstup 484 / 480
- Čtení referencí (běhů z 10, nástroj Read): `slova.md` 10, `vzorce.md` 10

**Prošlo 1 z 1** (čisté 0/0, ostatní 1/1).

| Případ | Typ | Výsledek | Běhy | Důvod |
|---|---|---|---|---|
| 4 – Pracovní e-mail | kontrola | prošlo | 10/10 | – |

Důvod uvádí, co selhalo a v kolika bězích. Případ projde i s jedním neúspěšným během ze tří; důvod pak ukazuje nestabilitu. Běhy jsou vyhodnocené / celkem; nevyhodnocené běhy (chyba infrastruktury i po opakování) do většiny nepočítají. Úplné výstupy, verdikty a nálezy mimo OČEKÁVÁNO jsou v `behy.json`.
