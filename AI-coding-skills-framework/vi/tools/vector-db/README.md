# 🗄️ Vector Databases — Lưu Trữ & Truy Xuất Memory Cho Harness

> ## 📑 Mục Lục
>
> - [Câu Chuyện Mở Đầu](#câu-chuyện-mở-đầu)
> - [Tại Sao Vector DB Quan Trọng?](#tại-sao-vector-db-quan-trọng)
> - [Quan Hệ Với Harness](#quan-hệ-với-harness)
> - [Tổng Quan Các Vector DB](#tổng-quan-các-vector-db)
> - [Lộ Trình Học (Cấu Trúc Thư Mục)](#lộ-trình-học-cấu-trúc-thư-mục)
> - [Case Studies Thực Tế](#case-studies-thực-tế)
> - [Tài Liệu Tham Khảo](#tài-liệu-tham-khảo)

---

### Câu Chuyện Mở Đầu

Harness thì phải có trí nhớ. Nhưng nhớ kiểu keyword-search thôi là chưa đủ — user hỏi *"lần trước mình bàn về bảo hiểm cho người lao động với điều kiện gì nhỉ?"* mà memory của bạn chỉ biết khớp đúng mặt chữ thì kiểu gì cũng sót.

> *"Memory is the difference between a stateless function and an agent that learns."*

**Vector Database** gỡ điểm này bằng cách biến mọi đoạn text thành **vector embedding** — một dãy số đại diện cho *ý nghĩa* — rồi tìm kiếm bằng **khoảng cách cosine**. Đây chính là nền tảng của `harness/01-retrieve-memory-knowledge`: thay vì bê cả kho kiến thức nhét vào LLM, bạn chỉ đưa **vài chunk liên quan nhất về mặt ngữ nghĩa**.

### Tại Sao Vector DB Quan Trọng?

> - **Vector Embedding** biến text thành dãy số (vector) để máy tính so sánh
> - **Vector Database** lưu trữ và tìm kiếm vector nhanh chóng
> — HARNESS_ENGINEERING.md

| # | Lý do | Giải thích |
|---|-------|------------|
| 1 | **Semantic search** | Tìm đúng *ý nghĩa* không chỉ *từ khóa* — nền tảng RAG |
| 2 | **Memory tiers** | Chỉ đưa vào context những gì liên quan — giảm token đáng kể |
| 3 | **Không phụ thuộc LLM** | Embedding tách rời khỏi generation — index một lần, query mãi |
| 4 | **Đã có trong harness** | HARNESS_ENGINEERING.md dùng vectorStore cho Tier 2 Warm Memory |

### Quan Hệ Với Harness

```
┌────────────────────────────────────────────────────────────┐
│  VECTOR DB MAP VS HARNESS COMPONENTS                       │
│                                                            │
│  harness/01-retrieve-memory-knowledge → Retrieval (chính)  │
│  harness/02-build-context            → Top-k chunks vào ctx│
│  harness/03-update-memory-store      → Upsert embeddings   │
│  harness/06-decide-tools-mcp         → vector_search tool  │
└────────────────────────────────────────────────────────────┘
```

```
Trong harness/01:
    User Query → Embedding → Vector DB → [chunk_liên_quan_1, chunk_liên_quan_2, ...]
                                                              ↓
                                             Context cho LLM (top-k chunks)
```

## Tổng Quan Các Vector DB

| Vector DB | Loại | Đặc điểm nổi bật | Best for |
|-----------|------|------------------|----------|
| **Chroma** | Open-source, local | `pip install chromadb`, Python-native, persistent local | Dev/Lab, học nhanh, RAG đơn giản |
| **Pinecone** | Managed cloud | Serverless, scale tốt, zero-ops, có free tier | Production, scale lớn, native cloud |
| **Qdrant** | Open-source + Cloud | Rust core, filter ngữ nghĩa + metadata, rất nhanh | Filtering phức tạp, production |
| **Weaviate** | Open-source + Cloud | GraphQL native, hybrid search (vector + keyword) | Hybrid search, linh hoạt |

## Vector DB Landscape 2025-2026

| DB | Đặc điểm | Tốt cho |
|----|---------|--------|
| Qdrant | Open source, Rust, hybrid search | Self-hosted, high performance |
| pgvector | Postgres extension | Small-medium scale, simple setup |
| Pinecone | Cloud-native, managed | Enterprise, managed infra |
| Weaviate | Open source, hybrid search | Multimodal (text+image) |
| Chroma | Local/embedded | Prototyping, local dev |

Embedding models mới (2026): OpenAI text-embedding-3-large, BGE-M3 (flag_embedding), Cohere v4.

> **pgvector lưu ý:** nếu dự án đã chạy Postgres, `pgvector` thường là lựa chọn ít ma sát nhất — không thêm hạ tầng mới, backup/permission dùng theo Postgres sẵn có. Hạn chế duy nhất là scale và tốc độ ở tập vector rất lớn không bằng Qdrant hay Pinecone chuyên dụng.

### Chroma — Khởi Đầu Nhanh (Local)

```python
import chromadb

client = chromadb.PersistentClient(path="./memory")   # harness/03 memory store
collection = client.get_or_create_collection("project_memory")

# Lưu memory (upsert — harness/03)
collection.upsert(
    ids=["doc-1"],
    documents=["BHYT cho người lao động: mức đóng 4.5% từ 2026"],
    metadatas=[{"topic": "insurance", "tier": "warm"}]   # Tier 2 Warm Memory
)

# Retrieve (harness/01) — semantic search
results = collection.query(
    query_texts=["chế độ bảo hiểm lao động"],
    n_results=3  # top-k → harness/02 build context
)
```

### Vector DB trong Tool Registry (harness/06)

```python
registry.register(ToolDefinition(
    name="vector_search",
    description="Tìm kiếm ngữ nghĩa trong cơ sở dữ liệu vector",
    parameters={
        "query": {"type": "string", "required": True},
        "top_k": {"type": "integer", "default": 5},
        "collection": {"type": "string"},
        "filters": {"type": "object"},
    },
    category="search",
    tags=["semantic", "vector", "embedding"],
))
```

## Lộ Trình Học (Cấu Trúc Thư Mục)

```
vector-db/
├── README.md            ← BẠN ĐANG Ở ĐÂY — tổng quan + lộ trình
├── 01-concepts/         ← (TODO) Embedding, cosine similarity, chunking, collections
├── 02-setup/            ← (TODO) Cài Chroma local → nâng Pinecone/Qdrant cloud
├── 03-patterns/         ← (TODO) RAG, memory tiers, hybrid search, re-ranking
├── 04-savings/          ← (TODO) Giảm token nhờ top-k retrieval vs full context
└── 05-troubleshooting/  ← (TODO) Embedding mismatch, chunk boundary, cold start
```

### Lộ Trình Đề Xuất

```
Bước 1: Hiểu embedding + cosine similarity (01-concepts)
   ↓
Bước 2: Cài Chroma local, tạo collection + upsert vài docs test (02-setup)
   ↓
Bước 3: Tích hợp vào harness/01 — query top-k → đưa vào context
   ↓
Bước 4: Nâng cấp Pinecone/Qdrant khi cần scale (03-patterns)
```

| Bạn muốn... | Đọc |
|-------------|-----|
| Hiểu memory tiers | [harness/01-retrieve-memory-knowledge](../../harness/01-retrieve-memory-knowledge/) |
| Build context từ chunks | [harness/02-build-context](../../harness/02-build-context/) |
| Update memory store | [harness/03-update-memory-store](../../harness/03-update-memory-store/) |
| LangChain RAG | [tools/langchain](../langchain/) |
| Embedding model | [ollama/MODEL.md](../../../ollama/MODEL.md) |

## Case Studies Thực Tế

### 1. RAG Cho Project Knowledge

```
Docs/ (Markdown, PDF) 
   → Chunk (01-concepts: 500-1000 tokens/chunk có overlap)
   → Embed (sentence-transformers / ollama embedding)
   → Upsert vào Chroma collection "project_memory"
   ↓
Agent hỏi → query vector → top-5 chunks → context cho LLM
```

### 2. Memory Tiering (harness/01 Warm Memory)

```
Tier 1 Cold  → Không embed, lưu file hệ thống
Tier 2 Warm  → Chroma vector_store — truy xuất nhanh, semantic
Tier 3 Hot   → Context window — luôn có sẵn

HARNESS_ENGINEERING.md dòng 1954:
  // Tier 2: Warm Memory (Vector DB)
```

## Tài Liệu Tham Khảo

- **Chroma**: https://www.trychroma.com
- **Pinecone**: https://www.pinecone.io
- **Qdrant**: https://qdrant.tech
- **Weaviate**: https://weaviate.io
- **pgvector**: https://github.com/pgvector/pgvector
- **BGE-M3**: https://huggingface.co/BAAI/bge-m3
- **HNSW index paper**: https://arxiv.org/abs/1603.09320

### Liên Kết Sang Nhánh Khác

- [HARNESS_ENGINEERING.md](../../HARNESS_ENGINEERING.md) — Tier 2 Warm Memory
- [harness/01-retrieve-memory-knowledge](../../harness/01-retrieve-memory-knowledge/) — Retrieval component
- [harness/06-decide-tools-mcp](../../harness/06-decide-tools-mcp/) — `vector_search` tool
- [tools/langchain](../langchain/) — LangChain retriever integrations
- [ollama/](../../../ollama/) — Embedding models local (nomic-embed-text)

---

> **"Don't give your LLM the whole library — give it the three most relevant pages."**

---

*Bài viết thuộc [AI Coding Skills Framework](../..) — nhánh Tools — vector-db*