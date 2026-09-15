# 📦 Dependency Sweeper Loop

**Goal**: Handle outdated packages / CVE alerts safely — patch low-risk versions, and escalate majors and denylisted packages to a human.

## Scheduling

**Recommended**:
- `/loop 6h–1d` (Grok, Claude Code)
- GitHub Action cron daily
- Dependabot for the discovery part; the sweeper for the patch + verify part

## Required Skills

- `dep-triage` — Reads Dependabot alerts / `npm audit` / CVE feeds, classifies severity + risk
- `minimal-fix` — The smallest patch for low-risk CVEs
- Project test skill — Full build + test for verification

## State

`dependency-sweeper-state.md`:

```markdown
# Dependency Sweeper State

Last run: 2026-06-09 16:00 UTC

## In-flight
- lodash 4.17.20 → 4.17.21 (CVE-2023-XXXX, low) — worktree open — verifier PASS — PR #1260

## Denylisted (human required)
- openssl 1.1 → 3.0 (major, breaking) — waiting on human decision
```

## How the Loop Runs (Typical Cycle)

1. Read dependency alerts (Dependabot, `npm audit`, `pip-audit`, ...).
2. For each alert:
   - **Low-risk CVE, patch-only within the first 30 days**: worktree → implementer patches → verifier runs `npm ci && npm test`.
   - **Major or breaking**: no auto-patching — escalate to a human.
   - **Denylisted package** (e.g. `openssl`, `auth`, `payments` libs): escalate.
3. Open a PR with the verified patch; a human merges it.
4. Prune resolved alerts.

## Verification Strategy

- Verifier = **full `npm ci && npm test`** (or the equivalent build + test) in the worktree.
- Don't patch a package without verifying the build — dependency changes often silently break the build.
- Human gate on **majors and denylisted packages**.

## Human Handoff Points

- Major version bumps (breaking changes)
- Packages on the denylist (security, auth, payments, infra)
- CVEs without a clear patch
- Alerts that require code changes (not just a version bump)

## Failure Modes & Mitigations

| Failure | Mitigation |
|---------|------------|
| Breaking upgrade goes unnoticed | Human gate mandatory for majors |
| Patch breaks the build | Verifier runs the full build + test |
| Running while CI is red | Pause the Dependency Sweeper when CI is red on main |
| Overwhelmed by many CVEs | Prioritize by severity; batch weekly |

## Cost Profile

| Scenario | Tokens/run | Notes |
|----------|------------|-------|
| No-op | ~5k | No new alerts |
| Triage alerts | ~20k | Read feeds + classify |
| Patch + verify (L2) | ~150k | Worktree + patch + full build/test |

**Cadence**: 6h–1d · **Tier**: medium · **Suggested daily cap**: 500k tokens

```bash
npx @cobusgreyling/loop cost --pattern dependency-sweeper --cadence 1d --level L2
```

## Success Metrics

- Time from CVE alert to merged patch
- % of alerts resolved without a human (low-risk only)
- Number of patches that broke the build (target: 0)

---

*Back to [02 — Seven Production Patterns](../02-patterns/)*
