# Benchmark skillů na reálných textech: plán

Stav: korpus, rozdělení, skóre AI-ovosti, pilot, kalibrace soudce a ostrý běh `test-1` na test sadě hotové (viz Stav u kroků; výsledek u kroku 7). Větev `benchmark-realna-data`.

## Proč

Regresní evaly (`skills/unslop-cs/evals/pripady.md`, `tools/evaly/runner.py`) mají vymyšlené vstupy i klíč OČEKÁVÁNO a obojí napsal Claude podle pravidel skillu. Měří, jestli skill dodržuje vlastní pravidla a jestli se nezhoršil, ne jestli má pravdu. Ani čisté případy nejsou lidské texty. `metriky.py` je kalibrovaný jen na plané poplachy (UD CAC a FicTree); citlivost na AI text nikdo nezměřil.

Benchmark má férově a opakovatelně porovnat dva skilly (nejdřív unslop-cs proti běhu bez skillu, později unslop-cs proti dvěma skillům, které dodá uživatel) na textech, u kterých víme, kdo je napsal. Klíčem je původ textu (člověk, nebo model), ne úsudek Clauda.

## Principy

1. **Párová data.** Lidský text a AI text na stejný obsah (metoda AI-Koditexu): rozdíl mezi nimi je rozdíl autora, ne tématu.
2. **Metriky mimo pravidla skillů.** Hlavní soudce nevychází z pravidel žádného srovnávaného skillu. `metriky.py` stojí na pravidlech unslop-cs, proto je jen doplňkovou metrikou a do rozhodnutí nevstupuje.
3. **Domácí hřiště zvlášť.** Pravidla unslop-cs vznikla z AI-Koditexu a prahy `metriky.py` z UD CAC a FicTree. Tyto vrstvy se vykazují zvlášť a do rozhodovacího pravidla nevstupují (viz Statistika).
4. **Zamčená test sada.** Pravidla se ladí jen na dev sadě; test sadu při ladění nikdo nečte (ani sezení Clauda).
5. **Rozhodovací pravidlo předem.** Je níže v tomto souboru a po prvním běhu na test sadě se nemění. Změnu je nutné zapsat do historie plánu s datem a důvodem a výsledky dřívějších běhů na test sadě se pak nepoužijí.
6. **Data mimo repozitář.** Texty, výstupy modelů nad nimi a soukromé texty jsou v `~/unslop-cs-data/benchmark/`; v repozitáři je kód, konfigurace, hashe a souhrnné výsledky.

## Krok 1: lidský korpus

Texty o 200–600 slovech. Delší díla se dělí na úseky na hranici odstavce; z jednoho díla nejvýš tolik úseků, aby žádný zdroj neměl ve vrstvě přes 20 %.

| Vrstva | Zdroj | Licence (ověřit před stažením) | Cíl |
|---|---|---|---|
| `klasika` | fejetony a sloupky: Čapek († 1938), Poláček († 1945), Hašek († 1923), Neruda († 1891); Wikizdroje, e-knihovna MKP, Kramerius NDK | autorská práva vypršela (70 let po smrti); ověřit podmínky užití edice a digitalizace u každého zdroje | 60 |
| `cac` | UD Czech-CAC, jen split `train` (kalibrace `metriky.py` použila `test`) | CC BY-SA 4.0 | 30 |
| `fictree` | UD Czech-FicTree, split `train` | CC BY-NC-SA 4.0 (nekomerční užití) | 20 |
| `wiki` | česká Wikipedie, poslední revize před 2022-01-01, jen souvislá próza | CC BY-SA 3.0/4.0 podle data revize | 30 |
| `uredni` | tiskové zprávy a sdělení úřadů před 2022 | § 3 autorského zákona kryje úřední díla, ne každou tiskovou zprávu; přednostně zdroje s výslovnými podmínkami užití | 20 |
| `soukromy` (volitelně) | texty uživatele před 2022 | jen lokálně, nikdy v repozitáři ani v souhrnu po jednotlivých textech | podle uživatele |

