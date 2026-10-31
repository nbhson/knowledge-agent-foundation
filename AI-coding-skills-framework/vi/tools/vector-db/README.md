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

Phần này giải thích vector DB là gì và tại sao harness cần nó. Nếu bỏ qua, agent của bạn sẽ giống người mất trí nhớ: mỗi phiên làm việc đều bắt đầu lại từ số 0.

Harness thì phải có trí nhớ. Nhưng nhớ kiểu keyword-search thôi là chưa đủ. Ví dụ: user hỏi *"lần trước mình bàn về bảo hiểm cho người lao động với điều kiện gì nhỉ?"* mà memory của bạn chỉ biết khớp đúng mặt chữ thì kiểu gì cũng sót. Vì sao sót? Lần trước ghi là "BHXH", hôm nay hỏi "bảo hiểm xã hội" — chữ khác nhau, ý nghĩa giống nhau. Tìm theo chữ là không ra.

> *"Memory is the difference between a stateless function and an agent that learns."*
>
> Dịch nôm na: "Có trí nhớ là điểm khác biệt giữa một hàm vô tri và một agent biết học hỏi." (stateless = không nhớ gì giữa các lần chạy.)

**Vector Database** (cơ sở dữ liệu vector) gỡ điểm này. Cách hoạt động:

- **Vector embedding** = biến đoạn text thành một dãy số, ví dụ `[0.12, -0.45, ...]`. Dãy số này đại diện cho *ý nghĩa*. Hai câu cùng ý nghĩa thì hai dãy số gần nhau — dù mặt chữ khác.
- **Khoảng cách cosine** = cách đo "hai dãy số có giống nhau không". Điểm càng gần 1 thì ý nghĩa càng sát. Ví dụ "BHXH" và "bảo hiểm xã hội" sẽ có điểm cao.

Đây chính là nền tảng của `harness/01-retrieve-memory-knowledge`: thay vì bê cả kho kiến thức nhét vào LLM, bạn chỉ đưa **vài chunk liên quan nhất về mặt ngữ nghĩa**. Chunk = một mẩu văn bản nhỏ, ví dụ cắt tài liệu thành từng đoạn 500-1000 tokens (token = đơn vị chữ mà LLM đọc, cỡ một từ).

> **Tóm gọn 1 câu:** Vector DB giúp agent nhớ theo *ý nghĩa* chứ không phải theo đúng mặt chữ, nên tìm được "BHXH" khi user hỏi "bảo hiểm xã hội".

### Tại Sao Vector DB Quan Trọng?

Phần này liệt kê 4 lý do bạn nên dùng vector DB thay vì tìm kiếm kiểu khác.

> - **Vector Embedding** biến text thành dãy số (vector) để máy tính so sánh
> - **Vector Database** lưu trữ và tìm kiếm vector nhanh chóng
> — HARNESS_ENGINEERING.md

Cách đọc bảng này: cột "Lý do" là tên gọi ngắn; cột "Giải thích" nói rõ vì sao nó có ích.

| # | Lý do | Giải thích |
|---|-------|------------|
| 1 | **Semantic search** | Tìm đúng *ý nghĩa* không chỉ *từ khóa* — nền tảng RAG (RAG = cho LLM tra tư liệu ngoài rồi mới trả lời) |
| 2 | **Memory tiers** | Chỉ đưa vào context những gì liên quan — giảm token đáng kể (context = "cửa sổ" text mà LLM đọc được trong một lần) |
| 3 | **Không phụ thuộc LLM** | Embedding tách rời khỏi generation — index một lần, query mãi (index = xây bảng tra cứu trước, query = tra sau) |
| 4 | **Đã có trong harness** | HARNESS_ENGINEERING.md dùng vectorStore cho Tier 2 Warm Memory (Tier 2 = tầng trí nhớ "ấm", giải thích ở phần Case Studies) |

> **Tóm gọn 1 câu:** Vector DB = tìm theo ý nghĩa, ít tốn token, chạy độc lập với LLM, và harness đã cài sẵn nó vào tầng Warm Memory.

