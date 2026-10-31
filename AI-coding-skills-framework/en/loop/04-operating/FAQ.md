# ❓ FAQ — Operating Loops in Production (Real Stories, Plain Language)

If a question is unclear, read the section in `../README.md` (named in brackets).
(Glossary used throughout: a **loop** = an agent task that runs on a schedule. **Cadence** = how often it runs, e.g. every 15 minutes. **Tokens** = the billing unit of model usage. **Run log** = the file where each run appends one line of history. **L1/L2/L3** = autonomy levels: report-only, assisted fixes, fully unattended.)

---

## Q1. My first loop burned a month of tokens in three days — can I estimate the cost before I schedule it? [→ §1 Token & Cost Budgeting]

This answer shows how to do the cost arithmetic *before* switching a loop on, not after the invoice.

**What you see**

The invoice is not the number you planned. A CI Sweeper on a `15m` cadence fires **96 times a day**; at roughly 50k tokens for a light triage run that is about **5M tokens/day**. A PR Babysitter on `5m` fires **288 times a day**. A Daily Triage loop on `1d` fires once and costs about 50k.
(In plain terms: "runs/day = 24 hours ÷ the cadence" — every 15 minutes is 96 runs a day, and each run costs tokens even if it finds nothing.)

How to read it: "Cadence" = how often the loop runs; "Runs/day" = 24h ÷ cadence; "Rough daily tokens" = runs/day × cost per run. For instance, the CI sweeper row: 96 runs × ~50k tokens ≈ 5M tokens a day — which is why a full-cost cadence is marked "avoid".

| Loop | Cadence | Runs/day | Rough daily tokens |
|------|---------|----------|--------------------|
| Daily triage (report only) | 1d | 1 | ~50k |
| CI sweeper (light) | 15m | 96 | ~5M (if full — avoid) |
| PR babysitter | 5m | 288 | High — use early exit |

**Why**

Cadence is a **linear multiplier** — `5m` versus `1d` is 288× the number of runs. Every sub-agent you spawn is a full model call plus its own tool round-trips, so sub-agents multiply the bill. A large repository and full CI logs make triage expensive even before anything is fixed. Nothing here is broken; the arithmetic was just never written down.

**What to do**

1. Estimate first, then scaffold the budget and log files:
> 📄 **Example code:** [`examples/01-q1-my-first-loop-burned-a-month-of.sh`](examples/01-q1-my-first-loop-burned-a-month-of.sh)
2. Write a **Loop Budget** block into the skill or `LOOP.md`: max tokens/day (e.g. `2M`), on exceed → *pause schedulers and notify a human*, max sub-agent spawns per run = `3`.
3. Make do-nothing runs cheap. Put this line in the scheduler prompt: *"If there are no high-priority items, exit immediately."* An empty watchlist should exit in **under 5k tokens**, not 50k.
4. Cheap triage first, action second — only spawn sub-agents when state reports something actionable.

**Verify**

`loop-audit` scores cost observability and **caps L3 (unattended) until** you have a budget file, a run log, and a budget section in `LOOP.md`. After one week, add up `tokens_estimate` in `loop-run-log.md` and compare it to the budget line. Already past 80% mid-week is your signal to slow down, not to keep going.

> **One-line summary:** Multiply cadence × cost per run before you schedule anything, then write a daily budget down and check the real spend weekly.

---

## Q2. Three weeks later someone asks "why didn't the loop handle PR #42?" and I have no answer — what should the log contain? [→ §2 Per-Run Logging]

This answer explains what one line of history per run should record, so future-you can reconstruct any decision.

**What you see**

A PR sits unhandled for days. You go looking for evidence of what the loop saw, what it decided, and what it cost. There is nothing. The only record is a chat message from three weeks ago saying "looks fine, triage is green".

**Why**

The run log is the loop's **black box**. One appended line per run answers the four questions you will always need later: how long did it run, what did it find, what did it do, what did it cost. The rule is **append-only — add, never edit or delete**, because edited logs stop being evidence. (append-only = like a paper logbook: you write new lines at the bottom; you never rewrite old ones.)

**What to do**

1. Append one entry per run to `loop-run-log.md` (or as structured JSON):
> 📄 **Example code:** [`examples/02-q2-three-weeks-later-someone-asks-why-didn.json`](examples/02-q2-three-weeks-later-someone-asks-why-didn.json)
2. If you prefer prose, put a one-line footer in `STATE.md`: `Run log: 2026-06-09 08:15 | 4 findings | 1 worktree opened | 0 escalations`. (In plain terms: "08:15 run, found 4 things, opened 1 worktree (a separate git copy for fixing), asked a human 0 times".)
3. Make sure `outcome` has real values (`success`, `error`, `skipped`) so you can filter later. A run that skipped because another loop held the lock should say so, not record `success` with zero actions.
4. Scaffold both files with `loop init .` so the format exists before you need it (scaffold = create the empty files with the right structure).

**Verify**

Pick any past incident and answer three questions from the log alone: what did it find, what did it do, what did it cost. If you cannot, the fields are missing. Then confirm the log only ever grows — no edited timestamps, no deleted bad runs.

> **One-line summary:** One append-only line per run — duration, findings, actions, cost — turns "why didn't it?" into a 30-second lookup.

---

## Q3. The loop never complains and runs every day — how do I know it is actually helping? [→ §3 Metrics Dashboard]

This answer explains how to measure a loop's value with a small weekly scorecard, so "seems fine" becomes a number.

**What you see**

Everything is green, no alerts fire, and you cannot answer a simple question: is this loop saving time or just spending money producing noise? You find out during an incident that the team had muted all of its notifications weeks ago.

