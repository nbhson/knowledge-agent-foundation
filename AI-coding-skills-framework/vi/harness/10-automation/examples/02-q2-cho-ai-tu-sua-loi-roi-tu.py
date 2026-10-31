def decide(baseline: dict, canary: dict) -> str:
    if canary["smoke_failures"] > 0 or canary["sev1_firing"]:
        return "ROLLBACK: smoke/sev1"
    if canary["error_rate"] > 0.02:
        return "ROLLBACK: error_rate"
    return "PROMOTE"
