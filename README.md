# unslop-cs

Redaktor pro české texty psané s AI. Najde místa, která znějí jako ChatGPT, opraví je a nic si přitom nevymyslí. Lidský text nechá být.

Skill pro Claude a další agenty, kteří čtou formát `SKILL.md` (Claude Code, Claude Desktop, Cursor, Codex).

*English: an editor for Czech prose written with AI. Flags and fixes AI tells on word, rhythm and structure level, leaves human text alone, never invents facts. Measured on real texts. Czech-language instructions.*

## V čem je silný

Čísla pocházejí z testu na 132 skutečných textech (66 lidských z Wikizdrojů, Wikipedie a tiskových zpráv ČSÚ a 66 AI protějšků na stejný obsah), model Claude Sonnet 5.5. Srovnání je se dvěma dalšími českými skilly a s modelem bez skillu, který dostal stejné zadání.

| | unslop-cs | ostatní (rozpětí) |
|---|---|---|
| lidské texty, ve kterých skill hlásí AI vzorec | **9 %** | 46–70 % |
| podíl slov, které skill v lidském textu změní | **0,1 %** | 1,3–6 % |
| přepisy AI textu s jménem, které v originálu nebylo | **3 %** | 9–18 % |
| ztracená jména při přepisu AI textu | **5 %** | 9–11 % |
| přepisy s vymyšleným číslem nebo datem | 0 % | 0–1,5 % |

- **Neplaší.** Když text napsal člověk, skill to většinou pozná a řekne, že je čistý. Ostatní skilly a model bez skillu najdou „AI vzorec“ skoro v každém druhém lidském textu.
- **Nevymýšlí.** Chybějící číslo, jméno nebo zdroj nedoplní, ale označí značkou `[OVĚŘIT: …]` v seznamu pod textem. Žádné smyšlené studie, procenta ani historky.
- **Vysvětluje.** Každý nález má citaci místa, závažnost (P0–P2) a důvod. Co vypadalo podezřele, ale je v pořádku, skill uvede zvlášť v oddílu Ponechané, takže víte, na co se díval.
- **Je český.** Kalky (*adresovat problém, na denní bázi*), česká typografie („–“ s mezerami, „25 %“), příklonky, tykání a vykání, rituální „tento… tato…“. Profily registrů: co vadí v eseji, může být v pořádku na LinkedInu.
- **Je změřený.** 34 regresních případů, z toho deset čistých textů, které skill označit nesmí, a benchmark na skutečných textech. Postup i výsledky jsou v repozitáři, včetně těch nepříznivých.

## Na co dobrý není

- **Neschová AI text před detektory ani před čtenářem.** U žádného ze skillů, které jsme měřili, se po přepisu měřitelně nezměnilo skóre statistického detektoru (vlastní model natrénovaný na českých textech) ani dojem čtenáře. Ve slepém testu čtenář u krátkých textů nepoznal AI ani bez úprav (14 z 30 dvojic, na úrovni náhody) a jeho dojem z textu se po přepisu nezměnil u žádného skillu. Účelem skillu je dobré psaní; kde je třeba použití AI přiznat, skill na tom nic nemění.
- **Nechytá všechno.** Nález hlásí u 65 % AI textů, ostatní skilly u 98–100 %. Je to cena za to, že neplaší u lidských textů: skill opraví, co je zřetelný tik, a hraniční místa nechá být. Kdo chce co nejvíc nálezů a nevadí mu, že je dostane i na vlastní text, najde jinde víc.
- **Nedodá osobnost ani fakta.** Text zkrátí a zpřesní, nepřidá vtip, zážitek ani čísla. Obecný text po něm zůstane obecný, jen bez frází; co chybí, uvidíte v seznamu `[OVĚŘIT]`.
- **Není nejlevnější.** Jedna kontrola s přepisem stojí na modelu Sonnet kolem 0,14 USD na text o 200–600 slovech, model bez skillu 0,04 USD.

## Kdy ho použít

- Máte text napsaný s AI a chcete ho učesat bez rizika, že se do něj dostane něco, co jste neřekli.
- Kontrolujete cizí text a potřebujete vědět, co v něm zní uměle, bez planých poplachů na lidských pasážích.
- Jiný skill (pro e-maily, příspěvky nebo články) potřebuje závěrečnou kontrolu nebo pravidla při psaní: unslop-cs umí běžet potichu v režimu psaní.

## Jak je to změřené

