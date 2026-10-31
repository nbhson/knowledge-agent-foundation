resp = client.ask(model="jev-1.13.0", state=ticket_text, questions={
    "team": {"type": "choice", "choices": ["billing", "tech", "account", "other"]},
    "urgency": {"type": "score", "levels": [
        {"level": 1, "label": "p0"}, {"level": 2, "label": "p1"},
        {"level": 3, "label": "p2"}, {"level": 4, "label": "p3"}]},
    "refund": {"type": "noul", "description": "Khách có yêu cầu hoàn tiền không?"},
})
