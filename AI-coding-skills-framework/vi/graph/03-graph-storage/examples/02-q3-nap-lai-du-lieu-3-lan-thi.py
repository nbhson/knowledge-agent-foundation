query = """
UNWIND $batch AS row
MERGE (n:Entity {name: row.name})
SET n.type = row.type, n.updated_at = datetime()
"""
for i in range(0, len(entities), 500):              # lô 500 dòng
    session.execute_write(lambda tx: tx.run(query, batch=entities[i:i+500]))