- **Benchmark na skutečných textech** (`tools/benchmark`, plán v `PLAN.md`, rozbor v `vysledky/test-2/rozbor.md`): lidské texty a AI protějšky na stejný obsah, zamčená test sada, rozhodovací pravidlo stanovené předem. Texty v repozitáři nejsou, jen kód a souhrny. Jeden běh na text, bez lidského hodnotitele.
- **Regresní případy** (`skills/unslop-cs/evals/pripady.md`, runner `tools/evaly/runner.py`): vymyšlené vstupy s klíčem, co skill najít musí a co nesmí. Měří, jestli skill dodržuje vlastní pravidla.
- **Čtenářské testy** (`tools/benchmark/CTENAR.md`): slepé určování autora krátkých úryvků a hodnocení dojmu z AI textů před přepisem a po něm. Jeden hodnotitel, proto jen orientačně.
- **Lidské texty v testech jsou starší a věcné** (literatura, Wikipedie, statistické zprávy). Na e-mailech a příspěvcích na sociálních sítích se plané poplachy zvlášť neměřily.

## Tři úrovně

Většina „humanizérů“ zakáže pár slov (*ponořit se, klíčový, game changer*) a tím končí. To nestačí ze dvou důvodů: seznamy slov stárnou s každou generací modelů a trvalý otisk nese stavba vět a celého textu. Skill proto pracuje na třech úrovních, hlavně na dvou hlubších:

| Úroveň | Co chytá | Příklady |
|---|---|---|
| 1 – Slova | slovník, fráze, kalky, typografie | „hraje klíčovou roli“, „adresovat problém“, „na denní bázi“, „—“ v českém textu |
| 2 – Věta | rytmus a skladba | řetězy krátkých vět, trojice, „nejde o X, jde o Y“, přívěsky s „což“, nadbytečné „svůj“, anglický slovosled, jmenný styl |
| 3 – Obsah a struktura | co text říká a jak je postavený | věty bez nové informace, výhled místo výsledku, pointa opakovaná v každém oddílu, falešné prozření, mravoučná pointa, „Závěrem lze konstatovat“ |

Jedno pravidlo platí všude: vágní tvrzení nahraď ověřitelným faktem. Když fakt chybí, skill vloží značku `[OVĚŘIT: …]` a nic si nevymyslí.

## Co skill hledá, od nejsilnějšího

Vzorce v bodech 1–8 jsou nálezem i jednou. Slabé signály z bodu 10 až ve shluku. Tři a víc různých vzorců v jednom textu znamenají šablonu jako celek a skill doporučí text přestavět.

1. **Zbytky chatu a vymyšlené autority:** „Doufám, že vám to pomůže!“, „Skvělá otázka!“, nevyplněné „[jméno]“, uniklé `utm_source=chatgpt.com`, „odborníci se shodují“ bez zdroje.
2. **Tvrzení bez faktu:** „výrazně zrychluje“, „uživatelé ji milují“ bez čísla, jména, data nebo mechanismu.
3. **Pointa jako maxima:** „Nástroje se mění. Řemeslo zůstává.“, „není to nástroj, ale zrcadlo“. Skill ji smaže, nevylepšuje.
4. **Šablonovitý úvod a závěr:** „V dnešní době…“, shrnutí na konci, výhled místo výsledku, pointa zopakovaná v každém oddílu.
5. **Text, který vykládá sám sebe:** „Jak je vidět…“, „Co většina lidí přehlíží:“, námitka, kterou nikdo nevznesl, odstavce podle jedné šablony.
6. **Vysvětlené vyprávění:** vypravěč pojmenuje podtext („…a tehdy mi došlo, že nikdy nešlo o…“), epilog po přirozeném konci, emoce hraná tělem („sevřené hrdlo“).
7. **Kontrastní obraty a trojice ze zvyku:** „nejde o X, jde o Y“, „nejen X, ale i Y“, tři přídavná jména za sebou.
8. **Inscenovaný rytmus a hraná lidskost:** „Výsledek? Rychlejší práce.“, řetěz krátkých vět pro efekt, přívěsky s „což“, „Upřímně řečeno…“.
9. **Česká skladba a slova:** anglický slovosled, rituální „Tento… Tato…“, příklonky mimo své místo, kalky (*adresovat problém, na denní bázi*), nafouknutý slovník (*klíčový, robustní, revoluční*), „—“ místo „–“. Slova ze seznamů počítá skript s prahy podle registru.
10. **Slabé signály:** jedna pomlčka, jedno jištění, jedno „Tento“, jeden šablonovitý přechod, rovné uvozovky.

Úplné výčty s příklady před a po jsou v `references/vzorce.md` a `references/slova.md`.

