query_at_time(edges, date(2024, 3, 1), "Alice")  # → TeamA
query_at_time(edges, date(2024, 8, 1), "Alice")  # → TeamB
# Cypher: WHERE r.valid_from <= date('2024-03-01') <= r.valid_until
