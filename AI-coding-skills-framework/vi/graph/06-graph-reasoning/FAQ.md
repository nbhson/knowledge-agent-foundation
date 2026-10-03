# ❓ FAQ — Suy Luận Trên Đồ Thị (Graph Reasoning)

Câu hỏi nào khó hiểu thì đọc `README.md` phần được nêu trong ngoặc vuông.

---

## Q1. Hỏi "Alice quản lý ai?" thì BFS toan quét cả graph, chạy mãi không xong — giới hạn sao? [→ §1 Traversal Strategies]

**Bạn sẽ thấy**

Graph công ty có khoảng 1 triệu node. Bạn hỏi một câu hỏi nhỏ: *"Team của Alice có ai làm AI không?"*, nhưng lần chạy đầu tiên quét cả triệu node, mất hàng chục phút rồi bị giết vì hết thời gian chờ. Chạy không ràng buộc còn cho ra cả `Dave`, dù `Dave` chỉ quen Alice qua quan hệ `KNOWS` với độ tin cậy chỉ 0.60 — hoàn toàn không liên quan tới việc "làm AI".

**Vì sao**

Traversal không ràng buộc = đi vào mọi nhánh, kể cả nhánh `KNOWS`, `FRIEND`, `MENTIONS` vốn không mang thông tin quản lý. Thêm nữa, BFS không giới hạn số node thăm: node động trùng tên hay kết nối đại đa sẽ kéo theo cả con quánh cũng thăm.

**Làm gì**

1. Chọn kiểu đi trước: muốn biết *tất cả* node cách 1–2 bước thì BFS; muốn biết *có tồn tại* một đường thì DFS nhanh hơn.
2. Luôn đặt ràng buộc cho đường đi và cho cả node đích.
3. Graph >1 triệu node thì bật chế độ lấy mẫu: mỗi bước chỉ ghé tối đa 10 node, có thể chọn `random`, `top-confidence` hoặc `pagerank`.
4. Suy ra `confidence` của đường đi bằng giá trị nhỏ nhất trong các cạnh — đường yếu là đường đáng nghi.

```python
results = constrained_bfs(G, "Alice", max_hops=3,
    allowed_edge_types={"MANAGES", "WORKS_ON"}, min_confidence=0.7)
# ['Alice','Bob','Carol'] (hops=2, conf=0.90)
# ['Alice','Bob','Phoenix'] (hops=2, conf=0.85)
# Dave bị loại: KNOWS không nằm trong allowed types
```

**Kiểm tra**

Chạy một graph nhỏ 1.000 node / 5.000 cạnh: BFS không ràng buộc thăm hết node, còn bản constrained thăm ít hơn và nhanh hơn nhiều lần; `Dave` phải biến mất khỏi kết quả; mọi đường trả về đều có `hops` và `confidence` kèm theo.

---

## Q2. "Liên hệ Alice với dự án AI bằng đường nào?" — tìm ra đường này nhưng đường đó toàn quan hệ rác [→ §2 Path Finding]

**Bạn sẽ thấy**

`nx.shortest_path()` trả về `['Alice', 'Dave', 'Carol']`, đúng 2 bước — nhưng bước đầu đi qua quan hệ `KNOWS`, là quan hệ yếu nhất trong graph. Đường thật sự đáng tin là `Alice → Bob → Carol → Atlas`, dài hơn nhưng mọi cạnh đều mạnh. Người dùng hỏi "ai là người duyệt Atlas", hệ thống dẫn đường qua một người chỉ quen biết.

**Vì sao**

Đường ngắn nhất theo số bước không phải đường đáng tin nhất. Nếu không gán trọng số cho cạnh, thuật toán coi `KNOWS` và `MANAGES` là hai cạnh như nhau — trong khi một cạnh đã được đánh dấu sai còn cạnh kia có `confidence` 0.95.

**Làm gì**

