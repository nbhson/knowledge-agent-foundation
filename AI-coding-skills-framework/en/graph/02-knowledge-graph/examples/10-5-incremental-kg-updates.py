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
