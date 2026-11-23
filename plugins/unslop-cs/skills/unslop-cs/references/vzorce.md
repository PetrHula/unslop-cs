# Pravidla a vzorce: před a po

Podrobná pravidla úrovní 1–3 a registrů. U každého vzorce je pravidlo, příklad PŘED a PO a podobný případ, který zůstává (PONECHAT). Jádro skillu, režimy, závažnost, pojistky a sebekontrola jsou v `../SKILL.md`, seznamy slov s prahy a typografie v `slova.md`, opora pravidel v `zdroje.md`.

Obsah příkladů je vymyšlený. Skutečná místa a instituce slouží jen jako kulisa a tvrzení o nich nejsou skutečná. Každá verze PO obsahuje jen informace z verze PŘED; co chybí, označuje značka `[OVĚŘIT: …]`. U vzorců, které stojí na měření, je opora v `zdroje.md`; čísla „AI / lidé“ jsou z porovnání AI-Koditexu s lidskými texty (D3 až D8 jsou dimenze stylu češtiny podle Cvrčka a kol.).

## Obsah

- **Úroveň 1: slova a typografie** – nafouknutý slovník a význam, reklamní jazyk, kalky a falešní přátelé, chatbotí artefakty, typografie a mikroformáty
- **Úroveň 2: věta a rytmus** – rytmus a řetěz krátkých vět, kontrastní obrat, trojice, přívěsky s „což“ a „čímž“, opisy pro „je“ a „má“, vrstvené jištění, synonymní kolotoč, falešné agens, dvojtečkové odhalení a otázka s odpovědí, inscenovaný důraz, heslovitá kadence, opakovaný obrat, tautologická zdvojení
- **Česká skladba** – nová informace na konec, příklonky, nadbytečná zájmena, ukazovací zájmena jako rituál, slovesa a aktér, slovo, které bys řekl nahlas, jedna myšlenka na větu, hustá síť odkazů
- **Úroveň 3: obsah** – relevance, čtenářova další otázka, pojmenované místo vágních odkazů, test přenositelnosti, výhled místo výsledku
- **Úroveň 3: stavba** – pointa jednou, stejně stavěné odstavce, nadpisy, šablonovité úvody a závěry, falešné prozření a mravoučná pointa, okřídlené metafory o AI, meta-komentář a text o sobě, ohlášení, rekapitulace a šablonovitá vyváženost, fantomové námitky, počítané seznamy, odpověď, která staví kontext znovu, formát podle obsahu
- **Úroveň 3: vyprávění** – příběhy, historky, případové studie, emoce
- **Registry** – registr prezentací, odborný text
- **Pojistky v příkladech** – význam ve stejné síle, postoj a konkrétnost, oprava bez nových chyb
- **Výčty tvarů podle závažnosti** – úplné výčty P1 a P2

## Úroveň 1: slova a typografie

Nejslabší, ale nejviditelnější signál. Seznamy slov, kalků, ustálených frází a typografických konvencí s prahy jsou ve `slova.md`.

### Nafouknutý slovník a nafouknutý význam

*klíčový, fascinující, udržitelný, inovativní, komplexní, aspekt, výzva, posunout na další úroveň, hrát klíčovou roli, nedílná součást.* Podle úrovně ve `slova.md` je nahraď, nebo je označ až ve shluku. Úrovně vycházejí z porovnání českých AI a lidských textů (AI-Koditex); zesilovače jako „velmi“, „zcela“, „opravdu“ AI v češtině nepřehání a samy nález nejsou.

- PŘED: „Otevření nové pobočky knihovny v Líšni představuje významný milník, který otevírá nové obzory pro celou komunitu.“
- PO: „V Líšni se otevřela nová pobočka knihovny.“ `[OVĚŘIT: co pobočka obyvatelům přináší]`
- PONECHAT: „Zákon poprvé zavedl povinné pojištění odpovědnosti.“ Věta tvrdí ověřitelnou změnu.

Test: když po smazání věty o významu zbude věta, která pořád funguje, byla to vata.

### Reklamní jazyk

- PŘED: „Naše revoluční platforma přináší komplexní řešení s unikátní přidanou hodnotou.“
- PO: Bez podloženého přepisu. `[OVĚŘIT: co platforma dělá, pro koho a v čem se liší od konkurence]`
- PONECHAT (sociální sítě, trocha prodeje je v pořádku): „Nová kolekce je venku. Mrkněte do e-shopu.“

### Kalky a falešní přátelé

*adresovat problém, na denní bázi, na konci dne, realizovat si (= uvědomit si), eventuálně (= nakonec).* Falešný přítel, který mění význam, a celá kalkovaná fráze, která česky zní cize („doufám, že vás e-mail zastihne v pořádku“), jsou P1, ostatní kalky P2. V pokračováních českých textů z AI-Koditexu se kalky jako signál AI nepotvrdily; hlídej je hlavně v odpovědích chatbota a v marketingu, kde model překládá z angličtiny.

- PŘED: „Musíme adresovat tento problém na týdenní bázi.“ → PO: „Musíme tento problém řešit každý týden.“
- PŘED: „Až později jsem si realizoval, že server běží na starém disku.“ → PO: „Až později jsem si uvědomil, že server běží na starém disku.“
- PŘED: „Dlouho jsme váhali, ale eventuálně jsme systém vyměnili.“ → PO: „Dlouho jsme váhali, ale nakonec jsme systém vyměnili.“

**Termíny** jdou opačným směrem: model zavedený termín přeloží tak, že se změní význam, nebo si český termín vymyslí. Obojí je P1. Když nevíš jistě, jestli výraz čeština používá, dej `[OVĚŘIT: používá se „…“?]` a nech původní termín.

- PŘED: „Úvodní stránka jarní kampaně měla míru okamžitého opuštění 71 %.“ → PO: „Vstupní stránka (landing page) jarní kampaně měla míru okamžitého opuštění 71 %.“ (překlad, který mění význam: úvodní stránka je homepage; skutečný výstup modelu při překladu)
- PŘED: „Každý zákazník dostal AI zástupce, který odpovídá na dotazy k fakturám.“ → PO: „Každý zákazník dostal AI agenta, který odpovídá na dotazy k fakturám.“ (překlad, který mění význam: zástupce jedná za někoho, agent plní úkoly)
- PŘED: „Robot našel na webu 40 mrtvých adres.“ → PO: „Robot našel na webu 40 nefunkčních odkazů.“ (vymyšlený termín)
- PONECHAT: „Pošli mi feedback do pátku.“, „Agent dostal vlastní prompt.“ (přejaté slovo a oborový termín), „Deník schoval články za platební zeď.“ (česká podoba, kterou píše i lidská publicistika, třeba Lupa.cz)
- PONECHAT: „Projekt se podařilo realizovat do konce roku.“ (realizovat = uskutečnit), „Pošlete fotku, eventuálně sken.“ (eventuálně = případně), „Ta věta nedává smysl.“, „Sdílím váš názor.“

### Chatbotí artefakty

Seznam je ve `slova.md` (P0).

- PŘED: „Skvělá otázka! Rád vám připravím přehled. Zde je seznam postupů. Doufám, že vám to pomůže!“
- PO: jen samotný přehled.
- PONECHAT: „Dobrý den, posílám smlouvu k podpisu. S pozdravem Jana Malá“ Běžné e-mailové oslovení a rozloučení nejsou chatbotí artefakty.

