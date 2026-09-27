# Workflow agent của dự án

Script điều phối nhiều agent (công cụ Workflow của Claude Code). Mỗi script bắt đầu bằng `export const meta`; tham số
`args` phải là GIÁ TRỊ JSON (mảng/đối tượng thật), không phải đường dẫn file.

| File | Việc | args |
|---|---|---|
| `main_atom_extraction.js` | T3.1–T3.2: trích mẩu theo phần trang → kiểm toán độc lập → sửa | nội dung `logs/wf/extract_args.json` |
| `foreign_store.js` | T2.6: thu thập giá trị nước ngoài theo nhóm bệnh → kiểm độc lập | nội dung `logs/wf/foreign_args.json` |
| `extract_plan.json` | kế hoạch chia phần trang cho 25 văn bản (bản đã chạy 27/9) | — |
| `foreign_groups.json` | 12 nhóm bệnh (id, mô tả, văn bản Bộ Y tế) — khớp `configs/foreign_groups.yaml` | — |
| `resume_args.py` | tính việc còn lại từ dữ liệu trên đĩa, ghi hai file args ở `logs/wf/` | — |
| `archive/` | workflow đã chạy xong (hiệu chỉnh trích mẩu, viết abstract FMC 250 từ) — lưu để tái lập | — |

Chạy tiếp sau khi đứt (hết giới hạn phiên, tắt máy): `$PY scripts/workflows/resume_args.py`, rồi gọi Workflow với
`scriptPath` và `args` như bảng trên. Phần trang đã có `atoms_parts/<phần>.jsonl` + `<phần>_coverage.md` đủ tới trang
cuối được bỏ qua; văn bản chưa có `review/extraction_audit/<doc>.json` được kiểm toán lại. Không sửa prompt của agent
trích mẩu mà không ghi `docs/DECISIONS.md` (giao thức trích là `configs/extraction_protocol.md`, được băm vào từng mẩu).
