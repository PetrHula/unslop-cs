# Benchmark skillů: dev-1

- Datum: 2026-11-13 15:50 +0100; sada: dev; textů: 90 (lidských 40, AI 50); běhů na text: 1
- Commit: `f1ced52`; otisky skillů: unslop-cs `d9b0dd154573`, anti-ai-slop-cz `d98a1147e447`, humanizer-czech `639d897a18a5`, bez-skillu `None`
- Model skillu: claude-sonnet-5-5 (effort medium; Claude Code 2.1.323); soudce: claude-opus-5-5; normalizace: claude-haiku-5-5; modely z běhů: claude-sonnet-5-5
- Cena celkem: 51.70 USD; nevyhodnocené běhy: 0

**POZOR: zamítnuté nástroje** (skill neběžel, jak je navržený): unslop-cs 4% běhů

## unslop-cs proti anti-ai-slop-cz: A není lepší (zhoršuje plané poplachy nebo zachování významu)

Rozhodovací vrstvy (bez aikoditex, cac, fictree); A − B, 95% interval z bootstrapu po shlucích. Kalibrace soudce: neprošla nebo neproběhla (A/B jen informativně)

- plane_poplachy: horní mez +0.103 > +0.030 (A může být horší)
- poruseni_vyznamu: soudce významu neprošel kalibrací, do rozhodnutí nevstupuje
- ztrata_cisel: horní mez +0.000 ≤ +0.020
- plane_poplachy: -0.038 [-0.250, +0.103]
- ztrata_cisel: +0.000 [+0.000, +0.000]
- posun_skore: +0.002 [-0.011, +0.011]

K výkladu (do rozhodnutí nevstupuje):

- cena A/B: 2.8×
- plané poplachy: A 7.7%, B 11.5% (B/A 1.5×)
- citlivost A − B: -0.192 [-0.414, +0.043]
- zmena_lidskych A − B: -0.008 [-0.020, -0.000]
- ztrata_jmen A − B: -0.023 [-0.084, +0.047]

## unslop-cs proti humanizer-czech: A není lepší (zhoršuje plané poplachy nebo zachování významu)

Rozhodovací vrstvy (bez aikoditex, cac, fictree); A − B, 95% interval z bootstrapu po shlucích. Kalibrace soudce: neprošla nebo neproběhla (A/B jen informativně)

- plane_poplachy: horní mez +0.062 > +0.030 (A může být horší)
- poruseni_vyznamu: soudce významu neprošel kalibrací, do rozhodnutí nevstupuje
- ztrata_cisel: horní mez +0.000 ≤ +0.020
- plane_poplachy: -0.115 [-0.391, +0.062]
- ztrata_cisel: -0.004 [-0.014, +0.000]
- posun_skore: -0.004 [-0.032, +0.015]

K výkladu (do rozhodnutí nevstupuje):

- cena A/B: 2.0×
- plané poplachy: A 7.7%, B 19.2% (B/A 2.5×)
- citlivost A − B: -0.154 [-0.269, -0.043]
- zmena_lidskych A − B: -0.053 [-0.112, -0.014]
- ztrata_jmen A − B: -0.056 [-0.156, +0.073]

## unslop-cs proti bez-skillu: A není lepší (zhoršuje plané poplachy nebo zachování významu)

Rozhodovací vrstvy (bez aikoditex, cac, fictree); A − B, 95% interval z bootstrapu po shlucích. Kalibrace soudce: neprošla nebo neproběhla (A/B jen informativně)

- plane_poplachy: horní mez +0.103 > +0.030 (A může být horší)
- poruseni_vyznamu: soudce významu neprošel kalibrací, do rozhodnutí nevstupuje
- ztrata_cisel: horní mez +0.000 ≤ +0.020
- plane_poplachy: -0.038 [-0.250, +0.103]
- ztrata_cisel: -0.004 [-0.014, +0.000]
- posun_skore: -0.012 [-0.032, +0.006]

K výkladu (do rozhodnutí nevstupuje):

