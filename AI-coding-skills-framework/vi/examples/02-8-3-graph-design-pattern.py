# Complete Graph Engineering Example
from graph_engine import GraphHarness

graph = GraphHarness(
    ontology={
        "node_types": ["Person", "Project", "Document", "Organization"],
        "edge_types": ["APPROVES", "REPORTS_TO", "BELONGS_TO", "REFERENCES"],
        "constraints": ["Person -[REPORTS_TO]-> Person", "Project -[APPROVES]-> Person"]
    },
    storage="neo4j://localhost:7687",
    embeddings={"model": "nomic-embed-text", "dim": 768},
    retrieval={
        "strategy": "hybrid",  # vector + graph traversal
        "max_hops": 3,
        "community_search": True,
    },
    reasoning={
        "path_finding": "shortest_path",
        "community_detection": "leiden",
    },
    evaluation={
        "metrics": ["coverage", "hallucination_rate", "path_precision"]
    }
)
