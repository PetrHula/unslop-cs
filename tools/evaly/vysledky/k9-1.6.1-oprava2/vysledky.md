# Výsledky evalů: k9-1.6.1-oprava2

- Datum: 2026-11-15 18:49 +0100
- Commit: `ef951a3 (neuložené změny)`, otisk skillu (bez evals): `273f03acd74d`
- Model skillu: claude-sonnet-5-5; hodnotitel: claude-sonnet-5-5
- Běhů na případ: 3 (rozhoduje většina); UDPipe: vypnutý
- Kritérium: nejvýš 1 nález P0/P1 mimo OČEKÁVÁNO
- Opakování chyb infrastruktury: 0 navíc; nevyhodnocené běhy: 0
- Povolené nástroje skillu: `Skill Read Write Glob Grep Bash(python3 *)`; vstup.txt s textem případu vytváří runner
- Zamítnuté nástroje: 0 běhů z 9 (podrobnosti v `behy.json`, pole `zamitnuto`)
- Cena celkem: 1.31 USD
- Tokeny skillu na běh (medián / průměr, 9 běhů, bez hodnotitele): vstup celkem 98 897 / 110 906 (z toho zápis do cache 24 868 / 24 810, čtení z cache 74 023 / 86 089), výstup 1 487 / 1 446, kroků 3 / 3
- Tokeny hodnotitele na běh (zvlášť): vstup celkem 5 790 / 5 867, výstup 307 / 470
- Výchozí běh (`--srovnat`): vstup celkem 98 284 / 103 812, výstup 1 459 / 1 502; změna mediánu: vstup +1 %, výstup +2 %

**Prošlo 2 z 3** (čisté 0/0, ostatní 2/3).

| Případ | Typ | Výsledek | Výchozí stav | Běhy | Důvod |
|---|---|---|---|---|---|
| 4 – Pracovní e-mail | kontrola | prošlo | prošlo | 3/3 | – |
| 21 – Začátky „Tento…“ a hustá síť odkazů | kontrola | **neprošlo** | neprošlo | 0/3 | ř. 2 „P2: hustá síť odkazů (řetěz „který“, „což“ v první větě)“ (3/3); ř. 3 „NESMÍ označit: údaje „o dva dny“, „Olomouc a Zlín“; nejsou …“ (1/3) |
| 23 – PŘEPIS: postoj a konkrétnost zůstávají | přepis | prošlo | prošlo | 3/3 | – |

Důvod uvádí, co selhalo a v kolika bězích. Případ projde i s jedním neúspěšným během ze tří; důvod pak ukazuje nestabilitu. Běhy jsou vyhodnocené / celkem; nevyhodnocené běhy (chyba infrastruktury i po opakování) do většiny nepočítají. Úplné výstupy, verdikty a nálezy mimo OČEKÁVÁNO jsou v `behy.json`.

⇄ = výsledek se oproti výchozímu stavu změnil.
