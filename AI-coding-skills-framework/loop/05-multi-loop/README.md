# 🔗 05. Multi-Loop Coordination

> Chạy nhiều hơn một loop trong repo là bình thường. Chạy chúng **không ranh giới** là cách các loops chiến đấu với nhau. Phần này hướng dẫn phối hợp an toàn.

---

## 1. Principles

1. **Một owner mỗi branch** — tối đa một loop mutate một branch mỗi giờ.
2. **State files riêng biệt** — `STATE.md` cho triage; pattern-specific files cho action loops.
3. **Triage reports, action loops execute** — Daily Triage L1 không bao giờ cạnh tranh với CI Sweeper fixes.
4. **Shared denylist** — copy cùng path denylist vào mọi LOOP.md.
5. **Aggregate token budget**.

---

## 2. Recommended State Layout

```
STATE.md                    # Daily Triage (priorities, human inbox)
pr-babysitter-state.md      # PR watcher
ci-sweeper-state.md         # Active CI failures + attempt counts
dependency-sweeper-state.md # In-flight package updates
post-merge-state.md         # Cleanup backlog
loop-run-log.md             # Append-only observability
```

Linear / GitHub Projects hoạt động tương đương — loop phải **đọc và ghi** cùng store mỗi run.

---

## 3. Priority Khi Loops Xung Đột

| Priority | Loop | Lý do |
|----------|------|-------|
| 1 | CI Sweeper | Red main chặn mọi thứ |
| 2 | PR Babysitter | PRs active nhạy thời gian |
| 3 | Dependency Sweeper | Pause khi CI red |
| 4 | Post-Merge Cleanup | Off-peak, urgency thấp nhất |
| 5 | Daily Triage | Reports only ở L1; điều phối cái khác |

---

## 4. Scheduler Coordination

Document trong root `LOOP.md`:

```markdown
## Multi-loop schedule
- CI Sweeper: /loop 15m (active hours)
- PR Babysitter: /loop 10m (active hours, skip nếu CI Sweeper đang action trên cùng PR)
- Daily Triage: /loop 1d 08:00
- Dependency Sweeper: /loop 6h (skip nếu main CI red)
- Post-Merge: /loop 1d 22:00
```

---

## 5. Collision Detection

Mỗi action loop nên ghi `acting_on: branch-or-pr-id` trong state file. Trước khi spawn một fix:

1. Đọc tất cả pattern state files khác
2. Nếu loop khác `acting_on` khớp → skip và log vào `loop-run-log.md`

**`loop-worktree` mã hoá điều này thành advisory lock** thay vì convention tự kiểm:

```bash
# Control script của loop, trước khi spawn worktree:
npx @cobusgreyling/loop-worktree lock --paths <globs> --owner <pattern>
# Sau khi xong:
npx @cobusgreyling/loop-worktree unlock --owner <pattern>
```

`loop-worktree create` không tự kiểm locks — hai lệnh này paired by convention trong control script.

`loop-sandbox` theo cùng convention qua option `--lock-paths` (opt-in) — một one-shot sandboxed agent run cũng là một control script có thể collide với scheduled loop.

---

## 6. Human Inbox

Dùng shared section trong `STATE.md`:

```markdown
## Human Inbox (ambiguous / cross-loop)
- [ ] PR #42: CI Sweeper và PR Babysitter đều flag — human chọn owner
```

---

## 7. Ví Dụ: Safe Three-Loop Setup

| Loop | Level | Cadence |
|------|-------|---------|
| Daily Triage | L1 | 1d |
| PR Babysitter | L2 | 10m |
| Post-Merge Cleanup | L1 → L2 | 1d off-peak |

Thêm CI Sweeper **chỉ sau khi** PR Babysitter attempt limits và verifier đã được chứng minh trong hai tuần.

---

## 8. Bài Học Thực Tế

- [stories/multi-loop-collision.md](https://github.com/cobusgreyling/loop-engineering/blob/main/stories/multi-loop-collision.md) — hai loops đánh nhau trên cùng branch
- [stories/dependency-vs-ci-sweeper-collision.md](https://github.com/cobusgreyling/loop-engineering/blob/main/stories/dependency-vs-ci-sweeper-collision.md) — Dependency Sweeper đụng CI Sweeper

---

*Tiếp theo: [06 — Anti-Patterns & Failure Modes](../06-anti-patterns/) → [07 — Tools & Ecosystem](../07-tools/)*
