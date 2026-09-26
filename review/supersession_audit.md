# Kiểm toán độc lập chuỗi thay thế, danh tính và lớp chữ của kho chính (T2.5) — 27/9/2026

Người làm: agent **integrity-auditor (AI, Claude)**. Đây là kiểm tra của AI, **không phải người kiểm**. Tôi đọc lại từ PDF (lớp chữ qua `vnsoc.extract.verify_span`, hoặc đọc ảnh trang khi trang quyết định là ảnh), không dựa vào kết luận của agent trước (`review/supersession_check.md`).

Tôi không sửa `data/interim/manifest*`, `results/tables/supersession.csv` hay `configs/`. Tôi không mở `data/runs/` và không truy cập trang thư viện pháp luật tư nhân. Tôi không tắt kiểm chứng chỉ TLS.

**Trạng thái lúc kiểm.**
- HEAD `1ee53ed`. `data/interim/manifest.jsonl` có 85 dòng; 26 dòng `in_corpus=true`, cả 26 đều `status=current`.
- sha256 của 26 tệp PDF trong kho khớp manifest (có tính `pdf_choice.json`: 5904/2019 → `5904_2019__9e6bbe13.pdf`).
- Đang có trích mẩu nghiên cứu chính (`data/interim/atoms_parts/`: 1019/2025, 1840/2025, 1857/2022, 2892/2022).

**Tệp tải thêm để kiểm.** Các tệp này chỉ nằm trong scratchpad của phiên, không lưu vào repo.
- Bản quét ký số 1154/2024 (Google Drive do BVĐK Sa Đéc liên kết), sha256 `ea8043c0…`.
- Trang QĐ 3319/2017 trên kcb.vn, sha256 `ca840b6d…`.
- Bản 2699/2020 có trang QĐ trên benhvienhatrung.vn, sha256 `ebf4833d…`.
- Danh mục API công khai của kcb.vn: 1.793 mục, mới nhất 25/9/2026.
- Danh mục API công khai của BVĐK Bạc Liêu: 1.204 văn bản pháp quy, mới nhất 07/8/2026; 100 tin mới nhất tới 22/9/2026.
- Trang bvtn.org.vn (đột quỵ, lao) và trang syt.gialai.gov.vn (678/2025).

## 1. Kết luận

**KHÔNG ĐẠT — chưa đóng được T2.5.** Chuỗi thay thế tự nó đúng, nhưng còn hai lỗi chặn về lớp chữ của văn bản trong kho, và bảng kết quả lệch với manifest.

| Hạng mục | Kết quả |
| --- | --- |
| Văn bản đã kiểm | 54 văn bản: 26 trong kho, 27 văn bản bị thay/bị bãi bỏ một phần nối với kho, và 2323/2025 (câu hỏi số hiệu) |
| Quan hệ đã kiểm | 39 quan hệ: **36 xác nhận** (3 quan hệ trong số này có bằng chứng nằm ngoài `data/raw`), **0 sai**, **3 không xác minh được** (4562/2018 bị thay; 2760/2021 bị 162/2024 thay; số hiệu "2760/2021") |
| Hiệu lực tới 27/9/2026 | Cả 26 văn bản trong kho **không bị văn bản nào thay** — theo điều khoản của 85 PDF trong danh mục, toàn bộ danh mục kcb.vn và danh mục BVĐK Bạc Liêu. Không xác nhận được cho 28/9–15/10. |
| Danh tính | 26/26 đúng văn bản ghi tên. 22 tệp có đủ QĐ + hướng dẫn. 1154/2024, 3192/2010, 678/2025 (tệp HD) không có trang QĐ trong `data/raw`. 1353/2021 là QĐ sửa đổi 1 trang. **Bốn văn bản không in số/ngày trong tệp:** 162/2024, 3312/2024, 678/2025 (trong kho) và 2323/2025 (ngoài kho). |
| Lớp chữ | **2 văn bản lỗi nặng:** 6101/2019 (không dùng được), 162/2024 (1.333 ký tự Kirin). Nhiều văn bản khác có lỗi nhỏ (§6). |

**Lỗi chặn**

| Mã | File / vị trí | Lỗi | Tái hiện |
| --- | --- | --- | --- |
| L1 | `data/raw/6101_2019.pdf` (trong kho), sidecar `data/interim/ocr/6101_2019/meta.json` (`"override_text_layer": false`) | Lớp chữ là OCR cũ mất dấu, dạng "Di~u 1. Ban hanh kern theo Quyet dinh" (tỷ lệ chữ có dấu 0,3%). Sidecar OCR 26/9 có đủ 6 trang nhưng không bao giờ được dùng: `verify_span._resolved` chỉ thay trang khi lớp chữ < 200 ký tự hoặc có `override_text_layer`, mà mọi trang đều > 1.000 ký tự. Vì vậy không span tiếng Việt nào kiểm được. D28 lại đang tính 6101 là "văn bản OCR". | `$PY -m vnsoc.extract.verify_span --find 6101/2019 "điều trị"` → `[]`. Kết quả cũng là 0/6 trang với "với", "người bệnh", "ngày". |
| L2 | `data/raw/162_2024.pdf` (trong kho, tầng 1) | Lớp chữ dùng ký tự Kirin thay chữ Việt: `ӟ` (U+04DF) thay "ớ", 1.102 lần; `ү` (U+04AF) thay "ẫ", 231 lần. Lỗi có trên 182/213 trang ("vӟi", "dưӟi", "Hưӟng dүn", "mүu", "lӟn"). `verify_span.norm()` (`_GLYPH`, dòng 34–36) không chuẩn hóa hai ký tự này. Hệ quả: span gõ đúng chính tả không khớp; span chép nguyên văn lại mang ký tự Kirin vào dữ liệu. **Đã xảy ra** ở `data/interim/pilot_atoms.jsonl` dòng 59, 60, 61, 65 (P-tbhiv-01, -02, -03, -07). | `--find 162/2024 "với"` → chỉ 20/213 trang có "với", trong khi "vӟi" xuất hiện 481 lần. Kiểm span: `grep -n '"162/2024"' data/interim/pilot_atoms.jsonl`. |
| L3 | `results/tables/supersession.csv` cột `in_corpus`; `review/supersession_check.md` §6 | Cột `in_corpus` vẫn là bộ 35 văn bản cũ, **lệch manifest ở 19 dòng**: 493/2026, 3510/2025, 2671/2023, 2959/2023, 1768/2026, 3908/2023, 2248/2023, 1530/2023, 465/2024, 3651/2024, 2989/2026, 2323/2025, TT13/2026, 1760/2024 ghi True nhưng manifest False; 6101/2019, 3610/2015, 1857/2022, 2855/2024, 1353/2021 ghi False nhưng manifest True. Các cột trạng thái và quan hệ thì khớp manifest 85/85. | So `csv.DictReader(results/tables/supersession.csv)` với `manifest.jsonl` theo `doc_key`. |

**Rủi ro với khoảng đăng ký trước.** `configs/project.yaml` đặt `n_current_guidelines: [25, 35]`. Con số 26 hiện tại tính cả 1353/2021 (QĐ sửa đổi 1 trang, không phải một hướng dẫn) và 6101/2019 (chưa dùng được). Không tính hai văn bản này thì còn **24**, dưới ngưỡng 25.

## 2. Cách làm (tái hiện được)

