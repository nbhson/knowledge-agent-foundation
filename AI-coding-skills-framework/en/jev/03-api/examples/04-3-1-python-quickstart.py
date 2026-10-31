import os
from typesafe import TypeSafe  # official TypeSafe Python SDK

client = TypeSafe(api_key=os.environ["TYPESAFE_API_KEY"])

result = client.systemone.ask(
    model="jev-latest",
    state="Invoice shows 3 line items; customer says they only ordered 2.",
    questions={
        "discrepancy": {
            "type": "noul",
            "question": "Does the text claim a billing discrepancy?",
            "criteria": "Yes only if the customer states the charge does not match the order.",
        },
        "team": {
            "type": "choice",
            "options": ["billing", "fraud", "support"],
            "question": "Which team owns this?",
        },
    },
)

p_disc = result.answers["discrepancy"].p_yes          # 0.91
team = result.answers["team"].choice.selected          # "billing"
conf = result.answers["team"].choice.confidence        # margin, not P(correct)
