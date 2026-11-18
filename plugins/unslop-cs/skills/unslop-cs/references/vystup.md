# Úrovně výstupu a diff

Podrobnosti k oddílu Formáty výstupu v `SKILL.md`. Výstup má čtyři úrovně podle toho, co agent umí. Úroveň 0 nepotřebuje žádný nástroj; vyšší úrovně ji jen zpřesňují a obsah výstupu se mezi nimi nemění.

## Zjištění úrovně

Na nástroje se uživatele neptej. Zjisti je sám, bez komentáře:

```sh
python3 --version   # když python3 neexistuje (typicky Windows), použij python nebo py -3
git --version
[ "$(LC_ALL=C.UTF-8 locale charmap 2>/dev/null)" = UTF-8 ] && echo utf8
```

| Výsledek | Úroveň diffu |
|---|---|
| shell chybí nebo všechny příkazy selžou | 0 |
| Python | 1 přes `scripts/diff.py` |
| git a locale `C.UTF-8`, bez Pythonu | 1 přes git |
| zadání je úprava souboru a agent umí soubory editovat | 2 |
| zadavatel výslovně chce revizní stránku nebo sledované změny | 3 |

Neúspěch kteréhokoli kroku tiše znamená nižší úroveň. Uživateli úroveň neoznamuj, výstup mluví sám za sebe.

## Úroveň 0 – po větách

Každá změněná věta dostane číslo, závažnost, vzorec a důvod v jedné hlavičce, pod ní větu před a po. Samostatná tabulka změn se v úrovni 0 nepíše, důvod je v hlavičce:

```text
[1] P0 · vágní autorita · „odborníci“ bez jména a zdroje
před: Odborníci se shodují, že firmy, které investují do dat, jsou úspěšnější.
po: [OVĚŘIT: kdo to tvrdí a o jaká data se opírá] Firmy, které investují do dat, jsou úspěšnější.

[2] P1 · kalky · „adresovat problém“ a „na denní bázi“
před: Moderní nástroje umožňují týmům adresovat problémy na denní bázi.
po: Moderní nástroje pomáhají týmům řešit problémy každý den.
```

- Větu „před“ zkopíruj ze zdroje znak po znaku, včetně překlepů a typografie. Uživatel ji musí najít hledáním.
- Neoznačuj slova uvnitř věty (`~~`, `**`). V delším textu je model píše nespolehlivě a rozbíjejí čitelnost bez vykreslení.
- Když jedna změna zasáhne víc vět (sloučení, přesun), uveď je pod jedním číslem: „před:“ obsahuje všechny původní věty, „po:“ výsledek.
- Smazaná věta má „po: (smazáno)“, nová věta „před: (nová)“. Nová věta smí vzniknout jen z obsahu zdroje (pojistky).

## Úroveň 1 – slovní diff

Oba texty ulož do souborů v pracovním adresáři.

**Python (výchozí).** `scripts/diff.py` rozdělí oba texty na věty, vynechá kód a citace, vypíše slovní diff jen změněných vět a k tomu hlídá tichou ztrátu (čísla, jména, částice a jištění, markery síly tvrzení). Na locale nezávisí:

```sh
python3 <adresář skillu>/scripts/diff.py pred.txt po.txt --metriky --profil blog
```

Výstup (blok diffu, oddíl Tichá ztráta a řádek metrik) přenes do odpovědi beze změny a změny číslované [1], [2]… zapiš do tabulky změn. Co skript hlásí jako ztrátu, buď vrať do nové verze, nebo zapiš do tabulky jako vědomý škrt s důvodem. Hlášení jmen je bez modelu přibližné, před vrácením ho ověř v diffu. `--format json` dá stejná data strojově, `--prisne` vrátí kód 1 při ztrátě. Přepínač `--metriky` pustí `metriky.py` na oba texty a vypíše řádek metrik před → po; po přepisu proto samostatný běh `metriky.py` na novou verzi nepouštěj.

**Git** (jen bez Pythonu). Rozděl oba texty na jednu větu na řádek, odstavec je jinak pro diff jeden dlouhý řádek. Regex drží pohromadě slova s diakritikou a čísla s desetinnou čárkou; uvozovky, pomlčky a tečky stojí zvlášť, takže zůstávají v kontextu:

```sh
LC_ALL=C.UTF-8 git diff --no-index --word-diff=plain \
  --word-diff-regex='[[:alnum:]]+([.,][[:digit:]]+)*|[^[:space:]]' \
  pred.txt po.txt | tail -n +6
```

