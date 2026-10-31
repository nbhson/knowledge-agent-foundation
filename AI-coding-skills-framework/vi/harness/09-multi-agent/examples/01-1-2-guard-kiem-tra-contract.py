def is_real_subagent(spec: dict) -> tuple[bool, str]:
    for f in ("role", "goal", "context", "tools", "budget", "lease"):
        if f not in spec:
            return False, f"thiếu trường: {f}"
    if not spec["context"].get("files") and not spec["context"].get("parentSummary"):
        return False, "context phải là files[] + parentSummary cắt gọn, không dump full"
    if spec["role"] in ("implementer",) and not spec.get("worktree"):
        return False, "implementer bắt buộc worktree cách ly"
    lease = spec["lease"]
    if not (lease.get("leaseId") and lease.get("deadlineMs") and lease.get("maxAttempts")):
        return False, "lease cần leaseId + deadlineMs + maxAttempts"
    return True, "ok"
