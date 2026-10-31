import os
import requests

API = "https://api.typesafe.ai/v1/systemone"
HEADERS = {
    "Authorization": f"Bearer {os.environ['TYPESAFE_API_KEY']}",
    "Content-Type": "application/json",
}

STATE = (
    "Ticket #4821: Customer was charged twice after upgrading to the Pro plan. "
    "They want the extra charge reversed and are threatening a chargeback."
)

QUESTIONS = {
    "team": {
        "type": "choice",
        "options": ["billing", "infra", "bug", "product", "other"],
        "question": "Which team should own this ticket?",
    }
}


def classify(text: str, questions: dict) -> dict:
    resp = requests.post(
        API,
        headers=HEADERS,
        json={"model": "jev-latest", "state": text, "questions": questions},
        timeout=5,
    )
    resp.raise_for_status()
    return resp.json()["answers"]


answers = classify(STATE, QUESTIONS)
team = answers["team"]["choice"]

print(team["selected"])            # e.g. "billing"
print(team["probabilities"])       # {"billing": 0.91, "infra": 0.02, ...}
print(team["confidence"])          # e.g. 0.87  ← a MARGIN, not P(correct)

# Act on the value — and on the confidence band:
if team["confidence"] >= 0.8:
    route(ticket, team["selected"])            # auto-act
elif team["confidence"] >= 0.5:
    route(ticket, team["selected"], confirm=True)  # confirm / more context
else:
    escalate_to_human(ticket)                  # or hand to an LLM
