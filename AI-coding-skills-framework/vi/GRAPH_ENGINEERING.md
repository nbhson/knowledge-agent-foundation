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

> Phần này giải thích xuất phát điểm của tài liệu: vì sao chỉ có vector search là chưa đủ, và graph bổ sung thứ gì đó.

Thời RAG (2023-2025) đã chứng minh một điều: **chỉ cần đưa đúng context, model nhỏ cũng có thể vượt model lớn**. (RAG = Retrieval-Augmented Generation — kỹ thuật "tìm tư liệu rồi mới trả lời"; context = các đoạn tư liệu nhét vào prompt.) Nhưng RAG chạy bằng vector search có một điểm mù đáng chú ý: nó chỉ tìm được **"đoạn văn giống câu hỏi"** — chứ chưa thấy được **"mối quan hệ giữa các thực thể"**. (Vector search = so độ giống về ý nghĩa giữa câu hỏi và đoạn văn bằng vector — "tấm thẻ" số học của mỗi đoạn văn.)

**Ví dụ:**
- Hỏi: *"Ai là người phê duyệt hợp đồng của dự án X, và người đó báo cáo cho ai?"*
- Vector RAG: tìm được chunk chứa "dự án X" nhưng **không nối** được `Người phê duyệt → Quản lý cấp trên` nếu 2 thông tin nằm ở 2 documents khác nhau.
- Graph RAG: duyệt `Project X —[approved_by]→ Person A —[reports_to]→ Person B` → trả lời chính xác với **citation path**. (citation path = "đường dẫn chứng minh" — chuỗi quan hệ cho thấy câu trả lời lấy từ đâu.)

### Bối Cảnh

Năm 2024, Microsoft Research công bố **GraphRAG**: dùng LLM trích xuất Knowledge Graph từ toàn bộ corpus, rồi community detection + hierarchical summarization. (corpus = toàn bộ kho tài liệu; community detection = tự động chia đồ thị thành các nhóm liên kết chặt; hierarchical summarization = tóm tắt từng nhóm, rồi tóm tắt lại của các nhóm.) Kết quả: **tăng 30-40% comprehensiveness và diversity** so với vanilla RAG trên các câu hỏi tổng hợp (global sensemaking). (vanilla RAG = RAG bản gốc chỉ dùng vector; comprehensiveness = độ bao quát; global sensemaking = hiểu ý chính của cả kho tài liệu.)

Cùng lúc, Neo4j, NebulaGraph và FalkorDB đưa graph database vào stack AI production. Tri thức dạng đồ thị từ "có thì tốt" thành **lớp nền bắt buộc** cho agent cần suy luận nhiều bước.

### Mục Đích

Tài liệu này giúp bạn có cái nhìn toàn diện về Graph Engineering:

- Định nghĩa, triết lý, và so sánh với Vector/RAG thuần
- Phân tích 3 giai đoạn tiến hoá: Keyword → Vector → Graph
- 7 thành phần cốt lõi của hệ thống graph
- Mapping 7 components → 9 modules thực hành trong `graph/`
- Case studies: Microsoft GraphRAG, Neo4j + LangChain, DeepSeek Knowledge Graph
- Nguyên tắc thiết kế, best practices, và roadmap 2026-2028

> **Tóm gọn 1 câu:** Graph Engineering là kỹ thuật xây "bản đồ quan hệ" cho agent, giúp trả lời được câu hỏi nhiều bước mà vector search bó tay.

---

## 2. Graph Engineering Là Gì?

> Phần này định nghĩa thuật ngữ chính và cho biết nó khác gì vector search mà bạn đã biết.

### Định Nghĩa

**Graph Engineering** là cách xây dựng và vận hành **hệ tri thức dạng đồ thị** làm nền cho AI Agents — từ trích xuất thực thể/quan hệ, lưu trữ đồ thị, embeddings, truy vấn, suy luận, tới ghép vào pipeline RAG/Workflow.

Nói đơn giản:
- **Vector DB** trả lời: *"Đoạn nào giống câu hỏi nhất?"*
- **Graph DB** trả lời: *"Thực thể nào liên quan, qua bao nhiêu bước, với độ tin cậy bao nhiêu?"*
- **Graph Engineering** kết hợp cả hai để trả lời: *"Câu trả lời đúng nhất, có giải thích được, với đường dẫn chứng minh."*

