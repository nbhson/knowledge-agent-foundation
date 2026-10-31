# ⚙️ 08. Graph Workflow — Pipeline, Cập Nhật và Vận Hành Đồ Thị

> ## 📑 Mục Lục
>
> - [Câu Chuyện Mở Đầu](#câu-chuyện-mở-đầu)
> - [Tại Sao Graph Workflow Quan Trọng?](#tại-sao-graph-workflow-quan-trọng)
> - [Tổng Quan](#tổng-quan)
> - [Nội Dung](#nội-dung)
> - [1. Graph ETL Pipeline](#1-graph-etl-pipeline)
> - [2. Incremental Updates](#2-incremental-updates)
> - [3. Versioning & Temporal Graphs](#3-versioning--temporal-graphs)
> - [4. Orchestration: Airflow, Prefect, Loop](#4-orchestration-airflow-prefect-loop)
> - [5. Observability & Error Recovery](#5-observability--error-recovery)
> - [6. Triển Khai Complete Workflow Engine](#6-triển-khai-complete-workflow-engine)
> - [7. Labs Thực Hành](#7-labs-thực-hành)
> - [Tài Liệu Tham Khảo](#tài-liệu-tham-khảo)

---

### Câu Chuyện Mở Đầu

Bạn đã xây xong Knowledge Graph với 10,000 nodes. Hệ thống chạy tốt.

Tuần sau:

- **Thứ 2**: 50 documents mới → cần ingest, không rebuild toàn bộ
- **Thứ 3**: Phát hiện 200 duplicate entities → cần merge, không mất relations
- **Thứ 4**: Schema thay đổi (thêm edge type `REVIEWS`) → cần migration
- **Thứ 5**: Một batch ingest lỗi → cần rollback

Không có workflow, bạn làm thủ công: chạy script, quên checkpoint, graph bị hỏng, mất 2 ngày khôi phục.

**Graph Workflow** là hệ thống **tự động, có checkpoint, có rollback, có observability** cho mọi thao tác trên graph — giống như CI/CD cho code, nhưng cho knowledge graph.

### Tại Sao Graph Workflow Quan Trọng?

> *"A graph without a workflow is a snapshot. A graph with a workflow is a living system."*

| # | Nguồn | Phát Hiện |
|---|-------|-----------|
| 1 | **Neo4j Production Survey (2024)** | 68% graph incidents do **thiếu incremental pipeline** — rebuild toàn bộ gây downtime |
| 2 | **Microsoft GraphRAG** | Incremental indexing giảm **90% re-indexing cost** khi thêm documents mới |
| 3 | **Prefect + Graph Benchmark (2025)** | Workflow với checkpoint giảm **80% recovery time** khi batch ingest lỗi |

---

## Tổng Quan

```
                    ┌─────────────────────────────────┐
                    │      GRAPH WORKFLOW ENGINE       │
                    │                                  │
  New Documents ───►│  ┌──────────┐  ┌──────────┐     │
                    │  │  ETL     │  │ Incremental│   │
  Schema Changes ──►│  │ Pipeline │  │  Updates │     │
                    │  └──────────┘  └──────────┘     │
  User Edits ──────►│  ┌──────────┐  ┌──────────┐     │
                    │  │Versioning│  │Orchestr. │     │
                    │  │& Temporal│  │(Schedule)│     │
                    │  └──────────┘  └──────────┘     │
                    │  ┌──────────────────────────┐   │
                    │  │ Observability & Recovery │   │
                    │  │ Logs, Metrics, Rollback  │   │
                    │  └──────────────────────────┘   │
                    └──────────────┬──────────────────┘
                                   │
                    ┌──────────────▼──────────────────┐
                    │     KNOWLEDGE GRAPH (Neo4j)      │
                    │  + Vector Index + Community Cache│
                    └─────────────────────────────────┘
```

---

## Nội Dung

| # | Chủ đề | Mô tả |
|---|--------|-------|
| 1 | [ETL Pipeline](#1-graph-etl-pipeline) | Extract → Transform → Load cho graph |
| 2 | [Incremental Updates](#2-incremental-updates) | Thêm/sửa/xóa không rebuild |
| 3 | [Versioning](#3-versioning--temporal-graphs) | Temporal, rollback, audit trail |
| 4 | [Orchestration](#4-orchestration-airflow-prefect-loop) | Schedule, DAG, loop integration |
| 5 | [Observability](#5-observability--error-recovery) | Logging, metrics, circuit breaker |
| 6 | [Engine](#6-triển-khai-complete-workflow-engine) | Code workflow engine |

---

## 1. Graph ETL Pipeline

> **📌 Khái Niệm Cơ Bản:**
> **Graph ETL = quy trình "nhồi dữ liệu vào graph"** theo 4 giai đoạn:
> 1. **Extract**: đọc documents → trích xuất entities + relations (bằng LLM)
> 2. **Transform**: làm sạch — gộp trùng (dedup), chuẩn hóa tên ("NV A" = "Nguyễn Văn A")
> 3. **Validate**: kiểm tra entities có hợp lệ theo ontology/schema không (không thể có `Person -[WORKS_ON]-> Person`)
> 4. **Load**: ghi vào graph dùng **MERGE** (không INSERT) — thêm mới nếu chưa có, cập nhật nếu đã có
>
> **Khác ETL bảng tính:**
> - Transform cần **LLM** (trích xuất tri thức từ text — không phải phép tính)
> - Load phải **idempotent** (chạy lại 100 lần cũng kết quả như nhau, không nhân đôi dữ liệu)
> - Bắt buộc **dedup + validation** trước khi ghi — vì LLM trích xuất không bao giờ chính xác 100%

```
ETL thường:  Raw Data → Clean → Transform → Load vào Table
Graph ETL:   Documents → Extract KG → Resolve → Validate → Load vào Graph

Khác biệt:
  - Transform = entity/relation extraction (cần LLM)
  - Load = MERGE (idempotent) thay vì INSERT
  - Cần dedup + ontology validation trước khi load
```

### 1.1 ETL Cho Graph Khác Gì ETL Thường?

<details>
<summary>Python Code — Graph ETL Pipeline (Click để xem)</summary>

> 📄 **Code ví dụ:** [`examples/01-1-1-etl-cho-graph-khac-gi-etl.py`](examples/01-1-1-etl-cho-graph-khac-gi-etl.py)

</details>

### 1.2 Batch vs Streaming

```
┌──────────────┬──────────────────────────────────┬──────────────────────────┐
│ Mode         │ Khi nào dùng                     │ Ví dụ                    │
├──────────────┼──────────────────────────────────┼──────────────────────────┤
│ Batch        │ Ingest hàng loạt (100-10K docs)  │ Initial load, nightly job│
│ Streaming    │ Ingest real-time (1 doc/event)   │ User uploads, webhook    │
│ Micro-batch  │ Cân bằng (10-100 docs/lần)       │ Hourly incremental       │
└──────────────┴──────────────────────────────────┴──────────────────────────┘

Khuyến nghị:
  - Initial: batch (toàn bộ corpus, 1 lần)
  - Daily: micro-batch (documents mới trong ngày)
  - Real-time: streaming (user edit, API webhook)
```

---

## 2. Incremental Updates

### 2.1 Tại Sao Incremental?

```
Rebuild toàn bộ (batch):
  10K docs × 2 LLM calls/doc × $0.005/1K = $100 + 2 giờ
  → Không thể làm mỗi khi có 1 doc mới

Incremental:
  1 doc mới × 2 LLM calls × $0.005/1K = $0.01 + 5 giây
  → Chỉ xử lý doc mới, merge vào graph hiện có
```

### 2.2 Incremental Strategies

<details>
<summary>Python Code — Incremental Update Engine (Click để xem)</summary>

> 📄 **Code ví dụ:** [`examples/02-2-2-incremental-strategies.py`](examples/02-2-2-incremental-strategies.py)

</details>

---

## 3. Versioning & Temporal Graphs

> **📌 Khái Niệm Cơ Bản:**
> **Grapactory luôn thay đổi** — nhân viên đổi team, dự án bị hủy, hợp đồng hết hạn. Nếu bạn xóa edge cũ, bạn **mất lịch sử + không thể trả lời câu hỏi "hồi Q1/2024 thì thế nào?"**.
>
> **Giải pháp 2 lớp:**
> 1. **Temporal Properties** — thêm `valid_from`/`valid_until` cho edge: quan hệ có **thời gian hiệu lực**. Query "ai quản lý TeamA vào 2024-02-01?" → chỉ xét edges active lúc đó.
> 2. **Audit Trail (Event Sourcing)** — ghi log **mọi thay đổi** (ai, khi nào, làm gì). Không có "xóa mất", chỉ có "ghi thêm 1 event DELETE" → **rollback được**.
>
> **Analogies:**
> - Temporal = hợp đồng lao động có ngày bắt đầu/kết thúc — chỉ "còn hiệu lực" trong khoảng đó.
> - Audit Trail = sổ nhật ký ghi mọi thao tác — tra được ai đã sửa gì. Không bao giờ tẩy xóa, chỉ thêm dòng mới.

### 3.1 Temporal Properties

> 📄 **Code ví dụ:** [`examples/03-3-1-temporal-properties.py`](examples/03-3-1-temporal-properties.py)

### 3.2 Audit Trail (Event Sourcing)

Giống như `trajectory-fork-replay` trong harness, graph cũng cần audit trail:

> 📄 **Code ví dụ:** [`examples/04-3-2-audit-trail-event-sourcing.py`](examples/04-3-2-audit-trail-event-sourcing.py)

---

## 4. Orchestration: Airflow, Prefect, Loop

### 4.1 So Sánh Orchestrators

```
┌─────────────────┬──────────────────┬──────────────────┬──────────────────────┐
│ Công cụ         │ Phù hợp nhất khi │ Lên lịch         │ Tích hợp với graph   │
├─────────────────┼──────────────────┼──────────────────┼──────────────────────┤
│ Airflow         │ Large DAGs, ETL  │ Cron, event      │ PythonOperator + Neo4j│
│ Prefect         │ Modern, Pythonic │ Cron, interval   │ @flow + @task        │
│ Loop (framework)│ Agent loops      │ Schedule + triage│ Automations + worktree│
│ GitHub Actions  │ CI/CD + KG sync  │ Push, schedule   │ Workflow YAML        │
│ Cron (simple)   │ Small, local     │ Cron             │ Shell script         │
└─────────────────┴──────────────────┴──────────────────┴──────────────────────┘
```

### 4.2 Prefect Example

<details>
<summary>Python Code — Prefect Graph Workflow (Click để xem)</summary>

> 📄 **Code ví dụ:** [`examples/05-4-2-prefect-example.py`](examples/05-4-2-prefect-example.py)

</details>

### 4.3 Tích Hợp Với Loop Engineering

Loop có thể tự động trigger graph updates:

```
Loop: Daily Triage
  Schedule: mỗi ngày 9:00
  Triage: phát hiện documents mới trong /data/raw_docs/
  Action:
    1. So sánh file list với STATE.md (đã ingest chưa)
    2. Với mỗi file mới → gọi IncrementalUpdater.add_document()
    3. Chạy community detection lại nếu >100 nodes mới
    4. Cập nhật STATE.md + graph audit log
    5. Nếu lỗi → escalate to human (loop/03-safety pattern)
```

---

## 5. Observability & Error Recovery

> **📌 Khái Niệm Cơ Bản:**
> **Observability = "nhìn được vào bên trong pipeline"** — bạn cần biết: mỗi lần chạy ETL:
> - Mất bao lâu (mỗi stage)?
> - Vào bao nhiêu entities/relations, ra bao nhiêu (bao nhiêu bị bad)?
> - Dedup (gộp trùng) bao nhiêu phần trăm?
> - Có bao nhiêu lỗi, ở stage nào?
>
> **Error Recovery = kế hoạch "khi lỗi thì làm gì":** thử lại (retry), bỏ qua (skip), hay dừng hẳn (fail). **Không bao giờ để pipeline lỗi âm thầm mà vẫn báo "thành công"**.

### 5.1 Metrics Cho Graph Workflow

> 📄 **Code ví dụ:** [`examples/06-5-1-metrics-cho-graph-workflow.py`](examples/06-5-1-metrics-cho-graph-workflow.py)

### 5.2 Error Recovery Patterns

> 📄 **Code ví dụ:** [`examples/07-5-2-error-recovery-patterns.py`](examples/07-5-2-error-recovery-patterns.py)

---

## 6. Triển Khai Complete Workflow Engine

<details>
<summary>Python Code — Graph Workflow Orchestrator (Click để xem)</summary>

> 📄 **Code ví dụ:** [`examples/08-6-trien-khai-complete-workflow-engine.py`](examples/08-6-trien-khai-complete-workflow-engine.py)

</details>

---

## 7. Labs Thực Hành

### Lab 1: ETL Pipeline Cho 100 Docs

1. Tạo 100 synthetic documents (dùng LLM generate)
2. Chạy `GraphETLPipeline` với 4 stages, đo thời gian từng stage
3. Thêm checkpoint và test rollback khi stage `validate` fail

### Lab 2: Incremental vs Rebuild Benchmark

1. Ingest 1000 docs (batch) — đo thời gian + cost
2. Thêm 10 docs mới: incremental (chỉ 10 docs) vs rebuild (1010 docs) — so sánh
3. Tính cost savings của incremental

### Lab 3: Loop Integration

1. Viết 1 GitHub Actions workflow: khi push `data/raw_docs/*.md` → trigger graph ETL
2. Hoặc: Prefect flow schedule mỗi giờ, kiểm tra `data/` có file mới không

---

## Tài Liệu Tham Khảo

- Prefect Docs — *Flows & Tasks* (https://docs.prefect.io/)
- Airflow Docs — *DAGs* (https://airflow.apache.org/docs/)
- Neo4j — *Import & ETL Tools* (https://neo4j.com/docs/operations-manual/current/tools/neo4j-admin/)
- *Data Pipelines with Apache Airflow* — Harenslak & de Ruiter (Manning)

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

---

*Tiếp theo: [09 — Evaluation](../09-evaluation/)*
