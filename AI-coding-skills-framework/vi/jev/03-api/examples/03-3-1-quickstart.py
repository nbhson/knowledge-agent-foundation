# pip install typesafe
import os
import typesafe

client = typesafe.Client(api_key=os.environ["TYPESAFE_API_KEY"])

resp = client.ask(
    model="jev-1.13.0",                     # pin version trong production
    state="Ticket: charged twice, want refund, very frustrated.",
    questions={
        "team": {
            "type": "choice",
            "choices": ["billing", "tech", "account", "other"],
            "description": "Which team owns this ticket?",
        },
        "refund_requested": {
            "type": "noul",
            "description": "Does the customer explicitly request a refund?",
        },
        "urgency": {
            "type": "score",
            "levels": [
                {"level": 1, "label": "low"},
                {"level": 2, "label": "medium"},
                {"level": 3, "label": "high"},
                {"level": 4, "label": "critical"},
            ],
            "description": "Urgency of handling this ticket",
        },
    },
)

team = resp.answers["team"]
if team.confidence > 0.7 and team.choice != "other":
    route(team.choice)
else:
    escalate_human(team.probabilities)

refund = resp.answers["refund_requested"]
if refund.p >= 0.85:
    open_refund_flow()
elif abs(refund.p - 0.5) < 0.1:
    ask_human()          # margin nhỏ → Jev gần như không biết

urgency = resp.answers["urgency"]
if urgency.score >= 3.5:
    page_oncall()
