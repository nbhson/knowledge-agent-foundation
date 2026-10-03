# ❓ FAQ — Graph Engineering (Tổng Quan Cả Track)

Câu hỏi nào khó hiểu thì đọc `README.md` phần được nêu trong ngoặc vuông.

---

## Q1. Graph khác vector database thế nào, tôi đang dùng vector RAG rồi? [→ Câu Chuyện Mở Đầu]

**Bạn sẽ thấy**

Bạn hỏi chatbot: *"Hợp đồng dự án Phoenix do ai phê duyệt, và người đó từng quản lý dự án nào liên quan đến AI?"* Hệ thống vector RAG tìm được 5 đoạn có chữ "Phoenix", nhưng không đoạn nào chứa đồng thời cả "người phê duyệt" lẫn "dự án AI", nên nó đoán mò và bịa ra một cái tên.

**Vì sao**

Vector search trả lời được câu hỏi *"đoạn nào giống câu hỏi?"*. Còn câu hỏi của bạn cần đi qua chuỗi quan hệ: Phoenix được duyệt bởi ai, người đó quản lý dự án nào, dự án đó có phải AI không. Đó là **3 bước nhảy** trên quan hệ, không phải một lần so khớp văn bản. Graph đã lưu sẵn chuỗi đó nên trả lời kèm đường dẫn chứng minh.

**Làm gì**

1. Nhìn câu hỏi của mình: chỉ cần tìm một đoạn thì vector đủ; cần nối qua nhiều thực thể thì cần graph.
2. Trong graph, mỗi sự thật là một **cạnh** giữa hai node, ví dụ `Phoenix —[APPROVED_BY]→ Nguyễn Văn A —[MANAGED]→ Atlas`.
3. Truy vấn theo số bước: một truy vấn đi 2 bước là đủ cho câu trên, và trả về cả đường đi chứ không chỉ tên.
4. Nếu cần cả hai, dùng chung: vector để nhớ (recall), graph để chính xác (precision).

```text
Harness = môi trường 1 agent chạy
Loop    = harness + lịch chạy + trạng thái + kiểm chứng
Graph   = nền tri thức bền vững mà cả hai cùng dùng
GraphRAG = Vector (nhớ) + Graph (chính xác + suy luận)
```

**Kiểm tra**

Lấy 20 câu hỏi thật của bạn, đánh dấu câu nào cần nhiều bước. Nếu trên dưới một phần ba số câu cần nhiều bước thì mới đáng xây; nếu hầu hết là tra cứu một ý thì vector RAG là đủ.

---

## Q2. Có nên xây graph không, hay cứ xài vector RAG làm cho nhanh? [→ Tại Sao Quan Trọng]

**Bạn sẽ thấy**

Bạn đang phân vân: xây Knowledge Graph tốn công trích xuất, thiết kế quy tắc, vận hành cơ sở dữ liệu đồ thị, còn vector RAG thì đã chạy được. Rủi ro lớn nhất không phải là tốn tiền, mà là xây xong rồi dùng không đúng chỗ và không thấy khác biệt.

**Vì sao**

Ba con số đo được: GraphRAG tăng **30–40%** độ bao phủ trên câu hỏi tổng hợp, thắng **70%** số lượt đánh giá; kết hợp vector và graph giảm **25–30%** tỉ lệ bịa; trên câu hỏi nhiều bước, độ chính xác là **68% so với 41%** của hệ thống chỉ dùng vector.

**Làm gì**

1. Chọn 30 câu hỏi thật của người dùng, đếm xem bao nhiêu câu là hỏi một bước và bao nhiêu câu là nhiều bước.
2. Chạy A/B trên bộ câu hỏi đó, dùng hai LLM giống nhau, chỉ khác phần truy xuất.
3. Đo riêng từng nhóm: nhiều bước và tổng hợp, và **cả nhóm hỏi một bước** — ở nhóm sau, hệ thống dựa trên graph thường yếu hơn hệ thống vector thuần.
4. Nếu kết quả tốt thì mới mở rộng; nếu không, giữ vector RAG và đừng làm tốn công.

