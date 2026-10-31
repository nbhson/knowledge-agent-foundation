# 📊 09. Evaluation — Evaluating Graph & GraphRAG Quality

> ## 📑 Table of Contents
>
> - [Opening Story](#opening-story)
> - [Why Is Evaluation Important?](#why-is-evaluation-important)
> - [Overview](#overview)
> - [Contents](#contents)
> - [1. Graph Quality Metrics](#1-graph-quality-metrics)
> - [2. Retrieval Evaluation](#2-retrieval-evaluation)
> - [3. Generation Evaluation (RAG)](#3-generation-evaluation-rag)
> - [4. Knowledge Graph Completion Metrics](#4-knowledge-graph-completion-metrics)
> - [5. Benchmarks & Datasets](#5-benchmarks--datasets)
> - [6. Evaluation Framework](#6-evaluation-framework)
> - [7. Hands-On Labs](#7-hands-on-labs)
> - [References](#references)

---

### Opening Story

This section shows why evaluation matters through a real demo that goes half-wrong.

You've built your GraphRAG (a RAG system that answers from a knowledge graph instead of plain text chunks) and demo it to your boss: *"Ask anything, it answers!"*

The boss asks 3 questions:

1. *"What's the Phoenix project budget?"* → Answer: "500 million" ✅ (correct, it's in the doc)
2. *"Who approved Phoenix?"* → Answer: "Alice" ✅ (correct, but confidence is 0.6 — low!)
3. *"How many people are on the AI team?"* → Answer: "15 people" ❌ (the doc says 10 — the LLM hallucinated, meaning it made the number up)

Without a good way to measure, you **don't know** how often your GraphRAG is right, how often it makes things up, and **why** it goes wrong (bad extraction? bad lookup? bad writing?).

**Evaluation is how you turn a fun demo into something you can trust in production.**

> **One-line summary:** Until you measure each stage, you cannot tell a lucky demo from a reliable system.

### Why Is Evaluation Important?

This section lists research findings that justify the metrics used later.

> *"If you can't measure it, you can't improve it. If you can't separate retrieval from generation, you don't know where to fix."*
> — RAG Evaluation Best Practices (2024)

How to read it: column 1 is the row number; column 2 names the study; column 3 is what it proved. For instance, row 2 says: measure "did the model stick to the facts" (generation) separately from "did search find the right documents" (retrieval), and debugging gets twice as fast.

| # | Source | Finding |
|---|-------|-----------|
| 1 | **Microsoft GraphRAG (2024)** | LLM-as-judge (comprehensiveness, diversity) distinguishes GraphRAG vs vanilla RAG at **p<0.01** |
| 2 | **RAGAS Framework (2024)** | Separating faithfulness (generation) from context relevance (retrieval) cuts **debug time by 50%** |
| 3 | **OGB + FB15k-237** | KG completion: Hits@10 and MRR are the standard metrics — don't use plain accuracy |

Glossary for the table: **LLM-as-judge** = a second model grades the answers on your behalf. **p<0.01** = the difference is statistically significant, not luck. **RAGAS** = a standard RAG evaluation framework. **OGB / FB15k-237** = public graph datasets used as standard tests. **Hits@10 / MRR** = ranking scores explained in section 4.

> **One-line summary:** Research shows you must grade retrieval and generation separately — one blended score hides where the system is broken.

---

## Overview

This section maps the whole evaluation framework: four stages, in order, feeding one benchmark and reporting layer.

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

## Contents

How to read it: column 1 is the section number; column 2 links to it; column 3 says in one line what it covers. For instance, section 2 is where Precision/Recall/MRR are defined.

| # | Topic | Description |
|---|--------|-------|
| 1 | [Graph Quality](#1-graph-quality-metrics) | Coverage, connectivity, density |
| 2 | [Retrieval](#2-retrieval-evaluation) | Precision, recall, MRR, path precision |
| 3 | [Generation](#3-generation-evaluation-rag) | Faithfulness, hallucination, LLM-as-judge |
| 4 | [KG Completion](#4-knowledge-graph-completion-metrics) | Hits@K, MRR, MR |
| 5 | [Benchmarks](#5-benchmarks--datasets) | HotpotQA, GraphRAG-Bench, KGHaluBench, evidence recall |
| 6 | [Framework](#6-evaluation-framework) | Evaluation pipeline code |

---

## 1. Graph Quality Metrics

> **📌 Core Concept:**
> **Before asking "does the AI answer correctly", ask "is the graph good?"** If the graph is incomplete or wrong, the RAG results are meaningless no matter how perfect the code is (GIGO — garbage in, garbage out).
>
> **9 measures of graph health.** Use these analogies:
>
> - **Node/Edge Coverage** = *coverage* — "what % of the facts did we extract from the documents?" Like a knowledge check: miss 30% of the knowledge and you only get 70% of the answers right.
> - **Duplicate Rate** = *cleanliness* — "how many entities are duplicated?" Like a phone book listing "Nguyen Van A" and "NV A" as two people → queries get split.
> - **Connectivity** = *connectedness* — "are the nodes linked together or scattered?" A graph broken into fragments → multi-hop queries can't reach the other fragment.
> - **Density / Avg Degree** = *thickness* — too sparse a graph → missing connections; too dense → noise.
> - **Isolated Nodes** = nodes **with no relationships at all** — useless, just taking up space.
> - **Invalid Edge Rate** = edges **violating the rules** (Person → MANAGES → Document) — must be 0%.
> - **Temporal Freshness** = old edges that have **expired** but weren't updated — answering with stale information.
>
> **One-line summary:** If the graph itself is incomplete or broken, perfect code downstream cannot save the answers.

### 1.1 Metrics for the Graph Itself

This section lists the nine numbers, what each means, and the bar each must clear.

Before measuring retrieval/generation, measure **whether the graph is good**:

```
┌──────────────────────┬──────────────────────────────────┬──────────────────────┐
│ Metric               │ Meaning                          │ Good when            │
├──────────────────────┼──────────────────────────────────┼──────────────────────┤
│ Node Coverage        │ % of real entities extracted     │ High (>80%)          │
│ Edge Coverage        │ % of real relations extracted    │ High (>70%)          │
│ Duplicate Rate       │ % duplicate nodes (not dedup'd)  │ Low (<5%)            │
│ Connectivity         │ % of nodes in the largest component │ High (>90%)      │
│ Density              │ 2|E| / |V|(|V|-1)                │ Domain-dependent     │
│ Avg Degree           │ Average relations per node       │ 3-10 (enterprise)    │
│ Isolated Nodes       │ Nodes with no edges at all       │ Low (<5%)            │
│ Invalid Edge Rate    │ % of edges violating the ontology│ 0%                   │
│ Temporal Freshness   │ % of edges still valid (not expired) │ High (>95%)     │
└──────────────────────┴──────────────────────────────────┴──────────────────────┘
```

How to read it: each row is one health check. "Metric" names it, "Meaning" says what it counts, "Good when" gives the target. For instance, Node Coverage > 80% means at least 4 out of 5 real entities must have been extracted; Invalid Edge Rate 0% means not a single edge may break the ontology (the schema that says which relation types are allowed between which node types).

<details>
<summary>Python Code — Graph Quality Metrics (Click to view)</summary>

> 📄 **Example code:** [`examples/01-1-1-metrics-for-the-graph-itself.py`](examples/01-1-1-metrics-for-the-graph-itself.py)

</details>

### 1.2 Coverage — Against Ground Truth

This section explains coverage: compare what the graph extracted against a list of facts known to be true (the "ground truth").

> 📄 **Example code:** [`examples/02-1-2-coverage-against-ground-truth.py`](examples/02-1-2-coverage-against-ground-truth.py)

---

## 2. Retrieval Evaluation

> **📌 Core Concept:**
> **Retrieval Evaluation = measuring "did the system find the right information?"** Before the LLM answers, the system must *pull the right context from the graph*. If retrieval pulls the wrong context → the LLM answers wrong no matter how good the model is.
>
> **Analogies to remember the 3 main metrics:**
> - **Precision@k** = *accuracy* — "of the 5 items retrieved, how many are RIGHT?" Retrieved 5 but 3 are wrong → low precision.
> - **Recall@k** = *completeness* — "of all N correct items total, how many did we catch?" There are 10 facts but we only retrieved 4 → low recall.
> - **MRR** = *how fast the correct answer appears* — "at what rank is the correct answer?" Correct at the top (rank 1) → score 1.0; at rank 5 → 0.2.
>
> **Think of the Precision/Recall formulas through a fishing analogy:** Precision = of the fish in the basket, how many are edible. Recall = of the fish in the pond, how many of the fish that exist did you catch.
>
> **One-line summary:** Retrieval evaluation asks one question — "did the system pull the right context?" — because a great model fed the wrong context still answers wrong.

### 2.1 Metrics for Retrieval

This section defines the six retrieval scores and their formulas.

```
┌──────────────────────┬──────────────────────────────────┬──────────────────────┐
│ Metric               │ Meaning                          │ Formula              │
├──────────────────────┼──────────────────────────────────┼──────────────────────┤
│ Precision@K          │ % of top-K retrieved that are right │ |relevant ∩ retrieved| / K │
│ Recall@K             │ % of ground truth that was retrieved │ |relevant ∩ retrieved| / |relevant| │
│ MRR (Mean Reciprocal)│ Average rank position of the correct answer │ mean(1/rank)    │
│ Path Precision       │ % of returned paths that are correct │ |correct paths| / |all paths| │
│ Context Relevance    │ Is the retrieved context related?  │ LLM-as-judge (0-1)   │
│ Hop Accuracy         │ Is the hop count right?            │ |correct hops| / |total| │
└──────────────────────┴──────────────────────────────────┴──────────────────────┘
```

How to read it: each row is one retrieval score. For instance, Precision@K with K=5 counts how many of the 5 retrieved items were actually relevant; MRR (Mean Reciprocal Rank) = average of 1 ÷ the rank of the first correct hit, so rank 1 scores 1.0 and rank 5 scores 0.2. "Ground truth" = the list of correct answers prepared in advance. "LLM-as-judge" = a second model grades the result for you.

<details>
<summary>Python Code — Retrieval Evaluation (Click to view)</summary>

> 📄 **Example code:** [`examples/03-2-1-metrics-for-retrieval.py`](examples/03-2-1-metrics-for-retrieval.py)

</details>

### 2.2 Comparing Vanilla RAG vs GraphRAG Retrieval

This section shows how to A/B-test plain vector search ("vanilla RAG") against graph-based retrieval on the same questions.

> 📄 **Example code:** [`examples/04-2-2-comparing-vanilla-rag-vs-graphrag-retrieval.py`](examples/04-2-2-comparing-vanilla-rag-vs-graphrag-retrieval.py)

---

## 3. Generation Evaluation (RAG)

### 3.1 RAGAS-Style Metrics

> **📌 Core Concept:**
> **The 2 most important questions about RAG answer quality:**
> - **Faithfulness** = *Did it make things up?* — every claim in the answer must **be grounded in the context** pulled from the graph. "Phoenix's budget is 700 million" when the graph doesn't say that → not faithful → hallucination.
> - **Answer Relevance** = *Does it actually answer the question?* — a long-winded answer that misses the point of the question scores low.
>
> **Analogies:** Faithfulness = "does the witness stick to the evidence or make things up?" Answer Relevance = "does the answer hit the heart of the question?"
>
> **How to measure (LLM-as-judge):** Split the answer into **claims** (small statements) → check whether each claim is in the context. Hallucination Rate = 1 - Faithfulness.
>
> **One-line summary:** Grade every sentence of the answer against the retrieved context — any sentence with no backing is a hallucination.

```
┌──────────────────────┬──────────────────────────────────┬──────────────────────┐
│ Metric               │ Meaning                          │ How it's measured    │
├──────────────────────┼──────────────────────────────────┼──────────────────────┤
│ Faithfulness         │ Is the answer grounded in the    │ LLM-as-judge: are the│
│                      │ context? (no fabrication)        │ claims in the context?│
│ Answer Relevance     │ Does the answer actually answer  │ LLM-as-judge: is the │
│                      │ the question?                    │ answer relevant?     │
│ Context Precision    │ Does the context contain the needed info? │ LLM-as-judge  │
│ Hallucination Rate   │ % of claims not in the context   │ 1 - faithfulness     │
│ Citation Accuracy    │ % of citations that point to the right source │ Check path/source │
└──────────────────────┴──────────────────────────────────┴──────────────────────┘
```

How to read it: each row is one answer-quality score and how it is measured. For instance, Faithfulness is judged by asking a second model ("LLM-as-judge") whether every claim in the answer appears in the context; Hallucination Rate is simply 1 minus Faithfulness.

<details>
<summary>Python Code — Faithfulness & Hallucination Detection (Click to view)</summary>

> 📄 **Example code:** [`examples/05-3-1-ragas-style-metrics.py`](examples/05-3-1-ragas-style-metrics.py)

</details>

### 3.2 LLM-as-Judge for Global Sensemaking (Microsoft Pattern)

This section covers Microsoft's pattern for broad "big-picture" questions ("global sensemaking" = questions about themes across the whole corpus), where a judge model scores answers on comprehensiveness and diversity.

> 📄 **Example code:** [`examples/06-3-2-llm-as-judge-for-global-sensemaking.py`](examples/06-3-2-llm-as-judge-for-global-sensemaking.py)

---

## 4. Knowledge Graph Completion Metrics

This section covers link prediction — guessing missing facts. KG completion = filling gaps in the graph, e.g. predicting that `Alice –WORKS_ON– X` exists because similar people do.

For link prediction / KG completion (GNN, TransE, etc. — neural models that learn from graph structure):

```
┌──────────────┬──────────────────────────────────┬──────────────────────┐
│ Metric       │ Meaning                          │ Good when            │
├──────────────┼──────────────────────────────────┼──────────────────────┤
│ Hits@K       │ % of correct answers in the top-K│ High (Hits@10 > 0.5) │
│ MRR          │ Mean Reciprocal Rank             │ High (>0.3)          │
│ MR (Mean Rank)│ Average rank position of the answer │ Low (<100)       │
│ AUC          │ Area under ROC for link prediction │ High (>0.8)        │
└──────────────┴──────────────────────────────────┴──────────────────────┘
```

How to read it: each row is one ranking score. For instance, Hits@10 asks "was the right answer in the model's top 10 guesses?"; MR (Mean Rank) is the average rank of the right answer, so **lower is better**. AUC = a 0–1 quality score from the ROC curve (a standard trade-off plot of hits vs false alarms).

<details>
<summary>Python Code — KG Completion Evaluation (Click to view)</summary>

> 📄 **Example code:** [`examples/07-4-knowledge-graph-completion-metrics.py`](examples/07-4-knowledge-graph-completion-metrics.py)

</details>

---

## 5. Benchmarks & Datasets

This section lists the public test sets to use instead of inventing your own.

### 5.1 Benchmarks for GraphRAG

How to read it: each row pairs a task type with a ready-made test set and its scoring metrics. For instance, a 2-hop question ("A approved B — what else did A do?") is tested on HotpotQA and scored with EM and F1. EM (Exact Match) = the answer must match the gold string exactly; F1 = partial word-overlap credit.

```
┌──────────────────────┬──────────────────────┬──────────────────────────────┐
│ Benchmark            │ Task                 │ Metric                       │
├──────────────────────┼──────────────────────┼──────────────────────────────┤
│ HotpotQA             │ Multi-hop QA (2 hops)│ EM, F1                       │
│ 2WikiMultihopQA      │ Multi-hop (2-4 hops) │ EM, F1                       │
│ MuSiQue              │ Multi-hop (2-4 hops) │ EM, F1 (harder)              │
│ Natural Questions    │ Open-domain QA       │ EM                           │
│ GraphRAG-Bench (MSFT)│ Domain KGQA, 1018 questions, 5 question types │ Multi-hop + single-hop + explainability (reasoning) │
│ KGHaluBench          │ KG-RAG hallucination │ Hallucination rate           │
│ Custom Enterprise QA │ Domain-specific      │ Faithfulness, P@K, MRR       │
└──────────────────────┴──────────────────────┴──────────────────────────────┘
```

Note on the table: " hops" = relationship steps followed to answer (1 hop = one edge). "KGQA" = question answering over a knowledge graph. "Explainability" = whether the system can show the reasoning path, not just the answer.

### 5.2 Benchmarks for KG Completion

How to read it: each row is a public dataset of facts (triples = `subject–relation–object` statements) used to test link prediction. "Triples" says how many facts the dataset holds; the metric column lists the ranking scores to report. For instance, FB15k-237 holds 310K facts from Freebase and is scored with Hits@10 and MRR.

```
┌──────────────────────┬──────────────────────┬──────────────────────────────┐
│ Benchmark            │ Triples              │ Metric                       │
├──────────────────────┼──────────────────────┼──────────────────────────────┤
│ FB15k-237            │ 310K (Freebase)      │ Hits@10, MRR                 │
│ WN18RR               │ 93K (WordNet)        │ Hits@10, MRR                 │
│ OGB-WikiKG2          │ 17M (Wikidata)       │ MRR                          │
│ Custom Enterprise KG │ Domain-dependent     │ Hits@K, coverage             │
└──────────────────────┴──────────────────────┴──────────────────────────────┘
```

### 5.3 Creating a Custom Benchmark

This section shows how to build a benchmark from your own documents — with the caveat that a self-made test set only proves what your pipeline already reads well, so human review is still required.

> 📄 **Example code:** [`examples/08-5-3-creating-a-custom-benchmark.py`](examples/08-5-3-creating-a-custom-benchmark.py)

### 5.4 The "Evaluation Gaps" in GraphRAG (2025-2026)

This section lists four blind spots that standard evaluation pipelines miss — reading it helps you avoid grading only half the problem.

> **📌 Core Concept — evaluating GraphRAG by measuring only retrieval/faithfulness is NOT enough.** New research shows 3 common gaps in today's evaluation pipelines:

**1. Missing "Evidence Recall" & "Context Relevancy"** — most systems only measure *"does the answer match the expected answer"* (EM/F1), not *"was the evidence fed to the LLM correct/sufficient"*.
- **Evidence Recall** = of the evidence the LLM received (chunks + graph paths), what % was **actually needed to answer** the question. Low recall means the model may have answered by luck.
- **Context Relevancy** = how much **irrelevant filler** was in the evidence fed in. Measured with a small question: *"In this context, which sentences do not help answer the question?"*
- Why it matters: high EM/F1 with skewed evidence → the system can't be trusted (retrieval was wrong but the LLM "bluffed" its way to the right answer — *lucky*).

**2. Retrieval Drift (CS-RAG)** — multi-step RAG systems (agentic/DRIFT, etc.) can **drift off track** partway through: step 1 has the right anchor but step 2 no longer follows the question → the answer drifts off course. How to measure: monitor the **"question anchoring"** of each retrieval hop (the hop's attention/score relative to the original question).

**3. KGHaluBench & KG-specific Hallucination** — GraphRAG hallucinations have 2 sources different from vanilla RAG:
- **Graph hallucination**: the self-built KG has a wrongly-extracted triplet (bad entity linking → the answer follows wrong).
- **Summary hallucination**: the LLM's community summary "fabricates" details that aren't in the graph.
- **KGHaluBench** measures the hallucination rate specifically when the underlying context is a graph instead of text. You need to evaluate **each source separately** — don't lump them into one faithfulness number.

**4. Systematic RAG vs GraphRAG Evaluation — don't be overconfident** — systematic benchmark results from 2025-2026: GraphRAG wins on multi-hop/global but **loses to vanilla RAG on single-hop/factoid**. So your evaluation should **split into 3 tracks** (single-hop / multi-hop / global) and report each separately — as Module 05 warned.

> 📄 **Example code:** [`examples/09-5-4-the-evaluation-gaps-in-graphrag-2025.py`](examples/09-5-4-the-evaluation-gaps-in-graphrag-2025.py)

> **One-line summary:** Check what evidence reached the model and grade single-hop, multi-hop, and global questions on separate tracks — a single score hides both lucky answers and lost categories.

---

## 6. Evaluation Framework

This section points to the complete runnable evaluation pipeline — the four stages above glued into one script.

<details>
<summary>Python Code — Complete Evaluation Pipeline (Click to view)</summary>

> 📄 **Example code:** [`examples/10-6-evaluation-framework.py`](examples/10-6-evaluation-framework.py)

</details>

---

## 7. Hands-On Labs

This section gives three exercises to run yourself — each proves one metric works as claimed. "Ground truth" = a prepared list of correct answers to score against.

### Lab 1: Evaluate Graph Quality

1. Create 2 graphs: 1 good (complete, connected) and 1 bad (many isolated, many duplicates)
2. Run `evaluate_graph_quality` on both, compare the metrics

### Lab 2: Compare Vanilla RAG vs GraphRAG

1. Prepare 20 queries with ground-truth `relevant` docs
2. Run both retrievers, measure P@5, R@5, MRR
3. Use `llm_judge` on 5 global queries — GraphRAG must win

### Lab 3: Hallucination Measurement

1. Create 20 QA pairs with `context` + `expected answer`
2. Have the LLM generate with the correct context vs without context
3. Measure faithfulness — with context it should be >0.8, without context the hallucination rate is high

> **One-line summary (Labs):** Each lab proves one claim: the graph metrics detect bad graphs, hybrid retrieval beats vector-only on multi-hop, and faithfulness collapses when context is removed.

---

## References

- Microsoft GraphRAG — *Evaluation: LLM-as-Judge* (https://microsoft.github.io/graphrag/)
- RAGAS — *RAG Assessment* (https://docs.ragas.io/)
- OGB — *Open Graph Benchmark Evaluation* (https://ogb.stanford.edu/docs/score/)
- HotpotQA — *Leaderboard* (https://hotpotqa.github.io/)
- *GraphRAG-Bench: A Domain-Specific Benchmark for GraphRAG* (arXiv:2506.02404) — 1018 questions, 5 types
- *KGHaluBench* — KG-augmented hallucination benchmark (2025)
- *CS-RAG: Retrieval Drift in Multi-Step RAG* (2025)
- *RAG vs GraphRAG: A Systematic Evaluation* (arXiv 2025) — splits into 3 tracks: single/multi/global
- *A Survey on Evaluation of Knowledge Graph Quality* — Paulheim (2017)

---

## GraphRAG — 2026 Update

This section tracks what changed recently, so you do not build to 2024 assumptions. LazyGraphRAG = a cheaper GraphRAG variant that puts off expensive LLM summarisation until query time.

Microsoft GraphRAG (2024-2025): uses knowledge graphs to enhance RAG. Complex (multi-hop) queries outperform vector-only RAG.

**New 2025-2026 developments:**
- **LazyGraphRAG** (Microsoft, late 2024): defers LLM summarisation to query time — indexing cost equal to vector RAG, quality equal to full GraphRAG, ~700× lower query cost. Integrated into Microsoft Discovery (2025) and Azure Local.
- **LightRAG** (HKUDS, EMNLP 2025): dual-layer graph + vector, incremental update instead of full re-index.
- **GraphRAG-Bench** (Microsoft, 06/2025): multi-hop + global queries GraphRAG wins; single-hop factoid vanilla RAG wins.
- **Gartner (2026)**: GraphRAG in "Top Trends in D&A for 2026" for complex cases where high-accuracy RAG falls short.
- **Knowledge Graph Market**: $1.48B (2025) → $2.04B (2026). GraphRAG shifting from "enterprise luxury" → production baseline.

Ref: https://microsoft.github.io/graphrag/

*End of the Graph Engineering Track — return to [README](../README.md) for the wrap-up.*

> **One-line summary (file):** Evaluate graph → retrieval → generation → completion, in that order, with stage-specific metrics and public benchmarks — never trust one blended number.
