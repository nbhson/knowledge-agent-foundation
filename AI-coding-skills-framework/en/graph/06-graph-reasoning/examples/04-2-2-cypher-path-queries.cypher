// Shortest path
MATCH (a:Person {name: 'Alice'}), (b:Project {name: 'Atlas'})
MATCH path = shortestPath((a)-[*]-(b))
RETURN path, length(path)

// All paths with a constraint
MATCH (a:Person {name: 'Alice'}), (b:Project {name: 'Atlas'})
MATCH path = (a)-[:MANAGES|WORKS_ON*1..4]->(b)
WHERE all(r in relationships(path) WHERE r.confidence > 0.7)
RETURN path, length(path)
ORDER BY length(path)
LIMIT 5

// Weighted path (using GDS)
// CALL gds.graph.project('myGraph', '*', '*', {relationshipProperties: 'weight'})
// CALL gds.shortestPath.dijkstra.stream('myGraph', {sourceNode: id(a), targetNode: id(b)})
