# 🧩 06. Graph Reasoning — Suy Luận Trên Đồ Thị

> ## 📑 Mục Lục
>
> - [Câu Chuyện Mở Đầu](#câu-chuyện-mở-đầu)
> - [Tại Sao Graph Reasoning Quan Trọng?](#tại-sao-graph-reasoning-quan-trọng)
> - [Tổng Quan](#tổng-quan)
> - [Nội Dung](#nội-dung)
> - [1. Traversal Strategies](#1-traversal-strategies)
> - [2. Path Finding](#2-path-finding)
> - [3. Inference Rules & Reasoning](#3-inference-rules--reasoning)
> - [4. Community Detection & Centrality](#4-community-detection--centrality)
> - [5. Temporal Reasoning](#5-temporal-reasoning)
> - [6. Triển Khai Reasoning Engine](#6-triển-khai-reasoning-engine)
> - [7. Labs Thực Hành](#7-labs-thực-hành)
> - [Tài Liệu Tham Khảo](#tài-liệu-tham-khảo)

---

### Câu Chuyện Mở Đầu

Bạn có Knowledge Graph:

```
Alice —[MANAGES]→ Bob —[WORKS_ON]→ Phoenix
  │
  └──[KNOWS]→ Carol —[WORKS_ON]→ Atlas (AI Platform)
```

Bạn hỏi: *"Team của Alice có ai làm AI không?"*

Đây **không phải** câu hỏi lookup — mà là **suy luận**:

1. `MANAGES` là transitive? Alice quản lý Bob, Bob có thuộc "team của Alice" không?
2. `WORKS_ON → Atlas` có phải là "làm AI" không? Atlas có property `domain: AI` không?
3. Có cần traverse `Alice → Bob → Phoenix → Atlas` (3 hops) để nối?

**Graph Reasoning** biến những câu hỏi mơ hồ này thành **logic có thể thực thi**: rules, path constraints, và inference chains có thể verify.

> **Tóm gọn 1 câu:** Graph Reasoning = biến câu hỏi mơ hồ ("team của Alice có ai làm AI?") thành chuỗi bước logic máy chạy được và kiểm chứng được.

### Tại Sao Graph Reasoning Quan Trọng?

> *"Retrieval finds facts. Reasoning connects them into answers you didn't know to ask for."*
>
> (Dịch: truy xuất tìm ra sự kiện; suy luận nối chúng thành câu trả lời mà bạn chưa nghĩ ra cách hỏi.)

> **Cách đọc bảng này:** mỗi dòng là 1 nghiên cứu/benchmark; cột "Phát Hiện" nói nó đo được điều gì. Ví dụ, dòng 1: câu hỏi cần nối 2+ bước suy luận chính xác hơn 27% khi đi qua graph.

| # | Nguồn | Phát Hiện |
|---|-------|-----------|
| 1 | **HotpotQA Benchmark** | Multi-hop reasoning trên graph tăng **27% accuracy** vs single-hop retrieval |
| 2 | **Neo4j GDS (2024)** | Shortest path + centrality giúp phát hiện **bottleneck persons** giảm 40% approval time |
| 3 | **Temporal KG Papers (2024)** | Temporal reasoning giảm **35% stale answers** (trả lời bằng thông tin đã hết hạn) |

---

## Tổng Quan

Sơ đồ liệt kê 5 "bộ kỹ năng" của reasoning: đi thăm graph, tìm đường, suy ra quan hệ mới, đo tầm quan trọng, và xử lý theo thời gian.

```
Knowledge Graph
    │
    ├──► Traversal (BFS/DFS, constrained)
    │      "Tìm tất cả nodes cách Alice 2 hops qua MANAGES/WORKS_ON"
    │
    ├──► Path Finding (shortest, all-paths, weighted)
    │      "Đường ngắn nhất giữa Bob và project AI nào?"
    │
    ├──► Inference (rules, transitivity, composition)
    │      "Nếu A MANAGES B và B WORKS_ON P → A INDIRECTLY_MANAGES P"
    │
    ├──► Community & Centrality
    │      "Ai là người quan trọng nhất trong org?"
    │
    └──► Temporal (valid_from/until, event ordering)
           "Ai quản lý team AI vào Q2/2024?"
```

---

## Nội Dung

> **Cách đọc bảng này:** cột "Chủ đề" là mục con bên dưới; cột "Mô tả" tóm tắt mục đó gồm những gì. Ví dụ, dòng 3 nói: phần Inference dạy viết luật để suy ra quan hệ chưa có trong graph.

| # | Chủ đề | Mô tả |
|---|--------|-------|
| 1 | [Traversal](#1-traversal-strategies) | BFS, DFS, constrained traversal, sampling |
| 2 | [Path Finding](#2-path-finding) | Shortest path, all paths, weighted, k-shortest |
| 3 | [Inference](#3-inference-rules--reasoning) | Rules, transitivity, composition, OWL-lite |
| 4 | [Community & Centrality](#4-community-detection--centrality) | Leiden, Louvain, PageRank, betweenness |
| 5 | [Temporal](#5-temporal-reasoning) | Time-aware traversal, versioning, expiration |
| 6 | [Engine](#6-triển-khai-reasoning-engine) | Code reasoning engine hoàn chỉnh |
| 7 | [Neuro-Symbolic QA](#7-neuro-symbolic-qa) | Think-on-Graph, KG-Agent, Planner-Executor-Reasoner |

---

## 1. Traversal Strategies

> **📌 Khái Niệm Cơ Bản:**
> **Traversal = "đi thăm" graph** — bắt đầu từ 1 node, lần lượt ghé qua các nodes khác theo mối quan hệ. Giống như "theo dõi" ai đó trên mạng xã hội: bắt đầu từ mình, xem bạn bè của mình → rồi xem bạn bè của bạn mình → tiếp tục...
>
> **3 kiểu đi:**
> - **BFS (Breadth-First)** = "Đi theo vòng tròn" — thăm tất cả nodes cách 1 hop trước, rồi tới 2 hops, 3 hops... **Ví von:** như đổ nước lên mặt lưới — nước lan đều ra xung quanh trước khi thấm sâu hơn
> - **DFS (Depth-First)** = "Đi hết một nhánh trước" — đi sâu tới cùng một đường, quay lại rồi mới rẽ sang đường khác. **Ví von:** như đi một con đường cho tới cuối rồi mới quay lại ngã rẽ
> - **Constrained** = BFS/DFS có điều kiện — chỉ đi qua nodes/edges thỏa điều kiện (ví dụ: chỉ qua `MANAGES` edges, chỉ đến Person nodes)

### 1.1 BFS vs DFS vs Constrained

```
Graph: Alice → Bob → Carol
         │      │
         └────→ Dave → Eve

BFS từ Alice (level-order):       DFS từ Alice (depth-first):
  Level 0: Alice                    Path 1: Alice → Bob → Carol (dead end, backtrack)
  Level 1: Bob, Dave                Path 2: Alice → Bob → Dave → Eve
  Level 2: Carol, Eve

Constrained BFS (chỉ qua MANAGES):
  Alice —[MANAGES]→ Bob —[MANAGES]→ Carol  ✅
  Alice —[KNOWS]→ Dave                     ❌ (bị filter)
```

**Khi nào chọn BFS, DFS?**

> **Cách đọc bảng này:** mỗi dòng là 1 tình huống và kiểu đi nên chọn. Ví dụ, muốn biết tất cả node cách 1-2 bước → chọn BFS vì nó quét đủ từng vòng trước khi đi sâu.

| Tình huống | Chọn | Lý do |
|-----------|------|-------|
| Muốn biết tất cả nodes cách 1-2 hops | **BFS** | Đảm bảo tìm được tất cả trước khi đi sâu |
| Muốn tìm đường ngắn nhất | **BFS** | BFS luôn tìm đường ngắn nhất đầu tiên |
| Muốn tìm đường bất kỳ, kiểm tra tồn tại | **DFS** | Nhanh hơn BFS khi chỉ cần kiểm tra có đường hay không |
| Graph lớn, cần giới hạn số nodes thăm | **Sampled BFS** | BFS có sampling, không visit hết |
| Chỉ cần nodes thỏa điều kiện | **Constrained BFS** | Kết hợp BFS + filter |

<details>
<summary>Python Code — Constrained Traversal (Click để xem)</summary>

> 📄 **Code ví dụ:** [`examples/01-1-1-bfs-vs-dfs-vs-constrained.py`](examples/01-1-1-bfs-vs-dfs-vs-constrained.py)

</details>

### 1.2 Sampling Cho Graph Lớn

Trên graph 1M+ nodes, không thể traverse toàn bộ:

> 📄 **Code ví dụ:** [`examples/02-1-2-sampling-cho-graph-lon.py`](examples/02-1-2-sampling-cho-graph-lon.py)

> **Tóm gọn 1 câu:** BFS quét theo vòng, DFS đi sâu từng nhánh — và với graph lớn luôn phải đặt điều kiện hoặc lấy mẫu, không chạy không ràng buộc.

---

## 2. Path Finding

> **📌 Khái Niệm Cơ Bản:**
> **Path Finding = tìm "con đường" nối 2 nodes trong graph.** Giống như Google Maps: từ điểm A đến điểm B có thể đi nhiều đường khác nhau, và bạn muốn tìm đường tối ưu theo tiêu chí (ít bước, nhanh nhất, đáng tin nhất).
>
> **Khi nào cần trong Agent?**
> - "Liên hệ Alice thông qua ai?" → shortest path Alice → Bob (sếp chung)
> - "Bob có mấy cách tiếp cận Project Atlas?" → all paths, giới hạn 4 hops
> - "Tìm đường đáng tin nhất (confidence cao)" → weighted shortest using confidence as weight

### 2.1 Các Loại Path Finding

> **Đọc bảng này như sau:** Mỗi loại trả lời 1 câu hỏi khác nhau — *cùng bộ dữ liệu nhưng "ý nghĩa đường đi" khác nhau*.

```
┌────────────────────┬──────────────────────────────────┬──────────────────┐
│ Loại               │ Trả lời câu hỏi                  │ Cypher / NetworkX│
├────────────────────┼──────────────────────────────────┼──────────────────┤
│ Shortest Path      │ "Đường nào ít bước nhất?"        │ shortestPath() / nx.shortest_path │
│ All Paths          │ "Có những đường nào (≤N hops)?"  │ MATCH *1..3 / nx.all_simple_paths │
│ K-Shortest Paths   │ "Top-K đường ưu tiên nhất?"      │ Yen's algo / nx.shortest_simple_paths │
│ Weighted Shortest  │ "Đường nào đáng tin nhất?"       │ Dijkstra / nx.dijkstra_path │
│ Constrained Path   │ "Đường nào chỉ qua MANAGES?"     │ WHERE + pattern      │
└────────────────────┴──────────────────────────────────┴──────────────────┘
```

**Mẹo chọn:** Nếu bạn không biết graph "dài bao nhiêu" → dùng Shortest Path. Nếu bạn muốn LLM cân nhắc nhiều lựa chọn (để suy luận, hợp lý thay vì may rủi) → dùng All Paths hoặc K-Shortest và đưa cả K paths vào prompt giúp LLM chọn logical alternative.

<details>
<summary>Python Code — Path Finding (Click để xem)</summary>

> 📄 **Code ví dụ:** [`examples/03-2-1-cac-loai-path-finding.py`](examples/03-2-1-cac-loai-path-finding.py)

</details>

### 2.2 Cypher Path Queries

> 📄 **Code ví dụ:** [`examples/04-2-2-cypher-path-queries.cypher`](examples/04-2-2-cypher-path-queries.cypher)

> **Tóm gọn 1 câu:** Đường ít bước chưa chắc là đường tốt — chọn loại tìm đường theo tiêu chí bạn cần: ít bước, đáng tin nhất, hay đưa nhiều lựa chọn cho LLM.

---

## 3. Inference Rules & Reasoning

> **📌 Khái Niệm Cơ Bản:**
> **Inference (suy diễn) = tạo ra kiến thức MỚI từ kiến thức CŨ.** Graph của bạn có thể thiếu kết nối trực tiếp — nhưng nếu bạn biết *quy luật ngầm* giữa các quan hệ, bạn "suy ra" được kết nối bị thiếu đó.
>
> **Ví dụ dễ nhất — Transitivity (bắc cầu):**
> ```
> Biết:  Alice ─MANAGES→ Bob ─MANAGES→ Carol
> Suy ra: Alice ─INDIRECTLY_MANAGES→ Carol   (bắc cầu)
>
> Giống trong đời thực: "Bạn của bạn không hẳn là bạn của tôi" — nhưng:
> A là quản lý của B, B là quản lý của C → A có quyền gián tiếp với C.
> Đây là "suy ra mới": ta không cần edge EU trực tiếp — vẫn trả lời được
> câu hỏi "ai thực ra có ảnh hưởng lên Carol?".
> ```
>
> **Tại sao cần?** Vì graph thực tế rất **thưa (sparse)** — không thể lưu mọi kết nối ngầm. Inference "nén" tri thức vào **các rule** thay vì lưu tất cả quan hệ dẫn xuất thủ công.

### 3.1 Rule-Based Inference

> **Quy trình khai báo rule rồi để máy chạy pattern matching:**
> 1. Bạn viết rule dạng `IF (pattern xuất hiện) THEN (tạo edge mới)`
> 2. Máy quét toàn bộ graph tìm mọi chỗ khớp pattern
> 3. Mỗi chỗ khớp → tạo edge suy ra (kèm confidence + evidence bằng chứng)

> 📄 **Code ví dụ:** [`examples/05-3-1-rule-based-inference.py`](examples/05-3-1-rule-based-inference.py)

### 3.2 Confidence Propagation

Khi suy diễn qua nhiều bước, confidence giảm (đi qua càng nhiều cạnh suy ra, tin cậy càng thấp):

> 📄 **Code ví dụ:** [`examples/06-3-2-confidence-propagation.py`](examples/06-3-2-confidence-propagation.py)

> **Tóm gọn 1 câu:** Thay vì lưu mọi quan hệ dẫn xuất, viết luật "nếu... thì..." để máy tự suy ra cạnh mới — kèm độ tin cậy giảm dần theo số bước suy luận.

---

## 4. Community Detection & Centrality

### 4.1 Community Detection Cho Reasoning

> 📄 **Code ví dụ:** [`examples/07-4-1-community-detection-cho-reasoning.py`](examples/07-4-1-community-detection-cho-reasoning.py)

### 4.2 Centrality — Ai Quan Trọng?

> **Centrality** = bộ chỉ số đo "tầm quan trọng" của node: PageRank đo mức được trỏ tới, betweenness đo mức node "nằm trên đường đi" giữa các node khác.

<details>
<summary>Python Code — Centrality Analysis (Click để xem)</summary>

> 📄 **Code ví dụ:** [`examples/08-4-2-centrality-ai-quan-trong.py`](examples/08-4-2-centrality-ai-quan-trong.py)

</details>

> **Tóm gọn 1 câu:** Community chỉ ra "ai thuộc nhóm nào", centrality chỉ ra "ai nổi bật nhất" — cả hai giúp suy luận biết đâu là điểm quan trọng cần đi qua.

---

## 5. Temporal Reasoning

Phần này xử lý quan hệ có "hạn sử dụng": khi nào còn đúng, khi nào hết.

### 5.1 Time-Aware Graph

> 📄 **Code ví dụ:** [`examples/09-5-1-time-aware-graph.py`](examples/09-5-1-time-aware-graph.py)

### 5.2 Versioning

> 📄 **Code ví dụ:** [`examples/10-5-2-versioning.py`](examples/10-5-2-versioning.py)

> **Tóm gọn 1 câu:** Mỗi cạnh gắn ngày hiệu lực, cập nhật thì "đóng hạn" cạnh cũ thay vì xoá — nhờ vậy câu hỏi về quá khứ vẫn trả lời được.

---

## 6. Triển Khai Reasoning Engine

<details>
<summary>Python Code — Complete Reasoning Engine (Click để xem)</summary>

> 📄 **Code ví dụ:** [`examples/11-6-trien-khai-reasoning-engine.py`](examples/11-6-trien-khai-reasoning-engine.py)

</details>

> **Tóm gọn 1 câu:** Reasoning engine = gói 5 mảnh trên vào một lớp: đi graph có ràng buộc, tìm đường, áp luật, đo tầm quan trọng, lọc theo thời gian.

---

## 7. Neuro-Symbolic QA — Kết Hợp LLM + Graph Traversal

> **📌 Khái Niệm Cơ Bản:**
> **Neuro-symbolic QA** = kết hợp hai thế mạnh: **LLM hiểu ngôn ngữ tự nhiên (neuro)** + **graph traversal tìm bằng chứng chính xác (symbolic)**. Thay vì LLM tự "nhớ" tri thức từ tham số (hay nhầm lẫn), LLM đóng vai **chỉ huy — lên kế hoạch, graph thực thi — tìm path — LLM tổng hợp**.
>
> **Vì sao đây là xu hướng?** Nghiên cứu cho thấy: LLM "đọc" graph thay vì "tự nhớ" → hallucination giảm đáng kể. Graph thực thi đảm bảo mỗi "bước suy luận" đều được **hỗ trợ bằng chứng** thực tế trong KG.
>
> Các mô hình tiêu biểu:

### 7.1 Think-on-Graph (ToG)

> LLM **đọc KG như người** — mỗi bước suy luận mới **thăm 1-2 nút**, xem dataframe, rồi quyết định bước tiếp. Nếu BFS không đúng hướng → **LLM tự điều chỉnh hướng** (đổi branch) — giống người "suy nghĩ trong đầu".

> 📄 **Code ví dụ:** [`examples/12-7-1-think-on-graph-tog.py`](examples/12-7-1-think-on-graph-tog.py)

### 7.2 Plan-on-Graph — Planner-Executor-Reasoner (PER)

> **Đóng 3 vai** — phân tách rõ ràng:
> - **Planner** (LLM): sinh "kế hoạch" — 1 chuỗi relation types cần đi qua (`GET_REPORTER`, `GET_PROJECT`, `GET_STATUS`)
> - **Executor** (Graph BFS): thực thi mối relation theo kế hoạch
> - **Reasoner** (LLM): **đọc kết quả thực thi** → tóm tắt answer
>
> **Kết quả chính:** Planner-Executor-Reasoner (PER) đạt **micro-F1 > 0.90** trên KGQA benchmark (2025-2026), với chi phí computation thấp hơn nhiều so với Neo4j full-LLM reasoning.

### 7.3 KG-Agent

> Agent **thao tác KG qua API** (CRUD) thay vì chỉ query — agent có thể **thêm relation, sửa node, viết bằng chứng mới** vào graph nếu cần, rồi dùng kết quả cho câu trả lời.

> 📄 **Code ví dụ:** [`examples/13-7-3-kg-agent.py`](examples/13-7-3-kg-agent.py)

> **So với Think-on-Graph:** PER tách rõ Planner (đổi hướng) / Executor / Reasoner. Think-on-Graph remix mọi thứ trong LLM + graph. PER thường **hiệu quả hơn về chi phí** vì Executor không tốn token LLM.

> **Tóm gọn 1 câu:** Để LLM chỉ huy, code chạy — mỗi bước suy luận đều có bằng chứng trong graph, nên giảm bịa và giảm chi phí token.

---

## 8. Labs Thực Hành

### Lab 1: Constrained Traversal Benchmark

1. Tạo graph 1K nodes, 5K edges với random types
2. Chạy BFS không constraint vs constrained (chỉ 2 edge types) — so sánh số nodes thăm và thời gian

### Lab 2: Rule Inference

1. Định nghĩa 5 rules cho org chart (transitive, composition)
2. Chạy `apply_rules` trên graph 50 nodes, đếm số inferred edges
3. Kiểm tra: inferred edges có đúng logic không? Có false positive không?

### Lab 3: Temporal Query

1. Tạo temporal graph với 20 edges có `valid_from/until` khác nhau
2. Hỏi: "Ai quản lý team X vào 2023-06-01 vs 2024-06-01?" — verify kết quả khác nhau

> **Tóm gọn 1 câu:** 3 lab cho bạn kiểm chứng: ràng buộc giúp nhanh hơn, luật suy ra cạnh đúng logic, và truy vấn theo thời gian trả đúng quá khứ.

---

## Tài Liệu Tham Khảo

> Bài báo gốc + tài liệu GDS; cần kỹ thuật nào đọc bài đó.

- *Reasoning with Knowledge Graphs* — Paulheim & Gangemi (2023)
- Neo4j GDS — *Path Finding & Centrality* (https://neo4j.com/docs/graph-data-science/current/)
- HotpotQA — *Multi-hop QA Benchmark* (https://hotpotqa.github.io/)
- *Temporal Knowledge Graphs* — Cai et al. (2024, survey)
- *Think-on-Graph: Deep and Responsible Reasoning of Large Language Model on Knowledge Graph* (ICLR 2024)
- *Plan-on-Graph & Planner-Executor-Reasoner* — LLM-planned multi-hop KGQA, micro-F1 > 0.90 (arXiv:2511.19648)
- *KG-Agent: An Efficient and Agentic LLM for Knowledge Graph Reasoning* (2025)

---

## GraphRAG — Cập nhật 2026

> **Đang nói về gì:** GraphRAG = RAG có trợ giúp của đồ thị (RAG = đưa tài liệu liên quan vào prompt cho LLM trả lời). **Multi-hop** = câu hỏi cần nối 2+ bước quan hệ; **vector-only RAG** = chỉ tìm theo "giống về nghĩa", không nhìn cấu trúc.

Microsoft GraphRAG (2024-2025): dùng knowledge graph để enhance RAG. Query phức tạp (multi-hop) tốt hơn vector-only RAG.

**Tin mới 2025-2026:**
- **LazyGraphRAG** (Microsoft, cuối 2024): defer LLM summarisation tới query time — "defer" = trì hoãn bước tóm tắt đắt tiền đến khi có người hỏi, thay vì tóm trước mọi thứ — indexing cost ngang vector RAG, quality ngang full GraphRAG, query cost thấp hơn ~700×. Đã tích hợp Microsoft Discovery (2025) và Azure Local.
- **LightRAG** (HKUDS, EMNLP 2025): dual-layer graph + vector, incremental update (thêm tài liệu mới chỉ cập nhật phần thay đổi) thay vì re-index toàn bộ.
- **GraphRAG-Bench** (Microsoft, 06/2025): multi-hop + global queries GraphRAG thắng; single-hop factoid vanilla RAG thắng.
- **Gartner (2026)**: GraphRAG trong "Top Trends in D&A for 2026" cho complex cases mà high-accuracy RAG thất bại.
- **Knowledge Graph Market**: 1.48B USD (2025) → 2.04B USD (2026). GraphRAG chuyển từ "enterprise luxury" → production baseline.

Ref: https://microsoft.github.io/graphrag/

> **Tóm gọn 1 câu:** Từ 2025-2026, GraphRAG đã rẻ và phổ biến hơn nhiều — chọn đúng biến thể giúp trả các câu hỏi nhiều bước mà vector RAG bó tay.

---

*Tiếp theo: [07 — GNN](../07-gnn/)*
