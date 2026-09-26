# HG1.2 — Kiểm toán tự động chủ đề malaria_ocr: phán quyết cuối (trọng tài)

Ngày 26/9/2026. **Kiểm bởi AI (Claude), không phải người, không phải bác sĩ.** Đầu vào: `malaria_ocr_A.json`, `malaria_ocr_B.json`, `state/gates/HG1.2_decisions.md` mục A.
Không đọc `data/runs/`. Với nguồn nước ngoài, chỉ ghi giá trị và vị trí.

**Kết quả: 3 ok · 5 đã sửa (02 và 07 là lỗi giá trị/nguồn, 01 đổi theo quyết định mặc định A.2, 04 và 05 chỉ sửa vị trí) · 0 loại · 0 chưa rõ.**

| Mẩu | a | b | c | d | Cuối | A≠B ở | Trường đã sửa |
|---|---|---|---|---|---|---|---|
| P-malaria_ocr-01 | pass | pass | pass | pass | **sửa** | c | vn (bỏ 3 mục DR8 từ 315/2015: chloroquine, quinine, sulfadoxine-pyrimethamine); extraction.decision_default (mới, A.2); extraction.dr8_sources[0].merged_into_vn; extraction.dr8_sources[1].merged_into_vn; extraction.notes (thêm); extraction.audit_fix (mới) |
| P-malaria_ocr-02 | pass | pass | pass | fail | **lỗi → đã sửa** | cd | foreign[US/CDC].values (bỏ 'B. atovaquon–proguanil'); foreign[US/CDC].locator; extraction.removed_foreign_values (mới); extraction.notes (thêm); extraction.audit_fix (mới) |
| P-malaria_ocr-03 | pass | pass | pass | pass | **ok** | — | — |
| P-malaria_ocr-04 | pass | pass | pass | pass | **sửa** | — | foreign[WHO 2026].locator; foreign[WHO 2026].values[0,5].text; extraction.notes (thêm); extraction.audit_fix (mới) |
| P-malaria_ocr-05 | pass | pass | pass | pass | **sửa** | — | foreign[WHO 2026].locator; foreign[WHO 2026].values[7 ngày].text; extraction.notes (thêm); extraction.audit_fix (mới) |
| P-malaria_ocr-06 | pass | pass | pass | pass | **ok** | — | — |
| P-malaria_ocr-07 | pass | pass | fail | pass | **lỗi → đã sửa** | — | vn (+2,4 mg/kg, 3377/2023 Phụ lục I Bảng 1 tr. PDF 15); extraction.dr8_sources (+1 nguồn cùng văn bản 3377/2023 tr.15, kèm image_text/ocr_note); extraction.dr8_sources[0].merged_into_vn (3312/2015, A.3); extraction.decision_default (mới, A.3); decoy ([3,6] → []); extraction.decoy_rule; extraction.notes (thêm); extraction.audit_fix (mới); conflict_status (tính lại bởi pilot_merge: conflict → concordant) |
| P-malaria_ocr-08 | pass | pass | pass | pass | **ok** | — | — |

## Quyết định chính

- **P-malaria_ocr-07 (mẩu xung đột → concordant).** Phụ lục I, Bảng 1 của chính 3377/2023 (tr. PDF 15, trọng tài đã xem ảnh) ghi «Giờ đầu tiêm 2,4 mg/kg, tiêm nhắc lại 2,4 mg/kg vào giờ thứ 12» và không có ngoại lệ cho trẻ < 20 kg. Trong khi đó tr.11 ghi 3 mg/kg/lần cho trẻ < 20 kg. Trọng tài hợp hai giá trị theo §1.2/DR8 (đã đăng ký trước), cùng tiền lệ TT51 ở phản vệ: vn = {3; 2,4}. Vì vậy mẩu **rời tập H1**, gắn `[concordant_by_union]`. Cách đọc "quy định riêng thắng" (vn = {3}, conflict) chỉ dùng cho độ nhạy khám phá. Mặc định A.3 được áp: không hợp 1,5 mg/kg/ngày. Mồi 3,6 bị bỏ theo quy tắc.
- **P-malaria_ocr-01.** Mặc định A.2 được áp (315/2015 không áp): vn = {quinin + clindamycin}. Mẩu vẫn conflict. Mâu thuẫn với 315/2015 vẫn được đếm là kết quả phụ DR8.
- **P-malaria_ocr-02.** Bỏ atovaquon–proguanil khỏi bản ghi CDC: thuốc này không phải ACT, mà câu hỏi chỉ hỏi ACT (CDC Table 1 p.1: A = AL, B = AP). Mẩu vẫn indistinguishable.
- **Quy tắc phạm vi 3312/2015** (hướng dẫn nhi): không áp cho quần thể người lớn. Dòng "Người lớn > 15 tuổi" (tr.521) là mốc liều dưới câu "trẻ em không dùng vượt quá liều người lớn". Quy tắc này áp nhất quán cho 01–07 và không đổi giá trị nào.
- **P-malaria_ocr-04/05.** WHO 2026 p.20 (khuyến cáo xét nghiệm G6PD 2024) cho phép 0,5 mg/kg/ngày × 7 ngày với người không thiếu G6PD. Locator cũ ghi "chỉ gợi ý cho Ấn Độ/châu Mỹ" là không đầy đủ, nay đã sửa. Xung đột của 04 với WHO chỉ nằm ở phương án 1 mg/kg/ngày.

## Tự kiểm
- `verify_span`: 8/8 OK. Schema: 8 dòng hợp lệ.
- `pilot_merge --only malaria_ocr`: giữ 8, loại 0. Trước sửa: conflict 5, indistinguishable 2, concordant 1. Sau sửa: conflict 4, indistinguishable 2, concordant 2 (chỉ 07 đổi, có chủ đích).
- Sao lưu: `C:/Users/Admin/AppData/Local/Temp/claude/d--phan-chau-trinh---y-khoa/1e1ea5eb-0832-473b-882a-b9921c8f5c59/scratchpad/audit/malaria_ocr_before.jsonl`. Script sửa (idempotent): `C:/Users/Admin/AppData/Local/Temp/claude/d--phan-chau-trinh---y-khoa/1e1ea5eb-0832-473b-882a-b9921c8f5c59/scratchpad/audit/malaria_ocr_fix.py`.

## Còn việc (ngoài tệp mẩu)
- Ghi `docs/DECISIONS.md`: áp A.2, A.3; quy tắc phạm vi 3312/2015; hợp nội bộ ở 07 kèm độ nhạy; bỏ AP ở 02.
- Chạy lại `pilot_merge` đầy đủ để cập nhật `pilot_atoms.jsonl` và checklist.
- Bộ câu hỏi v1 (dựng bằng qgen): trắc nghiệm 07 hết đủ điều kiện; trắc nghiệm 01 có thể đủ điều kiện.
- Lượt thí điểm đã chạy khi 07 còn là conflict và 01 còn 4 mục vn. Phải ghi đây là hạn chế khi báo cáo thí điểm.
