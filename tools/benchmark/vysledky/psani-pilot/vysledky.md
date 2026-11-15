# Režim psaní: psani-pilot

- Datum: 2026-11-15 15:10 +0100; dev sada, témat 3; commit `7a8683a`
- Model skillu: claude-sonnet-5-5 (effort medium); otisky: unslop-cs `66408a7984e8`, anti-ai-slop-cz `d98a1147e447`, bez-skillu `None`
- Cena celkem: 0.73 USD; nevyhodnoceno 0, bez textu mezi značkami 0

Skóre AI-ovosti: 0 = jako lidský text, 1 = jako AI (rysy F0, nezávislé na pravidlech skillů). Řádek „lidský originál“ je skóre lidského textu, ze kterého je téma. Do rozhodovacího pravidla nevstupuje.

## Vrstva: rozhodovaci

| | textů | skóre AI | délka/zadání | s čísly | značky/markdown | skill načten | cena/text | kroků |
|---|---|---|---|---|---|---|---|---|
| lidský originál | 2 | 0.044 | | | | | | |
| unslop-cs | 2 | 0.994 | 0.94 | 1.00 | 0.00 | 1.00 | 0.146 | 4 |
| anti-ai-slop-cz | 2 | 0.990 | 0.92 | 1.00 | 0.00 | 1.00 | 0.090 | 3 |
| bez-skillu | 2 | 0.798 | 0.90 | 0.50 | 0.00 | 1.00 | 0.022 | 1 |

- unslop-cs − bez-skillu, skóre AI: +0.196 [+0.000, +0.391]
- unslop-cs − bez-skillu, s čísly: +0.500 [+0.000, +1.000]
- anti-ai-slop-cz − bez-skillu, skóre AI: +0.192 [+0.000, +0.383]
- anti-ai-slop-cz − bez-skillu, s čísly: +0.500 [+0.000, +1.000]
- unslop-cs − anti-ai-slop-cz, skóre AI: +0.004 [+0.000, +0.008]
- unslop-cs − anti-ai-slop-cz, s čísly: +0.000 [+0.000, +0.000]

## Vrstva: vse

| | textů | skóre AI | délka/zadání | s čísly | značky/markdown | skill načten | cena/text | kroků |
|---|---|---|---|---|---|---|---|---|
| lidský originál | 3 | 0.048 | | | | | | |
| unslop-cs | 3 | 0.988 | 0.87 | 1.00 | 0.00 | 1.00 | 0.137 | 4 |
| anti-ai-slop-cz | 3 | 0.982 | 0.87 | 0.67 | 0.00 | 1.00 | 0.086 | 3 |
| bez-skillu | 3 | 0.864 | 0.91 | 0.33 | 0.00 | 1.00 | 0.022 | 1 |

- unslop-cs − bez-skillu, skóre AI: +0.124 [-0.020, +0.391]
- unslop-cs − bez-skillu, s čísly: +0.667 [+0.000, +1.000]
- anti-ai-slop-cz − bez-skillu, skóre AI: +0.118 [-0.030, +0.383]
- anti-ai-slop-cz − bez-skillu, s čísly: +0.333 [+0.000, +1.000]
- unslop-cs − anti-ai-slop-cz, skóre AI: +0.006 [+0.000, +0.009]
- unslop-cs − anti-ai-slop-cz, s čísly: +0.333 [+0.000, +1.000]

