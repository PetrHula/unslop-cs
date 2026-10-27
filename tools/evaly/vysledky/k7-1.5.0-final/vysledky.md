# Výsledky evalů: k7-1.5.0-final

- Datum: 2026-10-27 20:14 +0100
- Commit: `36ea0e2`, otisk skillu (bez evals): `7be100dd0c63`
- Model skillu: claude-sonnet-5-5; hodnotitel: claude-sonnet-5-5
- Běhů na případ: 3 (rozhoduje většina); UDPipe: vypnutý
- Kritérium: nejvýš 1 nález P0/P1 mimo OČEKÁVÁNO
- Opakování chyb infrastruktury: 0 navíc; nevyhodnocené běhy: 0
- Povolené nástroje skillu: `Skill Read Write Glob Grep Bash(python3 *)`; vstup.txt s textem případu vytváří runner
- Zamítnuté nástroje: 12 běhů z 90 (podrobnosti v `behy.json`, pole `zamitnuto`)
- Cena celkem: 23.28 USD
- Tokeny skillu na běh (medián / průměr, 90 běhů, bez hodnotitele): vstup celkem 179 602 / 191 235 (z toho zápis do cache 50 394 / 51 842, čtení z cache 129 560 / 139 387), výstup 1 960 / 2 043, kroků 5 / 6
- Tokeny hodnotitele na běh (zvlášť): vstup celkem 18 667 / 18 657, výstup 350 / 368
- Výchozí běh (`--srovnat`) nemá tokeny, změna se nepočítá
- Čtení referencí (běhů z 90, nástroj Read): `slova.md` 86, `vystup.md` 11, `vzorce.md` 87

**Prošlo 29 z 30** (čisté 10/10, ostatní 19/20).

| Případ | Typ | Výsledek | Výchozí stav | Běhy | Důvod |
|---|---|---|---|---|---|
| 1 – Příspěvek na LinkedIn | kontrola | prošlo | prošlo | 3/3 | – |
| 2 – Blogový odstavec s kalky | kontrola | prošlo | prošlo | 3/3 | – |
| 3 – Titulky slajdů | kontrola | prošlo | prošlo | 3/3 | – |
| 4 – Pracovní e-mail | kontrola | **neprošlo** | prošlo ⇄ | 1/3 | ř. 1 „P1: kalkovaný úvod („doufám, že vás tento e-mail zastihne v…“ (2/3) |
| 5 – Úřednický jmenný styl | kontrola | prošlo | prošlo | 3/3 | – |
| 6 – ČISTÝ: věcný odstavec s českou typografií | čistý | prošlo | prošlo | 3/3 | – |
| 7 – Anglický otisk ve skladbě | kontrola | prošlo | prošlo | 3/3 | – |
| 8 – PŘEPIS: pojistka proti vymýšlení | přepis | prošlo | prošlo | 3/3 | – |
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

Důvod uvádí, co selhalo a v kolika bězích. Případ projde i s jedním neúspěšným během ze tří; důvod pak ukazuje nestabilitu. Běhy jsou vyhodnocené / celkem; nevyhodnocené běhy (chyba infrastruktury i po opakování) do většiny nepočítají. Úplné výstupy, verdikty a nálezy mimo OČEKÁVÁNO jsou v `behy.json`.

⇄ = výsledek se oproti výchozímu stavu změnil.
