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

### Tại Sao Graph Embeddings Quan Trọng?

> *"Graph tells you WHO is connected. Embeddings tell you WHO IS SIMILAR without being directly connected."*

| # | Nguồn | Phát Hiện |
|---|-------|-----------|
| 1 | **Node2Vec Paper (2016)** | Graph embeddings tăng **22% accuracy** trên link prediction so với chỉ dùng node features |
| 2 | **Microsoft GraphRAG (2024)** | Kết hợp text embeddings + graph embeddings tăng **18% retrieval precision** |
| 3 | **OGB Benchmark (2024)** | GraphSAGE embeddings + ANN search nhanh hơn traversal thuần **50×** cho k-NN queries trên 1M nodes |

---

## Tổng Quan

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
> **Tại sao cần?** Vì vector vừa **so sánh được bằng cosine similarity**, vừa **lưu vào vector DB** để search nhanh bằng ANN. Graph structure → vector space → dùng được cho RAG, clustering, classification.

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

```
┌──────────────────────┬──────────────────────┬───────────────────────────────┐
│ Loại                 │ Cần Training?        │ Best For                      │
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
- **DeepWalk = Google Maps nhưng bị lạc đường**: Đi ngẫu nhiên quanh vùng,記錄 những nơi đi qua → hiểu cấu trúc vùng đất.

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

```python
# p và q hoạt động như thế nào:

p = return parameter (xác suất quay lại node vừa rời đi):
  - p nhỏ (0.5): hay quay lại → khám phá neighborhood chặt
  - p lớn (2.0): ít quay lại → đi xa hơn

q = in-out parameter (xác suất đi ra xa hay quay lại):
  - q nhỏ (0.5): dễ đi xa (DFS-like) → khám phá cấu trúc xa
  - q lớn (2.0): dễ đi gần (BFS-like) → khám phá community.local

# Hiểu đơn giản nhất:
# q < 1 (DFS-like): "Tôi muốn tìm người có CÙNG ROLE" dù ở khác team
# q > 1 (BFS-like): "Tôi muốn tìm người trong CÙNG TEAM"
```

<details>
<summary>Python Code — Node2Vec với NetworkX (Click để xem)</summary>

```python
import networkx as nx
import numpy as np
from gensim.models import Word2Vec
import random

def get_random_walk(graph, start_node: str, walk_length: int = 10) -> list[str]:
    walk = [start_node]
    current = start_node
    for _ in range(walk_length - 1):
        neighbors = list(graph.neighbors(current))
        if not neighbors:
            break
        current = random.choice(neighbors)
        walk.append(current)
    return walk

def deepwalk_embeddings(
    graph: nx.Graph,
    num_walks: int = 10,
    walk_length: int = 20,
    embedding_dim: int = 64,
    window: int = 5,
) -> dict[str, np.ndarray]:
    """Tạo embeddings bằng random walks + Word2Vec."""
    # Tạo corpus: nhiều random walks
    walks = []
    nodes = list(graph.nodes())
    for _ in range(num_walks):
        for node in nodes:
            walks.append(get_random_walk(graph, node, walk_length))
    
    print(f"Generated {len(walks)} walks, avg length {sum(len(w) for w in walks)/len(walks):.1f}")
    
    # Train Word2Vec
    model = Word2Vec(
        walks,
        vector_size=embedding_dim,
        window=window,
        min_count=0,
        sg=1,  # Skip-gram
        workers=4,
        epochs=5,
    )
    
    # Trả về dict node -> vector
    return {node: model.wv[node] for node in graph.nodes() if node in model.wv}

# Usage
G = nx.karate_club_graph()
# Đổi node labels thành strings cho Word2Vec
G_labeled = nx.relabel_nodes(G, {n: f"node_{n}" for n in G.nodes()})
embeddings = deepwalk_embeddings(G_labeled, num_walks=10, walk_length=20, embedding_dim=64)

# Tìm nodes giống nhau
def most_similar(target: str, embeddings: dict, top_k: int = 5) -> list:
    target_vec = embeddings[target]
    scores = []
    for node, vec in embeddings.items():
        if node == target:
            continue
        sim = float(np.dot(target_vec, vec) / (np.linalg.norm(target_vec) * np.linalg.norm(vec)))
        scores.append((node, sim))
    scores.sort(key=lambda x: x[1], reverse=True)
    return scores[:top_k]

