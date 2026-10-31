# ❓ FAQ — Graph Embeddings (Real Stories, Plain Language)

If a question is unclear, read the section in `../README.md` (named in brackets).

*Graph embeddings = turning each node (person, project, document) into a list of numbers, so "similar nodes" becomes "nearby numbers" that a computer can compare.* Each answer follows the same shape: **What you see** (the symptom), **Why** (the root cause), **What to do** (the fix), and **Verify** (how to check the fix worked).

---

## Q1. "Find the person most similar to Alice" returns people from the wrong team — how do I tune the walk? [→ §2.2 Node2Vec]

This answer shows why a similarity search drifts to look-alikes from the wrong team, and which two knobs fix it.

**What you see**

You ask for the node most similar to Alice in role and relationships. Your search returns three people who also manage five reports — but from unrelated teams. Nothing is technically broken: every cosine score is 0.91 or higher, so the ranking looks confident. ("Cosine score" = a similarity number: 1 means identical, 0 means unrelated. High only means *structurally* similar, not *semantically* right.)

**Why**

DeepWalk learns only "who keeps showing up next to whom". It runs purely random walks — a "walk" is one path that hops node → neighbour → neighbour with no preference. It cannot tell *same team* apart from *same job title*: both look like "people near Alice". Node2Vec (Grover & Leskovec, KDD 2016) adds exactly two knobs, `p` and `q`, that steer each hop: stay close to home or run far. Leave both at 1.0 and you get DeepWalk's behaviour plus tuning you never use.

**What to do**

How to read the table: each row is one setting of a knob, the effect it has on the walk, and what that walk tends to find. For instance, `q=0.5` makes the walk run far, so it matches people with the same **role** even on other teams.

| Knob | Value | Walk behaviour | Finds |
|---|---|---|---|
| `q` | 0.5 (DFS-like) | goes far | same **role**, other team |
| `q` | 2.0 (BFS-like) | stays close | same **team** |
| `p` | 0.5 | returns often | tight neighborhood |
| `p` | 2.0 | rarely returns | long-range structure |

("DFS-like" = depth-first, dives deep; "BFS-like" = breadth-first, explores the immediate surroundings first.)

> 📄 **Example code:** [`examples/01-q1-find-the-person-most-similar-to-alice.py`](examples/01-q1-find-the-person-most-similar-to-alice.py)

Then look at `most_similar("node_0", embeddings, top_k=5)` — "top_k=5" = return the 5 closest nodes — and check the top 5 by eye. Only reach for graph embeddings at all if traversal (walking the graph with queries) and text search both fail: Node2Vec reportedly improves link-prediction accuracy by 22% over node features alone, but it only looks at structure. If your nodes have attributes (age, department, description), Node2Vec ignores them.

**Verify**

Run the same graph at `q=0.5` and `q=2.0` and compare the results. Then Lab 2: mask 20% of edges (hide them), predict them back, and compare accuracy. If `q` does not move the number, your graph has one dense community and the knob has nothing to bite on.

> **One-line summary:** Random walks see only "who is near whom", so tune `p`/`q` to control whether similarity means *same role* or *same team* — and verify by eye plus a link-prediction test.

---

## Q2. A new node joins the graph and it has no vector — do I have to retrain everything? [→ §3.1 GraphSAGE]

This answer explains why one new node breaks `model.wv[node]`, and the model family that fixes it without retraining.

**What you see**

A new employee shows up in your graph. `model.wv[node]` raises a `KeyError` ("no such key in the table"), and the vector database returns nothing for their ID. The tempting fix is retraining — but retraining rewrites every node's vector, so your whole vector index becomes stale and you re-embed the entire corpus, not one row. ("Embed" = compute the number vector for a node.)

**Why**

Node2Vec and DeepWalk are **transductive**: "transductive" = the model memorises one fixed vector per node, stored 1-to-1 like a dictionary entry. There is no function that computes a vector — only a table that remembers one. A node absent from the table at training time can never get a value.

**What to do**

Switch to GraphSAGE (Hamilton et al., NeurIPS 2017). It learns **one aggregation function** instead of one vector per node: look at a node's neighbours, combine their vectors, and the result *is* the vector. ("Aggregate" = merge neighbour vectors, e.g. by averaging.) A node that did not exist yesterday just gets the function run on it.

