#!/usr/bin/env python3
"""Kalibrace soudce ruční slepou anotací (krok 6 PLAN.md).

pripravit: z běhu benchmarku na dev sadě vybere až 20 dvojic přepisů téhož AI textu (první
skill proti ostatním, stejný běh), v náhodném pořadí a bez názvů skillů. Dvojice se shodnými
přepisy vynechá; přepis shodný s originálem v dvojice.md jen označí. Zapíše do
DATA/kalibrace/<stitek>/:
  dvojice.md     originál a přepisy A a B (ke čtení)
  odpovedi.json  šablona: u každé dvojice "lepsi": "A" | "B" | "=" a u prvních 10 dvojic
                 u změněných přepisů "vyznam_A"/"vyznam_B": "ok" | "pridal" | "vynechal" | "oboji"
  klic.json      skutečné pořadí (neotvírat před vyplněním)
vyhodnotit: porovná odpovědi s verdikty soudce (soudce.jsonl). Shoda A/B = podíl dvojic, kde
mají preferenci uživatel i soudce a shodují se. Výsledek se přenese do konfigurace ručně:
"kalibrace_soudce_ok" (A/B ≥ 70 %, jinak párové srovnání do rozhodnutí nevstupuje) a
"kalibrace_vyznam_ok" (význam ≥ 70 %, jinak porušení významu do rozhodnutí nevstupuje).

Podklad: běh s dost AI texty, např.
  python -E -P tools/benchmark/benchmark.py --konfigurace … --stitek kalibrace-1 --jen-ai 20 --behy 1
Použití:
  python -I tools/benchmark/kalibrace_soudce.py pripravit --konfigurace … --stitek kalibrace-1
  python -I tools/benchmark/kalibrace_soudce.py vyhodnotit --konfigurace … --stitek kalibrace-1
"""
import argparse
import json
import os
import random

PRAH = 0.7


def nacti_jsonl(p):
    out = {}
    if os.path.exists(p):
        for r in open(p, encoding="utf-8"):
            z = json.loads(r)
            out[z["klic"]] = z
    return out


