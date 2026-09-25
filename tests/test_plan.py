"""The real plan (docs/02) must be valid and every task reachable (no deadlock), given time passes."""
import datetime as dt
import json
import shutil

import pytest

from vnsoc import state
from vnsoc.paths import paths


def test_plan_is_valid_and_reachable(tmp_path, monkeypatch):
    real = paths()
    if not real.plan.exists():
        pytest.skip("docs/02_KE_HOACH_TRIEN_KHAI.md chưa có")
    (tmp_path / "docs").mkdir()
    shutil.copy(real.plan, tmp_path / "docs" / real.plan.name)
    shutil.copytree(real.root / "configs", tmp_path / "configs")
    P = paths(tmp_path)
    st = state.init(P)
    day = dt.date(2026, 9, 25)
    for _ in range(1000):
        monkeypatch.setenv("VNSOC_TODAY", day.isoformat())
        st = state.load(P)
        nxt = (state.eligible_claude(st) or state.waiting_human(st) or [None])[0]
        if nxt:
            nxt["status"] = "done"
            P.progress.write_text(json.dumps(st))
            continue
        left = [i for i in st["order"] if st["tasks"][i]["status"] != "done"]
        if not left:
            break
        day += dt.timedelta(days=1)
        assert day < dt.date(2027, 6, 1), f"kẹt: {left}"
    assert all(t["status"] == "done" for t in state.load(P)["tasks"].values())
