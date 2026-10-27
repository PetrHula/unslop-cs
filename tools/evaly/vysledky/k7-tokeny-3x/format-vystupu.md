# Případy o formátu výstupu: k7-tokeny-3x

Commit `b2dc6f1`, otisk skillu `7eff2aad6076`. Tvar výstupu se kontroluje ručně podle OČEKÁVÁNO v `pripady.md`.

## Případ 31, běh 1

Tokeny: vstup celkem 170384, výstup 2319, kroků 5; nástroje: Skill, Read, Read

> **Verdikt:** text je hodně slopový, 1 × P0, 2 × P1. Skript jsem nepouštěl, protože text má čtyři věty. Reference jsem přečetl.
> 
> **Změny**
> 
> [1] P1 · šablonovitý úvod, „ponořit se“ a text o sobě · nic neříká, jen ohlašuje, že něco bude
> před: Pojďme se ponořit do světa datové analytiky.
> po: (smazáno, text začíná rovnou věcí)
> 
> [2] P1 · kalky „adresovat“ a „na denní bázi“, vata „moderní nástroje umožňují“ · dabing z angličtiny a věta, která platí o čemkoli
> před: Moderní nástroje umožňují týmům adresovat problémy na denní bázi.
> po: Týmy díky nástrojům řeší problémy každý den. `[OVĚŘIT: které nástroje a jaké problémy]`
> 
> [3] P0 · vágní autorita bez zdroje · „odborníci se shodují“ nemá jméno ani studii, tak jsem je nenahradil žádnou vymyšlenou
> před: Odborníci se shodují, že firmy, které investují do dat, jsou úspěšnější.
> po: Firmy, které investují do dat, jsou úspěšnější. `[OVĚŘIT: kdo to tvrdí, jaká studie, jaký vzorek, co znamená „úspěšnější“]`
> 
> **Ponecháno:** čtvrtá věta zůstává beze změny. Má jméno, místo, rok i číslo, což je přesně to, co textu chybí jinde. „Asi“ je skutečné jištění, protože příčina úspory není doložená, takže ho nemažu. Chybí jen základ: 12 % čeho. `[OVĚŘIT: 12 % čeho, nákladů, logistiky?]`
> 
> **Značky k doplnění:**
> - které nástroje a jaké problémy (věta 2)
> - zdroj tvrzení o investicích do dat a význam slova „úspěšnější“ (věta 3)
> - 12 % čeho (věta 4)
> 
> **Čistá verze:**
> 
> Týmy díky nástrojům řeší problémy každý den. `[OVĚŘIT: které nástroje a jaké problémy]` Firmy, které investují do dat, jsou úspěšnější. `[OVĚŘIT: zdroj a míra úspěšnosti]` Loni ušetřila brněnská firma Kovo 12 %, a to asi díky novému skladu. `[OVĚŘIT: 12 % čeho]`
> 
> Poznámka: věty 2 a 3 jsou obecné i po opravě. Víc textu z nich nevytvořím, pokud nedodáte fakta. Příklad s Kovem je jediný konkrétní bod, takže by dával smysl jako začátek, ne jako závěr odstavce.

## Případ 31, běh 2

Tokeny: vstup celkem 335821, výstup 2521, kroků 8; nástroje: Skill, Read, Read, Write, Bash, Read

