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

Result: three different "Alice" nodes in the graph that don't connect to each other → the graph is **fragmented**, queries fail.

**Knowledge Graph Construction** solves this problem: **consistent extraction, normalization, and linking** of knowledge from raw text into a queryable graph.

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

```yaml
# ontology.yaml — Schema for an Enterprise KG

node_types:
  Person:
    properties:
      name: {type: string, required: true, unique: true}
      role: {type: string, enum: [CTO, Engineer, Manager, Intern]}
      email: {type: string, format: email}
    indexes: [name]

  Project:
    properties:
      name: {type: string, required: true}
      budget: {type: number, min: 0}
      status: {type: string, enum: [Active, Completed, Cancelled]}
    indexes: [name, status]

  Document:
    properties:
      title: string
      doc_type: {type: string, enum: [Contract, Report, Email]}
      created_at: {type: datetime}

edge_types:
  MANAGES:
    from: Person
    to: Person
    properties:
      since: {type: date}
      confidence: {type: float, min: 0, max: 1}
    temporal: true  # has valid_from / valid_until

  APPROVES:
    from: Person
    to: Document
    properties:
      approved_at: date
      confidence: float

  WORKS_ON:
    from: Person
    to: Project
    properties:
      role: string
      allocation: {type: float, min: 0, max: 1}  # % of time

  BELONGS_TO:
    from: Document
    to: Project

constraints:
  - "Person -[MANAGES]-> Person (cannot manage yourself)"
  - "Project.budget > 0"
  - "APPROVES.confidence >= 0.7 to be considered valid"
```

### 1.3 Validation Code

<details>
<summary>Python Code — Ontology Validation (Click to view)</summary>

```python
from dataclasses import dataclass
from typing import Dict, List, Optional

@dataclass
class Ontology:
    node_types: Dict[str, Dict]
    edge_types: Dict[str, Dict]
    
    def validate_node(self, label: str, props: Dict) -> tuple[bool, str]:
        if label not in self.node_types:
            return False, f"Unknown node type: {label}"
        schema = self.node_types[label]
        for prop, rules in schema.get("properties", {}).items():
            if rules.get("required") and prop not in props:
                return False, f"Missing required property: {prop}"
            if prop in props and "enum" in rules:
                if props[prop] not in rules["enum"]:
                    return False, f"Invalid value for {prop}: {props[prop]}"
        return True, "OK"
    
    def validate_edge(self, edge_type: str, from_label: str, to_label: str) -> tuple[bool, str]:
        if edge_type not in self.edge_types:
            return False, f"Unknown edge type: {edge_type}"
        rule = self.edge_types[edge_type]
        if rule["from"] != from_label or rule["to"] != to_label:
            return False, f"Edge {edge_type} requires {rule['from']} -> {rule['to']}, got {from_label} -> {to_label}"
        if from_label == to_label and edge_type == "MANAGES":
            return False, "Cannot manage self"
        return True, "OK"

# Usage
ontology = Ontology(
    node_types={
        "Person": {"properties": {"name": {"required": True}, "role": {"enum": ["CTO", "Engineer"]}}},
        "Project": {"properties": {"name": {"required": True}}},
    },
    edge_types={
        "MANAGES": {"from": "Person", "to": "Person"},
        "WORKS_ON": {"from": "Person", "to": "Project"},
    }
)
print(ontology.validate_node("Person", {"name": "Alice", "role": "CTO"}))  # (True, OK)
print(ontology.validate_edge("MANAGES", "Person", "Person"))  # (True, OK)
print(ontology.validate_edge("MANAGES", "Project", "Person"))  # (False, ...)
```

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

