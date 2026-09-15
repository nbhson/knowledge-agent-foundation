# 🔢 04. Graph Embeddings — Vectorizing the Graph

> ## 📑 Table of Contents
>
> - [Opening Story](#opening-story)
> - [Why Do Graph Embeddings Matter?](#why-do-graph-embeddings-matter)
> - [Overview](#overview)
> - [Contents](#contents)
> - [1. What Are Graph Embeddings?](#1-what-are-graph-embeddings)
> - [2. Shallow Embeddings: Node2Vec, DeepWalk](#2-shallow-embeddings-node2vec-deepwalk)
> - [3. GNN-Based Embeddings: GraphSAGE, GAT](#3-gnn-based-embeddings-graphsage-gat)
> - [4. Knowledge Graph Embeddings: TransE, RotatE](#4-knowledge-graph-embeddings-transe-rotate)
> - [5. Hybrid Search: Vector + Graph](#5-hybrid-search-vector--graph)
> - [6. Hands-On Labs](#6-hands-on-labs)
> - [References](#references)

---

### Opening Story

You have a Knowledge Graph with 10,000 nodes. The user asks: *"Find the person most similar to Alice in role and relationships."*

- **Graph traversal**: find the person with the same number of neighbors? Not enough — Alice manages 5 people, Bob also manages 5 people, but completely different teams.
- **Text embedding**: embed Alice's `description` and compare? You ignore the whole graph structure.
- **Graph embedding**: each node becomes a vector **based on its position in the graph** → `cosine(alice_vec, bob_vec)` is high if they have similar roles/structures.

**Graph Embeddings turn graph structure into vectors — so you can use ANN search while still keeping the relationship information.**

### Why Do Graph Embeddings Matter?

> *"The graph tells you WHO is connected. Embeddings tell you WHO IS SIMILAR without being directly connected."*

| # | Source | Finding |
|---|-------|-----------|
| 1 | **Node2Vec Paper (2016)** | Graph embeddings improve **link prediction accuracy by 22%** compared to using only node features |
| 2 | **Microsoft GraphRAG (2024)** | Combining text embeddings + graph embeddings boosts **retrieval precision by 18%** |
| 3 | **OGB Benchmark (2024)** | GraphSAGE embeddings + ANN search are **50× faster** than pure traversal for k-NN queries on 1M nodes |

---

## Overview

```
Knowledge Graph
    │
    ├──► Text Embeddings ──► Vector DB (semantic search)
    │      "Alice is the CTO" → [0.23, -0.45, ...]
    │
    ├──► Graph Embeddings ──► Vector DB (structural search)
    │      Alice's position in the graph → [0.67, 0.12, ...]
    │
    └──► Hybrid ──► Fused Score: α·text_score + (1-α)·graph_score
           The best of both worlds
```

---

## Contents

| # | Topic | Description |
|---|--------|-------|
| 1 | [What Are Graph Embeddings?](#1-what-are-graph-embeddings) | Definition, intuition, classification |
| 2 | [Node2Vec/DeepWalk](#2-shallow-embeddings-node2vec-deepwalk) | Random walk embeddings |
| 3 | [GNN Embeddings](#3-gnn-based-embeddings-graphsage-gat) | GraphSAGE, GAT |
| 4 | [KG Embeddings](#4-knowledge-graph-embeddings-transe-rotate) | TransE, RotatE for KG completion, TKGE, Graph Transformers |
| 5 | [Hybrid Search](#5-hybrid-search-vector--graph) | Combining vector + graph (RRF, weighted) |

---

## 1. What Are Graph Embeddings?

> **📌 Core Concept:**
> **Graph Embedding** = turning nodes in a graph into **a sequence of numbers (a vector)** such that:
> 1. Nodes **close together in the graph** → close vectors (small distance)
> 2. Nodes **with the same role** → close vectors (even if not adjacent)
>
> **Why do we need this?** Because vectors can be **compared with cosine similarity** and **stored in a vector DB** for fast ANN search. Graph structure → vector space → usable for RAG, clustering, classification.

**Analogies to understand it:**
- **Graph = city map**: graph embedding = GPS coordinates (latitude, longitude) — each city (node) has coordinates, and cities close on the map have close coordinates
- **Graph embedding = photo portrait**: each node is "photographed" as a vector — clearly showing which features matter (position, role, community)

### 1.1 Intuition

```
Graph (discrete structure)  ──Embed──►  Vector Space (continuous, comparable)

Alice ──MANAGES──► Bob              alice_vec = [0.23, 0.81, -0.15, ...]
  │                  │              bob_vec   = [0.25, 0.79, -0.12, ...]  ← close to alice!
  └─WORKS_ON──► Phoenix            phoenix_vec = [0.88, 0.10, 0.42, ...]  ← farther (different type)

Small distance in vector space = Similar role/structure in the graph
```

**The end goal:** learn a function `f: V → R^d` (from node → d-dimensional real vector) such that:
- Nodes close in the graph → close vectors
- Nodes with similar roles → close vectors (even if not adjacent)

**Why is this harder than regular text embedding?** Text embedding only needs to understand **content** (Alice = "CTO" "manages"). Graph embedding needs to understand **position in the structure** too (Alice sits in a "central" position connecting many other nodes).

### 1.2 Classification

```
┌──────────────────────┬──────────────────────┬───────────────────────────────┐
│ Type                 │ Needs Training?      │ Best For                      │
├──────────────────────┼──────────────────────┼───────────────────────────────┤
│ Node2Vec / DeepWalk  │ Unsupervised (walks) │ General similarity, clustering│
│ GraphSAGE / GAT      │ Supervised / Semi    │ Node classification, inductive│
│ TransE / RotatE      │ KG triples           │ KG completion, link prediction│
│ Text + Graph Hybrid  │ Both                 │ GraphRAG, enterprise search   │
└──────────────────────┴──────────────────────┴───────────────────────────────┘
```

---

## 2. Shallow Embeddings: Node2Vec, DeepWalk

> **📌 Core Concept:**
> **Random Walk** = walking randomly through a graph — each step picks a random neighbor to move to.
> **DeepWalk/Node2Vec** = generates many "random paths" in the graph → uses Word2Vec (the same technology that understands words in NLP) to understand each node's position.
>
> **Why are they called "shallow"?** Because each node gets its own dedicated vector (strictly 1-to-1, like a dictionary) — so you have to retrain whenever a new node is added. Only suitable for small graphs.

**Analogies:**
- **Random Walk = strolling around town**: you start at "Alice", at each intersection you pick a direction at random → see which places you keep passing through. If "Alice" and "Bob" keep meeting on the same paths → they live in the same area.
- **DeepWalk = Google Maps but lost**: wander randomly around an area, record the places you pass → understand the terrain's structure.

### 2.1 DeepWalk — Random Walks + Word2Vec

> **Principle:** turn the graph into "text" by generating random walks → use Word2Vec (Skip-gram) to learn the embeddings.

```
Worked example:

Graph: Alice → Bob → Carol → Dave
                    ↘ Phoenix

Step 1: Generate many random walks (walk randomly)
  Walk 1: Alice → Bob → Carol → Dave     (each step picks a random neighbor)
  Walk 2: Alice → Bob → Phoenix → Bob
  Walk 3: Bob → Phoenix → Bob → Alice

Step 2: Treat each walk as a "sentence", each node as a "word"
  → "Alice Bob Carol Dave" = one sentence
  → Word2Vec learns: "Alice" often appears with "Bob" → their two vectors are close

Result: Nodes that often "appear together on random paths" → close vectors
```

### 2.2 Node2Vec — Biased Random Walks (added control)

> **What's new compared to DeepWalk:** adds two parameters `p` and `q` to **control the direction** of the walk — instead of walking purely at random, you decide whether to "go far" or "stay close".

```python
# How p and q work:

p = return parameter (probability of going back to the node you just left):
  - small p (0.5): often returns → explores the tight neighborhood
  - large p (2.0): rarely returns → goes farther

q = in-out parameter (probability of going far vs returning):
  - small q (0.5): tends to go far (DFS-like) → explores far-flung structure
  - large q (2.0): tends to stay close (BFS-like) → explores local community

# Simplest way to understand:
# q < 1 (DFS-like): "I want to find someone with the SAME ROLE" even in another team
# q > 1 (BFS-like): "I want to find someone in the SAME TEAM"
```

<details>
<summary>Python Code — Node2Vec with NetworkX (Click to view)</summary>

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
    """Create embeddings with random walks + Word2Vec."""
    # Generate the corpus: many random walks
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
    
    # Return a dict node -> vector
    return {node: model.wv[node] for node in graph.nodes() if node in model.wv}

# Usage
G = nx.karate_club_graph()
# Rename node labels to strings for Word2Vec
G_labeled = nx.relabel_nodes(G, {n: f"node_{n}" for n in G.nodes()})
embeddings = deepwalk_embeddings(G_labeled, num_walks=10, walk_length=20, embedding_dim=64)

# Find similar nodes
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

### 2.3 When to Use Node2Vec?

| Situation | Use it? | Reason |
|-----------|-------|-------|
| Small-medium graph (<100K nodes) | ✅ | Fast, no GPU needed, unsupervised |
| Need inductive (new nodes) | ❌ | Must retrain everything — use GraphSAGE instead |
| Need edge features / node features | ❌ | Node2Vec only uses structure — use GNNs |
| Clustering / community detection | ✅ | Embeddings reflect community structure well |

---

## 3. GNN-Based Embeddings: GraphSAGE, GAT

> **📌 Core Concept:**
> **Problem:** Node2Vec has to **retrain everything** when a new node appears (because each node has its own vector).
> **Solution:** a **GNN (Graph Neural Network)** learns a **single aggregation function** — *for any node, just look at its neighbors and you can compute the vector*. → A new node only needs the function "run" on it, no retraining.
>
> **Analogies:**
> - **Node2Vec = fixed photo**: each person has to stand still for their own portrait. A new person joins → you have to photograph the whole group again.
> - **GraphSAGE = describe a person through their friends**: anyone can be described as "the average of their friends" + "their own traits". A new person → just ask their friends and you can describe them right away.

### 3.1 GraphSAGE — Inductive Node Embeddings

> **To read the formula:** GraphSAGE learns an **aggregate** function that gathers information from neighbors, so it can embed **never-before-seen nodes** without retraining.

```
Formula (translated into plain language):

  h_v^k = σ( W^k · CONCAT( h_v^{k-1}, AGGREGATE({h_u^{k-1} : u ∈ N(v)}) ) )

Explanation of each symbol:
  h_v^k    = the embedding of node v AFTER layer k (has "heard" information k hops away)
  h_v^{k-1}= the embedding BEFORE that (k-1 hops away)
  N(v)     = v's neighbors (the friends around it)
  AGGREGATE= how to "combine" information from the friends:
              MEAN (take the average) / LSTM / MAX-pooling
  CONCAT   = "join together": concatenate [me before] + [my friends]
  W^k      = weights (learned coefficients) — act as a "filter" to transform the information
  σ        = activation function (usually ReLU — drops negative values)

Read as: "My new embedding = a blend of (my own traits) with (the aggregate of my friends' traits), then transformed by one neural layer"

K layers = K rounds of "asking friends" — the final node knows information K hops away
  Layer 1: knows direct friends (1 hop)
  Layer 2: knows friends of friends (2 hops)
  Layer 3: knows friends of friends of friends (3 hops)
```

```python
# Pseudocode: GraphSAGE forward
def graphsage_layer(node_features, adjacency, weights, aggregator="mean"):
    """
    node_features: (N, D) — features of N nodes
    adjacency: (N, N) — adjacency matrix
    """
    # Aggregate neighbors
    if aggregator == "mean":
        neighbor_agg = adjacency @ node_features / adjacency.sum(axis=1, keepdims=True)
    
    # Concatenate self + neighbors
    combined = np.concatenate([node_features, neighbor_agg], axis=1)
    
    # Transform
    output = np.maximum(0, combined @ weights)  # ReLU
    # Normalize
    output = output / np.linalg.norm(output, axis=1, keepdims=True)
    return output
```

### 3.2 GAT — Graph Attention Networks

> **📌 Core Concept:**
> **Problem:** GraphSAGE aggregates friends with a **simple average (uniform `mean`)** — meaning every friend counts as equally important.
> **Solution (GAT):** learn **attention weights** — the node decides for itself which friends matter more. Like listening to advice: your mentor's words weigh more than those of a casual acquaintance.

```
Formula (translated into plain language):

  α_{vu} = softmax( LeakyReLU( a^T [W h_v || W h_u] ) )
  h_v' = σ( Σ_{u∈N(v)} α_{vu} · W h_u )

Explanation:
  α_{vu} = the "importance" of neighbor u to node v  (sums to 1, thanks to softmax)
  Before = each neighbor contributes EQUALLY (average)
  GAT    = whichever neighbor is more trustworthy contributes MORE

Concrete example:
  Org chart: Alice's neighbors: Bob (direct report) + Dave (casual acquaintance)
  AGGREGATE (GraphSAGE): Bob contributes 50% + Dave contributes 50%
  ATTENTION (GAT):       Bob contributes 83% + Dave contributes 17%  ← learned "MANAGES matters more than KNOWS"
```

<details>
<summary>Python Code — GraphSAGE with PyG (Click to view)</summary>

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

# Create graph data
# edge_index: (2, E) — list of edges
edge_index = torch.tensor([[0, 1, 1, 2, 2, 3],
                           [1, 0, 2, 1, 3, 2]], dtype=torch.long)
x = torch.randn(4, 16)  # 4 nodes, 16 features per node

model = GraphSAGE(in_channels=16, hidden_channels=32, out_channels=8)
embeddings = model(x, edge_index)
print(f"Embeddings shape: {embeddings.shape}")  # (4, 8)
print(f"Embedding node 0: {embeddings[0]}")
```

</details>

### 3.3 Comparison

```
┌─────────────────┬──────────────────┬──────────────────┬──────────────────────┐
│ Property        │ Node2Vec         │ GraphSAGE        │ GAT                  │
├─────────────────┼──────────────────┼──────────────────┼──────────────────────┤
│ Inductive?      │ ❌ (transductive) │ ✅               │ ✅                   │
│ Needs features? │ ❌ (structure only)│ ✅             │ ✅                   │
│ Attention?      │ ❌ (uniform)      │ ❌ (mean)        │ ✅ (learned weights) │
│ Scalability     │ O(walks × len)    │ O(E) per layer   │ O(E) + attention     │
│ Training        │ Unsupervised      │ Supervised/Semi  │ Supervised           │
│ Best for        │ Clustering, viz   │ Classification   │ Heterogeneous, ranked│
└─────────────────┴──────────────────┴──────────────────┴──────────────────────┘
```

---

## 4. Knowledge Graph Embeddings: TransE, RotatE

> **📌 Core Concept:**
> **KG Embedding** differs from Node2Vec/GNN in that it learns **nodes AND relations together** — the goal is **link prediction**: predicting missing relations.
>
> **Analogies:**
> - **TransE = translation**: `vec(Alice) + vec(WORKS_ON) ≈ vec(Phoenix)`. Like navigation: "from Alice, follow the WORKS_ON direction and you arrive at Phoenix". If another project fits this direction → you can predict it.
> - **RotatE = rotation**: a relation is an "angle" — rotate Alice's vector by that angle to get Phoenix's vector. Makes sense for symmetric relations like "married" (rotate 180°).

KG embeddings learn **both nodes and relations** together — to do **link prediction**: `(Alice, WORKS_ON, ?)` → predict which project.

### 4.1 TransE — Translation Principle

> **Core idea (easiest): if the triple `(Alice, WORKS_ON, Phoenix)` is true, then:
> **vector(Alice) + vector(WORKS_ON) ≈ vector(Phoenix)**
>
> In other words: "Alice" + "the action of working on" ≈ "Phoenix". The relation acts as a **translation vector** — like a direction and distance.

```
TransE: h + r ≈ t

If (Alice, WORKS_ON, Phoenix) is true:
  vec(Alice) + vec(WORKS_ON) ≈ vec(Phoenix)

Score: ||h + r - t|| → low = correct triple, high = wrong

              WORKS_ON
  Alice ───────────────► Phoenix
  vec_h + vec_r  ≈  vec_t

  ❌ (Alice, WORKS_ON, Unknown) → ||h + r - t|| large → not valid
```

**Everyday example:** you have a formula "city + direction = destination". `Hanoi + North = ThaiNguyen` (correct), `Hanoi + North = SaiGon` (wrong — the vector is too far). TransE learns these vectors from data to predict a plausible destination for a new relation.

### 4.2 RotatE — Rotation in Complex Space

> **Idea:** instead of a relation being a "translation", RotatE treats a relation as a **rotation** in the complex plane. Each relation is a rotation angle: rotate vector `h` by that angle → lands near `t`.

```
RotatE: h ◦ r ≈ t  (◦ = element-wise rotation in complex space)

r is a complex vector with |r_i| = 1 (unit) → rotates h to be near t

Advantage: models symmetry, inversion, composition
  - (A, married_to, B) ↔ (B, married_to, A)  →  r = 180° rotation
  - (A, part_of, B) + (B, part_of, C) → (A, part_of, C)
```

**Everyday example:** the "married" relation is like a **180° turn**: A turns half a circle to reach B, and B turns half a circle to reach A (symmetric). TransE can't handle this well (because `A + r = B` doesn't imply `B + r = A`), but RotatE can.

<details>
<summary>Python Code — TransE Training Loop (Click to view)</summary>

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
        """Score triples — lower is better."""
        h_e = self.entity_emb(h)  # (batch, dim)
        r_e = self.relation_emb(r)
        t_e = self.entity_emb(t)
        # L1 distance: ||h + r - t||
        score = torch.norm(h_e + r_e - t_e, p=1, dim=1)
        return score  # (batch,)
    
    def predict_tail(self, h: int, r: int, all_entities: int) -> torch.Tensor:
        """Given (h, r, ?), rank all entities by score."""
        h_e = self.entity_emb(torch.tensor([h]))
        r_e = self.relation_emb(torch.tensor([r]))
        all_t = self.entity_emb.weight  # (num_entities, dim)
        scores = torch.norm(h_e + r_e - all_t, p=1, dim=1)
        return scores  # lowest = best prediction

# Training
model = TransE(num_entities=1000, num_relations=10, dim=100)
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

for epoch in range(100):
    # Positive triples: correct (h, r, t)
    h_pos = torch.randint(0, 1000, (32,))
    r_pos = torch.randint(0, 10, (32,))
    t_pos = torch.randint(0, 1000, (32,))
    
    # Negative triples: corrupt the tail
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
# top_k = torch.topk(scores, k=5, largest=False)  # 5 projects with the lowest scores
```

</details>

### 4.3 Temporal KG Embeddings (TKGE)

> **📌 Core Concept:**
> **Temporal KG embeddings** = learning vectors that know **space and time** — a triplet is no longer `(h, r, t)` but `(h, r, t, time)`, because most knowledge is NOT invariant:
> - `(Alice, WORKS_ON, Phoenix, 2023)` — true in 2023
> - `(Alice, WORKS_ON, Phoenix, LATER THAN 2025)` — **wrong**: Alice moved to another project
>
> **Why is this so simple?** A time-aware embedding has to answer: *"is this relationship still true at time X?"* — that's the **Temporal Knowledge Graph Completion (TKGC)** problem.
>
> **Model families (read as "strategies"):**
> - **Time-parameterized translation**: adds a time parameter to TransE/RotatE (e.g. **TuckERTNT** splits the tensor by time).
> - **Temporal message passing (time-indexed GNN)**: each event is a "moment of communication", nodes learn when to send/receive information — the standout example is **TGN (Temporal Graph Networks)**.
> - **Tendency-guided**: predicts the "trend of change" of a relation over time before querying the embedding.
>
> **Analogy:** TransE is a "static map". TKGE is **"the map + a change log"** — you have to know which year "Bridge A" collapsed so you don't take the wrong route.
>
> **When do you need this?** Only when your graph has a time column and the questions depend on the moment (recommendations, service logs, news, work history). If the graph isn't temporal, don't add the complexity.

### 4.4 Graph Transformers (GTs) — The Next Generation

> **📌 Core Concept:**
> **Graph Transformers** = applying the **self-attention mechanism (like in LLMs)** to graphs: each node "pays attention" to the whole graph instead of only its direct neighbors. This direction addresses the inherent limits of GNN message-passing (see "limitations" in detail in Module 07).
>
> **An easy-to-picture question:** GNN = a person who only asks **their direct neighbors** (1–3 rounds). Graph Transformer = a person who can **scan all the relationships** in the graph at once to decide who matters most.
>
> **The typical branch (GraphGPS, GT)** combines whole-graph attention + message passing: it keeps local chains but adds a "long view". The price: **O(N²) memory** with N nodes — so you need tricks like "1-hop source attention" (only one block does global attention).
>
> **When to (not yet) use it:** medium-sized graphs, graphs where long paths matter, need SOTA accuracy → pick GTs. Graphs of millions of nodes → message-passing GNNs still scale more easily. These are computational details belonging to Module 07 — in this module you just need to know this **"new-generation" family of embeddings exists**.

---

## 5. Hybrid Search: Vector + Graph

Graph embeddings don't replace text embeddings — they **complement** each other.

### 5.1 Fusion Techniques

<details>
<summary>Python Code — Hybrid Search (RRF + Weighted) (Click to view)</summary>

```python
import numpy as np
from typing import List, Dict

def reciprocal_rank_fusion(
    ranked_lists: List[List[str]],
    k: int = 60,
) -> Dict[str, float]:
    """RRF: merge several ranked lists into one score."""
    scores: Dict[str, float] = {}
    for ranked_list in ranked_lists:
        for rank, doc_id in enumerate(ranked_list):
            scores[doc_id] = scores.get(doc_id, 0) + 1 / (k + rank + 1)
    return scores

def hybrid_search(
    query_text: str,
    query_vector: List[float],
    text_index,       # Vector DB for text embeddings
    graph_embeddings: Dict[str, np.ndarray],
    top_k: int = 10,
    alpha: float = 0.6,  # weight for text search
) -> List[Dict]:
    """
    Hybrid: α * text_score + (1-α) * graph_score
    
    alpha=1.0 → text search only
    alpha=0.0 → graph search only
    alpha=0.6 → balanced (recommended)
    """
    # 1. Text search (semantic)
    text_results = text_index.search(query_vector, top_k=top_k * 2)
    # text_results = [{"id": "doc_1", "score": 0.92}, ...]
    
    # 2. Graph search (structural)
    query_graph_vec = embed(query_text)  # or the query entity embedding
    graph_scores = []
    for node_id, node_vec in graph_embeddings.items():
        sim = float(np.dot(query_graph_vec, node_vec) / 
                    (np.linalg.norm(query_graph_vec) * np.linalg.norm(node_vec)))
        graph_scores.append((node_id, sim))
    graph_scores.sort(key=lambda x: x[1], reverse=True)
    graph_ranked = [node_id for node_id, _ in graph_scores[:top_k * 2]]
    
    # 3a. Fusion by Weighted Score
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

# 3b. Fusion by RRF (no need to tune alpha)
def hybrid_search_rrf(text_ranked: List[str], graph_ranked: List[str], top_k: int = 10):
    fused = reciprocal_rank_fusion([text_ranked, graph_ranked])
    ranked = sorted(fused.items(), key=lambda x: x[1], reverse=True)
    return ranked[:top_k]
```

</details>

### 5.2 When to Use Hybrid?

```
Query type                        │ Best α  │ Strategy
──────────────────────────────────┼─────────┼──────────────────────────
Factoid (find a specific passage) │ 0.8     │ Text-heavy
Multi-hop (connect many entities)  │ 0.3     │ Graph-heavy
Global summary (synthesis)         │ 0.2     │ Graph communities
Hybrid (default)                  │ 0.5-0.6 │ Balanced
```

---

## 6. Hands-On Labs

### Lab 1: Node2Vec from Scratch

1. Create a 100-node graph with `nx.karate_club_graph()` or a synthetic org chart
2. Run `deepwalk_embeddings()` with `num_walks=10, walk_length=20`
3. Visualize the embeddings with t-SNE, observe the clustering

### Lab 2: Compare Node2Vec vs GraphSAGE

1. On the same graph, create embeddings with both methods
2. Measure link prediction accuracy: mask 20% of edges, predict them back
3. Compare accuracy and runtime

### Lab 3: Hybrid Search Benchmark

1. Create 50 queries: 25 factoid + 25 multi-hop
2. Run 3 modes: text-only (α=1.0), graph-only (α=0.0), hybrid (α=0.6)
3. Measure precision@5 for each query type

---

## References

- Grover & Leskovec — *Node2Vec: Scalable Feature Learning for Networks* (KDD 2016)
- Hamilton et al. — *Inductive Representation Learning on Large Graphs (GraphSAGE)* (NeurIPS 2017)
- Veličković et al. — *Graph Attention Networks* (ICLR 2018)
- *Temporal Knowledge Graph Completion: A Survey* — TGN, TuckERTNT, tendency-guided (arXiv 2024–2025)
- *Graph Transformers: A Survey* (arXiv:2502.16533) — GraphGPS, GT
- Bordes et al. — *Translating Embeddings for Modeling Multi-relational Data (TransE)* (NeurIPS 2013)
- Sun et al. — *RotatE: Knowledge Graph Embedding by Relational Rotation* (ICLR 2019)

---

*Next: [05 — GraphRAG](../05-graph-rag/)*
