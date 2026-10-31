registry.register(ToolDefinition(
    name="github_search_code",
    source="mcp:github",          # comes from an MCP server
    description="Search code in GitHub repos",
    parameters={"query": {"type": "string", "required": True}},
    category="search",
    requires_permission="standard",  # guardrails apply just like a normal tool
    rate_limit_per_minute=30,
))
