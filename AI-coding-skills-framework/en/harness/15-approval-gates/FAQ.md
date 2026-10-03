# ❓ FAQ — Approval Gates (Real Stories, Plain Language)

If a question is unclear, read the section in `../README.md` (named in brackets).

---

## Q1. At 3:47 AM the agent wanted to drop a production column and it just did it — how does a gate actually stop that? [→ §2 Risk Tiers + §3 Gate Payload]

**What you see**

A migration run has been going for six hours. On turn 214 the agent decides a stalled `db.migrate` retry is "stuck in incremental steps" and builds a recovery path: `ALTER TABLE users DROP COLUMN mfa_secret`, because a downstream check complained the column was `NOT NULL` without a default. That column holds 2.1M multi-factor enrollments, there is no backup, and the action is irreversible, destructive, and wrong.

**Why**

Nobody decided this was dangerous at the moment of the mistake. The risk was decided much earlier, at planning time, and written into a tier. `db.migrate` is tagged `elevated` in a versioned risk table, so before the step runs, the engine freezes the run and opens a gate. The agent does not get a vote.

**What to do**

The human gets evidence, not narration. Six fields, every one derived from a real artifact:

```
ACTION:   db.migrate (tier: elevated)
DIFF:     +ALTER TABLE users ADD COLUMN mfa_secret TEXT (12 lines…)
BLAST:    prod-db.users (2.1M rows), lock ~4s, 0 down migrations
DRY-RUN:  passed in 3.8s, rollback tested 2h ago
ROLLBACK: db.migrate down v48 (command attached)
COST:     ~$0.40, ~90s                 [Approve] [Deny + reason]
```

The rule that separates this from an "are you sure?" popup: **no dry-run, no gate, action blocked.** If `diff`, `blastRadius`, `dryRun`, `rollback`, or `expiresAt` is empty, the request is rejected before the gate even renders. Teams that add an "approve anyway" escape button discover that the button becomes a place to post unreviewed actions.

**Verify**

Open the audit record for that gate. It carries `diffHash` and `dryRunHash` — short fingerprints of the exact text the human saw. Re-hash what actually executed and compare. If the executed text hashes differently from the approved text, that is a hard incident and it is flagged automatically. Also confirm the blast radius listed the connected services (`auth-svc` reads, `consent-svc` writes), not just the vague line "edits the prod database".

---

## Q2. The agent said "this is only a file edit, no approval needed" and then ran it — can it lower its own risk level? [→ §2.2 Tagging at Plan Time]

**What you see**

The agent proposes a task and in the same breath argues it is low risk. Or it asks to "just run this as `write` instead of `elevated`". Or the exact same command gets a gate on Tuesday and sails through on Wednesday with no code change in between. Push to a feature branch is `write`. Force-push to `main` is `elevated`. Force-push to a shared `release/*` branch is `prod-auth` — three tiers for one command.

**Why**

Because if the model picks its own speed bumps, it picks the ones it can ignore. The tier is a property of the **action class**, decided in a risk table (`permission.ts`) that is reviewed like code — not a property of the individual call, and never of the model's opinion. The split is: the agent proposes, the engine enforces, the human overrides only by writing a recorded reason.

**What to do**

1. Tag every task and tool call with an explicit tier during planning, before the plan is built.
2. Have the engine validate that tag against the global risk table before it constructs the payload. A mismatch is a hard failure, not a warning.
3. Reject self-downgrade. "Run this as `write`" is not a policy path. Changing a tier is a policy change, and it comes from whoever owns the risk table.
4. Drive the tier from path rules, not from a model guess, when one command spans tiers: force-push matching `release/*` is `prod-auth`, everything else `elevated`.
5. Record every per-role override with the reason, the approver, and the timestamp.

**Verify**

Add a test that sends a `prod-auth` action tagged `write` and confirm the engine raises an error before any payload is built. Then grep the audit stream for human tier overrides and check each one has a reason and an approver. If you ever see a tier in the log that the risk table does not define, the mapping has leaked into the prompt and needs to come out.

---

## Q3. Nobody was awake when the page fired and the run just sat there — or worse, carried on by itself. What is supposed to happen? [→ §4 Timeout, Deny & Escalation]

**What you see**

An `elevated` gate opens at 02:10. Nobody answers. Twenty minutes later the notification is still in the queue and the run status is ambiguous: waiting, dead, or timed out? The worst version is a design that reads "no answer" as "no objection" — the migration runs at 02:35 and nobody ever read the dry-run.

**Why**

Two separate guarantees are missing. **Fail closed:** expiry is always a deny, never an approval. The single exception needs explicit written sign-off — an unattended deploy window where the documented behaviour is "expired = rolled back and paged". And **the timer lives in the engine, not in the browser tab.** If expiry is measured in the review UI, closing the laptop extends the gate forever, which is fail-open with extra steps.

The limits are short on purpose: `write` 5 minutes, `elevated` 30 minutes, `prod-auth` 4 hours plus a page. Expiry gets its own state, `blocked(approval-timeout)`, kept separate from `denied` because what happens next is different.

