# 🛠️ 04. Operating Loops trong Production

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Operating nghĩa là "vận hành" — khi loop đã chạy thật ngoài production, việc của bạn chuyển từ thiết kế sang **trông coi và điều tiết**: canh token cost, đọc run log, xem metrics, rồi quyết định lúc nào nên giảm tốc / tạm dừng / dẹp hẳn một loop.
> **Hình dung cho dễ:** Như **ngồi trong buồng lái** — máy bay (loop) đã cất cánh; bạn không cần chui xuống sửa động cơ giữa trời, chỉ cần đọc đồng hồ (metrics), canh nhiên liệu (token budget), và quyết định hạ cánh sớm (kill) khi đèn báo đỏ.
> **Vì sao đáng quan tâm:** Loop đầu tay kiểu gì cũng đốt kha khá token — chuyện đó bình thường. Phần này chỉ bạn **áng chi phí trước khi chạy** (đỡ bất ngờ khi thấy bill), **ghi log để còn biết đường tìm** ("sao nó lại làm vậy?"), và **dừng đúng lúc** trước khi thiệt hại nhỏ thành chuyện lớn.

> Chạy loop thực chất là làm vận hành. Phần này gồm: **ngân sách token (Token Budget)**, **ghi log (Logging)**, **chỉ số (Metrics)**, và **lúc nào nên giảm tốc, tạm dừng hay dẹp bỏ** một loop.

---

## 1. Token & Cost Budgeting

> **Đọc đoạn này thế nào:** Câu hỏi cốt lõi là "**loop này mỗi ngày tốn bao nhiêu tiền?**" — giống như áng tiền xăng trước chuyến đi xa. Bạn dùng `loop cost` để ước lượng, rồi đặt **trần chi tiêu (budget)** và **nút dừng khẩn cấp (kill switch)** phòng khi vượt mức. Nhớ quy tắc: chạy càng dày, đẻ càng nhiều sub-agent thì tiền càng tăng nhanh.

**Ước lượng trước khi schedule:**

```bash
npx @cobusgreyling/loop cost --pattern <id> --cadence <interval> --level L1
npx @cobusgreyling/loop init . --pattern <id>   # scaffold loop-budget.md + loop-run-log.md + loop-budget skill
```

`loop-audit` chấm điểm khả năng quan sát chi phí, và **giữ loop ở L3** cho tới khi có đủ budget, run log và mục budget trong LOOP.md.

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

> **Mẹo hay**: bạn cứ cho lượt triage chạy thật rẻ; chỉ tạo sub-agent khi state báo có việc đáng làm. Watchlist mà trống thì thoát luôn trong vòng < 5k tokens.

### Budget Rules

```markdown
## Loop Budget — Project X
- Max tokens/day: 2M (adjust theo plan)
- On exceed: pause schedulers, notify human
- Max sub-agent spawns per run: 3
```

Ghi thẳng vào skill hoặc prompt của scheduler: *"If no high-priority items, exit immediately."*

---

## 2. Logging Mỗi Run

> **Đọc đoạn này thế nào:** Log là "**hộp đen**" của loop — mỗi lần chạy ghi lại ngắn gọn: chạy bao lâu, thấy gì, đã làm gì, tốn bao nhiêu. Sau này nếu thắc mắc "sao nó không xử lý vụ X", bạn mở log ra là có câu trả lời. Chuẩn ở đây là **append-only**: chỉ thêm dòng mới, không sửa, không xóa.

Mỗi run bạn ghi tối thiểu chừng này (lưu vào `loop-run-log.md` hoặc JSON có cấu trúc):

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

Bản ngắn gọn cho người đọc, đặt ở cuối `STATE.md`:

```markdown
---
Run log: 2026-06-09 08:15 | 4 findings | 1 worktree opened | 0 escalations
```

---

## 3. Metrics Dashboard

> **Đọc đoạn này thế nào:** Metrics là "**sổ theo dõi sức khỏe**" của loop — mỗi tuần bạn mở ra và tự hỏi: loop có thực sự giúp được việc không, hay chỉ tốn tiền và gây nhiễu? Bạn điền số liệu vào bảng dưới (runs, findings, escalations, false positives) cho từng pattern để thấy xu hướng rõ ràng, thay vì đoán theo cảm tính.

Theo dõi theo tuần (bằng spreadsheet hoặc Notion):

| Metric | PR Babysitter | Daily Triage | CI Sweeper |
|--------|---------------|--------------|------------|
| Runs | | | |
| Actionable findings | | | |
| Auto-fixes proposed | | | |
| Human escalations | | | |
| False positives | | | |
| Mean time to human awareness | | | |
| Token spend (est.) | | | |

Chỉ số thành công riêng của từng pattern nằm trong [02-patterns](../02-patterns/).

---

## 4. Khi Nào Slow Down / Pause / Kill

> **Đọc đoạn này thế nào:** Đây là "**chân ga — chân phanh**" — 3 mức theo độ nghiêm trọng: **Slow down** (giảm ga vì sắp hết nhiên liệu), **Pause** (tạm dừng vì có chướng ngại ngay trước mặt), **Kill** (dẹp luôn vì con đường này không còn đáng đi). Mỗi lần có sự cố, bạn tự hỏi: mình đang ở mức nào?

### Slow Down

- Token budget > 80% giữa tuần
- False positive rate > 30% trên triage
- Cùng một item bị escalate 2+ lần trong 48h
- Tuần release lớn — tạm dừng các loop tự sửa, chỉ để chúng báo cáo

### Pause

- Đang có sự cố production (loop có thể phá hỏng bản hotfix)
- Đang chạy migration đổi schema kiểu breaking
- Người review chính đang nghỉ (OOO) mà auto-merge vẫn bật (đừng làm vậy)

### Kill

- Lỗi S2 lặp đi lặp lại, xem [failure catalog](../06-anti-patterns/README.md#2-failure-mode-catalog)
- Tiền bỏ ra > giá trị thu về suốt 2 tuần liền
- Cả team tắt hết thông báo
- Đã có cách làm theo sự kiện gọn hơn thay thế (VD: chỉ giữ lại CI Action)

**Các bước dẹp loop**:
1. `scheduler_delete` / tắt Automation / gỡ Action
2. Lưu trữ state file với `status: retired`
3. Viết post-mortem trong `stories/` (không bắt buộc nhưng rất nên làm)

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

**Đừng bao giờ bỏ qua L1** khi thử pattern mới trên repo production.

---

*Tiếp theo: [05 — Multi-Loop Coordination](../05-multi-loop/) → [06 — Anti-Patterns & Failure Modes](../06-anti-patterns/)*
