# Kiểm toán HG1.2 tự động — chủ đề HBV (bản trọng tài)

**Người kiểm: AI (Claude) — kiểm toán viên A, B và trọng tài. Không phải người, không phải bác sĩ.** Ngày 26/9/2026.
Nguồn: `review/pilot_audit/hbv_A.json`, `hbv_B.json`. Kết quả máy đọc: `review/pilot_audit/hbv_final.json`.

**Tổng: 9 ok · 1 đã sửa (fix) · 0 loại · 0 chưa chắc.**

| Mẩu | a | b | c | d | Bất đồng A/B | Kết luận | Loại | Ghi chú |
|---|---|---|---|---|---|---|---|---|
| P-hbv-01 | pass | pass | pass | pass | — | ok | không | QĐ mặc định A.7 cho mồi 25 U/L (ở bước phân tích). |
| P-hbv-02 | pass | pass | pass | pass | — | ok | không |  |
| P-hbv-03 | pass | pass | pass | pass | — | ok | không | v1: thêm 'không mang thai' vào câu hỏi (không chặn). |
| P-hbv-04 | pass | pass | pass | pass | — | ok | không | QĐ mặc định A.8: giữ cách chấm. |
| P-hbv-05 | pass | pass | pass | pass | — | ok | không |  |
| P-hbv-06 | pass | pass | pass | pass | — | ok | không |  |
| P-hbv-07 | pass | pass | fail | pass | d | fix | không | Siết quần thể (HBsAg còn dương tính; không HBcrAg/≥ 2 logU/mL; không suy giảm miễn dịch). (d) trọng tài: pass (slide 33 + ACG EBGI 12/2025; toàn văn chưa đọc). |
| P-hbv-08 | pass | pass | pass | pass | — | ok | không | v1: thêm 'không mang thai' vào câu hỏi (không chặn). |
| P-hbv-09 | pass | pass | pass | pass | — | ok | không |  |
| P-hbv-10 | pass | pass | pass | pass | — | ok | không |  |

## Điểm trọng tài phải quyết

**P-hbv-07 (c)** — A và B cùng fail. Trọng tài đã xem ảnh 1740/2026 tr.PDF 24 và xác nhận lỗi. Danh sách "VÀ có một trong các tiêu chuẩn" còn hai lối ngừng thuốc không cần mốc 3–4 năm:
- mất HBsAg tại 2 thời điểm cách nhau 6 tháng;
- HBcrAg < 2 logU/mL kèm HBV DNA dưới ngưỡng.

Ngoài ra, người suy giảm miễn dịch không được khuyến cáo ngừng thuốc. Đã siết `population`; giá trị "ít nhất 3–4 năm" giữ nguyên.

**P-hbv-07 (d)** — A để uncertain, B cho pass. Trọng tài quyết **pass**:
- Slide 33 trong bản đệm (sha 763a79fe…) ghi "tối thiểu 2 năm" HBV DNA không phát hiện, HBsAg < 100 IU/mL. Giá trị, đơn vị và quần thể đều khớp.
- Bộ slide là tài liệu chính thức của AASLD (2025) và được trang IDSA của hướng dẫn liên kết tới.
- Nguồn thứ cấp độc lập ACG Evidence-Based GI (17/12/2025, đệm sha e6d56791…) quy đúng tiêu chí này cho hướng dẫn AASLD/IDSA 2025.
- Hạn chế còn lại: toàn văn Ghany 2025 chưa đọc được (journals.lww.com trả 402). Mục HG1.2 B vẫn mở.
- Xung đột vẫn mong manh: khuyến cáo chính của AASLD (Rec 5) là không ngừng thuốc cho tới khi mất HBsAg.

## Thay đổi dữ liệu
- `data/interim/pilot/hbv.jsonl`, P-hbv-07:
  - `population` thêm `hbsag_status`, `hbcrag`, `immune_status`;
  - thêm `extraction.audit_fix`, bổ sung `extraction.notes`.
- Không đổi giá trị nào (vn, foreign, superseded, decoy, moh_neighbour, tolerance, conflict_status).
- Tự kiểm bằng `pilot_merge --only hbv`: giữ 10, loại 0, trạng thái {indistinguishable 6, concordant 3, conflict 1}, giống trước khi sửa.

## Việc còn mở
- Bộ câu hỏi v1 (trước đóng băng):
  - P-hbv-07: thêm "HBsAg vẫn dương tính" và "không có kết quả HBcrAg (hoặc ≥ 2 logU/mL)";
  - P-hbv-03/08: thêm "không mang thai".
- Câu hỏi thí điểm đã chạy nên không sửa.
- Đối chiếu toàn văn Ghany 2025 khi truy cập được.