> 📄 **Example code:** [`examples/02-q2-a-new-node-joins-the-graph-and.py`](examples/02-q2-a-new-node-joins-the-graph-and.py)

Pick `K` layers deliberately: K layers means K hops of information. ("Layer" = one round of neighbour aggregation; 2 layers = neighbours-of-neighbours.) Two layers on an org chart covers direct reports and skip-level; ten layers just smears everything into one average. Because existing vectors keep their values, adding a node becomes an *incremental* index write — one new row — instead of a full rebuild.

**Verify**

Add one synthetic node with two edges, run one forward pass (one run of the aggregation function), and confirm cosine similarity to its teammates is high. Then confirm the vector database gained one row and no other row's ID or vector changed.

> **One-line summary:** Node2Vec memorises a fixed vector per node, so new nodes have none — GraphSAGE learns a function over neighbours instead, letting you embed new nodes without retraining.

---

## Q3. GraphSAGE counts my CEO and a conference contact as equal — should I use GAT? [→ §3.2 GAT]

This answer shows why averaging all neighbours equally can be wrong, and when attention (per-neighbour weights) is worth its cost.

**What you see**

GraphSAGE's `mean` aggregator treats every neighbour identically. ("Aggregator" = the step that merges neighbour vectors into one; `mean` = plain average.) In an org chart, Alice's direct report and a person she met once at a conference both contribute 50%. A supplier node ends up parked halfway between "vendor" and "employee", so a classification query about vendors returns employees.

**Why**

GraphSAGE's aggregation is a uniform mean: the layer has no per-neighbour weight. GAT (Veličković et al., ICLR 2018) learns an attention weight per edge instead — "attention weight" = a learned importance score saying which neighbours matter more. It normalises them with `softmax` so they sum to 1 across neighbours ("softmax" = squash numbers into percentages that add up to 100%).

How to read the table: it compares how much each neighbour influences Alice's vector under the two models.

| Neighbour of Alice | GraphSAGE (mean) | GAT (attention) |
|---|---|---|
| Bob, direct report | 50% | 83% |
| Dave, casual contact | 50% | 17% |

**What to do**

> 📄 **Example code:** [`examples/03-q3-graphsage-counts-my-ceo-and-a-conference.py`](examples/03-q3-graphsage-counts-my-ceo-and-a-conference.py)

Cost: GraphSAGE is `O(E)` per layer, GAT is `O(E)` plus attention — same order, real overhead. ("O(E)" = work grows with the number of edges.) If your graph has no meaningful "who matters more", keep the mean. If you need the model to look past neighbours entirely, Graph Transformers apply attention over the whole graph — every node can look at every node — but they cost `O(N²)` memory, which is quadratic in node count: fine for medium graphs, wrong for millions of nodes.

**Verify**

Run Lab 2 on the same graph with both models and compare link-prediction accuracy against runtime. Check that attention weights sum to 1 per node, and inspect one node's weights by hand: if they land near uniform (roughly equal), attention bought you nothing and the mean is enough.

> **One-line summary:** A mean aggregator makes every neighbour count equally — GAT learns per-neighbour weights, but only switch if your edges genuinely differ in importance.

---

## Q4. My link predictor is confidently wrong — stale facts and backwards "married_to" [→ §4.1–4.3 TransE, RotatE, TKGE]

This answer covers two failure modes of knowledge-graph embeddings: facts that expired, and relations that only work in one direction.

**What you see**

`(Alice, WORKS_ON, ?)` returns Phoenix with the lowest score. It was right in 2023; in 2026 Alice works on Project Helios. ("Triple" = a fact written as head → relation → tail, e.g. `Alice → WORKS_ON → Phoenix`.) Separately, the model scores `(B, married_to, A)` worse than `(A, married_to, B)` even though both are the same fact — the relation should be symmetric (work the same in both directions).

**Why**

TransE scores a triple with one translation: `h + r ≈ t`, measured as `||h + r − t||`, lower is better. In words: head vector + relation vector should land on the tail vector, and the score is the miss distance. Two gaps follow from that formula. It has no time coordinate, so a learned triple is true forever. And translation cannot express symmetry — `A + r = B` simply does not imply `B + r = A`.

**What to do**