1. **Trang quyết định.** Với mỗi văn bản, tôi in trang 1–4 bằng `page_texts()` của `vnsoc.extract.verify_span` (có dùng sidecar OCR). Khi trang QĐ là ảnh hoặc lớp chữ hỏng, tôi dựng ảnh trang (PyMuPDF, 90–110 dpi) và đọc bằng mắt: 1019/2025 tr.1, 3312/2024 tr.1, 2855/2024 tr.1–2, 3610/2015 tr.2, 5904/2019 (bản chọn) tr.1, 1857/2022 tr.1, 6101/2019 tr.1, TT51/2017 tr.1, 4562/2018 tr.4, 4263/2015 tr.2, 3126/2018 tr.1, 3310/2019 (`__c43006cb`) tr.2, 4845/2016 tr.1–2, 458/2011 tr.1, 1154/2024 tr.1 (bản ký số ngoài repo), 3319/2017 (trang QĐ trên kcb.vn).
   - Tái hiện: `$PY -m vnsoc.extract.verify_span --page <KEY> <PAGE>` và `--image <KEY> <PAGE>`.
2. **Văn bản mới hơn trong 85 PDF.** Tôi quét 6 trang đầu của mọi PDF trong `data/raw/` tìm cụm "thay thế/bãi bỏ/hết hiệu lực/sửa đổi" kèm số QĐ/TT. Văn bản duy nhất nêu tên một văn bản trong kho là 1353/2021 (sửa 5481/2020).
   - Không PDF nào nêu 4562/2018 trong điều khoản.
   - "QĐ 2760 của BYT" chỉ xuất hiện ở 162/2024 tr.201, dưới dạng dẫn sơ đồ, không phải điều khoản.
   - TT51/2017 chỉ được dẫn như văn bản đang áp dụng: 162/2024 tr.100 và 3651/2024 tr.70, 74.
3. **Văn bản mới hơn trên mạng.**
   - kcb.vn: tải toàn bộ API `api/Content/Article/selectAll` (News 1.182, Download 171, LegalDocument 440; mới nhất 25/9/2026). Lọc theo tên bệnh và theo số QĐ của 26 văn bản: không có văn bản thay thế.
   - Công văn hỏa tốc của Bộ Y tế ngày 31/3/2026 (kcb.vn) còn dẫn "Quyết định số 292/QĐ-BYT ngày 06/2/2024" là hướng dẫn tay chân miệng đang áp dụng.
   - BVĐK Bạc Liêu: 1.204 văn bản pháp quy — không có văn bản thay thế.
   - Hai QĐ 1986/QĐ-BYT và 2149/QĐ-BYT năm 2026 sửa "hiệu lực thi hành" nhưng chỉ áp dụng cho **Hướng dẫn quy trình kỹ thuật**, không phải hướng dẫn chẩn đoán–điều trị.
   - Không kiểm được: moh.gov.vn (ứng dụng JS, HTML trống); vbpl.vn (JS); vaac.gov.vn, vncdc.gov.vn, emohbackup.moh.gov.vn (curl lỗi TLS 35); impe-qn.org.vn (lỗi chứng chỉ 60).
4. **Chất lượng lớp chữ.** Với mỗi văn bản có lớp chữ, tôi đếm ký tự Kirin, ký tự PUA, U+FFFD, glyph ƣ, dấu "~" giữa chữ và tỷ lệ chữ có dấu. Tôi xem 3 trang ngẫu nhiên (seed 20260927) và thử `find_pages` với 8 từ thông dụng (§6).

## 3. Văn bản trong kho (26) — mỗi văn bản một bảng

Quy ước: "tr." là trang PDF (1-based). Trích ≤ 150 ký tự, đúng nguyên văn của lớp chữ/OCR (kể cả lỗi OCR); khi đọc ảnh thì ghi "(ảnh)". "Hiệu lực" là tình trạng tới 27/9/2026.

### 1019/2025 — Sởi
| Mục | Kết luận | Bằng chứng |
| --- | --- | --- |
| Danh tính | Đúng. QĐ + HD đầy đủ, 21 tr. | tr.1 (ảnh): "Số: 1019/QĐ-BYT" · "Hà Nội, ngày 26 tháng 3 năm 2025" (số, ngày viết tay; sao y ký số 26-03-2025) |
| Hiệu lực | Hiện hành | Không có văn bản thay thế (xem §2 mục 2–3) |
| Thay 1327/2014 | **Xác nhận** | tr.1 (ảnh) Đ3: "Quyết định này thay thế Quyết định số 1327/QĐ-BYT ngày 18 tháng 4 năm 2014 của Bộ trưởng Bộ Y tế" |
| Lớp chữ | Tốt (tr.2–21). Tr.1 chỉ có ảnh, không có sidecar (không cần cho mẩu). | Mẫu tr.10, 13, 18 sạch; 61 ký tự PUA đầu dòng |

### 1154/2024 — THA thai kỳ, tiền sản giật, sản giật
| Mục | Kết luận | Bằng chứng |
| --- | --- | --- |
| Danh tính | Đúng; HD đầy đủ, 33 tr. (có tài liệu tham khảo). **Không có trang QĐ trong `data/raw`.** | tr.1 bìa (chữ đỏ): "Ban hành theo Quyết định số 1154 /QĐ-BYT ngày ..04.. tháng ..5... năm 2024" |
| Hiệu lực | Hiện hành | Không có văn bản thay thế |
| Thay 1911/2021 | **Xác nhận**, bằng tệp ngoài repo | Bản ký số (Drive, sha256 `ea8043c0…`) tr.1 (ảnh) Đ3: "…có hiệu lực kể từ ngày ký, ban hành và thay thế Quyết định số 1911/QĐ-BYT ngày 19 tháng 4 năm 2021" |
| Lớp chữ | Tốt | Mẫu tr.4, 5, 17 sạch; 140 ký tự PUA U+F02B (dấu đầu dòng) |

### 1353/2021 — Sửa đổi HD ĐTĐ típ 2 (1 trang)
| Mục | Kết luận | Bằng chứng |
| --- | --- | --- |
| Danh tính | Đúng. Đây là **QĐ sửa đổi, không phải hướng dẫn**. Số/ngày lấy từ tem. | tr.1: "Số: /QĐ-BYT" để trống; tem cuối trang "1353 23 02" |
| Hiệu lực | Hiện hành | Không văn bản nào sửa tiếp |
| Sửa một phần 5481/2020 | **Xác nhận** | tr.1 Đ1: "Sửa đổi, bổ sung một số nội dung của “Hướng dẫn chẩn đoán và điều trị đái tháo đường típ 2” được ban hành tại Quyết định số 5481/QĐ-BYT" |
| Ghi chú | Câu bị sửa nằm ở 5481/2020 tr.39 (điểm b): "insulin trộn không được khuyến cáo sử dụng thường quy". Mọi mẩu lấy từ câu này phải dùng bản sửa của 1353/2021. | — |

