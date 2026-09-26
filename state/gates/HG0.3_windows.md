# HG0.3 — Tài khoản, khóa, phần mềm (bản cho Windows)

Hạn: **26/9/2026**. Khoảng 1–2 giờ. Hướng dẫn gốc trong kế hoạch viết cho Ubuntu/macOS; máy bạn là Windows 11 nên làm theo bản này (xem `docs/DECISIONS.md`, mục ENV-WIN).

Kết quả kiểm tra môi trường lúc 26/9 (T0.2): nhóm `core` và `pdf` đã đủ; còn thiếu các mục dưới đây.

## 1. Kaggle (bắt buộc cho T0.4, T1.4, T5.x)
1. kaggle.com → Settings → xác minh số điện thoại (bắt buộc để bật GPU và Internet cho notebook).
2. Settings → API → **Create New Token** → tải `kaggle.json` → lưu vào `C:\Users\Admin\.kaggle\kaggle.json`.
   Hoặc thay vào đó điền `KAGGLE_API_TOKEN` trong `.env`.
3. Điền `KAGGLE_USERNAME=<tên đăng nhập Kaggle>` trong `.env`.

## 2. Hugging Face (bắt buộc cho mô hình gated)
1. Tạo tài khoản → Settings → Access Tokens → token loại **Read** → điền `HF_TOKEN` trong `.env`.
2. Mở hai trang sau và bấm đồng ý điều khoản (Llama có thể được duyệt sau vài giờ tới vài ngày):
   - https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct
   - https://huggingface.co/Viet-Mistral/Vistral-7B-Chat
3. Kaggle → Settings (hoặc trong notebook: Add-ons → Secrets) → thêm secret tên `HF_TOKEN` với cùng giá trị.

## 3. API trả phí (bắt buộc cho T0.5, trích mẩu, dịch, T5.5–T5.6)
1. Tạo khóa Gemini (Google AI Studio) và/hoặc OpenAI.
2. Đặt giới hạn chi tiêu ở trang quản trị của từng nhà cung cấp sao cho **tổng ≤ 40 USD** (ví dụ Gemini 25 + OpenAI 15). Ngoài ra dự án có trần cứng 40 USD trong `state/budget_ledger.csv`.
3. Điền `GEMINI_API_KEY`, `OPENAI_API_KEY` trong `.env`.

## 4. Phần mềm (PowerShell, không cần quyền quản trị với phạm vi người dùng)
```powershell
winget install --id RProject.R -e                 # R 4.6.1 (cho GLMM, tuần 10; gói R do Claude cài ở T6.0)
winget install --id UB-Mannheim.TesseractOCR -e -i   # OCR; -i mở trình cài: tích "Vietnamese" ở mục Additional language data
```
Sau khi cài: thêm vào PATH của người dùng (Settings → System → About → Advanced system settings → Environment Variables → Path của User → New):
- `C:\Program Files\R\R-4.6.1\bin`
- `C:\Program Files\Tesseract-OCR`

Rồi **đóng hẳn VS Code và mở lại** để PATH mới có hiệu lực. Nếu quên tích tiếng Việt: tải `vie.traineddata` từ https://github.com/tesseract-ocr/tessdata_best vào `C:\Program Files\Tesseract-OCR\tessdata\`.

## 5. File `.env`
Trong thư mục dự án (PowerShell): `Copy-Item .env.example .env`, mở bằng Notepad và điền các khóa ở trên.
**Không dán khóa vào chat.** Claude không đọc `.env`; mã Python tự nạp.

(Tùy chọn, dùng sau: `OSF_TOKEN`, `ZENODO_TOKEN` để Claude tạo bản nháp; `NCBI_API_KEY` để tra PubMed nhanh hơn.)

## Khi xong
Gõ một tin nhắn thường, dòng đầu bắt đầu bằng:
`XONG HG0.3 Llama: <đã duyệt/đang chờ>, Vistral: <đã/chưa>, giới hạn: Gemini <x> USD, OpenAI <y> USD`

Tôi sẽ chạy `python3 scripts/check_env.py --need core,kaggle,api` để xác nhận, rồi làm T0.4 (chạy thử Kaggle) và T0.5 (chạy thử API).
