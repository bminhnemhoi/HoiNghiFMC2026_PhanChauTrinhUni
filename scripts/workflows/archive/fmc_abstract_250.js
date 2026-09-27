export const meta = {
  name: 'fmc-abstract-250',
  description: 'Rewrite the FMC 2026 abstract (VI + EN) to the conference template at ~250 words: 3 drafts, 2 judges, synthesis, 3 adversarial verifiers',
  phases: [
    { title: 'Draft', detail: '3 drafters, different angles, registry placeholders only' },
    { title: 'Judge', detail: '2 independent judges score all drafts' },
    { title: 'Synthesize', detail: 'merge winner + grafts into final.md' },
    { title: 'Verify', detail: 'facts/honesty, Vietnamese+template, English+equivalence' },
  ],
}

const A = args
const ROOT = A.root
const SP = A.scratch
const CHECK = `cd "${A.root_bash}" && PYTHONUTF8=1 .venv/bin/python "${A.scratch_bash}/abs_check.py" <draft.md>`

const CONTEXT = `
CONTEXT — FMC 2026 abstract (Hội nghị Khoa học FMC 2026, Trường Đại học Phan Châu Trinh; topic "AI và Chuyển đổi số trong Y tế và Giáo dục Y khoa"; audience = Vietnamese clinicians, medical lecturers and medical students, not computer scientists).
Project root: ${ROOT}. Scratch folder: ${SP} (bash: ${A.scratch_bash}).
Read these first:
 - ${SP}/current.md — the CURRENT abstract source (VI + EN, ~440/396 words — far too long). Same markdown format you must produce.
 - ${SP}/pilot_keys.txt — every registry key you may use (key | rendered value | note explaining what it counts). Read the notes: use each key only for what it measures.
 - ${ROOT}/results/pilot/pilot_summary.md — pilot results summary (for understanding; do not copy numbers by hand).
 - ${ROOT}/review/M1/summary.md — criticism of the earlier abstract by the (AI) review panel.
 - The conference template (text): Title upper-case 13 pt; full author names; sections ĐẶT VẤN ĐỀ, MỤC TIÊU, PHƯƠNG PHÁP NGHIÊN CỨU, KẾT QUẢ, KẾT LUẬN, TỪ KHÓA; "Bảng tóm tắt không nên vượt quá 250 từ"; 3–5 lower-case keywords separated by ";"; note at the end whether published; Oral/Poster. Organisers: ONE language per file (VI file and EN file separately); 500 words is the hard limit, 250 recommended — we now target the recommended 250.

HARD RULES (breaking any = draft rejected):
 1. NO hand-written numbers anywhere in prose: every number comes from a registry placeholder {{pilot.key}} (Vietnamese) or {{pilot.key|en}} (English decimal point) — keys only from pilot_keys.txt. Words like "ba điều kiện"/"three conditions", "hai lượt"/"two passes" are fine as words. Model name "Qwen3-8B" is allowed. Do NOT invent any number, citation, or fact not supported by the pilot files.
 2. Honesty (project rules): it is a PILOT on a HAND-PICKED sample; quotation checks and label checks were done by AI (Claude) passes with an AI referee — NOT by humans; there was NO clinician review. Say this plainly (e.g. "kiểm bằng AI, chưa có bác sĩ duyệt"). Never imply a physician or expert reviewed anything. One small open model (Qwen3-8B, quantized, run locally on a laptop).
 3. Do not overclaim: the pilot did NOT find foreign-guideline defaults above the chance (decoy) level; most errors matched no recorded source; the passage condition improved correct answers but the paired test was not significant (report p from the key, do not call it significant). No causal or general claims about "LLMs" from one small model.
 4. Explain any project jargon in plain words the first time (e.g. decoy = "giá trị mồi — giá trị giả sinh theo quy tắc để ước lượng mức trùng ngẫu nhiên" / "rule-generated decoy value to estimate chance matches"; "conflict recommendations" = recommendations whose MoH value differs from at least one named foreign guideline). Prefer plain wording over internal labels.
 5. Keep the TITLE exactly as in current.md (VI and EN) — it matches the registered study. Keep GHI CHÚ / NOTE sections as they are. Rewrite "## Ô TÓM TẮT" (VI) and "## ABSTRACT BOX" (EN) web-form boxes too: ≤ 500 characters each (hard, browser maxlength), consistent with the new abstract.
 6. LENGTH TARGET: for EACH language, the five sections (ĐẶT VẤN ĐỀ..KẾT LUẬN / BACKGROUND..CONCLUSION) together ≤ 250 words INCLUDING the section headings ("BODY TOTAL ... with headings" line of the checker). Vietnamese words are counted as whitespace-separated syllables, like MS Word does. Keywords are not counted but must be 3–5, lower-case, ";"-separated.
 7. Same facts in VI and EN (a reader of either file learns the same things). EN section headings: BACKGROUND, OBJECTIVE, METHODS, RESULTS, CONCLUSION, KEYWORDS (keep the exact markdown heading structure of current.md: "## VI" with "### TIÊU ĐỀ", "### ĐẶT VẤN ĐỀ", "### MỤC TIÊU", "### PHƯƠNG PHÁP NGHIÊN CỨU", "### KẾT QUẢ", "### KẾT LUẬN", "### TỪ KHÓA"; "## EN" with "### TITLE" ... "### KEYWORDS").
 8. Must still contain (compressed): sample (recommendations quoted verbatim from official MoH PDFs; how many analysed, from how many in-force documents); reference values (named foreign guideline values WHO/US/Europe, superseded MoH values, decoys); model + languages + the three prompt conditions (no country cue / "according to the MoH" / with the MoH passage); pre-specified rule-based grading with AI double-check (and its agreement if space allows); the main result under the MoH cue in Vietnamese on conflict recommendations (correct n/N with % and CI; how many matched a foreign value vs no recorded source); foreign vs decoy matches; superseded-value matches; effect of supplying the passage; limitations; what the main study will do.

TOOL: validate every draft with:  ${CHECK}
It prints missing keys, hand-written digits, words per section, BODY TOTAL (with headings), box characters, fmc.checks, and the rendered text. Iterate until: MISSING KEYS none, HAND-WRITTEN DIGITS none, fmc.checks OK, BODY TOTAL with headings ≤ 250 for VI and for EN, boxes ≤ 500.
Write only inside ${SP}. Do not modify any project file.
`

