# Benchmark skillů: dev-2

- Datum: 2026-11-15 17:05 +0100; sada: dev; textů: 90 (lidských 40, AI 50); běhů na text: 1
- Commit: `d47821e (neuložené změny)`; otisky skillů: unslop-cs `72bb07be240f`, unslop-cs-jadro-2 `81c212c5ce05`, anti-ai-slop-cz `d98a1147e447`, humanizer-czech `639d897a18a5`, bez-skillu `None`
- Model skillu: claude-sonnet-5-5 (effort medium; Claude Code 2.1.323, 2.1.325); soudce: claude-opus-5-5; normalizace: claude-haiku-5-5; modely z běhů: claude-sonnet-5-5
- Cena celkem: 12.84 USD; nevyhodnocené běhy: 0; převzaté běhy: 360

## unslop-cs proti unslop-cs-jadro-2: shodná kvalita, B je levnější o víc než 20 %

Rozhodovací vrstvy (bez aikoditex, cac, fictree); A − B, 95% interval z bootstrapu po shlucích. Kalibrace soudce: neprošla nebo neproběhla (A/B jen informativně)

- lidske_s_nalezem: horní mez +0.000 ≤ +0.030
- zmena_lidskych: horní mez +0.000 ≤ +0.020
- poruseni_vyznamu: soudce významu neprošel kalibrací, do rozhodnutí nevstupuje
- ztrata_cisel: horní mez +0.000 ≤ +0.020
- pridana_cisla: horní mez +0.000 ≤ +0.050
- lidske_s_nalezem: +0.000 [+0.000, +0.000]
- zmena_lidskych: +0.000 [+0.000, +0.000]
- ztrata_cisel: +0.000 [+0.000, +0.000]
- pridana_cisla: +0.000 [+0.000, +0.000]
- posun_skore: -0.013 [-0.045, +0.012]

K výkladu (do rozhodnutí nevstupuje):

- cena A/B: 1.3×
- lidské texty s nálezem: A 0.0%, B 0.0%
- plané poplachy (vysoká/střední): A 0.0%, B 0.0%
- plane_poplachy_vs A − B: +0.000 [+0.000, +0.000]
- citlivost_vs A − B: -0.038 [-0.130, +0.000]
- ai_s_nalezem A − B: -0.077 [-0.217, +0.000]
- ztrata_jmen A − B: -0.042 [-0.148, +0.000]
- pridana_jmena A − B: +0.000 [+0.000, +0.000]

## unslop-cs proti anti-ai-slop-cz: shodná kvalita, B je levnější o víc než 20 %

Rozhodovací vrstvy (bez aikoditex, cac, fictree); A − B, 95% interval z bootstrapu po shlucích. Kalibrace soudce: neprošla nebo neproběhla (A/B jen informativně)

- lidske_s_nalezem: horní mez -0.385 ≤ +0.030
- zmena_lidskych: horní mez -0.001 ≤ +0.020
- poruseni_vyznamu: soudce významu neprošel kalibrací, do rozhodnutí nevstupuje
- ztrata_cisel: horní mez +0.000 ≤ +0.020
- pridana_cisla: horní mez +0.000 ≤ +0.050
- lidske_s_nalezem: -0.577 [-0.783, -0.385]
- zmena_lidskych: -0.010 [-0.024, -0.001]
- ztrata_cisel: +0.000 [+0.000, +0.000]
- pridana_cisla: +0.000 [+0.000, +0.000]
- posun_skore: +0.011 [-0.008, +0.028]

K výkladu (do rozhodnutí nevstupuje):

- cena A/B: 1.4×
- lidské texty s nálezem: A 0.0%, B 57.7%
- plané poplachy (vysoká/střední): A 0.0%, B 11.5%
- plane_poplachy_vs A − B: -0.115 [-0.269, +0.000]
- citlivost_vs A − B: +0.000 [-0.130, +0.094]
- ai_s_nalezem A − B: -0.308 [-0.522, -0.143]
- ztrata_jmen A − B: -0.012 [-0.074, +0.051]
- pridana_jmena A − B: -0.192 [-0.385, +0.000]

## unslop-cs proti humanizer-czech: shodná kvalita, náklady nerozhodují