**Kiểm tra**

Báo cáo phải tách ít nhất ba nhóm: hỏi một bước, hỏi nhiều bước, hỏi tổng hợp. Một điểm gộp chung sẽ không cho bạn biết nên đầu tư tiếp hay dừng.

---

## Q3. Lần đầu đụng vào, nên đọc phần nào trước — đọc hết 9 chương thì hơi nhiều? [→ Lộ Trình Học]

**Bạn sẽ thấy**

Thư mục có 9 module từ nền tảng đến đánh giá. Người mới không biết bắt đầu từ đâu, người đã biết Python thì lại muốn nhảy thẳng vào phần suy luận.

**Vì sao**

Các module phụ thuộc nhau theo thứ tự: không có cách trích xuất thực thể quan hệ thì không có graph; không có graph thì không có gì để truy vấn hay đo chất lượng. Đọc sai thứ tự sẽ phải đọc lại.

**Làm gì**

1. Đọc README tổng quan này để nắm bố cục 7 thành phần cốt lõi và vòng đời: trích xuất → dựng → lưu → nhúng → truy vấn → suy luận → đánh giá.
2. `01-foundations` để hiểu graph là gì và các thước đo cơ bản.
3. `02-knowledge-graph` để học trích xuất thực thể, quan hệ, thiết kế ontology; `03-graph-storage` để chọn cơ sở dữ liệu và viết câu truy vấn.
4. `04-graph-embeddings` + `05-graph-rag` cho phần tìm kiếm; `06-graph-reasoning` + `07-gnn` cho phần suy luận.
5. Cuối cùng `08-graph-workflow` và `09-evaluation` khi đã có hệ thống thật.

| Bạn muốn... | Đọc |
|---|---|
| Hiểu graph là gì, các thước đo | `01-foundations/` |
| Trích xuất graph từ tài liệu | `02-knowledge-graph/` |
| Kết hợp vector + graph | `04-graph-embeddings/` |
| Câu hỏi nhiều bước, tìm đường đi | `06-graph-reasoning/` |
| Đo chất lượng graph & GraphRAG | `09-evaluation/` |

**Kiểm tra**

Sau khi đọc tới module 05, bạn phải tự trả lời được: câu hỏi này cần đi mấy bước trên graph, và bằng chứng của từng bước là gì. Không trả lời được thì quay lại module trước.

---

## Q4. Dùng chung vector database và graph database được không, hay phải chọn một? [→ Tại Sao Quan Trọng, Case Study 2]

**Bạn sẽ thấy**

Bạn đã có một cơ sở dữ liệu vector chạy tốt. Người trong team bảo bỏ đi làm graph, hoặc ngược lại bảo xoá hết vector. Cả hai cách đều tốn công dựng lại từ đầu.

**Vì sao**

Chúng trả lời hai câu hỏi khác nhau: vector database trả lời "đoạn nào giống câu hỏi", cơ sở dữ liệu đồ thị trả lời "thực thể nào nối với thực thể nào qua mấy bước, bằng bằng chứng nào". Kết hợp lại là **GraphRAG**, và đây là hướng dùng chung được khuyến nghị.

**Làm gì**

1. Giữ cơ sở dữ liệu vector cho phần **nội dung văn bản**: đặt chỉ mục vector trên các node tài liệu.
2. Dùng graph cho phần **thực thể và quan hệ**: node người, dự án, rồi đi nhiều bước trên đó.
3. Trong hệ thống phổ biến 2025–2026, phần dựng dùng thư viện chuyển đồ thị của LangChain rồi nạp vào Neo4j; phần truy vấn dùng chuỗi Cypher được sinh từ câu hỏi tiếng Việt.
4. Chỉ chạy vector khi câu hỏi đơn giản; khi câu hỏi có ràng buộc nhiều bước thì chuyển sang graph.

**Kiểm tra**

