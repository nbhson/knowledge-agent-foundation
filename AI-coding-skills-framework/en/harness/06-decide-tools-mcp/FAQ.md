# ❓ FAQ — Decide Tools / MCP Calls (Real Stories, Plain Language)

If a question is unclear, read the section in `../README.md` (named in brackets).

---

## README.md

---

## Q1. The agent used a code tool on a question that had nothing to do with code — why? [→ §2. Intent Classification]

**What you see**

Someone asks "decode that base64 string". The agent calls `execute_python`, writes `fix.py`, and reports a code change. The execution log says `intent: code, method: rule, confidence: 0.4`.

Worse, on "research the README and check the tests", only the first half runs. `classify_multi_intent()` splits on `and|;|then|after that` and returns `[read, test]`, but `process_multi()` executes one tool per intent and then hits `break` — the test step is silently dropped, and the answer looks complete.

**Why**

`INTENT_RULES["code"]["keywords"]` contains the bare word `code`, and the matcher is a plain substring test (`if kw in query_lower`). So `code` is found inside "decode" and "encode". Confidence is computed as `min(score / 5, 1.0)`, and in `auto` mode the classifier only escalates to the model when confidence is below `0.7` — **and only if an LLM function was passed into `IntentClassifier(llm_func)`**. With `IntentClassifier()` and no LLM, a 0.4 guess is returned unchanged.

**What to do**

1. Match keywords on word boundaries, not substrings, and add negative keywords per intent.
2. Always pass an LLM function so `auto` mode can escalate below the `0.7` threshold.
3. Treat `confidence < 0.4` as "ask the user", not "guess".
4. Log every intent the pipeline *did not* execute, so dropped steps are visible.

```python
import re
def hits(kw, text):
    return re.search(rf"\b{re.escape(kw)}\b", text) is not None
scores[intent] = sum(1 for kw in config["keywords"] if hits(kw, query_lower))
```

**Verify**

Add tests next to the existing ones in §14: `classify("decode this base64")` must not return `code`; `classify("Hello!")` must still return `chat`; and a compound query must report `total_intents == total_success` or an explicit list of skipped steps.

---

## Q2. The agent ran a destructive tool even though it was "allowed" — how did that happen? [→ §8. Permission System, §17.2]

**What you see**

A user with role `user` triggers `write_file`, or a tool writes outside its declared area and the harness returns `error: "capability-escalation"`. In other runs nobody sees any denial at all: `execute()` steps 1–6 pass, and a file is gone.

**Why**

Two separate holes. First, in `ToolExecutor.execute()` the permission check is guarded by `if self.permission_checker and user_id:` — **no `user_id` means no permission check at all**. The same pattern appears in `HarnessToolDecisionSystem.executeTool()`. Second, permission levels are declared per tool: `sql_query`, `execute_python` and `write_file` carry `requires_permission="elevated"`, which only `power_user` and `admin` hold (`guest → public`, `user → public+standard`).

**What to do**

1. Fail closed: treat a missing `user_id` as `guest`, never as "skip the check".
2. Make tools declare their blast radius, not just their parameters: `net`, `allowWrite`, `secrets`, `irreversible`.
3. Apply default-deny to any tool that declares nothing, so it renders as unknown risk.
4. Refuse to widen: if a runtime write or egress host is outside the declaration, deny and emit `capability-escalation` instead of allowing it silently.
5. Keep the sandbox deadline `≥` `timeout_seconds`, so the outer deadline never fires before the tool reports.

```python
role = self.user_roles.get(user_id, "guest")   # never skip the check
allowed = required_permission in set(
    self.ROLE_PERMISSIONS.get(role, ["public"]) + custom_perms)
```

**Verify**

`check("user1", "elevated")` is denied, `check("admin1", "admin")` is allowed, and an audit line exists for both. Then attempt a write outside `allowWrite` and a fetch to an undeclared host: both must be denied and logged as escalations.

---

## Q3. MCP calls are slow and one giant result blew up my context window [→ §3.2 MCP Client, §17.3 MCP Production Rules]

**What you see**

Every single turn re-runs `tools/list`, so a five-step task pays the discovery cost five times. One search server returns 900KB of rows; the conversation now carries all of it. Sometimes you also see `MCP version mismatch` or provider `429`s after a loop.

**Why**

`MCPClient.list_tools()` in §3.2 reassigns `self._tools_cache` on every call — that is teaching code, not production code. §17.3 states the production rules the sample omits: pin `protocolVersion`, cache `tools/list` for 5–15 minutes, invalidate immediately on `426` or an unknown tool, and cap the payload (`timeout 30s`, result ≤ 128KB, args ≤ 32KB). Separately, every tool defaults to `rate_limit_per_minute: 60` with a 60-second sliding window, so an agent loop can burn the quota and be banned.

