# Benchmark skillů: test-2

- Datum: 2026-11-15 19:50 +0100; sada: test; textů: 132 (lidských 66, AI 66); běhů na text: 1; jen rozhodovací vrstvy (bez aikoditex, cac, fictree)
- Commit: `8065a8b`; otisky skillů: unslop-cs `9e801600fa97`, anti-ai-slop-cz `d98a1147e447`, humanizer-czech `639d897a18a5`, bez-skillu `None`
- Model skillu: claude-sonnet-5-5 (effort medium; Claude Code 2.1.325); soudce: claude-opus-5-5; normalizace: claude-haiku-5-5; modely z běhů: claude-sonnet-5-5
- Cena celkem: 56.90 USD; nevyhodnocené běhy: 0

## unslop-cs proti anti-ai-slop-cz: shodná kvalita, B je levnější o víc než 20 %

Rozhodovací vrstvy (bez aikoditex, cac, fictree); A − B, 95% interval z bootstrapu po shlucích. Kalibrace soudce: neprošla nebo neproběhla (A/B jen informativně)

- lidske_s_nalezem: horní mez -0.366 ≤ +0.030
- zmena_lidskych: horní mez -0.005 ≤ +0.020
- poruseni_vyznamu: soudce významu neprošel kalibrací, do rozhodnutí nevstupuje
- ztrata_cisel: horní mez +0.019 ≤ +0.020
- pridana_cisla: horní mez +0.000 ≤ +0.050
- lidske_s_nalezem: -0.485 [-0.603, -0.366]
- zmena_lidskych: -0.017 [-0.034, -0.005]
- ztrata_cisel: +0.006 [+0.000, +0.019]
- pridana_cisla: -0.015 [-0.053, +0.000]
- posun_skore: -0.003 [-0.035, +0.017]

K výkladu (do rozhodnutí nevstupuje):

- cena A/B: 1.3×
- lidské texty s nálezem: A 9.1%, B 57.6% (B/A 6.3×)
- plané poplachy (vysoká/střední): A 3.0%, B 7.6% (B/A 2.5×)
- plane_poplachy_vs A − B: -0.045 [-0.121, +0.016]
- citlivost_vs A − B: -0.061 [-0.169, +0.043]
- ai_s_nalezem A − B: -0.333 [-0.466, -0.220]
- ztrata_jmen A − B: -0.057 [-0.102, -0.010]
- pridana_jmena A − B: -0.061 [-0.140, +0.000]

## unslop-cs proti humanizer-czech: A je lepší

Rozhodovací vrstvy (bez aikoditex, cac, fictree); A − B, 95% interval z bootstrapu po shlucích. Kalibrace soudce: neprošla nebo neproběhla (A/B jen informativně)

- lidske_s_nalezem: horní mez -0.474 ≤ +0.030
- zmena_lidskych: horní mez -0.030 ≤ +0.020
- poruseni_vyznamu: soudce významu neprošel kalibrací, do rozhodnutí nevstupuje
- ztrata_cisel: horní mez +0.000 ≤ +0.020
- pridana_cisla: horní mez +0.000 ≤ +0.050
- posun skóre AI-ovosti: interval [+0.003, +0.059] nad nulou
- lidske_s_nalezem: -0.606 [-0.739, -0.474]
- zmena_lidskych: -0.059 [-0.099, -0.030]
- ztrata_cisel: +0.000 [+0.000, +0.000]
- pridana_cisla: +0.000 [+0.000, +0.000]
- posun_skore: +0.025 [+0.003, +0.059]

K výkladu (do rozhodnutí nevstupuje):

- cena A/B: 0.9×
- lidské texty s nálezem: A 9.1%, B 69.7% (B/A 7.7×)
- plané poplachy (vysoká/střední): A 3.0%, B 24.2% (B/A 8.0×)
- plane_poplachy_vs A − B: -0.212 [-0.345, -0.111]
- citlivost_vs A − B: -0.167 [-0.327, -0.027]
- ai_s_nalezem A − B: -0.333 [-0.464, -0.220]
- ztrata_jmen A − B: -0.035 [-0.087, +0.009]
- pridana_jmena A − B: -0.152 [-0.240, -0.074]

