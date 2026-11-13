# Benchmark skillů: test-1

- Datum: 2026-11-13 14:13 +0100; sada: test; textů: 216 (lidských 93, AI 123); běhů na text: 1
- Commit: `54cb082`; otisky skillů: unslop-cs `0048df92d2a1`, anti-ai-slop-cz `d98a1147e447`, humanizer-czech `639d897a18a5`, bez-skillu `None`
- Model skillu: claude-sonnet-5-5; soudce: claude-opus-5-5; normalizace: claude-haiku-5-5; modely z běhů: claude-sonnet-5-5
- Cena celkem: 126.98 USD; nevyhodnocené běhy: 0

## unslop-cs proti anti-ai-slop-cz: shodná kvalita, B je levnější o víc než 20 %

Rozhodovací vrstvy (bez aikoditex, cac, fictree); A − B, 95% interval z bootstrapu po shlucích. Kalibrace soudce: neprošla nebo neproběhla (A/B jen informativně)

- plane_poplachy: horní mez +0.000 ≤ +0.030
- poruseni_vyznamu: soudce významu neprošel kalibrací, do rozhodnutí nevstupuje
- ztrata_cisel: horní mez +0.012 ≤ +0.020
- plane_poplachy: -0.061 [-0.145, +0.000]
- ztrata_cisel: -0.025 [-0.074, +0.012]
- posun_skore: -0.014 [-0.041, +0.001]

## unslop-cs proti humanizer-czech: shodná kvalita, B je levnější o víc než 20 %

Rozhodovací vrstvy (bez aikoditex, cac, fictree); A − B, 95% interval z bootstrapu po shlucích. Kalibrace soudce: neprošla nebo neproběhla (A/B jen informativně)

- plane_poplachy: horní mez -0.113 ≤ +0.030
- poruseni_vyznamu: soudce významu neprošel kalibrací, do rozhodnutí nevstupuje
- ztrata_cisel: horní mez +0.019 ≤ +0.020
- plane_poplachy: -0.212 [-0.340, -0.113]
- ztrata_cisel: +0.006 [+0.000, +0.019]
- posun_skore: -0.000 [-0.025, +0.038]

## unslop-cs proti bez-skillu: shodná kvalita, B je levnější o víc než 20 %

Rozhodovací vrstvy (bez aikoditex, cac, fictree); A − B, 95% interval z bootstrapu po shlucích. Kalibrace soudce: neprošla nebo neproběhla (A/B jen informativně)

- plane_poplachy: horní mez -0.062 ≤ +0.030
- poruseni_vyznamu: soudce významu neprošel kalibrací, do rozhodnutí nevstupuje
- ztrata_cisel: horní mez +0.019 ≤ +0.020
- plane_poplachy: -0.152 [-0.254, -0.062]
- ztrata_cisel: -0.006 [-0.037, +0.019]
- posun_skore: -0.013 [-0.031, -0.001]

### Vrstva: rozhodovaci

| skill | lidských / AI | plané poplachy | AUC hustoty | kappa | posun skóre AI | přiblížení k autorovi | ztráta čísel | ztráta jmen | porušení významu | změna lidských | posun skóre lidských | bez verze | cena/text | kroků | čas s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| unslop-cs | 66 / 66 | 0.015 | 0.738 | – | -0.006 | -0.128 | 0.012 | 0.045 | – | 0.010 | -0.003 | 0 | 0.294 | 7.000 | 44.200 |
| anti-ai-slop-cz | 66 / 66 | 0.076 | 0.794 | – | 0.008 | -0.170 | 0.037 | 0.103 | – | 0.018 | -0.009 | 0 | 0.100 | 3.000 | 25.800 |
| humanizer-czech | 66 / 66 | 0.227 | 0.797 | – | -0.005 | -0.158 | 0.006 | 0.069 | – | 0.054 | -0.027 | 0 | 0.142 | 3.000 | 29.900 |
| bez-skillu | 66 / 66 | 0.167 | 0.852 | – | 0.008 | -0.272 | 0.019 | 0.118 | – | 0.014 | -0.016 | 0 | 0.041 | 1.000 | 24.750 |

### Vrstva: vse

