# 🔬 01. Core Concepts — Loop Engineering

> This section explains **what Loop Engineering is**, **the 5 building blocks + memory** that make up every loop, **the anatomy of a loop**, **the L1–L3 autonomy levels**, and **the taxonomy of nested loops**. Read [README.md](../README.md) first for the overall context.

---

## 1. What Is Loop Engineering?

> **📌 Core Concept**
>
> **Definition:** Loop Engineering is the design of **control systems** for AI coding agents — systems that discover the work to do, assign it, verify it, and maintain state — instead of you typing one prompt at a time.
> **Analogy:** Like a **manufacturing plant** — you don't assemble every product yourself; you design the production line (scheduler), the machinery (agents), the inspection equipment (verifiers), and the warehouse (state). And a **hand-crafted prompter** is the one who makes each item by hand.
> **Why it matters:** Prompting doesn't scale — you are the bottleneck of every task. Loops keep agents working continuously and disciplined, and you only step in at the key decision points (human gates).

### 1.1 From Prompt to Loop

The typical way of using an AI coding agent today is *ad-hoc prompting*: you open the agent, type a command, wait for the result. Every time starts from scratch, with no state, no history, and no systematic verification.

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

**Your role changes**: from *prompt typer* to *loop engineer*. You write skills (knowledge), define the state schema, choose the cadence, and keep decision rights at the **human gates**.

### 1.2 Harness vs Loop

A commonly confused pair of concepts. Harness and Loop are not the same thing:

```
Harness = single session setup
  → the tools, context, permissions, rules that ONE agent has in ONE session

Loop    = harness + schedule + state + verification chain
  → a system that orchestrates MANY harness runs over time
```

Modules VII–XI in this framework build the pieces of a harness. This Module XII (loop) **orchestrates them over time**: schedules, durable state, and verification chains.

### 1.3 A Loop Is a Recursive Goal

A loop is a **recursive goal**: define the purpose, let the agent iterate on its own (with external sub-agents and memory) until it is **done or the loop escalates to a human**.

```
Loop = Define purpose → Iterate → Done / Escalate to human
```

---

## 2. Five Building Blocks + Memory

These are the **primitives** that make up every loop. Actual capability matters more than product names — each primitive has a mapping in different tools (Grok, Claude Code, Codex, Cursor, Opencode, ...).

| Primitive | Job in the Loop |
|-----------|----------------|
| **Automations / Scheduling** | Discovery + triage on a cadence |
| **Worktrees** | Safe parallel execution |
| **Skills** | Durable project knowledge |
| **Plugins & Connectors** | Reaching into real tools (MCP) |
| **Sub-agents** | Separating maker / checker |
| **+ Memory / State** | The durable spine outside every conversation |

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

The heartbeat of the loop. **Without scheduling, you only have one agent running once.**

Common realizations:
- `/loop [interval] <prompt>` (Grok, Claude Code)
- Scheduled tasks / cron in Claude Code
- GitHub Actions + repository dispatch
- `/goal` — run until a verification condition is met
- Custom harness schedulers

Important properties: **interval, fire-immediately, recurring vs one-shot, durable (survives restarts).**

### 2.2 Worktrees

Parallelism without chaos.

When two agents edit the same file at the same time, you get merge hell. Git worktrees (or an equivalent isolated checkout) give each agent a **dedicated working directory** — sharing history but not the working tree.

```
Agent A (worktree 1)  ──►  edits fix/ci-auth-refresh
Agent B (worktree 2)  ──►  edits fix/issue-1241
         └────── sharing the same history ──────┘
```

**Cleanup is critical** — the loop must delete the worktree when the task is done or handed off. The `loop-worktree` tool makes this a mechanism: one worktree per attempt, tracked in a manifest, cleaned up on reject or escalate.

### 2.3 Skills

Durable memory of **intent**.

A skill (usually a `SKILL.md` + scripts/references) encodes:
- Project conventions
- "We don't do it this way because of incident X"
- Build/test/lint commands
- Review criteria
- Domain knowledge

**Without skills**, the loop re-derives everything from scratch on every run → **intent debt**.

```
Skills = "Conventions written once, read on every run"
```

### 2.4 Plugins & Connectors (MCP)

A loop that can only read the filesystem is very limited.

Connectors let the loop:
- Read/update Linear / Jira tickets
- Post to Slack / Discord
- Query databases / internal APIs
- Create branches and PRs on GitHub
- Trigger deploys / runbooks

**MCP (Model Context Protocol)** has become the common substrate — connectors written for one tool often run on others.

