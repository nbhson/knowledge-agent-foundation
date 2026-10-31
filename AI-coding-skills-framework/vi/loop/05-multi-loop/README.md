# 🔗 05. Multi-Loop Coordination

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Multi-loop coordination là **luật giao thông cho nhiều loop cùng chạy trên một repo** — chia nhau quyền giữ branch, mỗi loop một state file riêng, xếp thứ tự ưu tiên khi có va chạm, và có cách phát hiện va chạm (collision detection). Mục tiêu: nhiều loop chạy song song mà không "giẫm chân" nhau.
> **Hình dung cho dễ:** Như **ngã tư không đèn đỏ** — ai cũng cho mình được đi trước thì kẹt xe, thậm chí tai nạn. Có đèn đỏ (lock), biển báo (state file) và thứ tự ưu tiên (priority) thì xe nào cũng qua được. Một repo chạy nhiều loop không hề xấu — chỉ nguy hiểm khi **không có ranh giới rõ ràng**.
> **Vì sao đáng quan tâm:** Khi bạn có từ 2 loop trở lên (ví dụ Daily Triage + CI Sweeper), nếu không phân việc rõ, chúng sẽ sửa cùng file, cùng PR, thậm chí ghi đè dữ liệu của nhau. Phần này giúp bạn chặn chuyện đó từ sớm, thay vì trả giá rồi mới rút kinh nghiệm.

> Chạy nhiều hơn một loop trong repo là chuyện bình thường. Nhưng nếu chạy mà **không kẻ ranh giới rõ ràng** thì các loop sẽ sớm "va" vào nhau. Phần này hướng dẫn cách phối hợp cho an toàn.

---

## 1. Principles

**Phần này giải thích**: 5 luật gốc của multi-loop — mọi thứ bên dưới đều xuất phát từ đây.

1. **Mỗi branch một chủ** — trong một giờ, chỉ một loop được đụng vào một branch. Hai loop cùng sửa một nhánh là công thức cho diff ghép cục ("diff" = tập thay đổi).
2. **Mỗi loop một state file riêng** — `STATE.md` cho triage; action loop thì dùng file riêng theo pattern. "State file" = file ghi trí nhớ giữa các lần chạy; "pattern" = một mẫu loop trong [02-patterns](../02-patterns/).
3. **Triage chỉ báo cáo, action loop mới làm** — Daily Triage L1 không tranh việc với CI Sweeper. Nghĩa là loop phân loại việc chỉ ghi đề xuất, loop làm việc mới được đụng code.
4. **Dùng chung denylist** — chép cùng danh sách path cấm vào mọi LOOP.md. "Denylist" = danh sách file tuyệt đối không được đụng; một loop được đi đường tắt thì cả hệ thống có lỗ.
5. **Ngân sách token tính gộp chung** — tổng chi phí của cả nhóm loop mới là thứ đâm thủng túi bạn, từng cái riêng lẻ thì nhìn luôn nhỏ hơn thật.

> **Tóm gọn 1 câu:** Năm luật: một nhánh một chủ, một loop một state file, triage chỉ báo cáo, denylist dùng chung, ngân sách tính gộp.

---

## 2. Recommended State Layout

**Phần này giải thích**: nên chia file trạng thái ra sao khi chạy nhiều loop. Chia đúng thì loop không ghi đè hay xoá nhầm dữ liệu của nhau.

```
STATE.md                    # Daily Triage (priorities, human inbox)
pr-babysitter-state.md      # PR watcher
ci-sweeper-state.md         # Active CI failures + attempt counts
dependency-sweeper-state.md # In-flight package updates
post-merge-state.md         # Cleanup backlog
loop-run-log.md             # Append-only observability
```

Cách đọc danh sách: mỗi dòng là một file và vai trò của nó. Dịch nghĩa: `STATE.md` = bảng ưu tiên hằng ngày + hộp thư chờ người; "PR watcher" = loop theo dõi pull request; "active CI failures + attempt counts" = lỗi test đang tồn và số lần đã thử sửa; "in-flight package updates" = các lần nâng thư viện đang dở; "cleanup backlog" = việc dọn tồn đọng; "append-only observability" = nhật ký chỉ-thêm để quan sát toàn cục.

