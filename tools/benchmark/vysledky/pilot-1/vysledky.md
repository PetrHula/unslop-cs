# Benchmark skillů: pilot-1

- Datum: 2026-11-11 14:01 +0100; sada: dev; textů: 10 (lidských 5, AI 5); běhů na text: 1
- Commit: `c8340c4`; otisky skillů: unslop-cs `0048df92d2a1`, anti-ai-slop-cz `d98a1147e447`, humanizer-czech `639d897a18a5`, bez-skillu `None`
- Model skillu: claude-sonnet-5-5; soudce: claude-opus-5-5; normalizace: claude-haiku-5-5; modely z běhů: claude-sonnet-5-5
- Cena celkem: 7.86 USD; nevyhodnocené běhy: 0

## unslop-cs proti anti-ai-slop-cz: shodná kvalita, B je levnější o víc než 20 %

Rozhodovací vrstvy (bez aikoditex, cac, fictree); A − B, 95% interval z bootstrapu po shlucích. Kalibrace soudce: neprošla nebo neproběhla (A/B jen informativně)

- plane_poplachy: horní mez +0.000 ≤ +0.030
- poruseni_vyznamu: horní mez +0.000 ≤ +0.050
- ztrata_cisel: horní mez +0.000 ≤ +0.020
- plane_poplachy: +0.000 [+0.000, +0.000]
- poruseni_vyznamu: +0.000 [+0.000, +0.000]
- ztrata_cisel: +0.000 [+0.000, +0.000]
- posun_skore: -0.024 [-0.069, +0.000]
- vyhry_ab: -0.250 [-1.000, +0.500]

## unslop-cs proti humanizer-czech: shodná kvalita, B je levnější o víc než 20 %

Rozhodovací vrstvy (bez aikoditex, cac, fictree); A − B, 95% interval z bootstrapu po shlucích. Kalibrace soudce: neprošla nebo neproběhla (A/B jen informativně)

- plane_poplachy: horní mez +0.000 ≤ +0.030
- poruseni_vyznamu: horní mez +0.000 ≤ +0.050
- ztrata_cisel: horní mez +0.000 ≤ +0.020
- plane_poplachy: +0.000 [+0.000, +0.000]
- poruseni_vyznamu: -0.500 [-1.000, +0.000]
- ztrata_cisel: +0.000 [+0.000, +0.000]
- posun_skore: -0.146 [-0.408, +0.000]
- vyhry_ab: -1.000 [-1.000, -1.000]

## unslop-cs proti bez-skillu: shodná kvalita, B je levnější o víc než 20 %

Rozhodovací vrstvy (bez aikoditex, cac, fictree); A − B, 95% interval z bootstrapu po shlucích. Kalibrace soudce: neprošla nebo neproběhla (A/B jen informativně)

- plane_poplachy: horní mez +0.000 ≤ +0.030
- poruseni_vyznamu: horní mez +0.000 ≤ +0.050
- ztrata_cisel: horní mez +0.000 ≤ +0.020
- plane_poplachy: -0.333 [-1.000, +0.000]
- poruseni_vyznamu: +0.000 [+0.000, +0.000]
- ztrata_cisel: +0.000 [+0.000, +0.000]
- posun_skore: -0.068 [-0.204, +0.002]
- vyhry_ab: -0.250 [-1.000, +0.500]

### Vrstva: rozhodovaci

| skill | lidských / AI | plané poplachy | AUC hustoty | kappa | posun skóre AI | přiblížení k autorovi | ztráta čísel | ztráta jmen | porušení významu | změna lidských | posun skóre lidských | bez verze | cena/text | kroků | čas s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| unslop-cs | 3 / 4 | 0 | 0.625 | – | -0.000 | 0.000 | 0.000 | 0.000 | 0.250 | 0.003 | -0.002 | 0 | 0.296 | 7 | 40.100 |
| anti-ai-slop-cz | 3 / 4 | 0 | 0.625 | – | 0.024 | -0.191 | 0.000 | 0.125 | 0.250 | 0.037 | -0.002 | 0 | 0.107 | 3 | 27.700 |
| humanizer-czech | 3 / 4 | 0 | 0.875 | – | 0.146 | -0.184 | 0.000 | 0.137 | 0.750 | 0.020 | -0.007 | 0 | 0.148 | 3 | 32.100 |
| bez-skillu | 3 / 4 | 0.333 | 0.500 | – | 0.068 | -0.858 | 0.000 | 0.024 | 0.250 | 0.021 | -0.007 | 0 | 0.043 | 1 | 25.500 |

