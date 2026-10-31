# 🧹 CI Sweeper Loop

**Goal**: React quickly to CI failures on main or active branches — diagnose, propose minimal fixes, and escalate when the loop isn't confident enough to resolve it. (CI = continuous integration, the automated build-and-test system; escalate = hand the problem to a human.)

## Scheduling

Signpost: this section answers "how often does the loop check?" — high frequency is the point here, but it costs money.

**Recommended**:
- `/loop 15m` during active development (Grok, Claude Code)
- `/loop 5m` when main is red and you're shipping (red = tests are failing)
- GitHub Action on `workflow_run` failures (event-driven, better than polling) (event-driven = triggered by the failure event itself, rather than checking on a timer; polling = checking repeatedly on a schedule)

A slower overnight cadence (30–60m) is also fine when nobody is watching.

> **One-line summary:** Every 15 minutes normally, every 5 when main is red — or trigger straight off the failure event.

## Required Skills

Signpost: this section lists the knowledge files the loop loads — each skill covers one job.

- `ci-triage` — Parses CI logs, identifies the failing job/step, classifies failure type (flake, regression, env, config) (flake = a test that fails randomly without a real bug; regression = something that used to work now broken; env = environment problem, e.g. a missing dependency)
- `minimal-fix` — The smallest change that resolves the specific failure
- `loop-guard` — Circuit breaker: logs every attempt to `loop-ledger.json`; escalates instead of looping on the same failure (circuit breaker = cut off after repeated failures, like a fuse)
- Project test/lint skill — Build + test commands for your stack (lint = a code-style checker)

> **One-line summary:** Four skills: classify the failure, draft the minimal fix, guard the loop, and know your build/test commands.

## State

Signpost: this section defines the loop's memory — what it records so the next run and the team know what's in progress.

`ci-sweeper-state.md` or a section in `STATE.md`:

```markdown
## CI Sweeper — Active Failures

Last run: 2026-06-09 14:30 UTC

### main @ abc1234
- Job: test-auth
- Failure: AssertionError in test_refresh_token_expiry
- Attempts: 1/3
- Last action: Minimal fix proposed in worktree fix/ci-auth-refresh
- Status: Waiting for verifier + human

### Resolved (last 7d)
- main @ def5678 — lint fix merged via PR #1250
```

(Plain words: `main @ abc1234` = the branch and the exact commit (a commit SHA) that is failing; `Attempts: 1/3` = one fix try used out of the maximum of 3; worktree = an isolated copy of the repo checkout where the fix is drafted.)

Track: commit SHA, failing job, attempt count, worktree/PR link, outcome.

> **One-line summary:** The state records each active failure, its attempt count, and the fix's status — plus recently resolved ones.

## How the Loop Runs (Typical Cycle)

Signpost: this is the walk-through of one run, from spotting failures to proposing fixes or escalating.

1. Discover CI failures on watched branches (main, release/*, active PRs).
2. For each new failure:
   - **Classify**: flake vs real regression vs infra.
   - **If flake** (seen before, intermittent): add to Watch, **do not auto-fix**.
   - **If actionable**: open a worktree → implementer drafts the fix.
3. The verifier sub-agent checks: the fix resolves the failure, no unrelated changes, tests pass locally. (Verifier = a second agent whose only job is to check the first one's work.)
4. Open a PR or comment on the existing PR with the proposed fix. (PR = pull request, a proposed change awaiting review.)
5. Before each retry, `loop-guard` runs the circuit breaker. If the same failure recurs N times or attempts > max (e.g. 3): **trip → escalate** with a pruned context summary. (Pruned = trimmed down to the essentials.)
6. Prune resolved failures from the active list.

> **One-line summary:** Classify each failure, only fix real regressions, verify, and trip the breaker after 3 tries.

## Verification Strategy

Signpost: this section defines what must be true before any fix is accepted.

- The verifier **must** run tests in the worktree before approving.
- The implementer must not merge — only propose. (Merge = incorporate the change into the branch.)
- **Flake detection**: if the same test fails then passes on retry with no code change → do not auto-fix.

> **One-line summary:** Tests must pass in the worktree, the implementer only proposes, and flakes are never auto-fixed.

## Human Handoff Points

Signpost: these are the situations the loop must never handle alone — it stops and asks a person.

- Infrastructure failures (runner OOM, registry down, missing secrets) (OOM = out of memory; registry = the server that stores packages)
- Failures touching > 5 files or core architecture
- Security-sensitive test failures
- Max attempts exceeded on the same failure
- Intermittent flakes that need quarantine, not code changes (quarantine = mark the test as skipped/isolated until fixed, rather than patching around it)

> **One-line summary:** Infra failures, big or security-sensitive changes, repeat failures, and flakes all go to a human.

## Failure Modes & Mitigations

How to read it: left column = what goes wrong in practice; right column = the countermeasure. For instance, "fix-the-symptom loops" = the loop makes CI green without fixing the real bug — the verifier checks root cause, not just a green run.

| Failure | Mitigation |
|---------|------------|
| Fix-the-symptom loops | Verifier checks root cause, not just green CI |
| Fighting flakes with retries | Classify flakes; quarantine or skip with a ticket |
| Token burn on a red main | Pause the loop after N failures; batch fixes |
| Wrong branch targeted | Explicit branch allowlist in the skill (allowlist = "whitelist" — the only branches the loop may touch) |

> **One-line summary:** Root-cause checks, flake classification, failure pauses, and a branch allowlist cover the main failure modes.

## Cost Profile

How to read it: each row is a scenario and its token cost per run (tokens = AI compute units). The "no-op" row is mandatory: when CI is green, the loop must exit after the cheap check instead of running the full pipeline.

| Scenario | Tokens/run | Notes |
|----------|------------|-------|
| No-op (CI green) | ~5k | **Required** — don't run the full sweeper when green |
| Triage / classify | ~50k | Log parsing + failure classification |
| Fix attempt (L2) | ~200k | Worktree + implementer + verifier |

**Cadence**: 5–15m · **Tier**: very-high · **Suggested daily cap**: 1M tokens · **Early exit required**

> 📄 **Example code:** [`examples/01-cost-profile.sh`](examples/01-cost-profile.sh)

> ⚠️ At a 15m cadence without early-exit, worst-case spend exceeds 5M tokens/day. Never run full action paths on every tick.

> **One-line summary:** ~5k green, ~50k to triage, ~200k per fix attempt — capped at 1M tokens/day, and early exit is mandatory.

## Success Metrics

Signpost: these numbers tell you whether the loop is helping or just burning budget.

- Mean time to the first proposed fix after CI goes red
- % of failures resolved without human intervention (trivial cases only)
- Repeat failure rate (the same job failing again within 48h)

> **One-line summary:** Success = fast first fix proposal, high no-human rate on trivial cases, low repeat failures.

> **Best entry loop** for teams new to loop engineering — high frequency, bounded scope, clear verification.

> **One-line summary:** A high-frequency loop that classifies CI failures, proposes only minimal fixes through a verifier, and escalates flakes, infra issues, and repeat failures to humans — with strict cost caps.

---

*Back to [02 — Seven Production Patterns](../02-patterns/)*