```python
import requests

OLLAMA_URL = "http://localhost:11434"

EXTRACTION_PROMPT = """Extract entities from the text below.
Only extract these types: Person, Project, Document, Organization.

Text:
{text}

Already extracted (to avoid duplicates):
{already_extracted}

Return a JSON list:
[{{"name": "...", "type": "Person", "description": "..."}}]

If there are no new entities, return []
"""

def extract_entities(text: str, model: str = "gemma3:12b", max_gleanings: int = 2) -> list:
    """Gleaning loop: extract in multiple rounds to increase coverage."""
    all_entities = []
    already = set()
    
    for glean_round in range(max_gleanings + 1):
        prompt = EXTRACTION_PROMPT.format(
            text=text,
            already_extracted=", ".join(already) if already else "none yet"
        )
        
        resp = requests.post(f"{OLLAMA_URL}/api/generate", json={
            "model": model,
            "prompt": prompt,
            "stream": False,
            "format": "json"
        })
        import json as js
        try:
            new_entities = js.loads(resp.json()["response"])
        except:
            new_entities = []
        
        # Filter out duplicates
        added = 0
        for ent in new_entities:
            key = ent["name"].lower().strip()
            if key not in already:
                already.add(key)
                all_entities.append(ent)
                added += 1
        
        print(f"Gleaning round {glean_round}: +{added} entities")
        if added == 0:
            break  # Nothing new left
    
    return all_entities

# Usage
text = """
The Phoenix project was approved by Nguyen Van A. Contract C-2024 belongs to the Phoenix project.
Nguyen Van A reports to Tran Thi B, the company's CTO. Tran Thi B manages the AI team.
"""
entities = extract_entities(text)
print(entities)
# [{"name": "Nguyen Van A", "type": "Person", ...}, {"name": "Phoenix", "type": "Project", ...}, ...]
```

</details>

### 2.3 Chunking Before Extraction

Like RAG, large documents need to be split up before extraction:

```python
def chunk_for_extraction(text: str, chunk_size: int = 1000, overlap: int = 100) -> list[str]:
    """Split a document into chunks for extraction — extract each chunk separately, then merge."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
    return chunks

# Extract from each chunk, then merge entities
def extract_from_document(doc_text: str) -> list:
    chunks = chunk_for_extraction(doc_text)
    all_entities = []
    for chunk in chunks:
        all_entities.extend(extract_entities(chunk, max_gleanings=1))
    return all_entities
```

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

```python
CLAIM_PROMPT = """Extract assertions (claims) from the text.
Each claim = one fact worth keeping, with a simple header (topic).

Text:
{text}

Return a JSON list, each element:
{{"subject": "...", "predicate": "...", "object": "...", "description": "..."}}
If there are no claims, return []
"""

def extract_claims(text: str, model: str = "gemma3:12b") -> list:
    # (implementation similar to extract_entities — call the LLM, parse JSON)
    ...
    return claims

# Each claim is LINKED to its source chunk → traceable back to the document
def attach_claims(chunks: list[dict]) -> list[dict]:
    for chunk in chunks:
        claims = extract_claims(chunk["text"])
        for c in claims:
            c["source_chunk_id"] = chunk["id"]   # ← evidence provenance
    return ...
```

---

## 3. Relation Extraction

### 3.1 Schema-Guided Relation Extraction

<details>
<summary>Python Code — Relation Extraction (Click to view)</summary>

```python
RELATION_PROMPT = """Given a list of entities and a text, extract relations.

Entities:
{entities}

Text:
{text}

Valid relation types:
- MANAGES: Person -> Person
- APPROVES: Person -> Document
- WORKS_ON: Person -> Project
- BELONGS_TO: Document -> Project
- REPORTS_TO: Person -> Person

Return JSON:
[{{"source": "Nguyen Van A", "target": "Contract C-2024", "type": "APPROVES", "confidence": 0.9, "evidence": "..."}}]
"""

def extract_relations(text: str, entities: list, model: str = "gemma3:12b") -> list:
    ent_str = "\n".join(f"- {e['name']} ({e['type']})" for e in entities)
    prompt = RELATION_PROMPT.format(entities=ent_str, text=text)
    
    resp = requests.post(f"{OLLAMA_URL}/api/generate", json={
        "model": model,
        "prompt": prompt,
        "stream": False,
        "format": "json"
    })
    import json as js
    try:
        return js.loads(resp.json()["response"])
    except:
        return []

# Usage
relations = extract_relations(text, entities)
print(relations)
# [{"source": "Nguyen Van A", "target": "Contract C-2024", "type": "APPROVES", "confidence": 0.9}, ...]
```

</details>

### 3.2 Confidence Scoring

Each relation should carry a `confidence` for downstream filtering:

```python
def filter_by_confidence(relations: list, threshold: float = 0.7) -> list:
    """Keep only relations with confidence >= threshold."""
    filtered = [r for r in relations if r.get("confidence", 0) >= threshold]
    print(f"Filtered: {len(relations)} -> {len(filtered)} (threshold={threshold})")
    return filtered
```

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

