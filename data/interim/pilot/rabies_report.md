# T1.1 thí điểm — Dại, dự phòng sau phơi nhiễm (ID = rabies)

Ngày: 2026-09-26 · Người làm: agent atom-extractor + counterpart-matcher (Claude) · Trạng thái: **KHÔNG tạo được mẩu nào (0/3–4 chỉ tiêu)**

`data/interim/pilot/rabies.jsonl` là **file rỗng (0 mẩu)**. Hai lệnh kiểm vẫn qua trên file rỗng: `vnsoc.schemas atom` → "OK 0 dòng"; `verify_span` → "OK: 0 mẩu không đạt".

Tóm tắt lý do:
1. **Không lấy được PDF chính thức của QĐ 1622/QĐ-BYT (2014).** Link PDF duy nhất trên nguồn chính thức đã chết. Nguồn chính thức còn sống duy nhất (vncdc.gov.vn) chỉ có bản **.doc**. `fetch_pdf` chỉ nhận PDF, nên `data/raw/1622_2014.pdf` không tồn tại và không kiểm span được.
2. **Nội dung 1622/2014 (đọc từ bản .doc chính thức của vncdc) KHÔNG nêu lịch tiêm theo ngày, cũng không nêu liều huyết thanh (IU/kg), trong phần khuyến cáo.** Văn bản giao cho hướng dẫn của nhà sản xuất: "đường tiêm, lịch tiêm và liều lượng cần tuân thủ theo hướng dẫn của nhà sản xuất đã được Bộ Y tế Việt Nam cấp phép". Chuỗi ngày N0-3-7-14-28 và N0-3-7-28 chỉ xuất hiện dưới dạng **tên cột của biểu mẫu ghi chép trong phụ lục**. Vì vậy dòng hạt giống 4 và 5 gán giá trị này cho 1622/2014 với trạng thái "xác nhận" là **không đúng như mô tả** (xem mục 4).

---

## 1. Văn bản đã tìm / tải

### 1a. Văn bản Việt Nam

| Khóa | Nguồn / URL | Kết quả | sha256 (16) | Trang | text_kind |
|---|---|---|---|---|---|
| 1622/2014 (PDF) | benhviennhitrunguong.gov.vn, trang đăng lại QĐ 1622 (19/5/2014). Link PDF trỏ tới `http://syt.kontum.gov.vn/LinkClick.aspx?fileticket=ljRJ8u4x1HU%3d&tabid=425` | **Thất bại**: tên miền syt.kontum.gov.vn không còn phân giải DNS (tỉnh đã sáp nhập năm 2025). Wayback CDX không có bản lưu của link này | — | — | — |
| 1622/2014 (.doc) | vncdc.gov.vn (Cục YTDP cũ): `https://vncdc.gov.vn/files/article_attachment/2015/2/qd1622huongdangsdaitrennguoi2014722163754.doc` (trang tin nd13747) | Tải về **scratchpad** để đọc; KHÔNG ghi vào data/raw vì fetch_pdf từ chối file không phải PDF. Chứng chỉ TLS của vncdc.gov.vn đã hết hạn nên phải dùng `curl -k`. Metadata Word: 17 trang, 6.433 từ, lưu lần cuối 29/5/2014. Tiêu đề "Số: 1622/QĐ-BYT, Hà Nội, ngày 08 tháng 5 năm 2014", người ký Thứ trưởng Nguyễn Thanh Long | feee9c615798369a | 17 (Word) | không áp dụng (.doc, đọc bằng antiword) |
| 1622/2014 (khác) | bvphcn.thuathienhue.gov.vn, ttytdamrong.vn: DNS chết. chicuccntyhcm.gov.vn/Luat/1622-QD-BYT.aspx: 404. emoh.moh.gov.vn / emohbackup.moh.gov.vn: không truy cập được ("server name is not supported" / 404) | Thất bại | — | — | — |
| 1622/2014 | Nhiều kết quả tìm kiếm chỉ trỏ tới trang thư viện pháp luật tư nhân (và các trang tư nhân khác như lawnet, caselaw, luatvietnam, scribd, studocu) | **Không truy cập** (chỉ thấy trên trang thư viện pháp luật tư nhân / trang tư nhân) | — | — | — |
| 5642/2015 | kcb.vn `.../598cf44932833df0d644c6b27564f169Truyen-nhiem-1.pdf` (tải về scratchpad để xem mục lục) | Không có chương bệnh dại (14 bệnh + dengue, não mô cầu, TCM, Naegleria, H7N9). Không liên quan nên không ghi vào data/raw | — | 86 | ok |

