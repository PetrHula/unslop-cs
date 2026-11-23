# Benchmark skillů: dev-4-nazor

- Datum: 2026-11-23 16:03 +0100; sada: dev; textů: 164 (lidských 67, AI 97); běhů na text: 1
- Commit: `fb5c2bc (neuložené změny)`; otisky skillů: unslop-cs-nazor `ebd4245cf9af`
- Model skillu: claude-sonnet-5-5 (effort medium; Claude Code 2.1.330); soudce: claude-opus-5-5; normalizace: claude-haiku-5-5; modely z běhů: claude-sonnet-5-5
- Cena celkem: 27.12 USD; nevyhodnocené běhy: 0

**POZOR: zamítnuté nástroje** (skill neběžel, jak je navržený): unslop-cs-nazor 3% běhů

### Vrstva: rozhodovaci

| skill | lidských / AI | lidské s nálezem | AI s nálezem | AUC hustoty | plané poplachy v/s | citlivost v/s | AUC v/s | kappa | posun skóre AI | přiblížení k autorovi | ztráta čísel | přidaná čísla | ztráta jmen | přidaná jména | porušení významu | změna lidských | posun skóre lidských | bez verze | cena/text | kroků | čas s | zamítnutí | chyba nástroje |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| unslop-cs-nazor | 44 / 44 | 0.023 | 0.636 | 0.811 | 0 | 0.591 | 0.795 | – | -0.011 | -0.262 | 0.005 | 0.023 | 0.038 | 0.023 | – | 0.001 | -0.000 | 0 | 0.155 | 3.000 | 27.400 | 0.034 | 0.034 |

### Vrstva: vse

| skill | lidských / AI | lidské s nálezem | AI s nálezem | AUC hustoty | plané poplachy v/s | citlivost v/s | AUC v/s | kappa | posun skóre AI | přiblížení k autorovi | ztráta čísel | přidaná čísla | ztráta jmen | přidaná jména | porušení významu | změna lidských | posun skóre lidských | bez verze | cena/text | kroků | čas s | zamítnutí | chyba nástroje |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| unslop-cs-nazor | 67 / 97 | 0.030 | 0.711 | 0.849 | 0.015 | 0.660 | 0.827 | – | 0.005 | -0.337 | 0.003 | 0.010 | 0.029 | 0.041 | – | 0.001 | -0.000 | 0 | 0.156 | 3.000 | 28.900 | 0.030 | 0.030 |

### Vrstva: klasika

| skill | lidských / AI | lidské s nálezem | AI s nálezem | AUC hustoty | plané poplachy v/s | citlivost v/s | AUC v/s | kappa | posun skóre AI | přiblížení k autorovi | ztráta čísel | přidaná čísla | ztráta jmen | přidaná jména | porušení významu | změna lidských | posun skóre lidských | bez verze | cena/text | kroků | čas s | zamítnutí | chyba nástroje |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| unslop-cs-nazor | 24 / 24 | 0 | 0.625 | 0.812 | 0 | 0.542 | 0.771 | – | -0.006 | -0.038 | 0.000 | 0.042 | 0.023 | 0.042 | – | 0.000 | 0.000 | 0 | 0.151 | 3.000 | 26.500 | 0.021 | 0.021 |

### Vrstva: cac

| skill | lidských / AI | lidské s nálezem | AI s nálezem | AUC hustoty | plané poplachy v/s | citlivost v/s | AUC v/s | kappa | posun skóre AI | přiblížení k autorovi | ztráta čísel | přidaná čísla | ztráta jmen | přidaná jména | porušení významu | změna lidských | posun skóre lidských | bez verze | cena/text | kroků | čas s | zamítnutí | chyba nástroje |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| unslop-cs-nazor | 12 / 12 | 0.083 | 0.500 | 0.729 | 0.083 | 0.417 | 0.684 | – | -0.000 | -0.084 | 0.000 | 0 | 0.037 | 0.083 | – | 0.000 | 0.000 | 0 | 0.154 | 3.000 | 27.850 | 0.042 | 0.042 |

### Vrstva: fictree

