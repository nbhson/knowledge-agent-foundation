# 🔍 05. GraphRAG — Retrieval-Augmented Generation Trên Đồ Thị

> ## 📑 Mục Lục
>
> - [Câu Chuyện Mở Đầu](#câu-chuyện-mở-đầu)
> - [Tại Sao GraphRAG Quan Trọng?](#tại-sao-graphrag-quan-trọng)
> - [Tổng Quan](#tổng-quan)
> - [Nội Dung](#nội-dung)
> - [1. Vanilla RAG vs GraphRAG](#1-vanilla-rag-vs-graphrag)
> - [2. GraphRAG Pipeline Chi Tiết — 6 Bước](#2-graphrag-pipeline-chi-tiết-6-bước)
> - [3. Local Search vs Global Search](#3-local-search-vs-global-search)
> - [4. Community Summarization](#4-community-summarization)
> - [5. Triển Khai GraphRAG Với Python](#5-triển-khai-graphrag-với-python)
> - [6. Khi Nào Dùng GraphRAG?](#6-khi-nào-dùng-graphrag)
> - [7. Labs Thực Hành](#7-labs-thực-hành)
> - [Tài Liệu Tham Khảo](#tài-liệu-tham-khảo)

---

### Câu Chuyện Mở Đầu

Bạn có 1,000 báo cáo tài chính. Bạn hỏi:

> *"Thị trường AI năm 2024 có xu hướng gì nổi bật?"*

**Vanilla RAG**: chunk 1,000 báo cáo (chunk = cắt tài liệu thành đoạn nhỏ) → embed (biến đoạn thành vector) → tìm top-5 chunks giống câu hỏi nhất → đưa vào LLM. Kết quả: 5 đoạn văn rời rạc về "AI trend" nhưng **thiếu bức tranh tổng thể** — mỗi chunk chỉ nói về 1 khía cạnh.

**GraphRAG**: trước khi có câu hỏi, đã trích KG + phát hiện communities (ví dụ: community "AI Investment" gồm 200 entities, community "AI Regulation" gồm 150 entities) + tóm tắt từng community bằng LLM. Khi hỏi, **map-reduce trên community summaries** → trả lời toàn diện với **comprehensiveness + diversity** cao hơn 30-40% (Microsoft, 2024).

**GraphRAG không thay thế RAG. GraphRAG giúp RAG thông minh hơn nhờ khai thác cấu trúc đồ thị.**

> **Tóm gọn 1 câu:** RAG thường lấy 5 đoạn văn rời rạc; GraphRAG tóm tắt trước từng chủ đề rồi gộp lại — nên câu hỏi tổng quan được trả lời đầy đủ hơn.

### Tại Sao GraphRAG Quan Trọng?

> *"Vanilla RAG answers WHERE. GraphRAG answers WHY and HOW, with evidence paths."*
>
> (Dịch: RAG thường trả lời "ở đâu"; GraphRAG trả lời "vì sao" và "như thế nào", kèm đường dẫn bằng chứng.)

> **Cách đọc bảng này:** mỗi dòng là 1 nghiên cứu; cột "Phát Hiện" nói nó đo được điều gì. Ví dụ, dòng 1: với câu hỏi tổng hợp nhiều tài liệu, người chấm là LLM và GraphRAG thắng 70%.

| # | Nghiên Cứu | Phát Hiện |
|---|-----------|-----------|
| 1 | **Microsoft GraphRAG (2024)** | Trên global sensemaking Q&A, GraphRAG win rate **70%** vs vanilla RAG (LLM judge) |
| 2 | **Microsoft GraphRAG (2024)** | Comprehensiveness: GraphRAG **+35%**, Diversity: **+30%** vs baseline |
| 3 | **Anthropic (2025)** | Graph-grounded generation giảm **28% hallucination** trên enterprise QA |

---

## Tổng Quan

Sơ đồ gồm 2 nửa: nửa trên là khâu dựng chỉ mục (chạy 1 lần, offline), nửa dưới là khâu trả lời câu hỏi (chạy mỗi lần người dùng hỏi).

```
                    ┌─────────────────────────────────┐
                    │         INDEXING PIPELINE         │
                    │         (Offline, 1 lần)          │
Documents ──────────►│  Extract KG → Communities →      │
(1K-100K docs)      │  Community Summaries              │
                    └──────────────┬──────────────────┘
                                   │ Graph Index
                    ┌──────────────▼──────────────────┐
                    │       QUERY PIPELINE              │
User Query ────────►│  Local Search  vs  Global Search  │
                    │  (entity-centric)  (community)    │
                    └──────────────┬──────────────────┘
                                   │ Retrieved Context
                    ┌──────────────▼──────────────────┐
                    │     GENERATION (LLM)              │
                    │  Context + Query → Answer + Paths │
                    └─────────────────────────────────┘
```

---

## Nội Dung

> **Cách đọc bảng này:** cột "Chủ đề" là mục con bên dưới; cột "Mô tả" tóm tắt mục đó gồm những gì. Ví dụ, dòng 3 nói: phần Local vs Global dạy 2 chế độ truy vấn của GraphRAG.

| # | Chủ đề | Mô tả |
|---|--------|-------|
| 1 | [Vanilla vs GraphRAG](#1-vanilla-rag-vs-graphrag) | So sánh chi tiết, trade-offs |
| 2 | [Pipeline 6 Bước](#2-graphrag-pipeline-chi-tiết-6-bước) | Từ documents đến answer |
| 3 | [Local vs Global](#3-local-search-vs-global-search) | 2 chế độ truy vấn |
| 4 | [Community Summarization](#4-community-summarization) | Leiden + LLM summarization |
| 5 | [Triển Khai](#5-triển-khai-graphrag-với-python) | Code Python hoàn chỉnh |
| 6 | [Retriever Types & Fusion](#6-retriever-types--fusion) | Text2Cypher, DRIFT, agentic + RRF |
| 7 | [GraphRAG Variants](#7-graphrag-variants-sota) | LightRAG, HippoRAG2, KAG, GRAG |
| 8 | [Khi Nào Dùng](#8-khi-nào-dùng-graphrag) | Decision guide + counter-evidence |
| 9 | [Labs Thực Hành](#9-labs-thực-hành) | Practice |

---

## 1. Vanilla RAG vs GraphRAG

> **Cách đọc bảng này:** so sánh 2 cách theo từng khía cạnh; "Vanilla RAG" = RAG thường; "❌/✅" là yếu/mạnh. Ví dụ, dòng "Global Q&A": hỏi tổng hợp cả kho thì RAG thường yếu, GraphRAG mạnh.

```
┌──────────────────┬──────────────────────────────────┬──────────────────────────────────┐
│ Khía cạnh        │ Vanilla RAG                      │ GraphRAG                         │
├──────────────────┼──────────────────────────────────┼──────────────────────────────────┤
│ Đơn vị index     │ Chunk embeddings (vector DB)     │ Entities + Relations + Communities│
│ Retrieval        │ Cosine similarity top-K          │ Subgraph traversal + community   │
│ Context          │ 5-10 chunks rời rạc              │ Subgraph + community summaries   │
│ Global Q&A       │ ❌ Yếu (không tổng hợp được)     │ ✅ Mạnh (map-reduce summaries)   │
│ Local Q&A        │ ✅ Tốt                           │ ✅ Tốt (entity-centric)          │
│ Multi-hop        │ ❌ Hallucinate                   │ ✅ Path-based, có citation       │
│ Cost (indexing)  │ Thấp (chỉ embed)                 │ Cao (LLM extraction + summary)   │
│ Cost (query)     │ Thấp                             │ Trung bình (traversal + rerank)  │
│ Explainability   │ Thấp (chunks)                    │ Cao (path + subgraph)            │
└──────────────────┴──────────────────────────────────┴──────────────────────────────────┘
```

**Chi phí indexing GraphRAG** đắt hơn (tốn LLM calls để extract + summarize), nhưng là **one-time offline cost**. Query cost tương đương hoặc thấp hơn nhờ context ngắn gọn hơn.

> 📄 **Code ví dụ:** [`examples/01-1-vanilla-rag-vs-graphrag.py`](examples/01-1-vanilla-rag-vs-graphrag.py)

> **Tóm gọn 1 câu:** GraphRAG đắt hơn ở bước dựng chỉ mục, nhưng đổi lại câu trả lời có cấu trúc, có bằng chứng, và xử lý được câu hỏi tổng hợp cả kho.

---

## 2. GraphRAG Pipeline Chi Tiết — 6 Bước

### Bước 1: Document Processing & Chunking

> 📄 **Code ví dụ:** [`examples/02-buoc-1-document-processing-chunking.py`](examples/02-buoc-1-document-processing-chunking.py)

### Bước 2: Entity & Relation Extraction (LLM)

Xem chi tiết: [`02-knowledge-graph`](../02-knowledge-graph/) — dùng gleaning loop `extract_entities` + `extract_relations`.

### Bước 3: Community Detection (Leiden)

> **Khái niệm:** Chia graph thành các **nhóm (communities)** liên kết chặt — giống chia 1000 nhân viên thành các team/phòng ban. Mỗi community = 1 "chủ đề" gom tất cả entities liên quan nhau.
>
> **Tại sao cần?** Truy vấn toàn graph hàng triệu nodes rất đắt. Gom thành nhóm → chỉ cần tóm tắt từng nhóm (Bước 4), truy vấn toàn cục chỉ đọc tóm tắt nhóm thay vì đọc nguyên entities.
>
> Thuật toán **Leiden**: cải tiến của Louvain — nhanh hơn + cho cộng đồng tách biệt rõ hơn. Chi tiết ở §4.1.

### Bước 4: Community Summarization (LLM)

> **Khái niệm:** Với mỗi community (nhóm) tìm được ở Bước 3, dùng **LLM tóm tắt thành 1 đoạn ngắn** mô tả nhóm đó nói về gì.
>
> **Analogies:** Giống "tóm tắt biên bản họp" cho từng team: có 100 team → 100 biên bản ngắn thay vì phải đọc hồ sơ từng người. Khi hỏi "cả công ty đang làm gì?", chỉ cần đọc 100 biên bản đó.
>
> Kết quả: mỗi community có 1 `summary` → lưu vào graph như node/attribute. Chi tiết ở §4.2.

### Bước 5: Retrieval (Local vs Global)

> **Khái niệm:** Truy vấn được chia thành 2 loại:
> - **Local Search** (hỏi chi tiết về 1 thực thể): tìm node→ expand neighbors theo BFS (BFS = duyệt theo vòng: ghé hết node gần trước, rồi mới đi xa) → lấy embeddings + context của nodes liên quan
> - **Global Search** (hỏi tổng quan, so sánh, xu hướng): map- reduce trên **community summaries** — mỗi summary cho LLM, rồi gộp kết quả
>
> **Analogies:** Local = tra cứu hồ sơ 1 người (đọc bạn bè, team, dự án). Global = đọc báo cáo tổng hợp cả công ty (đọc từng phòng ban rồi gộp lại). Chi tiết ở §3.

### Bước 6: Generation (LLM với Graph Context)

> **Khái niệm:** Bước cuối — đưa context (danh sách entities, relations, paths, hoặc summaries) + câu hỏi vào prompt, LLM tạo câu trả lời kèm **nguồn bằng chứng** (các triple/path lấy từ graph).
>
> **Điểm khác RAG thường:** Vì context là **cấu trúc graph** (không phải chuỗi text rời rạc), LLM trả lời theo quan hệ — "Alice thông qua Phoenix nên bạn của Alice là Bob" thay vì "có thể Alice biết Bob".

Toàn bộ pipeline được triển khai chi tiết ở §5.

> **Tóm gọn 1 câu:** 6 bước: cắt tài liệu → trích thực thể/quan hệ → chia cụm → tóm tắt cụm → tìm theo 2 kiểu → LLM trả lời kèm bằng chứng.

---

## 3. Local Search vs Global Search

Đây là **phân biệt cốt lõi** của GraphRAG mà vanilla RAG không có:

> **Cách đọc bảng này:** so sánh 2 chế độ tìm kiếm theo từng dòng. Ví dụ, dòng "Câu hỏi mẫu": hỏi "ai phê duyệt hợp đồng Phoenix?" → Local; hỏi "xu hướng AI 2024?" → Global.

```
┌──────────────────┬──────────────────────────────────┬──────────────────────────────────┐
│                  │ Local Search                     │ Global Search                    │
├──────────────────┼──────────────────────────────────┼──────────────────────────────────┤
│ Câu hỏi mẫu      │ "Ai phê duyệt hợp đồng Phoenix?"│ "Xu hướng AI 2024 là gì?"        │
│ Bắt đầu từ       │ Entities trong query             │ Tất cả community summaries       │
│ Truy vấn         │ Entity → neighbors (1-2 hops)   │ Map-Reduce trên summaries        │
│ Context          │ Subgraph quanh entities          │ Tóm tắt từ nhiều communities     │
│ Phù hợp          │ Factoid, multi-hop, entity Q&A  │ Tổng hợp, thematic, sensemaking  │
│ Tương tự vanilla?│ Có, nhưng có path               │ Không — vanilla RAG không làm được│
└──────────────────┴──────────────────────────────────┴──────────────────────────────────┘
```

### 3.1 Local Search — Entity-Centric

```
Query: "Ai phê duyệt hợp đồng Phoenix?"

1. Extract entities từ query: ["Phoenix", "hợp đồng"]
2. Tìm entities trong KG khớp với query (vector similarity)
3. Traverse 1-2 hops quanh entities đó:
   Phoenix —[BELONGS_TO]→ Contract C-2024 —[APPROVED_BY]→ Alice (confidence: 0.95)
4. Thu thập: nodes + edges + text chunks của entities/relations
5. Re-rank bằng cross-encoder
6. Đưa vào LLM prompt với path
```

### 3.2 Global Search — Community-Based

```
Query: "Xu hướng AI 2024 là gì?"

1. KHÔNG extract entities — query quá chung, không map được vào entity cụ thể
2. Lấy TẤT CẢ community summaries (ví dụ 50 communities)
3. Map: LLM trả lời query DỰA TRÊN từng community summary (parallel)
   - Community "AI Investment" → "Đầu tư AI tăng 40%..."
   - Community "AI Regulation" → "EU AI Act có hiệu lực..."
   - Community "AI in Healthcare" → "AI chẩn đoán tăng..."
4. Reduce: LLM tổng hợp các partial answers thành final answer
5. Mỗi claim có citation về community nguồn
```

> **Tóm gọn 1 câu:** Local = bám vào thực thể trong câu hỏi rồi mở rộng quanh nó; Global = hỏi từng tóm tắt cụm rồi gộp — chọn kiểu theo câu hỏi có thực thể cụ thể hay không.

---

## 4. Community Summarization

### 4.1 Community Detection (Leiden Algorithm)

Leiden là thuật toán phát hiện community tốt nhất hiện tại — cải tiến của Louvain (thuật toán chia cụm kinh điển: gom các node nối chặt với nhau thành một nhóm):

> 📄 **Code ví dụ:** [`examples/03-4-1-community-detection-leiden-algorithm.py`](examples/03-4-1-community-detection-leiden-algorithm.py)

### 4.2 LLM Community Summarization

<details>
<summary>Python Code — Community Summarization (Click để xem)</summary>

> 📄 **Code ví dụ:** [`examples/04-4-2-llm-community-summarization.py`](examples/04-4-2-llm-community-summarization.py)

</details>

### 4.3 Hierarchical Communities

GraphRAG làm **hierarchical clustering**: communities cấp thấp gộp thành communities cấp cao → tạo hierarchy cho global search ở nhiều mức độ chi tiết.

```
Level 0: Toàn bộ graph (1 community)
  └── Level 1: 5 communities lớn (AI, Finance, HR, ...)
        └── Level 2: 20 communities nhỏ (AI-Investment, AI-Regulation, ...)
              └── Level 3: Entities + Relations (leaves)
```

> **Tóm gọn 1 câu:** Leiden chia graph thành nhóm theo chủ đề, LLM tóm tắt từng nhóm, rồi xếp tầng — tầng to cho câu tổng quan, tầng nhỏ cho câu chi tiết.

---

## 5. Triển Khai GraphRAG Với Python

<details>
<summary>Python Code — Complete GraphRAG Pipeline (Click để xem)</summary>

> 📄 **Code ví dụ:** [`examples/05-5-trien-khai-graphrag-voi-python.py`](examples/05-5-trien-khai-graphrag-voi-python.py)

</details>

---

## 6. Retriever Types & Fusion

> **📌 Khái Niệm Cơ Bản:**
> **Retriever** ở đây nghĩa như "cái máy rút" — phần quyết định **lấy cái gì** từ graph/vector để đưa vào LLM. Không phải chỉ có "Local/Global". Trong thực tế có **catalog nhiều loại retriever**, mỗi loại hợp 1 dạng câu hỏi.

### 6.1 Catalog Retriever Types

> **Cách đọc bảng này:** mỗi dòng là 1 loại "máy rút" dữ liệu; cột giữa nói cách nó lấy dữ liệu, cột "Ví dụ câu hỏi hợp" là dạng câu nó xử lý tốt. Ví dụ, Text2Cypher hợp câu hỏi cần tính toán như "ai quản lý dự án nhiều nhất?".

| Retriever | Cách hoạt động | Ví dụ câu hỏi hợp | Neo4j tương ứng |
|---|---|---|---|
| **VectorRetriever** | Embed câu hỏi → similarity trên entity/LLM text | "Tìm tài liệu nói về X" | KNN vector index |
| **VectorCypherRetriever** | Vector top-k → **traverse thêm neighbors** qua Cypher | "Tài liệu về X liên quan những ai?" | vector + `MATCH` |
| **HybridRetriever** | Vector + full-text → **RRF fuse** | "Từ khoá "Phoenix" hoặc naive-text" | combine indexes |
| **Text2Cypher** | LLM dịch câu hỏi → Cypher → chạy query | "Ai quản lý dự án nhiều nhất?" | LLM-generated Cypher |
| **DRIFT** (Microsoft) | "Drive the search": lấy càng nhanh, càng nhiều hướng | Module đầu vừa bế tắc → rẽ hướng | Agentic traversal |
| **Tools/Agentic retriever** | LLM-agent tự chọn tool (vector/traversal/cypher) | Nhiều kiểu câu trộn lẫn | `ToolsRetriever` |

### 6.2 Text2Cypher (NL → Cypher) Chi Tiết

> **📌 Khái Niệm Cơ Bản:**
> **Text2Cypher** = LLM đóng vai "phiên dịch câu hỏi tiếng người sang Cypher". Khác retrieve thông thường (kéo text về) — ở đây **câu trả lời là câu truy vấn**, chạy xong DB trả kết quả có cấu trúc.
>
> Công thức neo thành công: **Enhanced Schema Injection** — không nhồi toàn bộ schema (tốn token, LLM lẫn), mà chỉ nạp:
> - labels (loại thực thể) + tên attributes
> - vài **parent-child ngữ nghĩa quan trọng** (`(Person)-[:REPORTS_TO]->(Person)`)
>
> ```python
> # Enhanced schema cho Text2Cypher — chỉ nạp phần cần thiết
> def enhanced_schema_snippet() -> str:
>     return """Nodes: Person(name,role), Project(name,budget)
> Edges: Person-WORKS_ON->Project, Person-REPORTS_TO->Person
> Sample: (Alice,REPORTS_TO,Bob) — Bob là quản lý của Alice"""
>
> # Khi query trả rỗng → Text2Cypher tự sửa câu Cypher (Self-correction)
> # Khi schema không đủ → tự hỏi thêm metadata (schema refinement)
> ```

### 6.3 RRF — Hợp Nhất Nhiều Nguồn Không Cần "Điểm"

> **📌 Khái Niệm Cơ Bản:**
> **RRF (Reciprocal Rank Fusion)** = cách gộp nhiều bảng xếp hạng (từ vector, từ graph traversal, từ full-text) mà **không cần chuẩn hoá điểm**. Điểm số mới của mỗi item:
>
> ```
> score = Σ  1 / (k + rank_i)      với k ≈ 60
> ```
>
> Nghĩa gốc: **item càng top trong nhiều danh sách → càng được thưởng nhiều**. Item xếp #1 ở vector (nhận ~1/61) nhưng không xuất hiện ở graph traversal sẽ bị item #8 có mặt ở cả 2 nguồn (nhận ~1/68 + 1/68 > 1/61) vượt qua.
>
> **Analogies:** Giống bình chọn "vòng trong": ai được đề cử ở nhiều bảng khác nhau mới vào chung kết — kể cả không ai cho họ đứng nhất. RRF là kỹ thuật trong bài toán **hybrid retrieval** — kết hợp kết quả graph traversal + vector similarity.

> 📄 **Code ví dụ:** [`examples/06-6-3-rrf-hop-nhat-nhieu-nguon-khong.py`](examples/06-6-3-rrf-hop-nhat-nhieu-nguon-khong.py)

> **Tóm gọn 1 câu:** Chọn retriever theo dạng câu hỏi, và khi gộp nhiều nguồn dùng RRF — cộng theo thứ hạng nên không cần chuẩn hoá điểm số.

---

## 7. GraphRAG Variants (SOTA)

> **📌 Khái Niệm Cơ Bản:**
> **GraphRAG không chỉ là "1 công thức"** — từ GraphRAG gốc của Microsoft (index + các biến thể nối tiếp trước) tới 2025-2026 đã có nhiều hướng tối ưu khác nhau cho các bài toán khác nhau. Bảng dưới đây là **bản đồ những biến thể được nhắc nhiều nhất**:

> **Cách đọc bảng này:** mỗi dòng là 1 biến thể; cột "Ý tưởng cốt lõi" nói nó khác bản gốc chỗ nào, cột "Mạnh khi" chỉ tình huống nên dùng. Ví dụ, LightRAG rẻ hơn ~10 lần, hợp khi cần bao phủ rộng mà ít ngân sách.

| Variant | Ý tưởng cốt lõi | Mạnh khi | Yếu/giới hạn |
|---|---|---|---|
| **GraphRAG (MSFT)** | Index + Leiden communities + LLM summary | Global/sensemaking, multi-doc | Đắt (index tốn token), chậm |
| **LazyGraphRAG** (MSFT, 2024-2025) | Defer LLM summarisation tới query time | Index rẻ ngang vector RAG, quality ngang GraphRAG, query cost thấp hơn ~700× | Đã tích hợp Microsoft Discovery (2025) |
| **LightRAG** | Dual-level index (low/high); retrieval theo query; 10x nhanh GraphRAG, 1/3-1/4 cost | Bao phủ retrieval, cost nhỏ | Không làm tốt aggregation global như gốc |
| **HippoRAG (v2)** | Personalized PageRank trên KG + pairwise lai | Multi-hop, trả lời với **ít token** (20x rẻ hơn) | Phụ thuộc KG chất lượng |
| **KAG** | KG-augmented generation, semantic reasoning | Cần lý giải, trả lời logic | Cấu hình phức tạp |
| **DRIFT (MSFT)** | "Drive the search": lấy vô đủ hướng exploration | Truy vấn phức tạp, cần multi-direction | Vòng lặp agent phức tạp |
| **GRAG** | Divide-and-conquer subgraph truy xuất | Giảm nhiễu khi graph to | Cần pipeline phức tạp |

> **Đúc kết chọn variant:**
> - Cần **nhanh + giá rẻ + bao phủ**: `LightRAG`
> - Trả lời **multi-hop với ít token**: `HippoRAG2`
> - **Global/sensemaking trên cả corpus**: `GraphRAG` gốc
> - Truy vấn **phức tạp, phải nghĩ lại**: `DRIFT`
>
> Với framework học tập này, bản thân **hiểu được cơ chế (index + retrieve + community summary)** là quan trọng nhất — variants chỉ là cách tinh chỉnh 3 giai đoạn đó.

---

## 8. Khi Nào Dùng GraphRAG?

> **Cách đọc bảng này:** mỗi dòng là 1 dạng câu hỏi, cột "Dùng gì?" là công cụ nên chọn. Ví dụ, câu hỏi 1 bước như "Điều 5 nói gì?" → RAG thường; câu hỏi tổng hợp cả kho → Global GraphRAG.

```
┌──────────────────────────┬──────────────┬──────────────────────────────┐
│ Loại câu hỏi             │ Dùng gì?     │ Ví dụ                        │
├──────────────────────────┼──────────────┼──────────────────────────────┤
│ Factoid (1-hop)          │ Vanilla RAG  │ "Điều 5 của HĐ X nói gì?"    │
│                          │ hoặc Local   │ "Ai quản lý team Y?"         │
│ Multi-hop (2-4 hops)     │ Local GraphRAG│ "Ai duyệt HĐ của dự án X    │
│                          │              │  và người đó báo cáo cho ai?"│
│ Global / Sensemaking     │ Global GraphRAG│ "Chủ đề chính trong 1000  │
│                          │              │  docs này là gì?"            │
│ Aggregation              │ Global       │ "Có bao nhiêu dự án AI       │
│                          │              │  và ai quản lý chúng?"       │
│ Codebase Q&A             │ Local (code │ "Hàm X được gọi ở đâu?"       │
│                          │  graph)     │                              │
└──────────────────────────┴──────────────┴──────────────────────────────┘
```

**Decision flowchart:**

```
Câu hỏi có cần tổng hợp từ NHIỀU documents?
  ├── Không → Local Search (entity → subgraph)
  └── Có → Global Search (community summaries → map-reduce)

Câu hỏi có entities cụ thể?
  ├── Có → Local Search (bắt đầu từ entities đó)
  └── Không → Global Search (không có anchor để traverse)
```

> **⚠️ Khi Nào ĐỪNG Dùng GraphRAG (bằng chứng benchmark 2025-2026):**
>
> Nghiên cứu so sánh có hệ thống (RAG vs GraphRAG) cho thấy **GraphRAG không phải lúc nào cũng thắng**:
> 1. **Single-hop / factoid**: vanilla RAG **thắng** GraphRAG trên các câu hỏi hỏi "một sự thật đơn lẻ" (vd NQ) — vì graph retrieval có thêm chi phí traversal không cần thiết.
> 2. **Global community search dễ hallucinate**: summary của cộng đồng có thể **thiếu context cụ thể** → LLM "bịa" khi được hỏi chi tiết từ summary đó.
> 3. **Index cực đắt**: LLM-summarize toàn bộ communities ≈ chi phí index rất cao cho corpus lớn — nếu bạn chỉ có 50 docs nội bộ, đừng build GraphRAG.
>
> **Quyết định thực dụng:**
> - Corpus < 100 docs, câu trả lời chủ yếu factoid → **vanilla RAG đủ dùng**.
> - Cần multi-hop, aggregation, chủ đề xuyên nhiều docs → **GraphRAG**.
> - Đứng giữa: **LightRAG / HippoRAG** (nhẹ hơn, retriever text2cypher rẻ hơn).

> **Tóm gọn 1 câu:** Chọn theo câu hỏi: factoid 1 bước → RAG thường; nhiều bước → Local GraphRAG; tổng hợp cả kho → Global GraphRAG; chưa chắc → LightRAG/HippoRAG.

---

## 9. Labs Thực Hành

### Lab 1: So Sánh Vanilla RAG vs GraphRAG

1. Chuẩn bị 20 documents về 1 topic (ví dụ: "AI in Healthcare" — tự tạo hoặc scrape)
2. Chạy vanilla RAG (vector top-5) và GraphRAG (local search) trên 10 queries
3. Đánh giá thủ công: câu nào GraphRAG thắng? (global queries sẽ thắng rõ)

### Lab 2: Tuning Community Resolution

1. Thử `resolution` = 0.5, 1.0, 2.0 trong `detect_communities`
2. Quan sát số communities và global search quality
3. Tìm resolution tối ưu cho dataset của bạn

### Lab 3: Xây GraphRAG Cho Codebase

1. Parse 1 repo nhỏ (50 files) → tạo code graph (File → Function → Calls)
2. Hỏi: "Thay đổi hàm X ảnh hưởng đến những file nào?" → local search trên code graph
3. So sánh với `grep` thuần (grep = công cụ tìm chuỗi ký tự trong file, rất nhanh nhưng không hiểu quan hệ)

> **Tóm gọn 1 câu:** Lab 1 cho biết GraphRAG thắng ở đâu, Lab 2 chỉnh độ mịn của chia cụm, Lab 3 cho thấy code graph trả lời câu "sửa hàm X ảnh hưởng gì" mà grep không làm nổi.

---

## Tài Liệu Tham Khảo

> Tài liệu chính thức + bài báo gốc; cần gì tra nấy, không cần đọc hết.

- Edge et al. — *From Local to Global: A GraphRAG Approach to Query-Focused Summarization* (Microsoft Research, 2024) — https://arxiv.org/abs/2404.16130
- Microsoft GraphRAG — *GitHub* (https://github.com/microsoft/graphrag) — implementation + config
- Neo4j — *Building a Knowledge Graph with LLM* (https://neo4j.com/blog/developer/knowledge-graph-llm/)
- LangChain — *GraphCypherQAChain* (https://python.langchain.com/docs/use_cases/graph/)
- *GraphRAG in Practice: A Survey of Research Gaps* (arXiv:2507.03226) — RRF, retrieval & indexing at scale
- Neo4j graphrag-python — *Retriever types: Vector, VectorCypher, Hybrid, Text2Cypher, DRIFT* (https://neo4j.com/docs/graphrag-python/current/)
- *RAG vs GraphRAG: A Systematic Evaluation* — multi-hop thắng, single-hop thua vanilla RAG (arXiv 2025)
- LightRAG / HippoRAG2 — *Giảm chi phí graph retrieval* (https://github.com/HKUDS/LightRAG)

---

*Tiếp theo: [06 — Graph Reasoning](../06-graph-reasoning/)*
