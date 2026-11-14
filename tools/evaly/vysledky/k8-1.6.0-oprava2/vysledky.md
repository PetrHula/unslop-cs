# Výsledky evalů: k8-1.6.0-oprava2

- Datum: 2026-11-14 20:28 +0100
- Commit: `1a7f834`, otisk skillu (bez evals): `67f764ff8349`
- Model skillu: claude-sonnet-5-5; hodnotitel: claude-sonnet-5-5
- Běhů na případ: 3 (rozhoduje většina); UDPipe: vypnutý
- Kritérium: nejvýš 1 nález P0/P1 mimo OČEKÁVÁNO
- Opakování chyb infrastruktury: 0 navíc; nevyhodnocené běhy: 0
- Povolené nástroje skillu: `Skill Read Write Glob Grep Bash(python3 *)`; vstup.txt s textem případu vytváří runner
- Zamítnuté nástroje: 0 běhů z 9 (podrobnosti v `behy.json`, pole `zamitnuto`)
- Cena celkem: 1.34 USD
- Tokeny skillu na běh (medián / průměr, 9 běhů, bez hodnotitele): vstup celkem 98 412 / 110 588 (z toho zápis do cache 24 403 / 24 545, čtení z cache 74 029 / 86 037), výstup 1 894 / 1 821, kroků 3 / 3
- Tokeny hodnotitele na běh (zvlášť): vstup celkem 6 089 / 6 127, výstup 438 / 428
- Výchozí běh (`--srovnat`): vstup celkem 97 886 / 102 152, výstup 1 622 / 1 595; změna mediánu: vstup +1 %, výstup +17 %

**Prošlo 3 z 3** (čisté 0/0, ostatní 3/3).

| Případ | Typ | Výsledek | Výchozí stav | Běhy | Důvod |
|---|---|---|---|---|---|
| 3 – Titulky slajdů | kontrola | prošlo | neprošlo ⇄ | 3/3 | – |
| 7 – Anglický otisk ve skladbě | kontrola | prošlo | neprošlo ⇄ | 3/3 | – |
| 18 – Odpověď, která staví kontext znovu | kontrola | prošlo | neprošlo ⇄ | 3/3 | – |

Důvod uvádí, co selhalo a v kolika bězích. Případ projde i s jedním neúspěšným během ze tří; důvod pak ukazuje nestabilitu. Běhy jsou vyhodnocené / celkem; nevyhodnocené běhy (chyba infrastruktury i po opakování) do většiny nepočítají. Úplné výstupy, verdikty a nálezy mimo OČEKÁVÁNO jsou v `behy.json`.

⇄ = výsledek se oproti výchozímu stavu změnil.
