# Benchmark skillů: test-3j

- Datum: 2026-11-15 20:09 +0100; sada: test; textů: 132 (lidských 66, AI 66); běhů na text: 1; jen rozhodovací vrstvy (bez aikoditex, cac, fictree)
- Commit: `4745982`; otisky skillů: unslop-cs-jadro-2 `81c212c5ce05`, unslop-cs `9e801600fa97`, anti-ai-slop-cz `d98a1147e447`, humanizer-czech `639d897a18a5`, bez-skillu `None`
- Model skillu: claude-sonnet-5-5 (effort medium; Claude Code 2.1.325); soudce: claude-opus-5-5; normalizace: claude-haiku-5-5; modely z běhů: claude-sonnet-5-5
- Cena celkem: 0.00 USD; nevyhodnocené běhy: 0; převzaté běhy: 660

## unslop-cs-jadro-2 proti unslop-cs: A není lepší (zhoršuje plané poplachy nebo zachování významu)

Rozhodovací vrstvy (bez aikoditex, cac, fictree); A − B, 95% interval z bootstrapu po shlucích. Kalibrace soudce: neprošla nebo neproběhla (A/B jen informativně)

- lidske_s_nalezem: horní mez +0.099 > +0.030 (A může být horší)
- zmena_lidskych: horní mez +0.004 ≤ +0.020
- poruseni_vyznamu: soudce významu neprošel kalibrací, do rozhodnutí nevstupuje
- ztrata_cisel: horní mez +0.000 ≤ +0.020
- pridana_cisla: horní mez +0.000 ≤ +0.050
- lidske_s_nalezem: +0.015 [-0.066, +0.099]
- zmena_lidskych: +0.002 [+0.000, +0.004]
- ztrata_cisel: -0.006 [-0.019, +0.000]
- pridana_cisla: +0.000 [+0.000, +0.000]
- posun_skore: -0.004 [-0.022, +0.012]

K výkladu (do rozhodnutí nevstupuje):

- cena A/B: 0.8×
- lidské texty s nálezem: A 10.6%, B 9.1% (B/A 0.9×)
- plané poplachy (vysoká/střední): A 3.0%, B 3.0% (B/A 1.0×)
- plane_poplachy_vs A − B: +0.000 [-0.046, +0.044]
- citlivost_vs A − B: +0.000 [-0.038, +0.048]
- ai_s_nalezem A − B: +0.076 [-0.012, +0.185]
- ztrata_jmen A − B: -0.000 [-0.015, +0.014]
- pridana_jmena A − B: +0.000 [-0.051, +0.069]

## unslop-cs-jadro-2 proti anti-ai-slop-cz: shodná kvalita, náklady nerozhodují

Rozhodovací vrstvy (bez aikoditex, cac, fictree); A − B, 95% interval z bootstrapu po shlucích. Kalibrace soudce: neprošla nebo neproběhla (A/B jen informativně)

- lidske_s_nalezem: horní mez -0.362 ≤ +0.030
- zmena_lidskych: horní mez -0.004 ≤ +0.020
- poruseni_vyznamu: soudce významu neprošel kalibrací, do rozhodnutí nevstupuje
- ztrata_cisel: horní mez +0.000 ≤ +0.020
- pridana_cisla: horní mez +0.000 ≤ +0.050
- lidske_s_nalezem: -0.470 [-0.580, -0.362]
- zmena_lidskych: -0.015 [-0.033, -0.004]
- ztrata_cisel: +0.000 [+0.000, +0.000]
- pridana_cisla: -0.015 [-0.053, +0.000]
- posun_skore: -0.007 [-0.039, +0.017]

K výkladu (do rozhodnutí nevstupuje):

