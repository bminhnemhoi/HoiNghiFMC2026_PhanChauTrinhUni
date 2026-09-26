# Kiểm toán độc lập: Phản vệ từ OCR TT51/2017, có DR8 với QĐ 3942/2014 và QĐ 3312/2015 (ID = anaphylaxis_ocr)

- Ngày: 2026-09-26.
- Người kiểm: integrity-auditor (Claude, AI). Góc nhìn lâm sàng trong file này là **AI đóng vai bác sĩ Việt Nam, không phải bác sĩ thật**. Chưa có người nào kiểm các nội dung ở đây.
- Đầu vào: `data/interim/pilot/anaphylaxis_ocr.jsonl` (6 mẩu, ghi lúc 11:42) và `data/interim/pilot/anaphylaxis_ocr_report.md`.
- Tôi chỉ đọc dữ liệu. File duy nhất tôi ghi trong dự án là file này (thao tác phụ kê ở mục 7).

## 0. Kết luận ngắn

**Phán quyết: pass 1 · fix 5 · reject 0.**
- **pass:** P-…-03.
- **fix:** P-…-01, -02, -04, -05, -06.
- **Dữ liệu gốc đúng.** Mọi span, trang, con số, đơn vị và giá trị nước ngoài tôi kiểm lại đều đúng. Mồi và trạng thái tái tạo được y hệt. Tôi không thấy giá trị bịa.

Các vấn đề cần sửa, theo mức nặng:

1. **Hai mẩu "xung đột" (-01, -05) chỉ là xung đột khi tách quần thể theo nguyên nhân phản vệ.**
   - QĐ 3942/2014 chương dị ứng thức ăn (trang PDF 48) ghi 0,15 mg cho trẻ 10–25 kg. Nếu coi liều adrenalin tiêm bắp **không phụ thuộc nguyên nhân** (đây là cách hiểu lâm sàng tự nhiên), thì DR8 đưa 0,15 mg vào tập VN. Khi đó cả -01 lẫn -05 thành **concordant**. Tôi đã tính lại bằng `choose_decoy` và `finalize` (mục 3).
   - Bảng 3a của báo cáo **thiếu đúng cột này**.
   - Như vậy chủ đề này **không có mẩu xung đột nào đứng vững dưới mọi cách đọc**.
   - Thêm nữa, 150 µg là giá trị Bộ Y tế **hiện hành** cho trẻ cùng tuổi, cùng cân nặng. Vì vậy nếu mô hình trả lời 0,15 mg thì không quy sạch về RCUK/WAO được.
   - Đề nghị: **chưa đưa -01 và -05 vào tập kiểm định xác nhận H1** cho tới khi người dùng quyết định ở HG.
2. **`span_verified` sai với thực tế công cụ.**
   - Lúc 11:51, `verify_span.py` được sửa để đọc `extraction.dr8_sources`. Tôi chạy lại lúc 11:59: **6/6 OK**, exit 0.
   - File mẩu vẫn ghi `span_verified: false` cho 5 mẩu. Phần notes và `vn_item_checks` vẫn nói "verify_span LỖI". Báo cáo cũng ghi "1/6". Tất cả đã lỗi thời.
   - `pilot_merge` không tự đặt lại trường này.
3. **QĐ 3942/2014 chưa có dòng manifest.** Đây là nguồn DR8 của 5/6 mẩu, nên nó sẽ nằm **ngoài kho đóng băng**.
4. **Checklist HG1.2 do `pilot_merge.checklist()` sinh ra không in `dr8_sources` và không nhắc so ảnh trang OCR.** Người kiểm sẽ không thấy các span 3312/3942/TT51 tr.20, dù chính chúng quyết định trạng thái.
5. **Bộ chấm có lỗi đọc đơn vị:**
   - "0,01 ml/kg" bị đọc thành **10 µg**. Hệ quả: câu trả lời dùng đúng chữ của 3942 hay WAO sẽ bị chấm "không quy được nguồn".
   - "1⁄3" (dấu gạch phân số U+2044, có trong span -05) bị đọc thành 1 µg và **3000 µg**.