```python
import numpy as np

def cosine_sim(a, b):
    a, b = np.array(a), np.array(b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

def embed(text: str, model: str = "nomic-embed-text") -> list[float]:
    resp = requests.post(f"{OLLAMA_URL}/api/embed", json={"model": model, "input": text})
    return resp.json()["embeddings"][0]

def deduplicate_entities(entities: list, threshold: float = 0.85) -> list:
    """
    Merge duplicate entities based on embedding similarity.
    Keep the first entity as the canonical one.
    """
    if not entities:
        return []
    
    # Embed each entity name
    embeddings = [embed(e["name"]) for e in entities]
    
    canonical = []  # list of (entity, embedding)
    mapping = {}    # old_name -> canonical_name
    
    for ent, emb in zip(entities, embeddings):
        found = False
        for canon_ent, canon_emb in canonical:
            if ent["type"] != canon_ent["type"]:
                continue  # Only compare the same type
            sim = cosine_sim(emb, canon_emb)
            if sim >= threshold:
                mapping[ent["name"]] = canon_ent["name"]
                # Merge properties
                print(f"Dedup: '{ent['name']}' -> '{canon_ent['name']}' (sim={sim:.3f})")
                found = True
                break
        
        if not found:
            canonical.append((ent, emb))
            mapping[ent["name"]] = ent["name"]
    
    # Return the canonical entities + mapping to fix relations
    canonical_entities = [c[0] for c in canonical]
    return canonical_entities, mapping

def remap_relations(relations: list, mapping: dict) -> list:
    """Fix source/target in relations according to the dedup mapping."""
    for r in relations:
        r["source"] = mapping.get(r["source"], r["source"])
        r["target"] = mapping.get(r["target"], r["target"])
    # Drop self-loops created by dedup
    return [r for r in relations if r["source"] != r["target"]]

# Usage
entities_raw = [
    {"name": "Nguyen Van A", "type": "Person"},
    {"name": "Alice Nguyen", "type": "Person"},
    {"name": "Phoenix", "type": "Project"},
    {"name": "Phoenix Project", "type": "Project"},
]
canonical, mapping = deduplicate_entities(entities_raw, threshold=0.80)
print(f"Canonical: {[c['name'] for c in canonical]}")
print(f"Mapping: {mapping}")
```

</details>

### 4.3 Entity Linking & Coreference Resolution

