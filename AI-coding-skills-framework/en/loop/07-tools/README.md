# 🧰 07. Tools & Ecosystem

> **📌 Core Concept**
>
> **Definition:** This is the **CLI toolbox** and ecosystem around loop-engineering — the `npx @cobusgreyling/loop-*` commands for every stage: creating (`init`), scoring (`audit`), estimating cost (`cost`), spotting state drift (`sync`), isolating changes (`worktree`), and enforcing safety (`gate`).
> **Analogy:** Think of an **electrician's toolbox** — you don't need to know how every screwdriver is built inside. You just need to know which tool fits which job: the wire wrench (init), the meter (cost), the pliers (gate). One tool per job, and they work well together.
> **Why it matters:** These tools turn loop engineering from good intentions into automatic habits — they enforce the things people tend to skip (locking, blocking denylist paths), and give you a clear "Loop Ready score" instead of a vague feeling of "probably fine".

> You don't need to hand-write loop code from scratch — there is an open-source CLI system (`@cobusgreyling/loop-*`) to support every stage. This section introduces each tool and the wider ecosystem. (`npx` = download and run a Node.js package without installing it globally.)

---

## 1. Front Door — `loop init / doctor / status`

This section explains where to start: the one command that creates your loop files and checks your setup.

> **Easy way to read it:** `init` gives your repo a ready-made loop skeleton (skills, state, budget); `doctor` is a friendly health check that tells you the next 3 things to do. Please start every loop project here — no need to build by hand.

> 📄 **Example code:** [`examples/01-1-front-door-loop-init-doctor-status.sh`](examples/01-1-front-door-loop-init-doctor-status.sh)

`loop init` (or `loop-init`) scaffolds the skills, state, and budget files (*scaffold = generates the starter files for you*), then prints the **Loop Ready score** and the first loop command. `loop doctor` combines audit + sync + file checks into the top-3 next actions. Switch `--tool` to `claude`, `codex`, or `opencode`. Use `--with-foundry` when you want the loop to be a composable runtime stack.

> **One-line summary:** Start every loop with `loop init` (create the files) and `loop doctor` (what to do next).

---

## 2. loop-audit — Loop Readiness Score

This section explains the scoring tool: how ready your loop really is, as a number.

> **Easy way to read it:** `audit` grades your setup like an exam — it gives you a 0–100 score for production readiness. Like a credit score: a low score means don't let the loop run alone yet. The score goes up as you add the right pieces.

> 📄 **Example code:** [`examples/02-2-loop-audit-loop-readiness-score.sh`](examples/02-2-loop-audit-loop-readiness-score.sh)

Scores your project's **Loop Readiness** (L0→L3) — a single number that climbs from ~10 to 100 as you scaffold the pieces correctly. Includes constraints + governance + **Harness Runtime** (v1.7). Caps **L3** (*L3 = unattended: no human in the loop*) until `loop-budget.md`, `loop-run-log.md`, and a LOOP.md budget section exist.

> **One-line summary:** `audit` is your readiness credit score — L3 stays locked until budget, run log, and written rules exist.

---

## 3. loop-cost — Token Estimation

This section explains the cost tool: how much a scheduled loop will cost, before you schedule it.

> 📄 **Example code:** [`examples/03-3-loop-cost-token-estimation.sh`](examples/03-3-loop-cost-token-estimation.sh)

Estimates token spend **before scheduling** (*token = the unit of text the model reads and writes; you pay per token*) — so you avoid a surprise bill next week. See full budget rules in [04-operating](../04-operating/).

> **One-line summary:** Ask `loop cost` before you schedule — it predicts the bill from pattern, cadence, and level.

---

## 4. loop-sync — Drift Detection

This section explains the consistency tool: catching when two files describing the same loop disagree.

> 📄 **Example code:** [`examples/04-4-loop-sync-drift-detection.sh`](examples/04-4-loop-sync-drift-detection.sh)

Detects drift between `STATE.md` and `LOOP.md` — two files that describe the loop's state and configuration but can slowly drift apart over time (*drift = they stop matching, like two copies of a document edited by different people*).

> **One-line summary:** `loop sync` catches the moment your state file and your rules file stop telling the same story.

---

## 5. loop-context — Memory + Circuit Breaker

This section explains the memory tool: keeping long runs from drowning in their own history.

> 📄 **Example code:** [`examples/05-5-loop-context-memory-circuit-breaker.sh`](examples/05-5-loop-context-memory-circuit-breaker.sh)

Stateful memory manager + circuit breaker for long runs (*circuit breaker = an automatic stop switch, like the one in your fuse box, that trips when a run goes haywire*). Keeps context from growing out of control across iterations.

> **One-line summary:** `loop context` remembers what matters across runs and cuts off a run before its context overflows.

---

