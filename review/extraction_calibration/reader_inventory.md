# Kiểm kê bộ đọc thuốc/đơn vị trên toàn kho — grader 1.3.1

- Ngày: 27/9/2026. Người làm: agent chấm (AI), theo `skills/grading-protocol` và `skills/vn-number-normalization`.
- Lý do: hiệu chỉnh trích mẩu 4 văn bản (`review/extraction_calibration/{1019_2025,1840_2025,1857_2022,2892_2022}.md`,
  `data/interim/atoms_parts/*_coverage.md`) cho thấy 20–35% khuyến cáo bị bỏ vì bộ đọc số/thuốc (`src/vnsoc/normalize_vi.py`,
  `configs/grading.yaml`, `configs/drug_display.yaml`) không đọc được giá trị, nên người trích không làm cho giá trị kiểm
  được. Sửa MỘT lần cho cả kho trước khi trích toàn bộ.
- Mù với đầu ra mô hình: không mở `data/runs/`; mọi câu thử là câu tự viết theo cách viết của kho. Bộ chấm thí điểm vẫn khóa
  ở 1.2.0 (`vnsoc.analysis.pilot` không chạy).
- Kết quả: `grader_version` 1.3.0 → **1.3.1** (`configs/grading.yaml`, changelog ở đầu tệp). Cần một mục `docs/DECISIONS.md`
  (chưa viết — việc của người điều phối).

## 1. Phương pháp

1. Lớp chữ của 25 văn bản `in_corpus=true` (`data/interim/manifest.jsonl`), đọc bằng `vnsoc.extract.verify_span.page_texts`
   (tự áp tệp OCR kèm: 1470/2024, 2855/2024, 292/2024, 3377/2023, 6101/2019, TT51/2017 là OCR). 1.829 trang, 3,15 triệu ký tự.
2. Thuốc: (a) quét token theo gốc INN (-cillin, cef-, -mycin, -floxacin, -azol, -pril, -sartan, -olol, -dipin, -statin,
   -gliflozin, -gliptin, -glutid, -vir…), (b) mọi từ không phải âm tiết tiếng Việt, (c) 1–3 từ đứng ngay trước một liều
   ("Paracetamol 10-15 mg/kg"). Danh sách ứng viên được lọc tay; mỗi thuốc giữ lại được đếm trên kho (số lần, số văn bản,
   số lần trong ngữ cảnh khuyến cáo = cùng câu có liều hoặc động từ dùng/chỉ định/khuyến cáo/phối hợp/uống/tiêm/truyền).
   Bí danh tiếng Việt lấy từ kho (bỏ -e cuối, -cilin, typo có thật trong kho) và kiểm va chạm với âm tiết tiếng Việt bỏ dấu
   (`đặc`→`dac`, `kẽm`→`kem`, `nấc`→`nac` không được làm bí danh).
3. Đơn vị: quét "số + cụm đơn vị" (1.597 cách viết khác nhau), đọc từng cách viết bằng `parse_nums` trước và sau sửa.
4. Thử: `vnsoc.normalize_vi.parse_nums/parse_drugs`, `vnsoc.grade.parse_values/grade_short`,
   `vnsoc.extract.verify_span.missing_vn_values`. Tệp máy đọc trung gian ở scratchpad phiên (không đưa vào repo).

## 2. Kết quả tổng

| Chỉ số | 1.3.0 | 1.3.1 |
|---|---|---|
| Khóa thuốc trong `drugs` | 81 | 509 (+418 INN đơn, +9 phác đồ có tên, +1 lớp) |
| Bí danh thuốc | 143 | 1.113 (+947 trên khóa mới, +23 trên khóa cũ) |
| Tổ hợp cố định `combos` | 9 | 17 |
| Tên hiển thị `drug_display.yaml` | 67 | 485 |
| Cách viết đơn vị (`UNIT_ALIASES`) | 135 | 547 |
| Đơn vị chuẩn | 42 | 138 |
| Cạnh quy đổi cố định | 10 | 52 (+ cạnh theo `context`: analyte, valence, weight_kg, doses_per_day, mg_per_tablet) |
| Câu của kho có ≥ 1 tên thuốc đọc được | 1.351 / 42.001 | 4.150 / 42.001 |
| Cụm "số + đơn vị" đọc khác đi (đúng đơn vị) | — | 187 cách viết, 1.462 lần xuất hiện |

Câu có tên thuốc đọc được, theo văn bản (tổng câu | 1.3.0 | 1.3.1):

| Văn bản | Câu | 1.3.0 | 1.3.1 |
|---|---|---|---|
| 1019/2025 | 574 | 7 | 52 |
| 1154/2024 | 835 | 0 | 73 |
| 1470/2024 | 711 | 0 | 48 |
| 162/2024 | 4537 | 510 | 573 |
| 1740/2026 | 914 | 50 | 63 |
| 1840/2025 | 226 | 0 | 8 |
| 1857/2022 | 594 | 1 | 58 |
| 2131/2026 | 2921 | 63 | 223 |
| 2147/2026 | 2390 | 102 | 208 |
| 2388/2024 | 4845 | 27 | 325 |
| 2760/2023 | 2483 | 5 | 148 |
| 2855/2024 | 512 | 33 | 96 |
| 2892/2022 | 670 | 1 | 30 |
| 292/2024 | 664 | 1 | 50 |
| 3192/2010 | 220 | 0 | 8 |
| 3312/2024 | 3362 | 20 | 143 |
| 3377/2023 | 539 | 110 | 112 |
| 3610/2015 | 5499 | 18 | 650 |
| 5481/2020 | 1917 | 0 | 416 |
| 5642/2015 | 2188 | 59 | 220 |
| 5904/2019 | 1442 | 1 | 102 |
| 5968/2021 | 2951 | 286 | 428 |
| 6101/2019 | 153 | 5 | 11 |
| 678/2025 | 453 | 14 | 41 |
| TT51/2017 | 401 | 38 | 64 |

