# ❓ FAQ — GNN / Graph Neural Networks (Real Stories, Plain Language)

If a question is unclear, read the section in `../README.md` (named in brackets).

---

## Q1. My hand-written rules already work — do I really need a GNN? [→ Why Are GNNs Important / §1]

**What you see**

You built a rule engine (module 06) and it answers `(Alice, WORKS_ON, ?)` just fine. Then the graph grows to hundreds of relation types and every new pair needs another hand-written `if`. The benchmarks are not subtle about the payoff: on the OGB benchmark a GNN beats an MLP — a network that reads each node's features and nothing else — by **15–25% accuracy** on node classification. On FB15k-237, R-GCN plus a scoring function reaches **MRR 0.35** where TransE gets 0.29. MRR is the average reciprocal rank of the correct answer, so 0.35 means the right entity usually lands in the top 3.

**Why**

Rules encode what you already know. A GNN learns from the shape of the graph instead. Alice and Carol have never met and there is no edge between them, but both `WORKS_ON` Phoenix — after 2 message-passing layers their embeddings land close together, with no rule written for that case.

**What to do**

1. Train the feature-only MLP first as a baseline. If a GNN cannot beat it, you have no graph signal to exploit and you should keep the rules.
2. Only need embeddings for nodes that appear at inference time? Use GraphSAGE (inductive). If the graph is fixed, plain GCN is fine.
3. Hundreds of relation types? Hand-written rules do not scale — R-GCN gives each relation its own weight matrix instead.

```
# Lab 1 baseline: GNN must beat the MLP, or there is nothing to gain
gcn_acc = train_and_eval(GCN(...))   # 2 layers, only 4 labeled nodes
mlp_acc = train_and_eval(MLP(...))   # node features only, no edges
assert gcn_acc > mlp_acc, "graph is not paying for itself"
```

**Verify**

Run Lab 1 on `nx.karate_club_graph()` with 4 labeled nodes and compare against the MLP. If the gap is inside the noise, say so honestly — your graph is not adding information beyond node features.

---

## Q2. I stacked more layers and accuracy got WORSE — what did I break? [→ §6.1 / §6.2]

**What you see**

A 2-layer GCN gets 82% on Karate Club. You go to 4 layers: 76%. You go to 10: every node ends up with nearly the same vector and node classification collapses onto the majority class. Two different diseases produce that, and they are not the same problem.

**Why**

**Over-smoothing** is convergence: after many rounds of averaging, all embeddings drift toward the same value, so node A and node Z become indistinguishable — like the telephone game. **Over-squashing** is a bottleneck: a densely connected region blocks the path, so two nodes 20 hops apart still cannot exchange information through 10 layers. Separately, standard message passing is **no stronger than the WL test** (Weisfeiler-Lehman, 1968) — some structurally different graphs get identical embeddings no matter how deep you go.

**What to do**

1. Most of the time, just stop at 2–3 layers. The README's own advice: a 2-layer GraphSAGE beats a 10-layer one in practice.
2. Add residual connections (skip a layer instead of averaging it away) and normalization after each layer.
3. Genuinely need long-range reasoning? Add rewiring — extra short edges between distant nodes — or move to Graph Transformers, where attention reaches any node in one pass instead of through a chain of hops.

```
layers = 2                        # start here, not 8
conv = SAGEConv(in_c, hid_c)
conv.residual = True              # skip a layer instead of averaging it away
x = conv(x, edge_index).relu()
```

**Verify**

Sweep depth 1 → 10 at a fixed seed and plot accuracy: it should peak early and then decline. If accuracy only ever improves, you are probably leaking test edges into the encoder — see Q5.

---

## Q3. GCN ran out of memory on my real graph (40GB RAM) — which variant now? [→ §3.3]

**What you see**

The from-scratch `GCNLayer` takes `adj` as a `(N, N)` tensor and computes `agg = adj @ x`. At N = 100,000 that is 10^10 floats — roughly 40GB before a single weight is allocated. And every time a new person joins the company, you retrain from scratch.

**Why**

GCN is **transductive**: it needs the full adjacency up front and averages every neighbor uniformly. GraphSAGE instead *learns the aggregator function*, so a new node is embedded immediately by running that formula on its own neighbors. GAT adds learned attention weights on top of the edge-based cost.

| | GCN | GraphSAGE | GAT |
|---|---|---|---|
| New nodes | needs retrain | embed on arrival | embed on arrival |
| Cost | O(N²) dense | O(E) + sampling | O(E × heads) |
| Neighbor weights | none (uniform) | none | yes |

