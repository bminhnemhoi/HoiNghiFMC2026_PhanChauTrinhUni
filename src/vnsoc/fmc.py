"""FMC 2026 abstract: check the conference limits and build the DOCX in the official template's format (T1.6/T1.7).

Source = the RENDERED markdown (manuscript/build/fmc/<name>.md, numbers already filled), structured as
"## Ô TÓM TẮT" (Vietnamese web-form box), "## ABSTRACT BOX" (English box), "## VI" and "## EN" (each with
"### <SECTION>" blocks, the first being the title), "## GHI CHÚ" (Vietnamese note) and "## NOTE" (English note).
Limits: web-form box ≤ 500 characters (the form's maxlength=500); title ≤ 150 characters; abstract ≤ 500 words
per language — the organisers' answer to HG1.0 (26/9/2026): 500 words is the limit, 250 only recommended (warning);
3–5 lower-case keywords separated by ";". ONE LANGUAGE PER FILE (organisers' answer): a Vietnamese and an English
DOCX are built separately. Format: Times New Roman, title upper-case 13 pt, body 12 pt, line spacing 1.5.

  $PY -m vnsoc.fmc manuscript/build/fmc/abstract_fmc.md   # -> _vi.docx, _en.docx, _box_vi.txt, _box_en.txt
"""
from __future__ import annotations

import re
import sys
import unicodedata
from pathlib import Path

import yaml

from vnsoc.paths import paths

BOX_MAX, TITLE_MAX, WORDS_MAX, WORDS_REC = 500, 150, 500, 250


def parse(md: str) -> dict:
    doc, lang, sec = {"box": "", "box_en": "", "vi": {}, "en": {}, "note": "", "note_en": ""}, None, None
    for line in md.splitlines():
        if line.startswith("## "):
            head = line[3:].strip()
            lang = {"VI": "vi", "EN": "en"}.get(head, "box" if head.startswith("Ô TÓM TẮT") else
                                                 "box_en" if head.upper().startswith("ABSTRACT BOX") else
                                                 "note" if head.startswith("GHI CHÚ") else
                                                 "note_en" if head.upper().startswith("NOTE") else None)
            sec = None
            continue
        if line.startswith("### ") and lang in ("vi", "en"):
            sec = line[4:].strip()
            doc[lang][sec] = ""
            continue
        if not line.strip():
            continue
        if lang in ("vi", "en") and sec:
            doc[lang][sec] = (doc[lang][sec] + " " + line.strip()).strip()
        elif lang in ("box", "box_en", "note", "note_en"):
            doc[lang] = (doc[lang] + " " + line.strip()).strip()
    return doc


def words(s: str) -> int:
    return len(re.findall(r"\S+", s))


def warnings(doc: dict) -> list[str]:
    """Over the recommended 250 words (allowed up to 500)."""
    out = []
    for lang in ("vi", "en"):
        n = sum(words(t) for _, t in list(doc[lang].items())[1:-1])
        if n > WORDS_REC:
            out.append(f"{lang}: {n} từ > {WORDS_REC} (khuyến khích; giới hạn {WORDS_MAX})")
    return out


def checks(doc: dict) -> list[str]:
    probs = []
    for key, name in (("box", "ô tóm tắt"), ("box_en", "ô tóm tắt tiếng Anh")):
        box = unicodedata.normalize("NFC", doc.get(key) or "")
        if key == "box_en" and not box:
            continue
        if not box or len(box) > BOX_MAX:
            probs.append(f"{name} {len(box)} ký tự (tối đa {BOX_MAX})")
    for lang in ("vi", "en"):
        secs = list(doc[lang].items())
        if len(secs) < 7:
            probs.append(f"{lang}: thiếu mục (có {len(secs)}, cần tiêu đề + 5 mục + từ khóa)")
            continue
        title, body, kw = secs[0][1], secs[1:-1], secs[-1][1]
        if len(title) > TITLE_MAX:
            probs.append(f"{lang}: tiêu đề {len(title)} ký tự > {TITLE_MAX}")
        n = sum(words(t) for _, t in body)
        if n > WORDS_MAX:
            probs.append(f"{lang}: {n} từ > {WORDS_MAX}")
        kws = [k.strip() for k in kw.split(";") if k.strip()]
        if not 3 <= len(kws) <= 5 or any(k != k.lower() for k in kws):
            probs.append(f"{lang}: từ khóa phải 3–5, viết thường, cách nhau ';' (có {kws})")
        if "{{" in title + kw + "".join(t for _, t in body):
            probs.append(f"{lang}: còn placeholder chưa điền")
    return probs


