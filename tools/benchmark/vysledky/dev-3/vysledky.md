# Benchmark skillů: dev-3

- Datum: 2026-11-19 14:31 +0100; sada: dev; textů: 164 (lidských 67, AI 97); běhů na text: 1
- Commit: `1ea2dea (neuložené změny)`; otisky skillů: unslop-cs `946962ece23b`
- Model skillu: claude-sonnet-5-5 (effort medium; Claude Code 2.1.328); soudce: claude-opus-5-5; normalizace: claude-haiku-5-5; modely z běhů: claude-sonnet-5-5
- Cena celkem: 21.22 USD; nevyhodnocené běhy: 0

**POZOR: zamítnuté nástroje** (skill neběžel, jak je navržený): unslop-cs 1% běhů

### Vrstva: rozhodovaci

| skill | lidských / AI | lidské s nálezem | AI s nálezem | AUC hustoty | plané poplachy v/s | citlivost v/s | AUC v/s | kappa | posun skóre AI | přiblížení k autorovi | ztráta čísel | přidaná čísla | ztráta jmen | přidaná jména | porušení významu | změna lidských | posun skóre lidských | bez verze | cena/text | kroků | čas s | zamítnutí | chyba nástroje |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| unslop-cs | 44 / 44 | 0.023 | 0.750 | 0.872 | 0 | 0.727 | 0.864 | – | 0.011 | -0.249 | 0.000 | 0 | 0.091 | 0.045 | – | 0.000 | -0.000 | 0 | 0.147 | 3.000 | 29.650 | 0 | 0 |

### Vrstva: vse

| skill | lidských / AI | lidské s nálezem | AI s nálezem | AUC hustoty | plané poplachy v/s | citlivost v/s | AUC v/s | kappa | posun skóre AI | přiblížení k autorovi | ztráta čísel | přidaná čísla | ztráta jmen | přidaná jména | porušení významu | změna lidských | posun skóre lidských | bez verze | cena/text | kroků | čas s | zamítnutí | chyba nástroje |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| unslop-cs | 67 / 72 | 0.045 | 0.778 | 0.879 | 0.030 | 0.750 | 0.871 | – | 0.026 | -0.213 | 0.000 | 0 | 0.064 | 0.042 | – | 0.001 | 0.000 | 0 | 0.148 | 3 | 30.200 | 0.007 | 0.007 |

### Vrstva: klasika

| skill | lidských / AI | lidské s nálezem | AI s nálezem | AUC hustoty | plané poplachy v/s | citlivost v/s | AUC v/s | kappa | posun skóre AI | přiblížení k autorovi | ztráta čísel | přidaná čísla | ztráta jmen | přidaná jména | porušení významu | změna lidských | posun skóre lidských | bez verze | cena/text | kroků | čas s | zamítnutí | chyba nástroje |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| unslop-cs | 24 / 24 | 0 | 0.750 | 0.875 | 0 | 0.750 | 0.875 | – | 0.015 | -0.240 | 0.000 | 0 | 0.065 | 0 | – | 0.000 | 0.000 | 0 | 0.143 | 3.000 | 28.850 | 0 | 0 |

### Vrstva: cac

| skill | lidských / AI | lidské s nálezem | AI s nálezem | AUC hustoty | plané poplachy v/s | citlivost v/s | AUC v/s | kappa | posun skóre AI | přiblížení k autorovi | ztráta čísel | přidaná čísla | ztráta jmen | přidaná jména | porušení významu | změna lidských | posun skóre lidských | bez verze | cena/text | kroků | čas s | zamítnutí | chyba nástroje |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| unslop-cs | 12 / 12 | 0 | 0.583 | 0.792 | 0 | 0.583 | 0.792 | – | 0.001 | -0.127 | 0.000 | 0 | 0.037 | 0.083 | – | 0.000 | 0.000 | 0 | 0.146 | 3.000 | 29.300 | 0 | 0 |

### Vrstva: fictree