## 6. loop-worktree — Change Isolation

This section explains the isolation tool: protecting your main code from a failed fix attempt.

> **Easy way to read it:** `worktree` gives each fix attempt a "private practice room" — the agent edits in its own room, and if it fails that room is thrown away without ever touching the main code. It also has `lock/unlock` so two loops don't walk into the same room at once.

> 📄 **Example code:** [`examples/06-6-loop-worktree-change-isolation.sh`](examples/06-6-loop-worktree-change-isolation.sh)

Manages isolated git worktrees per fix attempt (*a git worktree = a private copy of the repo in its own folder*) — one worktree per attempt, tracked in a manifest, cleaned up on reject/escalate. Comes with `lock`/`unlock` for multi-loop coordination (see [05-multi-loop](../05-multi-loop/)).

> **One-line summary:** One private worktree per fix attempt, plus a lock, so failed attempts are thrown away and loops never collide.

---

## 7. loop-gate — Mechanical Enforcement

This section explains the safety tool: a real block, not a request the agent can ignore.

> 📄 **Example code:** [`examples/07-7-loop-gate-mechanical-enforcement.sh`](examples/07-7-loop-gate-mechanical-enforcement.sh)

Mechanically enforces the path denylist (*denylist = a blacklist of paths the loop must never touch*) + auto-merge allowlist (*allowlist = a whitelist of paths auto-merge is allowed on*) from `gate.yaml` — it does not depend on whether the loop has read the safety file. Exit `2` = escalate, `0` = proceed — the same convention `loop-context --check` uses, so control scripts can chain both.

> **One-line summary:** `loop gate` checks every action against `gate.yaml` at the moment it happens — exit 2 blocks and escalates, exit 0 proceeds.

---

## 8. loop-sandbox & loop-swarm — Isolation + Consensus

This section explains the two strictest tools: throwaway environments, and edits that need two agreeing runs.

> 📄 **Example code:** [`examples/08-8-loop-sandbox-loop-swarm-isolation-consensus.sh`](examples/08-8-loop-sandbox-loop-swarm-isolation-consensus.sh)

- **loop-sandbox**: Ephemeral git worktree isolation for single agent runs (*ephemeral = created for one run, deleted after*). Captures changes as reviewable patch files before applying them (*patch = a small file listing exactly which lines changed*).
- **loop-swarm**: Multi-agent consensus sandboxing across sequential `loop-sandbox` runs. Requires **byte-identical patch consensus** between runs before accepting edits (*byte-identical = the two runs produced exactly the same characters — no "close enough"*).

> **One-line summary:** `sandbox` runs edits in a throwaway copy and saves them as reviewable patches; `swarm` only accepts an edit when two independent runs produce identical patches.

---

## 9. Other Tools

This section lists the remaining tools in one table.

| Tool | Description | Command |
|------|-------|------|
| **loop-action** | GitHub Composite Action running loops in CI | `uses: cobusgreyling/loop-engineering/tools/loop-action@main` |
| **loop-mcp-server** | Patterns/skills/state/budget/safety docs as MCP resources | `npx @cobusgreyling/loop-mcp-server` |
| **loop-cost** | Token spend estimator | `npx @cobusgreyling/loop-cost` |

> **How to read it:** **Tool** = the name. **Description** = what it does in one line — for example, loop-action runs your loop inside GitHub Actions CI (CI = automated builds/tests that run on every push). **Command** = the exact line you run or paste to use it.

**Reference MCP server**: the repo ships `tools/mcp-server/` — patterns, skills, state, budget, and safety docs as runtime-queryable MCP resources (MCP = a standard protocol that lets an agent fetch documents and call tools; here it means the agent can query these docs instead of you pasting them into the prompt — *reducing prompt stuffing*). Config example: `examples/mcp/loop-engineering.mcp.json`.

> **One-line summary:** Three extras: run loops in CI (loop-action), serve docs to the agent over MCP (loop-mcp-server), and estimate cost (loop-cost).

---

## 10. Ecosystem Stack

This section shows how loop-engineering fits into a bigger family of projects, from memory to fleets of agents.

```
memory-engineering → loop-engineering → harness-foundry → outerloop → fleet-engineering
   (persist)            (patterns)         (runtime)        (verdict)     (population)
```

