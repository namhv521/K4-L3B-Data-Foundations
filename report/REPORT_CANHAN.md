# Báo Cáo Cá Nhân — Lab 7: Embedding & Vector Store

**Họ tên:** [Tên sinh viên]
**Nhóm:** [Tên nhóm]
**Ngày:** [Ngày nộp]

> **Nộp 1 bản / sinh viên.** Phần nhóm (lựa chọn tài liệu, thiết kế chiến lược, bộ câu hỏi đánh giá, demo) nộp chung 1 bản trong `REPORT_NHOM.md`. Chi tiết thang điểm: `docs/SCORING.md`.

**Tổng điểm phần cá nhân: 60** = Khởi động (5) + Hướng tiếp cận (10) + Hoàn thiện code (30) + Dự đoán độ tương tự (5) + Kết quả truy xuất của tôi (10).

---

## 1. Khởi động (Warm-up) — Cá nhân (5 điểm)

### Độ tương tự Cosine (Cosine Similarity) (Bài tập 1.1)

**Độ tương tự cosine cao (High cosine similarity) nghĩa là gì?**
> Độ tương tự cosine cao nghĩa là hai vector embedding có hướng gần giống nhau, cho thấy hai đoạn văn bản có nội dung hoặc ý nghĩa ngữ nghĩa tương đồng.

**Ví dụ có độ tương tự CAO:**
- Câu A:Điện thoại này được bảo hành trong 12 tháng.
- Câu B:Sản phẩm điện thoại có thời hạn bảo hành là 1 năm.
- Tại sao tương đồng:: Hai câu sử dụng từ ngữ khác nhau nhưng đều diễn đạt cùng ý nghĩa: điện thoại được bảo hành 12 tháng.

**Ví dụ có độ tương tự THẤP:**
- Câu A: Điện thoại này được bảo hành trong 12 tháng.
- Câu B: Cửa hàng mở cửa lúc 8 giờ sáng.
- Tại sao khác: Hai câu nói về hai chủ đề khác nhau: một câu về bảo hành, câu còn lại về giờ hoạt động của cửa hàng.

**Tại sao độ tương tự cosine (cosine similarity) được ưu tiên hơn khoảng cách Euclid (Euclidean distance) cho text embeddings?**
> Cosine similarity tập trung vào góc/hướng giữa các vector thay vì độ lớn của vector. Vì vậy, nó phù hợp để đo mức độ tương đồng về ngữ nghĩa giữa các text embedding và ít bị ảnh hưởng bởi độ lớn vector.

### Bài toán tính toán Chunking (Bài tập 1.2)

**Tài liệu 10,000 ký tự, chunk_size=500, overlap=50. Bao nhiêu chunks?**
> số steps = chunk_size - overlap = 450
> số chunks = (10000-500)/450 + 1 ~ 23
> 23
**Nếu độ chồng chéo (overlap) tăng lên 100, số lượng chunk thay đổi thế nào? Tại sao muốn độ chồng chéo nhiều hơn?**
> so chunks = (10000-500)/(500-100) + 1 ~ 25
> Số lượng tăng từ 23 lên 25 chunks. Overlap lớn hơn giúp giữ lại nhiều ngữ cảnh ở ranh giới giữa các chunk, giảm nguy cơ một câu hoặc ý quan trọng bị chia cắt; đổi lại sẽ làm tăng lượng dữ liệu cần embedding, lưu trữ và tìm kiếm.

---

## 2. Hướng tiếp cận của tôi (My Approach) — Cá nhân (10 điểm)

Giải thích cách tiếp cận của bạn khi lập trình (implement) các phần chính trong gói `src`.

### Các hàm chia nhỏ (Chunking Functions)

**`SentenceChunker.chunk`** — hướng tiếp cận:
>   Sử dụng biểu thức chính quy `re.split(r"(?<=[.!?])(?:\\s+|\\n+)", text)` với positive lookbehind để nhận diện ranh giới câu mà không làm mất các ký tự dấu câu (`.`, `!`, `?`). Sau đó, loại bỏ các chuỗi rỗng và gom nhóm các câu lại theo kích thước `max_sentences_per_chunk` bằng hàm `join`. Xử lý trường hợp văn bản không chứa dấu kết thúc câu hoặc văn bản rỗng bằng cách trả về danh sách an toàn.

**`RecursiveChunker.chunk` / `_split`** — hướng tiếp cận:
> Thuật toán tiếp cận theo hướng phân cấp giảm dần các ký tự phân tách: `["\\n\\n", "\\n", ". ", " ", ""]`. Base case xảy ra khi độ dài đoạn văn nhỏ hơn hoặc bằng `chunk_size`, hoặc khi danh sách separators rỗng (khi đó cắt cứng theo ký tự). Thuật toán có bước quan trọng là gom cụm (merge): ghép các đoạn ngắn liên tiếp lại với nhau bằng separator cho đến khi đạt ngưỡng `chunk_size`, tránh tạo ra các chunk quá vụn.

