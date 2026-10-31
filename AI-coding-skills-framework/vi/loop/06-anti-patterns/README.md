# ⚠️ 06. Anti-Patterns & Failure Modes

> Những lỗi thiết kế bạn nên tránh **trước khi** bật loops unattended, cùng **catalog các kiểu hỏng mà loops hay gặp** và cách giảm thiểu.
>
> Giải nghĩa nhanh: **loop unattended** = loop chạy không có người canh; **anti-pattern** = kiểu làm nghe hợp lý nhưng kinh nghiệm cho thấy hay hỏng; **failure mode** = kiểu hỏng cụ thể ngoài đời; **mitigation** = cách giảm thiểu hậu quả; **state** = file ghi lại loop đã làm gì để lần sau nhớ.

---

## 1. Anti-Patterns (Sai Lầm Thiết Kế)

Phần này liệt kê 10 sai lầm thiết kế phổ biến khi dựng loop. Cách đọc bảng này: cột "Tại sao hỏng" nêu hậu quả; cột "Làm thay" nêu cách làm đúng. Ví dụ, #1 là để cùng một agent vừa làm việc vừa tự chấm bài — nó sẽ tự biện hộ cho mình.

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

Giải nghĩa các từ trong bảng: **confirmation bias** = thiên kiến xác nhận (tin kết quả của chính mình); **rubber-stamp** = duyệt cho có; **verifier** = bước chuyên kiểm code; **escalate** = dừng tự động, chuyển người; **triage** = xếp hạng việc theo ưu tiên; **parse** = đọc hiểu theo cấu trúc; **L1/L2/L3** = chỉ báo cáo / sửa có người duyệt / tự chạy; **state rot** = state chứa tin cũ sai; **prune** = cắt mục đã xong; **blast radius** = phạm vi hư hại nếu sai; **connector** = cầu nối Slack/Linear; **kill switch** = nút dừng khẩn; **alert fatigue** = báo nhiều quá nên bị tắt tiếng; **flake** = test chập chờn lúc pass lúc fail; **quarantine** = cách ly khỏi luồng chính; **allowlist/denylist** = danh sách được phép / danh sách cấm; **run log** = nhật ký mỗi lần chạy.

> **Tóm gọn 1 câu:** Đừng để một agent tự làm rồi tự duyệt, đừng để loop chạy vô hạn hay đụng file cấm — tách người kiểm, đặt trần số lần thử, giới hạn vùng được đụng, và luôn có log với nút dừng.

---

## 2. Failure Mode Catalog

Phần này giải thích 10 kiểu hỏng có thật ngoài đời. Bạn dùng nó khi debug một loop đang chạy sai, hoặc khi viết pattern mới để biết phải phòng gì. Mỗi mục nêu: triệu chứng (symptom), mức nguy (severity), nguyên nhân (causes), cách phòng (mitigations).

### Phân Loại Severity

Cách đọc bảng này: mỗi kiểu hỏng bên dưới được gán một mức S1/S2/S3. Ví dụ, S3 là mức phải xử lý ngay vì mất dữ liệu hoặc lộ bảo mật.

| Severity | Nghĩa |
|----------|-------|
| **S1 — Annoying** | Lãng phí time/tokens, không gây hại |
| **S2 — Harmful** | Wrong code merged, bad tickets, alert fatigue |
| **S3 — Critical** | Security, data loss, production incident |

> **Tóm gọn 1 câu:** S1 chỉ phiền (đốt tiền, đốt thời gian), S2 gây hại thật (code sai vào repo), S3 là thảm họa (bảo mật, mất dữ liệu, sự cố production) — độ nguy càng cao thì human gate phải càng chặt.

---

### 2.1 Infinite Fix Loop