### Triết Lý Cốt Lõi

> *"Mỗi khi LLM hallucinate vì thiếu liên kết, bạn không viết prompt dài hơn — bạn xây một cạnh (edge) mới trong đồ thị."*

1. **Relationships over Chunks**: tri thức thật nằm ở **quan hệ**, không nằm ở đoạn văn lẻ. Chunking xé nhỏ văn bản; graph **nối chúng lại**.
2. **Structure over Similarity**: Similarity tìm cái giống; structure tìm **cái liên quan qua trung gian** (multi-hop).
3. **Explainability over Black-box**: Mỗi câu trả lời có thể truy về **path** trong đồ thị — audit được, citation được. (black-box = hộp đen: ra kết quả mà không giải thích được vì sao.)

### So Sánh Với Các Paradigm Khác

**Cách đọc bảng này:** mỗi cột là một công nghệ tìm kiếm; mỗi hàng là một khía cạnh so sánh. Ví dụ, hàng "Multi-hop" cho biết khả năng trả lời câu hỏi cần nối 2+ bước quan hệ: BM25 và vector đều yếu, chỉ graph làm tốt.

| Khía cạnh | Keyword Search (BM25) | Vector Search (RAG) | Graph Engineering |
|-----------|----------------------|---------------------|-------------------|
| **Focus** | Từ khóa chính xác | Ý nghĩa ngữ nghĩa | Thực thể + quan hệ + suy luận |
| **Đơn vị** | Document / Chunk | Chunk embedding | Node / Edge / Path / Community |
| **Truy vấn** | `MATCH keyword` | `cosine(query, chunk)` | `TRAVERSE / SHORTEST_PATH / COMMUNITY` |
| **Multi-hop** | ❌ Không | ❌ Yếu | ✅ Mạnh (2-6 hops) |
| **Explainability** | Thấp | Thấp | Cao (path + subgraph) |
| **Cập nhật** | Re-index | Re-embed | Thêm node/edge (incremental) |
| **Ví dụ** | Tìm "BHYT" | Tìm "bảo hiểm y tế ≈ BHYT" | `BHYT —covers→ Bệnh tim —treated_at→ BV Chợ Rẫy` |

> **Insight:** Graph không thay thế Vector — Graph **bọc ngoài và khuếch đại** Vector. Combo hiệu quả nhất là **Hybrid: Vector lo phần recall, Graph lo phần precision + reasoning**. (recall = tìm được nhiều kết quả liên quan, ít bỏ sót; precision = kết quả trả về ít rác; reasoning = suy luận nhiều bước.)

> **Tóm gọn 1 câu:** Graph Engineering = xây và vận hành đồ thị tri thức, kết hợp với vector search để câu trả lời vừa đúng vừa giải thích được bằng đường dẫn.

---

## 3. Ba Giai Đoạn Tiến Hóa Của Retrieval

> Phần này cho thấy retrieval (tìm kiếm tư liệu) tiến hóa qua 3 chặng — và vì sao chặng sau không bỏ được chặng trước.

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

Mỗi chặng **kế tiếp**, không thay thế:
- Bạn vẫn cần **BM25** cho exact match (mã hợp đồng, số hiệu). (exact match = tìm đúng y chữ, không chấp nhận sai một ký tự.)
- Bạn vẫn cần **Vector** cho semantic recall (paraphrase, synonym). (semantic recall = tìm được đoạn văn nói cách khác nhưng cùng nghĩa.)
- Bạn cần thêm **Graph** cho multi-hop, aggregation, và global sensemaking. (multi-hop = nối 2+ bước quan hệ; aggregation = gộp số liệu từ nhiều nguồn; global sensemaking = rút ý chính của cả kho.)

> **Tóm gọn 1 câu:** Keyword, vector, graph là ba tầng chồng lên nhau: giữ BM25 cho từ khóa chính xác, vector cho câu diễn đạt khác, và chỉ thêm graph khi cần suy luận nhiều bước.

---

## 4. Tại Sao Graph Engineering Quan Trọng?

