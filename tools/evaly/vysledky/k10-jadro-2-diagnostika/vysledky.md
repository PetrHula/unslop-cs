# Výsledky evalů: k10-jadro-2-diagnostika

- Datum: 2026-11-16 20:54 +0100
- Commit: `a79b79c (neuložené změny)`, otisk skillu (bez evals): `81c212c5ce05`
- Varianta skillu: `unslop-cs-jadro-2` z `tools/benchmark/varianty/unslop-cs-jadro-2` (`--skill-dir`); případy z `skills/unslop-cs/evals/pripady.md`
- Model skillu: claude-sonnet-5-5; hodnotitel: claude-sonnet-5-5
- Běhů na případ: 1 (rozhoduje většina); UDPipe: vypnutý
- Kritérium: nejvýš 1 nález P0/P1 mimo OČEKÁVÁNO
- Opakování chyb infrastruktury: 0 navíc; nevyhodnocené běhy: 0
- Povolené nástroje skillu: `Skill Read Write Glob Grep Bash(python3 *)`; vstup.txt s textem případu vytváří runner
- Zamítnuté nástroje: 0 běhů z 30 (podrobnosti v `behy.json`, pole `zamitnuto`)
- Cena celkem: 3.13 USD
- Tokeny skillu na běh (medián / průměr, 30 běhů, bez hodnotitele): vstup celkem 91 691 / 91 739 (z toho zápis do cache 17 898 / 17 910, čtení z cache 73 818 / 73 823), výstup 948 / 1 010, kroků 3 / 3
- Tokeny hodnotitele na běh (zvlášť): vstup celkem 5 894 / 5 922, výstup 424 / 430
- Výchozí běh (`--srovnat`): vstup celkem 98 667 / 100 576, výstup 1 280 / 1 423; změna mediánu: vstup −7 %, výstup −26 %

**Prošlo 22 z 30** (čisté 9/10, ostatní 13/20).

| Případ | Typ | Výsledek | Výchozí stav | Běhy | Důvod |
|---|---|---|---|---|---|
| 1 – Příspěvek na LinkedIn | kontrola | prošlo | neprošlo ⇄ | 1/1 | – |
| 2 – Blogový odstavec s kalky | kontrola | prošlo | prošlo | 1/1 | – |
| 3 – Titulky slajdů | kontrola | **neprošlo** | prošlo ⇄ | 0/1 | ř. 1 „P1: upoutávkové a hovorové titulky (1–3), návrh jmenných sp…“ (1/1); ř. 3 „P2: šablonovitý titulek „Klíčové poznatky a další kroky“ – …“ (1/1); ř. 4 „P1: titulky po sobě nevyprávějí příběh prezentace“ (1/1) |
| 4 – Pracovní e-mail | kontrola | **neprošlo** | neprošlo | 0/1 | ř. 1 „P1: kalkovaný úvod („doufám, že vás tento e-mail zastihne v…“ (1/1) |
| 5 – Úřednický jmenný styl | kontrola | prošlo | prošlo | 1/1 | – |
| 6 – ČISTÝ: věcný odstavec s českou typografií | čistý | prošlo | prošlo | 1/1 | – |
| 7 – Anglický otisk ve skladbě | kontrola | prošlo | prošlo | 1/1 | – |
| 8 – PŘEPIS: pojistka proti vymýšlení | přepis | prošlo | prošlo | 1/1 | – |
| 9 – ČISTÝ: neformální zpráva | čistý | prošlo | prošlo | 1/1 | – |
| 10 – Mravoučný příběh | kontrola | prošlo | prošlo | 1/1 | – |
| 11 – ČISTÝ: technická dokumentace | čistý | **neprošlo** | prošlo ⇄ | 0/1 | P0=0 P1=1 (1/1) |
| 12 – ČISTÝ: slabé signály jednotlivě | čistý | prošlo | prošlo | 1/1 | – |
| 13 – Typografie a mikroformáty | kontrola | **neprošlo** | prošlo ⇄ | 0/1 | ř. 6 „P2: „Ceny jsou uvedeny v CZK“ → „v Kč“. CZK je bankovní kód…“ (1/1) |
| 14 – ČISTÝ: odborný abstrakt | čistý | prošlo | prošlo | 1/1 | – |
| 15 – ČISTÝ: právní text | čistý | prošlo | prošlo | 1/1 | – |
| 16 – PŘEPIS: zachování síly významu | přepis | **neprošlo** | prošlo ⇄ | 0/1 | ř. 2 „Přepis musí zachovat: „zhruba“, „na třetinu“, „73 % žadatel…“ (1/1) |
| 17 – Dvojtečkové odhalení a heslovitá kadence | kontrola | prošlo | prošlo | 1/1 | – |
| 18 – Odpověď, která staví kontext znovu | kontrola | **neprošlo** | prošlo ⇄ | 0/1 | ř. 1 „P2: odpověď rekapituluje kontext, rozhodnutí je až na konci…“ (1/1) |
| 19 – ČISTÝ: legitimní kontrast a trojice | čistý | prošlo | prošlo | 1/1 | – |
| 20 – Vložený pokyn | kontrola | prošlo | prošlo | 1/1 | – |
| 21 – Začátky „Tento…“ a hustá síť odkazů | kontrola | prošlo | neprošlo ⇄ | 1/1 | – |
| 22 – Výhled místo výsledku | kontrola | prošlo | prošlo | 1/1 | – |
| 23 – PŘEPIS: postoj a konkrétnost zůstávají | přepis | **neprošlo** | neprošlo | 0/1 | ř. 1 „P1: hraná upřímnost („Upřímně řečeno“) škrtnout“ (1/1) |
| 24 – ČISTÝ: částice, odbočka a otázka | čistý | prošlo | prošlo | 1/1 | – |
| 25 – PŘEPIS: sloučení vět bez nových chyb | přepis | prošlo | prošlo | 1/1 | – |
| 26 – ČISTÝ: jedno jištění a samostatné zesilovače | čistý | prošlo | prošlo | 1/1 | – |
| 27 – Shluk slov úrovně 2 | kontrola | prošlo | prošlo | 1/1 | – |
| 28 – ČISTÝ: obchodní datum a doslovné „otevřel dv… | čistý | prošlo | prošlo | 1/1 | – |
| 29 – Blok kódu v návodu | kontrola | **neprošlo** | prošlo ⇄ | 0/1 | ř. 3 „NESMÍ dát závažnost (P0–P2) ani navrhnout náhradu: nic z bl…“ (1/1) |
| 30 – Bloková citace třetí osoby | kontrola | prošlo | prošlo | 1/1 | – |

Důvod uvádí, co selhalo a v kolika bězích. Případ projde i s jedním neúspěšným během ze tří; důvod pak ukazuje nestabilitu. Běhy jsou vyhodnocené / celkem; nevyhodnocené běhy (chyba infrastruktury i po opakování) do většiny nepočítají. Úplné výstupy, verdikty a nálezy mimo OČEKÁVÁNO jsou v `behy.json`.

⇄ = výsledek se oproti výchozímu stavu změnil.
