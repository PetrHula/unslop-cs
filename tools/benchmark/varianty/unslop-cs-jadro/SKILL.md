---
name: unslop-cs-jadro
description: >-
  Kontrola a přepis českého textu proti AI slopu (úsporná varianta unslop-cs pro benchmark).
  Použij, když někdo chce zkontrolovat, co v českém textu zní jako psané AI, nebo text přepsat lidsky.
---

# Unslop CS: jádro

Hledáš místa, podle kterých čtenář pozná český text psaný AI, a opravuješ je tak, aby text dál patřil autorovi. Posuzuješ vzorce, nikdy autorství.

## 1. Přečti text jako redaktor

Nejdřív celý text přečti a zeptej se: které věty bych autorovi vrátil, protože zní vyrobeně, obecně nebo šablonovitě? Zapiš si je i tehdy, když nesedí do žádné kategorie níže. Vlastní čtení je hlavní zdroj nálezů; seznam vzorců slouží ke kontrole, že ti nic neuteklo.

## 2. Silné vzorce

**Obsah a stavba** (nejsilnější signál):
- Tvrzení o výsledku, přínosu nebo kvalitě bez čísla, jména, data nebo mechanismu („výrazně zrychluje“, „klíčovou roli hraje“).
- Mravoučná, symbolická nebo aforistická pointa na konci; poučení po příběhu; epilog, který uklidí konec.
- Vysvětlování toho, co scéna nebo fakt už nese („Věděli to všichni, jen nikdo to neřekl.“); emoce hraná sérií obrazů.
- Šablonovitý úvod („V dnešní době…“) a závěr (shrnutí, výhled, „budoucnost vypadá slibně“); pointa zopakovaná víckrát.
- Odstavce stavěné podle stejné šablony; falešné prozření („A tehdy mi došlo…“); fantomová námitka; text, který komentuje sám sebe.

**Věta:**
- Kontrastní obrat jako figura: „není to X, je to Y“, „nejde o X, jde o Y“, „nejen X, ale i Y“, „A místo B“.
- Trojice ze zvyku (tři přídavná jména, tři příklady, tři krátká tvrzení).
- Přívěsek s „což“ a „čímž“, který předstírá důsledek („…, což podtrhuje význam…“).
- Dvojtečkové odhalení a otázka s odpovědí („Výsledek? Rychlejší práce.“); inscenovaný důraz.
- Opakovaný obrat (třikrát „jako by“); řetěz krátkých vět nebo jednoslovné věty pro drama.

**Slova:**
- Nafouknutý a reklamní slovník: klíčový, zásadní, komplexní, robustní, revoluční, unikátní, inovativní, posunout na další úroveň, odemknout potenciál.
- Kalky: realizovat, adresovat problém, hrát klíčovou roli, na denní bázi, ponořit se do.
- Šablonovité přechody na začátku vět, hlavně v řadě: Navíc, Kromě toho, Dále, Nicméně, V neposlední řadě.
- Dlouhá pomlčka „—“ v českém textu.

**Kombinace je nejsilnější signál.** Tři a více různých vzorců v jednom textu (třeba kontrastní obrat, trojice, obecný závěr a žádné číslo) jsou nález samy o sobě: text je šablonovitý jako celek.

## 3. Filtr přesnosti: co nálezem není

Tohle odlišuje dobrou kontrolu od paranoidní. Projdi každý nález, než mu dáš závažnost:

- **Lidský text má zvláštnosti.** Překlepy, dobové a knižní obraty, drsnější tón, odbočky a nerovnoměrný rytmus jsou známky člověka, ne vady.
- **Registr.** V odborném, úředním a právním textu jsou jmenný styl, pasivum, terminologie a kalibrované jištění („data naznačují“, „nesmí“, „s výhradou“) obsah, ne tik. V beletrii patří k registru dialog, útržky v přímé řeči, scénické poznámky a dlouhá souvětí. Na sociálních sítích jsou krátké věty běžné.
- **Cizí text.** Citace, přímá řeč, názvy, termíny a text třetích stran nepočítej jako vady autora.
- **Slabé samo o sobě.** Jedna pomlčka, jedno jištění, jedno „Tento“, jeden přechod, jedna trojice, která má opravdu tři části („jméno, e-mail a číslo smlouvy“), jeden kontrastní obrat, který opravuje („ne za duben“, „o 12 %, ne o 21 %“): to je v lidském psaní běžné. Nálezem je to až ve shluku s dalšími vzorci.
- **Typografie** (rovné uvozovky, spojovník místo pomlčky, mezery) je nanejvýš poznámka, ne znak AI. Výjimkou je dlouhá pomlčka „—“.

Co po tomhle posouzení neplatí, mezi nálezy nepiš. Patří do oddílu Ponechané, bez závažnosti.

## 4. Závažnost

- **P0, ničí důvěru:** chatbotí artefakty („Skvělá otázka!“, „Doufám, že vám to pomůže“), vágní autority bez zdroje („odborníci se shodují“, „studie ukazují“), vymyšlené údaje, nevyplněné zástupné texty, ozvěna zadání.
- **P1, jasný AI tik:** zřetelný výskyt silného vzorce z oddílu 2, který by čtenář poznal; každý vzorec z obsahu a stavby; kombinace tří a více vzorců.
- **P2, vyleštění:** slabší výskyt, který ve shluku není, ale stojí za úpravu.

V nálezech buď přímý: co bys jako redaktor autorovi vrátil, je nález se závažností. Opatrný buď v přepisu.

## 5. Přepis: pojistky

Měň jen označená místa; čisté věty přenes beze změny. Přepis, který poruší některou pojistku, selhal:

- **Nic nevymýšlej.** Žádné číslo, jméno, datum, studie, citace, historka ani první osoba, které nejsou ve zdroji. Chybějící údaj označ `[OVĚŘIT: co chybí]` v seznamu, do textu ho nevkládej.
- **Nic tiše neztrácej.** Čísla, data, jména, citace, pořadí a podložená tvrzení zůstávají. Význam ve stejné síle: „způsobuje“ nezměníš na „ovlivňuje“, „třikrát rychlejší“ na „rychlejší“, „zhruba 50 %“ na „50 %“, „nesmí“ na „neměl by“.
- **Neubírej postoj.** Částice a jištění (asi, snad, přece, prý, totiž, vlastně, docela, zhruba), skutečné otázky, oslovení a odbočky ze zdroje nech. Nepřidávej je tam, kde nejsou.
- **Žádná vnucená hovorovost, hraná upřímnost ani sekání na útržky.** Spisovný text zůstane spisovný.
- **Bez nových chyb.** Po sloučení vět zkontroluj shodu, čárky a místo příklonek.

## 6. Výstup

1. Verdikt v jedné větě a počty P0, P1, P2.
2. Nálezy, každý na řádek: `[1] P1 · „citace místa“ · vzorec · proč`.
3. Ponechané: co vypadalo podezřele, ale je v pořádku, a proč (krátce, bez závažnosti). Když nic, vynech.
4. Seznam `[OVĚŘIT: …]`, když nějaké jsou.
5. Opravená verze celého textu.

Když je text čistý, řekni to a nic neměň.
