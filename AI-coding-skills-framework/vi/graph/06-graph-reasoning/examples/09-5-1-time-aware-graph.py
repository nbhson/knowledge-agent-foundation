from datetime import datetime, date

# Edge có thời gian hiệu lực
temporal_edges = [
    {"from": "Alice", "to": "TeamA", "type": "MANAGES", 
     "valid_from": date(2023, 1, 1), "valid_until": date(2024, 6, 30)},
    {"from": "Alice", "to": "TeamB", "type": "MANAGES",
     "valid_from": date(2024, 7, 1), "valid_until": None},  # hiện tại
    {"from": "Bob", "to": "Phoenix", "type": "WORKS_ON",
     "valid_from": date(2024, 1, 1), "valid_until": date(2024, 12, 31)},
]

def query_at_time(edges: list, query_date: date, node: str) -> list:
    """Truy vấn graph tại một thời điểm cụ thể."""
    active = []
    for e in edges:
        valid_from = e["valid_from"]
        valid_until = e.get("valid_until") or date(9999, 12, 31)
        if valid_from <= query_date <= valid_until:
            if e["from"] == node or e["to"] == node:
                active.append(e)
    return active

# Hỏi: Alice quản lý team nào vào 2024-03-01?
print(query_at_time(temporal_edges, date(2024, 3, 1), "Alice"))
# → TeamA

# Hỏi: Alice quản lý team nào vào 2024-08-01?
print(query_at_time(temporal_edges, date(2024, 8, 1), "Alice"))
# → TeamB

# Cypher tương đương:
# MATCH (a:Person {name: 'Alice'})-[r:MANAGES]->(team)
# WHERE r.valid_from <= date('2024-03-01') <= r.valid_until
# RETURN team
