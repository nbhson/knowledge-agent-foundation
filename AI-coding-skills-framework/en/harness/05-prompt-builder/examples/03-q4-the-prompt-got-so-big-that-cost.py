TIERS = [("fast", 4000, 8000), ("balanced", 12000, 20000), ("max", 32000, 60000)]
def select_tier(needed, deadline_ms):
    for name, tok, ms in TIERS:
        if needed <= tok and deadline_ms <= ms: return name
    raise ValueError(f"needs {needed}tok/{deadline_ms}ms: exceeds all tiers; compact first")
