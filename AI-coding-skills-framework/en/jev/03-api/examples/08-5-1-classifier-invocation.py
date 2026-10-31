from langchain.classifiers import TypeSafeClassifier

classifier = TypeSafeClassifier(model="jev-latest")

answers = await classifier.ainvoke(
    state="User: my export keeps failing with timeout after 30s",
    questions={
        "intent": {
            "type": "choice",
            "options": ["bug_report", "how_to", "billing", "churn_risk"],
            "question": "What is the user's intent?",
        },
        "is_escalation": {
            "type": "noul",
            "question": "Is the user asking for a human?",
        },
    },
)

intent = answers["intent"].selected          # "bug_report"
p_esc = answers["is_escalation"].p_yes       # e.g. 0.12
