# ❓ FAQ — Loop CLI (Real Stories, Plain Language)

If a question is unclear, read the section in `../README.md` (named in brackets).

---

## Q1. I copy the same STATE.md and LOOP.md into every new project — is there one command that writes them for me? [→ Overview of the Commands]

**What you see**

You open project number two and you are hand-creating the same files again: `STATE.md`, `LOOP.md`, budget files, safety config. The case study in this README puts that at **about 30 minutes per project**. Every copy comes out slightly different, so a loop that behaved well last month misbehaves today, and there is nothing to diff against.

**Why**

`harness/` and `loop/` teach you the structure but never write the files. Loop CLI is the materialization layer — one binary that creates the skills, state and budget files and then tells you how ready your loop is. The CLI name is "Loop CLI", short for command-line interface; every command is run through `npx`, which downloads and runs the package without a global install.

**What to do**

1. Run the front-door command from the project root. It scaffolds, prints the Loop Ready score, and prints the first loop command to run next.
2. Follow it with `loop doctor .` — it merges audit, sync and file checks into **top-3 next actions** instead of a wall of warnings.
3. Set `--tool` to the coding agent you actually use: `claude`, `codex` or `opencode`. Leave it at `grok` only if that is your agent.
4. Add `--with-foundry` if you want an additional, versioned harness scaffolded next to the default one.

```bash
npx @cobusgreyling/loop init . --pattern daily-triage --tool grok
npx @cobusgreyling/loop doctor .
npx @cobusgreyling/loop status .
```

**Verify**

`loop init` prints a Loop Ready score plus one runnable command, and `loop doctor .` returns at most three actions. If either prints nothing useful, you are not in the project root. Older setups can keep calling the standalone `npx @cobusgreyling/loop-init .`, but the README recommends the single-binary form for all three jobs.

---

## Q2. My audit score sits near 10 out of 100 and never climbs past L3 — what exactly am I missing? [→ `loop audit` — Loop Readiness Score]

**What you see**

```text
$ npx @cobusgreyling/loop audit . --suggest
Loop Readiness: ~10/100   (L0)
```

You tidy the files, re-run, and the number barely moves. Frustrating, because it looks like the tool is grading your code. It is not — it is grading the scaffold.

**Why**

The score is **Loop Readiness**, graded L0 to L3, and it moves from roughly 10 toward 100 only when the scaffold is complete. The L3 cap is deliberate: the audit will not award full readiness until the loop can report its own cost and its own history, because an unattended loop without either cannot be trusted. The case study in this README states the contrast plainly — without Loop CLI, scoring is simply "no way to measure"; with `loop audit`, the score moves from about 10 to 100. `--suggest` is what turns that number into a to-do list.

**What to do**

1. Create `loop-budget.md` — the ceiling for what one run may spend.
2. Create `loop-run-log.md` — one line per execution, with its result.
3. Add the budget section inside `LOOP.md` itself. A separate budget file is not enough; the loop reads the section.
4. Re-run with `--suggest` so the audit names the missing item instead of leaving you to guess.

```bash
npx @cobusgreyling/loop audit . --suggest
# expect: loop-budget.md exists
# expect: loop-run-log.md exists
# expect: budget section inside LOOP.md
```

**Verify**

The grade reaches **L3** only when all three exist; delete any one of them and it drops back. The score also covers constraints, governance and the **Harness Runtime** (version 1.7), so treat it as a checklist of missing scaffolding — never as a quality score for your prompts.

---

## Q3. I put a loop on a 15-minute schedule and the invoice surprised me — can I see the cost before it runs? [→ `loop cost` — Token Estimation]

**What you see**

The loop runs every 15 minutes at readiness level `L2`. A week later the provider bill is far larger than expected and you cannot explain it, because you never measured a single run.

**Why**

Token spend is only knowable in advance if you model it from three inputs: the pattern, the cadence and the readiness level. `loop cost` does exactly that — it is an estimate, not a meter, so it is only honest if you feed it the same values the scheduler will use. The README is blunt about why: the point is to avoid being shocked by the bill next week.

**What to do**

