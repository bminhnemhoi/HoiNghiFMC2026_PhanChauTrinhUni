# Chuẩn điều trị của ai? — Tóm tắt dự án

*Sai lệch theo chuẩn nước ngoài và theo phiên bản cũ của LLM so với hướng dẫn chuyên môn của Bộ Y tế Việt Nam*
Bình Minh — sinh viên Khoa Công nghệ thông tin, Trường Đại học Tôn Đức Thắng (TDTU) · ngobinhminh2322006@gmail.com · Cập nhật ngày 26/9/2026

> **Tài liệu phục vụ nghiên cứu, không dùng để ra quyết định lâm sàng.** Các giá trị trong bảng dưới đây mới được agent AI đối chiếu sơ bộ với PDF chính thức (26/9/2026), **chưa có người kiểm** và **chưa được bác sĩ nào duyệt**.

## Vấn đề

Khi được hỏi "theo hướng dẫn của Bộ Y tế", LLM vẫn có thể trả lời bằng giá trị của hướng dẫn nước ngoài hoặc bằng giá trị của bản Bộ Y tế đã bị thay thế. Câu trả lời như vậy nghe rất có cơ sở, nên người hỏi khó phát hiện.

Các nghiên cứu trước đã thấy LLM có "chuẩn mặc định" theo Mỹ (Wang & Suresh 2026; Bazerbachi et al., Eur Radiol 2026). Tuy vậy, trong những gì nhóm đã tìm (arXiv, Crossref; chưa tra hết PubMed và tạp chí y học Việt Nam), chưa thấy nghiên cứu nào truy từng câu trả lời sai về một nguồn có tên, ở mức giá trị (liều, ngưỡng, thuốc, lịch), cho một chuẩn quốc gia Đông Nam Á, bằng cả tiếng Việt và tiếng Anh.

## Câu hỏi nghiên cứu

- **RQ1 (chính):** khi câu hỏi nói rõ "theo Bộ Y tế", bao nhiêu phần trăm mẩu xung đột bị trả lời bằng giá trị nước ngoài hoặc giá trị của bản cũ?
  - **Giả thuyết H1:** trên mẩu xung đột, với câu hỏi tiếng Việt nói rõ "theo Bộ Y tế" và gộp các mô hình mở, tỉ lệ trùng giá trị nước ngoài cao hơn tỉ lệ trùng giá trị mồi.
- **RQ2:** khi được cung cấp ngữ cảnh (truy xuất tài liệu, hoặc đưa đúng đoạn hướng dẫn), sai lệch còn lại bao nhiêu?
- **RQ3:** tín hiệu bất đồng có dùng được để cho mô hình từ chối trả lời, kèm chứng nhận thống kê về mức sai, không?
- **RQ4:** sai lệch phân bố thế nào trên các câu tình huống đặt tại bệnh viện Việt Nam?

## Thiết kế

- **Dữ liệu:** 25–35 hướng dẫn Bộ Y tế hiện hành có PDF chính thức. Kho được đóng băng ngày 15/10/2026. Dự kiến trích được 2.000–3.500 mẩu khuyến cáo, mỗi mẩu khớp nguyên văn và có số trang. Mỗi mẩu được gắn giá trị của WHO, Mỹ, châu Âu/Anh và của bản Bộ Y tế cũ, kèm tên nguồn và ngày phiên bản.
- **Mô hình và điều kiện hỏi:** 4 LLM mở và một số LLM thương mại, hỏi bằng tiếng Việt và tiếng Anh, ở các điều kiện sau:

| Mã | Điều kiện hỏi |
| --- | --- |
| A0 | Không nói quốc gia |
| A1 | Nói rõ "theo hướng dẫn hiện hành của Bộ Y tế" (điều kiện xác nhận chính) |
| A2 | Có truy xuất trên kho Bộ Y tế |
| A3 | Đưa đúng đoạn hướng dẫn chứa đáp án |

- **Chấm điểm:** bằng quy tắc so giá trị (không dùng LLM để chấm). Mỗi câu trả lời nhận một trong **6 nhãn**, theo thứ tự ưu tiên:
  1. đúng và biết bối cảnh;
  2. đúng theo Bộ Y tế;
  3. lệch phiên bản;
  4. trùng chuẩn nước ngoài;
  5. không quy được nguồn;
  6. từ chối.
