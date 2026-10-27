# Výsledky evalů: k7-tokeny-3x

- Datum: 2026-10-27 16:19 +0100
- Commit: `b2dc6f1`, otisk skillu (bez evals): `7eff2aad6076`
- Model skillu: claude-sonnet-5-5; hodnotitel: claude-sonnet-5-5
- Běhů na případ: 3 (rozhoduje většina); UDPipe: vypnutý
- Kritérium: nejvýš 1 nález P0/P1 mimo OČEKÁVÁNO
- Opakování chyb infrastruktury: 0 navíc; nevyhodnocené běhy: 0
- Povolené nástroje skillu: `Skill Read Write Glob Grep Bash(python3 *)`; vstup.txt s textem případu vytváří runner
- Zamítnuté nástroje: 5 běhů z 21 (podrobnosti v `behy.json`, pole `zamitnuto`)
- Cena celkem: 4.95 USD
- Tokeny skillu na běh (medián / průměr, 21 běhů, bez hodnotitele): vstup celkem 178 993 / 221 033 (z toho zápis do cache 47 043 / 43 465, čtení z cache 130 592 / 177 561), výstup 2 277 / 2 348, kroků 6 / 7
- Tokeny hodnotitele na běh (zvlášť): vstup celkem 18 826 / 18 734, výstup 357 / 394
- Výchozí běh (`--srovnat`): vstup celkem 185 432 / 214 276, výstup 2 323 / 2 404; změna mediánu: vstup −3 %, výstup −2 %

**Prošlo 7 z 7** (čisté 1/1, ostatní 6/6).

| Případ | Typ | Výsledek | Výchozí stav | Běhy | Důvod |
|---|---|---|---|---|---|
| 1 – Příspěvek na LinkedIn | kontrola | prošlo | prošlo | 3/3 | – |
| 3 – Titulky slajdů | kontrola | prošlo | prošlo | 3/3 | – |
| 8 – PŘEPIS: pojistka proti vymýšlení | přepis | prošlo | prošlo | 3/3 | – |
| 10 – Mravoučný příběh | kontrola | prošlo | prošlo | 3/3 | – |
| 14 – ČISTÝ: odborný abstrakt | čistý | prošlo | prošlo | 3/3 | – |
| 23 – PŘEPIS: postoj a konkrétnost zůstávají | přepis | prošlo | prošlo | 3/3 | – |
| 29 – Blok kódu v návodu | kontrola | prošlo | prošlo | 3/3 | – |

Důvod uvádí, co selhalo a v kolika bězích. Případ projde i s jedním neúspěšným během ze tří; důvod pak ukazuje nestabilitu. Běhy jsou vyhodnocené / celkem; nevyhodnocené běhy (chyba infrastruktury i po opakování) do většiny nepočítají. Úplné výstupy, verdikty a nálezy mimo OČEKÁVÁNO jsou v `behy.json`.

⇄ = výsledek se oproti výchozímu stavu změnil.
