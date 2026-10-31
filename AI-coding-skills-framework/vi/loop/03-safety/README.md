# 🛡️ 03. Safety & Loop Design Checklist

> Loop giúp khả năng phán đoán của bạn lan rộng ra — cả điểm tốt lẫn điểm chưa tốt. Phần này gồm hai thứ: **Loop Design Checklist** (bảng chấm điểm xem loop đã đủ cứng để lên production chưa) và **Safety & Guardrails** (mức an toàn tối thiểu cho loop production có đụng tới code hay hệ thống bên ngoài).

**Đọc mở đầu thế nào**: "Production" = môi trường chạy thật, có người dùng thật. "Guardrails" = lan can an toàn — các rào chắn không cho loop làm chuyện nguy hiểm. Mục 1 là bảng chấm điểm trước khi chạy thật; mục 2 là các rào chắn bắt buộc.

---

## 1. Loop Design Checklist

**Phần này giải thích**: cách chấm điểm một loop theo 10 hạng mục trước khi cho chạy thật. Mỗi dòng checkbox là một câu hỏi "loop của bạn đã có thứ này chưa".

Bạn cứ chấm điểm **thật lòng** trước khi cho loop chạy production. Loop nào còn thiếu khâu kiểm chứng thì chưa đủ điều kiện chạy mà không có người trông.

### §1 Purpose & Scope

**Phần này giải thích**: loop làm gì và chỉ làm trong phạm vi nào. "Scope" = phạm vi.

- [ ] **Mục tiêu duy nhất rõ ràng** — một câu: loop này hoàn thành điều gì? Một loop chỉ nên làm một việc.
- [ ] **Non-goals tường minh** — loop này sẽ *không* làm gì? "Non-goals" = danh sách việc ngoài phạm vi, ghi rõ để loop không lan man.
- [ ] **Watched scope** — repos, branches, PRs, tickets nào? "Watched" = những gì loop được phép theo dõi và động vào.
- [ ] **Phased rollout** — report-only trước, rồi act? "Phased rollout" = ra mắt theo nấc: chỉ báo cáo trước, có bằng chứng an toàn rồi mới cho tự hành động.
- [ ] **Ambiguous input handled** — khi work item quá mơ hồ để verify "done", loop clarify hoặc escalate thay vì đoán (scaffold `loop-intake` skill). "Clarify" = hỏi lại; "escalate" = đẩy lên người; "work item" = một việc trong danh sách (issue, ticket).

### §2 Scheduling

**Phần này giải thích**: loop chạy với nhịp nào và có sống sót khi hệ thống khởi động lại hay không.

- [ ] **Cadence đã chọn** — interval khớp urgency? "Cadence" = nhịp chạy; "interval" = khoảng cách giữa hai lần chạy; "urgency" = độ gấp của việc.
- [ ] **Fire immediately** — chạy lần đầu ngay hay chờ interval? Nếu chờ 1 ngày mới chạy đầu tiên thì bạn đợi hơi lâu.
- [ ] **Durable** — sống sót restart? "Restart" = máy hoặc service khởi động lại; lịch chạy không được biến mất sau restart.
- [ ] **Off-hours behavior** — cadence chậm hơn hoặc pause qua đêm? Đêm không ai nhìn, chạy dày chỉ tốn tiền.
- [ ] **Self-cleanup** — `scheduler_delete` khi watchlist rỗng? "Watchlist" = danh sách việc loop đang theo dõi; hết việc thì tự xoá lịch chạy, đừng chạy rỗng cho có.

### §3 Skills

**Phần này giải thích**: các "skill" (bộ chỉ thị đóng gói cho agent) cần đạt chuẩn gì.

- [ ] **Triage skill** tồn tại với output format chặt chẽ — skill quét việc phải trả kết quả theo mẫu cố định, không văn xuôi tự do.
- [ ] **Action skills** (minimal-fix...) khớp quy ước dự án — skill sửa code phải tuân theo cách build/test của repo này.
- [ ] **Skill descriptions** boring + specific (auto-triggering tốt) — mô tả skill càng nhạt nhẽo, cụ thể thì hệ thống càng kích hoạt đúng lúc. "Auto-triggering" = tự động chọn skill phù hợp.
- [ ] **Build/test commands** được ghi trong skills / AGENTS.md — agent phải biết lệnh build/test chính xác, đừng đoán.