**What to do**

1. Pin the protocol version and cache the tool list with a TTL plus an ETag.
2. Cap the result before it enters the transcript, and append a truncation marker.
3. Schema-validate arguments before sending; reject anything over 32KB.
4. Forward streaming `content` chunks, with a 10s idle timeout and an abort on client cancel.

```typescript
const key = `${tool}:${JSON.stringify(args)}`;
const hit = memo.get(key);
if (hit && Date.now() - hit.at < 60_000) return { ...hit.val, memoHit: true };
// after the call:
if (JSON.stringify(j).length > 128_000) text += "\n…[truncated: result cap 128k]";
```

**Verify**

A second identical call reports `memoHit: true`. A 900KB response arrives truncated with the marker. The 61st call in a minute is refused with `retry_after`. Restarting with a mismatched `protocolVersion` produces `426` and forces a cache invalidation.

---

## Q4. A tool failed three times and I still can't tell what happened [→ §4. Tool Executor]

**What you see**

The final answer is `Failed after 3 attempts: Timeout after 30s`, and the log has one row, not three. A tool that hangs never returns at all. And the rate limiter says you made 3 calls while `get_usage()` counts 1.

**Why**

`effective_timeout` is computed but never enforced — the only use is the error string, and `tool.function(**parameters)` runs with no timeout wrapper. The retry loop calls `time.sleep(min(0.5 * 2 ** attempt, 5.0))`, i.e. 0.5s then 1.0s for the default `max_retries=3`. Crucially, the rate-limit check happens **once before** the loop, so three real calls consume one slot. `_error_result()` appends only one log row per failed call, hiding how many attempts ran.

**What to do**

1. Enforce the timeout where the call happens, and kill the process group, not just the child.
2. Log one row per attempt with the attempt number and the backoff actually slept.
3. Count each retry against the rate limit, or retries become a quota bypass.
4. Put the actionable part in the message: tool name, attempt count, elapsed time.
5. Only retry what is actually retryable — a validation error or a permission denial will never succeed.

```python
for attempt in range(tool.max_retries):
    limiter.check(tool_name)                 # every attempt counts
    log_entry["attempt"] = attempt + 1
    # wrap the call in a real deadline, then sleep before the next try
    time.sleep(min(0.5 * (2 ** attempt), 5.0))
```

**Verify**

A tool that sleeps forever is killed at its declared timeout and the failure names the attempt count. `get_stats()` shows `total_calls`, `failed` and per-tool `tool_errors`. Retrying past the limit is refused instead of succeeding.

---

## Q5. With 50 tools registered, the agent keeps picking the slow, flaky one [→ §1.1 Tool Registry, §15.1 Tool Learning]

**What you see**

A `vector_search` that fails 40% of the time still wins over a proven 100%-success tool, and a brand-new tool beats your fastest one on day one. Nothing looks broken — the ranking is just wrong.

**Why**

Two ranking formulas disagree. `ToolRegistry.search()` sorts by `success_rate / max(avg_latency_ms, 1)`, and a fresh tool starts at `success_rate=1.0` with latency `0`, so every new tool ties at the top. Metrics move slowly because they are an exponential moving average with `alpha = 0.1`. `ToolLearner.recommend()` scores `success_rate * (1 - min(avg_latency/1000, 1))` and gives an **unused tool a neutral `0.5`** — so a tool with perfect success at 800ms scores 0.2 and loses to the unknown one.

**What to do**

1. Use `ToolLearner.recommend()` for task-type ranking, not raw keyword search.
2. Give an unused tool a small score (for example `0.1`), not `0.5`, so proven tools win.
3. Require a minimum number of observations before trusting a score; below that, treat it as unknown.
4. Keep the description precise — the model also reads it, and vague descriptions cause guessing.
5. Trim the exposed list per context (like Cursor in §11.3) instead of shipping all 50 every turn.

```python
if score["total_count"] < 5:
    final_score = 0.1                       # unknown, not competitive
else:
    final_score = success_rate * (1 - min(score["avg_latency"] / 1000, 1))
```

**Verify**

After 50 recorded runs, the tool with the higher success rate and lower latency ranks first; an unused tool ranks last. Add a §14-style unit test asserting both orderings so a scoring change cannot silently regress.

---

## code-mode-sdk.md

---

## Q1. My five-step refactor takes 10–15 seconds and keeps re-sending context — fix? [→ §1–§2 Context and Core Benefits]

**What you see**

Finding `*.ts` files, reading them, replacing `legacyFetch`, and running the linter costs five separate model round-trips. The transcript shows `Turn 1: search_files`, `Turn 2: read_file_1` … and each turn takes 1–3 seconds, so the task alone is 10–15 seconds before any real work happens.

