# Directed: relationships have direction
# REPORTS_TO: Alice reports to Bob ≠ Bob reports to Alice
G_directed = nx.DiGraph()
G_directed.add_edge("Alice", "Bob", relation="REPORTS_TO")

# Weighted: different levels of confidence
# KNOWS with confidence from extraction
G_weighted = nx.Graph()
G_weighted.add_edge("Alice", "Bob", weight=0.92, source="email_123")

# Temporal: relationships change over time
# Alice WORKS_AT Company X from 2020, moved to Y in 2024
G_temporal_data = {
    "nodes": ["Alice", "CompanyX", "CompanyY"],
    "edges": [
        {"from": "Alice", "to": "CompanyX", "type": "WORKS_AT", "valid": "[2020, 2024)"},
        {"from": "Alice", "to": "CompanyY", "type": "WORKS_AT", "valid": "[2024, now)"},
    ]
}

# Heterogeneous: many types
# Codebase graph: File, Function, Class are different node types
hetero_schema = {
    "node_types": ["File", "Function", "Class", "Test"],
    "edge_types": ["DEFINES", "CALLS", "INHERITS", "TESTED_BY"]
}