Linear / GitHub Projects cũng làm được như vậy — miễn là loop **đọc và ghi đúng một chỗ** mỗi lần chạy. Bảng công việc thay thế được cho file, miễn là điểm đọc và ghi là một.

---

## 3. Priority Khi Loops Xung Đột

> **Đọc đoạn này thế nào:** Hai loop mà muốn làm cùng một việc thì việc nào "cháy" hơn sẽ thắng — CI đỏ (hạng 1) chặn hết vì main đỏ thì chẳng ai merge được gì. Bạn đọc từ trên xuống như thang ưu tiên: có va chạm thì loop xếp trên thắng, loop xếp dưới nhường. "CI đỏ" = hệ thống test tự động đang thất bại; "merge" = gộp code vào nhánh chính.

| Priority | Loop | Lý do |
|----------|------|-------|
| 1 | CI Sweeper | Red main chặn mọi thứ |
| 2 | PR Babysitter | PRs active nhạy thời gian |
| 3 | Dependency Sweeper | Pause khi CI red |
| 4 | Post-Merge Cleanup | Off-peak, urgency thấp nhất |
| 5 | Daily Triage | Reports only ở L1; điều phối cái khác |

Cách đọc bảng: số "Priority" nhỏ hơn = đi trước khi có va chạm. Dịch nghĩa từng dòng: dọn lỗi CI đứng đầu vì nhánh chính đỏ thì không ai gộp được gì; theo dõi PR nhạy thời gian; nâng thư viện thì dừng khi CI đỏ; dọn sau merge chạy giờ thấp điểm nên ít gấp nhất; báo cáo hằng ngày chỉ ghi kết quả và điều phối, không tranh việc.

> **Tóm gọn 1 câu:** Thang ưu tiên cố định: việc chặn mọi người đi trước, việc chờ được thì nhường và tự dừng khi điều kiện chặn xuất hiện.

---

## 4. Scheduler Coordination

**Phần này giải thích**: ghi lịch chạy chung của tất cả loop vào một file duy nhất, để ai cũng thấy nhịp của ai và biết khi nào cần nhường.

Bạn ghi lịch chạy chung trong `LOOP.md` ở root:

```markdown
## Multi-loop schedule
- CI Sweeper: /loop 15m (active hours)
- PR Babysitter: /loop 10m (active hours, skip nếu CI Sweeper đang action trên cùng PR)
- Daily Triage: /loop 1d 08:00
- Dependency Sweeper: /loop 6h (skip nếu main CI red)
- Post-Merge: /loop 1d 22:00
```

Cách đọc ví dụ: mỗi dòng là một loop kèm nhịp chạy — "active hours" = chỉ chạy trong giờ làm việc; "skip" = bỏ qua lượt này khi điều kiện ghi kèm xảy ra. Ví dụ dòng Dependency Sweeper: chạy mỗi 6 giờ, nhưng nếu CI của nhánh chính đang đỏ thì bỏ lượt.

---

## 5. Collision Detection

> **Đọc đoạn này thế nào:** Collision detection nghĩa là "**nhìn trước ngó sau rồi hẵng qua đường**" — loop nào cũng ghi `acting_on` (đang làm gì) lên state; trước khi bắt tay vào việc, loop phải **đọc** state của các loop khác để chắc là không ai đang làm việc đó. Tool `loop-worktree lock/unlock` biến quy ước này thành khóa hẳn hoi (advisory lock) thay vì trông chờ mọi người tự giác. "Worktree" = bản sao tạm của repo để sửa code an toàn; "advisory lock" = khoá yêu cầu mọi bên tự hỏi trước khi lấy.

Mỗi action loop nên ghi `acting_on: branch-or-pr-id` vào state file — nghĩa là "loop này đang giữ nhánh/PR nào". Trước khi tạo một bản fix:

