# Phản hồi hội đồng M1 (vòng 1, 26–27/9/2026)

Hội đồng (5 agent AI, không phải người): CẦN SỬA, điểm trung bình có trọng số 5,69; không lỗi chết người, không bác bỏ. M1 chỉ một vòng và không chặn việc nộp abstract (skill review-panel, mục 6).

## Đã sửa trước khi nộp abstract (manuscript/fmc/abstract_fmc.md → manuscript/build/fmc/abstract_fmc_vi.docx, _en.docx)

1. Bản tiếng Anh: số in theo định dạng tiếng Anh (dấu chấm thập phân) bằng `{{key|en}}` trong `vnsoc.numbers render` (không sửa tay); dòng đơn vị tiếng Anh (`affiliation_en` trong configs/project.yaml). Họ tên đầy đủ của tác giả: CHỜ người dùng cung cấp (không đoán).
2. "13 hướng dẫn hiện hành" → 65 khuyến cáo, 61 phân tích từ 12 văn bản còn hiệu lực (khóa mới pilot.n_atoms_analysed, pilot.n_guidelines_analysed).
3. "Mỗi khuyến cáo gắn … mồi" → "… (khi có)".
4. Báo cáo chọn lọc mồi → nêu cả trả lời ngắn và trắc nghiệm (pilot.mcq_a1_vi_foreign / _decoy / _n); kết luận "chưa thấy khuynh hướng theo chuẩn nước ngoài vượt mức trùng ngẫu nhiên".
5. Bỏ "rõ/clearly"; thêm kiểm định ghép cặp A1→A3 (McNemar chính xác; pilot.a1a3_vi_conflict_improved/_worsened/_p).
6. "Không có nguồn/unsourced" → "không khớp giá trị đối chiếu nào / matching no value in the reference set".
7. Thêm kết quả lệch phiên bản (pilot.a1_vi_drift_stale/_n) và mốc đối chứng A1 (pilot.a1_vi_concordant_correct/_n); nêu số câu bộ chấm xếp "không trả lời".
8. Độ chính xác bộ chấm tính trên câu trả lời ngắn (pilot.grader_short_*), "độc lập" → "hai lượt AI (Claude) kiểm riêng, mù, có trọng tài".
9. Mục tiêu: "phân loại mỗi lỗi theo nguồn" thay cho "truy mỗi lỗi".

## Chuyển thành việc cho nghiên cứu chính (task R1.*, không chặn gì)

- R1.1 Kiểm chéo khác họ mô hình: chuẩn tham chiếu và nhãn đều do Claude tạo và tự kiểm. Người dùng không kiểm tay được (làm một mình) → thêm một lượt kiểm bằng mô hình mở KHÁC HỌ chạy cục bộ trên mẫu ngẫu nhiên có seed, báo đồng thuận; ghi hạn chế trong bài.
- R1.2 Bộ chấm cho nghiên cứu chính: sửa các lỗi thí điểm phát hiện (nhãn 6 cho câu có giá trị ở mẩu cat/drugs; HA "140 mmHg / 90 mmHg", "140 90 mmHg"; drugs_cover bỏ qua thuốc thừa; biệt dược thiếu; mã lao cách nhau bằng dấu cách) và kiểm trên tập GIỮ RIÊNG không thuộc thí điểm, với ngưỡng đăng ký trước, TRƯỚC khi đóng băng.
- R1.3 Ngân sách tính toán trên laptop: đo lại thông lượng (num_ctx 2048/4096), dự báo giờ máy cho ma trận chính, áp DR6 (giảm mô hình/điều kiện) nếu vượt; ghi seed, num_ctx, done_reason vào RunRecord; ràng buộc đầu ra trắc nghiệm (thí điểm: nhiều câu trắc nghiệm bị cắt ở 128 token).
- R1.4 Ngày xuất hiện của từng giá trị nước ngoài so với ngày cắt dữ liệu của từng mô hình; chia tầng "xung đột riêng" / "xung đột một phần"; phương án thay thế có điều kiện không gán nhãn 4; tách nhãn 5 thành nhãn phụ (sai đơn vị, sai quy đổi…).
- R1.5 Addendum đăng ký trước: bản đăng ký chưa tải lên OSF trước khi mở đầu ra thí điểm; liệt kê mọi sửa dựa trên đầu ra thí điểm; loại mẩu thí điểm khỏi mẫu kiểm bộ chấm và khỏi RQ3.
- R1.6 Phạm vi bài: "mô hình mở chạy tại chỗ" (không có mô hình thương mại — quyết định của người dùng); đăng ký trước tỉ lệ lỗi quy được nguồn là kết cục chính cùng H1; kế hoạch diễn giải khi H1/H3 âm tính.
- R1.7 Đoạn A3 của P-controls-01..04 lấy lại từ QĐ 2131/2026 (văn bản mới) trước khi đóng băng câu hỏi; mồi được chấm độ hợp lý (decoy_plausible) bằng kiểm toán AI kép theo thang đăng ký trước.
