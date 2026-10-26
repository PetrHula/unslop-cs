# Zdroje: o co se pravidla opírají

Skill řeší jen češtinu, většina výzkumu AI slopu je ale o angličtině. Tady jsou jen zdroje, které platí pro češtinu: měřené na češtině (**CZ**), česká norma (**norma**), nebo zjištění, která na jazyce nezávisí (**nezávislé**). Anglická jazyková zjištění (seznamy slov, gramatické rysy) do skillu nepatří, dokud je neověří česká data.

Pravidla bez odkazu sem pocházejí z praxe: architektura z jlwin/unslop_ai, české vzorce z nowork-ai/anti-ai-slop-cz a bejek/humanizer-czech (podrobnosti v README). Ani jeden z těchto skillů svá česká pravidla o měření neopírá.

## Dimenze stylu češtiny

Pravidla odkazují na dimenze multidimenzionálního modelu češtiny (Cvrček a kol. 2018, 2020). Benchmark AI-Koditex ukázal, kterým směrem se od lidí odchyluje česká AI:

| Dimenze | Posun AI v češtině | Co to znamená pro skill |
|---|---|---|
| D1 dynamický / statický, D2 spontánní / připravený | bez konzistentního směru | rytmus a „uhlazenost“ nemají českou oporu; vnucená hovorovost je chyba |
| D3 soudržnost | AI víc | řetězy „který“, korelativa, „svůj“, začátky „Tento…“ (Hustá síť odkazů) |
| D4 jedno téma / víc témat | AI monotematičtější | odbočky nemazat, slovník plošně neochuzovat |
| D5 oslovení adresáta | AI méně | otázky a oslovení ze zdroje zůstávají |
| D6 obecnost / konkrétnost | AI obecnější | univerzální pravidlo, test přenositelnosti, nafouknutý slovník |
| D7 výhled / ohlédnutí | AI víc výhledu | Výhled místo výsledku, šablonovité závěry |
| D8 postoj / faktuálnost | AI méně postoje | částice a jištění nemazat, zesilovače nejsou nález |

## Měřeno na češtině (CZ)

- **Milička, Marklová, Cvrček: Benchmark of stylistic variation in LLM-generated texts.** arXiv 2509.10179. Korpus AI-Koditex: modely dopisovaly psané texty z Koditexu. Zdroj posunů v tabulce výše. Omezení: pokračování textu, ne odpovědi chatbota; chatbotí fráze, formát odpovědí, e-maily a LinkedIn v něm nejsou.
- **AI-Koditex v2** (LINDAT, http://hdl.handle.net/11234/1-6189; popis arXiv 2509.22996) a **Koditex** v KonTextu (`koditex`, psané texty bez poezie a překladů). Z nich je porovnání slov a gramatických rysů, ze kterého vycházejí úrovně v `slova.md` a čísla „AI / lidé“ ve skillu: 25 instruovaných modelů z let 2023–2026, stejných 150 textů, lidská reference 5,08 mil. slov, log-ratio a G2 pro každý model zvlášť. Skripty jsou v repozitáři v `tools/koditex/`.
- **Rysy dimenzí českého modelu**, wiki ČNK: https://wiki.korpus.cz/doku.php/cnk:mda. Které rysy kterou dimenzi nesou (například že D3 nesou korelativa a věty s „který“, ne spojovací výrazy na začátku vět).
- **Cvrček a kol. (2018, 2020): multidimenzionální analýza češtiny.** Osm dimenzí stylu, ze kterých benchmark vychází. https://korpus.cz/mda
- **Milička, Marklová, Drobil, Pospíšilová: Humans can learn to detect AI-generated texts, or at least learn when they can't.** arXiv 2505.01877. 255 rodilých mluvčích, české texty, GPT-4o. Bez zpětné vazby určili správně 55 % textů, se zpětnou vazbou 65 %. AI texty byly čtivější a gramatické; vodítka „čtivý text je lidský“ a „AI je statická a připravená“ klamala. Platné vodítko byla obecnost místo konkrétu. Opora pro univerzální pravidlo, pro zásadu „posuzuj vzorce, ne autorství“ a pro pojistku „oprava nepřidává chyby a nezhoršuje čtivost“.

## Norma (ÚJČ)

Internetová jazyková příručka ÚJČ AV ČR, https://prirucka.ujc.cas.cz/. Typografická pravidla skillu stojí na těchto stránkách: pomlčka (id 165), uvozovky (162), datum (810), čas (820), značky a čísla (785), čárka před „a“ (153), velká písmena (180), přivlastňovací zájmena (630). Norma říká, co je chyba; jestli je chyba zároveň signálem AI, je jiná otázka (dlouhou pomlčku „—“ v češtině nikdo nezměřil).

## Nezávislé na jazyce

- **Shaib, Chakrabarty, Garcia-Olano, Wallace: Measuring AI „Slop“ in Text.** arXiv 2509.19163. Taxonomie slopu: užitečnost informace (hustota, relevance), kvalita informace (fakta, zaujatost), styl. Verdikt „slop“ nejvíc předpovídají relevance, hustota a tón, přitom právě u nich se anotátoři shodují nejméně. Konkrétní kódy (fakta, struktura) se posuzují spolehlivěji než celkový verdikt. Opora pro oddíl Obsah, pro značku `[OVĚŘIT]` a pro rozlišení registrů. Měřeno na angličtině; přenáší se kategorie, ne čísla.
- **Chakrabarty, Laban, Wu: Can AI writing be salvaged?** arXiv 2409.14509. Korpus LAMP: 1 057 anglických odstavců (z 80 % beletrie), 8 035 úprav od 18 spisovatelů. Kategorie úprav s podílem: volba slov 28 % (včetně nejasných zájmen a nadužitého pasiva), stavba věty 20 %, zbytečný výklad 18 %, klišé 17 %. Úpravy od spisovatelů text zlepšily víc než úpravy od modelu. Tvrzení, že prostý pokyn k sebeúpravě nefunguje, článek přebírá z Pan a kol. (2024), sám ho neměří. Přenáší se metoda a obsahové kategorie, ne anglická slova.
- **Russell a kol.: StoryScope.** arXiv 2604.03136. 61 608 povídek, beletrie, jazyk pravděpodobně angličtina. Opora jen pro strukturu vyprávění (oddíl Vyprávění), ne pro pracovní texty. Dvě zjištění sedí s českými dimenzemi: AI drží jednu dějovou linii (srov. D4) a méně oslovuje čtenáře (srov. D5).

## Kalibrace skriptu

Prahy `scripts/metriky.py` omezují falešné poplachy na lidských textech z Universal Dependencies: UD Czech-CAC (věcné texty ze 70. a 80. let, licence CC BY-SA 4.0) a UD Czech-FicTree (beletrie, licence CC BY-NC-SA 4.0). Data do repozitáře nepatří. Kalibrační skript je v repozitáři v `tools/kalibrace/`. Citlivost na AI text prahy zatím neměří.
