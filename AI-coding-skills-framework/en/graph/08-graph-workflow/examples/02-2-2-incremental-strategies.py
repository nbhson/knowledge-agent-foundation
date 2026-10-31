from typing import List, Dict, Optional
from datetime import datetime

class IncrementalUpdater:
    """
    Update the KG incrementally — no rebuild.
    
    Strategies:
      - ADD: add new entities/relations
      - UPSERT: create if missing, update if present
      - SOFT_DELETE: mark as deleted, no hard delete
      - MERGE: combine duplicate entities
    """
    
    def __init__(self, graph):
        self.graph = graph  # Neo4j driver or NetworkX
    
    def add_document(self, doc_id: str, text: str) -> Dict:
        """Add 1 new document to the KG."""
        print(f"Ingesting doc: {doc_id}")
        
        # 1. Extract only the new doc (don't re-extract everything)
        # entities = extract_entities(text)
        # relations = extract_relations(text, entities)
        entities = [{"name": "NewPerson", "type": "Person"}]  # mock
        relations = []
        
        # 2. Dedup against the existing graph (not just within the batch)
        # Check whether the entity already exists
        new_entities = []
        for ent in entities:
            exists = self._entity_exists(ent["name"])
            if not exists:
                new_entities.append(ent)
                print(f"  + New entity: {ent['name']}")
            else:
                print(f"  ~ Entity exists: {ent['name']} (updating properties)")
                self._update_entity(ent)
        
        # 3. Upsert into the graph
        for ent in new_entities:
            self._upsert_entity(ent, doc_id)
        for rel in relations:
            self._upsert_relation(rel, doc_id)
        
        return {"new_entities": len(new_entities), "relations": len(relations)}
    
    def merge_entities(self, canonical_name: str, duplicate_names: List[str]):
        """Merge duplicate entities: move all edges to the canonical one."""
        print(f"Merging {duplicate_names} → {canonical_name}")
        
        # Cypher for Neo4j:
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
                    # Move the edges
                    for successor in list(self.graph.successors(dup_name)):
                        edata = self.graph.get_edge_data(dup_name, successor)
                        self.graph.add_edge(canonical_name, successor, **edata)
                    for predecessor in list(self.graph.predecessors(dup_name)):
                        edata = self.graph.get_edge_data(predecessor, dup_name)
                        self.graph.add_edge(predecessor, canonical_name, **edata)
                    self.graph.remove_node(dup_name)
                    print(f"  Merged {dup_name} → {canonical_name}")
    
    def delete_document(self, doc_id: str, soft: bool = True):
        """Delete a document: soft delete (mark) or hard delete."""
        if soft:
            # Mark entities/relations from this doc as deleted
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
updater.add_document("doc_001", "Bob is an engineer working on Phoenix")
print(f"Graph: {list(G.nodes(data=True))}")
print(f"Edges: {list(G.edges(data=True))}")

# Merge duplicates
G.add_node("Alice Nguyen", type="Person")
G.add_edge("Alice Nguyen", "Phoenix", type="WORKS_ON")
updater.merge_entities("Alice", ["Alice Nguyen"])
print(f"After merge: {list(G.nodes())}")
