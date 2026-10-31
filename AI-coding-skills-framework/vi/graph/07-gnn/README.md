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

Giải thích nhanh 3 từ khóa trong 3 câu hỏi trên:

- **Link prediction** = đoán quan hệ mới. Ví dụ: đoán Alice sẽ WORKS_ON project nào tiếp theo.
- **Node classification** = gắn nhãn cho từng node. Ví dụ: đoán người này thuộc team nào.
- **KG completion** = điền phần thiếu vào Knowledge Graph. Ví dụ: graph thiếu cạnh "Alice WORKS_ON Phoenix" → GNN đoán ra cạnh đó.

> *"Rules tell the graph what you know. GNNs discover what you don't know you know."*

> **Tóm gọn 1 câu:** GNN học trực tiếp từ cấu trúc graph để đoán quan hệ mới, gắn nhãn node và điền dữ liệu thiếu — thay vì phải viết tay từng rule cho từng loại quan hệ.

### Tại Sao GNN Quan Trọng?

> *"GNN là deep learning cho dữ liệu có cấu trúc quan hệ — như CNN là deep learning cho ảnh."*

Cách đọc bảng này: mỗi dòng là một nghiên cứu; cột **Phát Hiện** cho biết GNN tốt hơn phương pháp cũ bao nhiêu. Ví dụ dòng 1: **MLP** = mạng neural thường chỉ đọc thông tin riêng của từng node, không nhìn quan hệ; **MRR** = điểm xếp hạng, đáp án đúng càng lên đầu danh sách thì điểm càng gần 1.0.

| # | Nguồn | Phát Hiện |
|---|-------|-----------|
| 1 | **OGB Benchmark (2024)** | GNN tăng **15-25% accuracy** trên node classification vs MLP chỉ dùng node features |
| 2 | **Knowledge Graph Completion (FB15k-237)** | R-GCN + scoring function đạt **MRR 0.35** vs TransE 0.29 |
| 3 | **Anthropic (2025)** | GNN-based link prediction gợi ý **missing relations** với precision 72% trên enterprise KG |

> **Tóm gọn 1 câu:** Con số nghiên cứu cho thấy GNN đoán chính xác hơn hẳn phương pháp cũ trên cả phân loại node lẫn điền thiếu quan hệ vào graph.

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

Đọc sơ đồ này thế nào: data vào = Knowledge Graph (các node + features); giữa = các lớp GNN "truyền tin nhắn" giữa các node; ra = 3 loại kết quả — gắn nhãn node, đoán quan hệ mới, đoán dữ liệu thiếu (**missing triples** = bộ 3 *chủ ngữ–quan hệ–tân ngữ* còn thiếu, ví dụ `Alice —WORKS_ON→ Phoenix`).

> **Tóm gọn 1 câu:** GNN nhận graph làm đầu vào, cho các node "trò chuyện" qua các lớp, rồi xuất ra embedding dùng cho mọi bài toán đoán quan hệ.

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

Cách đọc bảng này: đây là lộ trình 8 chủ đề nên đọc theo thứ tự. Cột **Mô tả** ghi ý chính của từng phần. Ví dụ dòng 1: *Message passing* = cách các node gửi thông tin cho nhau; *aggregation* = gộp thông tin nhận được; *update* = cập nhật thông tin của chính node.

> **Tóm gọn 1 câu:** Phần nội dung đi từ trực quan (GNN là gì) đến từng dòng model (GCN, GraphSAGE, GAT), rồi đến ứng dụng và code thực tế.

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

> **Tóm gọn 1 câu:** GNN khác MLP ở chỗ nó không chỉ đọc thông tin riêng của từng node, mà còn đọc cả mối quan hệ giữa các node — như hỏi bạn cùng lớp thay vì chỉ học thuộc bài.

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

> **Tóm gọn 1 câu:** Message passing = mỗi node hỏi dần các node lân cận; càng nhiều lớp, node càng biết thông tin từ càng xa (K lớp = biết xa K bước).

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