## 3. Thuốc đã thêm (`configs/grading.yaml` › `drugs`)

Tên là tên hiển thị tiếng Việt (`drug_display.yaml`, cách viết nhiều nhất trong kho; không dùng tên biệt dược, viết tắt,
lỗi chính tả). Ngoặc: (số câu có thuốc / số văn bản); "—" = không có trong kho (thuốc cùng nhóm, thêm để câu trả lời nêu
chúng là một giá trị — nhãn 5 — thay vì từ chối — tiền lệ 1.3.0 E5 — hoặc dạng kho không đọc được, xem §7).

- **Kháng khuẩn** — 73: amoxicillin (45/9), acid clavulanic (30/8), amoxicillin-acid clavulanic (26/8), ampicillin (27/5),
  sulbactam (10/3), ampicillin-sulbactam (7/3), penicillin G (34/7), benzathine penicillin (12/2), procaine penicillin (9/2),
  penicillin V (1/1), oxacilin (8/3), cloxacillin (5/3), dicloxacillin (1/1), nafcillin (1/1), piperacillin (21/4),
  tazobactam (22/4), piperacillin-tazobactam (17/4), cephalexin (5/3), cefazolin (7/2), cefuroxim (8/5), cefaclor (1/1),
  cefprozil (1/1), cefoxitin (4/1), cefotaxim (28/5), ceftriaxon (54/7), cefepim (19/4), cefixim (6/3), cefpodoxim (8/3),
  cefdinir (7/2), cefditoren (5/1), cefoperazon (2/1), cefoperazon-sulbactam (—), ceftarolin (10/1), ceftolozan (1/1),
  ceftolozan-tazobactam (1/1), avibactam (1/1), ceftazidim-avibactam (1/1), cefpirom (1/1), imipenem (+ cilastatin; 30/7),
  ertapenem (9/3), doripenem (4/2), aztreonam (2/1), gentamicin (12/5), tobramycin (12/5), netilmicin (4/1),
  capreomycin (7/1), clarithromycin (95/6), erythromycin (42/7), roxithromycin (4/2), spiramycin (2/2), tetracyclin (6/3),
  minocycline (5/3), tigecycline (4/2), ciprofloxacin (52/7), ofloxacin (9/5), norfloxacin (1/1), pefloxacin (2/1),
  gatifloxacin (3/1), acid nalidixic (1/1), vancomycin (40/5), teicoplanin (11/3), daptomycin (6/1), colistin (10/6),
  polymyxin B (—), fosfomycin (1/1), nitrofurantoin (—), metronidazol (23/7), tinidazole (1/1), trimethoprim (41/7),
  sulfamethoxazole (42/7), sulfadiazine (6/1), terizidone (3/1), acid para-aminosalicylic (PAS) (8/1).
- **Kháng vi rút** — 26: oseltamivir (15/4), zanamivir (7/3), baloxavir (3/1), peramivir (1/1), acyclovir (31/3),
  valaciclovir (8/1), famciclovir (6/1), ganciclovir (6/1), valganciclovir (4/1), ribavirin (31/2), sofosbuvir (55/3),
  velpatasvir (35/3), daclatasvir (20/3), ledipasvir (22/3), glecaprevir (4/1), pibrentasvir (5/1), voxilaprevir (10/1),
  elbasvir (7/2), grazoprevir (8/2), interferon alfa (2/2), peginterferon alfa (14/2), stavudine (2/1), etravirin (3/1),
  elvitegravir (1/1), tipranavir (4/1), saquinavir (7/2).
- **Kháng nấm, ký sinh trùng** — 16: fluconazole (22/4), itraconazole (13/4), voriconazole (5/3), posaconazol (2/2),
  ketoconazole (5/4), amphotericin B (12/2), flucytosine (4/1), nystatin (1/1), clotrimazole (4/1), miconazole (2/1),
  albendazol (4/1), mebendazol (1/1), praziquantel (1/1), ivermectin (2/2), pyrimethamine (10/1), acid folinic (7/2).