**Why**

Metrics are the loop's **weighing scale**. One run tells you almost nothing; four weekly rows tell you the trend. Without numbers, "it seems fine" is a feeling, and the two most expensive failure modes — high false positives and cost above value — stay invisible until the invoice. (false positive = the loop flags something as a problem when it isn't — like a fire alarm triggered by steam.)

**What to do**

1. Fill the empty columns in the dashboard table every week, per pattern, in a spreadsheet or Notion. Keep it to five rows you will actually read. How to read it: "Metric" = what you count weekly; "Warning sign" = the value that says something is wrong. For instance, "false positives above 30%" means a third of the loop's flags were wrong — time to tighten triage.

| Metric | Warning sign |
|---|---|
| Actionable findings | 0 for two weeks running |
| False positives | above 30% on triage |
| Human escalations | same item, 2+ times in 48h |
| Token spend (est.) | rising while fixes stay flat |
| Mean time to human awareness | getting longer, not shorter |

2. Track runs and auto-fixes proposed too, so spend has a denominator.
3. Read pattern-specific success metrics in each pattern's own file, not just this generic table.
4. Turn the numbers into brake-pedal levels: false positives over 30%, or cost above value for two consecutive weeks, means slow down then kill.

**Verify**

Once you have four weekly rows you can answer "is this loop helping?" without guessing. Escalations of 0 **and** findings of 0 means the loop is dead weight — kill it. If every metric is flat while token spend climbs, cut the cadence before you cut the capability.

> **One-line summary:** Five numbers filled in weekly tell you whether the loop earns its keep or is quietly burning money.

---

## Q4. Something is on fire right now — should I slow down, pause, or kill the loop? [→ §4 When to Slow Down / Pause / Kill]

This answer gives you the three-step "brake pedal" for a misbehaving loop, with the exact triggers for each level.

**What you see**

Concretely: token budget is past 80% mid-week. False positives on triage are above 30%. The same item has escalated twice in the last 48 hours. Or it is a major release week. Or a production incident is open and the loop has auto-merge on — it can break the hotfix while the team is mid-fix. (hotfix = an urgent production repair, usually done in a hurry.)

**Why**

Three levels, matched to severity. **Slow down** = ease off before you run out. **Pause** = stop, because there is immediate danger ahead. **Kill** = stop for good, because this road is not worth driving. Asking "which level are we at?" is the whole decision — teams skip it and treat a pause-worthy moment as a slow-down moment.

**What to do**

1. Slow down on any of: budget > 80% mid-week; false positive rate > 30%; same item escalated 2+ times in 48h; major release week (switch to report-only).
2. Pause on any of: a production incident is open; a breaking schema migration is running; the main human reviewer is out of office while auto-merge is on. (breaking schema migration = a change to the database structure that can break code that depends on the old shape.)
3. Kill on any of: ongoing S2 failures from the failure catalog (S2 = severity 2, "actually harmful"); cost above value for two consecutive weeks; the team has muted all notifications; an event-driven alternative supersedes the pattern.
4. Run the kill checklist in order: `scheduler_delete` / disable the Automation / remove the Action → archive the state file with `status: retired` → post-mortem in `stories/` (optional but valuable). (post-mortem = the "what did we learn" write-up after the fact.)

**Verify**

After pausing, confirm no scheduled run fires in the next interval — a paused loop that still wakes up is worse than one you never built. After killing, confirm the scheduler entry is gone **and** the archived state file says `status: retired`, so the loop is not resurrected by the next deploy.

> **One-line summary:** Match the response to severity — ease off on warning signs, stop during danger, and shut down for good when the loop costs more than it saves.

---

## Q5. Can a brand-new pattern go straight to unattended auto-fixing? [→ §5 Upgrade Path]

This answer explains the ladder of autonomy a new loop must climb, and why the bottom rung cannot be skipped.

**What you see**

Someone proposes wiring a fresh pattern directly to auto-merge on `main`, on a production repository, in week one. The pitch is that the loop is "obviously safe" because it only fixes lint. (lint = mechanical style checks, e.g. "this line is too long" — the *easiest* class of fix.)

**Why**

Autonomous fixing (level L3) needs four things that only exist after weeks of evidence: a denylist of paths it must never touch, a token budget, metrics proving it works, and human gates for the dangerous actions. Without the first two, an unattended loop can edit the wrong file with nobody awake to stop it.

**What to do**

1. Climb the ladder in order, spending real time on each rung (how to read it: each line is a level, top to bottom; the arrow says you may only move down the ladder after the previous level has run stably for a while):

```
Report-only (L1) → 1–2 weeks of stable triage
       ↓
Small auto-wins (L2) → verifier + worktree + max attempts
       ↓
Connectors (L2+) → PRs/tickets update themselves
       ↓
Unattended (L3) → only with a denylist, budget, metrics, human gates
```

2. **Never skip L1** for a new pattern on a production repo. Two weeks of report-only is what tells you the false positive rate.
3. At L2 add a verifier model, a worktree per fix, and a max-attempts cap so a failing fix cannot retry forever.
4. Only then, and only with all four L3 ingredients written down, consider unattended.

**Verify**

`loop-audit` refuses L3 until a budget, a run log, and a `LOOP.md` budget section all exist — treat that refusal as the gate, not as a bug to route around. Ask for the L1 report count: under two weeks of stable triage, the answer is no.

> **One-line summary:** No new loop goes straight to auto-merging — it earns autonomy rung by rung, starting with two weeks of report-only.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: README.md.*
