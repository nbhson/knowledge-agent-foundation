# ❓ FAQ — Multi-Loop Coordination (Real Stories, Plain Language)

If a question is unclear, read the section in `../README.md` (named in brackets).

---

## Q1. I turned on a second loop and now both of them fight over the same branch — how do I stop that? [→ §1 Principles, §5 Collision Detection]

**What you see**

The PR Babysitter opens a worktree on `fix/flaky-test` at 10:02. At 10:03 the Dependency Sweeper pushes `bump/lodash` to that same branch. One overwrites the other, the PR diff now contains both changes mixed together, and the human reviewer cannot tell which loop did what. This is not hypothetical — `stories/multi-loop-collision.md` and `stories/dependency-vs-ci-sweeper-collision.md` are both writeups of exactly this.

**Why**

Many loops in one repository is not bad by itself. It becomes dangerous only when **there are no boundaries** — like an intersection with no traffic lights, where every driver assumes they have priority. Without a shared record of who is working on what, both loops are behaving reasonably and still collide.

**What to do**

1. Every action loop writes `acting_on: <branch-or-pr-id>` into its own state file before it starts.
2. Before spawning a fix, read **all other** pattern state files. If another loop's `acting_on` matches, skip and log the skip to `loop-run-log.md`.
3. Better than self-discipline, use real advisory locks in the control script:

```bash
# before spawning a worktree
npx @cobusgreyling/loop-worktree lock --paths <globs> --owner <pattern>
# after finishing
npx @cobusgreyling/loop-worktree unlock --owner <pattern>
```

4. Know the gap: `loop-worktree create` does **not** check locks itself — the lock/unlock pairing is a convention you enforce in the control script. For one-shot sandboxed runs, `loop-sandbox --lock-paths` follows the same convention.

**Verify**

Start two loops that deliberately target the same branch. Exactly one should acquire the lock; the other should log a skip, not a duplicate worktree. Then confirm the lock is released — a stale lock is a loop that silently stops working forever.

---

## Q2. Should every loop share one `STATE.md`, or does each one get its own file? [→ §2 Recommended State Layout]

**What you see**

All four loops write into a single `STATE.md`. Then the Dependency Sweeper rewrites the file to record its in-flight updates, and the Daily Triage priorities plus the human inbox are gone. You now have a loop whose history nobody can reconstruct and a triage queue that silently resets.

**Why**

Separate state files are one of the five core principles. A shared file is a shared write target, and shared write targets are where loops overwrite each other's data. The only file that should be genuinely shared is the append-only run log.

**What to do**

1. Give each pattern its own state file, and keep one shared append-only log:

```
STATE.md                     # Daily Triage (priorities, human inbox)
pr-babysitter-state.md       # PR watcher
ci-sweeper-state.md          # Active CI failures + attempt counts
dependency-sweeper-state.md  # In-flight package updates
post-merge-state.md          # Cleanup backlog
loop-run-log.md              # Append-only observability
```

2. Linear or GitHub Projects work just as well — but the loop must **read and write the same store every run**. A store it only writes is a log; a store it only reads is a stale snapshot.
3. Copy the same path denylist into **every** `LOOP.md`, so no loop can be talked into touching a protected path.
4. Aggregate the token budget across loops, not per loop — three loops at 700k each is still 2.1M.

**Verify**

Delete one state file and run only its loop. If the loop still works, it was reading something else and you have not found your real state. Then check that `loop-run-log.md` still shows every pattern's entries after a week of parallel runs.

---

## Q3. CI on `main` is red and three loops all want to act — who goes first? [→ §3 Priority When Loops Conflict]

**What you see**

Main is red. The CI Sweeper wants to push a fix, the PR Babysitter wants to rebase an open PR, and the Dependency Sweeper wants to land a version bump. All three fire within the same 15-minute window, all three assume they are the most urgent, and the branch is now a three-way mess.

**Why**

Red CI on `main` blocks everything, because nobody can merge while it is failing. That makes it the top of a fixed priority ladder. Read the ladder top to bottom: on conflict the higher-ranked loop wins and the lower-ranked loop yields — no negotiation, no cleverness.

