import json

from vnsoc.check import main
from test_schemas import BASE
from pathlib import Path

ROOT_KIT = Path(__file__).resolve().parents[1]


def test_check_jsonl_and_count(proj, tmp_path):
    f = tmp_path / "a.jsonl"
    rows = [dict(BASE, atom_id=f"a{i}", span_verified=True, conflict_status="conflict", conflict_family=f"f{i % 3}")
            for i in range(5)]
    f.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n", encoding="utf-8")
    assert main(["jsonl", "atom", str(f), "--min", "5", "--require", "span_verified=true"]) == 0
    assert main(["jsonl", "atom", str(f), "--min", "6"]) == 1
    assert main(["count", str(f), "--min", "5", "--where", "conflict_status=conflict"]) == 0
    assert main(["families", str(f), "--min", "3"]) == 0 and main(["families", str(f), "--min", "4"]) == 1


def test_nofill_and_size(tmp_path):
    f = tmp_path / "abs.md"
    f.write_text("Kết quả: [a] mẩu\n", encoding="utf-8")
    assert main(["nofill", str(f)]) == 1
    f.write_text("Kết quả: 12 mẩu\n", encoding="utf-8")
    assert main(["nofill", str(f)]) == 0
    assert main(["maxsize", str(f), "1000"]) == 0


def test_check_runs(tmp_path):
    d = tmp_path / "runs"
    d.mkdir()
    rec = dict(run_id="r", model="qwen3_8b", model_version="abc", date="2026-11-05", atom_id="a", question_id="q",
               format="short", language="vi", condition="A1", temperature=0.0, max_tokens=128, prompt_hash="h",
               raw_output="ĐÁP ÁN: 15 ml/kg/giờ", backend="vllm")
    (d / "x.jsonl").write_text("\n".join(json.dumps(dict(rec, run_id=f"r{i}")) for i in range(10)) + "\n")
    plan = tmp_path / "plan.json"
    plan.write_text(json.dumps({"qwen3_8b|A1|vi|short": 10, "qwen3_8b|A2|vi|short": 10}))
    assert main(["runs", str(d), "--plan", str(plan), "--conditions", "A1"]) == 0
    assert main(["runs", str(d), "--plan", str(plan)]) == 1          # A2 missing


def test_review_gate_requires_user(proj, monkeypatch):
    from vnsoc import state
    from vnsoc.paths import paths
    from test_review import write
    P = paths(proj)
    state.init(P)
    write(proj, 6)                                          # panel fails
    assert main(["review", "M1"]) == 1
    (proj / "review" / "M1" / "response.md").write_text("Người dùng quyết định: tiếp tục")
    assert main(["review", "M1"]) == 1                      # Claude writing text is not enough
    state.add(P, "HGM1", "Quyết định", "human", "review", [], "", [], None, "chọn A hoặc B")
    P.human_ack.mkdir(exist_ok=True)
    (P.human_ack / "HGM1").write_text("XONG HGM1 chọn A")
    assert state.human_done(P, "HGM1") == 0
    assert main(["review", "M1"]) == 0


def test_runs_models_from_config(tmp_path, proj):
    d = tmp_path / "runs"
    d.mkdir()
    rec = dict(run_id="r", model="qwen3_8b", model_version="abc", date="2026-11-05", atom_id="a", question_id="q",
               format="short", language="vi", condition="A1", temperature=0.0, max_tokens=128, prompt_hash="h",
               raw_output="x", backend="vllm")
    (d / "x.jsonl").write_text(json.dumps(rec) + "\n")
    plan = tmp_path / "plan.json"
    plan.write_text(json.dumps({"qwen3_8b|A1|vi|short": 1, "cheap_1|A1|vi|short": 5}))
    assert main(["runs", str(d), "--plan", str(plan), "--models-from", "open"]) == 0
    assert main(["runs", str(d), "--plan", str(plan), "--models-from", "api_cheap"]) == 1


def test_kaggle_render_name(proj):
    from vnsoc.run.kaggle_jobs import render
    import shutil
    (proj / "kaggle").mkdir()
    shutil.copy(ROOT_KIT / "kaggle" / "runner_template.py", proj / "kaggle" / "runner_template.py")
    d = render("vnsoc-weights", {"shards": [], "user": "u"}, proj)
    meta = json.loads((d / "kernel-metadata.json").read_text())
    assert d.name == "vnsoc-weights" and meta["id"] == "u/vnsoc-weights" and meta["is_private"] is True
    d2 = render("a1-qwen", {"shards": [], "user": "u"}, proj)
    assert json.loads((d2 / "kernel-metadata.json").read_text())["id"] == "u/vnsoc-a1-qwen"
    compile((d / "run.py").read_text(), "run.py", "exec")
