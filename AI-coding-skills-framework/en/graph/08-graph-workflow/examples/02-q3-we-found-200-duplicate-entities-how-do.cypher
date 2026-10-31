MATCH (dup:Entity) WHERE dup.name IN $duplicates
MATCH (dup)-[r]->(other)
MATCH (c:Entity {name: $canonical})
CREATE (c)-[r2:RELATED {type: r.type}]->(other)
SET r2 = properties(r)
DELETE r
