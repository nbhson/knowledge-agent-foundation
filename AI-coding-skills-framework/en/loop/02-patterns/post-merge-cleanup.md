# 🧹 Post-Merge Cleanup Loop

**Goal**: Clean up TODOs, cruft, and merge debt after merges — keep the repo tidy without touching important work in progress.
(Glossary: a **TODO/FIXME** = a note a developer left in the code, e.g. `// TODO: remove debug log`. **Cruft** = leftover clutter — dead code, unused imports. **Merge debt** = small mess a merged PR (a proposed code change) left behind: stray branches, leftover notes.)

## Scheduling

Signpost: this section says when the loop should run — timing matters because it edits code.

**Recommended**:
- `/loop 1d–6h` in **off-peak** hours (e.g. `22:00`, weekends) — off-peak = times when nobody is actively developing, so a bad change disturbs fewer people
- Don't run concurrently with PR Babysitter (Post-Merge runs off-peak only) — two loops editing at once can overwrite each other

> **One-line summary:** Run it daily or every few hours, at night or on weekends, and never at the same time as the PR Babysitter.

## Required Skills

Signpost: each loop is built from small named skills. Here is what this one needs and why.

- `merge-cleanup` — Reads recent merges, finds TODOs/FIXMEs, dead code, leftover branches (dead code = code nothing calls anymore; leftover branches = git branches that should have been deleted after their PR merged)
- `minimal-fix` — Small fixes only

> **One-line summary:** One skill scans recent merges for leftovers; the other makes only small, safe fixes.

## State

Signpost: the loop keeps a small markdown file as its memory between runs. This is what it looks like.

`post-merge-state.md`:

```markdown
# Post-Merge Cleanup State

Last run: 2026-06-09 22:00 UTC

## Cleanup Backlog
- [ ] PR #1255 left a TODO in `auth/service.py` (3 TODOs)
  Loop action: Draft fix proposed. Waiting on human review.
- [ ] Branch fix/ci-auth-refresh not deleted after merge
  Loop action: Suggest delete.

## Resolved (last 7d)
- PR #1240 — cleanup logs merged
```

How to read it: the "Cleanup Backlog" is the to-do list; "Resolved" is what was already finished in the last 7 days. For instance, the first item means PR #1255 left three TODO notes in `auth/service.py`; the loop drafted a fix but is waiting for a human to review it. The second means a git branch was left behind after its merge, and the loop suggests deleting it.

> **One-line summary:** The state file lists what needs cleaning, what the loop proposes, and what is already done.

## How the Loop Runs (Typical Cycle)

Signpost: this is one full pass of the loop, from reading recent merges to cleaning up.

1. Read recent merges + `git log` (`git log` = the command that shows the repository's commit history).
2. Find new TODO/FIXMEs, dead code, and branches going stale after merges.
3. For small, clear cleanups: worktree → implementer → verifier → PR (worktree = a separate git copy of the repo so the agent never touches your main checkout; implementer = the agent that writes the fix; verifier = a separate agent that tests it).
4. For ambiguous items: record in the backlog, flag for humans.
5. Prune resolved items (prune = delete finished entries so the list stays short).

> **One-line summary:** Scan recent merges for leftovers, fix the small clear ones, flag the rest for humans.

## Verification Strategy

Signpost: how the loop proves a cleanup is safe before opening a PR.

- Small fixes only — no refactors, no behavior changes (refactor = restructuring code without changing what it does — still too big for this loop).
- The verifier checks for the "smallest possible diff" — no touching unrelated files (diff = the set of changed lines in a change).
- Off-peak — don't touch release/maintenance windows.

> **One-line summary:** Tiny changes only, verified to touch nothing extra, run when nobody else is working.

## Human Handoff Points

Signpost: the situations where the loop must stop and ask a person.

- Cleanups that require behavior changes or > N files (behavior change = the program would act differently, not just read differently)
- Deleting dead code that isn't certain to be unused
- Branches that need force-delete (force-delete = `git push --force`-style removal that skips safety checks — risky, so a human decides)

> **One-line summary:** Anything big, uncertain, or destructive goes to a human.

## Failure Modes & Mitigations

How to read it: "Failure" = what can go wrong; "Mitigation" = the guard that prevents it. For instance, the first row: cleanup could break working code, so the verifier checks behavior is unchanged and only small fixes are allowed.

| Failure | Mitigation |
|---------|------------|
| Cleanup touches working code | Verifier checks behavior is unchanged; small fixes only |
| TODO cleanup breaks logic | Only remove a TODO when the context is clear; human gate (gate = a mandatory approval stop) |
| Runs at the wrong time | Off-peak scheduling mandatory |

> **One-line summary:** Guardrails: tiny fixes, human approval for anything uncertain, strict off-peak timing.

## Cost Profile

How to read it: "Scenario" = what kind of run happens; "Tokens/run" = roughly how much model usage one such run costs (tokens = the billing unit of model usage). For instance, "No-op" means the loop woke up, found nothing to clean, and exited — that should cost almost nothing.

| Scenario | Tokens/run | Notes |
|----------|------------|-------|
| No-op | ~5k | No cleanup needed |
| Cleanup (L1→L2) | ~100k | Scan merges + small fixes (L1→L2 = escalating from report-only to assisted fixing when a task qualifies) |

**Cadence**: 1d–6h off-peak · **Tier**: low · **Suggested daily cap**: 200k tokens (cadence = how often it runs; tier = how much supervision it needs; daily cap = a hard spending limit per day)

> 📄 **Example code:** [`examples/01-cost-profile.sh`](examples/01-cost-profile.sh)

> **One-line summary:** Cheap scans most days; only real cleanup work costs tokens, under a daily cap.

## Success Metrics

Signpost: how you tell, with numbers, that this loop is worth keeping.

- New TODO/FIXME count per day (downward trend = cleanup is working)
- % of cleanups merged without rework (rework = a human had to redo or fix the loop's change)
- Repo "cleanliness" score (fewer stale branches, dead code)

> **One-line summary:** Success = fewer leftovers each day, and cleanups that stick without rework.

---

*Back to [02 — Seven Production Patterns](../02-patterns/)*
