def choose_graph_db(requirements: dict) -> str:
    """
    Choose a DB based on requirements.
    
    requirements = {
        "scale": "small" | "medium" | "large" | "trillion",
        "deployment": "local" | "self-hosted" | "managed",
        "latency": "realtime" | "interactive" | "batch",
        "team_size": int,
    }
    """
    if requirements["scale"] == "small" and requirements["deployment"] == "local":
        return "Kuzu (embedded, zero-ops) or NetworkX (prototyping)"
    
    if requirements["scale"] in ["large", "trillion"]:
        return "NebulaGraph or Neo4j Enterprise Cluster"
    
    if requirements["latency"] == "realtime":
        return "FalkorDB or Memgraph (in-memory)"
    
    if requirements["deployment"] == "managed":
        return "Neo4j Aura or Amazon Neptune"
    
    # Default: production balanced
    return "Neo4j Community (self-hosted) — recommended for most projects"
