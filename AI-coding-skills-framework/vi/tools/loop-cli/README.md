# 🔁 Loop CLI — Bộ Công Cụ Dòng Lệnh Cho Loop & Harness Runtime

> ## 📑 Mục Lục
>
> - [Câu Chuyện Mở Đầu](#câu-chuyện-mở-đầu)
> - [Tại Sao Loop CLI Quan Trọng?](#tại-sao-loop-cli-quan-trọng)
> - [Quan Hệ Với Harness](#quan-hệ-với-harness)
> - [Tổng Quan Các Lệnh](#tổng-quan-các-lệnh)
> - [Lộ Trình Học (Cấu Trúc Thư Mục)](#lộ-trình-học-cấu-trúc-thư-mục)
> - [Case Studies Thực Tế](#case-studies-thực-tế)
> - [Tài Liệu Tham Khảo](#tài-liệu-tham-khảo)

---

### Câu Chuyện Mở Đầu

Hãy hình dung thế này: bạn đã dựng xong một harness chỉn chu trong `harness/` — đủ context, memory, guardrails, evaluation. Bạn cũng đã tin loop là cách vận hành đúng. Nhưng ngặt một nỗi là mỗi loop lại phải **dựng tay từ đầu**: tạo `STATE.md`, `LOOP.md`, budget files, safety config, worktree isolation...

Có một nỗi đau thầm lặng ở đây: dự án mới nào bạn cũng **gõ lại cùng một bộ khung**, rồi thả cho các loop chạy tự do — không chấm điểm, không phát hiện drift, không có gate bắt buộc. Tới lúc nhiều loop chạy song song là chúng giẫm chân lên nhau ngay.

> *"Loops don't need to be hand-coded from scratch — there's an open-source CLI ecosystem supporting each phase."*

**Loop CLI** (`@cobusgreyling/loop-*`) là bộ công cụ dòng lệnh hiện thực hóa toàn bộ lý thuyết vòng lặp: từ init scaffold, chấm điểm readiness, ước lượng token, phát hiện drift, đến cưỡng chế cơ học và cô lập sandbox.

### Tại Sao Loop CLI Quan Trọng?

> **"A loop without tooling is a ritual. A loop with tooling is an engineering discipline."**

| # | Lý do | Giải thích |
|---|-------|------------|
| 1 | **Scaffold chuẩn hóa** | `loop init` tạo đúng cấu trúc skills/state/budget files — không còn "viết lại từ đầu" mỗi dự án |
| 2 | **Đo lường được** | `loop audit` chấm điểm Loop Readiness L0→L3; `loop cost` ước lượng token trước khi chạy |
| 3 | **Cưỡng chế cơ học** | `loop gate` enforce path denylist/allowlist từ config — không phụ thuộc việc agent có đọc safety file không |
| 4 | **An toàn đa loop** | `loop worktree` + `loop sandbox` cô lập từng attempt, `loop swarm` yêu cầu consensus trước khi chấp nhận edits |

### Quan Hệ Với Harness

```
harness/  ← dạy KIẾN THỨC (7 components, 15 modules)
loop/     ← dạy VÒNG LẶP (concepts, patterns, safety, operating)
tools/loop-cli/  ← ❯ CÔNG CỤ hiện thực hóa cả hai

┌────────────────────────────────────────────────────────────┐
│  LOOP CLI MAP VS HARNESS COMPONENTS                        │
│                                                            │
│  loop init / doctor / status  → scaffold toàn bộ harness   │
│  loop audit                   → đánh giá Harness Runtime   │
│  loop context --check         → harness/01, 03 (memory)    │
│  loop gate check              → harness/06 (permission)    │
│  loop sandbox / worktree      → harness/10 (automation)    │
│  loop-swarm                   → harness/09 (multi-agent)   │
│  loop-mcp-server              → harness/06 (MCP protocol)  │
└────────────────────────────────────────────────────────────┘
```

## Tổng Quan Các Lệnh

### 1. Front Door — `loop init / doctor / status`

```bash
# Scaffold + chẩn đoán + trạng thái (khuyên dùng: một binary cho cả ba)
npx @cobusgreyling/loop init . --pattern daily-triage --tool grok
npx @cobusgreyling/loop doctor .
npx @cobusgreyling/loop status .

# Tương đương cũ (forks không cần đổi)
npx @cobusgreyling/loop-init .

# Tuỳ chọn: scaffold thêm versioned harness
npx @cobusgreyling/loop init . --with-foundry
```

`loop init` dựng sẵn skills + state + budget files rồi in ra **Loop Ready score** kèm lệnh loop đầu tiên để bạn chạy thử. `loop doctor` gom audit + sync + file checks thành **top-3 việc nên làm tiếp theo**. Muốn đổi tool thì chỉnh `--tool` sang `claude`, `codex` hoặc `opencode`.

### 2. `loop audit` — Loop Readiness Score

```bash
npx @cobusgreyling/loop audit . --suggest
```

Chấm **Loop Readiness** (L0→L3) — scaffold càng chuẩn thì điểm càng nhích dần từ ~10 lên 100. Chấm cả constraints + governance + **Harness Runtime** (v1.7). Muốn chạm **L3** thì cần có đủ `loop-budget.md`, `loop-run-log.md` và budget section trong LOOP.md.

### 3. `loop cost` — Ước Lượng Token

```bash
npx @cobusgreyling/loop cost --pattern ci-sweeper --cadence 15m --level L2
```

Áng chừng token sẽ tốn **trước khi bạn đặt lịch chạy** — để tuần sau khỏi giật mình nhìn bill.

### 4. `loop sync` — Phát Hiện Drift

```bash
npx @cobusgreyling/loop sync .
```

Soi chỗ lệch giữa `STATE.md` và `LOOP.md` — hai file này chạy một thời gian là rất dễ trôi khỏi nhau.

### 5. `loop context` — Memory + Circuit Breaker

```bash
npx @cobusgreyling/loop context --check --ledger run.json
```

Một memory manager có trạng thái kèm circuit breaker cho các run dài hơi. Hiểu đơn giản là giữ cho context khỏi phình vô hạn sau nhiều vòng lặp.

### 6. `loop worktree` — Cô Lập Thay Đổi

```bash
npx @cobusgreyling/loop-worktree create --run-id <id> --pattern <p>
```

Đứng ra quản lý các git worktree cách ly — mỗi attempt một worktree riêng, theo dõi qua manifest, xong việc (reject/escalate) thì dọn. Có kèm `lock`/`unlock` để nhiều loop khỏi giành nhau.

### 7. `loop gate` — Cưỡng Chế Cơ Học

```bash
npx @cobusgreyling/loop gate check --action auto-merge --paths <f1,f2,...>
```

Bắt buộc **bằng cơ chế** path denylist + auto-merge allowlist đọc từ `gate.yaml`. Exit `2` là escalate, `0` là cho đi tiếp — cùng convention với `loop-context --check` nên bạn chain chúng lại được.

### 8. `loop sandbox` & `loop swarm` — Cô Lập + Consensus

```bash
npx @cobusgreyling/loop-sandbox run -- <cmd>   # Ephemeral worktree isolation + patch capture
```

- **loop-sandbox**: bắt changes thành reviewable patch files trước khi apply.
- **loop-swarm**: multi-agent consensus — yêu cầu **byte-identical patch consensus** giữa các runs.

### 9. Loop MCP Server

```bash
npx @cobusgreyling/loop-mcp-server
```

Patterns/skills/state/budget/safety docs như MCP resources — giảm prompt stuffing. Reference config: `examples/mcp/loop-engineering.mcp.json`.

## Lộ Trình Học (Cấu Trúc Thư Mục)

```
loop-cli/
├── README.md            ← BẠN ĐANG Ở ĐÂY — tổng quan + lộ trình
├── 01-concepts/         ← (TODO) Kiến trúc loop-*: plugin system, run ledger, state files
├── 02-setup/            ← (TODO) Cài đặt + scaffold dự án đầu tiên bằng loop init
├── 03-patterns/         ← (TODO) Kết hợp với loop/02-patterns (triage, sweeper, babysitter)
├── 04-savings/          ← (TODO) Đo token tiết kiệm, Loop Ready score tăng
└── 05-troubleshooting/  ← (TODO) Drift, gate false-positive, worktree conflicts
```

### Lộ Trình Đề Xuất

```
Bước 1: Đọc loop/07-tools/ trong nhánh loop/ để hiểu ecosystem
   ↓
Bước 2: loop init . --pattern daily-triage — scaffold dự án đầu tiên
   ↓
Bước 3: loop doctor . — xem top-3 next actions
   ↓
Bước 4: loop audit . — đo Loop Readiness ban đầu
   ↓
Bước 5: Thêm loop gate check vào CI để cưỡng chế cơ học
```

| Bạn muốn... | Đọc |
|-------------|-----|
| Hiểu ecosystem loop-* | [loop/07-tools](../../loop/07-tools/) |
| Hiểu loop concepts | [loop/01-concepts](../../loop/01-concepts/) |
| An toàn nhiều loop | [loop/03-safety](../../loop/03-safety/) + [loop/05-multi-loop](../../loop/05-multi-loop/) |
| Chống anti-patterns | [loop/06-anti-patterns](../../loop/06-anti-patterns/) |

## Case Studies Thực Tế

### 1. Từ Manual Loop → Loop Tooling

| Giai đoạn | Không có Loop CLI | Có Loop CLI |
|-----------|-------------------|-------------|
| Scaffold | Tạo tay STATE.md, LOOP.md, budgets (~30 phút) | `loop init .` (< 1 phút) |
| Chấm điểm | Không có cách đo | `loop audit` → score ~10→100 |
| Ngăn merge sai | Dựa vào agent đọc safety file | `loop gate` — cơ học, không bỏ lỡ |
| Nhiều attempt | Commit ồn ào lên main | `loop worktree` — cô lập từng attempt |
| Nhiều agents | Giẫm chân nhau | `loop-swarm` — byte-identical consensus |

### 2. Multi-Loop Coordination

```bash
# Developer A chạy loop trong worktree riêng
loop-worktree create --run-id fix-123 --pattern post-merge-cleanup

# Developer B chạy loop khác — lock tránh conflict
loop-worktree lock --scope refs/heads/main

# Cả hai kết thúc → gate check trước khi auto-merge
loop gate check --action auto-merge --paths src/,tests/
```

## Multi-Agent Loops Hiện Đại (2025) — Bối Cảnh

Loop CLI ở trên tập trung vào **vận hành loop đơn + đa loop an toàn**. Bên ngoài, hệ sinh thái multi-agent đã chuẩn hóa một số khái niệm nên biết để định vị loop-* đúng chỗ:

| Khái niệm | Là gì | Liên hệ với loop-* |
|-----------|-------|---------------------|
| **ReAct pattern** | Vòng Reason → Act → Observe lặp tới khi xong việc | Mỗi attempt trong `loop worktree` chính là một vòng ReAct có gác cổng |
| **Agent loop (OpenAI Agents SDK)** | Agent + Runner tự quản turn, tool call, handoffs | `loop init` scaffold chính là khung quanh một agent loop như vậy |
| **AutoGPT-style autonomous loops** | Agent tự chia mục tiêu thành task, chạy liên tục | `loop gate` + budget files chính là cơ chế giữ các loop kiểu này không chạy trôi |
| **A2A protocol (Google, 2025)** | Chuẩn mở cho agent ↔ agent giao tiếp, handoff qua server | `loop-swarm` consensus là một cách khắt khe hơn để agent trao đổi kết quả |

**Đọc thế nào**: các chuẩn này (OpenAI Agents SDK, A2A) định nghĩa *giao thức giữa các agent*; loop-* định nghĩa *kỷ luật vận hành quanh agent*. Hai tầng bổ sung cho nhau — khi nối loop-* với agent SDK bên ngoài, `loop gate` vẫn là điểm chặn cuối trước khi edits được merge.

Refs: [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/) · [A2A protocol](https://github.com/a2aproject/a2a)

## Tài Liệu Tham Khảo

### Nguồn Chính

- **Repo gốc**: https://github.com/cobusgreyling/loop-engineering
- **Ecosystem stack**: memory-engineering → loop-engineering → harness-foundry → outerloop → fleet-engineering
- **Companion**: [harness-foundry](https://github.com/cobusgreyling/harness-foundry), [outerloop](https://github.com/cobusgreyling/outerloop), [goal-engineering](https://github.com/cobusgreyling/goal-engineering)
- **OpenAI Agents SDK**: https://openai.github.io/openai-agents-python/ — agent loop + handoffs chuẩn 2025
- **A2A protocol**: https://github.com/a2aproject/a2a — chuẩn agent-to-agent (Google, 2025, đã donate cho Linux Foundation)
- **ReAct paper**: https://arxiv.org/abs/2210.03629

### Liên Kết Sang Nhánh Khác

- [loop/07-tools](../../loop/07-tools/) — Bảng đầy đủ các tool loop-* trong nhánh loop/
- [HARNESS_ENGINEERING.md](../../HARNESS_ENGINEERING.md) — Harness Runtime là gì
- [harness/10-automation](../../harness/10-automation/) — Automation component (loop gate, CI)

---

> **"A loop without a gate is a suggestion. A loop with a gate is a system."**

---

*Bài viết thuộc [AI Coding Skills Framework](../..) — nhánh Tools — loop-cli*