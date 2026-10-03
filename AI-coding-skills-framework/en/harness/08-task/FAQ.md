# ❓ FAQ — Task Management (Real Stories, Plain Language)

If a question is unclear, read the section in `../README.md` (named in brackets).

---

## Q1. I said "refactor the auth module, add tests, update docs, then deploy" and the agent did all of it badly — how do I stop that? [→ §1.3 + §2]

**What you see**

One message arrives containing four jobs. The agent starts at the top, loses track halfway, and ends up deploying code whose tests never ran. Nothing throws an error — the output is just a diff with three of the four steps half-finished and a deploy at the bottom.

**Why**

Because the request was never split. The whole request arrived as one unit, and a single unit has no order, no budget per step, and no way to say "this part is finished". The decision rule in the source is simple: if the request is unclear, clarify first; if it can be done in under 500 tokens, do it in one shot; if it is bigger, decompose it into sub-tasks and then pick sequential, parallel, or test-first execution.

**What to do**

1. Break the request into steps that each touch a small number of files. The layers pattern is a good default for a refactor: database → service → API → UI → integration tests, each one waiting on the previous.
2. Cap each sub-task at 5,000 tokens. Anything estimated above 20,000 tokens is flagged as a "killer task" and must be split.
3. Do not split the other way either. Sub-tasks under 500 tokens cost more in bookkeeping than they save; the sweet spot is roughly 100 to 5,000 tokens.
4. Mark sub-tasks that touch different files with `parallel=True` so they can run in the same batch.
5. Give every sub-task a written check ("schema updated, migrations run") so "done" is not a guess.

```python
# One file = one sub-task, safe to run side by side
SubTask(id=f"{task.id}-f01", order=1, parallel=True,
        files_to_modify=["src/auth.py"],
        estimated_tokens=1000,
        verification_criteria="File src/auth.py updated correctly")
```

**Verify**

Print the sub-task list with its order, dependencies and token totals, and add them up. If the total is 12,000 tokens for a change that should cost 6,300 (the `refactor` template in the source), the split is wrong. Then confirm no sub-task is above 5,000 tokens and none is below 500.

---

## Q2. Two tasks wait for each other and the whole run hangs — how do I find the loop? [→ §5]

**What you see**

The agent stops making progress and just sits there. Task A is listed as waiting on task B, task B is listed as waiting on task A, and neither ever starts. In a real project the same thing shows up as "batch 1 blocked the service and API steps, so the feature never ships".

**Why**

Dependencies are stored as a directed graph — "A → B" means A must finish before B starts. If someone (or the agent) writes A → B and B → A, that graph has a cycle, and a cycle has no valid order. Nothing crashes: the graph simply never becomes executable.

**What to do**

1. Detect the cycle before scheduling. The `has_cycle()` check walks the graph depth-first and reports the first back-edge it finds.
2. Let the sort fail loudly instead of looping forever. `topological_sort()` raises `ValueError("Cycle detected in task dependencies")`, and `parallel_groups()` raises `ValueError("Unresolvable dependency cycle")`.
3. Break the loop manually: pick one edge, delete it, and decide which of the two tasks is really the prerequisite.
4. Watch the count, not just the cycle. More than 5 dependencies on a single task is reported as `DEPENDENCY_OVERLOAD` with MEDIUM severity — that is usually a sign one task is doing three jobs.
5. Add a runtime guard so a stalled round cannot pass for progress: fail the batch if two scheduling rounds complete with nothing new finished.

**Verify**

Run the cycle check on every plan before execution starts, and keep a test fixture with a deliberate `A → B → A` loop that must be rejected. Confirm the error message names the cycle instead of the run simply stalling.

---

## Q3. I wrote "improve the code" and the agent went off in the wrong direction for 8,000 tokens — whose fault is that? [→ §1.2 + §8.2]

**What you see**

The request goes in as something like "clean up the API layer". The agent picks a direction, rewrites a few files, and produces something plausible but not what you meant. You find out only at the end, after the tokens are already spent.

**Why**

Two things. The description is vague, so it matches every category equally and the classifier falls back to its default. And no one wrote down what "done" means, so there was nothing to check the work against. The source lists the vague triggers explicitly: `improve`, `optimize`, `clean`, `better`, `refactor`, `make it work`, `fix it`.

