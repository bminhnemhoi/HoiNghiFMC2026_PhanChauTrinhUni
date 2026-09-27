"""FMC 2026 abstract: check the conference limits and build the DOCX in the official template's format (T1.6/T1.7).

Source = the RENDERED markdown (manuscript/build/fmc/<name>.md, numbers already filled), structured as
"## Ô TÓM TẮT" (Vietnamese web-form box), "## ABSTRACT BOX" (English box), "## VI" and "## EN" (each with
"### <SECTION>" blocks, the first being the title), "## GHI CHÚ" (Vietnamese note) and "## NOTE" (English note).
Limits: web-form box ≤ 500 characters (the form's maxlength=500); title ≤ 150 characters; abstract ≤ 500 words
per language — the organisers' answer to HG1.0 (26/9/2026): 500 words is the limit, 250 only recommended (warning,
counted on the five sections with their headings); 3–5 lower-case keywords separated by ";". ONE LANGUAGE PER FILE
(organisers' answer): a Vietnamese and an English DOCX are built separately, each by filling the conference's own
template (manuscript/fmc/template/, logos and layout kept; plain python-docx layout only if the template is missing).
Format: Times New Roman, title upper-case 13 pt, body 12 pt, line spacing 1.5.

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
        elif lang in ("box", "box_en"):
            doc[lang] = (doc[lang] + " " + line.strip()).strip()
        elif lang in ("note", "note_en"):             # one line per note item ("LABEL: text")
            doc[lang] = (doc[lang] + "\n" + line.strip()).strip()
    return doc


def words(s: str) -> int:
    return len(re.findall(r"\S+", s))


def body_words(doc: dict, lang: str, headings: bool = True) -> int:
    """Words of the five sections (title and keywords excluded), counted like MS Word (whitespace tokens), with the
    section headings by default — the template's 250-word recommendation applies to the abstract as printed."""
    secs = list(doc[lang].items())[1:-1]
    return sum(words(t) + (words(n + ":") if headings else 0) for n, t in secs)


def warnings(doc: dict) -> list[str]:
    """Over the recommended 250 words (allowed up to 500)."""
    out = []
    for lang in ("vi", "en"):
        n = body_words(doc, lang)
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

    def nm(a):                                      # Vietnamese file: Vietnamese name with diacritics when given
        return a.get("name_vi") or a["name"] if lang == "vi" else a["name"]

    def affil(a):                                   # one language per file: English affiliation in the EN file
        return a.get("affiliation_en") or a["affiliation"] if lang == "en" else a["affiliation"]

    aff = []
    for a in authors:
        if affil(a) not in aff:
            aff.append(affil(a))
    secs = list(doc[lang].items())
    para(secs[0][1].upper(), bold=True, size=13, align=WD_ALIGN_PARAGRAPH.CENTER)
    para(", ".join(f"{nm(a)}{'¹²³⁴⁵'[aff.index(affil(a))]}" for a in authors),
         align=WD_ALIGN_PARAGRAPH.CENTER)
    for k, af in enumerate(aff):
        para(f"{'¹²³⁴⁵'[k]}{af}", italic=True, align=WD_ALIGN_PARAGRAPH.CENTER)
    corr = [a for a in authors if a.get("corresponding") and a.get("email")]
    for a in corr:                                  # corresponding author line (name + e-mail), language of the file
        para(f"{'Tác giả liên hệ' if lang == 'vi' else 'Corresponding author'}: {nm(a)}, {a['email']}",
             align=WD_ALIGN_PARAGRAPH.CENTER, size=11)
    for name, text in secs[1:]:
        para(text, label=name.upper(), align=WD_ALIGN_PARAGRAPH.JUSTIFY)
    note = doc["note"] if lang == "vi" else (doc.get("note_en") or "")
    if note:
        para("")
        para(note, italic=True)
    out.parent.mkdir(parents=True, exist_ok=True)
    d.save(out)


