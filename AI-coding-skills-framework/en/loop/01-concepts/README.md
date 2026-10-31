# 🔬 01. Core Concepts — Loop Engineering

> This section covers **what Loop Engineering is**, **the 5 building blocks + memory** behind every loop, **how a loop is put together**, **the L1–L3 levels**, and **how loops fit inside each other**. Please read [README.md](../README.md) first for the big picture.

---

## 1. What Is Loop Engineering?

> **📌 Core Concept**
>
> **Definition:** Loop Engineering is the design of **control systems** for AI coding agents — systems that discover the work to do, assign it, verify it, and maintain state — instead of you typing one prompt at a time. (Control system = the machinery that decides what work happens, when, and who checks it; state = the saved memory between runs.)
> **Analogy:** Like a **manufacturing plant** — you don't assemble every product yourself; you design the production line (scheduler), the machinery (agents), the inspection equipment (verifiers), and the warehouse (state). And a **hand-crafted prompter** is the one who makes each item by hand.
> **Why it matters:** Prompting doesn't scale — you are the bottleneck of every task. Loops keep agents working continuously and disciplined, and you only step in at the key decision points (human gates). (Human gate = a step where a person must approve before things proceed.)

Signpost: this section defines the core idea — because everything later (anatomy, autonomy levels, patterns) builds on the difference between "typing prompts" and "designing a system".

### 1.1 From Prompt to Loop

The usual way to use an AI coding agent today is *one-off prompting*: you open the agent, type a command, wait for the result. Every time starts fresh, with no state, no history, and no systematic checking.

Loop Engineering inverts that:

```
AD-HOC PROMPTING:
  You ──prompt──► Agent ──result──► You (read, evaluate)
  You ──prompt──► Agent ──result──► You (read, evaluate)
  ... endless repetition, no system

LOOP ENGINEERING:
  Scheduler ──fire──► Triage Skill ──read/write──► STATE / Memory
       │                                              │
       ▼                                              ▼
  Isolated Worktree ◄──── Implementer ──patch──► Verifier
       │                                              │
       ▼                                              ▼
  MCP / Git / Tickets ◄──── Human Gate? ──► Commit / PR / Escalate
```

How to read the diagram: top half = the old way, one prompt at a time with no memory; bottom half = the loop way — a scheduler fires, a triage skill sorts work, the implementer writes code in an isolated worktree (an isolated copy of the repo checkout), a verifier checks it, and a human gate decides before anything ships. (MCP = Model Context Protocol, the standard way agents connect to external tools; patch = the set of changes.)

**Your role changes**: from *prompt typer* to *loop designer*. You write skills (knowledge), define the state shape, pick the schedule, and keep decision power at the **human gates**.

> **One-line summary:** Stop typing one prompt at a time; design the system that discovers, does, and checks the work.

### 1.2 Harness vs Loop

A pair of ideas people often mix up. Harness and Loop are not the same thing:

```
Harness = single session setup
  → the tools, context, permissions, rules that ONE agent has in ONE session

Loop    = harness + schedule + state + verification chain
  → a system that orchestrates MANY harness runs over time
```

(Plain words: harness = the workshop one worker uses for one shift; loop = the whole factory running shifts day after day.)

Modules VII–XI in this framework build the pieces of a harness. This Module XII (loop) **brings them together over time**: schedules, durable state, and checking chains.

> **One-line summary:** Harness = one agent's session setup; loop = many harness runs over time, with schedule, state, and verification.

### 1.3 A Loop Is a Recursive Goal

A loop is a **recursive goal**: define the purpose, let the agent iterate on its own (with external sub-agents and memory) until it is **done or the loop escalates to a human**. (Recursive goal = a goal the agent keeps working toward by repeating its own cycle; escalate = hand the problem to a human.)

```
Loop = Define purpose → Iterate → Done / Escalate to human
```

> **One-line summary:** A loop iterates on a stated purpose until done — or it escalates to a human.

> **One-line summary:** Loop Engineering means designing a self-running control system — scheduler, triage, worktree, verifier, human gates — instead of typing one prompt at a time.

---

## 2. Five Building Blocks + Memory

These are the **basic parts** that make up every loop. What each part can do matters more than product names — each part has an equivalent in different tools (Grok, Claude Code, Codex, Cursor, Opencode, ...).

