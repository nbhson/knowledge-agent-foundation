# 🧰 07. Tools & Ecosystem

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Đây là **bộ dụng cụ CLI** đi kèm loop-engineering — các lệnh `npx @cobusgreyling/loop-*` phủ từng giai đoạn: tạo mới (`init`), chấm điểm (`audit`), ước chi phí (`cost`), phát hiện lệch state (`sync`), cô lập thay đổi (`worktree`), và cưỡng chế an toàn (`gate`).
> **Hình dung cho dễ:** Giống **hộp đồ nghề thợ điện** — bạn không cần hiểu cấu tạo bên trong của từng cây tua vít; bạn chỉ cần biết cây nào dùng cho việc gì: cây vặn ốc nối dây (init), đồng hồ đo điện (cost), kìm khóa lại (gate). Mỗi tool một việc, dùng kết hợp được.
> **Vì sao quan trọng:** Các tool này là **phần cơ giới hoá** của loop engineering — chúng làm thay những việc mà kỷ luật con người dễ bỏ sót (giữ lock, chặn denylist), và cho bạn "Loop Ready score" đo được thay vì cảm giác "chắc là ổn".

> Loops không cần code thủ công từ đầu — đã có hệ CLI open-source (`@cobusgreyling/loop-*`) hỗ trợ từng giai đoạn. Phần này giới thiệu từng tool và hệ sinh thái xung quanh.

---

## 1. Front Door — `loop init / doctor / status`

> **Đọc sao cho dễ:** `init` là "dựng khung loop cho repo của bạn" (skills, state, budget); `doctor` là "khám sức khỏe" và cho biết 3 việc nên làm tiếp. Bạn bắt đầu mọi dự án loop từ đây — đừng tự dựng bằng tay.

> 📄 **Code ví dụ:** [`examples/01-1-front-door-loop-init-doctor-status.sh`](examples/01-1-front-door-loop-init-doctor-status.sh)

`loop init` (hoặc `loop-init`) dựng sẵn skills, state, budget files, rồi in ra **Loop Ready score** và lệnh loop đầu tiên. `loop doctor` gộp audit, sync và kiểm tra file thành top-3 việc nên làm tiếp. Bạn đổi `--tool` sang `claude`, `codex`, hoặc `opencode`. Dùng `--with-foundry` khi muốn loop thành composable runtime stack.

---

## 2. loop-audit — Loop Readiness Score

> **Đọc sao cho dễ:** `audit` là "chấm điểm bài kiểm tra vận hành" — cho bạn con số 0–100 thể hiện mức sẵn sàng production. Giống điểm tín nhiệm tín dụng: điểm thấp thì khoan để loop tự chạy, điểm cao dần lên khi bạn dựng khung đúng cách.

> 📄 **Code ví dụ:** [`examples/02-2-loop-audit-loop-readiness-score.sh`](examples/02-2-loop-audit-loop-readiness-score.sh)

Chấm điểm **Loop Readiness** (L0→L3) cho project của bạn — con số chạy từ ~10 lên 100 khi bạn dựng khung đúng các phần. Gồm constraints, governance và **Harness Runtime** (v1.7). Giữ ở **L3** cho đến khi có `loop-budget.md`, `loop-run-log.md`, và mục budget trong LOOP.md.

---

## 3. loop-cost — Ước Tính Token

> 📄 **Code ví dụ:** [`examples/03-3-loop-cost-uoc-tinh-token.sh`](examples/03-3-loop-cost-uoc-tinh-token.sh)

Ước lượng token spend **trước khi lên lịch chạy** — để không bất ngờ với bill tuần sau. Xem chi tiết budget rules trong [04-operating](../04-operating/).

---

## 4. loop-sync — Phát Hiện Drift

> 📄 **Code ví dụ:** [`examples/04-4-loop-sync-phat-hien-drift.sh`](examples/04-4-loop-sync-phat-hien-drift.sh)

