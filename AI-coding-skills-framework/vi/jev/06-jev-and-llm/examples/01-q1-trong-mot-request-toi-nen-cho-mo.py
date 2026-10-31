d = jev.ask(state=ticket_text, questions={
    "team":   {"type": "choice", "choices": ["billing", "tech", "account"]},
    "refund": {"type": "noul", "description": "Khách có yêu cầu hoàn tiền không?"}})
draft = llm.write(ticket_text, team=d["team"], refund_p=d["refund"].p)
