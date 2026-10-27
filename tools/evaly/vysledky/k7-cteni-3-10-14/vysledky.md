# Výsledky evalů: k7-cteni-3-10-14

- Datum: 2026-10-27 16:22 +0100
- Commit: `2e67d3f`, otisk skillu (bez evals): `7eff2aad6076`
- Model skillu: claude-sonnet-5-5; hodnotitel: claude-sonnet-5-5
- Běhů na případ: 3 (rozhoduje většina); UDPipe: vypnutý
- Kritérium: nejvýš 1 nález P0/P1 mimo OČEKÁVÁNO
- Opakování chyb infrastruktury: 0 navíc; nevyhodnocené běhy: 0
- Povolené nástroje skillu: `Skill Read Write Glob Grep Bash(python3 *)`; vstup.txt s textem případu vytváří runner
- Zamítnuté nástroje: 0 běhů z 9 (podrobnosti v `behy.json`, pole `zamitnuto`)
- Cena celkem: 1.93 USD
- Tokeny skillu na běh (medián / průměr, 9 běhů, bez hodnotitele): vstup celkem 208 567 / 206 768 (z toho zápis do cache 47 714 / 39 628, čtení z cache 186 498 / 167 133), výstup 2 198 / 2 258, kroků 6 / 7
- Tokeny hodnotitele na běh (zvlášť): vstup celkem 18 727 / 18 756, výstup 404 / 408
- Čtení referencí (běhů z 9, nástroj Read): `registry.md` 6, `slova.md` 6, `vypraveni.md` 3, `vzorce.md` 9

**Prošlo 3 z 3** (čisté 1/1, ostatní 2/2).

| Případ | Typ | Výsledek | Běhy | Důvod |
|---|---|---|---|---|
| 3 – Titulky slajdů | kontrola | prošlo | 2/3 | ř. 1 „P1: upoutávkové a hovorové titulky (1–3), návrh jmenných sp…“ (1/3); ř. 5 „NESMÍ označit: „Dodavatelé“ jako vadu; nanejvýš návrh zpřes…“ (1/3) |
| 10 – Mravoučný příběh | kontrola | prošlo | 3/3 | – |
| 14 – ČISTÝ: odborný abstrakt | čistý | prošlo | 3/3 | – |

Důvod uvádí, co selhalo a v kolika bězích. Případ projde i s jedním neúspěšným během ze tří; důvod pak ukazuje nestabilitu. Běhy jsou vyhodnocené / celkem; nevyhodnocené běhy (chyba infrastruktury i po opakování) do většiny nepočítají. Úplné výstupy, verdikty a nálezy mimo OČEKÁVÁNO jsou v `behy.json`.
