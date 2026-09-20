# Báo Cáo Nhóm — Lab 7: Embedding & Vector Store

**Nhóm:** [Tên nhóm]
**Thành viên:** [Họ tên từng thành viên]
**Ngày:** [Ngày nộp]

> **Nộp 1 bản / nhóm.** Phần cá nhân (hướng tiếp cận, kết quả riêng, dự đoán…) mỗi thành viên nộp riêng trong `REPORT_CANHAN.md`. Chi tiết thang điểm: `docs/SCORING.md`.

**Tổng điểm phần nhóm: 40** = Lựa chọn tài liệu (10) + Thiết kế chiến lược (15) + Chất lượng truy xuất (10) + Thuyết trình (5).

---

## 1. Lựa chọn tài liệu (Document Set Quality) — Nhóm (10 điểm)

### Chủ đề (Domain) & Lý Do Chọn

**Chủ đề:** Chính sách bảo hành và đổi trả sau bán của các nhà bán lẻ thiết bị công nghệ/điện tử tại Việt Nam.

**Tại sao nhóm chọn chủ đề này?**
> Nhóm chọn chủ đề bảo hành vì đây là nhu cầu hỗ trợ sau bán hàng phổ biến trong thương mại điện tử. Các chính sách có cấu trúc rõ ràng theo điều kiện, thời hạn, trường hợp từ chối và quy trình xử lý; đồng thời khác nhau giữa các nhà bán lẻ, phù hợp để sau này đánh giá khả năng truy xuất thông tin chính xác từ nguồn.

### Danh sách tài liệu (Data Inventory)

> **Phạm vi CP1–CP2:** dữ liệu hiện được lưu tại `data/warranty/`; `sources.csv` có 14 dòng tương ứng với 14 file Markdown. Toàn bộ nguồn được lấy ngày **2026-09-20** và chưa công bố phiên bản cụ thể (`not-stated`).

