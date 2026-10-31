from guardrails import Guard
from guardrails.hub import RegexMatch, ValidLength, TwoSimilarChunks

# Guard for a tool call
guard = Guard().use(RegexMatch("^[a-zA-Z0-9_./-]+$"))  # block weird paths
guard.validate("hacker/path/../etc/passwd")  # ❌ fail
guard.validate("src/main.py")                # ✅ pass
