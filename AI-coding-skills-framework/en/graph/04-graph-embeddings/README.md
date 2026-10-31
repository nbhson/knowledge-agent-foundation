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

- **Graph traversal**: find the person with the same number of neighbors? That is not quite enough — Alice manages 5 people, Bob also manages 5 people, but they work with completely different teams.
- **Text embedding**: embed Alice's `description` and compare? You ignore the whole graph structure.
- **Graph embedding**: each node becomes a vector **based on its position in the graph** → `cosine(alice_vec, bob_vec)` is high if they have similar roles/structures. (cosine similarity = a score for "how much do these two vectors point the same way", from 0 to 1; 1 = identical direction.)

**Graph Embeddings turn the shape of the graph into vectors — so you can use fast search while still keeping the relationship info.**

> **One-line summary:** This section shows why walking the graph or reading text alone is not enough — graph embeddings turn graph position into vectors, so "who is similar to Alice" becomes a fast vector lookup.

### Why Do Graph Embeddings Matter?

> *"The graph tells you WHO is connected. Embeddings tell you WHO IS SIMILAR without being directly connected."*

How to read this table: each row is one published study. **#** = row number, **Source** = who published the finding, **Finding** = the measured result in plain words. For instance, row 1 says adding graph embeddings cut link-prediction errors noticeably.

| # | Source | Finding |
|---|-------|-----------|
| 1 | **Node2Vec Paper (2016)** | Graph embeddings improve **link prediction accuracy by 22%** compared to using only node features |
| 2 | **Microsoft GraphRAG (2024)** | Combining text embeddings + graph embeddings boosts **retrieval precision by 18%** |
| 3 | **OGB Benchmark (2024)** | GraphSAGE embeddings + ANN search are **50× faster** than pure traversal for k-NN queries on 1M nodes |

(link prediction = guessing a missing edge, e.g. "Alice will join project X"; OGB = Open Graph Benchmark, a public test set for graph models; ANN = Approximate Nearest Neighbor, fast "find the closest vectors" search; k-NN = "find the k closest items".)

> **One-line summary:** Published benchmarks agree: graph embeddings make prediction more accurate and similarity search much faster on large graphs.

---

## Overview

This diagram shows the big picture: one knowledge graph feeds two kinds of embeddings, and you can mix them.

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

(The last line: the final score blends the text score and the graph score, with α = a mixing weight between 0 and 1 that you pick — α = 0.5 gives them equal say. Vector DB = a database built for nearest-vector search.)

> **One-line summary:** Text embeddings capture what a node says; graph embeddings capture where it sits; hybrid search blends both scores.

---

## Contents

How to read this table: each row is one section of this file. **#** = order, **Topic** = the clickable section title, **Description** = what that section teaches you. For instance, row 2 covers random-walk methods like Node2Vec.

