// 1. ONE-HOP: Ai làm việc trên Phoenix?
MATCH (person:Person)-[:WORKS_ON]->(p:Project {name: 'Phoenix'})
RETURN person.name

// 2. VARIABLE-LENGTH: Tìm qua 1-3 hops REPORTS_TO/MANAGES
MATCH path = (junior:Person)-[:REPORTS_TO|MANAGES*1..3]->(senior:Person {name: 'Alice'})
RETURN junior.name, length(path) as hops, [n in nodes(path) | n.name] as path

// 3. SHORTEST PATH: Đường ngắn nhất giữa 2 người
MATCH (a:Person {name: 'Bob'}), (b:Person {name: 'Carol'})
MATCH path = shortestPath((a)-[:REPORTS_TO|MANAGES*]-(b))
RETURN path, length(path)

// 4. SUBGRAPH: Lấy toàn bộ subgraph quanh 1 node (1-hop neighbors)
MATCH (center:Project {name: 'Phoenix'})-[r]-(neighbor)
RETURN center, r, neighbor

// 5. SUBGRAPH 2-HOPS: Mở rộng 2 hops
MATCH (center:Project {name: 'Phoenix'})-[r1]-(n1)-[r2]-(n2)
RETURN center, r1, n1, r2, n2
LIMIT 50

// 6. AGGREGATION: Đếm số projects mỗi person tham gia
MATCH (person:Person)-[:WORKS_ON]->(project:Project)
RETURN person.name, count(project) as project_count
ORDER BY project_count DESC

// 7. FILTER TRÊN PATH: Chỉ lấy path có confidence cao
MATCH path = (a:Person)-[r:WORKS_ON*1..2]->(p:Project)
WHERE all(rel in relationships(path) WHERE rel.confidence > 0.8)
RETURN path
