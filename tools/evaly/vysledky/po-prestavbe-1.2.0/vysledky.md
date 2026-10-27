# Výsledky evalů: po-prestavbe-1.2.0

- Datum: 2026-10-27 08:46 +0100
- Commit: `cc3dfd8 (neuložené změny)`, otisk skillu (bez evals): `d67fe524a396`
- Model skillu: claude-sonnet-5-5; hodnotitel: claude-sonnet-5-5
- Běhů na případ: 3 (rozhoduje většina); UDPipe: vypnutý
- Cena celkem: 16.05 USD

**Prošlo 27 z 28** (čisté 10/10, ostatní 17/18).

| Případ | Typ | Výsledek | Výchozí stav | Běhy | Důvod |
|---|---|---|---|---|---|
| 1 – Příspěvek na LinkedIn | kontrola | prošlo | prošlo | 3/3 | – |
| 2 – Blogový odstavec s kalky | kontrola | prošlo | prošlo | 3/3 | – |
| 3 – Titulky slajdů | kontrola | **neprošlo** | prošlo ⇄ | 0/3 | ř. 4 „P1: titulky po sobě nevyprávějí příběh prezentace“ (3/3) |
| 4 – Pracovní e-mail | kontrola | prošlo | prošlo | 3/3 | – |
| 5 – Úřednický jmenný styl | kontrola | prošlo | prošlo | 3/3 | – |
| 6 – ČISTÝ: věcný odstavec s českou typografií | čistý | prošlo | prošlo | 3/3 | – |
| 7 – Anglický otisk ve skladbě | kontrola | prošlo | prošlo | 3/3 | – |
| 8 – PŘEPIS: pojistka proti vymýšlení | přepis | prošlo | prošlo | 3/3 | – |
| 9 – ČISTÝ: neformální zpráva | čistý | prošlo | prošlo | 3/3 | – |
| 10 – Mravoučný příběh | kontrola | prošlo | prošlo | 3/3 | – |
| 11 – ČISTÝ: technická dokumentace | čistý | prošlo | prošlo | 3/3 | – |
| 12 – ČISTÝ: slabé signály jednotlivě | čistý | prošlo | prošlo | 3/3 | – |
| 13 – Typografie a mikroformáty | kontrola | prošlo | neprošlo ⇄ | 3/3 | – |
| 14 – ČISTÝ: odborný abstrakt | čistý | prošlo | prošlo | 3/3 | – |
| 15 – ČISTÝ: právní text | čistý | prošlo | prošlo | 3/3 | – |
| 16 – PŘEPIS: zachování síly významu | přepis | prošlo | prošlo | 3/3 | – |
| 17 – Dvojtečkové odhalení a heslovitá kadence | kontrola | prošlo | prošlo | 3/3 | – |
| 18 – Odpověď, která staví kontext znovu | kontrola | prošlo | prošlo | 3/3 | – |
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

Důvod uvádí, co selhalo a v kolika bězích. Případ projde i s jedním neúspěšným během ze tří; důvod pak ukazuje nestabilitu. Úplné výstupy a verdikty jsou v `behy.json`.

⇄ = výsledek se oproti výchozímu stavu změnil.
