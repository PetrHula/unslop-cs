# Změny

## 1.2.0 – 2026-10-27

Skill se spouští na vyžádání a `SKILL.md` je zkrácený na jádro. Pravidla se věcně nemění, kromě kódu měny CZK.

- **Description:** místo „Použij automaticky, i bez vyžádání“ a výčtu žánrů spouštění na pokyny (unslop, zní to jako AI, zkontroluj, polidšti, přepiš) a na výslovné volání z jiného skillu. Režim psaní zůstává: používá ho essay-style („uplatňuj unslop-cs potichu v režimu psaní“).
- **`SKILL.md` z 6 967 na 3 100 slov** (2 950 bez interpunkce a tabulek). V jádru zůstávají princip, režimy (sloučené se spoluprací s jinými skilly), krátká verze, postup, měření skriptem, profily registrů, závažnost (definice P0–P2 a „slabé samo o sobě“), pojistky celé, sebekontrola a formáty výstupu.
- **Postup:** krok 2 načítá `references/slova.md` a `references/vzorce.md` nástrojem Read na začátku každé kontroly a přepisu, i u čistě vypadajícího textu; krok 3 spouští `scripts/metriky.py` na text nad 100 slov s absolutní cestou k adresáři skillu. Ve výchozím běhu 1.1.0 nečetl reference ani jeden z 84 běhů.
- **Prezentace:** řada titulků, která po sobě nenese příběh, je v jádru výslovně samostatný nález P1 (dřív jen ve výčtu P1, který se přesunul do `vzorce.md`).
- **`references/vzorce.md`** přestavěný podle úrovní: podrobná pravidla úrovní 1–3, česká skladba, vyprávění, registr prezentací a odborný text, u každého vzorce příklad před a po a případ, který zůstává. Dřívější katalog příkladů je sloučený do stejných oddílů, nic není zdvojené. Nový oddíl Výčty tvarů podle závažnosti obsahuje úplné výčty P1 a P2.
- **Typografie a mikroformáty** jsou jen ve `references/slova.md` (tabulka doplněná o poznámky z dřívějšího `SKILL.md`).
- **CZK:** v běžném textu o částkách se píše „Kč“; „ceny v CZK“ je tam P2. CZK jako bankovní kód zůstává v bankovním, účetním a mezinárodním textu. Kód měny vedle „Kč“ není smíšený formát čísel (P1). Případ 13 to teď očekává jako P2 místo dřívějšího „NESMÍ označit“.
- **UDPipe:** model skill nikdy nehledá ani nestahuje; licence sjednocené s README (software MPL 2.0, modely CC BY-NC-SA 4.0).
- **`CONTRIBUTING.md`** v kořeni repozitáře převzal oddíl Údržba skillu a přidal příkaz pro srovnávací běh evalů.
- README a popis pluginu odpovídají spouštění na vyžádání.

## 1.1.1 – 2026-10-26

Úklid dokumentace a runner regresních případů. `SKILL.md` a seznamy slov se nemění.

- README: opatrnější tvrzení o opoře v datech, nový oddíl Omezení (co AI-Koditex obsahuje a co kalibrace skriptu měří) a UDPipe v oddílu Volitelné rozšíření s licencemi (software MPL 2.0, modely ÚFAL CC BY-NC-SA 4.0).
- `references/zdroje.md`: UD Czech-CAC má licenci CC BY-SA 4.0, ne CC BY-NC-SA; UD Czech-FicTree zůstává CC BY-NC-SA 4.0. Stejná oprava v hlavičce `tools/kalibrace/kalibrace_ud.py`.
- Záznam 1.1.0 odkazoval na soubor mimo repozitář; teď odkazuje na `references/zdroje.md` a `tools/koditex/README.md`.
- `tools/evaly/runner.py`: pouští případy z `evals/pripady.md` přes `claude -p` s načteným pluginem, každý případ 3×, rozhoduje většina. Výchozí stav pro porovnání po přestavbě `SKILL.md` je v `tools/evaly/vysledky/vychozi-1.1.0/`.

## 1.1.0 – 2026-10-26

Pravidla podložená výzkumem češtiny. Opora jednotlivých pravidel je v `references/zdroje.md`, postup porovnání AI-Koditexu s lidskými texty v `tools/koditex/README.md`.

- `references/slova.md` podle porovnání AI-Koditexu s lidskými texty Koditexu: nová slova v úrovních 1–3 (klíčový a fascinující do úrovně 1; aspekt, výzva, kontext, potenciál, příležitost, sdílet a další do úrovně 2), zesilovače (zcela, naprosto, opravdu, velmi, výrazně, značně) z úrovně 3 pryč. Slova úrovně 2, která v lidském věcném textu padají do víc než 5 % odstavců, jsou v úrovni 3; v odstavci nad 120 slov platí úroveň 2 až od tří slov.
- Nová pravidla s českou oporou: výhled místo výsledku, hustá síť odkazů, začátky vět „Tento / Tato / Toto“, oddíl Obsah (relevance, hustota, fakta) na začátku úrovně 3.
- Nové pojistky: postoj, oslovení a konkrétnost se při přepisu neubírají; oprava nepřidává chyby a nezhoršuje čtivost; odbočka zůstává.
- Zúžená pravidla, která šla proti českým datům: vrstvené jištění, opisy pro „je“, synonymní kolotoč, emoce ve vyprávění, kalky. „Pocit pojmenuj“ pryč z krátké verze.
- Typografie podle ÚJČ: dlouhá pomlčka „—“ jako neobvyklá, rozpočet pomlček jako heuristika, 04.05.2026 přípustné, 4.5.2026 P2.
- Skript `scripts/metriky.py` 0.2.0 (z větve `metriky`) a oddíl Měření skriptem: jeden přechod P2, dva a víc P1; úvodní fráze uprostřed odstavce P2; informativní metriky postoje a konkrétnosti s lidskou referencí.
- `references/zdroje.md`, `tools/koditex/` (analýza AI-Koditexu) a `tools/kalibrace/` (kalibrace na UD).
- Evaly: 28 případů, z toho 10 čistých. Oprava: verze 1.0 měla sedm čistých případů, ne osm.

## 1.0.0 – 2026-10-26

První verze.

- Architektura převzatá z jlwin/unslop_ai: tři úrovně, čtyři režimy, profily registrů, závažnost P0–P2, pojistky, sebekontrola.
- České vzorce sloučené z nowork-ai/anti-ai-slop-cz a bejek/humanizer-czech a doplněné o kalky, falešné přátele, člen, příklonky a aktuální členění větné.
- Typografie podle českých pravidel: pomlčka „–“ s mezerami, dlouhá „—“ jako signál, spojovník v neformálním textu povolen.
- Značka `[OVĚŘIT: …]` místo vymyšlených údajů.
- 20 regresních případů, z toho 8 čistých.
