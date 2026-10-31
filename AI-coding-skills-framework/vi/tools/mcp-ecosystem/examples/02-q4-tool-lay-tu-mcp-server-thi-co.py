registry.register(ToolDefinition(
    name="github_search_code", source="mcp:github",
    description="Tìm code trong GitHub repos",
    parameters={"query": {"type": "string", "required": True}},
    requires_permission="standard", rate_limit_per_minute=30,
))
