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

Giải thích 3 từ khóa: **hallucinate** = bịa ra thông tin không có trong dữ liệu; **extraction** = bước trích xuất thực thể/quan hệ từ tài liệu vào graph; **retrieval** = bước tìm dữ liệu trong graph; **generation** = bước LLM viết câu trả lời. Lỗi có thể nằm ở bất kỳ bước nào — evaluation là cách chỉ ra bước nào.

**Evaluation là cách biến "demo hay" thành "production đáng tin".**

> **Tóm gọn 1 câu:** Demo trả lời ngon chưa đủ — cần bộ đo để biết hệ thống đúng bao nhiêu phần trăm, bịa bao nhiêu, và sai ở bước nào.

### Tại Sao Evaluation Quan Trọng?

> *"Không đo được thì không cải thiện được. Không tách được retrieval vs generation thì không biết sửa ở đâu."*
> — RAG Evaluation Best Practices (2024)

Cách đọc bảng này: mỗi dòng là một nghiên cứu; cột **Phát Hiện** ghi điều được đo ra. Ví dụ dòng 1: **LLM-as-judge** = dùng một LLM khác làm "giám khảo" chấm câu trả lời, với 2 tiêu chí comprehensiveness (đầy đủ) và diversity (đa chiều); **p<0.01** = khác biệt có ý nghĩa thống kê, không phải trùng hợp.

| # | Nguồn | Phát Hiện |
|---|-------|-----------|
| 1 | **Microsoft GraphRAG (2024)** | LLM-as-judge (comprehensiveness, diversity) phân biệt GraphRAG vs vanilla RAG với **p<0.01** |
| 2 | **RAGAS Framework (2024)** | Tách faithfulness (generation) vs context relevance (retrieval) giúp **giảm 50% debug time** |
| 3 | **OGB + FB15k-237** | KG completion: Hits@10 và MRR là metrics chuẩn — không dùng accuracy thuần |

> **Tóm gọn 1 câu:** Nghiên cứu chỉ ra: tách chỉ số theo từng giai đoạn (tìm — trả lời — dự đoán) là cách đánh giá chuẩn, và nó rút ngắn việc truy lỗi đi một nửa.

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

Đọc sơ đồ này thế nào: bên trái là 4 thứ cần đo (bản thân graph, phần tìm, phần trả lời, phần dự đoán quan hệ), giữa là bộ chỉ số tương ứng, dưới là các bộ đề thi chuẩn (**benchmark**) và bảng báo cáo (**dashboard** = trang theo dõi số liệu trực quan).

> **Tóm gọn 1 câu:** Framework đánh giá gồm 4 lớp đo đúng theo 4 giai đoạn của pipeline, gom về các benchmark chuẩn và bảng báo cáo.

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

Cách đọc bảng này: 6 nhóm chỉ số theo thứ tự đọc. Ví dụ dòng 1: *Coverage, connectivity, density* = độ phủ, độ liên thông, độ dày — ba thước đo "graph có đầy đủ và liền mạch không".

> **Tóm gọn 1 câu:** Đo theo thứ tự: graph khỏe → tìm đúng → trả lời trung thành → dự đoán chính xác, rồi mới so trên benchmark chuẩn.

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

> **Tóm gọn 1 câu:** Đo sức khỏe graph bằng 9 thước (phủ, sạch, liên thông, dày vừa, ít node cô lập, không vi phạm, còn tươi) — graph xấu thì mọi chỉ số phía sau đều vô nghĩa.

### 1.1 Metrics Cho Bản Thân Graph

Trước khi đo retrieval/generation, phải đo **graph có tốt không**:

Cách đọc bảng này: cột **Ý nghĩa** định nghĩa chỉ số, cột **Tốt khi** cho ngưỡng nên đạt. Ví dụ: *Node Coverage > 80%* nghĩa là hơn 80% thực thể thật trong tài liệu đã được trích vào graph; *Invalid Edge Rate = 0%* nghĩa là không được có cạnh nào vi phạm quy tắc ontology (**ontology** = bộ quy tắc định nghĩa loại node/edge được phép có).

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

> **Tóm gọn 1 câu:** Chín chỉ số trên là "bảng khám sức khỏe" của graph — mỗi cái có ngưỡng rõ ràng, cái nào dưới ngưỡng thì sửa cái đó trước.

<details>
<summary>Python Code — Graph Quality Metrics (Click để xem)</summary>

> 📄 **Code ví dụ:** [`examples/01-1-1-metrics-cho-ban-than-graph.py`](examples/01-1-1-metrics-cho-ban-than-graph.py)

</details>

### 1.2 Coverage — So Với Ground Truth

> 📄 **Code ví dụ:** [`examples/02-1-2-coverage-so-voi-ground-truth.py`](examples/02-1-2-coverage-so-voi-ground-truth.py)

> **Tóm gọn 1 câu:** Coverage = so graph với "đáp án chuẩn" (ground truth) do người làm thủ công, để biết trích xuất hụt bao nhiêu phần trăm sự thật.

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