## 1. Lệnh kiểm đã chạy

| Lệnh | Kết quả |
|---|---|
| `vnsoc.schemas atom …/anaphylaxis_ocr.jsonl` | `OK 6 dòng hợp lệ (atom)` |
| `vnsoc.extract.verify_span …/anaphylaxis_ocr.jsonl` (lần 1, bản mã trước 11:51) | 1 OK (-03), 5 LỖI "không đọc lại được giá trị vn … từ span". Khớp với báo cáo |
| `verify_span` (lần 2, 11:59, sau khi `verify_span.py` sửa lúc 11:51:19 để đọc `dr8_sources`) | **OK cả 6, exit 0** |
| `pilot_merge.check()` và `source_warnings()` gọi trực tiếp (chỉ đọc, không chạy `main`) | `[]` cho cả 6 mẩu |
| `choose_decoy` / `finalize` tính lại từ đầu (bỏ decoy, tolerance, status đã ghi) | Trùng hoàn toàn: -01 và -05 mồi 383,333 µg (`mirror_arith`), dung sai 25, conflict. -02, -03, -04, -06 concordant; dung sai 25 / 0 / 0 / 8,33 |
| `--page` và `--image` TT51 trang 9 và 20; tôi mở PNG bằng Read | Xem mục 2 |
| `--page` 3312 tr.1, 29–32, 55, 81, 90, 103–107; 3942 tr.5, 12–15, 42, 47–49, 66–77, 123–144; 3610 tr.1, 132–133, 165–166; TT51 tr.3, 7, 8, 10–16, 18, 19 | Xem mục 4 |
| Quét mọi PDF trong `data/raw` (62 file) tìm liều adrenalin tiêm bắp | Chỉ TT51, 3942, 3312, 3610 có. 5 file là bản quét chưa OCR (1327/2014 sởi, 1470/2024 ĐTĐ thai kỳ, bản sao 3310/2019, TT10/2024, TT13/2026). Theo tên, không file nào là văn bản phản vệ |
| `vnsoc.match.sources grep` (bản đệm): RCUK 2021, WAO 2020, AAAAI 2023 | Mọi giá trị nước ngoài có đúng trang/vị trí. Xem mục 5 |

## 2. Kiểm ảnh trang OCR (tôi tự xem ảnh, độc lập với agent)

- **TT51 trang PDF 9** (số in 9), `data/cache/page_images/TT51_2017_p009.png`. Ảnh ghi:
  - "1. Thuốc adrenalin 1mg = 1ml = 1 ống, tiêm bắp:"
  - "a) Trẻ sơ sinh hoặc trẻ < 10kg: 0,2ml (tương đương 1/5 ống)."
  - "b) … 10 kg: 0,25ml (… 1/4 ống)."
  - "c) … 20 kg: 0,3ml (… 1/3 ống)."
  - "d) Trẻ > 30kg: 0,5ml (… 1/2 ống)."
  - "e) Người lớn: 0,5-1ml (… 1/2 - 1 ống)."
  - "2. Theo dõi huyết áp 3-5 phút/lần."
  - "3. Tiêm nhắc lại … 3-5 phút/lần …"
  - **Mọi số và đơn vị trong span của -01, -02, -03, -05, -06 và span DR8 tr.9 của -04 đều khớp ảnh.**
  - Lỗi OCR đều nằm ngoài span: "Img" = 1mg; "1⁄2 - ]" = "1/2 - 1"; "phúVlần" = phút/lần (span DR8 của -04 giữ nguyên văn OCR, đúng quy tắc). Thêm một lỗi agent chưa ghi: OCR đọc "≥ 90mmHg" thành "> 90mmHg", cũng ngoài span.
- **TT51 trang PDF 20** (số in 20), `…_p020.png`. Ô "TIÊM BẮP" ghi: "- Người lớn: 1/2 ống - Trẻ em: 1/5-1/3 ống • Nhắc lại sau mỗi 3-5 phút cho đến khi hết các dấu hiệu về hô hấp và tiêu hóa, huyết động ổn định".
  - **Khớp span của -04 và span DR8 tr.20.**
  - OCR chèn "6" trước "ôn định" và bỏ dấu "TIEM BAP". Cả hai đều ngoài phần số hoặc không phải chữ số.
  - Trang 19 (sơ đồ chi tiết PL X) có cùng các giá trị.
