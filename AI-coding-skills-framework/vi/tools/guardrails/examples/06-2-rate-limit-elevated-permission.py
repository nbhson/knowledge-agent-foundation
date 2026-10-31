registry.register(ToolDefinition(
    name="execute_python",
    category="computation",
    requires_permission="elevated",   # cần người xác nhận
    rate_limit_per_minute=10,          # chặn spam
    timeout_seconds=30,
    max_retries=1,
))