- **Symptom**: Cùng một PR/CI job bị auto-fix 5+ lần mà vẫn không xong.
- **Severity**: S2
- **Causes**: Verifier yếu hoặc cùng session với implementer; chẩn đoán sai nguyên nhân gốc (chỉ chữa triệu chứng); test chập chờn bị xem là regression (lỗi mới sau một thay đổi).
- **Mitigations**: Đặt hard cap attempts (ví dụ 3) rồi escalate; tách verifier ra model/effort riêng; phân loại flakes; ghi attempt count vào state.

> **Tóm gọn 1 câu:** Loop sửa mãi không xong vì người kiểm yếu hoặc chẩn đoán sai gốc rễ; chặn bằng trần cứng 3 lần thử, tách verifier riêng, và chuyển người khi chạm trần.

### 2.2 State Rot

- **Symptom**: `STATE.md` vẫn nhắc tới PR đã merge (đã gộp vào nhánh chính), ticket đã đóng, branch đã cũ.
- **Severity**: S1 → S2 (loop hành động dựa trên "bóng ma")
- **Causes**: Không có bước prune cuối mỗi run; state không được đọc đầu run; nhiều loop cùng ghi vào một file mà không có schema (khuôn dạng cố định).
- **Mitigations**: Prune các item đã closed/merged mỗi run; ghi `Last run` timestamp và kiểm tra lại IDs; mỗi pattern một state file riêng.

> **Tóm gọn 1 câu:** State cũ không được dọn thì loop làm việc theo "bóng ma" của những việc đã xong; cắt mục đã xong mỗi run và mỗi pattern một file state riêng.

### 2.3 Verifier Theater

- **Symptom**: Verifier bấm "approve" nhưng tests vẫn fail ngoài CI hoặc review vẫn thấy bug.
- **Severity**: S2
- **Causes**: Prompt của verifier chung chung ("looks good"); verifier không chạy tests; dùng cùng model, cùng context với implementer.
- **Mitigations**: Verifier phải chạy test/lint (công cụ soi lỗi chuẩn viết code) và báo cáo output; instructions khác đi ("tìm lý do để reject"); dùng model mạnh hơn cho unattended.

> **Tóm gọn 1 câu:** Verifier duyệt cho có vì không chạy test và dùng cùng bộ não với người viết; bắt nó chạy test, báo output thật, và mặc định tìm lý do để từ chối.

### 2.4 Notification Fatigue

- **Symptom**: Slack/email ping (báo tin) mỗi 5 phút; cả team tắt tiếng bot.
- **Severity**: S1 → S2 (các escalation thật bị bỏ lỡ)
- **Causes**: Cứ mỗi run là notify, thay vì chỉ notify khi có finding *đáng làm*; ngưỡng "high priority" đặt quá thấp.
- **Mitigations**: Chỉ notify khi cần người ra quyết định; dùng digest mode (gom thành một tin tổng mỗi ngày) cho report-only loops; siết lại triage rules.

> **Tóm gọn 1 câu:** Báo mỗi run là cả team tắt tiếng và lỡ báo thật; chỉ báo khi cần người quyết, còn lại gom thành tin tổng.

### 2.5 Token Burn

- **Symptom**: Bill tăng vọt; loop chạy full chuỗi sub-agent (agent nhỏ được agent chính gọi ra) dù triage trống hoặc toàn nhiễu.
- **Severity**: S1
- **Causes**: Cadence (nhịp chạy) dày dưới từng phút mà sub-agents nặng; không early-exit (thoát sớm) khi watchlist rỗng; retry cả pipeline dù chỉ lỗi API nhất thời.
- **Mitigations**: Chạy lượt triage-only rẻ tiền trước; `scheduler_delete` khi hết việc; đặt daily token budget để tự pause loop.

> **Tóm gọn 1 câu:** Nhịp chạy dày cộng chuỗi agent nặng là bill tăng vọt; chạy lượt rà rẻ trước, thoát sớm khi rỗng việc, và đặt hạn mức token theo ngày.

### 2.6 Over-Reach (Wrong Scope)

