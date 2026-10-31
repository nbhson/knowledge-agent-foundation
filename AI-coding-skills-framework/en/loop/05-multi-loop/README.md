# 🔗 05. Multi-Loop Coordination

> **📌 Core Concept**
>
> **Definition:** Multi-loop coordination is **the traffic rules for many loops sharing one repo** — who owns which branch, separate state files, priority ranking when conflicts happen, and collision detection. The goal: many loops can run side by side without "fighting".
> **Analogy:** Think of an **intersection without traffic lights** — if every driver decides alone, everyone assumes they have priority, and you get gridlock and crashes. Red lights (locks), signs (state files), and priority rules keep all cars moving safely. Many loops in one repo are not bad by themselves — they only get dangerous when **there are no boundaries**.
> **Why it matters:** Once you have 2+ loops (for example Daily Triage + CI Sweeper), without coordination they can edit the same file, the same PR, or overwrite each other's data. This section helps you prevent that before you learn it the hard way.

> Running more than one loop in a repo is normal. Running them **without boundaries** is how loops fight each other. This section shows you how to coordinate them safely.

---

## 1. Principles

1. **One owner per branch** — at most one loop mutates a branch per hour.
2. **Separate state files** — `STATE.md` for triage; pattern-specific files for action loops.
3. **Triage reports, action loops execute** — Daily Triage L1 never competes with CI Sweeper fixes.
4. **Shared denylist** — copy the same path denylist into every LOOP.md.
5. **Aggregate token budget**.

---

## 2. Recommended State Layout

```
STATE.md                    # Daily Triage (priorities, human inbox)
pr-babysitter-state.md      # PR watcher
ci-sweeper-state.md         # Active CI failures + attempt counts
dependency-sweeper-state.md # In-flight package updates
post-merge-state.md         # Cleanup backlog
loop-run-log.md             # Append-only observability
```

Linear / GitHub Projects work just as well — the loop must **read and write** the same store every run.

---

## 3. Priority When Loops Conflict

> **Easy way to read it:** When two loops want to do the same thing, the more urgent one wins — red CI (loop 1) blocks everything because nobody can merge. Please read the rows top to bottom as a priority ladder: when there is a conflict, the higher loop wins and the lower loop steps back.

| Priority | Loop | Reason |
|----------|------|-------|
| 1 | CI Sweeper | Red main blocks everything |
| 2 | PR Babysitter | Active PRs are time-sensitive |
| 3 | Dependency Sweeper | Pauses when CI is red |
| 4 | Post-Merge Cleanup | Off-peak, lowest urgency |
| 5 | Daily Triage | Reports only at L1; coordinates the others |

---

## 4. Scheduler Coordination

Document this in the root `LOOP.md`:

```markdown
## Multi-loop schedule
- CI Sweeper: /loop 15m (active hours)
- PR Babysitter: /loop 10m (active hours, skip if CI Sweeper is acting on the same PR)
- Daily Triage: /loop 1d 08:00
- Dependency Sweeper: /loop 6h (skip if main CI is red)
- Post-Merge: /loop 1d 22:00
```

---

## 5. Collision Detection

> **Easy way to read it:** Collision detection means "**look before you cross the road**" — every loop writes `acting_on` (what it is working on) into its state. Before starting work, the loop **reads** the other states to make sure nobody else is doing the same thing. The `loop-worktree lock/unlock` tool turns this from a polite agreement into real mechanical locks (advisory locks).

Every action loop should write `acting_on: branch-or-pr-id` in its state file. Before spawning a fix:

1. Read all other pattern state files
2. If another loop's `acting_on` matches → skip and log to `loop-run-log.md`

**`loop-worktree` encodes this as an advisory lock** instead of a self-check convention:

> 📄 **Example code:** [`examples/01-5-collision-detection.sh`](examples/01-5-collision-detection.sh)

`loop-worktree create` does not check locks itself — these two commands are paired by convention in the control script.

`loop-sandbox` follows the same convention via the `--lock-paths` option (opt-in) — a one-shot sandboxed agent run is also a control script that can collide with a scheduled loop.

---

## 6. Human Inbox

Use a shared section in `STATE.md`:

```markdown
## Human Inbox (ambiguous / cross-loop)
- [ ] PR #42: flagged by both CI Sweeper and PR Babysitter — human picks the owner
```

---

## 7. Example: Safe Three-Loop Setup

| Loop | Level | Cadence |
|------|-------|---------|
| Daily Triage | L1 | 1d |
| PR Babysitter | L2 | 10m |
| Post-Merge Cleanup | L1 → L2 | 1d off-peak |

Please add CI Sweeper **only after** the PR Babysitter's attempt limits and verifier have worked well for two weeks.

---

## 8. Real-World Lessons

- [stories/multi-loop-collision.md](https://github.com/cobusgreyling/loop-engineering/blob/main/stories/multi-loop-collision.md) — two loops fighting over the same branch
- [stories/dependency-vs-ci-sweeper-collision.md](https://github.com/cobusgreyling/loop-engineering/blob/main/stories/dependency-vs-ci-sweeper-collision.md) — Dependency Sweeper colliding with CI Sweeper

---

*Next: [06 — Anti-Patterns & Failure Modes](../06-anti-patterns/) → [07 — Tools & Ecosystem](../07-tools/)*
