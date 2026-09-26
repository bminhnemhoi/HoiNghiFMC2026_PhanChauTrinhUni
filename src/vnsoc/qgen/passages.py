"""A3 oracle passages (proposal §4.4; skill question-generation step 6): 150–300 words of the official page text
around the atom's span, cut at sentence boundaries, never mid-sentence; the span is always fully included.

Sentence boundary = ". ; ! ?" + whitespace + an upper-case letter (Unicode category Lu), a digit, a bullet/dash,
"(", an opening quote or a list marker ("d) ", "a. "). Never ":" (a list introduced by ":" stays with its items) and
never before a lower-case word (Vietnamese lower-case letters such as "ư", "à", "đ" do not start a sentence).
A page's unfinished first sentence (the page starts lower-case: it began on the previous page) and unfinished last
sentence (no ". ; ! ?" at the page end, e.g. "…một trong các biểu hiện:") are never added around the span; they
are kept only when the span itself lies in them.

Page furniture is removed OUTSIDE the span before cutting (privacy: stamps carry real officials' names):
digital-signature / clerk stamps "<login>.kcb_<Name>_<date [time]>", "syt_<province>_vt_<Name>_<date>",
"kcb_<Name>_<date>" (login with dots/hyphens; dates d/m/yyyy, d-m-yyyy, d.m.yyyy or yyyy/m/d), signature blocks
"Ký bởi|Người ký: … (Ngày|Giờ|Thời gian) ký: <date time tz>", a signer's name after "Ký bởi:/Người ký:" when the
block has no date (capitalised words, or words up to the next field label "Cơ quan:/Chức vụ:/Email:"), e-mail
addresses, kcb.vn / LuatVietnam watermarks, a bare printed page number at the start of the page (before an
upper-case word, a list marker or a numbered heading; "15 người bệnh…" is a count, not a page number) and bare numbers
left at its end (also right after a span that ends the page). (vnsoc.extract.pdf_to_text.furniture works on PDF lines; page texts here
are whitespace-collapsed, so the same idea is applied with in-line patterns.)
A passage that still looks like a signature block, stamp or e-mail (`residual_furniture`) fails the A3 QC row.
Pages read from the OCR sidecar are flagged (`passage_ocr`): their text must be checked against the page image.
"""
from __future__ import annotations

import re
import unicodedata

from vnsoc import normalize_vi as nv
from vnsoc.extract.verify_span import norm, ocr_pages, page_text, pdf_path

SENT_END = re.compile(r"(?<=[.;!?])\s+")
BULLETS = set("•-–—+*(")
DATE = r"(?:\d{1,2}[-/.]\d{1,2}[-/.]\d{4}|\d{4}[-/.]\d{1,2}[-/.]\d{1,2})"
TIME = r"(?:\s+\d{1,2}:\d{2}(?::\d{2})?)?(?:\s*[+-]\d{2}:?\d{2})?"
STAMP = re.compile(r"(?<![\w.@-])[A-Za-z0-9][\w.-]*_[^_\n]{1,80}?_" + DATE + TIME)
SIGN_BLOCK = re.compile(r"(?:Ký bởi|Người ký):?.{0,240}?(?:Ngày|Giờ|Thời gian) ký:?\s*" + DATE + TIME, re.I)
SIGNER = re.compile(r"(?:Ký bởi|KÝ BỞI|Người ký|NGƯỜI KÝ)\s*:?\s*|(?i:ký bởi|người ký)\s*:\s*")   # not "được ký bởi"
FIELD = re.compile(r"(?:Cơ quan|Chức vụ|Email|E-mail|Thời gian ký|Ngày ký|Giờ ký)\s*:", re.I)
EMAIL = re.compile(r"(?:E-?mail\s*:\s*)?[\w.+-]+@[\w-]+(?:\.[\w-]+)+", re.I)
WATERMARK = re.compile(r"(?:https?://)?(?:www\.)?(?:luatvietnam|kcb)\.vn\S*|(?<![\w.])LuatVietnam(?!\w)", re.I)
LEAD_PAGE_NO = re.compile(r"^(\d{1,3}) (?=(?:[-•*] )?[^\W\d_]|\d+(?:\.\d+)*\. )")
TAIL_NUMBERS = re.compile(r"(?<=[.;:!?)\]])(?:\s+\d{1,4}){1,3}\s*$")
_UNIT_AT = re.compile(nv.UNIT_RE, re.I)


LIST_MARK = re.compile(r"[a-zđ][).] ")                 # "d) Sau khi…", "a. Điều trị…"
QUOTES = set("“\"‘«")
TERMINAL = re.compile(r"[.;!?][)\]”\"’»]*\s*$")


def _starts_sentence(text: str, k: int) -> bool:
    ch = text[k]
    return (ch.isdigit() or ch in BULLETS or ch in QUOTES or unicodedata.category(ch) == "Lu"
            or bool(LIST_MARK.match(text, k)))


NUMBERING = re.compile(r"(?:[A-Z]|\d{1,2}|[IVX]{1,5})(?:\.\d{1,2}){0,4}\.?")   # "5.", "C.2.3.", "IV."


