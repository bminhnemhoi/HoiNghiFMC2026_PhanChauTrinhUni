# HG1.2 — Kiểm toán tự động chủ đề controls: kết quả trọng tài

Kiểm bởi AI (Claude: hai kiểm toán viên độc lập A, B và một trọng tài), **không phải người, không phải bác sĩ**. Ngày 26/9/2026. Không đọc `data/runs/`.

**Tổng:** 3 ok · 4 fix · 2 error (cả hai đã sửa được bằng nguyên văn/nguồn đã mở) · 0 uncertain · 0 loại.

**Phát hiện chính:** QĐ 2131/QĐ-BYT ngày 14/7/2026 có thật và thay QĐ 2767/2023 (Điều 3). Trọng tài đã tải bản chính thức (trang Bệnh viện ĐK Bạc Liêu) vào `data/raw/2131_2026.pdf`, cập nhật manifest, rồi neo lại 4 mẩu COPD. Chỉ mẩu 03 đổi giá trị: 5–7 ngày → 5 ngày.

| Mẩu | A | B | Trọng tài (a/b/c/d · hiệu lực) | Kết luận | Thay đổi dữ liệu |
|---|---|---|---|---|---|
| P-controls-01 | ok | fix | pass/pass/pass/pass · fail | fix → fixed | neo lại 2131/2026 tr.14; < 70% giữ nguyên; 2767 vào superseded |
| P-controls-02 | ok | fix | pass/pass/pass/pass · fail | fix → fixed | neo lại 2131/2026 tr.26 (mục 2.5.2); ≤ 55 mmHg giữ nguyên |
| P-controls-03 | error | error | pass/fail/fail/pass · fail | error → fixed | **vn 5–7 → 5 ngày** (2131 tr.35); 2767 (5–7) vào superseded; 5904 tuyến xã (≤ 7) vào moh_neighbour; treo HG2.3 về 4562/2018 |
| P-controls-04 | fix | fix | pass/pass/pass/fail · fail | fix → fixed | neo lại 2131/2026 tr.25; ≥ 300 giữ nguyên; sửa locator GOLD (Figure 3.10 p.78); moh_neighbour ≥ 100 mới |
| P-controls-05 | ok | ok | pass/pass/pass/pass · pass | ok → none | — |
| P-controls-06 | ok | ok | pass/pass/pass/pass · pass | ok → none | — |
| P-controls-07 | ok | ok | pass/pass/pass/pass · pass | ok → none | — |
| P-controls-08 | fix | ok | pass/pass/pass/pass · pass | fix → fixed | thêm moh_neighbour 3610/2015 tr.133 (SAT 2000 đv); sửa locator CDC |
| P-controls-09 | ok | error | pass/pass/pass/fail · pass | error → fixed | foreign US ≥ 25 → ≥ 23 (USPSTF cho người gốc Á); xung đột với WHO ≥ 25 và mồi 21 giữ nguyên |

## Đề xuất ngoài tệp chủ đề (chưa làm, cần người điều phối)

- P-controls-03: loại các câu điều kiện A3 của mẩu này khỏi phân tích A3/H3 thí điểm — đoạn oracle P-controls-03#A3 lấy từ 2767/2023 tr.31 và chứa giá trị bản cũ 5–7 ngày; dựng lại đoạn từ 2131/2026 tr.35 trước khi đóng băng câu hỏi.
- P-controls-01/02/04: dựng lại đoạn A3 từ 2131/2026 trước khi đóng băng (giá trị không đổi nên không cần loại trong thí điểm; đoạn 04 còn câu ≥ 100 của bản cũ, đã được cờ neighbour).
- P-controls-09: sửa option_roles của 4 câu trắc nghiệm trong data/interim/pilot_questions.jsonl 'foreign:US+WHO_global' → 'foreign:WHO_global' (mẩu đã ở mục descriptive).
- HG2.3/T2.5: đưa 2131/2026 vào kho thay 2767/2023; quyết hiệu lực 4562/2018 (ảnh hưởng tín hiệu lệch phiên bản của P-controls-03).
- Chủ đề htn (ngoài phạm vi): P-htn-01 dùng 5904/2019 (tuyến xã) làm dr8_sources — đề cương chỉ gộp DR8 trong cùng tuyến; cùng giá trị nên không đổi kết quả, chỉ nên ghi lại là neighbour/supporting.

## Tự kiểm

- verify_span data/interim/pilot/controls.jsonl: 9/9 OK; pilot_merge --only controls --no-checklist: giữ 9, loại 0, {'concordant': 7, 'conflict': 2} như trước; tolerance/conflict_status/mồi không đổi ở cả 9 mẩu; schemas atom OK; atom_flags check: 6 vấn đề y hệt trước khi sửa (việc của lúc đóng băng/HG3.5)

Chi tiết từng mẩu (bằng chứng, trang, lý do): `review/pilot_audit/controls_final.json`. Bản sao trước khi sửa: scratchpad `audit/controls_before.jsonl`.
