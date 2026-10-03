# ❓ FAQ — Automation (Real Stories, Plain Language)

If a question is unclear, read the section in `../README.md` (named in brackets).

---

## Q1. Our continuous integration run takes 32 minutes and people stopped reading it — is that a real problem? [→ §9 Anti-Patterns & Solutions, Best Practices]

**What you see**

The check on your pull request goes red after a long coffee break. Nobody opens the log; people push again and hope. After two weeks the whole team merges without looking, and a broken build sits on `main` overnight. The source calls this anti-pattern 5, word for word: "CI takes 30+ minutes → developers ignore results".

**Why**

Human attention is the bottleneck, not the machine. A check that arrives after the decision has already been made is decoration. Anti-pattern 6 (tests that fail at random) and anti-pattern 7 (deploy succeeds but the service is degraded) feed the same failure from the other side.

**What to do**

1. Run the cheapest check first and gate on it: `ruff check .` → `mypy src/` → `pytest tests/unit/ --cov=src/ --cov-fail-under=80`. A lint error must surface in under a minute.
2. Split the work into separate jobs chained with `needs:` so they run in parallel, not in one queue. The five-stage workflow in §2.2 does exactly this.
3. Install dependencies once with `pip install -e ".[dev]"` and cache them; do not reinstall from scratch in every job.
4. Quarantine flaky tests instead of re-running until green. A test that needs a second chance is a broken test.
5. Hold the line on the numbers the module gives you: under 10 minutes for CI, under 30 for delivery to production.

```yaml
jobs:
  lint-and-type-check: { runs-on: ubuntu-latest }
  unit-tests:
    needs: lint-and-type-check
    strategy: { matrix: { python-version: ['3.10','3.11','3.12'] } }
```

**Verify**

Time the run from push to result and review pipeline metrics every week. Then ask a teammate to predict the CI outcome from the diff alone — if they cannot, the signal arrives too late to matter.

---

## Q2. The pipeline went green but the app was broken for 20 minutes — why did nobody notice? [→ §15.1 Common Anti-Patterns, §5.2 Monitoring System]

**What you see**

Every job passed, the deploy step printed "Full rollout..." and finished in four seconds, and then users got 502 errors for twenty minutes. The source calls this anti-pattern 2: "pipeline reports success but deploy is broken".

**Why**

A pipeline can only see a process exit code. It cannot see that the new pods crash-loop, that a database migration renamed a column the API still reads, or that `/health` returns 200 with an error body inside it. The monitoring layer was supposed to catch that, and it has two specific holes in the sample code:

- The alert rule declares `cooldown_seconds: int = 300`, but `_check_alerts()` never reads it. The rule therefore re-fires on **every** data point — this is alert fatigue, the last anti-pattern in §15.1.
- `get_metric_stats()` computes p95 only when there are 20 or more points. Below 20 it silently returns `max(values)`, so a dashboard shows the worst spike of the day as if it were the typical value.

**What to do**

1. Make post-deploy verification a real gate, not a comment: `sleep 30` then `curl -f https://staging.example.com/health || exit 1`. If that fails, the job fails.
2. Emit a `deploy_id` on every deploy and join it to your metrics and logs, so a trigger can tell "errors went up" apart from "errors went up *after this deploy*".
3. Fix the cooldown bug and the p95 bug before you trust the dashboard. Add severity levels (info / warning / critical) and a runbook link to every alert.
4. Watch error rate and p95 latency — p95 means 95 out of 100 requests were faster than this number — for the first minutes after every deploy.

**Verify**

Ship a deliberately broken build to staging. The pipeline must turn red on its own. Then confirm the alert fired once, not three hundred times, and that the dashboard reports a typical value rather than a maximum.

---

## Q3. We released at 4pm and error rate went from 0.2% to 6% — how do we undo it in under a minute? [→ §17.1 Deploy Safety, §6.1 Self-Healing Patterns]

**What you see**

A release goes out at 16:12. Five minutes later p99 latency (the speed of the slowest 1 request in 100) jumps from 300ms to 4 seconds, and the error rate goes from 0.2% to 6%. Forty people appear in Slack. Nobody can say which image tag was running before. Anti-pattern 4 again: "deploy fails, no way to revert".

**Why**

A deploy is only reversible if reversibility was built in. The old version is almost certainly still running — nobody wrote down which one it was, and nobody decided in advance what "bad" means. Deciding during the incident is how 4pm becomes 2am.

**What to do**

1. Roll out in measured stages and let metrics gate each one: 5% for 10 minutes → 25% for 30 minutes → 50% for 30 minutes → 100%.
2. At every stage, require all of: error rate up less than 0.5 percentage points versus baseline, p95 latency up less than 10%, smoke tests 100% passing, and no severity-0 or severity-1 alerts firing.
3. Bind the rollback to metrics, not to a human. Auto-rollback fires when error rate is above 2% for 3 minutes, when p99 exceeds the service level objective for 5 minutes, when a smoke test fails, or when someone adds a `halt` label to the deploy pull request.
4. Keep database migrations backward compatible using expand → migrate → contract, so the old code can still run against the new schema.

