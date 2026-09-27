# CLAUDE.md — vn-soc-audit

Dự án: **“Chuẩn điều trị của ai?”** — đo và truy nguồn sai lệch của LLM so với hướng dẫn chẩn đoán–điều trị hiện hành của Bộ Y tế Việt Nam (lệch theo chuẩn nước ngoài có tên, lệch theo bản Bộ Y tế cũ có tên), kèm lớp từ chối có chứng nhận. Người dùng: Bình Minh, sinh viên CNTT (TDTU), làm một mình với laptop + Kaggle 2×T4 + ≤ 40 USD API. Đích: abstract FMC 2026 (hạn 30/9/2026), bài Q1 (JMIR Medical Informatics / IJMI) nộp 11–24/1/2027.

## Tài liệu đầu vào (CHỈ ĐỌC — hook chặn sửa)
- `docs/01_DE_CUONG.md` — đề cương: câu hỏi, giả thuyết, dữ liệu, phương pháp, thống kê. Nguồn sự thật về *khoa học*.
- `docs/02_KE_HOACH_TRIEN_KHAI.md` — kế hoạch: pha, task (khối YAML), cổng người dùng (HG), quy tắc quyết định DR0–DR13. Nguồn sự thật về *việc cần làm*.
- `docs/03_PROMPT_CLAUDE_CODE.md` — prompt khởi tạo (đã dùng để dựng repo này).
Đừng nạp nguyên văn các file này vào ngữ cảnh; tìm đúng mục bằng Grep (ví dụ mã task `T3.2`, `DR4`, `§4.5`).

## Vòng làm việc
0. Phiên mới hoặc sau tạm dừng: đọc `docs/HANDOFF.md` (việc đã xong, việc dở kèm số đo, cách chạy tiếp workflow agent ở `scripts/workflows/`).
1. Trạng thái nằm ở `state/progress.json`, **chỉ thay đổi qua `scripts/vs`** (init/next/start/done/block/skip/add/human-done). Không sửa tay.
2. Mỗi lượt: `/next` → một task trọn vẹn: start → đọc task + mục liên quan → nạp skill/agent ghi trong task → viết mã + test → chạy → `scripts/vs done <ID>` (lệnh kiểm tra phải qua) → commit git → báo ngắn.
3. `scripts/vs done` thất bại: sửa và thử lại (tối đa 3 lần), sau đó `scripts/vs block <ID> --reason "..."` với lý do cụ thể và điều người dùng cần làm.
4. Hook Stop giữ bạn làm tiếp khi autopilot bật và còn task làm được. Khi chỉ còn việc của người dùng: tóm tắt `state/HUMAN_TODO.md` và dừng.
5. Kết thúc mỗi mốc (M1–M4 trong kế hoạch): `/review-panel Mx`.

## Cổng người dùng (human gates, mã HG…)
- Việc cần tài khoản, khóa, thanh toán, chữ ký, quyết định khoa học/pháp lý, liên hệ con người, nộp bài/đăng ký: **chỉ người dùng làm**. Bạn chuẩn bị mọi thứ (bản nháp, hướng dẫn từng bước, nội dung email) và ghi rõ trong task.
- Người dùng báo xong bằng một dòng BẮT ĐẦU bằng `XONG HG1.9 <thông tin>` trong chat. Hook tạo xác nhận; bạn ghi bằng chứng họ đưa (URL OSF, mã nộp FMC...) vào file `outputs` của task, rồi `scripts/vs human-done HG1.9 --note "..."`.
- Không bao giờ tự tạo xác nhận, không đóng vai người dùng, không nói việc của người dùng đã xong khi họ chưa nói.

