# Rozbor dev-2: unslop-cs 1.6.1 na dev sadě

Stejný výběr jako `dev-1s` / `dev-1s-p` (90 dev textů: 40 lidských, 50 AI; 1 běh, bez soudce). Nově běžel jen unslop-cs (90 běhů, 12,84 USD), ostatní skilly převzaté (360 běhů). Pravidlo z 2026-11-15.

Změna 1.6.0 → 1.6.1 (CHANGELOG): filtr přesnosti nově vyřazuje místa, která skill sám nechává beze změny, obecné redakční vady bez vzorce AI a dobovou sazbu; text bez P0 a P1 s jedinou drobností P2 je čistý. Pravidla vznikla z rozboru deseti lidských dev textů, které 1.6.0 označila (8 z 10 nálezů byly P2 nebo místa, která výstup sám ponechal). **Ladilo se na stejných 40 lidských textech, na kterých se tu měří, takže zlepšení na lidských textech je optimistické; platí až test sada.**

| unslop-cs (všechny vrstvy) | 1.6.0 (`dev-1s-p`) | 1.6.1 (`dev-2`) | jadro-2 | anti-ai-slop-cz | bez-skillu |
|---|---|---|---|---|---|
| lidské s nálezem | 25 % | 2,5 % | 2,5 % | 65 % | 42,5 % |
| AI s nálezem | 82 % | 72 % | 78 % | 98 % | 100 % |
| AUC hustoty všech nálezů | 0,86 | 0,85 | 0,89 | 0,90 | 0,94 |
| citlivost v/s | 74 % | 68 % | 72 % | 68 % | 78 % |
| posun skóre AI (vš. / rozh.) | +0,033 / +0,017 | −0,001 / +0,010 | +0,018 / +0,023 | +0,019 / −0,000 | +0,018 / +0,013 |
| změna lidských | 0,2 % | 0,1 % | 0,0 % | 0,7 % | 1,9 % |
| cena/text | 0,138 | 0,138 | 0,107 | 0,101 | 0,041 |

**Co se zlepšilo:** lidské texty s nálezem klesly z 10 ze 40 na 1 ze 40 (fictree, trojice synonymních přídavných jmen a pleonasmy), v rozhodovacích vrstvách na 0. Podmínky neškodnosti teď unslop-cs splní proti všem skillům včetně jadro-2.

**Co se zhoršilo:** skill hlásí méně i u AI textů (82 % → 72 %) a přepis je opatrnější, takže posun skóre AI-ovosti po přepisu klesl na úroveň konkurence. Verdikt proti anti-ai-slop-cz se tím mění z „A je lepší“ (dev-1s-p, interval posunu [+0,001; +0,033], těsně nad nulou) na „shodná kvalita, B je levnější o víc než 20 %“. Jeden běh, intervaly posunu jsou široké.

**Verdikty (dev, jen orientačně):** proti jadro-2, anti-ai-slop-cz a bez-skillu „shodná kvalita, B je levnější o víc než 20 %“, proti humanizer-czech „shodná kvalita, náklady nerozhodují“. Plná verze 1.6.1 a jadro-2 se teď chovají skoro stejně; jadro-2 je o 22 % levnější a v AUC i citlivosti o kousek lepší.
