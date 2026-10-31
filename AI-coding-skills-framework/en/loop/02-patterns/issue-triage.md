# 🗂️ Issue Triage Loop

**Goal**: Sort noisy issues into an actionable backlog — suggest only, no auto-fix. Feeder for Daily Triage.
(Glossary: an **issue** = a GitHub ticket reporting a bug, idea, or question. **Backlog** = the to-do list. **Daily Triage** = the related loop that prioritizes the most important items each day. "Suggest only" = the loop never edits code; it only writes recommendations.)

## Scheduling

Signpost: this section says how often to run the loop.

**Recommended**:
- `/loop 2h–1d` (Grok, Claude Code) — `/loop` = a scheduler command: "run this every 2 hours to once a day"
- GitHub Action cron multiple times/day for issue-heavy repos (cron = a time-based scheduler)

> **One-line summary:** Run it a few times a day; busy repos can run it more often.

## Required Skills

Signpost: each loop is built from small named skills. Here is what this one needs and why.

- `loop-triage` — Reads issues, classifies severity/priority, detects duplicates/stale ones (duplicate = the same problem reported twice; stale = old and probably no longer relevant)
- `issue-intake` — Handles issues that are too ambiguous: clarify or escalate, no guessing (escalate = pass to a human)

> **One-line summary:** One skill classifies issues; the other handles the confusing ones by asking, not guessing.

## State

Signpost: the loop keeps a small markdown file as its memory between runs. This is what it looks like.

`issue-triage-state.md`:

```markdown
# Issue Triage State

Last run: 2026-06-09 10:00 UTC

## New Issues (last 24h)
- #1310 — bug: auth timeout — [High, actionable] — suggested: reproduce + fix
- #1311 — "app slow" — [Ambiguous] — loop-intake: needs more info, has asked via comment
- #1312 — duplicate of #1305 — [Dup] — suggested: close

## Needs Human
- #1298 — large feature request — needs a product decision
```

How to read it: each line is one issue. For instance, #1310 is a login timeout bug, judged High priority and fixable, so the loop suggests "reproduce + fix". #1311 ("app slow") is too vague to act on, so the loop asked the reporter for details instead of guessing. #1312 repeats #1305, so the suggestion is "close it". #1298 needs a product decision only a human can make.

> **One-line summary:** The state file lists each issue, its classification, and the loop's suggested next step.

## How the Loop Runs (Typical Cycle)

Signpost: this is one full pass of the loop, from reading issues to updating state.

1. Read new/updated open issues (last 24h).
2. For each issue:
   - **Classify**: bug / feature / question / duplicate / stale.
   - **Ambiguous** (not enough to verify "done"): the loop-intake skill asks for more or escalates — **no guessing**.
   - **Actionable**: write the suggested next action into state.
3. Update `issue-triage-state.md` — suggestions only, no auto-fix (L1 propose-only; L1 = the lowest autonomy level: the loop may only report and suggest).
4. High-priority issues become a source for Daily Triage.

> **One-line summary:** The loop labels every new issue and suggests a next step; it never fixes anything itself.

## Verification Strategy

Signpost: how the loop stays safe and trustworthy, given that it edits nothing.

- Level **L1 propose-only** — the loop only classifies and suggests, never edits code.
- The triage skill is **signal only** — no inventing architectural work (it may not invent big redesign tasks that nobody asked for).
- Every finding comes with evidence (issue link, classification reasoning).

> **One-line summary:** Suggestions only, every one backed by evidence — the loop edits no code.

## Human Handoff Points

Signpost: the situations where the loop must stop and ask a person.

- Feature requests that need a product decision
- Issues that remain unclear after asking
- High-priority issues with no owner (no owner = nobody has picked the issue up)
- Security issues (escalate immediately)

> **One-line summary:** Product calls, persistently unclear issues, urgent unowned issues, and anything security-related go straight to humans.

## Failure Modes & Mitigations

How to read it: "Failure" = what can go wrong; "Mitigation" = the guard that prevents it. For instance, the first row: triage could flood you with useless labels, so the skill's rules are tightened and obvious noise goes into a "Noise / Ignore" bucket.

| Failure | Mitigation |
|---------|------------|
| Triage produces noise | Tighten skill rules; "Noise / Ignore" section |
| Misclassification | Evidence for every finding; periodic human review |
| Guessing at ambiguous issues | loop-intake: ask for more or escalate, no guessing |
| Overwhelmed by many issues | Prioritize by severity; cap processing per run |

> **One-line summary:** Guardrails: strict rules against noise, evidence for every call, and asking instead of guessing.

## Cost Profile

How to read it: "Scenario" = what kind of run happens; "Tokens/run" = roughly how much model usage one such run costs (tokens = the billing unit of model usage). For instance, "No-op" means the loop woke up, found no new issues, and exited — that should cost almost nothing.

| Scenario | Tokens/run | Notes |
|----------|------------|-------|
| No-op | ~5k | No new issues |
| Full triage | ~40k | Scan issues + classify |

**Cadence**: 2h–1d · **Tier**: low · **Suggested daily cap**: 100k tokens (cadence = how often it runs; tier = how much supervision it needs; daily cap = a hard spending limit per day)

> 📄 **Example code:** [`examples/01-cost-profile.sh`](examples/01-cost-profile.sh)

> **One-line summary:** This is one of the cheapest loops — mostly reading and labeling, no expensive fixing.

## Success Metrics

Signpost: how you tell, with numbers, that this loop is worth keeping.

- Time from "new issue" to "classified + suggested action"
- % of classifications that are correct (no re-triage needed)
- Reduction in "orphaned" backlog issues no one knows about (orphaned = sitting in the list, ignored by everyone)

> **One-line summary:** Success = fast, correct classification and no forgotten issues.

> **Natural pair**: Issue Triage (classify) → Daily Triage (prioritize) → action loops (execute). Low risk, an excellent first pair with Daily Triage.

---

*Back to [02 — Seven Production Patterns](../02-patterns/)*
