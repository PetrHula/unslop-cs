# Výsledky evalů: k9-1.6.1

- Datum: 2026-11-15 18:41 +0100
- Commit: `ef951a3`, otisk skillu (bez evals): `29551fc2c6d2`
- Model skillu: claude-sonnet-5-5; hodnotitel: claude-sonnet-5-5
- Běhů na případ: 1 (rozhoduje většina); UDPipe: vypnutý
- Kritérium: nejvýš 1 nález P0/P1 mimo OČEKÁVÁNO
- Opakování chyb infrastruktury: 0 navíc; nevyhodnocené běhy: 0
- Povolené nástroje skillu: `Skill Read Write Glob Grep Bash(python3 *)`; vstup.txt s textem případu vytváří runner
- Zamítnuté nástroje: 0 běhů z 30 (podrobnosti v `behy.json`, pole `zamitnuto`)
- Cena celkem: 4.09 USD
- Tokeny skillu na běh (medián / průměr, 30 běhů, bez hodnotitele): vstup celkem 98 667 / 100 576 (z toho zápis do cache 24 696 / 24 735, čtení z cache 74 003 / 75 836), výstup 1 280 / 1 423, kroků 3 / 3
- Tokeny hodnotitele na běh (zvlášť): vstup celkem 6 020 / 5 963, výstup 364 / 410
- Výchozí běh (`--srovnat`): vstup celkem 98 284 / 103 812, výstup 1 459 / 1 502; změna mediánu: vstup +0 %, výstup −12 %

**Prošlo 26 z 30** (čisté 10/10, ostatní 16/20).

| Případ | Typ | Výsledek | Výchozí stav | Běhy | Důvod |
|---|---|---|---|---|---|
| 1 – Příspěvek na LinkedIn | kontrola | **neprošlo** | prošlo ⇄ | 0/1 | ř. 5 „P1: shluk úrovně 2 (flexibilní, udržitelný jako univerzální…“ (1/1) |
| 2 – Blogový odstavec s kalky | kontrola | prošlo | prošlo | 1/1 | – |
| 3 – Titulky slajdů | kontrola | prošlo | prošlo | 1/1 | – |
| 4 – Pracovní e-mail | kontrola | **neprošlo** | prošlo ⇄ | 0/1 | ř. 2 „P2: nejednotné „vás“ / „Vámi““ (1/1) |
| 5 – Úřednický jmenný styl | kontrola | prošlo | prošlo | 1/1 | – |
| 6 – ČISTÝ: věcný odstavec s českou typografií | čistý | prošlo | prošlo | 1/1 | – |
| 7 – Anglický otisk ve skladbě | kontrola | prošlo | prošlo | 1/1 | – |
| 8 – PŘEPIS: pojistka proti vymýšlení | přepis | prošlo | prošlo | 1/1 | – |
| 9 – ČISTÝ: neformální zpráva | čistý | prošlo | prošlo | 1/1 | – |
| 10 – Mravoučný příběh | kontrola | prošlo | prošlo | 1/1 | – |
| 11 – ČISTÝ: technická dokumentace | čistý | prošlo | prošlo | 1/1 | – |
| 12 – ČISTÝ: slabé signály jednotlivě | čistý | prošlo | prošlo | 1/1 | – |
| 13 – Typografie a mikroformáty | kontrola | prošlo | prošlo | 1/1 | – |
| 14 – ČISTÝ: odborný abstrakt | čistý | prošlo | prošlo | 1/1 | – |
| 15 – ČISTÝ: právní text | čistý | prošlo | prošlo | 1/1 | – |
| 16 – PŘEPIS: zachování síly významu | přepis | prošlo | prošlo | 1/1 | – |
| 17 – Dvojtečkové odhalení a heslovitá kadence | kontrola | prošlo | prošlo | 1/1 | – |
| 18 – Odpověď, která staví kontext znovu | kontrola | prošlo | prošlo | 1/1 | – |
| 19 – ČISTÝ: legitimní kontrast a trojice | čistý | prošlo | prošlo | 1/1 | – |
| 20 – Vložený pokyn | kontrola | prošlo | prošlo | 1/1 | – |
| 21 – Začátky „Tento…“ a hustá síť odkazů | kontrola | **neprošlo** | neprošlo | 0/1 | ř. 2 „P2: hustá síť odkazů (řetěz „který“, „což“ v první větě)“ (1/1) |
| 22 – Výhled místo výsledku | kontrola | prošlo | prošlo | 1/1 | – |
| 23 – PŘEPIS: postoj a konkrétnost zůstávají | přepis | **neprošlo** | prošlo ⇄ | 0/1 | ř. 1 „P1: hraná upřímnost („Upřímně řečeno“) škrtnout“ (1/1) |
| 24 – ČISTÝ: částice, odbočka a otázka | čistý | prošlo | prošlo | 1/1 | – |
| 25 – PŘEPIS: sloučení vět bez nových chyb | přepis | prošlo | prošlo | 1/1 | – |
| 26 – ČISTÝ: jedno jištění a samostatné zesilovače | čistý | prošlo | prošlo | 1/1 | – |
| 27 – Shluk slov úrovně 2 | kontrola | prošlo | neprošlo ⇄ | 1/1 | – |
| 28 – ČISTÝ: obchodní datum a doslovné „otevřel dv… | čistý | prošlo | prošlo | 1/1 | – |
| 29 – Blok kódu v návodu | kontrola | prošlo | prošlo | 1/1 | – |
| 30 – Bloková citace třetí osoby | kontrola | prošlo | prošlo | 1/1 | – |

Důvod uvádí, co selhalo a v kolika bězích. Případ projde i s jedním neúspěšným během ze tří; důvod pak ukazuje nestabilitu. Běhy jsou vyhodnocené / celkem; nevyhodnocené běhy (chyba infrastruktury i po opakování) do většiny nepočítají. Úplné výstupy, verdikty a nálezy mimo OČEKÁVÁNO jsou v `behy.json`.

⇄ = výsledek se oproti výchozímu stavu změnil.