### 1470/2024 — ĐTĐ thai kỳ (bản quét, OCR)
| Mục | Kết luận | Bằng chứng |
| --- | --- | --- |
| Danh tính | Đúng; QĐ + HD, 31 tr. | tr.1 (OCR): "Số: 1470 /QD-BYT Hà Nội, ngày 29 tháng 5 năm 2024" |
| Hiệu lực | Hiện hành | — |
| Thay 6173/2018 | **Xác nhận** | tr.1 (OCR) Đ3: "…hiệu lực kê từ ngày ký, ban hành và thay thể Quyét định số 6173/QD-BYT ngày 12 tháng 10 năm 2018" |
| Lớp chữ | Bản quét; OCR đủ 31 tr. OCR có lỗi dấu ("Ba mẹ", "QUYET") → giá trị phải kiểm bằng ảnh. | — |

### 162/2024 — Lao
| Mục | Kết luận | Bằng chứng |
| --- | --- | --- |
| Danh tính | Đúng nội dung; HD đầy đủ, 213 tr. **Tệp không in số và ngày.** | tr.1: "Số: /QĐ-BYT … ngày tháng năm 2024". Số "162" có ở danh mục BVĐK Bạc Liêu ("Quyết định 162/QĐ-BYT…", đăng 19/01/2024) và trang bvtn.org.vn. |
| Hiệu lực | Hiện hành | — |
| Thay 1314/2020 | **Xác nhận** | tr.1 Đ3: "Quyết định này có hiệu lực kể từ ngày ký, ban hành và thay thế Quyết định số 1314/QĐ-BYT ngày 24/03/2020" |
| Lớp chữ | **KHÔNG ĐẠT (L2)** — 1.333 ký tự Kirin trên 182/213 trang | Mẫu tr.29 (24 ký tự lạ), tr.95 (10), tr.180 (3): "tӟi phác đồ" |
| Ghi chú | Tệp đã qua Ghostscript (tạo 01/02/2026), không phải bản ký số nguyên vẹn. | metadata `producer: GPL Ghostscript 10.06.0` |

### 1740/2026 — Viêm gan B
| Mục | Kết luận | Bằng chứng |
| --- | --- | --- |
| Danh tính | Đúng; QĐ + HD, 42 tr. | tr.1 tem "1740 16 6"; kcb.vn tin 17/6/2026 "Quyết định 1740/QĐ-BYT" |
| Hiệu lực | Hiện hành | — |
| Thay 3310/2019 | **Xác nhận** | tr.1 Đ3: "Quyết định này thay thế Quyết định số 3310/QĐ-BYT ngày 29/7/2019 của Bộ trưởng Bộ Y tế" |
| Lớp chữ | Tốt | Mẫu tr.6, 13, 21 sạch |

### 1840/2025 — Cúm mùa
| Mục | Kết luận | Bằng chứng |
| --- | --- | --- |
| Danh tính | Đúng; QĐ + HD, 12 tr. Tr.4 ghi nhầm tiêu đề ban biên soạn "BỆNH SỞI" (lỗi văn bản gốc; danh sách người khác danh sách của 1019/2025). | tr.1 tem "1840 03 6" |
| Hiệu lực | Hiện hành | — |
| Thay 2078/2011 | **Xác nhận** | tr.1 Đ3: "Quyết định này thay thế Quyết định số 2078/QĐ-BYT ngày 23/6/2011 của Bộ trưởng Bộ Y tế" |
| Lớp chữ | Tốt | Mẫu tr.6, 9, 12 sạch |

### 1857/2022 — Suy tim
| Mục | Kết luận | Bằng chứng |
| --- | --- | --- |
| Danh tính | Đúng; QĐ + HD, 27 tr. | tr.1 (ảnh): "Số: 1857 /QĐ-BYT" · "ngày 05 tháng 7 năm 2022" |
| Hiệu lực | Hiện hành | — |
| Thay 1762/2020 | **Xác nhận** | tr.1 (ảnh) Đ3: "…có hiệu lực kể từ ngày ký, ban hành và thay thế Quyết định số 1762/QĐ-BYT ngày 17 tháng 04 năm 2020" |
| Lớp chữ | Tốt từ tr.2. Tr.1 có lớp OCR cũ mất dấu, nhưng chỉ là trang QĐ. | Mẫu tr.6, 10 sạch |

### 2131/2026 — COPD
| Mục | Kết luận | Bằng chứng |
| --- | --- | --- |
| Danh tính | Đúng; QĐ + HD, 130 tr. | tr.1 tem "2131 14 7" |
| Hiệu lực | Hiện hành | — |
| Thay 2767/2023 | **Xác nhận** | tr.1 Đ3: "…có hiệu lực kể từ ngày ký, ban hành và thay thế Quyết định số 2767/QĐ-BYT ngày 04 tháng 07 năm 2023" |
| Lớp chữ | Tốt | Mẫu tr.46, 70, 111 sạch |

### 2147/2026 — Viêm phổi cộng đồng người lớn
| Mục | Kết luận | Bằng chứng |
| --- | --- | --- |
| Danh tính | Đúng; QĐ + HD, 93 tr. | tr.1 tem "2147 15 7"; kcb.vn 23/7/2026 |
| Hiệu lực | Hiện hành | — |
| Thay 4815/2020 | **Xác nhận** | tr.1 Đ3: "…có hiệu lực kể từ ngày ký, ban hành và thay thế Quyết định số 4815/QĐ-BYT ngày 20 tháng 11 năm 2020" |
| Lớp chữ | Tốt | Mẫu tr.27, 80, 82 sạch |

### 2388/2024 — Bệnh thận mạn
| Mục | Kết luận | Bằng chứng |
| --- | --- | --- |
| Danh tính | Đúng; QĐ + HD, 192 tr. | tr.1 tem "2388 12 8" |
| Hiệu lực | Hiện hành | — |
| Bãi bỏ một phần 3931/2015 | **Xác nhận** | tr.1 Đ3: "Bãi bỏ bài “Bệnh thận đái tháo đường”, “Bệnh thận IgA”, “Viêm thận Lupus”, “Bệnh thận mạn” trong … Quyết định số 3931/QĐ-BYT" |
| Lớp chữ | Tốt. Có ký tự PUA U+F061 (α) ở tr.75, 161, 173. | Mẫu tr.5, 132, 167 sạch |

### 2760/2023 — Sốt xuất huyết Dengue
| Mục | Kết luận | Bằng chứng |
| --- | --- | --- |
| Danh tính | Đúng; QĐ + HD, 104 tr. | tr.1 tem "2760 04 … 7" và "Ngày ký: 04-07-2023" |
| Hiệu lực | Hiện hành | — |
| Thay 3705/2019 | **Xác nhận** | tr.1 Đ1: "…thay thế “Hướng dẫn chẩn đoán và điều trị Sốt xuất huyết Dengue” ban hành kèm theo Quyết định số 3705/QĐ-BYT ngày 22/8/2019" |
| Lớp chữ | Tốt | Mẫu tr.10, 20, 71 sạch |

### 2855/2024 — Viêm gan C (bản quét)
| Mục | Kết luận | Bằng chứng |
| --- | --- | --- |
| Danh tính | Đúng; QĐ + HD, 33 tr. | tr.1 (ảnh): "Số 2855/QĐ-BYT" · "ngày 25 tháng 9 năm 2024"; tr.2 (ảnh) bìa cùng số, ngày |
| Hiệu lực | Hiện hành | — |
| Thay 2065/2021 | **Xác nhận** | tr.1 (ảnh) Đ1: "…thay thế “Hướng dẫn chẩn đoán và điều trị bệnh viêm gan vi rút C” ban hành kèm theo Quyết định số 2065/QĐ-BYT ngày 29/04/2021" |
| Lớp chữ | Bản quét. Sidecar OCR hoàn tất trong lúc tôi kiểm (meta 27/9, 33 tr.). Manifest vẫn ghi `ocr=false`, `text_layer=false`. | — |

