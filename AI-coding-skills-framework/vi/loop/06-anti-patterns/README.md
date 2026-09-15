# ⚠️ 06. Anti-Patterns & Failure Modes

> Các sai lầm thiết kế cần tránh **trước khi** bật loops unattended, và **catalog các cách thực sự loops hỏng** kèm cách giảm thiểu.

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

Real ways loops fail — dùng khi debug một loop misbehaving hoặc viết pattern mới.

### Phân Loại Severity

| Severity | Nghĩa |
|----------|-------|
| **S1 — Annoying** | Lãng phí time/tokens, không gây hại |
| **S2 — Harmful** | Wrong code merged, bad tickets, alert fatigue |
| **S3 — Critical** | Security, data loss, production incident |

---

### 2.1 Infinite Fix Loop

- **Symptom**: Cùng PR/CI job bị auto-fix 5+ lần; không bao giờ hội tụ.
- **Severity**: S2
- **Causes**: Verifier yếu hoặc cùng session với implementer; root cause misdiagnosed (symptom fixing); flaky test bị xem là regression.
- **Mitigations**: Hard cap attempts (vd 3) → escalate; tách verifier model/effort; classify flakes; ghi attempt count trong state.

### 2.2 State Rot

- **Symptom**: `STATE.md` tham chiếu PRs merged, tickets đóng, branches stale.
- **Severity**: S1 → S2 (loop act trên ghosts)
- **Causes**: Không có prune step cuối run; state không được đọc đầu run; nhiều loops ghi cùng file không schema.
- **Mitigations**: Prune closed/merged items mỗi run; `Last run` timestamp + validate IDs; một state file mỗi pattern.

### 2.3 Verifier Theater

- **Symptom**: Verifier "approve" nhưng tests fail trong CI hoặc review thấy bugs.
- **Severity**: S2
- **Causes**: Verifier prompt mơ hồ ("looks good"); verifier không chạy tests; cùng model, cùng context với implementer.
- **Mitigations**: Verifier phải chạy test/lint và report output; khác instructions ("find reasons to reject"); model mạnh hơn cho unattended.

### 2.4 Notification Fatigue

- **Symptom**: Slack/email ping mỗi 5 phút; team mute bot.
- **Severity**: S1 → S2 (escalations thật bị bỏ lỡ)
- **Causes**: Notify trên mọi run, không phải mọi *actionable* finding; ngưỡng "high priority" quá thấp.
- **Mitigations**: Chỉ notify khi cần human decision; digest mode cho report-only loops; tighten triage rules.

### 2.5 Token Burn

- **Symptom**: Bill tăng vọt; loop chạy full sub-agent chains trên triage rỗng/nhiễu.
- **Severity**: S1
- **Causes**: Cadence dưới phút với sub-agents nặng; không early-exit khi watchlist rỗng; retry cả pipeline trên transient API errors.
- **Mitigations**: Cheaper triage-only pass trước; `scheduler_delete` khi hết việc; daily token budget → pause loop.

### 2.6 Over-Reach (Wrong Scope)

- **Symptom**: Loop refactor modules không liên quan, "fix" design issues, chạm denylist paths.
- **Severity**: S2 → S3
- **Causes**: minimal-fix skill quá permissive; không có path allowlist/denylist; triage xếp architectural work vào "High Priority".
- **Mitigations**: Denylist enforced trong skills; "smallest possible diff" + verifier kiểm tra touched files; triage signal-only.

### 2.7 Comprehension Debt Spiral

- **Symptom**: Velocity tăng nhưng không ai giải thích được recent changes; review thành rubber-stamp.
- **Severity**: S2 (dài hạn)
- **Causes**: Human ngừng đọc loop output; auto-merge trên allowlist phình to; không có human synthesis hàng tuần.
- **Mitigations**: Mandatory human review cho non-trivial PRs; weekly "loop digest"; cap auto-merge cho truly trivial paths.

### 2.8 Cognitive Surrender

- **Symptom**: "The loop handles it" — không có ý kiến về correctness/design.
- **Severity**: S2 (cultural)
- **Causes**: Loop success metric = volume, không phải quality; không human gates trên medium-risk work.
- **Mitigations**: Human gates tường minh trong mọi pattern; success metric = time saved *with* quality bar; Osmani: "Build it like someone who intends to stay the engineer".

### 2.9 Parallel Collision

- **Symptom**: Hai sub-agents sửa cùng files; merge conflicts; corrupted state.
- **Severity**: S2
- **Causes**: Không worktree isolation; hai loops action trên cùng PR không phối hợp.
- **Mitigations**: `isolation: worktree` cho mọi code-editing sub-agents; lock/queue trong state: "PR #1234 — worktree in progress".

### 2.10 Escalation Failure

- **Symptom**: Loop kẹt retrying; human không bao giờ được báo.
- **Severity**: S2
- **Causes**: Max attempts không được implement; escalation chỉ ghi vào state không ai đọc.
- **Mitigations**: Connector ping khi escalate (Slack, Linear comment); `High Priority (waiting on human)` section trong STATE.md; alert nếu item trong section đó > 24h.

---

*Tiếp theo: [07 — Tools & Ecosystem](../07-tools/) → [README](../README.md)*
