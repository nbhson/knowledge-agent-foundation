MERGE (n:Person {name: $name})
SET n.role = $role, n.updated_at = datetime()
# removals keep history instead of vanishing:
SET n.deleted = true, n.deleted_at = datetime()