### Quan Hệ Với Harness

Phần này cho thấy vector DB nằm ở đâu trong các thành phần của harness. harness = bộ khung các bước agent đi qua để trả lời.

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

Giải thích các từ khóa trong sơ đồ:

| Thuật ngữ | Nghĩa là gì |
|-----------|-------------|
| Retrieval | Bước "tra cứu": lấy ra những mẩu tin liên quan nhất |
| Top-k chunks | Lấy k mẩu văn bản giống ý nhất (k = số lượng, ví dụ top-5) |
| ctx | Context — phần text được đưa cho LLM đọc |
| Upsert | Update + insert: có rồi thì cập nhật, chưa có thì thêm mới |

```
Trong harness/01:
    User Query → Embedding → Vector DB → [chunk_liên_quan_1, chunk_liên_quan_2, ...]
                                                              ↓
                                             Context cho LLM (top-k chunks)
```

Đọc dòng trên như vầy: câu hỏi của user → đổi thành dãy số → tra trong vector DB → lấy ra vài mẩu văn bản giống ý nhất → nhét vào phần text LLM đọc.

> **Tóm gọn 1 câu:** Vector DB là "công cụ tra cứu" nằm giữa câu hỏi của user và context mà LLM đọc được.

## Tổng Quan Các Vector DB

Phần này so sánh 4 vector DB phổ biến để bạn chọn đúng cái phù hợp dự án.

Cách đọc bảng này: mỗi hàng là một vector DB. Cột "Loại" cho biết cài ở đâu (máy mình hay thuê cloud); "Đặc điểm nổi bật" là điểm mạnh; "Best for" là tình huống nên chọn nó.

| Vector DB | Loại | Đặc điểm nổi bật | Best for |
|-----------|------|------------------|----------|
| **Chroma** | Open-source, local | `pip install chromadb`, Python-native, persistent local | Dev/Lab, học nhanh, RAG đơn giản |
| **Pinecone** | Managed cloud | Serverless, scale tốt, zero-ops, có free tier | Production, scale lớn, native cloud |
| **Qdrant** | Open-source + Cloud | Rust core, filter ngữ nghĩa + metadata, rất nhanh | Filtering phức tạp, production |
| **Weaviate** | Open-source + Cloud | GraphQL native, hybrid search (vector + keyword) | Hybrid search, linh hoạt |

Giải thích nhanh các từ khóa: **persistent local** = dữ liệu lưu trên máy bạn, tắt máy không mất; **managed cloud** = nhà cung cấp chạy server giúp bạn, mình chỉ gọi API; **serverless / zero-ops** = không phải tự quản trị server; **hybrid search** = vừa tìm theo ý nghĩa vừa tìm theo từ khóa, lấy ưu điểm cả hai.

## Vector DB Landscape 2025-2026

Phần này là bảng so sánh phụ, có thêm 1 lựa chọn mới: pgvector. Hữu ích khi bạn muốn nhìn bức tranh toàn cảnh trước khi chọn.

Cách đọc bảng này: giống bảng trên, cột "Đặc điểm" là điểm mạnh, cột "Tốt cho" là nên dùng khi nào.

| DB | Đặc điểm | Tốt cho |
|----|---------|--------|
| Qdrant | Open source, Rust, hybrid search | Self-hosted, high performance |
| pgvector | Postgres extension | Small-medium scale, simple setup |
| Pinecone | Cloud-native, managed | Enterprise, managed infra |
| Weaviate | Open source, hybrid search | Multimodal (text+image) |
| Chroma | Local/embedded | Prototyping, local dev |

Giải thích: **pgvector** = một phần mở rộng (extension) cài thêm vào Postgres — database quan hệ quen thuộc — để nó tìm được luôn cả vector; **self-hosted** = tự cài và tự vận hành server của mình; **multimodal** = xử lý được nhiều kiểu dữ liệu cùng lúc (text, ảnh).

