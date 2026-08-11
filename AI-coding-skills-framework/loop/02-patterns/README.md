# 🧩 02. Bảy Production Patterns

> Đây là **7 pattern loop** đã được chứng minh có thể chạy trong môi trường thật. Mỗi pattern trả lời: giải quyết vấn đề gì, cadence nào, skills/state nào, cách kiểm chứng, cách bàn giao cho human, và tool-specific notes.

## Bảng Tổng Hợp

| Pattern | Cadence | Level khởi đầu | Token cost |
|---------|---------|---------------|------------|
| [Daily Triage](daily-triage.md) | 1d–2h | **L1** report | Low |
| [PR Babysitter](pr-babysitter.md) | 5–15m | L1 watch | High |
| [CI Sweeper](ci-sweeper.md) | 5–15m | L2 cautious | Very high |
| [Dependency Sweeper](dependency-sweeper.md) | 6h–1d | L2 patch-only | Medium |
| [Changelog Drafter](changelog-drafter.md) | 1d or tag | **L1** draft | Low |
| [Post-Merge Cleanup](post-merge-cleanup.md) | 1d–6h | **L1** off-peak | Low |
| [Issue Triage](issue-triage.md) | 2h–1d | **L1** propose-only | Low |

## Pattern Picker — Chọn Loop Nào?

```
What hurts right now?
  ├── CI red? ──► CI Sweeper
  ├── PRs stalling? ──► PR Babysitter
  ├── Morning chaos / noisy issues? ──► Daily Triage + Issue Triage
  ├── Dependabot / CVE noise? ──► Dependency Sweeper
  ├── Merge debt / TODOs piling up? ──► Post-Merge Cleanup
  ├── Release notes stale? ──► Changelog Drafter
  └── Tight token budget? ──► Changelog Drafter / Daily Triage (L1)
```

### Cost-aware Picks

| Situation | Nên chọn | Tránh (cho đến khi có budget + early-exit) |
|-----------|----------|---------------------------------------------|
| Hobby / plan eo hẹp | Changelog Drafter, Daily Triage (L1), Post-Merge | CI Sweeper ở 5m, PR Babysitter ở 5m |
| CI đang đỏ | CI Sweeper ở **15m+** với early-exit | Full triage mỗi 5m khi main xanh |
| Nhiều PR mở | PR Babysitter 10–15m, L1 watch trước | L2 fix loops trên mọi tick |
| Tuần release | Changelog Drafter daily | Dependency Sweeper + CI Sweeper unattended |

### Overlap Rules

| Combination | Rule |
|-------------|------|
| CI Sweeper + PR Babysitter | CI Sweeper sở hữu failing checks; PR Babysitter không re-fix cùng branch trong cùng giờ |
| Daily Triage + bất kỳ | Daily Triage reports; action loops execute. Triage không auto-fix ở L1 |
| Dependency Sweeper + CI Sweeper | Pause Dependency Sweeper khi CI đỏ trên main |
| Post-Merge + PR Babysitter | Post-Merge chạy off-peak only |
| Changelog Drafter + bất kỳ | Changelog Drafter read-mostly, an toàn; không auto-publish |

## First Loop Recommendation

Nếu không chắc, bắt đầu với **Daily Triage ở L1**. Nó dạy kỷ luật state mà không có rủi ro auto-merge.

## Cách Dùng Một Pattern

1. **Chọn pattern**: xem bảng trên hoặc decision tree phía trên.
2. **Scaffold**: `npx @cobusgreyling/loop init . --pattern <name> --tool grok` (hoặc `--tool claude` / `--tool opencode` / `--tool codex`).
3. **Copy skills** từ `templates/` nếu cần custom.
4. **Setup scheduling** (`/loop`, `scheduler_create`, GitHub Action, Codex Automation).
5. **Chạy tuần một ở L1 report-only** trước khi bật fixes.
6. **Audit**: `npx @cobusgreyling/loop audit . --suggest`.

> **Quy tắc vàng**: đừng bao giờ nhảy lên L3 cho một pattern mới trên production repo. Xem [04-operating](../04-operating/) về upgrade path.
