# ❓ FAQ — Nền tảng Graph (chuyện thật, dễ hiểu)

Câu hỏi nào khó hiểu thì đọc `../README.md` phần trong ngoặc.

---

## Q1. Graph của tôi 100 nghìn node, dùng ma trận kề là máy chết — lưu kiểu nào cho đỡ tốn bộ nhớ? [→ §3 Biểu Diễn Graph]

**Bạn sẽ thấy**

Gọi `nx.adjacency_matrix(G).todense()` trên graph 100.000 node và máy treo hoặc báo hết bộ nhớ. Vì ma trận kề phải dựng đủ 100.000 × 100.000 ô = 10 tỷ ô, dù mỗi ô chỉ chứa 0 hoặc 1. Trong khi đó graph của bạn chỉ có vài chục nghìn cạnh — nghĩa là phần lớn 10 tỷ ô đó là số 0 vô dụng.

**Vì sao**

Ma trận kề (adjacency matrix) được thiết kế cho graph **đặc** (dense): mọi cặp node đều có quan hệ. Còn graph tri thức của bạn **rất thưa** (sparse): 100 nghìn node nhưng chỉ vài chục nghìn cạnh. Stanford CS224W đã chỉ ra chọn sai kiểu biểu diễn trên graph thưa làm chậm tới **100×**.

**Làm gì**

1. Bắt đầu bằng **danh sách kề** (adjacency list) — `O(V + E)`, NetworkX dùng sẵn kiểu này, tìm "ai kề ai" rất nhanh.
2. Cần lưu file / truyền qua mạng → **danh sách cạnh** (edge list), nhẹ nhất `O(E)`, xuất ra CSV/parquet thoải mái.
3. Trên 1 triệu node, cần huấn luyện mạng nơ-ron đồ thị → **CSR** (dạng nén), vừa gọn như list vừa duyệt nhanh.
4. Muốn giảm ma trận dành: chuyển sang biểu diễn "thưa" (sparse) bằng `scipy`, đừng `.todense()`.
5. Nguyên tắc cho người mới: **đừng tối ưu sớm**. Chỉ đổi cách lưu khi bạn *đo được* vấn đề (chậm, hết RAM), không phải vì nghe nói "ma trận tốn".

```python
import networkx as nx
G = nx.karate_club_graph()             # 34 node, rất thưa
A = nx.to_scipy_sparse_array(G)
print(A.nnz, A.shape)                  # 78 ô khác 0 trên 1.156 ô
# shape (34, 34) — cùng dữ liệu này ở 100K node sẽ là (100000, 100000)
```

**Kiểm tra**

In `A.nnz` (số ô khác 0) và so với tổng số ô. Nếu nhỏ hơn 1% tổng thì graph thưa → dùng list/CSR. Sau đó chạy Lab 2 trong README: tạo `nx.erdos_renyi_graph(10000, 0.001)`, đo `nx.shortest_path` và `nx.degree_centrality`; nếu ra kết quả tính bằng mili giây thì cách lưu hiện tại không phải nút thắt của bạn.

---

## Q2. Tôi lưu quan hệ kiểu vô hướng, hỏi "ai báo cáo cho ai" thì ra kết quả sai — chọn loại graph nào? [→ §2 Các Loại Graph]

**Bạn sẽ thấy**

Bạn dùng `nx.Graph()` (vô hướng) rồi thêm `add_edge("Alice", "Bob", relation="REPORTS_TO")`. Truy vấn kiểu "Alice liên quan với Bob" chạy rất đẹp. Nhưng hỏi "ai báo cáo cho ai" thì ra cả hai chiều: hệ thống khẳng định Bob cũng báo cáo cho Alice — sai hoàn toàn. Trường hợp nặng hơn: quan hệ đã hết hạn năm 2024 vẫn được trả lời như đang hiệu lực.

**Vì sao**

`nx.Graph()` nghĩa là A—B giống hệt B—A: cạnh không có mũi tên, nên thông tin hướng bị xoá ngay lúc ghi. Doanh nghiệp thì đầy quan hệ một chiều: Alice `REPORTS_TO` Bob, không có nghĩa ngược lại. Ngoài ra quan hệ còn có **thời hạn** (Alice `WORKS_AT` Công ty X giai đoạn [2020, 2024), Công ty Y giai đoạn [2024, nay)).

**Làm gì**

1. Không chắc thì dùng `nx.DiGraph()` — có hướng, không mất thông tin. Chỉ dùng vô hướng khi bản chất quan hệ là hai chiều như nhau (`COLLABORATES_WITH`).
2. Nhiều loại thực thể trong cùng một graph (Person, Project, Document) → đó là graph **heterogeneous**, khai báo rõ `node_types` và `edge_types`.
3. Quan hệ có thời gian → gắn `valid_from` / `valid_until` vào cạnh, lúc truy vấn thì lọc theo mốc thời gian, quan hệ đã hết hạn không được trả lời.
4. Phân biệt 2 kiểu dữ liệu: **homophily** (cùng loại thì hay nối nhau — mạng xã hội) và **heterophily** (khác loại mới nối nhau — mạng phát hiện gian lận, virus, tấn công mạng). Mô hình đồ thị tiêu chuẩn mặc định giả định homophily, nên chạy trên graph loại thứ hai sẽ cho kết quả kém mà không rõ nguyên nhân.

```python
G = nx.DiGraph()                          # có hướng
G.add_edge("Alice", "Bob", relation="REPORTS_TO")
G.add_edge("Alice", "CompanyY", type="WORKS_AT",
           valid_from=2024, valid_until=None)   # None = còn hiệu lực
```

**Kiểm tra**

