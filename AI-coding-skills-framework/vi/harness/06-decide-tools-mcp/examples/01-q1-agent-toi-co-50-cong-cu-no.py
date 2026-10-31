registry.register(ToolDefinition(
    name="vector_search",
    description="Tìm kiếm ngữ nghĩa trong cơ sở dữ liệu vector",
    parameters={"query": {"type": "string", "required": True},
                "top_k": {"type": "integer", "default": 5}},
    category="search", tags=["semantic", "vector"],
))
