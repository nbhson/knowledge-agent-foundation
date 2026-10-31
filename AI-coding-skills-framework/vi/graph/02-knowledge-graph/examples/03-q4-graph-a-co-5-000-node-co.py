def upsert_entity(self, e):
    self.graph.run("MERGE (n:Person {name:$name}) "
                   "SET n.role=$role, n.updated_at=datetime()", e)

def soft_delete(self, name):
    self.graph.run("MATCH (n {name:$name}) SET n.deleted=true, "
                   "n.deleted_at=datetime()", {"name": name})
# MERGE chạy lại ba lần vẫn cho đúng một node — đây là điểm mấu chốt