| # | Tên tài liệu | Nguồn (Source URL) | Ngày lấy / Phiên bản | Số ký tự | Metadata đã gán |
|---|--------------|------------|--------------------|----------|-----------------|
| 1 | 24hStore.vn - Hệ thống uỷ quyền Apple và Samsung Việt Nam | https://24hstore.vn/ | 2026-09-20 / `not-stated` | 734 | `doc_id`, `title`, `source_url`, `retrieved_at`, `document_version` |
| 2 | Quy chế hoạt động sàn TMĐT Shopee.vn | https://help.shopee.vn/portal/4/article/77245 | 2026-09-20 / `not-stated` | 12.2 KB | `doc_id`, `title`, `source_url`, `retrieved_at`, `document_version` |
| 3 | An Phát Computer - Máy tính, thiết bị mạng chính hãng | https://www.anphatpc.com.vn/ | 2026-09-20 / `not-stated` | 5.0 KB | `doc_id`, `title`, `source_url`, `retrieved_at`, `document_version` |
| 4 | Chuyên Mua - Bán Máy ảnh kỹ thuật số - Bảo hành | https://www.mayanhkts.vn/b%E1%BA%A3o-h%C3%A0nh | 2026-09-20 / `not-stated` | 2.8 KB | `doc_id`, `title`, `source_url`, `retrieved_at`, `document_version` |
| 5 | Chính sách bảo hành tại Gearshop | https://gearshop.vn/bao-hanh-doi-tra.html | 2026-09-20 / `not-stated` | 7.7 KB | `doc_id`, `title`, `source_url`, `retrieved_at`, `document_version` |
| 6 | Chính sách bảo hành - Laptop Plus | https://laptopplus.vn/bao-hanh | 2026-09-20 / `not-stated` | 7.4 KB | `doc_id`, `title`, `source_url`, `retrieved_at`, `document_version` |
| 7 | Chính sách bảo hành của Nhà Công Nghệ | https://nhacongnghe.vn/chinh-sach-bao-hanh-cua-nha-cong-nghe/ | 2026-09-20 / `not-stated` | 20.3 KB | `doc_id`, `title`, `source_url`, `retrieved_at`, `document_version` |
| 8 | Chính sách bảo hành và đổi trả máy mới tại Di Động Việt | https://didongviet.vn/chinh-sach-bao-hanh-dien-thoai.html | 2026-09-20 / `not-stated` | 27.7 KB | `doc_id`, `title`, `source_url`, `retrieved_at`, `document_version` |
| 9 | Chính sách bảo hành sản phẩm tại Mayanh24h | https://mayanh24h.com/chinh-sach-bao-hanh-hang-hoa.html | 2026-09-20 / `not-stated` | 15.2 KB | `doc_id`, `title`, `source_url`, `retrieved_at`, `document_version` |
| 10 | Chính sách bảo hành tại DucanhPC | https://ducanhpc.com/chinh-sach-bao-hanh-tai-ducanhpc/ | 2026-09-20 / `not-stated` | 27.4 KB | `doc_id`, `title`, `source_url`, `retrieved_at`, `document_version` |
| 11 | Chính sách bảo hành và đổi trả sản phẩm - CellphoneS | https://cellphones.com.vn/chinh-sach-bao-hanh | 2026-09-20 / `not-stated` | 55.6 KB | `doc_id`, `title`, `source_url`, `retrieved_at`, `document_version` |
| 12 | Chính sách bảo hành - Camera Jshop | https://mayanhcu.com.vn/chinh-sach | 2026-09-20 / `not-stated` | 33.5 KB | `doc_id`, `title`, `source_url`, `retrieved_at`, `document_version` |
| 13 | Chính sách bảo hành - LP Camera Store | https://mayanhlp.com/pages/chinhsachbaohanh | 2026-09-20 / `not-stated` | 24.7 KB | `doc_id`, `title`, `source_url`, `retrieved_at`, `document_version` |
| 14 | MediaMart - Hệ thống siêu thị điện máy | https://baohanh.mediamart.vn | 2026-09-20 / `not-stated` | 13.4 KB | `doc_id`, `title`, `source_url`, `retrieved_at`, `document_version` |

**Danh sách kiểm tra quản trị dữ liệu (Data governance checklist):**
- [x] Tập tài liệu sử dụng các URL website công khai được liệt kê trong `data/warranty/sources.csv`; không sử dụng thông tin đăng nhập, dữ liệu nội bộ hoặc dữ liệu cá nhân của người dùng.
- [x] Mỗi tài liệu trong `data/warranty/` có `source_url`, `retrieved_at` và `document_version` trong YAML frontmatter; `sources.csv` ghi một dòng tương ứng cho mỗi file.

### Cấu trúc Metadata (Metadata Schema)

| Trường metadata | Kiểu | Ví dụ giá trị | Tại sao hữu ích cho truy xuất (retrieval)? |
|----------------|------|---------------|-------------------------------|
| `doc_id` | `string` | `chinh-sach-bao-hanh-tai-ducanhpc` | Định danh ổn định cho tài liệu; hỗ trợ truy vết nguồn và quản lý/xóa các chunk thuộc cùng tài liệu. |
| `title` | `string` | `Chính sách bảo hành - Laptop Plus` | Hiển thị nguồn dễ hiểu trong kết quả truy xuất và giúp người dùng kiểm tra ngữ cảnh. |
| `source_url` | `string` (URL) | `https://laptopplus.vn/bao-hanh` | Cho phép mở trang gốc để đối chiếu và bảo đảm tính minh bạch của corpus. |
| `retrieved_at` | `date` (`YYYY-MM-DD`) | `2026-09-20` | Cho biết thời điểm thu thập vì chính sách có thể thay đổi theo thời gian. |
| `document_version` | `string` | `not-stated` | Lưu phiên bản/ngày hiệu lực nếu nguồn công bố; `not-stated` thể hiện nguồn không nêu phiên bản, không tự suy đoán. |

