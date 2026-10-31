@dataclass
class ToolDefinition:
    requires_permission: str = "standard"  # standard, elevated, admin
    rate_limit_per_minute: int = 60
    timeout_seconds: int = 30
    max_retries: int = 3

# Guardrails check trước khi execute:
def guardrail_check(tool: ToolDefinition, params: Dict) -> bool:
    if tool.requires_permission == "elevated":
        approve = human_approve(params)     # cần người xác nhận
        if not approve: return False
    if exceeded_rate_limit(tool): return False  # rate limited

> 🔑 **Highlight Policy / Permission:** guardrail này là **checkpoint policy pre-execution** — `requires_permission` (standard / elevated / admin) ánh xạ sang RBAC ở `06` §8, và `elevated` leo lên `15-approval-gates` để human confirm. Rate limit là policy chống abuse đi kèm.
    return True
