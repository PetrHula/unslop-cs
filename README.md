# unslop-cs

Kontrola a přepis českého textu proti AI slopu. Skill pro Claude a další agenty, kteří čtou formát `SKILL.md` (Claude Code, Claude Desktop, Cursor, Codex).

*English: checks and rewrites Czech prose for AI slop on request – word, rhythm and structure level, register profiles, regression cases. Czech-language instructions.*

## Tři úrovně

Většina „humanizérů“ zakáže pár slov (*ponořit se, klíčový, game changer*) a tím končí. To nestačí ze dvou důvodů. Seznamy slov stárnou s každou generací modelů. Trvalý otisk ale nese stavba vět a celého textu. Skill proto pracuje na třech úrovních, hlavně na dvou hlubších:

| Úroveň | Co chytá | Příklady |
|---|---|---|
| 1 – Slova | slovník, fráze, kalky, typografie | „hraje klíčovou roli“, „adresovat problém“, „na denní bázi“, „—“ v českém textu |
| 2 – Věta | rytmus a skladba | řetězy krátkých vět, trojice, „nejde o X, jde o Y“, přívěsky s „což“, nadbytečné „svůj“, anglický slovosled, jmenný styl |
| 3 – Obsah a struktura | co text říká a jak je postavený | věty bez nové informace, výhled místo výsledku, pointa opakovaná v každém oddílu, falešné prozření, mravoučná pointa, „Závěrem lze konstatovat“ |

Jedno pravidlo platí všude: vágní tvrzení nahraď ověřitelným faktem. Když fakt chybí, skill vloží značku `[OVĚŘIT: …]` a nic si nevymyslí.

## Opora v českých datech

Od verze 1.1 se část pravidel opírá o data z češtiny místo anglických seznamů. Seznam slov vychází z porovnání AI-Koditexu (25 modelů, 2023–2026) s lidskými texty Koditexu a nová pravidla z posunů, které u české AI naměřil benchmark Miličky, Marklové a Cvrčka z FF UK: víc soudržnosti, víc obecnosti a výhledu, méně oslovení a postoje. Zbytek pravidel pochází z praxe a z existujících skillů (viz Původ a poděkování). Z dat plyne i to, co skill nedělá: nemaže částice, jištění, otázky, čísla a jména, protože jich česká AI píše méně než lidé. Zdroje s hodnocením platnosti pro češtinu jsou v `references/zdroje.md`.

## Omezení

- **AI-Koditex není chat.** Obsahuje pokračování psaných textů z Koditexu, ne odpovědi chatbota, e-maily ani příspěvky na LinkedIn. Pravidla pro tyto žánry (chatbotí fráze, formát odpovědí, obraty v e-mailech) oporu v českých datech nemají.
- **Kalibrace měří jen falešné poplachy.** Prahy skriptu `metriky.py` jsou nastavené tak, aby skript zbytečně neoznačoval lidské texty z UD Czech-CAC (věcné texty ze 70. a 80. let) a UD Czech-FicTree (beletrie). Jak spolehlivě skript pozná AI text, kalibrace neměří.

## Rozdíly oproti existujícím českým skillům

- **Správná česká typografie.** Česká pomlčka je „–“ s mezerami. Některé skilly radí místo ní spojovník „-“, který je v sazbě typografická chyba. Tenhle skill hlídá anglickou „—“ i rozpočet pomlček, ale spojovník v chatu nebo e-mailu nechá být, protože tak lidé běžně píšou.
- **Pojistky proti přepisování.** Klasické selhání humanizérů je výměna jednoho otisku za jiný: vymyšlená čísla a studie, sekání na útržky, hraná upřímnost, vnucená hovorovost. Skill to bere jako neúspěšný přepis. Smí škrtat a zpřesňovat; fakta ani osobnost nepřidává.
- **Registry.** Útržky jsou na LinkedInu běžné, v eseji působí jako tik. Jištění v reklamě vadí, odborný text ho potřebuje. Tabulka profilů (sociální sítě, blog a esej, e-mail, dokumentace, odborný text, prezentace) určuje přísnost každého pravidla.
- **Vzorce typické pro češtinu.** Kalky a falešní přátelé (*realizovat si, eventuálně, aktuálně, adresovat problém*), nadbytečná zájmena, rituální „tento… tato…“, příklonky mimo své místo, aktuální členění větné, tykání a vykání, „25 %“ a „25%“.
- **Regresní testy a měření.** 28 případů v `evals/pripady.md`, z toho deset čistých, které skill označit nesmí, protože přehnané označování je taky chyba. Runner `tools/evaly/runner.py` je pouští přes `claude -p` a ukládá tabulku výsledků. Skript `scripts/metriky.py` spočítá měřitelné věci (typografie, rytmus, shluky slov, přechody, trojice); jmenný styl, pasivum a příklonky měří jen s volitelným modelem UDPipe. Prahy skriptu omezují falešné poplachy na lidských textech z Universal Dependencies.

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

- Architektura (tři úrovně, režimy, profily registrů, závažnost, pojistky, sebekontrola, regresní případy) vychází z [jlwin/unslop_ai](https://github.com/jlwin/unslop_ai) od Jean-Luca Winklera (MIT), skillu pro němčinu a angličtinu.
- Část českých vzorců a frází čerpá z [nowork-ai/anti-ai-slop-cz](https://github.com/nowork-ai/anti-ai-slop-cz) (MIT) a [bejek/humanizer-czech](https://github.com/bejek/humanizer-czech) (MIT). Typografická pravidla jsou opravená podle českých norem a příklady přepsané tak, aby nevymýšlely čísla.
- Značka `[OVĚŘIT]` je inspirovaná `[OVERIŤ]` z [kuzmany/slovak-humanizer](https://github.com/kuzmany/slovak-humanizer) (MIT).

Účelem skillu je dobré psaní, obcházení detektorů AI nepodporuje. Kde je třeba použití AI přiznat, skill na tom nic nemění.

## Licence

MIT. Viz [LICENSE](LICENSE).
