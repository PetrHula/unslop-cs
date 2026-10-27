# Výsledky evalů: k7-vychozi-tokeny

- Datum: 2026-10-27 16:07 +0100
- Commit: `21bc601`, otisk skillu (bez evals): `edb8edd7fa1a`
- Model skillu: claude-sonnet-5-5; hodnotitel: claude-sonnet-5-5
- Běhů na případ: 1 (rozhoduje většina); UDPipe: vypnutý
- Kritérium: nejvýš 1 nález P0/P1 mimo OČEKÁVÁNO
- Opakování chyb infrastruktury: 0 navíc; nevyhodnocené běhy: 0
- Povolené nástroje skillu: `Skill Read Write Glob Grep Bash(python3 *)`; vstup.txt s textem případu vytváří runner
- Zamítnuté nástroje: 0 běhů z 7 (podrobnosti v `behy.json`, pole `zamitnuto`)
- Cena celkem: 1.99 USD
- Tokeny skillu na běh (medián / průměr, 7 běhů, bez hodnotitele): vstup celkem 185 163 / 222 611 (z toho zápis do cache 56 161 / 55 599, čtení z cache 129 014 / 167 005), výstup 2 535 / 2 397, kroků 6 / 6
- Tokeny hodnotitele na běh (zvlášť): vstup celkem 18 875 / 18 816, výstup 362 / 381

**Prošlo 7 z 7** (čisté 1/1, ostatní 6/6).

| Případ | Typ | Výsledek | Běhy | Důvod |
|---|---|---|---|---|
| 1 – Příspěvek na LinkedIn | kontrola | prošlo | 1/1 | – |
| 3 – Titulky slajdů | kontrola | prošlo | 1/1 | – |
| 8 – PŘEPIS: pojistka proti vymýšlení | přepis | prošlo | 1/1 | – |
| 10 – Mravoučný příběh | kontrola | prošlo | 1/1 | – |
| 14 – ČISTÝ: odborný abstrakt | čistý | prošlo | 1/1 | – |
| 23 – PŘEPIS: postoj a konkrétnost zůstávají | přepis | prošlo | 1/1 | – |
| 29 – Blok kódu v návodu | kontrola | prošlo | 1/1 | – |

Důvod uvádí, co selhalo a v kolika bězích. Případ projde i s jedním neúspěšným během ze tří; důvod pak ukazuje nestabilitu. Běhy jsou vyhodnocené / celkem; nevyhodnocené běhy (chyba infrastruktury i po opakování) do většiny nepočítají. Úplné výstupy, verdikty a nálezy mimo OČEKÁVÁNO jsou v `behy.json`.
