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

This section explains what a "loop" is through a kitchen story — because the fastest way to see the problem is to picture doing every step by hand, forever.

You hire a new chef. On the first day, he cooks a dish — you taste it and say *"Too salty"*. The next day, he cooks again — you taste it and say *"Less salty, but it could use a little more sweetness"*. On the third day, the dish is almost perfect.

Now imagine having to stand in the kitchen **for every single meal**, telling the chef each step. That would wear you out — and yet that is how many people use AI coding agents today: **type a prompt, wait, read the answer, fix the prompt, and repeat.**

> *"You shouldn't be prompting coding agents anymore. You should be designing loops that prompt your agents."*
> — **Peter Steinberger**

> *"I don't prompt Claude anymore. I have loops running that prompt Claude and figure out what to do. My job is to write loops."*
> — **Boris Cherny** (Head of Claude Code, Anthropic)

**Loop Engineering** is the craft of building **control systems** — systems that find the work on their own, assign it on their own, check it on their own, and keep their own state — so you no longer have to type each prompt by hand (*a loop = the same work cycle run on a schedule, with results saved to a file and the work double-checked*). The leverage point has moved: from *writing prompts* to *designing loops*.

> **One-line summary:** Stop typing every prompt by hand — build a scheduled system that finds work, checks itself, and remembers what it did.

### Why Loop Engineering Matters?

This section gives the evidence that loops actually work, plus the vocabulary you need for the rest of the module.

> **"Stop prompting. Design the loop. Get a score."**

#### 3 Pieces of Scientific & Practical Evidence

| # | Research / Source | Key Finding |
|---|-------------------|----------------------|
| 1 | **DeepMind (2025)** | Agents with structured feedback loops reduced **recurring errors by 52%** compared to agents without loops |
| 2 | **Anthropic (2025)** | Self-refine loops in Claude Code increased **code quality by 38%** on the SWE-bench benchmark |
| 3 | **loop-engineering (Cobus Greyling, 2026)** | The reference repo dogfoods itself: the `loop-audit` workflow grades a **Loop Ready score** on every PR/push, hitting 5.5k+ GitHub stars in 6 months |

> **How to read this table:** each row is one piece of evidence. **Research / Source** = who measured it and when. **Key Finding** = the number they found. For example, row 1: agents that check their own work in a loop made 52% fewer repeat mistakes than agents that run once. Row 3: *dogfood* = the repo runs its own patterns on itself, for real, every day.

#### Core philosophy:

```
Loop Engineering = Design control systems → Self-discovery + Self-verification → Readiness Score goes up
```

(In plain words: you build a system that finds its own work and checks its own results — and a readiness score tells you how safe it is to let it run.)

**Important distinctions:**

```
Prompting     = You type each command, the agent does each task
Harness       = The environment one agent runs in (tools, context, permissions)
Loop          = Harness + schedule + state + verification chain (runs repeatedly, self-maintaining)
```

> **How to read it:** *prompting* = you drive, one command at a time. *Harness* = the workshop the agent works in. *Loop* = the workshop **plus** a timer, a to-do file, and a checker — so it keeps running after you walk away.

**Analogies**: Loop Engineering is like a **manufacturing plant** — you don't build every product yourself; you design the production line (scheduler), the machines (agents), the inspection tools (verifiers), and the storage room (state). And **Cognitive Surrender** is when you stand and watch the line run and forget that you are the one who designed it.

**If you skip this**: you spend hours typing the same prompts again and again, agents keep making the same mistakes, tokens go to waste, and you never get a system you can reuse.

> **One-line summary:** The evidence says loops cut errors and raise quality — a loop is harness + schedule + state + verification, not a cleverer prompt.

## Overview

This section defines Loop Engineering properly and shows how its parts fit together, top to bottom.

**Loop Engineering** is about designing **structured loops** so AI agents can find work, do the work, check the work, and improve — on a regular schedule, across sessions, with **durable state** that lives outside any single conversation (*durable state = notes saved to files, not kept in the chat, so nothing is lost between runs*).

Unlike Module VII (Workflow), which organizes a pipeline, Loop Engineering focuses on **self-maintaining loops**: the agent not only finishes a task, but also **figures out which task is worth doing, checks the result, and learns from it** for next time.

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

> **How to read this diagram, top to bottom:** first you assemble the five building blocks (Automations = scheduled triggers; Worktrees = private copies of the repo; Skills = written instructions; MCP = a standard way to call tools; Sub-agents = helper agents — plus State, the shared to-do file). Then one run of a loop flows through the anatomy: on a Schedule, sort the work (Triage), record it (State), work on a private copy (Worktree), write the fix (Implementer), double-check it (Verifier), ask a human for risky steps (Human Gate), then commit or escalate. As trust grows you climb the autonomy levels: L1 = report only, L2 = acts but a human approves, L3 = acts alone. The bottom band is the safety net that makes L3 survivable.

> **One-line summary:** A loop is building blocks + a fixed run cycle + earned autonomy levels, all sitting on a safety layer.

## Learning Path (Directory Structure)

This section maps the seven directories so you always know where you are and what to read next.

Module XII is split into **focused files** so you can learn one part at a time — matching the documentation structure of the `loop-engineering` repo:

