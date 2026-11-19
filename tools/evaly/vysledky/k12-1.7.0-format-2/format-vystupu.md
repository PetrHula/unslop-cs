# Případy o formátu výstupu: k12-1.7.0-format-2

Commit `091c8b2`, otisk skillu `faba351ad4d9`. Tvar výstupu se kontroluje ručně podle OČEKÁVÁNO v `pripady.md`.

## Případ 31, běh 1

Tokeny: vstup celkem 158005, výstup 2548, kroků 4; nástroje: Skill, Bash

> Shell mi nepovolil spustit `metriky.py`, tak jsem text posoudil ručně.
> 
> **Verdikt:** 1 × P0, 3 × P1, 0 × P2. Text je šablonovitý jako celek: ohlašovací úvod, kalky, vágní autorita a nekonkrétní tvrzení. Poslední věta je jediná konkrétní.
> Legenda: P0 ničí důvěru, P1 zřetelný AI tik, P2 drobnost. ¶1.2 = 1. odstavec, 2. věta.
> 
> | # | kde | P | původně | návrh | proč |
> |---|---|---|---|---|---|
> | 1 | ¶1.1 | P1 | Pojďme se ponořit do světa datové analytiky. | (smazat) | šablonovitý úvod: ohlašuje téma a nic neříká |
> | 2 | ¶1.2 | P1 | …umožňují týmům adresovat problémy na denní bázi. | …pomáhají týmům řešit problémy každý den. | kalky „adresovat problém“ a „na denní bázi“ |
> | 3 | ¶1.3 | P0 | Odborníci se shodují, že firmy, které investují do dat, jsou úspěšnější. | Firmy, které investují do dat, bývají úspěšnější `[OVĚŘIT: zdroj a míra]`. | vágní autorita bez zdroje; zobecnění „jsou úspěšnější“ změkčeno na „bývají“ |
> | 4 | ¶1.2 | P1 | Moderní nástroje umožňují… | Nástroje pomáhají… | prázdné „moderní“ a „umožňují“ (reklamní slovník) |
> 
> Změny 2 a 4 jsou jedna úprava věty, v čisté verzi jsou sloučené.
> 
> **Značky k doplnění:**
> - `[OVĚŘIT: zdroj a míra]`: kdo to tvrdí a o kolik jsou firmy úspěšnější.
> - `[OVĚŘIT: 12 % čeho]`: úspora nákladů, času, nebo něco jiného? Nevím to a nedomýšlím si to.
> 
> **Ponechané:** poslední věta zůstává beze změny. Je konkrétní (jméno, město, číslo, období) a „asi“ je autorovo jištění, takže ho nechávám. Nad rámec zdroje jsem nic nepřidal: žádné „já“, žádné vymyšlené číslo ani příběh.
> 
> **Čistá verze:**
> 
> Nástroje pomáhají týmům řešit problémy každý den. Firmy, které investují do dat, bývají úspěšnější [OVĚŘIT: zdroj a míra]. Loni ušetřila brněnská firma Kovo 12 % [OVĚŘIT: 12 % čeho], a to asi díky novému skladu.
> 
> Až doplníte zdroj, dá se druhá věta přepsat na konkrétní: „Podle [zdroj] jsou firmy investující do dat o [X] úspěšnější.“ Bez něj ji doporučuji smazat. Věta o Kovu pak nese celý text a je lepší ji dát na začátek.