### §4 Maker / Checker Split

**Phần này giải thích**: người viết code và người kiểm code phải là hai thực thể khác nhau — đây là chốt chặn quan trọng nhất.

- [ ] **Implementer** và **verifier** là hai thực thể tách biệt (agent, model, hoặc instructions) — "implementer" = agent viết code; "verifier" = agent kiểm code; tách biệt để người viết không tự duyệt mình.
- [ ] Implementer **không thể** tự đánh dấu work của mình "done" — chỉ verifier mới có quyền chốt.
- [ ] Verifier chạy **tests** trong cô lập (worktree) trước khi approve — "worktree" = bản sao tạm của repo, test hỏng cũng không ảnh hưởng bản chính.
- [ ] `/goal` hoặc tương đương dùng **fresh model** cho stop condition — "fresh model" = một lượt gọi mô hình mới, không mang ngữ cảnh của người viết, để chấm "đã xong chưa" khách quan.

### §5 State / Memory

**Phần này giải thích**: file trí nhớ của loop. "State" = trạng thái lưu giữa các lần chạy.

- [ ] **State file** hoặc board schema được tài liệu hoá — "schema" = cấu trúc cố định của dữ liệu; ai đọc cũng hiểu được.
- [ ] Loop **đọc** state cũ ở đầu mỗi run — không đọc là loop quên sạch lần trước.
- [ ] Loop **ghi** outcomes, timestamps, last actions — "outcomes" = kết quả; "timestamps" = mốc thời gian.
- [ ] **Prune** resolved/merged/closed items mỗi run — "prune" = dọn bỏ việc đã xong, tránh state phình to và còn "việc bóng" (đã merge rồi mà vẫn nằm trong danh sách).
- [ ] Human overrides được ghi trong state — "overrides" = quyết định đè lên đề xuất của loop; ghi lại để loop không hỏi lại.

### §6 Human Handoff

**Phần này giải thích**: lúc nào và cách loop giao việc cho người.

- [ ] **Escalation triggers** tường minh (max attempts, risk paths, ambiguity) — "escalation triggers" = điều kiện bắt buộc đẩy việc lên người: thử quá số lần, đụng đường rủi ro, việc mơ hồ.
- [ ] **Denylist paths** — auth, payments, secrets, infra — "denylist" = danh sách file cấm đụng: đăng nhập, thanh toán, mật khẩu, hạ tầng.
- [ ] **Notification rule** — chỉ ping human khi cần hành động — ping vô ích làm người ta tắt hết thông báo.
- [ ] **Inbox** — nơi items mơ hồ đáp xuống — "inbox" = hộp thư chờ người xử lý.

### §7 Connectors (MCP)

**Phần này giải thích**: quyền của bot nối ra hệ thống ngoài. "MCP" = giao thức chuẩn để agent gọi các hệ thống ngoài; "connector" = từng điểm nối (GitHub, Slack...).

- [ ] Permissions tối thiểu (read vs write) — cấp đúng ít quyền nhất đủ để làm việc, không hơn.
- [ ] Loop có thể **mở/cập nhật PRs** hoặc tickets nếu đang act — nhưng nhớ: mở PR là được, tự merge thì không.
- [ ] Bot identity rõ ràng trên PR comments (VD: "Loop Engineering — PR Babysitter") — người đọc phải phân biệt được bình luận của máy với của người.

### §8 Cost & Limits

**Phần này giải thích**: chốt trần chi phí và nút dừng. "Token" = đơn vị tính dữ liệu của mô hình, tức đơn vị tính tiền.

