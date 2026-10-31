def choose_graph_db(requirements: dict) -> str:
    """
    Chọn DB dựa trên yêu cầu.
    
    requirements = {
        "scale": "small" | "medium" | "large" | "trillion",
        "deployment": "local" | "self-hosted" | "managed",
        "latency": "realtime" | "interactive" | "batch",
        "team_size": int,
    }
    """
    if requirements["scale"] == "small" and requirements["deployment"] == "local":
        return "Kuzu (embedded, zero-ops) hoặc NetworkX (prototyping)"
    
    if requirements["scale"] in ["large", "trillion"]:
        return "NebulaGraph hoặc Neo4j Enterprise Cluster"
    
    if requirements["latency"] == "realtime":
        return "FalkorDB hoặc Memgraph (in-memory)"
    
    if requirements["deployment"] == "managed":
        return "Neo4j Aura hoặc Amazon Neptune"
    
    # Default: production balanced
    return "Neo4j Community (self-hosted) — khuyến nghị cho hầu hết dự án"
