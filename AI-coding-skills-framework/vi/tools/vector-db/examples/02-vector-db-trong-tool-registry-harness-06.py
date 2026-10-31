registry.register(ToolDefinition(
    name="vector_search",
    description="Tìm kiếm ngữ nghĩa trong cơ sở dữ liệu vector",
    parameters={
        "query": {"type": "string", "required": True},
        "top_k": {"type": "integer", "default": 5},
        "collection": {"type": "string"},
        "filters": {"type": "object"},
    },
    category="search",
    tags=["semantic", "vector", "embedding"],
))