**What to do**

1. Use this ranking as written:

| Priority | Loop | Reason |
|---|---|---|
| 1 | CI Sweeper | Red main blocks everything |
| 2 | PR Babysitter | Active PRs are time-sensitive |
| 3 | Dependency Sweeper | Pauses when CI is red |
| 4 | Post-Merge Cleanup | Off-peak, lowest urgency |
| 5 | Daily Triage | Reports only at L1; coordinates the others |

2. Encode the yields in the root `LOOP.md` schedule so they are mechanical, not remembered: PR Babysitter *skip if CI Sweeper is acting on the same PR*; Dependency Sweeper *skip if main CI is red*.
3. Keep Daily Triage at report-only level L1. It coordinates the others and must never compete with them for the same edit.

**Verify**

Force a conflict on one branch with CI red. The CI Sweeper proceeds and the other two log a skip to `loop-run-log.md`. If the Dependency Sweeper still lands a bump, its skip condition is not actually in the prompt.

---

## Q4. Two loops flagged PR #42 and now neither of them will touch it — who decides? [→ §6 Human Inbox]

**What you see**

PR #42 is flagged by both the CI Sweeper and the PR Babysitter. Both loops see a matching `acting_on` from the other, both correctly yield, and the PR sits there untouched. Nobody was notified, so the stall is invisible until a human stumbles onto it days later.

**Why**

This is the *ambiguous / cross-loop* case: ownership is genuinely unclear, and both loops are behaving correctly by yielding. Coordination rules stop collisions, but they cannot invent an owner. Without an explicit handoff point, correct behaviour on both sides produces a silent deadlock.

**What to do**

1. Keep a shared inbox section at the top of `STATE.md` for exactly these cases:

```markdown
## Human Inbox (ambiguous / cross-loop)
- [ ] PR #42: flagged by both CI Sweeper and PR Babysitter — human picks the owner
```

2. Teach the rule: a loop that cannot claim ownership **writes an inbox item and exits** — it does not wait, retry, or force the edit.
3. Write the owner into the state file once a human decides, so the next run is unambiguous.
4. Review the inbox on a schedule. An inbox nobody reads is just a slower version of the same stall.

**Verify**

Create a genuine double-flag, then check that an inbox line appears within one run interval and names both loops and the PR id. After a human assigns the owner, confirm exactly one loop acts and the other logs a skip.

---

## Q5. Can I run four loops from day one, and in what order should I add them? [→ §7 Example: Safe Three-Loop Setup]

**What you see**

The plan is to switch on Daily Triage, PR Babysitter, Post-Merge Cleanup and CI Sweeper simultaneously in week one. It looks efficient on a slide. In practice the CI Sweeper retries the same unfixable failure all week, the Babysitter's worktrees pile up behind it, and nobody can tell which loop caused which change.

**Why**

Each loop needs its own guardrails proven before another one is added. A new action loop without proven **attempt limits** and a **verifier** will retry a red build indefinitely — the retry cap is what turns "CI is red" into "CI is red and we stopped trying". Adding loops in parallel multiplies the collisions from Q1 with none of the coordination already in place.

**What to do**

1. Start with three, at these levels and cadences:

| Loop | Level | Cadence |
|---|---|---|
| Daily Triage | L1 | 1d |
| PR Babysitter | L2 | 10m |
| Post-Merge Cleanup | L1 → L2 | 1d off-peak |

2. Add the CI Sweeper **only after** the PR Babysitter's attempt limits and verifier have held for two weeks.
3. Put loops on different clocks — active hours for the ones that touch branches, off-peak slots like `22:00` for cleanup — so they do not wake simultaneously.
4. Add each new loop's lock calls and `acting_on` write on day one, not after the first collision.

**Verify**

Before adding loop four, confirm two weeks of PR Babysitter history shows a bounded attempt count and no runaway retries. Then check `loop-run-log.md` shows clean lock acquire/release pairs for every action loop in the first week of parallel operation.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: README.md.*
