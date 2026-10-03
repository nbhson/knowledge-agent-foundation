# ❓ FAQ — Core Concepts of Loop Engineering (Real Stories, Plain Language)

If a question is unclear, read the section in `../README.md` (named in brackets).

---

## Q1. My loop runs on schedule, but every morning it reports "found 0 items, did nothing" — is it broken? [→ §3.1 The Lifecycle of One Run]

**What you see**

The loop wakes up, reads `STATE.md`, calls triage, finds nothing, and exits. The log says `outcome: "idle"`, `items_found: 0`, `actions_taken: 0`. You are staring at an empty `high_priority` list and an empty `watch_list`, and you cannot tell whether the loop is broken or whether your watchlist is genuinely empty. Meanwhile the issues you expected it to pick up are sitting there untouched.

**Why**

`IdleNoop` — the "nothing to do" exit — has to be a **normal branch of the state machine**, not a failure. The chain is `Scheduled → LoadingContext → RunningTriage → WorkingInWorktree → Verifying → AwaitingHumanGate → Applied / Rejected`, and `RunningTriage` is allowed to fall out sideways into `IdleNoop`. Most "the loop did nothing" reports are this branch working correctly. The two real problems are different: triage produced a **narrative instead of a structured list**, or the loop kept burning the full sub-agent chain on an empty watchlist.

**What to do**

1. Make triage output **structured, not prose** — three named buckets: `High Priority` (the loop is handling it, or waiting on a human), `Watch List` (being monitored), `Recent Noise` (ignored this time).
2. Early-exit on empty: if `high_priority` is empty, log the run and stop. The reference engine records `tokens_estimate=5_000, outcome="idle"` — **exit under 5k tokens** rather than spinning up implementer and verifier for nothing.
3. Persist the outcome. Every run writes `last_run` timestamp plus the last actions, so the next run — and you — can see "triage ran at 06:00 and found nothing" instead of guessing.
4. Log the four counters every time: `items_found`, `actions_taken`, `escalations`, `duration_s`. If `items_found` is 0 for ten straight days on a repo that has open issues, the problem is the triage skill's inputs, not the loop.

**Verify**

Run it once with a known issue number in the watchlist and confirm `items_found: 1`. Then empty the watchlist and confirm the run terminates in the `IdleNoop` branch under the 5k token line, with a durable log entry and no sub-agent invoked.

---

## Q2. The loop shipped 5 pull requests last night and I cannot explain 3 of them — is that normal? [→ §6.2 Comprehension Debt]

**What you see**

Velocity is way up. Merge count per day went from 1 to 5. But when you try to describe what changed and why, you find yourself reading the diffs cold. A colleague asks "who approved the config change in `internal/`?" and the honest answer is "the loop did, at 3am." Code review has quietly become a rubber stamp — you approve because the verifier already approved and you have no budget to re-read everything.

**Why**

This is **comprehension debt**: the growing gap between what exists in the repository and what you personally understand. Loops ship far more code than you wrote, and that gap widens every run unless you deliberately read what the loop produced. It is not a bug in the loop; it is the loop doing exactly what you asked while your understanding stays flat.

**What to do**

1. Treat the **state file as the review surface**, not the chat log. A teammate should be able to read `STATE.md` and understand the day's activity without ever opening a conversation log.
2. Cap the blast radius per run so you can still hold it in your head: max auto-PRs per day, max iterations per item per run, and max N changed files before a human gate (N=10 is the suggested number).
3. Keep the **maker / checker split** honest. The implementer never grades its own work; the verifier runs tests inside an isolated worktree and its default stance is **REJECT** — it is told to "find reasons to REJECT", not to be agreeable.
4. Schedule a **post-run critique** — false positives, repeated items, and one change to improve the next run. This is the feedback loop, and it is what makes the system get smarter instead of just faster.
5. Watch for the second trap, **cognitive surrender**: using the loop to avoid thinking is the accelerant. Designing the loop with your judgment is the remedy. Same loop, opposite outcomes.

**Verify**

Ask a teammate to read only the state file and summarize the day's changes. If they cannot, comprehension debt is already being paid in someone else's time — lower the daily PR cap before adding more autonomy.

---

## Q3. Two loops started editing the same file and I got merge hell — how do I stop this? [→ §2.2 Worktrees, §6.4 Orchestration Tax]

**What you see**

The `ci-sweeper` loop and the `dependency-sweeper` loop both open pull requests touching `package.json` in the same branch. One of them silently wins. Then a third loop refuses to start because the branch is locked. You now have three pull requests, two conflicts, and an afternoon of reading diffs to figure out which change actually landed.

**Why**

