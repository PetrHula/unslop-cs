"""Spuštění skillu přes `claude -p` a převod výstupu na společné schéma (krok 4 PLAN.md).

spust(): jedno volání skillu přes adaptér. Stejné přepínače jako regresní evaly
(tools/evaly/runner.py): stream-json, --plugin-dir, režim dontAsk, povolené nástroje
adaptéru, bez uživatelských nastavení a MCP. Chyby infrastruktury hlásí InfraChyba.

normalizuj(): finální text se bere deterministicky mezi řádky <<<VERZE a VERZE>>>.
Nálezy vypíše levný model se schématem JSON (stejně pro všechny skilly): jen přepisuje
nálezy a štítek závažnosti, jak je skill uvedl, nic nehodnotí. Převod štítku na společnou
úroveň dělá adaptér.
"""
import json
import os
import re
import shutil
import subprocess
import tempfile
import time

from cli import InfraChyba, infra_chyba, tokeny_z_usage, zavolej

_VERZE = re.compile(r"<<<VERZE\s*\n(.*?)\n\s*VERZE>>>", re.S)


def spust(adapter, text, model, timeout=900):
    zadani = adapter.zadani(text)
    cmd = ["claude", "-p", zadani, "--output-format", "stream-json", "--verbose",
           "--no-session-persistence", "--strict-mcp-config", "--setting-sources", "project",
           "--permission-mode", "dontAsk", "--model", model]
    if adapter.plugin_dir:
        cmd += ["--plugin-dir", adapter.plugin_dir]
    if adapter.nastroje:
        cmd += ["--allowedTools", adapter.nastroje]
    else:
        cmd += ["--tools", "", "--disable-slash-commands"]
    env = dict(os.environ)
    env.pop("UNSLOP_UDPIPE", None)
    cwd = tempfile.mkdtemp(prefix="unslop-bench-skill-")
    if adapter.vstup_v_souboru:
        with open(os.path.join(cwd, "vstup.txt"), "w", encoding="utf-8") as f:
            f.write(text + "\n")
    t0 = time.time()
    try:
        p = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True, encoding="utf-8",
                           timeout=timeout)
    except subprocess.TimeoutExpired:
        raise InfraChyba(f"timeout {timeout} s")
    finally:
        shutil.rmtree(cwd, ignore_errors=True)
    out = {"vystup": "", "skill_nacten": adapter.skill is None, "nastroje": [], "model": None, "cena": 0.0,
           "tokeny": None, "kroku": None, "cas_s": None, "chyba": None, "zamitnuto": 0}
    for radek in p.stdout.splitlines():
        try:
            u = json.loads(radek)
        except ValueError:
            continue
        if u.get("type") == "system" and u.get("subtype") == "init":
            out["model"] = u.get("model")
        elif u.get("type") == "assistant":
            for c in (u.get("message") or {}).get("content") or []:
                if c.get("type") == "tool_use":
                    out["nastroje"].append(c.get("name"))
                    if (c.get("name") == "Skill" and adapter.skill
                            and adapter.skill in json.dumps(c.get("input"), ensure_ascii=False)):
                        out["skill_nacten"] = True
        elif u.get("type") == "user":
            for c in (u.get("message") or {}).get("content") or []:
                if isinstance(c, dict) and c.get("type") == "tool_result" and c.get("is_error") \
                        and re.search(r"permission|denied|not allowed", str(c.get("content")), re.I):
                    out["zamitnuto"] += 1
        elif u.get("type") == "result":
            out["vystup"] = u.get("result") or ""
            out["cena"] = u.get("total_cost_usd") or 0.0
            out["tokeny"] = tokeny_z_usage(u.get("usage"), u.get("num_turns"))
            out["kroku"] = u.get("num_turns")
            if u.get("is_error"):
                out["chyba"] = u.get("subtype") or "chyba"
    out["cas_s"] = round(time.time() - t0, 1)
    inf = infra_chyba(out["vystup"]) or (infra_chyba(p.stderr) if not out["vystup"] else None)
    if inf:
        raise InfraChyba(inf)
    if not out["vystup"]:
        raise InfraChyba(f"prázdný výstup (kód {p.returncode}): {p.stderr.strip()[:200]}")
    return out


SYSTEM_EXTRAKTOR = "Převádíš výstup nástroje do JSON. Nic nehodnotíš ani nedoplňuješ."

ZADANI_EXTRAKTOR = """Níže je výstup nástroje, který kontroloval český text a hledal místa, která zní jako psaná AI. Vypiš každý nález, který výstup označil jako vadu: místo v textu (krátká citace, jak ji výstup uvádí), stručný popis a štítek závažnosti přesně tak, jak ho výstup uvádí (například „P1“, „vysoká“, „drobné“); když ho neuvádí, dej prázdný řetězec. Nepřidávej nic, co výstup neříká. Nález uvedený mezi nálezy vypiš i tehdy, když ho výstup nakonec v textu ponechal beze změny. Nevypisuj místa, která výstup uvádí jen jako to, co je v pořádku (například v oddílu „ponecháno“ nebo „neproblematické“), ani poznámky, o kterých výstup sám říká, že nejde o znak AI textu (například překlep nebo věcná chyba). Když výstup žádný nález nemá, vrať prázdné pole.

<vystup>
{vystup}
</vystup>"""

SCHEMA_EXTRAKTOR = {
    "type": "object",
    "properties": {"nalezy": {"type": "array", "items": {
        "type": "object",
        "properties": {"misto": {"type": "string"}, "popis": {"type": "string"},
                       "zavaznost_skillu": {"type": "string"}},
        "required": ["misto", "popis", "zavaznost_skillu"]}}},
    "required": ["nalezy"],
}


def finalni_text(vystup):
    m = _VERZE.findall(vystup)
    return m[-1].strip() + "\n" if m else None


def normalizuj(adapter, vystup, model_extraktoru, timeout=300):
    """Vrátí (nalezy, cena_extraktoru). nalezy: [{misto, popis, zavaznost_skillu, uroven}]."""
    bez_verze = _VERZE.sub("<<<VERZE … VERZE>>>", vystup)
    r = zavolej(ZADANI_EXTRAKTOR.format(vystup=bez_verze), model_extraktoru, SYSTEM_EXTRAKTOR,
                timeout=timeout, schema=SCHEMA_EXTRAKTOR)
    nalezy = (r.get("structured") or {}).get("nalezy") or []
    for n in nalezy:
        n["uroven"] = adapter.uroven(n.get("zavaznost_skillu"))
    return nalezy, r["cena"]
