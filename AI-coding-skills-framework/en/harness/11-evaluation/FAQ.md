# ❓ FAQ — Evaluation (Real Stories, Plain Language)

If a question is unclear, read the section in `../README.md` (named in brackets).

---

## README.md

### Q1. My new model scores 92% on HumanEval, but my bug-fix rate did not move at all — which benchmark should I trust? [→ §3.3 + §10.1]

**What you see**

You switch models, read a leaderboard, and celebrate 92% Pass@1 on HumanEval. Three weeks later your own issue tracker looks exactly the same. Meanwhile the SWE-bench-style numbers in the same chapter tell a different story: Claude 92% on HumanEval but only 53% on SWE-bench Verified, and 45% on LiveCodeBench. On the real-issue leaderboard (2294 GitHub issues with ground-truth patches) the best system resolves 26.0%, the worst 17.0% — and cost per issue ranges from ~$0.30 to ~$0.60 with 15K–30K tokens per attempt.

**Why**

HumanEval asks for one self-contained Python function. SWE-bench asks the agent to find the right file in a real repository, understand the issue text, and not break the other 900 tests. The HumanEval table also warns it is hitting a ceiling: GPT-3.5 Turbo went 48% → 72%, GPT-4 67% → 86%, and large models are now parked around 90%. A ceiling means the benchmark can no longer separate models.

**What to do**

1. Grade with the project's own test suite, using the 5-step method: run the agent, apply its patch, run the tests, check the failing tests now pass, then check the tests that used to pass still pass.
2. Pick the benchmark that matches the job. Editing code? Aider Polyglot-style. Fixing repo bugs? SWE-bench-style. Writing single functions? HumanEval is fine as a smoke test only.
3. Report resolve rate **and** cost per task together. Cheap models win on value: DeepSeek V3 reaches 92% of GPT-4o's quality at 11% of the cost.
4. Never mix benchmarks into one "composite" number — different question sets, different scales.

```python
summary = suite.run(agent_func)
print(summary["success_rate"], summary["avg_tokens"], summary["avg_attempts"])
# 0.45  21500  2.4   <- resolve rate, tokens, attempts
```

**Verify**

Your own suite has ~10 tasks from your domain (fix a null check in `UserService.getProfile`, add pagination, fix SQL injection in `UserDAO.findByEmail`). If a model change does not move your own resolve rate, the leaderboard number was never about your work.

---

### Q2. I changed one line in the system prompt and two tasks got worse — real regression or just noise? [→ §4.3 + §5.1]

**What you see**

You tweak wording, rerun, and two tasks that used to pass now fail. You cannot tell whether the change hurt the agent or the run was simply lucky before. Meanwhile `suggest_improvements` is telling you `⚠️ safety: Average score 47.3/100`, and `analyze_trend` returns `{"trend": "insufficient_data"}` because you only have one recorded iteration.

**Why**

A prompt change is a behaviour change, but one sample per task cannot separate signal from noise. Worse, the fallback scorer is weak: `_similarity_score` compares word sets, so `intersection / expected_words * 100` rewards copying the right words even when the logic is wrong. And a missing baseline silently defaults to `50.0`, which means a brand-new task is judged against a number you never measured.

**What to do**

1. Freeze a golden answer per task, then call `set_baseline` explicitly. Never rely on the `50.0` default.
2. Keep the 10-point band as your alarm: `if score < baseline - 10` flags a regression, `score > baseline + 10` an improvement. Below the band, treat a change as noise.
3. Run each task 3 times and take the median before declaring anything.
4. Compare like with like — a "don't" in the checklist is literally *don't compare across different benchmark setups*.
5. Act on the thresholds the tracker already encodes: average under 60 → fix the prompt; 60–80 → improve context and examples.

**Verify**

Run the same agent twice with no changes: the pass/fail list must be identical. Then revert your prompt edit — the score must return to baseline inside the ±10 band, and the alert (`⚠️ REGRESSION DETECTED!` with `id`, `baseline`, `current`) must stop firing.

---

### Q3. My benchmark reports 78% — but half the tasks were graded by a validator that always returns True. How do I stop fooling myself? [→ §3.2 + §4.1]

**What you see**

The suite reports a healthy `success_rate`, and you quote it in a slide. But in `BENCHMARK_TASKS`, six of the ten tasks — `api_endpoint`, `bug_fix`, `refactor_class`, `write_tests`, `security_audit`, `multi_file_refactor` — carry `"validator": lambda out: True`. Only three tasks actually assert anything: `string_reverse` checks `out("hello") == "olleh"`, `fibonacci` checks `out(10) == 55`, `binary_search` checks `out([1,2,3,4,5], 3) == 2`. Add a fourth trap: `check_test_passes` returns `50.0` when no tests are supplied ("No tests = neutral score").

