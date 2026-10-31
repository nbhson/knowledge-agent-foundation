from langchain.typesafe import TypeSafeClassifier

clf = TypeSafeClassifier(
    model="jev-1.13.0",
    api_key=os.environ["TYPESAFE_API_KEY"],
)

answers = clf.invoke({
    "state": "Ticket #4821: charged twice, want refund.",
    "questions": {
        "intent": {
            "type": "choice",
            "choices": ["billing", "tech", "account", "other"],
            "description": "Primary intent of this message?",
        },
        "toxic": {
            "type": "noul",
            "description": "Is this message abusive or toxic?",
        },
    },
})

print(answers["intent"].choice)     # → routing branch
if answers["toxic"].p >= 0.9:
    hold_for_moderation()