- cena A/B: 1.0×
- lidské texty s nálezem: A 10.6%, B 57.6% (B/A 5.4×)
- plané poplachy (vysoká/střední): A 3.0%, B 7.6% (B/A 2.5×)
- plane_poplachy_vs A − B: -0.045 [-0.121, +0.016]
- citlivost_vs A − B: -0.061 [-0.160, +0.031]
- ai_s_nalezem A − B: -0.258 [-0.356, -0.164]
- ztrata_jmen A − B: -0.057 [-0.102, -0.008]
- pridana_jmena A − B: -0.061 [-0.139, +0.016]

## unslop-cs-jadro-2 proti humanizer-czech: A je lepší

Rozhodovací vrstvy (bez aikoditex, cac, fictree); A − B, 95% interval z bootstrapu po shlucích. Kalibrace soudce: neprošla nebo neproběhla (A/B jen informativně)

- lidske_s_nalezem: horní mez -0.463 ≤ +0.030
- zmena_lidskych: horní mez -0.029 ≤ +0.020
- poruseni_vyznamu: soudce významu neprošel kalibrací, do rozhodnutí nevstupuje
- ztrata_cisel: horní mez +0.000 ≤ +0.020
- pridana_cisla: horní mez +0.000 ≤ +0.050
- posun skóre AI-ovosti: interval [+0.001, +0.052] nad nulou
- lidske_s_nalezem: -0.591 [-0.723, -0.463]
- zmena_lidskych: -0.057 [-0.096, -0.029]
- ztrata_cisel: -0.006 [-0.019, +0.000]
- pridana_cisla: +0.000 [+0.000, +0.000]
- posun_skore: +0.021 [+0.001, +0.052]

K výkladu (do rozhodnutí nevstupuje):

- cena A/B: 0.7×
- lidské texty s nálezem: A 10.6%, B 69.7% (B/A 6.6×)
- plané poplachy (vysoká/střední): A 3.0%, B 24.2% (B/A 8.0×)
- plane_poplachy_vs A − B: -0.212 [-0.346, -0.111]
- citlivost_vs A − B: -0.167 [-0.309, -0.044]
- ai_s_nalezem A − B: -0.258 [-0.358, -0.162]
- ztrata_jmen A − B: -0.035 [-0.085, +0.008]
- pridana_jmena A − B: -0.152 [-0.246, -0.052]

## unslop-cs-jadro-2 proti bez-skillu: shodná kvalita, B je levnější o víc než 20 %

Rozhodovací vrstvy (bez aikoditex, cac, fictree); A − B, 95% interval z bootstrapu po shlucích. Kalibrace soudce: neprošla nebo neproběhla (A/B jen informativně)

- lidske_s_nalezem: horní mez -0.238 ≤ +0.030
- zmena_lidskych: horní mez -0.003 ≤ +0.020
- poruseni_vyznamu: soudce významu neprošel kalibrací, do rozhodnutí nevstupuje
- ztrata_cisel: horní mez +0.000 ≤ +0.020
- pridana_cisla: horní mez +0.000 ≤ +0.050
- lidske_s_nalezem: -0.348 [-0.478, -0.238]
- zmena_lidskych: -0.011 [-0.024, -0.003]
- ztrata_cisel: -0.012 [-0.037, +0.000]
- pridana_cisla: +0.000 [+0.000, +0.000]
- posun_skore: +0.001 [-0.010, +0.013]

K výkladu (do rozhodnutí nevstupuje):

- cena A/B: 2.6×
- lidské texty s nálezem: A 10.6%, B 45.5% (B/A 4.3×)
- plané poplachy (vysoká/střední): A 3.0%, B 13.6% (B/A 4.5×)
- plane_poplachy_vs A − B: -0.106 [-0.204, -0.026]
- citlivost_vs A − B: -0.152 [-0.250, -0.071]
- ai_s_nalezem A − B: -0.273 [-0.375, -0.175]
- ztrata_jmen A − B: -0.062 [-0.111, -0.021]
- pridana_jmena A − B: -0.091 [-0.180, +0.000]

### Vrstva: rozhodovaci

