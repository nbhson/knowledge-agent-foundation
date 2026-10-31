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

Với JSON, bạn viết vòng lặp BFS thủ công (BFS = duyệt graph theo từng vòng: ghé hết node gần trước, rồi mới đi xa), load toàn bộ file vào RAM, chạy 2 giây cho 1 query. Với 100 queries? Timeout.

**Graph Database** giải quyết: **lưu native + index + query engine** — trả lời cùng câu hỏi trong 15ms bằng một dòng Cypher (ngôn ngữ truy vấn đồ thị, chi tiết ở §2).

> **Tóm gọn 1 câu:** Lưu graph trong JSON chỉ ổn với graph nhỏ; muốn hỏi nhanh những câu nhiều bước, cần graph database có index và ngôn ngữ truy vấn riêng.

### Tại Sao Storage & Query Quan Trọng?

> *"Không có DB phù hợp, graph chỉ là JSON đắt tiền. Không có query language, graph chỉ là hình vẽ."*
>
> (3-hop = câu hỏi cần đi qua 3 cạnh quan hệ, ví dụ A → B → C → D.)

> **Cách đọc bảng này:** mỗi dòng là 1 nghiên cứu/benchmark; cột "Phát Hiện" nói nó đo được điều gì. Ví dụ, dòng 1: với câu hỏi cần đi qua 3 cạnh, lưu graph "thuần" nhanh hơn JOIN SQL 100–1000 lần.

| # | Nguồn | Phát Hiện |
|---|-------|-----------|
| 1 | **Neo4j Benchmark (2024)** | Native graph storage nhanh hơn relational JOIN **100-1000×** cho 3-hop queries |
| 2 | **KuzuDB Paper (2024)** | Embedded graph DB (Kuzu) đạt **10× throughput** so với NetworkX in-memory trên 10M edges |
| 3 | **LDBC SNB Benchmark** | Index trên `label + property` giảm latency **80%** cho lookup queries |

---

## Tổng Quan

Phần này vẽ 6 giai đoạn để đưa graph từ "nhận về" tới "truy vấn được": chọn DB → tạo schema và index → nạp dữ liệu an toàn → truy vấn → theo dõi hiệu năng.

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

> **Cách đọc bảng này:** cột "Chủ đề" là mục con bên dưới; cột "Mô tả" tóm tắt mục đó gồm những gì. Ví dụ, dòng 3 nói: phần Indexing sẽ dạy tạo index và tối ưu câu truy vấn.

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
> **Chọn nhanh theo nhu cầu:**
> - Đang học hoặc làm prototype? → **Kuzu / NetworkX** (không cần cài Docker)
> - Cần hệ thống ổn định lâu dài, cộng đồng lớn? → **Neo4j** (đi từ Community lên Aura khi cần mở rộng)
> - Graph tới hàng nghìn tỷ cạnh? → **NebulaGraph** (mở rộng ngang)
> - Cần phản hồi dưới một mili giây? → **FalkorDB / Memgraph** (chạy trong bộ nhớ)

### 1.1 So Sánh Chi Tiết

> **Cách đọc bảng này:** cột "Kiểu" = cách DB lưu graph (embedded = chạy ngay trong app, không cần server riêng; in-memory = giữ hết trong RAM); cột "Quy mô" = cỡ dữ liệu chịu được; cột "Truy vấn" = ngôn ngữ dùng để hỏi; cột cuối = tình huống hợp nhất. Ví dụ, Kuzu hợp ai viết Python và muốn chạy local dưới 1 giây.

