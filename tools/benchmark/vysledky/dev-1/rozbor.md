# Rozbor dev-1

Dev sada, 40 lidských textů rozložených podle vrstev, 40 AI protějšků a 10 textů AI-Koditexu, 4 skilly, 1 běh, Sonnet 5.5 s effortem `medium`, 51,70 USD. Proti `test-1` poprvé se skriptem: unslop-cs načetl obě reference a `metriky.py` doběhl v 96 % běhů.

## Co se ukázalo

1. **Effort `medium` cenu skoro nesnížil:** unslop-cs 0,28 USD na text (test-1 0,29). Cenu určují načtené reference, ne přemýšlení.
2. **Plané poplachy unslop-cs vzrostly na 3 ze 40 lidských textů (7,5 %), stejně jako anti-ai-slop-cz.** Všechny tři jsou nálezy skriptu (shluk slov, dlouhá pomlčka), které výstup skillu sám posoudil jako neplatné („ponechal jako dobovou odbornou formulaci“, „po posouzení nález neplatí“), ale vypsal je se závažností P1. Extraktor je tak započítal. Bez skriptu (test-1) tyto nálezy nevznikaly. Rozpor je ve výstupu skillu: podle `SKILL.md` se závažnost přiřazuje až po posouzení, takže zamítnutý nález nemá mít P1.
3. **Nízká citlivost je hlavně kalibrace závažnosti.** Na AI textech má unslop-cs nějaký nález u 86 % textů (ostatní 98–100 %), ale většinu dává jako P2: úrovně vysoká/střední/nízká 5/73/118. Ostatní skilly dávají vysokou závažnost 52–66krát. S nálezem vysoká/střední je 44 % AI textů (anti 68 %, humanizer 68 %, bez skillu 78 %). Na lidských textech má unslop-cs nějaký nález u 65 % textů, stejně jako anti; výhoda v planých poplaších tedy stojí na tom, jakou závažnost nálezu dá, ne na tom, kolik toho najde.
4. **Zamítnutí ve 4 z 90 běhů unslop-cs:** dvakrát `sed` na úpravu souboru, dvakrát spuštění skriptu s předponou `cd … &&` nebo s proměnnou, které povolení `Bash(python3 *)` nepokryje. Ostatní běhy skript spustily. Benchmark nově končí chybou až nad 10 % běhů (`behy.max_zamitnuti`).

## Co z toho plyne pro skill

- **Zamítnuté nálezy bez závažnosti:** co skill po posouzení nechá být (nález skriptu, který neplatí), patří do „Ponechané nálezy“ bez P0–P2. Mělo by to vrátit plané poplachy k úrovni test-1, aniž by se ztratila citlivost.
- **Kalibrace P1 a P2:** zjistit na dev běhu, které vzorce dává unslop-cs na AI textech jako P2 a na lidských textech skoro nikdy. Ty jsou kandidáti na P1 (případně jen ve shluku). Tím se zvedne citlivost tam, kde neroste riziko planého poplachu.
- **Cena** zůstává na zvláštní krok (reference).

Malý vzorek: 26 lidských a 26 AI textů v rozhodovacích vrstvách, rozdíly v planých poplaších mezi skilly zde nejsou průkazné; rozdíl v citlivosti proti bez-skillu ano (−35 p. b. [−53; −15]).
