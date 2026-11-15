#!/usr/bin/env python3
"""Benchmark skillů na reálných textech: jeden příkaz (kroky 4–8 PLAN.md).

Pustí každý skill z konfigurace na vybrané texty sady (dev, nebo zamčený test), převede
výstupy na společné schéma, spočítá metriky, párové rozdíly s bootstrapem a rozhodnutí
podle předem stanoveného pravidla.

Výstupy:
  DATA/behy/<stitek>/behy.jsonl        jeden záznam na běh skillu (texty, nálezy, ceny)
  DATA/behy/<stitek>/soudce.jsonl      verdikty soudce
  tools/benchmark/vysledky/<stitek>/   konfigurace.json, data.json, modely.json, otisky.json,
                                       souhrn.json, vysledky.md (jen souhrny, žádné texty)
Běh jde přerušit a pustit znovu se stejným štítkem: hotové běhy se přeskočí.
Běhy skillů, které se od jiného štítku nezměnily, jde převzít (--prevzit), viz PLAN.md, krok 8.

Použití (spouštět `python -E -P`, rysy potřebují ufal.udpipe a numpy):
  python -E -P tools/benchmark/benchmark.py --konfigurace tools/benchmark/konfigurace.json \\
      --stitek pilot-1 --pilot
  python -E -P tools/benchmark/benchmark.py --konfigurace … --stitek test-1 --sada test --test
  python -E -P tools/benchmark/benchmark.py --konfigurace … --stitek dev-a2 --lidskych 40 --aikoditex 20 \\
      --vyber-seed dev-a1 --prevzit dev-a1
"""
import argparse
import collections
import concurrent.futures
import datetime
import hashlib
import json
import os
import random
import shutil
import statistics
import subprocess
import sys
import threading

KOREN = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, KOREN)
import adaptery  # noqa: E402
import soudce  # noqa: E402
import spoustec  # noqa: E402
import statistika  # noqa: E402
import zachovani  # noqa: E402
from cli import s_opakovanim  # noqa: E402
from generuj import rozdel_prefix  # noqa: E402
from korpus import slov  # noqa: E402

DOMACI = {"aikoditex", "cac", "fictree"}  # vrstvy, ze kterých vznikla pravidla nebo prahy unslop-cs
VRSTVY = ["klasika", "cac", "fictree", "wiki", "uredni", "aikoditex"]
_ZAMEK = threading.Lock()


# ---------------------------------------------------------------------------
# Data

