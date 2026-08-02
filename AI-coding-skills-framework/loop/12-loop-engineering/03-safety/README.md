# 🛡️ 03. Safety & Loop Design Checklist

> Loops khuếch đại judgment — cả tốt lẫn xấu. Phần này gồm: **Loop Design Checklist** (rubric sẵn sàng production) và **Safety & Guardrails** (mức tối thiểu cho loops production chạm vào code hoặc external systems).

---

## 1. Loop Design Checklist

Dùng trước khi bật loop trong production. Chấm điểm **thành thật** — một loop thiếu verification chưa sẵn sàng để chạy unattended.

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

Dừng và sửa trước khi tiếp tục nếu:
- Cùng PR có > 3 lần auto-fix attempt không tiến triển
- Verifier là **cùng agent session** với implementer
- Không có state file — loop mất trí nhớ mỗi lần chạy
- Notifications trên mọi run bất kể findings
- Auto-merge bật mà không có path allowlist

---

## 2. Safety & Guardrails

### 2.1 Path Denylist

Loop **không bao giờ** được auto-edit các paths này nếu không có sự đồng ý của con người:

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

Encode trong `minimal-fix` và implementer skills:

> Do not modify files matching the denylist. Escalate to human with context.

Tool `loop-gate` cưỡng chế denylist này **một cách cơ học** từ `gate.yaml` (không dựa vào việc loop đã đọc file này chưa):

```bash
npx @cobusgreyling/loop gate check --action auto-merge --paths <changed files>
# exit 2 = escalate, exit 0 = proceed
```

### 2.2 Auto-Merge Policy

**Mặc định: không auto-merge.**

Nếu bạn cho phép auto-merge cho loops trivial:

| Được phép | Không được phép |
|-----------|-----------------|
| Typo trong comment/docs | Thay đổi behavior |
| Lint auto-fix trong test files only | Dependency version bumps |
| Import ordering | Lockfile changes |
| Config trong allowlisted `docs/` paths | Bất kỳ denylist path nào |

Document allowlist trong `AGENTS.md` hoặc `loop-auto-merge-allowlist.md`.

### 2.3 MCP Connector Least Privilege

| Connector | Read | Write |
|-----------|------|-------|
| GitHub | issues, PRs, checks | comment, label (không merge mặc định) |
| Linear | team issues | comment, status (không delete) |
| Slack | channel history | post vào `#loop-escalations` only |
| Database | — | không production write từ loops |

Dùng bot accounts / tokens riêng với scopes tối thiểu.

### 2.4 Human Gates

Luôn yêu cầu human cho:
- Security, authentication, authorization
- Payments, billing, PII handling
- Infrastructure / Terraform / K8s prod
- Dependency upgrades (supply chain risk)
- Changes chạm > N files (gợi ý N=10)
- Lần thứ ba thất bại trên cùng item
- Token budget extension: agents **không thể** tự nâng caps trong `loop-budget.md` — human phải approve và tự sửa. (L3 loops dùng `budget-negotiator` skill để *request* thêm budget.)

### 2.5 Secrets in Prompts & Logs

- Không bao giờ dán API keys vào scheduler prompts
- CI logs có thể chứa secrets — triage skill nên redact trước khi ghi state
- State files thường được commit — **không credentials trong `STATE.md`**

### 2.6 Flake & Test Safety

- Không disable tests để làm CI xanh
- Không tăng timeouts mù quáng mà không có root-cause note
- Quarantine flakes qua ticket tường minh + human approval

### 2.7 Incident Response

Nếu loop merge code xấu:
1. **Pause tất cả loops ngay** (`scheduler_list` → delete)
2. Revert merge
3. Ghi trong state + `stories/`
4. Tighten verifier hoặc shrink scope trước khi restart

### 2.8 Pre-Flight Safety Check (trước L3)

- [ ] Denylist trong skills
- [ ] Auto-merge off hoặc strict allowlist
- [ ] Connector scopes được review
- [ ] Human gates được tài liệu trong pattern
- [ ] Kill switch được tài liệu

### 2.9 Worktree Isolation & Consensus Sandboxing

- **`loop-sandbox`**: Ephemeral git worktree isolation cho single agent runs. Bắt changes thành reviewable patch files trước khi apply.
- **`loop-swarm`**: Multi-agent consensus sandboxing qua các `loop-sandbox` runs tuần tự. Yêu cầu **byte-identical patch consensus** giữa các runs trước khi accept edits.

---

*Tiếp theo: [04 — Operating Loops](../04-operating/) → [05 — Multi-Loop Coordination](../05-multi-loop/)*