| skill | lidských / AI | lidské s nálezem | AI s nálezem | AUC hustoty | plané poplachy v/s | citlivost v/s | AUC v/s | kappa | posun skóre AI | přiblížení k autorovi | ztráta čísel | přidaná čísla | ztráta jmen | přidaná jména | porušení významu | změna lidských | posun skóre lidských | bez verze | cena/text | kroků | čas s | zamítnutí | chyba nástroje |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| unslop-cs-jadro-2 | 66 / 66 | 0.106 | 0.727 | 0.837 | 0.030 | 0.591 | 0.787 | – | 0.002 | -0.285 | 0.000 | 0 | 0.051 | 0.030 | – | 0.002 | 0.005 | 0 | 0.105 | 3.000 | 26.200 | 0 | 0 |
| unslop-cs | 66 / 66 | 0.091 | 0.652 | 0.803 | 0.030 | 0.591 | 0.788 | – | 0.006 | -0.335 | 0.006 | 0 | 0.052 | 0.030 | – | 0.001 | 0.003 | 0 | 0.136 | 3.000 | 29.600 | 0 | 0 |
| anti-ai-slop-cz | 66 / 66 | 0.576 | 0.985 | 0.897 | 0.076 | 0.652 | 0.804 | – | 0.009 | -0.368 | 0.000 | 0.015 | 0.108 | 0.091 | – | 0.017 | -0.000 | 0 | 0.101 | 3.000 | 27.500 | 0 | 0 |
| humanizer-czech | 66 / 66 | 0.697 | 0.985 | 0.879 | 0.242 | 0.758 | 0.786 | – | -0.019 | -0.396 | 0.006 | 0 | 0.086 | 0.182 | – | 0.060 | -0.019 | 0 | 0.143 | 3.000 | 30.750 | 0 | 0 |
| bez-skillu | 66 / 66 | 0.455 | 1 | 0.963 | 0.136 | 0.742 | 0.842 | – | 0.001 | -0.381 | 0.012 | 0 | 0.113 | 0.121 | – | 0.013 | -0.002 | 0 | 0.040 | 1.000 | 24.700 | 0 | 0 |

### Vrstva: vse

| skill | lidských / AI | lidské s nálezem | AI s nálezem | AUC hustoty | plané poplachy v/s | citlivost v/s | AUC v/s | kappa | posun skóre AI | přiblížení k autorovi | ztráta čísel | přidaná čísla | ztráta jmen | přidaná jména | porušení významu | změna lidských | posun skóre lidských | bez verze | cena/text | kroků | čas s | zamítnutí | chyba nástroje |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| unslop-cs-jadro-2 | 66 / 66 | 0.106 | 0.727 | 0.837 | 0.030 | 0.591 | 0.787 | – | 0.002 | -0.285 | 0.000 | 0 | 0.051 | 0.030 | – | 0.002 | 0.005 | 0 | 0.105 | 3.000 | 26.200 | 0 | 0 |
| unslop-cs | 66 / 66 | 0.091 | 0.652 | 0.803 | 0.030 | 0.591 | 0.788 | – | 0.006 | -0.335 | 0.006 | 0 | 0.052 | 0.030 | – | 0.001 | 0.003 | 0 | 0.136 | 3.000 | 29.600 | 0 | 0 |
| anti-ai-slop-cz | 66 / 66 | 0.576 | 0.985 | 0.897 | 0.076 | 0.652 | 0.804 | – | 0.009 | -0.368 | 0.000 | 0.015 | 0.108 | 0.091 | – | 0.017 | -0.000 | 0 | 0.101 | 3.000 | 27.500 | 0 | 0 |
| humanizer-czech | 66 / 66 | 0.697 | 0.985 | 0.879 | 0.242 | 0.758 | 0.786 | – | -0.019 | -0.396 | 0.006 | 0 | 0.086 | 0.182 | – | 0.060 | -0.019 | 0 | 0.143 | 3.000 | 30.750 | 0 | 0 |
| bez-skillu | 66 / 66 | 0.455 | 1 | 0.963 | 0.136 | 0.742 | 0.842 | – | 0.001 | -0.381 | 0.012 | 0 | 0.113 | 0.121 | – | 0.013 | -0.002 | 0 | 0.040 | 1.000 | 24.700 | 0 | 0 |

