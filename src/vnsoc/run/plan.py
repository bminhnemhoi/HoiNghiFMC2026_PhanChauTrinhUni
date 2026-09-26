"""Build the request set and the expected-count run plan for a run matrix (T1.4 pilot; T4.3/T5.x reuse it).

Pilot matrix (proposal §5.7): short answers at A0, A1, A3 x VI/EN for every atom; MCQs (both orders) at A1 for
conflict / superseded atoms; greedy decoding, 128 tokens (configs/conditions.yaml decoding).
Writes: <out>/requests.jsonl (Kaggle runner format), <out>/index.jsonl (request metadata for collect), and the plan
{"<model_key>|<condition>|<language>|<format>": n} used by `vnsoc.check runs`.

  $PY -m vnsoc.run.plan --questions data/interim/pilot_questions.jsonl --atoms data/interim/pilot_atoms.jsonl \
      --passages data/interim/pilot_passages.jsonl --models qwen3_8b cheap_1 --out data/runs/pilot/requests \
      --plan results/run_plan_pilot.json
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from vnsoc.run.api_batch import prompt_hash
from vnsoc.run.prompts import conditions, messages, request_id

PILOT_SHORT = ("A0", "A1", "A3")
PILOT_MCQ = ("A1",)


def _jsonl(p) -> list[dict]:
    return [json.loads(x) for x in Path(p).read_text(encoding="utf-8").splitlines() if x.strip()]


def build(questions: list[dict], atoms: dict[str, dict], passages: dict[str, str], model_keys: list[str],
          short_conds=PILOT_SHORT, mcq_conds=PILOT_MCQ, root=None) -> tuple[list[dict], list[dict], dict]:
    dec = conditions(root)["decoding"]
    reqs, index, plan = [], [], {}
    for q in questions:
        conds = short_conds if q["format"] == "short" else mcq_conds if q["format"] == "mcq" else ()
        for c in conds:
            a = atoms[q["atom_id"]]
            passage = passages.get(q.get("oracle_passage_id") or "") if c == "A3" else None
            if c == "A3" and not passage:
                continue
            msgs = messages(q, c, a, passage, root)
            for mk in model_keys:
                rid = request_id(q["question_id"], c, mk, 0)
                reqs.append({"request_id": rid, "model_key": mk, "messages": msgs,
                             "sampling": {"temperature": dec["temperature"], "max_tokens": dec["max_tokens"]}})
                index.append({"request_id": rid, "question_id": q["question_id"], "atom_id": q["atom_id"],
                              "format": q["format"], "language": q["language"], "condition": c, "model_key": mk,
                              "sample_idx": 0, "temperature": dec["temperature"], "max_tokens": dec["max_tokens"],
                              "prompt_hash": prompt_hash(msgs), "retrieved_ids": []})
                k = f"{mk}|{c}|{q['language']}|{q['format']}"
                plan[k] = plan.get(k, 0) + 1
    return reqs, index, plan


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="run.plan")
    ap.add_argument("--questions", required=True)
    ap.add_argument("--atoms", required=True)
    ap.add_argument("--passages", required=True)
    ap.add_argument("--models", nargs="+", required=True)
    ap.add_argument("--out", required=True, help="thư mục ghi requests.jsonl + index.jsonl")
    ap.add_argument("--plan", required=True)
    a = ap.parse_args(argv)
    atoms = {x["atom_id"]: x for x in _jsonl(a.atoms)}
    passages = {x["passage_id"]: x["text"] for x in _jsonl(a.passages)}
    reqs, index, plan = build(_jsonl(a.questions), atoms, passages, a.models)
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    for name, rows in (("requests.jsonl", reqs), ("index.jsonl", index)):
        (out / name).write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")
    Path(a.plan).parent.mkdir(parents=True, exist_ok=True)
    Path(a.plan).write_text(json.dumps(dict(sorted(plan.items())), indent=1), encoding="utf-8")
    print(f"{len(reqs)} yêu cầu cho {len(a.models)} mô hình; kế hoạch {len(plan)} ô → {a.plan}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
