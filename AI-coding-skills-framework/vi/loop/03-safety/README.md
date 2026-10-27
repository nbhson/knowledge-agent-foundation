# 🛡️ 03. Safety & Loop Design Checklist

> Loop giúp khả năng phán đoán của bạn lan rộng ra — cả điểm tốt lẫn điểm chưa tốt. Phần này gồm hai thứ: **Loop Design Checklist** (bảng chấm điểm xem loop đã đủ cứng để lên production chưa) và **Safety & Guardrails** (mức an toàn tối thiểu cho loop production có đụng tới code hay hệ thống bên ngoài).

---

## 1. Loop Design Checklist

Bạn cứ chấm điểm **thật lòng** trước khi cho loop chạy production. Loop nào còn thiếu khâu kiểm chứng thì chưa đủ điều kiện chạy mà không có người trông.

### §1 Purpose & Scope
- [ ] **Mục tiêu duy nhất rõ ràng** — một câu: loop này hoàn thành điều gì?
- [ ] **Non-goals tường minh** — loop này sẽ *không* làm gì?
- [ ] **Watched scope** — repos, branches, PRs, tickets nào?
- [ ] **Phased rollout** — report-only trước, rồi act?
- [ ] **Ambiguous input handled** — khi work item quá mơ hồ để verify "done", loop clarify hoặc escalate thay vì đoán (scaffold `loop-intake` skill)

### §2 Scheduling
- [ ] **Cadence đã chọn** — interval khớp urgency?
- [ ] **Fire immediately** — chạy lần đầu ngay hay chờ interval?
- [ ] **Durable** — sống sót restart?
- [ ] **Off-hours behavior** — cadence chậm hơn hoặc pause qua đêm?
- [ ] **Self-cleanup** — `scheduler_delete` khi watchlist rỗng?

### §3 Skills
- [ ] **Triage skill** tồn tại với output format chặt chẽ
- [ ] **Action skills** (minimal-fix...) khớp quy ước dự án
- [ ] **Skill descriptions** boring + specific (auto-triggering tốt)
- [ ] **Build/test commands** được ghi trong skills / AGENTS.md

### §4 Maker / Checker Split
- [ ] **Implementer** và **verifier** là hai thực thể tách biệt (agent, model, hoặc instructions)
- [ ] Implementer **không thể** tự đánh dấu work của mình "done"
- [ ] Verifier chạy **tests** trong cô lập (worktree) trước khi approve
- [ ] `/goal` hoặc tương đương dùng **fresh model** cho stop condition

### §5 State / Memory
- [ ] **State file** hoặc board schema được tài liệu hoá
- [ ] Loop **đọc** state cũ ở đầu mỗi run
- [ ] Loop **ghi** outcomes, timestamps, last actions
- [ ] **Prune** resolved/merged/closed items mỗi run
- [ ] Human overrides được ghi trong state

### §6 Human Handoff
- [ ] **Escalation triggers** tường minh (max attempts, risk paths, ambiguity)
- [ ] **Denylist paths** — auth, payments, secrets, infra
- [ ] **Notification rule** — chỉ ping human khi cần hành động
- [ ] **Inbox** — nơi items mơ hồ đáp xuống

### §7 Connectors (MCP)
- [ ] Permissions tối thiểu (read vs write)
- [ ] Loop có thể **mở/cập nhật PRs** hoặc tickets nếu đang act
- [ ] Bot identity rõ ràng trên PR comments (VD: "Loop Engineering — PR Babysitter")

### §8 Cost & Limits
- [ ] **Token budget** được ước tính
- [ ] **`loop-budget.md`** với daily caps + kill switch
- [ ] **`loop-run-log.md`** cho append-only run history
- [ ] **`loop-budget` skill** kiểm tra spend đầu/cuối mỗi run
- [ ] **Max iterations** mỗi item mỗi run
- [ ] **Max auto-PRs** mỗi ngày (cleanup loops)
- [ ] **Pause/kill criteria** được định nghĩa

### §9 Observability
- [ ] Log mỗi run: started, items found, actions taken, escalations
- [ ] **Success metrics** đã chọn
- [ ] Team có thể **inspect state file** mà không cần đọc chat logs

### §10 Safety
- [ ] Không auto-merge nếu không có allowlist tường minh
- [ ] Secrets/env files trong denylist
- [ ] Flake handling — không "fix" tests gián đoạn bằng retries

### Readiness Levels

| Level | Mô tả | Checklist |
|-------|-------|-----------|
| **L0 — Draft** | Chỉ có ý định được ghi chép | §1 |
| **L1 — Report** | Triage → state, không auto-action | §1–3, §5 |
| **L2 — Assisted** | Auto-fix nhỏ với verifier | §1–7 |
| **L3 — Unattended** | Chạy không cần bạn nhìn | Tất cả sections |

### Quick Red Flags

