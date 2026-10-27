# ⚠️ 06. Anti-Patterns & Failure Modes

> Những lỗi thiết kế bạn nên tránh **trước khi** bật loops unattended, cùng **catalog các kiểu hỏng mà loops hay gặp** và cách giảm thiểu.

---

## 1. Anti-Patterns (Sai Lầm Thiết Kế)

| # | Anti-Pattern | Tại sao hỏng | Làm thay |
|---|--------------|--------------|----------|
| 1 | **Same agent implements AND verifies** | Confirmation bias; tests yếu bị rubber-stamp | Tách verifier sub-agent/model; stance mặc định REJECT |
| 2 | **No attempt cap** | "Cứ thử cho đến khi CI xanh" → infinite fix loops, token burn | Hard cap (vd 3) → escalate với full context trong state |
| 3 | **Vague triage output** | Loop không parse được priorities; humans bỏ qua STATE.md | Structured markdown, one-line items, explicit `Suggested loop action` |
| 4 | **L3 before L1 quality** | Loop act trên bad signal; comprehension debt bùng nổ | L1 report-only tuần một; đo triage accuracy trước khi bật L2 |
| 5 | **Shared state without schema** | Ba loops append vào một STATE.md unstructured → state rot, xung đột | Một state file mỗi pattern, hoặc sections tách rõ với prune rules |
| 6 | **MCP with write-everything scope** | Blast radius của một bad triage decision quá lớn | L1 read-only connectors; mở rộng scope sau khi earned trust |
| 7 | **No kill switch** | Loop chạy 24/7 không có pause criteria → alert fatigue, budget overrun | Document pause/kill trong LOOP.md + budget template |
| 8 | **Fixing flakes with code** | Mặt nạ infra problems; random diffs | Classify → quarantine/retry policy → escalate env/infra |
| 9 | **Auto-merge without allowlist** | Security + business-logic bugs qua weak verifiers | Path allowlist tường minh; human merge cho denylist paths |
| 10 | **No run log** | Chỉ STATE.md, không history → không debug được | Append `loop-run-log.md` mỗi run |

---

## 2. Failure Mode Catalog

Đây là những kiểu hỏng có thật ngoài đời — bạn dùng khi debug một loop đang chạy sai hoặc khi viết pattern mới.

### Phân Loại Severity

| Severity | Nghĩa |
|----------|-------|
| **S1 — Annoying** | Lãng phí time/tokens, không gây hại |
| **S2 — Harmful** | Wrong code merged, bad tickets, alert fatigue |
| **S3 — Critical** | Security, data loss, production incident |

---

### 2.1 Infinite Fix Loop

- **Symptom**: Cùng một PR/CI job bị auto-fix 5+ lần mà vẫn không xong.
- **Severity**: S2
- **Causes**: Verifier yếu hoặc cùng session với implementer; chẩn đoán sai nguyên nhân gốc (chỉ chữa triệu chứng); test chập chờn bị xem là regression.
- **Mitigations**: Đặt hard cap attempts (ví dụ 3) rồi escalate; tách verifier ra model/effort riêng; phân loại flakes; ghi attempt count vào state.

### 2.2 State Rot

- **Symptom**: `STATE.md` vẫn nhắc tới PR đã merge, ticket đã đóng, branch đã cũ.
- **Severity**: S1 → S2 (loop hành động dựa trên "bóng ma")
- **Causes**: Không có bước prune cuối mỗi run; state không được đọc đầu run; nhiều loop cùng ghi vào một file mà không có schema.
- **Mitigations**: Prune các item đã closed/merged mỗi run; ghi `Last run` timestamp và kiểm tra lại IDs; mỗi pattern một state file riêng.

### 2.3 Verifier Theater