> Phần này nêu 5 lý do cụ thể kèm số liệu: từ giới hạn của chunking tới việc cập nhật tri thức hằng ngày.

### 4.1. Vượt Qua Giới Hạn Của Chunking

Vector RAG phụ thuộc vào chunking. (chunking = cắt văn bản thành từng khúc nhỏ để nạp vào model.) Nếu 2 sự thật nằm ở 2 chunks khác nhau và không có chunk nào chứa cả hai → RAG **không bao giờ** trả lời đúng câu hỏi nối chúng. Graph trích xuất entities/relations **trước khi** chunking phá vỡ liên kết. (entities/relations = thực thể và quan hệ — "người, dự án, hợp đồng" và "ai làm gì với ai".)

### 4.2. Global Sensemaking vs Local Lookup

Nghiên cứu Microsoft GraphRAG (2024):

**Cách đọc bảng này:** cột giữa và cột phải là kết quả của hai công nghệ với cùng một dạng câu hỏi. Ví dụ, câu hỏi global (tổng hợp cả kho) thì vector RAG yếu, GraphRAG vượt trội.

| Loại câu hỏi | Vector RAG | GraphRAG |
|--------------|-----------|----------|
| Local: "Điều 5 của hợp đồng X nói gì?" | ✅ Tốt | ✅ Tốt |
| Global: "Chủ đề chính nào lặp lại trong toàn bộ 1000 tài liệu này?" | ❌ Yếu | ✅ Vượt trội (+35% comprehensiveness) |
| Multi-hop: "Dự án X do ai duyệt và người đó quản lý dự án nào khác?" | ❌ Hallucinate | ✅ Chính xác với path |

### 4.3. Giảm Hallucination Có Kiểm Chứng

Graph cung cấp **grounding path**: mỗi edge có `source_document`, `confidence`, `timestamp`. (hallucination = model bịa ra thông tin không có thật; grounding path = đường dẫn neo câu trả lời vào tư liệu thật.) LLM phải đi theo path thay vì bịa. Microsoft báo cáo giảm **25-30% hallucination** khi thay vanilla RAG bằng GraphRAG trên benchmark QA. (benchmark QA = bộ câu hỏi kiểm tra chuẩn.)

### 4.4. Incremental Knowledge Updates

- Vector DB: cập nhật 1 tài liệu → re-chunk + re-embed nhiều chunks, khó giữ consistency. (re-embed = tính lại vector cho các đoạn; consistency = tính nhất quán giữa các dữ liệu đã lưu.)
- Graph DB: cập nhật 1 sự kiện → thêm/sửa 1 node/edge, **không ảnh hưởng** phần còn lại của đồ thị. Phù hợp cho enterprise knowledge base thay đổi hàng ngày.

### 4.5. Nền Tảng Cho Agent Reasoning

Agent cần **plan → retrieve → reason → act**. (lập kế hoạch → tìm tư liệu → suy luận → hành động.) Graph cung cấp:
- **Planning**: duyệt dependencies giữa tasks (`Task A —blocks→ Task B`) — biết việc nào chặn việc nào.
- **Reasoning**: path finding, community detection để suy luận gián tiếp — đi theo con đường quan hệ để kết luận điều chưa viết ra.
- **Memory**: lưu episodic memory dạng graph (`User —prefers→ Dark Mode —since→ 2025-11-01`) — ghi nhớ trải nghiệm từng lần tương tác với người dùng.

> **Tóm gọn 1 câu:** Graph đáng giá vì nó vượt giới hạn chunking, trả lời câu hỏi tổng hợp cả kho, giảm bịa đặt, cập nhật từng phần được, và cho agent thứ để suy luận.

---

## 5. Các Thành Phần Cốt Lõi Của Graph

> Phần này liệt kê 7 mảnh ghép bắt buộc của một hệ thống graph hoàn chỉnh, và cho biết mỗi mảnh học ở module nào.

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

**Cách đọc bảng này:** cột "#" là số thứ tự; "Thành phần" là mảnh ghép của hệ thống; "Vai trò" là việc nó làm; cột cuối là thư mục trong `graph/` dạy về nó. Ví dụ, thành phần số 1 là node — đơn vị tri thức như "Person", học ở `01-foundations`.

