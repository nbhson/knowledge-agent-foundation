# ❓ FAQ — Automation (Real Stories, Plain Language)

If a question is unclear, read the section in `../README.md` (named in brackets).

> How to read this file: each question is a real failure story. **What you see** = the symptom, **Why** = the cause, **What to do** = the fix, **Verify** = how to prove the fix works.

---

## Q1. Our continuous integration run takes 32 minutes and people stopped reading it — is that a real problem? [→ §9 Anti-Patterns & Solutions, Best Practices]

This section explains why a slow CI pipeline stops being useful, and how to make checks fast enough that people actually read them.

**What you see**

CI = continuous integration = the automated checks (build, lint, tests) that run on every push. The check on your pull request goes red after a long coffee break. Nobody opens the log; people push again and hope. After two weeks the whole team merges without looking, and a broken build sits on `main` (the main branch of the repo) overnight. The source calls this anti-pattern 5, word for word: "CI takes 30+ minutes → developers ignore results".

**Why**

Human attention is the bottleneck, not the machine. A check that arrives after the decision has already been made is decoration. Anti-pattern 6 (tests that fail at random, so-called *flaky* tests) and anti-pattern 7 (deploy succeeds but the service is degraded) feed the same failure from the other side.

**What to do**

1. Run the cheapest check first and gate on it (gate = the step must pass before the next step runs): `ruff check .` (a fast Python linter — a tool that flags bad code style and obvious mistakes) → `mypy src/` (a static type checker — it finds type errors without running the code) → `pytest tests/unit/ --cov=src/ --cov-fail-under=80` (unit tests, and fail if code coverage — the share of code the tests touch — is under 80%). A lint error must surface in under a minute.
2. Split the work into separate jobs chained with `needs:` (a GitHub Actions keyword meaning "this job starts only after the named jobs finish") so they run in parallel, not in one queue. The five-stage workflow in §2.2 does exactly this.
3. Install dependencies once with `pip install -e ".[dev]"` (installs the package itself plus its `dev` extra packages, in editable mode) and cache them; do not reinstall from scratch in every job.
4. Quarantine flaky tests instead of re-running until green. A test that needs a second chance is a broken test.
5. Hold the line on the numbers the module gives you: under 10 minutes for CI, under 30 for delivery to production.

> 📄 **Example code:** [`examples/01-q1-our-continuous-integration-run-takes-32-minutes.yaml`](examples/01-q1-our-continuous-integration-run-takes-32-minutes.yaml)

**Verify**

Time the run from push to result and review pipeline metrics every week. Then ask a teammate to predict the CI outcome from the diff alone (the diff = the list of changed lines). If they cannot, the signal arrives too late to matter.

> **One-line summary:** A CI pipeline slower than ~10 minutes gets ignored, so order checks cheapest-first, parallelize jobs, cache installs, and quarantine flaky tests.

---

## Q2. The pipeline went green but the app was broken for 20 minutes — why did nobody notice? [→ §15.1 Common Anti-Patterns, §5.2 Monitoring System]

This section explains why "pipeline green" does not mean "app healthy", and what monitoring holes hide behind it.

**What you see**

Every job passed, the deploy step printed "Full rollout..." and finished in four seconds, and then users got 502 errors (an HTTP error meaning the server behind the gateway is failing) for twenty minutes. The source calls this anti-pattern 2: "pipeline reports success but deploy is broken".

**Why**

A pipeline can only see a process exit code (the number a program returns when it ends; 0 usually means "ok"). It cannot see that the new pods (the smallest deployable units in Kubernetes) crash-loop, that a database migration renamed a column the API still reads, or that `/health` returns 200 with an error body inside it. The monitoring layer was supposed to catch that, and it has two specific holes in the sample code:

- The alert rule declares `cooldown_seconds: int = 300`, but `_check_alerts()` never reads it. So the same alert re-fires on **every** data point — 300 seconds of quiet between alerts is promised but never delivered. This is alert fatigue, the last anti-pattern in §15.1: too many alerts, so people mute them.
- `get_metric_stats()` computes p95 (the 95th percentile — 95 out of 100 requests were faster than this number) only when there are 20 or more points. Below 20 it silently returns `max(values)` (the single worst value), so a dashboard shows the worst spike of the day as if it were the typical value.