### Typografie a mikroformáty

Pravidla (pomlčka a rozpočet pomlček, uvozovky, desetinná čárka, řády, procenta, měna, datum, čas, nadpisy, tykání a vykání) jsou v tabulce ve `slova.md`. Typografie je norma: chyba bez ohledu na to, kdo text psal. Dlouhá pomlčka jako signál AI v češtině změřená není, v praxi ale k nejviditelnějším patří.

- PŘED: „Nová funkce—dlouho očekávaná—je konečně tady.“ → PO: „Nová funkce je konečně tady. Čekalo se na ni dlouho.“ V textu k publikaci, kde jinak pomlčky nejsou, projde i „Nová funkce – dlouho očekávaná – je konečně tady.“
- PŘED: „Sleva 25% platí do 5/4/2026.“ → PO: „Sleva 25 % platí do `[OVĚŘIT: 4. 5. 2026, nebo 5. 4. 2026?]`.“
- PŘED (e-shop): „Všechny ceny jsou uvedeny v CZK.“ → PO: „Všechny ceny jsou uvedeny v Kč.“ CZK je bankovní kód měny; v běžném textu o částkách se píše „Kč“ (P2).
- PŘED: „Strategické Priority Pro Rok 2027“ → PO: „Strategické priority pro rok 2027“ (anglický title case, P1)
- PŘED: „Vyplňte formulář a odešlete ho. Pak ti přijde potvrzení.“ → PO: „Vyplňte formulář a odešlete ho. Pak vám přijde potvrzení.“ (sjednoceno podle převažující formy; když žádná nepřevažuje, zeptej se)
- PONECHAT: „25% sleva na všechno“ (přídavné jméno), „Ahoj, posílám to - kdyžtak napiš“ (spojovník v chatu), „Částka 12 500 CZK bude odepsána z účtu CZ65 0800 …“ (bankovní kontext, kód měny je tu na místě).

## Úroveň 2: věta a rytmus

### Rytmus a řetěz krátkých vět

**Rytmus.** Hledej tři po sobě jdoucí věty podobné délky a stejné stavby. Délka sama je jen indicie. Česká AI píše spíš delší souvětí než lidé, ne útržky (orientační měření); v souvislém textu proto hlídej hlavně dlouhá souvětí s řetězem „který“ (Hustá síť odkazů). Míchej krátké věty (3–8 slov) s dlouhými (25 a víc), kde to obsah dovolí. Nikdy nenatahuj ani nesekej čistou pasáž kvůli kvótě.

**Past řetězu krátkých vět.** Řada krátkých hlavních vět („Krátká věta. Další. A ještě jedna.“) je sama AI tik. Spojuj myšlenky spojkami, vedlejšími větami, středníkem nebo dvojtečkou, aby příčina a protiklad žily ve skladbě. Jeden záměrný útržek je v pořádku, tři stejné za sebou už tvoří vzorec (P2). Jednoslovné věty pro drama („Brutální.“ „Tečka.“) patří sem.

- PŘED: „Tým chtěl rychlejší výsledky. Nasadil nový nástroj. Práce se zrychlila. Všichni byli spokojení.“
- PO: „Tým chtěl rychlejší výsledky, a tak nasadil nový nástroj. Práce se zrychlila a všichni byli spokojení.“ `[OVĚŘIT: o kolik se práce zrychlila]`
- PŘED: čtyři věty po osmnácti slovech, každá ve tvaru podmět – přísudek – předmět.
- PO: dvě souvisící věty spoj do souvětí, jednu nech krátkou. Obsah beze změny.
- PONECHAT: „Hotovo. Teď můžeš soubor zavřít.“ Jeden záměrný útržek.

### Kontrastní obrat

„Nejde o X, jde o Y“, „Není to X, je to Y“, „nejen X, ale i Y“ jako řečnická figura, také rozdělené do dvou vět, s nahromaděnými zápory před odhalením („Nejde o nástroje. Nejde o procesy. Jde o lidi.“) a ve zkrácené podobě „A místo B“ („Dialog místo přednášky“). Jako řečnická figura je nálezem P1 i jednou za text. Obvykle stačí kladná věta, protože alternativu vylučuje sama. Zůstávají tři podobné případy: pokyn, který opravuje, opravené číslo a tvrzení o pravosti.

- PŘED: „Nejde o software. Nejde o procesy. Jde o lidi.“
- PO: Bez podloženého přepisu. `[OVĚŘIT: co konkrétně se má u lidí změnit]`
- PŘED: „Kurz není jen o vaření, ale i o společné večeři, při které účastníci snědí, co uvařili.“
- PO: „Na konci kurzu účastníci společně snědí, co uvařili.“
- PŘED (slajd, kde nikdo přednášku nenavrhoval): „Workshop místo přednášky“
- PO: „Formát: workshop“
- PONECHAT: „Pošli fakturu za březen, ne za duben.“ (pokyn, který opravuje), „Tržby klesly o 12 %, ne o 21 %.“ (opravené číslo), „Fotka je skutečná, ne montáž.“ (tvrzení o pravosti)

### Trojice

„Rychle, levně a spolehlivě“: AI tlačí všechno do skupin po třech. Vezmi dvě, čtyři, nebo napiš celou větu. Nejvýš jedna trojice přídavných jmen na text. Trojice se slovem z úrovně 1 nebo 2 („praktický, flexibilní a udržitelný“) je P1 hned, druhá trojice přídavných jmen v textu také; ostatní P2. Vzorec roste i do větších celků: odstavec ze tří stejných příkladů nebo ze tří krátkých tvrzení s mravním naučením na konci. Trojice zůstává jen tam, kde má obsah tři části.

- PŘED: „Naše pekárna je tradiční, poctivá a lokální: mouku bereme ze mlýna v Kostelci.“
- PO: „Mouku bereme ze mlýna v Kostelci.“
- PŘED: odstavec ze tří stejně stavěných příkladů zakončený větou „Všechny tři ukazují, jak důležitá je komunikace.“
- PO: příklady ponech, zobecnění na konci škrtni.
- PONECHAT: „Formulář chce jméno, e-mail a číslo smlouvy.“ Obsah má tři části.

### Přívěsky s „což“ a „čímž“

„…, což podtrhuje význam…“, „…, čímž přispívá k…“, „…, a tím zajišťuje…“ jsou českou obdobou anglických -ing přívěsků. Předstírají hloubku. Česká AI je píše zhruba dvakrát častěji než lidé (AI-Koditex). Škrtni je, nebo z nich udělej samostatnou větu s doloženým faktem. Přívěsek, který nese skutečný důsledek, zůstává.

- PŘED: „Obec opravila chodník u školy, což podtrhuje její zájem o bezpečnost dětí.“
- PO: „Obec opravila chodník u školy.“
- PŘED: „Aplikace ukládá data jen v telefonu, čímž zajišťuje maximální soukromí uživatelů.“
- PO: „Aplikace ukládá data jen v telefonu.“
- PONECHAT: „Uzávěrka se posunula na pátek, což znamená, že výplaty odejdou v pondělí.“ Přívěsek nese skutečný důsledek.