> **Tóm gọn 1 câu:** GNN mạnh hơn MLP vì embedding của mỗi node chứa cả thông tin từ các node lân cận — hai người cùng làm một project sẽ được nhận diện là "liên quan", dù profile gốc khác nhau.

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

> **Tóm gọn 1 câu:** GCN = lấy trung bình có trọng số của "chính tôi + bạn bè tôi", rồi lọc nhiễu — đơn giản, nhanh, nhưng coi mọi neighbor ngang hàng nhau.

<details>
<summary>Python Code — GCN Layer Từ Scratch (Click để xem)</summary>

> 📄 **Code ví dụ:** [`examples/01-2-1-cong-thuc-gcn-kipf-welling-2017.py`](examples/01-2-1-cong-thuc-gcn-kipf-welling-2017.py)

</details>

### 2.2 GCN 2-Layer Cho Node Classification

<details>
<summary>Python Code — GCN 2-Layer (Click để xem)</summary>

> 📄 **Code ví dụ:** [`examples/02-2-2-gcn-2-layer-cho-node-classification.py`](examples/02-2-2-gcn-2-layer-cho-node-classification.py)

</details>

> **Tóm gọn 1 câu:** Ghép 2 lớp GCN lại là đủ để phân loại node thực tế — mỗi lớp cho node biết thêm thông tin từ xa 1 bước.

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

> **Tóm gọn 1 câu:** Ba dòng model = ba mức "thông minh" dần: GCN học thuộc từng khu phố, GraphSAGE học cách hỏi bất cứ ai, GAT còn biết chọn ai đáng hỏi nhất.

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

> **Tóm gọn 1 câu:** GraphSAGE học một "công thức hỏi bạn bè" dùng được cho mọi node — nên node mới xuất hiện cũng embed được ngay, không cần huấn luyện lại.

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

> **Tóm gọn 1 câu:** GAT chấm điểm từng neighbor xem "ai quan trọng với tôi" rồi gộp theo tỷ trọng — nên node kết nối nhiều không bị bạn bè ít quan trọng "pha loãng".

<details>
<summary>Python Code — GAT Với PyG (Click để xem)</summary>

> 📄 **Code ví dụ:** [`examples/03-3-2-gat-attention.py`](examples/03-3-2-gat-attention.py)

</details>

### 3.3 So Sánh

Cách đọc bảng này: mỗi dòng là một tiêu chí so sánh giữa 3 model; ✅ = có, ❌ = không. Ví dụ dòng "Inductive?": GCN ❌ nghĩa là GCN **không** xử lý được node mới mà không huấn luyện lại; dòng "Scalability" nói chi phí tăng thế nào khi graph lớn (O(N²) = tốn theo bình phương số node — graph càng to càng đắt đỏ).

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

> **Tóm gọn 1 câu:** Graph nhỏ dùng GCN cho rẻ; graph lớn cần node mới → GraphSAGE; cần phân biệt neighbor quan trọng → GAT.

---

## 4. Link Prediction & Node Classification

### 4.1 Link Prediction — "Alice sẽ WORKS_ON gì?"

<details>
<summary>Python Code — Link Prediction (Click để xem)</summary>

> 📄 **Code ví dụ:** [`examples/04-4-1-link-prediction-alice-se-works-on.py`](examples/04-4-1-link-prediction-alice-se-works-on.py)

</details>

> **Tóm gọn 1 câu:** Link prediction = tính "độ hợp cặp" giữa hai node bằng embedding rồi chọn cặp có điểm cao nhất — chính là cách gợi ý quan hệ còn thiếu.

### 4.2 Node Classification — "Người này thuộc team nào?"

> 📄 **Code ví dụ:** [`examples/05-4-2-node-classification-nguoi-nay-thuoc-team.py`](examples/05-4-2-node-classification-nguoi-nay-thuoc-team.py)

> **Tóm gọn 1 câu:** Node classification = lấy embedding cuối cùng của node (đã "hội ý" với cả graph) rồi đưa qua một lớp phân loại để gắn nhãn.

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

