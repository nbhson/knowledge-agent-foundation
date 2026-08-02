# 📋 Daily Triage Loop

**Goal**: Bắt đầu mỗi ngày (hoặc mỗi khoảng hoạt động) với một bức tranh ưu tiên, có thể hành động được về những gì cần chú ý — mà không cần tự kiểm tra CI, issues, PRs, chat.

## Scheduling

**Khuyên dùng**:
- `/loop 1d` cho morning triage (Grok, Claude Code)
- `/loop 2h` trong active sprints cho signal nhanh hơn
- GitHub Action cron `0 8 * * 1-5` cho teams không có TUI

Nhiều teams chạy triage-only trước (reporting, không auto-fix) 1–2 tuần trước khi bật action.

## Required Skills

- `loop-triage` — Đọc CI, issues, commits, chat; tạo prioritized findings (output format CHẶT CHẼ)
- `minimal-fix` (optional, phase 2) — Draft small fixes cho obvious failures
- Reviewer sub-agent hoặc skill (optional, phase 2) — Kiểm chứng proposed fixes

## State

Dùng `STATE.md` (hoặc Linear board view) làm memory spine:

```markdown
# Loop State — Project X

Last run: 2026-06-09 08:15 UTC

## High Priority (loop đang xử lý / chờ human)
- [ ] #1241 — flaky test trong auth flow (CI red trên main)
  Loop action: Opened worktree. Fix proposed. Waiting for human PR review.

## Watch List
- PR #1238 open 4 ngày không có hoạt động.

## Recent Noise (ignored lần này)
- Dependabot PRs (automation riêng)
```

Fields loop **bắt buộc** cập nhật mỗi run:
- `Last run` timestamp
- Item status + last action taken
- Human decisions đã override loop

## How the Loop Runs (Typical Cycle)

1. Scheduler fire (sáng hoặc interval).
2. Triage skill ingests: CI failures (24h), open issues/tickets, recent commits, STATE.md cũ.
3. High-priority items append vào state kèm suggested next action.
4. (Phase 2) Với bug nhỏ: worktree → implementer → verifier.
5. (Phase 3) Connectors cập nhật PRs/tickets; items mơ hồ flag cho human.
6. Prune resolved/merged items khỏi state.
7. Ghi **post-run critique**: false positives, items lặp lại, một điều chỉnh cho lần sau.

## Verification Strategy

- Phase 1 (report-only): Human đọc `STATE.md` — không cần auto-action verification.
- Phase 2+: Implementer không bao giờ tự đánh dấu done; verifier confirm fix scope + tests.
- Triage skill **không được invent architectural work** — signal only.

## Human Handoff Points

- Design decisions hoặc multi-file refactors
- Security, auth, payments, infrastructure
- Items flag "needs discussion" trong triage output
- Bất cứ thứ gì loop surface 3+ ngày không có resolution

## Tool-Specific Notes

**Grok Build TUI**:
```bash
/loop 1d Run the loop-triage skill. Append high-priority items to STATE.md. For obvious small bugfixes only: worktree + minimal-fix + verifier sub-agent (maker/checker). Flag ambiguous items for human review.
```

**Claude Code**:
```bash
/loop 1d Run $loop-triage and update STATE.md. Do not auto-fix on first week — report only.
```

**Codex**:
- Automations tab: daily prompt calling `$loop-triage`, output vào Triage inbox + `STATE.md`.

**GitHub Actions**:
- `daily-triage.yml` chạy weekdays, update `STATE.md` + `loop-run-log.md`.

## Failure Modes & Mitigations

| Failure | Mitigation |
|---------|------------|
| Triage tạo noise | Tighten skill rules; thêm "Noise / Ignore" section |
| State file lớn vô hạn | Prune merged/closed items mỗi run |
| Auto-fix sai priority | Bắt đầu report-only; thêm effort/risk gates |
| Missed overnight failures | `fireImmediately: true` hoặc chạy đầu ngày + giữa ngày |
| Stale critique, không được review | Human handoff khi critique tích tụ không resolution qua N runs |

## Cost Profile

| Scenario | Tokens/run | Notes |
|----------|------------|-------|
| No-op | ~5k | Không có gì actionable trong state |
| Full triage (L1) | ~50k | CI + issues + commits scan |
| Assisted fix (L2) | ~200k | Worktree + implementer + verifier |

**Cadence**: 1d–2h · **Tier**: low · **Suggested daily cap**: 100k tokens

```bash
npx @cobusgreyling/loop cost --pattern daily-triage --cadence 1d --level L1
```

## Success Metrics

- Thời gian từ "có gì đó hỏng" đến "human biết"
- % các buổi sáng `STATE.md` khớp với những gì bạn tự tìm được
- Giảm ad-hoc "cái gì đang cháy?" Slack messages

**Bắt đầu report-only. Thêm action chỉ khi triage quality ổn định.**

---

*Trở về [02 — Bảy Production Patterns](../02-patterns/)*
