"""Freeze a dataset version into data/frozen/ (never overwrites; appends SHA256SUMS).

  $PY -m vnsoc.freeze corpus      # data/interim/manifest.jsonl (+ hashes of data/raw PDFs in the corpus)
  $PY -m vnsoc.freeze atoms       # data/interim/atoms.jsonl  (schema-validated)
  $PY -m vnsoc.freeze questions   # data/interim/questions.jsonl + configs/grading.yaml + configs/conditions.yaml
"""
from __future__ import annotations

import hashlib
import json
import shutil
import sys
from pathlib import Path

from vnsoc.paths import paths

SOURCES = {
    "corpus": [("data/interim/manifest.jsonl", "manifest", "manifest")],
    "atoms": [("data/interim/atoms.jsonl", "atoms", "atom")],
    "questions": [("data/interim/questions.jsonl", "questions", "question"),
                  ("configs/grading.yaml", "grading", None), ("configs/conditions.yaml", "conditions", None)],
}


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def next_version(frozen: Path, stem: str) -> int:
    vs = [int(p.stem.split("_v")[-1]) for p in frozen.glob(f"{stem}_v*.*") if p.stem.split("_v")[-1].isdigit()]
    return max(vs, default=0) + 1


def freeze(kind: str, root=None) -> list[Path]:
    P = paths(root)
    frozen = P.root / "data" / "frozen"
    frozen.mkdir(parents=True, exist_ok=True)
    out, lines = [], []
    for src_rel, stem, schema in SOURCES[kind]:
        src = P.root / src_rel
        if not src.exists() or src.stat().st_size == 0:
            raise SystemExit(f"Thiếu {src_rel}")
        if schema:
            from vnsoc.schemas import validate_jsonl

            n, errs = validate_jsonl(schema, str(src))
            if errs:
                raise SystemExit(f"{src_rel}: {len(errs)} dòng lỗi schema — không đóng băng.\n" + "\n".join(errs[:10]))
        v = next_version(frozen, stem)
        dst = frozen / f"{stem}_v{v}{src.suffix}"
        if dst.exists():
            raise SystemExit(f"{dst} đã tồn tại")
        shutil.copy2(src, dst)
        dst.chmod(0o444)
        out.append(dst)
        lines.append(f"{sha256(dst)}  {dst.name}")
    if kind == "corpus":
        rows = [json.loads(x) for x in (P.root / "data/interim/manifest.jsonl").read_text(encoding="utf-8").splitlines()
                if x.strip()]
        missing = [r["doc_key"] for r in rows if r.get("in_corpus") and not r.get("sha256")]
        if missing:
            raise SystemExit(f"Văn bản trong kho thiếu sha256: {missing}")
        lines += [f"{r['sha256']}  raw/{r['doc_key'].replace('/', '_')}.pdf" for r in rows if r.get("in_corpus")]
    with (frozen / "SHA256SUMS").open("a", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    from vnsoc.state import append_decision, append_log

    append_log(P, f"ĐÓNG BĂNG {kind}: " + ", ".join(p.name for p in out))
    append_decision(P, f"Đóng băng {kind}: " + ", ".join(f"{p.name} ({sha256(p)[:12]})" for p in out))
    return out


def main(argv=None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    if len(argv) != 1 or argv[0] not in SOURCES:
        print(__doc__)
        return 2
    for p in freeze(argv[0]):
        print("OK", p)
    return 0


if __name__ == "__main__":
    sys.exit(main())