- **Symptom**: Loop refactor (viết lại cho gọn mà không đổi hành vi) các module không liên quan, "fix" cả design issue, chạm vào denylist paths.
- **Severity**: S2 → S3
- **Causes**: minimal-fix skill (kiểu "sửa nhỏ nhất có thể") cho phép quá rộng; không có path allowlist/denylist; triage xếp architectural work vào "High Priority".
- **Mitigations**: Siết denylist ngay trong skills; giữ nguyên tắc "diff (phần code thay đổi) nhỏ nhất có thể" và verifier kiểm tra touched files; triage chỉ phát tín hiệu.

> **Tóm gọn 1 câu:** Loop tay dài vào việc khác khi không có danh sách cấm và không ai bắt nó giữ diff nhỏ; chặn bằng denylist trong skill và bắt verifier kiểm từng file bị đụng.

### 2.7 Comprehension Debt Spiral

- **Symptom**: Tốc độ tăng nhưng không ai giải thích được các change gần đây; review thành gật cho qua.
- **Severity**: S2 (dài hạn)
- **Causes**: Mọi người ngừng đọc output của loop; auto-merge (gộp code không cần người duyệt) allowlist phình to; thiếu tổng hợp hàng tuần từ con người.
- **Mitigations**: Bắt buộc review bởi người với PR non-trivial (không phải việc vụn vặt); duy trì "loop digest" hàng tuần; chỉ auto-merge các path thật sự vụn vặt.

> **Tóm gọn 1 câu:** Khi không ai đọc output của loop nữa, code to lên mà hiểu biết thì không — bắt người review PR quan trọng và tổng hợp lại mỗi tuần.

### 2.8 Cognitive Surrender

- **Symptom**: "Loop lo hết rồi" — không còn ai có ý kiến về correctness (tính đúng đắn) và design.
- **Severity**: S2 (văn hóa)
- **Causes**: Đo thành công của loop bằng số lượng thay vì chất lượng; thiếu human gates (điểm bắt buộc có người duyệt) cho medium-risk work.
- **Mitigations**: Ghi human gates rõ ràng trong mọi pattern; đo thành công bằng time saved *kèm* quality bar (chuẩn chất lượng tối thiểu); như Osmani nói: "Build it like someone who intends to stay the engineer".

> **Tóm gọn 1 câu:** Đo loop bằng số lượng và bỏ hết cổng duyệt người là bạn thôi làm kỹ sư; đo bằng thời gian tiết kiệm kèm chuẩn chất lượng, và giữ cổng duyệt cho việc rủi ro vừa.

### 2.9 Parallel Collision

- **Symptom**: Hai sub-agent sửa cùng files; merge conflicts (git không biết giữ bản của ai); state hỏng.
- **Severity**: S2
- **Causes**: Không cô lập bằng worktree (bản sao riêng của repo để sửa không đụng code chính); hai loop cùng action trên một PR mà không phối hợp.
- **Mitigations**: Dùng `isolation: worktree` cho mọi sub-agent sửa code; khóa/hàng đợi trong state: "PR #1234 — worktree in progress".

> **Tóm gọn 1 câu:** Hai agent sửa cùng chỗ cùng lúc là đè code của nhau; mỗi agent một worktree riêng và ghi khóa "đang có người làm" vào state.

### 2.10 Escalation Failure

- **Symptom**: Loop kẹt ở retrying (thử đi thử lại) mãi; không ai được báo.
- **Severity**: S2
- **Causes**: Max attempts không được cài thật; escalation chỉ ghi vào state mà chẳng ai đọc.
- **Mitigations**: Ping qua connector khi escalate (Slack, Linear comment); giữ mục `High Priority (waiting on human)` trong STATE.md; báo động nếu item nằm đó quá 24h.

> **Tóm gọn 1 câu:** Ghi escalation vào state mà không ai đọc thì loop kẹt mãi trong im lặng; ping thẳng Slack/Linear và báo động nếu việc chờ người quá 24 giờ.

---

*Tiếp theo: [07 — Tools & Ecosystem](../07-tools/) → [README](../README.md)*
