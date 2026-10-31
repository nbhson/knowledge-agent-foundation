q = decide(state=ticket_text, questions={"queue":    {"type": "choice"},
                                         "priority": {"type": "score"}})
if q["queue_confidence"] >= 0.8 and q["priority_confidence"] >= 0.7:
    auto_route(q["queue"], q["priority"])   # vùng cao: tự làm
elif q["queue_confidence"] >= 0.5:
    suggest_to_agent(q)                      # vùng vừa: gợi ý, người duyệt
else:
    human_triage(ticket_text, q)            # vùng thấp: người xử lý
