# T2.1–T2.2 · Cụm c4_resp_circulars (hô hấp + thông tư) — ghi chú của corpus-librarian

Ngày: 2026-09-26 · File dữ liệu: `data/interim/manifest_parts/c4_resp_circulars.jsonl` (12 dòng; `vnsoc.schemas manifest` → OK 12 dòng; sha256 của cả 9 dòng có file đều khớp file trong `data/raw/`).

## 1. Tóm tắt

- **Viêm phổi cộng đồng 2147/2026 đã có trên kcb.vn** (mục tin-tuc, đăng 23/07/2026), có lớp chữ, 93 trang. Điều 3 (trang PDF 1) thay thế 4815/2020. Đề cương §3.1 ghi "chưa thấy trên kcb.vn". Ghi chú này đã cũ.
- **COPD 2131/2026: không tìm thấy** văn bản ở bất kỳ nguồn chính thức nào tôi truy cập được. Tôi chưa chứng minh được văn bản này tồn tại. Hiện COPD chỉ có bản 2767/2023 (kcb.vn, có lớp chữ).
- **Chuỗi COPD bất thường (trái kỳ vọng):** kcb.vn đăng file dưới nhãn "3874/QĐ-BYT ngày 26/06/2018", nhưng trang PDF 4 của file là **QĐ 4562/QĐ-BYT ngày 19/7/2018**. QĐ 4562 thay thế 3874/2018 và 2866/2015. 2767/2023 lại chỉ nói thay 3874/2018, không nhắc 4562/2018. Theo quy tắc "chỉ tin điều khoản tường minh", 4562/2018 chưa bị văn bản nào thay. Ngoài ra, `data/raw/3874_2018.pdf` (một agent khác tải) thực chất là 4562/2018, tức đặt sai khóa.
- **Hen phế quản:** hướng dẫn hiện hành trên kcb.vn là **1851/2020** (người lớn và trẻ ≥ 12 tuổi). Văn bản này bãi bỏ 4776/2009 và 2 bài hen trong 3942/2014. Trên kcb.vn không có hướng dẫn hen riêng cho trẻ < 12 tuổi. Chỉ có bài "Hen phế quản trẻ em" trong **3312/2015** (Bệnh thường gặp ở trẻ em).
- **Tiêm chủng:** TT10/2024 **đã hết hiệu lực** từ 15/02/2026 (bị TT52/2025 thay). TT52/2025 cũng hết hiệu lực từ 01/7/2026 (bị TT13/2026 bãi bỏ). TT13/2026 **không chứa bảng lịch tiêm**, mà giao lịch cho "hướng dẫn chuyên môn của Cục Phòng bệnh". Văn bản đó chưa tìm thấy. Tôi đã tự kiểm lại chuỗi này bằng ảnh và lớp chữ trang, và kết quả khớp phát hiện của thí điểm tiêm chủng.
- **Phản vệ TT51/2017:** bản chính thức duy nhất (kcb.vn) là bản quét, nên không kiểm span được khi chưa có OCR. Chưa thấy văn bản sửa đổi hay thay thế nào.

## 2. Bảng văn bản

