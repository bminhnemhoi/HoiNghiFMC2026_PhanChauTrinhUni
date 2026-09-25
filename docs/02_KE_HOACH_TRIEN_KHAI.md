# Kế hoạch triển khai chi tiết — “Chuẩn điều trị của ai?”

Phiên bản 1 · 25/9/2026 · Đi cùng `01_DE_CUONG.md` (nội dung khoa học) và `03_PROMPT_CLAUDE_CODE.md` (dựng hệ thống Claude Code)

Kế hoạch này biến đề cương thành 88 việc có thứ tự, trong đó 65 việc Claude Code tự làm và 23 việc chỉ bạn làm được (mã HG). Mỗi việc có sản phẩm, tiêu chí xong và một lệnh kiểm tra tự động; Claude chỉ được đánh dấu xong khi lệnh kiểm tra chạy qua. Lịch khoảng 17 tuần: abstract FMC 30/9/2026, đóng băng kho 15/10/2026, hội nghị 12/12/2026, nộp tạp chí 11–24/1/2027. So với lịch mục 7.1 đề cương, sau khi xếp phụ thuộc thật, phần chạy mô hình lùi khoảng 1 tuần (tuần 7–9, dùng tuần dự phòng 9) để có đủ 2 tuần cho việc kiểm tay 100% mẩu xung đột; các mốc FMC, đóng băng và hạn nộp giữ nguyên.

## 0. Bắt đầu nhanh

1. **Máy**: macOS, Linux, hoặc Windows với WSL2 (Ubuntu). Hook và script chạy bằng bash + python3, nên trên Windows phải chạy Claude Code **bên trong WSL2**. Cần Python ≥ 3.10 (Ubuntu/WSL thêm gói `python3-venv`), git và Claude Code (cài theo hướng dẫn chính thức của Anthropic).
2. Tạo thư mục trống `vn-soc-audit`, chép 3 file `01_DE_CUONG.md`, `02_KE_HOACH_TRIEN_KHAI.md`, `03_PROMPT_CLAUDE_CODE.md` vào đó.
3. Trong thư mục đó chạy `claude` và gõ: **Đọc 03_PROMPT_CLAUDE_CODE.md và thực hiện toàn bộ phần KHỞI TẠO.**
4. Khi Claude báo khởi tạo xong: thoát (`/exit`) rồi chạy lại `claude` trong cùng thư mục, để các hook có hiệu lực (Claude Code nạp hook khi mở phiên). Nếu được hỏi có tin cậy thư mục/hook không, chọn đồng ý sau khi xem `.claude/settings.json`.
5. Gõ `/next`. Từ đây Claude tự làm lần lượt; hook Stop giữ Claude làm tiếp cho tới khi chỉ còn việc của bạn.
6. Muốn chạy không cần ngồi canh: mở terminal khác, chạy `scripts/autopilot.sh`. Muốn dừng: `/pause` (hoặc tạo file `state/PAUSE`).
7. Khi Claude báo có việc của bạn: xem `state/HUMAN_TODO.md` (hoặc gõ `/gate`), làm xong thì gửi một tin nhắn thường có dòng **bắt đầu** bằng **XONG <mã> <thông tin>**, ví dụ `XONG HG0.3 Llama: đang chờ duyệt`.

Việc gấp nhất hôm nay: **HG0.3** (tài khoản, khóa, phần mềm) và **HG1.0** (email ban tổ chức) trước 26/9; **HG1.2** (kiểm trích dẫn thí điểm) trước 28/9; **HG1.9** (nộp abstract) trước 30/9.

## 1. Tự động hóa tới đâu — nói thẳng

| Claude Code tự làm | Chỉ bạn làm được (HG) | Không ai bảo đảm được |
| --- | --- | --- |
| Viết và kiểm thử toàn bộ mã; tải PDF từ nguồn chính thức; trích mẩu; ghép giá trị nước ngoài; sinh và dịch câu hỏi; chạy Kaggle và API trong ngân sách; chấm điểm; thống kê; vẽ hình; viết abstract, slide, bản thảo, supplement, thư nộp; kiểm trích dẫn; tổ chức hội đồng phản biện agent ở 4 mốc; kiểm toán toàn vẹn | Tạo tài khoản, khóa, thanh toán; đồng ý điều khoản mô hình; gửi email; nộp FMC, OSF, Zenodo, tạp chí, arXiv; kiểm tay dữ liệu (lớn nhất: 100% mẩu xung đột, 40–70 giờ); làm việc với giảng viên và bác sĩ; trình bày ở hội nghị | Việc bài được nhận ở tạp chí Q1. Kế hoạch tối đa hóa khả năng (thiết kế đăng ký trước, dữ liệu kiểm chứng, phản biện nhiều vòng), nhưng quyết định là của biên tập viên và phản biện thật |

**Thời gian của bạn** ước tính 90–145 giờ trong 17 tuần (bảng mục 4), dồn nhiều nhất ở tuần 3–5. Đây là phần làm nên chất lượng: phản biện vòng 2 đã chỉ ra rằng không kiểm tay thì 11–32% “xung đột” có thể là giả do lỗi trích xuất.

**Giới hạn kỹ thuật cần biết**: hook và lệnh kiểm tra chặn các vi phạm *vô tình* (gõ nhầm, đi tắt, quên quy tắc); chúng không phải rào an ninh tuyệt đối trước một tác tử cố tình lách (ví dụ viết script Python làm điều hook chặn ở dòng lệnh). Lớp bảo vệ còn lại là quy tắc trong CLAUDE.md, test tĩnh `tests/test_integrity.py`, kiểm toán độc lập và việc bạn đọc `docs/LOG.md`. Claude Code không nhớ gì giữa các phiên ngoài file trong repo, nên mọi trạng thái nằm trong `state/`, `docs/LOG.md`, `docs/DECISIONS.md`. Phiên dài sẽ bị nén ngữ cảnh; hook tự ghi dấu và nạp lại tóm tắt. Kaggle giới hạn giờ GPU mỗi tuần và 12 giờ mỗi phiên; kế hoạch chia job ≤ 10 giờ. Hội đồng phản biện là AI: hữu ích để bắt lỗi sớm, nhưng không thay giảng viên, bác sĩ hay phản biện tạp chí.

## 2. Pha, mốc và lịch

| Pha | Thời gian | Mục tiêu | Mốc/cổng chất lượng |
| --- | --- | --- | --- |
| P0 Khởi tạo | 25–26/9 | Repo, hook, môi trường, tài khoản, chạy thử Kaggle + API | `make test` xanh; smoke test Kaggle/API |
| P1 Thí điểm + FMC | 25–30/9 | ~60 mẩu thí điểm từ PDF chính thức, chạy 3 mô hình, abstract | M1 (hội đồng agent 1 vòng); nộp FMC 30/9 |
| P2 Kho + đăng ký trước | 1–15/10 | Phân loại 52+ văn bản, kho 25–35 hướng dẫn, kho nước ngoài, OSF | OSF trước 7/10; đóng băng kho 15/10 |
| P3 Mẩu khuyến cáo | 10/10–6/11 | Trích mẩu (bắt đầu trước đóng băng), ghép, kiểm 100% xung đột 18/10–1/11, QC, bác sĩ | Độ chính xác trích ≥ 90% (cận dưới); đóng băng mẩu v1 |
| P4 Câu hỏi + thiết kế | 6–13/11 | Bộ câu hỏi VI/EN, đóng băng câu hỏi + quy tắc chấm, Zenodo, chuẩn bị trọng số | M2 (trước khi chạy chính); DOI Zenodo |
| P5 Chạy mô hình | 12/11–2/12 | 4 mô hình mở × A0–A4, API rẻ, API mạnh | Đủ ≥ 98% lượt theo run_plan; ≤ 80 giờ GPU; ≤ 40 USD |
| P6 Chấm + phân tích | 26/11–16/12 | Chấm, kiểm bộ tách (500 câu), H1–H4, RQ1–RQ4, độ nhạy | M3 (kết quả) |
| P7 Viết + FMC | 8/12–10/1 | Slide (kết quả sơ bộ), hình, bản thảo, trích dẫn, kiểm toán | Trình bày FMC 12/12; M4; giảng viên duyệt |
| P8 Nộp | 11–24/1/2027 | Gói nộp, dữ liệu/mã công khai | Bài đã nộp |

### Lịch theo tuần

| Tuần | Ngày | Việc (mã) |
| --- | --- | --- |
| 0 | 25–30/9 | T0.1, T0.2, T0.6, HG1.0*, HG0.3*, T0.4, T0.5, T1.1, HG1.2*, T1.3, T1.4, T1.5, T1.6, T1.7, T1.8, HG1.9* |
| 1 | 1–7/10 | HG1.10*, HG1.11*, T2.10, HG2.9*, T2.11, T2.1, T2.2, T2.8 |
| 2 | 8–14/10 | HG2.3*, T2.4, T2.5, T2.6, T3.1, T3.2 |
| 3 | 15–21/10 | T2.7, T3.3, T3.4, HG3.6* |
| 4 | 22–28/10 | HG3.5*, HG3.7*, T3.8, T4.9 |
| 5 | 29/10–4/11 | HG5.0*, HG4.6* |
| 6 | 5–11/11 | HG3.9*, T3.10, T3.11, T3.12, T4.1, HG4.2*, T4.3, T5.0, T6.0 |
| 7 | 12–18/11 | HG3.13*, T4.4, HG4.5*, T4.6, T4.7, T4.8, T4.10, T5.1, T5.2 |
| 8 | 19–25/11 | T5.3, T5.5 |
| 9 | 26/11–2/12 | T5.4, T5.6, T5.7, T5.8, HG5.9*, T6.1 |
| 10 | 3–9/12 | HG6.2*, T6.3, T6.4, T6.5, T6.6, T7.2 |
| 11 | 10–16/12 | T6.7, T6.8, T6.9, HG7.3* |
| 12 | 17–27/12 | T7.1, T7.4 |
| 13 | 28/12–3/1 | T7.5, HG7.6* |
| 14 | 4–10/1 | T7.7, T7.8, T7.9, HG7.10* |
| 15 | 11–17/1 | T7.11, T8.1 |
| 16 | 18–24/1 | HG8.2*, T8.3 |

`*` = việc của bạn.

## 3. Việc theo pha

Cột “Chờ” là việc phải xong trước. Chi tiết đầy đủ (sản phẩm, tiêu chí, lệnh kiểm tra, hướng dẫn cho bạn) nằm trong khối YAML ở mục 10 — đó là bản Claude đọc.

### P0 · Khởi tạo

| Mã | Việc | Ai | Tuần | Chờ | Ghi chú |
| --- | --- | --- | --- | --- | --- |
| T0.1 | Dựng repo từ prompt, cài môi trường, chạy test lõi | Claude | 0 | — |  |
| T0.2 | Kiểm tra môi trường và ghi báo cáo | Claude | 0 | T0.1 |  |
| T0.6 | Soạn sẵn thư và tài liệu cho các cổng người dùng sớm | Claude | 0 | T0.1 |  |
| HG1.0 | Gửi email hỏi ban tổ chức FMC | Bạn | 0 | T0.6 | hạn 26/9 |
| HG0.3 | Tạo tài khoản, khóa API, giới hạn chi tiêu, cài phần mềm hệ thống | Bạn | 0 | T0.2 | hạn 26/9 |
| T0.4 | Chạy thử Kaggle vLLM (Qwen3-8B-AWQ, 20 câu), chốt phiên bản vLLM chạy được trên T4 | Claude | 0 | HG0.3 | agent run-orchestrator |
| T0.5 | Chạy thử API, xác minh model ID, giá và tham số suy luận tối thiểu | Claude | 0 | HG0.3 | agent run-orchestrator |

### P1 · Thí điểm và abstract FMC

| Mã | Việc | Ai | Tuần | Chờ | Ghi chú |
| --- | --- | --- | --- | --- | --- |
| T1.1 | Dựng ~60 mẩu thí điểm từ PDF chính thức (trích nguyên văn + trang), kèm giá trị nước ngoài đã kiểm | Claude | 0 | T0.2 | có thể bỏ theo DR; agent atom-extractor |
| HG1.2 | Kiểm tay trích dẫn của mẩu thí điểm | Bạn | 0 | T1.1 | hạn 28/9; có thể bỏ theo DR |
| T1.3 | Sinh câu hỏi thí điểm (VI/EN; A0, A1, A3; trắc nghiệm 2 thứ tự) | Claude | 0 | T1.1 | có thể bỏ theo DR; agent question-writer |
| T1.4 | Chạy thí điểm — Qwen3-8B-AWQ (2 GPU) + 1 API rẻ | Claude | 0 | T1.3, HG1.2, T0.4, T0.5 | có thể bỏ theo DR; agent run-orchestrator |
| T1.5 | Chấm và phân tích thí điểm (số đếm + Clopper–Pearson; trùng nước ngoài vs trùng mồi) | Claude | 0 | T1.4 | có thể bỏ theo DR; agent grader |
| T1.6 | Viết abstract FMC bản 'thiết kế' (dự phòng) + DOCX | Claude | 0 | T0.6 | agent manuscript-writer |
| T1.7 | Viết abstract FMC có kết quả thí điểm + DOCX | Claude | 0 | T1.5, T1.6 | hạn 30/9; có thể bỏ theo DR; agent manuscript-writer |
| T1.8 | Hội đồng agent mốc M1 (thí điểm + abstract), một vòng | Claude | 0 | T1.7 |  |
| HG1.9 | Nộp abstract FMC | Bạn | 0 | T1.6 | hạn 30/9 |
| HG1.10 | Gặp giảng viên hướng dẫn — pháp lý, đạo đức, đồng tác giả | Bạn | 1 | T0.6 | hạn 7/10 |
| HG1.11 | Mời bác sĩ đồng tác giả (3–5 người) | Bạn | 1 | T0.6 | hạn 14/10 |

### P2 · Kho văn bản và đăng ký trước