Bạn khoan làm tiếp mà lo sửa trước nếu gặp mấy dấu hiệu này:
- Cùng một PR mà auto-fix tới > 3 lần vẫn không tiến triển
- Verifier lại **chính là agent session** đã viết code
- Không có state file — mỗi lần chạy là loop quên sạch lần trước
- Run nào cũng ping người, có việc hay không cũng ping
- Đã bật auto-merge mà không có path allowlist

---

## 2. Safety & Guardrails

### 2.1 Path Denylist

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

Ghi thẳng vào `minimal-fix` và implementer skills:

> Do not modify files matching the denylist. Escalate to human with context.

Tool `loop-gate` chặn cứng denylist này **bằng máy** dựa trên `gate.yaml` (không trông chờ vào việc loop có đọc file này hay chưa):

```bash
npx @cobusgreyling/loop gate check --action auto-merge --paths <changed files>
# exit 2 = escalate, exit 0 = proceed
```

### 2.2 Auto-Merge Policy

**Mặc định: không auto-merge.**

Nếu bạn cho phép auto-merge với những việc lặt vặt:

| Được phép | Không được phép |
|-----------|-----------------|
| Typo trong comment/docs | Thay đổi behavior |
| Lint auto-fix trong test files only | Dependency version bumps |
| Import ordering | Lockfile changes |
| Config trong allowlisted `docs/` paths | Bất kỳ denylist path nào |

Ghi allowlist vào `AGENTS.md` hoặc `loop-auto-merge-allowlist.md`.

> 🔑 **Highlight Policy / Permission:** đây là **policy quyền merge** — mặc định cấm auto-merge, chỉ allowlist ghi rõ ràng mới được ngoại lệ. Bạn cứ coi file allowlist như policy-as-code: có version, có review, và được `gate check` kiểm tra trước mọi lần merge.

### 2.3 MCP Connector Least Privilege

| Connector | Read | Write |
|-----------|------|-------|
| GitHub | issues, PRs, checks | comment, label (không merge mặc định) |
| Linear | team issues | comment, status (không delete) |
| Slack | channel history | post vào `#loop-escalations` only |
| Database | — | không production write từ loops |

Bạn nên dùng bot account / token riêng, chỉ mở đúng scope tối thiểu cần thiết.

> 🔑 **Highlight Policy / Permission (connector):** đây là **policy permission theo từng connector** (mỗi integration chỉ được đúng quyền tối thiểu) — mỗi MCP connector chỉ nhận đúng scope read/write cần thiết, trên identity riêng. Bạn có thể đối chiếu với `12-sandbox-execution` §6 (ma trận theo role) và `06` §8 (các mức RBAC).

### 2.4 Human Gates

Mấy việc sau lúc nào cũng cần người duyệt qua:
- Security, authentication, authorization
- Payments, billing, PII handling
- Infrastructure / Terraform / K8s prod
- Dependency upgrades (supply chain risk)
- Thay đổi đụng > N files (gợi ý N=10)
- Thất bại lần thứ ba trên cùng một item
- Muốn nới token budget: agent **không được** tự nâng caps trong `loop-budget.md` — phải có người duyệt và tự sửa. (Loop L3 thì dùng skill `budget-negotiator` để *xin* thêm budget.)

### 2.5 Secrets in Prompts & Logs

- Đừng bao giờ chèn API key vào prompt của scheduler
- Log CI có thể lộ secret — skill triage nên che bớt trước khi ghi vào state
- State file hay được commit lên git — **đừng để credential lọt vào `STATE.md`**

### 2.6 Flake & Test Safety

- Đừng tắt test chỉ để CI xanh cho xong chuyện
- Đừng tăng timeout bừa khi chưa ghi rõ nguyên nhân gốc
- Muốn cách ly test chập chờn thì mở ticket hẳn hoi và nhờ người duyệt

### 2.7 Incident Response

Nếu loop merge nhầm code xấu, bạn xử lý theo các bước sau:
1. **Dừng mọi loop ngay** (`scheduler_list` → delete)
2. Revert cú merge đó
3. Ghi lại trong state + `stories/`
4. Siết chặt verifier hoặc thu hẹp phạm vi rồi mới chạy lại

### 2.8 Pre-Flight Safety Check (trước L3)

- [ ] Denylist trong skills
- [ ] Auto-merge off hoặc strict allowlist
- [ ] Connector scopes được review
- [ ] Human gates được tài liệu trong pattern
- [ ] Kill switch được tài liệu

### 2.9 Worktree Isolation & Consensus Sandboxing

- **`loop-sandbox`**: Chạy từng agent riêng lẻ trong git worktree tạm, tách biệt hẳn. Mọi thay đổi được gom thành file patch để bạn review trước khi áp vào.
- **`loop-swarm`**: Cho nhiều agent chạy sandbox nối tiếp nhau để đối chiếu kết quả. Chỉ nhận sửa đổi khi các lượt chạy cho ra patch **giống nhau từng byte**.

---

*Tiếp theo: [04 — Operating Loops](../04-operating/) → [05 — Multi-Loop Coordination](../05-multi-loop/)*
