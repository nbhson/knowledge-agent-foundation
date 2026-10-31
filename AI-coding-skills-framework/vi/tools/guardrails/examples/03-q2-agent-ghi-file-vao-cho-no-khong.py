from guardrails import Guard
from guardrails.hub import RegexMatch

guard = Guard().use(RegexMatch("^[a-zA-Z0-9_./-]+$"))
result = guard.validate("/etc/hosts")   # REJECT
result = guard.validate("src/main.py")  # ALLOW