- [ ] **Token budget** được ước tính — biết trước mỗi ngày đốt bao nhiêu.
- [ ] **`loop-budget.md`** với daily caps + kill switch — "daily cap" = trần token mỗi ngày; "kill switch" = nút tắt ngay mọi loop.
- [ ] **`loop-run-log.md`** cho append-only run history — "append-only" = chỉ thêm dòng mới, không sửa không xóa; sửa được thì log không đáng tin.
- [ ] **`loop-budget` skill** kiểm tra spend đầu/cuối mỗi run — "spend" = tiền đã tiêu.
- [ ] **Max iterations** mỗi item mỗi run — "iteration" = lần lặp; một việc bị lặp quá số lần thì dừng.
- [ ] **Max auto-PRs** mỗi ngày (cleanup loops) — giới hạn số PR loop tự tạo, tránh spam.
- [ ] **Pause/kill criteria** được định nghĩa — "criteria" = tiêu chí rõ ràng cho việc tạm dừng hoặc dẹp loop.

### §9 Observability

**Phần này giải thích**: khả năng nhìn thấy loop đang làm gì mà không phải phỏng đoán.

- [ ] Log mỗi run: started, items found, actions taken, escalations — mỗi lần chạy ghi lại: bắt đầu lúc nào, thấy gì, làm gì, đẩy gì lên người.
- [ ] **Success metrics** đã chọn — số liệu biết loop có ích hay chỉ đốt tiền.
- [ ] Team có thể **inspect state file** mà không cần đọc chat logs — "inspect" = mở ra xem trực tiếp; state file là nguồn sự thật, không phải đoạn chat.

### §10 Safety

**Phần này giải thích**: ba rào chắn cuối cùng trước khi loop chạy thật.

- [ ] Không auto-merge nếu không có allowlist tường minh — "allowlist" = danh sách trắng, chỉ những loại thay đổi liệt kê rõ mới được gộp tự động.
- [ ] Secrets/env files trong denylist — "secrets" = mật khẩu, khoá API; file `.env` chứa chúng.
- [ ] Flake handling — không "fix" tests gián đoạn bằng retries — "flaky test" = test lúc được lúc không do lý do ngoài code; đừng bấm chạy lại cho tới khi xanh mà bỏ qua nguyên nhân thật.

### Readiness Levels

**Phần này giải thích**: thang 4 bậc quyết định loop được tự chủ đến đâu. Cách đọc bảng: cột "Level" = bậc tự chủ; "Mô tả" = loop làm được gì ở bậc đó; "Checklist" = cần đạt những mục nào. Ví dụ L2 nghĩa là loop được tự sửa lỗi nhỏ nhưng mỗi bản sửa phải có verifier kiểm và người duyệt.

| Level | Mô tả | Checklist |
|-------|-------|-----------|
| **L0 — Draft** | Chỉ có ý định được ghi chép | §1 |
| **L1 — Report** | Triage → state, không auto-action | §1–3, §5 |
| **L2 — Assisted** | Auto-fix nhỏ với verifier | §1–7 |
| **L3 — Unattended** | Chạy không cần bạn nhìn | Tất cả sections |

### Quick Red Flags

**Phần này giải thích**: năm dấu hiệu cho thấy loop chưa an toàn — gặp thì sửa ngay trước khi làm tiếp.

Bạn khoan làm tiếp mà lo sửa trước nếu gặp mấy dấu hiệu này:
- Cùng một PR mà auto-fix tới > 3 lần vẫn không tiến triển — loop đang mù, cứ thử mãi, đốt token không thôi.
- Verifier lại **chính là agent session** đã viết code — vừa đá bóng vừa thổi còi thì không có chốt chặn.
- Không có state file — mỗi lần chạy là loop quên sạch lần trước.
- Run nào cũng ping người, có việc hay không cũng ping — sắp tới cả team tắt thông báo, cảnh báo thật cũng mất.
- Đã bật auto-merge mà không có path allowlist — cho phép gộp mọi thứ, kể cả thay đổi nguy hiểm.

> **Tóm gọn 1 câu:** Chấm điểm loop thành thật theo 10 mục checklist để xếp bậc tự chủ L0–L3 — bậc càng cao cần càng nhiều bằng chứng, và dính red flag thì hạ bậc.

---

## 2. Safety & Guardrails

