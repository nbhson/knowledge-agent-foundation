# 🔗 05. Multi-Loop Coordination

> **📌 Core Concept**
>
> **Definition:** Multi-loop coordination is **the traffic rules for many loops sharing one repo** — branch ownership, separate state files, priority ranking on conflict, and collision detection. Goal: many loops running in parallel without "fighting".
> **Analogy:** Like an **intersection with no traffic lights** — if every driver decides for themselves, everyone thinks they have priority, and gridlock and accidents follow. The red light (locks), the signs (state files), and the priority ranking keep all cars moving safely. A repo with many loops is not inherently bad — it's only dangerous when **there are no boundaries**.
> **Why it matters:** Once you have 2+ loops (say Daily Triage + CI Sweeper), without coordination they'll edit the same file, the same PR, or lose each other's data. This section prevents that before you have to learn it from mistakes.

> Running more than one loop in a repo is normal. Running them **without boundaries** is how loops fight each other. This section guides safe coordination.

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

Linear / GitHub Projects work equivalently — the loop must **read and write** the same store every run.

---

## 3. Priority When Loops Conflict

> **Easy way to read it:** When two loops want to do the same thing, the one that is more "on fire" wins — red CI (loop 1) blocks everything because no one can merge to the repo. Read the rows top to bottom as a priority ladder: on conflict, the higher-ranked loop wins; the lower-ranked loop yields.

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

> **Easy way to read it:** Collision detection is "**looking before crossing the road**" — every loop writes `acting_on` (what it's doing) to its state; before starting work, the loop **reads** the other states to be sure nobody else is doing the same thing. The `loop-worktree lock/unlock` tool turns this into mechanical locks (advisory locks) instead of relying on self-discipline.

Every action loop should write `acting_on: branch-or-pr-id` in its state file. Before spawning a fix:

1. Read all other pattern state files
2. If another loop's `acting_on` matches → skip and log to `loop-run-log.md`

**`loop-worktree` encodes this as an advisory lock** instead of a self-check convention:

```bash
# In the loop's control script, before spawning a worktree:
npx @cobusgreyling/loop-worktree lock --paths <globs> --owner <pattern>
# After finishing:
npx @cobusgreyling/loop-worktree unlock --owner <pattern>
```

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

Add CI Sweeper **only after** the PR Babysitter's attempt limits and verifier have been proven for two weeks.

---

## 8. Real-World Lessons

- [stories/multi-loop-collision.md](https://github.com/cobusgreyling/loop-engineering/blob/main/stories/multi-loop-collision.md) — two loops fighting over the same branch
- [stories/dependency-vs-ci-sweeper-collision.md](https://github.com/cobusgreyling/loop-engineering/blob/main/stories/dependency-vs-ci-sweeper-collision.md) — Dependency Sweeper colliding with CI Sweeper

---

*Next: [06 — Anti-Patterns & Failure Modes](../06-anti-patterns/) → [07 — Tools & Ecosystem](../07-tools/)*
