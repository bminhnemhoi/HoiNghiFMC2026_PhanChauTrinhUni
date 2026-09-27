# BÀN GIAO — trạng thái dự án và cách làm tiếp

Cập nhật: 27/9/2026, 23:50 (+07). Phiên trước dừng theo yêu cầu người dùng ("đang có việc; lưu đầy đủ để phiên sau
triển khai tiếp"). Autopilot đang **tạm dừng** (`state/PAUSE`). Tài liệu này là điểm vào của phiên sau; số liệu đo
bằng mã lúc bàn giao, không ước lượng.

## 0. Phiên sau bắt đầu thế nào

1. Đọc `CLAUDE.md` và tài liệu này. `scripts/vs list` và `/status` để xem task.
2. Chỉ chạy tiếp khi người dùng bảo (ví dụ "bắt đầu triển khai tiếp") → `scripts/vs resume` (hoặc `/resume`).
3. Hỏi/nhắc người dùng hai cổng đang chờ (mục 2) trước khi làm việc dài.
4. Làm theo thứ tự ở mục 5. Hai workflow agent chạy tiếp theo mục 4 (không dùng `resumeFromRunId` — chỉ có hiệu
   lực trong phiên đã chạy).

## 1. Đã xong (có bằng chứng trong repo)

| Hạng mục | Kết quả | Ở đâu |
|---|---|---|
| Thí điểm (T1.x) | 65 mẩu chọn tay, 61 phân tích, Qwen3-8B cục bộ; bộ chấm 1.2.0 khóa; hội đồng M1 + sửa R1.1–R1.7 | `results/pilot/`, `results/numbers.json` (pilot.*), `review/M1/` |
| Abstract FMC 2026 | Viết lại theo mẫu hội nghị, VI 250 / EN 246 từ; dựng từ chính file mẫu; kiểm toán độc lập tính lại mọi số (482/482 nhãn khớp) | `Nop_Final_PhanChauTrinh_HT2026/` (thư mục nộp duy nhất), nguồn `manuscript/fmc/abstract_fmc.md`, `src/vnsoc/fmc.py` |
| Kho hướng dẫn (T2.1–T2.5) | 25 văn bản in_corpus (D28), chuỗi thay thế, OCR 9/10 | `data/interim/manifest.jsonl`, `review/supersession_check.md`, `results/tables/supersession.csv` |
| Đăng ký trước (bản nháp) | Đồng bộ 1.2.0/1.3.x, D1–D30 (D13–D30 mặc định chờ tác giả xác nhận), addendum 1 | `prereg/osf_preregistration.md`, `prereg/addenda/`, `review/prereg/response.md` |
| Bộ đọc/chấm 1.3.1 | 418 INN, 970 bí danh, 412 cách viết đơn vị; CHƯA đóng băng (cần R1.2b) | `configs/grading.yaml`, `src/vnsoc/grade.py`, `src/vnsoc/normalize_vi.py` |
| Mô hình cục bộ | Máy chủ Ollama riêng cổng 11435, `D:\ollama\models`: qwen3:8b (500a1f06…), llama3.1:8b, sailor2:8b, Vistral-7B Q4_0, bge-m3 | `scripts/ollama_d.ps1`, `configs/models.yaml`, DECISIONS 27/9 18:10 |
| R | R 4.6.1 + lme4, glmmTMB, sandwich, boot, jsonlite, arrow (T6.0) | `analysis_R/setup.R` |
| Bản thảo | Khung JMIR/TRIPOD-LLM ~11.600 từ: Methods + Limitations viết xong; Results/Discussion chờ số nghiên cứu chính | `manuscript/main.md`, `manuscript/TODO_manuscript.md`, `manuscript/references.yaml` (100 mục: 86 ok, 14 cần người kiểm) |

## 2. Việc CHỈ người dùng làm (cổng đang chờ)

- **HG1.9 — nộp abstract FMC, hạn hết 30/9/2026.** Hướng dẫn: `Nop_Final_PhanChauTrinh_HT2026/00_DOC_TRUOC_HUONG_DAN_NOP.txt`.
  Khi người dùng gõ `XONG HG1.9 …`: ghi bằng chứng vào `state/gates/`, `scripts/vs human-done HG1.9 --note "…"`.
  Thư mục cũ `NOP_FMC/` là bản lỗi thời — hook chặn Claude xóa; người dùng tự xóa nếu muốn.
- **HG2.9 — nộp đăng ký trước trên OSF, hạn 7/10/2026.** Trước đó người dùng nên xác nhận (hoặc để mặc định) D13–D30
  trong `review/prereg/response.md`. Sau khi nộp: T2.11 lưu bản bất biến + mã băm.
- Không có bác sĩ thật (HG3.9 chưa có) và người dùng không muốn gửi gói kiểm cho đồng tác giả → mọi kiểm tra là kiểm
  toán AI; bài báo ghi rõ là hạn chế. Không bao giờ viết "bác sĩ đã duyệt".

## 3. Đang dở — số đo lúc bàn giao

### 3.1 Trích mẩu nghiên cứu chính (T3.1–T3.2)
- `data/interim/atoms_parts/`: **10.903 mẩu** thô (chưa gộp, chưa kiểm toán) trên 16/25 văn bản; **45/62 phần trang xong**
  (có file mẩu + `_coverage.md` đủ tới trang cuối).
- Xong trọn: 3610/2015, 162/2024, 2388/2024, 3312/2024, 5968/2021, 2131/2026, 2760/2023, và 4 văn bản trích thử đã
  làm lại theo giao thức 1.1 (2892/2022, 1857/2022, 1019/2025, 1840/2025).
- Dở: 2147/2026 (thiếu tr. 32–62), 5642/2015 (thiếu tr. 59–86), 5481/2020 (thiếu tr. 27–77).
- Chưa trích: 5904/2019, 1740/2026, 1154/2024, 2855/2024, 1470/2024, 678/2025, 292/2024, 3377/2023, TT51/2017, 3192/2010, 6101/2019.
- **Chưa văn bản nào được kiểm toán độc lập** (mọi agent kiểm toán của lượt trước hỏng vì hết giới hạn phiên tài khoản).
- Tỉ lệ tìm lại mẩu thí điểm (tiêu chí ≥ 90%): **30/61 = 49,2%** — cả 31 mẩu thiếu nằm trên trang CHƯA trích
  (1740/2026 ×10, 3377/2023 ×8, TT51/2017 ×7, 5904/2019 ×2, 3192/2010, 5642 tr.63/84, 5481 tr.34); trên trang đã trích: 30/30.
  Đo lại bằng `$PY -m vnsoc.extract.atomize refind` (ghi `review/extraction_audit/pilot_refind.json`).
- Số mẩu nhiều hơn dự kiến (2.000–3.500) → chạy mô hình theo quy tắc lấy mẫu D30 (prereg §2.5).

### 3.2 Kho giá trị nước ngoài (T2.6, trạng thái in_progress)
- `data/interim/foreign_parts/`: 10/12 nhóm, **1.464 bản ghi**; sổ nguồn `data/interim/foreign_sources/` (chỉ URL, phiên
  bản, sha256, vị trí — không đoạn văn).
- Thiếu 2 nhóm: **ckd** (2388/2024) và **acute_infect_tox** (TT51/2017, 5642/2015, 3610/2015).
- Chưa nhóm nào được kiểm độc lập. `foreign_values.jsonl` (1.347 giữ / 117 loại) gộp lúc 12:55 — gộp lại sau khi đủ nhóm:
  `$PY -m vnsoc.match.foreign_store`.

## 4. Chạy tiếp hai workflow agent (đã lưu trong repo)

```bash
$PY scripts/workflows/resume_args.py      # tính việc còn lại từ đĩa -> logs/wf/extract_args.json, logs/wf/foreign_args.json
```
- Trích mẩu: Workflow với `scriptPath: scripts/workflows/main_atom_extraction.js` (chép sang scratchpad nếu công cụ báo
  không đọc được đường dẫn) và `args` = NỘI DUNG JSON của `logs/wf/extract_args.json` (mảng thật, không phải đường dẫn).
  Mỗi văn bản: trích các phần `todo` → kiểm toán độc lập (mẫu 40 mẩu, hạt giống 20260927, độ phủ trên trang ngẫu nhiên)
  → sửa nếu `needs_repair`. Kết quả kiểm toán: `review/extraction_audit/<doc>.md|.json`.
- Kho nước ngoài: `scriptPath: scripts/workflows/foreign_store.js`, `args` = nội dung `logs/wf/foreign_args.json`
  (nhóm đã thu thập chỉ qua bước kiểm; kết quả `review/foreign_audit/<nhóm>.md|.json`).
- **Giới hạn phiên tài khoản** đã làm hỏng 42/87 agent lượt trước: chạy theo lô nhỏ (ví dụ 6–8 văn bản mỗi lần), chạy lại
  `resume_args.py` giữa các lô; văn bản lớn (≥ 100 trang) trước.
- Sau mỗi lô: `$PY -m vnsoc.extract.atoms_merge` (gộp + kiểm bằng mã → `data/interim/atoms.jsonl`, `atoms_rejects.jsonl`,
  `review/atoms/audit_sheet.csv`), `refind`, commit.
- Các script workflow đã chạy xong (hiệu chỉnh trích mẩu, viết abstract FMC) lưu ở `scripts/workflows/archive/` để tái lập.

## 5. Thứ tự việc tiếp theo (theo kế hoạch `docs/02_KE_HOACH_TRIEN_KHAI.md`)

1. Trích nốt 17 phần + kiểm toán/sửa 25 văn bản (mục 4) → gộp → refind ≥ 90% → đóng T3.1/T3.2 bằng `scripts/vs done`.
2. Kho nước ngoài: thu thập ckd + acute_infect_tox, kiểm 12 nhóm, gộp → `scripts/vs done T2.6`.
3. T3.3 ghép: `$PY -m vnsoc.match.candidates` (ứng viên bằng mã, `configs/foreign_groups.yaml`) → agent counterpart-matcher
   xác nhận từng cặp; giá trị bản cũ theo chuỗi thay thế; mồi theo quy tắc; conflict_status.
4. Kiểm toán AI mẩu xung đột (thay HG3.5–HG3.7 theo quyết định người dùng; cần `scripts/vs waive` với xác nhận của
   chính người dùng — không tự tạo xác nhận) → T3.10–T3.12 đóng băng mẩu v1 (`/freeze atoms`).
5. T2.7 đóng băng kho hướng dẫn ngày **15/10/2026**.
6. R1.2b: kiểm bộ chấm 1.3.x trên tập giữ riêng (ngưỡng `gv_*` trong `configs/project.yaml`) rồi đóng băng bộ chấm.
7. T4.1 bộ câu hỏi (lấy mẫu D30) → T4.3 đóng băng câu hỏi + quy tắc chấm + addendum → hội đồng M2 (T4.6–T4.7).
8. P5 chạy 4 mô hình cục bộ (không API trả phí, không Kaggle — HG0.3/HG2.3/HG5.0) → P6 chấm + GLMM trong R → P7 bản thảo.
9. Mốc: slide + trình bày FMC 12/12/2026 (nếu được nhận); nộp tạp chí 11–24/1/2027.

## 6. Ghi nhớ quan trọng

- Máy chủ Ollama của đề tài: chạy `powershell -File scripts/ollama_d.ps1` trước mọi lần chạy mô hình (cổng 11435;
  `vnsoc.run.ollama_local` dùng `VNSOC_OLLAMA_URL`). Không đụng Ollama mặc định (cổng 11434, ổ C). Ổ D còn ~11 GB.
- Windows: `PYTHONUTF8=1`; giữ kiểu xuống dòng khi vá file (nhiều file LF, `docs/DECISIONS.md` CRLF); heredoc Bash làm hỏng
  dấu `\` → vá bằng script Python; hook chặn lệnh nhắc `state/.human_ack` và lệnh xóa trong state/dữ liệu.
- `results/numbers.json` chỉ ghi qua `vnsoc.numbers.put()` từ mã phân tích; văn bản dùng `{{khóa}}`; `make verify` trước khi
  báo xong bản thảo (hiện `main.md` còn thiếu khóa nghiên cứu chính — dự kiến).
- Ghi cho bài báo (từ kiểm toán abstract, `manuscript/TODO_manuscript.md` §6): mồi P-tbhiv-05 không hợp lệ (tập H1 còn 14
  mồi); mẫu số nhóm lệch phiên bản gồm ≥ 5 mẩu có giá trị cũ = mới; nêu cả kết quả trắc nghiệm và cấu hình mô hình.
- Văn bản dại 1622/2014 không lấy được từ nguồn chính thức (lỗi TLS; không tắt kiểm TLS) → kho không có họ bệnh dại.
- Ngân sách API: 0 USD đã dùng (không dùng API trả phí theo quyết định người dùng).
