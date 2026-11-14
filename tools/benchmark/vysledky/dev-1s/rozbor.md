# Rozbor dev-1s: unslop-cs 1.6.0

Stejných 90 dev textů jako dev-1, dev-1j a dev-1j2; nově běžel jen unslop-cs 1.6.0 (commit `9622eac`, 90 běhů, 12,85 USD), ostatní převzaté z dev-1j2.

| skill | plané poplachy | lidské texty s jakýmkoli nálezem | citlivost (vš. / rozh.) | AUC všech nálezů | ztráta jmen (vš.) | cena/text |
|---|---|---|---|---|---|---|
| **unslop-cs 1.6.0** | 1/40 | 10/40 | **74 % / 65 %** | 0,86 | 8,3 % | 0,14 |
| unslop-cs-jadro-2 | 0/40 | 1/40 | 72 % / 65 % | 0,89 | 8,9 % | 0,11 |
| unslop-cs 1.5.0 (dev-1) | 3/40 | 26/40 | 44 % / 42 % | 0,74 | 4,4 % | 0,28 |
| anti-ai-slop-cz | 3/40 | 26/40 | 68 % / 62 % | 0,90 | 12,1 % | 0,10 |
| humanizer-czech | 8/40 | 28/40 | 68 % / 58 % | 0,90 | 9,9 % | 0,14 |
| bez-skillu | 5/40 | 17/40 | 78 % / 77 % | 0,94 | 10,4 % | 0,04 |

**Proti 1.5.0:** citlivost 44 % → 74 %, plané poplachy 3 → 1, lidské texty s jakýmkoli nálezem 26 → 10, odlišení AI textu (AUC) 0,74 → 0,86, cena 0,28 → 0,14 USD. Ztráta jmen vzrostla (4,4 % → 8,3 %), nová pojistka o přenesení jmen ze smazané pointy ji nesnížila.

**Proti konkurenci:** nejvyšší citlivost ze skillů a nejméně planých poplachů ze skillů; cena 1,4× anti-ai-slop-cz, stejná jako humanizer-czech. Model bez skillu má citlivost vyšší (78 %), ale 5 planých poplachů ze 40.

**Proti jadro-2:** stejná citlivost, o 30 % dražší (delší jádro s registry, pojistkami a formáty) a víc drobných nálezů na lidských textech (10 proti 1 ze 40). Jediný planý poplach: dlouhé pomlčky „—“ v dobově sazeném textu (klasika), které výstup sám ponechal jako dobovou sazbu, ale vypsal s P1. Pravidlo „co neplatí, do Ponechaných bez závažnosti“ se tu nedodrželo.

**Rozhodovací pravidlo** vyhlašuje proti jadro-2, anti a bez-skillu „A není lepší“, protože horní mez intervalu planých poplachů přesahuje 3 p. b. Na 26 lidských textech v rozhodovacích vrstvách stačí jeden planý poplach; vzorek na tohle pravidlo nestačí.

Skript spustilo 6 z 90 běhů, reference žádný. Varianta i 1.6.0 vznikly podle chyb na týchž dev textech; ověření patří na test sadu.
