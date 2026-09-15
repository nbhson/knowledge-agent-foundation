# Graph Engineering — Kỹ Thuật Thiết Kế Hệ Thống Tri Thức Dạng Đồ Thị Cho AI Agents

> **"Vector search tìm được đoạn văn giống nhau. Graph search tìm được mối quan hệ ẩn sau đoạn văn đó."**  
> — GraphRAG Team, Microsoft Research (2024)

---

## Mục Lục

- [Graph Engineering — Kỹ Thuật Thiết Kế Hệ Thống Tri Thức Dạng Đồ Thị Cho AI Agents](#graph-engineering--kỹ-thuật-thiết-kế-hệ-thống-tri-thức-dạng-đồ-thị-cho-ai-agents)
  - [Mục Lục](#mục-lục)
  - [1. Giới Thiệu](#1-giới-thiệu)
    - [Bối Cảnh](#bối-cảnh)
    - [Mục Đích](#mục-đích)
  - [2. Graph Engineering Là Gì?](#2-graph-engineering-là-gì)
    - [Định Nghĩa](#định-nghĩa)
    - [Triết Lý Cốt Lõi](#triết-lý-cốt-lõi)
    - [So Sánh Với Các Paradigm Khác](#so-sánh-với-các-paradigm-khác)
  - [3. Ba Giai Đoạn Tiến Hóa Của Retrieval](#3-ba-giai-đoạn-tiến-hóa-của-retrieval)
  - [4. Tại Sao Graph Engineering Quan Trọng?](#4-tại-sao-graph-engineering-quan-trọng)
  - [5. Các Thành Phần Cốt Lõi Của Graph](#5-các-thành-phần-cốt-lõi-của-graph)
  - [6. Kiến Trúc Tổng Thể: 7 Components → 9 Modules](#6-kiến-trúc-tổng-thể-7-components--9-modules)
  - [7. Case Studies](#7-case-studies)
  - [8. Nguyên Tắc Thiết Kế Graph](#8-nguyên-tắc-thiết-kế-graph)
  - [9. Best Practices](#9-best-practices)
  - [10. Công Cụ và Framework](#10-công-cụ-và-framework)
  - [11. Tương Lai Của Graph Engineering](#11-tương-lai-của-graph-engineering)
  - [12. Tài Liệu Tham Khảo](#12-tài-liệu-tham-khảo)

---

## 1. Giới Thiệu

Trong kỷ nguyên RAG (2023-2025), chúng ta đã chứng minh: **chỉ cần đưa đúng context vào LLM, model nhỏ cũng thắng model lớn**. Nhưng RAG dựa trên vector search có một điểm mù chí mạng: nó chỉ tìm **"đoạn văn giống câu hỏi"** — không tìm được **"mối quan hệ giữa các thực thể"**.

**Ví dụ:**
- Hỏi: *"Ai là người phê duyệt hợp đồng của dự án X, và người đó báo cáo cho ai?"*
- Vector RAG: tìm được chunk chứa "dự án X" nhưng **không nối** được `Người phê duyệt → Quản lý cấp trên` nếu 2 thông tin nằm ở 2 documents khác nhau.
- Graph RAG: duyệt `Project X —[approved_by]→ Person A —[reports_to]→ Person B` → trả lời chính xác với **citation path**.

### Bối Cảnh

Năm 2024, Microsoft Research công bố **GraphRAG**: dùng LLM trích xuất Knowledge Graph từ toàn bộ corpus, rồi community detection + hierarchical summarization. Kết quả: **tăng 30-40% comprehensiveness và diversity** so với vanilla RAG trên các câu hỏi tổng hợp (global sensemaking).

Cùng lúc, Neo4j, NebulaGraph, và FalkorDB đưa graph databases vào production AI stacks. Kiến thức dạng đồ thị từ "nice-to-have" trở thành **substrate bắt buộc** cho agents cần reasoning đa bước.

### Mục Đích

Tài liệu này cung cấp cái nhìn toàn diện về Graph Engineering:

- Định nghĩa, triết lý, và so sánh với Vector/RAG thuần
- Phân tích 3 giai đoạn tiến hoá: Keyword → Vector → Graph
- 7 thành phần cốt lõi của hệ thống graph
- Mapping 7 components → 9 modules thực hành trong `graph/`
- Case studies: Microsoft GraphRAG, Neo4j + LangChain, DeepSeek Knowledge Graph
- Nguyên tắc thiết kế, best practices, và roadmap 2026-2028

---

## 2. Graph Engineering Là Gì?

### Định Nghĩa

**Graph Engineering** là kỹ thuật xây dựng và vận hành **hệ thống tri thức dạng đồ thị** làm nền tảng cho AI Agents — bao gồm trích xuất thực thể/quan hệ, lưu trữ đồ thị, embeddings, truy vấn, reasoning, và tích hợp vào pipeline RAG/Workflow.

Nói đơn giản:
- **Vector DB** trả lời: *"Đoạn nào giống câu hỏi nhất?"*
- **Graph DB** trả lời: *"Thực thể nào liên quan, qua bao nhiêu bước, với độ tin cậy bao nhiêu?"*
- **Graph Engineering** kết hợp cả hai để trả lời: *"Câu trả lời đúng nhất, có giải thích được, với đường dẫn chứng minh."*

### Triết Lý Cốt Lõi

> *"Mỗi khi LLM hallucinate vì thiếu liên kết, bạn không viết prompt dài hơn — bạn xây một cạnh (edge) mới trong đồ thị."*

1. **Relationships over Chunks**: Tri thức thực sự nằm ở **quan hệ**, không phải đoạn văn cô lập. Chunking chia nhỏ văn bản; graph **nối lại** chúng.
2. **Structure over Similarity**: Similarity tìm cái giống; structure tìm **cái liên quan qua trung gian** (multi-hop).
3. **Explainability over Black-box**: Mỗi câu trả lời có thể truy về **path** trong đồ thị — audit được, citation được.

### So Sánh Với Các Paradigm Khác

| Khía cạnh | Keyword Search (BM25) | Vector Search (RAG) | Graph Engineering |
|-----------|----------------------|---------------------|-------------------|
| **Focus** | Từ khóa chính xác | Ý nghĩa ngữ nghĩa | Thực thể + quan hệ + suy luận |
| **Đơn vị** | Document / Chunk | Chunk embedding | Node / Edge / Path / Community |
| **Truy vấn** | `MATCH keyword` | `cosine(query, chunk)` | `TRAVERSE / SHORTEST_PATH / COMMUNITY` |
| **Multi-hop** | ❌ Không | ❌ Yếu | ✅ Mạnh (2-6 hops) |
| **Explainability** | Thấp | Thấp | Cao (path + subgraph) |
| **Cập nhật** | Re-index | Re-embed | Thêm node/edge (incremental) |
| **Ví dụ** | Tìm "BHYT" | Tìm "bảo hiểm y tế ≈ BHYT" | `BHYT —covers→ Bệnh tim —treated_at→ BV Chợ Rẫy` |

> **Insight:** Graph không thay thế Vector — Graph **bao bọc và khuếch đại** Vector. Hệ thống tốt nhất là **Hybrid: Vector cho recall, Graph cho precision + reasoning**.

---

## 3. Ba Giai Đoạn Tiến Hóa Của Retrieval

```
┌──────────────────────────────────────────────────────────────────┐
│                    TIẾN HÓA RETRIEVAL                             │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  2020-2022: KEYWORD RETRIEVAL                                    │
│  ┌─────────────────────────────────┐                             │
│  │ "Tìm đúng từ khóa"              │                             │
│  │ BM25, TF-IDF, Inverted Index    │                             │
│  │ Control: ⭐ Thấp                │                             │
│  └─────────────────────────────────┘                             │
│                    │                                             │
│                    ▼                                             │
│  2023-2025: VECTOR RETRIEVAL (RAG)                                │
│  ┌─────────────────────────────────┐                             │
│  │ "Tìm ý nghĩa giống nhau"        │                             │
│  │ Embeddings + ANN (HNSW, IVF)    │                             │
│  │ Control: ⭐⭐⭐ Trung bình       │                             │
│  └─────────────────────────────────┘                             │
│                    │                                             │
│                    ▼                                             │
│  2026+: GRAPH RETRIEVAL (GraphRAG)                               │
│  ┌─────────────────────────────────┐                             │
│  │ "Tìm quan hệ + suy luận"       │                             │
│  │ Knowledge Graph + GraphRAG + GNN│                             │
│  │ Control: ⭐⭐⭐⭐⭐ Cao           │                             │
│  └─────────────────────────────────┘                             │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

Mỗi giai đoạn **bổ sung**, không thay thế:
- Bạn vẫn cần **BM25** cho exact match (mã hợp đồng, số hiệu).
- Bạn vẫn cần **Vector** cho semantic recall (paraphrase, synonym).
- Bạn cần thêm **Graph** cho multi-hop, aggregation, và global sensemaking.

---

## 4. Tại Sao Graph Engineering Quan Trọng?

### 4.1. Vượt Qua Giới Hạn Của Chunking

Vector RAG phụ thuộc vào chunking. Nếu 2 sự thật nằm ở 2 chunks khác nhau và không có chunk nào chứa cả hai → RAG **không bao giờ** trả lời đúng câu hỏi nối chúng. Graph trích xuất entities/relations **trước khi** chunking phá vỡ liên kết.

### 4.2. Global Sensemaking vs Local Lookup

Nghiên cứu Microsoft GraphRAG (2024):

| Loại câu hỏi | Vector RAG | GraphRAG |
|--------------|-----------|----------|
| Local: "Điều 5 của hợp đồng X nói gì?" | ✅ Tốt | ✅ Tốt |
| Global: "Chủ đề chính nào lặp lại trong toàn bộ 1000 tài liệu này?" | ❌ Yếu | ✅ Vượt trội (+35% comprehensiveness) |
| Multi-hop: "Dự án X do ai duyệt và người đó quản lý dự án nào khác?" | ❌ Hallucinate | ✅ Chính xác với path |

### 4.3. Giảm Hallucination Có Kiểm Chứng

Graph cung cấp **grounding path**: mỗi edge có `source_document`, `confidence`, `timestamp`. LLM phải đi theo path thay vì bịa. Microsoft báo cáo giảm **25-30% hallucination** khi thay vanilla RAG bằng GraphRAG trên benchmark QA.

### 4.4. Incremental Knowledge Updates

- Vector DB: cập nhật 1 tài liệu → re-chunk + re-embed nhiều chunks, khó giữ consistency.
- Graph DB: cập nhật 1 sự kiện → thêm/sửa 1 node/edge, **không ảnh hưởng** phần còn lại của đồ thị. Phù hợp cho enterprise knowledge base thay đổi hàng ngày.

### 4.5. Nền Tảng Cho Agent Reasoning

Agent cần **plan → retrieve → reason → act**. Graph cung cấp:
- **Planning**: duyệt dependencies giữa tasks (`Task A —blocks→ Task B`)
- **Reasoning**: path finding, community detection để suy luận gián tiếp
- **Memory**: lưu episodic memory dạng graph (`User —prefers→ Dark Mode —since→ 2025-11-01`)

---

## 5. Các Thành Phần Cốt Lõi Của Graph

```
┌──────────────────────────────────────────────────────────────────┐
│                    KIẾN TRÚC GRAPH HOÀN CHỈNH                     │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────┐      ┌─────────────┐      ┌──────────────┐     │
│  │   ENTITIES  │◄────►│  RELATIONS  │◄────►│   ONTOLOGY   │     │
│  │  (Nodes)    │      │  (Edges)    │      │  (Schema)    │     │
│  └─────────────┘      └─────────────┘      └──────────────┘     │
│         ▲                    ▲                     ▲              │
│         │                    │                     │              │
│         ▼                    ▼                     ▼              │
│  ┌────────────────────────────────────────────────────┐          │
│  │           GRAPH STORAGE & QUERY                    │          │
│  │   Neo4j / NebulaGraph / FalkorDB / RDF Triple Store│          │
│  └────────────────────────────────────────────────────┘          │
│         ▲                    ▲                     ▲              │
│         │                    │                     │              │
│  ┌─────────────┐      ┌─────────────┐      ┌──────────────┐     │
│  │ EMBEDDINGS  │      │   REASONING │      │   GRAPH RAG  │     │
│  │ (Vector+Graph)│    │(Traversal)  │      │ (Retrieval)  │     │
│  └─────────────┘      └─────────────┘      └──────────────┘     │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

| # | Thành phần | Vai trò | Module tương ứng |
|---|-----------|---------|-----------------|
| 1 | **Entities & Nodes** | Đơn vị tri thức (person, project, doc, concept) | `01-foundations` |
| 2 | **Relations & Edges** | Quan hệ có hướng, có trọng số, có thời gian | `01-foundations`, `02-knowledge-graph` |
| 3 | **Ontology & Schema** | Quy tắc: loại node/edge nào hợp lệ, ràng buộc | `02-knowledge-graph` |
| 4 | **Storage & Query** | Lưu và truy vấn (Cypher, GQL, SPARQL) | `03-graph-storage` |
| 5 | **Embeddings** | Vector hóa node/edge/path cho hybrid search | `04-graph-embeddings` |
| 6 | **Reasoning** | Traversal, shortest path, community, centrality | `06-graph-reasoning` |
| 7 | **GraphRAG** | Kết hợp graph + LLM để generate có grounding | `05-graph-rag` |

---

## 6. Kiến Trúc Tổng Thể: 7 Components → 9 Modules

```
┌──────────────────────────────────────────────────────────────────────────┐
│                 GRAPH ENGINEERING → MODULE MAPPING                        │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌──────────────┐     ┌────────────────────────────────────────┐         │
│  │ FOUNDATIONS  │────►│ 01-foundations                         │         │
│  │ Graph Theory │     │ Graph types, representations, metrics  │         │
│  └──────────────┘     └────────────────────────────────────────┘         │
│                                                                          │
│  ┌──────────────┐     ┌────────────────────────────────────────┐         │
│  │ KNOWLEDGE    │────►│ 02-knowledge-graph                     │         │
│  │ GRAPH BUILD  │     │ Entity/relation extraction, ontology   │         │
│  └──────────────┘     └────────────────────────────────────────┘         │
│                                                                          │
│  ┌──────────────┐     ┌────────────────────────────────────────┐         │
│  │ STORAGE      │────►│ 03-graph-storage                       │         │
│  │ & QUERY      │     │ Neo4j, Cypher, indexing, transaction   │         │
│  └──────────────┘     └────────────────────────────────────────┘         │
│                                                                          │
│  ┌──────────────┐     ┌────────────────────────────────────────┐         │
│  │ EMBEDDINGS   │────►│ 04-graph-embeddings                    │         │
│  │              │     │ Node2Vec, GraphSAGE, hybrid search     │         │
│  └──────────────┘     └────────────────────────────────────────┘         │
│                                                                          │
│  ┌──────────────┐     ┌────────────────────────────────────────┐         │
│  │ GRAPH RAG    │────►│ 05-graph-rag                           │         │
│  │              │     │ Subgraph retrieval, community summary  │         │
│  └──────────────┘     └────────────────────────────────────────┘         │
│                                                                          │
│  ┌──────────────┐     ┌────────────────────────────────────────┐         │
│  │ REASONING    │────►│ 06-graph-reasoning                     │         │
│  │              │     │ Path finding, inference, rules         │         │
│  └──────────────┘     └────────────────────────────────────────┘         │
│                                                                          │
│  ┌──────────────┐     ┌────────────────────────────────────────┐         │
│  │ LEARNING     │────►│ 07-gnn                                 │         │
│  │ (GNN)        │     │ GNN, link prediction, classification   │         │
│  └──────────────┘     └────────────────────────────────────────┘         │
│                                                                          │
│  ┌──────────────┐     ┌────────────────────────────────────────┐         │
│  │ WORKFLOW     │────►│ 08-graph-workflow                      │         │
│  │              │     │ Pipeline, incremental updates, ETL     │         │
│  └──────────────┘     └────────────────────────────────────────┘         │
│                                                                          │
│  ┌──────────────┐     ┌────────────────────────────────────────┐         │
│  │ EVALUATION   │────►│ 09-evaluation                          │         │
│  │              │     │ Correctness, coverage, hallucination   │         │
│  └──────────────┘     └────────────────────────────────────────┘         │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

### Tích Hợp Với Harness và Loop

```
HARNESS (harness/01-11)  ──►  cung cấp Tools, Memory, Context, Guardrails cho 1 Agent run
GRAPH   (graph/01-09)    ──►  cung cấp Knowledge substrate cho Harness (thay vì chỉ Vector DB)
LOOP    (loop/01-07)     ──►  điều phối NHIỀU Harness runs theo thời gian

Flow đầy đủ:
  Documents ──► Graph Construction (graph/02) ──► Graph Storage (graph/03)
      │
      ▼
  User Query ──► GraphRAG Retrieval (graph/05) ──► Context Building (harness/02)
      │
      ▼
  Prompt + Graph Context ──► LLM ──► Answer với citation path

Loop vận hành:
  Loop Scheduler ──► phát hiện document mới ──► incremental graph update (graph/08)
```

---

## 7. Case Studies

### 7.1. Microsoft GraphRAG — Global Sensemaking

**Kiến trúc:**

```
Documents ──► LLM Entity/Relation Extraction ──► Knowledge Graph
                                                         │
                              ┌──────────────────────────┘
                              ▼
                    Community Detection (Leiden)
                              │
                              ▼
                    Community Summarization (LLM)
                              │
                              ▼
                    Hierarchical Search:
                      - Local Search (entity-centric)
                      - Global Search (community summaries)
```

**Kết quả:** Trên benchmark Q&A tổng hợp từ podcast transcripts + news articles, GraphRAG đạt **win rate 70%** so với vanilla RAG khi đánh giá bởi LLM judge (comprehensiveness, diversity, empowerment).

**Bài học:** Đầu tư vào **pre-processing graph construction** đắt hơn (tốn LLM calls), nhưng payoff lớn cho câu hỏi phức tạp/long-tail.

### 7.2. Neo4j + LangChain — Enterprise Knowledge Graph

Stack production phổ biến:

```python
# Construction
from langchain_experimental.graph_transformers import LLMGraphTransformer
transformer = LLMGraphTransformer(llm=ChatOpenAI(model="gpt-4o"))
graph_docs = await transformer.convert_to_graph_documents(raw_docs)

# Storage
from langchain_community.graphs import Neo4jGraph
graph = Neo4jGraph(url="bolt://localhost:7687", username="neo4j", password="***")
graph.add_graph_documents(graph_docs)

# Retrieval
from langchain_community.chains import GraphCypherQAChain
chain = GraphCypherQAChain.from_llm(llm=ChatOpenAI(model="gpt-4o"), graph=graph)
answer = chain.invoke("Ai phê duyệt dự án X?")
```

### 7.3. DeepSeek Harness — Trajectory as Graph

DeepSeek lưu trajectory của agent **không phải** dạng flat log, mà dạng **event graph**: mỗi tool call là node, dependencies là edges → cho phép fork/replay nhánh như git branches (`harness/03-update-memory-store/trajectory-fork-replay.md`). Pattern này chính là **graph thinking** áp dụng cho agent execution.

### Bài Học Chung

1. **Graph construction là bottleneck** — chất lượng entity/relation extraction quyết định toàn bộ pipeline phía sau.
2. **Hybrid luôn thắng** — Vector cho recall, Graph cho reasoning. Đừng chọn 1 trong 2.
3. **Schema matter** — không có ontology, graph thành "hairball" không query được.

---

## 8. Nguyên Tắc Thiết Kế Graph

### 8.1. Nguyên Tắc SOLID Cho Graph

| Nguyên tắc | Áp dụng cho Graph |
|-----------|-------------------|
| **Single Responsibility** | Mỗi node type làm 1 việc (Person ≠ Organization ≠ Document) |
| **Open/Closed** | Thêm node/edge type mới không sửa schema cũ (extend, không modify) |
| **Liskov Substitution** | Subgraph phải thay thế được cho full graph trong test |
| **Interface Segregation** | Tách query interfaces: read-only vs write vs admin |
| **Dependency Inversion** | Code phụ thuộc vào Graph abstraction, không phụ thuộc Neo4j cụ thể |

### 8.2. The 8 Commandments of Graph Engineering

1. **Schema First, Data Second** — định nghĩa ontology trước khi ingest.
2. **Every Edge Has Provenance** — mỗi quan hệ phải có `source`, `confidence`, `timestamp`.
3. **Incremental Over Batch** — cập nhật graph theo event, không rebuild toàn bộ.
4. **Hybrid Search By Default** — luôn kết hợp vector + graph, không chọn 1.
5. **Paths Are Citations** — mỗi câu trả lời phải kèm path có thể verify.
6. **Community Before Detail** — summarize communities trước khi đi vào chi tiết local.
7. **Temporal Awareness** — quan hệ có thời gian (`valid_from`, `valid_until`), không phải vĩnh viễn.
8. **Evaluate With Graphs** — đo coverage, connectivity, hallucination rate, không chỉ BLEU/ROUGE.

### 8.3. Graph Design Pattern

```python
# Complete Graph Engineering Example
from graph_engine import GraphHarness

graph = GraphHarness(
    ontology={
        "node_types": ["Person", "Project", "Document", "Organization"],
        "edge_types": ["APPROVES", "REPORTS_TO", "BELONGS_TO", "REFERENCES"],
        "constraints": ["Person -[REPORTS_TO]-> Person", "Project -[APPROVES]-> Person"]
    },
    storage="neo4j://localhost:7687",
    embeddings={"model": "nomic-embed-text", "dim": 768},
    retrieval={
        "strategy": "hybrid",  # vector + graph traversal
        "max_hops": 3,
        "community_search": True,
    },
    reasoning={
        "path_finding": "shortest_path",
        "community_detection": "leiden",
    },
    evaluation={
        "metrics": ["coverage", "hallucination_rate", "path_precision"]
    }
)
```

---

## 9. Best Practices

### 9.1. Graph Construction
- ✅ Dùng LLM + rule-based hybrid cho extraction (LLM cho recall, rules cho precision).
- ✅ Deduplicate entities bằng embedding similarity + canonical name resolution.
- ✅ Batch extraction với checkpoint, không ingest 1 lần toàn bộ corpus lớn.

### 9.2. Storage & Query
- ✅ Index trên `label + property` hay dùng (ví dụ: `Person.name`).
- ✅ Giới hạn `max_hops` (thường 2-3) để tránh explosion.
- ✅ Dùng parameterized Cypher, không string concatenation.

### 9.3. Retrieval
- ✅ Retrieve **subgraph** (nodes + edges), không chỉ nodes cô lập.
- ✅ Re-rank paths bằng cross-encoder giống như re-rank chunks.
- ✅ Tóm tắt community trước khi trả về chi tiết local.

### 9.4. Guardrails
- ✅ Validate ontology trước khi write (không cho `Person -[EATS]-> Project`).
- ✅ Access control trên subgraph level (user chỉ thấy subgraph được phép).
- ✅ Temporal versioning: soft-delete edge bằng `valid_until`, không xóa cứng.

### 9.5. Testing Graph
- ✅ Unit test: từng extractor, từng Cypher query.
- ✅ Integration test: ingest → query → retrieve round-trip.
- ✅ Chaos test: thêm node/edge rác, đo retrieval robustness.

---

## 10. Công Cụ và Framework

### 10.1. Graph Databases

| Tool | Type | Scale | Best For |
|------|------|-------|----------|
| **Neo4j** | Property Graph | Billions nodes | Production, Cypher, ecosystem lớn |
| **NebulaGraph** | Distributed Property Graph | Trillions edges | Large-scale, horizontal scaling |
| **FalkorDB** | Redis-based Graph | Millions | Low-latency, Redis stack |
| **Amazon Neptune** | Managed (Property + RDF) | Billions | AWS managed, SPARQL + Gremlin |
| **Kuzu** | Embedded Graph DB | Millions | Local, Python-native, fast |
| **NetworkX** | In-memory Library | Thousands | Prototyping, algorithms |

### 10.2. LLM + Graph Frameworks

| Framework | Mô tả |
|-----------|-------|
| **Microsoft GraphRAG** | End-to-end: extract → communities → hierarchical Q&A |
| **LangChain GraphTransformers** | LLM → graph documents, Cypher QA chains |
| **LlamaIndex Property Graph** | Property graph index + retrievers |
| **NebulaGraph + LLM** | NGQL generation từ natural language |

### 10.3. Embeddings & GNN

| Tool | Mô tả |
|------|-------|
| **Node2Vec / DeepWalk** | Random walk embeddings, unsupervised |
| **GraphSAGE / GAT** | GNN cho inductive learning |
| **PyG (PyTorch Geometric)** | GNN library đầy đủ |
| **DGL (Deep Graph Library)** | Scalable GNN, multi-backend |

### 10.4. Starter Template

```
my-graph-project/
├── graph/
│   ├── 01-foundations/
│   ├── 02-knowledge-graph/
│   └── ... (09 modules)
├── data/
│   ├── raw_docs/
│   └── ontology.yaml
├── scripts/
│   ├── extract_graph.py
│   ├── query_graph.py
│   └── evaluate.py
└── docker-compose.yml  # Neo4j + app
```

---

## 11. Tương Lai Của Graph Engineering

### 11.1. Xu Hướng 2026-2028

| Năm | Xu hướng |
|-----|---------|
| **2026** | GraphRAG trở thành default cho enterprise RAG (thay vì vanilla vector RAG) |
| **2026** | Graph databases thêm vector index native → single DB cho hybrid search |
| **2027** | Temporal graphs phổ biến: mọi edge có lifecycle, query theo thời gian |
| **2027** | GNN + LLM fusion: LLM gọi GNN như tool để reasoning trên graph lớn |
| **2028** | Auto-ontology: LLM tự đề xuất và evolve schema từ data |
| **2028** | Federated graphs: nhiều org chia sẻ subgraph mà không chia sẻ raw data |

### 11.2. Thách Thức

- **Construction cost**: LLM extraction tốn token, cần cheaper distilled extractors.
- **Schema drift**: ontology thay đổi theo thời gian, migration phức tạp.
- **Evaluation**: chưa có benchmark chuẩn cho graph correctness như SWE-bench cho coding.

### 11.3. Lời Khuyên

> **"Bắt đầu với 100 documents, 3 node types, 5 edge types. Đừng cố xây Wikipedia Graph ngày đầu."**

---

## 12. Tài Liệu Tham Khảo

### Papers & Research
- Microsoft Research — *GraphRAG: Unlocking LLM discovery on narrative private data* (2024)
- *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks* — Lewis et al. (2020, RAG gốc)
- *Knowledge Graph Completion via Embeddings* — Bordes et al. (TransE, 2013)

### Frameworks & Tools
- [Microsoft GraphRAG (GitHub)](https://github.com/microsoft/graphrag)
- [Neo4j Graph Data Science](https://neo4j.com/docs/graph-data-science/current/)
- [LangChain — Graph QA](https://python.langchain.com/docs/use_cases/graph/)
- [LlamaIndex — Property Graph Index](https://docs.llamaindex.ai/en/stable/module_guides/indexing/lpg_index_guide/)

### Communities
- Neo4j Community Forum
- GraphRAG Discord
- Knowledge Graph Conference (KGC)

### Courses & Tutorials
- Neo4j GraphAcademy — *Introduction to Neo4j & Cypher*
- Stanford CS224W — *Machine Learning with Graphs*

---

*Bài viết thuộc [AI Coding Skills Framework](./AI_AGENT_FRAMEWORK.md) — Graph Engineering Track*
