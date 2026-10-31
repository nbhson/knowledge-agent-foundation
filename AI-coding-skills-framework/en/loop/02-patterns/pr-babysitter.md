# 👶 PR Babysitter Loop

**Goal**: Watch PRs awaiting review/CI/rebase, nudge them, and suggest small fixes.
(Glossary: a **PR** (pull request) = a proposed code change waiting to be reviewed and merged. **CI** = the automated build-and-test pipeline; "red CI" = tests failing. **Rebase** = updating a PR branch onto the latest `main` so it can merge cleanly. **Nudge** = a polite reminder comment, e.g. "gentle ping — this PR has been waiting 4h".)

## Scheduling

Signpost: this section says how often the loop should run — this loop checks frequently because PRs move fast.

**Recommended**:
- `/loop 10–15m` during active hours (Grok, Claude Code) — `/loop` = a scheduler command: "run this every 10–15 minutes"
- `/loop 5m` when there are many "stale" PRs and you're shipping (stale = no activity for hours; "shipping" = actively releasing)
- GitHub Action on `pull_request` events (event-driven) (event-driven = the loop runs when something happens, e.g. a new PR, instead of on a timer)

> **One-line summary:** Check every 10–15 minutes while the team works; speed up only during busy shipping weeks.

## Required Skills

Signpost: each loop is built from small named skills. Here is what this one needs and why.

- `loop-triage` — Reads PRs, CI checks, review status
- `minimal-fix` — Drafts small fixes for PRs with red CI
- Reviewer sub-agent — verifies proposed fixes (mandatory at L2) (sub-agent = a helper agent the loop spawns for one task; L2 = the "assisted" level where the loop auto-drafts fixes but always with this verification)

> **One-line summary:** One skill watches PR status, one drafts fixes, and a separate reviewer agent double-checks every draft.

## State

Signpost: the loop keeps a small markdown file as its memory between runs. This is what it looks like.

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
(How to read it: "Active PRs" = PRs still being watched; "Resolved" = finished in the last 7 days. For instance, PR #1250 has pending CI, 2 of 3 needed approvals, has been stale for 4 hours — so the loop sent a nudge comment. PR #1248 has failing tests (`test-auth`), so the loop opened a worktree, proposed a fix, tests passed, and now it waits for a human. A worktree = a separate git copy of the repo so the agent never touches your main checkout.)

> **One-line summary:** The state file tracks every watched PR — its status, what the loop did, and what it is waiting on.

## How the Loop Runs (Typical Cycle)

Signpost: this is one full pass of the loop, from reading PRs to cleaning up.

1. Read the list of open PRs on watched branches.
2. For each PR:
   - **Stale** (no activity for > N hours): send a gentle nudge comment.
   - **CI red**: classify the failure → if actionable, worktree + implementer + verifier (implementer = the agent that writes the fix; verifier = a separate agent that tests it).
   - **Needs review**: remind reviewers via comment/label.
3. Prune merged/closed PRs from the active list (prune = delete finished entries so the list stays short).

> **One-line summary:** The loop watches every open PR and reacts: nudge the stalled ones, fix the red ones, remind slow reviewers.

## Verification Strategy

Signpost: how the loop proves a proposed fix is safe before a human ever sees it.

- The verifier must run tests in the worktree before approving.
- The implementer only proposes, never merges — **no auto-merge by default**.
- If the verifier REJECTS → clean up the worktree, record the attempt, escalate after max (e.g. 3) (escalate = hand the problem to a human).

> **One-line summary:** Every fix is tested in isolation before review, and the loop never merges anything itself.

## Human Handoff Points

Signpost: the situations where the loop must stop and ask a person.

- Fixes touching > 5 files or core architecture
- Security-sensitive changes
- Max attempts exceeded on the same PR
- Conflicts requiring a human decision (e.g., two valid approaches)

> **One-line summary:** Big, sensitive, stuck, or judgment-call situations go to a human.

## Failure Modes & Mitigations

How to read it: "Failure" = what can go wrong; "Mitigation" = the guard that prevents it. For instance, the first row: the loop could spam the team with nudge comments, so it only nudges a PR once per day and only after it is truly stale.

| Failure | Mitigation |
|---------|------------|
| Spammy nudge comments | Only nudge when a PR is stale past the threshold; no repeat nudges the same day |
| Fixing the wrong PR | Verifier checks scope; only act on clear PRs |
| Token burn with many PRs | Cap how many active PRs the loop processes per run; early-exit (early-exit = stop immediately when there is nothing to do) |
| Two loops touching the same PR | `acting_on` in state + `loop-worktree lock` (`acting_on` = a field naming which branch/PR the loop is working on; lock = a shared flag so only one loop proceeds) |

> **One-line summary:** Guardrails: no spam, no wrong targets, capped work per run, and locks against loop collisions.

## Cost Profile

How to read it: "Scenario" = what kind of run happens; "Tokens/run" = roughly how much model usage one such run costs (tokens = the billing unit of model usage). For instance, "No-op" means every PR is fine and the loop exits immediately — that must stay cheap, which is why early exit is required.

| Scenario | Tokens/run | Notes |
|----------|------------|-------|
| No-op (all PRs fine) | ~5k | Required — don't run the full chain when there's nothing |
| Watch + nudge (L1) | ~30k | Scan PRs + CI status (L1 = report-only level) |
| Fix attempt (L2) | ~200k | Worktree + implementer + verifier (L2 = assisted-fix level) |

**Cadence**: 5–15m · **Tier**: high · **Suggested daily cap**: 2M tokens · **Early exit required** (cadence = how often it runs; tier = how much supervision it needs; daily cap = a hard spending limit per day)

> 📄 **Example code:** [`examples/01-cost-profile.sh`](examples/01-cost-profile.sh)

> **One-line summary:** This is the most expensive loop here — it stays affordable only by exiting instantly when all PRs are fine.

## Success Metrics

Signpost: how you tell, with numbers, that this loop is worth keeping.

- Mean time from "PR stale" to "reviewed/nudged"
- % of red-CI PRs resolved without a human (trivial cases only)
- Review turnaround time (turnaround = how long the whole review takes end to end)

> **One-line summary:** Success = stalled PRs get moving again fast, with only trivial fixes automated.

---

*Back to [02 — Seven Production Patterns](../02-patterns/)*