| # | Thành phần | Vai trò | Module tương ứng |
|---|-----------|---------|-----------------|
| 1 | **Entities & Nodes** | Đơn vị tri thức (person, project, doc, concept) | `01-foundations` |
| 2 | **Relations & Edges** | Quan hệ có hướng, có trọng số, có thời gian | `01-foundations`, `02-knowledge-graph` |
| 3 | **Ontology & Schema** | Quy tắc: loại node/edge nào hợp lệ, ràng buộc | `02-knowledge-graph` |
| 4 | **Storage & Query** | Lưu và truy vấn (Cypher, GQL, SPARQL) | `03-graph-storage` |
| 5 | **Embeddings** | Vector hóa node/edge/path cho hybrid search | `04-graph-embeddings` |
| 6 | **Reasoning** | Traversal, shortest path, community, centrality | `06-graph-reasoning` |
| 7 | **GraphRAG** | Kết hợp graph + LLM để generate có grounding | `05-graph-rag` |

> **Tóm gọn 1 câu:** Một hệ graph gồm 7 mảnh: node, edge, schema, kho lưu trữ, embedding, suy luận, GraphRAG — mỗi mảnh tương ứng một module trong `graph/`.

---

## 6. Kiến Trúc Tổng Thể: 7 Components → 9 Modules

> Phần này ghép 7 thành phần ở trên thành sơ đồ hoàn chỉnh và chỉ ra dòng chảy dữ liệu giữa harness, graph, loop.

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

(Đọc sơ đồ: harness = bộ khung cho 1 lần chạy agent; graph = lớp tri thức nằm dưới; loop = bộ hẹn giờ chạy nhiều lần. Dòng "Flow đầy đủ" là đường đi của dữ liệu: tài liệu → xây graph → lưu → nhận câu hỏi → GraphRAG lấy tư liệu → ghép context → LLM trả lời kèm chứng minh.)

> **Tóm gọn 1 câu:** Harness cấp công cụ cho 1 lần chạy, graph cấp tri thức, loop điều phối nhiều lần chạy — ba tầng phối hợp theo đúng sơ đồ trên.

---

## 7. Case Studies

> Phần này kể 3 ví dụ thật đã chạy: Microsoft GraphRAG, Neo4j + LangChain, và DeepSeek — để thấy nguyên lý ở trên dùng ngoài đời như thế nào.

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

**Kết quả:** Trên benchmark Q&A tổng hợp từ podcast transcripts + news articles, GraphRAG đạt **win rate 70%** so với vanilla RAG khi đánh giá bởi LLM judge (comprehensiveness, diversity, empowerment). (win rate = tỉ lệ thắng; LLM judge = dùng một LLM khác làm giám khảo chấm điểm.)

**Bài học:** Đầu tư vào **pre-processing graph construction** đắt hơn (tốn LLM calls), nhưng payoff lớn cho câu hỏi phức tạp/long-tail. (long-tail = câu hỏi hiếm gặp, không phổ thông.)

### 7.2. Neo4j + LangChain — Enterprise Knowledge Graph

Stack production phổ biến:

> 📄 **Code ví dụ:** [`examples/01-7-2-neo4j-langchain-enterprise-knowledge-graph.py`](examples/01-7-2-neo4j-langchain-enterprise-knowledge-graph.py)

### 7.3. DeepSeek Harness — Trajectory as Graph

DeepSeek lưu trajectory của agent **không phải** dạng flat log, mà dạng **event graph**: mỗi tool call là node, dependencies là edges → cho phép fork/replay nhánh như git branches (`harness/03-update-memory-store/trajectory-fork-replay.md`). (trajectory = dòng thời gian các bước agent đã đi; flat log = nhật ký dạng dòng phẳng; fork/replay = tách nhánh và chạy lại như git.) Pattern này chính là **graph thinking** áp dụng cho agent execution.

### Bài Học Chung

1. **Graph construction là bottleneck** — chất lượng entity/relation extraction quyết định toàn bộ pipeline phía sau. (bottleneck = nút thắt cổ chai.)
2. **Hybrid luôn thắng** — Vector cho recall, Graph cho reasoning. Đừng chọn 1 trong 2.
3. **Schema matter** — không có ontology, graph thành "hairball" không query được. (hairball = búi tóc rối — đồ thị chằng chịt mà không truy vấn nổi.)

