# 👶 PR Babysitter Loop

**Goal**: Theo dõi PRs đang chờ review/CI/rebase, nhắc nhở, và gợi ý fix nhỏ.

**Đọc Goal thế nào**: "PR" = pull request, một đề nghị gộp code vào nhánh chính. "Baby sit" = trông trẻ — loop này canh những PR đang "kẹt": chờ người review, chờ CI (hệ thống chạy test tự động) chạy xong, hay cần rebase (cập nhật code mới từ nhánh chính). Nó nhắc nhẹ nhàng và đề xuất bản sửa nhỏ.

## Scheduling

**Phần này giải thích**: loop nên chạy với nhịp nào.

**Khuyên dùng**:
- `/loop 10–15m` trong giờ hoạt động (Grok, Claude Code) — chạy lại mỗi 10–15 phút khi team đang làm việc.
- `/loop 5m` khi có nhiều PR đang "stale" và bạn đang ship — "stale" = PR đứng yên lâu không ai đụng; "ship" = đang ở giai đoạn dồn dập tung bản mới.
- GitHub Action trên `pull_request` events (event-driven) — chạy **khi có sự kiện** (PR mới, có comment) thay vì chạy theo lịch. "Event-driven" = kích hoạt theo sự kiện.

## Required Skills

**Phần này giải thích**: loop cần kỹ năng (skill = bộ chỉ thị đóng gói cho agent) nào.

- `loop-triage` — Đọc PRs, CI checks, review status. "CI checks" = kết quả test tự động trên từng PR.
- `minimal-fix` — Draft fix nhỏ cho các PR bị CI red. "CI red" = test tự động đang thất bại.
- Reviewer sub-agent — Kiểm chứng proposed fixes (bắt buộc ở L2). "Sub-agent" = agent con do loop triệu gọi; agent này riêng biệt với agent viết fix, để người viết không tự duyệt code của mình.

## State

**Phần này giải thích**: file ghi nhớ giữa các lần chạy, để loop biết đang trông PR nào và đã làm gì.

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

Cách đọc ví dụ: dòng `PR #1250` nghĩa là PR này test chưa xong (pending), đã có 2 trên 3 lượt review cần, đứng yên 4 giờ — loop đã gửi comment nhắc và đang chờ người review. Dòng `PR #1248` nghĩa là test đỏ vì lỗi ở `test-auth`; loop đã mở worktree (bản sao tạm của repo), soạn bản sửa, verifier (agent kiểm chứng) đã duyệt — giờ chờ người bấm merge.

Fields: PR ID, branch, CI status, review count, time stale, last action, worktree/PR link — nghĩa là mỗi dòng trong state ghi: mã PR, nhánh, trạng thái test, số lượt review, thời gian đứng yên, hành động cuối, và link tới bản sửa.

## How the Loop Runs (Typical Cycle)

**Phần này giải thích**: một lượt chạy gồm các bước nào.

1. Đọc danh sách open PRs trên watched branches — quét các PR còn mở trong những nhánh loop được theo dõi.
2. Với mỗi PR:
   - **Stale** (> N giờ không hoạt động): gửi nudge comment nhẹ nhàng. "Nudge" = comment nhắc lịch sự kiểu "PR này cần review giúp nhé", không phải la mắng.
   - **CI red**: classify failure → nếu actionable, worktree + implementer + verifier. Dịch: xác định lỗi test là gì → nếu sửa được theo cách đơn giản, làm trong worktree, rồi có agent riêng kiểm chứng.
   - **Needs review**: nhắc reviewer qua comment/label. "Label" = nhãn gắn lên PR trên GitHub.
3. Prune merged/closed PRs khỏi active list — dọn bỏ khỏi danh sách những PR đã gộp hoặc đã đóng.

> **Tóm gọn 1 câu:** Loop này mỗi 5–15 phút quét các PR đang kẹt, nhắc người review, và tự đề xuất bản sửa nhỏ cho test đỏ — nhưng không bao giờ tự merge.

