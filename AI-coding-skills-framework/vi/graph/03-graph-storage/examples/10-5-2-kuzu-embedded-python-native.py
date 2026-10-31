import kuzu

# Tạo DB in-process (không cần Docker)
db = kuzu.Database("./kuzu_db")
conn = kuzu.Connection(db)

# Tạo schema
conn.execute("CREATE NODE TABLE Person(name STRING, role STRING, PRIMARY KEY(name))")
conn.execute("CREATE NODE TABLE Project(name STRING, budget INT64, PRIMARY KEY(name))")
conn.execute("CREATE REL TABLE WORKS_ON(FROM Person TO Project, role STRING, confidence DOUBLE)")
conn.execute("CREATE REL TABLE MANAGES(FROM Person TO Person, since STRING)")

# Insert
conn.execute('CREATE (a:Person {name: "Alice", role: "CTO"})')
conn.execute('CREATE (a:Person {name: "Bob", role: "Engineer"})')
conn.execute('CREATE (a:Project {name: "Phoenix", budget: 500000})')

# Query
result = conn.execute("""
    MATCH (p:Person)-[r:WORKS_ON]->(proj:Project)
    RETURN p.name, proj.name, r.role
""")
while result.has_next():
    print(result.get_next())

# Hybrid: Kuzu cũng hỗ trợ vector search (extension)
# conn.execute("INSTALL vector; LOAD EXTENSION vector;")