- **Tim mạch, chống đông, đảo ngược chống đông** — 103: sacubitril (15/2), valsartan (17/4), sacubitril/valsartan (15/2),
  losartan, irbesartan, candesartan, telmisartan, olmesartan, captopril, enalapril, lisinopril, perindopril, ramipril,
  imidapril, benazepril, quinapril, trandolapril, bisoprolol, carvedilol, metoprolol, nebivolol, atenolol (9/5),
  propranolol (9/7), labetalol (10/4), esmolol, acebutolol, nadolol, sotalol, amlodipine, nifedipine (14/5), felodipin,
  lercanidipin, lacidipine, nicardipine (12/3), nimodipine (6/1), diltiazem, verapamil, methyldopa (12/4), clonidine,
  hydralazine (7/4), urapidil, natri nitroprussid (8/5), isosorbid dinitrat (5/1), isosorbid mononitrat (—),
  nitroglycerin, furosemide (34/7), bumetanide, torsemide, spironolactone, eplerenon (—), hydrochlorothiazide, indapamide,
  chlorthalidone, acetazolamide, tolvaptan (7/4), dapagliflozin (25/3), empagliflozin (23/3), canagliflozin (5/3),
  ertugliflozin (—), digoxin (28/6), ivabradin, milrinone, levosimendan (—), vasopressin, noradrenalin (26/8),
  dopamin (31/10), dobutamin (29/7), amiodaron (10/4), lidocain (9/5), atropin (48/3), ranolazin, 7 statin (atorvastatin
  12/7 … pitavastatin 1/1), ezetimibe (16/3), fenofibrate, gemfibrozil (—), aspirin (62/11), clopidogrel (16/3),
  ticagrelor (9/4), prasugrel, cilostazol, dipyridamole, heparin (16/4), enoxaparin, nadroparin, fondaparinux (—),
  warfarin (23/5), acenocoumarol, dabigatran (10/2), rivaroxaban, apixaban, edoxaban, protamine (17/2), idarucizumab,
  andexanet alfa (—), phức hợp prothrombin cô đặc (PCC) (7/2), vitamin K1 (9/2), acid tranexamic.
- **Đái tháo đường, béo phì, tuyến giáp, gút** — 24: insulin (mọi loại insulin là MỘT thuốc; 377/8), metformin (71/6),
  gliclazide (20/3), glimepiride, glyburide/glibenclamid (7/2), glipizide, repaglinide, acarbose, pioglitazone (12/1),
  sitagliptin, vildagliptin, saxagliptin, linagliptin, alogliptin (—), liraglutide (21/3), dulaglutid (—),
  semaglutid (—), exenatid (—), orlistat (16/1), phentermine, levothyroxine, allopurinol, febuxostat, colchicin (15/4).
- **Hô hấp** — 23: salbutamol (45/5), terbutaline, fenoterol (12/3), ipratropium (21/4), tiotropium, umeclidinium,
  glycopyronium, aclidinium (—), indacaterol, olodaterol, vilanterol, formoterol (19/2), salmeterol (10/2),
  budesonide (31/5), fluticasone (21/3), beclomethasone, theophylline (13/3), aminophylline, doxofyllin (—), roflumilast,
  N-acetylcystein (12/3), carbocystein, montelukast.
- **Corticoid, giảm đau, gây mê, chống co giật, kháng histamin** — 31: prednisolon (31/10), prednisone, methylprednisolon
  (27/7), hydrocortison, dexamethasone (12/6), betamethasone, paracetamol (104/11), ibuprofen (16/5), diclofenac,
  morphin (19/5), fentanyl, tramadol, codein, ketamin, propofol, thiopental (16/3), diazepam (37/9), midazolam (17/5),
  lorazepam, clonazepam, phenobarbital (35/6), phenytoin (14/7), valproat, levetiracetam, carbamazepin (10/4),
  haloperidol (11/5), diphenhydramin (13/4), chlorpheniramine, promethazin, cetirizin, loratadin.
- **Tiêu hóa, bù nước, kẽm** — 12: omeprazole, esomeprazol, pantoprazol, ranitidin, famotidin, cimetidin, metoclopramid,
  domperidon, ondansetron, lactulose, oresol (ORS) (18/4), kẽm (gluconat/sulfat; 5/2).
- **Thận, thiếu máu, ức chế miễn dịch, globulin miễn dịch, albumin** — 30: sevelamer, calci carbonat (—), cinacalcet,
  calcitriol, alfacalcidol, natri/calci polystyren sulfonat, natri zirconium cyclosilicat (—), patiromer (—),
  erythropoietin (6/2), darbepoetin alfa (—), methoxy polyethylene glycol-epoetin beta, sắt sucrose, sắt sulfat/fumarat/
  gluconat, acid folic, cyclophosphamide (17/2), mycophenolat mofetil (13/1), acid mycophenolic (—), tacrolimus (12/2),
  cyclosporine (18/4), azathioprine, rituximab, hydroxychloroquin, immunoglobulin (IVIG) (37/6), HBIG (3/2), TIG (3/1),
  huyết thanh kháng độc tố uốn ván (SAT) (2/1), albumin người (6/2).
- **Dịch truyền, điện giải** — 11: natri clorid (140/14), Ringer lactat (46/5), mannitol (12/9), kali clorid, natri
  bicarbonat (17/5), calci gluconat, calci clorid, magie sulphat (44/3), HES (9/2), dextran, gelatin.
- **Giải độc, vitamin** — 27: than hoạt tính (79/2), sorbitol (25/2), pralidoxim (PAM) (10/1), naloxon (12/2),
  flumazenil (10/1), fomepizole, ethanol (36/3), xanh methylen (8/2), hydroxocobalamin (10/1), natri thiosulfat (15/1),
  natri nitrit, amyl nitrit (7/1), dimercaprol (BAL) (—), succimer (11/1), DMPS, CaNa2EDTA (10/1), penicillamin (8/2),
  glucagon (18/4), octreotide, neostigmin, pyridoxine (14/2), vitamin B1, silibinin, silymarin, huyết thanh kháng nọc rắn
  (95/1), nhũ dịch lipid (3/1), vitamin A (18/3).