### Opisy pro „je“ a „má“

„představuje“, „slouží jako“, „funguje jako“, „disponuje“, „pyšní se“, „nabízí“ ve smyslu „má“. Opis škrtni, nebo řekni, co věc dělá. „Je“ napiš jen tam, kde jde o totožnost nebo zařazení; česká AI píše jmenných přísudků s „je“ víc než lidé, takže prostá výměna opisu za „je“ tik nezruší (D3, D7). Samo o sobě P2; nafouknutá ustálená fráze v téže větě může zvlášť zasloužit P1.

- PŘED: „Hrad Kunětická hora představuje oblíbený cíl výletů a disponuje vyhlídkovou věží.“
- PO: „Na hrad Kunětická hora jezdí výletníci rádi, má vyhlídkovou věž.“
- PŘED: „Nová aplikace představuje nástroj pro správu výdajů.“
- PO: „Nová aplikace hlídá výdaje.“ `[OVĚŘIT: jaké výdaje a jak]`
- PONECHAT: „Zastupitelstvo představilo návrh rozpočtu.“ (představit = ukázat veřejnosti), „Tabulka slouží k evidenci výpůjček.“ (skutečný účel)

### Vrstvené jištění

„Mohlo by potenciálně“, „by se dalo říci, že možná“: dvě a víc jištění v jednom tvrzení. Nech jedno. Jištění samo nález není: česká AI jistí méně než lidé („asi“, „snad“, „zřejmě“ píše třikrát až pětkrát méně), takže škrtání jednotlivých jištění text posouvá k AI (D8). Kalibrované jištění při skutečné nejistotě zůstává, v odborném a technickém registru je nutné.

- PŘED: „Tento přístup by mohl potenciálně v některých případech vést k určitému zlepšení.“
- PO: „Tento přístup může v některých případech vést ke zlepšení.“ `[OVĚŘIT: v jakých případech a o kolik]`
- PONECHAT (zdravotnický text): „Lék může u některých pacientů způsobit závratě.“ Jištění je obsah.
- PONECHAT: „Asi to do pátku nestihneme, chybí nám podklady od dodavatele.“ Jedno jištění v tvrzení je lidský postoj.

### Synonymní kolotoč

„Společnost… firma… podnik… korporace“ pro tutéž věc v jednom odstavci. Platí pro termíny a pojmenování téže entity v odborném a technickém textu: tam vyber jeden výraz a drž ho; zájmeno nebo vynechání podmětu je v pořádku. Patří sem i termín střídaný s vlastním překladem („prompt… výzva… zadání“). Jinde jen ve shluku s dalšími tiky. Česká AI má slovník spíš chudší než lidé (D4), pestrost slov proto plošně nesnižuj.

### Falešné agens

„Čísla mluví sama za sebe“, „data vyprávějí příběh“, „nástroj rozhoduje“. Řekni, co číslo ukazuje, nebo pojmenuj mechanismus. Běžná technická slovesa zůstávají.

- PŘED: „Návštěvnost vzrostla z 1 200 na 1 900 měsíčně. Čísla mluví sama za sebe.“ → PO: „Návštěvnost vzrostla z 1 200 na 1 900 měsíčně.“
- PONECHAT: „Parser přečte soubor a test selže, když chybí hlavička.“

### Dvojtečkové odhalení a otázka s odpovědí

„Nejlepší na tom: učí se.“, „Výsledek? Rychlejší práce.“, „Největší problém? Lidi.“ Dvojtečka nebo otazník tu inscenují pauzu místo spojení dvou myšlenek. Přepiš na obyčejnou větu jen z toho, co zdroj tvrdí. Dvojtečka před výčtem, citací nebo věcně uvedeným důsledkem zůstává. Skutečná otázka na čtenáře zůstává vždy: česká AI se ptá zhruba o polovinu méně než lidé (D5), mazat se má jen inscenovaná pauza.

- PŘED: „Nejlepší na tom: funguje i offline.“ → PO: „Funguje i offline.“
- PŘED: „Výsledek? Rychlejší práce.“ → PO: „Práce se zrychlila.“ `[OVĚŘIT: o kolik]`
- PONECHAT: „Potřebujete: občanský průkaz, výpis z účtu, plnou moc.“ (dvojtečka před výčtem), „Kdy přesně termín vyprší? Ve smlouvě je 30. června.“ (skutečná otázka, kterou si čtenář klade)

### Inscenovaný důraz

Slova velkými písmeny nebo rozsekaná tečkami („KAŽDÝ. JEDNOTLIVÝ. DEN.“) a pokyn k pauze („Přečtěte si to znovu.“, „Nechte to chvíli uležet.“). Škrtni, nebo tam dej fakt, který by váhu unesl.

### Heslovitá kadence

Dvoutaktové heslo („Méně papírování. Víc času.“), číselná dvojice („Jeden účet, tři pobočky.“) a nadpis ze dvou útržků („Jeden klik. Hotovo.“). Jedno takové místo je hlas autora, od tří v jednom textu jde o šablonu. Spoj je do normální věty, nebo obměň tvar. Na slajdech a v odrážkách platí registr prezentací.

- PŘED: „Méně klikání. Víc prodeje. Jeden účet, tři systémy.“ → PO: „S jedním účtem se přihlásíte do všech tří systémů, takže méně klikáte a víc prodáte.“ `[OVĚŘIT: o kolik méně klikání a víc prodeje]`
- PONECHAT: jedno heslo v textu („Méně papírování.“ jako podnadpis) je hlas autora.

### Opakovaný obrat

Tatáž víceslovná figura se stejnou rétorickou funkcí vrací v textu znovu a znovu: třikrát „jako by“, opakované „A právě tady…“, „Nejde jen o…“, „To není náhoda.“. Je to vzorec: P2 od tří výskytů, P1 ve shluku s dalšími tiky. Obměň tvar, nebo nech jen jeden výskyt.

Opakované jedno slovo vzorec není, ani když jde o spojku nebo částici („přitom“, „také“, „ale“, „totiž“). Patří do tabulky Jiné vady jako stylistická poznámka, ne mezi nálezy. Pojistka o částicích platí dál: navrhni obměnu nebo škrt jen tam, kde slovo nic nenese, a zbytek nech.

- PŘED: „Město vypadalo, jako by spalo. Tržnice stála, jako by ji někdo opustil. Řeka tekla, jako by spěchala pryč.“ → PO: „Město spalo. Tržnice stála prázdná a řeka tekla rychle.“
- PONECHAT (Jiné vady): „Knihovna přitom otevírá v sedm… Výpůjčka je přitom zdarma… Přitom má jen dva zaměstnance.“ Opakované „přitom“ je slovo, ne figura; v tabulce Jiné vady stačí „přitom 3×, obměnit“.

### Tautologická zdvojení

„různé a rozmanité“, „efektivní a účinný“, „jasný a srozumitelný“, „důležitý a zásadní“. Nech jedno slovo.

## Česká skladba

Odstranit tiky je jen polovina druhé úrovně. Druhá polovina je, jak se věta staví. Dobře postavená věta začíná aktérem a slovesem a česká AI navíc často prosvítá anglickou kostrou.

