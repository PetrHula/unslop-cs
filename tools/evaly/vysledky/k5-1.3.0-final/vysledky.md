# Výsledky evalů: k5-1.3.0-final

- Datum: 2026-10-27 13:13 +0100
- Commit: `dbd78ee`, otisk skillu (bez evals): `d65ecdb73786`
- Model skillu: claude-sonnet-5-5; hodnotitel: claude-sonnet-5-5
- Běhů na případ: 3 (rozhoduje většina); UDPipe: vypnutý
- Cena celkem: 19.57 USD

**Prošlo 25 z 30** (čisté 8/10, ostatní 17/20).

| Případ | Typ | Výsledek | Výchozí stav | Běhy | Důvod |
|---|---|---|---|---|---|
| 1 – Příspěvek na LinkedIn | kontrola | prošlo | prošlo | 3/3 | – |
| 2 – Blogový odstavec s kalky | kontrola | prošlo | prošlo | 3/3 | – |
| 3 – Titulky slajdů | kontrola | prošlo | prošlo | 3/3 | – |
| 4 – Pracovní e-mail | kontrola | prošlo | prošlo | 3/3 | – |
| 5 – Úřednický jmenný styl | kontrola | prošlo | prošlo | 3/3 | – |
| 6 – ČISTÝ: věcný odstavec s českou typografií | čistý | prošlo | prošlo | 3/3 | – |
| 7 – Anglický otisk ve skladbě | kontrola | prošlo | prošlo | 2/3 | hodnotitel nevrátil řádky [1, 2, 3, 4] (1/3) |
| 8 – PŘEPIS: pojistka proti vymýšlení | přepis | prošlo | prošlo | 2/3 | ř. 2 „Výstup obsahuje značky `[OVĚŘIT: …]` minimálně pro „výrazně…“ (1/3) |
| 9 – ČISTÝ: neformální zpráva | čistý | prošlo | prošlo | 2/3 | success (1/3) |
| 10 – Mravoučný příběh | kontrola | **neprošlo** | prošlo ⇄ | 0/3 | success (3/3) |
| 11 – ČISTÝ: technická dokumentace | čistý | **neprošlo** | prošlo ⇄ | 0/3 | success (3/3) |
| 12 – ČISTÝ: slabé signály jednotlivě | čistý | **neprošlo** | prošlo ⇄ | 0/3 | success (3/3) |
| 13 – Typografie a mikroformáty | kontrola | **neprošlo** | prošlo ⇄ | 1/3 | success (2/3) |
| 14 – ČISTÝ: odborný abstrakt | čistý | prošlo | prošlo | 3/3 | – |
| 15 – ČISTÝ: právní text | čistý | prošlo | prošlo | 3/3 | – |
| 16 – PŘEPIS: zachování síly významu | přepis | prošlo | prošlo | 3/3 | – |
| 17 – Dvojtečkové odhalení a heslovitá kadence | kontrola | **neprošlo** | prošlo ⇄ | 1/3 | ř. 4 „Upozornit: „spokojení zákazníci“ bez dokladu → `[OVĚŘIT]`“ (2/3) |
| 18 – Odpověď, která staví kontext znovu | kontrola | prošlo | prošlo | 3/3 | – |
| 19 – ČISTÝ: legitimní kontrast a trojice | čistý | prošlo | prošlo | 3/3 | – |
| 20 – Vložený pokyn | kontrola | prošlo | prošlo | 3/3 | – |
| 21 – Začátky „Tento…“ a hustá síť odkazů | kontrola | prošlo | prošlo | 3/3 | – |
| 22 – Výhled místo výsledku | kontrola | prošlo | prošlo | 3/3 | – |
| 23 – PŘEPIS: postoj a konkrétnost zůstávají | přepis | prošlo | prošlo | 3/3 | – |
| 24 – ČISTÝ: částice, odbočka a otázka | čistý | prošlo | prošlo | 3/3 | – |
| 25 – PŘEPIS: sloučení vět bez nových chyb | přepis | prošlo | prošlo | 3/3 | – |
| 26 – ČISTÝ: jedno jištění a samostatné zesilovače | čistý | prošlo | prošlo | 3/3 | – |
| 27 – Shluk slov úrovně 2 | kontrola | prošlo | prošlo | 3/3 | – |
| 28 – ČISTÝ: obchodní datum a doslovné „otevřel dv… | čistý | prošlo | prošlo | 3/3 | – |
| 29 – Blok kódu v návodu | kontrola | prošlo | prošlo | 3/3 | – |
| 30 – Bloková citace třetí osoby | kontrola | prošlo | prošlo | 3/3 | – |

Důvod uvádí, co selhalo a v kolika bězích. Případ projde i s jedním neúspěšným během ze tří; důvod pak ukazuje nestabilitu. Úplné výstupy a verdikty jsou v `behy.json`.

⇄ = výsledek se oproti výchozímu stavu změnil.
