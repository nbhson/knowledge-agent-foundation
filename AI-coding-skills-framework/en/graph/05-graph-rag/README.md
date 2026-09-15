# 🔍 05. GraphRAG — Retrieval-Augmented Generation on Graphs

> ## 📑 Table of Contents
>
> - [Opening Story](#opening-story)
> - [Why Does GraphRAG Matter?](#why-does-graphrag-matter)
> - [Overview](#overview)
> - [Contents](#contents)
> - [1. Vanilla RAG vs GraphRAG](#1-vanilla-rag-vs-graphrag)
> - [2. The GraphRAG Pipeline in Detail — 6 Steps](#2-the-graphrag-pipeline-in-detail--6-steps)
> - [3. Local Search vs Global Search](#3-local-search-vs-global-search)
> - [4. Community Summarization](#4-community-summarization)
> - [5. Implementing GraphRAG in Python](#5-implementing-graphrag-in-python)
> - [6. When to Use GraphRAG?](#6-when-to-use-graphrag)
> - [7. Hands-On Labs](#7-hands-on-labs)
> - [References](#references)

---

### Opening Story

You have 1,000 financial reports. You ask:

> *"What are the standout trends in the AI market in 2024?"*

**Vanilla RAG**: chunk 1,000 reports → embed → find the top-5 chunks most similar to the question → feed to the LLM. Result: 5 disconnected passages about "AI trends" but **no big picture** — each chunk only covers one aspect.

**GraphRAG**: before the question even arrives, it has extracted a KG + detected communities (e.g. an "AI Investment" community of 200 entities, an "AI Regulation" community of 150 entities) + summarized each community with an LLM. When asked, it **map-reduces over the community summaries** → a comprehensive answer with **30–40% higher comprehensiveness + diversity** (Microsoft, 2024).

**GraphRAG does not replace RAG. GraphRAG makes RAG smarter using graph structure.**

### Why Does GraphRAG Matter?

> *"Vanilla RAG answers WHERE. GraphRAG answers WHY and HOW, with evidence paths."*

| # | Research | Finding |
|---|-----------|-----------|
| 1 | **Microsoft GraphRAG (2024)** | On global sensemaking Q&A, GraphRAG wins **70%** of the time vs vanilla RAG (LLM judge) |
| 2 | **Microsoft GraphRAG (2024)** | Comprehensiveness: GraphRAG is **+35%**, Diversity: **+30%** vs baseline |
| 3 | **Anthropic (2025)** | Graph-grounded generation cuts **hallucination by 28%** on enterprise QA |

---

## Overview

```
                    ┌─────────────────────────────────┐
                    │         INDEXING PIPELINE         │
                    │         (Offline, once)          │
Documents ──────────►│  Extract KG → Communities →      │
(1K-100K docs)      │  Community Summaries              │
                    └──────────────┬──────────────────┘
                                   │ Graph Index
                    ┌──────────────▼──────────────────┐
                    │       QUERY PIPELINE              │
User Query ────────►│  Local Search  vs  Global Search  │
                    │  (entity-centric)  (community)    │
                    └──────────────┬──────────────────┘
                                   │ Retrieved Context
                    ┌──────────────▼──────────────────┐
                    │     GENERATION (LLM)              │
                    │  Context + Query → Answer + Paths │
                    └─────────────────────────────────┘
```

---

## Contents

| # | Topic | Description |
|---|--------|-------|
| 1 | [Vanilla vs GraphRAG](#1-vanilla-rag-vs-graphrag) | Detailed comparison, trade-offs |
| 2 | [The 6-Step Pipeline](#2-the-graphrag-pipeline-in-detail--6-steps) | From documents to answer |
| 3 | [Local vs Global](#3-local-search-vs-global-search) | The two query modes |
| 4 | [Community Summarization](#4-community-summarization) | Leiden + LLM summarization |
| 5 | [Implementation](#5-implementing-graphrag-in-python) | Complete Python code |
| 6 | [Retriever Types & Fusion](#6-retriever-types--fusion) | Text2Cypher, DRIFT, agentic + RRF |
| 7 | [GraphRAG Variants](#7-graphrag-variants-sota) | LightRAG, HippoRAG2, KAG, GRAG |
| 8 | [When to Use](#8-when-to-use-graphrag) | Decision guide + counter-evidence |
| 9 | [Hands-On Labs](#9-hands-on-labs) | Practice |

---

## 1. Vanilla RAG vs GraphRAG

```
┌──────────────────┬──────────────────────────────────┬──────────────────────────────────┐
│ Aspect           │ Vanilla RAG                      │ GraphRAG                         │
├──────────────────┼──────────────────────────────────┼──────────────────────────────────┤
│ Index unit       │ Chunk embeddings (vector DB)     │ Entities + Relations + Communities│
│ Retrieval        │ Cosine similarity top-K          │ Subgraph traversal + community   │
│ Context          │ 5-10 disconnected chunks         │ Subgraph + community summaries   │
│ Global Q&A       │ ❌ Weak (can't synthesize)       │ ✅ Strong (map-reduce summaries) │
│ Local Q&A        │ ✅ Good                          │ ✅ Good (entity-centric)         │
│ Multi-hop        │ ❌ Hallucinates                  │ ✅ Path-based, with citations    │
│ Cost (indexing)  │ Low (just embedding)             │ High (LLM extraction + summary)  │
│ Cost (query)     │ Low                              │ Medium (traversal + rerank)      │
│ Explainability   │ Low (chunks)                     │ High (path + subgraph)           │
└──────────────────┴──────────────────────────────────┴──────────────────────────────────┘
```

**GraphRAG's indexing cost** is higher (LLM calls to extract + summarize), but it's a **one-time offline cost**. Query cost is equivalent or lower thanks to the more concise context.

```python
# Token cost comparison (estimate for 1000 docs, ~500K tokens)
vanilla_rag_indexing = {
    "embedding": "500K tokens × $0.0001/1K = $0.05",
    "total": "$0.05"
}

graphrag_indexing = {
    "entity_extraction": "500K tokens × $0.005/1K (GPT-4o) × 2 gleanings = $5.00",
    "community_summary": "50 communities × 2K tokens × $0.005/1K = $0.50",
    "embeddings": "$0.05",
    "total": "$5.55 (111× more expensive, but one-time)"
}

# But: query quality improves 30-40% → fewer retries, fewer hallucinations → saves long-term
```

---

## 2. The GraphRAG Pipeline in Detail — 6 Steps

### Step 1: Document Processing & Chunking

```python
from pathlib import Path

class DocumentProcessor:
    def __init__(self, chunk_size=1000, overlap=100):
        self.chunk_size = chunk_size
        self.overlap = overlap
    
    def chunk(self, text: str) -> list[str]:
        chunks = []
        start = 0
        while start < len(text):
            end = start + self.chunk_size
            chunks.append(text[start:end])
            start = end - self.overlap
        return chunks
    
    def process_directory(self, dir_path: str) -> list[dict]:
        all_chunks = []
        for file in Path(dir_path).glob("*.md"):
            text = file.read_text(encoding="utf-8")
            for i, chunk in enumerate(self.chunk(text)):
                all_chunks.append({
                    "id": f"{file.name}#{i}",
                    "text": chunk,
                    "source": str(file),
                })
        return all_chunks
```

### Step 2: Entity & Relation Extraction (LLM)

See details: [`02-knowledge-graph`](../02-knowledge-graph/) — use the gleaning loop `extract_entities` + `extract_relations`.

### Step 3: Community Detection (Leiden)

> **Concept:** split the graph into tightly connected **groups (communities)** — like dividing 1000 employees into teams/departments. Each community = one "topic" grouping all related entities.
>
> **Why is it needed?** Querying an entire graph of millions of nodes is very expensive. Grouping them → you only need to summarize each group (Step 4), and a global query reads the group summaries instead of the raw entities.
>
> The **Leiden** algorithm: an improvement over Louvain — faster + yields more clearly separated communities. Details in §4.1.

### Step 4: Community Summarization (LLM)

> **Concept:** for each community (group) found in Step 3, use the **LLM to summarize it into a short passage** describing what the group is about.
>
> **Analogy:** like a "meeting-minutes summary" for each team: 100 teams → 100 short minutes instead of reading every person's file. When asked "what is the whole company doing?", you only read those 100 minutes.
>
> Result: each community gets one `summary` → stored in the graph as a node/attribute. Details in §4.2.

### Step 5: Retrieval (Local vs Global)

> **Concept:** queries split into two types:
> - **Local Search** (asking details about one entity): find the node → expand neighbors with BFS → collect the embeddings + context of the related nodes
> - **Global Search** (asking the big picture, comparisons, trends): map-reduce over **community summaries** — each summary goes to the LLM, then the results are merged
>
> **Analogy:** Local = looking up one person's file (reading their friends, team, projects). Global = reading a company-wide aggregate report (reading each department, then merging). Details in §3.

### Step 6: Generation (LLM with Graph Context)

> **Concept:** the final step — put the context (a list of entities, relations, paths, or summaries) + the question into the prompt; the LLM produces the answer with **evidence sources** (the triple/paths taken from the graph).
>
> **The difference from regular RAG:** because the context is **graph structure** (not a string of disconnected text), the LLM answers along the relationships — "Alice is friends with Bob through Phoenix" instead of "Alice might know Bob".

The whole pipeline is implemented in detail in §5.

---

## 3. Local Search vs Global Search

This is the **core distinction** of GraphRAG that vanilla RAG doesn't have:

```
┌──────────────────┬──────────────────────────────────┬──────────────────────────────────┐
│                  │ Local Search                     │ Global Search                    │
├──────────────────┼──────────────────────────────────┼──────────────────────────────────┤
│ Sample question  │ "Who approved the Phoenix contract?"│ "What are the AI trends of 2024?" │
│ Starts from      │ Entities in the query            │ All community summaries          │
│ Query            │ Entity → neighbors (1-2 hops)    │ Map-Reduce over summaries        │
│ Context          │ Subgraph around the entities     │ Summaries from many communities  │
│ Best for         │ Factoid, multi-hop, entity Q&A   │ Synthesis, thematic, sensemaking │
│ Similar to vanilla?│ Yes, but with paths             │ No — vanilla RAG can't do this  │
└──────────────────┴──────────────────────────────────┴──────────────────────────────────┘
```

### 3.1 Local Search — Entity-Centric

```
Query: "Who approved the Phoenix contract?"

1. Extract entities from the query: ["Phoenix", "contract"]
2. Find entities in the KG matching the query (vector similarity)
3. Traverse 1-2 hops around those entities:
   Phoenix —[BELONGS_TO]→ Contract C-2024 —[APPROVED_BY]→ Alice (confidence: 0.95)
4. Collect: nodes + edges + text chunks of the entities/relations
5. Re-rank with a cross-encoder
6. Feed the LLM prompt with the paths
```

### 3.2 Global Search — Community-Based

```
Query: "What are the AI trends of 2024?"

1. Do NOT extract entities — the query is too general to map to a specific entity
2. Take ALL community summaries (e.g. 50 communities)
3. Map: the LLM answers the query BASED ON each community summary (in parallel)
   - Community "AI Investment" → "AI investment up 40%..."
   - Community "AI Regulation" → "The EU AI Act takes effect..."
   - Community "AI in Healthcare" → "AI diagnostics increasing..."
4. Reduce: the LLM synthesizes the partial answers into a final answer
5. Each claim carries a citation back to its source community
```

---

## 4. Community Summarization

### 4.1 Community Detection (Leiden Algorithm)

Leiden is currently the best community-detection algorithm (an improvement over Louvain):

```python
import networkx as nx

def detect_communities(graph: nx.Graph, resolution: float = 1.0) -> dict:
    """
    Leiden-style community detection.
    
    resolution: controls granularity
      - low (0.5) → fewer, larger communities
      - high (2.0) → many small communities
    """
    try:
        import community as community_louvain  # python-louvain (Louvain)
        partition = community_louvain.best_partition(graph, resolution=resolution)
    except ImportError:
        # Fallback: greedy modularity
        from networkx.algorithms.community import greedy_modularity_communities
        comms = list(greedy_modularity_communities(graph))
        partition = {}
        for cid, comm in enumerate(comms):
            for node in comm:
                partition[node] = cid
    
    # Group nodes by community
    communities = {}
    for node, cid in partition.items():
        communities.setdefault(cid, []).append(node)
    
    print(f"Detected {len(communities)} communities")
    for cid, members in communities.items():
        print(f"  Community {cid}: {len(members)} nodes — {members[:5]}...")
    
    return communities

# Usage
G = nx.karate_club_graph()
G_labeled = nx.relabel_nodes(G, {n: f"n{n}" for n in G.nodes()})
communities = detect_communities(G_labeled)
```

### 4.2 LLM Community Summarization

<details>
<summary>Python Code — Community Summarization (Click to view)</summary>

```python
import requests

COMMUNITY_SUMMARY_PROMPT = """Summarize the following community in a short, concise paragraph.

Community Members (entities):
{entities}

Relations in the community:
{relations}

Related text chunks:
{chunks}

Summarize:
1. The main topic of this community
2. The important entities and their roles
3. Notable events/relations

Summary (2-4 sentences, concise):
"""

def summarize_community(
    community_id: int,
    members: list[str],
    graph: nx.Graph,
    chunk_map: dict,  # entity -> chunks
    model: str = "gemma3:12b",
) -> str:
    # Collect relations inside the community
    relations = []
    for u in members:
        for v in graph.neighbors(u):
            if v in members:
                edge_data = graph.get_edge_data(u, v)
                relations.append(f"({u}) -[{edge_data.get('type', 'RELATED')}]→ ({v})")
    
    # Collect chunks
    chunks = []
    for m in members[:10]:  # limit to avoid the token limit
        if m in chunk_map:
            chunks.append(chunk_map[m][:500])
    
    prompt = COMMUNITY_SUMMARY_PROMPT.format(
        entities=", ".join(members[:20]),
        relations="\n".join(relations[:20]),
        chunks="\n---\n".join(chunks[:5]),
    )
    
    resp = requests.post(f"{OLLAMA_URL}/api/generate", json={
        "model": model,
        "prompt": prompt,
        "stream": False,
    })
    return resp.json()["response"]

# Summarize all communities
def summarize_all_communities(graph, communities, chunk_map):
    summaries = {}
    for cid, members in communities.items():
        summary = summarize_community(cid, members, graph, chunk_map)
        summaries[cid] = {"members": members, "summary": summary}
        print(f"Community {cid} summary: {summary[:100]}...")
    return summaries
```

</details>

### 4.3 Hierarchical Communities

GraphRAG does **hierarchical clustering**: low-level communities are merged into higher-level communities → creating a hierarchy for global search at multiple levels of detail.

```
Level 0: the whole graph (1 community)
  └── Level 1: 5 large communities (AI, Finance, HR, ...)
        └── Level 2: 20 small communities (AI-Investment, AI-Regulation, ...)
              └── Level 3: Entities + Relations (leaves)
```

---

## 5. Implementing GraphRAG in Python

<details>
<summary>Python Code — Complete GraphRAG Pipeline (Click to view)</summary>

```python
import requests
import networkx as nx
from typing import List, Dict, Optional

OLLAMA_URL = "http://localhost:11434"

# ============================================================
# GRAPH RAG PIPELINE — End-to-End
# ============================================================

class GraphRAG:
    def __init__(self, model: str = "gemma3:12b", embed_model: str = "nomic-embed-text"):
        self.model = model
        self.embed_model = embed_model
        self.graph = nx.Graph()
        self.communities: Dict[int, List[str]] = {}
        self.community_summaries: Dict[int, str] = {}
        self.chunk_map: Dict[str, str] = {}
    
    # ---------- INDEXING (Offline) ----------
    
    def index(self, documents: List[str]):
        """One-time indexing: Documents -> Graph -> Communities -> Summaries"""
        print("Step 1: Extracting entities & relations...")
        for doc in documents:
            entities, relations = self._extract(doc)
            for ent in entities:
                self.graph.add_node(ent["name"], type=ent["type"], description=ent.get("description", ""))
                self.chunk_map[ent["name"]] = doc[:1000]
            for rel in relations:
                self.graph.add_edge(rel["source"], rel["target"], 
                                    type=rel["type"], confidence=rel.get("confidence", 0.8))
        
        print(f"Graph: {self.graph.number_of_nodes()} nodes, {self.graph.number_of_edges()} edges")
        
        print("Step 2: Detecting communities...")
        self.communities = detect_communities(self.graph)
        
        print("Step 3: Summarizing communities...")
        for cid, members in self.communities.items():
            self.community_summaries[cid] = summarize_community(cid, members, self.graph, self.chunk_map, self.model)
        
        print("Indexing complete!")
    
    def _extract(self, text: str) -> tuple:
        """Wrapper for extract_entities + extract_relations (from 02-knowledge-graph)."""
        # Simplified — in production use the gleaning loop
        entities_prompt = f"Extract entities (Person, Project, Document) from:\n{text}\nReturn a JSON list."
        resp = requests.post(f"{OLLAMA_URL}/api/generate", json={
            "model": self.model, "prompt": entities_prompt, "stream": False, "format": "json"
        })
        import json
        try:
            entities = json.loads(resp.json()["response"])
        except:
            entities = []
        
        relations_prompt = f"Entities: {entities}\nText: {text}\nExtract relations (MANAGES, WORKS_ON, APPROVES) as a JSON list."
        resp = requests.post(f"{OLLAMA_URL}/api/generate", json={
            "model": self.model, "prompt": relations_prompt, "stream": False, "format": "json"
        })
        try:
            relations = json.loads(resp.json()["response"])
        except:
            relations = []
        
        return entities, relations
    
    # ---------- LOCAL SEARCH ----------
    
    def local_search(self, query: str, max_hops: int = 2, top_k: int = 5) -> str:
        """Entity-centric search: find entities in the query, traverse the subgraph."""
        # 1. Extract query entities
        query_entities = self._extract_query_entities(query)
        print(f"Query entities: {query_entities}")
        
        # 2. Find matching nodes in the graph (fuzzy match)
        matched_nodes = []
        for qe in query_entities:
            for node in self.graph.nodes():
                if qe.lower() in node.lower() or node.lower() in qe.lower():
                    matched_nodes.append(node)
        
        # Fallback: vector similarity if no exact match
        if not matched_nodes:
            matched_nodes = self._vector_entity_search(query, top_k=3)
        
        print(f"Matched nodes: {matched_nodes}")
        
        # 3. Traverse the subgraph around the matched nodes
        subgraph_context = []
        for node in matched_nodes:
            # BFS 1-2 hops
            for neighbor in nx.single_source_shortest_path_length(self.graph, node, cutoff=max_hops):
                if neighbor == node:
                    continue
                # Get the path
                try:
                    path = nx.shortest_path(self.graph, source=node, target=neighbor)
                    edges = []
                    for i in range(len(path) - 1):
                        edata = self.graph.get_edge_data(path[i], path[i+1])
                        edges.append(f"({path[i]}) -[{edata.get('type','RELATED')}]→ ({path[i+1]})")
                    subgraph_context.append(" → ".join(edges))
                except nx.NetworkXNoPath:
                    continue
        
        # 4. Build the context + generate
        context = "\n".join(subgraph_context[:20])
        chunks = "\n---\n".join(self.chunk_map.get(n, "")[:500] for n in matched_nodes)
        
        prompt = f"""Based on the graph information and documents below, answer the question.

Knowledge graph:
{context}

Related documents:
{chunks}

Question: {query}

Answer concisely, with the proof path if available:
"""
        resp = requests.post(f"{OLLAMA_URL}/api/generate", json={
            "model": self.model, "prompt": prompt, "stream": False
        })
        return resp.json()["response"]
    
    # ---------- GLOBAL SEARCH ----------
    
    def global_search(self, query: str) -> str:
        """Community-based search: map-reduce over the community summaries."""
        # 1. Map: each community summary answers the query
        partial_answers = []
        for cid, summary in self.community_summaries.items():
            map_prompt = f"""Based on the following community summary, answer the question if there is relevant information.
If not relevant, return "No information".

Community Summary: {summary}

Question: {query}

Answer (1-2 sentences, or "No information"):
"""
            resp = requests.post(f"{OLLAMA_URL}/api/generate", json={
                "model": self.model, "prompt": map_prompt, "stream": False
            })
            answer = resp.json()["response"].strip()
            if "no information" not in answer.lower():
                partial_answers.append(f"[Community {cid}]: {answer}")
        
        print(f"Map: {len(partial_answers)}/{len(self.community_summaries)} communities have information")
        
        # 2. Reduce: synthesize
        if not partial_answers:
            return "No relevant information found in the knowledge graph."
        
        reduce_prompt = f"""Synthesize the following partial answers into one complete, comprehensive answer.

Partial answers:
{chr(10).join(partial_answers)}

Original question: {query}

Synthesized answer (structured, concise, with the community sources):
"""
        resp = requests.post(f"{OLLAMA_URL}/api/generate", json={
            "model": self.model, "prompt": reduce_prompt, "stream": False
        })
        return resp.json()["response"]
    
    # ---------- HELPERS ----------
    
    def _extract_query_entities(self, query: str) -> List[str]:
        prompt = f"Extract entities from the following question, return a JSON list of strings:\n{query}"
        resp = requests.post(f"{OLLAMA_URL}/api/generate", json={
            "model": self.model, "prompt": prompt, "stream": False, "format": "json"
        })
        import json
        try:
            return json.loads(resp.json()["response"])
        except:
            return query.split()  # fallback: word split
    
    def _vector_entity_search(self, query: str, top_k: int = 3) -> List[str]:
        """Find entities by vector similarity."""
        query_vec = requests.post(f"{OLLAMA_URL}/api/embed", json={
            "model": self.embed_model, "input": query
        }).json()["embeddings"][0]
        
        import numpy as np
        scores = []
        for node in self.graph.nodes():
            node_vec = requests.post(f"{OLLAMA_URL}/api/embed", json={
                "model": self.embed_model, "input": node
            }).json()["embeddings"][0]
            sim = float(np.dot(query_vec, node_vec) / (np.linalg.norm(query_vec) * np.linalg.norm(node_vec)))
            scores.append((node, sim))
        scores.sort(key=lambda x: x[1], reverse=True)
        return [n for n, _ in scores[:top_k]]

# Usage
rag = GraphRAG(model="gemma3:12b")
rag.index([
    "The Phoenix project was approved by Nguyen Van A. Contract C-2024 belongs to the Phoenix project. Budget 500 million.",
    "Nguyen Van A reports to Tran Thi B, the CTO. Tran Thi B manages a 10-person AI team.",
    "The Atlas project is an AI platform initiated by Tran Thi B. Atlas is related to Phoenix through shared infrastructure.",
])

# Local: factoid
print(rag.local_search("Who approved the Phoenix contract?"))
# → Nguyen Van A (path: Phoenix —BELONGS_TO→ C-2024 —APPROVED_BY→ Alice)

# Global: sensemaking
print(rag.global_search("What are the AI trends in the company?"))
# → Map-reduce over the community summaries
```

</details>

---

## 6. Retriever Types & Fusion

> **📌 Core Concept:**
> **Retriever** here means "the thing that pulls" — the part that decides **what to take** from the graph/vector to feed the LLM. It's not just "Local/Global". In practice there's a **catalog of many retriever types**, each fitting a different kind of question.

### 6.1 Catalog of Retriever Types

| Retriever | How it works | Example question it fits | Neo4j counterpart |
|---|---|---|---|
| **VectorRetriever** | Embed the question → similarity over entities/LLM text | "Find documents about X" | KNN vector index |
| **VectorCypherRetriever** | Vector top-k → **traverse further to neighbors** via Cypher | "Which people are related to documents about X?" | vector + `MATCH` |
| **HybridRetriever** | Vector + full-text → **RRF fusion** | "The keyword 'Phoenix' or fuzzy text" | combined indexes |
| **Text2Cypher** | LLM translates the question → Cypher → run the query | "Who manages the most projects?" | LLM-generated Cypher |
| **DRIFT** (Microsoft) | "Drive the search": fetch as fast and wide as possible | The first path hits a dead end → pivot | Agentic traversal |
| **Tools/Agentic retriever** | An LLM agent picks its own tools (vector/traversal/cypher) | A mix of many question types | `ToolsRetriever` |

### 6.2 Text2Cypher (NL → Cypher) in Detail

> **📌 Core Concept:**
> **Text2Cypher** = the LLM acting as a "translator from human questions to Cypher". Unlike regular retrieval (pulling text back) — here **the answer is the query itself**; once it runs, the DB returns structured results.
>
> The formula for success: **Enhanced Schema Injection** — don't stuff the entire schema in (token-hungry, confuses the LLM); inject only:
> - labels (entity types) + attribute names
> - a few **semantically important parent-child relations** (`(Person)-[:REPORTS_TO]->(Person)`)
>
> ```python
> # Enhanced schema for Text2Cypher — inject only what's needed
> def enhanced_schema_snippet() -> str:
>     return """Nodes: Person(name,role), Project(name,budget)
> Edges: Person-WORKS_ON->Project, Person-REPORTS_TO->Person
> Sample: (Alice,REPORTS_TO,Bob) — Bob is Alice's manager"""
>
> # When a query returns empty → Text2Cypher self-corrects the Cypher statement (Self-correction)
> # When the schema is insufficient → ask for more metadata itself (schema refinement)
> ```

### 6.3 RRF — Merging Multiple Sources Without "Scores"

> **📌 Core Concept:**
> **RRF (Reciprocal Rank Fusion)** = a way to combine multiple ranked lists (from vectors, from graph traversal, from full-text) **without normalizing scores**. The new score for each item:
>
> ```
> score = Σ  1 / (k + rank_i)      with k ≈ 60
> ```
>
> Original meaning: **the higher an item ranks in more lists, the more it gets rewarded**. An item at #1 in vectors (receiving ~1/61) but absent from graph traversal is outscored by an item at #8 that appears in both sources (receiving ~1/68 + 1/68 > 1/61).
>
> **Analogy:** like an "inside track" vote: only people nominated on many different ballots make the final — even if nobody ranked them first. RRF is a technique in the **hybrid retrieval** problem — combining graph traversal results + vector similarity.

```python
import numpy as np

def rrf_score(ranked_lists: list[list[str]], k: int = 60) -> dict[str, float]:
    """Fuse several ranked lists → RRF score, no score normalization needed."""
    fused: dict[str, float] = {}
    for lst in ranked_lists:
        for rank, item in enumerate(lst, start=1):
            fused[item] = fused.get(item, 0.0) + 1.0 / (k + rank)
    return dict(sorted(fused.items(), key=lambda x: -x[1]))

# vector_rank, graph_rank, fulltext_rank = ...  (3 top-k lists)
# final = rrf_score([vector_rank, graph_rank, fulltext_rank])
```

---

## 7. GraphRAG Variants (SOTA)

> **📌 Core Concept:**
> **GraphRAG is not "one formula"** — from Microsoft's original GraphRAG (index + the subsequent connected variants) up to 2025–2026, many different optimization directions have appeared for different problems. The table below is a **map of the most-cited variants**:

| Variant | Core idea | Strong when | Weakness/limits |
|---|---|---|---|
| **GraphRAG (MSFT)** | Index + Leiden communities + LLM summaries | Global/sensemaking, multi-doc | Expensive (indexing costs tokens), slow |
| **LightRAG** | Dual-level index (low/high); retrieval per query; 10× faster than GraphRAG, 1/3–1/4 the cost | Retrieval coverage, low cost | Not as good at global aggregation as the original |
| **HippoRAG (v2)** | Personalized PageRank on the KG + pairwise hybrid | Multi-hop, answers with **fewer tokens** (20× cheaper) | Depends on KG quality |
| **KAG** | KG-augmented generation, semantic reasoning | When explanation/logic answers are needed | Complex configuration |
| **DRIFT (MSFT)** | "Drive the search": explore in as many directions as needed | Complex queries needing multi-direction | Complex agent loop |
| **GRAG** | Divide-and-conquer subgraph retrieval | Less noise on large graphs | Needs a complex pipeline |

> **Summary for picking a variant:**
> - Need **fast + cheap + broad coverage**: `LightRAG`
> - Answer **multi-hop with few tokens**: `HippoRAG2`
> - **Global/sensemaking over the whole corpus**: original `GraphRAG`
> - **Complex queries that need to rethink**: `DRIFT`
>
> In this learning framework, **understanding the mechanisms (index + retrieve + community summary)** matters most — the variants are just refinements of those three stages.

---

## 8. When to Use GraphRAG?

```
┌──────────────────────────┬──────────────┬──────────────────────────────┐
│ Question type            │ Use what?     │ Example                      │
├──────────────────────────┼──────────────┼──────────────────────────────┤
│ Factoid (1-hop)          │ Vanilla RAG  │ "What does section 5 of contract X say?" │
│                          │ or Local     │ "Who manages team Y?"         │
│ Multi-hop (2-4 hops)     │ Local GraphRAG│ "Who approved the contract of project X │
│                          │              │  and who does that person report to?"│
│ Global / Sensemaking     │ Global GraphRAG│ "What are the main themes in these 1000 │
│                          │              │  documents?"            │
│ Aggregation              │ Global       │ "How many AI projects are there │
│                          │              │  and who manages them?"       │
│ Codebase Q&A             │ Local (code  │ "Where is function X called?"   │
│                          │  graph)      │                              │
└──────────────────────────┴──────────────┴──────────────────────────────┘
```

**Decision flowchart:**

```
Does the question need synthesis across MANY documents?
  ├── No → Local Search (entity → subgraph)
  └── Yes → Global Search (community summaries → map-reduce)

Does the question have specific entities?
  ├── Yes → Local Search (start from those entities)
  └── No → Global Search (no anchor to traverse from)
```

> **⚠️ When NOT to Use GraphRAG (2025–2026 benchmark evidence):**
>
> Systematic comparison studies (RAG vs GraphRAG) show **GraphRAG doesn't always win**:
> 1. **Single-hop / factoid**: vanilla RAG **beats** GraphRAG on "single fact" questions (e.g. NQ) — because graph retrieval adds unnecessary traversal cost.
> 2. **Global community search can hallucinate**: a community summary may **lack specific context** → the LLM "makes things up" when asked for details from that summary.
> 3. **Indexing is extremely expensive**: LLM-summarizing all communities ≈ very high indexing cost on large corpora — if you only have 50 internal docs, don't build GraphRAG.
>
> **Pragmatic decision:**
> - Corpus < 100 docs, answers mostly factoid → **vanilla RAG is enough**.
> - Need multi-hop, aggregation, themes spanning many docs → **GraphRAG**.
> - In between: **LightRAG / HippoRAG** (lighter, cheaper text2cypher retriever).

---

## 9. Hands-On Labs

### Lab 1: Compare Vanilla RAG vs GraphRAG

1. Prepare 20 documents on one topic (e.g. "AI in Healthcare" — create or scrape them)
2. Run vanilla RAG (vector top-5) and GraphRAG (local search) on 10 queries
3. Judge manually: which questions does GraphRAG win? (global queries win clearly)

### Lab 2: Tuning Community Resolution

1. Try `resolution` = 0.5, 1.0, 2.0 in `detect_communities`
2. Observe the number of communities and global search quality
3. Find the optimal resolution for your dataset

### Lab 3: Build a Codebase GraphRAG

1. Parse a small repo (50 files) → build a code graph (File → Function → Calls)
2. Ask: "Changing function X affects which files?" → local search on the code graph
3. Compare with plain `grep`

---

## References

- Edge et al. — *From Local to Global: A GraphRAG Approach to Query-Focused Summarization* (Microsoft Research, 2024) — https://arxiv.org/abs/2404.16130
- Microsoft GraphRAG — *GitHub* (https://github.com/microsoft/graphrag) — implementation + config
- Neo4j — *Building a Knowledge Graph with LLM* (https://neo4j.com/blog/developer/knowledge-graph-llm/)
- LangChain — *GraphCypherQAChain* (https://python.langchain.com/docs/use_cases/graph/)
- *GraphRAG in Practice: A Survey of Research Gaps* (arXiv:2507.03226) — RRF, retrieval & indexing at scale
- Neo4j graphrag-python — *Retriever types: Vector, VectorCypher, Hybrid, Text2Cypher, DRIFT* (https://neo4j.com/docs/graphrag-python/current/)
- *RAG vs GraphRAG: A Systematic Evaluation* — multi-hop wins, single-hop loses to vanilla RAG (arXiv 2025)
- LightRAG / HippoRAG2 — *Reducing graph retrieval cost* (https://github.com/HKUDS/LightRAG)

---

*Next: [06 — Graph Reasoning](../06-graph-reasoning/)*
