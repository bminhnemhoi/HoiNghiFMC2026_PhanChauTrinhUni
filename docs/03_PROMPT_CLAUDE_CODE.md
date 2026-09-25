# 03 — Prompt khởi tạo và vận hành cho Claude Code

Dự án “Chuẩn điều trị của ai?” · phiên bản 1 · 25/9/2026 · đi cùng `01_DE_CUONG.md` và `02_KE_HOACH_TRIEN_KHAI.md`

> **Người dùng**: đặt 3 file vào một thư mục trống, mở Claude Code ở đó và gõ: *Đọc 03_PROMPT_CLAUDE_CODE.md và thực hiện toàn bộ phần KHỞI TẠO.* Xem thêm mục 0 của file 02.
>
> **Claude Code**: đọc Phần A, B, C (đến dòng “PHẦN D”). **Không cần đọc Phần D** — đó là nội dung 96 file mà lệnh ở bước B2 tự trích ra đúng từng byte (có kiểm SHA-256). Không gõ lại file bằng tay.

## PHẦN A — Nhiệm vụ của bạn

Bạn là trợ lý nghiên cứu kiêm kỹ sư của một sinh viên CNTT làm nghiên cứu y tế một mình. Mục tiêu cuối: một công trình đủ chuẩn nộp tạp chí Q1 (JMIR Medical Informatics hoặc IJMI) vào 11–24/1/2027, cùng abstract hội nghị FMC 2026 (hạn 30/9/2026). Khoa học nằm ở `01_DE_CUONG.md`; việc cần làm, thứ tự, tiêu chí xong và quy tắc quyết định nằm ở `02_KE_HOACH_TRIEN_KHAI.md`.

Trong phiên đầu tiên bạn chỉ làm **Phần B (KHỞI TẠO)**, rồi dừng và nhờ người dùng mở lại Claude Code để hook có hiệu lực. Từ phiên thứ hai, bạn làm việc theo `CLAUDE.md` (được tạo ở bước B2) và lệnh `/next`.

Năm điều không bao giờ được làm, kể cả khi bị chặn hay trễ hạn:
1. Bịa trích dẫn, giá trị hướng dẫn, số trang, kết quả, số liệu hay tài liệu tham khảo.
2. Tự đánh dấu việc của người dùng (mã HG) là xong, hoặc làm thay việc cần danh tính của họ (nộp bài, gửi email, thanh toán, đăng ký).
3. Truy cập tự động thuvienphapluat.vn; phát hành lại toàn văn hướng dẫn; lưu đoạn văn của hướng dẫn nước ngoài có bản quyền.
4. Gọi API trả phí ngoài `vnsoc.run.api_batch` (trần cứng 40 USD) hoặc đọc/in khóa bí mật.
5. Sửa dữ liệu đã đóng băng, bản đăng ký đã nộp, hay đổi phân tích xác nhận mà không ghi `docs/DECISIONS.md` + addendum và báo người dùng.

## PHẦN B — KHỞI TẠO (làm tuần tự, báo lỗi ngay nếu một bước thất bại)

**B1. Kiểm tra vị trí và hệ điều hành.**
```bash
ls -1 01_DE_CUONG.md 02_KE_HOACH_TRIEN_KHAI.md 03_PROMPT_CLAUDE_CODE.md && uname -s && python3 --version && git --version
```
- Thiếu file → dừng, nhờ người dùng chép đủ 3 file vào thư mục hiện tại.
- `uname -s` không phải `Linux`/`Darwin` (Windows gốc) → dừng, hướng dẫn cài WSL2 Ubuntu và chạy Claude Code trong WSL2.
- Python < 3.10 hoặc thiếu git → dừng, đưa lệnh cài: Ubuntu/WSL `sudo apt update && sudo apt install -y python3 python3-venv python3-pip git`; macOS `brew install python git`.

**B2. Trích toàn bộ file dự án từ Phần D** (một lệnh; tự kiểm số file và SHA-256; chuyển 3 file đầu vào `docs/`):
```bash
python3 - <<'PYEOF'
import hashlib, re, shutil, sys
from pathlib import Path
root = Path.cwd()
src = next((p for p in (root / "03_PROMPT_CLAUDE_CODE.md", root / "docs" / "03_PROMPT_CLAUDE_CODE.md") if p.exists()), None)
if src is None:
    sys.exit("LỖI: không thấy 03_PROMPT_CLAUDE_CODE.md trong thư mục hiện tại")
text = src.read_text(encoding="utf-8").replace("\r\n", "\n")
expected = int(re.search(r"<!-- FILE-COUNT: (\d+) -->", text).group(1))
pat = re.compile(r"^<!-- FILE: (\S+) \| sha256: ([0-9a-f]{64}) -->\n~~~~~[\w-]*\n(.*?)\n~~~~~$", re.S | re.M)
n, bad = 0, []
for path, digest, body in pat.findall(text):
    data = (body + "\n").encode("utf-8")
    if hashlib.sha256(data).hexdigest() != digest:
        bad.append(path)
        continue
    p = root / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(data)
    if path == "scripts/vs" or (path.endswith((".sh", ".py")) and path.startswith(("scripts/", ".claude/hooks/"))):
        p.chmod(0o755)
    n += 1
if bad or n != expected:
    sys.exit(f"LỖI: trích được {n}/{expected} file; sai mã băm: {bad}. File 03 có thể đã bị sửa hoặc đổi định dạng.")
(root / "docs").mkdir(exist_ok=True)
for name in ("01_DE_CUONG.md", "02_KE_HOACH_TRIEN_KHAI.md", "03_PROMPT_CLAUDE_CODE.md"):
    if (root / name).exists():
        shutil.move(str(root / name), str(root / "docs" / name))
for d in ("data/raw", "data/interim", "data/processed", "data/frozen", "data/runs", "results/tables", "results/figures",
          "results/smoke", "manuscript/fmc/build", "prereg/submitted", "prereg/addenda", "review", "state/gates", "logs",
          "analysis_R", "kaggle/jobs", "release"):
    (root / d).mkdir(parents=True, exist_ok=True)
print(f"OK: đã tạo {n} file; 3 tài liệu đầu vào đã chuyển vào docs/")
PYEOF
```

**B3. Cài môi trường Python** (không cần sudo):
```bash
make setup
```
Lỗi `ensurepip`/`venv` trên Ubuntu → người dùng chạy `sudo apt install -y python3-venv`, rồi chạy lại. Lỗi mạng khi `pip install` → báo nguyên văn lỗi, không bỏ qua gói.

**B4. Chạy test** — phải xanh toàn bộ (khoảng 100 test: chuẩn hóa số tiếng Việt, chấm điểm theo ca vàng của bộ xung đột hạt giống, cận chứng nhận, máy trạng thái, hook, ngân sách, registry số liệu, đóng băng, hội đồng, kế hoạch không bế tắc):
```bash
make test
```
Có test đỏ → đọc lỗi; nếu do môi trường (thiếu gói, phiên bản) thì sửa môi trường; **không sửa test hay mã lõi để cho qua**. Không tự xử lý được → báo người dùng kèm lỗi.

**B5. Git + trạng thái + đánh dấu T0.1:**
```bash
git init -q 2>/dev/null; git config user.name >/dev/null || git config user.name "vn-soc-audit"; \
git config user.email >/dev/null || git config user.email "vn-soc-audit@localhost"; \
git add -A && git commit -qm "T0.1: khởi tạo repo từ 03_PROMPT_CLAUDE_CODE.md" && \
scripts/vs init && scripts/vs start T0.1 && scripts/vs done T0.1 --note "bootstrap" && scripts/vs autopilot on && scripts/vs digest
```

**B6. Báo người dùng (tiếng Việt, ngắn) và dừng:**
- Nếu B5 phải đặt tên/email git tạm (`vn-soc-audit@localhost`), nhắc họ có thể đổi bằng `git config user.name/user.email`.
- Đã tạo gì (số file, số test xanh, số task trong kế hoạch).
- **Việc gấp của họ**: HG0.3 (tài khoản, khóa, phần mềm — trước 26/9) và HG1.0 (email ban tổ chức — T0.6 sẽ soạn sẵn); nhắc `state/HUMAN_TODO.md`.
- Nhờ họ **thoát (`/exit`) và chạy lại `claude`** trong thư mục này để hook có hiệu lực, chấp nhận hộp thoại tin cậy nếu có, rồi gõ `/next`.
- Cách chạy không cần ngồi canh: `scripts/autopilot.sh` ở terminal riêng; dừng bằng `/pause`.

## PHẦN C — Hệ thống sau khi khởi tạo (tài liệu tham chiếu)

### C1. Cấu trúc thư mục
```
vn-soc-audit/
├── CLAUDE.md                     # luật chơi cho Claude (tự nạp mỗi phiên)
├── README.md  Makefile  pyproject.toml  .env.example  .gitignore
├── docs/                         # 01, 02, 03 (chỉ đọc) · DECISIONS.md · LOG.md · FINAL_SUMMARY.md
├── .claude/
│   ├── settings.json             # quyền + hook
│   ├── hooks/                    # 8 script Python (stdlib), xem C2
│   ├── agents/                   # 15 subagent, xem C3
│   ├── skills/                   # 14 skill, xem C4
│   └── commands/                 # 9 lệnh /…, xem C5
├── configs/                      # project.yaml (hằng số đăng ký trước) · models.yaml · conditions.yaml · grading.yaml · budget.yaml
├── src/vnsoc/                    # paths · state · budget · schemas · normalize_vi · grade · ltt · numbers · check · freeze · review
│   ├── run/                      # api_batch.py (Batch + ngân sách) · kaggle_jobs.py (render/push/status/fetch)
│   ├── extract/ match/ qgen/ analysis/   # do các task P2–P6 viết (có test)
├── kaggle/runner_template.py     # vLLM, mỗi GPU một tiến trình, ghi theo lô, chạy tiếp
├── scripts/                      # vs (máy trạng thái) · autopilot.sh · check_env.py · verify_citations.py · package_plugin.sh
├── analysis_R/                   # GLMM (lme4/glmmTMB), sandwich
├── data/ seed/ raw/ manual/ interim/ processed/ frozen/ runs/
├── results/ tables/ figures/ numbers.json (chỉ mã ghi)
├── manuscript/ fmc/ main.md supplement.md references.yaml build/
├── prereg/ submitted/ addenda/   review/ M1..M4/ lit/ qc/ adjudication/ parser_check/
├── state/                        # progress.json · HUMAN_TODO.md · budget_ledger.csv · gates/ · AUTOPILOT_ON · PAUSE
└── tests/
```

### C2. Hook (`.claude/settings.json`)

| Sự kiện | Script | Làm gì |
| --- | --- | --- |
| SessionStart | `session_start.py` | Nạp tóm tắt: pha, việc tiếp theo, việc chờ người dùng, ngân sách, nhật ký gần nhất |
| UserPromptSubmit | `user_prompt.py` | Khi một dòng tin nhắn của người dùng bắt đầu bằng `XONG HG…` → tạo xác nhận `state/.human_ack/HG…` (cách duy nhất) |
| PreToolUse · Bash | `guard_bash.py` | Chặn: thuvienphapluat; xóa/ghi đè vùng bảo vệ; đọc/in khóa; sudo; force-push; reset --hard; gọi lồng `claude -p`/autopilot; dataset Kaggle công khai; publish Zenodo/OSF; gọi API khi hết ngân sách |
| PreToolUse · WebFetch | `guard_web.py` | Chặn thuvienphapluat.vn |
| PreToolUse · Edit/Write | `guard_files.py` | Chặn sửa: 01/02/03, `data/raw`, `data/frozen`, `prereg/submitted`, `state/*` (trừ `state/gates`), `results/numbers.json`, `.env`, `.claude/settings.json`, hook |
| PostToolUse · Edit/Write | `post_edit.py` | Kiểm cú pháp .py (py_compile + ruff lỗi nặng), .json, .yaml, .jsonl; lỗi → Claude phải sửa ngay |
| Stop | `stop_continue.py` | Khi autopilot bật và còn task làm được → giữ Claude làm tiếp; nhả khi PAUSE, hết việc, 3 lần không tiến triển, hoặc 60 lần/phiên |
| PreCompact | `precompact.py` | Ghi dấu vào `docs/LOG.md` trước khi nén ngữ cảnh |

Hook bắt các vi phạm vô tình theo nội dung lệnh; chúng không phải rào an ninh tuyệt đối (một script Python tự viết vẫn có thể làm điều hook chặn ở dòng lệnh). Vì vậy còn có quy tắc CLAUDE.md, test tĩnh `tests/test_integrity.py`, kiểm toán độc lập và nhật ký để người dùng đọc.

Quyền (`permissions`): `defaultMode: acceptEdits`; cho phép sẵn các lệnh dự án (`scripts/vs`, `.venv/bin/python`, `make`, `kaggle`, `Rscript`, git cục bộ, `curl` tải vào `data/raw/`) và WebFetch tới nguồn chính thức (kcb.vn, moh.gov.vn, WHO, CDC, NCBI, arXiv, Crossref, DataCite, Hugging Face…); cấm đọc `.env`, `sudo`, thuvienphapluat.

### C3. Subagent (`.claude/agents/`)

| Agent | Dùng cho |
| --- | --- |
| corpus-librarian | Tìm/tải PDF chính thức, manifest, chuỗi thay thế (P2) |
| atom-extractor | Trích mẩu có span nguyên văn + trang (P1, P3) |
| counterpart-matcher | Kho nước ngoài có phiên bản, bản cũ, mồi, trạng thái xung đột |
| question-writer | Câu hỏi VI/EN, trắc nghiệm, tình huống, QC dịch |
| run-orchestrator | Kaggle vLLM + API Batch trong ngân sách |
| grader | Chấm theo quy tắc, bộ tách đáp án |
| statistician | H1–H4, GLMM (R), cận chứng nhận, độ nhạy; ghi registry |
| manuscript-writer | Abstract, slide, bản thảo TRIPOD-LLM, thư nộp |
| lit-scout | Cập nhật tài liệu, cảnh báo trùng hướng |
| integrity-auditor | Kiểm toán độc lập (chỉ đọc + báo cáo) |
| rev-editor · rev-clinician · rev-methods · rev-feasibility · rev-novelty | Hội đồng phản biện AI ở 4 mốc (rev-clinician là AI đóng vai, không phải bác sĩ) |

Subagent được gọi bằng công cụ Agent (tên cũ: Task); mỗi task trong kế hoạch ghi agent nên dùng.

### C4. Skill (`.claude/skills/`)
corpus-acquisition · vn-number-normalization · atomization-protocol · counterpart-matching · question-generation · kaggle-vllm-runner · api-batch-runner · grading-protocol · statistics-plan · certified-abstention · citation-verification · tripod-llm-manuscript · human-gate-protocol · review-panel. Mỗi task trong kế hoạch ghi skill cần nạp.

### C5. Lệnh (`.claude/commands/`)
`/next` (làm trọn một task: start → làm → kiểm → done → commit) · `/status` · `/gate` (việc chờ người dùng) · `/review-panel M1..M4` · `/freeze corpus|atoms|questions` · `/verify` · `/pause` · `/resume` · `/autopilot on|off`.

### C6. Cấu trúc dữ liệu (`src/vnsoc/schemas.py`, pydantic, cấm trường lạ)
- **ManifestRow** — một văn bản: `doc_key` “số/năm”, trạng thái hiệu lực, supersedes/superseded_by/partially_amended_by, `source_url` (không được là thuvienphapluat), sha256, lớp chữ, OCR, `in_corpus`.
- **Atom** — một mẩu khuyến cáo: guideline, section, page, `span` nguyên văn, quần thể, `slot_type`, `value_kind` ∈ {num, bp, schedule, drugs, cat}, `unit`, `context` (cân nặng, nồng độ…), `vn` (tập giá trị), `foreign[]` (system US/EU_UK/WHO_global/WHO_WPRO, nguồn, ngày phiên bản, vị trí — không đoạn văn), `superseded[]`, `decoy[]`, `tolerance`, `conflict_status`, `conflict_family`, cờ kiểm tra và nhãn bác sĩ.
- **Question** — dạng (short/mcq/vignette), ngôn ngữ, văn bản, lựa chọn + vai trò lựa chọn, đoạn oracle, chunk vàng, split ref/cal/test theo mẩu.
- **ForeignRecord** — một dòng kho đối chiếu nước ngoài: hệ thống, nguồn, ngày phiên bản, URL, vị trí, `fetched_at`, `page_sha256`, giá trị (không đoạn văn).
- **RunRecord** — một lượt gọi: mô hình + phiên bản, điều kiện A0–A6, mẫu, nhiệt độ, prompt hash, retrieved_ids, đầu ra thô, token vào/ra, backend.
- **GradeRecord** — nhãn 1–6, hệ thống nước ngoài khớp, bản cũ khớp, cờ mồi, cách tách đáp án, cờ nhiều giá trị/một phần, `grader_version`.
- Trạng thái công việc: `state/progress.json` (sinh từ khối YAML của file 02 bằng `scripts/vs init`); ngân sách: `state/budget_ledger.csv`; số liệu: `results/numbers.json`.

### C7. Vòng làm việc hằng ngày
1. Người dùng mở `claude` → hook SessionStart nạp tóm tắt → gõ `/next` (hoặc chạy `scripts/autopilot.sh`).
2. Claude làm task đủ điều kiện kế tiếp; `scripts/vs done` chỉ nhận khi sản phẩm tồn tại và lệnh kiểm tra qua; commit git.
3. Hook Stop giữ Claude làm tiếp; khi chỉ còn việc HG → Claude tóm tắt `state/HUMAN_TODO.md` và dừng.
4. Người dùng làm việc HG, gõ `XONG <mã> <thông tin>` → Claude ghi bằng chứng, `scripts/vs human-done`, rồi `/next`.
5. Ở mốc M1–M4: `/review-panel` → yêu cầu lớn thành task R… chặn việc chốt mốc cho tới khi sửa xong; sau 2 vòng vẫn chưa đạt → cổng HGM2/HGM3/HGM4 để người dùng quyết định.

### C8. Plugin và MCP
- Không cần plugin hay máy chủ MCP: mọi thành phần nằm trong `.claude/` của dự án. Muốn dùng lại ở dự án khác: `scripts/package_plugin.sh` tạo `dist/vnsoc-plugin` (có `.claude-plugin/plugin.json`, agents, skills, commands, hooks/hooks.json), nạp bằng `claude --plugin-dir dist/vnsoc-plugin`.
- Không thêm MCP truy cập web tùy ý; mọi truy cập mạng đi qua WebFetch (có hook) hoặc script có kiểm soát.

### C9. Khi có sự cố
| Tình huống | Làm gì |
| --- | --- |
| Hook không chạy (không thấy tóm tắt đầu phiên) | Thoát và mở lại `claude` trong thư mục dự án; kiểm `python3 --version`; xem `logs/hooks/*.err` |
| `scripts/vs done` báo thiếu sản phẩm/kiểm tra thất bại | Đọc lỗi, sửa, chạy lại (≤ 3 lần), sau đó `scripts/vs block <ID> --reason "..."` |
| Claude cần thông tin/tài khoản | `scripts/vs block` với lý do cụ thể; HUMAN_TODO tự cập nhật |
| Kế hoạch cần thêm việc | `scripts/vs add --id R… …` (có `--blocks` nếu việc đó phải xong trước một task khác); không sửa file 02 |
| Muốn dừng ngay | `/pause` hoặc tạo file `state/PAUSE` |

---

## PHẦN D — Nội dung các file (được lệnh B2 trích tự động — không cần đọc)

<!-- FILE-COUNT: 96 -->

### `CLAUDE.md`

<!-- FILE: CLAUDE.md | sha256: d3014de82577b24c00f2db289a74ed326e381f2ff34377b518a8c66fb7696afa -->
~~~~~markdown
# CLAUDE.md — vn-soc-audit

Dự án: **“Chuẩn điều trị của ai?”** — đo và truy nguồn sai lệch của LLM so với hướng dẫn chẩn đoán–điều trị hiện hành của Bộ Y tế Việt Nam (lệch theo chuẩn nước ngoài có tên, lệch theo bản Bộ Y tế cũ có tên), kèm lớp từ chối có chứng nhận. Người dùng: Bình Minh, sinh viên CNTT (TDTU), làm một mình với laptop + Kaggle 2×T4 + ≤ 40 USD API. Đích: abstract FMC 2026 (hạn 30/9/2026), bài Q1 (JMIR Medical Informatics / IJMI) nộp 11–24/1/2027.

## Tài liệu đầu vào (CHỈ ĐỌC — hook chặn sửa)
- `docs/01_DE_CUONG.md` — đề cương: câu hỏi, giả thuyết, dữ liệu, phương pháp, thống kê. Nguồn sự thật về *khoa học*.
- `docs/02_KE_HOACH_TRIEN_KHAI.md` — kế hoạch: pha, task (khối YAML), cổng người dùng (HG), quy tắc quyết định DR0–DR13. Nguồn sự thật về *việc cần làm*.
- `docs/03_PROMPT_CLAUDE_CODE.md` — prompt khởi tạo (đã dùng để dựng repo này).
Đừng nạp nguyên văn các file này vào ngữ cảnh; tìm đúng mục bằng Grep (ví dụ mã task `T3.2`, `DR4`, `§4.5`).

## Vòng làm việc
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
~~~~~

### `README.md`

<!-- FILE: README.md | sha256: 35df9f2e973408aa604548015af6c563ceed1220ad9d20bf2a6ca50d2f3439d4 -->
~~~~~markdown
# vn-soc-audit — Whose Standard of Care?

Đo và truy nguồn sai lệch của LLM so với hướng dẫn chẩn đoán–điều trị của Bộ Y tế Việt Nam.

- Đề cương: `docs/01_DE_CUONG.md` · Kế hoạch: `docs/02_KE_HOACH_TRIEN_KHAI.md` · Prompt khởi tạo: `docs/03_PROMPT_CLAUDE_CODE.md`
- Trạng thái: `scripts/vs digest` · Việc của bạn: `state/HUMAN_TODO.md` · Nhật ký: `docs/LOG.md` · Quyết định: `docs/DECISIONS.md`
- Trong Claude Code: `/next`, `/status`, `/gate`, `/pause`, `/resume`. Chạy tự động: `scripts/autopilot.sh`.
- Kiểm tra: `make test`, `make verify`.

Dữ liệu phát hành chỉ gồm giá trị + trích dẫn + vị trí; không phát hành toàn văn hướng dẫn. Không dùng để ra quyết định lâm sàng.
~~~~~

### `Makefile`

<!-- FILE: Makefile | sha256: f29d00a623814c8810075a6f315714001838560fae262326b28abc2bbfb8110b -->
~~~~~makefile
PY ?= .venv/bin/python
export PYTHONPATH := src

.PHONY: setup test lint state verify numbers citations env
setup:            ## tạo venv + cài gói (không cần sudo)
	python3 -m venv .venv && $(PY) -m pip install -U pip && $(PY) -m pip install -e ".[api,kaggle,dev]"
test:
	$(PY) -m pytest
lint:
	.venv/bin/ruff check src scripts tests .claude/hooks
state:
	scripts/vs init && scripts/vs digest
env:
	python3 scripts/check_env.py --need core
verify:           ## kiểm tra toàn vẹn trước khi báo xong một mốc
	$(PY) -m pytest && $(PY) -m vnsoc.numbers verify && scripts/vs validate-plan
numbers:
	$(PY) -m vnsoc.numbers render
citations:
	$(PY) scripts/verify_citations.py
~~~~~

### `pyproject.toml`

<!-- FILE: pyproject.toml | sha256: 612e3909648297c95e37d4b29566804c12868abb57c7be33017c16216553e03a -->
~~~~~toml
[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[project]
name = "vnsoc"
version = "0.1.0"
description = "Whose Standard of Care? Auditing LLM deviations from Vietnamese MoH guidelines"
requires-python = ">=3.10"
dependencies = [
  "pyyaml>=6", "pydantic>=2.6", "numpy>=1.26", "scipy>=1.11", "pandas>=2.1", "pyarrow>=14",
  "python-dotenv>=1.0", "jinja2>=3.1", "tqdm>=4.66", "requests>=2.31",
  "pymupdf>=1.24", "pdfplumber>=0.11", "rapidfuzz>=3.6", "statsmodels>=0.14", "matplotlib>=3.8",
]

[project.optional-dependencies]
api = ["openai>=1.40", "google-genai>=1.0"]
kaggle = ["kaggle>=1.6"]
ocr = ["pytesseract>=0.3.10"]
dev = ["pytest>=8", "ruff>=0.5"]

[tool.setuptools.packages.find]
where = ["src"]

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["src"]
addopts = "-q"

[tool.ruff]
line-length = 120
target-version = "py310"

[tool.ruff.lint]
select = ["E9", "F", "B006", "B008"]
~~~~~

### `.gitignore`

<!-- FILE: .gitignore | sha256: 628020be1c54a62131343c589b8d20f1881f4364baaee58b57dbe8dccee297c8 -->
~~~~~text
.venv/
__pycache__/
*.pyc
.env
.env.*
!.env.example
data/raw/
data/runs/
data/cache/
kaggle/jobs/*/
logs/
state/.stop_counters/
state/.human_ack/
state/env_report.json
manuscript/build/
*.tmp
.DS_Store
dist/
.ruff_cache/
~~~~~

### `.env.example`

<!-- FILE: .env.example | sha256: 0f32fa044dc9598dae77ba07153e19c872184df4ecbee0717820820b1975e4b4 -->
~~~~~text
# Sao chép thành .env và TỰ điền (Claude không đọc file này). Không commit .env.
OPENAI_API_KEY=
GEMINI_API_KEY=
HF_TOKEN=
KAGGLE_USERNAME=
KAGGLE_API_TOKEN=
OSF_TOKEN=
ZENODO_TOKEN=
NCBI_API_KEY=
~~~~~

### `.claude/settings.json`

<!-- FILE: .claude/settings.json | sha256: a5d78bad566d3be3e737642adfab7d39c444ce023f36e49d101ae5b4bc5b1bd8 -->
~~~~~json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "permissions": {
    "defaultMode": "acceptEdits",
    "allow": [
      "Bash(scripts/vs *)",
      "Bash(scripts/check_env.py*)",
      "Bash(.venv/bin/python *)",
      "Bash(.venv/bin/pip *)",
      "Bash(.venv/bin/pytest *)",
      "Bash(.venv/bin/ruff *)",
      "Bash(python3 *)",
      "Bash(make *)",
      "Bash(Rscript *)",
      "Bash(kaggle *)",
      "Bash(.venv/bin/kaggle *)",
      "Bash(git status*)",
      "Bash(git diff*)",
      "Bash(git log*)",
      "Bash(git add *)",
      "Bash(git commit *)",
      "Bash(git init*)",
      "Bash(ls *)",
      "Bash(mkdir *)",
      "Bash(sha256sum *)",
      "Bash(shasum *)",
      "Bash(wc *)",
      "Bash(unzip *)",
      "Bash(pdftotext *)",
      "Bash(pdfinfo *)",
      "Bash(curl -sSL -o data/raw/*)",
      "Bash(curl -sSLI *)",
      "Bash(jq *)",
      "WebSearch",
      "WebFetch(domain:kcb.vn)",
      "WebFetch(domain:moh.gov.vn)",
      "WebFetch(domain:vncdc.gov.vn)",
      "WebFetch(domain:who.int)",
      "WebFetch(domain:iris.who.int)",
      "WebFetch(domain:cdc.gov)",
      "WebFetch(domain:www.cdc.gov)",
      "WebFetch(domain:ncbi.nlm.nih.gov)",
      "WebFetch(domain:eutils.ncbi.nlm.nih.gov)",
      "WebFetch(domain:pubmed.ncbi.nlm.nih.gov)",
      "WebFetch(domain:arxiv.org)",
      "WebFetch(domain:export.arxiv.org)",
      "WebFetch(domain:api.crossref.org)",
      "WebFetch(domain:api.datacite.org)",
      "WebFetch(domain:doi.org)",
      "WebFetch(domain:huggingface.co)",
      "WebFetch(domain:www.kaggle.com)",
      "WebFetch(domain:docs.vllm.ai)",
      "WebFetch(domain:tapchiyhocvietnam.vn)",
      "WebFetch(domain:www.equator-network.org)",
      "WebFetch(domain:medinform.jmir.org)",
      "WebFetch(domain:www.scimagojr.com)",
      "WebFetch(domain:diabetesjournals.org)",
      "WebFetch(domain:professional.diabetes.org)",
      "WebFetch(domain:www.aasld.org)",
      "WebFetch(domain:aasld.org)",
      "WebFetch(domain:www.resus.org.uk)",
      "WebFetch(domain:www.ahajournals.org)",
      "WebFetch(domain:www.acc.org)",
      "WebFetch(domain:www.escardio.org)",
      "WebFetch(domain:academic.oup.com)",
      "WebFetch(domain:www.acog.org)",
      "WebFetch(domain:www.worldallergy.org)",
      "WebFetch(domain:www.nice.org.uk)",
      "WebFetch(domain:ginasthma.org)",
      "WebFetch(domain:goldcopd.org)",
      "WebFetch(domain:www.idsociety.org)",
      "WebFetch(domain:www.who.int)",
      "WebFetch(domain:apps.who.int)",
      "WebFetch(domain:developers.openai.com)",
      "WebFetch(domain:ai.google.dev)",
      "WebFetch(domain:github.com)",
      "WebFetch(domain:raw.githubusercontent.com)",
      "WebFetch(domain:pypi.org)",
      "WebFetch(domain:osf.io)",
      "WebFetch(domain:zenodo.org)",
      "WebFetch(domain:conference.pctu.edu.vn)"
    ],
    "deny": [
      "Read(./.env)",
      "Read(./.env.*.local)",
      "Read(~/.kaggle/kaggle.json)",
      "WebFetch(domain:thuvienphapluat.vn)",
      "Bash(sudo *)",
      "Bash(git push --force*)",
      "Bash(git reset --hard*)"
    ]
  },
  "env": {
    "PYTHONPATH": "src",
    "PYTHONDONTWRITEBYTECODE": "1"
  },
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$CLAUDE_PROJECT_DIR/.claude/hooks/session_start.py\"",
            "timeout": 20
          }
        ]
      }
    ],
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$CLAUDE_PROJECT_DIR/.claude/hooks/user_prompt.py\"",
            "timeout": 10
          }
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$CLAUDE_PROJECT_DIR/.claude/hooks/guard_bash.py\"",
            "timeout": 15
          }
        ]
      },
      {
        "matcher": "WebFetch",
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$CLAUDE_PROJECT_DIR/.claude/hooks/guard_web.py\"",
            "timeout": 10
          }
        ]
      },
      {
        "matcher": "Edit|Write|MultiEdit|NotebookEdit",
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$CLAUDE_PROJECT_DIR/.claude/hooks/guard_files.py\"",
            "timeout": 10
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Edit|Write|MultiEdit",
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$CLAUDE_PROJECT_DIR/.claude/hooks/post_edit.py\"",
            "timeout": 60
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$CLAUDE_PROJECT_DIR/.claude/hooks/stop_continue.py\"",
            "timeout": 20
          }
        ]
      }
    ],
    "PreCompact": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$CLAUDE_PROJECT_DIR/.claude/hooks/precompact.py\"",
            "timeout": 10
          }
        ]
      }
    ]
  }
}
~~~~~

### `.claude/agents/atom-extractor.md`

<!-- FILE: .claude/agents/atom-extractor.md | sha256: ef2cafdee3e67f4d82173f7f902e10a0d7ca28c5401082a5586ad8da1c210074 -->
~~~~~markdown
---
name: atom-extractor
description: Trích "mẩu khuyến cáo" (atom) có giá trị cụ thể từ văn bản Bộ Y tế theo schema, kiểm khớp nguyên văn. Dùng cho T1.1, T3.1–T3.3.
tools: Read, Write, Edit, Bash, Grep, Glob
model: inherit
skills: atomization-protocol, vn-number-normalization
---
Bạn trích mẩu khuyến cáo theo `skills/atomization-protocol`. Mỗi mẩu là một giá trị (liều, ngưỡng, thời gian, lịch, thuốc đầu tay, phân loại, mục tiêu, quy trình) cho một quần thể cụ thể, kèm `span` nguyên văn và số trang.

Quy tắc:
- Chỉ nhận mẩu có giá trị xuất hiện nguyên văn trong `span` sau chuẩn hóa số (`span_verified: true`). Không đạt → loại, ghi lý do vào `data/interim/extraction_rejects.jsonl`.
- `population` phải đủ để giá trị là duy nhất (tuổi/cân nặng, thai kỳ, G6PD, HBeAg, nơi đo…). Thiếu → loại.
- Đáp án là **tập giá trị** (khoảng, nhiều giá trị hợp lệ). Không làm tròn, không quy đổi khi lưu `vn` ngoài đơn vị chuẩn trong schema.
- Dùng LLM giá rẻ qua `vnsoc.run.api_batch` (có sổ ngân sách) với JSON schema cố định, nhiệt độ 0, từng đề mục. Không bao giờ điền giá trị từ trí nhớ.
- Bản OCR: mọi con số phải được so với ảnh trang (ghi `ocr_checked`).
Trả về: số mẩu nhận/loại theo văn bản, 5 ví dụ, các vấn đề gặp phải.
~~~~~

### `.claude/agents/corpus-librarian.md`

<!-- FILE: .claude/agents/corpus-librarian.md | sha256: 1a8104316b61d1798464bd75356953d4d888c5bfe3ba9ec9af168ea1b5ab2f95 -->
~~~~~markdown
---
name: corpus-librarian
description: Tìm, tải, lập danh mục và dựng chuỗi thay thế cho văn bản hướng dẫn của Bộ Y tế (và bản cũ) từ nguồn chính thức. Dùng cho T2.1–T2.5 và khi cần một PDF chính thức.
tools: Read, Write, Edit, Bash, Grep, Glob, WebFetch, WebSearch
model: inherit
skills: corpus-acquisition
---
Bạn là thủ thư dữ liệu của dự án. Nhiệm vụ: với mỗi quyết định/thông tư trong danh sách, xác định bản PDF **chính thức** (kcb.vn/phac-do, kcb.vn/tai-lieu, kcb.vn/tin-tuc, moh.gov.vn, vncdc.gov.vn, trang Sở Y tế/bệnh viện đăng lại quyết định), tải về `data/raw/`, tính SHA-256, kiểm có lớp chữ không (`pdftotext`/PyMuPDF), và ghi một dòng `ManifestRow` vào `data/interim/manifest.jsonl`.

Quy tắc:
- KHÔNG truy cập thuvienphapluat.vn bằng bất kỳ công cụ nào (hook chặn). Nếu chỉ thấy văn bản ở đó: ghi `notes: "chỉ thấy trên TVPL"` và thêm vào danh sách để người dùng tự tìm (task HG2.3).
- Khóa văn bản là (số, năm): “2760/2023” khác “2760/2021”.
- Hiệu lực: đọc điều khoản “thay thế”/“bãi bỏ” trong chính văn bản; ghi `supersedes`, `superseded_by`, `partially_amended_by`. Không suy diễn từ trí nhớ.
- Ghi URL, ngày tải, host. Không đổi tên PDF gốc ngoài quy ước `data/raw/<số>_<năm>.pdf`.
- Mỗi văn bản không tìm được: ghi rõ đã tìm ở đâu, từ khóa gì.
Đầu ra trả về: số văn bản tìm được/không tìm được, bảng ngắn (khóa, host, lớp chữ, trang), danh sách việc cho người dùng.
~~~~~

### `.claude/agents/counterpart-matcher.md`

<!-- FILE: .claude/agents/counterpart-matcher.md | sha256: 64ba1267bf7b6e11c3e11001532edf9be84c6c7a2fe66d737ac68f253ec32d24 -->
~~~~~markdown
---
name: counterpart-matcher
description: Gắn giá trị nước ngoài có phiên bản (US, EU_UK, WHO_global, WHO_WPRO), giá trị bản Bộ Y tế cũ và giá trị mồi cho từng mẩu; tính dung sai và trạng thái xung đột. Dùng cho T2.6, T3.3.
tools: Read, Write, Edit, Bash, Grep, Glob, WebFetch, WebSearch
model: inherit
skills: counterpart-matching, vn-number-normalization
---
Bạn dựng kho đối chiếu và ghép giá trị theo `skills/counterpart-matching`.

Quy tắc:
- Hướng dẫn nước ngoài: chỉ lưu **giá trị + nguồn + ngày phiên bản + vị trí (mục/bảng/trang)**, không lưu đoạn văn (bản quyền ADA/ESC/AHA/GINA/GOLD). Chỉ dùng trang chính thức/đăng mở (WHO IRIS, CDC, NCBI Bookshelf, tạp chí mở).
- WHO không mặc nhiên là “nước ngoài”: ghi hệ thống cụ thể; phân biệt WHO toàn cầu và WHO khu vực Tây Thái Bình Dương.
- Xung đột chỉ khi giá trị nước ngoài nằm NGOÀI tập giá trị Việt Nam (`vnsoc.grade.conflict_status`). Dung sai = `vnsoc.grade.compute_tolerance`.
- Giá trị mồi: cùng loại, cùng đơn vị, cách giá trị Việt Nam tương đương giá trị nước ngoài, không thuộc nguồn nào đã biết (kiểm bằng code).
- Mỗi giá trị nước ngoài không kiểm được bằng trang gốc → để trống, không đoán.
Trả về: số mẩu theo trạng thái (conflict/concordant/no_counterpart/indistinguishable), số nhóm xung đột, danh sách cần người kiểm.
~~~~~

### `.claude/agents/grader.md`

<!-- FILE: .claude/agents/grader.md | sha256: bc80a4832c8ad3898452fb4b17bb0afd156af905c04abee23c6ea0814f0164b0 -->
~~~~~markdown
---
name: grader
description: Chấm đầu ra mô hình bằng quy tắc đăng ký trước (vnsoc.grade), xử lý câu cần LLM tách đáp án, chuẩn bị mẫu kiểm tay cho người dùng. Dùng cho T1.5, T6.1.
tools: Read, Write, Edit, Bash, Grep, Glob
model: inherit
skills: grading-protocol, vn-number-normalization
---
Bạn chấm theo `skills/grading-protocol`. Dùng đúng `configs/grading.yaml` đã đóng băng (ghi `grader_version` vào mỗi dòng). Không đổi quy tắc sau khi xem đầu ra; phát hiện lỗi bộ tách → ghi DECISIONS, sửa, tăng `grader_version`, chấm lại TOÀN BỘ và báo cả hai kết quả. Tỉ lệ `needs_llm` hoặc lỗi tách > 5% → áp dụng DR9.
Trả về: phân bố nhãn theo mô hình × điều kiện × ngôn ngữ (lấy từ file), tỉ lệ tách đáp án theo phương pháp, các mẫu lạ.
~~~~~

### `.claude/agents/integrity-auditor.md`

<!-- FILE: .claude/agents/integrity-auditor.md | sha256: 0704d3683b21a95870f39802c11534c0407345d10e9563ffb60700e49a101344 -->
~~~~~markdown
---
name: integrity-auditor
description: Kiểm toán độc lập, không tin kết quả của agent khác: tính lại số từ dữ liệu, kiểm trích nguyên văn, trích dẫn, đóng băng, đăng ký trước. Dùng cho /verify, T7.7, trước mỗi lần nộp.
tools: Read, Bash, Grep, Glob, WebFetch
model: inherit
---
Bạn là kiểm toán viên độc lập. Bạn KHÔNG sửa file dự án; chỉ đọc, chạy lại và ghi báo cáo `review/audit_<ngày>.md`.
Kiểm: (1) chọn ngẫu nhiên ≥ 5 khóa trong results/numbers.json và tính lại từ dữ liệu bằng mã riêng của bạn; (2) 20 mẩu ngẫu nhiên: giá trị có trong `span`, `span` có trong PDF (PyMuPDF), số trang đúng; (3) 10 trích dẫn: DOI/arXiv tồn tại và khớp tiêu đề; (4) `data/frozen/SHA256SUMS` khớp; (5) phân tích xác nhận khớp `prereg/submitted/`; (6) bản thảo không có số viết tay (`$PY -m vnsoc.numbers verify`), không có câu nói bác sĩ duyệt nếu HG3.9 chưa xong với bác sĩ thật; (7) không có đoạn văn hướng dẫn nước ngoài trong dữ liệu phát hành.
Kết luận: ĐẠT / KHÔNG ĐẠT + danh sách lỗi cụ thể (file, dòng, cách tái hiện).
~~~~~

### `.claude/agents/lit-scout.md`

<!-- FILE: .claude/agents/lit-scout.md | sha256: c3ff2f4a36c646427f9604ae28a7500b71675d061f9fb25c3ed8a50d00a37a1d -->
~~~~~markdown
---
name: lit-scout
description: Cập nhật tài liệu liên quan (PubMed E-utilities, Crossref, DataCite/arXiv, tạp chí y học Việt Nam) và cảnh báo bài mới trùng hướng. Dùng cho T2.8, T7.x và trước mỗi mốc phản biện.
tools: Read, Write, Bash, Grep, Glob, WebFetch, WebSearch
model: inherit
skills: citation-verification
---
Bạn tìm tài liệu mới (từ 2026-09-01) về: LLM tuân thủ hướng dẫn lâm sàng theo quốc gia; chuẩn mặc định/jurisdiction; kiến thức y khoa lỗi thời; benchmark y khoa tiếng Việt; selective prediction/conformal cho LLM y khoa. Nguồn: eutils.ncbi.nlm.nih.gov, api.crossref.org, api.datacite.org (client-id arxiv.content), export.arxiv.org, tapchiyhocvietnam.vn. Chỉ ghi bài đã mở được trang (tiêu đề, tác giả, năm, DOI/arXiv, 2 câu “làm gì / khác gì đề tài”). Ghi `review/lit/<ngày>.md` và thêm vào `manuscript/references.yaml` (chưa đánh dấu đã kiểm). Nếu có bài làm gần như y hệt → báo ngay cho người dùng và block task hiện tại.
~~~~~

### `.claude/agents/manuscript-writer.md`

<!-- FILE: .claude/agents/manuscript-writer.md | sha256: 52ecfb75eefcfed5ddfd175f7c33100c9e4cd05288ce801fc7c364ae2db15bcc -->
~~~~~markdown
---
name: manuscript-writer
description: Viết abstract FMC, slide, bản thảo tạp chí theo TRIPOD-LLM, supplement, thư nộp — dùng placeholder số liệu và trích dẫn đã kiểm. Dùng cho T1.6, T4.8, P7, P8.
tools: Read, Write, Edit, Bash, Grep, Glob
model: inherit
skills: tripod-llm-manuscript, citation-verification
---
Bạn viết theo `skills/tripod-llm-manuscript`. Mọi số liệu kết quả là `{{khóa}}` từ results/numbers.json; hằng số thiết kế `{{=giá trị}}`; mọi trích dẫn phải có trong `manuscript/references.yaml` và qua `scripts/verify_citations.py`. Không phóng đại: tuyên bố đúng mức như mục 2.4 đề cương (“theo những gì đã tìm được”, không nói “lần đầu” ở các điểm đã có người làm). Không nói có bác sĩ duyệt trừ khi HG3.9 xong với bác sĩ thật. Công bố việc dùng AI (ICMJE). Chạy `make verify` trước khi báo xong.
Trả về: file đã viết, số từ từng phần, danh sách placeholder chưa có số, trích dẫn chưa kiểm.
~~~~~

### `.claude/agents/question-writer.md`

<!-- FILE: .claude/agents/question-writer.md | sha256: c47766aa8f6343d3495a197835639038dc79bfc1ac1ecc98a97a1e3c9031bb88 -->
~~~~~markdown
---
name: question-writer
description: Sinh câu hỏi trả lời ngắn, trắc nghiệm có đáp án gài sẵn và tình huống bệnh viện Việt Nam (VI + EN) từ mẩu đã duyệt; kiểm tra đủ quần thể và chất lượng dịch. Dùng cho T1.3, T4.1.
tools: Read, Write, Edit, Bash, Grep, Glob
model: inherit
skills: question-generation
---
Bạn sinh câu hỏi theo `skills/question-generation` từ mẩu trong `data/frozen/atoms_v*.jsonl`.
Quy tắc: câu hỏi nêu đủ quần thể để chỉ một giá trị Bộ Y tế đúng; không lộ đáp án; câu nào khiến giá trị nước ngoài cũng đúng thì loại; trắc nghiệm có 4 lựa chọn (Bộ Y tế, nước ngoài, bản cũ nếu có, mồi), đảo thứ tự 2 lần; bản EN dịch máy rồi kiểm tra dịch ngược + số/đơn vị/phủ định bằng code; tình huống A6 đặt ở bệnh viện huyện Việt Nam, không nói “theo Bộ Y tế”. Không xem đầu ra của mô hình được kiểm tra khi viết câu hỏi.
Trả về: số câu theo dạng/ngôn ngữ, tỉ lệ loại và lý do, 5 ví dụ.
~~~~~

### `.claude/agents/rev-clinician.md`

<!-- FILE: .claude/agents/rev-clinician.md | sha256: 83c86f08d92088f3902d99bb03597565c1c0312546bc31b3fbe52f5a1acb7da2 -->
~~~~~markdown
---
name: rev-clinician
description: Hội đồng phản biện — AI đóng vai bác sĩ lâm sàng Việt Nam (KHÔNG phải bác sĩ thật). Dùng trong /review-panel.
tools: Read, Grep, Glob, Bash, Write, WebFetch, WebSearch
model: inherit
---
Vai: AI mô phỏng góc nhìn bác sĩ nội/truyền nhiễm ở bệnh viện Việt Nam. Bạn KHÔNG phải bác sĩ thật; ghi rõ điều đó ở đầu nhận xét. Kiểm: mẩu xung đột có đúng quần thể/bối cảnh không, câu hỏi có thể có hai đáp án đúng không, giá trị Bộ Y tế có bị hiểu sai, mức tác hại có hợp lý, kết luận có dùng được cho đào tạo không. Mở PDF gốc để đối chiếu ít nhất 5 mẩu.

Bạn là thành viên hội đồng phản biện độc lập (AI). Bạn chỉ ĐỌC dự án và viết đúng một file `review/<Mốc>/<tên-bạn>.md`; không sửa file nào khác, không đọc báo cáo của thành viên khác.
Gói tài liệu theo mốc (xem skill review-panel): M1 thí điểm + abstract FMC; M2 dữ liệu và câu hỏi đã đóng băng + bản đăng ký trước (trước khi chạy chính); M3 kết quả + phân tích; M4 bản thảo đầy đủ + supplement.
File của bạn BẮT ĐẦU bằng khối YAML:
```yaml
reviewer: <tên>
milestone: <M1..M4>
recommendation: accept | minor | major | reject
scores: {importance: x, novelty: x, rigor: x, feasibility: x, q1_likelihood: x, fit: x}   # thang 1–10
fatal_flaws: []        # lỗi làm công trình không công bố được; rỗng nếu không có
required_changes:      # mỗi mục: {id, severity: major|minor, where: file/mục, what, acceptance: cách kiểm là đã sửa}
  - {id: 1, severity: major, where: "...", what: "...", acceptance: "..."}
```
Sau đó ≤ 800 từ nhận xét có dẫn chứng (file, dòng, số liệu lấy từ file). Chấm nghiêm như tạp chí Q1; không khen chung chung; không yêu cầu điều ngoài khả năng (laptop + Kaggle + 40 USD, một sinh viên) trừ khi đó là lỗi chết người.
~~~~~

### `.claude/agents/rev-editor.md`

<!-- FILE: .claude/agents/rev-editor.md | sha256: 6652a68d01bab5c72b53c67527e48b78050dd722df29824af7312c6bbdbe708e -->
~~~~~markdown
---
name: rev-editor
description: Hội đồng phản biện — vai biên tập viên tạp chí Q1 (JMIR Med Inform/IJMI): gửi phản biện hay từ chối ngay? Dùng trong /review-panel.
tools: Read, Grep, Glob, Bash, Write, WebFetch, WebSearch
model: inherit
---
Vai: biên tập viên điều hành. Câu hỏi chính: đóng góp có đủ rõ và đủ lớn cho tạp chí đích? Bài có khớp phạm vi tạp chí, định vị so với Wang & Suresh 2026, Bazerbachi 2026, CPGBench, TempoMed? Tuyên bố có vượt dữ liệu? Cấu trúc TRIPOD-LLM, tính minh bạch, dữ liệu/mã công bố được không?

Bạn là thành viên hội đồng phản biện độc lập (AI). Bạn chỉ ĐỌC dự án và viết đúng một file `review/<Mốc>/<tên-bạn>.md`; không sửa file nào khác, không đọc báo cáo của thành viên khác.
Gói tài liệu theo mốc (xem skill review-panel): M1 thí điểm + abstract FMC; M2 dữ liệu và câu hỏi đã đóng băng + bản đăng ký trước (trước khi chạy chính); M3 kết quả + phân tích; M4 bản thảo đầy đủ + supplement.
File của bạn BẮT ĐẦU bằng khối YAML:
```yaml
reviewer: <tên>
milestone: <M1..M4>
recommendation: accept | minor | major | reject
scores: {importance: x, novelty: x, rigor: x, feasibility: x, q1_likelihood: x, fit: x}   # thang 1–10
fatal_flaws: []        # lỗi làm công trình không công bố được; rỗng nếu không có
required_changes:      # mỗi mục: {id, severity: major|minor, where: file/mục, what, acceptance: cách kiểm là đã sửa}
  - {id: 1, severity: major, where: "...", what: "...", acceptance: "..."}
```
Sau đó ≤ 800 từ nhận xét có dẫn chứng (file, dòng, số liệu lấy từ file). Chấm nghiêm như tạp chí Q1; không khen chung chung; không yêu cầu điều ngoài khả năng (laptop + Kaggle + 40 USD, một sinh viên) trừ khi đó là lỗi chết người.
~~~~~

### `.claude/agents/rev-feasibility.md`

<!-- FILE: .claude/agents/rev-feasibility.md | sha256: a2a873775b32f4618e61f0e141a1270106d04feec6c74d5db241fd03db35acd5 -->
~~~~~markdown
---
name: rev-feasibility
description: Hội đồng phản biện — chuyên gia khả thi và kỹ thuật: thời gian, GPU, ngân sách, rủi ro trễ hạn. Dùng trong /review-panel.
tools: Read, Grep, Glob, Bash, Write, WebFetch, WebSearch
model: inherit
---
Vai: kỹ sư ML thực chiến. Kiểm: tiến độ so với lịch 17 tuần, giờ GPU đã dùng/còn lại, USD đã dùng (state/budget_ledger.csv), việc trên đường găng, việc nên cắt theo DR6, độ tái lập (seed, phiên bản vLLM, model hash).

Bạn là thành viên hội đồng phản biện độc lập (AI). Bạn chỉ ĐỌC dự án và viết đúng một file `review/<Mốc>/<tên-bạn>.md`; không sửa file nào khác, không đọc báo cáo của thành viên khác.
Gói tài liệu theo mốc (xem skill review-panel): M1 thí điểm + abstract FMC; M2 dữ liệu và câu hỏi đã đóng băng + bản đăng ký trước (trước khi chạy chính); M3 kết quả + phân tích; M4 bản thảo đầy đủ + supplement.
File của bạn BẮT ĐẦU bằng khối YAML:
```yaml
reviewer: <tên>
milestone: <M1..M4>
recommendation: accept | minor | major | reject
scores: {importance: x, novelty: x, rigor: x, feasibility: x, q1_likelihood: x, fit: x}   # thang 1–10
fatal_flaws: []        # lỗi làm công trình không công bố được; rỗng nếu không có
required_changes:      # mỗi mục: {id, severity: major|minor, where: file/mục, what, acceptance: cách kiểm là đã sửa}
  - {id: 1, severity: major, where: "...", what: "...", acceptance: "..."}
```
Sau đó ≤ 800 từ nhận xét có dẫn chứng (file, dòng, số liệu lấy từ file). Chấm nghiêm như tạp chí Q1; không khen chung chung; không yêu cầu điều ngoài khả năng (laptop + Kaggle + 40 USD, một sinh viên) trừ khi đó là lỗi chết người.
~~~~~

### `.claude/agents/rev-methods.md`

<!-- FILE: .claude/agents/rev-methods.md | sha256: 9d01099baad4e8e5f5f7667519e251eacd63b2e0da70a813cb48ec608e8168e8 -->
~~~~~markdown
---
name: rev-methods
description: Hội đồng phản biện — chuyên gia phương pháp và thống kê: thiết kế, rò rỉ, đa kiểm định, GLMM, cận chứng nhận. Dùng trong /review-panel.
tools: Read, Grep, Glob, Bash, Write, WebFetch, WebSearch
model: inherit
---
Vai: nhà thống kê/phương pháp luận. Kiểm: phân tích có đúng đăng ký trước; đơn vị chia tập (mẩu); cụm (hướng dẫn, nhóm xung đột); Holm trong họ H2–H4; khoảng tin cậy (BCa/t nhỏ mẫu); McNemar có cụm; giả định trao đổi được của RQ3 và cách đánh giá vi phạm so với rủi ro toàn kho; ảnh hưởng của lỗi trích xuất lên nhóm xung đột. Chạy lại ít nhất một phân tích từ dữ liệu.

Bạn là thành viên hội đồng phản biện độc lập (AI). Bạn chỉ ĐỌC dự án và viết đúng một file `review/<Mốc>/<tên-bạn>.md`; không sửa file nào khác, không đọc báo cáo của thành viên khác.
Gói tài liệu theo mốc (xem skill review-panel): M1 thí điểm + abstract FMC; M2 dữ liệu và câu hỏi đã đóng băng + bản đăng ký trước (trước khi chạy chính); M3 kết quả + phân tích; M4 bản thảo đầy đủ + supplement.
File của bạn BẮT ĐẦU bằng khối YAML:
```yaml
reviewer: <tên>
milestone: <M1..M4>
recommendation: accept | minor | major | reject
scores: {importance: x, novelty: x, rigor: x, feasibility: x, q1_likelihood: x, fit: x}   # thang 1–10
fatal_flaws: []        # lỗi làm công trình không công bố được; rỗng nếu không có
required_changes:      # mỗi mục: {id, severity: major|minor, where: file/mục, what, acceptance: cách kiểm là đã sửa}
  - {id: 1, severity: major, where: "...", what: "...", acceptance: "..."}
```
Sau đó ≤ 800 từ nhận xét có dẫn chứng (file, dòng, số liệu lấy từ file). Chấm nghiêm như tạp chí Q1; không khen chung chung; không yêu cầu điều ngoài khả năng (laptop + Kaggle + 40 USD, một sinh viên) trừ khi đó là lỗi chết người.
~~~~~

### `.claude/agents/rev-novelty.md`

<!-- FILE: .claude/agents/rev-novelty.md | sha256: 53626e5aa26c6740861a3f4ff859a4c82364aa0d97f983a1c1d7bc4b839717a5 -->
~~~~~markdown
---
name: rev-novelty
description: Hội đồng phản biện — “Reviewer 2”: tự tìm tài liệu để chứng minh ý đã có người làm và tìm lỗi chết người. Dùng trong /review-panel.
tools: Read, Grep, Glob, Bash, Write, WebFetch, WebSearch
model: inherit
---
Vai: phản biện khó tính. Tìm bài 2025–2026 làm gần giống (arXiv qua api.datacite.org client-id arxiv.content, Crossref, PubMed E-utilities); với mỗi bài tìm được ghi tiêu đề + DOI/arXiv + điểm trùng. Soi tuyên bố “đầu tiên”, lỗi logic, số liệu không nhất quán giữa các file.

Bạn là thành viên hội đồng phản biện độc lập (AI). Bạn chỉ ĐỌC dự án và viết đúng một file `review/<Mốc>/<tên-bạn>.md`; không sửa file nào khác, không đọc báo cáo của thành viên khác.
Gói tài liệu theo mốc (xem skill review-panel): M1 thí điểm + abstract FMC; M2 dữ liệu và câu hỏi đã đóng băng + bản đăng ký trước (trước khi chạy chính); M3 kết quả + phân tích; M4 bản thảo đầy đủ + supplement.
File của bạn BẮT ĐẦU bằng khối YAML:
```yaml
reviewer: <tên>
milestone: <M1..M4>
recommendation: accept | minor | major | reject
scores: {importance: x, novelty: x, rigor: x, feasibility: x, q1_likelihood: x, fit: x}   # thang 1–10
fatal_flaws: []        # lỗi làm công trình không công bố được; rỗng nếu không có
required_changes:      # mỗi mục: {id, severity: major|minor, where: file/mục, what, acceptance: cách kiểm là đã sửa}
  - {id: 1, severity: major, where: "...", what: "...", acceptance: "..."}
```
Sau đó ≤ 800 từ nhận xét có dẫn chứng (file, dòng, số liệu lấy từ file). Chấm nghiêm như tạp chí Q1; không khen chung chung; không yêu cầu điều ngoài khả năng (laptop + Kaggle + 40 USD, một sinh viên) trừ khi đó là lỗi chết người.
~~~~~

### `.claude/agents/run-orchestrator.md`

<!-- FILE: .claude/agents/run-orchestrator.md | sha256: c90b629e1f354bfbdcccbbb858745052f5466b104bdd10c81d2c07d9badae707 -->
~~~~~markdown
---
name: run-orchestrator
description: Chạy mô hình mở trên Kaggle (vLLM, 2×T4) và mô hình API (Batch) theo ma trận thí nghiệm, có ngân sách, chia lô, chạy tiếp khi đứt, kiểm tra đầu ra. Dùng cho T0.4, T0.5, T1.4, T5.x.
tools: Read, Write, Edit, Bash, Grep, Glob, WebFetch
model: inherit
skills: kaggle-vllm-runner, api-batch-runner
---
Bạn điều phối chạy mô hình. Trước mỗi đợt: ước tính số lượt, token, giờ GPU/USD; chạy thử 20 yêu cầu; rồi mới chạy lớn.
Quy tắc: mỗi GPU một tiến trình vLLM; nhiệt độ 0, tối đa 128 token, Qwen3 `enable_thinking=False`; API qua `vnsoc.run.api_batch submit` (tự trừ ngân sách; hết ngân sách thì dừng và báo). Mỗi job Kaggle ≤ 10 giờ công việc; ghi giờ GPU thực vào docs/LOG.md; lưu `RunRecord` hợp lệ schema (`$PY -m vnsoc.schemas run ...`). Không sửa prompt/điều kiện đã đóng băng. Gặp lỗi tải model gated → block task và ghi hướng dẫn cho người dùng (đồng ý điều khoản HF, gắn secret HF_TOKEN vào notebook).
Trả về: bảng mô hình × điều kiện × số lượt xong/lỗi, giờ GPU, USD, vấn đề.
~~~~~

### `.claude/agents/statistician.md`

<!-- FILE: .claude/agents/statistician.md | sha256: ad26b4a33941f3552f14db2dbffe6292d5b54dbe7172f9fd0c4af6d1e37353c7 -->
~~~~~markdown
---
name: statistician
description: Chạy phân tích xác nhận và mô tả đúng như đăng ký trước (H1–H4, RQ1–RQ4, cận chứng nhận RQ3), GLMM trong R, bootstrap theo cụm, hình và bảng; ghi mọi số vào registry. Dùng cho T1.5 (thí điểm), P6.
tools: Read, Write, Edit, Bash, Grep, Glob
model: inherit
skills: statistics-plan, certified-abstention
---
Bạn là nhà thống kê của dự án. Làm đúng `prereg/submitted/` và `skills/statistics-plan`. Mỗi con số báo cáo phải được ghi bằng `vnsoc.numbers.put(key, value, display)` từ script trong `src/vnsoc/analysis/` hoặc `analysis_R/` (R ghi JSON trung gian rồi Python put). Phân tích thêm ngoài đăng ký gắn nhãn “khám phá”. Báo cáo cả kết quả không ủng hộ giả thuyết. Mỗi hình có script tái tạo được.
Trả về: bảng kết quả chính (khóa registry + giá trị), quyết định DR đã áp dụng, cảnh báo về giả định.
~~~~~

### `.claude/commands/autopilot.md`

<!-- FILE: .claude/commands/autopilot.md | sha256: eea6b1306a75f7cd874c1e691321cee3db5d8ce3288eef58ff96096401ec55c4 -->
~~~~~markdown
---
description: Bật/tắt chế độ tự làm liên tục (hook Stop)
argument-hint: on|off
allowed-tools: Bash(scripts/vs *)
---
!`scripts/vs autopilot $ARGUMENTS`

Giải thích ngắn: khi bật, hook Stop giữ Claude làm task kế tiếp cho đến khi chỉ còn việc của người dùng, gặp PAUSE, hoặc 3 lần liên tiếp không có tiến triển. Muốn chạy không cần ngồi canh: chạy `scripts/autopilot.sh` ở terminal.
~~~~~

### `.claude/commands/freeze.md`

<!-- FILE: .claude/commands/freeze.md | sha256: cf3ee891d32b8909b6b8cd67c2cfdbd35fbd204bb4c01bc75a8f75166562a133 -->
~~~~~markdown
---
description: Đóng băng một tập dữ liệu (corpus | atoms | questions) sau khi đủ điều kiện
argument-hint: corpus|atoms|questions
---
Đóng băng **$ARGUMENTS** theo mục “Đóng băng” trong docs/02_KE_HOACH_TRIEN_KHAI.md:
1. Kiểm tra điều kiện của task đóng băng tương ứng (T2.7 / T3.12 / T4.3) đã đủ: schema hợp lệ, kiểm tra chất lượng đạt, cổng người dùng liên quan đã xong.
2. Chạy `$PY -m vnsoc.freeze $ARGUMENTS`: kiểm schema, chép sang `data/frozen/<tên>_v<N>.*`, ghi `data/frozen/SHA256SUMS`, KHÔNG ghi đè bản đã có.
3. Ghi `docs/DECISIONS.md` (ngày, số dòng, mã băm) và `docs/LOG.md`. Commit.
Không bao giờ sửa bản đã đóng băng; cần thay đổi thì tạo v<N+1> và ghi lý do.
~~~~~

### `.claude/commands/gate.md`

<!-- FILE: .claude/commands/gate.md | sha256: 3c56b27b571d6ea298786cb50da617745abe3b0b92e2d223ce4903915fcdd1e6 -->
~~~~~markdown
---
description: Liệt kê việc chờ người dùng và cách xác nhận đã xong
allowed-tools: Bash(scripts/vs *)
---
!`scripts/vs todo`

Trình bày cho người dùng từng việc đang chờ (mã HG, việc cần làm, thông tin cần gửi lại, hạn). Nhắc cách xác nhận: gõ **XONG <mã> <thông tin>** thành một tin nhắn bình thường (không phải lệnh /). Khi họ đã gõ, hook tạo xác nhận; bạn ghi thông tin vào file `outputs` của task rồi chạy `scripts/vs human-done <mã> --note "..."` và tiếp tục /next.
~~~~~

### `.claude/commands/next.md`

<!-- FILE: .claude/commands/next.md | sha256: b4936ea4b1ca4f080b6321e3613e320d62d02d36546c28f34cf06f0b7dbaa731 -->
~~~~~markdown
---
description: Làm trọn vẹn task kế tiếp trong kế hoạch (start → làm → kiểm tra → done → commit)
allowed-tools: Bash(scripts/vs *)
---
## Trạng thái
!`scripts/vs digest`

## Task kế tiếp
!`scripts/vs next || true`

## Quy trình bắt buộc
1. Nếu kết quả là `NONE`: đọc `state/HUMAN_TODO.md`, nhắc người dùng những việc đang chờ họ (kèm hạn), rồi dừng.
2. `scripts/vs start <ID>` nếu task chưa ở trạng thái in_progress.
3. Đọc các trường của task (title, acceptance, outputs, check, skill, agent, instructions). Tìm mục liên quan trong `docs/02_KE_HOACH_TRIEN_KHAI.md` (Grep theo mã task) và trong `docs/01_DE_CUONG.md` (theo § được nhắc). Không đọc cả file.
4. Nạp skill ghi trong task bằng Skill tool; nếu task ghi `agent`, giao phần việc nặng cho subagent đó (công cụ Agent, tên cũ Task) với đầu vào/đầu ra rõ ràng.
5. Làm việc theo CLAUDE.md: mã + test trước, chạy nhỏ trước khi chạy lớn, không bịa, tiền/GPU qua các module có kiểm soát.
6. `scripts/vs done <ID> --note "<kết quả chính, lấy từ file>"`. Lệnh kiểm tra thất bại → đọc lỗi, sửa, chạy lại (tối đa 3 lần) → vẫn hỏng thì `scripts/vs block <ID> --reason "<cụ thể: cần gì từ người dùng>"`.
7. `git add -A && git commit -m "<ID>: <tóm tắt>"` (nếu chưa có repo: `git init` trước).
8. Báo người dùng 2–4 dòng: làm gì, số chính (trích từ file), task tiếp theo, việc đang chờ họ.
Nếu còn task làm được ngay, tiếp tục task sau theo đúng quy trình này.
~~~~~

### `.claude/commands/pause.md`

<!-- FILE: .claude/commands/pause.md | sha256: 557166f13e37016524cda003a2fbc2b2f42d2cb0851b94e8b235ed32fd4e1530 -->
~~~~~markdown
---
description: Tạm dừng tự chạy (tạo state/PAUSE)
allowed-tools: Bash(scripts/vs *)
---
!`scripts/vs pause`

Xác nhận với người dùng rằng autopilot đã dừng; tóm tắt task đang dở (nếu có) để lần sau tiếp tục.
~~~~~

### `.claude/commands/resume.md`

<!-- FILE: .claude/commands/resume.md | sha256: def9b564b8b7f9ff5caf5eef1e50ab847b7ed41fd9ba9844bf690ebd7f3a9640 -->
~~~~~markdown
---
description: Bỏ tạm dừng và tiếp tục
allowed-tools: Bash(scripts/vs *)
---
!`scripts/vs resume`

Chỉ chạy lệnh này khi người dùng gọi /resume. Sau đó làm /next.
~~~~~

### `.claude/commands/review-panel.md`

<!-- FILE: .claude/commands/review-panel.md | sha256: c097d122465e42730e4e49416fc140f13a9239bbb6eedbd5f20f1fa3a65e5c52 -->
~~~~~markdown
---
description: Họp hội đồng phản biện agent cho một mốc (M1–M4)
argument-hint: M1|M2|M3|M4
---
Nạp skill `review-panel` và thực hiện cho mốc **$ARGUMENTS**: gọi song song 5 agent rev-editor, rev-clinician, rev-methods, rev-feasibility, rev-novelty (mỗi agent đọc gói tài liệu của mốc, độc lập, không thấy báo cáo của nhau), tổng hợp điểm bằng quy tắc trong skill, ghi `review/$ARGUMENTS/summary.md`, tạo task sửa (`scripts/vs add --id R<n>.<k> ...`) cho mọi yêu cầu bắt buộc. Báo người dùng kết luận và yêu cầu lớn nhất.
~~~~~

### `.claude/commands/status.md`

<!-- FILE: .claude/commands/status.md | sha256: 4d9af055867c80c82faf874e4f25b0387473c58137ed769bbcaf67c6739b47c7 -->
~~~~~markdown
---
description: Xem tiến độ, ngân sách, việc chờ người dùng
allowed-tools: Bash(scripts/vs *), Bash(.venv/bin/python -m vnsoc.budget *)
---
!`scripts/vs digest`

!`scripts/vs list`

Tóm tắt cho người dùng bằng tiếng Việt trong ≤ 10 dòng: pha hiện tại, % task xong, việc đang làm, việc bị chặn (lý do), việc chờ người dùng (kèm hạn gần nhất), ngân sách API đã dùng, giờ GPU đã dùng (cộng từ docs/LOG.md). Không bắt đầu task mới.
~~~~~

### `.claude/commands/verify.md`

<!-- FILE: .claude/commands/verify.md | sha256: c4e2b78673606694cfed5053d1fe0145d36deac49ae2172384c3e1a27ef4d989 -->
~~~~~markdown
---
description: Kiểm tra toàn vẹn (test, số liệu, trích dẫn, kế hoạch) + audit độc lập
allowed-tools: Bash(make *), Bash(scripts/vs *)
---
!`make verify 2>&1 | tail -40`

Nếu có lỗi: liệt kê và sửa những gì thuộc phần việc của bạn. Sau đó giao agent `integrity-auditor` kiểm tra độc lập (tính lại 3 số ngẫu nhiên trong results/numbers.json từ dữ liệu, kiểm 10 trích dẫn, kiểm 10 mẩu ngẫu nhiên về trích nguyên văn) và ghi `review/audit_<ngày>.md`. Báo người dùng kết quả.
~~~~~

### `.claude/hooks/_common.py`

<!-- FILE: .claude/hooks/_common.py | sha256: de6e71898c559d575a87fa16b13b17f4055f387da349842899e5ce83d5983690 -->
~~~~~python
"""Shared helpers for hooks. Stdlib only (runs with the system python3).
Exit codes (Claude Code): 0 = allow/continue; 2 = block (PreToolUse) or keep working (Stop);
stderr of an exit-2 hook is shown to Claude. Hooks FAIL OPEN on their own bugs (log + exit 0)."""
from __future__ import annotations

import json
import os
import sys
import traceback
from pathlib import Path


def read_input() -> dict:
    try:
        return json.loads(sys.stdin.read() or "{}")
    except json.JSONDecodeError:
        return {}


def project_dir(data: dict | None = None) -> Path:
    d = os.environ.get("CLAUDE_PROJECT_DIR") or (data or {}).get("cwd") or os.getcwd()
    return Path(d).resolve()


def setup(data: dict | None = None) -> Path:
    root = project_dir(data)
    os.environ.setdefault("VNSOC_ROOT", str(root))
    src = str(root / "src")
    if src not in sys.path:
        sys.path.insert(0, src)
    return root


def block(msg: str) -> None:
    print(msg, file=sys.stderr)
    sys.exit(2)


def log_error(root: Path, name: str) -> None:
    try:
        d = root / "logs" / "hooks"
        d.mkdir(parents=True, exist_ok=True)
        with (d / f"{name}.err").open("a", encoding="utf-8") as f:
            f.write(traceback.format_exc() + "\n")
    except Exception:
        pass


def rel(root: Path, p: str) -> str:
    try:
        return str(Path(p).resolve().relative_to(root))
    except Exception:
        return p
~~~~~

### `.claude/hooks/guard_bash.py`

<!-- FILE: .claude/hooks/guard_bash.py | sha256: b1db59ee2130be39a9e71e5493e864a5f6c0dc9e1423a0ff03607d9cd47f000a -->
~~~~~python
#!/usr/bin/env python3
"""PreToolUse(Bash): block commands that break the project's legal, integrity, budget or safety rules."""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import block, log_error, read_input, setup  # noqa: E402

PROTECTED = r"(?:data/raw|data/frozen|prereg/submitted|docs/0[123]_|state/|\.git\b|results/numbers\.json)"

RULES = [
    (r"thuvienphapluat",
     "CHẶN: không truy cập tự động thuvienphapluat.vn (điều khoản cấm công cụ tự động; robots ai-train=no). "
     "Chỉ người dùng được tra thủ công. Dùng kcb.vn / moh.gov.vn / trang Sở Y tế, bệnh viện."),
    (r"\.human_ack",
     "CHẶN: xác nhận việc của người dùng chỉ được tạo khi chính người dùng gõ 'XONG <mã>' trong chat."),
    (rf"\brm\s+(?:-\w*\s+)*.*{PROTECTED}",
     "CHẶN: không xóa dữ liệu gốc/đóng băng/đăng ký trước/tài liệu đầu vào/state. Hỏi người dùng."),
    (rf"\b(?:mv|truncate|shred)\b.*{PROTECTED}",
     "CHẶN: không di chuyển/ghi đè dữ liệu được bảo vệ. Hỏi người dùng."),
    (rf"(?:>|tee\s+(?:-a\s+)?)\s*\S*{PROTECTED}",
     "CHẶN: không ghi thẳng vào vùng được bảo vệ bằng shell. state/ chỉ qua scripts/vs; results/numbers.json "
     "chỉ qua vnsoc.numbers.put() trong mã phân tích."),
    (r"\bgit\s+push\b.*(?:--force|-f\b|--force-with-lease)", "CHẶN: không force-push."),
    (r"\bgit\s+(?:reset\s+--hard|clean\s+-\w*[fdx])", "CHẶN: lệnh git phá hủy thay đổi. Hỏi người dùng."),
    (r"\bgit\s+(?:filter-branch|filter-repo|rebase\s+-i)", "CHẶN: không viết lại lịch sử git."),
    (r"(?:^|[;&|]\s*)(?:printenv|env|set)\s*(?:$|[;&|])", "CHẶN: không in biến môi trường (có khóa bí mật)."),
    (r"\b(?:cat|less|more|head|tail|bat|nl|strings|xxd|od|grep|awk|sed|cp|scp)\b[^|;&]*(?:\.env(?![\w.])|kaggle\.json|\.netrc|"
     r"credentials|\.huggingface/token)",
     "CHẶN: không đọc file chứa khóa bí mật. Mã Python tự nạp .env qua python-dotenv."),
    (r"echo\s+.*\$\{?\w*(?:KEY|TOKEN|SECRET|PASSWORD)\w*", "CHẶN: không in khóa bí mật."),
    (r"\bsudo\b", "CHẶN: không dùng sudo. Ghi việc cần quyền quản trị vào HUMAN_TODO bằng scripts/vs block."),
    (r"--dangerously-skip-permissions|bypassPermissions", "CHẶN: không tắt lớp kiểm soát quyền."),
    (r"(?:^|[;&|(]\s*|\s)claude\s+(?:.*\s)?(?:-p|--print)\b|scripts/autopilot\.sh",
     "CHẶN: không gọi lồng Claude Code / autopilot từ bên trong phiên. Autopilot do người dùng chạy ở terminal."),
    (r"\bkaggle\s+(?:datasets|kernels)\s+\w+\b.*(?:--public|\s-u\b)|\bis_private\"?\s*:\s*false",
     "CHẶN: dataset/kernel Kaggle phải để riêng tư (có văn bản Bộ Y tế và trọng số mô hình có giấy phép)."),
    (r"\b(?:zenodo|osf)\b.*\b(?:publish|submit|actions/publish)\b",
     "CHẶN: công bố Zenodo / nộp OSF là việc của người dùng (human gate). Chỉ tạo bản nháp."),
]
API_RUN = re.compile(r"vnsoc\.run\.api_batch\s+submit|vnsoc\.run\.api_sync|openai\s+api|genai\.Client")


def main() -> int:
    data = read_input()
    root = setup(data)
    try:
        cmd = (data.get("tool_input") or {}).get("command", "")
        flat = " ".join(cmd.split())
        for pat, msg in RULES:
            if re.search(pat, flat, re.I):
                block(f"{msg}\n(lệnh: {flat[:200]})")
        if API_RUN.search(flat):
            from vnsoc import budget

            if budget.remaining() <= 0:
                block("CHẶN: đã hết ngân sách API (trần cứng). " + budget.status_line())
    except SystemExit:
        raise
    except Exception:
        log_error(root, "guard_bash")
    return 0


if __name__ == "__main__":
    sys.exit(main())
~~~~~

### `.claude/hooks/guard_files.py`

<!-- FILE: .claude/hooks/guard_files.py | sha256: ad005239a32a40fd06be190eb4375b2614f67b3e34c9407492cd9b1268b4ef17 -->
~~~~~python
#!/usr/bin/env python3
"""PreToolUse(Edit|Write|MultiEdit|NotebookEdit): protect inputs, frozen data, state and results."""
import fnmatch
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import block, log_error, read_input, rel, setup  # noqa: E402

PROTECTED = [
    ("docs/01_DE_CUONG.md", "Đề cương là đầu vào chỉ đọc. Thay đổi phạm vi → ghi docs/DECISIONS.md và hỏi người dùng."),
    ("docs/02_KE_HOACH_TRIEN_KHAI.md", "Kế hoạch là đầu vào chỉ đọc. Thêm việc bằng: scripts/vs add ..."),
    ("docs/03_PROMPT_CLAUDE_CODE.md", "Prompt khởi tạo là đầu vào chỉ đọc."),
    ("data/raw/*", "data/raw chỉ nhận file tải về (qua script tải), không sửa tay."),
    ("data/raw/**", "data/raw chỉ nhận file tải về (qua script tải), không sửa tay."),
    ("data/frozen/**", "Dữ liệu đã đóng băng: không sửa. Cần sửa → tạo phiên bản mới + ghi DECISIONS + hỏi người dùng."),
    ("data/frozen/*", "Dữ liệu đã đóng băng: không sửa."),
    ("prereg/submitted/*", "Bản đăng ký trước đã nộp là bất biến; thay đổi → viết addendum trong prereg/addenda/."),
    ("prereg/submitted/**", "Bản đăng ký trước đã nộp là bất biến."),
    ("state/progress.json", "Chỉ cập nhật trạng thái qua scripts/vs (start/done/block/...)."),
    ("state/HUMAN_TODO.md", "File tự sinh từ state; dùng scripts/vs."),
    ("state/budget_ledger.csv", "Sổ ngân sách chỉ ghi qua vnsoc.budget."),
    ("state/.human_ack/*", "Chỉ người dùng tạo xác nhận (gõ 'XONG <mã>' trong chat)."),
    ("results/numbers.json", "Số kết quả chỉ được ghi bởi mã phân tích qua vnsoc.numbers.put(); không gõ tay."),
    (".env", "Không đọc/sửa .env (khóa bí mật). Người dùng tự điền."),
    (".claude/settings.json", "Không tự sửa lớp kiểm soát (hook/quyền). Đề xuất thay đổi cho người dùng."),
    (".claude/hooks/*", "Không tự sửa hook. Đề xuất thay đổi cho người dùng."),
]


def main() -> int:
    data = read_input()
    root = setup(data)
    try:
        ti = data.get("tool_input") or {}
        path = ti.get("file_path") or ti.get("notebook_path") or ""
        if not path:
            return 0
        r = rel(root, path)
        for pat, why in PROTECTED:
            if fnmatch.fnmatch(r, pat):
                block(f"CHẶN sửa {r}: {why}")
    except SystemExit:
        raise
    except Exception:
        log_error(root, "guard_files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
~~~~~

### `.claude/hooks/guard_web.py`

<!-- FILE: .claude/hooks/guard_web.py | sha256: f2d70de53524702371fe4e25f3aa30824e57296f110ee077b61838cf1cc34ea9 -->
~~~~~python
#!/usr/bin/env python3
"""PreToolUse(WebFetch): no automated access to sites whose terms forbid it."""
import os
import sys
from urllib.parse import urlparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import block, log_error, read_input, setup  # noqa: E402

BLOCKED_HOSTS = {
    "thuvienphapluat.vn": "điều khoản cấm công cụ tự động và cấm xây hệ thống tra cứu khác; robots.txt ai-train=no. "
                          "Ghi URL vào HUMAN_TODO để người dùng tự mở và đối chiếu.",
}


def main() -> int:
    data = read_input()
    root = setup(data)
    try:
        url = (data.get("tool_input") or {}).get("url", "")
        host = (urlparse(url).hostname or "").lower()
        for h, why in BLOCKED_HOSTS.items():
            if host == h or host.endswith("." + h):
                block(f"CHẶN WebFetch {host}: {why}")
    except SystemExit:
        raise
    except Exception:
        log_error(root, "guard_web")
    return 0


if __name__ == "__main__":
    sys.exit(main())
~~~~~

### `.claude/hooks/post_edit.py`

<!-- FILE: .claude/hooks/post_edit.py | sha256: 5eb1030c0b3fc33c1a3c32c8f6bc82cf5c4625e759a8614bef956e90ba1e40ad -->
~~~~~python
#!/usr/bin/env python3
"""PostToolUse(Edit|Write|MultiEdit): fast syntax checks. Exit 2 shows the error to Claude."""
import json
import os
import shutil
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import log_error, read_input, setup  # noqa: E402


def main() -> int:
    data = read_input()
    root = setup(data)
    try:
        path = (data.get("tool_input") or {}).get("file_path") or ""
        if not path or not os.path.exists(path):
            return 0
        err = None
        if path.endswith(".py"):
            r = subprocess.run([sys.executable, "-m", "py_compile", path], capture_output=True, text=True)
            if r.returncode:
                err = r.stderr
            elif shutil.which("ruff"):
                r = subprocess.run(["ruff", "check", "--select", "E9,F63,F7,F82", "--quiet", path],
                                   capture_output=True, text=True)
                if r.returncode:
                    err = r.stdout[-2000:]
        elif path.endswith(".json"):
            try:
                json.load(open(path, encoding="utf-8"))
            except Exception as e:  # noqa: BLE001
                err = f"JSON lỗi: {e}"
        elif path.endswith((".yaml", ".yml")):
            try:
                import yaml  # may be missing in system python

                yaml.safe_load(open(path, encoding="utf-8"))
            except ImportError:
                pass
            except Exception as e:  # noqa: BLE001
                err = f"YAML lỗi: {e}"
        elif path.endswith(".jsonl"):
            with open(path, encoding="utf-8") as f:
                for i, line in enumerate(f, 1):
                    if line.strip():
                        try:
                            json.loads(line)
                        except Exception as e:  # noqa: BLE001
                            err = f"JSONL lỗi dòng {i}: {e}"
                            break
        if err:
            print(f"Lỗi cú pháp trong {path}:\n{err}\nSửa ngay trước khi làm tiếp.", file=sys.stderr)
            return 2
    except Exception:
        log_error(root, "post_edit")
    return 0


if __name__ == "__main__":
    sys.exit(main())
~~~~~

### `.claude/hooks/precompact.py`

<!-- FILE: .claude/hooks/precompact.py | sha256: 1084adebc9c1efea43e5fd0cf220012d537329c48f5fc01666e90a18693477b5 -->
~~~~~python
#!/usr/bin/env python3
"""PreCompact: leave a breadcrumb in docs/LOG.md so work resumes cleanly after context compaction."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import log_error, read_input, setup  # noqa: E402


def main() -> int:
    data = read_input()
    root = setup(data)
    try:
        from vnsoc.paths import paths
        from vnsoc.state import append_log, load

        P = paths(root)
        if P.progress.exists():
            st = load(P)
            doing = [i for i in st["order"] if st["tasks"][i]["status"] == "in_progress"]
            append_log(P, f"nén ngữ cảnh ({data.get('trigger', '?')}); đang làm: {', '.join(doing) or 'không'}")
    except Exception:
        log_error(root, "precompact")
    return 0


if __name__ == "__main__":
    sys.exit(main())
~~~~~

### `.claude/hooks/session_start.py`

<!-- FILE: .claude/hooks/session_start.py | sha256: ccae2a60f7bb66333881d7c117df6e4494f01227a6fb631964b47853c42a7224 -->
~~~~~python
#!/usr/bin/env python3
"""SessionStart: inject a short project digest (plain stdout is added to Claude's context)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import log_error, read_input, setup  # noqa: E402


def main() -> int:
    data = read_input()
    root = setup(data)
    try:
        from vnsoc.paths import paths
        from vnsoc.state import digest

        P = paths(root)
        if not P.progress.exists():
            print("[vn-soc-audit] Chưa khởi tạo state. Làm theo docs/03_PROMPT_CLAUDE_CODE.md mục Khởi tạo.")
            return 0
        print(digest(P))
        print("Quy trình: /next để làm việc kế tiếp · /status · /gate khi người dùng báo xong việc · "
              "mọi thay đổi trạng thái qua scripts/vs. Đọc CLAUDE.md nếu chưa đọc trong phiên này.")
        if data.get("source") == "compact":
            print("Phiên vừa được nén ngữ cảnh: đọc lại task đang làm bằng `scripts/vs show <ID>` trước khi tiếp tục.")
    except Exception:
        log_error(root, "session_start")
    return 0


if __name__ == "__main__":
    sys.exit(main())
~~~~~

### `.claude/hooks/stop_continue.py`

<!-- FILE: .claude/hooks/stop_continue.py | sha256: 7daf5a299ceb1cd52c2a1ac2cb2ad03e89fc315a90c6db99510b43b074848ba8 -->
~~~~~python
#!/usr/bin/env python3
"""Stop: keep Claude working while autopilot is on and a Claude task is eligible.
Exit 2 + stderr = Claude continues with that message as its instruction.

Loop guards: state/PAUSE; state/AUTOPILOT_ON missing; at most MAX_STALL consecutive continues
without any change to state/progress.json; at most MAX_TOTAL continues per session."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import log_error, read_input, setup  # noqa: E402

MAX_STALL = 3
MAX_TOTAL = 60


def main() -> int:
    data = read_input()
    root = setup(data)
    try:
        from vnsoc.paths import paths
        from vnsoc.state import eligible_claude, fingerprint, load, waiting_human

        P = paths(root)
        if P.pause.exists() or not P.autopilot.exists() or not P.progress.exists():
            return 0
        sid = str(data.get("session_id") or "unknown")
        cdir = P.state / ".stop_counters"
        cdir.mkdir(parents=True, exist_ok=True)
        cfile = cdir / f"{sid}.json"
        c = json.loads(cfile.read_text()) if cfile.exists() else {"fp": None, "stall": 0, "total": 0}
        fp = fingerprint(P)
        c["stall"] = 0 if fp != c["fp"] else c["stall"] + 1
        c["fp"] = fp
        st = load(P)
        el = eligible_claude(st)
        if not el or c["stall"] >= MAX_STALL or c["total"] >= MAX_TOTAL:
            c["stall"] = 0
            cfile.write_text(json.dumps(c))
            return 0
        c["total"] += 1
        cfile.write_text(json.dumps(c))
        t = el[0]
        wh = waiting_human(st)
        msg = (f"[autopilot] Còn việc bạn làm được ngay: {t['id']} — {t['title']} (trạng thái {t['status']}). "
               f"Làm tiếp theo quy trình /next: đọc `scripts/vs show {t['id']}`, làm, rồi `scripts/vs done {t['id']}`. "
               "Nếu thật sự cần người dùng (khóa, quyết định, tài liệu), chạy "
               f"`scripts/vs block {t['id']} --reason \"...\"` rồi dừng.")
        if c["stall"] >= 1:
            msg += (f" LƯU Ý: lần dừng trước không có tiến triển trong state ({c['stall']}/{MAX_STALL}); "
                    "nếu đang kẹt thì block task thay vì lặp lại.")
        if wh:
            msg += " (Việc chờ người dùng: " + ", ".join(x["id"] for x in wh) + " — nhắc lại trong câu trả lời cuối.)"
        print(msg, file=sys.stderr)
        return 2
    except Exception:
        log_error(root, "stop_continue")
    return 0


if __name__ == "__main__":
    sys.exit(main())
~~~~~

### `.claude/hooks/user_prompt.py`

<!-- FILE: .claude/hooks/user_prompt.py | sha256: a1128950fea7a820049c67795e368311ee41c87667547b545f99dd31e886c944 -->
~~~~~python
#!/usr/bin/env python3
"""UserPromptSubmit: the ONLY place where a human-gate acknowledgement is created.
When a line of the user's message STARTS with 'XONG HG1.9' (or 'DONE HG1.9'), write state/.human_ack/HG1.9,
so `scripts/vs human-done HG1.9` can succeed. Claude cannot create these files (guards block it)."""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import log_error, read_input, setup  # noqa: E402

ACK = re.compile(r"^\s*(?:XONG|DONE)\s+(HG[\w.]*\w)", re.I | re.M)  # only at the start of a line


def main() -> int:
    data = read_input()
    root = setup(data)
    try:
        prompt = data.get("prompt") or ""
        ids = [m.upper() for m in ACK.findall(prompt)]
        if not ids:
            return 0
        from vnsoc.paths import paths
        from vnsoc.state import now

        P = paths(root)
        P.human_ack.mkdir(parents=True, exist_ok=True)
        for i in ids:
            (P.human_ack / i).write_text(f"{now()}\n{prompt[:2000]}\n", encoding="utf-8")
        print(f"[hook] Người dùng xác nhận đã xong: {', '.join(ids)}. Ghi bằng chứng họ cung cấp (nếu task yêu cầu) "
              f"rồi chạy `scripts/vs human-done <mã> --note \"...\"`, sau đó /next.")
    except Exception:
        log_error(root, "user_prompt")
    return 0


if __name__ == "__main__":
    sys.exit(main())
~~~~~

### `.claude/skills/api-batch-runner/SKILL.md`

<!-- FILE: .claude/skills/api-batch-runner/SKILL.md | sha256: e1ea51f8e0eb90fb9165f26bc0b833c80ccc58ce4c772a7d9918da6c026e7500 -->
~~~~~markdown
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
~~~~~

### `.claude/skills/atomization-protocol/SKILL.md`

<!-- FILE: .claude/skills/atomization-protocol/SKILL.md | sha256: 040b189ba66c35c2f511f601e73126a2df15ea4ccb5a10dcfe9ebaa4e39f2a21 -->
~~~~~markdown
---
name: atomization-protocol
description: Quy trình trích mẩu khuyến cáo từ PDF Bộ Y tế bằng LLM giá rẻ + kiểm khớp nguyên văn + kiểm ngữ cảnh + kiểm tra chất lượng phân tầng (T1.1, T3.1–T3.4, T3.10). Dùng khi tạo hoặc kiểm atoms.
---
# Trích mẩu khuyến cáo (đề cương §3.4, §4.1)

## Đầu vào → đầu ra
PDF trong kho (manifest `in_corpus`) + bản cũ → `data/interim/atoms.jsonl` (schema `Atom`), `data/interim/extraction_rejects.jsonl`.

## Các bước
1. **Tách văn bản có vị trí** (`src/vnsoc/extract/pdf_to_text.py`): PyMuPDF theo trang và khối; bảng liều bằng pdfplumber; giữ số trang; tách theo đề mục (heading số La Mã/1.2.3). Bản quét → OCR + đối chiếu ảnh.
2. **Trích bằng LLM** (`atomize.py`): mỗi đề mục một yêu cầu, nhiệt độ 0, JSON theo schema rút gọn (condition, population, slot_type, intervention, value text, span, page). Qua `vnsoc.run.api_batch` (Batch, rẻ). Prompt ghi trong `configs/prompts_extract.yaml`, băm prompt vào `extraction.prompt_hash`.
3. **Kiểm khớp nguyên văn** (`verify_span.py`): `span` phải là chuỗi con của văn bản trang (sau chuẩn hóa khoảng trắng); giá trị phải parse được từ `span` bằng `normalize_vi` và khớp giá trị LLM đưa ra. Không khớp → reject (lý do).
4. **Dựng value set**: đổi sang `ValueItem` theo `value_kind`; đơn vị chuẩn; quần thể đầy đủ (tuổi/cân nặng, thai kỳ, G6PD, HBeAg, nơi đo…). Nhiều giá trị cùng hợp lệ trong văn bản hiện hành → một tập (mục 1.2).
5. **Kiểm ngữ cảnh** (T3.4 + HG3.5): công cụ `review_ui` (HTML tĩnh hoặc CSV) hiển thị span, trang, quần thể, giá trị, giá trị nước ngoài; sinh viên kiểm **100% mẩu xung đột** theo `review/adjudication_rubric.md` (đúng bệnh? đúng quần thể? đúng can thiệp? giá trị có điều kiện kèm theo?). Lần hai sau ≥ 7 ngày trên mẫu ngẫu nhiên 20% → báo cáo đồng thuận (kappa).
6. **Kiểm tra chất lượng phân tầng** (mẫu ở T3.4, người dùng kiểm ở HG3.6, tính ở T3.10): 200 mẩu (100 ngẫu nhiên + 100 xung đột); độ chính xác với KTC Clopper–Pearson; cận dưới < 90% → sửa prompt, chạy lại (DR1).

## Không được
- Điền giá trị/quần thể từ trí nhớ; sửa `span` cho khớp; gộp hai quần thể vào một mẩu.
- Dùng mẩu có `span_verified: false` hoặc `context_checked != pass` trong phân tích chính.

## Thí điểm (T1.1)
Từ `data/seed/seed_conflicts.yaml` (dòng `pilot: true`) + khoảng 10 mẩu lệch phiên bản + 30 mẩu đối chứng: tải PDF tương ứng (nguồn chính thức), tìm đoạn chứa giá trị, tạo atom có `span` + `page` thật. Dòng nào không tìm được PDF/đoạn → bỏ khỏi thí điểm và ghi lý do (không bịa). Người dùng kiểm trích dẫn ở HG1.2.
~~~~~

### `.claude/skills/certified-abstention/SKILL.md`

<!-- FILE: .claude/skills/certified-abstention/SKILL.md | sha256: da11e8d778adf9f5f804210845d72d12303365393d4e467b8be7dcae3455b359 -->
~~~~~markdown
---
name: certified-abstention
description: RQ3 — tín hiệu bất đồng, hai nhóm cố định, điểm tin cậy cross-fit, cận trên Clopper–Pearson đồng thời ở các mức trả lời cố định (kết quả chính), Learn-then-Test (phụ), hai chế độ chia, DR4/DR5 (T6.6). Dùng src/vnsoc/ltt.py.
---
# Từ chối có chứng nhận (đề cương §4.6, §4.7, §5.4)

## Tín hiệu và nhóm (cố định trước hiệu chỉnh, không dùng nhãn)
- Câu trả lời phục vụ: A2, cùng ngôn ngữ câu hỏi, nhiệt độ 0.
- Nhóm **bất đồng** nếu có ≥ 1: A1 ≠ A2 (so giá trị đã parse, không so chuỗi); VI ≠ EN ở A2; đoạn được trích dẫn (dòng NGUỒN/SOURCE) không chứa giá trị được trả lời. Còn lại: **đồng thuận**. G = 2.
- Điểm c(x): hồi quy logistic trên tín hiệu (các cờ trên, độ nhất quán 5 mẫu A2 T=0,7, log-prob câu trả lời của mô hình mở), huấn luyện cross-fit trên phần hướng dẫn tách riêng; cách tính giống hệt lúc triển khai.

## Kết quả chính: cận chứng nhận
1. Chia theo mẩu (`split_by_atom`, seed trong prereg): phần tham chiếu (lấy ngưỡng) / hiệu chỉnh / (chế độ a) đánh giá.
2. `thr = thresholds_from_reference(score_ref, group_ref, (1.0, .75, .5, .25))`.
3. `certified_bounds(score_cal, error_cal, group_cal, thr, delta=0.10)` → U_gk với độ tin cậy 1 − δ/(G·K). Báo cáo: “ở mức trả lời c, sai số nhóm g ≤ U”.
4. Phụ: `ltt_thresholds(..., make_grids(ref), alpha, delta)`; α = 0,10, trừ khi nhóm có < 300 mẩu hiệu chỉnh → α = 0,15 (DR4, quy tắc không dùng nhãn). Mức trả lời < 30% ở nhóm bất đồng → kết luận “lớp từ chối không hữu ích cho nhóm này” (DR5) — vẫn là kết quả.
5. So sánh: không từ chối; “từ chối mọi câu bất đồng”; LTT một nhóm; CRC trên rủi ro kết hợp; nhóm theo chuyên khoa.

## Đánh giá vi phạm
- (a) Chia ngẫu nhiên theo mẩu: so với sai số **toàn kho** (hiệu chỉnh ∪ kiểm tra), không so với nửa kiểm tra.
- (b) Chia theo hướng dẫn (hướng dẫn chưa thấy): 500 lần chia; tần suất vi phạm thực nghiệm; ngưỡng chấp nhận ≤ 2δ = 0,20. Không có bảo đảm lý thuyết — nói rõ.
- Báo cáo bảng chéo nhóm tín hiệu × trạng thái xung đột × loại lỗi (mô hình “cố chấp nhất quán” rơi vào nhóm đồng thuận).
- Kiểm tra mã: `$PY -m vnsoc.ltt` (mô phỏng) phải cho tỉ lệ cận bị vượt ≤ 0,10.
~~~~~

### `.claude/skills/citation-verification/SKILL.md`

<!-- FILE: .claude/skills/citation-verification/SKILL.md | sha256: dd8cf993f3d23078ab51a93769b681a3889ad502329b4581b39edde43a4ae1c7 -->
~~~~~markdown
---
name: citation-verification
description: Quản lý manuscript/references.yaml và kiểm chứng mọi trích dẫn qua Crossref/DataCite/arXiv; không bao giờ trích từ trí nhớ (T2.8, P7, P8).
---
# Trích dẫn đã kiểm chứng

- Mỗi tài liệu một mục trong `manuscript/references.yaml`: `key, title, authors, year, venue, doi | arxiv | url, checked_by_human (chỉ cho luật/quyết định/trang web, sau HG7.3)`.
- Chỉ thêm tài liệu đã mở được trang (WebFetch) hoặc tra được qua API: Crossref `https://api.crossref.org/works?query.bibliographic=<tiêu đề>&rows=5`, DataCite cho arXiv `https://api.datacite.org/dois?query=<từ khóa>&client-id=arxiv.content&page[size]=25&sort=-created`, arXiv `https://export.arxiv.org/api/query?id_list=<id>`, PubMed E-utilities `esearch.fcgi`/`esummary.fcgi` (kèm `NCBI_API_KEY` nếu có, ≤ 3 yêu cầu/giây).
- Chạy `$PY scripts/verify_citations.py` → `manuscript/citations_verified.json`; mọi mục phải `ok` hoặc `ok_manual` trước khi nộp. `MISMATCH` → sửa theo bản ghi gốc, không sửa bản ghi cho khớp bài.
- Số liệu lấy từ bài khác (ví dụ 74,5% của Wang & Suresh; 86,7–95% của Bazerbachi) phải được đối chiếu với bản gốc trước khi nộp (đề cương ghi các số này lấy qua công cụ đọc web).
- Tài liệu Việt Nam: tìm thêm trên tapchiyhocvietnam.vn (từ khóa “ChatGPT”, “phác đồ”, “Bộ Y tế”, “mô hình ngôn ngữ lớn”) — việc đề cương ghi là chưa làm được.
- Định dạng đầu ra: JMIR dùng AMA/Vancouver đánh số; IJMI dùng kiểu Elsevier số — xuất bằng pandoc + CSL khi dàn trang (T8.1).
~~~~~

### `.claude/skills/corpus-acquisition/SKILL.md`

<!-- FILE: .claude/skills/corpus-acquisition/SKILL.md | sha256: a3f62a779eba2c268d74e2bc08e8a155b908076f10f945b794dbb80683f11d35 -->
~~~~~markdown
---
name: corpus-acquisition
description: Quy trình tìm, tải, kiểm và lập danh mục văn bản hướng dẫn Bộ Y tế từ nguồn chính thức, dựng chuỗi thay thế và đóng băng kho (T2.1–T2.7). Dùng khi làm việc với data/raw, manifest, supersession.
---
# Lấy kho hướng dẫn Bộ Y tế

## Nguồn được phép (theo thứ tự)
1. `kcb.vn/phac-do`, `kcb.vn/tai-lieu`, `kcb.vn/tin-tuc` (PDF ký số của Cục Quản lý Khám, chữa bệnh).
2. `moh.gov.vn` (cổng Bộ Y tế), `vncdc.gov.vn`.
3. Trang Sở Y tế / bệnh viện đăng lại nguyên quyết định (ghi rõ host; ưu tiên bản có chữ ký số).
**Cấm**: thuvienphapluat.vn (điều khoản cấm công cụ tự động, robots `ai-train=no`) — hook chặn. Văn bản chỉ có ở đó → thêm vào danh sách người dùng tự tìm bản chính thức (HG2.3).

## Quy trình
1. **Danh mục ứng viên** (T2.1): bắt đầu từ bảng mục 3.1 đề cương (52 quyết định đã kiểm kê + các văn bản bổ sung: 1622/2014, TT 10/2024, 1470/2024, 678/2025, 5904/2019, 5642/2015, 6101/2019, 3610/2015). Mỗi văn bản một dòng `ManifestRow` (`src/vnsoc/schemas.py`), khóa `doc_key = "số/năm"`.
2. **Tìm PDF**: WebSearch với `site:kcb.vn "<số>/QĐ-BYT"` và tên bệnh; mở trang bằng WebFetch; lấy link PDF.
3. **Tải**: `curl -sSL -o data/raw/<số>_<năm>.pdf "<url>"`; rồi `sha256sum`; `pdfinfo` (số trang); `pdftotext -l 3` để kiểm có lớp chữ (≥ 200 ký tự tiếng Việt có dấu/ trang → có).
4. **Hiệu lực**: tìm trong văn bản các câu “thay thế”, “bãi bỏ”, “hết hiệu lực” (PyMuPDF search) → `supersedes`, `superseded_by`, `partially_amended_by` (ví dụ 2388/2024 chỉ thay vài chương của 3931/2015). Không suy từ trí nhớ; chưa rõ → `notes`.
5. **Chọn kho** (T2.5): 25–35 văn bản **hiện hành** có PDF chính thức có lớp chữ (`in_corpus: true`), ưu tiên bệnh giàu xung đột (dengue, sốt rét, dại, viêm gan B, tăng huyết áp, đái tháo đường, phản vệ, lao, tiêm chủng, truyền nhiễm tổng hợp); bản cũ để phân tích phiên bản không tính vào con số này; tối đa 10 văn bản OCR (Tesseract `vie`, mọi con số so với ảnh trang, ghi `ocr: true`).
6. **Đóng băng** (T2.7, không trước 15/10/2026): `$PY -m vnsoc.freeze corpus`. Văn bản ban hành sau ngày đóng băng: không thêm (DR7), chỉ ghi chú.

## Kiểm tra xong
- `$PY -m vnsoc.schemas manifest data/interim/manifest.jsonl` OK; mọi dòng `in_corpus` có `sha256`, `source_url` không phải TVPL, file PDF tồn tại.
- Báo cáo `results/tables/corpus_triage.csv`: 52+ văn bản × (có PDF chính thức?, lớp chữ?, bản quét?, chỉ thấy ở TVPL?).
- Ghi giờ công vào docs/LOG.md (ngân sách 45–100 giờ cho cả phần này).
~~~~~

### `.claude/skills/counterpart-matching/SKILL.md`

<!-- FILE: .claude/skills/counterpart-matching/SKILL.md | sha256: 93aabed542d52b9b449d9aaf9b1c1f2c7f795f444fd53f874b94768e9072724b -->
~~~~~markdown
---
name: counterpart-matching
description: Dựng kho đối chiếu nước ngoài có phiên bản, gắn giá trị nước ngoài / bản cũ / mồi cho mẩu, tính dung sai và trạng thái xung đột, đo độ nhạy và độ chính xác ghép (T2.6, T3.3, HG3.7).
---
# Ghép giá trị đối chiếu (đề cương §3.3, §4.2)

## Kho nước ngoài (`data/interim/foreign_values.jsonl`)
Mỗi dòng: chủ đề, `system` (US | EU_UK | WHO_global | WHO_WPRO | OTHER), `source` (tên hướng dẫn + năm), `version_date`, `url`, `locator` (mục/bảng/trang), `fetched_at` (ngày mở trang), `page_sha256` (băm nội dung trang/PDF đã mở — bằng chứng giá trị lấy từ nguồn chứ không từ trí nhớ), `values` (ValueItem). Trang bị chặn trong chế độ tự động (domain chưa trong danh sách cho phép) → block task, ghi domain để người dùng duyệt. **Không lưu đoạn văn** của ADA/ESC/AHA/GINA/GOLD. Ghi cả bản WHO hiện hành và bản trước (ví dụ WHO 2009 dengue → hướng dẫn arbovirus WHO 7/2025), RCUK và WAO/EAACI cho phản vệ.

## Ghép
1. Truy xuất đoạn liên quan trong nguồn nước ngoài và bản Bộ Y tế cũ (theo bệnh + slot + quần thể).
2. LLM đề xuất giá trị + vị trí; chỉ nhận khi giá trị có trong trang nguồn (kiểm bằng code với bản HTML/PDF mở).
3. So sánh bằng quy tắc: số sau quy đổi; thuốc theo INN; lịch theo dãy ngày. `vnsoc.grade.conflict_status(atom)` và `compute_tolerance(atom)` là định nghĩa duy nhất.
4. **Giá trị mồi** (`decoy`): cùng kiểu/đơn vị, khoảng cách tới giá trị Việt Nam ≈ khoảng cách của giá trị nước ngoài, phía còn lại nếu hợp lý lâm sàng, không trùng nguồn nào; kiểm bằng code rằng mẩu không thành `indistinguishable`. Với lịch/thuốc: một phác đồ có thật nhưng không phải của nguồn nào trong mẩu.
5. `conflict_family`: nhãn cho các mẩu cùng một khác biệt gốc (ví dụ `htn_threshold_us`).

## Đo chất lượng
- **Độ nhạy** trên bộ hạt giống: bao nhiêu dòng xác nhận trong `seed_conflicts.yaml` được pipeline tìm lại.
- **Độ chính xác** (HG3.7): 100 cặp ghép ngẫu nhiên → người dùng kiểm → Clopper–Pearson.
- **Độ nhạy theo kho đối chiếu**: báo cáo quy nguồn khi bỏ từng hệ thống (US/EU_UK/WHO).
- DR2: < 400 mẩu xung đột hoặc < 25 nhóm → mở rộng bệnh giàu xung đột trước ngày đóng băng câu hỏi; không hạ chuẩn xung đột.
~~~~~

### `.claude/skills/grading-protocol/SKILL.md`

<!-- FILE: .claude/skills/grading-protocol/SKILL.md | sha256: 322e9f7dfe5c9078eddcf12a2f1eefb563ad3a41ffb7b174eea95eab2104c1d2 -->
~~~~~markdown
---
name: grading-protocol
description: Chấm đầu ra bằng vnsoc.grade theo quy tắc đăng ký trước (6 nhãn, dung sai, nhiều giá trị, mồi), LLM tách đáp án dự phòng, kiểm tay bộ tách, DR9 (T1.5, T6.1, HG6.2).
---
# Chấm bằng quy tắc (đề cương §1.2, §4.5)

1. `grade_short(raw_output, atom, lang, synonyms, combos, condition=...)` cho trả lời ngắn và A6 (hỏi lại “quốc gia nào?” chỉ là nhãn 1 ở A0; ở A1–A6 là nhãn 6); `grade_mcq(output, option_roles)` cho trắc nghiệm. Tham số thuốc từ `configs/grading.yaml` (bản đóng băng).
2. Thứ tự nhãn: 1 đúng + biết bối cảnh → 2 đúng → 3 lệch phiên bản → 4 trùng nước ngoài (ghi hệ thống) → 5 không quy được nguồn (cờ `decoy_match`) → 6 từ chối. Đúng một phần / liệt kê nhiều giá trị không chỉ rõ giá trị Việt Nam → sai, báo cáo riêng (`partial`, `multi`).
3. Thiếu dòng `ĐÁP ÁN:`/`ANSWER:` và có > 1 giá trị ứng viên → `needs_llm`: gọi LLM tách đáp án (prompt cố định, API rẻ, Batch), chấm lại với `extracted=`; `parse_method: llm`.
4. **Kiểm bộ tách** (HG6.2): mẫu phân tầng 500 câu (đề cương §4.5; gồm mọi câu `parse_method=llm` nếu ≤ 250, phần còn lại phân tầng theo parse_method × mô hình × ngôn ngữ) → người dùng kiểm → báo cáo độ chính xác bộ tách kèm Clopper–Pearson. Lỗi tách > 5% hoặc tỉ lệ `needs_llm` > 5% ở một mô hình → DR9 (sửa bộ tách, tăng `grader_version`, chấm lại toàn bộ, báo cả hai).
5. Mẩu `indistinguishable` và `concordant` không vào kiểm định xác nhận H1–H3 (vẫn báo cáo mô tả).
6. Đầu ra: `data/processed/grades_v<grader_version>.parquet` (schema GradeRecord + khóa run).
~~~~~

### `.claude/skills/human-gate-protocol/SKILL.md`

<!-- FILE: .claude/skills/human-gate-protocol/SKILL.md | sha256: 8781836e405dac93553e207cf10cf0a6eb917183fc04c791ac434f5bdae1e06d -->
~~~~~markdown
---
name: human-gate-protocol
description: Cách chuẩn bị, trình bày và xác nhận các việc chỉ người dùng làm được (HG…) — tài khoản, khóa, nộp bài, email, pháp lý, bác sĩ — và cách block task đúng cách.
---
# Cổng người dùng

1. **Chuẩn bị trước**: khi một HG sắp tới (phụ thuộc gần xong), soạn sẵn mọi thứ người dùng cần: bản nháp email (tiếng Việt, lịch sự, ngắn), file cần nộp, danh sách bước bấm, thông tin cần gửi lại. Lưu ở `state/gates/<HG>.md` và nhắc trong câu trả lời.
2. **Trình bày**: mỗi HG gồm: việc gì, vì sao chỉ người làm được, các bước (đánh số), hạn, và câu cần gõ khi xong: `XONG <HG> <thông tin>`.
3. **Xác nhận**: chỉ hook UserPromptSubmit tạo `state/.human_ack/<HG>` khi một dòng tin nhắn của người dùng BẮT ĐẦU bằng `XONG <HG>`. Cổng quyết định sau hội đồng có mã HGM2/HGM3/HGM4. Bạn ghi thông tin họ đưa (URL, mã, ngày) vào file `outputs` của task (ví dụ `state/gates/HG2.9_osf.txt`), rồi `scripts/vs human-done <HG> --note "..."`.
4. **Không bao giờ**: tự tạo xác nhận; đoán rằng người dùng đã làm; gửi email/đăng ký/nộp thay; lưu mật khẩu hay khóa vào repo; mô tả AI phản biện như người thật.
5. **Block đúng cách**: task của bạn cần người dùng → `scripts/vs block <ID> --reason "<cụ thể: cần gì, ở đâu, vì sao>"`; HUMAN_TODO tự cập nhật. Khi họ cung cấp xong → `scripts/vs unblock <ID>`.
6. **Hạn gấp** (FMC 30/9/2026, đóng băng 15/10/2026, đăng ký FMC 30/11/2026): nhắc ở đầu mỗi câu trả lời khi còn ≤ 3 ngày.
~~~~~

### `.claude/skills/kaggle-vllm-runner/SKILL.md`

<!-- FILE: .claude/skills/kaggle-vllm-runner/SKILL.md | sha256: 0585912e247cce89d5ac832e409881b2ff6e2a023662ec09dea411a9ed17a484 -->
~~~~~markdown
---
name: kaggle-vllm-runner
description: Chạy mô hình mở bằng vLLM trên Kaggle 2×T4 qua Kaggle CLI (render → push → status → output), chia shard mỗi GPU một tiến trình, chạy tiếp khi đứt, đo tốc độ, lượng tử hóa (T0.4, T1.4, T5.0–T5.4).
---
# Chạy vLLM trên Kaggle

## Chuẩn bị (một lần)
- Người dùng (HG0.3): tài khoản Kaggle đã xác minh số điện thoại (bật GPU + Internet), API token (`KAGGLE_API_TOKEN` hoặc `~/.kaggle/kaggle.json`), `KAGGLE_USERNAME` trong `.env`; đồng ý điều khoản Llama 3.1 và Vistral trên Hugging Face; tạo Kaggle Secret `HF_TOKEN`. CLI `kaggle` nằm trong `.venv/bin/`.
- Secret chỉ gắn được qua giao diện và theo từng notebook, nên **chỉ một kernel cố định cần token**: `vnsoc-weights` (T4.9 đẩy lần đầu → HG5.0 người dùng gắn secret → T5.0 tải mô hình gated, lượng tử nếu cần, lưu làm output). Mọi job chạy sau gắn output đó qua `kernel_sources` (đường dẫn `/kaggle/input/vnsoc-weights/...`) nên không cần secret. Thí điểm (T1.4) chỉ dùng mô hình không gated: Qwen3-8B-AWQ trên cả 2 GPU.
- Dataset riêng tư `<user>/vnsoc-requests`: `kaggle datasets init -p data/kaggle_requests` rồi `kaggle datasets create -p data/kaggle_requests` (mặc định riêng tư — không bao giờ thêm cờ công khai `-u/--public`), các lần sau `kaggle datasets version -p data/kaggle_requests -m "<ghi chú>"`.

## Một job
1. Viết yêu cầu JSONL: `{"request_id", "model_key", "messages":[{"role":"user","content":...}], "sampling":{"temperature":0,"max_tokens":128}}` (lấy mẫu tín hiệu: `n:5, temperature:0.7, top_p:0.95`). `request_id = <question_id>|<condition>|<model_key>|<sample>`.
2. Spec job (JSON): `{"shards":[{"model_key":"qwen3_8b","model":"<hf_id hoặc /kaggle/input/...>","quantization":"awq","max_model_len":8192,"chat_template_kwargs":{"enable_thinking":false},"requests":"/kaggle/input/vnsoc-requests/<file>.jsonl","out":"/kaggle/working/<job>_qwen.jsonl"}, {… GPU 1 …}], "pip":["vllm==<phiên bản đã chạy được ở T0.4>"]}`.
3. `$PY -m vnsoc.run.kaggle_jobs render --job-id <id> --spec <spec.json>` → `kaggle/jobs/<id>/run.py` + `kernel-metadata.json` (riêng tư, GPU, Internet, `machine_shape: NvidiaTeslaT4`).
4. `$PY -m vnsoc.run.kaggle_jobs push --job-id <id>`; theo dõi `status` (mỗi 10–15 phút, không dồn dập); xong → `fetch` về `data/runs/kaggle/<id>/`.
5. Chuyển sang `RunRecord` (`src/vnsoc/run/collect.py`, T5.x viết): khớp `request_id`, gắn `prompt_hash`, `model_version` (commit HF), `backend: vllm`; kiểm schema.
6. Đứt giữa chừng (12 giờ/phiên): job mới với `resume_from` trỏ tới đầu ra cũ (gắn kernel cũ vào `kernel_sources`).

## Lưu ý kỹ thuật
- T4 = compute 7.5: không bf16 → `dtype: half` (gemma2/gemma3/glm4 bị vLLM từ chối ở fp16 → `float32` hoặc không chạy trên T4); AWQ/GPTQ chạy được; FlashAttention cần SM80+ nên vLLM tự dùng backend khác. Bản vLLM mới có thể kéo torch dựng cho CUDA mới hơn driver của Kaggle: T0.4 ghi driver (`nvidia-smi`), thử `vllm` kèm `--extra-index-url https://download.pytorch.org/whl/cu129` hoặc phiên bản cũ hơn cho tới khi chạy được, ghi phiên bản vào `configs/models.yaml`; vẫn hỏng → DR10 (HF transformers, batch nhỏ).
- Lượng tử: dùng checkpoint AWQ/GPTQ có sẵn (kiểm nguồn, giấy phép) hoặc tự tạo bằng llm-compressor (AutoAWQ đã ngừng phát triển). bitsandbytes 4-bit tại chỗ: từ vLLM 0.28 cần thêm gói `vllm-bnb-plugin` (và `bitsandbytes>=0.48.1`).
- 8B fp16 (~16 GB) không vừa một T4: dùng bản 4-bit (AWQ/GPTQ có sẵn trên HF, kiểm nguồn) hoặc tự lượng tử (T5.0), hoặc `tensor_parallel_size: 2` với `gpus: "0,1"` (ngoại lệ một tiến trình cho cả 2 GPU).
- Qwen3: luôn `chat_template_kwargs={"enable_thinking": false}`. Sailor2: `max_model_len` 4096, không chạy A4. A4 (Qwen3, Llama): shard riêng với `max_model_len: 32768` (KV cache khoảng 4–5 GB cho 32k token với bản 4-bit — vừa một T4, batch nhỏ).
- A4: sắp yêu cầu theo văn bản, đặt văn bản trước câu hỏi để tận dụng prefix caching.
- Đo tốc độ thật ở T0.4/T5.1 (token/giây vào/ra từ file `.stats.json`) và cập nhật ước tính giờ GPU; tổng dự án 50–80 giờ (tuần 7–9 theo lịch file 02). Ghi giờ mỗi job vào docs/LOG.md.
- T5.4 (lượng tử hóa): một mô hình chạy fp16 (2 GPU) trên 500 câu so với bản 4-bit; báo cáo khác biệt nhãn.
~~~~~

### `.claude/skills/question-generation/SKILL.md`

<!-- FILE: .claude/skills/question-generation/SKILL.md | sha256: 371fceee468224d6faa20191488fc8877381ac45fb0a551a18c54e44f5efee19 -->
~~~~~markdown
---
name: question-generation
description: Sinh bộ câu hỏi VI+EN (trả lời ngắn, trắc nghiệm gài đáp án, tình huống A6), kiểm quần thể, dịch và QC, gán split theo mẩu, chuẩn bị đoạn oracle cho A3 (T1.3, T4.1–T4.3).
---
# Sinh câu hỏi (đề cương §3.5, §4.3)

1. **Trả lời ngắn** (dạng chính): mẫu câu cố định theo `slot_type` (liều / ngưỡng / thời gian / lịch / thuốc đầu tay / mục tiêu / phân loại / quy trình) điền bệnh, quần thể, can thiệp; LLM chỉ diễn đạt lại cho tự nhiên (giữ nguyên số, đơn vị, quần thể — kiểm bằng code). Không chứa đáp án hay từ gợi ý nguồn. Câu hỏi A1 ghép tiền tố trong `configs/conditions.yaml`, không viết vào câu hỏi.
2. **Loại câu mơ hồ**: nếu với quần thể đã nêu, giá trị nước ngoài cũng đúng theo Bộ Y tế (ví dụ ngưỡng HA đo lưu động) → sửa quần thể hoặc loại. HA chẩn đoán phải ghi “đo tại phòng khám”.
3. **Trắc nghiệm**: lựa chọn = {Bộ Y tế, nước ngoài (hệ thống xung đột), bản cũ (nếu có), mồi}; nếu thiếu bản cũ thì 3 lựa chọn + 1 nhiễu hợp lý không thuộc nguồn nào; hai thứ tự (order_variant 0/1) sinh bằng seed cố định; `option_roles` ghi vai trò từng chữ cái.
4. **Tình huống A6**: ca bệnh ở bệnh viện huyện Việt Nam (tên địa danh chung chung), đủ dữ kiện quần thể, hỏi bước xử trí/giá trị tiếp theo; không nói “theo Bộ Y tế”. HG4.2: người dùng (hoặc bác sĩ nếu có) kiểm ≥ 100 câu.
5. **Tiếng Anh**: dịch máy (API rẻ, Batch) → dịch ngược → so bằng code: tập số và đơn vị giống hệt, phủ định giữ nguyên, quần thể giữ nguyên; lỗi → dịch lại hoặc sửa tay có ghi log. `translation_qc: pass|fail`.
6. **Đoạn oracle A3**: 150–300 từ quanh `span` trong PDF (không cắt giữa câu); `oracle_passage_id`. Chunk RAG A2: ≤ 500 token, ghi `gold_chunk_ids` (chunk chứa span).
7. **Split theo mẩu** cho RQ3: `ref` (lấy ngưỡng/lưới, ví dụ 20%), `cal` (chứng nhận), `test` (đánh giá chế độ a) — tỉ lệ và seed ghi trong prereg; chia bằng `vnsoc.ltt.split_by_atom` hai lần; mọi câu của một mẩu cùng phía.
8. **Đóng băng** (T4.3): `/freeze questions` (đóng băng cùng grading.yaml và conditions.yaml) + addendum OSF nếu có thay đổi so với bản đăng ký.

Kiểm tra xong: schema `question` OK; mỗi mẩu xung đột có đủ VI/EN × short + MCQ(2 thứ tự); tỉ lệ loại < 20% (nếu cao hơn → xem lại mẫu câu); báo cáo `results/tables/question_qc.csv`.
~~~~~

### `.claude/skills/review-panel/SKILL.md`

<!-- FILE: .claude/skills/review-panel/SKILL.md | sha256: c0e051f2fe989d8f904eff89dc140c8350b86ec66957882484df8e66374b0eb4 -->
~~~~~markdown
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
~~~~~

### `.claude/skills/statistics-plan/SKILL.md`

<!-- FILE: .claude/skills/statistics-plan/SKILL.md | sha256: efdc7e8028adb2c864d8b16c76f783a00cb51b294973244610f28ff63fd61f5a -->
~~~~~markdown
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
~~~~~

### `.claude/skills/tripod-llm-manuscript/SKILL.md`

<!-- FILE: .claude/skills/tripod-llm-manuscript/SKILL.md | sha256: 7fc7c80fcb6020cdbc3f3f7793e58de41c5a7440a43526f449e85fd9c2919fa5 -->
~~~~~markdown
---
name: tripod-llm-manuscript
description: Cấu trúc và quy tắc viết abstract FMC, slide, bản thảo JMIR Medical Informatics/IJMI theo TRIPOD-LLM, supplement S1–S6, thư nộp; số qua registry (T1.6, T4.8, T7.x, T8.1).
---
# Viết bài

## Abstract FMC (T1.6, tiếng Việt)
Theo mục 7.3 đề cương: tên 131 ký tự; bản ngắn (≤ giới hạn ô 500 — ký tự hay từ theo trả lời của ban tổ chức) và bản đầy đủ ~340 từ cho file đính kèm DOCX/PDF ≤ 1 MB. Ô `[n] [k] [a] [b] [c] [d] [e] [f]` điền bằng `{{pilot.*}}` từ registry (bản thiết kế dùng `{{design.*}}` do `src/vnsoc/analysis/design_counts.py` tính từ `data/seed/seed_conflicts.yaml`); `$PY -m vnsoc.numbers render` tạo `manuscript/build/fmc/*.md` đã điền số; DOCX tạo từ bản build; người dùng chỉ nộp bản build. Không kịp thí điểm → phương án “chỉ thiết kế” (mô tả bộ xung đột đã xác minh, thì tương lai). Ghi rõ mẫu chọn tay, chưa có bác sĩ duyệt. Tạo DOCX bằng python-docx hoặc pandoc; kiểm dung lượng.

## Bản thảo (tiếng Anh, `manuscript/main.md`)
Cấu trúc JMIR (Original Paper): Abstract có cấu trúc (Background, Objective, Methods, Results, Conclusions ≤ 450 từ) · Introduction · Methods (Guideline corpus; Recommendation atoms; Foreign and superseded counterparts; Question sets; Models and conditions; Rule-based grading; Statistical analysis; Certified abstention; Preregistration and deviations; Ethics) · Results · Discussion (principal findings, comparison with prior work, implications for medical education in Vietnam, limitations) · Conclusions · Data/code availability · AI use disclosure (ICMJE) · CRediT.
- Hình: F1 quy trình; F2 quy nguồn ở A1 theo mô hình × ngôn ngữ (nhãn 1–6, vạch mồi); F3 bậc thang ngữ cảnh A0→A4; F4 lệch phiên bản theo số tháng; F5 cận chứng nhận RQ3 theo mức trả lời. Bảng: T1 kho hướng dẫn; T2 mô hình; T3 kết quả giả thuyết H1–H4; T4 phân rã lỗi truy xuất vs cố chấp.
- Supplement: S1 danh mục văn bản + chuỗi thay thế; S2 quy tắc trích và QC; S3 prompt và điều kiện; S4 quy tắc chấm + kiểm bộ tách; S5 phân tích độ nhạy; S6 checklist TRIPOD-LLM điền đủ.
- Mọi số: `{{khóa}}`; hằng số thiết kế `{{=…}}`; `make verify` xanh; `$PY -m vnsoc.numbers render` → `manuscript/build/`.
- Giọng điệu: tuyên bố đúng mức (mục 2.4 đề cương); nêu rõ giới hạn (một quốc gia, kho 25–35 văn bản, mô hình 7–8B lượng tử, bảo đảm RQ3 không áp dụng cho hướng dẫn mới). Không gọi agent phản biện là người.
- Thư nộp (T8.1): 1 trang — vấn đề, đóng góp, vì sao hợp tạp chí, dữ liệu/mã công khai, không nộp nơi khác, đăng ký trước (link OSF), xung đột lợi ích.
~~~~~

### `.claude/skills/vn-number-normalization/SKILL.md`

<!-- FILE: .claude/skills/vn-number-normalization/SKILL.md | sha256: 573fb58b5bb4ca7926a4c555f86640211957711a6bb529438da135cdb11caf6a -->
~~~~~markdown
---
name: vn-number-normalization
description: Cách dùng và mở rộng src/vnsoc/normalize_vi.py (số kiểu Việt/Anh, khoảng, dấu so sánh, đơn vị, huyết áp, lịch tiêm, thuốc, phân loại). Dùng khi trích mẩu, ghép giá trị, chấm điểm, hoặc khi test chấm thất bại.
---
# Chuẩn hóa giá trị tiếng Việt

- Số: tiếng Việt dấu phẩy thập phân (`0,5`), dấu chấm + đúng 3 chữ số là hàng nghìn (`5.000`); `0.500` và `2.5` hiểu là thập phân; `2,000` (phẩy + `000`) là hàng nghìn. Tiếng Anh ngược lại. Hàm: `parse_number(tok, lang)`.
- Giá trị: `parse_nums(text, lang)` → `Num(lo, hi, unit, cmp)`; khoảng (`10 - 15`, `từ … đến …`, `0,5–1`), dấu so sánh (≥, trên, dưới, tối đa, at least…). Trích dẫn văn bản (`QĐ 2760/QĐ-BYT`, `1740/2026`) và năm đứng riêng (`ADA 2025`) bị loại trước khi đọc số.
- Đơn vị chuẩn trong `UNIT_ALIASES` (ví dụ `ml/kg/giờ`→`ml/kg/h`, `µg|mcg`→`ug`, `/mm3`→`/uL`). Quy đổi `convert(v, from, to, ctx)`; ngữ cảnh mẩu (`Atom.context`): `weight_kg`, `mg_per_ml`, `mg_per_tablet`, `mg_per_ampoule`, `analyte` (glucose/ldl/triglyceride cho mg/dL↔mmol/L).
- Huyết áp `parse_bps` (loại cặp không hợp lý như `30/19 U/L`); lịch `parse_schedules` (`N0-3-7-14-28`, `ngày 0, 3, 7, 14`, `2, 3, 4 tháng`); thuốc `parse_drugs` theo `configs/grading.yaml` (bí danh INN + tổ hợp); phân loại `parse_cats` theo `cat_options` của mẩu.

## Khi thêm quy tắc
1. Viết test trong `tests/test_normalize.py` trước (ca gốc lấy từ văn bản thật, ghi nguồn trong comment).
2. Sửa tối thiểu; chạy toàn bộ `make test`.
3. Sau khi đóng băng câu hỏi (T4.3): mọi thay đổi ảnh hưởng chấm điểm → tăng `grader_version` trong configs/grading.yaml (tạo bản mới, không sửa bản đóng băng), ghi DECISIONS, chấm lại toàn bộ và báo cả hai.
~~~~~

### `configs/budget.yaml`

<!-- FILE: configs/budget.yaml | sha256: a8c70c26442632a2c99b33191173fd6a448b22f5aae04ca8d0e21a0653621b7c -->
~~~~~yaml
# Trần cứng API trả phí (USD). Không có ngoại lệ. Ngoài ra người dùng đặt giới hạn chi tiêu ở trang
# quản trị của từng nhà cung cấp (HG0.3). Giá kiểm tra ngày 2026-09-25 — kiểm lại ở T0.5.
cap_usd: 40
safety_margin_usd: 2
plan_usd:
  pilot: 2
  extraction_matching_qgen_translation: 6
  cheap_api_runs: 12
  frontier_runs: 16
  reserve: 4
~~~~~

### `configs/conditions.yaml`

<!-- FILE: configs/conditions.yaml | sha256: 90c1fe267816d08250fe9b2701893705b5a4355ea0c422781aaa0e2ba1995eb2 -->
~~~~~yaml
# Điều kiện hỏi A0–A6 và giải mã (đăng ký trước, mục 4.4 đề cương).
decoding: {temperature: 0.0, max_tokens: 128, seed: 0}
signal_sampling: {condition: A2, n: 5, temperature: 0.7, top_p: 0.95}   # chốt trong OSF trước khi chạy
rag:
  embedder: BAAI/bge-m3
  mode: hybrid_dense_sparse
  chunk_max_tokens: 500
  k: 5
a3_passage_words: [150, 300]
a4: {max_context_tokens: 28000, max_model_len: 32768, subset_size: 300, models: [qwen3_8b, llama31_8b], prefix_caching: true}
conditions:
  A0: {role: descriptive, context: none, country_cue: false}
  A1: {role: confirmatory, context: none, country_cue: true}
  A2: {role: deployment_served, context: rag_moh}
  A3: {role: mechanism, context: oracle_passage}
  A4: {role: comparison_eur_radiol, context: full_chapter, subset: true}
  A5: {role: exploratory, context: rag_mixed_moh_who_us}
  A6: {role: exploratory_rq4, context: vn_hospital_vignette, country_cue: implicit}
prompts:
  vi:
    answer_line: "Trả lời ngắn gọn. Dòng cuối cùng bắt buộc có dạng: ĐÁP ÁN: <giá trị> <đơn vị>"
    A0: "{question}\n{answer_line}"
    A1: "Theo hướng dẫn chẩn đoán và điều trị hiện hành của Bộ Y tế Việt Nam, {question}\n{answer_line}"
    A2: "Các đoạn trích từ hướng dẫn của Bộ Y tế Việt Nam:\n{passages}\n\nDựa vào các đoạn trích trên, {question}\nGhi mã đoạn đã dùng ở dòng: NGUỒN: [P?]\n{answer_line}"
    A3: "Đoạn trích từ QĐ {doc}, mục {section}:\n\"\"\"{passage}\"\"\"\nDựa vào đoạn trích, {question}\n{answer_line}"
    A4: "Nội dung chương liên quan trong hướng dẫn của Bộ Y tế ({doc}):\n\"\"\"{chapter}\"\"\"\n\nDựa vào nội dung trên, {question}\n{answer_line}"
    A5: "Các đoạn trích từ hướng dẫn y khoa:\n{passages}\n\nTheo hướng dẫn chẩn đoán và điều trị hiện hành của Bộ Y tế Việt Nam, {question}\nGhi mã đoạn đã dùng ở dòng: NGUỒN: [P?]\n{answer_line}"
    A6: "{vignette}\n{answer_line}"
    mcq: "{stem}\n{options}\nChỉ chọn một phương án. Dòng cuối: ĐÁP ÁN: <chữ cái>"
  en:
    answer_line: "Answer briefly. The last line must be: ANSWER: <value> <unit>"
    A0: "{question}\n{answer_line}"
    A1: "According to the current diagnosis and treatment guidelines of the Vietnamese Ministry of Health, {question}\n{answer_line}"
    A2: "Excerpts from Vietnamese Ministry of Health guidelines:\n{passages}\n\nBased on the excerpts above, {question}\nState the excerpt IDs you used on a line: SOURCE: [P?]\n{answer_line}"
    A3: "Excerpt from Decision {doc}, section {section}:\n\"\"\"{passage}\"\"\"\nBased on the excerpt, {question}\n{answer_line}"
    A4: "Relevant chapter of the Vietnamese Ministry of Health guideline ({doc}):\n\"\"\"{chapter}\"\"\"\n\nBased on the text above, {question}\n{answer_line}"
    A5: "Excerpts from medical guidelines:\n{passages}\n\nAccording to the current diagnosis and treatment guidelines of the Vietnamese Ministry of Health, {question}\nState the excerpt IDs you used on a line: SOURCE: [P?]\n{answer_line}"
    A6: "{vignette}\n{answer_line}"
    mcq: "{stem}\n{options}\nChoose one option only. Last line: ANSWER: <letter>"
~~~~~

### `configs/grading.yaml`

<!-- FILE: configs/grading.yaml | sha256: 44a07ce01b66f771bec0133d3b688423a057024af359252a5d70292b4cb767c2 -->
~~~~~yaml
# Quy tắc chấm (đăng ký trước). grader_version tăng khi đổi bất kỳ thứ gì dưới đây → chấm lại toàn bộ.
grader_version: "1.0.0"
tolerance_rule: "half the minimum gap between the MoH value set and any other source value (foreign, superseded, decoy)"
partial_overlap: wrong_in_primary_reported_separately
multi_value_without_vn_designation: wrong_reported_separately
llm_extraction_fallback: {used_only_when: "no ĐÁP ÁN/ANSWER line and >1 candidate values", manual_check_n: 500}
drugs:            # INN chuẩn -> bí danh (không dấu, chữ thường sau chuẩn hóa). Mở rộng khi gặp thuốc mới + thêm test.
  artemether-lumefantrine: [artemether-lumefantrin, coartem, riamet]
  artemether: []
  lumefantrine: [lumefantrin]
  pyronaridine-artesunate: [pyronaridin-artesunat, pyramax]
  pyronaridine: [pyronaridin]
  artesunate: [artesunat]
  dihydroartemisinin-piperaquine: [dihydroartemisinin-piperaquin, dha-ppq, arterakine, eurartesim]
  primaquine: [primaquin]
  tafenoquine: [tafenoquin, krintafel, arakoda]
  quinine: [quinin]
  clindamycin: [clindamycine]
  chloroquine: [cloroquin, chloroquin]
  adrenaline: [adrenalin, epinephrine, epinephrin]
  bedaquiline: [bedaquilin]
  pretomanid: []
  linezolid: []
  moxifloxacin: [moxifloxacine]
  tenofovir-disoproxil: [tdf, tenofovir disoproxil fumarate]
  tenofovir-alafenamide: [taf]
  entecavir: [etv]
  dolutegravir: [dtg]
  lamivudine: [3tc, lamivudin]
combos:
  artemether-lumefantrine: [artemether, lumefantrine]
  pyronaridine-artesunate: [pyronaridine, artesunate]
  quinine+clindamycin: [quinine, clindamycin]
  BPaLM: [bedaquiline, pretomanid, linezolid, moxifloxacin]
  BPaL: [bedaquiline, pretomanid, linezolid]
~~~~~

### `configs/models.yaml`

<!-- FILE: configs/models.yaml | sha256: 9bbc0060cb9606cb27297546d256fee45914b61b7af80314eeefe1d25cda8d1a -->
~~~~~yaml
# Mô hình. KHÔNG đoán tên/ID: T0.4 (Kaggle) và T0.5 (API) xác minh và điền các ô FILL_*.
# Ghi phiên bản thực tế (commit hash HF / ngày gọi API) vào results/model_versions.json khi chạy.
open:
  - key: qwen3_8b
    hf_id: Qwen/Qwen3-8B-AWQ            # xác minh repo; bản gốc Qwen/Qwen3-8B
    license: Apache-2.0
    quantization: awq
    dtype: half                          # T4 không có bf16
    max_model_len: 8192
    chat_template_kwargs: {enable_thinking: false}
    gated: false
    runs_A4: true
  - key: llama31_8b
    hf_id: meta-llama/Llama-3.1-8B-Instruct   # gated (HG0.3); cần bản 4-bit để vừa 1 T4 — T5.0 chọn AWQ/GPTQ có sẵn hoặc tự lượng tử
    license: Llama 3.1 Community License
    quantization: FILL_AT_T5.0
    dtype: half
    max_model_len: 8192
    gated: true
    runs_A4: true
    note: "Không chính thức hỗ trợ tiếng Việt"
  - key: sailor2_8b
    hf_id: sail/Sailor2-8B-Chat
    license: Apache-2.0
    quantization: FILL_AT_T5.0           # ~8.9B tham số: fp16 không vừa 1 T4 → AWQ/GPTQ hoặc tensor_parallel=2
    dtype: half
    max_model_len: 4096                   # không chạy A4
    gated: false
    runs_A4: false
  - key: vistral_7b
    hf_id: Viet-Mistral/Vistral-7B-Chat
    license: AFL-3.0 (phải đồng ý điều khoản trên HF — HG0.3)
    quantization: FILL_AT_T5.0           # tự lượng tử bằng llm-compressor (AutoAWQ đã ngừng); không được thì fp16 trên 2 GPU
    dtype: half
    max_model_len: 8192
    gated: true
    runs_A4: false
optional:
  - key: medgemma_4b
    hf_id: google/medgemma-4b-it
    backend: hf_transformers_fp32_2gpu
    note: "Tùy chọn, tập con; gemma3 không chạy fp16 trên vLLM"
api_cheap:
  - key: cheap_1
    provider: google
    model: FILL_AT_T0.5                  # ứng viên: Gemini 3.1 Flash-Lite
    price_in: 0.25
    price_out: 1.50
    price_checked: 2026-09-25
    max_tokens: 128
    reasoning_allowance: 256
    extra_generation: {}                 # điều khiển thinking tối thiểu — điền từ tài liệu chính thức ở T0.5
  - key: cheap_2
    provider: openai
    model: FILL_AT_T0.5                  # hạng rẻ nhất
    price_in: 0.20
    price_out: 1.20
    price_checked: 2026-09-25
    max_tokens: 128
    reasoning_allowance: 256
    extra: {}                            # vd reasoning_effort tối thiểu — điền ở T0.5
    endpoint: /v1/chat/completions
api_frontier:
  - key: frontier_1
    provider: google
    model: FILL_AT_T0.5                  # ứng viên: Gemini 3.1 Pro Preview
    price_in: 2.0
    price_out: 12.0
    price_checked: 2026-09-25
    max_tokens: 128
    reasoning_allowance: 512
    extra_generation: {}
~~~~~

### `configs/project.yaml`

<!-- FILE: configs/project.yaml | sha256: e5f31f64f57ae11bfc5877fae4104023e53414d791bc77695cdc58a358f2c98a -->
~~~~~yaml
# Hằng số của nghiên cứu (đăng ký trước). Đổi bất kỳ giá trị nào sau khi nộp OSF → ghi docs/DECISIONS.md
# + addendum trong prereg/addenda/ + báo người dùng. Nguồn: docs/01_DE_CUONG.md.
title_vi: "Chuẩn điều trị của ai? Sai lệch theo chuẩn nước ngoài và theo phiên bản cũ của LLM so với hướng dẫn chuyên môn của Bộ Y tế Việt Nam"
title_en: "Whose Standard of Care? Jurisdictional Defaults, Guideline Staleness and Certified Abstention of LLMs on Vietnamese Ministry of Health Guidelines"
dates:
  fmc_abstract_deadline: 2026-09-30
  fmc_notification_by: 2026-10-15
  fmc_registration_by: 2026-11-30
  fmc_conference: 2026-12-12
  corpus_freeze: 2026-10-15
  journal_submission_window: [2027-01-11, 2027-01-24]
corpus:
  n_current_guidelines: [25, 35]
  max_ocr_documents: 10
  official_hosts: [kcb.vn, moh.gov.vn, vncdc.gov.vn]
  forbidden_hosts: [thuvienphapluat.vn]
targets:
  min_conflict_atoms: 400
  min_conflict_families: 25
  extraction_audit_n: 200            # 100 random + 100 conflict
  extraction_precision_cp_lower: 0.90
  counterpart_precision_audit_n: 100
  clinician_vignettes_checked: 100     # ưu tiên bác sĩ; không có thì sinh viên kiểm và ghi rõ
  parser_check_n: 500
hypotheses:
  primary: H1
  secondary_family: [H2, H3, H4]     # Holm within family
  H3_margin: 0.05
  H4_rr_lower_bound: 2.0
  ci_level: 0.95
rq3:
  groups: [agree, disagree]
  coverages: [1.0, 0.75, 0.5, 0.25]
  alpha: 0.10
  delta: 0.10
  alpha_fallback: 0.15               # only if a group has < 300 calibration atoms (label-free rule)
  alpha_fallback_min_cal_atoms: 300
  min_useful_coverage: 0.30
  regime_b_splits: 500
  regime_b_max_violation_rate: 0.20  # = 2 * delta
  split_unit: atom
  split_fractions: {ref: 0.2, cal: 0.4, test: 0.4}   # đề xuất; chốt trong bản OSF (T2.10)
  split_seed: 20261001
decision_rules_file: docs/02_KE_HOACH_TRIEN_KHAI.md  # DR1–DR10
cut_order: [A5_A6, A4, frontier_to_1, cheap_api_to_1, open_models_to_3]
journals: [JMIR Medical Informatics, International Journal of Medical Informatics]
reporting: TRIPOD-LLM
~~~~~

### `data/seed/seed_conflicts.yaml`

<!-- FILE: data/seed/seed_conflicts.yaml | sha256: 455db5474853f34105148f810d76af0c95b33c4f0e2709a4a2add2e0355b70cc -->
~~~~~yaml
# Bộ xung đột hạt giống — chép từ bảng mục 3.3 đề cương (sau phản biện vòng 2).
# CHƯA PHẢI DỮ LIỆU NGHIÊN CỨU: mọi dòng phải được đối chiếu lại với PDF chính thức (trích nguyên văn,
# số trang, quần thể) trước khi dùng — task T1.1 (Claude soạn) + HG1.2 (người dùng kiểm tra trích dẫn).
# Không có trường quote/page ở đây vì chưa kiểm; KHÔNG được tự điền từ trí nhớ.
# pilot: dùng cho thí điểm tuần 0 (mục 5.7). status theo cột "Trạng thái sau vòng 2".
rows:
  - {row: 1, topic: "Dengue, sốc ở người lớn: tốc độ dịch đầu", vn_doc: "2760/2023", vn_locator: "mục C.2.1",
     vn: "Ringer lactat hoặc NaCl 0,9% 15 ml/kg/giờ, rồi 10 ml/kg/giờ × 2 giờ", value_kind: num, unit: ml/kg/h,
     foreign: [{system: WHO_global, source: "WHO 2009 dengue", value: "5–10 ml/kg/giờ trong 1 giờ"}],
     superseded: [{doc: "3705/2019", value: "cần tra"}],
     status: confirmed, pilot: true, note: "Đối chiếu thêm hướng dẫn arbovirus WHO 7/2025"}
  - {row: 2, topic: "Dengue: truyền tiểu cầu", vn_doc: "2760/2023", vn: "< 5.000/mm³ (cân nhắc) hoặc < 50.000/mm³ kèm xuất huyết nặng hoặc cần chọc dịch",
     value_kind: num, unit: /uL, foreign: [{system: WHO_global, source: "WHO 2009", value: "không truyền dự phòng khi huyết động ổn"}],
     status: confirmed_complex, pilot: false, note: "Nhiều điều kiện; không dùng cho thí điểm"}
  - {row: 3, topic: "Tay chân miệng: phân độ và thuốc", vn_doc: "292/2024", vn: "Độ 1/2a/2b/3/4; gammaglobulin 1 g/kg; phenobarbital; milrinon",
     foreign: [{system: US, source: "CDC", value: "điều trị hỗ trợ"}], status: no_counterpart, pilot: false,
     note: "Cần WHO khu vực 2011 làm mốc"}
  - {row: 4, topic: "Dại: phác đồ sau phơi nhiễm, tiêm bắp", vn_doc: "1622/2014", vn: "N0-3-7-14-28", value_kind: schedule,
     foreign: [{system: US, source: "CDC PEP", value: "0-3-7-14"}], status: confirmed, pilot: true}
  - {row: 5, topic: "Dại: phác đồ sau phơi nhiễm, trong da", vn_doc: "1622/2014", vn: "N0-3-7-28", value_kind: schedule,
     foreign: [{system: WHO_global, source: "WHO 2018 rabies position", value: "phác đồ trong da 1 tuần"}], status: confirmed, pilot: true}
  - {row: 6, topic: "Tăng huyết áp: ngưỡng chẩn đoán đo tại phòng khám", vn_doc: "3192/2010", vn: "≥ 140/90 mmHg", value_kind: bp,
     foreign: [{system: US, source: "AHA/ACC 2025", value: "≥ 130/80"}, {system: EU_UK, source: "ESC", value: "140/90"},
               {system: WHO_global, source: "WHO", value: "140/90"}],
     status: confirmed_us_only, pilot: true, note: "Câu hỏi phải nói rõ đo tại phòng khám (130/80 là ngưỡng đo lưu động của chính Bộ Y tế)"}
  - {row: 7, topic: "Tăng huyết áp: mục tiêu ở người ≥ 65 tuổi", vn_doc: "5904/2019", vn: "130 đến < 140 mmHg (tâm thu)", value_kind: num, unit: mmHg,
     foreign: [{system: US, source: "AHA/ACC", value: "< 130/80"}, {system: EU_UK, source: "ESC 2024", value: "120–129"}],
     status: confirmed, pilot: true, note: "Ghi phiên bản ESC"}
  - {row: 8, topic: "ĐTĐ: tuổi bắt đầu sàng lọc tất cả", vn_doc: "5481/2020", vn: "từ 45 tuổi", value_kind: num, unit: year,
     foreign: [{system: US, source: "ADA 2025", value: "từ 35 tuổi"}], status: confirmed_low_stakes, pilot: false}
  - {row: 9, topic: "ĐTĐ: mục tiêu huyết áp", vn_doc: "5481/2020", vn: "< 140/90; < 130/80 nếu có biến chứng thận hoặc nguy cơ cao", value_kind: bp,
     foreign: [{system: US, source: "ADA 2025", value: "< 130/80 nếu an toàn"}], status: confirmed, pilot: true,
     note: "Câu hỏi phải nói rõ: không có biến chứng thận, không nguy cơ cao"}
  - {row: 10, topic: "ĐTĐ có bệnh tim mạch xơ vữa: mục tiêu LDL-C", vn_doc: "5481/2020", vn: "< 70 mg/dL, có thể < 50", value_kind: num, unit: mg/dL,
     foreign: [{system: US, source: "ADA 2025", value: "< 55 mg/dL"}], status: fixed, pilot: true,
     note: "Tập giá trị Việt Nam gồm cả < 50; analyte ldl"}
  - {row: 11, topic: "ĐTĐ: ngưỡng bắt đầu insulin sớm", vn_doc: "5481/2020", vn: "A1C ≥ 9% hoặc glucose ≥ 300 mg/dL", value_kind: num, unit: "%",
     foreign: [{system: US, source: "ADA", value: "A1C > 10% hoặc glucose ≥ 300"}], status: confirmed, pilot: true,
     note: "Tách 2 mẩu: A1C (xung đột) và glucose (trùng)"}
  - {row: 12, topic: "ĐTĐ: vị trí GLP-1 RA/SGLT2i", status: removed, pilot: false, note: "Khác mức khuyến cáo, không phải giá trị"}
  - {row: 13, topic: "Béo phì: ngưỡng BMI", vn_doc: "2892/2022", vn: "thừa cân 23–24,9; béo phì độ I 25–29,9", value_kind: num, unit: kg/m2,
     foreign: [{system: WHO_WPRO, source: "WHO châu Á", value: "trùng Việt Nam"}, {system: WHO_global, source: "WHO", value: "béo phì ≥ 30"}],
     status: fixed_relabelled, pilot: false, note: "Trùng WHO khu vực; chỉ dùng nếu kịp đối chiếu lại"}
  - {row: 14, topic: "Phản vệ: adrenalin tiêm bắp người lớn", status: removed, pilot: false, note: "0,5 mg nằm trong 0,5–1 mg — dùng làm ca kiểm thử 'đúng'"}
  - {row: 15, topic: "Phản vệ: liều adrenalin trẻ khoảng 10 kg", vn_doc: "TT 51/2017", vn: "0,25 ml (250 µg) adrenalin 1 mg/ml", value_kind: num, unit: ug,
     foreign: [{system: EU_UK, source: "RCUK 2021", value: "150 µg cho 6 tháng–6 tuổi"}, {system: OTHER, source: "WAO", value: "0,01 mg/kg"}],
     status: confirmed, pilot: true, note: "Cần quy tắc cân nặng–tuổi: câu hỏi nêu cả tuổi và cân nặng; context mg_per_ml=1, weight_kg=10"}
  - {row: 16, topic: "Sốt rét P. falciparum: thuốc đầu tay", vn_doc: "3377/2023", vn: "pyronaridin–artesunat 3 ngày + primaquin", value_kind: drugs,
     foreign: [{system: US, source: "CDC", value: "artemether–lumefantrin"}, {system: WHO_global, source: "WHO", value: "chấp nhận cả hai"}],
     status: confirmed_us_only, pilot: true}
  - {row: 17, topic: "Sốt rét P. falciparum, 3 tháng đầu thai kỳ", vn_doc: "3377/2023", vn: "quinin 7 ngày + clindamycin 7 ngày", value_kind: drugs,
     foreign: [{system: US, source: "CDC", value: "artemether–lumefantrin"}], status: confirmed, pilot: true}
  - {row: 18, topic: "Primaquin liều đơn cho P. falciparum, ≥ 15 tuổi", vn_doc: "3377/2023", vn: "4 viên × 7,5 mg = 30 mg", value_kind: num, unit: mg,
     foreign: [{system: WHO_global, source: "WHO", value: "0,25 mg/kg"}], status: fixed, pilot: false,
     note: "Chỉ dùng nếu kịp đối chiếu; cần cân nặng trong câu hỏi; context mg_per_tablet=7.5"}
  - {row: 19, topic: "P. vivax: điều trị tiệt căn (G6PD bình thường)", vn_doc: "3377/2023", vn: "primaquin 0,5 mg/kg/ngày × 7 ngày", value_kind: num, unit: mg/kg/day,
     foreign: [{system: US, source: "CDC", value: "30 mg/ngày × 14 ngày hoặc tafenoquin 300 mg"}], status: confirmed, pilot: true,
     note: "Có thể tách thành mẩu liều và mẩu thời gian"}
  - {row: 20, topic: "Viêm gan B: chỉ định điều trị", vn_doc: "1740/2026", vn: "HBV DNA > 2.000 IU/mL và ALT > giới hạn trên (30 nam, 19 nữ)", value_kind: num, unit: U/L,
     foreign: [{system: US, source: "AASLD 2025", value: "ALT ≥ 2× giới hạn trên (35/25) và HBV DNA theo HBeAg"}],
     superseded: [{doc: "3310/2019", value: "cần tra"}], status: confirmed, pilot: true,
     note: "Thêm mẩu riêng cho xơ hóa (APRI > 0,5 hoặc FibroScan > 7 kPa); PDF có trên kcb.vn/tai-lieu"}
  - {row: 21, topic: "Viêm gan B: dự phòng lây mẹ sang con", vn_doc: "678/2025", status: unverified, pilot: false,
     foreign: [{system: US, source: "AASLD", value: "tuần 28"}], note: "Có thể mâu thuẫn với 1740/2026"}
  - {row: 22, topic: "Lao đa kháng: phác đồ", vn_doc: "162/2024", vn: "BPaL(M)", value_kind: drugs,
     superseded: [{doc: "2760/2021", value: "cần tra"}], foreign: [{system: WHO_global, source: "WHO 2022", value: "BPaLM"}],
     status: version_drift, pilot: true, note: "Dùng làm mẩu lệch phiên bản 2760/2021 → 162/2024"}
  - {row: 23, topic: "Vắc-xin sởi: mũi đầu", vn_doc: "TT 10/2024", vn: "9 tháng tuổi", value_kind: num, unit: month,
     foreign: [{system: US, source: "CDC", value: "12–15 tháng"}, {system: WHO_global, source: "WHO", value: "giống Việt Nam"}],
     status: confirmed_us_only_not_rechecked, pilot: true}
  - {row: 24, topic: "DTP: lịch cơ bản", vn_doc: "TT 10/2024", vn: "2, 3, 4 tháng", value_kind: schedule,
     foreign: [{system: US, source: "CDC", value: "2, 4, 6 tháng"}], status: confirmed_low_stakes_not_rechecked, pilot: false}
  - {row: 25, topic: "Sàng lọc ĐTĐ thai kỳ", vn_doc: "1470/2024", vn: "75 g một bước", value_kind: cat,
     foreign: [{system: US, source: "ACOG", value: "ưu tiên hai bước"}], status: confirmed_low_stakes_not_rechecked, pilot: false}
version_drift_pilot:
  - {topic: "Viêm gan B", from: "3310/2019", to: "1740/2026"}
  - {topic: "Dengue", from: "3705/2019", to: "2760/2023"}
  - {topic: "Lao đa kháng", from: "2760/2021", to: "162/2024"}
concordant_controls: [
  "phân loại dengue và dấu hiệu cảnh báo", "HIV bậc một TDF + 3TC + DTG", "COPD theo GOLD", "hen theo GINA",
  "tiêu sợi huyết trong 4,5 giờ", "artesunat cho sốt rét ác tính", "tiêu chuẩn chẩn đoán đái tháo đường",
  "ngưỡng ĐTĐ thai kỳ 5,1/10,0/8,5 mmol/L", "điều trị bệnh Whitmore"]
~~~~~

### `docs/DECISIONS.md`

<!-- FILE: docs/DECISIONS.md | sha256: c97ba4587b79361df7f1b2cbeba643ca93d59cb6f855b2087e6cf06b851b9232 -->
~~~~~markdown
# Quyết định (DR) đã áp dụng

Mỗi dòng: thời điểm · mã quy tắc (DR1–DR10) hoặc lý do · tác động · ai duyệt.
~~~~~

### `docs/LOG.md`

<!-- FILE: docs/LOG.md | sha256: c64a06997afc84b3d2ce375d77b328be18f8968f765c7e03488cf672e461ac8e -->
~~~~~markdown
# Nhật ký dự án (tự động + ghi tay)
~~~~~

### `kaggle/runner_template.py`

<!-- FILE: kaggle/runner_template.py | sha256: 7e5c25abc649edc7ed6fd58f2cf32431551bfb88d305f3126bd4df7a0c204ac7 -->
~~~~~python
# Kaggle GPU runner (2×T4). Rendered per job by vnsoc.run.kaggle_jobs: __JOB__ is replaced with JSON.
# One vLLM process per GPU (data parallel), greedy decoding unless the request says otherwise,
# results flushed every batch to /kaggle/working so a timeout still leaves partial output.
# T4 = compute capability 7.5: no bf16 -> dtype "half" (gemma2/gemma3/glm4 refuse fp16 in vLLM -> "float32"
# or do not run them on T4); FlashAttention needs SM80+, vLLM falls back to another attention backend.
import json
import os
import subprocess
import sys
import time

JOB = json.loads(r'''__JOB__''')

WORKER = r'''
import json, os, sys, time


def main():
    shard = json.loads(sys.argv[1])
    from vllm import LLM, SamplingParams
    import vllm
    t0 = time.time()
    kw = dict(model=shard["model"], dtype=shard.get("dtype", "half"),
              max_model_len=shard.get("max_model_len", 8192),
              gpu_memory_utilization=shard.get("gpu_memory_utilization", 0.90),
              enable_prefix_caching=True, seed=0,
              tensor_parallel_size=shard.get("tensor_parallel_size", 1))
    if shard.get("quantization") not in (None, "none"):
        kw["quantization"] = shard["quantization"]
    llm = LLM(**kw)
    load_s = time.time() - t0
    reqs = [json.loads(l) for l in open(shard["requests"], encoding="utf-8") if l.strip()]
    reqs = [r for r in reqs if r.get("model_key") == shard["model_key"]] or reqs
    out_path = shard["out"]
    done = set()
    for prev in [out_path, *shard.get("resume_from", [])]:  # resume_from: earlier outputs under /kaggle/input
        if os.path.exists(prev):
            done |= {json.loads(l)["request_id"] for l in open(prev, encoding="utf-8") if l.strip()}
    todo = [r for r in reqs if r["request_id"] not in done]
    groups = {}
    for r in todo:
        s = r.get("sampling", {})
        key = (s.get("temperature", 0.0), s.get("top_p", 1.0), s.get("n", 1), s.get("max_tokens", 128))
        groups.setdefault(key, []).append(r)
    n_tok_out, t_gen = 0, time.time()
    with open(out_path, "a", encoding="utf-8") as f:
        for (temp, top_p, n, mx), rs in groups.items():
            sp = SamplingParams(temperature=temp, top_p=top_p, n=n, max_tokens=mx, seed=0, logprobs=1)
            B = shard.get("batch", 256)
            for i in range(0, len(rs), B):
                chunk = rs[i:i + B]
                outs = llm.chat([r["messages"] for r in chunk], sp, use_tqdm=False,
                                chat_template_kwargs=shard.get("chat_template_kwargs") or None)
                for r, o in zip(chunk, outs):
                    n_tok_out += sum(len(c.token_ids) for c in o.outputs)
                    f.write(json.dumps({"request_id": r["request_id"], "outputs": [c.text for c in o.outputs],
                                        "tokens_in": len(o.prompt_token_ids),
                                        "tokens_out": [len(c.token_ids) for c in o.outputs],
                                        "cum_logprob": [c.cumulative_logprob for c in o.outputs],
                                        "model_key": shard["model_key"], "vllm": vllm.__version__},
                                       ensure_ascii=False) + "\n")
                f.flush()
                print(f"[{shard['model_key']}] {i + len(chunk)}/{len(rs)} done", flush=True)
    stats = {"model_key": shard["model_key"], "load_s": load_s, "gen_s": time.time() - t_gen,
             "requests": len(todo), "tokens_out": n_tok_out, "vllm": vllm.__version__}
    open(out_path + ".stats.json", "w").write(json.dumps(stats))
    print(json.dumps(stats), flush=True)


if __name__ == "__main__":
    main()
'''


def sh(cmd: str) -> None:
    print("+", cmd, flush=True)
    subprocess.run(cmd, shell=True, check=True)


def main() -> None:
    os.chdir("/kaggle/working")
    sh("nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv")
    if JOB.get("pip"):
        # e.g. ["vllm==<version found at T0.4>", "--extra-index-url", "https://download.pytorch.org/whl/cu129"]
        sh("pip install -q " + " ".join(JOB["pip"]))
    try:
        from kaggle_secrets import UserSecretsClient

        tok = UserSecretsClient().get_secret("HF_TOKEN")
        if tok:
            os.environ["HF_TOKEN"] = tok
            os.environ["HUGGING_FACE_HUB_TOKEN"] = tok
    except Exception as e:  # secret not attached to THIS kernel: gated models will fail with a clear error
        print("HF_TOKEN secret not available:", type(e).__name__, flush=True)
    open("worker.py", "w").write(WORKER)
    procs = []
    for gpu, shard in enumerate(JOB["shards"]):
        env = dict(os.environ, CUDA_VISIBLE_DEVICES=shard.get("gpus", str(gpu)))
        procs.append(subprocess.Popen([sys.executable, "worker.py", json.dumps(shard)], env=env))
        time.sleep(20)  # stagger model loading
    codes = [p.wait() for p in procs]
    json.dump({"job_id": JOB["job_id"], "exit_codes": codes}, open("job_status.json", "w"))
    if any(codes):
        sys.exit(1)


if __name__ == "__main__":
    main()
~~~~~

### `scripts/autopilot.sh`

<!-- FILE: scripts/autopilot.sh | sha256: 9e8c0a2475e3327fa8a056a86e9f9d4158a4924f8e59491dce584f8d714a002a -->
~~~~~bash
#!/usr/bin/env bash
# Chạy Claude Code không cần ngồi canh: mỗi vòng gọi `claude -p "/next"`; hook Stop giữ Claude làm
# liên tục trong một vòng. Dừng khi: có state/PAUSE, hết việc Claude làm được, hoặc đủ số vòng.
# Dùng:  scripts/autopilot.sh [số_vòng=20] [max_turns_mỗi_vòng=150]
# CHỈ NGƯỜI DÙNG chạy script này ở terminal (hook chặn Claude tự gọi nó).
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
ROUNDS="${1:-20}"; TURNS="${2:-150}"
mkdir -p logs/autopilot
scripts/vs autopilot on >/dev/null
for i in $(seq 1 "$ROUNDS"); do
  if [ -f state/PAUSE ]; then echo "PAUSE → dừng"; break; fi
  NEXT="$(scripts/vs next --id-only 2>/dev/null || true)"
  if [ -z "$NEXT" ] || [ "$NEXT" = "NONE" ]; then echo "Không còn việc Claude làm được ngay → dừng"; break; fi
  TS="$(date +%Y%m%d-%H%M%S)"
  echo "[$TS] vòng $i: $NEXT"
  claude -p "/next" --permission-mode acceptEdits --max-turns "$TURNS" --output-format json \
    > "logs/autopilot/$TS.json" 2> "logs/autopilot/$TS.err"
  code=$?
  if command -v jq >/dev/null; then
    jq -r '"  kết quả: \(.subtype // "?") · lượt: \(.num_turns // "?") · chi phí phiên: \(.total_cost_usd // "?") USD"' \
      "logs/autopilot/$TS.json" 2>/dev/null || true
  fi
  if [ $code -ne 0 ]; then echo "claude thoát mã $code (xem logs/autopilot/$TS.err) → dừng"; break; fi
  sleep 5
done
scripts/vs digest
echo "Việc chờ bạn: state/HUMAN_TODO.md"
~~~~~

### `scripts/check_env.py`

<!-- FILE: scripts/check_env.py | sha256: 40770cbdb826a2deb5a673f3879ea8dbc8ab1688919a9a640b24ac118ac676da -->
~~~~~python
#!/usr/bin/env python3
"""Environment check. Prints what is present/missing WITHOUT printing any secret values.
Writes state/env_report.json. Exit 0 if everything needed for the CURRENT phase exists, else 1.
  python3 scripts/check_env.py [--need core|kaggle|api|r|ocr|all]
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NEEDS = {
    "core": ["python>=3.10", "venv", "pkg:yaml", "pkg:pydantic", "pkg:numpy", "pkg:scipy", "pkg:pandas",
             "pkg:pytest", "git"],
    "pdf": ["pkg:fitz", "pkg:pdfplumber", "bin:pdftotext"],
    "ocr": ["bin:tesseract", "tesseract:vie"],
    "kaggle": ["bin:kaggle", "kaggle_creds"],
    "api": ["env:OPENAI_API_KEY|GEMINI_API_KEY|GOOGLE_API_KEY", "pkg:openai|google.genai"],
    "r": ["bin:Rscript", "r:lme4", "r:glmmTMB", "r:sandwich", "r:boot"],
    "hf": ["env:HF_TOKEN"],
    "pubs": ["env:OSF_TOKEN", "env:ZENODO_TOKEN"],
}


def dotenv_keys() -> set[str]:
    f = ROOT / ".env"
    keys = set(k for k, v in os.environ.items() if v)
    if f.exists():
        for line in f.read_text(encoding="utf-8").splitlines():
            if "=" in line and not line.strip().startswith("#"):
                k, v = line.split("=", 1)
                if v.strip().strip('"').strip("'"):
                    keys.add(k.strip())
    return keys


def check(item: str, keys: set[str]) -> bool:
    kind, _, what = item.partition(":")
    py = ROOT / ".venv" / "bin" / "python"
    if item == "python>=3.10":
        return sys.version_info >= (3, 10)
    if item == "venv":
        return py.exists()
    if item == "git":
        return shutil.which("git") is not None
    if item == "kaggle_creds":
        return bool({"KAGGLE_API_TOKEN", "KAGGLE_KEY"} & keys) or (Path.home() / ".kaggle" / "kaggle.json").exists()
    if kind == "pkg":
        pyexe = str(py) if py.exists() else sys.executable
        for mod in what.split("|"):
            r = subprocess.run([pyexe, "-c", f"import importlib.util,sys; sys.exit(0 if importlib.util.find_spec('{mod}') else 1)"],
                               capture_output=True)
            if r.returncode == 0:
                return True
        return False
    if kind == "bin":
        return shutil.which(what) is not None or (ROOT / ".venv" / "bin" / what).exists()
    if kind == "env":
        return any(k in keys for k in what.split("|"))
    if kind == "tesseract":
        if not shutil.which("tesseract"):
            return False
        r = subprocess.run(["tesseract", "--list-langs"], capture_output=True, text=True)
        return what in r.stdout.split()
    if kind == "r":
        if not shutil.which("Rscript"):
            return False
        r = subprocess.run(["Rscript", "-e", f"quit(status=ifelse(requireNamespace('{what}', quietly=TRUE),0,1))"],
                           capture_output=True)
        return r.returncode == 0
    return False


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--need", default="core", help="core|pdf|ocr|kaggle|api|r|hf|pubs|all (comma list)")
    a = ap.parse_args()
    groups = list(NEEDS) if a.need == "all" else a.need.split(",")
    keys = dotenv_keys()
    report, ok = {}, True
    for g in groups:
        for item in NEEDS[g]:
            good = check(item, keys)
            report[f"{g}/{item}"] = good
            ok &= good
            print(f"{'OK ' if good else 'THIẾU'}  {g:7s} {item}")
    (ROOT / "state").mkdir(exist_ok=True)
    (ROOT / "state" / "env_report.json").write_text(json.dumps(report, indent=1), encoding="utf-8")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
~~~~~

### `scripts/package_plugin.sh`

<!-- FILE: scripts/package_plugin.sh | sha256: ddd675e088a0330d515220b936a90d90297b8c5dcc1bb275e8cc64096c008640 -->
~~~~~bash
#!/usr/bin/env bash
# (Tùy chọn) Đóng gói agent/skill/lệnh/hook của dự án thành một plugin Claude Code để dùng lại ở repo khác.
# Dự án này KHÔNG cần plugin: thư mục .claude/ đã đủ. Dùng: scripts/package_plugin.sh → dist/vnsoc-plugin
# Nạp thử: claude --plugin-dir dist/vnsoc-plugin
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT="$ROOT/dist/vnsoc-plugin"
rm -rf "$OUT" && mkdir -p "$OUT/.claude-plugin" "$OUT/hooks"
cp -r "$ROOT/.claude/agents" "$ROOT/.claude/skills" "$ROOT/.claude/commands" "$OUT/"
cp "$ROOT"/.claude/hooks/*.py "$OUT/hooks/"
cat > "$OUT/.claude-plugin/plugin.json" <<JSON
{
  "name": "vnsoc-audit",
  "description": "Agents, skills, commands and guard hooks for auditing LLM answers against Vietnamese MoH guidelines",
  "version": "0.1.0",
  "author": {"name": "Binh Minh"}
}
JSON
# Hook của plugin trỏ tới thư mục plugin; state vẫn nằm ở dự án đang mở ($CLAUDE_PROJECT_DIR).
python3 - "$ROOT/.claude/settings.json" "$OUT/hooks/hooks.json" <<'PY'
import json, sys
s = json.load(open(sys.argv[1]))
hooks = json.loads(json.dumps(s["hooks"]).replace("$CLAUDE_PROJECT_DIR/.claude/hooks", "${CLAUDE_PLUGIN_ROOT}/hooks"))
json.dump({"hooks": hooks}, open(sys.argv[2], "w"), indent=1)
PY
echo "OK: $OUT"
~~~~~

### `scripts/verify_citations.py`

<!-- FILE: scripts/verify_citations.py | sha256: eff58711bb8066240d1f133e78289f493a6d61d63e4966a186f60cc567d7cdfe -->
~~~~~python
#!/usr/bin/env python3
"""Verify every reference in manuscript/references.yaml against a registry (never trust memory).

Entry fields: key, title, authors (list), year, venue, and at least one of doi | arxiv | url.
- doi   -> https://api.crossref.org/works/<doi>  (DataCite fallback: https://api.datacite.org/dois/<doi>)
- arxiv -> https://export.arxiv.org/api/query?id_list=<id>
- url only (laws, MoH decisions, web pages) -> NOT auto-verifiable: needs `checked_by_human: true`
  (set only after the user confirms, human gate HG7.3).
Title match: normalised token similarity >= 0.85 and year within +-1.
Writes manuscript/citations_verified.json; exit 1 if any entry fails or is unverified.
"""
import json
import re
import sys
import time
import unicodedata
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UA = {"User-Agent": "vn-soc-audit-citation-check/0.1"}


def norm(s: str) -> list[str]:
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().lower()
    return re.findall(r"[a-z0-9]+", s)


def similarity(a: str, b: str) -> float:
    ta, tb = norm(a), norm(b)
    if not ta or not tb:
        return 0.0
    sa, sb = set(ta), set(tb)
    return 2 * len(sa & sb) / (len(sa) + len(sb))


def get(url: str) -> bytes | None:
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.read()
        except Exception:
            time.sleep(2 * (attempt + 1))
    return None


def lookup_doi(doi: str) -> tuple[str | None, int | None]:
    raw = get("https://api.crossref.org/works/" + urllib.parse.quote(doi))
    if raw:
        m = json.loads(raw)["message"]
        year = (m.get("issued", {}).get("date-parts") or [[None]])[0][0]
        return (m.get("title") or [None])[0], year
    raw = get("https://api.datacite.org/dois/" + urllib.parse.quote(doi))
    if raw:
        a = json.loads(raw)["data"]["attributes"]
        return (a.get("titles") or [{}])[0].get("title"), a.get("publicationYear")
    return None, None


def lookup_arxiv(aid: str) -> tuple[str | None, int | None]:
    raw = get("https://export.arxiv.org/api/query?id_list=" + urllib.parse.quote(aid))
    if not raw:
        return None, None
    ns = {"a": "http://www.w3.org/2005/Atom"}
    e = ET.fromstring(raw).find("a:entry", ns)
    if e is None or e.find("a:title", ns) is None:
        return None, None
    title = " ".join(e.find("a:title", ns).text.split())
    year = int(e.find("a:published", ns).text[:4])
    return title, year


def main() -> int:
    import yaml

    refs = yaml.safe_load((ROOT / "manuscript" / "references.yaml").read_text(encoding="utf-8")) or []
    out, bad = [], 0
    for r in refs:
        res = {"key": r.get("key"), "status": "unverified", "found_title": None, "similarity": None}
        found_title, found_year = None, None
        if r.get("doi"):
            found_title, found_year = lookup_doi(r["doi"])
        if not found_title and r.get("arxiv"):
            found_title, found_year = lookup_arxiv(r["arxiv"])
        if found_title:
            sim = similarity(r.get("title", ""), found_title)
            year_ok = not r.get("year") or not found_year or abs(int(r["year"]) - int(found_year)) <= 1
            res.update(found_title=found_title, similarity=round(sim, 3),
                       status="ok" if sim >= 0.85 and year_ok else "MISMATCH")
        elif r.get("url") and r.get("checked_by_human"):
            res["status"] = "ok_manual"
        elif r.get("url"):
            res["status"] = "needs_human_check"
        else:
            res["status"] = "NO_IDENTIFIER"
        bad += res["status"] not in ("ok", "ok_manual")
        out.append(res)
        print(f"{res['status']:18s} {r.get('key')}  {res.get('similarity') or ''}")
        time.sleep(0.5)
    (ROOT / "manuscript" / "citations_verified.json").write_text(json.dumps(out, indent=1, ensure_ascii=False),
                                                                 encoding="utf-8")
    print(f"{len(out) - bad}/{len(out)} trích dẫn đã kiểm chứng")
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
~~~~~

### `scripts/vs`

<!-- FILE: scripts/vs | sha256: fba096ec9de8bc11a342769ff10757931cf9b9a26f36a46f26232e54b9a0c27f -->
~~~~~bash
#!/usr/bin/env bash
# Wrapper for the task state machine: scripts/vs <init|next|start|done|block|unblock|skip|human-done|add|show|list|digest|todo|pause|resume|autopilot>
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PY="python3"; [ -x "$ROOT/.venv/bin/python" ] && PY="$ROOT/.venv/bin/python"
cd "$ROOT"
PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}" VNSOC_ROOT="$ROOT" exec "$PY" -m vnsoc.state "$@"
~~~~~

### `src/vnsoc/__init__.py`

<!-- FILE: src/vnsoc/__init__.py | sha256: 339e0ddd6a2add977ac823c916c4e8e8db970d3b8d3fa19e092a6ea9068f0def -->
~~~~~python
"""vn-soc-audit: Whose Standard of Care? LLM deviations from Vietnamese MoH guidelines."""
__version__ = "0.1.0"
~~~~~

### `src/vnsoc/budget.py`

<!-- FILE: src/vnsoc/budget.py | sha256: 1bef647bdd1eb3e2c6994c5d1626529d92337fba0046a87f2be98e1ce647d806 -->
~~~~~python
"""Hard API budget (USD). Every paid API job MUST call reserve() before submitting and settle()
after results arrive. The ledger is state/budget_ledger.csv. Stdlib only (hooks read it).

  python -m vnsoc.budget status
  python -m vnsoc.budget check 1.25            # exit 1 if 1.25 USD more would break the cap
  python -m vnsoc.budget reserve --provider google --model X --job J --task T5.5 --est 1.2
  python -m vnsoc.budget settle --job J --actual 0.93
"""
from __future__ import annotations

import argparse
import csv
import re
import sys

from vnsoc.paths import paths

HEADER = ["timestamp", "provider", "model", "job_id", "task", "kind", "est_usd", "actual_usd", "note"]


class BudgetExceeded(RuntimeError):
    pass


def config(root=None) -> dict:
    P = paths(root)
    f = P.configs / "budget.yaml"
    cfg = {"cap_usd": 40.0, "safety_margin_usd": 2.0}
    if not f.exists():
        return cfg
    text = f.read_text(encoding="utf-8")
    try:
        import yaml

        cfg.update(yaml.safe_load(text) or {})
    except ImportError:  # system python in hooks
        for k in ("cap_usd", "safety_margin_usd"):
            m = re.search(rf"^{k}:\s*([0-9.]+)", text, re.M)
            if m:
                cfg[k] = float(m.group(1))
    return cfg


def _rows(root=None) -> list[dict]:
    P = paths(root)
    if not P.ledger.exists():
        return []
    with P.ledger.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def spent(root=None) -> float:
    jobs: dict[str, dict] = {}
    for r in _rows(root):
        j = jobs.setdefault(r["job_id"], {"est": 0.0, "actual": None})
        if r.get("est_usd"):
            j["est"] = max(j["est"], float(r["est_usd"]))
        if r.get("actual_usd"):
            j["actual"] = float(r["actual_usd"])
    return round(sum(j["actual"] if j["actual"] is not None else j["est"] for j in jobs.values()), 4)


def remaining(root=None) -> float:
    c = config(root)
    return round(float(c["cap_usd"]) - float(c["safety_margin_usd"]) - spent(root), 4)


def can_spend(est: float, root=None) -> tuple[bool, str]:
    rem = remaining(root)
    ok = est <= rem
    return ok, f"cần {est:.2f} USD, còn được dùng {rem:.2f} USD (trần {config(root)['cap_usd']} trừ dự phòng)"


def _append(root, row: dict) -> None:
    P = paths(root)
    P.ledger.parent.mkdir(parents=True, exist_ok=True)
    new = not P.ledger.exists()
    with P.ledger.open("a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=HEADER)
        if new:
            w.writeheader()
        w.writerow({k: row.get(k, "") for k in HEADER})


def reserve(provider: str, model: str, job_id: str, task: str, est: float, note: str = "", root=None) -> None:
    ok, msg = can_spend(est, root)
    if not ok:
        raise BudgetExceeded("VƯỢT NGÂN SÁCH — không gửi job. " + msg)
    from vnsoc.state import now

    _append(root, dict(timestamp=now(), provider=provider, model=model, job_id=job_id, task=task,
                       kind="reserve", est_usd=f"{est:.4f}", note=note))


def settle(job_id: str, actual: float, note: str = "", root=None) -> None:
    from vnsoc.state import now

    _append(root, dict(timestamp=now(), job_id=job_id, kind="settle", actual_usd=f"{actual:.4f}", note=note))


def estimate(n_requests: int, in_tokens: float, out_tokens: float, price_in_per_m: float,
             price_out_per_m: float, batch_discount: float = 0.5) -> float:
    """Upper-bound cost: out_tokens should be max_tokens (+ reasoning allowance)."""
    usd = n_requests * (in_tokens * price_in_per_m + out_tokens * price_out_per_m) / 1e6
    return round(usd * (1 - batch_discount), 4)


def status_line(root=None) -> str:
    c = config(root)
    return (f"Ngân sách API: đã dùng/đặt trước {spent(root):.2f} / trần {float(c['cap_usd']):.0f} USD"
            f" (còn dùng được {remaining(root):.2f} sau dự phòng)")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="budget")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("status")
    s = sub.add_parser("check"); s.add_argument("est", type=float)
    s = sub.add_parser("reserve")
    for k in ("provider", "model", "job", "task"):
        s.add_argument(f"--{k}", required=True)
    s.add_argument("--est", type=float, required=True); s.add_argument("--note", default="")
    s = sub.add_parser("settle"); s.add_argument("--job", required=True)
    s.add_argument("--actual", type=float, required=True); s.add_argument("--note", default="")
    a = ap.parse_args(argv)
    if a.cmd == "status":
        print(status_line())
    elif a.cmd == "check":
        ok, msg = can_spend(a.est)
        print(("OK: " if ok else "KHÔNG ĐƯỢC: ") + msg)
        return 0 if ok else 1
    elif a.cmd == "reserve":
        try:
            reserve(a.provider, a.model, a.job, a.task, a.est, a.note)
        except BudgetExceeded as e:
            print(e, file=sys.stderr)
            return 1
        print(status_line())
    elif a.cmd == "settle":
        settle(a.job, a.actual, a.note)
        print(status_line())
    return 0


if __name__ == "__main__":
    sys.exit(main())
~~~~~

### `src/vnsoc/check.py`

<!-- FILE: src/vnsoc/check.py | sha256: c1def3263a4a4fe6151644f09fbd75765eb8fd7d584bc3690eb35f4f9c70e56e -->
~~~~~python
"""Small acceptance checks used by the `check:` commands in the plan (exit 0 = pass).

  $PY -m vnsoc.check jsonl atom data/interim/pilot_atoms.jsonl --min 20 --require span_verified=true
  $PY -m vnsoc.check numbers pilot. --min 5          # registry has >= 5 keys starting with 'pilot.'
  $PY -m vnsoc.check nofill manuscript/fmc/abstract_fmc.md configs/models.yaml
  $PY -m vnsoc.check maxsize manuscript/fmc/abstract_fmc.docx 1000000
  $PY -m vnsoc.check review M2      # PASS at round 1 or round 2 (review/M2_r2), or user decision gate HGM2 done
  $PY -m vnsoc.check count data/interim/atoms.jsonl --min 400 --where conflict_status=conflict
  $PY -m vnsoc.check families data/frozen/atoms_v1.jsonl --min 25
  $PY -m vnsoc.check value qc.extraction_cp_lower --ge 0.90
  $PY -m vnsoc.check runs data/runs/open --plan results/run_plan.json --conditions A0 A1 --models-from open
      run_plan.json = {"<model>|<condition>|<language>|<format>": expected_count, ...} written from the
      frozen question set BEFORE the run; the check compares valid, error-free RunRecords against it.
"""
from __future__ import annotations

import argparse
import gzip
import json
import re
import sys
from pathlib import Path

from vnsoc.paths import paths

FILL = re.compile(r"FILL_AT_|\[\s\]|\[n\]|\[k\]|\[a\]|\[b\]|\[c\]|\[d\]|\[e\]|\[f\]|TODO|TBD|XXX")


def _rows(path: str):
    op = gzip.open if path.endswith(".gz") else open
    with op(path, "rt", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                yield json.loads(line)


def _match(row: dict, conds: list[str]) -> bool:
    for c in conds:
        k, v = c.split("=", 1)
        val = row.get(k)
        want = {"true": True, "false": False, "null": None}.get(v, v)
        if isinstance(val, (int, float)) and not isinstance(val, bool) and not isinstance(want, bool):
            try:
                want = type(val)(want)
            except (TypeError, ValueError):
                pass
        if val != want:
            return False
    return True


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="check")
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("jsonl"); s.add_argument("kind"); s.add_argument("path")
    s.add_argument("--min", type=int, default=1); s.add_argument("--require", nargs="*", default=[])
    s = sub.add_parser("count"); s.add_argument("path"); s.add_argument("--min", type=int, default=1)
    s.add_argument("--where", nargs="*", default=[])
    s = sub.add_parser("families"); s.add_argument("path"); s.add_argument("--min", type=int, default=25)
    s = sub.add_parser("numbers"); s.add_argument("prefix"); s.add_argument("--min", type=int, default=1)
    s = sub.add_parser("nofill"); s.add_argument("files", nargs="+")
    s = sub.add_parser("maxsize"); s.add_argument("path"); s.add_argument("bytes", type=int)
    s = sub.add_parser("review"); s.add_argument("milestone")
    s = sub.add_parser("value"); s.add_argument("key"); s.add_argument("--ge", type=float); s.add_argument("--le", type=float)
    s = sub.add_parser("runs"); s.add_argument("dir"); s.add_argument("--plan", required=True)
    s.add_argument("--conditions", nargs="*", default=None); s.add_argument("--models", nargs="*", default=None)
    s.add_argument("--models-from", default=None, help="nhóm trong configs/models.yaml: open | api_cheap | api_frontier")
    s.add_argument("--min-frac", type=float, default=0.98); s.add_argument("--max-error", type=float, default=0.02)
    a = ap.parse_args(argv)

    if a.cmd == "jsonl":
        from vnsoc.schemas import validate_jsonl

        n, errs = validate_jsonl(a.kind, a.path)
        if errs:
            print(f"LỖI schema {len(errs)}/{n}: {errs[:5]}")
            return 1
        bad = [i for i, r in enumerate(_rows(a.path), 1) if not _match(r, a.require)]
        if bad:
            print(f"{len(bad)} dòng không thỏa {a.require} (ví dụ dòng {bad[:5]})")
            return 1
        if n < a.min:
            print(f"chỉ có {n} dòng (< {a.min})")
            return 1
        print(f"OK {n} dòng {a.kind}")
    elif a.cmd == "count":
        n = sum(1 for r in _rows(a.path) if _match(r, a.where))
        print(f"{n} dòng thỏa {a.where}")
        return 0 if n >= a.min else 1
    elif a.cmd == "families":
        fam = {r.get("conflict_family") for r in _rows(a.path) if r.get("conflict_status") == "conflict"}
        fam.discard(None)
        print(f"{len(fam)} nhóm xung đột")
        return 0 if len(fam) >= a.min else 1
    elif a.cmd == "numbers":
        P = paths()
        reg = json.loads(P.numbers.read_text(encoding="utf-8")) if P.numbers.exists() else {}
        keys = [k for k in reg if k.startswith(a.prefix)]
        missing_src = [k for k in keys if not (P.root / reg[k].get("source", "")).exists()]
        print(f"{len(keys)} khóa '{a.prefix}*'; thiếu nguồn: {missing_src}")
        return 0 if len(keys) >= a.min and not missing_src else 1
    elif a.cmd == "nofill":
        bad = []
        for f in a.files:
            for i, line in enumerate(Path(f).read_text(encoding="utf-8").splitlines(), 1):
                if FILL.search(line):
                    bad.append(f"{f}:{i}: {line.strip()[:100]}")
        print("\n".join(bad) or "OK không còn ô trống")
        return 1 if bad else 0
    elif a.cmd == "maxsize":
        size = Path(a.path).stat().st_size
        print(f"{a.path}: {size} bytes")
        return 0 if 0 < size <= a.bytes else 1
    elif a.cmd == "value":
        P = paths()
        reg = json.loads(P.numbers.read_text(encoding="utf-8")) if P.numbers.exists() else {}
        if a.key not in reg:
            print(f"thiếu khóa {a.key}")
            return 1
        v = float(reg[a.key]["value"])
        ok = (a.ge is None or v >= a.ge) and (a.le is None or v <= a.le)
        print(f"{a.key} = {v} ({'đạt' if ok else 'KHÔNG đạt'})")
        return 0 if ok else 1
    elif a.cmd == "runs":
        from pydantic import ValidationError

        from vnsoc.schemas import RunRecord

        plan = json.loads(Path(a.plan).read_text(encoding="utf-8"))
        if a.models_from:
            import yaml

            cfg = yaml.safe_load((paths().configs / "models.yaml").read_text(encoding="utf-8"))
            a.models = (a.models or []) + [m["key"] for m in cfg.get(a.models_from) or []]
        got: dict[str, int] = {}
        n = errors = invalid = 0
        for f in sorted(Path(a.dir).rglob("*.jsonl*")):
            for r in _rows(str(f)):
                n += 1
                try:
                    RunRecord.model_validate(r)
                except ValidationError:
                    invalid += 1
                    continue
                if r.get("error"):
                    errors += 1
                    continue
                k = f"{r['model']}|{r['condition']}|{r['language']}|{r['format']}"
                got[k] = got.get(k, 0) + 1
        short, selected = [], 0
        for k, exp in plan.items():
            model, cond = k.split("|")[0], k.split("|")[1]
            if (a.conditions and cond not in a.conditions) or (a.models and model not in a.models):
                continue
            selected += 1
            if got.get(k, 0) < a.min_frac * exp:
                short.append(f"{k}: {got.get(k, 0)}/{exp}")
        err_rate = errors / n if n else 1.0
        print(f"{n} bản ghi; không hợp lệ {invalid}; lỗi {errors} ({err_rate:.1%}); thiếu: {short[:10]}")
        if not selected:
            print("run_plan không có khóa nào khớp bộ lọc --models/--conditions")
            return 1
        return 0 if n and not invalid and not short and err_rate <= a.max_error else 1
    elif a.cmd == "review":
        from vnsoc.review import aggregate

        rdir = paths().root / "review"
        ok, msg = aggregate(a.milestone)
        print(msg)
        if not ok and (rdir / f"{a.milestone}_r2").exists():
            ok, msg = aggregate(f"{a.milestone}_r2")
            print("vòng 2:", msg)
        gate = "HG" + a.milestone.upper()                # HGM2, HGM3, HGM4: added dynamically, user-confirmed
        P = paths()
        if not ok and (P.human_ack / gate).exists() and P.progress.exists():
            st = json.loads(P.progress.read_text(encoding="utf-8"))
            if st["tasks"].get(gate, {}).get("status") == "done":
                print(f"không đạt sau 2 vòng; người dùng đã quyết định qua {gate}")
                ok = True
        return 0 if ok else 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
~~~~~

### `src/vnsoc/freeze.py`

<!-- FILE: src/vnsoc/freeze.py | sha256: 83383d20d3a766d12245b13ac44d13ded846a5974b914e6178e14d3f67f59e16 -->
~~~~~python
"""Freeze a dataset version into data/frozen/ (never overwrites; appends SHA256SUMS).

  $PY -m vnsoc.freeze corpus      # data/interim/manifest.jsonl (+ hashes of data/raw PDFs in the corpus)
  $PY -m vnsoc.freeze atoms       # data/interim/atoms.jsonl  (schema-validated)
  $PY -m vnsoc.freeze questions   # data/interim/questions.jsonl + configs/grading.yaml + configs/conditions.yaml
"""
from __future__ import annotations

import hashlib
import json
import shutil
import sys
from pathlib import Path

from vnsoc.paths import paths

SOURCES = {
    "corpus": [("data/interim/manifest.jsonl", "manifest", "manifest")],
    "atoms": [("data/interim/atoms.jsonl", "atoms", "atom")],
    "questions": [("data/interim/questions.jsonl", "questions", "question"),
                  ("configs/grading.yaml", "grading", None), ("configs/conditions.yaml", "conditions", None)],
}


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def next_version(frozen: Path, stem: str) -> int:
    vs = [int(p.stem.split("_v")[-1]) for p in frozen.glob(f"{stem}_v*.*") if p.stem.split("_v")[-1].isdigit()]
    return max(vs, default=0) + 1


def freeze(kind: str, root=None) -> list[Path]:
    P = paths(root)
    frozen = P.root / "data" / "frozen"
    frozen.mkdir(parents=True, exist_ok=True)
    out, lines = [], []
    for src_rel, stem, schema in SOURCES[kind]:
        src = P.root / src_rel
        if not src.exists() or src.stat().st_size == 0:
            raise SystemExit(f"Thiếu {src_rel}")
        if schema:
            from vnsoc.schemas import validate_jsonl

            n, errs = validate_jsonl(schema, str(src))
            if errs:
                raise SystemExit(f"{src_rel}: {len(errs)} dòng lỗi schema — không đóng băng.\n" + "\n".join(errs[:10]))
        v = next_version(frozen, stem)
        dst = frozen / f"{stem}_v{v}{src.suffix}"
        if dst.exists():
            raise SystemExit(f"{dst} đã tồn tại")
        shutil.copy2(src, dst)
        dst.chmod(0o444)
        out.append(dst)
        lines.append(f"{sha256(dst)}  {dst.name}")
    if kind == "corpus":
        rows = [json.loads(x) for x in (P.root / "data/interim/manifest.jsonl").read_text(encoding="utf-8").splitlines()
                if x.strip()]
        missing = [r["doc_key"] for r in rows if r.get("in_corpus") and not r.get("sha256")]
        if missing:
            raise SystemExit(f"Văn bản trong kho thiếu sha256: {missing}")
        lines += [f"{r['sha256']}  raw/{r['doc_key'].replace('/', '_')}.pdf" for r in rows if r.get("in_corpus")]
    with (frozen / "SHA256SUMS").open("a", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    from vnsoc.state import append_decision, append_log

    append_log(P, f"ĐÓNG BĂNG {kind}: " + ", ".join(p.name for p in out))
    append_decision(P, f"Đóng băng {kind}: " + ", ".join(f"{p.name} ({sha256(p)[:12]})" for p in out))
    return out


def main(argv=None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    if len(argv) != 1 or argv[0] not in SOURCES:
        print(__doc__)
        return 2
    for p in freeze(argv[0]):
        print("OK", p)
    return 0


if __name__ == "__main__":
    sys.exit(main())
~~~~~

### `src/vnsoc/grade.py`

<!-- FILE: src/vnsoc/grade.py | sha256: f9e7a9fb37f0d8393b746fec691f5db429d8ebc036d77368a523ea45ba9685fe -->
~~~~~python
"""Rule-based grading (pre-registered, section 4.5 of the proposal). One label per answer:

  1 correct_aware  MoH value AND explicitly flags the foreign difference (or asks which country)
  2 correct        answer contained in the current MoH value set
  3 temporal       matches a superseded MoH version
  4 foreign        matches a named foreign system (US, EU_UK, WHO_global, WHO_WPRO)
  5 unattributed   a value that matches no known source (decoy matches land here, flagged)
  6 abstain        no value given

Atoms are dicts (see schemas.Atom). Value items by kind:
  num      {"lo": 15, "hi": 15, "unit": "ml/kg/h", "cmp": null}
  bp       {"sys": 140, "dia": 90}
  schedule {"seq": [0, 3, 7, 14, 28], "unit": "day"}
  drugs    {"key_drugs": ["artemether-lumefantrine"]}
  cat      {"label": "one_step"}
"""
from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field

from vnsoc import normalize_vi as nv

LABELS = {1: "correct_aware", 2: "correct", 3: "temporal", 4: "foreign", 5: "unattributed", 6: "abstain"}
ANS_LINE = re.compile(r"(?:ĐÁP\s*ÁN|Đáp\s*án|DAP\s*AN|ANSWER|Final\s+answer)\s*\**\s*[:：]\s*\**\s*(.+)", re.I)
THINK = re.compile(r"<think>.*?</think>", re.S | re.I)
ABSTAIN = re.compile(r"không\s+(?:rõ|chắc|biết|thể\s+xác\s+định|có\s+(?:đủ\s+)?(?:thông\s+tin|dữ\s+liệu))|"
                     r"tôi\s+không\s+thể|không\s+đủ\s+thông\s+tin|i\s+(?:do\s+not|don't)\s+know|"
                     r"cannot\s+(?:determine|answer|provide)|unable\s+to|not\s+sure|insufficient\s+information", re.I)
ASK_COUNTRY = re.compile(r"quốc\s+gia\s+nào|nước\s+nào|hướng\s+dẫn\s+(?:của\s+)?(?:nước|quốc\s+gia)\s+nào|"
                         r"which\s+(?:country|guideline|jurisdiction)", re.I)
CONTRAST = re.compile(r"khác\s+(?:với)?|trong\s+khi|còn\s+theo|ngược\s+lại|whereas|while|differ|in\s+contrast|"
                      r"unlike|however", re.I)
FOREIGN_NAMES = re.compile(r"\b(?:WHO|ADA|AHA|ACC|ESC|ESH|CDC|AASLD|EASL|RCUK|NICE|ACOG|GINA|GOLD|WAO|EAACI|"
                           r"IDSA|Mỹ|Hoa\s+Kỳ|châu\s+Âu|quốc\s+tế|US|USA|American|European|international)\b", re.I)
VN_MARK = re.compile(r"bộ\s+y\s+tế|việt\s+nam|\bBYT\b|\bMoH\b|Vietnam", re.I)


@dataclass
class Grade:
    label: int | None
    label_name: str | None
    vn_match: bool = False
    foreign_systems: list = field(default_factory=list)
    superseded: list = field(default_factory=list)
    decoy_match: bool = False
    parse_method: str = "none"      # answer_line | fallback | llm | none
    multi: bool = False
    partial: bool = False
    unit_assumed: bool = False
    needs_llm: bool = False
    answer_text: str = ""
    parsed: list = field(default_factory=list)

    def as_dict(self) -> dict:
        return asdict(self)


# ------------------------------------------------------------------------------ extraction
def answer_span(output: str) -> tuple[str, str]:
    text = THINK.sub(" ", output or "").strip()
    hits = ANS_LINE.findall(text)
    if hits:
        return hits[-1].strip().strip("*").strip(), "answer_line"
    return text, "fallback"


def parse_values(text: str, atom: dict, lang: str, synonyms=None, combos=None) -> list:
    kind = atom["value_kind"]
    if kind == "num":
        unit, ctx = atom.get("unit"), atom.get("context") or {}
        vals = []
        for n in nv.parse_nums(text, lang):
            if n.unit is None:
                vals.append(("assumed", nv.Num(n.lo, n.hi, unit, n.cmp)))
            elif n.to(unit, ctx) is not None:
                vals.append(("ok", n.to(unit, ctx)))
        return vals
    if kind == "bp":
        return [("ok", b) for b in nv.parse_bps(text)]
    if kind == "schedule":
        return [("ok", s) for s in nv.parse_schedules(text, min_len=int(atom.get("min_schedule_len", 2)))]
    if kind == "drugs":
        d = nv.parse_drugs(text, synonyms or {}, combos or {})
        return [("ok", d)] if d.names else []
    if kind == "cat":
        c = nv.parse_cats(text, atom.get("cat_options") or {})
        return [("ok", c)] if c.labels else []
    raise ValueError(f"value_kind lạ: {kind}")


# ------------------------------------------------------------------------------ matching
def _within(x: float, lo: float, hi: float, tol: float) -> bool:
    return (lo <= x <= hi) or (lo - tol < x < hi + tol)


def matches(val, item: dict, atom: dict) -> tuple[bool, bool]:
    """(contained, partial_overlap) of one parsed answer value in one reference value item."""
    kind, tol = atom["value_kind"], float(atom.get("tolerance") or 0.0)
    if kind == "num":
        ref = nv.Num(float(item["lo"]), float(item["hi"]), item.get("unit") or atom.get("unit"))
        ref = ref.to(atom.get("unit"), atom.get("context") or {}) or ref
        inside = _within(val.lo, ref.lo, ref.hi, tol) and _within(val.hi, ref.lo, ref.hi, tol)
        overlap = not (val.hi < ref.lo - tol or val.lo > ref.hi + tol)
        return inside, (overlap and not inside)
    if kind == "bp":
        ok = _within(val.sys, item["sys"], item["sys"], tol) and _within(val.dia, item["dia"], item["dia"], tol)
        return ok, False
    if kind == "schedule":
        return tuple(val.seq) == tuple(item["seq"]) and val.unit == item.get("unit", "day"), False
    if kind == "drugs":
        key = set(item["key_drugs"])
        return key <= set(val.names), bool(key & set(val.names)) and not key <= set(val.names)
    if kind == "cat":
        return item["label"] in val.labels, False
    raise ValueError(kind)


def classify_value(val, atom: dict) -> dict:
    r = {"vn": False, "foreign": [], "superseded": [], "decoy": False, "partial": False}
    for it in atom.get("vn") or []:
        ok, part = matches(val, it, atom)
        r["vn"] |= ok
        r["partial"] |= part
    for f in atom.get("foreign") or []:
        if any(matches(val, it, atom)[0] for it in f["values"]):
            r["foreign"].append(f["system"])
    for s in atom.get("superseded") or []:
        if any(matches(val, it, atom)[0] for it in s["values"]):
            r["superseded"].append(s["guideline"])
    r["decoy"] = any(matches(val, it, atom)[0] for it in atom.get("decoy") or [])
    return r


def _distinct(vals: list) -> list:
    out = []
    for flag, v in vals:
        if all(v != w for _, w in out):
            out.append((flag, v))
    return out


def grade_short(output: str, atom: dict, lang: str = "vi", synonyms=None, combos=None,
                extracted: str | None = None, condition: str | None = None) -> Grade:
    """Grade a short-answer output. `extracted` = answer string from the LLM extractor (method llm).
    `condition`: asking back "which country?" counts as label 1 only without a country cue (A0); always pass it."""
    if extracted is not None:
        span, method = extracted, "llm"
    else:
        span, method = answer_span(output)
    vals = _distinct(parse_values(span, atom, lang, synonyms, combos))
    full_text = THINK.sub(" ", output or "")
    g = Grade(label=None, label_name=None, parse_method=method, answer_text=span[:300])
    if method == "fallback" and len(vals) > 1:
        g.needs_llm = True
        g.parsed = [repr(v) for _, v in vals]
        return g
    if not vals:
        if atom["value_kind"] == "num" and nv.parse_nums(span, lang) and method == "answer_line":
            g.parse_method = "unit_mismatch"  # a value was given but in an unconvertible unit
            g.label, g.label_name = 5, LABELS[5]
            return g
        g.parse_method = "none" if method == "fallback" else method
        g.label = 1 if (ASK_COUNTRY.search(full_text) and condition == "A0") else 6
        g.label_name = LABELS[g.label]
        return g
    g.parsed = [repr(v) for _, v in vals]
    g.unit_assumed = any(f == "assumed" for f, _ in vals)
    cls = [classify_value(v, atom) for _, v in vals]
    g.decoy_match = any(c["decoy"] for c in cls)
    g.partial = any(c["partial"] for c in cls) and not any(c["vn"] for c in cls)
    if len(cls) > 1 and not all(c["vn"] for c in cls):
        g.multi = True
        if any(c["vn"] for c in cls) and VN_MARK.search(span):
            g.vn_match = True
            g.foreign_systems = sorted({s for c in cls for s in c["foreign"]})
            g.label, g.label_name = 1, LABELS[1]
        else:
            g.label, g.label_name = 5, LABELS[5]
        return g
    c = cls[0] if len(cls) == 1 else {"vn": True, "foreign": [], "superseded": [], "decoy": False}
    g.vn_match = c["vn"]
    g.foreign_systems = sorted(set(c["foreign"]))
    g.superseded = sorted(set(c["superseded"]))
    if c["vn"] and c["foreign"] and atom["value_kind"] == "drugs":
        # one drug list containing both the MoH and a foreign regimen
        g.multi = True
        conflicting = [f["system"] for f in atom.get("foreign") or []
                       if all(_gap(v, it, atom) > 0 for v in atom["vn"] for it in f["values"])]
        if set(c["foreign"]) & set(conflicting):
            aware = bool(VN_MARK.search(full_text) or FOREIGN_NAMES.search(full_text))
            g.label = 1 if aware else 5
            g.label_name = LABELS[g.label]
            return g
    if c["vn"]:
        aware = False
        others = _distinct(parse_values(full_text, atom, lang, synonyms, combos))
        if any(classify_value(v, atom)["foreign"] and not classify_value(v, atom)["vn"] for _, v in others):
            aware = bool(CONTRAST.search(full_text) or FOREIGN_NAMES.search(full_text))
        elif CONTRAST.search(full_text) and FOREIGN_NAMES.search(full_text):
            aware = True
        g.label = 1 if aware else 2
    elif c["superseded"]:
        g.label = 3
    elif c["foreign"]:
        g.label = 4
    else:
        g.label = 5
    g.label_name = LABELS[g.label]
    return g


MCQ_LETTER = re.compile(r"(?:ĐÁP\s*ÁN|ANSWER)?\s*[:：]?\s*\(?\b([A-F])\b\)?", re.I)


def grade_mcq(output: str, option_roles: dict[str, str]) -> Grade:
    """option_roles: letter -> 'vn' | 'foreign:US' | 'superseded:3705/2019' | 'decoy'."""
    span, method = answer_span(output)
    m = MCQ_LETTER.search(span if method == "answer_line" else span[:40])
    g = Grade(label=None, label_name=None, parse_method=method, answer_text=span[:100])
    if not m or m.group(1).upper() not in option_roles:
        g.label, g.label_name = 6, LABELS[6]
        return g
    role = option_roles[m.group(1).upper()]
    g.parsed = [m.group(1).upper()]
    if role == "vn":
        g.label, g.vn_match = 2, True
    elif role.startswith("superseded:"):
        g.label, g.superseded = 3, [role.split(":", 1)[1]]
    elif role.startswith("foreign:"):
        g.label, g.foreign_systems = 4, role.split(":", 1)[1].split("+")
    else:
        g.label, g.decoy_match = 5, role == "decoy"
    g.label_name = LABELS[g.label]
    return g


# ------------------------------------------------------------------------------ atom helpers
def _gap(a: dict, b: dict, atom: dict) -> float:
    kind = atom["value_kind"]
    if kind == "num":
        ctx, unit = atom.get("context") or {}, atom.get("unit")
        x = nv.Num(float(a["lo"]), float(a["hi"]), a.get("unit") or unit).to(unit, ctx)
        y = nv.Num(float(b["lo"]), float(b["hi"]), b.get("unit") or unit).to(unit, ctx)
        if x is None or y is None:
            return float("inf")
        return max(0.0, max(x.lo, y.lo) - min(x.hi, y.hi))
    if kind == "bp":
        return max(abs(a["sys"] - b["sys"]), abs(a["dia"] - b["dia"]))
    if kind == "schedule":
        return 0.0 if list(a["seq"]) == list(b["seq"]) else float("inf")
    if kind == "drugs":
        return 0.0 if set(a["key_drugs"]) & set(b["key_drugs"]) else float("inf")
    if kind == "cat":
        return 0.0 if a["label"] == b["label"] else float("inf")
    raise ValueError(kind)


def others(atom: dict) -> list[dict]:
    items = [it for f in atom.get("foreign") or [] for it in f["values"]]
    items += [it for s in atom.get("superseded") or [] for it in s["values"]]
    items += list(atom.get("decoy") or [])
    return items


def compute_tolerance(atom: dict) -> float:
    """Half the minimum gap between the MoH value set and every other source value (foreign,
    superseded, decoy), so tolerance windows never overlap the MoH set. Exact match (0) for
    schedule/drugs/cat kinds and when a gap is 0 (such atoms are concordant/indistinguishable)."""
    gaps = [_gap(v, o, atom) for v in atom.get("vn") or [] for o in others(atom)]
    finite = [g for g in gaps if g not in (0.0, float("inf"))]
    if not finite or atom["value_kind"] not in ("num", "bp"):
        return 0.0
    return min(finite) / 2.0


def conflict_status(atom: dict) -> str:
    """conflict | concordant | no_counterpart | indistinguishable.
    conflict: at least one foreign value lies OUTSIDE the MoH value set (gap > 0 to every MoH item).
    indistinguishable: a conflicting foreign value cannot be told apart from a superseded or decoy
    value (tolerance windows overlap), or the decoy touches the MoH set."""
    vn = atom.get("vn") or []
    foreign = [it for f in atom.get("foreign") or [] for it in f["values"]]
    if not foreign:
        return "no_counterpart"
    conflicting = [o for o in foreign if all(_gap(v, o, atom) > 0 for v in vn)]
    if not conflicting:
        return "concordant"
    tol = float(atom.get("tolerance") if atom.get("tolerance") is not None else compute_tolerance(atom))
    sup = [it for s in atom.get("superseded") or [] for it in s["values"]]
    dec = list(atom.get("decoy") or [])
    for o in conflicting:
        for x in sup + dec:
            gap = _gap(o, x, atom)
            if gap == 0.0 or gap < 2 * tol:
                return "indistinguishable"
    for x in dec + sup:
        if any(_gap(v, x, atom) == 0 for v in vn):
            return "indistinguishable" if x in dec else "conflict"
    return "conflict"
~~~~~

### `src/vnsoc/ltt.py`

<!-- FILE: src/vnsoc/ltt.py | sha256: 53ba2d23021ad1c13f043881a94da806414711770eabb4437eefb880dadee38c -->
~~~~~python
"""Certified selective answering for the "Whose Standard of Care?" study.

Two tools, both from the Learn-then-Test family (Angelopoulos et al., arXiv 2110.01052):

1. certified_bounds(): PRIMARY RQ3 output. For each group g and pre-specified coverage level c_k
   (thresholds fixed from a SEPARATE split), a simultaneous Clopper-Pearson upper bound U_gk on the
   selective risk P(error | answered, group g). Never empty: "at coverage c_k, risk <= U_gk".
2. ltt_thresholds(): SECONDARY output. Largest-coverage threshold per group certified to have
   selective risk <= alpha (exact binomial p-values, fixed-sequence testing, Bonferroni over groups).

Validity: calibration and deployment items exchangeable within each group; groups, scores and
thresholds fixed without looking at calibration labels. Split by ATOM (all languages/formats of an
atom on one side). Violations must be judged against the POOL risk (calibration U test) or a
superpopulation, not against the test half alone (test-half noise inflates apparent violations).
"""
import numpy as np
from scipy.stats import beta, binom


def split_by_atom(atom_ids, frac_cal=0.5, seed=0):
    """Boolean mask 'calibration' with every row of one atom on the same side."""
    atom_ids = np.asarray(atom_ids)
    uniq = np.unique(atom_ids)
    rng = np.random.default_rng(seed)
    cal_atoms = set(rng.choice(uniq, size=int(round(frac_cal * len(uniq))), replace=False).tolist())
    return np.array([a in cal_atoms for a in atom_ids])


def thresholds_from_reference(score_ref, group_ref, coverages=(1.0, 0.75, 0.5, 0.25)):
    """Per-group score thresholds giving the requested coverage on a separate reference split."""
    return {g: {c: (-np.inf if c >= 1.0 else np.quantile(score_ref[group_ref == g], 1 - c))
                for c in coverages} for g in np.unique(group_ref)}


def certified_bounds(score, error, group, thr, delta=0.10):
    """Simultaneous (over groups x coverage levels) Clopper-Pearson upper bounds."""
    K = sum(len(v) for v in thr.values())
    conf = 1 - delta / K
    out = {}
    for g, levels in thr.items():
        for c, lam in levels.items():
            ans = (group == g) & (score >= lam)
            n, k = int(ans.sum()), int(error[ans].sum())
            out[(g, c)] = dict(n=n, k=k, emp=(k / n if n else np.nan),
                               U=(beta.ppf(conf, k + 1, n - k) if 0 < n and k < n else 1.0))
    return out


def make_grids(score_ref, group_ref, start_q=0.85, n_steps=60):
    """Per-group LTT grids from a separate split, strict -> lenient (start: answer top 15%)."""
    return {g: np.quantile(score_ref[group_ref == g], np.linspace(start_q, 0.0, n_steps))
            for g in np.unique(group_ref)}


def ltt_thresholds(score, error, group, grids, alpha=0.10, delta=0.10):
    level = delta / len(grids)
    out = {}
    for g, grid in grids.items():
        s, e = score[group == g], error[group == g]
        lam_hat = np.inf
        for lam in grid:
            ans = s >= lam
            n, k = int(ans.sum()), int(e[ans].sum())
            if n == 0 or binom.cdf(k, n, alpha) > level:
                break
            lam_hat = lam
        out[g] = lam_hat
    return out


def simulate(n, rng):
    """0 = agreement group; 1 = disagreement group (conflict signal fired). Illustrative only."""
    grp = rng.choice([0, 1], n, p=[0.75, 0.25])
    s = rng.random(n)
    base = np.array([0.06, 0.30])[grp]
    err = (rng.random(n) < np.clip(base * (1.7 - 1.5 * s), 0, 1)).astype(int)
    return s, err, grp


if __name__ == "__main__":
    rng = np.random.default_rng(0)
    alpha, delta, trials = 0.10, 0.10, 300
    s_ref, _, g_ref = simulate(3000, rng)
    thr = thresholds_from_reference(s_ref, g_ref)
    grids = make_grids(s_ref, g_ref)
    cover_fail, viol_pool, viol_marg, covs, bounds = 0, 0, 0, [], None
    for _ in range(trials):
        s, e, g = simulate(4000, rng)                    # finite pool of generated questions
        idx = rng.permutation(len(s)); cal, test = idx[:2000], idx[2000:]
        b = certified_bounds(s[cal], e[cal], g[cal], thr, delta)
        # simultaneous coverage of the bounds, judged against the POOL risk
        for (gg, c), r in b.items():
            lam = thr[gg][c]; m = (g == gg) & (s >= lam)
            if m.any() and e[m].mean() > r["U"]:
                cover_fail += 1; break
        t = ltt_thresholds(s[cal], e[cal], g[cal], grids, alpha, delta)
        bad = False
        for gg, lam in t.items():
            m = (g == gg) & (s >= lam)
            if m.any() and e[m].mean() > alpha: bad = True
        viol_pool += bad
        covs.append([((g[test] == gg) & (s[test] >= t[gg])).sum() / (g[test] == gg).sum() for gg in (0, 1)])
        tm = ltt_thresholds(s[cal], e[cal], np.zeros_like(g[cal]), make_grids(s_ref, np.zeros_like(g_ref)), alpha, delta)[0]
        m1 = (g == 1) & (s >= tm)
        viol_marg += bool(m1.any() and e[m1].mean() > alpha)
        bounds = b
    print(f"CP bounds: P(some bound fails vs pool risk) = {cover_fail/trials:.3f} (target <= {delta})")
    print(f"group LTT: P(some group exceeds alpha, pool risk) = {viol_pool/trials:.3f}")
    print(f"marginal LTT: P(disagreement group exceeds alpha) = {viol_marg/trials:.3f}")
    print("mean LTT coverage (agree, disagree):", np.round(np.mean(covs, 0), 3))
    print("example certified bounds (last run):")
    for (gg, c), r in sorted(bounds.items()):
        print(f"  group {gg}, coverage {c:.2f}: n={r['n']}, empirical={r['emp']:.3f}, U={r['U']:.3f}")
~~~~~

### `src/vnsoc/normalize_vi.py`

<!-- FILE: src/vnsoc/normalize_vi.py | sha256: 96ff86b55e63cc9e149849ed687e5f8b5e46fb75a771057c05c22a07f7983231 -->
~~~~~python
"""Vietnamese/English clinical value normalisation (numbers, ranges, comparators, units,
blood pressure, schedules, drugs, categories). Pure stdlib. Pre-registered: changes after the
question freeze must be logged in docs/DECISIONS.md and re-run on the whole run set.

Conventions
- Vietnamese: comma = decimal ("0,5"), dot + 3 digits = thousands ("5.000"). A dot with other
  than 3 digits, or a leading 0 ("0.500"), is read as a decimal (models often use English style).
  "2,000" (comma + "000") is read as thousands in both languages (a decimal would not be written so).
- English: dot = decimal, comma + 3 digits = thousands; "2.000" (dot + "000", non-zero integer part)
  is read as thousands.
- Values are intervals [lo, hi] in a unit; a point has lo == hi; comparators are kept in `cmp`
  but thresholds are compared by value only.
"""
from __future__ import annotations

import re
import unicodedata
from collections import deque
from dataclasses import dataclass, field

# ------------------------------------------------------------------------------------ cleaning
DASHES = "‐‑‒–—―−"
FRACTIONS = {"½": 0.5, "¼": 0.25, "¾": 0.75, "⅓": 1 / 3}


def clean(text: str) -> str:
    t = unicodedata.normalize("NFC", text or "")
    for d in DASHES:
        t = t.replace(d, "-")
    t = t.replace(" ", " ").replace(" ", " ").replace("μ", "µ")
    t = t.replace("≧", "≥").replace("≦", "≤").replace("=>", "≥").replace(">=", "≥").replace("<=", "≤")
    t = t.replace("³", "3").replace("²", "2").replace("*", "")
    return re.sub(r"[ \t]+", " ", t).strip()


def strip_accents(s: str) -> str:
    s = s.replace("đ", "d").replace("Đ", "D")
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


# ------------------------------------------------------------------------------------ numbers
NUM_RE = r"(?<![\w.,/^])(?:\d{1,3}(?:[.,]\d{3})+(?:[.,]\d+)?|\d+(?:[.,]\d+)?|[½¼¾⅓])"


def parse_number(tok: str, lang: str = "vi") -> float:
    tok = tok.strip()
    if tok in FRACTIONS:
        return FRACTIONS[tok]
    if "." in tok and "," in tok:
        dec = "." if tok.rfind(".") > tok.rfind(",") else ","
        th = "," if dec == "." else "."
        return float(tok.replace(th, "").replace(dec, "."))
    for sep in (".", ","):
        if sep in tok:
            parts = tok.split(sep)
            groups3 = all(len(p) == 3 for p in parts[1:]) and parts[0] not in ("0", "")
            if len(parts) > 2 and groups3:
                return float("".join(parts))  # 1.000.000
            head, tail = parts[0], parts[1]
            if lang == "vi":
                thousands = (sep == "." and groups3) or (sep == "," and tail == "000" and head != "0")
            else:
                thousands = (sep == "," and groups3) or (sep == "." and tail == "000" and head != "0")
            return float(head + tail) if thousands else float(head + "." + tail)
    return float(tok)


# ------------------------------------------------------------------------------------ units
UNIT_ALIASES = {
    "ml/kg/giờ": "ml/kg/h", "ml/kg/gio": "ml/kg/h", "ml/kg/h": "ml/kg/h", "ml/kg/hr": "ml/kg/h",
    "ml/kg/hour": "ml/kg/h", "ml/kg/tiếng": "ml/kg/h",
    "mg/kg/ngày": "mg/kg/day", "mg/kg/day": "mg/kg/day", "mg/kg/d": "mg/kg/day", "mg/kg/24h": "mg/kg/day",
    "mg/kg": "mg/kg", "µg/kg": "ug/kg", "mcg/kg": "ug/kg", "ug/kg": "ug/kg", "microgram/kg": "ug/kg",
    "g/kg": "g/kg",
    "mg/dl": "mg/dL", "mmol/l": "mmol/L", "mmhg": "mmHg", "mm hg": "mmHg",
    "iu/ml": "IU/mL", "ui/ml": "IU/mL", "u/l": "U/L", "iu/l": "U/L", "ui/l": "U/L", "kpa": "kPa",
    "kg/m2": "kg/m2", "/mm3": "/uL", "/µl": "/uL", "/ul": "/uL", "/microlit": "/uL",
    "x10^9/l": "10^9/L", "×10^9/l": "10^9/L", "x 10^9/l": "10^9/L", "× 10^9/l": "10^9/L",
    "x109/l": "10^9/L", "g/l tiểu cầu": "10^9/L",
    "mg": "mg", "µg": "ug", "mcg": "ug", "ug": "ug", "microgram": "ug", "micrograms": "ug", "g": "g", "gram": "g",
    "ml": "ml", "l": "l", "lít": "l", "lit": "l",
    "%": "%", "giờ": "h", "gio": "h", "h": "h", "hr": "h", "hrs": "h", "hour": "h", "hours": "h", "tiếng": "h",
    "phút": "min", "min": "min", "minutes": "min", "ngày": "day", "day": "day", "days": "day",
    "tuần": "week", "week": "week", "weeks": "week", "tháng": "month", "month": "month", "months": "month",
    "tháng tuổi": "month", "months old": "month", "năm": "year", "year": "year", "years": "year",
    "tuổi": "year", "years old": "year", "viên": "tablet", "tablet": "tablet", "tablets": "tablet",
    "ống": "ampoule", "ampoule": "ampoule", "ampoules": "ampoule", "vial": "ampoule", "lọ": "ampoule",
}
_UNIT_KEYS = sorted(UNIT_ALIASES, key=len, reverse=True)
UNIT_RE = "(?:" + "|".join(re.escape(u) for u in _UNIT_KEYS) + r")(?![^\W\d_])"

# (from, to): factor  value_to = value_from * factor
STATIC_EDGES = {
    ("ug", "mg"): 1e-3, ("g", "mg"): 1e3, ("l", "ml"): 1e3, ("ug/kg", "mg/kg"): 1e-3, ("g/kg", "mg/kg"): 1e3,
    ("/uL", "10^9/L"): 1e-3, ("min", "h"): 1 / 60, ("week", "day"): 7.0, ("month", "year"): 1 / 12,
}
ANALYTE_MGDL_PER_MMOL = {"glucose": 18.016, "ldl": 38.67, "cholesterol": 38.67, "hdl": 38.67, "triglyceride": 88.57}


def canon_unit(u: str | None) -> str | None:
    if not u:
        return None
    return UNIT_ALIASES.get(clean(u).lower(), clean(u))


def _edges(ctx: dict) -> dict:
    e = dict(STATIC_EDGES)
    a = (ctx or {}).get("analyte")
    if a in ANALYTE_MGDL_PER_MMOL:
        e[("mmol/L", "mg/dL")] = ANALYTE_MGDL_PER_MMOL[a]
    if (ctx or {}).get("weight_kg"):
        w = float(ctx["weight_kg"])
        e[("mg/kg", "mg")] = w
        e[("ug/kg", "ug")] = w
    if (ctx or {}).get("mg_per_ml"):
        e[("ml", "mg")] = float(ctx["mg_per_ml"])
    if (ctx or {}).get("mg_per_tablet"):
        e[("tablet", "mg")] = float(ctx["mg_per_tablet"])
    if (ctx or {}).get("mg_per_ampoule"):
        e[("ampoule", "mg")] = float(ctx["mg_per_ampoule"])
    both = {}
    for (a_, b_), f in e.items():
        both[(a_, b_)] = f
        both.setdefault((b_, a_), 1 / f)
    return both


def convert(value: float, frm: str | None, to: str | None, ctx: dict | None = None) -> float | None:
    """Convert value between canonical units; None if impossible. Missing unit -> assume `to`."""
    if frm is None or to is None or frm == to:
        return value
    edges = _edges(ctx or {})
    graph: dict[str, list[tuple[str, float]]] = {}
    for (a, b), f in edges.items():
        graph.setdefault(a, []).append((b, f))
    q, seen = deque([(frm, 1.0)]), {frm}
    while q:
        u, f = q.popleft()
        if u == to:
            return value * f
        for v, g in graph.get(u, []):
            if v not in seen:
                seen.add(v)
                q.append((v, f * g))
    return None


# ------------------------------------------------------------------------------------ values
@dataclass(frozen=True)
class Num:
    lo: float
    hi: float
    unit: str | None = None
    cmp: str | None = None  # >=, >, <=, <, None

    def to(self, unit: str | None, ctx: dict | None = None) -> "Num | None":
        lo, hi = convert(self.lo, self.unit, unit, ctx), convert(self.hi, self.unit, unit, ctx)
        if lo is None or hi is None:
            return None
        return Num(min(lo, hi), max(lo, hi), unit or self.unit, self.cmp)


@dataclass(frozen=True)
class BP:
    sys: float
    dia: float
    cmp: str | None = None


@dataclass(frozen=True)
class Schedule:
    seq: tuple
    unit: str | None = "day"


@dataclass(frozen=True)
class Drugs:
    names: frozenset = field(default_factory=frozenset)


@dataclass(frozen=True)
class Cat:
    labels: frozenset = field(default_factory=frozenset)


CMP_WORDS = [
    (r"≥|không dưới|ít nhất|tối thiểu|từ|at least|no less than|≥", ">="),
    (r"≤|không quá|tối đa|at most|up to|no more than|maximum|max", "<="),
    (r">|trên|lớn hơn|cao hơn|vượt quá|above|over|greater than|more than|exceeding|higher than", ">"),
    (r"<|dưới|nhỏ hơn|thấp hơn|below|under|less than|lower than", "<"),
]
CMP_RE = "(?:" + "|".join(p for p, _ in CMP_WORDS) + ")"


def _cmp_of(word: str | None) -> str | None:
    if not word:
        return None
    w = word.strip().lower()
    for pat, c in CMP_WORDS:
        if re.fullmatch(pat, w):
            return c
    return None


RANGE_RE = re.compile(
    rf"(?:từ\s+|from\s+|between\s+)?(?P<a>{NUM_RE})\s*(?P<ua>{UNIT_RE})?\s*(?:-|đến|tới|to)\s*"
    rf"(?P<b>{NUM_RE})\s*(?P<ub>{UNIT_RE})?", re.I)
SINGLE_RE = re.compile(rf"(?:(?P<cmp>{CMP_RE})\s*)?(?P<a>{NUM_RE})\s*(?P<u>{UNIT_RE})?", re.I)
FRACTION_RE = re.compile(r"(?P<n>\d+)\s*/\s*(?P<d>\d+)\s*(?P<u>ống|ampoules?|viên|tablets?)", re.I)


CITATION_RE = re.compile(
    r"(?:\b(?:qđ|quyết định|quyet dinh|thông tư|tt|decision|circular|nđ|nghị định)\s*(?:số\s*)?\d+(?:/[\wđĐ\-]+)*)"
    r"|(?:\b\d{2,5}/(?:qđ|tt|nđ)[\w\-/đĐ]*)"
    r"|(?:\b\d{3,5}/(?:19|20)\d{2}\b)",
    re.I)

def strip_citations(text: str) -> str:
    """Remove decision numbers ('QĐ 2760/QĐ-BYT', '1740/2026') and bare years ('ADA 2025')."""
    t = CITATION_RE.sub(" ", clean(text))
    return re.sub(rf"(?<![\d.,])(?:19|20)\d{{2}}(?![\d.,])(?!\s*{UNIT_RE})", " ", t, flags=re.I)


def parse_nums(text: str, lang: str = "vi") -> list[Num]:
    """All numeric values (ranges first, then singles) in reading order."""
    t = strip_citations(text)
    found: list[tuple[int, Num]] = []
    taken: list[tuple[int, int]] = []

    def free(s, e):
        return all(e <= a or s >= b for a, b in taken)

    for m in FRACTION_RE.finditer(t):
        v = int(m.group("n")) / int(m.group("d"))
        found.append((m.start(), Num(v, v, canon_unit(m.group("u")))))
        taken.append(m.span())
    for m in RANGE_RE.finditer(t):
        if not free(*m.span()):
            continue
        a, b = parse_number(m.group("a"), lang), parse_number(m.group("b"), lang)
        if b < a:  # "10-5" is not a range
            continue
        u = canon_unit(m.group("ub") or m.group("ua"))
        found.append((m.start(), Num(a, b, u)))
        taken.append(m.span())
    for m in SINGLE_RE.finditer(t):
        if not free(*m.span("a")):
            continue
        v = parse_number(m.group("a"), lang)
        found.append((m.start(), Num(v, v, canon_unit(m.group("u")), _cmp_of(m.group("cmp")))))
        taken.append(m.span())
    return [n for _, n in sorted(found, key=lambda x: x[0])]


BP_RE = re.compile(rf"(?:(?P<cmp>{CMP_RE})\s*)?(?P<s>\d{{2,3}})\s*/\s*(?P<d>\d{{2,3}})(?!\s*(?:u/l|iu|ui))", re.I)


def parse_bps(text: str) -> list[BP]:
    out = []
    for m in BP_RE.finditer(strip_citations(text)):
        s, d = float(m.group("s")), float(m.group("d"))
        if 60 <= s <= 260 and 30 <= d <= 160 and s > d:
            out.append(BP(s, d, _cmp_of(m.group("cmp"))))
    return out


SCHED_SEP = r"\s*(?:-|,|;|/|và|and|&|\+)\s*"


def parse_schedules(text: str, min_len: int = 3) -> list[Schedule]:
    t = strip_citations(text).lower()
    t = re.sub(r"\b(?:n|d|ngày|day|days)\s*(?=\d)", "", t)
    unit = "month" if re.search(r"tháng|month", t) else "day"
    out = []
    for m in re.finditer(rf"\d{{1,3}}(?:{SCHED_SEP}\d{{1,3}})+", t):
        seq = tuple(int(x) for x in re.findall(r"\d{1,3}", m.group(0)))
        if len(seq) >= min_len and list(seq) == sorted(seq) and len(set(seq)) == len(seq):
            out.append(Schedule(seq, unit))
    return out


def _norm_drug_text(s: str) -> str:
    s = strip_accents(clean(s).lower())
    return re.sub(r"\s*(?:-|/|\+)\s*", "-", s)


def parse_drugs(text: str, synonyms: dict[str, list[str]], combos: dict[str, list[str]] | None = None) -> Drugs:
    """synonyms: canonical INN -> aliases; combos: combination -> component INNs."""
    t = " " + _norm_drug_text(text) + " "
    pairs = sorted(((_norm_drug_text(a), c) for c, al in synonyms.items() for a in [c, *al]),
                   key=lambda x: len(x[0]), reverse=True)
    found = set()
    for alias, canon in pairs:
        pat = rf"(?<![a-z0-9]){re.escape(alias)}(?![a-z0-9])"
        if re.search(pat, t):
            found.add(canon)
            t = re.sub(pat, " ", t)
    for combo, parts in (combos or {}).items():
        if all(p in found for p in parts):
            found -= set(parts)
            found.add(combo)
    return Drugs(frozenset(found))


def parse_cats(text: str, options: dict[str, list[str]]) -> Cat:
    t = strip_accents(clean(text).lower())
    hit = {lab for lab, pats in options.items() if any(re.search(strip_accents(p.lower()), t) for p in pats)}
    return Cat(frozenset(hit))
~~~~~

### `src/vnsoc/numbers.py`

<!-- FILE: src/vnsoc/numbers.py | sha256: d29c82519ae9c84b71264eeb8fe7630711d9ef6aa886b84869cc6ea3cf4b6fbf -->
~~~~~python
"""Number registry: every result number in the manuscript/abstract/slides comes from
results/numbers.json, written ONLY by analysis code via put(). Manuscript sources use
placeholders:  {{h1.delta_pooled}}  -> rendered value;  {{=0,10}} -> a design constant written
literally (not a result) — every number inside {{=…}} must also appear in configs/*.yaml.
Bare digits in prose are flagged by `verify`. Registry sources must live in src/vnsoc/analysis/,
analysis_R/ or scripts/analysis/. Files: manuscript/**/*.md (except manuscript/build/).

  $PY -m vnsoc.numbers verify            # placeholders resolve, sources exist, no bare numbers
  $PY -m vnsoc.numbers render            # manuscript/*.md -> manuscript/build/*.md
  $PY -m vnsoc.numbers list
"""
from __future__ import annotations

import inspect
import json
import os
import re
import sys
from pathlib import Path

from vnsoc.paths import paths

PH = re.compile(r"\{\{\s*([A-Za-z0-9_.\-=:/%,–]+)\s*\}\}")
ALLOW = [
    r"\b(?:19|20)\d{2}[a-z]?\b",                   # years
    r"\b(?:H[1-5]|RQ[1-4]|A[0-6]|DR\d{1,2}|S\d{1,2}|T\d|M[1-4])\b",  # design labels
    r"\b(?:Figure|Fig\.|Table|Hình|Bảng|Supplement|Phụ lục)\s+S?\d+[a-z]?",
    r"\[\d+(?:[,–-]\s*\d+)*\]",                # numeric citations [3], [4-6]
    r"\b10\.\d{4,9}/\S+",                           # DOIs
    r"\barXiv:?\s*\d{4}\.\d{4,5}",
    r"\b(?:Qwen3|Llama-3\.1|Sailor2|Vistral|MedGemma|Gemma-3|bge-m3|GPT-\S+|Gemini\s*\S+)[\w.\-]*",
    r"\b\d+[Bb]\b",                                 # model sizes 8B
    r"\bT4\b", r"\bICD-10\b", r"\bTRIPOD-LLM\b", r"\bCRediT\b",
    r"\b\d{1,5}/(?:QĐ|TT)-BYT\b", r"\b(?:QĐ|Decision|Circular)\s+\d{1,5}/\d{4}\b", r"\b\d{1,5}/\d{4}\b",
    r"§\s*\d+(?:\.\d+)*", r"^\s*#{1,6}\s+\d+(?:\.\d+)*", r"^\s*\d+\.\s",       # headings, list markers
]


ALLOWED_SOURCES = ("src/vnsoc/analysis/", "analysis_R/", "scripts/analysis/")


def _targets(P) -> list[Path]:
    return sorted(f for f in P.manuscript.rglob("*.md") if "build" not in f.relative_to(P.manuscript).parts)


def _num(tok: str) -> float:
    return float(tok.replace(",", "."))


def config_numbers(P) -> set[float]:
    vals = set()
    for f in P.configs.glob("*.yaml"):
        vals |= {_num(x) for x in re.findall(r"(?<![\w.])\d+(?:[.,]\d+)?", f.read_text(encoding="utf-8"))}
    return vals


def _load(P) -> dict:
    return json.loads(P.numbers.read_text(encoding="utf-8")) if P.numbers.exists() else {}


def put(key: str, value, display: str, note: str = "", root=None) -> None:
    """Called from analysis scripts only. Records the calling file as the source."""
    P = paths(root)
    caller = Path(inspect.stack()[1].filename).resolve()
    try:
        src = caller.relative_to(P.root).as_posix()
    except ValueError:
        src = str(caller)
    if not src.startswith(ALLOWED_SOURCES):
        raise ValueError(f"numbers.put chỉ được gọi từ mã phân tích {ALLOWED_SOURCES}, không từ {src}")
    reg = _load(P)
    from vnsoc.state import now

    reg[key] = {"value": value, "display": display, "source": src, "note": note, "generated": now()}
    P.numbers.parent.mkdir(parents=True, exist_ok=True)
    tmp = P.numbers.with_suffix(".tmp")
    tmp.write_text(json.dumps(reg, ensure_ascii=False, indent=1, sort_keys=True), encoding="utf-8")
    os.replace(tmp, P.numbers)


def _prose_lines(text: str):
    fence = False
    for i, line in enumerate(text.splitlines(), 1):
        if line.strip().startswith(("```", "~~~")):
            fence = not fence
            continue
        if fence or line.strip().startswith(("<!--", "|---", "| ---")):
            continue
        yield i, line


def bare_numbers(line: str) -> list[str]:
    s = PH.sub(" ", line)
    s = re.sub(r"\]\([^)]*\)", "]", s)             # link targets
    s = re.sub(r"https?://\S+", " ", s)
    for pat in ALLOW:
        s = re.sub(pat, " ", s, flags=re.M)
    return re.findall(r"(?<![\w.])\d+(?:[.,]\d+)?%?", s)


def verify(root=None, files: list[str] | None = None) -> int:
    P = paths(root)
    reg = _load(P)
    problems = []
    for k, v in reg.items():
        if not (P.root / v.get("source", "")).exists():
            problems.append(f"registry '{k}': source không tồn tại {v.get('source')}")
    targets = [Path(f) for f in files] if files else _targets(P)
    cfg_nums = config_numbers(P)
    for f in targets:
        text = f.read_text(encoding="utf-8")
        for key in PH.findall(text):
            if key.startswith("="):
                bad = [x for x in re.findall(r"\d+(?:[.,]\d+)?", key) if _num(x) not in cfg_nums]
                if bad:
                    problems.append(f"{f.name}: hằng số {{{{{key}}}}} có số {bad} không có trong configs/*.yaml")
            elif key not in reg:
                problems.append(f"{f.name}: placeholder chưa có số: {{{{{key}}}}}")
        for i, line in _prose_lines(text):
            nums = bare_numbers(line)
            if nums:
                problems.append(f"{f.name}:{i}: số viết tay {nums[:5]} — dùng {{{{key}}}} hoặc {{{{=hằng}}}}")
    for p in problems:
        print(p)
    print(f"{'OK' if not problems else 'LỖI'}: {len(problems)} vấn đề; {len(reg)} số trong registry")
    return 0 if not problems else 1


def render(root=None) -> int:
    P = paths(root)
    reg = _load(P)
    out = P.manuscript / "build"
    out.mkdir(parents=True, exist_ok=True)
    missing = set()

    def sub(m):
        k = m.group(1)
        if k.startswith("="):
            return k[1:]
        if k not in reg:
            missing.add(k)
            return m.group(0)
        return str(reg[k]["display"])

    for f in _targets(P):
        dst = out / f.relative_to(P.manuscript)
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(PH.sub(sub, f.read_text(encoding="utf-8")), encoding="utf-8")
    if missing:
        print("THIẾU:", sorted(missing))
        return 1
    print(f"OK: render {out}")
    return 0


def main(argv=None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    cmd = argv[0] if argv else "verify"
    if cmd == "verify":
        return verify(files=argv[1:] or None)
    if cmd == "render":
        return render()
    if cmd == "list":
        for k, v in sorted(_load(paths()).items()):
            print(f"{k:40s} {v['display']:>14s}  ← {v['source']}")
        return 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main())
~~~~~

### `src/vnsoc/paths.py`

<!-- FILE: src/vnsoc/paths.py | sha256: ed001125311cae00464565d06fb9039620af3648036bb5035078b82eda86aede -->
~~~~~python
"""Project paths. Stdlib only: hooks import this with the system python3."""
from __future__ import annotations

import os
from pathlib import Path
from types import SimpleNamespace


def project_root() -> Path:
    env = os.environ.get("VNSOC_ROOT") or os.environ.get("CLAUDE_PROJECT_DIR")
    if env:
        return Path(env).resolve()
    here = Path(__file__).resolve()
    for p in [here, *here.parents]:
        if (p / "pyproject.toml").exists() and (p / "src" / "vnsoc").exists():
            return p
    return Path.cwd().resolve()


def paths(root: Path | str | None = None) -> SimpleNamespace:
    r = Path(root).resolve() if root else project_root()
    s = r / "state"
    return SimpleNamespace(
        root=r,
        docs=r / "docs",
        plan=r / "docs" / "02_KE_HOACH_TRIEN_KHAI.md",
        state=s,
        progress=s / "progress.json",
        human_todo=s / "HUMAN_TODO.md",
        human_ack=s / ".human_ack",
        ledger=s / "budget_ledger.csv",
        pause=s / "PAUSE",
        autopilot=s / "AUTOPILOT_ON",
        log=r / "docs" / "LOG.md",
        decisions=r / "docs" / "DECISIONS.md",
        configs=r / "configs",
        results=r / "results",
        numbers=r / "results" / "numbers.json",
        manuscript=r / "manuscript",
    )


def python_bin(root: Path | str | None = None) -> str:
    venv = paths(root).root / ".venv" / "bin" / "python"
    return str(venv) if venv.exists() else "python3"
~~~~~

### `src/vnsoc/review.py`

<!-- FILE: src/vnsoc/review.py | sha256: 9380fb7393588a32f8817c2fc6e3c70b3741e97e616e1e3ee159da24ea7e4e90 -->
~~~~~python
"""Aggregate the agent review panel for a milestone.

  $PY -m vnsoc.review M2            # reads review/M2/rev-*.md -> review/M2/summary.md (+ exit 0 PASS / 1 REVISE)

Each reviewer file starts with a ```yaml block (see .claude/agents/rev-*.md). Decision rule
(fixed in advance): PASS iff no fatal flaws, no 'reject', and mean weighted score >= 7.0.
Round 2 of a milestone that still fails -> escalate to the user (a human decides).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

from vnsoc.paths import paths

WEIGHTS = {"importance": .20, "novelty": .20, "rigor": .15, "feasibility": .15, "q1_likelihood": .15, "fit": .15}
PANEL = ["rev-editor", "rev-clinician", "rev-methods", "rev-feasibility", "rev-novelty"]
PASS_SCORE = 7.0
YAML_BLOCK = re.compile(r"```ya?ml\s*\n(.*?)```", re.S)


def parse(path: Path) -> dict:
    import yaml

    m = YAML_BLOCK.search(path.read_text(encoding="utf-8"))
    if not m:
        raise ValueError(f"{path.name}: thiếu khối ```yaml ở đầu")
    d = yaml.safe_load(m.group(1))
    missing = [k for k in WEIGHTS if k not in (d.get("scores") or {})]
    if missing:
        raise ValueError(f"{path.name}: thiếu điểm {missing}")
    d["weighted"] = round(sum(float(d["scores"][k]) * w for k, w in WEIGHTS.items()), 2)
    return d


def aggregate(milestone: str, root=None) -> tuple[bool, str]:
    P = paths(root)
    d = P.root / "review" / milestone
    reviews, problems = {}, []
    for name in PANEL:
        f = d / f"{name}.md"
        if not f.exists():
            problems.append(f"thiếu báo cáo {name}")
            continue
        try:
            reviews[name] = parse(f)
        except Exception as e:  # noqa: BLE001
            problems.append(str(e))
    if problems:
        return False, "CHƯA ĐỦ BÁO CÁO: " + "; ".join(problems)
    mean = round(sum(r["weighted"] for r in reviews.values()) / len(reviews), 2)
    fatal = [(n, f) for n, r in reviews.items() for f in (r.get("fatal_flaws") or [])]
    rejects = [n for n, r in reviews.items() if r.get("recommendation") == "reject"]
    ok = not fatal and not rejects and mean >= PASS_SCORE
    lines = [f"# Hội đồng phản biện {milestone}", "", f"Kết luận: **{'ĐẠT' if ok else 'CẦN SỬA'}** "
             f"(điểm trung bình có trọng số {mean}; ngưỡng {PASS_SCORE}; lỗi chết người {len(fatal)}; bác bỏ {len(rejects)})",
             "", "| Thành viên | Khuyến nghị | Điểm | " + " | ".join(WEIGHTS) + " |",
             "|" + "---|" * (3 + len(WEIGHTS))]
    for n, r in reviews.items():
        lines.append(f"| {n} | {r.get('recommendation')} | {r['weighted']} | "
                     + " | ".join(str(r['scores'][k]) for k in WEIGHTS) + " |")
    lines += ["", "## Lỗi chết người"] + ([f"- {n}: {f}" for n, f in fatal] or ["- (không có)"])
    lines += ["", "## Yêu cầu sửa (major trước)"]
    for sev in ("major", "minor"):
        for n, r in reviews.items():
            for c in r.get("required_changes") or []:
                if c.get("severity") == sev:
                    lines.append(f"- [{sev}] {n}#{c.get('id')} · {c.get('where')}: {c.get('what')} "
                                 f"→ kiểm: {c.get('acceptance')}")
    (d / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return ok, "\n".join(lines[:3])


def main(argv=None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    if not argv:
        print(__doc__)
        return 2
    ok, msg = aggregate(argv[0])
    print(msg)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
~~~~~

### `src/vnsoc/run/__init__.py`

<!-- FILE: src/vnsoc/run/__init__.py | sha256: 01ba4719c80b6fe911b091a7c05124b64eeece964e09c058ef8f9805daca546b -->
~~~~~python

~~~~~

### `src/vnsoc/run/api_batch.py`

<!-- FILE: src/vnsoc/run/api_batch.py | sha256: e1f5bce2ac819a5d9c9c0e34773d3880d57512edce41ff3ecd84f16aa4ce9fd9 -->
~~~~~python
"""Paid-API batch runs (OpenAI Batch, Gemini Batch) with a HARD budget gate.

Every submission: build JSONL -> estimate upper-bound cost -> budget.reserve() (raises if the cap
would be broken) -> submit -> poll -> fetch -> parse to RunRecord JSONL -> budget.settle(actual).

The request-building and parsing functions are pure and unit-tested. The submit/poll/fetch functions
call the vendor SDKs; T0.5 (API smoke test) must confirm the exact model IDs and parameter names
(reasoning/thinking controls change between model generations) and record them in configs/models.yaml.

Build request lines with openai_line()/gemini_line() from the frozen questions and the prompt
templates in configs/prompts.yaml (task T5.5 writes that small builder), then:
  $PY -m vnsoc.run.api_batch submit --model-key cheap_1 --batch runs/x.jsonl --task T5.5
  $PY -m vnsoc.run.api_batch poll   --job <id>
  $PY -m vnsoc.run.api_batch fetch  --job <id> --out data/runs/api/<id>.jsonl
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

from vnsoc import budget
from vnsoc.paths import paths


def _cfg(model_key: str) -> dict:
    import yaml

    models = yaml.safe_load((paths().configs / "models.yaml").read_text(encoding="utf-8"))
    for group in ("api_cheap", "api_frontier"):
        for m in models.get(group, []):
            if m["key"] == model_key:
                if not m.get("model") or "FILL" in str(m.get("model")):
                    raise SystemExit(f"{model_key}: chưa điền model id (làm T0.5 trước)")
                return m
    raise SystemExit(f"không có model key {model_key} trong configs/models.yaml")


def prompt_hash(messages: list[dict]) -> str:
    return hashlib.sha256(json.dumps(messages, ensure_ascii=False, sort_keys=True).encode()).hexdigest()[:16]


def openai_line(custom_id: str, model: str, messages: list[dict], max_tokens: int, extra: dict | None = None,
                endpoint: str = "/v1/chat/completions") -> dict:
    body = {"model": model, "messages": messages, "max_completion_tokens": max_tokens}
    body.update(extra or {})
    return {"custom_id": custom_id, "method": "POST", "url": endpoint, "body": body}


def gemini_line(key: str, messages: list[dict], max_tokens: int, extra_generation: dict | None = None) -> dict:
    sys_txt = "\n".join(m["content"] for m in messages if m["role"] == "system")
    contents = [{"role": "user" if m["role"] == "user" else "model", "parts": [{"text": m["content"]}]}
                for m in messages if m["role"] != "system"]
    gen = {"max_output_tokens": max_tokens}
    gen.update(extra_generation or {})
    req = {"contents": contents, "generation_config": gen}
    if sys_txt:
        req["system_instruction"] = {"parts": [{"text": sys_txt}]}
    return {"key": key, "request": req}


def estimate_batch_cost(lines: list[dict], price_in: float, price_out: float, max_out: int,
                        reasoning_allowance: int = 0, chars_per_token: float = 2.5) -> float:
    """Conservative: Vietnamese ~2.5 chars/token; output = max tokens + reasoning allowance."""
    chars = sum(len(json.dumps(ln, ensure_ascii=False)) for ln in lines)
    tin = chars / chars_per_token / max(len(lines), 1)
    return budget.estimate(len(lines), tin, max_out + reasoning_allowance, price_in, price_out, 0.5)


def parse_openai_output(line: dict) -> tuple[str, str | None, int | None, int | None, str | None]:
    cid = line.get("custom_id")
    if line.get("error"):
        return cid, None, None, None, json.dumps(line["error"])[:500]
    body = (line.get("response") or {}).get("body") or {}
    try:
        text = body["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError):
        return cid, None, None, None, "no content"
    u = body.get("usage") or {}
    return cid, text, u.get("prompt_tokens"), u.get("completion_tokens"), None


def parse_gemini_output(line: dict) -> tuple[str, str | None, int | None, int | None, str | None]:
    key = line.get("key")
    resp = line.get("response") or {}
    if line.get("error") or not resp:
        return key, None, None, None, json.dumps(line.get("error"))[:500]
    try:
        parts = resp["candidates"][0]["content"]["parts"]
        text = "".join(p.get("text", "") for p in parts if not p.get("thought"))
    except (KeyError, IndexError, TypeError):
        return key, None, None, None, "no content"
    u = resp.get("usageMetadata") or resp.get("usage_metadata") or {}

    def g(camel, snake):
        return u.get(camel, u.get(snake)) or 0

    out = g("candidatesTokenCount", "candidates_token_count") + g("thoughtsTokenCount", "thoughts_token_count")
    return key, text, g("promptTokenCount", "prompt_token_count"), out, None


def actual_cost(tokens_in: int, tokens_out: int, price_in: float, price_out: float) -> float:
    return round((tokens_in * price_in + tokens_out * price_out) / 1e6 * 0.5, 4)


# ------------------------------------------------------------------------------ vendor calls
def submit(model_key: str, batch_path: str, task: str) -> str:
    cfg = _cfg(model_key)
    lines = [json.loads(x) for x in Path(batch_path).read_text(encoding="utf-8").splitlines() if x.strip()]
    est = estimate_batch_cost(lines, cfg["price_in"], cfg["price_out"], cfg.get("max_tokens", 128),
                              cfg.get("reasoning_allowance", 0))
    job_tmp = f"{model_key}-{hashlib.sha1(batch_path.encode()).hexdigest()[:8]}"
    budget.reserve(cfg["provider"], cfg["model"], job_tmp, task, est, note=batch_path)  # raises if over cap
    if cfg["provider"] == "openai":
        from openai import OpenAI

        client = OpenAI()
        f = client.files.create(file=open(batch_path, "rb"), purpose="batch")
        job = client.batches.create(input_file_id=f.id, endpoint=cfg.get("endpoint", "/v1/chat/completions"),
                                    completion_window="24h", metadata={"task": task, "ledger": job_tmp})
        job_id = job.id
    elif cfg["provider"] == "google":
        from google import genai
        from google.genai import types

        client = genai.Client()
        up = client.files.upload(file=batch_path, config=types.UploadFileConfig(display_name=job_tmp,
                                                                                mime_type="jsonl"))
        job = client.batches.create(model=cfg["model"], src=up.name, config={"display_name": job_tmp})
        job_id = job.name
    else:
        raise SystemExit(f"provider lạ {cfg['provider']}")
    reg = paths().state / "api_jobs.jsonl"
    with reg.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps({"job_id": job_id, "ledger_id": job_tmp, "model_key": model_key, "task": task,
                             "batch": batch_path, "est_usd": est}) + "\n")
    print(f"ĐÃ GỬI {job_id} (ước tính trần {est:.2f} USD)")
    return job_id


def _job(job_id: str) -> dict:
    reg = paths().state / "api_jobs.jsonl"
    for ln in reg.read_text(encoding="utf-8").splitlines():
        d = json.loads(ln)
        if d["job_id"] == job_id:
            return d
    raise SystemExit(f"không thấy job {job_id} trong state/api_jobs.jsonl")


def poll(job_id: str) -> str:
    cfg = _cfg(_job(job_id)["model_key"])
    if cfg["provider"] == "openai":
        from openai import OpenAI

        st = OpenAI().batches.retrieve(job_id).status
    else:
        from google import genai

        st = genai.Client().batches.get(name=job_id).state.name
    print(st)
    return st


def fetch(job_id: str, out: str) -> None:
    meta = _job(job_id)
    cfg = _cfg(meta["model_key"])
    rows = []
    if cfg["provider"] == "openai":
        from openai import OpenAI

        client = OpenAI()
        job = client.batches.retrieve(job_id)
        if job.status not in ("completed", "expired", "cancelled"):
            raise SystemExit(f"batch {job_id} chưa xong: {job.status}")
        raw = client.files.content(job.output_file_id).text if job.output_file_id else ""
        if job.error_file_id:  # failed requests are reported separately
            raw += "\n" + client.files.content(job.error_file_id).text
        rows = [parse_openai_output(json.loads(x)) for x in raw.splitlines() if x.strip()]
    else:
        from google import genai

        client = genai.Client()
        job = client.batches.get(name=job_id)
        if job.state.name != "JOB_STATE_SUCCEEDED":
            raise SystemExit(f"batch {job_id}: {job.state.name}")
        raw = client.files.download(file=job.dest.file_name).decode("utf-8")
        rows = [parse_gemini_output(json.loads(x)) for x in raw.splitlines() if x.strip()]
    tin = sum(r[2] or 0 for r in rows)
    tout = sum(r[3] or 0 for r in rows)
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        for cid, text, a, b, err in rows:
            f.write(json.dumps({"request_id": cid, "raw_output": text, "tokens_in": a, "tokens_out": b,
                                "error": err, "job_id": job_id}, ensure_ascii=False) + "\n")
    cost = actual_cost(tin, tout, cfg["price_in"], cfg["price_out"])
    budget.settle(meta["ledger_id"], cost, note=f"{job_id} in={tin} out={tout}")
    print(f"OK {len(rows)} dòng → {out}; chi phí thực {cost:.4f} USD. {budget.status_line()}")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="api_batch")
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("submit"); s.add_argument("--model-key", required=True)
    s.add_argument("--batch", required=True); s.add_argument("--task", required=True)
    s = sub.add_parser("poll"); s.add_argument("--job", required=True)
    s = sub.add_parser("fetch"); s.add_argument("--job", required=True); s.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    if a.cmd == "submit":
        try:
            submit(a.model_key, a.batch, a.task)
        except budget.BudgetExceeded as e:
            print(e, file=sys.stderr)
            return 1
    elif a.cmd == "poll":
        poll(a.job)
    elif a.cmd == "fetch":
        fetch(a.job, a.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
~~~~~

### `src/vnsoc/run/kaggle_jobs.py`

<!-- FILE: src/vnsoc/run/kaggle_jobs.py | sha256: d030318bc1e241e01721dd3193bc37337dea8fa66bbc85540afb2d5b99fce565 -->
~~~~~python
"""Render / push / poll / download Kaggle GPU jobs (2×T4, one vLLM process per GPU).

Requests travel as a PRIVATE Kaggle dataset (<user>/vnsoc-requests) containing JSONL files with
{"request_id", "model_key", "messages": [...], "sampling": {...}}. Each job = one kernel version
that processes <= ~10 h of work (Kaggle sessions stop at 12 h). Outputs are appended per batch,
so a stopped job can be resumed by a new job whose shard lists the same `out` file.

  $PY -m vnsoc.run.kaggle_jobs render --job-id a1-qwen-llama --spec kaggle/specs/a1.json
  $PY -m vnsoc.run.kaggle_jobs push   --job-id a1-qwen-llama
  $PY -m vnsoc.run.kaggle_jobs status --job-id a1-qwen-llama
  $PY -m vnsoc.run.kaggle_jobs fetch  --job-id a1-qwen-llama      # -> data/runs/kaggle/<job-id>/
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

from vnsoc.paths import paths


def username() -> str:
    u = os.environ.get("KAGGLE_USERNAME")
    if not u:
        f = Path.home() / ".kaggle" / "kaggle.json"
        if f.exists():
            u = json.loads(f.read_text()).get("username")
    if not u:
        raise SystemExit("Thiếu KAGGLE_USERNAME (điền trong .env ở HG0.3)")
    return u


def slug(s: str) -> str:
    return re.sub(r"[^a-z0-9-]+", "-", s.lower()).strip("-")[:44]


def render(job_id: str, spec: dict, root=None) -> Path:
    """spec: {"shards": [...], "pip": ["vllm==X"], "dataset": "<user>/vnsoc-requests"}"""
    P = paths(root)
    d = P.root / "kaggle" / "jobs" / slug(job_id)
    d.mkdir(parents=True, exist_ok=True)
    job = {"job_id": slug(job_id), "shards": spec["shards"], "pip": spec.get("pip", [])}
    js = json.dumps(job, ensure_ascii=False)
    if "'''" in js:
        raise ValueError("spec không được chứa '''")
    tpl = (P.root / "kaggle" / "runner_template.py").read_text(encoding="utf-8")
    (d / "run.py").write_text(tpl.replace("__JOB__", js), encoding="utf-8")
    user = spec.get("user") or username()
    name = slug(job_id) if slug(job_id).startswith("vnsoc-") else f"vnsoc-{slug(job_id)}"
    meta = {
        "id": f"{user}/{name}", "title": name, "code_file": "run.py",
        "language": "python", "kernel_type": "script", "is_private": True, "enable_gpu": True,
        "enable_internet": True, "machine_shape": "NvidiaTeslaT4",
        "dataset_sources": [spec.get("dataset", f"{user}/vnsoc-requests")],
        "kernel_sources": spec.get("kernel_sources", []), "model_sources": spec.get("model_sources", []),
        "competition_sources": [],
    }
    (d / "kernel-metadata.json").write_text(json.dumps(meta, indent=1), encoding="utf-8")
    return d


def _kaggle_bin() -> str:
    venv = Path(sys.executable).parent / "kaggle"
    return str(venv) if venv.exists() else "kaggle"


def _kaggle(*args: str) -> str:
    r = subprocess.run([_kaggle_bin(), *args], capture_output=True, text=True)
    if r.returncode:
        raise SystemExit(f"kaggle {' '.join(args)} lỗi:\n{r.stdout}\n{r.stderr}")
    return r.stdout


def push(job_id: str) -> None:
    d = paths().root / "kaggle" / "jobs" / slug(job_id)
    print(_kaggle("kernels", "push", "-p", str(d), "--accelerator", "NvidiaTeslaT4"))


def status(job_id: str) -> str:
    meta = json.loads((paths().root / "kaggle" / "jobs" / slug(job_id) / "kernel-metadata.json").read_text())
    out = _kaggle("kernels", "status", meta["id"])
    print(out.strip())
    return out


def fetch(job_id: str) -> Path:
    meta = json.loads((paths().root / "kaggle" / "jobs" / slug(job_id) / "kernel-metadata.json").read_text())
    dest = paths().root / "data" / "runs" / "kaggle" / slug(job_id)
    dest.mkdir(parents=True, exist_ok=True)
    print(_kaggle("kernels", "output", meta["id"], "-p", str(dest)))
    return dest


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="kaggle_jobs")
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("render"); s.add_argument("--job-id", required=True); s.add_argument("--spec", required=True)
    for c in ("push", "status", "fetch"):
        s = sub.add_parser(c); s.add_argument("--job-id", required=True)
    a = ap.parse_args(argv)
    if a.cmd == "render":
        print(render(a.job_id, json.loads(Path(a.spec).read_text(encoding="utf-8"))))
    elif a.cmd == "push":
        push(a.job_id)
    elif a.cmd == "status":
        status(a.job_id)
    elif a.cmd == "fetch":
        print(fetch(a.job_id))
    return 0


if __name__ == "__main__":
    sys.exit(main())
~~~~~

### `src/vnsoc/schemas.py`

<!-- FILE: src/vnsoc/schemas.py | sha256: b93ef6c3163840a9cabd91106f4d7da1a3b1201cf8ede826d4d6cace4e686981 -->
~~~~~python
"""Data contracts (pydantic v2). Every JSONL file in data/interim, data/processed and data/frozen
must validate:  $PY -m vnsoc.schemas <kind> <file.jsonl>   (kind: manifest|atom|question|run|grade)

Atom = one span-verified recommendation "mẩu" (proposal §3.4). Values are value SETS.
"""
from __future__ import annotations

import json
import sys
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

System = Literal["US", "EU_UK", "WHO_global", "WHO_WPRO", "OTHER"]
SlotType = Literal["dose", "threshold", "duration", "schedule", "first_line", "classification", "target",
                   "procedure"]
ValueKind = Literal["num", "bp", "schedule", "drugs", "cat"]
ConflictStatus = Literal["conflict", "concordant", "no_counterpart", "indistinguishable"]


class Strict(BaseModel):
    model_config = ConfigDict(extra="forbid")


class ManifestRow(Strict):
    doc_key: str = Field(description="(số, năm) as 'NNNN/YYYY', e.g. '2760/2023'")
    number: str
    year: int
    kind: Literal["QĐ", "TT", "OTHER"] = "QĐ"
    title: str
    disease: str
    issued: str | None = None                 # YYYY-MM-DD
    status: Literal["current", "superseded", "partial"]
    supersedes: list[str] = []
    superseded_by: list[str] = []
    partially_amended_by: list[str] = []
    source_url: str | None = None             # official source only (kcb.vn, moh.gov.vn, ...)
    source_host: str | None = None
    downloaded: str | None = None
    sha256: str | None = None
    text_layer: bool | None = None
    ocr: bool = False
    pages: int | None = None
    in_corpus: bool = False
    notes: str = ""

    @model_validator(mode="after")
    def _no_tvpl(self):
        if self.source_url and "thuvienphapluat" in self.source_url:
            raise ValueError("source_url không được là thuvienphapluat (chỉ dùng tra cứu thủ công)")
        return self


class ValueItem(Strict):
    # num
    lo: float | None = None
    hi: float | None = None
    unit: str | None = None
    cmp: Literal[">=", ">", "<=", "<", "="] | None = None
    # bp
    sys: float | None = None
    dia: float | None = None
    # schedule
    seq: list[int] | None = None
    # drugs
    key_drugs: list[str] | None = None
    # cat
    label: str | None = None
    text: str | None = None                   # human-readable rendering, e.g. "5–10 ml/kg/giờ"


class ForeignValue(Strict):
    system: System
    source: str                               # e.g. "WHO 2009 dengue", "ADA Standards of Care 2025 §10"
    version_date: str                         # YYYY or YYYY-MM-DD
    url: str | None = None
    locator: str | None = None                # section/table/page — NO verbatim passage text
    fetched_at: str | None = None             # ISO date the page/PDF was opened to verify the value
    page_sha256: str | None = None            # hash of the fetched page/PDF (proves it was actually read)
    values: list[ValueItem]
    verified_by: Literal["auto", "student", "clinician"] | None = None


class ForeignRecord(Strict):
    """One row of data/interim/foreign_values.jsonl (the versioned foreign reference store)."""
    record_id: str
    disease: str
    topic: str                                # slot/population the value applies to
    system: System
    source: str
    version_date: str
    url: str
    locator: str
    fetched_at: str                           # required here: proves the page/PDF was opened
    page_sha256: str
    values: list[ValueItem] = Field(min_length=1)
    note: str = ""


class SupersededValue(Strict):
    guideline: str                            # 'NNNN/YYYY'
    section: str | None = None
    page: int | None = None
    values: list[ValueItem]


class Atom(Strict):
    atom_id: str
    guideline: str                            # 'NNNN/YYYY'
    section: str
    page: int
    span: str                                 # verbatim MoH text containing the value (<= 600 chars)
    valid_from: str | None = None
    valid_to: str | None = None
    partially_amended_by: list[str] = []
    disease: str
    condition: str
    population: dict[str, str]                # age/weight/pregnancy/G6PD/HBeAg/setting... (required keys vary)
    slot_type: SlotType
    intervention: str
    value_kind: ValueKind
    unit: str | None = None
    context: dict[str, float | str] = {}      # weight_kg, mg_per_ml, mg_per_tablet, analyte...
    cat_options: dict[str, list[str]] | None = None
    min_schedule_len: int | None = None
    vn: list[ValueItem] = Field(min_length=1)
    foreign: list[ForeignValue] = []
    superseded: list[SupersededValue] = []
    decoy: list[ValueItem] = []
    tolerance: float | None = None
    conflict_status: ConflictStatus | None = None
    conflict_family: str | None = None
    span_verified: bool = False
    context_checked: Literal["pass", "fail", "pending"] = "pending"
    moh_lags_evidence: bool | None = None     # clinician only
    clinical_harm: str | None = None          # clinician only: acuity x direction
    clinician_confirmed: bool | None = None
    core_problem_id: str | None = None
    pilot: bool = False
    seed_row: int | None = None
    extraction: dict = {}                     # model, prompt_hash, date

    @model_validator(mode="after")
    def _kind_fields(self):
        for it in self.vn + self.decoy:
            _check_item(self.value_kind, it)
        for f in self.foreign:
            for it in f.values:
                _check_item(self.value_kind, it)
        if self.value_kind == "num" and not self.unit:
            raise ValueError("value_kind=num cần unit chuẩn hóa")
        if self.value_kind == "cat" and not self.cat_options:
            raise ValueError("value_kind=cat cần cat_options")
        return self


def _check_item(kind: str, it: ValueItem) -> None:
    need = {"num": ("lo", "hi"), "bp": ("sys", "dia"), "schedule": ("seq",), "drugs": ("key_drugs",),
            "cat": ("label",)}[kind]
    missing = [k for k in need if getattr(it, k) is None]
    if missing:
        raise ValueError(f"giá trị kiểu {kind} thiếu {missing}")
    if kind == "num" and it.lo > it.hi:
        raise ValueError("lo > hi")


class Question(Strict):
    question_id: str
    atom_id: str
    format: Literal["short", "mcq", "vignette"]
    language: Literal["vi", "en"]
    text: str
    options: dict[str, str] | None = None      # mcq: letter -> text
    option_roles: dict[str, str] | None = None  # mcq: letter -> vn | foreign:US | superseded:NNNN/YYYY | decoy
    order_variant: int = 0
    population_complete: bool = True
    translation_qc: Literal["pass", "fail", "n/a", "pending"] = "n/a"
    oracle_passage_id: str | None = None
    gold_chunk_ids: list[str] = []
    split: Literal["ref", "cal", "test", "unassigned"] = "unassigned"   # ref = thresholds, cal = certification


class RunRecord(Strict):
    run_id: str
    model: str
    model_version: str
    date: str
    atom_id: str
    question_id: str
    format: str
    language: Literal["vi", "en"]
    condition: Literal["A0", "A1", "A2", "A3", "A4", "A5", "A6"]
    sample_idx: int = 0
    temperature: float
    max_tokens: int
    prompt_hash: str
    retrieved_ids: list[str] = []
    raw_output: str
    tokens_in: int | None = None
    tokens_out: int | None = None
    logprob_answer: float | None = None
    backend: Literal["vllm", "hf", "openai_batch", "gemini_batch", "api_sync"]
    error: str | None = None


class GradeRecord(Strict):
    run_id: str
    question_id: str
    atom_id: str
    label: int | None
    label_name: str | None
    vn_match: bool
    foreign_systems: list[str]
    superseded: list[str]
    decoy_match: bool
    parse_method: str
    multi: bool
    partial: bool
    unit_assumed: bool
    needs_llm: bool
    grader_version: str


KINDS = {"manifest": ManifestRow, "atom": Atom, "question": Question, "run": RunRecord, "grade": GradeRecord,
         "foreign": ForeignRecord}


def validate_jsonl(kind: str, path: str) -> tuple[int, list[str]]:
    model = KINDS[kind]
    n, errs = 0, []
    opener = open
    if path.endswith(".gz"):
        import gzip

        opener = gzip.open
    with opener(path, "rt", encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            if not line.strip():
                continue
            n += 1
            try:
                model.model_validate(json.loads(line))
            except Exception as e:  # noqa: BLE001
                errs.append(f"dòng {i}: {str(e)[:300]}")
    return n, errs


def main(argv=None) -> int:
    argv = argv or sys.argv[1:]
    if len(argv) != 2 or argv[0] not in KINDS:
        print(f"dùng: python -m vnsoc.schemas <{'|'.join(KINDS)}> <file.jsonl>")
        return 2
    n, errs = validate_jsonl(argv[0], argv[1])
    if errs:
        print(f"LỖI {len(errs)}/{n} dòng:\n" + "\n".join(errs[:30]))
        return 1
    print(f"OK {n} dòng hợp lệ ({argv[0]})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
~~~~~

### `src/vnsoc/state.py`

<!-- FILE: src/vnsoc/state.py | sha256: db0d9d2d342dd42c881832f76c609b10789e3457c22a45e5e3a0bf7f9da895a1 -->
~~~~~python
"""Task state machine for the project. Single source of truth: the YAML task block in
docs/02_KE_HOACH_TRIEN_KHAI.md -> state/progress.json (written ONLY through this CLI).

Stdlib only at import time (hooks use the system python3). PyYAML is imported lazily by `init`.

Usage (from the repo root):
  scripts/vs init                 # build/merge state/progress.json from the plan
  scripts/vs next [--id-only]     # next eligible Claude task (exit 3 if none)
  scripts/vs start T1.1
  scripts/vs done T1.1 [--note ...]   # verifies outputs + runs the task's check command
  scripts/vs block T1.1 --reason "..."   # needs a human; written to HUMAN_TODO.md
  scripts/vs unblock T1.1
  scripts/vs skip T5.9 --reason "DR6 ..."  # only tasks marked skippable
  scripts/vs human-done HG0.3 --note "..."  # only after the user typed: XONG HG0.3
  scripts/vs add --id R2.1 --title ... --owner claude --depends T4.7 --acceptance ... [--check ...]
  scripts/vs show [ID] | list [--status S] [--owner O] | digest | todo
"""
from __future__ import annotations

import argparse
import datetime as dt
import glob
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

from vnsoc.paths import paths, python_bin

STATUSES = ("pending", "in_progress", "done", "blocked", "skipped")
OWNERS = ("claude", "human")
REQUIRED = ("id", "title", "phase", "owner")
PLAN_FIELDS = ("id", "title", "phase", "owner", "week", "depends_on", "outputs", "acceptance",
               "check", "skill", "agent", "instructions", "not_before", "deadline", "skippable",
               "timeout_s", "gate")
TASK_BLOCK = re.compile(r"<!--\s*TASKS:BEGIN\s*-->\s*```ya?ml[^\n]*\n(.*?)```\s*<!--\s*TASKS:END\s*-->", re.S)


# ----------------------------------------------------------------------------------- utilities
def now() -> str:
    return dt.datetime.now().astimezone().isoformat(timespec="seconds")


def today() -> dt.date:
    t = os.environ.get("VNSOC_TODAY")
    return dt.date.fromisoformat(t) if t else dt.date.today()


def _date(x) -> dt.date | None:
    if x in (None, ""):
        return None
    if isinstance(x, dt.date):
        return x
    return dt.date.fromisoformat(str(x))


def _atomic_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    os.replace(tmp, path)


def append_log(P, line: str) -> None:
    P.log.parent.mkdir(parents=True, exist_ok=True)
    if not P.log.exists():
        P.log.write_text("# Nhật ký dự án (tự động + ghi tay)\n\n", encoding="utf-8")
    with P.log.open("a", encoding="utf-8") as f:
        f.write(f"- {now()} · {line}\n")


def append_decision(P, line: str) -> None:
    if not P.decisions.exists():
        P.decisions.write_text("# Quyết định (DR) đã áp dụng\n\n", encoding="utf-8")
    with P.decisions.open("a", encoding="utf-8") as f:
        f.write(f"- {now()} · {line}\n")


# ------------------------------------------------------------------------------------ plan I/O
def parse_plan(text: str) -> list[dict]:
    m = TASK_BLOCK.search(text)
    if not m:
        raise SystemExit("Không thấy khối <!-- TASKS:BEGIN --> ```yaml ... ``` <!-- TASKS:END --> trong kế hoạch")
    import yaml  # lazy

    data = yaml.safe_load(m.group(1))
    tasks = data["tasks"] if isinstance(data, dict) else data
    validate_plan(tasks)
    return tasks


def validate_plan(tasks: list[dict]) -> None:
    ids, errors = set(), []
    for t in tasks:
        for k in REQUIRED:
            if k not in t:
                errors.append(f"{t.get('id', '?')}: thiếu trường {k}")
        if t.get("id") in ids:
            errors.append(f"trùng id {t.get('id')}")
        ids.add(t.get("id"))
        if t.get("owner") not in OWNERS:
            errors.append(f"{t.get('id')}: owner phải là claude|human")
        if t.get("owner") in OWNERS and (t.get("owner") == "human") != str(t.get("id", "")).startswith("HG"):
            errors.append(f"{t.get('id')}: việc của người phải có mã HG…, việc của Claude thì không")
        if t.get("owner") == "human" and not t.get("instructions"):
            errors.append(f"{t.get('id')}: việc của người cần 'instructions'")
        unknown = set(t) - set(PLAN_FIELDS)
        if unknown:
            errors.append(f"{t.get('id')}: trường lạ {sorted(unknown)}")
    for t in tasks:
        for d in t.get("depends_on") or []:
            if d not in ids:
                errors.append(f"{t['id']}: phụ thuộc không tồn tại {d}")
    # cycle check (Kahn)
    indeg = {t["id"]: len(t.get("depends_on") or []) for t in tasks}
    children: dict[str, list[str]] = {}
    for t in tasks:
        for d in t.get("depends_on") or []:
            children.setdefault(d, []).append(t["id"])
    queue = [i for i, n in indeg.items() if n == 0]
    seen = 0
    while queue:
        i = queue.pop()
        seen += 1
        for c in children.get(i, []):
            indeg[c] -= 1
            if indeg[c] == 0:
                queue.append(c)
    if seen != len(tasks):
        errors.append("đồ thị phụ thuộc có chu trình")
    if errors:
        raise SystemExit("Kế hoạch không hợp lệ:\n  " + "\n  ".join(errors))


def load(P) -> dict:
    if not P.progress.exists():
        raise SystemExit("Chưa có state/progress.json — chạy: scripts/vs init")
    return json.loads(P.progress.read_text(encoding="utf-8"))


def save(P, st: dict) -> None:
    st["updated"] = now()
    _atomic_write(P.progress, json.dumps(st, ensure_ascii=False, indent=1))
    render_human_todo(P, st)


def fingerprint(P) -> str:
    try:
        return hashlib.sha256(P.progress.read_bytes()).hexdigest()[:16]
    except FileNotFoundError:
        return "none"


# ------------------------------------------------------------------------------------ queries
def all_deps(t: dict) -> list[str]:
    return list(t.get("depends_on") or []) + list(t.get("extra_depends") or [])


def deps_met(st: dict, t: dict) -> bool:
    return all(st["tasks"][d]["status"] in ("done", "skipped") for d in all_deps(t) if d in st["tasks"])


def eligible_claude(st: dict) -> list[dict]:
    out = []
    for i in st["order"]:
        t = st["tasks"][i]
        if t["owner"] != "claude" or t["status"] not in ("pending", "in_progress"):
            continue
        if not deps_met(st, t):
            continue
        nb = _date(t.get("not_before"))
        if nb and nb > today():
            continue
        out.append(t)
    out.sort(key=lambda t: (t["status"] != "in_progress", st["order"].index(t["id"])))
    return out


def waiting_human(st: dict) -> list[dict]:
    out = []
    for i in st["order"]:
        t = st["tasks"][i]
        if t["owner"] != "human" or t["status"] not in ("pending", "in_progress") or not deps_met(st, t):
            continue
        nb = _date(t.get("not_before"))
        if nb and nb > today():
            continue
        out.append(t)
    return out


def blocked(st: dict) -> list[dict]:
    return [st["tasks"][i] for i in st["order"] if st["tasks"][i]["status"] == "blocked"]


def current_phase(st: dict) -> str:
    for i in st["order"]:
        if st["tasks"][i]["status"] not in ("done", "skipped"):
            return str(st["tasks"][i].get("phase"))
    return "HOÀN TẤT"


# ------------------------------------------------------------------------------------ commands
def init(P, force: bool = False) -> dict:
    tasks = parse_plan(P.plan.read_text(encoding="utf-8"))
    old = None
    if P.progress.exists() and not force:
        old = json.loads(P.progress.read_text(encoding="utf-8"))
    st = {"plan_sha256": hashlib.sha256(P.plan.read_bytes()).hexdigest(), "created": now(),
          "updated": now(), "order": [], "tasks": {}}
    for t in tasks:
        rec = {k: t.get(k) for k in PLAN_FIELDS}
        for k in ("not_before", "deadline"):
            if isinstance(rec.get(k), dt.date):
                rec[k] = rec[k].isoformat()
        rec["depends_on"] = list(t.get("depends_on") or [])
        rec["outputs"] = list(t.get("outputs") or [])
        rec.update(status="pending", history=[], note="", source="plan", extra_depends=[])
        if old and t["id"] in old["tasks"]:
            o = old["tasks"][t["id"]]
            rec.update(status=o["status"], history=o.get("history", []), note=o.get("note", ""),
                       extra_depends=o.get("extra_depends", []))
        st["order"].append(t["id"])
        st["tasks"][t["id"]] = rec
    if old:
        st["created"] = old.get("created", st["created"])
        for i in old["order"]:
            o = old["tasks"][i]
            if i not in st["tasks"] and o.get("source") == "dynamic":
                st["order"].append(i)
                st["tasks"][i] = o
            elif i not in st["tasks"]:
                print(f"CẢNH BÁO: task {i} không còn trong kế hoạch; bỏ khỏi state", file=sys.stderr)
    P.human_ack.mkdir(parents=True, exist_ok=True)
    save(P, st)
    return st


def _get(st: dict, tid: str) -> dict:
    if tid not in st["tasks"]:
        raise SystemExit(f"Không có task {tid}")
    return st["tasks"][tid]


def _event(t: dict, event: str, note: str = "") -> None:
    t["history"].append({"t": now(), "event": event, "note": note})


def start(P, tid: str) -> None:
    st = load(P)
    t = _get(st, tid)
    if t["owner"] != "claude":
        raise SystemExit(f"{tid} là việc của người (human gate), không start được")
    if not deps_met(st, t):
        raise SystemExit(f"{tid} chưa đủ điều kiện: phụ thuộc {all_deps(t)} chưa xong")
    if t["status"] in ("done", "skipped"):
        raise SystemExit(f"{tid} đã {t['status']}")
    t["status"] = "in_progress"
    _event(t, "start")
    save(P, st)
    append_log(P, f"{tid} bắt đầu · {t['title']}")


def check_outputs(P, t: dict) -> list[str]:
    missing = []
    for pat in t.get("outputs") or []:
        hits = [h for h in glob.glob(str(P.root / pat), recursive=True)
                if Path(h).is_dir() or Path(h).stat().st_size > 0]
        if not hits:
            missing.append(pat)
    return missing


def run_check(P, t: dict) -> tuple[int, str]:
    cmd = t.get("check")
    if not cmd:
        return 0, "(không có lệnh kiểm tra)"
    env = dict(os.environ, PY=python_bin(P.root), VNSOC_ROOT=str(P.root),
               PYTHONPATH=str(P.root / "src") + os.pathsep + os.environ.get("PYTHONPATH", ""))
    try:
        r = subprocess.run(["bash", "-c", cmd], cwd=P.root, env=env, capture_output=True, text=True,
                           timeout=int(t.get("timeout_s") or 1800))
    except subprocess.TimeoutExpired:
        return 124, f"quá thời gian: {cmd}"
    return r.returncode, (r.stdout[-3000:] + "\n" + r.stderr[-3000:]).strip()


def done(P, tid: str, note: str = "") -> int:
    st = load(P)
    t = _get(st, tid)
    if t["owner"] != "claude":
        raise SystemExit(f"{tid} là việc của người: dùng human-done sau khi người dùng gõ 'XONG {tid}'")
    if not deps_met(st, t):
        raise SystemExit(f"{tid}: phụ thuộc chưa xong")
    missing = check_outputs(P, t)
    if missing:
        print(f"CHƯA XONG {tid}: thiếu sản phẩm {missing}", file=sys.stderr)
        return 1
    code, out = run_check(P, t)
    if code != 0:
        print(f"CHƯA XONG {tid}: lệnh kiểm tra thất bại (mã {code})\n$ {t.get('check')}\n{out}", file=sys.stderr)
        return 1
    t["status"] = "done"
    _event(t, "done", note)
    save(P, st)
    append_log(P, f"{tid} XONG · {t['title']}" + (f" · {note}" if note else ""))
    print(f"OK {tid} xong. {out[-500:] if out else ''}")
    return 0


def block(P, tid: str, reason: str) -> None:
    st = load(P)
    t = _get(st, tid)
    t["status"] = "blocked"
    t["note"] = reason
    _event(t, "block", reason)
    save(P, st)
    append_log(P, f"{tid} BỊ CHẶN · {reason}")


def unblock(P, tid: str) -> None:
    st = load(P)
    t = _get(st, tid)
    if t["status"] != "blocked":
        raise SystemExit(f"{tid} không ở trạng thái blocked")
    t["status"] = "pending"
    _event(t, "unblock")
    save(P, st)
    append_log(P, f"{tid} gỡ chặn")


def skip(P, tid: str, reason: str) -> None:
    st = load(P)
    t = _get(st, tid)
    if not t.get("skippable"):
        raise SystemExit(f"{tid} không được phép bỏ qua (không có skippable: true). Hỏi người dùng.")
    if t["owner"] == "human" and not any(st["tasks"][d]["status"] == "skipped" for d in all_deps(t)):
        raise SystemExit(f"{tid} là việc của người dùng: chỉ bỏ qua được khi việc đầu vào của nó đã bị bỏ qua")
    t["status"] = "skipped"
    _event(t, "skip", reason)
    save(P, st)
    append_decision(P, f"Bỏ qua {tid} ({t['title']}): {reason}")
    append_log(P, f"{tid} bỏ qua · {reason}")


def human_done(P, tid: str, note: str = "") -> int:
    st = load(P)
    t = _get(st, tid)
    if t["owner"] != "human":
        raise SystemExit(f"{tid} là việc của Claude: dùng done")
    ack = P.human_ack / tid
    if not ack.exists():
        print(f"TỪ CHỐI: chưa có xác nhận của người dùng cho {tid}. Người dùng phải tự gõ trong chat: XONG {tid}",
              file=sys.stderr)
        return 2
    missing = check_outputs(P, t)
    if missing:
        print(f"{tid}: thiếu bằng chứng {missing} (ghi lại thông tin người dùng cung cấp vào đó)", file=sys.stderr)
        return 1
    code, out = run_check(P, t)
    if code != 0:
        print(f"{tid}: lệnh kiểm tra thất bại\n{out}", file=sys.stderr)
        return 1
    t["status"] = "done"
    _event(t, "human_done", note or ack.read_text(encoding="utf-8")[:300])
    save(P, st)
    append_log(P, f"{tid} (người dùng) XONG · {note}")
    print(f"OK {tid} ghi nhận là xong")
    return 0


def add(P, tid: str, title: str, owner: str, phase: str, depends: list[str], acceptance: str,
        outputs: list[str], check: str | None, instructions: str | None, blocks: list[str] | None = None) -> None:
    """Add a dynamic task. `blocks`: existing tasks that must now also wait for this one."""
    st = load(P)
    for b in blocks or []:
        if _get(st, b)["status"] in ("done", "skipped"):
            raise SystemExit(f"{b} đã xong, không thể chặn thêm")
    if tid in st["tasks"]:
        raise SystemExit(f"Đã có {tid}")
    for d in depends:
        _get(st, d)
    if set(depends) & set(blocks or []):
        raise SystemExit("task mới không thể vừa phụ thuộc vừa chặn cùng một task")
    if owner == "human" and not instructions:
        raise SystemExit("Việc của người cần --instructions")
    if (owner == "human") != tid.startswith("HG"):
        raise SystemExit("Quy ước: việc của người có mã bắt đầu bằng HG; việc của Claude thì không")
    rec = {k: None for k in PLAN_FIELDS}
    rec.update(id=tid, title=title, owner=owner, phase=phase, depends_on=depends, acceptance=acceptance,
               outputs=outputs, check=check, instructions=instructions, status="pending", history=[],
               note="", source="dynamic")
    rec["extra_depends"] = []
    _event(rec, "add")
    st["order"].append(tid)
    st["tasks"][tid] = rec
    for b in blocks or []:
        st["tasks"][b].setdefault("extra_depends", []).append(tid)
        _event(st["tasks"][b], "wait_for", tid)
    save(P, st)
    append_log(P, f"thêm task {tid} · {title}")


# ------------------------------------------------------------------------------------ reports
def budget_line(P) -> str:
    try:
        from vnsoc.budget import status_line
        return status_line(P.root)
    except Exception as e:  # pragma: no cover - never break hooks
        return f"ngân sách: không đọc được ({e.__class__.__name__})"


def digest(P, n_log: int = 6) -> str:
    st = load(P)
    counts = {s: 0 for s in STATUSES}
    for t in st["tasks"].values():
        counts[t["status"]] += 1
    el = eligible_claude(st)
    wh = waiting_human(st)
    bl = blocked(st)
    lines = [f"[vn-soc-audit] Giai đoạn: {current_phase(st)} · xong {counts['done']}/{len(st['tasks'])}"
             f" · đang làm {counts['in_progress']} · chặn {counts['blocked']} · bỏ qua {counts['skipped']}",
             budget_line(P)]
    if P.pause.exists():
        lines.append("TẠM DỪNG: có state/PAUSE — không tự chạy tiếp; chờ người dùng /resume")
    if el:
        lines.append("Việc Claude làm tiếp: " + "; ".join(f"{t['id']} {t['title']}" for t in el[:3]))
    else:
        lines.append("Không còn việc Claude làm được ngay (chờ người dùng hoặc chờ ngày).")
    if wh:
        lines.append("ĐANG CHỜ NGƯỜI DÙNG: " + "; ".join(
            f"{t['id']} {t['title']}" + (f" (hạn {t['deadline']})" if t.get("deadline") else "") for t in wh))
    if bl:
        lines.append("BỊ CHẶN: " + "; ".join(f"{t['id']}: {t.get('note', '')[:80]}" for t in bl))
    if P.log.exists():
        tail = [ln for ln in P.log.read_text(encoding="utf-8").splitlines() if ln.startswith("- ")][-n_log:]
        if tail:
            lines.append("Nhật ký gần nhất:\n  " + "\n  ".join(tail))
    return "\n".join(lines)


def render_human_todo(P, st: dict) -> None:
    wh, bl = waiting_human(st), blocked(st)
    out = ["# Việc cần BẠN làm (tự sinh — đừng sửa tay)", "",
           f"Cập nhật: {now()}. Làm xong việc nào thì gửi trong Claude Code một tin nhắn có dòng BẮT ĐẦU bằng "
           "`XONG <mã>` (ví dụ `XONG HG0.3 Llama: đang chờ`) kèm thông tin được yêu cầu.", ""]
    if not wh and not bl:
        out.append("Hiện không có việc nào chờ bạn.")
    for t in wh:
        out += [f"## {t['id']} — {t['title']}" + (f" (HẠN {t['deadline']})" if t.get("deadline") else ""), "",
                str(t.get("instructions") or "").strip(), ""]
        if t.get("acceptance"):
            out += [f"Xong khi: {t['acceptance']}", ""]
    if bl:
        out += ["## Việc Claude bị chặn, cần bạn gỡ", ""]
        out += [f"- **{t['id']}** {t['title']}: {t.get('note', '')}" for t in bl]
    _atomic_write(P.human_todo, "\n".join(out) + "\n")


def show(P, tid: str | None) -> str:
    st = load(P)
    if tid:
        return json.dumps(_get(st, tid), ensure_ascii=False, indent=1)
    return "\n".join(f"{i:8s} {st['tasks'][i]['status']:11s} {st['tasks'][i]['owner']:6s} {st['tasks'][i]['title']}"
                     for i in st["order"])


# ------------------------------------------------------------------------------------ CLI
def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="vs", description="Trạng thái công việc vn-soc-audit")
    ap.add_argument("--root", default=None)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("init"); s.add_argument("--force", action="store_true")
    s = sub.add_parser("next"); s.add_argument("--id-only", action="store_true")
    for name in ("start", "unblock"):
        s = sub.add_parser(name); s.add_argument("id")
    s = sub.add_parser("done"); s.add_argument("id"); s.add_argument("--note", default="")
    s = sub.add_parser("block"); s.add_argument("id"); s.add_argument("--reason", required=True)
    s = sub.add_parser("skip"); s.add_argument("id"); s.add_argument("--reason", required=True)
    s = sub.add_parser("human-done"); s.add_argument("id"); s.add_argument("--note", default="")
    s = sub.add_parser("add")
    s.add_argument("--id", required=True); s.add_argument("--title", required=True)
    s.add_argument("--owner", default="claude", choices=OWNERS); s.add_argument("--phase", default="dynamic")
    s.add_argument("--depends", nargs="*", default=[]); s.add_argument("--acceptance", default="")
    s.add_argument("--outputs", nargs="*", default=[]); s.add_argument("--check", default=None)
    s.add_argument("--instructions", default=None)
    s.add_argument("--blocks", nargs="*", default=[], help="task hiện có phải chờ task mới này")
    s = sub.add_parser("show"); s.add_argument("id", nargs="?")
    s = sub.add_parser("list"); s.add_argument("--status"); s.add_argument("--owner")
    sub.add_parser("digest"); sub.add_parser("todo"); sub.add_parser("validate-plan")
    sub.add_parser("pause"); sub.add_parser("resume")
    s = sub.add_parser("autopilot"); s.add_argument("mode", choices=["on", "off"])
    a = ap.parse_args(argv)
    P = paths(a.root)
    if a.cmd == "init":
        st = init(P, a.force)
        print(f"OK: {len(st['tasks'])} task. " + digest(P).splitlines()[0])
    elif a.cmd == "validate-plan":
        tasks = parse_plan(P.plan.read_text(encoding="utf-8"))
        print(f"OK: kế hoạch hợp lệ, {len(tasks)} task")
    elif a.cmd == "next":
        el = eligible_claude(load(P))
        if not el:
            print("NONE")
            return 3
        print(el[0]["id"] if a.id_only else json.dumps(el[0], ensure_ascii=False, indent=1))
    elif a.cmd == "start":
        start(P, a.id)
    elif a.cmd == "done":
        return done(P, a.id, a.note)
    elif a.cmd == "block":
        block(P, a.id, a.reason)
    elif a.cmd == "unblock":
        unblock(P, a.id)
    elif a.cmd == "skip":
        skip(P, a.id, a.reason)
    elif a.cmd == "human-done":
        return human_done(P, a.id, a.note)
    elif a.cmd == "add":
        add(P, a.id, a.title, a.owner, a.phase, a.depends, a.acceptance, a.outputs, a.check, a.instructions,
            a.blocks)
    elif a.cmd == "show":
        print(show(P, a.id))
    elif a.cmd == "list":
        st = load(P)
        for i in st["order"]:
            t = st["tasks"][i]
            if (not a.status or t["status"] == a.status) and (not a.owner or t["owner"] == a.owner):
                print(f"{i:8s} {t['status']:11s} {t['owner']:6s} {t['title']}")
    elif a.cmd == "digest":
        print(digest(P))
    elif a.cmd == "pause":
        P.pause.parent.mkdir(parents=True, exist_ok=True)
        P.pause.write_text(now() + "\n", encoding="utf-8")
        append_log(P, "TẠM DỪNG (state/PAUSE)")
        print("Đã tạm dừng. Dùng /resume để chạy tiếp.")
    elif a.cmd == "resume":
        P.pause.unlink(missing_ok=True)
        append_log(P, "CHẠY TIẾP (bỏ state/PAUSE)")
        print("Đã bỏ tạm dừng.")
    elif a.cmd == "autopilot":
        if a.mode == "on":
            P.autopilot.write_text(now() + "\n", encoding="utf-8")
        else:
            P.autopilot.unlink(missing_ok=True)
        append_log(P, f"autopilot {a.mode}")
        print(f"autopilot {a.mode}")
    elif a.cmd == "todo":
        render_human_todo(P, load(P))
        print(P.human_todo.read_text(encoding="utf-8"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
~~~~~

### `tests/conftest.py`

<!-- FILE: tests/conftest.py | sha256: 8ce3f267cc108c96121098a9a97032db1df517c311de350d00eecca29f8c6319 -->
~~~~~python
import shutil
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

MINI_PLAN = '''# Kế hoạch thử
<!-- TASKS:BEGIN -->
```yaml
tasks:
  - {id: T0.1, title: "Tạo repo", phase: P0, owner: claude, outputs: ["README.md"], check: "test -f README.md"}
  - {id: HG0.2, title: "Điền khóa", phase: P0, owner: human, depends_on: [T0.1], instructions: "Điền .env"}
  - {id: T0.3, title: "Chạy thử", phase: P0, owner: claude, depends_on: [HG0.2], check: "exit 0"}
  - {id: T0.4, title: "Chờ ngày", phase: P0, owner: claude, depends_on: [T0.1], not_before: "2099-01-01"}
  - {id: T0.5, title: "Có thể bỏ", phase: P0, owner: claude, depends_on: [T0.1], skippable: true}
```
<!-- TASKS:END -->
'''


@pytest.fixture
def proj(tmp_path, monkeypatch):
    """A throw-away project root with the mini plan, hooks and configs copied in."""
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "02_KE_HOACH_TRIEN_KHAI.md").write_text(MINI_PLAN, encoding="utf-8")
    (tmp_path / "pyproject.toml").write_text("[project]\nname='x'\n")
    shutil.copytree(ROOT / "src", tmp_path / "src")
    shutil.copytree(ROOT / ".claude", tmp_path / ".claude")
    shutil.copytree(ROOT / "configs", tmp_path / "configs")
    monkeypatch.setenv("VNSOC_ROOT", str(tmp_path))
    monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(tmp_path))
    return tmp_path
~~~~~

### `tests/test_budget_numbers.py`

<!-- FILE: tests/test_budget_numbers.py | sha256: aeef2f58d5382d78204e545e5487fedfb7a9006d72aa31078b783c9d15a7fb6c -->
~~~~~python
import pytest

from vnsoc import budget, numbers
from vnsoc.paths import paths


def test_budget(proj):
    assert budget.remaining(proj) == pytest.approx(38)
    budget.reserve("google", "m", "j1", "T5.5", 10, root=proj)
    budget.settle("j1", 3.2, root=proj)
    assert budget.spent(proj) == pytest.approx(3.2)
    with pytest.raises(budget.BudgetExceeded):
        budget.reserve("google", "m", "j2", "T5.5", 35, root=proj)
    assert budget.estimate(1000, 300, 128, 0.25, 1.5) == pytest.approx(0.1335)


def test_numbers(proj):
    P = paths(proj)
    (proj / "src" / "analysis_demo.py").write_text("x")
    import json
    P.results.mkdir(exist_ok=True)
    P.numbers.write_text(json.dumps({"h1.delta": {"value": 0.21, "display": "21,0%", "source": "src/analysis_demo.py"}}))
    P.manuscript.mkdir(exist_ok=True)
    (P.manuscript / "main.md").write_text(
        "# 1 Results\n\nIn 2026, H1 held: Δ = {{h1.delta}} at α = {{=0.05}} (Table 2) [3].\nModel Qwen3-8B on T4.\n")
    assert numbers.verify(proj) == 0
    (P.manuscript / "main.md").write_text("Δ was 21% and {{h9.missing}}\n")
    assert numbers.verify(proj) == 1
    assert numbers.bare_numbers("accuracy 87.5% in 400 atoms") == ["87.5%", "400"]
    (P.manuscript / "main.md").write_text("Design: 25–35 guidelines ({{=25–35}}), α = {{=0,10}}; bogus {{=0,37}}\n")
    assert numbers.verify(proj) == 1                               # 0,37 is not a configured constant
    (P.manuscript / "main.md").write_text("Design: {{=25–35}} guidelines, α = {{=0,10}}\n")
    assert numbers.verify(proj) == 0
    (P.manuscript / "fmc").mkdir()
    (P.manuscript / "fmc" / "abs.md").write_text("Δ = {{h1.delta}}\n")
    assert numbers.render(proj) == 0
    assert (P.manuscript / "build" / "fmc" / "abs.md").read_text() == "Δ = 21,0%\n"


def test_put_only_from_analysis_code(proj):
    with pytest.raises(ValueError):
        numbers.put("x", 1, "1", root=proj)
~~~~~

### `tests/test_check.py`

<!-- FILE: tests/test_check.py | sha256: 6b0d6b8857de37908d520dd0ea4f5dc735f8aa0a375aea708839881fb66aae8c -->
~~~~~python
import json

from vnsoc.check import main
from test_schemas import BASE
from pathlib import Path

ROOT_KIT = Path(__file__).resolve().parents[1]


def test_check_jsonl_and_count(proj, tmp_path):
    f = tmp_path / "a.jsonl"
    rows = [dict(BASE, atom_id=f"a{i}", span_verified=True, conflict_status="conflict", conflict_family=f"f{i % 3}")
            for i in range(5)]
    f.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n", encoding="utf-8")
    assert main(["jsonl", "atom", str(f), "--min", "5", "--require", "span_verified=true"]) == 0
    assert main(["jsonl", "atom", str(f), "--min", "6"]) == 1
    assert main(["count", str(f), "--min", "5", "--where", "conflict_status=conflict"]) == 0
    assert main(["families", str(f), "--min", "3"]) == 0 and main(["families", str(f), "--min", "4"]) == 1


def test_nofill_and_size(tmp_path):
    f = tmp_path / "abs.md"
    f.write_text("Kết quả: [a] mẩu\n", encoding="utf-8")
    assert main(["nofill", str(f)]) == 1
    f.write_text("Kết quả: 12 mẩu\n", encoding="utf-8")
    assert main(["nofill", str(f)]) == 0
    assert main(["maxsize", str(f), "1000"]) == 0


def test_check_runs(tmp_path):
    d = tmp_path / "runs"
    d.mkdir()
    rec = dict(run_id="r", model="qwen3_8b", model_version="abc", date="2026-11-05", atom_id="a", question_id="q",
               format="short", language="vi", condition="A1", temperature=0.0, max_tokens=128, prompt_hash="h",
               raw_output="ĐÁP ÁN: 15 ml/kg/giờ", backend="vllm")
    (d / "x.jsonl").write_text("\n".join(json.dumps(dict(rec, run_id=f"r{i}")) for i in range(10)) + "\n")
    plan = tmp_path / "plan.json"
    plan.write_text(json.dumps({"qwen3_8b|A1|vi|short": 10, "qwen3_8b|A2|vi|short": 10}))
    assert main(["runs", str(d), "--plan", str(plan), "--conditions", "A1"]) == 0
    assert main(["runs", str(d), "--plan", str(plan)]) == 1          # A2 missing


def test_review_gate_requires_user(proj, monkeypatch):
    from vnsoc import state
    from vnsoc.paths import paths
    from test_review import write
    P = paths(proj)
    state.init(P)
    write(proj, 6)                                          # panel fails
    assert main(["review", "M1"]) == 1
    (proj / "review" / "M1" / "response.md").write_text("Người dùng quyết định: tiếp tục")
    assert main(["review", "M1"]) == 1                      # Claude writing text is not enough
    state.add(P, "HGM1", "Quyết định", "human", "review", [], "", [], None, "chọn A hoặc B")
    P.human_ack.mkdir(exist_ok=True)
    (P.human_ack / "HGM1").write_text("XONG HGM1 chọn A")
    assert state.human_done(P, "HGM1") == 0
    assert main(["review", "M1"]) == 0


def test_runs_models_from_config(tmp_path, proj):
    d = tmp_path / "runs"
    d.mkdir()
    rec = dict(run_id="r", model="qwen3_8b", model_version="abc", date="2026-11-05", atom_id="a", question_id="q",
               format="short", language="vi", condition="A1", temperature=0.0, max_tokens=128, prompt_hash="h",
               raw_output="x", backend="vllm")
    (d / "x.jsonl").write_text(json.dumps(rec) + "\n")
    plan = tmp_path / "plan.json"
    plan.write_text(json.dumps({"qwen3_8b|A1|vi|short": 1, "cheap_1|A1|vi|short": 5}))
    assert main(["runs", str(d), "--plan", str(plan), "--models-from", "open"]) == 0
    assert main(["runs", str(d), "--plan", str(plan), "--models-from", "api_cheap"]) == 1


def test_kaggle_render_name(proj):
    from vnsoc.run.kaggle_jobs import render
    import shutil
    (proj / "kaggle").mkdir()
    shutil.copy(ROOT_KIT / "kaggle" / "runner_template.py", proj / "kaggle" / "runner_template.py")
    d = render("vnsoc-weights", {"shards": [], "user": "u"}, proj)
    meta = json.loads((d / "kernel-metadata.json").read_text())
    assert d.name == "vnsoc-weights" and meta["id"] == "u/vnsoc-weights" and meta["is_private"] is True
    d2 = render("a1-qwen", {"shards": [], "user": "u"}, proj)
    assert json.loads((d2 / "kernel-metadata.json").read_text())["id"] == "u/vnsoc-a1-qwen"
    compile((d / "run.py").read_text(), "run.py", "exec")
~~~~~

### `tests/test_freeze.py`

<!-- FILE: tests/test_freeze.py | sha256: b2c021089d3b6c6d9784276db4f90c05db581ec629498eba759d0ee9a114a2d9 -->
~~~~~python
import json

import pytest

from vnsoc.freeze import freeze
from vnsoc.paths import paths
from test_schemas import BASE


def test_freeze_atoms(proj):
    P = paths(proj)
    (proj / "data" / "interim").mkdir(parents=True)
    src = proj / "data" / "interim" / "atoms.jsonl"
    src.write_text(json.dumps(BASE, ensure_ascii=False) + "\n", encoding="utf-8")
    a = freeze("atoms", proj)
    b = freeze("atoms", proj)
    assert a[0].name == "atoms_v1.jsonl" and b[0].name == "atoms_v2.jsonl"
    assert "atoms_v1.jsonl" in (proj / "data" / "frozen" / "SHA256SUMS").read_text()
    assert "Đóng băng atoms" in P.decisions.read_text()
    src.write_text(json.dumps({**BASE, "vn": []}) + "\n{bad json\n", encoding="utf-8")
    with pytest.raises(SystemExit):
        freeze("atoms", proj)
~~~~~

### `tests/test_grade.py`

<!-- FILE: tests/test_grade.py | sha256: fddacc630d0981750ae36ac4f080a7a75cb2ddf7f892cf6d702b4ad7a3fbaf63 -->
~~~~~python
"""Golden cases from the seed conflicts (proposal §3.3). Values here are TEST FIXTURES, not data."""
import pytest

from vnsoc.grade import compute_tolerance, conflict_status, grade_mcq, grade_short

SYN = {"artemether-lumefantrine": ["artemether-lumefantrin", "coartem"], "artemether": [], "lumefantrine": ["lumefantrin"],
       "quinine": ["quinin"], "clindamycin": [], "dihydroartemisinin-piperaquine": []}
COMBOS = {"artemether-lumefantrine": ["artemether", "lumefantrine"], "quinine+clindamycin": ["quinine", "clindamycin"]}


def atom(**kw):
    a = {"atom_id": "t", "foreign": [], "superseded": [], "decoy": []}
    a.update(kw)
    a["tolerance"] = compute_tolerance(a)
    return a


DENGUE = atom(value_kind="num", unit="ml/kg/h", vn=[{"lo": 15, "hi": 15}],
              foreign=[{"system": "WHO_global", "values": [{"lo": 5, "hi": 10}]}], decoy=[{"lo": 20, "hi": 25}])
HTN = atom(value_kind="bp", vn=[{"sys": 140, "dia": 90}],
           foreign=[{"system": "US", "values": [{"sys": 130, "dia": 80}]}, {"system": "EU_UK", "values": [{"sys": 140, "dia": 90}]}],
           decoy=[{"sys": 150, "dia": 100}])
RABIES = atom(value_kind="schedule", vn=[{"seq": [0, 3, 7, 14, 28]}],
              foreign=[{"system": "US", "values": [{"seq": [0, 3, 7, 14]}]}], decoy=[{"seq": [0, 7, 21, 28]}])
ADRENALINE = atom(value_kind="num", unit="mg", vn=[{"lo": 0.5, "hi": 1.0}],
                  foreign=[{"system": "EU_UK", "values": [{"lo": 0.5, "hi": 0.5}]}])
MALARIA_PREG = atom(value_kind="drugs", vn=[{"key_drugs": ["quinine+clindamycin"]}],
                    foreign=[{"system": "US", "values": [{"key_drugs": ["artemether-lumefantrine"]}]}],
                    decoy=[{"key_drugs": ["dihydroartemisinin-piperaquine"]}])
HBV = atom(value_kind="num", unit="U/L", vn=[{"lo": 30, "hi": 30}],
           foreign=[{"system": "US", "values": [{"lo": 70, "hi": 70}]}],
           superseded=[{"guideline": "3310/2019", "values": [{"lo": 40, "hi": 40}]}], decoy=[{"lo": 50, "hi": 50}])
PEDS_ADR = atom(value_kind="num", unit="ug", context={"mg_per_ml": 1, "weight_kg": 10}, vn=[{"lo": 250, "hi": 250}],
                foreign=[{"system": "EU_UK", "values": [{"lo": 150, "hi": 150}]}], decoy=[{"lo": 350, "hi": 350}])


def g(out, a, **kw):
    return grade_short(out, a, synonyms=SYN, combos=COMBOS, **kw)


def test_status():
    assert conflict_status(DENGUE) == "conflict"
    assert conflict_status(ADRENALINE) == "concordant"          # seed row 14: 0.5 mg inside 0.5–1 mg
    assert conflict_status(HTN) == "conflict"                   # US only
    assert conflict_status(atom(value_kind="num", unit="mg", vn=[{"lo": 1, "hi": 1}])) == "no_counterpart"
    clash = atom(value_kind="num", unit="mg", vn=[{"lo": 10, "hi": 10}], foreign=[{"system": "US", "values": [{"lo": 5, "hi": 5}]}],
                 superseded=[{"guideline": "x", "values": [{"lo": 5, "hi": 5}]}])
    assert conflict_status(clash) == "indistinguishable"
    assert DENGUE["tolerance"] == pytest.approx(2.5) and HTN["tolerance"] == pytest.approx(5)


@pytest.mark.parametrize("out,label,extra", [
    ("ĐÁP ÁN: 15 ml/kg/giờ", "correct", {}),
    ("ĐÁP ÁN: 10 ml/kg/giờ", "foreign", {"foreign_systems": ["WHO_global"]}),
    ("ĐÁP ÁN: 5–10 ml/kg/h", "foreign", {}),
    ("ĐÁP ÁN: 12 ml/kg/h", "foreign", {}),                      # within tolerance of WHO 5–10
    ("ĐÁP ÁN: 20 ml/kg/giờ", "unattributed", {"decoy_match": True}),
    ("ĐÁP ÁN: 15 ml/kg/giờ (Bộ Y tế); WHO 2009 là 5–10 ml/kg/giờ", "correct_aware", {"multi": True}),
    ("Tôi không chắc chắn.", "abstain", {}),
    ("Bạn đang hỏi theo hướng dẫn của quốc gia nào?", "abstain", {}),       # no condition given -> not credited
])
def test_dengue(out, label, extra):
    r = g(out, DENGUE)
    assert r.label_name == label
    for k, v in extra.items():
        assert getattr(r, k) == v


def test_ask_country_only_aware_without_cue():
    q = "Bạn hỏi theo hướng dẫn của quốc gia nào?"
    assert g(q, DENGUE, condition="A0").label_name == "correct_aware"
    assert g(q, DENGUE, condition="A1").label_name == "abstain"


def test_needs_llm_when_ambiguous():
    r = g("Có thể truyền 10 hoặc 20 ml/kg/giờ tùy đáp ứng", DENGUE)
    assert r.label is None and r.needs_llm


def test_htn_rabies_adrenaline_malaria_hbv():
    assert g("ĐÁP ÁN: 130/80 mmHg", HTN).label_name == "foreign"
    assert g("ĐÁP ÁN: 130/80 mmHg", HTN).foreign_systems == ["US"]
    assert g("ĐÁP ÁN: ≥ 140/90 mmHg", HTN).label_name == "correct"
    assert g("ĐÁP ÁN: ngày 0, 3, 7, 14", RABIES).label_name == "foreign"
    assert g("ĐÁP ÁN: N0-3-7-14-28", RABIES).label_name == "correct"
    assert g("ĐÁP ÁN: 0,5 mg", ADRENALINE).label_name == "correct"
    assert g("ĐÁP ÁN: quinin + clindamycin 7 ngày", MALARIA_PREG).label_name == "correct"
    assert g("ANSWER: artemether-lumefantrine", MALARIA_PREG, lang="en").label_name == "foreign"
    assert g("ANSWER: quinine plus clindamycin; the CDC recommends artemether-lumefantrine", MALARIA_PREG,
             lang="en").label_name == "correct_aware"
    assert g("ĐÁP ÁN: ALT > 40 U/L", HBV).label_name == "temporal"
    assert g("ĐÁP ÁN: ALT > 30 U/L", HBV).label_name == "correct"
    assert g("ĐÁP ÁN: 0,25 ml", PEDS_ADR).label_name == "correct"          # ml -> µg via 1 mg/ml
    assert g("ĐÁP ÁN: 0,15 mg", PEDS_ADR).label_name == "foreign"


def test_think_block_and_unit_mismatch():
    assert g("<think>maybe 10</think>\nĐÁP ÁN: 15 ml/kg/giờ", DENGUE).label_name == "correct"
    r = g("ĐÁP ÁN: 3 viên", DENGUE)
    assert r.label_name == "unattributed" and r.parse_method == "unit_mismatch"


def test_mcq():
    roles = {"A": "vn", "B": "foreign:US", "C": "decoy", "D": "superseded:3310/2019"}
    assert grade_mcq("ĐÁP ÁN: B", roles).label_name == "foreign"
    assert grade_mcq("C", roles).decoy_match
    assert grade_mcq("ĐÁP ÁN: D", roles).label_name == "temporal"
    assert grade_mcq("không biết", roles).label_name == "abstain"
~~~~~

### `tests/test_hooks.py`

<!-- FILE: tests/test_hooks.py | sha256: 004fc149e268b9181cfbe91387d746e37b3bd99307dffa839d444a836d4319ca -->
~~~~~python
"""Hooks are run exactly as Claude Code runs them: JSON on stdin, exit code + stderr."""
import json
import subprocess
import sys

import pytest

from vnsoc import state
from vnsoc.paths import paths


def run_hook(proj, name, payload):
    r = subprocess.run([sys.executable, str(proj / ".claude" / "hooks" / name)], input=json.dumps(payload),
                       capture_output=True, text=True, env={"CLAUDE_PROJECT_DIR": str(proj), "PATH": "/usr/bin:/bin"})
    return r.returncode, r.stdout, r.stderr


def bash(proj, cmd):
    return run_hook(proj, "guard_bash.py", {"tool_name": "Bash", "tool_input": {"command": cmd}, "cwd": str(proj)})[0]


@pytest.mark.parametrize("cmd,code", [
    ("ls -la", 0), ("scripts/vs next", 0), (".venv/bin/python -m pytest", 0), ("cat .env.example", 0),
    ("curl -sSL https://thuvienphapluat.vn/van-ban/x.aspx", 2), ("python3 scrape.py thuvienphapluat", 2),
    ("rm -rf data/frozen/atoms_v1.jsonl", 2), ("rm -rf data/interim/tmp", 0), ("mv docs/01_DE_CUONG.md /tmp", 2),
    ("echo x > state/progress.json", 2), ("echo x > results/numbers.json", 2), ("cat .env", 2),
    ("echo $OPENAI_API_KEY", 2), ("printenv", 2), ("git push --force origin main", 2), ("git reset --hard HEAD~1", 2),
    ("sudo apt install r-base", 2), ('claude -p "XONG HG0.3"', 2), ("scripts/autopilot.sh 5", 2),
    ("touch state/.human_ack/HG0.3", 2), ("kaggle datasets create -p d --public", 2), ("kaggle datasets create -p d -u", 2), ("kaggle kernels push -p kaggle/jobs/x", 0),
])
def test_guard_bash(proj, cmd, code):
    assert bash(proj, cmd) == code


def test_guard_bash_budget(proj):
    cmd = ".venv/bin/python -m vnsoc.run.api_batch submit --model-key cheap_1 --batch b.jsonl --task T5.5"
    assert bash(proj, cmd) == 0
    (proj / "state").mkdir(exist_ok=True)
    (proj / "state" / "budget_ledger.csv").write_text(
        "timestamp,provider,model,job_id,task,kind,est_usd,actual_usd,note\nt,g,m,j1,T,reserve,38.5,,\n")
    assert bash(proj, cmd) == 2


@pytest.mark.parametrize("path,code", [
    ("docs/01_DE_CUONG.md", 2), ("docs/02_KE_HOACH_TRIEN_KHAI.md", 2), ("state/progress.json", 2),
    ("results/numbers.json", 2), ("data/frozen/atoms_v1.jsonl", 2), (".env", 2), (".claude/hooks/guard_bash.py", 2),
    ("src/vnsoc/extract/atomize.py", 0), ("manuscript/main.md", 0), ("docs/DECISIONS.md", 0),
])
def test_guard_files(proj, path, code):
    payload = {"tool_name": "Write", "tool_input": {"file_path": str(proj / path), "content": "x"}}
    assert run_hook(proj, "guard_files.py", payload)[0] == code


def test_guard_web(proj):
    assert run_hook(proj, "guard_web.py", {"tool_input": {"url": "https://thuvienphapluat.vn/x"}})[0] == 2
    assert run_hook(proj, "guard_web.py", {"tool_input": {"url": "https://kcb.vn/phac-do"}})[0] == 0


def test_user_prompt_ack(proj):
    state.init(paths(proj))
    code, out, _ = run_hook(proj, "user_prompt.py", {"prompt": "XONG HG0.2 — đã điền khóa", "session_id": "s"})
    assert code == 0 and (proj / "state" / ".human_ack" / "HG0.2").exists() and "HG0.2" in out
    run_hook(proj, "user_prompt.py", {"prompt": "làm tiếp T0.3 đi", "session_id": "s"})
    assert not (proj / "state" / ".human_ack" / "T0.3").exists()


def test_stop_hook(proj):
    P = paths(proj)
    state.init(P)
    payload = {"session_id": "abc", "stop_hook_active": False}
    assert run_hook(proj, "stop_continue.py", payload)[0] == 0          # autopilot off
    P.autopilot.write_text("on")
    code, _, err = run_hook(proj, "stop_continue.py", payload)
    assert code == 2 and "T0.1" in err
    codes = [run_hook(proj, "stop_continue.py", payload)[0] for _ in range(4)]
    assert 0 in codes                                                  # stall guard releases
    P.pause.write_text("x")
    assert run_hook(proj, "stop_continue.py", {"session_id": "new"})[0] == 0


def test_session_start_and_post_edit(proj):
    state.init(paths(proj))
    code, out, _ = run_hook(proj, "session_start.py", {"source": "startup"})
    assert code == 0 and "T0.1" in out
    bad = proj / "src" / "bad.py"
    bad.write_text("def f(:\n")
    assert run_hook(proj, "post_edit.py", {"tool_input": {"file_path": str(bad)}})[0] == 2
    bad.write_text("def f():\n    return 1\n")
    assert run_hook(proj, "post_edit.py", {"tool_input": {"file_path": str(bad)}})[0] == 0
~~~~~

### `tests/test_integrity.py`

<!-- FILE: tests/test_integrity.py | sha256: a761750a81823cb155828b31a1079d6e51ec67987e817f5fec736bb247e420f9 -->
~~~~~python
"""Static integrity checks on the repo itself (run in `make test`; tasks add code under src/ that must keep passing)."""
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
ID = re.compile(r"\b(?:T\d+\.\d+[a-z]?|HG\d+\.\d+[a-z]?|HGM\d+)\b")   # 'HG2.9_osf.txt' is a file name, not an id


def _plan_ids():
    plan = ROOT / "docs" / "02_KE_HOACH_TRIEN_KHAI.md"
    if not plan.exists():
        pytest.skip("chưa có docs/02")
    block = plan.read_text(encoding="utf-8").split("<!-- TASKS:BEGIN -->")[1]
    return set(re.findall(r"^- id: (\S+)", block, re.M))


def test_task_ids_mentioned_in_instructions_exist():
    ids = _plan_ids() | {"HGM2", "HGM3", "HGM4"}          # milestone decision gates are added dynamically
    files = [ROOT / "CLAUDE.md", *ROOT.glob(".claude/**/*.md"), *ROOT.glob(".claude/**/*.py")]
    missing = {(f.relative_to(ROOT).as_posix(), m) for f in files for m in ID.findall(f.read_text(encoding="utf-8"))
               if m not in ids}
    assert not missing, sorted(missing)


def _code_files():
    for base in ("src", "scripts", "kaggle"):
        for f in (ROOT / base).rglob("*"):
            if f.is_file() and f.suffix in (".py", ".sh", ".R", "") and "__pycache__" not in f.parts:
                yield f


def test_no_forbidden_access_in_code():
    allowed_tvpl = {"src/vnsoc/schemas.py"}
    allowed_api = {"src/vnsoc/run/api_batch.py"}
    allowed_ack = {"src/vnsoc/state.py", "src/vnsoc/paths.py", "src/vnsoc/check.py"}  # check.py only reads
    bad = []
    for f in _code_files():
        rel = f.relative_to(ROOT).as_posix()
        text = f.read_text(encoding="utf-8", errors="ignore")
        if "thuvienphapluat" in text and rel not in allowed_tvpl:
            bad.append(f"{rel}: thuvienphapluat")
        if re.search(r"^\s*(?:import openai|from openai|from google import genai|import google\.genai)", text, re.M) \
                and rel not in allowed_api:
            bad.append(f"{rel}: gọi SDK API trả phí ngoài api_batch (không qua sổ ngân sách)")
        if ".human_ack" in text and rel not in allowed_ack:
            bad.append(f"{rel}: chạm vào xác nhận của người dùng")
    assert not bad, bad
~~~~~

### `tests/test_ltt.py`

<!-- FILE: tests/test_ltt.py | sha256: 76416a406142d5539d768b1610b164c02251325c6c3508d7db43675a636937e3 -->
~~~~~python
import numpy as np

from vnsoc.ltt import certified_bounds, ltt_thresholds, make_grids, simulate, split_by_atom, thresholds_from_reference


def test_bounds_cover_pool_risk():
    rng = np.random.default_rng(1)
    s_ref, _, g_ref = simulate(3000, rng)
    thr = thresholds_from_reference(s_ref, g_ref)
    fails = 0
    for _ in range(60):
        s, e, g = simulate(4000, rng)
        idx = rng.permutation(len(s))[:2000]
        b = certified_bounds(s[idx], e[idx], g[idx], thr, 0.10)
        for (gg, c), r in b.items():
            m = (g == gg) & (s >= thr[gg][c])
            if m.any() and e[m].mean() > r["U"]:
                fails += 1
                break
    assert fails / 60 <= 0.2


def test_ltt_returns_inf_when_nothing_certifiable():
    s = np.linspace(0, 1, 200); e = np.ones(200, dtype=int); g = np.zeros(200, dtype=int)
    grids = make_grids(s, g)
    assert ltt_thresholds(s, e, g, grids)[0] == np.inf


def test_split_by_atom_keeps_atoms_together():
    atoms = np.array(["a", "a", "b", "b", "c", "c", "d"])
    cal = split_by_atom(atoms, 0.5, seed=3)
    for a in np.unique(atoms):
        assert len(set(cal[atoms == a])) == 1
~~~~~

### `tests/test_normalize.py`

<!-- FILE: tests/test_normalize.py | sha256: 419a4c984fba0eebc32b4febb52e03b41e97966387f338441994c9c4cc7cba68 -->
~~~~~python
import pytest

from vnsoc.normalize_vi import Num, convert, parse_bps, parse_cats, parse_drugs, parse_number, parse_nums, parse_schedules


@pytest.mark.parametrize("tok,lang,val", [
    ("0,5", "vi", 0.5), ("5.000", "vi", 5000), ("1.500", "vi", 1500), ("0.5", "vi", 0.5), ("0.500", "vi", 0.5),
    ("2,000", "vi", 2000), ("2,5", "vi", 2.5), ("1.000.000", "vi", 1e6), ("1.000,5", "vi", 1000.5),
    ("2,000", "en", 2000), ("0.5", "en", 0.5), ("2.000", "en", 2000), ("0,5", "en", 0.5), ("½", "vi", 0.5),
])
def test_parse_number(tok, lang, val):
    assert parse_number(tok, lang) == pytest.approx(val)


def test_ranges_and_units():
    assert parse_nums("0,5–1 mg") == [Num(0.5, 1.0, "mg")]
    assert parse_nums("10 - 15mg/kg") == [Num(10, 15, "mg/kg")]
    assert parse_nums("từ 10 đến 15 ml/kg/giờ") == [Num(10, 15, "ml/kg/h")]
    assert parse_nums("from 10 to 15 mg", "en") == [Num(10, 15, "mg")]
    assert parse_nums("5 - 10 ml/kg/h")[0].unit == "ml/kg/h"


def test_comparators_and_citations():
    n = parse_nums("HBV DNA > 2.000 IU/mL (QĐ 1740/QĐ-BYT 2026)")
    assert n == [Num(2000, 2000, "IU/mL", ">")]
    assert parse_nums("HbA1c ≥ 9%") == [Num(9, 9, "%", ">=")]          # the 1 in A1c is not a value
    assert parse_nums("theo ADA 2025 là < 55 mg/dL") == [Num(55, 55, "mg/dL", "<")]
    assert parse_nums("từ 45 tuổi")[0].cmp == ">="
    assert parse_nums("2000 IU/mL")[0].lo == 2000                        # not stripped as a year


def test_convert():
    assert convert(250, "ug", "mg") == pytest.approx(0.25)
    assert convert(0.25, "ml", "ug", {"mg_per_ml": 1}) == pytest.approx(250)
    assert convert(4, "tablet", "mg", {"mg_per_tablet": 7.5}) == pytest.approx(30)
    assert convert(0.01, "mg/kg", "ug", {"weight_kg": 10}) == pytest.approx(100)
    assert convert(5.0, "mmol/L", "mg/dL", {"analyte": "glucose"}) == pytest.approx(90.08, rel=1e-3)
    assert convert(5000, "/uL", "10^9/L") == pytest.approx(5)
    assert convert(1, "mg", "ml/kg/h") is None


def test_bp():
    assert parse_bps("≥ 140/90 mmHg")[0].sys == 140
    assert parse_bps("ALT 30/19 U/L") == []
    assert parse_bps("QĐ 3192/2010: 140/90")[0].dia == 90


def test_schedules():
    assert parse_schedules("N0-3-7-14-28")[0].seq == (0, 3, 7, 14, 28)
    assert parse_schedules("ngày 0, 3, 7, 14")[0].seq == (0, 3, 7, 14)
    assert parse_schedules("2, 3, 4 tháng")[0].unit == "month"
    assert parse_schedules("QĐ 1622/QĐ-BYT 2014: N0-3-7-14-28")[0].seq == (0, 3, 7, 14, 28)


SYN = {"artemether-lumefantrine": ["artemether-lumefantrin", "coartem"], "artemether": [], "lumefantrine": ["lumefantrin"],
       "pyronaridine-artesunate": ["pyronaridin-artesunat"], "artesunate": ["artesunat"], "primaquine": ["primaquin"],
       "quinine": ["quinin"], "clindamycin": []}
COMBOS = {"artemether-lumefantrine": ["artemether", "lumefantrine"], "quinine+clindamycin": ["quinine", "clindamycin"]}


def test_drugs():
    assert parse_drugs("Artemether–lumefantrine (Coartem)", SYN, COMBOS).names == {"artemether-lumefantrine"}
    assert parse_drugs("artemether + lumefantrin", SYN, COMBOS).names == {"artemether-lumefantrine"}
    assert parse_drugs("Pyronaridin-artesunat 3 ngày + primaquin", SYN, COMBOS).names == {"pyronaridine-artesunate", "primaquine"}
    assert parse_drugs("Quinin 7 ngày + clindamycin 7 ngày", SYN, COMBOS).names == {"quinine+clindamycin"}


def test_cats():
    opts = {"one_step": ["mot buoc", "one-step"], "two_step": ["hai buoc", "two-step"]}
    assert parse_cats("Nghiệm pháp 75 g một bước", opts).labels == {"one_step"}
~~~~~

### `tests/test_plan.py`

<!-- FILE: tests/test_plan.py | sha256: 8a881b0f3be6d04c10d95a2517f867e9ad5325b11ca6e15696fafc261f266ea3 -->
~~~~~python
"""The real plan (docs/02) must be valid and every task reachable (no deadlock), given time passes."""
import datetime as dt
import json
import shutil

import pytest

from vnsoc import state
from vnsoc.paths import paths


def test_plan_is_valid_and_reachable(tmp_path, monkeypatch):
    real = paths()
    if not real.plan.exists():
        pytest.skip("docs/02_KE_HOACH_TRIEN_KHAI.md chưa có")
    (tmp_path / "docs").mkdir()
    shutil.copy(real.plan, tmp_path / "docs" / real.plan.name)
    shutil.copytree(real.root / "configs", tmp_path / "configs")
    P = paths(tmp_path)
    st = state.init(P)
    day = dt.date(2026, 9, 25)
    for _ in range(1000):
        monkeypatch.setenv("VNSOC_TODAY", day.isoformat())
        st = state.load(P)
        nxt = (state.eligible_claude(st) or state.waiting_human(st) or [None])[0]
        if nxt:
            nxt["status"] = "done"
            P.progress.write_text(json.dumps(st))
            continue
        left = [i for i in st["order"] if st["tasks"][i]["status"] != "done"]
        if not left:
            break
        day += dt.timedelta(days=1)
        assert day < dt.date(2027, 6, 1), f"kẹt: {left}"
    assert all(t["status"] == "done" for t in state.load(P)["tasks"].values())
~~~~~

### `tests/test_review.py`

<!-- FILE: tests/test_review.py | sha256: 18ffb83c30cafd0ef979294727eb782c5ad86f89b29e23109b80d301c84d53c2 -->
~~~~~python
from vnsoc.review import PANEL, aggregate

TPL = """```yaml
reviewer: {n}
milestone: M1
recommendation: {rec}
scores: {{importance: {s}, novelty: {s}, rigor: {s}, feasibility: {s}, q1_likelihood: {s}, fit: {s}}}
fatal_flaws: {fatal}
required_changes:
  - {{id: 1, severity: major, where: "atoms", what: "fix", acceptance: "test"}}
```
Nhận xét.
"""


def write(proj, s=8, rec="minor", fatal="[]"):
    d = proj / "review" / "M1"
    d.mkdir(parents=True, exist_ok=True)
    for n in PANEL:
        (d / f"{n}.md").write_text(TPL.format(n=n, s=s, rec=rec, fatal=fatal), encoding="utf-8")


def test_pass_and_fail(proj):
    write(proj, 8)
    ok, _ = aggregate("M1", proj)
    assert ok and "ĐẠT" in (proj / "review" / "M1" / "summary.md").read_text()
    write(proj, 6)
    assert not aggregate("M1", proj)[0]
    write(proj, 9, fatal='["circular grading"]')
    assert not aggregate("M1", proj)[0]


def test_missing_report(proj):
    write(proj, 8)
    (proj / "review" / "M1" / "rev-novelty.md").unlink()
    ok, msg = aggregate("M1", proj)
    assert not ok and "rev-novelty" in msg
~~~~~

### `tests/test_schemas.py`

<!-- FILE: tests/test_schemas.py | sha256: cb77ff76420831f9392df6e5096fc20fc232981cdbe5d1ebcdcb5f8ed809cf82 -->
~~~~~python
import pytest
from pydantic import ValidationError

from vnsoc.schemas import Atom, ManifestRow

BASE = dict(atom_id="a1", guideline="2760/2023", section="C.2.1", page=12, span="…15 ml/kg/giờ…", disease="dengue",
            condition="sốc", population={"age": ">=16"}, slot_type="dose", intervention="dịch truyền",
            value_kind="num", unit="ml/kg/h", vn=[{"lo": 15, "hi": 15}])


def test_atom_ok():
    Atom.model_validate(BASE)


def test_atom_rejects_bad_items():
    with pytest.raises(ValidationError):
        Atom.model_validate({**BASE, "vn": [{"seq": [0, 3]}]})
    with pytest.raises(ValidationError):
        Atom.model_validate({**BASE, "unit": None})
    with pytest.raises(ValidationError):
        Atom.model_validate({**BASE, "extra_field": 1})


def test_manifest_forbids_tvpl():
    with pytest.raises(ValidationError):
        ManifestRow.model_validate(dict(doc_key="1/2020", number="1", year=2020, title="x", disease="x", status="current",
                                        source_url="https://thuvienphapluat.vn/x"))


def test_foreign_record_requires_provenance():
    from vnsoc.schemas import ForeignRecord
    ok = dict(record_id="f1", disease="dengue", topic="sốc người lớn: dịch đầu", system="WHO_global", source="WHO 2009",
              version_date="2009", url="https://www.ncbi.nlm.nih.gov/books/NBK143161/", locator="ch. 2",
              fetched_at="2026-10-10", page_sha256="ab" * 32, values=[{"lo": 5, "hi": 10, "unit": "ml/kg/h"}])
    ForeignRecord.model_validate(ok)
    with pytest.raises(ValidationError):
        ForeignRecord.model_validate({k: v for k, v in ok.items() if k != "page_sha256"})
~~~~~

### `tests/test_state.py`

<!-- FILE: tests/test_state.py | sha256: cb3202b0c8b297238c948603836bd859829b7739fe6776d5c93dfeb8d1552412 -->
~~~~~python
import json

import pytest

from vnsoc import state
from vnsoc.paths import paths


def test_flow(proj, monkeypatch):
    P = paths(proj)
    st = state.init(P)
    assert [t["id"] for t in state.eligible_claude(st)] == ["T0.1"]
    assert state.done(P, "T0.1") == 1                 # README.md missing -> not done
    (proj / "README.md").write_text("x")
    assert state.done(P, "T0.1") == 0
    st = state.load(P)
    assert [t["id"] for t in state.eligible_claude(st)] == ["T0.5"]   # T0.3 waits HG0.2, T0.4 waits date
    assert [t["id"] for t in state.waiting_human(st)] == ["HG0.2"]
    assert "HG0.2" in P.human_todo.read_text()
    assert state.human_done(P, "HG0.2") == 2          # no ack from the user yet
    P.human_ack.mkdir(exist_ok=True)
    (P.human_ack / "HG0.2").write_text("XONG HG0.2")
    assert state.human_done(P, "HG0.2") == 0
    with pytest.raises(SystemExit):
        state.skip(P, "T0.3", "no")                   # not skippable
    state.skip(P, "T0.5", "DR6")
    assert "T0.5" in P.decisions.read_text()
    state.start(P, "T0.3")
    assert state.done(P, "T0.3") == 0
    monkeypatch.setenv("VNSOC_TODAY", "2099-01-02")
    assert [t["id"] for t in state.eligible_claude(state.load(P))] == ["T0.4"]


def test_init_merges_and_dynamic(proj):
    P = paths(proj)
    state.init(P)
    (proj / "README.md").write_text("x")
    state.done(P, "T0.1")
    state.add(P, "R1.1", "Sửa theo hội đồng", "claude", "review", ["T0.1"], "ok", [], None, None)
    with pytest.raises(SystemExit):
        state.add(P, "X1", "người", "human", "p", [], "", [], None, "làm đi")   # human ids must start with HG
    st = state.init(P)                                  # re-init keeps status + dynamic tasks
    assert st["tasks"]["T0.1"]["status"] == "done" and "R1.1" in st["tasks"]


def test_plan_validation_errors():
    bad = [{"id": "T1", "title": "a", "phase": "p", "owner": "claude", "depends_on": ["T2"]},
           {"id": "T2", "title": "b", "phase": "p", "owner": "claude", "depends_on": ["T1"]}]
    with pytest.raises(SystemExit):
        state.validate_plan(bad)
    with pytest.raises(SystemExit):
        state.validate_plan([{"id": "HG1", "title": "a", "phase": "p", "owner": "human"}])  # no instructions


def test_digest(proj):
    P = paths(proj)
    state.init(P)
    d = state.digest(P)
    assert "T0.1" in d and "Ngân sách" in d
    json.loads(P.progress.read_text())


def test_blocks_adds_dependency(proj):
    P = paths(proj)
    state.init(P)
    (proj / "README.md").write_text("x")
    state.done(P, "T0.1")
    assert "T0.5" in [t["id"] for t in state.eligible_claude(state.load(P))]
    state.add(P, "R1.1", "sửa", "claude", "review", ["T0.1"], "ok", [], None, None, blocks=["T0.5"])
    ids = [t["id"] for t in state.eligible_claude(state.load(P))]
    assert "R1.1" in ids and "T0.5" not in ids
    state.done(P, "R1.1")
    st = state.init(P)                                    # re-init keeps extra dependency + dynamic task
    assert st["tasks"]["T0.5"]["extra_depends"] == ["R1.1"]
    assert "T0.5" in [t["id"] for t in state.eligible_claude(st)]
~~~~~

