# ⚠️ 06. Anti-Patterns & Failure Modes

> Design mistakes to avoid **before** turning loops unattended, plus a **catalog of the real ways loops actually break** with mitigations.

---

## 1. Anti-Patterns (Design Mistakes)

| # | Anti-Pattern | Why it breaks | Do this instead |
|---|--------------|--------------|----------|
| 1 | **Same agent implements AND verifies** | Confirmation bias; weak tests get rubber-stamped | Separate verifier sub-agent/model; default stance REJECT |
| 2 | **No attempt cap** | "Just try until CI is green" → infinite fix loops, token burn | Hard cap (e.g. 3) → escalate with full context in state |
| 3 | **Vague triage output** | The loop can't parse priorities; humans ignore STATE.md | Structured markdown, one-line items, explicit `Suggested loop action` |
| 4 | **L3 before L1 quality** | The loop acts on bad signal; comprehension debt explodes | Week one L1 report-only; measure triage accuracy before enabling L2 |
| 5 | **Shared state without a schema** | Three loops append to one unstructured STATE.md → state rot, conflicts | One state file per pattern, or clearly separated sections with prune rules |
| 6 | **MCP with write-everything scope** | The blast radius of one bad triage decision is too large | L1 read-only connectors; expand scope after earned trust |
| 7 | **No kill switch** | A loop runs 24/7 with no pause criteria → alert fatigue, budget overrun | Document pause/kill in LOOP.md + budget template |
| 8 | **Fixing flakes with code** | Masks infra problems; random diffs | Classify → quarantine/retry policy → escalate env/infra |
| 9 | **Auto-merge without an allowlist** | Security + business-logic bugs through weak verifiers | Explicit path allowlist; human merge for denylist paths |
| 10 | **No run log** | Only STATE.md, no history → can't debug | Append to `loop-run-log.md` every run |

---

## 2. Failure Mode Catalog

Real ways loops break — use this when debugging a misbehaving loop or writing a new pattern.

### Severity Classification

| Severity | Meaning |
|----------|-------|
| **S1 — Annoying** | Wastes time/tokens, no harm |
| **S2 — Harmful** | Wrong code merged, bad tickets, alert fatigue |
| **S3 — Critical** | Security, data loss, production incident |

---

### 2.1 Infinite Fix Loop

- **Symptom**: The same PR/CI job gets auto-fixed 5+ times; never converges.
- **Severity**: S2
- **Causes**: Weak verifier or one sharing the implementer's session; root cause misdiagnosed (symptom fixing); a flaky test treated as a regression.
- **Mitigations**: Hard cap on attempts (e.g. 3) → escalate; separate the verifier model/effort; classify flakes; record the attempt count in state.

### 2.2 State Rot

- **Symptom**: `STATE.md` references merged PRs, closed tickets, stale branches.
- **Severity**: S1 → S2 (the loop acts on ghosts)
- **Causes**: No prune step at the end of the run; state not read at the start of the run; multiple loops writing to the same file without a schema.
- **Mitigations**: Prune closed/merged items every run; `Last run` timestamp + validate IDs; one state file per pattern.

### 2.3 Verifier Theater

- **Symptom**: The verifier "approves" but tests fail in CI or review finds bugs.
- **Severity**: S2
- **Causes**: Vague verifier prompt ("looks good"); the verifier doesn't run tests; same model, same context as the implementer.
- **Mitigations**: The verifier must run test/lint and report output; different instructions ("find reasons to reject"); a stronger model for unattended.

### 2.4 Notification Fatigue

- **Symptom**: Slack/email pings every 5 minutes; the team mutes the bot.
- **Severity**: S1 → S2 (real escalations get missed)
- **Causes**: Notifying on every run, not on every *actionable* finding; the "high priority" threshold set too low.
- **Mitigations**: Notify only when a human decision is needed; digest mode for report-only loops; tighten triage rules.

### 2.5 Token Burn

- **Symptom**: The bill spikes; the loop runs full sub-agent chains on empty/noisy triage.
- **Severity**: S1
- **Causes**: Sub-minute cadence with heavy sub-agents; no early-exit when the watchlist is empty; retrying the whole pipeline on transient API errors.
- **Mitigations**: Cheaper triage-only pass first; `scheduler_delete` when the work is done; daily token budget → pause the loop.

### 2.6 Over-Reach (Wrong Scope)

- **Symptom**: The loop refactors unrelated modules, "fixes" design issues, touches denylist paths.
- **Severity**: S2 → S3
- **Causes**: The minimal-fix skill is too permissive; no path allowlist/denylist; triage queues architectural work under "High Priority".
- **Mitigations**: Denylist enforced in the skills; "smallest possible diff" + verifier checks touched files; triage is signal-only.

### 2.7 Comprehension Debt Spiral

- **Symptom**: Velocity is up but nobody can explain the recent changes; review becomes rubber-stamp.
- **Severity**: S2 (long-term)
- **Causes**: Humans stop reading the loop's output; the auto-merge allowlist grows; no weekly human synthesis.
- **Mitigations**: Mandatory human review for non-trivial PRs; a weekly "loop digest"; cap auto-merge to truly trivial paths.

### 2.8 Cognitive Surrender

- **Symptom**: "The loop handles it" — no opinion on correctness/design.
- **Severity**: S2 (cultural)
- **Causes**: The loop's success metric = volume, not quality; no human gates on medium-risk work.
- **Mitigations**: Explicit human gates in every pattern; success metric = time saved *with* a quality bar; Osmani: "Build it like someone who intends to stay the engineer".

### 2.9 Parallel Collision

- **Symptom**: Two sub-agents edit the same files; merge conflicts; corrupted state.
- **Severity**: S2
- **Causes**: No worktree isolation; two loops acting on the same PR without coordinating.
- **Mitigations**: `isolation: worktree` for every code-editing sub-agent; a lock/queue in state: "PR #1234 — worktree in progress".

### 2.10 Escalation Failure

- **Symptom**: The loop is stuck retrying; the human is never told.
- **Severity**: S2
- **Causes**: Max attempts not implemented; escalation is only written to state nobody reads.
- **Mitigations**: A connector ping on escalation (Slack, Linear comment); a `High Priority (waiting on human)` section in STATE.md; alert when an item in that section is > 24h old.

---

*Next: [07 — Tools & Ecosystem](../07-tools/) → [README](../README.md)*