- **Sơ đồ:** ô TIÊM BẮP nằm dưới "Nặng (độ II)". "Nguy kịch (độ III)" dẫn tới ô ĐƯỜNG TĨNH MẠCH, nhưng ô này mở đầu bằng "Sau khi tiêm bắp adrenalin > 2 lần". PL III mục III (tr.8) áp phác đồ cho độ II và III. Như vậy cả độ II lẫn III đều tiêm bắp theo mục IV.1.

## 3. Phát hiện chính: trạng thái của -01 và -05 phụ thuộc cách đọc quần thể

Tôi tính lại bằng `choose_decoy` và `finalize`. Các giá trị thêm vào đều có span thật đã kiểm: 3942 tr.48 "Trẻ em nặng 10-25kg: adrenaline 0,15mg tiêm bắp" và "Trẻ em nặng > 25kg, adrenaline 0.3mg"; 3942 tr.77 "người lớn: 0,3-0,5 mg" và "nhắc lại cứ 10 phút/lần".

| Mẩu | Bản ghi (DR8 theo nguyên nhân) | **DR8 không phụ thuộc nguyên nhân** (cột báo cáo thiếu) | Coi 3942/3312 là bản cũ (theo báo cáo) | Chỉ TT51 PL III (Điều 6.2, xem dưới) |
|---|---|---|---|---|
| -01 (10 kg) | conflict | **concordant** (+0,15 mg của tr.48) | indistinguishable | conflict (mồi 350 µg, dung sai 50) |
| -05 (20 kg) | conflict | **concordant** (+0,15 mg của tr.48, 10–25 kg) | conflict | conflict (mồi 400 µg) |
| -06 (35 kg) | concordant | concordant | indistinguishable | conflict (mồi 650 µg) |
| -02 (10 kg, thức ăn) | concordant | concordant; **trùng hẳn -01** | indistinguishable | conflict (mồi 350 µg) |
| -03 (người lớn) | concordant | concordant (tập VN thành 0,3–1 mg) | concordant | concordant |
| -04 (nhắc lại) | concordant | concordant (+10 phút) | concordant | concordant |

**Nhận định lâm sàng (AI đóng vai):**
- Liều adrenalin tiêm bắp cho phản vệ **không đổi theo tác nhân**. Việc 3942 ghi 0,15 mg ở chương thức ăn và 0,01 ml/kg ở chương thuốc là do phạm vi từng chương, không phải một khác biệt lâm sàng.
- Một bác sĩ Việt Nam đọc 3942 sẽ coi 0,15 mg cho trẻ 10–25 kg là liều Bộ Y tế chấp nhận.
- Vì vậy, tách quần thể "do thuốc" và "do thức ăn" để giữ xung đột là **cách đọc theo câu chữ, hợp lệ nhưng yếu**. Nó đúng tinh thần quy tắc "mẩu không phân biệt được nguồn" (§1.2) ít hơn cách đọc lâm sàng.

**TT51 Điều 6.2** (OCR tr.3; bài kiểm toán `anaphylaxis_verify.md` trước đã nêu) ghi: "Bác sĩ, y sỹ, điều dưỡng viên … phải xử trí cấp cứu phản vệ theo quy định tại Phụ lục III, Phụ lục IV". PL III I.1 áp cho "Tất cả trường hợp phản vệ".
- Đây là căn cứ pháp lý mạnh nhất cho cách đọc "chỉ TT51" (TT51 là văn bản quy phạm pháp luật; 3942/3312 là quyết định chuyên môn).
- Báo cáo OCR **vẫn không nêu Điều 6.2** trong danh sách quyết định cho người (mục 7.2).

**Kết luận:** việc chọn cách đọc là **quyết định khoa học/pháp lý của người dùng**, phải ghi `docs/DECISIONS.md` trước khi đóng băng mẩu.

