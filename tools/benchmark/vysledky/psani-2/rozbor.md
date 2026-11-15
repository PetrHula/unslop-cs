# Rozbor psani-2: režim psaní, unslop-cs 1.6.1

Stejných 67 dev témat jako `psani-1`. Nově běžel jen unslop-cs (67 běhů, 9,36 USD), anti-ai-slop-cz a bez-skillu převzaté z `psani-1` (134 běhů, `--prevzit`).

Změna 1.6.0 → 1.6.1 v režimu psaní (`references/psani.md`, SKILL.md): statistiky, procenta, ceny a počty jen z podkladů, obecně známé datum nebo jméno jen s jistotou; text odevzdat vždy, bez `[OVĚŘIT]` a zástupných textů, chybějící údaje do seznamu „Neověřené údaje“ pod text.

| rozhodovací vrstvy (44 témat) | skóre AI | s čísly | značky/markdown | bez textu | cena/text |
|---|---|---|---|---|---|
| lidský originál | 0,020 | | | | |
| unslop-cs 1.6.0 (`psani-1`) | 0,960 | 67 % | 7 % | 1 | 0,135 |
| unslop-cs 1.6.1 | 0,982 | 55 % | 2 % | 0 | 0,140 |
| anti-ai-slop-cz | 0,964 | 61 % | 11 % | 0 | 0,087 |
| bez-skillu | 0,995 | 50 % | 2 % | 0 | 0,022 |

**Pravidla skill teď dodržuje:** v žádném ze 67 textů nezůstala značka `[OVĚŘIT]`, žádné psaní neodmítl a seznam neověřených údajů dal pod 60 textů. Jediná „značka“ je odrážkový seznam v hesle.

**Doplněná čísla:** 67 % → 55 %; rozdíl proti bez-skillu už není průkazný (+5 p. b. [−11; +16]). Pravdivost se dál neověřuje.

**Cena za to:** skóre AI-ovosti je o něco vyšší (0,960 → 0,982); rozdíl proti anti-ai-slop-cz +0,019 [−0,014; +0,071] ani proti bez-skillu −0,013 [−0,031; +0,005] průkazný není. Čísla a jména patří k rysům, podle kterých F0 pozná lidský text, takže méně doplněných údajů text klasifikátoru přibližuje AI. To je vědomá volba: vymyšlený údaj je horší než obecnější věta.

Omezení jako u `psani-1`: jeden běh, dev sada, žánry z korpusu.