**Phần này giải thích**: các rào chắn bắt buộc cho loop chạy production. Mỗi mục là một luật "không được phép vi phạm" — checklist §1 chấm điểm, mục này chỉ bạn chốt từng rào chắn cụ thể.

### 2.1 Path Denylist

**Phần này giải thích**: danh sách file loop tuyệt đối không được đụng. "Path" = đường dẫn file; "denylist" = danh sách đen (cấm), ngược với allowlist (cho phép).

Loop **tuyệt đối không** tự sửa các đường dẫn này nếu chưa có người đồng ý:

```
.env
.env.*
**/secrets/**
**/credentials/**
**/*_key*
**/*_secret*
.terraform/**
k8s/production/**
**/migrations/**          # trừ khi có migration loop chuyên dụng
auth/**
payments/**
billing/**
```

Cách đọc danh sách: mỗi dòng là một "pattern" (mẫu tên file). `**/secrets/**` = thư mục tên `secrets` ở bất kỳ đâu; `.env.*` = mọi file bắt đầu bằng `.env.`; `*` = khớp ký tự bất kỳ.

Ghi thẳng vào `minimal-fix` và implementer skills:

> Do not modify files matching the denylist. Escalate to human with context.

Nghĩa: "Đừng sửa file khớp danh sách cấm. Đẩy lên người kèm bối cảnh."

Tool `loop-gate` chặn cứng denylist này **bằng máy** dựa trên `gate.yaml` (không trông chờ vào việc loop có đọc file này hay chưa) — vì lời chỉ dẫn trong prompt là thứ model có thể quên, còn lệnh kiểm tra thì không bao giờ quên.

> 📄 **Code ví dụ:** [`examples/01-2-1-path-denylist.sh`](examples/01-2-1-path-denylist.sh)

> **Tóm gọn 1 câu:** File chứa mật khẩu, khoá, hạ tầng, thanh toán phải nằm trong denylist và bị tool kiểm tra chặn bằng máy — không trông chờ model tự nhớ.

### 2.2 Auto-Merge Policy

**Phần này giải thích**: có nên để loop tự gộp code (merge) vào nhánh chính hay không. Merge = gộp thay đổi vào code chính.

**Mặc định: không auto-merge.**

Nếu bạn cho phép auto-merge với những việc lặt vặt:

| Được phép | Không được phép |
|-----------|-----------------|
| Typo trong comment/docs | Thay đổi behavior |
| Lint auto-fix trong test files only | Dependency version bumps |
| Import ordering | Lockfile changes |
| Config trong allowlisted `docs/` paths | Bất kỳ denylist path nào |

Cách đọc bảng: cột trái = thay đổi vô hại đến mức máy tự gộp được (typo = lỗi chính tả; lint auto-fix = máy tự sửa lỗi định dạng; import ordering = sắp xếp lại dòng khai báo thư viện); cột phải = thay đổi lúc nào cũng cần người duyệt (behavior = cách app chạy; dependency version bump = nâng phiên bản thư viện; lockfile = file "đóng băng" phiên bản thư viện).

Ghi allowlist vào `AGENTS.md` hoặc `loop-auto-merge-allowlist.md`.

> 🔑 **Highlight Policy / Permission:** đây là **policy quyền merge** — mặc định cấm auto-merge, chỉ allowlist ghi rõ ràng mới được ngoại lệ. Bạn cứ coi file allowlist như policy-as-code: có version, có review, và được `gate check` kiểm tra trước mọi lần merge. "Policy-as-code" = luật an toàn được viết thành file trong repo, có người review và máy kiểm tra, thay vì chỉ nói miệng.

> **Tóm gọn 1 câu:** Mặc định cấm tự gộp; chỉ thay đổi vô hại trong allowlist được ngoại lệ, và file allowlist phải được quản lý như một luật trong repo.

### 2.3 MCP Connector Least Privilege

**Phần này giải thích**: quyền tối thiểu cho từng điểm nối ra hệ thống ngoài. "Least privilege" = cấp ít quyền nhất đủ dùng, không hơn.

| Connector | Read | Write |
|-----------|------|-------|
| GitHub | issues, PRs, checks | comment, label (không merge mặc định) |
| Linear | team issues | comment, status (không delete) |
| Slack | channel history | post vào `#loop-escalations` only |
| Database | — | không production write từ loops |

