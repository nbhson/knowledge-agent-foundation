# ❓ FAQ — Graph Embeddings (Real Stories, Plain Language)

If a question is unclear, read the section in `../README.md` (named in brackets).

---

## Q1. "Find the person most similar to Alice" returns people from the wrong team — how do I tune the walk? [→ §2.2 Node2Vec]

**What you see**

You ask for the node most similar to Alice in role and relationships. Your search returns three people who also manage five reports — but from completely unrelated teams, on the other continent. Nothing is technically wrong: every cosine score is 0.91 or higher, so the ranking looks confident.

**Why**

DeepWalk walks purely at random, so it only learns "who keeps showing up next to whom". It has no way to say *same team* versus *same job title*. Node2Vec (Grover & Leskovec, KDD 2016) adds exactly two knobs, `p` and `q`, that decide whether a walk stays local or runs far. Leave both at 1.0 and you get DeepWalk's behaviour plus extra tuning you never use.

**What to do**

| Knob | Value | Walk behaviour | Finds |
|---|---|---|---|
| `q` | 0.5 (DFS-like) | goes far | same **role**, other team |
| `q` | 2.0 (BFS-like) | stays close | same **team** |
| `p` | 0.5 | returns often | tight neighborhood |
| `p` | 2.0 | rarely returns | long-range structure |

```python
model = Node2Vec(G, dimensions=64, walk_length=20, num_walks=10,
                 p=0.5, q=2.0)   # q=2.0 -> BFS-like -> "same team"
```

Then look at `most_similar("node_0", embeddings, top_k=5)` and check the top 5 by eye. Only reach for graph embeddings at all if traversal and text search both fail: Node2Vec reportedly improves link-prediction accuracy by 22% over node features alone, but it only looks at structure — if you have node or edge attributes, it ignores them.

**Verify**

Run the same graph at `q=0.5` and `q=2.0`. Then Lab 2: mask 20% of edges, predict them back, and compare accuracy. If `q` does not move the number, your graph has one dense community and the knob has nothing to bite on.

---

## Q2. A new node joins the graph and it has no vector — do I have to retrain everything? [→ §3.1 GraphSAGE]

**What you see**

A new employee shows up in your graph. `model.wv[node]` raises a `KeyError`, and the vector database returns nothing for their ID. The tempting fix is retraining — but that rewrites every node's vector, so your whole vector index is now stale and you re-embed the entire corpus, not one row.

**Why**

Node2Vec and DeepWalk are **transductive**: each node owns one dedicated vector, stored 1-to-1 like a dictionary entry. There is no function that computes a vector — only a table that remembers one. A node absent from the table at training time can never get a value.

**What to do**

Switch to GraphSAGE (Hamilton et al., NeurIPS 2017). It learns **one aggregation function** instead of one vector per node: look at a node's neighbours, combine them, and you have the vector. A node that did not exist yesterday just gets the function run on it.

```python
def graphsage_layer(x, adjacency, weights, aggregator="mean"):
    neighbor_agg = adjacency @ x / adjacency.sum(axis=1, keepdims=True)  # mean of friends
    combined = np.concatenate([x, neighbor_agg], axis=1)  # "me" + "my friends"
    output = np.maximum(0, combined @ weights)             # one ReLU layer
    return output / np.linalg.norm(output, axis=1, keepdims=True)
```

Pick `K` layers deliberately: K layers means K hops of information. Two layers on an org chart covers direct reports and skip-level; ten layers just smears everything into one average. Because existing vectors keep their values, adding a node becomes an *incremental* index write instead of a full rebuild.

**Verify**

Add one synthetic node with two edges, run one forward pass, and confirm cosine similarity to its teammates is high. Then confirm the vector database gained one row and no other row's ID or vector changed.

---

## Q3. GraphSAGE counts my CEO and a conference contact as equal — should I use GAT? [→ §3.2 GAT]

**What you see**

The `mean` aggregator treats every neighbour identically. In an org chart, Alice's direct report and a person she met once at a conference both contribute 50%. A supplier node ends up parked halfway between "vendor" and "employee", so a classification query about vendors returns employees.

**Why**

GraphSAGE's aggregation is a uniform mean: the layer has no per-neighbour weight. GAT (Veličković et al., ICLR 2018) learns an attention weight per edge instead, and normalises them with `softmax` so they sum to 1 across neighbours.

| Neighbour of Alice | GraphSAGE (mean) | GAT (attention) |
|---|---|---|
| Bob, direct report | 50% | 83% |
| Dave, casual contact | 50% | 17% |

**What to do**