## 4. Kiểm DR8: văn bản, phạm vi, tính đầy đủ

- **Mọi span DR8 có đúng trên trang khai báo** (`span_on_page` = True): TT51 tr.20 (51 ký tự), TT51 tr.9 (100), 3312 tr.106 (258), 3942 tr.13 (239), 3942 tr.48 (165). Tất cả ≤ 300 ký tự.
- **Đọc lại theo từng nguồn khai báo** (tôi tự tách từng span): mỗi mục `vn` đọc lại được từ **đúng** nguồn của nó.
  - -01 vn[2] từ 3312 tr.106 (0,01 mg/kg → 100 µg).
  - -02 vn[3] từ 3942 tr.48 (150 µg).
  - -04 vn[1] từ 3942 tr.13 (5–15 phút).
  - -05 vn[2] từ 3312.
  - -06 vn[1] từ TT51 tr.20, vn[2] từ 3312 (350 µg), vn[3] từ 3942 tr.13 (≤ 300 µg).
  - Riêng "0,01 ml/kg" của 3942 tr.13 không đọc được (lỗi bộ chấm, mục 6.3).
- **Hạn chế của `verify_span` mới:** công cụ gộp số của **mọi** span rồi so, không so theo nguồn khai báo của từng mục. Có khớp do trùng số:
  - vn[1] của -01 (200–333 µg) cũng "khớp" với "0,2ml" của dòng a) "< 10kg" nằm trong span chính (quần thể khác).
  - Nó cũng khớp với "0,3 ml" của 3312 (dành cho "trẻ em không biết cân nặng").
  - Với 6 mẩu này kết quả vẫn đúng, vì nguồn thật có tồn tại. Nhưng công cụ sẽ **không bắt được** trường hợp khai nguồn sai (đề xuất 6.2).
- **Tính hiện hành:**
  - TT51 Điều 7 (OCR tr.3) chỉ làm hết hiệu lực TT08/1999.
  - 3312 tr.1 là bìa "Ban hành kèm theo Quyết định số 3312/QĐ-BYT ngày 07/8/2015", 807 trang (đúng như báo cáo). Manifest ghi: trang quyết định không bãi bỏ văn bản nào.
  - 3942: manifest của 1851/2020 ghi 1851 chỉ bãi bỏ 2 bài hen của 3942, không đụng phần phản vệ.
  - **3942/2014 không có dòng manifest.** Tôi đã tìm trong `manifest.jsonl` và `manifest_parts/*`: chỉ thấy nhắc trong ghi chú của dòng 1851. PDF `data/raw/3942_2014.pdf` có sha256 `4be16be0fe6812f4…`, trùng bản giải nén từ `Mien-dich.rar` của kcb.vn mà báo cáo trước đã ghi. Nguồn là chính thức, nhưng phải lập dòng manifest.
- **Phạm vi chương đã xác minh:**
  - 3942 mục lục tr.5: không có chương phản vệ chung.
  - Ch.1 mục 4.1 "Điều trị SPV", Bảng 3 (tr.13).
  - Ch.5 "SPV do thức ăn" (tr.48).
  - Ch.9 vắc xin (tr.71): "Tham khảo phần bài SPV".
  - Ch.10 côn trùng đốt (tr.77).
  - Ch.4 mày đay (tr.42): "0,3 – 0,5mg tiêm bắp, nhắc lại sau 15 – 20 phút".
  - 3942 tr.15, 18, 49, 126–130, 143 **không** có liều tiêm bắp khác.
  - **Ghi chú:** Bảng 3 ch.1 dùng câu chữ chung ("Ngừng ngay tiếp xúc với dị nguyên: theo mọi đường vào cơ thể"), và ch.9 trỏ về "bài SPV". Như vậy chính 3942 cũng có dấu hiệu coi Bảng 3 là phác đồ SPV chung. Điều này làm yếu thêm việc gán "chương 1 = chỉ do thuốc".
