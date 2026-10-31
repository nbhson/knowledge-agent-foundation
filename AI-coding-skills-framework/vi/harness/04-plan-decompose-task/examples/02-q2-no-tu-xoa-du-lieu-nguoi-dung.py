if risk in ("high", "irreversible") and not approved(plan, sub, inputs):
    return {"status": "blocked", "reason": "approval-denied"}  # → replan
# timeout không có phản hồi = deny, không phải approve
