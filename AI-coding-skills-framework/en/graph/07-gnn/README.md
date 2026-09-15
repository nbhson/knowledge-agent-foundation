# 🧬 07. GNN — Graph Neural Networks

> ## 📑 Table of Contents
>
> - [Opening Story](#opening-story)
> - [Why Are GNNs Important?](#why-are-gnns-important)
> - [Overview](#overview)
> - [Contents](#contents)
> - [1. What Is a GNN? Intuition](#1-what-is-a-gnn-intuition)
> - [2. GCN — Graph Convolutional Network](#2-gcn--graph-convolutional-network)
> - [3. GraphSAGE & GAT](#3-graphsage--gat)
> - [4. Link Prediction & Node Classification](#4-link-prediction--node-classification)
> - [5. GNN for Knowledge Graph Completion](#5-gnn-for-knowledge-graph-completion)
> - [6. GNN Limits & Ways Past Them](#6-gnn-limits--ways-past-them)
> - [7. Heterogeneous & Temporal GNNs](#7-heterogeneous--temporal-gnn)
> - [8. Implementation with PyG](#8-implementation-with-pyg)
> - [9. Hands-On Labs](#9-hands-on-labs)
> - [References](#references)

---

### Opening Story

You have a Knowledge Graph with 10,000 people and projects. You want to:

1. **Predict**: which project will Alice work on next? (link prediction)
2. **Classify**: which team does this person belong to? (node classification)
3. **Detect**: are any relations missing? (KG completion)

**Rule-based reasoning** (module 06) works with hand-written rules — but it doesn't scale when there are hundreds of relation types. **GNNs** learn automatically from the graph's structure: no rules to write, just examples needed.

> *"Rules tell the graph what you know. GNNs discover what you don't know you know."*

### Why Are GNNs Important?

> *"A GNN is deep learning for relational-structured data — the way a CNN is deep learning for images."*

| # | Source | Finding |
|---|-------|-----------|
| 1 | **OGB Benchmark (2024)** | GNNs boost **accuracy by 15-25%** on node classification vs an MLP using node features alone |
| 2 | **Knowledge Graph Completion (FB15k-237)** | R-GCN + a scoring function reaches **MRR 0.35** vs TransE's 0.29 |
| 3 | **Anthropic (2025)** | GNN-based link prediction suggests **missing relations** with 72% precision on an enterprise KG |

---

## Overview

```
Knowledge Graph
    │
    ├──► Node Features (text embeddings, properties)
    │         │
    │         ▼
    │   ┌─────────────────┐
    │   │   GNN Layers    │  ← Message Passing: aggregate neighbors
    │   │  GCN / GraphSAGE│     Update: combine self + neighbors
    │   │  GAT / R-GCN    │     Readout: graph-level embedding (if needed)
    │   └────────┬────────┘
    │            │
    │            ▼
    ├──► Node Embeddings ──► Node Classification ("Which team is Alice on?")
    │                       Link Prediction ("What will Alice WORKS_ON?")
    │                       Graph Classification ("What kind of graph is this?")
    │
    └──► KG Completion ──► Predict missing triples
```

---

## Contents

| # | Topic | Description |
|---|--------|-------|
| 1 | [GNN Intuition](#1-what-is-a-gnn-intuition) | Message passing, aggregation, update |
| 2 | [GCN](#2-gcn--graph-convolutional-network) | Spectral GCN, PyTorch code |
| 3 | [GraphSAGE & GAT](#3-graphsage--gat) | Inductive, attention |
| 4 | [Link Prediction](#4-link-prediction--node-classification) | Predict new relations |
| 5 | [KG Completion](#5-gnn-for-knowledge-graph-completion) | R-GCN, CompGCN |
| 6 | [Limits & Ways Past Them](#6-gnn-limits--ways-past-them) | Over-smoothing, expressivity, Graph Transformers |
| 7 | [Heterogeneous & Temporal](#7-heterogeneous--temporal-gnn) | RGCN/HAN/HGT, TGN for dynamic graphs |
| 8 | [PyG](#8-implementation-with-pyg) | Training pipeline |

---

## 1. What Is a GNN? Intuition

> **📌 Core Concept:**
> **GNN (Graph Neural Network)** = a neural network that operates **on graph structure**. Unlike an MLP (which only reads each node's features in isolation), a GNN also reads **the relationships between nodes**.
>
> **Like a CNN for images** (a CNN understands which pixels are next to each other), a **GNN for graphs** (a GNN understands which nodes connect to which nodes).
>
> **Analogies:**
> - **MLP = a student memorizing the text**: knows each theory line (node features) but doesn't understand how the document hangs together.
> - **GNN = wanting to understand a lesson, you ask classmates**: your embedding = (your knowledge) + (your friends' knowledge). Deeper layers → asking more, more indirect friends.

### 1.1 The Message Passing Framework

> **📌 Understand before reading the formula:**
> **Message Passing** = each node computes a new embedding by:
> 1. **MESSAGE**: each neighbor "sends a message" to the node (embedding + the relation between the two nodes)
> 2. **AGGREGATE**: the node "combines" all the messages (mean / sum / max)
> 3. **UPDATE**: the node "merges" the aggregated message with itself → new embedding
>
> After **K layers** (K rounds), a node's embedding contains information from nodes **K hops away**.

```
Worked example — "Alice needs to understand her team":
  Layer 1: Alice receives messages from Bob + Carol (her closest contacts)
    → Alice learns: Bob works on Phoenix, Carol works on Atlas
  Layer 2: Alice receives messages from Bob's friend (Dave) + Carol's friends
    → Alice learns: Dave works on AI Research
  Layer 3: Alice learns about "Dave's team"...

→ After K layers, Alice knows information K steps away in the graph
```

```
For node v at layer k:

  1. MESSAGE:  m_{vu}^k = MSG(h_v^{k-1}, h_u^{k-1}, e_{vu})  for each neighbor u
     → Each neighbor u writes 1 "message" to v
     → The message contains: v's embedding, u's embedding, the relation e_uv

  2. AGGREGATE: a_v^k = AGG({m_{vu}^k : u ∈ N(v)})            combine messages
     → v combines all messages (usually MEAN = the average)

  3. UPDATE:   h_v^k = UPDATE(h_v^{k-1}, a_v^k)               update the embedding
     → v merges its old self + the aggregated message → a richer new embedding

  h_v^0 = initial features (text embedding, one-hot, etc.)
  h_v^K = final embedding after K layers (holds K-hop information)

One-layer example for Alice:

  Alice(h_A) ◄── Bob(h_B) + Carol(h_C)     (neighbors)

  a_Alice = MEAN(h_Bob, h_Carol)           (aggregate)
  h_Alice' = ReLU(W · CONCAT(h_Alice, a_Alice))  (update)
```

### 1.2 Why Is a GNN Stronger Than an MLP?

```
MLP: only uses that node's features
  h_Alice' = MLP(h_Alice)  ← knows nothing about neighbors

GNN: uses the whole graph structure
  h_Alice' = GNN(h_Alice, h_Bob, h_Carol, h_Phoenix)
  → Alice's embedding contains information about her team and projects
  → 2 people on the same team → their embeddings are close (even if initial features differ)

Example: Alice and Carol have never met (no direct edge),
       but both WORKS_ON Phoenix
       → GNN: Alice's & Carol's embeddings are close (same group)
       → MLP: embeddings differ (because initial features differ) — doesn't know they're connected
```

---

## 2. GCN — Graph Convolutional Network

### 2.1 The GCN Formula (Kipf & Welling, 2017)

> **📌 Understand before reading the formula:**
> **GCN = a node takes a *weighted average* of its neighbors + itself, then passes through a fully-connected layer + ReLU.**
> *Weighted average* = each node contributes in inverse proportion to its number of neighbors (so a highly-connected node doesn't "drown out" a sparsely-connected one).
>
> **Analogies:**
> - **GCN = a group discussion**: each person = a node. Each layer = one group meeting: everyone shares opinions (message), then everyone consolidates into a new opinion (update). Listening to many friends → broader understanding.
> - **Activation (ReLU) = noise filtering**: keeps only the positive signal, discards the negative (negative) signal — helps the model learn nonlinear patterns.

```
H^{(l+1)} = σ( D^{-1/2} Â D^{-1/2} H^{(l)} W^{(l)} )

  Â = A + I          (adjacency + self-loop — add "myself" to the friends list)
  D = degree matrix  (normalization — divide by number of neighbors to balance)
  H^{(l)} = (N, D_l) node embeddings at layer l
  W^{(l)} = (D_l, D_{l+1}) learnable weights (the layer's filter)
  σ = ReLU (discard negative values)

Read as a sentence:
  "The new embedding of all nodes = (normalized) × (average of myself + my friends) × (learned filter) × (discard negative values)"
```

**Warning for beginners:** don't misunderstand GCN as "automatically learning relations". GCN only **averages** neighbors (uniformly), without distinguishing which neighbor is important. If you need to distinguish importance → use GAT (Section 3).

<details>
<summary>Python Code — GCN Layer From Scratch (Click to view)</summary>

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
        adj: (N, N) — adjacency matrix (normalized)
        """
        # Aggregate: adj @ x → each node takes the average of neighbors
        agg = adj @ x  # (N, in_dim)
        # Transform + activation
        out = self.linear(agg)  # (N, out_dim)
        return F.relu(out)

def normalize_adjacency(adj: torch.Tensor) -> torch.Tensor:
    """Normalize: D^{-1/2} (A + I) D^{-1/2}"""
    n = adj.shape[0]
    adj_hat = adj + torch.eye(n)  # add self-loop
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

### 2.2 2-Layer GCN for Node Classification

<details>
<summary>Python Code — 2-Layer GCN (Click to view)</summary>

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

# Labels: only a few nodes have labels (semi-supervised)
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

> **📌 Core Concept:**
> - **GCN** — needs the **full adjacency matrix** up front (transductive), can't extend to new nodes
> - **GraphSAGE** — learns a reusable **aggregator function** → **inductive**, new nodes can be embedded immediately
> - **GAT** — adds **attention**: each neighbor has a different importance
>
> **Analogies:**
> - **GCN = memorizing your own neighborhood**: knows every alley in that area. A new neighborhood → learn from scratch.
> - **GraphSAGE = learning how to listen**: ask friends then consolidate → applies anywhere; new friend → ask the new friend.
> - **GAT = choosing friends selectively**: not every friend carries equal weight — teachers matter more than passing acquaintances.

### 3.1 GraphSAGE — Inductive

GraphSAGE differs from GCN in that: **it learns the aggregator function**, not trained on a fixed adjacency → can embed new nodes.

> **Plain-language explanation:** GCN computes the neighbor average AT TRAINING TIME (depends on a fixed adjacency). GraphSAGE learns a separate "friend-combining formula" (aggregator), so any new node only needs to run that formula on its own neighbors.

```
GraphSAGE aggregators (3 ways to combine friends):
  - Mean:  a_v = mean({h_u : u ∈ N(v)})
           → arithmetic mean (like GCN)
  - LSTM:  a_v = LSTM(random_permutation(N(v)))  — has order!
           → learns that "order" can matter (not fully order-invariant)
  - Pooling: a_v = max({MLP(h_u) : u ∈ N(v)})
           → each friend casts one vote, keep the strongest vote on each dimension

  h_v^k = σ( W^k · CONCAT(h_v^{k-1}, a_v^k) )
  → Concatenate "old me" + "my friends", transform with the learned filter
```

### 3.2 GAT — Attention

GAT learns an **attention weight** per neighbor — not everyone is equally important.

> **Plain-language explanation:** instead of "averaging all friends", GAT learns: "which are my important friends?" → gives them a high weight. How importance is scored: **compare my vector with my friends' vectors** (concatenate then pass through a learned function + activation).

```
Step 1 — score each neighbor's importance:
  score(v,u) = LeakyReLU( a^T [W h_v || W h_u] )
  → "How much do I (W h_v) and my friend (W h_u) have in common?"

Step 2 — normalize into weights (sum = 1):
  α_{vu} = softmax(score(v,u))  
  → "What percentage do my friends contribute to me?"

Step 3 — weighted combination:
  h_v' = σ( Σ_{u∈N(v)} α_{vu} · W h_u )
  → "Important friend → contributes more; less important friend → contributes less"

Multi-head (multiple "viewpoints"):
  h_v' = CONCAT(head_1, ..., head_K)  or  MEAN(heads)
  → Like asking K separate experts then combining — lower variance, more stable
```

<details>
<summary>Python Code — GAT with PyG (Click to view)</summary>

```python
# pip install torch torch-geometric

import torch
from torch_geometric.nn import GATConv, SAGEConv
from torch_geometric.data import Data

# Prepare data
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
        # GATConv with heads: output = hid_c * heads
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

### 3.3 Comparison

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

### 4.1 Link Prediction — "What will Alice WORKS_ON?"

<details>
<summary>Python Code — Link Prediction (Click to view)</summary>

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
        """Score edges by dot product."""
        src = z[edge_label_index[0]]  # (E, out_dim)
        dst = z[edge_label_index[1]]
        return (src * dst).sum(dim=-1)  # (E,) scores
    
    def forward(self, x, edge_index, edge_label_index):
        z = self.encode(x, edge_index)
        return self.decode(z, edge_label_index)

# Data
edge_index = torch.tensor([[0,1,1,2,2,3],[1,0,2,1,3,2]], dtype=torch.long)
x = torch.randn(4, 8)
# Positive edges (existing) + negative sampling
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

# Predict: which node will Alice(0) connect to?
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

### 4.2 Node Classification — "Which team is this person on?"

```python
# Already covered in §2.2 — 2-layer GCN with cross-entropy loss
# Add: class imbalance handling

# If team A has 100 people and team B has 10 → weighted loss
class_weights = torch.tensor([1.0, 10.0])  # weight for the minority class
loss = F.cross_entropy(out[train_mask], labels[train_mask], weight=class_weights)
```

---

## 5. GNN for Knowledge Graph Completion

### 5.1 R-GCN — Relational GCN

For a heterogeneous KG with many relation types, R-GCN has **separate weights for each relation**:

```
h_v^{(l+1)} = σ( Σ_{r∈R} Σ_{u∈N_r(v)} (1/c_{v,r}) W_r^{(l)} h_u^{(l)} + W_0^{(l)} h_v^{(l)} )

  R = set of relations (MANAGES, WORKS_ON, ...)
  W_r = dedicated weights for relation r
  c_{v,r} = normalization (number of neighbors via relation r)
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

# edge_type: (E,) — relation type for each edge
edge_index = torch.tensor([[0,1,2,0],[1,2,3,2]], dtype=torch.long)
edge_type = torch.tensor([0, 1, 0, 1])  # 0=MANAGES, 1=WORKS_ON
x = torch.randn(4, 8)

model = RGCN(8, 16, 8, num_relations=2)
out = model(x, edge_index, edge_type)
print(f"R-GCN output: {out.shape}")  # (4, 8)
```

### 5.2 Scoring Functions for KG Completion

Once you have embeddings from R-GCN, use a scoring function to predict missing triples:

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

## 6. GNN Limits & Ways Past Them

> **📌 Core Concept:**
> GNN message passing is powerful, but **going too deep breaks it**. These are the 2 "diseases" most cited in the research, and you need to know them so you don't pick GNN for the wrong problem.

### 6.1 Over-Smoothing (When Nodes Become... Alike)

> **Over-smoothing** = after many GCN layers, **all nodes' features converge toward the same value** — node A and node Z (totally unrelated) end up with the same vector, and the model can't tell anyone from anyone. Node classification falls apart badly.
>
> **Analogies:** like the game **"telephone"**: after many rounds the message is increasingly far from the original — information from far away gets "diluted".

### 6.2 Over-Squashing + Expressivity (WL Test)

> **Over-squashing** = a **bottleneck** in the graph. A node in a densely-connected region "blocks" information flow from distant regions → far-apart nodes are nearly **incapable of communicating**, even with 10 GNN layers. Long paths get squashed and lose detail.
>
> **Expressivity** = standard GNN message passing is **no stronger than the WL test** (the Weisfeiler-Lehman isomorphism-checking algorithm from 1968). Meaning there exist different graphs that a standard GNN **cannot distinguish**. This limit is very practical when comparing graphs/molecules.
>
> **Remedies (fixes) — pick one of the following:**
> - **Residual connections** (skip a layer) — like a GCN with `residual`
> - **Normalization** — normalize features after each layer
> - **Rewiring / graph surgery** — add short edges between distant nodes ("graph rewiring")
> - **Just use 2-3 layers** instead of going deep — in practice a 2-layer GraphSAGE beats a 10-layer one

### 6.3 Graph Transformers — Getting Past Over-Smoothing

> **Graph Transformers (GraphGPS, GT)** use **self-attention over the whole graph**: a node can "look at" any other node directly in a single computation pass — **not through a chain of hops**, so no over-smoothing/over-squashing. They excel on data where **long-range paths matter**, on graphs with complex local structure.
>
> **The price:** the attention matrix is O(N²) memory for N nodes → hard to scale to million-node graphs. The hybrid solution (GraphGPS): message-passing keeps local context + just one global attention block.

---

## 7. Heterogeneous & Temporal GNN

> **📌 Core Concept:**
> **Heterogeneous graph** = a graph with **many node types and many edge types** — real KGs are all heterogeneous (`Person`-`WORKS_ON`->`Project`, `Person`-`REPORTS_TO`->`Person`, `Project`-`HAS_BUDGET`->`Number`). Standard GNNs (GCN/GraphSAGE) assume **every node and every edge is the same type** — shoving a KG straight in loses the meaning of each relation.
>
> **3 representative model families for heterogeneous graphs:**
> - **R-GCN (Relational GCN)**: each relation type has its own W matrix — like "each relation type is a different 'lens'" → each relation's messages go through its own lens (covered in section 5).
> - **HAN (Heterogeneous Attention Network)**: hierarchical **meta-path** — aggregates along each "path type" (`P--WORKS_ON--Project--HAS_BUDGET--Budget`) then attention between meta-paths.
> - **HGT (Heterogeneous Graph Transformer)**: applies the Transformer with layer separation by node/edge type — attends to relative importance across relation types, SOTA for modern KGs.
>
> **When to use:** your real KG (Module 02) is always heterogeneous → if you need node embeddings that exploit relation semantics, don't flatten to homogeneous.
>
> **Temporal GNN (TGN)** = an extension for **graphs that change over time** (event logs, transactions). Instead of a static snapshot, TGN processes an **event stream** per timestamp — each event "knocks" on a node, and the node updates its memory. Combined with temporal embeddings (Module 04) it becomes a complete time-aware prediction pipeline.

```python
# Pseudocode — HGT: attention per (node_type, edge_type) pair
def hgt_message(head, rel, tail):
    # Project already has a different node type than Person → use dedicated matrices
    W_head = weight_matrix[head.node_type]
    W_edge = weight_matrix[rel.edge_type]
    W_tail = weight_matrix[tail.node_type]
    attn = attention(W_head @ head.h, W_edge @ rel.h, W_tail @ tail.h)
    return attn * (W_head @ head.h)
```

---

## 8. Implementation with PyG

<details>
<summary>Python Code — Complete Training Pipeline (Click to view)</summary>

```python
import torch
import torch.nn.functional as F
from torch_geometric.nn import GCNConv
from torch_geometric.data import Data
from torch_geometric.utils import train_test_split_edges

# 1. Prepare data
edge_index = torch.tensor([
    [0,1,1,2,2,3,3,0,0,2],
    [1,0,2,1,3,2,0,3,2,0]
], dtype=torch.long)
x = torch.randn(4, 16)
y = torch.tensor([0, 0, 1, 1])  # 2 classes

data = Data(x=x, edge_index=edge_index, y=y, num_nodes=4)
# Split edges for link prediction
# data = train_test_split_edges(data)  # for large graphs

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
        return x  # embeddings for link prediction

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

## 9. Hands-On Labs

### Lab 1: Node Classification on Karate Club

1. Load `nx.karate_club_graph()`, create features (degree, one-hot, or random)
2. Train a 2-layer GCN, measure accuracy with 4 labeled nodes (semi-supervised)
3. Compare against MLP (no graph) — GNN must win

### Lab 2: Link Prediction

1. Mask 20% of the edges of a 100-node graph
2. Train a link predictor (§4.1), measure AUC on the masked edges
3. Try different negative sampling ratios (1:1 vs 1:5)

### Lab 3: Mini KG Completion

1. Build a small KG: 20 entities, 3 relations, 50 triples
2. Train R-GCN + DistMult scoring
3. Ask: `(Alice, WORKS_ON, ?)` → rank all entities, check the rank of the correct answer

---

## References

- Kipf & Welling — *Semi-Supervised Classification with Graph Convolutional Networks* (ICLR 2017)
- Hamilton et al. — *Inductive Representation Learning on Large Graphs (GraphSAGE)* (NeurIPS 2017)
- Veličković et al. — *Graph Attention Networks* (ICLR 2018)
- Schlichtkrull et al. — *Modeling Relational Data with Graph Convolutional Networks (R-GCN)* (ESWC 2018)
- *Graph Transformers: A Survey* (arXiv:2502.16533) — over-smoothing/over-squashing, GraphGPS
- *Over-smoothing & Over-squashing in GNNs* (arXiv:2502.10818) — remedies: residual, rewiring
- Hamilton — *Graph Representation Learning* (2020) — WL-test expressivity, chapter 9
- PyG Docs — *Creating Your Own GNN* (https://pytorch-geometric.readthedocs.io/)
- OGB — *Open Graph Benchmark* (https://ogb.stanford.edu/)

---

*Next: [08 — Graph Workflow](../08-graph-workflow/)*
