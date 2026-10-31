# 🧠 02. Knowledge Graph Construction — Xây Dựng Đồ Thị Tri Thức

> ## 📑 Mục Lục
>
> - [Câu Chuyện Mở Đầu](#câu-chuyện-mở-đầu)
> - [Tại Sao KG Construction Quan Trọng?](#tại-sao-kg-construction-quan-trọng)
> - [Tổng Quan](#tổng-quan)
> - [Nội Dung](#nội-dung)
> - [1. Ontology & Schema Design](#1-ontology--schema-design)
> - [2. Entity Extraction](#2-entity-extraction)
> - [3. Relation Extraction](#3-relation-extraction)
> - [4. Entity Resolution & Deduplication](#4-entity-resolution--deduplication)
> - [5. Incremental KG Updates](#5-incremental-kg-updates)
> - [6. Complete Pipeline](#6-complete-pipeline)
> - [7. Labs Thực Hành](#7-labs-thực-hành)
> - [Tài Liệu Tham Khảo](#tài-liệu-tham-khảo)

---

### Câu Chuyện Mở Đầu

Bạn có 1,000 tài liệu: hợp đồng, báo cáo, emails. Bạn thuê 3 interns đọc và trích xuất tri thức:

- Intern A trích: `(Phoenix, managed_by, Alice)` — nhưng ghi "Alice Nguyen"
- Intern B trích: `(Alice N., approves, Contract C-2024)` — viết tắt khác
- Intern C trích: `(Alice Nguyễn, reports_to, Bob)` — dấu tiếng Việt khác

Kết quả: 3 nodes "Alice" khác nhau trong graph, không nối được với nhau → graph **rời rạc**, truy vấn thất bại.

**Knowledge Graph Construction** giải quyết bài toán này: **trích xuất nhất quán, chuẩn hóa, và nối kết** tri thức từ raw text thành graph có thể truy vấn.

> **Tóm gọn 1 câu:** Ba người đọc cùng tài liệu viết cùng người khác ba kiểu → graph rời rạc; bài toán của module này là trích xuất thống nhất, gộp trùng, và nối kết.

### Tại Sao KG Construction Quan Trọng?

> *"Garbage in, garbage out — graph tệ hơn vector nếu extraction sai. Extraction quyết định 80% chất lượng GraphRAG."*
> — Microsoft GraphRAG Paper (2024)

**Cách đọc bảng này:** cột "Nghiên Cứu" là nguồn phát hiện; cột "Phát Hiện" là kết luận kèm số liệu. Ví dụ, trích nhiều vòng (gleaning) tăng 25% số thực thể bắt được so với trích một lần.

| # | Nghiên Cứu | Phát Hiện |
|---|-----------|-----------|
| 1 | **Microsoft GraphRAG (2024)** | Gleaning loop (trích nhiều vòng) tăng **25% entity coverage** so với single-pass |
| 2 | **LangChain Evaluation (2025)** | Deduplication bằng embedding similarity giảm **40% duplicate nodes** |
| 3 | **Stanford KB Construction (2024)** | Schema-first approach giảm **60% invalid relations** so với open extraction |

---

## Tổng Quan

```
(Đọc sơ đồ: 5 bước nối tiếp — định nghĩa schema → trích thực thể → trích quan hệ → gộp trùng → cập nhật dần, cuối cùng ra Knowledge Graph sẵn sàng dùng.)
Raw Documents
    │
    ▼
┌─────────────────────┐
│  1. ONTOLOGY DESIGN │  ← Định nghĩa node/edge types hợp lệ (schema)
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│ 2. ENTITY EXTRACTION│  ← LLM/NER trích entities từ text
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│ 3. RELATION EXTRACT │  ← LLM trích quan hệ giữa entities
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│ 4. RESOLUTION       │  ← Gộp trùng lặp (Alice = Alice Nguyen)
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│ 5. INCREMENTAL UPDATE│ ← Cập nhật graph khi có doc mới
└──────────┬──────────┘
           ▼
     Knowledge Graph (sẵn sàng cho Storage & GraphRAG)
```

---

## Nội Dung

**Cách đọc bảng này:** cột "#" là số thứ tự phần; "Chủ đề" có link bấm tới được; "Mô tả" tóm tắt phần đó dạy gì. Ví dụ, phần 4 là cách gộp "một người bị viết thành nhiều node".

| # | Chủ đề | Mô tả |
|---|--------|-------|
| 1 | [Ontology & Schema](#1-ontology--schema-design) | Thiết kế schema, constraints, temporal properties |
| 2 | [Entity Extraction](#2-entity-extraction) | NER, LLM extraction, gleaning loop |
| 3 | [Relation Extraction](#3-relation-extraction) | Open RE, schema-guided RE, confidence scoring |
| 4 | [Resolution](#4-entity-resolution--deduplication) | Deduplication, canonicalization, embedding-based |
| 5 | [Incremental Updates](#5-incremental-kg-updates) | Thêm/sửa/xóa không rebuild toàn bộ |
| 6 | [Pipeline](#6-complete-pipeline) | End-to-end code |
| 7 | [Agentic Construction](#7-agentic-kg-construction) | LLM-agent tự xây & tự sửa KG bằng CRUD |

> **Tóm gọn 1 câu:** Pipeline gồm 6 bước tuần tự (schema → trích → gộp → cập nhật) cộng một hướng đi mới: agent tự xây tự sửa — mỗi phần một mục dưới đây.

---

## 1. Ontology & Schema Design

> Phần này giải thích "bản thiết kế" của graph: khai báo trước loại thực thể và quan hệ nào hợp lệ — bước đầu tiên và quan trọng nhất.

> **📌 Khái Niệm Cơ Bản:**
> **Ontology = "bản thiết kế" của graph** — quy định TRƯỚC những loại thực thể nào tồn tại (`Person`, `Project`, `Document`) và quan hệ nào hợp lệ (`Person` mới được `MANAGES`).
>
> **Tại sao quan trọng?** Nếu không có ontology, LLM trích xuất tự do → graph trở thành **"hairball"** (mớ rối không kiểm soát): 5 thứ gọi là "team", già reviewer đồng nghĩa... query không chuẩn, kết quả sai.
>
> **Analogies:** Ontology giống **khung biểu mẫu** công ty — biết trước hồ sơ có những trường nào, ai được phê duyệt ai. Không có khung → mỗi người ghi hồ sơ mỗi kiểu, không ai tra được.
>
> **2 hướng thiết kế:**
> - **Schema-First**: định trước schema rồi trích xuất theo schema — sạch nhưng có thể bỏ sót quan hệ ngoài dự kiến.
> - **Schema-Free**: trích xuất tự do rồi mới quy hoạch — linh hoạt nhưng sinh nhiều rác.
> - **Hybrid (khuyến nghị)**: schema cốt lõi + xác nhận + cho phép edge lạ vào "pending" để review định kỳ.

### 1.1 Schema-First vs Schema-Free

```
(Cách đọc: so sánh 3 cách thiết kế — định trước schema, để tự do rồi quy hoạch sau, hoặc hybrid. Ví dụ: Schema-First ít rác nhưng cần chuyên gia định nghĩa trước.)
┌──────────────────┬──────────────────────────────────┬──────────────────────────────┐
│ Cách tiếp cận    │ Ưu điểm                          │ Nhược điểm                   │
├──────────────────┼──────────────────────────────────┼──────────────────────────────┤
│ Schema-First     │ Precise, ít rác, dễ query        │ Bỏ sót quan hệ ngoài schema │
│ (định trước)     │ Validation chặt                  │ Cần domain expert            │
│ Schema-Free      │ Linh hoạt, khám phá quan hệ mới  │ Nhiều rác, khó query        │
│ (open extraction)│ Không cần expert                 │ Hairball graph               │
│ Hybrid (khuyến nghị)│ Best of both                │ Phức tạp hơn                 │
└──────────────────┴──────────────────────────────────┴──────────────────────────────┘
```

### 1.2 Thiết Kế Ontology

> 📄 **Code ví dụ:** [`examples/01-1-2-thiet-ke-ontology.yaml`](examples/01-1-2-thiet-ke-ontology.yaml)

### 1.3 Validation Code

<details>
<summary>Python Code — Ontology Validation (Click để xem)</summary>

> 📄 **Code ví dụ:** [`examples/02-1-3-validation-code.py`](examples/02-1-3-validation-code.py)

</details>

> **Tóm gọn 1 câu:** Không có ontology thì graph thành mớ rối — dùng hybrid: schema cốt lõi định trước, edge lạ cho vào "pending" để duyệt định kỳ.

---

## 2. Entity Extraction

> Phần này dạy 4 cách "gạch chân thực thể" trong văn bản, từ regex cứng tới LLM chạy nhiều vòng.

> **📌 Khái Niệm Cơ Bản:**
> **Entity Extraction = "đọc tài liệu và gạch chân những thực thể quan trọng"** — tìm ra ai là ai (`Nguyễn Văn A = Person`), cái gì là gì (`Phoenix = Project`).
>
> **Analogies:** Giống bạn đọc hợp đồng và bôi đen: tên người, tên dự án, tên tổ chức, tên tài liệu.
>
> **4 cách trích xuất, từ đơn giản tới thông minh dần:**
> - **Rule-based (regex)**: luật cố định như "C-2024" là mã hợp đồng — chính xác cao nhưng chỉ xử lý pattern đã biết.
> - **NER (spaCy/BERT)**: model học sẵn nhận diện Person/Location/Org — nhanh, chuẩn cho thể loại thông dụng.
> - **LLM extract đơn vòng**: gọi LLM 1 lần lấy JSON entities — linh hoạt nhưng dễ **bỏ sót** khi văn bản dài (LLM "quên" phần sau).
> - **LLM + Gleaning (khuyến nghị cho GraphRAG)**: chạy **nhiều vòng** — vòng sau hỏi "còn entity nào bỏ sót không?" (đưa danh sách đã trích vào prompt) → coverage gần như đầy đủ.

### 2.1 So Sánh Phương Pháp

**Cách đọc bảng này:** Precision = độ đúng (ít báo nhầm); Recall = độ đủ (ít bỏ sót); ⭐ càng nhiều càng tốt. Ví dụ, regex rất đúng nhưng sót nhiều (recall ⭐⭐).

```
┌──────────────────┬──────────┬──────────┬──────────────────────────────┐
│ Phương pháp      │ Precision│ Recall   │ Phù hợp nhất khi             │
├──────────────────┼──────────┼──────────┼──────────────────────────────┤
│ Rule-based (regex)│ ⭐⭐⭐⭐⭐ │ ⭐⭐     │ Pattern cố định (mã HĐ, ngày)│
│ NER (spaCy, BERT)│ ⭐⭐⭐⭐  │ ⭐⭐⭐   │ Person, Org, Location        │
│ LLM (GPT-4o)     │ ⭐⭐⭐   │ ⭐⭐⭐⭐⭐ │ Mọi entity type, context-aware│
│ LLM + Gleaning   │ ⭐⭐⭐⭐  │ ⭐⭐⭐⭐⭐ │ GraphRAG: nhiều vòng, full coverage│
└──────────────────┴──────────┴──────────┴──────────────────────────────┘
```

### 2.2 LLM Extraction với Gleaning Loop (GraphRAG Pattern)

<details>
<summary>Python Code — Entity Extraction với Gleaning (Click để xem)</summary>

> 📄 **Code ví dụ:** [`examples/03-2-2-llm-extraction-voi-gleaning-loop-graphrag.py`](examples/03-2-2-llm-extraction-voi-gleaning-loop-graphrag.py)

</details>

### 2.3 Chunking Trước Khi Extract

Giống như RAG, documents lớn cần chia nhỏ trước khi extraction:

> 📄 **Code ví dụ:** [`examples/04-2-3-chunking-truoc-khi-extract.py`](examples/04-2-3-chunking-truoc-khi-extract.py)

### 2.4 Claims Extraction (GraphRAG Pattern)

> **📌 Khái Niệm Cơ Bản:**
> **Claims = "các khẳng định/dữ kiện" đáng giá trích ra từ văn bản**, không chỉ entities + relations.
>
> Ví dụ từ câu *"Phòng ban cần cắt giảm 20% ngân sách quý sau"*:
> - Entity: `Phòng ban`, `ngân sách`
> - Relation: hợp lệ giữa ai với ai
> - **Claim**: `{subject: Phòng ban, predicate: CUT_BUDGET, object: 20%, period: quý sau, source_chunk: "doc #3"}`
>
> **Tại sao cần?** GraphRAG của Microsoft trích cả 3 loại (entity/relation/claim). Claim cho phép trả lời câu hỏi dạng **"qui định nào / bằng chứng nào nói về X?"** — LLM trả lời kèm **nguồn bằng chứng** (source text) thay vì đoán. Mỗi claim **click được về chunk gốc** (evidence provenance).

> 📄 **Code ví dụ:** [`examples/05-2-4-claims-extraction-graphrag-pattern.py`](examples/05-2-4-claims-extraction-graphrag-pattern.py)

> **Tóm gọn 1 câu:** Ngoài entity và relation, hãy trích cả claims (khẳng định có bằng chứng) — nhờ vậy câu trả lời click được về đoạn văn bản gốc.

---

## 3. Relation Extraction

> Phần này dạy trích quan hệ giữa các thực thể theo đúng schema, kèm điểm tin cậy (confidence) để lọc sau.

### 3.1 Schema-Guided Relation Extraction

<details>
<summary>Python Code — Relation Extraction (Click để xem)</summary>

> 📄 **Code ví dụ:** [`examples/06-3-1-schema-guided-relation-extraction.py`](examples/06-3-1-schema-guided-relation-extraction.py)

</details>

### 3.2 Confidence Scoring

Mỗi relation nên có `confidence` để downstream filtering: (confidence = điểm tin cậy model tự chấm, từ 0 đến 1 — dùng để lọc bỏ quan hệ mơ hồ)

> 📄 **Code ví dụ:** [`examples/07-3-2-confidence-scoring.py`](examples/07-3-2-confidence-scoring.py)

> **Tóm gọn 1 câu:** Trích quan hệ theo schema (đúng loại node mới nối) và gắn điểm confidence cho mỗi quan hệ để lọc rác về sau.

---

## 4. Entity Resolution & Deduplication

> Phần này dạy gộp "một người bị viết thành nhiều node" — bước quyết định graph liền mạch hay rời rạc.

> **📌 Khái Niệm Cơ Bản:**
> **Deduplication = tìm và gộp "1 người viết bằng 2 tên"** — LLM trích xuất từ từng chunk khác nhau nên **cùng 1 thực thể có thể thành nhiều nodes**: "Nguyễn Văn A" (doc 1), "NV A" (doc 2), "Nguyen Van A" (doc 3).
>
> **Analogies:** Danh bạ công ty 2 lần ghi cùng một người — "Nguyễn Văn A - CTO" và "anh A - giám đốc công nghệ". Không gộp → query "CTO là ai?" chia đôi dữ liệu, trả lời sai.
>
> **Các mức dedup (từ đơn giản → thông minh):**
> 1. **Chuẩn hóa text**: lowercase, bỏ dấu, bỏ từ thừa → "Nguyen Van A" == "nguyễn văn a"
> 2. **Fuzzy match**: Levenshtein/TF-IDF similarity — "Nguyen Van A" vs "Nguyen Van An" gần giống
> 3. **Embedding similarity**: "CTO Alice" và "giám đốc công nghệ Alice" ngữ nghĩa giống nhau
>
> **Cảnh báo:** gộp quá mạnh → **hợp nhất nhầm 2 người thật sự khác nhau** (Alice nhân sự ≠ Alice CTO). Luôn đặt **ngưỡng (threshold)** và cho phép split lại.

### 4.1 Bài Toán

```
Raw extraction:
  "Nguyễn Văn A" (Person)
  "Alice Nguyen" (Person)    ← cùng người?
  "A. Nguyen"    (Person)

  "Dự án Phoenix" (Project)
  "Phoenix Project" (Project) ← cùng project?
  "Phoenix" (Project)
```

### 4.2 Embedding-Based Deduplication

<details>
<summary>Python Code — Deduplication (Click để xem)</summary>

> 📄 **Code ví dụ:** [`examples/08-4-2-embedding-based-deduplication.py`](examples/08-4-2-embedding-based-deduplication.py)

</details>

### 4.3 Entity Linking & Coreference Resolution

> **📌 Khái Niệm Cơ Bản:**
> **Entity Linking** = gắn một danh từ/đại từ về **đúng thực thể duy nhất** trong graph (mặc dù viết khác nhau). **Coreference Resolution** = nhận biết "anh ấy", "CEO", "ông A" đều chỉ cùng 1 người.
>
> **Khác Dedup ở chỗ nào?** Dedup gộp *hậu kỳ* (sau khi trích). Entity linking xử lý *ngay lúc trích* — biết "NV A" trong doc 2 chính là node "Nguyễn Văn A" đã tồn tại.
>
> **Analogies:** Giống tổ chức sự kiện: 3 người đăng ký ghi khác tên ("Nguyễn Văn A", "NV A", "anh A") — bảo vệ (linking) phải nhận ra đó là 1 người để không cấp 3 thẻ khác nhau.

> 📄 **Code ví dụ:** [`examples/09-4-3-entity-linking-coreference-resolution.py`](examples/09-4-3-entity-linking-coreference-resolution.py)

> **Tóm gọn 1 câu:** Dedup gộp sau khi trích (3 tên = 1 node), entity linking nhận ra ngay lúc trích ("NV A" = "Nguyễn Văn A" đã có trong graph); luôn đặt ngưỡng và cho phép tách lại.

---

## 5. Incremental KG Updates

> Phần này dạy cập nhật graph khi có tài liệu mới mà không xây lại từ đầu.

KG production thay đổi hàng ngày — không thể rebuild toàn bộ mỗi lần. (rebuild = xây lại toàn bộ từ đầu.)

> 📄 **Code ví dụ:** [`examples/10-5-incremental-kg-updates.py`](examples/10-5-incremental-kg-updates.py)

> **Tóm gọn 1 câu:** Thêm/sửa/xoá từng phần bằng `MERGE` và xoá mềm — chạy lại được, không nhân bản, không đụng phần còn lại của đồ thị.

---

## 6. Complete Pipeline

> Phần này gom toàn bộ 5 bước trên thành một đoạn code chạy đầu-cuối.

<details>
<summary>Python Code — End-to-End KG Construction (Click để xem)</summary>

> 📄 **Code ví dụ:** [`examples/11-6-complete-pipeline.py`](examples/11-6-complete-pipeline.py)

</details>

> **Tóm gọn 1 câu:** Pipeline hoàn chỉnh = schema → trích → gộp → ghi, chạy được lại từ đầu đến cuối mà không hỏng dữ liệu cũ.

---

## 7. Agentic KG Construction

> **📌 Khái Niệm Cơ Bản:**
> **Agentic KG construction** = thay vì pipeline batch trích-trước-rồi-virtual nên **LLM-agent trực tiếp thao tác graph bằng CRUD** (Create/Read/Update/Delete qua Cypher). Agent đọc văn bản → viết query `CREATE`/`MERGE` → kiểm tra kết quả → **tự nhận lỗi và sửa** nếu query sai hoặc thông tin chưa đúng.
>
> **So với pipeline batch (các section trên):**
>
> (Cách đọc bảng: mỗi hàng là một tiêu chí so sánh. Ví dụ, hàng "Bằng chứng": pipeline không lưu nguồn, agent gắn `source_chunk` — ghi rõ mỗi quan hệ lấy từ đoạn văn bản nào.)
>
> | | Batch Pipeline | Agentic Agent |
> |---|---|---|
> | Quy trình | 1 chiều: text → extract → gom | Vòng lặp: đọc → ghi → kiểm tra → sửa |
> | Sửa lỗi | Chạy lại pipeline | Tự quyết định UPDATE/DELETE |
> | Bằng chứng | Không lưu | **Mỗi triplet gắn `source_chunk`** để truy vết |
> | Cost | Trung bình | Cao hơn (nhiều LLM calls) |
> | Phù hợp | Dữ liệu lớn, batch | KG nhỏ, cần chính xác, tự điều chỉnh schema |
>
> **Analogies:** Pipeline batch giống dây chuyền nhà máy; agent giống **thợ lành nghề** — vừa xây vừa nhìn, thấy lỗi thì tháo ra sửa ngay, và ghi chú "viên gạch này lấy từ nguồn X".
>
> Các hệ thống điển hình: **KnoBuilder, KG-Agent** (tự trích triplet theo vòng lặp), **RAGA** (đánh giá chất lượng KG rồi cho agent sửa). Nghiên cứu 2025-2026 cho thấy agentic approach **giảm đáng kể triplets sai** so với batch single-pass, với chi phí cao hơn 2-3×. (triplet = bộ ba thực thể–quan hệ–thực thể; single-pass = chạy một lượt duy nhất.)

> 📄 **Code ví dụ:** [`examples/12-7-agentic-kg-construction.py`](examples/12-7-agentic-kg-construction.py)

> **Tóm gọn 1 câu:** Agent tự xây tự sửa graph cho chính xác và truy vết được nguồn, đổi lại tốn 2-3 lần chi phí — hợp với graph nhỏ cần chất lượng cao.

---

## 8. Labs Thực Hành

> Phần này là 3 bài tập tay: trích KG từ 5 tài liệu, so trích 1 vòng với 2 vòng, và chỉnh ngưỡng gộp trùng.

### Lab 1: Extract KG từ 5 Documents

- Viết script đọc 5 markdown files trong `data/raw_docs/`
- Chạy `extract_entities` + `extract_relations` cho từng file
- Merge và deduplicate, in ra số entities/relations

### Lab 2: So Sánh Single-Pass vs Gleaning

- Trích entities 1 lần (gleaning=0) vs 2 vòng (gleaning=2)
- Đo coverage: số entities trích được, so sánh precision thủ công

### Lab 3: Deduplication Tuning

- Thử thresholds 0.80, 0.85, 0.90 cho `deduplicate_entities`
- Quan sát: threshold thấp → gộp quá tay (false positive), cao → sót trùng lặp

> **Tóm gọn 1 câu:** Làm đủ 3 lab để tự tay thấy: gleaning tăng độ phủ, ngưỡng gộp quyết định đúng/sai — đếm số node trước và sau mỗi lab.

---

## Tài Liệu Tham Khảo

- Microsoft GraphRAG — *Entity & Relationship Extraction* (https://microsoft.github.io/graphrag/)
- LangChain — *LLMGraphTransformer* (https://python.langchain.com/docs/use_cases/graph/constructing)
- spaCy — *Named Entity Recognition* (https://spacy.io/usage/linguistic-features#named-entities)
- Microsoft GraphRAG — *Claims Extraction Pattern* (https://microsoft.github.io/graphrag/)
- *Knowledge Graph Agent: An Agentic Construction Benchmark* — KnoBuilder/RAGA/KG-Agent (arXiv 2025)
- *Knowledge Graph Construction Survey* — Paulheim (2017)

---

## GraphRAG — Cập nhật 2026

Microsoft GraphRAG (2024-2025): dùng knowledge graph để enhance RAG. Query phức tạp (multi-hop) tốt hơn vector-only RAG.

**Tin mới 2025-2026:**
- **LazyGraphRAG** (Microsoft, cuối 2024): defer LLM summarisation tới query time — indexing cost ngang vector RAG, quality ngang full GraphRAG, query cost thấp hơn ~700×. Đã tích hợp Microsoft Discovery (2025) và Azure Local.
- **LightRAG** (HKUDS, EMNLP 2025): dual-layer graph + vector, incremental update thay vì re-index toàn bộ.
- **GraphRAG-Bench** (Microsoft, 06/2025): multi-hop + global queries GraphRAG thắng; single-hop factoid vanilla RAG thắng.
- **Gartner (2026)**: GraphRAG trong "Top Trends in D&A for 2026" cho complex cases mà high-accuracy RAG thất bại.
- **Knowledge Graph Market**: 1.48B USD (2025) → 2.04B USD (2026). GraphRAG chuyển từ "enterprise luxury" → production baseline.

Ref: https://microsoft.github.io/graphrag/

> **Tóm gọn 1 câu:** Tin mới 2025-2026: GraphRAG ngày càng rẻ (LazyGraphRAG, LightRAG) và đang thành chuẩn production; chi tiết trong bảng ở file GRAPH_ENGINEERING.md.

---

*Tiếp theo: [03 — Graph Storage & Query](../03-graph-storage/)*
