# 🧩 02. Bảy Production Patterns

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Nói ngắn gọn, một "production pattern" là **mẫu vòng lặp đã có người dùng thật và chạy ổn ngoài thực tế** — có sẵn scheduler, skills, state, cách kiểm chứng và cách bàn giao cho con người. Thay vì tự vẽ loop từ đầu, bạn chỉ cần chọn mẫu hợp nhất rồi chạy `loop init` để dựng khung.
> **Hình dung cho dễ:** Cứ như **gọi món ở quán quen** — bạn không cần tự nghĩ công thức; bếp (repo loop-engineering) đã nấu thử, đã bán cho khách thật, và ghi chú rõ "món này cay (tốn token), món này lành cho người mới (L1)". Việc của bạn chỉ là chọn món hợp với mình.
> **Vì sao đáng quan tâm:** Mỗi chi tiết trong các pattern này (chạy bao lâu một lần, tốn bao nhiêu token, hay hỏng theo kiểu gì) đều là bài học trả bằng tiền thật, không phải lý thuyết suông. Bạn dùng lại kinh nghiệm đó để khỏi vấp đúng 7 cái hố mà người đi trước đã gặp.

> Dưới đây là **7 mẫu loop dùng được thật ngoài production**. Mỗi mẫu trả lời ngắn gọn: giải quyết việc gì, chạy bao lâu một lần, cần skills/state nào, kiểm chứng ra sao, bàn giao cho con người thế nào, cùng vài lưu ý riêng theo từng tool.

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

> **Đọc bảng này thế nào:** Bạn chỉ cần trả lời một câu "chỗ nào đang đau nhất lúc này?" rồi đi theo nhánh tương ứng. Nếu đau hai chỗ cùng lúc, đọc tiếp `Overlap Rules` để biết loop nào chạy chung được với loop nào.

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

Nếu bạn còn phân vân chưa biết bắt đầu từ đâu, cứ chọn **Daily Triage ở L1**. Loop này giúp bạn làm quen với nếp ghi state mà không lo nó tự merge linh tinh.

## Cách Dùng Một Pattern

1. **Chọn mẫu**: nhìn bảng hoặc cây quyết định ở trên.
2. **Dựng khung**: `npx @cobusgreyling/loop init . --pattern <name> --tool grok` (hoặc `--tool claude` / `--tool opencode` / `--tool codex`).
3. **Chép thêm skills** từ `templates/` nếu bạn muốn tùy biến thêm.
4. **Gắn lịch chạy** (`/loop`, `scheduler_create`, GitHub Action, Codex Automation).
5. **Tuần đầu cứ chạy ở L1 report-only** rồi hãy mở thêm quyền tự sửa.
6. **Chấm điểm lại**: `npx @cobusgreyling/loop audit . --suggest`.

> **Nhớ kỹ**: đừng nhảy thẳng lên L3 cho mẫu mới trên repo production. Xem [04-operating](../04-operating/) để biết lộ trình nâng cấp từ từ.
