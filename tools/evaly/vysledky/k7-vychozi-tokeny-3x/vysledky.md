# Výsledky evalů: k7-vychozi-tokeny-3x

- Datum: 2026-10-27 16:10 +0100
- Commit: `21bc601`, otisk skillu (bez evals): `edb8edd7fa1a`
- Model skillu: claude-sonnet-5-5; hodnotitel: claude-sonnet-5-5
- Běhů na případ: 3 (rozhoduje většina); UDPipe: vypnutý
- Kritérium: nejvýš 1 nález P0/P1 mimo OČEKÁVÁNO
- Opakování chyb infrastruktury: 0 navíc; nevyhodnocené běhy: 0
- Povolené nástroje skillu: `Skill Read Write Glob Grep Bash(python3 *)`; vstup.txt s textem případu vytváří runner
- Zamítnuté nástroje: 2 běhů z 21 (podrobnosti v `behy.json`, pole `zamitnuto`)
- Cena celkem: 5.82 USD
- Tokeny skillu na běh (medián / průměr, 21 běhů, bez hodnotitele): vstup celkem 185 432 / 214 276 (z toho zápis do cache 54 260 / 53 974, čtení z cache 130 715 / 160 295), výstup 2 323 / 2 404, kroků 6 / 6
- Tokeny hodnotitele na běh (zvlášť): vstup celkem 18 971 / 19 976, výstup 328 / 402
- Výchozí běh (`--srovnat`) nemá tokeny, změna se nepočítá

**Prošlo 7 z 7** (čisté 1/1, ostatní 6/6).

| Případ | Typ | Výsledek | Výchozí stav | Běhy | Důvod |
|---|---|---|---|---|---|
| 1 – Příspěvek na LinkedIn | kontrola | prošlo | prošlo | 3/3 | – |
| 3 – Titulky slajdů | kontrola | prošlo | prošlo | 2/3 | ř. 3 „P2: šablonovitý titulek „Klíčové poznatky a další kroky“ – …“ (1/3) |
| 8 – PŘEPIS: pojistka proti vymýšlení | přepis | prošlo | prošlo | 3/3 | – |
| 10 – Mravoučný příběh | kontrola | prošlo | prošlo | 3/3 | – |
| 14 – ČISTÝ: odborný abstrakt | čistý | prošlo | prošlo | 3/3 | – |
| 23 – PŘEPIS: postoj a konkrétnost zůstávají | přepis | prošlo | prošlo | 3/3 | – |
| 29 – Blok kódu v návodu | kontrola | prošlo | prošlo | 3/3 | – |

Důvod uvádí, co selhalo a v kolika bězích. Případ projde i s jedním neúspěšným během ze tří; důvod pak ukazuje nestabilitu. Běhy jsou vyhodnocené / celkem; nevyhodnocené běhy (chyba infrastruktury i po opakování) do většiny nepočítají. Úplné výstupy, verdikty a nálezy mimo OČEKÁVÁNO jsou v `behy.json`.

⇄ = výsledek se oproti výchozímu stavu změnil.
