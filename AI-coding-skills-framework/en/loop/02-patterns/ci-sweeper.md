# 🧹 CI Sweeper Loop

**Goal**: React quickly to CI failures on main or active branches — diagnose, propose minimal fixes, and escalate when the loop isn't confident enough to resolve it.

## Scheduling

**Recommended**:
- `/loop 15m` during active development (Grok, Claude Code)
- `/loop 5m` when main is red and you're shipping
- GitHub Action on `workflow_run` failures (event-driven, better than polling)

A slower overnight cadence (30–60m) is also fine when nobody is watching.

## Required Skills

- `ci-triage` — Parses CI logs, identifies the failing job/step, classifies failure type (flake, regression, env, config)
- `minimal-fix` — The smallest change that resolves the specific failure
- `loop-guard` — Circuit breaker: logs every attempt to `loop-ledger.json`; escalates instead of looping on the same failure
- Project test/lint skill — Build + test commands for your stack

## State

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

Track: commit SHA, failing job, attempt count, worktree/PR link, outcome.

## How the Loop Runs (Typical Cycle)

1. Discover CI failures on watched branches (main, release/*, active PRs).
2. For each new failure:
   - **Classify**: flake vs real regression vs infra.
   - **If flake** (seen before, intermittent): add to Watch, **do not auto-fix**.
   - **If actionable**: open a worktree → implementer drafts the fix.
3. The verifier sub-agent checks: the fix resolves the failure, no unrelated changes, tests pass locally.
4. Open a PR or comment on the existing PR with the proposed fix.
5. Before each retry, `loop-guard` runs the circuit breaker. If the same failure recurs N times or attempts > max (e.g. 3): **trip → escalate** with a pruned context summary.
6. Prune resolved failures from the active list.

## Verification Strategy

- The verifier **must** run tests in the worktree before approving.
- The implementer must not merge — only propose.
- **Flake detection**: if the same test fails then passes on retry with no code change → do not auto-fix.

## Human Handoff Points

- Infrastructure failures (runner OOM, registry down, missing secrets)
- Failures touching > 5 files or core architecture
- Security-sensitive test failures
- Max attempts exceeded on the same failure
- Intermittent flakes that need quarantine, not code changes

## Failure Modes & Mitigations

| Failure | Mitigation |
|---------|------------|
| Fix-the-symptom loops | Verifier checks root cause, not just green CI |
| Fighting flakes with retries | Classify flakes; quarantine or skip with a ticket |
| Token burn on a red main | Pause the loop after N failures; batch fixes |
| Wrong branch targeted | Explicit branch allowlist in the skill |

## Cost Profile

| Scenario | Tokens/run | Notes |
|----------|------------|-------|
| No-op (CI green) | ~5k | **Required** — don't run the full sweeper when green |
| Triage / classify | ~50k | Log parsing + failure classification |
| Fix attempt (L2) | ~200k | Worktree + implementer + verifier |

**Cadence**: 5–15m · **Tier**: very-high · **Suggested daily cap**: 1M tokens · **Early exit required**

```bash
npx @cobusgreyling/loop cost --pattern ci-sweeper --cadence 15m --level L2
```

> ⚠️ At a 15m cadence without early-exit, worst-case spend exceeds 5M tokens/day. Never run full action paths on every tick.

## Success Metrics

- Mean time to the first proposed fix after CI goes red
- % of failures resolved without human intervention (trivial cases only)
- Repeat failure rate (the same job failing again within 48h)

> **Best entry loop** for teams new to loop engineering — high frequency, bounded scope, clear verification.

---

*Back to [02 — Seven Production Patterns](../02-patterns/)*
