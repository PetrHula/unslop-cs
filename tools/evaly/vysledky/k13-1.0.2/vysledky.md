# Výsledky evalů: k13-1.0.2

- Datum: 2026-11-19 14:12 +0100
- Commit: `1ea2dea (neuložené změny)`, otisk skillu (bez evals): `ba1b920c227e`
- Model skillu: claude-opus-5-5; hodnotitel: výchozí model claude
- Běhů na případ: 1 (rozhoduje většina); UDPipe: vypnutý
- Kritérium: nejvýš 1 nález P0/P1 mimo OČEKÁVÁNO
- Opakování chyb infrastruktury: 0 navíc; nevyhodnocené běhy: 0
- Povolené nástroje skillu: `Skill Read Write Glob Grep Bash(python3 *)`; vstup.txt s textem případu vytváří runner
- Zamítnuté nástroje: 22 běhů z 32 (podrobnosti v `behy.json`, pole `zamitnuto`)
- Cena celkem: 10.91 USD
- Tokeny skillu na běh (medián / průměr, 32 běhů, bez hodnotitele): vstup celkem 159 598 / 185 234 (z toho zápis do cache 26 974 / 29 092, čtení z cache 132 592 / 156 133), výstup 2 022 / 2 147, kroků 4 / 4
- Tokeny hodnotitele na běh (zvlášť): vstup celkem 6 584 / 6 548, výstup 573 / 561
- Výchozí běh (`--srovnat`): vstup celkem 98 667 / 100 576, výstup 1 280 / 1 423; změna mediánu: vstup +62 %, výstup +58 %
- Čtení referencí (běhů z 32, nástroj Read): `slova.md` 2, `vystup.md` 2, `vzorce.md` 1

**Prošlo 30 z 32** (čisté 11/12, ostatní 19/20).

| Případ | Typ | Výsledek | Výchozí stav | Běhy | Důvod |
|---|---|---|---|---|---|
| 1 – Příspěvek na LinkedIn | kontrola | prošlo | neprošlo ⇄ | 1/1 | – |
| 2 – Blogový odstavec s kalky | kontrola | prošlo | prošlo | 1/1 | – |
| 3 – Titulky slajdů | kontrola | prošlo | prošlo | 1/1 | – |
| 4 – Pracovní e-mail | kontrola | prošlo | neprošlo ⇄ | 1/1 | – |
| 5 – Úřednický jmenný styl | kontrola | prošlo | prošlo | 1/1 | – |
| 6 – ČISTÝ: věcný odstavec s českou typografií | čistý | prošlo | prošlo | 1/1 | – |
| 7 – Anglický otisk ve skladbě | kontrola | **neprošlo** | prošlo ⇄ | 0/1 | ř. 4 „NESMÍ označit: „Jeden kolega mi napsal“ ani „ten server“ (z…“ (1/1) |
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
| 21 – Začátky „Tento…“ a hustá síť odkazů | kontrola | prošlo | neprošlo ⇄ | 1/1 | – |
| 22 – Výhled místo výsledku | kontrola | prošlo | prošlo | 1/1 | – |
| 23 – PŘEPIS: postoj a konkrétnost zůstávají | přepis | prošlo | neprošlo ⇄ | 1/1 | – |
| 24 – ČISTÝ: částice, odbočka a otázka | čistý | prošlo | prošlo | 1/1 | – |
| 25 – PŘEPIS: sloučení vět bez nových chyb | přepis | prošlo | prošlo | 1/1 | – |
| 26 – ČISTÝ: jedno jištění a samostatné zesilovače | čistý | prošlo | prošlo | 1/1 | – |
| 27 – Shluk slov úrovně 2 | kontrola | prošlo | prošlo | 1/1 | – |
| 28 – ČISTÝ: obchodní datum a doslovné „otevřel dv… | čistý | prošlo | prošlo | 1/1 | – |
| 29 – Blok kódu v návodu | kontrola | prošlo | prošlo | 1/1 | – |
| 30 – Bloková citace třetí osoby | kontrola | prošlo | prošlo | 1/1 | – |
| 35 – ČISTÝ: lidský sloupek z roku 2008 | čistý | prošlo | – | 1/1 | – |
| 36 – ČISTÝ: lidský názorový článek z roku 2015 | čistý | **neprošlo** | – | 0/1 | P0=1 P1=1 (1/1) |

Důvod uvádí, co selhalo a v kolika bězích. Případ projde i s jedním neúspěšným během ze tří; důvod pak ukazuje nestabilitu. Běhy jsou vyhodnocené / celkem; nevyhodnocené běhy (chyba infrastruktury i po opakování) do většiny nepočítají. Úplné výstupy, verdikty a nálezy mimo OČEKÁVÁNO jsou v `behy.json`.

⇄ = výsledek se oproti výchozímu stavu změnil.
