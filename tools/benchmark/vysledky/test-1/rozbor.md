# Rozbor běhu test-1: kde je unslop-cs nejlepší a kde nejhorší

Zdroj: `souhrn.json` tohoto běhu (jen agregáty; texty test sady se nečetly), dev běhy `pilot-1` a `kalibrace-1` pro rozklad ceny. Čísla jsou z rozhodovacích vrstev (66 lidských, 66 AI textů), pokud není uvedeno jinak. Jeden běh na text, takže u menších rozdílů chybí rozptyl mezi běhy.

Tento rozbor slouží k výběru, **na čem** pracovat. Konkrétní úpravy skillu se ladí a ověřují na dev sadě, ne podle test sady.

## Shrnutí

unslop-cs je **opatrný a věrný**: falešně označuje lidské texty 5–15× méně než ostatní, nejméně mění lidské texty a nejméně ztrácí jména. Platí za to **2–3× vyšší cenou** proti skillům a **nižší citlivostí na AI text**: na AI textech najde i přepíše nejméně. Část druhé slabiny může být chyba prostředí, ne skillu: měřicí skript v tomto běhu ani jednou neproběhl.

## Kde je výrazně nejlepší

| ukazatel | unslop-cs | anti-ai-slop-cz | humanizer-czech | bez-skillu | poměr |
|---|---|---|---|---|---|
| plané poplachy (lidské texty s nálezem vysoká/střední) | **1,5 %** | 7,6 % | 22,7 % | 16,7 % | 5–15× méně |
| plané poplachy, vrstva wiki | **5,6 %** | 22,2 % | 55,6 % | 44,4 % | 4–10× méně |
| plané poplachy, vrstva úřední | **0 %** | 8,3 % | 41,7 % | 8,3 % | |
| změněný podíl lidského textu | **1,0 %** | 1,8 % | 5,4 % | 1,4 % | 1,4–5× méně |
| ztráta jmen v přepisu AI textu | **4,5 %** | 10,3 % | 6,9 % | 11,8 % | 1,5–2,6× méně |
| ztráta jmen, AI-Koditex | **6,8 %** | 18,8 % | 19,1 % | 17,9 % | ~2,7× méně |
| vzdálenost od stylu autora (všechny vrstvy; záporné = přepis se od autora vzdálil) | **−0,16** | −0,27 | −0,17 | −0,30 | |

Rozdíl v planých poplachech je jediný rozdíl v kvalitě, který má interval celý mimo nulu: −15 p. b. proti bez-skillu, −21 p. b. proti humanizer-czech. Tohle je hlavní argument skillu a úpravy ho nesmějí rozbít.

## Kde je výrazně nejhorší

| ukazatel | unslop-cs | anti-ai-slop-cz | humanizer-czech | bez-skillu | poměr |
|---|---|---|---|---|---|
| cena na text (medián) | 0,29 USD | **0,10** | 0,14 | 0,04 | 2,1× / 2,9× / 7× |
| čas na text (medián) | 44 s | **26 s** | 30 s | 25 s | 1,5–1,8× |
| AUC hustoty nálezů (odliší AI od lidského textu) | 0,74 | 0,79 | 0,80 | **0,85** | nejnižší |
| změněný podíl AI textu | 6,5 % | 20,7 % | 19,0 % | 19,7 % | 3× méně |
| změněný podíl AI textu, AI-Koditex | 17,8 % | 42,9 % | 44,4 % | 36,6 % | 2–2,5× méně |
| výstup (tokeny, medián) | 3 670 | 2 350 | 2 670 | 2 580 | 1,4–1,6× |

Malý zásah do AI textu sám o sobě vadou být nemusí. Posun skóre AI-ovosti je ale u všech skillů blízko nuly, takže benchmark neumí říct, jestli větší zásah ostatních skillů přepis zlepšil. Jistá je jen nižší AUC: hustota nálezů u unslop-cs odlišuje AI text od lidského hůř. Opatrnost tu jde proti citlivosti.

## Proč je dražší