- **Khác trong kho** — 29 + 13: vitamin D/C/B12, citicolin, cerebrolysin, piracetam, vinpocetin, memantine, donepezil,
  desmopressin, roxadustat, daprodustat, icodextrin, methotrexate, nicotin (liệu pháp thay thế), bupropion, analgin
  (metamizol), vecuronium, pipecuronium, everolimus, anakinra, quetiapine, gabapentin, pregabalin, duloxetin,
  amitriptyline, fluoxetin, tizanidin, baclofen; lần cuối (đứng trước một liều, 1–3 lần): indomethacin, naproxen,
  metolazone, amiloride, relebactam, lixisenatide, canakinumab, pancuronium, probenecid, bisacodyl, amobarbital,
  clorpromazin (aminazin), pethidin (dolargan).

Bí danh thêm vào khóa cũ (23): amikacine; streptomicin/streptomicine/steptomycin(e) (lỗi chính tả trong kho); `~km`;
`mpm`; `~ABC@2` (abacavir), `~RAL@2` (raltegravir); isoniazide; pyrazynamid; chloroquin(e) phosphat; co-trimoxazole
(cotrimoxazole, sulfamethoxazol(e)-trimethoprim, trimethoprim-sulfamethoxazol, smx-tmp, trimoxazol(e)); các lỗi chính tả
có trong kho (pimaquin → primaquine, doxycillin → doxycycline).

Phác đồ có tên (khóa "a+b", nở ra INN thành phần): Epclusa, Harvoni + `sof/led`, `sof/dac` (2855/2024 viết "SOF/DAC",
"SOF/LED"; "DAC" đứng riêng là chữ "đặc" bỏ dấu nên không làm bí danh), Mavyret/Maviret, Vosevi, Zepatier, Berodual,
Combivent, 3HP/1HP (isoniazid + rifapentine).

Tổ hợp cố định (`combos`, các thành phần gộp thành sản phẩm): amoxicillin-clavulanate, co-trimoxazole (SMX + TMP),
sacubitril-valsartan, piperacillin-tazobactam, ceftolozane-tazobactam, ampicillin-sulbactam, cefoperazone-sulbactam,
ceftazidime-avibactam. Mẩu ghi `key_drugs` bằng khóa tổ hợp (vd. `amoxicillin-clavulanate`), không bằng hai thành phần.
TDF/3TC/DTG, SOF/VEL… vẫn đọc từng INN (không gộp), như quy ước 1.1.0 cho TLD.

Lớp thuốc: CHỈ thêm LMWH (`enoxaparin|nadroparin`: "heparin trọng lượng phân tử thấp", "LMWH") vì trước đây cụm này bị
đọc thành heparin (không phân đoạn). Lớp thuốc khác không thêm (§7).

Mã chuỗi 3 chữ HOA (phân biệt hoa-thường, cần ≥ 2 thuốc khác trong cùng chuỗi): `~ABC@2` ("ABC + 3TC + DTG" = abacavir;
"Đánh giá ABC, adrenalin" không), `~RAL@2`, `~PAS@2`; mã lao `~km`, `~cm`. `tests/test_grade.py` cho phép dạng này.

Không phải thuốc (không đọc, có test): chất xét nghiệm trơn (kali, calci/canxi, magie, glucose, albumin, bicarbonate trơn,
sắt trơn, kẽm trơn), "glucagon-like peptide", "kháng insulin"/"tiết insulin"/"insulin resistance"
(`normalize_vi.NOT_DRUG_RE`), "interferon" trơn (IGRA "interferon gamma"), "BAL" (rửa phế quản phế nang), "triệu" trơn.

## 4. Thuốc hỗ trợ (`adjunct_drugs`, quy tắc mới trong `grade.regimen_drugs`)

Bảng lớn hơn làm các thuốc trước đây vô hình trở thành "thuốc thừa" (E4 1.3.0) → câu trả lời thành "phác đồ khác", nhãn 5.
Thử trên mẩu thí điểm (câu tự viết), TRƯỚC khi có quy tắc này: "TDF + 3TC + DTG + vitamin B6" 2 → 5; "…, kèm paracetamol nếu
sốt" 2 → 5; "TDF (bổ sung vitamin D, calci)" 2 → 5; "quinin + clindamycin + acid folic" 2 → 5; "BPaL + pyridoxine" 2 → 5;
"DHA-PPQ + primaquin + paracetamol" 3 → 5. Quy tắc 1.3.1: 31 thuốc hỗ trợ (paracetamol, vitamin A/B1/B6/B12/C/D, acid folic,
sắt uống, calci carbonat, kẽm, ORS, natri clorid, Ringer lactat, PPI, kháng H2, chống nôn, kháng histamin, lactulose) mà
KHÔNG là `key_drugs` của mục nào của mẩu được coi như thuốc nền — mọi câu trên giữ nhãn 1.3.0. Là key_drugs của một mục thì
tính như mọi thuốc (vitamin A trong sởi). KHÔNG có NSAID (ibuprofen chống chỉ định trong SXHD), kháng sinh (co-trimoxazole
dự phòng vẫn là phác đồ khác, như 1.3.0), thuốc đặc hiệu. Người điều phối có thể làm rỗng danh sách để về E4 chặt.

