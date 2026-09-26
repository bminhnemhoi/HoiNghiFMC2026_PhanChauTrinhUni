"""Local pilot backend (DECISIONS 2026-09-26, user-approved deviation): the same request file as the Kaggle
runner, served by a local Ollama model (llama.cpp GGUF) on the laptop GPU. Greedy decoding exactly as
configs/conditions.yaml (temperature 0, max_tokens 128, seed 0), thinking disabled ("think": false for Qwen3).
Output lines match the Kaggle runner ({"request_id", "outputs", "tokens_in", "tokens_out", "cum_logprob",
"model_key", "engine"}) so vnsoc.run.collect works unchanged; appends and resumes by request_id.

  $PY -m vnsoc.run.ollama_local --requests data/runs/pilot/requests/requests.jsonl --model-key qwen3_8b_local \
      --tag qwen3:8b --out data/runs/pilot/raw/qwen3_8b_local.jsonl
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

URL = "http://localhost:11434"


def _post(path: str, body: dict, timeout: int = 600) -> dict:
    import requests

    r = requests.post(URL + path, json=body, timeout=timeout)
    r.raise_for_status()
    return r.json()


def model_info(tag: str) -> dict:
    import requests

    tags = requests.get(URL + "/api/tags", timeout=30).json().get("models", [])
    m = next((x for x in tags if x.get("name") == tag or x.get("model") == tag), None)
    ver = requests.get(URL + "/api/version", timeout=30).json().get("version")
    if m is None:
        raise SystemExit(f"Ollama chưa có mô hình {tag} (ollama pull {tag})")
    d = m.get("details") or {}
    return {"tag": tag, "digest": m.get("digest"), "quantization": d.get("quantization_level"),
            "parameter_size": d.get("parameter_size"), "format": d.get("format"), "ollama": ver}


def run(requests_path: str, model_key: str, tag: str, out: str, num_ctx: int = 8192, limit: int | None = None) -> dict:
    info = model_info(tag)
    reqs = [json.loads(x) for x in Path(requests_path).read_text(encoding="utf-8").splitlines() if x.strip()]
    reqs = [r for r in reqs if r["model_key"] == model_key]
    outp = Path(out)
    outp.parent.mkdir(parents=True, exist_ok=True)
    done = set()
    if outp.exists():
        done = {json.loads(x)["request_id"] for x in outp.read_text(encoding="utf-8").splitlines() if x.strip()}
    todo = [r for r in reqs if r["request_id"] not in done][:limit]
    t0, n_out = time.time(), 0
    with outp.open("a", encoding="utf-8") as f:
        for i, r in enumerate(todo, 1):
            s = r.get("sampling") or {}
            body = {"model": tag, "messages": r["messages"], "stream": False, "think": False,
                    "options": {"temperature": s.get("temperature", 0.0), "num_predict": s.get("max_tokens", 128),
                                "seed": 0, "num_ctx": num_ctx, "top_p": s.get("top_p", 1.0)}}
            try:
                res = _post("/api/chat", body)
                text, err = (res.get("message") or {}).get("content", ""), None
                tin, tout = res.get("prompt_eval_count"), res.get("eval_count")
            except Exception as e:  # noqa: BLE001
                text, err, tin, tout = None, f"{type(e).__name__}: {str(e)[:300]}", None, None
            n_out += tout or 0
            f.write(json.dumps({"request_id": r["request_id"], "outputs": [text], "tokens_in": tin, "tokens_out": [tout],
                                "cum_logprob": [None], "model_key": model_key, "error": err,
                                "engine": f"ollama {info['ollama']} {tag} {info['quantization']} {info['digest'][:12]}"},
                               ensure_ascii=False) + "\n")
            f.flush()
            if i % 25 == 0:
                print(f"[{model_key}] {i}/{len(todo)} · {n_out / max(time.time() - t0, 1e-9):.1f} tok/s ra", flush=True)
    stats = {"model_key": model_key, **info, "requests": len(todo), "tokens_out": n_out, "seconds": round(time.time() - t0, 1)}
    Path(str(outp) + ".stats.json").write_text(json.dumps(stats, ensure_ascii=False, indent=1), encoding="utf-8")
    return stats


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="run.ollama_local")
    ap.add_argument("--requests", required=True)
    ap.add_argument("--model-key", required=True)
    ap.add_argument("--tag", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--num-ctx", type=int, default=8192)
    ap.add_argument("--limit", type=int)
    a = ap.parse_args(argv)
    print(json.dumps(run(a.requests, a.model_key, a.tag, a.out, a.num_ctx, a.limit), ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
