# 🧬 07. GNN — Graph Neural Networks

> ## 📑 Mục Lục
>
> - [Câu Chuyện Mở Đầu](#câu-chuyện-mở-đầu)
> - [Tại Sao GNN Quan Trọng?](#tại-sao-gnn-quan-trọng)
> - [Tổng Quan](#tổng-quan)
> - [Nội Dung](#nội-dung)
> - [1. GNN Là Gì? Intuition](#1-gnn-là-gì-intuition)
> - [2. GCN — Graph Convolutional Network](#2-gcn--graph-convolutional-network)
> - [3. GraphSAGE & GAT](#3-graphsage--gat)
> - [4. Link Prediction & Node Classification](#4-link-prediction--node-classification)
> - [5. GNN Cho Knowledge Graph Completion](#5-gnn-cho-knowledge-graph-completion)
> - [6. Triển Khai Với PyG](#6-triển-khai-với-pyg)
> - [7. Labs Thực Hành](#7-labs-thực-hành)
> - [Tài Liệu Tham Khảo](#tài-liệu-tham-khảo)

---

### Câu Chuyện Mở Đầu

Bạn có Knowledge Graph với 10,000 người và projects. Bạn muốn:

1. **Dự đoán**: Alice sẽ làm project nào tiếp theo? (link prediction)
2. **Phân loại**: Người này thuộc team nào? (node classification)
3. **Phát hiện**: Có quan hệ nào bị thiếu không? (KG completion)

**Rule-based reasoning** (module 06) làm được với rules thủ công — nhưng không scale khi có hàng trăm loại quan hệ. **GNN** học tự động từ cấu trúc graph: không cần viết rule, chỉ cần examples.

> *"Rules tell the graph what you know. GNNs discover what you don't know you know."*

### Tại Sao GNN Quan Trọng?

> *"GNN là deep learning cho dữ liệu có cấu trúc quan hệ — như CNN là deep learning cho ảnh."*

| # | Nguồn | Phát Hiện |
|---|-------|-----------|
| 1 | **OGB Benchmark (2024)** | GNN tăng **15-25% accuracy** trên node classification vs MLP chỉ dùng node features |
| 2 | **Knowledge Graph Completion (FB15k-237)** | R-GCN + scoring function đạt **MRR 0.35** vs TransE 0.29 |
| 3 | **Anthropic (2025)** | GNN-based link prediction gợi ý **missing relations** với precision 72% trên enterprise KG |

---

## Tổng Quan

```
Knowledge Graph
    │
    ├──► Node Features (text embeddings, properties)
    │         │
    │         ▼
    │   ┌─────────────────┐
    │   │   GNN Layers    │  ← Message Passing: aggregate neighbors
    │   │  GCN / GraphSAGE│     Update: combine self + neighbors
    │   │  GAT / R-GCN    │     Readout: graph-level embedding (nếu cần)
    │   └────────┬────────┘
    │            │
    │            ▼
    ├──► Node Embeddings ──► Node Classification ("Alice thuộc team nào?")
    │                       Link Prediction ("Alice sẽ WORKS_ON gì?")
    │                       Graph Classification ("Graph này là loại nào?")
    │
    └──► KG Completion ──► Dự đoán missing triples
```

---

## Nội Dung

| # | Chủ đề | Mô tả |
|---|--------|-------|
| 1 | [GNN Intuition](#1-gnn-là-gì-intuition) | Message passing, aggregation, update |
| 2 | [GCN](#2-gcn--graph-convolutional-network) | Spectral GCN, code PyTorch |
| 3 | [GraphSAGE & GAT](#3-graphsage--gat) | Inductive, attention |
| 4 | [Link Prediction](#4-link-prediction--node-classification) | Dự đoán quan hệ mới |
| 5 | [KG Completion](#5-gnn-cho-knowledge-graph-completion) | R-GCN, CompGCN |
| 6 | [Giới Hạn & Hướng Vượt Qua](#6-giới-hạn-gnn--hướng-vượt-qua) | Over-smoothing, Expressivity, Graph Transformers |
| 7 | [Heterogeneous & Temporal](#7-heterogeneous--temporal-gnn) | RGCN/HAN/HGT, TGN cho graph động |
| 8 | [PyG](#8-triển-khai-với-pyg) | Training pipeline |

---

## 1. GNN Là Gì? Intuition

> **📌 Khái Niệm Cơ Bản:**
> **GNN (Graph Neural Network)** = mạng neural nơ-ron hoạt động **trên cấu trúc graph**. Khác MLP (chỉ đọc features của từng node riêng lẻ), GNN còn đọc **mối quan hệ giữa các nodes**.
>
> **Giống như CNN dành cho ảnh** (CNN hiểu pixel nào nằm cạnh nhau), **GNN dành cho graph** (GNN hiểu node nào nối với node nào).
>
> **Analogies:**
> - **MLP = Học sinh học thuộc bài**: Biết từng dòng lý thuyết (node features) nhưng không hiểu tài liệu nối nhau thế nào.
> - **GNN = Muốn hiểu bài, hỏi bạn cùng lớp**: Embedding của bạn = (kiến thức của bạn) + (kiến thức bạn bè). Lớp càng sâu → hỏi càng nhiều bạn bè gián tiếp.

### 1.1 Message Passing Framework

> **📌 Hiểu trước khi đọc công thức:**
> **Message Passing (truyền tin nhắn)** = mỗi node tính embedding mới bằng cách:
> 1. **MESSAGE**: Mỗi neighbor "gửi tin nhắn" cho node (embedding + quan hệ giữa 2 node)
> 2. **AGGREGATE**: Node "gộp" tất cả tin nhắn lại (lấy trung bình / tổng / max)
> 3. **UPDATE**: Node "kết hợp" tin nhắn đã gộp với chính nó → embedding mới
>
> Sau **K layers** (K vòng), embedding của node chứa thông tin của nodes **cách K hops**.

```
Ví dụ minh họa — "Alice cần hiểu team của mình":
  Layer 1: Alice nhận tin từ Bob + Carol (bạn thân)
    → Alice biết: Bob làm Phoenix, Carol làm Atlas
  Layer 2: Alice nhận tin từ bạn của Bob (Dave) + bạn của Carol
    → Alice biết: Dave làm AI Research
  Layer 3: Alice biết cả "team của Dave"...

→ Sau K layers, Alice biết thông tin cách K bước trong graph
```

```
Layer k cho node v:

  1. MESSAGE:  m_{vu}^k = MSG(h_v^{k-1}, h_u^{k-1}, e_{vu})  cho mỗi neighbor u
     → Mỗi neighbor u viết 1 "tin nhắn" gửi cho v
     → Tin nhắn chứa: embedding của v, embedding của u, quan hệ e_uv

  2. AGGREGATE: a_v^k = AGG({m_{vu}^k : u ∈ N(v)})            gộp messages
     → v gộp tất cả tin nhắn lại (thường dùng MEAN = trung bình)

  3. UPDATE:   h_v^k = UPDATE(h_v^{k-1}, a_v^k)               cập nhật embedding
     → v kết hợp bản thân cũ + tin nhắn đã gộp → embedding mới hoàn chỉnh hơn

  h_v^0 = initial features (text embedding, one-hot, etc.)
  h_v^K = final embedding sau K layers (chứa thông tin K hops)

Ví dụ 1 layer cho Alice:

  Alice(h_A) ◄── Bob(h_B) + Carol(h_C)     (neighbors)

  a_Alice = MEAN(h_Bob, h_Carol)           (aggregate)
  h_Alice' = ReLU(W · CONCAT(h_Alice, a_Alice))  (update)
```

### 1.2 Tại Sao GNN Mạnh Hơn MLP?

```
MLP: chỉ dùng features của node đó
  h_Alice' = MLP(h_Alice)  ← không biết gì về neighbors

GNN: dùng cả graph structure
  h_Alice' = GNN(h_Alice, h_Bob, h_Carol, h_Phoenix)
  → Alice embedding chứa thông tin về team và projects của Alice
  → 2 người có cùng team → embeddings gần nhau (dù features ban đầu khác)

Ví dụ: Alice và Carol chưa từng gặp nhau (không có edge trực tiếp),
       nhưng cả 2 cùng WORKS_ON Phoenix
       → GNN: embeddings của Alice & Carol gần nhau (cùng một nhóm)
       → MLP: embeddings khác nhau (vì features ban đầu khác) — không biết họ liên quan
```

---

## 2. GCN — Graph Convolutional Network

### 2.1 Công Thức GCN (Kipf & Welling, 2017)

> **📌 Hiểu trước khi đọc công thức:**
> **GCN = Node lấy *trung bình có trọng số* của neighbors + chính nó, rồi qua một lớp fully-connected + ReLU.**
> *Trung bình có trọng số* = mỗi node được đóng góp theo tỷ lệ nghịch với số lượng neighbors của nó (để node kết nối nhiều không "át" node ít kết nối).
>
> **Analogies:**
> - **GCN = Nhóm thảo luận**: Mỗi người = node. Mỗi layer = 1 buổi họp nhóm: mọi người chia sẻ ý kiến (message), rồi ai cũng tổng hợp thành ý kiến mới (update). Nghe nhiều bạn bè → hiểu biết rộng hơn.
> - **Activation (ReLU) = Lọc nhiễu**: Chỉ giữ lại tín hiệu tích cực, bỏ tín hiệu tiêu cực (âm) — giúp model học được pattern phi tuyến.

```
H^{(l+1)} = σ( D^{-1/2} Â D^{-1/2} H^{(l)} W^{(l)} )

  Â = A + I          (adjacency + self-loop — thêm "chính tôi" vào danh sách bạn bè)
  D = degree matrix  (chuẩn hóa — chia cho số lượng neighbors để cân bằng)
  H^{(l)} = (N, D_l) node embeddings layer l
  W^{(l)} = (D_l, D_{l+1}) learnable weights (hệ số học được — bộ lọc của layer)
  σ = ReLU (bỏ giá trị âm)

Đọc thành câu:
  "Embedding mới của mọi nodes = (chuẩn hóa) × (trung bình của chính tôi + bạn bè tôi) × (bộ lọc đã học) × (bỏ giá trị âm)"
```

**Cảnh báo cho người mới:** Đừng hiểu lầm GCN là "tự động học quan hệ". GCN chỉ **trung bình hóa** neighbors (uniform), không phân biệt neighbor nào quan trọng. Nếu bạn cần phân biệt tầm quan trọng → dùng GAT (Section 3).

<details>
<summary>Python Code — GCN Layer Từ Scratch (Click để xem)</summary>

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class GCNLayer(nn.Module):
    def __init__(self, in_dim: int, out_dim: int):
        super().__init__()
        self.linear = nn.Linear(in_dim, out_dim)
    
    def forward(self, x: torch.Tensor, adj: torch.Tensor) -> torch.Tensor:
        """
        x: (N, in_dim) — node features
        adj: (N, N) — adjacency matrix (đã chuẩn hóa)
        """
        # Aggregate: adj @ x → mỗi node lấy trung bình neighbors
        agg = adj @ x  # (N, in_dim)
        # Transform + activation
        out = self.linear(agg)  # (N, out_dim)
        return F.relu(out)

def normalize_adjacency(adj: torch.Tensor) -> torch.Tensor:
    """Chuẩn hóa: D^{-1/2} (A + I) D^{-1/2}"""
    n = adj.shape[0]
    adj_hat = adj + torch.eye(n)  # thêm self-loop
    degree = adj_hat.sum(dim=1)
    d_inv_sqrt = torch.diag(torch.pow(degree, -0.5))
    d_inv_sqrt[torch.isinf(d_inv_sqrt)] = 0
    return d_inv_sqrt @ adj_hat @ d_inv_sqrt

# Usage
N, in_dim, out_dim = 4, 8, 16
x = torch.randn(N, in_dim)
adj = torch.tensor([[0,1,1,0],[1,0,1,0],[1,1,0,1],[0,0,1,0]], dtype=torch.float32)
adj_norm = normalize_adjacency(adj)

gcn = GCNLayer(in_dim, out_dim)
h = gcn(x, adj_norm)
print(f"GCN output: {h.shape}")  # (4, 16)
```

</details>

### 2.2 GCN 2-Layer Cho Node Classification

<details>
<summary>Python Code — GCN 2-Layer (Click để xem)</summary>

```python
class GCN(nn.Module):
    def __init__(self, in_dim: int, hidden_dim: int, out_dim: int, dropout: float = 0.5):
        super().__init__()
        self.gc1 = GCNLayer(in_dim, hidden_dim)
        self.gc2 = GCNLayer(hidden_dim, out_dim)
        self.dropout = dropout
    
    def forward(self, x, adj):
        x = self.gc1(x, adj)
        x = F.dropout(x, p=self.dropout, training=self.training)
        x = self.gc2(x, adj)
        return F.log_softmax(x, dim=1)  # (N, num_classes)

# Training
model = GCN(in_dim=8, hidden_dim=16, out_dim=3)  # 3 classes
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

# Labels: chỉ 1 vài nodes có label (semi-supervised)
labels = torch.tensor([0, 1, -1, -1])  # -1 = unlabeled
train_mask = labels != -1

for epoch in range(200):
    model.train()
    out = model(x, adj_norm)
    loss = F.nll_loss(out[train_mask], labels[train_mask])
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    if epoch % 50 == 0:
        print(f"Epoch {epoch}: loss={loss.item():.4f}")

# Predict unlabeled
model.eval()
pred = model(x, adj_norm).argmax(dim=1)
print(f"Predictions: {pred}")
```

</details>

---

## 3. GraphSAGE & GAT

> **📌 Khái Niệm Cơ Bản:**
> - **GCN** — cần **toàn bộ adjacency matrix** trước (transductive), không mở rộng được khi có node mới
> - **GraphSAGE** — học **hàm gộp (aggregator)** tái sử dụng được → **inductive**, node mới embed được ngay
> - **GAT** — thêm **attention**: mỗi neighbor quan trọng khác nhau
>
> **Analogies:**
> - **GCN = Học thuộc khu phố**: Biết rõ từng ngõ ngách của khu đó. Khu phố mới → học lại từ đầu.
> - **GraphSAGE = Học cách lắng nghe**: Hỏi bạn bè rồi tổng hợp → áp dụng ở bất kỳ đâu, có bạn mới thì hỏi bạn mới.
> - **GAT = Chọn bạn chơi mà chơi**: Không phải bạn nào cũng có trọng lượng như nhau — thầy cô quan trọng hơn bạn lướt qua.

### 3.1 GraphSAGE — Inductive

GraphSAGE khác GCN ở chỗ: **học aggregator function**, không học trên adjacency cố định → có thể embed node mới.

> **Giải thích dễ hiểu:** GCN tính trung bình neighbors NGAY TẠI training (phụ thuộc adjacency cố định). GraphSAGE học một "công thức gộp bạn bè" (aggregator) riêng, nên bất kỳ node mới nào cũng chỉ cần chạy công thức đó với bạn bè của nó.

```
GraphSAGE aggregators (3 cách gộp bạn bè):
  - Mean:  a_v = mean({h_u : u ∈ N(v)})
           → trung bình cộng (giống GCN)
  - LSTM:  a_v = LSTM(random_permutation(N(v)))  — có thứ tự!
           → học được "thứ tự" quan trọng (không hoàn toàn thứ tự-độc lập)
  - Pooling: a_v = max({MLP(h_u) : u ∈ N(v)})
           → mỗi bạn học đưa ra 1 phiếu, giữ phiếu mạnh nhất theo từng chiều

  h_v^k = σ( W^k · CONCAT(h_v^{k-1}, a_v^k) )
  → Ghép "tôi cũ" + "bạn bè tôi" lại, biến hóa bằng bộ lọc học được
```

### 3.2 GAT — Attention

GAT học **attention weight** cho từng neighbor — không phải ai cũng quan trọng như nhau.

> **Giải thích dễ hiểu:** Thay vì "trung bình cộng mọi bạn bè", GAT học: "ai là bạn quan trọng của tôi?" → cho trọng số cao. Cách tính điểm quan trọng: **so sánh vector của tôi với vector bạn bè** (concatenate rồi qua 1 hàm học được + activation).

```
Bước 1 — Tính điểm quan trọng cho từng neighbor:
  score(v,u) = LeakyReLU( a^T [W h_v || W h_u] )
  → "Tôi (W h_v) và bạn (W h_u) giống nhau bao nhiêu?"

Bước 2 — Chuẩn hóa thành tỷ trọng (tổng = 1):
  α_{vu} = softmax(score(v,u))  
  → "Bạn đóng góp bao nhiêu phần trăm cho tôi?"

Bước 3 — Gộp có trọng số:
  h_v' = σ( Σ_{u∈N(v)} α_{vu} · W h_u )
  → "Bạn quan trọng → đóng góp nhiều; bạn kém quan trọng → đóng góp ít"

Multi-head (nhiều "góc nhìn"):
  h_v' = CONCAT(head_1, ..., head_K)  hoặc  MEAN(heads)
  → Giống như hỏi K chuyên gia riêng lẻ rồi gộp — giảm variance, ổn định hơn
```

<details>
<summary>Python Code — GAT Với PyG (Click để xem)</summary>

```python
# pip install torch torch-geometric

import torch
from torch_geometric.nn import GATConv, SAGEConv
from torch_geometric.data import Data

# Chuẩn bị data
edge_index = torch.tensor([[0,1,1,2,2,3,0,2],
                           [1,0,2,1,3,2,2,0]], dtype=torch.long)
x = torch.randn(4, 8)  # 4 nodes, 8 features
y = torch.tensor([0, 1, 0, 1])  # labels

data = Data(x=x, edge_index=edge_index, y=y)

# GraphSAGE model
class GraphSAGEModel(torch.nn.Module):
    def __init__(self, in_c, hid_c, out_c):
        super().__init__()
        self.conv1 = SAGEConv(in_c, hid_c)
        self.conv2 = SAGEConv(hid_c, out_c)
    def forward(self, x, edge_index):
        x = self.conv1(x, edge_index).relu()
        x = self.conv2(x, edge_index)
        return x

# GAT model
class GATModel(torch.nn.Module):
    def __init__(self, in_c, hid_c, out_c, heads=4):
        super().__init__()
        self.conv1 = GATConv(in_c, hid_c, heads=heads, dropout=0.6)
        # GATConv với heads: output = hid_c * heads
        self.conv2 = GATConv(hid_c * heads, out_c, heads=1, concat=False, dropout=0.6)
    def forward(self, x, edge_index):
        x = self.conv1(x, edge_index).relu()
        x = F.dropout(x, p=0.6, training=self.training)
        x = self.conv2(x, edge_index)
        return x

# Train
for name, ModelClass in [("GraphSAGE", GraphSAGEModel), ("GAT", GATModel)]:
    model = ModelClass(8, 16, 2)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
    for epoch in range(100):
        model.train()
        out = model(data.x, data.edge_index)
        loss = F.cross_entropy(out, data.y)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    print(f"{name} final loss: {loss.item():.4f}")
```

</details>

### 3.3 So Sánh

```
┌─────────────────┬──────────────┬──────────────┬──────────────┐
│                 │ GCN          │ GraphSAGE    │ GAT          │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Inductive?      │ ❌           │ ✅           │ ✅           │
│ Attention?      │ ❌ (uniform) │ ❌           │ ✅           │
│ Scalability     │ O(N²) dense  │ O(E) + sample│ O(E × heads) │
│ Best for        │ Small graphs │ Large, need  │ Heterogeneous│
│                 │ Semi-superv. │ inductive    │ Ranked neighbors│
└─────────────────┴──────────────┴──────────────┴──────────────┘
```

---

## 4. Link Prediction & Node Classification

### 4.1 Link Prediction — "Alice sẽ WORKS_ON gì?"

<details>
<summary>Python Code — Link Prediction (Click để xem)</summary>

```python
import torch
import torch.nn.functional as F
from torch_geometric.nn import GCNConv
from torch_geometric.utils import negative_sampling

class LinkPredictor(torch.nn.Module):
    def __init__(self, in_dim, hidden_dim, out_dim):
        super().__init__()
        self.conv1 = GCNConv(in_dim, hidden_dim)
        self.conv2 = GCNConv(hidden_dim, out_dim)
    
    def encode(self, x, edge_index):
        x = self.conv1(x, edge_index).relu()
        x = self.conv2(x, edge_index)
        return x  # (N, out_dim) embeddings
    
    def decode(self, z, edge_label_index):
        """Score edges bằng dot product."""
        src = z[edge_label_index[0]]  # (E, out_dim)
        dst = z[edge_label_index[1]]
        return (src * dst).sum(dim=-1)  # (E,) scores
    
    def forward(self, x, edge_index, edge_label_index):
        z = self.encode(x, edge_index)
        return self.decode(z, edge_label_index)

# Data
edge_index = torch.tensor([[0,1,1,2,2,3],[1,0,2,1,3,2]], dtype=torch.long)
x = torch.randn(4, 8)
# Positive edges (tồn tại) + negative sampling
pos_edges = edge_index
neg_edges = negative_sampling(edge_index, num_nodes=4, num_neg_samples=4)

model = LinkPredictor(8, 16, 8)
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

for epoch in range(200):
    model.train()
    # Positive scores
    pos_score = model(x, edge_index, pos_edges)
    neg_score = model(x, edge_index, neg_edges)
    
    # BCE loss: pos → 1, neg → 0
    pos_loss = F.binary_cross_entropy_with_logits(pos_score, torch.ones_like(pos_score))
    neg_loss = F.binary_cross_entropy_with_logits(neg_score, torch.zeros_like(neg_score))
    loss = pos_loss + neg_loss
    
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    if epoch % 50 == 0:
        print(f"Epoch {epoch}: loss={loss.item():.4f}")

# Predict: Alice(0) sẽ connect với ai?
model.eval()
z = model.encode(x, edge_index)
for target in range(4):
    if target == 0:
        continue
    score = model.decode(z, torch.tensor([[0],[target]]))
    prob = torch.sigmoid(score).item()
    print(f"  Alice -> node_{target}: prob={prob:.3f}")
```

</details>

### 4.2 Node Classification — "Người này thuộc team nào?"

```python
# Đã cover ở §2.2 — GCN 2-layer với cross-entropy loss
# Thêm: class imbalance handling

# Nếu team A có 100 người, team B có 10 người → weighted loss
class_weights = torch.tensor([1.0, 10.0])  # weight cho minority class
loss = F.cross_entropy(out[train_mask], labels[train_mask], weight=class_weights)
```

---

## 5. GNN Cho Knowledge Graph Completion

### 5.1 R-GCN — Relational GCN

Cho heterogeneous KG với nhiều loại quan hệ, R-GCN có **weights riêng cho từng relation**:

```
h_v^{(l+1)} = σ( Σ_{r∈R} Σ_{u∈N_r(v)} (1/c_{v,r}) W_r^{(l)} h_u^{(l)} + W_0^{(l)} h_v^{(l)} )

  R = tập relations (MANAGES, WORKS_ON, ...)
  W_r = weights riêng cho relation r
  c_{v,r} = normalization (số neighbors qua relation r)
  W_0 = self-loop weights
```

```python
from torch_geometric.nn import RGCNConv

class RGCN(torch.nn.Module):
    def __init__(self, in_dim, hidden_dim, out_dim, num_relations):
        super().__init__()
        self.conv1 = RGCNConv(in_dim, hidden_dim, num_relations)
        self.conv2 = RGCNConv(hidden_dim, out_dim, num_relations)
    
    def forward(self, x, edge_index, edge_type):
        x = self.conv1(x, edge_index, edge_type).relu()
        x = self.conv2(x, edge_index, edge_type)
        return x

# edge_type: (E,) — loại relation cho mỗi edge
edge_index = torch.tensor([[0,1,2,0],[1,2,3,2]], dtype=torch.long)
edge_type = torch.tensor([0, 1, 0, 1])  # 0=MANAGES, 1=WORKS_ON
x = torch.randn(4, 8)

model = RGCN(8, 16, 8, num_relations=2)
out = model(x, edge_index, edge_type)
print(f"R-GCN output: {out.shape}")  # (4, 8)
```

### 5.2 Scoring Functions Cho KG Completion

Sau khi có embeddings từ R-GCN, dùng scoring function để predict missing triples:

```
┌──────────────┬──────────────────────────────────┬──────────────────────┐
│ Method       │ Score(h, r, t)                   │ Best For             │
├──────────────┼──────────────────────────────────┼──────────────────────┤
│ TransE       │ -||h + r - t||                   │ Simple, fast         │
│ DistMult     │ <h, r, t> (trilinear dot)        │ Symmetric relations  │
│ ComplEx      │ Re(<h, r, conj(t)>) (complex)    │ Asymmetric + symmetric│
│ RotatE       │ -||h ◦ r - t|| (rotation)        │ Composition, inversion│
└──────────────┴──────────────────────────────────┴──────────────────────┘
```

---

## 6. Giới Hạn GNN & Hướng Vượt Qua

> **📌 Khái Niệm Cơ Bản:**
> GNN message-passing mạnh, nhưng **đào sâu quá lại hỏng**. Đây là 2 "bệnh" được nhắc nhiều nhất trong nghiên cứu, và bạn cần biết để không chọn GNN sai bài toán.

### 6.1 Over-Smoothing (Khi Node Trở Nên... Giống Như Nhao)

> **Over-smoothing** = sau nhiều lớp GCN, **features của mọi nodes dồn về giống nhau dần** — node A và node Z (chẳng liên quan) nhận cùng vector, mô hình không phân biệt được ai với ai. Phân loại node hỏng nặng.
>
> **Analogies:** Giống trò chơi **"điện thoại hỏng"**: qua nhiều vòng thì message càng ngày càng mất gốc — thông tin từ xa bị "pha loãng".

### 6.2 Over-Squashing + Expressivity (WL Test)

> **Over-squashing** = **nút thắt cổ chai** trong graph. Node ở vùng nhiều kết nối "chặn" đường truyền thông tin từ vùng xa → nodes ở xa nhau gần như **không liên lạc được** dù GNN có lên 10 lớp. Đường đi dài bị nén mất chi tiết.
>
> **Expressivity (sức biểu diễn)** = GNN message-passing chuẩn **không mạnh hơn WL test** (thuật toán kiểm tra đẳng cấu của Weisfeiler-Lehman năm 1968). Nghĩa là có những graph khác nhau mà GNN chuẩn **không phân biệt được**. Giới hạn này rất thực tế khi so graph/molecules.
>
> **Remedies (cách chữa) - chọn 1 trong các cách dưới:**
> - **Residual connections** (bỏ qua 1 lớp) — như GCN có `residual`
> - **Normalization** chuẩn hóa feature sau mỗi layer
> - **Rewiring / graph surgery** — nối thêm cạnh ngắn giữa nodes xa (gọi là "graph rewiring")
> - **Chỉ dùng 2-3 lớp** thay vì đào sâu — thực tế GraphSAGE 2 lớp hiệu quả hơn 10 lớp

### 6.3 Graph Transformers — Vượt Qua Over-Smoothing

> **Graph Transformers (GraphGPS, GT)** dùng **self-attention trên toàn graph**: node có thể "nhìn" mọi node khác trực tiếp với đúng 1 lượt tính — **không phải qua chuỗi hops** nên không bị over-smoothing/over-squashing. Vượt trội trên dữ liệu cần **đường đi dài quan trọng**, graph có cấu trúc cục bộ phức tạp.
>
> **Giá phải trả:** attention matrix O(N²) memory cho N nodes → khó scale graph hàng triệu nodes. Giải pháp lai (GraphGPS): message-passing giữ local context + chỉ 1 block attention global.

---

## 7. Heterogeneous & Temporal GNN

> **📌 Khái Niệm Cơ Bản:**
> **Heterogeneous graph** = graph có **nhiều loại node và nhiều loại edge** — như KG thật đều là heterogeneous (`Person`-`WORKS_ON`->`Project`, `Person`-`REPORTS_TO`->`Person`, `Project`-`HAS_BUDGET`->`Number`). GNN chuẩn (GCN/GraphSAGE) giả định **mọi node mọi edge cùng 1 loại** — nếu nhét thẳng KG vào sẽ đánh mất ý nghĩa từng relation.
>
> **3 họ mô hình tiêu biểu cho heterogeneous:**
> - **R-GCN (Relational GCN)**: mỗi relation type có 1 ma trận W riêng — như "mỗi loại quan hệ là 1 'lăng kính' nhìn khác nhau" → message của từng relation đi qua lăng kính của riêng nó (đã nói ở section 5).
> - **HAN (Heterogeneous Attention Network)**: phân cấp **meta-path** — tổng hợp theo từng "con đường loại" (`P--WORKS_ON--Project--HAS_BUDGET--Budget`) rồi attention giữa các meta-path.
> - **HGT (Heterogeneous Graph Transformer)**: áp dụng kỹ thuật Transformer phân-tách-lớp theo loại node/edge — chú ý độ quan trọng tương đối giữa các loại quan hệ, SOTA cho KG hiện đại.
>
> **Khi nào dùng:** KG thật của bạn (Module 02) luôn heterogeneous → nếu cần học node embeddings tận dụng relation semantics, đừng flatten về homogeneous.
>
> **Temporal GNN (TGN)** = extension dành cho **graph biến đổi theo thời gian** (log sự kiện, giao dịch). Thay vì 1 snapshot tĩnh, TGN xử lý **stream sự kiện** theo từng timestamp — mỗi sự kiện "gõ cửa" node, node cập nhật memory. Kết hợp với temporal embeddings (Module 04) thành dòng hoàn chỉnh dự đoán theo thời gian.

```python
# Pseudocode — HGT: attention theo từng cặp (node_type, edge_type)
def hgt_message(head, rel, tail):
    # Project đã có node type khác Person → dùng ma trận riêng
    W_head = weight_matrix[head.node_type]
    W_edge = weight_matrix[rel.edge_type]
    W_tail = weight_matrix[tail.node_type]
    attn = attention(W_head @ head.h, W_edge @ rel.h, W_tail @ tail.h)
    return attn * (W_head @ head.h)
```

---

## 8. Triển Khai Với PyG

<details>
<summary>Python Code — Complete Training Pipeline (Click để xem)</summary>

```python
import torch
import torch.nn.functional as F
from torch_geometric.nn import GCNConv
from torch_geometric.data import Data
from torch_geometric.utils import train_test_split_edges

# 1. Chuẩn bị data
edge_index = torch.tensor([
    [0,1,1,2,2,3,3,0,0,2],
    [1,0,2,1,3,2,0,3,2,0]
], dtype=torch.long)
x = torch.randn(4, 16)
y = torch.tensor([0, 0, 1, 1])  # 2 classes

data = Data(x=x, edge_index=edge_index, y=y, num_nodes=4)
# Split edges cho link prediction
# data = train_test_split_edges(data)  # cho large graphs

# 2. Model
class GNN(torch.nn.Module):
    def __init__(self, in_c, hid_c, out_c):
        super().__init__()
        self.conv1 = GCNConv(in_c, hid_c)
        self.conv2 = GCNConv(hid_c, out_c)
        self.classifier = torch.nn.Linear(out_c, 2)
    
    def forward(self, x, edge_index, task="classify"):
        x = self.conv1(x, edge_index).relu()
        x = F.dropout(x, p=0.5, training=self.training)
        x = self.conv2(x, edge_index)
        if task == "classify":
            return self.classifier(x)
        return x  # embeddings cho link prediction

model = GNN(16, 32, 16)
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

# 3. Training loop
for epoch in range(200):
    model.train()
    out = model(data.x, data.edge_index, task="classify")
    loss = F.cross_entropy(out, data.y)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    if epoch % 50 == 0:
        pred = out.argmax(dim=1)
        acc = (pred == data.y).float().mean().item()
        print(f"Epoch {epoch}: loss={loss.item():.4f}, acc={acc:.2f}")

# 4. Evaluation
model.eval()
with torch.no_grad():
    out = model(data.x, data.edge_index, task="classify")
    pred = out.argmax(dim=1)
    print(f"Final predictions: {pred.tolist()}, true: {y.tolist()}")
```

</details>

---

## 9. Labs Thực Hành

### Lab 1: Node Classification Trên Karate Club

1. Load `nx.karate_club_graph()`, tạo features (degree, one-hot, hoặc random)
2. Train GCN 2-layer, đo accuracy với 4 labeled nodes (semi-supervised)
3. So sánh với MLP (không dùng graph) — GNN phải thắng

### Lab 2: Link Prediction

1. Mask 20% edges của graph 100 nodes
2. Train link predictor (§4.1), đo AUC trên masked edges
3. Thử negative sampling ratios khác nhau (1:1 vs 1:5)

### Lab 3: KG Completion Mini

1. Tạo KG nhỏ: 20 entities, 3 relations, 50 triples
2. Train R-GCN + DistMult scoring
3. Hỏi: `(Alice, WORKS_ON, ?)` → rank tất cả entities, kiểm tra rank của đáp án đúng

---

## Tài Liệu Tham Khảo

- Kipf & Welling — *Semi-Supervised Classification with Graph Convolutional Networks* (ICLR 2017)
- Hamilton et al. — *Inductive Representation Learning on Large Graphs (GraphSAGE)* (NeurIPS 2017)
- Veličković et al. — *Graph Attention Networks* (ICLR 2018)
- Schlichtkrull et al. — *Modeling Relational Data with Graph Convolutional Networks (R-GCN)* (ESWC 2018)
- *Graph Transformers: A Survey* (arXiv:2502.16533) — over-smoothing/over-squashing, GraphGPS
- *Over-smoothing & Over-squashing in GNNs* (arXiv:2502.10818) — remedies: residual, rewiring
- Hamilton — *Graph Representation Learning* (2020) — WL-test expressivity chương 9
- PyG Docs — *Creating Your Own GNN* (https://pytorch-geometric.readthedocs.io/)
- OGB — *Open Graph Benchmark* (https://ogb.stanford.edu/)

---

*Tiếp theo: [08 — Graph Workflow](../08-graph-workflow/)*