**What to do**

1. Move to GraphSAGE with neighbor sampling and use `edge_index` — an `(2, E)` list of node pairs — never a dense `(N, N)` matrix.
2. Reach for GAT only when neighbor importance genuinely differs. With `heads=4` and `hid_c=16`, layer 1 outputs 16 × 4 = 64 features, so layer 2's input must be 64.
3. Whole-graph attention costs O(N²) memory, which is why GraphGPS keeps local message passing and adds only one global attention block.

```
from torch_geometric.nn import SAGEConv
conv1 = SAGEConv(in_c, hid_c, num_neighbors=[10, 10])  # sample 10 per hop
conv2 = SAGEConv(hid_c, out_c, num_neighbors=[10, 10])
# edge_index shape (2, E) — never build a (N, N) matrix
```

**Verify**

Peak memory must stay roughly flat as N grows 10×. Then confirm a brand-new node gets an embedding **without retraining** — that is the entire point of the inductive variant.

---

## Q4. Should I throw away my relation types and treat every edge the same? [→ §5.1 / §5.2 / §7]

**What you see**

Your graph has `Person --WORKS_ON--> Project`, `Person --REPORTS_TO--> Person`, `Project --HAS_BUDGET--> Number`. You flatten them into one edge list for GCN. Now `REPORTS_TO` and `WORKS_ON` get averaged into the same bucket, and the model cannot tell a manager edge from a project edge.

**Why**

GCN and GraphSAGE assume a single node type and a single edge type. Homogeneous treatment throws away relation semantics — which, in a knowledge graph, is most of the signal you have.

**What to do**

1. Keep an `edge_type` tensor beside `edge_index` and use R-GCN: one weight matrix per relation type.
2. Pick the scoring function to fit the relation. TransE is simple and fast but weak on asymmetry; ComplEx handles symmetric *and* asymmetric relations; RotatE fits composition and inversion. DistMult works for symmetric relations only.
3. Need embeddings that cross types? HAN aggregates along **meta-paths** (e.g. `P--WORKS_ON--Project--HAS_BUDGET--Budget`) then attends between the meta-paths; HGT is the stronger modern choice. The graph changes over time → TGN processes an event stream per timestamp instead of a static snapshot.

```
edge_type = torch.tensor([0, 1, 0, 1])   # 0=MANAGES, 1=WORKS_ON
from torch_geometric.nn import RGCNConv
conv = RGCNConv(in_dim, hidden_dim, num_relations=len(relation_names))
h = conv(x, edge_index, edge_type)
```

**Verify**

Train R-GCN + DistMult on the mini KG (20 entities, 3 relations, 50 triples), then ask `(Alice, WORKS_ON, ?)` and check the rank of the correct entity. Compare against the flattened homogeneous version — if MRR does not improve, your relation types are carrying no signal and the extra machinery is not worth it.

---

## Q5. Loss printed 0.0000 but every predicted link is wrong — where is the leak? [→ §4.1 / §8]

**What you see**

The link-prediction loop reports `Epoch 150: loss=0.0000`, and then every candidate pair for Alice comes out at `prob=0.500`. Node classification shows the same shape: 100% train accuracy, chance-level test accuracy.

**Why**

Leakage, not overfitting. In the pipeline the encoder sees the full `edge_index` and the positive training edges *are that same* `edge_index` — the graph already contains the answer, so the model learns to copy it. Easy negatives make it worse: a random pair like (Project, Person) is trivially non-existent, so the loss falls while the embeddings stay useless.

**What to do**

1. Hold out edges *before* training, and build the encoder's graph from training edges only. `train_test_split_edges` is imported in the README pipeline but sits commented out.
2. Sample hard negatives — same node type, genuinely plausible — not random mismatches.
3. For node classification use a label mask (`-1` = unlabeled), not a random row split, and reweight imbalanced classes: 100 people in team A vs 10 in team B → `class_weights = [1.0, 10.0]`.

```
data = train_test_split_edges(data)               # hold out ~20% of edges
z = model.encode(data.x, data.train_edge_index)   # encoder never sees test edges
neg = negative_sampling(data.train_edge_index, num_neg_samples=100)
```

**Verify**

Measure AUC on the masked edges (Lab 2 hides 20% of edges of a 100-node graph) and sweep the negative ratio 1:1 vs 1:5. If train AUC is 1.0 while test AUC is 0.5, you have leakage — not a capacity problem.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: README.md.*