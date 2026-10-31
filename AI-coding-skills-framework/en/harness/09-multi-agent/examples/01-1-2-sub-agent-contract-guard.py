def is_real_subagent(spec: dict) -> tuple[bool, str]:
    for f in ("role", "goal", "context", "tools", "budget", "lease"):
        if f not in spec:
            return False, f"missing field: {f}"
    if not spec["context"].get("files") and not spec["context"].get("parentSummary"):
        return False, "context must be trimmed files[] + parentSummary, never full dump"
    if spec["role"] in ("implementer",) and not spec.get("worktree"):
        return False, "implementer requires isolated worktree"
    lease = spec["lease"]
    if not (lease.get("leaseId") and lease.get("deadlineMs") and lease.get("maxAttempts")):
        return False, "lease requires leaseId + deadlineMs + maxAttempts"
    return True, "ok"
