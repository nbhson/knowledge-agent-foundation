# 👶 PR Babysitter Loop

**Goal**: Theo dõi PRs đang chờ review/CI/rebase, nhắc nhở, và gợi ý fix nhỏ.

## Scheduling

**Khuyên dùng**:
- `/loop 10–15m` trong giờ hoạt động (Grok, Claude Code)
- `/loop 5m` khi có nhiều PR đang "stale" và bạn đang ship
- GitHub Action trên `pull_request` events (event-driven)

## Required Skills

- `loop-triage` — Đọc PRs, CI checks, review status
- `minimal-fix` — Draft fix nhỏ cho các PR bị CI red
- Reviewer sub-agent — Kiểm chứng proposed fixes (bắt buộc ở L2)

## State

`pr-babysitter-state.md`:

```markdown
# PR Babysitter State

Last run: 2026-06-09 14:30 UTC

## Active PRs
- PR #1250 — fix/ci-auth-refresh — CI: pending — review: 2/3 — stale 4h
  Loop action: Nudge comment sent. Waiting review.
- PR #1248 — dep bump lodash — CI: red (test-auth)
  Loop action: Worktree opened. Fix proposed. Verifier PASS. Waiting human.

## Resolved (last 7d)
- PR #1245 — merged 2026-06-08
```

Fields: PR ID, branch, CI status, review count, time stale, last action, worktree/PR link.

## How the Loop Runs (Typical Cycle)

1. Đọc danh sách open PRs trên watched branches.
2. Với mỗi PR:
   - **Stale** (> N giờ không hoạt động): gửi nudge comment nhẹ nhàng.
   - **CI red**: classify failure → nếu actionable, worktree + implementer + verifier.
   - **Needs review**: nhắc reviewer qua comment/label.
3. Prune merged/closed PRs khỏi active list.

## Verification Strategy

- Verifier phải chạy tests trong worktree trước khi approve.
- Implementer chỉ propose, không merge — **không auto-merge mặc định**.
- Nếu verifier REJECT → dọn worktree, ghi attempt, escalate sau max (vd 3).

## Human Handoff Points

- Fix chạm > 5 files hoặc core architecture
- Security-sensitive changes
- Max attempts exceeded trên cùng PR
- Conflict cần quyết định con người (ví dụ: hai approaches đều hợp lệ)

## Failure Modes & Mitigations

| Failure | Mitigation |
|---------|------------|
| Spammy nudge comments | Chỉ nudge khi PR stale > ngưỡng; không nudge lặp trong cùng ngày |
| Fix nhầm PR | Verifier kiểm tra scope; chỉ action trên PR rõ ràng |
| Token burn với nhiều PR | Giới hạn số PR active loop xử lý mỗi run; early-exit |
| Cùng PR bị 2 loops đụng | `acting_on` trong state + `loop-worktree lock` |

## Cost Profile

| Scenario | Tokens/run | Notes |
|----------|------------|-------|
| No-op (mọi PR ổn) | ~5k | Required — không chạy full khi không có gì |
| Watch + nudge (L1) | ~30k | Scan PRs + CI status |
| Fix attempt (L2) | ~200k | Worktree + implementer + verifier |

**Cadence**: 5–15m · **Tier**: high · **Suggested daily cap**: 2M tokens · **Early exit required**

```bash
npx @cobusgreyling/loop cost --pattern pr-babysitter --cadence 10m --level L1
```

## Success Metrics

- Mean time from "PR stale" to "review/nudge"
- % PRs CI red được resolve không cần human (trivial cases)
- Review turnaround time

---

*Trở về [02 — Bảy Production Patterns](../02-patterns/)*
