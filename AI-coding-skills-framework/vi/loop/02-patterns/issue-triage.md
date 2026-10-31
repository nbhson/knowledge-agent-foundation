# 🗂️ Issue Triage Loop

**Goal**: Phân loại noisy issues thành actionable backlog — gợi ý, không tự sửa. Feeder cho Daily Triage.

**Đọc Goal thế nào**: "Noisy issues" = những issue mơ hồ, trùng lặp, hoặc report thiếu thông tin. "Actionable backlog" = danh sách việc có thể làm được ngay. "Feeder" = loop này chỉ **nạp nguyên liệu** (danh sách issue đã phân loại) cho loop Daily Triage chạy sau nó — nó không tự sửa code.

## Scheduling

**Phần này giải thích**: loop nên chạy với nhịp nào. "Scheduling" = đặt lịch chạy tự động.

**Khuyên dùng**:
- `/loop 2h–1d` (Grok, Claude Code) — chạy lại mỗi 2 tiếng đến 1 ngày. `/loop` = lệnh bật vòng lặp tự động.
- GitHub Action cron nhiều lần/ngày cho repos nhiều issues — "cron" = hẹn giờ chạy tự động trên GitHub, không cần máy bạn mở.

## Required Skills

**Phần này giải thích**: loop cần những "kỹ năng" (skill = bộ chỉ thị đóng gói cho agent) nào để chạy.

- `loop-triage` — Đọc issues, classify severity/priority, detect duplicates/stale. "Severity" = mức nghiêm trọng; "duplicates" = issue trùng nhau; "stale" = issue cũ bỏ quên, không ai quan tâm nữa.
- `issue-intake` — Handle issues quá mơ hồ: clarify hoặc escalate, không đoán mò. "Clarify" = hỏi lại người report thêm thông tin; "escalate" = đẩy lên cho người thật xử lý.

## State

**Phần này giải thích**: file lưu trí nhớ giữa các lần chạy. Mỗi lần chạy loop đọc file này để biết lần trước đã làm gì, rồi cập nhật lại.

`issue-triage-state.md`:

```markdown
# Issue Triage State

Last run: 2026-06-09 10:00 UTC

## New Issues (last 24h)
- #1310 — bug: auth timeout — [High, actionable] — suggested: reproduce + fix
- #1311 — "app slow" — [Ambiguous] — loop-intake: cần thông tin thêm, đã comment hỏi
- #1312 — duplicate of #1305 — [Dup] — suggested: close

## Needs Human
- #1298 — feature request lớn — cần product decision
```

Cách đọc ví dụ: dòng `#1311` nghĩa là issue "app chậm" quá mơ hồ, loop đã comment hỏi lại người report thay vì tự đoán. "Actionable" = làm được ngay; "Ambiguous" = chưa đủ thông tin; "Dup" = trùng issue cũ.

## How the Loop Runs (Typical Cycle)

**Phần này giải thích**: một lượt chạy diễn ra theo các bước nào.

1. Đọc open issues mới/updated (last 24h) — chỉ những issue còn mở, xuất hiện hoặc có thay đổi trong 24 giờ qua.
2. Với mỗi issue:
   - **Classify**: bug / feature / question / duplicate / stale — gắn nhãn xem đây là lỗi, tính năng mới, câu hỏi, issue trùng, hay issue bỏ quên.
   - **Mơ hồ** (không đủ để verify "done"): loop-intake skill hỏi thêm hoặc escalate — **không đoán mò**. "Verify done" = kiểm tra được việc đã hoàn thành hay chưa; nếu không kiểm tra được thì đừng tự làm.
   - **Actionable**: ghi suggested next action vào state — ghi đề nghị bước tiếp theo vào file trạng thái, ví dụ "reproduce rồi fix".
3. Cập nhật `issue-triage-state.md` — chỉ gợi ý, không tự sửa (L1 propose-only). "L1 propose-only" = mức tự chủ thấp nhất có hành động: loop chỉ **đề xuất**, mọi thay đổi đều chờ người duyệt.
4. High-priority issues trở thành nguồn cho Daily Triage — issue quan trọng sẽ được loop Daily Triage (loop xếp việc theo ngày) nhận xử lý tiếp.

