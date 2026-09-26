# T1.1 thí điểm — Kiểm toán độc lập chủ đề Dại, dự phòng sau phơi nhiễm (ID = rabies)

Ngày: 2026-09-26 · Người kiểm: integrity-auditor (Claude), kiêm góc nhìn bác sĩ lâm sàng Việt Nam **do AI đóng vai, không phải bác sĩ thật** · Đầu vào: `data/interim/pilot/rabies.jsonl` (0 byte), `data/interim/pilot/rabies_report.md`

**Kết luận ngắn**
- File mẩu rỗng, nên **không có atom_id nào để phán quyết** (pass = 0, fix = 0, reject = 0).
- Việc không tạo mẩu là **đúng**: không có PDF chính thức của QĐ 1622/QĐ-BYT, nên không có span nào kiểm được (quy tắc cứng 1).
- Các khẳng định cốt lõi của báo cáo đều được tôi kiểm lại độc lập và **đúng**, gồm: sha256 bản .doc, link chết, nội dung chỉ giao lịch tiêm cho nhà sản xuất, dãy ngày chỉ nằm trong biểu mẫu phụ lục, và giá trị WHO 2018 / ACIP 2010.
- Báo cáo có **4 thiếu sót quan trọng**:
  - (A) Không kiểm WHO 2010 toàn văn. Tôi đã tải được: giá trị Việt Nam của dòng hạt giống 4 và 5 **trùng khít WHO 2010**, tức là lệch phiên bản chứ không chỉ xung đột với Mỹ.
  - (B) Bỏ sót ít nhất 2 ứng viên **xung đột thật** và 3 ứng viên **đối chứng** nằm ngay trong phần khuyến cáo của 1622. Chúng không phụ thuộc biểu mẫu phụ lục.
  - (C) Bỏ sót điều kiện "suy giảm miễn dịch" của ACIP: Mỹ dùng đúng 0-3-7-14-28 cho nhóm này.
  - (D) Vài khẳng định không kèm URL nên không kiểm lại được.
- Đề nghị **chưa loại chủ đề dại** (phương án c của báo cáo). Việc cần làm trước tiên là lấy PDF chính thức, hoặc ra quyết định phương pháp về bản .doc chính thức.

---

## 0. Lệnh kiểm đã chạy

| Lệnh | Kết quả |
|---|---|
| `vnsoc.schemas atom data/interim/pilot/rabies.jsonl` | `OK 0 dòng hợp lệ (atom)`, exit 0 |
| `vnsoc.extract.verify_span data/interim/pilot/rabies.jsonl` | `OK: 0 mẩu không đạt`, exit 0 |
| `ls data/raw` | Không có `1622_2014.pdf` (đúng như báo cáo) |

Hai lệnh "OK" ở đây chỉ vì file rỗng. Chúng **không** chứng minh gì về chất lượng.

## 1. Phán quyết từng mẩu

**Không có mẩu nào** trong `rabies.jsonl`, nên không có mục `{atom_id, verdict}` nào.

## 2. Kiểm các ứng viên bị loại trong báo cáo (mục 3)

