from collections import defaultdict
import httpx

API_URL = "https://api.typesafe.ai/v1/systemone"


def evaluate( labelled: list[dict],
              questions: dict,
              model: str = "jev-latest",
            ) -> dict:
    """labelled = [{"state": ..., "answers": {"q": "billing"}}, ...]"""
    buckets = defaultdict(lambda: [0, 0])          # p_bucket -> [stated, n]
    per_class = defaultdict(lambda: [0, 0])        # class -> [correct, n]
    gate = []                                      # (p, correct)

    for row in labelled:
        r = httpx.post(
            API_URL,
            headers={"Authorization": f"Bearer {API_KEY}"},
            json={"model": model, "state": row["state"], "questions": questions},
            timeout=10.0,
        )
        r.raise_for_status()
        res = r.json()["results"]

        for q, gold in row["answers"].items():
            pred = res[q]
            p = pred["probabilities"].get(pred["selected"], 0.0)
            correct = pred["selected"] == gold

            b = round(p, 1)                        # 0.0, 0.1, … 1.0
            buckets[b][0] += int(correct)
            buckets[b][1] += 1

            per_class[gold][0] += int(correct)
            per_class[gold][1] += 1

            gate.append((p, correct))

    calibration = {b: c / n for b, (c, n) in sorted(buckets.items()) if n}
    acc_by_class = {k: c / n for k, (c, n) in per_class.items()}

    # sweep thresholds → pick YOUR operating point
    sweeps = {}
    for tau in [0.5, 0.6, 0.7, 0.8, 0.9]:
        auto = [(p, ok) for p, ok in gate if p >= tau]
        sweeps[tau] = {
            "coverage": len(auto) / len(gate),
            "auto_acc": (sum(ok for _, ok in auto) / len(auto)) if auto else None,
        }

    return {"calibration": calibration,
            "per_class_accuracy": acc_by_class,
            "threshold_sweep": sweeps}