Stav dat UD (staženo 2026-11-11, připnuto na commit, záznam v `~/unslop-cs-data/benchmark/stazeni.json`): CAC train má 130 dokumentů (66 odborných, 50 novinových, 14 administrativních; 70. a 80. léta), všechny delší než 600 slov a bez značek odstavců, takže se dělí na hranici věty. FicTree train má jen 8 děl (108 tis. slov) se značkami odstavců; celé dílo jde do jedné sady, rozdělení dev/test je proto u FicTree hrubé (přibližně 3 : 5 děl).

Klasika: stažena jen z Wikizdrojů (`zdroje/wikizdroje.py`, výběr v `zdroje/wikizdroje_vyber.json`, revize připnuté v `revize.json` u dat), 334 stránek: Čapek 194, Hašek 100, Arne Novák († 1939) 21, Poláček 7, Neruda 2, ostatní fejetonisté z kategorie Fejetony 10; šablony `PD old 70` (333) a `PD anon 70` (1). Podmínky e-knihovny MKP ani NDK se ověřit nepodařilo (e-knihovna.cz nedostupná, podmínky NDK jen v JavaScriptu, FAQ NK ČR varuje před strojovým vytěžováním), proto se nepoužívají. Poláček a Neruda jsou zastoupeni slabě; je to omezení vrstvy.

Wikipedie: `zdroje/wikipedie.py`, 30 článků (21 dobrých, 9 nejlepších; seed 20261111), poslední revize před 2022-01-01 (revize z let 2021), jen odstavce `<p>` mimo tabulky, 379–8 981 slov prózy na článek. Při řezání na úseky odstranit `[zdroj?]`, zbytky šablon (`{{…}}`) a odstavce s kódem nebo vzorci (např. L-systém).

Úřední: `zdroje/csu.py`, 20 tiskových zpráv ČSÚ z let 2010–2014 (seed 20261111; roční archivy jsou staticky dostupné jen pro 2003–2014), 253–598 slov, celkem 7 785 slov. Uložena jen próza bez kontaktů, odkazů a příloh. Licence CC BY 4.0 podle podmínek ČSÚ, které mluví o „statistických informacích“; zda kryjí i text zpráv, výslovně neříkají. ČNB zakazuje obsahové úpravy textů, vláda.cz a ministerstva podmínky užití nemají, proto se nepoužívají.

FicTree: podle README jsou texty kvůli dohodě s nositeli práv rozdělené na kousky do 100 slov rozházené mezi train, dev a test. V train jdou kousky (`newpar`) vzestupně; běhy po sobě jdoucích id jsou souvislý text (146 běhů ≥ 200 slov). Úseky se skládají jen z takových běhů; hranice odstavců jsou hranice kousků, ne původní odstavce. 20 % děl jsou překlady; které, README neříká.

**Korpus** (`korpus.py`, seed 20261111, 2026-11-11): 160 textů, 62 628 slov – klasika 60 (Čapek 20, Hašek 15, Novák 11, Poláček 6, Neruda 4, ostatní 4; 29 děl, nejvýš 10 z jednoho), CAC 30 (novinové 12, odborné 12, administrativní 6), FicTree 20 (7 děl, nejvýš 4), wiki 30, úřední 20. Mediány délky 350–410 slov. Hashe v `manifest_hashe.json`, texty a úplný manifest jen u dat.

Klasika je stará, ostatní vrstvy brání tomu, aby klasifikátor AI-ovosti měřil hlavně období a archaismy.

**Manifest** `~/unslop-cs-data/benchmark/manifest.json`, jeden záznam na text: `id`, `vrstva`, `zdroj`, `url`, `licence`, `licence_overeni` (URL stránky s podmínkami), `datum_stazeni`, `sha256` (textu po normalizaci), `zanr`, `obdobi` (rok vydání nebo revize), `autor`, `slov`, `soukromy`, `poznamka`. Do repozitáře jde jen `tools/benchmark/manifest_hashe.json` (id, vrstva, sha256, slov), bez textů a bez soukromé vrstvy.

**Normalizace:** UTF-8, NFC, sjednocené bílé znaky, odstavce oddělené prázdným řádkem, bez poznámek editora a čísel stran. Typografii (uvozovky, pomlčky) normalizace nemění, je součástí stylu.

