// Xem query plan
PROFILE MATCH (a:Person {name: 'Alice'})-[:MANAGES*1..3]->(b:Person) RETURN b

// Output cho biết: có dùng index không, số db hits, memory
