# Đơn đề nghị miễn xem xét đạo đức trong nghiên cứu

> **Ghi chú cho Bình Minh (xóa phần này trước khi nộp):**
> - Đơn này thuộc cổng **HG1.10**.
> - Nếu Trường có biểu mẫu chính thức, hãy chép nội dung dưới đây sang biểu mẫu đó. Không tự đặt số hiệu biểu mẫu.
> - Sửa dòng "Kính gửi" theo đúng tên hội đồng hoặc đơn vị mà giảng viên hướng dẫn chỉ (Claude không biết tên chính xác).
> - Bổ sung mã số sinh viên, họ tên và học vị của giảng viên hướng dẫn ở chỗ ký nếu biểu mẫu yêu cầu.
> - Nếu nộp vào ngày khác, sửa lại ngày ở cuối đơn.
> - Nộp kèm `project_onepager.md` (xuất ra PDF hoặc DOCX).

---

**CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM**
**Độc lập – Tự do – Hạnh phúc**

## ĐƠN ĐỀ NGHỊ MIỄN XEM XÉT ĐẠO ĐỨC TRONG NGHIÊN CỨU

**Kính gửi:** Hội đồng Đạo đức trong nghiên cứu của Trường

**Người đề nghị:** Bình Minh — sinh viên Khoa Công nghệ thông tin, Trường Đại học Tôn Đức Thắng (TDTU). Email: ngobinhminh2322006@gmail.com

**Người hướng dẫn:** giảng viên hướng dẫn của Khoa Công nghệ thông tin, ký xác nhận ở cuối đơn.

### 1. Tên đề tài

- Tiếng Việt: *Chuẩn điều trị của ai? Sai lệch theo chuẩn nước ngoài và theo phiên bản cũ của LLM so với hướng dẫn chuyên môn của Bộ Y tế Việt Nam*
- Tiếng Anh: *Whose Standard of Care? Jurisdictional Defaults, Guideline Staleness and Certified Abstention of LLMs on Vietnamese Ministry of Health Guidelines*

### 2. Thời gian thực hiện

Từ tháng 9/2026 đến tháng 1/2027.

### 3. Mục tiêu

Nghiên cứu đo mức độ các mô hình ngôn ngữ lớn (LLM) trả lời khác với hướng dẫn chẩn đoán và điều trị hiện hành của Bộ Y tế Việt Nam. Với mỗi câu trả lời sai, nghiên cứu truy xem giá trị đó đến từ hướng dẫn nước ngoài nào, hoặc từ bản Bộ Y tế cũ nào. Ngoài ra, nghiên cứu đánh giá một cơ chế cho phép mô hình từ chối trả lời, kèm chứng nhận thống kê về mức sai.

### 4. Thiết kế và nguồn dữ liệu

Đây là nghiên cứu đánh giá phần mềm, dựa hoàn toàn trên tài liệu và máy tính.

- **Văn bản Bộ Y tế:** các quyết định và thông tư hướng dẫn chuyên môn đã công bố công khai, tải từ nguồn chính thức (kcb.vn, moh.gov.vn, trang của Sở Y tế hoặc bệnh viện).
- **Hướng dẫn nước ngoài** (WHO, Mỹ, châu Âu/Anh): bộ dữ liệu chỉ ghi giá trị, tên nguồn và vị trí, không chứa đoạn văn.
- **Câu hỏi:** nhóm tự sinh câu hỏi từ các khuyến cáo trên. Tình huống lâm sàng là **giả định**, không lấy từ hồ sơ bệnh án hay từ người bệnh thật.
- **Đầu ra của mô hình:** gồm câu trả lời của các mô hình mở chạy trên máy chủ Kaggle và của một số mô hình thương mại gọi qua API. Dữ liệu gửi cho mô hình chỉ gồm văn bản công khai và câu hỏi do nhóm soạn, không có thông tin cá nhân.
- **Cách chấm:** câu trả lời được chấm tự động bằng quy tắc so giá trị đã đăng ký trước. Kết quả được báo cáo ở mức tổng hợp.

### 5. Căn cứ đề nghị miễn xem xét

1. **Không có người tham gia nghiên cứu.** Nghiên cứu không tuyển người tham gia; không phỏng vấn, khảo sát hay can thiệp trên người.
2. **Không có dữ liệu bệnh nhân hay dữ liệu cá nhân.** Nghiên cứu không dùng hồ sơ bệnh án, mẫu sinh phẩm hay bất kỳ thông tin nào định danh được một người.
3. **Chỉ dùng văn bản công khai và đầu ra của mô hình máy tính.**
4. **Bác sĩ không phải đối tượng nghiên cứu.** Các bác sĩ và dược sĩ lâm sàng (nếu nhận lời) tham gia với tư cách **đồng tác giả**, làm việc rà soát chuyên môn trên dữ liệu văn bản. Nhóm không thu thập dữ liệu về họ.
5. **Không phải công cụ điều trị.** Nghiên cứu không xây dựng hay triển khai công cụ kê đơn hoặc hỗ trợ quyết định trên người bệnh. Mọi sản phẩm đều ghi rõ "phục vụ nghiên cứu và đánh giá, không dùng để ra quyết định lâm sàng".

### 6. Cam kết

Em xin cam kết:

- Không thu thập dữ liệu người bệnh hoặc dữ liệu cá nhân. Nếu phạm vi nghiên cứu thay đổi theo hướng có người tham gia, em sẽ nộp hồ sơ xét duyệt đạo đức đầy đủ **trước khi** thực hiện phần đó.
- Chỉ dùng văn bản Bộ Y tế từ nguồn chính thức. Không phát hành lại toàn văn các văn bản. Với hướng dẫn nước ngoài có bản quyền, chỉ công bố giá trị và trích dẫn.
- Công bố việc sử dụng công cụ trí tuệ nhân tạo trong nghiên cứu và trong soạn thảo theo khuyến nghị của ICMJE và quy định của tạp chí. Công cụ AI không được ghi là tác giả.
- Trong bài báo, ghi rõ "trùng với Bộ Y tế" không đồng nghĩa với "đúng về y khoa". Các mục Bộ Y tế chậm hơn bằng chứng hiện nay sẽ được báo cáo riêng.
- Đăng ký trước kế hoạch phân tích trên OSF và báo cáo trung thực mọi kết quả, kể cả kết quả âm tính.

Kính mong Hội đồng xem xét và cấp xác nhận miễn xem xét đạo đức cho đề tài.

Em xin trân trọng cảm ơn.

Thành phố Hồ Chí Minh, ngày 26 tháng 9 năm 2026

| Xác nhận của giảng viên hướng dẫn | Người làm đơn |
| --- | --- |
| (ký và ghi rõ họ tên) | (ký và ghi rõ họ tên) |
| | Bình Minh |

**Tài liệu kèm theo:** trang tóm tắt dự án (`project_onepager`).
