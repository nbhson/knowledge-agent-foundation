# 🔄 XII. Loop Engineering

> ## 📑 Table of Contents
>
> - [Opening Story](#opening-story)
> - [Why Loop Engineering Matters](#why-loop-engineering-matters)
> - [Overview](#overview)
> - [Learning Path (Directory Structure)](#learning-path-directory-structure)
> - [Real-World Case Studies](#real-case-studies)
> - [Reference Materials](#references)

---

### Opening Story

You hire a new chef. On the first day, he cooks a dish — you taste it and say *"Too salty"*. The next day, he cooks again — you taste it and say *"Less salty, but it needs more sweetness"*. On the third day, the dish is nearly perfect.

Now imagine that you had to stand in the kitchen **every single meal**, whispering instructions to the chef. You would be exhausted — and that is exactly how most people are using AI coding agents: **type a prompt, wait, read, fix the prompt, type it again.**

> *"You shouldn't be prompting coding agents anymore. You should be designing loops that prompt your agents."*
> — **Peter Steinberger**

> *"I don't prompt Claude anymore. I have loops running that prompt Claude and figure out what to do. My job is to write loops."*
> — **Boris Cherny** (Head of Claude Code, Anthropic)

**Loop Engineering** is the craft of designing **control systems** — systems that discover the work to do on their own, assign the work on their own, verify on their own, and maintain their own state — instead of you typing each prompt. The leverage point has shifted: from *writing prompts* to *designing loops*.

### Why Loop Engineering Matters?

> **"Stop prompting. Design the loop. Get a score."**

#### 3 Pieces of Scientific & Practical Evidence

| # | Research / Source | Key Finding |
|---|-------------------|----------------------|
| 1 | **DeepMind (2025)** | Agents with structured feedback loops reduced **recurring errors by 52%** compared to agents without loops |
| 2 | **Anthropic (2025)** | Self-refine loops in Claude Code increased **code quality by 38%** on the SWE-bench benchmark |
| 3 | **loop-engineering (Cobus Greyling, 2026)** | The reference repo dogfoods itself: the `loop-audit` workflow grades a **Loop Ready score** on every PR/push, hitting 5.5k+ GitHub stars in 6 months |

#### Core philosophy:

```
Loop Engineering = Design control systems → Self-discovery + Self-verification → Readiness Score goes up
```

**Important distinctions:**

```
Prompting     = You type each command, the agent does each task
Harness       = The environment one agent runs in (tools, context, permissions)
Loop          = Harness + schedule + state + verification chain (runs repeatedly, self-maintaining)
```

**Analogies**: Loop Engineering is like a **manufacturing plant** — you don't assemble every product yourself; you design the production line (scheduler), the machinery (agents), the inspection equipment (verifiers), and the warehouse (state). And **Cognitive Surrender** is when you stand watching the line run and forget that you are the one who designed it.

**If you skip this**: You spend hours typing the same prompts over and over, agents repeat the same mistakes, tokens are wasted, and you never get a reusable system.

## Overview

**Loop Engineering** is the design of **structured loops** so that AI agents discover work, execute it, verify it, and improve — on a regular cadence, across sessions, with **durable state** that lives outside any single conversation.

Unlike Module VII (Workflow), which organizes a pipeline, Loop Engineering focuses on **self-maintaining loops**: the agent not only finishes a task, but also **decides which task is worth doing, verifies the outcome, and learns from it** for the next run.

```
┌─────────────────────────────────────────────────────────────────────┐
│                        LOOP ENGINEERING                              │
│                                                                     │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │               FIVE BUILDING BLOCKS + MEMORY                   │  │
│  │  Automations · Worktrees · Skills · MCP · Sub-agents + State  │  │
│  └───────────────────────────────────────────────────────────────┘  │
│       │                                                            │
│       ▼                                                            │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │              ANATOMY OF A LOOP                                 │  │
│  │  Schedule → Triage → State → Worktree → Implementer → Verifier│  │
│  │  → MCP → Human Gate → Commit/PR/Escalate                       │  │
│  └───────────────────────────────────────────────────────────────┘  │
│       │                                                            │
│       ▼                                                            │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │              AUTONOMY LEVELS                                   │  │
│  │  L1 Report ──► L2 Assisted ──► L3 Unattended                   │  │
│  └───────────────────────────────────────────────────────────────┘  │
│       │                                                            │
│       ▼                                                            │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │              SAFETY + OPERATING                                │  │
│  │  Denylist · Auto-merge policy · Human gates · Token budget     │  │
│  └───────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

## Learning Path (Directory Structure)

Module XII is split into **dedicated files** so it is easy to learn one part at a time — mirroring the documentation structure of the `loop-engineering` repo:

```
12-loop-engineering/
├── README.md            ← YOU ARE HERE — overview + learning path + case studies
├── 01-concepts/         ← Concepts: 5 building blocks, anatomy, L1-L3, taxonomy
├── 02-patterns/         ← 7 production patterns, one file per pattern
│   ├── README.md        ←   Pattern picker + summary table
│   ├── daily-triage.md
│   ├── pr-babysitter.md
│   ├── ci-sweeper.md
│   ├── dependency-sweeper.md
│   ├── changelog-drafter.md
│   ├── post-merge-cleanup.md
│   └── issue-triage.md
├── 03-safety/           ← Loop Design Checklist + Safety & Guardrails
├── 04-operating/        ← Budget, logging, metrics, when to pause/kill
├── 05-multi-loop/       ← Coordinating when running multiple loops
├── 06-anti-patterns/    ← 10 anti-patterns + failure mode catalog
└── 07-tools/            ← loop-init, loop-audit, loop-cost, ... + ecosystem
```

> Each directory contains a `README.md` — consistent with the `harness/` convention (each module is `NN-name/README.md`).

### Recommended Path

```
Step 1: Read this README.md to understand the context
   ↓
Step 2: 01-concepts/ — learn the 5 building blocks + anatomy + L1-L3
   ↓
Step 3: 02-patterns/ — pick your first pattern (suggestion: Daily Triage L1)
   ↓
Step 4: 03-safety/ — loop design checklist + guardrails
   ↓
Step 5: 04-operating/ — budget + logging before a real schedule
   ↓
Step 6: 05-multi-loop/ + 06-anti-patterns/ — when scaling to many loops
   ↓
Step 7: 07-tools/ — use the CLI scaffold, audit, monitoring
```

| You want to... | Read |
|-------------|-----|
| Understand what a loop is, its building blocks | [01-concepts](01-concepts/) |
| Choose which loop to start with | [02-patterns](02-patterns/) — pattern picker |
| Implement Daily Triage from scratch | [02-patterns/daily-triage.md](02-patterns/daily-triage.md) |
| Check whether your loop is production-ready | [03-safety](03-safety/) — checklist §1–§10 |
| Stop a loop from breaking production | [03-safety](03-safety/) — denylist, auto-merge, human gates |
| Control token cost | [04-operating](04-operating/) — budget + run log |
| Run many loops without them fighting | [05-multi-loop](05-multi-loop/) |
| Avoid expensive mistakes | [06-anti-patterns](06-anti-patterns/) |
| Use the CLI scaffold/audit | [07-tools](07-tools/) |

---

## Real-World Case Studies

### 1. Reference Repo — Eating Its Own Dogfood

The `loop-engineering` repo runs its own patterns on itself:

| Loop | Level | Automation | Notes |
|------|-------|------------|-------|
| Daily Triage | L1 | ✅ `daily-triage.yml` | Weekdays; updates `STATE.md` + `loop-run-log.md` |
| Changelog Drafter | L1 | ✅ `changelog-drafter.yml` | Mondays; opens a release-prep issue |
| Star History | L1 | ✅ `update-star-history.yml` | Daily; auto-PR |
| Validate + Audit | L1 | ✅ `validate-patterns.yml`, `audit.yml` | Readiness score on PRs |
| Dependabot | L1 | ✅ `.github/dependabot.yml` | Weekly npm + Actions |
| PR Babysitter | L2 | ⏸ Manual | Worktrees for fixes; verifier required |
| Dependency Sweeper | L2 | ⏸ Dependabot only | Patch-only |
| CI Sweeper | L2 | ⏸ Partial | Reacts via failing validate/audit |

### 2. Real Stories (Honest Wins and Failures)

The repo has a `stories/` directory recording both wins and failures — the most valuable lesson:

- **CI Sweeper: Infinite Flaky Test** — `stories/ci-sweeper-infinite-flaky-test.md`: the lesson about not auto-fixing flakes.
- **Why We Killed CI Sweeper** — `stories/why-we-killed-ci-sweeper.md`: when to kill a loop.
- **Score Climbs Then Budget Burns** — `stories/score-climbs-then-budget-burns.md`: token budget escaping control.
- **Multi-Loop Collision** — `stories/multi-loop-collision.md`: two loops fighting over the same branch.
- **The Verifier Problem** — `stories/quant-loop-the-verifier-problem.md`: verifier theater in practice.

### 3. Example Implementations Per Tool

- **Grok**: `/loop 1d Run loop-triage. Update STATE.md.` — `examples/grok/daily-triage.md`
- **Claude Code**: `/loop 1d Run $loop-triage...report only` — `examples/claude-code/`
- **Codex**: Automations tab, daily prompt + Triage inbox — `examples/codex/`
- **Opencode**: CLI-first loops: cron/systemd + `opencode run`, skills, worktrees — `examples/opencode/`
- **GitHub Actions**: event-driven CI sweeper — `examples/github-actions/`

---

## Reference Materials

### Articles & Sources

- [Cobus Greyling — Loop Engineering (Substack)](https://cobusgreyling.substack.com/p/loop-engineering) — the concept, primitives, Grok mapping
- [Addy Osmani — Loop Engineering](https://addyosmani.com/blog/loop-engineering/) — "Build the loop like someone who intends to stay the engineer"
- [loop-engineering — GitHub](https://github.com/cobusgreyling/loop-engineering) — reference repo, patterns, starters, tools
- [Goal Engineering](https://github.com/cobusgreyling/goal-engineering) — loops discover, goals complete
- [Memory Engineering](https://github.com/cobusgreyling/memory-engineering) — stop re-explaining your repo
- [Harness Foundry](https://github.com/cobusgreyling/harness-foundry) — versioned runtime stack
- [Outerloop](https://github.com/cobusgreyling/outerloop) — evidence → verdict → answerability
- [Fleet Engineering](https://github.com/cobusgreyling/fleet-engineering) — governing populations of agents

### Frameworks & Tools

- **loop** (front door) — `npx @cobusgreyling/loop init | doctor | status | audit | cost`
- **loop-audit** — Loop Readiness Score CLI
- **loop-cost** — token spend estimator
- **loop-sync** — drift detection between STATE.md and LOOP.md
- **loop-context** — stateful memory + circuit breaker
- **loop-worktree** — isolated worktree management
- **loop-gate** — mechanical denylist + auto-merge enforcement
- **loop-sandbox / loop-swarm** — ephemeral isolation + consensus
- **loop-mcp-server** — patterns/skills/state/budget as MCP resources

For details on each tool: [07-tools](07-tools/).

---

> **"The best system is not the one that never fails — it is the one that corrects mistakes fastest."**

> *"Build the loop. But build it like someone who intends to stay the engineer, not just the person who presses go."* — Addy Osmani

---

*This article is part of the [AI Coding Skills Framework](../..) — Module XII: Loop Engineering*