def build_docx(doc: dict, out: Path, authors: list[dict], lang: str = "vi") -> None:
    """One-language DOCX (the organisers accept one language per file)."""
    from docx import Document
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.oxml.ns import qn
    from docx.shared import Cm, Pt

    d = Document()
    for s in d.sections:
        s.top_margin = s.bottom_margin = Cm(2)
        s.left_margin = s.right_margin = Cm(2.5)
    st = d.styles["Normal"]
    st.font.name, st.font.size = "Times New Roman", Pt(12)
    st.element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
    st.paragraph_format.line_spacing = 1.5
    st.paragraph_format.space_after = Pt(0)

    def para(text="", bold=False, size=12, align=None, italic=False, label=None):
        p = d.add_paragraph()
        if align:
            p.alignment = align
        if label:
            r = p.add_run(label + ": ")
            r.bold, r.font.size = True, Pt(size)
        r = p.add_run(text)
        r.bold, r.italic, r.font.size = bold, italic, Pt(size)
        return p

    def affil(a):                                   # one language per file: English affiliation in the EN file
        return a.get("affiliation_en") or a["affiliation"] if lang == "en" else a["affiliation"]

    aff = []
    for a in authors:
        if affil(a) not in aff:
            aff.append(affil(a))
    secs = list(doc[lang].items())
    para(secs[0][1].upper(), bold=True, size=13, align=WD_ALIGN_PARAGRAPH.CENTER)
    para(", ".join(f"{a['name']}{'¹²³⁴⁵'[aff.index(affil(a))]}" for a in authors),
         align=WD_ALIGN_PARAGRAPH.CENTER)
    for k, af in enumerate(aff):
        para(f"{'¹²³⁴⁵'[k]}{af}", italic=True, align=WD_ALIGN_PARAGRAPH.CENTER)
    for name, text in secs[1:]:
        para(text, label=name.upper(), align=WD_ALIGN_PARAGRAPH.JUSTIFY)
    note = doc["note"] if lang == "vi" else (doc.get("note_en") or "")
    if note:
        para("")
        para(note, italic=True)
    out.parent.mkdir(parents=True, exist_ok=True)
    d.save(out)


def main(argv=None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    src = Path(argv[0])
    doc = parse(src.read_text(encoding="utf-8"))
    probs = checks(doc)
    for p in probs:
        print("LỖI", p)
    for w in warnings(doc):
        print("CẢNH BÁO", w)
    cfg = yaml.safe_load((paths().configs / "project.yaml").read_text(encoding="utf-8"))
    sizes = {}
    for lang in ("vi", "en"):
        out = src.with_name(f"{src.stem}_{lang}.docx")
        build_docx(doc, out, cfg["authors"], lang)
        sizes[lang] = out.stat().st_size
        box = doc["box"] if lang == "vi" else (doc.get("box_en") or "")
        if box:
            src.with_name(f"{src.stem}_box_{lang}.txt").write_text(unicodedata.normalize("NFC", box) + "\n",
                                                                  encoding="utf-8")
    vi = sum(words(t) for _, t in list(doc["vi"].items())[1:-1])
    en = sum(words(t) for _, t in list(doc["en"].items())[1:-1])
    print(f"ô tóm tắt VI {len(unicodedata.normalize('NFC', doc['box']))} ký tự, EN "
          f"{len(unicodedata.normalize('NFC', doc.get('box_en') or ''))} ký tự; VI {vi} từ; EN {en} từ; "
          f"DOCX VI {sizes['vi']} bytes, EN {sizes['en']} bytes")
    return 1 if probs else 0


if __name__ == "__main__":
    sys.exit(main())