## unslop-cs proti bez-skillu: shodná kvalita, B je levnější o víc než 20 %

Rozhodovací vrstvy (bez aikoditex, cac, fictree); A − B, 95% interval z bootstrapu po shlucích. Kalibrace soudce: neprošla nebo neproběhla (A/B jen informativně)

- lidske_s_nalezem: horní mez -0.250 ≤ +0.030
- zmena_lidskych: horní mez -0.005 ≤ +0.020
- poruseni_vyznamu: soudce významu neprošel kalibrací, do rozhodnutí nevstupuje
- ztrata_cisel: horní mez +0.000 ≤ +0.020
- pridana_cisla: horní mez +0.000 ≤ +0.050
- lidske_s_nalezem: -0.364 [-0.500, -0.250]
- zmena_lidskych: -0.013 [-0.026, -0.005]
- ztrata_cisel: -0.006 [-0.019, +0.000]
- pridana_cisla: +0.000 [+0.000, +0.000]
- posun_skore: +0.005 [-0.008, +0.022]

K výkladu (do rozhodnutí nevstupuje):

- cena A/B: 3.4×
- lidské texty s nálezem: A 9.1%, B 45.5% (B/A 5.0×)
- plané poplachy (vysoká/střední): A 3.0%, B 13.6% (B/A 4.5×)
- plane_poplachy_vs A − B: -0.106 [-0.204, -0.027]
- citlivost_vs A − B: -0.152 [-0.263, -0.056]
- ai_s_nalezem A − B: -0.348 [-0.483, -0.232]
- ztrata_jmen A − B: -0.061 [-0.111, -0.025]
- pridana_jmena A − B: -0.091 [-0.182, -0.014]

### Vrstva: rozhodovaci

| skill | lidských / AI | lidské s nálezem | AI s nálezem | AUC hustoty | plané poplachy v/s | citlivost v/s | AUC v/s | kappa | posun skóre AI | přiblížení k autorovi | ztráta čísel | přidaná čísla | ztráta jmen | přidaná jména | porušení významu | změna lidských | posun skóre lidských | bez verze | cena/text | kroků | čas s | zamítnutí | chyba nástroje |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| unslop-cs | 66 / 66 | 0.091 | 0.652 | 0.803 | 0.030 | 0.591 | 0.788 | – | 0.006 | -0.335 | 0.006 | 0 | 0.052 | 0.030 | – | 0.001 | 0.003 | 0 | 0.136 | 3.000 | 29.600 | 0 | 0 |
| anti-ai-slop-cz | 66 / 66 | 0.576 | 0.985 | 0.897 | 0.076 | 0.652 | 0.804 | – | 0.009 | -0.368 | 0.000 | 0.015 | 0.108 | 0.091 | – | 0.017 | -0.000 | 0 | 0.101 | 3.000 | 27.500 | 0 | 0 |
| humanizer-czech | 66 / 66 | 0.697 | 0.985 | 0.879 | 0.242 | 0.758 | 0.786 | – | -0.019 | -0.396 | 0.006 | 0 | 0.086 | 0.182 | – | 0.060 | -0.019 | 0 | 0.143 | 3.000 | 30.750 | 0 | 0 |
| bez-skillu | 66 / 66 | 0.455 | 1 | 0.963 | 0.136 | 0.742 | 0.842 | – | 0.001 | -0.381 | 0.012 | 0 | 0.113 | 0.121 | – | 0.013 | -0.002 | 0 | 0.040 | 1.000 | 24.700 | 0 | 0 |

### Vrstva: vse

