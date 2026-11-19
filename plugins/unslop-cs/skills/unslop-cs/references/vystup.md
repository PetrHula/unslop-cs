# Tabulka nálezů a kontrola přepisu

Podrobnosti k oddílu Formáty výstupu v `SKILL.md`. Tvar výstupu je pro uživatele vždy stejný: verdikt, tabulka nálezů s pozicí, původním úsekem a návrhem, pak čistá verze. Nástroje (Python, git, úprava souborů) mění jen to, jak přepis ověříš a kam ho zapíšeš.

## Pozice

Pozice musí jít najít bez hledání.

- **Soubor:** číslo řádku jako odkaz `clanek.md:62`, v rozhraní, které odkazy umí, je klikací. Při kontrole jde o řádek originálu. Po úpravě souboru uveď řádek v upraveném souboru, protože tam uživatel změnu otevře. Úsek, který zabírá víc řádků, má rozpětí `clanek.md:62–64`.
- **Text v chatu:** `¶odstavec.věta`. Odstavce počítej od 1 podle prázdných řádků; nadpis, položka seznamu a řádek citace jsou samostatný odstavec. Věty počítej v rámci odstavce. Výklad patří do řádku legendy pod verdiktem: „¶3.2 = 3. odstavec, 2. věta“. Změna přes celý odstavec má jen `¶3`, přes dva odstavce `¶3–4`.
- **Vlastní číslování textu** má přednost: paragrafy a odstavce zákona či smlouvy („§ 4 odst. 2“), číslované body („bod 7“), čísla řádků v básni nebo scénáři. U textu nad zhruba 1000 slov s nadpisy přidej k `¶` název oddílu („Měření ¶2.1“), aby čtenář nemusel počítat od začátku.
- **Prezentace:** „slajd 5, titulek“, „slajd 5, odrážka 3“, „slajd 5, poznámky“.

## Tabulka

```markdown
| # | kde | P | původně | návrh | proč |
|---|---|---|---|---|---|
| 1 | ¶1.1 | P1 | Pojďme se ponořit do světa datové analytiky. | (smazat) | šablonovitý úvod: věta nic neříká, „ponořit se do“ je kalk |
| 2 | ¶1.2 | P1 | …umožňují týmům adresovat problémy na denní bázi. | …pomáhají týmům řešit problémy každý den. | kalky: „adresovat problém“ a „na denní bázi“ |
```

- Řádky jdou v pořadí textu. Uživatel tabulku čte souběžně s textem; závažnost je ve sloupci P a v počtech ve verdiktu.
- **Původně** kopíruj ze zdroje znak po znaku, včetně překlepů a typografie. Vezmi změněný úsek a tolik slov okolí, aby byl v textu jednoznačný. Delší úsek zkrať „…“ na začátku nebo na konci, nikdy uprostřed změny.
- **Návrh** je tentýž úsek po úpravě a začíná i končí na stejném místě jako „původně“, aby šly porovnat očima. Smazání je „(smazat)“. Chybějící fakt je `[OVĚŘIT: co chybí]` na místě, kam patří.
- **Proč:** název vzorce, dvojtečka a čím vadí čtenáři. Interní zkratky (D6, úroveň 1) sem nepatří.
- Víc úprav v jedné větě je jeden řádek, jinak se pořadí tabulky rozpadne; v „proč“ je vyjmenuj. Jeden vzorec na několika místech má řádek pro každé místo; v „proč“ můžeš napsat „jako [2]“.
- V buňkách nepiš `~~`, `**` ani `[-…-]`. Svislou čáru z textu zapiš jako `\|`, jinak rozbije tabulku.
- V kontrole je sloupec „návrh“ nabídka: text se nemění. Když místo nejde opravit bez faktu, který nemáš, napiš do návrhu jen značku `[OVĚŘIT: …]`.

**Velké změny.** Sloučení vět, přesun nebo přestavba odstavce se do buňky nevejde. V tabulce má řádek s pozicí, závažností a „viz pod tabulkou“ ve sloupcích „původně“ a „návrh“. Pod tabulkou dostane blok:

```text
[3] ¶2 · P1 · stejně stavěné odstavce · tři věty začínají „Tento…“ a končí přívěskem s „což“
před: (celé původní věty ze zdroje, beze změny)
po: (nové znění)
```