Đọc công thức thế nào: khác GCN chỉ có một ma trận trọng số duy nhất, R-GCN (**Relational GCN** = GCN phân loại quan hệ) cho **mỗi loại quan hệ một ma trận riêng**. Ví dụ: cạnh `MANAGES` đi qua "lăng kính" riêng, cạnh `WORKS_ON` đi qua lăng kính khác — nên ý nghĩa từng quan hệ không bị trộn lẫn.

> 📄 **Code ví dụ:** [`examples/06-5-1-r-gcn-relational-gcn.py`](examples/06-5-1-r-gcn-relational-gcn.py)

> **Tóm gọn 1 câu:** R-GCN = GCN nhưng mỗi loại quan hệ có một bộ trọng số riêng — để "MANAGES" và "WORKS_ON" không bị hiểu lẫn thành một thứ.

### 5.2 Scoring Functions Cho KG Completion

Sau khi có embeddings từ R-GCN, dùng scoring function để predict missing triples:

Cách đọc bảng này: mỗi dòng là một công thức chấm điểm (**scoring function** = hàm cho điểm cao khi triple *(chủ ngữ h, quan hệ r, tân ngữ t)* "có khả năng đúng"). Ví dụ dòng TransE: head + relation nên "đi tới" tail — đơn giản, nhanh, nhưng kém với quan hệ đối xứng.

```
┌──────────────┬──────────────────────────────────┬──────────────────────┐
│ Phương pháp  │ Hàm chấm điểm(h, r, t)           │ Phù hợp nhất khi   │
├──────────────┼──────────────────────────────────┼──────────────────────┤
│ TransE       │ -||h + r - t||                   │ Simple, fast         │
│ DistMult     │ <h, r, t> (trilinear dot)        │ Symmetric relations  │
│ ComplEx      │ Re(<h, r, conj(t)>) (complex)    │ Asymmetric + symmetric│
│ RotatE       │ -||h ◦ r - t|| (rotation)        │ Composition, inversion│
└──────────────┴──────────────────────────────────┴──────────────────────┘
```

> **Tóm gọn 1 câu:** Scoring function là "giám khảo chấm điểm cặp (h, r, t)" — chọn loại nào tùy quan hệ của bạn đối xứng hay có thứ tự.

---

## 6. Giới Hạn GNN & Hướng Vượt Qua

> **📌 Khái Niệm Cơ Bản:**
> GNN message-passing mạnh, nhưng **đào sâu quá lại hỏng**. Đây là 2 "bệnh" được nhắc nhiều nhất trong nghiên cứu, và bạn cần biết để không chọn GNN sai bài toán.

### 6.1 Over-Smoothing (Khi Node Trở Nên... Giống Như Nhao)

> **Over-smoothing** = sau nhiều lớp GCN, **features của mọi nodes dồn về giống nhau dần** — node A và node Z (chẳng liên quan) nhận cùng vector, mô hình không phân biệt được ai với ai. Phân loại node hỏng nặng.
>
> **Analogies:** Giống trò chơi **"điện thoại hỏng"**: qua nhiều vòng thì message càng ngày càng mất gốc — thông tin từ xa bị "pha loãng".

> **Tóm gọn 1 câu:** Over-smoothing = đào GNN quá sâu thì mọi node trở nên giống hệt nhau và mô hình không phân biệt được ai với ai — nên thực tế chỉ dùng 2-3 lớp.

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

> **Tóm gọn 1 câu:** Hai "bệnh" của GNN sâu là node bị dồn về giống nhau (over-smoothing) và thông tin xa bị nén mất (over-squashing); chữa bằng residual, chuẩn hóa, nối thêm cạnh, hoặc không đào sâu.

### 6.3 Graph Transformers — Vượt Qua Over-Smoothing

