CREATE INDEX person_name FOR (n:Person) ON (n.name);
CREATE CONSTRAINT person_unique FOR (n:Person) REQUIRE n.name IS UNIQUE;
MATCH (a:Person {name:'Alice'})-[:MANAGES*1..3]->(b:Person)
RETURN b.name LIMIT 100
