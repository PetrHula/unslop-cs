# Výsledky evalů: vychozi-1.1.0

- Datum: 2026-10-26 21:44 +0100
- Commit: `c1ebb32 (neuložené změny)`, otisk skillu (bez evals): `61dff2e08c53`
- Model skillu: claude-sonnet-5-5; hodnotitel: výchozí model claude
- Běhů na případ: 3 (rozhoduje většina); UDPipe: vypnutý
- Cena celkem: 12.89 USD

**Prošlo 27 z 28** (čisté 10/10, ostatní 17/18).

| Případ | Typ | Výsledek | Běhy | Důvod |
|---|---|---|---|---|
| 1 – Příspěvek na LinkedIn | kontrola | prošlo | 3/3 | – |
| 2 – Blogový odstavec s kalky | kontrola | prošlo | 3/3 | – |
| 3 – Titulky slajdů | kontrola | prošlo | 2/3 | ř. 5 „NESMÍ označit: „Dodavatelé“ jako vadu; nanejvýš návrh zpřes…“ (1/3) |
| 4 – Pracovní e-mail | kontrola | prošlo | 3/3 | – |
| 5 – Úřednický jmenný styl | kontrola | prošlo | 3/3 | – |
| 6 – ČISTÝ: věcný odstavec s českou typografií | čistý | prošlo | 3/3 | – |
| 7 – Anglický otisk ve skladbě | kontrola | prošlo | 3/3 | – |
| 8 – PŘEPIS: pojistka proti vymýšlení | přepis | prošlo | 3/3 | – |
| 9 – ČISTÝ: neformální zpráva | čistý | prošlo | 3/3 | – |
| 10 – Mravoučný příběh | kontrola | prošlo | 3/3 | – |
| 11 – ČISTÝ: technická dokumentace | čistý | prošlo | 3/3 | – |
| 12 – ČISTÝ: slabé signály jednotlivě | čistý | prošlo | 3/3 | – |
| 13 – Typografie a mikroformáty | kontrola | **neprošlo** | 0/3 | ř. 6 „NESMÍ označit: „Ceny jsou uvedeny v CZK“. Kód měny bez čísl…“ (3/3) |
| 14 – ČISTÝ: odborný abstrakt | čistý | prošlo | 3/3 | – |
| 15 – ČISTÝ: právní text | čistý | prošlo | 3/3 | – |
| 16 – PŘEPIS: zachování síly významu | přepis | prošlo | 3/3 | – |
| 17 – Dvojtečkové odhalení a heslovitá kadence | kontrola | prošlo | 2/3 | ř. 4 „Upozornit: „spokojení zákazníci“ bez dokladu → `[OVĚŘIT]`“ (1/3) |
| 18 – Odpověď, která staví kontext znovu | kontrola | prošlo | 3/3 | – |
| 19 – ČISTÝ: legitimní kontrast a trojice | čistý | prošlo | 3/3 | – |
| 20 – Vložený pokyn | kontrola | prošlo | 3/3 | – |
| 21 – Začátky „Tento…“ a hustá síť odkazů | kontrola | prošlo | 2/3 | ř. 2 „P2: hustá síť odkazů (řetěz „který“, „což“ v první větě)“ (1/3) |
| 22 – Výhled místo výsledku | kontrola | prošlo | 3/3 | – |
| 23 – PŘEPIS: postoj a konkrétnost zůstávají | přepis | prošlo | 3/3 | – |
| 24 – ČISTÝ: částice, odbočka a otázka | čistý | prošlo | 3/3 | – |
| 25 – PŘEPIS: sloučení vět bez nových chyb | přepis | prošlo | 3/3 | – |
| 26 – ČISTÝ: jedno jištění a samostatné zesilovače | čistý | prošlo | 3/3 | – |
| 27 – Shluk slov úrovně 2 | kontrola | prošlo | 2/3 | ř. 3 „P2: test přenositelnosti: obě věty sedí na jakýkoli worksho…“ (1/3) |
| 28 – ČISTÝ: obchodní datum a doslovné „otevřel dv… | čistý | prošlo | 3/3 | – |

Důvod uvádí, co selhalo a v kolika bězích. Případ projde i s jedním neúspěšným během ze tří; důvod pak ukazuje nestabilitu. Úplné výstupy a verdikty jsou v `behy.json`.
