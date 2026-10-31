# 📋 Daily Triage Loop

**Goal**: Bắt đầu mỗi ngày (hoặc mỗi khoảng hoạt động) với một bức tranh ưu tiên, có thể hành động được về những gì cần chú ý — mà không cần tự kiểm tra CI, issues, PRs, chat.

> **Tóm gọn ý nghĩa:** Triage = phân loại việc theo mức ưu tiên (từ y khoa: chọn ai cứu trước). Loop này như "trợ lý trực sáng": mỗi sáng nó quét CI, issues, PRs, chat rồi viết cho bạn một tờ "hôm nay cần chú ý gì", xếp thứ tự sẵn.

## Scheduling

**Khuyên dùng**:
- `/loop 1d` cho morning triage (Grok, Claude Code) — `/loop 1d` = tự chạy lại mỗi ngày một lần
- `/loop 2h` trong active sprints cho signal nhanh hơn (signal = tín hiệu có việc đáng chú ý)
- GitHub Action cron `0 8 * * 1-5` cho teams không có TUI (cron = lịch hẹn giờ kiểu Linux; `0 8 * * 1-5` nghĩa là 8 giờ sáng thứ Hai đến thứ Sáu)

Nhiều teams chạy triage-only trước (reporting, không auto-fix) 1–2 tuần trước khi bật action.

> **Tóm gọn 1 câu:** Mỗi sáng một lần là nhịp chuẩn; tuần đầu chỉ cho nó báo cáo, chưa cho tự sửa.

## Required Skills

- `loop-triage` — Đọc CI, issues, commits, chat; tạo prioritized findings (output format CHẶT CHẼ). "Prioritized findings" = danh sách việc xếp theo độ ưu tiên; "output format chặt chẽ" = bắt buộc trình bày theo khuôn cố định để code đọc được.
- `minimal-fix` (optional, phase 2) — Draft small fixes cho obvious failures (phase 2 = giai đoạn 2, sau khi giai đoạn 1 chạy ổn)
- Reviewer sub-agent hoặc skill (optional, phase 2) — Kiểm chứng proposed fixes

> **Tóm gọn 1 câu:** Skill bắt buộc chỉ có một: quét nguồn và viết báo cáo ưu tiên; hai skill sửa code và kiểm tra là tùy chọn cho giai đoạn sau.

## State

State = sổ ghi trạng thái giữa các lần chạy, là bộ nhớ duy nhất của loop.

Dùng `STATE.md` (hoặc Linear board view) làm memory spine (memory spine = "xương sống trí nhớ", nguồn sự thật duy nhất):

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

Đọc state này thế nào: mục "High Priority" là việc đang xử lý hoặc chờ người — ví dụ issue #1241 là test chập chờn, loop đã mở worktree và đề xuất sửa, giờ chờ người review PR. "Watch List" là việc đang theo dõi chưa cần hành động. "Recent Noise" là thứ đã chủ động bỏ qua để khỏi nhiễu.

Fields loop **bắt buộc** cập nhật mỗi run:
- `Last run` timestamp
- Item status + last action taken
- Human decisions đã override loop (override = người ra quyết định ngược lại loop)

> **Tóm gọn 1 câu:** State chia 3 ngăn — việc nóng, việc theo dõi, nhiễu đã lọc — và mỗi lần chạy bắt buộc phải cập nhật.

## How the Loop Runs (Typical Cycle)

1. Scheduler fire (sáng hoặc interval) — scheduler fire = lịch hẹn "re" gọi loop chạy.
2. Triage skill ingests: CI failures (24h), open issues/tickets, recent commits, STATE.md cũ (ingests = nuốt vào, tức là đọc và nạp dữ liệu).
3. High-priority items append vào state kèm suggested next action.
4. (Phase 2) Với bug nhỏ: worktree → implementer → verifier.
5. (Phase 3) Connectors cập nhật PRs/tickets; items mơ hồ flag cho human (flag = gắn cờ đánh dấu).
6. Prune resolved/merged items khỏi state.
7. Ghi **post-run critique**: false positives, items lặp lại, một điều chỉnh cho lần sau (critique = tự kiểm điểm; false positive = báo nhầm việc không có vấn đề).

> **Tóm gọn 1 câu:** Vòng chạy: quét mọi nguồn → ghi việc nóng vào state → (sau) sửa bug nhỏ có kiểm tra → dọn việc xong → tự kiểm điểm một điều để lần sau khôn hơn.

## Verification Strategy

