// View the query plan
PROFILE MATCH (a:Person {name: 'Alice'})-[:MANAGES*1..3]->(b:Person) RETURN b

// The output shows: whether an index was used, db hits, memory
