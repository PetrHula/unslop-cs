# Benchmark skillů: kalibrace-1

- Datum: 2026-11-11 14:30 +0100; sada: dev; textů: 20 (lidských 0, AI 20); běhů na text: 1
- Commit: `45201e4`; otisky skillů: unslop-cs `0048df92d2a1`, anti-ai-slop-cz `d98a1147e447`, humanizer-czech `639d897a18a5`, bez-skillu `None`
- Model skillu: claude-sonnet-5-5; soudce: claude-opus-5-5; normalizace: claude-haiku-5-5; modely z běhů: claude-sonnet-5-5
- Cena celkem: 19.35 USD; nevyhodnocené běhy: 0

## unslop-cs proti anti-ai-slop-cz: A není lepší (zhoršuje plané poplachy nebo zachování významu)

Rozhodovací vrstvy (bez aikoditex, cac, fictree); A − B, 95% interval z bootstrapu po shlucích. Kalibrace soudce: neprošla nebo neproběhla (A/B jen informativně)

- plane_poplachy: chybí data
- poruseni_vyznamu: horní mez +0.000 ≤ +0.050
- ztrata_cisel: horní mez +0.000 ≤ +0.020
- poruseni_vyznamu: -0.231 [-0.462, +0.000]
- ztrata_cisel: +0.000 [+0.000, +0.000]
- posun_skore: +0.007 [-0.005, +0.025]
- vyhry_ab: +0.000 [-0.500, +0.429]

## unslop-cs proti humanizer-czech: A není lepší (zhoršuje plané poplachy nebo zachování významu)

Rozhodovací vrstvy (bez aikoditex, cac, fictree); A − B, 95% interval z bootstrapu po shlucích. Kalibrace soudce: neprošla nebo neproběhla (A/B jen informativně)

- plane_poplachy: chybí data
- poruseni_vyznamu: horní mez +0.000 ≤ +0.050
- ztrata_cisel: horní mez +0.000 ≤ +0.020
- poruseni_vyznamu: -0.231 [-0.462, +0.000]
- ztrata_cisel: +0.000 [+0.000, +0.000]
- posun_skore: +0.003 [-0.000, +0.008]
- vyhry_ab: +0.077 [-0.400, +0.455]

## unslop-cs proti bez-skillu: A není lepší (zhoršuje plané poplachy nebo zachování významu)

Rozhodovací vrstvy (bez aikoditex, cac, fictree); A − B, 95% interval z bootstrapu po shlucích. Kalibrace soudce: neprošla nebo neproběhla (A/B jen informativně)

- plane_poplachy: chybí data
- poruseni_vyznamu: horní mez +0.000 ≤ +0.050
- ztrata_cisel: horní mez +0.000 ≤ +0.020
- poruseni_vyznamu: -0.308 [-0.538, +0.000]
- ztrata_cisel: +0.000 [+0.000, +0.000]
- posun_skore: -0.002 [-0.009, +0.002]
- vyhry_ab: -0.077 [-0.556, +0.222]

### Vrstva: rozhodovaci

| skill | lidských / AI | plané poplachy | AUC hustoty | kappa | posun skóre AI | přiblížení k autorovi | ztráta čísel | ztráta jmen | porušení významu | změna lidských | posun skóre lidských | bez verze | cena/text | kroků | čas s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| unslop-cs | 0 / 13 | – | – | – | -0.000 | -0.049 | 0.000 | 0.026 | 0.231 | – | – | 0 | 0.292 | 7 | 37.700 |
| anti-ai-slop-cz | 0 / 13 | – | – | – | -0.007 | -0.597 | 0.000 | 0.030 | 0.462 | – | – | 0 | 0.098 | 3 | 25.900 |
| humanizer-czech | 0 / 13 | – | – | – | -0.003 | -0.215 | 0.000 | 0.026 | 0.462 | – | – | 0 | 0.139 | 3 | 26.100 |
| bez-skillu | 0 / 13 | – | – | – | 0.002 | -0.597 | 0.000 | 0.029 | 0.538 | – | – | 0 | 0.044 | 1 | 28.600 |