const ANGLES = [
  { id: 'A', name: 'clinician-clarity', brief: 'Write for a busy Vietnamese clinician/medical lecturer: plain, concrete, why it matters for practice and teaching; minimal technical vocabulary; every number immediately interpretable (n/N).' },
  { id: 'B', name: 'methods-rigor', brief: 'Write for a strict scientific reviewer: precise design, denominators, CI, pre-specification, chance-level control, explicit limitations; no ambiguity about what was measured.' },
  { id: 'C', name: 'message-first', brief: 'Write for impact within honesty: one clear message per section, strongest defensible finding first, tight sentences, memorable but never overclaiming; conference-talk quality.' },
]

const DRAFT_SCHEMA = { type: 'object', properties: {
  path: { type: 'string' }, vi_words_with_headings: { type: 'number' }, en_words_with_headings: { type: 'number' },
  box_vi_chars: { type: 'number' }, box_en_chars: { type: 'number' }, choices: { type: 'string' } },
  required: ['path', 'vi_words_with_headings', 'en_words_with_headings', 'choices'] }

phase('Draft')
const drafts = (await parallel(ANGLES.map(g => () => agent(
  `You are drafting a new version of a conference abstract (Vietnamese AND English).\n${CONTEXT}\nYOUR ANGLE (${g.name}): ${g.brief}\n\nWrite your full draft (whole file in the same format as current.md, including a short "# ..." first line, "## Ô TÓM TẮT", "## VI", "## EN", "## GHI CHÚ", "## NOTE", "## ABSTRACT BOX") to ${SP}/draft_${g.id}.md, validate with the checker, iterate until all limits pass. Vietnamese must read as natural, professional Vietnamese medical-scientific prose (not a translation of English); English must be natural academic English. Return the path, the checker's word counts (with headings) and 2–4 sentences on your key choices (what you cut and why).`,
  { label: `draft:${g.id}-${g.name}`, phase: 'Draft', schema: DRAFT_SCHEMA })))).filter(Boolean)