**Kiểm văn bản thay thế (1622/2014 còn hiệu lực không?):** không tìm thấy văn bản Bộ Y tế nào mới hơn thay phần điều trị dự phòng hoặc phác đồ vắc xin dại.
- Công văn Sở Y tế An Giang (4/2024, cdcangiang.vn) và HCDC (TP.HCM) vẫn dẫn 1622/QĐ-BYT ngày 08/5/2014 là hướng dẫn hiện hành.
- Tin Bộ Y tế 22/8/2026 (Cục Phòng bệnh, Ngày Thế giới phòng chống bệnh dại 2026) không nêu văn bản chuyên môn mới.

Mức chắc chắn: "không tìm thấy", **chưa chứng minh được là không có**, vì phiên đã hết hạn mức WebSearch (200/200) trước khi quét hết.

### 1b. Nguồn nước ngoài (qua `vnsoc.match.sources`, chỉ lưu giá trị và vị trí)

| Hệ thống | Nguồn | URL | fetched_at | sha256 (16) | Trang PDF | Giá trị (đã grep xác nhận) |
|---|---|---|---|---|---|---|
| WHO_global | Rabies vaccines: WHO position paper, April 2018 (WER 93(16):201–220; 19/4/2018) | `https://iris.who.int/server/api/core/bitstreams/b3f08b00-3107-4643-a0b2-b473f9599540/content` | 2026-09-26 | efadc6faa41ae740 | 19 | **Bảng 1 (PDF tr.15), người chưa tiêm, độ II/III:** ID 2 vị trí ngày 0, 3, 7 (chú thích 73: phác đồ 1 tuần 2-2-2-0-0). HOẶC IM 1 vị trí ngày 0, 3, 7 và 1 mũi trong khoảng ngày 14–28 (chú thích 74: 4 liều Essen 1-1-1-1-0). HOẶC IM 2 vị trí ngày 0 + 1 vị trí ngày 7, 21 (chú thích 75: Zagreb 2-0-1-0-1). **Người đã tiêm (Bảng 1):** ID 1 vị trí ngày 0 và 3, HOẶC ID 4 vị trí ngày 0, HOẶC IM 1 vị trí ngày 0 và 3; không dùng RIG. **RIG (PDF tr.16):** liều tối đa ERIG 40 IU/kg, HRIG 20 IU/kg. PDF tr.8 (mô tả, không phải khuyến cáo): đa số nhà sản xuất khuyên IM 5 liều ngày 0, 3, 7, 14, 28 hoặc Zagreb; một số thêm ID TRC ngày 0, 3, 7, 28 |
| US | ACIP, MMWR Recomm Rep 2010;59(RR-2) (19/3/2010), phác đồ 4 liều | `https://www.cdc.gov/mmwr/pdf/rr/rr5902.pdf` | 2026-09-26 | 6d74a8f35b3c3ec1 | 12 | Người chưa tiêm: liều 1 ngày 0, rồi các ngày 3, 7, 14 (tr.3, tr.8). HRIG 20 IU/kg (tr.8). Người đã tiêm: 2 liều, liều thứ hai vào ngày 3 (tr.8). Người suy giảm miễn dịch: xem tr.9 (không trích tiếp) |
| US | CDC, Rabies PEP (trang HCP hiện hành) | `https://www.cdc.gov/rabies/hcp/clinical-care/post-exposure-prophylaxis.html` | 2026-09-26 | **null** (vnsoc.match.sources bị **403**; đọc bằng WebFetch) | — | Theo WebFetch: ngày 0, 3, 7, 14 (suy giảm miễn dịch thêm ngày 28). HRIG 20 IU/kg. Người đã tiêm: ngày 0 và 3. IM. Trang ghi cập nhật 17/9/2026. **needs_human_check** |
| WHO_global (bản trước) | Summary of the WHO position paper on rabies vaccines, 6/8/2010 | `https://cdn.who.int/media/docs/default-source/ntds/rabies/summary-of-the-rabies-vaccines-who-position-paper-2010.pdf?sfvrsn=91dc30c6_0` | 2026-09-26 | fcbb87a716297c5d | 1 | Bản tóm tắt **không có lịch tiêm theo ngày**. Chưa tải được toàn văn WER 85(32) 2010 (hết hạn mức tìm kiếm) → giá trị WHO 2010 **chưa kiểm** |

