# Případy o formátu výstupu: k7-vychozi-tokeny-3x

Commit `21bc601`, otisk skillu `edb8edd7fa1a`. Tvar výstupu se kontroluje ručně podle OČEKÁVÁNO v `pripady.md`.

## Případ 31, běh 1

Tokeny: vstup celkem 268541, výstup 2220, kroků 7; nástroje: Skill, Read, Read, Read, Bash

> **Verdikt:** čtyři věty, z toho jedna vágní autorita (P0), úvodní fráze a kalky (P1). Poslední věta je v pořádku. P0: 1, P1: 2, P2: 0.
> 
> Shell mi v tomhle režimu zamítl spuštění `metriky.py`, proto jsem text změřil ručně. Řádek metrik tu proto chybí.
> 
> ```text
> [1] P1 · šablonovitý úvod
> před: Pojďme se ponořit do světa datové analytiky.
> po: (smazáno)
> 
> [2] P1 · kalky
> před: Moderní nástroje umožňují týmům adresovat problémy na denní bázi.
> po: Moderní nástroje pomáhají týmům řešit problémy každý den.
> 
> [3] P0 · vágní autorita
> před: Odborníci se shodují, že firmy, které investují do dat, jsou úspěšnější.
> po: [OVĚŘIT: kdo to tvrdí a o jaká data se opírá] Firmy, které investují do dat, jsou úspěšnější.
> ```
> 
> | # | P | Vzorec | Proč |
> |---|---|---|---|
> | 1 | P1 | šablonovitý úvod | Věta nenese informaci, „ponořit se do“ je přenesené a ohrané. |
> | 2 | P1 | kalky | „Adresovat problém“ a „na denní bázi“ jsou překlad z angličtiny. „Umožňují“ jsem změnil na „pomáhají“, protože je to přirozenější. |
> | 3 | P0 | vágní autorita | „Odborníci“ bez jména a zdroje. Tvrzení o úspěšnosti je bez údaje navíc vágní. Zdroj jsem nevymýšlel, jen jsem označil mezeru. |
> 
> **Ponecháno:**
> - „Moderní nástroje“ je obecné, ale bez zbytku článku to nejde zpřesnit.
> - Poslední větu jsem nechal beze změny. Obsahuje číslo (12 %), jméno (Kovo), místo (Brno), čas (loni) i lidské jištění „asi“. Přesně to česká AI píše málo, takže by se tu nemělo mazat.
> 
> **Druhý průchod:** nenašel nový tik ani chybu ve shodě nebo čárkách.
> 
> **K ověření:** `[OVĚŘIT: kdo to tvrdí a o jaká data se opírá]`
> 
> **Čistá verze:**
> 
> > Moderní nástroje pomáhají týmům řešit problémy každý den. [OVĚŘIT: kdo to tvrdí a o jaká data se opírá] Firmy, které investují do dat, jsou úspěšnější. Loni ušetřila brněnská firma Kovo 12 %, a to asi díky novému skladu.
> 
> Až doplníš zdroj, značku nahraď jménem studie nebo firmy, třeba „Podle průzkumu X z roku Y…“. Pokud ho nemáš, větu o úspěšnějších firmách radši škrtni. Příklad z Kova ji unese i bez ní.

## Případ 31, běh 2

Tokeny: vstup celkem 269138, výstup 2462, kroků 8; nástroje: Skill, Read, Read, Read, Write, Bash

