# tools/koditex – analýza AI-Koditexu (F2)

Skripty bez dat a bez modelu. AI-Koditex v2 (LINDAT 11234/1-6189) i model UDPipe
`czech-pdt-ud-2.5-191206.udpipe` (LINDAT 11234/1-3131, CC BY-NC-SA) do repozitáře nepatří.
Python spouštějte s `-I`, data držte v samostatné složce.

```
pip install ufal.udpipe
python3 -I sample.py AI_Koditex_v2_plain_texts.zip vzorek --per-group 150 --temps 100
python3 -I parse.py czech-pdt-ud-2.5-191206.udpipe vzorek conllu --jobs 2
python3 -I slova.py extract slova.md slova_polozky.json            # ruční opravy: slova_opravy.json
python3 -I slova.py lemmatize czech-pdt-ud-2.5-191206.udpipe slova_polozky.json slova_lemmata.json
python3 -I features.py conllu feat --phrases slova_lemmata.json
# lidská reference z KonTextu (export lemma+tag, počet vět, začátky vět, dotazy)
python3 -I kontext_ref.py feat/koditex_human_kontext.json.gz --lemma-tag lt.csv --sents N \
        --starts starts.csv --queries dotazy.json --phrases slova_lemmata.json
python3 -I compare.py feat out --ref-group koditex_human_kontext --label "Koditex (KonText)"
python3 -I slova_verdikt.py feat slova_lemmata.json slova_srovnani.csv
```

Export z KonTextu (Koditex, `within <chunk mode="wri" & class!="ver" & srclang="cs: čeština"/>`):
`[]` → frekvence víceúrovňově lemma + tag (CSV, všechny řádky), `<s>[]` → frekvence podle lemmatu
a počty pěti dotazů do `dotazy.json` (`kx_coz`, `kx_cimz`, `kx_byt_adj_ze`, `kx_korel`, `kx_qmark`).

## Rozhodnutí v kódu

- **Stejná ID textů** ve všech skupinách: modely se srovnávají na stejném obsahu.
- **První věta** souboru je useknutá promptem; `parse.py` ji označí, analýza ji vynechá.
- **Opakované věty** v rámci textu se počítají jednou (DeepSeek a Llama se zacyklují).
- **Lemmata se záporem a 3. stupněm.** UD lemmatizace PDT zápor i „nej-“ odstraňuje
  (nezbytný → zbytný); `lex_lemma` je vrací, jinak by se míchala opačná slova.
- **Slovesná substantiva.** Model UD 2.5 `VerbForm=Vnoun` nezná. Heuristika: středorodé
  podstatné jméno na -ní/-tí bez -ství/-stí/-letí a bez seznamu výjimek (`common.vnoun_lemma`).
- **Rysy `kx_*`** jsou definované přes poziční značky PDT (XPOS z UDPipe), stejně jako dotazy
  v KonTextu, aby obě strany srovnání měly stejnou definici. Rysy z UD závislostí
  (koordinace, zvratné pasivum, `je + adj. + že/aby` přes strom) jsou jen pro srovnání mezi modely.
- **Klíčovost:** log-ratio (Hardie 2014, +0,5) a G2; nadreprezentace u modelu = LR ≥ 1 a G2 ≥ 15,13.
  Lemma musí být aspoň v 10 % textů (`--min-df`), aby do výsledku nepronikla témata konkrétních textů.
- Ustálené fráze (FRAZE, P0) se počítají i v přesném tvaru (`id#tvar`), ostatní položky na lemmatech.
- **Sjednocení lemmatizace UD a ČNK** (`common.unify_lemma`): technické přípony PDT, množná zájmena
  na jednotná (my → já), varianty (spíš/spíše, -koliv/-koli), zkratky na plné tvary, „dále“ a „raději“.
  Krátká příčestí trpná jdou do `<VPASS>` (UD je lemmatizuje jako přídavné jméno, ČNK jako sloveso).
- Tagset ČNK (16 pozic) dává osobu i příčestí minulému; osoba se proto počítá jen u určitých tvarů.