**Why**

A validator that always returns true is not a weak measurement — it is the absence of one, counted as a success. The suite then measures *attempt rate*, not quality, and every improvement you "see" is your own scoring code lying to you.

**What to do**

1. Replace every `lambda out: True` with a real assertion, or move the task to a human-reviewed pool.
2. Fail closed: no validator means score 0, not pass. Never let "I had nothing to check" become "it worked".
3. Make `check_test_passes` actually execute the test suite and return the pass rate.
4. Add the process metrics from `AgentQualityMetrics` next to the score: `first_attempt_success`, `edit_precision` (edits that were truly necessary ÷ total edits), and `regression_free_rate`.
5. Say which tasks are objective and which are subjective, in the report itself.

**Verify**

Mutation check: deliberately break one solution (return `None` instead of the result) and rerun. Every honest score must drop. If the number stays at 78%, your validator is decorative — fix that task before trusting any trend line.

---

### Q4. The dashboard says composite 81/100, but developers still rewrite most of the output — which number do I trust? [→ §2.3 + §10.4 + §9.1]

**What you see**

```
CORRECTNESS   82%   (test pass 85, edge cases 72, regression free 90)
QUALITY       75%   (maintainability 70, naming 88, documentation 68)
EFFICIENCY    80%   SAFETY 88%   COMPOSITE 81/100
```

The composite is green, and it has been green for a month. But developers reject or rewrite most suggestions, so the work still costs more than writing it by hand.

**Why**

The composite is a weighted average of proxies, and the weakest proxy is doing the most damage: documentation coverage at 68% says nothing about whether a human accepts the code. Benchmark score measures the benchmark. Meanwhile a checklist item you are already violating is *don't optimize for benchmark at expense of real usage*.

**What to do**

1. Run four layers, as the Anthropic case does: automated benchmarks, human review, real user feedback, A/B tests. No single layer tells the whole story.
2. Make **acceptance rate** — the share of AI suggestions a developer keeps — the headline number, and keep the composite as a diagnostic.
3. Calibrate the automatic score against humans on a sample, on a schedule. An uncalibrated auto-score is a guess with decimals.
4. Treat trades as regressions: if correctness rose 82 → 90 while maintainability fell 70 → 55, you did not improve the agent.
5. Track dollars per quality point, so "cheaper model" is a measured decision.

**Verify**

Have two senior developers blind-score 30 sampled outputs each month and compare with the auto score. Below roughly 80% agreement, recalibrate. And watch the pair: acceptance rate rising while the composite sits flat means the composite is measuring the wrong thing.

---

## minimal-benchmark-harness.md

### Q5. My harness reports 45% Pass@1 but the published number is 53% — which one is my model's real ability? [→ §1 Context & Motivation + §2 Philosophy]

**What you see**

Your own run over the same SWE-bench tasks gives 45%. The public leaderboard says 53% for the same model. The gap moves around between runs, and nobody can point at the cause.

**Why**

Three things distort a benchmark before the model does anything: a system prompt of 2,000+ tokens steers behaviour too hard; framework layers (RAG retrieval, memory consolidation, guardrails) quietly rewrite the answer; and a crowded tool set degrades tool selection, because every extra tool is a chance to pick the wrong one. The result is that you cannot answer the real question — *is the model good at programming reasoning, or is my harness hiding its weakness?*

**What to do**

1. Build the minimal mode: a system prompt under 100 tokens, zero framework middleware, exactly two tools (`bash` and `editor`).
2. Run the same model in both modes and report both numbers. The gap is your harness's contribution, and the README's SWE-bench table suggests harness design alone accounts for 30%+ of the difference between agents.
3. Pin `temperature` and `maxTokens`, cap `maxTurns` at 20, and keep the full `log`/`trajectory` for every task so you can audit a disagreement.
4. Grade objectively: run `task.testCommand` and set `solved = (exitCode === 0)` — never ask the model whether it thinks it passed.

**Verify**

Same 20 tasks, full harness vs minimal harness, more than once each. If the spread between modes is wider than the spread between repeats, the harness is the variable, not the model. Confirm `toolsUsed` contains only `bash` and `editor` on every single task.

---

### Q6. I added a hint and a search tool to help the agent, and the score jumped from 45% to 61% — did I improve it, or just cheat? [→ §7 Best Practices & Isolation Guardrails]

**What you see**

