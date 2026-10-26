# unslop-cs

Pojistka proti AI slopu v českém textu. Skill pro Claude a další agenty, kteří čtou formát `SKILL.md` (Claude Code, Claude Desktop, Cursor, Codex).

*English: a writing guardrail against AI slop in Czech prose – word, rhythm and structure level, four modes, register profiles, regression cases. Czech-language instructions.*

## Tři úrovně

Většina „humanizérů“ zakáže pár slov (*ponořit se, klíčový, game changer*) a tím končí. To nestačí ze dvou důvodů. Seznamy slov stárnou s každou generací modelů. A trvalý otisk sedí jinde: ve stavbě vět a celého textu. Skill proto pracuje na třech úrovních, s důrazem na dvě hlubší:

| Úroveň | Co chytá | Příklady |
|---|---|---|
| 1 – Slova | slovník, fráze, kalky, typografie | „hraje klíčovou roli“, „adresovat problém“, „na denní bázi“, „—“ v českém textu |
| 2 – Věta | rytmus a skladba | řetězy krátkých vět, trojice, „nejde o X, jde o Y“, přívěsky s „což“, nadbytečné „svůj“, anglický slovosled, jmenný styl |
| 3 – Struktura | tvar celého textu | pointa opakovaná v každém oddílu, falešné prozření, mravoučná pointa, „Závěrem lze konstatovat“, hovorové nadpisy |

Jedno pravidlo platí všude: vágní tvrzení nahraď ověřitelným faktem. Když fakt chybí, skill vloží značku `[OVĚŘIT: …]` a nic si nevymyslí.

## Rozdíly oproti existujícím českým skillům

- **Správná česká typografie.** Česká pomlčka je „–“ s mezerami. Některé skilly radí místo ní spojovník „-“, který je v sazbě typografická chyba. Tenhle skill hlídá anglickou „—“ i rozpočet pomlček, ale spojovník v chatu nebo e-mailu nechá být, protože tak lidé běžně píšou.
- **Pojistky proti přepisování.** Klasické selhání humanizérů je výměna jednoho otisku za jiný: vymyšlená čísla a studie, sekání na útržky, hraná upřímnost, vnucená hovorovost. Skill to bere jako neúspěšný přepis. Smí škrtat a zpřesňovat; fakta ani osobnost nepřidává.
- **Registry.** Útržky jsou na LinkedInu běžné, v eseji působí jako tik. Jištění v reklamě vadí, odborný text ho potřebuje. Tabulka profilů (sociální sítě, blog a esej, e-mail, dokumentace, odborný text, prezentace) určuje přísnost každého pravidla.
- **Česky specifické vzorce.** Kalky a falešní přátelé (*realizovat si, eventuálně, aktuálně, adresovat problém*), nadbytečná zájmena, rituální „tento… tato…“, příklonky mimo své místo, aktuální členění větné, tykání a vykání, „25 %“ a „25%“.
- **Regresní testy.** Dvacet případů v `evals/pripady.md`, z toho sedm čistých, které skill označit nesmí, protože přehnané označování je taky chyba.

## Režimy

- **Psaní** – skill běží potichu, když Claude píše delší český text.
- **Kontrola** – „zkontroluj, co tu zní jako AI“: nálezy podle závažnosti P0–P2, nic se nemění.
- **Přepis** – audit, opravená verze a seznam změn.
- **Úprava souboru** – minimální zásahy přímo v souboru.

## Instalace

**Claude Code jako plugin:**

```
/plugin marketplace add PetrHula/unslop-cs
/plugin install unslop-cs@unslop-cs
```

**Ručně (Claude Code, Cursor, Codex):** zkopíruj složku `skills/unslop-cs` do adresáře se skilly, např. `~/.claude/skills/unslop-cs`.

**Claude.ai a Claude Desktop:** zabal složku `skills/unslop-cs` do ZIPu a nahraj ji v nastavení Claude v části se skilly.

## Struktura

```
skills/unslop-cs/
├── SKILL.md                 hlavní pravidla, režimy, registry, pojistky
├── references/
│   ├── slova.md             slova ve třech úrovních, kalky, fráze, typografie
│   └── vzorce.md            příklady před a po, včetně případů, které zůstávají
└── evals/
    └── pripady.md           regresní případy
```

## Původ a poděkování

- Architektura (tři úrovně, režimy, profily registrů, závažnost, pojistky, sebekontrola, regresní případy) vychází z [jlwin/unslop_ai](https://github.com/jlwin/unslop_ai) od Jean-Luca Winklera (MIT), skillu pro němčinu a angličtinu.
- Část českých vzorců a frází čerpá z [nowork-ai/anti-ai-slop-cz](https://github.com/nowork-ai/anti-ai-slop-cz) (MIT) a [bejek/humanizer-czech](https://github.com/bejek/humanizer-czech) (MIT). Typografická pravidla jsou opravená podle českých norem a příklady přepsané tak, aby nevymýšlely čísla.
- Značka `[OVĚŘIT]` je inspirovaná `[OVERIŤ]` z [kuzmany/slovak-humanizer](https://github.com/kuzmany/slovak-humanizer) (MIT).

Účelem skillu je dobré psaní, obcházení detektorů AI nepodporuje. Kde je třeba použití AI přiznat, skill na tom nic nemění.

## Licence

MIT. Viz [LICENSE](LICENSE).
