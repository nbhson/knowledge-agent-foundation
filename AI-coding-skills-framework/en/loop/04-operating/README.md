# 🛠️ 04. Operating Loops in Production

> **📌 Core Concept**
>
> **Definition:** "Operating" means "operations" — once a loop is really running in production, your job shifts from design to **monitoring and control**: tracking token cost, reading the run log, watching metrics, and deciding when to slow down / pause / kill a loop.
> **Analogy:** Like a **pilot in the cockpit** — the plane (the loop) is already in the air; your job isn't to fix the engine mid-flight, but to read the gauges (metrics), check the fuel (token budget), and decide whether to land early (kill) when there's an alert.
> **Why it matters:** Your first loop will burn tokens — that's normal. This section teaches you to **estimate before running** (avoiding bill shock), **log for debugging** ("why did it do that?"), and **stop at the right moment** before damage becomes a disaster.

> Running a loop is an operations job. This section covers: **Token Budget**, **Logging**, **Metrics**, and **when to pause or kill** a loop.

---

## 1. Token & Cost Budgeting

> **Easy way to read it:** The question here is "**how much will this loop cost per day?**" — like calculating the fuel cost before a long trip. Use `loop cost` to estimate, then set a **limit (budget)** and a **stop point (kill switch)** for exceeding it. Rule of thumb: the faster the cadence and the more sub-agents, the exponentially higher the cost.

**Estimate before scheduling:**

```bash
npx @cobusgreyling/loop cost --pattern <id> --cadence <interval> --level L1
npx @cobusgreyling/loop init . --pattern <id>   # scaffolds loop-budget.md + loop-run-log.md + loop-budget skill
```

`loop-audit` scores cost observability and **caps L3** until you have a budget + run log + a LOOP.md budget section.

### Estimation Factors

| Factor | Impact |
|--------|-----------|
| Cadence | Linear multiplier (5m vs 1d = 288× runs/day) |
| Sub-agents per run | Each one = a full model + tool round-trips |
| Context size | Large repos + full CI logs = expensive triage |
| Verifier model | A stronger model on the verifier = worth it for unattended |

### Example Estimates (~50k tokens for a light triage run, ~200k for a run with implementer + verifier)

| Loop | Cadence | Runs/day | Rough daily tokens |
|------|---------|-----------|--------------------|
| Daily triage (report only) | 1d | 1 | ~50k |
| CI sweeper (light) | 15m | 96 | ~5M (if full — **avoid**) |
| PR babysitter | 5m | 288 | High — use early exit |

> **Best practice**: cheap triage pass; only spawn sub-agents when state reports something actionable. Empty watchlist → exit in < 5k tokens.

### Budget Rules

```markdown
## Loop Budget — Project X
- Max tokens/day: 2M (adjust to your plan)
- On exceed: pause schedulers, notify a human
- Max sub-agent spawns per run: 3
```

Encode this in the skill or scheduler prompt: *"If there are no high-priority items, exit immediately."*

---

## 2. Per-Run Logging

> **Easy way to read it:** The log is the loop's "**black box**" — each run writes one line answering: how long did it run? what did it find? what did it do? what did it cost? Later, when you wonder "why didn't it handle X?", open the log and the answer is there. The standard is **append-only**: add, never edit or delete.

Minimum log entry (append to `loop-run-log.md` or structured JSON):

```json
{
  "run_id": "2026-06-09T08:15:00Z",
  "pattern": "daily-triage",
  "duration_s": 45,
  "items_found": 4,
  "actions_taken": 1,
  "escalations": 0,
  "tokens_estimate": 52000,
  "outcome": "success"
}
```

Human-readable alternative in the `STATE.md` footer:

```markdown
---
Run log: 2026-06-09 08:15 | 4 findings | 1 worktree opened | 0 escalations
```

---

## 3. Metrics Dashboard

> **Easy way to read it:** Metrics are the loop's "**weighing scale**" — each week you look and ask: is this loop actually helping, or is it just spending money creating noise? Fill in the empty columns in the table below (runs, findings, escalations, false positives) for each pattern to see trends, not vibes.

Track weekly (spreadsheet or Notion):

| Metric | PR Babysitter | Daily Triage | CI Sweeper |
|--------|---------------|--------------|------------|
| Runs | | | |
| Actionable findings | | | |
| Auto-fixes proposed | | | |
| Human escalations | | | |
| False positives | | | |
| Mean time to human awareness | | | |
| Token spend (est.) | | | |

Pattern-specific success metrics live in each [pattern](../02-patterns/).

---

## 4. When to Slow Down / Pause / Kill

> **Easy way to read it:** This is the "**brake pedal scale**" — 3 levels matching severity: **Slow down** (ease off the pedal before running out of fuel), **Pause** (stop temporarily because there's immediate danger ahead), **Kill** (stop completely because this road is no longer worth driving). The question every time an incident happens: which level are we at?

### Slow Down

- Token budget > 80% mid-week
- False positive rate > 30% on triage
- The same item escalated 2+ times in 48h
- Major release week — pause auto-fix loops, report-only

### Pause

- A production incident is happening (the loop could break a hotfix)
- A breaking schema migration is in progress
- The main human reviewer is OOO + auto-merge is on (don't do this)

### Kill

- Ongoing S2 failures from the [failure catalog](../06-anti-patterns/README.md#2-failure-mode-catalog)
- Cost > value for 2 consecutive weeks
- The team has muted all notifications
- The pattern is superseded by an event-driven alternative (e.g., only the CI Action remains)

**Kill checklist**:
1. `scheduler_delete` / disable the Automation / remove the Action
2. Archive the state file with `status: retired`
3. Post-mortem in `stories/` (optional but valuable)

---

## 5. Upgrade Path

```
Report-only (L1) → 1–2 weeks of stable triage
       ↓
Small auto-wins (L2) → verifier + worktree + max attempts
       ↓
Connectors (L2+) → PRs/tickets update themselves
       ↓
Unattended (L3) → only with a denylist, budget, metrics, human gates
```

**Never skip L1** for a new pattern on a production repo.

---

*Next: [05 — Multi-Loop Coordination](../05-multi-loop/) → [06 — Anti-Patterns & Failure Modes](../06-anti-patterns/)*
