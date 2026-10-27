# Výsledky evalů: diag4-krok4-HEAD

- Datum: 2026-10-27 20:19 +0100
- Commit: `36ea0e2`, otisk skillu (bez evals): `7be100dd0c63`
- Model skillu: claude-sonnet-5-5; hodnotitel: claude-sonnet-5-5
- Běhů na případ: 6 (rozhoduje většina); UDPipe: vypnutý
- Kritérium: nejvýš 1 nález P0/P1 mimo OČEKÁVÁNO
- Opakování chyb infrastruktury: 0 navíc; nevyhodnocené běhy: 0
- Povolené nástroje skillu: `Skill Read Write Glob Grep Bash(python3 *)`; vstup.txt s textem případu vytváří runner
- Zamítnuté nástroje: 2 běhů z 6 (podrobnosti v `behy.json`, pole `zamitnuto`)
- Cena celkem: 1.34 USD
- Tokeny skillu na běh (medián / průměr, 6 běhů, bez hodnotitele): vstup celkem 179 510 / 169 369 (z toho zápis do cache 49 972 / 39 742, čtení z cache 129 556 / 129 621), výstup 2 514 / 2 536, kroků 6 / 6
- Tokeny hodnotitele na běh (zvlášť): vstup celkem 18 811 / 18 816, výstup 496 / 496
- Čtení referencí (běhů z 6, nástroj Read): `slova.md` 4, `vzorce.md` 4

**Prošlo 0 z 1** (čisté 0/0, ostatní 0/1).

| Případ | Typ | Výsledek | Běhy | Důvod |
|---|---|---|---|---|
| 4 – Pracovní e-mail | kontrola | **neprošlo** | 3/6 | ř. 1 „P1: kalkovaný úvod („doufám, že vás tento e-mail zastihne v…“ (2/6); hodnotitel nevrátil řádky [6] (1/6); ř. 2 „P2: nejednotné „vás“ / „Vámi““ (1/6); ř. 4 „P1: e-mail ohlašuje aktualizaci, ale žádnou neobsahuje“ (1/6) |

Důvod uvádí, co selhalo a v kolika bězích. Případ projde i s jedním neúspěšným během ze tří; důvod pak ukazuje nestabilitu. Běhy jsou vyhodnocené / celkem; nevyhodnocené běhy (chyba infrastruktury i po opakování) do většiny nepočítají. Úplné výstupy, verdikty a nálezy mimo OČEKÁVÁNO jsou v `behy.json`.