> **Verdikt:** čtyři věty, P0 1, P1 2, P2 0. Poslední věta je konkrétní a zůstává.
> 
> Shell mi byl zamítnut, takže `metriky.py` neběžel. Délky vět, pomlčky i nálezy ze seznamů slov jsem posoudil ručně podle referencí. Text má čtyři krátké věty bez pomlček, trojic a kontrastních obratů. Řádek metrik proto chybí.
> 
> ```text
> [1] P1 · šablonovitý úvod
> před: Pojďme se ponořit do světa datové analytiky.
> po: (smazáno)
> 
> [2] P1 · kalky
> před: Moderní nástroje umožňují týmům adresovat problémy na denní bázi.
> po: Moderní nástroje pomáhají týmům řešit problémy každý den.
> 
> [3] P0 · vágní autorita
> před: Odborníci se shodují, že firmy, které investují do dat, jsou úspěšnější.
> po: [OVĚŘIT: kdo to tvrdí a o jaká data se opírá] Firmy, které investují do dat, jsou úspěšnější.
> ```
> 
> | # | P | Vzorec | Proč |
> |---|---|---|---|
> | 1 | P1 | šablonovitý úvod | věta nenese informaci, „ponořit se do“ je tu přenesené a šablonovité |
> | 2 | P1 | kalky | „adresovat problém“ a „na denní bázi“ z angličtiny, „umožňovat“ je vata |
> | 3 | P0 | vágní autorita | „odborníci se shodují“ bez jména a zdroje |
> 
> **Ponechané:**
> - „Moderní nástroje“ je obecné, ale ze zdroje nejde zpřesnit.
> - „Loni ušetřila brněnská firma Kovo 12 %, a to asi díky novému skladu“ je konkrétní: jméno, místo, období, číslo. „Asi“ je lidské jištění a zůstává.
> 
> **Druhý průchod:** nové tiky ani chyby ve shodě nevznikly, čísla a jména zůstala.
> 
> **Značky `[OVĚŘIT: …]`:**
> - `[OVĚŘIT: kdo to tvrdí a o jaká data se opírá]`
> - Mimo text: Co přesně Kovo ušetřila, tedy 12 % čeho (nákladů, času, skladových zásob)? Věta to neříká. Nic jsem nedopsal.
> 
> **Čistá verze:**
> 
> > Moderní nástroje pomáhají týmům řešit problémy každý den. [OVĚŘIT: kdo to tvrdí a o jaká data se opírá] Firmy, které investují do dat, jsou úspěšnější. Loni ušetřila brněnská firma Kovo 12 %, a to asi díky novému skladu.
> 
> Až doplníš zdroj, značka z textu zmizí. Když zdroj nebude, nejčistší je třetí větu škrtnout. Pak zůstane jen věta o Kovu, která tvrzení o investicích do dat doloží lépe.

## Případ 31, běh 3

Tokeny: vstup celkem 269267, výstup 2244, kroků 8; nástroje: Skill, Read, Read, Read, Write, Bash

> Shell mi nepovolili, takže skript s metrikami neběžel a text jsem změřil ručně. Řádek metrik proto chybí. Reference jsem načetl.
> 
> Text má dvě vady P1 a jednu P0 (vágní autorita). Poslední věta je v pořádku. Má číslo, jméno, období a jištění „asi“, tak ji nechávám.
> 
> ```text
> [1] P1 · šablonovitý úvod
> před: Pojďme se ponořit do světa datové analytiky.
> po: (smazáno)
> 
> [2] P1 · kalky
> před: Moderní nástroje umožňují týmům adresovat problémy na denní bázi.
> po: Moderní nástroje pomáhají týmům řešit problémy každý den.
> 
> [3] P0 · vágní autorita
> před: Odborníci se shodují, že firmy, které investují do dat, jsou úspěšnější.
> po: [OVĚŘIT: kdo to tvrdí a o jaká data se opírá] Firmy, které investují do dat, jsou úspěšnější.
> ```
> 
> | # | P | Vzorec | Proč |
> |---|---|---|---|
> | 1 | P1 | šablonovitý úvod | věta nenese informaci, „ponořit se do“ je kalk |
> | 2 | P1 | kalky | „adresovat problém“ a „na denní bázi“ |
> | 3 | P0 | vágní autorita | „odborníci“ bez jména a zdroje |
> 
> **Ponechané:**
> - „Moderní nástroje“ je obecné, ale bez zbytku článku nejde zpřesnit.
> - Věta o firmě Kovo zůstává beze změny. Číslo, jméno, období a jištění „asi“ jsou přesně to, co se mazat nemá.
> 
> **Druhý průchod:** nenašel nový tik ani chybu ve shodě. Čísla, jména a částice ze zdroje zůstaly.
> 
> **Značky k doplnění:**
> - `[OVĚŘIT: kdo to tvrdí a o jaká data se opírá]`
> 
> **Čistá verze:**
> 
> > Moderní nástroje pomáhají týmům řešit problémy každý den. [OVĚŘIT: kdo to tvrdí a o jaká data se opírá] Firmy, které investují do dat, jsou úspěšnější. Loni ušetřila brněnská firma Kovo 12 %, a to asi díky novému skladu.
> 
> Až doplníš zdroj k třetí větě, bude odstavec držet pohromadě. Kovo pak působí jako konkrétní příklad k obecnému tvrzení. Zdroj ani číslo jsem nevymýšlel.