Both agents share one working directory. When two agents edit the same file at the same time, you get merge hell — it is not a model failure, it is a filesystem collision. **Orchestration tax** is the real limiter: review bandwidth, merge conflicts, and context switching. Git worktrees remove the mechanical collisions; they do not remove the tax.

**What to do**

1. Give every agent a **dedicated working directory** — a git worktree, or an equivalent isolated checkout. Same history, separate working tree.
2. **One worktree per attempt**, tracked in a manifest, and name it after the attempt so you can see history at a glance:

```bash
loop-worktree create --run-id <id> --pattern ci-sweeper
# .worktrees/fix-1   attempt 1
# .worktrees/fix-2   attempt 2 (after a REJECT)
```

3. **Clean up on reject or escalate.** This is the step everyone forgets. When the verifier rejects a patch, or the run escalates to a human, the worktree is deleted in the same step. Orphaned worktrees are how you end up with forty stale checkouts and no idea which one is live.
4. When the verifier rejects, do not merge and do not retry forever — the engine records the attempt, and at the **hard cap of 3 attempts** it escalates with full context so you do not have to re-hunt for what it was doing.
5. Accept the ceiling. You are still the limit on how many parallel loops you can personally absorb. Three loops is a week of review; six is silence.

**Verify**

Run two loops simultaneously against the same repo and confirm zero file-level conflicts and no overlapping working directories. Separately, after a rejected run, confirm the worktree count did not grow.

---

## Q4. I keep asking the agent the same things — conventions, build commands, "why we don't do it this way" — should I write all that into a skill? [→ §2.3 Skills, §6.1 Intent Debt]

**What you see**

Every session, the agent starts from a blank slate. It guesses the package manager, picks the wrong test command, re-adds a logging library you banned after an incident, and proposes the exact approach you rejected in review last month. You paste the same correction into the chat every single morning. Then one week later it does it again.

**Why**

The model has no long-term memory across separate turns or sessions. Every missing piece of intent gets filled with a **confident guess — and wrong guesses**. This accumulation is called **intent debt**, and skills are how you pay it down.

**What to do**

1. Write it **once** into a `SKILL.md` plus scripts or references. A skill is durable memory of *intent*: project conventions, "we don't do it this way because of incident X", build/test/lint commands, review criteria, domain knowledge.
2. Cover the boring operational facts first — the actual build command, the actual test command, the actual lint command. These are the ones that get guessed wrongly and they are written in `AGENTS.md` or in the skill so every run reads them.
3. Record the **negative knowledge**: the approaches that failed and why. This is the part nobody writes and the part that saves the most rework.
4. Write skills so they **auto-trigger**: skill descriptions should be boring and specific, because a vague description does not get selected when it is needed.
5. Give triage its own skill with a strict output format, and separate action skills (small fixes and so on) that match project conventions.

**Verify**

Start a fresh session with no history and ask it to run the build. If the command is right first try with no correction from you, the skill is doing its job.

---

## Q5. Can I just flip this loop to unattended (L3) on a production repo right now? [→ §4 Autonomy Levels L1 → L3]

**What you see**

You built a daily triage loop, watched it run in report-only mode for an afternoon, and now you want it to actually fix things overnight so you can stop checking. Your reasoning: the report looked good, the logic is simple, nothing scary happened yet. You are about to remove yourself from the loop entirely.

**Why**

Autonomy is not a reward tier — it is a **safety license graduated by trust**. Skipping L1 and jumping straight to L3 on a production repository is the fastest way to have a loop break production before you understand it. The levels are a verified progression, not settings you pick once.

**What to do**

1. Move one step at a time, and only on evidence:

```
L1 REPORT-ONLY ──► L2 ASSISTED ──► L3 UNATTENDED
  Triage → state     Small auto-fixes   Runs without you watching
  No auto-action     With a verifier    Needs denylist + budget + gates
```

2. **L1 → L2** requires a better audit score and a human saying yes. At L2 the loop makes small self-fixes and a separate verifier checks them — the implementer cannot mark its own work done.
3. **L2 → L3** requires the denylist, the budget, and the gates to be *proven*, not merely written. Unattended means nobody is watching when it runs.
4. Know your **downgrade** paths before you need them: L3 → L2 on an incident or a cost spike; L2 → L1 is the kill switch.
5. Do not confuse loop speed with your intervention speed. The **inner loop** (think → act → observe → reflect, milliseconds) is too fast to guardrail and needs none — the guardrails belong to the **execution loop** (per action, per second) and the **outer loop** (per day or week). Banning infinite retries belongs to the execution loop, not the outer one.

**Verify**

Name the current level out loud and point to the evidence for it: for L2, an audit score plus a human approval; for L3, a working denylist, a budget cap, and a tested human gate. If you cannot name the evidence, you are not ready for that level.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: README.md.*
