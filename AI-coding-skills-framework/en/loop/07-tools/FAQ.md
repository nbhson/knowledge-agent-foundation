# ❓ FAQ — Tools & Ecosystem (Real Stories, Plain Language)

If a question is unclear, read the section in `../README.md` (named in brackets).

---

## Q1. Do I have to hand-write every loop file, or is there a CLI that sets it all up? [→ §1 Front Door]

**What you see**

You have an idea for a daily triage loop and you're about to create seven files by hand: the skill, `STATE.md`, `loop-budget.md`, `loop-run-log.md`, the safety config. Two hours of copying from a blog post, and you'll probably miss one.

**Why**

You don't need to. The `loop` command is the **front door**: it scaffolds the skeleton and then tells you the next thing to do. Most people skip it because the old instructions and the new one look like different products — the docs even mention the legacy path still works, so nothing forces you to notice the new one.

**What to do**

1. Run the front door. One binary handles init, doctor and status.
2. Pick your pattern and your agent tool with the flags — `--tool` accepts `claude`, `codex`, `grok`, or `opencode`.
3. Then run `doctor .`. It combines the audit, the drift check and file checks into **the top 3 next actions**, so you don't have to guess what to do after scaffolding.
4. Add `--with-foundry` only if you want a versioned, composable runtime stack. Skip it on day one.

```
npx @cobusgreyling/loop init . --pattern daily-triage --tool grok
npx @cobusgreyling/loop doctor .
# legacy, still supported:  npx @cobusgreyling/loop-init .
```

**Verify**

`init` prints a **Loop Ready score** and the first loop command to run. Run `doctor` again — the top action should have moved from "create files" to something about your pattern, because the files now exist.

---

## Q2. What's the "Loop Ready score" and why is mine stuck below L3? [→ §2 loop-audit]

**What you see**

You score your project and get a number out of 100 — maybe 62. The docs call the top level **L3** (unattended: no human in the loop). The score refuses to go above a ceiling no matter how much you improve, and `audit` recommends `harness-foundry` when the number is high but `.foundry/stack.yaml` doesn't exist.

**Why**

The score grades **Loop Readiness** from L0 to L3, climbing from roughly 10 to 100 as you add the pieces. It's a credit score, not a vibe: low means don't let the loop run alone yet. The ceiling is deliberate — **L3 is capped** until three specific files exist. That's the tool refusing to certify you for unattended operation while you have no budget, no run history, and no written rules.

**What to do**

1. Run it with `--suggest` so it tells you which files are missing instead of just docking points.
2. Create the three required artefacts: `loop-budget.md`, `loop-run-log.md`, and a budget section inside `LOOP.md`.
3. Don't chase 100 before you run anything. A score of 60 with a real log beats 95 with an empty one.
4. Re-run after each real week, not every hour — the score should track what actually happened.

```
npx @cobusgreyling/loop audit . --suggest
missing: loop-budget.md, loop-run-log.md, LOOP.md budget section  -> L3 capped
```

**Verify**

Add the three files, re-run `audit`, and the L3 cap lifts. Then delete one file and confirm the cap comes back — the check is real, not decorative.

---

## Q3. How much will this loop cost before I schedule it every 15 minutes? [→ §3 loop-cost]

**What you see**

You are about to put a CI-sweeper loop on a 15-minute cadence at level L2 (assisted: a human still gates the risky parts). You have no idea whether that's $2 a month or $400.

**Why**

Nobody estimates, because the cost isn't visible until the invoice arrives — and by then you've scheduled it. Each run chains multiple sub-agent calls, and the multiplier is the *cadence times the level times the length of the work*. Guess wrong and you find out next week.

**What to do**

1. Ask the estimator before scheduling, giving it the three numbers that actually drive cost: pattern, cadence, level.
2. Write the estimate into `loop-budget.md` as a hard daily limit.
3. Run the cheap triage-only pass first — that's where most of the savings are, because most triage output is empty.
4. Set the rule that a loop which has no actionable findings **does not escalate to sub-agents**.

```
npx @cobusgreyling/loop cost --pattern ci-sweeper --cadence 15m --level L2
# full budget rules live in 04-operating/ — read them before a real schedule
```

**Verify**

Compare the estimate against the real spend after seven days. If the real number is double, you almost certainly have no early exit on an empty watchlist — add it and re-measure.

---

## Q4. The loop edited a file it was never supposed to touch. Can a tool block that, or does it only work if the agent obeys the rules? [→ §7 loop-gate + §6 loop-worktree]

**What you see**

Your safety file says `src/auth/**` is off-limits. The agent refactors it anyway, because a rule written in markdown is a suggestion, and the model was mid-flow. You find out in code review.

**Why**

Two different protections, and people confuse them. **loop-gate** is *mechanical enforcement*: it checks the path denylist and the auto-merge allowlist from `gate.yaml` **without depending on whether the loop ever read the safety file.** It answers yes at the moment the action is taken. **loop-worktree** is the other layer: the agent works in its own throwaway directory, so even a wrong edit never reaches your main code.

**What to do**

1. Put the denylist in `gate.yaml`, not only in a prose safety file.
2. Check the action *before* it happens, including the auto-merge path allowlist.
3. Read the exit code: **2 means escalate, 0 means proceed.** Any script chaining gates must honour 2.
4. Isolate the work anyway — one worktree per fix attempt, tracked in a manifest, discarded on reject or escalate.

```
npx @cobusgreyling/loop gate check --action auto-merge --paths src/auth/login.ts
# exit 2 = escalate (blocked)   exit 0 = proceed
npx @cobusgreyling/loop-worktree create --run-id <id> --pattern <p>
```

**Verify**

Ask the loop to touch a denylisted path. `gate check` exits 2, the escalation fires, and the main branch file's checksum is unchanged. If it exits 0, the denylist is not in `gate.yaml` — a markdown rule was doing the work.

---

## Q5. Two loops edited the same branch and we got merge conflicts and corrupted state. Which tool fixes that? [→ §6 lock/unlock + §8 loop-sandbox / loop-swarm]

**What you see**

Parallel collision: two sub-agents open the same files at the same time. You get a merge conflict, then a state file with two contradictory entries about the same PR. One of the agents had its work silently thrown away.

**Why**

Loops that write code need **isolation plus exclusion**. Isolation is `isolation: worktree` — each code-editing sub-agent gets its own git worktree, a private copy of the repo, so a failed attempt is discarded instead of corrupting the main tree. Exclusion is `lock`/`unlock` — loops don't enter the same room at the same time. `loop-sandbox` adds ephemeral isolation plus **patch capture**, saving changes as reviewable patch files before anything is applied. `loop-swarm` is the stricter version for multi-agent consensus: it requires **byte-identical patches** between runs before accepting any edit.

**What to do**

1. Every code-editing sub-agent gets `isolation: worktree`. No exceptions.
2. Acquire a lock and record it in state: `PR #1234 — worktree in progress`.
3. Release the lock on every exit path — success, reject, and escalate.
4. For high-risk edits, run `loop-swarm` so two independent runs must agree exactly.

```
npx @cobusgreyling/loop-sandbox run -- <cmd>   # ephemeral worktree + patch capture
# loop-swarm: accept the edit only on byte-identical patch consensus
```

**Verify**

Start two loops on the same PR deliberately. Exactly one holds the lock; the other waits or escalates. Both finish with zero merge conflicts, and the state file has one entry for that PR, not two.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: README.md.*