### Vrstva: vse

| skill | lidských / AI | plané poplachy | AUC hustoty | kappa | posun skóre AI | přiblížení k autorovi | ztráta čísel | ztráta jmen | porušení významu | změna lidských | posun skóre lidských | bez verze | cena/text | kroků | čas s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| unslop-cs | 5 / 5 | 0 | 0.700 | – | -0.006 | 0.000 | 0.000 | 0.000 | 0.200 | 0.005 | -0.002 | 0 | 0.297 | 7.000 | 43.550 |
| anti-ai-slop-cz | 5 / 5 | 0.200 | 0.640 | – | 0.013 | -0.191 | 0.250 | 0.100 | 0.400 | 0.027 | 0.005 | 0 | 0.104 | 3.000 | 27.600 |
| humanizer-czech | 5 / 5 | 0.200 | 0.800 | – | 0.110 | -0.184 | 0.000 | 0.110 | 0.800 | 0.024 | -0.016 | 0 | 0.147 | 3.000 | 31.000 |
| bez-skillu | 5 / 5 | 0.400 | 0.580 | – | 0.050 | -0.858 | 0.000 | 0.019 | 0.400 | 0.032 | -0.013 | 0 | 0.042 | 1.000 | 25.100 |

### Vrstva: klasika

| skill | lidských / AI | plané poplachy | AUC hustoty | kappa | posun skóre AI | přiblížení k autorovi | ztráta čísel | ztráta jmen | porušení významu | změna lidských | posun skóre lidských | bez verze | cena/text | kroků | čas s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| unslop-cs | 1 / 1 | 0 | 1.000 | – | -0.000 | – | – | 0.000 | 1 | 0.000 | 0.000 | 0 | 0.259 | 6.500 | 47.300 |
| anti-ai-slop-cz | 1 / 1 | 0 | 1.000 | – | -0.000 | – | – | 0.500 | 1 | 0.000 | 0.000 | 0 | 0.111 | 3.000 | 32.200 |
| humanizer-czech | 1 / 1 | 0 | 1.000 | – | -0.000 | – | – | 0.500 | 1 | 0.002 | 0.000 | 0 | 0.153 | 3.000 | 35.200 |
| bez-skillu | 1 / 1 | 0 | 1.000 | – | -0.000 | – | – | 0.000 | 1 | 0.000 | 0.000 | 0 | 0.053 | 1.000 | 33.650 |

### Vrstva: cac

| skill | lidských / AI | plané poplachy | AUC hustoty | kappa | posun skóre AI | přiblížení k autorovi | ztráta čísel | ztráta jmen | porušení významu | změna lidských | posun skóre lidských | bez verze | cena/text | kroků | čas s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| unslop-cs | 1 / 0 | 0 | – | – | – | – | – | – | – | 0.000 | 0.000 | 0 | 0.293 | 7 | 39.200 |
| anti-ai-slop-cz | 1 / 0 | 0 | – | – | – | – | – | – | – | 0.000 | 0.000 | 0 | 0.100 | 3 | 23.100 |
| humanizer-czech | 1 / 0 | 0 | – | – | – | – | – | – | – | 0.000 | 0.000 | 0 | 0.143 | 3 | 27.600 |
| bez-skillu | 1 / 0 | 0 | – | – | – | – | – | – | – | 0.000 | 0.000 | 0 | 0.037 | 1 | 23.400 |

### Vrstva: fictree

| skill | lidských / AI | plané poplachy | AUC hustoty | kappa | posun skóre AI | přiblížení k autorovi | ztráta čísel | ztráta jmen | porušení významu | změna lidských | posun skóre lidských | bez verze | cena/text | kroků | čas s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| unslop-cs | 1 / 0 | 0 | – | – | – | – | – | – | – | 0.016 | -0.006 | 0 | 0.298 | 7 | 47.000 |
| anti-ai-slop-cz | 1 / 0 | 1 | – | – | – | – | – | – | – | 0.023 | 0.031 | 0 | 0.103 | 3 | 27.500 |
| humanizer-czech | 1 / 0 | 1 | – | – | – | – | – | – | – | 0.058 | -0.056 | 0 | 0.152 | 3 | 33.800 |
| bez-skillu | 1 / 0 | 1 | – | – | – | – | – | – | – | 0.098 | -0.044 | 0 | 0.055 | 1 | 34.900 |