TEMPLATE = Path("manuscript") / "fmc" / "template" / "FMC2026_Huong-dan-viet-Abstract.docx"
# Header lines of the official template, per file language (the template itself is Vietnamese-only; "MẪU" = "form",
# dropped once the form is filled).
HEADER = {"vi": ("HỘI NGHỊ KHOA HỌC FMC - 2026", "TÓM TẮT BÁO CÁO KHOA HỌC"),
          "en": ("FMC 2026 SCIENTIFIC CONFERENCE", "ABSTRACT")}
CORR = {"vi": "Tác giả liên hệ", "en": "Corresponding author"}
SLOTS = ("ĐẶT VẤN ĐỀ", "MỤC TIÊU", "PHƯƠNG PHÁP NGHIÊN CỨU", "KẾT QUẢ", "KẾT LUẬN", "TỪ KHÓA")


def nbsp(text: str) -> str:
    """Keep short units on one line in print: "Bộ Y tế" and "p = 0,15" never break across lines."""
    for w in ("Bộ Y tế", "BỘ Y TẾ"):
        text = text.replace(w, w.replace(" ", " "))
    return text.replace("p = ", "p = ")


def build_docx_template(doc: dict, out: Path, authors: list[dict], lang: str, template: Path) -> None:
    """Fill the conference's own template DOCX (logos in the page header, colours, fonts and layout kept): title,
    authors with superscript affiliation numbers, affiliations, corresponding author, the five sections, keywords and
    the closing note lines ("LABEL: text"); the template's instruction lines (hints, HÌNH THỨC, HẠN NỘP, the topic list
    on page 2) are removed. Body paragraphs get the 1.5 line spacing the template's instructions require."""
    from copy import deepcopy

    from docx import Document
    from docx.shared import Pt, RGBColor
    from docx.text.paragraph import Paragraph

    d = Document(str(template))
    paras = d.paragraphs

    def find(prefix: str, start: int = 0) -> int:
        for i in range(start, len(paras)):
            if paras[i].text.strip().startswith(prefix):
                return i
        raise ValueError(f"mẫu không có đoạn bắt đầu bằng {prefix!r}")

    def fill(p, parts):
        """Replace p's runs by parts [(text, overrides)], each run copying the formatting of p's first run."""
        base = deepcopy(p.runs[0]._element.rPr) if p.runs and p.runs[0]._element.rPr is not None else None
        for r in list(p.runs):
            r._element.getparent().remove(r._element)
        for text, fmt in parts:
            r = p.add_run(text)
            if base is not None:
                r._element.insert(0, deepcopy(base))
            for k, v in fmt.items():
                if k == "color":
                    r.font.color.rgb = RGBColor.from_string(v)
                elif k == "size":
                    r.font.size = Pt(v)
                else:
                    setattr(r.font, k, v)

    def clone_after(p):
        e = deepcopy(p._element)
        p._element.addnext(e)
        return Paragraph(e, p._parent)

    def drop(p):
        p._element.getparent().remove(p._element)

    plain = {"bold": False, "italic": False, "color": "000000"}
    label = {"bold": True, "italic": False, "color": "153D63"}      # the template's heading colour
    nm = (lambda a: a.get("name_vi") or a["name"]) if lang == "vi" else (lambda a: a["name"])
    affil = (lambda a: a.get("affiliation_en") or a["affiliation"]) if lang == "en" else (lambda a: a["affiliation"])
    aff: list[str] = []
    for a in authors:
        if affil(a) not in aff:
            aff.append(affil(a))

    i_conf, i_form = find("HỘI NGHỊ KHOA HỌC"), find("MẪU")
    fill(paras[i_conf], [(HEADER[lang][0], {})])
    fill(paras[i_form], [(HEADER[lang][1], {})])
    secs = list(doc[lang].items())
    i_title = find("TIÊU ĐỀ")
    fill(paras[i_title], [(nbsp(secs[0][1].upper()), {})])
    i_au = find("Tên đầy đủ tác giả")
    parts = []
    for k, a in enumerate(authors):
        parts += [((", " if k else "") + nm(a), {"superscript": False}),
                  (str(aff.index(affil(a)) + 1), {"superscript": True})]
    fill(paras[i_au], parts)
    paras[i_au].paragraph_format.first_line_indent = 0  # the template indents these centred lines (bad wrapping)
    aff_slots = [p for p in paras[i_au + 1:find("[Tên của")] if "Khoa/" in p.text]
    while len(aff_slots) < len(aff):
        aff_slots.append(clone_after(aff_slots[-1]))
    for k, p in enumerate(aff_slots):
        if k >= len(aff):
            drop(p)
            continue
        fill(p, [(str(k + 1), {"superscript": True}),
                 (aff[k] + (";" if k < len(aff) - 1 else ""), {"superscript": False})])
        p.paragraph_format.first_line_indent = 0
    corr = [a for a in authors if a.get("corresponding") and a.get("email")]
    paras = d.paragraphs
    hint_au = paras[find("[Tên của")]
    if corr:
        fill(hint_au, [(f"{CORR[lang]}: {nm(corr[0])}, {corr[0]['email']}", dict(plain, size=11))])
    else:
        drop(hint_au)
    drop(paras[find("[Tiêu đề")])
    paras = d.paragraphs

    slots = [next(i for i, p in enumerate(paras) if p.text.strip().startswith(s)) for s in SLOTS]
    if len(secs) != len(SLOTS) + 1:
        raise ValueError(f"{lang}: cần tiêu đề + {len(SLOTS)} mục, có {len(secs)}")
    for k, (i, (name, text)) in enumerate(zip(slots, secs[1:])):   # as in the template: no-break space after a
        sep = ": " if k == len(SLOTS) - 1 else ": "             # section heading, plain space after TỪ KHÓA
        fill(paras[i], [(f"{name.upper()}{sep}", label), (nbsp(text), plain)])
    for p in paras[slots[0]:slots[-1] + 1]:
        p.paragraph_format.line_spacing = 1.5

    i_form_note, i_deadline = find("HÌNH THỨC:"), find("HẠN NỘP")
    note_p = paras[i_form_note]
    lines = [x for x in (doc["note"] if lang == "vi" else doc.get("note_en") or "").split("\n") if x.strip()]
    tail = [note_p]
    for _ in lines[1:]:
        tail.append(clone_after(tail[-1]))
    for p, line in zip(tail, lines):
        head, sep, rest = line.partition(": ")
        fill(p, [(f"{head.upper()}: ", label), (rest, plain)] if sep and head.isupper() else [(line, plain)])
        p.paragraph_format.line_spacing = 1.5
    if not lines:
        drop(note_p)
    for p in paras[i_deadline:]:                    # deadline line and the topic list page
        drop(p)
    out.parent.mkdir(parents=True, exist_ok=True)
    d.save(str(out))


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
    template = paths().root / TEMPLATE
    for lang in ("vi", "en"):
        out = src.with_name(f"{src.stem}_{lang}.docx")
        if template.exists():                       # the conference's own template (logos, layout)
            build_docx_template(doc, out, cfg["authors"], lang, template)
        else:
            build_docx(doc, out, cfg["authors"], lang)
        sizes[lang] = out.stat().st_size
        if lang == "vi":                            # <stem>.docx = the Vietnamese file (plan checks this name)
            import shutil

            shutil.copyfile(out, src.with_suffix(".docx"))
        box = doc["box"] if lang == "vi" else (doc.get("box_en") or "")
        if box:
            src.with_name(f"{src.stem}_box_{lang}.txt").write_text(unicodedata.normalize("NFC", box) + "\n",
                                                                  encoding="utf-8")
    vi, en = body_words(doc, "vi"), body_words(doc, "en")
    print(f"ô tóm tắt VI {len(unicodedata.normalize('NFC', doc['box']))} ký tự, EN "
          f"{len(unicodedata.normalize('NFC', doc.get('box_en') or ''))} ký tự; VI {vi} từ; EN {en} từ (5 mục, kể cả tên mục); "
          f"DOCX VI {sizes['vi']} bytes, EN {sizes['en']} bytes")
    return 1 if probs else 0


if __name__ == "__main__":
    sys.exit(main())
