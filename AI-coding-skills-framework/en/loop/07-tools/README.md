# 🧰 07. Tools & Ecosystem

> **📌 Core Concept**
>
> **Definition:** This is the **CLI toolbox** and ecosystem around loop-engineering — the `npx @cobusgreyling/loop-*` commands covering every stage: creating (`init`), scoring (`audit`), estimating cost (`cost`), detecting state drift (`sync`), isolating changes (`worktree`), and enforcing safety (`gate`).
> **Analogy:** Like an **electrician's toolbox** — you don't need to understand the inside of every screwdriver; you just need to know which one to use for which job: the wire-connector wrench (init), the electrical meter (cost), the cable-tightening pliers (gate). One tool per job, and they work in combination.
> **Why it matters:** These tools are the **mechanization** of loop engineering — they enforce the things human discipline tends to slack on (locking, blocking denylist paths), and give you a measurable "Loop Ready score" instead of a feeling of "probably fine".

> Loops don't need hand-rolled code from scratch — there is an open-source CLI system (`@cobusgreyling/loop-*`) that supports every stage. This section introduces each tool and the surrounding ecosystem.

---

## 1. Front Door — `loop init / doctor / status`

> **Easy way to read it:** `init` = "equips your repo with the loop skeleton" (skills, state, budget); `doctor` = a "health check" that tells you the next 3 things to do. Start every loop project here — don't build by hand.

```bash
# Front door (recommended) — one binary for init + doctor + status
npx @cobusgreyling/loop init . --pattern daily-triage --tool grok
npx @cobusgreyling/loop doctor .

# Legacy equivalent (still supported — forks don't need to change)
npx @cobusgreyling/loop-init .

# Optional: scaffold a versioned harness too (harness-foundry)
npx @cobusgreyling/loop init . --with-foundry
```

`loop init` (or `loop-init`) scaffolds the skills, state, and budget files, then prints the **Loop Ready score** and the first loop command. `loop doctor` combines audit + sync + file checks into the top-3 next actions. Switch `--tool` to `claude`, `codex`, or `opencode`. Use `--with-foundry` when you want the loop to be a composable runtime stack.

---

## 2. loop-audit — Loop Readiness Score

> **Easy way to read it:** `audit` = "grading the operations exam" — gives you a number from 0–100 showing production readiness. Like a credit score: low means don't let the loop run on its own yet; it rises as you scaffold the pieces correctly.

```bash
npx @cobusgreyling/loop audit . --suggest
```

Scores your project's **Loop Readiness** (L0→L3) — a single number that climbs from ~10 to 100 as you scaffold the pieces correctly. Includes constraints + governance + **Harness Runtime** (v1.7). Caps **L3** until `loop-budget.md`, `loop-run-log.md`, and a LOOP.md budget section exist.

---

## 3. loop-cost — Token Estimation

```bash
npx @cobusgreyling/loop cost --pattern ci-sweeper --cadence 15m --level L2
```

Estimates token spend **before scheduling** — avoiding next week's bill shock. See budget rules in detail in [04-operating](../04-operating/).

---

## 4. loop-sync — Drift Detection

```bash
npx @cobusgreyling/loop sync .
```

Detects drift between `STATE.md` and `LOOP.md` — two files that describe the loop's state and configuration but can diverge over time.

---

## 5. loop-context — Memory + Circuit Breaker

```bash
npx @cobusgreyling/loop context --check --ledger run.json
```

Stateful memory manager + circuit breaker for long runs. Keeps context from ballooning unboundedly across iterations.

---

## 6. loop-worktree — Change Isolation

> **Easy way to read it:** `worktree` = a "private practice room" for each fix attempt — the agent edits in its own room, and if it fails that room is discarded, never touching the main code. Comes with `lock/unlock` so loops don't enter the same room at the same time.

```bash
npx @cobusgreyling/loop-worktree create --run-id <id> --pattern <p>
```

Manages isolated git worktrees per fix attempt — one worktree per attempt, tracked in a manifest, cleaned up on reject/escalate. Comes with `lock`/`unlock` for multi-loop coordination (see [05-multi-loop](../05-multi-loop/)).

---

## 7. loop-gate — Mechanical Enforcement

```bash
npx @cobusgreyling/loop gate check --action auto-merge --paths <f1,f2,...>
```

Mechanically enforces the path denylist + auto-merge allowlist from `gate.yaml` — it does not depend on whether the loop has read the safety file. Exit `2` = escalate, `0` = proceed — the same convention `loop-context --check` uses, so control scripts can chain both.

---

## 8. loop-sandbox & loop-swarm — Isolation + Consensus

```bash
npx @cobusgreyling/loop-sandbox run -- <cmd>   # Ephemeral worktree isolation + patch capture
```

- **loop-sandbox**: Ephemeral git worktree isolation for single agent runs. Captures changes as reviewable patch files before applying them.
- **loop-swarm**: Multi-agent consensus sandboxing across sequential `loop-sandbox` runs. Requires **byte-identical patch consensus** between runs before accepting edits.

---

## 9. Other Tools

| Tool | Description | Command |
|------|-------|------|
| **loop-action** | GitHub Composite Action running loops in CI | `uses: cobusgreyling/loop-engineering/tools/loop-action@main` |
| **loop-mcp-server** | Patterns/skills/state/budget/safety docs as MCP resources | `npx @cobusgreyling/loop-mcp-server` |
| **loop-cost** | Token spend estimator | `npx @cobusgreyling/loop-cost` |

**Reference MCP server**: the repo ships `tools/mcp-server/` — patterns, skills, state, budget, and safety docs as runtime-queryable MCP resources (reducing prompt stuffing). Config example: `examples/mcp/loop-engineering.mcp.json`.

---

## 10. Ecosystem Stack

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

### Companion Projects

| Companion | Description |
|-----------|-------|
| [Goal Engineering](https://github.com/cobusgreyling/goal-engineering) | Loops discover, goals complete — `/goal` + stack cookbook |
| [Memory Engineering](https://github.com/cobusgreyling/memory-engineering) | Stop re-explaining your repo — tiers, budget, Memory Ready score |
| [Fleet Engineering](https://github.com/cobusgreyling/fleet-engineering) | Governing populations of agents — registry, inbox, kill switch |
| [harness-foundry](https://github.com/cobusgreyling/harness-foundry) | Companion runtime — versioned stacks, sessions, traces |
| [outerloop](https://github.com/cobusgreyling/outerloop) | Companion governance — evidence → verdict → answerability |

### When to Add What

- When agents **forget between sessions** → add memory-engineering.
- When the team has **many agents/loops** → add fleet-engineering.
- Next after **Loop Ready 80+** → version your loop as a harness (`loop-init` prints the CTA automatically; `loop-audit` recommends Foundry when the score is strong but `.foundry/stack.yaml` is missing).

---

*Back to [README](../README.md) — Module XII overview*
