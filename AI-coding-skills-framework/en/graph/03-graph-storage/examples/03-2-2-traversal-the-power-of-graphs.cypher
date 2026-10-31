// 1. ONE-HOP: Who works on Phoenix?
MATCH (person:Person)-[:WORKS_ON]->(p:Project {name: 'Phoenix'})
RETURN person.name

// 2. VARIABLE-LENGTH: Find through 1-3 hops of REPORTS_TO/MANAGES
MATCH path = (junior:Person)-[:REPORTS_TO|MANAGES*1..3]->(senior:Person {name: 'Alice'})
RETURN junior.name, length(path) as hops, [n in nodes(path) | n.name] as path

// 3. SHORTEST PATH: Shortest path between two people
MATCH (a:Person {name: 'Bob'}), (b:Person {name: 'Carol'})
MATCH path = shortestPath((a)-[:REPORTS_TO|MANAGES*]-(b))
RETURN path, length(path)

// 4. SUBGRAPH: Grab the whole subgraph around a node (1-hop neighbors)
MATCH (center:Project {name: 'Phoenix'})-[r]-(neighbor)
RETURN center, r, neighbor

// 5. SUBGRAPH 2-HOPS: Expand 2 hops
MATCH (center:Project {name: 'Phoenix'})-[r1]-(n1)-[r2]-(n2)
RETURN center, r1, n1, r2, n2
LIMIT 50

// 6. AGGREGATION: Count how many projects each person works on
MATCH (person:Person)-[:WORKS_ON]->(project:Project)
RETURN person.name, count(project) as project_count
ORDER BY project_count DESC

// 7. FILTER ON THE PATH: Only take paths with high confidence
MATCH path = (a:Person)-[r:WORKS_ON*1..2]->(p:Project)
WHERE all(rel in relationships(path) WHERE rel.confidence > 0.8)
RETURN path