> **Ghi nhận phạm vi CP1–CP2:** Frontmatter hiện có 5 trường metadata nêu trên. Các trường phục vụ lọc như `audience`, `category` và `language` chưa được gán trong corpus hiện tại; vì vậy báo cáo không khẳng định các trường đó đã sẵn sàng. Mục chiến lược, benchmark, A/B test và demo bên dưới được giữ nguyên để thực hiện ở checkpoint sau.

---

## 2. Thiết kế chiến lược (Strategy Design) — Nhóm (15 điểm)

> Mỗi thành viên thử **một chiến lược khác nhau** trên cùng bộ tài liệu; nhóm tổng hợp và so sánh ở đây.

### Phân tích đường cơ sở (Baseline Analysis)

Đã chạy `ChunkingStrategyComparator().compare(..., chunk_size=200)` trên **phần body sau frontmatter** của 3 tài liệu. Vì vậy các con số dưới đây chỉ đo nội dung chính sách, không đo khối YAML metadata.

| Tài liệu | Chiến lược (Strategy) | Số lượng Chunk | Độ dài trung bình | Giữ được ngữ cảnh không? |
|-----------|----------|-------------|------------|-------------------|
| `77245.md` (77.900 ký tự body) | FixedSizeChunker (`fixed_size`) | 433 | 199,86 | Không; có thể cắt giữa câu/mục. |
| `77245.md` (77.900 ký tự body) | SentenceChunker (`by_sentences`) | 293 | 263,74 | Một phần; giữ trọn câu nhưng một chunk có thể ghép hai mục xa nhau. |
| `77245.md` (77.900 ký tự body) | RecursiveChunker (`recursive`) | 608 | 126,34 | Tương đối; ưu tiên đoạn/dòng, nhưng HTML crawl tạo nhiều đoạn ngắn. |
| `chinh-sach-bao-hanh-dien-thoai.md` (16.166 ký tự body) | FixedSizeChunker (`fixed_size`) | 90 | 199,40 | Không; có thể cắt giữa câu/mục. |
| `chinh-sach-bao-hanh-dien-thoai.md` (16.166 ký tự body) | SentenceChunker (`by_sentences`) | 84 | 189,87 | Một phần; giữ trọn câu nhưng không nhận biết ranh giới điều khoản. |
| `chinh-sach-bao-hanh-dien-thoai.md` (16.166 ký tự body) | RecursiveChunker (`recursive`) | 115 | 138,65 | Tương đối; tôn trọng newline/đoạn trước khi cắt nhỏ. |
| `bao-hanh-doi-tra.md` (7.181 ký tự body) | FixedSizeChunker (`fixed_size`) | 40 | 199,03 | Không; có thể cắt giữa câu/mục. |
| `bao-hanh-doi-tra.md` (7.181 ký tự body) | SentenceChunker (`by_sentences`) | 27 | 259,22 | Một phần; giữ trọn câu nhưng các câu dài làm chunk lớn. |
| `bao-hanh-doi-tra.md` (7.181 ký tự body) | RecursiveChunker (`recursive`) | 50 | 140,82 | Tương đối; giữ đoạn khi có thể, phù hợp hơn fixed-size với văn bản nhiều xuống dòng. |

> Nhận xét baseline: SentenceChunker tạo ít chunk nhất nhưng độ dài biến thiên theo câu rất dài của dữ liệu web. RecursiveChunker tạo nhiều chunk ngắn hơn vì tôn trọng ranh giới newline; điều này tránh cắt giữa điều khoản nhưng vẫn chưa khai thác trực tiếp cấu trúc mục/điều của văn bản quy định.

### Chiến lược của từng thành viên

> Mỗi thành viên điền một khối dưới đây (copy thêm nếu nhóm có nhiều hơn 3 người).

