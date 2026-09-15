# 🧰 07. Tools & Ecosystem

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Đây là **bộ dụng cụ CLI** và ecosystem đi kèm loop-engineering — các lệnh `npx @cobusgreyling/loop-*` phủ từng giai đoạn: tạo mới (`init`), chấm điểm (`audit`), ước chi phí (`cost`), phát hiện lệch state (`sync`), cô lập thay đổi (`worktree`), và cưỡng chế an toàn (`gate`).
> **Ẩn dụ/so sánh:** Giống **hộp đồ nghề thợ điện** — bạn không cần hiểu cấu tạo trong của từng cây tua vít; bạn chỉ cần biết cây nào dùng cho việc gì: cây vặn ốc nối dây (init), đồng hồ đo điện (cost), kìm răng cưa khóa lại (gate). Mỗi tool một việc, dùng kết hợp được.
> **Vì sao quan trọng:** Các tool này là **phần cơ giới hoá** của loop engineering — chúng cưỡng chế những thứ mà kỷ luật con người dễ lơi (nối lock, chặn denylist), và cho bạn "Loop Ready score" đo được thay vì cảm giác "chắc ổn".

> Loops không cần code thủ công từ đầu — có một hệ CLI open-source (`@cobusgreyling/loop-*`) hỗ trợ từng giai đoạn. Phần này giới thiệu từng tool và ecosystem xung quanh.

---

## 1. Front Door — `loop init / doctor / status`

> **Đọc sao cho dễ:** `init` = "trang bị cho repo của bạn bộ khung loop" (skills, state, budget); `doctor` = "khám sức khỏe" cho biết 3 việc kế tiếp nên làm. Bắt đầu mọi dự án loop từ đây — đừng tự dựng tay.

```bash
# Front door (khuyên dùng) — một binary cho init + doctor + status
npx @cobusgreyling/loop init . --pattern daily-triage --tool grok
npx @cobusgreyling/loop doctor .

# Tương đương cũ (vẫn hỗ trợ — forks không cần đổi)
npx @cobusgreyling/loop-init .

# Tuỳ chọn: scaffold thêm versioned harness (harness-foundry)
npx @cobusgreyling/loop init . --with-foundry
```

`loop init` (hoặc `loop-init`) scaffold skills, state, budget files, rồi in **Loop Ready score** và lệnh loop đầu tiên. `loop doctor` kết hợp audit + sync + file checks thành top-3 next actions. Đổi `--tool` sang `claude`, `codex`, hoặc `opencode`. Dùng `--with-foundry` khi muốn loop thành composable runtime stack.

---

## 2. loop-audit — Loop Readiness Score

> **Đọc sao cho dễ:** `audit` = "chấm điểm bài kiểm tra vận hành" — cho bạn một con số 0–100 thể hiện mức sẵn sàng production. Giống điểm tín nhiệm tín dụng: thấp thì khoan để loop tự chạy, cao lên dần khi bạn scaffold đúng.

```bash
npx @cobusgreyling/loop audit . --suggest
```

Chấm điểm **Loop Readiness** (L0→L3) cho project của bạn — một con số chạy từ ~10 lên 100 khi bạn scaffold đúng các phần. Gồm constraints + governance + **Harness Runtime** (v1.7). Cap **L3** cho đến khi `loop-budget.md`, `loop-run-log.md`, và một LOOP.md budget section tồn tại.

---

## 3. loop-cost — Ước Tính Token

```bash
npx @cobusgreyling/loop cost --pattern ci-sweeper --cadence 15m --level L2
```

Ước lượng token spend **trước khi schedule** — tránh bị sốc bill tuần sau. Xem chi tiết budget rules trong [04-operating](../04-operating/).

---

## 4. loop-sync — Phát Hiện Drift

```bash
npx @cobusgreyling/loop sync .
```

Phát hiện drift giữa `STATE.md` và `LOOP.md` — hai file mô tả trạng thái và cấu hình loop nhưng có thể lệch nhau theo thời gian.

---

## 5. loop-context — Memory + Circuit Breaker

```bash
npx @cobusgreyling/loop context --check --ledger run.json
```

Stateful memory manager + circuit breaker cho long runs. Quản lý context không phình vô hạn qua nhiều iterations.

---

## 6. loop-worktree — Cô Lập Thay Đổi

> **Đọc sao cho dễ:** `worktree` = "phòng thực hành riêng" cho mỗi lần thử fix — agent sửa trong phòng riêng, hỏng thì bỏ phòng đó, không đụng tới code chính. Kèm `lock/unlock` để các loops không vào cùng phòng cùng lúc.

```bash
npx @cobusgreyling/loop-worktree create --run-id <id> --pattern <p>
```

Quản lý isolated git worktrees mỗi lần thử fix — một worktree mỗi attempt, theo dõi trong manifest, dọn khi reject/escalate. Kèm `lock`/`unlock` cho multi-loop coordination (xem [05-multi-loop](../05-multi-loop/)).

---

## 7. loop-gate — Cưỡng Chế Cơ Học

```bash
npx @cobusgreyling/loop gate check --action auto-merge --paths <f1,f2,...>
```

Cưỡng chế **cơ học** path denylist + auto-merge allowlist từ `gate.yaml` — không dựa vào việc loop có đọc file safety hay không. Exit `2` = escalate, `0` = proceed — cùng convention `loop-context --check` dùng, nên control scripts chain được cả hai.

---

## 8. loop-sandbox & loop-swarm — Cô Lập + Consensus

```bash
npx @cobusgreyling/loop-sandbox run -- <cmd>   # Ephemeral worktree isolation + patch capture
```

- **loop-sandbox**: ephemeral git worktree isolation cho single agent runs. Bắt changes thành reviewable patch files trước khi apply.
- **loop-swarm**: multi-agent consensus sandboxing qua các `loop-sandbox` runs tuần tự. Yêu cầu **byte-identical patch consensus** giữa các runs trước khi accept edits.

---

## 9. Các Tool Khác

| Tool | Mô tả | Lệnh |
|------|-------|------|
| **loop-action** | GitHub Composite Action chạy loops trong CI | `uses: cobusgreyling/loop-engineering/tools/loop-action@main` |
| **loop-mcp-server** | Patterns/skills/state/budget/safety docs như MCP resources | `npx @cobusgreyling/loop-mcp-server` |
| **loop-cost** | Token spend estimator | `npx @cobusgreyling/loop-cost` |

**Reference MCP server**: repo ship `tools/mcp-server/` — patterns, skills, state, budget, safety docs như runtime-queryable MCP resources (giảm prompt stuffing). Config example: `examples/mcp/loop-engineering.mcp.json`.

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

- Khi agents **quên giữa các sessions** → thêm memory-engineering.
- Khi có **nhiều agents/loops** trong team → thêm fleet-engineering.
- Next sau **Loop Ready 80+** → version loop như một harness (`loop-init` tự in CTA; `loop-audit` recommend Foundry khi score mạnh nhưng thiếu `.foundry/stack.yaml`).

---

*Trở về [README](../README.md) — tổng quan Module XII*
