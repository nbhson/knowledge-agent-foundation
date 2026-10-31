registry.register(ToolDefinition(
    name="execute_python",
    requires_permission="elevated",  # human confirmation required
    rate_limit_per_minute=10,         # block spam
    timeout_seconds=30,
    max_retries=1,
))
