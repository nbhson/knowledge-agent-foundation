# ❌ Chậm: không dùng index, scan toàn bộ
# MATCH (n:Person) WHERE n.name = 'Alice' RETURN n

# ✅ Nhanh: dùng index
# CREATE INDEX FOR (n:Person) ON (n.name)  -- tạo 1 lần
# MATCH (n:Person {name: 'Alice'}) RETURN n  -- tự động dùng index

# ❌ Chậm: không giới hạn hops, explosion
# MATCH (a)-[*]->(b) RETURN a, b

# ✅ Nhanh: giới hạn hops + limit
# MATCH (a:Person)-[:MANAGES*1..3]->(b:Person) RETURN a, b LIMIT 100

# ❌ Chậm: trả về toàn bộ graph
# MATCH (n) RETURN n

# ✅ Nhanh: chỉ lấy cần thiết
# MATCH (p:Person {name: 'Alice'})-[:WORKS_ON]->(proj) RETURN proj.name
