"""Lidské texty z webu pro regresní případy, které se do repozitáře neukládají.

Případ v pripady.md má místo bloku VSTUP řádek
    ZDROJ: <url> sha256=<prvních 12 znaků> [od="<začátek>"] [do="<konec>"]
Volitelné od/do omezí text na úsek od odstavce, který obsahuje „začátek“, po odstavec
před tím, který obsahuje „konec“ (pro weby, kde obecný extraktor vezme i okolí článku).
Runner text při prvním běhu stáhne, vytáhne z HTML tělo článku, uloží ho do
tools/evaly/cache/ (v .gitignore) a ověří otisk. Když se stránka změní a otisk
nesedí, runner skončí s chybou: případ pak měří jiný text a výsledky by nebyly
srovnatelné. Text patří autorovi a vydavateli, proto v repozitáři zůstává jen odkaz.

Lupa.cz a Root.cz mají vlastní extraktor (stejný vydavatel, stejné HTML), ostatní weby
obecný: odstavce z <article> nebo z těla stránky, u archivů e-mailových konferencí <pre>.
Jen standardní knihovna Pythonu 3.8+.
"""

import hashlib
import html
import os
import re
import urllib.request

KOREN = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CACHE = os.path.join(KOREN, "tools", "evaly", "cache")

_ZDROJ = re.compile(r'^ZDROJ:\s*(\S+)\s+sha256=([0-9a-f]{12})'
                    r'(?:\s+od="([^"]*)")?(?:\s+do="([^"]*)")?\s*$')

# Prvky stránky Lupa.cz, které nejsou textem článku.
_SUM = ("Přidat mezi oblíbené zdroje na Googlu", "Sdílet")
_KONEC = ("Autor článku", "Zdroje informací")


def rozeber_radek(radek):
    """Vrátí (url, otisk, od, do) pro řádek ZDROJ:, jinak None."""
    m = _ZDROJ.match(radek.strip())
    return (m.group(1), m.group(2), m.group(3), m.group(4)) if m else None


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


def _cisty(obsah):
    t = html.unescape(re.sub(r"<[^>]+>", " ", re.sub(r"(?i)<br\s*/?>", "\n", obsah)))
    t = re.sub(r"\s*\n\s*", "\n", t)
    return re.sub(r"[ \t\xa0]+", " ", t).strip()


def text_obecny(stranka):
    """Tělo článku na jiném webu: odstavce a mezititulky z <article> (nebo z těla stránky),
    od prvního odstavce delšího než 100 znaků. Archiv konference: obsah <pre>."""
    s = re.sub(r"(?is)<(script|style|nav|header|footer|aside|form|noscript)\b.*?</\1>|<!--.*?-->",
               " ", stranka)
    clanky = re.findall(r"(?is)<article\b.*?</article>", s)
    oblast = max(clanky, key=len) if clanky else s
    prvky = []
    for tag, obsah in re.findall(r"(?is)<(p|h2|h3)\b[^>]*>(.*?)</\1>", oblast):
        t = re.sub(r"\s+", " ", _cisty(obsah)).strip()
        if t:
            prvky.append((tag, t))
    zacatek = next((i for i, (tag, t) in enumerate(prvky) if tag == "p" and len(t) > 100), None)
    if zacatek is None:
        pre = re.findall(r"(?is)<pre\b[^>]*>(.*?)</pre>", oblast)
        if pre:
            t = _cisty(max(pre, key=len))
            odst = [o.strip().replace("\n", " ") for o in re.split(r"\n\s*\n", t) if o.strip()]
            return "\n\n".join(odst).strip()
        raise ValueError("v HTML není odstavec článku")
    return "\n\n".join(t for _, t in prvky[zacatek:]).strip()


def vyrez(text, od=None, do=None):
    """Úsek od odstavce s „od“ po odstavec před tím s „do“."""
    odst = text.split("\n\n")
    if od:
        i = next((k for k, o in enumerate(odst) if od in o), None)
        if i is None:
            raise ValueError(f"začátek „{od}“ v textu není")
        odst = odst[i:]
    if do:
        j = next((k for k, o in enumerate(odst) if do in o), None)
        if j is None:
            raise ValueError(f"konec „{do}“ v textu není")
        odst = odst[:j]
    return "\n\n".join(odst).strip()


def stahni(url):
    """HTML stránky dekódované podle hlavičky nebo meta charset (staré weby mají windows-1250)."""
    pozadavek = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (unslop-cs evaly)"})
    with urllib.request.urlopen(pozadavek, timeout=60) as r:
        data = r.read()
        kod = r.headers.get_content_charset()
    if not kod:
        m = re.search(rb"charset=[\"']?([A-Za-z0-9_-]+)", data[:4000])
        kod = m.group(1).decode("ascii") if m else "utf-8"
    return data.decode(kod, errors="replace")


def text_stranky(url, od=None, do=None):
    stranka = stahni(url)
    t = text_lupa(stranka) if ("lupa.cz/" in url or "root.cz/" in url) else text_obecny(stranka)
    return vyrez(t, od, do)


def nacti(url, ocekavany_otisk, od=None, do=None, cache=CACHE):
    """Text zdroje z cache, nebo stažený. Při nesouhlasu otisku vyhodí ValueError."""
    os.makedirs(cache, exist_ok=True)
    klic = url if not (od or do) else f"{url}|{od or ''}|{do or ''}"
    soubor = os.path.join(cache, hashlib.sha256(klic.encode()).hexdigest()[:16] + ".txt")
    if os.path.exists(soubor):
        with open(soubor, encoding="utf-8") as f:
            text = f.read()
    else:
        text = text_stranky(url, od, do)
    skutecny = otisk(text)
    if skutecny != ocekavany_otisk:
        raise ValueError(f"otisk textu z {url} je {skutecny}, případ čeká {ocekavany_otisk}; "
                         "stránka se změnila, nebo extraktor vrací jiný text")
    if not os.path.exists(soubor):
        with open(soubor, "w", encoding="utf-8") as f:
            f.write(text)
    return text


if __name__ == "__main__":
    # Výpis otisku a textu pro nový případ:
    #   python3 tools/evaly/zdroje_web.py <url> [začátek] [konec]
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    t = text_stranky(sys.argv[1], *(sys.argv[2:4] + [None, None])[:2])
    print(f"sha256={otisk(t)} slov={len(t.split())}\n")
    print(t)
