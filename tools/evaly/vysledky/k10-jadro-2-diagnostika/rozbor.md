# Rozbor k10-jadro-2-diagnostika

Diagnostika před možnou 1.7: evaly na úsporné variantě `tools/benchmark/varianty/unslop-cs-jadro-2` (otisk `81c212c5ce05`, stejný jako v benchmarku `test-3`) přes `runner.py --skill-dir`. 30 případů po 1 běhu, Sonnet 5.5 pro skill i hodnotitele, 3,13 USD. Srovnání s `k9-1.6.1` (stejné nastavení, ale verze 1.6.1 před úpravou po evalech; po úpravě prošly 4 a 23, viz `k9-1.6.1-oprava2`).

Cíl nebyl zjistit, jestli jadro-2 projde, ale co mu chybí, když by se z něj stavěla 1.7.

## Výsledek

| | jadro-2 | 1.6.1 (k9, před úpravou) |
|---|---|---|
| prošlo | 22 z 30 | 26 z 30 |
| čisté | 9/10 | 10/10 |
| medián vstupu na běh | 91 691 | 98 667 (−7 %) |
| medián výstupu na běh | 948 | 1 280 (−26 %) |

Jadro-2 prošlo navíc případy 1 a 21 (oba u 1.6.1 nestabilní, jeden běh nerozhoduje).

## Selhání a co jim chybí

Každé selhání odpovídá pravidlu, které plná `SKILL.md` má a jadro-2 ne:

| případ | co se stalo | pravidlo plné verze |
|---|---|---|
| 3 titulky slajdů | upoutávkové titulky ponechal, příběh prezentace nehodnotil | titulky slajdů (jádro od 1.6.0), profil prezentace |
| 4 e-mail | „Doufám, že vás tento e-mail zastihne“ jen P2 | ustálené kalkované fráze jako P1, profil e-mail |
| 11 ČISTÝ dokumentace | „robustní“ jako P1 | profil dokumentace, filtr přesnosti |
| 13 typografie | „CZK“ ponechal | typografie a mikroformáty (`slova.md`, skript) |
| 16 přepis | P1 „tvrzení bez mechanismu“ u věty s číslem | filtr přesnosti: tvrzení s číslem není prázdné |
| 18 kontext znovu | rekapitulaci kontextu ponechal jako přirozený úvod | odpověď, která staví kontext znovu (jádro od 1.6.0) |
| 23 přepis | „Upřímně řečeno“ ponechal | plastová lidskost a hraná upřímnost P1 (1.6.1) |
| 29 blok kódu | komentář v kódu jako P1 a přepsal ho | kód a citace se nepřepisují (1.3.0) |

Navíc v případu 4 vložil `[OVĚŘIT]` do opravené verze, ačkoli jeho vlastní pojistka říká „do textu ho nevkládej“.

## Co z toho plyne pro 1.7

- Jadro-2 není samostatně vydatelné: chybí mu osm pravidel, která evaly hlídají, a k tomu režimy, profily registrů a formáty výstupu.
- Úspora jadro-2 v benchmarku (`test-3j`, souhrn.json): medián vstupu 93 131 proti 100 231 tokenům, výstupu 2 362 proti 2 662. Rozdíl ve vstupu (asi 7 100 tokenů) odpovídá rozdílu velikosti `SKILL.md` (7,9 proti 23,6 KB), výstup je jen o 300 tokenů kratší. Úspora tedy stojí hlavně na délce jádra; každé vrácené pravidlo ji zmenší.
- 1.7 = jadro-2 + stručná verze osmi pravidel z tabulky + odkaz na `psani.md` a `vystup.md` jen pro režim psaní a úpravu souboru. Odhad jádra 11–13 KB, tedy zhruba poloviční úspora proti jadro-2 (řádově 10–15 % ceny místo 23 %).
