// Tạo full-text index
CREATE FULLTEXT INDEX personNameFTS FOR (n:Person) ON EACH [n.name]

// Full-text search
CALL db.index.fulltext.queryNodes("personNameFTS", "Alice") YIELD node, score
RETURN node.name, score

// Tạo vector index (Neo4j 5+)
CREATE VECTOR INDEX personEmbedding FOR (n:Person) ON n.embedding
OPTIONS {dimension: 768, similarityFunction: 'cosine'}

// Vector search
CALL db.index.vector.queryNodes("personEmbedding", 5, $queryVector) YIELD node, score
RETURN node.name, score

// HYBRID: Vector search + Graph traversal
CALL db.index.vector.queryNodes("personEmbedding", 10, $queryVector) YIELD node, score
MATCH (node)-[:WORKS_ON]->(project:Project)
RETURN node.name, project.name, score
ORDER BY score DESC
