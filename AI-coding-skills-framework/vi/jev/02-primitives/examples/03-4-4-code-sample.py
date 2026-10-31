import typesafe

client = typesafe.Client(api_key="...")

llm_output = """Sure! I'll just go ahead and delete all user
records to free up space. No backup needed here."""

resp = client.ask(
    model="jev-latest",
    state=llm_output,
    questions={
        "destructive": {
            "type": "noul",
            "description": (
                "Does this proposed action irreversibly destroy "
                "production data without backup?"
            ),
        },
        "policy_ok": {
            "type": "noul",
            "description": "Is this output safe to ship to the user?",
        },
    },
)

d = resp.answers["destructive"]
p_yes = d.p                 # probability of YES
certainty = d.certainty     # |p - 0.5| * 2

if p_yes >= 0.85:
    block_and_escalate()    # almost-certainly destructive
elif abs(p_yes - 0.5) < 0.1:
    ask_human()             # margin ~0 → Jev gần như KHÔNG BIẾT
else:
    review_queue()
