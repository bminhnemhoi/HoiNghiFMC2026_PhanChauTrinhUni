"""Non-LLM cross-check of the pilot reference standard (review M1, R1.1).

The citation audit (state/gates/HG1.2_result.md) and the grading check were done by AI (Claude) because the author
works alone. This module adds a check that uses NO language model at all, so it is independent of the model that
extracted the atoms:
  (a) the verbatim span is found on the stated PDF page (text layer or verified OCR sidecar) — vnsoc.extract.verify_span;
  (b) every MoH value is parsed back from the span or a DR8 span by the deterministic grader parser;
  (d) every foreign value's numbers / drug names occur in the hashed cached source (vnsoc.extract.pilot_merge
      .source_warnings) and the source hash is not an anti-bot page.
Reports pass counts, the agreement with the AI audit verdicts (review/pilot_audit/*_final.json), and registers
pilot.indep_* keys. Criterion (c) (population/context) has no code equivalent and stays AI-only (stated).

  $PY -m vnsoc.analysis.independent_check
"""
from __future__ import annotations

import json
import sys

from vnsoc.numbers import put
from vnsoc.paths import paths

NOTE = "kiểm bằng mã, không dùng mô hình ngôn ngữ; tiêu chí quần thể (c) chỉ có kiểm bằng AI"


def check_atoms(atoms: list[dict], root=None) -> list[dict]:
    from vnsoc.extract.pilot_merge import source_warnings
    from vnsoc.extract.verify_span import drug_tables, verify_atom
    from vnsoc.match.sources import block_hashes

    syn, combos = drug_tables(root)
    blocks = block_hashes()
    out = []
    for a in atoms:
        v = verify_atom(a, root, syn, combos)
        warns = source_warnings(a, blocks, root)
        n_foreign = len(a.get("foreign") or [])
        bad_sources = {w.split(":")[0] for w in warns}
        out.append({"atom_id": a["atom_id"], "span_on_page": bool(v.get("span_on_page")),
                    "values_parsed": not v.get("missing_vn"), "ocr": bool(v.get("ocr")),
                    "foreign_records": n_foreign, "foreign_found": n_foreign - len(bad_sources),
                    "warnings": warns})
    return out


def main(argv=None) -> int:
    P = paths()
    atoms = [json.loads(x) for x in (P.root / "data" / "interim" / "pilot_atoms.jsonl").read_text(encoding="utf-8")
             .splitlines() if x.strip()]
    rows = check_atoms(atoms)
    audit = {}
    for f in sorted((P.root / "review" / "pilot_audit").glob("*_final.json")):
        for a in json.loads(f.read_text(encoding="utf-8"))["atoms"]:
            audit[a["atom_id"]] = a
    n = len(rows)
    span_ok = sum(r["span_on_page"] for r in rows)
    val_ok = sum(r["values_parsed"] for r in rows)
    fr = sum(r["foreign_records"] for r in rows)
    ff = sum(r["foreign_found"] for r in rows)
    agree_a = sum(1 for r in rows if r["atom_id"] in audit and
                  (audit[r["atom_id"]].get("a") == "pass") == r["span_on_page"])
    agree_b = sum(1 for r in rows if r["atom_id"] in audit and
                  (audit[r["atom_id"]].get("b") == "pass") == r["values_parsed"])
    for k, v in (("n", n), ("span_ok", span_ok), ("values_ok", val_ok), ("foreign_records", fr),
                 ("foreign_found", ff), ("agree_a", agree_a), ("agree_b", agree_b)):
        put(f"pilot.indep_{k}", v, str(v), NOTE)
    lines = ["# Kiểm chéo không dùng LLM cho chuẩn tham chiếu thí điểm (R1.1)", "", NOTE + ".", "",
             f"- Đoạn trích có trên đúng trang PDF: {span_ok}/{n}",
             f"- Giá trị Bộ Y tế đọc lại được từ nguyên văn (bộ đọc số của bộ chấm): {val_ok}/{n}",
             f"- Bản ghi nước ngoài có số/tên thuốc tìm thấy trong bản nguồn đã băm: {ff}/{fr}",
             f"- Khớp với kết luận kiểm toán AI: (a) {agree_a}/{n}, (b) {agree_b}/{n}", "",
             "## Cảnh báo theo mẩu (số không tìm thấy nguyên dạng trong nguồn có thể là giá trị quy đổi — xem kiểm toán AI)", ""]
    for r in rows:
        for w in r["warnings"]:
            lines.append(f"- {r['atom_id']}: {w}")
        if not r["span_on_page"] or not r["values_parsed"]:
            lines.append(f"- {r['atom_id']}: span_on_page={r['span_on_page']}, values_parsed={r['values_parsed']}")
    out = P.root / "review" / "pilot_audit" / "independent_code_check.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines[4:8]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
