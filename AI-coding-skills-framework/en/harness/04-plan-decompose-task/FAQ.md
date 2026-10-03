# ❓ FAQ — Planning & Task Decomposition (Real Stories, Plain Language)

If a question is unclear, read the section in `../README.md` (named in brackets).

---

## Q1. My agent wrote 400 lines in one shot and half of it was wrong — why is planning worth 30 seconds? [→ Why Are Planning & Decomposition Important?]

**What you see**

You ask for "add rate limiting to the API", and the agent immediately writes the middleware, the config, the tests and the docs in a single pass. Reviewing it takes longer than rewriting it. Measured across many runs: agents **without planning** succeed **32%** of the time; with **structured decomposition**, **78%** — a 2.4x jump. Retries drop from **40-60% of tasks** down to **10-15%**, and token use falls **30-50%**.

**Why**

Two failure modes sit behind this. **Oversimplification**: the agent jumps into code with no structure, implements the requirement wrong, and starts over from scratch. **Analysis Paralysis**: it analyses forever and never starts. Both waste the same thing — your retry budget.

**What to do**

Run the fixed loop before touching a file: analyze → prioritise → sequence → execute → validate. Keep subtask groups at **3-7 items** (accuracy improves **52%** vs one monolithic task; humans and models both work best with roughly 5-9 items in working memory). Spend 15-30 seconds planning to save 5-15 minutes of retries — a **1:20** return.

```
Plan & Decompose = Analyze → Prioritize → Sequence → Execute → Validate
Decompose any task with more than 3 steps into sub-tasks
Limit plan depth to 4 levels or fewer
Add a validation checkpoint after each major step
Re-plan when a sub-task fails — do not retry identically
```

**Verify**

Check the plan before execution: does each sub-task have a dependency list, a token budget, a termination condition, and a pass criteria? If a plan arrives with none of those four, it is not a plan yet — send it back.

---

## Q2. The agent loops A → B → A → B forever, and "hello world" came back with authentication and i18n — what stops that? [→ If You Skip Planning... / 9.2 DON'T ❌]

**What you see**

Two classic symptoms. **Infinite loop**: the agent runs task A, then B, then A again, and the run never ends. **Scope creep**: you asked for a hello-world script and got auth, logging, internationalisation and a database. Both come from a plan with no stop condition.

**Why**

Three causes: no termination condition per sub-task, no hardcoded-but-computed ordering, and no validation between sub-tasks. Without them, one wrong sub-task silently poisons the other four.

**What to do**

1. Give every sub-task a numeric cap and an exit condition — never "loop until it looks right".
2. Compute the order from dependencies, never write the order by hand.
3. Cap the outer loop too, so a confused agent cannot burn the whole budget.
4. Keep sub-tasks coarse; over-decomposition costs more overhead than it saves.

```python
class Task:                      # guardrails nằm trên từng task
    max_retries = 3; timeout_seconds = 300
    token_budget = None; tools_allowed = []

class ReActAgent:
    def __init__(self, tools, llm_func, max_steps=10):
        self.max_steps = max_steps   # outer loop guardrail
```

**Verify**

Run the module's own unit tests: `test_retry_logic` must return `False` after `retry_count = 3`, and `test_max_depth_limit` must keep depth at 2 when `max_depth=2`. A run that exits with `"Max steps reached without final answer"` means the guardrail fired — raise the diagnosis, not the limit.

---

## Q3. A subtask fails and the agent retries it exactly the same way, three times — how do I make it change strategy? [→ 14.2 Dynamic Replanning Decision Table]

**What you see**

The log shows the identical command failing with `timeout`, then `429`, then `timeout` again. Each attempt costs real tokens and returns the same result. Eventually the run either dies or silently produces a half-finished tree.

**Why**

Because "retry" and "replan" were treated as one action. They are different: a retry repeats the same decomposition, a replan produces a **different** one, and a third option stops and asks a human. Treating all failures as retryable wastes the budget and hides the real cause.

**What to do**

Classify every failure into one of three decisions, then log `attempt, error_class, decision, reason`. Cap auto-retries at **3** and auto-replans at **2**, then escalate — no infinite loops. A deny from an approval gate must trigger a **replan that excludes the denied branch**, never a retry, or it loops forever.

