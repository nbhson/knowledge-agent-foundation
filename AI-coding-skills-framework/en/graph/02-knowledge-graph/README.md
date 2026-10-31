# 🧠 02. Knowledge Graph Construction — Building the Knowledge Graph

> ## 📑 Table of Contents
>
> - [Opening Story](#opening-story)
> - [Why Is KG Construction Important?](#why-is-kg-construction-important)
> - [Overview](#overview)
> - [Contents](#contents)
> - [1. Ontology & Schema Design](#1-ontology--schema-design)
> - [2. Entity Extraction](#2-entity-extraction)
> - [3. Relation Extraction](#3-relation-extraction)
> - [4. Entity Resolution & Deduplication](#4-entity-resolution--deduplication)
> - [5. Incremental KG Updates](#5-incremental-kg-updates)
> - [6. Complete Pipeline](#6-complete-pipeline)
> - [7. Hands-On Labs](#7-hands-on-labs)
> - [References](#references)

---

### Opening Story

You have 1,000 documents: contracts, reports, emails. You hire 3 interns to read them and extract knowledge:

- Intern A extracts: `(Phoenix, managed_by, Alice)` — but writes "Alice Nguyen"
- Intern B extracts: `(Alice N., approves, Contract C-2024)` — different abbreviation
- Intern C extracts: `(Alice Nguyen, reports_to, Bob)` — different diacritics

Result: three different "Alice" nodes in the graph that don't link to each other → the graph is **broken into pieces**, and queries fail.

**Knowledge Graph Construction** fixes this: it pulls knowledge out of raw text in a **steady, consistent way** and links it up so you can query it easily.

### Why Is KG Construction Important?

> *"Garbage in, garbage out — a bad extraction makes the graph worse than vectors. Extraction determines 80% of GraphRAG quality."*
> — Microsoft GraphRAG Paper (2024)

| # | Research | Finding |
|---|-----------|-----------|
| 1 | **Microsoft GraphRAG (2024)** | The gleaning loop (extracting in multiple rounds) increases **entity coverage by 25%** vs single-pass |
| 2 | **LangChain Evaluation (2025)** | Deduplication via embedding similarity reduces **duplicate nodes by 40%** |
| 3 | **Stanford KB Construction (2024)** | The schema-first approach reduces **invalid relations by 60%** compared to open extraction |

---

## Overview

```
Raw Documents
    │
    ▼
┌─────────────────────┐
│  1. ONTOLOGY DESIGN │  ← Define valid node/edge types (schema)
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│ 2. ENTITY EXTRACTION│  ← LLM/NER extracts entities from text
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│ 3. RELATION EXTRACT │  ← LLM extracts relations between entities
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│ 4. RESOLUTION       │  ← Merge duplicates (Alice = Alice Nguyen)
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│ 5. INCREMENTAL UPDATE│ ← Update the graph when new documents arrive
└──────────┬──────────┘
           ▼
     Knowledge Graph (ready for Storage & GraphRAG)
```

---

## Contents

| # | Topic | Description |
|---|--------|-------|
| 1 | [Ontology & Schema](#1-ontology--schema-design) | Schema design, constraints, temporal properties |
| 2 | [Entity Extraction](#2-entity-extraction) | NER, LLM extraction, gleaning loop |
| 3 | [Relation Extraction](#3-relation-extraction) | Open RE, schema-guided RE, confidence scoring |
| 4 | [Resolution](#4-entity-resolution--deduplication) | Deduplication, canonicalization, embedding-based |
| 5 | [Incremental Updates](#5-incremental-kg-updates) | Add/modify/delete without rebuilding everything |
| 6 | [Pipeline](#6-complete-pipeline) | End-to-end code |
| 7 | [Agentic Construction](#7-agentic-kg-construction) | An LLM agent builds & self-corrects the KG via CRUD |

---

## 1. Ontology & Schema Design

> **📌 Core Concept:**
> **An ontology = the "blueprint" of your graph** — it prescribes in advance which entity types exist (`Person`, `Project`, `Document`) and which relations are valid (`Person` may `MANAGES`).
>
> **Why does it matter?** Without an ontology, the LLM extracts freely → the graph becomes a **"hairball"** (an uncontrolled mess of tangles): 5 things called "team", "senior reviewer" synonymous with... queries stop being precise, results come out wrong.
>
> **Analogy:** An ontology is like a company's **form template** — you know in advance which fields a record has, and who approves whom. No template → everyone records things their own way, nobody can look anything up.
>
> **Two design directions:**
> - **Schema-First**: define the schema first, then extract according to it — clean, but you may miss relations outside expectations.
> - **Schema-Free**: extract freely first, then organize — flexible, but produces lots of junk.
> - **Hybrid (recommended)**: a core schema + validation + unknown edges go into "pending" for periodic review.

### 1.1 Schema-First vs Schema-Free

```
┌──────────────────┬──────────────────────────────────┬──────────────────────────────┐
│ Approach         │ Pros                             │ Cons                       │
├──────────────────┼──────────────────────────────────┼──────────────────────────────┤
│ Schema-First     │ Precise, little junk, easy queries│ Misses relations outside schema│
│ (predefined)     │ Strict validation                │ Needs a domain expert        │
│ Schema-Free      │ Flexible, discovers new relations │ Lots of junk, hard queries   │
│ (open extraction)│ No expert needed                 │ Hairball graph              │
│ Hybrid (recommended)│ Best of both                  │ More complex                │
└──────────────────┴──────────────────────────────────┴──────────────────────────────┘
```

### 1.2 Designing an Ontology

> 📄 **Example code:** [`examples/01-1-2-designing-an-ontology.yaml`](examples/01-1-2-designing-an-ontology.yaml)

### 1.3 Validation Code

<details>
<summary>Python Code — Ontology Validation (Click to view)</summary>

> 📄 **Example code:** [`examples/02-1-3-validation-code.py`](examples/02-1-3-validation-code.py)

</details>

---

## 2. Entity Extraction

> **📌 Core Concept:**
> **Entity Extraction = "reading a document and underlining the important entities"** — figuring out who is who (`Nguyen Van A = Person`), what is what (`Phoenix = Project`).
>
> **Analogy:** Like reading a contract and highlighting: person names, project names, organization names, document names.
>
> **4 extraction methods, from "dry" to "smart":**
> - **Rule-based (regex)**: fixed rules like "C-2024" is a contract code — high precision, but only handles known patterns.
> - **NER (spaCy/BERT)**: a pre-trained model recognizes Person/Location/Org — fast, standard for common categories.
> - **Single-round LLM extraction**: call the LLM once for JSON entities — flexible, but easily **misses** things in long texts (the LLM "forgets" later parts).
> - **LLM + Gleaning (recommended for GraphRAG)**: run **multiple rounds** — each round asks "any entities left that were missed?" (the already-extracted list goes into the prompt) → coverage becomes nearly complete.

### 2.1 Method Comparison

```
┌──────────────────┬──────────┬──────────┬──────────────────────────────┐
│ Method           │ Precision│ Recall   │ Best For                     │
├──────────────────┼──────────┼──────────┼──────────────────────────────┤
│ Rule-based (regex)│ ⭐⭐⭐⭐⭐ │ ⭐⭐     │ Fixed patterns (contract codes, dates)│
│ NER (spaCy, BERT)│ ⭐⭐⭐⭐  │ ⭐⭐⭐   │ Person, Org, Location        │
│ LLM (GPT-4o)     │ ⭐⭐⭐   │ ⭐⭐⭐⭐⭐ │ All entity types, context-aware│
│ LLM + Gleaning   │ ⭐⭐⭐⭐  │ ⭐⭐⭐⭐⭐ │ GraphRAG: multiple rounds, full coverage│
└──────────────────┴──────────┴──────────┴──────────────────────────────┘
```

### 2.2 LLM Extraction with a Gleaning Loop (GraphRAG Pattern)

<details>
<summary>Python Code — Entity Extraction with Gleaning (Click to view)</summary>

> 📄 **Example code:** [`examples/03-2-2-llm-extraction-with-a-gleaning-loop.py`](examples/03-2-2-llm-extraction-with-a-gleaning-loop.py)

</details>

### 2.3 Chunking Before Extraction

Like RAG, large documents need to be split up before extraction:

> 📄 **Example code:** [`examples/04-2-3-chunking-before-extraction.py`](examples/04-2-3-chunking-before-extraction.py)

### 2.4 Claims Extraction (GraphRAG Pattern)

> **📌 Core Concept:**
> **Claims = "assertions/facts" worth extracting from a text**, not just entities + relations.
>
> Example from the sentence *"The department needs to cut 20% of its budget next quarter"*:
> - Entities: `the department`, `budget`
> - Relation: who has it valid between whom
> - **Claim**: `{subject: the department, predicate: CUT_BUDGET, object: 20%, period: next quarter, source_chunk: "doc #3"}`
>
> **Why do we need them?** Microsoft's GraphRAG extracts all 3 kinds (entity/relation/claim). Claims make it possible to answer questions of the form **"which regulation / which evidence speaks about X?"** — the LLM answers with a **piece of evidence** (source text) instead of guessing. Each claim is **clickable back to the original chunk** (evidence provenance).

> 📄 **Example code:** [`examples/05-2-4-claims-extraction-graphrag-pattern.py`](examples/05-2-4-claims-extraction-graphrag-pattern.py)

---

## 3. Relation Extraction

### 3.1 Schema-Guided Relation Extraction

<details>
<summary>Python Code — Relation Extraction (Click to view)</summary>

> 📄 **Example code:** [`examples/06-3-1-schema-guided-relation-extraction.py`](examples/06-3-1-schema-guided-relation-extraction.py)

</details>

### 3.2 Confidence Scoring

Each relation should carry a `confidence` for downstream filtering:

> 📄 **Example code:** [`examples/07-3-2-confidence-scoring.py`](examples/07-3-2-confidence-scoring.py)

---

## 4. Entity Resolution & Deduplication

> **📌 Core Concept:**
> **Deduplication = finding and merging "the same person written with two names"** — since the LLM extracts from each chunk separately, **the same entity can end up as multiple nodes**: "Nguyen Van A" (doc 1), "NV A" (doc 2), "Nguyen Van A" (doc 3).
>
> **Analogy:** A company directory listing the same person twice — "Nguyen Van A - CTO" and "Mr. A - technology director". Not merged → the query "who is the CTO?" splits the data in two, wrong answer.
>
> **Dedup levels (simple → smart):**
> 1. **Text normalization**: lowercase, strip diacritics, drop extra words → "Nguyen Van A" == "nguyen van a"
> 2. **Fuzzy match**: Levenshtein/TF-IDF similarity — "Nguyen Van A" vs "Nguyen Van An" is close
> 3. **Embedding similarity**: "CTO Alice" and "Alice, the technology director" are semantically the same
>
> **Warning:** merging too aggressively → **two genuinely different people get fused together** (the HR Alice ≠ the CTO Alice). Always set a **threshold** and allow splitting back apart.

### 4.1 The Problem

```
Raw extraction:
  "Nguyen Van A" (Person)
  "Alice Nguyen" (Person)    ← same person?
  "A. Nguyen"    (Person)

  "Phoenix Project" (Project)
  "Phoenix Project" (Project) ← same project?
  "Phoenix" (Project)
```

### 4.2 Embedding-Based Deduplication

<details>
<summary>Python Code — Deduplication (Click to view)</summary>

> 📄 **Example code:** [`examples/08-4-2-embedding-based-deduplication.py`](examples/08-4-2-embedding-based-deduplication.py)

</details>

### 4.3 Entity Linking & Coreference Resolution

> **📌 Core Concept:**
> **Entity Linking** = attaching a noun/pronoun to **the single correct entity** in the graph (even if it's spelled differently). **Coreference Resolution** = recognizing that "he", "the CEO", and "Mr. A" all point to the same person.
>
> **How is that different from dedup?** Dedup merges *after the fact* (post-extraction). Entity linking happens *at extraction time* — knowing that "NV A" in doc 2 is the existing node "Nguyen Van A".
>
> **Analogy:** Like event registration: 3 people sign up with different names ("Nguyen Van A", "NV A", "Mr. A") — the guard (the linker) has to recognize it's one person so they don't issue 3 different badges.

> 📄 **Example code:** [`examples/09-4-3-entity-linking-coreference-resolution.py`](examples/09-4-3-entity-linking-coreference-resolution.py)

---

## 5. Incremental KG Updates

A production KG changes every day — you can't rebuild the whole thing each time.

> 📄 **Example code:** [`examples/10-5-incremental-kg-updates.py`](examples/10-5-incremental-kg-updates.py)

---

## 6. Complete Pipeline

<details>
<summary>Python Code — End-to-End KG Construction (Click to view)</summary>

> 📄 **Example code:** [`examples/11-6-complete-pipeline.py`](examples/11-6-complete-pipeline.py)

</details>

---

## 7. Agentic KG Construction

> **📌 Core Concept:**
> **Agentic KG construction** = instead of an extract-then-merge batch pipeline, an **LLM agent operates the graph directly via CRUD** (Create/Read/Update/Delete through Cypher). The agent reads the text → writes `CREATE`/`MERGE` queries → checks the results → **catches its own errors and fixes them** when a query is wrong or the information isn't quite right.
>
> **Versus a batch pipeline (the sections above):**
>
> | | Batch Pipeline | Agentic Agent |
> |---|---|---|
> | Flow | One-way: text → extract → merge | Loop: read → write → check → fix |
> | Error handling | Re-run the pipeline | Decides UPDATE/DELETE on its own |
> | Evidence | Not stored | **Every triplet is tagged with a `source_chunk`** for traceability |
> | Cost | Moderate | Higher (more LLM calls) |
> | Good for | Large data, batch | Small KGs, need accuracy, self-adjusting schemas |
>
> **Analogy:** A batch pipeline is like a factory assembly line; an agent is like a **skilled craftsman** — builds while watching, dismantles and fixes mistakes on the spot, and writes a note saying "this brick came from source X".
>
> Notable systems: **KnoBuilder, KG-Agent** (iteratively extract triplets in a loop), **RAGA** (evaluates KG quality, then has the agent fix it). 2025–2026 research shows the agentic approach **significantly reduces incorrect triplets** compared to single-pass batch, at a 2–3× higher cost.

> 📄 **Example code:** [`examples/12-7-agentic-kg-construction.py`](examples/12-7-agentic-kg-construction.py)

---

## 8. Hands-On Labs

### Lab 1: Extract a KG from 5 Documents

- Write a script that reads 5 markdown files in `data/raw_docs/`
- Run `extract_entities` + `extract_relations` for each file
- Merge and deduplicate, print the number of entities/relations

### Lab 2: Single-Pass vs Gleaning

- Extract entities once (gleaning=0) vs 2 rounds (gleaning=2)
- Measure coverage: number of entities extracted, manually compare precision

### Lab 3: Tuning Deduplication

- Try thresholds 0.80, 0.85, 0.90 for `deduplicate_entities`
- Observe: low threshold → over-merging (false positives), high threshold → duplicates slip through

---

## References

- Microsoft GraphRAG — *Entity & Relationship Extraction* (https://microsoft.github.io/graphrag/)
- LangChain — *LLMGraphTransformer* (https://python.langchain.com/docs/use_cases/graph/constructing)
- spaCy — *Named Entity Recognition* (https://spacy.io/usage/linguistic-features#named-entities)
- Microsoft GraphRAG — *Claims Extraction Pattern* (https://microsoft.github.io/graphrag/)
- *Knowledge Graph Agent: An Agentic Construction Benchmark* — KnoBuilder/RAGA/KG-Agent (arXiv 2025)
- *Knowledge Graph Construction Survey* — Paulheim (2017)

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

*Next: [03 — Graph Storage & Query](../03-graph-storage/)*
