# 🔁 Loop CLI — The Command-Line Toolset for Loop & Harness Runtime

> ## 📑 Table of Contents
>
> - [The Opening Story](#the-opening-story)
> - [Why Loop CLI Matters?](#why-loop-cli-matters)
> - [Relationship to the Harness](#relationship-to-the-harness)
> - [Overview of the Commands](#overview-of-the-commands)
> - [Learning Roadmap (Directory Structure)](#learning-roadmap-directory-structure)
> - [Real-World Case Studies](#real-world-case-studies)
> - [Reference Materials](#reference-materials)

---

### The Opening Story

This section explains the pain Loop CLI removes: hand-setting up the same loop files for every project.

You have finished designing a full harness in `harness/` — context, memory, guardrails, evaluation. You have learned that loops are the right way to run it. But each loop still needs **setup by hand**: making `STATE.md`, `LOOP.md`, budget files, safety settings, isolated worktrees...

Plain glosses: `STATE.md` = a file tracking where the work stands. `LOOP.md` = the loop's instructions and rules. Budget files = caps on how many tokens or dollars a loop may spend. Worktree = a separate working copy of the repo where one attempt runs without touching the main branch.

Here is the quiet pain: for every new project you **set up the same files again by hand**, and the loops run in an ad-hoc way — no scoring, no drift checks, no firm gate. "Ad-hoc" = improvised, with no fixed procedure. "Drift" = files slowly contradicting each other as they get edited separately. "Gate" = a hard checkpoint that can block an action.

> *"Loops don't need to be hand-coded from scratch — there's an open-source CLI ecosystem supporting each phase."*

**Loop CLI** (`@cobusgreyling/loop-*`) is the command-line toolkit that turns the whole loop idea into real commands: from starter scaffolding, readiness scoring, token estimates, and drift checks, to firm enforcement and safe isolation. "Scaffolding" = generating the starter files for you.

> **One-line summary:** Loop CLI automates loop setup and adds scoring, gates, and isolation that hand-run loops lack.

### Why Loop CLI Matters?

This section gives four reasons to use the CLI instead of setting loops up by hand.

> **"A loop without tooling is a ritual. A loop with tooling is an engineering discipline."**

How to read the table: **#** is a row number; **Reason** is the short label; **Explanation** says what the tool actually does. For example, row 3: `loop gate` enforces path rules mechanically — meaning by code, not by hoping the agent reads the safety file.

| # | Reason | Explanation |
|---|--------|-------------|
| 1 | **Standardized scaffolding** | `loop init` builds the right skills, state, and budget files — no need to start from zero each time |
| 2 | **Measurable** | `loop audit` gives a Loop Readiness score from L0 to L3; `loop cost` predicts tokens before you run |
| 3 | **Mechanical enforcement** | `loop gate` applies the allow/deny path rules from config — it works even if the agent skips the safety file |
| 4 | **Safe multi-loop** | `loop worktree` + `loop sandbox` keep each try separate, and `loop swarm` asks for agreement before accepting edits |

Plain glosses: L0–L3 = readiness levels, L0 = "just started", L3 = "fully equipped". "Allow/deny path rules" = lists of folders the loop may or may not touch (allowlist = "list of allowed things", denylist = "list of forbidden things"). "Sandbox" = a sealed test area where changes can't harm the real repo.

> **One-line summary:** Loop CLI turns loop setup, scoring, cost checks, and enforcement from habits into commands.

### Relationship to the Harness

This section shows where Loop CLI sits relative to the `harness/` and `loop/` docs: they teach, it executes.

```
harness/  ← teaches KNOWLEDGE (7 components, 15 modules)
loop/     ← teaches LOOPS (concepts, patterns, safety, operating)
tools/loop-cli/  ← ❯ TOOLING that materializes both
```

The map below shows which command covers which harness component. Read `→` as "implements". For example, "loop gate check → harness/06" means: the gate command is the working code for harness/06's permission checks.

```
┌────────────────────────────────────────────────────────────┐
│  LOOP CLI MAP VS HARNESS COMPONENTS                        │
│                                                            │
│  loop init / doctor / status  → scaffold the whole harness │
│  loop audit                   → assess the Harness Runtime │
│  loop context --check         → harness/01, 03 (memory)    │
│  loop gate check              → harness/06 (permissions)   │
│  loop sandbox / worktree      → harness/10 (automation)    │
│  loop-swarm                   → harness/09 (multi-agent)   │
│  loop-mcp-server              → harness/06 (MCP protocol)  │
└────────────────────────────────────────────────────────────┘
```

Plain glosses: MCP protocol = Model Context Protocol, a standard way to expose tools and files to agents. "Scaffold" = create the starter files.

> **One-line summary:** The harness and loop docs teach the ideas; Loop CLI is the code that runs them.

## Overview of the Commands

This section walks through each command one by one, with a sample script for each.

> **One-line summary:** Nine tools, one job each: set up, score, price, sync, remember, isolate, gate, agree, and serve.

### 1. Front Door — `loop init / doctor / status`

What these do: the three commands you run first in any project — set up, health-check, and report status.

> 📄 **Example code:** [`examples/01-1-front-door-loop-init-doctor-status.sh`](examples/01-1-front-door-loop-init-doctor-status.sh)

`loop init` creates the skills, state, and budget files, then shows the **Loop Ready score** and the first loop command. `loop doctor` combines audit, sync, and file checks into the **top-3 next steps** — like a checkup that ends with a short to-do list. Change `--tool` to `claude`, `codex`, or `opencode` to target the AI tool you use.

> **One-line summary:** `init` sets the project up, `doctor` tells you what to fix first, `status` reports where you stand.

### 2. `loop audit` — Loop Readiness Score

What this does: measures how ready your project is for loops, as a score you can improve.

> 📄 **Example code:** [`examples/02-2-loop-audit-loop-readiness-score.sh`](examples/02-2-loop-audit-loop-readiness-score.sh)

It scores **Loop Readiness** (L0 to L3) — the number climbs from around 10 toward 100 when the setup is correct. It covers constraints, governance, and the **Harness Runtime** (v1.7). "Governance" = the rules about who/what may do what. You stay capped at **L3** until you have `loop-budget.md`, `loop-run-log.md`, and the LOOP.md budget section — the three files that prove the loop is being tracked and capped.

> **One-line summary:** `loop audit` scores your loop setup from ~10 to 100; top score needs the budget and run-log files in place.

### 3. `loop cost` — Token Estimation

> 📄 **Example code:** [`examples/03-3-loop-cost-token-estimation.sh`](examples/03-3-loop-cost-token-estimation.sh)

It predicts token spend **before you set up a schedule** — so next week's bill does not surprise you. "Predicts token spend" = estimates the text units the model will charge for, before running anything.

> **One-line summary:** `loop cost` is the price estimate you check before committing to a schedule.

### 4. `loop sync` — Drift Detection

What this does: catches when `STATE.md` and `LOOP.md` stop agreeing with each other.

> 📄 **Example code:** [`examples/04-4-loop-sync-drift-detection.sh`](examples/04-4-loop-sync-drift-detection.sh)

It spots drift between `STATE.md` and `LOOP.md` — those two files can slowly grow apart over time, e.g. one says "phase 2 running" while the other still says "phase 1".

> **One-line summary:** `loop sync` flags when the state file and the loop file no longer tell the same story.

### 5. `loop context` — Memory + Circuit Breaker

What this does: manages what the loop remembers between rounds, with a safety cut-off.

> 📄 **Example code:** [`examples/05-5-loop-context-memory-circuit-breaker.sh`](examples/05-5-loop-context-memory-circuit-breaker.sh)

A memory manager with a circuit breaker for long runs. "Circuit breaker" = an automatic stop, like the fuse switch in a house: when context grows past a limit, it trips and prevents overload. It keeps context from growing without limit over many rounds.

> **One-line summary:** `loop context` keeps the loop's memory tidy and auto-stops it before context overload.

### 6. `loop worktree` — Isolating Changes

What this does: gives every loop attempt its own git worktree so attempts never step on each other.

> 📄 **Example code:** [`examples/06-6-loop-worktree-isolating-changes.sh`](examples/06-6-loop-worktree-isolating-changes.sh)

It manages separate git worktrees — each try gets its own worktree, tracked in a list, and cleaned up when rejected or escalated. "Escalated" = handed up to a human or a bigger loop for a decision. It includes `lock`/`unlock` so several loops can work side by side — the lock stops two loops grabbing the same worktree.

> **One-line summary:** `loop worktree` = one sandbox copy of the repo per attempt, with locking and cleanup included.

### 7. `loop gate` — Mechanical Enforcement

What this does: checks every change against path rules in code, so safety does not depend on the agent behaving.

> 📄 **Example code:** [`examples/07-7-loop-gate-mechanical-enforcement.sh`](examples/07-7-loop-gate-mechanical-enforcement.sh)

It strictly applies the path denylist and auto-merge allowlist from `gate.yaml`. Denylist = folders nothing may touch (e.g. production configs); allowlist = folders auto-merge may accept; `gate.yaml` = the config file listing them. Exit `2` means escalate, `0` means go ahead — these are the program's exit codes (0 = success/allowed, 2 = blocked), the same style as `loop-context --check`, so you can chain them in scripts.

> **One-line summary:** `loop gate` = a code-enforced bouncer: allowed paths pass (exit 0), forbidden paths are blocked (exit 2).

### 8. `loop sandbox` & `loop swarm` — Isolation + Consensus

What these do: sandbox saves changes safely for review; swarm makes several agents agree before edits are accepted.

> 📄 **Example code:** [`examples/08-8-loop-sandbox-loop-swarm-isolation-consensus.sh`](examples/08-8-loop-sandbox-loop-swarm-isolation-consensus.sh)

- **loop-sandbox**: saves changes as reviewable patch files before applying them. A "patch file" = a small text file describing exactly what changed, line by line.
- **loop-swarm**: team agreement — it needs **byte-identical patches** across runs before accepting them, i.e. several agents must produce exactly the same change before it is trusted.

> **One-line summary:** Sandbox stages changes as reviewable patches; swarm only accepts edits that multiple agents agree on exactly.

### 9. Loop MCP Server

> 📄 **Example code:** [`examples/09-9-loop-mcp-server.sh`](examples/09-9-loop-mcp-server.sh)

Patterns, skills, state, budget, and safety docs become MCP resources — so prompts stay small: the agent reads them on demand instead of pasting them into every prompt. MCP = Model Context Protocol, the standard for exposing such resources. Example config: `examples/mcp/loop-engineering.mcp.json`.

> **One-line summary:** The MCP server lets the agent fetch loop docs on demand, keeping each prompt lean.

## Learning Roadmap (Directory Structure)

> **One-line summary:** This section maps the folder layout and a step-by-step learning path; `(TODO)` = not written yet.

```
loop-cli/
├── README.md            ← YOU ARE HERE — overview + roadmap
├── 01-concepts/         ← (TODO) The loop-* architecture: plugin system, run ledger, state files
├── 02-setup/            ← (TODO) Installation + scaffolding your first project with loop init
├── 03-patterns/         ← (TODO) Combining with loop/02-patterns (triage, sweeper, babysitter)
├── 04-savings/          ← (TODO) Measuring token savings, Loop Ready score gains
└── 05-troubleshooting/  ← (TODO) Drift, gate false-positives, worktree conflicts
```

Plain glosses: "run ledger" = a log of every loop run. "Triage/sweeper/babysitter" = loop patterns named for their job: sorting incoming work, cleaning up backlogs, and watching long runs.

### Recommended Roadmap

A suggested order to get productive; read `↓` as "then do this next". CI = continuous integration, the automated build/test pipeline on every commit.

```
Step 1: Read loop/07-tools/ in the loop/ branch to understand the ecosystem
   ↓
Step 2: loop init . --pattern daily-triage — scaffold your first project
   ↓
Step 3: loop doctor . — see the top-3 next actions
   ↓
Step 4: loop audit . — measure initial Loop Readiness
   ↓
Step 5: Add loop gate check into CI for mechanical enforcement
```

This table maps goals to docs. How to read it: left column = what you want to learn; right column = where to read it.

| If you want to... | Read |
|-------------------|------|
| Understand the loop-* ecosystem | [loop/07-tools](../../loop/07-tools/) |
| Understand loop concepts | [loop/01-concepts](../../loop/01-concepts/) |
| Multi-loop safety | [loop/03-safety](../../loop/03-safety/) + [loop/05-multi-loop](../../loop/05-multi-loop/) |
| Fighting anti-patterns | [loop/06-anti-patterns](../../loop/06-anti-patterns/) |

> **One-line summary:** Start with the ecosystem overview, scaffold with `loop init`, diagnose with `doctor`, score with `audit`, then wire `gate` into CI.

## Real-World Case Studies

Two worked scenarios: what changes when you adopt the tooling, and how to coordinate many loops.

> **One-line summary:** Manual habits vs tooling side by side, plus a recipe for running many loops at once.

### 1. From Manual Loops → Loop Tooling

How to read this table: each row is one stage of running loops; the middle column is the manual (painful) way; the right column is the Loop CLI way. For example, row 1: hand-creating the setup files takes about 30 minutes per project, while `loop init .` does it in under a minute.

| Stage | Without Loop CLI | With Loop CLI |
|-------|------------------|---------------|
| Scaffold | Hand-create STATE.md, LOOP.md, budgets (~30 minutes) | `loop init .` (< 1 minute) |
| Scoring | No way to measure | `loop audit` → score ~10→100 |
| Preventing bad merges | Relies on the agent reading the safety file | `loop gate` — mechanical, nothing missed |
| Many attempts | Noisy commits onto main | `loop worktree` — each attempt isolated |
| Many agents | Trample each other | `loop-swarm` — byte-identical consensus |

> **One-line summary:** Every manual, error-prone loop habit in the left column has a mechanical replacement in the right column.

### 2. Multi-Loop Coordination

What this shows: several loops running at once without interfering — worktrees for separation, locks and swarm for coordination.

> 📄 **Example code:** [`examples/10-2-multi-loop-coordination.sh`](examples/10-2-multi-loop-coordination.sh)

> **One-line summary:** Worktrees isolate, locks prevent collisions, and swarm consensus merges only agreed changes.

## Modern Multi-Agent Loops (2025) — Context

This section places Loop CLI among the wider agent ecosystem terms you will meet in 2025 articles. The loop-* CLI above covers the **operations discipline** of a loop (scaffold, score, gate, isolate). The wider ecosystem has standardized a few concepts worth placing alongside it:

How to read this table: **Concept** = the industry term; **What it is** = a plain definition; **Relation to loop-\*** = how it connects to this toolset. For example, the ReAct pattern is the classic "think, act, look at result, repeat" cycle.

| Concept | What it is | Relation to loop-* |
|---------|-----------|--------------------|
| **ReAct pattern** | Reason → Act → Observe, repeated until done | Each `loop worktree` attempt is one ReAct-style loop with a gate |
| **Agent loop (OpenAI Agents SDK)** | Agent + Runner manage turns, tool calls, and handoffs | `loop init` scaffolds the shell around such an agent loop |
| **AutoGPT-style autonomous loops** | Agent loops that run unattended toward a goal | `loop gate` + budget files are the guardrails that keep them from drifting |
| **A2A protocol (Google, 2025)** | Open protocol for agent-to-agent discovery and handoff | `loop-swarm` consensus is a stricter alternative for accepting another agent's work |

**How to read this**: the SDKs and A2A define the *protocol between agents*; loop-* defines the *operating discipline around them*. They compose — when you wire loop-* to an external agent runtime, `loop gate` remains the mechanical checkpoint before edits reach the main branch.

> **One-line summary:** Other projects define how agents talk; Loop CLI defines the discipline around their work — the two stack.

Refs: [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/) · [A2A protocol](https://github.com/a2aproject/a2a)

## Reference Materials

> **One-line summary:** Where the tool comes from, its ecosystem, and the standards it aligns with.

### Primary Sources

Where the tool and its ecosystem come from, for deeper reading.

> **One-line summary:** One original repo plus a five-part ecosystem stack and three standards (Agents SDK, A2A, ReAct).

- **Original repo**: https://github.com/cobusgreyling/loop-engineering
- **Ecosystem stack**: memory-engineering → loop-engineering → harness-foundry → outerloop → fleet-engineering
- **Companions**: [harness-foundry](https://github.com/cobusgreyling/harness-foundry), [outerloop](https://github.com/cobusgreyling/outerloop), [goal-engineering](https://github.com/cobusgreyling/goal-engineering)
- **OpenAI Agents SDK**: https://openai.github.io/openai-agents-python/ — the agent loop standard
- **A2A protocol**: https://github.com/a2aproject/a2a — agent-to-agent interoperability
- **ReAct paper**: https://arxiv.org/abs/2210.03629

### Links to Other Branches

Related pages in this repo — follow them for the neighboring topic.

> **One-line summary:** Neighboring topics: the loop tool table, the Harness Runtime definition, and the automation component.

- [loop/07-tools](../../loop/07-tools/) — The full table of loop-* tools in the loop/ branch
- [HARNESS_ENGINEERING.md](../../HARNESS_ENGINEERING.md) — What the Harness Runtime is
- [harness/10-automation](../../harness/10-automation/) — The automation component (loop gate, CI)

---

> **"A loop without a gate is a suggestion. A loop with a gate is a system."**

---

*This article is part of the [AI Coding Skills Framework](../..) — the Tools branch — loop-cli*
