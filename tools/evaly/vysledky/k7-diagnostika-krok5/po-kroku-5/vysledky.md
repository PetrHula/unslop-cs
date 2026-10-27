# Výsledky evalů: diag-head

- Datum: 2026-10-27 16:33 +0100
- Commit: `ca6386b`, otisk skillu (bez evals): `7eff2aad6076`
- Model skillu: claude-sonnet-5-5; hodnotitel: claude-sonnet-5-5
- Běhů na případ: 5 (rozhoduje většina); UDPipe: vypnutý
- Kritérium: nejvýš 1 nález P0/P1 mimo OČEKÁVÁNO
- Opakování chyb infrastruktury: 0 navíc; nevyhodnocené běhy: 0
- Povolené nástroje skillu: `Skill Read Write Glob Grep Bash(python3 *)`; vstup.txt s textem případu vytváří runner
- Zamítnuté nástroje: 5 běhů z 15 (podrobnosti v `behy.json`, pole `zamitnuto`)
- Cena celkem: 2.44 USD
- Tokeny skillu na běh (medián / průměr, 15 běhů, bez hodnotitele): vstup celkem 202 795 / 197 395 (z toho zápis do cache 21 438 / 27 678, čtení z cache 182 541 / 169 710), výstup 2 007 / 1 880, kroků 5 / 6
- Tokeny hodnotitele na běh (zvlášť): vstup celkem 18 698 / 18 713, výstup 463 / 466
- Čtení referencí (běhů z 15, nástroj Read): `registry.md` 5, `slova.md` 7, `vzorce.md` 7

**Prošlo 2 z 3** (čisté 1/1, ostatní 1/2).

| Případ | Typ | Výsledek | Běhy | Důvod |
|---|---|---|---|---|
| 3 – Titulky slajdů | kontrola | **neprošlo** | 2/5 | ř. 5 „NESMÍ označit: „Dodavatelé“ jako vadu; nanejvýš návrh zpřes…“ (3/5); ř. 1 „P1: upoutávkové a hovorové titulky (1–3), návrh jmenných sp…“ (1/5); ř. 3 „P2: šablonovitý titulek „Klíčové poznatky a další kroky“ – …“ (1/5) |
| 13 – Typografie a mikroformáty | kontrola | prošlo | 5/5 | – |
| 28 – ČISTÝ: obchodní datum a doslovné „otevřel dv… | čistý | prošlo | 5/5 | – |

Důvod uvádí, co selhalo a v kolika bězích. Případ projde i s jedním neúspěšným během ze tří; důvod pak ukazuje nestabilitu. Běhy jsou vyhodnocené / celkem; nevyhodnocené běhy (chyba infrastruktury i po opakování) do většiny nepočítají. Úplné výstupy, verdikty a nálezy mimo OČEKÁVÁNO jsou v `behy.json`.