| Mã | Việc | Ai | Tuần | Chờ | Ghi chú |
| --- | --- | --- | --- | --- | --- |
| T2.10 | Soạn bản đăng ký trước OSF + mã phân tích H1 chạy trên dữ liệu mô phỏng | Claude | 1 | T1.6 | agent statistician |
| HG2.9 | Nộp đăng ký trước trên OSF | Bạn | 1 | T2.10 | hạn 7/10 |
| T2.11 | Lưu bản đăng ký đã nộp (bất biến) và mã băm | Claude | 1 | HG2.9 |  |
| T2.1 | Phân loại 52+ quyết định (PDF chính thức? lớp chữ? bản quét? chỉ thấy trên TVPL?) | Claude | 1 | T0.2 | agent corpus-librarian |
| T2.2 | Tải PDF chính thức, băm SHA-256, kiểm lớp chữ | Claude | 1 | T2.1 | agent corpus-librarian |
| HG2.3 | Tìm tay văn bản chưa có PDF chính thức | Bạn | 2 | T2.2 | hạn 12/10 |
| T2.4 | Tách văn bản có vị trí (PyMuPDF/pdfplumber); OCR ≤ 10 văn bản có kiểm số | Claude | 2 | T2.2 |  |
| T2.5 | Dựng chuỗi thay thế và chọn kho 25–35 hướng dẫn hiện hành | Claude | 2 | T2.4, HG2.3 | agent corpus-librarian |
| T2.6 | Kho đối chiếu nước ngoài có phiên bản (chỉ giá trị + nguồn + vị trí) | Claude | 2 | T2.5 | agent counterpart-matcher |
| T2.7 | Đóng băng kho hướng dẫn (15/10/2026) | Claude | 3 | T2.5, T3.3 | không trước 15/10 |
| T2.8 | Cập nhật tài liệu (PubMed, Crossref, arXiv, tạp chí y học Việt Nam) + cảnh báo trùng hướng | Claude | 1 | T1.6 | agent lit-scout |

### P3 · Mẩu khuyến cáo

| Mã | Việc | Ai | Tuần | Chờ | Ghi chú |
| --- | --- | --- | --- | --- | --- |
| T3.1 | Viết pipeline trích mẩu (atomize + verify_span) và test | Claude | 2 | T2.4, T0.5 | agent atom-extractor |
| T3.2 | Trích mẩu trên kho đã chọn (trước khi đóng băng; văn bản thêm theo DR2 trích bổ sung) | Claude | 2 | T2.5, T3.1 | agent atom-extractor |
| T3.3 | Ghép giá trị nước ngoài, bản cũ, mồi; dung sai; trạng thái xung đột; nhóm xung đột | Claude | 3 | T3.2, T2.6 | agent counterpart-matcher |
| T3.4 | Công cụ duyệt + bảng tiêu chí + mẫu kiểm (100% xung đột, 200 mẩu QC, 100 cặp ghép) | Claude | 3 | T3.3 |  |
| HG3.5 | Kiểm tra 100% mẩu xung đột theo bảng tiêu chí (lượt 1) | Bạn | 4 | T3.4 | hạn 1/11 |
| HG3.6 | Kiểm chất lượng trích xuất trên 200 mẩu phân tầng | Bạn | 3 | T3.4 | hạn 27/10 |
| HG3.7 | Kiểm 100 cặp ghép giá trị nước ngoài | Bạn | 4 | T3.4 | hạn 29/10 |
| T3.8 | Gói tài liệu cho bác sĩ duyệt mẩu xung đột | Claude | 4 | T3.4, HG1.11 | có thể bỏ theo DR |
| HG3.9 | Bác sĩ duyệt mẩu xung đột — hoặc xác nhận không có bác sĩ | Bạn | 6 | T3.8 | hạn 5/11; có thể bỏ theo DR |
| T3.10 | Nhập kết quả kiểm; độ chính xác trích xuất và ghép (Clopper–Pearson); áp DR1/DR2 | Claude | 6 | HG3.5, HG3.6, HG3.7 | agent statistician |
| T3.11 | Nhập nhãn bác sĩ, tính đồng thuận, cờ 'Bộ Y tế chậm hơn bằng chứng' | Claude | 6 | T3.10, HG3.9 | agent statistician |
| T3.12 | Đóng băng mẩu v1 | Claude | 6 | T3.11, T2.7 |  |
| HG3.13 | Kiểm lại lần hai 20% mẩu xung đột (độ tin cậy nội bộ) | Bạn | 7 | HG3.5 | hạn 22/11; không trước 8/11 |

### P4 · Câu hỏi và đóng băng thiết kế

| Mã | Việc | Ai | Tuần | Chờ | Ghi chú |
| --- | --- | --- | --- | --- | --- |
| T4.1 | Sinh bộ câu hỏi chính (VI/EN; ngắn, trắc nghiệm, A6) + đoạn oracle + chunk RAG + split theo mẩu | Claude | 6 | T3.12 | agent question-writer |
| HG4.2 | Kiểm 100 câu tình huống A6 | Bạn | 6 | T4.1 | hạn 10/11 |
| T4.3 | Đóng băng câu hỏi + quy tắc chấm + điều kiện; addendum đăng ký trước | Claude | 6 | HG4.2, T2.11, T4.1 |  |
| T4.4 | Chuẩn bị gói Zenodo v1 (bộ xung đột đã duyệt + quy trình), bản nháp | Claude | 7 | T4.3, HG3.9 |  |
| HG4.5 | Công bố Zenodo v1 và tải addendum lên OSF | Bạn | 7 | T4.4 | hạn 13/11 |
| T4.6 | Hội đồng agent mốc M2 (trước khi chạy chính) — vòng 1 | Claude | 7 | T4.3 |  |
| T4.7 | Chốt mốc M2 (sửa xong yêu cầu, vòng 2 nếu cần) | Claude | 7 | T4.6 |  |
| T4.8 | Khung bản thảo (Methods có placeholder) + references.yaml | Claude | 7 | T4.3 | agent manuscript-writer |
| T4.9 | Tạo kernel Kaggle cố định 'vnsoc-weights' để chuẩn bị trọng số 4-bit (đẩy lần đầu) | Claude | 4 | T0.4 | agent run-orchestrator |
| HG5.0 | Gắn secret HF_TOKEN vào kernel vnsoc-weights (giao diện Kaggle) | Bạn | 5 | T4.9 | hạn 1/11 |
| HG4.6 | Chép danh mục 128 vấn đề cốt lõi (cho RQ4) — hoặc bỏ RQ4 sang bài sau | Bạn | 5 | T0.6 | hạn 8/11 |
| T4.10 | Ánh xạ mẩu và câu tình huống vào 128 vấn đề (core_problem_id) | Claude | 7 | HG4.6, T4.1 | có thể bỏ theo DR |

### P5 · Chạy mô hình

| Mã | Việc | Ai | Tuần | Chờ | Ghi chú |
| --- | --- | --- | --- | --- | --- |
| T5.0 | Chuẩn bị trọng số 4-bit (Llama, Sailor2, Vistral) và kiểm nạp trên T4 | Claude | 6 | T0.4, HG5.0 | agent run-orchestrator |
| T5.1 | Chỉ mục RAG bge-m3 lai (Kaggle) + đánh giá truy xuất | Claude | 7 | T4.3, T0.4 | agent run-orchestrator |
| T5.2 | Mô hình mở — A0, A1 (mọi mẩu × VI/EN) + trắc nghiệm A1 | Claude | 7 | T4.7, T5.0 | agent run-orchestrator |
| T5.3 | Mô hình mở — A2 (+5 mẫu tín hiệu), A3, A4 tập con 300 | Claude | 8 | T5.1, T5.2 | agent run-orchestrator |
| T5.4 | Kiểm ảnh hưởng lượng tử hóa (fp16 vs 4-bit, 500 câu) | Claude | 9 | T5.2 | có thể bỏ theo DR |
| T5.5 | API giá rẻ (Batch) — tập con phân tầng 1.000–1.500 mẩu × VI/EN × A0–A3 | Claude | 8 | T4.7, T0.5, T5.1 | agent run-orchestrator |
| T5.6 | API mạnh — mọi mẩu xung đột × A0/A1 × VI/EN | Claude | 9 | T5.5 | có thể bỏ theo DR; agent run-orchestrator |
| T5.7 | Khám phá A5 (RAG kho trộn) và A6 (tình huống) — nếu còn thời gian | Claude | 9 | T5.3 | có thể bỏ theo DR |
| T5.8 | Kiểm tra chất lượng lượt chạy + ghi phiên bản mô hình | Claude | 9 | T5.3, T5.4, T5.5, T5.6, T5.7 | agent run-orchestrator |
| HG5.9 | Đăng ký tham dự FMC (nếu abstract được nhận) | Bạn | 9 | HG1.9 | hạn 30/11 |

### P6 · Chấm và phân tích

| Mã | Việc | Ai | Tuần | Chờ | Ghi chú |
| --- | --- | --- | --- | --- | --- |
| T6.0 | Cài gói R (lme4, glmmTMB, sandwich, boot, jsonlite, arrow) vào thư viện người dùng | Claude | 6 | HG0.3 |  |
| T6.1 | Chấm toàn bộ lượt chạy (grader_version đóng băng) + mẫu kiểm bộ tách | Claude | 9 | T5.8 | agent grader |
| HG6.2 | Kiểm tay bộ tách đáp án | Bạn | 10 | T6.1 | hạn 6/12 |
| T6.3 | RQ1 — H1 (chính), H2, mô tả A0; GLMM trong R | Claude | 10 | HG6.2, T6.0 | agent statistician |
| T6.4 | RQ2 — H3 (A3), phân rã lỗi truy xuất vs cố chấp, bậc thang ngữ cảnh | Claude | 10 | HG6.2 | agent statistician |
| T6.5 | Lệch phiên bản (H5, biến liên tục) + thiên lệch 'mới nhất' + RQ4 mô tả | Claude | 10 | HG6.2, T4.10 | agent statistician |
| T6.6 | RQ3 — H4, cận chứng nhận Clopper–Pearson, Learn-then-Test, hai chế độ chia, so sánh | Claude | 10 | HG6.2 | agent statistician |
| T6.7 | Phân tích độ nhạy, Holm cho H2–H4, đồng thuận kiểm tay, DR3 | Claude | 11 | T6.3, T6.4, T6.5, T6.6, HG3.13 | agent statistician |
| T6.8 | Hội đồng agent mốc M3 (kết quả) — vòng 1 | Claude | 11 | T6.7 |  |
| T6.9 | Chốt mốc M3 | Claude | 11 | T6.8 |  |

### P7 · Viết bài và FMC

| Mã | Việc | Ai | Tuần | Chờ | Ghi chú |
| --- | --- | --- | --- | --- | --- |
| T7.1 | Hình F1–F5, bảng T1–T4 bản cuối (script tái tạo được) | Claude | 12 | T6.9 | agent statistician |
| T7.2 | Slide FMC (tiếng Việt, 10–12 phút) + ghi chú thuyết trình | Claude | 10 | T6.3, T6.4, HG5.9 | hạn 10/12; có thể bỏ theo DR; agent manuscript-writer |
| HG7.3 | Trình bày tại FMC (12/12/2026) | Bạn | 11 | T7.2 | hạn 12/12 |
| T7.4 | Bản thảo đầy đủ + supplement S1–S6 + checklist TRIPOD-LLM | Claude | 12 | T7.1, T4.8 | agent manuscript-writer |
| T7.5 | Kiểm chứng toàn bộ trích dẫn | Claude | 13 | T7.4 | agent lit-scout |
| HG7.6 | Xác nhận các trích dẫn văn bản pháp quy / trang web | Bạn | 13 | T7.5 | hạn 2/1/2027 |
| T7.7 | Kiểm toán toàn vẹn độc lập (integrity-auditor) + sửa lỗi | Claude | 14 | HG7.6 | agent integrity-auditor |
| T7.8 | Hội đồng agent mốc M4 (bản thảo) — vòng 1 | Claude | 14 | T7.7 |  |
| T7.9 | Chốt mốc M4 | Claude | 14 | T7.8 |  |
| HG7.10 | Giảng viên và bác sĩ đọc, duyệt bản thảo; chốt tác giả (CRediT) | Bạn | 14 | T7.9 | hạn 12/1/2027 |
| T7.11 | Sửa theo góp ý giảng viên/bác sĩ | Claude | 15 | HG7.10 | agent manuscript-writer |

### P8 · Nộp bài

| Mã | Việc | Ai | Tuần | Chờ | Ghi chú |
| --- | --- | --- | --- | --- | --- |
| T8.1 | Gói nộp tạp chí (JMIR Med Inform), thư nộp, dữ liệu/mã công khai, gói arXiv, Zenodo v2 | Claude | 15 | T7.11 | agent manuscript-writer |
| HG8.2 | Nộp bài tạp chí + arXiv + công bố Zenodo v2 | Bạn | 16 | T8.1 | hạn 24/1/2027 |
| T8.3 | Lưu trữ, gắn tag phiên bản, tổng kết dự án | Claude | 16 | HG8.2 |  |

**Đường găng**: T0.6 → T1.6 → HG1.9 (nộp FMC, bản thiết kế luôn sẵn sàng; bản có thí điểm nếu kịp); T2.1 → T2.2 → HG2.3 → T2.5 → T3.2 → T3.3 → T3.4 → **HG3.5** (40–70 giờ, 18/10–1/11, 3–5 giờ mỗi ngày) → T3.10 → T3.12 → T4.1 → HG4.2 → T4.3 → M2 → T5.2 → T5.3 → T6.1 → HG6.2 → phân tích → M3 → viết → M4 → HG7.10 → nộp. Song song: T4.9 → HG5.0 → T5.0 (trọng số) phải xong trước T5.2. Trễ ở HG3.5 kéo lùi toàn bộ phần sau.

## 4. Việc của bạn (cổng người dùng)