### Vrstva: vse

| skill | lidských / AI | plané poplachy | AUC hustoty | kappa | posun skóre AI | přiblížení k autorovi | ztráta čísel | ztráta jmen | porušení významu | změna lidských | posun skóre lidských | bez verze | cena/text | kroků | čas s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| unslop-cs | 0 / 20 | – | – | – | -0.006 | -0.046 | 0.000 | 0.026 | 0.400 | – | – | 0 | 0.300 | 7.000 | 42.350 |
| anti-ai-slop-cz | 0 / 20 | – | – | – | 0.021 | -0.564 | 0.000 | 0.090 | 0.650 | – | – | 0 | 0.103 | 3.000 | 26.850 |
| humanizer-czech | 0 / 20 | – | – | – | 0.028 | -0.290 | 0.000 | 0.053 | 0.600 | – | – | 0 | 0.141 | 3.000 | 27.600 |
| bez-skillu | 0 / 20 | – | – | – | 0.065 | -0.542 | 0.000 | 0.050 | 0.650 | – | – | 0 | 0.048 | 1.000 | 30.600 |

### Vrstva: klasika

| skill | lidských / AI | plané poplachy | AUC hustoty | kappa | posun skóre AI | přiblížení k autorovi | ztráta čísel | ztráta jmen | porušení významu | změna lidských | posun skóre lidských | bez verze | cena/text | kroků | čas s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| unslop-cs | 0 / 7 | – | – | – | -0.000 | -0.156 | – | 0.000 | 0.143 | – | – | 0 | 0.292 | 7 | 37.700 |
| anti-ai-slop-cz | 0 / 7 | – | – | – | -0.015 | -0.482 | – | 0.008 | 0.429 | – | – | 0 | 0.100 | 3 | 26.200 |
| humanizer-czech | 0 / 7 | – | – | – | 0.000 | -0.133 | – | 0.000 | 0.286 | – | – | 0 | 0.137 | 3 | 25.000 |
| bez-skillu | 0 / 7 | – | – | – | -0.000 | -0.320 | – | 0.000 | 0.571 | – | – | 0 | 0.049 | 1 | 30.700 |

### Vrstva: cac

| skill | lidských / AI | plané poplachy | AUC hustoty | kappa | posun skóre AI | přiblížení k autorovi | ztráta čísel | ztráta jmen | porušení významu | změna lidských | posun skóre lidských | bez verze | cena/text | kroků | čas s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| unslop-cs | 0 / 2 | – | – | – | -0.078 | -0.056 | – | 0.143 | 1 | – | – | 0 | 0.335 | 7.000 | 79.500 |
| anti-ai-slop-cz | 0 / 2 | – | – | – | -0.091 | -1.537 | – | 0.000 | 1 | – | – | 0 | 0.111 | 3.000 | 33.500 |
| humanizer-czech | 0 / 2 | – | – | – | -0.047 | -0.945 | – | 0.000 | 0.500 | – | – | 0 | 0.151 | 3.000 | 32.350 |
| bez-skillu | 0 / 2 | – | – | – | -0.075 | 0.143 | – | 0.000 | 0.500 | – | – | 0 | 0.053 | 1.000 | 33.750 |

### Vrstva: fictree

| skill | lidských / AI | plané poplachy | AUC hustoty | kappa | posun skóre AI | přiblížení k autorovi | ztráta čísel | ztráta jmen | porušení významu | změna lidských | posun skóre lidských | bez verze | cena/text | kroků | čas s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| unslop-cs | 0 / 3 | – | – | – | -0.000 | 0.000 | – | 0.000 | 0.333 | – | – | 0 | 0.301 | 7 | 42.900 |
| anti-ai-slop-cz | 0 / 3 | – | – | – | 0.001 | 0.732 | – | 0.071 | 1 | – | – | 0 | 0.103 | 3 | 27.100 |
| humanizer-czech | 0 / 3 | – | – | – | 0.002 | -0.393 | – | 0.071 | 1 | – | – | 0 | 0.145 | 3 | 27.800 |
| bez-skillu | 0 / 3 | – | – | – | 0.250 | -0.679 | – | 0.143 | 1 | – | – | 0 | 0.052 | 1 | 30.900 |