### Vrstva: klasika

| skill | lidských / AI | lidské s nálezem | AI s nálezem | AUC hustoty | plané poplachy v/s | citlivost v/s | AUC v/s | kappa | posun skóre AI | přiblížení k autorovi | ztráta čísel | přidaná čísla | ztráta jmen | přidaná jména | porušení významu | změna lidských | posun skóre lidských | bez verze | cena/text | kroků | čas s | zamítnutí | chyba nástroje |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| unslop-cs-jadro-2 | 36 / 36 | 0 | 0.722 | 0.861 | 0 | 0.694 | 0.847 | – | 0.009 | -0.395 | 0.000 | 0 | 0.040 | 0.028 | – | 0.000 | -0.000 | 0 | 0.104 | 3.000 | 26.150 | 0 | 0 |
| unslop-cs | 36 / 36 | 0 | 0.722 | 0.861 | 0 | 0.694 | 0.847 | – | 0.004 | -0.356 | 0.000 | 0 | 0.044 | 0.056 | – | 0.000 | 0.000 | 0 | 0.136 | 3.000 | 29.500 | 0 | 0 |
| anti-ai-slop-cz | 36 / 36 | 0.361 | 1 | 0.978 | 0 | 0.639 | 0.819 | – | 0.001 | -0.296 | 0.000 | 0.028 | 0.145 | 0.056 | – | 0.000 | -0.000 | 0 | 0.100 | 3.000 | 26.850 | 0 | 0 |
| humanizer-czech | 36 / 36 | 0.472 | 0.972 | 0.970 | 0 | 0.639 | 0.819 | – | 0.002 | -0.205 | 0.000 | 0 | 0.055 | 0.111 | – | 0.000 | -0.000 | 0 | 0.141 | 3.000 | 29.100 | 0 | 0 |
| bez-skillu | 36 / 36 | 0.222 | 1 | 0.992 | 0.028 | 0.778 | 0.883 | – | 0.005 | -0.257 | 0.000 | 0 | 0.081 | 0.111 | – | 0.002 | -0.004 | 0 | 0.039 | 1.000 | 24.350 | 0 | 0 |

### Vrstva: wiki

| skill | lidských / AI | lidské s nálezem | AI s nálezem | AUC hustoty | plané poplachy v/s | citlivost v/s | AUC v/s | kappa | posun skóre AI | přiblížení k autorovi | ztráta čísel | přidaná čísla | ztráta jmen | přidaná jména | porušení významu | změna lidských | posun skóre lidských | bez verze | cena/text | kroků | čas s | zamítnutí | chyba nástroje |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| unslop-cs-jadro-2 | 18 / 18 | 0.333 | 0.667 | 0.741 | 0.111 | 0.333 | 0.627 | – | -0.015 | -0.099 | 0.000 | 0 | 0.037 | 0.056 | – | 0.008 | 0.019 | 0 | 0.107 | 3.000 | 26.450 | 0 | 0 |
| unslop-cs | 18 / 18 | 0.278 | 0.500 | 0.647 | 0.111 | 0.333 | 0.627 | – | -0.024 | -0.152 | 0.000 | 0 | 0.029 | 0 | – | 0.002 | 0.011 | 0 | 0.138 | 3.000 | 30.400 | 0 | 0 |
| anti-ai-slop-cz | 18 / 18 | 0.889 | 0.944 | 0.650 | 0.222 | 0.556 | 0.694 | – | 0.013 | -0.369 | 0.000 | 0 | 0.036 | 0.111 | – | 0.053 | -0.004 | 0 | 0.103 | 3.000 | 28.650 | 0 | 0 |
| humanizer-czech | 18 / 18 | 0.944 | 1 | 0.747 | 0.556 | 0.889 | 0.679 | – | -0.066 | -0.439 | 0.000 | 0 | 0.065 | 0.333 | – | 0.139 | -0.044 | 0 | 0.148 | 3.000 | 33.600 | 0 | 0 |
| bez-skillu | 18 / 18 | 0.778 | 1 | 0.769 | 0.389 | 0.667 | 0.710 | – | -0.009 | -0.430 | 0.000 | 0 | 0.076 | 0.167 | – | 0.041 | -0.007 | 0 | 0.044 | 1.000 | 26.350 | 0 | 0 |

