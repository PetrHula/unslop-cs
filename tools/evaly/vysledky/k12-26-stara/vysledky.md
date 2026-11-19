# Výsledky evalů: k12-26-stara

- Datum: 2026-11-19 12:15 +0100
- Commit: `6ab0b41`, otisk skillu (bez evals): `6ee7a530d403`
- Varianta skillu: `unslop-cs` z `../../Users/PETR~1.HUL/AppData/Local/Temp/claude/57194403cb7bd791/22a0631a-47bd-4347-97cf-ca836e0da6be/scratchpad/skill-161/skills/unslop-cs` (`--skill-dir`); případy z `skills/unslop-cs/evals/pripady.md`
- Model skillu: claude-sonnet-5-5; hodnotitel: claude-sonnet-5-5
- Běhů na případ: 3 (rozhoduje většina); UDPipe: vypnutý
- Kritérium: nejvýš 1 nález P0/P1 mimo OČEKÁVÁNO
- Opakování chyb infrastruktury: 0 navíc; nevyhodnocené běhy: 0
- Povolené nástroje skillu: `Skill Read Write Glob Grep Bash(python3 *)`; vstup.txt s textem případu vytváří runner
- Zamítnuté nástroje: 0 běhů z 3 (podrobnosti v `behy.json`, pole `zamitnuto`)
- Cena celkem: 0.37 USD
- Tokeny skillu na běh (medián / průměr, 3 běhů, bez hodnotitele): vstup celkem 100 770 / 100 695 (z toho zápis do cache 25 177 / 25 102, čtení z cache 75 587 / 75 587), výstup 1 646 / 1 595, kroků 3 / 3

**Prošlo 0 z 1** (čisté 0/1, ostatní 0/0).

| Případ | Typ | Výsledek | Běhy | Důvod |
|---|---|---|---|---|
| 26 – ČISTÝ: jedno jištění a samostatné zesilovače | čistý | **neprošlo** | 0/3 | P0=0 P1=1 (3/3) |

Důvod uvádí, co selhalo a v kolika bězích. Případ projde i s jedním neúspěšným během ze tří; důvod pak ukazuje nestabilitu. Běhy jsou vyhodnocené / celkem; nevyhodnocené běhy (chyba infrastruktury i po opakování) do většiny nepočítají. Úplné výstupy, verdikty a nálezy mimo OČEKÁVÁNO jsou v `behy.json`.