| skill | lidských / AI | lidské s nálezem | AI s nálezem | AUC hustoty | plané poplachy v/s | citlivost v/s | AUC v/s | kappa | posun skóre AI | přiblížení k autorovi | ztráta čísel | přidaná čísla | ztráta jmen | přidaná jména | porušení významu | změna lidských | posun skóre lidských | bez verze | cena/text | kroků | čas s | zamítnutí | chyba nástroje |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| unslop-cs | 66 / 66 | 0.091 | 0.652 | 0.803 | 0.030 | 0.591 | 0.788 | – | 0.006 | -0.335 | 0.006 | 0 | 0.052 | 0.030 | – | 0.001 | 0.003 | 0 | 0.136 | 3.000 | 29.600 | 0 | 0 |
| anti-ai-slop-cz | 66 / 66 | 0.576 | 0.985 | 0.897 | 0.076 | 0.652 | 0.804 | – | 0.009 | -0.368 | 0.000 | 0.015 | 0.108 | 0.091 | – | 0.017 | -0.000 | 0 | 0.101 | 3.000 | 27.500 | 0 | 0 |
| humanizer-czech | 66 / 66 | 0.697 | 0.985 | 0.879 | 0.242 | 0.758 | 0.786 | – | -0.019 | -0.396 | 0.006 | 0 | 0.086 | 0.182 | – | 0.060 | -0.019 | 0 | 0.143 | 3.000 | 30.750 | 0 | 0 |
| bez-skillu | 66 / 66 | 0.455 | 1 | 0.963 | 0.136 | 0.742 | 0.842 | – | 0.001 | -0.381 | 0.012 | 0 | 0.113 | 0.121 | – | 0.013 | -0.002 | 0 | 0.040 | 1.000 | 24.700 | 0 | 0 |

### Vrstva: klasika

| skill | lidských / AI | lidské s nálezem | AI s nálezem | AUC hustoty | plané poplachy v/s | citlivost v/s | AUC v/s | kappa | posun skóre AI | přiblížení k autorovi | ztráta čísel | přidaná čísla | ztráta jmen | přidaná jména | porušení významu | změna lidských | posun skóre lidských | bez verze | cena/text | kroků | čas s | zamítnutí | chyba nástroje |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| unslop-cs | 36 / 36 | 0 | 0.722 | 0.861 | 0 | 0.694 | 0.847 | – | 0.004 | -0.356 | 0.000 | 0 | 0.044 | 0.056 | – | 0.000 | 0.000 | 0 | 0.136 | 3.000 | 29.500 | 0 | 0 |
| anti-ai-slop-cz | 36 / 36 | 0.361 | 1 | 0.978 | 0 | 0.639 | 0.819 | – | 0.001 | -0.296 | 0.000 | 0.028 | 0.145 | 0.056 | – | 0.000 | -0.000 | 0 | 0.100 | 3.000 | 26.850 | 0 | 0 |
| humanizer-czech | 36 / 36 | 0.472 | 0.972 | 0.970 | 0 | 0.639 | 0.819 | – | 0.002 | -0.205 | 0.000 | 0 | 0.055 | 0.111 | – | 0.000 | -0.000 | 0 | 0.141 | 3.000 | 29.100 | 0 | 0 |
| bez-skillu | 36 / 36 | 0.222 | 1 | 0.992 | 0.028 | 0.778 | 0.883 | – | 0.005 | -0.257 | 0.000 | 0 | 0.081 | 0.111 | – | 0.002 | -0.004 | 0 | 0.039 | 1.000 | 24.350 | 0 | 0 |

### Vrstva: wiki

