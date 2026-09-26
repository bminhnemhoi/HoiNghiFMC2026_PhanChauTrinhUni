# Trọng tài HG1.2: phản vệ (bản OCR, `anaphylaxis_ocr`)

Kiểm bởi AI (Claude, vai integrity-auditor), **không phải người**. Ngày 26/9/2026. Đầu vào: kiểm toán A và B. Chi tiết và bằng chứng ở `anaphylaxis_ocr_final.json`.

**Kết quả:** 1 ok, 5 đã sửa, 0 loại, 0 chưa chắc. Không có lỗi giá trị, đơn vị hay quần thể. Tập `vn`, trạng thái xung đột, dung sai, mồi và nhóm xung đột không đổi (pilot_merge tính lại: giữ 6, loại 0; 2 xung đột, 4 đối chứng).

| Mẩu | a | b | c | d | A / B | Chốt | Việc đã làm |
|---|---|---|---|---|---|---|---|
| -01 (trẻ 10 kg, do thuốc) | pass | pass | pass | pass | ok / fix | **fix** | Thêm vào `moh_neighbour` bước tiêm TM trẻ em ở QĐ 3312/2015 tr.106 (mâu thuẫn nội tại: 0,1 mg/kg hay 0,1 ml/kg dd 1/10.000). Bổ sung locator WHO: tr.379 và tr.438 ghi 0,3 ml cho trẻ > 6 tuổi. |
| -02 (trẻ 10 kg, do thức ăn) | pass | pass | pass | pass | ok / ok | **fix** | Bổ sung locator WHO như -01 (lỗi trọng tài tự tìm ra). |
| -03 (người lớn) | pass | pass | pass | pass | ok / ok | **ok** | Không đổi. |
| -04 (khoảng nhắc lại) | **pass** (A fail) | pass | pass | pass | fix / ok | **fix** | Trọng tài xem ảnh tr.20: mọi chữ số đúng, OCR chỉ mất dấu ('TIEM BAP', '*'). Span giữ theo lớp chữ để verify_span qua; thêm `span_image_text` (chữ đúng theo ảnh). Thêm `grading_caveat`: QĐ 3942 ghi "có thể sớm hơn 5 phút". |
| -05 (trẻ 20 kg) | pass | pass | pass | pass | ok / fix | **fix** | Thêm bước tiêm TM của 3312 tr.106 như -01. Bổ sung locator WHO. Thêm `span_image_text` ('1/3' thay cho '1⁄3' của lớp OCR). |
| -06 (trẻ 10 tuổi, 35 kg) | pass | pass | pass | pass | ok / fix | **fix** | Ghi chú WHO cũ sai: bảng thuốc WHO tr.379/tr.438 ghi 0,3 ml cho trẻ > 6 tuổi, tức 300 µg, không phải 150 µg. Đã sửa ghi chú, thêm bản ghi WHO 0,3 mg (nằm trong tập VN, nên vẫn là đối chứng), thêm AAAAI tr.19 vào locator. |

## Cần điều phối quyết (chưa áp vào dữ liệu)

**Mặc định HG1.2 mục A.5** là "DR8 không phụ thuộc nguyên nhân". Dữ liệu hiện lại mã hóa DR8 **theo nguyên nhân**. Chỉ thị ghi "giữ nguyên", nên tôi không đổi tập `vn`. Hai cách này **không trùng nhau**. Nếu áp mặc định (theo `dr8_reading_sensitivity` do chính mẩu tính):

- -01 và -05 chuyển **xung đột → đối chứng**, vì thêm liều 3942 tr.48 "Trẻ em nặng 10-25kg: adrenaline 0,15mg".
- -03 thêm 0,3–0,5 mg (3942 tr.77) vào tập `vn`, vẫn là đối chứng.
- Các mẩu khác không đổi.

Hai mẩu xung đột duy nhất của chủ đề này phụ thuộc quyết định này. Phải áp trước khi đóng băng hoặc chấm H1. Cả 6 mẩu đã có `extraction.decision_default` với `applied_to_data=false`.

## Việc còn mở (ngoài file này)

- Manifest thiếu dòng QĐ 3942/2014. Dòng TT51/2017 còn metadata cũ.
- Sửa sidecar OCR TT51 tr.9 và tr.20 (việc S5), rồi cập nhật span cùng lúc.
- Chưa có giá trị bản cũ: TT08/1999 chưa lấy từ nguồn chính thức (HG2.3).
- Mâu thuẫn nội tại ở 3312 tr.106: chuyển bác sĩ thật xem (HG3.9).

**Ghi chú quy tắc mù:** đầu phiên có một lệnh `grep -r` từ gốc repo, có thể đã quét qua `data/runs/` trước khi tôi dừng nó. Không có tên file hay nội dung nào từ `data/runs/` được hiển thị.