def pripravit(cfg, stitek, pocet):
    data = os.path.expanduser(cfg["data"])
    behy = nacti_jsonl(os.path.join(data, "behy", stitek, "behy.jsonl"))
    soud = nacti_jsonl(os.path.join(data, "behy", stitek, "soudce.jsonl"))
    rnd = random.Random(f"{cfg['seed']}:kalibrace:{stitek}")
    def kl(v, strana):
        c = v["klic"].split("|")
        return "|".join(c[1:4] if strana == "a" else c[4:7])

    def norm(s):
        return " ".join((s or "").split())

    # dvojice se shodnými přepisy nic neříkají o preferenci soudce
    dvojice = [v for v in soud.values() if v.get("druh") == "ab" and not v.get("nevyhodnoceno")
               and norm(behy[kl(v, "a")].get("finalni_text")) != norm(behy[kl(v, "b")].get("finalni_text"))]
    dvojice.sort(key=lambda v: v["klic"])
    rnd.shuffle(dvojice)
    dvojice = dvojice[:pocet]
    if len(dvojice) < pocet:
        print(f"POZOR: jen {len(dvojice)} dvojic; pro 20 pusť běh s --jen-ai 20")
    cil = os.path.join(data, "kalibrace", stitek)
    os.makedirs(cil, exist_ok=True)
    md, odpovedi, klic = ["# Kalibrace soudce: slepé dvojice", "",
                          "U každé dvojice rozhodni, který přepis je lepší: čte se jako text psaný člověkem, "
                          "je přirozený a zachovává obsah originálu. Odpovědi piš do odpovedi.json.", ""], {}, {}
    for i, v in enumerate(dvojice, 1):
        ka, kb = "|".join(v["klic"].split("|")[1:4]), "|".join(v["klic"].split("|")[4:7])
        za, zb = behy[ka], behy[kb]
        prohodit = rnd.random() < 0.5
        prvni, druhy = (zb, za) if prohodit else (za, zb)
        tid = za["tid"]
        original = open(os.path.join(data, "dev", tid), encoding="utf-8").read()
        md += [f"## Dvojice {i}", "", "### Originál", "", original.strip(), ""]
        for nazev, z in (("A", prvni), ("B", druhy)):
            md += [f"### Přepis {nazev}", ""]
            if norm(z["finalni_text"]) == norm(original):
                md += ["*(shodný s originálem, text se nezměnil)*", ""]
            else:
                md += [z["finalni_text"].strip(), ""]
        md += ["---", ""]
        odpovedi[str(i)] = {"lepsi": ""}
        if i <= 10:  # význam jen u změněných přepisů; nezměněný text je triviálně v pořádku
            for nazev, z in (("A", prvni), ("B", druhy)):
                if norm(z["finalni_text"]) != norm(original):
                    odpovedi[str(i)][f"vyznam_{nazev}"] = ""
        klic[str(i)] = {"A": prvni["klic"], "B": druhy["klic"], "soudce_ab": v["klic"]}
    with open(os.path.join(cil, "dvojice.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(md))
    with open(os.path.join(cil, "odpovedi.json"), "w", encoding="utf-8") as f:
        json.dump(odpovedi, f, ensure_ascii=False, indent=1)
    with open(os.path.join(cil, "klic.json"), "w", encoding="utf-8") as f:
        json.dump(klic, f, ensure_ascii=False, indent=1)
    print(f"{len(dvojice)} dvojic v {cil}")


def vyhodnotit(cfg, stitek):
    data = os.path.expanduser(cfg["data"])
    cil = os.path.join(data, "kalibrace", stitek)
    odp = json.load(open(os.path.join(cil, "odpovedi.json"), encoding="utf-8"))
    klic = json.load(open(os.path.join(cil, "klic.json"), encoding="utf-8"))
    soud = nacti_jsonl(os.path.join(data, "behy", stitek, "soudce.jsonl"))
    shoda = obe_pref = 0
    vyz_shoda = vyz_celkem = 0
    for i, o in odp.items():
        k = klic[i]
        v = soud[k["soudce_ab"]]
        vitez_klic = {"a": v["klic"].split("|")[1:4], "b": v["klic"].split("|")[4:7]}.get(v["vysledek"])
        soudce_volba = None
        if vitez_klic:
            soudce_volba = "A" if "|".join(vitez_klic) == k["A"] else "B"
        uziv = (o.get("lepsi") or "").strip().upper()
        if uziv in ("A", "B") and soudce_volba:
            obe_pref += 1
            shoda += uziv == soudce_volba
        for strana in ("A", "B"):
            u = (o.get(f"vyznam_{strana}") or "").strip().lower()
            if not u:
                continue
            sv = soud.get("vyznam|" + k[strana])
            if not sv or sv.get("nevyhodnoceno"):
                continue
            vyz_celkem += 1
            vyz_shoda += (u != "ok") == bool(sv["poruseni"])
    vysledek = {"ab_shoda": shoda / obe_pref if obe_pref else None, "ab_dvojic_s_preferenci": obe_pref,
                "vyznam_shoda": vyz_shoda / vyz_celkem if vyz_celkem else None, "vyznam_hodnoceni": vyz_celkem,
                "prah": PRAH}
    vysledek["ab_ok"] = vysledek["ab_shoda"] is not None and vysledek["ab_shoda"] >= PRAH
    vysledek["vyznam_ok"] = vysledek["vyznam_shoda"] is not None and vysledek["vyznam_shoda"] >= PRAH
    with open(os.path.join(cil, "vyhodnoceni.json"), "w", encoding="utf-8") as f:
        json.dump(vysledek, f, ensure_ascii=False, indent=1)
    print(json.dumps(vysledek, ensure_ascii=False, indent=1))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("prikaz", choices=["pripravit", "vyhodnotit"])
    ap.add_argument("--konfigurace", required=True)
    ap.add_argument("--stitek", required=True)
    ap.add_argument("--pocet", type=int, default=20)
    a = ap.parse_args()
    cfg = json.load(open(a.konfigurace, encoding="utf-8"))
    if a.prikaz == "pripravit":
        pripravit(cfg, a.stitek, a.pocet)
    else:
        vyhodnotit(cfg, a.stitek)


if __name__ == "__main__":
    main()