- **Symptom**: Verifier bấm "approve" nhưng tests vẫn fail ngoài CI hoặc review vẫn thấy bug.
- **Severity**: S2
- **Causes**: Prompt của verifier chung chung ("looks good"); verifier không chạy tests; dùng cùng model, cùng context với implementer.
- **Mitigations**: Verifier phải chạy test/lint và báo cáo output; instructions khác đi ("tìm lý do để reject"); dùng model mạnh hơn cho unattended.

### 2.4 Notification Fatigue

- **Symptom**: Slack/email ping mỗi 5 phút; cả team tắt tiếng bot.
- **Severity**: S1 → S2 (các escalation thật bị bỏ lỡ)
- **Causes**: Cứ mỗi run là notify, thay vì chỉ notify khi có finding *đáng làm*; ngưỡng "high priority" đặt quá thấp.
- **Mitigations**: Chỉ notify khi cần người ra quyết định; dùng digest mode cho report-only loops; siết lại triage rules.

### 2.5 Token Burn

- **Symptom**: Bill tăng vọt; loop chạy full chuỗi sub-agent dù triage trống hoặc toàn nhiễu.
- **Severity**: S1
- **Causes**: Cadence dày dưới từng phút mà sub-agents nặng; không early-exit khi watchlist rỗng; retry cả pipeline dù chỉ lỗi API nhất thời.
- **Mitigations**: Chạy lượt triage-only rẻ trước; `scheduler_delete` khi hết việc; đặt daily token budget để tự pause loop.

### 2.6 Over-Reach (Wrong Scope)

- **Symptom**: Loop refactor các module không liên quan, "fix" cả design issue, chạm vào denylist paths.
- **Severity**: S2 → S3
- **Causes**: minimal-fix skill cho phép quá rộng; không có path allowlist/denylist; triage xếp architectural work vào "High Priority".
- **Mitigations**: Siết denylist ngay trong skills; giữ nguyên tắc "diff nhỏ nhất có thể" và verifier kiểm tra touched files; triage chỉ phát tín hiệu.

### 2.7 Comprehension Debt Spiral

- **Symptom**: Tốc độ tăng nhưng không ai giải thích được các change gần đây; review thành gật cho qua.
- **Severity**: S2 (dài hạn)
- **Causes**: Mọi người ngừng đọc output của loop; auto-merge allowlist phình to; thiếu tổng hợp hàng tuần từ con người.
- **Mitigations**: Bắt buộc review bởi người với PR non-trivial; duy trì "loop digest" hàng tuần; chỉ auto-merge các path thật sự vụn vặt.

### 2.8 Cognitive Surrender

- **Symptom**: "Loop lo hết rồi" — không còn ai có ý kiến về correctness/design.
- **Severity**: S2 (văn hóa)
- **Causes**: Đo thành công của loop bằng số lượng thay vì chất lượng; thiếu human gates cho medium-risk work.
- **Mitigations**: Ghi human gates rõ ràng trong mọi pattern; đo thành công bằng time saved *kèm* quality bar; như Osmani nói: "Build it like someone who intends to stay the engineer".

### 2.9 Parallel Collision

- **Symptom**: Hai sub-agent sửa cùng files; merge conflicts; state hỏng.
- **Severity**: S2
- **Causes**: Không cô lập bằng worktree; hai loop cùng action trên một PR mà không phối hợp.
- **Mitigations**: Dùng `isolation: worktree` cho mọi sub-agent sửa code; khóa/hàng đợi trong state: "PR #1234 — worktree in progress".

### 2.10 Escalation Failure

- **Symptom**: Loop kẹt ở retrying mãi; không ai được báo.
- **Severity**: S2
- **Causes**: Max attempts không được cài thật; escalation chỉ ghi vào state mà chẳng ai đọc.
- **Mitigations**: Ping qua connector khi escalate (Slack, Linear comment); giữ mục `High Priority (waiting on human)` trong STATE.md; báo động nếu item nằm đó quá 24h.

---

*Tiếp theo: [07 — Tools & Ecosystem](../07-tools/) → [README](../README.md)*
