# HG1.2 tự động: trọng tài chủ đề tbhiv (lao, HIV)

Ngày 26/9/2026. **Kiểm bởi AI (Claude), không phải người, không phải bác sĩ.** Kiểm toán viên A, B và trọng tài đều là AI.
Đầu vào: `tbhiv_A.json`, `tbhiv_B.json`. Kết quả máy đọc: `tbhiv_final.json`.

**Kết quả: 4 ok, 3 đã sửa (fix, không đổi giá trị), 0 loại, 0 chưa rõ.**

A và B chỉ khác nhau ở một chỗ: tiêu chí (c) của P-tbhiv-03 (A pass, B fail). Không có tiêu chí nào uncertain. Trọng tài đã tự mở lại các nguồn sau:
- 162/2024: lớp chữ tr. PDF 69, 70, 101 và ảnh tr. 69, 70;
- WHO 2026 Module 4 bản 2: tr. PDF 73 và 140;
- bản ghi IRIS 10665/387622;
- 162/2024 tr. 201 và 2760/2021 tr. 1, 37.

Không đọc `data/runs/`.

| Mẩu | a | b | c | d | A/B | Chốt | Thay đổi |
|---|---|---|---|---|---|---|---|
| P-tbhiv-01 | pass | pass | pass | pass | ok/ok | **fix** | `extraction.notes`: bằng chứng danh tính 2760/2021; căn cứ ngày WHO 2026 |
| P-tbhiv-02 | pass | pass | pass | pass | ok/ok | **fix** | `foreign[0].locator` WHO 2026: thêm ký hiệu phác đồ ở PDF tr. 73 |
| P-tbhiv-03 | pass | pass | **fail** | pass | ok/fix | **fix** | `moh_neighbour` +3 mục (suy thận, 2RHZ/4RH): tr. 69, 70, 101 |
| P-tbhiv-04 | pass | pass | pass | pass | ok/ok | **ok** | — |
| P-tbhiv-05 | pass | pass | pass | pass | ok/ok | **ok** | — (mồi TLE chờ quyết định A.7, không đổi dữ liệu) |
| P-tbhiv-06 | pass | pass | pass | pass | ok/ok | **ok** | — |
| P-tbhiv-07 | pass | pass | pass | pass | ok/ok | **ok** | — |

## Chỗ A và B khác nhau: P-tbhiv-03, tiêu chí (c)

162/2024 ghi phác đồ **2RHZ/4RH** (giai đoạn duy trì 4RH, nhãn HR) cho người lớn mắc lao có suy thận. Nhãn này trùng nhãn WHO/Mỹ. Trọng tài đã xem ở cả lớp chữ lẫn ảnh trang:
- tr. PDF 69 (in 68), mục 3.1.4: «Phác đồ 2RHZ/4RH có thể áp dụng điều trị lao cho người bệnh suy thận.»
- tr. PDF 70 (in 69), mục người bệnh lao tiểu đường có biến chứng suy thận: «Phác đồ 2RHZ/4RH có thể áp dụng cho bệnh nhân lao thường.»
- tr. PDF 101 (in 100), mục 5.3.4 c): «Phác đồ 2RHZ/4RH có thể áp dụng điều trị cho người bệnh lao có suy thận.»

Câu hỏi VI/EN không nêu chức năng thận, chức năng gan hay đái tháo đường. `moh_neighbour` chưa ghi các giá trị trên.

**Chốt (c) = fail, mẩu = fix, không phải error.**
- B đúng ở chỗ mẩu bỏ sót giá trị lân cận.
- A đúng ở chỗ giá trị 4RHE (A1, tr. 44) vẫn đúng cho quần thể của mẩu. Đây là một nhóm bệnh nhân khác, không phải giá trị sai.

**Đã sửa:** thêm 3 mục `moh_neighbour`. Span lấy nguyên văn từ lớp chữ, `span_on_page` = True.

**Ảnh hưởng tới phân tích:** không có. `neighbour_overlap` vốn đã True (do A2 trẻ em và mục HIV tr. 71). Vì vậy trạng thái (conflict), `status_with_neighbours` (indistinguishable) và N1 đều giữ nguyên.