**What to do**

1. Run the anti-pattern detector before starting, not after. A vague word plus an empty verification field is reported as `AMBIGUOUS_TASK`, MEDIUM.
2. Replace vague words with a file list and an outcome: "cut `handlers.py` from 600 to under 300 lines, no behaviour change, all tests green".
3. Fill in the missing numbers. No token estimate raises `MISSING_ESTIMATE`; a modification task with an empty file list raises `MISSING_FILE_SCOPE` — scan the codebase and name the files.
4. Classify the request so the strategy follows: generation across more than 3 files becomes vertical slices, modification across more than 5 files becomes layer-based, anything COMPLEX or EPIC starts with a timeboxed spike.
5. Use an existing template instead of inventing steps — `bug_fix` totals about 5,300 tokens, `new_feature` about 8,100.

**Verify**

Before executing, confirm the task has a non-empty description, a token estimate above zero, and a verification string. If the detector returns any MEDIUM or HIGH item, fix it first.

---

## Q4. The context window filled up halfway and the agent forgot the original goal — what now? [→ §10]

**What you see**

You are maybe 80% through the work and the agent starts answering a slightly different question than the one you asked. It re-reads files it already read, forgets a constraint you stated at the start, and the session ends with no room left to even write a summary.

**Why**

Nobody split the context window into budgets. In the source's 128K allocation, the system prompt takes about 5,000 tokens, project context 30,000, task context 20,000, and working memory 50,000 — leaving a reserve of roughly 23,000. Working memory is the part that grows without limit: generated code, intermediate results, tool output.

**What to do**

1. Set the reserve before you start, not after you overflow. `TokenBudgetManager` holds back 20,000 tokens by default, and `remaining` subtracts that reserve every time you ask.
2. Check before every sub-task. `allocate_for_task()` returns `False` when the estimate does not fit — treat that `False` as "stop and start a new session", not as "squeeze it in".
3. Know the warning marks: usage above 80% prints a high-usage warning, and remaining under 5,000 is flagged critical.
4. Compact on a schedule. Working memory above 30,000 means summarize it; project context above 20,000 means drop non-essential files; above 85% usage, finish the current sub-task and start fresh.
5. This is also the cure for context drift: timebox each task so the agent is forced to refresh its own context instead of carrying everything.

**Verify**

Print the budget summary — total, per-bucket usage, remaining, usage percent — at the start of every sub-task. In one real auth refactor the budget gate deferred the UI docs to session 2 on purpose, and nothing was lost.

---

## Q5. A task timed out at 60 seconds, the retry ran the database migration a second time — how do I stop double writes? [→ §12]

**What you see**

The task is marked `failed:timeout`. The engine retries it, and this time it succeeds — but the migration that already ran on the first attempt runs again, or a file gets written twice, or a duplicate row appears in the database. The retry "fixed" the failure and created a new one.

**Why**

Timeout and retry are not aware of side effects. `timeoutMs` defaults to 60 seconds per task and aborts the run on expiry; `maxRetries` then retries with exponential backoff and jitter. Without a marker saying "this exact work already happened", the retry cannot tell a duplicate from a first attempt.

**What to do**

1. Give every task an idempotency key — a value that is identical for a retry and different for genuinely new work. The TypeScript engine builds it as `${t.id}:${t.title.length}` and uses it to dedupe retries.
2. Retry only what is safe to repeat: idempotent operations, or tasks that checkpoint before the risky step. Never auto-retry a non-idempotent write.
3. Keep a single writable step per task at a time — the queue depth is 1 per task — so two attempts cannot overlap.
4. Classify failures instead of blanket-retrying. Transient → retry; permanent → park the task and emit `task.failed`; budget → compact and re-estimate, then continue the graph.
5. When you cancel a task, expect its dependents to become `blocked` rather than silently skipped.

**Verify**

Inject a deliberate timeout on a write task, let the retry happen, and check the audit record: the `trajectoryId` and the `transition` events show both attempts, and the side effect happened exactly once. In the source's auth refactor case study, that is exactly the outcome — 1 retry, 0 double-writes.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: README.md.*