Rozhodovací vrstvy (bez aikoditex, cac, fictree); A − B, 95% interval z bootstrapu po shlucích. Kalibrace soudce: neprošla nebo neproběhla (A/B jen informativně)

- lidske_s_nalezem: horní mez -0.371 ≤ +0.030
- zmena_lidskych: horní mez -0.015 ≤ +0.020
- poruseni_vyznamu: soudce významu neprošel kalibrací, do rozhodnutí nevstupuje
- ztrata_cisel: horní mez +0.000 ≤ +0.020
- pridana_cisla: horní mez +0.000 ≤ +0.050
- lidske_s_nalezem: -0.538 [-0.783, -0.371]
- zmena_lidskych: -0.055 [-0.116, -0.015]
- ztrata_cisel: -0.004 [-0.014, +0.000]
- pridana_cisla: +0.000 [+0.000, +0.000]
- posun_skore: +0.005 [-0.027, +0.028]

K výkladu (do rozhodnutí nevstupuje):

- cena A/B: 1.0×
- lidské texty s nálezem: A 0.0%, B 53.8%
- plané poplachy (vysoká/střední): A 0.0%, B 19.2%
- plane_poplachy_vs A − B: -0.192 [-0.400, -0.057]
- citlivost_vs A − B: +0.038 [-0.154, +0.211]
- ai_s_nalezem A − B: -0.346 [-0.565, -0.172]
- ztrata_jmen A − B: -0.046 [-0.147, +0.083]
- pridana_jmena A − B: -0.077 [-0.174, +0.000]

## unslop-cs proti bez-skillu: shodná kvalita, B je levnější o víc než 20 %

Rozhodovací vrstvy (bez aikoditex, cac, fictree); A − B, 95% interval z bootstrapu po shlucích. Kalibrace soudce: neprošla nebo neproběhla (A/B jen informativně)

- lidske_s_nalezem: horní mez -0.130 ≤ +0.030
- zmena_lidskych: horní mez -0.004 ≤ +0.020
- poruseni_vyznamu: soudce významu neprošel kalibrací, do rozhodnutí nevstupuje
- ztrata_cisel: horní mez +0.000 ≤ +0.020
- pridana_cisla: horní mez +0.000 ≤ +0.050
- lidske_s_nalezem: -0.308 [-0.550, -0.130]
- zmena_lidskych: -0.024 [-0.053, -0.004]
- ztrata_cisel: -0.004 [-0.014, +0.000]
- pridana_cisla: +0.000 [+0.000, +0.000]
- posun_skore: -0.003 [-0.017, +0.011]

K výkladu (do rozhodnutí nevstupuje):

- cena A/B: 3.3×
- lidské texty s nálezem: A 0.0%, B 30.8%
- plané poplachy (vysoká/střední): A 0.0%, B 11.5%
- plane_poplachy_vs A − B: -0.115 [-0.269, +0.000]
- citlivost_vs A − B: -0.154 [-0.348, -0.034]
- ai_s_nalezem A − B: -0.346 [-0.565, -0.172]
- ztrata_jmen A − B: -0.002 [-0.014, +0.017]
- pridana_jmena A − B: -0.038 [-0.130, +0.000]

### Vrstva: rozhodovaci