Signpost: this section names the six parts every loop needs, whatever tool you use — knowing them lets you swap tools without redesigning the loop.

How to read the table: each row is one building block and its single job in the loop. For instance, "Worktrees" = giving each agent its own safe copy of the code to edit.

| Primitive | Job in the Loop |
|-----------|----------------|
| **Automations / Scheduling** | Discovery + triage on a cadence |
| **Worktrees** | Safe parallel execution |
| **Skills** | Durable project knowledge |
| **Plugins & Connectors** | Reaching into real tools (MCP) |
| **Sub-agents** | Separating maker / checker |
| **+ Memory / State** | The durable spine outside every conversation |

(Plain words: *cadence* = how often it runs; *durable* = survives restarts and new sessions; *maker / checker* = the one who writes vs the one who reviews; *spine* = the backbone every run reads from and writes to.)

```
┌───────────────────────────────────────────────────────────────┐
│               FIVE BUILDING BLOCKS + MEMORY                     │
│                                                               │
│  ┌─────────────┐ ┌───────────┐ ┌──────────┐ ┌──────────────┐ │
│  │ Automations │ │ Worktrees │ │  Skills  │ │Plugins & Conn│ │
│  │ / Scheduling│ │(isolated) │ │(knowledge)│ │  (MCP)       │ │
│  └──────┬──────┘ └─────┬─────┘ └────┬─────┘ └──────┬───────┘ │
│         └───────────────┼────────────┼──────────────┘        │
│                         ▼            ▼                        │
│              ┌────────────────────────────────────┐          │
│              │   SUB-AGENTS (Maker / Checker)      │          │
│              └────────────────────────────────────┘          │
│                         │                                     │
│                         ▼                                     │
│              ┌────────────────────────────────────┐          │
│              │   MEMORY / STATE (durable)          │          │
│              └────────────────────────────────────┘          │
└───────────────────────────────────────────────────────────────┘
```

### 2.1 Automations / Scheduling

The heartbeat of the loop. **Without scheduling, you just have one agent running once.**

Signpost: this block explains how the loop gets triggered — the difference between a one-shot agent and a recurring system.

Common realizations:
- `/loop [interval] <prompt>` (Grok, Claude Code)
- Scheduled tasks / cron in Claude Code (cron = the classic scheduler that runs commands at fixed times)
- GitHub Actions + repository dispatch (repository dispatch = an event you can send to a GitHub repo to trigger a workflow)
- `/goal` — run until a verification condition is met
- Custom harness schedulers

Important properties: **interval, fire-immediately, recurring vs one-shot, durable (survives restarts).**

> **One-line summary:** Scheduling is the heartbeat — check interval, fire-immediately, recurrence, and durability.

### 2.2 Worktrees

Parallelism without chaos.

When two agents edit the same file at the same time, you get merge hell. Git worktrees (or an equivalent isolated checkout) give each agent a **dedicated working directory** — sharing history but not the working tree. (Merge hell = a tangle of conflicting changes that takes hours to untangle; working tree = the actual editable copy of the files.)

```
Agent A (worktree 1)  ──►  edits fix/ci-auth-refresh
Agent B (worktree 2)  ──►  edits fix/issue-1241
         └────── sharing the same history ──────┘
```

