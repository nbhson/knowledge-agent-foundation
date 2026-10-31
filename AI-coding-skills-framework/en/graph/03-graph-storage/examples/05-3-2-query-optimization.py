# ❌ Slow: no index, full scan
# MATCH (n:Person) WHERE n.name = 'Alice' RETURN n

# ✅ Fast: uses the index
# CREATE INDEX FOR (n:Person) ON (n.name)  -- create once
# MATCH (n:Person {name: 'Alice'}) RETURN n  -- automatically uses the index

# ❌ Slow: unlimited hops, explosion
# MATCH (a)-[*]->(b) RETURN a, b

# ✅ Fast: cap hops + limit
# MATCH (a:Person)-[:MANAGES*1..3]->(b:Person) RETURN a, b LIMIT 100

# ❌ Slow: returns the entire graph
# MATCH (n) RETURN n

# ✅ Fast: take only what you need
# MATCH (p:Person {name: 'Alice'})-[:WORKS_ON]->(proj) RETURN proj.name
