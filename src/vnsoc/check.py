"""Small acceptance checks used by the `check:` commands in the plan (exit 0 = pass).

  $PY -m vnsoc.check jsonl atom data/interim/pilot_atoms.jsonl --min 20 --require span_verified=true
  $PY -m vnsoc.check numbers pilot. --min 5          # registry has >= 5 keys starting with 'pilot.'
  $PY -m vnsoc.check nofill manuscript/fmc/abstract_fmc.md configs/models.yaml
  $PY -m vnsoc.check maxsize manuscript/fmc/abstract_fmc.docx 1000000
  $PY -m vnsoc.check review M2      # PASS at round 1 or round 2 (review/M2_r2), or user decision gate HGM2 done
  $PY -m vnsoc.check count data/interim/atoms.jsonl --min 400 --where conflict_status=conflict
  $PY -m vnsoc.check families data/frozen/atoms_v1.jsonl --min 25
  $PY -m vnsoc.check value qc.extraction_cp_lower --ge 0.90
  $PY -m vnsoc.check runs data/runs/open --plan results/run_plan.json --conditions A0 A1 --models-from open
      run_plan.json = {"<model>|<condition>|<language>|<format>": expected_count, ...} written from the
      frozen question set BEFORE the run; the check compares valid, error-free RunRecords against it.
"""
from __future__ import annotations

import argparse
import gzip
import json
import re
import sys
from pathlib import Path

from vnsoc.paths import paths

FILL = re.compile(r"FILL_AT_|\[\s\]|\[n\]|\[k\]|\[a\]|\[b\]|\[c\]|\[d\]|\[e\]|\[f\]|TODO|TBD|XXX")