Embedding models mới (2026): OpenAI text-embedding-3-large, BGE-M3 (flag_embedding), Cohere v4. (Embedding model = mô hình chuyên biến text thành dãy số.)

> **pgvector lưu ý:** nếu dự án đã chạy Postgres, `pgvector` thường là lựa chọn ít ma sát nhất — không thêm hạ tầng mới, backup/permission dùng theo Postgres sẵn có. Hạn chế duy nhất là scale và tốc độ ở tập vector rất lớn không bằng Qdrant hay Pinecone chuyên dụng.

> **Tóm gọn 1 câu:** Mới học thì dùng Chroma, dự án đã có Postgres thì dùng pgvector, cần scale lớn hoặc lọc phức tạp thì lên Qdrant/Pinecone.

### Chroma — Khởi Đầu Nhanh (Local)

Phần này dẫn tới ví dụ cài Chroma chạy trên máy local — cách nhanh nhất để học vector DB mà không cần đăng ký dịch vụ gì.

> 📄 **Code ví dụ:** [`examples/01-chroma-khoi-au-nhanh-local.py`](examples/01-chroma-khoi-au-nhanh-local.py)

### Vector DB trong Tool Registry (harness/06)

Phần này dẫn tới ví dụ biến tìm kiếm vector thành một "tool" mà agent có thể tự gọi. Tool registry = danh sách các công cụ agent được phép dùng (harness/06 là bước agent chọn tool để xử lý việc).

> 📄 **Code ví dụ:** [`examples/02-vector-db-trong-tool-registry-harness-06.py`](examples/02-vector-db-trong-tool-registry-harness-06.py)

## Lộ Trình Học (Cấu Trúc Thư Mục)

Các thư mục đánh dấu (TODO) là chưa viết — xem như lộ trình dự kiến.

```
vector-db/
├── README.md            ← BẠN ĐANG Ở ĐÂY — tổng quan + lộ trình
├── 01-concepts/         ← (TODO) Embedding, cosine similarity, chunking, collections
├── 02-setup/            ← (TODO) Cài Chroma local → nâng Pinecone/Qdrant cloud
├── 03-patterns/         ← (TODO) RAG, memory tiers, hybrid search, re-ranking
├── 04-savings/          ← (TODO) Giảm token nhờ top-k retrieval vs full context
└── 05-troubleshooting/  ← (TODO) Embedding mismatch, chunk boundary, cold start
```

Giải thích các chủ đề chưa viết: **chunking** = cắt tài liệu dài thành các mẩu nhỏ; **collections** = "thư mục" chứa các vector trong Chroma; **re-ranking** = lấy kết quả thô rồi sắp xếp lại cho chuẩn hơn; **embedding mismatch** = lỗi query và dữ liệu bị embed bằng hai model khác nhau nên không "hiểu" nhau; **cold start** = lúc DB còn trống nên chưa tìm ra gì.

### Lộ Trình Đề Xuất

Phần này là 4 bước đi từ số 0 tới khi dùng được trong harness.

```
Bước 1: Hiểu embedding + cosine similarity (01-concepts)
   ↓
Bước 2: Cài Chroma local, tạo collection + upsert vài docs test (02-setup)
   ↓
Bước 3: Tích hợp vào harness/01 — query top-k → đưa vào context
   ↓
Bước 4: Nâng cấp Pinecone/Qdrant khi cần scale (03-patterns)
```

Cách đọc: đọc từ trên xuống, mỗi bước dựng trên bước trước. Bước 2 có "docs test" = vài tài liệu mẫu để thử. Bước 4 mới cần làm khi lượng dữ liệu lớn lên.

Nếu muốn đào sâu từng mảnh, đọc theo bảng dưới:

| Bạn muốn... | Đọc |
|-------------|-----|
| Hiểu memory tiers | [harness/01-retrieve-memory-knowledge](../../harness/01-retrieve-memory-knowledge/) |
| Build context từ chunks | [harness/02-build-context](../../harness/02-build-context/) |
| Update memory store | [harness/03-update-memory-store](../../harness/03-update-memory-store/) |
| LangChain RAG | [tools/langchain](../langchain/) |
| Embedding model | [ollama/MODEL.md](../../../../ollama/MODEL.md) |