- Phase 1 (report-only): Human đọc `STATE.md` — không cần auto-action verification. Nói cách khác, giai đoạn này loop không hành động gì nên không có gì để kiểm chứng ngoài mắt người đọc.
- Phase 2+: Implementer không bao giờ tự đánh dấu done; verifier confirm fix scope + tests.
- Triage skill **không được invent architectural work** — signal only (nghĩa là nó chỉ được báo tín hiệu, không được tự "sáng tác" việc kiến trúc lớn).

> **Tóm gọn 1 câu:** Giai đoạn báo cáo thì người đọc và tự phán; giai đoạn tự sửa thì bắt buộc agent khác xác nhận — và loop không bao giờ tự chế ra việc lớn.

## Human Handoff Points

- Design decisions hoặc multi-file refactors (refactor = làm lại cấu trúc code mà không đổi hành vi)
- Security, auth, payments, infrastructure
- Items flag "needs discussion" trong triage output
- Bất cứ thứ gì loop surface 3+ ngày không có resolution (surface = đưa vào báo cáo)

> **Tóm gọn 1 câu:** Việc đụng thiết kế, bảo mật, tiền bạc, hạ tầng — hoặc việc treo quá 3 ngày — là việc của người, không của loop.

## Tool-Specific Notes

Phần này ghi cách cài loop cho từng tool cụ thể — bạn chỉ đọc dòng của tool đang dùng.

**Grok Build TUI**:
> 📄 **Code ví dụ:** [`examples/01-tool-specific-notes.sh`](examples/01-tool-specific-notes.sh)

**Claude Code**:
> 📄 **Code ví dụ:** [`examples/02-tool-specific-notes.sh`](examples/02-tool-specific-notes.sh)

**Codex**:
- Automations tab: daily prompt calling `$loop-triage`, output vào Triage inbox + `STATE.md`.

**GitHub Actions**:
- `daily-triage.yml` chạy weekdays, update `STATE.md` + `loop-run-log.md`.

> **Tóm gọn 1 câu:** Cùng một pattern, bốn cách cài: chọn đúng dòng của tool bạn đang dùng là đủ.

## Failure Modes & Mitigations

**Cách đọc bảng này:** cột "Failure" là cách loop hay hỏng; cột "Mitigation" là cách phòng. Ví dụ, dòng 1: loop báo quá nhiều việc nhỏ nhặt thành nhiễu → siết luật trong skill và thêm mục "Noise / Ignore" để chủ động bỏ qua.

| Failure | Mitigation |
|---------|------------|
| Triage tạo noise | Tighten skill rules; thêm "Noise / Ignore" section |
| State file lớn vô hạn | Prune merged/closed items mỗi run |
| Auto-fix sai priority | Bắt đầu report-only; thêm effort/risk gates |
| Missed overnight failures | `fireImmediately: true` hoặc chạy đầu ngày + giữa ngày |
| Stale critique, không được review | Human handoff khi critique tích tụ không resolution qua N runs |

> **Tóm gọn 1 câu:** Năm kiểu hỏng đều phòng được bằng một trong ba cách: siết luật skill, dọn state đều, và kịp thời chuyển người khi việc tồn đọng.

## Cost Profile

**Cách đọc bảng này:** "Tokens/run" là chi phí mỗi lần chạy theo tình huống. Ví dụ, sáng không có gì nóng (no-op) chỉ tốn ~5k token, còn buổi quét đầy đủ ~50k, và nếu cho tự sửa (L2) thì lên ~200k.

| Scenario | Tokens/run | Notes |
|----------|------------|-------|
| No-op | ~5k | Không có gì actionable trong state |
| Full triage (L1) | ~50k | CI + issues + commits scan |
| Assisted fix (L2) | ~200k | Worktree + implementer + verifier |

**Cadence**: 1d–2h · **Tier**: low · **Suggested daily cap**: 100k tokens

> 📄 **Code ví dụ:** [`examples/03-cost-profile.sh`](examples/03-cost-profile.sh)

> **Tóm gọn 1 câu:** Phần lớn chi phí nằm ở phần tự sửa (L2) — giữ loop ở mức báo cáo thì mỗi ngày tốn chưa tới 100k token.

## Success Metrics

- Thời gian từ "có gì đó hỏng" đến "human biết"
- % các buổi sáng `STATE.md` khớp với những gì bạn tự tìm được
- Giảm ad-hoc "cái gì đang cháy?" Slack messages (ad-hoc = chớp nhoáng, không có hệ thống)

**Bắt đầu report-only. Thêm action chỉ khi triage quality ổn định.**

> **Tóm gọn 1 câu:** Loop thành công khi bạn biết tin-state-vì-state-đúng, lỗi được biết sớm hơn, và phòng Slack bớt câu "gì đang cháy?".

---

*Trở về [02 — Bảy Production Patterns](../02-patterns/)*
