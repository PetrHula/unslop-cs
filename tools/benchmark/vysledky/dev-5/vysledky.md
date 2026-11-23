# Benchmark skillů: dev-5

- Datum: 2026-11-23 20:44 +0100; sada: dev; textů: 164 (lidských 67, AI 97); běhů na text: 1
- Commit: `fb5c2bc (neuložené změny)`; otisky skillů: unslop-cs `fa1e907dacee`
- Model skillu: claude-sonnet-5-5 (effort medium; Claude Code 2.1.330); soudce: claude-opus-5-5; normalizace: claude-haiku-5-5; modely z běhů: claude-sonnet-5-5
- Cena celkem: 27.23 USD; nevyhodnocené běhy: 0

**POZOR: zamítnuté nástroje** (skill neběžel, jak je navržený): unslop-cs 8% běhů

### Vrstva: rozhodovaci

| skill | lidských / AI | lidské s nálezem | AI s nálezem | AUC hustoty | plané poplachy v/s | citlivost v/s | AUC v/s | kappa | posun skóre AI | přiblížení k autorovi | ztráta čísel | přidaná čísla | ztráta jmen | přidaná jména | porušení významu | změna lidských | posun skóre lidských | bez verze | cena/text | kroků | čas s | zamítnutí | chyba nástroje |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| unslop-cs | 44 / 44 | 0.068 | 0.705 | 0.836 | 0.045 | 0.659 | 0.817 | – | -0.003 | -0.200 | 0.030 | 0.023 | 0.005 | 0.023 | – | 0.001 | -0.000 | 0 | 0.154 | 3.000 | 29.900 | 0.114 | 0.114 |

### Vrstva: vse

| skill | lidských / AI | lidské s nálezem | AI s nálezem | AUC hustoty | plané poplachy v/s | citlivost v/s | AUC v/s | kappa | posun skóre AI | přiblížení k autorovi | ztráta čísel | přidaná čísla | ztráta jmen | přidaná jména | porušení významu | změna lidských | posun skóre lidských | bez verze | cena/text | kroků | čas s | zamítnutí | chyba nástroje |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| unslop-cs | 67 / 97 | 0.075 | 0.742 | 0.854 | 0.045 | 0.701 | 0.840 | – | 0.018 | -0.230 | 0.015 | 0.010 | 0.032 | 0.041 | – | 0.001 | -0.000 | 0 | 0.157 | 3.000 | 33.250 | 0.079 | 0.079 |

### Vrstva: klasika

| skill | lidských / AI | lidské s nálezem | AI s nálezem | AUC hustoty | plané poplachy v/s | citlivost v/s | AUC v/s | kappa | posun skóre AI | přiblížení k autorovi | ztráta čísel | přidaná čísla | ztráta jmen | přidaná jména | porušení významu | změna lidských | posun skóre lidských | bez verze | cena/text | kroků | čas s | zamítnutí | chyba nástroje |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| unslop-cs | 24 / 24 | 0 | 0.708 | 0.854 | 0 | 0.667 | 0.833 | – | 0.006 | -0.318 | 0.000 | 0 | 0.009 | 0.042 | – | 0.000 | 0.000 | 0 | 0.152 | 3.000 | 28.950 | 0.104 | 0.104 |

### Vrstva: cac

| skill | lidských / AI | lidské s nálezem | AI s nálezem | AUC hustoty | plané poplachy v/s | citlivost v/s | AUC v/s | kappa | posun skóre AI | přiblížení k autorovi | ztráta čísel | přidaná čísla | ztráta jmen | přidaná jména | porušení významu | změna lidských | posun skóre lidských | bez verze | cena/text | kroků | čas s | zamítnutí | chyba nástroje |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| unslop-cs | 12 / 12 | 0 | 0.417 | 0.708 | 0 | 0.417 | 0.708 | – | -0.000 | -0.146 | 0.000 | 0 | 0.037 | 0 | – | 0.000 | 0.000 | 0 | 0.152 | 3.000 | 32.850 | 0.042 | 0.042 |

### Vrstva: fictree