> **Tóm gọn 1 câu:** Học theo thứ tự hiểu khái niệm → cài Chroma thử → gắn vào harness/01 → nâng cấp DB khi cần scale.

## Case Studies Thực Tế

Phần này cho thấy 2 cách dùng vector DB phổ biến nhất: làm kho tư liệu cho RAG, và chia trí nhớ thành các tầng.

### 1. RAG Cho Project Knowledge

```
Docs/ (Markdown, PDF) 
   → Chunk (01-concepts: 500-1000 tokens/chunk có overlap)
   → Embed (sentence-transformers / ollama embedding)
   → Upsert vào Chroma collection "project_memory"
   ↓
Agent hỏi → query vector → top-5 chunks → context cho LLM
```

Đọc sơ đồ từ trên xuống: tài liệu gốc → cắt thành mẩu 500-1000 tokens (overlap = các mẩu chen nhau vài dòng, để không cắt hỏng câu) → đổi thành dãy số bằng embedding model (sentence-transformers / ollama embedding là các model chạy local) → lưu vào collection tên "project_memory". Khi agent cần, nó tra top-5 mẩu giống ý nhất và đưa cho LLM đọc.

### 2. Memory Tiering (harness/01 Warm Memory)

```
Tier 1 Cold  → Không embed, lưu file hệ thống
Tier 2 Warm  → Chroma vector_store — truy xuất nhanh, semantic
Tier 3 Hot   → Context window — luôn có sẵn

HARNESS_ENGINEERING.md dòng 1954:
  // Tier 2: Warm Memory (Vector DB)
```

Đọc như chia trí nhớ 3 tầng, từ chậm tới nhanh:

| Tầng | Nghĩa là gì |
|------|-------------|
| Tier 1 Cold | Lưu trữ lâu dài dạng file, không cần tra nhanh |
| Tier 2 Warm | Lưu trong Chroma, tra theo ý nghĩa, nhanh vừa phải |
| Tier 3 Hot | Đã nằm sẵn trong context window (phần text LLM luôn đọc được) |

> **Tóm gọn 1 câu:** Vector DB thường dùng để (1) làm kho tư liệu RAG từ tài liệu dự án, và (2) làm tầng trí nhớ Warm giữa file và context.

## Tài Liệu Tham Khảo

- **Chroma**: https://www.trychroma.com
- **Pinecone**: https://www.pinecone.io
- **Qdrant**: https://qdrant.tech
- **Weaviate**: https://weaviate.io
- **pgvector**: https://github.com/pgvector/pgvector
- **BGE-M3**: https://huggingface.co/BAAI/bge-m3
- **HNSW index paper**: https://arxiv.org/abs/1603.09320

(HNSW = thuật toán indexing giúp tra vector nhanh; paper = bài báo nghiên cứu gốc.)

### Liên Kết Sang Nhánh Khác

Các file trong repo liên quan trực tiếp tới vector DB — đọc để xem nó gắn vào bức tranh chung thế nào.

- [HARNESS_ENGINEERING.md](../../HARNESS_ENGINEERING.md) — Tier 2 Warm Memory
- [harness/01-retrieve-memory-knowledge](../../harness/01-retrieve-memory-knowledge/) — Retrieval component
- [harness/06-decide-tools-mcp](../../harness/06-decide-tools-mcp/) — `vector_search` tool
- [tools/langchain](../langchain/) — LangChain retriever integrations
- [ollama/](../../../../ollama/) — Embedding models local (nomic-embed-text)

---

> **"Don't give your LLM the whole library — give it the three most relevant pages."**
>
> Dịch nôm na: "Đừng đưa cho LLM cả thư viện — chỉ đưa 3 trang liên quan nhất."

---

*Bài viết thuộc [AI Coding Skills Framework](../..) — nhánh Tools — vector-db*
