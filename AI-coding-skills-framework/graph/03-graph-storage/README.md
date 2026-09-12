# 💾 03. Graph Storage & Query — Lưu Trữ và Truy Vấn Đồ Thị

> ## 📑 Mục Lục
>
> - [Câu Chuyện Mở Đầu](#câu-chuyện-mở-đầu)
> - [Tại Sao Storage & Query Quan Trọng?](#tại-sao-storage--query-quan-trọng)
> - [Tổng Quan](#tổng-quan)
> - [Nội Dung](#nội-dung)
> - [1. Chọn Graph Database](#1-chọn-graph-database)
> - [2. Cypher & GQL — Ngôn Ngữ Truy Vấn](#2-cypher--gql--ngôn-ngữ-truy-vấn)
> - [3. Indexing & Performance](#3-indexing--performance)
> - [4. Transactions & Consistency](#4-transactions--consistency)
> - [5. Triển Khai Với Neo4j & Kuzu](#5-triển-khai-với-neo4j--kuzu)
> - [6. Labs Thực Hành](#6-labs-thực-hành)
> - [Tài Liệu Tham Khảo](#tài-liệu-tham-khảo)

---

### Câu Chuyện Mở Đầu

Bạn đã trích được 5,000 entities và 12,000 relations. Bạn lưu vào `graph.json` — một file JSON 50MB.

Tuần sau, bạn cần trả lời: *"Tìm tất cả projects mà team của Alice đã làm, qua tối đa 3 bước REPORTS_TO/MANAGES."*

Với JSON, bạn viết vòng lặp BFS thủ công, load toàn bộ file vào RAM, chạy 2 giây cho 1 query. Với 100 queries? Timeout.

**Graph Database** giải quyết: **lưu native + index + query engine** — trả lời cùng câu hỏi trong 15ms bằng một dòng Cypher.

### Tại Sao Storage & Query Quan Trọng?

> *"Không có DB phù hợp, graph chỉ là JSON đắt tiền. Không có query language, graph chỉ là hình vẽ."*

| # | Nguồn | Phát Hiện |
|---|-------|-----------|
| 1 | **Neo4j Benchmark (2024)** | Native graph storage nhanh hơn relational JOIN **100-1000×** cho 3-hop queries |
| 2 | **KuzuDB Paper (2024)** | Embedded graph DB (Kuzu) đạt **10× throughput** so với NetworkX in-memory trên 10M edges |
| 3 | **LDBC SNB Benchmark** | Index trên `label + property` giảm latency **80%** cho lookup queries |

---

## Tổng Quan

```
Knowledge Graph (từ 02)
    │
    ▼
┌──────────────────────┐
│  CHỌN DATABASE       │  ← Neo4j, Kuzu, NebulaGraph, FalkorDB, NetworkX
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│  SCHEMA & INDEXING   │  ← Tạo constraints, indexes
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
│  OBSERVABILITY       │  ← Query log, slow query, metrics
└──────────────────────┘
```

---

## Nội Dung

| # | Chủ đề | Mô tả |
|---|--------|-------|
| 1 | [Chọn DB](#1-chọn-graph-database) | So sánh 6 DB, decision matrix |
| 2 | [Cypher & GQL](#2-cypher--gql--ngôn-ngữ-truy-vấn) | CRUD, traversal, aggregation, full-text |
| 3 | [Indexing](#3-indexing--performance) | Index types, query optimization |
| 4 | [Transactions](#4-transactions--consistency) | ACID, batch ingest, idempotency |
| 5 | [Triển Khai](#5-triển-khai-với-neo4j--kuzu) | Docker, Python client, code mẫu |

---

## 1. Chọn Graph Database

> **📌 Khi nào cần Graph DB?** Khi câu hỏi của bạn là **"thực thể này liên quan đến ai/as thế nào?"** (traversal multi-hop), SQL phải JOIN nhiều lần rất chậm — graph DB đi qua edges trực tiếp. **Dấu hiệu cần graph DB:** truy vấn của bạn luôn có pattern `A —[...]→ B —[...]→ C` (2+ hops).
>
> **Q&A nhanh để chọn:**
> - Bạn đang học/prototype? → **Kuzu / NetworkX** (không cần cài Docker)
> - Cần production ổn định, ecosystem lớn? → **Neo4j** (Community → Aura khi scale)
> - Hàng ngàn tỷ edges? → **NebulaGraph** (scale-out)
> - Cần phản hồi dưới mili giây? → **FalkorDB / Memgraph** (in-memory)

### 1.1 So Sánh Chi Tiết

```
┌────────────────┬──────────┬──────────┬──────────┬────────────────────────────┐
│ Database       │ Type     │ Scale    │ Query    │ Best For                   │
├────────────────┼──────────┼──────────┼──────────┼────────────────────────────┤
│ Neo4j          │ Property │ Billions │ Cypher   │ Production, ecosystem lớn  │
│ (Community/Ent)│ Graph    │ nodes    │ GQL      │ Full-text, GDS, Aura cloud │
│ NebulaGraph    │ Distrib. │ Trillions│ nGQL     │ Trillions edges, scale-out │
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
    Chọn DB dựa trên yêu cầu.
    
    requirements = {
        "scale": "small" | "medium" | "large" | "trillion",
        "deployment": "local" | "self-hosted" | "managed",
        "latency": "realtime" | "interactive" | "batch",
        "team_size": int,
    }
    """
    if requirements["scale"] == "small" and requirements["deployment"] == "local":
        return "Kuzu (embedded, zero-ops) hoặc NetworkX (prototyping)"
    
    if requirements["scale"] in ["large", "trillion"]:
        return "NebulaGraph hoặc Neo4j Enterprise Cluster"
    
    if requirements["latency"] == "realtime":
        return "FalkorDB hoặc Memgraph (in-memory)"
    
    if requirements["deployment"] == "managed":
        return "Neo4j Aura hoặc Amazon Neptune"
    
    # Default: production balanced
    return "Neo4j Community (self-hosted) — khuyến nghị cho hầu hết dự án"
```

**Khuyến nghị cho Framework này:**

| Giai đoạn | DB | Lý do |
|-----------|----|-------|
| **Học & Prototype** | Kuzu hoặc NetworkX | Zero setup, `pip install`, chạy local |
| **Development** | Neo4j Community (Docker) | Cypher chuẩn, GDS library, dễ migrate lên Aura |
| **Production** | Neo4j Aura / NebulaGraph | Managed, HA, backup |

> **📌 Khái Niệm Bổ Sung: FalkorDB & Hybrid Indexing**
>
> **FalkorDB** = graph database chạy **ngay trên Redis** (từng tên "RedisGraph"). Lưu đồ thị dưới dạng **sparse matrices** (dùng thư viện tính ma trận thưa GraphBLAS) — về bản chất là "tính traversal bằng phép nhân ma trận", cực nhanh với dữ liệu lưu trong RAM. Query bằng Cypher, phản hồi **dưới mili giây** với hàng triệu nodes.
>
> **"Hybrid indexing trong một engine"**: FalkorDB đánh index **nhiều kiểu dữ liệu trên cùng 1 node** — full-text (tìm "tên chứa 'Phoenix'"), vector search (tìm "entity giống embedding này"), và range index (lọc theo số). Nghĩa là một truy vấn GraphRAG có thể lọc theo text + vector + thời gian **ngay trong DB**, không cần kéo về application layer. Neo4j cũng kết hợp full-text + vector index từ bản 5.x; Kuzu bổ sung vector index từ v1.5 — xu hướng chung là **một engine, nhiều kiểu index**.

---

## 2. Cypher & GQL — Ngôn Ngữ Truy Vấn

> **📌 Khái Niệm Cơ Bản:**
> **Cypher** = ngôn ngữ truy vấn graph (giống SQL cho relational db). Câu Cypher **"vẽ ra"** pattern bạn muốn tìm — đọc khá trực quan:
>
> ```
> MATCH (a:Person)-[:MANAGES]->(b:Person)  ← "vẽ": Person a —MANAGES→ Person b
> WHERE a.name = 'Alice'                   ← "lọc": chỉ Alice
> RETURN b.name                            ← "lấy ra": tên các nhân viên
> ```
>
> **Cú pháp biểu tượng:**
> - `(n)` = node, `(n:Label)` = node có label, `(n:Label {prop: 'val'})` = node có property
> - `--` = vô hướng, `-->`/`<--` = có hướng, `-[:TYPE]->` = edge có type
> - `*1..3` = từ 1 đến 3 hops (traversal)
>
> **Analogies:** SQL = câu hỏi trên bảng tính (phải biết trước cột nào). Cypher = mô tả hình ảnh quan hệ (vẽ pattern ra, DB tự tìm khớp).

### 2.1 CRUD Cơ Bản

### 2.1 CRUD Cơ Bản

<details>
<summary>Cypher Code — CRUD (Click để xem)</summary>

```cypher
// ============ CREATE ============

// Tạo node
CREATE (a:Person {name: 'Alice', role: 'CTO', age: 35})
CREATE (b:Person {name: 'Bob', role: 'Engineer'})
CREATE (p:Project {name: 'Phoenix', budget: 500000})

// Tạo edge
MATCH (a:Person {name: 'Alice'}), (b:Person {name: 'Bob'})
CREATE (a)-[:MANAGES {since: '2024-01-01'}]->(b)

MATCH (b:Person {name: 'Bob'}), (p:Project {name: 'Phoenix'})
CREATE (b)-[:WORKS_ON {role: 'Lead', allocation: 0.8}]->(p)

// ============ READ ============

// Tìm tất cả Person
MATCH (n:Person) RETURN n.name, n.role

// Tìm với filter
MATCH (p:Project) WHERE p.budget > 300000 RETURN p

// ============ UPDATE ============

// Cập nhật property
MATCH (p:Person {name: 'Bob'}) SET p.role = 'Senior Engineer' RETURN p

// Thêm label
MATCH (n {name: 'Phoenix'}) SET n:ActiveProject RETURN n

// ============ DELETE ============

// Xóa edge
MATCH (a:Person {name: 'Alice'})-[r:MANAGES]->(b:Person {name: 'Bob'}) DELETE r

// Xóa node (phải xóa edges trước)
MATCH (n:Person {name: 'Bob'}) DETACH DELETE n

// Soft delete (khuyến nghị cho KG)
MATCH (n:Person {name: 'Bob'}) SET n.deleted = true, n.deleted_at = datetime()
```

</details>

### 2.2 Traversal — Sức Mạnh Của Graph

<details>
<summary>Cypher Code — Traversal Patterns (Click để xem)</summary>

```cypher
// 1. ONE-HOP: Ai làm việc trên Phoenix?
MATCH (person:Person)-[:WORKS_ON]->(p:Project {name: 'Phoenix'})
RETURN person.name

// 2. VARIABLE-LENGTH: Tìm qua 1-3 hops REPORTS_TO/MANAGES
MATCH path = (junior:Person)-[:REPORTS_TO|MANAGES*1..3]->(senior:Person {name: 'Alice'})
RETURN junior.name, length(path) as hops, [n in nodes(path) | n.name] as path

// 3. SHORTEST PATH: Đường ngắn nhất giữa 2 người
MATCH (a:Person {name: 'Bob'}), (b:Person {name: 'Carol'})
MATCH path = shortestPath((a)-[:REPORTS_TO|MANAGES*]-(b))
RETURN path, length(path)

// 4. SUBGRAPH: Lấy toàn bộ subgraph quanh 1 node (1-hop neighbors)
MATCH (center:Project {name: 'Phoenix'})-[r]-(neighbor)
RETURN center, r, neighbor

// 5. SUBGRAPH 2-HOPS: Mở rộng 2 hops
MATCH (center:Project {name: 'Phoenix'})-[r1]-(n1)-[r2]-(n2)
RETURN center, r1, n1, r2, n2
LIMIT 50

// 6. AGGREGATION: Đếm số projects mỗi person tham gia
MATCH (person:Person)-[:WORKS_ON]->(project:Project)
RETURN person.name, count(project) as project_count
ORDER BY project_count DESC

// 7. FILTER TRÊN PATH: Chỉ lấy path có confidence cao
MATCH path = (a:Person)-[r:WORKS_ON*1..2]->(p:Project)
WHERE all(rel in relationships(path) WHERE rel.confidence > 0.8)
RETURN path
```

</details>

### 2.3 Full-Text & Vector Search Trong Graph

Neo4j hỗ trợ hybrid: graph traversal + full-text + vector index trên cùng DB.

```cypher
// Tạo full-text index
CREATE FULLTEXT INDEX personNameFTS FOR (n:Person) ON EACH [n.name]

// Full-text search
CALL db.index.fulltext.queryNodes("personNameFTS", "Alice") YIELD node, score
RETURN node.name, score

// Tạo vector index (Neo4j 5+)
CREATE VECTOR INDEX personEmbedding FOR (n:Person) ON n.embedding
OPTIONS {dimension: 768, similarityFunction: 'cosine'}

// Vector search
CALL db.index.vector.queryNodes("personEmbedding", 5, $queryVector) YIELD node, score
RETURN node.name, score

// HYBRID: Vector search + Graph traversal
CALL db.index.vector.queryNodes("personEmbedding", 10, $queryVector) YIELD node, score
MATCH (node)-[:WORKS_ON]->(project:Project)
RETURN node.name, project.name, score
ORDER BY score DESC
```

---

## 3. Indexing & Performance

> **📌 Khái Niệm Cơ Bản:**
> **Index = "mục lục" của database** — giống mục lục cuối sách: muốn tìm "Alice" ở trang nào không cần lật từng trang, chỉ cần tra mục lục. Không có index → mỗi truy vấn phải **quét toàn bộ** graph (rất chậm với triệu nodes).
>
> **Nguyên tắc:** Index nào cũng có **chi phí ghi** (mỗi lần thêm node phải cập nhật index). Nên chỉ tạo index cho **các trường bạn truy vấn thường xuyên** — không tạo bừa bãi.
>
> **Loại index = loại truy vấn bạn cần:**
> - Tìm theo tên/id chính xác → **Range Index**
> - Tìm theo từ khóa trong text (mơ hồ) → **Full-Text Index** (hoạt động như Google search)
> - Tìm theo nghĩa (semantic, dùng vector) → **Vector Index** (ANN tìm gần giống)
> - Lọc nhiều thuộc tính → **Composite Index**
> - Cần đảm bảo không trùng lặp → **Unique Constraint** (tự tạo index ngầm)

### 3.1 Các Loại Index

```
┌──────────────────┬─────────────────────────────────┬─────────────────────────┐
│ Index Type       │ Khi nào dùng                    │ Cypher                  │
├──────────────────┼─────────────────────────────────┼─────────────────────────┤
│ Range Index      │ Lookup theo property (name, id) │ CREATE INDEX FOR (n:Person) ON (n.name) │
│ Full-Text Index  │ Search theo keyword             │ CREATE FULLTEXT INDEX ... ON EACH [n.bio] │
│ Vector Index     │ Semantic search                 │ CREATE VECTOR INDEX ... ON n.embedding │
│ Composite Index  │ Filter nhiều properties         │ CREATE INDEX FOR (n:Project) ON (n.name, n.status) │
│ Constraint (unique)│ Đảm bảo unique + index ngầm  │ CREATE CONSTRAINT FOR (n:Person) REQUIRE n.name IS UNIQUE │
└──────────────────┴─────────────────────────────────┴─────────────────────────┘
```

### 3.2 Query Optimization

```python
# ❌ Chậm: không dùng index, scan toàn bộ
# MATCH (n:Person) WHERE n.name = 'Alice' RETURN n

# ✅ Nhanh: dùng index
# CREATE INDEX FOR (n:Person) ON (n.name)  -- tạo 1 lần
# MATCH (n:Person {name: 'Alice'}) RETURN n  -- tự động dùng index

# ❌ Chậm: không giới hạn hops, explosion
# MATCH (a)-[*]->(b) RETURN a, b

# ✅ Nhanh: giới hạn hops + limit
# MATCH (a:Person)-[:MANAGES*1..3]->(b:Person) RETURN a, b LIMIT 100

# ❌ Chậm: trả về toàn bộ graph
# MATCH (n) RETURN n

# ✅ Nhanh: chỉ lấy cần thiết
# MATCH (p:Person {name: 'Alice'})-[:WORKS_ON]->(proj) RETURN proj.name
```

### 3.3 Profiling

```cypher
// Xem query plan
PROFILE MATCH (a:Person {name: 'Alice'})-[:MANAGES*1..3]->(b:Person) RETURN b

// Output cho biết: có dùng index không, số db hits, memory
```

---

## 4. Transactions & Consistency

### 4.1 ACID Cho Graph

```
┌───────────┬──────────────────────────────────────────────────────────┐
│ Thuộc tính│ Ý nghĩa cho Graph                                        │
├───────────┼──────────────────────────────────────────────────────────┤
│ Atomicity │ Batch ingest: hoặc tất cả thành công, hoặc rollback hết │
│ Consistency│ Không vi phạm ontology constraints                      │
│ Isolation │ 2 transactions đồng thời không tạo duplicate nodes      │
│ Durability│ Sau commit, data không mất khi crash                    │
└───────────┴──────────────────────────────────────────────────────────┘
```

### 4.2 Batch Ingest (Idempotent)

<details>
<summary>Python Code — Batch Ingest với MERGE (Click để xem)</summary>

```python
from neo4j import GraphDatabase

class GraphIngestor:
    def __init__(self, uri: str, user: str, password: str):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
    
    def ingest_batch(self, entities: list, relations: list, batch_size: int = 1000):
        """Batch ingest — idempotent nhờ MERGE."""
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
        # UNWIND = loop trong Cypher, hiệu quả hơn gọi nhiều lần
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

**Key pattern:** `MERGE` thay vì `CREATE` → idempotent, chạy lại không tạo duplicate.

</details>

---

## 5. Triển Khai Với Neo4j & Kuzu

### 5.1 Neo4j với Docker

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
# Khởi động
docker compose up -d neo4j
# Mở browser: http://localhost:7474

# Kiểm tra
docker exec -it <container> cypher-shell -u neo4j -p password "MATCH (n) RETURN count(n)"
```

### 5.2 Kuzu (Embedded, Python-Native)

<details>
<summary>Python Code — Kuzu Embedded (Click để xem)</summary>

```python
import kuzu

# Tạo DB in-process (không cần Docker)
db = kuzu.Database("./kuzu_db")
conn = kuzu.Connection(db)

# Tạo schema
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

# Hybrid: Kuzu cũng hỗ trợ vector search (extension)
# conn.execute("INSTALL vector; LOAD EXTENSION vector;")
```

</details>

### 5.3 NetworkX (Prototyping, Không Cần DB)

```python
import networkx as nx

# Nhanh nhất để prototype — không cần install DB
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

## 6. Labs Thực Hành

### Lab 1: Neo4j Docker + Cypher CRUD

1. `docker compose up -d neo4j`
2. Mở `http://localhost:7474`, chạy các Cypher queries trong §2.1
3. Tạo 20 nodes + 30 edges cho org chart mini

### Lab 2: Benchmark Index Impact

1. Tạo 10K nodes không index → đo thời gian `MATCH (n:Person {name: 'Alice'})`
2. Tạo index `CREATE INDEX FOR (n:Person) ON (n.name)` → đo lại
3. So sánh latency (thường giảm 80-90%)

### Lab 3: So Sánh 3 DB

- Cùng một dataset 1K nodes, ingest vào NetworkX, Kuzu, và Neo4j
- Chạy cùng query `MATCH (a)-[*1..3]->(b)` và so sánh latency

---

## Tài Liệu Tham Khảo

- Neo4j Docs — *Cypher Manual* (https://neo4j.com/docs/cypher-manual/current/)
- Kuzu Docs — *Cypher Query* (https://docs.kuzudb.com/cypher/)
- *Graph Databases* — Robinson, Webber, Eifrem (O'Reilly, 2nd Edition)
- FalkorDB Docs — *Hybrid index: vector + full-text + range* (https://www.falkordb.com/docs/)
- LDBC — *Social Network Benchmark* (https://ldbcouncil.org/benchmarks/snb/)

---

*Tiếp theo: [04 — Graph Embeddings](../04-graph-embeddings/)*
