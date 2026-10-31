CREATE VECTOR INDEX personEmbedding FOR (n:Person) ON n.embedding
OPTIONS {dimension: 768, similarityFunction: 'cosine'}
CALL db.index.vector.queryNodes("personEmbedding", 10, $queryVector) YIELD node, score
MATCH (node)-[:WORKS_ON]->(p:Project) RETURN node.name, p.name, score
