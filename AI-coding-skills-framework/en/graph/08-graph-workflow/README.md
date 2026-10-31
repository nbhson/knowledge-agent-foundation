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

This opening shows what goes wrong when you maintain a knowledge graph by hand — and why a workflow exists.

You've built your Knowledge Graph with 10,000 nodes. The system is running well. ("Knowledge Graph" = a store of facts as entities — people, projects, documents — plus the links between them.)

The following week:

- **Monday**: 50 new documents → need to ingest, not rebuild everything ("ingest" = load new data in)
- **Tuesday**: 200 duplicate entities found → need to merge, without losing relations ("entity" = one thing in the graph, such as a person or project)
- **Wednesday**: Schema changes (new edge type `REVIEWS`) → need a migration ("schema" = the rulebook of allowed node and edge types; "migration" = a planned change to that rulebook)
- **Thursday**: A batch ingest fails → need to rollback ("rollback" = undo the failed run and return to the last known-good state)

Without a workflow, you end up doing it by hand: running scripts, forgetting checkpoints, breaking the graph, and spending 2 days fixing it. ("Checkpoint" = a saved progress marker you can return to after a failure.)

**Graph Workflow** is the **steady, automatic setup** for everything you do to the graph — with checkpoints, easy rollbacks, and clear logs — a bit like CI/CD for code, but for knowledge graphs. ("CI/CD" = the automated build → test → deploy pipeline software teams run on code.)

> **One-line summary:** A knowledge graph changes every day, so hand-run scripts break it — a graph workflow gives you checkpoints, rollbacks, and logs, like CI/CD for your graph.

### Why Are Graph Workflows Important?

> *"A graph without a workflow is a snapshot. A graph with a workflow is a living system."*

How to read the table: each row is one study or benchmark, and the number is what happens with vs without a workflow. For instance, row 1 says most graph outages trace back to rebuilding everything instead of updating incrementally.

| # | Source | Finding |
|---|-------|-----------|
| 1 | **Neo4j Production Survey (2024)** | 68% of graph incidents stem from **lacking an incremental pipeline** — full rebuilds cause downtime |
| 2 | **Microsoft GraphRAG** | Incremental indexing cuts **re-indexing cost by 90%** when adding new documents |
| 3 | **Prefect + Graph Benchmark (2025)** | Workflows with checkpoints reduce **recovery time by 80%** when a batch ingest fails |

("Incremental" = process only what changed, instead of redoing the whole graph.)

> **One-line summary:** Industry data agrees: incremental pipelines, indexing, and checkpoints turn costly downtime into cheap, fast updates.

---

## Overview

This diagram shows the whole workflow engine at a glance: what flows in, which four modules handle it, and what it all writes to. Read it top to bottom — inputs on the left, the Knowledge Graph store at the bottom.

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

(Neo4j = a popular graph database; "vector index" = a fast lookup of similar vectors; "community cache" = stored results of grouping related nodes.)

> **One-line summary:** One engine takes in documents, schema changes, and edits; it runs ETL, incremental updates, versioning, and scheduling; and everything lands safely in the graph database.

---

## Contents

How to read the table: each row is one section of this document — the number, the title, and a one-line description. For instance, section 2 covers how to add new data without rebuilding the graph.