## Quy tắc cứng (vi phạm = hỏng công trình)
1. **Không bịa**: không bịa trích dẫn, số trang, giá trị, kết quả, số liệu, DOI, tên bài. Không biết → ghi “chưa rõ”, để ô `[ ]`, hoặc block task. Mọi giá trị hướng dẫn phải có trích nguyên văn + số trang từ PDF chính thức (`span_verified`).
2. **Số trong bài báo/abstract/slide** chỉ qua registry: mã phân tích gọi `vnsoc.numbers.put()`, văn bản dùng `{{khóa}}`; hằng số thiết kế viết `{{=0,10}}` (số đó phải có trong `configs/*.yaml`); hàm `put()` chỉ nhận lời gọi từ `src/vnsoc/analysis/`, `analysis_R/`, `scripts/analysis/`. `make verify` phải qua trước khi báo xong bản thảo.
3. **Trích dẫn** chỉ khi đã kiểm bằng `scripts/verify_citations.py` (Crossref/DataCite/arXiv) hoặc người dùng xác nhận (luật, quyết định).
4. **Đăng ký trước** (OSF, HG2.9): phân tích xác nhận làm đúng như đã đăng ký. Lệch → ghi `docs/DECISIONS.md` + addendum `prereg/addenda/` + báo người dùng. Phân tích thêm ghi rõ “khám phá”.
5. **Đóng băng**: kho hướng dẫn ngày 15/10/2026; mẩu v1 và bộ câu hỏi v1 + quy tắc chấm đóng băng **trước** khi chạy mô hình chính. Không xem đầu ra mô hình khi sửa quy tắc chấm hay bộ câu hỏi. Dữ liệu đóng băng nằm ở `data/frozen/` kèm `SHA256SUMS` và không bị sửa.
6. **Agent phản biện không phải người**: `rev-clinician` là AI đóng vai bác sĩ. Không bao giờ viết “bác sĩ đã duyệt” trừ khi HG3.9 (bác sĩ thật) đã xong với kết quả có bác sĩ; trong bài báo chỉ nêu người thật.
7. **Pháp lý**: không truy cập tự động thuvienphapluat.vn (hook chặn); chỉ lấy văn bản từ nguồn chính thức (kcb.vn, moh.gov.vn, trang Sở Y tế/bệnh viện); không phát hành lại toàn văn; hướng dẫn nước ngoài (ADA, ESC, AHA, GINA, GOLD…) chỉ lưu và công bố *giá trị + trích dẫn + vị trí*, không lưu đoạn văn; dataset/kernel Kaggle để riêng tư.
8. **Ngân sách**: API trả phí chỉ qua `vnsoc.run.api_batch` (tự đặt trước và trừ vào sổ `state/budget_ledger.csv`, trần cứng 40 USD). Kaggle GPU 50–80 giờ cho cả dự án: ghi giờ mỗi job vào `docs/LOG.md`. Thử nhỏ trước khi chạy lớn.
9. **Bí mật**: không đọc `.env`, `~/.kaggle/kaggle.json`; không in biến môi trường; mã Python tự nạp `.env` bằng python-dotenv.
10. **Trung thực với người dùng**: báo thẳng khi hỏng, bị chặn, thiếu dữ liệu, kết quả âm tính hoặc trái giả thuyết. Kết quả âm tính vẫn là kết quả; không “chỉnh” phân tích cho đẹp.

## Quy ước kỹ thuật
- Python ≥ 3.10, gói `src/vnsoc/`; chạy bằng `.venv/bin/python` (hoặc `$PY`). Mọi hàm biến đổi dữ liệu có test trong `tests/`. `make test` phải xanh trước khi `done`.
- Dữ liệu: JSONL cho manifest/atoms/questions (kiểm bằng `$PY -m vnsoc.schemas <kind> <file>`), JSONL.gz cho đầu ra chạy mô hình, Parquet cho bảng phân tích. Tên file có phiên bản: `atoms_v1.jsonl`.
- Script idempotent, có `--dry-run` khi tốn tiền/GPU, cố định seed, ghi log vào `logs/`.
- Thống kê xác nhận (GLMM) viết bằng R (`analysis_R/`), phần còn lại Python. Hình: matplotlib, lưu PDF + PNG ở `results/figures/`.
- Git: repo cục bộ; commit sau mỗi task (`T3.2: …`). Không push trừ khi người dùng cấu hình remote và yêu cầu.

## Bản đồ thư mục
`configs/` hằng số đăng ký trước, mô hình, điều kiện, chấm, ngân sách · `data/raw` PDF gốc (không commit) · `data/interim` trung gian · `data/frozen` bản đóng băng · `data/runs` đầu ra mô hình · `results/` bảng, hình, `numbers.json` · `manuscript/` bài báo (placeholder) · `prereg/` OSF · `review/` báo cáo hội đồng · `kaggle/` runner · `analysis_R/` · `state/` trạng thái · `docs/DECISIONS.md`, `docs/LOG.md`.

## Agent, skill, lệnh
- Agent (`.claude/agents/`): corpus-librarian, atom-extractor, counterpart-matcher, question-writer, run-orchestrator, grader, statistician, manuscript-writer, lit-scout, integrity-auditor; hội đồng phản biện rev-editor, rev-clinician, rev-methods, rev-feasibility, rev-novelty. Giao việc đọc/tra cứu nhiều cho agent để giữ ngữ cảnh gọn; agent ghi kết quả ra file, trả về tóm tắt.
- Skill (`.claude/skills/`): corpus-acquisition, vn-number-normalization, atomization-protocol, counterpart-matching, question-generation, kaggle-vllm-runner, api-batch-runner, grading-protocol, statistics-plan, certified-abstention, citation-verification, tripod-llm-manuscript, human-gate-protocol, review-panel.
- Lệnh: `/next`, `/status`, `/gate`, `/review-panel Mx`, `/freeze <corpus|atoms|questions>`, `/verify`, `/pause`, `/resume`, `/autopilot on|off`.

## Giao tiếp
Nói với người dùng bằng tiếng Việt, ngắn, cụ thể (việc đã xong, số liệu lấy từ file, việc tiếp theo, việc họ cần làm kèm hạn). Bài báo, supplement, thư nộp bằng tiếng Anh; abstract và slide FMC bằng tiếng Việt.
