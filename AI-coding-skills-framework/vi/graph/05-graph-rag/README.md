# 🔍 05. GraphRAG — Retrieval-Augmented Generation Trên Đồ Thị

> ## 📑 Mục Lục
>
> - [Câu Chuyện Mở Đầu](#câu-chuyện-mở-đầu)
> - [Tại Sao GraphRAG Quan Trọng?](#tại-sao-graphrag-quan-trọng)
> - [Tổng Quan](#tổng-quan)
> - [Nội Dung](#nội-dung)
> - [1. Vanilla RAG vs GraphRAG](#1-vanilla-rag-vs-graphrag)
> - [2. GraphRAG Pipeline Chi Tiết — 6 Bước](#2-graphrag-pipeline-chi-tiết-6-bước)
> - [3. Local Search vs Global Search](#3-local-search-vs-global-search)
> - [4. Community Summarization](#4-community-summarization)
> - [5. Triển Khai GraphRAG Với Python](#5-triển-khai-graphrag-với-python)
> - [6. Khi Nào Dùng GraphRAG?](#6-khi-nào-dùng-graphrag)
> - [7. Labs Thực Hành](#7-labs-thực-hành)
> - [Tài Liệu Tham Khảo](#tài-liệu-tham-khảo)

---

### Câu Chuyện Mở Đầu

Bạn có 1,000 báo cáo tài chính. Bạn hỏi:

> *"Thị trường AI năm 2024 có xu hướng gì nổi bật?"*

**Vanilla RAG**: chunk 1,000 báo cáo → embed → tìm top-5 chunks giống câu hỏi nhất → đưa vào LLM. Kết quả: 5 đoạn văn rời rạc về "AI trend" nhưng **thiếu bức tranh tổng thể** — mỗi chunk chỉ nói về 1 khía cạnh.

**GraphRAG**: trước khi có câu hỏi, đã trích KG + phát hiện communities (ví dụ: community "AI Investment" gồm 200 entities, community "AI Regulation" gồm 150 entities) + tóm tắt từng community bằng LLM. Khi hỏi, **map-reduce trên community summaries** → trả lời toàn diện với **comprehensiveness + diversity** cao hơn 30-40% (Microsoft, 2024).

**GraphRAG không thay thế RAG. GraphRAG làm RAG thông minh hơn bằng cấu trúc đồ thị.**

### Tại Sao GraphRAG Quan Trọng?

> *"Vanilla RAG answers WHERE. GraphRAG answers WHY and HOW, with evidence paths."*

| # | Nghiên Cứu | Phát Hiện |
|---|-----------|-----------|
| 1 | **Microsoft GraphRAG (2024)** | Trên global sensemaking Q&A, GraphRAG win rate **70%** vs vanilla RAG (LLM judge) |
| 2 | **Microsoft GraphRAG (2024)** | Comprehensiveness: GraphRAG **+35%**, Diversity: **+30%** vs baseline |
| 3 | **Anthropic (2025)** | Graph-grounded generation giảm **28% hallucination** trên enterprise QA |

---

## Tổng Quan

```
                    ┌─────────────────────────────────┐
                    │         INDEXING PIPELINE         │
                    │         (Offline, 1 lần)          │
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

## Nội Dung

| # | Chủ đề | Mô tả |
|---|--------|-------|
| 1 | [Vanilla vs GraphRAG](#1-vanilla-rag-vs-graphrag) | So sánh chi tiết, trade-offs |
| 2 | [Pipeline 6 Bước](#2-graphrag-pipeline-chi-tiết-6-bước) | Từ documents đến answer |
| 3 | [Local vs Global](#3-local-search-vs-global-search) | 2 chế độ truy vấn |
| 4 | [Community Summarization](#4-community-summarization) | Leiden + LLM summarization |
| 5 | [Triển Khai](#5-triển-khai-graphrag-với-python) | Code Python hoàn chỉnh |
| 6 | [Retriever Types & Fusion](#6-retriever-types--fusion) | Text2Cypher, DRIFT, agentic + RRF |
| 7 | [GraphRAG Variants](#7-graphrag-variants-sota) | LightRAG, HippoRAG2, KAG, GRAG |
| 8 | [Khi Nào Dùng](#8-khi-nào-dùng-graphrag) | Decision guide + counter-evidence |
| 9 | [Labs Thực Hành](#9-labs-thực-hành) | Practice |

---

## 1. Vanilla RAG vs GraphRAG

```
┌──────────────────┬──────────────────────────────────┬──────────────────────────────────┐
│ Khía cạnh        │ Vanilla RAG                      │ GraphRAG                         │
├──────────────────┼──────────────────────────────────┼──────────────────────────────────┤
│ Đơn vị index     │ Chunk embeddings (vector DB)     │ Entities + Relations + Communities│
│ Retrieval        │ Cosine similarity top-K          │ Subgraph traversal + community   │
│ Context          │ 5-10 chunks rời rạc              │ Subgraph + community summaries   │
│ Global Q&A       │ ❌ Yếu (không tổng hợp được)     │ ✅ Mạnh (map-reduce summaries)   │
│ Local Q&A        │ ✅ Tốt                           │ ✅ Tốt (entity-centric)          │
│ Multi-hop        │ ❌ Hallucinate                   │ ✅ Path-based, có citation       │
│ Cost (indexing)  │ Thấp (chỉ embed)                 │ Cao (LLM extraction + summary)   │
│ Cost (query)     │ Thấp                             │ Trung bình (traversal + rerank)  │
│ Explainability   │ Thấp (chunks)                    │ Cao (path + subgraph)            │
└──────────────────┴──────────────────────────────────┴──────────────────────────────────┘
```

**Chi phí indexing GraphRAG** đắt hơn (tốn LLM calls để extract + summarize), nhưng là **one-time offline cost**. Query cost tương đương hoặc thấp hơn nhờ context ngắn gọn hơn.

```python
# So sánh token cost (ước tính cho 1000 docs, ~500K tokens)
vanilla_rag_indexing = {
    "embedding": "500K tokens × $0.0001/1K = $0.05",
    "total": "$0.05"
}

graphrag_indexing = {
    "entity_extraction": "500K tokens × $0.005/1K (GPT-4o) × 2 gleanings = $5.00",
    "community_summary": "50 communities × 2K tokens × $0.005/1K = $0.50",
    "embeddings": "$0.05",
    "total": "$5.55 (111× đắt hơn, nhưng one-time)"
}

# Nhưng: query quality tăng 30-40% → ít retry, ít hallucination → tiết kiệm long-term
```

---

## 2. GraphRAG Pipeline Chi Tiết — 6 Bước

### Bước 1: Document Processing & Chunking

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

### Bước 2: Entity & Relation Extraction (LLM)

Xem chi tiết: [`02-knowledge-graph`](../02-knowledge-graph/) — dùng gleaning loop `extract_entities` + `extract_relations`.

### Bước 3: Community Detection (Leiden)

> **Khái niệm:** Chia graph thành các **nhóm (communities)** liên kết chặt — giống chia 1000 nhân viên thành các team/phòng ban. Mỗi community = 1 "chủ đề" gom tất cả entities liên quan nhau.
>
> **Tại sao cần?** Truy vấn toàn graph hàng triệu nodes rất đắt. Gom thành nhóm → chỉ cần tóm tắt từng nhóm (Bước 4), truy vấn toàn cục chỉ đọc tóm tắt nhóm thay vì đọc nguyên entities.
>
> Thuật toán **Leiden**: cải tiến của Louvain — nhanh hơn + cho cộng đồng tách biệt rõ hơn. Chi tiết ở §4.1.

### Bước 4: Community Summarization (LLM)

> **Khái niệm:** Với mỗi community (nhóm) tìm được ở Bước 3, dùng **LLM tóm tắt thành 1 đoạn ngắn** mô tả nhóm đó nói về gì.
>
> **Analogies:** Giống "tóm tắt biên bản họp" cho từng team: có 100 team → 100 biên bản ngắn thay vì phải đọc hồ sơ từng người. Khi hỏi "cả công ty đang làm gì?", chỉ cần đọc 100 biên bản đó.
>
> Kết quả: mỗi community có 1 `summary` → lưu vào graph như node/attribute. Chi tiết ở §4.2.

### Bước 5: Retrieval (Local vs Global)

> **Khái niệm:** Truy vấn được chia thành 2 loại:
> - **Local Search** (hỏi chi tiết về 1 thực thể): tìm node→ expand neighbors theo BFS → lấy embeddings + context của nodes liên quan
> - **Global Search** (hỏi tổng quan, so sánh, xu hướng): map- reduce trên **community summaries** — mỗi summary cho LLM, rồi gộp kết quả
>
> **Analogies:** Local = tra cứu hồ sơ 1 người (đọc bạn bè, team, dự án). Global = đọc báo cáo tổng hợp cả công ty (đọc từng phòng ban rồi gộp lại). Chi tiết ở §3.

### Bước 6: Generation (LLM với Graph Context)

> **Khái niệm:** Bước cuối — đưa context (danh sách entities, relations, paths, hoặc summaries) + câu hỏi vào prompt, LLM tạo câu trả lời kèm **nguồn bằng chứng** (các triple/path lấy từ graph).
>
> **Điểm khác RAG thường:** Vì context là **cấu trúc graph** (không phải chuỗi text rời rạc), LLM trả lời theo quan hệ — "Alice thông qua Phoenix nên bạn của Alice là Bob" thay vì "có thể Alice biết Bob".

Toàn bộ pipeline được triển khai chi tiết ở §5.

---

## 3. Local Search vs Global Search

Đây là **phân biệt cốt lõi** của GraphRAG mà vanilla RAG không có:

```
┌──────────────────┬──────────────────────────────────┬──────────────────────────────────┐
│                  │ Local Search                     │ Global Search                    │
├──────────────────┼──────────────────────────────────┼──────────────────────────────────┤
│ Câu hỏi mẫu      │ "Ai phê duyệt hợp đồng Phoenix?"│ "Xu hướng AI 2024 là gì?"        │
│ Bắt đầu từ       │ Entities trong query             │ Tất cả community summaries       │
│ Truy vấn         │ Entity → neighbors (1-2 hops)   │ Map-Reduce trên summaries        │
│ Context          │ Subgraph quanh entities          │ Tóm tắt từ nhiều communities     │
│ Phù hợp          │ Factoid, multi-hop, entity Q&A  │ Tổng hợp, thematic, sensemaking  │
│ Tương tự vanilla?│ Có, nhưng có path               │ Không — vanilla RAG không làm được│
└──────────────────┴──────────────────────────────────┴──────────────────────────────────┘
```

### 3.1 Local Search — Entity-Centric

```
Query: "Ai phê duyệt hợp đồng Phoenix?"

1. Extract entities từ query: ["Phoenix", "hợp đồng"]
2. Tìm entities trong KG khớp với query (vector similarity)
3. Traverse 1-2 hops quanh entities đó:
   Phoenix —[BELONGS_TO]→ Contract C-2024 —[APPROVED_BY]→ Alice (confidence: 0.95)
4. Thu thập: nodes + edges + text chunks của entities/relations
5. Re-rank bằng cross-encoder
6. Đưa vào LLM prompt với path
```

### 3.2 Global Search — Community-Based

```
Query: "Xu hướng AI 2024 là gì?"

1. KHÔNG extract entities — query quá chung, không map được vào entity cụ thể
2. Lấy TẤT CẢ community summaries (ví dụ 50 communities)
3. Map: LLM trả lời query DỰA TRÊN từng community summary (parallel)
   - Community "AI Investment" → "Đầu tư AI tăng 40%..."
   - Community "AI Regulation" → "EU AI Act có hiệu lực..."
   - Community "AI in Healthcare" → "AI chẩn đoán tăng..."
4. Reduce: LLM tổng hợp các partial answers thành final answer
5. Mỗi claim có citation về community nguồn
```

---

## 4. Community Summarization

### 4.1 Community Detection (Leiden Algorithm)

Leiden là thuật toán phát hiện community tốt nhất hiện tại (cải tiến Louvain):

```python
import networkx as nx

def detect_communities(graph: nx.Graph, resolution: float = 1.0) -> dict:
    """
    Leiden-style community detection.
    
    resolution: điều khiển granularity
      - thấp (0.5) → ít community lớn
      - cao (2.0) → nhiều community nhỏ
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
    
    # Nhóm nodes theo community
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
<summary>Python Code — Community Summarization (Click để xem)</summary>

```python
import requests

COMMUNITY_SUMMARY_PROMPT = """Tóm tắt community sau thành 1 đoạn văn ngắn gọn.

Community Members (entities):
{entities}

Relations trong community:
{relations}

Text chunks liên quan:
{chunks}

Hãy tóm tắt:
1. Chủ đề chính của community này
2. Các thực thể quan trọng và vai trò
3. Các sự kiện/quan hệ nổi bật

Tóm tắt (2-4 câu, súc tích):
"""

def summarize_community(
    community_id: int,
    members: list[str],
    graph: nx.Graph,
    chunk_map: dict,  # entity -> chunks
    model: str = "gemma3:12b",
) -> str:
    # Thu thập relations trong community
    relations = []
    for u in members:
        for v in graph.neighbors(u):
            if v in members:
                edge_data = graph.get_edge_data(u, v)
                relations.append(f"({u}) -[{edge_data.get('type', 'RELATED')}]→ ({v})")
    
    # Thu thập chunks
    chunks = []
    for m in members[:10]:  # giới hạn để không vượt token limit
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

# Summarize tất cả communities
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

GraphRAG làm **hierarchical clustering**: communities cấp thấp gộp thành communities cấp cao → tạo hierarchy cho global search ở nhiều mức độ chi tiết.

```
Level 0: Toàn bộ graph (1 community)
  └── Level 1: 5 communities lớn (AI, Finance, HR, ...)
        └── Level 2: 20 communities nhỏ (AI-Investment, AI-Regulation, ...)
              └── Level 3: Entities + Relations (leaves)
```

---

## 5. Triển Khai GraphRAG Với Python

<details>
<summary>Python Code — Complete GraphRAG Pipeline (Click để xem)</summary>

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
        """Wrapper cho extract_entities + extract_relations (từ 02-knowledge-graph)."""
        # Simplified — trong production dùng gleaning loop
        entities_prompt = f"Trích entities (Person, Project, Document) từ:\n{text}\nTrả về JSON list."
        resp = requests.post(f"{OLLAMA_URL}/api/generate", json={
            "model": self.model, "prompt": entities_prompt, "stream": False, "format": "json"
        })
        import json
        try:
            entities = json.loads(resp.json()["response"])
        except:
            entities = []
        
        relations_prompt = f"Entities: {entities}\nText: {text}\nTrích relations (MANAGES, WORKS_ON, APPROVES) JSON list."
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
        """Entity-centric search: tìm entities trong query, traverse subgraph."""
        # 1. Extract query entities
        query_entities = self._extract_query_entities(query)
        print(f"Query entities: {query_entities}")
        
        # 2. Tìm nodes khớp trong graph (fuzzy match)
        matched_nodes = []
        for qe in query_entities:
            for node in self.graph.nodes():
                if qe.lower() in node.lower() or node.lower() in qe.lower():
                    matched_nodes.append(node)
        
        # Fallback: vector similarity nếu không match chính xác
        if not matched_nodes:
            matched_nodes = self._vector_entity_search(query, top_k=3)
        
        print(f"Matched nodes: {matched_nodes}")
        
        # 3. Traverse subgraph quanh matched nodes
        subgraph_context = []
        for node in matched_nodes:
            # BFS 1-2 hops
            for neighbor in nx.single_source_shortest_path_length(self.graph, node, cutoff=max_hops):
                if neighbor == node:
                    continue
                # Lấy path
                try:
                    path = nx.shortest_path(self.graph, source=node, target=neighbor)
                    edges = []
                    for i in range(len(path) - 1):
                        edata = self.graph.get_edge_data(path[i], path[i+1])
                        edges.append(f"({path[i]}) -[{edata.get('type','RELATED')}]→ ({path[i+1]})")
                    subgraph_context.append(" → ".join(edges))
                except nx.NetworkXNoPath:
                    continue
        
        # 4. Build context + Generate
        context = "\n".join(subgraph_context[:20])
        chunks = "\n---\n".join(self.chunk_map.get(n, "")[:500] for n in matched_nodes)
        
        prompt = f"""Dựa trên thông tin đồ thị và tài liệu sau, trả lời câu hỏi.

Đồ thị tri thức:
{context}

Tài liệu liên quan:
{chunks}

Câu hỏi: {query}

Trả lời súc tích, kèm đường dẫn chứng minh (path) nếu có:
"""
        resp = requests.post(f"{OLLAMA_URL}/api/generate", json={
            "model": self.model, "prompt": prompt, "stream": False
        })
        return resp.json()["response"]
    
    # ---------- GLOBAL SEARCH ----------
    
    def global_search(self, query: str) -> str:
        """Community-based search: map-reduce trên community summaries."""
        # 1. Map: mỗi community summary trả lời query
        partial_answers = []
        for cid, summary in self.community_summaries.items():
            map_prompt = f"""Dựa trên tóm tắt community sau, trả lời câu hỏi nếu có thông tin liên quan.
Nếu không liên quan, trả về "Không có thông tin".

Community Summary: {summary}

Câu hỏi: {query}

Trả lời (1-2 câu, hoặc "Không có thông tin"):
"""
            resp = requests.post(f"{OLLAMA_URL}/api/generate", json={
                "model": self.model, "prompt": map_prompt, "stream": False
            })
            answer = resp.json()["response"].strip()
            if "không có thông tin" not in answer.lower():
                partial_answers.append(f"[Community {cid}]: {answer}")
        
        print(f"Map: {len(partial_answers)}/{len(self.community_summaries)} communities có thông tin")
        
        # 2. Reduce: tổng hợp
        if not partial_answers:
            return "Không tìm thấy thông tin liên quan trong knowledge graph."
        
        reduce_prompt = f"""Tổng hợp các câu trả lời bộ phận sau thành một câu trả lời hoàn chỉnh, toàn diện.

Các câu trả lời bộ phận:
{chr(10).join(partial_answers)}

Câu hỏi gốc: {query}

Câu trả lời tổng hợp (có cấu trúc, súc tích, kèm nguồn community):
"""
        resp = requests.post(f"{OLLAMA_URL}/api/generate", json={
            "model": self.model, "prompt": reduce_prompt, "stream": False
        })
        return resp.json()["response"]
    
    # ---------- HELPERS ----------
    
    def _extract_query_entities(self, query: str) -> List[str]:
        prompt = f"Trích entities từ câu hỏi sau, trả về JSON list of strings:\n{query}"
        resp = requests.post(f"{OLLAMA_URL}/api/generate", json={
            "model": self.model, "prompt": prompt, "stream": False, "format": "json"
        })
        import json
        try:
            return json.loads(resp.json()["response"])
        except:
            return query.split()  # fallback: split words
    
    def _vector_entity_search(self, query: str, top_k: int = 3) -> List[str]:
        """Tìm entities bằng vector similarity."""
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
    "Dự án Phoenix do Nguyễn Văn A phê duyệt. Hợp đồng C-2024 thuộc dự án Phoenix. Ngân sách 500 triệu.",
    "Nguyễn Văn A báo cáo cho Trần Thị B, CTO. Trần Thị B quản lý team AI 10 người.",
    "Dự án Atlas là AI platform do Trần Thị B khởi xướng. Atlas liên quan đến Phoenix qua shared infrastructure.",
])

# Local: factoid
print(rag.local_search("Ai phê duyệt hợp đồng Phoenix?"))
# → Nguyễn Văn A (path: Phoenix —BELONGS_TO→ C-2024 —APPROVED_BY→ Alice)

# Global: sensemaking
print(rag.global_search("Xu hướng AI trong công ty là gì?"))
# → Map-reduce trên community summaries
```

</details>

---

## 6. Retriever Types & Fusion

> **📌 Khái Niệm Cơ Bản:**
> **Retriever** ở đây nghĩa như "cái máy rút" — phần quyết định **lấy cái gì** từ graph/vector để đưa vào LLM. Không phải chỉ có "Local/Global". Trong thực tế có **catalog nhiều loại retriever**, mỗi loại hợp 1 dạng câu hỏi.

### 6.1 Catalog Retriever Types

| Retriever | Cách hoạt động | Ví dụ câu hỏi hợp | Neo4j tương ứng |
|---|---|---|---|
| **VectorRetriever** | Embed câu hỏi → similarity trên entity/LLM text | "Tìm tài liệu nói về X" | KNN vector index |
| **VectorCypherRetriever** | Vector top-k → **traverse thêm neighbors** qua Cypher | "Tài liệu về X liên quan những ai?" | vector + `MATCH` |
| **HybridRetriever** | Vector + full-text → **RRF fuse** | "Từ khoá "Phoenix" hoặc naive-text" | combine indexes |
| **Text2Cypher** | LLM dịch câu hỏi → Cypher → chạy query | "Ai quản lý dự án nhiều nhất?" | LLM-generated Cypher |
| **DRIFT** (Microsoft) | "Drive the search": lấy càng nhanh, càng nhiều hướng | Module đầu vừa bế tắc → rẽ hướng | Agentic traversal |
| **Tools/Agentic retriever** | LLM-agent tự chọn tool (vector/traversal/cypher) | Nhiều kiểu câu trộn lẫn | `ToolsRetriever` |

### 6.2 Text2Cypher (NL → Cypher) Chi Tiết

> **📌 Khái Niệm Cơ Bản:**
> **Text2Cypher** = LLM đóng vai "phiên dịch câu hỏi tiếng người sang Cypher". Khác retrieve thông thường (kéo text về) — ở đây **câu trả lời là câu truy vấn**, chạy xong DB trả kết quả có cấu trúc.
>
> Công thức neo thành công: **Enhanced Schema Injection** — không nhồi toàn bộ schema (tốn token, LLM lẫn), mà chỉ nạp:
> - labels (loại thực thể) + tên attributes
> - vài **parent-child ngữ nghĩa quan trọng** (`(Person)-[:REPORTS_TO]->(Person)`)
>
> ```python
> # Enhanced schema cho Text2Cypher — chỉ nạp phần cần thiết
> def enhanced_schema_snippet() -> str:
>     return """Nodes: Person(name,role), Project(name,budget)
> Edges: Person-WORKS_ON->Project, Person-REPORTS_TO->Person
> Sample: (Alice,REPORTS_TO,Bob) — Bob là quản lý của Alice"""
>
> # Khi query trả rỗng → Text2Cypher tự sửa câu Cypher (Self-correction)
> # Khi schema không đủ → tự hỏi thêm metadata (schema refinement)
> ```

### 6.3 RRF — Hợp Nhất Nhiều Nguồn Không Cần "Điểm"

> **📌 Khái Niệm Cơ Bản:**
> **RRF (Reciprocal Rank Fusion)** = cách gộp nhiều bảng xếp hạng (từ vector, từ graph traversal, từ full-text) mà **không cần chuẩn hoá điểm**. Điểm số mới của mỗi item:
>
> ```
> score = Σ  1 / (k + rank_i)      với k ≈ 60
> ```
>
> Nghĩa gốc: **item càng top trong nhiều danh sách → càng được thưởng nhiều**. Item xếp #1 ở vector (nhận ~1/61) nhưng không xuất hiện ở graph traversal sẽ bị item #8 có mặt ở cả 2 nguồn (nhận ~1/68 + 1/68 > 1/61) vượt qua.
>
> **Analogies:** Giống bình chọn "vòng trong": ai được đề cử ở nhiều bảng khác nhau mới vào chung kết — kể cả không ai cho họ đứng nhất. RRF là kỹ thuật trong bài toán **hybrid retrieval** — kết hợp kết quả graph traversal + vector similarity.

```python
import numpy as np

def rrf_score(ranked_lists: list[list[str]], k: int = 60) -> dict[str, float]:
    """Fuse nhiều danh sách rank → điểm RRF, không cần score chuẩn."""
    fused: dict[str, float] = {}
    for lst in ranked_lists:
        for rank, item in enumerate(lst, start=1):
            fused[item] = fused.get(item, 0.0) + 1.0 / (k + rank)
    return dict(sorted(fused.items(), key=lambda x: -x[1]))

# vector_rank, graph_rank, fulltext_rank = ...  (3 danh sách top-k)
# final = rrf_score([vector_rank, graph_rank, fulltext_rank])
```

---

## 7. GraphRAG Variants (SOTA)

> **📌 Khái Niệm Cơ Bản:**
> **GraphRAG không chỉ là "1 công thức"** — từ GraphRAG gốc của Microsoft (index + các biến thể nối tiếp trước) tới 2025-2026 đã có nhiều hướng tối ưu khác nhau cho các bài toán khác nhau. Bảng dưới đây là **bản đồ những biến thể được nhắc nhiều nhất**:

| Variant | Ý tưởng cốt lõi | Mạnh khi | Yếu/giới hạn |
|---|---|---|---|
| **GraphRAG (MSFT)** | Index + Leiden communities + LLM summary | Global/sensemaking, multi-doc | Đắt (index tốn token), chậm |
| **LightRAG** | Dual-level index (low/high); retrieval theo query; 10x nhanh GraphRAG, 1/3-1/4 cost | Bao phủ retrieval, cost nhỏ | Không làm tốt aggregation global như gốc |
| **HippoRAG (v2)** | Personalized PageRank trên KG + pairwise lai | Multi-hop, trả lời với **ít token** (20x rẻ hơn) | Phụ thuộc KG chất lượng |
| **KAG** | KG-augmented generation, semantic reasoning | Cần lý giải, trả lời logic | Cấu hình phức tạp |
| **DRIFT (MSFT)** | "Drive the search": lấy vô đủ hướng exploration | Truy vấn phức tạp, cần multi-direction | Vòng lặp agent phức tạp |
| **GRAG** | Divide-and-conquer subgraph truy xuất | Giảm nhiễu khi graph to | Cần pipeline phức tạp |

> **Đúc kết chọn variant:**
> - Cần **nhanh + giá rẻ + bao phủ**: `LightRAG`
> - Trả lời **multi-hop với ít token**: `HippoRAG2`
> - **Global/sensemaking trên cả corpus**: `GraphRAG` gốc
> - Truy vấn **phức tạp, phải nghĩ lại**: `DRIFT`
>
> Với framework học tập này, bản thân **hiểu được cơ chế (index + retrieve + community summary)** là quan trọng nhất — variants chỉ là cách tinh chỉnh 3 giai đoạn đó.

---

## 8. Khi Nào Dùng GraphRAG?

```
┌──────────────────────────┬──────────────┬──────────────────────────────┐
│ Loại câu hỏi             │ Dùng gì?     │ Ví dụ                        │
├──────────────────────────┼──────────────┼──────────────────────────────┤
│ Factoid (1-hop)          │ Vanilla RAG  │ "Điều 5 của HĐ X nói gì?"    │
│                          │ hoặc Local   │ "Ai quản lý team Y?"         │
│ Multi-hop (2-4 hops)     │ Local GraphRAG│ "Ai duyệt HĐ của dự án X    │
│                          │              │  và người đó báo cáo cho ai?"│
│ Global / Sensemaking     │ Global GraphRAG│ "Chủ đề chính trong 1000  │
│                          │              │  docs này là gì?"            │
│ Aggregation              │ Global       │ "Có bao nhiêu dự án AI       │
│                          │              │  và ai quản lý chúng?"       │
│ Codebase Q&A             │ Local (code │ "Hàm X được gọi ở đâu?"       │
│                          │  graph)     │                              │
└──────────────────────────┴──────────────┴──────────────────────────────┘
```

**Decision flowchart:**

```
Câu hỏi có cần tổng hợp từ NHIỀU documents?
  ├── Không → Local Search (entity → subgraph)
  └── Có → Global Search (community summaries → map-reduce)

Câu hỏi có entities cụ thể?
  ├── Có → Local Search (bắt đầu từ entities đó)
  └── Không → Global Search (không có anchor để traverse)
```

> **⚠️ Khi Nào ĐỪNG Dùng GraphRAG (bằng chứng benchmark 2025-2026):**
>
> Nghiên cứu so sánh có hệ thống (RAG vs GraphRAG) cho thấy **GraphRAG không phải lúc nào cũng thắng**:
> 1. **Single-hop / factoid**: vanilla RAG **thắng** GraphRAG trên các câu hỏi hỏi "một sự thật đơn lẻ" (vd NQ) — vì graph retrieval có thêm chi phí traversal không cần thiết.
> 2. **Global community search dễ hallucinate**: summary của cộng đồng có thể **thiếu context cụ thể** → LLM "bịa" khi được hỏi chi tiết từ summary đó.
> 3. **Index cực đắt**: LLM-summarize toàn bộ communities ≈ chi phí index rất cao cho corpus lớn — nếu bạn chỉ có 50 docs nội bộ, đừng build GraphRAG.
>
> **Quyết định thực dụng:**
> - Corpus < 100 docs, câu trả lời chủ yếu factoid → **vanilla RAG đủ dùng**.
> - Cần multi-hop, aggregation, chủ đề xuyên nhiều docs → **GraphRAG**.
> - Đứng giữa: **LightRAG / HippoRAG** (nhẹ hơn, retriever text2cypher rẻ hơn).

---

## 9. Labs Thực Hành

### Lab 1: So Sánh Vanilla RAG vs GraphRAG

1. Chuẩn bị 20 documents về 1 topic (ví dụ: "AI in Healthcare" — tự tạo hoặc scrape)
2. Chạy vanilla RAG (vector top-5) và GraphRAG (local search) trên 10 queries
3. Đánh giá thủ công: câu nào GraphRAG thắng? (global queries sẽ thắng rõ)

### Lab 2: Tuning Community Resolution

1. Thử `resolution` = 0.5, 1.0, 2.0 trong `detect_communities`
2. Quan sát số communities và global search quality
3. Tìm resolution tối ưu cho dataset của bạn

### Lab 3: Xây GraphRAG Cho Codebase

1. Parse 1 repo nhỏ (50 files) → tạo code graph (File → Function → Calls)
2. Hỏi: "Thay đổi hàm X ảnh hưởng đến những file nào?" → local search trên code graph
3. So sánh với `grep` thuần

---

## Tài Liệu Tham Khảo

- Edge et al. — *From Local to Global: A GraphRAG Approach to Query-Focused Summarization* (Microsoft Research, 2024) — https://arxiv.org/abs/2404.16130
- Microsoft GraphRAG — *GitHub* (https://github.com/microsoft/graphrag) — implementation + config
- Neo4j — *Building a Knowledge Graph with LLM* (https://neo4j.com/blog/developer/knowledge-graph-llm/)
- LangChain — *GraphCypherQAChain* (https://python.langchain.com/docs/use_cases/graph/)
- *GraphRAG in Practice: A Survey of Research Gaps* (arXiv:2507.03226) — RRF, retrieval & indexing at scale
- Neo4j graphrag-python — *Retriever types: Vector, VectorCypher, Hybrid, Text2Cypher, DRIFT* (https://neo4j.com/docs/graphrag-python/current/)
- *RAG vs GraphRAG: A Systematic Evaluation* — multi-hop thắng, single-hop thua vanilla RAG (arXiv 2025)
- LightRAG / HippoRAG2 — *Giảm chi phí graph retrieval* (https://github.com/HKUDS/LightRAG)

---

*Tiếp theo: [06 — Graph Reasoning](../06-graph-reasoning/)*
