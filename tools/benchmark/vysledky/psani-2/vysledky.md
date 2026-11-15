# Režim psaní: psani-2

- Datum: 2026-11-15 16:56 +0100; dev sada, témat 67; commit `d47821e`
- Model skillu: claude-sonnet-5-5 (effort medium); otisky: unslop-cs `72bb07be240f`, anti-ai-slop-cz `d98a1147e447`, bez-skillu `None`
- Cena celkem: 9.36 USD; nevyhodnoceno 0, bez textu mezi značkami 0

Skóre AI-ovosti: 0 = jako lidský text, 1 = jako AI (rysy F0, nezávislé na pravidlech skillů). Řádek „lidský originál“ je skóre lidského textu, ze kterého je téma. Do rozhodovacího pravidla nevstupuje.

## Vrstva: rozhodovaci

| | textů | skóre AI | délka/zadání | s čísly | značky/markdown | skill načten | cena/text | kroků |
|---|---|---|---|---|---|---|---|---|
| lidský originál | 44 | 0.020 | | | | | | |
| unslop-cs | 44 | 0.982 | 0.89 | 0.55 | 0.02 | 1.00 | 0.140 | 4 |
| anti-ai-slop-cz | 44 | 0.964 | 0.90 | 0.61 | 0.11 | 1.00 | 0.087 | 3 |
| bez-skillu | 44 | 0.995 | 0.93 | 0.50 | 0.02 | 1.00 | 0.022 | 1 |

- unslop-cs − bez-skillu, skóre AI: -0.013 [-0.031, +0.005]
- unslop-cs − bez-skillu, s čísly: +0.045 [-0.108, +0.156]
- anti-ai-slop-cz − bez-skillu, skóre AI: -0.032 [-0.072, -0.009]
- anti-ai-slop-cz − bez-skillu, s čísly: +0.114 [-0.030, +0.214]
- unslop-cs − anti-ai-slop-cz, skóre AI: +0.019 [-0.014, +0.071]
- unslop-cs − anti-ai-slop-cz, s čísly: -0.068 [-0.170, +0.029]

## Vrstva: vse

| | textů | skóre AI | délka/zadání | s čísly | značky/markdown | skill načten | cena/text | kroků |
|---|---|---|---|---|---|---|---|---|
| lidský originál | 67 | 0.025 | | | | | | |
| unslop-cs | 67 | 0.987 | 0.89 | 0.48 | 0.01 | 1.00 | 0.139 | 4 |
| anti-ai-slop-cz | 67 | 0.975 | 0.90 | 0.52 | 0.07 | 1.00 | 0.086 | 3 |
| bez-skillu | 67 | 0.997 | 0.94 | 0.43 | 0.01 | 1.00 | 0.022 | 1 |

- unslop-cs − bez-skillu, skóre AI: -0.009 [-0.023, +0.003]
- unslop-cs − bez-skillu, s čísly: +0.045 [-0.076, +0.141]
- anti-ai-slop-cz − bez-skillu, skóre AI: -0.021 [-0.046, -0.006]
- anti-ai-slop-cz − bez-skillu, s čísly: +0.090 [-0.020, +0.187]
- unslop-cs − anti-ai-slop-cz, skóre AI: +0.012 [-0.010, +0.043]
- unslop-cs − anti-ai-slop-cz, s čísly: -0.045 [-0.133, +0.045]