- cena A/B: 6.8×
- plané poplachy: A 7.7%, B 11.5% (B/A 1.5×)
- citlivost A − B: -0.346 [-0.531, -0.150]
- zmena_lidskych A − B: -0.021 [-0.048, -0.003]
- ztrata_jmen A − B: -0.012 [-0.028, +0.000]

### Vrstva: rozhodovaci

| skill | lidských / AI | plané poplachy | citlivost | AUC hustoty | kappa | posun skóre AI | přiblížení k autorovi | ztráta čísel | ztráta jmen | porušení významu | změna lidských | posun skóre lidských | bez verze | cena/text | kroků | čas s | zamítnutí | chyba nástroje |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| unslop-cs | 26 / 26 | 0.077 | 0.423 | 0.688 | – | 0.001 | -0.049 | 0.000 | 0.062 | – | 0.002 | -0.001 | 0 | 0.279 | 6.000 | 38.200 | 0.038 | 0.038 |
| anti-ai-slop-cz | 26 / 26 | 0.115 | 0.615 | 0.781 | – | -0.000 | -0.056 | 0.000 | 0.085 | – | 0.010 | -0.003 | 0 | 0.101 | 3.000 | 25.300 | 0 | 0 |
| humanizer-czech | 26 / 26 | 0.192 | 0.577 | 0.729 | – | 0.005 | -0.060 | 0.004 | 0.119 | – | 0.055 | -0.049 | 0 | 0.142 | 3.000 | 29.100 | 0 | 0 |
| bez-skillu | 26 / 26 | 0.115 | 0.769 | 0.854 | – | 0.013 | -0.108 | 0.004 | 0.075 | – | 0.024 | -0.006 | 0 | 0.041 | 1.000 | 26.050 | 0 | 0 |

### Vrstva: vse

| skill | lidských / AI | plané poplachy | citlivost | AUC hustoty | kappa | posun skóre AI | přiblížení k autorovi | ztráta čísel | ztráta jmen | porušení významu | změna lidských | posun skóre lidských | bez verze | cena/text | kroků | čas s | zamítnutí | chyba nástroje |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| unslop-cs | 40 / 50 | 0.075 | 0.440 | 0.698 | – | -0.011 | -0.046 | 0.000 | 0.044 | – | 0.001 | -0.001 | 0 | 0.281 | 6.000 | 40.900 | 0.044 | 0.044 |
| anti-ai-slop-cz | 40 / 50 | 0.075 | 0.680 | 0.824 | – | 0.019 | -0.080 | 0.010 | 0.121 | – | 0.007 | -0.002 | 0 | 0.101 | 3.000 | 25.850 | 0 | 0 |
| humanizer-czech | 40 / 50 | 0.200 | 0.680 | 0.785 | – | 0.006 | -0.072 | 0.013 | 0.099 | – | 0.055 | -0.050 | 0 | 0.144 | 3.000 | 29.400 | 0 | 0 |
| bez-skillu | 40 / 50 | 0.125 | 0.796 | 0.855 | – | 0.018 | -0.101 | 0.008 | 0.104 | – | 0.019 | -0.003 | 0 | 0.041 | 1.000 | 26.600 | 0 | 0 |

### Vrstva: klasika

| skill | lidských / AI | plané poplachy | citlivost | AUC hustoty | kappa | posun skóre AI | přiblížení k autorovi | ztráta čísel | ztráta jmen | porušení významu | změna lidských | posun skóre lidských | bez verze | cena/text | kroků | čas s | zamítnutí | chyba nástroje |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| unslop-cs | 14 / 14 | 0.143 | 0.286 | 0.592 | – | 0.002 | 0.000 | 0.000 | 0.000 | – | 0.000 | 0.000 | 0 | 0.277 | 6.000 | 37.300 | 0 | 0 |
| anti-ai-slop-cz | 14 / 14 | 0 | 0.643 | 0.821 | – | -0.007 | 0.155 | 0.000 | 0.074 | – | 0.000 | 0.000 | 0 | 0.100 | 3.000 | 25.050 | 0 | 0 |
| humanizer-czech | 14 / 14 | 0 | 0.500 | 0.750 | – | -0.008 | -0.053 | 0.000 | 0.131 | – | 0.002 | -0.004 | 0 | 0.140 | 3.000 | 26.800 | 0 | 0 |
| bez-skillu | 14 / 14 | 0 | 0.857 | 0.929 | – | 0.021 | -0.090 | 0.000 | 0.022 | – | 0.000 | 0.000 | 0 | 0.038 | 1.000 | 25.550 | 0 | 0 |

