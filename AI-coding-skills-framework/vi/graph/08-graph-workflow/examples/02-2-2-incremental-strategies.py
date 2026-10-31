from typing import List, Dict, Optional
from datetime import datetime

class IncrementalUpdater:
    """
    Cập nhật KG theo incremental — không rebuild.
    
    Strategies:
      - ADD: thêm entities/relations mới
      - UPSERT: tạo nếu chưa có, cập nhật nếu có
      - SOFT_DELETE: đánh dấu xóa, không xóa cứng
      - MERGE: gộp duplicate entities
    """
    
    def __init__(self, graph):
        self.graph = graph  # Neo4j driver hoặc NetworkX
    
    def add_document(self, doc_id: str, text: str) -> Dict:
        """Thêm 1 document mới vào KG."""
        print(f"Ingesting doc: {doc_id}")
        
        # 1. Extract chỉ doc mới (không re-extract toàn bộ)
        # entities = extract_entities(text)
        # relations = extract_relations(text, entities)
        entities = [{"name": "NewPerson", "type": "Person"}]  # mock
        relations = []
        
        # 2. Dedup với graph hiện có (không chỉ trong batch)
        # Kiểm tra entity đã tồn tại chưa
        new_entities = []
        for ent in entities:
            exists = self._entity_exists(ent["name"])
            if not exists:
                new_entities.append(ent)
                print(f"  + New entity: {ent['name']}")
            else:
                print(f"  ~ Entity exists: {ent['name']} (updating properties)")
                self._update_entity(ent)
        
        # 3. Upsert vào graph
        for ent in new_entities:
            self._upsert_entity(ent, doc_id)
        for rel in relations:
            self._upsert_relation(rel, doc_id)
        
        return {"new_entities": len(new_entities), "relations": len(relations)}
    
    def merge_entities(self, canonical_name: str, duplicate_names: List[str]):
        """Gộp duplicate entities: chuyển tất cả edges về canonical."""
        print(f"Merging {duplicate_names} → {canonical_name}")
        
        # Cypher cho Neo4j:
        # MATCH (dup:Entity) WHERE dup.name IN $duplicates
        # MATCH (dup)-[r]->(other)
        # MATCH (canonical:Entity {name: $canonical})
        # CREATE (canonical)-[r2:RELATED {type: r.type}]->(other)
        # SET r2 = properties(r)
        # DELETE r
        
        # NetworkX:
        if hasattr(self.graph, 'nodes') and canonical_name in self.graph:
            for dup_name in duplicate_names:
                if dup_name in self.graph:
                    # Chuyển edges
                    for successor in list(self.graph.successors(dup_name)):
                        edata = self.graph.get_edge_data(dup_name, successor)
                        self.graph.add_edge(canonical_name, successor, **edata)
                    for predecessor in list(self.graph.predecessors(dup_name)):
                        edata = self.graph.get_edge_data(predecessor, dup_name)
                        self.graph.add_edge(predecessor, canonical_name, **edata)
                    self.graph.remove_node(dup_name)
                    print(f"  Merged {dup_name} → {canonical_name}")
    
    def delete_document(self, doc_id: str, soft: bool = True):
        """Xóa document: soft delete (đánh dấu) hoặc hard delete."""
        if soft:
            # Đánh dấu entities/relations từ doc này là deleted
            print(f"Soft deleting doc: {doc_id}")
            # Cypher: MATCH (n {source_doc: $doc_id}) SET n.deleted = true
        else:
            print(f"Hard deleting doc: {doc_id}")
            # Cypher: MATCH (n {source_doc: $doc_id}) DETACH DELETE n
    
    def _entity_exists(self, name: str) -> bool:
        if hasattr(self.graph, 'has_node'):
            return self.graph.has_node(name)
        return False  # Neo4j: query check
    
    def _upsert_entity(self, entity: Dict, doc_id: str):
        # Neo4j: MERGE (n:Entity {name: $name}) SET n += $props
        if hasattr(self.graph, 'add_node'):
            self.graph.add_node(entity["name"], **entity, source_doc=doc_id)
    
    def _update_entity(self, entity: Dict):
        if hasattr(self.graph, 'nodes') and entity["name"] in self.graph:
            for k, v in entity.items():
                self.graph.nodes[entity["name"]][k] = v
    
    def _upsert_relation(self, relation: Dict, doc_id: str):
        if hasattr(self.graph, 'add_edge'):
            self.graph.add_edge(relation["source"], relation["target"],
                                type=relation["type"], source_doc=doc_id)

# Usage
import networkx as nx
G = nx.DiGraph()
G.add_node("Alice", type="Person")

updater = IncrementalUpdater(G)
updater.add_document("doc_001", "Bob là engineer làm việc trên Phoenix")
print(f"Graph: {list(G.nodes(data=True))}")
print(f"Edges: {list(G.edges(data=True))}")

# Merge duplicates
G.add_node("Alice Nguyen", type="Person")
G.add_edge("Alice Nguyen", "Phoenix", type="WORKS_ON")
updater.merge_entities("Alice", ["Alice Nguyen"])
print(f"After merge: {list(G.nodes())}")