Câu tr. 70 có thể đọc rộng là "mọi người bệnh lao". Nếu đọc như vậy thì đây là mâu thuẫn nội bộ thứ hai của 162/2024. Cách đọc này để **bác sĩ thật xem ở HG3.9**; AI không kết luận.

## Chi tiết các thay đổi (`data/interim/pilot/tbhiv.jsonl`)

Bản sao lưu nằm ở `scratchpad/audit/tbhiv_before.jsonl` (sha256 cb91a511…). Sau khi sửa, sha256 là 837f0fa1…. Script sửa đã kiểm các bất biến sau: span, trang, quần thể, cat_options, vn, giá trị nước ngoài, bản cũ, mồi, dung sai và trạng thái đều không đổi.

- **P-tbhiv-03.** Thêm `moh_neighbour` tr. 69, 70, 101 và ghi chú. Cũng ở tr. 69, mục viêm gan có "2 HRSE/6 RH". Giai đoạn duy trì ở đây kéo dài 6 tháng, không cùng khe 4 tháng, nên chỉ ghi chú. Không có 4RE, nên mồi RE vẫn sạch.
- **P-tbhiv-02.** Locator WHO 2026 thêm PDF tr. 73, nơi có ký hiệu 4–6 Bdq[6]-Lfx[Mfx]-Eto-E-Z-Hh-Cfz / 5 Lfx[Mfx]-Cfz-Z-E. Tr. 140 chỉ ghi thành phần bằng lời. Giá trị không đổi.
- **P-tbhiv-01.** Chỉ thêm ghi chú:
  - Bằng chứng gián tiếp rằng tài liệu này là QĐ 2760: 162/2024 tr. 201 dẫn "sơ đồ 3.1. 2 (QĐ 2760 của BYT)", và 2760/2021 tr. 37 có "Sơ đồ 3.1.2" cùng tên. Hiệu lực vẫn là suy luận.
  - Ngày WHO 2026 là 2026-09-21. B ghi "không kiểm được", nhưng bản đệm bản ghi IRIS 10665/387622 có `dc.date.issued` = 2026-09-21 và trỏ đúng tệp PDF đã băm. Vì vậy **không sửa** `version_date`.

## Đề xuất loại

Không có.

## Không sửa dữ liệu, chỉ ghi lại

- **Ký tự lạ trong 162/2024 (vấn đề hệ thống, việc của chủ mã).** Lớp chữ dùng 'ӟ' (U+04DF) thay 'ớ' và 'ү' (U+04AF) thay 'ẫ'. Hàm `verify_span.norm()` chưa quy đổi hai ký tự này, nên span và đoạn A3 mang ký tự lạ tới mô hình.
  - Cần thêm ánh xạ vào `_GLYPH`, kèm test.
  - Sau đó dựng lại đoạn A3 trước khi đóng băng.
- **P-tbhiv-05.** Mồi TLE trùng phương án thay thế của WHO 2014. Đây là quyết định HG1.2 mục A.7 (mặc định: đổi sang doravirine), không phải lỗi trích dẫn. A.7 không thuộc danh sách mặc định được giao áp dữ liệu ở lượt này, nên dữ liệu để nguyên.
- **Việc cho question-writer.** Làm trước khi đóng băng bộ câu hỏi v1 và không xem đầu ra mô hình:
  - P-tbhiv-03: thêm "chức năng thận và gan bình thường, không đái tháo đường".
  - P-tbhiv-01 (tùy chọn): thêm "không có chống chỉ định khác của BPaL" (tr. 54).
- **P-tbhiv-03, `population.hiv_pregnancy`.** Giữ nguyên. Trường này mô tả đúng phạm vi đoạn văn; câu hỏi hẹp hơn là không sai.

## Tự kiểm

- `vnsoc.schemas atom`: OK 7/7.
- `pilot_merge --only tbhiv --no-checklist`: giữ 7, loại 0, gồm 3 conflict, 1 indistinguishable, 3 concordant. Kết quả giống hệt lần chạy trước khi sửa.