Hỏi "Bob báo cáo cho Alice không?" — với `DiGraph` phải trả về rỗng. Rồi thử một truy vấn có điều kiện thời gian và xác nhận quan hệ có `valid_until = 2024` không còn xuất hiện. Nếu hai bước này đều đúng thì bạn đã giữ được cả hướng lẫn thời gian.

---

## Q3. Bên tôi toàn dùng RDF và SPARQL, có phải bỏ hết sang Neo4j/Cypher không? [→ §5 Property Graph vs RDF]

**Bạn sẽ thấy**

Team của bạn mô tả dữ liệu bằng ontology (bộ luật định nghĩa thực thể), truy vấn bằng SPARQL. Mọi thuộc tính gắn trên quan hệ đều phải "bọc lại" thành một node trung gian (reification) — đội phát triển phải làm thêm bước này mỗi lần. Kết quả: câu hỏi duyệt 2–3 bước (traversal) chậm hơn property graph **3–5 lần** theo benchmark Neo4j 2024.

**Vì sao**

Property Graph cho phép thuộc tính nằm thẳng trên node và cạnh (`edge.weight = 0.9`), schema linh hoạt theo nhãn, truy vấn bằng Cypher trông như vẽ hình. RDF Triple Store thì đơn vị là bộ ba (chủ thể – vị – đối tượng) cộng định chỉ URI, schema phải tuân ontology chặt, suy luận (OWL reasoning) thì có sẵn — nhưng thuộc tính trên cạnh thì phức tạp.

**Làm gì**

1. Trả lời theo nhu cầu thật, không theo sở thích: dữ liệu liên tổ chức, cần ontology hoặc suy luận OWL → giữ RDF/SPARQL. Knowledge graph nội bộ, GraphRAG, truy vấn nhiều bước → chuyển sang Property Graph.
2. Với framework này, khuyến nghị Property Graph (Neo4j / Kuzu / NetworkX); RDF chỉ dùng khi phải làm việc với dữ liệu liên kết mở.
3. Cypher học nhanh vì gần tiếng Việt: `MATCH` là "tìm", `-[:TEN_LOAI]->` là "có quan hệ", `*1..2` là đi từ 1 đến 2 bước.
4. Nhớ bỏ qua `rdf:type` khi so sánh schema: Property Graph đã dùng nhãn (label) làm kiểu dữ liệu rồi.

```cypher
CREATE (a:Person {name:'Alice', role:'CTO'})
CREATE (p:Project {name:'Phoenix', budget:500000})
CREATE (a)-[:MANAGES {since:'2024-01-01', confidence:0.95}]->(p)
MATCH (who:Person)-[:MANAGES|WORKS_ON*1..2]->(proj:Project {name:'Phoenix'})
RETURN who.name, proj.name
```

**Kiểm tra**

Chạy cùng một câu hỏi duyệt 3 bước trên cả hai hệ thống và so thời gian trả lời. Nếu dự án của bạn không có ontology sẵn, không cần suy luận OWL, và người mới phải tự viết truy vấn — Property Graph là lựa chọn ít ma sát hơn rõ rệt.

---

## Q4. 10 nghìn node trong tay, muốn biết ai "quan trọng" và chỗ nào nghẽn — đo cái gì? [→ §4 Metrics & Đặc Trưng]

**Bạn sẽ thấy**

Bạn hỏi "ai là trung tâm của mạng lưới nội bộ?" và đếm số quan hệ của từng người. Kết quả ra người ghi nhiều email nhất — họ có 50 quan hệ nhưng 48 là quan hệ xã giao, không ai phải qua họ. Sau đó bạn hỏi "bỏ ai thì quy trình duyệt bị nghẽn?" và đo y hệt, ra lại đúng người đó. Hai câu hỏi khác nhau, một công cụ đo.

**Vì sao**

Mỗi thước đo trả lời đúng một câu hỏi. **Degree** = số quan hệ. **Betweenness** = nằm trên bao nhiêu đường ngắn nhất nối các cặp người khác (tức làm cầu nối). **PageRank** = được các node quan trọng "phiếu". **Clustering** = bạn bè của người này có quen nhau không. **Modularity / Density** = các nhóm có tách biệt rõ, graph đặc hay thưa.

**Làm gì**

1. Chọn thước đo theo câu hỏi, không chọn theo "cái nào nghe hay".
2. Muốn biết "traverse mấy bước là đủ để không bỏ sót", dùng **Diameter** (khoảng cách xa nhất) và **average shortest path length**.
3. Đo trên graph nhỏ trước (`nx.karate_club_graph()`, 34 node) để hiểu ý nghĩa từng con số, rồi mới áp lên dữ liệu thật.
4. Với GraphRAG (tìm kiếm trên đồ thị), hai thước đo quan trọng nhất là **Clustering** và **Modularity** — chúng quyết định cách chia cụm để tóm tắt.

| Câu hỏi | Dùng thước đo |
|---|---|
| Ai kết nối nhiều nhất | Degree centrality |
| Ai làm nghẽn quy trình | Betweenness |
| Ai có ảnh hưởng dù ít giao tiếp | PageRank |
| Chia 1.000 thực thể thành chủ đề | Clustering + Modularity |

```python
G = nx.karate_club_graph()          # 34 node mẫu
print(nx.average_clustering(G))     # bạn bè có quen nhau không
b = nx.betweenness_centrality(G)
print(max(b, key=b.get))            # cầu nối
print(nx.diameter(G), nx.average_shortest_path_length(G))
```

**Kiểm tra**

Trên graph thật, so sánh top-3 theo Degree với top-3 theo Betweenness. Nếu hai danh sách trùng nhau hết, bạn đang đo một thứ hai lần — hãy thử PageRank rồi xem bảng xếp hạng có thay đổi không. Nếu có, bạn đã tìm ra câu trả lời đúng cho từng câu hỏi.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: README.md.*