def _rows(path: str):
    op = gzip.open if path.endswith(".gz") else open
    with op(path, "rt", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                yield json.loads(line)


def _match(row: dict, conds: list[str]) -> bool:
    for c in conds:
        k, v = c.split("=", 1)
        val = row.get(k)
        want = {"true": True, "false": False, "null": None}.get(v, v)
        if isinstance(val, (int, float)) and not isinstance(val, bool) and not isinstance(want, bool):
            try:
                want = type(val)(want)
            except (TypeError, ValueError):
                pass
        if val != want:
            return False
    return True


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="check")
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("jsonl"); s.add_argument("kind"); s.add_argument("path")
    s.add_argument("--min", type=int, default=1); s.add_argument("--require", nargs="*", default=[])
    s = sub.add_parser("count"); s.add_argument("path"); s.add_argument("--min", type=int, default=1)
    s.add_argument("--where", nargs="*", default=[])
    s = sub.add_parser("families"); s.add_argument("path"); s.add_argument("--min", type=int, default=25)
    s = sub.add_parser("numbers"); s.add_argument("prefix"); s.add_argument("--min", type=int, default=1)
    s = sub.add_parser("nofill"); s.add_argument("files", nargs="+")
    s = sub.add_parser("maxsize"); s.add_argument("path"); s.add_argument("bytes", type=int)
    s = sub.add_parser("review"); s.add_argument("milestone")
    s = sub.add_parser("value"); s.add_argument("key"); s.add_argument("--ge", type=float); s.add_argument("--le", type=float)
    s = sub.add_parser("runs"); s.add_argument("dir"); s.add_argument("--plan", required=True)
    s.add_argument("--conditions", nargs="*", default=None); s.add_argument("--models", nargs="*", default=None)
    s.add_argument("--models-from", default=None, help="nhóm trong configs/models.yaml: open | api_cheap | api_frontier")
    s.add_argument("--min-frac", type=float, default=0.98); s.add_argument("--max-error", type=float, default=0.02)
    a = ap.parse_args(argv)

    if a.cmd == "jsonl":
        from vnsoc.schemas import validate_jsonl

        n, errs = validate_jsonl(a.kind, a.path)
        if errs:
            print(f"LỖI schema {len(errs)}/{n}: {errs[:5]}")
            return 1
        bad = [i for i, r in enumerate(_rows(a.path), 1) if not _match(r, a.require)]
        if bad:
            print(f"{len(bad)} dòng không thỏa {a.require} (ví dụ dòng {bad[:5]})")
            return 1
        if n < a.min:
            print(f"chỉ có {n} dòng (< {a.min})")
            return 1
        print(f"OK {n} dòng {a.kind}")
    elif a.cmd == "count":
        n = sum(1 for r in _rows(a.path) if _match(r, a.where))
        print(f"{n} dòng thỏa {a.where}")
        return 0 if n >= a.min else 1
    elif a.cmd == "families":
        fam = {r.get("conflict_family") for r in _rows(a.path) if r.get("conflict_status") == "conflict"}
        fam.discard(None)
        print(f"{len(fam)} nhóm xung đột")
        return 0 if len(fam) >= a.min else 1
    elif a.cmd == "numbers":
        P = paths()
        reg = json.loads(P.numbers.read_text(encoding="utf-8")) if P.numbers.exists() else {}
        keys = [k for k in reg if k.startswith(a.prefix)]
        missing_src = [k for k in keys if not (P.root / reg[k].get("source", "")).exists()]
        print(f"{len(keys)} khóa '{a.prefix}*'; thiếu nguồn: {missing_src}")
        return 0 if len(keys) >= a.min and not missing_src else 1
    elif a.cmd == "nofill":
        bad = []
        for f in a.files:
            for i, line in enumerate(Path(f).read_text(encoding="utf-8").splitlines(), 1):
                if FILL.search(line):
                    bad.append(f"{f}:{i}: {line.strip()[:100]}")
        print("\n".join(bad) or "OK không còn ô trống")
        return 1 if bad else 0
    elif a.cmd == "maxsize":
        size = Path(a.path).stat().st_size
        print(f"{a.path}: {size} bytes")
        return 0 if 0 < size <= a.bytes else 1
    elif a.cmd == "value":
        P = paths()
        reg = json.loads(P.numbers.read_text(encoding="utf-8")) if P.numbers.exists() else {}
        if a.key not in reg:
            print(f"thiếu khóa {a.key}")
            return 1
        v = float(reg[a.key]["value"])
        ok = (a.ge is None or v >= a.ge) and (a.le is None or v <= a.le)
        print(f"{a.key} = {v} ({'đạt' if ok else 'KHÔNG đạt'})")
        return 0 if ok else 1
    elif a.cmd == "runs":
        from pydantic import ValidationError

        from vnsoc.schemas import RunRecord

        plan = json.loads(Path(a.plan).read_text(encoding="utf-8"))
        if a.models_from:
            import yaml

            cfg = yaml.safe_load((paths().configs / "models.yaml").read_text(encoding="utf-8"))
            a.models = (a.models or []) + [m["key"] for m in cfg.get(a.models_from) or []]
        got: dict[str, int] = {}
        n = errors = invalid = 0
        for f in sorted(Path(a.dir).rglob("*.jsonl*")):
            for r in _rows(str(f)):
                n += 1
                try:
                    RunRecord.model_validate(r)
                except ValidationError:
                    invalid += 1
                    continue
                if r.get("error"):
                    errors += 1
                    continue
                k = f"{r['model']}|{r['condition']}|{r['language']}|{r['format']}"
                got[k] = got.get(k, 0) + 1
        short, selected = [], 0
        for k, exp in plan.items():
            model, cond = k.split("|")[0], k.split("|")[1]
            if (a.conditions and cond not in a.conditions) or (a.models and model not in a.models):
                continue
            selected += 1
            if got.get(k, 0) < a.min_frac * exp:
                short.append(f"{k}: {got.get(k, 0)}/{exp}")
        err_rate = errors / n if n else 1.0
        print(f"{n} bản ghi; không hợp lệ {invalid}; lỗi {errors} ({err_rate:.1%}); thiếu: {short[:10]}")
        if not selected:
            print("run_plan không có khóa nào khớp bộ lọc --models/--conditions")
            return 1
        return 0 if n and not invalid and not short and err_rate <= a.max_error else 1
    elif a.cmd == "review":
        from vnsoc.review import aggregate

        rdir = paths().root / "review"
        ok, msg = aggregate(a.milestone)
        print(msg)
        if not ok and (rdir / f"{a.milestone}_r2").exists():
            ok, msg = aggregate(f"{a.milestone}_r2")
            print("vòng 2:", msg)
        gate = "HG" + a.milestone.upper()                # HGM2, HGM3, HGM4: added dynamically, user-confirmed
        P = paths()
        if not ok and (P.human_ack / gate).exists() and P.progress.exists():
            st = json.loads(P.progress.read_text(encoding="utf-8"))
            if st["tasks"].get(gate, {}).get("status") == "done":
                print(f"không đạt sau 2 vòng; người dùng đã quyết định qua {gate}")
                ok = True
        return 0 if ok else 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
