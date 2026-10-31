entities = [{"name": "NewPerson", "type": "Person"}]
new = [e for e in entities if not self._entity_exists(e["name"])]
for ent in new: self._upsert_entity(ent, "doc_001")
# Neo4j: MERGE (n:Entity {name:$name}) SET n += $props
