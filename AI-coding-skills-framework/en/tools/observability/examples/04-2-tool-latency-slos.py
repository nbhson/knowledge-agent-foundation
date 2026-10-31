# ToolDefinition metrics (from harness/06)
tool.update_metrics(latency_ms=1200, success=True)  # record on call

# Dashboard alerts:
#   If vector_search.avg_latency_ms > 2000 → alert
#   If execute_python.success_rate < 0.95 → alert