## Verification Strategy

**Phần này giải thích**: làm sao tin được bản sửa loop đề xuất.

- Verifier phải chạy tests trong worktree trước khi approve — phải chứng minh bằng kết quả test thật, không chỉ "nhìn có ổn".
- Implementer chỉ propose, không merge — **không auto-merge mặc định**. Người viết fix chỉ được đề xuất; nút gộp luôn thuộc về người.
- Nếu verifier REJECT → dọn worktree, ghi attempt, escalate sau max (vd 3). "Attempt" = lần thử; thất bại quá 3 lần trên cùng PR thì dừng và đẩy lên cho người.

## Human Handoff Points

**Phần này giải thích**: lúc nào loop phải dừng và giao cho người.

- Fix chạm > 5 files hoặc core architecture — bản sửa lớn hoặc động vào kiến trúc lõi thì phải người quyết.
- Security-sensitive changes — mọi thứ liên quan bảo mật đều cần người duyệt.
- Max attempts exceeded trên cùng PR — một PR bị thử sửa quá giới hạn thì dừng, tránh đốt token vô ích.
- Conflict cần quyết định con người (ví dụ: hai approaches đều hợp lệ) — khi hai cách giải quyết đều đúng, chỉ người mới chọn được.

## Failure Modes & Mitigations

**Cách đọc bảng này**: cột "Failure" = lỗi loop hay mắc; cột "Mitigation" = cách phòng chống. Ví dụ dòng cuối: hai loop cùng sửa một PR → phòng bằng ghi trường `acting_on` trong state và khoá worktree.

| Failure | Mitigation |
|---------|------------|
| Spammy nudge comments | Chỉ nudge khi PR stale > ngưỡng; không nudge lặp trong cùng ngày |
| Fix nhầm PR | Verifier kiểm tra scope; chỉ action trên PR rõ ràng |
| Token burn với nhiều PR | Giới hạn số PR active loop xử lý mỗi run; early-exit |
| Cùng PR bị 2 loops đụng | `acting_on` trong state + `loop-worktree lock` |

Glossary cho dòng cuối: `acting_on` = trường ghi rõ "loop này đang giữ PR nào"; `loop-worktree lock` = khoá của tool, biến quy ước "một PR một chủ" thành cơ chế cứng.

## Cost Profile

**Cách đọc bảng này**: "Scenario" = tình huống; "Tokens/run" = số token (đơn vị tính tiền mô hình) mỗi lượt; "Notes" = giải thích. "No-op" = lượt chạy không có việc; "L1/L2" = mức tự chủ tăng dần (báo cáo → tự sửa có kiểm chứng).

| Scenario | Tokens/run | Notes |
|----------|------------|-------|
| No-op (mọi PR ổn) | ~5k | Required — không chạy full khi không có gì |
| Watch + nudge (L1) | ~30k | Scan PRs + CI status |
| Fix attempt (L2) | ~200k | Worktree + implementer + verifier |

**Cadence**: 5–15m · **Tier**: high · **Suggested daily cap**: 2M tokens · **Early exit required** — "Tier: high" = loop này chạy dày và đắt nhất trong các pattern; "early exit required" = bắt buộc thoát sớm khi không có việc, đừng chạy trọn bộ cho có.

> 📄 **Code ví dụ:** [`examples/01-cost-profile.sh`](examples/01-cost-profile.sh)

## Success Metrics

**Phần này giải thích**: đo gì để biết loop có ích.

- Mean time from "PR stale" to "review/nudge" — trung bình bao lâu thì một PR kẹt được nhắc tới.
- % PRs CI red được resolve không cần human (trivial cases) — bao nhiêu phần trăm lỗi test đơn giản loop tự đề xuất fix thành công. "Trivial" = vụn vặt, dễ.
- Review turnaround time — thời gian từ lúc PR chờ review đến lúc được review.

---

*Trở về [02 — Bảy Production Patterns](../02-patterns/)*