### 2.5 Sub-agents — Maker / Checker Split

**The most important structural pattern** for trustworthy loops.

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

> **The state file is often the most important artifact a loop produces.**

---

## 3. Anatomy of a Loop

> **📌 Core Concept**
>
> **Definition:** The Anatomy of a Loop is "the structure of a loop" — the fixed list of steps a loop goes through on every run: from the scheduler waking it up, to triage discovering work, verifying in an isolated worktree, and handing off to a human or committing.
> **Analogy:** Like an **auto assembly line** — the car moves through each station in a fixed order: load parts (context), sort (triage), assemble in a dedicated area (worktree), inspect (verifier), and finally ship or return to the warehouse (commit / escalate). Skip a station and the car leaves the factory uninspected.
> **Why it matters:** The anatomy is the "blueprint" you refer to when designing any loop. We find that the order of the steps determines whether a loop is safe or dangerous — working in an isolated worktree *before* verifying is the "mandatory" order for code-fixing loops.

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

### 3.1 The Lifecycle of One Run

> **📌 Core Concept**
>
> **Definition:** "The lifecycle of one run" is the chain of states a loop run goes through — from being triggered by the scheduler to ending with a log entry. This is the "state machine" that remembers every step, so you (and the loop) know exactly where the run is.
> **Analogy:** Like **the checkpoints on a flight** — a plane can't "skip ahead" from departure to destination; it passes through each stage: takeoff (Scheduled), turbulence with a detour (RunningTriage → IdleNoop when there's nothing to do), safe landing (Applied) or holding for human approval (AwaitingHumanGate).
> **Why it matters:** Reading a run's state = knowing what the loop is "busy with" and **why it stopped** — especially when you debug a loop that complains "it did nothing" (the answer is usually `IdleNoop`).

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

**Key point**: `IdleNoop` must be a normal branch — the loop should **exit cleanly (< 5k tokens)** when the watchlist is empty, not run the full sub-agent chain.

### 3.2 The Loop Orchestration Engine

> **📌 Core Concept**
>
> **Definition:** The Loop Orchestration Engine is the "orchestration brain" as code — a control layer that makes sure every run follows the right steps: read state, triage, run in a worktree with a verifier, and write the log. This is the **reference template**: you don't have to write it exactly, just understand the key decisions it enforces.
> **Analogy:** Like an **elevator controller** — it can't repair the building itself, but it decides: when the doors open (trigger), which floor to go to (triage), who gets to enter/exit (human gate), and logs the journey. Everything flows through a single path so nothing is missed.
> **Why it matters:** This code is the "only place" the rules live: default to **REJECT** when the verifier is unsure, **hard cap of 3 attempts then escalate** (no infinite retries), and an **append-only log** so later you can answer "why did it do that on Tuesday?". Read it with three questions: *where is the state read? who grades? when does it stop?*

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional
import time


@dataclass
class RunOutcome:
    """The outcome of one loop cycle."""
    run_id: str
    pattern: str
    duration_s: float
    items_found: int
    actions_taken: int
    escalations: int
    tokens_estimate: int
    outcome: str  # success / idle / failed / budget_blocked


