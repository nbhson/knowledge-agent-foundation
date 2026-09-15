# 💾 03. Graph Storage & Query — Storing and Querying the Graph

> ## 📑 Table of Contents
>
> - [Opening Story](#opening-story)
> - [Why Storage & Query Matter?](#why-storage--query-matter)
> - [Overview](#overview)
> - [Contents](#contents)
> - [1. Choosing a Graph Database](#1-choosing-a-graph-database)
> - [2. Cypher & GQL — The Query Language](#2-cypher--gql--the-query-language)
> - [3. Indexing & Performance](#3-indexing--performance)
> - [4. Transactions & Consistency](#4-transactions--consistency)
> - [5. Deployment with Neo4j & Kuzu](#5-deployment-with-neo4j--kuzu)
> - [6. Hands-On Labs](#6-hands-on-labs)
> - [References](#references)

---

### Opening Story

You have extracted 5,000 entities and 12,000 relations. You store them in `graph.json` — a 50MB JSON file.

The next week, you need to answer: *"Find all projects that Alice's team has worked on, up to 3 steps of REPORTS_TO/MANAGES."*

With JSON, you write a manual BFS loop, load the entire file into RAM, and run 2 seconds per query. 100 queries? Timeout.

A **Graph Database** solves this: **native storage + indexes + query engine** — answers the same question in 15ms with a single line of Cypher.

### Why Storage & Query Matter?

> *"Without the right DB, a graph is just an expensive JSON file. Without a query language, a graph is just a drawing."*

| # | Source | Finding |
|---|-------|-----------|
| 1 | **Neo4j Benchmark (2024)** | Native graph storage is **100–1000× faster** than relational JOINs for 3-hop queries |
| 2 | **KuzuDB Paper (2024)** | An embedded graph DB (Kuzu) achieves **10× the throughput** of in-memory NetworkX on 10M edges |
| 3 | **LDBC SNB Benchmark** | Indexes on `label + property` cut latency by **80%** for lookup queries |

---

## Overview

```
Knowledge Graph (from 02)
    │
    ▼
┌──────────────────────┐
│  CHOOSE DATABASE     │  ← Neo4j, Kuzu, NebulaGraph, FalkorDB, NetworkX
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│  SCHEMA & INDEXING   │  ← Create constraints, indexes
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│  INGEST & TRANSACTIONS│ ← Batch insert, ACID, upsert
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│  QUERY (Cypher/GQL)  │  ← Traversal, aggregation, path finding
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│  OBSERVABILITY       │  ← Query log, slow queries, metrics
└──────────────────────┘
```

---

## Contents

| # | Topic | Description |
|---|--------|-------|
| 1 | [Choosing a DB](#1-choosing-a-graph-database) | Comparing 6 DBs, decision matrix |
| 2 | [Cypher & GQL](#2-cypher--gql--the-query-language) | CRUD, traversal, aggregation, full-text |
| 3 | [Indexing](#3-indexing--performance) | Index types, query optimization |
| 4 | [Transactions](#4-transactions--consistency) | ACID, batch ingest, idempotency |
| 5 | [Deployment](#5-deployment-with-neo4j--kuzu) | Docker, Python client, sample code |

---

## 1. Choosing a Graph Database

> **📌 When do you need a graph DB?** When your question is **"which entities are related to this one / how are they related?"** (multi-hop traversal) — SQL has to JOIN repeatedly and gets very slow; a graph DB walks the edges directly. **Sign you need a graph DB:** your queries always have the pattern `A —[...]→ B —[...]→ C` (2+ hops).
>
> **Quick Q&A to choose:**
> - Learning / prototyping? → **Kuzu / NetworkX** (no Docker needed)
> - Need stable production, big ecosystem? → **Neo4j** (Community → Aura when scaling)
> - Trillions of edges? → **NebulaGraph** (scale-out)
> - Need sub-millisecond responses? → **FalkorDB / Memgraph** (in-memory)

### 1.1 Detailed Comparison

```
┌────────────────┬──────────┬──────────┬──────────┬────────────────────────────┐
│ Database       │ Type     │ Scale    │ Query    │ Best For                   │
├────────────────┼──────────┼──────────┼──────────┼────────────────────────────┤
│ Neo4j          │ Property │ Billions │ Cypher   │ Production, large ecosystem│
│ (Community/Ent)│ Graph    │ nodes    │ GQL      │ Full-text, GDS, Aura cloud │
│ NebulaGraph    │ Distrib. │ Trillions│ nGQL     │ Trillions of edges, scale-out │
│                │ Property │ edges    │          │ Alibaba, Tencent scale     │
│ FalkorDB       │ Redis    │ Millions │ Cypher   │ Low-latency, Redis stack   │
│ Kuzu           │ Embedded │ Millions │ Cypher   │ Local, Python-native, <1s  │
│ NetworkX       │ Library  │ 100K     │ Python   │ Prototyping, algorithms    │
│ Amazon Neptune │ Managed  │ Billions │ Gremlin/ │ AWS managed, SPARQL+PG     │
│                │ PG + RDF │          │ SPARQL   │                            │
│ Memgraph       │ In-memory│ Millions │ Cypher   │ Real-time, streaming       │
└────────────────┴──────────┴──────────┴──────────┴────────────────────────────┘
```

### 1.2 Decision Matrix

```python
def choose_graph_db(requirements: dict) -> str:
    """
    Choose a DB based on requirements.
    
    requirements = {
        "scale": "small" | "medium" | "large" | "trillion",
        "deployment": "local" | "self-hosted" | "managed",
        "latency": "realtime" | "interactive" | "batch",
        "team_size": int,
    }
    """
    if requirements["scale"] == "small" and requirements["deployment"] == "local":
        return "Kuzu (embedded, zero-ops) or NetworkX (prototyping)"
    
    if requirements["scale"] in ["large", "trillion"]:
        return "NebulaGraph or Neo4j Enterprise Cluster"
    
    if requirements["latency"] == "realtime":
        return "FalkorDB or Memgraph (in-memory)"
    
    if requirements["deployment"] == "managed":
        return "Neo4j Aura or Amazon Neptune"
    
    # Default: production balanced
    return "Neo4j Community (self-hosted) — recommended for most projects"
```

**Recommendation for this Framework:**

| Stage | DB | Reason |
|-----------|----|-------|
| **Learning & Prototyping** | Kuzu or NetworkX | Zero setup, `pip install`, runs locally |
| **Development** | Neo4j Community (Docker) | Standard Cypher, GDS library, easy migration to Aura |
| **Production** | Neo4j Aura / NebulaGraph | Managed, HA, backup |

> **📌 Bonus Concept: FalkorDB & Hybrid Indexing**
>
> **FalkorDB** = a graph database that runs **directly on Redis** (formerly "RedisGraph"). It stores the graph as **sparse matrices** (using the GraphBLAS sparse-matrix library) — essentially "computing traversal with matrix multiplication", extremely fast for data held in RAM. Queries use Cypher, with **sub-millisecond** responses even at millions of nodes.
>
> **"Hybrid indexing in a single engine"**: FalkorDB indexes **multiple data types on the same node** — full-text (find "names containing 'Phoenix'"), vector search (find "entities similar to this embedding"), and range indexes (filter by number). That means a GraphRAG query can filter by text + vector + time **right inside the DB**, without pulling results back to the application layer. Neo4j also combines full-text + vector indexes since 5.x; Kuzu added vector indexes in v1.5 — the general trend is **one engine, many index types**.

---

## 2. Cypher & GQL — The Query Language

> **�📌 Core Concept:**
> **Cypher** = a graph query language (like SQL for relational DBs). A Cypher statement **"draws"** the pattern you want to find — it reads quite intuitively:
>
> ```
> MATCH (a:Person)-[:MANAGES]->(b:Person)  ← "draw": Person a —MANAGES→ Person b
> WHERE a.name = 'Alice'                   ← "filter": Alice only
> RETURN b.name                            ← "take out": the employees' names
> ```
>
> **Symbol syntax:**
> - `(n)` = node, `(n:Label)` = node with a label, `(n:Label {prop: 'val'})` = node with a property
> - `--` = undirected, `-->`/`<--` = directed, `-[:TYPE]->` = typed edge
> - `*1..3` = 1 to 3 hops (traversal)
>
> **Analogy:** SQL = questions about a spreadsheet (you have to know the columns in advance). Cypher = describing a picture of the relationship (draw the pattern, the DB finds the match itself).

### 2.1 Basic CRUD

### 2.1 Basic CRUD

<details>
<summary>Cypher Code — CRUD (Click to view)</summary>

```cypher
// ============ CREATE ============

// Create nodes
CREATE (a:Person {name: 'Alice', role: 'CTO', age: 35})
CREATE (b:Person {name: 'Bob', role: 'Engineer'})
CREATE (p:Project {name: 'Phoenix', budget: 500000})

// Create edges
MATCH (a:Person {name: 'Alice'}), (b:Person {name: 'Bob'})
CREATE (a)-[:MANAGES {since: '2024-01-01'}]->(b)

MATCH (b:Person {name: 'Bob'}), (p:Project {name: 'Phoenix'})
CREATE (b)-[:WORKS_ON {role: 'Lead', allocation: 0.8}]->(p)

// ============ READ ============

// Find all Persons
MATCH (n:Person) RETURN n.name, n.role

// Find with a filter
MATCH (p:Project) WHERE p.budget > 300000 RETURN p

// ============ UPDATE ============

// Update a property
MATCH (p:Person {name: 'Bob'}) SET p.role = 'Senior Engineer' RETURN p

// Add a label
MATCH (n {name: 'Phoenix'}) SET n:ActiveProject RETURN n

// ============ DELETE ============

// Delete an edge
MATCH (a:Person {name: 'Alice'})-[r:MANAGES]->(b:Person {name: 'Bob'}) DELETE r

// Delete a node (edges must be deleted first)
MATCH (n:Person {name: 'Bob'}) DETACH DELETE n

// Soft delete (recommended for KGs)
MATCH (n:Person {name: 'Bob'}) SET n.deleted = true, n.deleted_at = datetime()
```

</details>

### 2.2 Traversal — The Power of Graphs

<details>
<summary>Cypher Code — Traversal Patterns (Click to view)</summary>

```cypher
// 1. ONE-HOP: Who works on Phoenix?
MATCH (person:Person)-[:WORKS_ON]->(p:Project {name: 'Phoenix'})
RETURN person.name

// 2. VARIABLE-LENGTH: Find through 1-3 hops of REPORTS_TO/MANAGES
MATCH path = (junior:Person)-[:REPORTS_TO|MANAGES*1..3]->(senior:Person {name: 'Alice'})
RETURN junior.name, length(path) as hops, [n in nodes(path) | n.name] as path

// 3. SHORTEST PATH: Shortest path between two people
MATCH (a:Person {name: 'Bob'}), (b:Person {name: 'Carol'})
MATCH path = shortestPath((a)-[:REPORTS_TO|MANAGES*]-(b))
RETURN path, length(path)

// 4. SUBGRAPH: Grab the whole subgraph around a node (1-hop neighbors)
MATCH (center:Project {name: 'Phoenix'})-[r]-(neighbor)
RETURN center, r, neighbor

// 5. SUBGRAPH 2-HOPS: Expand 2 hops
MATCH (center:Project {name: 'Phoenix'})-[r1]-(n1)-[r2]-(n2)
RETURN center, r1, n1, r2, n2
LIMIT 50

// 6. AGGREGATION: Count how many projects each person works on
MATCH (person:Person)-[:WORKS_ON]->(project:Project)
RETURN person.name, count(project) as project_count
ORDER BY project_count DESC

// 7. FILTER ON THE PATH: Only take paths with high confidence
MATCH path = (a:Person)-[r:WORKS_ON*1..2]->(p:Project)
WHERE all(rel in relationships(path) WHERE rel.confidence > 0.8)
RETURN path
```

</details>

### 2.3 Full-Text & Vector Search Inside the Graph

Neo4j supports hybrid: graph traversal + full-text + vector indexes in the same DB.

```cypher
// Create a full-text index
CREATE FULLTEXT INDEX personNameFTS FOR (n:Person) ON EACH [n.name]

// Full-text search
CALL db.index.fulltext.queryNodes("personNameFTS", "Alice") YIELD node, score
RETURN node.name, score

// Create a vector index (Neo4j 5+)
CREATE VECTOR INDEX personEmbedding FOR (n:Person) ON n.embedding
OPTIONS {dimension: 768, similarityFunction: 'cosine'}

// Vector search
CALL db.index.vector.queryNodes("personEmbedding", 5, $queryVector) YIELD node, score
RETURN node.name, score

// HYBRID: Vector search + graph traversal
CALL db.index.vector.queryNodes("personEmbedding", 10, $queryVector) YIELD node, score
MATCH (node)-[:WORKS_ON]->(project:Project)
RETURN node.name, project.name, score
ORDER BY score DESC
```

---

## 3. Indexing & Performance

> **📌 Core Concept:**
> **An index = the "table of contents" of a database** — like the index at the back of a book: to find which page "Alice" is on, you don't flip through every page, you just look at the index. No index → every query must **scan the entire** graph (very slow at millions of nodes).
>
> **Principle:** Every index has a **write cost** (each new node must update the index). So only create indexes on **fields you query frequently** — don't create them willy-nilly.
>
> **Index type = the query type you need:**
> - Look up by exact name/id → **Range Index**
> - Search by fuzzy keywords in text → **Full-Text Index** (works like Google search)
> - Search by meaning (semantic, using vectors) → **Vector Index** (ANN finds the closest matches)
> - Filter on multiple properties → **Composite Index**
> - Need to guarantee no duplicates → **Unique Constraint** (creates an index behind the scenes)

### 3.1 The Index Types

```
┌──────────────────┬─────────────────────────────────┬─────────────────────────┐
│ Index Type       │ When to use                    │ Cypher                  │
├──────────────────┼─────────────────────────────────┼─────────────────────────┤
│ Range Index      │ Lookup by property (name, id)  │ CREATE INDEX FOR (n:Person) ON (n.name) │
│ Full-Text Index  │ Search by keyword               │ CREATE FULLTEXT INDEX ... ON EACH [n.bio] │
│ Vector Index     │ Semantic search                │ CREATE VECTOR INDEX ... ON n.embedding │
│ Composite Index  │ Filter on multiple properties  │ CREATE INDEX FOR (n:Project) ON (n.name, n.status) │
│ Constraint (unique)│ Guarantee uniqueness + hidden index │ CREATE CONSTRAINT FOR (n:Person) REQUIRE n.name IS UNIQUE │
└──────────────────┴─────────────────────────────────┴─────────────────────────┘
```

### 3.2 Query Optimization

```python
# ❌ Slow: no index, full scan
# MATCH (n:Person) WHERE n.name = 'Alice' RETURN n

# ✅ Fast: uses the index
# CREATE INDEX FOR (n:Person) ON (n.name)  -- create once
# MATCH (n:Person {name: 'Alice'}) RETURN n  -- automatically uses the index

# ❌ Slow: unlimited hops, explosion
# MATCH (a)-[*]->(b) RETURN a, b

# ✅ Fast: cap hops + limit
# MATCH (a:Person)-[:MANAGES*1..3]->(b:Person) RETURN a, b LIMIT 100

# ❌ Slow: returns the entire graph
# MATCH (n) RETURN n

# ✅ Fast: take only what you need
# MATCH (p:Person {name: 'Alice'})-[:WORKS_ON]->(proj) RETURN proj.name
```

### 3.3 Profiling

```cypher
// View the query plan
PROFILE MATCH (a:Person {name: 'Alice'})-[:MANAGES*1..3]->(b:Person) RETURN b

// The output shows: whether an index was used, db hits, memory
```

---

## 4. Transactions & Consistency

### 4.1 ACID for Graphs

```
┌───────────┬──────────────────────────────────────────────────────────┐
│ Property  │ Meaning for graphs                                       │
├───────────┼──────────────────────────────────────────────────────────┤
│ Atomicity │ Batch ingest: either everything succeeds, or full rollback │
│ Consistency│ No violation of ontology constraints                   │
│ Isolation │ Two concurrent transactions don't create duplicate nodes │
│ Durability│ After commit, data survives a crash                     │
└───────────┴──────────────────────────────────────────────────────────┘
```

### 4.2 Batch Ingest (Idempotent)

<details>
<summary>Python Code — Batch Ingest with MERGE (Click to view)</summary>

```python
from neo4j import GraphDatabase

class GraphIngestor:
    def __init__(self, uri: str, user: str, password: str):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
    
    def ingest_batch(self, entities: list, relations: list, batch_size: int = 1000):
        """Batch ingest — idempotent thanks to MERGE."""
        with self.driver.session() as session:
            # Batch entities
            for i in range(0, len(entities), batch_size):
                batch = entities[i:i + batch_size]
                session.execute_write(self._merge_entities, batch)
                print(f"Ingested entities batch {i//batch_size + 1}: {len(batch)} nodes")
            
            # Batch relations
            for i in range(0, len(relations), batch_size):
                batch = relations[i:i + batch_size]
                session.execute_write(self._merge_relations, batch)
                print(f"Ingested relations batch {i//batch_size + 1}: {len(batch)} edges")
    
    @staticmethod
    def _merge_entities(tx, batch):
        # UNWIND = a loop inside Cypher, more efficient than many calls
        query = """
        UNWIND $batch as row
        MERGE (n:Entity {name: row.name})
        SET n.type = row.type,
            n.description = row.description,
            n.updated_at = datetime()
        """
        tx.run(query, batch=batch)
    
    @staticmethod
    def _merge_relations(tx, batch):
        query = """
        UNWIND $batch as row
        MATCH (a:Entity {name: row.source})
        MATCH (b:Entity {name: row.target})
        MERGE (a)-[r:RELATED {type: row.type}]->(b)
        SET r.confidence = row.confidence,
            r.evidence = row.evidence,
            r.updated_at = datetime()
        """
        tx.run(query, batch=batch)
    
    def close(self):
        self.driver.close()

# Usage
ingestor = GraphIngestor("bolt://localhost:7687", "neo4j", "password")
ingestor.ingest_batch(entities, relations, batch_size=500)
ingestor.close()
```

**Key pattern:** `MERGE` instead of `CREATE` → idempotent, re-running doesn't create duplicates.

</details>

---

## 5. Deployment with Neo4j & Kuzu

### 5.1 Neo4j with Docker

```yaml
# docker-compose.yml
version: '3.8'
services:
  neo4j:
    image: neo4j:5-community
    ports:
      - "7474:7474"  # Browser
      - "7687:7687"  # Bolt
    environment:
      NEO4J_AUTH: neo4j/password
      NEO4J_PLUGINS: '["apoc", "graph-data-science"]'
    volumes:
      - neo4j_data:/data
      - neo4j_logs:/logs
    healthcheck:
      test: ["CMD", "cypher-shell", "-u", "neo4j", "-p", "password", "RETURN 1"]
      interval: 10s
      retries: 5

volumes:
  neo4j_data:
  neo4j_logs:
```

```bash
# Start it up
docker compose up -d neo4j
# Open the browser: http://localhost:7474

# Check
docker exec -it <container> cypher-shell -u neo4j -p password "MATCH (n) RETURN count(n)"
```

### 5.2 Kuzu (Embedded, Python-Native)

<details>
<summary>Python Code — Kuzu Embedded (Click to view)</summary>

```python
import kuzu

# Create an in-process DB (no Docker needed)
db = kuzu.Database("./kuzu_db")
conn = kuzu.Connection(db)

# Create the schema
conn.execute("CREATE NODE TABLE Person(name STRING, role STRING, PRIMARY KEY(name))")
conn.execute("CREATE NODE TABLE Project(name STRING, budget INT64, PRIMARY KEY(name))")
conn.execute("CREATE REL TABLE WORKS_ON(FROM Person TO Project, role STRING, confidence DOUBLE)")
conn.execute("CREATE REL TABLE MANAGES(FROM Person TO Person, since STRING)")

# Insert
conn.execute('CREATE (a:Person {name: "Alice", role: "CTO"})')
conn.execute('CREATE (a:Person {name: "Bob", role: "Engineer"})')
conn.execute('CREATE (a:Project {name: "Phoenix", budget: 500000})')

# Query
result = conn.execute("""
    MATCH (p:Person)-[r:WORKS_ON]->(proj:Project)
    RETURN p.name, proj.name, r.role
""")
while result.has_next():
    print(result.get_next())

# Hybrid: Kuzu also supports vector search (extension)
# conn.execute("INSTALL vector; LOAD EXTENSION vector;")
```

</details>

### 5.3 NetworkX (Prototyping, No DB Needed)

```python
import networkx as nx

# Fastest way to prototype — no DB to install
G = nx.DiGraph()

# Add nodes
G.add_node("Alice", label="Person", role="CTO")
G.add_node("Phoenix", label="Project", budget=500000)

# Add edges
G.add_edge("Alice", "Phoenix", type="WORKS_ON", confidence=0.9)

# Query: BFS traversal
from collections import deque

def bfs_traversal(graph, start: str, max_hops: int = 2) -> list:
    visited = set([start])
    queue = deque([(start, 0)])
    result = []
    while queue:
        node, hops = queue.popleft()
        if hops >= max_hops:
            continue
        for neighbor in graph.successors(node):
            if neighbor not in visited:
                visited.add(neighbor)
                result.append((node, neighbor, graph[node][neighbor]))
                queue.append((neighbor, hops + 1))
    return result

print(bfs_traversal(G, "Alice", max_hops=2))
```

---

## 6. Hands-On Labs

### Lab 1: Neo4j Docker + Cypher CRUD

1. `docker compose up -d neo4j`
2. Open `http://localhost:7474`, run the Cypher queries from §2.1
3. Create 20 nodes + 30 edges for a mini org chart

### Lab 2: Benchmark the Impact of Indexes

1. Create 10K nodes without an index → measure the time for `MATCH (n:Person {name: 'Alice'})`
2. Create the index `CREATE INDEX FOR (n:Person) ON (n.name)` → measure again
3. Compare latency (typically an 80–90% reduction)

### Lab 3: Compare 3 DBs

- Take the same 1K-node dataset, ingest it into NetworkX, Kuzu, and Neo4j
- Run the same `MATCH (a)-[*1..3]->(b)` query and compare latency

---

## References

- Neo4j Docs — *Cypher Manual* (https://neo4j.com/docs/cypher-manual/current/)
- Kuzu Docs — *Cypher Query* (https://docs.kuzudb.com/cypher/)
- *Graph Databases* — Robinson, Webber, Eifrem (O'Reilly, 2nd Edition)
- FalkorDB Docs — *Hybrid index: vector + full-text + range* (https://www.falkordb.com/docs/)
- LDBC — *Social Network Benchmark* (https://ldbcouncil.org/benchmarks/snb/)

---

*Next: [04 — Graph Embeddings](../04-graph-embeddings/)*
