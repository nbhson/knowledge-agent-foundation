# 🔗 05. Multi-Loop Coordination

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Multi-loop coordination là **luật giao thông cho nhiều loops chạy chung một repo** — phân quyền sở hữu branch, tách state file, xếp hạng ưu tiên khi xung đột, và cơ chế phát hiện va chạm (collision detection). Mục tiêu: nhiều loops chạy song song mà không "đánh nhau".
> **Ẩn dụ/so sánh:** Giống **một ngã tư không có đèn đỏ** — nếu mỗi người lái tự quyết, ai cũng nghĩ mình được ưu tiên, kẹt xe và tai nạn xảy ra. Đèn đỏ (lock), biển báo (state files), và xếp hạng ưu tiên (priority) giúp mọi xe đi qua an toàn. Một repo có nhiều loops không hề xấu — chỉ nguy hiểm khi **không có ranh giới**.
> **Vì sao quan trọng:** Khi bạn có 2+ loops (Daily Triage + CI Sweeper chẳng hạn), nếu không phối hợp chúng sẽ sửa cùng file, cùng PR hoặc mất nhau dữ liệu. Phần này ngăn điều đó trước khi bạn phải học bằng sai lầm.

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

> **Đọc sao cho dễ:** Khi hai loops muốn làm cùng một thứ, kẻ nào "cháy" hơn sẽ thắng — CI đỏ (loop 1) ngăn mọi thứ khác vì repo không ai merge được. Đọc hàng trên xuống như thang ưu tiên: Xung đột thì loop xếp trên thắng, loop xếp dưới tự nhường.

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

> **Đọc sao cho dễ:** Collision detection là "**nhìn trước khi băng qua đường**" — mọi loop ghi `acting_on` (đang làm gì) lên state; trước khi bắt tay vào việc, loop **đọc** các state khác để chắc không ai đang làm điều đó. Tool `loop-worktree lock/unlock` biến việc này thành khoá cơ học (advisory lock) thay vì tin vào kỷ luật tự giác.

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