Pojistky platí i tady: měníš stavbu, nikdy obsah. Žádná nová fakta, žádná vnucená osobnost. Pravidla platí pro souvislý text; prezentace část z nich obracejí, tam je střídmý jmenný styl profesionální hlas (Registr prezentací).

### Nová informace na konec (aktuální členění)

V češtině nese důraz konec věty. Anglický slovosled s podmětem vždy na začátku zní jako překlad.

- PŘED: „Nová verze aplikace vyřešila tento problém.“ (novinkou je, co problém vyřešilo)
- PO: „Tento problém vyřešila nová verze aplikace.“

### Příklonky za prvním větným členem

*se, si, jsem, bych, mi, ho* stojí hned za prvním větným členem, ve vedlejší větě za spojkou nebo vztažným slovem.

- PŘED: „Tuto smlouvu podepsal jsem včera.“ → PO: „Tuto smlouvu jsem podepsal včera.“

### Nadbytečná zájmena

Vynechávej zájmena, která čeština nepotřebuje: podmětová zájmena bez důrazu („Já jsem šel…“, „On řekl…“) a přivlastňovací tam, kde je vlastník jasný („Otevřel své oči“ → „Otevřel oči“). Obojí je anglický otisk a nadbytečné „svůj“ k němu patří nejčastěji. Nadbytečné přivlastňovací zájmeno je podle ÚJČ chyba; „svůj“ píše česká AI o pětinu častěji než lidé. Nadbytečná podmětová zájmena data neprokázala, zůstávají jako slabý signál.

- PŘED: „Petr vzal svůj telefon ze svého stolu a on zkontroloval své zprávy.“
- PO: „Petr vzal telefon ze stolu a zkontroloval zprávy.“
- PONECHAT: „Vezmi si svůj, tenhle je můj.“ Zájmeno rozlišuje vlastníka. „Já to podepíšu, ty ne.“ Podmětové zájmeno nese důraz.

### Ukazovací zájmena jako rituál

Řada vět, které začínají „Tento problém… Tato situace… Tyto faktory…“, je úřednický zvyk, který AI přehání. Je to nejpevnější větný signál z českých dat: AI začíná ukazovacím zájmenem čtyřikrát častěji než lidé, a to u všech 25 měřených modelů; podobně „Každý…“ a „Některé…“ na začátku věty. Ukazovací zájmeno patří tam, kde na něco skutečně ukazuje. Neurčité „jeden“ („jeden kolega mi říkal“) je taky běžné; signálem je až šablonovitý začátek historky bez jména a detailu (Vyprávění).

- PŘED: „Tento problém se týká mnoha firem. Tato situace vyžaduje rychlé řešení. Tyto faktory je třeba zvážit.“
- PO: „Problém se týká mnoha firem a vyžaduje rychlé řešení.“ `[OVĚŘIT: které faktory]`
- PONECHAT: „Ten server, co jsme minulý týden restartovali, zase spadl.“ Zájmeno ukazuje na známou věc. „Jeden kolega mi říkal, že…“ je běžná čeština.

### Slovesa a aktér

**Slovesa místo podstatných jmen.** „Došlo k realizaci implementace“ → „Nasadili jsme“. Každé „provedení“, „zajištění“, „realizace“, „dochází k“, „v rámci provádění“ schovává sloveso, které věta chtěla.

**Pojmenuj aktéra.** Opisné pasivum („bylo rozhodnuto“, „je prováděn“) skrývá, kdo co dělá. Pojmenuj ho, když ho zdroj zná. Zvratné pasivum („kontroluje se“, „platí se předem“) je v češtině přirozené a samo o sobě nález není. Jedno opisné pasivum je taky slabé samo o sobě.

**Sloveso musí pojmenovat skutečnou operaci.** Když je aktér pojmenovaný, sloveso má říct, co se s předmětem děje: čte, třídí, posílá, kontroluje, maže. Metafora na místě slovesa („nese“, „táhne“, „stojí na“) zruší práci, kterou udělal pojmenovaný aktér.

- PŘED: „V rámci realizace projektu došlo k provedení migrace dat ze strany externího dodavatele.“
- PO: „Externí dodavatel v projektu přenesl data.“
- PŘED: „Bylo rozhodnuto, že bude připraven nový postup.“
- PO: `[OVĚŘIT: kdo rozhodl a kdo postup připraví]`
- PONECHAT: „Přihlášky se podávají do 30. června.“ (zvratné pasivum, aktér je jasný), „Pacient byl převezen na JIP.“ (aktér nehraje roli)

### Slovo, které bys řekl nahlas

„řešit“ místo „adresovat“, „zjistit“ místo „eruovat“, „mít“ místo „disponovat“, „použít“ místo „využít“ (když nejde o využití výhody, příležitosti nebo kapacity). Výjimkou jsou registry, kde je odborný výraz ten přesný (právo, medicína, bezpečnost).

### Jedna myšlenka na větu

Jedna vedlejší věta je výchozí stav. Řetězy „který“ a „přičemž“ působí jako generovaná vata. Rozděl větu a spojení nech nést logické slovo (protože, ale, proto), ne nahromaděné „kromě toho“ a „zároveň“.

### Hustá síť odkazů

Česká AI drží text pohromadě víc než lidé (D3): píše o polovinu víc „který“, skoro dvakrát víc „, což“, korelativ („to, co“; „tak, aby“; „ten, kdo“) a „svůj“ a začíná věty „Tento…“. Jeden takový prostředek je obyčejná čeština. Signálem je pasáž, kde se hromadí a každá věta se odkazuje na předchozí místo toho, aby řekla něco nového. Pojmenuj věc, na kterou zájmeno ukazuje, nebo větu rozděl. „Navíc“ a „Dále“ na začátku věty AI nepřehání; vadí až řetěz tří a víc.

- PŘED: „Firma zavedla nový systém evidence, který zrychlil schvalování faktur, což ocenili hlavně účetní, kteří dříve trávili hodiny tím, co nyní zvládnou za minuty. Tento systém zároveň umožnil, aby každý viděl, v jakém stavu jeho faktura je.“
- PO: „Firma zavedla nový systém evidence a schvalování faktur se zrychlilo. Účetní, kteří na něm dřív trávili hodiny, ho teď zvládnou za minuty. Každý navíc vidí, v jakém stavu je jeho faktura.“ `[OVĚŘIT: o kolik se schvalování zrychlilo]`
- PONECHAT: „Fakturu, kterou jste poslali v pátek, jsme zaplatili.“ Jedna vztažná věta s „který“ je obyčejná čeština.

## Úroveň 3: obsah

Relevance k zadání a hustota informace nejsilněji předpovídají, jestli čtenář text označí za slop; seznamy slov je nezachytí (Shaib a kol. 2025). Projdi je proto první.

### Relevance

Každý odstavec odpovídá na to, proč čtenář text čte. Odstavec, který vysvětluje obecné pozadí, opakuje zadání nebo rozebírá věc, na kterou se nikdo neptal, zkrať na větu, nebo škrtni.

### Odpověz na čtenářovu další otázku

Člověk po tvrzení napíše důsledek („Stojí o 400 Kč víc. Odpadne ale druhá návštěva.“), model zopakuje tvrzení jinými slovy. Když další věta nepřidává informaci, škrtni ji.

### Pojmenované místo vágních odkazů

