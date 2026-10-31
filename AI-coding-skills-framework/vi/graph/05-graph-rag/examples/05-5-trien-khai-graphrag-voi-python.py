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