Đo tỉ lệ bịa trên bộ câu hỏi nội bộ, so sánh trước và sau khi bật phần graph. Biện minh quyết định bằng số liệu, không bằng cảm tính.

---

## Q5. Có ví dụ nào chạy được trong thực tế không, hay toàn lý thuyết? [→ Case Studies Thực Tế]

**Bạn sẽ thấy**

Bạn muốn xem một hệ thống đã chạy thật để bắt chước, chứ không phải sơ đồ trên giấy. Bạn cần biết chính xác mỗi bước làm gì và dùng công cụ gì.

**Vì sao**

Có bốn mẫu hệ thống đã công bố, mỗi mẫu cho một bài toán khác nhau. Biết mẫu nào gần việc của bạn thì tiết kiệm hàng tuần thử nghiệm.

**Làm gì**

1. **Microsoft GraphRAG** — mẫu tham khảu cho câu hỏi tổng hợp: tài liệu → trích xuất thực thể và quan hệ bằng mô hình ngôn ngữ → tìm cộng đồng bằng thuật toán Leiden → tóm tắt từng cộng đồng → trả lời bằng cách gom tóm tắt.
2. Vòng lặp trích xuất có lặp lại, nên lượng thực thể tìm được nhiều hơn 3 đến 5 lần so với một lượt.
3. **Neo4j + LangChain** — mẫu cho doanh nghiệp: dùng chuyển đổi đồ thị của LangChain để dựng, và chuỗi hỏi đáp Cypher để truy vấn; quy mô tới hàng tỷ node.
4. **DeepSeek** lưu lịch sử thao tác của agent dạng đồ thị sự kiện, nên có thể nhánh và phát lại như nhánh git.
5. **Codebase knowledge graph** — mẫu cho việc mã nguồn: file định nghĩa hàm, hàm gọi hàm, hàm được hàm kiểm thử nào.

```text
File —[DEFINES]→ Function —[CALLS]→ Function —[TESTED_BY]→ TestFile
```

**Kiểm tra**

Thử nguyên lý luận mẫu 1 trên kho tài liệu thật của bạn: hỏi ba câu tổng hợp ở tầng "cả tổ chức này đang làm gì", so sánh với vector RAG thuần trên đúng ba câu đó.

---

## Q6. Làm sao biết graph của tôi tốt, không phải cứ nhìn demo thấy nó chạy? [→ Tổng Quan]

**Bạn sẽ thấy**

Bạn dựng xong, hỏi thử thấy trả lời ổn. Nhưng bạn không có con số nào để biết tỷ lệ bịa bao nhiêu, hay có bao nhiêu phần tài liệu chưa được trích xuất. Đến lúc sếp hỏi "tin đâu?" thì hệ thống không có gì để trả lời.

**Vì sao**

Cần đo bốn lớp riêng biệt: chất lượng bản thân graph, chất lượng truy xuất, chất lượng câu trả lời, và chất lượng dự đoán quan hệ thiếu. Đo lớp sau mà bỏ lớp trước thì không biết sửa ở đâu.

**Làm gì**

1. Đo **chất lượng graph**: độ phủ thực thể và quan hệ, độ liên thông, tỉ lệ trùng lặp, số node không nối với ai.
2. Đo **chất lượng truy xuất**: độ chính xác trong 5 kết quả đầu, độ đầy đủ, và độ chính xác của các đường đi trả về.
3. Đo **chất lượng câu trả lời**: mỗi mệnh đề có bằng chứng trong graph không, và có đúng câu hỏi không.
4. Đo **chất lượng dự đoán quan hệ thiếu**: tỉ lệ đáp án đúng nằm trong top 10 và thứ hạng trung bình của đáp án đúng.
5. Chạy lại bộ đo này mỗi lần đổi pipeline, và lưu lại báo cáo để so sánh phiên bản.

**Kiểm tra**

Một câu hỏi trả lời sai phải truy được về lớp: chất lượng graph, truy xuất, hay diễn giải. Nếu không chỉ ra được thì hệ thống đánh giá của bạn chưa dùng được.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: README.md.*