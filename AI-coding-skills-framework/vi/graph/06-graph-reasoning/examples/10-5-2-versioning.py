# Thay vì xóa edge cũ, đánh dấu hết hạn và tạo edge mới
def update_temporal_edge(edges: list, from_node: str, to_node: str, 
                          edge_type: str, new_valid_from: date):
    """Cập nhật temporal edge: expire cũ, tạo mới."""
    for e in edges:
        if e["from"] == from_node and e["to"] == to_node and e["type"] == edge_type:
            if e.get("valid_until") is None:  # đang active
                e["valid_until"] = new_valid_from  # expire
    
    edges.append({
        "from": from_node, "to": to_node, "type": edge_type,
        "valid_from": new_valid_from, "valid_until": None,
    })
    return edges
