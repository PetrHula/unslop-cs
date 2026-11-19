# Případy o formátu výstupu: k14-1.0.3-format-2

Commit `9a9aee9`, otisk skillu `853a906c54cf`. Tvar výstupu se kontroluje ručně podle OČEKÁVÁNO v `pripady.md`.

## Případ 31, běh 1

Tokeny: vstup celkem 102605, výstup 1911, kroků 3; nástroje: Skill

> **Verdikt:** text je šablonovitý jako celek (ozvěna zadání, kalky, vágní autorita, žádný mechanismus). Našel jsem 1× P0 a 2× P1. Přepsal jsem ho na dvě věty.
> 
> P = priorita úpravy: P0 ničí důvěru, P1 zřetelný AI tik, P2 drobnost. ¶1.2 = 1. odstavec, 2. věta.
> 
> | # | kde | P | původně | návrh | proč |
> |---|---|---|---|---|---|
> | 1 | ¶1.1 | P1 | Pojďme se ponořit do světa datové analytiky. | (smazat) | šablonovitý úvod, který ohlašuje téma a nic neříká |
> | 2 | ¶1.2 | P1 | …umožňují týmům adresovat problémy na denní bázi. | …pomáhají týmům řešit problémy každý den. | kalky „adresovat problém“ a „na denní bázi“; „umožňují“ je nafouknuté |
> | 3 | ¶1.3 | P0 | Odborníci se shodují, že firmy, které investují do dat, jsou úspěšnější. | (smazat) `[OVĚŘIT: zdroj tvrzení o úspěšnosti firem investujících do dat]` | vágní autorita bez zdroje, nepodložené obecné tvrzení |
> | 4 | ¶1.4 | – | …Kovo 12 %, a to asi díky novému skladu. | …Kovo 12 %, asi díky novému skladu. | jen zhuštění; „asi“ zůstává jako autorovo jištění |
> 
> **Je potřeba doplnit:**
> - `[OVĚŘIT: zdroj tvrzení, že firmy investující do dat jsou úspěšnější]`. Pokud zdroj existuje, věta se vrátí s odkazem.
> - `[OVĚŘIT: které nástroje a jaké problémy]`. Věta 2 zůstává obecná.
> - `[OVĚŘIT: 12 % čeho (nákladů, skladových zásob…) a jak sklad souvisí s datovou analytikou]`. Bez toho příklad téma nepodpírá.
> 
> **Ponechané:** „asi“ ve čtvrté větě je autorovo jištění, tak jsem ho nechal. Číslo 12 %, jméno firmy a Brno jsou konkrétní a zůstaly beze změny.
> 
> **Čistá verze:**
> 
> Moderní nástroje pomáhají týmům řešit problémy každý den. Loni ušetřila brněnská firma Kovo 12 %, asi díky novému skladu.

## Případ 32, běh 1

Tokeny: vstup celkem 102695, výstup 2032, kroků 3; nástroje: Skill

> **Verdikt:** text je šablonovitý jako celek (ozvěna zadání, kalk, vágní autorita, k tomu chybí čísla). Nálezy: P0 ×1, P1 ×2, P2 ×0.
> P = priorita úpravy: P0 ničí důvěru, P1 zřetelný AI tik, P2 drobnost. ¶1.2 = 1. odstavec, 2. věta.
> 
> | # | kde | P | původně | návrh | proč |
> |---|---|---|---|---|---|
> | 1 | ¶1.1 | P1 | Pojďme se ponořit do světa datové analytiky. | (smazat) | šablonovitý úvod, který jen ohlašuje téma a nic nesděluje |
> | 2 | ¶1.2 | P1 | …umožňují týmům adresovat problémy na denní bázi. | …umožňují týmům řešit problémy každý den. | kalky „adresovat problém“ a „na denní bázi“ |
> | 3 | ¶1.3 | P0 | Odborníci se shodují, že firmy, které investují do dat, jsou úspěšnější. | (smazat) `[OVĚŘIT: kdo se shoduje, studie nebo zdroj]` | vágní autorita bez zdroje, tvrzení bez čísla a jména |
> 
> **Ověřit:**
> - Kdo konkrétně tvrdí, že firmy investující do dat jsou úspěšnější? Zdroj, studie nebo číslo. Dokud chybí, věta zůstává pryč.
> - Co se u Kova ušetřilo (náklady, čas, zásoby) a vůči čemu se těch 12 % počítá?
> 
> **Ponechané:**
> - „Moderní nástroje“ je slabé přívlastkové slovo, ale samo o sobě je to nanejvýš drobnost.
> - „asi díky novému skladu“ je autorovo jištění. Odhad zůstává odhadem a částice zůstává.
> - Konkrétní příklad (Kovo, Brno, 12 %, loni) je to nejlepší v textu a zůstává beze změny.
> 
> Skripty `metriky.py` a `diff.py` jsem nespouštěl, text má čtyři věty. Čísla a jména jsem porovnal ručně: 12 %, Kovo, Brno a „loni“ zůstaly.
> 
> **Čistá verze:**
> 
> Moderní nástroje umožňují týmům řešit problémy každý den. Loni ušetřila brněnská firma Kovo 12 %, a to asi díky novému skladu.
> 
> Pokud najdete zdroj k tvrzení o úspěšnějších firmách, vložte ho jako samostatnou větu s číslem a jménem. A pokud víte, co těch 12 % znamená, doplňte to, protože právě to má v textu nejvíc váhy.