| skill | lidských / AI | lidské s nálezem | AI s nálezem | AUC hustoty | plané poplachy v/s | citlivost v/s | AUC v/s | kappa | posun skóre AI | přiblížení k autorovi | ztráta čísel | přidaná čísla | ztráta jmen | přidaná jména | porušení významu | změna lidských | posun skóre lidských | bez verze | cena/text | kroků | čas s | zamítnutí | chyba nástroje |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| unslop-cs | 26 / 26 | 0 | 0.654 | 0.827 | 0 | 0.615 | 0.808 | – | 0.010 | -0.112 | 0.000 | 0 | 0.073 | 0 | – | 0.000 | -0.000 | 0 | 0.136 | 3.000 | 29.800 | 0 | 0 |
| unslop-cs-jadro-2 | 26 / 26 | 0 | 0.731 | 0.865 | 0 | 0.654 | 0.827 | – | 0.023 | -0.230 | 0.000 | 0 | 0.115 | 0 | – | 0.000 | -0.000 | 0 | 0.106 | 3.000 | 28.600 | 0 | 0 |
| anti-ai-slop-cz | 26 / 26 | 0.577 | 0.962 | 0.863 | 0.115 | 0.615 | 0.781 | – | -0.000 | -0.056 | 0.000 | 0 | 0.085 | 0.192 | – | 0.010 | -0.003 | 0 | 0.101 | 3.000 | 25.300 | 0 | 0 |
| humanizer-czech | 26 / 26 | 0.538 | 1 | 0.907 | 0.192 | 0.577 | 0.729 | – | 0.005 | -0.060 | 0.004 | 0 | 0.119 | 0.077 | – | 0.055 | -0.049 | 0 | 0.142 | 3.000 | 29.100 | 0 | 0 |
| bez-skillu | 26 / 26 | 0.308 | 1 | 0.926 | 0.115 | 0.769 | 0.854 | – | 0.013 | -0.108 | 0.004 | 0 | 0.075 | 0.038 | – | 0.024 | -0.006 | 0 | 0.041 | 1.000 | 26.050 | 0 | 0 |

### Vrstva: vse

| skill | lidských / AI | lidské s nálezem | AI s nálezem | AUC hustoty | plané poplachy v/s | citlivost v/s | AUC v/s | kappa | posun skóre AI | přiblížení k autorovi | ztráta čísel | přidaná čísla | ztráta jmen | přidaná jména | porušení významu | změna lidských | posun skóre lidských | bez verze | cena/text | kroků | čas s | zamítnutí | chyba nástroje |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| unslop-cs | 40 / 50 | 0.025 | 0.720 | 0.847 | 0.025 | 0.680 | 0.836 | – | -0.001 | -0.072 | 0.000 | 0.020 | 0.078 | 0.020 | – | 0.001 | 0.001 | 0 | 0.138 | 3.000 | 31.400 | 0 | 0 |
| unslop-cs-jadro-2 | 40 / 50 | 0.025 | 0.780 | 0.887 | 0 | 0.720 | 0.860 | – | 0.018 | -0.219 | 0.000 | 0 | 0.089 | 0 | – | 0.000 | -0.000 | 0 | 0.107 | 3.000 | 29.300 | 0 | 0 |
| anti-ai-slop-cz | 40 / 50 | 0.650 | 0.980 | 0.900 | 0.075 | 0.680 | 0.824 | – | 0.019 | -0.080 | 0.010 | 0 | 0.121 | 0.180 | – | 0.007 | -0.002 | 0 | 0.101 | 3.000 | 25.850 | 0 | 0 |
| humanizer-czech | 40 / 50 | 0.700 | 1 | 0.896 | 0.200 | 0.680 | 0.785 | – | 0.006 | -0.072 | 0.013 | 0.020 | 0.099 | 0.100 | – | 0.055 | -0.050 | 0 | 0.144 | 3.000 | 29.400 | 0 | 0 |
| bez-skillu | 40 / 50 | 0.425 | 1 | 0.936 | 0.125 | 0.780 | 0.855 | – | 0.018 | -0.101 | 0.008 | 0.040 | 0.104 | 0.140 | – | 0.019 | -0.003 | 0 | 0.041 | 1.000 | 26.600 | 0 | 0 |

### Vrstva: klasika