1. Gán trọng số cho mỗi cạnh, theo kiểu `1 / confidence`: cạnh chắc 0.95 → trọng số 1.0, cạnh yếu 0.60 → trọng số 3.0.
2. Muốn đường ít bước nhất dùng `nx.shortest_path`; muốn đường đáng tin nhất dùng `nx.dijkstra_path` (tổng trọng số nhỏ nhất).
3. Muốn người dùng/model chọn trong nhiều lựa chọn thì lấy nhiều đường: `nx.all_simple_paths(..., cutoff=4)` hoặc `nx.shortest_simple_paths` rồi đưa cả danh sách vào prompt.
4. Trả kèm bằng chứng: từng cạnh `(từ, đến, loại quan hệ, trọng số)` và `total_confidence`.

```python
path = nx.dijkstra_path(G, source="Alice", target="Carol", weight="weight")
all_p = list(nx.all_simple_paths(G, "Alice", "Carol", cutoff=4))
k_p = list(nx.shortest_simple_paths(G, "Alice", "Carol", weight="weight"))
```

Trong Cypher thì ràng buộc bằng `WHERE all(r in relationships(path) WHERE r.confidence > 0.7)`.

**Kiểm tra**

Đường trả về phải không đi qua cạnh dưới ngưỡng 0.7. Với đồ thị mẫu, đường ít bước phải là `['Alice','Bob','Carol']`, còn đường trọng số phải đổi sang nhánh khác nếu nhánh đó có cạnh yếu. In ra `evidence` và kiểm tra từng cặp liền kề có thật trong graph không.

---

## Q3. Graph không có cạnh nối trực tiếp, làm sao trả lời "ai có ảnh hưởng tới Carol?" mà không bịa? [→ §3 Inference Rules]

**Bạn sẽ thấy**

Trong graph không có cạnh nào nối `Alice` với `Carol` — chỉ có `Alice —MANAGES→ Bob` và `Bob —MANAGES→ Carol`. Hệ thống trả lời "không tìm thấy", dù ai cũng biết Alice là sếp gián tiếp. Nếu bạn tự chèn cạnh `Alice —INDIRECTLY_MANAGES→ Carol` thì lại mất thông tin "cái này là suy ra, không phải dữ liệu gốc".

**Vì sao**

Graph thật luôn **thưa** (sparse): không thể lưu mọi quan hệ dẫn xuất. Vấn đề thứ hai là **độ tin cậy**: quan hệ suy ra yếu hơn quan hệ gốc, nên phải gắn số đi riêng thay vì trộn vào cùng một loại cạnh.

**Làm gì**

1. Khai báo luật dạng "nếu mẫu này xuất hiện thì tạo cạnh này", mỗi luật mang tên, `confidence` và phần mô tả.
2. Máy quét graph, khớp mẫu, sinh cạnh suy ra kèm `evidence` (chuỗi cạnh gốc) để luôn truy vết được.
3. Giảm độ tin cậy theo chuỗi: Alice 0.95 × Bob 0.90 = **0.855** bằng phép nhân, hoặc lấy giá trị yếu nhất là **0.90**.
4. Khi trả lời, luôn kèm đường suy luận để người đọc thấy "kết luận này từ cạnh gốc nào".

```python
INFERENCE_RULES = [{"name": "transitive_manages",
  "pattern": [("A","MANAGES","B"),("B","MANAGES","C")],
  "infer": ("A","INDIRECTLY_MANAGES","C"), "confidence": 0.8}]
inferred = apply_rules(G, INFERENCE_RULES)
# Alice -[INDIRECTLY_MANAGES]-> Carol via transitive_manages
```

**Kiểm tra**

Trên graph 50 node với 5 luật, đếm số cạnh suy ra và đối chiếu tay từng cạnh: có cạnh nào sai logic không, có cạnh "bịa" không. Mỗi cạnh suy ra phải truy ngược lại được chuỗi `evidence`.

---

## Q4. Hỏi "quý 2/2024 Alice quản lý team nào?" thì hệ thống trả về TeamB — sai mốc thời gian [→ §5 Temporal Reasoning]

**Bạn sẽ thấy**

