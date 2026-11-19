# Výsledky evalů: k13-1.0.2-pripad7

- Datum: 2026-11-19 14:17 +0100
- Commit: `1ea2dea (neuložené změny)`, otisk skillu (bez evals): `ba1b920c227e`
- Model skillu: claude-opus-5-5; hodnotitel: výchozí model claude
- Běhů na případ: 3 (rozhoduje většina); UDPipe: vypnutý
- Kritérium: nejvýš 1 nález P0/P1 mimo OČEKÁVÁNO
- Opakování chyb infrastruktury: 0 navíc; nevyhodnocené běhy: 0
- Povolené nástroje skillu: `Skill Read Write Glob Grep Bash(python3 *)`; vstup.txt s textem případu vytváří runner
- Zamítnuté nástroje: 1 běhů z 3 (podrobnosti v `behy.json`, pole `zamitnuto`)
- Cena celkem: 1.06 USD
- Tokeny skillu na běh (medián / průměr, 3 běhů, bez hodnotitele): vstup celkem 159 691 / 159 573 (z toho zápis do cache 27 208 / 27 076, čtení z cache 132 489 / 132 489), výstup 2 695 / 2 656, kroků 4 / 4
- Tokeny hodnotitele na běh (zvlášť): vstup celkem 6 792 / 6 801, výstup 566 / 554

**Prošlo 1 z 1** (čisté 0/0, ostatní 1/1).

| Případ | Typ | Výsledek | Běhy | Důvod |
|---|---|---|---|---|
| 7 – Anglický otisk ve skladbě | kontrola | prošlo | 3/3 | – |

Důvod uvádí, co selhalo a v kolika bězích. Případ projde i s jedním neúspěšným během ze tří; důvod pak ukazuje nestabilitu. Běhy jsou vyhodnocené / celkem; nevyhodnocené běhy (chyba infrastruktury i po opakování) do většiny nepočítají. Úplné výstupy, verdikty a nálezy mimo OČEKÁVÁNO jsou v `behy.json`.
