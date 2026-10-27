# Změny

## 1.4.0 – nevydáno

Výstup přepisu ukazuje změny jako diff a funguje v každém agentovi, ne jen v Claude. Pravidla skillu se věcně nemění.

- **Formáty výstupu:** přepis má pořadí verdikt s počty P0/P1/P2, diff, tabulka změn `# | P | vzorec | proč`, ponechané nálezy, řádek metrik před → po, druhý průchod, seznam `[OVĚŘIT: …]`, čistá verze. Tabulka nahrazuje dřívější oddíly „nálezy“ a „co se změnilo“, které se překrývaly a neukázaly tichou ztrátu. Kontrola dává nálezům jen čísla.
- **Úrovně podle schopností agenta:** 0 jen text (změny po celých větách, „před:“ a „po:“), 1 shell (`scripts/diff.py`, bez Pythonu git `--word-diff`), 2 úprava souborů (diff ukáže rozhraní agenta), 3 na přání (revizní stránka, sledované změny). Základ nepotřebuje žádný nástroj. Na nástroje se agent neptá, zjistí je sám a neúspěch tiše znamená nižší úroveň. Ptát se smí jen na cíl, jednou otázkou; při volání z jiného skillu a v režimu psaní nikdy.
- **Nový `references/vystup.md`:** zjištění úrovně, příkazy, ukázka přepisu. Ověřeno na českých textech: regex `[[:alnum:]]+([.,][[:digit:]]+)*|[^[:space:]]` drží pohromadě čísla s čárkou a nechává uvozovky, pomlčky a nezlomitelné mezery v kontextu; v locale `C` ale rozbíjí UTF-8, proto vyžaduje `LC_ALL=C.UTF-8`.
- **Nový `scripts/diff.py`:** slovní diff po větách bez gitu (difflib, nezávisí na locale), vynechává kód a citace a hlídá tichou ztrátu: čísla, vlastní jména (shoda kmene včetně střídání koncovky), částice a jištění ze seznamů `metriky.py`, markery síly tvrzení jako info. Výstup md a json, `--metriky` přidá řádek metrik před → po, `--prisne` vrátí kód 1 při ztrátě. Importuje `metriky.py`, seznamy ani tokenizaci nekopíruje.
- **Testy:** `scripts/test_diff.py`, 21 testů (interpunkce, uvozovky, nezlomitelná mezera, desetinná čísla, ztráty, skloňovaná jména, kód a citace, rozhraní).
- **`SKILL.md`:** upraveny kroky 3 a 7, sebekontrola 12 a odkazy. Počet slov 3 141 → 3 440 (`wc -w`; po sloučení s 1.3.0 3 505).
- **Evaly:** nové případy 31 (agent bez shellu), 32 (agent s Pythonem a gitem), 33 (volání z jiného skillu bez dotazu), 34 (nejasný cíl, jedna otázka). Zatím jen popsané: `runner.py` a `test_metriky.py` je přeskakují (nadpis „Formát výstupu“), pouštějí se ručně.
- **Runner, chyby infrastruktury:** limit session nebo použití, přetížení API, timeout, prázdný výstup a rozbitá odpověď hodnotitele se opakují (`--opakovani`, výchozí 3, pauza `--pauza` roste s pokusem). Hláška limitu přicházela s podtypem `success` a runner ji dřív hodnotil jako výstup skillu (12 prázdných běhů v `k5-1.3.0-final`). Běh, který neprojde ani po opakování, je „nevyhodnocený“: do většiny se nepočítá a zpráva ho uvádí zvlášť. Detekce bere jen krátký výstup, který chybou začíná a nemá řádek SOUHRN ani blok VERZE.
- **Runner, zamítnutý shell:** v bězích k5 se 4 až 10 běhů z 90 pokusilo uložit vstup skriptu přes `mkdir … && cd … && cat > v.txt <<EOF`, režim `dontAsk` to zamítl i s pravidly `Bash(cat *)`, `Bash(cd *)` a model skript nespustil (čísla „skript spuštěn“ v k5 jsou tedy mírně nízká). Runner teď text případu sám uloží do `vstup.txt` v pracovním adresáři a zadání to říká; model ho jen předá skriptu, což pravidlo `Bash(python3 *)` pustí. Plné `Bash` runner záměrně nepovoluje. Příkazy Bash a zamítnutí nástrojů se ukládají do `behy.json` (pole `prikazy`, `zamitnuto`) a zpráva uvádí počet běhů se zamítnutím. Nemění skill, mění podmínky měření: výsledky nejsou srovnatelné s k4 a k5.
- **Runner, nálezy mimo OČEKÁVÁNO:** hodnotitel vrací i nálezy P0/P1, které nepokrývá žádný řádek OČEKÁVÁNO (jakéhokoli typu: u přepisových případů řádky o značkách `[OVĚŘIT]` nebo zachování vět také pokrývají místa, o kterých mluví); běh neprojde, když jich je víc než jeden (`--max-mimo`, `-1` vypne). Nové kritérium úspěchu: výsledky nejsou srovnatelné s `k4-1.3.0` ani `k5-*`, zpráva na rozdíl kritérií upozorní a výchozí běh se zakládá znovu.

