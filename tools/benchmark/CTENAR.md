# Čtenářský test: návrh

Stav: návrh z 2026-11-16. **K1 splněno** (`vysledky/ctenar-k1`, `ctenar.py`, 3,72 USD včetně pilotu): Opus na 120 dev dvojicích AI originálu správně určil lidský úryvek v 95 % [90 %; 98 %], ve všech vrstvách, metodách i u všech tří generujících modelů nad 89 %. Rozporná pořadí 7 ze 120. Podle zdůvodnění čtenář pozná AI úryvek podle uhlazenosti a obecnosti, šablon („nejsou pouhými…, ale“) a ozdobných metafor, lidský podle konkrétních údajů, neobratné skladby, překlepů a dobové češtiny. **K2 nesplněno** (2026-11-17, `vysledky/ctenar-k2`): uživatel (autor skillu) na 30 dvojicích z K1 určil lidský úryvek ve 14 z 30 (47 %, test proti náhodě p = 0,71), u odpovědí „jsem si jistý“ ve 3 z 11, u tipů v 11 z 19; shoda s modelem 42 %, model měl na týchž dvojicích 92 %. Na úryvcích o 2–3 větách člověk AI nepozná a model za čtenáře zastupovat nemůže. U jistých odpovědí uživatel spíš označoval za lidský hladký AI úryvek; lidské texty vrstev klasika, wiki a úřední (dobová čeština, kostrbatá Wikipedie, tiskové zprávy) mu připadaly strojové. Měření přepisů v této podobě se nespouští. Rozhodovací pravidlo v PLAN.md se tímto souborem nemění. Kdyby se čtenářský test měl stát jeho součástí, zapíše se to do Historie plánu před během na test sadě.

## Proč

Cílem unslop-cs je, aby čtenář nepoznal text jako psaný AI. Benchmark to dosud neměřil:

- Skóre AI-ovosti (F0) se po přepisu nehne u žádného skillu (−0,019 až +0,009 v `test-2`), i když ostatní skilly přepíšou 20 % AI textu. Měří funkční slova, slovní druhy a délku vět, tedy záměrně ne to, co skilly mění.
- Soudce A/B v kalibraci neprošel (shoda 53 %). Volil mezi dvěma přepisy podle vkusu, ne podle známé odpovědi.

Bod 3 rozhodovacího pravidla proto nemůže splnit žádný skill a každé srovnání skončí cenou.

Čtenářský test se ptá přímo: poznám, který ze dvou krátkých úryvků napsal člověk? Správnou odpověď zná původ textu.

## Úryvky: 2 až 3 věty

Úryvek tvoří 2 nebo 3 celé věty v rozsahu 20–60 slov. Když mají tři věty přes 60 slov, berou se dvě; když i dvě, okno se vynechá. Délky obou úryvků ve dvojici se smí lišit nejvýš 1,5×. Okna s markdownem (nadpis, odrážka, tučné) a okna, která tvoří jen přímá řeč, se vynechávají. Typografie zůstává, jak je, protože ji čtenář vidí a skilly ji opravují.

Co krátký úryvek ukáže: frázi, kalk, nafouknuté slovo, aforistickou pointu uprostřed textu, rytmus vět, hraný tón.

Co neukáže: vzorce stavby celého textu (šablonovitý úvod a závěr, stejně stavěné odstavce, zopakovaná pointa, ohlášená osnova). Test proto podceňuje skilly, které opravují stavbu, a nadceňuje ty, které mění slova. Na tyto vzorce se unslop-cs zaměřuje hodně; když vyjde test dobře pro ostatní a špatně pro unslop-cs, je třeba tohle omezení zvážit. Kontrola na delších úsecích (jeden odstavec) je možná později jako samostatný krok.

## Dvojice

Jen rozhodovací vrstvy (klasika, wiki, úřední) a jen AI texty s lidským párem.

- **Pokračování:** model i autor navazují na stejný začátek (~100 slov). Úryvek je první okno za koncem začátku, u lidského i AI textu. Obě strany jsou uprostřed textu na stejném místě, takže se liší jen autor.
- **Chatbot:** stejné téma, jiný text. Úryvek je okno od věty nejblíž 40 % délky textu, u obou stran. Začátky a konce se neberou: lidský úsek je vyříznutý z delšího díla, takže jeho začátek a konec jsou náhodné řezy, kdežto AI text má skutečný úvod a závěr. Test by pak měřil řez, ne styl.

Pozice oken se určí z originálů před pohledem na přepisy a jsou stejné pro všechny podmínky.

## Podmínky

Ke každé dvojici čte čtenář lidský úryvek a jednu z verzí AI úryvku:

1. AI originál,
2. přepis unslop-cs (1.6.1),
3. přepis unslop-cs-jadro-2,
4. přepis anti-ai-slop-cz,
5. přepis humanizer-czech,
6. přepis bez skillu.

Přepisy se znovu nespouští, berou se z uložených běhů (`DATA/behy/<stitek>/behy.jsonl`, pole `finalni_text`). Úryvek přepisu je úsek, který odpovídá větám okna v originálu (zarovnání vět přes difflib jako v `scripts/diff.py`). Když skill větu smazal nebo sloučil, úryvek je kratší nebo delší; když skill okno nezměnil, je shodný s originálem. Podíl nezměněných oken se vykazuje u každého skillu, protože vysvětluje velkou část rozdílů.

