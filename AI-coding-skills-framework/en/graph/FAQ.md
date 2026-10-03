# ❓ FAQ — Graph Engineering (Real Stories, Plain Language)

If a question is unclear, read the section in `README.md` (named in brackets).

---

## Q1. My chatbot answers simple questions just fine — do I really need a graph? [→ Why Does Graph Engineering Matter?]

**What you see**

You point a retrieval-augmented chatbot (RAG: search documents first, then let the model answer) at a 10,000-page repository — contracts, reports, org charts, emails — and ask: *"Who approved the Phoenix project contract, and what AI-related projects has that person managed before?"*

Vector search returns 5 chunks containing the word "Phoenix". Not one of them contains both the approver and the AI projects in the same passage. The model picks the most plausible-sounding name and states it as fact. You cannot prove where the answer came from.

**Why**

Vector search compares the *wording* of a question to the *wording* of a passage. It has no idea that Nguyen Van A is connected to the Phoenix contract by an `APPROVED_BY` link. Chunking is like tearing a city map into pieces and trying to reassemble it at query time. Multi-hop questions — "who, and what else they own" — are exactly the ones that break.

**What to do**

1. Do not rebuild anything yet. Write 20 real questions your users ask, and mark which ones need two or more relationship steps.
2. If failures cluster on "who approved", "reports to", "what else did they manage", you have a graph case. If they cluster on "what does this paragraph say", keep vector search and save the money.
3. Start with one narrow domain (contracts, or the org chart) — not the whole 10,000 pages. Extract entities and relations into triples.
4. Keep vector search for recall and add graph only for the multi-hop step.

**Verify**

Ask the 20 questions again. Every correct multi-hop answer must come with a printed path, like `Phoenix → APPROVED_BY → Nguyen Van A → MANAGED → Atlas (AI)`. If a path cannot be printed, the answer is a guess.

---

## Q2. Should I replace my vector database with a graph database? [→ Core philosophy]

**What you see**

A team asks the all-or-nothing question: "we run ChromaDB today, so do we rip it out and move to Neo4j?" Half-built migration, three weeks of work, and the multi-hop questions still fail at the end.

**Why**

They are not alternatives. They answer different questions.

| Store | Question it answers |
|---|---|
| Vector database | "Which passage *resembles* the question?" |
| Graph database | "Which entities are *related*, how many hops away, with what evidence?" |

GraphRAG is simply both used together: vector for recall, graph for precision and reasoning. Replacing recall with precision is not a trade — it is a downgrade plus extra work.

The README's analogy is a city map: vector search says "there's a restaurant nearby", a graph says who owns it, what else they own, and the shortest route there. Scale is not the excuse either — this stack already runs in production on Neo4j Aura or self-hosted clusters with billions of nodes.

**What to do**

Keep the vector store. Add a graph beside it, then wire them together — this is the standard 2025–2026 production stack (Neo4j + LangChain):

```python
from langchain_experimental.graph_transformers import LLMGraphTransformer
docs = LLMGraphTransformer().transform_documents(raw_docs)
Neo4jGraph.from_documents(docs)          # writes nodes + relations

# hybrid: vector index on Document nodes
#         traversal on Person / Project nodes
```

