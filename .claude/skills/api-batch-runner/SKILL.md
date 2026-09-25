---
name: api-batch-runner
description: Gọi mô hình API trả phí qua Batch (OpenAI, Gemini) với trần ngân sách cứng, xác minh model ID và tham số suy luận tối thiểu, gom kết quả thành RunRecord (T0.5, T1.4, T3.x trích xuất, T5.5).
---
# API Batch có ngân sách

- Trần cứng 40 USD (configs/budget.yaml, dự phòng 2 USD). Mọi job: `$PY -m vnsoc.run.api_batch submit ...` → tự ước tính trần chi phí (token vào ≈ ký tự/2,5; token ra = max_tokens + reasoning_allowance; giá × 0,5 Batch) → `budget.reserve` (vượt thì từ chối) → gửi → `poll` → `fetch` (ghi chi phí thực từ usage).
- **T0.5 xác minh** (không đoán): liệt kê model khả dụng bằng SDK, chọn đúng ID cho ứng viên trong `configs/models.yaml`, kiểm giá trên trang giá chính thức, tìm tham số tắt/giảm suy luận (reasoning effort tối thiểu / thinking level thấp nhất) trong tài liệu chính thức, gửi 5 yêu cầu đồng bộ + 1 batch 20 dòng; ghi kết quả vào docs/DECISIONS.md.
- Token suy luận tính như token ra: luôn đặt mức tối thiểu và ghi `tokens_out` (đã gồm thoughts).
- Không tự sinh nhiều mẫu trên API (không có `n` rẻ) → RQ3 chỉ trên mô hình mở.
- Phân bổ (configs/budget.yaml): thí điểm ≤ 2; trích xuất + ghép + sinh/dịch câu hỏi 3–6; API rẻ 8–12; mô hình mạnh (mọi mẩu xung đột × A0/A1 × VI/EN) 5–10 mỗi mô hình; vượt → cắt theo DR6.
- Lỗi/từ chối trả lời của API ghi `error`, không gửi lại quá 1 lần; tỉ lệ lỗi > 2% → dừng và kiểm.
