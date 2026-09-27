"""scripts/build_fmc_package.py: web-form field texts respect the live form's limits."""
import importlib.util
from pathlib import Path

import pytest

spec = importlib.util.spec_from_file_location(
    "build_fmc_package", Path(__file__).resolve().parents[1] / "scripts" / "build_fmc_package.py")
pkg = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pkg)

AU = [{"name": "Binh Minh Ngo", "name_vi": "Ngô Bình Minh", "affiliation": "Khoa CNTT, TDTU, Việt Nam",
       "email": "a@b.vn", "corresponding": True},
      {"name": "B", "name_vi": "Bê", "affiliation": "Khoa Y, PCTU, Việt Nam"},
      {"name": "C", "name_vi": "Xê", "affiliation": "Khoa Y, PCTU, Việt Nam"}]


def _doc(box="Tóm tắt ngắn.", title="Tên đề tài"):
    return {"box": box, "box_en": "Short.", "vi": {"TIÊU ĐỀ": title}, "en": {"TITLE": "Title"}}


def test_fields_in_form_order_and_shared_affiliations():
    rows = pkg.form_fields(_doc(), AU)
    assert [r[1] for r in rows] == ["chude[]", "Tendetai", "Donvi", "tacgia", "tomtat", "email", "file"]
    d = dict((r[1], r[2]) for r in rows)
    assert d["Donvi"] == "(1) Khoa CNTT, TDTU, Việt Nam; (2) Khoa Y, PCTU, Việt Nam"
    assert d["tacgia"] == "Ngô Bình Minh (1) – tác giả liên hệ; Bê (2); Xê (2)" and d["email"] == "a@b.vn"


@pytest.mark.parametrize("kw", [dict(box="x" * 501), dict(title="t" * 151)])
def test_over_limit_is_refused(kw):
    with pytest.raises(SystemExit):
        pkg.form_fields(_doc(**kw), AU)