**Thành viên 1 — [Tên]**
- **Loại chiến lược:** [FixedSize / Sentence / Recursive / custom]
- **Mô tả & lý do chọn cho chủ đề này:** *(2-3 câu)*
- **Code snippet (nếu custom):**
```python
# Dán mã nguồn (implementation) vào đây
```

**Thành viên 2 — [Tên]**
- **Loại chiến lược:**
- **Mô tả & lý do chọn:**
- **Code snippet (nếu custom):**

**Thành viên 3 — R3**
- **Loại chiến lược:** Custom `HeadingChunker` (heading → recursive fallback).
- **Mô tả & lý do chọn:** Chính sách/quy định thường được người soạn chia sẵn theo heading như `## Điều 4 — ...`; mỗi section vì vậy là một đơn vị ngữ nghĩa tốt hơn cắt theo số ký tự. Chunker tách trước mọi Markdown heading (`#`–`######`), giữ nguyên section ngắn và chỉ dùng recursive khi section vượt 500 ký tự. Với mọi mảnh con, heading được gắn lại để mảnh thứ hai trở đi vẫn biết mình đang nói về điều/mục nào.
- **Code snippet (nếu custom):**
```python
prefix = f"{heading}\n"
body_chunk_size = max(1, self.chunk_size - len(prefix))
body_chunks = RecursiveChunker(chunk_size=body_chunk_size).chunk(body)
return [f"{prefix}{chunk.strip()}" for chunk in body_chunks if chunk.strip()]
```

> Lưu ý dữ liệu: ba file baseline hiện chỉ chuẩn hóa root heading Markdown `#`; các tiêu đề điều/mục còn lại thường là văn bản thường từ trang crawl. `HeadingChunker` đã sẵn sàng khai thác `##`–`######` khi corpus được chuẩn hóa heading ở bước làm sạch dữ liệu.

### So Sánh Giữa Các Thành Viên

| Thành viên | Chiến lược (Strategy) | Điểm truy xuất (/10) | Điểm mạnh | Điểm yếu |
|-----------|----------|----------------------|-----------|----------|
| | | | | |
| | | | | |
| | | | | |

**Chiến lược nào tốt nhất cho chủ đề này? Tại sao?**
> *Viết 2-3 câu — đây là phần được đánh giá cao nhất (khả năng suy nghĩ & giải thích):*

---

## 3. Câu hỏi đánh giá & Chất lượng truy xuất (Retrieval Quality) — Nhóm (10 điểm)

### Câu hỏi đánh giá & Câu trả lời chuẩn (nhóm thống nhất)

> **Đúng 5 câu hỏi**, đa dạng, có thể kiểm chứng; **ít nhất 1 câu** cần lọc metadata mới trả lời tốt. Đây là bộ câu hỏi chung cho mọi thành viên chạy.

