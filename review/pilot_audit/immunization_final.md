# Kiểm toán HG1.2 tự động — chủ đề Tiêm chủng (bản trọng tài)

**Người kiểm: AI (Claude), gồm kiểm toán viên A, kiểm toán viên B và trọng tài. Không phải người, không phải bác sĩ.** Ngày 26/9/2026.

- Nguồn: `review/pilot_audit/immunization_A.json`, `immunization_B.json`.
- Kết quả máy đọc: `review/pilot_audit/immunization_final.json`.
- Không đọc `data/runs/`.

**Tổng: 1 ok · 2 đã sửa locator (không đổi giá trị) · 3 loại khỏi phân tích chính (giữ báo cáo mô tả) · 0 chưa chắc.**
Hai mẩu P-01 và P-04 vừa được sửa, vừa bị loại khỏi phân tích chính.

| Mẩu | a | b | c | d | Hiệu lực | A / B | Kết luận | Loại (phân tích chính) | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|
| P-immunization-01 | pass | pass | pass | pass | fail | ok / error | error (văn bản hết hiệu lực) | có, giữ mô tả | Sửa locator WHO PP 2017. |
| P-immunization-02 | pass | pass | pass | pass | fail | ok / error | error (văn bản hết hiệu lực) | có, giữ mô tả | — |
| P-immunization-03 | pass | pass | pass | pass | pass | ok / ok | ok | không | Thêm ghi chú pháp lý Mỹ. Kiểm lại sau 06/10 và trước 15/10. |
| P-immunization-04 | pass | pass | pass | pass | fail | fix / error | error (văn bản hết hiệu lực) | có, giữ mô tả | Bỏ footnote 4 khỏi locator UKHSA. |

A và B đồng ý ở cả 4 tiêu chí (a)–(d) của mọi mẩu. Bất đồng chỉ nằm ở phán quyết cuối và ở locator.

## Điểm trọng tài phải quyết

**1. Hiệu lực của TT 52/2025 (P-01, P-02, P-04).**
- Về sự kiện, A và B khớp nhau. A coi đây là cờ chờ người quyết; B coi là lỗi.
- Trọng tài đã tự xem ảnh TT 13/2026:
  - trang PDF 18, Điều 27 khoản 2 điểm d: «Thông tư số 52/2025/TT-BYT … hết hiệu lực» từ 01/7/2026;
  - trang PDF 3, Điều 5 khoản 4: «Lịch tiêm chủng … thực hiện theo hướng dẫn của nhà sản xuất, hướng dẫn chuyên môn của Cục Phòng bệnh».
- 3 lần tìm kiếm ngày 26/9/2026 không thấy văn bản lịch tiêm nào của Cục Phòng bệnh ban hành sau 01/7/2026.
- Kết luận: giá trị (9 tháng, 7 tuổi, 18 tháng) chép đúng, nhưng không xác minh được là chuẩn hiện hành.
- Áp mặc định **HG1.2 A.1(c)**: loại khỏi phân tích chính, giữ báo cáo mô tả.
  - Quyết định này đã có sẵn trong `data/interim/pilot_analysis_exclusions.yaml`, mục `descriptive`.
  - **Không** thêm vào `pilot_exclusions.yaml`, vì làm vậy sẽ xóa mẩu khỏi `pilot_atoms`.

**2. Locator UKHSA của P-04.**
- A cho rằng footnote 4 thuộc chương trình chọn lọc; B không nêu lỗi.
- Trọng tài mở bản đệm (sha 61db065b…): "[footnote 4]" chỉ xuất hiện một lần, ở dòng "Babies born to women with hepatitis B infection" của bảng chương trình chọn lọc.
- A đúng. Đã bỏ phần footnote 4 khỏi locator.
- Giá trị 18 tháng vẫn đúng theo hàng "Eighteen months old" (sinh từ 01/7/2024).

**3. Locator WHO PP 2017 của P-01.**
- Cả A và B đều nêu điểm này.
- Trang 1 của bản tóm tắt (sha 704cfe53…) đặt điều kiện cho mốc 9 tháng theo nguy cơ tử vong sởi ở nhũ nhi, không dùng cụm "ongoing transmission".
- Đã sửa locator và nhãn mô tả; giá trị 9 tháng giữ nguyên.
- Locator của Table 1 fn 9 đúng, nên giữ nguyên.

## Thay đổi dữ liệu (`data/interim/pilot/immunization.jsonl`)
- **P-01:** `foreign[WHO PP 2017].locator`, `values[0].text` (chỉ phần mô tả), `extraction.audit_fix`.
- **P-04:** `foreign[EU_UK].locator`, `extraction.audit_fix`.
- **P-03:** thêm `extraction.notes`, dẫn nguồn thứ cấp đã băm (Medical Daily 15/9/2026, sha 3d3987fc…). Nội dung:
  - lệnh ngày 16/3/2026 vẫn chặn lịch CDC 1/2026, kể cả phiếu ACIP 12/2025 về liều sơ sinh viêm gan B;
  - Tòa Khu vực 1 nghe tranh luận ngày 06/10/2026.
- **P-02:** không đổi.
- **Không đổi giá trị nào:** vn, giá trị nước ngoài, mẩu lân cận, mồi, dung sai, conflict_status, span, trang, quần thể.
- Sao lưu trước khi sửa: `scratchpad/audit/immunization_before.jsonl` (sha256 bc49005b…).
- Tự kiểm bằng `pilot_merge --only immunization`:
  - giữ 4, loại 0, trạng thái {conflict 2, concordant 2}, giống hệt trước khi sửa;
  - schema OK 4/4; verify_span OK 4/4.

## Việc còn mở
- **P-03:** bắt buộc kiểm lại lịch CDC sau phiên tòa 06/10/2026 và trước 15/10/2026. Nếu lịch 1/2026 được khôi phục, trạng thái concordant có thể đổi.
- **P-01/-02/-04:** chuyển sang A.1(a) nếu tìm được hướng dẫn lịch TCMR hiện hành của Cục Phòng bệnh trước 15/10/2026.
- **Mã:** hàm `checklist()` trong `pilot_merge.py` không in `valid_to`, `hg_block` và `moh_neighbour`, nên người đọc checklist không thấy việc TT 52/2025 đã hết hiệu lực. Chủ mã nên sửa.
