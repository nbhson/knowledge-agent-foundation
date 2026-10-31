registry.register(ToolDefinition(
    name="vector_search",
    description="Semantic search in the vector database",
    parameters={
        "query": {"type": "string", "required": True},
        "top_k": {"type": "integer", "default": 5},
        "collection": {"type": "string"},
        "filters": {"type": "object"},
    },
    category="search",
    tags=["semantic", "vector", "embedding"],
))