| # | Topic | Description |
|---|--------|-------|
| 1 | [What Are Graph Embeddings?](#1-what-are-graph-embeddings) | Definition, intuition, classification |
| 2 | [Node2Vec/DeepWalk](#2-shallow-embeddings-node2vec-deepwalk) | Random walk embeddings |
| 3 | [GNN Embeddings](#3-gnn-based-embeddings-graphsage-gat) | GraphSAGE, GAT |
| 4 | [KG Embeddings](#4-knowledge-graph-embeddings-transe-rotate) | TransE, RotatE for KG completion, TKGE, Graph Transformers |
| 5 | [Hybrid Search](#5-hybrid-search-vector--graph) | Combining vector + graph (RRF, weighted) |

> **One-line summary:** The file moves from the definition, through four families of methods, to hybrid search that combines them.

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

> **One-line summary:** A graph embedding is a list of numbers per node, arranged so "close in the graph" or "same role" means "close in the vector space".

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

> **One-line summary:** The goal is a function that maps each node to a vector; it is harder than text embedding because it must encode structure, not just content.

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

How to read it: each row is one method family. **Type** = the method name, **Needs Training?** = what data you train it on (Unsupervised = no labels; Supervised = needs labeled examples; KG triples = needs (node, relation, node) facts), **Best For** = the task it fits. For instance, Node2Vec needs no labels and suits clustering.

> **One-line summary:** There are four method families — random-walk, GNN-based, KG-specific, and hybrid — and the right one depends on your task and training data.

---

## 2. Shallow Embeddings: Node2Vec, DeepWalk

This section explains the "random walk" family: what it is, how it works, and when to pick it.

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

> **One-line summary:** DeepWalk treats random walks as sentences and nodes as words, then lets Word2Vec place frequently co-occurring nodes close together.

### 2.2 Node2Vec — Biased Random Walks (added control)

> **What's new compared to DeepWalk:** adds two parameters `p` and `q` to **control the direction** of the walk — instead of walking purely at random, you decide whether to "go far" or "stay close".

> 📄 **Example code:** [`examples/01-2-2-node2vec-biased-random-walks-added-control.py`](examples/01-2-2-node2vec-biased-random-walks-added-control.py)

<details>
<summary>Python Code — Node2Vec with NetworkX (Click to view)</summary>

> 📄 **Example code:** [`examples/02-2-2-node2vec-biased-random-walks-added-control.py`](examples/02-2-2-node2vec-biased-random-walks-added-control.py)

</details>

> **One-line summary:** Node2Vec is DeepWalk plus two knobs (p, q) that bias walks toward breadth-first or depth-first behavior, giving you control over what "similar" means.

### 2.3 When to Use Node2Vec?

How to read this table: each row is one situation you might be in. **Situation** = your case, **Use it?** = ✅ yes or ❌ no, **Reason** = why. For instance, row 2 says: if your graph keeps growing with new nodes, skip Node2Vec.

| Situation | Use it? | Reason |
|-----------|-------|-------|
| Small-medium graph (<100K nodes) | ✅ | Fast, no GPU needed, unsupervised |
| Need inductive (new nodes) | ❌ | Must retrain everything — use GraphSAGE instead |
| Need edge features / node features | ❌ | Node2Vec only uses structure — use GNNs |
| Clustering / community detection | ✅ | Embeddings reflect community structure well |

(inductive = works on nodes it never saw during training; the opposite, transductive = only works on the exact nodes it was trained on.)

> **One-line summary:** Use Node2Vec for small, fixed graphs and clustering; switch to a GNN when you have new nodes or node/edge features.

---

## 3. GNN-Based Embeddings: GraphSAGE, GAT

This section covers the GNN family: models that compute embeddings from neighbors with a learned function, so new nodes need no retraining.

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

> **One-line summary:** GraphSAGE learns one "combine your friends' information" function, so any node — even a brand-new one — gets an embedding by just running that function.

(hop = one step along an edge; "2 hops away" = a friend of a friend.)

> 📄 **Example code:** [`examples/03-3-1-graphsage-inductive-node-embeddings.py`](examples/03-3-1-graphsage-inductive-node-embeddings.py)

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

> **One-line summary:** GAT upgrades the plain average into learned weights, so each node decides which of its neighbors should count more.

<details>
<summary>Python Code — GraphSAGE with PyG (Click to view)</summary>

> 📄 **Example code:** [`examples/04-3-2-gat-graph-attention-networks.py`](examples/04-3-2-gat-graph-attention-networks.py)

</details>

### 3.3 Comparison

How to read it: each row compares the three methods on one property. For instance, "Inductive?" asks whether the method can embed a node it never saw in training.

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

(O(E) = work grows with the number of edges E, not the number of node pairs — that is why it scales. O(walks × len) = work grows with how many walks you run and how long each is.)

> **One-line summary:** Node2Vec suits small fixed graphs and clustering; GraphSAGE handles new nodes; GAT adds learned neighbor importance at a small extra cost.

---

## 4. Knowledge Graph Embeddings: TransE, RotatE

This section covers embeddings that learn nodes AND relations together, built to predict missing links in a knowledge graph.

> **📌 Core Concept:**
> **KG Embedding** differs from Node2Vec/GNN in that it learns **nodes AND relations together** — the goal is **link prediction**: predicting missing relations.
>
> **Analogies:**
> - **TransE = translation**: `vec(Alice) + vec(WORKS_ON) ≈ vec(Phoenix)`. Like navigation: "from Alice, follow the WORKS_ON direction and you arrive at Phoenix". If another project fits this direction → you can predict it.
> - **RotatE = rotation**: a relation is an "angle" — rotate Alice's vector by that angle to get Phoenix's vector. Makes sense for symmetric relations like "married" (rotate 180°).

KG embeddings learn **both nodes and relations** together — to do **link prediction**: `(Alice, WORKS_ON, ?)` → predict which project.

> **One-line summary:** Unlike the earlier methods, KG embeddings give relations their own vectors, so you can score and predict missing triples like (Alice, WORKS_ON, ?).

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

> **One-line summary:** TransE treats each relation as a direction: head vector + relation vector should land on the tail vector, so wrong triples score badly.

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

> **One-line summary:** RotatE treats relations as rotations in complex space, which lets it model symmetric and reversible relations that TransE cannot.

<details>
<summary>Python Code — TransE Training Loop (Click to view)</summary>

> 📄 **Example code:** [`examples/05-4-2-rotate-rotation-in-complex-space.py`](examples/05-4-2-rotate-rotation-in-complex-space.py)

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

> **One-line summary:** TKGE adds a timestamp to every triple, so you can ask "was this still true at date X?" — only worth it if your questions depend on time.

### 4.4 Graph Transformers (GTs) — The Next Generation

> **📌 Core Concept:**
> **Graph Transformers** = applying the **self-attention mechanism (like in LLMs)** to graphs: each node "pays attention" to the whole graph instead of only its direct neighbors. This direction addresses the inherent limits of GNN message-passing (see "limitations" in detail in Module 07).
>
> **An easy-to-picture question:** GNN = a person who only asks **their direct neighbors** (1–3 rounds). Graph Transformer = a person who can **scan all the relationships** in the graph at once to decide who matters most.
>
> **The typical branch (GraphGPS, GT)** combines whole-graph attention + message passing: it keeps local chains but adds a "long view". The price: **O(N²) memory** with N nodes — so you need tricks like "1-hop source attention" (only one block does global attention).
>
> **When to (not yet) use it:** medium-sized graphs, graphs where long paths matter, need SOTA accuracy → pick GTs. Graphs of millions of nodes → message-passing GNNs still scale more easily. These are computational details belonging to Module 07 — in this module you just need to know this **"new-generation" family of embeddings exists**.

> **One-line summary:** Graph Transformers let every node look at every other node at once — more accurate on long-range patterns, but memory-hungry on big graphs.

---

## 5. Hybrid Search: Vector + Graph

This section explains how to combine text-embedding scores and graph-embedding scores into one ranking.

Graph embeddings don't replace text embeddings — they **complement** each other.

### 5.1 Fusion Techniques

<details>
<summary>Python Code — Hybrid Search (RRF + Weighted) (Click to view)</summary>

> 📄 **Example code:** [`examples/06-5-1-fusion-techniques.py`](examples/06-5-1-fusion-techniques.py)

</details>

> **One-line summary:** Fusion means merging two ranked lists (text-based and graph-based) into one — either by a weighted average of scores or by RRF, which rewards items that rank well in both lists.

(RRF = Reciprocal Rank Fusion — a formula that merges ranked lists using only positions, not raw scores.)

### 5.2 When to Use Hybrid?

How to read it: each row is a type of question. **Query type** = what the user asks, **Best α** = the weight to give the text score (α = 1 means text only, α = 0 means graph only), **Strategy** = the plain-language description. For instance, "find this exact passage" → rely mostly on text (α = 0.8).

```
Query type                        │ Best α  │ Strategy
──────────────────────────────────┼─────────┼──────────────────────────
Factoid (find a specific passage) │ 0.8     │ Text-heavy
Multi-hop (connect many entities)  │ 0.3     │ Graph-heavy
Global summary (synthesis)         │ 0.2     │ Graph communities
Hybrid (default)                  │ 0.5-0.6 │ Balanced
```

> **One-line summary:** Pick the text/graph mix by question type: exact facts lean on text, multi-hop and summary questions lean on the graph.

---

## 6. Hands-On Labs

These labs let you practice the methods above on small graphs, so the ideas become concrete.

### Lab 1: Node2Vec from Scratch

1. Create a 100-node graph with `nx.karate_club_graph()` or a synthetic org chart
2. Run `deepwalk_embeddings()` with `num_walks=10, walk_length=20`
3. Visualize the embeddings with t-SNE, observe the clustering

(t-SNE = a plotting technique that squeezes high-dimensional vectors onto a 2D chart so you can see clusters.)

> **One-line summary:** Build a small graph, run random walks, and see the clusters appear when you plot the vectors.

### Lab 2: Compare Node2Vec vs GraphSAGE

1. On the same graph, create embeddings with both methods
2. Measure link prediction accuracy: mask 20% of edges, predict them back
3. Compare accuracy and runtime

> **One-line summary:** On the same graph, check whether the GNN's extra power beats Node2Vec's simplicity — measure, don't assume.

### Lab 3: Hybrid Search Benchmark

1. Create 50 queries: 25 factoid + 25 multi-hop
2. Run 3 modes: text-only (α=1.0), graph-only (α=0.0), hybrid (α=0.6)
3. Measure precision@5 for each query type

(precision@5 = of the top 5 results returned, how many are actually correct.)

> **One-line summary:** Benchmark text-only, graph-only, and hybrid search on two question types to see where the blend actually wins.

---

## References

> **One-line summary:** The original papers behind every method in this module — start with Node2Vec (2016) and GraphSAGE (2017) if you read only two.

- Grover & Leskovec — *Node2Vec: Scalable Feature Learning for Networks* (KDD 2016)
- Hamilton et al. — *Inductive Representation Learning on Large Graphs (GraphSAGE)* (NeurIPS 2017)
- Veličković et al. — *Graph Attention Networks* (ICLR 2018)
- *Temporal Knowledge Graph Completion: A Survey* — TGN, TuckERTNT, tendency-guided (arXiv 2024–2025)
- *Graph Transformers: A Survey* (arXiv:2502.16533) — GraphGPS, GT
- Bordes et al. — *Translating Embeddings for Modeling Multi-relational Data (TransE)* (NeurIPS 2013)
- Sun et al. — *RotatE: Knowledge Graph Embedding by Relational Rotation* (ICLR 2019)

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

> **One-line summary:** The graph-RAG field is moving fast toward cheaper, incremental indexing — and graph embeddings are part of that retrieval stack.

---

*Next: [05 — GraphRAG](../05-graph-rag/)*