```python
e_vu  = LeakyReLU(a @ (W h_v + W h_u))   # "how much do I trust u"
alpha = softmax(e_vu)                    # sums to 1 over neighbours
h_v   = sigmoid(sum(alpha * W h_u))
```

Cost: GraphSAGE is `O(E)` per layer, GAT is `O(E)` plus attention — same order, real overhead. If your graph has no meaningful "who matters more", keep the mean. If you need the model to look past neighbours entirely, Graph Transformers apply attention over the whole graph, but they cost `O(N²)` memory — fine for medium graphs, wrong for millions of nodes.

**Verify**

Run Lab 2 on the same graph with both models and compare link-prediction accuracy against runtime. Check that attention weights sum to 1 per node, and inspect one node's weights by hand: if they land near uniform, attention bought you nothing and the mean is enough.

---

## Q4. My link predictor is confidently wrong — stale facts and backwards "married_to" [→ §4.1–4.3 TransE, RotatE, TKGE]

**What you see**

`(Alice, WORKS_ON, ?)` returns Phoenix with the lowest score. It was right in 2023; in 2026 Alice works on Project Helios. Separately, the model scores `(B, married_to, A)` worse than `(A, married_to, B)` even though both are the same fact.

**Why**

TransE scores a triple with one translation: `h + r ≈ t`, measured as `||h + r − t||`, lower is better. Two gaps follow from that formula. It has no time coordinate, so a learned triple is true forever. And translation cannot express symmetry — `A + r = B` simply does not imply `B + r = A`.

**What to do**

1. **Symmetric or composable relations → RotatE.** A relation becomes a rotation angle in complex space with `|r_i| = 1`. `married_to` becomes a 180° turn, and `part_of` composes: `(A, part_of, B)` + `(B, part_of, C)` → `(A, part_of, C)`.
2. **Facts that expire → add time, but only then.** A triple becomes `(h, r, t, time)`: `(Alice, WORKS_ON, Phoenix, 2023)` is true, `(…, later than 2025)` is not. Families to try: time-parameterized translation (TuckERTNT splits the tensor by time), temporal message passing (TGN), tendency-guided models that predict the direction of change before you query.
3. **If your graph has no time column, skip all of it.** Extra temporal machinery on a timeless graph is cost with no return.

```python
score = torch.norm(h_e + r_e - t_e, p=1, dim=1)          # TransE, lower = better
loss  = torch.relu(pos_score - neg_score + margin).mean()  # margin = 1.0
```

**Verify**

Hold out 20% of triples and report hit@10, not training loss. Then re-score a triple past its end date — the correct answer's score must rise. For a symmetric relation, confirm both directions score identically after switching to RotatE.

---

## Q5. Text search alone gets 41% precision on multi-hop questions — how do I mix in graph scores? [→ §5 Hybrid Search]

**What you see**

Your text-only retrieval nails factoid questions (precision@5 around 0.78) and flops on multi-hop ones (0.41). Someone asks "why did the auth refactor touch the billing service?" and the top 5 passages contain each half of the chain but never the link between them.

**Why**

Text embeddings encode content; graph embeddings encode position in the structure. Microsoft GraphRAG (2024) reports that combining the two lifts retrieval precision by 18%, and the OGB benchmark (2024) puts GraphSAGE embeddings plus ANN search at 50× faster than pure traversal for k-NN queries over 1M nodes. The practical trap is fusing two scores that do not share a scale — a cosine similarity (−1 to 1) and a raw text score (0 upward) cannot simply be added.

**What to do**

Use weighted fusion, `α · text_score + (1 − α) · graph_score`, and pull `top_k * 2` candidates from each side before merging.

| Query type | α | Strategy |
|---|---|---|
| Factoid | 0.8 | text-heavy |
| Multi-hop | 0.3 | graph-heavy |
| Global summary | 0.2 | graph communities |
| Default | 0.5–0.6 | balanced |

If tuning α per query type is not worth the maintenance, use RRF (Reciprocal Rank Fusion): it reads only ranks, never raw scores, so scale differences disappear. The `k = 60` damping constant stops the top of one list from steamrolling the other.

```python
hybrid[doc] = alpha * text_score.get(doc, 0) + (1 - alpha) * graph_score.get(doc, 0)
fused[doc]  = sum(1 / (60 + rank + 1) for lst in ranked_lists for rank, doc in enumerate(lst))
```

**Verify**

Run Lab 3: 50 queries (25 factoid, 25 multi-hop), three modes — text-only `α=1.0`, graph-only `α=0.0`, hybrid `α=0.6` — and record precision@5 per query type. Report the two types separately; one averaged number hides exactly the regression you are trying to fix.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: README.md.*
