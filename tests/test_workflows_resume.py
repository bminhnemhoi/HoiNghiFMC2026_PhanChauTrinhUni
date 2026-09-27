"""scripts/workflows/resume_args.py: a page chunk counts as done only when its coverage file reaches the last page."""
import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "resume_args", Path(__file__).resolve().parents[1] / "scripts" / "workflows" / "resume_args.py")
ra = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ra)


def test_coverage_formats(tmp_path):
    f = tmp_path / "c.md"
    f.write_text("| Trang PDF (in) | Mẩu |\n|---|---|\n| 67 (60) | 2 |\n| 68–70 (61–63) | 0 |\n", encoding="utf-8")
    assert ra.coverage_last_page(f, 67, 99) == 70
    f.write_text("## Trang đã đọc (33/33)\n| 67 (60) | 2 |\n", encoding="utf-8")
    assert ra.coverage_last_page(f, 67, 99) == 99                    # whole chunk declared read
    f.write_text("## Trang đã đọc (20/33)\n| 5 | x |\n| 2024 | năm |\n", encoding="utf-8")
    assert ra.coverage_last_page(f, 1, 33) == 5                      # numbers outside the chunk are ignored


def test_part_names():
    d = {"key": "162/2024", "chunks": [[1, 36], [37, 72]]}
    assert ra.part_name(d, [37, 72]) == "162_2024__p037-072"
    assert ra.part_name({"key": "TT51/2017", "chunks": [[1, 20]]}, [1, 20]) == "TT51_2017"