> **Tóm gọn 1 câu:** Loop này mỗi vài giờ quét issue mới, gắn nhãn và ghi đề nghị xử lý vào file state — nó chỉ gợi ý, không tự sửa code.

## Verification Strategy

**Phần này giải thích**: làm sao tin được kết quả của loop. "Verification" = kiểm chứng.

- Level **L1 propose-only** — loop chỉ phân loại và gợi ý, không edit code. Rủi ro thấp nhất nên không cần verifier (phần kiểm chứng riêng).
- Triage skill **signal only** — không invent architectural work. "Signal only" = chỉ **báo tín hiệu** ("issue này nên xử lý"), không tự nghĩ ra việc lớn kiểu refactor kiến trúc.
- Mỗi finding kèm evidence (link issue, lý do phân loại) — "finding" = kết quả loop tìm ra; "evidence" = bằng chứng, để người review kiểm tra được loop phân loại đúng hay sai.

## Human Handoff Points

**Phần này giải thích**: lúc nào loop phải dừng và giao lại cho người. "Handoff" = bàn giao.

- Feature requests cần product decision — tính năng mới lớn ảnh hưởng định hướng sản phẩm, người thật phải quyết.
- Issues mơ hồ sau khi hỏi vẫn chưa rõ — đã hỏi lại mà vẫn mù mờ thì đừng đoán nữa.
- Issues high-priority + chưa có owner — "owner" = người phụ trách; việc nóng mà không ai nhận thì cần người sắp xếp.
- Bảo mật/security issues (escalate ngay) — lỗi bảo mật phải báo người lập tức, không để loop tự xử.

## Failure Modes & Mitigations

**Cách đọc bảng này**: cột "Failure" = lỗi loop hay mắc phải; cột "Mitigation" = cách phòng chống lỗi đó. Ví dụ dòng 1: loop phân loại lung tung tạo nhiễu → khắc phục bằng siết luật trong skill.

| Failure | Mitigation |
|---------|------------|
| Triage tạo noise | Tighten skill rules; "Noise / Ignore" section |
| Phân loại sai | Evidence cho mỗi finding; human review định kỳ |
| Đoán mò issue mơ hồ | loop-intake: hỏi thêm hoặc escalate, không guess |
| Overwhelm với nhiều issues | Ưu tiên theo severity; giới hạn xử lý mỗi run |

## Cost Profile

**Cách đọc bảng này**: cột "Scenario" = tình huống; "Tokens/run" = số token (đơn vị tính tiền mô hình) mỗi lượt chạy; "Notes" = giải thích. "No-op" = lượt chạy không có gì để làm.

| Scenario | Tokens/run | Notes |
|----------|------------|-------|
| No-op | ~5k | Không có issue mới |
| Full triage | ~40k | Scan issues + classify |

**Cadence**: 2h–1d · **Tier**: low · **Suggested daily cap**: 100k tokens — "Tier" = mức độ nguy hiểm/cần chú ý; "daily cap" = trần token cho phép mỗi ngày, vượt thì dừng.

> 📄 **Code ví dụ:** [`examples/01-cost-profile.sh`](examples/01-cost-profile.sh)

## Success Metrics

**Phần này giải thích**: đo gì để biết loop có ích hay chỉ đốt tiền.

- Time từ "issue mới" đến "được phân loại + suggested action" — càng ngắn càng tốt.
- % phân loại chính xác (không phải re-triage) — "re-triage" = phải phân loại lại vì lần trước sai.
- Giảm issue backlog "mồ côi" không ai biết — "backlog mồ côi" = issue tồn đọng lâu ngày không ai nhận.

> **Pair tự nhiên**: Issue Triage (phân loại) → Daily Triage (ưu tiên) → action loops (thực thi). Low risk, excellent first pair với Daily Triage. Nghĩa là: ba loop này ghép tự nhiên thành dây chuyền — phân loại rồi ưu tiên rồi làm — và đây là cặp loop an toàn nhất để bắt đầu.

---

*Trở về [02 — Bảy Production Patterns](../02-patterns/)*
