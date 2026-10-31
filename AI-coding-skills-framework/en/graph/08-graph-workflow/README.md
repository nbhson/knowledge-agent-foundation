# ⚙️ 08. Graph Workflow — Pipeline, Updates, and Graph Operations

> ## 📑 Table of Contents
>
> - [Opening Story](#opening-story)
> - [Why Are Graph Workflows Important?](#why-are-graph-workflows-important)
> - [Overview](#overview)
> - [Contents](#contents)
> - [1. Graph ETL Pipeline](#1-graph-etl-pipeline)
> - [2. Incremental Updates](#2-incremental-updates)
> - [3. Versioning & Temporal Graphs](#3-versioning--temporal-graphs)
> - [4. Orchestration: Airflow, Prefect, Loop](#4-orchestration-airflow-prefect-loop)
> - [5. Observability & Error Recovery](#5-observability--error-recovery)
> - [6. Implementing a Complete Workflow Engine](#6-implementing-a-complete-workflow-engine)
> - [7. Hands-On Labs](#7-hands-on-labs)
> - [References](#references)

---

### Opening Story

You've built your Knowledge Graph with 10,000 nodes. The system is running well.

The following week:

- **Monday**: 50 new documents → need to ingest, not rebuild everything
- **Tuesday**: 200 duplicate entities found → need to merge, without losing relations
- **Wednesday**: Schema changes (new edge type `REVIEWS`) → need a migration
- **Thursday**: A batch ingest fails → need to rollback

Without a workflow, you end up doing it by hand: running scripts, forgetting checkpoints, breaking the graph, and spending 2 days fixing it.

**Graph Workflow** is the **steady, automatic setup** for everything you do to the graph — with checkpoints, easy rollbacks, and clear logs — a bit like CI/CD for code, but for knowledge graphs.

### Why Are Graph Workflows Important?

> *"A graph without a workflow is a snapshot. A graph with a workflow is a living system."*

| # | Source | Finding |
|---|-------|-----------|
| 1 | **Neo4j Production Survey (2024)** | 68% of graph incidents stem from **lacking an incremental pipeline** — full rebuilds cause downtime |
| 2 | **Microsoft GraphRAG** | Incremental indexing cuts **re-indexing cost by 90%** when adding new documents |
| 3 | **Prefect + Graph Benchmark (2025)** | Workflows with checkpoints reduce **recovery time by 80%** when a batch ingest fails |

---

## Overview

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

## Contents

| # | Topic | Description |
|---|--------|-------|
| 1 | [ETL Pipeline](#1-graph-etl-pipeline) | Extract → Transform → Load for graphs |
| 2 | [Incremental Updates](#2-incremental-updates) | Add/update/delete without rebuilding |
| 3 | [Versioning](#3-versioning--temporal-graphs) | Temporal, rollback, audit trail |
| 4 | [Orchestration](#4-orchestration-airflow-prefect-loop) | Scheduling, DAGs, loop integration |
| 5 | [Observability](#5-observability--error-recovery) | Logging, metrics, circuit breaker |
| 6 | [Engine](#6-implementing-a-complete-workflow-engine) | Workflow engine code |

---

## 1. Graph ETL Pipeline

> **📌 Core Concept:**
> **Graph ETL = the "data-into-the-graph" process** in 4 stages:
> 1. **Extract**: read documents → extract entities + relations (via LLM)
> 2. **Transform**: clean — merge duplicates (dedup), normalize names ("NV A" = "Nguyen Van A")
> 3. **Validate**: check entities are valid per the ontology/schema (you can't have `Person -[WORKS_ON]-> Person`)
> 4. **Load**: write to the graph using **MERGE** (not INSERT) — add if new, update if it already exists
>
> **Different from spreadsheet ETL:**
> - Transform needs an **LLM** (extracting knowledge from text — not arithmetic)
> - Load must be **idempotent** (running it 100 times gives the same result, no doubling of data)
> - **dedup + validation are mandatory** before writing — because LLM extraction is never 100% correct

```
Regular ETL:  Raw Data → Clean → Transform → Load into Table
Graph ETL:   Documents → Extract KG → Resolve → Validate → Load into Graph

Differences:
  - Transform = entity/relation extraction (needs an LLM)
  - Load = MERGE (idempotent) instead of INSERT
  - dedup + ontology validation are required before load
```

### 1.1 How Is Graph ETL Different from Regular ETL?

<details>
<summary>Python Code — Graph ETL Pipeline (Click to view)</summary>

> 📄 **Example code:** [`examples/01-1-1-how-is-graph-etl-different-from.py`](examples/01-1-1-how-is-graph-etl-different-from.py)

</details>

### 1.2 Batch vs Streaming

```
┌──────────────┬──────────────────────────────────┬──────────────────────────┐
│ Mode         │ When to use                      │ Example                  │
├──────────────┼──────────────────────────────────┼──────────────────────────┤
│ Batch        │ Bulk ingest (100-10K docs)       │ Initial load, nightly job│
│ Streaming    │ Real-time ingest (1 doc/event)   │ User uploads, webhook    │
│ Micro-batch  │ Balanced (10-100 docs/run)       │ Hourly incremental       │
└──────────────┴──────────────────────────────────┴──────────────────────────┘

Recommendations:
  - Initial: batch (the whole corpus, once)
  - Daily: micro-batch (documents new that day)
  - Real-time: streaming (user edits, API webhooks)
```

---

## 2. Incremental Updates

### 2.1 Why Incremental?

```
Full rebuild (batch):
  10K docs × 2 LLM calls/doc × $0.005/1K = $100 + 2 hours
  → Not feasible every time a new doc arrives

Incremental:
  1 new doc × 2 LLM calls × $0.005/1K = $0.01 + 5 seconds
  → Only process the new doc, merge into the existing graph
```

### 2.2 Incremental Strategies

<details>
<summary>Python Code — Incremental Update Engine (Click to view)</summary>

> 📄 **Example code:** [`examples/02-2-2-incremental-strategies.py`](examples/02-2-2-incremental-strategies.py)

</details>

---

## 3. Versioning & Temporal Graphs

> **📌 Core Concept:**
> **A graph always changes** — employees switch teams, projects get canceled, contracts expire. If you delete old edges, you **lose history and can no longer answer "how was it in Q1/2024?"**.
>
> **The two-layer solution:**
> 1. **Temporal Properties** — add `valid_from`/`valid_until` to edges: the relation has an **effective period**. The query "who managed TeamA on 2024-02-01?" → only considers edges active at that time.
> 2. **Audit Trail (Event Sourcing)** — log **every change** (who, when, what). There is no "delete forever", only "append one DELETE event" → **rollback is possible**.
>
> **Analogies:**
> - Temporal = an employment contract with a start/end date — "in effect" only within that window.
> - Audit Trail = a logbook recording every action — you can look up who changed what. Never erase, only append a new line.

### 3.1 Temporal Properties

> 📄 **Example code:** [`examples/03-3-1-temporal-properties.py`](examples/03-3-1-temporal-properties.py)

### 3.2 Audit Trail (Event Sourcing)

Just like `trajectory-fork-replay` in the harness, a graph also needs an audit trail:

> 📄 **Example code:** [`examples/04-3-2-audit-trail-event-sourcing.py`](examples/04-3-2-audit-trail-event-sourcing.py)

---

## 4. Orchestration: Airflow, Prefect, Loop

### 4.1 Comparing Orchestrators

```
┌─────────────────┬──────────────────┬──────────────────┬──────────────────────┐
│ Tool            │ Best For         │ Schedule         │ Graph Integration    │
├─────────────────┼──────────────────┼──────────────────┼──────────────────────┤
│ Airflow         │ Large DAGs, ETL  │ Cron, event      │ PythonOperator + Neo4j│
│ Prefect         │ Modern, Pythonic │ Cron, interval   │ @flow + @task        │
│ Loop (framework)│ Agent loops      │ Schedule + triage│ Automations + worktree│
│ GitHub Actions  │ CI/CD + KG sync  │ Push, schedule   │ Workflow YAML        │
│ Cron (simple)   │ Small, local     │ Cron             │ Shell script         │
└─────────────────┴──────────────────┴──────────────────┴──────────────────────┘
```

### 4.2 A Prefect Example

<details>
<summary>Python Code — Prefect Graph Workflow (Click to view)</summary>

> 📄 **Example code:** [`examples/05-4-2-a-prefect-example.py`](examples/05-4-2-a-prefect-example.py)

</details>

### 4.3 Integration with Loop Engineering

A Loop can automatically trigger graph updates:

```
Loop: Daily Triage
  Schedule: every day at 09:00
  Triage: detect new documents in /data/raw_docs/
  Action:
    1. Compare the file list against STATE.md (already ingested?)
    2. For each new file → call IncrementalUpdater.add_document()
    3. Re-run community detection if >100 new nodes
    4. Update STATE.md + the graph audit log
    5. On error → escalate to a human (loop/03-safety pattern)
```

---

## 5. Observability & Error Recovery

> **📌 Core Concept:**
> **Observability = "seeing inside the pipeline"** — for each ETL run you need to know:
> - How long it took (per stage)?
> - How many entities/relations in, how many out (how many were bad)?
> - What percentage got deduplicated (merged)?
> - How many errors, in which stage?
>
> **Error Recovery = a "what to do on error" plan:** retry, skip, or stop completely (fail). **Never let a pipeline fail silently while reporting "success"**.

### 5.1 Metrics for a Graph Workflow

> 📄 **Example code:** [`examples/06-5-1-metrics-for-a-graph-workflow.py`](examples/06-5-1-metrics-for-a-graph-workflow.py)

### 5.2 Error Recovery Patterns

> 📄 **Example code:** [`examples/07-5-2-error-recovery-patterns.py`](examples/07-5-2-error-recovery-patterns.py)

---

## 6. Implementing a Complete Workflow Engine

<details>
<summary>Python Code — Graph Workflow Orchestrator (Click to view)</summary>

> 📄 **Example code:** [`examples/08-6-implementing-a-complete-workflow-engine.py`](examples/08-6-implementing-a-complete-workflow-engine.py)

</details>

---

## 7. Hands-On Labs

### Lab 1: An ETL Pipeline for 100 Docs

1. Create 100 synthetic documents (generated with an LLM)
2. Run `GraphETLPipeline` with the 4 stages, time each stage
3. Add a checkpoint and test rollback when the `validate` stage fails

### Lab 2: Incremental vs Rebuild Benchmark

1. Ingest 1000 documents (batch) — measure time + cost
2. Add 10 new documents: incremental (only the 10) vs rebuild (1010 docs) — compare
3. Calculate the cost savings of incremental

### Lab 3: Loop Integration

1. Write a GitHub Actions workflow: on push of `data/raw_docs/*.md` → trigger graph ETL
2. Or: a Prefect flow scheduled hourly, checking `data/` for new files

---

## References

- Prefect Docs — *Flows & Tasks* (https://docs.prefect.io/)
- Airflow Docs — *DAGs* (https://airflow.apache.org/docs/)
- Neo4j — *Import & ETL Tools* (https://neo4j.com/docs/operations-manual/current/tools/neo4j-admin/)
- *Data Pipelines with Apache Airflow* — Harenslak & de Ruiter (Manning)

---

## GraphRAG — 2026 Update

Microsoft GraphRAG (2024-2025): uses knowledge graphs to enhance RAG. Complex (multi-hop) queries outperform vector-only RAG.

**New 2025-2026 developments:**
- **LazyGraphRAG** (Microsoft, late 2024): defers LLM summarisation to query time — indexing cost equal to vector RAG, quality equal to full GraphRAG, ~700× lower query cost. Integrated into Microsoft Discovery (2025) and Azure Local.
- **LightRAG** (HKUDS, EMNLP 2025): dual-layer graph + vector, incremental update instead of full re-index.
- **GraphRAG-Bench** (Microsoft, 06/2025): multi-hop + global queries GraphRAG wins; single-hop factoid vanilla RAG wins.
- **Gartner (2026)**: GraphRAG in "Top Trends in D&A for 2026" for complex cases where high-accuracy RAG falls short.
- **Knowledge Graph Market**: $1.48B (2025) → $2.04B (2026). GraphRAG shifting from "enterprise luxury" → production baseline.

Ref: https://microsoft.github.io/graphrag/

---

*Next: [09 — Evaluation](../09-evaluation/)*
