registry.register(ToolDefinition(
    name="github_search_code",
    source="mcp:github",          # đến từ MCP server
    description="Tìm code trong GitHub repos",
    parameters={"query": {"type": "string", "required": True}},
    category="search",
    requires_permission="standard",  # guardrails áp dụng như tool thường
    rate_limit_per_minute=30,
))