| Ứng viên | Tôi đồng ý loại? | Ghi chú kiểm toán |
|---|---|---|
| P-rabies-01 (IM 0-3-7-14-28) | **Đồng ý**, nhưng lý do cần bổ sung | Đã kiểm bản .doc (sha256 `feee9c615798369a…`, trích UTF-16 trực tiếp từ nhị phân). Mục 3.3.3.1 không có ngày. Chuỗi "Ngày 0 / Ngày 3 / Ngày 7 / Ngày 14 / Ngày 28" chỉ có ở tiêu đề cột Phụ lục 1 ("Phác đồ tiêm bắp (Ghi rõ ngày, tháng, năm vào từng ô)"). "Tiêm bắp: N0…N3…N7…N14…N28" chỉ có ở phiếu điều tra. **Bổ sung:** giá trị này trùng WHO 2010 (xem §4.1) và trùng lịch Mỹ cho **người suy giảm miễn dịch** (ACIP 2010 tr.9; trang CDC HCP). Nếu sau này dựng mẩu, quần thể phải ghi rõ "người miễn dịch bình thường", nếu không thì không có xung đột với Mỹ |
| P-rabies-02 (ID 0-3-7-28) | **Đồng ý** | Chỉ có trong cột "Phác đồ tiêm trong da" của Phụ lục 1 và phiếu điều tra. **Bổ sung:** trùng khít WHO 2010 tr.11 (TRC 2 vị trí, ngày 0, 3, 7, 28). Bản 0-3-7-28-90 (bài vncdc 2016, tờ HDSD Rabipur) là TRC gốc cũ hơn. Mâu thuẫn nội bộ phía Việt Nam mà báo cáo nêu là **có thật** (tôi đã kiểm lại cả hai nguồn) |
| P-rabies-03 (liều RIG IU/kg) | **Đồng ý** | Thân văn bản không có "IU/kg" hay "UI/kg". Con số UI duy nhất là "0,5UI/ml" ở mục 3.2 (ngưỡng tiêm nhắc trước phơi nhiễm), không phải liều RIG |
| P-rabies-04 (người đã tiêm: ngày 0 và 3) | **Đồng ý** (không có ngày) | **Nhưng** mục 3.3.4 có một giá trị định lượng khác mà báo cáo không dựng thành ứng viên: "chưa đủ 3 mũi" thì tiêm lại đủ phác đồ. Xem §4.2-b (ứng viên xung đột / lệch phiên bản) |
| Mốc 7 ngày của huyết thanh | **Đồng ý** (thiếu PDF) | Phía nước ngoài nay **đã grep được**: WHO 2018 tr.16 ("should not be given after day 7…"), WHO 2010 tr.12 ("beyond the seventh day…"), ACIP 2010 tr.8 ("up to and including day 7"). Đây là **đối chứng** tốt khi có PDF |

## 3. Kiểm các khẳng định trong báo cáo

