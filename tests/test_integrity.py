"""Static integrity checks on the repo itself (run in `make test`; tasks add code under src/ that must keep passing)."""
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
ID = re.compile(r"\b(?:T\d+\.\d+[a-z]?|HG\d+\.\d+[a-z]?|HGM\d+)\b")   # 'HG2.9_osf.txt' is a file name, not an id


def _plan_ids():
    plan = ROOT / "docs" / "02_KE_HOACH_TRIEN_KHAI.md"
    if not plan.exists():
        pytest.skip("chưa có docs/02")
    block = plan.read_text(encoding="utf-8").split("<!-- TASKS:BEGIN -->")[1]
    return set(re.findall(r"^- id: (\S+)", block, re.M))


def test_task_ids_mentioned_in_instructions_exist():
    ids = _plan_ids() | {"HGM2", "HGM3", "HGM4"}          # milestone decision gates are added dynamically
    files = [ROOT / "CLAUDE.md", *ROOT.glob(".claude/**/*.md"), *ROOT.glob(".claude/**/*.py")]
    missing = {(f.relative_to(ROOT).as_posix(), m) for f in files for m in ID.findall(f.read_text(encoding="utf-8"))
               if m not in ids}
    assert not missing, sorted(missing)


def _code_files():
    for base in ("src", "scripts", "kaggle"):
        for f in (ROOT / base).rglob("*"):
            if f.is_file() and f.suffix in (".py", ".sh", ".R", "") and "__pycache__" not in f.parts:
                yield f


def test_no_forbidden_access_in_code():
    allowed_tvpl = {"src/vnsoc/schemas.py"}
    allowed_api = {"src/vnsoc/run/api_batch.py"}
    allowed_ack = {"src/vnsoc/state.py", "src/vnsoc/paths.py", "src/vnsoc/check.py"}  # check.py only reads
    bad = []
    for f in _code_files():
        rel = f.relative_to(ROOT).as_posix()
        text = f.read_text(encoding="utf-8", errors="ignore")
        if "thuvienphapluat" in text and rel not in allowed_tvpl:
            bad.append(f"{rel}: thuvienphapluat")
        if re.search(r"^\s*(?:import openai|from openai|from google import genai|import google\.genai)", text, re.M) \
                and rel not in allowed_api:
            bad.append(f"{rel}: gọi SDK API trả phí ngoài api_batch (không qua sổ ngân sách)")
        if ".human_ack" in text and rel not in allowed_ack:
            bad.append(f"{rel}: chạm vào xác nhận của người dùng")
    assert not bad, bad
