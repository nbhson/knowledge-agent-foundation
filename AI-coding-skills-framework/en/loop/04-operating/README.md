# 🛠️ 04. Operating Loops in Production

> **📌 Core Concept**
>
> **Definition:** "Operating" means everyday operations — once a loop is really running in production, your job changes from design to **monitoring and control**: watching token cost, reading the run log, checking metrics, and deciding when to slow down / pause / kill a loop.
> **Analogy:** Think of a **pilot in the cockpit** — the plane (the loop) is already flying. Your job is not to fix the engine mid-flight, but to read the gauges (metrics), check the fuel (token budget), and land early (kill) when you see a warning.
> **Why it matters:** Your first loop will use extra tokens — that is completely normal. This section shows you how to **estimate before you run** (so you avoid bill shock), **keep logs for debugging** ("why did it do that?"), and **stop at the right time** before small damage turns into a disaster.

> Running a loop is an operations job. This section covers: **Token Budget**, **Logging**, **Metrics**, and **when to pause or kill** a loop.

---

## 1. Token & Cost Budgeting

> **Easy way to read it:** The key question here is "**how much will this loop cost per day?**" — just like figuring out fuel costs before a long trip. Use `loop cost` to get an estimate, then set a **limit (budget)** and a **stop rule (kill switch)** for when you go over it. As a rule of thumb: faster cadence plus more sub-agents means much higher cost.

**Estimate before scheduling:**

> 📄 **Example code:** [`examples/01-1-token-cost-budgeting.sh`](examples/01-1-token-cost-budgeting.sh)

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

> **Best practice**: start with a cheap triage pass, and only spawn sub-agents when the state shows something worth acting on. Empty watchlist → exit in < 5k tokens.

### Budget Rules

```markdown
## Loop Budget — Project X
- Max tokens/day: 2M (adjust to your plan)
- On exceed: pause schedulers, notify a human
- Max sub-agent spawns per run: 3
```

Please put this in the skill or scheduler prompt: *"If there are no high-priority items, exit immediately."*

---

## 2. Per-Run Logging

> **Easy way to read it:** The log is the loop's "**black box**" — each run adds one line answering: how long did it take? what did it find? what did it do? how much did it cost? Later, when you wonder "why didn't it handle X?", just open the log and you will find the answer. The rule is **append-only**: always add, never edit or delete.

Minimum log entry (append to `loop-run-log.md` or structured JSON):

> 📄 **Example code:** [`examples/02-2-per-run-logging.json`](examples/02-2-per-run-logging.json)

Human-readable alternative in the `STATE.md` footer:

```markdown
---
Run log: 2026-06-09 08:15 | 4 findings | 1 worktree opened | 0 escalations
```

---

## 3. Metrics Dashboard

> **Easy way to read it:** Metrics are the loop's "**bathroom scale**" — each week you step back and ask: is this loop really helping, or is it just spending money and making noise? Fill in the empty cells below (runs, findings, escalations, false positives) for each pattern so you can see trends, not just gut feelings.

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

> **Easy way to read it:** Think of this as the "**brake pedal scale**" — 3 levels depending on how serious things are: **Slow down** (ease off before you run out of fuel), **Pause** (stop for now because there is danger ahead), **Kill** (stop for good because this road is no longer worth it). Whenever something goes wrong, just ask: which level are we at?

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