| Khẳng định | Kết quả | Bằng chứng tôi tự tạo |
|---|---|---|
| .doc vncdc sha256 `feee9c61…`, 17 trang Word | **Đúng** | Tải lại độc lập vào scratchpad: `feee9c615798369abdf0219cc8c85a4318b39f20d753e41c8e94ba3d63edfbdb`, 388.096 byte, application/msword. Metadata Word: 17 trang, 6.433 từ, lưu 29/5/2014 |
| Chứng chỉ TLS vncdc.gov.vn hết hạn | **Đúng** | curl không có `-k` báo lỗi `SEC_E_CERT_EXPIRED` |
| syt.kontum.gov.vn chết, Wayback không có bản lưu | **Đúng** | `nslookup`: Non-existent domain. Wayback `available` trả `archived_snapshots: {}`. CDX tiền tố `syt.kontum.gov.vn/LinkClick.aspx` có 80 bản lưu, **không** có fileticket `ljRJ8u4x1HU` |
| vncdc chỉ có .doc | **Đúng** | CDX Wayback `vncdc.gov.vn/files/article_attachment/2015/2/` chỉ có đúng file .doc này |
| Phần khuyến cáo giao lịch tiêm cho nhà sản xuất | **Đúng** | Mục "Lưu ý" sau bảng chỉ định: "đường tiêm, lịch tiêm và liều lượng cần tuân thủ theo hướng dẫn của nhà sản xuất đã được Bộ Y tế Việt Nam cấp phép" |
| 5642/2015 không có chương dại | **Đúng** | `verify_span --find 5642/2015` với "dại", "Dại", "BỆNH DẠI": đều `[]` |
| WHO 2018 (sha `efadc6fa…`): Bảng 1 tr.15; 2-2-2-0-0; Essen 1-1-1-1-0 (liều 4 trong khoảng ngày 14–28); Zagreb 2-0-1-0-1; người đã tiêm ID 1 vị trí ngày 0 và 3 / ID 4 vị trí ngày 0 / IM 1 vị trí ngày 0 và 3; RIG 40/20 IU/kg tr.16; tr.8 mô tả lịch nhà sản xuất (0, 3, 7, 14, 28; TRC 0, 3, 7, 28) | **Đúng cả** | Đã grep từng chuỗi, trang khớp. Trang WHO position papers (WebFetch, không có sha) xác nhận **2018 vẫn là bản hiện hành, chưa có bản 2019–2026** |
| ACIP 2010 (sha `6d74a8f3…`): 0, 3, 7, 14 (tr.3, 8); HRIG 20 IU/kg (tr.8); người đã tiêm 2 liều | **Đúng** | Đã grep. **Bị bỏ sót:** tr.9 ghi người suy giảm miễn dịch dùng phác đồ 5 liều ngày 0, 3, 7, 14, 28 |
| CDC HCP bị 403 | **Đúng** | `vnsoc.match.sources fetch` báo 403. WebFetch: 0, 3, 7, 14; suy giảm miễn dịch 0, 3, 7, 14, 28; HRIG 20 IU/kg; người đã tiêm ngày 0 và 3; chỉ IM. Trang ghi Updated 17/9/2026. Vẫn **needs_human_check** (page_sha256 = null) |
| Bản tóm tắt WHO 2010 không có lịch theo ngày | **Đúng** | Grep "days" trên sha `fcbb87a7…` được 0 kết quả |
| Tờ HDSD Rabipur (dav.gov.vn, sha `e6db2a29…`) | **Đúng về giá trị**; sai nhỏ về năm | Có IM 0, 3, 7, 14, 28; 2-1-1; ID TRC 2-2-2-0-1-1 (ngày 28/30 và 90), có thể dời liều ngày 90 về ngày 28; HRIG 20 / ERIG 40 IU/kg; người đã tiêm ngày 0 và 3. Metadata PDF CreationDate = **30/6/2014** (báo cáo ghi "2015", thư mục URL 4122015 chỉ là ngày đăng). Báo cáo bỏ sót phác đồ Oxford 8 vị trí (8-0-4-0-1-1) và câu về người suy giảm miễn dịch / bắt đầu muộn (5 liều, **gấp đôi liều ban đầu**) |
| Bài vncdc 24/06/2016: ID ngày 0, 3, 7 (2 vị trí), rồi ngày 28 và 90 | **Đúng** | Đọc lại bản HTML. Ngữ cảnh là vắc xin **Verorab**, không phải khuyến cáo chung |
| An Giang 2024, HCDC vẫn dẫn 1622; "Tin Bộ Y tế 22/8/2026" | **Không kiểm được** | Báo cáo **không ghi URL**. Hạn mức WebSearch của phiên đã hết (200/200, tôi đã thử và bị từ chối). Tìm trên nihe.org.vn: "Không kết quả". Mức chắc chắn vẫn chỉ là "không tìm thấy văn bản thay thế" |

Ghi thêm: trong scratchpad của agent trước có `na9300.pdf` (dự thảo QĐ "Kế hoạch TCMR 2026–2028", 33 trang, sha `16d494c1…`). Báo cáo không liệt kê file này. Nó không liên quan (chữ "dại" duy nhất là "bại liệt hoang dại"), nhưng mọi file đã tải nên được ghi lại cho minh bạch.

## 4. Phát hiện mới của kiểm toán

### 4.1 WHO 2010 toàn văn: giá trị Việt Nam trùng khít bản WHO cũ (lệch phiên bản)

- Nguồn: Rabies vaccines: WHO position paper, WER 85(32):309–320, 6/8/2010.
- URL: `https://iris.who.int/server/api/core/bitstreams/7ffb982f-2b49-4f57-a600-b9252857d0e5/content` (IRIS handle 10665/241614, bản tiếng Anh `WER8532_309-320.PDF`).
- Tải bằng `vnsoc.match.sources fetch`: sha256 `d5b4bece75f78737291f79bed0023a579ca31ad4ee9e36af03cb2b7d6db9baee`, fetched_at 2026-09-26, 12 trang PDF.

Giá trị đã grep (chỉ ghi giá trị và vị trí):