Phát hiện lệch giữa `STATE.md` và `LOOP.md` — hai file mô tả trạng thái và cấu hình loop nhưng có thể lệch nhau dần theo thời gian.

---

## 5. loop-context — Memory + Circuit Breaker

> 📄 **Code ví dụ:** [`examples/05-5-loop-context-memory-circuit-breaker.sh`](examples/05-5-loop-context-memory-circuit-breaker.sh)

Bộ nhớ có trạng thái và cầu dao tự ngắt cho các run dài. Giúp context không phình vô hạn qua nhiều vòng lặp.

---

## 6. loop-worktree — Cô Lập Thay Đổi

> **Đọc sao cho dễ:** `worktree` là "phòng thực hành riêng" cho mỗi lần thử fix — agent sửa trong phòng riêng, hỏng thì bỏ phòng đó, không ảnh hưởng tới code chính. Kèm thêm `lock/unlock` để các loop không vào cùng chỗ cùng lúc.

> 📄 **Code ví dụ:** [`examples/06-6-loop-worktree-co-lap-thay-oi.sh`](examples/06-6-loop-worktree-co-lap-thay-oi.sh)

Quản lý git worktree riêng cho mỗi lần thử fix — một worktree cho mỗi attempt, theo dõi trong manifest, dọn khi reject/escalate. Kèm `lock`/`unlock` cho multi-loop coordination (xem [05-multi-loop](../05-multi-loop/)).

---

## 7. loop-gate — Cưỡng Chế Cơ Học

> 📄 **Code ví dụ:** [`examples/07-7-loop-gate-cuong-che-co-hoc.sh`](examples/07-7-loop-gate-cuong-che-co-hoc.sh)

Cưỡng chế **bằng máy** path denylist và auto-merge allowlist từ `gate.yaml` — không phụ thuộc vào việc loop có đọc file safety hay không. Exit `2` là escalate, `0` là proceed — cùng quy ước mà `loop-context --check` dùng, nên control scripts nối tiếp được cả hai.

---

## 8. loop-sandbox & loop-swarm — Cô Lập + Consensus

> 📄 **Code ví dụ:** [`examples/08-8-loop-sandbox-loop-swarm-co-lap-consensus.sh`](examples/08-8-loop-sandbox-loop-swarm-co-lap-consensus.sh)

- **loop-sandbox**: git worktree tách biệt tạm thời cho từng lượt chạy agent đơn lẻ. Gom changes thành patch files để review trước khi áp vào.
- **loop-swarm**: sandbox lấy đồng thuận từ nhiều agent qua các lượt `loop-sandbox` chạy nối tiếp. Chỉ chấp nhận edits khi các lượt cho ra patch **giống nhau từng byte**.

---

## 9. Các Tool Khác

| Tool | Mô tả | Lệnh |
|------|-------|------|
| **loop-action** | GitHub Composite Action chạy loops trong CI | `uses: cobusgreyling/loop-engineering/tools/loop-action@main` |
| **loop-mcp-server** | Patterns/skills/state/budget/safety docs như MCP resources | `npx @cobusgreyling/loop-mcp-server` |
| **loop-cost** | Token spend estimator | `npx @cobusgreyling/loop-cost` |

**Reference MCP server**: repo có sẵn `tools/mcp-server/` — patterns, skills, state, budget, safety docs thành MCP resources truy vấn được lúc chạy (đỡ nhồi prompt). Ví dụ config: `examples/mcp/loop-engineering.mcp.json`.

---

## 10. Ecosystem Stack

```
memory-engineering → loop-engineering → harness-foundry → outerloop → fleet-engineering
   (persist)            (patterns)         (runtime)        (verdict)     (population)
```

