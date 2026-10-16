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

You have finished designing a full harness in `harness/` — context, memory, guardrails, evaluation. You have learned that loops are the right way to run it. But each loop still needs **setup by hand**: making `STATE.md`, `LOOP.md`, budget files, safety settings, isolated worktrees...

Here is the quiet pain: for every new project you **set up the same files again by hand**, and the loops run in an ad-hoc way — no scoring, no drift checks, no firm gate. When several loops run at the same time, they get in each other's way.

> *"Loops don't need to be hand-coded from scratch — there's an open-source CLI ecosystem supporting each phase."*

**Loop CLI** (`@cobusgreyling/loop-*`) is the command-line toolkit that turns the whole loop idea into real commands: from starter scaffolding, readiness scoring, token estimates, and drift checks, to firm enforcement and safe isolation.

### Why Loop CLI Matters?

> **"A loop without tooling is a ritual. A loop with tooling is an engineering discipline."**

| # | Reason | Explanation |
|---|--------|-------------|
| 1 | **Standardized scaffolding** | `loop init` builds the right skills, state, and budget files — no need to start from zero each time |
| 2 | **Measurable** | `loop audit` gives a Loop Readiness score from L0 to L3; `loop cost` predicts tokens before you run |
| 3 | **Mechanical enforcement** | `loop gate` applies the allow/deny path rules from config — it works even if the agent skips the safety file |
| 4 | **Safe multi-loop** | `loop worktree` + `loop sandbox` keep each try separate, and `loop swarm` asks for agreement before accepting edits |

### Relationship to the Harness

```
harness/  ← teaches KNOWLEDGE (7 components, 15 modules)
loop/     ← teaches LOOPS (concepts, patterns, safety, operating)
tools/loop-cli/  ← ❯ TOOLING that materializes both

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

## Overview of the Commands

### 1. Front Door — `loop init / doctor / status`

```bash
# Scaffold + diagnose + status (recommended: one binary for all three)
npx @cobusgreyling/loop init . --pattern daily-triage --tool grok
npx @cobusgreyling/loop doctor .
npx @cobusgreyling/loop status .

# Legacy equivalents (forks that don't need to change)
npx @cobusgreyling/loop-init .

