export const meta = {
  name: 'main-atom-extraction',
  description: 'Main-study atom extraction over the 25-guideline corpus (resumable: only todo chunks are extracted): chunked extractors per document, independent audit (precision sample + recall on sampled pages), repair when needed',
  phases: [
    { title: 'Extract', detail: 'one extractor per page chunk (or repair of calibrated documents)' },
    { title: 'Audit', detail: 'independent auditor per document' },
    { title: 'Repair', detail: 'apply audit findings per document' },
  ],
}
const SH = 'cd "/d/phan chau trinh _ y khoa" && PYTHONUTF8=1 .venv/bin/python'
// Thư mục tạm cho --out tự kiểm và bản sao lưu (không có dấu cách; ngoài repo).
const SCR = 'C:/Users/Admin/AppData/Local/Temp/vnsoc_wf/extract'
const CTX = `Dự án vn-soc-audit (Git Bash /d/phan chau trinh _ y khoa). Python: ${SH} ... . CLAUDE.md áp dụng nghiêm: không bịa giá trị/trang/quần thể; không đọc data/runs/; không truy cập trang luật tư nhân; không commit; không sửa src/, configs/, data/raw, manifest.
ĐỌC KỸ TRƯỚC KHI LÀM: configs/extraction_protocol.md (giao thức 1.1 — bắt buộc, đặc biệt §5), src/vnsoc/schemas.py (Atom, ValueItem, SlotType). Bộ đọc số/thuốc đã mở rộng (grader 1.3.1): trước khi coi một thuốc/đơn vị là "không đọc được", THỬ bằng ${SH} -c "from vnsoc.grade import parse_values; ..." hoặc vnsoc.normalize_vi.parse_nums/parse_drugs. Bảng dùng dấu chấm thập phân kiểu Anh ("3.125 mg") mà bộ đọc hiểu thành 3125 → không tạo mẩu, ghi _skipped với reason "other" và ghi chú decimal_style.
Công cụ đọc PDF: ${SH} -m vnsoc.extract.verify_span --help (--page KEY TRANG; --image KEY TRANG xuất PNG để mở bằng Read — dùng cho bảng/lưu đồ và trang OCR; --find KEY "chuỗi"). Trang OCR được áp tự động.
Trường extraction.protocol_sha256: lấy bằng sha256sum configs/extraction_protocol.md.`

const partName = (d, c) => d.chunks.length === 1 ? d.key.replace('/', '_') : `${d.key.replace('/', '_')}__p${String(c[0]).padStart(3, '0')}-${String(c[1]).padStart(3, '0')}`
const idRule = (d, c) => d.chunks.length === 1 ? `A-${d.key.replace('/', '_')}-NNN (đánh liên tục)` : `A-${d.key.replace('/', '_')}-p${String(c[0]).padStart(3, '0')}-NNN (NNN đánh liên tục trong phần này; tiền tố p${String(c[0]).padStart(3, '0')} để không trùng phần khác)`

const extractP = (d, c) => `Bạn là atom-extractor. ${CTX}
VIỆC: trích MỌI mẩu khuyến cáo thỏa giao thức trong văn bản ${d.key} (${d.topic}), CHỈ các trang PDF ${c[0]}–${c[1]} (trên tổng ${d.pages} trang; phần khác do agent khác làm — khuyến cáo nằm vắt qua trang ${c[1]}/${c[1] + 1} thì phần có trang BẮT ĐẦU câu sẽ xử lý, nếu không kiểm được thì ghi _skipped reason span_across_pages). Đọc lần lượt từng trang; trang hành chính (quyết định, mục lục, ban biên soạn) ghi "không có mẩu".
Ghi: data/interim/atoms_parts/${partName(d, c)}.jsonl (atom_id theo mẫu ${idRule(d, c)}), data/interim/atoms_parts/${partName(d, c)}_skipped.jsonl, data/interim/atoms_parts/${partName(d, c)}_coverage.md (mỗi trang: số mẩu hoặc lý do không có). Chỉ ghi 3 file này.
Tự kiểm: ${SH} -m vnsoc.extract.atoms_merge --only ${partName(d, c)} --out ${SCR}/${partName(d, c)}.jsonl → 0 mẩu bị LOẠI.
Trả về: số mẩu (theo slot_type, value_kind), số dòng skipped theo reason, trang khó.`

