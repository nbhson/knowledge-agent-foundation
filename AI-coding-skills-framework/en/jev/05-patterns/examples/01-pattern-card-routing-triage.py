import httpx

API_URL = "https://api.typesafe.ai/v1/systemone"
TEAMS = ["billing", "infra", "product", "data"]

def triage(ticket: dict) -> dict:
    """One call → queue + priority, evaluated in parallel."""
    r = httpx.post(
        API_URL,
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={
            "model": "jev-latest",
            "state": ticket,          # subject + body snippet + customer tier
            "questions": {
                "queue":   {"type": "choice", "options": TEAMS},
                "priority": {"type": "score",
                             "levels": ["p0", "p1", "p2", "p3"]},
            },
        },
        timeout=5.0,
    )
    r.raise_for_status()
    res = r.json()["results"]

    queue = res["queue"]
    priority = res["priority"]

    return {
        "queue": queue["selected"],
        "queue_p": queue["probabilities"].get(queue["selected"]),
        "priority": priority["selected"],
        "priority_confidence": priority["confidence"],
        "band": "auto" if queue["confidence"] >= 0.7 else "human_review",
    }
