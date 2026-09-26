"""Turn raw outputs (Kaggle vLLM runner or api_batch fetch) into schema-valid RunRecord JSONL.

Kaggle output line: {"request_id", "outputs": [...], "tokens_in", "tokens_out": [...], "cum_logprob": [...],
"model_key", "vllm"}; api_batch fetch line: {"request_id", "raw_output", "tokens_in", "tokens_out", "error"}.
Metadata (question, condition, prompt hash, decoding) comes from the index written by vnsoc.run.plan, so a record
can only exist for a request that was planned.

  $PY -m vnsoc.run.collect --index data/runs/pilot/requests/index.jsonl --raw <file.jsonl> ... \
      --model-version "<hf commit | api model id>" --backend vllm --date 2026-09-28 --out data/runs/pilot/qwen3_8b.jsonl
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from vnsoc.schemas import RunRecord


def records(index: dict[str, dict], raw_rows: list[dict], model_version: str, backend: str, date: str) -> list[dict]:
    out = []
    for r in raw_rows:
        meta = index.get(r["request_id"])
        if meta is None:
            raise ValueError(f"request_id không có trong index: {r['request_id']}")
        texts = r.get("outputs") if "outputs" in r else [r.get("raw_output")]
        touts = r.get("tokens_out")
        touts = touts if isinstance(touts, list) else [touts] * len(texts)
        lps = r.get("cum_logprob") or [None] * len(texts)
        for k, text in enumerate(texts):
            rec = {"run_id": f"{r['request_id']}#{k}", "model": meta["model_key"], "model_version": model_version,
                   "date": date, "atom_id": meta["atom_id"], "question_id": meta["question_id"],
                   "format": meta["format"], "language": meta["language"], "condition": meta["condition"],
                   "sample_idx": meta["sample_idx"] + k, "temperature": meta["temperature"],
                   "max_tokens": meta["max_tokens"], "prompt_hash": meta["prompt_hash"],
                   "retrieved_ids": meta.get("retrieved_ids") or [], "raw_output": text or "",
                   "tokens_in": r.get("tokens_in"), "tokens_out": touts[k] if k < len(touts) else None,
                   "logprob_answer": lps[k] if k < len(lps) else None, "backend": backend,
                   "error": r.get("error") or (None if text is not None else "no output")}
            out.append(RunRecord.model_validate(rec).model_dump())
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="run.collect")
    ap.add_argument("--index", required=True)
    ap.add_argument("--raw", nargs="+", required=True)
    ap.add_argument("--model-version", required=True)
    ap.add_argument("--backend", required=True, choices=["vllm", "hf", "openai_batch", "gemini_batch", "api_sync", "ollama"])
    ap.add_argument("--date", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    index = {}
    for line in Path(a.index).read_text(encoding="utf-8").splitlines():
        if line.strip():
            d = json.loads(line)
            index[d["request_id"]] = d
    raw = [json.loads(x) for f in a.raw for x in Path(f).read_text(encoding="utf-8").splitlines() if x.strip()]
    recs = records(index, raw, a.model_version, a.backend, a.date)
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in recs), encoding="utf-8")
    errs = sum(1 for r in recs if r["error"])
    print(f"{len(recs)} RunRecord → {a.out} ({errs} lỗi)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
