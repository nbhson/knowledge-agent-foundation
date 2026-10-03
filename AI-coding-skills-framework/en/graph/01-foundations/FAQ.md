# ❓ FAQ — Graph Foundations (Real Stories, Plain Language)

If a question is unclear, read the section in `../README.md` (named in brackets).

---

## Q1. My graph query is slow and my machine runs out of memory — matrix or list? [→ §3 Graph Representations]

**What you see**

You build the graph the way the textbook draws it: a square table of 0s and 1s, one row and one column per node. Everything works on a tutorial graph of 4 nodes. Then you load the real thing — 100,000 nodes — and the process either takes minutes or dies.

```
cells = 100,000 × 100,000 = 10 billion cells
float64 → ~80 GB just to hold it
```

Almost none of those cells are ever used. A knowledge graph is **sparse**: a person connects to a handful of documents, not to all 99,999 others. The matrix spends memory storing the word "no" 10 billion times.

**Why**

The table above is only worth it when the graph is **dense** — when roughly 30% of the cells or more are actually filled, or when you need real matrix math (PageRank, spectral methods). Stanford CS224W's point in the "3 Pieces of Evidence" table is blunt: choosing the wrong representation is **100× slower** on sparse graphs. The matrix is fast for one single question ("is A connected to B?" = one cell lookup), and terrible for everything else.

**What to do**

1. Start with an **adjacency list** — the default. In NetworkX, `nx.Graph()` *is* an adjacency list, so you get it for free. Memory is O(V + E), meaning "proportional to the number of nodes plus the number of edges".
2. Measure before you switch. Only move when you have a real number in front of you, not because a blog post said so.
3. If you must choose from scratch:

```
<10K nodes, fast traversal   → Adjacency List (NetworkX)
>1M nodes, training GNNs     → CSR (PyG / DGL)
Storage + complex queries    → Property Table (Neo4j / Kuzu)
Dense, ≥30% of cells filled  → Adjacency Matrix + GPU
ETL, export, streaming       → Edge List (parquet / csv)
```

**Verify**

Benchmark both on the same data before you commit — the Lab 2 pattern in the README is enough: `nx.erdos_renyi_graph(10000, 0.001)`, then time `nx.shortest_path` and `nx.degree_centrality`. Check peak memory with `/usr/bin/time -l`. If the list finishes in milliseconds and the matrix needs gigabytes, you have your answer, and a number you can put in a design doc.

---

## Q2. I asked "who reports to whom?" and got a confident wrong answer [→ §2 The Kinds of Graphs]

**What you see**

The query runs, returns rows, no error. But the list is wrong in a way that is hard to spot: Bob shows up as reporting to Alice *and* Alice as reporting to Bob. Or you model a friendship as directed and now "who follows whom" returns only half the pairs, in one arbitrary direction. Nothing crashes — the answer is just quietly incorrect.

**Why**

You stored the edge as **undirected** when the real relationship is **directed**. An undirected edge means "A—B is the same as B—A". A directed edge means "A→B is not the same as B→A". `REPORTS_TO`, `MANAGES`, `BELONGS_TO`, `APPROVES` are all one-way: Alice manages Bob, and that fact says nothing about whether Bob manages Alice.

| Relationship | Type | If you get it wrong |
|---|---|---|
| `REPORTS_TO`, `MANAGES` | Directed | Answer is symmetric nonsense |
| `COLLABORATES_WITH`, `KNOWS` | Undirected | Half your pairs vanish |
| `KNOWS {weight: 0.92}` | Weighted | You cannot rank by confidence |

**What to do**

1. Pick the type from the sentence, not from convenience. "Alice manages Bob" is directed. "Alice collaborates with Bob" is undirected.
2. If an edge has a number on it, store the number: `KNOWS {weight: 0.92}` from extraction is what lets you later say "knows well" versus "barely acquainted".
3. If you have two kinds of entities and only cross-links — users and movies — that is a **bipartite** graph: users never link to users.

```python
G = nx.Graph()                        # ❌ direction discarded
G.add_edge("Alice", "Bob", relation="REPORTS_TO")

G = nx.DiGraph()                      # ✅ A→B ≠ B→A
G.add_edge("Alice", "Bob", relation="REPORTS_TO")
list(G.successors("Alice"))   # ['Bob'] — Alice reports to Bob
list(G.predecessors("Bob"))   # ['Alice']
```

**Verify**

`nx.is_directed(G)` returns `True`. Then test the reverse case on purpose: search for "Bob reports to Alice" and assert you get zero rows. Also count edges before and after the switch — if a reciprocal pair `A—B` and `B—A` collapses into one, your old data was silently losing information. On a codebase graph (`File —DEFINES→ Function —CALLS→ Function`), `G_code.predecessors("validateCard")` must return the caller and not the callee.

---

## Q3. The answer is three years out of date — "Alice still manages Team B" [→ §2 The Kinds of Graphs, Temporal]

**What you see**

Someone asks who manages Team B. Your graph confidently answers Alice. She moved in 2024. The edge is still in your store, nothing marks it as expired, and your system now states a falsehood with total confidence — the worst kind of bug, because there is no error message.

**Why**