Ghi chú:
- Bản cache `data/cache/foreign/a859cc83d1150843….html` là bản rỗng của link IRIS cũ `.../10665/272371/WER9316.pdf`. Trang này trả về HTML 0 ký tự, không dùng.
- Các giá trị trên chưa có mẩu nào để gắn vào. Có thể nạp vào kho `foreign_values.jsonl` (T2.6) khi dựng mẩu dại.

### 1c. Tài liệu chính thức khác (ngoài định nghĩa "hướng dẫn chuyên môn", chỉ để người quyết định)

| Tài liệu | URL | sha256 (16) | Nội dung liên quan |
|---|---|---|---|
| Tờ hướng dẫn sử dụng vắc xin Rabipur được Cục Quản lý Dược duyệt (dav.gov.vn, 2015) | `https://dav.gov.vn/upload/attach/4122015_rapipur.pdf` | e6db2a29f23ab418 | 9 trang, có lớp chữ. **IM:** ngày 0, 3, 7, 14, 28 (5 liều) hoặc 2-1-1 (2 liều ngày 0, rồi ngày 7, 21). **ID TRC:** 2-2-2-0-1-1 (ngày 0, 3, 7, 28, 90) hoặc TRC cập nhật 2-2-2-0-2 (ngày 0, 3, 7, 28). **HRIG** 20 IU/kg, **ERIG** 40 IU/kg. **Người đã tiêm:** ngày 0 và 3 |
| Bài "BỆNH DẠI" trên vncdc.gov.vn (24/06/2016, bài tuyên truyền, không phải quyết định) | `https://vncdc.gov.vn/benh-dai-nd14503.html` | — | IM 0,5 ml × 5 liều ngày 0, 3, 7, 14, 28. **ID 0,1 ml: ngày 0, 3, 7 (2 vị trí), rồi ngày 28 và ngày 90** → tức là 0-3-7-28-90, **khác** 0-3-7-28 trong biểu mẫu 1622 |

---

## 2. Bảng mẩu

**Không có mẩu nào đạt.** Không có dòng nào trong `rabies.jsonl`.

| id | slot | VN | Nước ngoài | Trạng thái | Trang PDF |
|---|---|---|---|---|---|
| — | — | — | — | — | — |

---

## 3. Ứng viên bị loại và lý do

| Ứng viên | Dự kiến | Lý do loại |
|---|---|---|
| P-rabies-01: lịch IM sau phơi nhiễm, người chưa tiêm (hạt giống dòng 4) | VN {0,3,7,14,28} ↔ US {0,3,7,14}; WHO 2018 {0,3,7,d (d=14…28)}, Zagreb {0,7,21} | (a) Không có PDF chính thức nên không kiểm span được. (b) Trong bản .doc chính thức, **mục 3.3.3.1 "Tiêm vắc xin phòng dại" chỉ ghi nguyên tắc** (chọn tiêm bắp hoặc trong da) và **không có ngày tiêm**. Mục "Lưu ý" sau bảng chỉ định chuyển lịch tiêm sang hướng dẫn nhà sản xuất được cấp phép. Ngày 0, 3, 7, 14, 28 chỉ có ở (i) Phụ lục 1 "Bảng theo dõi người tiêm vắc xin phòng dại và huyết thanh kháng dại", cột "Phác đồ tiêm bắp" với các ô Ngày 0/3/7/14/28, và (ii) "Phiếu điều tra bệnh nhân nghi dại/tử vong do bệnh dại", dòng "Tiêm bắp: N0…N3…N7…N14…N28". Đây là biểu mẫu ghi chép, không phải câu khuyến cáo. (c) Kể cả khi có PDF, `parse_schedules` không đọc được dạng "Ngày 0 Ngày 3 …" (chỉ cách bằng dấu cách) hay "N0……N3" (dấu chấm dẫn), nên `verify_span` sẽ thất bại |
| P-rabies-02: lịch ID sau phơi nhiễm, người chưa tiêm (hạt giống dòng 5) | VN {0,3,7,28} ↔ WHO 2018 {0,3,7} | Như trên: chỉ có trong cột "Phác đồ tiêm trong da" (Ngày 0/3/7/28) của Phụ lục 1 và dòng "Tiêm trong da: N0…N3…N7…N28" của phiếu điều tra. Nguồn chính thức khác của Việt Nam lại ghi **0-3-7-28-90** (bài vncdc 2016; tờ HDSD Rabipur bản TRC gốc), nên tập giá trị VN chưa xác định. US không có phác đồ ID sau phơi nhiễm, nên không có đối chiếu US |
| P-rabies-03: liều huyết thanh/globulin kháng dại (đối chứng dự kiến) | VN ? ↔ WHO ERIG 40 / HRIG 20 IU/kg; CDC HRIG 20 IU/kg | 1622/2014 **không có con số IU/kg nào**. Mục 3.3.3.2 chỉ nêu cách tiêm (phong bế vết thương, phần còn lại tiêm bắp xa chỗ tiêm vắc xin, pha loãng 2–3 lần nếu nhiều vết thương) và mốc "không dùng sau 7 ngày kể từ mũi vắc xin đầu". Giá trị 20/40 IU/kg chỉ có trong tờ HDSD vắc xin, không có trong hướng dẫn Bộ Y tế |
| P-rabies-04: người đã tiêm phòng (đối chứng dự kiến) | VN ? ↔ WHO/CDC ngày 0 và 3 | Mục 3.3.4 chỉ ghi: không cần huyết thanh; chọn IM hoặc ID; và các trường hợp phải tiêm lại đủ phác đồ (chưa đủ 3 mũi, vắc xin mô não, HIV/ức chế miễn dịch). **Không có ngày tiêm** |
| Mốc 7 ngày của huyết thanh (có thể thay thế) | VN "không dùng HTKD sau 7 ngày kể từ mũi vắc xin đầu" ↔ WHO 2018 (có nội dung tương tự, chưa grep) | Không có PDF chính thức. Ngoài ra chưa có nhãn slot phù hợp (duration/threshold) và chưa grep phía WHO/CDC. Để dành khi có PDF |