One week: 45%. You add a `hints` block to the problem statement and a grep/search tool. Next run: 61%, and the leaderboard-beating number feels great. Then the same model scores 44% when someone else runs it.

**Why**

The harness file lists this as an anti-pattern: putting problem-solution information or detailed instructions into the system prompt is **prompt leakage**. The second anti-pattern is a **shared workspace**, where tasks share a working directory and produce side effects between tests. Both inflate the score, and neither result is comparable to any published number — you measured the harness author, not the model.

**What to do**

1. Only pass `hints` when the official benchmark task ships them. Keep a separate "harness-assisted" run if you want to track that number.
2. Give each task a fresh container: reset the Docker environment to its pristine state (`git clean` / `git reset`) before every task.
3. Never let two tasks share a working directory.
4. Load **zero injected memory** — no data from previous sessions.
5. Assert the tool allowlist in code, so a leaked tool fails loudly instead of quietly helping.

```typescript
if (!['bash', 'editor'].includes(call.type)) {
  throw new Error(`Tool ${call.type} not allowed in minimal harness`);
}
```

**Verify**

Run task B immediately after task A in the same session: B must still pass. Then rerun the official task set with no hints and confirm you land back on the baseline number. Grep your system prompt for words that appear in the expected patch — if any match, the score is contaminated.

---

### Q7. One task never ends — the runner just sits there and the whole benchmark is stuck. Where is the timeout? [→ §5 Implementing the Benchmark Runner + §7 Best Practices]

**What you see**

The loop is `while (turn < maxTurns)` with `maxTurns = 20`. The model never emits `COMPLETE_TASK`, so it keeps calling `bash`, one of those calls hangs, and the run has no end. Nothing in `BenchmarkResult` ever gets set to `timeout` — the field exists in the type, but the loop has no way to reach it.

**Why**

Turn count and wall-clock time are different limits. A single `npm install` can eat a whole turn budget, and twenty such turns stretch a nightly job into a day. The best-practice list says it directly: set strict timeouts (for example 5 minutes per task) on bash commands to avoid hung processes.

**What to do**

1. Pass a timeout into every container command (`task.timeout || config.limits.timeoutSeconds * 1000`).
2. Add a per-task wall-clock deadline — 5 minutes/task — enforced outside the model loop.
3. Keep `maxTurns = 20` as a second, independent bound.
4. Record `status: 'timeout'` separately from `'failed'`. A timeout is *no answer*, not a wrong answer; averaging the two hides a broken task.
5. Kill the container, not just the child process, so nothing survives into the next task.

**Verify**

Inject a task containing `sleep 3600`. The run must abort at the deadline, the result must show `timeout` with a non-zero `turns` count, no container may survive, and the summary `total_tasks` must still equal the number of tasks you queued.

---

### Q8. Tool error rate came out at 22%, far above the 5% target — is the model bad, or is my tool schema bad? [→ §6 Evaluation Criteria & Metrics + §4 The Minimal Tool Set]

**What you see**

The metric table sets four targets: Pass@1 higher, average turns per task lower, tool error rate **below 5%**, token efficiency lower. Your report shows a 22% tool error rate and 14 average turns per task, while Pass@1 sits at 45%. The obvious conclusion — "the model is weak" — is probably wrong.

**Why**

Look at the `editor` schema: one `command` field with values `view`, `create`, `str_replace`, plus `path`, `file_text`, `old_str`, `new_str` all sitting at the same level as optional-looking siblings. Nothing forces `str_replace` to arrive with **both** `old_str` and `new_str`, or `create` to arrive with `file_text`. Every half-filled call is rejected, wastes a turn, and burns tokens — the model is being punished for your schema, not for its reasoning. Compare the flat `action` enum (`read`/`write`/`edit`/`list`/`grep`) in the README's version, which pairs each action with its own named fields.

**What to do**

1. Make required fields explicit per action, so an invalid call is impossible to express rather than merely discouraged.
2. Classify every rejected call: unknown tool, missing required field, bad enum value, bash syntax error. The top three shapes tell you what to fix.
3. Allow one self-repair attempt with the error text fed back, then give up and log it.
4. Report tool error rate next to Pass@1, never merged into it — a 45% Pass@1 with a 2% error rate is a different problem from 45% with 22%.
5. Use the trajectory log (`toolsUsed`, `log`) to prove which tools were touched.

**Verify**

Log all rejected tool calls for one week. Each of the top three error shapes should have a matching schema change, after which the rate drops under 5% and average turns per task falls with it.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: README.md, minimal-benchmark-harness.md.*