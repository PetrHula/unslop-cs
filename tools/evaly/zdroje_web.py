"""Lidské texty z webu pro regresní případy, které se do repozitáře neukládají.

Případ v pripady.md má místo bloku VSTUP řádek
    ZDROJ: <url> sha256=<prvních 12 znaků>
Runner text při prvním běhu stáhne, vytáhne z HTML tělo článku, uloží ho do
tools/evaly/cache/ (v .gitignore) a ověří otisk. Když se stránka změní a otisk
nesedí, runner skončí s chybou: případ pak měří jiný text a výsledky by nebyly
srovnatelné. Text patří autorovi a vydavateli, proto v repozitáři zůstává jen odkaz.

Extraktor umí jen články Lupa.cz (jediný zdroj, který případy používají).
Jen standardní knihovna Pythonu 3.8+.
"""

import hashlib
import html
import os
import re
import urllib.request

KOREN = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CACHE = os.path.join(KOREN, "tools", "evaly", "cache")

_ZDROJ = re.compile(r"^ZDROJ:\s*(\S+)\s+sha256=([0-9a-f]{12})\s*$")

# Prvky stránky Lupa.cz, které nejsou textem článku.
_SUM = ("Přidat mezi oblíbené zdroje na Googlu", "Sdílet")
_KONEC = ("Autor článku", "Zdroje informací")


def rozeber_radek(radek):
    """Vrátí (url, otisk) pro řádek ZDROJ:, jinak None."""
    m = _ZDROJ.match(radek.strip())
    return (m.group(1), m.group(2)) if m else None


def otisk(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]


def text_lupa(stranka):
    """Tělo článku Lupa.cz: perex, odstavce a mezititulky, bez popisků a patičky."""
    prvky = []
    for tag, obsah in re.findall(r"<(p|h2|h3)\b[^>]*>(.*?)</\1>", stranka, re.S):
        t = html.unescape(re.sub(r"<[^>]+>", "", obsah))
        t = re.sub(r"\s+", " ", t).strip()
        if t:
            prvky.append((tag, t))
    zacatek = next((i for i, (tag, t) in enumerate(prvky) if tag == "p" and len(t) > 100), None)
    if zacatek is None:
        raise ValueError("v HTML není odstavec článku")
    vystup = []
    for tag, t in prvky[zacatek:]:
        if t in _KONEC:
            break
        if t in _SUM or t.startswith("Autor:"):
            continue
        vystup.append(t)
    return "\n\n".join(vystup).strip()


def nacti(url, ocekavany_otisk, cache=CACHE):
    """Text zdroje z cache, nebo stažený. Při nesouhlasu otisku vyhodí ValueError."""
    os.makedirs(cache, exist_ok=True)
    soubor = os.path.join(cache, hashlib.sha256(url.encode()).hexdigest()[:16] + ".txt")
    if os.path.exists(soubor):
        with open(soubor, encoding="utf-8") as f:
            text = f.read()
    else:
        if "lupa.cz/" not in url:
            raise ValueError(f"extraktor pro {url} neexistuje (umí jen lupa.cz)")
        pozadavek = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (unslop-cs evaly)"})
        with urllib.request.urlopen(pozadavek, timeout=60) as r:
            stranka = r.read().decode("utf-8", errors="replace")
        text = text_lupa(stranka)
    skutecny = otisk(text)
    if skutecny != ocekavany_otisk:
        raise ValueError(f"otisk textu z {url} je {skutecny}, případ čeká {ocekavany_otisk}; "
                         "stránka se změnila, nebo extraktor vrací jiný text")
    if not os.path.exists(soubor):
        with open(soubor, "w", encoding="utf-8") as f:
            f.write(text)
    return text


if __name__ == "__main__":
    # Výpis otisku a textu pro nový případ: python3 tools/evaly/zdroje_web.py <url>
    import sys
    pozadavek = urllib.request.Request(sys.argv[1], headers={"User-Agent": "Mozilla/5.0 (unslop-cs evaly)"})
    with urllib.request.urlopen(pozadavek, timeout=60) as r:
        t = text_lupa(r.read().decode("utf-8", errors="replace"))
    sys.stdout.reconfigure(encoding="utf-8")
    print(f"sha256={otisk(t)} slov={len(t.split())}\n")
    print(t)