**Stahování:** před každým zdrojem se uživatel ptá (zdroj, licence, velikost). Žádné účty, žádné odesílání dat. Surová data jdou do `surove/<zdroj>/` jako nedůvěryhodná; Python, který je čte, běží s `-I`.

## Krok 2: AI protějšky

Ke každému lidskému textu dva protějšky od každého generujícího modelu:

- **(a) pokračování** (metoda AI-Koditexu): prvních ~100 slov lidského textu, zaříznuté na konci věty, a pokyn pokračovat ve stejném stylu do délky zbytku (±20 %). Srovnává se se skutečným pokračováním autora. Prefix se z hodnocení vynechává u obou stran.
- **(b) chatbotí zadání:** „Napiš <žánr> na téma X, asi N slov.“ Téma X v ≤ 10 slovech a žánr se zapíšou do manifestu ručně nebo levným modelem; zápis tématu nesmí citovat text.

**Modely:** Claude Haiku, Sonnet a Opus přes `claude -p` bez nástrojů a bez pluginů. Další výrobce (GPT, Gemini, Llama) jen když uživatel dodá přístup; vícevýrobcovou AI vrstvu jinak dává AI-Koditex. `claude -p` neumožňuje nastavit teplotu ani seed; zaznamená se verze modelu z události `init`.

**Filtr kontaminace:** klasiku mohly modely vidět při trénování. Pokračování se vyřadí, když sdílí s autorovým pokračováním (nebo s celým dílem, je-li stažené) jakýkoli shodný úsek 12 slov nebo víc než 2 % slovních 8-gramů. Stejný filtr platí pro chatbotí zadání. Počty vyřazených se vykazují po vrstvách a modelech.

**AI-Koditex** (`~/unslop-cs-data/korpusy/rozbaleno/AI_Koditex_plain_texts`): vrstva `aikoditex` bez lidského páru (lidské originály Koditexu nemáme). Vzorek 100 textů napříč modely, teplota 0 i 100, první věta vynechaná jako v `tools/koditex/parse.py`.

**Stav (2026-11-11):** `generuj.py` vytvořil 960 protějšků (160 textů × 2 metody × Haiku, Sonnet a Opus 5.5) a 160 témat za 17,66 USD (Opus 12,62, Sonnet 4,69, Haiku 0,35), žádné volání neselhalo. Délka proti zadání (medián): Opus a Sonnet 0,87–0,96, Haiku 0,77–0,78. Filtr kontaminace nevyřadil nic (nejdelší shoda 11 slov, nejvyšší podíl 8-gramů 1,5 %). Vyřazeno 17 chatbotích výstupů: odmítnutí nebo přiznání neznalosti (4; Haiku odmítl dvě humoresky kvůli etnickému stereotypu v tématu) a zástupné značky typu „[datum]“ (15, hlavně tiskové zprávy). Markdown (tučné, oddělovače) má 80 chatbotích a 15 pokračování; zůstávají, jsou označené v `kontaminace.json` a detekce se vykáže i bez nich. AI-Koditex: 100 textů z 24 instruovaných modelů (teplota 0: 34, 100: 66), každé id Koditexu jednou.

Výstup: `~/unslop-cs-data/benchmark/ai/<metoda>/<model>/<id>.txt` a `ai_manifest.json` (zdrojové id, metoda, model, verze, datum, zadání, sha256, výsledek filtru).

## Krok 3: rozdělení dev/test

