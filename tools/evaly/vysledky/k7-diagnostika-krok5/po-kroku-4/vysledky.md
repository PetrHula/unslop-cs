# Výsledky evalů: diag-2d93caf

- Datum: 2026-10-27 16:33 +0100
- Commit: `2d93caf (neuložené změny)`, otisk skillu (bez evals): `7be100dd0c63`
- Model skillu: claude-sonnet-5-5; hodnotitel: claude-sonnet-5-5
- Běhů na případ: 5 (rozhoduje většina); UDPipe: vypnutý
- Kritérium: nejvýš 1 nález P0/P1 mimo OČEKÁVÁNO
- Opakování chyb infrastruktury: 0 navíc; nevyhodnocené běhy: 0
- Povolené nástroje skillu: `Skill Read Write Glob Grep Bash(python3 *)`; vstup.txt s textem případu vytváří runner
- Zamítnuté nástroje: 4 běhů z 15 (podrobnosti v `behy.json`, pole `zamitnuto`)
- Cena celkem: 2.99 USD
- Tokeny skillu na běh (medián / průměr, 15 běhů, bez hodnotitele): vstup celkem 179 928 / 199 736 (z toho zápis do cache 34 654 / 36 415, čtení z cache 129 802 / 163 314), výstup 2 039 / 2 090, kroků 5 / 6
- Tokeny hodnotitele na běh (zvlášť): vstup celkem 18 676 / 18 704, výstup 462 / 454
- Čtení referencí (běhů z 15, nástroj Read): `slova.md` 11, `vzorce.md` 11

**Prošlo 3 z 3** (čisté 1/1, ostatní 2/2).

| Případ | Typ | Výsledek | Běhy | Důvod |
|---|---|---|---|---|
| 3 – Titulky slajdů | kontrola | prošlo | 5/5 | – |
| 13 – Typografie a mikroformáty | kontrola | prošlo | 5/5 | – |
| 28 – ČISTÝ: obchodní datum a doslovné „otevřel dv… | čistý | prošlo | 5/5 | – |

Důvod uvádí, co selhalo a v kolika bězích. Případ projde i s jedním neúspěšným během ze tří; důvod pak ukazuje nestabilitu. Běhy jsou vyhodnocené / celkem; nevyhodnocené běhy (chyba infrastruktury i po opakování) do většiny nepočítají. Úplné výstupy, verdikty a nálezy mimo OČEKÁVÁNO jsou v `behy.json`.
