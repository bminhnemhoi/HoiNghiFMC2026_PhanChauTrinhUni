"""Human sample check by the co-authors: one self-contained HTML file (opens offline on a phone or laptop, nothing to
install) showing, for each selected atom, the image of the official PDF page with the quoted span highlighted, the
values and population the atom claims, and three questions — (a) is the quote on this page, (b) are the value and
unit right, (c) is the population right. Answers stay in the browser and are downloaded as one JSON file that the
reviewer sends back; `import` turns it into a CSV and reports agreement with the AI audit.

  $PY -m vnsoc.review_pack build --atoms data/interim/pilot_atoms.jsonl --status conflict \
      --out review/human_check/pilot_conflicts.html --title "Kiểm mẩu xung đột (thí điểm)"
  $PY -m vnsoc.review_pack import review/human_check/<reviewer>.json --audit review/pilot_audit
Reviewers are people (co-authors); their role is stated as it is (students of medicine/dentistry), never "clinician".
"""
from __future__ import annotations

import argparse
import base64
import csv
import html
import json
import sys
from pathlib import Path

from vnsoc.extract.verify_span import pdf_path

QUESTIONS = [("a", "Đoạn trích (tô vàng) có đúng trên trang này không?"),
             ("b", "Giá trị và đơn vị Bộ Y tế ghi dưới đây có đúng như văn bản không?"),
             ("c", "Quần thể/bối cảnh ghi dưới đây có đúng phạm vi của đoạn văn không?")]
CHOICES = [("dung", "Đúng"), ("sai", "Sai"), ("khong_ro", "Không chắc")]


def page_image(atom: dict, root=None, zoom: float = 1.6, quality: int = 70) -> tuple[str, bool]:
    """(JPEG base64 of the atom's PDF page, span highlighted?) — scanned pages have no text layer to highlight."""
    import pymupdf

    doc = pymupdf.open(pdf_path(atom["guideline"], root))
    page = doc[int(atom["page"]) - 1]
    words = (atom.get("span") or "").split()
    rects = []
    for i in range(0, max(len(words) - 2, 1), 4):          # overlapping 6-word windows cover the whole span
        probe = " ".join(words[i:i + 6])
        rects += page.search_for(probe) if probe else []
    for r in rects:
        a = page.add_highlight_annot(r)
        a.set_colors(stroke=(1, 0.85, 0))
        a.update()
    pix = page.get_pixmap(matrix=pymupdf.Matrix(zoom, zoom), annots=True)
    data = pix.tobytes("jpeg", jpg_quality=quality)
    doc.close()
    return base64.b64encode(data).decode("ascii"), bool(rects)


def _vals(items) -> str:
    return "; ".join(str(it.get("text") or {k: v for k, v in it.items() if v is not None}) for it in items or [])


def card(atom: dict, i: int, img_b64: str, found: bool = True) -> str:
    e = html.escape
    pop = "".join(f"<li><b>{e(str(k))}</b>: {e(str(v))}</li>" for k, v in (atom.get("population") or {}).items())
    qs = ""
    for q, text in QUESTIONS:
        opts = "".join(f'<label><input type="radio" name="{e(atom["atom_id"])}|{q}" value="{v}"> {lab}</label>'
                       for v, lab in CHOICES)
        qs += f'<fieldset><legend>({q}) {e(text)}</legend>{opts}</fieldset>'
    return f"""<section class="card" id="c{i}">
<h2>{i}. {e(atom.get('disease') or '')} — {e(atom.get('intervention') or '')}</h2>
<p class="meta">Mã {e(atom['atom_id'])} · Văn bản {e(atom['guideline'])} · <b>trang PDF {e(str(atom['page']))}</b> · mục {e(atom.get('section') or '')}</p>
<p><b>Đoạn trích:</b> «{e(atom.get('span') or '')}»</p>
<p><b>Giá trị Bộ Y tế (theo mẩu):</b> {e(_vals(atom.get('vn')))}</p>
<p><b>Quần thể:</b></p><ul>{pop}</ul>
<details open><summary>{"Ảnh trang PDF (đoạn trích được tô vàng)" if found else "Ảnh trang PDF — trang scan, không tô được: tự tìm đoạn trích trên ảnh và so từng con số"}</summary>
<img alt="trang {e(str(atom['page']))}" src="data:image/jpeg;base64,{img_b64}"></details>
{qs}
<textarea name="{e(atom['atom_id'])}|note" placeholder="Ghi chú (nếu Sai/Không chắc: sai ở đâu?)"></textarea>
</section>"""