print(most_similar("node_0", embeddings, top_k=5))
```

</details>

### 2.3 Khi Nào Dùng Node2Vec?

| Tình huống | Dùng? | Lý do |
|-----------|-------|-------|
| Graph nhỏ-medium (<100K nodes) | ✅ | Nhanh, không cần GPU, unsupervised |
| Cần inductive (thêm node mới) | ❌ | Phải retrain toàn bộ — dùng GraphSAGE thay thế |
| Cần edge features / node features | ❌ | Node2Vec chỉ dùng cấu trúc — dùng GNN |
| Clustering / community detection | ✅ | Embeddings phản ánh community structure tốt |

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

```python
# Pseudocode: GraphSAGE forward
def graphsage_layer(node_features, adjacency, weights, aggregator="mean"):
    """
    node_features: (N, D) — features của N nodes
    adjacency: (N, N) — adjacency matrix
    """
    # Aggregate neighbors
    if aggregator == "mean":
        neighbor_agg = adjacency @ node_features / adjacency.sum(axis=1, keepdims=True)
    
    # Concat self + neighbors
    combined = np.concatenate([node_features, neighbor_agg], axis=1)
    
    # Transform
    output = np.maximum(0, combined @ weights)  # ReLU
    # Normalize
    output = output / np.linalg.norm(output, axis=1, keepdims=True)
    return output
```

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

```python
# pip install torch torch-geometric

import torch
from torch_geometric.nn import SAGEConv
from torch_geometric.data import Data

class GraphSAGE(torch.nn.Module):
    def __init__(self, in_channels: int, hidden_channels: int, out_channels: int):
        super().__init__()
        self.conv1 = SAGEConv(in_channels, hidden_channels)
        self.conv2 = SAGEConv(hidden_channels, out_channels)
    
    def forward(self, x, edge_index):
        x = self.conv1(x, edge_index)
        x = x.relu()
        x = self.conv2(x, edge_index)
        return x  # (N, out_channels) embeddings

# Tạo graph data
# edge_index: (2, E) — danh sách edges
edge_index = torch.tensor([[0, 1, 1, 2, 2, 3],
                           [1, 0, 2, 1, 3, 2]], dtype=torch.long)
x = torch.randn(4, 16)  # 4 nodes, 16 features mỗi node

model = GraphSAGE(in_channels=16, hidden_channels=32, out_channels=8)
embeddings = model(x, edge_index)
print(f"Embeddings shape: {embeddings.shape}")  # (4, 8)
print(f"Embedding node 0: {embeddings[0]}")
```

</details>

### 3.3 So Sánh

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

> **Ý tưởng:** Thay vì relation = "dịch chuyển", RotatE xem relation = **phép quay** trên mặt phẳng phức. Mỗi relation là 1 góc quay: quay vector `h` một góc = góc của relation → ra gần `t`.

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

```python
import torch
import torch.nn as nn

class TransE(nn.Module):
    def __init__(self, num_entities: int, num_relations: int, dim: int = 100):
        super().__init__()
        self.entity_emb = nn.Embedding(num_entities, dim)
        self.relation_emb = nn.Embedding(num_relations, dim)
        nn.init.xavier_uniform_(self.entity_emb.weight)
        nn.init.xavier_uniform_(self.relation_emb.weight)
    
    def forward(self, h: torch.Tensor, r: torch.Tensor, t: torch.Tensor) -> torch.Tensor:
        """Score triples — thấp = đúng."""
        h_e = self.entity_emb(h)  # (batch, dim)
        r_e = self.relation_emb(r)
        t_e = self.entity_emb(t)
        # L1 distance: ||h + r - t||
        score = torch.norm(h_e + r_e - t_e, p=1, dim=1)
        return score  # (batch,)
    
    def predict_tail(self, h: int, r: int, all_entities: int) -> torch.Tensor:
        """Cho (h, r, ?), rank tất cả entities theo score."""
        h_e = self.entity_emb(torch.tensor([h]))
        r_e = self.relation_emb(torch.tensor([r]))
        all_t = self.entity_emb.weight  # (num_entities, dim)
        scores = torch.norm(h_e + r_e - all_t, p=1, dim=1)
        return scores  # thấp nhất = dự đoán tốt nhất

# Training
model = TransE(num_entities=1000, num_relations=10, dim=100)
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

for epoch in range(100):
    # Positive triples: (h, r, t) đúng
    h_pos = torch.randint(0, 1000, (32,))
    r_pos = torch.randint(0, 10, (32,))
    t_pos = torch.randint(0, 1000, (32,))
    
    # Negative triples: corrupt tail
    t_neg = torch.randint(0, 1000, (32,))
    
    pos_score = model(h_pos, r_pos, t_pos)
    neg_score = model(h_pos, r_pos, t_neg)
    
    # Margin ranking loss: pos_score + margin < neg_score
    margin = 1.0
    loss = torch.relu(pos_score - neg_score + margin).mean()
    
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    
    if epoch % 20 == 0:
        print(f"Epoch {epoch}: loss={loss.item():.4f}")