| Slot | WHO 2010 | Trang PDF |
|---|---|---|
| IM, người chưa tiêm, độ II/III | 5 liều ngày 0, 3, 7, 14, 28 | 11 |
| IM 4 liều Zagreb | 2 liều ngày 0, rồi 1 liều ngày 7 và 21 | 11 |
| IM 4 liều thay thế | ngày 0, 3, 7, 14, **chỉ** cho người khỏe, miễn dịch bình thường, được xử lý vết thương và RIG chất lượng | 11 |
| ID 2 vị trí | 0,1 ml × 2 vị trí, ngày 0, 3, 7, 28 | 11 |
| RIG | HRIG 20 IU/kg; ngựa / F(ab')2 40 IU/kg | 12 |
| RIG, mốc thời gian | không chỉ định sau ngày thứ 7 kể từ liều đầu | 12 |
| Trước phơi nhiễm | 3 liều ngày 0, 7, 21 hoặc 28 | 9 |
| Người đã tiêm | có giấy tờ tiêm đủ trước hoặc sau phơi nhiễm → ngày 0 và 3, không RIG | 11 |
| Phân độ III | gồm "contamination of mucous membrane with saliva from licks, licks on broken skin" | 10 |

WHO 2018 tr.1 ghi rõ bản 2018 **thay thế** bản 2010.

**Hệ quả:**
- Dòng hạt giống 4 (IM 0-3-7-14-28) và 5 (ID 0-3-7-28) nên được mô tả là **lệch phiên bản** (Việt Nam = WHO 2010, đã bị WHO 2018 thay thế), đồng thời **xung đột** với WHO 2018 và Mỹ hiện hành.
- Câu trả lời "0-3-7-14" của mô hình **không** quy riêng cho Mỹ được. Nó khớp Mỹ hiện hành, WHO 2018 (liều 4 trong khoảng ngày 14–28) và cả WHO 2010 (phác đồ thay thế có điều kiện).
- Câu trả lời "0-3-7-14-28" khớp Việt Nam (biểu mẫu), WHO 2010, Mỹ cho người suy giảm miễn dịch, và nhãn nhà sản xuất.
- Hệ thống nhãn quy nguồn phải xử lý tình huống **một giá trị khớp nhiều nguồn**. Ghi vào kho `foreign_values` với `system = WHO_global`, `version_date = 2010-08-06`, cờ `superseded_by` là WHO 2018-04-20.

### 4.2 Ứng viên có giá trị ngay trong phần khuyến cáo của 1622, báo cáo bỏ sót

Cả năm ứng viên đều **chưa dựng mẩu được**, vì chưa có PDF. Văn bản Việt Nam dưới đây đọc từ bản .doc chính thức, **không** có số trang PDF. Phía nước ngoài đã grep bằng `vnsoc.match.sources`.

| # | Slot | Việt Nam (1622, mục) | Nước ngoài (đã grep) | Trạng thái dự kiến | Cần bác sĩ? |
|---|---|---|---|---|---|
| a | **Phân độ liếm trên da tổn thương / niêm mạc** | Bảng "Tóm tắt chỉ định" (3.3.2): **Độ II** gồm "liếm trên da bị tổn thương, niêm mạc". Nếu con vật bình thường thì chỉ tiêm vắc xin, dừng sau ngày thứ 10, **không RIG** | WHO 2018 tr.3: **Category III** gồm "contamination of mucous membrane or broken skin with saliva from animal licks". WHO 2010 tr.10: như vậy. Category III cần RIG (2018 tr.14, 2010 tr.10) | **Xung đột**, cả WHO 2010 và 2018 đều khác Việt Nam. Hệ quả lâm sàng lớn (không dùng RIG). Là ứng viên xung đột **mạnh nhất** của chủ đề | Có (HG3.9) |
| b | **Ngưỡng "đã tiêm phòng"** | 3.3.4: tiêm lại đủ phác đồ nếu "chưa đủ 3 mũi" vắc xin tế bào | WHO 2018 tr.14: người đã tiêm = có giấy tờ tiêm trước phơi nhiễm hoặc **≥ 2 liều** sau phơi nhiễm; trước phơi nhiễm 2018 chỉ 2 lần (ngày 0 và 7, tr.17). WHO 2010 tr.11 và tr.9: tiêm "đủ" trước phơi nhiễm = 3 liều | **Xung đột** với WHO 2018, **lệch phiên bản** khớp WHO 2010 | Có |
| c | Mốc 7 ngày của RIG | 3.3.3.2: "Không sử dụng huyết thanh kháng dại sau 7 ngày kể từ mũi tiêm vắc xin đầu tiên" | WHO 2018 tr.16; WHO 2010 tr.12; ACIP 2010 tr.8 | **Đối chứng** | Không |
| d | Theo dõi con vật 10 ngày | Bảng 3.3.2: "dừng tiêm sau ngày thứ 10" nếu con vật bình thường | WHO 2018 tr.15: 10-day observation (chó, mèo, chồn sương) | **Đối chứng**. Lưu ý Việt Nam áp dụng cho mọi động vật trong bảng, WHO chỉ cho chó/mèo/chồn sương | Không |
| e | Ngưỡng kháng thể để tiêm nhắc trước phơi nhiễm | 3.2: nhắc 1 liều khi kháng thể "dưới 0,5UI/ml" | WHO 2018 tr.18: <0.5 IU/ml. WHO 2010 tr.10: như vậy | **Đối chứng** (thuộc trước phơi nhiễm, ngoài phạm vi sau phơi nhiễm; chỉ dùng nếu mở rộng chủ đề) | Không |

Nếu có PDF hoặc được chấp nhận bản .doc, chủ đề dại có thể đủ chỉ tiêu (2 xung đột a, b và 1–2 đối chứng c, d) mà **không cần** dựa vào biểu mẫu phụ lục hay tờ HDSD. Vì vậy phương án (c) "loại dại khỏi thí điểm" của báo cáo là quá sớm.

### 4.3 Góc nhìn lâm sàng (AI đóng vai bác sĩ, không phải bác sĩ thật)

- Ứng viên (a) là khác biệt có ý nghĩa an toàn thật. Ở Việt Nam, câu hỏi thường gặp là "chó liếm vào vết xước / niêm mạc mắt". Theo 1622, nếu con vật bình thường thì không cần RIG. Theo WHO thì cần. Bác sĩ thật phải xác nhận cách đọc bảng 1622 (cột "Tình trạng động vật") trước khi dựng mẩu.
- Bảng 1622: Độ III "vết cắn/cào chảy máu ở vùng xa thần kinh trung ương", con vật bình thường → chỉ vắc xin, không RIG. WHO: Category III → vắc xin + RIG, nhưng WHO 2018 có mục ưu tiên RIG khi thiếu (tr.14–16). Đây là ứng viên xung đột thứ ba **có điều kiện**. Tôi chưa grep đủ phần ưu tiên RIG của WHO 2018 nên **không** đề xuất dựng mẩu cho điểm này nếu chưa có bác sĩ.
- 1622 (3.3.3.2): Độ II ở người ức chế miễn dịch "nên sử dụng" RIG. WHO 2010 tr.8 cũng khuyên RIG cho độ II ở người suy giảm miễn dịch, tức là đối chứng với bản cũ. Chưa kiểm WHO 2018 cho điểm này.

## 5. Đánh giá mục "Sai lệch so với bộ hạt giống" (§4 của báo cáo)

| Mục | Đánh giá | Sửa / bổ sung |
|---|---|---|
| 1. Dòng 4 không phải câu khuyến cáo | **Chính xác** | Đổi `status` đề xuất thành `unverified_needs_design_decision`. Nếu dựng từ biểu mẫu, ghi thêm `version_drift` so với WHO 2010 |
| 2. CDC {0,3,7,14} thuộc tập WHO 2018 | **Chính xác** | Bổ sung: cũng thuộc WHO 2010 (phác đồ thay thế có điều kiện, tr.11). Mỹ dùng {0,3,7,14,28} cho người suy giảm miễn dịch (ACIP 2010 tr.9), nên quần thể của mẩu phải loại trừ nhóm này |
| 3. Dòng 5 và mâu thuẫn nội bộ Việt Nam | **Chính xác** | Bổ sung: 0-3-7-28 = WHO 2010 TRC cập nhật; 0-3-7-28-90 = TRC gốc cũ hơn (tờ HDSD Rabipur). Phía WHO 2018 "phác đồ trong da 1 tuần" = 2-2-2-0-0 (tr.15, chú thích 73): hạt giống ghi đúng |
| 4. Không có đối chứng IU/kg | **Chính xác** | — |
| 5. Chưa kiểm WHO 2010 | **Đã giải quyết trong kiểm toán này** | WHO 2010 có đúng cả hai giá trị (xem §4.1). Giả thuyết "Việt Nam trùng bản WHO cũ" là **đúng** |

Tóm lại, hạt giống dòng 4–5 ghi `status: confirmed` là **không đúng như mô tả**, và dòng 4 thiếu đối chiếu WHO (cả 2010 lẫn 2018). Seed là đầu vào nên không sửa. Việc này đã ghi ở `docs/DECISIONS.md` (2026-09-26T13:00); nên bổ sung phát hiện WHO 2010 vào đó.

## Vấn đề chung

1. **Nút thắt chính: không có PDF chính thức của 1622/2014.** Mọi nguồn chính thức còn sống chỉ có .doc. Quy tắc hiện hành đòi "span nguyên văn + số trang PDF", nên không có đường tự động nào. Cần người dùng quyết định (HG), chọn một trong hai:
   - (i) Xin hoặc tìm PDF từ Cục Phòng bệnh, NIHE, Viện Pasteur, hoặc trang Sở Y tế khác.
   - (ii) Chấp nhận **bản .doc chính thức** (sha256 `feee9c61…`, vncdc.gov.vn) làm tệp nguồn. Khi đó định vị span bằng **số mục** (3.3.2, 3.3.3.2, 3.3.4) thay cho số trang PDF, vì số trang Word phụ thuộc máy render. Ghi `docs/DECISIONS.md` và addendum nếu đã đăng ký trước.

   Tôi **không** khuyến nghị tự chuyển .doc sang PDF rồi coi là "PDF chính thức".
2. **Thiếu URL** cho các khẳng định về văn bản thay thế (An Giang 2024, HCDC, tin Bộ Y tế 22/8/2026). Không kiểm lại được. Mọi khẳng định "vẫn hiện hành" cần kèm URL.
3. **Kiểm tính hiện hành chưa xong.** Hạn mức WebSearch đã hết (200/200) nên kiểm toán không quét thêm được. Việc kiểm "1622 có bị thay chưa" (đặc biệt sau khi thành lập Cục Phòng bệnh năm 2025) phải để HG1.2.
   - TT52/2025 (dự thảo, sẽ thay TT10/2024) chỉ liệt kê "Vắc xin dại, huyết thanh kháng dại" là sinh phẩm bắt buộc (tr.9), không có lịch tiêm.
   - Không PDF nào trong `data/raw` có chữ "vắc xin dại". "kháng dại" chỉ xuất hiện ở TT52/2025, không có lịch tiêm.
4. **Quy nguồn nhiều hệ thống.** Các lịch tiêm dại trùng nhau giữa WHO 2010, WHO 2018, Mỹ và nhãn nhà sản xuất. Quy tắc gán nhãn (`adopted_foreign` / `outdated_moh` / WHO bản cũ) phải xử lý "khớp nhiều nguồn" trước khi đóng băng. Nên kiểm trong `configs/grading.yaml` và skill counterpart-matching.
5. **Đề xuất mã trong báo cáo đã được thực hiện một phần.** `normalize_vi.py` đã có bí danh `iu/kg`, `ui/kg`, `đơn vị/kg`. `parse_schedules` đã xác định đơn vị cục bộ và đọc được "Ngày 0 Ngày 3 …". Dạng dấu chấm dẫn "N0……N3……" của phiếu điều tra **vẫn trả về rỗng** (tôi đã chạy thử). Đề xuất `seq_ranges` / `doses_per_visit` (ghi Zagreb 2-1-1 và "liều 4 trong khoảng ngày 14–28") vẫn chưa làm và vẫn cần.
6. Cache nước ngoài mới do kiểm toán tạo (qua công cụ dự án, không phải data/raw): `data/cache/foreign/d5b4bece75f78737291f.pdf` (WHO 2010 toàn văn).