| Layer | You get | Start |
|-------|---------------|-------|
| **Memory** | Tiers, recall budget, Memory Ready score | [memory-engineering](https://github.com/cobusgreyling/memory-engineering) |
| **Design** (loop-engineering repo) | Patterns, starters, Loop Ready score | `npx @cobusgreyling/loop init .` then `loop doctor .` |
| **Runtime** | Versioned harness, traces, evolution | `npx @cobusgreyling/loop init . --with-foundry` or the [harness-foundry showcase](https://github.com/cobusgreyling/harness-foundry) |
| **Govern** | Evidence, verdict, answerability | [outerloop](https://github.com/cobusgreyling/outerloop) |
| **Fleet** | Registry, inbox, budgets, kill switch | `npx @cobusgreyling/fleet-init .` |

> **How to read it:** each row is one layer of the stack. **Layer** = which job it does (Memory = the agent remembers between sessions; Design = you create the loops; Runtime = the loops run on a versioned engine; Govern = outputs are judged with evidence; Fleet = you manage many agents at once). **You get** = the features. **Start** = the command or link to begin.

### Companion Projects

| Companion | Description |
|-----------|-------------|
| [Goal Engineering](https://github.com/cobusgreyling/goal-engineering) | Loops discover, goals complete — `/goal` + stack cookbook |
| [Memory Engineering](https://github.com/cobusgreyling/memory-engineering) | Stop re-explaining your repo — tiers, budget, Memory Ready score |
| [Fleet Engineering](https://github.com/cobusgreyling/fleet-engineering) | Governing populations of agents — registry, inbox, kill switch |
| [harness-foundry](https://github.com/cobusgreyling/harness-foundry) | Companion runtime — versioned stacks, sessions, traces |
| [outerloop](https://github.com/cobusgreyling/outerloop) | Companion governance — evidence → verdict → answerability |

> **How to read it:** each row is a sibling project. **Companion** = its name (a link). **Description** = the one-line job it does for you — for example, Memory Engineering means you stop re-pasting your repo's context into every session.

> **One-line summary:** Five sibling projects, one job each — goals, memory, fleets, runtime, and governance.

### When to Add What

- When agents **forget between sessions** → add memory-engineering.
- When the team has **many agents/loops** → add fleet-engineering.
- Next after **Loop Ready 80+** → version your loop as a harness (`loop-init` prints the CTA automatically; `loop-audit` recommends Foundry when the score is strong but `.foundry/stack.yaml` is missing).

> **One-line summary:** The stack grows by need — memory when agents forget, fleet when there are many loops, Foundry when your readiness score is high enough to formalize.

---

## October 2026 Update — Alternative Toolchain & Comparison

> **One-line summary:** Same loops, other schedulers — this update compares cron, GitHub Actions, Temporal, Airflow and asyncio, and when each fits.

### Comparing Loop Scheduling Approaches

| Approach | Characteristics | Best fit |
|----------|----------|-------------|
| **Shell script + cron** | Simplest, no deps, runs right on your machine | Personal loops, demos, environments that already have cron |
| **GitHub Actions** | Hosted, free tier, event-driven (cron + PR/issue triggers) | Repo-tied loops, small teams that want zero infra |
| **Temporal** | Durable execution, native checkpoint/resume | Long-running agents — stop/resume without losing state |
| **Airflow** | Data pipelines, complex DAGs, dependency graphs | Data/ML pipelines with many interdependent steps |
| **Python asyncio scheduler** (in-process) | Runs in the same process as the app | Hundreds of loops in a single self-managed service |

> **How to read it:** this table compares ways to *trigger* a loop on a schedule. **Approach** = the scheduler. **Characteristics** = what it's good and bad at — for instance, cron = the classic Unix timer that runs a command at fixed times; Temporal's "durable execution" = a run can stop and resume later without losing its state. **Best fit** = when to choose it.

> **One-line summary:** Five ways to trigger a loop, from a one-line cron job to full orchestration — pick the simplest that fits.

### When to Choose What

- **1–2 runs per day** → cron or GitHub Actions is enough; don't over-engineer.
- **Long-running checkpoint/resume** → Temporal — durable execution was built for this.
- **ML / data pipelines** → Airflow with a clear DAG per step (DAG = a dependency graph: step B runs only after step A finishes).
- **Hundreds of loops** → a dedicated orchestrator (Kestra, Temporal, fleet-engineering).

> **One-line summary:** Match the scheduler to scale: cron or GitHub Actions for light use, Temporal for resumable runs, Airflow for data pipelines.

> **📌 Note:** The `loop-*` CLIs introduced above are currently **one option**, not a requirement. The patterns in [02-patterns](../02-patterns/) run on **every scheduler** in the table above — a pattern is process + metrics + safety gates, and the scheduler is just how it gets triggered.

### See Also

- [harness — 10. Automation](../../harness/10-automation/README.md) — scheduler patterns in detail.
- [AGENT_SYSTEM_ARCHITECTURE.md](../../AGENT_SYSTEM_ARCHITECTURE.md) — Layer 5 (automation in the overall architecture).

> **One-line summary:** Any scheduler works — pick cron or GitHub Actions for simple loops, Temporal/Airflow for long or complex runs; the loop pattern itself doesn't change.

---

*Back to [README](../README.md) — Module XII overview*
