import re, os
PATTERNS = [r"sk-[A-Za-z0-9]+", r"ghp_[A-Za-z0-9]+", r"AKIA[0-9A-Z]{16}"]
def redact(text: str) -> str:
    for p in PATTERNS:
        text = re.sub(p, "[REDACTED]", text)
    return text

def inject_secret(scope: str, ttl_min: int) -> dict:
    token = f"tmp-{scope}-{ttl_min}m"  # broker cấp token thật
    os.environ["SUBAGENT_TOKEN"] = token
    return {"scope": scope, "ttlMinutes": ttl_min, "via": "env"}
