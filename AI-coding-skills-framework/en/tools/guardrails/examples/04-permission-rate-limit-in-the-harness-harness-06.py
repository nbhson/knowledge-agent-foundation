@dataclass
class ToolDefinition:
    requires_permission: str = "standard"  # standard, elevated, admin
    rate_limit_per_minute: int = 60
    timeout_seconds: int = 30
    max_retries: int = 3

# Guardrails check before executing:
def guardrail_check(tool: ToolDefinition, params: Dict) -> bool:
    if tool.requires_permission == "elevated":
        approve = human_approve(params)     # human confirmation required
        if not approve: return False
    if exceeded_rate_limit(tool): return False  # rate limited

> 🔑 **Policy / Permission highlight:** this guardrail is the **pre-execution policy checkpoint** — `requires_permission` (standard / elevated / admin) maps to `06` §8 RBAC, and `elevated` escalates to `15-approval-gates` for human confirm. Rate limit is the companion abuse policy.
    return True
