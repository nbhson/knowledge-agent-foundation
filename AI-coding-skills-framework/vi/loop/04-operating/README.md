# 🛠️ 04. Operating Loops trong Production

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Operating nghĩa là "vận hành" — khi loop đã chạy thật ngoài production, việc của bạn chuyển từ thiết kế sang **trông coi và điều tiết**: canh token cost, đọc run log, xem metrics, rồi quyết định lúc nào nên giảm tốc / tạm dừng / dẹp hẳn một loop.
> **Hình dung cho dễ:** Như **ngồi trong buồng lái** — máy bay (loop) đã cất cánh; bạn không cần chui xuống sửa động cơ giữa trời, chỉ cần đọc đồng hồ (metrics), canh nhiên liệu (token budget), và quyết định hạ cánh sớm (kill) khi đèn báo đỏ.
> **Vì sao đáng quan tâm:** Loop đầu tay kiểu gì cũng đốt kha khá token — chuyện đó bình thường. Phần này chỉ bạn **áng chi phí trước khi chạy** (đỡ bất ngờ khi thấy bill), **ghi log để còn biết đường tìm** ("sao nó lại làm vậy?"), và **dừng đúng lúc** trước khi thiệt hại nhỏ thành chuyện lớn.

> Chạy loop thực chất là làm vận hành. Phần này gồm: **ngân sách token (Token Budget)**, **ghi log (Logging)**, **chỉ số (Metrics)**, và **lúc nào nên giảm tốc, tạm dừng hay dẹp bỏ** một loop.

---

## 1. Token & Cost Budgeting

> **Đọc đoạn này thế nào:** Câu hỏi cốt lõi là "**loop này mỗi ngày tốn bao nhiêu tiền?**" — giống như áng tiền xăng trước chuyến đi xa. Bạn dùng `loop cost` để ước lượng, rồi đặt **trần chi tiêu (budget)** và **nút dừng khẩn cấp (kill switch)** phòng khi vượt mức. "Token" = đơn vị tính dữ liệu vào/ra của mô hình, tức đơn vị tính tiền. Nhớ quy tắc: chạy càng dày, đẻ càng nhiều sub-agent thì tiền càng tăng nhanh.

**Ước lượng trước khi schedule:**

> 📄 **Code ví dụ:** [`examples/01-1-token-cost-budgeting.sh`](examples/01-1-token-cost-budgeting.sh)

`loop-audit` chấm điểm khả năng quan sát chi phí, và **giữ loop ở L3** cho tới khi có đủ budget, run log và mục budget trong LOOP.md. Nghĩa là: tool kiểm định này không cho loop chạy tự do (L3 = mức không cần người trông) nếu bạn chưa chốt trần chi phí và nhật ký chạy.

### Các Yếu Tố Ước Lượng

**Cách đọc bảng này**: cột "Yếu tố" = cái gì làm chi phí tăng; cột "Ảnh hưởng" = tăng thế nào. Ví dụ dòng 1: nhịp chạy 5 phút thay vì 1 ngày nghĩa là 288 lần chạy/ngày thay vì 1 — tiền nhân theo đúng tỉ lệ đó.

| Yếu tố | Ảnh hưởng |
|--------|-----------|
| Cadence | Linear multiplier (5m vs 1d = 288× runs/ngày) |
| Sub-agents per run | Mỗi cái = full model + tool round-trips |
| Context size | Repos lớn + full CI logs = triage đắt |
| Verifier model | Model mạnh hơn trên verifier = đáng giá cho unattended |

Glossary: "Cadence" = nhịp chạy; "sub-agent" = agent con do loop triệu gọi, mỗi cái là một lượt trả tiền riêng; "context size" = khối dữ liệu gửi cho model (repo lớn + toàn bộ log CI thì mỗi lượt đắt hơn); "unattended" = chạy không cần người trông.

### Example Estimates (~50k tokens cho light triage run, ~200k cho run với implementer + verifier)

**Cách đọc bảng này**: ước lượng token mỗi ngày theo từng loop. "Light triage" = lượt quét nhẹ; "implementer + verifier" = lượt đầy đủ có agent viết code và agent kiểm code.

| Loop | Cadence | Runs/ngày | Rough daily tokens |
|------|---------|-----------|--------------------|
| Daily triage (report only) | 1d | 1 | ~50k |
| CI sweeper (light) | 15m | 96 | ~5M (nếu full — **tránh**) |
| PR babysitter | 5m | 288 | High — dùng early exit |

Glossary: "CI sweeper" = loop quét lỗi test tự động; "early exit" = thoát sớm khi không có việc, đừng chạy trọn bộ.