**What to do**

1. Make post-deploy verification a real gate, not a comment: `sleep 30` (wait 30 seconds for the service to warm up) then `curl -f https://staging.example.com/health || exit 1` (`curl -f` fails the command if the server returns an error; `|| exit 1` means "if curl failed, fail this job too"). If that fails, the job fails.
2. Emit a `deploy_id` (a unique label for each deploy) on every deploy and join it to your metrics and logs, so a trigger can tell "errors went up" apart from "errors went up *after this deploy*".
3. Fix the cooldown bug and the p95 bug before you trust the dashboard. Add severity levels (info / warning / critical) and a runbook link (a step-by-step page for handling the alert) to every alert.
4. Watch error rate and p95 latency for the first minutes after every deploy.

**Verify**

Ship a deliberately broken build to staging (a pre-production environment). The pipeline must turn red on its own. Then confirm the alert fired once, not three hundred times, and that the dashboard reports a typical value rather than a maximum.

> **One-line summary:** A green pipeline only proves the process exited, so add a real post-deploy health check, tag deploys with an id, and fix the cooldown and p95 bugs before trusting alerts.

---

## Q3. We released at 4pm and error rate went from 0.2% to 6% — how do we undo it in under a minute? [→ §17.1 Deploy Safety, §6.1 Self-Healing Patterns]

This section explains how to make a deploy reversible in advance, so a bad release can be undone in seconds, not hours.

**What you see**

A release goes out at 16:12. Five minutes later p99 latency (the speed of the slowest 1 request in 100) jumps from 300ms to 4 seconds, and the error rate goes from 0.2% to 6%. Forty people appear in Slack. Nobody can say which image tag (the version label of the deployed build) was running before. Anti-pattern 4 again: "deploy fails, no way to revert".

**Why**

A deploy is only reversible if reversibility was built in. The old version is almost certainly still running — nobody wrote down which one it was, and nobody decided in advance what "bad" means. Deciding during the incident is how 4pm becomes 2am.

**What to do**

1. Roll out in measured stages and let metrics gate each one: 5% of users for 10 minutes → 25% for 30 minutes → 50% for 30 minutes → 100%.
2. At every stage, require all of: error rate up less than 0.5 percentage points versus baseline (the value measured before the change), p95 latency up less than 10%, smoke tests 100% passing (smoke tests = a small set of checks that prove the service basically works), and no severity-0 or severity-1 alerts firing (the two most urgent alert levels).
3. Bind the rollback (going back to the previous version) to metrics, not to a human. Auto-rollback fires when error rate is above 2% for 3 minutes, when p99 exceeds the service level objective for 5 minutes (SLO = the performance target you promised users), when a smoke test fails, or when someone adds a `halt` label to the deploy pull request.
4. Keep database migrations backward compatible using expand → migrate → contract: first add the new column while keeping the old one (expand), then copy data and switch code (migrate), and only remove the old column later (contract). That way the old code can still run against the new schema.

> 📄 **Example code:** [`examples/02-q3-we-released-at-4pm-and-error-rate.py`](examples/02-q3-we-released-at-4pm-and-error-rate.py)

**Verify**

Run a game day once a month (a rehearsal where you break things on purpose): deliberately break a deploy in staging, confirm the rollback fires on its own and lands on the previous known-good version. A rollback path that has never been exercised is a hope, not a plan.

> **One-line summary:** A deploy is only undoable in under a minute if you staged the rollout, defined "bad" as metrics in advance, and wired auto-rollback to those metrics.

---

## Q4. My nightly job ran three times at once and a stuck job from Friday was still running on Monday — how do I stop that? [→ §17.4 Scheduled-Task Idempotency, §7.1 Task Scheduler]

This section explains why cron-style schedules can start duplicate and stuck jobs, and how to make each run happen exactly once.

**What you see**

The `nightly-e2e` task starts at 02:00 and finishes at 02:40. On a slow night the scheduler fires again at 02:00 while the first copy is still going, and later a retry starts a third. A migration job gets stuck on Friday and is still running Monday. One backup wrote a half-finished file that nobody noticed.

**Why**