1. Estimate first, schedule second. Run the estimate before you write the timer entry, not after the first surprise.
2. Pass the real pattern name (`ci-sweeper`), the real cadence (`15m`) and the real level (`L2`). A mismatch describes a loop you are not running.
3. Compare `L1` against `L3` at the same cadence before committing. More context per iteration usually costs more than it returns.
4. Re-run the estimate whenever you change the pattern, the cadence or the level. A stale estimate is worse than none, because it looks like a measurement.
5. Do the arithmetic yourself — this is the part the tool will not do for you.

```bash
npx @cobusgreyling/loop cost \
  --pattern ci-sweeper --cadence 15m --level L2
```

**Verify**

Multiply the per-run estimate by **96** for one day at 15-minute cadence, then by **30** for a month. If that monthly figure is not already a line item you budgeted, lower the cadence or the level now — before the scheduler is live.

---

## Q4. Weeks in, the agent acts on information that no longer matches the project — how do I catch that? [→ `loop sync` — Drift Detection / `loop context` — Memory + Circuit Breaker]

**What you see**

`STATE.md` says the database migration finished. `LOOP.md` still lists it as open work. The loop faithfully re-runs the same step every cycle, and the context grows on each iteration until the run is mostly a transcript of itself.

**Why**

Two separate failures, both invisible while you watch a single run. The first is **drift**: `STATE.md` and `LOOP.md` are two files that describe the same reality, and they diverge over time. The second is unbounded growth: a long run keeps every iteration in context unless something actively prunes it. Neither shows up in a screenshot; both show up weeks later as a loop that confidently repeats yesterday's work.

**What to do**

1. Run `loop sync .` on a schedule. It compares `STATE.md` against `LOOP.md` and reports exactly where they disagree.
2. Run `loop context --check --ledger run.json` for long runs. It is a stateful memory manager and a circuit breaker: it keeps context from growing without bound across iterations and records each run into the ledger file `run.json`.
3. Chain both on the same exit-code convention as the gate (see Q5), so drift stops the loop instead of only printing a warning nobody reads.
4. Treat a disagreement as a bug in your process, not in the files. One of the two is out of date, and the loop cannot tell which.

```bash
npx @cobusgreyling/loop sync .
npx @cobusgreyling/loop context --check --ledger run.json
```

**Verify**

After `loop sync`, both files list the same open items. After `loop context --check`, `run.json` records the current iteration and the context size stays flat across repeated runs rather than climbing every cycle.

---

## Q5. The agent promises it will not touch protected paths, and three loops keep overwriting each other — can the tooling stop both? [→ `loop gate` / `loop worktree` / `loop-sandbox` & `loop-swarm`]

**What you see**

Two failures at once. A loop finishes and merges changes you never approved, because the rule lived in a safety markdown file the agent was supposed to read. Meanwhile developer A runs a loop in one directory and developer B runs another, and both write to the main branch.

**Why**

Both are enforcement problems, not intelligence problems. A rule written in prose is a suggestion the model may skip; a rule held in `gate.yaml` and read by a command is a wall. And loops sharing one working directory have no way to see each other at all.

**What to do**

1. Move the path denylist and the auto-merge allowlist into `gate.yaml`.
2. Run `loop gate check` in continuous integration (CI) before every merge. Exit code `2` means escalate; `0` means proceed — the same convention as `loop context --check`, so both chain cleanly.
3. Give each attempt its own isolated git worktree with `loop-worktree create --run-id <id> --pattern <p>`, then use `lock` / `unlock` on the shared branch scope.
4. For several agents at once, use `loop-swarm`: it only accepts edits when the patch is **byte-identical** across runs.
5. Wrap risky commands in `loop-sandbox run -- <cmd>`; it captures changes into reviewable patch files before they are applied.

```bash
npx @cobusgreyling/loop gate check --action auto-merge --paths src/,tests/
npx @cobusgreyling/loop-worktree lock --scope refs/heads/main
```

**Verify**

Point `gate check` at a denied path on purpose and confirm CI sees exit `2`. Then confirm no two live worktrees share a run ID, and that a rejected attempt's worktree is cleaned up rather than left behind.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: README.md.*