### Lớp EmbeddingStore

**`add_documents` + `search`** — hướng tiếp cận:
> Lưu trữ toàn bộ dữ liệu dưới dạng danh sách các từ điển trong bộ nhớ (`self._store`). Khi nạp tài liệu, hệ thống tính toán vector nhúng qua `self._embedding_fn` và chuẩn hóa metadata (đặc biệt là bảo toàn trường `doc_id`). Khi tìm kiếm, thuật toán tính tích vô hướng (dot product) giữa vector câu hỏi và vector từng tài liệu, sắp xếp theo điểm số giảm dần và trích xuất top-k kết quả.

**`search_with_filter` + `delete_document`** — hướng tiếp cận:
>  `search_with_filter` áp dụng chiến lược lọc trước (Pre-filtering): duyệt qua toàn bộ store để chọn ra danh sách các bản ghi thỏa mãn tất cả các điều kiện trong `metadata_filter`, sau đó mới thực hiện tìm kiếm tương đồng trên danh sách đã lọc. `delete_document` lọc bỏ mọi bản ghi có `metadata['doc_id'] == doc_id` hoặc `id == doc_id` và trả về `True` nếu số lượng bản ghi giảm đi, ngược lại trả về `False`.

### Tác tử KnowledgeBaseAgent

**`answer`** — hướng tiếp cận:
>  Dựng prompt theo chuẩn RAG: truy xuất top-k chunk liên quan nhất từ store, định dạng ngữ cảnh rõ ràng có đánh số thứ tự trích dẫn `[1]`, `[2]` kèm nguồn tài liệu, đặt chỉ dẫn bắt buộc LLM chỉ trả lời dựa trên ngữ cảnh để chống bịa đặt (anti-hallucination). Nếu store không có kết quả nào, trả về thông báo từ chối lịch sự thay vì gọi LLM vô ích.

### Mở rộng cho benchmark chính sách bảo hành

**`HeadingChunker.chunk`** — hướng tiếp cận:
> Dùng `re.finditer(r"^(#{1,6}\\s+.+)$", re.MULTILINE)` để tìm từng heading Markdown từ `#` đến `######` và lấy body của section theo vị trí heading kế tiếp. Dùng `finditer()` thay vì `split()` để hai heading liên tiếp vẫn tạo hai section độc lập. Section ngắn được giữ nguyên; section dài được giao cho `RecursiveChunker`, đồng thời lặp lại prefix heading trong mọi sub-chunk và trừ độ dài prefix khỏi `chunk_size` để không vượt giới hạn ký tự.

**`bench.py`** — hướng tiếp cận:
> Benchmark có một cấu hình `CHUNKER` duy nhất để thay chiến lược công bằng. Khi ingest, mã tách YAML frontmatter khỏi body trước khi chunk, đưa frontmatter vào metadata của mọi chunk và tạo ID ổn định dạng `f"{path.stem}#{index}"`; nhờ đó câu 4 có thể pre-filter `{"audience": "both"}`. Với OpenAI, `CachedEmbedder` lưu vector theo SHA-256 của nội dung để chạy lại không embed/bị tính phí lần nữa. Hàm `configure_utf8_output()` gọi `reconfigure(encoding="utf-8", errors="replace")` cho stdout/stderr, tránh lỗi CP1252 khi in tiếng Việt trên Windows.

---

## 3. Hoàn thiện code (Core Implementation) — Cá nhân (30 điểm)

Vượt qua bộ kiểm thử là điều kiện tính điểm phần này.

### Kết Quả Kiểm Thử (Test Results)

```text
$ python -m pytest tests -v
collected 54 items

tests/test_heading_bench.py::TestHeadingChunker::test_splits_at_each_markdown_heading PASSED
tests/test_heading_bench.py::TestHeadingChunker::test_consecutive_headings_remain_separate_sections PASSED
tests/test_heading_bench.py::TestHeadingChunker::test_long_section_repeats_its_heading_on_every_recursive_subchunk PASSED
tests/test_heading_bench.py::TestCachedEmbedder::test_reuses_persisted_vector_for_the_same_content_hash PASSED
tests/test_heading_bench.py::TestBenchIngestion::test_chunk_documents_use_source_stem_as_doc_id_and_propagate_metadata PASSED
tests/test_heading_bench.py::TestBenchIngestion::test_filtered_benchmark_query_receives_no_buyer_chunks PASSED
tests/test_benchmark_warranty.py::TestWarrantyBenchmark::test_configure_utf8_output_reconfigures_console_stream PASSED
tests/test_solution.py::TestEmbeddingStoreSearchWithFilter::test_filter_by_department PASSED
tests/test_solution.py::TestKnowledgeBaseAgent::test_answer_non_empty PASSED
...
============================= 54 passed in 0.10s ==============================
```

