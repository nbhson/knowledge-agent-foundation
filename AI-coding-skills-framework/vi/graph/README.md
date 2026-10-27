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

Hãy tưởng tượng thế này: bạn có cả một kho tài liệu công ty dày tới 10.000 trang — nào là hợp đồng, báo cáo, sơ đồ tổ chức, email qua lại đủ kiểu. Rồi một hôm bạn hỏi con chatbot RAG:

> *"Hợp đồng dự án Phoenix do ai phê duyệt, và người đó từng quản lý dự án nào liên quan đến AI?"*

**Vector RAG** loay hoay lôi ra được 5 mẩu văn bản có chữ "Phoenix" — khổ nỗi, chẳng mẩu nào nói cùng lúc cả `người phê duyệt` lẫn `dự án AI`. Bí quá, nó đành đoán bừa một cái tên cho xong.

**GraphRAG** thì chơi kiểu khác hẳn. Nó đã bóc sẵn mối quan hệ từ trước:

```
(Phoenix) —[APPROVED_BY]→ (Nguyễn Văn A) —[MANAGED]→ (Project Atlas - AI Platform)
                  └—[REPORTS_TO]→ (Trần Thị B - CTO)
```

Chỉ cần một câu truy vấn `TRAVERSE 2 hops` là ra đáp án đúng phóc, **kèm luôn đường đi chứng minh tại sao đúng** — khỏi đoán mò, khỏi bịa.

> *"Vector search tìm đoạn văn giống nhau. Graph search tìm mối quan hệ ẩn sau đoạn văn."*
> — **Microsoft Research, GraphRAG (2024)**

> *"Knowledge is not a pile of chunks. It's a web of relationships."*

Nói dễ hiểu, **Graph Engineering** là cách mình thiết kế **substrate tri thức dạng đồ thị** — để AI không chỉ *đi tìm* thông tin, mà còn biết *lần theo sợi dây* suy luận qua nhiều bước, giải thích được vì sao, trích nguồn được rõ ràng.

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

**Analogies**: Nói nôm na cho dễ hình dung, Graph Engineering giống như **cái bản đồ thành phố**. Tìm bằng vector thì giống như hỏi "quanh đây có quán ăn nào không" — nó chỉ cho bạn cái tên. Còn tìm bằng graph thì nó chỉ luôn "quán này của ai mở, chủ quán còn mở thêm quán nào nữa, đường nào đi tới đó nhanh nhất". Ngược lại, **chỉ cắt nhỏ văn bản (chunking thuần)** thì giống như xé tấm bản đồ ra thành từng mảnh vụn, tới lúc cần tìm đường lại loay hoay ghép lại.

**Nếu bỏ qua**: Nói thật, con agent vẫn trả lời ngon ơ mấy câu đơn giản, nhưng cứ gặp câu hỏi lòng vòng nhiều bước là lại bịa, hỏi "sao mày biết" thì ú ớ không chỉ được nguồn, muốn thêm tài liệu mới lại phải làm lại từ đầu rất cực.

## Tổng Quan

Hiểu đơn giản, **Graph Engineering** là chuyện mình xây hẳn một **hệ tri thức dạng đồ thị** để AI agent có chỗ lưu, chỗ hỏi, chỗ suy luận cho đàng hoàng — nào là đi nhiều bước (multi-hop traversal), gom nhóm (community detection), trả lời có trích nguồn đàng hoàng.

Nó khác với Module 01 (Retrieve Memory & Knowledge) ở chỗ: Module 01 lo chuyện tìm trên mấy đoạn văn bản cắt nhỏ bằng vector/hybrid search, còn ở đây mình chơi với **đồ thị tri thức** hẳn hoi: mỗi sự thật là một cạnh nối (triple), mỗi câu trả lời là một hành trình (path), và mỗi bản tóm tắt là một cụm cộng đồng (community).

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

Module XIII này được chia thành **9 module nhỏ** — cách chia giống hệt bên `harness/` cho dễ theo dõi (mỗi module là một thư mục `NN-name/README.md`).

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

> Mỗi thư mục đều có một file `README.md` riêng — đúng chuẩn như bên `harness/` và `loop/` thôi, nên bạn mở ra là quen ngay.

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

Nói về graph thì phải nhắc tới GraphRAG của Microsoft đầu tiên — đây coi như **bản mẫu chuẩn** cho cả track này:

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

Đây là bộ đồ nghề mà nhiều team đem ra chạy production nhất trong giai đoạn 2025-2026:

- **Construction**: `LLMGraphTransformer` (LangChain) → `Neo4jGraph.add_graph_documents()`
- **Query**: `GraphCypherQAChain` → LLM sinh Cypher từ natural language
- **Hybrid**: Vector index trên `Document` nodes + graph traversal trên `Person/Project` nodes
- **Scale**: Neo4j Aura / self-hosted cluster, billions of nodes

### 3. Trajectory as Graph — DeepSeek Pattern

Team DeepSeek làm một chuyện rất hay: thay vì lưu lịch sử chạy của agent kiểu nhật ký dài lê thê (flat log), họ lưu hẳn thành **đồ thị sự kiện (event graph)**: mỗi lần gọi tool là một nút, mối liên quan giữa các lần gọi là cạnh nối — nhờ vậy mới rẽ nhánh, chạy lại ngon lành như dùng git branch vậy. Bạn xem chi tiết ở đây: [`harness/03-update-memory-store/trajectory-fork-replay.md`](../harness/03-update-memory-store/trajectory-fork-replay.md). Nói chung, đây chính là kiểu **tư duy đồ thị** đem áp thẳng vào cách agent chạy.

### 4. Codebase Knowledge Graph

Còn đây là cách đem graph vào chuyện code để AI hiểu codebase:

```
File ─[DEFINES]→ Function ─[CALLS]→ Function ─[TESTED_BY]→ TestFile
  │                │                     │
  └[IMPORTS]→ Module  └[USES]→ Class ─[INHERITS]→ BaseClass
```

Mấy câu kiểu "hàm này được gọi ở chỗ nào?", "sửa file này thì ảnh hưởng tới đâu?", "test nào đang cover hàm này?" — hỏi kiểu này thì tìm bằng vector chịu chết, chỉ có graph mới lần ra được.

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
