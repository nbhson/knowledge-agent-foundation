if anger["score"] >= 2.5 and anger["confidence"] >= 0.6:
    page_oncall(ticket)            # right level, peaked → auto-act
elif anger["score"] >= 2.5:
    flag_for_human_review(ticket)  # right level, weak margin → confirm
