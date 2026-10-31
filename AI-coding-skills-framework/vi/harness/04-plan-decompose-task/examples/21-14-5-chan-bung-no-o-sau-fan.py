import hashlib
MAX_RETRY, MAX_REPLAN = 3, 2
MAX_DEPTH, MAX_FANOUT, MAX_TOKENS = 4, 5, 100_000

def idem_key(plan: str, sub: str, inputs: dict) -> str:
    h = hashlib.sha1(repr(sorted(inputs.items())).encode()).hexdigest()[:12]
    return f"{plan}:{sub}:{h}"

store: dict = {}
def run_subtask(plan: str, sub: str, inputs: dict, fn, *, risk="low"):
    k = idem_key(plan, sub, inputs)
    if k in store: return store[k]  # replay idempotent
    if risk in ("high", "irreversible") and not approved(plan, sub, inputs):
        return {"status": "blocked", "reason": "approval-denied"}
    try:
        out = fn(inputs); store[k] = {"status": "ok", "out": out}
    except Exception as e:
        store[k] = {"status": "failed", "err": str(e), "transient": is_transient(e)}
    return store[k]

def decide(state: dict) -> str:  # retry | replan | escalate | done
    if state.get("risk_gate"): return "escalate"
    if state.get("tokens", 0) > MAX_TOKENS * 0.8: return "escalate"
    if state.get("replans", 0) >= MAX_REPLAN: return "escalate"
    if state.get("transient") and state.get("attempts", 0) < MAX_RETRY: return "retry"
    if state.get("status") == "failed": return "replan"
    return "done"

def approved(plan, sub, inputs) -> bool:
    print(f"[GATE] approve {plan}/{sub} {inputs} ? (y/n, timeout -> deny)")
    return input().strip().lower() == "y"

def is_transient(e: Exception) -> bool:
    return any(s in str(e).lower() for s in ("timeout", "429", "econnreset"))
