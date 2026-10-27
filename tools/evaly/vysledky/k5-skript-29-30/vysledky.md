# Výsledky evalů: k5-skript-29-30

- Datum: 2026-10-27 10:24 +0100
- Commit: `0bc99c2 (neuložené změny)`, otisk skillu (bez evals): `e67a1acb1651`
- Model skillu: claude-sonnet-5-5; hodnotitel: claude-sonnet-5-5
- Běhů na případ: 3 (rozhoduje většina); UDPipe: vypnutý
- Cena celkem: 1.64 USD

**Prošlo 1 z 2** (čisté 0/0, ostatní 1/2).

| Případ | Typ | Výsledek | Výchozí stav | Běhy | Důvod |
|---|---|---|---|---|---|
| 29 – Blok kódu v návodu | kontrola | **neprošlo** | prošlo ⇄ | 1/3 | ř. 3 „NESMÍ dát závažnost (P0–P2) ani navrhnout náhradu: nic z bl…“ (2/3) |
| 30 – Bloková citace třetí osoby | kontrola | prošlo | prošlo | 3/3 | – |

Důvod uvádí, co selhalo a v kolika bězích. Případ projde i s jedním neúspěšným během ze tří; důvod pak ukazuje nestabilitu. Úplné výstupy a verdikty jsou v `behy.json`.

⇄ = výsledek se oproti výchozímu stavu změnil.