log(`drafts: ${drafts.map(d => `${d.path.split(/[\\/]/).pop()} VI ${d.vi_words_with_headings} / EN ${d.en_words_with_headings}`).join('; ')}`)

const SCORE_SCHEMA = { type: 'object', properties: {
  scores: { type: 'array', items: { type: 'object', properties: {
    draft: { type: 'string' }, accuracy: { type: 'number' }, clarity: { type: 'number' }, structure: { type: 'number' },
    concision: { type: 'number' }, language_vi: { type: 'number' }, language_en: { type: 'number' }, equivalence: { type: 'number' },
    total: { type: 'number' }, problems: { type: 'array', items: { type: 'string' } }, best_parts: { type: 'array', items: { type: 'string' } } },
    required: ['draft', 'accuracy', 'clarity', 'structure', 'concision', 'language_vi', 'language_en', 'equivalence', 'total', 'problems', 'best_parts'] } },
  winner: { type: 'string' }, graft_instructions: { type: 'string' } }, required: ['scores', 'winner', 'graft_instructions'] }

const JUDGES = [
  { id: 'clinical-reader', lens: 'You judge as the scientific committee of a Vietnamese medical conference (you are an AI playing this role, not a physician): Is the problem clinically meaningful and clearly posed? Would a Vietnamese doctor/lecturer understand every sentence on first read? Is the Vietnamese natural and in correct medical register? Are claims appropriately cautious?' },
  { id: 'methods-accuracy', lens: 'You judge as a methods/statistics reviewer: check every placeholder is used for exactly what its note in pilot_keys.txt says (wrong key = serious error), denominators are right, no overclaim, limitations explicit, VI and EN state the same facts, template sections each do their job.' },
]
phase('Judge')
const judgements = (await parallel(JUDGES.map(j => () => agent(
  `${CONTEXT}\nThree candidate drafts: ${drafts.map(d => d.path).join(', ')}. Render each with the checker to see real numbers and counts.\nLENS: ${j.lens}\nScore each draft 1–10 on: accuracy (faithful to pilot results & key notes, honesty rules), clarity (for the conference audience), structure (template sections each doing their job), concision (≤250 words incl. headings each language), language_vi, language_en, equivalence (VI/EN same facts). total = sum. List concrete problems (quote the text) and the best parts worth grafting. Pick a winner and write precise graft instructions for a synthesizer (which sentences to take from which draft, what to fix).`,
  { label: `judge:${j.id}`, phase: 'Judge', schema: SCORE_SCHEMA })))).filter(Boolean)

const SYN_SCHEMA = { type: 'object', properties: {
  path: { type: 'string' }, vi_words_with_headings: { type: 'number' }, en_words_with_headings: { type: 'number' },
  box_vi_chars: { type: 'number' }, box_en_chars: { type: 'number' }, changes: { type: 'string' } },
  required: ['path', 'vi_words_with_headings', 'en_words_with_headings', 'changes'] }

phase('Synthesize')
const final = await agent(
  `${CONTEXT}\nDrafts: ${drafts.map(d => d.path).join(', ')}.\nTwo independent judgements (JSON):\n${JSON.stringify(judgements, null, 1)}\n\nProduce the single best final version at ${SP}/final.md: start from the winner(s), graft the best parts, fix every problem the judges listed (quote-level). Vietnamese must be natural professional Vietnamese medical prose; English natural academic English; same facts in both. Validate with the checker until all limits pass (≤ 250 words incl. headings per language, no missing keys, no hand-written digits, boxes ≤ 500 chars). Return path, counts, and a summary of what you took from where and what you fixed.`,
  { label: 'synthesize', phase: 'Synthesize', schema: SYN_SCHEMA })

