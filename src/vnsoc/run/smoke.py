"""T0.4 smoke test for the Kaggle vLLM runner (and the same check for any backend's output file).

`build` writes 20 general Vietnamese questions (NOT study items — no contamination of pilot/main data) in the runner's
request format; `summarize` reads the runner output (+ its .stats.json) and writes results/smoke/kaggle_smoke.json with
the fields the T0.4 check needs: vllm_version, requests_ok, tokens_out_per_s, think_leak, load_s.

  $PY -m vnsoc.run.smoke build --model-key qwen3_8b --out data/kaggle_requests/smoke.jsonl
  $PY -m vnsoc.run.smoke summarize --raw data/runs/kaggle/<job>/smoke_qwen.jsonl --out results/smoke/kaggle_smoke.json
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

QUESTIONS = [
    "Thủ đô của Việt Nam là thành phố nào?", "Một năm thường có bao nhiêu tháng?", "Nước sôi ở bao nhiêu độ C ở mực nước biển?",
    "Một giờ có bao nhiêu phút?", "Tam giác đều có mấy cạnh bằng nhau?", "Trái Đất quay quanh ngôi sao nào?",
    "Một kilôgam bằng bao nhiêu gam?", "Nhiệt độ cơ thể người bình thường khoảng bao nhiêu độ C?",
    "Một tuần có bao nhiêu ngày?", "Có bao nhiêu châu lục trên Trái Đất?", "Một mét bằng bao nhiêu xentimét?",
    "Nước đóng băng ở bao nhiêu độ C?", "Một ngày có bao nhiêu giờ?", "Một lít bằng bao nhiêu mililít?",
    "Tim người có bao nhiêu ngăn?", "Người trưởng thành có bao nhiêu cái răng vĩnh viễn (tính cả răng khôn)?",
    "Một thế kỷ có bao nhiêu năm?", "Một tá gồm bao nhiêu vật?", "Hình vuông có bao nhiêu góc vuông?",
    "Tháng Hai năm nhuận có bao nhiêu ngày?",
]
ANSWER_LINE = "Trả lời ngắn gọn. Dòng cuối cùng bắt buộc có dạng: ĐÁP ÁN: <giá trị> <đơn vị>"


def build(model_key: str) -> list[dict]:
    return [{"request_id": f"smoke{i:02d}|A0|{model_key}|0", "model_key": model_key,
             "messages": [{"role": "user", "content": f"{q}\n{ANSWER_LINE}"}],
             "sampling": {"temperature": 0.0, "max_tokens": 128}} for i, q in enumerate(QUESTIONS)]


def summarize(raw: str) -> dict:
    rows = [json.loads(x) for x in Path(raw).read_text(encoding="utf-8").splitlines() if x.strip()]
    texts = [(r.get("outputs") or [None])[0] or "" for r in rows]
    stats_f = Path(raw + ".stats.json")
    st = json.loads(stats_f.read_text(encoding="utf-8")) if stats_f.exists() else {}
    ok = sum(1 for t in texts if "ĐÁP ÁN" in t.upper() or "ĐÁP ÁN" in t)
    gen_s = st.get("gen_s") or st.get("seconds") or 0
    return {"requests": len(rows), "requests_ok": ok, "think_leak": any("<think>" in t for t in texts),
            "vllm_version": st.get("vllm") or (rows[0].get("vllm") if rows else None) or st.get("ollama"),
            "load_s": st.get("load_s"), "gen_s": gen_s, "tokens_out": st.get("tokens_out"),
            "tokens_out_per_s": (st.get("tokens_out") or 0) / gen_s if gen_s else 0.0, "raw": raw}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="run.smoke")
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("build"); s.add_argument("--model-key", required=True); s.add_argument("--out", required=True)
    s = sub.add_parser("summarize"); s.add_argument("--raw", required=True); s.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    if a.cmd == "build":
        out.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in build(a.model_key)), encoding="utf-8")
        print(f"{len(QUESTIONS)} yêu cầu → {out}")
    else:
        d = summarize(a.raw)
        out.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
        print(json.dumps(d, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
