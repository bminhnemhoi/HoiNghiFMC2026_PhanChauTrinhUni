"""Paid-API batch runs (OpenAI Batch, Gemini Batch) with a HARD budget gate.

Every submission: build JSONL -> estimate upper-bound cost -> budget.reserve() (raises if the cap
would be broken) -> submit -> poll -> fetch -> parse to RunRecord JSONL -> budget.settle(actual).

The request-building and parsing functions are pure and unit-tested. The submit/poll/fetch functions
call the vendor SDKs; T0.5 (API smoke test) must confirm the exact model IDs and parameter names
(reasoning/thinking controls change between model generations) and record them in configs/models.yaml.

Build request lines with openai_line()/gemini_line() from the frozen questions and the prompt
templates in configs/prompts.yaml (task T5.5 writes that small builder), then:
  $PY -m vnsoc.run.api_batch submit --model-key cheap_1 --batch runs/x.jsonl --task T5.5
  $PY -m vnsoc.run.api_batch poll   --job <id>
  $PY -m vnsoc.run.api_batch fetch  --job <id> --out data/runs/api/<id>.jsonl
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

from vnsoc import budget
from vnsoc.paths import paths


def _cfg(model_key: str) -> dict:
    import yaml

    models = yaml.safe_load((paths().configs / "models.yaml").read_text(encoding="utf-8"))
    for group in ("api_cheap", "api_frontier"):
        for m in models.get(group, []):
            if m["key"] == model_key:
                if not m.get("model") or "FILL" in str(m.get("model")):
                    raise SystemExit(f"{model_key}: chưa điền model id (làm T0.5 trước)")
                return m
    raise SystemExit(f"không có model key {model_key} trong configs/models.yaml")


def prompt_hash(messages: list[dict]) -> str:
    return hashlib.sha256(json.dumps(messages, ensure_ascii=False, sort_keys=True).encode()).hexdigest()[:16]


def openai_line(custom_id: str, model: str, messages: list[dict], max_tokens: int, extra: dict | None = None,
                endpoint: str = "/v1/chat/completions") -> dict:
    body = {"model": model, "messages": messages, "max_completion_tokens": max_tokens}
    body.update(extra or {})
    return {"custom_id": custom_id, "method": "POST", "url": endpoint, "body": body}


def gemini_line(key: str, messages: list[dict], max_tokens: int, extra_generation: dict | None = None) -> dict:
    sys_txt = "\n".join(m["content"] for m in messages if m["role"] == "system")
    contents = [{"role": "user" if m["role"] == "user" else "model", "parts": [{"text": m["content"]}]}
                for m in messages if m["role"] != "system"]
    gen = {"max_output_tokens": max_tokens}
    gen.update(extra_generation or {})
    req = {"contents": contents, "generation_config": gen}
    if sys_txt:
        req["system_instruction"] = {"parts": [{"text": sys_txt}]}
    return {"key": key, "request": req}


def estimate_batch_cost(lines: list[dict], price_in: float, price_out: float, max_out: int,
                        reasoning_allowance: int = 0, chars_per_token: float = 2.5) -> float:
    """Conservative: Vietnamese ~2.5 chars/token; output = max tokens + reasoning allowance."""
    chars = sum(len(json.dumps(ln, ensure_ascii=False)) for ln in lines)
    tin = chars / chars_per_token / max(len(lines), 1)
    return budget.estimate(len(lines), tin, max_out + reasoning_allowance, price_in, price_out, 0.5)


def parse_openai_output(line: dict) -> tuple[str, str | None, int | None, int | None, str | None]:
    cid = line.get("custom_id")
    if line.get("error"):
        return cid, None, None, None, json.dumps(line["error"])[:500]
    body = (line.get("response") or {}).get("body") or {}
    try:
        text = body["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError):
        return cid, None, None, None, "no content"
    u = body.get("usage") or {}
    return cid, text, u.get("prompt_tokens"), u.get("completion_tokens"), None


def parse_gemini_output(line: dict) -> tuple[str, str | None, int | None, int | None, str | None]:
    key = line.get("key")
    resp = line.get("response") or {}
    if line.get("error") or not resp:
        return key, None, None, None, json.dumps(line.get("error"))[:500]
    try:
        parts = resp["candidates"][0]["content"]["parts"]
        text = "".join(p.get("text", "") for p in parts if not p.get("thought"))
    except (KeyError, IndexError, TypeError):
        return key, None, None, None, "no content"
    u = resp.get("usageMetadata") or resp.get("usage_metadata") or {}

    def g(camel, snake):
        return u.get(camel, u.get(snake)) or 0

    out = g("candidatesTokenCount", "candidates_token_count") + g("thoughtsTokenCount", "thoughts_token_count")
    return key, text, g("promptTokenCount", "prompt_token_count"), out, None


def actual_cost(tokens_in: int, tokens_out: int, price_in: float, price_out: float) -> float:
    return round((tokens_in * price_in + tokens_out * price_out) / 1e6 * 0.5, 4)


# ------------------------------------------------------------------------------ vendor calls
def submit(model_key: str, batch_path: str, task: str) -> str:
    cfg = _cfg(model_key)
    lines = [json.loads(x) for x in Path(batch_path).read_text(encoding="utf-8").splitlines() if x.strip()]
    est = estimate_batch_cost(lines, cfg["price_in"], cfg["price_out"], cfg.get("max_tokens", 128),
                              cfg.get("reasoning_allowance", 0))
    job_tmp = f"{model_key}-{hashlib.sha1(batch_path.encode()).hexdigest()[:8]}"
    budget.reserve(cfg["provider"], cfg["model"], job_tmp, task, est, note=batch_path)  # raises if over cap
    if cfg["provider"] == "openai":
        from openai import OpenAI

        client = OpenAI()
        f = client.files.create(file=open(batch_path, "rb"), purpose="batch")
        job = client.batches.create(input_file_id=f.id, endpoint=cfg.get("endpoint", "/v1/chat/completions"),
                                    completion_window="24h", metadata={"task": task, "ledger": job_tmp})
        job_id = job.id
    elif cfg["provider"] == "google":
        from google import genai
        from google.genai import types

        client = genai.Client()
        up = client.files.upload(file=batch_path, config=types.UploadFileConfig(display_name=job_tmp,
                                                                                mime_type="jsonl"))
        job = client.batches.create(model=cfg["model"], src=up.name, config={"display_name": job_tmp})
        job_id = job.name
    else:
        raise SystemExit(f"provider lạ {cfg['provider']}")
    reg = paths().state / "api_jobs.jsonl"
    with reg.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps({"job_id": job_id, "ledger_id": job_tmp, "model_key": model_key, "task": task,
                             "batch": batch_path, "est_usd": est}) + "\n")
    print(f"ĐÃ GỬI {job_id} (ước tính trần {est:.2f} USD)")
    return job_id


def _job(job_id: str) -> dict:
    reg = paths().state / "api_jobs.jsonl"
    for ln in reg.read_text(encoding="utf-8").splitlines():
        d = json.loads(ln)
        if d["job_id"] == job_id:
            return d
    raise SystemExit(f"không thấy job {job_id} trong state/api_jobs.jsonl")


def poll(job_id: str) -> str:
    cfg = _cfg(_job(job_id)["model_key"])
    if cfg["provider"] == "openai":
        from openai import OpenAI

        st = OpenAI().batches.retrieve(job_id).status
    else:
        from google import genai

        st = genai.Client().batches.get(name=job_id).state.name
    print(st)
    return st


def fetch(job_id: str, out: str) -> None:
    meta = _job(job_id)
    cfg = _cfg(meta["model_key"])
    rows = []
    if cfg["provider"] == "openai":
        from openai import OpenAI

        client = OpenAI()
        job = client.batches.retrieve(job_id)
        if job.status not in ("completed", "expired", "cancelled"):
            raise SystemExit(f"batch {job_id} chưa xong: {job.status}")
        raw = client.files.content(job.output_file_id).text if job.output_file_id else ""
        if job.error_file_id:  # failed requests are reported separately
            raw += "\n" + client.files.content(job.error_file_id).text
        rows = [parse_openai_output(json.loads(x)) for x in raw.splitlines() if x.strip()]
    else:
        from google import genai

        client = genai.Client()
        job = client.batches.get(name=job_id)
        if job.state.name != "JOB_STATE_SUCCEEDED":
            raise SystemExit(f"batch {job_id}: {job.state.name}")
        raw = client.files.download(file=job.dest.file_name).decode("utf-8")
        rows = [parse_gemini_output(json.loads(x)) for x in raw.splitlines() if x.strip()]
    tin = sum(r[2] or 0 for r in rows)
    tout = sum(r[3] or 0 for r in rows)
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        for cid, text, a, b, err in rows:
            f.write(json.dumps({"request_id": cid, "raw_output": text, "tokens_in": a, "tokens_out": b,
                                "error": err, "job_id": job_id}, ensure_ascii=False) + "\n")
    cost = actual_cost(tin, tout, cfg["price_in"], cfg["price_out"])
    budget.settle(meta["ledger_id"], cost, note=f"{job_id} in={tin} out={tout}")
    print(f"OK {len(rows)} dòng → {out}; chi phí thực {cost:.4f} USD. {budget.status_line()}")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="api_batch")
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("submit"); s.add_argument("--model-key", required=True)
    s.add_argument("--batch", required=True); s.add_argument("--task", required=True)
    s = sub.add_parser("poll"); s.add_argument("--job", required=True)
    s = sub.add_parser("fetch"); s.add_argument("--job", required=True); s.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    if a.cmd == "submit":
        try:
            submit(a.model_key, a.batch, a.task)
        except budget.BudgetExceeded as e:
            print(e, file=sys.stderr)
            return 1
    elif a.cmd == "poll":
        poll(a.job)
    elif a.cmd == "fetch":
        fetch(a.job, a.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