> Text je krátký a sedí na něj tři nálezy: P0 1, P1 2, P2 0. Skript `metriky.py` jsem nepustil, protože shell byl zamítnutý. Počty jsou z ručního průchodu a řádek metrik před → po proto chybí.
> 
> ```text
> [1] P1 · šablonovitý úvod · věta nenese informaci, „ponořit se do“ je kalk
> před: Pojďme se ponořit do světa datové analytiky.
> po: (smazáno)
> 
> [2] P1 · kalky · „adresovat problém“ a „na denní bázi“
> před: Moderní nástroje umožňují týmům adresovat problémy na denní bázi.
> po: Moderní nástroje pomáhají týmům řešit problémy každý den.
> 
> [3] P0 · vágní autorita · „odborníci“ bez jména a zdroje
> před: Odborníci se shodují, že firmy, které investují do dat, jsou úspěšnější.
> po: [OVĚŘIT: kdo to tvrdí a o jaká data se opírá] Firmy, které investují do dat, jsou úspěšnější.
> ```
> 
> **Ponechané:** Poslední věta zůstává beze změny. Je jediná konkrétní: obsahuje jméno, rok, číslo a jištění „asi“, které se nemaže. Použil jsem ji jako oporu pro zbytek textu.
> 
> **Značky `[OVĚŘIT: …]`:**
> - `[OVĚŘIT: kdo to tvrdí a o jaká data se opírá]` (věta 3)
> - `[OVĚŘIT: které nástroje a jaké problémy]`: věta 2 je i po opravě obecná a prošla by do textu o jakémkoli oboru.
> - `[OVĚŘIT: 12 % čeho (nákladů, skladových nákladů?) a jak úspora souvisí s daty]`: věta 4 stojí v odstavci o datech, ale úsporu připisuje skladu.
> 
> **Čistá verze:**
> 
> > Moderní nástroje pomáhají týmům řešit problémy každý den. [OVĚŘIT: kdo to tvrdí a o jaká data se opírá] Firmy, které investují do dat, jsou úspěšnější. Loni ušetřila brněnská firma Kovo 12 %, a to asi díky novému skladu.

## Případ 31, běh 3

Tokeny: vstup celkem 170334, výstup 1812, kroků 5; nástroje: Skill, Read, Read

> **Verdikt:** čtyři věty, tři z nich jsou slop. P0: 1, P1: 3, P2: 0. Poslední věta je v pořádku.
> 
> **Změny**
> 
> [1] P1 · šablonovitý úvod, kalk „pojďme se ponořit do“
> před: „Pojďme se ponořit do světa datové analytiky.“
> po: smazáno. Věta jen ohlašuje téma a nenese žádnou informaci.
> 
> [2] P1 · kalk „adresovat na denní bázi“, nafouknutý význam, vata
> před: „Moderní nástroje umožňují týmům adresovat problémy na denní bázi.“
> po: smazáno. Věta platí o jakémkoli nástroji a jakémkoli týmu. Chybí v ní, který nástroj, jaké problémy a co se změnilo. `[OVĚŘIT: který nástroj, jaké problémy, jaký výsledek]`
> 
> [3] P0 · vágní autorita bez zdroje
> před: „Odborníci se shodují, že firmy, které investují do dat, jsou úspěšnější.“
> po: smazáno. Bez jména odborníka nebo zdroje se tvrzení nedá ověřit. Číslo ani zdroj si nevymýšlím. `[OVĚŘIT: kdo to tvrdí, kdy a podle jakého měřítka úspěšnosti]`
> 
> **Ponechané**
> „Loni ušetřila brněnská firma Kovo 12 %, a to asi díky novému skladu.“ Věta má jméno, místo, období i číslo. Jištění „asi“ je lidský postoj autora, a proto zůstává.
> 
> **Neověřené údaje**
> - `[OVĚŘIT: 12 % čeho – nákladů, provozu? A jak se úspora měřila?]`
> - Věta o Kovu nemluví o datech, jen o skladu. Spojení s datovou analytikou si text musí doložit sám. Doplňte ho, jen pokud je to pravda.
> - Metriky skript neměřil (text má čtyři věty), řádek před → po proto chybí.
> 
> **Čistá verze**
> 
> Loni ušetřila brněnská firma Kovo 12 %, a to asi díky novému skladu.
> 
> Z původního textu zbyla jedna věta. Zbytek byl vata nebo tvrzení bez opory. Pokud k tématu máte vlastní fakta, doplňte je tam, kde jsou značky `[OVĚŘIT]`.