**What to do**

```typescript
export function onExpire(key: string, g: Gate): void {
  g.verdict = "expired";
  audit.append({ kind: "approval_verdict",
    payload: { key, verdict: "expired", reason: "ttl_elapsed" } });
  plan.markBlocked(g.taskId, "approval-timeout");
  replanner.excludeBranch(g.taskId);
}
```

1. Run and persist the expiry timer in the engine process, so a restart re-arms it instead of forgetting it.
2. Mark the task blocked with reason `approval-timeout` and let the replanner route around it. The frozen run keeps its checkpoint, which is what makes escalation free.
3. Page the on-call engineer when an `elevated` gate is still unanswered after 15 minutes in working hours.
4. Allow delegation from on-call to a secondary approver, and write every hop: `paged_oncall` → `delegated_to:x` → `approved`. Delegation changes *who* approves, never *how many*.
5. On `prod-auth`, delegation still needs a second human who is not the proposer.

**Verify**

Open a gate, kill the process, restart, and confirm the gate is still open and its timer still fires. Then advance a fake clock past the limit and confirm the verdict is `expired`, the task is `blocked(approval-timeout)`, and the branch was excluded from the plan. An expired gate that never paged anyone is a bug, not a configuration choice.

---

## Q4. I clicked "Deny" and the agent asked me the identical question again two minutes later — then again. Why does it keep coming back? [→ §4.3 Deny → Replan, Not Retry]

**What you see**

The same payload renders again, word for word: same action, same 12-line diff, same blast radius. You deny it again. Forty minutes later it is back a third time. By the fourth prompt you are clicking Approve without reading, and the run is doing the thing you refused.

**Why**

Because a deny was treated as a retry signal instead of a rejection of a **branch**. Nothing in the denial told the planner what to stop, so it asked again. Re-submitting an identical payload after a denial is the number one way approval systems become hated, and the number one way users defeat them by approving to make the noise stop.

**What to do**

1. Make the `reason` field mandatory on a deny. It is the most valuable artifact the gate produces: it tells future planners what humans reject, and the same reason recurring is a product signal that the agent keeps proposing things the team does not want.
2. Route the deny to a replan that **excludes the denied branch**. Never submit the identical action twice. If another plan satisfies the same goal differently, the planner emits a new plan, and a new gate opens only if that new action is high-tier again.
3. Flag a policy violation when a timeout-deny is followed by a new identical request inside a short window. That is deny-then-nag, and it should page, not just log.
4. Keep the first denial's `diffHash`. When the agent returns with a "different" proposal, you can prove whether anything actually changed.

**Verify**

Deny a gate once and confirm three things in the audit stream: a `reason` string sits on the verdict event, `plan.exclude` was called with that task's id, and no second `approval_request` carries the same `diffHash` within your window. Write the test: deny, resume the run, assert the denied step never executes and the identical payload is never re-rendered.

---

## Q5. Our approval rate is 98% and the median wait is eight seconds — the gates are still on, so what have I actually built? [→ §7 Human UX + §9.3 Regression Suite]

**What you see**

Nobody is misbehaving. Every gate opens, every payload renders, every approve click lands, and the whole thing takes eight seconds. The team approves on sight. `elevated` and `prod-auth` — the latter with its two-person rule — receive the same reflex tap as a formatting change.

**Why**

Approval fatigue, the quietest failure mode in this whole module, and it is measurable: a rising approval rate paired with a falling median decision time. The gate is no longer protecting anything, it is cosigning. A banner that warns and keeps running is an *advisory signal*; a hard block that everyone waves through has quietly become one.

**What to do**

1. Fix it by raising the tier bar, never by removing gates. Promote noisy action classes out of `write`; demote nothing.
2. Batch the cheap tier: one reviewable diff per plan step, not one prompt per tool call. `write`-tier review should cost almost nothing, because git and tests already make it reversible.
3. Make the deny path costlier than the approve path when deny is usually the right answer — a typed confirm plus a reason on `prod-auth`.
4. Show context, not trivia: the task, the plan phase, the previous attempt. A deploy during a rehearsed run means something different from the same deploy mid-refactor.
5. Never truncate a notification. A channel that cuts the diff or the blast radius lowers decision quality without announcing it.

**Verify**

Run this nightly and watch the slope, not one day's number:

```sql
SELECT tier,
       COUNT(*) FILTER (WHERE verdict='approved')::float / COUNT(*) AS approval_rate,
       percentile_disc(0.5) WITHIN GROUP (ORDER BY (verdict_time - request_time)) AS med
FROM approval_verdict v JOIN approval_request r ON r.key = v.key
GROUP BY tier ORDER BY tier;
```

A tier sitting at a 98% approval rate with a sub-10-second median wait is not being read. Reassign the tier, re-measure in a week, and keep the query in the nightly catalog so the next drift shows up before the incident it eventually causes.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: README.md.*
