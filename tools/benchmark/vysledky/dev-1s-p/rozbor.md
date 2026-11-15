# Rozbor dev-1s-p: přepočet dev-1s s mírami nezávislými na štítcích

Stejné běhy jako `dev-1s` (90 dev textů, 1 běh, 450 převzatých běhů, 0 USD), jen nové metriky a pravidlo z 2026-11-15 (PLAN.md, Historie plánu). Dev sada: unslop-cs se na ní ladil, čísla jsou pro něj optimistická.

| skill | lidské s nálezem (vš.) | AI s nálezem (vš.) | AUC hustoty všech nálezů (vš. / rozh.) | plané poplachy v/s (vš.) | změna lidských (rozh.) | přidaná čísla (vš.) |
|---|---|---|---|---|---|---|
| unslop-cs 1.6.0 | 25 % | 82 % | 0,86 / 0,87 | 2,5 % | 0,1 % | 0 % |
| unslop-cs-jadro-2 | 2,5 % | 78 % | 0,89 / 0,87 | 0 % | 0,0 % | 0 % |
| anti-ai-slop-cz | 65 % | 98 % | 0,90 / 0,86 | 7,5 % | 1,0 % | 0 % |
| humanizer-czech | 70 % | 100 % | 0,90 / 0,91 | 20 % | 5,5 % | 2 % |
| bez-skillu | 42,5 % | 100 % | 0,94 / 0,93 | 12,5 % | 2,4 % | 4 % |

**Co obstojí i bez štítků závažnosti:** unslop-cs označí výrazně méně lidských textů (25 % proti 65–70 % u konkurence, interval rozdílu proti oběma celý pod nulou) a lidské texty skoro nemění. To je rozdíl v chování, ne ve štítkování.

**Co neobstojí:** v odlišení AI od lidského textu podle hustoty všech nálezů (AUC) není unslop-cs lepší než konkurence a je o něco horší než model bez skillu (0,86 proti 0,94). Ostatní skilly hlásí nález skoro u každého textu, takže citlivost 98–100 % nic neříká; unslop-cs hlásí méně všude, i u AI textů.

**Rozhodnutí podle nového pravidla (dev, jen orientačně):** proti anti-ai-slop-cz „A je lepší“ (lidské s nálezem i změna lidských v mezích, posun skóre AI-ovosti [+0,001; +0,033] nad nulou; nad nulou je jen těsně), proti humanizer-czech „shodná kvalita, náklady nerozhodují“, proti jadro-2 a bez-skillu „A není lepší“ kvůli lidským textům s nálezem (horní meze +0,40 a +0,14). Starým pravidlem byl verdikt proti anti-ai-slop-cz „A není lepší“; změna pravidla mu tedy pomáhá. Platí až běh na test sadě.

**Pro verzi 1.6.0:** jadro-2 má na lidských textech 1 nález ze 40, plná verze 10. Drobné nálezy na lidských textech jsou přesně to, na co si budou uživatelé stěžovat.

Přidaná čísla: ve 450 bězích jen tři případy (bez-skillu 2, humanizer-czech 1; všechny letopočty). Opakování čísla z originálu se nepočítá.
