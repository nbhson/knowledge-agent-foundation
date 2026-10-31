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

**Rule-based reasoning** (module 06) works with hand-written rules — but it gets hard to keep up when you have hundreds of relation types. **GNNs** learn the patterns straight from the shape of the graph: no hand-written rules, just examples to learn from.

> *"Rules tell the graph what you know. GNNs discover what you don't know you know."*

> **One-line summary:** GNNs learn patterns directly from graph structure, replacing hundreds of hand-written rules with learned message passing.

### Why Are GNNs Important?

> *"A GNN is deep learning for relational-structured data — the way a CNN is deep learning for images."*

How to read this table: each row is one published result. **#** = row number, **Source** = who published it, **Finding** = the measured effect. For instance, row 1 says adding graph structure beats reading node features alone by 15–25% accuracy.

| # | Source | Finding |
|---|-------|-----------|
| 1 | **OGB Benchmark (2024)** | GNNs boost **accuracy by 15-25%** on node classification vs an MLP using node features alone |
| 2 | **Knowledge Graph Completion (FB15k-237)** | R-GCN + a scoring function reaches **MRR 0.35** vs TransE's 0.29 |
| 3 | **Anthropic (2025)** | GNN-based link prediction suggests **missing relations** with 72% precision on an enterprise KG |