## Případ 32, běh 1

Tokeny: vstup celkem 189219, výstup 2406, kroků 7; nástroje: Skill, Read, Read, Read, Bash

> Přepsané jsou čtyři věty ze čtyř: jedna smazaná, dvě upravené a jedna ponechaná. Nálezy: P0 1, P1 2, P2 1. Skript běžel na původním textu, na novou verzi ne, protože má jen tři věty.
> 
> ```text
> [1] P1 · šablonovitý úvod
> před: Pojďme se ponořit do světa datové analytiky.
> po: (smazáno)
> 
> [2] P1 · kalky
> před: Moderní nástroje umožňují týmům adresovat problémy na denní bázi.
> po: Moderní nástroje umožňují týmům řešit problémy každý den.
> 
> [3] P0 · vágní autorita
> před: Odborníci se shodují, že firmy, které investují do dat, jsou úspěšnější.
> po: [OVĚŘIT: kdo to tvrdí, o jaká data se opírá a v čem se úspěšnost měří] Firmy, které investují do dat, jsou úspěšnější.
> ```
> 
> | # | P | Vzorec | Proč |
> |---|---|---|---|
> | 1 | P1 | šablonovitý úvod | Věta nenese informaci a „ponořit se do“ je přeneseně použitý kalk. |
> | 2 | P1/P2 | kalky | „Na denní bázi“ je P1, „adresovat problémy“ P2. Obojí je z angličtiny a mluvená čeština řekne „řešit“ a „každý den“. |
> | 3 | P0 | vágní autorita | „Odborníci se shodují“ je bez jména a zdroje. Tvrzení o úspěšnosti je navíc bez čísla a bez měřítka. |
> 
> **Ponechané:**
> - Věta 4 zůstává celá. Má číslo, jméno a příčinu a jištění „asi“ je lidský postoj, takže ho nemažu.
> - „Umožňují“ jsem ve větě 2 nechal. Ve shluku s ostatními slovy je slabé.
> - „Moderní nástroje“ je obecné, ale bez zbytku článku nejde zpřesnit. Označuji to jako P2 a konkrétní nástroje by měl doplnit autor.
> 
> **Druhý průchod:** nenašel nový tik ani chybu ve shodě, čárkách nebo příklonkách. Číslo 12 %, jméno Kovo, jištění „asi“ i příčina „díky novému skladu“ zůstaly.
> 
> **Značky `[OVĚŘIT]`:**
> - `[OVĚŘIT: kdo to tvrdí, o jaká data se opírá a v čem se úspěšnost měří]`
> 
> Čistá verze (značku před zveřejněním buď doplňte zdrojem, nebo větu škrtněte):
> 
> > Moderní nástroje umožňují týmům řešit problémy každý den. [OVĚŘIT: kdo to tvrdí, o jaká data se opírá a v čem se úspěšnost měří] Firmy, které investují do dat, jsou úspěšnější. Loni ušetřila brněnská firma Kovo 12 %, a to asi díky novému skladu.

## Případ 32, běh 2

Tokeny: vstup celkem 367908, výstup 2142, kroků 8; nástroje: Skill, Read, Read, Read, Bash, Bash