| skill | lidských / AI | lidské s nálezem | AI s nálezem | AUC hustoty | plané poplachy v/s | citlivost v/s | AUC v/s | kappa | posun skóre AI | přiblížení k autorovi | ztráta čísel | přidaná čísla | ztráta jmen | přidaná jména | porušení významu | změna lidských | posun skóre lidských | bez verze | cena/text | kroků | čas s | zamítnutí | chyba nástroje |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| unslop-cs | 18 / 18 | 0.278 | 0.500 | 0.647 | 0.111 | 0.333 | 0.627 | – | -0.024 | -0.152 | 0.000 | 0 | 0.029 | 0 | – | 0.002 | 0.011 | 0 | 0.138 | 3.000 | 30.400 | 0 | 0 |
| anti-ai-slop-cz | 18 / 18 | 0.889 | 0.944 | 0.650 | 0.222 | 0.556 | 0.694 | – | 0.013 | -0.369 | 0.000 | 0 | 0.036 | 0.111 | – | 0.053 | -0.004 | 0 | 0.103 | 3.000 | 28.650 | 0 | 0 |
| humanizer-czech | 18 / 18 | 0.944 | 1 | 0.747 | 0.556 | 0.889 | 0.679 | – | -0.066 | -0.439 | 0.000 | 0 | 0.065 | 0.333 | – | 0.139 | -0.044 | 0 | 0.148 | 3.000 | 33.600 | 0 | 0 |
| bez-skillu | 18 / 18 | 0.778 | 1 | 0.769 | 0.389 | 0.667 | 0.710 | – | -0.009 | -0.430 | 0.000 | 0 | 0.076 | 0.167 | – | 0.041 | -0.007 | 0 | 0.044 | 1.000 | 26.350 | 0 | 0 |

### Vrstva: uredni

| skill | lidských / AI | lidské s nálezem | AI s nálezem | AUC hustoty | plané poplachy v/s | citlivost v/s | AUC v/s | kappa | posun skóre AI | přiblížení k autorovi | ztráta čísel | přidaná čísla | ztráta jmen | přidaná jména | porušení významu | změna lidských | posun skóre lidských | bez verze | cena/text | kroků | čas s | zamítnutí | chyba nástroje |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| unslop-cs | 12 / 12 | 0.083 | 0.667 | 0.819 | 0 | 0.667 | 0.833 | – | 0.058 | -0.567 | 0.015 | 0 | 0.125 | 0 | – | 0.000 | -0.000 | 0 | 0.135 | 3.000 | 28.200 | 0 | 0 |
| anti-ai-slop-cz | 12 / 12 | 0.750 | 1 | 0.917 | 0.083 | 0.833 | 0.889 | – | 0.029 | -0.561 | 0.000 | 0 | 0.125 | 0.167 | – | 0.016 | 0.005 | 0 | 0.102 | 3.000 | 27.050 | 0 | 0 |
| humanizer-czech | 12 / 12 | 1 | 1 | 0.903 | 0.500 | 0.917 | 0.851 | – | -0.010 | -0.850 | 0.015 | 0 | 0.250 | 0.167 | – | 0.120 | -0.041 | 0 | 0.145 | 3.000 | 31.700 | 0 | 0 |
| bez-skillu | 12 / 12 | 0.667 | 1 | 1.000 | 0.083 | 0.750 | 0.865 | – | 0.002 | -0.638 | 0.030 | 0 | 0.312 | 0.083 | – | 0.007 | 0.010 | 0 | 0.035 | 1.000 | 21.600 | 0 | 0 |

Lidské / AI s nálezem = podíl lidských / AI textů s aspoň jedním nálezem jakékoli závažnosti (nezávisí na tom, jak skill štítkuje závažnost); AUC hustoty = odlišení AI a lidských textů podle počtu všech nálezů na 1000 slov. Plané poplachy v/s a citlivost v/s = totéž jen s nálezy vysoké nebo střední závažnosti. Přidaná čísla / jména = podíl přepisů AI textů s aspoň jedním číslem či datem / vlastním jménem, které v originálu není. Zamítnutí a chyba nástroje = podíl běhů, kde skill narazil na zamítnutý nebo chybný nástroj (chyba nástroje se zaznamenává od 2026-11-13). Posun skóre = skóre AI-ovosti před minus po přepisu (kladné = blíž lidským textům). Přiblížení k autorovi = o kolik se rysy F0 pokračování přiblížily skutečnému pokračování autora. Ztráty a porušení významu jen u AI textů. Kappa = shoda běhů v tom, zda text má nález.
