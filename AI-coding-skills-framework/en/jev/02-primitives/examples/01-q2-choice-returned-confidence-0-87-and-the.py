if team["confidence"] >= 0.8:
    route(ticket, team["selected"])                   # auto-act
elif team["confidence"] >= 0.5:
    route(ticket, team["selected"], confirm=True)     # confirm / more context
else:
    escalate_to_human(ticket)
