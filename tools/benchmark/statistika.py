"""Párové rozdíly, bootstrap po shlucích a rozhodovací pravidlo (krok 7 PLAN.md).

Vstup jsou hodnoty po textech (už zprůměrované přes běhy) pro skill A a B na stejných
textech. Bootstrap převzorkuje shluky (zdrojový lidský text i s AI protějšky), ne texty.
"""
import random
import statistics

MEZE = {"plane_poplachy": 0.03, "poruseni_vyznamu": 0.05, "ztrata_cisel": 0.02}


def bootstrap_rozdil(hodnoty_a, hodnoty_b, shluky, opakovani=10000, seed=0, alfa=0.05):
    """hodnoty_a/b: {id: hodnota}; shluky: {id: shluk}. Vrátí (průměr A − B, dolní, horní).
    Počítá jen texty, které mají hodnotu u A i B."""
    ids = sorted(set(hodnoty_a) & set(hodnoty_b))
    if not ids:
        return None
    rozdil = {i: hodnoty_a[i] - hodnoty_b[i] for i in ids}
    po_shlucich = {}
    for i in ids:
        po_shlucich.setdefault(shluky[i], []).append(rozdil[i])
    klice = sorted(po_shlucich)
    bod = statistics.mean(rozdil.values())
    rnd = random.Random(seed)
    vzorky = []
    for _ in range(opakovani):
        vyber = [klice[rnd.randrange(len(klice))] for _ in klice]
        hodnoty = [x for k in vyber for x in po_shlucich[k]]
        vzorky.append(sum(hodnoty) / len(hodnoty))
    vzorky.sort()
    dolni = vzorky[int(alfa / 2 * opakovani)]
    horni = vzorky[int((1 - alfa / 2) * opakovani) - 1]
    return bod, dolni, horni


def rozhodni(intervaly, kalibrace_ok, naklady_a=None, naklady_b=None, vyznam_ok=True):
    """intervaly: dict s klíči plane_poplachy, poruseni_vyznamu, ztrata_cisel, posun_skore,
    vyhry_ab (každý (bod, dolní, horní) jako A − B, nebo None). kalibrace_ok: soudce A/B prošel
    kalibrací; vyznam_ok: soudce významu prošel kalibrací. Vrátí (verdikt, zdůvodnění)."""
    duvody = []
    ok_neskodnost = True
    for klic, mez in MEZE.items():
        if klic == "poruseni_vyznamu" and not vyznam_ok:
            duvody.append("poruseni_vyznamu: soudce významu neprošel kalibrací, do rozhodnutí nevstupuje")
            continue
        iv = intervaly.get(klic)
        if iv is None:
            duvody.append(f"{klic}: chybí data")
            ok_neskodnost = False
        elif iv[2] > mez:
            duvody.append(f"{klic}: horní mez {iv[2]:+.3f} > {mez:+.3f} (A může být horší)")
            ok_neskodnost = False
        else:
            duvody.append(f"{klic}: horní mez {iv[2]:+.3f} ≤ {mez:+.3f}")
    zlepseni = False
    iv = intervaly.get("posun_skore")
    if iv is not None and iv[1] > 0:
        zlepseni = True
        duvody.append(f"posun skóre AI-ovosti: interval [{iv[1]:+.3f}, {iv[2]:+.3f}] nad nulou")
    iv = intervaly.get("vyhry_ab")
    if iv is not None and kalibrace_ok and iv[1] > 0:
        zlepseni = True
        duvody.append(f"výhry A/B: interval [{iv[1]:+.3f}, {iv[2]:+.3f}] nad nulou")
    if not ok_neskodnost:
        return "A není lepší (zhoršuje plané poplachy nebo zachování významu)", duvody
    if zlepseni:
        return "A je lepší", duvody
    if naklady_a is not None and naklady_b is not None:
        if naklady_a < 0.8 * naklady_b:
            return "shodná kvalita, A je levnější o víc než 20 %", duvody
        if naklady_b < 0.8 * naklady_a:
            return "shodná kvalita, B je levnější o víc než 20 %", duvody
    return "shodná kvalita, náklady nerozhodují", duvody