„Jedna známá kniha o produktivitě“ → skutečný název. Odborníci dostanou jméno, „nedávno“ dostane datum. Vágní autorita („studie ukazují“, „odborníci se shodují“) buď dostane skutečný zdroj, nebo zmizí (P0, seznam ve `slova.md`). Totéž platí pro prestižní výčet („Psali o nás tři celostátní deníky a dva oborové weby“): ponech médium, které řeklo něco konkrétního, a co řeklo. Chybějící citace sama o sobě tik není, většina textů žádné nemá.

- PŘED: „Odborníci se shodují, že pravidelné zálohování je klíčové.“
- PO: „Zálohujte pravidelně.“ `[OVĚŘIT: kdo to doporučuje]`
- PŘED: „Studie ukazují, že lidé čtou na mobilu méně pozorně.“
- PO: `[OVĚŘIT: která studie, kdy, na jakém vzorku]` Číslo ani zdroj nevymýšlej.
- PŘED: „Jedna známá kniha o návycích tvrdí…“
- PO: `[OVĚŘIT: název a autor knihy]`
- PŘED: „Psali o nás Ranní listy, Týden v byznysu i Techportál. Ranní listy v březnu srovnávaly naše ceny s konkurencí.“
- PO: „Ranní listy v březnu srovnávaly naše ceny s konkurencí.“
- PONECHAT: „Podle Českého statistického úřadu…“ s konkrétním údajem. Běžný text bez citací, který žádnou autoritu nepředstírá.

### Test přenositelnosti

Přesuň větu beze změny do textu o jiné firmě, produktu nebo člověku. Když tam pořád sedí, byla to vata. Nahraď ji faktem, mechanismem, důsledkem nebo úsudkem, který platí jen tady, nebo ji škrtni. Je to nejrychlejší jednotlivý průchod hotovým textem a chytí, co seznamy slov minou.

### Výhled místo výsledku

Text, který má říct, co se stalo nebo co platí, sklouzne k tomu, co bude a co by mohlo být: „otevírá cestu k dalšímu rozvoji“, „má potenciál změnit“, „přináší nové příležitosti“, „v budoucnu bude hrát roli“. Česká AI píše slova výhledu (budoucnost, potenciál, rozvoj, perspektiva, příležitost, otevírat, umožňovat) dvaapůlkrát častěji než lidé a vazbu „je důležité, aby“ o dvě třetiny častěji (D7). Nahraď je tím, co se stalo, co platí teď, nebo konkrétním plánem s datem. Budoucí čas sám signálem není, AI ho píše méně než lidé. Výhled zůstává tam, kde ho text slibuje: plán, odhad, prognóza se zdrojem. P2, ve shluku se slovy z úrovně 2 P1.

- PŘED: „Nová cyklostezka mezi Hlubočepy a Barrandovem otevírá cestu k dalšímu rozvoji městské dopravy a má potenciál změnit, jak se lidé ve čtvrti pohybují.“
- PO: „Mezi Hlubočepy a Barrandovem vede nová cyklostezka.“ `[OVĚŘIT: od kdy a kolik lidí ji používá]`
- PŘED: „Je důležité, aby obec v budoucnu hledala nové příležitosti pro rozvoj cestovního ruchu.“
- PO: Bez podloženého přepisu. `[OVĚŘIT: co konkrétně má obec udělat a do kdy]`
- PONECHAT: „Stezka se má do konce roku 2027 prodloužit do Řeporyj, rozhodla o tom rada městské části.“ Plán s datem a zdrojem je informace.

## Úroveň 3: stavba

### Pointa jednou

Hlavní myšlenku řekni jednou, na místě s největším účinkem. Výjimkou jsou povinná shrnutí (perex, manažerské shrnutí). Neopakuj ji v každém oddílu a nepřidávej rituální odstavec „Co to znamená pro vás?“. Aspoň jeden příklad nech bez výkladu; čtenář umí myslet.

- PŘED: úvod říká „Pravidelný servis šetří peníze“, každý oddíl končí větou o úsporách a závěr totéž opakuje.
- PO: pointa jednou, na místě s největším účinkem; oddíly končí svým posledním faktem.
- PONECHAT: perex nebo manažerské shrnutí, které pointu opakuje z povahy formátu.

### Stejně stavěné odstavce

Když má každý odstavec tři až pět vět stejné délky, rozbij vzorec záměrně: jeden odstavec o jedné větě, jeden delší. Totéž platí pro oddíly, které všechny jedou podle schématu tvrzení, tři opory, mini-shrnutí.

### Nadpisy pojmenovávají obsah

Nahraď šablonu („Úvod / Přehled / Závěr / Klíčové poznatky“) a dramatizující titulky jmenným spojením, které obsah pojmenuje: „Vývoj tržeb 2024–2026“, „Rizika projektu“. Označ nadpis-upoutávku, která jen naznačuje („Co to pro nás znamená“, „Pohled na naše čísla“), hovorový větný nadpis („Co na školení bylo“ → „Obsah školení“), číselný nadpis z útržků („Jedna hodina. Tři úkoly.“) a nadpis, který pojmenovává akt prezentace místo obsahu („Představení výsledků“). Nadpisy v češtině mají velké jen první písmeno a vlastní jména; anglický title case je nález. V eseji a publicistice je větný titulek legitimní, když nese konkrétní tvrzení.

- PŘED (slajd): „Co nám prozradila zpětná vazba zákazníků“ → PO: „Zpětná vazba zákazníků“
- PŘED (slajd): „Pohled na naše čísla“ → PO: „Čísla“ `[OVĚŘIT: které ukazatele a za jaké období]`
- PŘED: „Jedna hodina. Tři úkoly.“ → PO: „Úkoly na jednu hodinu“
- PŘED: „Přizpůsobil lektor obsah?“ → PO: „Přizpůsobení obsahu“
- PŘED: „Představení výsledků průzkumu“ → PO: „Výsledky průzkumu“
- PŘED: „Co na školení bylo“ → PO: „Obsah školení“
- PŘED: „Koho jsme se ptali“ → PO: „Respondenti“
- PONECHAT (akční titulek s ověřitelným tvrzením): „Odchod zákazníků klesá od května o 2 body měsíčně“
- PONECHAT (titulek eseje): „Proč děti přestaly číst návody“. V publicistice je větný titulek legitimní, když slibuje konkrétní odpověď.

### Šablonovité úvody a závěry

Nezačínej širokoúhlým kontextem („V dnešní rychle se měnící době…“, „V éře umělé inteligence…“). Začni zprávou nebo tvrzením, kontext přijde potom. Žádný obecný konec („Budoucnost ukáže“, „Čeká nás zajímavá doba“). Česká AI skoro vždy končí rituálem „Závěrem lze konstatovat…“ nebo nadpisem „Závěr“ se shrnutím toho, co už zaznělo. Když text závěrečný oddíl potřebuje, musí přinést novou myšlenku: důsledek, rozhodnutí, další krok. Jinak ho škrtni a skonči o odstavec dřív.