### 2892/2022 — Béo phì
| Mục | Kết luận | Bằng chứng |
| --- | --- | --- |
| Danh tính | Đúng; QĐ + HD, 28 tr. | tr.1 tem "2892 22 10", "Ngày ký: 22-10- 2022" |
| Hiệu lực | Hiện hành | — |
| Bãi bỏ một phần 3879/2014 | **Xác nhận** | tr.1 Đ3: "Bãi bỏ bài “Bệnh béo phì” trong “Hướng dẫn chẩn đoán và điều trị bệnh nội tiết – chuyển hóa” được ban hành tại Quyết định số 3879/QĐ-BYT" |
| Lớp chữ | Tốt (sạch nhất kho) | Mẫu tr.8, 11, 21 |

### 292/2024 — Tay chân miệng (bản quét, OCR)
| Mục | Kết luận | Bằng chứng |
| --- | --- | --- |
| Danh tính | Đúng; QĐ + HD, 24 tr. | sidecar OCR p001: "Số: 292 /QĐ-BYT Hà Nội, ngày 06 tháng 02 năm 2024" |
| Hiệu lực | Hiện hành. Công văn hỏa tốc Bộ Y tế 31/3/2026 (kcb.vn) còn dẫn QĐ 292/QĐ-BYT ngày 06/2/2024. | — |
| Thay 1003/2012 | **Xác nhận** | tr.1 (OCR): "…thay thế “Hướng dẫn chẩn đoán và điều trị bệnh tay chân miệng” ban hành kèm theo Quyết định số 1003/QĐ-BYT ngày 30/3/2012" |
| Lớp chữ | Bản quét; OCR tr.2–24. Tr.1 không dùng sidecar vì lớp chữ ký số dài 225 ký tự (> 200), nhưng tr.1 là trang QĐ. | — |

### 3192/2010 — Tăng huyết áp
| Mục | Kết luận | Bằng chứng |
| --- | --- | --- |
| Danh tính | Đúng tên, 19 tr. **Chỉ có phần HD, không có trang QĐ.** Đây là bản Word xuất PDF, không ký số (tạo 22/8/2012, tác giả "YEN"). | tr.1: "(Ban hành kèm theo Quyết định số 3192/QĐ-BYT ngày 31 tháng 08 năm 2010 của Bộ trưởng Bộ Y tế)" |
| Hiệu lực | **Không xác nhận được bằng điều khoản.** Không đọc được điều khoản của chính văn bản. Không thấy văn bản THA mới hơn (kcb.vn, BVĐK Bạc Liêu, 85 PDF). | Trang kcb.vn ghi "Đã có hiệu lực" (nghĩa là đã tới ngày hiệu lực, không phải "còn hiệu lực"). API kcb.vn ghi `statusEffective: "Hết hiệu lực"`, nhưng giá trị này có ở 426/440 văn bản cũ → không dùng được làm bằng chứng. |
| Quan hệ | Không có | — |
| Lớp chữ | Tốt. **Lỗi nội dung ở tr.2 (Bảng 2):** "Tăng huyết áp độ 1 … 140 – 150", "90 – 99 110 – 109", mâu thuẫn Bảng 3 cùng trang ("140-159", "100-109"). | Mẫu tr.2, 7, 17 |

### 3312/2024 — Đột quỵ não
| Mục | Kết luận | Bằng chứng |
| --- | --- | --- |
| Danh tính | Đúng nội dung; QĐ + HD, 148 tr. **Tệp không in số và ngày.** | tr.1 (ảnh): "Số: /QĐ-BYT" · "Hà Nội, ngày tháng năm 2024". Trang bvtn.org.vn (nơi đăng đúng tệp này): "Quyết định số 3312/QĐ-BYT của Bộ Y tế ngày 05/11/2024". Ngày tạo tệp 2024-11-05. |
| Hiệu lực | Hiện hành | — |
| Thay 5331/2020 | **Xác nhận** | tr.1 (ảnh) Đ3: "…có hiệu lực kể từ ngày ký, ban hành và thay thế Quyết định số 5331/QĐ-BYT ngày 23 tháng 12 năm 2020" |
| Lớp chữ | Tốt (190 ký tự PUA đầu dòng) | Mẫu tr.12, 17, 33 |

### 3377/2023 — Sốt rét (bản quét, OCR)
| Mục | Kết luận | Bằng chứng |
| --- | --- | --- |
| Danh tính | Đúng; QĐ + HD, 23 tr. | tr.1 (OCR): "Số: 3377 /QĐ-BYT Hà Nội, ngày 30 tháng 8 năm 2023" |
| Hiệu lực | Hiện hành | — |
| Thay 2699/2020 | **Xác nhận** | tr.1 (OCR) Đ1: "…thay thê hướng dân chân đoán, điêu trị bệnh Sôt rét ban hành kèm Quyêt định sô 2699/QĐ-BYT ngày 26 tháng 06 nam 2020" |
| Lớp chữ | Bản quét; OCR đủ; lỗi dấu OCR nhiều → giá trị phải kiểm bằng ảnh | — |

### 3610/2015 — Ngộ độc
| Mục | Kết luận | Bằng chứng |
| --- | --- | --- |
| Danh tính | Đúng; QĐ (ảnh tr.2) + HD, 228 tr. | tr.2 (ảnh): "Số: 3610 /QĐ-BYT" · "Hà Nội, ngày 31 tháng 8 năm 2015" |
| Hiệu lực | Hiện hành. Điều khoản của chính văn bản: chỉ hiệu lực, không thay văn bản nào. Không thấy văn bản mới hơn. | tr.2 (ảnh) Đ3: "Quyết định này có hiệu lực kể từ ngày ký ban hành." |
| Quan hệ | Không có | — |
| Lớp chữ | Dùng được sau chuẩn hóa: 2.843 ký tự ƣ, đã được `norm()` đổi thành ư | Mẫu tr.108, 182, 184 |

### 5481/2020 — ĐTĐ típ 2
| Mục | Kết luận | Bằng chứng |
| --- | --- | --- |
| Danh tính | Đúng; QĐ + HD, 77 tr. | tr.1 tem "5481 30 12" |
| Hiệu lực | Hiện hành, **đã bị sửa một phần** bởi 1353/2021 (tr.39, điểm b) | — |
| Thay 3319/2017 | **Xác nhận** | tr.1 Đ3: "…có hiệu lực kể từ ngày ký, ban hành và thay thế Quyết định số 3319/QĐ-BYT ngày 19/07/2017" |
| Lớp chữ | Tốt (ký tự PUA α, →) | Mẫu tr.6, 18, 37 |

