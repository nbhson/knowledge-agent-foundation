resp = client.ask(model="jev-1.13.0", state=ticket_text, questions={
    "team":   {"type": "choice", "choices": ["billing", "tech", "account", "other"]},
    "refund": {"type": "noul", "description": "Khách có yêu cầu hoàn tiền không?"},
})
if resp.answers["refund"].p >= 0.85:
    open_refund_flow()