| Khóa | Tiêu đề ngắn | Host | text_kind | Trang | Hiệu lực (theo điều khoản đã đọc) |
|---|---|---|---|---|---|
| 2147/2026 | Viêm phổi mắc phải cộng đồng người lớn | kcb.vn | ok | 93 | **current**. Ký 15/07/2026, hiệu lực từ ngày ký. Thay 4815/2020 (Điều 3, tr. 1) |
| 4815/2020 | Viêm phổi mắc phải cộng đồng người lớn (bản cũ) | — | — | — | superseded bởi 2147/2026. **Không có PDF chính thức** |
| 2131/2026 | COPD (theo đề cương) | — | — | — | **Chưa xác minh.** Không tìm thấy văn bản. `status` chỉ là giá trị giữ chỗ |
| 2767/2023 | COPD | kcb.vn | ok | 87 (đề cương ghi 81) | current. Ký 04/07/2023. Thay 3874/2018 (Điều 3, tr. 1) |
| 4562/2018 | COPD, bản cập nhật 2018 (**mới phát hiện**) | kcb.vn | ok | 86 | **Hiệu lực chưa xác nhận.** Ký 19/7/2018, thay 3874/2018 và 2866/2015 (Điều 3, tr. PDF 4). Không văn bản nào nêu tên để thay nó |
| 3874/2018 | COPD 2018 (bản 26/6/2018) | — | — | — | superseded bởi 4562/2018 và 2767/2023. **Không có PDF gốc.** File kcb.vn gắn nhãn 3874 thực chất là 4562 |
| 1851/2020 | Hen phế quản người lớn và trẻ ≥ 12 tuổi | kcb.vn | ok (glyph ƣ ở 19/48 trang, mất dấu "≥") | 48 | current. Ký 24/4/2020. Bãi bỏ 4776/2009 và 2 bài hen của 3942/2014 (Điều 3, tr. 1) |
| 3312/2015 | Bệnh thường gặp ở trẻ em (có bài hen trẻ em, tr. 685 và 694) | kcb.vn (.rar) | ok (glyph ƣ) | 807 | current, ký 07/8/2015. Không có điều khoản thay thế. Hiệu lực từng chương chưa xác nhận |
| TT51/2017 | Phòng, chẩn đoán và xử trí phản vệ | kcb.vn | **scanned_or_empty** | 20 | current. Ký 29/12/2017, hiệu lực 15/02/2018. Thay TT08/1999 (Điều 7, tr. 3) |
| TT10/2024 | Danh mục bệnh, đối tượng, phạm vi vắc xin bắt buộc (lịch TCMR) | datafiles.chinhphu.vn | **scanned_or_empty** | 5 | **superseded** từ 15/02/2026 bởi TT52/2025. Ký 13/6/2024, hiệu lực 01/8/2024. Thay TT38/2017 (Điều 4, tr. 4) |
| TT52/2025 | Như TT10/2024 (bản 2025) (**mới phát hiện**) | cmsapi.tiemchungmorong.vn | ok | 10 | **superseded** từ 01/7/2026 bởi TT13/2026. Ký 31/12/2025, hiệu lực 15/02/2026. Thay TT10/2024 (Điều 4, tr. 9) |
| TT13/2026 | Quy định về hoạt động tiêm chủng (**mới phát hiện**) | bcp.cdnchinhphu.vn | **scanned_or_empty** | 19 | current. Ký 16/5/2026, hiệu lực 01/7/2026. Bãi bỏ TT52/2025, TT24/2018, TT34/2018, TT05/2020 (Điều 27, tr. 18). **Không có lịch tiêm** (Điều 5 khoản 4, tr. 3) |

Số trang ở cột cuối là số trang PDF (đếm từ 1). Ở các văn bản ký số của kcb.vn (2147/2026, 2767/2023), lớp chữ để trống số và ngày. Danh tính được xác nhận bằng tiêu đề, dấu ký số in trên trang và trang danh mục kcb.vn.

## 3. Không tìm được bản chính thức và nơi đã tìm

| Khóa | Nơi đã tìm (đều không có) |
|---|---|
| 2131/2026 | Ô tìm kiếm nội bộ kcb.vn (`/page/search?keyword=`: "2131", "2131/QĐ-BYT", "phổi tắc nghẽn", "COPD"). Trang thẻ kcb.vn "Quyết định số 2131/QĐ-BYT" (rỗng). Danh mục kcb.vn/phac-do và /tai-lieu. vilaphoikhoe.kcb.vn (`?s=2131`). vanban.chinhphu.vn ("phổi tắc nghẽn"). moh.gov.vn (cổng chỉ trả khung JS, không tìm kiếm được). Tìm chuỗi "2131" trong 2147/2026, 1740/2026, 2767/2023 |
| 4815/2020 | kcb.vn nội bộ ("4815", "viêm phổi", "viêm phổi mắc phải cộng đồng", "mắc phải cộng đồng"). vilaphoikhoe.kcb.vn (`?s=4815`). vanban.chinhphu.vn ("viêm phổi"). moh.gov.vn (như trên) |
| 3874/2018 (bản gốc) | kcb.vn chỉ có file sách 2018, bên trong là QĐ 4562/2018. Tìm "4562" trên kcb.vn: không có trang riêng |
| TT51/2017 bản có lớp chữ | kcb.vn (2 link, cùng một file quét). vanban.chinhphu.vn ("phản vệ", "xử trí phản vệ", "51/2017/TT-BYT"). Danh mục Bộ Y tế trên congbao.chinhphu.vn (quét 47 trang, 639 mục; danh mục không đầy đủ, không có TT51/2017, TT10/2024, TT52/2025, TT13/2026). vbpl.vn chặn bot (JS) |