Two query paths, chosen by question type: plain similarity for "what does this document say", graph traversal for "who is connected to whom". Only send a Cypher query (Neo4j's query language) to the database for the second kind.

**Verify**

Pick a question whose answer is split across two separate documents. Vector-only search returns the wrong half; the hybrid query returns the joined answer plus the edge that joined them. If that test does not pass, the two stores are not actually connected.

---

## Q3. There are 9 sub-folders here — where do I actually start? [→ Learning Path]

**What you see**

You open the directory, see `01-foundations` through `09-evaluation`, read the first folder, then jump to `07-gnn` because it sounds impressive, and abandon the whole track two days later.

**Why**

Numbered folders invite reading in order. But this track is a set of decision points, not a linear textbook, and the deep-learning folder sits before the storage and evaluation folders on purpose.

**What to do**

Pick your goal first, then read only that row:

| Your real goal | Read |
|---|---|
| turn raw documents into a graph | `02-knowledge-graph/` |
| choose a database, write queries | `03-graph-storage/` |
| ship a working retrieval pipeline | `05-graph-rag/` |
| answer multi-hop questions, find paths | `06-graph-reasoning/` |
| prove the graph is worth the cost | `09-evaluation/` |

The four folders not in the table are triggered by their own moment. Read `01-foundations/` only if "graph" is new vocabulary to you. Read `04-graph-embeddings/` when you want "find similar projects", not "who approved what". Read `07-gnn/` when you must predict a link that nobody wrote down. Read `08-graph-workflow/` the day a document changes and you realise the graph is stale.

If you genuinely want the full sequence, the README's own order is: overview → foundations → knowledge graph → storage → embeddings + GraphRAG → reasoning + GNN → workflow + evaluation. Skip nothing in the first four; those are load-bearing.

**Verify**

Say out loud, in one sentence, which folder answers your current problem. If you cannot, you are not ready to pick a folder — go write down the 20 real questions first.

One warning about the two "advanced" folders. `07-gnn/` and `06-graph-reasoning/` are where people get stuck for weeks, and both are optional on day one. Nothing in `05-graph-rag/` requires them. Leave them until a real question forces the issue — see Q6.

---

## Q4. A new contract arrives every day — do I have to rebuild everything from scratch? [→ Overview, Graph Lifecycle]

**What you see**

The README's warning is blunt: without a graph, you cannot update knowledge without re-embedding everything. Meanwhile the pipeline you built — extract, build, store, embed, query, reason, evaluate — is defined as one long chain, and nobody on the team knows which link is safe to re-run.

**Why**

The lifecycle has seven stages, but they are not all expensive or all irreversible. Extraction and embedding are the slow ones; query, reason and evaluate are read-only and always cheap to repeat. Treating the chain as one unit means a single new PDF triggers a full rebuild.

**What to do**

Separate the stages so only the dirty ones re-run. A new document only invalidates the documents it touched:

```
changed_doc_ids = ["contract_1042"]
1. Extract  → triples only for changed_doc_ids
2. Store    → upsert nodes/edges, tag each with its source doc_id
3. Embed    → re-embed only changed nodes, keep vector ids stable
4. Reason   → no-op (read-only)
```

Tag every node and edge with the document id that produced it. Without that tag, an incremental update cannot know what to overwrite, and you are back to full rebuilds. Microsoft-style extraction also helps: a gleaning loop (ask the model again for entities it missed) pulls out 3–5× more entities than a single pass, so you do it once, correctly, rather than three times.

**What to do, continued**

Use `08-graph-workflow/` — ETL pipelines (extract, transform, load: move raw documents into queryable storage), incremental updates, and versioning. Versioning is what makes rollback possible when an extraction bug poisons a month of triples. The agent loop in this framework should trigger this update automatically when a new document arrives, not wait for a human.

**Verify**

Ingest one new document. Count what changed: only the new entities and edges appear, pre-existing triples are byte-identical, and you can still serve queries from the previous snapshot.

---

## Q5. How do I know the graph is any good, or am I just building an expensive toy? [→ Overview, Evaluation]

**What you see**

Six months in, the graph has 400,000 nodes and nobody can say whether answers improved. Someone proposes measuring it by counting rows. You need a number a manager will accept.

**Why**

A graph database reports storage stats, not quality. What actually matters is coverage (how much of the source text turned into usable triples), connectivity (are related entities actually linked, or are they two lonely islands), hallucination rate, and path precision — whether the returned path is the right one.

**What to do**

Measure four things, then compare against your vector-only baseline on the same question set:

1. **Coverage** — percentage of source documents that produced at least one extracted relation. A low number usually means the extraction prompt is too narrow, not that the documents are empty.
2. **Connectivity** — how many entities have more than one edge. Isolated nodes are the signature of a deduplication failure (see `02-knowledge-graph/`).
3. **Hallucination rate** — answers with no supporting path. Target the 25–30% reduction reported for hybrid vector + graph retrieval on a 10K-document enterprise benchmark.
4. **Path precision** — of the paths returned, how many survive human checking.

Use a real public benchmark instead of inventing one: HotpotQA or 2WikiMultihopQA for multi-hop questions, FB15k-237 or WN18RR for link prediction, OGB for graph learning tasks.

**Verify**

Report a before/after table: same 20 questions, vector-only versus hybrid, with multi-hop accuracy and hallucination rate on both sides. If the two columns are identical, the graph is not earning its keep — find out why before adding more data.

---

## Q6. Do I need to train a neural network before I can use a graph? [→ Learning Path]

**What you see**

A team reads about Graph Neural Networks (GNNs: neural networks that learn from a graph's structure) and concludes they need PyTorch, a GPU, and three months before they can answer "who reports to whom". Meanwhile a single query solves it today.

**Why**

GNNs solve two specific problems: predicting a *missing* edge, and classifying a node. They are not needed to *traverse* edges you already have. A large share of real questions are traversal — "who approved this", "what does this person manage" — and traversal is a plain database query, not a learning problem.

**What to do**

Climb only as far as you need:

1. **Level 0 — traversal.** Cypher queries, shortest path, pattern matching. Handles "who approved this", "what does this person manage".
2. **Level 1 — rules.** Explicit inference over the graph: if `A REPORTED_TO B` and `B REPORTED_TO C`, then `A` is two hops from `C`. See `06-graph-reasoning/` for inference rules and temporal reasoning (ignoring edges that expired).
3. **Level 2 — embeddings.** Node2Vec or GraphSAGE turn a node's neighbours into a vector, useful for "find similar projects" — see `04-graph-embeddings/`.
4. **Level 3 — GNN.** Only now, and only for link prediction on benchmarks like FB15k-237. Frameworks: PyG or DGL.

**Verify**

Answer a week of real questions using only Levels 0 and 1. If almost everything resolves, stop — you do not need Level 3, and shipping it adds a model to train, serve, and explain.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: README.md.*