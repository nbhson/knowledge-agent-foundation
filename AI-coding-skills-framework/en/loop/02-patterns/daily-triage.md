# 📋 Daily Triage Loop

**Goal**: Start every day (or every active window) with a prioritized, actionable picture of what needs attention — without manually checking CI, issues, PRs, and chat.

## Scheduling

**Recommended**:
- `/loop 1d` for morning triage (Grok, Claude Code)
- `/loop 2h` during active sprints for faster signal
- GitHub Action cron `0 8 * * 1-5` for teams without a TUI

Many teams run triage-only first (reporting, no auto-fix) for 1–2 weeks before enabling actions.

## Required Skills

- `loop-triage` — Reads CI, issues, commits, chat; produces prioritized findings (STRICT output format)
- `minimal-fix` (optional, phase 2) — Drafts small fixes for obvious failures
- Reviewer sub-agent or skill (optional, phase 2) — verifies proposed fixes

## State

Use `STATE.md` (or a Linear board view) as the memory spine:

```markdown
# Loop State — Project X

Last run: 2026-06-09 08:15 UTC

## High Priority (loop is handling / waiting on human)
- [ ] #1241 — flaky test in auth flow (CI red on main)
  Loop action: Opened worktree. Fix proposed. Waiting for human PR review.

## Watch List
- PR #1238 open for 4 days without activity.

## Recent Noise (ignored this time)
- Dependabot PRs (separate automation)
```

Fields the loop **must** update every run:
- `Last run` timestamp
- Item status + last action taken
- Human decisions that overrode the loop

## How the Loop Runs (Typical Cycle)

1. Scheduler fires (morning or interval).
2. Triage skill ingests: CI failures (24h), open issues/tickets, recent commits, old STATE.md.
3. High-priority items are appended to state with a suggested next action.
4. (Phase 2) For small bugs: worktree → implementer → verifier.
5. (Phase 3) Connectors update PRs/tickets; ambiguous items are flagged for humans.
6. Prune resolved/merged items from state.
7. Write a **post-run critique**: false positives, repeated items, one adjustment for next time.

## Verification Strategy

- Phase 1 (report-only): Humans read `STATE.md` — no auto-action verification needed.
- Phase 2+: The implementer never marks itself done; the verifier confirms fix scope + tests.
- The triage skill **must not invent architectural work** — signal only.

## Human Handoff Points

- Design decisions or multi-file refactors
- Security, auth, payments, infrastructure
- Items flagged "needs discussion" in triage output
- Anything the loop has surfaced for 3+ days without resolution

## Tool-Specific Notes

**Grok Build TUI**:
```bash
/loop 1d Run the loop-triage skill. Append high-priority items to STATE.md. For obvious small bugfixes only: worktree + minimal-fix + verifier sub-agent (maker/checker). Flag ambiguous items for human review.
```

**Claude Code**:
```bash
/loop 1d Run $loop-triage and update STATE.md. Do not auto-fix in the first week — report only.
```

**Codex**:
- Automations tab: daily prompt calling `$loop-triage`, output into the Triage inbox + `STATE.md`.

**GitHub Actions**:
- `daily-triage.yml` runs on weekdays, updates `STATE.md` + `loop-run-log.md`.

## Failure Modes & Mitigations

| Failure | Mitigation |
|---------|------------|
| Triage produces noise | Tighten skill rules; add a "Noise / Ignore" section |
| State file grows without bound | Prune merged/closed items every run |
| Auto-fixes with wrong priority | Start report-only; add effort/risk gates |
| Missed overnight failures | `fireImmediately: true` or run at start of day + midday |
| Stale critique, never reviewed | Human handoff when the critique accumulates without resolution over N runs |

## Cost Profile

| Scenario | Tokens/run | Notes |
|----------|------------|-------|
| No-op | ~5k | Nothing actionable in state |
| Full triage (L1) | ~50k | CI + issues + commits scan |
| Assisted fix (L2) | ~200k | Worktree + implementer + verifier |

**Cadence**: 1d–2h · **Tier**: low · **Suggested daily cap**: 100k tokens

```bash
npx @cobusgreyling/loop cost --pattern daily-triage --cadence 1d --level L1
```

## Success Metrics

- Time from "something broke" to "humans know"
- % of mornings where `STATE.md` matches what you would have found yourself
- Reduction in ad-hoc "what's on fire?" Slack messages

**Start report-only. Add actions only when triage quality is stable.**

---

*Back to [02 — Seven Production Patterns](../02-patterns/)*