## 5. Đơn vị và số (`normalize_vi`)

Cụm "số + đơn vị" đọc khác đi (xuất hiện ≥ 3 lần; cột 3 = số văn bản; "—" = trước đây không đọc được đơn vị, số được hiểu
theo đơn vị của mẩu):

| Cách viết (chữ thường) | Lần | VB | 1.3.0 | 1.3.1 |
|---|---|---|---|---|
| `ml/phút/1,73m2` | 64 | 2 | ml | mL/min/1.73m2 |
| `mm` | 57 | 13 | — | mm |
| `ml/phút` | 55 | 9 | ml | ml/min |
| `g/ngày` | 55 | 9 | g | g/day |
| `viên/ngày` | 46 | 7 | tablet | tablet/day |
| `lần/phút` | 45 | 11 | times | /min |
| `ml/phút/1,73 m2` | 42 | 3 | ml | mL/min/1.73m2 |
| `ml/ph` | 41 | 5 | ml | ml/min |
| `g/l` | 39 | 8 | g | g/L |
| `giây` | 38 | 8 | — | s |
| `cmh2o` | 37 | 5 | — | cmH2O |
| `g/dl` | 36 | 9 | g | g/dL |
| `mg/l` | 34 | 8 | mg | mg/L |
| `nhát` | 30 | 3 | — | puff |
| `°` | 25 | 8 | — | ° |
| `mg/g` | 24 | 2 | mg | mg/g |
| `viên/ ngày` | 22 | 2 | tablet | tablet/day |
| `oc` | 22 | 3 | — | °C |
| `µmol/l` | 21 | 8 | — | umol/L |
| `độ` | 20 | 7 | — | ° |
| `pg/ml` | 18 | 3 | — | pg/mL |
| `ngày/ tuần` | 18 | 1 | day | days/week |
| `mg/giờ` | 18 | 5 | mg | mg/h |
| `mg/m2/24h` | 17 | 1 | mg | mg/m2/day |
| `ml/giờ` | 16 | 2 | ml | ml/h |
| `lít/phút` | 16 | 4 | l | L/min |
| `ml/ ngày` | 14 | 1 | ml | ml/day |
| `mg/kg/giờ` | 14 | 5 | mg/kg | mg/kg/h |
| `giọt` | 14 | 4 | — | drop |
| `ms` | 13 | 4 | — | ms |
| `µg/kg/phút` | 12 | 2 | ug/kg | ug/kg/min |
| `ngày/tuần` | 12 | 4 | day | days/week |
| `mg/mmol` | 12 | 1 | mg | mg/mmol |
| `mg/ ngày` | 12 | 5 | mg | mg/day |
| `log10` | 12 | 2 | — | log10 |
| `gói` | 12 | 3 | — | sachet |
| `ug/kg/phút` | 11 | 2 | ug/kg | ug/kg/min |
| `meq/l` | 11 | 4 | — | mEq/L |
| `lần/năm` | 11 | 4 | times | times/year |
| `thang` | 10 | 6 | — | month |
| `mg/phút` | 10 | 4 | mg | mg/min |
| `kcal/kg` | 10 | 4 | — | kcal/kg |
| `g/kg/ngày` | 10 | 4 | g/kg | g/kg/day |
| `g/24 giờ` | 10 | 2 | g | g/day |
| `pg/kg/phút` | 9 | 1 | — | pg/kg/min (lỗi OCR của µg/kg/phút ở 292/2024: KHÔNG đoán) |
| `ngay` | 9 | 4 | — | day |
| `ng/ml` | 9 | 3 | — | ng/mL |
| `µg/l` | 8 | 2 | ug | ug/L |
| `umol/l` | 8 | 4 | — | umol/L |
| `mosm/kg` | 8 | 2 | — | mOsm/kg |
| `mmol` | 8 | 3 | — | mmol |
| `g/giờ` | 8 | 2 | g | g/h |
| `ml/ngày` | 7 | 3 | ml | ml/day |
| `ml/h` | 7 | 2 | ml | ml/h |
| `mcg/kg/ph` | 7 | 2 | ug/kg | ug/kg/min |
| `lan/ngay` | 7 | 1 | — | times/day |
| `µg/ml` | 6 | 1 | ug | ug/mL |
| `µg/kg/min` | 6 | 1 | ug/kg | ug/kg/min |
| `tb/mm3` | 6 | 1 | — | /uL |
| `phút/ngày` | 6 | 2 | min | min/day |
| `miu` | 6 | 1 | — | MIU |
| `l/phút` | 6 | 5 | l | L/min |
| `µg/ngày`, `µg/dl`, `tuoi`, `phút/tuần`, `ml/ph/1,73m2`, `ml/1 phút`, `mg/ngay`, `mg/ m2/lần`, `mg%`, `liều/ngày`, `l/kg`, `g/ ngày`, `cm2` | 5 mỗi | 1–3 | ug, ug, —, min, ml, ml, mg, mg, mg, —, l, g, cm | ug/day, ug/dL, year, min/week, mL/min/1.73m2, ml/min, mg/day, mg/m2, mg/dL, times/day, L/kg, g/day, cm2 |
| 31 cách viết khác xuất hiện 3–4 lần (`vién/ngay`, `ng/kg/phút`, `ml/24 giờ`, `lần/24 giờ`, `kcal/kg/ngày`, `giò`, `ck/phút`, `đv/kg`, `u/kg`, `tuôi`, `nhịp/phút`, `ml/kg/phút`, `meq`, `iu/kg/ngày`, `gam/ngày`, `g/g`…) | 3–4 | 1–3 | | đúng đơn vị |