Cách đọc bảng: mỗi dòng là một hệ thống bot nối vào; cột "Read" = được xem gì; cột "Write" = được ghi gì. Ví dụ dòng Slack: bot đọc được lịch sử kênh nhưng chỉ được đăng vào đúng kênh `#loop-escalations` (kênh nhận việc khẩn).

Bạn nên dùng bot account / token riêng, chỉ mở đúng scope tối thiểu cần thiết. "Token" = chuỗi khoá xác thực; "scope" = phạm vi quyền của token đó.

> 🔑 **Highlight Policy / Permission (connector):** đây là **policy permission theo từng connector** (mỗi integration chỉ được đúng quyền tối thiểu) — mỗi MCP connector chỉ nhận đúng scope read/write cần thiết, trên identity riêng. Bạn có thể đối chiếu với `12-sandbox-execution` §6 (ma trận theo role) và `06` §8 (các mức RBAC). "RBAC" = phân quyền theo vai trò (role-based access control).

> **Tóm gọn 1 câu:** Mỗi connector dùng token bot riêng với quyền tối thiểu — đọc/ghi đúng phần việc, không merge, không đụng database chạy thật.

### 2.4 Human Gates

**Phần này giải thích**: danh sách việc mà lúc nào cũng cần người duyệt qua, không kể loop "tự tin" đến đâu. "Human gate" = cổng người duyệt.

Mấy việc sau lúc nào cũng cần người duyệt qua:
- Security, authentication, authorization — bảo mật và phân quyền; sai một dòng là lỗ hổng.
- Payments, billing, PII handling — thanh toán và thông tin cá nhân ("PII" = dữ liệu nhận diện cá nhân như số CMND, địa chỉ).
- Infrastructure / Terraform / K8s prod — hạ tầng chạy thật; sửa nhầm là sập dịch vụ.
- Dependency upgrades (supply chain risk) — nâng thư viện có rủi ro "chuỗi cung ứng": thư viện mới có thể chứa mã độc.
- Thay đổi đụng > N files (gợi ý N=10) — diff lớn thường là việc kiến trúc, không phải việc nhỏ.
- Thất bại lần thứ ba trên cùng một item — ba lần không xong nghĩa là loop đang mù, cần người nhìn bằng mắt thường.
- Muốn nới token budget: agent **không được** tự nâng caps trong `loop-budget.md` — phải có người duyệt và tự sửa. (Loop L3 thì dùng skill `budget-negotiator` để *xin* thêm budget.)

> **Tóm gọn 1 câu:** Bảy loại việc này luôn chờ người bấm duyệt — đặc biệt là tiền, bảo mật, hạ tầng, và việc agent muốn tự nới ngân sách của chính nó.

### 2.5 Secrets in Prompts & Logs

**Phần này giải thích**: cách tránh làm lộ mật khẩu, khoá API qua prompt và log.

- Đừng bao giờ chèn API key vào prompt của scheduler — "scheduler" = bộ hẹn giờ; prompt là văn bản gửi cho model, có thể bị lưu lại nhiều nơi.
- Log CI có thể lộ secret — skill triage nên che bớt trước khi ghi vào state. "Secret" = mật khẩu/khoá; "che bớt" = thay bằng `***` trước khi ghi.
- State file hay được commit lên git — **đừng để credential lọt vào `STATE.md`**. "Commit" = lưu vào lịch sử git; một khi vào git thì khó xoá sạch được.

> **Tóm gọn 1 câu:** Khoá và mật khẩu không bao giờ được xuất hiện trong prompt, log hay state file — che chúng trước khi ghi bất cứ đâu.

### 2.6 Flake & Test Safety

**Phần này giải thích**: cách ứng phó với test chập chờn mà không phá bộ test. "Flaky test" = test lúc xanh lúc đỏ không do code bạn đổi, mà do nguyên nhân ngoài (timing, mạng, dữ liệu dùng chung).