> **Mẹo hay**: bạn cứ cho lượt triage chạy thật rẻ; chỉ tạo sub-agent khi state báo có việc đáng làm. Watchlist mà trống thì thoát luôn trong vòng < 5k tokens. "Watchlist" = danh sách việc loop đang theo dõi.

### Budget Rules

**Phần này giải thích**: mẫu file ngân sách. Đây là "hợp đồng chi tiêu" của loop — vượt trần thì phải dừng, và agent không được tự sửa trần.

```markdown
## Loop Budget — Project X
- Max tokens/day: 2M (adjust theo plan)
- On exceed: pause schedulers, notify human
- Max sub-agent spawns per run: 3
```

Cách đọc ví dụ: tối đa 2 triệu token mỗi ngày (tự chỉnh theo gói của bạn); vượt thì tạm dừng mọi bộ hẹn giờ và báo người; mỗi lượt chạy chỉ được triệu gọi tối đa 3 agent con.

Ghi thẳng vào skill hoặc prompt của scheduler: *"If no high-priority items, exit immediately."* — nghĩa là "không có việc ưu tiên cao thì thoát ngay".

> **Tóm gọn 1 câu:** Ước lượng tiền trước khi hẹn giờ, ghi trần chi tiêu vào file ngân sách với nút dừng khẩn, và thoát sớm khi không có việc.

---

## 2. Logging Mỗi Run

> **Đọc đoạn này thế nào:** Log là "**hộp đen**" của loop — mỗi lần chạy ghi lại ngắn gọn: chạy bao lâu, thấy gì, đã làm gì, tốn bao nhiêu. Sau này nếu thắc mắc "sao nó không xử lý vụ X", bạn mở log ra là có câu trả lời. Chuẩn ở đây là **append-only**: chỉ thêm dòng mới, không sửa, không xóa — vì dòng nào sửa được thì dòng đó không đáng tin.

Mỗi run bạn ghi tối thiểu chừng này (lưu vào `loop-run-log.md` hoặc JSON có cấu trúc): thời điểm bắt đầu, kiểu loop, số việc tìm được, số hành động đã làm, số lần đẩy lên người, ước lượng token, và kết quả cuối.

> 📄 **Code ví dụ:** [`examples/02-2-logging-moi-run.json`](examples/02-2-logging-moi-run.json)

Bản ngắn gọn cho người đọc, đặt ở cuối `STATE.md`:

```markdown
---
Run log: 2026-06-09 08:15 | 4 findings | 1 worktree opened | 0 escalations
```

Cách đọc ví dụ: lượt chạy lúc 08:15 tìm thấy 4 việc, mở 1 worktree (bản sao tạm của repo để sửa an toàn), không phải đẩy việc nào lên người.

> **Tóm gọn 1 câu:** Mỗi lần chạy ghi một dòng log chỉ-thêm-không-sửa — đó là hộp đen duy nhất giúp bạn lần ra "sao nó làm vậy".

---

## 3. Metrics Dashboard

> **Đọc đoạn này thế nào:** Metrics là "**sổ theo dõi sức khỏe**" của loop — mỗi tuần bạn mở ra và tự hỏi: loop có thực sự giúp được việc không, hay chỉ tốn tiền và gây nhiễu? Bạn điền số liệu vào bảng dưới (runs, findings, escalations, false positives) cho từng pattern để thấy xu hướng rõ ràng, thay vì đoán theo cảm tính. "Finding" = việc loop phát hiện ra; "escalation" = việc đẩy lên người; "false positive" = báo động giả, cảnh báo sai.

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

Cách đọc bảng: mỗi cột là một loop, mỗi dòng là một chỉ số điền hàng tuần. Nghĩa từng dòng: số lượt chạy; số phát hiện đáng xử lý; số bản fix tự động đề xuất; số lần phải nhờ người; số cảnh báo sai; thời gian trung bình từ khi có việc đến khi người biết; và tiền token đã tiêu (ước lượng).

Chỉ số thành công riêng của từng pattern nằm trong [02-patterns](../02-patterns/).

> **Tóm gọn 1 câu:** Điền bảng số liệu mỗi tuần cho từng loop — nếu báo động giả và chi phí tăng đều thì đó là dấu hiệu giảm tốc, bất kể cảm giác "chắc ổn".

---

## 4. Khi Nào Slow Down / Pause / Kill

> **Đọc đoạn này thế nào:** Đây là "**chân ga — chân phanh**" — 3 mức theo độ nghiêm trọng: **Slow down** (giảm ga vì sắp hết nhiên liệu), **Pause** (tạm dừng vì có chướng ngại ngay trước mặt), **Kill** (dẹp luôn vì con đường này không còn đáng đi). Mỗi lần có sự cố, bạn tự hỏi: mình đang ở mức nào?

### Slow Down

