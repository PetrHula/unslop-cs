# Režim psaní: psani-1

- Datum: 2026-11-15 15:22 +0100; dev sada, témat 67; commit `9f222d2`
- Model skillu: claude-sonnet-5-5 (effort medium); otisky: unslop-cs `66408a7984e8`, anti-ai-slop-cz `d98a1147e447`, bez-skillu `None`
- Cena celkem: 16.60 USD; nevyhodnoceno 0, bez textu mezi značkami 1

Skóre AI-ovosti: 0 = jako lidský text, 1 = jako AI (rysy F0, nezávislé na pravidlech skillů). Řádek „lidský originál“ je skóre lidského textu, ze kterého je téma. Do rozhodovacího pravidla nevstupuje.

## Vrstva: rozhodovaci

| | textů | skóre AI | délka/zadání | s čísly | značky/markdown | skill načten | cena/text | kroků |
|---|---|---|---|---|---|---|---|---|
| lidský originál | 44 | 0.020 | | | | | | |
| unslop-cs | 43 | 0.960 | 0.89 | 0.67 | 0.07 | 1.00 | 0.135 | 4 |
| anti-ai-slop-cz | 44 | 0.964 | 0.90 | 0.61 | 0.11 | 1.00 | 0.087 | 3 |
| bez-skillu | 44 | 0.995 | 0.93 | 0.50 | 0.02 | 1.00 | 0.022 | 1 |

- unslop-cs − bez-skillu, skóre AI: -0.035 [-0.088, -0.004]
- unslop-cs − bez-skillu, s čísly: +0.186 [+0.031, +0.306]
- anti-ai-slop-cz − bez-skillu, skóre AI: -0.032 [-0.072, -0.009]
- anti-ai-slop-cz − bez-skillu, s čísly: +0.114 [-0.030, +0.214]
- unslop-cs − anti-ai-slop-cz, skóre AI: -0.003 [-0.054, +0.042]
- unslop-cs − anti-ai-slop-cz, s čísly: +0.070 [-0.031, +0.167]

## Vrstva: vse

| | textů | skóre AI | délka/zadání | s čísly | značky/markdown | skill načten | cena/text | kroků |
|---|---|---|---|---|---|---|---|---|
| lidský originál | 67 | 0.025 | | | | | | |
| unslop-cs | 66 | 0.974 | 0.89 | 0.59 | 0.05 | 1.00 | 0.135 | 4 |
| anti-ai-slop-cz | 67 | 0.975 | 0.90 | 0.52 | 0.07 | 1.00 | 0.086 | 3 |
| bez-skillu | 67 | 0.997 | 0.94 | 0.43 | 0.01 | 1.00 | 0.022 | 1 |

- unslop-cs − bez-skillu, skóre AI: -0.023 [-0.054, -0.002]
- unslop-cs − bez-skillu, s čísly: +0.167 [+0.029, +0.277]
- anti-ai-slop-cz − bez-skillu, skóre AI: -0.021 [-0.046, -0.006]
- anti-ai-slop-cz − bez-skillu, s čísly: +0.090 [-0.020, +0.187]
- unslop-cs − anti-ai-slop-cz, skóre AI: -0.001 [-0.033, +0.027]
- unslop-cs − anti-ai-slop-cz, s čísly: +0.076 [-0.018, +0.162]

