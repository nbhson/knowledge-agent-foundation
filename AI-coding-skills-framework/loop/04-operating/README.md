# 🛠️ 04. Operating Loops trong Production

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Operating là "vận hành" — khi loop đã chạy thật trong production, công việc của bạn chuyển từ thiết kế sang **giám sát và điều khiển**: theo dõi token cost, đọc run log, xem metrics, và quyết định khi nào giảm tốc / tạm dừng / giết một loop.
> **Ẩn dụ/so sánh:** Giống **phi công trên buồng lái** — máy bay (loop) đã cất cánh rồi; việc của bạn không phải sửa động cơ giữa chừng, mà là đọc đồng hồ (metrics), kiểm tra nhiên liệu (token budget), và quyết định có hạ cánh sớm (kill) khi có cảnh báo.
> **Vì sao quan trọng:** Loop đầu tiên của bạn sẽ đốt tiền token — đó là chuyện bình thường. Phần này dạy bạn **ước lượng trước khi chạy** (tránh sốc bill), **ghi log để debug** ("tại sao nó làm vậy?"), và **dừng đúng lúc** trước khi thiệt hại thành thảm họa.

> Chạy một loop là công việc operations. Phần này bao gồm: **Token Budget**, **Logging**, **Metrics**, và **khi nào pause hoặc kill** một loop.

---

## 1. Token & Cost Budgeting

> **Đọc sao cho dễ:** Câu hỏi ở đây là "**loop này sẽ tốn bao nhiêu tiền mỗi ngày?**" — giống tính tiền xăng trước một chuyến đi xa. Bạn dùng `loop cost` để ước lượng, rồi đặt **giới hạn (budget)** và **điểm dừng (kill switch)** nếu vượt quá. Quy tắc nhớ: cadence càng nhanh, sub-agent càng nhiều, chi phí càng cao gấp bội.

**Ước lượng trước khi schedule:**

```bash
npx @cobusgreyling/loop cost --pattern <id> --cadence <interval> --level L1
npx @cobusgreyling/loop init . --pattern <id>   # scaffold loop-budget.md + loop-run-log.md + loop-budget skill
```

`loop-audit` chấm điểm cost observability và **cap L3** cho đến khi có budget + run log + LOOP.md budget section.

### Các Yếu Tố Ước Lượng

| Yếu tố | Ảnh hưởng |
|--------|-----------|
| Cadence | Linear multiplier (5m vs 1d = 288× runs/ngày) |
| Sub-agents per run | Mỗi cái = full model + tool round-trips |
| Context size | Repos lớn + full CI logs = triage đắt |
| Verifier model | Model mạnh hơn trên verifier = đáng giá cho unattended |

### Example Estimates (~50k tokens cho light triage run, ~200k cho run với implementer + verifier)

| Loop | Cadence | Runs/ngày | Rough daily tokens |
|------|---------|-----------|--------------------|
| Daily triage (report only) | 1d | 1 | ~50k |
| CI sweeper (light) | 15m | 96 | ~5M (nếu full — **tránh**) |
| PR babysitter | 5m | 288 | High — dùng early exit |

> **Best practice**: triage pass rẻ; chỉ spawn sub-agents khi state báo actionable. Empty watchlist → exit trong < 5k tokens.

### Budget Rules

```markdown
## Loop Budget — Project X
- Max tokens/day: 2M (adjust theo plan)
- On exceed: pause schedulers, notify human
- Max sub-agent spawns per run: 3
```

Encode trong skill hoặc scheduler prompt: *"If no high-priority items, exit immediately."*

---

## 2. Logging Mỗi Run

> **Đọc sao cho dễ:** Log là "**hộp đen**" của loop — mỗi lần chạy ghi một dòng trả lời: chạy bao lâu? tìm được gì? làm gì? tốn bao nhiêu? Sau này khi thắc mắc "vì sao nó không xử lý X", bạn mở log ra là có câu trả lời. Chuẩn là **append-only**: chỉ thêm, không sửa, không xoá.

Minimum log entry (append vào `loop-run-log.md` hoặc structured JSON):

```json
{
  "run_id": "2026-06-09T08:15:00Z",
  "pattern": "daily-triage",
  "duration_s": 45,
  "items_found": 4,
  "actions_taken": 1,
  "escalations": 0,
  "tokens_estimate": 52000,
  "outcome": "success"
}
```

Human-readable alternative trong `STATE.md` footer:

```markdown
---
Run log: 2026-06-09 08:15 | 4 findings | 1 worktree opened | 0 escalations
```

---

## 3. Metrics Dashboard

> **Đọc sao cho dễ:** Metrics là "**bảng cân này của loop**" — mỗi tuần bạn nhìn vào và hỏi: loop có thực sự giúp ích không, hay chỉ tốn tiền làm nhiễu? Điền các cột trống trong bảng dưới (runs, findings, escalations, false positives) cho từng pattern để thấy xu hướng, chứ không phải cảm giác.

Theo dõi hàng tuần (spreadsheet hoặc Notion):

| Metric | PR Babysitter | Daily Triage | CI Sweeper |
|--------|---------------|--------------|------------|
| Runs | | | |
| Actionable findings | | | |
| Auto-fixes proposed | | | |
| Human escalations | | | |
| False positives | | | |
| Mean time to human awareness | | | |
| Token spend (est.) | | | |

Pattern-specific success metrics nằm trong từng [pattern](../02-patterns/).

---

## 4. Khi Nào Slow Down / Pause / Kill

> **Đọc sao cho dễ:** Đây là "**thang đo dầu phanh**" — 3 mức ứng với mức độ nghiêm trọng: **Slow down** (giảm ga vì hết nhiên liệu chút nữa), **Pause** (tạm dừng vì đang có nguy hiểm ngay trước mặt), **Kill** (dừng hẳn vì con đường này không còn đáng đi). Câu hỏi mỗi lần gặp sự cố: đang ở mức nào?

### Slow Down

- Token budget > 80% giữa tuần
- False positive rate > 30% trên triage
- Cùng item escalated 2+ lần trong 48h
- Tuần release lớn — pause auto-fix loops, report-only

### Pause

- Production incident đang xảy ra (loop có thể phá hotfix)
- Breaking schema migration đang diễn ra
- Human reviewer chính OOO + auto-merge đã bật (đừng)

### Kill

- S2 failures liên tục từ [failure catalog](../06-anti-patterns/README.md#2-failure-mode-catalog)
- Cost > value trong 2 tuần liên tiếp
- Team mute hết notifications
- Pattern bị thay thế bởi event-driven alternative (VD: chỉ còn CI Action)

**Kill checklist**:
1. `scheduler_delete` / disable Automation / remove Action
2. Archive state file với `status: retired`
3. Post-mortem trong `stories/` (optional nhưng giá trị)

---

## 5. Upgrade Path

```
Report-only (L1) → 1–2 tuần triage ổn định
       ↓
Small auto-wins (L2) → verifier + worktree + max attempts
       ↓
Connectors (L2+) → PRs/tickets tự cập nhật
       ↓
Unattended (L3) → chỉ khi có denylist, budget, metrics, human gates
```

**Never skip L1** cho một pattern mới trên production repo.

---

*Tiếp theo: [05 — Multi-Loop Coordination](../05-multi-loop/) → [06 — Anti-Patterns & Failure Modes](../06-anti-patterns/)*
