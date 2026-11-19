# Výsledky evalů: k12-26-nova

- Datum: 2026-11-19 12:15 +0100
- Commit: `6ab0b41`, otisk skillu (bez evals): `eeedf9621927`
- Model skillu: claude-sonnet-5-5; hodnotitel: claude-sonnet-5-5
- Běhů na případ: 3 (rozhoduje většina); UDPipe: vypnutý
- Kritérium: nejvýš 1 nález P0/P1 mimo OČEKÁVÁNO
- Opakování chyb infrastruktury: 0 navíc; nevyhodnocené běhy: 0
- Povolené nástroje skillu: `Skill Read Write Glob Grep Bash(python3 *)`; vstup.txt s textem případu vytváří runner
- Zamítnuté nástroje: 0 běhů z 3 (podrobnosti v `behy.json`, pole `zamitnuto`)
- Cena celkem: 0.39 USD
- Tokeny skillu na běh (medián / průměr, 3 běhů, bez hodnotitele): vstup celkem 101 274 / 101 273 (z toho zápis do cache 25 682 / 25 682, čtení z cache 75 586 / 75 586), výstup 1 971 / 1 955, kroků 3 / 3

**Prošlo 1 z 1** (čisté 1/1, ostatní 0/0).

| Případ | Typ | Výsledek | Běhy | Důvod |
|---|---|---|---|---|
| 26 – ČISTÝ: jedno jištění a samostatné zesilovače | čistý | prošlo | 2/3 | P0=0 P1=1 (1/3) |

Důvod uvádí, co selhalo a v kolika bězích. Případ projde i s jedním neúspěšným během ze tří; důvod pak ukazuje nestabilitu. Běhy jsou vyhodnocené / celkem; nevyhodnocené běhy (chyba infrastruktury i po opakování) do většiny nepočítají. Úplné výstupy, verdikty a nálezy mimo OČEKÁVÁNO jsou v `behy.json`.