> **Tóm gọn 1 câu:** Retrieval evaluation = đo phần "tìm" bằng 3 chỉ số: lấy ra đúng mấy (precision), bắt đủ mấy (recall), đáp án đúng đứng hạng mấy (MRR) — tìm sai thì LLM giỏi mấy cũng trả lời sai.

### 2.1 Metrics Cho Retrieval

Cách đọc bảng này: cột **Ý nghĩa** định nghĩa chỉ số, cột **Công thức** cho cách tính. Ví dụ: *Precision@K* = trong K kết quả lấy ra, bao nhiêu % là đúng; *ground truth* = đáp án chuẩn đã biết trước; *Hop Accuracy* = độ chính xác của từng bước đi trên graph (**hop** = 1 bước nhảy từ node này sang node kề nó).

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

> **Tóm gọn 1 câu:** Sáu chỉ số trên đo phần "tìm": trúng mấy trong K kết quả đầu, bắt đủ chưa, đúng đứng hạng mấy, và từng bước đi trên graph có đúng không.

<details>
<summary>Python Code — Retrieval Evaluation (Click để xem)</summary>

> 📄 **Code ví dụ:** [`examples/03-2-1-metrics-cho-retrieval.py`](examples/03-2-1-metrics-cho-retrieval.py)

</details>

### 2.2 So Sánh Vanilla RAG vs GraphRAG Retrieval

> 📄 **Code ví dụ:** [`examples/04-2-2-so-sanh-vanilla-rag-vs-graphrag.py`](examples/04-2-2-so-sanh-vanilla-rag-vs-graphrag.py)

> **Tóm gọn 1 câu:** Chạy cả hai hệ thống trên cùng bộ câu hỏi, đo P@5/R@5/MRR riêng — GraphRAG phải thắng ở câu nhiều bước, còn vanilla RAG thường thắng ở câu tra cứu đơn giản.

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

> **Tóm gọn 1 câu:** Hai câu hỏi chính cho phần trả lời: "có bịa không" (faithfulness) và "có trúng câu hỏi không" (answer relevance) — đo bằng cách tách mệnh đề rồi cho LLM khác làm giám khảo.

Cách đọc bảng này: cột **Ý nghĩa** định nghĩa, cột **Đo thế nào** cho cách đo. Ví dụ: *Hallucination Rate = 1 - faithfulness* nghĩa là tỉ lệ bịa bằng 100% trừ đi độ trung thành — trung thành 0.9 thì bịa 10%.

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

> **Tóm gọn 1 câu:** Năm chỉ số RAGAS-style đo chất lượng câu trả lời: không bịa, trúng câu hỏi, context có ích, tỉ lệ bịa thấp, trích dẫn đúng nguồn.

<details>
<summary>Python Code — Faithfulness & Hallucination Detection (Click để xem)</summary>

> 📄 **Code ví dụ:** [`examples/05-3-1-ragas-style-metrics.py`](examples/05-3-1-ragas-style-metrics.py)

</details>

### 3.2 LLM-as-Judge Cho Global Sensemaking (Microsoft Pattern)

> 📄 **Code ví dụ:** [`examples/06-3-2-llm-as-judge-cho-global-sensemaking.py`](examples/06-3-2-llm-as-judge-cho-global-sensemaking.py)

> **Tóm gọn 1 câu:** Với câu hỏi tổng hợp ("cả tổ chức đang làm gì?") không có đáp án đúng duy nhất — dùng LLM làm giám khảo chấm theo độ đầy đủ và đa chiều.

---

## 4. Knowledge Graph Completion Metrics

Cho link prediction / KG completion (GNN, TransE, v.v.):

Cách đọc bảng này: đây là các chỉ số cho bài "đoán quan hệ còn thiếu". Ví dụ: *Hits@10 > 0.5* = hơn 50% câu hỏi có đáp án đúng nằm trong 10 gợi ý đầu; *MR < 100* = đáp án đúng trung bình đứng dưới hạng 100; *AUC > 0.8* = model phân biệt tốt giữa quan hệ có thật và quan hệ bịa.

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

> **Tóm gọn 1 câu:** Đo dự đoán quan hệ bằng thứ hạng (Hits@K, MRR, MR) chứ không dùng accuracy thuần — vì người dùng thật chỉ đọc vài gợi ý đầu.

<details>
<summary>Python Code — KG Completion Evaluation (Click để xem)</summary>

> 📄 **Code ví dụ:** [`examples/07-4-knowledge-graph-completion-metrics.py`](examples/07-4-knowledge-graph-completion-metrics.py)

</details>

---

## 5. Benchmarks & Datasets

### 5.1 Benchmarks Cho GraphRAG

Cách đọc bảng này: mỗi dòng là một "đề thi" sẵn có (**benchmark** = bộ câu hỏi + đáp án chuẩn để so sánh các hệ thống). Ví dụ: *HotpotQA* = 2-hop QA (**QA** = question answering, hỏi-đáp); *EM, F1* = khớp chữ chính xác / điểm hài hòa; *KGHaluBench* = đề thi chuyên đo tỉ lệ bịa khi dùng graph.

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

