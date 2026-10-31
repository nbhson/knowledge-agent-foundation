# 🔢 04. Graph Embeddings — Vector Hóa Đồ Thị

> ## 📑 Mục Lục
>
> - [Câu Chuyện Mở Đầu](#câu-chuyện-mở-đầu)
> - [Tại Sao Graph Embeddings Quan Trọng?](#tại-sao-graph-embeddings-quan-trọng)
> - [Tổng Quan](#tổng-quan)
> - [Nội Dung](#nội-dung)
> - [1. Graph Embeddings Là Gì?](#1-graph-embeddings-là-gì)
> - [2. Shallow Embeddings: Node2Vec, DeepWalk](#2-shallow-embeddings-node2vec-deepwalk)
> - [3. GNN-Based Embeddings: GraphSAGE, GAT](#3-gnn-based-embeddings-graphsage-gat)
> - [4. Knowledge Graph Embeddings: TransE, RotatE](#4-knowledge-graph-embeddings-transe-rotate)
> - [5. Hybrid Search: Vector + Graph](#5-hybrid-search-vector--graph)
> - [6. Labs Thực Hành](#6-labs-thực-hành)
> - [Tài Liệu Tham Khảo](#tài-liệu-tham-khảo)

---

### Câu Chuyện Mở Đầu

Bạn có Knowledge Graph với 10,000 nodes. User hỏi: *"Tìm người giống Alice nhất về vai trò và mối quan hệ."*

- **Graph traversal**: tìm người có cùng số neighbors? Không đủ — Alice quản lý 5 người, Bob cũng quản lý 5 người nhưng team khác hoàn toàn.
- **Text embedding**: embed `description` của Alice và so sánh? Bỏ qua toàn bộ cấu trúc graph.
- **Graph embedding**: mỗi node thành vector **dựa trên vị trí trong graph** → `cosine(alice_vec, bob_vec)` cao nếu họ có vai trò/cấu trúc tương tự.

**Graph Embeddings biến cấu trúc đồ thị thành vector — để vừa dùng được ANN search, vừa giữ được thông tin quan hệ.**

> **Tóm gọn 1 câu:** Graph embedding = "chụp ảnh" mỗi node thành dãy số, sao cho hai node giống nhau về vai trò/cấu trúc thì hai bức ảnh giống nhau — và dãy số thì máy so sánh được cực nhanh.

### Tại Sao Graph Embeddings Quan Trọng?

> *"Graph tells you WHO is connected. Embeddings tell you WHO IS SIMILAR without being directly connected."*
>
> (Dịch: graph cho biết AI nối với AI; embedding cho biết AI GIỐNG AI dù không nối trực tiếp.)

> **Cách đọc bảng này:** mỗi dòng là 1 nghiên cứu/benchmark; cột "Phát Hiện" nói nó đo được điều gì. Ví dụ, dòng 1: dùng graph embeddings giúp đoán quan hệ còn thiếu chính xác hơn 22%.

| # | Nguồn | Phát Hiện |
|---|-------|-----------|
| 1 | **Node2Vec Paper (2016)** | Graph embeddings tăng **22% accuracy** trên link prediction so với chỉ dùng node features |
| 2 | **Microsoft GraphRAG (2024)** | Kết hợp text embeddings + graph embeddings tăng **18% retrieval precision** |
| 3 | **OGB Benchmark (2024)** | GraphSAGE embeddings + ANN search nhanh hơn traversal thuần **50×** cho k-NN queries trên 1M nodes |

---

## Tổng Quan

Phần này chỉ ra 3 đường đi: biến chữ thành vector, biến vị trí trong graph thành vector, rồi pha cả hai lại thành 1 điểm số.

```
Knowledge Graph
    │
    ├──► Text Embeddings ──► Vector DB (semantic search)
    │      "Alice là CTO" → [0.23, -0.45, ...]
    │
    ├──► Graph Embeddings ──► Vector DB (structural search)
    │      vị trí của Alice trong graph → [0.67, 0.12, ...]
    │
    └──► Hybrid ──► Fused Score: α·text_score + (1-α)·graph_score
           Best of both worlds
```

---

## Nội Dung

> **Cách đọc bảng này:** cột "Chủ đề" là mục con bên dưới; cột "Mô tả" tóm tắt mục đó gồm những gì. Ví dụ, dòng 4 nói: phần KG Embeddings dạy TransE, RotatE và cách đoán quan hệ còn thiếu.

| # | Chủ đề | Mô tả |
|---|--------|-------|
| 1 | [Graph Embeddings Là Gì?](#1-graph-embeddings-là-gì) | Định nghĩa, intuition, phân loại |
| 2 | [Node2Vec/DeepWalk](#2-shallow-embeddings-node2vec-deepwalk) | Random walk embeddings |
| 3 | [GNN Embeddings](#3-gnn-based-embeddings-graphsage-gat) | GraphSAGE, GAT |
| 4 | [KG Embeddings](#4-knowledge-graph-embeddings-transe-rotate) | TransE, RotatE cho KG completion, TKGE, Graph Transformers |
| 5 | [Hybrid Search](#5-hybrid-search-vector--graph) | Kết hợp vector + graph (RRF, weighted) |

---

## 1. Graph Embeddings Là Gì?

> **📌 Khái Niệm Cơ Bản:**
> **Graph Embedding** = cách biến nodes trong graph thành **dãy số (vector)** sao cho:
> 1. Nodes **gần nhau trong graph** → vector gần nhau (distance nhỏ)
> 2. Nodes **có vai trò giống nhau** → vector gần nhau (dù không kề nhau)
>
> **Tại sao cần?** Vì vector vừa **so sánh được bằng cosine similarity** (cosine = đo hai vector "cùng hướng" bao nhiêu — 1 là giống hệt, 0 là không liên quan), vừa **lưu vào vector DB** để search nhanh bằng ANN (ANN = Approximate Nearest Neighbor — tìm "gần giống nhất" mà không phải so từng cặp, đổi chút độ chính xác lấy tốc độ). Graph structure → vector space → dùng được cho RAG, clustering, classification.

**Analogies để hiểu:**
- **Đồ thị = Bản đồ thành phố**: Graph embedding = GPS coordinates (vĩ độ, kinh độ) — mỗi thành phố (node) có tọa độ, thành phố gần nhau trong bản đồ sẽ có tọa độ gần nhau
- **Graph embedding = Photo portrait**: Mỗi node được "chụp ảnh" dưới dạng vector — thấy rõ feature gì quan trọng (position, role, community)

### 1.1 Intuition

```
Graph (cấu trúc rời rạc)  ──Embed──►  Vector Space (liên tục, so sánh được)

Alice ──MANAGES──► Bob              alice_vec = [0.23, 0.81, -0.15, ...]
  │                  │              bob_vec   = [0.25, 0.79, -0.12, ...]  ← gần alice!
  └─WORKS_ON──► Phoenix            phoenix_vec = [0.88, 0.10, 0.42, ...]  ← xa hơn (loại khác)

Khoảng cách gần trong vector space = Vai trò/cấu trúc giống nhau trong graph
```

**Mục tiêu cuối cùng:** Học hàm `f: V → R^d` (từ node → vector số thực d chiều) sao cho:
- Nodes gần nhau trong graph → vectors gần nhau
- Nodes có vai trò tương tự → vectors gần nhau (dù không kề nhau)

**Tại sao điều này khó hơn text embedding thông thường?** Text embedding chỉ cần hiểu **nội dung** (Alice = "CTO" "quản lý"). Graph embedding cần hiểu cả **vị trí trong cấu trúc** (Alice nằm ở vị trí "trung tâm" kết nối nhiều nodes khác).

### 1.2 Phân Loại

> **Cách đọc bảng này:** 4 họ phương pháp, chia theo "cần training kiểu gì" và "dùng vào việc gì". Ví dụ, Node2Vec không cần nhãn, hợp tìm node giống nhau; TransE/RotatE hợp đoán quan hệ còn thiếu trong knowledge graph.

```
┌──────────────────────┬──────────────────────┬───────────────────────────────┐
│ Loại                 │ Cần training?        │ Phù hợp nhất khi              │
├──────────────────────┼──────────────────────┼───────────────────────────────┤
│ Node2Vec / DeepWalk  │ Unsupervised (walks) │ General similarity, clustering│
│ GraphSAGE / GAT      │ Supervised / Semi    │ Node classification, inductive│
│ TransE / RotatE      │ KG triples           │ KG completion, link prediction│
│ Text + Graph Hybrid  │ Cả hai               │ GraphRAG, enterprise search   │
└──────────────────────┴──────────────────────┴───────────────────────────────┘
```

---

## 2. Shallow Embeddings: Node2Vec, DeepWalk

> **📌 Khái Niệm Cơ Bản:**
> **Random Walk** = đi bộ ngẫu nhiên trong graph — mỗi bước chọn 1 neighbor ngẫu nhiên để đi tới.
> **DeepWalk/Node2Vec** = tạo nhiều "con đường ngẫu nhiên" trong graph → dùng Word2Vec (cùng công nghệ hiểu từ trong NLP) để hiểu vị trí của mỗi node.
>
> **Tại sao gọi là "shallow"?** Vì mỗi node có 1 vector riêng (đúng 1-1, như từ điển) — nên phải train lại nếu thêm node mới. Nên chỉ phù hợp graph nhỏ.

**Analogies:**
- **Random Walk = đi chơi quanh phố**: Bạn xuất phát tại "Alice", mỗi ngã rẽ chọn hướng ngẫu nhiên → xem những nơi nào bạn thường xuyên đi qua. Nếu "Alice" và "Bob" thường xuyên gặp nhau trên những con đường giống nhau → họ ở khu vực giống nhau.
- **DeepWalk = Google Maps nhưng đi lạc đường**: cứ đi ngẫu nhiên quanh khu vực, ghi lại những nơi đã đi qua → từ đó hiểu được cấu trúc của cả vùng.

### 2.1 DeepWalk — Random Walk + Word2Vec

> **Nguyên tắc:** Chuyển graph thành "văn bản" bằng cách tạo random walks → dùng Word2Vec (Skip-gram) để học embedding.

```
Ví dụ minh họa:

Graph: Alice → Bob → Carol → Dave
                    ↘ Phoenix

Bước 1: Tạo nhiều random walks (đi bộ ngẫu nhiên)
  Walk 1: Alice → Bob → Carol → Dave     (mỗi bước chọn random neighbor)
  Walk 2: Alice → Bob → Phoenix → Bob
  Walk 3: Bob → Phoenix → Bob → Alice

Bước 2: Coi mỗi walk là 1 "câu" (sentence), mỗi node là 1 "từ" (word)
  → "Alice Bob Carol Dave" = 1 câu
  → Word2Vec learns: "Alice" hay xuất hiện cùng "Bob" → 2 vector gần nhau

Kết quả: Node nào hay "xuất hiện cùng nhau trên các con đường ngẫu nhiên" → vector gần nhau
```

### 2.2 Node2Vec — Biased Random Walk (thêm kiểm soát)

> **Điểm mới so với DeepWalk:** Thêm 2 tham số `p` và `q` để **kiểu soát hướng đi** — thay vì đi hoàn toàn ngẫu nhiên, bạn quyết định "đi xa" hay "đi gần".

> 📄 **Code ví dụ:** [`examples/01-2-2-node2vec-biased-random-walk-them-kiem.py`](examples/01-2-2-node2vec-biased-random-walk-them-kiem.py)

<details>
<summary>Python Code — Node2Vec với NetworkX (Click để xem)</summary>

> 📄 **Code ví dụ:** [`examples/02-2-2-node2vec-biased-random-walk-them-kiem.py`](examples/02-2-2-node2vec-biased-random-walk-them-kiem.py)

</details>

### 2.3 Khi Nào Dùng Node2Vec?

> **Cách đọc bảng này:** cột "Dùng?" là dấu ✅ (nên dùng) hoặc ❌ (kém hợp); cột "Lý do" giải thích. Ví dụ, dòng 2: node mới thêm liên tục thì Node2Vec phải học lại toàn bộ — nên chuyển sang GraphSAGE.

| Tình huống | Dùng? | Lý do |
|-----------|-------|-------|
| Graph nhỏ-medium (<100K nodes) | ✅ | Nhanh, không cần GPU, unsupervised |
| Cần inductive (thêm node mới) | ❌ | Phải retrain toàn bộ — dùng GraphSAGE thay thế |
| Cần edge features / node features | ❌ | Node2Vec chỉ dùng cấu trúc — dùng GNN |
| Clustering / community detection | ✅ | Embeddings phản ánh community structure tốt |

> **Tóm gọn 1 câu:** Node2Vec = đi bộ ngẫu nhiên rồi học như học từ: rẻ, không cần GPU, nhưng node mới là phải học lại — chỉ hợp graph nhỏ và ít thay đổi.

---

## 3. GNN-Based Embeddings: GraphSAGE, GAT

> **📌 Khái Niệm Cơ Bản:**
> **Vấn đề:** Node2Vec phải **retrain toàn bộ** khi có node mới (vì mỗi node có 1 vector riêng).
> **Giải pháp:** **GNN (Graph Neural Network)** học một **hàm tổng hợp** (aggregate function) — *bất kể node nào, chỉ cần nhìn neighbors của nó là có thể tính vector*. → Thêm node mới thì chỉ cần "chạy hàm" cho node đó, không retrain.
>
> **Analogies:**
> - **Node2Vec = Chụp hình cố định**: Mỗi người phải đứng yên chụp 1 tấm ảnh riêng. Người mới tham gia → phải chụp lại cả nhóm.
> - **GraphSAGE = Mô tả bạn qua bạn bè**: Bất kỳ ai cũng có thể được mô tả = "trung bình của bạn bè họ" + "đặc điểm riêng". Người mới → chỉ cần hỏi bạn bè của họ là mô tả được ngay.

### 3.1 GraphSAGE — Inductive Node Embeddings

> **Đọc thêm về công thức:** GraphSAGE học hàm **aggregate** (gộp) thông tin từ neighbors, nên có thể embed **node mới chưa từng thấy** mà không retrain.

```
Công thức (dịch ra tiếng người):

  h_v^k = σ( W^k · CONCAT( h_v^{k-1}, AGGREGATE({h_u^{k-1} : u ∈ N(v)}) ) )

Giải thích từng ký hiệu:
  h_v^k    = embedding của node v SAU lớp k (đã "nghe" thông tin cách k hops)
  h_v^{k-1}= embedding TRƯỚC đó (cách k-1 hops)
  N(v)     = neighbors (bạn bè xung quanh) của v
  AGGREGATE= cách "gộp" thông tin từ bạn bè:
              MEAN (lấy trung bình) / LSTM / MAX-pooling
  CONCAT   = "nối lại": nối vector [tôi trước đó] + [bạn bè của tôi]
  W^k      = weights (hệ số học được) — biến thành "bộ lọc" để biến hóa thông tin
  σ        = activation function (thường ReLU — loại bỏ giá trị âm)

Đọc là: "Embedding mới của tôi = pha trộn (đặc điểm riêng của tôi) với (gộp đặc điểm của bạn bè tôi), rồi biến hóa bằng 1 lớp neural"

K layers = K vòng "hỏi bạn bè" — node cuối cùng biết thông tin cách K hops
  Layer 1: biết bạn bè trực tiếp (1 hop)
  Layer 2: biết bạn bè của bạn bè (2 hops)
  Layer 3: biết bạn bè của bạn bè của bạn bè (3 hops)
```

> 📄 **Code ví dụ:** [`examples/03-3-1-graphsage-inductive-node-embeddings.py`](examples/03-3-1-graphsage-inductive-node-embeddings.py)

### 3.2 GAT — Graph Attention Networks

> **📌 Khái Niệm Cơ Bản:**
> **Vấn đề:** GraphSAGE gộp bạn bè bằng **trung bình cộng (uniform `mean`)** — nghĩa là xem mọi bạn bè = quan trọng như nhau.
> **Giải pháp (GAT):** Học **attention weights (trọng số chú ý)** — node tự quyết định bạn bè nào quan trọng hơn. Giống như khi bạn nghe lời khuyên: lời của mentor có trọng lượng hơn lời của người mới quen.

```
Công thức (dịch ra tiếng người):

  α_{vu} = softmax( LeakyReLU( a^T [W h_v || W h_u] ) )
  h_v' = σ( Σ_{u∈N(v)} α_{vu} · W h_u )

Giải thích:
  α_{vu} = "độ quan trọng" của neighbor u đối với node v  (tổng = 1, nhờ softmax)
  Trước  = mỗi neighbor góp RÕ RÀNG (trung bình)
  GAT    = neighbor nào đáng tin cậy thì góp NHIỀU hơn

Ví dụ trực quan:
  Org chart: Alice có neighbors: Bob (báo cáo trực tiếp) + Dave (quen biết xã giao)
  AGGREGATE (GraphSAGE): Bob góp 50% + Dave góp 50%
  ATTENTION (GAT):       Bob góp 83% + Dave góp 17%  ← học được "MANAGES quan trọng hơn KNOWS"
```

<details>
<summary>Python Code — GraphSAGE với PyG (Click để xem)</summary>

> 📄 **Code ví dụ:** [`examples/04-3-2-gat-graph-attention-networks.py`](examples/04-3-2-gat-graph-attention-networks.py)

</details>

### 3.3 So Sánh

> **Cách đọc bảng này:** so sánh 3 mô hình theo từng tiêu chí. Ví dụ, dòng "Inductive?": Node2Vec không xử lý được node mới (❌), GraphSAGE và GAT xử lý được (✅). Dòng "Attention?": chỉ GAT tự học "nghe ai nhiều hơn".

```
┌─────────────────┬──────────────────┬──────────────────┬──────────────────────┐
│ Thuộc tính      │ Node2Vec         │ GraphSAGE        │ GAT                  │
├─────────────────┼──────────────────┼──────────────────┼──────────────────────┤
│ Inductive?      │ ❌ (transductive) │ ✅               │ ✅                   │
│ Cần features?   │ ❌ (chỉ structure)│ ✅               │ ✅                   │
│ Attention?      │ ❌ (uniform)     │ ❌ (mean)        │ ✅ (learned weights) │
│ Scalability     │ O(walks × len)   │ O(E) per layer   │ O(E) + attention     │
│ Training        │ Unsupervised     │ Supervised/Semi  │ Supervised           │
│ Best for        │ Clustering, viz  │ Classification   │ Heterogeneous, ranked│
└─────────────────┴──────────────────┴──────────────────┴──────────────────────┘
```

> **Tóm gọn 1 câu:** GNN học hàm gộp thông tin từ bạn bè nên thêm node không phải học lại; GAT còn tự học "nghe ai nhiều hơn" thay vì lấy trung bình đều.

---

## 4. Knowledge Graph Embeddings: TransE, RotatE

> **📌 Khái Niệm Cơ Bản:**
> **KG Embedding** khác Node2Vec/GNN ở chỗ: học **cả node VÀ relation cùng lúc** — mục tiêu là **link prediction**: dự đoán quan hệ còn thiếu.
>
> **Analogies:**
> - **TransE = Phép dịch chuyển (translation)**: `vec(Alice) + vec(WORKS_ON) ≈ vec(Phoenix)`. Giống như điều hướng: "Từ Alice, đi theo hướng WORKS_ON sẽ đến Phoenix". Nếu một project khác phù hợp với hướng này → dự đoán được.
> - **RotatE = Phép quay (rotation)**: relation là "góc quay" — xoay vector Alice một góc để ra vector Phoenix. Hợp lý cho quan hệ đối xứng như "married" (quay 180°).

KG embeddings học **cả node và relation** cùng lúc — để làm **link prediction**: `(Alice, WORKS_ON, ?)` → dự đoán project nào.

### 4.1 TransE — Translation Principle

> **Ý tưởng cốt lõi (dễ nhất):** Nếu triple `(Alice, WORKS_ON, Phoenix)` đúng, thì:
> **vector(Alice) + vector(WORKS_ON) ≈ vector(Phoenix)**
>
> Nói cách khác: "Alice" + "hành động làm việc trên" ≈ "Phoenix". Relation đóng vai trò **vector dịch chuyển** — giống hướng đi và quãng đường.

```
TransE: h + r ≈ t

Nếu (Alice, WORKS_ON, Phoenix) là true:
  vec(Alice) + vec(WORKS_ON) ≈ vec(Phoenix)

Score: ||h + r - t|| → thấp = triple đúng, cao = sai

              WORKS_ON
  Alice ───────────────► Phoenix
  vec_h + vec_r  ≈  vec_t

  ❌ (Alice, WORKS_ON, Unknown) → ||h + r - t|| lớn → không hợp lệ
```

**Ví dụ cuộc sống:** Bạn có công thức "thành phố + phương hướng = nơi đến". `Hanoi + North = ThaiNguyen` (đúng), `Hanoi + North = SaiGon` (sai — vector quá xa). TransE học các vector này từ dữ liệu để dự đoán nơi đến hợp lý cho quan hệ mới.

### 4.2 RotatE — Rotation in Complex Space

> **Ý tưởng:** Thay vì relation = "dịch chuyển", RotatE xem relation = **phép quay** trên mặt phẳng phức (số phức = số có phần "ảnh" i; dùng nó cho phép biểu diễn quay một cách tự nhiên). Mỗi relation là 1 góc quay: quay vector `h` một góc = góc của relation → ra gần `t`.

```
RotatE: h ◦ r ≈ t  (◦ = element-wise rotation in complex space)

r là vector phức với |r_i| = 1 (đơn vị) → quay h để gần t

Ưu điểm: mô hình được symmetry, inversion, composition
  - (A, married_to, B) ↔ (B, married_to, A)  →  r = rotation 180°
  - (A, part_of, B) + (B, part_of, C) → (A, part_of, C)
```

**Ví dụ cuộc sống:** Quan hệ "married" giống **quay 180°**: A quay nửa vòng tròn ra B, và B quay nửa vòng tròn cũng ra A (đối xứng). TransE không làm được điều này tốt (vì `A + r = B` không suy ra `B + r = A`), RotatE thì có.

<details>
<summary>Python Code — TransE Training Loop (Click để xem)</summary>

> 📄 **Code ví dụ:** [`examples/05-4-2-rotate-rotation-in-complex-space.py`](examples/05-4-2-rotate-rotation-in-complex-space.py)

</details>

### 4.3 Temporal KG Embeddings (TKGE)

> **📌 Khái Niệm Cơ Bản:**
> **Temporal KG embeddings** = học vector biết **cả không gian lẫn thời gian** — triplet không còn là `(h, r, t)` mà là `(h, r, t, time)`, vì hầu hết tri thức KHÔNG bất biến:
> - `(Alice, WORKS_ON, Phoenix, 2023)` — đúng năm 2023
> - `(Alice, WORKS_ON, Phoenix, LATER THAN 2025)` — **sai**: Alice đã chuyển dự án
>
> **Vì sao đơn giản như vậy?** Embedding học được theo thời gian phải biết trả lời: *"mối quan hệ này còn đúng ở thời điểm X hay không?"* — đây là bài toán **Temporal Knowledge Graph Completion (TKGC)**.
>
> **Các nhóm mô hình (đọc là "các chiến lược"):**
> - **Time-parameterized translation**: thêm tham số thời gian vào TransE/RotatE (vd **TuckERTNT** tách tensor theo thời gian).
> - **Temporal message passing (GNN theo thời điểm)**: mỗi sự kiện là 1 "thời điểm giao tiếp", nodes học khi nào nhận/truyền thông tin — tiêu biểu **TGN (Temporal Graph Networks)**.
> - **Tendency-guided**: dự đoán "xu hướng thay đổi" của 1 quan hệ theo thời gian trước khi hỏi embedding.
>
> **Analogies:** TransE là "tấm bản đồ tĩnh". TKGE là **"bản đồ + hồ sơ lịch sử"** — bạn phải biết "cầu A" bị sập năm nào thì mới không đi nhầm.
>
> **Khi nào cần?** Chỉ khi graph của bạn có cột thời gian và câu hỏi phụ thuộc thời điểm (khuyến nghị, log dịch vụ, tin tức, lịch sử công việc). Nếu graph không temporal, đừng thêm phức tạp.

### 4.4 Graph Transformers (GTs) — Thế Hệ Tiếp Theo

> **📌 Khái Niệm Cơ Bản:**
> **Graph Transformers** = áp dụng cơ chế **self-attention (như trong LLM)** lên graph: mỗi node "chú ý" tới toàn bộ graph thay vì chỉ neighbors trực tiếp. Đây là hướng khắc phục giới hạn cố hữu của GNN message-passing (xem chi tiết "giới hạn" ở Module 07).
>
> **Ví dụ đặt câu hỏi dễ hình dung:** GNN = người chỉ hỏi **hàng xóm trực tiếp** (1-3 vòng). Graph Transformer = người có thể **quét toàn bộ các mối quan hệ** trong đồ thị cùng lúc để quyết định ai quan trọng nhất.
>
> **Nhánh tiêu biểu (GraphGPS, GT)** kết hợp attention toàn-graph + message passing: giữ được chuỗi local nhưng thêm "tấm nhìn xa". Giá phải trả: **tốn memory O(N²)** với N nodes — nên cần trick như "attention 1-hop nguồn" (chỉ 1 block mới attention global).
>
> **Khi nào nên (hoặc chưa nên) dùng:** graph cỡ vừa, có đường đi dài quan trọng và cần độ chính xác cao nhất → hãy chọn GT. Graph tới hàng triệu nodes → GNN truyền tin thông thường (message-passing) vẫn dễ mở rộng hơn. Phần tính toán chi tiết thuộc về Module 07 — ở module này bạn chỉ cần biết **đang có thêm họ embedding "thế hệ mới"** này.

> **Tóm gọn 1 câu:** TransE coi quan hệ là phép dịch, RotatE là phép quay; graph có yếu tố thời gian thì dùng TKGE — còn Graph Transformer nhìn xa hơn GNN nhưng tốn bộ nhớ theo bình phương số node.

---

## 5. Hybrid Search: Vector + Graph

Graph embeddings không thay thế text embeddings — chúng **bổ sung** cho nhau.

### 5.1 Kỹ Thuật Fusion

<details>
<summary>Python Code — Hybrid Search (RRF + Weighted) (Click để xem)</summary>

> 📄 **Code ví dụ:** [`examples/06-5-1-ky-thuat-fusion.py`](examples/06-5-1-ky-thuat-fusion.py)

</details>

### 5.2 Khi Nào Dùng Hybrid?

> **Cách đọc bảng này:** mỗi dòng là 1 loại câu hỏi; "Best α" là trọng số nên đặt (α càng nhỏ càng nghiêng về graph); "Strategy" là hướng đi. Ví dụ, câu hỏi tìm 1 đoạn cụ thể → α = 0.8, nghe text là chính.

```
Query type                        │ Best α  │ Strategy
──────────────────────────────────┼─────────┼──────────────────────────
Factoid (tìm đoạn văn cụ thể)     │ 0.8     │ Text-heavy
Multi-hop (nối nhiều thực thể)    │ 0.3     │ Graph-heavy
Global summary (tổng hợp)         │ 0.2     │ Graph communities
Hybrid (default)                  │ 0.5-0.6 │ Cân bằng
```

> **Tóm gọn 1 câu:** Text vector bắt "nói gì", graph vector bắt "đứng ở đâu" — pha hai điểm theo trọng số α: câu hỏi chi tiết nghiêng về text, câu hỏi tổng hợp nghiêng về graph.

---

## 6. Labs Thực Hành

### Lab 1: Node2Vec từ Scratch

1. Tạo graph 100 nodes với `nx.karate_club_graph()` hoặc org chart synthetic
2. Chạy `deepwalk_embeddings()` với `num_walks=10, walk_length=20`
3. Visualize embeddings bằng t-SNE, quan sát clustering

### Lab 2: So Sánh Node2Vec vs GraphSAGE

1. Dùng cùng graph, tạo embeddings bằng cả 2 phương pháp
2. Đo link prediction accuracy: mask 20% edges, predict lại
3. So sánh accuracy và thời gian

### Lab 3: Hybrid Search Benchmark

1. Tạo 50 queries: 25 factoid + 25 multi-hop
2. Chạy 3 modes: text-only (α=1.0), graph-only (α=0.0), hybrid (α=0.6)
3. Đo precision@5 cho từng loại query (precision@5 = trong 5 kết quả đầu, bao nhiêu phần trăm là đúng)

> **Tóm gọn 1 câu:** Lab 1 cho bạn thấy embedding "nhìn" ra sao, Lab 2 cho biết đổi mô hình thế nào khi node mới xuất hiện, Lab 3 đo xem hybrid có đáng giá không.

---

## Tài Liệu Tham Khảo

> Bài báo gốc của từng mô hình; cần hiểu sâu kỹ thuật nào thì đọc bài đó, không cần đọc hết.

- Grover & Leskovec — *Node2Vec: Scalable Feature Learning for Networks* (KDD 2016)
- Hamilton et al. — *Inductive Representation Learning on Large Graphs (GraphSAGE)* (NeurIPS 2017)
- Veličković et al. — *Graph Attention Networks* (ICLR 2018)
- *Temporal Knowledge Graph Completion: A Survey* — TGN, TuckERTNT, tendency-guided (arXiv 2024-2025)
- *Graph Transformers: A Survey* (arXiv:2502.16533) — GraphGPS, GT
- Bordes et al. — *Translating Embeddings for Modeling Multi-relational Data (TransE)* (NeurIPS 2013)
- Sun et al. — *RotatE: Knowledge Graph Embedding by Relational Rotation* (ICLR 2019)

---

## GraphRAG — Cập nhật 2026

> **Đang nói về gì:** GraphRAG = RAG có trợ giúp của đồ thị (RAG = đưa tài liệu liên quan vào prompt cho LLM trả lời). **Multi-hop** = câu hỏi cần nối 2+ bước quan hệ; **vector-only RAG** = chỉ tìm theo "giống về nghĩa", không nhìn cấu trúc.

Microsoft GraphRAG (2024-2025): dùng knowledge graph để enhance RAG. Query phức tạp (multi-hop) tốt hơn vector-only RAG.

**Tin mới 2025-2026:**
- **LazyGraphRAG** (Microsoft, cuối 2024): defer LLM summarisation tới query time — "defer" = trì hoãn bước tóm tắt đắt tiền đến khi có người hỏi, thay vì tóm trước mọi thứ — indexing cost ngang vector RAG, quality ngang full GraphRAG, query cost thấp hơn ~700×. Đã tích hợp Microsoft Discovery (2025) và Azure Local.
- **LightRAG** (HKUDS, EMNLP 2025): dual-layer graph + vector, incremental update (thêm tài liệu mới chỉ cập nhật phần thay đổi) thay vì re-index toàn bộ.
- **GraphRAG-Bench** (Microsoft, 06/2025): multi-hop + global queries GraphRAG thắng; single-hop factoid vanilla RAG thắng.
- **Gartner (2026)**: GraphRAG trong "Top Trends in D&A for 2026" cho complex cases mà high-accuracy RAG thất bại.
- **Knowledge Graph Market**: 1.48B USD (2025) → 2.04B USD (2026). GraphRAG chuyển từ "enterprise luxury" → production baseline.

Ref: https://microsoft.github.io/graphrag/

> **Tóm gọn 1 câu:** Từ 2025-2026, GraphRAG đã rẻ và phổ biến hơn nhiều — chọn đúng biến thể giúp trả các câu hỏi nhiều bước mà vector RAG bó tay.

---

*Tiếp theo: [05 — GraphRAG](../05-graph-rag/)*
