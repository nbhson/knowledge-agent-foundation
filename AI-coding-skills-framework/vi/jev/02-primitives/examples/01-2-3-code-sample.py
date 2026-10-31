import typesafe

client = typesafe.Client(api_key="...")

state = """
Ticket #4821: "I was charged twice for my Pro plan this month,
please refund the duplicate charge."
"""

resp = client.ask(
    model="jev-latest",
    state=state,
    questions={
        "team": {
            "type": "choice",
            "choices": ["billing", "tech", "account", "other"],
            "description": "Which team owns this ticket?",
        },
        "channel": {
            "type": "choice",
            "choices": ["self_serve", "human_agent", "callback"],
            "description": "Best resolution channel?",
        },
    },
)

team = resp.answers["team"]
print(team.choice)        # "billing"
print(team.confidence)    # 0.91  (distribution tập trung)
print(team.probabilities) # {"billing": 0.91, "tech": 0.05, ...}

# Dùng full distribution để route 2 nhánh nếu muốn:
p = team.probabilities
if p["billing"] > 0.6:
    route_billing_agent()
elif p["other"] > 0.3:
    escalate_human()      # other cao → taxonomy có vấn đề
else:
    route_generic_queue()
