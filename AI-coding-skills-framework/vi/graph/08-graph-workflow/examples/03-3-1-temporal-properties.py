from datetime import date

# Mỗi edge có lifecycle
temporal_edge = {
    "from": "Alice",
    "to": "TeamA",
    "type": "MANAGES",
    "valid_from": date(2023, 1, 1),
    "valid_until": date(2024, 6, 30),  # None = vẫn active
    "created_at": datetime.now(),
    "created_by": "ingest:doc_123",
}

# Query tại thời điểm cụ thể
def query_at(graph_edges: List[Dict], query_date: date) -> List[Dict]:
    active = []
    for e in graph_edges:
        vf = e["valid_from"]
        vu = e.get("valid_until") or date(9999, 12, 31)
        if vf <= query_date <= vu:
            active.append(e)
    return active
