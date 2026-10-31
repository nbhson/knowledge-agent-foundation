from collections import defaultdict


def calibration_report(pairs: list[tuple[float, bool]], buckets: int = 10) -> dict:
    """
    pairs = [(predicted_probability_of_selected, was_correct), ...]
    Trả về bảng calibration + ECE.
    """
    bucketed: dict[int, list[bool]] = defaultdict(list)
    for p, correct in pairs:
        b = min(int(p * buckets), buckets - 1)
        bucketed[b].append(correct)

    rows, ece = [], 0.0
    total = sum(len(v) for v in bucketed.values()) or 1
    for b in sorted(bucketed):
        ps = [(b + 0.5) / buckets] * len(bucketed[b])
        p_avg = sum(ps) / len(ps)
        acc = sum(bucketed[b]) / len(bucketed[b])
        n = len(bucketed[b])
        ece += (n / total) * abs(p_avg - acc)
        rows.append({"bucket": f"{b}/{buckets}", "mean_p": round(p_avg, 3),
                     "accuracy": round(acc, 3), "n": n})
    return {"rows": rows, "ece": round(ece, 4)}


def per_class_accuracy(results: list[dict]) -> dict:
    """results = [{gold, pred}, ...] → accuracy từng class."""
    stats = defaultdict(lambda: {"correct": 0, "total": 0})
    for r in results:
        stats[r["gold"]]["total"] += 1
        if r["gold"] == r["pred"]:
            stats[r["gold"]]["correct"] += 1
    return {
        k: {"accuracy": round(v["correct"] / max(v["total"], 1), 3),
            "n": v["total"]}
        for k, v in stats.items()
    }