> **Tóm gọn 1 câu:** Ba case thật dạy cùng một bài: đầu tư vào xây graph bằng giá, luôn dùng hybrid vector + graph, và có schema ngay từ đầu.

---

## 8. Nguyên Tắc Thiết Kế Graph

> Phần này cho ra 5 nguyên tắc thiết kế và 8 "điều răn" — checklist để bạn tự kiểm tra hệ thống graph của mình.

### 8.1. Nguyên Tắc SOLID Cho Graph

**Cách đọc bảng này:** cột trái là nguyên tắc SOLID (5 nguyên tắc thiết kế phần mềm kinh điển); cột phải là cách áp nguyên tắc đó cho đồ thị. Ví dụ, "Single Responsibility" nghĩa là mỗi loại node chỉ đại diện cho một loại thứ — Person không lẫn với Organization.

| Nguyên tắc | Áp dụng cho Graph |
|-----------|-------------------|
| **Single Responsibility** | Mỗi node type làm 1 việc (Person ≠ Organization ≠ Document) |
| **Open/Closed** | Thêm node/edge type mới không sửa schema cũ (extend, không modify) |
| **Liskov Substitution** | Subgraph phải thay thế được cho full graph trong test |
| **Interface Segregation** | Tách query interfaces: read-only vs write vs admin |
| **Dependency Inversion** | Code phụ thuộc vào Graph abstraction, không phụ thuộc Neo4j cụ thể |

### 8.2. The 8 Commandments of Graph Engineering

(Đọc danh sách này như 8 điều răn: mỗi điều là một luật nên tuân theo. Ví dụ điều 2 nghĩa là mọi quan hệ phải ghi rõ lấy từ nguồn nào, chắc tới đâu, tại thời điểm nào — để câu trả lời kiểm chứng được.)

1. **Schema First, Data Second** — định nghĩa ontology trước khi ingest. (ingest = nạp dữ liệu vào hệ thống.)
2. **Every Edge Has Provenance** — mỗi quan hệ phải có `source`, `confidence`, `timestamp`. (provenance = nguồn gốc, truy ngược được.)
3. **Incremental Over Batch** — cập nhật graph theo event, không rebuild toàn bộ. (rebuild = xây lại từ đầu.)
4. **Hybrid Search By Default** — luôn kết hợp vector + graph, không chọn 1.
5. **Paths Are Citations** — mỗi câu trả lời phải kèm path có thể verify. (verify = đối chứng được.)
6. **Community Before Detail** — summarize communities trước khi đi vào chi tiết local.
7. **Temporal Awareness** — quan hệ có thời gian (`valid_from`, `valid_until`), không phải vĩnh viễn.
8. **Evaluate With Graphs** — đo coverage, connectivity, hallucination rate, không chỉ BLEU/ROUGE. (coverage = độ phủ; connectivity = mức liên thông; BLEU/ROUGE = thước đo điểm văn bản thông thường.)

### 8.3. Graph Design Pattern

> 📄 **Code ví dụ:** [`examples/02-8-3-graph-design-pattern.py`](examples/02-8-3-graph-design-pattern.py)

> **Tóm gọn 1 câu:** Thiết kế graph bằng đúng 5 nguyên tắc SOLID và 8 điều răn — quan trọng nhất: định schema trước, mọi quan hệ ghi nguồn, luôn hybrid vector + graph.

---

## 9. Best Practices

> Phần này là checklist "nên làm" theo từng công đoạn: xây graph, lưu trữ, tìm kiếm, bảo vệ, kiểm thử.

### 9.1. Graph Construction
- ✅ Dùng LLM + rule-based hybrid cho extraction (LLM cho recall, rules cho precision). (rule-based = dùng luật cứng do người viết, ví dụ regex bắt mã "C-2024".)
- ✅ Deduplicate entities bằng embedding similarity + canonical name resolution. (deduplicate = gộp trùng lặp — "Alice N." và "Alice Nguyen" là một người; canonical name = tên chuẩn được chọn.)
- ✅ Batch extraction với checkpoint, không ingest 1 lần toàn bộ corpus lớn. (checkpoint = mốc lưu lại để hỏng chỗ nào chạy lại đúng chỗ đó.)