Ngoài bảng (mới, ít hoặc ghép nhiều từ): `2,4 triệu đơn vị` / `triệu U` / `MIU` / `million units` = MIU (= 10^6 IU; trước
đây "2,4" được hiểu theo đơn vị của mẩu); "G/L" (G hoa) = 10^9/L, "g/L" (g thường) = gam/lít; `tế bào/mm3` = /µL; `mEq/L/h`,
`mmol/L/h`, `mmol/L/24 giờ` = mmol/L/day; `IU/kg/h`, `IU/h`, `IU/day`, `MIU/day`; `drops/min`; `mL/min/year` (dốc eGFR);
`kg/tháng`, `kg/tuần`; `min/day`, `min/week`, `h/day`; `mg/m2`, `mg/m2/day`, `mg/m2/week`; `°F`; `‰`; `percentile`
("95th percentile", "bách phân vị"); các cách viết không dấu/OCR (`lan/ngay`, `lân/ngày`, `vién`, `tuôi`, `giò`).

Quy tắc đọc mới:
- Khoảng trắng quanh "/" được đọc cho MỌI đơn vị ("60mg/ ngày" = "60 mg /ngày" = "60mg/ngày" → mg/day; trước: mg).
- Dạng mỗi liều giữ đơn vị mỗi liều ("mg/lần", "mg/liều", "mg/kg/lần" → mg, mg/kg); dạng mỗi ngày là /day ("g/ngày",
  "viên/ngày", "UI/ngày"); khoảng cách ("8 giờ/lần", "3 tháng/lần") là khoảng thời gian.
- "0,0625" là một số (trước: "0,062" + "5" vì nhánh hàng nghìn không chặn chữ số tiếp theo; calibration 1857 G1).
- Liều tổ hợp cố định: "49/51 mg", "37.5mg/20mg", "300/300/50 mg", "800/160 mg" = mỗi phần một giá trị mg (chỉ đơn vị khối
  lượng; "250 mg/5 ml", "500 mg/12h", "10/20 mg/kg" không phải cặp).
- Chữ số chỉ số dưới ("cmH₂O", "MgSO₄") là chữ số.

Cạnh quy đổi mới — CHỈ khi chính xác: tiền tố SI và thời gian (g/day↔mg/day, mg/h↔mg/day, µg/kg/min↔mg/kg/h, L/min↔mL/min,
mL/day↔mL/h, IU/h↔IU/day, MIU↔IU, s↔min, ms↔s, mm↔cm, ‰↔%), nồng độ khối lượng (g/L↔mg/L↔mg/dL↔g/dL, µg/mL=mg/L,
ng/mL=µg/L, pg/mL=ng/L, µmol/L↔mmol/L, mIU/mL↔mIU/L), "°" = °C (Celsius là thang duy nhất của kho). Theo `context` của mẩu:
`analyte` (thêm creatinine 113,12; uric_acid; calcium; phosphate; magnesium cho mg/dL↔mmol/L; valence cho mEq↔mmol của
sodium/potassium/chloride/bicarbonate (1) và calcium/magnesium (2)), `weight_kg` (mg/kg/h, µg/kg/min, µg/kg/h → theo cân
nặng), `doses_per_day` (MỚI: mg↔mg/day, mg/kg↔mg/kg/day, g, µg, mL, IU, viên), `mg_per_tablet` (viên/ngày↔mg/day).
KHÔNG có cạnh (có test): mg↔mg/day không có `doses_per_day`; mL/min↔mL/min/1.73m2; days/week↔times/week; min/day↔min/week;
kg/tháng↔kg/tuần; cmH2O↔mmHg; °F↔°C; mg/g↔mg/mmol; drops/min↔mL/h; dốc eGFR↔eGFR.

## 6. Kiểm hồi quy

- Toàn bộ test: **1.734 passed** (`.venv/bin/python -m pytest`); ruff sạch (`ruff check src scripts tests .claude/hooks`).
  Test mới: `tests/test_normalize.py` (mục 1.3.1: đơn vị kho, khoảng trắng quanh "/", mỗi liều/mỗi ngày, cạnh chính xác và
  cạnh bị cấm, liều tổ hợp, thuốc của kho, không-phải-thuốc, bí danh không trùng từ tiếng Việt) và
  `tests/test_grade_fixes.py` (mục 1.3.1: chấm đơn vị mới, doses_per_day, thuốc hỗ trợ đối xứng Bộ Y tế/nước ngoài/mồi,
  tổ hợp cố định, E6 với thuốc mới, hồi quy 65 mẩu thí điểm và 368 phương án trắc nghiệm). Một test cũ đổi kỳ vọng có chủ
  đích: "10 mg/kg/h" nay là mg/kg/h (trước: mg/kg vì chưa có đơn vị này). `tests/test_grade.py` cho phép mã chuỗi 3 chữ HOA
  với ngưỡng ≥ 2.
