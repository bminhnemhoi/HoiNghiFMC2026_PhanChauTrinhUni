---
description: Họp hội đồng phản biện agent cho một mốc (M1–M4)
argument-hint: M1|M2|M3|M4
---
Nạp skill `review-panel` và thực hiện cho mốc **$ARGUMENTS**: gọi song song 5 agent rev-editor, rev-clinician, rev-methods, rev-feasibility, rev-novelty (mỗi agent đọc gói tài liệu của mốc, độc lập, không thấy báo cáo của nhau), tổng hợp điểm bằng quy tắc trong skill, ghi `review/$ARGUMENTS/summary.md`, tạo task sửa (`scripts/vs add --id R<n>.<k> ...`) cho mọi yêu cầu bắt buộc. Báo người dùng kết luận và yêu cầu lớn nhất.