**Why**

Standard tool calling needs one interaction per step, and the whole conversation history is re-sent every turn. The model also has no place to put a loop, an `if`, or a `try/catch`, so filtering happens in prose instead of in code. Code Mode inverts this: the model writes **one** program that orchestrates the SDK, and the whole chain runs in a single turn — §2 claims 80% lower latency and token cost, and §11.4 of the README reports 70–90%.

**What to do**

1. Batch first: `batchTools` groups calls, capped at `maxBatchSize: 10` with a `maxWaitMs: 50` flush window.
2. Keep intermediate data in the runtime's RAM instead of shuttling it through the context window.
3. Return one aggregated result plus a trajectory trace, not every intermediate payload.
4. Ship the complete `@types/dsh` definitions in the system prompt so generated code compiles.
5. Keep standard tool calling for interactive questions where the next step depends on the user's reply.

```typescript
const files = await tools.findFiles('src/**/*.ts');
for (const file of files) {
  const content = await tools.readFile(file);
  if (content.includes('legacyFetch')) {
    await tools.writeFile(file, content.replace(/legacyFetch/g, 'modernFetch'));
  }
}
```

**Verify**

The same refactor completes in one turn and reports `durationMs` around 2,340ms in the README example. Run it twice: same script plus same input gives the same output, so it can be asserted in CI.

---

## Q2. Is it safe to let the model write code that calls tools? [→ §7. Security Guardrails]

**What you see**

A generated script contains `git push --force` or `rm -rf ./src`, and your instinct is that approving the whole program once is enough. The generated code is arbitrary code — it is the most dangerous thing in the system.

**Why**

Code Mode is a **bundler, not a security boundary**. It collapses N individual tool calls into one program, which means per-call approval disappears unless you put it back explicitly. The guardrails are borrowed, not invented here: isolation belongs to `12-sandbox-execution` (Docker container, worker threads, or a V8 isolate — never `eval()` or `vm.runInThisContext()`), the resource caps (`timeoutMs`, `maxMemory`, max shell commands) are that module's §3, and the human pause is the `PAUSED:` protocol in `15-approval-gates` §5.

**What to do**

1. Run the script in an isolated sandbox; never `eval()`, never the current context.
2. Require a dry-run first — static analysis or a TypeScript compile — before execution.
3. Force `console.log()` at key milestones so the event stream has a trail.
4. Pause and ask for dangerous operations; do not treat a timeout as a denial, since that is `15`'s decision.
5. Put **every individual tool call inside the program** through the approval gate.

```typescript
const wrapped = `(async () => { ${code} })();`;
const script = new vm.Script(wrapped);
await script.runInContext(vm.createContext(sandboxContext), { timeout: timeoutMs });
```

**Verify**

A script containing `rm -rf ./src` never reaches the filesystem; the run stops at `PAUSED:` with the command, files touched and the `irreversible` flag rendered from the tool's declaration. A syntax error is caught by the dry run, before any sandbox starts.

---

## Q3. Should I use Code Mode, or is ordinary tool calling safer? [→ §6. Detailed Comparison]

**What you see**

You are choosing between two modes for a real task, and the decision is usually made on vibes. Someone argues Code Mode is faster; someone else says a JSON tool call is auditable.

**Why**

They optimize different things. Standard tool calling gives you a visible, per-call decision record and is the right choice when the next step depends on the user or on reasoning you want to see. Code Mode gives you loops, `try/catch`, and data that never enters the context window, which is what batch jobs need. §6 puts it plainly: multi-turn for step-by-step analysis and interactive questions, single turn for batch processing, code refactoring and data migration.

| Criterion | Standard tool calling | Code Mode SDK |
|---|---|---|
| Turns | N turns for N steps | 1 turn for the whole chain |
| Intermediate data | shuttled through the context window | processed in runtime RAM |
| Control structures | none | `for`, `try/catch`, `map/filter` |
| Isolation | process-level | V8 isolate sandbox |
| Best suited for | interactive Q&A, analysis | batch, refactoring, migration |

**What to do**

1. Pick by task shape: well-defined and repetitive → Code Mode; conversational and open-ended → standard calling.
2. Keep Code Mode for code-shaped work; it exposes only `bash`, `editor` and `llm_complete`.
3. Exploit determinism: same script plus same input gives the same output, so it belongs in CI.
4. Keep the audit trail either way — the trajectory trace replaces the visible turns, it does not replace logging.

**Verify**

Run one task of each kind in both modes and compare wall-clock time, transcript size and whether you could point at the exact tool call that caused a bad result. If you cannot name that call from the trace, the mode is wrong for the task.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: README.md, code-mode-sdk.md.*
