# Výsledky evalů: k9-1.6.1-opak

- Datum: 2026-11-15 18:42 +0100
- Commit: `ef951a3`, otisk skillu (bez evals): `29551fc2c6d2`
- Model skillu: claude-sonnet-5-5; hodnotitel: claude-sonnet-5-5
- Běhů na případ: 3 (rozhoduje většina); UDPipe: vypnutý
- Kritérium: nejvýš 1 nález P0/P1 mimo OČEKÁVÁNO
- Opakování chyb infrastruktury: 0 navíc; nevyhodnocené běhy: 0
- Povolené nástroje skillu: `Skill Read Write Glob Grep Bash(python3 *)`; vstup.txt s textem případu vytváří runner
- Zamítnuté nástroje: 0 běhů z 12 (podrobnosti v `behy.json`, pole `zamitnuto`)
- Cena celkem: 1.78 USD
- Tokeny skillu na běh (medián / průměr, 12 běhů, bez hodnotitele): vstup celkem 98 704 / 98 736 (z toho zápis do cache 24 731 / 24 728, čtení z cache 74 016 / 74 002), výstup 1 874 / 1 807, kroků 3 / 3
- Tokeny hodnotitele na běh (zvlášť): vstup celkem 6 008 / 5 987, výstup 482 / 533
- Výchozí běh (`--srovnat`): vstup celkem 98 284 / 103 812, výstup 1 459 / 1 502; změna mediánu: vstup +0 %, výstup +28 %

**Prošlo 1 z 4** (čisté 0/0, ostatní 1/4).

| Případ | Typ | Výsledek | Výchozí stav | Běhy | Důvod |
|---|---|---|---|---|---|
| 1 – Příspěvek na LinkedIn | kontrola | prošlo | prošlo | 3/3 | – |
| 4 – Pracovní e-mail | kontrola | **neprošlo** | prošlo ⇄ | 1/3 | ř. 2 „P2: nejednotné „vás“ / „Vámi““ (2/3); ř. 1 „P1: kalkovaný úvod („doufám, že vás tento e-mail zastihne v…“ (1/3) |
| 21 – Začátky „Tento…“ a hustá síť odkazů | kontrola | **neprošlo** | neprošlo | 0/3 | ř. 2 „P2: hustá síť odkazů (řetěz „který“, „což“ v první větě)“ (3/3) |
| 23 – PŘEPIS: postoj a konkrétnost zůstávají | přepis | **neprošlo** | prošlo ⇄ | 0/3 | ř. 1 „P1: hraná upřímnost („Upřímně řečeno“) škrtnout“ (2/3); ř. 2 „Přepis musí zachovat částice a jištění „vlastně“, „docela“,…“ (1/3); ř. 3 „Přepis selže, když ubere částici nebo jištění, zaokrouhlí „…“ (1/3) |

Důvod uvádí, co selhalo a v kolika bězích. Případ projde i s jedním neúspěšným během ze tří; důvod pak ukazuje nestabilitu. Běhy jsou vyhodnocené / celkem; nevyhodnocené běhy (chyba infrastruktury i po opakování) do většiny nepočítají. Úplné výstupy, verdikty a nálezy mimo OČEKÁVÁNO jsou v `behy.json`.

⇄ = výsledek se oproti výchozímu stavu změnil.