| skill | lidských / AI | lidské s nálezem | AI s nálezem | AUC hustoty | plané poplachy v/s | citlivost v/s | AUC v/s | kappa | posun skóre AI | přiblížení k autorovi | ztráta čísel | přidaná čísla | ztráta jmen | přidaná jména | porušení významu | změna lidských | posun skóre lidských | bez verze | cena/text | kroků | čas s | zamítnutí | chyba nástroje |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| unslop-cs | 14 / 14 | 0 | 0.714 | 0.857 | 0 | 0.714 | 0.857 | – | 0.016 | -0.048 | 0.000 | 0 | 0.010 | 0 | – | 0.000 | 0.000 | 0 | 0.136 | 3.000 | 31.450 | 0 | 0 |
| unslop-cs-jadro-2 | 14 / 14 | 0 | 0.714 | 0.857 | 0 | 0.714 | 0.857 | – | 0.042 | -0.061 | 0.000 | 0 | 0.010 | 0 | – | 0.000 | 0.000 | 0 | 0.104 | 3.000 | 27.750 | 0 | 0 |
| anti-ai-slop-cz | 14 / 14 | 0.286 | 0.929 | 0.903 | 0 | 0.643 | 0.821 | – | -0.007 | 0.155 | 0.000 | 0 | 0.074 | 0.214 | – | 0.000 | 0.000 | 0 | 0.100 | 3.000 | 25.050 | 0 | 0 |
| humanizer-czech | 14 / 14 | 0.143 | 1 | 1.000 | 0 | 0.500 | 0.750 | – | -0.008 | -0.053 | 0.000 | 0 | 0.131 | 0.071 | – | 0.002 | -0.004 | 0 | 0.140 | 3.000 | 26.800 | 0 | 0 |
| bez-skillu | 14 / 14 | 0 | 1 | 1.000 | 0 | 0.857 | 0.929 | – | 0.021 | -0.090 | 0.000 | 0 | 0.022 | 0 | – | 0.000 | 0.000 | 0 | 0.038 | 1.000 | 25.550 | 0 | 0 |

### Vrstva: cac

| skill | lidských / AI | lidské s nálezem | AI s nálezem | AUC hustoty | plané poplachy v/s | citlivost v/s | AUC v/s | kappa | posun skóre AI | přiblížení k autorovi | ztráta čísel | přidaná čísla | ztráta jmen | přidaná jména | porušení významu | změna lidských | posun skóre lidských | bez verze | cena/text | kroků | čas s | zamítnutí | chyba nástroje |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| unslop-cs | 7 / 7 | 0 | 0.714 | 0.857 | 0 | 0.714 | 0.857 | – | 0.002 | -0.167 | 0.000 | 0 | 0.000 | 0 | – | 0.000 | 0.003 | 0 | 0.137 | 3.000 | 30.750 | 0 | 0 |
| unslop-cs-jadro-2 | 7 / 7 | 0 | 0.857 | 0.929 | 0 | 0.857 | 0.929 | – | 0.001 | -0.366 | 0.000 | 0 | 0.000 | 0 | – | 0.000 | 0.000 | 0 | 0.108 | 3.000 | 30.350 | 0 | 0 |
| anti-ai-slop-cz | 7 / 7 | 0.714 | 1 | 0.959 | 0 | 0.857 | 0.929 | – | 0.025 | -0.408 | 0.000 | 0 | 0.200 | 0 | – | 0.000 | 0.000 | 0 | 0.102 | 3.000 | 27.300 | 0 | 0 |
| humanizer-czech | 7 / 7 | 1 | 1 | 0.878 | 0.143 | 0.714 | 0.776 | – | 0.005 | -0.216 | 0.000 | 0 | 0.000 | 0 | – | 0.089 | -0.096 | 0 | 0.144 | 3.000 | 31.200 | 0 | 0 |
| bez-skillu | 7 / 7 | 0.429 | 1 | 1.000 | 0 | 0.857 | 0.929 | – | 0.007 | -0.339 | 0.000 | 0.143 | 0.200 | 0 | – | 0.001 | 0.000 | 0 | 0.039 | 1.000 | 25.150 | 0 | 0 |

### Vrstva: fictree

