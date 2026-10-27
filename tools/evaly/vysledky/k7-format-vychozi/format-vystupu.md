# Případy o formátu výstupu: k7-format-vychozi

Commit `8fd9af6`, otisk skillu `edb8edd7fa1a`. Tvar výstupu se kontroluje ručně podle OČEKÁVÁNO v `pripady.md`.

## Případ 31, běh 1

Tokeny: vstup celkem 269087, výstup 2574, kroků 7; nástroje: Skill, Read, Read, Read, Bash

> Shell mi zamítli, takže skript `metriky.py` neběžel a text jsem posoudil ručně podle pravidel. Řádek metrik proto chybí.
> 
> Odstavec má chatbotí úvod, kalky a vágní autoritu. Poslední věta je konkrétní a zůstává. Nálezy: P0 1, P1 2, P2 0.
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
> | 1 | P1 | šablonovitý úvod | Věta nenese informaci a „ponořit se do“ je přenesené použití. |
> | 2 | P1 | kalky | „Adresovat problém“ a „na denní bázi“ jsou překlady z angličtiny. |
> | 3 | P0 | vágní autorita | „Odborníci se shodují“ je bez jména a zdroje. |
> 
> **Ponechané:**
> - Čtvrtá věta zůstává beze změny. Má jméno, číslo i datum a „asi“ je lidské jištění, které se nemaže.
> - „Moderní nástroje“ je obecné, ale bez zbytku článku nejde zpřesnit.
> 
> **Druhý průchod:** nenašel nový tik ani chybu ve shodě. Fakta a jištění ze zdroje zůstala.
> 
> **Značky k doplnění:**
> - `[OVĚŘIT: kdo to tvrdí a o jaká data se opírá]`
> - U čtvrté věty by se hodilo doplnit, 12 % čeho firma ušetřila. Ve zdroji to chybí, tak jsem nic nepřidal.
> 
> **Čistá verze:**
> 
> > Moderní nástroje pomáhají týmům řešit problémy každý den. [OVĚŘIT: kdo to tvrdí a o jaká data se opírá] Firmy, které investují do dat, jsou úspěšnější. Loni ušetřila brněnská firma Kovo 12 %, a to asi díky novému skladu.
> 
> Odstavec je po úpravě kratší a stojí na jediném doložitelném faktu, tedy na Kovu. Kdybyste k druhé větě doplnili zdroj, bude blogu sedět víc než jakákoli další výměna slov.

## Případ 31, běh 2

Tokeny: vstup celkem 269868, výstup 2804, kroků 8; nástroje: Skill, Read, Read, Read, Write, Bash

> Přepsáno ručně. Shell odmítl spustit měřicí skript, takže řádek metrik chybí. Text má jen čtyři věty a počty jsem určil z pravidel.
> 
> Verdikt: jedna vágní autorita, dva tiky v úvodu a ve druhé větě. Poslední věta je v pořádku. P0 1, P1 2, P2 0.
> 
> ```text
> [1] P1 · šablonovitý úvod
> před: Pojďme se ponořit do světa datové analytiky.
> po: (smazáno)
> 
> [2] P1 · kalky
> před: Moderní nástroje umožňují týmům adresovat problémy na denní bázi.
> po: Moderní nástroje umožňují týmům řešit problémy denně.
> 
> [3] P0 · vágní autorita
> před: Odborníci se shodují, že firmy, které investují do dat, jsou úspěšnější.
> po: [OVĚŘIT: kdo to tvrdí a o jaká data se opírá] Firmy, které investují do dat, jsou úspěšnější.
> ```
> 
> | # | P | Vzorec | Proč |
> |---|---|---|---|
> | 1 | P1 | šablonovitý úvod | věta nenese informaci, „ponořit se do“ je kalk |
> | 2 | P1 | kalky | „adresovat problém“ a „na denní bázi“ jsou překlady z angličtiny |
> | 3 | P0 | vágní autorita | „odborníci“ bez jména a zdroje |
> 
> **Ponechané:**
> - Čtvrtá věta zůstává beze změny. Má jméno, rok i číslo a „asi“ je poctivé jištění, které se nemaže.
> - „Moderní nástroje“ je obecné, ale bez zbytku článku se zpřesnit nedá. Věta [1] zmizela celá, takže text teď začíná tvrzením o nástrojích.
> 
> **Druhý průchod:** nenašel nový tik ani chybu ve shodě nebo čárkách.
> 
> **Značky k doplnění:**
> - `[OVĚŘIT: kdo to tvrdí a o jaká data se opírá]`
> - Věta o firmě Kovo neříká, 12 % čeho se ušetřilo (nákladů na skladování, provozu?). Do textu jsem nic nevkládal, ale `[OVĚŘIT: 12 % čeho]` by se tam hodilo.
> 
> **Čistá verze:**
> 
> > Moderní nástroje umožňují týmům řešit problémy denně. [OVĚŘIT: kdo to tvrdí a o jaká data se opírá] Firmy, které investují do dat, jsou úspěšnější. Loni ušetřila brněnská firma Kovo 12 %, a to asi díky novému skladu.
> 
> Značku před zveřejněním buď nahraď jménem zdroje, nebo ji spolu s větou smaž. Bez zdroje by ta věta zůstala jen holým tvrzením.