(MLP = a plain neural network reading only each node's own features; MRR = Mean Reciprocal Rank — how high the correct answer ranks on average; precision = of the suggestions made, how many were right.)

> **One-line summary:** Benchmarks show GNNs beat feature-only models by 15–25% and predict missing relations well — that is why graphs matter.

---

## Overview

This diagram shows how a GNN flows: node features go in, message-passing layers mix neighbor information, and the output embeddings feed prediction tasks.

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

> **One-line summary:** Features + graph go through message-passing layers; the resulting embeddings power classification, link prediction, and KG completion.

---

## Contents

How to read this table: each row is one section of this file. **#** = order, **Topic** = the clickable title, **Description** = what you will learn. For instance, row 2 covers the GCN model in detail.

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

(PyG = PyTorch Geometric, the standard Python library for building GNNs.)

> **One-line summary:** The module goes from intuition, through the three core models, to limits, heterogeneous variants, and working PyTorch code.

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
>
> **One-line summary:** A GNN reads not just each node's features but also its connections — like a CNN reading pixel neighborhoods, but for graph nodes.

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

> **One-line summary:** Message passing = every node collects neighbor messages, combines them, and merges the result with its own vector — K layers reach K hops away.

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

> **One-line summary:** An MLP sees nodes in isolation; a GNN sees connections, so people in the same group end up with similar embeddings even if their raw features differ.

---

## 2. GCN — Graph Convolutional Network

This section covers GCN, the baseline GNN: what its formula does and when its plain averaging is enough.

### 2.1 The GCN Formula (Kipf & Welling, 2017)

> **📌 Understand before reading the formula:**
> **GCN = a node takes a *weighted average* of its neighbors + itself, then passes through a fully-connected layer + ReLU.**
> *Weighted average* = each node contributes in inverse proportion to its number of neighbors (so a highly-connected node doesn't "drown out" a sparsely-connected one).
>
> **Analogies:**
> - **GCN = a group discussion**: each person = a node. Each layer = one group meeting: everyone shares opinions (message), then everyone consolidates into a new opinion (update). Listening to many friends → broader knowing.
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

> **One-line summary:** GCN = weighted average of yourself + neighbors, passed through a learned filter — simple and effective, but blind to neighbor importance.

<details>
<summary>Python Code — GCN Layer From Scratch (Click to view)</summary>

> 📄 **Example code:** [`examples/01-2-1-the-gcn-formula-kipf-welling-2017.py`](examples/01-2-1-the-gcn-formula-kipf-welling-2017.py)

</details>

### 2.2 2-Layer GCN for Node Classification

<details>
<summary>Python Code — 2-Layer GCN (Click to view)</summary>

> 📄 **Example code:** [`examples/02-2-2-2-layer-gcn-for-node-classification.py`](examples/02-2-2-2-layer-gcn-for-node-classification.py)

</details>

> **One-line summary:** Two GCN layers are the standard recipe for node classification — enough reach (2 hops) without over-smoothing.

---

## 3. GraphSAGE & GAT

This section covers the two upgrades over GCN: GraphSAGE (works on new nodes) and GAT (weights neighbors by importance).

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

> **One-line summary:** GraphSAGE learns a reusable "combine the friends" formula, so new nodes get embeddings on arrival — no retraining.

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

> **One-line summary:** GAT scores each neighbor's importance, turns scores into weights, and combines neighbors weighted — with several attention "heads" for stability.

<details>
<summary>Python Code — GAT with PyG (Click to view)</summary>

> 📄 **Example code:** [`examples/03-3-2-gat-attention.py`](examples/03-3-2-gat-attention.py)

</details>

### 3.3 Comparison

How to read it: each row compares the three models on one property. For instance, "Inductive?" asks whether the model can embed a node it never saw during training.

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

(O(N²) = memory grows with the square of node count — the dense-matrix trap; O(E) = grows with edge count instead.)

> **One-line summary:** GCN for small fixed graphs, GraphSAGE for scale and new nodes, GAT when neighbor importance matters — pick by your bottleneck.

---

## 4. Link Prediction & Node Classification

This section covers the two most common GNN tasks: predicting missing edges and labeling nodes.

### 4.1 Link Prediction — "What will Alice WORKS_ON?"

<details>
<summary>Python Code — Link Prediction (Click to view)</summary>

> 📄 **Example code:** [`examples/04-4-1-link-prediction-what-will-alice-works.py`](examples/04-4-1-link-prediction-what-will-alice-works.py)

</details>

> **One-line summary:** Link prediction scores candidate pairs (Alice, ?, X) from their embeddings, so missing edges surface as high scores.

### 4.2 Node Classification — "Which team is this person on?"

**What this does:** train the GNN on a few labeled nodes, then predict labels for the rest.

> 📄 **Example code:** [`examples/05-4-2-node-classification-which-team-is-this.py`](examples/05-4-2-node-classification-which-team-is-this.py)

> **One-line summary:** With labels on only a few nodes, the GNN propagates team information through the graph to classify everyone else.

---

## 5. GNN for Knowledge Graph Completion

This section covers predicting missing triples in a knowledge graph: relation-aware GNNs plus scoring functions.

### 5.1 R-GCN — Relational GCN

For a heterogeneous KG with many relation types, R-GCN has **separate weights for each relation**:

```
h_v^{(l+1)} = σ( Σ_{r∈R} Σ_{u∈N_r(v)} (1/c_{v,r}) W_r^{(l)} h_u^{(l)} + W_0^{(l)} h_v^{(l)} )

  R = set of relations (MANAGES, WORKS_ON, ...)
  W_r = dedicated weights for relation r
  c_{v,r} = normalization (number of neighbors via relation r)
  W_0 = self-loop weights
```

(The formula in words: each relation type r has its own weight matrix W_r, neighbors are aggregated per relation, and the node's own vector is added back via W_0.)

> **One-line summary:** R-GCN gives every relation type its own weights, so a MANAGES edge and a WORKS_ON edge carry different information.

> 📄 **Example code:** [`examples/06-5-1-r-gcn-relational-gcn.py`](examples/06-5-1-r-gcn-relational-gcn.py)

### 5.2 Scoring Functions for KG Completion

**What this covers:** after R-GCN produces embeddings, a scoring function decides which (head, relation, tail) triples are plausible.

Once you have embeddings from R-GCN, use a scoring function to predict missing triples:

How to read it: each row is one scoring method. **Method** = its name, **Score(h, r, t)** = the formula for triple (head, relation, tail), **Best For** = the relation kinds it handles. For instance, DistMult handles symmetric relations ("married to") but not asymmetric ones ("manages").

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

> **One-line summary:** Score triples with a function matched to your relations — TransE for speed, ComplEx/RotatE when relations are asymmetric or composable.

---

## 6. GNN Limits & Ways Past Them

This section covers the two known failure modes of deep GNNs and the standard fixes for each.

> **📌 Core Concept:**
> GNN message passing is powerful, but **going too deep breaks it**. These are the 2 "diseases" most cited in the research, and you need to know them so you don't pick GNN for the wrong problem.

### 6.1 Over-Smoothing (When Nodes Become... Alike)

> **Over-smoothing** = after many GCN layers, **all nodes' features converge toward the same value** — node A and node Z (totally unrelated) end up with the same vector, and the model can't tell anyone from anyone. Node classification falls apart badly.
>
> **Analogies:** like the game **"telephone"**: after many rounds the message is increasingly far from the original — information from far away gets "diluted".
>
> **One-line summary:** Over-smoothing = too many averaging layers make every node's vector converge to the same thing, erasing all distinctions.

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
>
> **One-line summary:** Over-squashing strangles long-range information through bottlenecks, and plain GNNs can't even distinguish some different graphs — the fixes are residuals, rewiring, or just staying shallow.

### 6.3 Graph Transformers — Getting Past Over-Smoothing

> **Graph Transformers (GraphGPS, GT)** use **self-attention over the whole graph**: a node can "look at" any other node directly in a single computation pass — **not through a chain of hops**, so no over-smoothing/over-squashing. They excel on data where **long-range paths matter**, on graphs with complex local structure.
>
> **The price:** the attention matrix is O(N²) memory for N nodes → hard to scale to million-node graphs. The hybrid solution (GraphGPS): message-passing keeps local context + just one global attention block.
>
> **One-line summary:** Graph Transformers give every node direct sight of every other node — no smoothing or squashing — but the O(N²) memory cost limits them to smaller graphs.

---

## 7. Heterogeneous & Temporal GNN

This section covers graphs with many node/edge types, and graphs that change over time — both need special GNN variants.

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
>
> **One-line summary:** Real KGs have many node/edge types (use R-GCN, HAN, or HGT) and keep changing (use TGN) — flattening or freezing them throws away signal.

> 📄 **Example code:** [`examples/07-7-heterogeneous-temporal-gnn.py`](examples/07-7-heterogeneous-temporal-gnn.py)

---

## 8. Implementation with PyG

This section points to the complete PyTorch Geometric training pipeline — data, model, loss, and evaluation in one file.

<details>
<summary>Python Code — Complete Training Pipeline (Click to view)</summary>

> 📄 **Example code:** [`examples/08-8-implementation-with-pyg.py`](examples/08-8-implementation-with-pyg.py)

</details>

> **One-line summary:** The end-to-end PyG pipeline shows the full training loop — encode, sample negatives, score, and evaluate.

---

## 9. Hands-On Labs

These labs are the practice drills for the module — each one proves (or disproves) a claim from the sections above.

### Lab 1: Node Classification on Karate Club

1. Load `nx.karate_club_graph()`, create features (degree, one-hot, or random)
2. Train a 2-layer GCN, measure accuracy with 4 labeled nodes (semi-supervised)
3. Compare against MLP (no graph) — GNN must win

> **One-line summary:** The minimal sanity check: on 4 labeled nodes, the GNN must beat an MLP, or the graph adds nothing.

### Lab 2: Link Prediction

1. Mask 20% of the edges of a 100-node graph
2. Train a link predictor (§4.1), measure AUC on the masked edges
3. Try different negative sampling ratios (1:1 vs 1:5)

(negative sampling = inventing fake pairs the model should reject, to teach it what "not linked" looks like; AUC = a 0-to-1 score for the classifier, 0.5 = guessing.)

> **One-line summary:** Hide edges, predict them back, and tune the fake-pair ratio — AUC on hidden edges is the honest score.

### Lab 3: Mini KG Completion

1. Build a small KG: 20 entities, 3 relations, 50 triples
2. Train R-GCN + DistMult scoring
3. Ask: `(Alice, WORKS_ON, ?)` → rank all entities, check the rank of the correct answer

> **One-line summary:** Train R-GCN + a scoring function on a toy KG and check where the true answer ranks — the ranking position is your quality metric.

---

## References

> **One-line summary:** The founding papers (GCN, GraphSAGE, GAT, R-GCN) plus surveys on limits and the PyG docs — all linked for deeper reading.

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

## GraphRAG — 2026 Update

Microsoft GraphRAG (2024-2025): uses knowledge graphs to enhance RAG. Complex (multi-hop) queries outperform vector-only RAG.

**New 2025-2026 developments:**
- **LazyGraphRAG** (Microsoft, late 2024): defers LLM summarisation to query time — indexing cost equal to vector RAG, quality equal to full GraphRAG, ~700× lower query cost. Integrated into Microsoft Discovery (2025) and Azure Local.
- **LightRAG** (HKUDS, EMNLP 2025): dual-layer graph + vector, incremental update instead of full re-index.
- **GraphRAG-Bench** (Microsoft, 06/2025): multi-hop + global queries GraphRAG wins; single-hop factoid vanilla RAG wins.
- **Gartner (2026)**: GraphRAG in "Top Trends in D&A for 2026" for complex cases where high-accuracy RAG falls short.
- **Knowledge Graph Market**: $1.48B (2025) → $2.04B (2026). GraphRAG shifting from "enterprise luxury" → production baseline.

Ref: https://microsoft.github.io/graphrag/

> **One-line summary:** The GNN ecosystem keeps growing alongside GraphRAG — watch the market and benchmark numbers before choosing heavy machinery.

---

*Next: [08 — Graph Workflow](../08-graph-workflow/)*