### 5642/2015 — Một số bệnh truyền nhiễm
| Mục | Kết luận | Bằng chứng |
| --- | --- | --- |
| Danh tính | Đúng. Sách NXB Y học 2016, **phần 1**: QĐ ở tr.3, 14 chương, trang sách 13–86. Phần phụ lục in lại các QĐ khác (dengue, sởi, viêm gan…) không có trong tệp — đúng như mong muốn. | tr.3: "Số: 5642/QĐ-BYT … Hà Nội, ngày 31 tháng 12 năm 2015" |
| Hiệu lực | Hiện hành (không văn bản nào nêu tên). **Nhưng chương 8 "Bệnh cúm mùa" (tr. sách 49) và chương 5 "Bệnh sốt rét kháng thuốc" (tr.33) trùng chủ đề với văn bản mới hơn 1840/2025 và 3377/2023**; hai văn bản này không bãi bỏ các chương đó. | tr.3 Đ3: "Quyết định này có hiệu lực kể từ ngày ký ban hành." |
| Quan hệ | Không có | — |
| Lớp chữ | Tốt. 446 ký tự PUA; U+F0B0 (°) ở tr.44: "39 - 40[U+F0B0]C" (không đọc được thành °C). | Mẫu tr.9, 46, 83 |

### 5904/2019 — BKLN tại trạm y tế xã (bản chọn `5904_2019__9e6bbe13.pdf`)
| Mục | Kết luận | Bằng chứng |
| --- | --- | --- |
| Danh tính | Đúng; tr.1 là ảnh QĐ có chữ ký, 5 phần đủ, 68 tr. Bản Word xuất PDF (tạo 06/01/2020), không ký số. | tr.1 (ảnh): "Số: 5904/QĐ-BYT" · "ngày 20 tháng 12 năm 2019"; tr.2: "Ban hành kèm theo Quyết định số 5904/QĐ-BYT ngày 20 tháng 12 năm 2019" |
| Hiệu lực | Hiện hành. Trùng chủ đề với 3192/2010, 5481/2020, 2131/2026 (DR8). | — |
| Bãi bỏ một phần 2919/2014 | **Xác nhận** | tr.1 (ảnh) Đ3: "Bãi bỏ nội dung Phần 2 - Chẩn đoán và điều trị một số bệnh mạn tính thường gặp … tại Quyết định số 2919/ QĐ-BYT ngày 6/8/2014" |
| Lớp chữ | Dùng được: 168 ký tự ƣ được `norm()` xử lý. Mất chữ "Ư" đầu từ ở vài chỗ: tr.3 "ớc tính" ×3, "u tiên" ×1. | Mẫu tr.11, 14, 36 |

### 5968/2021 — HIV/AIDS
| Mục | Kết luận | Bằng chứng |
| --- | --- | --- |
| Danh tính | Đúng; QĐ + HD, 145 tr. | tr.1 tem "5968 31 12" |
| Hiệu lực | Hiện hành theo mọi nguồn đọc được. Không kiểm được vaac.gov.vn (lỗi TLS). | — |
| Thay 5456/2019 | **Xác nhận** | tr.1 Đ2: "Quyết định này có hiệu lực kể từ ngày ký, ban hành và thay thế Quyết định số 5456/QĐ-BYT ngày 20/11/2019" |
| Lớp chữ | Dùng được: 2.032 ký tự ƣ đã chuẩn hóa | Mẫu tr.29, 35, 57 |

### 6101/2019 — Whitmore
| Mục | Kết luận | Bằng chứng |
| --- | --- | --- |
| Danh tính | Đúng; QĐ + HD 5 tr. (kết thúc ở mục V, có chữ ký) | tr.1 (ảnh): "Số: 6101/QĐ-BYT" · "ngày 30 tháng 12 năm 2019" |
| Hiệu lực | Hiện hành | tr.1 (ảnh) Đ2: "Quyết định này có hiệu lực kể từ ngày ký, ban hành." |
| Quan hệ | Không có | — |
| Lớp chữ | **KHÔNG ĐẠT (L1)** | tr.1: "Di~u 1. Ban hanh kern theo Quyet dinh nay Hu6ng d~n chAn doan" |

### 678/2025 — Dự phòng lây truyền mẹ–con
| Mục | Kết luận | Bằng chứng |
| --- | --- | --- |
| Danh tính | Đúng nội dung. HD 26 tr. (`678_2025.pdf`) + trang QĐ 1 tr. (`678_2025__3241fdd5.pdf`). **Không tệp nào in số hoặc ngày.** | QĐ tr.1: "Số: /QĐ-BYT … ngày tháng năm 2025"; trang syt.gialai.gov.vn: "Quyết định số 678/QĐ-BYT [27/02/2025]"; ngày sửa tệp QĐ 26/02/2025 → **ngày chưa thống nhất (26 hay 27/02)** |
| Hiệu lực | Hiện hành. Trùng chủ đề với 5968/2021 (HIV mẹ–con) và 1740/2026 (HBV mẹ–con, mới hơn) — DR8. | — |
| Thay 2834/2019 | **Xác nhận** | `678_2025__3241fdd5.pdf` tr.1 Đ2: "…có hiệu lực thi hành kể từ ngày ký, ban hành và thay thế Quyết định số 2834/QĐ-BYT ngày 4/7/2019" |
| Lớp chữ | Tốt | Mẫu tr.4, 18, 21 |

### TT51/2017 — Phản vệ (bản quét, OCR)
| Mục | Kết luận | Bằng chứng |
| --- | --- | --- |
| Danh tính | Đúng; Thông tư đủ Phụ lục I–X, 20 tr. | tr.1 (ảnh): "Số: 51 /2017/TT-BYT" · "ngày 29 tháng 12 năm 2017" (OCR đọc "Số:b /2017") |
| Hiệu lực | **Chưa xác nhận bằng cơ sở dữ liệu pháp luật.** Không thấy thông tư thay thế trên kcb.vn và BVĐK Bạc Liêu. TT13/2026 Đ27 không nêu TT51. 162/2024 và 3651/2024 còn dẫn TT51. | vbpl.vn chạy JS nên không đọc được; API kcb.vn ghi "Hết hiệu lực" (giá trị mặc định, không tin được) |
| TT08/1999 hết hiệu lực | **Xác nhận** | tr.3 (OCR) Đ7 k2: "Thông tư số 08/1999/TT- BYT ngày 4 tháng 5 năm 1999 … hết hiệu lực kể từ ngày Thông tư này có hiệu lực thi hành" |
| Lớp chữ | Bản quét; OCR đủ | — |

## 4. Văn bản nối với kho (bị thay hoặc bị bãi bỏ một phần)