A cron entry (a time-based schedule, e.g. "run daily at 02:00") only says "run at 02:00". It does not say "run once per window", it does not stop a second copy while the first is alive, and it does not stop itself. The sample scheduler has the same gap: it recomputes the next run from `now` (`now + timedelta(days=1)`), so every delay pushes the next run later and a daily job drifts hours over a few months.

**What to do**

1. Give every run an idempotency key — a value that makes repeating the same work harmless, like a "this window was already done" receipt: `task_name + window_start`, for example `nightly-e2e#2026-09-28`. Check a dedup store (a small database of keys already processed) before acting, and key the side effects on the same value.
2. Set `concurrencyPolicy: Forbid` (a Kubernetes CronJob option: skip the new run if the previous one is still going) for deploys and migrations. Use `Replace` (kill the old run and start fresh) only for cheap read-only syncs.
3. Cap the run with `activeDeadlineSeconds` (kill the job after this many seconds) and `startingDeadlineSeconds` (skip the run if its start window was missed by more than this), so a stuck job is killed and a missed window does not pile up.
4. Set `failedJobsHistoryLimit=3` (keep at most 3 failed-run records for debugging), and backfill a missed window (run it later for a past time slot) only when it is explicitly marked `backfill: true`.
5. Watch `run_count` and `failure_count` from the scheduler report — a rising failure count is the early warning.

> 📄 **Example code:** [`examples/03-q4-my-nightly-job-ran-three-times-at.yaml`](examples/03-q4-my-nightly-job-ran-three-times-at.yaml)

**Verify**

Fire the same window twice on purpose: the handler body must execute once. Then force a job to hang and confirm it is killed at its deadline instead of surviving into the next day.

> **One-line summary:** Schedules alone cannot prevent duplicates — use an idempotency key per window, forbid concurrent runs, and cap every run with a hard deadline.

---

## Q5. The self-healing agent retried for ten hours and the API bill jumped by $312 — where is the brake? [→ §17.3 Autonomous Loop Guards, §17.2 Secrets & Config Management]

This section explains why an automated retry loop needs an explicit budget and how to keep secrets out of its logs.

**What you see**

An agent keeps "fixing" one failing test, committing each time. Ten hours later the invoice is up $312, the repository has 400 commits, and the test still fails. In the same window someone notices a key that starts with `sk-` (an OpenAI API key — whoever holds it can spend your money) sitting in an agent transcript and in the CI log.

**Why**

Self-healing without a budget has no stop condition. The `SelfHealingSystem` in §6.2 does bound things — `max_failures = 5`, `circuit_open_duration = 60` seconds (the circuit breaker: after repeated failures it stops calling the service for 60s, like an electrical fuse), states `CLOSED` / `OPEN` / `HALF_OPEN` — but that protects the **service**, not the **agent loop**. Separately, secrets placed in a repo, a UI, or a transcript are readable by every future run and every log reader.

**What to do**

1. Give every agent or self-healing loop an explicit budget: `LoopBudget { maxIterations=10, maxCostUSD=5, maxLatencyMs=300_000, maxToolCalls=50 }` — stop after 10 attempts, $5, 5 minutes, or 50 tool calls, whichever comes first.
2. Exit the loop on the first of three conditions: success, budget exhausted, or a confidence plateau — three rounds with no improvement.
3. On exhaustion, freeze the work and open an incident (a tracked ticket with the full history) with the full trace. Never silently retry; that is exactly how a $5 budget becomes a $312 bill.
4. Print the live counters (iteration, cost, latency) into the logs and the CI summary so the brake is visible before it fires.
5. Keep secrets in a vault or cloud secret manager only — never in the repo, never in a UI-only config, never in an agent transcript. Scope per environment and per service, lease short-lived credentials instead of long-lived production keys, rotate every 30–90 days and immediately after an incident, and mask values in CI logs.

**Verify**

Run the loop against a deliberately impossible task and confirm it stops at the budget, files an incident, and shows the three counters in the summary. Then grep the logs and transcripts for `sk-`, `ghp_` (a GitHub token prefix), `AKIA` (an AWS key prefix) and confirm every match comes back masked (replaced with `***`).

> **One-line summary:** An agent loop without a budget retries forever and leaks keys — cap iterations, cost, and time, escalate on exhaustion, and keep secrets in a vault, never in logs.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: README.md.*
