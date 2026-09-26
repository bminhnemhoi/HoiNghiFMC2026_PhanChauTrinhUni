"""Number registry: every result number in the manuscript/abstract/slides comes from
results/numbers.json, written ONLY by analysis code via put(). Manuscript sources use
placeholders:  {{h1.delta_pooled}}  -> rendered value;  {{=0,10}} -> a design constant written
literally (not a result) — every number inside {{=…}} must also appear in configs/*.yaml.
Bare digits in prose are flagged by `verify`. Registry sources must live in src/vnsoc/analysis/,
analysis_R/ or scripts/analysis/. Files: manuscript/**/*.md (except manuscript/build/).

  $PY -m vnsoc.numbers verify            # placeholders resolve, sources exist, no bare numbers
  $PY -m vnsoc.numbers render            # manuscript/*.md -> manuscript/build/*.md
  $PY -m vnsoc.numbers list
"""
from __future__ import annotations

import inspect
import json
import os
import re
import sys
from pathlib import Path

from vnsoc.paths import paths

PH = re.compile(r"\{\{\s*([A-Za-z0-9_.\-=:/%,–|]+)\s*\}\}")
EN = "|en"          # {{key|en}}: the registry display in English number format (decimal point, thousands comma)


def en_format(display: str) -> str:
    """'91,5%' -> '91.5%', '15,4%–59,2%' -> '15.4%–59.2%', '1.000' -> '1,000' (Vietnamese -> English separators)."""
    return re.sub(r"(?<=\d)[.,](?=\d)", lambda m: "." if m.group(0) == "," else ",", display)
ALLOW = [
    r"\b(?:19|20)\d{2}[a-z]?\b",                   # years
    r"\b(?:H[1-5]|RQ[1-4]|A[0-6]|DR\d{1,2}|S\d{1,2}|T\d|M[1-4])\b",  # design labels
    r"\b(?:Figure|Fig\.|Table|Hình|Bảng|Supplement|Phụ lục)\s+S?\d+[a-z]?",
    r"\[\d+(?:[,–-]\s*\d+)*\]",                # numeric citations [3], [4-6]
    r"\b10\.\d{4,9}/\S+",                           # DOIs
    r"\barXiv:?\s*\d{4}\.\d{4,5}",
    r"\b(?:Qwen3|Llama-3\.1|Sailor2|Vistral|MedGemma|Gemma-3|bge-m3|GPT-\S+|Gemini\s*\S+)[\w.\-]*",
    r"\b\d+[Bb]\b",                                 # model sizes 8B
    r"\bT4\b", r"\bICD-10\b", r"\bTRIPOD-LLM\b", r"\bCRediT\b",
    r"\b\d{1,5}/(?:QĐ|TT)-BYT\b", r"\b(?:QĐ|Decision|Circular)\s+\d{1,5}/\d{4}\b", r"\b\d{1,5}/\d{4}\b",
    r"§\s*\d+(?:\.\d+)*", r"^\s*#{1,6}\s+\d+(?:\.\d+)*", r"^\s*\d+\.\s",       # headings, list markers
]


ALLOWED_SOURCES = ("src/vnsoc/analysis/", "analysis_R/", "scripts/analysis/")


def _targets(P) -> list[Path]:
    return sorted(f for f in P.manuscript.rglob("*.md") if "build" not in f.relative_to(P.manuscript).parts)


def _num(tok: str) -> float:
    return float(tok.replace(",", "."))


def config_numbers(P) -> set[float]:
    vals = set()
    for f in P.configs.glob("*.yaml"):
        vals |= {_num(x) for x in re.findall(r"(?<![\w.])\d+(?:[.,]\d+)?", f.read_text(encoding="utf-8"))}
    return vals


def _load(P) -> dict:
    return json.loads(P.numbers.read_text(encoding="utf-8")) if P.numbers.exists() else {}