**Phần này giải thích**: lúc nào giảm nhịp nhưng vẫn chạy — loop còn giá trị, chỉ cần thở chậm lại.

- Token budget > 80% giữa tuần — gần cạn xăng mà còn giữa đường.
- False positive rate > 30% trên triage — báo động giả quá nhiều, hạ thông báo xuống trước khi cả team tắt hết.
- Cùng một item bị escalate 2+ lần trong 48h — một việc phải nhờ người hoài nghĩa là loop không xử lý được nó.
- Tuần release lớn — tạm dừng các loop tự sửa, chỉ để chúng báo cáo — "release" = tung bản mới ra người dùng; tuần nhạy cảm thì đừng cho máy tự tay vào code.

### Pause

**Phần này giải thích**: lúc nào dừng tạm — có chướng ngại cụ thể ngay trước mặt, qua khỏi thì bật lại.

- Đang có sự cố production (loop có thể phá hỏng bản hotfix) — "hotfix" = bản vá gấp; loop tự sửa trong lúc đang vá gấp là kẻ phá đám.
- Đang chạy migration đổi schema kiểu breaking — "migration" = script đổi cấu trúc database; "breaking" = kiểu làm bản cũ không đọc được dữ liệu mới.
- Người review chính đang nghỉ (OOO) mà auto-merge vẫn bật (đừng làm vậy) — "OOO" = out of office, đi vắng; không có người duyệt thì đừng bật tự gộp.

### Kill

**Phần này giải thích**: lúc nào dẹp hẳn loop — đây là quyết định về giá trị, không phải về sự cố.

- Lỗi S2 lặp đi lặp lại, xem [failure catalog](../06-anti-patterns/README.md#2-failure-mode-catalog) — "S2" = mức nghiêm trọng "có hại" (code sai có thể lọt vào nhánh chính).
- Tiền bỏ ra > giá trị thu về suốt 2 tuần liền — hai tuần liên tục lỗ thì không hy vọng tháng sau tự lãi.
- Cả team tắt hết thông báo — loop không ai nghe nữa thì chạy cũng như không.
- Đã có cách làm theo sự kiện gọn hơn thay thế (VD: chỉ giữ lại CI Action) — "theo sự kiện" = chạy khi có việc xảy ra thay vì chạy lịch đều đều.

**Các bước dẹp loop**:
1. `scheduler_delete` / tắt Automation / gỡ Action — xoá lịch chạy để không còn lần nào nữa.
2. Lưu trữ state file với `status: retired` — "retired" = đã nghỉ hưu; giữ file để sau này tra lại.
3. Viết post-mortem trong `stories/` (không bắt buộc nhưng rất nên làm) — "post-mortem" = báo cáo rút kinh nghiệm sau sự cố.

> **Tóm gọn 1 câu:** Ba mức can thiệp: giảm tốc khi sắp cạn nguồn lực, tạm dừng khi có nguy hiểm trước mắt, dẹp hẳn khi loop không còn đáng tiền.

---

## 5. Upgrade Path

**Phần này giải thích**: lộ trình nâng loop lên từng bậc tự chủ, mỗi bậc chỉ lên khi bậc dưới đã có bằng chứng hoạt động tốt. L0 = bản nháp, L1 = chỉ báo cáo, L2 = tự sửa nhỏ có kiểm chứng, L3 = chạy tự do.

```
Report-only (L1) → 1–2 tuần triage ổn định
       ↓
Small auto-wins (L2) → verifier + worktree + max attempts
       ↓
Connectors (L2+) → PRs/tickets tự cập nhật
       ↓
Unattended (L3) → chỉ khi có denylist, budget, metrics, human gates
```

Cách đọc sơ đồ: đi từ trên xuống; bên phải mỗi bậc là điều kiện bắt buộc trước khi lên tiếp. Glossary: "triage" = quét và phân loại việc; "verifier" = agent riêng kiểm chứng bản sửa; "worktree" = bản sao tạm của repo; "max attempts" = giới hạn số lần thử; "connector" = điểm nối ra hệ thống ngoài (GitHub, Linear...); "denylist" = danh sách file cấm đụng; "human gates" = các điểm bắt buộc người duyệt.

**Đừng bao giờ bỏ qua L1** khi thử pattern mới trên repo production — bậc chỉ-báo-cáo là chỗ bạn đo nhiễu và rủi ro mà không tốn gì nhiều.

> **Tóm gọn 1 câu:** Nâng loop từng bậc L1→L3, mỗi bậc cần bằng chứng thực tế từ bậc dưới — đi tắt nghĩa là tin một hệ thống chưa từng chạy ở mức đó.

---

*Tiếp theo: [05 — Multi-Loop Coordination](../05-multi-loop/) → [06 — Anti-Patterns & Failure Modes](../06-anti-patterns/)*
