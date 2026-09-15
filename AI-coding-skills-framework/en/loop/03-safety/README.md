# 🛡️ 03. Safety & Loop Design Checklist

> Loops amplify judgment — both good and bad. This section covers the **Loop Design Checklist** (the production readiness rubric) and **Safety & Guardrails** (the minimum for production loops that touch code or external systems).

---

## 1. Loop Design Checklist

Use this before turning a loop on in production. Score **honestly** — a loop missing verification is not ready to run unattended.

### §1 Purpose & Scope
- [ ] **One clear goal** — in one sentence: what does this loop accomplish?
- [ ] **Explicit non-goals** — what will this loop *not* do?
- [ ] **Watched scope** — which repos, branches, PRs, tickets?
- [ ] **Phased rollout** — report-only first, then act?
- [ ] **Ambiguous input handled** — when a work item is too vague to verify "done", the loop clarifies or escalates instead of guessing (scaffold an `loop-intake` skill)

### §2 Scheduling
- [ ] **Cadence chosen** — does the interval match the urgency?
- [ ] **Fire immediately** — run the first time now or wait for the interval?
- [ ] **Durable** — does it survive restarts?
- [ ] **Off-hours behavior** — slower cadence or pause overnight?
- [ ] **Self-cleanup** — `scheduler_delete` when the watchlist is empty?

### §3 Skills
- [ ] **Triage skill** exists with a strict output format
- [ ] **Action skills** (minimal-fix...) match project conventions
- [ ] **Skill descriptions** are boring + specific (good for auto-triggering)
- [ ] **Build/test commands** are written down in skills / AGENTS.md

### §4 Maker / Checker Split
- [ ] **Implementer** and **verifier** are two separate entities (agent, model, or instructions)
- [ ] The implementer **cannot** mark its own work "done"
- [ ] The verifier runs **tests** in isolation (worktree) before approving
- [ ] `/goal` or equivalent uses a **fresh model** for the stop condition

### §5 State / Memory
- [ ] **State file** or board schema is documented
- [ ] The loop **reads** old state at the start of each run
- [ ] The loop **writes** outcomes, timestamps, last actions
- [ ] **Prunes** resolved/merged/closed items every run
- [ ] Human overrides are recorded in state

### §6 Human Handoff
- [ ] **Escalation triggers** are explicit (max attempts, risky paths, ambiguity)
- [ ] **Denylist paths** — auth, payments, secrets, infra
- [ ] **Notification rule** — ping a human only when action is needed
- [ ] **Inbox** — where ambiguous items land

### §7 Connectors (MCP)
- [ ] Minimum permissions (read vs write)
- [ ] The loop can **open/update PRs** or tickets if it is acting
- [ ] Clear bot identity on PR comments (e.g. "Loop Engineering — PR Babysitter")

### §8 Cost & Limits
- [ ] **Token budget** estimated
- [ ] **`loop-budget.md`** with daily caps + kill switch
- [ ] **`loop-run-log.md`** for append-only run history
- [ ] **`loop-budget` skill** checks spend at start/end of each run
- [ ] **Max iterations** per item per run
- [ ] **Max auto-PRs** per day (cleanup loops)
- [ ] **Pause/kill criteria** defined

### §9 Observability
- [ ] Log each run: started, items found, actions taken, escalations
- [ ] **Success metrics** chosen
- [ ] The team can **inspect the state file** without reading chat logs

### §10 Safety
- [ ] No auto-merge without an explicit allowlist
- [ ] Secrets/env files are on the denylist
- [ ] Flake handling — don't "fix" flaky tests with retries

### Readiness Levels

| Level | Description | Checklist |
|-------|-------|-----------|
| **L0 — Draft** | Intent written down only | §1 |
| **L1 — Report** | Triage → state, no auto-action | §1–3, §5 |
| **L2 — Assisted** | Small auto-fixes with a verifier | §1–7 |
| **L3 — Unattended** | Runs without you watching | All sections |

### Quick Red Flags

Stop and fix before continuing if:
- The same PR has > 3 auto-fix attempts with no progress
- The verifier is **the same agent session** as the implementer
- There is no state file — the loop loses its memory every run
- Notifications on every run regardless of findings
- Auto-merge on without a path allowlist

---

## 2. Safety & Guardrails

### 2.1 Path Denylist

A loop must **never** auto-edit these paths without human consent:

```
.env
.env.*
**/secrets/**
**/credentials/**
**/*_key*
**/*_secret*
.terraform/**
k8s/production/**
**/migrations/**          # unless a dedicated migration loop exists
auth/**
payments/**
billing/**
```

Encode this in the `minimal-fix` and implementer skills:

> Do not modify files matching the denylist. Escalate to a human with context.

The `loop-gate` tool enforces this denylist **mechanically** from `gate.yaml` (it does not rely on whether the loop has read the file):

```bash
npx @cobusgreyling/loop gate check --action auto-merge --paths <changed files>
# exit 2 = escalate, exit 0 = proceed
```

### 2.2 Auto-Merge Policy

**Default: no auto-merge.**

If you allow auto-merge for trivial loops:

| Allowed | Not allowed |
|-----------|-----------------|
| Typos in comments/docs | Behavior changes |
| Lint auto-fixes in test files only | Dependency version bumps |
| Import ordering | Lockfile changes |
| Config in allowlisted `docs/` paths | Any denylist path |

Document the allowlist in `AGENTS.md` or `loop-auto-merge-allowlist.md`.

### 2.3 MCP Connector Least Privilege

| Connector | Read | Write |
|-----------|------|-------|
| GitHub | issues, PRs, checks | comment, label (no merge by default) |
| Linear | team issues | comment, status (no delete) |
| Slack | channel history | post to `#loop-escalations` only |
| Database | — | no production writes from loops |

Use dedicated bot accounts / tokens with minimal scopes.

### 2.4 Human Gates

Always require a human for:
- Security, authentication, authorization
- Payments, billing, PII handling
- Infrastructure / Terraform / K8s production
- Dependency upgrades (supply chain risk)
- Changes touching > N files (suggested N=10)
- A third failure on the same item
- Token budget extensions: agents **cannot** raise caps in `loop-budget.md` on their own — a human must approve and make the edit. (L3 loops use the `budget-negotiator` skill to *request* more budget.)

### 2.5 Secrets in Prompts & Logs

- Never paste API keys into scheduler prompts
- CI logs can contain secrets — the triage skill should redact before writing state
- State files are often committed — **no credentials in `STATE.md`**

### 2.6 Flake & Test Safety

- Don't disable tests to make CI green
- Don't raise timeouts blindly without a root-cause note
- Quarantine flakes with an explicit ticket + human approval

### 2.7 Incident Response

If a loop merges bad code:
1. **Pause all loops immediately** (`scheduler_list` → delete)
2. Revert the merge
3. Write it up in state + `stories/`
4. Tighten the verifier or shrink the scope before restarting

### 2.8 Pre-Flight Safety Check (before L3)

- [ ] Denylist in the skills
- [ ] Auto-merge off or strict allowlist
- [ ] Connector scopes reviewed
- [ ] Human gates documented in the pattern
- [ ] Kill switch documented

### 2.9 Worktree Isolation & Consensus Sandboxing

- **`loop-sandbox`**: Ephemeral git worktree isolation for single agent runs. Captures changes as reviewable patch files before applying them.
- **`loop-swarm`**: Multi-agent consensus sandboxing across sequential `loop-sandbox` runs. Requires **byte-identical patch consensus** between runs before accepting edits.

---

*Next: [04 — Operating Loops](../04-operating/) → [05 — Multi-Loop Coordination](../05-multi-loop/)*