| Signal | Retry | Replan | Escalate |
|---|---|---|---|
| `timeout`, `429`, attempt < 3 | yes | — | — |
| Same subtask failed 3x / new error class | — | yes | — |
| Plan confidence < 0.4, unclear intent | — | ask-clarify first | — |
| Deploy / delete / payment | — | — | approval gate |

**Verify**

```python
if state.get("replans", 0) >= MAX_REPLAN: return "escalate"
if state.get("transient") and state.get("attempts", 0) < MAX_RETRY: return "retry"
if state.get("status") == "failed": return "replan"
```

Assert in tests that a run cannot exceed 3 retries and 2 replans, and that every transition wrote a decision and a reason to the log.

---

## Q4. A deploy subtask ran twice after a crash and the payment step fired twice — how do I stop double side effects? [→ 14.4 Subtask Idempotency + Partial Failure]

**What you see**

The process crashed after subtask 3 succeeded but before its result was saved. On restart, subtask 3 ran again: a second database migration, a second `prod.deploy`, a duplicated charge. Subtask 5 never ran, and the caller received a vague error instead of a status.

**Why**

Side-effecting subtasks had no stable identity. Without one, "resume" and "run again" look identical to the executor, so recovery silently doubles irreversible work.

**What to do**

1. Build a stable key from plan, subtask and a hash of the inputs: `f"{plan_id}:{subtask_id}:{sha1(canonical_inputs)}"`.
2. Check the result store **before** executing; on replay, return the cached result.
3. Tag risky subtasks during decomposition: `db.migrate, prod.deploy, user.delete, external.send` → `risk ∈ {high, irreversible}`. Untagged subtasks are `low` and never block.
4. Track per-node status `ok/failed/skipped`, keep independent branches going, skip dependents of failed nodes, and return `partial:true + completed[] + failed[]` explicitly.

```python
def idem_key(plan: str, sub: str, inputs: dict) -> str:
    h = hashlib.sha1(repr(sorted(inputs.items())).encode()).hexdigest()[:12]
    return f"{plan}:{sub}:{h}"

store: dict = {}
def run_subtask(plan, sub, inputs, fn, *, risk="low"):
    k = idem_key(plan, sub, inputs)
    if k in store: return store[k]   # idempotent replay
```

**Verify**

Crash the executor mid-subtask, replay it, and confirm the cache returns the first result with no second side effect. Confirm the caller receives `partial: true` with both `completed[]` and `failed[]` rather than a generic error.

---

## Q5. My token bill exploded and Tree of Thoughts explored 27 paths to fix one typo — where is the ceiling? [→ 9.3 Token Budget Management / 14.5 Explosion Guards]

**What you see**

A "small" bug triggered a full branch search: `branching_factor=3`, `max_depth=3`, so `paths_explored` reported **27** rollouts. The run also passed the 100k token ceiling and the 50-tool-call limit, then kept going. Separately, a subtask that only needed 5,000 tokens was allocated 100,000 and used 9,500 without anyone noticing.

**Why**

Two missing ceilings. **Tree of Thoughts** (ToT — explore several reasoning branches, score each, keep the best) multiplies: branches × depth. **Budget** without a per-task stop rule means the plan decides the ceiling, and the model decides the plan.

**What to do**

Hard-cap structure and cost together: `MAX_DEPTH=4, MAX_FANOUT=5, MAX_SUBTASKS=25`; ToT `MAX_BRANCHES=3, MAX_ROLLOUTS=9`, prune any branch scoring below 0.3 after 2 steps. Globally: `MAX_TOKENS_PER_PLAN=100k` and `MAX_TOOL_CALLS=50`, with a warning subtask at 80% and a freeze plus escalate at 100%, carrying a `best-so-far` summary. Per task, stop at 90% of its own allocation.

```typescript
canContinue(taskId: string): boolean {
  const allocated = this.allocated.get(taskId) || 0;
  const used = this.used.get(taskId) || 0;
  return used < allocated * 0.9;   // allow up to 90%
}
```

**Verify**

Run the module's budget tests: allocating 30,000 then 25,000 against a 50,000 total must return `False`; reporting 5,000 then 4,500 on a 10,000 allocation must flip `canContinue` to `False`. Confirm no run exceeds 25 sub-tasks or 9 rollouts.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: `README.md` (IV. Planning & Task Decomposition).*