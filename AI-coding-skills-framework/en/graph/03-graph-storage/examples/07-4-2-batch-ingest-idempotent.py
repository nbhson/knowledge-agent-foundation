from neo4j import GraphDatabase

class GraphIngestor:
    def __init__(self, uri: str, user: str, password: str):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
    
    def ingest_batch(self, entities: list, relations: list, batch_size: int = 1000):
        """Batch ingest — idempotent thanks to MERGE."""
        with self.driver.session() as session:
            # Batch entities
            for i in range(0, len(entities), batch_size):
                batch = entities[i:i + batch_size]
                session.execute_write(self._merge_entities, batch)
                print(f"Ingested entities batch {i//batch_size + 1}: {len(batch)} nodes")
            
            # Batch relations
            for i in range(0, len(relations), batch_size):
                batch = relations[i:i + batch_size]
                session.execute_write(self._merge_relations, batch)
                print(f"Ingested relations batch {i//batch_size + 1}: {len(batch)} edges")
    
    @staticmethod
    def _merge_entities(tx, batch):
        # UNWIND = a loop inside Cypher, more efficient than many calls
        query = """
        UNWIND $batch as row
        MERGE (n:Entity {name: row.name})
        SET n.type = row.type,
            n.description = row.description,
            n.updated_at = datetime()
        """
        tx.run(query, batch=batch)
    
    @staticmethod
    def _merge_relations(tx, batch):
        query = """
        UNWIND $batch as row
        MATCH (a:Entity {name: row.source})
        MATCH (b:Entity {name: row.target})
        MERGE (a)-[r:RELATED {type: row.type}]->(b)
        SET r.confidence = row.confidence,
            r.evidence = row.evidence,
            r.updated_at = datetime()
        """
        tx.run(query, batch=batch)
    
    def close(self):
        self.driver.close()

# Usage
ingestor = GraphIngestor("bolt://localhost:7687", "neo4j", "password")
ingestor.ingest_batch(entities, relations, batch_size=500)
ingestor.close()
