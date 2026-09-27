export const meta = {
  name: 'foreign-store',
  description: 'T2.6 versioned foreign reference store: per disease group, find and cache official WHO/WPRO/US/EU_UK guidelines (current + previous), record values with locators, then independent verification',
  phases: [
    { title: 'Collect', detail: 'one counterpart-matcher per disease group' },
    { title: 'Verify', detail: 'independent check of recorded values against cached sources' },
  ],
}
const SH = 'cd "/d/phan chau trinh _ y khoa" && PYTHONUTF8=1 .venv/bin/python'
const CTX = `Dự án vn-soc-audit (Git Bash /d/phan chau trinh _ y khoa). Python: ${SH} ... . CLAUDE.md áp dụng nghiêm:
- KHÔNG lưu đoạn văn của hướng dẫn nước ngoài (chỉ giá trị + nguồn + vị trí; mọi trường chữ ≤ 200 ký tự);
- không bịa giá trị, năm, URL; giá trị phải có trong trang/PDF đã mở và băm;
- chỉ nguồn chính thức (who.int, iris.who.int, cdc.gov, nice.org.uk, escardio.org, idsa, aasld, diabetesjournals.org, ahajournals.org, bản PMC/nhà xuất bản chính thức…);
- không tắt kiểm TLS; không đọc data/runs/; không commit; không sửa src/, configs/, data/raw, manifest, pilot_atoms.
Công cụ: ${SH} -m vnsoc.match.sources fetch <url> (tải + băm vào data/cache/foreign, in sha256) và ${SH} -m vnsoc.match.sources grep <sha> "<chuỗi>" (tìm trong bản đệm). Schema: src/vnsoc/schemas.py ForeignRecord (record_id, disease, topic, system US|EU_UK|WHO_global|WHO_WPRO|OTHER, source, version_date, url, locator, fetched_at, page_sha256, values: ValueItem như mẩu Bộ Y tế — num {lo,hi,unit,cmp}, bp {sys,dia,cmp}, schedule {seq,unit}, drugs {key_drugs: INN chữ thường có trong configs/grading.yaml}, cat {label}; first_version_date nếu xác minh được ấn bản ĐẦU TIÊN chứa giá trị; population_match full|partial; note ≤ 200 ký tự). Đọc .claude/skills/counterpart-matching/SKILL.md.
Mẩu Bộ Y tế đã trích (đang trích tiếp, CHỈ ĐỌC): data/interim/atoms_parts/<số_năm>*.jsonl — dùng để biết các slot (liều, ngưỡng, thời gian, thuốc đầu tay, đích…) cần đối chiếu; mẩu thí điểm: data/interim/pilot_atoms.jsonl (nhiều giá trị nước ngoài đã có ở trường foreign — có thể dùng lại sau khi kiểm lại nguồn).`
const collectP = g => `Bạn là counterpart-matcher cho nhóm bệnh "${g.id}": ${g.desc}. Văn bản Bộ Y tế trong kho: ${g.docs.join(', ')}. ${CTX}
VIỆC:
1. SỔ NGUỒN: xác định các hướng dẫn nước ngoài tương ứng — WHO toàn cầu HIỆN HÀNH + ấn bản TRƯỚC, WHO WPRO (nếu có), Mỹ (CDC/hội chuyên ngành), châu Âu/Anh (NICE/ESC/ERS/EASL…). Với mỗi nguồn: tên, năm/ngày phiên bản, URL chính thức, đã tải được chưa (sha256) hay bị chặn/trả phí (ghi rõ). Ghi data/interim/foreign_sources/${g.id}.jsonl (một dòng mỗi nguồn: {system, source, version_date, url, page_sha256|null, status: fetched|blocked|paywalled|not_found, note}).
2. BẢN GHI GIÁ TRỊ: với các khuyến cáo có giá trị cụ thể (liều, ngưỡng, thời gian, lịch, thuốc đầu tay, đích) TƯƠNG ỨNG với các slot của mẩu Bộ Y tế trong nhóm (ưu tiên slot chính của mỗi văn bản; mục tiêu ≥ 40 bản ghi cho nhóm lớn, ≥ 15 cho nhóm nhỏ), ghi ForeignRecord vào data/interim/foreign_parts/${g.id}.jsonl, record_id "F-${g.id}-NNN", topic = slot + quần thể (khớp cách mẩu Bộ Y tế mô tả), locator = mục/bảng/trang (KHÔNG chép câu). Quần thể khác một phần (bối cảnh, tuyến) → population_match "partial" + note. first_version_date chỉ khi đã mở ấn bản cũ hơn và thấy cùng giá trị.
3. TỰ KIỂM: ${SH} -m vnsoc.match.foreign_store (gộp mọi phần) → mọi bản ghi của nhóm phải được GIỮ (không LOẠI); nếu bị loại vì "không thấy [...] trong nguồn đã băm" thì sửa giá trị/nguồn hoặc bỏ bản ghi.
Chỉ ghi 2 file của nhóm. Trả về: số nguồn (fetched/blocked), số bản ghi theo system, nguồn bị chặn cần người dùng, khó khăn.`
const verifyP = (g, c) => `Bạn là KIỂM TOÁN VIÊN ĐỘC LẬP (integrity-auditor, AI) cho kho giá trị nước ngoài nhóm "${g.id}" (${g.desc}). ${CTX}
Người thu thập báo: ${JSON.stringify(c).slice(0, 1200)}
KIỂM (không sửa file của người thu thập; ghi review/foreign_audit/${g.id}.md và .json): chọn ngẫu nhiên có hạt giống cố định min(25, tổng) bản ghi trong data/interim/foreign_parts/${g.id}.jsonl; với mỗi bản ghi: mở bản đệm theo page_sha256 (grep) và/hoặc URL, tới locator: (a) giá trị và đơn vị đúng; (b) quần thể/bối cảnh đúng như topic; (c) phiên bản/năm đúng, có ấn bản mới hơn thay thế không; (d) system gán đúng (US/EU_UK/WHO…); (e) không có đoạn văn nguồn bị chép. Phán quyết ok/fix/error + đề xuất sửa. Kiểm thêm sổ nguồn: có thiếu hướng dẫn chủ chốt nào (ví dụ WHO hiện hành) không.
Trả về: sampled, ok, fix, error, thiếu nguồn chủ chốt, lỗi hệ thống.`
const SCH = { type: 'object', properties: { n: { type: 'integer' }, sampled: { type: 'integer' }, ok: { type: 'integer' }, fix: { type: 'integer' }, error: { type: 'integer' }, issues: { type: 'array', items: { type: 'string' } }, summary: { type: 'string' } }, required: ['summary'] }
// args = logs/wf/foreign_args.json từ scripts/workflows/resume_args.py: mỗi nhóm {id, desc, docs, collected}.
// Nhóm đã thu thập (collected) chỉ qua bước kiểm độc lập.
const out = await pipeline(args,
  g => g.collected
    ? Promise.resolve({ summary: `Nhóm ${g.id} đã thu thập ở phiên trước: data/interim/foreign_parts/${g.id}.jsonl và data/interim/foreign_sources/${g.id}.jsonl.` })
    : agent(collectP(g), { label: `collect:${g.id}`, phase: 'Collect', schema: SCH, agentType: 'counterpart-matcher' }),
  (c, g) => agent(verifyP(g, c), { label: `verify:${g.id}`, phase: 'Verify', schema: SCH, agentType: 'integrity-auditor' }).then(v => ({ group: g.id, c, v })),
)
return out.map(o => o && ({ group: o.group, n: o.c && o.c.n, collect: o.c && o.c.summary && o.c.summary.slice(0, 600), verify: o.v && { sampled: o.v.sampled, ok: o.v.ok, fix: o.v.fix, error: o.v.error, issues: (o.v.issues || []).slice(0, 6) } }))
