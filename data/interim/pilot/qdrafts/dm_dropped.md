# Mẩu bị loại khỏi bộ câu hỏi thí điểm: chủ đề `dm`

> **ĐÃ KHÔI PHỤC (2026-09-26):** dòng nháp P-dm-05 đã được đưa lại vào `dm.jsonl` nguyên văn (điều kiện (a) đã đạt: mã qgen mới bỏ trắc nghiệm có chủ đích khi tập Bộ Y tế nhiều mục / không có giá trị ngoài tập Bộ Y tế / không có mồi, QC ok). Hai câu trả lời ngắn quay lại; trắc nghiệm không dựng. Mẩu mang nhãn `[concordant_by_union]` trong `extraction.notes` (S3), chờ HG1.2. Phần dưới giữ làm lịch sử.


- Người ghi: question-writer (agent AI). Ngày 2026-09-26. Căn cứ: `dm_review.md` (phản biện AI đóng vai rev-clinician và rev-methods, không phải bác sĩ thật). Không xem đầu ra của mô hình được kiểm tra.
- Số mẩu bị loại: **1/8** (P-dm-05).

## P-dm-05: ĐTĐ thai kỳ, chiến lược tầm soát và chẩn đoán ở tuần 24–28 (`value_kind: cat`)

**Quyết định:** xóa dòng nháp khỏi `dm.jsonl`. Mẩu **không có câu hỏi thí điểm** (cả trả lời ngắn lẫn trắc nghiệm).

**Lý do loại phần trắc nghiệm** (phản biện kết luận "drop", người viết đồng ý):
1. Mẩu không có mồi (`decoy: []`), nên `mcq.options()` báo lỗi "mẩu không có mồi". Lỗi nằm ở dữ liệu mẩu, bản nháp không sửa được.
2. Lỗi S2 trong `mcq.options()`: phương án `superseded:3319/2017` là `two_step_allowed`, nhưng giá trị này cũng nằm trong tập Bộ Y tế hiện hành (3879/2014, DR8). Vì vậy dù có mồi, câu vẫn có hai phương án đúng theo Bộ Y tế, và một phương án bị gán sai vai "bản cũ".
3. Theo cả hai cách hiểu của HG1.2, câu trắc nghiệm không cho thông tin:
   - giữ 3879/2014: cả hai nhãn đều đúng theo Bộ Y tế;
   - bỏ 3879/2014: `two_step_allowed` trùng cùng lúc Mỹ (ADA 2026) và bản cũ 3319/2017, nên không quy được vai trò.
   Loại `cat` chỉ có hai nhãn, nên sẽ phải bịa thêm hai phương án.

**Lý do bỏ luôn phần trả lời ngắn** (khác với phản biện, phản biện chỉ loại MCQ):
- Mã dựng (`build_all`) luôn dựng MCQ cho mẩu có `superseded`, và bản nháp không có cách nào tắt việc này:
  - có stem: QC báo "mẩu không có mồi";
  - stem = null: QC báo "thiếu stem trắc nghiệm".
- Không được sửa `src/` và `pilot_atoms.jsonl`, trong khi yêu cầu là 0 mục QC không đạt. Vì vậy cách duy nhất là bỏ cả dòng nháp.
- Cái giá phải trả nhỏ. Theo S3 của phản biện, mẩu này là "đối chứng suy biến" (`concordant_by_union`): tập Bộ Y tế {one_step_only, two_step_allowed} gồm hai giá trị loại trừ nhau, nên gần như mọi câu trả lời đều được chấm "đúng Bộ Y tế". Phản biện đề nghị loại mẩu này khỏi mẫu số độ chính xác đối chứng.
- Cái mất: 2 câu trả lời ngắn (VI và EN). Hai câu này đã đạt cả 6 tiêu chí phản biện và QC mã ở lần dựng trước.

**Điều kiện đưa lại** (dán nguyên dòng JSON dưới đây vào `dm.jsonl` rồi dựng lại):
- (a) người giữ `src/` sửa S2: `options()` lọc `sup` theo cả tập `vn`, và `build_all` ghi `ok=True` kèm "MCQ không áp dụng" khi không có giá trị cài sẵn nào nằm ngoài tập Bộ Y tế. Khi đó 2 câu trả lời ngắn quay lại, còn MCQ không dựng;
- hoặc (b) HG1.2 kết luận về hiệu lực của 3879/2014 và người giữ atoms cập nhật mẩu (thêm mồi, đổi trạng thái).
- Nếu đưa lại, câu trả lời ngắn phải mang nhãn phân tích `concordant_by_union` (S3), chờ HG1.2.
- Ghi chú cho HG1.2 (theo phản biện): 5481/2020 viết "có thể thực hiện phương pháp 1 bước", tức là lời cho phép, nên nhãn `one_step_only` là một cách diễn giải. 1470/2024 (bản quét) viết theo kiểu chỉ định rõ hơn.

**Dòng nháp nguyên văn (lưu để khôi phục):**

```json
{"atom_id": "P-dm-05", "short_vi": "Ở thai phụ tuần 24–28 của thai kỳ chưa được chẩn đoán đái tháo đường trước đó, nên dùng phương pháp nào để tầm soát và chẩn đoán đái tháo đường thai kỳ (tên phương pháp/nghiệm pháp)?", "short_en": "In pregnant women at weeks 24–28 of gestation who have not been diagnosed with diabetes before, which method should be used to screen for and diagnose gestational diabetes (name of the strategy/test)?", "mcq_stem_vi": "Ở thai phụ tuần 24–28 của thai kỳ chưa được chẩn đoán đái tháo đường trước đó, chiến lược tầm soát và chẩn đoán đái tháo đường thai kỳ được khuyến cáo là gì?", "mcq_stem_en": "In pregnant women at weeks 24–28 of gestation who have not been diagnosed with diabetes before, what is the recommended strategy to screen for and diagnose gestational diabetes?", "filler": null, "notes": "Câu hỏi tránh mọi từ khớp regex cat_options (1/một bước, 2/hai bước, 75 g, 50 g, 100 g) để không lộ nhãn. Mẩu concordant theo DR8 (tập VN có cả one_step_only và two_step_allowed) nhưng có superseded (3319/2017) nên mã vẫn dựng MCQ: stem đã viết, song MCQ KHÔNG dựng được vì mẩu không có mồi (decoy: []) → mục QC 'mẩu không có mồi' là lỗi dữ liệu mẩu, không sửa được ở bản nháp. Hơn nữa lựa chọn 'superseded:3319/2017' = two_step_allowed cũng nằm trong tập VN hiện hành (3879/2014, DR8) → vai trò lựa chọn sẽ gán sai; đề nghị KHÔNG dựng MCQ cho mẩu này (hoặc chờ HG1.2: nếu bỏ 3879 thì two_step_allowed trùng cả US lẫn bản cũ → indistinguishable, MCQ vẫn không có thông tin). filler null (có superseded)."}
```

## Tác động lên bộ thí điểm `dm`

- Trước: 8 mẩu, 24 câu dựng được (16 ngắn và 8 MCQ), 8 đoạn A3, 1 mục QC không đạt.
- Sau: 7 mẩu, 22 câu (14 ngắn và 8 MCQ), 7 đoạn A3, 0 mục QC không đạt.
- Tỉ lệ loại theo mẩu là 1/8, dưới ngưỡng 20% của skill question-generation.
