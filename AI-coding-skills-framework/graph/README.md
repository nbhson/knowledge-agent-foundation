# 🕸️ XIII. Graph Engineering

> ## 📑 Mục Lục
>
> - [Câu Chuyện Mở Đầu](#câu-chuyện-mở-đầu)
> - [Tại Sao Graph Engineering Quan Trọng?](#tại-sao-graph-engineering-quan-trọng)
> - [Tổng Quan](#tổng-quan)
> - [Lộ Trình Học (Cấu Trúc Thư Mục)](#lộ-trình-học-cấu-trúc-thư-mục)
> - [Case Studies Thực Tế](#case-studies-thực-tế)
> - [Tài Liệu Tham Khảo](#tài-liệu-tham-khảo)

---

### Câu Chuyện Mở Đầu

Bạn có một kho tài liệu 10,000 trang về công ty: hợp đồng, báo cáo, org chart, emails. Bạn hỏi chatbot RAG:

> *"Hợp đồng dự án Phoenix do ai phê duyệt, và người đó từng quản lý dự án nào liên quan đến AI?"*

**Vector RAG** tìm được 5 chunks chứa "Phoenix" — nhưng không chunk nào chứa cả `người phê duyệt` lẫn `dự án AI` cùng lúc. Nó đoán mò, hallucinate một cái tên.

**GraphRAG** thì khác. Nó đã trích xuất sẵn:

```
(Phoenix) —[APPROVED_BY]→ (Nguyễn Văn A) —[MANAGED]→ (Project Atlas - AI Platform)
                  └—[REPORTS_TO]→ (Trần Thị B - CTO)
```

Một câu truy vấn `TRAVERSE 2 hops` trả về đáp án chính xác **kèm đường dẫn chứng minh** — không đoán, không bịa.

> *"Vector search tìm đoạn văn giống nhau. Graph search tìm mối quan hệ ẩn sau đoạn văn."*
> — **Microsoft Research, GraphRAG (2024)**

> *"Knowledge is not a pile of chunks. It's a web of relationships."*

**Graph Engineering** là kỹ thuật thiết kế **substrate tri thức dạng đồ thị** — để AI không chỉ *tìm* thông tin, mà còn *suy luận* trên thông tin đó qua nhiều bước, có giải thích, có citation.

### Tại Sao Graph Engineering Quan Trọng?

> **"Stop chunking. Start connecting. Get a path."**

#### 3 Bằng Chứng Khoa Học & Thực Tiễn

| # | Nghiên Cứu / Nguồn | Phát Hiện Quan Trọng |
|---|-------------------|----------------------|
| 1 | **Microsoft GraphRAG (2024)** | GraphRAG tăng **30-40% comprehensiveness** trên câu hỏi tổng hợp (global sensemaking) so với vanilla RAG; win rate 70% khi đánh giá bởi LLM judge |
| 2 | **Neo4j + LangChain Benchmark (2025)** | Hybrid Vector + Graph giảm **25-30% hallucination** trên enterprise QA benchmark (10K docs) |
| 3 | **Stanford CS224W (2024)** | Knowledge Graph retrieval giải quyết **multi-hop QA** với accuracy 68% vs 41% của vector-only RAG |

#### Triết lý cốt lõi:

```
Graph Engineering = Trích xuất thực thể & quan hệ → Lưu dạng đồ thị → Truy vấn + Suy luận → GraphRAG
```

**Phân biệt quan trọng:**

```
Harness  = môi trường 1 agent chạy (tools, context, permissions)
Loop     = harness + schedule + state + verification (chạy nhiều lần, tự duy trì)
Graph    = substrate tri thức bền vững (knowledge substrate) mà Harness và Loop cùng dùng

Vector DB  = "đoạn nào giống câu hỏi?"
Graph DB   = "thực thể nào liên quan qua bao nhiêu bước, với bằng chứng nào?"
GraphRAG   = Vector (recall) + Graph (precision + reasoning)
```

**Analogies**: Graph Engineering giống **bản đồ thành phố** — vector search cho bạn biết "có một nhà hàng gần đây", graph cho bạn biết "nhà hàng đó do ai sở hữu, họ còn sở hữu gì, và con đường ngắn nhất để đến đó là gì". Còn **chunking thuần** giống xé bản đồ thành từng mảnh rồi cố ghép lại khi cần.

**Nếu bỏ qua**: Agent trả lời đúng câu hỏi đơn giản nhưng hallucinate mọi câu hỏi multi-hop, không giải thích được nguồn, và không thể cập nhật tri thức mà không re-embed toàn bộ.

## Tổng Quan

**Graph Engineering** là việc thiết kế các **hệ thống tri thức dạng đồ thị** để AI agent lưu trữ, truy vấn, và suy luận trên tri thức có cấu trúc — với khả năng multi-hop traversal, community detection, và grounding có citation.

Khác với Module 01 (Retrieve Memory & Knowledge) vốn tập trung vào vector/hybrid search trên chunks, Graph Engineering tập trung vào **đồ thị tri thức**: mỗi sự thật là một cạnh (triple), mỗi câu trả lời là một đường đi (path), và mỗi tóm tắt là một community.

```
┌─────────────────────────────────────────────────────────────────────┐
│                      GRAPH ENGINEERING                               │
│                                                                     │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │              7 THÀNH PHẦN CỐT LÕI                              │  │
│  │  Entities · Relations · Ontology · Storage · Embeddings        │  │
│  │  Reasoning · GraphRAG                                          │  │
│  └───────────────────────────────────────────────────────────────┘  │
│       │                                                            │
│       ▼                                                            │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │              GRAPH LIFECYCLE                                   │  │
│  │  Extract → Build → Store → Embed → Query → Reason → Evaluate  │  │
│  └───────────────────────────────────────────────────────────────┘  │
│       │                                                            │
│       ▼                                                            │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │              TÍCH HỢP HARNESS & LOOP                           │  │
│  │  Graph là knowledge substrate cho Harness (context)            │  │
│  │  Loop tự động cập nhật Graph khi có document mới               │  │
│  └───────────────────────────────────────────────────────────────┘  │
│       │                                                            │
│       ▼                                                            │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │              EVALUATION + OBSERVABILITY                        │  │
│  │  Coverage · Connectivity · Hallucination · Path Precision      │  │
│  └───────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

## Lộ Trình Học (Cấu Trúc Thư Mục)

Module XIII được chia thành **9 modules chuyên đề** — đồng nhất với convention của `harness/` (mỗi module là `NN-name/README.md`).

```
graph/
├── README.md                    ← BẠN ĐANG Ở ĐÂY — tổng quan + lộ trình + case studies
├── 01-foundations/              ← Nền tảng: graph theory, types, representations, metrics
├── 02-knowledge-graph/          ← Xây dựng KG: entity/relation extraction, ontology, deduplication
├── 03-graph-storage/            ← Lưu trữ & truy vấn: Neo4j, Cypher, indexing, transactions
├── 04-graph-embeddings/         ← Embeddings: Node2Vec, GraphSAGE, hybrid vector+graph search
├── 05-graph-rag/                ← GraphRAG: subgraph retrieval, community summaries, Microsoft pattern
├── 06-graph-reasoning/          ← Suy luận: traversal, path finding, inference rules, temporal reasoning
├── 07-gnn/                      ← GNN: Graph Neural Networks, link prediction, classification
├── 08-graph-workflow/           ← Workflow: pipeline ETL, incremental updates, versioning
└── 09-evaluation/               ← Đánh giá: coverage, hallucination, path precision, benchmarks
```

> Mỗi thư mục chứa một `README.md` — đồng nhất với convention của `harness/` và `loop/`.

### Lộ Trình Đề Xuất

```
Bước 1: Đọc README.md này + GRAPH_ENGINEERING.md để hiểu bối cảnh
   ↓
Bước 2: 01-foundations/ — nắm graph types, representations, metrics cơ bản
   ↓
Bước 3: 02-knowledge-graph/ — học cách trích xuất entities/relations, thiết kế ontology
   ↓
Bước 4: 03-graph-storage/ — chọn DB, viết Cypher, indexing
   ↓
Bước 5: 04-graph-embeddings/ + 05-graph-rag/ — embeddings + GraphRAG pipeline
   ↓
Bước 6: 06-graph-reasoning/ + 07-gnn/ — suy luận nâng cao, GNN
   ↓
Bước 7: 08-graph-workflow/ + 09-evaluation/ — pipeline production + đánh giá
```

| Bạn muốn... | Đọc |
|-------------|-----|
| Hiểu graph là gì, các loại graph, metrics | [01-foundations](01-foundations/) |
| Trích xuất Knowledge Graph từ documents | [02-knowledge-graph](02-knowledge-graph/) |
| Chọn DB, lưu và truy vấn graph | [03-graph-storage](03-graph-storage/) |
| Kết hợp vector + graph embeddings | [04-graph-embeddings](04-graph-embeddings/) |
| Xây GraphRAG pipeline hoàn chỉnh | [05-graph-rag](05-graph-rag/) |
| Multi-hop reasoning, path finding | [06-graph-reasoning](06-graph-reasoning/) |
| Dùng GNN cho link prediction/classification | [07-gnn](07-gnn/) |
| Pipeline ETL, cập nhật incremental | [08-graph-workflow](08-graph-workflow/) |
| Đo chất lượng graph & GraphRAG | [09-evaluation](09-evaluation/) |

---

## Case Studies Thực Tế

### 1. Microsoft GraphRAG — Global Sensemaking

GraphRAG của Microsoft là **reference implementation** cho toàn bộ track này:

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
                      - Local Search (entity-centric, 1-2 hops)
                      - Global Search (community summaries, map-reduce)
```

| Loop | Pattern | Kết quả |
|------|---------|---------|
| Entity Extraction | LLM + gleaning loop | Extract 3-5× nhiều entities hơn single-pass |
| Community Detection | Leiden algorithm | Tự động nhóm entities thành communities có ý nghĩa |
| Global Search | Map-reduce over community summaries | Win rate 70% vs vanilla RAG trên global Q&A |
| Local Search | Entity → neighbors → context | Chính xác cho factoid + multi-hop queries |

### 2. Neo4j + LangChain — Enterprise Stack

Stack production phổ biến nhất 2025-2026:

- **Construction**: `LLMGraphTransformer` (LangChain) → `Neo4jGraph.add_graph_documents()`
- **Query**: `GraphCypherQAChain` → LLM sinh Cypher từ natural language
- **Hybrid**: Vector index trên `Document` nodes + graph traversal trên `Person/Project` nodes
- **Scale**: Neo4j Aura / self-hosted cluster, billions of nodes

### 3. Trajectory as Graph — DeepSeek Pattern

DeepSeek Harness không lưu trajectory dạng flat log — mà dạng **event graph**: mỗi tool call là node, dependencies là edges → cho phép fork/replay như git branches. Chi tiết: [`harness/03-update-memory-store/trajectory-fork-replay.md`](../harness/03-update-memory-store/trajectory-fork-replay.md). Đây chính là **graph thinking** áp dụng cho agent execution.

### 4. Codebase Knowledge Graph

Ứng dụng graph cho AI coding:

```
File ─[DEFINES]→ Function ─[CALLS]→ Function ─[TESTED_BY]→ TestFile
  │                │                     │
  └[IMPORTS]→ Module  └[USES]→ Class ─[INHERITS]→ BaseClass
```

Dùng để: "hàm này được gọi ở đâu?", "thay đổi file này ảnh hưởng gì?", "test nào cover function này?" — mà vector search không trả lời được.

---

## Tài Liệu Tham Khảo

### Bài Viết & Nguồn

- [Microsoft Research — GraphRAG: Unlocking LLM discovery on narrative private data](https://microsoft.github.io/graphrag/) — paper + open-source implementation
- [Neo4j — GraphRAG Use Cases](https://neo4j.com/use-cases/knowledge-graph/) — enterprise patterns
- [LangChain — Graph QA](https://python.langchain.com/docs/use_cases/graph/) — Cypher QA chains
- [LlamaIndex — Property Graph Index](https://docs.llamaindex.ai/en/stable/module_guides/indexing/lpg_index_guide/) — LPG + retrievers
- [DeepSeek Harness — Micro-Kernel & Trajectory Graph](../harness/07-workflow/cordis-kernel-plugin.md) — event graph pattern
- [Stanford CS224W — Machine Learning with Graphs](http://web.stanford.edu/class/cs224w/) — GNN foundations

### Frameworks & Tools

- **graphrag** (Microsoft) — `pip install graphrag` — end-to-end GraphRAG pipeline
- **Neo4j** — `docker run neo4j:5` — graph DB + Cypher + GDS library
- **NetworkX / igraph** — local graph algorithms & prototyping
- **PyG / DGL** — GNN training & inference
- **Kuzu** — embedded graph DB, Python-native

### Datasets & Benchmarks

- **HotpotQA / 2WikiMultihopQA** — multi-hop QA benchmarks
- **FB15k-237 / WN18RR** — knowledge graph completion benchmarks
- **OGB (Open Graph Benchmark)** — large-scale GNN benchmarks

Chi tiết từng module: [01-foundations](01-foundations/) → [09-evaluation](09-evaluation/).

---

> **"Knowledge is not a pile of chunks. It's a web of relationships. Graph Engineering is how you weave that web."**

---

*Bài viết thuộc [AI Coding Skills Framework](../) — Module XIII: Graph Engineering*
