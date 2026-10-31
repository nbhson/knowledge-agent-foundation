def cost_per_run(events: list[TrajectoryEvent]) -> dict[str, dict]:
    """Tổng tokens / latency per run, group theo task type.
    Run vượt p95 của task type × 3 → flag điều tra, đừng đoán."""
    agg: dict[str, dict] = defaultdict(lambda: {"tokens": 0, "latency_ms": 0, "steps": 0})
    for e in events:
        a = agg[e.payload.get("task_type", "unknown")]
        a["tokens"] += e.tokens_in + e.tokens_out
        a["latency_ms"] += e.latency_ms; a["steps"] += 1
    return dict(agg)