| skill | lidských / AI | lidské s nálezem | AI s nálezem | AUC hustoty | plané poplachy v/s | citlivost v/s | AUC v/s | kappa | posun skóre AI | přiblížení k autorovi | ztráta čísel | přidaná čísla | ztráta jmen | přidaná jména | porušení významu | změna lidských | posun skóre lidských | bez verze | cena/text | kroků | čas s | zamítnutí | chyba nástroje |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| unslop-cs-nazor | 11 / 11 | 0 | 0.909 | 0.955 | 0 | 0.909 | 0.955 | – | 0.032 | -0.876 | – | 0 | 0.000 | 0 | – | 0.000 | -0.000 | 0 | 0.155 | 3.000 | 30.200 | 0 | 0 |

### Vrstva: wiki

| skill | lidských / AI | lidské s nálezem | AI s nálezem | AUC hustoty | plané poplachy v/s | citlivost v/s | AUC v/s | kappa | posun skóre AI | přiblížení k autorovi | ztráta čísel | přidaná čísla | ztráta jmen | přidaná jména | porušení významu | změna lidských | posun skóre lidských | bez verze | cena/text | kroků | čas s | zamítnutí | chyba nástroje |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| unslop-cs-nazor | 12 / 12 | 0.083 | 0.500 | 0.722 | 0 | 0.500 | 0.750 | – | -0.025 | -0.421 | 0.000 | 0 | 0.091 | 0 | – | 0.003 | -0.000 | 0 | 0.157 | 3.000 | 28.050 | 0.083 | 0.083 |

### Vrstva: uredni

| skill | lidských / AI | lidské s nálezem | AI s nálezem | AUC hustoty | plané poplachy v/s | citlivost v/s | AUC v/s | kappa | posun skóre AI | přiblížení k autorovi | ztráta čísel | přidaná čísla | ztráta jmen | přidaná jména | porušení významu | změna lidských | posun skóre lidských | bez verze | cena/text | kroků | čas s | zamítnutí | chyba nástroje |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| unslop-cs-nazor | 8 / 8 | 0 | 0.875 | 0.938 | 0 | 0.875 | 0.938 | – | -0.002 | -0.535 | 0.017 | 0 | 0.000 | 0 | – | 0.000 | -0.000 | 0 | 0.154 | 3.000 | 27.350 | 0 | 0 |

### Vrstva: aikoditex

| skill | lidských / AI | lidské s nálezem | AI s nálezem | AUC hustoty | plané poplachy v/s | citlivost v/s | AUC v/s | kappa | posun skóre AI | přiblížení k autorovi | ztráta čísel | přidaná čísla | ztráta jmen | přidaná jména | porušení významu | změna lidských | posun skóre lidských | bez verze | cena/text | kroků | čas s | zamítnutí | chyba nástroje |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| unslop-cs-nazor | 0 / 30 | – | 0.833 | – | – | 0.767 | – | – | 0.022 | – | 0.000 | 0 | 0.025 | 0.067 | – | – | – | 0 | 0.188 | 3.000 | 51.500 | 0.033 | 0.033 |

Lidské / AI s nálezem = podíl lidských / AI textů s aspoň jedním nálezem jakékoli závažnosti (nezávisí na tom, jak skill štítkuje závažnost); AUC hustoty = odlišení AI a lidských textů podle počtu všech nálezů na 1000 slov. Plané poplachy v/s a citlivost v/s = totéž jen s nálezy vysoké nebo střední závažnosti. Přidaná čísla / jména = podíl přepisů AI textů s aspoň jedním číslem či datem / vlastním jménem, které v originálu není. Zamítnutí a chyba nástroje = podíl běhů, kde skill narazil na zamítnutý nebo chybný nástroj (chyba nástroje se zaznamenává od 2026-11-13). Posun skóre = skóre AI-ovosti před minus po přepisu (kladné = blíž lidským textům). Přiblížení k autorovi = o kolik se rysy F0 pokračování přiblížily skutečnému pokračování autora. Ztráty a porušení významu jen u AI textů. Kappa = shoda běhů v tom, zda text má nález.