### Vrstva: cac

| skill | lidských / AI | plané poplachy | citlivost | AUC hustoty | kappa | posun skóre AI | přiblížení k autorovi | ztráta čísel | ztráta jmen | porušení významu | změna lidských | posun skóre lidských | bez verze | cena/text | kroků | čas s | zamítnutí | chyba nástroje |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| unslop-cs | 7 / 7 | 0.143 | 0.429 | 0.673 | – | 0.005 | -0.061 | 0.000 | 0.000 | – | 0.000 | 0.000 | 0 | 0.283 | 6.000 | 45.600 | 0 | 0 |
| anti-ai-slop-cz | 7 / 7 | 0 | 0.857 | 0.929 | – | 0.025 | -0.408 | 0.000 | 0.200 | – | 0.000 | 0.000 | 0 | 0.102 | 3.000 | 27.300 | 0 | 0 |
| humanizer-czech | 7 / 7 | 0.143 | 0.714 | 0.776 | – | 0.005 | -0.216 | 0.000 | 0.000 | – | 0.089 | -0.096 | 0 | 0.144 | 3.000 | 31.200 | 0 | 0 |
| bez-skillu | 7 / 7 | 0 | 0.857 | 0.929 | – | 0.007 | -0.339 | 0.000 | 0.200 | – | 0.001 | 0.000 | 0 | 0.039 | 1.000 | 25.150 | 0 | 0 |

### Vrstva: fictree

| skill | lidských / AI | plané poplachy | citlivost | AUC hustoty | kappa | posun skóre AI | přiblížení k autorovi | ztráta čísel | ztráta jmen | porušení významu | změna lidských | posun skóre lidských | bez verze | cena/text | kroků | čas s | zamítnutí | chyba nástroje |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| unslop-cs | 7 / 7 | 0 | 0.143 | 0.571 | – | -0.000 | -0.031 | – | 0.000 | – | 0.000 | -0.000 | 0 | 0.281 | 6.000 | 38.800 | 0 | 0 |
| anti-ai-slop-cz | 7 / 7 | 0 | 0.571 | 0.786 | – | -0.002 | 0.058 | – | 0.083 | – | 0.000 | -0.000 | 0 | 0.099 | 3.000 | 25.250 | 0 | 0 |
| humanizer-czech | 7 / 7 | 0.286 | 0.857 | 0.888 | – | -0.002 | -0.014 | – | 0.042 | – | 0.020 | -0.009 | 0 | 0.141 | 3.000 | 28.200 | 0 | 0 |
| bez-skillu | 7 / 7 | 0.286 | 0.714 | 0.755 | – | -0.001 | 0.058 | – | 0.042 | – | 0.019 | 0.005 | 0 | 0.041 | 1.000 | 26.950 | 0 | 0 |

### Vrstva: wiki

