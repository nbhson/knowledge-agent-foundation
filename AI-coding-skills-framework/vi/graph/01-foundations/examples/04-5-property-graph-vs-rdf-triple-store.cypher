// Tạo nodes + edges với properties
CREATE (a:Person {name: 'Alice', role: 'CTO'})
CREATE (b:Person {name: 'Bob', role: 'Engineer'})
CREATE (p:Project {name: 'Phoenix', budget: 500000})
CREATE (a)-[:MANAGES {since: '2024-01-01'}]->(b)
CREATE (b)-[:WORKS_ON {role: 'Lead'}]->(p)

// Truy vấn: ai quản lý project Phoenix?
MATCH (person:Person)-[:MANAGES*1..2]->(proj:Project {name: 'Phoenix'})
RETURN person.name
