CREATE (a:Person {name:'Alice', role:'CTO'})
CREATE (p:Project {name:'Phoenix', budget:500000})
CREATE (a)-[:MANAGES {since:'2024-01-01', confidence:0.95}]->(p)
MATCH (who:Person)-[:MANAGES|WORKS_ON*1..2]->(proj:Project {name:'Phoenix'})
RETURN who.name, proj.name