- **3312:** tr.29, 30, 32, 55 ghi "10 µg/kg" (tr.29, lớp chữ mất ký tự µ: "10g/kg") tiêm bắp, đều bằng 0,01 mg/kg. Tr.81 là ong đốt "0,3ml (TDD)". Tr.90 là tiêm dưới da **dự phòng trước huyết thanh kháng nọc rắn**, không phải điều trị. Không có giá trị nào báo cáo bỏ sót làm đổi tập VN.
- **3610/2015 (Hướng dẫn chẩn đoán và xử trí ngộ độc; manifest ghi current) báo cáo không nhắc tới:**
  - Tr.133 (ong đốt): "tiêm bắp ngay adrenalin 0,3-0,5 ml dung dịch 1/1000". Nguyên nhân côn trùng, không áp cho mẩu nào.
  - Tr.166 (**dị ứng dứa**, tức là do thức ăn): "xử trí theo phác đồ sốc phản vệ của Bộ Y tế: adrenalin tiêm bắp 0,3-0,5 mg/lần, lặp lại sau 5- 15 phút", không nêu tuổi.
  - Theo đúng logic tách theo nguyên nhân của agent, đoạn tr.166 **áp cho -02** nếu thức ăn là dứa. Không đổi trạng thái (-02 vẫn concordant), nhưng quần thể của -02 phải nêu rõ loại thức ăn (mục 5).

## 5. Phán quyết từng mẩu

### P-anaphylaxis_ocr-01 (hạt giống 15, conflict): **fix**

**Đúng:**
- Span tr.9 khớp ảnh. vn gồm 250 µg (tr.9), 200–333,3 µg (tr.20), 0,01 mg/kg = 100 µg (3312 tr.106; 3942 tr.13).
- RCUK tr.29 "6 months - 6 years: 150 micrograms".
- WAO Bảng 6 "children aged 1-5 years 0.15 mg" và 0,01 mg/kg.
- AAAAI tr.4/tr.31 "0.01 mg/kg, up to a maximum of 0.3 mg for children and teenagers".
- Trang RCUK (bản đệm `eb860f98…`, lấy ngày 26/9/2026) ghi "most recent version … published in May 2021". Không có bản mới hơn.
- Mồi và trạng thái tái tạo được.

**Vấn đề và cách sửa:**
1. Đặt `span_verified: true`, vì `verify_span` đã OK từ 11:51. Cập nhật `extraction.notes` và `vn_item_checks`: bỏ câu "verify_span LỖI"; mục ghi chú "không đọc lại được giá trị vn [0]" ở 3942 tr.13 bị đánh số sai, thực ra là vn[2] và do lỗi ml/kg.
2. Trạng thái conflict **phụ thuộc cách đọc** (mục 3). Cách sửa:
   - Thêm vào `extraction.notes` cờ "conflict chỉ khi tách theo nguyên nhân; DR8 không phụ thuộc nguyên nhân → concordant; 3942 tr.48 0,15 mg cùng tuổi và cân nặng".
   - **Không tính -01 vào tập xác nhận H1** và không tính vào chỉ tiêu ≥ 400 mẩu xung đột cho tới khi có quyết định HG ghi trong `docs/DECISIONS.md`.
3. `population.severity` = "độ II–III" không khớp phạm vi "SPV" của 3312/3942. TT51 độ II ghi "Huyết áp chưa tụt", còn 3312 và 3942 viết cho **sốc** phản vệ. Cách sửa: đổi thành "phản vệ độ III (nguy kịch: tụt huyết áp/sốc)". Cả TT51 PL III/PL X lẫn 3312/3942 đều áp chắc chắn cho mức này, nên tập VN là duy nhất. Giá trị không đổi.
4. Span chính có dòng a) "< 10kg: 0,2ml", là giá trị của quần thể khác, và dòng này tạo khớp trùng số cho vn[1]. Cách sửa: cắt span còn "b) Trẻ khoảng 10 kg: 0,25ml (tương đương 1/4 ống)." giống cách -05 và -06 đã làm. Chuỗi này có nguyên văn ở tr.9; mục "tiêm bắp" đã ghi ở `section`.
5. Quy nguồn 150 µg:
   - AAAAI tr.4/tr.31 cũng có bút tiêm 0,15 mg cho trẻ < 15 kg (khuyến cáo 12, tr.20). Agent loại vì khác dạng thuốc (bút tiêm, không phải ống 1 mg/ml). Tôi chấp nhận lý do này.
   - Tuy vậy, cần ghi trong notes rằng câu trả lời 0,15 mg cũng khớp liều bút tiêm của Mỹ, để khi phân tích theo hệ thống không gán riêng cho EU_UK.
