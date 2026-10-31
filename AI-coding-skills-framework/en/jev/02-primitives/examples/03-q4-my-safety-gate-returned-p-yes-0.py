conf = lambda p: abs(p - 0.5) * 2
if p_refund > 0.5 and conf(p_refund) >= 0.8:
    open_refund_workflow(ticket)      # high band
elif p_refund > 0.5:
    queue_for_agent_review(ticket)    # balanced → confirm
else:
    reply_with_clarifying_question(ticket)
