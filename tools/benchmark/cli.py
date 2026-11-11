"""Volání `claude -p` pro benchmark: bez nástrojů, bez pluginů, s vlastním systémovým promptem.

Znovu používá z tools/evaly/runner.py detekci chyb infrastruktury (`infra_chyba`) a čtení
tokenů (`tokeny_z_usage`); runner.py se nemění.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time

KOREN_REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(KOREN_REPO, "tools", "evaly"))
from runner import InfraChyba, infra_chyba, tokeny_z_usage  # noqa: E402


def _prostredi():
    env = dict(os.environ)
    env.pop("UNSLOP_UDPIPE", None)
    return env


def zavolej(prompt, model, system, timeout=300, schema=None):
    """Jedno volání bez nástrojů. Vrátí dict: text, structured, cena, tokeny, model, cas_s.
    Selhání prostředí hlásí výjimkou InfraChyba."""
    cmd = ["claude", "-p", prompt, "--output-format", "json", "--no-session-persistence",
           "--strict-mcp-config", "--setting-sources", "project", "--disable-slash-commands",
           "--tools", "", "--system-prompt", system, "--model", model]
    if schema:
        cmd += ["--json-schema", json.dumps(schema)]
    cwd = tempfile.mkdtemp(prefix="unslop-bench-")
    t0 = time.time()
    try:
        p = subprocess.run(cmd, cwd=cwd, env=_prostredi(), capture_output=True, text=True,
                           encoding="utf-8", timeout=timeout)
    except subprocess.TimeoutExpired:
        raise InfraChyba(f"timeout {timeout} s")
    finally:
        shutil.rmtree(cwd, ignore_errors=True)
    try:
        d = json.loads(p.stdout)
    except ValueError:
        raise InfraChyba(infra_chyba(p.stdout + " " + p.stderr)
                         or f"nečitelná odpověď (kód {p.returncode}): {p.stderr.strip()[:200]}")
    text = d.get("result") or ""
    if d.get("is_error"):
        raise InfraChyba(infra_chyba(text) or f"chyba: {d.get('subtype')} {text[:160]}")
    inf = infra_chyba(text)
    if inf or (not text and not d.get("structured_output")):
        raise InfraChyba(inf or "prázdný výstup")
    modely = sorted((d.get("modelUsage") or {}).keys())
    return {"text": text, "structured": d.get("structured_output"), "cena": d.get("total_cost_usd") or 0.0,
            "tokeny": tokeny_z_usage(d.get("usage"), d.get("num_turns")),
            "model": ", ".join(modely) or model, "cas_s": round(time.time() - t0, 1)}


def s_opakovanim(fn, *args, pokusu=4, pauza=20, **kw):
    """Zavolá fn; při InfraChyba počká a zkusí znovu. Vrátí (výsledek | None, chyby)."""
    chyby = []
    for pokus in range(1, pokusu + 1):
        try:
            return fn(*args, **kw), chyby
        except InfraChyba as e:
            chyby.append(str(e))
            if pokus < pokusu:
                time.sleep(pauza * pokus)
    return None, chyby