- Jednotkou rozdělení je **zdrojový lidský text** i se všemi svými AI protějšky (shluk), aby se tentýž obsah neobjevil v obou sadách. U klasiky a FicTree jde do jedné sady celé dílo.
- Poměr dev : test = 40 : 60, stratifikace podle vrstvy, losování se seedem z konfigurace.
- Test sada leží v `~/unslop-cs-data/benchmark/test/`. V repozitáři je jen `tools/benchmark/zamek.json`: seed, datum, sha256 seřazeného seznamu id a sha256 každého testového souboru.
- `benchmark.py` pustí test sadu jen s přepínačem `--test` a štítkem `test-*`; každé odemčení zapíše do `vysledky/<stitek>/` a ověří hashe proti zámku. Výsledky z test sady se vykazují jen souhrnně, ne po textech, aby z nich nešlo ladit pravidla.
- **Stav (2026-11-11):** `rozdel.py` rozdělil lidské texty dev 67 : test 93 (klasika 24 : 36, CAC 12 : 18, FicTree 11 : 9 – celá díla, proto hrubě, wiki 12 : 18, úřední 8 : 12) a AI-Koditex 40 : 60. Test sada má 701 souborů; zámek je v `zamek.json`.
- Pravidlo pro údržbu (doplnit do `CONTRIBUTING.md`): při úpravách unslop-cs se čtou jen dev výsledky; test běh je jednou na vydání.

## Krok 4: spouštěč nezávislý na skillu

Benchmark znovu použije z `tools/evaly/runner.py` volání `claude -p` se stream-json, čtení tokenů (`tokeny_z_usage`), detekci chyb infrastruktury (`infra_chyba`) a opakování (`_s_opakovanim`). `runner.py` se nemění; benchmark má vlastní obecnou funkci volání s parametry pro adresář pluginu, název skillu a povolené nástroje.

**Jedno zadání pro všechny:** „Zkontroluj text a vypiš, co v něm zní jako psané AI. Pak dej opravenou verzi; když není co opravit, nech text beze změny.“ Adaptér ho převede do přirozené podoby daného skillu (vyvolání skillu, jeho režim, formát výstupu). Jedno volání na text dává nálezy i finální text.

**Adaptéry** (`tools/benchmark/adaptery/`): `unslop_cs.py`, `bez_skillu.py` (stejné zadání bez pluginu), šablona pro další skilly. Adaptér deklaruje plugin, název skillu, povolené nástroje, zadání a převod závažnosti na společnou škálu (`vysoka`, `stredni`, `nizka`, `neuvedena`). Pro unslop-cs: P0 → vysoká, P1 → střední, P2 → nízká.

**Normalizace** na společné schéma (`normalizovany.json`): `skill`, `text_id`, `beh`, `nalezy` [{`zavaznost`, `misto` (citace), `popis`}], `finalni_text`, `surovy_vystup`, `tokeny`, `kroku`, `cas_s`, `cena_usd`, `model`. Přednost má deterministický parser adaptéru; když skill nemá strojově čitelný formát, nálezy vytáhne levný model se schématem JSON, který jen přepisuje, nehodnotí. Způsob normalizace se zaznamená u každého výstupu.

**Konfigurace** (`tools/benchmark/konfigurace.json`, jeden soubor): model skillu, model soudce, generující modely, seed, počet běhů, vybrané vrstvy, cesty k datům, seznam skillů (cesta k pluginu, adaptér). Otisk skillu = sha256 obsahu jeho adresáře (jako `_otisk_skillu` v runneru).

## Krok 5: metriky

### Hlavní: nezávislé skóre AI-ovosti

Logistická regrese (L2, numpy) trénovaná jen na dev sadě: lidské texty proti AI textům. Rysy se počítají po zpracování UDPipe (`~/unslop-cs-data/model/czech-pdt-ud-2.5-191206.udpipe`):

- **F0 (hlavní, slepá k pravidlům):** četnosti 100 nejčastějších lemmat uzavřených slovních druhů (seznam zmrazený z lidské reference KonText před tréninkem), podíly slovních druhů a dvojic slovních druhů, délka vět (průměr, rozptyl), délka slov, STTR, interpunkce na 1000 slov.
- **F1 (citlivostní analýza):** F0 a rysy dimenzí MDA z `tools/koditex/features.py` (`kx_*`). Pravidla unslop-cs z těchto dimenzí vycházejí, proto F1 nerozhoduje.
- Vyloučené vždy: rysy odvozené ze `slova.md` a `vzorce.md` (fráze, `KALKY`, `OUTLOOK`, `OPIS_JE`, `START_CONNECTIVES`) a všechny výstupy `metriky.py`.

