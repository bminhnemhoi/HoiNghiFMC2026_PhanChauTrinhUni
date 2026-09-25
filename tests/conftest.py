import shutil
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

MINI_PLAN = '''# Kế hoạch thử
<!-- TASKS:BEGIN -->
```yaml
tasks:
  - {id: T0.1, title: "Tạo repo", phase: P0, owner: claude, outputs: ["README.md"], check: "test -f README.md"}
  - {id: HG0.2, title: "Điền khóa", phase: P0, owner: human, depends_on: [T0.1], instructions: "Điền .env"}
  - {id: T0.3, title: "Chạy thử", phase: P0, owner: claude, depends_on: [HG0.2], check: "exit 0"}
  - {id: T0.4, title: "Chờ ngày", phase: P0, owner: claude, depends_on: [T0.1], not_before: "2099-01-01"}
  - {id: T0.5, title: "Có thể bỏ", phase: P0, owner: claude, depends_on: [T0.1], skippable: true}
```
<!-- TASKS:END -->
'''


@pytest.fixture
def proj(tmp_path, monkeypatch):
    """A throw-away project root with the mini plan, hooks and configs copied in."""
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "02_KE_HOACH_TRIEN_KHAI.md").write_text(MINI_PLAN, encoding="utf-8")
    (tmp_path / "pyproject.toml").write_text("[project]\nname='x'\n")
    shutil.copytree(ROOT / "src", tmp_path / "src")
    shutil.copytree(ROOT / ".claude", tmp_path / ".claude")
    shutil.copytree(ROOT / "configs", tmp_path / "configs")
    monkeypatch.setenv("VNSOC_ROOT", str(tmp_path))
    monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(tmp_path))
    return tmp_path