Smazaná věta mimo tabulku má „po: (smazáno)“, nová věta „před: (nová)“. Nová věta smí vzniknout jen z obsahu zdroje (pojistky).

## Jiné vady

Vady, které nejsou vzorcem AI (filtr přesnosti v `SKILL.md`), jdou do vlastní tabulky pod tabulkou nálezů. Uživatel tak hned vidí, že nejde o AI nálezy:

```markdown
Jiné vady (nejsou znakem AI):

| kde | původně | návrh | co |
|---|---|---|---|
| ¶2.2 | …se pak vrátil zpátky zpět do kanceláře. | …se pak vrátil do kanceláře. | zdvojený výraz: „zpátky“ a „zpět“ říkají totéž |
| ¶4.1 | Děti si celé odpoledne hráli na zahradě. | Děti si celé odpoledne hrály na zahradě. | shoda podmětu s přísudkem |
```

- Bez čísla a bez P; do počtů ve verdiktu, do řádku `SOUHRN` ani do Ponechaných nepatří.
- Pravidla pro „kde“, „původně“ a „návrh“ jsou stejná jako v tabulce nálezů. „Co“ pojmenuje vadu dvěma až šesti slovy.
- Nanejvýš pět řádků, nejdůležitější vady. Samostatně je nehledáš; zapiš, co ti padlo do oka při čtení.
- Při přepisu je čistá verze neopravuje: lidský text zůstává drsný a opravu si autor vybere sám.

## Zjištění nástrojů

Na nástroje se uživatele neptej. Zjisti je sám, bez komentáře:

```sh
python3 --version   # když python3 neexistuje (typicky Windows), použij python nebo py -3
git --version
[ "$(LC_ALL=C.UTF-8 locale charmap 2>/dev/null)" = UTF-8 ] && echo utf8
```

Neúspěch kteréhokoli kroku tiše znamená, že se bez nástroje obejdeš. Uživateli to neoznamuj, kromě jedné věty o chybějícím řádku metrik.

## Kontrola přepisu skriptem

Tabulka je pro uživatele, diff je pro tebe: ověří, že přepis nezměnil nic, co v tabulce není, a že nic tiše nezmizelo. Oba texty ulož do souborů v pracovním adresáři.

**Python (výchozí).** `scripts/diff.py` rozdělí oba texty na věty, vynechá kód a citace, vypíše slovní diff změněných vět a hlídá tichou ztrátu (čísla, jména, částice a jištění, markery síly tvrzení). Na locale nezávisí:

```sh
python3 <adresář skillu>/scripts/diff.py pred.txt po.txt --metriky --profil blog
```

- Každá změněná věta z diffu musí mít řádek v tabulce. Změnu bez řádku vrať, nebo ji do tabulky doplň s důvodem.
- Co skript hlásí jako tichou ztrátu, vrať do nové verze, nebo to zapiš do tabulky jako vědomý škrt s důvodem. Hlášení jmen je bez modelu přibližné, ověř ho v diffu.
- Do odpovědi přenes beze změny oddíl Tichá ztráta (jen když něco hlásí) a řádek metrik. Blok diffu do odpovědi nedávej, ledaže o něj uživatel požádá; tabulka říká totéž čitelněji.
- `--format json` dá stejná data strojově, `--prisne` vrátí kód 1 při ztrátě. Přepínač `--metriky` pustí `metriky.py` na oba texty; samostatný běh `metriky.py` na novou verzi proto nepouštěj.

**Git** (jen bez Pythonu). Rozděl oba texty na jednu větu na řádek, odstavec je jinak pro diff jeden dlouhý řádek. Regex drží pohromadě slova s diakritikou a čísla s desetinnou čárkou:

```sh
LC_ALL=C.UTF-8 git diff --no-index --word-diff=plain \
  --word-diff-regex='[[:alnum:]]+([.,][[:digit:]]+)*|[^[:space:]]' \
  pred.txt po.txt | tail -n +6
```

`LC_ALL=C.UTF-8` je povinné. V locale `C` regex dělí UTF-8 po bajtech a výstup poškodí (`Ob�[-� pos-]`). Ztrátu čísel a jmen git nehlídá, projdi ji v diffu ručně. Řádek metrik bez Pythonu chybí; řekni to jednou větou.