**Stav (2026-11-11):** `rysy.py trenuj` na dev sadě (67 lidských, 435 AI textů; 100 funkčních slov z KonTextu, 40 dvojic UPOS z dev): AUC křížové validace po shlucích (5 skupin) celkem 0,92; klasika 0,97, FicTree 0,94, wiki 0,92, CAC 0,92, úřední 0,91, AI-Koditex 0,85; bez textů s markdownem 0,93. Po původu: chatbot 0,92–0,98, pokračování 0,87–0,94 (stejný autor i doba, takže skóre neměří jen období). Všechny vrstvy splňují práh 0,75. Model je v `DATA/modely/ai_skore.json`, předpovědi z křížové validace v `ai_skore_cv.json`.

Skóre se použije jen ve vrstvě, kde má při křížové validaci na dev sadě AUC ≥ 0,75; jinak se pro vrstvu nevykazuje. Model se po prvním test běhu nepřetrénovává.

### Kontrola (detekce)

- AUC hustoty nálezů `vysoka` + `stredni` na 1000 slov: lidské proti AI textům, po vrstvách.
- Plané poplachy: podíl lidských textů s aspoň jedním nálezem `vysoka` nebo `stredni`, po vrstvách.
- Shoda mezi 3 běhy: Fleissova kappa pro „aspoň jeden nález vysoká/střední“ a směrodatná odchylka hustoty na text.

### Přepis AI textu

- **Posun skóre AI-ovosti:** skóre před minus po (kladné = text se posunul k lidskému).
- **Vzdálenost od autora** (jen pokračování): eukleidovská vzdálenost standardizovaných rysů F0 od autorova skutečného pokračování, před a po.
- **Zachování čísel, dat a jmen** (skript): podíl čísel, dat a vlastních jmen (UDPipe `PROPN`) z originálu, které v přepisu zůstaly; selhání = ztráta kteréhokoli čísla nebo data.
- **Zachování významu** (soudce): přidal přepis tvrzení, které v originálu není, nebo vynechal tvrzení, které tam je? Strukturovaná odpověď se seznamem; porušení = aspoň jedno přidané nebo vynechané věcné tvrzení.
- **Slepé párové srovnání A/B:** soudce vidí originál a dva přepisy bez názvů skillů, v obou pořadích. Výhra platí jen při shodě obou pořadí, jinak remíza.
- Doplňkově: počty P0/P1 z `metriky.py` před a po (do rozhodnutí nevstupují).

### Přepis lidského textu (neškodnost)

- Podíl změněného textu: 1 − podíl shodných slov podle `difflib.SequenceMatcher`.
- Posun skóre AI-ovosti u lidského textu (nemá se hýbat).

### Náklady

Tokeny (vstup celkem, výstup), počet kroků, čas a cena v USD na text, z události `result`.

### Soudce

Soudce je jiný model než ten, který spouští skill (výchozí: skill `claude-sonnet-5-5`, soudce `claude-opus-5-5`), bez nástrojů, se schématem JSON. Zbývá riziko, že model Claude jako soudce preferuje výstupy Clauda; proto krok 6.

## Krok 6: kalibrace soudce

Z dev sady 20 dvojic přepisů (stejný originál, dva různé přepisy), pořadí náhodné, bez názvů. Uživatel v lokálním souboru u každé dvojice zvolí A, B nebo „nerozhodně“ a u 10 přepisů označí, jestli přidaly nebo vynechaly tvrzení. Shoda = podíl dvojic, kde má preferenci uživatel i soudce a shodují se. **Při shodě pod 70 % se párové srovnání A/B do rozhodnutí nepoužije** (vykazuje se jen informativně). Stejné pravidlo platí pro soudce zachování významu.

**Stav (2026-11-13):** běh `kalibrace-1` (20 AI textů z dev, 4 skilly, 1 běh, 19,35 USD); 20 dvojic unslop-cs proti ostatním třem skillům, bez dvojic se shodnými přepisy; význam jen u změněných přepisů (14 hodnocení). Shoda A/B 9/17 = 53 %, význam 8/14 = 57 %. **Neprošlo ani jedno:** `kalibrace_soudce_ok` a `kalibrace_vyznam_ok` jsou `false`. Bod 2 rozhodovacího pravidla proto stojí jen na ztrátě čísel a dat, bod 3 jen na posunu skóre AI-ovosti; A/B a porušení významu se vykazují informativně. Anotoval autor unslop-cs (naslepo); jeho vkus může být blízký pravidlům unslop-cs. Souhrn v `vysledky/kalibrace-1/kalibrace_soudce.json`.

