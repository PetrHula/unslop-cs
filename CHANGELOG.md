# Změny

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
