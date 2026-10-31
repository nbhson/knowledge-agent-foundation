# Không có guardrail:
agent → write_file(path="/etc/hosts", content="...")  # 💥

# Có guardrail:
guard = Guard().use(PathValidate(whitelist=["src/", "tests/", "./"]))
result = guard.validate(path="/etc/hosts")  # ❌ REJECT
result = guard.validate(path="src/main.py") # ✅ ALLOW