6. WHO_global chưa được xét:
   - Mục bản đệm WHO Pocket Book (`…/81170/9789241548373_eng.pdf`) có sha `a859cc83…`. Sha này dùng chung cho 6 URL WHO khác nhau, và văn bản đệm dài **0 ký tự**, nghĩa là trang bị chặn.
   - Tôi thử WebFetch NCBI Bookshelf: bị CAPTCHA.
   - Cách sửa: để người kiểm WHO (Pocket Book 2013, WHO Model Formulary for Children) ở HG. Không điền từ trí nhớ.

### P-anaphylaxis_ocr-02 (biến thể "do thức ăn", concordant): **fix**

**Đúng:** span 3942 tr.48 có trên trang, 0,15 mg đúng, concordant tái tạo được.

**Vấn đề và cách sửa:**
1. Đặt `span_verified: true` và cập nhật notes, như -01.
2. `population.cause` = "do thức ăn (ví dụ sau ăn lạc/sữa)" chưa đủ để tập VN là duy nhất.
   - 3610/2015 tr.166 (dị ứng dứa) cho "0,3-0,5 mg/lần", không nêu tuổi.
   - Cách sửa: ghi "do lạc hoặc sữa bò (không phải dứa/bromelain)". Thêm vào notes: "3610 tr.166 (dứa) và tr.133 (ong) đã kiểm, không áp dụng".
3. Sửa `severity` và cắt span như -01.
4. Nếu người dùng chọn DR8 không phụ thuộc nguyên nhân, -02 **trùng hẳn** -01 (cùng tập VN). Khi đó giữ một mẩu.

### P-anaphylaxis_ocr-03 (hạt giống 14, đối chứng người lớn): **pass**

- `schemas` và `verify_span` OK, `span_verified: true`.
- Span "e) Người lớn: 0,5-1ml" khớp ảnh tr.9. Span được cắt trước chỗ OCR đọc sai "] ống".
- vn 0,5–1 mg trùng 3942 tr.13 và PL X "1/2 ống".
- RCUK 500 µg (tr.29), WAO 0,5 mg (Bảng 6), AAAAI 0,5 mg đều đúng.
- Concordant dưới **mọi** cách đọc ở mục 3.

Ghi chú, không cần sửa ngay: nếu người dùng chọn DR8 không phụ thuộc nguyên nhân, vn phải thêm 0,3–0,5 mg (3942 tr.77 côn trùng; 3610 tr.133 ong: 0,3–0,5 ml dung dịch 1/1000). Khi đó câu trả lời "0,3 mg" (bút tiêm của Mỹ) sẽ thành đúng theo Bộ Y tế thay vì không quy được nguồn.

### P-anaphylaxis_ocr-04 (khoảng tiêm nhắc lại, người lớn, đối chứng): **fix** (chỉ sửa trường)

**Đúng:**
- Span tr.20 khớp ảnh. Span DR8 tr.9 "3-5 phúVlần" giữ đúng nguyên văn OCR.
- vn = 3–5 phút (TT51) ∪ 5–15 phút (3942 tr.13).
- RCUK "repeat IM adrenaline after 5 minutes" (tr.7, 13, 29). WAO "every 5-15 min".
- AAAAI tr.29 "difficult to suggest a specific duration", nên không ghi là đúng.
- Concordant dưới mọi cách đọc.

**Vấn đề và cách sửa:**
1. Đặt `span_verified: true` và cập nhật notes.
2. Sửa `severity` như -01 (không đổi giá trị).
3. RCUK 5 phút chỉ chạm biên 5 của TT51. Mẩu vẫn dùng được làm đối chứng, nhưng không phải đối chứng mạnh.

