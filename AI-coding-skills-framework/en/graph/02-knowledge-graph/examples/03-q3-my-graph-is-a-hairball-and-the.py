def validate_edge(self, edge_type, from_label, to_label):
    rule = self.edge_types[edge_type]
    if rule["from"] != from_label or rule["to"] != to_label:
        return False, f"Edge {edge_type} requires {rule['from']} -> {rule['to']}"
    if from_label == to_label and edge_type == "MANAGES":
        return False, "Cannot manage self"
    return True, "OK"
