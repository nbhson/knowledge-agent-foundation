def decide(baseline: dict, canary: dict) -> str:
    err_delta = canary["error_rate"] - baseline["error_rate"]
    lat_delta = (canary["p99_ms"] - baseline["p99_ms"]) / max(baseline["p99_ms"], 1)
    if canary["smoke_failures"] > 0 or canary["sev1_firing"]:
        return "ROLLBACK: smoke/sev1"
    if canary["error_rate"] > 0.02 or err_delta > 0.005:
        return f"ROLLBACK: error_rate delta={err_delta:+.3f}"
    return "PROMOTE"