## Případ 32, běh 1

Tokeny: vstup celkem 267106, výstup 2198, kroků 8; nástroje: Skill, Read, Read, Read, Bash, Bash

> Text byl z větší části slop: jedna vágní autorita (P0), dva tiky (P1) a jeden slabší kalk (P2). Poslední věta o firmě Kovo je konkrétní a zůstává.
> 
> ```text
> [1] P1 · šablonovitý úvod, kalk · „Pojďme se ponořit do“ nenese informaci
> před: Pojďme se ponořit do světa datové analytiky.
> po: (smazáno)
> 
> [2] P1 · kalky · „adresovat problémy“ a „na denní bázi“
> před: Moderní nástroje umožňují týmům adresovat problémy na denní bázi.
> po: Moderní nástroje pomáhají týmům řešit problémy každý den.
> 
> [3] P0 · vágní autorita · „Odborníci se shodují“ bez jména a zdroje
> před: Odborníci se shodují, že firmy, které investují do dat, jsou úspěšnější.
> po: [OVĚŘIT: kdo to tvrdí a o jaká data se opírá] Firmy, které investují do dat, jsou úspěšnější.
> ```
> 
> Ponechané: „Moderní nástroje“ je obecné, ale bez zbytku článku to nejde zpřesnit. Poslední věta zůstává beze změny: má číslo, jméno, místo, období a autorovo jištění „asi“. Jištění ani číslo jsem nemazal.
> 
> Metriky před → po: částice 0 → 0 · jištění 25,6 → 27 · otázky 0 → 0 · čísla 25,6 → 27 · jména 25,6 → 54,1. Hodnoty rostou jen proto, že text zkrácením zmenšil jmenovatel, nic z textu nezmizelo.
> 
> Značky k doplnění:
> - `[OVĚŘIT: kdo to tvrdí a o jaká data se opírá]`
> 
> Čistá verze:
> 
> > Moderní nástroje pomáhají týmům řešit problémy každý den. [OVĚŘIT: kdo to tvrdí a o jaká data se opírá] Firmy, které investují do dat, jsou úspěšnější. Loni ušetřila brněnská firma Kovo 12 %, a to asi díky novému skladu.

## Případ 32, běh 2

Tokeny: vstup celkem 257690, výstup 2890, kroků 7; nástroje: Skill, Read, Read, Bash, Bash

> Verdikt: text má vzorce, které se dají odstranit, ale jde hlavně o dvě mezery v obsahu. Nálezy: P0 1, P1 2, P2 1. Skript doběhl, `diff.py` shell nepustil (zamítnutý Bash), takže chybí řádek metrik před → po.
> 
> **Změny**
> 
> [1] P0 · vágní autorita · tvrzení bez zdroje
> před: „Odborníci se shodují, že firmy, které investují do dat, jsou úspěšnější.“
> po: „Firmy, které investují do dat, jsou úspěšnější. `[OVĚŘIT: kdo to tvrdí, na jakých datech a co je „úspěšnější“]`“
> Odkaz na odborníky bez jména jsem vypustil. Tvrzení samo zůstává ve stejné síle, jen čeká na zdroj.
> 
> [2] P1 · šablonový úvod / kalk „ponořit se“
> před: „Pojďme se ponořit do světa datové analytiky.“
> po: věta pryč, téma přešlo do druhé věty.
> Žádný fakt se neztratil, věta jen ohlašovala, že text začne.
> 
> [3] P1 · kalk „na denní bázi“
> před: „Moderní nástroje umožňují týmům adresovat problémy na denní bázi.“
> po: „Nástroje pro datovou analytiku týmům umožňují řešit problémy každý den. `[OVĚŘIT: jaké problémy, které nástroje]`“
> „Adresovat“ (P2) jsem změnil na „řešit“. „Moderní“ je pryč, protože nic neporovnává.
> 
> **Ponechané**
> - „Loni ušetřila brněnská firma Kovo 12 %, a to asi díky novému skladu.“ Věta má jméno, číslo i období. „Asi“ je skutečné jištění, takže zůstává. Chybí jen základ procent, proto značka níže.
> - Souvislost mezi příkladem Kovo a datovou analytikou ze zdroje nevyplývá (sklad není analytika). Nic jsem nedomýšlel, ale autor by ji měl doplnit.
> 
> **Značky `[OVĚŘIT]`**
> - kdo tvrdí, že firmy investující do dat jsou úspěšnější, na jakých datech a co „úspěšnější“ znamená
> - jaké problémy a které nástroje (věta 2)
> - 12 % čeho (tržeb, nákladů, skladových nákladů)
> 
> **Čistá verze**
> 
> Nástroje pro datovou analytiku týmům umožňují řešit problémy každý den. `[OVĚŘIT: jaké problémy, které nástroje]` Firmy, které investují do dat, jsou úspěšnější. `[OVĚŘIT: kdo to tvrdí, na jakých datech a co je „úspěšnější“]` Loni ušetřila brněnská firma Kovo 12 %, a to asi díky novému skladu. `[OVĚŘIT: 12 % čeho]`

