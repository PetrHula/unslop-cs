# Případy o formátu výstupu: k14-1.0.3-format

Commit `9a9aee9`, otisk skillu `88cd94d1f839`. Tvar výstupu se kontroluje ručně podle OČEKÁVÁNO v `pripady.md`.

## Případ 31, běh 1

Tokeny: vstup celkem 102247, výstup 1689, kroků 3; nástroje: Skill

> **Verdikt:** text je šablonovitý jako celek (šablonový úvod, kalky, vágní autorita, žádné konkrétní číslo ani jméno kromě poslední věty). P0: 1, P1: 2, P2: 0.
> 
> P = priorita úpravy: P0 ničí důvěru, P1 zřetelný AI tik, P2 drobnost. ¶1.2 = 1. odstavec, 2. věta.
> 
> | # | kde | P | původně | návrh | proč |
> |---|---|---|---|---|---|
> | 1 | ¶1.1 | P1 | Pojďme se ponořit do světa datové analytiky. | (smazat) | šablonovitý úvod, který jen ohlašuje téma a nic nesděluje |
> | 2 | ¶1.2 | P1 | …umožňují týmům adresovat problémy na denní bázi. | …pomáhají týmům řešit problémy každý den. | kalky „adresovat problém“ a „na denní bázi“ |
> | 3 | ¶1.3 | P0 | Odborníci se shodují, že firmy, které investují do dat, jsou úspěšnější. | (smazat) `[OVĚŘIT: zdroj nebo studie k tvrzení o úspěšnosti firem]` | vágní autorita bez zdroje, tvrzení bez čísla a jména |
> 
> **Seznam k ověření:**
> - `[OVĚŘIT: zdroj nebo studie k tvrzení, že firmy investující do dat jsou úspěšnější]`. Bez zdroje větu nevracím.
> - `[OVĚŘIT: jaký nástroj a jaký problém]`. Věta 2 je po úpravě čistší, ale pořád obecná. Konkrétní příklad od autora ji zlepší nejvíc.
> 
> **Jiné vady (nejsou znakem AI):**
> 
> | kde | původně | návrh | co |
> |---|---|---|---|
> | ¶1.4 | …ušetřila brněnská firma Kovo 12 %, a to asi díky novému skladu. | `[OVĚŘIT: 12 % čeho]` | chybí, co se ušetřilo. Příklad s novým skladem také nesouvisí s datovou analytikou, tak ho autor buď propojí, nebo změní. |
> 
> **Ponechané:** věta o firmě Kovo má jméno, číslo i rok, takže je to nejlepší místo textu. Hedge „asi“ je autorův postoj a zůstává.
> 
> **Čistá verze:**
> 
> Moderní nástroje pomáhají týmům řešit problémy každý den. Loni ušetřila brněnská firma Kovo 12 %, a to asi díky novému skladu.
> 
> Chcete, abych to zapsal do souboru, nebo vám stačí text ke zkopírování?

## Případ 32, běh 1

Tokeny: vstup celkem 102553, výstup 1778, kroků 3; nástroje: Skill

> **Verdikt:** text je šablonovitý jako celek (úvod, kalk, vágní autorita, žádný zdroj). Našel jsem P0: 1, P1: 2, P2: 0. Skript jsem nepouštěl, text má jen čtyři věty a posoudil jsem ho čtením.
> 
> P = priorita úpravy: P0 ničí důvěru, P1 zřetelný AI tik. ¶1.2 = 1. odstavec, 2. věta.
> 
> | # | kde | P | původně | návrh | proč |
> |---|---|---|---|---|---|
> | 1 | ¶1.1 | P1 | Pojďme se ponořit do světa datové analytiky. | (smazat) | šablonovitý úvod, který ohlašuje téma a nic neříká |
> | 2 | ¶1.2 | P1 | …umožňují týmům adresovat problémy na denní bázi. | …pomáhají týmům řešit problémy každý den. | kalky „adresovat problém“ a „na denní bázi“ |
> | 3 | ¶1.3 | P0 | Odborníci se shodují, že firmy, které investují do dat, jsou úspěšnější. | Firmy, které investují do dat, jsou úspěšnější `[OVĚŘIT: zdroj tvrzení]`. | vágní autorita bez jména a zdroje |
> 
> **Seznam [OVĚŘIT]:**
> - Kdo nebo jaká studie tvrdí, že firmy investující do dat jsou úspěšnější.
> - 12 % čeho Kovo ušetřila (nákladů? skladových zásob?). Ve zdroji to není, v textu to nechávám tak, jak to je.
> 
> **Ponechané:**
> - „asi díky novému skladu“ je autorovo jištění a odhad, takže zůstává.
> - Věta o Kovu je konkrétní (jméno, město, rok, číslo), proto ji neměním.
> 
> **Čistá verze:**
> 
> Moderní nástroje pomáhají týmům řešit problémy každý den. Firmy, které investují do dat, jsou úspěšnější [OVĚŘIT: zdroj tvrzení]. Loni ušetřila brněnská firma Kovo 12 %, a to asi díky novému skladu.
> 
> Chceš, abych tvrzení o úspěšnějších firmách odstranil úplně? Věta o Kovu totiž stojí i sama a je jediná podložená.