- PŘED: „V dnešní rychle se měnící době je stále důležitější věnovat pozornost kybernetické bezpečnosti. Minulý týden útočníci zašifrovali data dvou obecních úřadů na Vysočině.“
- PO: „Minulý týden útočníci zašifrovali data dvou obecních úřadů na Vysočině.“
- PŘED (konec článku): „Závěrem lze konstatovat, že digitalizace přináší výzvy i příležitosti. Budoucnost ukáže.“
- PO: smazat a skončit posledním konkrétním odstavcem.
- PONECHAT: oddíl „Závěr“ v odborné práci, když přináší výsledek.

### Falešné prozření a mravoučná pointa

„Potvrdilo mi to jednu věc.“, „Otevřelo mi to oči.“, „Pravda je taková:“, „A právě tehdy mi došlo…“ předstírají aha moment, který se nestal. Závěrečná věta, která pointu povýší na metaforu nebo moudro („Technologie sama o sobě nestačí.“, „Všechno začíná u lidí.“, „Nástroje se mění, řemeslo zůstává.“), je totéž. Smaž ji a nevylepšuj: lepší metafora by v textu nechala stejný vzorec. Skonči nejkonkrétnější větou, kterou text už má.

- PŘED (poslední věta): „Technologie se mění, ale lidé zůstávají.“ → PO: smazat a skončit nejkonkrétnější větou, kterou text už má.
- PŘED: „Potvrdilo mi to jednu věc: AI není o technologii.“ → PO: `[OVĚŘIT: co konkrétně autor viděl]`, nebo celé smazat.
- PONECHAT: přímá citace, která moudro obsahuje a je přisouzená autorovi.

### Okřídlené metafory o AI

„AI je kopilot, ne autopilot“, „data jsou nová ropa“, „prompt je nový brief“. Tak ohrané, že samy prozradí strojový text. Popiš, co nástroj konkrétně dělá.

- PŘED: „AI je kopilot, ne autopilot: napíše první verzi, ale co v ní zůstane, rozhoduje člověk.“ → PO: „AI napíše první verzi, ale co v ní zůstane, rozhoduje člověk.“

### Meta-komentář a text o sobě

Věty, které vystoupí z tématu a říkají čtenáři, jak číst: „To je důležitější, než se zdá“, „Rozhodující je tohle:“, „Jak vidíte“, „Jinými slovy“ po větě, která už byla jasná. Sem patří i předstíraný vhled („Co většina lidí přehlíží“, „Co vám nikdo neřekne“) a text o sobě samém („V tomto článku se podíváme na…“, „Nyní se zaměříme na…“, „Jak jsme si ukázali výše…“, „Tabulka níže srovnává…“). Smaž, nebo na to místo dej chybějící fakt. Oslovení, které čtenáři šetří čas („Když spěcháte, stačí poslední odstavec.“), zůstává; česká AI oslovuje čtenáře méně než lidé (D5).

- PŘED: „To je důležitější, než se na první pohled zdá. Co většina lidí přehlíží: zálohy se musí i testovat.“
- PO: „Zálohy se musí i testovat.“
- PŘED: „Pro tento přehled jsme prošli weby všech dodavatelů a údaje převedli do tabulky. Tabulka níže je seřazena podle ceny.“
- PO: tabulku ponech; zdroj uveď jednou pod ní, když na něm záleží.
- PONECHAT: „Kdo potřebuje jen cenu, najde ji ve třetím odstavci.“ Jedno skutečné oslovení čtenáře, které mu šetří čas. Poznámky k vydání a changelog, kde popis změny je obsah.

### Ohlášení, rekapitulace a šablonovitá vyváženost

**Ohlášení a rekapitulace.** Úvod ohlásí osnovu, nadpisy ji zopakují a závěr zrekapituluje úvod. Čtenář dostane strukturu třikrát a obsah jednou. Škrtni ohlášení, nech nadpisy pojmenovat obsah, skonči posledním novým bodem.

**Šablonovitá vyváženost.** Ústupek, který nic neváží („I když je X slibné, Y zůstává výzvou“), a rámec „na jedné straně… na druhé straně… nakonec záleží na konkrétní situaci“ v textu, který čtenáři dluží závěr. Pojmenuj skutečný kompromis, nebo zaujmi stanovisko a obhaj ho. Recenze, posudky a přehledy literatury, které protinázory potřebují, jsou výjimka.

- PŘED: „Na jedné straně přináší home office flexibilitu, na druhé straně s sebou nese rizika. Nakonec záleží na konkrétní situaci.“
- PO: Bez podloženého přepisu. `[OVĚŘIT: jaká rizika a k jakému doporučení text směřuje]`
- PŘED: „V tomto článku se podíváme na tři oblasti…“ + nadpisy, které je opakují + závěr „Jak jsme si ukázali…“
- PO: ohlášení i rekapitulaci škrtni, nadpisy ponech.
- PONECHAT: recenze nebo posudek, kde je srovnání pro a proti účelem textu.

### Fantomové námitky

Text se brání tvrzení, které nikdo nevyslovil: „Tím nechci říct, že…“, „Nechápejte mě špatně“, „Aby bylo jasno“. Smaž obrannou polovinu a řekni, co se tvrdí. Námitka zůstává, když text uvede, kdo ji vznesl, nebo se s ní skutečně vypořádá.

- PŘED: „Tím nechci říct, že by tabulky byly špatné. Nechápejte mě špatně, Excel má své místo. Ale pro sdílenou evidenci je tabulka v e-mailu nevhodná, protože každý pak má jinou verzi.“
- PO: „Pro sdílenou evidenci je tabulka v e-mailu nevhodná, protože každý pak má jinou verzi.“
- PONECHAT: „Vedení namítlo, že přechod bude drahý. Licence stojí 40 000 Kč ročně, ale odpadne ruční přepisování.“ Námitku někdo vznesl a text s ní pracuje.

### Počítané seznamy pro efekt

„Tři klíčové poznatky“, „5 věcí, které musíte vědět“. Číslo tu o obsahu nic neříká. Počítej, jen když je počet informace.

### Odpověď, která staví kontext znovu

V odpovědi na e-mail nebo zprávu čtenář kontext zná. Když odpověď rekapituluje problém, prochází analýzu a rozhodnutí řekne až na konci, pointa se ztratí. Rozhodnutí patří na začátek. Ponech fakt, který čtenáři chybí, úvahu, která by změnila jeho souhlas, a odkaz, který potřebuje k akci.

- PŘED (odpověď v Teams): „Jak víš, minulý týden jsme řešili zpoždění dodávek. Prošel jsem 14 objednávek a 9 z nich přišlo pozdě, i když smlouva garantuje dva dny. Probral jsem to s logistikou a po zvážení všech možností jsem došel k závěru, že bychom měli změnit dopravce.“
- PO: „Navrhuju změnit dopravce. Ze 14 objednávek přišlo 9 pozdě, i když smlouva garantuje dva dny. S logistikou je to probrané.“
- PONECHAT: první e-mail adresátovi, který kontext nezná.

### Formát podle obsahu

Nadpis nad oddílem o dvou větách, odrážky, které rozsekají argument, emoji v nadpisech, seznamy s tučným štítkem a dvojtečkou, které jen opakují řádek („**Výkon:** Výkon se zlepšil…“), tučné písmo u každého pojmu. Odrážky si místo zaslouží, když jsou položky opravdu souběžné a čtenář je přelétne. Markdown nepatří do textu pro pole bez formátování (e-mail, příspěvek, SMS).

