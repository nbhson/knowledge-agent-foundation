# 📋 Daily Triage Loop

**Goal**: Start every day (or every active window) with a prioritized, actionable picture of what needs attention — without manually checking CI, issues, PRs, and chat. (Triage = sorting items by priority; CI = the automated build-and-test system; PR = pull request, a proposed change awaiting review.)

## Scheduling

Signpost: this section answers "when does the loop run?" — usually once each morning, with an option for faster signal during sprints.

**Recommended**:
- `/loop 1d` for morning triage (Grok, Claude Code)
- `/loop 2h` during active sprints for faster signal (sprint = a short development cycle, typically 1–2 weeks)
- GitHub Action cron `0 8 * * 1-5` for teams without a TUI (cron = the classic time scheduler — this expression means 08:00 on weekdays; TUI = terminal user interface)

Many teams run triage-only first (reporting, no auto-fix) for 1–2 weeks before enabling actions.

> **One-line summary:** Daily in the morning (or every 2h in a sprint); report-only for the first 1–2 weeks.

## Required Skills

Signpost: this section lists the knowledge files the loop loads — each skill covers one job.

- `loop-triage` — Reads CI, issues, commits, chat; produces prioritized findings (STRICT output format) (strict output format = fixed fields and sections, so other tools can read it)
- `minimal-fix` (optional, phase 2) — Drafts small fixes for obvious failures
- Reviewer sub-agent or skill (optional, phase 2) — verifies proposed fixes (sub-agent = a second agent with its own instructions)

> **One-line summary:** One triage skill with a strict output format; fix and reviewer skills come later, in phase 2.

## State

Signpost: this section defines the loop's memory — the file it updates every run, which doubles as the team's daily briefing.

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

(Plain words: *High Priority* = the loop is acting on it or waiting for a person; *Watch List* = monitored but not acted on; *Recent Noise* = deliberately ignored this run; *flaky test* = a test that fails randomly without a real bug; worktree = an isolated copy of the repo checkout.)

Fields the loop **must** update every run:
- `Last run` timestamp
- Item status + last action taken
- Human decisions that overrode the loop (overrode = where a person decided differently from the loop's suggestion)

> **One-line summary:** The state file is the daily briefing — priorities, statuses, and where humans overruled the loop.

## How the Loop Runs (Typical Cycle)

Signpost: this is the walk-through of one run, from the scheduler firing to a written self-critique.

1. Scheduler fires (morning or interval).
2. Triage skill ingests: CI failures (24h), open issues/tickets, recent commits, old STATE.md.
3. High-priority items are appended to state with a suggested next action.
4. (Phase 2) For small bugs: worktree → implementer → verifier.
5. (Phase 3) Connectors update PRs/tickets; ambiguous items are flagged for humans. (Connectors = integrations that reach external tools like GitHub or Linear.)
6. Prune resolved/merged items from state. (Prune = remove entries that are no longer relevant.)
7. Write a **post-run critique**: false positives, repeated items, one adjustment for next time.

> **One-line summary:** Read signals → append priorities to state → (later phases) fix and update tickets → prune and self-critique.

## Verification Strategy

Signpost: this section explains how output quality is checked at each phase.

- Phase 1 (report-only): Humans read `STATE.md` — no auto-action verification needed.
- Phase 2+: The implementer never marks itself done; the verifier confirms fix scope + tests.
- The triage skill **must not invent architectural work** — signal only. (Architectural work = large structural changes; those always belong to humans.)

> **One-line summary:** Phase 1 is human-checked reports; from phase 2 a separate verifier confirms every fix.

## Human Handoff Points

Signpost: these are the items that must always reach a person, never be auto-fixed.

- Design decisions or multi-file refactors (refactor = restructuring code without changing behavior)
- Security, auth, payments, infrastructure
- Items flagged "needs discussion" in triage output
- Anything the loop has surfaced for 3+ days without resolution

> **One-line summary:** Big refactors, sensitive areas, "needs discussion" items, and 3-day-old unresolved items go to people.

## Tool-Specific Notes

Signpost: this section shows how to wire the same loop in four common tools — pick the one your team uses.

**Grok Build TUI**:
> 📄 **Example code:** [`examples/01-tool-specific-notes.sh`](examples/01-tool-specific-notes.sh)

**Claude Code**:
> 📄 **Example code:** [`examples/02-tool-specific-notes.sh`](examples/02-tool-specific-notes.sh)

**Codex**:
- Automations tab: daily prompt calling `$loop-triage`, output into the Triage inbox + `STATE.md`.

**GitHub Actions**:
- `daily-triage.yml` runs on weekdays, updates `STATE.md` + `loop-run-log.md`.

> **One-line summary:** Same loop, four wirings — Grok, Claude Code, Codex Automations, or a GitHub Action.

## Failure Modes & Mitigations

How to read it: left column = what goes wrong in practice; right column = the countermeasure. For instance, "state file grows without bound" = the memory file keeps growing with stale entries — the fix is pruning merged/closed items every run.

| Failure | Mitigation |
|---------|------------|
| Triage produces noise | Tighten skill rules; add a "Noise / Ignore" section |
| State file grows without bound | Prune merged/closed items every run |
| Auto-fixes with wrong priority | Start report-only; add effort/risk gates (gate = a mandatory approval check) |
| Missed overnight failures | `fireImmediately: true` or run at start of day + midday |
| Stale critique, never reviewed | Human handoff when the critique accumulates without resolution over N runs |

> **One-line summary:** Tighten rules against noise, prune state, start report-only, and never let the critique pile up unread.

## Cost Profile

How to read it: each row is a scenario and its token cost per run (tokens = AI compute units). Note the jump from L1 (report) to L2 (assisted fix) — that's why you enable fixes only after the reports are trustworthy.

| Scenario | Tokens/run | Notes |
|----------|------------|-------|
| No-op | ~5k | Nothing actionable in state |
| Full triage (L1) | ~50k | CI + issues + commits scan |
| Assisted fix (L2) | ~200k | Worktree + implementer + verifier |

**Cadence**: 1d–2h · **Tier**: low · **Suggested daily cap**: 100k tokens

> 📄 **Example code:** [`examples/03-cost-profile.sh`](examples/03-cost-profile.sh)

> **One-line summary:** ~5k idle, ~50k for a full L1 triage, ~200k for an L2 fix — capped at 100k tokens/day.

## Success Metrics

Signpost: these numbers tell you whether the morning report is actually replacing manual checking.

- Time from "something broke" to "humans know"
- % of mornings where `STATE.md` matches what you would have found yourself
- Reduction in ad-hoc "what's on fire?" Slack messages

> **One-line summary:** Success = faster awareness of breakage, an accurate state file, and fewer panic pings.

**Start report-only. Add actions only when triage quality is stable.**

> **One-line summary:** A cheap daily loop that reads CI, issues, and commits, writes a prioritized STATE.md briefing, and only earns auto-fix rights after weeks of trustworthy report-only runs.

---

*Back to [02 — Seven Production Patterns](../02-patterns/)*