# Optional: scaffold an additional versioned harness
npx @cobusgreyling/loop init . --with-foundry
```

`loop init` creates the skills, state, and budget files, then shows the **Loop Ready score** and the first loop command. `loop doctor` combines audit, sync, and file checks into the **top-3 next steps**. Change `--tool` to `claude`, `codex`, or `opencode`.

### 2. `loop audit` — Loop Readiness Score

```bash
npx @cobusgreyling/loop audit . --suggest
```

It scores **Loop Readiness** (L0 to L3) — the number climbs from around 10 toward 100 when the setup is correct. It covers constraints, governance, and the **Harness Runtime** (v1.7). You stay capped at **L3** until you have `loop-budget.md`, `loop-run-log.md`, and the LOOP.md budget section.

### 3. `loop cost` — Token Estimation

```bash
npx @cobusgreyling/loop cost --pattern ci-sweeper --cadence 15m --level L2
```

It predicts token spend **before you set up a schedule** — so next week's bill does not surprise you.

### 4. `loop sync` — Drift Detection

```bash
npx @cobusgreyling/loop sync .
```

It spots drift between `STATE.md` and `LOOP.md` — those two files can slowly grow apart over time.

### 5. `loop context` — Memory + Circuit Breaker

```bash
npx @cobusgreyling/loop context --check --ledger run.json
```

A memory manager with a circuit breaker for long runs. It keeps context from growing without limit over many rounds.

### 6. `loop worktree` — Isolating Changes

```bash
npx @cobusgreyling/loop-worktree create --run-id <id> --pattern <p>
```

It manages separate git worktrees — each try gets its own worktree, tracked in a list, and cleaned up when rejected or escalated. It includes `lock`/`unlock` so several loops can work side by side.

### 7. `loop gate` — Mechanical Enforcement

```bash
npx @cobusgreyling/loop gate check --action auto-merge --paths <f1,f2,...>
```

It strictly applies the path denylist and auto-merge allowlist from `gate.yaml`. Exit `2` means escalate, `0` means go ahead — the same style as `loop-context --check`, so you can chain them.

### 8. `loop sandbox` & `loop swarm` — Isolation + Consensus

```bash
npx @cobusgreyling/loop-sandbox run -- <cmd>   # Ephemeral worktree isolation + patch capture
```

- **loop-sandbox**: saves changes as reviewable patch files before applying them.
- **loop-swarm**: team agreement — it needs **byte-identical patches** across runs before accepting them.

### 9. Loop MCP Server

```bash
npx @cobusgreyling/loop-mcp-server
```

Patterns, skills, state, budget, and safety docs become MCP resources — so prompts stay small. Example config: `examples/mcp/loop-engineering.mcp.json`.

## Learning Roadmap (Directory Structure)

```
loop-cli/
├── README.md            ← YOU ARE HERE — overview + roadmap
├── 01-concepts/         ← (TODO) The loop-* architecture: plugin system, run ledger, state files
├── 02-setup/            ← (TODO) Installation + scaffolding your first project with loop init
├── 03-patterns/         ← (TODO) Combining with loop/02-patterns (triage, sweeper, babysitter)
├── 04-savings/          ← (TODO) Measuring token savings, Loop Ready score gains
└── 05-troubleshooting/  ← (TODO) Drift, gate false-positives, worktree conflicts
```

### Recommended Roadmap

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

| If you want to... | Read |
|-------------------|------|
| Understand the loop-* ecosystem | [loop/07-tools](../../loop/07-tools/) |
| Understand loop concepts | [loop/01-concepts](../../loop/01-concepts/) |
| Multi-loop safety | [loop/03-safety](../../loop/03-safety/) + [loop/05-multi-loop](../../loop/05-multi-loop/) |
| Fighting anti-patterns | [loop/06-anti-patterns](../../loop/06-anti-patterns/) |

## Real-World Case Studies

### 1. From Manual Loops → Loop Tooling

| Stage | Without Loop CLI | With Loop CLI |
|-------|------------------|---------------|
| Scaffold | Hand-create STATE.md, LOOP.md, budgets (~30 minutes) | `loop init .` (< 1 minute) |
| Scoring | No way to measure | `loop audit` → score ~10→100 |
| Preventing bad merges | Relies on the agent reading the safety file | `loop gate` — mechanical, nothing missed |
| Many attempts | Noisy commits onto main | `loop worktree` — each attempt isolated |
| Many agents | Trample each other | `loop-swarm` — byte-identical consensus |

### 2. Multi-Loop Coordination

```bash
# Developer A runs a loop in their own worktree
loop-worktree create --run-id fix-123 --pattern post-merge-cleanup

# Developer B runs a different loop — lock avoids conflicts
loop-worktree lock --scope refs/heads/main

# Both finish → gate check before auto-merge
loop gate check --action auto-merge --paths src/,tests/
```

## Reference Materials

### Primary Sources

- **Original repo**: https://github.com/cobusgreyling/loop-engineering
- **Ecosystem stack**: memory-engineering → loop-engineering → harness-foundry → outerloop → fleet-engineering
- **Companions**: [harness-foundry](https://github.com/cobusgreyling/harness-foundry), [outerloop](https://github.com/cobusgreyling/outerloop), [goal-engineering](https://github.com/cobusgreyling/goal-engineering)

### Links to Other Branches

- [loop/07-tools](../../loop/07-tools/) — The full table of loop-* tools in the loop/ branch
- [HARNESS_ENGINEERING.md](../../HARNESS_ENGINEERING.md) — What the Harness Runtime is
- [harness/10-automation](../../harness/10-automation/) — The automation component (loop gate, CI)

---

> **"A loop without a gate is a suggestion. A loop with a gate is a system."**

---

*This article is part of the [AI Coding Skills Framework](../..) — the Tools branch — loop-cli*
