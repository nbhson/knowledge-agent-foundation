# ❓ FAQ — Graph Storage & Query (Real Stories, Plain Language)

If a question is unclear, read the section in `../README.md` (named in brackets).

---

## Q1. My graph already lives in a 50MB `graph.json` — do I really need a graph database? [→ §1 Choosing a Graph Database]

**What you see**

Extraction gave you 5,000 entities and 12,000 relations. You saved them as one 50MB JSON file. Then a real question arrives: *"find all projects Alice's team worked on, up to 3 hops of `REPORTS_TO`/`MANAGES`."* You hand-write a BFS loop, load the whole file into RAM, and spend about **2 seconds per query**. Ask 100 questions in a session and it times out. The same question in Cypher, a property-graph query language, takes **15ms** — one line instead of a loop.

**Why**

JSON has storage but no indexes and no query engine, so every question re-reads everything. The signal that you have outgrown it is simple: your question is always a chain like `A —[…]→ B —[…]→ C`. That is exactly where a graph DB wins — the Neo4j 2024 benchmark reports **100–1000× faster** than relational JOINs on 3-hop queries, the KuzuDB 2024 paper reports **10× the throughput** of in-memory NetworkX at 10M edges, and LDBC's Social Network Benchmark shows an index on `label + property` cuts lookup latency by **80%**.

**What to do**

1. Write your top 5 real questions down. If most are "who is related to X, and how", move to a graph DB. If they are "what is the budget of project Phoenix", a relational table is fine.
2. Count how many questions you ask per session. One or two a day → keep JSON and cache the answers.
3. Start at the lowest-complexity end: NetworkX for pure prototyping, Kuzu for a real embedded DB with no Docker.
4. Keep `graph.json` anyway as the portable export — the DB is a cache for queries, not the only copy.

```
MATCH (j:Person)-[:REPORTS_TO|MANAGES*1..3]->(s:Person {name:'Alice'})
RETURN j.name, length(path) AS hops   -- 15ms, no BFS loop
```

**Verify**

Ingest the same dataset into NetworkX, Kuzu, and Neo4j, then run the same `MATCH (a)-[*1..3]->(b)` against all three and compare latency (Lab 3). If the graph DB is not measurably faster at your actual data size, stay in JSON.

---

## Q2. Neo4j, Kuzu, FalkorDB, NebulaGraph — which one do I install? [→ §1, §5 Deployment]

**What you see**

You want a decision, not a survey. The practical split that matters:

| Situation | Pick | Scale ceiling | Query lang |
|---|---|---|---|
| Learning / prototyping | Kuzu or NetworkX | ~100K–millions | Cypher / Python |
| Stable production, big ecosystem | Neo4j | billions of nodes | Cypher / GQL |
| Trillions of edges, scale out | NebulaGraph | trillions | nGQL |
| Sub-millisecond answers | FalkorDB / Memgraph | millions, in RAM | Cypher |

**Why**

The deciding variable is not features, it is *your* constraint. Deployment type beats everything: `local + small` → embedded Kuzu, zero ops. `managed` → Neo4j Aura or Amazon Neptune. `realtime` latency → an in-memory engine. NebulaGraph exists because Alibaba and Tencent run it at trillions of edges, which you do not. FalkorDB is a graph DB running directly on Redis, storing the graph as sparse matrices via the GraphBLAS library — traversal becomes matrix multiplication.

**What to do**

1. Prototype with Kuzu: `pip install`, create a `kuzu.Database("./kuzu_db")`, no server. Or skip even that with `networkx`.
2. For development, run Neo4j Community in Docker with the `apoc` and `graph-data-science` plugins so migration later is painless.
3. For production, use a managed tier (Aura, Neptune) so HA and backup are not your problem.
4. Do not switch graph DBs late — Cypher is the portable skill, the storage engine is not.

```yaml
image: neo4j:5-community
ports: ["7474:7474", "7687:7687"]   # Browser UI / Bolt protocol
NEO4J_PLUGINS: '["apoc","graph-data-science"]'
```

**Verify**

`docker exec -it <container> cypher-shell -u neo4j -p password "MATCH (n) RETURN count(n)"` returns a count. Browser opens on `http://localhost:7474`. Healthcheck runs `RETURN 1` every 10s, 5 retries.

---

## Q3. The same query takes 2 seconds on 100K nodes — slow query or missing index? [→ §3 Indexing & Performance]

**What you see**

You write `MATCH (n:Person) WHERE n.name = 'Alice' RETURN n` and it takes 2 seconds. A colleague's equivalent query returns in milliseconds. The three classic culprits show up in real logs: a filter written as `WHERE` on an unindexed property, an unlimited hop pattern `MATCH (a)-[*]->(b)` that explodes combinatorially, or `MATCH (n) RETURN n` that hands back the entire graph to your process.

**Why**