```python
def decide(baseline: dict, canary: dict) -> str:
    err_delta = canary["error_rate"] - baseline["error_rate"]
    lat_delta = (canary["p99_ms"] - baseline["p99_ms"]) / max(baseline["p99_ms"], 1)
    if canary["smoke_failures"] > 0 or canary["sev1_firing"]:
        return "ROLLBACK: smoke/sev1"
    if canary["error_rate"] > 0.02 or err_delta > 0.005:
        return f"ROLLBACK: error_rate delta={err_delta:+.3f}"
    return "PROMOTE"
```

**Verify**

Run a game day once a month: deliberately break a deploy in staging, confirm the rollback fires on its own and lands on the previous known-good version. A rollback path that has never been exercised is a hope, not a plan.

---

## Q4. My nightly job ran three times at once and a stuck job from Friday was still running on Monday — how do I stop that? [→ §17.4 Scheduled-Task Idempotency, §7.1 Task Scheduler]

**What you see**

The `nightly-e2e` task starts at 02:00 and finishes at 02:40. On a slow night the scheduler fires again at 02:00 while the first copy is still going, and later a retry starts a third. A migration job gets stuck on Friday and is still running Monday. One backup wrote a half-finished file that nobody noticed.

**Why**

A cron entry only says "run at 02:00". It does not say "run once per window", it does not stop a second copy while the first is alive, and it does not stop itself. The sample scheduler has the same gap: it recomputes the next run from `now` (`now + timedelta(days=1)`), so every delay pushes the next run later and a daily job drifts hours over a few months.

**What to do**

1. Give every run an idempotency key — a value that makes repeating the same work harmless: `task_name + window_start`, for example `nightly-e2e#2026-09-28`. Check a dedup store before acting, and key the side effects on the same value.
2. Set `concurrencyPolicy: Forbid` for deploys and migrations (skip if the previous run is still going). Use `Replace` only for cheap read-only syncs.
3. Cap the run with `activeDeadlineSeconds` and `startingDeadlineSeconds`, so a stuck job is killed and a missed window does not pile up.
4. Set `failedJobsHistoryLimit=3`, and backfill a missed window only when it is explicitly marked `backfill: true`.
5. Watch `run_count` and `failure_count` from the scheduler report — a rising failure count is the early warning.

```yaml
concurrencyPolicy: Forbid
activeDeadlineSeconds: 3600
startingDeadlineSeconds: 300
failedJobsHistoryLimit: 3
```

**Verify**

Fire the same window twice on purpose: the handler body must execute once. Then force a job to hang and confirm it is killed at its deadline instead of surviving into the next day.

---

## Q5. The self-healing agent retried for ten hours and the API bill jumped by $312 — where is the brake? [→ §17.3 Autonomous Loop Guards, §17.2 Secrets & Config Management]

**What you see**

An agent keeps "fixing" one failing test, committing each time. Ten hours later the invoice is up $312, the repository has 400 commits, and the test still fails. In the same window someone notices a key that starts with `sk-` sitting in an agent transcript and in the CI log.

**Why**

Self-healing without a budget has no stop condition. The `SelfHealingSystem` in §6.2 does bound things — `max_failures = 5`, `circuit_open_duration = 60` seconds, states `CLOSED` / `OPEN` / `HALF_OPEN` — but that protects the **service**, not the **agent loop**. Separately, secrets placed in a repo, a UI, or a transcript are readable by every future run and every log reader.

**What to do**

1. Give every agent or self-healing loop an explicit budget: `LoopBudget { maxIterations=10, maxCostUSD=5, maxLatencyMs=300_000, maxToolCalls=50 }`.
2. Exit the loop on the first of three conditions: success, budget exhausted, or a confidence plateau — three rounds with no improvement.
3. On exhaustion, freeze the work and open an incident with the full trace. Never silently retry; that is exactly how a $5 budget becomes a $312 bill.
4. Print the live counters (iteration, cost, latency) into the logs and the CI summary so the brake is visible before it fires.
5. Keep secrets in a vault or cloud secret manager only — never in the repo, never in a UI-only config, never in an agent transcript. Scope per environment and per service, lease short-lived credentials instead of long-lived production keys, rotate every 30–90 days and immediately after an incident, and mask values in CI logs.

**Verify**

Run the loop against a deliberately impossible task and confirm it stops at the budget, files an incident, and shows the three counters in the summary. Then grep the logs and transcripts for `sk-`, `ghp_`, `AKIA` and confirm every match comes back masked.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: README.md.*