def sha_souboru(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def over_zamek(data):
    zamek = json.load(open(os.path.join(KOREN, "zamek.json"), encoding="utf-8"))
    chyby = [rel for rel, h in zamek["soubory"].items()
             if not os.path.exists(os.path.join(data, rel)) or sha_souboru(os.path.join(data, rel)) != h]
    if chyby:
        raise SystemExit(f"Test sada nesouhlasí se zámkem ({len(chyby)} souborů), např. {chyby[:3]}")
    return zamek


def nacti_texty(data, sada):
    """Všechny texty sady: lidské i AI. Vrátí seznam dictů."""
    manifest = {z["id"]: z for z in json.load(open(os.path.join(data, "manifest.json"),
                                                   encoding="utf-8"))["texty"]}
    koren = os.path.join(data, sada)
    out = []
    for dirpath, _, soubory in os.walk(koren):
        for f in sorted(soubory):
            if not f.endswith(".txt"):
                continue
            rel = os.path.relpath(os.path.join(dirpath, f), koren).replace(os.sep, "/")
            id_ = f[:-4]
            if rel.startswith("texty/"):
                z = manifest[id_]
                out.append({"tid": rel, "y": 0, "vrstva": z["vrstva"], "shluk": z["dilo"], "metoda": "člověk",
                            "model": None, "id_lidsky": id_})
            elif rel.startswith("ai/aikoditex/"):
                out.append({"tid": rel, "y": 1, "vrstva": "aikoditex", "shluk": f"aikoditex:{id_}",
                            "metoda": "aikoditex", "model": rel.split("/")[2], "id_lidsky": None})
            else:
                _, metoda, model, _ = rel.split("/")
                z = manifest[id_]
                out.append({"tid": rel, "y": 1, "vrstva": z["vrstva"], "shluk": z["dilo"], "metoda": metoda,
                            "model": model, "id_lidsky": id_})
    for t in out:
        t["text"] = open(os.path.join(koren, t["tid"]), encoding="utf-8").read()
    return out


def vyber(texty, cfg, a, rnd):
    lidske = [t for t in texty if t["y"] == 0]
    ai = [t for t in texty if t["y"] == 1]
    if a.jen_ai:  # např. podklad pro kalibraci soudce
        ai = sorted(ai, key=lambda t: t["tid"])
        rnd.shuffle(ai)
        vyb, zdroje = [], set()
        for t in ai:
            if len(vyb) >= a.jen_ai:
                break
            if t["id_lidsky"] and t["id_lidsky"] in zdroje:
                continue
            vyb.append(t)
            zdroje.add(t["id_lidsky"])
        return vyb
    if a.pilot:
        vyb = []
        for v in ["klasika", "cac", "fictree", "wiki", "uredni"]:
            kand = [t for t in lidske if t["vrstva"] == v]
            if kand:
                vyb.append(rnd.choice(kand))
        pouzite = set()
        for metoda, n in (("pokracovani", 2), ("chatbot", 2), ("aikoditex", 1)):
            kand = [t for t in ai if t["metoda"] == metoda and t["id_lidsky"] not in pouzite]
            rnd.shuffle(kand)
            modely = set()
            for t in kand:
                if n == 0:
                    break
                if t["model"] in modely:
                    continue
                vyb.append(t)
                modely.add(t["model"])
                pouzite.add(t["id_lidsky"])
                n -= 1
        return vyb
    v = cfg["behy"].get("vyber", {})
    if getattr(a, "lidskych", None):
        lidske = vzorek_po_vrstvach(lidske, a.lidskych, rnd)
    vyb = list(lidske)
    zdroje = {t["id_lidsky"] for t in lidske}
    po_zdroji = collections.defaultdict(list)
    for t in ai:
        if t["metoda"] != "aikoditex" and (not getattr(a, "lidskych", None) or t["id_lidsky"] in zdroje):
            po_zdroji[t["id_lidsky"]].append(t)
    for k in sorted(po_zdroji):
        kand = sorted(po_zdroji[k], key=lambda t: t["tid"])
        rnd.shuffle(kand)
        vyb += kand[:v.get("ai_na_zdroj", 1)]
    ak = sorted((t for t in ai if t["metoda"] == "aikoditex"), key=lambda t: t["tid"])
    rnd.shuffle(ak)
    n_ak = a.aikoditex if getattr(a, "aikoditex", None) is not None else v.get("aikoditex", 30)
    vyb += ak[:n_ak]
    return vyb


def vzorek_po_vrstvach(lidske, n, rnd):
    """n lidských textů, z každé vrstvy úměrně její velikosti (největší zbytky), uvnitř vrstvy náhodně."""
    po_vrstve = collections.defaultdict(list)
    for t in sorted(lidske, key=lambda t: t["tid"]):
        po_vrstve[t["vrstva"]].append(t)
    celkem = len(lidske)
    if n >= celkem:
        return list(lidske)
    podily = {v: n * len(tt) / celkem for v, tt in po_vrstve.items()}
    kolik = {v: int(p) for v, p in podily.items()}
    for v in sorted(podily, key=lambda v: (-(podily[v] - kolik[v]), v))[:n - sum(kolik.values())]:
        kolik[v] += 1
    out = []
    for v in sorted(po_vrstve):
        tt = list(po_vrstve[v])
        rnd.shuffle(tt)
        out += tt[:kolik[v]]
    return out


# ---------------------------------------------------------------------------
# Běhy

class Zapisovac:
    def __init__(self, cesta):
        self.cesta = cesta
        self.hotove = {}
        if os.path.exists(cesta):
            for r in open(cesta, encoding="utf-8"):
                z = json.loads(r)
                self.hotove[z["klic"]] = z

    def zapis(self, z):
        with _ZAMEK:
            self.hotove[z["klic"]] = z
            with open(self.cesta, "a", encoding="utf-8") as f:
                f.write(json.dumps(z, ensure_ascii=False) + "\n")


class Rozpocet:
    def __init__(self, max_usd, utraceno):
        self.max, self.cena, self.stop = max_usd, utraceno, False

    def pridej(self, c):
        with _ZAMEK:
            self.cena += c or 0
            if self.cena > self.max:
                self.stop = True


_OTISKY = {}


def otisk(adapter):
    if adapter.nazev not in _OTISKY:
        _OTISKY[adapter.nazev] = adapter.otisk()
    return _OTISKY[adapter.nazev]


def sha_textu(*casti):
    return hashlib.sha256("\0".join(str(c) for c in casti).encode("utf-8")).hexdigest()[:16]


def puvod(adapter, t, cfg):
    """Co určuje výsledek běhu: obsah skillu, celé zadání s nástroji, model a zadání extraktoru.
    Běh se smí převzít do jiného štítku, jen když se všechno shoduje."""
    return {"otisk": otisk(adapter),
            "zadani_sha": sha_textu(adapter.zadani(t["text"]), adapter.nastroje, adapter.vstup_v_souboru,
                                    bool(adapter.plugin_dir)),
            "model_pozadovany": cfg["behy"]["model_skillu"],
            "effort": cfg["behy"].get("effort_skillu"),
            "extraktor_sha": sha_textu(spoustec.ZADANI_EXTRAKTOR, json.dumps(spoustec.SCHEMA_EXTRAKTOR,
                                                                              sort_keys=True),
                                       cfg["behy"]["model_extraktoru"])}


def _blok_prikazu(zdroj):
    """Část spoustec.spust, která skládá příkaz claude (z textu souboru)."""
    i = zdroj.find('cmd = ["claude"')
    j = zdroj.find("cwd = tempfile", i)
    return zdroj[i:j] if i >= 0 and j > i else None


def starsi_beh_shodny(src, skilly, skilly_cfg, cfg):
    """Pro běhy bez polí původu (štítky před zavedením převzetí): {název skillu: bool}.
    Shoda = stejný otisk skillu, stejný záznam skillu v konfiguraci, stejný model, čistý commit
    a od něj beze změny adaptery.py i složení příkazu claude. extraktor: zda sedí i jeho zadání."""
    cil = os.path.join(KOREN, "vysledky", src)
    try:
        otisky = json.load(open(os.path.join(cil, "otisky.json"), encoding="utf-8"))
        kfg = json.load(open(os.path.join(cil, "konfigurace.json"), encoding="utf-8"))
        meta = json.load(open(os.path.join(cil, "souhrn.json"), encoding="utf-8"))["meta"]
    except (OSError, ValueError, KeyError):
        return {}, False
    commit = meta.get("commit", "")
    if " " in commit or not commit:
        return {}, False
    kod_ok = (subprocess.run(["git", "-C", os.path.dirname(os.path.dirname(KOREN)), "diff", "--quiet", commit,
                              "HEAD", "--", "tools/benchmark/adaptery.py"]).returncode == 0)
    stary_spoustec = git("show", f"{commit}:tools/benchmark/spoustec.py")
    kod_ok = kod_ok and _blok_prikazu(stary_spoustec) == _blok_prikazu(
        open(os.path.join(KOREN, "spoustec.py"), encoding="utf-8").read())
    model_ok = (kfg.get("behy", {}).get("model_skillu") == cfg["behy"]["model_skillu"]
                and kfg.get("behy", {}).get("effort_skillu") == cfg["behy"].get("effort_skillu"))
    stare_spec = {s["nazev"]: s for s in kfg.get("skilly") or []}
    shoda = {}
    for spec, a in zip(skilly_cfg, skilly):
        shoda[spec["nazev"]] = (kod_ok and model_ok and stare_spec.get(spec["nazev"]) == spec
                                and spec["nazev"] in otisky and otisky[spec["nazev"]] == otisk(a))
    extraktor_ok = (spoustec.ZADANI_EXTRAKTOR in stary_spoustec
                    and kfg.get("behy", {}).get("model_extraktoru") == cfg["behy"]["model_extraktoru"])
    return shoda, extraktor_ok


def prevzit(zdroje, skilly, skilly_cfg, vybrane, pocet_behu, cfg, data, zb, rozpocet):
    """Zkopíruje z jiných štítků běhy, které by dopadly stejně (viz puvod). Vrátí počty po skillech."""
    pocty = collections.Counter()
    for src in zdroje:
        p = os.path.join(data, "behy", src, "behy.jsonl")
        if not os.path.exists(p):
            raise SystemExit(f"--prevzit: štítek {src} nemá {p}")
        stare = {}
        for r in open(p, encoding="utf-8"):
            z = json.loads(r)
            stare[z["klic"]] = z
        legacy, extraktor_legacy = starsi_beh_shodny(src, skilly, skilly_cfg, cfg)
        for s in skilly:
            for t in vybrane:
                for k in range(1, pocet_behu + 1):
                    klic = f"{s.nazev}|{t['tid']}|{k}"
                    z = stare.get(klic)
                    if klic in zb.hotove or not z or z.get("nevyhodnoceno") or z.get("chyba"):
                        continue
                    ted = puvod(s, t, cfg)
                    if "zadani_sha" in z:
                        if any(z.get(x) != ted[x] for x in ("otisk", "zadani_sha", "model_pozadovany", "effort")):
                            continue
                        extraktor_ok = z.get("extraktor_sha") == ted["extraktor_sha"]
                    else:
                        if not legacy.get(s.nazev):
                            continue
                        extraktor_ok = extraktor_legacy
                    novy = dict(z, **ted, prevzato_z=src, cena_prevzeti=0.0)
                    if not extraktor_ok or novy.get("nalezy") is None:
                        try:
                            novy["nalezy"], c = spoustec.normalizuj(s, z["vystup"], cfg["behy"]["model_extraktoru"])
                        except spoustec.InfraChyba:
                            continue
                        novy["cena_normalizace"] = novy["cena_prevzeti"] = c
                        novy.pop("chyba_normalizace", None)
                        rozpocet.pridej(c)
                    zb.zapis(novy)
                    pocty[f"{s.nazev} z {src}"] += 1
    return dict(pocty)


def jeden_beh(adapter, t, beh, cfg, rozpocet):
    if rozpocet.stop:
        return None
    b = cfg["behy"]
    r, chyby = s_opakovanim(spoustec.spust, adapter, t["text"], b["model_skillu"],
                            timeout=b.get("timeout_s", 900), effort=b.get("effort_skillu"))
    z = {"klic": f"{adapter.nazev}|{t['tid']}|{beh}", "skill": adapter.nazev, "tid": t["tid"], "beh": beh,
         "infra_chyby": chyby}
    if r is None:
        z["nevyhodnoceno"] = True
        return z
    rozpocet.pridej(r["cena"])
    z.update({k: r.get(k) for k in ("vystup", "skill_nacten", "nastroje", "model", "cena", "tokeny", "kroku",
                                "cas_s", "chyba", "zamitnuto", "chyby_nastroju", "verze_cli")})
    z.update(puvod(adapter, t, cfg))
    z["finalni_text"] = spoustec.finalni_text(r["vystup"])
    try:
        z["nalezy"], c = spoustec.normalizuj(adapter, r["vystup"], b["model_extraktoru"])
        z["cena_normalizace"] = c
        rozpocet.pridej(c)
    except spoustec.InfraChyba as e:
        z["nalezy"], z["chyba_normalizace"] = None, str(e)
    return z


def soudce_vyznam(z, t, cfg, rozpocet):
    if rozpocet.stop:
        return None
    r, chyby = s_opakovanim(soudce.vyznam, t["text"], z["finalni_text"], cfg["behy"]["model_soudce"])
    if r is None:
        return {"klic": "vyznam|" + z["klic"], "nevyhodnoceno": True, "infra_chyby": chyby}
    v, cena = r
    rozpocet.pridej(cena)
    return {"klic": "vyznam|" + z["klic"], "druh": "vyznam", "beh_klic": z["klic"], "cena": cena, **v}


def soudce_ab(za, zb, t, cfg, rozpocet):
    klic = f"ab|{za['klic']}|{zb['klic']}"
    if rozpocet.stop:
        return None
    r, chyby = s_opakovanim(soudce.ab, t["text"], za["finalni_text"], zb["finalni_text"],
                            cfg["behy"]["model_soudce"])
    if r is None:
        return {"klic": klic, "nevyhodnoceno": True, "infra_chyby": chyby}
    vysledek, detail, cena = r
    rozpocet.pridej(cena)
    return {"klic": klic, "druh": "ab", "a": za["skill"], "b": zb["skill"], "tid": t["tid"], "beh": za["beh"],
            "vysledek": {"x": "a", "y": "b"}.get(vysledek, "remiza"), "detail": detail, "cena": cena}


# ---------------------------------------------------------------------------
# Metriky

def auc(skore, y):
    pos = [s for s, v in zip(skore, y) if v == 1]
    neg = [s for s, v in zip(skore, y) if v == 0]
    if not pos or not neg:
        return None
    return sum((p > q) + 0.5 * (p == q) for p in pos for q in neg) / (len(pos) * len(neg))


def fleiss_kappa_bin(hodnoceni):
    """hodnoceni: seznam seznamů 0/1 (běhy na text, aspoň 2). Vrátí kappa nebo None."""
    hodnoceni = [h for h in hodnoceni if len(h) >= 2]
    if not hodnoceni:
        return None
    P, p1, celkem = [], 0, 0
    for h in hodnoceni:
        n, k = len(h), sum(h)
        P.append((k * (k - 1) + (n - k) * (n - k - 1)) / (n * (n - 1)))
        p1 += k
        celkem += n
    p1 /= celkem
    pe = p1 ** 2 + (1 - p1) ** 2
    return None if pe == 1 else (statistics.mean(P) - pe) / (1 - pe)


def prumer(x):
    x = [v for v in x if v is not None]
    return statistics.mean(x) if x else None


def median(x):
    x = [v for v in x if v is not None]
    return statistics.median(x) if x else None


def spocitej_metriky(vybrane, behy, vyznamy, cfg, data, sada):
    """Doplní metriky ke každému běhu a vrátí {(skill, tid): metriky textu}."""
    import numpy as np  # noqa: PLC0415
    from rysy import Analyzator, rysy_f0, skore  # noqa: PLC0415
    model = json.load(open(os.path.join(data, "modely", "ai_skore.json"), encoding="utf-8"))
    an = Analyzator(os.path.expanduser(cfg["udpipe"]), os.path.join(data, "cache_udpipe"))
    bigramy = [tuple(b) for b in model["bigramy"]]
    mu, sd = np.asarray(model["mu"]), np.asarray(model["sd"])

    def zvec(text):
        r = rysy_f0(an.vety(text), model["funkcni"], bigramy)
        return (np.asarray([r[k] for k in model["rysy"]]) - mu) / sd

    t_of = {t["tid"]: t for t in vybrane}
    orig_skore = dict(zip(t_of, skore([t["text"] for t in vybrane], model, an)))
    zbytek = {}
    for t in vybrane:
        if t["metoda"] == "pokracovani":
            lidsky = open(os.path.join(data, sada, "texty", t["id_lidsky"] + ".txt"), encoding="utf-8").read()
            zbytek[t["tid"]] = zvec(rozdel_prefix(lidsky, cfg["generovani"]["prefix_slov"])[1])

    po_textu = collections.defaultdict(list)
    for z in behy:
        if z.get("nevyhodnoceno") or z.get("chyba"):
            continue
        t = t_of[z["tid"]]
        m = {"beh": z["beh"]}
        nal = z.get("nalezy")
        if nal is not None:
            vs = sum(n["uroven"] in ("vysoka", "stredni") for n in nal)
            m["nalezu_vs"] = vs
            m["nalezu"] = len(nal)
            m["ma_nalez_vs"] = int(vs > 0)
            m["ma_nalez"] = int(len(nal) > 0)  # jakýkoli nález: nezávisí na štítcích závažnosti skillu
            m["hustota_vs"] = 1000 * vs / max(1, slov(t["text"]))
            m["hustota"] = 1000 * len(nal) / max(1, slov(t["text"]))
        final = z.get("finalni_text")
        m["chybi_verze"] = int(final is None)
        final = final or t["text"]
        m["zmeneny_podil"] = zachovani.zmeneny_podil(t["text"], final)
        m["skore_po"] = skore([final], model, an)[0]
        m["posun_skore"] = orig_skore[t["tid"]] - m["skore_po"]
        m["pridana_cisla"] = int(zachovani.pridana_cisla(t["text"], final) > 0)
        if t["y"] == 1:
            k, n = zachovani.cisla_a_data(t["text"], final)
            m["ztrata_cisel"] = None if n == 0 else 1 - k / n
            vo, vp = an.vety(t["text"]), an.vety(final)
            k, n = zachovani.jmena(vo, vp)
            m["ztrata_jmen"] = None if n == 0 else 1 - k / n
            m["pridana_jmena"] = int(zachovani.pridana_jmena(vo, vp) > 0)
            v = vyznamy.get("vyznam|" + z["klic"])
            m["poruseni_vyznamu"] = int(v["poruseni"]) if v and not v.get("nevyhodnoceno") else None
            if t["tid"] in zbytek:
                ref = zbytek[t["tid"]]
                m["vzdalenost_pred"] = float(np.linalg.norm(zvec(t["text"]) - ref))
                m["vzdalenost_po"] = float(np.linalg.norm(zvec(final) - ref))
                m["vzdalenost_zmena"] = m["vzdalenost_pred"] - m["vzdalenost_po"]
        m.update(cena=(z.get("cena") or 0), vstup_tokenu=(z.get("tokeny") or {}).get("vstup_celkem"),
                 vystup_tokenu=(z.get("tokeny") or {}).get("vystup"), kroku=z.get("kroku"), cas_s=z.get("cas_s"),
                 skill_nacten=int(bool(z.get("skill_nacten"))), zamitnuto=int((z.get("zamitnuto") or 0) > 0),
                 chyba_nastroje=None if "chyby_nastroju" not in z else int(bool(z["chyby_nastroju"])))
        po_textu[(z["skill"], z["tid"])].append(m)
    return po_textu, orig_skore


def agreguj(po_textu, vybrane, skilly):
    """Průměry přes běhy na text a souhrn po skillech a vrstvách."""
    t_of = {t["tid"]: t for t in vybrane}
    na_text = {}
    for (s, tid), mm in po_textu.items():
        klice = {k for m in mm for k in m if k != "beh"}
        na_text[(s, tid)] = {k: prumer([m.get(k) for m in mm]) for k in klice}
        na_text[(s, tid)]["_behy_vs"] = [m["ma_nalez_vs"] for m in mm if "ma_nalez_vs" in m]
    souhrn = {}
    for s in skilly:
        for vrstva in VRSTVY + ["vse", "rozhodovaci"]:
            def patri(t):
                return (vrstva == "vse" or t["vrstva"] == vrstva
                        or (vrstva == "rozhodovaci" and t["vrstva"] not in DOMACI))
            tt = [t for t in vybrane if patri(t) and (s, t["tid"]) in na_text]
            if not tt:
                continue
            lid = [na_text[(s, t["tid"])] for t in tt if t["y"] == 0]
            ai = [na_text[(s, t["tid"])] for t in tt if t["y"] == 1]
            vs = [na_text[(s, t["tid"])] for t in tt]
            souhrn[f"{s}|{vrstva}"] = {
                "textu_lidskych": len(lid), "textu_ai": len(ai),
                "lidske_s_nalezem": prumer([x.get("ma_nalez") for x in lid]),
                "ai_s_nalezem": prumer([x.get("ma_nalez") for x in ai]),
                "auc_hustoty_vse": auc([x.get("hustota", 0) for x in vs], [t["y"] for t in tt]),
                "plane_poplachy": prumer([x.get("ma_nalez_vs") for x in lid]),
                "citlivost": prumer([x.get("ma_nalez_vs") for x in ai]),
                "auc_hustoty": auc([x.get("hustota_vs", 0) for x in vs], [t["y"] for t in tt]),
                "kappa_3_behu": fleiss_kappa_bin([x["_behy_vs"] for x in vs]),
                "posun_skore_ai": prumer([x.get("posun_skore") for x in ai]),
                "posun_skore_lidske": prumer([x.get("posun_skore") for x in lid]),
                "vzdalenost_zmena": prumer([x.get("vzdalenost_zmena") for x in ai]),
                "ztrata_cisel": prumer([x.get("ztrata_cisel") for x in ai]),
                "ztrata_jmen": prumer([x.get("ztrata_jmen") for x in ai]),
                "pridana_cisla_ai": prumer([x.get("pridana_cisla") for x in ai]),
                "pridana_cisla_lidske": prumer([x.get("pridana_cisla") for x in lid]),
                "pridana_jmena_ai": prumer([x.get("pridana_jmena") for x in ai]),
                "poruseni_vyznamu": prumer([x.get("poruseni_vyznamu") for x in ai]),
                "zmeneny_podil_lidske": prumer([x.get("zmeneny_podil") for x in lid]),
                "zmeneny_podil_ai": prumer([x.get("zmeneny_podil") for x in ai]),
                "chybi_verze": prumer([x.get("chybi_verze") for x in vs]),
                "skill_nacten": prumer([x.get("skill_nacten") for x in vs]),
                "zamitnuto_podil": prumer([x.get("zamitnuto") for x in vs]),
                "chyba_nastroje_podil": prumer([x.get("chyba_nastroje") for x in vs]),
                "cena_median": median([x.get("cena") for x in vs]),
                "vstup_tokenu_median": median([x.get("vstup_tokenu") for x in vs]),
                "vystup_tokenu_median": median([x.get("vystup_tokenu") for x in vs]),
                "kroku_median": median([x.get("kroku") for x in vs]),
                "cas_s_median": median([x.get("cas_s") for x in vs]),
            }
    return na_text, souhrn


def srovnani(a, b, na_text, vybrane, ab_verdikty, cfg):
    """Párové intervaly A − B na rozhodovacích vrstvách a rozhodnutí."""
    tt = [t for t in vybrane if t["vrstva"] not in DOMACI]
    shluky = {t["tid"]: t["shluk"] for t in tt}
    seed = cfg["seed"]

    def hodnoty(s, klic, y):
        return {t["tid"]: na_text[(s, t["tid"])][klic] for t in tt
                if t["y"] == y and (s, t["tid"]) in na_text and na_text[(s, t["tid"])].get(klic) is not None}

    iv = {}
    for klic, metrika, y in (("lidske_s_nalezem", "ma_nalez", 0), ("zmena_lidskych", "zmeneny_podil", 0),
                             ("poruseni_vyznamu", "poruseni_vyznamu", 1),
                             ("ztrata_cisel", "ztrata_cisel", 1), ("pridana_cisla", "pridana_cisla", 1),
                             ("posun_skore", "posun_skore", 1)):
        iv[klic] = statistika.bootstrap_rozdil(hodnoty(a, metrika, y), hodnoty(b, metrika, y), shluky, seed=seed)
    vyhry = collections.defaultdict(list)
    for v in ab_verdikty:
        if v.get("nevyhodnoceno") or v["a"] != a or v["b"] != b or v["tid"] not in shluky:
            continue
        vyhry[v["tid"]].append({"a": 1, "b": -1}.get(v["vysledek"], 0))
    vy = {k: statistics.mean(x) for k, x in vyhry.items()}
    iv["vyhry_ab"] = statistika.bootstrap_rozdil(vy, {k: 0.0 for k in vy}, shluky, seed=seed) if vy else None
    # jen k výkladu, do rozhodnutí nevstupují (pravidlo v PLAN.md, krok 7)
    info = {}
    for klic, metrika, y in (("plane_poplachy_vs", "ma_nalez_vs", 0), ("citlivost_vs", "ma_nalez_vs", 1),
                             ("ai_s_nalezem", "ma_nalez", 1), ("ztrata_jmen", "ztrata_jmen", 1),
                             ("pridana_jmena", "pridana_jmena", 1)):
        info[klic] = statistika.bootstrap_rozdil(hodnoty(a, metrika, y), hodnoty(b, metrika, y), shluky, seed=seed)
    na = median([na_text[(a, t["tid"])].get("cena") for t in tt if (a, t["tid"]) in na_text])
    nb = median([na_text[(b, t["tid"])].get("cena") for t in tt if (b, t["tid"]) in na_text])
    verdikt, duvody = statistika.rozhodni(iv, cfg["behy"].get("kalibrace_soudce_ok", False), na, nb,
                                          vyznam_ok=cfg["behy"].get("kalibrace_vyznam_ok", True))
    return {"a": a, "b": b, "intervaly": iv, "vyklad": info, "cena_a": na, "cena_b": nb,
            "verdikt": verdikt, "duvody": duvody,
            "vyhry_ab_textu": len(vy), "kalibrace_soudce_ok": cfg["behy"].get("kalibrace_soudce_ok", False)}


# ---------------------------------------------------------------------------
# Zpráva

def f(x, n=3):
    return "–" if x is None else (f"{x:.{n}f}" if isinstance(x, float) else str(x))


def _pomer(x, y):
    return None if not x or not y else x / y


def vyklad(sc, souhrn):
    """Řádky „k výkladu“: poměr ceny proti poměru kvality. Do rozhodnutí nevstupuje."""
    a = souhrn.get(f"{sc['a']}|rozhodovaci") or {}
    b = souhrn.get(f"{sc['b']}|rozhodovaci") or {}
    r = ["K výkladu (do rozhodnutí nevstupuje):", ""]
    pc = _pomer(sc.get("cena_a"), sc.get("cena_b"))
    if pc:
        r.append(f"- cena A/B: {pc:.1f}×")
    for klic, popis in (("lidske_s_nalezem", "lidské texty s nálezem"),
                        ("plane_poplachy", "plané poplachy (vysoká/střední)")):
        pa, pb = a.get(klic), b.get(klic)
        if pa is not None and pb is not None:
            r.append(f"- {popis}: A {pa:.1%}, B {pb:.1%}" + (f" (B/A {pb / pa:.1f}×)" if pa else ""))
    for k, iv in (sc.get("vyklad") or {}).items():
        if iv:
            r.append(f"- {k} A − B: {iv[0]:+.3f} [{iv[1]:+.3f}, {iv[2]:+.3f}]")
    return r + [""]


def zprava(meta, souhrn, srovnani_list, skilly):
    r = [f"# Benchmark skillů: {meta['stitek']}", "",
         f"- Datum: {meta['datum']}; sada: {meta['sada']}; textů: {meta['textu']} "
         f"(lidských {meta['lidskych']}, AI {meta['ai']}); běhů na text: {meta['behy']}",
         f"- Commit: `{meta['commit']}`; otisky skillů: "
         + ", ".join(f"{k} `{v}`" for k, v in meta["otisky"].items()),
         f"- Model skillu: {meta['model_skillu']} (effort {meta.get('effort_skillu') or 'výchozí'}"
         f"{'; Claude Code ' + ', '.join(meta['verze_cli']) if meta.get('verze_cli') else ''}); "
         f"soudce: {meta['model_soudce']}; normalizace: "
         f"{meta['model_extraktoru']}; modely z běhů: {', '.join(meta['modely_z_behu']) or '?'}",
         f"- Cena celkem: {meta['cena']:.2f} USD; nevyhodnocené běhy: {meta['nevyhodnoceno']}"
         + (f"; převzaté běhy: {meta['prevzato']}" if meta.get("prevzato") else ""), ""]
    zam = [s for s in skilly if (souhrn.get(f"{s}|vse") or {}).get("zamitnuto_podil")]
    if zam:
        r += ["**POZOR: zamítnuté nástroje** (skill neběžel, jak je navržený): "
              + ", ".join(f"{s} {souhrn[f'{s}|vse']['zamitnuto_podil']:.0%} běhů" for s in zam), ""]
    for sc in srovnani_list:
        r.append(f"## {sc['a']} proti {sc['b']}: {sc['verdikt']}")
        r.append("")
        r.append("Rozhodovací vrstvy (bez " + ", ".join(sorted(DOMACI)) + "); A − B, 95% interval "
                 "z bootstrapu po shlucích. Kalibrace soudce: "
                 + ("prošla" if sc["kalibrace_soudce_ok"] else "neprošla nebo neproběhla (A/B jen informativně)"))
        r.append("")
        for d in sc["duvody"]:
            r.append(f"- {d}")
        for k, iv in sc["intervaly"].items():
            if iv:
                r.append(f"- {k}: {iv[0]:+.3f} [{iv[1]:+.3f}, {iv[2]:+.3f}]")
        r.append("")
        r += vyklad(sc, souhrn)
    pole = [("lidske_s_nalezem", "lidské s nálezem"), ("ai_s_nalezem", "AI s nálezem"),
            ("auc_hustoty_vse", "AUC hustoty"),
            ("plane_poplachy", "plané poplachy v/s"), ("citlivost", "citlivost v/s"), ("auc_hustoty", "AUC v/s"),
            ("kappa_3_behu", "kappa"),
            ("posun_skore_ai", "posun skóre AI"), ("vzdalenost_zmena", "přiblížení k autorovi"),
            ("ztrata_cisel", "ztráta čísel"), ("pridana_cisla_ai", "přidaná čísla"),
            ("ztrata_jmen", "ztráta jmen"), ("pridana_jmena_ai", "přidaná jména"),
            ("poruseni_vyznamu", "porušení významu"), ("zmeneny_podil_lidske", "změna lidských"),
            ("posun_skore_lidske", "posun skóre lidských"), ("chybi_verze", "bez verze"),
            ("cena_median", "cena/text"), ("kroku_median", "kroků"), ("cas_s_median", "čas s"),
            ("zamitnuto_podil", "zamítnutí"), ("chyba_nastroje_podil", "chyba nástroje")]
    for vrstva in ["rozhodovaci", "vse"] + VRSTVY:
        radky = [(s, souhrn.get(f"{s}|{vrstva}")) for s in skilly if souhrn.get(f"{s}|{vrstva}")]
        if not radky:
            continue
        r.append(f"### Vrstva: {vrstva}")
        r.append("")
        r.append("| skill | lidských / AI | " + " | ".join(p for _, p in pole) + " |")
        r.append("|---|---|" + "---|" * len(pole))
        for s, x in radky:
            r.append(f"| {s} | {x['textu_lidskych']} / {x['textu_ai']} | "
                     + " | ".join(f(x.get(k)) for k, _ in pole) + " |")
        r.append("")
    r.append("Lidské / AI s nálezem = podíl lidských / AI textů s aspoň jedním nálezem jakékoli závažnosti "
             "(nezávisí na tom, jak skill štítkuje závažnost); AUC hustoty = odlišení AI a lidských textů podle "
             "počtu všech nálezů na 1000 slov. Plané poplachy v/s a citlivost v/s = totéž jen s nálezy vysoké "
             "nebo střední závažnosti. Přidaná čísla / jména = podíl přepisů AI textů s aspoň jedním číslem "
             "či datem / vlastním jménem, které v originálu není. Zamítnutí a chyba nástroje = podíl běhů, kde skill narazil na "
             "zamítnutý nebo chybný nástroj (chyba nástroje se zaznamenává od 2026-11-13). "
             "Posun skóre = skóre AI-ovosti před minus po přepisu (kladné = blíž lidským textům). "
             "Přiblížení k autorovi = o kolik se rysy F0 pokračování přiblížily skutečnému pokračování autora. "
             "Ztráty a porušení významu jen u AI textů. Kappa = shoda běhů v tom, zda text má nález.")
    return "\n".join(r) + "\n"


def git(*args):
    try:
        return subprocess.run(["git", "-C", os.path.dirname(os.path.dirname(KOREN))] + list(args),
                              capture_output=True, text=True, timeout=30).stdout.strip()
    except Exception:  # noqa: BLE001
        return ""


# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--konfigurace", required=True)
    ap.add_argument("--stitek", required=True)
    ap.add_argument("--sada", choices=["dev", "test"], default="dev")
    ap.add_argument("--test", action="store_true", help="odemkne test sadu (štítek musí začínat test-)")
    ap.add_argument("--pilot", action="store_true", help="5 lidských a 5 AI textů z dev, 1 běh")
    ap.add_argument("--jen-ai", type=int, help="jen N AI textů (každý z jiného zdroje), bez lidských")
    ap.add_argument("--behy", type=int, help="přebije behy.pocet_behu z konfigurace")
    ap.add_argument("--max-usd", type=float, help="strop ceny běhu")
    ap.add_argument("--bez-soudce", action="store_true", help="nepouštět soudce (význam, A/B)")
    ap.add_argument("--prevzit", action="append", default=[], metavar="STITEK",
                    help="převzít shodné běhy z jiného štítku (stejný otisk skillu, zadání, model); lze opakovat")
    ap.add_argument("--vyber-seed", metavar="STITEK",
                    help="výběr textů jako u jiného štítku (výchozí: vlastní štítek); kvůli --prevzit")
    ap.add_argument("--lidskych", type=int,
                    help="jen N lidských textů (rozložených podle vrstev) a AI protějšky jen k nim")
    ap.add_argument("--aikoditex", type=int, help="přebije behy.vyber.aikoditex")
    ap.add_argument("--povolit-zamitnuti", action="store_true",
                    help="nezastavit běh a nekončit kódem 2, když skill narazí na zamítnutý nástroj")
    ap.add_argument("--jen-prevzate", action="store_true",
                    help="jen přepočet metrik z převzatých běhů; skončí chybou, kdyby měl nějaký skill platit")
    a = ap.parse_args()
    cfg = json.load(open(a.konfigurace, encoding="utf-8"))
    data = os.path.expanduser(cfg["data"])
    if a.sada == "test":
        if not a.test or not a.stitek.startswith("test-"):
            raise SystemExit("Test sada: přidej --test a štítek začínající test-.")
        if a.pilot:
            raise SystemExit("Pilot běží jen na dev sadě.")
        over_zamek(data)
    b = cfg["behy"]
    pocet_behu = a.behy or (1 if a.pilot else b["pocet_behu"])
    skilly_cfg = cfg["skilly"] or [{"nazev": "unslop-cs", "adapter": "unslop_cs", "plugin_dir": "."},
                                   {"nazev": "bez-skillu", "adapter": "bez_skillu"}]
    skilly = [adaptery.nacti(s) for s in skilly_cfg]
    rnd = random.Random(f"{cfg['seed']}:{a.vyber_seed or a.stitek}:vyber")
    vybrane = vyber(nacti_texty(data, a.sada), cfg, a, rnd)
    t_of = {t["tid"]: t for t in vybrane}
    print(f"textů {len(vybrane)} (lidských {sum(t['y'] == 0 for t in vybrane)}), skillů {len(skilly)}, "
          f"běhů {pocet_behu}", flush=True)

    behy_dir = os.path.join(data, "behy", a.stitek)
    os.makedirs(behy_dir, exist_ok=True)
    zb = Zapisovac(os.path.join(behy_dir, "behy.jsonl"))
    zs = Zapisovac(os.path.join(behy_dir, "soudce.jsonl"))
    utraceno = sum(z.get("cena_prevzeti") or 0 if z.get("prevzato_z")
                   else (z.get("cena") or 0) + (z.get("cena_normalizace") or 0) for z in zb.hotove.values()) \
        + sum(z.get("cena") or 0 for z in zs.hotove.values())
    rozpocet = Rozpocet(a.max_usd or b.get("max_usd", 10.0), utraceno)
    if a.prevzit:
        pocty = prevzit(a.prevzit, skilly, skilly_cfg, vybrane, pocet_behu, cfg, data, zb, rozpocet)
        print("převzato: " + (", ".join(f"{k} {n}" for k, n in sorted(pocty.items())) or "nic"), flush=True)

    ulohy = [(s, t, k) for t in vybrane for s in skilly for k in range(1, pocet_behu + 1)
             if f"{s.nazev}|{t['tid']}|{k}" not in zb.hotove]
    if a.jen_prevzate and ulohy:
        raise SystemExit(f"--jen-prevzate: {len(ulohy)} běhů nejde převzít (např. {ulohy[0][0].nazev} "
                         f"{ulohy[0][1]['tid']}); nic se nespustilo.")
    hotovo, zamitnuto = collections.Counter(), collections.Counter()
    with concurrent.futures.ThreadPoolExecutor(max_workers=b.get("jobs", 4)) as ex:
        for i, fut in enumerate(concurrent.futures.as_completed(
                [ex.submit(jeden_beh, s, t, k, cfg, rozpocet) for s, t, k in ulohy]), 1):
            z = fut.result()
            if z:
                zb.zapis(z)
                print(f"[{i}/{len(ulohy)}] {z['klic']} {'nevyhodnoceno' if z.get('nevyhodnoceno') else 'ok'} "
                      f"{rozpocet.cena:.2f} USD" + (f" zamítnuto {z['zamitnuto']}" if z.get("zamitnuto") else ""),
                      flush=True)
                hotovo[z["skill"]] += 1
                zamitnuto[z["skill"]] += bool(z.get("zamitnuto"))
                if (not a.povolit_zamitnuti and not rozpocet.stop and hotovo[z["skill"]] >= 2
                        and zamitnuto[z["skill"]] == hotovo[z["skill"]]):
                    rozpocet.stop = True  # další úlohy se nespustí; běžící doběhnou
                    print(f"POZOR: {z['skill']} má zamítnutý nástroj ve všech prvních bězích; běh zastaven. "
                          "Oprav prostředí, nebo pusť s --povolit-zamitnuti.", flush=True)

    behy = [z for z in zb.hotove.values() if z["tid"] in t_of]
    if not a.bez_soudce:
        ulohy_s = []
        for z in behy:
            t = t_of[z["tid"]]
            if t["y"] == 1 and z.get("finalni_text") and "vyznam|" + z["klic"] not in zs.hotove:
                ulohy_s.append(("v", z, None, t))
        prvni = skilly[0].nazev
        for z in behy:
            t = t_of[z["tid"]]
            if z["skill"] == prvni or t["y"] != 1 or not z.get("finalni_text"):
                continue
            za = zb.hotove.get(f"{prvni}|{z['tid']}|{z['beh']}")
            if za and za.get("finalni_text") and f"ab|{za['klic']}|{z['klic']}" not in zs.hotove:
                ulohy_s.append(("ab", za, z, t))
        with concurrent.futures.ThreadPoolExecutor(max_workers=b.get("jobs", 4)) as ex:
            futs = [ex.submit(soudce_vyznam, z1, t, cfg, rozpocet) if druh == "v"
                    else ex.submit(soudce_ab, z1, z2, t, cfg, rozpocet) for druh, z1, z2, t in ulohy_s]
            for fut in concurrent.futures.as_completed(futs):
                v = fut.result()
                if v:
                    zs.zapis(v)
        print(f"soudce: {len(ulohy_s)} verdiktů; {rozpocet.cena:.2f} USD", flush=True)
    if rozpocet.stop:
        print(f"POZOR: běh zastaven (strop {rozpocet.max} USD nebo zamítnuté nástroje); výsledky jsou neúplné",
              flush=True)

    vyznamy = {k: v for k, v in zs.hotove.items() if k.startswith("vyznam|")}
    ab_verdikty = [v for k, v in zs.hotove.items() if k.startswith("ab|")]
    po_textu, _ = spocitej_metriky(vybrane, behy, vyznamy, cfg, data, a.sada)
    nazvy = [s.nazev for s in skilly]
    na_text, souhrn = agreguj(po_textu, vybrane, nazvy)
    srovnani_list = [srovnani(nazvy[0], s, na_text, vybrane, ab_verdikty, cfg) for s in nazvy[1:]]

    cil = os.path.join(KOREN, "vysledky", a.stitek)
    os.makedirs(cil, exist_ok=True)
    shutil.copy(a.konfigurace, os.path.join(cil, "konfigurace.json"))
    seznam = "\n".join(sorted(t_of))
    data_info = {"manifest_sha256": sha_souboru(os.path.join(data, "manifest.json")),
                 "rozdeleni_sha256": sha_souboru(os.path.join(data, "rozdeleni.json")),
                 "zamek_sha256": sha_souboru(os.path.join(KOREN, "zamek.json")),
                 "ai_skore_sha256": sha_souboru(os.path.join(data, "modely", "ai_skore.json")),
                 "vybrane_texty_sha256": hashlib.sha256(seznam.encode()).hexdigest(), "sada": a.sada,
                 "textu": len(vybrane)}
    modely = sorted({z.get("model") for z in behy if z.get("model")})
    otisky = {s.nazev: s.otisk() for s in skilly}
    meta = {"stitek": a.stitek, "datum": datetime.datetime.now().astimezone().strftime("%Y-%m-%d %H:%M %z"),
            "sada": a.sada, "textu": len(vybrane), "lidskych": sum(t["y"] == 0 for t in vybrane),
            "ai": sum(t["y"] == 1 for t in vybrane), "behy": pocet_behu,
            "commit": git("rev-parse", "--short", "HEAD") + (" (neuložené změny)" if git(
                "status", "--porcelain", "--", "tools/benchmark", ":!tools/benchmark/vysledky") else ""),
            "otisky": otisky, "model_skillu": b["model_skillu"], "effort_skillu": b.get("effort_skillu"),
            "verze_cli": sorted({z["verze_cli"] for z in behy if z.get("verze_cli")}),
            "model_soudce": b["model_soudce"],
            "model_extraktoru": b["model_extraktoru"], "modely_z_behu": modely, "cena": rozpocet.cena,
            "nevyhodnoceno": sum(bool(z.get("nevyhodnoceno")) for z in behy), "zastaveno_rozpoctem": rozpocet.stop,
            "prevzato": sum(bool(z.get("prevzato_z")) for z in behy),
            "prevzato_ze": sorted({z["prevzato_z"] for z in behy if z.get("prevzato_z")}),
            "vyber_seed": a.vyber_seed or a.stitek, "lidskych_vzorek": a.lidskych, "aikoditex": a.aikoditex}
    for nazev, obsah in (("data.json", data_info), ("modely.json", {"skill": modely,
                                                                   "effort_skillu": b.get("effort_skillu"),
                                                                   "soudce": b["model_soudce"],
                                                                   "extraktor": b["model_extraktoru"]}),
                         ("otisky.json", otisky),
                         ("souhrn.json", {"meta": meta, "souhrn": souhrn, "srovnani": srovnani_list})):
        with open(os.path.join(cil, nazev), "w", encoding="utf-8", newline="\n") as fh:
            json.dump(obsah, fh, ensure_ascii=False, indent=1)
    md = zprava(meta, souhrn, srovnani_list, nazvy)
    with open(os.path.join(cil, "vysledky.md"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(md)
    print(md)
    print(f"Uloženo do {cil}; běhy po textech v {behy_dir}", file=sys.stderr)
    mez = b.get("max_zamitnuti", 0.1)  # ojedinělé zamítnutí (např. „cd … && python3“) běh neznehodnotí
    zam = {s: souhrn[f"{s}|vse"]["zamitnuto_podil"] for s in nazvy
           if ((souhrn.get(f"{s}|vse") or {}).get("zamitnuto_podil") or 0) > mez}
    if zam and not a.povolit_zamitnuti:
        print(f"POZOR: zamítnuté nástroje nad {mez:.0%} běhů u "
              + ", ".join(f"{s} ({p:.0%})" for s, p in zam.items())
              + "; výsledky tohoto skillu neodpovídají jeho návrhu. Oprav prostředí, nebo pusť s "
              "--povolit-zamitnuti.", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
