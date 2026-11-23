# Výsledky evalů: k16-zaklad-spinave

- Datum: 2026-11-23 16:01 +0100
- Commit: `fb5c2bc (neuložené změny)`, otisk skillu (bez evals): `4d7053db7564`
- Model skillu: claude-sonnet-5-5; hodnotitel: claude-sonnet-5-5
- Běhů na případ: 1 (rozhoduje většina); UDPipe: vypnutý
- Kritérium: nejvýš 1 nález P0/P1 mimo OČEKÁVÁNO
- Opakování chyb infrastruktury: 0 navíc; nevyhodnocené běhy: 0
- Povolené nástroje skillu: `Skill Read Write Glob Grep Bash(python3 *) Bash(python *) Bash(py *)`; vstup.txt s textem případu vytváří runner
- Zamítnuté nástroje: 0 běhů z 20 (podrobnosti v `behy.json`, pole `zamitnuto`)
- Cena celkem: 3.27 USD
- Tokeny skillu na běh (medián / průměr, 20 běhů, bez hodnotitele): vstup celkem 103 534 / 103 537 (z toho zápis do cache 27 956 / 27 931, čtení z cache 75 593 / 75 600), výstup 1 942 / 1 913, kroků 3 / 3
- Tokeny hodnotitele na běh (zvlášť): vstup celkem 6 474 / 6 470, výstup 397 / 425
- Výchozí běh (`--srovnat`): vstup celkem 104 064 / 113 391, výstup 1 930 / 1 977; změna mediánu: vstup −1 %, výstup +1 %

**Prošlo 18 z 20** (čisté 0/0, ostatní 18/20).

| Případ | Typ | Výsledek | Výchozí stav | Běhy | Důvod |
|---|---|---|---|---|---|
| 1 – Příspěvek na LinkedIn | kontrola | prošlo | prošlo | 1/1 | – |
| 2 – Blogový odstavec s kalky | kontrola | prošlo | prošlo | 1/1 | – |
| 3 – Titulky slajdů | kontrola | **neprošlo** | prošlo ⇄ | 0/1 | ř. 4 „P1: titulky po sobě nevyprávějí příběh prezentace“ (1/1) |
| 4 – Pracovní e-mail | kontrola | prošlo | prošlo | 1/1 | – |
| 5 – Úřednický jmenný styl | kontrola | prošlo | prošlo | 1/1 | – |
| 7 – Anglický otisk ve skladbě | kontrola | prošlo | prošlo | 1/1 | – |
| 8 – PŘEPIS: pojistka proti vymýšlení | přepis | prošlo | prošlo | 1/1 | – |
| 10 – Mravoučný příběh | kontrola | prošlo | prošlo | 1/1 | – |
| 13 – Typografie a mikroformáty | kontrola | prošlo | prošlo | 1/1 | – |
| 16 – PŘEPIS: zachování síly významu | přepis | prošlo | prošlo | 1/1 | – |
| 17 – Dvojtečkové odhalení a heslovitá kadence | kontrola | prošlo | prošlo | 1/1 | – |
| 18 – Odpověď, která staví kontext znovu | kontrola | prošlo | prošlo | 1/1 | – |
| 20 – Vložený pokyn | kontrola | prošlo | prošlo | 1/1 | – |
| 21 – Začátky „Tento…“ a hustá síť odkazů | kontrola | **neprošlo** | neprošlo | 0/1 | ř. 2 „P2: hustá síť odkazů (řetěz „který“, „což“ v první větě)“ (1/1) |
| 22 – Výhled místo výsledku | kontrola | prošlo | prošlo | 1/1 | – |
| 23 – PŘEPIS: postoj a konkrétnost zůstávají | přepis | prošlo | prošlo | 1/1 | – |
| 25 – PŘEPIS: sloučení vět bez nových chyb | přepis | prošlo | prošlo | 1/1 | – |
| 27 – Shluk slov úrovně 2 | kontrola | prošlo | prošlo | 1/1 | – |
| 29 – Blok kódu v návodu | kontrola | prošlo | neprošlo ⇄ | 1/1 | – |
| 30 – Bloková citace třetí osoby | kontrola | prošlo | prošlo | 1/1 | – |

Důvod uvádí, co selhalo a v kolika bězích. Případ projde i s jedním neúspěšným během ze tří; důvod pak ukazuje nestabilitu. Běhy jsou vyhodnocené / celkem; nevyhodnocené běhy (chyba infrastruktury i po opakování) do většiny nepočítají. Úplné výstupy, verdikty a nálezy mimo OČEKÁVÁNO jsou v `behy.json`.

⇄ = výsledek se oproti výchozímu stavu změnil.