| skill | lidských / AI | plané poplachy | AUC hustoty | kappa | posun skóre AI | přiblížení k autorovi | ztráta čísel | ztráta jmen | porušení významu | změna lidských | posun skóre lidských | bez verze | cena/text | kroků | čas s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| unslop-cs | 93 / 123 | 0.011 | 0.761 | – | -0.015 | -0.155 | 0.007 | 0.041 | – | 0.008 | -0.001 | 0 | 0.296 | 7.000 | 45.900 |
| anti-ai-slop-cz | 93 / 123 | 0.054 | 0.826 | – | -0.000 | -0.274 | 0.020 | 0.106 | – | 0.013 | -0.006 | 0 | 0.101 | 3.000 | 26.400 |
| humanizer-czech | 93 / 123 | 0.172 | 0.831 | – | -0.010 | -0.175 | 0.024 | 0.096 | – | 0.039 | -0.018 | 0 | 0.143 | 3.000 | 29.650 |
| bez-skillu | 93 / 123 | 0.118 | 0.855 | – | -0.003 | -0.300 | 0.037 | 0.111 | – | 0.010 | -0.011 | 0 | 0.040 | 1.000 | 25.400 |

### Vrstva: klasika

| skill | lidských / AI | plané poplachy | AUC hustoty | kappa | posun skóre AI | přiblížení k autorovi | ztráta čísel | ztráta jmen | porušení významu | změna lidských | posun skóre lidských | bez verze | cena/text | kroků | čas s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| unslop-cs | 36 / 36 | 0 | 0.736 | – | 0.001 | -0.001 | 0.000 | 0.050 | – | 0.000 | -0.000 | 0 | 0.290 | 7.000 | 42.000 |
| anti-ai-slop-cz | 36 / 36 | 0 | 0.833 | – | -0.001 | 0.054 | 0.250 | 0.135 | – | 0.000 | -0.000 | 0 | 0.098 | 3.000 | 25.750 |
| humanizer-czech | 36 / 36 | 0 | 0.819 | – | 0.014 | -0.055 | 0.000 | 0.058 | – | 0.001 | 0.002 | 0 | 0.140 | 3.000 | 28.400 |
| bez-skillu | 36 / 36 | 0.056 | 0.883 | – | 0.002 | -0.138 | 0.000 | 0.142 | – | 0.002 | -0.002 | 0 | 0.039 | 1.000 | 23.950 |

### Vrstva: cac

| skill | lidských / AI | plané poplachy | AUC hustoty | kappa | posun skóre AI | přiblížení k autorovi | ztráta čísel | ztráta jmen | porušení významu | změna lidských | posun skóre lidských | bez verze | cena/text | kroků | čas s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| unslop-cs | 18 / 18 | 0 | 0.639 | – | 0.010 | -0.130 | 0.000 | 0.000 | – | 0.001 | 0.000 | 0 | 0.293 | 7.000 | 44.150 |
| anti-ai-slop-cz | 18 / 18 | 0 | 0.722 | – | 0.006 | -0.495 | 0.000 | 0.014 | – | 0.000 | -0.000 | 0 | 0.100 | 3.000 | 26.350 |
| humanizer-czech | 18 / 18 | 0 | 0.750 | – | 0.020 | -0.254 | 0.000 | 0.036 | – | 0.000 | -0.000 | 0 | 0.142 | 3.000 | 28.050 |
| bez-skillu | 18 / 18 | 0 | 0.694 | – | 0.037 | -0.344 | 0.000 | 0.020 | – | 0.001 | 0.000 | 0 | 0.037 | 1.000 | 23.650 |

### Vrstva: fictree

| skill | lidských / AI | plané poplachy | AUC hustoty | kappa | posun skóre AI | přiblížení k autorovi | ztráta čísel | ztráta jmen | porušení významu | změna lidských | posun skóre lidských | bez verze | cena/text | kroků | čas s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| unslop-cs | 9 / 9 | 0 | 0.722 | – | -0.002 | -0.428 | 0.000 | 0.000 | – | 0.002 | 0.006 | 0 | 0.291 | 7.000 | 42.450 |
| anti-ai-slop-cz | 9 / 9 | 0 | 0.833 | – | -0.002 | -0.421 | 0.000 | 0.018 | – | 0.002 | 0.007 | 0 | 0.098 | 3.000 | 25.300 |
| humanizer-czech | 9 / 9 | 0.111 | 0.815 | – | 0.005 | -0.080 | 0.000 | 0.080 | – | 0.002 | 0.007 | 0 | 0.140 | 3.000 | 26.950 |
| bez-skillu | 9 / 9 | 0 | 0.833 | – | -0.004 | -0.379 | 0.000 | 0.000 | – | 0.000 | 0.000 | 0 | 0.038 | 1.000 | 25.050 |