def _sentences(text: str) -> list[tuple[int, int]]:
    out, start = [], 0
    for m in SENT_END.finditer(text):
        if m.end() < len(text) and _starts_sentence(text, m.end()):
            if NUMBERING.fullmatch(text[start:m.start()]):
                continue                                # a bare heading number stays with its heading
            out.append((start, m.start()))
            start = m.end()
    out.append((start, len(text)))
    return [(a, b) for a, b in out if b > a]


def _drop(pattern: re.Pattern, s: str) -> str:
    return pattern.sub(" ", s)


def _drop_signers(s: str) -> str:
    """'Ký bởi: Xxx Yyy Cơ quan: …' without a signing date: drop the label and the signer's name (words up to the
    next field label, else the capitalised words that follow, at most 8)."""
    out, pos = [], 0
    for m in SIGNER.finditer(s):
        if m.start() < pos:
            continue
        nxt = FIELD.search(s, m.end(), m.end() + 120)
        if nxt:
            end = nxt.start()
        else:
            end, n = m.end(), 0
            for w in re.finditer(r"\S+", s[m.end():]):
                if n >= 8 or unicodedata.category(w.group(0)[0]) != "Lu":
                    break
                end, n = m.end() + w.end(), n + 1
        out.append(s[pos:m.start()] + " ")
        pos = end
    return "".join(out) + s[pos:]


def _strip_head(pre: str, rest: str, page: int | None) -> str:
    """Bare printed page number at the start of the page ('10 b) Phụ nữ…' -> 'b) Phụ nữ…'): only a number no larger
    than the PDF page, followed by a word that is not a unit, a bullet + word, or a numbered heading ('48 2.2.2.').
    `rest` (the span and what follows) is only looked at, never cut."""
    full = pre + rest
    m = LEAD_PAGE_NO.match(full)
    if (m and m.end() <= len(pre) and (page is None or 1 <= int(m.group(1)) <= page)
            and not _UNIT_AT.match(full[m.end():]) and _starts_sentence(full, m.end())):
        return pre[m.end():]
    return pre


def clean_page(page_txt: str, span: str, page: int | None = None) -> tuple[str, int, int]:
    """(page text without furniture, start, end of the span in it). Furniture is removed only outside the span, so
    the span stays verbatim; raises ValueError when the span is not on the page."""
    text, s = norm(page_txt), norm(span)
    i = text.find(s)
    if i < 0:
        raise ValueError("span không có trong trang")
    pre, post = text[:i], text[i + len(s):]
    for pat in (STAMP, SIGN_BLOCK, EMAIL, WATERMARK):
        pre, post = _drop(pat, pre), _drop(pat, post)
    pre, post = _drop_signers(pre), _drop_signers(post)
    pre = _strip_head(re.sub(r" {2,}", " ", pre).lstrip(), s, page)
    post = re.sub(r" {2,}", " ", post).rstrip()
    m = TAIL_NUMBERS.search(s + post)                   # the numbers may follow the span's own final "."
    if m and m.start() >= len(s):
        post = post[:m.start() - len(s)]
    return pre + s + post, len(pre), len(pre) + len(s)


def oracle_passage(page_txt: str, span: str, min_words: int = 150, max_words: int = 300,
                   page: int | None = None) -> str:
    text, i, j = clean_page(page_txt, span, page)
    sents = _sentences(text)
    first = next(k for k, (a, b) in enumerate(sents) if b > i)
    last = next(k for k, (a, b) in enumerate(sents) if b >= j)
    lo, hi = first, last
    lo_min = 0 if _starts_sentence(text, sents[0][0]) else min(1, first)       # unfinished page start
    hi_max = len(sents) - 1
    if not TERMINAL.search(text[sents[-1][0]:sents[-1][1]]):                   # unfinished page end
        hi_max = max(last, hi_max - 1)

    def words(a, b):
        return len(text[sents[a][0]:sents[b][1]].split())

    while words(lo, hi) < min_words and (lo > lo_min or hi < hi_max):
        grow_hi = hi < hi_max and (lo == lo_min or (hi - last) <= (first - lo))
        cand = (lo, hi + 1) if grow_hi else (lo - 1, hi)
        if words(*cand) > max_words and words(lo, hi) >= min_words // 2:
            break
        lo, hi = cand
    return text[sents[lo][0]:sents[hi][1]].strip()


def atom_passage(atom: dict, root=None, min_words: int = 150, max_words: int = 300) -> str:
    page = int(atom["page"])
    return oracle_passage(page_text(pdf_path(atom["guideline"], root), page), atom["span"], min_words, max_words,
                          page)


RESIDUAL = re.compile(r"(?i:ký bởi|người ký)\s*:|(?i:thời gian ký|ngày ký|giờ ký)\s*:\s*\d|\S@\S|_" + DATE)


def residual_furniture(text: str) -> bool:
    """True when a passage still looks like it holds a signature block, a stamp or an e-mail (a shape the filters do
    not know): the A3 row then fails QC and the passage is checked by hand (privacy)."""
    return bool(RESIDUAL.search(text))


def passage_ocr(atom: dict, root=None) -> bool:
    """True when the atom's page text comes from the OCR sidecar (vnsoc.extract.verify_span.ocr_pages)."""
    pdf = pdf_path(atom["guideline"], root)
    return pdf.exists() and int(atom["page"]) in ocr_pages(pdf)
