-- Wrong: every run creates a new node
CREATE (e:Entity {name: $name}) SET e += $props
-- Right: match-or-create, then update in place
MERGE (e:Entity {name: $name}) SET e += $props, e.source_doc = $doc_id
