# Změny

## 1.0.2 – 2026-11-19

Vady, které nejsou znakem AI, mají vlastní tabulku, a legenda vysvětluje písmeno P.

- **Jiné vady:** překlepy, neobratnosti, germanismy, nejednotné uvozovky nebo velké a malé V a věcné nesrovnalosti, které nejsou vzorcem AI, skill nehlásí jako nálezy, ale zapíše je do samostatné tabulky „Jiné vady (nejsou znakem AI)“: bez priority, nejvýš pět řádků, přepis je neopravuje. Dosud je buď hlásil jako AI nález, nebo zamlčel.
- **Legenda:** „P = priorita úpravy: P0 ničí důvěru, P1 zřetelný AI tik, P2 drobnost“.
- **Regresní případy 35 a 36:** první skutečné lidské texty, sloupky z Lupa.cz z let 2008 a 2015 (před generativní AI). V repozitáři je jen odkaz a otisk; runner text stáhne (`tools/evaly/zdroje_web.py`).

### Změřeno

- **Evaly** (Claude Sonnet 5.5): 30 z 32 při jednom běhu; po třech bězích prošly případy 4, 7, 21, 23 a 35. Případ 36 neprochází: skill v lidském názorovém článku hlásí „Ti, kdo informatice rozumí, se shodují“ jako vágní autoritu (P0) a „Zastavte se a promyslete…“ jako výklad pro čtenáře (P1), stejně jako ve verzi 1.0.1.
- **Benchmark na dev sadě:** lidské texty s nálezem beze změny (1 ze 40), tabulku jiných vad má 49 z 50 výstupů (průměrně 2,3 řádku), cena na text +6,5 % (0,147 USD).

## 1.0.1 – 2026-11-19

Srozumitelnější výstup: u každého nálezu je vidět, kde v textu je, co tam stojí a co skill navrhuje místo toho.

- **Tabulka nálezů** `# | kde | P | původně | návrh | proč` v kontrole i přepisu, řádky v pořadí textu. „Původně“ je úsek zkopírovaný ze zdroje, takže jde najít hledáním, „návrh“ je tentýž úsek po úpravě. Jedna věta má jeden řádek; přestavba celého odstavce má pod tabulkou blok „před:“ a „po:“.
- **Pozice:** řádek souboru jako odkaz (`clanek.md:62`), v textu z chatu odstavec a věta (`¶3.2`); vlastní číslování textu (§, body) a u prezentací číslo slajdu mají přednost.
- **Kontrola navrhuje úpravu**, text dál nemění.
- **Legenda** pod verdiktem vysvětluje závažnost P0–P2 a zápis pozic.
- **`diff.py`** slouží ke kontrole, že každá změna má řádek v tabulce a nic tiše nezmizelo; blok diffu se do výstupu dává jen na vyžádání.
- **Volání z jiného skillu** dál dostává seznam změn bez tabulky, nově s pozicí.
- Regresní případy 31–34 (formát výstupu) upravené na tabulku s pozicí.

## 1.0.0 – 2026-11-19

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