| Khóa | Trạng thái (csv) | Quan hệ → kết luận | Bằng chứng |
| --- | --- | --- | --- |
| 1327/2014 | superseded | thay 476/2009 → **xác nhận**; bị 1019/2025 thay → **xác nhận** | tr.1 (OCR) Đ2: "Bãi bd Quyết định số 476/QD- -BYT ngày 4/03/2009" |
| 1911/2021 | superseded | bị 1154/2024 thay → **xác nhận** (tệp ngoài repo); điều khoản của chính nó chỉ nói hiệu lực | `1911_2021__27810c20.pdf` tr.1 Đ2: "Quyết định này có hiệu lực kể từ ngày ký, ban hành." (tem "1911 19 04") |
| 6173/2018 | superseded | bị 1470/2024 thay → **xác nhận** | tr.2 Đ2: "Quyết định này có hiệu lực kể từ ngày ký, ban hành." |
| 1314/2020 | superseded | thay 3126/2018 → **xác nhận**; bị 162/2024 thay → **xác nhận**; `partially_amended_by` 2760/2021 → nội dung xác nhận, **số hiệu không xác minh được** | tr.1 Đ3: "…thay thế Quyết định số 3126/QĐ-BYT ngày 23 tháng 5 năm 2018" |
| 3126/2018 | superseded | thay 4263/2015 → **xác nhận**; bị 1314/2020 thay → **xác nhận** | `3126_2018.pdf` tr.1 (ảnh) Đ3: "…thay thế Quyết định số 4263/QĐ-BYT ngày 13 tháng 10 năm 2015" |
| 4263/2015 | superseded | thay 979/2009 → **xác nhận**; bị 3126/2018 thay → **xác nhận** | tr.2 (ảnh) Đ3: "…thay thế Quyết định số 979/QĐ-BYT ngày 24 tháng 3 năm 2009" |
| 2760/2021 | superseded (suy luận) | bị 162/2024 thay → **không xác minh được** (162/2024 Đ3 chỉ nêu 1314/2020). Về thực chất đã bị thay: 162/2024 có phần lao kháng thuốc riêng và tr.201 dẫn "(QĐ 2760 của BYT)". Tệp không có trang QĐ, không có chuỗi "2760". | tr.1: "Nội dung này thay cho các nội dung liên quan đến nguyên tắc và phác đồ điều trị lao kháng thuốc/ tài liệu phê duyệt tại quyết định số 1314/QĐ-BYT" |
| 3310/2019 | superseded | thay 5448/2014 → **xác nhận**; bị 1740/2026 thay → **xác nhận** | `3310_2019__c43006cb.pdf` tr.2 (ảnh) Đ2: "Bãi bỏ Quyết định số 5448/QĐ-BYT ngày 30/12/2014" |
| 5448/2014 | superseded | bị 3310/2019 thay → **xác nhận** | tr.1 Đ2: "Quyết định này có hiệu lực kể từ ngày ký, ban hành." |
| 2078/2011 | superseded | bị 1840/2025 thay → **xác nhận** | tr.1 Đ3: "Quyết định này có hiệu lực kể từ ngày ký ban hành." |
| 1762/2020 | superseded | bị 1857/2022 thay → **xác nhận** | tr.1 Đ3: "Quyết định này có hiệu lực kể từ ngày ký, ban hành." |
| 2767/2023 | superseded | thay 3874/2018 → **xác nhận**; bị 2131/2026 thay → **xác nhận** | tr.1 Đ3: "…thay thế Quyết định số 3874/QĐ-BYT ngày 26 tháng 06 năm 2018" |
| 3874/2018 | superseded | bị 4562/2018 thay → **xác nhận**; bị 2767/2023 thay → **xác nhận**. **Không có PDF của chính 3874:** `data/raw/3874_2018.pdf` cùng sha256 `68a2f132…` với `4562_2018.pdf`. | xem 4562/2018 và 2767/2023 |
| 4562/2018 | superseded (suy luận) | thay 3874/2018 → **xác nhận**; thay 2866/2015 → **xác nhận**; bị thay → **không xác minh được** (không văn bản nào nêu tên 4562) | tr.4 (ảnh + chữ) Đ3: "…thay thế Quyết định số 3874/QĐ-BYT ngày 26/6/2018 và Quyết định số 2866/QĐ-BYT ngày 8 tháng 7 năm 2015" |
| 4815/2020 | superseded | bị 2147/2026 thay → **xác nhận** | tr.1 Đ3: "Quyết định này có hiệu lực kể từ ngày ký, ban hành." (tem "4815 20 11") |
| 3931/2015 | partial | bị 2388/2024 bãi bỏ 4 bài → **xác nhận**. Tệp không có trang QĐ (bìa tr.1: "Quyết định số 3931/QĐ-BYT ngày 21/9/2015"). | xem 2388/2024 |
| 3705/2019 | superseded | thay 458/2011 → **xác nhận**; bị 2760/2023 thay → **xác nhận** | tr.1 (OCR) Đ2: "Bãi bỏ Quyêt định sô 458/QĐ-BYT ngày 16/02/2011" |
| 458/2011 | superseded | thay 794/2009 → **xác nhận** | tr.1 (ảnh) Đ3: "Quyết định này thay thế Quyết định số 794/QĐ-BYT ngày 09 tháng 3 năm 2009" |
| 2065/2021 | superseded | thay 5012/2016 → **xác nhận**; bị 2855/2024 thay → **xác nhận** | tr.1 Đ1: "…ban hành kèm theo Quyết định số 5012/Q-BYT ngày 20/9/2016" |
| 3879/2014 | partial | bị 2892/2022 bãi bỏ bài béo phì → **xác nhận**; bị 3319/2017 bãi bỏ phần ĐTĐ típ 2 → **xác nhận**, bằng tệp kcb.vn ngoài repo (sha256 `ca840b6d…`) | tr.3 Đ3 (của chính 3879): "Quyết định này có hiệu lực kể từ ngày ký ban hành." · 3319 QĐ (ảnh) Đ3: "Bãi bỏ nội dung “Hướng dẫn chẩn đoán và điều trị đái tháo đường típ 2” trong …" |
| 3319/2017 | superseded | bị 5481/2020 thay → **xác nhận**. `3319_2017.pdf` không có trang QĐ. | xem 5481/2020 |
| 5331/2020 | superseded | bị 3312/2024 thay → **xác nhận** | tr.1 Đ3: "Quyết định này có hiệu lực kể từ ngày ký, ban hành." (tem "5331 23 12") |
| 2699/2020 | superseded | thay 4845/2016 → **xác nhận** (bản benhvienhatrung.vn ngoài repo, sha256 `ebf4833d…`; `2699_2020.pdf` trong repo không có trang QĐ và để trống số); bị 3377/2023 thay → **xác nhận** | bản ngoài repo tr.1 Đ1: "…thay thế Hướng dẫn chẩn đoán, điều trị bệnh Sốt rét ban hành tại Quyết định số 4845/QĐ-BYT ngày 08/9/2016" |
| 4845/2016 | superseded | thay 3232/2013 → **xác nhận**; bị 2699/2020 thay → **xác nhận** | tr.1 (ảnh) Đ2: "Bãi bỏ Quyết định số 3232/QĐ-BYT ngày 30/8/2013" |
| 2919/2014 | partial | bị 5904/2019 bãi bỏ Phần 2 → **xác nhận** | xem 5904/2019 |
| 1003/2012 | superseded | bị 292/2024 thay → **xác nhận** (không có PDF chính thức; `data/raw/manual/1003_2012.doc` lấy từ trang luật tư nhân, vẫn còn) | xem 292/2024 |
| 5456/2019 | superseded | bị 5968/2021 thay → **xác nhận** (không có PDF) | xem 5968/2021 |

## 5. Văn bản không in số/ngày trong tệp