## Čtenář: model

`claude-opus-5-5` přes `claude -p`, bez nástrojů a bez pluginů, jedna dvojice na volání, aby si čtenář nevytvářel měřítko z předchozích dvojic. Zadání:

> Jeden z úryvků napsal člověk, druhý jazykový model. Který napsal člověk? Odpověz JSON: {"clovek": "A" nebo "B", "jistota": 1–3, "proc": "nejvýš 15 slov"}.

Každá dvojice běží dvakrát s prohozeným pořadím. Shodná odpověď počítá 1 nebo 0, rozporná 0,5. Pole `proc` slouží jen k rozboru: ukáže, podle čeho čtenář AI pozná.

## Čtenář: člověk

Uživatel naslepo na 30 dvojicích AI originálu z dev sady (náhodný výběr ze stejných dvojic, jaké čte model). Úryvky jsou krátké, takže to zabere asi 20 minut. Formát: buď soukromá stránka s tlačítky A/B (jde i z telefonu), nebo soubor v `~/unslop-cs-data/benchmark/ctenar/`, kam se píše A nebo B. Klíč leží zvlášť a uživatel ho před vyplněním nevidí. Dvojice jsou jen z dev sady, nikdy z test sady.

## Kalibrace (dev, před vším ostatním)

1. **Pilot:** 10 dvojic, obě pořadí. Ověří formát odpovědi, ceny a vyřazování oken.
2. **K1, model pozná originál:** asi 120 dvojic AI originálu z dev pokračování a chatbotů (bez přepisů, tedy i texty mimo výběr `dev-2`). Úspěšnost aspoň 70 %, dolní mez 95% intervalu aspoň 60 %. Když neprojde, dvě až tři věty modelu nestačí: buď jedno další kolo se 4–5 větami, nebo konec.
3. **K2, model čte jako člověk:** shoda modelu s uživatelem na jeho 30 dvojicích aspoň 70 %. Vykazuje se i úspěšnost uživatele samotného. Když uživatel pozná originál jen náhodou (kolem 50 %) a model výrazně líp, model si všímá něčeho, co čtenář nevidí, a za čtenáře zastupovat nemůže.

Test pokračuje jen při splnění K1 i K2.

## Míry

- **Poznatelnost** p: podíl dvojic, ve kterých čtenář správně určí lidský úryvek.
- **Účinek skillu** Δ = p(originál) − p(přepis) na stejných oknech. Kladné Δ znamená, že přepis AI úryvek skryl.
- Rozdíl dvou skillů: Δ(A) − Δ(B) = p(B) − p(A).
- Interval: bootstrap 95 %, převzorkování po shlucích podle zdrojového lidského textu, stejně jako v PLAN.md, krok 7.
- Zvlášť po vrstvách, po metodě (pokračování, chatbot) a po generujícím modelu; podíl nezměněných oken; rozpornost odpovědí při prohození pořadí.

## Návrh do rozhodovacího pravidla (jen po schválení)

V bodu 3 přibude třetí možnost: A přinese zlepšení, když interval p(B) − p(A) leží celý nad nulou, jen při splnění K1 a K2. Podle zásady 5 v PLAN.md se změna zapíše do Historie plánu s datem a důvodem a dřívější verdikty z test sady se pak nepoužijí. Test sada se tím použije počtvrté, ale na uložené výstupy a jako potvrzení: kritéria budou zapsaná předem a podle výsledku se pravidla skillu ladit nebudou.

## Rizika

- **Paměť modelu:** Opus mohl klasiku nebo Wikipedii vidět a lidský úryvek poznat podle obsahu, ne podle stylu. Filtr kontaminace ukázal nejdelší shodu 11 slov, takže to není pravděpodobné, ale vrstva úřední (tiskové zprávy ČSÚ) slouží jako kontrola a vykazuje se zvlášť.
- **Málo dvojic:** dev má 40 AI textů s přepisy, intervaly budou široké. Dev výsledek je orientační, rozhoduje test sada (66 AI textů).
- **Verze v dev:** `dev-2` měří 1.6.1 před úpravou po evalech (otisk `72bb07be240f`), konečnou verzi měří až `test-2`.
- **Čtenář je Claude a AI texty psal Claude:** model může mít slepá místa pro vlastní styl. Proto K2.
- **Krátký úryvek nevidí stavbu** (viz výše).

## Cena a pořadí

| krok | volání | odhad |
|---|---|---|
| pilot | 20 | do 1 USD |
| K1 | asi 240 | asi 5 USD |
| K2 | 0 (čte uživatel) | 0 |
| dev, 6 podmínek | 40 oken × 6 × 2 = 480 | asi 10 USD |
| test, 6 podmínek | 66 oken × 6 × 2 = 792 | asi 16 USD |

Odhad počítá s 0,02 USD na volání; pilot ukáže skutečnou cenu. Před každým placeným krokem se uživatel zeptá.

Kód: nový `tools/benchmark/ctenar.py` (okna, dvojice, volání čtenáře přes `cli.zavolej`, export a vyhodnocení listu pro uživatele), statistika z `statistika.py`. Texty a odpovědi v `DATA/ctenar/<stitek>/`, souhrny v `vysledky/<stitek>/`.