const ISSUE_SCHEMA = { type: 'object', properties: {
  verdict: { type: 'string', enum: ['pass', 'pass_with_fixes', 'fail'] },
  issues: { type: 'array', items: { type: 'object', properties: {
    severity: { type: 'string', enum: ['critical', 'major', 'minor'] }, lang: { type: 'string', enum: ['vi', 'en', 'both', 'box'] },
    quote: { type: 'string' }, problem: { type: 'string' }, fix: { type: 'string' } },
    required: ['severity', 'lang', 'quote', 'problem', 'fix'] } } }, required: ['verdict', 'issues'] }

const VERIFIERS = [
  { id: 'facts-honesty', task: `ADVERSARIAL FACT & HONESTY CHECK. For every sentence of the VI and EN abstract and both boxes: (a) each placeholder key is used for exactly what its note in pilot_keys.txt measures (open ${ROOT}/results/numbers.json for the full note/source if needed, and cross-check against ${ROOT}/results/pilot/pilot_summary.md); (b) every factual statement without a number is supported by the pilot files or current.md (e.g. which checks were AI, how many conditions, languages, what the reference values are); (c) no overclaim: foreign defaults not above decoy level, p not significant, one small model, hand-picked sample; (d) limitations explicitly present in BOTH languages: hand-picked sample, AI checks (not humans), no clinician review; (e) no statement implies physician/expert review. Assume there ARE errors and hunt for them; report each with the exact quote and a concrete fix. Do not report style preferences.` },
  { id: 'vietnamese-template', task: `VIETNAMESE LANGUAGE + TEMPLATE CHECK (VI file content and the "Ô TÓM TẮT" box). Check: natural, grammatical Vietnamese scientific-medical prose (không "văn dịch"), correct terminology (khuyến cáo, hướng dẫn chẩn đoán và điều trị, Bộ Y tế, khoảng tin cậy/KTC, mô hình ngôn ngữ lớn), consistent terms throughout, correct decimal comma in rendered numbers, no unexplained jargon, each template section does its job (Đặt vấn đề = vấn đề + khoảng trống; Mục tiêu = một mục tiêu rõ; Phương pháp = thiết kế, mẫu, giá trị đối chiếu, mô hình, điều kiện, cách chấm; Kết quả = số chính có mẫu số; Kết luận = trả lời mục tiêu + giới hạn + hướng tiếp), keywords 3–5 lower-case ";"-separated and useful, length ≤ 250 incl. headings. Report exact quotes with concrete rewrites that do NOT add words beyond the limit.` },
  { id: 'english-equivalence', task: `ENGLISH LANGUAGE + VI/EN EQUIVALENCE CHECK (EN file content and the ABSTRACT BOX). Check: natural academic English (JMIR-style), correct statistics wording (95% CI, p value), consistent terminology, English decimal point in rendered numbers (keys used with |en where a decimal appears), each section does its job, keywords 3–5 lower-case. Then compare VI vs EN sentence by sentence: every fact/number present in one must be present in the other with the same meaning (list any mismatch). Length ≤ 250 incl. headings. Report exact quotes with concrete fixes.` },
]
phase('Verify')
const verdicts = (await parallel(VERIFIERS.map(v => () => agent(
  `${CONTEXT}\nThe FINAL candidate is ${final ? final.path : SP + '/final.md'} — render it with the checker first.\n${v.task}`,
  { label: `verify:${v.id}`, phase: 'Verify', schema: ISSUE_SCHEMA }).then(r => r && ({ verifier: v.id, ...r }))))).filter(Boolean)

return { drafts, judgements, final, verdicts }