### 9.2. Storage & Query
- ✅ Index trên `label + property` hay dùng (ví dụ: `Person.name`). (index = mục lục giúp tra nhanh không phải quét toàn bộ.)
- ✅ Giới hạn `max_hops` (thường 2-3) để tránh explosion. (explosion = số kết quả nổ tung lên theo cấp số nhân.)
- ✅ Dùng parameterized Cypher, không string concatenation. (parameterized = truyền tham số an toàn; string concatenation = nối chuỗi thủ công — dễ dính lỗi bảo mật SQL injection.)

### 9.3. Retrieval
- ✅ Retrieve **subgraph** (nodes + edges), không chỉ nodes cô lập. (subgraph = một vùng nhỏ của đồ thị.)
- ✅ Re-rank paths bằng cross-encoder giống như re-rank chunks. (re-rank = xếp lại hạng theo độ liên quan chính xác hơn; cross-encoder = model chấm điểm cặp câu hỏi–kết quả.)
- ✅ Tóm tắt community trước khi trả về chi tiết local.

### 9.4. Guardrails
- ✅ Validate ontology trước khi write (không cho `Person -[EATS]-> Project`). (validate = kiểm tra tính hợp lệ trước khi ghi.)
- ✅ Access control trên subgraph level (user chỉ thấy subgraph được phép). (access control = phân quyền truy cập.)
- ✅ Temporal versioning: soft-delete edge bằng `valid_until`, không xóa cứng. (soft-delete = xoá mềm — đánh dấu hết hiệu lực chứ không xoá dữ liệu.)

### 9.5. Testing Graph
- ✅ Unit test: từng extractor, từng Cypher query. (unit test = kiểm thử từng đơn vị nhỏ.)
- ✅ Integration test: ingest → query → retrieve round-trip. (integration test = kiểm thử cả chuỗi ghép lại.)
- ✅ Chaos test: thêm node/edge rác, đo retrieval robustness. (chaos test = cố nhồi dữ liệu bậy để xem hệ có chịu nổi không.)

> **Tóm gọn 1 câu:** Làm đúng 5 nhóm checklist: trích xuất có checkpoint, query có index và giới hạn hops, tìm kiếm lấy subgraph, ghi dữ liệu qua guardrails, và kiểm thử đủ 3 cấp.

---

## 10. Công Cụ và Framework

> Phần này chọn giúp bạn công cụ theo từng nhu cầu: database nào, framework nào, thư viện embedding/GNN nào.

### 10.1. Graph Databases

**Cách đọc bảng này:** cột "Type" là kiểu database; "Scale" là cỡ dữ liệu nó chịu được; "Best For" là tình huống nên chọn nó. Ví dụ, thử nghiệm trên máy cá nhân thì chọn Kuzu hoặc NetworkX, còn production hàng nghìn người dùng thì chọn Neo4j.

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

**Cách đọc bảng này:** đây là các thư viện biến node/đồ thị thành vector để học máy. GNN = Graph Neural Network — mạng nơ-ron chạy trên đồ thị. Ví dụ, muốn học "hai node nào có khả năng nối nhau" thì dùng Node2Vec hoặc GraphSAGE.

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

> **Tóm gọn 1 câu:** Chọn công cụ theo quy mô: Kuzu/NetworkX để học và thử, Neo4j để lên production, GraphRAG/LangChain làm tầng LLM.

---

## 11. Tương Lai Của Graph Engineering

> Phần này nhìn trước 2025-2028: hướng đi của GraphRAG, khó khăn còn tồn tại, và lời khuyên cho người bắt đầu.

### 11.1. Xu Hướng 2025-2028

## GraphRAG — Cập nhật 2026

> Microsoft GraphRAG (2024-2025): dùng knowledge graph để enhance RAG. Query phức tạp (multi-hop) tốt hơn vector-only RAG.
> Ref: https://microsoft.github.io/graphrag/

### Developments quan trọng 2025-2026:

