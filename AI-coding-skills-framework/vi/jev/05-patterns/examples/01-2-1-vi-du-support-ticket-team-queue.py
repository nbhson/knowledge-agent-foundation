import requests

API = "https://api.typesafe.ai/v1/systemone"
HEADERS = {"Authorization": "Bearer <KEY>", "Content-Type": "application/json"}

QUEUES = ["billing", "tech_support", "sales", "churn_risk"]
PRIORITY_LEVELS = ["p0", "p1", "p2", "p3"]


def triage_ticket(ticket_text: str) -> dict:
    resp = requests.post(
        API,
        headers=HEADERS,
        json={
            "model": "jev-1.13.0",
            "state": ticket_text,
            "questions": {
                "queue": {"type": "choice", "options": QUEUES},
                "priority": {"type": "score", "levels": PRIORITY_LEVELS},
            },
        },
        timeout=5,
    )
    resp.raise_for_status()
    data = resp.json()
    q = data["answers"]["queue"]
    p = data["answers"]["priority"]

    return {
        "queue": q["selected"],
        "queue_probs": q.get("probabilities", {}),
        "queue_confidence": q.get("confidence", 0.0),
        # Score: probability-weighted score có thể NGỒI GIỮA 2 level
        "priority": p.get("score", p.get("selected")),
        "priority_confidence": p.get("confidence", 0.0),
        "request_id": data.get("request_id"),
    }


def route(ticket_text: str) -> None:
    result = triage_ticket(ticket_text)
    if result["queue_confidence"] >= 0.8 and result["priority_confidence"] >= 0.7:
        auto_route(result["queue"], result["priority"])   # HIGH band
    elif result["queue_confidence"] >= 0.5:
        suggest_to_agent(result)                          # MEDIUM band
    else:
        human_triage(ticket_text, result)                 # LOW band