- 65 mẩu thí điểm: render mọi giá trị ghi nhận (VI+EN) rồi `grade_short` — 0 thay đổi (nhãn, decoy, hệ thống nước ngoài,
  bản cũ, parse_method); chấm `text` của mọi mục — 0 thay đổi; `conflict_status`/tolerance 65/65 không đổi;
  `missing_vn_values` rỗng (0/65).
- 368 phương án trắc nghiệm thí điểm chấm như câu ngắn: 4 thay đổi, đều là phương án gây nhiễu "Dùng metamizol xen kẽ với
  paracetamol" (P-dengue-04, VI/EN × 2 thứ tự) 6 → 5 `unlisted` — đúng vai trò (giá trị không thuộc nguồn nào);
  lệch vai trò 8 → 4, không có lệch mới.
- 317 mẩu hiệu chỉnh (`data/interim/atoms_parts/`): `missing_vn_values` đổi ở **24 mẩu** — TẤT CẢ là mẩu ghi đơn vị thay
  thế theo cách bộ đọc cũ đọc sai (người trích đã tự khai phần lớn ở `extraction.unit_gap`/coverage). Cả 24 qua khi đặt
  đúng đơn vị thật (đã thử trong bộ nhớ, không sửa tệp):
  - 1019/2025: 037, 068, 069, 071, 072, 073 (l → **L/min**); 074, 075, 080 (cm → **cmH2O**); 063 (g → **g/L**);
    050 (g/kg → **g/kg/day**); 015 (IU → **IU/day**, "UI/ngày").
  - 1840/2025: 045, 046, 047 (mg → **mg/day**, "60mg/ ngày" — đúng đề nghị của kiểm toán S2).
  - 1857/2022: 096–101 (ug/kg → **ug/kg/min**).
  - 2892/2022: 016 (g → **g/day**, "muối dưới 5g/ngày"), 025 (kg → **kg/month**), 035 (day → **days/week**).
  Mẩu khác đọc thêm giá trị đúng mà không đổi kết quả kiểm: 1019-017…020 (bỏ "> 38,5oC" khỏi mẩu mg/kg vì nay là °C),
  1857-010/067/104 (bỏ "lần/phút", "ms", "µmol/L" khỏi mẩu % / pH), 1857-049/050 (đọc thêm ISDN 20, 40 mg trong
  "37.5mg/20mg"), 1857-105/106 (µmol/L ↔ mmol/L nay quy đổi được).
- Các khuyến cáo bị chặn vì bảng thuốc ở hiệu chỉnh nay đọc được từ lớp chữ: 1019 D1–D6 (amoxicillin ± acid clavulanic,
  ciprofloxacin/ofloxacin/levofloxacin, cefotaxim/ceftriaxon, nystatin, oxacillin/cloxacillin/vancomycin, colistin,
  mannitol, paracetamol/ibuprofen, oresol, diazepam), 1840 (oseltamivir, zanamivir, baloxavir), 1857 mục 7–14
  (sacubitril/valsartan/ARNI, dapagliflozin, empagliflozin, canagliflozin, 4 chẹn beta, furosemid, noradrenalin, dopamin),
  2892 (orlistat, liraglutide).

## 7. Còn chưa đọc được / việc cần người điều phối quyết

Đơn vị và số:
1. **"3.125 mg"** (bảng 1857/2022 dùng dấu chấm thập phân kiểu Anh) vẫn là 3125 theo quy ước tiếng Việt đã đăng ký; cần
   `extraction.decimal_style: en` + kiểm span bằng `lang="en"` (đề xuất P8 của kiểm toán) — chưa làm (ngoài bộ đọc).
2. **"mg daily", "mg mỗi ngày", "50 mg 1 lần/ngày"** vẫn đọc là mg (mỗi liều), như 1.3.0: đổi sang mg/day sẽ làm câu trả lời
   đúng "50 mg once daily" cho mẩu đơn vị mg thành lệch đơn vị. Mẩu liều dùng n lần/ngày nên ghi `context.doses_per_day`
   (mg↔mg/day chính xác). "mg/ngày" (có gạch chéo) vẫn là mg/day như trước.
3. **eGFR viết "ml/phút"** (không có /1,73 m2) là mL/min, KHÁC mL/min/1.73m2 — câu trả lời "eGFR < 30 ml/phút" cho mẩu
   mL/min/1.73m2 là nhãn 5 (unit_mismatch). Kho viết cả hai dạng (55 lần "ml/phút", 106 lần "ml/phút/1,73 m2"). Người
   trích phải ghi đúng đơn vị của span; có coi hai đơn vị là một khi chấm hay không là quyết định khoa học (chưa làm).
4. **days/week ↔ times/week** ("5 ngày/tuần" vs "5 lần/tuần") không quy đổi (không chính xác nếu một ngày có nhiều buổi);
   mẩu vận động 2892 cần quyết định.
