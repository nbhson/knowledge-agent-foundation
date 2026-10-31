# Instead of deleting old edges, mark them expired and create new ones
def update_temporal_edge(edges: list, from_node: str, to_node: str, 
                          edge_type: str, new_valid_from: date):
    """Update a temporal edge: expire the old one, create a new one."""
    for e in edges:
        if e["from"] == from_node and e["to"] == to_node and e["type"] == edge_type:
            if e.get("valid_until") is None:  # currently active
                e["valid_until"] = new_valid_from  # expire it
    
    edges.append({
        "from": from_node, "to": to_node, "type": edge_type,
        "valid_from": new_valid_from, "valid_until": None,
    })
    return edges
