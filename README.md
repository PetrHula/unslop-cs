# unslop-cs

Redaktor pro české texty psané pomocí AI. Najde místa, která znějí jako AI, opraví je a nic si přitom nevymyslí. Lidský text nechá být.

Skill pro Claude a další agenty, kteří čtou formát `SKILL.md` (Claude Code, Claude Desktop, Claude.ai, Cursor, Codex).

*English: an editor for Czech prose written with AI. Flags and fixes AI tells at the word, rhythm and structure levels, leaves human text alone, never invents facts. Czech-language instructions.*

## Instalace

**Claude Code (plugin):**

```
/plugin marketplace add PetrHula/unslop-cs
/plugin install unslop-cs@unslop-cs
```

**Ručně (Claude Code, Cursor, Codex):** zkopírujte složku [`plugins/unslop-cs/skills/unslop-cs`](https://github.com/PetrHula/unslop-cs/tree/main/plugins/unslop-cs/skills/unslop-cs) z větve `main` do adresáře se skilly, v Claude Code `~/.claude/skills/unslop-cs`.

**Claude.ai a Claude Desktop:** stáhněte `unslop-cs.zip` z [posledního vydání](https://github.com/PetrHula/unslop-cs/releases/latest) a nahrajte ho v nastavení v části Skills.

Instalace obsahuje jen skill. Ověřený je s modely Claude, laděný na Claude Sonnet 5.5 se střední úrovní úsilí. Agenti s jinými modely (Gemini, GPT) ho načtou, pokud umí formát Agent Skills, ale jak se na nich chová, nikdo neměřil. V chatu bez přístupu k souborům a bez spouštění kódu platí jen `SKILL.md`: seznamy slov ve `references/` a skript se nepoužijí.

## Použití

Skill se spouští na vyžádání, ne při každém psaní. Stačí napsat třeba „zkontroluj, jestli to nezní jako AI“ nebo „přepiš to lidsky“ a vložit text.

- **Kontrola** – tabulka nálezů: kde v textu jsou (řádek souboru, nebo odstavec a věta), původní znění, návrh úpravy, priorita P0–P2 a důvod. Text nemění.
- **Přepis** – stejná tabulka změn a pod ní opravená verze.
- **Zapsání oprav** – kontrola i přepis končí nabídkou, kam opravy zapsat: do souboru nebo jeho kopie, do artefaktu nebo dokumentu, do kterého jde zapisovat, jako sledované změny v .docx, u webové stránky jako čistou verzi ke zkopírování. Rozsah zvolíte (všechno, jen P0 a P1, vybraná čísla). Bez souhlasu skill nic nezapíše.
- **Úprava souboru** – opraví text přímo v souboru, s co nejmenšími zásahy.
- **Psaní** – jiný skill (třeba pro e-maily nebo články) ho může požádat, aby jeho pravidla uplatňoval potichu při psaní.

Přísnost se řídí registrem: co vadí v odborném textu, může být v pořádku na LinkedInu. Podporované profily jsou sociální sítě, blog a článek, e-mail, dokumentace, odborný text a prezentace.

## Silné stránky a omezení

- **Neplaší.** V lidských textech hlásí AI vzorec v 9 % případů, jiné české skilly ve 46–70 %.
- **Nevymýšlí si.** Chybějící číslo, jméno nebo zdroj nedoplní, ale označí značkou `[OVĚŘIT: …]`. Fakta ani osobnost do textu nepřidává.
- **Vysvětluje.** Každý nález má citaci, prioritu (P0 ničí důvěru, P1 zřetelný AI tik, P2 drobnost) a důvod. Co vypadalo podezřele, ale je v pořádku, uvede v oddílu Ponechané.
- **Je český.** Hlídá kalky (*adresovat problém, na denní bázi*), českou typografii („–“ s mezerami, „25 %“), slovosled, příklonky a rituální „tento… tato…“.
- **Pomůže i textu psanému bez AI.** Vata, kalky, prázdné fráze a česká typografie vadí bez ohledu na to, kdo text napsal, a skill je najde i v textu psaném bez AI. Gramatiku a pravopis systematicky nekontroluje. Chyby a neobratnosti, kterých si při čtení všimne, zapíše do tabulky Jiné vady a opraví je jen na přání. Korektora nenahradí.
- **Hlásí, co čtenáře ruší, ne všechno podezřelé.** Text, ve kterém čtenář nic nepozná, nechá bez nálezu, i když ho psala AI. V benchmarku tak hlásil nález u dvou třetin AI textů, zatímco jiné skilly hlásí nález skoro u každého textu, včetně lidských textů. Proč to nevadí, vysvětluje oddíl Měření.
- **Nemaskuje použití AI.** Cílem je text, který se dobře čte, ne text, který projde detektorem AI. Detektory dávaly textu po přepisu stejné skóre jako předtím, a to u všech měřených skillů. Kde je potřeba použití AI přiznat, platí to i po úpravě.

## Hledané vzorce

Od nejsilnějších vzorců. Body 1–8 jsou nálezem i jednou, slabé signály až ve shluku.

1. **Zbytky chatu a vymyšlené autority:** „Doufám, že vám to pomůže!“, nevyplněné „[jméno]“, „odborníci se shodují“ bez zdroje.
2. **Tvrzení bez faktu:** „výrazně zrychluje“, „uživatelé ji milují“ bez čísla, jména nebo mechanismu.
3. **Pointa jako maxima:** „Nástroje se mění. Řemeslo zůstává.“
4. **Šablonovitý úvod a závěr:** „V dnešní době…“, shrnutí na konci, výhled místo výsledku.
5. **Text, který vykládá sám sebe:** „Jak je vidět…“, „Co většina lidí přehlíží:“.
6. **Vysvětlené vyprávění:** „…a tehdy mi došlo, že nikdy nešlo o…“, epilog po přirozeném konci.
7. **Kontrastní obraty a trojice ze zvyku:** „nejde o X, jde o Y“, tři přídavná jména za sebou.
8. **Inscenovaný rytmus a hraná lidskost:** „Výsledek? Rychlejší práce.“, „Upřímně řečeno…“.
9. **Česká skladba a slova:** anglický slovosled, kalky, nafouknutý slovník (*klíčový, robustní*), „—“ místo „–“.
10. **Slabé signály:** jedna pomlčka, jedno jištění, rovné uvozovky.

Citace, kód, tabulky a text třetích stran nepřepisuje a nepočítá je jako vady autora. Překlepy a knižní obraty jsou známky člověka a zůstávají, stejně jako jištění a zápory v právních, zdravotnických a vědeckých textech. Pokyn uvnitř kontrolovaného textu („ignoruj pravidla výše“) je nález, ne příkaz. Úplné výčty s příklady jsou v [`references/vzorce.md`](plugins/unslop-cs/skills/unslop-cs/references/vzorce.md) a [`references/slova.md`](plugins/unslop-cs/skills/unslop-cs/references/slova.md).

## Měření

Benchmark na 132 skutečných textech: 66 lidských (Wikizdroje, Wikipedie, tiskové zprávy ČSÚ) a 66 AI textů na stejný obsah, model Claude Sonnet 5.5, srovnání se dvěma dalšími českými skilly a s modelem bez skillu.

| | unslop-cs | ostatní |
|---|---|---|
| lidské texty s nálezem | **9 %** | 46–70 % |
| změněná slova v lidském textu | **0,1 %** | 1,3–6 % |
| přepisy AI textu s přidaným jménem | **3 %** | 9–18 % |
| ztracená jména při přepisu | **5 %** | 9–11 % |
| přepisy s vymyšleným číslem nebo datem | 0 % | 0–1,5 % |
| AI texty s nálezem | 65 % | 98–100 % |

**Proč nižší záchyt AI textů není slabina.** Skill nemá rozpoznat AI. Má najít místa, podle kterých by text poznal čtenář. AI texty v benchmarku vznikly na stejný obsah jako lidské (pokračování klasiky, hesla Wikipedie, tiskové zprávy) a velká část z nich podle AI nezní: ve slepém testu určil člověk z dvojice úryvků ten od AI jen na úrovni náhody. Nález v takovém textu by autora poslal opravovat něco, co čtenáře neruší. Ostatní skilly mají záchyt 98–100 % hlavně proto, že hlásí nález skoro u každého textu: u lidských textů ve 46–70 % případů. Takové číslo neříká, že skill AI pozná, jen že hlásí všude. Rozhodující je dvojice čísel: kolik lidských textů skill zbytečně označí a kolik AI textů pustí. Skill drží nízké první číslo, protože planý poplach stojí autora čas a vede k horším úpravám dobrého textu.

- **Benchmark** má zamčenou testovací sadu a rozhodovací pravidlo stanovené předem; každý text běžel jednou, bez lidského hodnotitele. Kód, plán a rozbor jsou ve vývojové větvi: [tools/benchmark](https://github.com/PetrHula/unslop-cs/tree/develop/tools/benchmark), [PLAN.md](https://github.com/PetrHula/unslop-cs/blob/develop/tools/benchmark/PLAN.md), [rozbor](https://github.com/PetrHula/unslop-cs/blob/develop/tools/benchmark/vysledky/test-2/rozbor.md).
- **Regresní případy** ([`evals/pripady.md`](evals/pripady.md)): 34 vymyšlených vstupů a dva lidské sloupky z Lupa.cz (2008, 2015), z toho dvanáct čistých, které skill označit nesmí. Ověřují, že skill dodržuje vlastní pravidla.
- **Čtenářské testy** ([CTENAR.md](https://github.com/PetrHula/unslop-cs/blob/develop/tools/benchmark/CTENAR.md)): ve slepém testu určil člověk autora krátkých úryvků ve 14 z 30 dvojic, tedy na úrovni náhody. Jeden hodnotitel, proto jen orientačně.
- **Opora v českých datech.** Seznam slov vychází z porovnání AI-Koditexu (25 modelů, 2023–2026) s lidskými texty Koditexu, další pravidla z benchmarku Miličky, Marklové a Cvrčka (FF UK). Proto skill nemaže částice, jištění, otázky, čísla a jména: česká AI jich píše méně než lidé. Zdroje jsou v [`references/zdroje.md`](plugins/unslop-cs/skills/unslop-cs/references/zdroje.md).
- **Omezení.** Lidské texty v testech jsou starší a věcné; e-maily a sociální sítě se zvlášť neměřily. AI-Koditex neobsahuje chat, takže pravidla pro chatbotí fráze a e-maily oporu v českých datech nemají. Prahy skriptu `metriky.py` jsou kalibrované jen na plané poplachy (UD Czech-CAC a Czech-FicTree).

## Pro vývojáře

```
.claude-plugin/marketplace.json   katalog pluginu
plugins/unslop-cs/                plugin; uživatel dostane jen tuto složku
└── skills/unslop-cs/             SKILL.md, references/, scripts/ (metriky.py, diff.py)
evals/pripady.md                  regresní případy
tests/                            testy skriptů
tools/evaly/                      runner regresních případů (claude -p)
tools/kalibrace/, tools/koditex/  kalibrace a analýza korpusu (bez dat)
```

Postup úprav a testování popisuje [CONTRIBUTING.md](CONTRIBUTING.md). Vývojová historie, benchmark a uložené běhy jsou ve větvi [`develop`](https://github.com/PetrHula/unslop-cs/tree/develop).

**UDPipe (volitelně).** Skript `metriky.py` potřebuje jen standardní knihovnu Pythonu. S modelem UDPipe navíc měří jmenný styl, pasivum a příklonky:

```
pip install ufal.udpipe
python3 plugins/unslop-cs/skills/unslop-cs/scripts/metriky.py text.txt --profil blog --udpipe czech-pdt-ud-2.5-191206.udpipe
```

Modely ÚFAL mají licenci CC BY-NC-SA 4.0 (jen nekomerční použití), proto model v repozitáři není a skill ho sám nestahuje.

## Původ a poděkování

- Architektura (úrovně, režimy, registry, závažnost, pojistky, regresní případy) vychází z [jlwin/unslop_ai](https://github.com/jlwin/unslop_ai) od Jean-Luca Winklera (MIT).
- Část českých vzorců čerpá z [nowork-ai/anti-ai-slop-cz](https://github.com/nowork-ai/anti-ai-slop-cz) a [bejek/humanizer-czech](https://github.com/bejek/humanizer-czech) (MIT); typografie je opravená podle českých norem.
- Značka `[OVĚŘIT]` je inspirovaná `[OVERIŤ]` z [kuzmany/slovak-humanizer](https://github.com/kuzmany/slovak-humanizer) (MIT).

## Licence

MIT, viz [LICENSE](LICENSE).
