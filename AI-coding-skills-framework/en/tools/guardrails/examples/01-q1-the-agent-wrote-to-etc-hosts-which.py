from guardrails import Guard
from guardrails.hub import PathValidate, RegexMatch
guard = Guard().use(PathValidate(whitelist=["src/", "tests/", "./"]))
guard.validate(path="/etc/hosts")    # REJECT
guard.validate(path="src/main.py")   # ALLOW
