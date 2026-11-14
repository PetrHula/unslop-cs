# Rozbor dev-1j2: varianta unslop-cs-jadro-2

Stejných 90 dev textů jako dev-1 a dev-1j; nově běžela jen jadro-2 (90 běhů, 9,99 USD), ostatní převzaté. Změny proti jadro-1: vzorce obsahu, stavby a vyprávění jsou P1 i jednotlivě; „slabé samo o sobě“ jen pro drobné signály; žánr pointu neomlouvá; vypravěčské vzorce a aforistická pointa převzaté z anglického unslop (StoryScope 2026).

| skill | plané poplachy | lidské texty s jakýmkoli nálezem | citlivost (vš. / rozh.) | AUC vys./stř. (vš.) | AUC všech nálezů | ztráta jmen (vš.) | cena/text |
|---|---|---|---|---|---|---|---|
| **unslop-cs-jadro-2** | **0/40** | **1/40** | **72 % / 65 %** | **0,86** | 0,89 | 8,9 % | 0,11 |
| unslop-cs-jadro | 0/40 | 3/40 | 52 % / 38 % | 0,76 | 0,84 | 5,6 % | 0,10 |
| unslop-cs | 3/40 | 26/40 | 44 % / 42 % | 0,70 | 0,74 | 4,4 % | 0,28 |
| anti-ai-slop-cz | 3/40 | 26/40 | 68 % / 62 % | 0,82 | 0,90 | 12,1 % | 0,10 |
| humanizer-czech | 8/40 | 28/40 | 68 % / 58 % | 0,79 | 0,90 | 9,9 % | 0,15 |
| bez-skillu | 5/40 | 17/40 | 78 % / 77 % | 0,86 | 0,94 | 10,4 % | 0,05 |

**Výsledek:** citlivost vzrostla z 52 % na 72 % (proti jadro-1 +27 p. b. na rozhodovacích vrstvách, interval [+10; +42]) a plané poplachy zůstaly nulové. Na úrovni vysoká/střední odlišuje jadro-2 AI text od lidského stejně dobře jako model bez skillu (AUC 0,86) a lépe než ostatní skilly, za cenu anti-ai-slop-cz a 2,5× levněji než unslop-cs. Ztráta čísel 0.

**Pozor:**
- Ztráta jmen vzrostla (8,9 % proti 4,4 % u unslop-cs; interval proti unslop-cs [0; +15 p. b.]). Hrubá kontrola: část ztrát jsou jména ve smazané mravoučné pointě („Leštinské družstvo dokazuje, že…“). Pravidlo „aforistickou pointu smaž“ se tu bije s pojistkou „nic tiše neztrácej“; příští verze má fakta a jména ze smazané věty přenést jinam, nebo větu jen zkrátit.
- Varianta vznikla podle chyb na stejných dev textech, na kterých je změřená. Výsledek je proto optimistický; potvrdit ho musí jiná data (test sada, se záznamem v historii plánu).
