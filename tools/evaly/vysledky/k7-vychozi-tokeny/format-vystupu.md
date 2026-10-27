# Případy o formátu výstupu: k7-vychozi-tokeny

Commit `21bc601`, otisk skillu `edb8edd7fa1a`. Tvar výstupu se kontroluje ručně podle OČEKÁVÁNO v `pripady.md`.

## Případ 31, běh 1

Tokeny: vstup celkem 269300, výstup 2876, kroků 8; nástroje: Skill, Read, Read, Read, Write, Bash

> Shell mi nepovolil spustit `metriky.py`, takže jsem text změřel ručně. Text má jen čtyři věty a zbytek postupu proběhl podle referencí.
> 
> Verdikt: dvě věty jsou slop, jedna je neověřená a jedna je čistá. Nálezy: P0 1, P1 2, P2 0.
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
> | 1 | P1 | šablonovitý úvod | Věta nenese informaci a „ponořit se do“ je kalk. |
> | 2 | P1 | kalky | „Adresovat problém“ a „na denní bázi“ jsou kalky z angličtiny. |
> | 3 | P0 | vágní autorita | „Odborníci“ bez jména a zdroje. Tvrzení o úspěšnosti jsem nezpřesňoval, protože zdroj chybí. |
> 
> Ponechané:
> - **Věta o Kovu:** nechal jsem ji celou. Má jméno, číslo, dobu i „asi“, což je lidské jištění, takže jsem je nemazal.
> - **„Moderní nástroje umožňují“:** je obecné, ale samo o sobě to není nález. Zpřesnit ho jde jen s informací, kterou ve zdroji nemám.
> 
> Druhý průchod nenašel nový tik ani chybu ve shodě nebo čárkách. Částice „asi“, číslo 12 % i obě jména (Brno, Kovo) zůstala.
> 
> Metriky: skript neběžel, protože shell byl zamítnut. Ručně: částice 1 → 1, jištění 1 → 1, otázky 0 → 0, čísla 1 → 1, jména 2 → 2.
> 
> Značky k doplnění:
> - `[OVĚŘIT: kdo to tvrdí a o jaká data se opírá]`
> - Mimo text: 12 % čeho (nákladů, výdajů na provoz?) a na čem stojí vazba na nový sklad. Zdroj to neříká a nic jsem nedomýšlel.
> 
> Čistá verze:
> 
> > Moderní nástroje umožňují týmům řešit problémy každý den. [OVĚŘIT: kdo to tvrdí a o jaká data se opírá] Firmy, které investují do dat, jsou úspěšnější. Loni ušetřila brněnská firma Kovo 12 %, a to asi díky novému skladu.
> 
> Pokud k tvrzení o úspěšnosti žádný zdroj nemáš, nejpoctivější je druhou větu vypustit a nechat za ní jen příklad Kova.

## Případ 32, běh 1

Tokeny: vstup celkem 285455, výstup 3200, kroků 9; nástroje: Skill, Read, Read, Read, Bash, Write, Bash

> Text jsem přepsal, ale konečné měření nového textu se nespustilo: shell mi u druhého příkazu odepřel oprávnění. Diff proto vychází z úrovně 0, po větách. Původní text jsem změřil skriptem před přepisem.
> 
> **Verdikt:** krátký odstavec s vágní autoritou, dvěma kalky a prázdným úvodem. Nálezy: P0 1, P1 2, P2 1.
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
> po: [OVĚŘIT: kdo tvrdí, že firmy investující do dat jsou úspěšnější, a z jakých dat to vychází] Firmy, které investují do dat, jsou úspěšnější.
> ```
> 
> | # | P | Vzorec | Proč |
> |---|---|---|---|
> | 1 | P1 | šablonovitý úvod | věta nenese informaci, „ponořit se do“ je kalk |
> | 2 | P1 (+P2) | kalky | „na denní bázi“ je P1, „adresovat problémy“ P2 |
> | 3 | P0 | vágní autorita | „odborníci se shodují“ bez jména a zdroje |
> 
> **Ponechané:**
> - „Moderní nástroje“ je obecné, ale bez zbytku článku nejde zpřesnit.
> - Poslední věta zůstává celá. Má číslo, jméno a jištění „asi“, tedy přesně to, co se při přepisu nemá ubírat. Spojení „ušetřila 12 %“ nic dalšího neříká (čeho), to je mezera zdroje, ne tik.
> 
> **Metriky:** po přepisu neměřeno. Zdroj před přepisem: částice 1 slovo na 39 · jištění 25,6 na 1000 slov · otázky 0 · čísla 25,6 · jména 25,6. Po přepisu nic z toho neubylo: věta s „asi“, číslem a jménem Kovo zůstala beze změny.
> 
> **Druhý průchod:** nový tik ani chybu ve shodě jsem nenašel. Nahrazení „umožňují“ za „pomáhají“ mírně zeslabuje sílu tvrzení, takže ji případně vrať, pokud zdroj říká „umožňují“ doslova.
> 
> **Značky k doplnění:**
> - `[OVĚŘIT: kdo tvrdí, že firmy investující do dat jsou úspěšnější, a z jakých dat to vychází]`
> 
> **Čistá verze:**
> 
> > Moderní nástroje pomáhají týmům řešit problémy každý den. [OVĚŘIT: kdo tvrdí, že firmy investující do dat jsou úspěšnější, a z jakých dat to vychází] Firmy, které investují do dat, jsou úspěšnější. Loni ušetřila brněnská firma Kovo 12 %, a to asi díky novému skladu.
> 
> Je uložená i v `/tmp/claude-0/-tmp-unslop-eval-mr5087yg/eca9f5b4-cc07-5c69-96d0-9e0f51e19304/scratchpad/po.txt`. Pokud chceš měření nové verze, povol shell a pustím `metriky.py` a `diff.py`.