const repairCalP = d => `Bạn là atom-extractor, làm lại văn bản ${d.key} (${d.topic}, ${d.pages} trang) đã trích thử theo giao thức 1.0. ${CTX}
Đầu vào: data/interim/atoms_parts/${d.key.replace('/', '_')}.jsonl (mẩu hiện có), review/extraction_calibration/${d.key.replace('/', '_')}.md và .json (kiểm toán độc lập: lỗi fix/error, bỏ sót trên trang mẫu, lỗi hệ thống), review/extraction_calibration/reader_inventory.md (bộ đọc 1.3.1 — đơn vị cần đổi cho 24 mẩu trích thử, ví dụ l → L/min, cm → cmH2O, g → g/L, mg → mg/day theo đúng văn bản), data/interim/atoms_parts/${d.key.replace('/', '_')}_coverage.md (khuyến cáo trước đây bị chặn vì thiếu thuốc/đơn vị).
VIỆC: (1) sửa mọi mẩu fix/error theo kiểm toán (không đổi giá trị trừ khi văn bản nói khác; mẩu không phải khuyến cáo Bộ Y tế → xóa, ghi _skipped); (2) đổi đơn vị thay thế sang đơn vị đúng; (3) áp giao thức 1.1 §5 cho CẢ văn bản: thêm các mẩu khác quần thể bị gộp/bỏ, khuyến cáo phân loại (chỉ định, chống chỉ định, không dùng...), tần suất, required_terms bắt buộc; (4) đọc lại các khuyến cáo trước đây bị chặn vì thiếu thuốc/đơn vị và tạo mẩu nếu nay đọc được; (5) cập nhật extraction.protocol = "extraction_protocol 1.1" và protocol_sha256 cho mọi mẩu. Giữ atom_id cũ cho mẩu cũ; mẩu mới đánh tiếp số.
Ghi: data/interim/atoms_parts/${d.key.replace('/', '_')}.jsonl, _skipped.jsonl, _coverage.md (sao lưu bản cũ vào ${SCR}/backup_${d.key.replace('/', '_')}.jsonl trước).
Tự kiểm: ${SH} -m vnsoc.extract.atoms_merge --only ${d.key.replace('/', '_')} --out ${SCR}/${d.key.replace('/', '_')}.jsonl → 0 LOẠI.
Trả về: số mẩu trước/sau, số sửa, số thêm, skipped theo reason.`

const auditP = (d, ex) => `Bạn là KIỂM TOÁN VIÊN ĐỘC LẬP (integrity-auditor, AI — không phải người) cho mẩu trích từ văn bản ${d.key} (${d.topic}, ${d.pages} trang). ${CTX}
Các file mẩu: data/interim/atoms_parts/${d.key.replace('/', '_')}*.jsonl (không tính _skipped); _skipped và _coverage đi kèm. Tóm tắt người trích: ${JSON.stringify(ex).slice(0, 1500)}
KIỂM (KHÔNG sửa file mẩu; ghi review/extraction_audit/${d.key.replace('/', '_')}.md và .json):
1. Chạy ${SH} -m vnsoc.extract.atoms_merge --only <từng phần> --out ${SCR}/audit_<phần>.jsonl → ghi số LOẠI.
2. ĐỘ CHÍNH XÁC trên MẪU NGẪU NHIÊN có hạt giống cố định (random.Random(20260927), ghi rõ): min(40, tổng) mẩu. Mỗi mẩu: (a) span nguyên văn đúng trang; (b) giá trị/đơn vị đúng (mở ảnh trang nếu bảng/OCR); (c) quần thể và required_terms đủ phân biệt đáp án; (d) đúng là khuyến cáo Bộ Y tế, slot/value_kind hợp; (e) tập vn không thiếu giá trị cùng quần thể trong văn bản. Phán quyết ok/fix/error kèm sửa đề xuất.
3. ĐỘ PHỦ: chọn ngẫu nhiên có hạt giống ${d.pages > 60 ? 8 : 5} trang chuyên môn; tự liệt kê mọi mẩu thỏa giao thức trên các trang đó TRƯỚC khi mở file; so → bỏ sót/tổng (đếm riêng bỏ sót đã được ghi ở _skipped với lý do hợp lệ).
4. Lỗi hệ thống (lặp lại ≥ 3 lần) — mô tả và mẩu ví dụ.
Trả về JSON theo schema: n (tổng mẩu), sampled, ok, fix, error, missed, recall_total, issues (mỗi mục một lỗi cụ thể có atom_id/trang), needs_repair (true nếu có error, fix ≥ 5% mẫu, hoặc bỏ sót > 10%).`

