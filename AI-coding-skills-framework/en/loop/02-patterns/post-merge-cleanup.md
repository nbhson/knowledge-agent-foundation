# 🧹 Post-Merge Cleanup Loop

**Goal**: Clean up TODOs, cruft, and merge debt after merges — keep the repo tidy without touching important work in progress.

## Scheduling

**Recommended**:
- `/loop 1d–6h` in **off-peak** hours (e.g. `22:00`, weekends)
- Don't run concurrently with PR Babysitter (Post-Merge runs off-peak only)

## Required Skills

- `merge-cleanup` — Reads recent merges, finds TODOs/FIXMEs, dead code, leftover branches
- `minimal-fix` — Small fixes only

## State

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

## How the Loop Runs (Typical Cycle)

1. Read recent merges + `git log`.
2. Find new TODO/FIXMEs, dead code, and branches going stale after merges.
3. For small, clear cleanups: worktree → implementer → verifier → PR.
4. For ambiguous items: record in the backlog, flag for humans.
5. Prune resolved items.

## Verification Strategy

- Small fixes only — no refactors, no behavior changes.
- The verifier checks for the "smallest possible diff" — no touching unrelated files.
- Off-peak — don't touch release/maintenance windows.

## Human Handoff Points

- Cleanups that require behavior changes or > N files
- Deleting dead code that isn't certain to be unused
- Branches that need force-delete

## Failure Modes & Mitigations

| Failure | Mitigation |
|---------|------------|
| Cleanup touches working code | Verifier checks behavior is unchanged; small fixes only |
| TODO cleanup breaks logic | Only remove a TODO when the context is clear; human gate |
| Runs at the wrong time | Off-peak scheduling mandatory |

## Cost Profile

| Scenario | Tokens/run | Notes |
|----------|------------|-------|
| No-op | ~5k | No cleanup needed |
| Cleanup (L1→L2) | ~100k | Scan merges + small fixes |

**Cadence**: 1d–6h off-peak · **Tier**: low · **Suggested daily cap**: 200k tokens

```bash
npx @cobusgreyling/loop cost --pattern post-merge-cleanup --cadence 1d --level L1
```

## Success Metrics

- New TODO/FIXME count per day (downward trend = cleanup is working)
- % of cleanups merged without rework
- Repo "cleanliness" score (fewer stale branches, dead code)

---

*Back to [02 — Seven Production Patterns](../02-patterns/)*
