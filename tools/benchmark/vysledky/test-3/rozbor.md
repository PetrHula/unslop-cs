# Rozbor test-3: jadro-2 na test sadě

Stejný výběr jako `test-2` (132 textů rozhodovacích vrstev: 66 lidských, 66 AI; 1 běh, bez soudce). Nově běžela jen varianta unslop-cs-jadro-2 (otisk `81c212c5ce05`, beze změny od dev kola `dev-1j2`), 14,24 USD; běhy ostatních skillů převzaté z `test-2`. Verdikty s jadro-2 jako skillem A jsou přepočtené bez nových běhů v `vysledky/test-3j` (0 USD, jen jiné pořadí skillů v konfiguraci). Plán běhu je v PLAN.md, Historie, zapsaný před během. Výsledky z test sady jen souhrnně.

| (rozhodovací vrstvy) | lidské s nálezem | AI s nálezem | AUC hustoty | plané poplachy v/s | posun skóre AI | cena/text |
|---|---|---|---|---|---|---|
| unslop-cs 1.6.1 | 9,1 % | 65 % | 0,80 | 3,0 % | +0,006 | 0,136 |
| unslop-cs-jadro-2 | 10,6 % | 73 % | 0,84 | 3,0 % | +0,002 | 0,105 |
| anti-ai-slop-cz | 57,6 % | 98 % | 0,90 | 7,6 % | +0,009 | 0,101 |
| humanizer-czech | 69,7 % | 98 % | 0,88 | 24,2 % | −0,019 | 0,143 |
| bez-skillu | 45,5 % | 100 % | 0,96 | 13,6 % | +0,001 | 0,040 |

**Verdikty jadro-2 (test-3j):** proti anti-ai-slop-cz „shodná kvalita, náklady nerozhodují“ (lidské s nálezem −47 p. b. [−58; −36], ztráta čísel +0,0, cena 1,0×), proti humanizer-czech „A je lepší“, proti bez-skillu „shodná kvalita, B je levnější“, proti plné verzi „A není lepší“ jen proto, že interval lidských textů s nálezem (+1,5 p. b. [−6,6; +9,9] jako jadro − plná) přesahuje mez +3 p. b.

**Plná verze 1.6.1 proti jadro-2:** rozdíl ve všech rozhodovacích mírách je malý a neprůkazný (lidské s nálezem −1,5 p. b. [−9,9; +6,6], posun skóre +0,004 [−0,012; +0,022]); plná verze je o 30 % dražší (1,3×) a ztratí o kousek víc čísel (+0,6 p. b. [0; +1,9]). Na test sadě tedy plná verze za vyšší cenu nic měřitelného nepřináší.

**Omezení:** jeden běh; režim psaní jadro-2 se neměřil; soudce významu neprošel kalibrací, zachování významu stojí jen na číslech a jménech.
