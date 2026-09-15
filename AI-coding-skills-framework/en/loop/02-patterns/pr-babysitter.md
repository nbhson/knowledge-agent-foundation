# 👶 PR Babysitter Loop

**Goal**: Watch PRs awaiting review/CI/rebase, nudge them, and suggest small fixes.

## Scheduling

**Recommended**:
- `/loop 10–15m` during active hours (Grok, Claude Code)
- `/loop 5m` when there are many "stale" PRs and you're shipping
- GitHub Action on `pull_request` events (event-driven)

## Required Skills

- `loop-triage` — Reads PRs, CI checks, review status
- `minimal-fix` — Drafts small fixes for PRs with red CI
- Reviewer sub-agent — verifies proposed fixes (mandatory at L2)

## State

`pr-babysitter-state.md`:

```markdown
# PR Babysitter State

Last run: 2026-06-09 14:30 UTC

## Active PRs
- PR #1250 — fix/ci-auth-refresh — CI: pending — review: 2/3 — stale 4h
  Loop action: Nudge comment sent. Waiting on review.
- PR #1248 — lodash dep bump — CI: red (test-auth)
  Loop action: Worktree opened. Fix proposed. Verifier PASS. Waiting on human.

## Resolved (last 7d)
- PR #1245 — merged 2026-06-08
```

Fields: PR ID, branch, CI status, review count, time stale, last action, worktree/PR link.

## How the Loop Runs (Typical Cycle)

1. Read the list of open PRs on watched branches.
2. For each PR:
   - **Stale** (no activity for > N hours): send a gentle nudge comment.
   - **CI red**: classify the failure → if actionable, worktree + implementer + verifier.
   - **Needs review**: remind reviewers via comment/label.
3. Prune merged/closed PRs from the active list.

## Verification Strategy

- The verifier must run tests in the worktree before approving.
- The implementer only proposes, never merges — **no auto-merge by default**.
- If the verifier REJECTS → clean up the worktree, record the attempt, escalate after max (e.g. 3).

## Human Handoff Points

- Fixes touching > 5 files or core architecture
- Security-sensitive changes
- Max attempts exceeded on the same PR
- Conflicts requiring a human decision (e.g., two valid approaches)

## Failure Modes & Mitigations

| Failure | Mitigation |
|---------|------------|
| Spammy nudge comments | Only nudge when a PR is stale past the threshold; no repeat nudges the same day |
| Fixing the wrong PR | Verifier checks scope; only act on clear PRs |
| Token burn with many PRs | Cap how many active PRs the loop processes per run; early-exit |
| Two loops touching the same PR | `acting_on` in state + `loop-worktree lock` |

## Cost Profile

| Scenario | Tokens/run | Notes |
|----------|------------|-------|
| No-op (all PRs fine) | ~5k | Required — don't run the full chain when there's nothing |
| Watch + nudge (L1) | ~30k | Scan PRs + CI status |
| Fix attempt (L2) | ~200k | Worktree + implementer + verifier |

**Cadence**: 5–15m · **Tier**: high · **Suggested daily cap**: 2M tokens · **Early exit required**

```bash
npx @cobusgreyling/loop cost --pattern pr-babysitter --cadence 10m --level L1
```

## Success Metrics

- Mean time from "PR stale" to "reviewed/nudged"
- % of red-CI PRs resolved without a human (trivial cases only)
- Review turnaround time

---

*Back to [02 — Seven Production Patterns](../02-patterns/)*
