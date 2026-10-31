# 🔗 05. Multi-Loop Coordination

> **📌 Core Concept**
>
> **Definition:** Multi-loop coordination is **the traffic rules for many loops sharing one repo** — who owns which branch, separate state files, priority ranking when conflicts happen, and collision detection. The goal: many loops can run side by side without "fighting".
> **Analogy:** Think of an **intersection without traffic lights** — if every driver decides alone, everyone assumes they have priority, and you get gridlock and crashes. Red lights (locks), signs (state files), and priority rules keep all cars moving safely. Many loops in one repo are not bad by themselves — they only get dangerous when **there are no boundaries**.
> **Why it matters:** Once you have 2+ loops (for example Daily Triage + CI Sweeper), without coordination they can edit the same file, the same PR, or overwrite each other's data. This section helps you prevent that before you learn it the hard way.

> Running more than one loop in a repo is normal. Running them **without boundaries** is how loops fight each other. This section shows you how to coordinate them safely.
> (Glossary: a **loop** = an agent task that runs on a schedule. **Branch** = an independent line of work in git. **State file** = one loop's memory between runs. **Denylist** = "blacklist" — paths no loop may touch. **Lock** = a shared flag letting only one loop proceed.)

---

## 1. Principles

Signpost: these five rules are the whole section in miniature — everything after is one of them in detail.

1. **One owner per branch** — at most one loop mutates a branch per hour. (mutates = changes, e.g. pushes commits or rebases.)
2. **Separate state files** — `STATE.md` for triage; pattern-specific files for action loops.
3. **Triage reports, action loops execute** — Daily Triage L1 never competes with CI Sweeper fixes. (L1 = report-only level.)
4. **Shared denylist** — copy the same path denylist into every LOOP.md.
5. **Aggregate token budget**. (aggregate = sum the budget across *all* loops, not per loop — three loops at 700k each is still 2.1M total.)

> **One-line summary:** Five rules: one owner per branch, separate state, reporters don't edit, one shared denylist, one combined budget.

## 2. Recommended State Layout

Signpost: this shows which file each loop writes to — one memory file per loop, so they never overwrite each other.

```
STATE.md                    # Daily Triage (priorities, human inbox)
pr-babysitter-state.md      # PR watcher
ci-sweeper-state.md         # Active CI failures + attempt counts
dependency-sweeper-state.md # In-flight package updates
post-merge-state.md         # Cleanup backlog
loop-run-log.md             # Append-only observability
```
(How to read it: each line = one file and its owner. For instance, `ci-sweeper-state.md` belongs to the CI Sweeper loop and tracks which build failures it is retrying. The only genuinely shared file is `loop-run-log.md`, which is append-only — new lines are added, old lines are never edited.)

Linear / GitHub Projects work just as well — the loop must **read and write** the same store every run. (A store it only writes is a log; a store it only reads is a stale snapshot.)

> **One-line summary:** One state file per loop, one shared append-only log — that's the layout that prevents overwrites.

## 3. Priority When Loops Conflict

> **Easy way to read it:** When two loops want to do the same thing, the more urgent one wins — red CI (loop 1) blocks everything because nobody can merge. Please read the rows top to bottom as a priority ladder: when there is a conflict, the higher loop wins and the lower loop steps back.

| Priority | Loop | Reason |
|----------|------|-------|
| 1 | CI Sweeper | Red main blocks everything |
| 2 | PR Babysitter | Active PRs are time-sensitive |
| 3 | Dependency Sweeper | Pauses when CI is red |
| 4 | Post-Merge Cleanup | Off-peak, lowest urgency |
| 5 | Daily Triage | Reports only at L1; coordinates the others |

> **One-line summary:** When loops collide, the higher-ranked loop wins and the lower one skips — red CI on main always goes first.

---

## 4. Scheduler Coordination

Signpost: this is where the priority rules become mechanical — written into the shared schedule file so no loop has to "remember" them.

Document this in the root `LOOP.md`:

```markdown
## Multi-loop schedule
- CI Sweeper: /loop 15m (active hours)
- PR Babysitter: /loop 10m (active hours, skip if CI Sweeper is acting on the same PR)
- Daily Triage: /loop 1d 08:00
- Dependency Sweeper: /loop 6h (skip if main CI is red)
- Post-Merge: /loop 1d 22:00
```
(How to read it: each line = one loop, its `/loop` run interval, and its skip condition. For instance, the Dependency Sweeper line says "run every 6 hours, but skip if CI on main is red" — the priority ladder from §3, written down as a rule.)

> **One-line summary:** Write every skip condition into the shared `LOOP.md` schedule, so coordination is mechanical rather than remembered.

## 5. Collision Detection

> **Easy way to read it:** Collision detection means "**look before you cross the road**" — every loop writes `acting_on` (what it is working on) into its state. Before starting work, the loop **reads** the other states to make sure nobody else is doing the same thing. The `loop-worktree lock/unlock` tool turns this from a polite agreement into real mechanical locks (advisory locks).

Every action loop should write `acting_on: branch-or-pr-id` in its state file. Before spawning a fix:

1. Read all other pattern state files
2. If another loop's `acting_on` matches → skip and log to `loop-run-log.md`

**`loop-worktree` encodes this as an advisory lock** instead of a self-check convention:

> 📄 **Example code:** [`examples/01-5-collision-detection.sh`](examples/01-5-collision-detection.sh)

`loop-worktree create` does not check locks itself — these two commands are paired by convention in the control script.

`loop-sandbox` follows the same convention via the `--lock-paths` option (opt-in) — a one-shot sandboxed agent run is also a control script that can collide with a scheduled loop. (one-shot = runs once on demand, not on a schedule; opt-in = you must switch the option on yourself.)

> **One-line summary:** Every loop announces what it's working on (`acting_on`) and checks the others before starting — plus real locks to make it enforceable.

---

## 6. Human Inbox

Signpost: when two loops both correctly step back and nobody owns the item, it needs a place to wait for a person.

Use a shared section in `STATE.md`:

```markdown
## Human Inbox (ambiguous / cross-loop)
- [ ] PR #42: flagged by both CI Sweeper and PR Babysitter — human picks the owner
```
(In plain terms: the inbox is a to-do list for humans. Here, both loops saw PR #42, both stepped back, so the loop wrote one line asking a person to pick an owner.)

> **One-line summary:** Ambiguous or contested items go to a "human inbox" list — a loop that can't claim ownership writes there and exits.

---

## 7. Example: Safe Three-Loop Setup

Signpost: this is the recommended starter set — which loops to run first, at which autonomy level and cadence.

How to read it: "Loop" = which loop; "Level" = autonomy level (L1 report-only, L2 assisted fixes); "Cadence" = how often it runs. For instance, the PR Babysitter row: it may draft small fixes (L2), checked every 10 minutes during active hours.

| Loop | Level | Cadence |
|------|-------|---------|
| Daily Triage | L1 | 1d |
| PR Babysitter | L2 | 10m |
| Post-Merge Cleanup | L1 → L2 | 1d off-peak |

Please add CI Sweeper **only after** the PR Babysitter's attempt limits and verifier have worked well for two weeks.

> **One-line summary:** Start with three loops (report, babysit, clean), and add the fourth only after two weeks of proven guardrails.

---

## 8. Real-World Lessons

Signpost: two real incident write-ups (stories = post-mortems of things that actually happened).

- [stories/multi-loop-collision.md](https://github.com/cobusgreyling/loop-engineering/blob/main/stories/multi-loop-collision.md) — two loops fighting over the same branch
- [stories/dependency-vs-ci-sweeper-collision.md](https://github.com/cobusgreyling/loop-engineering/blob/main/stories/dependency-vs-ci-sweeper-collision.md) — Dependency Sweeper colliding with CI Sweeper

> **One-line summary:** Both linked stories are real collisions of the kind this section prevents — worth reading before you run loop two.

*Next: [06 — Anti-Patterns & Failure Modes](../06-anti-patterns/) → [07 — Tools & Ecosystem](../07-tools/)*