| Layer | Bạn nhận được | Start |
|-------|---------------|-------|
| **Memory** | Tiers, recall budget, Memory Ready score | [memory-engineering](https://github.com/cobusgreyling/memory-engineering) |
| **Design** (repo loop-engineering) | Patterns, starters, Loop Ready score | `npx @cobusgreyling/loop init .` rồi `loop doctor .` |
| **Runtime** | Versioned harness, traces, evolve | `npx @cobusgreyling/loop init . --with-foundry` hoặc [harness-foundry showcase](https://github.com/cobusgreyling/harness-foundry) |
| **Govern** | Evidence, verdict, answerability | [outerloop](https://github.com/cobusgreyling/outerloop) |
| **Fleet** | Registry, inbox, budgets, kill switch | `npx @cobusgreyling/fleet-init .` |

### Companion Projects

| Companion | Mô tả |
|-----------|-------|
| [Goal Engineering](https://github.com/cobusgreyling/goal-engineering) | Loops phát hiện, goals hoàn thành — `/goal` + stack cookbook |
| [Memory Engineering](https://github.com/cobusgreyling/memory-engineering) | Ngừng giải thích lại repo — tiers, budget, Memory Ready score |
| [Fleet Engineering](https://github.com/cobusgreyling/fleet-engineering) | Quản trị population agents — registry, inbox, kill switch |
| [harness-foundry](https://github.com/cobusgreyling/harness-foundry) | Companion runtime — versioned stacks, sessions, traces |
| [outerloop](https://github.com/cobusgreyling/outerloop) | Companion governance — evidence → verdict → answerability |

### Khi Nào Thêm Gì

- Khi agents **quên giữa các session** → thêm memory-engineering.
- Khi có **nhiều agents/loops** trong team → thêm fleet-engineering.
- Bước tiếp theo sau **Loop Ready 80+** → version loop của bạn như một harness (`loop-init` tự in CTA; `loop-audit` gợi ý Foundry khi điểm mạnh nhưng thiếu `.foundry/stack.yaml`).

---

## Cập nhật 10/2026 — Alternative Toolchain & So Sánh

### So Sánh Loop Scheduling Approaches

| Approach | Đặc điểm | Phù hợp khi |
|----------|----------|-------------|
| **Shell script + cron** | Đơn giản nhất, no deps, chạy ngay trên máy bạn | Loop cá nhân, demo, môi trường đã có cron |
| **GitHub Actions** | Hosted, free tier, event-driven (cron + trigger theo PR/issue) | Loop gắn với repo, team nhỏ muốn zero infra |
| **Temporal** | Durable execution, checkpoint/resume native | Long-running agents — dừng/tiếp tục không mất state |
| **Airflow** | Data pipelines, DAG phức tạp, dependency graph | Pipeline dữ liệu/ML nhiều bước phụ thuộc nhau |
| **Python asyncio scheduler** (in-process) | Chạy trong cùng process với app | Hundreds of loops trong một service tự quản |

### Khi Nào Chọn Gì

- **Mỗi ngày 1–2 runs** → cron hoặc GitHub Actions là đủ, đừng phức tạp hoá.
- **Cần checkpoint/resume dài hạn** → Temporal — durable execution sinh ra cho việc này.
- **ML / data pipeline** → Airflow với DAG rõ ràng từng bước.
- **Hundreds of loops** → dedicated orchestrator (Kestra, Temporal, fleet-engineering).

> **📌 Lưu ý:** Các CLI `loop-*` giới thiệu ở trên hiện tại là **một lựa chọn**, không phải bắt buộc. Các pattern ở [02-patterns](../02-patterns/) chạy được trên **mọi scheduler** trong bảng ở trên — pattern là quy trình + metrics + safety gates, scheduler chỉ là cách thức kích hoạt.

### Xem Thêm

- [harness — 10. Automation](../../harness/10-automation/README.md) — scheduler patterns chi tiết.
- [AGENT_SYSTEM_ARCHITECTURE.md](../../AGENT_SYSTEM_ARCHITECTURE.md) — Layer 5 (automation trong tổng thể kiến trúc).

---

*Trở về [README](../README.md) — tổng quan Module XII*