| Khóa | Trong tệp | Nguồn chính thức xác nhận số/ngày | Kết luận |
| --- | --- | --- | --- |
| 3312/2024 | tr.1 (ảnh): "Số: /QĐ-BYT", "ngày tháng năm 2024"; không tem, không ký số | bvtn.org.vn (BV Thống Nhất, trang đăng đúng URL tệp): "Quyết định số 3312/QĐ-BYT của Bộ Y tế ngày 05/11/2024". Không có trên kcb.vn và BVĐK Bạc Liêu. | Số/ngày **xác nhận gián tiếp** (một trang bệnh viện). Chưa có bản mang số. |
| 678/2025 | Cả hai tệp để trống số/ngày; ngày sửa tệp QĐ 26/02/2025 | syt.gialai.gov.vn: "Quyết định số 678/QĐ-BYT [27/02/2025]" | Số: xác nhận gián tiếp. **Ngày chưa thống nhất:** 26/02 (manifest) hay 27/02 (Sở Y tế Gia Lai). |
| 2323/2025 (ngoài kho) | Không có trang QĐ; bìa "Ban hành kèm theo Quyết định số /QĐ-BYT ngày tháng 7 năm 2025" | Danh mục BVĐK Bạc Liêu: "Quyết định 2323/QĐ-BYT 2025 ban hành tài liệu chuyên môn 'Hướng dẫn quốc gia về các dịch vụ chăm sóc và điều trị trẻ sơ sinh'", đăng 14/07/2025 | Số: xác nhận gián tiếp. Điều khoản thay thế: không đọc được. |
| **162/2024** (agent trước không liệt kê ở §6) | tr.1–2: "Số: /QĐ-BYT", "ngày tháng năm 2024"; không tem | Danh mục BVĐK Bạc Liêu: "Quyết định 162/QĐ-BYT … 'Hướng dẫn Chẩn đoán, điều trị và dự phòng bệnh Lao'", đăng 19/01/2024; bvtn.org.vn: "Quyết định số 162/QĐ-BYT…" | Số: xác nhận gián tiếp. Ngày 19/01/2024 chỉ là ngày đăng trong danh mục; manifest `issued=null`. |

Bốn văn bản trên không xác nhận được số/ngày từ chính văn bản (không có trang chữ ký mang số). Đối chiếu: 1154/2024 có số đỏ trên bìa; 1353, 1740, 1840, 2131, 2147, 2388, 2760/2023, 5481, 5968 có tem "số ngày tháng" trong lớp chữ.

## 6. Chất lượng lớp chữ (văn bản có lớp chữ trong kho)

Cột "với" = số trang mà `find_pages` tìm được chữ "với" gõ chuẩn.

| Khóa | Tr. | Tỷ lệ chữ có dấu | Kirin | PUA | ƣ (thô) | "với" | Kết luận |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1019/2025 | 21 | 0,219 | 0 | 61 | 0 | 11 | Đạt |
| 1154/2024 | 33 | 0,227 | 0 | 140 | 0 | 15 | Đạt |
| 1353/2021 | 1 | 0,304 | 0 | 0 | 0 | 0 | Đạt |
| **162/2024** | 213 | 0,238 | **1.333** | 203 | 0 | **20** | **Không đạt (L2)** |
| 1740/2026 | 42 | 0,241 | 0 | 20 | 0 | 26 | Đạt |
| 1840/2025 | 12 | 0,264 | 0 | 8 | 0 | 4 | Đạt |
| 1857/2022 | 27 | 0,230 | 0 | 26 | 0 | 15 | Đạt (tr.1 hỏng, là trang QĐ) |
| 2131/2026 | 130 | 0,243 | 0 | 63 | 0 | 80 | Đạt |
| 2147/2026 | 93 | 0,203 | 0 | 7 | 0 | 54 | Đạt |
| 2388/2024 | 192 | 0,227 | 0 | 13 | 0 | 124 | Đạt (α PUA ở tr.75, 161, 173) |
| 2760/2023 | 104 | 0,249 | 0 | 6 | 0 | 62 | Đạt |
| 2892/2022 | 28 | 0,260 | 0 | 0 | 0 | 20 | Đạt |
| 3192/2010 | 19 | 0,252 | 0 | 0 | 0 | 8 | Đạt về glyph; lỗi nội dung Bảng 2 tr.2 |
| 3312/2024 | 148 | 0,253 | 0 | 190 | 0 | 97 | Đạt |
| 3610/2015 | 228 | 0,248 | 0 | 0 | 2.843 | 144 | Đạt sau `norm()` |
| 5481/2020 | 77 | 0,252 | 0 | 20 | 0 | 55 | Đạt |
| 5642/2015 | 86 | 0,240 | 0 | 446 | 0 | 56 | Đạt (° PUA tr.44) |
| 5904/2019 | 68 | 0,272 | 0 | 46 | 168 | 38 | Đạt sau `norm()`; mất "Ư" đầu từ ở vài chỗ |
| 5968/2021 | 145 | 0,250 | 0 | 23 | 2.032 | 105 | Đạt sau `norm()` |
| **6101/2019** | 6 | **0,003** | 0 | 0 | 0 | **0** | **Không đạt (L1)** |
| 678/2025 | 26 | 0,247 | 0 | 6 | 0 | 13 | Đạt |

Văn bản quét dùng OCR: 1470/2024, 292/2024, 3377/2023, TT51/2017, và 2855/2024 (sidecar mới xong). OCR đọc được nhưng sai dấu nhiều, nên giá trị phải đối chiếu ảnh như `configs/extraction_protocol.md` quy định.

**Số văn bản OCR.**
- Trong kho: 1470, 292, 3377, TT51, 2855 = 5, cộng 6101 nếu sửa L1 = 6. Bản cũ: 1327, 3310, 3705 = 3. Tổng 9, khớp D28.
- Tuy vậy `data/interim/ocr/` có 11 sidecar (thêm TT13/2026 và 4121/2009, cả hai ngoài kho). Cần ghi rõ trần 10 tính những văn bản nào.

## 7. Bất đồng với agent trước

1. **3610/2015.** Agent trước ghi "không có trang QĐ đọc được → điều khoản thay thế chưa đọc" (verified=no). Thực tế tr.2 là ảnh trang QĐ (Số 3610/QĐ-BYT, 31/8/2015), Đ3 chỉ nói hiệu lực, không thay văn bản nào. Nên sửa thành `verified=yes`, bằng chứng tr.2.
2. **5642/2015.** Bằng chứng ghi "tr.1 trang QĐ", nhưng tr.1 là bìa sách; trang QĐ là **tr.3**.
3. **Văn bản không in số.** Agent trước nêu 3 văn bản (3312/2024, 678/2025, 2323/2025); thực tế có **4**, thêm **162/2024** (trong kho, tầng 1). Manifest notes có ghi, nhưng `supersession_check.md` §6 mục 4 bỏ sót.
4. **Cảnh báo lớp chữ.** `supersession_check.md` §6 mục 5 chỉ nêu Kirin ở 2248/2023 (nay ngoài kho). Báo cáo bỏ sót 162/2024 (trong kho) và lớp chữ hỏng của 6101/2019 (trong kho).
   - Manifest notes của 6101 còn ghi "IN_CORPUS=false … hạng 52/53".
   - D28 tính 6101 là văn bản OCR, trong khi OCR của nó không được dùng (L1).
5. **Bằng chứng hiệu lực từ kcb.vn.** Agent trước dùng dòng "Đã có hiệu lực" trên kcb.vn làm bằng chứng còn hiệu lực (3192/2010, 3610/2015, 5642/2015). Dòng này chỉ nói văn bản đã tới ngày hiệu lực. Trường API `statusEffective` ghi "Hết hiệu lực" cho chính các văn bản này và TT51/2017, nhưng đó là giá trị mặc định (426/440 văn bản cũ). **Cả hai đều không chứng minh được tình trạng hiệu lực.**
6. **Chồng lấn trong cùng Bộ Y tế, chưa được nêu.**
   - 5642/2015 chương 8 (cúm mùa) trùng 1840/2025; chương 5 (sốt rét kháng thuốc) trùng 3377/2023.
   - 5904/2019 trùng 3192/2010, 5481/2020 và 2131/2026.
   - 678/2025 trùng 1740/2026 và 5968/2021.
   - 3280/2011 (ĐTĐ típ 2, "current" theo quy tắc) và 4562/2018 (COPD) có trạng thái ảnh hưởng tập giá trị DR8.
