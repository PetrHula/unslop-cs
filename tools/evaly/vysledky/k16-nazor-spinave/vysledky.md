# Výsledky evalů: k16-nazor-spinave

- Datum: 2026-11-23 15:59 +0100
- Commit: `fb5c2bc (neuložené změny)`, otisk skillu (bez evals): `c5e0844c978b`
- Varianta skillu: `unslop-cs-nazor` z `tools/benchmark/varianty/unslop-cs-nazor` (`--skill-dir`); případy z `evals/pripady.md`
- Model skillu: claude-sonnet-5-5; hodnotitel: claude-sonnet-5-5
- Běhů na případ: 1 (rozhoduje většina); UDPipe: vypnutý
- Kritérium: nejvýš 1 nález P0/P1 mimo OČEKÁVÁNO
- Opakování chyb infrastruktury: 0 navíc; nevyhodnocené běhy: 0
- Povolené nástroje skillu: `Skill Read Write Glob Grep Bash(python3 *) Bash(python *) Bash(py *)`; vstup.txt s textem případu vytváří runner
- Zamítnuté nástroje: 0 běhů z 20 (podrobnosti v `behy.json`, pole `zamitnuto`)
- Cena celkem: 3.36 USD
- Tokeny skillu na běh (medián / průměr, 20 běhů, bez hodnotitele): vstup celkem 104 064 / 113 391 (z toho zápis do cache 28 479 / 28 730, čtení z cache 75 615 / 84 655), výstup 1 930 / 1 977, kroků 3 / 3
- Tokeny hodnotitele na běh (zvlášť): vstup celkem 6 466 / 6 434, výstup 371 / 383

**Prošlo 18 z 20** (čisté 0/0, ostatní 18/20).

| Případ | Typ | Výsledek | Běhy | Důvod |
|---|---|---|---|---|
| 1 – Příspěvek na LinkedIn | kontrola | prošlo | 1/1 | – |
| 2 – Blogový odstavec s kalky | kontrola | prošlo | 1/1 | – |
| 3 – Titulky slajdů | kontrola | prošlo | 1/1 | – |
| 4 – Pracovní e-mail | kontrola | prošlo | 1/1 | – |
| 5 – Úřednický jmenný styl | kontrola | prošlo | 1/1 | – |
| 7 – Anglický otisk ve skladbě | kontrola | prošlo | 1/1 | – |
| 8 – PŘEPIS: pojistka proti vymýšlení | přepis | prošlo | 1/1 | – |
| 10 – Mravoučný příběh | kontrola | prošlo | 1/1 | – |
| 13 – Typografie a mikroformáty | kontrola | prošlo | 1/1 | – |
| 16 – PŘEPIS: zachování síly významu | přepis | prošlo | 1/1 | – |
| 17 – Dvojtečkové odhalení a heslovitá kadence | kontrola | prošlo | 1/1 | – |
| 18 – Odpověď, která staví kontext znovu | kontrola | prošlo | 1/1 | – |
| 20 – Vložený pokyn | kontrola | prošlo | 1/1 | – |
| 21 – Začátky „Tento…“ a hustá síť odkazů | kontrola | **neprošlo** | 0/1 | ř. 2 „P2: hustá síť odkazů (řetěz „který“, „což“ v první větě)“ (1/1) |
| 22 – Výhled místo výsledku | kontrola | prošlo | 1/1 | – |
| 23 – PŘEPIS: postoj a konkrétnost zůstávají | přepis | prošlo | 1/1 | – |
| 25 – PŘEPIS: sloučení vět bez nových chyb | přepis | prošlo | 1/1 | – |
| 27 – Shluk slov úrovně 2 | kontrola | prošlo | 1/1 | – |
| 29 – Blok kódu v návodu | kontrola | **neprošlo** | 0/1 | ř. 2 „P1: dlouhá pomlčka „—“ bez mezer v textu mimo blok kódu („k…“ (1/1) |
| 30 – Bloková citace třetí osoby | kontrola | prošlo | 1/1 | – |

Důvod uvádí, co selhalo a v kolika bězích. Případ projde i s jedním neúspěšným během ze tří; důvod pak ukazuje nestabilitu. Běhy jsou vyhodnocené / celkem; nevyhodnocené běhy (chyba infrastruktury i po opakování) do většiny nepočítají. Úplné výstupy, verdikty a nálezy mimo OČEKÁVÁNO jsou v `behy.json`.
