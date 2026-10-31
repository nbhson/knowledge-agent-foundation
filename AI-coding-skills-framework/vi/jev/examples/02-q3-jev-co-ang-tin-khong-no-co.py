probs = answer["probabilities"]
top = max(probs.values())
second = sorted(probs.values())[-2]
if top - second < 0.15:      # gần hòa → đừng tự quyết
    escalate_to_human(probs)
else:
    route(answer["selected"])
