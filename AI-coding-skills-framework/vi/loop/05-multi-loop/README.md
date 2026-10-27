# 🔗 05. Multi-Loop Coordination

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Multi-loop coordination là **luật giao thông cho nhiều loop cùng chạy trên một repo** — chia nhau quyền giữ branch, mỗi loop một state file riêng, xếp thứ tự ưu tiên khi có va chạm, và có cách phát hiện va chạm (collision detection). Mục tiêu: nhiều loop chạy song song mà không "giẫm chân" nhau.
> **Hình dung cho dễ:** Như **ngã tư không đèn đỏ** — ai cũng cho mình được đi trước thì kẹt xe, thậm chí tai nạn. Có đèn đỏ (lock), biển báo (state file) và thứ tự ưu tiên (priority) thì xe nào cũng qua được. Một repo chạy nhiều loop không hề xấu — chỉ nguy hiểm khi **không có ranh giới rõ ràng**.
> **Vì sao đáng quan tâm:** Khi bạn có từ 2 loop trở lên (ví dụ Daily Triage + CI Sweeper), nếu không phân việc rõ, chúng sẽ sửa cùng file, cùng PR, thậm chí ghi đè dữ liệu của nhau. Phần này giúp bạn chặn chuyện đó từ sớm, thay vì trả giá rồi mới rút kinh nghiệm.

> Chạy nhiều hơn một loop trong repo là chuyện bình thường. Nhưng nếu chạy mà **không kẻ ranh giới rõ ràng** thì các loop sẽ sớm "va" vào nhau. Phần này hướng dẫn cách phối hợp cho an toàn.

---

## 1. Principles

1. **Mỗi branch một chủ** — trong một giờ, chỉ một loop được đụng vào một branch.
2. **Mỗi loop một state file riêng** — `STATE.md` cho triage; action loop thì dùng file riêng theo pattern.
3. **Triage chỉ báo cáo, action loop mới làm** — Daily Triage L1 không tranh việc với CI Sweeper.
4. **Dùng chung denylist** — chép cùng danh sách path cấm vào mọi LOOP.md.
5. **Ngân sách token tính gộp chung**.

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

Linear / GitHub Projects cũng làm được như vậy — miễn là loop **đọc và ghi đúng một chỗ** mỗi lần chạy.

---

## 3. Priority Khi Loops Xung Đột

> **Đọc đoạn này thế nào:** Hai loop mà muốn làm cùng một việc thì việc nào "cháy" hơn sẽ thắng — CI đỏ (hạng 1) chặn hết vì main đỏ thì chẳng ai merge được gì. Bạn đọc từ trên xuống như thang ưu tiên: có va chạm thì loop xếp trên thắng, loop xếp dưới nhường.

| Priority | Loop | Lý do |
|----------|------|-------|
| 1 | CI Sweeper | Red main chặn mọi thứ |
| 2 | PR Babysitter | PRs active nhạy thời gian |
| 3 | Dependency Sweeper | Pause khi CI red |
| 4 | Post-Merge Cleanup | Off-peak, urgency thấp nhất |
| 5 | Daily Triage | Reports only ở L1; điều phối cái khác |

---

## 4. Scheduler Coordination

Bạn ghi lịch chạy chung trong `LOOP.md` ở root:

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

> **Đọc đoạn này thế nào:** Collision detection nghĩa là "**nhìn trước ngó sau rồi hẵng qua đường**" — loop nào cũng ghi `acting_on` (đang làm gì) lên state; trước khi bắt tay vào việc, loop phải **đọc** state của các loop khác để chắc là không ai đang làm việc đó. Tool `loop-worktree lock/unlock` biến quy ước này thành khóa hẳn hoi (advisory lock) thay vì trông chờ mọi người tự giác.

Mỗi action loop nên ghi `acting_on: branch-or-pr-id` vào state file. Trước khi tạo một bản fix:

1. Đọc hết state file của các pattern khác
2. Thấy loop khác đang `acting_on` trùng khớp → bỏ qua lượt này và ghi vào `loop-run-log.md`

**`loop-worktree` biến quy ước này thành advisory lock** thay vì chỉ trông chờ tự giác:

```bash
# Control script của loop, trước khi spawn worktree:
npx @cobusgreyling/loop-worktree lock --paths <globs> --owner <pattern>
# Sau khi xong:
npx @cobusgreyling/loop-worktree unlock --owner <pattern>
```

Lệnh `loop-worktree create` không tự kiểm tra lock — cặp `lock/unlock` này đi chung với nhau theo quy ước trong control script.

`loop-sandbox` cũng theo quy ước đó qua option `--lock-paths` (bạn tự bật khi cần) — một lượt chạy agent đơn lẻ trong sandbox cũng là control script nên vẫn có thể đụng scheduled loop.

---

## 6. Human Inbox

Bạn dành một mục chung trong `STATE.md`:

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

Bạn thêm CI Sweeper **chỉ sau khi** attempt limits và verifier của PR Babysitter đã được kiểm chứng ổn trong hai tuần.

---

## 8. Bài Học Thực Tế

- [stories/multi-loop-collision.md](https://github.com/cobusgreyling/loop-engineering/blob/main/stories/multi-loop-collision.md) — hai loops đánh nhau trên cùng branch
- [stories/dependency-vs-ci-sweeper-collision.md](https://github.com/cobusgreyling/loop-engineering/blob/main/stories/dependency-vs-ci-sweeper-collision.md) — Dependency Sweeper đụng CI Sweeper

---

*Tiếp theo: [06 — Anti-Patterns & Failure Modes](../06-anti-patterns/) → [07 — Tools & Ecosystem](../07-tools/)*