- PŘED:
  - **Rychlost:** Aplikace je rychlejší.
  - **Bezpečnost:** Přidali jsme šifrování.
- PO: „Aplikace je rychlejší a přidali jsme šifrování.“
- PONECHAT: „**Krok 1. Stáhněte si formulář.** Najdete ho na úřední desce obce.“ Štítek pojmenuje krok a za ním následuje nová informace.

## Úroveň 3: vyprávění (příběhy, historky, případové studie)

- **Škrtni dovětek s poučením.** „…a tehdy mi došlo, že nikdy nešlo o nástroj.“ Skonči událostí, číslem nebo otevřenou otázkou; poučení si čtenář vyvodí sám.
- **Žádný epilog po konci.** Když příběh dopadne, přestaň. Jeden nevyřešený konec zní lidsky, úplná uklizenost strojově.
- **Nech ambivalenci stát.** „Přechod se vyplatil a starý systém mi stejně chybí“ nepotřebuje smiřovací větu.
- **Neservíruj celé pozadí předem.** Jeden časový tah na text (začátek uprostřed scény, odložené číslo, návrat k detailu) vydá víc než jakákoli výměna slov.
- **Uveď lidi tím, co dělají nebo říkají.** Odstavec s titulem a životopisem zkrať, nebo škrtni. Kde existuje skutečný výrok, cituj ho. Nikdy ho nevymýšlej.
- **Generická historka bez jména a detailu** („Nedávno mi jeden klient řekl…“) působí vymyšleně, protože většinou je. Když zdroj detail nemá, označ mezeru.
- **Emoce: obraz nejvýš jednou.** Když text emoci hraje sérií obrazů (sevřené hrdlo, zatajený dech, ticho, které by se dalo krájet), nech jeden, nebo ji pojmenuj. Pojmenovaný pocit z lidského textu zůstává („Bál jsem se.“ je v pořádku). V přepisu emoci nemaž; když obraz nemá ve zdroji oporu, uveď mezeru v seznamu značek, větu nech. Opora je jen v anglické beletrii, pravidlo proto platí úzce: hlídá sérii obrazů, ne emoci samotnou.
- **Jedna odbočka je dovolená.** Lidé v příběhu i v eseji odbočí, AI drží jedno téma (D4). Odbočku ze zdroje v přepisu nemaž.
- **Oslov čtenáře jen tam, kde je to skutečné.** Otázku nebo oslovení ze zdroje nech; nové nepřidávej, to by byla vnucená osobnost.

Nikdy z toho nedělej kontrolní seznam. Vyber jeden nebo dva tahy na text a střídej je mezi texty. Kdyby každý text dostal všechny tahy najednou, vznikla by nová šablona.

- PŘED: „V pondělí poslala tabulku sama, bez urgence. A tehdy mi došlo, že nikdy nešlo o tabulky, ale o důvěru.“
- PO: „V pondělí poslala tabulku sama, bez urgence.“
- PŘED: „Jana Nováková, vedoucí provozu s patnáctiletou praxí v logistice, je známá svým systematickým přístupem. Po dvou minutách přerušila prezentaci: ‚Tohle nám trvá moc dlouho.‘“
- PO: „Vedoucí provozu Jana Nováková přerušila prezentaci po dvou minutách: ‚Tohle nám trvá moc dlouho.‘“ (patnáctiletá praxe se dá zmínit později, když na ní v příběhu záleží)
- PŘED: „Nedávno mi jeden klient řekl něco, co mi změnilo pohled.“
- PO: `[OVĚŘIT: kdo, kdy a co přesně řekl]`
- PŘED: „Když jsem otevřel e-mail, sevřel se mi žaludek, svět se na chvíli zastavil a v uších mi hučelo.“
- PO: „Když jsem otevřel e-mail, sevřel se mi žaludek.“ Jeden obraz zůstává, pocit se nehádá a nemaže.
- PŘED: „Ten e-mail mě vyděsil. Sevřel se mi žaludek a svět se na chvíli zastavil.“
- PO: „Ten e-mail mě vyděsil, sevřel se mi žaludek.“
- PONECHAT: příběh, který končí otevřeně a ambivalentně, bez smiřovací věty. „Bál jsem se.“ Jeden obraz ve chvíli, která si ho zaslouží.

## Registry

### Registr prezentací

Prezentace jsou vlastní registr a jedno pravidlo pro souvislý text obracejí: na slajdu je věcný jmenný styl lidský profesionální hlas. „Úvod do základů“ je jmenný ekvivalent „začneme od nuly“; hovorová věta, která v blogu zní živě, na slajdu působí ledabyle.

- **Řada titulků je shrnutí prezentace.** Přečti jen titulky po sobě; musí nést příběh samy. Jedno hlavní sdělení na slajd. Agenda je seznam titulků.
- **Podstatná jména místo hovorových sloves.** „Funkce systému“ místo „Co systém umí“, „Postup“ místo „Jak na to“. Střídmé pasivum je tu v pořádku: „Neověřené údaje se nepřebírají“ říká jasné pravidlo.
- **Žádné senzační jednověté pointy a žádná nosná metafora jako verdikt** („Koncept nese“, „Tohle je páteř strategie“). Dej na slajd číslo nebo kritérium.
- **Tón doporučení.** „Doporučení: čísla před odesláním zkontrolovat“ místo „Čísla vždycky checkněte!“.
- **Poznámky patří do poznámek.** Pokyny pro řečníka a interní komentáře nikdy na slajd. Žádná razítka („Návrh“, „Finální“, „Důvěrné“), pokud o ně nikdo nežádá.
- **Žádná dlouhá pomlčka.** Konstrukci s pomlčkou nahraď spojkou, dvojtečkou nebo vedlejší větou. Pomlčka „–“ v rozsahu (2024–2026) je v pořádku.

Uvnitř odrážek neplatí pravidlo o útržcích; odrážky na slajdu jsou útržky záměrně. Posuzuj je podle obsahu informace. Odrážky stejného gramatického tvaru, které netvrdí nic ověřitelného, zůstávají nálezem.

- PŘED (slajd): „Čísla před odesláním vždycky checkněte!“ → PO: „Doporučení: čísla před každým odesláním zkontrolovat“
- PŘED (slajd): „Neověřené = bezcenné“ → PO: označ mezeru: co se s neověřeným údajem stane a proč. Pravidlo přijetí nedomýšlej.
- PŘED (slajd): „Rychlé nasazení—ideální pro nové kolegy“ → PO: „Rychlé nasazení, ideální pro nové kolegy“
- PŘED (slajd): „Tady zdůraznit, že rozpočet ještě není schválený“ → PO: přesunout do poznámek řečníka.
- PONECHAT (slajd): „Rozpočet 2027: 4,2 mil. Kč (+8 %)“. Jmenný styl je tu správný.

### Odborný text

Odborný text má k seznamům slov navíc vlastní seznam: přehnaná slovesa („dokazuje“ → „ukazuje“, jen když zdroj tu sílu podporuje), klišé ve výčtu přínosů, hromadné citace bez zařazení, „nový“ a „unikátní“ jako nafouknutí. Žádné sloveso silnější než jeho důkaz. Když důkaz chybí, označ mezeru, tiše tvrzení neoslabuj. Opisné pasivum a „my“ jsou tu přirozené. Lidský odborný text je věcný a neosobní: neutralita a přesnost jsou tu lidský hlas, osobnost do něj nevnášej. Ponech kalibrované jištění („data naznačují“), pasivum tam, kde aktér nehraje roli, „my“, terminologii a všechna čísla a citace beze změny.