| # | Câu hỏi (Query) | Câu trả lời chuẩn (Gold Answer) | Chunk nào chứa thông tin? |
|---|-------|-------------------------------|--------------------------|
| 1 | Điện thoại mới bị lỗi do nhà sản xuất được Điện Máy Chợ Lớn đổi trả trong bao lâu và có ngoại lệ nào? | Được đổi miễn phí trong vòng 35 ngày nếu lỗi do nhà sản xuất; chính sách này không áp dụng cho sản phẩm Apple. | `dien-may-cho-lon-warranty.md`, dòng 19–23 |
| 2 | Di Động Việt chờ kết quả thẩm định của hãng tối đa bao lâu tại TP.HCM và tại Tỉnh/Hà Nội; quá hạn thì xử lý thế nào? | Tối đa 15 ngày tại TP.HCM và 20 ngày tại Tỉnh/Hà Nội, tính từ ngày lập biên bản cam kết. Nếu quá thời hạn mà chưa có kết quả, Di Động Việt đổi sản phẩm dù máy có lỗi hay không. | `di-dong-viet-warranty.md`, dòng 268–272 |
| 3 | Khi khách gửi sản phẩm đến MemoryZone để bảo hành, MemoryZone chịu phần chi phí vận chuyển nào? | MemoryZone chịu chi phí một chiều để gửi trả sản phẩm đã bảo hành cho khách hàng. | `memoryzone-warranty.md`, dòng 275–289 |
| 4 | Theo tài liệu dành cho cả người mua và người bán, ai chịu trách nhiệm bảo hành sản phẩm bán trên Shopee và Shopee có trực tiếp bảo hành không? | Người bán tiếp nhận bảo hành theo chính sách của người bán hoặc nhà sản xuất. Shopee không trực tiếp chịu nghĩa vụ bảo hành và chỉ hỗ trợ trong khả năng cho phép, trừ sản phẩm do chính Shopee trực tiếp đăng bán. | `77245.md`, dòng 204–214; dùng `metadata_filter={"audience": "both"}` |
| 5 | MemoryZone có bảo hành hoặc chịu trách nhiệm đối với dữ liệu nằm trong thiết bị của khách hàng không? | Không. MemoryZone không bảo hành dữ liệu và không chịu trách nhiệm đối với dữ liệu có trong sản phẩm hoặc thiết bị khi bảo hành. | `memoryzone-warranty.md`, dòng 265–269 |

### Tự kiểm câu trả lời chuẩn

- [x] Câu 1 đối chiếu điều khoản đổi trả 35 ngày và ngoại lệ Apple trong `dien-may-cho-lon-warranty.md`.
- [x] Câu 2 đối chiếu mốc 15/20 ngày và cách xử lý quá hạn trong `di-dong-viet-warranty.md`.
- [x] Câu 3 đối chiếu quy định MemoryZone chịu phí vận chuyển một chiều gửi trả hàng trong `memoryzone-warranty.md`.
- [x] Câu 4 đối chiếu trách nhiệm của Người Bán, Nhà sản xuất và ngoại lệ sản phẩm do Shopee trực tiếp đăng bán trong `77245.md`.
- [x] Câu 5 đối chiếu tuyên bố không bảo hành và không chịu trách nhiệm về dữ liệu trong `memoryzone-warranty.md`.

### Tổng hợp chất lượng truy xuất của nhóm

> Cách chấm (theo `docs/SCORING.md`): **2 điểm/câu** — top-3 chứa chunk liên quan + agent trả lời đúng (2), có liên quan nhưng thiếu/không ở top-1 (1), không có trong top-3 (0).

| # | Câu hỏi | Chiến lược tốt nhất cho câu này | Có chunk liên quan trong top-3? | Ghi chú |
|---|---------|-------------------------------|-------------------------------|---------|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |
| 4 | | | | |
| 5 | | | | |

**Lọc bằng metadata có giúp ích không? Ở câu hỏi nào?**
> *Viết 2-3 câu:*

---

## 4. Thuyết trình (Demo) & Bài học nhóm — Nhóm (5 điểm)

**Những phân tích (insights) hay nhất nhóm sẽ trình bày:**
> *Liệt kê 2-3 ý:*

**Bài học rút ra khi so sánh trong nhóm:**
> *Viết 2-3 câu — cùng tài liệu nhưng chiến lược khác nhau dẫn tới khác biệt gì?*

**Nếu làm lại, nhóm sẽ thay đổi gì trong chiến lược dữ liệu (data strategy)?**
> *Viết 2-3 câu:*

---

## Tự Đánh Giá (Phần Nhóm)

| Tiêu chí | Điểm tự đánh giá |
|----------|-------------------|
| Lựa chọn tài liệu (Document Set Quality) | / 10 |
| Thiết kế chiến lược (Strategy Design) | / 15 |
| Chất lượng truy xuất (Retrieval Quality) | / 10 |
| Thuyết trình (Demo) | / 5 |
| **Tổng phần nhóm** | **/ 40** |