class LoopOrchestrator:
    """
    The Loop Orchestration Engine — orchestrates the entire loop.

    Anatomy of a Loop:
      Schedule → Triage → State → Worktree → Implementer → Verifier → Gate
    """

    def __init__(self, pattern: str = "daily-triage"):
        self.pattern = pattern
        self.state: Dict[str, Any] = {}
        self.run_log: List[RunOutcome] = []
        self._attempt_count = 0
        self._max_attempts = 3  # Hard cap → escalate, no infinite loops

    def read_state(self, path: str) -> Dict:
        """Read durable state at the start of every run."""
        # In production: read STATE.md / LOOP-STATE.json
        self.state = {"last_run": None, "high_priority": [], "watch_list": []}
        return self.state

    def triage(self) -> List[str]:
        """
        Triage skill — discovers the work to do.
        Output must be STRUCTURED (not narrative):
        - High Priority items (loop is handling / waiting on human)
        - Watch List (being monitored)
        - Recent Noise (ignored this time)
        """
        # In production: call the $loop-triage skill → parse CI, issues, commits, chat
        findings = []
        if not self.state.get("high_priority"):
            # Early exit when there is nothing to do
            self._log(RunOutcome(
                run_id=self._new_run_id(), pattern=self.pattern,
                duration_s=0.1, items_found=0, actions_taken=0,
                escalations=0, tokens_estimate=5_000, outcome="idle",
            ))
        return findings

    def run_worktree(self, task: str, implementer: Callable, verifier: Callable) -> Dict:
        """
        Maker/Checker split in an isolated worktree.

        Rules:
        - The implementer must NOT self-grade "done".
        - The verifier must run tests in the worktree before approving.
        - If the verifier REJECTS → clean up the worktree, record the attempt, escalate after max.
        """
        self._attempt_count += 1

        # In production: `loop-worktree create --run-id <id> --pattern <p>`
        worktree_path = f".worktrees/fix-{self._attempt_count}"

        # The implementer produces the patch inside the worktree
        patch = implementer(task, worktree_path)

        # Independent verifier — default stance is REJECT
        verdict = verifier(patch)

        if verdict.get("pass"):
            return {"verdict": "PASS", "patch": patch, "attempts": self._attempt_count}

        # Verifier REJECTS → no merge, no infinite retries
        if self._attempt_count >= self._max_attempts:
            self.escalate_to_human(patch, verdict.get("reason"))
            return {"verdict": "ESCALATED", "attempts": self._attempt_count}

        return {"verdict": "RETRY", "attempts": self._attempt_count}

    def escalate_to_human(self, patch: Any, reason: str):
        """Escalate with FULL context — don't make the human re-hunt for it."""
        # In production: write to STATE.md under "High Priority (waiting on human)"
        # + a connector ping (Slack, Linear comment) at max attempts
        self.state["high_priority"].append({
            "item": str(patch)[:100], "reason": reason,
            "attempts": self._attempt_count,
        })

    def update_state(self, path: str):
        """Write outcome + timestamp + prune resolved items at the end of each run."""
        # Prune merged/closed items — prevents State Rot
        self.state["last_run"] = time.strftime("%Y-%m-%d %H:%M:%S")
        # In production: write STATE.md

    def _log(self, outcome: RunOutcome):
        """Append-only run log — for debugging "why did it do that on Tuesday?"."""
        self.run_log.append(outcome)

    def _new_run_id(self) -> str:
        return time.strftime("%Y-%m-%dT%H:%M:%SZ")

    def run_cycle(self, path: str = "STATE.md") -> Dict:
        """One complete loop cycle."""
        self.read_state(path)
        findings = self.triage()
        # ... implementer/verifier for each actionable item ...
        self.update_state(path)
        return {"pattern": self.pattern, "state": self.state, "log": self.run_log}
```

</details>

---

## 4. Autonomy Levels L1 → L2 → L3

> **📌 Core Concept**
>
> **Definition:** An autonomy level is a scale for **how far a loop is allowed to act** — from L0 (recording intent only), L1 (report only), L2 (small self-fixes with a verifier), to L3 (running without you watching). It is not a reward tier but a **safety license** graduated by trust.
> **Analogy:** Like a **learner's driving license**: L1 is "ride along as passenger, only report on the road" — the driver just says "there's a pothole ahead" but doesn't steer; L2 is "drive solo in familiar areas with the instructor beside you"; L3 is "a solo road trip across the province" — only after you trust the trainee's judgment over several weeks.
> **Why it matters:** Skipping L1 and jumping straight to L3 is the fastest way to have a loop break production before you understand it. This scale forces you to collect **evidence of good behavior** before granting more action rights.

No one should run a loop **unattended** from day one. The three autonomy levels are a verified progression:

```
L1 REPORT-ONLY ──► L2 ASSISTED ──► L3 UNATTENDED
  Triage → state     Small auto-fixes   Runs without you watching
  No auto-action     With a verifier    Needs denylist + budget + gates
  First week         + worktree         + max attempts