### Vrstva: wiki

| skill | lidských / AI | plané poplachy | AUC hustoty | kappa | posun skóre AI | přiblížení k autorovi | ztráta čísel | ztráta jmen | porušení významu | změna lidských | posun skóre lidských | bez verze | cena/text | kroků | čas s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| unslop-cs | 18 / 18 | 0.056 | 0.707 | – | -0.022 | -0.158 | 0.000 | 0.000 | – | 0.027 | -0.006 | 0 | 0.300 | 7.000 | 45.600 |
| anti-ai-slop-cz | 18 / 18 | 0.222 | 0.657 | – | 0.016 | -0.174 | 0.024 | 0.035 | – | 0.061 | -0.035 | 0 | 0.102 | 3.000 | 26.450 |
| humanizer-czech | 18 / 18 | 0.556 | 0.654 | – | -0.058 | -0.247 | 0.000 | 0.060 | – | 0.122 | -0.073 | 0 | 0.148 | 3.000 | 31.950 |
| bez-skillu | 18 / 18 | 0.444 | 0.750 | – | 0.001 | -0.403 | 0.024 | 0.072 | – | 0.043 | -0.055 | 0 | 0.044 | 1.000 | 26.350 |

### Vrstva: uredni

| skill | lidských / AI | plané poplachy | AUC hustoty | kappa | posun skóre AI | přiblížení k autorovi | ztráta čísel | ztráta jmen | porušení významu | změna lidských | posun skóre lidských | bez verze | cena/text | kroků | čas s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| unslop-cs | 12 / 12 | 0 | 0.792 | – | -0.001 | -0.425 | 0.030 | 0.125 | – | 0.015 | -0.005 | 0 | 0.302 | 7.000 | 47.350 |
| anti-ai-slop-cz | 12 / 12 | 0.083 | 0.865 | – | 0.025 | -0.771 | 0.015 | 0.125 | – | 0.006 | 0.003 | 0 | 0.100 | 3.000 | 25.150 |
| humanizer-czech | 12 / 12 | 0.417 | 0.931 | – | 0.016 | -0.297 | 0.015 | 0.125 | – | 0.112 | -0.045 | 0 | 0.142 | 3.000 | 27.200 |
| bez-skillu | 12 / 12 | 0.083 | 0.882 | – | 0.034 | -0.431 | 0.015 | 0.125 | – | 0.006 | -0.001 | 0 | 0.039 | 1.000 | 22.250 |

### Vrstva: aikoditex

| skill | lidských / AI | plané poplachy | AUC hustoty | kappa | posun skóre AI | přiblížení k autorovi | ztráta čísel | ztráta jmen | porušení významu | změna lidských | posun skóre lidských | bez verze | cena/text | kroků | čas s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| unslop-cs | 0 / 30 | – | – | – | -0.054 | – | 0.000 | 0.068 | – | – | – | 0 | 0.330 | 7.000 | 69.000 |
| anti-ai-slop-cz | 0 / 30 | – | – | – | -0.021 | – | 0.000 | 0.188 | – | – | – | 0 | 0.108 | 3.000 | 30.700 |
| humanizer-czech | 0 / 30 | – | – | – | -0.045 | – | 0.077 | 0.191 | – | – | – | 0 | 0.152 | 3.000 | 35.700 |
| bez-skillu | 0 / 30 | – | – | – | -0.051 | – | 0.103 | 0.179 | – | – | – | 0 | 0.062 | 1.000 | 38.800 |

Plané poplachy = podíl lidských textů s aspoň jedním nálezem vysoké nebo střední závažnosti. Posun skóre = skóre AI-ovosti před minus po přepisu (kladné = blíž lidským textům). Přiblížení k autorovi = o kolik se rysy F0 pokračování přiblížily skutečnému pokračování autora. Ztráty a porušení významu jen u AI textů. Kappa = shoda běhů v tom, zda text má nález.
