# Výsledky evalů: k11-1.6.1-verejna

- Datum: 2026-11-18 20:44 +0100
- Commit: `7d1a189`, otisk skillu (bez evals): `e5f2a32b5852`
- Model skillu: claude-sonnet-5-5; hodnotitel: claude-sonnet-5-5
- Běhů na případ: 3 (rozhoduje většina); UDPipe: vypnutý
- Kritérium: nejvýš 1 nález P0/P1 mimo OČEKÁVÁNO
- Opakování chyb infrastruktury: 0 navíc; nevyhodnocené běhy: 0
- Povolené nástroje skillu: `Skill Read Write Glob Grep Bash(python3 *)`; vstup.txt s textem případu vytváří runner
- Zamítnuté nástroje: 1 běhů z 90 (podrobnosti v `behy.json`, pole `zamitnuto`)
- Cena celkem: 12.38 USD
- Tokeny skillu na běh (medián / průměr, 90 běhů, bez hodnotitele): vstup celkem 99 613 / 100 220 (z toho zápis do cache 24 814 / 24 801, čtení z cache 74 794 / 75 412), výstup 1 480 / 1 502, kroků 3 / 3
- Tokeny hodnotitele na běh (zvlášť): vstup celkem 6 052 / 6 145, výstup 389 / 427
- Výchozí běh (`--srovnat`): vstup celkem 98 667 / 100 576, výstup 1 280 / 1 423; změna mediánu: vstup +1 %, výstup +16 %

**Prošlo 29 z 30** (čisté 10/10, ostatní 19/20).

| Případ | Typ | Výsledek | Výchozí stav | Běhy | Důvod |
|---|---|---|---|---|---|
| 1 – Příspěvek na LinkedIn | kontrola | prošlo | neprošlo ⇄ | 3/3 | – |
| 2 – Blogový odstavec s kalky | kontrola | prošlo | prošlo | 3/3 | – |
| 3 – Titulky slajdů | kontrola | prošlo | prošlo | 2/3 | ř. 4 „P1: titulky po sobě nevyprávějí příběh prezentace“ (1/3) |
| 4 – Pracovní e-mail | kontrola | prošlo | neprošlo ⇄ | 3/3 | – |
| 5 – Úřednický jmenný styl | kontrola | prošlo | prošlo | 3/3 | – |
| 6 – ČISTÝ: věcný odstavec s českou typografií | čistý | prošlo | prošlo | 3/3 | – |
| 7 – Anglický otisk ve skladbě | kontrola | prošlo | prošlo | 3/3 | – |
| 8 – PŘEPIS: pojistka proti vymýšlení | přepis | prošlo | prošlo | 2/3 | ř. 2 „Výstup obsahuje značky `[OVĚŘIT: …]` minimálně pro „výrazně…“ (1/3) |
| 9 – ČISTÝ: neformální zpráva | čistý | prošlo | prošlo | 3/3 | – |
| 10 – Mravoučný příběh | kontrola | prošlo | prošlo | 3/3 | – |
| 11 – ČISTÝ: technická dokumentace | čistý | prošlo | prošlo | 3/3 | – |
| 12 – ČISTÝ: slabé signály jednotlivě | čistý | prošlo | prošlo | 3/3 | – |
| 13 – Typografie a mikroformáty | kontrola | prošlo | prošlo | 3/3 | – |
| 14 – ČISTÝ: odborný abstrakt | čistý | prošlo | prošlo | 3/3 | – |
| 15 – ČISTÝ: právní text | čistý | prošlo | prošlo | 3/3 | – |
| 16 – PŘEPIS: zachování síly významu | přepis | prošlo | prošlo | 3/3 | – |
| 17 – Dvojtečkové odhalení a heslovitá kadence | kontrola | prošlo | prošlo | 3/3 | – |
| 18 – Odpověď, která staví kontext znovu | kontrola | prošlo | prošlo | 3/3 | – |
| 19 – ČISTÝ: legitimní kontrast a trojice | čistý | prošlo | prošlo | 3/3 | – |
| 20 – Vložený pokyn | kontrola | prošlo | prošlo | 3/3 | – |
| 21 – Začátky „Tento…“ a hustá síť odkazů | kontrola | prošlo | neprošlo ⇄ | 2/3 | ř. 2 „P2: hustá síť odkazů (řetěz „který“, „což“ v první větě)“ (1/3) |
| 22 – Výhled místo výsledku | kontrola | prošlo | prošlo | 3/3 | – |
| 23 – PŘEPIS: postoj a konkrétnost zůstávají | přepis | prošlo | neprošlo ⇄ | 3/3 | – |
| 24 – ČISTÝ: částice, odbočka a otázka | čistý | prošlo | prošlo | 3/3 | – |
| 25 – PŘEPIS: sloučení vět bez nových chyb | přepis | prošlo | prošlo | 3/3 | – |
| 26 – ČISTÝ: jedno jištění a samostatné zesilovače | čistý | prošlo | prošlo | 3/3 | – |
| 27 – Shluk slov úrovně 2 | kontrola | prošlo | prošlo | 3/3 | – |
| 28 – ČISTÝ: obchodní datum a doslovné „otevřel dv… | čistý | prošlo | prošlo | 3/3 | – |
| 29 – Blok kódu v návodu | kontrola | **neprošlo** | prošlo ⇄ | 1/3 | ř. 3 „NESMÍ dát závažnost (P0–P2) ani navrhnout náhradu: nic z bl…“ (2/3) |
| 30 – Bloková citace třetí osoby | kontrola | prošlo | prošlo | 3/3 | – |

Důvod uvádí, co selhalo a v kolika bězích. Případ projde i s jedním neúspěšným během ze tří; důvod pak ukazuje nestabilitu. Běhy jsou vyhodnocené / celkem; nevyhodnocené běhy (chyba infrastruktury i po opakování) do většiny nepočítají. Úplné výstupy, verdikty a nálezy mimo OČEKÁVÁNO jsou v `behy.json`.

⇄ = výsledek se oproti výchozímu stavu změnil.