## Krok 7: statistika a rozhodovací pravidlo

Stanoveno předem; platí pro test sadu, mimo vrstvy `aikoditex`, `cac` a `fictree` (domácí hřiště unslop-cs, vykazují se zvlášť).

- Jednotka: text. Hodnota textu = průměr přes běhy (plán 3; běh `test-1` má 1, viz Historie plánu 2026-11-13). Rozdíl A − B se počítá na stejném textu.
- Interval spolehlivosti: bootstrap 95 % (percentilový, 10 000 opakování, seed z konfigurace), převzorkují se shluky podle zdrojového lidského textu.
- Výsledky vždy i po vrstvách; rozhodnutí stojí na sloučených vrstvách z věty výše.

**A je lepší než B**, když platí všechno:

1. **Plané poplachy se nezhorší:** horní mez intervalu rozdílu (A − B) v podílu lidských textů s nálezem vysoká/střední je ≤ +3 procentní body.
2. **Zachování významu se nezhorší:** horní mez intervalu rozdílu v podílu přepisů AI textů s porušením významu je ≤ +5 p. b. a A neztratí víc čísel či dat než B (horní mez ≤ +2 p. b.).
3. **A přinese zlepšení:** interval rozdílu posunu skóre AI-ovosti (A − B) leží celý nad nulou, **nebo** interval podílu výher A minus výher B v párovém srovnání leží celý nad nulou (jen když soudce prošel kalibrací).

Když body 1 a 2 platí a bod 3 nevyjde ani pro jednoho, mají skilly shodnou kvalitu a rozhodují náklady (medián ceny na text; levnější o víc než 20 % vyhrává). Když bod 1 nebo 2 neplatí, A lepší není bez ohledu na bod 3.

Neškodnost na lidských textech (podíl změněného textu) a AUC detekce se vykazují vedle rozhodnutí a slouží k výkladu, ne k rozhodnutí.

**Stav (2026-11-13):** běh `test-1` na zamčené test sadě (216 textů: 93 lidských, 123 AI; 4 skilly, 1 běh, bez soudce, 126,98 USD, nevyhodnocené běhy 0). Rozhodnutí podle pravidla: unslop-cs proti anti-ai-slop-cz, humanizer-czech i bez-skillu vždy **shodná kvalita, rozhodují náklady, levnější je druhý skill** (bod 1 a ztráta čísel platí, bod 3 nevyšel). Plané poplachy na rozhodovacích vrstvách: unslop-cs 1,5 %, anti-ai-slop-cz 7,6 %, humanizer-czech 22,7 %, bez-skillu 16,7 %. Pravidlo je ale bere jen jako podmínku „nezhoršit“, takže nižší podíl planých poplachů unslop-cs k výhře nestačí. Posun skóre AI-ovosti AI textů je u všech skillů blízko nuly (−0,006 až +0,008); proti bez-skillu má unslop-cs interval celý pod nulou (−0,013 [−0,031; −0,001]). Cena na text: unslop-cs 0,29, anti-ai-slop-cz 0,10, humanizer-czech 0,14, bez-skillu 0,04 USD. Podrobnosti po vrstvách jsou v `vysledky/test-1/vysledky.md`.

## Krok 8: opakovatelnost

Jeden příkaz:

```
python -E -P tools/benchmark/benchmark.py --konfigurace tools/benchmark/konfigurace.json --stitek <stitek> [--sada dev|test --test] [--pilot] [--jen-ai N] [--behy N] [--max-usd X]
    [--lidskych N] [--aikoditex N] [--vyber-seed STITEK] [--prevzit STITEK …] [--povolit-zamitnuti]
```

