from guardrails import Guard
from guardrails.hub import RegexMatch, ValidLength, TwoSimilarChunks

# Guard cho một tool call
guard = Guard().use(RegexMatch("^[a-zA-Z0-9_./-]+$"))  # chặn path lạ
guard.validate("hacker/path/../etc/passwd")  # ❌ fail
guard.validate("src/main.py")                # ✅ pass