| Mã | Việc | Hạn | Giờ ước tính |
| --- | --- | --- | --- |
| HG1.0 | Gửi email hỏi ban tổ chức FMC | 26/9 | 0,2 |
| HG0.3 | Tạo tài khoản, khóa API, giới hạn chi tiêu, cài phần mềm hệ thống | 26/9 | 1–2 |
| HG1.2 | Kiểm tay trích dẫn của mẩu thí điểm | 28/9 | 1–2 |
| HG1.9 | Nộp abstract FMC | 30/9 | 0,5 |
| HG1.10 | Gặp giảng viên hướng dẫn — pháp lý, đạo đức, đồng tác giả | 7/10 | 2 |
| HG1.11 | Mời bác sĩ đồng tác giả (3–5 người) | 14/10 | 1 |
| HG2.9 | Nộp đăng ký trước trên OSF | 7/10 | 1 |
| HG2.3 | Tìm tay văn bản chưa có PDF chính thức | 12/10 | 3–8 |
| HG3.5 | Kiểm tra 100% mẩu xung đột theo bảng tiêu chí (lượt 1) | 1/11 | 40–70 |
| HG3.6 | Kiểm chất lượng trích xuất trên 200 mẩu phân tầng | 27/10 | 6–8 |
| HG3.7 | Kiểm 100 cặp ghép giá trị nước ngoài | 29/10 | 4–6 |
| HG3.9 | Bác sĩ duyệt mẩu xung đột — hoặc xác nhận không có bác sĩ | 5/11 | 1 (+25–30 của bác sĩ) |
| HG3.13 | Kiểm lại lần hai 20% mẩu xung đột (độ tin cậy nội bộ) | 22/11 | 5–8 |
| HG4.2 | Kiểm 100 câu tình huống A6 | 10/11 | 3–4 |
| HG4.5 | Công bố Zenodo v1 và tải addendum lên OSF | 13/11 | 1 |
| HG5.0 | Gắn secret HF_TOKEN vào kernel vnsoc-weights (giao diện Kaggle) | 1/11 | 0,3 |
| HG4.6 | Chép danh mục 128 vấn đề cốt lõi (cho RQ4) — hoặc bỏ RQ4 sang bài sau | 8/11 | 4 (hoặc 0 nếu bỏ RQ4) |
| HG5.9 | Đăng ký tham dự FMC (nếu abstract được nhận) | 30/11 | 1 |
| HG6.2 | Kiểm tay bộ tách đáp án | 6/12 | 8–12 |
| HG7.3 | Trình bày tại FMC (12/12/2026) | 12/12 | 1 ngày hội nghị |
| HG7.6 | Xác nhận các trích dẫn văn bản pháp quy / trang web | 2/1/2027 | 2–3 |
| HG7.10 | Giảng viên và bác sĩ đọc, duyệt bản thảo; chốt tác giả (CRediT) | 12/1/2027 | 3–5 |
| HG8.2 | Nộp bài tạp chí + arXiv + công bố Zenodo v2 | 24/1/2027 | 2–3 |

Cách xác nhận: gửi tin nhắn thường có dòng bắt đầu bằng **XONG <mã> <thông tin>**. Theo thiết kế, chỉ tin nhắn của bạn tạo được xác nhận (hook `user_prompt.py`); lệnh đánh dấu xong từ chối nếu thiếu xác nhận, và hook + test chặn các cách tạo xác nhận thông thường từ phía Claude.

## 5. Quy tắc quyết định (định trước, Claude áp dụng và ghi `docs/DECISIONS.md`)

| Mã | Khi nào | Làm gì | Ai quyết |
| --- | --- | --- | --- |
| DR0 | 20:00 ngày 29/9 mà chưa có kết quả thí điểm (T1.5) | Bỏ T1.7; nộp abstract bản “thiết kế” (T1.6), viết ở thì tương lai | Claude, báo bạn |
| DR1 | Cận dưới Clopper–Pearson của độ chính xác trích xuất < 90% (T3.10) | Sửa prompt, trích lại phần liên quan; sau 2 lần vẫn < 90% thì chỉ giữ loại slot có độ chính xác đạt và nêu giới hạn | Claude; lần 2 hỏi bạn |
| DR2 | Đếm sơ bộ ở T3.3 (trước đóng băng kho) hoặc sau kiểm tay ở T3.10: < 400 mẩu xung đột hoặc < 25 nhóm | Trước đóng băng: thêm văn bản hiện hành giàu xung đột có trong danh mục (ban hành trước 15/10), trích và ghép bổ sung (task thêm bằng `scripts/vs add --blocks T2.7`). Sau đóng băng: chạy tiếp với số hiện có và tính lại độ rộng khoảng tin cậy, nêu trong addendum. Không nới định nghĩa xung đột | Claude, báo bạn |
| DR3 | Cận trên KTC 95% của tỉ lệ (lệch phiên bản ∪ trùng nước ngoài) ở A2 trên mẩu xung đột < 5% với mọi mô hình | Kết quả chính = sai lệch ở A1 + kết luận “RAG trên kho Bộ Y tế là đủ”; RQ3 thành khám phá | Đăng ký trước |
| DR4 | Nhóm có < 300 mẩu hiệu chỉnh | α = 0,15 cho nhóm đó (quy tắc không dùng nhãn) | Đăng ký trước |
| DR5 | Mức trả lời được chứng nhận < 30% ở nhóm bất đồng | Kết luận lớp từ chối không hữu ích cho nhóm này — vẫn báo cáo | Đăng ký trước |
| DR6 | Dự báo giờ GPU > 80, hoặc USD > 38, hoặc trễ > 1 tuần so với lịch | Cắt theo thứ tự: A5/A6 → A4 → mô hình mạnh còn 1 → API rẻ còn 1 → mô hình mở còn 3. Luôn giữ RQ1 với A1 và A3 | Claude, báo bạn trước khi cắt bước thứ 3 trở đi |
| DR7 | Có hướng dẫn mới ban hành sau 15/10 | Không thêm vào kho; nếu nó thay một văn bản trong kho thì đánh dấu mẩu liên quan và làm phân tích độ nhạy | Claude |
| DR8 | Hai văn bản Bộ Y tế hiện hành khác nhau cho cùng quần thể | Mọi giá trị hiện hành đều đúng (hợp tập giá trị); đếm và báo cáo như kết quả phụ | Đăng ký trước |
| DR9 | Lỗi bộ tách > 5% (HG6.2) hoặc `needs_llm` > 5% ở một mô hình | Sửa bộ tách, tăng `grader_version`, chấm lại toàn bộ, báo cả hai kết quả | Claude |
| DR10 | Không có phiên bản vLLM nào chạy được trên T4 | Chuyển HF transformers + 4-bit, batch nhỏ; tính lại giờ GPU, áp DR6 nếu cần | Claude |
| DR11 | Tới tuần 5 chưa được quyền Llama 3.1 | Thay bằng một mô hình mở 7–8B khác có giấy phép rõ ràng, chọn ở T5.0, ghi lý do | Claude, báo bạn |
| DR12 | Không có bác sĩ (HG1.11/HG3.9) | Điểm kết cục chính vẫn kiểm chứng tự động; nhắm JMIR Medical Informatics/IJMI; nêu giới hạn; không nhắm JAMIA | Bạn |
| DR13 | Tìm thấy bài công bố gần như y hệt (lit-scout, rev-novelty) | Dừng, báo bạn; định vị lại theo phần chưa bị làm (truy nguồn mức giá trị, Đông Nam Á, trục phiên bản, RQ3) | Bạn + giảng viên |

## 6. Chất lượng và toàn vẹn

- **Hook chặn các vi phạm vô tình** (không phải rào an ninh tuyệt đối — xem mục 1): truy cập tự động thuvienphapluat; sửa đề cương/kế hoạch/dữ liệu đóng băng/bản đăng ký đã nộp/state/`results/numbers.json`; đọc hoặc in khóa bí mật; `sudo`, force-push, xóa dữ liệu gốc; gọi API khi hết ngân sách; tạo dataset Kaggle công khai; tự tạo xác nhận thay bạn.
- **Lệnh kiểm tra cho từng việc**: schema dữ liệu (pydantic), số lượng tối thiểu, test đơn vị, độ đủ lượt chạy so với `run_plan.json`, registry số liệu, trích dẫn.
- **Registry số liệu**: mọi con số trong abstract, slide, bài báo lấy từ `results/numbers.json` (chỉ mã trong `src/vnsoc/analysis/`, `analysis_R/` ghi được); hằng số thiết kế `{{=…}}` phải có trong `configs/*.yaml`; `make verify` bắt số gõ tay trong văn bản.
- **Đăng ký trước + đóng băng**: OSF trước khi có dữ liệu chính; kho, mẩu, câu hỏi, quy tắc chấm đóng băng có mã băm trước khi chạy; mọi lệch ghi addendum.
- **Kiểm tay có đo lường**: 100% mẩu xung đột (2 lượt, kappa), 200 mẩu QC, 100 cặp ghép, 100 câu tình huống, mẫu bộ tách đáp án.
- **Hội đồng agent 4 mốc** (M1–M4): 5 vai độc lập, điểm có trọng số, ngưỡng 7,0, không lỗi chết người; tối đa 2 vòng rồi bạn quyết định qua cổng HGM2/HGM3/HGM4 (Claude không tự vượt được).
- **Test tĩnh** (`tests/test_integrity.py`): mọi mã task được nhắc trong CLAUDE.md/agent/skill phải tồn tại; mã nguồn không gọi SDK API trả phí ngoài `api_batch`, không nhắc thuvienphapluat, không chạm xác nhận của bạn.
- **Kiểm toán độc lập** (integrity-auditor) trước khi nộp: tính lại số từ dữ liệu, kiểm trích nguyên văn, trích dẫn, mã băm, đăng ký trước.

## 7. Bản đồ bài báo

- **Tạp chí**: JMIR Medical Informatics (đầu tiên), IJMI (thay thế); JAMIA chỉ khi có bác sĩ đồng tác giả, tập mẩu đã duyệt và mô hình hàng đầu. Bài thứ hai (RQ4, tình huống kiểu đề thi) cho JMIR Medical Education.
- **Tên**: Whose Standard of Care? Jurisdictional Defaults, Guideline Staleness and Certified Abstention of LLMs on Vietnamese Ministry of Health Guidelines.
- **Thông điệp chính (tùy kết quả, viết cả hai nhánh)**: nếu H1 xác nhận — LLM, kể cả khi được yêu cầu “theo Bộ Y tế”, trả lời theo giá trị nước ngoài có tên nhiều hơn mức ngẫu nhiên; truy nguồn cho thấy hệ thống nào chiếm ưu thế và RAG/đoạn đúng sửa được bao nhiêu. Nếu không xác nhận — một kết quả âm tính có đo lường (tỉ lệ thấp, khoảng tin cậy hẹp) vẫn đáng công bố như bằng chứng an toàn có điều kiện; DR3 xác định câu chuyện RAG.
- **Hình**: F1 quy trình; F2 quy nguồn ở A1 (nhãn 1–6, vạch mồi) theo mô hình × ngôn ngữ; F3 bậc thang ngữ cảnh A0→A4; F4 lệch phiên bản theo số tháng; F5 cận chứng nhận theo mức trả lời. **Bảng**: T1 kho; T2 mô hình; T3 giả thuyết H1–H4; T4 phân rã lỗi truy xuất và cố chấp.
- **Supplement**: S1 danh mục + chuỗi thay thế; S2 quy tắc trích + QC; S3 prompt + điều kiện; S4 quy tắc chấm + kiểm bộ tách; S5 độ nhạy; S6 checklist TRIPOD-LLM.
- **Dữ liệu và mã công bố**: mẩu (giá trị + trích dẫn + vị trí), câu hỏi, mã, kết quả chấm; không phát hành toàn văn hướng dẫn.

## 8. Ngân sách

| Hạng mục | GPU Kaggle | API (USD) | Việc |
| --- | --- | --- | --- |
| Chạy thử + thí điểm | < 3 giờ | < 2 | T0.4, T0.5, T1.4 |
| Trích mẩu, ghép, sinh/dịch câu hỏi | — | 3–6 | T3.1–T4.1 |
| Chuẩn bị trọng số, RAG | 3–6 giờ | — | T5.0, T5.1 |
| 4 mô hình mở, A0–A4 (tuần 7–9) | 45–70 giờ | — | T5.2, T5.3, T5.4 |
| API giá rẻ (Batch) | — | 8–12 | T5.5 |
| API mạnh (mẩu xung đột × A0/A1 × VI/EN) | — | 5–10 mỗi mô hình | T5.6 |
| **Tổng** | **50–80 giờ** | **≤ 40 (trần cứng, dự phòng 2)** | |

Giờ công của bạn theo pha: P0–P1 khoảng 6–8 giờ; P2 4–9; P3 56–93 (kiểm tay, dồn vào 18/10–1/11); P4 8–10; P5 1; P6 8–12; P7–P8 7–11 (chưa tính ngày dự hội nghị).

## 9. Rủi ro vận hành và cách xử lý

| Rủi ro | Dấu hiệu | Xử lý |
| --- | --- | --- |
| Claude lặp vô ích hoặc kẹt | `docs/LOG.md` không có dòng mới; hook Stop nhả sau 3 lần không tiến triển | Claude phải `block` task với lý do; bạn đọc `state/HUMAN_TODO.md` |
| Hết quota Kaggle tuần | Job xếp hàng lâu / báo hết giờ | Chuyển việc không cần GPU lên trước; kéo dài sang tuần 9 dự phòng; DR6 |
| Mô hình gated chưa duyệt | Lỗi 401/403 khi tải | Kiểm HG0.3 bước 2–3; DR11 |
| Giá hoặc tên model API đổi | T0.5 hoặc job batch lỗi | Xác minh lại trên trang chính thức, cập nhật configs/models.yaml, ghi DECISIONS |
| Mất máy/phiên | — | Commit git sau mỗi task; đẩy lên GitHub riêng tư nếu bạn muốn (tự cấu hình remote) |
| Trễ lịch do việc kiểm tay | HG3.5 chậm | Làm đều hằng ngày; Claude sắp xếp mẩu theo nhóm xung đột để kiểm nhanh; DR6 cho phần chạy |
| Hướng dẫn mới ban hành giữa chừng | lit-scout/corpus-librarian phát hiện | DR7 |