**Cách đọc bảng này:** cột "Năm" là mốc thời gian ra đời; cột "Phát triển" là tên sự kiện/công nghệ; cột "Chi tiết" giải thích ngắn gọn. Ví dụ, hàng đầu tiên: LazyGraphRAG giúp chi phí index (chuẩn bị dữ liệu) rẻ bằng vector RAG.

| Năm | Phát triển | Chi tiết |
|-----|-----------|---------|
| 2024-2025 | **LazyGraphRAG** (Microsoft) | LLM summarisation defer tới query time → indexing cost ngang vector RAG, quality ngang full GraphRAG, query cost thấp hơn ~700×. Đã tích hợp Microsoft Discovery (2025) và Azure Local. |
| 2025 | **LightRAG** (HKUDS, EMNLP 2025) | Dual-layer graph + vector index, incremental update thay vì re-index toàn bộ, cost ~1/100 full GraphRAG. |
| 2025 | **GraphRAG-Bench** (Microsoft, 06/2025) | Benchmark hệ thống: single-hop vanilla RAG thắng; multi-hop và global GraphRAG thắng rõ. |
| 2026 | **Gartner** "Top Trends in D&A 2026" | GraphRAG được nêu như path cho complex cases mà high-accuracy RAG thuần không đủ. |
| 2026 | **Knowledge Graph Market** | 1.48 tỷ USD (2025) → 2.04 tỷ USD (2026). GraphRAG chuyển từ "enterprise luxury" → baseline production. |

### Khi nào dùng GraphRAG vs LazyGraphRAG vs LightRAG:

**Cách đọc bảng này:** cột trái là hoàn cảnh của bạn; cột phải là lựa chọn khuyến nghị. Ví dụ, tài liệu thay đổi liên tục thì chọn LightRAG vì nó cập nhật tăng dần được.

| Trường hợp | Khuyến nghị |
|-----------|-------------|
| Cần global/sensemaking query trên toàn bộ corpus | GraphRAG nguyên gốc |
| Corpus rất lớn, cần index rẻ, query phức tạp | LazyGraphRAG hoặc LightRAG |
| Cần incremental update (document thay đổi liên tục) | LightRAG |
| Chỉ cần single-hop, factoid queries | Vanilla RAG (không cần graph) |

(Thêm một bảng dự báo: mỗi hàng là một mốc năm và việc dự kiến sẽ phổ biến. Ví dụ, 2027 dự báo mọi quan hệ sẽ có thời hạn hiệu lực.)

| Năm | Xu hướng |
|-----|---------|
| **2026** | GraphRAG trở thành default cho enterprise RAG (thay vì vanilla vector RAG) |
| **2026** | Graph databases thêm vector index native → single DB cho hybrid search |
| **2027** | Temporal graphs phổ biến: mọi edge có lifecycle, query theo thời gian |
| **2027** | GNN + LLM fusion: LLM gọi GNN như tool để reasoning trên graph lớn |
| **2028** | Auto-ontology: LLM tự đề xuất và evolve schema từ data |
| **2028** | Federated graphs: nhiều org chia sẻ subgraph mà không chia sẻ raw data |

### 11.2. Thách Thức

- **Construction cost**: LLM extraction tốn token, cần cheaper distilled extractors. (distilled = model bản nén nhỏ, rẻ hơn.)
- **Schema drift**: ontology thay đổi theo thời gian, migration phức tạp. (schema drift = schema "trôi" khỏi thiết kế ban đầu; migration = chuyển đổi dữ liệu sang cấu trúc mới.)
- **Evaluation**: chưa có benchmark chuẩn cho graph correctness như SWE-bench cho coding.

### 11.3. Lời Khuyên

> **Bắt đầu với 100 documents, 3 node types, 5 edge types. Đừng cố xây đồ thị cỡ Wikipedia ngay từ ngày đầu nhé.**

> **Tóm gọn 1 câu:** Xu hướng 2026 là GraphRAG thành mặc định, nhưng chi phí xây graph và thiếu benchmark vẫn là bài toán chưa giải — nên cứ bắt đầu nhỏ.

---

## 12. Tài Liệu Tham Khảo

> Phần này là danh sách nguồn để đọc thêm: papers nghiên cứu, tài liệu công cụ, cộng đồng, và khóa học.

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