def put(key: str, value, display: str, note: str = "", root=None) -> None:
    """Called from analysis scripts only. Records the calling file as the source."""
    P = paths(root)
    caller = Path(inspect.stack()[1].filename).resolve()
    try:
        src = caller.relative_to(P.root).as_posix()
    except ValueError:
        src = str(caller)
    if not src.startswith(ALLOWED_SOURCES):
        raise ValueError(f"numbers.put chỉ được gọi từ mã phân tích {ALLOWED_SOURCES}, không từ {src}")
    reg = _load(P)
    from vnsoc.state import now

    reg[key] = {"value": value, "display": display, "source": src, "note": note, "generated": now()}
    P.numbers.parent.mkdir(parents=True, exist_ok=True)
    tmp = P.numbers.with_suffix(".tmp")
    tmp.write_text(json.dumps(reg, ensure_ascii=False, indent=1, sort_keys=True), encoding="utf-8")
    for attempt in range(20):             # Windows: a reader (editor, another process) can lock the target briefly
        try:
            os.replace(tmp, P.numbers)
            break
        except PermissionError:
            if attempt == 19:
                raise
            import time

            time.sleep(0.25)


def _prose_lines(text: str):
    fence = False
    for i, line in enumerate(text.splitlines(), 1):
        if line.strip().startswith(("```", "~~~")):
            fence = not fence
            continue
        if fence or line.strip().startswith(("<!--", "|---", "| ---")):
            continue
        yield i, line


def bare_numbers(line: str) -> list[str]:
    s = PH.sub(" ", line)
    s = re.sub(r"\]\([^)]*\)", "]", s)             # link targets
    s = re.sub(r"https?://\S+", " ", s)
    for pat in ALLOW:
        s = re.sub(pat, " ", s, flags=re.M)
    return re.findall(r"(?<![\w.])\d+(?:[.,]\d+)?%?", s)


def verify(root=None, files: list[str] | None = None) -> int:
    P = paths(root)
    reg = _load(P)
    problems = []
    for k, v in reg.items():
        if not (P.root / v.get("source", "")).exists():
            problems.append(f"registry '{k}': source không tồn tại {v.get('source')}")
    targets = [Path(f) for f in files] if files else _targets(P)
    cfg_nums = config_numbers(P)
    for f in targets:
        text = f.read_text(encoding="utf-8")
        for key in PH.findall(text):
            if key.startswith("="):
                bad = [x for x in re.findall(r"\d+(?:[.,]\d+)?", key) if _num(x) not in cfg_nums]
                if bad:
                    problems.append(f"{f.name}: hằng số {{{{{key}}}}} có số {bad} không có trong configs/*.yaml")
            elif key.removesuffix(EN) not in reg:
                problems.append(f"{f.name}: placeholder chưa có số: {{{{{key}}}}}")
        for i, line in _prose_lines(text):
            nums = bare_numbers(line)
            if nums:
                problems.append(f"{f.name}:{i}: số viết tay {nums[:5]} — dùng {{{{key}}}} hoặc {{{{=hằng}}}}")
    for p in problems:
        print(p)
    print(f"{'OK' if not problems else 'LỖI'}: {len(problems)} vấn đề; {len(reg)} số trong registry")
    return 0 if not problems else 1


def render(root=None) -> int:
    P = paths(root)
    reg = _load(P)
    out = P.manuscript / "build"
    out.mkdir(parents=True, exist_ok=True)
    missing = set()

    def sub(m):
        k = m.group(1)
        if k.startswith("="):
            return k[1:]
        base = k.removesuffix(EN)
        if base not in reg:
            missing.add(k)
            return m.group(0)
        d = str(reg[base]["display"])
        return en_format(d) if k.endswith(EN) else d

    for f in _targets(P):
        dst = out / f.relative_to(P.manuscript)
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(PH.sub(sub, f.read_text(encoding="utf-8")), encoding="utf-8")
    if missing:
        print("THIẾU:", sorted(missing))
        return 1
    print(f"OK: render {out}")
    return 0


def main(argv=None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    cmd = argv[0] if argv else "verify"
    if cmd == "verify":
        return verify(files=argv[1:] or None)
    if cmd == "render":
        return render()
    if cmd == "list":
        for k, v in sorted(_load(paths()).items()):
            print(f"{k:40s} {v['display']:>14s}  ← {v['source']}")
        return 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main())
