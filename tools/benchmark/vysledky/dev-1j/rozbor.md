# Rozbor dev-1j: úsporná varianta unslop-cs-jadro

Stejný výběr jako dev-1 (90 textů); ostatní skilly převzaté z dev-1, nově běžela jen varianta (90 běhů, 9,49 USD). Varianta: `tools/benchmark/varianty/unslop-cs-jadro/SKILL.md` (asi 6 kB), bez povinných referencí a skriptu; detekce úsudkem („přečti jako redaktor“), krátký seznam silných vzorců, pravidla unslop-cs jako filtr přesnosti a pojistky.

| skill | plané poplachy (vš. vrstvy) | lidské texty s jakýmkoli nálezem | citlivost (vš. vrstvy) | citlivost (rozhodovací) | AUC všech nálezů | cena/text | kroků |
|---|---|---|---|---|---|---|---|
| unslop-cs-jadro | **0/40** | **3/40** | 52 % | 38 % | 0,84 | **0,10** | 3 |
| unslop-cs | 3/40 | 26/40 | 44 % | 42 % | 0,74 | 0,28 | 6 |
| anti-ai-slop-cz | 3/40 | 26/40 | 68 % | 62 % | 0,90 | 0,10 | 3 |
| humanizer-czech | 8/40 | 28/40 | 68 % | 58 % | 0,90 | 0,14 | 3 |
| bez-skillu | 5/40 | 17/40 | 78 % | 77 % | 0,94 | 0,04 | 1 |

AUC je spočítané ze všech nálezů na 1 000 slov bez ohledu na závažnost (humanizer a anti z dev-1).

**Co vyšlo:** cena klesla na třetinu (stejně jako anti), plané poplachy na nulu a na lidských textech varianta skoro nic nehlásí (3 ze 40 proti 26). Odlišení AI od lidského textu se zlepšilo (AUC 0,74 → 0,84), ale citlivost na úrovni vysoká/střední skoro ne.

**Co nevyšlo:** varianta vidí stejné vzorce jako model bez skillu (mravoučná pointa, kontrastní obrat, obecný závěr), ale dá jim P2 („jeden výskyt, žádný shluk“, „pointa patří k žánru“). Filtr přesnosti působí silněji, než měl: pravidlo „slabé samo o sobě“ se rozšířilo i na vzorce obsahu a stavby, které měly být P1 i jednotlivě.

**Další krok (jadro-2):** zúžit „slabé samo o sobě“ jen na drobné signály (pomlčka, jištění, „Tento“, přechod, typografie) a výslovně říct, že vzorce obsahu a stavby a kontrastní obrat jako figura jsou P1 i jednotlivě; žánr pointu neomlouvá. Čekám vyšší citlivost a mírný nárůst planých poplachů.