---

## 4. Sai lệch so với bộ hạt giống (§3.3, `data/seed/seed_conflicts.yaml`)

1. **Dòng 4 (IM N0-3-7-14-28, 1622/2014, "confirmed"): KHÔNG xác nhận được như mô tả.** Giá trị này không nằm trong phần khuyến cáo của 1622/2014. Phần khuyến cáo nói lịch tiêm theo hướng dẫn nhà sản xuất được Bộ Y tế cấp phép. Chuỗi ngày chỉ là tên cột biểu mẫu ở phụ lục. Nguồn thật của giá trị nhiều khả năng là tờ HDSD vắc xin (Verorab/Rabipur). WHO 2018 (tr.8) cũng mô tả IM 5 liều 0, 3, 7, 14, 28 là lịch "đa số nhà sản xuất khuyến cáo". Đề nghị đổi trạng thái thành `unverified` / `needs_design_decision`.
2. **Dòng 4, phía nước ngoài:** CDC {0,3,7,14} là **một phần tử của tập WHO 2018** (liều 4 trong khoảng ngày 14–28). Vì vậy câu trả lời "0-3-7-14" sẽ được quy cho cả US và WHO_global, không riêng Mỹ. Hạt giống chỉ ghi CDC. Cần ghi đủ cả hai hệ thống. WHO 2018 còn có Zagreb (2 liều ngày 0, rồi ngày 7, 21).
3. **Dòng 5 (ID N0-3-7-28, "confirmed"): KHÔNG xác nhận được như mô tả**, cùng lý do như dòng 4. Thêm vào đó có **mâu thuẫn nội bộ phía Việt Nam**: bài vncdc 2016 và tờ HDSD Rabipur (bản TRC gốc) ghi ID **0-3-7-28-90**, còn biểu mẫu 1622 ghi 0-3-7-28. Phía WHO: "phác đồ trong da 1 tuần" = 2 vị trí ngày 0, 3, 7 (2-2-2-0-0), đúng với hạt giống.
4. **"Việc: đối chứng liều HRIG/ERIG IU/kg"**: 1622/2014 không có giá trị IU/kg, nên không có đối chứng từ văn bản Bộ Y tế.
5. Chưa kiểm được WHO 2010 (bản trước). Nếu WHO 2010 có IM 5 liều Essen hoặc ID TRC 0-3-7-28 thì giá trị Việt Nam trùng **WHO bản cũ**. Điểm này quan trọng cho nhãn quy nguồn, và phải kiểm toàn văn WER 85(32) 2010 trước khi dùng.

---

## 5. Việc cần người kiểm ở HG1.2