- PŘED: „Rozsáhlé experimenty na řadě datových sad jednoznačně dokazují, že náš nový přístup výrazně překonává současné metody.“
- PO: Bez podloženého přepisu. Označ mezery: které datové sady, které metody, jaké skóre a jaký test podporuje „výrazně“. Důkaz nevymýšlej a srovnání tiše neoslabuj.
- PONECHAT: „Výsledky naznačují, že vztah mezi proměnnými není lineární (r = 0,31; p = 0,02).“

## Pojistky v příkladech

Pravidla pojistek jsou celá v `../SKILL.md`. Tady jsou kontrolní příklady.

### Význam ve stejné síle

- „způsobuje“ se nesmí změnit na „ovlivňuje“
- „třikrát rychlejší“ se nesmí změnit na „rychlejší“
- „73 % dotázaných“ se nesmí změnit na „dotázaní“
- „zhruba 50 %“ se nesmí změnit na „50 %“
- „nesmí“ se nesmí změnit na „neměl by“
- „musí“ se nesmí změnit na „je potřeba“
- „od 2 do 5 dnů“ si ponechá oba konce
- „současně“ nesmí vypadnout, když tvrdí, že se dvě věci dějí najednou

### Postoj a konkrétnost při přepisu

Česká AI píše méně částic, jištění, otázek a čísel než lidé. Přepis je proto nesmí ubrat, i když větu jinak čistí.

- PŘED (lidský text s jedním tikem): „Upřímně, ten nový tarif je vlastně docela výhodný. Platíme zhruba o 300 Kč měsíčně míň a změnu jsme stihli za dva dny. Proč jsme to neudělali dřív?“
- ŠPATNÉ PO: „Nový tarif je výhodný. Platíme méně a změna proběhla rychle.“ Zmizela částice, jištění „docela“ a „zhruba“, číslo, doba i otázka.
- PO: „Ten nový tarif je vlastně docela výhodný. Platíme zhruba o 300 Kč měsíčně míň a změnu jsme stihli za dva dny. Proč jsme to neudělali dřív?“ Škrtnuté je jen dodatečné „Upřímně“.
- ŠKRTNI I TAK: vrstvené jištění („mohlo by možná potenciálně“) zkrať na jedno; „možná“ AI naopak přehání.

### Oprava bez nových chyb

Česká AI píše gramaticky a čtivě. Přepis, který vnese chybu, text nezlidští, jen pokazí.

- PŘED: „Data zpracovala firma z Brna. Výsledky poslala v pátek.“
- ŠPATNÉ PO: „Data zpracovala firma z Brna a výsledky poslali v pátek.“ Sloučení rozbilo shodu.
- PO: „Data zpracovala firma z Brna a výsledky poslala v pátek.“
- PŘED: „Nový tarif—platí od května—je levnější.“
- ŠPATNÉ PO: „Nový tarif který platí od května je levnější.“ Chybí čárky kolem vedlejší věty.
- PO: „Nový tarif, který platí od května, je levnější.“
- PŘED: „Problém jsme vyřešili. Pak jsme ho nahlásili.“
- ŠPATNÉ PO: „Problém vyřešili jsme a pak nahlásili.“ Příklonka „jsme“ patří za první větný člen.
- PO: „Problém jsme vyřešili a pak nahlásili.“

## Výčty tvarů podle závažnosti

Definice P0–P2, P0 celé a filtr přesnosti jsou v `../SKILL.md`. Závažnost řadí nález až po uplatnění registru, prahů, záměrného užití a filtru přesnosti; neznamená, že každý vyjmenovaný tvar je nález. Vzorce obsahu, stavby a vyprávění jsou P1 i jednotlivě; slabé samo o sobě jsou jen drobné signály.

**P1 – jasné AI tiky** (oprav před zveřejněním, s ohledem na profil, prahy a výjimky): nálezy ze seznamu slov nad prahem, kalky a falešní přátelé, kteří mění význam nebo znějí cize, termíny přeložené se změnou významu a vymyšlené termíny, kontrastní obraty a trojice mimo povolené užití, šablonovité úvody a přechody, dlouhá pomlčka „—“ v textu s dalšími nálezy P0 nebo P1, překročený rozpočet pomlček, nadužité tučné písmo, vrstvené jištění v jednom tvrzení, nafouknutý význam, dvojtečkové odhalení a otázka s odpovědí, předstíraný vhled, falešné prozření a mravoučná pointa, plastová lidskost („Upřímně řečeno“, „A víte, co je na tom nejlepší?“), vágní tvrzení o výsledku nebo účinku bez údaje („výrazně zrychluje“, „uživatelé ji milují“), okřídlené metafory o AI, fantomové námitky, inscenovaný důraz, heslovitá kadence od tří výskytů v textu, prestižní výčty, falešné agens, šablonovitá vyváženost, upoutávkové a hovorové titulky, anglický title case v nadpisech, nadbytečná přivlastňovací a podmětová zájmena v řadě, anglický slovosled, který mění důraz, příklonky mimo své místo, jmenný styl a opisné pasivum, když tvoří většinu vět textu, smíšené české a anglické formáty čísel v jednom textu (oddělovač řádů, desetinná čárka, datum, čas), generická historka bez jména a detailu (P0 jen tehdy, když zdroj ukazuje, že údaj je vymyšlený), dovětek s poučením a epilog v příběhu, vysvětlený podtext, emoce hraná tělem a atmosférou, aforistická pointa na konci i uprostřed textu, stejně stavěné odstavce, meta-komentář a výklad pro čtenáře („Jak je vidět“, „Co většina lidí přehlíží“), text o sobě, počítané seznamy pro efekt, ohlášení a rekapitulace, obecné a šablonovité závěry, výhled místo výsledku, rovnoměrná emoční gradace v příběhu, uvedení postavy životopisným odstavcem, řada titulků prezentace, která sama nenese příběh, odkaz na obsah, který v textu chybí (ohlášená příloha nebo aktualizace).

**P2 – vyleštění** (když je čas): samotná dlouhá pomlčka „—“, jednotvárný rytmus a řetězy krátkých vět mimo jejich domácí registr, odpověď, která staví kontext znovu, věty, které neprojdou testem přenositelnosti, opakované začátky vět, opakovaný obrat od tří výskytů, nepodložené absolutní výrazy v přesvědčovacím textu („vždy“, „všichni“, „nikdo“), opisy pro „je“ a „má“, šablonovité nadpisy a titulky slajdů („Úvod“, „Závěr“, „Klíčové poznatky“), jmenný styl a opisné pasivum v souvislém textu, ukazovací zájmena jako rituál, hustá síť odkazů, jediný šablonovitý přechod v textu, slabé kalky, nadbytečné anglicismy v textu pro obecné publikum, nejednotné velké a malé V ve vykání, tautologická zdvojení, drobnosti v mikroformátech (mezera v „50 %“, datum, desetinná čárka, kód „CZK“ místo „Kč“ v běžném textu o částkách).