**Số lượng bài test vượt qua (pass):** 54 / 54

**Phần đã bổ sung và kiểm thử:** `HeadingChunker` tách heading, xử lý heading liên tiếp và lặp heading khi recursive split; benchmark tách frontmatter, lan truyền metadata/`doc_id`, áp dụng filter câu 4, cache embedding OpenAI và cấu hình UTF-8 cho console Windows. Toàn bộ test gốc và test bổ sung đều pass.

---

## 4. Dự đoán độ tương tự (Similarity Predictions) — Cá nhân (5 điểm)

> Đo live bằng `GeminiEmbedder` của mã nguồn cá nhân, model `gemini-embedding-001`. Với từng cặp, tôi tạo hai embedding rồi dùng `compute_similarity` để tính cosine; kết quả chạy được lưu tại `.cache/gemini_similarity.stdout.log`. Vì vậy đây là kết quả semantic, không phải vector băm của `MockEmbedder`.

| Cặp | Câu A | Câu B | Dự đoán | Cosine thực tế | Đúng? |
|------|-----------|-----------|---------|----------------|-------|
| 1 | Điện thoại được bảo hành 12 tháng. | Sản phẩm điện thoại có thời hạn bảo hành một năm. | Cao | 0.9222 | Có — cao nhất trong 5 cặp |
| 2 | Điện thoại được bảo hành 12 tháng. | Cửa hàng mở cửa lúc 8 giờ sáng. | Thấp | 0.6117 | Có — thấp nhất trong 5 cặp |
| 3 | MemoryZone chịu phí gửi trả sản phẩm sau bảo hành. | Khách hàng không phải trả phí vận chuyển chiều gửi trả hàng. | Cao | 0.7396 | Có |
| 4 | Shopee không trực tiếp bảo hành sản phẩm. | Người bán tiếp nhận bảo hành theo chính sách của họ hoặc nhà sản xuất. | Trung bình–cao (hai vế bổ sung của cùng chính sách) | 0.8016 | Có |
| 5 | Dữ liệu trong thiết bị không được bảo hành. | Thông tin lưu trên máy không thuộc phạm vi bảo hành. | Cao | 0.9005 | Có |

**Kết quả nào bất ngờ nhất? Điều này nói gì về cách embeddings biểu diễn ý nghĩa?**
> Cặp 2 không liên quan trực tiếp nhưng vẫn đạt 0.6117, cho thấy các câu tiếng Việt ngắn cùng bối cảnh bán lẻ có thể chia sẻ một phần không gian biểu diễn. Vì vậy không nên áp một ngưỡng cosine tuyệt đối cho mọi truy vấn; cần so sánh tương đối trong cùng tập kết quả. Tuy nhiên, model vẫn tách được cặp này khỏi các cặp cùng nghĩa/liên quan chính sách (0.7396–0.9222); cặp diễn đạt cùng thời hạn bảo hành đạt cao nhất 0.9222.

---

## 5. Kết quả truy xuất của tôi (Competition Results) — Cá nhân (10 điểm)

Chạy **5 câu hỏi đánh giá của nhóm** trên mã nguồn cá nhân của bạn trong gói `src`. **5 câu hỏi này phải trùng với các thành viên cùng nhóm** (xem `REPORT_NHOM.md`).

> Benchmark semantic được chạy trên corpus hoàn chỉnh gồm **16** tài liệu Markdown trong `data/warranty/`. `HeadingChunker(chunk_size=500)` tạo **627 chunks**; mọi chunk và 5 query được embed bằng `GeminiEmbedder` / `gemini-embedding-001`. Script `.cache/benchmark_gemini.py` checkpoint vector theo batch để tuân quota API và ghi ranking tái lập vào `.cache/gemini_benchmark.json`. Với Q4, truy xuất dùng `search_with_filter(..., metadata_filter={"audience": "both"})`. Sau retrieval, `KnowledgeBaseAgent` được gọi với đúng top‑3 chunk của từng query và `gemini-2.5-flash`; các ký hiệu `[1]`, `[2]`, `[3]` trong câu trả lời là thứ tự các chunk đó.

