export const meta = {
  name: 'atom-extraction-calibration',
  description: 'Calibrate main-study atom extraction on 4 small guidelines: one extractor + one independent auditor (precision + missed recommendations) each',
  phases: [
    { title: 'Extract', detail: 'extract every value recommendation per protocol, code-checked' },
    { title: 'Audit', detail: 'independent check of each atom + recall on sampled pages' },
  ],
}
const SH = 'cd "/d/phan chau trinh _ y khoa" && PYTHONUTF8=1 .venv/bin/python'
const SCR = 'C:/Users/Admin/AppData/Local/Temp/claude/d--phan-chau-trinh---y-khoa/2de32612-1105-4b6a-9f6c-5dab64d37c64/scratchpad/extract'
const CTX = `Dự án vn-soc-audit (Git Bash /d/phan chau trinh _ y khoa), 27/9/2026. Python: ${SH} ... . CLAUDE.md áp dụng nghiêm: không bịa giá trị, trang, quần thể; không đọc data/runs/; không truy cập trang luật tư nhân; không commit. Đọc KỸ configs/extraction_protocol.md (giao thức trích — bắt buộc) và src/vnsoc/schemas.py (Atom, ValueItem). Mẩu thí điểm mẫu (định dạng tham khảo, KHÔNG chép giá trị): data/interim/pilot_atoms.jsonl. Công cụ đọc PDF: ${SH} -m vnsoc.extract.verify_span --help (--page KEY TRANG in chữ trang; --image KEY TRANG xuất PNG để mở bằng Read; --find KEY "chuỗi"). Chữ đã tách theo khối có đề mục: data/interim/text/<số_năm>.jsonl (nếu có).`
const DOCS = args
const ext = d => `Bạn là atom-extractor. ${CTX}
VIỆC: trích MỌI mẩu khuyến cáo có giá trị trong văn bản ${d.key} (${d.pages} trang, ${d.topic}) theo giao thức, vào data/interim/atoms_parts/${d.key.replace('/', '_')}.jsonl (tạo thư mục nếu cần; chỉ ghi file của văn bản này và file _coverage.md của nó). Đọc lần lượt từng trang chuyên môn.
Tự kiểm: ${SH} -m vnsoc.extract.atoms_merge --only ${d.key.replace('/', '_')} --out ${SCR}/${d.key.replace('/', '_')}.jsonl → 0 mẩu bị LOẠI.
Trả về: số mẩu theo slot_type và value_kind, số trang đã đọc, các trường hợp khó (ghi rõ trang), thời gian ước tính mỗi trang.`
const aud = (d, e) => `Bạn là KIỂM TOÁN VIÊN ĐỘC LẬP (integrity-auditor, AI — không phải người) cho bước trích mẩu văn bản ${d.key} (${d.topic}). ${CTX}
Người trích báo: ${JSON.stringify(e).slice(0, 1200)}
KIỂM (không sửa file của người trích; ghi kết quả vào review/extraction_calibration/${d.key.replace('/', '_')}.md và .json):
1. ĐỘ CHÍNH XÁC: với MỖI mẩu trong data/interim/atoms_parts/${d.key.replace('/', '_')}.jsonl: (a) span nguyên văn trên đúng trang; (b) giá trị/đơn vị đúng; (c) quần thể/bối cảnh đúng và đủ (có thuộc tính nào quyết định đáp án bị thiếu không?); (d) có đúng là khuyến cáo (không phải mô tả/ví dụ) và slot_type/value_kind hợp lý; (e) tập vn có thiếu giá trị khác cùng quần thể trong CÙNG văn bản không. Phán quyết ok / fix (sửa không đổi giá trị) / error.
2. ĐỘ PHỦ (bỏ sót): chọn NGẪU NHIÊN 5 trang chuyên môn (ghi rõ trang đã chọn và cách chọn — ví dụ dùng số trang chẵn/lẻ theo thứ tự cố định), tự đọc và liệt kê mọi mẩu thỏa giao thức mục 1 trên các trang đó; so với file của người trích → số mẩu bỏ sót / tổng.
3. Góp ý sửa giao thức (configs/extraction_protocol.md) nếu thấy quy tắc mơ hồ gây lỗi.
Trả về: số mẩu ok/fix/error, tỉ lệ bỏ sót trên trang mẫu, các lỗi hệ thống, đề xuất sửa giao thức.`
const SCH = { type: 'object', properties: { n: { type: 'integer' }, ok: { type: 'integer' }, fix: { type: 'integer' }, error: { type: 'integer' }, missed: { type: 'integer' }, sampled: { type: 'integer' }, issues: { type: 'array', items: { type: 'string' } }, summary: { type: 'string' } }, required: ['summary'] }
const out = await pipeline(DOCS,
  d => agent(ext(d), { label: `extract:${d.key}`, phase: 'Extract', schema: SCH, agentType: 'atom-extractor' }),
  (e, d) => agent(aud(d, e), { label: `audit:${d.key}`, phase: 'Audit', schema: SCH, agentType: 'integrity-auditor' }).then(a => ({ doc: d.key, e, a })),
)
return out
