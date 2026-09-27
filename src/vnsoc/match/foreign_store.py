"""Versioned foreign reference store (T2.6): merge data/interim/foreign_parts/*.jsonl into
data/interim/foreign_values.jsonl and check every record by code.

A record is kept only when it is schema-valid (schemas.ForeignRecord), its page_sha256 names a cached source that is
not an anti-bot/interstitial page (vnsoc.match.sources.block_hashes) and every recorded number / key drug name is
found in that cached text (the same evidence check as the pilot, vnsoc.extract.pilot_merge.source_warnings). No
passage text is stored: every string field is at most 200 characters (legal rule: values + citation + locator only).

  $PY -m vnsoc.match.foreign_store            # merge + check -> foreign_values.jsonl, foreign_rejects.jsonl
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from vnsoc.paths import paths
from vnsoc.schemas import ForeignRecord

MAX_TEXT = 200


def long_text_fields(rec: dict) -> list[str]:
    """Names of string fields (incl. value 'text') longer than MAX_TEXT characters."""
    out = [k for k, v in rec.items() if isinstance(v, str) and len(v) > MAX_TEXT and k not in ("url",)]
    out += [f"values[{i}].text" for i, it in enumerate(rec.get("values") or [])
            if isinstance(it.get("text"), str) and len(it["text"]) > MAX_TEXT]
    return out


def check_record(rec: dict, blocks: set[str], root=None) -> list[str]:
    from vnsoc.extract.pilot_merge import source_warnings

    probs = []
    try:
        ForeignRecord.model_validate(rec)
    except Exception as e:  # noqa: BLE001
        probs.append(f"schema: {str(e)[:200]}")
        return probs
    long = long_text_fields(rec)
    if long:
        probs.append(f"trường chữ > {MAX_TEXT} ký tự (có thể là đoạn văn nguồn): {long}")
    atom_like = {"foreign": [{"source": rec["source"], "page_sha256": rec["page_sha256"], "values": rec["values"]}]}
    probs += source_warnings(atom_like, blocks, root)
    return probs


def load_parts(d: Path) -> list[dict]:
    rows = []
    for f in sorted(d.glob("*.jsonl")):
        rows += [json.loads(x) for x in f.read_text(encoding="utf-8").splitlines() if x.strip()]
    return rows


def main(argv=None) -> int:
    from vnsoc.match.sources import block_hashes

    P = paths()
    parts = P.root / "data" / "interim" / "foreign_parts"
    rows = load_parts(parts)
    blocks = block_hashes()
    keep, bad, seen = [], [], set()
    for r in rows:
        probs = check_record(r, blocks)
        if r.get("record_id") in seen:
            probs.append("record_id trùng")
        seen.add(r.get("record_id"))
        (bad if probs else keep).append((r, probs))
    out = P.root / "data" / "interim" / "foreign_values.jsonl"
    out.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r, _ in keep), encoding="utf-8")
    rej = P.root / "data" / "interim" / "foreign_rejects.jsonl"
    rej.write_text("".join(json.dumps({"record_id": r.get("record_id"), "problems": p}, ensure_ascii=False) + "\n"
                           for r, p in bad), encoding="utf-8")
    by = {}
    for r, _ in keep:
        by[r["system"]] = by.get(r["system"], 0) + 1
    print(f"giữ {len(keep)} bản ghi {by}; loại {len(bad)} (xem {rej.name})")
    for r, p in bad[:30]:
        print(f"  LOẠI {r.get('record_id')}: {'; '.join(p)[:300]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
