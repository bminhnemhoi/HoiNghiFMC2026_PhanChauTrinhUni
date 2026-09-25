import json

import pytest

from vnsoc import state
from vnsoc.paths import paths


def test_flow(proj, monkeypatch):
    P = paths(proj)
    st = state.init(P)
    assert [t["id"] for t in state.eligible_claude(st)] == ["T0.1"]
    assert state.done(P, "T0.1") == 1                 # README.md missing -> not done
    (proj / "README.md").write_text("x")
    assert state.done(P, "T0.1") == 0
    st = state.load(P)
    assert [t["id"] for t in state.eligible_claude(st)] == ["T0.5"]   # T0.3 waits HG0.2, T0.4 waits date
    assert [t["id"] for t in state.waiting_human(st)] == ["HG0.2"]
    assert "HG0.2" in P.human_todo.read_text()
    assert state.human_done(P, "HG0.2") == 2          # no ack from the user yet
    P.human_ack.mkdir(exist_ok=True)
    (P.human_ack / "HG0.2").write_text("XONG HG0.2")
    assert state.human_done(P, "HG0.2") == 0
    with pytest.raises(SystemExit):
        state.skip(P, "T0.3", "no")                   # not skippable
    state.skip(P, "T0.5", "DR6")
    assert "T0.5" in P.decisions.read_text()
    state.start(P, "T0.3")
    assert state.done(P, "T0.3") == 0
    monkeypatch.setenv("VNSOC_TODAY", "2099-01-02")
    assert [t["id"] for t in state.eligible_claude(state.load(P))] == ["T0.4"]


def test_init_merges_and_dynamic(proj):
    P = paths(proj)
    state.init(P)
    (proj / "README.md").write_text("x")
    state.done(P, "T0.1")
    state.add(P, "R1.1", "Sửa theo hội đồng", "claude", "review", ["T0.1"], "ok", [], None, None)
    with pytest.raises(SystemExit):
        state.add(P, "X1", "người", "human", "p", [], "", [], None, "làm đi")   # human ids must start with HG
    st = state.init(P)                                  # re-init keeps status + dynamic tasks
    assert st["tasks"]["T0.1"]["status"] == "done" and "R1.1" in st["tasks"]


def test_plan_validation_errors():
    bad = [{"id": "T1", "title": "a", "phase": "p", "owner": "claude", "depends_on": ["T2"]},
           {"id": "T2", "title": "b", "phase": "p", "owner": "claude", "depends_on": ["T1"]}]
    with pytest.raises(SystemExit):
        state.validate_plan(bad)
    with pytest.raises(SystemExit):
        state.validate_plan([{"id": "HG1", "title": "a", "phase": "p", "owner": "human"}])  # no instructions


def test_digest(proj):
    P = paths(proj)
    state.init(P)
    d = state.digest(P)
    assert "T0.1" in d and "Ngân sách" in d
    json.loads(P.progress.read_text())


def test_blocks_adds_dependency(proj):
    P = paths(proj)
    state.init(P)
    (proj / "README.md").write_text("x")
    state.done(P, "T0.1")
    assert "T0.5" in [t["id"] for t in state.eligible_claude(state.load(P))]
    state.add(P, "R1.1", "sửa", "claude", "review", ["T0.1"], "ok", [], None, None, blocks=["T0.5"])
    ids = [t["id"] for t in state.eligible_claude(state.load(P))]
    assert "R1.1" in ids and "T0.5" not in ids
    state.done(P, "R1.1")
    st = state.init(P)                                    # re-init keeps extra dependency + dynamic task
    assert st["tasks"]["T0.5"]["extra_depends"] == ["R1.1"]
    assert "T0.5" in [t["id"] for t in state.eligible_claude(st)]
