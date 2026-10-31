p = resp.answers["destructive"].p
certainty = abs(p - 0.5) * 2
if p >= 0.85 and certainty >= 0.5:
    block_and_escalate()
elif certainty < 0.2:
    ask_human()          # p ≈ 0.5 → gần như không biết
else:
    review_queue()