1. **Lấy PDF chính thức 1622/QĐ-BYT (08/5/2014)** từ nguồn chính thức còn sống. Ví dụ: xin Cục Phòng bệnh / Viện VSDT TƯ / Viện Pasteur, hoặc tìm trang Sở Y tế / bệnh viện khác đăng lại. Sau đó chạy `fetch_pdf --key 1622/2014 --url <url>` và báo lại để dựng mẩu.
2. **Quyết định phương pháp (người dùng / bác sĩ):**
   - (a) Biểu mẫu phụ lục của quyết định (cột "Phác đồ tiêm bắp: Ngày 0/3/7/14/28") có được coi là "giá trị khuyến cáo" không?
   - (b) Khi hướng dẫn Bộ Y tế giao lịch tiêm cho "hướng dẫn nhà sản xuất đã được Bộ Y tế cấp phép", có đưa tờ HDSD do Cục Quản lý Dược duyệt (dav.gov.vn) vào tập tham chiếu Việt Nam không? Nếu có, tập VN cho IM sẽ gồm cả Zagreb {0,7,21}, trùng WHO 2018. Tập ID gồm {0,3,7,28} và {0,3,7,28,90}. HRIG 20 / ERIG 40 IU/kg trùng WHO/CDC và sẽ thành đối chứng. Đây là thay đổi định nghĩa chuẩn tham chiếu (§1.2) nên cần ghi `docs/DECISIONS.md`.
   - (c) Nếu không chấp nhận (a) và (b): **loại chủ đề dại khỏi thí điểm** và thay bằng chủ đề khác. Thiếu 2 mẩu xung đột so với chỉ tiêu §5.7.
3. Kiểm tay trang CDC HCP (tool bị 403): lịch ngày 0, 3, 7, 14 (+28 khi suy giảm miễn dịch), HRIG 20 IU/kg, người đã tiêm ngày 0 và 3, cập nhật 17/9/2026.
4. Tải và kiểm toàn văn WHO position paper 2010 (WER 85(32):309–320) để ghi giá trị WHO bản trước.
5. Bác sĩ (HG3.9) xác nhận quần thể: phân độ phơi nhiễm II/III, chưa tiêm hoặc đã tiêm, suy giảm miễn dịch. Lịch IM ở người suy giảm miễn dịch khác người thường ở cả CDC và Rabipur.

---

## 6. Đề xuất bổ sung mã / configs (không tự sửa)

1. **`src/vnsoc/extract/fetch_pdf.py`**: cho phép nhận `.doc/.docx` từ nguồn chính thức (vncdc.gov.vn, moh.gov.vn, kcb.vn). Lưu nguyên file gốc kèm sha256, rồi chuyển sang PDF/văn bản bằng công cụ xác định (LibreOffice headless hoặc antiword). Gắn cờ `derived_from_doc: true` để span được kiểm trên văn bản chuyển đổi, và ghi rõ trong manifest. Cần thêm lựa chọn `verify=False` (có ghi log) cho host chính thức có chứng chỉ hết hạn (vncdc.gov.vn), hoặc để người dùng tải tay.
2. **`src/vnsoc/normalize_vi.py` UNIT_ALIASES**: thêm `"iu/kg": "IU/kg"`, `"ui/kg": "IU/kg"`, `"đơn vị/kg": "IU/kg"` cho liều RIG.
3. **`parse_schedules`**:
   - (i) Nhận chuỗi "Ngày 0 Ngày 3 Ngày 7…" và "N0……N3" (dấu chấm dẫn), vì hiện chỉ nhận dấu `- , ; / và & +`.
   - (ii) Hiện hàm đặt `unit="month"` hễ span có chữ "tháng" ở bất kỳ đâu. Span tiếng Việt về vắc xin dại rất dễ chứa chữ "tháng", nên sẽ đọc sai đơn vị.
4. **Biểu diễn lịch tiêm**: `ValueItem.seq` là dãy ngày duy nhất, nên (i) không ghi được Zagreb "2 liều ngày 0" (2-1-1 thành [0,7,21], mất thông tin số liều), và (ii) không ghi được "liều 4 trong khoảng ngày 14–28" của WHO 2018 (phải liệt kê 15 dãy, hoặc thêm trường khoảng). Đề xuất thêm `doses_per_visit` hoặc `seq_ranges` vào schema, kèm quy tắc chấm đăng ký trước.
5. Không cần thêm thuốc vào `configs/grading.yaml` (lịch tiêm không dùng INN). Nếu sau này có mẩu drugs về RIG thì cân nhắc thêm bí danh `hrig`, `erig`, `rabies immune globulin`, `huyết thanh kháng dại`.
