def idem_key(plan: str, sub: str, inputs: dict) -> str:
    h = hashlib.sha1(repr(sorted(inputs.items())).encode()).hexdigest()[:12]
    return f"{plan}:{sub}:{h}"

store: dict = {}
def run_subtask(plan, sub, inputs, fn, *, risk="low"):
    k = idem_key(plan, sub, inputs)
    if k in store: return store[k]   # idempotent replay
