# Výsledky evalů: k8-1.6.0

- Datum: 2026-11-14 20:21 +0100
- Commit: `7b6d451`, otisk skillu (bez evals): `a323c7488790`
- Model skillu: claude-sonnet-5-5; hodnotitel: claude-sonnet-5-5
- Běhů na případ: 3 (rozhoduje většina); UDPipe: vypnutý
- Kritérium: nejvýš 1 nález P0/P1 mimo OČEKÁVÁNO
- Opakování chyb infrastruktury: 0 navíc; nevyhodnocené běhy: 0
- Povolené nástroje skillu: `Skill Read Write Glob Grep Bash(python3 *)`; vstup.txt s textem případu vytváří runner
- Zamítnuté nástroje: 0 běhů z 90 (podrobnosti v `behy.json`, pole `zamitnuto`)
- Cena celkem: 12.19 USD
- Tokeny skillu na běh (medián / průměr, 90 běhů, bez hodnotitele): vstup celkem 97 886 / 102 152 (z toho zápis do cache 23 904 / 23 951, čtení z cache 74 004 / 78 195), výstup 1 622 / 1 595, kroků 3 / 3
- Tokeny hodnotitele na běh (zvlášť): vstup celkem 6 045 / 6 027, výstup 400 / 461
- Výchozí běh (`--srovnat`): vstup celkem 179 602 / 191 235, výstup 1 960 / 2 043; změna mediánu: vstup −45 %, výstup −17 %

**Prošlo 26 z 30** (čisté 10/10, ostatní 16/20).

| Případ | Typ | Výsledek | Výchozí stav | Běhy | Důvod |
|---|---|---|---|---|---|
| 1 – Příspěvek na LinkedIn | kontrola | prošlo | prošlo | 3/3 | – |
| 2 – Blogový odstavec s kalky | kontrola | prošlo | prošlo | 2/3 | mimo OČEKÁVÁNO: 2 nálezy P0/P1 (1/3); ř. 2 „P2: opis pro „je“ („představují“)“ (1/3) |
| 3 – Titulky slajdů | kontrola | **neprošlo** | prošlo ⇄ | 0/3 | ř. 5 „NESMÍ označit: „Dodavatelé“ jako vadu; nanejvýš návrh zpřes…“ (3/3) |
| 4 – Pracovní e-mail | kontrola | prošlo | neprošlo ⇄ | 3/3 | – |
| 5 – Úřednický jmenný styl | kontrola | prošlo | prošlo | 3/3 | – |
| 6 – ČISTÝ: věcný odstavec s českou typografií | čistý | prošlo | prošlo | 3/3 | – |
| 7 – Anglický otisk ve skladbě | kontrola | **neprošlo** | prošlo ⇄ | 0/3 | ř. 4 „NESMÍ označit: „Jeden kolega mi napsal“ ani „ten server“ (z…“ (2/3); mimo OČEKÁVÁNO: 2 nálezy P0/P1 (2/3); ř. 2 „P1: příklonka mimo své místo („řešili jsme“)“ (1/3) |
| 8 – PŘEPIS: pojistka proti vymýšlení | přepis | prošlo | prošlo | 3/3 | – |
| 9 – ČISTÝ: neformální zpráva | čistý | prošlo | prošlo | 3/3 | – |
| 10 – Mravoučný příběh | kontrola | prošlo | prošlo | 3/3 | – |
| 11 – ČISTÝ: technická dokumentace | čistý | prošlo | prošlo | 3/3 | – |
| 12 – ČISTÝ: slabé signály jednotlivě | čistý | prošlo | prošlo | 3/3 | – |
| 13 – Typografie a mikroformáty | kontrola | prošlo | prošlo | 3/3 | – |
| 14 – ČISTÝ: odborný abstrakt | čistý | prošlo | prošlo | 3/3 | – |
| 15 – ČISTÝ: právní text | čistý | prošlo | prošlo | 3/3 | – |
| 16 – PŘEPIS: zachování síly významu | přepis | prošlo | prošlo | 2/3 | ř. 2 „Přepis musí zachovat: „zhruba“, „na třetinu“, „73 % žadatel…“ (1/3) |
| 17 – Dvojtečkové odhalení a heslovitá kadence | kontrola | **neprošlo** | prošlo ⇄ | 1/3 | mimo OČEKÁVÁNO: 2 nálezy P0/P1 (2/3) |
| 18 – Odpověď, která staví kontext znovu | kontrola | **neprošlo** | prošlo ⇄ | 0/3 | ř. 1 „P2: odpověď rekapituluje kontext, rozhodnutí je až na konci…“ (3/3) |
| 19 – ČISTÝ: legitimní kontrast a trojice | čistý | prošlo | prošlo | 3/3 | – |
| 20 – Vložený pokyn | kontrola | prošlo | prošlo | 3/3 | – |
| 21 – Začátky „Tento…“ a hustá síť odkazů | kontrola | prošlo | prošlo | 2/3 | ř. 2 „P2: hustá síť odkazů (řetěz „který“, „což“ v první větě)“ (1/3) |
| 22 – Výhled místo výsledku | kontrola | prošlo | prošlo | 3/3 | – |
| 23 – PŘEPIS: postoj a konkrétnost zůstávají | přepis | prošlo | prošlo | 2/3 | ř. 1 „P1: hraná upřímnost („Upřímně řečeno“) škrtnout“ (1/3) |
| 24 – ČISTÝ: částice, odbočka a otázka | čistý | prošlo | prošlo | 3/3 | – |
| 25 – PŘEPIS: sloučení vět bez nových chyb | přepis | prošlo | prošlo | 3/3 | – |
| 26 – ČISTÝ: jedno jištění a samostatné zesilovače | čistý | prošlo | prošlo | 3/3 | – |
| 27 – Shluk slov úrovně 2 | kontrola | prošlo | prošlo | 3/3 | – |
| 28 – ČISTÝ: obchodní datum a doslovné „otevřel dv… | čistý | prošlo | prošlo | 3/3 | – |
| 29 – Blok kódu v návodu | kontrola | prošlo | prošlo | 2/3 | ř. 3 „NESMÍ dát závažnost (P0–P2) ani navrhnout náhradu: nic z bl…“ (1/3) |
| 30 – Bloková citace třetí osoby | kontrola | prošlo | prošlo | 3/3 | – |

Důvod uvádí, co selhalo a v kolika bězích. Případ projde i s jedním neúspěšným během ze tří; důvod pak ukazuje nestabilitu. Běhy jsou vyhodnocené / celkem; nevyhodnocené běhy (chyba infrastruktury i po opakování) do většiny nepočítají. Úplné výstupy, verdikty a nálezy mimo OČEKÁVÁNO jsou v `behy.json`.

⇄ = výsledek se oproti výchozímu stavu změnil.
