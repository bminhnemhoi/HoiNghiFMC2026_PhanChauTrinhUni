---
name: review-panel
description: Tổ chức hội đồng phản biện agent ở các mốc M1–M4 (gói tài liệu, gọi 5 agent song song, tổng hợp điểm, tạo task sửa, giới hạn 2 vòng rồi chuyển người dùng quyết định).
---
# Hội đồng phản biện agent

## Gói tài liệu theo mốc (đưa đường dẫn cho agent, không dán nội dung)
- **M1** (sau thí điểm, trước khi nộp FMC): docs/01 §1–§5.7, `results/pilot/`, abstract FMC, `data/interim/pilot_atoms.jsonl`.
- **M2** (trước khi chạy chính — tuần 7): `data/frozen/atoms_v*`, `questions_v*`, `configs/grading*`, `prereg/submitted/` + addenda, báo cáo QC trích xuất/ghép, `review/adjudication_rubric.md`.
- **M3** (sau phân tích — tuần 11): `results/` (bảng, hình, numbers.json), `analysis_R/`, `src/vnsoc/analysis/`, docs/DECISIONS.md.
- **M4** (bản thảo — tuần 14): `manuscript/build/`, supplement, checklist TRIPOD-LLM, `manuscript/citations_verified.json`.

## Thủ tục
1. Tạo `review/<Mx>/`. Gọi song song 5 subagent (công cụ Agent, tên cũ Task): rev-editor, rev-clinician, rev-methods, rev-feasibility, rev-novelty; mỗi agent nhận: mốc, danh sách file, yêu cầu viết `review/<Mx>/<tên>.md` theo mẫu YAML trong định nghĩa agent. Không cho agent thấy báo cáo của nhau.
2. `$PY -m vnsoc.review <Mx>` → `review/<Mx>/summary.md`; ĐẠT khi không có lỗi chết người, không ai “reject”, điểm trung bình có trọng số ≥ 7,0 (trọng số: tầm quan trọng 20%, mới 20%, chặt 15%, khả thi 15%, Q1 15%, đúng yêu cầu 15%).
3. Mỗi yêu cầu **major** → một task `scripts/vs add --id R<m>.<k> --title "..." --depends <task mốc vòng 1, đã xong> --blocks <task chốt mốc> --acceptance "<acceptance của reviewer>"`; minor → gộp thành 1 task. Yêu cầu không làm → ghi lý do trong `review/<Mx>/response.md` (như mục 8.2 đề cương).
4. Task **chốt mốc** (ví dụ T4.7 cho M2, T6.9 cho M3, T7.9 cho M4) chỉ đủ điều kiện khi mọi task R đã xong. Nếu vòng 1 chưa ĐẠT: chạy vòng 2 vào `review/<Mx>_r2/` (cùng 5 agent, kèm `review/<Mx>/response.md` giải trình từng yêu cầu) rồi `$PY -m vnsoc.review <Mx>_r2`. Vẫn CẦN SỬA → `scripts/vs add --id HGM<m> --owner human --title "Quyết định sau hội đồng <Mx>" --instructions "<tóm tắt 2 lựa chọn, mỗi lựa chọn được gì mất gì>" --blocks <task chốt mốc>` (ví dụ HGM2 cho M2). Người dùng gõ `XONG HGM<m> <lựa chọn>`; bạn ghi quyết định vào `review/<Mx>/response.md` rồi `scripts/vs human-done HGM<m>`. `$PY -m vnsoc.check review <Mx>` chỉ qua khi hội đồng ĐẠT hoặc cổng này đã được người dùng xác nhận. Không chạy vòng 3.
5. Báo người dùng: kết luận, điểm, 3 yêu cầu lớn nhất, việc đã tạo.
6. M1 (hạn FMC) chỉ một vòng và không chặn việc nộp abstract: yêu cầu major của M1 thành task R1.* không chặn gì.
Lưu ý: hội đồng là AI. Kết quả của nó không thay cho giảng viên hướng dẫn hay bác sĩ thật (HG7.10) và không được mô tả trong bài báo như phản biện của người.
