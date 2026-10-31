import typesafe

client = typesafe.Client(api_key="...")

state = """
Conversation snippet (support):
User: "This is the THIRD time this month. I've wasted two hours
on hold already. Fix it or I'm gone."
"""

resp = client.ask(
    model="jev-latest",
    state=state,
    questions={
        "urgency": {
            "type": "score",
            "levels": [
                {"level": 1, "label": "low"},
                {"level": 2, "label": "medium"},
                {"level": 3, "label": "high"},
                {"level": 4, "label": "critical"},
            ],
            "description": "Urgency of this conversation",
        },
    },
)

u = resp.answers["urgency"]
print(u.score)          # e.g. 3.4  (giữa high và critical)
print(u.distribution)   # {1: 0.01, 2: 0.04, 3: 0.52, 4: 0.43}
print(u.confidence)     # 0.58

# Threshold dựa trên score, không int() blind:
if u.score >= 3.5 and u.confidence > 0.5:
    page_oncall()               # critical + đủ tự tin
elif u.score >= 2.5:
    bump_priority_queue()
else:
    standard_queue()