**Cleanup is critical** — the loop must delete the worktree when the task is done or handed off. The `loop-worktree` tool makes this a mechanism: one worktree per attempt, tracked in a manifest, cleaned up on reject or escalate. (Manifest = a small index file listing which worktrees exist and what they're for.)

> **One-line summary:** One isolated worktree per attempt, deleted when done — parallelism without merge hell.

> **One-line summary:** Every loop is built from six blocks — scheduler, worktrees, skills, connectors, sub-agents, and durable state — and each has a tool-independent job.

### 2.3 Skills

Durable memory of **intent**.

Signpost: this block explains how the loop remembers your project's rules — because the model itself forgets everything between sessions.

A skill (a `SKILL.md` + `scripts/`/`references/`/`assets/` per the Agent Skills spec — see `harness/05-prompt-builder/agent-skills-spec.md`) encodes:
- Project conventions
- "We don't do it this way because of incident X"
- Build/test/lint commands (lint = a tool that checks code style)
- Review criteria
- Domain knowledge

**Without skills**, the loop re-derives everything from scratch on every run → **intent debt**. (Intent debt = wrong confident guesses caused by missing project knowledge.)

```
Skills = "Conventions written once, read on every run"
```

> **One-line summary:** Skills are conventions written once and read every run — the cure for intent debt.

### 2.4 Plugins & Connectors (MCP)

A loop that can only read the filesystem is very limited.

Connectors let the loop:
- Read/update Linear / Jira tickets
- Post to Slack / Discord
- Query databases / internal APIs
- Create branches and PRs on GitHub
- Trigger deploys / runbooks (runbook = a documented emergency/procedure script)

**MCP (Model Context Protocol)** has become the common substrate — connectors written for one tool often run on others. (Substrate = the shared foundation layer.)

> **One-line summary:** Connectors via MCP let the loop touch tickets, chat, databases, and GitHub — not just files.

### 2.5 Sub-agents — Maker / Checker Split

**The most important structural pattern** for trustworthy loops.

Signpost: this block explains why two different agents must be involved — because the author of a mistake is the worst person (or agent) to catch it.

The agent that writes code is a bad grader of its own work. A second agent (sometimes a stronger model, always with different instructions) performs the **verification**.

```
Implementer (Maker) ──patch──► Verifier (Checker) ──approve/reject──►
   Never grades its            "Find reasons to REJECT"              Commit / PR
   own work
```

Common splits:
- Explorer → Implementer → Verifier
- Implementer → Security reviewer
- Implementer → Test writer + runner

In **unattended** loops, the verifier is what lets you walk away with some confidence.

> **One-line summary:** The implementer never grades its own work; a separate verifier is what makes unattended runs safe.

### 2.6 Memory / State

The model has no long-term memory across separate turns or sessions.

A loop **must** read from and write to something durable:
- `STATE.md` or `LOOP-STATE.json` in the repo
- A dedicated section of a Linear board / GitHub Project
- A row in a small database

Good state answers:
- What are we working on?
- What did we try last time, and what was the result?
- What is waiting on a human?

> **The state file is often the most important artifact a loop produces.** (Artifact = the output/document a process leaves behind.)

> **One-line summary:** Durable state answers what we're doing, what we tried, and what's waiting on a human.

> **One-line summary:** Skills remember your intent, connectors reach the outside world, a second agent grades the first, and a durable state file is the loop's memory spine.

---

## 3. Anatomy of a Loop

> **📌 Core Concept**
>
> **Definition:** The Anatomy of a Loop is "the structure of a loop" — the fixed list of steps a loop goes through on every run: from the scheduler waking it up, to triage discovering work, verifying in an isolated worktree, and handing off to a human or committing. (Triage = sorting incoming items by priority; worktree = an isolated copy of the repo checkout.)
> **Analogy:** Like an **auto assembly line** — the car moves through each station in a fixed order: load parts (context), sort (triage), assemble in a dedicated area (worktree), inspect (verifier), and finally ship or return to the warehouse (commit / escalate). Skip a station and the car leaves the factory uninspected.
> **Why it matters:** The anatomy is the "blueprint" you refer to when designing any loop. We find that the order of the steps determines whether a loop is safe or dangerous — working in an isolated worktree *before* verifying is the "mandatory" order for code-fixing loops.

Signpost: this section gives the blueprint to copy for any loop you design — the order of stations is the safety property.

A complete loop cycle looks like this:

```
┌──────────────────────────────────────────────────────────────────────┐
│ Schedule / Automation ──► Triage Skill                               │
│     │                          │                                     │
│     │                          ▼                                     │
│     │                   Read + Write STATE / Memory                  │
│     │                          │                                     │
│     │                          ▼                                     │
│     │                  Isolated Worktree                             │
│     │                          │                                     │
│     │                          ▼                                     │
│     │                  Implementer Sub-agent                         │
│     │                          │                                     │
│     │                          ▼                                     │
│     │                  Verifier Sub-agent (tests + gates)            │
│     │                          │                                     │
│     │                          ▼                                     │
│     │                  MCP / Git / Tickets                           │
│     │                          │                                     │
│     │                          ▼                                     │
│     │                  Human Gate?                                   │
│     └── safe/allowlisted ──► Commit / PR / Action                    │
│     └── risky/ambiguous ────► Escalate to human (full context)       │
└──────────────────────────────────────────────────────────────────────┘
```

(Plain words: *allowlisted* = on the pre-approved list, e.g. safe file paths; *escalate with full context* = hand to a human together with everything needed to decide.)

### 3.1 The Lifecycle of One Run

> **📌 Core Concept**
>
> **Definition:** "The lifecycle of one run" is the chain of states a loop run goes through — from being triggered by the scheduler to ending with a log entry. This is the "state machine" that remembers every step, so you (and the loop) know exactly where the run is. (State machine = the fixed set of named stages and allowed transitions.)
> **Analogy:** Like **the checkpoints on a flight** — a plane can't "skip ahead" from departure to destination; it passes through each stage: takeoff (Scheduled), turbulence with a detour (RunningTriage → IdleNoop when there's nothing to do), safe landing (Applied) or holding for human approval (AwaitingHumanGate).
> **Why it matters:** Reading a run's state = knowing what the loop is "busy with" and **why it stopped** — especially when you debug a loop that complains "it did nothing" (the answer is usually `IdleNoop`). (`IdleNoop` = the clean "found nothing to do" exit.)