Ceny tokenů dopočtené z dev běhů (sedí přesně): zápis do cache 4 USD/M, čtení z cache 0,10 USD/M, výstup 10 USD/M. Cenu tedy určuje, kolik tokenů vstoupí do kontextu, ne počet kroků.

| část | tokenů | USD/text |
|---|---|---|
| základ (systémový prompt s nástroji, zadání, text) | ~15 tis. | 0,060 |
| `SKILL.md` | ~10 tis. | 0,040 |
| `references/vzorce.md` (povinné čtení) | ~21 tis. | 0,083 |
| `references/slova.md` (povinné čtení) | ~8 tis. | 0,033 |
| výstup | ~3,7–4,4 tis. | 0,04 |
| čtení cache (7 kroků) | ~220 tis. | 0,022 |

anti-ai-slop-cz načte jen svůj `SKILL.md` (~2 tis. tokenů) a reference nečte vůbec.

## Nedostatek testu: skript neproběhl

`metriky.py` v konzoli cp1252 (Windows) spadl na `UnicodeEncodeError`. Druhý pokus model spustil jiným příkazem a povolení `Bash(python3 *)` ho zamítlo, v průměru 0,95 zamítnutí na běh. unslop-cs se tak měřil bez skriptu, který počítá seznamy slov, rytmus a shluky, a zaplatil dva zbytečné kroky. Opraveno v `a7acf69`. Smoke test zamítnutí ukázal, ale nebralo se jako blokující chyba.

Hypotéza k ověření na dev sadě: se skriptem najde unslop-cs na AI textech víc (vyšší AUC) a plané poplachy zůstanou nízko.

## Nedostatky benchmarku a návrhy pro příští srovnání

1. **Kvalitu přepisu benchmark neměří.** Posun skóre AI-ovosti je u všech skillů v řádu setin a stylometrický model na přepisy nereaguje. Soudce A/B a soudce významu neprošli kalibrací. Bod 3 pravidla proto nevyjde nikomu a rozhodnutí spadne vždy na cenu. Návrh pro další verzi pravidla, zapsaný před během: plané poplachy a citlivost (AUC nebo podíl AI textů s nálezem) jako dvojice přesnost a citlivost; zachování jmen a čísel jako měřená kvalita, ne jen pojistka; posun skóre jen informativně.
2. **Pravidlo nevyjadřuje „o fous dražší, ale lepší“.** Kvalita je jen ano/ne a cena rozhoduje jen při shodě. Návrh: vykazovat cenu za kvalitu (například cena na odhalený AI text nebo na lidský text bez planého poplachu) a poměr ceny jako výklad vedle rozhodnutí.
3. **Zamítnutí nástrojů nebylo blokující.** Návrh: smoke test i zpráva vypíší podíl běhů se zamítnutím nebo chybou nástroje a pouštět ostrý běh, když je nad nulou, nejde bez `--povolit-zamitnuti`.
4. **Každé kolo platí za všechny skilly znovu.** anti-ai-slop-cz, humanizer-czech a bez-skillu se nemění (stejný otisk, model a zadání), přesto běží znovu. Návrh: převzít jejich běhy z dřívějšího štítku, když sedí otisk skillu, model, hash zadání a text. Kolo unslop-cs na stejném výběru pak stojí jen jeho běhy (dnes ~65 USD místo ~130 USD).
5. **Pomalé.** 864 volání běželo asi 2 hodiny se 4 souběžnými úlohami (`behy.jobs` 4). Návrh: 8 úloh, pokud to dovolí limity účtu.
6. **Velikost výběru.** Rozdíly v planých poplachech jsou velké, na jejich odhalení stačí méně textů. Pro ladění: pevný dev výběr 40 lidských a 40 AI textů, ostatní skilly změřit jednou a dál převzít; jedno kolo unslop-cs pak ~25 USD.
7. **Test sada je použitá.** Každý další běh na ní je druhý pohled na stejná data. Pro definitivní tvrzení po úpravách skillu buď jeden závěrečný běh na test sadě se záznamem v historii plánu, nebo čerstvá odložená sada.
8. **Jeden běh na text:** chybí rozptyl mezi běhy (kappa) a menší rozdíly (ztráta čísel, posun skóre) jsou na hraně šumu.