const repairP = (d, a) => `Bạn là atom-extractor, sửa mẩu văn bản ${d.key} theo kiểm toán độc lập. ${CTX}
Kiểm toán: review/extraction_audit/${d.key.replace('/', '_')}.md và .json. Tóm tắt: ${JSON.stringify(a).slice(0, 2500)}
VIỆC: (1) sửa mọi mẩu error/fix đã nêu; (2) thêm các mẩu bỏ sót trên trang mẫu; (3) với MỖI lỗi hệ thống: rà lại TOÀN văn bản (mọi phần data/interim/atoms_parts/${d.key.replace('/', '_')}*.jsonl) và sửa mọi mẩu cùng lỗi, thêm mọi mẩu cùng loại bị bỏ; (4) nếu thấy kiểm toán sai → giữ nguyên và ghi lý do vào review/extraction_audit/${d.key.replace('/', '_')}_response.md. Mẩu mới đánh tiếp số trong đúng file phần của trang đó. Sao lưu trước vào ${SCR}/pre_repair_<phần>.jsonl.
Tự kiểm mọi phần bằng atoms_merge --only → 0 LOẠI.
Trả về: số sửa, số thêm, số xóa, lỗi hệ thống đã xử lý, điểm bác bỏ.`

const SCH = { type: 'object', properties: { n: { type: 'integer' }, sampled: { type: 'integer' }, ok: { type: 'integer' }, fix: { type: 'integer' }, error: { type: 'integer' }, missed: { type: 'integer' }, recall_total: { type: 'integer' }, needs_repair: { type: 'boolean' }, issues: { type: 'array', items: { type: 'string' } }, summary: { type: 'string' } }, required: ['summary'] }

// args = logs/wf/extract_args.json từ scripts/workflows/resume_args.py: mỗi văn bản {key, pages, topic, chunks, todo, repair}.
// todo = các phần còn phải trích (phần đã có file mẩu + độ phủ đủ trang được bỏ qua); văn bản nào cũng qua kiểm toán.
const docs = args
const todoOf = d => d.todo || d.chunks
log(`${docs.length} văn bản, ${docs.reduce((s, d) => s + todoOf(d).length, 0)} phần cần trích`)
const out = await pipeline(docs,
  d => d.repair
    ? agent(repairCalP(d), { label: `recal:${d.key}`, phase: 'Extract', schema: SCH, agentType: 'atom-extractor' }).then(r => [r])
    : todoOf(d).length === 0
      ? Promise.resolve([])
      : parallel(todoOf(d).map(c => () => agent(extractP(d, c), { label: `ext:${d.key}:${c[0]}-${c[1]}`, phase: 'Extract', schema: SCH, agentType: 'atom-extractor' }))),
  (ex, d) => agent(auditP(d, (ex || []).map(x => x && x.summary)), { label: `audit:${d.key}`, phase: 'Audit', schema: SCH, agentType: 'integrity-auditor' }).then(a => ({ ex, a })),
  (x, d) => (x.a && x.a.needs_repair)
    ? agent(repairP(d, x.a), { label: `repair:${d.key}`, phase: 'Repair', schema: SCH, agentType: 'atom-extractor' }).then(r => ({ doc: d.key, ...x, r }))
    : { doc: d.key, ...x, r: null },
)
return out.map(o => o && ({ doc: o.doc, extracted: (o.ex || []).map(e => e && e.n), audit: o.a && { n: o.a.n, sampled: o.a.sampled, ok: o.a.ok, fix: o.a.fix, error: o.a.error, missed: o.a.missed, recall_total: o.a.recall_total, needs_repair: o.a.needs_repair }, repair: o.r && o.r.summary }))