> **Graph Transformers (GraphGPS, GT)** dùng **self-attention trên toàn graph**: node có thể "nhìn" mọi node khác trực tiếp với đúng 1 lượt tính — **không phải qua chuỗi hops** nên không bị over-smoothing/over-squashing. Vượt trội trên dữ liệu cần **đường đi dài quan trọng**, graph có cấu trúc cục bộ phức tạp.
>
> **Giá phải trả:** attention matrix O(N²) memory cho N nodes → khó scale graph hàng triệu nodes. Giải pháp lai (GraphGPS): message-passing giữ local context + chỉ 1 block attention global.

> **Tóm gọn 1 câu:** Graph Transformer cho mọi node nhìn thẳng mọi node khác nên không mắc hai bệnh của GNN sâu — đổi lại tốn bộ nhớ O(N²), nên dùng kiểu lai (GraphGPS) cho graph lớn.

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

> 📄 **Code ví dụ:** [`examples/07-7-heterogeneous-temporal-gnn.py`](examples/07-7-heterogeneous-temporal-gnn.py)

> **Tóm gọn 1 câu:** KG thật có nhiều loại node/edge nên cần R-GCN, HAN hoặc HGT thay vì GNN thường; graph có thời gian thì dùng TGN.

---

## 8. Triển Khai Với PyG

<details>
<summary>Python Code — Complete Training Pipeline (Click để xem)</summary>

> 📄 **Code ví dụ:** [`examples/08-8-trien-khai-voi-pyg.py`](examples/08-8-trien-khai-voi-pyg.py)

</details>

> **Tóm gọn 1 câu:** PyG là thư viện Python chuẩn để dựng và huấn luyện GNN — pipeline đầy đủ gồm nạp graph, dựng model, train, và đo trên tập test.

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

Từ khóa trong labs: **AUC** = diện tích dưới đường cong ROC, đo khả năng phân biệt đúng/sai (1.0 = hoàn hảo, 0.5 = đoán mò); **negative sampling** = tạo ra các cặp sai cố tình để model học cách loại bỏ; **semi-supervised** = chỉ có rất ít node được gắn nhãn (4 node trong Lab 1).

> **Tóm gọn 1 câu:** Ba lab đi từ dễ đến khó: phân loại node trên graph nhỏ, đoán cạnh bị giấu, rồi điền thiếu quan hệ cho một KG mini.

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

> **Tóm gọn 1 câu:** Đây là nguồn gốc của từng kỹ thuật trong bài — đọc thêm khi cần đi sâu vào công thức hay benchmark.

---

## GraphRAG — Cập nhật 2026

Microsoft GraphRAG (2024-2025): dùng knowledge graph để enhance RAG. Query phức tạp (multi-hop) tốt hơn vector-only RAG. (**Multi-hop** = câu hỏi phải đi qua nhiều bước quan hệ, ví dụ "ai duyệt project của người từng quản lý AI team?". **RAG** = đưa tài liệu liên quan vào prompt trước khi LLM trả lời.)

**Tin mới 2025-2026:**
- **LazyGraphRAG** (Microsoft, cuối 2024): defer LLM summarisation tới query time — indexing cost ngang vector RAG, quality ngang full GraphRAG, query cost thấp hơn ~700×. Đã tích hợp Microsoft Discovery (2025) và Azure Local.
- **LightRAG** (HKUDS, EMNLP 2025): dual-layer graph + vector, incremental update thay vì re-index toàn bộ.
- **GraphRAG-Bench** (Microsoft, 06/2025): multi-hop + global queries GraphRAG thắng; single-hop factoid vanilla RAG thắng.
- **Gartner (2026)**: GraphRAG trong "Top Trends in D&A for 2026" cho complex cases mà high-accuracy RAG thất bại.
- **Knowledge Graph Market**: 1.48B USD (2025) → 2.04B USD (2026). GraphRAG chuyển từ "enterprise luxury" → production baseline.

Ref: https://microsoft.github.io/graphrag/

> **Tóm gọn 1 câu:** GraphRAG đã từ "xa xỉ của doanh nghiệp lớn" thành chuẩn production — với LazyGraphRAG, chi phí đã ngang vector RAG.

---

*Tiếp theo: [08 — Graph Workflow](../08-graph-workflow/)*
