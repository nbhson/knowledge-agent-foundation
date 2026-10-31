# ToolDefinition metrics (từ harness/06)
tool.update_metrics(latency_ms=1200, success=True)  # ghi nhận khi gọi

# Dashboard alert:
#   Nếu vector_search.avg_latency_ms > 2000 → cảnh báo
#   Nếu execute_python.success_rate < 0.95 → cảnh báo