## Případ 32, běh 3

Tokeny: vstup celkem 352304, výstup 2296, kroků 8; nástroje: Skill, Read, Read, Read, Bash, Bash

> Verdikt: text obsahuje vágní autoritu a kalky a ve dvou větách nenese žádný fakt. Našel jsem P0 1, P1 2, P2 1.
> 
> ```text
> [1] P1 · šablonovitý úvod · věta nenese informaci, „ponořit se do“ je kalk
> před: Pojďme se ponořit do světa datové analytiky.
> po: (smazáno)
> 
> [2] P1 · kalky · „adresovat problémy“ a „na denní bázi“
> před: Moderní nástroje umožňují týmům adresovat problémy na denní bázi.
> po: Moderní nástroje pomáhají týmům řešit problémy každý den.
> 
> [3] P0 · vágní autorita · „odborníci se shodují“ bez jména a zdroje
> před: Odborníci se shodují, že firmy, které investují do dat, jsou úspěšnější.
> po: [OVĚŘIT: kdo to tvrdí a o jaká data se opírá] Firmy, které investují do dat, jsou úspěšnější.
> ```
> 
> Ponechané:
> - Čtvrtá věta zůstává slovo od slova. Má jméno, místo, číslo i jištění „asi“.
> - Druhá věta zůstává obecná („moderní nástroje“, „problémy“), ale bez zbytku článku ji nejde zpřesnit. Hodila by se tu konkrétní nástroj a konkrétní problém.
> 
> Seznam značek:
> - `[OVĚŘIT: kdo to tvrdí a o jaká data se opírá]`
> - Ve čtvrté větě chybí, z čeho se těch 12 % počítá (náklady, skladové zásoby, jiný základ). Do textu jsem značku nedával, doplň to z článku.
> 
> Metriky ze skriptu pro původní text (diff.py se nespustil, shell byl zamítnutý, takže chybí řádek před → po): čísla 25,6 a jména 25,6 na 1000 slov. Čísla i jména jsem zachoval, tedy Kovo, Brno, 12 % i „asi“.
> 
> Čistá verze:
> 
> > Moderní nástroje pomáhají týmům řešit problémy každý den. [OVĚŘIT: kdo to tvrdí a o jaká data se opírá] Firmy, které investují do dat, jsou úspěšnější. Loni ušetřila brněnská firma Kovo 12 %, a to asi díky novému skladu.
> 
> Značku před zveřejněním nahraď zdrojem, nebo tvrzení o úspěšnějších firmách vypusť. Příklad s Kovem by pak stál sám a dával by smysl i bez něj.