### Vrstva: wiki

| skill | lidských / AI | plané poplachy | AUC hustoty | kappa | posun skóre AI | přiblížení k autorovi | ztráta čísel | ztráta jmen | porušení významu | změna lidských | posun skóre lidských | bez verze | cena/text | kroků | čas s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| unslop-cs | 0 / 4 | – | – | – | 0.000 | 0.072 | 0.000 | 0.083 | 0.250 | – | – | 0 | 0.291 | 7.000 | 37.750 |
| anti-ai-slop-cz | 0 / 4 | – | – | – | 0.005 | -0.889 | 0.000 | 0.083 | 0.500 | – | – | 0 | 0.096 | 3.000 | 24.350 |
| humanizer-czech | 0 / 4 | – | – | – | -0.010 | -0.370 | 0.000 | 0.083 | 0.750 | – | – | 0 | 0.140 | 3.000 | 26.900 |
| bez-skillu | 0 / 4 | – | – | – | 0.006 | -1.093 | 0.000 | 0.093 | 0.500 | – | – | 0 | 0.041 | 1.000 | 24.400 |

### Vrstva: uredni

| skill | lidských / AI | plané poplachy | AUC hustoty | kappa | posun skóre AI | přiblížení k autorovi | ztráta čísel | ztráta jmen | porušení významu | změna lidských | posun skóre lidských | bez verze | cena/text | kroků | čas s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| unslop-cs | 0 / 2 | – | – | – | 0.000 | 0.000 | 0.000 | 0.000 | 0.500 | – | – | 0 | 0.300 | 7.000 | 42.200 |
| anti-ai-slop-cz | 0 / 2 | – | – | – | 0.001 | 0.000 | 0.000 | 0.000 | 0.500 | – | – | 0 | 0.105 | 3.000 | 27.800 |
| humanizer-czech | 0 / 2 | – | – | – | 0.000 | 0.000 | 0.000 | 0.000 | 0.500 | – | – | 0 | 0.143 | 3.000 | 27.350 |
| bez-skillu | 0 / 2 | – | – | – | 0.000 | 0.000 | 0.000 | 0.000 | 0.500 | – | – | 0 | 0.044 | 1.000 | 25.550 |

### Vrstva: aikoditex

| skill | lidských / AI | plané poplachy | AUC hustoty | kappa | posun skóre AI | přiblížení k autorovi | ztráta čísel | ztráta jmen | porušení významu | změna lidských | posun skóre lidských | bez verze | cena/text | kroků | čas s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| unslop-cs | 0 / 2 | – | – | – | 0.022 | – | – | 0.000 | 1 | – | – | 0 | 0.321 | 7.000 | 60.750 |
| anti-ai-slop-cz | 0 / 2 | – | – | – | 0.341 | – | – | 0.542 | 1 | – | – | 0 | 0.106 | 3.000 | 32.300 |
| humanizer-czech | 0 / 2 | – | – | – | 0.341 | – | – | 0.236 | 1 | – | – | 0 | 0.148 | 3.000 | 31.650 |
| bez-skillu | 0 / 2 | – | – | – | 0.337 | – | – | 0.125 | 1 | – | – | 0 | 0.052 | 1.000 | 32.700 |

Plané poplachy = podíl lidských textů s aspoň jedním nálezem vysoké nebo střední závažnosti. Posun skóre = skóre AI-ovosti před minus po přepisu (kladné = blíž lidským textům). Přiblížení k autorovi = o kolik se rysy F0 pokračování přiblížily skutečnému pokračování autora. Ztráty a porušení významu jen u AI textů. Kappa = shoda běhů v tom, zda text má nález.