### Vrstva: wiki

| skill | lidských / AI | plané poplachy | AUC hustoty | kappa | posun skóre AI | přiblížení k autorovi | ztráta čísel | ztráta jmen | porušení významu | změna lidských | posun skóre lidských | bez verze | cena/text | kroků | čas s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| unslop-cs | 1 / 2 | 0 | 0.500 | – | 0.000 | 0.000 | 0.000 | 0.000 | 0 | 0.004 | -0.000 | 0 | 0.296 | 7 | 37.800 |
| anti-ai-slop-cz | 1 / 2 | 0 | 0.500 | – | 0.046 | -0.232 | 0.000 | 0.000 | 0 | 0.110 | -0.005 | 0 | 0.108 | 3 | 27.700 |
| humanizer-czech | 1 / 2 | 0 | 1.000 | – | 0.291 | -0.367 | 0.000 | 0.024 | 1 | 0.058 | -0.022 | 0 | 0.151 | 3 | 32.100 |
| bez-skillu | 1 / 2 | 1 | 0.000 | – | 0.135 | -1.716 | 0.000 | 0.048 | 0 | 0.063 | -0.020 | 0 | 0.049 | 1 | 28.800 |

### Vrstva: uredni

| skill | lidských / AI | plané poplachy | AUC hustoty | kappa | posun skóre AI | přiblížení k autorovi | ztráta čísel | ztráta jmen | porušení významu | změna lidských | posun skóre lidských | bez verze | cena/text | kroků | čas s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| unslop-cs | 1 / 1 | 0 | 0.500 | – | 0.000 | 0.000 | 0.000 | 0.000 | 0 | 0.006 | -0.006 | 0 | 0.299 | 7.000 | 46.100 |
| anti-ai-slop-cz | 1 / 1 | 0 | 0.500 | – | 0.003 | -0.150 | 0.000 | 0.000 | 0 | 0.000 | 0.000 | 0 | 0.100 | 3.000 | 24.600 |
| humanizer-czech | 1 / 1 | 0 | 0.500 | – | -0.001 | -0.001 | 0.000 | 0.000 | 0 | 0.000 | 0.000 | 0 | 0.141 | 3.000 | 27.350 |
| bez-skillu | 1 / 1 | 0 | 0.500 | – | 0.000 | 0.000 | 0.000 | 0.000 | 0 | 0.000 | 0.000 | 0 | 0.036 | 1.000 | 21.850 |

### Vrstva: aikoditex

| skill | lidských / AI | plané poplachy | AUC hustoty | kappa | posun skóre AI | přiblížení k autorovi | ztráta čísel | ztráta jmen | porušení významu | změna lidských | posun skóre lidských | bez verze | cena/text | kroků | čas s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| unslop-cs | 0 / 1 | – | – | – | -0.029 | – | 0.000 | 0.000 | 0 | – | – | 0 | 0.342 | 7 | 68.600 |
| anti-ai-slop-cz | 0 / 1 | – | – | – | -0.029 | – | 1.000 | 0.000 | 1 | – | – | 0 | 0.104 | 3 | 28.100 |
| humanizer-czech | 0 / 1 | – | – | – | -0.030 | – | 0.000 | 0.000 | 1 | – | – | 0 | 0.140 | 3 | 24.100 |
| bez-skillu | 0 / 1 | – | – | – | -0.019 | – | 0.000 | 0.000 | 1 | – | – | 0 | 0.034 | 1 | 21.800 |

Plané poplachy = podíl lidských textů s aspoň jedním nálezem vysoké nebo střední závažnosti. Posun skóre = skóre AI-ovosti před minus po přepisu (kladné = blíž lidským textům). Přiblížení k autorovi = o kolik se rysy F0 pokračování přiblížily skutečnému pokračování autora. Ztráty a porušení významu jen u AI textů. Kappa = shoda běhů v tom, zda text má nález.