# Predict: Alice WORKS_ON ?
# alice_id = entity_to_id["Alice"], works_on_id = relation_to_id["WORKS_ON"]
# scores = model.predict_tail(alice_id, works_on_id, num_entities=1000)
# top_k = torch.topk(scores, k=5, largest=False)  # 5 projects có score thấp nhất
```

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
> **Khi nào nên (chưa) dùng:** medium-size graphs, graph có đường đi dài quan trọng, cần SOTA accuracy → chọn GT. Graph hàng triệu nodes → message-passing GNN vẫn dễ scale hơn. Đây là chi tiết tính toán thuộc Module 07 — ở Module này chỉ cần biết **tồn tại họ embedding "thế hệ mới"** này.

---

## 5. Hybrid Search: Vector + Graph

Graph embeddings không thay thế text embeddings — chúng **bổ sung** cho nhau.

### 5.1 Kỹ Thuật Fusion

<details>
<summary>Python Code — Hybrid Search (RRF + Weighted) (Click để xem)</summary>

```python
import numpy as np
from typing import List, Dict

def reciprocal_rank_fusion(
    ranked_lists: List[List[str]],
    k: int = 60,
) -> Dict[str, float]:
    """RRF: gộp nhiều ranked lists thành 1 score."""
    scores: Dict[str, float] = {}
    for ranked_list in ranked_lists:
        for rank, doc_id in enumerate(ranked_list):
            scores[doc_id] = scores.get(doc_id, 0) + 1 / (k + rank + 1)
    return scores

def hybrid_search(
    query_text: str,
    query_vector: List[float],
    text_index,       # Vector DB cho text embeddings
    graph_embeddings: Dict[str, np.ndarray],
    top_k: int = 10,
    alpha: float = 0.6,  # weight cho text search
) -> List[Dict]:
    """
    Hybrid: α * text_score + (1-α) * graph_score
    
    alpha=1.0 → chỉ text search
    alpha=0.0 → chỉ graph search
    alpha=0.6 → cân bằng (khuyến nghị)
    """
    # 1. Text search (semantic)
    text_results = text_index.search(query_vector, top_k=top_k * 2)
    # text_results = [{"id": "doc_1", "score": 0.92}, ...]
    
    # 2. Graph search (structural)
    query_graph_vec = embed(query_text)  # hoặc query entity embedding
    graph_scores = []
    for node_id, node_vec in graph_embeddings.items():
        sim = float(np.dot(query_graph_vec, node_vec) / 
                    (np.linalg.norm(query_graph_vec) * np.linalg.norm(node_vec)))
        graph_scores.append((node_id, sim))
    graph_scores.sort(key=lambda x: x[1], reverse=True)
    graph_ranked = [node_id for node_id, _ in graph_scores[:top_k * 2]]
    
    # 3a. Fusion bằng Weighted Score
    text_score_map = {r["id"]: r["score"] for r in text_results}
    graph_score_map = {node_id: score for node_id, score in graph_scores}
    
    all_ids = set(text_score_map.keys()) | set(graph_score_map.keys())
    hybrid_scores = {}
    for doc_id in all_ids:
        t_score = text_score_map.get(doc_id, 0)
        g_score = graph_score_map.get(doc_id, 0)
        hybrid_scores[doc_id] = alpha * t_score + (1 - alpha) * g_score
    
    ranked = sorted(hybrid_scores.items(), key=lambda x: x[1], reverse=True)
    return [{"id": doc_id, "score": score} for doc_id, score in ranked[:top_k]]

# 3b. Fusion bằng RRF (không cần tune alpha)
def hybrid_search_rrf(text_ranked: List[str], graph_ranked: List[str], top_k: int = 10):
    fused = reciprocal_rank_fusion([text_ranked, graph_ranked])
    ranked = sorted(fused.items(), key=lambda x: x[1], reverse=True)
    return ranked[:top_k]
```

</details>

### 5.2 Khi Nào Dùng Hybrid?

```
Query type                        │ Best α  │ Strategy
──────────────────────────────────┼─────────┼──────────────────────────
Factoid (tìm đoạn văn cụ thể)     │ 0.8     │ Text-heavy
Multi-hop (nối nhiều thực thể)    │ 0.3     │ Graph-heavy
Global summary (tổng hợp)         │ 0.2     │ Graph communities
Hybrid (default)                  │ 0.5-0.6 │ Cân bằng
```

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
3. Đo precision@5 cho từng loại query

---

## Tài Liệu Tham Khảo

- Grover & Leskovec — *Node2Vec: Scalable Feature Learning for Networks* (KDD 2016)
- Hamilton et al. — *Inductive Representation Learning on Large Graphs (GraphSAGE)* (NeurIPS 2017)
- Veličković et al. — *Graph Attention Networks* (ICLR 2018)
- *Temporal Knowledge Graph Completion: A Survey* — TGN, TuckERTNT, tendency-guided (arXiv 2024-2025)
- *Graph Transformers: A Survey* (arXiv:2502.16533) — GraphGPS, GT
- Bordes et al. — *Translating Embeddings for Modeling Multi-relational Data (TransE)* (NeurIPS 2013)
- Sun et al. — *RotatE: Knowledge Graph Embedding by Relational Rotation* (ICLR 2019)

---

*Tiếp theo: [05 — GraphRAG](../05-graph-rag/)*