| skill | lidských / AI | lidské s nálezem | AI s nálezem | AUC hustoty | plané poplachy v/s | citlivost v/s | AUC v/s | kappa | posun skóre AI | přiblížení k autorovi | ztráta čísel | přidaná čísla | ztráta jmen | přidaná jména | porušení významu | změna lidských | posun skóre lidských | bez verze | cena/text | kroků | čas s | zamítnutí | chyba nástroje |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| unslop-cs | 7 / 7 | 0.143 | 0.857 | 0.837 | 0.143 | 0.714 | 0.837 | – | -0.001 | 0.081 | – | 0 | 0.042 | 0 | – | 0.004 | 0.004 | 0 | 0.139 | 3.000 | 31.200 | 0 | 0 |
| unslop-cs-jadro-2 | 7 / 7 | 0.143 | 0.857 | 0.918 | 0 | 0.714 | 0.857 | – | -0.001 | -0.104 | – | 0 | 0.042 | 0 | – | 0.002 | -0.000 | 0 | 0.105 | 3.000 | 27.550 | 0 | 0 |
| anti-ai-slop-cz | 7 / 7 | 0.857 | 1 | 1.000 | 0 | 0.571 | 0.786 | – | -0.002 | 0.058 | – | 0 | 0.083 | 0.286 | – | 0.000 | -0.000 | 0 | 0.099 | 3.000 | 25.250 | 0 | 0 |
| humanizer-czech | 7 / 7 | 1 | 1 | 0.918 | 0.286 | 0.857 | 0.888 | – | -0.002 | -0.014 | – | 0 | 0.042 | 0 | – | 0.020 | -0.009 | 0 | 0.141 | 3.000 | 28.200 | 0 | 0 |
| bez-skillu | 7 / 7 | 0.857 | 1 | 0.980 | 0.286 | 0.714 | 0.755 | – | -0.001 | 0.058 | – | 0 | 0.042 | 0.286 | – | 0.019 | 0.005 | 0 | 0.041 | 1.000 | 26.950 | 0 | 0 |

### Vrstva: wiki

| skill | lidských / AI | lidské s nálezem | AI s nálezem | AUC hustoty | plané poplachy v/s | citlivost v/s | AUC v/s | kappa | posun skóre AI | přiblížení k autorovi | ztráta čísel | přidaná čísla | ztráta jmen | přidaná jména | porušení významu | změna lidských | posun skóre lidských | bez verze | cena/text | kroků | čas s | zamítnutí | chyba nástroje |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| unslop-cs | 7 / 7 | 0 | 0.429 | 0.714 | 0 | 0.286 | 0.643 | – | -0.010 | -0.166 | 0.000 | 0 | 0.143 | 0 | – | 0.000 | -0.000 | 0 | 0.137 | 3.000 | 27.000 | 0 | 0 |
| unslop-cs-jadro-2 | 7 / 7 | 0 | 0.571 | 0.786 | 0 | 0.429 | 0.714 | – | -0.002 | -0.484 | 0.000 | 0 | 0.143 | 0 | – | 0.000 | -0.000 | 0 | 0.108 | 3.000 | 29.650 | 0 | 0 |
| anti-ai-slop-cz | 7 / 7 | 1 | 1 | 0.592 | 0.429 | 0.429 | 0.592 | – | -0.011 | -0.364 | 0.000 | 0 | 0.147 | 0.143 | – | 0.036 | -0.012 | 0 | 0.105 | 3.000 | 27.050 | 0 | 0 |
| humanizer-czech | 7 / 7 | 1 | 1 | 0.612 | 0.714 | 0.571 | 0.531 | – | -0.027 | -0.065 | 0.010 | 0 | 0.111 | 0 | – | 0.187 | -0.173 | 0 | 0.149 | 3.000 | 33.200 | 0 | 0 |
| bez-skillu | 7 / 7 | 1 | 1 | 0.551 | 0.429 | 0.571 | 0.653 | – | -0.000 | -0.178 | 0.010 | 0 | 0.146 | 0 | – | 0.088 | -0.021 | 0 | 0.047 | 1.000 | 28.500 | 0 | 0 |

### Vrstva: uredni