Kolo ladění jednoho skillu (od 2026-11-13): pevný výběr `--lidskych N --aikoditex N --vyber-seed <první štítek kola>` a `--prevzit <starší štítek>`. Převezmou se běhy skillů, které by dopadly stejně: stejný otisk skillu, celé zadání včetně nástrojů, model skillu a zadání extraktoru (u starších štítků bez těchto polí: stejný otisk a záznam skillu v konfiguraci, čistý commit, od něj beze změny `adaptery.py` a příkaz `claude`). Převzaté běhy se nepočítají do útraty běhu, cena na text zůstává. Zamítnutý nástroj ve dvou prvních bězích skillu běh zastaví a zamítnutí na konci skončí kódem 2; `--povolit-zamitnuti` to vypne. Zpráva má navíc citlivost (podíl AI textů s nálezem vysoká/střední), podíl běhů se zamítnutím a s chybou nástroje a u každého srovnání oddíl „K výkladu“ (poměr ceny, plané poplachy, intervaly citlivosti, změny lidských textů a ztráty jmen); do rozhodnutí nic z toho nevstupuje.

Pilot: `--stitek pilot-1 --pilot` (5 lidských textů, po jednom z každé vrstvy, a 5 AI: 2 pokračování, 2 chatbotí, 1 AI-Koditex, z různých zdrojů a modelů; 1 běh). Podklad pro kalibraci soudce: `--stitek kalibrace-1 --jen-ai 20 --behy 1`, pak `kalibrace_soudce.py pripravit` a `vyhodnotit`. Plný výběr řídí `behy.vyber` v konfiguraci (všechny lidské texty sady, `ai_na_zdroj` AI protějšků na zdrojový text, `aikoditex` textů AI-Koditexu); velikost se doladí podle ceny z pilotu.

Ověřeno offline (2026-11-11): celý řetězec s náhradními odpověďmi místo `claude -p` (výběr, běhy, normalizace, soudce, rysy, metriky, bootstrap, rozhodnutí, zpráva, příprava a vyhodnocení kalibrace). Skutečné volání skillu a soudce zatím neběželo.

Pozn.: na dev sadě se skóre AI-ovosti počítá modelem natrénovaným na téže sadě (originály jsou „viděné“); rozdíl mezi skilly je i tak férový, protože oba přepisují stejné texty. Na test sadě je skóre mimo trénink.

Výstup `tools/benchmark/vysledky/<stitek>/`: `konfigurace.json` (kopie), `data.json` (sha256 manifestu, rozdělení a zámku), `modely.json` (verze modelů z událostí `init`), otisky skillů, commit gitu, `souhrn.json` a `vysledky.md`. Výstupy po textech (`behy.jsonl`) zůstávají v `~/unslop-cs-data/benchmark/behy/<stitek>/`, protože obsahují texty korpusu.

## Struktura kódu

```
tools/benchmark/
  PLAN.md               tento soubor
  konfigurace.json      modely, seed, běhy, skilly
  korpus.py             normalizace, manifest, úseky 200–600 slov
  zdroje/               stahování a extrakce po zdrojích (spouští se až po souhlasu)
  generuj.py            AI protějšky (a), (b)
  kontaminace.py        n-gramový filtr
  rozdel.py             dev/test a zamek.json
  aikoditex.py          vrstva AI-Koditex bez páru
  cli.py                volání claude -p bez nástrojů (generování, soudce, normalizace)
  adaptery.py           adaptéry: unslop_cs, bez_skillu, obecny (skill dodaný uživatelem)
  spoustec.py           volání skillu přes claude -p, finální text a normalizace nálezů
  zachovani.py          čísla a data, vlastní jména, podíl změněného textu
  rysy.py               rysy F0 (UDPipe), skóre AI-ovosti, funkcni_slova.json
  soudce.py             zachování významu, párové A/B
  statistika.py         párové rozdíly, bootstrap, rozhodovací pravidlo
  kalibrace_soudce.py   20 dvojic k ruční anotaci
  benchmark.py          jeden příkaz
  vysledky/<stitek>/
```

Závislosti: Python 3.8+, `ufal.udpipe`, `numpy` (pro `rysy.py`; ostatní skripty jen standardní knihovna). Bez scikit-learn, aby výsledek nezávisel na jeho verzi. Balíčky nainstalované s `pip --user` přepínač `-I` nevidí; skripty s nimi se spouštějí `python -E -P` (bez proměnných prostředí a bez adresáře skriptu v cestě).