| # | Câu hỏi (Query) | Top-1 chunk truy xuất được (tóm tắt) | Score | Có liên quan không? (Relevant) | Câu trả lời grounded của Agent (tóm tắt) |
|---|-------|--------------------------------|-------|-----------|------------------------|
| 1 | Điện Máy Chợ Lớn đổi trả lỗi NSX trong bao lâu, ngoại lệ nào? | `dien-may-cho-lon-warranty#0`: đổi miễn phí **35 ngày** nếu lỗi NSX; không áp dụng Apple. | 0.8441 | Có — top‑1 là gold chunk và trả lời đủ cả thời hạn lẫn ngoại lệ. | Đổi miễn phí trong 35 ngày nếu lỗi NSX; ngoại lệ sản phẩm Apple `[1]`. |
| 2 | Di Động Việt chờ thẩm định 15/20 ngày và xử lý quá hạn thế nào? | `chinh-sach-bao-hanh-dien-thoai#28`: tối đa **15 ngày TP.HCM**, **20 ngày Tỉnh/Hà Nội**; quá hạn đổi máy dù có lỗi hay không. | 0.8452 | Có — top‑1 là gold chunk, có toàn bộ mốc thời gian và cách xử lý. | 15 ngày tại TP.HCM, 20 ngày tại Tỉnh/Hà Nội; quá hạn chưa có kết quả thì đổi sản phẩm dù có lỗi hay không `[1]`, `[3]`. |
| 3 | MemoryZone chịu chi phí vận chuyển nào khi bảo hành? | `memoryzone-warranty#27`: chịu phí vận chuyển **một chiều gửi trả** hàng đã bảo hành cho khách. | 0.9095 | Có — top‑1 là gold chunk và nêu đúng chiều vận chuyển. | MemoryZone chi trả một chiều gửi trả sản phẩm đã bảo hành `[1]`; top‑3 không chứng minh MemoryZone chi trả chiều khách gửi đến. |
| 4 | Theo tài liệu `audience=both`, ai bảo hành trên Shopee và Shopee có trực tiếp bảo hành? | `77245#38`: Shopee không thực hiện nghĩa vụ bảo hành, trừ sản phẩm do Shopee tự đăng bán. | 0.9101 | Có — top‑3 đều là chunk chính sách bảo hành Shopee; Q4 đã pre-filter `audience=both`. | Người bán thực hiện bảo hành theo chính sách của họ/nhà sản xuất; Shopee chỉ hỗ trợ trong khả năng, không trực tiếp bảo hành trừ sản phẩm do Shopee trực tiếp đăng bán `[1]`, `[2]`, `[3]`. |
| 5 | MemoryZone có bảo hành/chịu trách nhiệm dữ liệu trong thiết bị không? | `memoryzone-warranty#21`: không bảo hành và không chịu trách nhiệm dữ liệu trong thiết bị khi bảo hành. | 0.9493 | Có — top‑1 là gold chunk và nêu trọn điều khoản. | Không; MemoryZone không bảo hành hay chịu trách nhiệm đối với dữ liệu trong sản phẩm/thiết bị `[1]`. |

**Bao nhiêu câu hỏi trả về chunk có liên quan trong top-3?** **5 / 5**. Cả 5 expected document đều xuất hiện trong top‑3, đồng thời đều là top‑1; kiểm tra thủ công nội dung top‑1 xác nhận chúng chứa điều khoản gold tương ứng.

**Chấm theo rubric truy xuất:** mỗi query có chunk liên quan trong top‑3 và agent trả lời đúng theo gold answer, nên đạt `2 × 5 = 10 / 10`. Với Q3, câu trả lời giữ đúng phạm vi bằng chứng: chính sách chỉ khẳng định phí một chiều **gửi trả**, không suy diễn về chiều khách gửi hàng đến.

**Điều hay nhất tôi học được từ thành viên khác / nhóm khác (qua demo):**
> Chưa có dữ liệu demo của thành viên/nhóm khác để ghi nhận trung thực. Từ benchmark của chính mình, tôi học được rằng test cấu trúc pass không tự bảo đảm retrieval semantic tốt: lần Mock ban đầu sai nguồn hoặc thiếu gold source, trong khi sau khi bổ sung corpus và dùng embedding semantic, top‑1 đúng ở 5/5 câu. Metadata filter của Q4 cũng minh hoạ pre-filter có thể thu hẹp không gian tìm kiếm đúng đối tượng trước khi xếp hạng semantic.

---

## Tự Đánh Giá (Phần Cá Nhân)

> Điểm semantic bên dưới dựa trên `gemini-embedding-001`, corpus đã đủ 16 tài liệu và kết quả top‑3/grounded answer được lưu trong `.cache/gemini_benchmark.json` và `.cache/gemini_agent_answers.json`; không dùng `MockEmbedder` để tự kết luận chất lượng retrieval.

| Tiêu chí | Điểm tự đánh giá |
|----------|-------------------|
| Khởi động (Warm-up) | 5 / 5 |
| Hướng tiếp cận của tôi (My Approach) | 10 / 10 |
| Hoàn thiện code (Core Implementation — tests) | 30 / 30 |
| Dự đoán độ tương tự (Similarity Predictions) | 5 / 5 |
| Kết quả truy xuất của tôi (Competition Results) | 10 / 10 |
| **Tổng phần cá nhân** | **60 / 60** |