| skill | lidských / AI | lidské s nálezem | AI s nálezem | AUC hustoty | plané poplachy v/s | citlivost v/s | AUC v/s | kappa | posun skóre AI | přiblížení k autorovi | ztráta čísel | přidaná čísla | ztráta jmen | přidaná jména | porušení významu | změna lidských | posun skóre lidských | bez verze | cena/text | kroků | čas s | zamítnutí | chyba nástroje |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| unslop-cs | 5 / 5 | 0 | 0.800 | 0.900 | 0 | 0.800 | 0.900 | – | 0.021 | -0.146 | 0.000 | 0 | 0.125 | 0 | – | 0.000 | -0.000 | 0 | 0.137 | 3.000 | 29.450 | 0 | 0 |
| unslop-cs-jadro-2 | 5 / 5 | 0 | 1 | 1.000 | 0 | 0.800 | 0.900 | – | 0.005 | -0.175 | 0.000 | 0 | 0.325 | 0 | – | 0.000 | -0.000 | 0 | 0.108 | 3.000 | 29.950 | 0 | 0 |
| anti-ai-slop-cz | 5 / 5 | 0.800 | 1 | 1.000 | 0 | 0.800 | 0.900 | – | 0.032 | 0.003 | 0.000 | 0 | 0.025 | 0.200 | – | 0.002 | 0.002 | 0 | 0.099 | 3.000 | 24.000 | 0 | 0 |
| humanizer-czech | 5 / 5 | 1 | 1 | 1.000 | 0 | 0.800 | 0.900 | – | 0.086 | -0.065 | 0.000 | 0 | 0.100 | 0.200 | – | 0.022 | -0.001 | 0 | 0.142 | 3.000 | 28.950 | 0 | 0 |
| bez-skillu | 5 / 5 | 0.200 | 1 | 1.000 | 0 | 0.800 | 0.900 | – | 0.010 | -0.046 | 0.000 | 0 | 0.100 | 0.200 | – | 0.000 | -0.000 | 0 | 0.034 | 1.000 | 21.450 | 0 | 0 |

### Vrstva: aikoditex

| skill | lidských / AI | lidské s nálezem | AI s nálezem | AUC hustoty | plané poplachy v/s | citlivost v/s | AUC v/s | kappa | posun skóre AI | přiblížení k autorovi | ztráta čísel | přidaná čísla | ztráta jmen | přidaná jména | porušení významu | změna lidských | posun skóre lidských | bez verze | cena/text | kroků | čas s | zamítnutí | chyba nástroje |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| unslop-cs | 0 / 10 | – | 0.800 | – | – | 0.800 | – | – | -0.034 | – | 0.000 | 0.100 | 0.150 | 0.100 | – | – | – | 0 | 0.157 | 3.000 | 42.850 | 0 | 0 |
| unslop-cs-jadro-2 | 0 / 10 | – | 0.800 | – | – | 0.800 | – | – | 0.031 | – | 0.000 | 0 | 0.100 | 0 | – | – | – | 0 | 0.130 | 3.000 | 41.400 | 0 | 0 |
| anti-ai-slop-cz | 0 / 10 | – | 1 | – | – | 0.800 | – | – | 0.079 | – | 0.050 | 0 | 0.189 | 0.200 | – | – | – | 0 | 0.104 | 3.000 | 27.700 | 0 | 0 |
| humanizer-czech | 0 / 10 | – | 1 | – | – | 0.800 | – | – | 0.013 | – | 0.050 | 0.100 | 0.136 | 0.300 | – | – | – | 0 | 0.147 | 3.000 | 32.250 | 0 | 0 |
| bez-skillu | 0 / 10 | – | 1 | – | – | 0.800 | – | – | 0.054 | – | 0.025 | 0.100 | 0.164 | 0.400 | – | – | – | 0 | 0.057 | 1.000 | 35.500 | 0 | 0 |

Lidské / AI s nálezem = podíl lidských / AI textů s aspoň jedním nálezem jakékoli závažnosti (nezávisí na tom, jak skill štítkuje závažnost); AUC hustoty = odlišení AI a lidských textů podle počtu všech nálezů na 1000 slov. Plané poplachy v/s a citlivost v/s = totéž jen s nálezy vysoké nebo střední závažnosti. Přidaná čísla / jména = podíl přepisů AI textů s aspoň jedním číslem či datem / vlastním jménem, které v originálu není. Zamítnutí a chyba nástroje = podíl běhů, kde skill narazil na zamítnutý nebo chybný nástroj (chyba nástroje se zaznamenává od 2026-11-13). Posun skóre = skóre AI-ovosti před minus po přepisu (kladné = blíž lidským textům). Přiblížení k autorovi = o kolik se rysy F0 pokračování přiblížily skutečnému pokračování autora. Ztráty a porušení významu jen u AI textů. Kappa = shoda běhů v tom, zda text má nález.
