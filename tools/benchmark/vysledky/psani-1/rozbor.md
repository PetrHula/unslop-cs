# Rozbor psani-1: režim psaní

67 dev témat (chatbotí zadání z kroku 2), 1 běh, Sonnet 5.5 s effortem medium, 16,60 USD. Skóre AI-ovosti je klasifikátor F0 trénovaný na dev sadě (včetně chatbotích textů Clauda na stejná témata), nezávislý na pravidlech skillů.

| rozhodovací vrstvy (44 témat) | skóre AI | s čísly | značky/markdown | cena/text |
|---|---|---|---|---|
| lidský originál | 0,020 | | | |
| unslop-cs 1.6.0 | 0,960 | 67 % | 7 % | 0,135 |
| anti-ai-slop-cz | 0,964 | 61 % | 11 % | 0,087 |
| bez-skillu | 0,995 | 50 % | 2 % | 0,022 |

**Hlavní výsledek:** v psaní jsou unslop-cs a anti-ai-slop-cz stejně dobré (rozdíl skóre −0,003 [−0,054; +0,042]). Proti psaní bez skillu sníží skóre oba jen o 3 setiny; výsledné texty klasifikátor dál bezpečně pozná jako AI. Skill psaní nezlidští, jen odstraní nejvýraznější obraty; rozdíl je hlavně v rysech, které F0 nevidí (slovník, fráze).

**Riziko:** oba skilly tlačí ke konkrétnosti, a proto častěji doplní čísla, data a jména, která v zadání nejsou. U unslop-cs je rozdíl proti bez-skillu statisticky jistý (+19 p. b. [+3; +31]). Pravdivost se neověřuje; u faktických žánrů (heslo, tisková zpráva) je to místo, kde vznikají vymyšlené údaje.

**Dodržování vlastních pravidel:**
- unslop-cs nechal ve dvou textech značky `[OVĚŘIT: …]` přímo v textu, ačkoli je podle SKILL.md v režimu psaní vrací zvlášť. Jednou psaní odmítl (tisková zpráva o volbách bez faktů) a napsal proč; to je poctivé, ale uživatel nedostal text.
- anti-ai-slop-cz nechává zástupné značky `[doplnit]`, `[datum]`, `[jméno, telefon, e-mail]` (hlavně u tiskových zpráv).

**Omezení:** témata a žánry jsou z korpusu (fejeton, beletrie, heslo, tisková zpráva), ne z firemní komunikace (e-mail, LinkedIn), na kterou míří anti-ai-slop-cz. Jeden běh, dev sada.