1. Đọc hết state file của các pattern khác
2. Thấy loop khác đang `acting_on` trùng khớp → bỏ qua lượt này và ghi vào `loop-run-log.md`

**`loop-worktree` biến quy ước này thành advisory lock** thay vì chỉ trông chờ tự giác:

> 📄 **Code ví dụ:** [`examples/01-5-collision-detection.sh`](examples/01-5-collision-detection.sh)

Lệnh `loop-worktree create` không tự kiểm tra lock — cặp `lock/unlock` này đi chung với nhau theo quy ước trong control script. Nghĩa là: kịch bản điều khiển của bạn phải lấy khoá trước và nhả khoá sau, vì lệnh tạo worktree không tự hỏi "có ai đang giữ không".

`loop-sandbox` cũng theo quy ước đó qua option `--lock-paths` (bạn tự bật khi cần) — một lượt chạy agent đơn lẻ trong sandbox ("sandbox" = môi trường tách biệt, hỏng cũng không lan) cũng là control script nên vẫn có thể đụng scheduled loop.

> **Tóm gọn 1 câu:** Mỗi loop ghi `acting_on` lên state, đọc state của nhau trước khi làm, và dùng khoá `loop-worktree` — quy ước tự giác là chưa đủ, phải có khoá thật.

---

## 6. Human Inbox

**Phần này giải thích**: một hộp thư duy nhất gom mọi thứ cần người xử lý — việc mơ hồ, tranh chấp giữa các loop — để bạn không phải dò nhiều nơi.

Bạn dành một mục chung trong `STATE.md`:

```markdown
## Human Inbox (ambiguous / cross-loop)
- [ ] PR #42: CI Sweeper và PR Babysitter đều flag — human chọn owner
```

Cách đọc ví dụ: "ambiguous / cross-loop" = mơ hồ hoặc tranh chấp giữa các loop. Dòng dưới: PR #42 bị hai loop cùng đánh dấu ("flag"), người phải chọn ai là chủ sở hữu xử lý. Chọn xong ghi lại để các loop lần sau biết.

---

## 7. Ví Dụ: Safe Three-Loop Setup

**Phần này giải thích**: bộ ba loop an toàn để lần đầu chạy nhiều loop — thận trọng tăng dần, không bật hàng loạt.

| Loop | Level | Cadence |
|------|-------|---------|
| Daily Triage | L1 | 1d |
| PR Babysitter | L2 | 10m |
| Post-Merge Cleanup | L1 → L2 | 1d off-peak |

Cách đọc bảng: "Level" = bậc tự chủ (L1 = chỉ báo cáo, L2 = tự sửa nhỏ có verifier kiểm); "Cadence" = nhịp chạy. Dòng 3: loop dọn sau merge bắt đầu ở mức chỉ báo cáo, chứng minh an toàn rồi mới lên mức tự sửa, và chỉ chạy giờ thấp điểm ("off-peak").

Bạn thêm CI Sweeper **chỉ sau khi** attempt limits và verifier của PR Babysitter đã được kiểm chứng ổn trong hai tuần — "attempt limits" = giới hạn số lần thử sửa trên cùng một việc.

---

## 8. Bài Học Thực Tế

**Phần này giải thích**: hai bài viết ghi lại sự cố thật khi các loop va nhau — đọc để thấy hậu quả trước khi tự mắc.

- [stories/multi-loop-collision.md](https://github.com/cobusgreyling/loop-engineering/blob/main/stories/multi-loop-collision.md) — hai loops đánh nhau trên cùng branch
- [stories/dependency-vs-ci-sweeper-collision.md](https://github.com/cobusgreyling/loop-engineering/blob/main/stories/dependency-vs-ci-sweeper-collision.md) — Dependency Sweeper đụng CI Sweeper

---

*Tiếp theo: [06 — Anti-Patterns & Failure Modes](../06-anti-patterns/) → [07 — Tools & Ecosystem](../07-tools/)*