| # | Topic | Description |
|---|--------|-------|
| 1 | [ETL Pipeline](#1-graph-etl-pipeline) | Extract → Transform → Load for graphs |
| 2 | [Incremental Updates](#2-incremental-updates) | Add/update/delete without rebuilding |
| 3 | [Versioning](#3-versioning--temporal-graphs) | Temporal, rollback, audit trail |
| 4 | [Orchestration](#4-orchestration-airflow-prefect-loop) | Scheduling, DAGs, loop integration |
| 5 | [Observability](#5-observability--error-recovery) | Logging, metrics, circuit breaker |
| 6 | [Engine](#6-implementing-a-complete-workflow-engine) | Workflow engine code |

("DAG" = directed acyclic graph — a task graph with arrows and no loops, used to express pipeline order; "circuit breaker" = a switch that stops calling a failing service so failures don't cascade.)

> **One-line summary:** Six sections: getting data in, updating it, remembering history, scheduling runs, watching for errors, and a full engine putting it all together.

---

## 1. Graph ETL Pipeline

This section explains the "data into the graph" process: four stages, each with a plain-language job.

> **📌 Core Concept:**
> **Graph ETL = the "data-into-the-graph" process** in 4 stages:
> 1. **Extract**: read documents → extract entities + relations (via LLM) ("LLM" = a large language model, e.g. GPT — here it reads text and pulls out the facts)
> 2. **Transform**: clean — merge duplicates (dedup), normalize names ("NV A" = "Nguyen Van A") ("dedup" = deduplicate, i.e. merge copies of the same thing)
> 3. **Validate**: check entities are valid per the ontology/schema (you can't have `Person -[WORKS_ON]-> Person`) ("ontology" = the dictionary of allowed node types, edge types, and which may connect to which)
> 4. **Load**: write to the graph using **MERGE** (not INSERT) — add if new, update if it already exists
>
> **Different from spreadsheet ETL:**
> - Transform needs an **LLM** (extracting knowledge from text — not arithmetic)
> - Load must be **idempotent** (running it 100 times gives the same result, no doubling of data) — "idempotent" = safe to repeat
> - **dedup + validation are mandatory** before writing — because LLM extraction is never 100% correct

```
Regular ETL:  Raw Data → Clean → Transform → Load into Table
Graph ETL:   Documents → Extract KG → Resolve → Validate → Load into Graph

Differences:
  - Transform = entity/relation extraction (needs an LLM)
  - Load = MERGE (idempotent) instead of INSERT
  - dedup + ontology validation are required before load
```

("Resolve" here = dedup + name normalization: deciding that "NV A" and "Nguyen Van A" are one person.)

> **One-line summary:** Graph ETL extracts facts with an LLM, then cleans, validates against the schema, and writes with repeat-safe MERGE — because LLM output is never perfect.

### 1.1 How Is Graph ETL Different from Regular ETL?

The short version: regular ETL moves rows between tables; graph ETL turns unstructured text into entities and links, which is why it needs an LLM and cannot skip validation.

<details>
<summary>Python Code — Graph ETL Pipeline (Click to view)</summary>

> 📄 **Example code:** [`examples/01-1-1-how-is-graph-etl-different-from.py`](examples/01-1-1-how-is-graph-etl-different-from.py)

</details>

> **One-line summary:** The difference is the source: text needs LLM extraction, dedup, and schema validation before anything can be loaded.

### 1.2 Batch vs Streaming

This subsection answers "how often should data flow in?" — the answer depends on volume and urgency.

How to read the table: each row is an ingest mode, when it fits, and a typical example. For instance, "batch" = process everything at once, suited to a one-off initial load.

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

("Corpus" = your whole document collection; "webhook" = an automatic HTTP call one system sends another when something happens.)

> **One-line summary:** Start with one big batch, then switch to micro-batches for daily inflow and streaming for instant updates — match the mode to volume and urgency.

---

## 2. Incremental Updates

This section shows why reprocessing the whole graph for every new document is unaffordable, and how "process only the new part" works.

### 2.1 Why Incremental?

Read the two cost calculations below: same LLM, same price per call — the only difference is how many documents you touch.

```
Full rebuild (batch):
  10K docs × 2 LLM calls/doc × $0.005/1K = $100 + 2 hours
  → Not feasible every time a new doc arrives

Incremental:
  1 new doc × 2 LLM calls × $0.005/1K = $0.01 + 5 seconds
  → Only process the new doc, merge into the existing graph
```

("$0.005/1K" = the LLM price per 1,000 tokens of text; a rebuild costs 10,000× more than one incremental document.)

> **One-line summary:** A full rebuild costs ~$100 and 2 hours per run; incremental costs ~$0.01 and 5 seconds — always process only what changed.

### 2.2 Incremental Strategies

"Incremental strategy" = the plan for applying one new document: extract its facts, match them against existing nodes, and merge without touching the rest.

<details>
<summary>Python Code — Incremental Update Engine (Click to view)</summary>

> 📄 **Example code:** [`examples/02-2-2-incremental-strategies.py`](examples/02-2-2-incremental-strategies.py)

</details>

> **One-line summary:** An incremental update extracts the new document's facts, resolves them against existing nodes, and merges — the other 10,000 nodes stay untouched.

---

## 3. Versioning & Temporal Graphs

This section answers "how do we remember the past?" — both when facts were true, and who changed what.

> **📌 Core Concept:**
> **A graph always changes** — employees switch teams, projects get canceled, contracts expire. If you delete old edges, you **lose history and can no longer answer "how was it in Q1/2024?"** ("Edge" = a link between two nodes, e.g. `Alice -[MANAGES]-> TeamA`.)
>
> **The two-layer solution:**
> 1. **Temporal Properties** — add `valid_from`/`valid_until` to edges: the relation has an **effective period**. The query "who managed TeamA on 2024-02-01?" → only considers edges active at that time.
> 2. **Audit Trail (Event Sourcing)** — log **every change** (who, when, what). There is no "delete forever", only "append one DELETE event" → **rollback is possible**. ("Event sourcing" = store every change as an append-only event; the current state is the sum of all events, so you can replay or undo them.)
>
> **Analogies:**
> - Temporal = an employment contract with a start/end date — "in effect" only within that window.
> - Audit Trail = a logbook recording every action — you can look up who changed what. Never erase, only append a new line.

> **One-line summary:** Never delete — date-stamp edges (`valid_from`/`valid_until`) so old facts stay queryable, and log every change as an event so any state can be replayed or rolled back.

### 3.1 Temporal Properties

"Temporal properties" = extra date fields on an edge saying when that relation was true — the graph equivalent of a contract's start and end date.

> 📄 **Example code:** [`examples/03-3-1-temporal-properties.py`](examples/03-3-1-temporal-properties.py)

> **One-line summary:** Adding `valid_from`/`valid_until` to edges lets you ask "who managed TeamA on 2024-02-01?" and get the answer as of that date.

### 3.2 Audit Trail (Event Sourcing)

Just like `trajectory-fork-replay` in the harness, a graph also needs an audit trail: every change is an append-only event, so history can be replayed or rolled back, never lost.

> 📄 **Example code:** [`examples/04-3-2-audit-trail-event-sourcing.py`](examples/04-3-2-audit-trail-event-sourcing.py)

> **One-line summary:** An audit trail turns "delete" into "append a DELETE event" — history is never lost and every mistake is reversible.

---

## 4. Orchestration: Airflow, Prefect, Loop

"Orchestration" = a scheduler that runs pipeline steps for you on a schedule or on trigger, instead of a human pressing enter.

### 4.1 Comparing Orchestrators

How to read the table: each row is one orchestration tool, what it is best at, how you tell it when to run, and how it plugs into graph work. For instance, Airflow suits large scheduled ETL pipelines.

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

("Cron" = the classic Unix time scheduler; "triage" = quickly sorting items into categories; "worktree" = a separate working copy of a repo; "Workflow YAML" = a GitHub Actions config file.)

> **One-line summary:** Pick by scale: cron for tiny local jobs, Prefect or Airflow for real pipelines, GitHub Actions or Loop when the graph should update on git pushes or agent runs.

### 4.2 A Prefect Example

"Prefect" = a Python orchestration library where you decorate functions with `@flow` (the pipeline) and `@task` (its steps).

<details>
<summary>Python Code — Prefect Graph Workflow (Click to view)</summary>

> 📄 **Example code:** [`examples/05-4-2-a-prefect-example.py`](examples/05-4-2-a-prefect-example.py)

</details>

> **One-line summary:** In Prefect, a graph workflow is just a `@flow` function whose `@task` steps are the ETL stages — scheduling comes for free.

### 4.3 Integration with Loop Engineering

A Loop can automatically trigger graph updates ("Loop" = an agent that wakes on a schedule, checks what changed, and acts):

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

("STATE.md" = a plain file the agent uses as its memory of what was already processed; "community detection" = grouping closely connected nodes.)

> **One-line summary:** An agent loop can run the whole daily update itself — check for new files, ingest them, regroup communities if the graph grew, and escalate to a human on error.

---

## 5. Observability & Error Recovery

This section covers two things every pipeline needs: a window into what is happening (observability) and a pre-decided plan for failures (error recovery).

> **📌 Core Concept:**
> **Observability = "seeing inside the pipeline"** — for each ETL run you need to know:
> - How long it took (per stage)? ("stage" = one step of the pipeline, e.g. extract or validate)
> - How many entities/relations in, how many out (how many were bad)?
> - What percentage got deduplicated (merged)?
> - How many errors, in which stage?
>
> **Error Recovery = a "what to do on error" plan:** retry, skip, or stop completely (fail). **Never let a pipeline fail silently while reporting "success"**.

> **One-line summary:** Measure time, volume, dedup rate, and errors per stage — and decide in advance whether a failure means retry, skip, or stop; silent "success" is the one unacceptable outcome.

### 5.1 Metrics for a Graph Workflow

"Metrics" = the numbers you record for each run, so you can spot slowdowns and data loss before users do.

> 📄 **Example code:** [`examples/06-5-1-metrics-for-a-graph-workflow.py`](examples/06-5-1-metrics-for-a-graph-workflow.py)

> **One-line summary:** Track per-stage duration, entity/relation counts in vs out, and error counts — those four numbers reveal almost every pipeline problem.

### 5.2 Error Recovery Patterns

"Recovery pattern" = a named recipe for failures, e.g. retry three times with backoff (increasing waits), skip the bad item, or stop the whole run.

> 📄 **Example code:** [`examples/07-5-2-error-recovery-patterns.py`](examples/07-5-2-error-recovery-patterns.py)

> **One-line summary:** Choose a recovery pattern per failure type — retry for transient errors, skip for one bad record, stop for systemic ones.

---

## 6. Implementing a Complete Workflow Engine

This section is the capstone: one engine class that wires together the stages, checkpoints, and recovery from sections 1–5.

<details>
<summary>Python Code — Graph Workflow Orchestrator (Click to view)</summary>

> 📄 **Example code:** [`examples/08-6-implementing-a-complete-workflow-engine.py`](examples/08-6-implementing-a-complete-workflow-engine.py)

</details>

> **One-line summary:** The full engine combines ETL stages, incremental updates, checkpoints, and recovery patterns into one runnable orchestrator — use it as the reference implementation.

---

## 7. Hands-On Labs

These labs let you practice the section above: run an ETL pipeline, prove incremental is cheaper, and wire the graph into automation.

### Lab 1: An ETL Pipeline for 100 Docs

1. Create 100 synthetic documents (generated with an LLM) ("synthetic" = made-up data for testing, not real documents)
2. Run `GraphETLPipeline` with the 4 stages, time each stage
3. Add a checkpoint and test rollback when the `validate` stage fails

### Lab 2: Incremental vs Rebuild Benchmark

("Benchmark" = a controlled comparison measuring time and cost.)

1. Ingest 1000 documents (batch) — measure time + cost
2. Add 10 new documents: incremental (only the 10) vs rebuild (1010 docs) — compare
3. Calculate the cost savings of incremental

### Lab 3: Loop Integration

1. Write a GitHub Actions workflow: on push of `data/raw_docs/*.md` → trigger graph ETL
2. Or: a Prefect flow scheduled hourly, checking `data/` for new files

> **One-line summary:** Three labs: run and time a 4-stage ETL with rollback, prove incremental beats rebuild on cost, and automate the pipeline with GitHub Actions or Prefect.

---

## References

("Docs" = official documentation; start with Prefect if you only read one.)

- Prefect Docs — *Flows & Tasks* (https://docs.prefect.io/)
- Airflow Docs — *DAGs* (https://airflow.apache.org/docs/)
- Neo4j — *Import & ETL Tools* (https://neo4j.com/docs/operations-manual/current/tools/neo4j-admin/)
- *Data Pipelines with Apache Airflow* — Harenslak & de Ruiter (Manning)

> **One-line summary:** Official docs for Prefect, Airflow, and Neo4j import tools, plus one full book on Airflow pipelines.

---

## GraphRAG — 2026 Update

This closing section tracks how the field moved: GraphRAG and its successors, and what changed in 2025–2026.

Microsoft GraphRAG (2024-2025): uses knowledge graphs to enhance RAG ("RAG" = retrieval-augmented generation — an LLM answering questions using retrieved documents). Complex (multi-hop) queries outperform vector-only RAG.

**New 2025-2026 developments:**
- **LazyGraphRAG** (Microsoft, late 2024): defers LLM summarisation to query time ("defer" = postpone the expensive step until someone actually asks) — indexing cost equal to vector RAG, quality equal to full GraphRAG, ~700× lower query cost. Integrated into Microsoft Discovery (2025) and Azure Local.
- **LightRAG** (HKUDS, EMNLP 2025): dual-layer graph + vector, incremental update instead of full re-index.
- **GraphRAG-Bench** (Microsoft, 06/2025): multi-hop + global queries GraphRAG wins; single-hop factoid vanilla RAG wins ("vanilla" = plain, unmodified).
- **Gartner (2026)**: GraphRAG in "Top Trends in D&A for 2026" for complex cases where high-accuracy RAG falls short.
- **Knowledge Graph Market**: $1.48B (2025) → $2.04B (2026). GraphRAG shifting from "enterprise luxury" → production baseline.

Ref: https://microsoft.github.io/graphrag/

> **One-line summary:** GraphRAG keeps getting cheaper and more incremental — LazyGraphRAG and LightRAG cut cost, benchmarks say use it for multi-hop questions, and the market is making it standard.

---

*Next: [09 — Evaluation](../09-evaluation/)*