## 1.3.0 – 2026-10-27

Skript `metriky.py` (0.3.0) neměří kód a citace a skill slop v nich nehodnotí jako vadu autora. Skill skript spouští vždy, když má shell.

- **Vyloučeno z měření:** ohrazené bloky ```` ``` ```` a `~~~`, odsazený kód (podle CommonMark: před blokem prázdný řádek, nejde o pokračování položky seznamu; když je odsazená víc než polovina odstavců, jde o odsazení prvního řádku a měří se), HTML `<pre>` a `<code>` a blokové citace `>`. Inline kód, URL a e-maily jako dosud. Vyloučený text se nepočítá do slov, rozpočtu pomlček na 300 slov, vět ani rytmu; běh vět podobné délky a řetěz krátkých vět se přes vyloučený blok nepřenáší. Upozornění GitHubu (`> [!NOTE]` a další) jsou text autora a měří se.
- **Jen info:** místní nálezy v tabulkách Markdownu a uvnitř „…“ (dřív jen seznamy slov a vágní autorita). Buňky tabulek jsou mimo počet slov a rytmus, pomlčky a vykřičníky v tabulkách a v „…“ mimo rozpočet. Krátká citace v „…“ se dál měří: přímá řeč v AI textu je legitimní cíl, jen nedává P0–P2.
- **`--vse`:** blokové citace, tabulky a „…“ měří naplno jako v 1.2.0. Kód, URL a e-maily zůstávají vyloučené.
- **Výstup:** nové pole `souhrn.vylouceno` (`slov`, `useku` podle druhu) a v textovém přehledu řádek „vyloučeno z měření: N slov (kód 2, citace 1)“, jen když se něco vyloučilo. Pole `vse` v JSON.
- **Opravy:** vestavěné nálezy (zástupný text, vložený pokyn, vágní autorita) se hledají v maskovaném textu, uniklé citační tokeny dál i v kódu; dvojtečka před citací („řekla: „…““) není dvojtečkové odhalení; nález rozpočtu pomlček ukazuje na pomlčku, ne na mezeru před ní.
- **`SKILL.md`:** citace, bloky kódu, tabulky a text třetích stran skill nepřepisuje a nepočítá jako vady autora; slop v nich zmíní jednou větou mimo nálezy, bez závažnosti a bez návrhu náhrady (dřív „označ, nikdy nepřepisuj“). Oddíl Měření skriptem popisuje vyloučení a `--vse`.
- **Testy:** 20 nových testů v `scripts/test_metriky.py` (každý vyloučený typ s chráněným protějškem, tabulky, „…“, `--vse`, počet slov, rytmus přes blok, případy 29 a 30). Komentáře odkazují na `references/zdroje.md` a `tools/koditex/README.md` místo souborů mimo repozitář.
- **Evaly:** nové případy 29 (blok kódu v návodu) a 30 (bloková citace třetí osoby), oba nad 100 slov. Běh `tools/evaly/vysledky/k4-1.3.0/`: prošlo 30/30 (výchozí 1.2.0 28/28); případy 8, 17 a 25 teď 3/3 (dřív 2/3), případ 29 2/3 (jednou navrhl náhradu komentáře v kódu). Skript `metriky.py` nespustil ani jeden běh, ani u případů 29 a 30: model texty kolem 110 slov hodnotí jako krátké a krok 3 vynechá.
- **Kalibrace** (UD Czech-CAC a FicTree test, bez modelu i se zlatou anotací): CAC beze změny; ve FicTree ubyly nálezy v přímé řeči (dvojtečkové odhalení P1 bez modelu z 3,0 na 1,5 % úseků, vykřičníky P2 z 15 na 4, trojice P2 se zlatou anotací ze 7 na 4). Nový falešný poplach nepřibyl. S modelem UDPipe (`czech-pdt-ud-2.5-191206`, stejná data, skript 0.2.0 proti 0.3.0): CAC shodné; FicTree dvojtečkové odhalení P1 z 3,0 na 1,5 % úseků, vykřičníky P2 z 15 na 4, trojice P2 ze 4 na 1, jinak beze změny nebo o 1 méně. Testy s modelem: 115 prošlo (2 přeskočené jsou testy třídy bez modelu).
- **Krok 3 postupu:** skript se spouští vždy, když je shell, kromě textů o jedné až třech větách; délku model neodhaduje. Výjimka platí jen pro skript, reference z kroku 2 se načítají vždy (bez té věty přestaly krátké texty reference číst: běhy bez jediného Read 12–18 z 90 místo 4).
- **Kód a citace:** u slopu v nich skill nedává žádné doporučení, ani smazání či úpravu (případ 29 předtím navrhoval komentář v kódu smazat).
- **Kontrola, `[OVĚŘIT]`:** formát výstupu kontroly žádá `[OVĚŘIT: co chybí]` přímo u každého nepodloženého tvrzení (výsledek, spokojenost, přínos bez čísla, jména nebo zdroje). Případ 17 předtím selhával na chybějící značce (1.2.0 2/3, k5 před úpravou 3/3, 2/3, 2/3, 1/3).
- **Evaly krok 5** (`tools/evaly/vysledky/k5-*`): konečný stav (commit `78820fe`) prošel 30/30 (čisté 10/10, ostatní 20/20), 3 běhy na případ, Sonnet 5.5 pro skill i hodnotitele, složeno ze tří běhů `k5-dobeh`, `k5-pripad17` a `k5-zbytek` (22,46 USD). Reference načetlo 88 z 90 běhů (k4 85), běhů bez jediného Read 0 (k4 4). Skript spustilo 35 z 90 běhů, u případů 29 a 30 6 ze 6 (k4 0 z 6). Stabilita: 8, 17, 25 a 29 po 3/3; jediný nestabilní případ 3 (2/3). Dřívější běhy kroku 5 před opravou čtení referencí a před úpravou `[OVĚŘIT]` (`k5-1.3.0-beh1` až `beh3`, `k5-cileny-reference`, `k5-1.3.0-final` s 12 běhy na limitu session) jsou v adresáři jako historie, vydání na nich nestojí.

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
- **Evaly** (`tools/evaly/vysledky/vychozi-1.2.0/`, výchozí stav pro další krok): prošlo 28/28, výchozí 1.1.0 27/28. Reference načetlo 82 z 84 běhů, v 1.1.0 žádný. Skript se nespustil, žádný případ nemá přes 100 slov. Běh je dražší (asi 20 USD místo 13), protože model reference skutečně čte.

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
