from datetime import datetime, date

# Edges with validity periods
temporal_edges = [
    {"from": "Alice", "to": "TeamA", "type": "MANAGES", 
     "valid_from": date(2023, 1, 1), "valid_until": date(2024, 6, 30)},
    {"from": "Alice", "to": "TeamB", "type": "MANAGES",
     "valid_from": date(2024, 7, 1), "valid_until": None},  # current
    {"from": "Bob", "to": "Phoenix", "type": "WORKS_ON",
     "valid_from": date(2024, 1, 1), "valid_until": date(2024, 12, 31)},
]

def query_at_time(edges: list, query_date: date, node: str) -> list:
    """Query the graph at a specific moment."""
    active = []
    for e in edges:
        valid_from = e["valid_from"]
        valid_until = e.get("valid_until") or date(9999, 12, 31)
        if valid_from <= query_date <= valid_until:
            if e["from"] == node or e["to"] == node:
                active.append(e)
    return active

# Question: which team did Alice manage on 2024-03-01?
print(query_at_time(temporal_edges, date(2024, 3, 1), "Alice"))
# → TeamA

# Question: which team did Alice manage on 2024-08-01?
print(query_at_time(temporal_edges, date(2024, 8, 1), "Alice"))
# → TeamB

# Equivalent Cypher:
# MATCH (a:Person {name: 'Alice'})-[r:MANAGES]->(team)
# WHERE r.valid_from <= date('2024-03-01') <= r.valid_until
# RETURN team