> Text je krátký a zasažený: P0 1, P1 2, P2 0. Čtvrtá věta je čistá a zůstává.
> 
> ```text
> [1] P1 · šablonovitý úvod
> před: Pojďme se ponořit do světa datové analytiky.
> po: (smazáno)
> 
> [2] P1 · kalky
> před: Moderní nástroje umožňují týmům adresovat problémy na denní bázi.
> po: Moderní nástroje pomáhají týmům řešit problémy každý den.
> 
> [3] P0 · vágní autorita
> před: Odborníci se shodují, že firmy, které investují do dat, jsou úspěšnější.
> po: [OVĚŘIT: kdo to tvrdí a o jaká data se opírá] Firmy, které investují do dat, jsou úspěšnější.
> ```
> 
> | # | P | Vzorec | Proč |
> |---|---|---|---|
> | 1 | P1 | šablonovitý úvod | věta nenese informaci, „ponořit se do“ je kalk |
> | 2 | P1 | kalky | „adresovat problém“ a „na denní bázi“ |
> | 3 | P0 | vágní autorita | „odborníci“ bez jména a zdroje |
> 
> **Ponechané:**
> - „Moderní nástroje“ je obecné, ale bez zbytku článku nejde zpřesnit.
> - Věta o firmě Kovo zůstává beze změny. Je konkrétní (jméno, rok, číslo) a jištění „asi“ je lidský postoj, který se nemaže.
> 
> **Metriky před → po:** částice 25,6 → 37,0 · jištění 25,6 → 37,0 · otázky 0 → 0 · čísla 25,6 → 37,0 · jména 25,6 → 37,0. Čísla na 1000 slov vzrostla jen proto, že text ztratil slova. Absolutně nic nezmizelo: částice „asi“, číslo 12 % i jméno Kovo zůstaly.
> 
> **Druhý průchod:** nenašel nový tik ani chybu ve shodě. Skript na nové verzi hlásí 0 nálezů P0, P1 i P2.
> 
> **Mezery k ověření:**
> - `[OVĚŘIT: kdo to tvrdí a o jaká data se opírá]`
> - Volitelně: 12 % z čeho (z nákladů na sklad, nebo z celkových nákladů)? Ve zdroji to není, proto jsem nic nedoplňoval.
> 
> **Čistá verze:**
> 
> > Moderní nástroje pomáhají týmům řešit problémy každý den. [OVĚŘIT: kdo to tvrdí a o jaká data se opírá] Firmy, které investují do dat, jsou úspěšnější. Loni ušetřila brněnská firma Kovo 12 %, a to asi díky novému skladu.

## Případ 32, běh 3

Tokeny: vstup celkem 284974, výstup 2644, kroků 8; nástroje: Skill, Read, Read, Read, Bash, Bash

> Verdikt: odstavec má jednu vadu P0 (vágní autorita), dvě P1 (šablonovitý úvod, kalk „na denní bázi“) a jednu P2 (kalk „adresovat problémy“). Druhé měření, na nové verzi, mi shell zamítl, takže jsem metriky před a po porovnal ručně. První měření skriptem na původním textu proběhlo.
> 
> ```text
> [1] P1 · šablonovitý úvod
> před: Pojďme se ponořit do světa datové analytiky.
> po: (smazáno)
> 
> [2] P1 · kalky
> před: Moderní nástroje umožňují týmům adresovat problémy na denní bázi.
> po: Moderní nástroje pomáhají týmům řešit problémy každý den.
> 
> [3] P0 · vágní autorita
> před: Odborníci se shodují, že firmy, které investují do dat, jsou úspěšnější.
> po: [OVĚŘIT: kdo to tvrdí a o jaká data se opírá] Firmy, které investují do dat, jsou úspěšnější.
> ```
> 
> | # | P | Vzorec | Proč |
> |---|---|---|---|
> | 1 | P1 | šablonovitý úvod | věta nenese informaci, „ponořit se do“ je kalk |
> | 2 | P1 | kalky | „adresovat problémy“ a „na denní bázi“ |
> | 3 | P0 | vágní autorita | „odborníci“ bez jména a zdroje |
> 
> **Ponechané:** poslední věta zůstala slovo od slova. Je konkrétní (jméno, město, číslo, „loni“) a „asi“ je lidské jištění, které se nemaže. „Moderní nástroje“ je obecné, ale bez zbytku článku nejde zpřesnit.
> 
> **Metriky před → po (ručně, skript na novou verzi neběžel):** čísla (12 %), jména (Kovo, Brno) i částice „asi“ zůstaly, otázky 0 → 0. Skript na původním textu naměřil jedno číslo a jedno vlastní jméno na 39 slov. Jediný pokles je u vlastních jmen: „Brno“ je jen v přídavném jménu „brněnská“, takže skript ho nepočítá.
> 
> **Druhý průchod:** nenašel nový tik ani chybu ve shodě. Mezera `[OVĚŘIT]` zůstala na místě vágní autority.
> 
> **Co chybí:**
> - `[OVĚŘIT: kdo to tvrdí a o jaká data se opírá]`
> - `[OVĚŘIT: 12 % čeho (nákladů, skladových nákladů?) a na čem se zakládá „asi díky novému skladu“]`
> 
> U druhé značky jsem větu v textu neměnil, jen jsem k ní připsal otázku.
> 
> **Čistá verze:**
> 
> > Moderní nástroje pomáhají týmům řešit problémy každý den. [OVĚŘIT: kdo to tvrdí a o jaká data se opírá] Firmy, které investují do dat, jsou úspěšnější. Loni ušetřila brněnská firma Kovo 12 %, a to asi díky novému skladu.