PAGE = """<!doctype html><html lang="vi"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>{title}</title>
<style>
:root {{ --bg:#fafaf7; --fg:#1d1d1b; --muted:#5d5d58; --card:#fff; --line:#dedcd4; --accent:#1f5f8b; }}
@media (prefers-color-scheme: dark) {{ :root {{ --bg:#161614; --fg:#ecebe6; --muted:#a8a69d; --card:#20201d; --line:#3a3934; --accent:#7fb6dd; }} }}
body {{ margin:0; background:var(--bg); color:var(--fg); font:16px/1.5 system-ui, sans-serif; }}
main {{ max-width:900px; margin:0 auto; padding:16px; }}
.card {{ background:var(--card); border:1px solid var(--line); border-radius:10px; padding:16px; margin:16px 0; }}
.meta {{ color:var(--muted); font-size:14px; }} img {{ width:100%; height:auto; border:1px solid var(--line); margin:8px 0; }}
fieldset {{ border:1px solid var(--line); border-radius:8px; margin:8px 0; }} label {{ margin-right:16px; display:inline-block; padding:4px 0; }}
textarea {{ width:100%; min-height:48px; box-sizing:border-box; }}
.bar {{ position:sticky; top:0; background:var(--bg); padding:8px 0; border-bottom:1px solid var(--line); z-index:2; }}
button {{ background:var(--accent); color:#fff; border:0; border-radius:8px; padding:10px 16px; font-size:16px; }}
input[type=text] {{ font-size:16px; padding:6px; width:min(320px,100%); }}
</style></head><body><main>
<h1>{title}</h1>
<p>{n} khuyến cáo. Với mỗi khuyến cáo: nhìn ảnh trang PDF, trả lời 3 câu (a)(b)(c). Không cần tra nguồn nước ngoài.
Trả lời được lưu trong trình duyệt của bạn; làm xong bấm <b>Tải kết quả</b> và gửi file .json cho Minh.</p>
<div class="bar"><label>Tên người kiểm: <input type="text" id="reviewer" placeholder="ví dụ: Thong"></label>
<button onclick="save()">Tải kết quả</button> <span id="done"></span></div>
{cards}
<p><button onclick="save()">Tải kết quả</button></p>
</main><script>
const KEY = "vnsoc-review-{slug}";
function collect() {{
  const out = {{}};
  document.querySelectorAll("input[type=radio]:checked, textarea").forEach(el => {{
    if (el.type === "radio" || el.value.trim()) out[el.name] = el.value; }});
  return out; }}
function progress() {{
  const a = collect(); const n = Object.keys(a).filter(k => !k.endsWith("|note")).length;
  document.getElementById("done").textContent = n + " / {nq} câu đã trả lời";
  try {{ localStorage.setItem(KEY, JSON.stringify({{answers: a, reviewer: document.getElementById("reviewer").value}})); }} catch (e) {{}} }}
function restore() {{
  let s = null; try {{ s = JSON.parse(localStorage.getItem(KEY) || "null"); }} catch (e) {{}}
  if (!s) return; document.getElementById("reviewer").value = s.reviewer || "";
  for (const [k, v] of Object.entries(s.answers || {{}})) {{
    const r = document.querySelector(`input[type=radio][name="${{CSS.escape(k)}}"][value="${{CSS.escape(v)}}"]`);
    if (r) r.checked = true; const t = document.querySelector(`textarea[name="${{CSS.escape(k)}}"]`); if (t) t.value = v; }} }}
function save() {{
  const who = document.getElementById("reviewer").value.trim() || "nguoi_kiem";
  const blob = new Blob([JSON.stringify({{pack: "{slug}", reviewer: who, saved_at: new Date().toISOString(), answers: collect()}}, null, 1)],
                        {{type: "application/json"}});
  const a = document.createElement("a"); a.href = URL.createObjectURL(blob);
  a.download = "{slug}_" + who.replace(/[^A-Za-z0-9_-]/g, "_") + ".json"; a.click(); }}
document.addEventListener("change", progress); document.addEventListener("input", progress);
restore(); progress();
</script></body></html>"""