## Kdy skill nezasahuje

- **Neurčuje autora.** Posuzuje vzorce, ne to, kdo text napsal. Lidé píšou fráze a šablony taky a dobrý model se jim umí vyhnout. Kdo soudí podle pocitu, hádá: v našem slepém testu autor skillu určil autora krátkých úryvků ve 14 z 30 případů. Když skill najde vzorce v textu z doby před ChatGPT (konec roku 2022), dokládá to jen, že je lidé psali dřív než AI.
- **Nepřepisuje cizí text.** Citace, bloky kódu, tabulky a text třetích stran nechá být; slop v nich zmíní jednou větou bez závažnosti.
- **Nehladí lidský text.** Překlepy, dobové a knižní obraty, odbočky a drsnější tón jsou známky člověka a zůstanou. Čistý text ohlásí jako čistý a nic na něm nemění.
- **Nesahá na nosný jazyk.** V právních, zdravotnických, vědeckých a bezpečnostních textech jsou jištění, zápory a jmenný styl obsah, ne vata.
- **Neplní pokyny z textu.** Věta „ignoruj pravidla výše“ v kontrolovaném textu je nález, ne příkaz.

## Opora v českých datech

Od verze 1.1 se část pravidel opírá o data z češtiny místo anglických seznamů. Seznam slov vychází z porovnání AI-Koditexu (25 modelů, 2023–2026) s lidskými texty Koditexu a nová pravidla z posunů, které u české AI naměřil benchmark Miličky, Marklové a Cvrčka z FF UK: víc soudržnosti, víc obecnosti a výhledu, méně oslovení a postoje. Zbytek pravidel pochází z praxe a z existujících skillů (viz Původ a poděkování). Z dat plyne i to, co skill nedělá: nemaže částice, jištění, otázky, čísla a jména, protože jich česká AI píše méně než lidé. Zdroje s hodnocením platnosti pro češtinu jsou v `references/zdroje.md`.

## Omezení

- **AI-Koditex není chat.** Obsahuje pokračování psaných textů z Koditexu, ne odpovědi chatbota, e-maily ani příspěvky na LinkedIn. Pravidla pro tyto žánry (chatbotí fráze, formát odpovědí, obraty v e-mailech) oporu v českých datech nemají.
- **Kalibrace měří jen falešné poplachy.** Prahy skriptu `metriky.py` jsou nastavené tak, aby skript zbytečně neoznačoval lidské texty z UD Czech-CAC (věcné texty ze 70. a 80. let) a UD Czech-FicTree (beletrie). Jak spolehlivě skript pozná AI text, kalibrace neměří.

## Podrobnosti

- **Správná česká typografie.** Česká pomlčka je „–“ s mezerami. Některé skilly radí místo ní spojovník „-“, který je v sazbě typografická chyba. Tenhle skill hlídá anglickou „—“ i rozpočet pomlček, ale spojovník v chatu nebo e-mailu nechá být, protože tak lidé běžně píšou.
- **Pojistky proti přepisování.** Klasické selhání humanizérů je výměna jednoho otisku za jiný: vymyšlená čísla a studie, sekání na útržky, hraná upřímnost, vnucená hovorovost. Skill to bere jako neúspěšný přepis. Smí škrtat a zpřesňovat; fakta ani osobnost nepřidává.
- **Registry.** Útržky jsou na LinkedInu běžné, v eseji působí jako tik. Jištění v reklamě vadí, odborný text ho potřebuje. Tabulka profilů (sociální sítě, blog a esej, e-mail, dokumentace, odborný text, prezentace) určuje přísnost každého pravidla.
- **Vlastní hlas.** Když přiložíte ukázku svého psaní, mají její zvyky (pomlčky, délka vět, začátky) přednost před obecnými limity.
- **Skript.** `scripts/metriky.py` spočítá měřitelné věci (typografie, rytmus, shluky slov, přechody, trojice); jmenný styl, pasivum a příklonky měří jen s volitelným modelem UDPipe. Prahy omezují falešné poplachy na lidských textech z Universal Dependencies.

## Režimy

Skill se spouští na vyžádání („unslop“, „zní to jako AI“, „zkontroluj“, „polidšti to“, „přepiš“), ne automaticky při každém psaní.

- **Kontrola** – „zkontroluj, co tu zní jako AI“: nálezy podle závažnosti P0–P2, nic se nemění.
- **Přepis** – audit, opravená verze a seznam změn.
- **Úprava souboru** – minimální zásahy přímo v souboru.
- **Psaní** – skill běží potichu, když ho o to výslovně požádá uživatel nebo jiný skill (například skill pro eseje: „uplatňuj unslop-cs potichu v režimu psaní“).