- **Giá trị mồi:** mỗi mẩu có một giá trị mồi. Giá trị này cùng loại và cùng đơn vị với đáp án, hợp lý như nhau, nhưng không thuộc nguồn nào. Mồi dùng để đo mức trùng ngẫu nhiên. Kết quả chính là phần vượt quá mức trùng ngẫu nhiên đó.
- **Minh bạch:** kế hoạch phân tích sẽ được đăng ký trước trên OSF (dự kiến đầu tháng 10/2026). Bộ câu hỏi và quy tắc chấm sẽ được đóng băng trước khi chạy mô hình.

## Một số xung đột hạt giống (trích từ đề cương §3.3, kèm kết quả đối chiếu sơ bộ ngày 26/9/2026)

| # | Mục | Bộ Y tế Việt Nam | Nước ngoài | Trạng thái sau đối chiếu sơ bộ (agent, chưa có người kiểm) |
| --- | --- | --- | --- | --- |
| 1 | Sốc dengue người lớn: tốc độ dịch đầu | Ringer lactat hoặc NaCl 0,9% 15 ml/kg/giờ, rồi 10 ml/kg/giờ × 2 giờ (QĐ 2760/QĐ-BYT 2023, mục C.2.1) | 5–10 ml/kg/giờ trong 1 giờ (WHO 2009) | **Còn là xung đột.** Giá trị Việt Nam có nguyên văn ở trang PDF 28. Phải đối chiếu thêm hướng dẫn arbovirus WHO 2025 |
| 4–5 | Dại: phác đồ sau phơi nhiễm | Tiêm bắp N0-3-7-14-28; trong da N0-3-7-28 (QĐ 1622/QĐ-BYT 2014) | Tiêm bắp 0-3-7-14 (CDC); trong da 1 tuần (WHO 2018) | **Chưa xác nhận.** Chưa lấy được PDF chính thức. Theo bản .doc chính thức, phần khuyến cáo giao lịch tiêm cho hướng dẫn của nhà sản xuất; chuỗi ngày chỉ có ở biểu mẫu phụ lục. Lịch 0-3-7-14 của CDC cũng nằm trong tập WHO 2018 |
| 6 | Tăng huyết áp: ngưỡng chẩn đoán đo tại phòng khám | ≥ 140/90 mmHg (QĐ 3192/QĐ-BYT 2010) | ≥ 130/80 (AHA/ACC 2025); ESC và WHO cũng 140/90 | **Còn là xung đột, chỉ với Mỹ.** Giá trị có ở 3192/2010 và QĐ 5904/QĐ-BYT 2019 (trang PDF 11) |
| 9 | Đái tháo đường: mục tiêu huyết áp | < 140/90; < 130/80 nếu có biến chứng thận hoặc nguy cơ cao (QĐ 5481/QĐ-BYT 2020) | < 130/80 nếu an toàn (ADA 2025) | **Không còn là xung đột.** QĐ 5904/QĐ-BYT 2019 (hiện hành) ghi mục tiêu < 130/80 cho người tăng huyết áp kèm đái tháo đường, nên < 130/80 nằm trong tập giá trị Việt Nam |
| 11 | Đái tháo đường: ngưỡng bắt đầu insulin sớm | A1C ≥ 9% hoặc glucose ≥ 300 mg/dL (QĐ 5481/QĐ-BYT 2020) | A1C > 10% hoặc glucose ≥ 300 mg/dL (ADA) | **Còn là xung đột** ở ngưỡng A1C. Giá trị Việt Nam có nguyên văn ở trang PDF 25 |
| 15 | Phản vệ: liều adrenalin cho trẻ khoảng 10 kg | 0,25 ml (250 µg) (TT 51/2017/TT-BYT) | 150 µg cho trẻ 6 tháng–6 tuổi (RCUK); 0,01 mg/kg (WAO) | **Nhiều khả năng không phải xung đột.** Giá trị TT 51/2017 đúng (bản quét, đọc bằng mắt), nhưng QĐ 3942/QĐ-BYT 2014 và QĐ 3312/QĐ-BYT 2015 vẫn đăng trên kcb.vn và ghi 0,01 mg/kg và 0,15 mg cho trẻ |
| 16 | Sốt rét *P. falciparum*: thuốc đầu tay | Pyronaridin–artesunat 3 ngày + primaquin (QĐ 3377/QĐ-BYT 2023) | Artemether–lumefantrin (CDC); WHO chấp nhận cả hai | **Nhiều khả năng loại.** Giá trị Việt Nam đúng, nhưng 3377/2023 có artemether–lumefantrin làm thuốc thay thế, nên khác biệt là thứ tự ưu tiên chứ không phải giá trị |
| 17 | Sốt rét *P. falciparum*, 3 tháng đầu thai kỳ | Quinin 7 ngày + clindamycin 7 ngày (QĐ 3377/QĐ-BYT 2023) | Artemether–lumefantrin (CDC) | **Cần quyết định.** 3377/2023 cho dùng artemether–lumefantrin khi không có quinin; WHO cũng khuyến cáo artemether–lumefantrin |
| 20 | Viêm gan B: chỉ định điều trị | HBV DNA > 2.000 IU/mL và ALT > giới hạn trên (30 nam, 19 nữ) (QĐ 1740/QĐ-BYT 2026) | ALT ≥ 2× giới hạn trên (35/25) và HBV DNA theo HBeAg (AASLD 2025) | **Không phải xung đột sạch.** Giá trị 1740/2026 đúng (trang PDF 18, 20), nhưng bản cũ 3310/2019 dùng giới hạn trên 35/25, trùng AASLD. Chỉ dùng để mô tả lệch phiên bản |
| 23 | Vắc-xin sởi: tuổi tiêm mũi đầu | 9 tháng tuổi (TT 10/2024/TT-BYT) | 12–15 tháng (CDC); WHO giống Việt Nam | **Giá trị đúng, văn bản chưa rõ.** "Đủ 9 tháng tuổi" có ở TT 52/2025 (trang PDF 7). TT 10/2024 đã bị TT 52/2025 thay; TT 52/2025 bị TT 13/2026 bãi bỏ, và theo bản quét TT 13/2026 không ghi lịch tiêm |

