u = resp.answers["urgency"]
if u.score >= 3.5 and u.confidence > 0.5:
    page_oncall()               # vượt ngưỡng và đủ chắc
elif u.score >= 2.5:
    bump_priority_queue()       # trung bình
else:
    standard_queue()