```
loop/
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

> **One-line summary:** Seven numbered directories, read in order — concepts first, tools last.

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

> **How to read this table:** the left column is your goal, in your words ("I want to stop my loop breaking things"). The right column is the exact file to open — for instance, "Stop a loop from breaking production" points to the denylist/auto-merge/human-gate sections of `03-safety` (*denylist = a blacklist of paths the loop must never touch*).

> **One-line summary:** Follow steps 1–7 in order and use the table as a shortcut from your current problem to the right file.

---

## Real-World Case Studies

This section shows real repos and real stories: how the reference repo runs its own loops, what failed, and how the same patterns look in each agent tool.

### 1. Reference Repo — Eating Its Own Dogfood

The `loop-engineering` repo runs its own patterns on itself, as a friendly real-life example (*dogfood = a project uses its own product on itself, daily, for real*):

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

> **How to read this table:** **Loop** = which pattern runs. **Level** = how much autonomy it has (L1 = report only; L2 = acts, but a human approves risky steps). **Automation** = ✅ means it runs automatically from the named GitHub Actions workflow file; ⏸ means it is paused or manually triggered. **Notes** = the schedule or the extra safety in play. For example, "Daily Triage, L1, ✅" = a report-only loop that runs on weekdays and writes its findings to two files.

> **One-line summary:** The reference repo runs eight of its own loops — all report-only L1, except three L2 ones, which are paused.

### 2. Real Stories (Honest Wins and Failures)

The repo has a `stories/` folder with both wins and honest failures — the most helpful lesson is:

- **CI Sweeper: Infinite Flaky Test** — `stories/ci-sweeper-infinite-flaky-test.md`: the lesson about not auto-fixing flakes (*flake = a test that fails randomly, not because the code is wrong*).
- **Why We Killed CI Sweeper** — `stories/why-we-killed-ci-sweeper.md`: when to kill a loop.
- **Score Climbs Then Budget Burns** — `stories/score-climbs-then-budget-burns.md`: token budget escaping control.
- **Multi-Loop Collision** — `stories/multi-loop-collision.md`: two loops fighting over the same branch.
- **The Verifier Problem** — `stories/quant-loop-the-verifier-problem.md`: verifier theater in practice (*verifier theater = a check that exists but proves nothing, like a guard who never looks at badges*).

> **One-line summary:** The failures are documented too — infinite flaky fixes, budget burn, loop collisions, and fake verification.

### 3. Example Implementations Per Tool

- **Grok**: `/loop 1d Run loop-triage. Update STATE.md.` — `examples/grok/daily-triage.md`
- **Claude Code**: `/loop 1d Run $loop-triage...report only` — `examples/claude-code/`
- **Codex**: Automations tab, daily prompt + Triage inbox — `examples/codex/`
- **Opencode**: CLI-first loops: cron/systemd + `opencode run`, skills, worktrees — `examples/opencode/`
- **GitHub Actions**: event-driven CI sweeper — `examples/github-actions/`

> **One-line summary:** The reference repo runs its own loops daily (mostly report-only L1), publishes its failures as stories, and ships a copy-paste example per agent tool.

---

## Reference Materials

This section lists the sources and the exact CLI commands, so you can go deeper or start running things.

> **One-line summary:** Original articles, the reference repo, and every CLI command — one line each.

### Articles & Sources

- [Cobus Greyling — Loop Engineering (Substack)](https://cobusgreyling.substack.com/p/loop-engineering) — the concept, primitives, Grok mapping
- [Addy Osmani — Loop Engineering](https://addyosmani.com/blog/loop-engineering/) — "Build the loop like someone who intends to stay the engineer"
- [loop-engineering — GitHub](https://github.com/cobusgreyling/loop-engineering) — reference repo, patterns, starters, tools
- [Goal Engineering](https://github.com/cobusgreyling/goal-engineering) — loops discover, goals complete
- [Memory Engineering](https://github.com/cobusgreyling/memory-engineering) — stop re-explaining your repo
- [Harness Foundry](https://github.com/cobusgreyling/harness-foundry) — versioned runtime stack
- [Outerloop](https://github.com/cobusgreyling/outerloop) — evidence → verdict → answerability
- [Fleet Engineering](https://github.com/cobusgreyling/fleet-engineering) — governing populations of agents

> **One-line summary:** Six links worth reading — two articles, the reference repo, and four companion projects.

### Frameworks & Tools

- **loop** (front door) — `npx @cobusgreyling/loop init | doctor | status | audit | cost` (*npx = download and run a Node.js package without installing it globally*)
- **loop-audit** — Loop Readiness Score CLI (*scores 0–100 how safe it is to let your loop run*)
- **loop-cost** — token spend estimator (*token = the unit of text the model reads and writes; you pay per token*)
- **loop-sync** — drift detection between STATE.md and LOOP.md (*drift = the two files stop matching*)
- **loop-context** — stateful memory + circuit breaker (*circuit breaker = an automatic stop switch for a run gone haywire*)
- **loop-worktree** — isolated worktree management (*worktree = a private copy of the repo in its own folder*)
- **loop-gate** — mechanical denylist + auto-merge enforcement (*denylist = a blacklist of paths that must never be touched*)
- **loop-sandbox / loop-swarm** — ephemeral isolation + consensus (*consensus = two independent runs must agree exactly before an edit is accepted*)
- **loop-mcp-server** — patterns/skills/state/budget as MCP resources (*MCP = a standard protocol that lets an agent fetch documents and call tools*)

For details on each tool: [07-tools](07-tools/).

> **One-line summary:** Nine CLI tools, one line each — the front door is `loop init | doctor | status`.

---

> **"The best system is not the one that never fails — it is the one that corrects mistakes fastest."**

> *"Build the loop. But build it like someone who intends to stay the engineer, not just the person who presses go."* — Addy Osmani

---

*This article is part of the [AI Coding Skills Framework](../..) — Module XII: Loop Engineering*
