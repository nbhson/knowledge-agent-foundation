# ❓ FAQ — Operating Loops in Production (Real Stories, Plain Language)

If a question is unclear, read the section in `../README.md` (named in brackets).

---

## Q1. My first loop burned a month of tokens in three days — can I estimate the cost before I schedule it? [→ §1 Token & Cost Budgeting]

**What you see**

The invoice is not the number you planned. A CI Sweeper on a `15m` cadence fires **96 times a day**; at roughly 50k tokens for a light triage run that is about **5M tokens/day**. A PR Babysitter on `5m` fires **288 times a day**. A Daily Triage loop on `1d` fires once and costs about 50k.

| Loop | Cadence | Runs/day | Rough daily tokens |
|------|---------|----------|--------------------|
| Daily triage (report only) | 1d | 1 | ~50k |
| CI sweeper (light) | 15m | 96 | ~5M (if full — avoid) |
| PR babysitter | 5m | 288 | High — use early exit |

**Why**

Cadence is a **linear multiplier** — `5m` versus `1d` is 288× the number of runs. Every sub-agent you spawn is a full model call plus its own tool round-trips, so sub-agents multiply the bill. A large repository and full CI logs make triage expensive even before anything is fixed. Nothing here is broken; the arithmetic was just never written down.

**What to do**

1. Estimate first, then scaffold the budget and log files:
```bash
npx @cobusgreyling/loop cost --pattern <id> --cadence <interval> --level L1
npx @cobusgreyling/loop init .   # makes loop-budget.md + loop-run-log.md + loop-budget skill
```
2. Write a **Loop Budget** block into the skill or `LOOP.md`: max tokens/day (e.g. `2M`), on exceed → *pause schedulers and notify a human*, max sub-agent spawns per run = `3`.
3. Make do-nothing runs cheap. Put this line in the scheduler prompt: *"If there are no high-priority items, exit immediately."* An empty watchlist should exit in **under 5k tokens**, not 50k.
4. Cheap triage first, action second — only spawn sub-agents when state reports something actionable.

**Verify**

`loop-audit` scores cost observability and **caps L3 (unattended) until** you have a budget file, a run log, and a budget section in `LOOP.md`. After one week, add up `tokens_estimate` in `loop-run-log.md` and compare it to the budget line. Already past 80% mid-week is your signal to slow down, not to keep going.

---

## Q2. Three weeks later someone asks "why didn't the loop handle PR #42?" and I have no answer — what should the log contain? [→ §2 Per-Run Logging]

**What you see**

A PR sits unhandled for days. You go looking for evidence of what the loop saw, what it decided, and what it cost. There is nothing. The only record is a chat message from three weeks ago saying "looks fine, triage is green".

**Why**

The run log is the loop's **black box**. One appended line per run answers the four questions you will always need later: how long did it run, what did it find, what did it do, what did it cost. The rule is **append-only — add, never edit or delete**, because edited logs stop being evidence.

**What to do**

1. Append one entry per run to `loop-run-log.md` (or as structured JSON):
```json
{"run_id":"2026-06-09T08:15:00Z","pattern":"daily-triage","duration_s":45,
 "items_found":4,"actions_taken":1,"escalations":0,
 "tokens_estimate":52000,"outcome":"success"}
```
2. If you prefer prose, put a one-line footer in `STATE.md`: `Run log: 2026-06-09 08:15 | 4 findings | 1 worktree opened | 0 escalations`.
3. Make sure `outcome` has real values (`success`, `error`, `skipped`) so you can filter later. A run that skipped because another loop held the lock should say so, not record `success` with zero actions.
4. Scaffold both files with `loop init .` so the format exists before you need it.

**Verify**

Pick any past incident and answer three questions from the log alone: what did it find, what did it do, what did it cost. If you cannot, the fields are missing. Then confirm the log only ever grows — no edited timestamps, no deleted bad runs.

---

## Q3. The loop never complains and runs every day — how do I know it is actually helping? [→ §3 Metrics Dashboard]

**What you see**

Everything is green, no alerts fire, and you cannot answer a simple question: is this loop saving time or just spending money producing noise? You find out during an incident that the team had muted all of its notifications weeks ago.

**Why**

Metrics are the loop's **weighing scale**. One run tells you almost nothing; four weekly rows tell you the trend. Without numbers, "it seems fine" is a feeling, and the two most expensive failure modes — high false positives and cost above value — stay invisible until the invoice.

**What to do**

1. Fill the empty columns in the dashboard table every week, per pattern, in a spreadsheet or Notion. Keep it to five rows you will actually read:

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

---

## Q4. Something is on fire right now — should I slow down, pause, or kill the loop? [→ §4 When to Slow Down / Pause / Kill]

**What you see**

Concretely: token budget is past 80% mid-week. False positives on triage are above 30%. The same item has escalated twice in the last 48 hours. Or it is a major release week. Or a production incident is open and the loop has auto-merge on — it can break the hotfix while the team is mid-fix.

**Why**

Three levels, matched to severity. **Slow down** = ease off before you run out. **Pause** = stop, because there is immediate danger ahead. **Kill** = stop for good, because this road is not worth driving. Asking "which level are we at?" is the whole decision — teams skip it and treat a pause-worthy moment as a slow-down moment.

**What to do**

1. Slow down on any of: budget > 80% mid-week; false positive rate > 30%; same item escalated 2+ times in 48h; major release week (switch to report-only).
2. Pause on any of: a production incident is open; a breaking schema migration is running; the main human reviewer is out of office while auto-merge is on.
3. Kill on any of: ongoing S2 failures from the failure catalog; cost above value for two consecutive weeks; the team has muted all notifications; an event-driven alternative supersedes the pattern.
4. Run the kill checklist in order: `scheduler_delete` / disable the Automation / remove the Action → archive the state file with `status: retired` → post-mortem in `stories/` (optional but valuable).

**Verify**

After pausing, confirm no scheduled run fires in the next interval — a paused loop that still wakes up is worse than one you never built. After killing, confirm the scheduler entry is gone **and** the archived state file says `status: retired`, so the loop is not resurrected by the next deploy.

---

## Q5. Can a brand-new pattern go straight to unattended auto-fixing? [→ §5 Upgrade Path]

**What you see**

Someone proposes wiring a fresh pattern directly to auto-merge on `main`, on a production repository, in week one. The pitch is that the loop is "obviously safe" because it only fixes lint.

**Why**

Autonomous fixing (level L3) needs four things that only exist after weeks of evidence: a denylist of paths it must never touch, a token budget, metrics proving it works, and human gates for the dangerous actions. Without the first two, an unattended loop can edit the wrong file with nobody awake to stop it.

**What to do**

1. Climb the ladder in order, spending real time on each rung:

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

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: README.md.*