> **Tóm gọn 1 câu:** Dùng đề thi sẵn (HotpotQA, GraphRAG-Bench...) cho nhanh, nhưng với dữ liệu nội bộ thì phải tự tạo benchmark riêng theo domain của mình.

### 5.2 Benchmarks Cho KG Completion

Cách đọc bảng này: mỗi dòng là một bộ dữ liệu chuẩn cho bài "điền thiếu quan hệ" (**triple** = bộ 3 *chủ ngữ–quan hệ–tân ngữ*, ví dụ `Alice —WORKS_ON→ Phoenix`). Ví dụ: *FB15k-237* có 310 nghìn triple từ Freebase của Google; *OGB-WikiKG2* tới 17 triệu triple từ Wikidata.

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

> **Tóm gọn 1 câu:** So model với nhau trên các bộ triple chuẩn (FB15k-237, WN18RR, OGB-WikiKG2) bằng Hits@10 và MRR — không so bằng cảm tính.

### 5.3 Tạo Custom Benchmark

> 📄 **Code ví dụ:** [`examples/08-5-3-tao-custom-benchmark.py`](examples/08-5-3-tao-custom-benchmark.py)

> **Tóm gọn 1 câu:** Benchmark riêng = lấy câu hỏi thật của người dùng + đáp án chuẩn do người kiểm tra, để đo hệ thống trên đúng dữ liệu của mình.

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

**4. Systematic Eval RAG vs GraphRAG — đừng tự tin thái quá** — Kết quả benchmark có hệ thống 2025-2026: GraphRAG thắng trên multi-hop/global nhưng **thua vanilla RAG trên single-hop/factoid**. (**Single-hop/factoid** = câu hỏi tra cứu một ý, ví dụ "Phoenix ngân sách bao nhiêu?".) Vì vậy evaluation của bạn nên **chia 3 track** (single-hop / multi-hop / global) và báo cáo riêng — như Module 05 đã cảnh báo.

> 📄 **Code ví dụ:** [`examples/09-5-4-nhung-lo-hong-anh-gia-trong.py`](examples/09-5-4-nhung-lo-hong-anh-gia-trong.py)

> **Tóm gọn 1 câu:** Điểm số tổng hợp che giấu lỗi — phải đo thêm bằng chứng đưa vào, theo dõi trôi hướng ở từng bước, và báo riêng tỉ lệ bịa từ graph và từ tóm tắt.

---

## 6. Evaluation Framework

<details>
<summary>Python Code — Complete Evaluation Pipeline (Click để xem)</summary>

> 📄 **Code ví dụ:** [`examples/10-6-evaluation-framework.py`](examples/10-6-evaluation-framework.py)

</details>

> **Tóm gọn 1 câu:** Pipeline đánh giá hoàn chỉnh = chạy cả 4 lớp đo (graph, retrieval, generation, KG completion) trong một lần, xuất ra báo cáo so sánh được theo từng phiên bản.

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

> **Tóm gọn 1 câu:** Ba lab chứng minh rằng bộ đo của bạn "bắt được" khác biệt: graph tệ phải ra điểm tệ, GraphRAG phải thắng câu nhiều bước, và không có context thì tỉ lệ bịa phải tăng.

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

> **Tóm gọn 1 câu:** Đây là nguồn gốc của từng chỉ số trong bài — đọc thêm khi cần dẫn chứng hoặc đi sâu.

---

## GraphRAG — Cập nhật 2026

Microsoft GraphRAG (2024-2025): dùng knowledge graph để enhance RAG. Query phức tạp (multi-hop) tốt hơn vector-only RAG. (**Multi-hop** = câu hỏi phải đi qua nhiều bước quan hệ; **RAG** = đưa tài liệu liên quan vào prompt trước khi LLM trả lời.)

**Tin mới 2025-2026:**
- **LazyGraphRAG** (Microsoft, cuối 2024): defer LLM summarisation tới query time — indexing cost ngang vector RAG, quality ngang full GraphRAG, query cost thấp hơn ~700×. Đã tích hợp Microsoft Discovery (2025) và Azure Local.
- **LightRAG** (HKUDS, EMNLP 2025): dual-layer graph + vector, incremental update thay vì re-index toàn bộ.
- **GraphRAG-Bench** (Microsoft, 06/2025): multi-hop + global queries GraphRAG thắng; single-hop factoid vanilla RAG thắng.
- **Gartner (2026)**: GraphRAG trong "Top Trends in D&A for 2026" cho complex cases mà high-accuracy RAG thất bại.
- **Knowledge Graph Market**: 1.48B USD (2025) → 2.04B USD (2026). GraphRAG chuyển từ "enterprise luxury" → production baseline.

Ref: https://microsoft.github.io/graphrag/

> **Tóm gọn 1 câu:** GraphRAG đã thành chuẩn production (chi phí xuống ngang vector RAG nhờ LazyGraphRAG) — nên đo nó theo chuẩn production cũng là chuyện cần làm ngay.

*Hoàn thành Graph Engineering Track — quay lại [README](../README.md) để tổng kết.*
