# Čtenářský test: ctenar-k1

- Datum: 2026-11-16 21:25 +0100; režim: kalibrace; sada: dev, vrstvy klasika, wiki, uredni
- Čtenář: claude-opus-5-5, každá dvojice ve dvou pořadích; commit `a35ea1c`
- Dvojic: 120 (kandidátů 207); úryvky 2–3 věty, 20–60 slov, medián slov lidský 44, AI 41
- Odpovědí: 240; nevyhodnoceno: 0; bez platné odpovědi: 0; cena 3.72 USD
- Vyřazené kandidátní dvojice: chatbot lidské okno 12, chatbot poměr délek 16, pokracovani lidské okno 15, pokracovani poměr délek 7

Úspěšnost = podíl dvojic, ve kterých čtenář správně určil lidský úryvek (rozporná pořadí 0,5). Interval: bootstrap 95 % po shlucích (dílo).

| skupina | dvojic | úspěšnost | interval | rozporná pořadí |
|---|---|---|---|---|
| vse | 120 | 95 % | [90 %; 98 %] | 7 |
| metoda:pokracovani | 60 | 92 % | [85 %; 98 %] | 3 |
| metoda:chatbot | 60 | 97 % | [92 %; 99 %] | 4 |
| vrstva:klasika | 55 | 94 % | [82 %; 100 %] | 3 |
| vrstva:wiki | 43 | 95 % | [91 %; 99 %] | 4 |
| vrstva:uredni | 22 | 95 % | [88 %; 100 %] | 0 |
| model:claude-haiku-5-5 | 39 | 96 % | [89 %; 100 %] | 3 |
| model:claude-opus-5-5 | 38 | 89 % | [78 %; 97 %] | 2 |
| model:claude-sonnet-5-5 | 43 | 98 % | [95 %; 100 %] | 2 |

**K1 (úspěšnost ≥ 70 % a dolní mez ≥ 60 %): splněno.**

Úspěšnost podle jistoty čtenáře (jednotlivé odpovědi): 1: 11/14; 2: 132/142; 3: 84/84