7. **Đồng ý có điều kiện.**
   - 1154→1911, 3319→3879 (một phần) và 2699→4845 do agent trước kết luận từ tệp ngoài `data/raw`. Tôi tải lại các tệp đó và xác nhận (sha256 khớp ghi chú manifest).
   - Tuy vậy bằng chứng vẫn **không nằm trong repo**, nên không tái hiện được sau này.
8. **Bảng và ghi chú cũ.** Cột `in_corpus` của `supersession.csv` và bảng 35 văn bản ở `supersession_check.md` §6 là trạng thái trước D28 (L3). Manifest notes của 1353, 1857, 3610, 6101 vẫn ghi "IN_CORPUS=false … vượt 35 văn bản"; notes của 3312 và 678 vẫn giữ đoạn cũ "không tìm thấy bản chính thức; CHƯA xác minh".
9. **Đồng ý với agent trước:**
   - Toàn bộ 36 quan hệ tôi xác nhận.
   - Ba quan hệ suy luận (4562/2018 bị thay, 2760/2021 bị thay, số hiệu 2760/2021) không có điều khoản nào nêu tên.
   - `3874_2018.pdf` là bản trùng của 4562; `3216_2018.pdf` trùng sha256 `a734645a…` với `3126_2018.pdf`.

## 8. Văn bản nên rời kho, hoặc chỉ dùng có giới hạn

Không văn bản nào phải rời kho vì đã bị thay thế. Tuy vậy:

- **6101/2019** — không được dùng cho trích mẩu cho tới khi sửa L1: OCR lại với `override_text_layer=true`, rồi kiểm `--find 6101/2019 "điều trị"`. Nếu không sửa được thì phải rút khỏi kho.
- **1353/2021** — không nên tính là một "hướng dẫn" độc lập trong khoảng [25, 35]. Nên gắn vào 5481/2020 như văn bản sửa đổi. Hệ quả: kho chỉ còn 25 hướng dẫn (24 nếu 6101 bị rút) → xem rủi ro ở §1.
- **5642/2015** — nên loại chương 5 (sốt rét kháng thuốc) và chương 8 (cúm mùa) khỏi trích mẩu, hoặc đăng ký rõ cách DR8 xử lý hai chương này. Nếu không, giá trị năm 2015 sẽ được tính là "Bộ Y tế hiện hành" song song với 1840/2025 và 3377/2023.
- **3192/2010** — giữ, nhưng hiệu lực chỉ dựa vào việc không tìm thấy văn bản thay thế. Mẩu từ Bảng 2 tr.2 (phân độ THA) không nên dùng khi chưa có quyết định về lỗi "140 – 150" / "110 – 109".

## 9. Việc chỉ người dùng làm được

1. **TT51/2017.** Tra hiệu lực trên vbpl.vn (Cơ sở dữ liệu quốc gia về văn bản pháp luật) hoặc Công báo bằng trình duyệt, rồi báo lại. Công cụ không đọc được trang JS, và không được dùng trang luật tư nhân.
2. **4562/2018 và 3280/2011.** Quyết định trạng thái hai văn bản này, vì chúng ảnh hưởng tập giá trị DR8. Ghi vào `docs/DECISIONS.md` trước HG2.9. Đề xuất coi 4562/2018 là đã bị thay: 2767/2023 Đ3 nêu 3874/2018, văn bản mà chính 4562 đã thay, nên nhiều khả năng Bộ ghi nhầm số.
3. **Số/ngày.**
   - 678/2025: ngày 26/02 hay 27/02/2025; số 678 hiện chỉ có từ danh mục của Sở Y tế Gia Lai.
   - 3312/2024: số và ngày chỉ có từ trang BV Thống Nhất.
   - 162/2024: ngày ban hành.
   - Cách làm: tìm bản QĐ có số (bản sao y có số, công văn triển khai của Sở Y tế…).
4. **Chấp nhận nguồn.**
   - 1154/2024: Drive do BV Sa Đéc liên kết.
   - 2892/2022 và 678/2025: thư viện Sở Y tế Gia Lai.
   - 3192/2010: bản Word không ký trên kcb.vn.
   - 5904/2019: bản Word không ký kèm ảnh QĐ, benhvienhatrung.vn.
5. **Quyết định khoa học.** Chọn cách xử lý:
   - Bảng 2 của 3192/2010.
   - Các chương trùng của 5642/2015.
   - Chồng lấn 5904/2019, 678/2025 (DR8).
   - Có tính 1353/2021 là một hướng dẫn hay không.
6. **Xóa tay** (hook chặn agent):
   - `data/raw/3874_2018.pdf` (trùng 4562).
   - `data/raw/3216_2018.pdf` (trùng 3126).
   - `data/raw/manual/1003_2012.doc` (lấy từ trang luật tư nhân — quy tắc cứng 7).
7. **Ngày 15/10/2026, trước khi đóng băng.** Quét lại kcb.vn (API), BVĐK Bạc Liêu và thư viện Sở Y tế Gia Lai. Kiểm vaac.gov.vn và vncdc.gov.vn bằng trình duyệt (HIV, dại). Danh mục văn bản BVĐK Bạc Liêu mới cập nhật tới 07/8/2026.

## 10. Đề xuất sửa cho agent chính (không phải việc của người dùng)

1. **L2 — Kirin trong 162/2024.**
   - Thêm vào `_GLYPH` trong `src/vnsoc/extract/verify_span.py` hai ánh xạ: U+04DF → "ớ", U+04AF → "ẫ". Nếu có chữ hoa thì thêm cả chữ hoa. Kèm test.
   - Chạy lại verify cho P-tbhiv-01, -02, -03, -07 và chép lại span bằng chữ chuẩn.
   - Làm việc này trước khi trích mẩu nghiên cứu chính từ 162/2024.
2. **L1 — 6101/2019.** OCR lại 6101/2019 với override; cập nhật `ocr`/`text_layer` trong manifest. Cập nhật manifest cho 2855/2024 (OCR đã xong).
3. **L3 — bảng và ghi chú.** Đồng bộ cột `in_corpus` của `supersession.csv` với manifest; sửa `supersession_check.md` §6 và các notes cũ nêu ở §7 mục 8.
4. **Lưu bằng chứng vào repo.** Lưu ba tệp bằng chứng hiện nằm ngoài repo vào `data/raw/manual/` kèm sha256: bản ký số 1154/2024, trang QĐ 3319/2017 của kcb.vn, bản 2699/2020 có trang QĐ. Sửa bằng chứng của 3610/2015 (tr.2) và 5642/2015 (tr.3).
5. **Ký tự PUA.** Cân nhắc thêm U+F0B0 → "°", U+F061 → "α", U+F062 → "β" vào `_GLYPH`. Nếu thêm, kiểm lại mọi mẩu đã verify.