```
┌────────────────┬──────────┬──────────┬──────────┬────────────────────────────┐
│ Database       │ Kiểu     │ Quy mô   │ Truy vấn │ Phù hợp nhất khi           │
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

> 📄 **Code ví dụ:** [`examples/01-1-2-decision-matrix.py`](examples/01-1-2-decision-matrix.py)

**Khuyến nghị cho Framework này:**

> **Cách đọc bảng này:** mỗi dòng là 1 giai đoạn của dự án — chọn DB theo nơi bạn đang đứng. Ví dụ, đang học thì chọn Kuzu vì cài 1 dòng `pip install` là chạy được.

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

<details>
<summary>Cypher Code — CRUD (Click để xem)</summary>

> 📄 **Code ví dụ:** [`examples/02-2-1-crud-co-ban.cypher`](examples/02-2-1-crud-co-ban.cypher)

</details>

### 2.2 Traversal — Sức Mạnh Của Graph

<details>
<summary>Cypher Code — Traversal Patterns (Click để xem)</summary>

> 📄 **Code ví dụ:** [`examples/03-2-2-traversal-suc-manh-cua-graph.cypher`](examples/03-2-2-traversal-suc-manh-cua-graph.cypher)

</details>

### 2.3 Full-Text & Vector Search Trong Graph

Neo4j hỗ trợ hybrid: graph traversal + full-text + vector index trên cùng DB.

> 📄 **Code ví dụ:** [`examples/04-2-3-full-text-vector-search-trong-graph.cypher`](examples/04-2-3-full-text-vector-search-trong-graph.cypher)

> **Tóm gọn 1 câu:** Cypher = SQL của đồ thị: bạn "vẽ" pattern cần tìm, DB tự đi tìm mọi chỗ khớp.

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

> **Cách đọc bảng này:** cột "Khi nào dùng" chỉ tình huống; cột "Cypher" là lệnh tạo index tương ứng. Ví dụ, dòng 1: hay hỏi theo tên → tạo index trên `n.name`.

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

> 📄 **Code ví dụ:** [`examples/05-3-2-query-optimization.py`](examples/05-3-2-query-optimization.py)

### 3.3 Profiling

> 📄 **Code ví dụ:** [`examples/06-3-3-profiling.cypher`](examples/06-3-3-profiling.cypher)

---

## 4. Transactions & Consistency

### 4.1 ACID Cho Graph

> **ACID = 4 lời hứa của một transaction** (transaction = nhóm thao tác hoặc xong hết, hoặc không xong gì — như chuyển tiền: không thể trừ tiền mà không nhận tiền). Cách đọc bảng: cột trái là tên lời hứa, cột phải là nghĩa của nó khi nạp dữ liệu vào graph.

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

> 📄 **Code ví dụ:** [`examples/07-4-2-batch-ingest-idempotent.py`](examples/07-4-2-batch-ingest-idempotent.py)

**Key pattern:** `MERGE` thay vì `CREATE` → idempotent (chạy lại bao nhiêu lần cũng cho cùng kết quả — như nút thang máy: bấm 5 lần vẫn chỉ gọi 1 chuyến), chạy lại không tạo node trùng.

> **Tóm gọn 1 câu:** Transaction bảo đảm "hoặc xong hết hoặc không xong gì", còn `MERGE` bảo đảm nạp lại 100 lần cũng không sinh dữ liệu trùng.

</details>

---

## 5. Triển Khai Với Neo4j & Kuzu

### 5.1 Neo4j với Docker

> **Docker** = chạy phần mềm trong "hộp" đóng gói sẵn — không cần cài tay từng thành phần, xoá hộp là sạch sẽ.

> 📄 **Code ví dụ:** [`examples/08-5-1-neo4j-voi-docker.yaml`](examples/08-5-1-neo4j-voi-docker.yaml)

> 📄 **Code ví dụ:** [`examples/09-5-1-neo4j-voi-docker.sh`](examples/09-5-1-neo4j-voi-docker.sh)

### 5.2 Kuzu (Embedded, Python-Native)

<details>
<summary>Python Code — Kuzu Embedded (Click để xem)</summary>

> 📄 **Code ví dụ:** [`examples/10-5-2-kuzu-embedded-python-native.py`](examples/10-5-2-kuzu-embedded-python-native.py)

</details>

### 5.3 NetworkX (Prototyping, Không Cần DB)

> 📄 **Code ví dụ:** [`examples/11-5-3-networkx-prototyping-khong-can-db.py`](examples/11-5-3-networkx-prototyping-khong-can-db.py)

> **Tóm gọn 1 câu:** Neo4j chạy như server riêng (qua Docker), Kuzu chạy ngay trong Python (embedded = gắn liền app, không cần server), còn NetworkX chỉ là thư viện prototype — chưa phải database.

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
- Chạy cùng query `MATCH (a)-[*1..3]->(b)` — đi 1 đến 3 bước từ node này tới node kia — và so sánh latency (latency = thời gian trả lời 1 câu hỏi)

> **Tóm gọn 1 câu:** Tự tay làm 3 lab trên là cách nhanh nhất để "cảm" được khác biệt giữa các DB và giá trị thật của index.

---

## Tài Liệu Tham Khảo

> Tài liệu chính thức để tra cú pháp khi làm; cần gì tra nấy, không cần đọc hết.

- Neo4j Docs — *Cypher Manual* (https://neo4j.com/docs/cypher-manual/current/)
- Kuzu Docs — *Cypher Query* (https://docs.kuzudb.com/cypher/)
- *Graph Databases* — Robinson, Webber, Eifrem (O'Reilly, 2nd Edition)
- FalkorDB Docs — *Hybrid index: vector + full-text + range* (https://www.falkordb.com/docs/)
- LDBC — *Social Network Benchmark* (https://ldbcouncil.org/benchmarks/snb/)

---

## GraphRAG — Cập nhật 2026

> **Đang nói về gì:** GraphRAG = RAG có trợ giúp của đồ thị (RAG = đưa tài liệu liên quan vào prompt cho LLM trả lời). **Multi-hop** = câu hỏi cần nối 2+ bước quan hệ; **vector-only RAG** = chỉ tìm theo "giống về nghĩa", không nhìn cấu trúc.

Microsoft GraphRAG (2024-2025): dùng knowledge graph để enhance RAG. Query phức tạp (multi-hop) tốt hơn vector-only RAG.

**Tin mới 2025-2026:**
- **LazyGraphRAG** (Microsoft, cuối 2024): defer LLM summarisation tới query time — "defer" = trì hoãn bước tóm tắt đắt tiền đến khi có người hỏi, thay vì tóm trước mọi thứ — indexing cost ngang vector RAG, quality ngang full GraphRAG, query cost thấp hơn ~700×. Đã tích hợp Microsoft Discovery (2025) và Azure Local.
- **LightRAG** (HKUDS, EMNLP 2025): dual-layer graph + vector, incremental update (thêm tài liệu mới chỉ cập nhật phần thay đổi) thay vì re-index toàn bộ.
- **GraphRAG-Bench** (Microsoft, 06/2025): multi-hop + global queries GraphRAG thắng; single-hop factoid vanilla RAG thắng.
- **Gartner (2026)**: GraphRAG trong "Top Trends in D&A for 2026" cho complex cases mà high-accuracy RAG thất bại.
- **Knowledge Graph Market**: 1.48B USD (2025) → 2.04B USD (2026). GraphRAG chuyển từ "enterprise luxury" → production baseline.

Ref: https://microsoft.github.io/graphrag/

> **Tóm gọn 1 câu:** Từ 2025-2026, GraphRAG đã rẻ và phổ biến hơn nhiều — chọn đúng biến thể giúp trả các câu hỏi nhiều bước mà vector RAG bó tay.

---

*Tiếp theo: [04 — Graph Embeddings](../04-graph-embeddings/)*