Câu hỏi về quý 2/2024, hệ thống trả lời `TeamB`. Nhưng `TeamB` chỉ có hiệu lực từ **2024-07-01**. Còn `TeamA` mới là team đúng vào **2024-03-01**. Kết quả: người đọc tin vào con số cũ, hoặc ra quyết định sai — đây chính là nhóm lỗi gọi là "câu trả lời lỗi thời", các nghiên cứu 2024 đo được giảm tới **35%** khi thêm suy luận theo thời gian.

**Vì sao**

Quan hệ trong đời thực có ngày bắt đầu và ngày kết thúc: nhân viên đổi team, dự án bị hủy, hợp đồng hết hạn. Nếu bạn **xoá** cạnh cũ mỗi khi cập nhật thì vĩnh viễn không trả lời được câu hỏi "hồi tháng 3 năm ngoái thế nào".

**Làm gì**

1. Mọi cạnh mang hai thuộc tính `valid_from` và `valid_until`; `valid_until = None` nghĩa là đang còn hiệu lực.
2. Xem như ngày `9999-12-31` cho cạnh chưa hết hạn, rồi lọc theo điều kiện `valid_from <= ngày_hỏi <= valid_until`.
3. Khi cập nhật quan hệ, **không xoá cạnh cũ**: đóng hạn nó bằng `valid_until` rồi tạo cạnh mới.
4. Trả lời kèm khoảng thời gian để câu trả lời tự nói "đúng trong giai đoạn này".

```python
query_at_time(edges, date(2024, 3, 1), "Alice")  # → TeamA
query_at_time(edges, date(2024, 8, 1), "Alice")  # → TeamB
# Cypher: WHERE r.valid_from <= date('2024-03-01') <= r.valid_until
```

**Kiểm tra**

Tạo 20 cạnh có khoảng hiệu lực khác nhau, hỏi cùng một câu ở hai mốc 2023-06-01 và 2024-06-01: kết quả phải khác nhau và khớp đúng dữ liệu. Sau khi cập nhật, kiểm tra cạnh cũ vẫn còn trong graph với `valid_until` đã đóng.

---

## Q5. Nên để LLM tự suy luận hết, hay chia nhỏ ra cho code đi? [→ §7 Neuro-Symbolic QA]

**Bạn sẽ thấy**

Bạn giao nguyên câu hỏi cho LLM và bảo nó "tự suy luận trong graph đi". Nó trả lời trôi chảy, nhưng bạn không biết nó dựa vào cạnh nào, và khi graph có vài chục nghìn node thì mỗi câu hỏi tốn hàng chục nghìn token, chậm và đắt. Ngược lại, cách chia Planner / Executor / Reasoner thì đạt micro-F1 trên 0.90 với chi phí tính toán thấp hơn nhiều.

**Vì sao**

LLM "nhớ" tri thức từ tham số nên hay nhầm lẫn, còn graph là dữ liệu thật có thể kiểm chứng từng bước. Nếu để LLM vừa lên kế hoạch vừa tra cứu vừa kết luận, ta mất cả độ chính xác lẫn khả năng truy vết.

**Làm gì**

1. **Kiểu Think-on-Graph**: mỗi bước LLM chỉ thăm 1–2 node, xem danh sách hàng xóm rồi tự chọn hướng; hỏng hướng thì đổi nhánh.
2. **Kiểu Planner–Executor–Reasoner** (PER): Planner (LLM) sinh danh sách bước như `["FIND","GET_REPORTER","GET_PROJECT","SUM"]`; Executor (code BFS) chạy từng bước; Reasoner (LLM) chỉ đọc kết quả để tổng hợp.
3. Muốn độ chính xác cao mà chưa tin LLM: cho phép KG-Agent thao tác graph qua API để **thêm quan hệ mới và viết bằng chứng** khi tìm thiếu.
4. Cân nhắc chi phí: PER rẻ hơn vì bước Executor không tốn token LLM.

**Kiểm tra**

Chạy cùng 50 câu hỏi multi-hop với hai cách; so sánh độ đúng, số token tiêu thụ, và khả năng chỉ ra được chuỗi cạnh dẫn tới đáp án cho từng câu.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: README.md.*