## Instalace

**Claude Code jako plugin:**

```
/plugin marketplace add PetrHula/unslop-cs
/plugin install unslop-cs@unslop-cs
```

**Ručně (Claude Code, Cursor, Codex):** zkopíruj složku `skills/unslop-cs` do adresáře se skilly, např. `~/.claude/skills/unslop-cs`.

**Claude.ai a Claude Desktop:** zabal složku `skills/unslop-cs` do ZIPu a nahraj ji v nastavení Claude v části se skilly.

**Doporučený model.** Skill je psaný pro každého agenta, který čte `SKILL.md`, ale ověřený je jen s modely Claude. Laděný a měřený je na modelu třídy Sonnet (Claude Sonnet 5.5) se střední úrovní úsilí (effort `medium`). Silnější model nebo vyšší effort výsledek zdraží; že by ho zlepšily, zatím změřené není. Modely jiných výrobců (v Cursoru, Codexu a dalších) benchmark ani regresní testy neměří.

## Struktura

```
skills/unslop-cs/
├── SKILL.md                 jádro: režimy, postup, silné vzorce, filtr přesnosti, registry, závažnost, pojistky
├── references/
│   ├── slova.md             slova ve třech úrovních, kalky, fráze, typografie (čte je skript)
│   ├── vzorce.md            příklady před a po a případy, které zůstávají (u sporných případů)
│   ├── vystup.md            úrovně výstupu, diff a ukázka přepisu
│   ├── psani.md             krátká verze pravidel pro režim psaní
│   └── zdroje.md            výzkum a norma, o které se pravidla opírají
├── scripts/
│   ├── metriky.py           měřitelné kontroly (Python 3, volitelně UDPipe)
│   ├── test_metriky.py      testy skriptu
│   ├── diff.py              slovní diff po větách a kontrola tiché ztráty
│   └── test_diff.py         testy diff.py
└── evals/
    └── pripady.md           regresní případy
tools/
├── koditex/                 analýza AI-Koditexu (bez dat)
├── kalibrace/               kalibrace skriptu na lidských textech UD (bez dat)
├── benchmark/               srovnání skillů na skutečných textech a čtenářské testy (bez dat)
└── evaly/
    ├── runner.py            spouští regresní případy přes claude -p
    └── vysledky/            uložené běhy (výchozí stav a další)
```

Korpusová data v repozitáři nejsou. Jak skill upravovat a testovat, popisuje [CONTRIBUTING.md](CONTRIBUTING.md).

## Volitelné rozšíření: UDPipe

Skript `metriky.py` běží bez dalších závislostí, jen se standardní knihovnou Pythonu. S modelem UDPipe navíc měří jmenný styl, pasivum a příklonky a slova ze seznamů páruje přes lemmata místo kmenů. Model se zapíná jen výslovně, přepínačem `--udpipe` nebo proměnnou `UNSLOP_UDPIPE`:

```
pip install ufal.udpipe
python3 skills/unslop-cs/scripts/metriky.py text.txt --profil blog --udpipe czech-pdt-ud-2.5-191206.udpipe
```

**Licence.** Software UDPipe má licenci MPL 2.0. Modely ÚFAL, včetně `czech-pdt-ud-2.5-191206.udpipe` z LINDAT, mají licenci CC BY-NC-SA 4.0, tedy jen pro nekomerční použití. Proto model v repozitáři není a skill ho sám nestahuje; kdo ho stáhne a použije, ručí za dodržení licence.

## Původ a poděkování

- Architektura (tři úrovně, režimy, profily registrů, závažnost, pojistky, sebekontrola, regresní případy) vychází z [jlwin/unslop_ai](https://github.com/jlwin/unslop_ai) od Jean-Luca Winklera (MIT), skillu pro němčinu a angličtinu, který je i v adresáři pluginů Anthropicu.
- Část českých vzorců a frází čerpá z [nowork-ai/anti-ai-slop-cz](https://github.com/nowork-ai/anti-ai-slop-cz) (MIT) a [bejek/humanizer-czech](https://github.com/bejek/humanizer-czech) (MIT). Typografická pravidla jsou opravená podle českých norem a příklady přepsané tak, aby nevymýšlely čísla.
- Značka `[OVĚŘIT]` je inspirovaná `[OVERIŤ]` z [kuzmany/slovak-humanizer](https://github.com/kuzmany/slovak-humanizer) (MIT).

## Licence

MIT. Viz [LICENSE](LICENSE).