5. Giá trị chỉ bằng chữ không số: "mỗi tuần", "hàng tháng", "hằng ngày" (2892 S5); ô bảng "Uống 1 lần x 10 ngày"
   (1840 P3: "1 lần" là số lần, không phải lần/ngày) — không đọc (nguy cơ đọc nhầm mạo từ; luật "một/one" 1.2.0 giữ nguyên).
6. Số đếm không phải đơn vị: "2 mũi", "3 bữa", "2 nang" (nang = viên nang hoặc u nang), "tế bào" không có "/mm3" — số
   hiểu theo đơn vị của mẩu (luật 3). "triệu" trơn không đọc ("4 triệu chứng").
7. Lỗi OCR không đoán: "pg/kg/phút" (292/2024, thật là µg/kg/phút), "tuân" (2855/2024, "tuần"; không đọc vì "6 Tuân thủ"),
   "1,73m®", "Amoxieillin", "Cefoperazon/sulbac tam" — người trích ghi span nguyên văn và gắn cờ; kiểm ảnh trang.
8. Nồng độ chế phẩm ("1 mg/ml", "1‰", "1:1000") vẫn bị bộ chấm bỏ (1.1.0); mẩu về nồng độ pha không chấm được.
9. `ml/min`, `L/kg`, `mOsm`, `mg/g`, `percentile`… là đơn vị riêng: số không đơn vị trong câu trả lời vẫn hiểu theo đơn vị
   mẩu (luật 3 đã đăng ký; kiểm span còn yếu S3 của hiệu chỉnh 1019).

Thuốc:
10. **Khuyến cáo ở mức nhóm thuốc** (statin, SGLT2i, ACEi/ARB, chẹn beta, MRA, LABA/LAMA/ICS, PPI, NSAID, cephalosporin thế
    hệ 3, carbapenem, fluoroquinolone, macrolide, aminoglycoside, corticoid, benzodiazepin, NOAC/DOAC, insulin nền…) không
    thêm thành lớp: đổi nghĩa chấm (lớp = một thành viên, luật trung lập) và cần quyết định P12 của kiểm toán. Chỉ LMWH được
    thêm để chặn đọc nhầm thành heparin.
11. **Mọi loại insulin là MỘT thuốc** (`insulin`): không phân biệt glargine/NPH/regular bằng mẩu thuốc; khuyến cáo loại insulin
    phải làm mẩu cat.
12. **Thuốc nhắc lại từ đề** ("ngộ độc paracetamol → N-acetylcystein", "dị ứng penicillin → doxycyclin", "kháng rifampicin")
    được đọc như thuốc của câu trả lời → E4 "thuốc thừa" → nhãn 5. Vấn đề đã có từ 1.3.0 (rifampicin), nay rộng hơn (3610
    ngộ độc). Chưa thêm luật "thuốc của đề là nền" vì phản ví dụ ngay trong thí điểm: P-tbhiv-01/02 có "kháng rifampicin"
    trong đề — cho rifampicin làm nền sẽ chấm đúng "BPaLM + rifampicin". Cách hiện có: người trích ghi thuốc của đề vào `text`
    của mục khi cần (thành nền của mẩu), hoặc người điều phối quyết một luật riêng.
13. **E6 (1.3.0) rộng hơn**: mẩu cat — câu trả lời chỉ nêu một thuốc mới đọc được, không khớp hạng mục nào → 5 `unlisted`
    (trước: 6 vì không biết là thuốc). Ví dụ tự viết: "ĐÁP ÁN: Paracetamol" cho P-dengue-04 (metamizol có được dùng?) 6 → 5;
    "Oresol", "Dopamin" cho P-dengue-03 6 → 5. Đúng ý E6 nhưng là thay đổi nhãn so với 1.3.0.
14. Viết tắt mơ hồ vẫn không đọc đứng riêng: "ABC"/"RAL" cần ≥ 2 thuốc khác trong chuỗi ("ABC/3TC" riêng không đọc), "DAC"
    (= đặc), "LED", "BAL", "NAC" (= nấc), "SAT" (= sắt), "G/P". Phác đồ chữ lao (HRZE, 2RHZE/4RH) vẫn do `tb_codes` đọc cho mẩu
    cat, không thành danh sách thuốc.
15. Không phải thuốc theo nghĩa bảng: vắc xin, chế phẩm máu (hồng cầu lắng, tiểu cầu, huyết tương), oxy, nguyên tố vi lượng
    dinh dưỡng (selen, crom… 2131/2026), chất độc (paraquat, methanol…).
16. Ngoài bảng vì chỉ có trong kho ở dạng không đọc được: dimercaprol ("BAL"), cefoperazone-sulbactam ("sulbac tam" OCR),
    calci carbonat ("canxi" trơn), natri zirconium cyclosilicat ("muối silicate của zirconium").

Việc tiếp theo cho người trích: sửa `unit` của 24 mẩu ở §6 (và bỏ `extraction.unit_gap`), tạo lại các mẩu thuốc đã khai
"chờ bảng thuốc" (1019: 14 dòng; 1857: 8 mẩu; 1840: 010–011 chuyển sang `drugs`; 2892: orlistat/liraglutide), ghi
`key_drugs` bằng khóa tổ hợp cho sản phẩm cố định, ghi `context.doses_per_day` cho liều mỗi lần có số lần/ngày.
