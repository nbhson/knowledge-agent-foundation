from datetime import date, datetime

# Each edge has a lifecycle
temporal_edge = {
    "from": "Alice",
    "to": "TeamA",
    "type": "MANAGES",
    "valid_from": date(2023, 1, 1),
    "valid_until": date(2024, 6, 30),  # None = still active
    "created_at": datetime.now(),
    "created_by": "ingest:doc_123",
}

# Query at a specific point in time
def query_at(graph_edges: List[Dict], query_date: date) -> List[Dict]:
    active = []
    for e in graph_edges:
        vf = e["valid_from"]
        vu = e.get("valid_until") or date(9999, 12, 31)
        if vf <= query_date <= vu:
            active.append(e)
    return active