**Cách đọc bảng:**
- Cột trạng thái là kết quả đối chiếu sơ bộ với PDF chính thức do agent AI làm ngày 26/9/2026, chưa có người thật kiểm. Dòng 1, 6 và 11 vẫn là xung đột; dòng 23 đúng giá trị nhưng chưa rõ văn bản hiện hành; các dòng còn lại không còn là xung đột sạch hoặc chưa xác nhận được.
- Trước khi dùng cho nghiên cứu chính, mỗi dòng cần có đủ: trích nguyên văn ở cả hai phía, số trang trong PDF chính thức, quần thể áp dụng, và **chữ ký duyệt của bác sĩ**.
- Nhóm chỉ ghi giá trị và nguồn của hướng dẫn nước ngoài, không chép đoạn văn.

## Mốc thời gian

| Thời điểm | Việc |
| --- | --- |
| Trước 30/9/2026 | Nộp tóm tắt Hội nghị Khoa học FMC 2026 (thiết kế và thí điểm chọn tay) |
| Đầu tháng 10/2026 | Đăng ký trước trên OSF; mời bác sĩ đồng tác giả |
| 15/10/2026 | Đóng băng kho hướng dẫn |
| 22/10 – 4/11/2026 | Kiểm tra 100% mẩu xung đột; **bác sĩ duyệt**; đóng băng bộ câu hỏi |
| Tháng 11/2026 | Chạy mô hình, chấm điểm |
| 12/12/2026 | Hội nghị FMC 2026 |
| 11–24/1/2027 | Nộp JMIR Medical Informatics hoặc IJMI (JAMIA nếu có bác sĩ đồng tác giả) |

**Nghiên cứu này không làm những việc sau:**
- không xây công cụ kê đơn hay hỗ trợ quyết định lâm sàng;
- không đánh giá hướng dẫn nào đúng hơn, vì chuẩn tham chiếu là mức trung thành với hướng dẫn hiện hành của Bộ Y tế;
- không tuyên bố gì về nội dung đề thi quốc gia.

Nghiên cứu không có người tham gia và không dùng dữ liệu bệnh nhân.
