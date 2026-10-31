import os
import requests

API = "https://api.typesafe.ai/v1/systemone"
HEADERS = {
    "Authorization": f"Bearer {os.environ['TYPESAFE_API_KEY']}",
    "Content-Type": "application/json",
}

STATE = "Ticket #4821: charged twice after plan upgrade — please refund the extra $49."

QUESTIONS = {
    "refund_requested": {
        "type": "noul",
        "question": "Does the customer explicitly ask for money back?",
        "criteria": "Yes only if the text requests a refund or reversal of a charge.",
    },
    "chargeback_threat": {
        "type": "noul",
        "question": "Does the customer threaten a chargeback?",
    },
}

resp = requests.post(
    API,
    headers=HEADERS,
    json={"model": "jev-latest", "state": STATE, "questions": QUESTIONS},
    timeout=5,
)
resp.raise_for_status()
answers = resp.json()["answers"]

p_refund = answers["refund_requested"]["noul"]["p_yes"]     # e.g. 0.97
p_charge = answers["chargeback_threat"]["noul"]["p_yes"]    # e.g. 0.61

# Intrinsic confidence — no separate field for Noul:
conf = lambda p: abs(p - 0.5) * 2
print(conf(p_refund))   # 0.94  → auto-act (high band)
print(conf(p_charge))   # 0.22  → confirm / more context (mid band)

if p_refund > 0.5 and conf(p_refund) >= 0.8:
    open_refund_workflow(ticket)
elif p_refund > 0.5:
    queue_for_agent_review(ticket)   # right call, thin margin → confirm
else:
    reply_with_clarifying_question(ticket)