Giới hạn công cụ: **hạn mức WebSearch của phiên đã hết (200/200)** ngay từ lần tìm đầu, nên tôi không dùng được máy tìm kiếm chung. Tôi chỉ dùng ô tìm kiếm và danh mục của chính các trang chính thức. Vì vậy, trang Sở Y tế và bệnh viện đăng lại quyết định **chưa được tìm có hệ thống**. Không truy cập trang thư viện pháp luật tư nhân.

## 4. Văn bản mới phát hiện

1. **TT52/2025/TT-BYT** (31/12/2025). Thay TT10/2024, rồi bị TT13/2026 bãi bỏ. Thí điểm tiêm chủng tìm ra trước, tôi kiểm lại.
2. **TT13/2026/TT-BYT** (16/5/2026). Văn bản tiêm chủng hiện hành, không có bảng lịch tiêm.
3. **QĐ 4562/QĐ-BYT** (19/7/2018). Bản COPD thật sự có hiệu lực trước 2767/2023. Bị kcb.vn gắn nhầm nhãn 3874.
4. **QĐ 3312/QĐ-BYT** (07/8/2015). Nguồn Bộ Y tế duy nhất trên kcb.vn cho hen trẻ < 12 tuổi.
5. **TT 47/2025/TT-BYT** (30/12/2025, Công báo số 54, hiệu lực 15/02/2026) bãi bỏ một loạt văn bản quy phạm pháp luật của Bộ Y tế. Tôi đọc bản PDF Công báo trong scratchpad: danh sách bãi bỏ **không có** TT51/2017 hay TT10/2024. Văn bản này không liên quan trực tiếp nên tôi không ghi dòng.

Các văn bản được nêu tên nhưng không ghi dòng: 4776/2009 và 3942/2014 (hen), 2866/2015 (COPD), TT08/1999, TT38/2017, TT24/2018, TT34/2018, TT05/2020. Chúng chỉ nằm trong `supersedes`. **Dòng 3942/2014** (một agent khác đã tải `data/raw/3942_2014.pdf`) phải có `partially_amended_by: ["1851/2020"]` và `status: "partial"`, theo 1851/2020 Điều 3, trang PDF 1.

## 5. Hệ quả cho bảng hạt giống và thiết kế

- Hạt giống dòng 23–24 (sởi 9 tháng, DTP) đang trỏ **TT10/2024, văn bản đã hết hiệu lực**. Văn bản cuối cùng có bảng lịch là TT52/2025, cũng đã hết hiệu lực từ 01/7/2026. Tại ngày đóng băng 15/10/2026, chưa có văn bản pháp quy nào chứa lịch TCMR mà tôi kiểm được. Các span chỉ kiểm được ở TT52/2025 (có lớp chữ).
- COPD: nếu coi 4562/2018 là "hiện hành" (theo quy tắc điều khoản tường minh), thì theo DR8 (§1.2) một câu trả lời đúng theo bản 2018 cũng bị tính là đúng. Cần người quyết định trước khi tạo mẩu COPD và trước phân tích phiên bản.
- Phản vệ (hạt giống dòng 14–15) và lịch tiêm (TT13/2026) chỉ có bản quét. Không tạo mẩu được cho tới khi có OCR (tối đa 10 văn bản OCR theo §3.1) hoặc tìm được bản có lớp chữ.
- 1851/2020: lớp chữ mất dấu "≥" và rơi vài chữ hoa. Khi trích mẩu có ngưỡng (ví dụ ≥, ≤), phải so với ảnh trang.

## 6. Việc cho người dùng (HG2.3)

