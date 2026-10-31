# 📦 Dependency Sweeper Loop

**Goal**: Handle outdated packages / CVE alerts safely — patch low-risk versions, and escalate majors and denylisted packages to a human.
(Glossary: a **CVE alert** = a public security warning with an ID, e.g. "CVE-2023-XXXX", saying a library you use has a known hole. **Patch** = swap in the fixed version. **Escalate** = hand the decision to a human instead of acting. **Denylist** = "blacklist" — a list of packages the loop must never auto-touch.)

## Scheduling

This section answers: when should this loop run?

**Recommended**:
- `/loop 6h–1d` (Grok, Claude Code) — `/loop` = a scheduler command: "run this loop every 6 hours to 1 day"
- GitHub Action cron daily — cron = a time-based scheduler that fires jobs on a schedule
- Dependabot for the discovery part; the sweeper for the patch + verify part (Dependabot = GitHub's bot that *finds* outdated packages; this loop does the fixing)

> **One-line summary:** Run it daily or every few hours; let Dependabot find the alerts and this loop do the fixing.

## Required Skills

Signpost: each loop is built from small named skills. Here is what this one needs and why.

- `dep-triage` — Reads Dependabot alerts / `npm audit` / CVE feeds, classifies severity + risk (`npm audit` = a command that scans your dependency list and reports known vulnerabilities)
- `minimal-fix` — The smallest patch for low-risk CVEs — e.g. bump lodash 4.17.20 → 4.17.21, change nothing else
- Project test skill — Full build + test for verification

> **One-line summary:** One skill reads and classifies alerts, one patches, one verifies with tests.

## State

Signpost: the loop keeps a small markdown file as its memory between runs. This section shows what goes in it.

`dependency-sweeper-state.md`:

```markdown
# Dependency Sweeper State

Last run: 2026-06-09 16:00 UTC

## In-flight
- lodash 4.17.20 → 4.17.21 (CVE-2023-XXXX, low) — worktree open — verifier PASS — PR #1260

## Denylisted (human required)
- openssl 1.1 → 3.0 (major, breaking) — waiting on human decision
```

How to read it: "Last run" is when the loop last executed. "In-flight" = updates currently in progress, e.g. lodash is being bumped from 4.17.20 to 4.17.21 to fix a low-severity CVE; a worktree is open; tests passed; PR #1260 is waiting for a human to merge. "Denylisted" = updates the loop must never auto-do (here: a major openssl jump that can break things).

> **One-line summary:** The state file is the loop's memory: what is in progress, and what is waiting on a human.

## How the Loop Runs (Typical Cycle)

Signpost: this is one full pass of the loop, from reading alerts to cleaning up.

1. Read dependency alerts (Dependabot, `npm audit`, `pip-audit`, ... — `pip-audit` is the Python equivalent of `npm audit`).
2. For each alert:
   - **Low-risk CVE, patch-only within the first 30 days**: worktree → implementer patches → verifier runs `npm ci && npm test`. (worktree = a separate git copy of the repo so the agent never touches your main checkout; implementer = the agent that writes the fix; verifier = a separate agent that checks it; `npm ci` = clean-install dependencies exactly as locked, then `npm test` runs the tests)
   - **Major or breaking**: no auto-patching — escalate to a human (major = a version jump like 2.x → 3.x that often changes behavior).
   - **Denylisted package** (e.g. `openssl`, `auth`, `payments` libs — anything where a wrong change is expensive): escalate.
3. Open a PR with the verified patch; a human merges it (PR = pull request, a proposed code change awaiting review).
4. Prune resolved alerts (prune = delete finished entries so the list stays short).

> **One-line summary:** The loop reads security alerts, safely patches only the low-risk ones (with tests), and hands everything risky to a human.

## Verification Strategy

Signpost: how the loop proves a patch is safe before opening a PR.

- Verifier = **full `npm ci && npm test`** (or the equivalent build + test) in the worktree.
- Don't patch a package without verifying the build — dependency changes often silently break the build.
- Human gate on **majors and denylisted packages** (gate = a mandatory approval stop; nothing proceeds until a person says yes).

> **One-line summary:** No patch ships without a full clean build + test run, and risky upgrades always wait for human approval.

## Human Handoff Points

Signpost: the situations where the loop must stop and ask a person, instead of acting.

- Major version bumps (breaking changes)
- Packages on the denylist (security, auth, payments, infra)
- CVEs without a clear patch
- Alerts that require code changes (not just a version bump)

> **One-line summary:** Anything big, sensitive, unclear, or code-touching goes to a human — the loop only handles simple version bumps.

## Failure Modes & Mitigations

How to read it: "Failure" = what can go wrong; "Mitigation" = the guard that prevents it. For instance, the first row: a breaking upgrade could slip through unnoticed, so a human must approve every major version bump.

| Failure | Mitigation |
|---------|------------|
| Breaking upgrade goes unnoticed | Human gate mandatory for majors |
| Patch breaks the build | Verifier runs the full build + test |
| Running while CI is red | Pause the Dependency Sweeper when CI is red on main (CI = the automated build/test pipeline; "red" = failing) |
| Overwhelmed by many CVEs | Prioritize by severity; batch weekly |

> **One-line summary:** Every failure mode is covered by a mechanical guard: human gates for majors, full tests for patches, pausing on red CI.

## Cost Profile

How to read it: "Scenario" = what kind of run happens; "Tokens/run" = roughly how much model usage one such run costs (tokens = the billing unit of model usage). For instance, "No-op" means the loop woke up, found nothing, and exited — that should cost almost nothing.

| Scenario | Tokens/run | Notes |
|----------|------------|-------|
| No-op | ~5k | No new alerts |
| Triage alerts | ~20k | Read feeds + classify |
| Patch + verify (L2) | ~150k | Worktree + patch + full build/test (L2 = "assisted" level: the loop auto-fixes small things with a verifier) |

**Cadence**: 6h–1d · **Tier**: medium · **Suggested daily cap**: 500k tokens (cadence = how often it runs; tier = how much supervision it needs; daily cap = a hard spending limit per day)

> 📄 **Example code:** [`examples/01-cost-profile.sh`](examples/01-cost-profile.sh)

> **One-line summary:** Most runs are cheap scans; only real patching is expensive, and the daily cap keeps the total bounded.

## Success Metrics

Signpost: how you tell, with numbers, that this loop is worth keeping.

- Time from CVE alert to merged patch
- % of alerts resolved without a human (low-risk only)
- Number of patches that broke the build (target: 0)

> **One-line summary:** Success = faster fixes, more safe automation, and zero broken builds.

---

*Back to [02 — Seven Production Patterns](../02-patterns/)*