### P-anaphylaxis_ocr-05 (5 tuổi, 20 kg, conflict): **fix**

**Đúng:**
- Span "c) Trẻ khoảng 20 kg: 0,3ml (tương đương 1⁄3 ống)." khớp ảnh ("1/3"). Ký tự "⁄" đúng là U+2044 trong văn bản OCR và được giữ nguyên văn, đúng quy tắc.
- RCUK 150 µg (6 tháng–6 tuổi) và WAO 0,15 mg (1–5 tuổi, gồm 5 tuổi) đúng.
- Mồi 383,333 µg và conflict tái tạo được.

**Vấn đề và cách sửa:**
1. Đặt `span_verified: true` và cập nhật notes.
2. **Giống -01 mục 2:** 3942 tr.48 ghi "Trẻ em nặng 10-25kg: adrenaline 0,15mg", áp **đúng** cho 20 kg. Nếu DR8 không phụ thuộc nguyên nhân, mẩu thành concordant. Cờ và cách xử lý như -01.
3. Bộ chấm đọc "1⁄3 ống" thành 1 µg (giả định) và 3000 µg. Không làm hỏng span (vn[0] đọc từ "0,3ml"), nhưng cần sửa `normalize_vi` (mục 6.3).
4. Quy nguồn 150 µg: FDA cho bút tiêm 0,15 mg ở 15–30 kg; AAP cho 0,15 mg ở 13–25 kg (AAAAI tr.4). Ghi vào notes như -01 mục 5.
5. Sửa `severity` như -01.

### P-anaphylaxis_ocr-06 (10 tuổi, 35 kg, concordant): **fix** (chỉ sửa trường)

**Đúng:**
- Span "d) Trẻ > 30kg: 0,5ml (tương đương 1/2 ống)." khớp ảnh.
- vn = 500 (tr.9) ∪ 200–333,3 (tr.20) ∪ 350 (3312, 0,01 mg/kg, không ghi liều tối đa, đúng câu chữ) ∪ 300 µg (3942, tối đa 0,3 ml).
- RCUK 6–12 tuổi 300 µg. WAO 0,3 mg (6–12 tuổi) và 0,01 mg/kg = 350 µg. AAAAI 0,35 mg giới hạn tối đa 0,3 mg ở trẻ. Tất cả nằm trong tập VN nên concordant.

**Vấn đề và cách sửa:**
1. Đặt `span_verified: true` và cập nhật notes.
2. Sửa `severity` như -01.
3. Trạng thái concordant **dựa hoàn toàn vào DR8**: nếu chỉ dùng TT51 PL III thì conflict (mồi 650 µg). Báo cáo đã nêu điều này (bảng 3a).

## 6. Kiểm các khẳng định của báo cáo và đề xuất sửa mã

**Khẳng định đúng** (tôi đã tự kiểm):
- sha256 cả 3 PDF: TT51 `cab611be9dd14312…`, 3942 `4be16be0fe6812f4…`, 3312 `a66c5e8bc460807c…`.
- meta OCR TT51 khớp sha PDF (Tesseract 5.4.0, vie+eng, 300 dpi).
- Các lỗi OCR đều nằm ngoài span.
- 3312 là "SPV ở trẻ em", phạm vi mọi nguyên nhân (tr.103, mục 2).
- Liều 3942 tr.13, 42, 48, 77.
- Mọi giá trị nước ngoài và vị trí.
- `source_warnings` rỗng.
- Hòa khoảng cách khi chọn mồi (đề xuất 6.6 của agent) **có thật**. Tôi đảo thứ tự vn của -01 thì `choose_decoy` cho **50 µg**, trùng liều tiêm tĩnh mạch chậm người lớn "50-100µg" của chính TT51 (tr.9, tr.20). `check_decoy` không bắt được vì giá trị này không có trong mẩu. Cần luật phá hòa tất định, đăng ký trước.

