import requests

API = "https://api.typesafe.ai/v1/systemone"
HEADERS = {
    "Authorization": "Bearer <YOUR_KEY>",
    "Content-Type": "application/json",
}

def decide(model: str, state, questions: dict) -> dict:
    resp = requests.post(
        API,
        headers=HEADERS,
        json={"model": model, "state": state, "questions": questions},
        timeout=5,
    )
    resp.raise_for_status()
    return resp.json()

def read_distribution(answer: dict) -> dict:
    """
    Trích xuất phân phối đầy đủ từ một Choice answer.
    answer chứa: selected + full distribution (probabilities trên options).
    """
    probs = answer.get("probabilities", {})
    ranked = sorted(probs.items(), key=lambda kv: kv[1], reverse=True)
    top, second = ranked[0], ranked[1] if len(ranked) > 1 else (None, 0.0)
    margin = (top[1] - second[1]) if second[0] is not None else top[1]
    return {
        "selected": top[0],
        "top_p": top[1],
        "margin": margin,
        "flat": margin < 0.15,          # gần hòa → escalate
        "full": dict(ranked),
    }

result = decide(
    model="jev-1.13.0",
    state="Khách hàng phản ánh bị trừ tiền 2 lần cho cùng một đơn hàng #4821.",
    questions={
        "ticket_type": {
            "type": "choice",
            "options": ["billing_issue", "refund_request", "general", "account_access"],
        }
    },
)

analysis = read_distribution(result["answers"]["ticket_type"])
print(analysis)
# {'selected': 'billing_issue', 'top_p': 0.86, 'margin': 0.78,
#  'flat': False, 'full': {...}}

if analysis["flat"]:
    escalate_to_human(analysis)          # phân phối flat → đừng auto-act
else:
    route_ticket(analysis["selected"])   # peaked → hành động được