| skill | lidských / AI | lidské s nálezem | AI s nálezem | AUC hustoty | plané poplachy v/s | citlivost v/s | AUC v/s | kappa | posun skóre AI | přiblížení k autorovi | ztráta čísel | přidaná čísla | ztráta jmen | přidaná jména | porušení významu | změna lidských | posun skóre lidských | bez verze | cena/text | kroků | čas s | zamítnutí | chyba nástroje |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| unslop-cs | 11 / 11 | 0.182 | 1 | 0.917 | 0.182 | 0.909 | 0.938 | – | 0.015 | -0.167 | – | 0 | 0.000 | 0 | – | 0.004 | 0.000 | 0 | 0.150 | 3.000 | 33.550 | 0.045 | 0.045 |

### Vrstva: wiki

| skill | lidských / AI | lidské s nálezem | AI s nálezem | AUC hustoty | plané poplachy v/s | citlivost v/s | AUC v/s | kappa | posun skóre AI | přiblížení k autorovi | ztráta čísel | přidaná čísla | ztráta jmen | přidaná jména | porušení významu | změna lidských | posun skóre lidských | bez verze | cena/text | kroků | čas s | zamítnutí | chyba nástroje |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| unslop-cs | 12 / 12 | 0 | 0.667 | 0.833 | 0 | 0.583 | 0.792 | – | -0.001 | -0.202 | 0.000 | 0 | 0.139 | 0 | – | 0.000 | -0.000 | 0 | 0.147 | 3.000 | 28.850 | 0 | 0 |

### Vrstva: uredni

| skill | lidských / AI | lidské s nálezem | AI s nálezem | AUC hustoty | plané poplachy v/s | citlivost v/s | AUC v/s | kappa | posun skóre AI | přiblížení k autorovi | ztráta čísel | přidaná čísla | ztráta jmen | přidaná jména | porušení významu | změna lidských | posun skóre lidských | bez verze | cena/text | kroků | čas s | zamítnutí | chyba nástroje |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| unslop-cs | 8 / 8 | 0.125 | 0.875 | 0.930 | 0 | 0.875 | 0.938 | – | 0.017 | -0.318 | 0.000 | 0 | 0.084 | 0.250 | – | 0.000 | -0.000 | 0 | 0.154 | 3.000 | 33.450 | 0 | 0 |

### Vrstva: aikoditex

| skill | lidských / AI | lidské s nálezem | AI s nálezem | AUC hustoty | plané poplachy v/s | citlivost v/s | AUC v/s | kappa | posun skóre AI | přiblížení k autorovi | ztráta čísel | přidaná čísla | ztráta jmen | přidaná jména | porušení významu | změna lidských | posun skóre lidských | bez verze | cena/text | kroků | čas s | zamítnutí | chyba nástroje |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| unslop-cs | 0 / 5 | – | 1 | – | – | 1 | – | – | 0.241 | – | 0.000 | 0 | 0.000 | 0 | – | – | – | 0 | 0.185 | 3 | 50.900 | 0 | 0 |

Lidské / AI s nálezem = podíl lidských / AI textů s aspoň jedním nálezem jakékoli závažnosti (nezávisí na tom, jak skill štítkuje závažnost); AUC hustoty = odlišení AI a lidských textů podle počtu všech nálezů na 1000 slov. Plané poplachy v/s a citlivost v/s = totéž jen s nálezy vysoké nebo střední závažnosti. Přidaná čísla / jména = podíl přepisů AI textů s aspoň jedním číslem či datem / vlastním jménem, které v originálu není. Zamítnutí a chyba nástroje = podíl běhů, kde skill narazil na zamítnutý nebo chybný nástroj (chyba nástroje se zaznamenává od 2026-11-13). Posun skóre = skóre AI-ovosti před minus po přepisu (kladné = blíž lidským textům). Přiblížení k autorovi = o kolik se rysy F0 pokračování přiblížily skutečnému pokračování autora. Ztráty a porušení významu jen u AI textů. Kappa = shoda běhů v tom, zda text má nález.