**Khẳng định đã lỗi thời hoặc thiếu:**
- "verify_span chỉ 1/6 OK" nay là 6/6.
- Bảng 3a thiếu cột DR8 không phụ thuộc nguyên nhân.
- Mục 7 thiếu TT51 Điều 6.2.
- Bảng ứng viên bị loại không nhắc 3610/2015 (tr.133, tr.166) và 3312 tr.90.
- "Chỉ mục bản đệm thiếu RCUK algorithm": nay đã có (`c7b75e76…`).

**Đề xuất sửa mã/config** (không sửa; ngoài quyền kiểm toán):
1. **`pilot_merge.checklist()`:** in mọi `extraction.dr8_sources` (văn bản, trang, span). Với trang OCR (`ocr_pages`), in dòng "SO SỐ VỚI ẢNH TRANG N" và đường dẫn PNG.
2. **`verify_span`:** so theo **nguồn khai báo** của từng mục vn (ví dụ `dr8_sources[k].vn_idx`), không gộp số của mọi span. Đồng thời để `pilot_merge` đặt `span_verified` theo kết quả `verify_atom`, để không còn mâu thuẫn như 5 mẩu này.
3. **`normalize_vi`:**
   - Thêm `ml/kg` (quy về mg/kg bằng `mg_per_ml`, rồi về mg bằng `weight_kg`).
   - Map U+2044 "⁄" thành "/".
   - Xử lý khoảng phân số "1/5-1/3 ống".
   - Hiện "0,01 ml/kg" thành 10 µg và "1⁄3 ống" thành 3000 µg. Cả hai sẽ **chấm sai** câu trả lời thật.
4. **Manifest:** corpus-librarian lập dòng 3942/2014: nguồn kcb.vn `…Mien-dich.rar` (sha rar `ab82a392…`, sha PDF `4be16be0…`), `partially_amended_by: ['1851/2020']` (chỉ 2 bài hen). Nếu thiếu dòng này, 5 mẩu dựa vào 3942 nằm ngoài kho đóng băng ngày 15/10.
5. **Nhãn chấm "giá trị Bộ Y tế của quần thể bên cạnh"** (đề xuất 6.5 của agent): tôi đồng ý. Đây là điều kiện để dùng -01 và -05 cho H1 nếu người dùng giữ cách tách theo nguyên nhân.

## 7. Việc cho người dùng (HG) và thao tác phụ của tôi

**Việc cho người dùng (HG):**
1. **Quyết định (ghi `docs/DECISIONS.md` trước khi đóng băng mẩu).** Có ba cách đọc DR8 cho liều adrenalin tiêm bắp:
   - (a) tách theo nguyên nhân (như bản ghi);
   - (b) không phụ thuộc nguyên nhân, khi đó -01 và -05 thành concordant;
   - (c) chỉ TT51, theo Điều 6.2.
   - Kèm câu hỏi 3942/3312 có còn là "hiện hành" cho phản vệ hay không.
2. **HG1.2:** so ảnh TT51 tr.9 và tr.20 (các số ở mục 2), **cộng các span DR8** 3312 tr.106, 3942 tr.13 và tr.48. Checklist tự động hiện chưa in các span DR8 này.
3. **WHO_global và EAACI 2021:** mở bản toàn văn, ghi liều tiêm bắp theo tuổi và vị trí. Bản đệm WHO hiện rỗng (sha `a859cc83…`).
4. **Bác sĩ thật (HG3.9):** việc liều adrenalin tiêm bắp không phụ thuộc tác nhân có phải là quan điểm lâm sàng chuẩn tại Việt Nam không? Bệnh viện đang dùng bảng cân nặng của TT51 hay 0,01 mg/kg?

**Thao tác phụ của tôi:**
- Chạy `--image` cho TT51 tr.9 và tr.20. Lệnh ghi đè 2 PNG sẵn có trong `data/cache/page_images/` bằng cùng nội dung.
- Đặt 3 script chỉ đọc trong scratchpad của phiên.
- Gọi WebFetch 1 lần (NCBI, bị CAPTCHA, không lưu gì).
- Không sửa JSONL, mã, config, `data/raw` hay `state`.
