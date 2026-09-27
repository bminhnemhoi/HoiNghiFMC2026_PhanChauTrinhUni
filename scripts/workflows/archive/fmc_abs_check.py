"""Render an FMC abstract draft (same markdown format as manuscript/fmc/abstract_fmc.md, with {{key}} / {{key|en}}
placeholders) from results/numbers.json and report: missing keys, hand-written digits, per-section word counts,
body totals (5 sections, title and keywords excluded), box/title characters, fmc.checks problems, rendered text.

  cd "D:/phan chau trinh _ y khoa" && PYTHONUTF8=1 .venv/Scripts/python.exe <this file> <draft.md>
"""
import re, sys, unicodedata
from pathlib import Path
sys.path.insert(0, "src")
from vnsoc import fmc
from vnsoc.numbers import PH, EN, en_format, bare_numbers, _load
from vnsoc.paths import paths

src = Path(sys.argv[1]).read_text(encoding="utf-8")
reg = _load(paths())
missing = []
def sub(m):
    k = m.group(1)
    if k.startswith("="):
        return k[1:]
    b = k.removesuffix(EN)
    if b not in reg:
        missing.append(k); return m.group(0)
    d = str(reg[b]["display"])
    return en_format(d) if k.endswith(EN) else d
body_lines = [l for l in src.splitlines() if not l.startswith("#")]
hand = sorted({n for l in body_lines for n in bare_numbers(l)})
rendered = PH.sub(sub, src)
doc = fmc.parse(rendered)
print("MISSING KEYS:", missing or "none")
print("HAND-WRITTEN DIGITS (must be none; use {{key}} or {{=const}}):", hand or "none")
for lang in ("vi", "en"):
    secs = list(doc[lang].items())
    print(f"--- {lang.upper()}: title {len(secs[0][1]) if secs else 0} chars")
    tot = 0
    for name, t in secs[1:-1]:
        n = fmc.words(t); tot += n
        print(f"   {name}: {n} words (+{fmc.words(name + ':')} heading words)")
    head = sum(fmc.words(n + ":") for n, _ in secs[1:-1])
    print(f"   BODY TOTAL {tot} words (with headings {tot + head}); keywords: {secs[-1][1] if secs else ''}")
print("BOX VI chars:", len(unicodedata.normalize("NFC", doc["box"])), "| BOX EN chars:", len(unicodedata.normalize("NFC", doc.get("box_en") or "")))
print("fmc.checks:", fmc.checks(doc) or "OK")
print("=========== RENDERED ===========")
print(rendered)
