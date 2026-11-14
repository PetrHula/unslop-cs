# Výsledky evalů: k8-1.6.0-oprava

- Datum: 2026-11-14 20:25 +0100
- Commit: `77d229f`, otisk skillu (bez evals): `a7ffd0ab1725`
- Model skillu: claude-sonnet-5-5; hodnotitel: claude-sonnet-5-5
- Běhů na případ: 3 (rozhoduje většina); UDPipe: vypnutý
- Kritérium: nejvýš 1 nález P0/P1 mimo OČEKÁVÁNO
- Opakování chyb infrastruktury: 0 navíc; nevyhodnocené běhy: 0
- Povolené nástroje skillu: `Skill Read Write Glob Grep Bash(python3 *)`; vstup.txt s textem případu vytváří runner
- Zamítnuté nástroje: 0 běhů z 18 (podrobnosti v `behy.json`, pole `zamitnuto`)
- Cena celkem: 2.60 USD
- Tokeny skillu na běh (medián / průměr, 18 běhů, bez hodnotitele): vstup celkem 98 184 / 110 293 (z toho zápis do cache 24 170 / 24 287, čtení z cache 74 014 / 86 000), výstup 1 895 / 1 806, kroků 3 / 3
- Tokeny hodnotitele na běh (zvlášť): vstup celkem 6 124 / 6 100, výstup 450 / 503
- Výchozí běh (`--srovnat`): vstup celkem 97 886 / 102 152, výstup 1 622 / 1 595; změna mediánu: vstup +0 %, výstup +17 %

**Prošlo 3 z 6** (čisté 1/1, ostatní 2/5).

| Případ | Typ | Výsledek | Výchozí stav | Běhy | Důvod |
|---|---|---|---|---|---|
| 3 – Titulky slajdů | kontrola | **neprošlo** | neprošlo | 1/3 | ř. 1 „P1: upoutávkové a hovorové titulky (1–3), návrh jmenných sp…“ (2/3) |
| 7 – Anglický otisk ve skladbě | kontrola | **neprošlo** | neprošlo | 1/3 | ř. 2 „P1: příklonka mimo své místo („řešili jsme“)“ (2/3) |
| 10 – Mravoučný příběh | kontrola | prošlo | prošlo | 3/3 | – |
| 12 – ČISTÝ: slabé signály jednotlivě | čistý | prošlo | prošlo | 3/3 | – |
| 17 – Dvojtečkové odhalení a heslovitá kadence | kontrola | prošlo | neprošlo ⇄ | 3/3 | – |
| 18 – Odpověď, která staví kontext znovu | kontrola | **neprošlo** | neprošlo | 0/3 | ř. 1 „P2: odpověď rekapituluje kontext, rozhodnutí je až na konci…“ (3/3) |

Důvod uvádí, co selhalo a v kolika bězích. Případ projde i s jedním neúspěšným během ze tří; důvod pak ukazuje nestabilitu. Běhy jsou vyhodnocené / celkem; nevyhodnocené běhy (chyba infrastruktury i po opakování) do většiny nepočítají. Úplné výstupy, verdikty a nálezy mimo OČEKÁVÁNO jsou v `behy.json`.

⇄ = výsledek se oproti výchozímu stavu změnil.
