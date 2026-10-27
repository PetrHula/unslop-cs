# Výsledky evalů: k6-1.4.0

- Datum: 2026-10-27 15:17 +0100
- Commit: `8fd9af6`, otisk skillu (bez evals): `edb8edd7fa1a`
- Model skillu: claude-sonnet-5-5; hodnotitel: claude-sonnet-5-5
- Běhů na případ: 3 (rozhoduje většina); UDPipe: vypnutý
- Kritérium: nejvýš 1 nález P0/P1 mimo OČEKÁVÁNO
- Opakování chyb infrastruktury: 0 navíc; nevyhodnocené běhy: 0
- Povolené nástroje skillu: `Skill Read Write Glob Grep Bash(python3 *)`; vstup.txt s textem případu vytváří runner
- Zamítnuté nástroje: 2 běhů z 90 (podrobnosti v `behy.json`, pole `zamitnuto`)
- Cena celkem: 23.25 USD

**Prošlo 30 z 30** (čisté 10/10, ostatní 20/20).

| Případ | Typ | Výsledek | Běhy | Důvod |
|---|---|---|---|---|
| 1 – Příspěvek na LinkedIn | kontrola | prošlo | 3/3 | – |
| 2 – Blogový odstavec s kalky | kontrola | prošlo | 3/3 | – |
| 3 – Titulky slajdů | kontrola | prošlo | 3/3 | – |
| 4 – Pracovní e-mail | kontrola | prošlo | 3/3 | – |
| 5 – Úřednický jmenný styl | kontrola | prošlo | 3/3 | – |
| 6 – ČISTÝ: věcný odstavec s českou typografií | čistý | prošlo | 3/3 | – |
| 7 – Anglický otisk ve skladbě | kontrola | prošlo | 3/3 | – |
| 8 – PŘEPIS: pojistka proti vymýšlení | přepis | prošlo | 3/3 | – |
| 9 – ČISTÝ: neformální zpráva | čistý | prošlo | 3/3 | – |
| 10 – Mravoučný příběh | kontrola | prošlo | 3/3 | – |
| 11 – ČISTÝ: technická dokumentace | čistý | prošlo | 3/3 | – |
| 12 – ČISTÝ: slabé signály jednotlivě | čistý | prošlo | 3/3 | – |
| 13 – Typografie a mikroformáty | kontrola | prošlo | 3/3 | – |
| 14 – ČISTÝ: odborný abstrakt | čistý | prošlo | 3/3 | – |
| 15 – ČISTÝ: právní text | čistý | prošlo | 3/3 | – |
| 16 – PŘEPIS: zachování síly významu | přepis | prošlo | 3/3 | – |
| 17 – Dvojtečkové odhalení a heslovitá kadence | kontrola | prošlo | 3/3 | – |
| 18 – Odpověď, která staví kontext znovu | kontrola | prošlo | 3/3 | – |
| 19 – ČISTÝ: legitimní kontrast a trojice | čistý | prošlo | 3/3 | – |
| 20 – Vložený pokyn | kontrola | prošlo | 3/3 | – |
| 21 – Začátky „Tento…“ a hustá síť odkazů | kontrola | prošlo | 3/3 | – |
| 22 – Výhled místo výsledku | kontrola | prošlo | 3/3 | – |
| 23 – PŘEPIS: postoj a konkrétnost zůstávají | přepis | prošlo | 3/3 | – |
| 24 – ČISTÝ: částice, odbočka a otázka | čistý | prošlo | 3/3 | – |
| 25 – PŘEPIS: sloučení vět bez nových chyb | přepis | prošlo | 3/3 | – |
| 26 – ČISTÝ: jedno jištění a samostatné zesilovače | čistý | prošlo | 3/3 | – |
| 27 – Shluk slov úrovně 2 | kontrola | prošlo | 3/3 | – |
| 28 – ČISTÝ: obchodní datum a doslovné „otevřel dv… | čistý | prošlo | 3/3 | – |
| 29 – Blok kódu v návodu | kontrola | prošlo | 2/3 | ř. 1 „P1: kalk a úroveň 1 v textu mimo blok kódu („na denní bázi“…“ (1/3); ř. 3 „NESMÍ dát závažnost (P0–P2) ani navrhnout náhradu: nic z bl…“ (1/3) |
| 30 – Bloková citace třetí osoby | kontrola | prošlo | 3/3 | – |

Důvod uvádí, co selhalo a v kolika bězích. Případ projde i s jedním neúspěšným během ze tří; důvod pak ukazuje nestabilitu. Běhy jsou vyhodnocené / celkem; nevyhodnocené běhy (chyba infrastruktury i po opakování) do většiny nepočítají. Úplné výstupy, verdikty a nálezy mimo OČEKÁVÁNO jsou v `behy.json`.