You stored the relationship as a plain fact instead of a **temporal** fact. A temporal edge carries a validity period, usually written as a half-open interval: `valid_from` inclusive, `valid_until` exclusive. In the README's own data shape, Alice has two `WORKS_AT` edges — `[2020, 2024)` and `[2024, now)`. Both are true records. Only one is true *today*.

```python
{"from":"Alice","to":"CompanyX","type":"WORKS_AT","valid":"[2020, 2024)"},
{"from":"Alice","to":"CompanyY","type":"WORKS_AT","valid":"[2024, now)"},
# Alice works at exactly one company today, not two
```

**What to do**

1. Add validity to every edge that can change: employment, ownership, reporting lines, project membership. Fixed facts (a person's date of birth) do not need it.
2. Filter on the way in, not at the end. Every traversal asks "is this edge active as of today?"
3. Write the filter once, in one shared place, so no query can forget it.

```python
def is_active(edge, today):
    start, end = edge["valid"]
    return start <= today and (end == "now" or today < end)

live = [e for e in edges if is_active(e, "2026-10-03")]
```

**Verify**

Run yesterday's question against data with a known expiry: the count of active `WORKS_AT` edges per person must equal 1, never 0 and never 2. Add a unit test that inserts an edge ending at `2024` and asserts the query returns nothing for today's date — this is the cheapest regression test in the whole module.

---

## Q4. Neo4j or a triple store? And what exactly does RDF cost me? [→ §5 Property Graph vs RDF Triple Store]

**What you see**

You are choosing a database and the docs describe two incompatible worlds. One stores nodes and edges with properties; the other stores triples `(Subject, Predicate, Object)`. Both claim to be "the graph database". Teams pick one, migrate later, and lose a quarter.

**Why**

They optimise for different goals. A **property graph** gives every node and edge a bag of key-value attributes — `weight: 0.9`, `since: "2024-01-01"`, `confidence: 0.95`. An **RDF triple store** is built around URIs and an **ontology** (a formal schema, e.g. OWL/RDFS) with built-in logical *reasoning*: it can infer that a fact follows from other facts without you writing code.

| Aspect | Property graph | RDF triple store |
|---|---|---|
| Unit | node + edge with properties | triple + URI |
| Query language | Cypher / GQL | SPARQL |
| Properties on edges | native | reification (heavy) |
| Reasoning | you write the code | built in (OWL) |

The Neo4j benchmark in the README's evidence table: property graphs are **3–5× faster** for 2–3 hop traversal, which is the shape of almost every real question.

**What to do**

1. For this framework, use a property graph — Neo4j, Kuzu, or NetworkX. RDF only earns its place with linked open data or when you genuinely need OWL reasoning.
2. Write the edge property, not a side table. In a triple store, an attribute on a relationship needs **reification** — extra triples to describe a triple, and your 2-hop query gets heavy.

```cypher
CREATE (a:Person {name:'Alice', role:'CTO'})
CREATE (p:Project {name:'Phoenix', budget:500000})
CREATE (a)-[:MANAGES {since:'2024-01-01', confidence:0.95}]->(p)
MATCH (person:Person)-[:MANAGES*1..2]->(proj:Project {name:'Phoenix'})
RETURN person.name
```

**Verify**

Time the identical 2–3 hop question in both engines on the same 100k-node dataset and record milliseconds side by side. Then try to filter on an edge attribute (`confidence > 0.9`) in each — in the property graph it is `WHERE e.confidence > 0.9`, in the triple store it is the thing that made you read about reification in the first place.

---

## Q5. Which metric do I actually report — and why does my GNN ignore fraud patterns? [→ §4 Metrics & Graph Characteristics]

**What you see**

Two failures, opposite shapes. First: you report "average degree" in a status update and nobody can tell whether the graph is healthy. Second, worse: your fraud-detection model scores well on random splits and badly in production, because fraudsters connect to *different* kinds of nodes than their neighbours.

**Why**

Metrics are measuring tools, not trophies — pick the one that answers your actual question. And there is a quiet assumption baked into standard GNNs (GCN, GraphSAGE): **homophily**, meaning nearby nodes tend to share a label. It holds for social graphs and breaks on fraud, virus spread, and cyber attack networks, where the whole signal *is* that a node connects across types.

**What to do**

1. Match metric to question: degree centrality for "who is the hub", **betweenness** for the bridge whose removal blocks a team, PageRank for influence without volume, clustering + modularity for splitting 1,000 entities into summarizable topics.
2. Use diameter and average path length to set your traversal budget — that is your `max_hops`.
3. Check homophily before training. If neighbours rarely share labels, use a heterophilous model instead.

```python
G = nx.karate_club_graph()          # 34 nodes — the standard smoke test
nx.average_clustering(G)            # ≈0.57 -> are friends also friends?
nx.diameter(G)                      # 5     -> set max_hops from this
top = sorted(nx.betweenness_centrality(G).items(),
             key=lambda kv: -kv[1])[:3]
```

**Verify**

Sanity-check the arithmetic before you publish: average degree must equal `2E/V` (for the karate club, 78 edges / 34 nodes ≈ 4.6). Run Louvain and print modularity `Q` — a high value means the communities are genuinely separated; that same number is what tunes the Leiden resolution parameter, and Microsoft GraphRAG reports **15% better answer quality** from getting it right. For the GNN, compare neighbour label agreement against a random baseline; no gap means your dataset is heterophilous and the standard model will not help you.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: README.md.*