1. **COPD 2131/2026:** tự tìm trên web (moh.gov.vn, kcb.vn, trang Bệnh viện Bạch Mai hoặc Bệnh viện Phổi Trung ương, Sở Y tế) để xác nhận văn bản có tồn tại, và lấy link PDF chính thức. Nếu chỉ thấy trên trang thư viện pháp luật tư nhân, ghi "chỉ thấy trên trang tư nhân". Khi có link: `fetch_pdf --key 2131/2026 --url ...`.
2. **Viêm phổi 4815/2020:** tìm bản PDF chính thức (Sở Y tế hoặc bệnh viện đăng lại nguyên quyết định) cho phân tích phiên bản.
3. **Quyết định về 4562/2018:** coi là đã bị 2767/2023 thay trên thực tế (Bộ Y tế ghi nhầm số 3874) hay vẫn "hiện hành"? Ghi vào `docs/DECISIONS.md`.
4. **Đổi khóa file `data/raw/3874_2018.pdf`:** file này trùng sha256 với `4562_2018.pdf` và không phải 3874/2018. Đề xuất xóa hoặc đổi tên (agent không được sửa `data/raw`).
5. **Lịch TCMR:** tìm "hướng dẫn chuyên môn của Cục Phòng bệnh" về lịch tiêm theo TT13/2026 Điều 5 khoản 4 (vncdc.gov.vn bị lỗi chứng chỉ, tiemchungmorong.vn). Sau đó quyết định văn bản nào làm "chuẩn hiện hành" cho hạt giống 23–24.
6. **Chấp nhận host** ngoài danh sách ưu tiên: datafiles.chinhphu.vn (TT10/2024), bcp.cdnchinhphu.vn (TT13/2026), cmsapi.tiemchungmorong.vn (TT52/2025). Đều là nguồn nhà nước hoặc cấp viện của Bộ Y tế.
7. **TT51/2017 bản có lớp chữ:** thử tra Công báo năm 2018 trên congbao.chinhphu.vn bằng trình duyệt (tìm kiếm của trang chạy bằng JS). Nếu không có, xếp TT51/2017 vào danh sách OCR.
8. **Hen trẻ < 12 tuổi:** xác nhận có dùng 3312/2015 (bài hen trẻ em) làm chuẩn cho nhóm tuổi này hay loại hen trẻ nhỏ khỏi phạm vi.
9. (Bảo mật, không liên quan trực tiếp) vilaphoikhoe.kcb.vn (trang con của Cục KCB) đang có bài spam ("Foxit Reader Full Crack…"). Không dùng trang này làm nguồn. Có thể báo cho Cục KCB.

## 7. Đề xuất sửa mã và config (agent không tự sửa)

- `vnsoc.extract.fetch_pdf`: sau khi tải, tìm mẫu `Số:\s*(\d+)/(QĐ|20\d\d/TT)-BYT` trong 5 trang đầu. Nếu gặp số khác khóa, in cảnh báo `number_mismatch`. Kiểm tra này sẽ bắt được lỗi 3874 → 4562. Lưu ý: bản ký số thường để trống số, nên chỉ cảnh báo khi đọc được số.
- `fetch_pdf`: khi gặp 404, thử lại URL với tên file ở dạng Unicode NFD và NFC (kcb.vn dùng NFD, ví dụ 1851/2020). Bắt `ChunkedEncodingError` và thử lại 1–2 lần (kcb.vn ngắt kết nối giữa chừng khi tải .rar 8 MB).
- `text_quality`: đếm cả glyph `ƣ/Ƣ` (U+01A3/U+01A2) như dấu hiệu lớp chữ kém, và báo tỉ lệ trang gần như không có chữ trên toàn văn bản, thay vì chỉ 4 trang đầu.
- Với gói .rar có nhiều PDF (3312/2015), cho phép lưu thêm PDF trang quyết định dưới khóa phụ (ví dụ `3312/2015__qd`), để trang chứa điều khoản hiệu lực cũng có sha256.
- Hàm gộp manifest nên báo trùng `doc_key` giữa các cụm. Các dòng 3312/2015, 3874/2018 và 4562/2018 có thể trùng với cụm khác, vì agent khác đã tải các file này.