`LC_ALL=C.UTF-8` je povinné. V locale `C` regex dělí UTF-8 po bajtech a výstup poškodí (`Ob�[-� pos-]`). Výchozí `--word-diff=plain` bez regexu je bezpečné v každém locale, ale hrubé: dělí jen na mezerách, takže „zásadní.“ se změní i s tečkou a uvozovkou. Ztrátu čísel a jmen git nehlídá, projdi ji ručně podle diffu.

Diff vlož do bloku ` ```text `, aby hvězdičky a podtržítka z textu nerozbily formátování. Před každý řádek se změnou dej číslo změny:

```text
[1] Podíl vzrostl na [-1,3-]{+1,5+} % a ve [-2-]{+3+}. čtvrtletí dosáhl 4,5 bodu.
[2] [-Tento krok tak výrazně posílil důvěru občanů-]{+Občané mu víc věří+}, proto ho vítáme.
```

Diff kopíruj z výstupu nástroje beze změny. Když se diff a tabulka změn neshodují (v diffu je změna bez čísla), přepis změnil něco, co neměl: vrať to, nebo změnu doplň do tabulky s důvodem.

## Úroveň 2 – úprava souboru

Přepis proveď jako úpravu kopie souboru (například `text.unslop.md` vedle originálu), u režimu Úprava souboru přímo v souboru. Diff ukáže rozhraní agenta, proto ho do odpovědi nepřepisuj. Vlastní řádky „před → po“ piš jen u změn, které rozhraní nezobrazí (například když nástroj přepsal celý soubor najednou). Čistá verze je soubor sám; v odpovědi stačí cesta.

## Úroveň 3 – na přání

Revizní stránku (artefakt se zvýrazněnými změnami) nebo .docx se sledovanými změnami připrav jen tehdy, když o ni zadavatel požádá. Obsah se nemění: čísla změn, tabulka, metriky i seznam `[OVĚŘIT: …]` zůstávají.

## Řádek metrik

`diff.py --metriky` vypíše řádek metrik postoje a konkrétnosti sám, v úrovni 1 ho přenes s diffem. V úrovni 2 pusť stejný příkaz na zdroj a kopii a převezmi jen řádek. Bez Pythonu řádek chybí a říká se to v odpovědi jednou větou.

```text
Metriky před → po: částice 6,1 → 6,1 · jištění 4,0 → 2,0 · otázky 0 → 0 · čísla 18 → 12 · jména 30 → 30
```

Pokles čísel, jmen, částic nebo jištění je varování: vrať se do diffu a najdi, kde zmizely. Když pokles odpovídá vědomé změně (smazaná vágní autorita), napiš to za řádek jednou větou.

## Ukázka přepisu (úroveň 0)

VSTUP (profil blog):

> Pojďme se ponořit do světa datové analytiky. Moderní nástroje umožňují týmům adresovat problémy na denní bázi. Odborníci se shodují, že firmy, které investují do dat, jsou úspěšnější.

VÝSTUP:

Krátký odstavec s jedním chatbotím úvodem, kalky a vágní autoritou: P0 1, P1 2, P2 0.

```text
[1] P1 · šablonovitý úvod · věta nenese informaci, „ponořit se do“ je kalk
před: Pojďme se ponořit do světa datové analytiky.
po: (smazáno)

[2] P1 · kalky · „adresovat problém“ a „na denní bázi“
před: Moderní nástroje umožňují týmům adresovat problémy na denní bázi.
po: Moderní nástroje pomáhají týmům řešit problémy každý den.

[3] P0 · vágní autorita · „odborníci“ bez jména a zdroje
před: Odborníci se shodují, že firmy, které investují do dat, jsou úspěšnější.
po: [OVĚŘIT: kdo to tvrdí a o jaká data se opírá] Firmy, které investují do dat, jsou úspěšnější.
```

Ponechané: „Moderní nástroje“ je obecné, ale bez zbytku článku nejde zpřesnit.

- `[OVĚŘIT: kdo to tvrdí a o jaká data se opírá]`

Čistá verze:

> Moderní nástroje pomáhají týmům řešit problémy každý den. [OVĚŘIT: kdo to tvrdí a o jaká data se opírá] Firmy, které investují do dat, jsou úspěšnější.

Chybí tabulka změn (důvod je v hlavičkách), řádek metrik (text má dvě věty, skript neběžel) a druhý průchod (nic nenašel). Oddíl bez obsahu se nepíše vůbec.

## Volání z jiného skillu

Neptej se nikdy, ani na cíl. Volající dostane opravený text a pod ním jen seznam změn v úrovni 0. Značky `[OVĚŘIT: …]` jdou jen do seznamu pod textem, text zůstává bez nich. V režimu psaní, kde žádný zdroj není, dostane volající jen text a seznam neověřených údajů.