Each scheduled run passes through the states below, ending with a durable log entry:

```
Scheduled → LoadingContext → RunningTriage → WorkingInWorktree → Verifying
     │              │              │
     │              ├──► BlockedBudget (budget exceeded)
     │              └──► RunningTriage
     │                              └──► IdleNoop (nothing to do)
     │
     Verifying → AwaitingHumanGate → Applied / Rejected
           │            └──► Failed
           │
           └──► (every terminal state) → Logged → [*]
```

How to read it: read left to right as the happy path; anything branching downward is a side exit (out of budget, nothing to do, failed). "Terminal state" = a stage where the run ends, after which it is always logged.

**Key point**: `IdleNoop` must be a normal branch — the loop should **exit cleanly (< 5k tokens)** when the watchlist is empty, not run the full sub-agent chain.

> **One-line summary:** Every run walks a fixed state chain from Scheduled to a logged outcome, and `IdleNoop` is a healthy exit — not a failure.

### 3.2 The Loop Orchestration Engine

> **📌 Core Concept**
>
> **Definition:** The Loop Orchestration Engine is the "orchestration brain" as code — a control layer that makes sure every run follows the right steps: read state, triage, run in a worktree with a verifier, and write the log. This is the **reference template**: you don't have to write it exactly, just understand the key decisions it enforces. (Orchestration = coordinating the parts; reference template = a model implementation to copy or adapt.)
> **Analogy:** Like an **elevator controller** — it can't repair the building itself, but it decides: when the doors open (trigger), which floor to go to (triage), who gets to enter/exit (human gate), and logs the journey. Everything flows through a single path so nothing is missed.
> **Why it matters:** This code is the "only place" the rules live: default to **REJECT** when the verifier is unsure, **hard cap of 3 attempts then escalate** (no infinite retries), and an **append-only log** so later you can answer "why did it do that on Tuesday?". Read it with three questions: *where is the state read? who grades? when does it stop?* (Append-only log = entries can only be added, never edited or deleted — so history can't be rewritten.)

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/01-3-2-the-loop-orchestration-engine.py`](examples/01-3-2-the-loop-orchestration-engine.py)

</details>

> **One-line summary:** The engine enforces REJECT-by-default, a 3-attempt cap, and an append-only log.

> **One-line summary:** The orchestration engine is the single place the safety rules live — verifier defaults to REJECT, 3 attempts max then escalate, and an append-only log you can audit later.

---

## 4. Autonomy Levels L1 → L2 → L3

> **📌 Core Concept**
>
> **Definition:** An autonomy level is a scale for **how far a loop is allowed to act** — from L0 (recording intent only), L1 (report only), L2 (small self-fixes with a verifier), to L3 (running without you watching). It is not a reward tier but a **safety license** graduated by trust. (Graduated by trust = each level unlocks only with evidence from the one below.)
> **Analogy:** Like a **learner's driving license**: L1 is "ride along as passenger, only report on the road" — the driver just says "there's a pothole ahead" but doesn't steer; L2 is "drive solo in familiar areas with the instructor beside you"; L3 is "a solo road trip across the province" — only after you trust the trainee's judgment over several weeks.
> **Why it matters:** Skipping L1 and jumping straight to L3 is the fastest way to have a loop break production before you understand it. This scale forces you to collect **evidence of good behavior** before granting more action rights.

Signpost: this section defines how much a loop may do on its own — and what evidence unlocks the next level.

No one should run a loop **unattended** from day one. The three autonomy levels are a verified progression:

```
L1 REPORT-ONLY ──► L2 ASSISTED ──► L3 UNATTENDED
  Triage → state     Small auto-fixes   Runs without you watching
  No auto-action     With a verifier    Needs denylist + budget + gates
  First week         + worktree         + max attempts
```

(Plain words: *denylist* = the list of forbidden actions or paths; *budget* = a hard cap on token spend; *gates* = mandatory human approval points.)

How to read the table: each row is a level, what the loop may do at that level, and which sections of this doc you must have in place first. For instance, L2 requires everything from §1 through §7 — including the verifier and state handling.

| Level | Description | Checklist |
|-------|-------|-----------|
| **L0 — Draft** | Intent written down only | §1 (purpose & scope) |
| **L1 — Report** | Triage → state, no auto-action | §1–3, §5 |
| **L2 — Assisted** | Small auto-fixes with a verifier | §1–7 |
| **L3 — Unattended** | Runs without you watching | All sections |

**Golden rule**: never skip to L3 for a new pattern on a production repo.

```
L1 ──► L2: audit score up + human OK
L2 ──► L3: denylist + budget + gates proven
L3 ──► L2: incident or cost spike
L2 ──► L1: kill switch
```

> **One-line summary:** Autonomy is a safety license earned with evidence — report first (L1), assisted fixes next (L2), unattended (L3) only when denylist, budget, and gates are proven, with downgrade paths ready.

---

## 5. Loop Taxonomy — Nested Loops

> **📌 Core Concept**
>
> **Definition:** The loop taxonomy is how **loops nest inside each other** across 5 speed tiers — from the thinking loops inside the agent's head (millisecond/second scale) to loops that improve the whole system (day/week scale). Not 5 separate things; they sit **inside each other** like 5 onion layers. (Taxonomy = a naming/classification scheme.)
> **Analogy:** Like a **conductor leading an orchestra**: the fastest tempo is each musician's bow stroke (inner loop, milliseconds), the next tier is the whole piece replayed if the tempo breaks (execution loop), and the slowest tier is deciding which pieces to play next season (outer loop). The conductor can't control each fingertip — he controls at the tier that needs its own guardrails.
> **Why it matters:** Guardrails must attach to the right tier: banning infinite retries belongs to the **execution loop** (milliseconds), not the **outer loop** (days). Knowing the taxonomy = knowing which loops are fast and which are slow, which need a verifier, and which only need a human pinned in place.

Signpost: this section sorts loops by speed so you attach each safety rule to the right layer — a rule on the wrong layer protects nothing.

How to read the diagram: each box contains the next; the innermost runs per thought (milliseconds), the outermost per week. Guardrails attach at the layer matching the risk.

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│  OUTER LOOP (cross-task, day/week)                                 │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │  LEARNING LOOP (per-task, hour)                                │  │
│  │  ┌─────────────────────────────────────────────────────────┐  │  │
│  │  │  EXECUTION LOOP (per-action, second)                     │  │  │
│  │  │  ┌───────────────────────────────────────────────────┐  │  │  │
│  │  │  │  INNER LOOP (per-step, ms)                         │  │  │  │
│  │  │  │  Think ──► Act ──► Observe ──► Reflect            │  │  │  │
│  │  │  │     ▲                              │              │  │  │  │
│  │  │  │     └──────────────────────────────┘              │  │  │  │
│  │  │  │                                                   │  │  │  │
│  │  │  │  Execute ──► Retry ──► Verify ──► Escalate        │  │  │  │
│  │  │  └───────────────────────────────────────────────────┘  │  │  │
│  │  └─────────────────────────────────────────────────────────┘  │  │
│  │                                                               │  │
│  │  Task 1 ──► Task 2 ──► Task 3 ──► ... ──► Optimize           │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 5.1 Inner Loop

The fastest loop — it happens inside the agent's thinking. The agent "talks to itself" before acting: Think → Act → Observe → Reflect.

**Easy way to read it:** Like a **chess player calculating before making a move** — evaluate the board (Think), make the move (Act), look at the result (Observe), draw a lesson (Reflect). This loop is too fast for you to intervene: no scripting, no guardrails needed — it is the agent's "instinct".

> **One-line summary:** The inner loop is the agent's millisecond thinking cycle — too fast to guardrail, none needed.

### 5.2 Execution Loop

Error handling during execution — making sure the agent doesn't give up too early but also **doesn't retry infinitely**. Key patterns: retry with backoff, circuit breaker, timeout. The key guardrail: **hard cap on attempts → escalate**. (Backoff = waiting longer between each retry; circuit breaker = cut off after repeated failures, like a fuse.)

**Easy way to read it:** Like **an ATM withdrawal** — the machine says "transaction error", pressing it again is reasonable; but pressing 50 times in a row is crazy. The execution loop allows a few tries with waits (backoff), then cuts the breaker (circuit breaker) and calls for a human (escalate).

> **One-line summary:** Five loop speeds nest like onion layers — attach retry caps to the execution loop, improvement to the outer loop, and leave the millisecond inner loop unguarded.

### 5.3 Validation Loop

Ensures the agent's output **actually works** before it is accepted. Write → Test → Fix → Re-test. In production loop engineering, this lives in the **verifier sub-agent** running tests in an isolated worktree.

**Easy way to read it:** Like a **chef tasting the dish before serving it** — finish cooking (Write), taste it (Test), if it's off adjust the seasoning (Fix), taste again (Re-test). The verifier is "a taster other than the chef" so they don't get too attached to their own dish.

> **One-line summary:** Validation is a taster-other-than-the-cook: the verifier tests before anything is accepted.

### 5.4 Feedback Loop

The spine of loop engineering — connecting past results with future actions. Collect metrics → Analyze → Optimize → Apply. Each run should record a **post-run critique**: false positives, repeated items, one change to improve the next run. (Post-run critique = a short self-review written after each run.)

**Easy way to read it:** Like a **room thermostat** — measure the temperature (Collect), see it's too hot (Analyze), turn the AC down (Optimize), and tomorrow the machine remembers to pick that level from the start (Apply). Without this loop, the loop keeps running but never gets smarter.

> **One-line summary:** A post-run critique every run is what makes the loop smarter instead of just faster.

### 5.5 Outer Loop

Runs at low frequency (day/week), focused on improving **the whole system**: prompt evolution, pattern learning, metric tracking. This is where you measure "is the loop getting better?".

**Easy way to read it:** Like a **weekly team debrief at a sports club** — not fixing individual plays (that's the coach's job during the match), but looking at the whole season: which tactics scored, which players need replacing. This is where humans participate the most — and where you catch early "the loop is getting worse".

> **One-line summary:** The outer loop is the weekly debrief — where humans judge whether the whole system is improving.

> **One-line summary:** Validation (test before accept) and feedback (critique every run) make each run correct and the next run smarter; the slow outer loop is where humans judge the whole system.

---

## 6. Concepts & Vocabulary

> **📌 Core Concept**
>
> **Definition:** This is the "shared dictionary" of loop engineering — the abstract concepts that show up everywhere when talking about agents: intent debt, comprehension debt, cognitive surrender, orchestration tax. Knowing the names helps you call the problem correctly when it happens.
> **Analogy:** Like **psychology terms** — before the word "burnout" existed, people just said "I'm too tired to work". With the right word you recognize the condition earlier and treat it properly. These are the "burnouts" of the agent world.
> **Why it matters:** Most loop problems that are "hard to understand" during debugging turn out to be one of these 5 concepts in action. Learn this before reading [06 — Anti-Patterns](../06-anti-patterns/) to know the enemy's name before learning how to fight it.

Signpost: this section is the vocabulary — five named problems that account for most "my loop feels wrong" moments.

### 6.1 Intent Debt

Every session, the agent starts from a **blank slate**. Missing intent gets filled with confident guesses — and wrong guesses. **Skills** are how you pay down intent debt: conventions, build steps, "we don't do it this way" — written once, read on every run. (Intent debt = the pile of project knowledge the agent lacks and keeps guessing wrong.)

> **One-line summary:** Pay intent debt once — write conventions and past failures into skills.

### 6.2 Comprehension Debt

The gap between what exists in the repo and what you actually understand. Loops ship far more code than you wrote — **comprehension debt grows unless you read what the loop produces**.

> *"Velocity up, but no one can explain recent changes; review becomes rubber-stamp."*

> **One-line summary:** Unread loop output becomes comprehension debt; reading the state file is the payment.

### 6.3 Cognitive Surrender

The trap of letting the loop run while you **stop having opinions**. Designing the loop with judgment is the remedy; using the loop to avoid thinking is the accelerant. The same action, opposite outcomes.

> **One-line summary:** Use the loop to extend your judgment, never to avoid having any.

### 6.4 Orchestration Tax

The human cost of coordinating parallel agents: review bandwidth, merge conflicts, context switching. **Worktrees** remove the mechanical collisions; you are still the ceiling on how many parallel loops you can absorb.

> **One-line summary:** Worktrees fix collisions; only you can absorb the review load — so you are the limit.

### 6.5 Code Agent Orchestra / Adversarial Review

A structural pattern: agents with different roles (explore, implement, verify). **The implementer never grades its own work** — mandatory for unattended loops. (Adversarial review = the checker is instructed to argue against the work, i.e. "find reasons to REJECT".)

> **One-line summary:** Split agents into explore / implement / verify roles — and never let the implementer grade itself.

> **One-line summary:** Five named failure patterns — intent debt, comprehension debt, cognitive surrender, orchestration tax, and self-grading — explain most "my loop feels wrong" moments.

---

## 7. The Future of Loop Engineering

Signpost: this closing section sketches where the field is heading, so today's designs don't fight tomorrow's direction.

### Trends

How to read it: a timeline from top (past) to bottom (future); each block names the era and what it added.

```
┌─────────────────────────────────────────────────────────────┐
│                 LOOP ENGINEERING EVOLUTION                    │
│                                                              │
│  2024-2025: Manual prompting → first loops                  │
│       → Ad-hoc agents, no state, no verifiers                │
│                                                              │
│  2025-2026: Production loop frameworks                      │
│       → Patterns, starters, readiness scores                │
│       → Denylist, budget, human gates (loop-engineering)    │
│       → Cross-tool primitives (Grok, Claude, Codex, ...)    │
│                                                              │
│  2027: Self-verifying & self-tuning loops                   │
│       → Loops that adjust cadence by signal quality         │
│       → Cross-task learning at scale                        │
│       → Multi-agent loop coordination (fleet)               │
│                                                              │
│  2028: Autonomous improvement with human governance         │
│       → Loops that design new loops                         │
│       → Human-in-the-loop for strategic decisions only      │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

(Plain words: *cadence* = how often the loop runs; *readiness scores* = audit numbers saying how safe a loop is to level up; *fleet* = many agents running in coordination.)

> **One-line summary:** The timeline runs from ad-hoc prompting to self-tuning loops with human governance by 2028.

### Research Directions

Signpost: these are the open questions researchers are working on — useful to know so you don't hand-roll what will soon be standard.

1. **Goal vs Loop** — loops discover ongoing work; goals complete bounded tasks (`/goal`). The boundary is blurring.
2. **Multi-Agent Loop Coordination** — multiple agents sharing loop insights, improving collectively.
3. **Self-Tuning Parameters** — loops that adjust cadence/budget based on signal quality.
4. **Loop Compression** — reducing the number of iterations needed via predicted outcomes.
5. **Ethical Loop Constraints** — ensuring loops don't create harmful feedback cycles.

> **One-line summary:** Five open research threads — goal/loop blur, multi-agent coordination, self-tuning, compression, and ethics.

> **One-line summary:** The field is moving from hand-built loops toward self-tuning, coordinated loops — but the core you learned here (state, verifier, gates) stays the foundation.

---

*Next: [02 — Seven Production Patterns](../02-patterns/) → [03 — Safety & Loop Design Checklist](../03-safety/)*
