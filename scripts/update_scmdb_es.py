"""Rebuild the Spanish SCMDB language file from the latest upstream sources.

Sources:
  - SCMDB template + build script: github.com/KrovaxCode/SCMDB_LANG (newest LIVE template)
  - Spanish translation:          github.com/Thord82/Star_citizen_ES (branch propuestas_thord)

Outputs (in the repo root):
  - lang-es-latest.json              fixed name -> the URL never changes
  - lang-es-global-<version>.json    one per SCMDB version; ALL of them are
                                     rewritten with the current content so
                                     old links keep working

The translation must stay the pure Thord82 text (no Smart Citizen tags), which
is why it is downloaded straight from Thord82 and not from our other repo.

Usage: python scripts/update_scmdb_es.py
Exits 0 with nothing changed when the sources produce an identical file.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path

UPSTREAM = "https://github.com/KrovaxCode/SCMDB_LANG"
THORD_INI = "https://raw.githubusercontent.com/Thord82/Star_citizen_ES/refs/heads/propuestas_thord/global.ini"
PROFILE = "live"
MIN_TRANSLATED = 1000  # sanity floor: refuse to publish a broken build

repo = Path(__file__).resolve().parent.parent


def build_number(name: str) -> int:
    m = re.search(rf"-{PROFILE}\.(\d+)\.json$", name)
    return int(m.group(1)) if m else -1


with tempfile.TemporaryDirectory() as tmp:
    tmp = Path(tmp)
    up = tmp / "upstream"
    subprocess.run(["git", "clone", "-q", "--depth", "1", UPSTREAM, str(up)], check=True)

    templates = [p for p in up.glob(f"lang-template-*-{PROFILE}.*.json") if build_number(p.name) >= 0]
    if not templates:
        sys.exit(f"No {PROFILE} template found upstream")
    template = max(templates, key=lambda p: build_number(p.name))
    print(f"Template: {template.name}")

    # Isolated work dir with exactly one template, so the build script cannot
    # pick an older one (it sorts names as text, where 4.9 > 4.10).
    work = tmp / "work"
    work.mkdir()
    shutil.copy(up / "build_lang_template.py", work)
    shutil.copy(template, work)
    with urllib.request.urlopen(THORD_INI, timeout=120) as r:
        (work / "es-global.ini").write_bytes(r.read())

    subprocess.run(
        [sys.executable, "-I", "build_lang_template.py", "-p", PROFILE, "--translate", "es-global.ini"],
        cwd=work, check=True, stdout=subprocess.DEVNULL,
    )
    outs = list(work.glob("lang-es-global-*.json"))
    if len(outs) != 1:
        sys.exit(f"Expected one output file, got {[o.name for o in outs]}")

    data = json.loads(outs[0].read_text(encoding="utf-8"))
    data["targetLanguage"] = "es"  # the build script reports "unknown" for our file name
    translated = data.get("stats", {}).get("translated", 0)
    if translated < MIN_TRANSLATED:
        sys.exit(f"Only {translated} keys translated, refusing to publish")

    text = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    version = data.get("version", "unknown")
    print(f"Version: {version} | translated: {translated} | keys: {data.get('keyCount')}")

    # Every Spanish file ever published gets the current content, so any old
    # link someone shared keeps serving the latest translation.
    targets = {"lang-es-latest.json", f"lang-es-global-{version}.json"}
    targets |= {p.name for p in repo.glob("lang-es-global-*.json")}
    changed = []
    for name in sorted(targets):
        dest = repo / name
        if not dest.exists() or dest.read_text(encoding="utf-8") != text:
            dest.write_text(text, encoding="utf-8")
            changed.append(name)

    print("Changed: " + (", ".join(changed) if changed else "nothing"))
    gh_out = os.environ.get("GITHUB_OUTPUT")
    if gh_out:
        with open(gh_out, "a", encoding="utf-8") as f:
            f.write(f"version={version}\ntranslated={translated}\n")