## 10. Khối task (máy đọc)

Khối dưới đây là nguồn sự thật của `scripts/vs` (state/progress.json được sinh từ đây). Trường: `id`, `title`, `phase`, `owner` (claude | human; việc của bạn có mã HG), `week`, `depends_on`, `outputs` (đường dẫn/glob phải tồn tại, không rỗng), `acceptance`, `check` (lệnh bash phải thoát mã 0; `$PY` = python của `.venv`), `skill`, `agent`, `instructions` (hướng dẫn cho bạn), `not_before`, `deadline`, `skippable` (chỉ việc có cờ này mới được bỏ qua theo DR). Việc phát sinh (sửa theo hội đồng) được thêm bằng `scripts/vs add`, không sửa file này.

<!-- TASKS:BEGIN -->
```yaml
tasks:
# ============================ P0 · Khởi tạo (25–26/9) ============================
- id: T0.1
  title: Dựng repo từ prompt, cài môi trường, chạy test lõi
  phase: P0
  owner: claude
  week: 0
  outputs: [CLAUDE.md, .claude/settings.json, src/vnsoc/state.py, docs/01_DE_CUONG.md, docs/02_KE_HOACH_TRIEN_KHAI.md]
  acceptance: "Toàn bộ file trong 03 đã được tạo đúng đường dẫn; .venv có đủ gói; make test xanh; kế hoạch hợp lệ; git init + commit đầu"
  check: "test -x .venv/bin/python && $PY -m pytest -q && scripts/vs validate-plan && git rev-parse --git-dir"
- id: T0.2
  title: Kiểm tra môi trường và ghi báo cáo
  phase: P0
  owner: claude
  week: 0
  depends_on: [T0.1]
  outputs: [state/env_report.json]
  acceptance: "Báo cáo nhóm core đủ; liệt kê phần thiếu (pdf, ocr, kaggle, api, r) để người dùng làm ở HG0.3"
  check: "python3 scripts/check_env.py --need core"
- id: T0.6
  title: Soạn sẵn thư và tài liệu cho các cổng người dùng sớm
  phase: P0
  owner: claude
  week: 0
  depends_on: [T0.1]
  skill: human-gate-protocol
  outputs: [state/gates/HG1.0_email.md, state/gates/advisor_memo.md, state/gates/ethics_exemption.md, state/gates/clinician_invite.md, state/gates/project_onepager.md]
  acceptance: "Email hỏi ban tổ chức FMC (ô 500 là ký tự hay từ; abstract chỉ có thiết kế + thí điểm có được không); bản ghi nhớ cho giảng viên về pháp lý (Luật SHTT Điều 15 khoản 2, Luật 131/2025, NĐ 134/2026, điều khoản thuvienphapluat) và đồng tác giả; đơn xin miễn xem xét đạo đức (không người tham gia, văn bản công khai); thư mời bác sĩ + trang tóm tắt dự án kèm bảng xung đột hạt giống (ghi rõ chưa kiểm PDF). Tiếng Việt, lịch sự, ngắn; không bịa tên người nhận"
  check: "$PY -m vnsoc.check nofill state/gates/HG1.0_email.md state/gates/advisor_memo.md state/gates/ethics_exemption.md state/gates/clinician_invite.md"
- id: HG1.0
  title: Gửi email hỏi ban tổ chức FMC
  phase: P0
  owner: human
  week: 0
  depends_on: [T0.6]
  deadline: 2026-09-26
  outputs: [state/gates/HG1.0.txt]
  instructions: |
    1. Mở state/gates/HG1.0_email.md, sửa tên/thông tin liên hệ của bạn nếu cần.
    2. Gửi tới conference@pctu.edu.vn (tiêu đề đã soạn sẵn). Hỏi: giới hạn 500 là ký tự hay từ; abstract gồm thiết kế + thí điểm nhỏ có phù hợp không.
    3. Gõ trong Claude Code: XONG HG1.0 đã gửi lúc <giờ>. Khi ban tổ chức trả lời, dán câu trả lời vào chat.
  acceptance: "Email đã gửi"
- id: HG0.3
  title: Tạo tài khoản, khóa API, giới hạn chi tiêu, cài phần mềm hệ thống
  phase: P0
  owner: human
  week: 0
  depends_on: [T0.2]
  deadline: 2026-09-26
  outputs: [state/gates/HG0.3.txt]
  check: "python3 scripts/check_env.py --need core,kaggle,api"
  instructions: |
    Làm theo thứ tự (khoảng 1–2 giờ; Llama có thể được duyệt sau vài giờ–vài ngày):
    1. Kaggle: kaggle.com → Settings → xác minh số điện thoại (bắt buộc để dùng GPU và Internet). Settings → API → Create New Token → lưu file vào ~/.kaggle/kaggle.json rồi chạy chmod 600 ~/.kaggle/kaggle.json (hoặc đặt KAGGLE_API_TOKEN trong .env). Điền KAGGLE_USERNAME trong .env.
    2. Hugging Face: tạo tài khoản; Settings → Access Tokens → tạo token loại Read → HF_TOKEN trong .env. Mở trang meta-llama/Llama-3.1-8B-Instruct và Viet-Mistral/Vistral-7B-Chat, bấm đồng ý điều khoản.
    3. Kaggle Secrets: Settings của Kaggle (hoặc trong một notebook: Add-ons → Secrets) → thêm secret tên HF_TOKEN với giá trị token ở bước 2.
    4. API trả phí: tạo khóa Gemini (Google AI Studio) và/hoặc OpenAI. Đặt giới hạn chi tiêu ở trang quản trị sao cho TỔNG ≤ 40 USD (ví dụ Gemini 25 USD + OpenAI 15 USD). Điền GEMINI_API_KEY, OPENAI_API_KEY trong .env.
    5. Phần mềm (WSL2 Ubuntu/Linux): sudo apt update && sudo apt install -y poppler-utils tesseract-ocr tesseract-ocr-vie r-base jq pandoc git. macOS: brew install poppler tesseract tesseract-lang r jq pandoc git.
    6. Trong thư mục dự án: cp .env.example .env rồi điền các khóa. KHÔNG dán khóa vào chat.
    Gõ: XONG HG0.3 Llama: <đã duyệt/đang chờ>, Vistral: <đã/chưa>, giới hạn: Gemini <x> USD, OpenAI <y> USD.
  acceptance: "check_env nhóm core, kaggle, api đều OK"
- id: T0.4
  title: Chạy thử Kaggle vLLM (Qwen3-8B-AWQ, 20 câu), chốt phiên bản vLLM chạy được trên T4
  phase: P0
  owner: claude
  week: 0
  depends_on: [HG0.3]
  skill: kaggle-vllm-runner
  agent: run-orchestrator
  outputs: [results/smoke/kaggle_smoke.json]
  acceptance: "20 câu tiếng Việt trả về có dòng ĐÁP ÁN, không có nội dung <think>; ghi vllm_version, thời gian nạp, token/giây vào và ra; phiên bản vLLM ghi vào configs/models.yaml và docs/DECISIONS.md; giờ GPU ghi vào docs/LOG.md"
  check: "$PY -c \"import json;d=json.load(open('results/smoke/kaggle_smoke.json'));assert d['vllm_version'] and d['requests_ok']>=20 and d['tokens_out_per_s']>0 and not d.get('think_leak')\""
- id: T0.5
  title: Chạy thử API, xác minh model ID, giá và tham số suy luận tối thiểu
  phase: P0
  owner: claude
  week: 0
  depends_on: [HG0.3]
  skill: api-batch-runner
  agent: run-orchestrator
  outputs: [results/smoke/api_smoke.json]
  acceptance: "Model ID lấy từ API list (không đoán), giá kiểm trên trang chính thức ngày chạy, tham số suy luận tối thiểu đã thử; 5 lượt đồng bộ + 1 batch 20 dòng thành công; chi phí ghi sổ; configs/models.yaml hết FILL_AT_T0.5"
  check: "! grep -q FILL_AT_T0.5 configs/models.yaml && $PY -c \"import json;d=json.load(open('results/smoke/api_smoke.json'));assert d['batch_ok'] and d['models']\""
# ============================ P1 · Thí điểm và abstract FMC (25–30/9) ============================
- id: T1.1
  title: Dựng ~60 mẩu thí điểm từ PDF chính thức (trích nguyên văn + trang), kèm giá trị nước ngoài đã kiểm
  phase: P1
  owner: claude
  skippable: true
  week: 0
  depends_on: [T0.2]
  skill: atomization-protocol
  agent: atom-extractor
  outputs: [data/interim/pilot_atoms.jsonl, state/gates/HG1.2_checklist.md, tests/test_pilot_atoms.py]
  acceptance: "Từ data/seed/seed_conflicts.yaml (pilot: true) + 3 cặp lệch phiên bản + mẩu đối chứng. Mỗi mẩu có span nguyên văn, trang, quần thể, value set; giá trị nước ngoài có URL + vị trí đã mở kiểm (WHO/CDC/NCBI…); mẩu không tìm được PDF/đoạn thì bỏ và ghi lý do. ≥ 30 mẩu (mục tiêu 60), ≥ 12 mẩu xung đột. Test kiểm span có trong trang PDF và giá trị parse được từ span"
  check: "$PY -m vnsoc.check jsonl atom data/interim/pilot_atoms.jsonl --min 30 --require span_verified=true pilot=true && $PY -m vnsoc.check count data/interim/pilot_atoms.jsonl --min 12 --where conflict_status=conflict && $PY -m pytest -q tests/test_pilot_atoms.py"
- id: HG1.2
  title: Kiểm tay trích dẫn của mẩu thí điểm
  phase: P1
  owner: human
  skippable: true
  week: 0
  depends_on: [T1.1]
  deadline: 2026-09-28
  outputs: [state/gates/HG1.2_result.md]
  instructions: |
    Mở state/gates/HG1.2_checklist.md (khoảng 1–2 giờ). Với từng mẩu: mở PDF ở đúng trang, xác nhận (a) đoạn trích có đúng nguyên văn, (b) giá trị và đơn vị đúng, (c) quần thể/bối cảnh đúng (ví dụ người lớn, đo tại phòng khám, 3 tháng đầu thai kỳ), (d) giá trị nước ngoài khớp trang nguồn.
    Gõ: XONG HG1.2 sai: <danh sách mã mẩu và lỗi>, hoặc XONG HG1.2 không có lỗi.
  acceptance: "Người dùng đã kiểm toàn bộ checklist"
- id: T1.3
  title: Sinh câu hỏi thí điểm (VI/EN; A0, A1, A3; trắc nghiệm 2 thứ tự)
  phase: P1
  owner: claude
  skippable: true
  week: 0
  depends_on: [T1.1]
  skill: question-generation
  agent: question-writer
  outputs: [data/interim/pilot_questions.jsonl]
  acceptance: "Mỗi mẩu: trả lời ngắn VI + EN (quần thể đầy đủ), đoạn oracle cho A3; mẩu xung đột/lệch phiên bản có trắc nghiệm 2 thứ tự; dịch có kiểm số/đơn vị"
  check: "$PY -m vnsoc.check jsonl question data/interim/pilot_questions.jsonl --min 60"
- id: T1.4
  title: "Chạy thí điểm — Qwen3-8B-AWQ (2 GPU) + 1 API rẻ"
  phase: P1
  owner: claude
  skippable: true
  week: 0
  depends_on: [T1.3, HG1.2, T0.4, T0.5]
  skill: kaggle-vllm-runner
  agent: run-orchestrator
  outputs: [data/runs/pilot, results/run_plan_pilot.json]
  acceptance: "Loại mẩu người dùng báo sai ở HG1.2 trước khi chạy; results/run_plan_pilot.json ghi số lượt dự kiến; Qwen3-8B-AWQ chạy trên cả 2 GPU (chia đôi yêu cầu, mỗi GPU một tiến trình) + 1 API rẻ; thêm mô hình mở thứ hai chỉ khi đã có bản 4-bit không cần token; A0/A1/A3 × VI/EN + trắc nghiệm; nhiệt độ 0, 128 token; < 2 giờ GPU, < 2 USD"
  check: "$PY -m vnsoc.check runs data/runs/pilot --plan results/run_plan_pilot.json --min-frac 0.95"
- id: T1.5
  title: Chấm và phân tích thí điểm (số đếm + Clopper–Pearson; trùng nước ngoài vs trùng mồi)
  phase: P1
  owner: claude
  skippable: true
  week: 0
  depends_on: [T1.4]
  skill: grading-protocol
  agent: grader
  outputs: [data/processed/pilot_grades.parquet, results/pilot/pilot_summary.md]
  acceptance: "Kiểm tay mọi đầu ra trên mẩu xung đột; số đếm a/b riêng cho mẩu xung đột và đối chứng; mọi số ghi registry khóa pilot.* (n mẩu, k văn bản, a, b, c, d, e, f của mục 7.3)"
  check: "$PY -m vnsoc.check numbers pilot. --min 8"
- id: T1.6
  title: Viết abstract FMC bản 'thiết kế' (dự phòng) + DOCX
  phase: P1
  owner: claude
  week: 0
  depends_on: [T0.6]
  skill: tripod-llm-manuscript
  agent: manuscript-writer
  outputs: [src/vnsoc/analysis/design_counts.py, manuscript/fmc/abstract_fmc_design.md, manuscript/build/fmc/abstract_fmc_design.docx]
  acceptance: "Theo mục 7.3 (phương án không kịp thí điểm): mô tả thiết kế và bộ xung đột ứng viên, thì tương lai; mọi con số là {{design.*}} do src/vnsoc/analysis/design_counts.py tính từ data/seed/seed_conflicts.yaml (ghi rõ bộ này mới được agent đối chiếu, chưa có người kiểm) hoặc {{=hằng số}} có trong configs; tên 131 ký tự; bản ngắn + bản đủ; render ra manuscript/build/fmc/, DOCX tạo từ bản render, ≤ 1 MB"
  check: "$PY -m vnsoc.check numbers design. --min 2 && $PY -m vnsoc.numbers verify manuscript/fmc/abstract_fmc_design.md && $PY -m vnsoc.numbers render && ! grep -q '{{' manuscript/build/fmc/abstract_fmc_design.md && $PY -m vnsoc.check maxsize manuscript/build/fmc/abstract_fmc_design.docx 1000000"
- id: T1.7
  title: Viết abstract FMC có kết quả thí điểm + DOCX
  phase: P1
  owner: claude
  week: 0
  depends_on: [T1.5, T1.6]
  deadline: 2026-09-30
  skippable: true
  skill: tripod-llm-manuscript
  agent: manuscript-writer
  outputs: [manuscript/fmc/abstract_fmc.md, manuscript/build/fmc/abstract_fmc.docx]
  acceptance: "Điền các ô [n] [k] [a]…[f] bằng {{pilot.*}}; đúng giới hạn ô 500 theo trả lời ban tổ chức (chưa có trả lời → bản ≤ 500 ký tự); nêu rõ mẫu chọn tay, chưa có bác sĩ duyệt; DOCX từ bản render ≤ 1 MB. 20:00 ngày 29/9 chưa có T1.5 → skip theo DR0 và báo người dùng nộp bản thiết kế"
  check: "$PY -m vnsoc.numbers verify manuscript/fmc/abstract_fmc.md && $PY -m vnsoc.numbers render && ! grep -q '{{' manuscript/build/fmc/abstract_fmc.md && $PY -m vnsoc.check maxsize manuscript/build/fmc/abstract_fmc.docx 1000000"
- id: T1.8
  title: Hội đồng agent mốc M1 (thí điểm + abstract), một vòng
  phase: P1
  owner: claude
  week: 0
  depends_on: [T1.7]
  skill: review-panel
  outputs: [review/M1/summary.md]
  acceptance: "5 báo cáo độc lập + summary; sửa ngay lỗi làm abstract sai/nói quá (trước khi người dùng nộp); yêu cầu lớn khác thành task R1.* không chặn gì. Hạn FMC ưu tiên hơn hội đồng: không kịp trước trưa 30/9 thì làm sau khi nộp"
  check: "test -s review/M1/summary.md"
- id: HG1.9
  title: Nộp abstract FMC
  phase: P1
  owner: human
  week: 0
  depends_on: [T1.6]
  deadline: 2026-09-30
  outputs: [state/gates/HG1.9.txt]
  instructions: |
    1. Mở biểu mẫu nộp bài trên trang hội nghị (conference.pctu.edu.vn, Thông báo số 1), chọn Chủ đề 1 “AI và chuyển đổi số trong Y tế và Giáo dục Y khoa”.
    2. Chờ Claude báo bản cuối (dự kiến tối 29/9). Nếu T1.7 xong: dùng manuscript/build/fmc/abstract_fmc.md và .docx; nếu không: manuscript/build/fmc/abstract_fmc_design.md và .docx. Tới trưa 30/9 chưa có báo thì nộp bản thiết kế. Luôn dùng bản trong manuscript/build/ (đã điền số), không dùng bản còn {{…}}.
    Tên: dán dòng tên 131 ký tự. Tóm tắt: dán bản ngắn. Đính kèm file DOCX (≤ 1 MB).
    3. Kiểm lại tác giả, đơn vị (TDTU), email liên hệ trước khi bấm gửi.
    Gõ: XONG HG1.9 đã nộp lúc <giờ>, mã/email xác nhận: <...>.
  acceptance: "Đã nộp trước hạn"
- id: HG1.10
  title: Gặp giảng viên hướng dẫn — pháp lý, đạo đức, đồng tác giả
  phase: P1
  owner: human
  week: 1
  depends_on: [T0.6]
  deadline: 2026-10-07
  outputs: [state/gates/HG1.10.txt]
  instructions: |
    1. Gửi/trao đổi state/gates/advisor_memo.md với giảng viên hướng dẫn: xác nhận cách hiểu bản quyền hướng dẫn Bộ Y tế, chính sách không cào thuvienphapluat, việc chỉ công bố giá trị + trích dẫn của hướng dẫn nước ngoài; hỏi vai trò đồng tác giả.
    2. Nộp state/gates/ethics_exemption.md theo thủ tục của trường (xin miễn xem xét đạo đức).
    Gõ: XONG HG1.10 pháp lý: <ý kiến thầy/cô>, đạo đức: <đã nộp/đã có kết quả>, đồng tác giả: <...>.
  acceptance: "Có ý kiến giảng viên về pháp lý; đơn đạo đức đã nộp"
- id: HG1.11
  title: Mời bác sĩ đồng tác giả (3–5 người)
  phase: P1
  owner: human
  week: 1
  depends_on: [T0.6]
  deadline: 2026-10-14
  outputs: [state/gates/HG1.11.txt]
  instructions: |
    Gửi state/gates/clinician_invite.md + project_onepager.md tới 3–5 bác sĩ nội/truyền nhiễm hoặc dược sĩ lâm sàng (kênh gợi ý mục 9.3 đề cương: giảng viên ĐH Phan Châu Trinh, giảng viên y TDTU, nhóm tác giả khảo sát sinh viên y về AI). Công việc: duyệt mẩu xung đột tuần 4–5 (khoảng 25–30 giờ).
    Gõ: XONG HG1.11 <ai đồng ý, chuyên khoa>, hoặc XONG HG1.11 chưa có ai.
  acceptance: "Đã gửi lời mời; ghi lại kết quả"
# ============================ P2 · Kho văn bản và đăng ký trước (1–15/10) ============================
- id: T2.10
  title: Soạn bản đăng ký trước OSF + mã phân tích H1 chạy trên dữ liệu mô phỏng
  phase: P2
  owner: claude
  week: 1
  depends_on: [T1.6]
  skill: statistics-plan
  agent: statistician
  outputs: [prereg/osf_preregistration.md, prereg/analysis_plan, tests/test_prereg_code.py]
  acceptance: "Theo mẫu OSF Preregistration: câu hỏi, giả thuyết H1–H4 (điều kiện xác nhận A1), điểm kết cục, quy tắc chấm 6 nhãn + thứ tự, giá trị mồi, định nghĩa nhóm RQ3, α, δ, quy tắc sinh lưới ngưỡng, c_k, ngưỡng 30%, α dự phòng, DR3, hai chế độ đánh giá, seed chia, cỡ mẫu (mục 5.4), phân tích độ nhạy, cách xử lý mẩu thí điểm. Mã H1/H4/RQ3 chạy được trên dữ liệu mô phỏng"
  check: "$PY -m vnsoc.check nofill prereg/osf_preregistration.md && $PY -m pytest -q tests/test_prereg_code.py"
- id: HG2.9
  title: Nộp đăng ký trước trên OSF
  phase: P2
  owner: human
  week: 1
  depends_on: [T2.10]
  deadline: 2026-10-07
  outputs: [state/gates/HG2.9_osf.txt]
  check: "grep -Eq 'osf\\.io|10\\.17605' state/gates/HG2.9_osf.txt"
  instructions: |
    1. osf.io → tạo project “Whose Standard of Care?” → Registrations → New registration → mẫu “OSF Preregistration”.
    2. Chép từng phần từ prereg/osf_preregistration.md; đính kèm thư mục prereg/analysis_plan (nén zip).
    3. Có thể chọn embargo (vẫn có dấu thời gian, công khai sau). Bấm Submit.
    Gõ: XONG HG2.9 <link OSF hoặc DOI 10.17605/...>.
  acceptance: "Có link/DOI đăng ký"
- id: T2.11
  title: Lưu bản đăng ký đã nộp (bất biến) và mã băm
  phase: P2
  owner: claude
  week: 1
  depends_on: [HG2.9]
  outputs: [prereg/submitted/osf_preregistration.md, prereg/submitted/SHA256SUMS]
  acceptance: "Chép đúng bản đã nộp + analysis_plan vào prereg/submitted/, ghi link OSF, sha256; từ đây mọi thay đổi là addendum"
  check: "test -s prereg/submitted/osf_preregistration.md && test -s prereg/submitted/SHA256SUMS"
- id: T2.1
  title: Phân loại 52+ quyết định (PDF chính thức? lớp chữ? bản quét? chỉ thấy trên TVPL?)
  phase: P2
  owner: claude
  week: 1
  depends_on: [T0.2]
  skill: corpus-acquisition
  agent: corpus-librarian
  outputs: [data/interim/manifest.jsonl, results/tables/corpus_triage.csv]
  acceptance: "Mỗi văn bản một ManifestRow; khóa (số, năm); nguồn chính thức; không truy cập TVPL"
  check: "$PY -m vnsoc.check jsonl manifest data/interim/manifest.jsonl --min 52"
- id: T2.2
  title: Tải PDF chính thức, băm SHA-256, kiểm lớp chữ
  phase: P2
  owner: claude
  week: 1
  depends_on: [T2.1]
  skill: corpus-acquisition
  agent: corpus-librarian
  outputs: [tests/test_manifest.py, state/gates/HG2.3_missing.md]
  acceptance: "Mọi dòng có source_url đều có file trong data/raw khớp sha256; state/gates/HG2.3_missing.md liệt kê văn bản Bộ Y tế chưa tìm được (kèm nơi đã tìm) và nguồn nước ngoài cần đăng ký để tải (ví dụ GINA, GOLD)"
  check: "$PY -m pytest -q tests/test_manifest.py"
- id: HG2.3
  title: Tìm tay văn bản chưa có PDF chính thức
  phase: P2
  owner: human
  week: 2
  depends_on: [T2.2]
  deadline: 2026-10-12
  outputs: [state/gates/HG2.3.txt]
  instructions: |
    Mở state/gates/HG2.3_missing.md. Với từng văn bản: tìm bản PDF chính thức (kcb.vn, moh.gov.vn, trang Sở Y tế/bệnh viện, thư viện trường). Có thể dùng thuvienphapluat.vn để TRA số hiệu/ngày, nhưng không dùng file từ đó làm nguồn.
    Lưu PDF vào data/raw/manual/<số>_<năm>.pdf và ghi URL nguồn bên cạnh tên văn bản trong file HG2.3_missing.md.
    Nguồn nước ngoài cần đăng ký (GINA, GOLD…): tự đăng ký, tải PDF vào data/raw/manual_foreign/ (chỉ dùng nội bộ, không phát hành lại).
    Gõ: XONG HG2.3 tìm được <n>/<tổng>.
  acceptance: "Đã tìm hết khả năng; văn bản không tìm được được ghi rõ"
- id: T2.4
  title: Tách văn bản có vị trí (PyMuPDF/pdfplumber); OCR ≤ 10 văn bản có kiểm số
  phase: P2
  owner: claude
  week: 2
  depends_on: [T2.2]
  skill: corpus-acquisition
  outputs: [src/vnsoc/extract/pdf_to_text.py, tests/test_pdf_text.py, data/interim/text]
  acceptance: "Mỗi PDF → JSONL theo trang/khối/đề mục; bảng liều giữ cấu trúc; OCR tiếng Việt cho bản quét (≤ 10) và mọi con số được so ảnh trang (ghi log)"
  check: "$PY -m pytest -q tests/test_pdf_text.py"
- id: T2.5
  title: Dựng chuỗi thay thế và chọn kho 25–35 hướng dẫn hiện hành
  phase: P2
  owner: claude
  week: 2
  depends_on: [T2.4, HG2.3]
  skill: corpus-acquisition
  agent: corpus-librarian
  outputs: [results/tables/supersession.csv, review/supersession_check.md]
  acceptance: "supersedes/superseded_by/partially_amended_by lấy từ điều khoản trong văn bản; agent integrity-auditor kiểm lại độc lập toàn bộ chuỗi; 25–35 văn bản in_corpus (hiện hành, có lớp chữ hoặc OCR đã kiểm), ưu tiên bệnh giàu xung đột"
  check: "$PY -m vnsoc.check count data/interim/manifest.jsonl --min 25 --where in_corpus=true status=current && test -s review/supersession_check.md"
- id: T2.6
  title: Kho đối chiếu nước ngoài có phiên bản (chỉ giá trị + nguồn + vị trí)
  phase: P2
  owner: claude
  week: 2
  depends_on: [T2.5]
  skill: counterpart-matching
  agent: counterpart-matcher
  outputs: [data/interim/foreign_values.jsonl, tests/test_foreign_store.py]
  acceptance: "Mỗi bệnh trong kho: WHO hiện hành + bản trước, WHO WPRO (nếu có), US, EU_UK. Mỗi dòng ForeignRecord có url, version_date, locator, fetched_at, page_sha256 (băm trang/PDF đã mở thật); giá trị không mở được nguồn thì bỏ trống. Không lưu đoạn văn (test: không trường text nào > 200 ký tự)"
  check: "$PY -m vnsoc.check jsonl foreign data/interim/foreign_values.jsonl --min 20 && $PY -m pytest -q tests/test_foreign_store.py"
- id: T2.7
  title: Đóng băng kho hướng dẫn (15/10/2026)
  phase: P2
  owner: claude
  week: 3
  depends_on: [T2.5, T3.3]
  not_before: 2026-10-15
  outputs: [data/frozen/manifest_v1.jsonl]
  acceptance: "$PY -m vnsoc.freeze corpus sau khi đã đếm sơ bộ mẩu xung đột (T3.3) và áp DR2 nếu cần; văn bản ban hành sau 15/10 không thêm (DR7)"
  check: "test -s data/frozen/manifest_v1.jsonl && grep -q manifest_v1 data/frozen/SHA256SUMS"
- id: T2.8
  title: Cập nhật tài liệu (PubMed, Crossref, arXiv, tạp chí y học Việt Nam) + cảnh báo trùng hướng
  phase: P2
  owner: claude
  week: 1
  depends_on: [T1.6]
  skill: citation-verification
  agent: lit-scout
  outputs: [review/lit/2026-10.md, manuscript/references.yaml]
  acceptance: "Tìm các bài từ 2026-09 và các nguồn đề cương ghi là chưa tìm được (PubMed, tapchiyhocvietnam.vn); mỗi bài có DOI/arXiv và 2 câu so sánh; có bài gần như y hệt → báo người dùng ngay"
  check: "test -s review/lit/2026-10.md && test -s manuscript/references.yaml"
# ============================ P3 · Mẩu khuyến cáo (15/10–4/11) ============================
- id: T3.1
  title: Viết pipeline trích mẩu (atomize + verify_span) và test
  phase: P3
  owner: claude
  week: 2
  depends_on: [T2.4, T0.5]
  skill: atomization-protocol
  agent: atom-extractor
  outputs: [src/vnsoc/extract/atomize.py, src/vnsoc/extract/verify_span.py, configs/prompts_extract.yaml, tests/test_extract.py]
  acceptance: "Chạy thử trên 2 văn bản (≤ 0,5 USD); nếu có mẩu thí điểm thì ≥ 90% được tìm lại; test cho verify_span (khớp nguyên văn sau chuẩn hóa, giá trị parse được)"
  check: "$PY -m pytest -q tests/test_extract.py"
- id: T3.2
  title: "Trích mẩu trên kho đã chọn (trước khi đóng băng; văn bản thêm theo DR2 trích bổ sung)"
  phase: P3
  owner: claude
  week: 2
  depends_on: [T2.5, T3.1]
  skill: atomization-protocol
  agent: atom-extractor
  outputs: [data/interim/atoms_raw.jsonl, data/interim/extraction_rejects.jsonl]
  acceptance: "Mọi mẩu span_verified; bản cũ (superseded) cũng trích cho phân tích phiên bản; chi phí ghi sổ"
  check: "$PY -m vnsoc.check jsonl atom data/interim/atoms_raw.jsonl --min 500 --require span_verified=true"
- id: T3.3
  title: Ghép giá trị nước ngoài, bản cũ, mồi; dung sai; trạng thái xung đột; nhóm xung đột
  phase: P3
  owner: claude
  week: 3
  depends_on: [T3.2, T2.6]
  skill: counterpart-matching
  agent: counterpart-matcher
  outputs: [data/interim/atoms_matched.jsonl, tests/test_match.py, results/tables/conflict_summary.csv]
  acceptance: "conflict_status và tolerance tính bằng vnsoc.grade; mồi không làm mẩu thành indistinguishable; độ nhạy trên bộ hạt giống; đếm sơ bộ mẩu xung đột và nhóm → áp DR2 TRƯỚC khi đóng băng kho (task bổ sung: scripts/vs add --blocks T2.7)"
  check: "$PY -m vnsoc.check jsonl atom data/interim/atoms_matched.jsonl --min 500 && $PY -m pytest -q tests/test_match.py"
- id: T3.4
  title: Công cụ duyệt + bảng tiêu chí + mẫu kiểm (100% xung đột, 200 mẩu QC, 100 cặp ghép)
  phase: P3
  owner: claude
  week: 3
  depends_on: [T3.3]
  skill: atomization-protocol
  outputs: [review/adjudication_rubric.md, review/ui/conflicts.html, review/qc/extraction_sample.csv, review/qc/pairs_sample.csv]
  acceptance: "UI HTML tĩnh mở bằng trình duyệt, hiển thị span/trang/quần thể/giá trị VN/nước ngoài, xuất CSV; mẫu QC phân tầng 100 ngẫu nhiên + 100 xung đột (seed ghi lại); 100 cặp ghép ngẫu nhiên"
  check: "test -s review/adjudication_rubric.md && test -s review/ui/conflicts.html && test -s review/qc/extraction_sample.csv && test -s review/qc/pairs_sample.csv"
- id: HG3.5
  title: Kiểm tra 100% mẩu xung đột theo bảng tiêu chí (lượt 1)
  phase: P3
  owner: human
  week: 4
  depends_on: [T3.4]
  deadline: 2026-11-01
  outputs: [review/adjudication/conflicts_pass1.csv]
  instructions: |
    Việc lớn nhất của bạn (40–70 giờ trong khoảng 18/10–1/11, tức 3–5 giờ mỗi ngày; trên đường găng). Mở review/ui/conflicts.html bằng trình duyệt, đọc review/adjudication_rubric.md.
    Với từng mẩu xung đột: đúng bệnh? đúng quần thể? đúng can thiệp? giá trị có điều kiện đi kèm bị bỏ sót? giá trị nước ngoài đúng quần thể tương ứng? → pass/fail + lý do.
    Xuất CSV từ UI và lưu thành review/adjudication/conflicts_pass1.csv. Có thể làm từng phần; Claude tính tiến độ khi bạn hỏi.
    Gõ: XONG HG3.5 đã kiểm <n> mẩu.
  acceptance: "100% mẩu xung đột có quyết định pass/fail"
- id: HG3.6
  title: Kiểm chất lượng trích xuất trên 200 mẩu phân tầng
  phase: P3
  owner: human
  week: 3
  depends_on: [T3.4]
  deadline: 2026-10-27
  outputs: [review/qc/extraction_sample_checked.csv]
  instructions: |
    Mở review/qc/extraction_sample.csv (200 dòng). Với mỗi dòng đối chiếu PDF: giá trị, đơn vị, quần thể, can thiệp có đúng không (cột correct = 1/0, ghi lỗi). Lưu thành review/qc/extraction_sample_checked.csv.
    Gõ: XONG HG3.6.
  acceptance: "200/200 dòng đã kiểm"
- id: HG3.7
  title: Kiểm 100 cặp ghép giá trị nước ngoài
  phase: P3
  owner: human
  week: 4
  depends_on: [T3.4]
  deadline: 2026-10-29
  outputs: [review/qc/pairs_sample_checked.csv]
  instructions: |
    Mở review/qc/pairs_sample.csv (100 dòng): mở link nguồn nước ngoài, kiểm giá trị + quần thể + phiên bản (cột correct = 1/0). Lưu thành review/qc/pairs_sample_checked.csv.
    Gõ: XONG HG3.7.
  acceptance: "100/100 cặp đã kiểm"
- id: T3.8
  title: Gói tài liệu cho bác sĩ duyệt mẩu xung đột
  phase: P3
  owner: claude
  week: 4
  depends_on: [T3.4, HG1.11]
  skippable: true
  outputs: [review/clinician_packet/README.md, review/clinician_packet/conflicts_for_review.csv]
  acceptance: "Hướng dẫn 1 trang; bảng mẩu xung đột đã pass ở HG3.5, gửi theo đợt khi HG3.5 tiến triển; cột xác nhận, moh_lags_evidence, clinical_harm (độ cấp tính × hướng sai); ước tính thời gian. Không có bác sĩ (HG1.11) → skip"
  check: "test -s review/clinician_packet/conflicts_for_review.csv"
- id: HG3.9
  title: Bác sĩ duyệt mẩu xung đột — hoặc xác nhận không có bác sĩ
  phase: P3
  owner: human
  skippable: true
  week: 6
  depends_on: [T3.8]
  deadline: 2026-11-05
  outputs: [state/gates/HG3.9.txt]
  instructions: |
    Có bác sĩ: gửi review/clinician_packet/ cho bác sĩ, nhận lại file đã điền và lưu thành review/clinician/returned.csv. Gõ: XONG HG3.9 bác sĩ <tên, chuyên khoa> đã duyệt <n> mẩu.
    Không có bác sĩ: gõ XONG HG3.9 không có bác sĩ (bài nhắm JMIR Med Inform/IJMI và nêu giới hạn).
  acceptance: "Có file bác sĩ trả về, hoặc xác nhận không có bác sĩ"
- id: T3.10
  title: Nhập kết quả kiểm; độ chính xác trích xuất và ghép (Clopper–Pearson); áp DR1/DR2
  phase: P3
  owner: claude
  week: 6
  depends_on: [HG3.5, HG3.6, HG3.7]
  skill: atomization-protocol
  agent: statistician
  outputs: [data/interim/atoms.jsonl, results/tables/extraction_qc.csv]
  acceptance: "Mẩu xung đột fail bị loại hoặc sửa theo ghi chú (ghi log); registry qc.* gồm qc.extraction_cp_lower (cận dưới Clopper–Pearson độ chính xác trích), qc.pairs_cp_lower, số mẩu xung đột, số nhóm; dưới ngưỡng → áp DR1/DR2 và ghi DECISIONS (việc làm lại thêm bằng scripts/vs add --blocks T3.12)"
  check: "$PY -m vnsoc.check jsonl atom data/interim/atoms.jsonl --min 500 --require span_verified=true && $PY -m vnsoc.check numbers qc. --min 4 && ($PY -m vnsoc.check value qc.extraction_cp_lower --ge 0.90 || grep -q DR1 docs/DECISIONS.md) && (($PY -m vnsoc.check count data/interim/atoms.jsonl --min 400 --where conflict_status=conflict && $PY -m vnsoc.check families data/interim/atoms.jsonl --min 25) || grep -q DR2 docs/DECISIONS.md)"
- id: T3.11
  title: Nhập nhãn bác sĩ, tính đồng thuận, cờ 'Bộ Y tế chậm hơn bằng chứng'
  phase: P3
  owner: claude
  week: 6
  depends_on: [T3.10, HG3.9]
  agent: statistician
  outputs: [results/tables/clinician_review.csv]
  acceptance: "Có bác sĩ: gắn clinician_confirmed, moh_lags_evidence, clinical_harm; báo cáo tỉ lệ xác nhận. Không có: ghi bảng rỗng có ghi chú và registry clin.available = 0"
  check: "$PY -m vnsoc.check numbers clin. --min 1"
- id: T3.12
  title: Đóng băng mẩu v1
  phase: P3
  owner: claude
  week: 6
  depends_on: [T3.11, T2.7]
  outputs: [data/frozen/atoms_v1.jsonl]
  acceptance: "/freeze atoms; DR2 ghi trong DECISIONS nếu < 400 mẩu xung đột hoặc < 25 nhóm (kèm cỡ mẫu tính lại)"
  check: "$PY -m vnsoc.check jsonl atom data/frozen/atoms_v1.jsonl --min 500 --require span_verified=true"
- id: HG3.13
  title: Kiểm lại lần hai 20% mẩu xung đột (độ tin cậy nội bộ)
  phase: P3
  owner: human
  week: 7
  depends_on: [HG3.5]
  not_before: 2026-11-08
  deadline: 2026-11-22
  outputs: [review/adjudication/conflicts_pass2.csv]
  instructions: |
    Sau ít nhất 7 ngày kể từ lượt 1: mở review/ui/conflicts.html ở chế độ “lượt 2” (mẫu ngẫu nhiên 20%, ẩn quyết định cũ), kiểm lại như lượt 1, xuất review/adjudication/conflicts_pass2.csv.
    Gõ: XONG HG3.13.
  acceptance: "Đủ mẫu 20%"
# ============================ P4 · Câu hỏi và đóng băng thiết kế (29/10–4/11) ============================
- id: T4.1
  title: Sinh bộ câu hỏi chính (VI/EN; ngắn, trắc nghiệm, A6) + đoạn oracle + chunk RAG + split theo mẩu
  phase: P4
  owner: claude
  week: 6
  depends_on: [T3.12]
  skill: question-generation
  agent: question-writer
  outputs: [data/interim/questions.jsonl, results/tables/question_qc.csv, data/processed/rag/chunks.jsonl, review/qc/vignettes_sample.csv]
  acceptance: "Đủ dạng/ngôn ngữ cho mọi mẩu; câu mơ hồ bị loại; dịch QC; split theo mẩu ref/cal/test (tỉ lệ và seed ghi trong prereg); review/qc/vignettes_sample.csv 100 câu A6 cho HG4.2"
  check: "$PY -m vnsoc.check jsonl question data/interim/questions.jsonl --min 1000"
- id: HG4.2
  title: Kiểm 100 câu tình huống A6
  phase: P4
  owner: human
  week: 6
  depends_on: [T4.1]
  deadline: 2026-11-10
  outputs: [review/qc/vignettes_checked.csv]
  instructions: |
    Mở review/qc/vignettes_sample.csv (100 câu, Claude tạo ở T4.1). Ưu tiên nhờ bác sĩ đồng tác giả kiểm (đề cương §3.5); không có bác sĩ thì bạn kiểm và bài báo ghi rõ người kiểm. Kiểm: tình huống hợp lý ở bệnh viện huyện; đủ dữ kiện để chỉ một đáp án theo Bộ Y tế; không lộ đáp án. Cột ok = 1/0, cột nguoi_kiem, ghi chú. Lưu thành review/qc/vignettes_checked.csv.
    Gõ: XONG HG4.2.
  acceptance: "100 câu đã kiểm"
- id: T4.3
  title: Đóng băng câu hỏi + quy tắc chấm + điều kiện; addendum đăng ký trước
  phase: P4
  owner: claude
  week: 6
  depends_on: [HG4.2, T2.11, T4.1]
  outputs: [data/frozen/questions_v1.jsonl, data/frozen/grading_v1.yaml, data/frozen/conditions_v1.yaml, prereg/addenda/addendum_1.md, results/run_plan.json]
  acceptance: "Sửa/loại câu A6 theo HG4.2; /freeze questions; results/run_plan.json = số lượt dự kiến cho mọi mô hình (mở và API) × điều kiện × ngôn ngữ × dạng theo phạm vi mục 5.2, khóa model|condition|language|format; addendum liệt kê mọi khác biệt so với bản OSF — người dùng tải lên OSF ở HG4.5"
  check: "test -s data/frozen/questions_v1.jsonl && test -s data/frozen/grading_v1.yaml && test -s prereg/addenda/addendum_1.md && $PY -c \"import json;d=json.load(open('results/run_plan.json'));assert len(d)>=8 and all(v>0 for v in d.values())\""
- id: T4.4
  title: Chuẩn bị gói Zenodo v1 (bộ xung đột đã duyệt + quy trình), bản nháp
  phase: P4
  owner: claude
  week: 7
  depends_on: [T4.3, HG3.9]
  outputs: [release/zenodo_v1/README.md, tests/test_release.py, state/gates/HG4.5_zenodo.md]
  acceptance: "Chỉ giá trị + trích dẫn + vị trí (không đoạn văn nước ngoài, không toàn văn Bộ Y tế); giấy phép CC BY 4.0 dữ liệu, MIT mã; metadata; nếu có ZENODO_TOKEN tạo bản nháp qua API (không publish)"
  check: "$PY -m pytest -q tests/test_release.py"
- id: HG4.5
  title: Công bố Zenodo v1 và tải addendum lên OSF
  phase: P4
  owner: human
  week: 7
  depends_on: [T4.4]
  deadline: 2026-11-13
  outputs: [state/gates/HG4.5.txt]
  check: "grep -Eq 'zenodo|10\\.5281' state/gates/HG4.5.txt"
  instructions: |
    1. Làm theo state/gates/HG4.5_zenodo.md: mở bản nháp trên zenodo.org (hoặc tạo mới, tải file trong release/zenodo_v1/), kiểm tác giả, giấy phép, mô tả; bấm Publish.
    2. Trên OSF: thêm prereg/addenda/addendum_1.md vào project (Files) và ghi chú trong phần registration updates.
    3. (Tùy chọn) ghi chú arXiv ngắn “bộ dữ liệu + thí điểm” nếu kịp — hỏi Claude soạn.
    Gõ: XONG HG4.5 <DOI Zenodo 10.5281/...>.
  acceptance: "Có DOI Zenodo"
- id: T4.6
  title: Hội đồng agent mốc M2 (trước khi chạy chính) — vòng 1
  phase: P4
  owner: claude
  week: 7
  depends_on: [T4.3]
  skill: review-panel
  outputs: [review/M2/summary.md]
  acceptance: "5 báo cáo độc lập; yêu cầu major thành task R2.* (--blocks T4.7)"
  check: "test -s review/M2/summary.md"
- id: T4.7
  title: Chốt mốc M2 (sửa xong yêu cầu, vòng 2 nếu cần)
  phase: P4
  owner: claude
  week: 7
  depends_on: [T4.6]
  skill: review-panel
  outputs: [review/M2/summary.md]
  acceptance: "M2 ĐẠT ở vòng 1 hoặc 2, hoặc người dùng quyết định qua cổng HGM2 (chỉ người dùng xác nhận được)"
  check: "$PY -m vnsoc.check review M2"
- id: T4.8
  title: Khung bản thảo (Methods có placeholder) + references.yaml
  phase: P4
  owner: claude
  week: 7
  depends_on: [T4.3]
  skill: tripod-llm-manuscript
  agent: manuscript-writer
  outputs: [manuscript/main.md]
  acceptance: "Đủ đề mục JMIR; Methods viết xong theo bản đóng băng; Results là khung với {{khóa}}"
  check: "grep -q '## Methods' manuscript/main.md && grep -q '## Results' manuscript/main.md"
- id: T4.9
  title: Tạo kernel Kaggle cố định 'vnsoc-weights' để chuẩn bị trọng số 4-bit (đẩy lần đầu)
  phase: P4
  owner: claude
  week: 4
  depends_on: [T0.4]
  skill: kaggle-vllm-runner
  agent: run-orchestrator
  outputs: [kaggle/jobs/vnsoc-weights/kernel-metadata.json]
  acceptance: "Kernel riêng tư, id cố định <user>/vnsoc-weights, đã push một lần (tải mô hình không gated để kiểm); hướng dẫn gắn secret ghi vào state/gates/HG5.0.md"
  check: "test -s kaggle/jobs/vnsoc-weights/kernel-metadata.json && test -s state/gates/HG5.0.md"
- id: HG5.0
  title: Gắn secret HF_TOKEN vào kernel vnsoc-weights (giao diện Kaggle)
  phase: P4
  owner: human
  week: 5
  depends_on: [T4.9]
  deadline: 2026-11-01
  outputs: [state/gates/HG5.0.txt]
  instructions: |
    Secret chỉ gắn được qua giao diện và gắn theo từng notebook. Mở kaggle.com → Code → notebook “vnsoc-weights” → Edit → Add-ons → Secrets → bật HF_TOKEN → Save Version (hoặc chỉ Save). Xem thêm state/gates/HG5.0.md.
    Kiểm trên Hugging Face rằng quyền Llama 3.1 và Vistral đã được duyệt.
    Gõ: XONG HG5.0 Llama: <đã duyệt/chưa>, Vistral: <đã/chưa>.
  acceptance: "Secret đã gắn; biết trạng thái quyền của mô hình gated"
- id: HG4.6
  title: Chép danh mục 128 vấn đề cốt lõi (cho RQ4) — hoặc bỏ RQ4 sang bài sau
  phase: P4
  owner: human
  week: 5
  depends_on: [T0.6]
  deadline: 2026-11-08
  outputs: [state/gates/HG4.6.txt]
  instructions: |
    Danh mục 128 vấn đề (QĐ 22/QĐ-HĐYKQG) hiện chỉ thấy dạng ảnh. Xin bản gốc từ trường y hoặc chép tay (khoảng 4 giờ) vào data/manual/core_problems_128.csv với cột: ma, ten_van_de, chuyen_khoa.
    Không làm được: gõ XONG HG4.6 bỏ RQ4 (RQ4 chuyển sang bài thứ hai, đúng như đề cương cho phép).
    Làm xong: gõ XONG HG4.6 đã chép 128 dòng.
  acceptance: "Có file 128 dòng, hoặc quyết định bỏ RQ4"
- id: T4.10
  title: Ánh xạ mẩu và câu tình huống vào 128 vấn đề (core_problem_id)
  phase: P4
  owner: claude
  week: 7
  depends_on: [HG4.6, T4.1]
  skippable: true
  outputs: [results/tables/core_problem_map.csv]
  acceptance: "LLM đề xuất ánh xạ kèm độ tin cậy, người dùng xem mẫu 30 dòng khi được hỏi; gắn nhãn khám phá. Người dùng bỏ RQ4 ở HG4.6 → skip"
  check: "test -s results/tables/core_problem_map.csv"
# ============================ P5 · Chạy mô hình (5–25/11) ============================
- id: T5.0
  title: Chuẩn bị trọng số 4-bit (Llama, Sailor2, Vistral) và kiểm nạp trên T4
  phase: P5
  owner: claude
  week: 6
  depends_on: [T0.4, HG5.0]
  skill: kaggle-vllm-runner
  agent: run-orchestrator
  outputs: [results/smoke/model_load.json]
  acceptance: "Kernel vnsoc-weights tải mô hình (có HF_TOKEN), dùng bản 4-bit có sẵn đã kiểm nguồn/giấy phép hoặc tự lượng tử (llm-compressor; AutoAWQ đã ngừng phát triển), lưu làm output kernel để các job sau gắn qua kernel_sources (không cần secret); mỗi mô hình nạp được trên 1 T4 (hoặc TP=2 có lý do) và trả lời 10 câu; configs/models.yaml hết FILL_AT_T5.0; chưa có quyền Llama → DR11"
  check: "! grep -q FILL_AT_T5.0 configs/models.yaml && test -s results/smoke/model_load.json"
- id: T5.1
  title: Chỉ mục RAG bge-m3 lai (Kaggle) + đánh giá truy xuất
  phase: P5
  owner: claude
  week: 7
  depends_on: [T4.3, T0.4]
  skill: kaggle-vllm-runner
  agent: run-orchestrator
  outputs: [data/processed/rag/index_meta.json, results/tables/retrieval_eval.csv]
  acceptance: "Đoạn ≤ 500 token; k = 5; recall@5 của đoạn chứa đáp án ghi registry rag.*; top-k cho mọi câu A2 lưu sẵn (retrieved_ids)"
  check: "$PY -m vnsoc.check numbers rag. --min 1"
- id: T5.2
  title: Mô hình mở — A0, A1 (mọi mẩu × VI/EN) + trắc nghiệm A1
  phase: P5
  owner: claude
  week: 7
  depends_on: [T4.7, T5.0]
  skill: kaggle-vllm-runner
  agent: run-orchestrator
  outputs: [data/runs/open]
  acceptance: "Dùng results/run_plan.json từ T4.3; đo tốc độ thật ngày đầu và cập nhật ước tính giờ GPU (DR6 nếu vượt 80 giờ); mô hình thay thế theo DR11 thì cập nhật run_plan và ghi DECISIONS"
  check: "$PY -m vnsoc.check runs data/runs/open --plan results/run_plan.json --conditions A0 A1 --models-from open"
- id: T5.3
  title: Mô hình mở — A2 (+5 mẫu tín hiệu), A3, A4 tập con 300
  phase: P5
  owner: claude
  week: 8
  depends_on: [T5.1, T5.2]
  skill: kaggle-vllm-runner
  agent: run-orchestrator
  outputs: [data/runs/open]
  acceptance: "A2 phục vụ ở T=0 + 5 mẫu T=0,7; A3 đoạn oracle; A4 chỉ Qwen3 và Llama với max_model_len 32768 (chương ≤ 28k token), prefix caching"
  check: "$PY -m vnsoc.check runs data/runs/open --plan results/run_plan.json --conditions A2 A3 A4 --models-from open"
- id: T5.4
  title: Kiểm ảnh hưởng lượng tử hóa (fp16 vs 4-bit, 500 câu)
  phase: P5
  owner: claude
  week: 9
  depends_on: [T5.2]
  skippable: true
  skill: kaggle-vllm-runner
  outputs: [results/tables/quantization_check.csv]
  acceptance: "Một mô hình fp16 (2 GPU) vs 4-bit trên 500 câu cố định; tỉ lệ nhãn khác nhau; ghi registry quant.*"
  check: "$PY -m vnsoc.check numbers quant. --min 1"
- id: T5.5
  title: API giá rẻ (Batch) — tập con phân tầng 1.000–1.500 mẩu × VI/EN × A0–A3
  phase: P5
  owner: claude
  week: 8
  depends_on: [T4.7, T0.5, T5.1]
  skill: api-batch-runner
  agent: run-orchestrator
  outputs: [data/runs/api]
  acceptance: "Mọi mẩu xung đột + đối chứng ngẫu nhiên; ngân sách đặt trước qua api_batch; chi phí thực ghi sổ"
  check: "$PY -m vnsoc.check runs data/runs/api --plan results/run_plan.json --models-from api_cheap --min-frac 0.97"
- id: T5.6
  title: API mạnh — mọi mẩu xung đột × A0/A1 × VI/EN
  phase: P5
  owner: claude
  week: 9
  depends_on: [T5.5]
  skippable: true
  skill: api-batch-runner
  agent: run-orchestrator
  outputs: [data/runs/api_frontier]
  acceptance: "1–2 mô hình hàng đầu; dừng khi ngân sách còn < chi phí ước tính (DR6: còn 1 mô hình)"
  check: "$PY -m vnsoc.check runs data/runs/api_frontier --plan results/run_plan.json --models-from api_frontier --min-frac 0.97"
- id: T5.7
  title: Khám phá A5 (RAG kho trộn) và A6 (tình huống) — nếu còn thời gian
  phase: P5
  owner: claude
  week: 9
  depends_on: [T5.3]
  skippable: true
  skill: kaggle-vllm-runner
  outputs: [data/runs/open_exploratory]
  acceptance: "Gắn nhãn khám phá; cắt đầu tiên theo DR6"
  check: "$PY -m vnsoc.check runs data/runs/open_exploratory --plan results/run_plan.json --conditions A5 A6 --models-from open --min-frac 0.9"
- id: T5.8
  title: Kiểm tra chất lượng lượt chạy + ghi phiên bản mô hình
  phase: P5
  owner: claude
  week: 9
  depends_on: [T5.3, T5.4, T5.5, T5.6, T5.7]
  agent: run-orchestrator
  outputs: [results/tables/run_qa.csv, results/model_versions.json]
  acceptance: "Ma trận đủ/thiếu theo mô hình × điều kiện × ngôn ngữ × dạng; tỉ lệ lỗi; tỉ lệ thiếu dòng ĐÁP ÁN; commit hash/phiên bản và ngày cắt dữ liệu từng mô hình; tổng giờ GPU và USD"
  check: "test -s results/tables/run_qa.csv && test -s results/model_versions.json"
- id: HG5.9
  title: Đăng ký tham dự FMC (nếu abstract được nhận)
  phase: P5
  owner: human
  week: 9
  depends_on: [HG1.9]
  deadline: 2026-11-30
  outputs: [state/gates/HG5.9.txt]
  instructions: |
    Ban tổ chức thông báo trước 15/10. Được nhận: đăng ký và đóng phí theo hướng dẫn của hội nghị trước 30/11. Không được nhận: báo lại để Claude bỏ các việc FMC.
    Gõ: XONG HG5.9 <đã đăng ký / không được nhận>.
  acceptance: "Đã đăng ký hoặc đã báo không được nhận"
# ============================ P6 · Chấm và phân tích (19/11–9/12) ============================
- id: T6.0
  title: Cài gói R (lme4, glmmTMB, sandwich, boot, jsonlite, arrow) vào thư viện người dùng
  phase: P6
  owner: claude
  week: 6
  depends_on: [HG0.3]
  outputs: [analysis_R/setup.R]
  acceptance: "Rscript analysis_R/setup.R cài được không cần sudo; check_env nhóm r OK"
  check: "python3 scripts/check_env.py --need r"
- id: T6.1
  title: Chấm toàn bộ lượt chạy (grader_version đóng băng) + mẫu kiểm bộ tách
  phase: P6
  owner: claude
  week: 9
  depends_on: [T5.8]
  skill: grading-protocol
  agent: grader
  outputs: [data/processed/grades_v1.parquet, review/parser_check/sample.csv]
  acceptance: "Mọi RunRecord có nhãn hoặc needs_llm đã xử lý; condition truyền vào grade_short; tỉ lệ theo parse_method ghi registry grade.*; mẫu phân tầng 500 câu (mọi câu parse_method=llm + phân tầng theo mô hình × ngôn ngữ × cách tách) cho HG6.2"
  check: "$PY -m vnsoc.check numbers grade. --min 3 && test -s review/parser_check/sample.csv"
- id: HG6.2
  title: Kiểm tay bộ tách đáp án
  phase: P6
  owner: human
  week: 10
  depends_on: [T6.1]
  deadline: 2026-12-06
  outputs: [review/parser_check/sample_checked.csv]
  instructions: |
    Mở review/parser_check/sample.csv (500 dòng, 8–12 giờ): mỗi dòng có đầu ra gốc của mô hình và giá trị bộ tách đọc được. Cột correct = 1/0 (bộ tách đọc đúng giá trị mô hình đã trả lời hay không — KHÔNG chấm đúng/sai y khoa). Lưu thành review/parser_check/sample_checked.csv.
    Gõ: XONG HG6.2.
  acceptance: "Mẫu đã kiểm đủ"
- id: T6.3
  title: RQ1 — H1 (chính), H2, mô tả A0; GLMM trong R
  phase: P6
  owner: claude
  week: 10
  depends_on: [HG6.2, T6.0]
  skill: statistics-plan
  agent: statistician
  outputs: [results/tables/h1_h2.csv, results/figures/F2_attribution.pdf, analysis_R/glmm.R]
  acceptance: "Áp DR9 nếu bộ tách lỗi > 5%; đúng prereg; registry h1.*, h2.*, glmm.*"
  check: "$PY -m vnsoc.check numbers h1. --min 3 && $PY -m vnsoc.check numbers h2. --min 1"
- id: T6.4
  title: RQ2 — H3 (A3), phân rã lỗi truy xuất vs cố chấp, bậc thang ngữ cảnh
  phase: P6
  owner: claude
  week: 10
  depends_on: [HG6.2]
  skill: statistics-plan
  agent: statistician
  outputs: [results/tables/h3_decomposition.csv, results/figures/F3_context_ladder.pdf]
  acceptance: "Registry h3.*; lỗi truy xuất = đoạn đúng không trong top-k và trả lời sai"
  check: "$PY -m vnsoc.check numbers h3. --min 2"
- id: T6.5
  title: Lệch phiên bản (H5, biến liên tục) + thiên lệch 'mới nhất' + RQ4 mô tả
  phase: P6
  owner: claude
  week: 10
  depends_on: [HG6.2, T4.10]
  skill: statistics-plan
  agent: statistician
  outputs: [results/figures/F4_temporal.pdf, results/tables/temporal.csv]
  acceptance: "Registry h5.*, rq4.* (nếu A6 đã chạy)"
  check: "$PY -m vnsoc.check numbers h5. --min 1"
- id: T6.6
  title: RQ3 — H4, cận chứng nhận Clopper–Pearson, Learn-then-Test, hai chế độ chia, so sánh
  phase: P6
  owner: claude
  week: 10
  depends_on: [HG6.2]
  skill: certified-abstention
  agent: statistician
  outputs: [results/tables/rq3_bounds.csv, results/figures/F5_certified.pdf]
  acceptance: "Nhóm và điểm cố định trước; DR3/DR4/DR5 áp dụng và ghi DECISIONS; chế độ (b) 500 lần chia; registry h4.*, rq3.*"
  check: "$PY -m vnsoc.check numbers rq3. --min 4 && $PY -m vnsoc.check numbers h4. --min 1"
- id: T6.7
  title: Phân tích độ nhạy, Holm cho H2–H4, đồng thuận kiểm tay, DR3
  phase: P6
  owner: claude
  week: 11
  depends_on: [T6.3, T6.4, T6.5, T6.6, HG3.13]
  skill: statistics-plan
  agent: statistician
  outputs: [results/tables/sensitivity.csv]
  acceptance: "Đủ các phân tích độ nhạy đăng ký trước; kappa lượt 1–2; registry sens.*, holm.*"
  check: "$PY -m vnsoc.check numbers sens. --min 3 && $PY -m vnsoc.check numbers holm. --min 3"
- id: T6.8
  title: Hội đồng agent mốc M3 (kết quả) — vòng 1
  phase: P6
  owner: claude
  week: 11
  depends_on: [T6.7]
  skill: review-panel
  outputs: [review/M3/summary.md]
  acceptance: "Yêu cầu major thành task R3.* (--blocks T6.9)"
  check: "test -s review/M3/summary.md"
- id: T6.9
  title: Chốt mốc M3
  phase: P6
  owner: claude
  week: 11
  depends_on: [T6.8]
  skill: review-panel
  outputs: [review/M3/summary.md]
  acceptance: "M3 ĐẠT ở vòng 1 hoặc 2, hoặc người dùng quyết định qua cổng HGM3"
  check: "$PY -m vnsoc.check review M3"
# ============================ P7 · Viết bài, FMC (3/12/2026–10/1/2027) ============================
- id: T7.1
  title: Hình F1–F5, bảng T1–T4 bản cuối (script tái tạo được)
  phase: P7
  owner: claude
  week: 12
  depends_on: [T6.9]
  agent: statistician
  outputs: [results/figures/F1_pipeline.pdf, results/figures/F2_attribution.pdf, results/figures/F3_context_ladder.pdf, results/figures/F4_temporal.pdf, results/figures/F5_certified.pdf]
  acceptance: "PDF + PNG 300 dpi; font đọc được; mỗi hình có script trong src/vnsoc/analysis/figures/"
  check: "ls results/figures/F1_pipeline.pdf results/figures/F5_certified.pdf"
- id: T7.2
  title: Slide FMC (tiếng Việt, 10–12 phút) + ghi chú thuyết trình
  phase: P7
  owner: claude
  week: 10
  depends_on: [T6.3, T6.4, HG5.9]
  deadline: 2026-12-10
  skippable: true
  skill: tripod-llm-manuscript
  agent: manuscript-writer
  outputs: [manuscript/fmc/slides.md]
  acceptance: "Dựa trên kết quả H1–H3 đã có (M3 có thể chưa xong: ghi rõ “sơ bộ”); số qua registry; không nói quá; render ra manuscript/build/fmc/slides.md; bỏ qua nếu abstract không được nhận (HG5.9)"
  check: "$PY -m vnsoc.numbers verify manuscript/fmc/slides.md && $PY -m vnsoc.numbers render && ! grep -q '{{' manuscript/build/fmc/slides.md"
- id: HG7.3
  title: Trình bày tại FMC (12/12/2026)
  phase: P7
  owner: human
  week: 11
  depends_on: [T7.2]
  deadline: 2026-12-12
  outputs: [state/gates/HG7.3.txt]
  instructions: |
    Tập slide manuscript/build/fmc/slides.md (bản đã điền số; Claude có thể xuất PPTX/PDF). Trình bày; ghi lại câu hỏi và góp ý của khán giả, người liên hệ (bác sĩ quan tâm).
    Gõ: XONG HG7.3 <góp ý chính>. Nếu abstract không được nhận hoặc bạn không dự: XONG HG7.3 không tham dự.
  acceptance: "Đã trình bày"
- id: T7.4
  title: Bản thảo đầy đủ + supplement S1–S6 + checklist TRIPOD-LLM
  phase: P7
  owner: claude
  week: 12
  depends_on: [T7.1, T4.8]
  skill: tripod-llm-manuscript
  agent: manuscript-writer
  outputs: [manuscript/main.md, manuscript/supplement.md, manuscript/tripod_llm_checklist.md]
  acceptance: "make verify xanh (không số viết tay, placeholder đủ); tuyên bố đúng mức; giới hạn đầy đủ; công bố dùng AI"
  check: "$PY -m vnsoc.numbers verify && $PY -m vnsoc.numbers render"
- id: T7.5
  title: Kiểm chứng toàn bộ trích dẫn
  phase: P7
  owner: claude
  week: 13
  depends_on: [T7.4]
  skill: citation-verification
  agent: lit-scout
  outputs: [manuscript/citations_verified.json, state/gates/HG7.6_manual_refs.md]
  acceptance: "Mọi DOI/arXiv ok; state/gates/HG7.6_manual_refs.md liệt kê văn bản pháp quy/trang web cần người dùng xác nhận VÀ mọi con số trích từ bài khác (kèm câu gốc cần đối chiếu)"
  check: "test -s manuscript/citations_verified.json"
- id: HG7.6
  title: Xác nhận các trích dẫn văn bản pháp quy / trang web
  phase: P7
  owner: human
  week: 13
  depends_on: [T7.5]
  deadline: 2027-01-02
  outputs: [state/gates/HG7.6.txt]
  instructions: |
    Mở state/gates/HG7.6_manual_refs.md: mở từng link, xác nhận tên văn bản, số hiệu, ngày, và câu/giá trị được dẫn; với mỗi con số trích từ bài khác (ví dụ 74,5% của Wang & Suresh; 86,7–95% của Bazerbachi) mở bài gốc và đối chiếu. Ghi sai sót nếu có.
    Gõ: XONG HG7.6 <danh sách sai hoặc 'không sai'>.
  acceptance: "Mọi mục đã xác nhận"
- id: T7.7
  title: Kiểm toán toàn vẹn độc lập (integrity-auditor) + sửa lỗi
  phase: P7
  owner: claude
  week: 14
  depends_on: [HG7.6]
  agent: integrity-auditor
  outputs: [review/audit_final.md]
  acceptance: "Kết luận ĐẠT; mọi lỗi đã sửa và kiểm lại; verify_citations exit 0"
  check: "grep -q 'ĐẠT' review/audit_final.md && ! grep -q 'KHÔNG ĐẠT' review/audit_final.md && $PY scripts/verify_citations.py"
- id: T7.8
  title: Hội đồng agent mốc M4 (bản thảo) — vòng 1
  phase: P7
  owner: claude
  week: 14
  depends_on: [T7.7]
  skill: review-panel
  outputs: [review/M4/summary.md]
  acceptance: "Yêu cầu major thành task R4.* (--blocks T7.9)"
  check: "test -s review/M4/summary.md"
- id: T7.9
  title: Chốt mốc M4
  phase: P7
  owner: claude
  week: 14
  depends_on: [T7.8]
  skill: review-panel
  outputs: [review/M4/summary.md]
  acceptance: "M4 ĐẠT ở vòng 1 hoặc 2, hoặc người dùng quyết định qua cổng HGM4"
  check: "$PY -m vnsoc.check review M4"
- id: HG7.10
  title: Giảng viên và bác sĩ đọc, duyệt bản thảo; chốt tác giả (CRediT)
  phase: P7
  owner: human
  week: 14
  depends_on: [T7.9]
  deadline: 2027-01-12
  outputs: [state/gates/HG7.10.txt]
  instructions: |
    Gửi manuscript/build/main.md (Claude xuất DOCX/PDF khi bạn yêu cầu) + supplement cho giảng viên hướng dẫn và bác sĩ đồng tác giả. Thu góp ý (file hoặc ghi chú) vào review/advisor/. Thống nhất danh sách và thứ tự tác giả, vai trò CRediT, xung đột lợi ích, nguồn tài trợ (nếu có).
    Gõ: XONG HG7.10 tác giả: <...>; góp ý ở review/advisor/<file>.
  acceptance: "Có sự đồng ý của giảng viên (và bác sĩ nếu có)"
- id: T7.11
  title: Sửa theo góp ý giảng viên/bác sĩ
  phase: P7
  owner: claude
  week: 15
  depends_on: [HG7.10]
  agent: manuscript-writer
  outputs: [review/advisor/response.md]
  acceptance: "Bảng phản hồi từng góp ý; make verify xanh"
  check: "test -s review/advisor/response.md && $PY -m vnsoc.numbers verify"
# ============================ P8 · Nộp bài (11–24/1/2027) ============================
- id: T8.1
  title: Gói nộp tạp chí (JMIR Med Inform), thư nộp, dữ liệu/mã công khai, gói arXiv, Zenodo v2
  phase: P8
  owner: claude
  week: 15
  depends_on: [T7.11]
  skill: tripod-llm-manuscript
  agent: manuscript-writer
  outputs: [submission/cover_letter.md, submission/manuscript.docx, submission/checklist.md, release/zenodo_v2/README.md]
  acceptance: "Đúng hướng dẫn tác giả của tạp chí (kiểm trang hướng dẫn ngày làm); định dạng trích dẫn; dữ liệu phát hành chỉ giá trị + trích dẫn; make verify xanh"
  check: "make verify && $PY -m vnsoc.check nofill submission/cover_letter.md submission/checklist.md"
- id: HG8.2
  title: Nộp bài tạp chí + arXiv + công bố Zenodo v2
  phase: P8
  owner: human
  week: 16
  depends_on: [T8.1]
  deadline: 2027-01-24
  outputs: [state/gates/HG8.2.txt]
  instructions: |
    1. Tạo tài khoản trên hệ thống nộp bài của JMIR Medical Informatics (hoặc IJMI nếu chọn), nộp theo submission/checklist.md: bản thảo, supplement, thư nộp, link OSF, DOI Zenodo.
    2. arXiv (cs.CL hoặc cs.CY; cần người giới thiệu nếu lần đầu): tải gói submission/arxiv/.
    3. Zenodo: publish bản nháp v2.
    Gõ: XONG HG8.2 mã bài: <...>, arXiv: <...>, Zenodo v2: <DOI>.
  acceptance: "Bài đã nộp"
- id: T8.3
  title: Lưu trữ, gắn tag phiên bản, tổng kết dự án
  phase: P8
  owner: claude
  week: 16
  depends_on: [HG8.2]
  outputs: [docs/FINAL_SUMMARY.md]
  acceptance: "git tag v1.0-submitted; tổng kết giờ GPU, USD, số liệu chính, việc cho vòng phản biện tạp chí"
  check: "test -s docs/FINAL_SUMMARY.md && git tag | grep -q v1.0-submitted"
```
<!-- TASKS:END -->
