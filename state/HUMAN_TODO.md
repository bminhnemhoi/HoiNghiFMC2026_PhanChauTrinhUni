# Việc cần BẠN làm (tự sinh — đừng sửa tay)

Cập nhật: 2026-09-26T10:23:13+07:00. Làm xong việc nào thì gửi trong Claude Code một tin nhắn có dòng BẮT ĐẦU bằng `XONG <mã>` (ví dụ `XONG HG0.3 Llama: đang chờ`) kèm thông tin được yêu cầu.

## HG0.3 — Tạo tài khoản, khóa API, giới hạn chi tiêu, cài phần mềm hệ thống (HẠN 2026-09-26)

Làm theo thứ tự (khoảng 1–2 giờ; Llama có thể được duyệt sau vài giờ–vài ngày):
1. Kaggle: kaggle.com → Settings → xác minh số điện thoại (bắt buộc để dùng GPU và Internet). Settings → API → Create New Token → lưu file vào ~/.kaggle/kaggle.json rồi chạy chmod 600 ~/.kaggle/kaggle.json (hoặc đặt KAGGLE_API_TOKEN trong .env). Điền KAGGLE_USERNAME trong .env.
2. Hugging Face: tạo tài khoản; Settings → Access Tokens → tạo token loại Read → HF_TOKEN trong .env. Mở trang meta-llama/Llama-3.1-8B-Instruct và Viet-Mistral/Vistral-7B-Chat, bấm đồng ý điều khoản.
3. Kaggle Secrets: Settings của Kaggle (hoặc trong một notebook: Add-ons → Secrets) → thêm secret tên HF_TOKEN với giá trị token ở bước 2.
4. API trả phí: tạo khóa Gemini (Google AI Studio) và/hoặc OpenAI. Đặt giới hạn chi tiêu ở trang quản trị sao cho TỔNG ≤ 40 USD (ví dụ Gemini 25 USD + OpenAI 15 USD). Điền GEMINI_API_KEY, OPENAI_API_KEY trong .env.
5. Phần mềm (WSL2 Ubuntu/Linux): sudo apt update && sudo apt install -y poppler-utils tesseract-ocr tesseract-ocr-vie r-base jq pandoc git. macOS: brew install poppler tesseract tesseract-lang r jq pandoc git.
6. Trong thư mục dự án: cp .env.example .env rồi điền các khóa. KHÔNG dán khóa vào chat.
Gõ: XONG HG0.3 Llama: <đã duyệt/đang chờ>, Vistral: <đã/chưa>, giới hạn: Gemini <x> USD, OpenAI <y> USD.

Xong khi: check_env nhóm core, kaggle, api đều OK

