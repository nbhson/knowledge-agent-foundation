# 📦 Dependency Sweeper Loop

**Goal**: Xử lý outdated packages / CVE alerts một cách an toàn — patch các phiên bản low-risk, escalate majors và denylisted packages cho human.

## Scheduling

**Khuyên dùng**:
- `/loop 6h–1d` (Grok, Claude Code)
- GitHub Action cron daily
- Dependabot cho phần discovery; sweeper cho phần patch + verify

## Required Skills

- `dep-triage` — Đọc Dependabot alerts / `npm audit` / CVE feeds, classify severity + risk
- `minimal-fix` — Patch nhỏ nhất cho CVE thấp rủi ro
- Project test skill — Full build + test để verify

## State

`dependency-sweeper-state.md`:

```markdown
# Dependency Sweeper State

Last run: 2026-06-09 16:00 UTC

## In-flight
- lodash 4.17.20 → 4.17.21 (CVE-2023-XXXX, low) — worktree open — verifier PASS — PR #1260

## Denylisted (human required)
- openssl 1.1 → 3.0 (major, breaking) — waiting human decision
```

## How the Loop Runs (Typical Cycle)

1. Đọc dependency alerts (Dependabot, `npm audit`, `pip-audit`, ...).
2. Với mỗi alert:
   - **Low-risk CVE, patch-only trong 30 ngày đầu**: worktree → implementer patch → verifier `npm ci && npm test`.
   - **Major hoặc breaking**: không tự patch — escalate cho human.
   - **Denylisted package** (VD: `openssl`, `auth`, `payments` libs): escalate.
3. Mở PR với patch verified; human merge.
4. Prune resolved alerts.

## Verification Strategy

- Verifier = **full `npm ci && npm test`** (hoặc build + test tương đương) trong worktree.
- Không patch package mà không verify build — dependency thay đổi thường phá build ngầm.
- Human gate trên **majors và denylisted packages**.

## Human Handoff Points

- Major version bumps (breaking changes)
- Packages thuộc denylist (security, auth, payments, infra)
- CVEs không có patch rõ ràng
- Alerts đòi hỏi thay đổi code (không chỉ bump version)

## Failure Modes & Mitigations

| Failure | Mitigation |
|---------|------------|
| Breaking upgrade không ai để ý | Human gate bắt buộc cho majors |
| Patch phá build | Verifier chạy full build + test |
| Chạy cùng lúc với CI đỏ | Pause Dependency Sweeper khi CI red trên main |
| Overwhelm với nhiều CVEs | Ưu tiên theo severity; batch theo tuần |

## Cost Profile

| Scenario | Tokens/run | Notes |
|----------|------------|-------|
| No-op | ~5k | Không có alert mới |
| Triage alerts | ~20k | Đọc feeds + classify |
| Patch + verify (L2) | ~150k | Worktree + patch + full build/test |

**Cadence**: 6h–1d · **Tier**: medium · **Suggested daily cap**: 500k tokens

```bash
npx @cobusgreyling/loop cost --pattern dependency-sweeper --cadence 1d --level L2
```

## Success Metrics

- Time từ CVE alert đến patch merged
- % alerts resolved không cần human (low-risk only)
- Số lần patch phá build (mục tiêu: 0)

---

*Trở về [02 — Bảy Production Patterns](../02-patterns/)*
