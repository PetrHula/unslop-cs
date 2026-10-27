# Výsledky evalů: k7-pripad3-po-reverzu

- Datum: 2026-10-27 16:38 +0100
- Commit: `8bf7a8e (neuložené změny)`, otisk skillu (bez evals): `7be100dd0c63`
- Model skillu: claude-sonnet-5-5; hodnotitel: claude-sonnet-5-5
- Běhů na případ: 5 (rozhoduje většina); UDPipe: vypnutý
- Kritérium: nejvýš 1 nález P0/P1 mimo OČEKÁVÁNO
- Opakování chyb infrastruktury: 0 navíc; nevyhodnocené běhy: 0
- Povolené nástroje skillu: `Skill Read Write Glob Grep Bash(python3 *)`; vstup.txt s textem případu vytváří runner
- Zamítnuté nástroje: 1 běhů z 5 (podrobnosti v `behy.json`, pole `zamitnuto`)
- Cena celkem: 1.13 USD
- Tokeny skillu na běh (medián / průměr, 5 běhů, bez hodnotitele): vstup celkem 179 150 / 204 228 (z toho zápis do cache 49 509 / 40 601, čtení z cache 129 561 / 163 620), výstup 2 333 / 2 353, kroků 5 / 6
- Tokeny hodnotitele na běh (zvlášť): vstup celkem 18 787 / 18 818, výstup 423 / 416
- Čtení referencí (běhů z 5, nástroj Read): `slova.md` 3, `vzorce.md` 5

**Prošlo 1 z 1** (čisté 0/0, ostatní 1/1).

| Případ | Typ | Výsledek | Běhy | Důvod |
|---|---|---|---|---|
| 3 – Titulky slajdů | kontrola | prošlo | 5/5 | – |

Důvod uvádí, co selhalo a v kolika bězích. Případ projde i s jedním neúspěšným během ze tří; důvod pak ukazuje nestabilitu. Běhy jsou vyhodnocené / celkem; nevyhodnocené běhy (chyba infrastruktury i po opakování) do většiny nepočítají. Úplné výstupy, verdikty a nálezy mimo OČEKÁVÁNO jsou v `behy.json`.
