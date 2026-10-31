import os
import requests

API = "https://api.typesafe.ai/v1/systemone"
HEADERS = {
    "Authorization": f"Bearer {os.environ['TYPESAFE_API_KEY']}",
    "Content-Type": "application/json",
}

STATE = "Third email today. 'If this isn't fixed by Friday I'm filing a chargeback.'"

QUESTIONS = {
    "anger": {
        "type": "score",
        "levels": [
            {"level": 1, "description": "calm — patient, no urgency signals"},
            {"level": 2, "description": "frustrated — annoyed, repeated contact"},
            {"level": 3, "description": "very angry — hostile, threats, chargeback talk"},
        ],
        "question": "How angry is the customer?",
    }
}

resp = requests.post(
    API,
    headers=HEADERS,
    json={"model": "jev-latest", "state": STATE, "questions": QUESTIONS},
    timeout=5,
)
resp.raise_for_status()
anger = resp.json()["answers"]["anger"]["score"]

print(anger["score"])            # e.g. 2.70  (may fall BETWEEN levels)
print(anger["legend"])           # your level descriptions, echoed
print(anger["probabilities"])    # {1: 0.05, 2: 0.20, 3: 0.75}
print(anger["confidence"])       # margin from the distribution shape

if anger["score"] >= 2.5 and anger["confidence"] >= 0.6:
    page_oncall(ticket)          # high band → auto-act
elif anger["score"] >= 2.5:
    flag_for_human_review(ticket)  # right level, weaker margin → confirm
