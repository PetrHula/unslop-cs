# Rozbor test-2: unslop-cs 1.6.1 na test sadě

První platný běh podle rozhodovacího pravidla z 2026-11-15 (PLAN.md, krok 7 a Historie plánu). Test sada, jen rozhodovací vrstvy (klasika, wiki, úřední): 132 textů (66 lidských, 66 AI), výběr `--vyber-seed test-1` bez vrstev aikoditex, cac a fictree. 4 skilly, 1 běh, effort `medium`, bez soudce. Cena 56,90 USD, nevyhodnocené běhy 0, zamítnuté nástroje 0. Výsledky jen souhrnně; texty test sady se při rozboru nečetly.

## Rozhodnutí

| unslop-cs 1.6.1 proti | bod 1 (lidské s nálezem, změna lidských) | bod 2 (ztráta čísel, přidaná čísla) | bod 3 (posun skóre AI) | rozhodnutí |
|---|---|---|---|---|
| anti-ai-slop-cz | platí | platí (ztráta čísel horní mez +1,9 p. b., mez +2) | nevyšel | shodná kvalita, anti-ai-slop-cz je levnější o víc než 20 % |
| humanizer-czech | platí | platí | [+0,003; +0,059] nad nulou | **unslop-cs je lepší** |
| bez-skillu | platí | platí | nevyšel | shodná kvalita, bez-skillu je levnější o víc než 20 % |

Bod 3 proti humanizer-czech vyšel proto, že humanizer-czech posouvá AI texty mírně k vyššímu skóre AI-ovosti (−0,019), ne proto, že by unslop-cs AI texty výrazně polidštil (+0,006). Posun skóre je u všech skillů blízko nuly, jako v `test-1`.

## Míry nezávislé na štítcích závažnosti

| skill | lidské s nálezem | AI s nálezem | AUC hustoty všech nálezů | změna lidských | ztráta jmen | přidaná čísla | přidaná jména | cena/text |
|---|---|---|---|---|---|---|---|---|
| unslop-cs 1.6.1 | **9,1 %** | 65 % | 0,80 | **0,1 %** | **5,2 %** | 0 % | **3,0 %** | 0,136 USD |
| anti-ai-slop-cz | 57,6 % | 98 % | 0,90 | 1,7 % | 10,8 % | 1,5 % | 9,1 % | 0,101 USD |
| humanizer-czech | 69,7 % | 98 % | 0,88 | 6,0 % | 8,6 % | 0 % | 18,2 % | 0,143 USD |
| bez-skillu | 45,5 % | 100 % | 0,96 | 1,3 % | 11,3 % | 0 % | 12,1 % | 0,040 USD |

Plané poplachy jen s nálezy vysoká/střední (štítky ostatním skillům dává model): unslop-cs 3,0 %, anti-ai-slop-cz 7,6 %, humanizer-czech 24,2 %, bez-skillu 13,6 %.

## Výklad

**V čem je unslop-cs výrazně nejlepší:** lidské texty nechává být. Nález hlásí u 9 % lidských textů, konkurence u 46–70 % (interval rozdílu proti každému skillu celý pod nulou, −25 až −74 p. b.), a lidské texty skoro nemění. Méně ztrácí jména (proti anti-ai-slop-cz a bez-skillu interval celý pod nulou) a méně jich přidává. Ladění 1.6.1 na dev sadě (25 % → 2,5 % lidských s nálezem) se na test sadě potvrdilo jen zčásti: 9,1 % je víc než na dev, ale pořád pětkrát až osmkrát méně než konkurence.

**V čem je nejhorší:** v záchytu AI textu. Bez nálezu nechá 35 % AI textů (konkurence 0–2 %) a v odlišení AI od lidského textu podle hustoty nálezů má nejnižší AUC (0,80 proti 0,88–0,96). Nejslabší je ve vrstvě wiki (nález jen u poloviny AI textů). Ostatní skilly mají vysokou citlivost hlavně proto, že hlásí nález skoro u každého textu; i tak model bez skillu odlišuje AI text podle hustoty nálezů lépe.

**Cena:** 1,3× anti-ai-slop-cz, stejně jako humanizer-czech, 3,4× bez-skillu. Proti `test-1` (0,29 USD/text) poloviční.

**Pozor na ztrátu čísel proti anti-ai-slop-cz:** horní mez +1,9 p. b. je těsně pod mezí +2 p. b. (unslop-cs ztratil průměrně 0,6 % čísel a dat z AI textů, anti-ai-slop-cz žádné).

## Shrnutí

Podle předem stanoveného pravidla je unslop-cs 1.6.1 lepší než humanizer-czech a proti anti-ai-slop-cz a bez-skillu má shodnou kvalitu za vyšší cenu. Pravidlo bere plané poplachy jen jako podmínku „nezhoršit“, takže pětinásobně nižší podíl označených lidských textů k výhře nestačí. Profil skillu je „opatrný redaktor“: málo zbytečných zásahů do lidského textu za cenu toho, že třetinu AI textů pustí bez nálezu.

## Omezení

- 1 běh, bez soudce: porušení významu ani slepé A/B srovnání nejsou k dispozici, shoda mezi běhy se nevykazuje.
- Jen rozhodovací vrstvy, 66 + 66 textů; výklad „všechny vrstvy“ nejde přímo srovnat s `test-1` ani s dev běhy.
- Test sada je teď viděná podruhé (`test-1` se starou verzí skillu a starým pravidlem). Další ladění podle těchto výsledků by vyžadovalo novou nezávislou sadu.