| skill | lidských / AI | lidské s nálezem | AI s nálezem | AUC hustoty | plané poplachy v/s | citlivost v/s | AUC v/s | kappa | posun skóre AI | přiblížení k autorovi | ztráta čísel | přidaná čísla | ztráta jmen | přidaná jména | porušení významu | změna lidských | posun skóre lidských | bez verze | cena/text | kroků | čas s | zamítnutí | chyba nástroje |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| unslop-cs | 11 / 11 | 0.182 | 0.909 | 0.888 | 0.091 | 0.909 | 0.950 | – | 0.067 | -0.428 | – | 0 | 0.000 | 0 | – | 0.004 | -0.002 | 0 | 0.156 | 3.000 | 37.800 | 0.045 | 0.045 |

### Vrstva: wiki

| skill | lidských / AI | lidské s nálezem | AI s nálezem | AUC hustoty | plané poplachy v/s | citlivost v/s | AUC v/s | kappa | posun skóre AI | přiblížení k autorovi | ztráta čísel | přidaná čísla | ztráta jmen | přidaná jména | porušení významu | změna lidských | posun skóre lidských | bez verze | cena/text | kroků | čas s | zamítnutí | chyba nástroje |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| unslop-cs | 12 / 12 | 0.250 | 0.583 | 0.698 | 0.167 | 0.500 | 0.674 | – | -0.021 | -0.080 | 0.006 | 0 | 0.000 | 0 | – | 0.003 | -0.000 | 0 | 0.160 | 3.000 | 31.750 | 0.083 | 0.083 |

### Vrstva: uredni

| skill | lidských / AI | lidské s nálezem | AI s nálezem | AUC hustoty | plané poplachy v/s | citlivost v/s | AUC v/s | kappa | posun skóre AI | přiblížení k autorovi | ztráta čísel | přidaná čísla | ztráta jmen | přidaná jména | porušení významu | změna lidských | posun skóre lidských | bez verze | cena/text | kroků | čas s | zamítnutí | chyba nástroje |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| unslop-cs | 8 / 8 | 0 | 0.875 | 0.938 | 0 | 0.875 | 0.938 | – | -0.002 | -0.108 | 0.083 | 0.125 | 0.000 | 0 | – | 0.000 | -0.000 | 0 | 0.155 | 3.000 | 30.000 | 0.188 | 0.188 |

### Vrstva: aikoditex

| skill | lidských / AI | lidské s nálezem | AI s nálezem | AUC hustoty | plané poplachy v/s | citlivost v/s | AUC v/s | kappa | posun skóre AI | přiblížení k autorovi | ztráta čísel | přidaná čísla | ztráta jmen | přidaná jména | porušení významu | změna lidských | posun skóre lidských | bez verze | cena/text | kroků | čas s | zamítnutí | chyba nástroje |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| unslop-cs | 0 / 30 | – | 0.867 | – | – | 0.800 | – | – | 0.037 | – | 0.000 | 0 | 0.086 | 0.100 | – | – | – | 0 | 0.187 | 3.000 | 48.900 | 0.033 | 0.033 |

Lidské / AI s nálezem = podíl lidských / AI textů s aspoň jedním nálezem jakékoli závažnosti (nezávisí na tom, jak skill štítkuje závažnost); AUC hustoty = odlišení AI a lidských textů podle počtu všech nálezů na 1000 slov. Plané poplachy v/s a citlivost v/s = totéž jen s nálezy vysoké nebo střední závažnosti. Přidaná čísla / jména = podíl přepisů AI textů s aspoň jedním číslem či datem / vlastním jménem, které v originálu není. Zamítnutí a chyba nástroje = podíl běhů, kde skill narazil na zamítnutý nebo chybný nástroj (chyba nástroje se zaznamenává od 2026-11-13). Posun skóre = skóre AI-ovosti před minus po přepisu (kladné = blíž lidským textům). Přiblížení k autorovi = o kolik se rysy F0 pokračování přiblížily skutečnému pokračování autora. Ztráty a porušení významu jen u AI textů. Kappa = shoda běhů v tom, zda text má nález.