**Bez shellu** porovnej tabulku s čistou verzí sám: každý rozdíl mezi zdrojem a čistou verzí má řádek v tabulce, čísla a jména ze zdroje jsou v čisté verzi.

## Úprava souboru

Přepis proveď jako úpravu kopie souboru (například `text.unslop.md` vedle originálu), u režimu Úprava souboru přímo v souboru. Diff ukáže rozhraní agenta, proto ho do odpovědi nepřepisuj. Tabulka změn má pozice `soubor:řádek` v upraveném souboru; čistá verze je soubor sám, v odpovědi stačí cesta.

## Revizní stránka a sledované změny

Jen když o ně zadavatel požádá. Revizní stránka (artefakt) ukáže tabulku se dvěma sloupci vedle sebe, změněná slova zvýrazní a pozice odkáže na místo v plném textu. Soubor .docx dostane změny jako sledované změny a důvod jako komentář. Obsah se nemění: čísla změn, pozice, metriky i seznam `[OVĚŘIT: …]` zůstávají.

## Řádek metrik

```text
Metriky před → po: částice 6,1 → 6,1 · jištění 4,0 → 2,0 · otázky 0 → 0 · čísla 18 → 12 · jména 30 → 30
```

Pokles čísel, jmen, částic nebo jištění je varování: vrať se do diffu a najdi, kde zmizely. Když pokles odpovídá vědomé změně (smazaná vágní autorita), napiš to za řádek jednou větou. V úpravě souboru pusť `diff.py --metriky` na zdroj a kopii a převezmi jen řádek.

## Ukázka přepisu (text v chatu, bez shellu)

VSTUP (profil blog):

> Pojďme se ponořit do světa datové analytiky. Moderní nástroje umožňují týmům adresovat problémy na denní bázi. Odborníci se shodují, že firmy, které investují do dat, jsou úspěšnější.

VÝSTUP:

Krátký odstavec s chatbotím úvodem, kalky a vágní autoritou: P0 1, P1 2, P2 0.

P = priorita úpravy: P0 ničí důvěru, P1 zřetelný AI tik, P2 drobnost; ¶1.2 = 1. odstavec, 2. věta.

| # | kde | P | původně | návrh | proč |
|---|---|---|---|---|---|
| 1 | ¶1.1 | P1 | Pojďme se ponořit do světa datové analytiky. | (smazat) | šablonovitý úvod: věta nic neříká, „ponořit se do“ je kalk |
| 2 | ¶1.2 | P1 | …umožňují týmům adresovat problémy na denní bázi. | …pomáhají týmům řešit problémy každý den. | kalky: „adresovat problém“ a „na denní bázi“ |
| 3 | ¶1.3 | P0 | Odborníci se shodují, že firmy… | `[OVĚŘIT: kdo to tvrdí a o jaká data se opírá]` Firmy… | vágní autorita: „odborníci“ bez jména a zdroje |

- `[OVĚŘIT: kdo to tvrdí a o jaká data se opírá]`

Ponechané: „Moderní nástroje“ je obecné, ale bez zbytku článku nejde zpřesnit.

Řádek metrik chybí, skript neběžel (text má tři věty a agent nemá shell).

Čistá verze:

> Moderní nástroje pomáhají týmům řešit problémy každý den. [OVĚŘIT: kdo to tvrdí a o jaká data se opírá] Firmy, které investují do dat, jsou úspěšnější.

Druhý průchod nic nenašel, proto se nepíše. Oddíl bez obsahu se nepíše vůbec.

## Volání z jiného skillu

Neptej se nikdy, ani na cíl. Volající dostane opravený text a pod ním seznam změn bez tabulky, protože ho volající skill dál zpracovává a tabulku by musel rozebírat:

```text
[1] ¶1.2 · P1 · kalky · „adresovat problém“ a „na denní bázi“
před: Moderní nástroje umožňují týmům adresovat problémy na denní bázi.
po: Moderní nástroje pomáhají týmům řešit problémy každý den.
```

Značky `[OVĚŘIT: …]` jdou jen do seznamu pod textem, text zůstává bez nich. V režimu psaní, kde žádný zdroj není, dostane volající jen text a seznam neověřených údajů.