| skill | lidských / AI | plané poplachy | citlivost | AUC hustoty | kappa | posun skóre AI | přiblížení k autorovi | ztráta čísel | ztráta jmen | porušení významu | změna lidských | posun skóre lidských | bez verze | cena/text | kroků | čas s | zamítnutí | chyba nástroje |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| unslop-cs | 7 / 7 | 0 | 0.429 | 0.714 | – | -0.001 | -0.041 | 0.000 | 0.143 | – | 0.008 | -0.004 | 0 | 0.286 | 6.000 | 43.250 | 0.143 | 0.143 |
| anti-ai-slop-cz | 7 / 7 | 0.429 | 0.429 | 0.592 | – | -0.011 | -0.364 | 0.000 | 0.147 | – | 0.036 | -0.012 | 0 | 0.105 | 3.000 | 27.050 | 0 | 0 |
| humanizer-czech | 7 / 7 | 0.714 | 0.571 | 0.531 | – | -0.027 | -0.065 | 0.010 | 0.111 | – | 0.187 | -0.173 | 0 | 0.149 | 3.000 | 33.200 | 0 | 0 |
| bez-skillu | 7 / 7 | 0.429 | 0.571 | 0.653 | – | -0.000 | -0.178 | 0.010 | 0.146 | – | 0.088 | -0.021 | 0 | 0.047 | 1.000 | 28.500 | 0 | 0 |

### Vrstva: uredni

| skill | lidských / AI | plané poplachy | citlivost | AUC hustoty | kappa | posun skóre AI | přiblížení k autorovi | ztráta čísel | ztráta jmen | porušení významu | změna lidských | posun skóre lidských | bez verze | cena/text | kroků | čas s | zamítnutí | chyba nástroje |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| unslop-cs | 5 / 5 | 0 | 0.800 | 0.900 | – | 0.001 | -0.141 | 0.000 | 0.100 | – | 0.000 | -0.000 | 0 | 0.279 | 6.000 | 37.100 | 0 | 0 |
| anti-ai-slop-cz | 5 / 5 | 0 | 0.800 | 0.900 | – | 0.032 | 0.003 | 0.000 | 0.025 | – | 0.002 | 0.002 | 0 | 0.099 | 3.000 | 24.000 | 0 | 0 |
| humanizer-czech | 5 / 5 | 0 | 0.800 | 0.900 | – | 0.086 | -0.065 | 0.000 | 0.100 | – | 0.022 | -0.001 | 0 | 0.142 | 3.000 | 28.950 | 0 | 0 |
| bez-skillu | 5 / 5 | 0 | 0.800 | 0.900 | – | 0.010 | -0.046 | 0.000 | 0.100 | – | 0.000 | -0.000 | 0 | 0.034 | 1.000 | 21.450 | 0 | 0 |

### Vrstva: aikoditex

| skill | lidských / AI | plané poplachy | citlivost | AUC hustoty | kappa | posun skóre AI | přiblížení k autorovi | ztráta čísel | ztráta jmen | porušení významu | změna lidských | posun skóre lidských | bez verze | cena/text | kroků | čas s | zamítnutí | chyba nástroje |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| unslop-cs | 0 / 10 | – | 0.700 | – | – | -0.062 | – | 0.000 | 0.050 | – | – | – | 0 | 0.312 | 6.000 | 56.900 | 0.200 | 0.200 |
| anti-ai-slop-cz | 0 / 10 | – | 0.800 | – | – | 0.079 | – | 0.050 | 0.189 | – | – | – | 0 | 0.104 | 3.000 | 27.700 | 0 | 0 |
| humanizer-czech | 0 / 10 | – | 0.800 | – | – | 0.013 | – | 0.050 | 0.136 | – | – | – | 0 | 0.147 | 3.000 | 32.250 | 0 | 0 |
| bez-skillu | 0 / 10 | – | 0.889 | – | – | 0.054 | – | 0.025 | 0.164 | – | – | – | 0 | 0.057 | 1.000 | 35.500 | 0 | 0 |

Plané poplachy = podíl lidských textů s aspoň jedním nálezem vysoké nebo střední závažnosti; citlivost = totéž u AI textů. Zamítnutí a chyba nástroje = podíl běhů, kde skill narazil na zamítnutý nebo chybný nástroj (chyba nástroje se zaznamenává od 2026-11-13). Posun skóre = skóre AI-ovosti před minus po přepisu (kladné = blíž lidským textům). Přiblížení k autorovi = o kolik se rysy F0 pokračování přiblížily skutečnému pokračování autora. Ztráty a porušení významu jen u AI textů. Kappa = shoda běhů v tom, zda text má nález.