def build(atoms: list[dict], out: Path, title: str, root=None) -> Path:
    cards = "\n".join(card(a, i, *page_image(a, root)) for i, a in enumerate(atoms, 1))
    slug = out.stem
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(PAGE.format(title=html.escape(title), n=len(atoms), cards=cards, slug=slug,
                               nq=len(atoms) * len(QUESTIONS)), encoding="utf-8")
    return out


def import_answers(path: Path, audit_dir: Path | None = None) -> dict:
    """reviewer JSON -> rows {atom_id, a, b, c, note} (+ AI audit verdicts when available) and agreement counts."""
    d = json.loads(path.read_text(encoding="utf-8"))
    rows: dict[str, dict] = {}
    for k, v in d["answers"].items():
        aid, q = k.rsplit("|", 1)
        rows.setdefault(aid, {"atom_id": aid})[q] = v
    ai = {}
    if audit_dir and audit_dir.exists():
        for f in audit_dir.glob("*_final.json"):
            for a in json.loads(f.read_text(encoding="utf-8"))["atoms"]:
                ai[a["atom_id"]] = a
    agree = total = 0
    for r in rows.values():
        a = ai.get(r["atom_id"])
        for q in ("a", "b", "c"):
            if a and r.get(q) in ("dung", "sai") and a.get(q) in ("pass", "fail"):
                r[f"ai_{q}"] = a[q]
                total += 1
                agree += (r[q] == "dung") == (a[q] == "pass")
    return {"reviewer": d.get("reviewer"), "rows": list(rows.values()), "agree": agree, "compared": total}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="python -m vnsoc.review_pack")
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build")
    b.add_argument("--atoms", required=True)
    b.add_argument("--status", nargs="*", help="chỉ lấy mẩu có conflict_status này")
    b.add_argument("--ids", nargs="*", help="chỉ lấy các atom_id này")
    b.add_argument("--out", required=True)
    b.add_argument("--title", default="Kiểm trích dẫn khuyến cáo")
    m = sub.add_parser("import")
    m.add_argument("json")
    m.add_argument("--audit", help="thư mục kết quả kiểm toán AI (*_final.json) để tính đồng thuận")
    a = ap.parse_args(argv)
    if a.cmd == "build":
        atoms = [json.loads(x) for x in Path(a.atoms).read_text(encoding="utf-8").splitlines() if x.strip()]
        atoms = [x for x in atoms if (not a.status or x.get("conflict_status") in a.status)
                 and (not a.ids or x["atom_id"] in a.ids)]
        out = build(atoms, Path(a.out), a.title)
        print(f"{len(atoms)} mẩu -> {out} ({out.stat().st_size // 1024} KB)")
        return 0
    r = import_answers(Path(a.json), Path(a.audit) if a.audit else None)
    dst = Path(a.json).with_suffix(".csv")
    cols = ["atom_id", "a", "b", "c", "note", "ai_a", "ai_b", "ai_c"]
    with open(dst, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, restval="", extrasaction="ignore")
        w.writeheader()
        w.writerows(r["rows"])
    print(f"{r['reviewer']}: {len(r['rows'])} mẩu -> {dst}; đồng thuận người–AI {r['agree']}/{r['compared']} tiêu chí")
    return 0


if __name__ == "__main__":
    sys.exit(main())
