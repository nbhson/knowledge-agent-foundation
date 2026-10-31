// ============ CREATE ============

// Create nodes
CREATE (a:Person {name: 'Alice', role: 'CTO', age: 35})
CREATE (b:Person {name: 'Bob', role: 'Engineer'})
CREATE (p:Project {name: 'Phoenix', budget: 500000})

// Create edges
MATCH (a:Person {name: 'Alice'}), (b:Person {name: 'Bob'})
CREATE (a)-[:MANAGES {since: '2024-01-01'}]->(b)

MATCH (b:Person {name: 'Bob'}), (p:Project {name: 'Phoenix'})
CREATE (b)-[:WORKS_ON {role: 'Lead', allocation: 0.8}]->(p)

// ============ READ ============

// Find all Persons
MATCH (n:Person) RETURN n.name, n.role

// Find with a filter
MATCH (p:Project) WHERE p.budget > 300000 RETURN p

// ============ UPDATE ============

// Update a property
MATCH (p:Person {name: 'Bob'}) SET p.role = 'Senior Engineer' RETURN p

// Add a label
MATCH (n {name: 'Phoenix'}) SET n:ActiveProject RETURN n

// ============ DELETE ============

// Delete an edge
MATCH (a:Person {name: 'Alice'})-[r:MANAGES]->(b:Person {name: 'Bob'}) DELETE r

// Delete a node (edges must be deleted first)
MATCH (n:Person {name: 'Bob'}) DETACH DELETE n

// Soft delete (recommended for KGs)
MATCH (n:Person {name: 'Bob'}) SET n.deleted = true, n.deleted_at = datetime()
