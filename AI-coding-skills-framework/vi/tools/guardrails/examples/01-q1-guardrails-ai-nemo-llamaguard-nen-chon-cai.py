from guardrails import Guard
from guardrails.hub import RegexMatch

guard = Guard().use(RegexMatch("^[a-zA-Z0-9_./-]+$"))
guard.validate("hacker/path/../etc/passwd")  # fail
guard.validate("src/main.py")                 # pass
