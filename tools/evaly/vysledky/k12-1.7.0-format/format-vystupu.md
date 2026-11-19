# Případy o formátu výstupu: k12-1.7.0-format

Commit `091c8b2`, otisk skillu `d717f63b33d0`. Tvar výstupu se kontroluje ručně podle OČEKÁVÁNO v `pripady.md`.

## Případ 31, běh 1

Tokeny: vstup celkem 101046, výstup 1982, kroků 3; nástroje: Skill

> **Verdikt:** 1 P0, 2 P1, 1 P2. Text je šablonovitý jako celek: ohlášení tématu, kalky, vágní autorita a téměř žádné konkrétní údaje kromě poslední věty. P0 ničí důvěru, P1 je zřetelný AI tik, P2 drobnost.
> 
> | # | kde | P | původně | návrh | proč |
> |---|---|---|---|---|---|
> | 1 | ¶1.1 | P1 | Pojďme se ponořit do světa datové analytiky. | (smazat) | šablonovitý úvod: ohlašuje téma místo toho, aby ho rozvinul |
> | 2 | ¶1.2 | P1 | …umožňují týmům adresovat problémy na denní bázi. | …pomáhají týmům řešit problémy každý den. [OVĚŘIT: které nástroje a jaké problémy] | kalky „adresovat problém“ a „na denní bázi“; věta je bez konkrétního příkladu |
> | 3 | ¶1.3 | P0 | Odborníci se shodují, že firmy, které investují do dat, jsou úspěšnější. | Firmy, které investují do dat, jsou úspěšnější. [OVĚŘIT: zdroj, studie nebo jméno] | vágní autorita bez zdroje; tvrzení „úspěšnější“ nemá míru ani měřítko |
> | 4 | ¶1.4 | P2 | Loni ušetřila brněnská firma Kovo 12 %… | beze změny, jen doplnit [OVĚŘIT: 12 % čeho, například nákladů na logistiku] | chybí, k čemu se procento vztahuje |
> 
> **K doplnění:**
> - Které nástroje a jaké problémy má věta 2 na mysli.
> - Zdroj tvrzení o úspěšnějších firmách.
> - Základ 12% úspory u firmy Kovo.
> 
> **Ponechané:**
> - „asi díky novému skladu“: opatrný odhad ze zdroje, zůstává. Částice „asi“ drží sílu příčiny na úrovni odhadu.
> - Brněnská firma Kovo, rok („loni“) a 12 %: konkrétní údaje, nesahal jsem na ně.
> 
> **Čistá verze:**
> 
> Moderní nástroje pomáhají týmům řešit problémy každý den. [OVĚŘIT: které nástroje a jaké problémy] Firmy, které investují do dat, jsou úspěšnější. [OVĚŘIT: zdroj] Loni ušetřila brněnská firma Kovo 12 % [OVĚŘIT: čeho], a to asi díky novému skladu.
> 
> Značky `[OVĚŘIT]` nahraďte skutečnými údaji, nebo příslušné věty vynechte. Bez nich text zůstává obecný. Konkrétní příklad firmy Kovo by mohl být jeho jádrem a celý text by se pak dal postavit kolem něj.

## Případ 32, běh 1

Tokeny: vstup celkem 101082, výstup 1825, kroků 3; nástroje: Skill

> **Verdikt:** přepis má 1 P0, 3 P1 a 0 P2. Text je šablonovitý jako celek: má šablonový úvod, kalky, vágní autoritu a obecné tvrzení bez čísla.
> 
> P0 ničí důvěru, P1 je zřetelný AI tik, P2 drobnost. Pozice `¶1.2` je druhá věta prvního odstavce.
> 
> | # | kde | P | původně | návrh | proč |
> |---|---|---|---|---|---|
> | 1 | ¶1.1 | P1 | Pojďme se ponořit do světa datové analytiky. | (smazat) | Šablonovitý úvod, který jen ohlašuje téma a nic neříká. |
> | 2 | ¶1.2 | P1 | …umožňují týmům adresovat problémy na denní bázi. | …pomáhají týmům řešit problémy každý den. | Kalky „adresovat problém“ a „na denní bázi“. |
> | 3 | ¶1.3 | P0 | Odborníci se shodují, že firmy, které investují do dat, jsou úspěšnější. | (smazat) `[OVĚŘIT: kdo to tvrdí, jaká studie nebo čísla]` | Vágní autorita bez zdroje. |
> | 4 | ¶1.4 | P1 | …Kovo 12 %, a to asi díky novému skladu. | beze změny, `[OVĚŘIT: 12 % čeho a jak nový sklad souvisí s daty]` | Číslo je bez základu a příklad nenavazuje na téma datové analytiky. Jde o chybějící fakt, ne o formulační vadu. |
> 
> **K ověření:**
> - Kdo a na základě čeho tvrdí, že firmy investující do dat jsou úspěšnější (věta z ¶1.3, kterou jsem smazal).
> - Jaký základ má těch 12 % (náklady, sklad, zásoby…).
> - Jak nový sklad souvisí s datovou analytikou.
> 
> **Ponechané:** „asi“ ve čtvrté větě zůstává, protože je to autorovo jištění odhadu, ne vata. Číslo, město a jméno firmy beze změny. „Moderní nástroje“ je obecné, ale bez zdroje nemám čím ho nahradit.
> 
> **Čistá verze:**
> 
> Moderní nástroje pomáhají týmům řešit problémy každý den. Loni ušetřila brněnská firma Kovo 12 %, a to asi díky novému skladu.
> 
> Pokud chcete, aby text držel pohromadě, doplňte, jak sklad s daty souvisí. Zatím z něj čtenář tuhle souvislost nepozná.
