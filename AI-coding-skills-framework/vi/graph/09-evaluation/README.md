# 📊 09. Evaluation — Đánh Giá Chất Lượng Graph & GraphRAG

> ## 📑 Mục Lục
>
> - [Câu Chuyện Mở Đầu](#câu-chuyện-mở-đầu)
> - [Tại Sao Evaluation Quan Trọng?](#tại-sao-evaluation-quan-trọng)
> - [Tổng Quan](#tổng-quan)
> - [Nội Dung](#nội-dung)
> - [1. Graph Quality Metrics](#1-graph-quality-metrics)
> - [2. Retrieval Evaluation](#2-retrieval-evaluation)
> - [3. Generation Evaluation (RAG)](#3-generation-evaluation-rag)
> - [4. Knowledge Graph Completion Metrics](#4-knowledge-graph-completion-metrics)
> - [5. Benchmarks & Datasets](#5-benchmarks--datasets)
> - [6. Evaluation Framework](#6-evaluation-framework)
> - [7. Labs Thực Hành](#7-labs-thực-hành)
> - [Tài Liệu Tham Khảo](#tài-liệu-tham-khảo)

---

### Câu Chuyện Mở Đầu

Bạn đã xây xong GraphRAG, demo cho sếp: *"Hỏi gì cũng trả lời được!"*

Sếp hỏi 3 câu:

1. *"Dự án Phoenix ngân sách bao nhiêu?"* → Trả lời: "500 triệu" ✅ (đúng, trong doc)
2. *"Ai duyệt Phoenix?"* → Trả lời: "Alice" ✅ (đúng, nhưng confidence 0.6 — thấp!)
3. *"Team AI có bao nhiêu người?"* → Trả lời: "15 người" ❌ (doc ghi 10, LLM hallucinate)

Không có evaluation framework, bạn **không biết** GraphRAG đúng bao nhiêu %, hallucinate bao nhiêu %, và **tại sao** sai (extraction sai? retrieval sai? generation sai?).

**Evaluation là cách biến "demo hay" thành "production đáng tin".**

### Tại Sao Evaluation Quan Trọng?

> *"Không đo được thì không cải thiện được. Không tách được retrieval vs generation thì không biết sửa ở đâu."*
> — RAG Evaluation Best Practices (2024)

| # | Nguồn | Phát Hiện |
|---|-------|-----------|
| 1 | **Microsoft GraphRAG (2024)** | LLM-as-judge (comprehensiveness, diversity) phân biệt GraphRAG vs vanilla RAG với **p<0.01** |
| 2 | **RAGAS Framework (2024)** | Tách faithfulness (generation) vs context relevance (retrieval) giúp **giảm 50% debug time** |
| 3 | **OGB + FB15k-237** | KG completion: Hits@10 và MRR là metrics chuẩn — không dùng accuracy thuần |

---

## Tổng Quan

```
                    ┌─────────────────────────────────┐
                    │      EVALUATION FRAMEWORK        │
                    │                                  │
  Knowledge Graph ──►│  1. Graph Quality               │
  (nodes, edges)     │     Coverage, Density, Connectivity│
                     │                                  │
  Retrieval ────────►│  2. Retrieval Quality            │
  (subgraph, paths)  │     Precision, Recall, MRR, Path Precision│
                     │                                  │
  Generation ───────►│  3. Generation Quality           │
  (answer + citation)│     Faithfulness, Relevance, Hallucination│
                     │                                  │
  KG Completion ────►│  4. KG Completion                │
  (link prediction)  │     Hits@K, MRR, MR              │
                     │                                  │
                     └──────────────┬──────────────────┘
                                    │
                     ┌──────────────▼──────────────────┐
                     │  BENCHMARKS & REPORTING          │
                     │  HotpotQA, 2Wiki, Custom, Dashboard│
                     └─────────────────────────────────┘
```

---

## Nội Dung

| # | Chủ đề | Mô tả |
|---|--------|-------|
| 1 | [Graph Quality](#1-graph-quality-metrics) | Coverage, connectivity, density |
| 2 | [Retrieval](#2-retrieval-evaluation) | Precision, recall, MRR, path precision |
| 3 | [Generation](#3-generation-evaluation-rag) | Faithfulness, hallucination, LLM-as-judge |
| 4 | [KG Completion](#4-knowledge-graph-completion-metrics) | Hits@K, MRR, MR |
| 5 | [Benchmarks](#5-benchmarks--datasets) | HotpotQA, GraphRAG-Bench, KGHaluBench, evidence recall |
| 6 | [Framework](#6-evaluation-framework) | Code evaluation pipeline |

---

## 1. Graph Quality Metrics

> **📌 Khái Niệm Cơ Bản:**
> **Trước khi đánh giá "AI trả lời đúng không", phải đánh giá "graph có tốt không"?** Nếu graph thiếu sót hoặc sai, kết quả RAG dù code hoàn hảo cũng sẽ vô nghĩa (GIGO — garbage in, garbage out).
>
> **Có 9 thước đo để kiểm tra "sức khỏe" của graph.** Hình dung nôm na như sau:
>
> - **Node/Edge Coverage** = *độ phủ* — "trích xuất được bao nhiêu % sự thật từ documents?" Giống kiểm tra kiến thức: bỏ sót 30% kiến thức thì trả lời chỉ đúng 70%.
> - **Duplicate Rate** = *độ sạch* — "có bao nhiêu entities trùng lặp?" Giống danh bạ ghi "Nguyễn Văn A" và "NV A" thành 2 người → truy vấn bị chia cắt.
> - **Connectivity** = *độ liên thông* — "các nodes có nối liền nhau hay rời rạc?" Graph gãy làm nhiều mảnh → truy vấn multi-hop không đi sang được mảnh khác.
> - **Density / Avg Degree** = *độ dày* — graph quá thưa → thiếu kết nối; quá đặc → nhiễu.
> - **Isolated Nodes** = nodes **không có mối quan hệ nào** — vô dụng, chỉ tốn chỗ.
> - **Invalid Edge Rate** = edges **vi phạm quy tắc** (Person → MANAGES → Document) — 100% phải bằng 0.
> - **Temporal Freshness** = edge cũ **hết hạn** nhưng chưa cập nhật — trả lời bằng thông tin lỗi thời.

### 1.1 Metrics Cho Bản Thân Graph

Trước khi đo retrieval/generation, phải đo **graph có tốt không**:

```
┌──────────────────────┬──────────────────────────────────┬──────────────────────┐
│ Metric               │ Ý nghĩa                          │ Tốt khi              │
├──────────────────────┼──────────────────────────────────┼──────────────────────┤
│ Node Coverage        │ % entities thực tế được trích    │ Cao (>80%)           │
│ Edge Coverage        │ % relations thực tế được trích   │ Cao (>70%)           │
│ Duplicate Rate       │ % nodes trùng lặp (chưa dedup)   │ Thấp (<5%)           │
│ Connectivity         │ % nodes trong largest component  │ Cao (>90%)           │
│ Density              │ 2|E| / |V|(|V|-1)                │ Tùy domain           │
│ Avg Degree           │ Số quan hệ trung bình / node     │ 3-10 (enterprise)    │
│ Isolated Nodes       │ Nodes không có edge nào          │ Thấp (<5%)           │
│ Invalid Edge Rate    │ % edges vi phạm ontology         │ 0%                   │
│ Temporal Freshness   │ % edges còn valid (chưa expire)  │ Cao (>95%)           │
└──────────────────────┴──────────────────────────────────┴──────────────────────┘
```

<details>
<summary>Python Code — Graph Quality Metrics (Click để xem)</summary>

> 📄 **Code ví dụ:** [`examples/01-1-1-metrics-cho-ban-than-graph.py`](examples/01-1-1-metrics-cho-ban-than-graph.py)

</details>

### 1.2 Coverage — So Với Ground Truth

> 📄 **Code ví dụ:** [`examples/02-1-2-coverage-so-voi-ground-truth.py`](examples/02-1-2-coverage-so-voi-ground-truth.py)

---

## 2. Retrieval Evaluation

> **📌 Khái Niệm Cơ Bản:**
> **Retrieval Evaluation = đo "hệ thống tìm đúng thông tin không?"** Trước khi LLM trả lời, hệ thống phải *lấy đúng context từ graph*. Nếu retrieval lấy sai context → LLM trả lời sai dù model giỏi.
>
> **Analogies để nhớ 3 metrics chính:**
> - **Precision@k** = *độ chính xác* — "trong 5 thứ lấy ra, bao nhiêu cái ĐÚNG?" Lấy 5 nhưng 3 sai → precision thấp.
> - **Recall@k** = *độ đầy đủ* — "trong tổng N thứ đúng, mình bắt được bao nhiêu?" Có 10 sự thật nhưng chỉ lấy được 4 → recall thấp.
> - **MRR** = *độ nhanh gặp đúng* — "câu trả lời đúng nằm ở hạng bao nhiêu?" Đúng nằm đầu (rank 1) → điểm 1.0; nằm hạng 5 → 0.2.
>
> **Biểu thức Pre/Recall như phong phanh trong fishing:** Precision = trong rổ cá, mấy con ăn được. Recall = trong ao, mình vớt được bao nhiêu con cá có.

### 2.1 Metrics Cho Retrieval

```
┌──────────────────────┬──────────────────────────────────┬──────────────────────┐
│ Metric               │ Ý nghĩa                          │ Công thức            │
├──────────────────────┼──────────────────────────────────┼──────────────────────┤
│ Precision@K          │ % retrieved đúng trong top-K     │ |relevant ∩ retrieved| / K │
│ Recall@K             │ % ground truth được retrieve     │ |relevant ∩ retrieved| / |relevant| │
│ MRR (Mean Reciprocal)│ Vị trí trung bình của đáp án đúng│ mean(1/rank)         │
│ Path Precision       │ % paths trả về là đúng           │ |correct paths| / |all paths| │
│ Context Relevance    │ Retrieved context có liên quan?  │ LLM-as-judge (0-1)   │
│ Hop Accuracy         │ Số hops có đúng không?           │ |correct hops| / |total| │
└──────────────────────┴──────────────────────────────────┴──────────────────────┘
```

<details>
<summary>Python Code — Retrieval Evaluation (Click để xem)</summary>

> 📄 **Code ví dụ:** [`examples/03-2-1-metrics-cho-retrieval.py`](examples/03-2-1-metrics-cho-retrieval.py)

</details>

### 2.2 So Sánh Vanilla RAG vs GraphRAG Retrieval

> 📄 **Code ví dụ:** [`examples/04-2-2-so-sanh-vanilla-rag-vs-graphrag.py`](examples/04-2-2-so-sanh-vanilla-rag-vs-graphrag.py)

---

## 3. Generation Evaluation (RAG)

### 3.1 RAGAS-Style Metrics

> **📌 Khái Niệm Cơ Bản:**
> **2 câu hỏi quan trọng nhất về chất lượng câu trả lời RAG:**
> - **Faithfulness (trung thành)** = *Có bịa không?* — mỗi claim (lời khẳng định) trong câu trả lời phải **nằm trong context** lấy từ graph. "Phoenix ngân sách 700 triệu" mà graph không có → không trung thành → hallucination.
> - **Answer Relevance (đáng trả lời)** = *Có trả lời đúng câu hỏi không?* — trả lời dài dòng nhưng không trúng câu hỏi = điểm thấp.
>
> **Analogies:** Faithfulness = "nhân chứng có khai bám vào bằng chứng không hay tự bịa?" Answer Relevance = "trả lời có đúng trọng tâm câu hỏi không?"
>
> **Cách đo (LLM-as-judge):** Tách câu trả lời thành các **claims** (mệnh đề nhỏ) → kiểm tra từng claim có trong context không. Hallucination Rate = 1 - Faithfulness.

```
┌──────────────────────┬──────────────────────────────────┬──────────────────────┐
│ Metric               │ Ý nghĩa                          │ Đo thế nào           │
├──────────────────────┼──────────────────────────────────┼──────────────────────┤
│ Faithfulness         │ Câu trả lời có grounded trong    │ LLM-as-judge: claims │
│                      │ context không? (không bịa)       │ có trong context?    │
│ Answer Relevance     │ Câu trả lời có trả lời đúng      │ LLM-as-judge: câu trả│
│                      │ câu hỏi không?                   │ lời liên quan?       │
│ Context Precision    │ Context có chứa thông tin cần?   │ LLM-as-judge         │
│ Hallucination Rate   │ % claims không có trong context  │ 1 - faithfulness     │
│ Citation Accuracy    │ % citations trỏ đúng source      │ Check path/source    │
└──────────────────────┴──────────────────────────────────┴──────────────────────┘
```

<details>
<summary>Python Code — Faithfulness & Hallucination Detection (Click để xem)</summary>

> 📄 **Code ví dụ:** [`examples/05-3-1-ragas-style-metrics.py`](examples/05-3-1-ragas-style-metrics.py)

</details>

### 3.2 LLM-as-Judge Cho Global Sensemaking (Microsoft Pattern)

> 📄 **Code ví dụ:** [`examples/06-3-2-llm-as-judge-cho-global-sensemaking.py`](examples/06-3-2-llm-as-judge-cho-global-sensemaking.py)

---

## 4. Knowledge Graph Completion Metrics

Cho link prediction / KG completion (GNN, TransE, v.v.):

```
┌──────────────┬──────────────────────────────────┬──────────────────────┐
│ Metric       │ Ý nghĩa                          │ Tốt khi              │
├──────────────┼──────────────────────────────────┼──────────────────────┤
│ Hits@K       │ % đáp án đúng trong top-K        │ Cao (Hits@10 > 0.5)  │
│ MRR          │ Mean Reciprocal Rank             │ Cao (>0.3)           │
│ MR (Mean Rank)│ Vị trí trung bình của đáp án    │ Thấp (<100)          │
│ AUC          │ Area under ROC cho link predict  │ Cao (>0.8)           │
└──────────────┴──────────────────────────────────┴──────────────────────┘
```

<details>
<summary>Python Code — KG Completion Evaluation (Click để xem)</summary>

> 📄 **Code ví dụ:** [`examples/07-4-knowledge-graph-completion-metrics.py`](examples/07-4-knowledge-graph-completion-metrics.py)

</details>

---

## 5. Benchmarks & Datasets

### 5.1 Benchmarks Cho GraphRAG

```
┌──────────────────────┬──────────────────────┬──────────────────────────────┐
│ Benchmark            │ Task                 │ Metric                       │
├──────────────────────┼──────────────────────┼──────────────────────────────┤
│ HotpotQA             │ Multi-hop QA (2 hops)│ EM, F1                       │
│ 2WikiMultihopQA      │ Multi-hop (2-4 hops) │ EM, F1                       │
│ MuSiQue              │ Multi-hop (2-4 hops) │ EM, F1 (khó hơn)             │
│ Natural Questions    │ Open-domain QA       │ EM                           │
│ GraphRAG-Bench (MSFT)│ Domain KGQA, 1018 câu│ Multi-hop + single-hop +   │
│                      │ 5 dạng câu hỏi       │ explainability (reasoning)  │
│ KGHaluBench          │ KG-rag hallucination │ Hallucination rate           │
│ Custom Enterprise QA │ Domain-specific      │ Faithfulness, P@K, MRR       │
└──────────────────────┴──────────────────────┴──────────────────────────────┘
```

### 5.2 Benchmarks Cho KG Completion

```
┌──────────────────────┬──────────────────────┬──────────────────────────────┐
│ Benchmark            │ Triples              │ Metric                       │
├──────────────────────┼──────────────────────┼──────────────────────────────┤
│ FB15k-237            │ 310K (Freebase)      │ Hits@10, MRR                 │
│ WN18RR               │ 93K (WordNet)        │ Hits@10, MRR                 │
│ OGB-WikiKG2          │ 17M (Wikidata)       │ MRR                          │
│ Custom Enterprise KG │ Tùy domain           │ Hits@K, coverage             │
└──────────────────────┴──────────────────────┴──────────────────────────────┘
```

### 5.3 Tạo Custom Benchmark

> 📄 **Code ví dụ:** [`examples/08-5-3-tao-custom-benchmark.py`](examples/08-5-3-tao-custom-benchmark.py)

### 5.4 Những "Lỗ Hổng Đánh Giá" Trong GraphRAG (2025-2026)

> **📌 Khái Niệm Cơ Bản — đánh giá GraphRAG chỉ đo retrieval/faithfulness là CHƯA đủ.** Nghiên cứu mới chỉ ra 3 thiếu hụt hay gặp trong pipeline đánh giá hiện tại:

**1. Thiếu "Evidence Recall" & "Context Relevancy"** — Hầu hết hệ thống chỉ đo *"câu trả lời có khớp đáp án không"* (EM/F1) mà không đo *"chứng cớ đưa vào LLM có đúng/đủ không"*.
- **Evidence Recall** = trong các bằng chứng LLM nhận được (chunks + path graph), bao nhiêu % **thực sự cần để trả lời** câu hỏi đó đã được đưa vào.
- **Context Relevancy** = bằng chứng đưa vào có **dư thừa ngoài lề** bao nhiêu. Đo bằng câu hỏi nhỏ: *"Trong context này, câu nào không giúp trả lời câu hỏi?"*
- Vì sao quan trọng: EM/F1 cao mà evidence lệch → system không tin tưởng được (retrieval sai nhưng LLM "mạnh miệng" đoán trúng — *lucky*).

**2. Retrieval Drift (CS-RAG)** — Hệ thống RAG nhiều bước (như agentic/DRIFT) có thể **lệch hướng** giữa chừng: bước 1 đúng anchor nhưng bước 2 không theo hướng câu hỏi nữa → trả lời trôi ra ngoài. Cách đo: giám sát **độ 'bám câu hỏi'** của từng hop retrieval (attention/score của hop với câu hỏi gốc).

**3. KGHaluBench & Hallucination đặc thù KG** — Hallucination trong GraphRAG có 2 nguồn khác vanilla RAG:
- **Graph hallucination**: KG tự xây bị trích sai triplet (entity Linking sai → answer kéo theo sai).
- **Summary hallucination**: community summary của LLM "bịa" chi tiết không có trong graph.
- **KGHaluBench** đo riêng rate hallucination khi bối cảnh gốc là graph thay vì text. Cần đánh giá **riêng từng nguồn** — đừng gộp chung vào 1 chỉ số faithfulness.

**4. Systematic Eval RAG vs GraphRAG — đừng tự tin thái quá** — Kết quả benchmark có hệ thống 2025-2026: GraphRAG thắng trên multi-hop/global nhưng **thua vanilla RAG trên single-hop/factoid**. Vì vậy evaluation của bạn nên **chia 3 track** (single-hop / multi-hop / global) và báo cáo riêng — như Module 05 đã cảnh báo.

> 📄 **Code ví dụ:** [`examples/09-5-4-nhung-lo-hong-anh-gia-trong.py`](examples/09-5-4-nhung-lo-hong-anh-gia-trong.py)

---

## 6. Evaluation Framework

<details>
<summary>Python Code — Complete Evaluation Pipeline (Click để xem)</summary>

> 📄 **Code ví dụ:** [`examples/10-6-evaluation-framework.py`](examples/10-6-evaluation-framework.py)

</details>

---

## 7. Labs Thực Hành

### Lab 1: Đánh Giá Graph Quality

1. Tạo 2 graphs: 1 tốt (đầy đủ, connected) và 1 tệ (nhiều isolated, duplicate)
2. Chạy `evaluate_graph_quality` cho cả 2, so sánh metrics

### Lab 2: So Sánh Vanilla RAG vs GraphRAG

1. Chuẩn bị 20 queries với ground truth `relevant` docs
2. Chạy cả 2 retrievers, đo P@5, R@5, MRR
3. Dùng `llm_judge` cho 5 global queries — GraphRAG phải thắng

### Lab 3: Hallucination Measurement

1. Tạo 20 QA pairs với `context` + `expected answer`
2. Cho LLM generate với context đúng vs không có context
3. Đo faithfulness — có context phải >0.8, không context hallucination cao

---

## Tài Liệu Tham Khảo

- Microsoft GraphRAG — *Evaluation: LLM-as-Judge* (https://microsoft.github.io/graphrag/)
- RAGAS — *RAG Assessment* (https://docs.ragas.io/)
- OGB — *Open Graph Benchmark Evaluation* (https://ogb.stanford.edu/docs/score/)
- HotpotQA — *Leaderboard* (https://hotpotqa.github.io/)
- *GraphRAG-Bench: A Domain-Specific Benchmark for GraphRAG* (arXiv:2506.02404) — 1018 câu, 5 dạng
- *KGHaluBench* — KG-augmented hallucination benchmark (2025)
- *CS-RAG: Retrieval Drift in Multi-Step RAG* (2025)
- *RAG vs GraphRAG: A Systematic Evaluation* (arXiv 2025) — tách 3 track single/multi/global
- *A Survey on Evaluation of Knowledge Graph Quality* — Paulheim (2017)

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

*Hoàn thành Graph Engineering Track — quay lại [README](../README.md) để tổng kết.*