> **📌 Core Concept:**
> **Entity Linking** = attaching a noun/pronoun to **the single correct entity** in the graph (even if it's spelled differently). **Coreference Resolution** = recognizing that "he", "the CEO", and "Mr. A" all point to the same person.
>
> **How is that different from dedup?** Dedup merges *after the fact* (post-extraction). Entity linking happens *at extraction time* — knowing that "NV A" in doc 2 is the existing node "Nguyen Van A".
>
> **Analogy:** Like event registration: 3 people sign up with different names ("Nguyen Van A", "NV A", "Mr. A") — the guard (the linker) has to recognize it's one person so they don't issue 3 different badges.

```python
# Coreference in text: "Alice signed the contract. She delivered 200m."
# → "She" = Alice (coreference)
# → "Alice" (written "A. Nguyen" in another doc) = the existing Alice node (entity linking)

def entity_linking(mention: str, graph_entities: list[str], embedding_fn) -> str:
    """Link a mention ('A. Nguyen') to the canonical entity via similarity."""
    best, best_score = None, 0
    v_mention = embedding_fn(mention)
    for ent in graph_entities:
        score = cosine(v_mention, embedding_fn(ent))
        if score > best_score:
            best, best_score = ent, score
    return best if best_score > 0.85 else None   # below threshold → NEW entity
```

---

## 5. Incremental KG Updates

A production KG changes every day — you can't rebuild the whole thing each time.

```python
class IncrementalKGUpdater:
    """Update the KG event-by-event — add/modify/delete without rebuilding."""
    
    def __init__(self, graph):
        self.graph = graph  # Neo4j / NetworkX / Kuzu
    
    def upsert_entity(self, entity: dict):
        """Add or update an entity (based on the unique key)."""
        # Cypher: MERGE (create if absent, update if present)
        query = """
        MERGE (n:Person {name: $name})
        SET n.role = $role, n.updated_at = datetime()
        RETURN n
        """
        self.graph.query(query, params=entity)
    
    def upsert_relation(self, source: str, target: str, rel_type: str, props: dict):
        query = f"""
        MATCH (a {{name: $source}}), (b {{name: $target}})
        MERGE (a)-[r:{rel_type}]->(b)
        SET r.confidence = $confidence, r.updated_at = datetime()
        RETURN r
        """
        self.graph.query(query, params={"source": source, "target": target, **props})
    
    def soft_delete(self, node_name: str):
        """Soft delete: mark it, don't hard-delete — keep the history."""
        query = """
        MATCH (n {name: $name})
        SET n.deleted = true, n.deleted_at = datetime()
        """
        self.graph.query(query, params={"name": node_name})
    
    def process_new_document(self, doc_text: str, doc_id: str):
        """Pipeline for a new document: extract → dedup → upsert."""
        entities = extract_entities(doc_text)
        relations = extract_relations(doc_text, entities)
        canonical, mapping = deduplicate_entities(entities)
        relations = remap_relations(relations, mapping)
        
        for ent in canonical:
            self.upsert_entity(ent)
        for rel in relations:
            self.upsert_relation(rel["source"], rel["target"], rel["type"], rel)
        
        print(f"Ingested doc {doc_id}: {len(canonical)} entities, {len(relations)} relations")
```

---

## 6. Complete Pipeline

<details>
<summary>Python Code — End-to-End KG Construction (Click to view)</summary>

```python
def build_knowledge_graph(documents: list[str], ontology: Ontology) -> dict:
    """
    Complete pipeline: Documents -> Knowledge Graph
    """
    all_entities = []
    all_relations = []
    
    # Step 1: Extract from each document
    for doc in documents:
        entities = extract_entities(doc, max_gleanings=2)
        relations = extract_relations(doc, entities)
        all_entities.extend(entities)
        all_relations.extend(relations)
    
    print(f"Raw: {len(all_entities)} entities, {len(all_relations)} relations")
    
    # Step 2: Deduplicate
    canonical_entities, mapping = deduplicate_entities(all_entities, threshold=0.85)
    all_relations = remap_relations(all_relations, mapping)
    
    print(f"After dedup: {len(canonical_entities)} entities, {len(all_relations)} relations")
    
    # Step 3: Validate against the ontology
    valid_entities = []
    for ent in canonical_entities:
        ok, msg = ontology.validate_node(ent["type"], ent)
        if ok:
            valid_entities.append(ent)
        else:
            print(f"Invalid entity {ent['name']}: {msg}")
    
    valid_relations = []
    for rel in all_relations:
        # Find the type of source/target
        src_type = next((e["type"] for e in valid_entities if e["name"] == rel["source"]), None)
        tgt_type = next((e["type"] for e in valid_entities if e["name"] == rel["target"]), None)
        if src_type and tgt_type:
            ok, msg = ontology.validate_edge(rel["type"], src_type, tgt_type)
            if ok and rel.get("confidence", 0) >= 0.7:
                valid_relations.append(rel)
            else:
                print(f"Invalid relation {rel}: {msg}")
    
    print(f"After validation: {len(valid_entities)} entities, {len(valid_relations)} relations")
    
    return {"entities": valid_entities, "relations": valid_relations}

# Usage
docs = [
    "The Phoenix project was approved by Nguyen Van A. Contract C-2024 belongs to the Phoenix project.",
    "Nguyen Van A reports to Tran Thi B, the CTO. Tran Thi B manages an AI team of 10 engineers.",
]
kg = build_knowledge_graph(docs, ontology)
print(kg)
```

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

```python
# Pseudocode — an agent building a KG (using Cypher + check queries)
TOOLS = ["create_entity", "link_entities", "query_graph", "delete_triplet"]

def agent_build_chunk(chunk_text: str, cypher_exec) -> list[str]:
    """The agent reads the chunk, decides CRUD operations, then verifies itself."""
    actions = []
    # 1) PLAN: the LLM decides which triplets to add
    triplets = llm(f"From the passage below, which (entity, relation, entity) are worth recording? {chunk_text}")
    for subj, rel, obj in triplets:
        # 2) ACTION: try MERGE + SET source for traceability
        cypher_exec("""
            MERGE (s {name:$subj}) 
            ON CREATE SET s.source_chunk=$chunk
            WITH s
            MATCH (t {name: $obj})
            MERGE (s)-[r:REL {type:$rel}]->(t)
            SET r.source_chunk=$chunk
        """, subj=subj, rel=rel, obj=obj, chunk=chunk_text[:100])
        actions.append(f"CREATE {subj}--{rel}-->{obj}")
    # 3) VERIFY: at the end of the chunk, ask the LLM again to check what was just written
    review = llm(f"Are these triplets correct/complete? {triplets}")
    if "needs fixing" in review:
        cypher_exec("DELETE ...")  # the agent fixes it itself (UPDATE/DELETE)
        actions.append("FIX: " + review)
    return actions
```

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

*Next: [03 — Graph Storage & Query](../03-graph-storage/)*