1. **Symmetric or composable relations → RotatE.** A relation becomes a rotation angle in complex space with `|r_i| = 1` — "rotation" = the relation spins the head vector by an angle instead of shifting it. `married_to` becomes a 180° turn, which works the same forwards and backwards, and `part_of` composes: `(A, part_of, B)` + `(B, part_of, C)` → `(A, part_of, C)` (relations chain like "Vietnam → part of Asia", "Asia → part of Earth").
2. **Facts that expire → add time, but only then.** A triple becomes `(h, r, t, time)`: `(Alice, WORKS_ON, Phoenix, 2023)` is true, `(…, later than 2025)` is not. Families to try: time-parameterized translation (TuckERTNT splits the tensor by time), temporal message passing (TGN), tendency-guided models that predict the direction of change before you query.
3. **If your graph has no time column, skip all of it.** Extra temporal machinery ("temporal" = time-aware) on a timeless graph is cost with no return.

> 📄 **Example code:** [`examples/04-q4-my-link-predictor-is-confidently-wrong-stale.py`](examples/04-q4-my-link-predictor-is-confidently-wrong-stale.py)

**Verify**

Hold out 20% of triples (hide them from training) and report hit@10 — "hit@10" = the correct answer appears in the top 10 predictions — not training loss. Then re-score a triple past its end date: the correct answer's score must rise. For a symmetric relation, confirm both directions score identically after switching to RotatE.

> **One-line summary:** TransE treats every fact as true forever and one-directional — use RotatE for symmetric relations and time-aware models (TKGE) only when your triples actually carry dates.

---

## Q5. Text search alone gets 41% precision on multi-hop questions — how do I mix in graph scores? [→ §5 Hybrid Search]

This answer explains how to combine text-retrieval scores with graph scores without the two scales fighting each other.

**What you see**

Your text-only retrieval nails factoid questions (precision@5 around 0.78) and flops on multi-hop ones (0.41). "Factoid" = a single-fact question; "multi-hop" = a question whose answer needs a chain of facts, A → B → C; "precision@5" = of the top 5 results, how many are actually relevant. Someone asks "why did the auth refactor touch the billing service?" and the top 5 passages contain each half of the chain but never the link between them.

**Why**

Text embeddings encode content — what a document says; graph embeddings encode position in the structure — who connects to whom. Microsoft GraphRAG (2024) reports that combining the two lifts retrieval precision by 18%, and the OGB benchmark (2024) puts GraphSAGE embeddings plus ANN search ("ANN" = approximate nearest neighbour, a fast way to find closest vectors) at 50× faster than pure traversal for k-NN queries over 1M nodes. The practical trap is fusing two scores that do not share a scale — a cosine similarity (−1 to 1) and a raw text score (0 upward) cannot simply be added, like adding metres to kilograms.

**What to do**

Use weighted fusion, `α · text_score + (1 − α) · graph_score` — "α" (alpha) = a 0-to-1 dial setting how much text vs graph counts — and pull `top_k * 2` candidates from each side before merging, so the merge has room to work.

How to read the table: for each question type, it gives the α value (higher α = trust text more) and the resulting strategy.

| Query type | α | Strategy |
|---|---|---|
| Factoid | 0.8 | text-heavy |
| Multi-hop | 0.3 | graph-heavy |
| Global summary | 0.2 | graph communities |
| Default | 0.5–0.6 | balanced |

If tuning α per query type is not worth the maintenance, use RRF (Reciprocal Rank Fusion): "RRF" = merge result lists by their *rank positions* only, never their raw scores, so scale differences disappear. The `k = 60` damping constant stops the top of one list from steamrolling the other.

> 📄 **Example code:** [`examples/05-q5-text-search-alone-gets-41-precision-on.py`](examples/05-q5-text-search-alone-gets-41-precision-on.py)

**Verify**

Run Lab 3: 50 queries (25 factoid, 25 multi-hop), three modes — text-only `α=1.0`, graph-only `α=0.0`, hybrid `α=0.6` — and record precision@5 per query type. Report the two types separately; one averaged number hides exactly the regression you are trying to fix.

> **One-line summary:** Text embeddings capture *content*, graph embeddings capture *structure* — fuse them with a weighted α or rank-based RRF, because their raw scores live on different scales.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: README.md.*