An index is the database's table of contents — without one, the engine must scan every node. And every index has a write cost, since each new node updates it, so people over-index or under-index randomly. The fix depends on the query type, and the type is chosen by the question you ask.

**What to do**

1. Match the index type to the question: exact name/id → range index; fuzzy keyword → full-text index; meaning → vector index (finds nearest neighbours); several properties at once → composite index; no duplicates allowed → unique constraint.
2. Prefer the pattern form `{name: 'Alice'}` over a `WHERE` clause — the engine picks the index for you.
3. Cap variable-length hops (`*1..3`) and add a `LIMIT`.
4. Return only the fields you need, never whole nodes.
5. Confirm with `PROFILE` that the index was actually used before shipping.

```
❌ MATCH (n:Person) WHERE n.name = 'Alice' RETURN n
✅ CREATE INDEX FOR (n:Person) ON (n.name)
✅ MATCH (p:Person {name:'Alice'})-[:WORKS_ON]->(proj) RETURN proj.name
```

**Verify**

Run `PROFILE MATCH (a:Person {name:'Alice'})-[:MANAGES*1..3]->(b:Person) RETURN b` and read the plan: index used, db hits, memory. Lab 2's 10K-node before/after test should show the 80–90% latency drop the benchmark table predicts.

---

## Q4. I ran the ingest script twice and now the graph has duplicate nodes — how do I make loading repeatable? [→ §4 Transactions & Consistency]

**What you see**

First run: 5,000 entities land cleanly. You fix a parser bug, re-run the loader, and now `MATCH (n:Entity {name:'Alice'}) RETURN count(n)` returns 2. Worse, the second pass blew up with a "cannot delete node" style error, because edges still point at it. In a knowledge graph, half-broken entities also poison every later traversal.

**Why**

`CREATE` always makes a new node; `MERGE` (match-or-create) is the idempotent form — re-running finds the existing node and updates it instead. The reader's four ACID properties matter here: **Atomicity** means a batch of 1,000 rows commits fully or rolls back, **Isolation** stops two concurrent loads creating the same node twice, **Durability** means a committed batch survives a crash. Delete order is the other trap: in Cypher, edges must go before nodes unless you use `DETACH DELETE`.

**What to do**

1. Use `MERGE`, never `CREATE`, in every loader path.
2. Wrap rows in `UNWIND` (a loop inside Cypher) and commit in batches — the example defaults to `batch_size=1000`, and `execute_write` handles the transaction per batch.
3. Add a unique constraint on the natural key so the database rejects duplicates at the last line of defence.
4. Prefer soft delete for graph data: `SET n.deleted = true, n.deleted_at = datetime()` instead of removing the node.
5. When you must really delete, use `DETACH DELETE` so attached edges go too.

```
UNWIND $batch AS row
MERGE (n:Entity {name: row.name})
SET n.type = row.type, n.updated_at = datetime()
```

**Verify**

Run the loader three times against the same input; `count(n)` stays at 5,000 and `count(r)` at 12,000. Then run `PROFILE` on a `MERGE` and confirm it reports zero nodes created on the third pass.

---

## Q5. Do I need a separate vector database for GraphRAG, or can the graph DB handle embeddings? [→ §2.3 Full-Text & Vector Search]

**What you see**

Your GraphRAG feature needs two things at once: "find people whose bio mentions Phoenix" and "find people similar to this embedding." The natural instinct is to bolt on a second system — a vector store plus the graph — and then write code that fetches from one, filters with the other, and merges the results in application code.

**Why**

The trend in graph databases is one engine with many index types. **FalkorDB** indexes full-text, vector, and range data on the same node, so a query filters by text + vector + time *inside* the database instead of round-tripping to your app. Neo4j combines full-text and vector indexes since 5.x; Kuzu added vector indexes in v1.5. One system also means one transaction, one backup, one consistency story.

**What to do**

1. Create a full-text index and a vector index on the same label in the same database.
2. Size the vector index to your model: the example uses `dimension: 768` with cosine similarity, matching a 768-dimension embedding.
3. Combine them in one statement — vector search first, then traverse from the hits.
4. Keep the scores in the output and sort, so you can tune the cut-off later.

```cypher
CREATE VECTOR INDEX personEmbedding FOR (n:Person) ON n.embedding
OPTIONS {dimension: 768, similarityFunction: 'cosine'}
CALL db.index.vector.queryNodes("personEmbedding", 10, $queryVector) YIELD node, score
MATCH (node)-[:WORKS_ON]->(p:Project) RETURN node.name, p.name, score
```

**Verify**

The hybrid query returns `person` + `project` + `score` rows ordered by score. Full-text search via `CALL db.index.fulltext.queryNodes("personNameFTS", "Alice")` returns the same node from a second index. On Kuzu, confirm the extension path: `INSTALL vector; LOAD EXTENSION vector;`.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: README.md.*