## Případ 31, běh 3

Tokeny: vstup celkem 269849, výstup 2741, kroků 8; nástroje: Skill, Read, Read, Read, Write, Bash

> Krátký odstavec s úvodní frází, dvěma kalky a vágní autoritou: P0 1, P1 2, P2 0.
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
> po: [OVĚŘIT: kdo to tvrdí a o jaká data se opírá] Firmy, které investují do dat, jsou úspěšnější.
> ```
> 
> | # | P | Vzorec | Proč |
> |---|---|---|---|
> | 1 | P1 | šablonovitý úvod | věta nenese informaci, „ponořit se do“ je tu kalk |
> | 2 | P1 | kalky | „adresovat problém“ a „na denní bázi“ z angličtiny |
> | 3 | P0 | vágní autorita | „odborníci se shodují“ bez jména a zdroje |
> 
> **Ponechané:**
> - Poslední věta zůstává celá. Má jméno (Kovo), místo (Brno), číslo (12 %) i jištění „asi“, které je lidský postoj, takže jsem nic z toho nemazal.
> - „Moderní nástroje“ je obecné, ale bez zbytku článku se zpřesnit nedá.
> 
> **Metriky:** Skript metrik jsem nemohl spustit, protože shell byl zamítnutý. Měřil jsem ručně: ve čtyřech větách žádná pomlčka, žádná trojice ani kontrastní obrat. Číslo a vlastní jména zůstala, částice a jištění („asi“) také. Řádek metrik před → po proto chybí.
> 
> **Druhý průchod:** Nenašel nový tik ani chybu ve shodě. Smazáním první věty text nepřišel o žádný fakt.
> 
> **Značky k doplnění:**
> - `[OVĚŘIT: kdo to tvrdí a o jaká data se opírá]`
> - Mimo text si ještě ověř, 12 % čeho Kovo ušetřilo (náklady, sklad, doprava?) a odkud je vazba na nový sklad. Zdroj nic takového neříká, tak jsem nic nedoplňoval.
> 
> **Čistá verze:**
> 
> > Moderní nástroje umožňují týmům řešit problémy každý den. [OVĚŘIT: kdo to tvrdí a o jaká data se opírá] Firmy, které investují do dat, jsou úspěšnější. Loni ušetřila brněnská firma Kovo 12 %, a to asi díky novému skladu.
> 
> Před zveřejněním značku buď nahraď skutečným zdrojem, nebo tvrzení o úspěšnějších firmách škrtni. Bez zdroje je to jen prázdné tvrzení.

## Případ 32, běh 1

Tokeny: vstup celkem 367177, výstup 2398, kroků 8; nástroje: Skill, Read, Read, Read, Bash, Bash

> Přepsáno, ale metriky nové verze jsem neměl čím změřit. První běh skriptu proběhl, druhé spuštění shell zamítl. Proto chybí diff skriptem i řádek metrik před → po. Hodnoty z prvního měření jsou níže.
> 
> Verdikt: krátký odstavec s chatbotím úvodem, kalky a vágní autoritou, takže P0 1, P1 2, P2 0. Skript u původního textu hlásil 39 slov, 4 věty a 1 × P0, 2 × P1, 1 × P2. Tu P2 jsem po posouzení neuplatnil.
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
> - „Moderní nástroje“ je obecné, ale bez zbytku článku se zpřesnit nedá.
> - Poslední věta zůstává beze změny. Má jméno, místo, číslo a časový údaj. „Asi“ je jedno jištění, které patří k autorovu postoji.
> 
> **Metriky:** skript naměřil u původního textu jen vzorce a rytmus. Postoj a konkrétnost (částice, jištění, otázky, čísla, jména) z něj nemám. Ručně: číslo „12 %“, jméno „Kovo“ i jištění „asi“ jsem zachoval, takže nic neubylo.
> 
> **Druhý průchod:** nenašel nový tik ani chybu ve shodě. Pomlčky v textu nejsou.
> 
> **Značky k doplnění:**
> - `[OVĚŘIT: kdo to tvrdí a o jaká data se opírá]`
> 
> **Čistá verze:**
> 
> > Moderní nástroje pomáhají týmům řešit problémy každý den. [OVĚŘIT: kdo to tvrdí a o jaká data se opírá] Firmy, které investují do dat, jsou úspěšnější. Loni ušetřila brněnská firma Kovo 12 %, a to asi díky novému skladu.
> 
> Pokud chcete diff a metriky skriptem, povolte mi shell a spustím je.

## Případ 32, běh 2

Tokeny: vstup celkem 370073, výstup 3647, kroků 8; nástroje: Skill, Read, Read, Bash, Write, Bash

> **Verdikt:** text je typický slop v krátkém balení. Nálezy: P0 ×1, P1 ×2, P2 ×1. Obsahu je v něm málo, takže se po opravě zkrátil na tři věty.
> 
> **Diff**
> 
> [1] P1 · šablonovitý úvod („ponořit se“)
> - před: „Pojďme se ponořit do světa datové analytiky.“
> - po: věta zmizela. Nic netvrdila a ozdobně ohlašovala téma.
> 
> [2] P1 · kalk „na denní bázi“ a P2 kalk „adresovat problémy“
> - před: „Moderní nástroje umožňují týmům adresovat problémy na denní bázi.“
> - po: „Týmy s moderními nástroji řeší problémy denně.“
> 
> [3] P0 · vágní autorita bez zdroje
> - před: „Odborníci se shodují, že firmy, které investují do dat, jsou úspěšnější.“
> - po: „Firmy, které investují do dat, jsou úspěšnější [OVĚŘIT: kdo to tvrdí a podle čeho].“
> 
> Čtvrtá věta o firmě Kovo zůstala beze změny.
> 
> **Tabulka změn**
> 
> | # | P | vzorec | proč |
> |---|---|---|---|
> | 1 | P1 | šablonovitý úvod, „ponořit se“ | věta bez informace |
> | 2 | P1/P2 | kalky „na denní bázi“, „adresovat“ | česky „denně“ a „řešit“ |
> | 3 | P0 | vágní autorita „odborníci se shodují“ | chybí jméno, zdroj i definice „úspěšnější“ |
> 
> **Ponechané nálezy:** věta o Kovu je konkrétní (jméno, město, číslo, rok) a „asi“ je lidské jištění, takže zůstává. „Moderní“, „nástroje“ a „umožňují“ samy nález nejsou: je jich málo a skript je označil jen jako info. Slovo „moderní“ jsem nechal, protože odstavec je krátký.
> 
> **Metriky před → po:** částice „asi“ 1 → 1, čísla 1 → 1, vlastní jména 1 → 1 (jmenuje se tu jen Kovo; „brněnská“ skript nepočítá). Počty na 1000 slov vyšly 25,6 → 30,3 jen proto, že text je kratší. Skript hlásí P0/P1/P2 = 0 a postoj ani konkrétnost se nezmenšily.
> 
> **Druhý průchod:** nic nového, shoda a slovosled jsou v pořádku.
> 
> **Značky `[OVĚŘIT]`:**
> - kdo tvrdí, že firmy investující do dat jsou úspěšnější, na jakých datech a co znamená „úspěšnější“
> - volitelně: 12 % čeho (nákladů, skladových zásob?) a zda „loni“ platí pro rok vydání textu
> 
> **Čistá verze**
> 
> Týmy s moderními nástroji řeší problémy denně. Firmy, které investují do dat, jsou úspěšnější [OVĚŘIT: kdo to tvrdí a podle čeho]. Loni ušetřila brněnská firma Kovo 12 %, a to asi díky novému skladu.
> 
> Pro blog je tohle spíš kostra než hotový text. Čtenáři chybí příklad, na kterém by se nástroje a data ukázaly, a ten si vymyslet nesmím. Kovo by takový příklad mohlo nést, kdybyste doplnil, co se na skladu změnilo a z čeho se těch 12 % počítá.

## Případ 32, běh 3

Tokeny: vstup celkem 278174, výstup 3336, kroků 7; nástroje: Skill, Read, Read, Bash, Bash

> **Verdikt:** text je převážně slop. Tři ze čtyř vět jsou vata nebo nepodložené tvrzení. P0: 1, P1: 2, P2: 1.
> 
> **Změny**
> 
> [1] P1 · šablonovitý úvod („Pojďme se ponořit…“), věta bez informace
> - před: „Pojďme se ponořit do světa datové analytiky.“
> - po: smazáno
> 
> [2] P1 + P2 · kalky „adresovat“ a „na denní bázi“
> - před: „Moderní nástroje umožňují týmům adresovat problémy na denní bázi.“
> - po: „Moderní nástroje umožňují týmům řešit problémy denně.“
> 
> [3] P0 · vágní autorita bez zdroje a nepodložené tvrzení
> - před: „Odborníci se shodují, že firmy, které investují do dat, jsou úspěšnější.“
> - po: smazáno. Zdroj ani jméno ve vstupu nejsou, nic jsem nedoplňoval.
> 
> | # | P | vzorec | proč |
> |---|---|---|---|
> | 1 | P1 | šablonovitý úvod | ozvěna „pojďme“, žádná informace |
> | 2 | P1/P2 | kalky | řešit / denně jsou běžná čeština se stejným významem |
> | 3 | P0 | vágní autorita | „odborníci se shodují“ bez zdroje |
> 
> **Ponecháno:** věta o firmě Kovo zůstává beze změny. Je konkrétní (jméno, město, rok, 12 %) a „asi“ je lidské jištění, které se nemaže. „Moderní“ a „umožňují“ jsou samy o sobě slabé signály, bez shluku je nechávám.
> 
> **Metriky:** skript proběhl na původním textu (39 slov, 4 věty). Měření nové verze mi shell zamítl, proto ho nemám. Ručně: částice „asi“, číslo 12 % i jméno Kovo zůstaly, nic z postoje ani konkrétnosti neubylo.
> 
> **Druhý průchod:** nová verze je bez dalších nálezů, shoda a čárky jsou v pořádku.
> 
> **Značky [OVĚŘIT]:**
> - které nástroje a jaké problémy, tedy příklad k větě o nástrojích
> - 12 % čeho (nákladů? skladových nákladů?) a čím nový sklad úsporu způsobil
> - kdo tvrdí, že firmy investující do dat jsou úspěšnější. Pokud existuje zdroj, tvrzení se může vrátit i s ním.
> 
> **Čistá verze**
> 
> Moderní nástroje umožňují týmům řešit problémy denně. Brněnská firma Kovo loni ušetřila 12 %, asi díky novému skladu.
> 
> Soubor `vstup.txt` jsem needitoval, nebylo o to požádáno.
