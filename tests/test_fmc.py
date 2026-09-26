"""FMC abstract: parser, conference limits, DOCX build (synthetic text)."""
import pytest

from vnsoc import fmc

SECT_VI = ["TIÊU ĐỀ", "ĐẶT VẤN ĐỀ", "MỤC TIÊU", "PHƯƠNG PHÁP NGHIÊN CỨU", "KẾT QUẢ", "KẾT LUẬN", "TỪ KHÓA"]
SECT_EN = ["TITLE", "BACKGROUND", "OBJECTIVE", "METHODS", "RESULTS", "CONCLUSION", "KEYWORDS"]


def md(box="Tóm tắt ngắn.", body="nội dung ngắn gọn", kw_vi="a; b; c", kw_en="x; y; z", title="Tên đề tài"):
    out = ["# x", "", "## Ô TÓM TẮT", "", box, "", "## VI", ""]
    for s in SECT_VI:
        out += [f"### {s}", "", title if s == "TIÊU ĐỀ" else kw_vi if s == "TỪ KHÓA" else body, ""]
    out += ["## EN", ""]
    for s in SECT_EN:
        out += [f"### {s}", "", title if s == "TITLE" else kw_en if s == "KEYWORDS" else body, ""]
    return "\n".join(out + ["## GHI CHÚ", "", "Chưa đăng.", ""])


def test_parse_and_ok():
    d = fmc.parse(md())
    assert d["box"] == "Tóm tắt ngắn." and list(d["vi"])[0] == "TIÊU ĐỀ" and d["note"] == "Chưa đăng."
    assert fmc.checks(d) == []


@pytest.mark.parametrize("kw,problem", [
    (dict(box="x" * 501), "ký tự"), (dict(body=" ".join(["từ"] * 60)), "từ >"), (dict(kw_vi="a; b"), "từ khóa"),
    (dict(kw_en="X; y; z"), "từ khóa"), (dict(title="t" * 151), "tiêu đề"), (dict(body="có {{design.x}}"), "placeholder"),
])
def test_limits(kw, problem):
    assert any(problem in p for p in fmc.checks(fmc.parse(md(**kw))))


def test_docx(tmp_path):
    pytest.importorskip("docx")
    out = tmp_path / "a.docx"
    fmc.build_docx(fmc.parse(md()), out, [{"name": "Bình Minh", "affiliation": "Khoa CNTT, TDTU, Việt Nam"}])
    import docx

    text = "\n".join(p.text for p in docx.Document(out).paragraphs)
    assert "TÊN ĐỀ TÀI" in text and "Bình Minh¹" in text and "ĐẶT VẤN ĐỀ: nội dung" in text and "KEYWORDS: x; y; z" in text
    assert 0 < out.stat().st_size < 1_000_000
