# Změny

## 1.0.0 – nevydáno

První veřejná verze skillu `unslop-cs`: kontrola a přepis českého textu proti AI slopu.

- **Tři úrovně:** slova (slovník, fráze, kalky, typografie), věta (rytmus, skladba, česká stavba) a obsah se strukturou (věty bez nové informace, výhled místo výsledku, opakovaná pointa, mravoučný závěr).
- **Režimy:** kontrola, přepis, úprava souboru a psaní, ve kterém skill běží potichu na výzvu uživatele nebo jiného skillu. Spouští se jen na vyžádání.
- **Profily registrů:** sociální sítě, blog, esej a článek, e-mail, dokumentace, odborný text a prezentace; profil určuje přísnost každého pravidla.
- **Závažnost P0–P2** a filtr přesnosti: nález je vzorec AI, ne jakákoli vada textu; co skill ponechává, uvádí zvlášť.
- **Pojistky proti přepisování:** žádná vymyšlená čísla, jména ani zdroje, osobnost a síla významu zůstávají, chybějící fakt nahradí značka `[OVĚŘIT: …]`.
- **Skripty:** `scripts/metriky.py` počítá měřitelné vzorce (typografie, rytmus, shluky slov, přechody, trojice; s volitelným modelem UDPipe i jmenný styl, pasivum a příklonky) a `scripts/diff.py` dělá slovní diff po větách a hlídá tichou ztrátu čísel, jmen a jištění.
- **Regresní případy:** 34 případů v `evals/pripady.md`, deset z nich čistých, které skill označit nesmí. Runner `tools/evaly/runner.py` je pouští přes `claude -p`.
- **Podklady:** analýza AI-Koditexu (`tools/koditex`) a kalibrace prahů na lidských textech UD (`tools/kalibrace`).

### Změřeno

- **Regresní evaly veřejné podoby:** 29 z 30 případů, z toho čisté texty 10 z 10 (3 běhy na případ, model Claude Sonnet 5.5).
- **Benchmark na skutečných textech** (132 textů: lidské z Wikizdrojů, Wikipedie a tiskových zpráv ČSÚ a jejich AI protějšky; srovnání s jinými českými skilly a s modelem bez skillu): lidské texty s nálezem 9,1 % proti 45,5–69,7 %, změna lidských textů 0,1 % slov proti 1,3–6,0 %, přidaná jména při přepisu 3 % proti 9–18 %, AI texty s nálezem 65 % proti 98–100 %, cena 0,136 USD na text. Skill tedy málo plaší a nevymýšlí, ale nechytá všechno.
- **Známá omezení:** případ 29 (komentář v bloku kódu) je nestabilní, skill ho správně nehodnotí, ale v Ponechaných občas navrhne přepsat nebo smazat. Skript `metriky.py` se v evalech spouští zřídka (1 běh z 90), seznamy slov tedy většinou posuzuje model sám.
- **Čtenářské testy:** ve slepém testu s úryvky o 2–3 větách poznal člověk AI text ve 14 z 30 dvojic (na úrovni náhody), model v 95 % dvojic; žádný skill dojem z textu měřitelně nezměnil. Skill proto slibuje dobrý text, ne neodhalitelnost.

Podrobná historie vývoje, včetně neúspěšných pokusů, je ve [vývojové větvi](https://github.com/PetrHula/unslop-cs/blob/develop/CHANGELOG.md).