## Pořadí a rozpočet

| Fáze | Co | Placené volání | Odhad |
|---|---|---|---|
| 1 | lidský korpus a manifest | ne | – |
| 2 | AI protějšky (~160 textů × 2 metody × 3 modely) | ano | 10–20 USD, ptát se předem |
| 3 | rozdělení dev/test a zámek | ne | – |
| – | skriptové metriky bez LLM (rysy, skóre AI-ovosti, čísla a jména, změněný text) | ne | – |
| pilot | 10 dev textů (5 AI, 5 lidských), unslop-cs proti „bez skillu“, 1 běh | ano | < 10 USD |
| 6 | kalibrace soudce | ano (malé) | < 3 USD |
| plný běh | test sada, dva skilly + bez skillu, 3 běhy | ano | 100–150 USD, až po souhlasu a po dodání dalších skillů |

Pilot ověřuje, že celý řetězec běží, a odhaduje cenu na text; jeho čísla nic nerozhodují. Po každém kroku krátký report a otázka před dalším stahováním nebo placeným během.

## Otevřené otázky pro uživatele

1. Přístup k jiným výrobcům než Anthropic pro generování AI protějšků (bez něj Claude a AI-Koditex).
2. Soukromá vrstva: ano, nebo ne; kolik textů.
3. FicTree má licenci CC BY-NC-SA: vyhovuje zamýšlenému užití?
4. Model skillu a soudce v plném běhu (výchozí Sonnet 5.5 a Opus 5.5).

## Rizika a omezení

- Skóre AI-ovosti měří odlišitelnost od lidských textů, ne kvalitu. Skill ho může „zlepšit“ i tím, že text zhorší; proto zachování významu a neškodnost jako podmínky.
- Klasika vs. současnost: klasifikátor může rozpoznávat období. Brání tomu současné vrstvy, rysy F0 bez slovníku a vykazování po vrstvách.
- AI protějšky jsou hlavně od Clauda a soudce je Claude. Kalibrace soudce a AI-Koditex (jiní výrobci) to zmírňují, neodstraňují.
- Pokračování a chatbotí zadání nepokrývají e-maily, LinkedIn a formát odpovědí chatbota.
- Zámek test sady je procedurální, technicky se dá obejít. Platí pravidlo z kroku 3.

## Historie plánu

- 2026-11-11: první verze.
- 2026-11-11: soudce významu podléhá kalibraci stejně jako A/B (`kalibrace_vyznam_ok`); když neprojde, porušení významu do rozhodnutí nevstupuje a bod 2 stojí jen na ztrátě čísel. Upřesnění před prvním během na test sadě.
- 2026-11-13: ostrý běh `test-1` má 1 běh místo 3 a běží bez soudce (`--bez-soudce`). Důvod: rozpočet ~150 USD; 4 skilly stojí podle pilotu a kalibrace 0,60 USD na text a běh, celá test sada (216 textů) tedy ~129 USD na běh. Soudce po neúspěšné kalibraci do rozhodnutí nevstupuje, A/B a porušení významu proto v `test-1` nejsou ani informativně. Shoda mezi běhy (kappa) se nevykazuje. Rozhodovací pravidlo jinak beze změny. Zapsáno před prvním během na test sadě.
- 2026-11-13: po běhu `test-1` nástroje benchmarku, ne pravidlo: převzetí shodných běhů (`--prevzit`), pevný menší výběr (`--lidskych`, `--aikoditex`, `--vyber-seed`), hlídání zamítnutých nástrojů, citlivost a oddíl „K výkladu“ ve zprávě, `behy.jobs` 4 → 8. Důvod: v `test-1` se skript unslop-cs ani jednou nespustil (Windows cp1252, opraveno v `a7acf69`), ostatní skilly se při každém kole platily znovu a běh trval ~2 h (rozbor v `vysledky/test-1/rozbor.md`). Rozhodovací pravidlo v kroku 7 zůstává beze změny.
