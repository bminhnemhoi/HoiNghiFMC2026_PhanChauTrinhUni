---
name: statistics-plan
description: Kế hoạch phân tích đăng ký trước — H1 (chính), H2–H4 (Holm), mô tả RQ1–RQ4, GLMM trong R, bootstrap cụm, McNemar có cụm, phân tích độ nhạy, quy tắc DR (T1.5, T6.3–T6.8).
---
# Phân tích (đề cương §1.4, §5.3; làm đúng prereg/submitted)

## Kết cục và kiểm định
- **H1 (chính)**: A1, tiếng Việt, gộp 4 mô hình mở, mẩu `conflict`: Δ = P(nhãn 4 | xung đột) − P(`decoy_match` | xung đột). Xác nhận nếu cận dưới KTC 95% của Δ > 0. KTC: bootstrap theo **nhóm xung đột** (BCa; < 20 cụm → t nhỏ mẫu). Báo cáo từng mô hình và tỉ lệ vượt mức ngẫu nhiên (π_nn − π_mồi)/(1 − π_mồi).
- **H2**: A1, mẩu chỉ-Mỹ-khác (giá trị US khác mọi nguồn khác), EN vs VI: hiệu P(nhãn 4 với hệ US) — McNemar có cụm (Durkalski) hoặc GLMM ghép cặp.
- **H3**: A3, tỉ lệ (nhãn 3 hoặc 4) trên mẩu có giá trị khác biệt: cận dưới KTC 95% > 5% ở ≥ một nửa mô hình mở.
- **H4**: A2 phục vụ, tỉ số rủi ro sai (nhóm bất đồng / nhóm đồng thuận) khi trả lời tất cả: cận dưới KTC theo cụm > 2.
- Holm trong họ {H2, H3, H4}. H5 (lệch phiên bản) mô tả theo biến liên tục “số tháng từ ngày ban hành đến ngày cắt dữ liệu của mô hình” + kiểm tra thiên lệch “mới nhất”.

## Mô hình hồi quy (R, `analysis_R/glmm.R`)
`glmer(wrong ~ model*language + model*condition + slot_type + (1 + language | guideline) + (1 | atom), family = binomial)` (lme4; không hội tụ → glmmTMB; vẫn không → bỏ slope ngẫu nhiên, ghi DECISIONS). Kiểm tra bằng GLM + sai số chuẩn cụm đa chiều `sandwich::vcovCL(cluster = ~ guideline + atom)` (clubSandwich không hỗ trợ glmer/glmmTMB). Ba loại lỗi → ba GLMM nhị phân riêng. R ghi kết quả ra JSON → Python `numbers.put`.

## Độ nhạy (đăng ký trước)
Bỏ mẩu thí điểm; chỉ mẩu bác sĩ xác nhận (nếu HG3.9 có bác sĩ thật); bỏ mẩu “Bộ Y tế chậm hơn bằng chứng”; bỏ từng hệ thống đối chiếu; trọng số tác hại (chỉ khi bác sĩ gán) vs trọng số đều; ảnh hưởng lượng tử hóa (T5.4).

## Quy tắc quyết định (chi tiết trong docs/02, mục DR)
DR3: cận trên KTC 95% của tỉ lệ (3|4) ở A2 trên mẩu xung đột < 5% cho mọi mô hình → kết quả chính là sai lệch ở A1 + kết luận “RAG trên kho Bộ Y tế là đủ”, RQ3 thành khám phá. DR4, DR5 cho RQ3 (skill certified-abstention).

## Thí điểm (T1.5)
Chỉ số đếm a/b + Clopper–Pearson chính xác (không bootstrap với ~10 văn bản); tỉ lệ trùng nước ngoài vs trùng mồi; ghi rõ mẫu chọn tay, chưa có bác sĩ duyệt.