### Vrstva: uredni

| skill | lidských / AI | lidské s nálezem | AI s nálezem | AUC hustoty | plané poplachy v/s | citlivost v/s | AUC v/s | kappa | posun skóre AI | přiblížení k autorovi | ztráta čísel | přidaná čísla | ztráta jmen | přidaná jména | porušení významu | změna lidských | posun skóre lidských | bez verze | cena/text | kroků | čas s | zamítnutí | chyba nástroje |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| unslop-cs-jadro-2 | 12 / 12 | 0.083 | 0.833 | 0.896 | 0 | 0.667 | 0.833 | – | 0.005 | -0.279 | 0.000 | 0 | 0.125 | 0 | – | 0.000 | 0.002 | 0 | 0.106 | 3.000 | 26.000 | 0 | 0 |
| unslop-cs | 12 / 12 | 0.083 | 0.667 | 0.819 | 0 | 0.667 | 0.833 | – | 0.058 | -0.567 | 0.015 | 0 | 0.125 | 0 | – | 0.000 | -0.000 | 0 | 0.135 | 3.000 | 28.200 | 0 | 0 |
| anti-ai-slop-cz | 12 / 12 | 0.750 | 1 | 0.917 | 0.083 | 0.833 | 0.889 | – | 0.029 | -0.561 | 0.000 | 0 | 0.125 | 0.167 | – | 0.016 | 0.005 | 0 | 0.102 | 3.000 | 27.050 | 0 | 0 |
| humanizer-czech | 12 / 12 | 1 | 1 | 0.903 | 0.500 | 0.917 | 0.851 | – | -0.010 | -0.850 | 0.015 | 0 | 0.250 | 0.167 | – | 0.120 | -0.041 | 0 | 0.145 | 3.000 | 31.700 | 0 | 0 |
| bez-skillu | 12 / 12 | 0.667 | 1 | 1.000 | 0.083 | 0.750 | 0.865 | – | 0.002 | -0.638 | 0.030 | 0 | 0.312 | 0.083 | – | 0.007 | 0.010 | 0 | 0.035 | 1.000 | 21.600 | 0 | 0 |

Lidské / AI s nálezem = podíl lidských / AI textů s aspoň jedním nálezem jakékoli závažnosti (nezávisí na tom, jak skill štítkuje závažnost); AUC hustoty = odlišení AI a lidských textů podle počtu všech nálezů na 1000 slov. Plané poplachy v/s a citlivost v/s = totéž jen s nálezy vysoké nebo střední závažnosti. Přidaná čísla / jména = podíl přepisů AI textů s aspoň jedním číslem či datem / vlastním jménem, které v originálu není. Zamítnutí a chyba nástroje = podíl běhů, kde skill narazil na zamítnutý nebo chybný nástroj (chyba nástroje se zaznamenává od 2026-11-13). Posun skóre = skóre AI-ovosti před minus po přepisu (kladné = blíž lidským textům). Přiblížení k autorovi = o kolik se rysy F0 pokračování přiblížily skutečnému pokračování autora. Ztráty a porušení významu jen u AI textů. Kappa = shoda běhů v tom, zda text má nález.