- Đừng tắt test chỉ để CI xanh cho xong chuyện — tắt test là mù mắt, không phải chữa bệnh.
- Đừng tăng timeout bừa khi chưa ghi rõ nguyên nhân gốc — "timeout" = thời gian chờ tối đa; tăng bừa chỉ che triệu chứng.
- Muốn cách ly test chập chờn thì mở ticket hẳn hoi và nhờ người duyệt — "cách ly" = tạm tách test ra khỏi bộ chính, nhưng phải có ticket ghi lại để có người xử lý gốc rễ.

> **Tóm gọn 1 câu:** Test chập chờn phải được ghi nhận và đưa cho người xử lý — đừng tắt test hay tăng timeout cho CI xanh mà giấu vấn đề.

### 2.7 Incident Response

**Phần này giải thích**: khi loop gây ra sự cố (ví dụ merge nhầm code xấu), xử lý theo thứ tự nào. "Incident" = sự cố.

Nếu loop merge nhầm code xấu, bạn xử lý theo các bước sau:
1. **Dừng mọi loop ngay** (`scheduler_list` → delete) — liệt kê mọi lịch chạy rồi xoá, tránh loop còn chạy nữa làm thêm hại.
2. Revert cú merge đó — "revert" = hoàn tác, đưa code về trạng thái trước khi merge.
3. Ghi lại trong state + `stories/` — "stories/" = thư mục lưu bài học sự cố, để lần sau không lặp lại.
4. Siết chặt verifier hoặc thu hẹp phạm vi rồi mới chạy lại — sửa nguyên nhân trước, đừng bật lại ngay.

> **Tóm gọn 1 câu:** Sự cố thì dừng loop trước, hoàn tác sau, ghi bài học, siết chốt chặn rồi mới chạy lại.

### 2.8 Pre-Flight Safety Check (trước L3)

**Phần này giải thích**: 5 gạch đầu dòng phải đạt trước khi cho loop chạy tự do. "Pre-flight" = kiểm tra trước khi cất cánh, như phi công soát buồng lái; "L3" = mức chạy không cần người trông.

- [ ] Denylist trong skills — danh sách file cấm đã được ghi vào skill của agent.
- [ ] Auto-merge off hoặc strict allowlist — hoặc tắt hoàn toàn, hoặc chỉ cho allowlist chặt chẽ.
- [ ] Connector scopes được review — phạm vi quyền token đã có người duyệt.
- [ ] Human gates được tài liệu trong pattern — các điểm bắt buộc người duyệt đã ghi rõ.
- [ ] Kill switch được tài liệu — nút tắt khẩn đã ghi rõ ở đâu và bấm kiểu gì.

> **Tóm gọn 1 câu:** Năm mục này đạt hết thì loop mới đủ tư cách chạy không người canh — thiếu một mục là hạ về mức có người duyệt.

### 2.9 Worktree Isolation & Consensus Sandboxing

**Phần này giải thích**: hai kỹ thuật hạn chế thiệt hại khi loop tự sửa code: chạy trong môi trường tách biệt, và yêu cầu nhiều lượt chạy đồng thuận.

- **`loop-sandbox`**: Chạy từng agent riêng lẻ trong git worktree tạm, tách biệt hẳn. Mọi thay đổi được gom thành file patch để bạn review trước khi áp vào. "Worktree" = bản sao tạm của repo; "patch" = file ghi tập thay đổi, chưa áp vào bản chính.
- **`loop-swarm`**: Cho nhiều agent chạy sandbox nối tiếp nhau để đối chiếu kết quả. Chỉ nhận sửa đổi khi các lượt chạy cho ra patch **giống nhau từng byte**. Nghĩa là: nhiều agent cùng giải một bài, chỉ nhận đáp án khi tất cả viết y hệt nhau — giảm khả năng một agent ảo tưởng.

> **Tóm gọn 1 câu:** Cách ly bằng worktree để hỏng cũng không lan, và dùng consensus (nhiều agent phải ra cùng kết quả) trước khi nhận bản sửa.

---

*Tiếp theo: [04 — Operating Loops](../04-operating/) → [05 — Multi-Loop Coordination](../05-multi-loop/)*