```

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

---

## 5. Loop Taxonomy — Nested Loops

> **📌 Core Concept**
>
> **Definition:** The loop taxonomy is how **loops nest inside each other** across 5 speed tiers — from the thinking loops inside the agent's head (millisecond/second scale) to loops that improve the whole system (day/week scale). Not 5 separate things; they sit **inside each other** like 5 onion layers.
> **Analogy:** Like a **conductor leading an orchestra**: the fastest tempo is each musician's bow stroke (inner loop, milliseconds), the next tier is the whole piece replayed if the tempo breaks (execution loop), and the slowest tier is deciding which pieces to play next season (outer loop). The conductor can't control each fingertip — he controls at the tier that needs its own guardrails.
> **Why it matters:** Guardrails must attach to the right tier: banning infinite retries belongs to the **execution loop** (milliseconds), not the **outer loop** (days). Understanding the taxonomy = knowing which loops are fast and which are slow, which need a verifier, and which only need a human pinned in place.

At the system-design level, each large loop contains smaller loops. Understanding this taxonomy tells you **which loop needs which guardrail**.

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

### 5.2 Execution Loop

Error handling during execution — making sure the agent doesn't give up too early but also **doesn't retry infinitely**. Key patterns: retry with backoff, circuit breaker, timeout. The key guardrail: **hard cap on attempts → escalate**.

**Easy way to read it:** Like **an ATM withdrawal** — the machine says "transaction error", pressing it again is reasonable; but pressing 50 times in a row is crazy. The execution loop allows a few tries with waits (backoff), then cuts the breaker (circuit breaker) and calls for a human (escalate).

### 5.3 Validation Loop

Ensures the agent's output **actually works** before it is accepted. Write → Test → Fix → Re-test. In production loop engineering, this lives in the **verifier sub-agent** running tests in an isolated worktree.

**Easy way to read it:** Like a **chef tasting the dish before serving it** — finish cooking (Write), taste it (Test), if it's off adjust the seasoning (Fix), taste again (Re-test). The verifier is "a taster other than the chef" so they don't get too attached to their own dish.

### 5.4 Feedback Loop

The spine of loop engineering — connecting past results with future actions. Collect metrics → Analyze → Optimize → Apply. Each run should record a **post-run critique**: false positives, repeated items, one change to improve the next run.

**Easy way to read it:** Like a **room thermostat** — measure the temperature (Collect), see it's too hot (Analyze), turn the AC down (Optimize), and tomorrow the machine remembers to pick that level from the start (Apply). Without this loop, the loop keeps running but never gets smarter.

### 5.5 Outer Loop

Runs at low frequency (day/week), focused on improving **the whole system**: prompt evolution, pattern learning, metric tracking. This is where you measure "is the loop getting better?".

**Easy way to read it:** Like a **weekly team debrief at a sports club** — not fixing individual plays (that's the coach's job during the match), but looking at the whole season: which tactics scored, which players need replacing. This is where humans participate the most — and where you catch early "the loop is getting worse".

---

## 6. Concepts & Vocabulary

> **📌 Core Concept**
>
> **Definition:** This is the "shared dictionary" of loop engineering — the abstract concepts that show up everywhere when talking about agents: intent debt, comprehension debt, cognitive surrender, orchestration tax. Knowing the names helps you call the problem correctly when it happens.
> **Analogy:** Like **psychology terms** — before the word "burnout" existed, people just said "I'm too tired to work". With the right word you recognize the condition earlier and treat it properly. These are the "burnouts" of the agent world.
> **Why it matters:** Most loop problems that are "hard to understand" during debugging turn out to be one of these 5 concepts in action. Learn this before reading [06 — Anti-Patterns](../06-anti-patterns/) to know the enemy's name before learning how to fight it.

### 6.1 Intent Debt

Every session, the agent starts from a **blank slate**. Missing intent gets filled with confident guesses — and wrong guesses. **Skills** are how you pay down intent debt: conventions, build steps, "we don't do it this way" — written once, read on every run.

### 6.2 Comprehension Debt

The gap between what exists in the repo and what you actually understand. Loops ship far more code than you wrote — **comprehension debt grows unless you read what the loop produces**.

> *"Velocity up, but no one can explain recent changes; review becomes rubber-stamp."*

### 6.3 Cognitive Surrender

The trap of letting the loop run while you **stop having opinions**. Designing the loop with judgment is the remedy; using the loop to avoid thinking is the accelerant. The same action, opposite outcomes.

### 6.4 Orchestration Tax

The human cost of coordinating parallel agents: review bandwidth, merge conflicts, context switching. **Worktrees** remove the mechanical collisions; you are still the ceiling on how many parallel loops you can absorb.

### 6.5 Code Agent Orchestra / Adversarial Review

A structural pattern: agents with different roles (explore, implement, verify). **The implementer never grades its own work** — mandatory for unattended loops.

---

## 7. The Future of Loop Engineering

### Trends

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

### Research Directions

1. **Goal vs Loop** — loops discover ongoing work; goals complete bounded tasks (`/goal`). The boundary is blurring.
2. **Multi-Agent Loop Coordination** — multiple agents sharing loop insights, improving collectively.
3. **Self-Tuning Parameters** — loops that adjust cadence/budget based on signal quality.
4. **Loop Compression** — reducing the number of iterations needed via predicted outcomes.
5. **Ethical Loop Constraints** — ensuring loops don't create harmful feedback cycles.

---

*Next: [02 — Seven Production Patterns](../02-patterns/) → [03 — Safety & Loop Design Checklist](../03-safety/)*
