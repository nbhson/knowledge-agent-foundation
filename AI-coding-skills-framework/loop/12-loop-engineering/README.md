# 🔄 XII. Loop Engineering

> ## 📑 Mục Lục
>
> - [Câu Chuyện Mở Đầu](#câu-chuyện-mở-đầu)
> - [Tại Sao Loop Engineering Quan Trọng?](#tại-sao-loop-engineering-quan-trọng)
> - [Tổng Quan](#tổng-quan)
> - [Lộ Trình Học (Cấu Trúc Thư Mục)](#lộ-trình-học-cấu-trúc-thư-mục)
> - [Case Studies Thực Tế](#case-studies-thực-tế)
> - [Tài Liệu Tham Khảo](#tài-liệu-tham-khảo)

---

### Câu Chuyện Mở Đầu

Bạn thuê một đầu bếp mới. Ngày đầu tiên, anh ta nấu món — bạn nếm, nói *"Quá mặn"*. Ngày hôm sau, anh ta nấu lại — bạn nếm, nói *"Ít mặn hơn nhưng thiếu ngọt"*. Ngày thứ ba, món ăn gần như hoàn hảo.

Giờ hãy tưởng tượng bạn phải đứng bếp **từng bữa ăn**, thì thầm từng hướng dẫn cho đầu bếp. Bạn sẽ kiệt sức — và đó chính là cách hầu hết mọi người đang dùng AI coding agents: **gõ prompt, chờ, đọc, sửa prompt, gõ lại.**

> *"You shouldn't be prompting coding agents anymore. You should be designing loops that prompt your agents."*
> — **Peter Steinberger**

> *"I don't prompt Claude anymore. I have loops running that prompt Claude and figuring out what to do. My job is to write loops."*
> — **Boris Cherny** (Head of Claude Code, Anthropic)

**Loop Engineering** là kỹ thuật thiết kế **hệ thống điều khiển** — hệ thống tự phát hiện việc cần làm, tự giao việc, tự kiểm chứng, và tự duy trì trạng thái — thay vì bạn phải gõ từng prompt. Điểm đòn bẩy (leverage point) đã dịch chuyển: từ *viết prompt* sang *thiết kế vòng lặp*.

### Tại Sao Loop Engineering Quan Trọng?

> **"Stop prompting. Design the loop. Get a score."**

#### 3 Bằng Chứng Khoa Học & Thực Tiễn

| # | Nghiên Cứu / Nguồn | Phát Hiện Quan Trọng |
|---|-------------------|----------------------|
| 1 | **DeepMind (2025)** | Agents với structured feedback loops giảm **52% lỗi lặp lại** so với agents không có loop |
| 2 | **Anthropic (2025)** | Self-refine loops trong Claude Code tăng **38% code quality** trên benchmark SWE-bench |
| 3 | **loop-engineering (Cobus Greyling, 2026)** | Repo reference tự dogfood: `loop-audit` workflow chấm **Loop Ready score** trên mọi PR/push, đạt 5.5k+ GitHub stars trong 6 tháng |

#### Triết lý cốt lõi:

```
Loop Engineering = Thiết kế hệ thống điều khiển → Tự phát hiện + Tự kiểm chứng → Điểm sẵn sàng (Score) tăng
```

**Phân biệt quan trọng:**

```
Prompting     = Bạn gõ từng lệnh, agent làm từng việc
Harness       = Môi trường 1 agent chạy (tools, context, permissions)
Loop          = Harness + schedule + state + verification chain (chạy nhiều lần, tự duy trì)
```

**Analogies**: Loop Engineering giống **nhà máy sản xuất** — bạn không tự lắp ráp từng sản phẩm; bạn thiết kế dây chuyền (scheduler), máy móc (agents), thiết bị kiểm định (verifiers), và kho lưu trữ (state). Còn **Cognitive Surrender** là khi bạn đứng nhìn dây chuyền chạy mà quên mất mình là người thiết kế nó.

**Nếu bỏ qua**: Bạn dành hàng giờ gõ prompt lặp đi lặp lại, agent lặp lại cùng một sai lầm, token lãng phí, và không bao giờ có hệ thống tái sử dụng được.

## Tổng Quan

**Loop Engineering** là việc thiết kế các **vòng lặp có cấu trúc** để AI agent tự phát hiện công việc, tự thực thi, tự kiểm chứng, và tự cải thiện — trên nhịp (cadence) định kỳ, qua nhiều phiên (sessions), với **trạng thái bền vững** nằm ngoài bất kỳ cuộc hội thoại nào.

Khác với Module VII (Workflow) vốn tổ chức một pipeline, Loop Engineering tập trung vào **vòng lặp tự duy trì**: agent không chỉ chạy xong một task, mà còn **quyết định task nào đáng làm, kiểm chứng kết quả, và học từ kết quả** cho lần chạy sau.

```
┌─────────────────────────────────────────────────────────────────────┐
│                        LOOP ENGINEERING                              │
│                                                                     │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │               NĂM BUILDING BLOCKS + MEMORY                     │  │
│  │  Automations · Worktrees · Skills · MCP · Sub-agents + State  │  │
│  └───────────────────────────────────────────────────────────────┘  │
│       │                                                            │
│       ▼                                                            │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │              ANATOMY OF A LOOP                                 │  │
│  │  Schedule → Triage → State → Worktree → Implementer → Verifier│  │
│  │  → MCP → Human Gate → Commit/PR/Escalate                       │  │
│  └───────────────────────────────────────────────────────────────┘  │
│       │                                                            │
│       ▼                                                            │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │              AUTONOMY LEVELS                                   │  │
│  │  L1 Report ──► L2 Assisted ──► L3 Unattended                   │  │
│  └───────────────────────────────────────────────────────────────┘  │
│       │                                                            │
│       ▼                                                            │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │              SAFETY + OPERATING                                │  │
│  │  Denylist · Auto-merge policy · Human gates · Token budget     │  │
│  └───────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

## Lộ Trình Học (Cấu Trúc Thư Mục)

Module XII được chia thành **các file chuyên đề** để dễ học theo từng phần — tương ứng cấu trúc tài liệu của repo `loop-engineering`:

```
12-loop-engineering/
├── README.md            ← BẠN ĐANG Ở ĐÂY — tổng quan + lộ trình + case studies
├── 01-concepts/         ← Khái niệm: 5 building blocks, anatomy, L1-L3, taxonomy
├── 02-patterns/         ← 7 production patterns, mỗi pattern một file
│   ├── README.md        ←   Pattern picker + bảng tổng hợp
│   ├── daily-triage.md
│   ├── pr-babysitter.md
│   ├── ci-sweeper.md
│   ├── dependency-sweeper.md
│   ├── changelog-drafter.md
│   ├── post-merge-cleanup.md
│   └── issue-triage.md
├── 03-safety/           ← Loop Design Checklist + Safety & Guardrails
├── 04-operating/        ← Budget, logging, metrics, khi nào pause/kill
├── 05-multi-loop/       ← Phối hợp khi chạy nhiều loops
├── 06-anti-patterns/    ← 10 anti-patterns + failure mode catalog
└── 07-tools/            ← loop-init, loop-audit, loop-cost, ... + ecosystem
```

> Mỗi thư mục chứa một `README.md` — đồng nhất với convention của `harness/` (mỗi module là `NN-name/README.md`).

### Lộ Trình Đề Xuất

```
Bước 1: Đọc README.md này để hiểu bối cảnh
   ↓
Bước 2: 01-concepts/ — nắm 5 building blocks + anatomy + L1-L3
   ↓
Bước 3: 02-patterns/ — chọn pattern đầu tiên (gợi ý: Daily Triage L1)
   ↓
Bước 4: 03-safety/ — loop design checklist + guardrails
   ↓
Bước 5: 04-operating/ — budget + logging trước khi schedule thật
   ↓
Bước 6: 05-multi-loop/ + 06-anti-patterns/ — khi mở rộng nhiều loops
   ↓
Bước 7: 07-tools/ — dùng CLI scaffold, audit, giám sát
```

| Bạn muốn... | Đọc |
|-------------|-----|
| Hiểu loop là gì, các nguyên khối | [01-concepts](01-concepts/) |
| Chọn loop nào để bắt đầu | [02-patterns](02-patterns/) — pattern picker |
| Triển khai Daily Triage từ đầu | [02-patterns/daily-triage.md](02-patterns/daily-triage.md) |
| Kiểm tra loop đã sẵn sàng production chưa | [03-safety](03-safety/) — checklist §1–§10 |
| Ngăn loop phá production | [03-safety](03-safety/) — denylist, auto-merge, human gates |
| Kiểm soát token cost | [04-operating](04-operating/) — budget + run log |
| Chạy nhiều loops không đánh nhau | [05-multi-loop](05-multi-loop/) |
| Tránh các sai lầm đắt giá | [06-anti-patterns](06-anti-patterns/) |
| Dùng CLI scaffold/audit | [07-tools](07-tools/) |

---

## Case Studies Thực Tế

### 1. Repo Reference — Eat Its Own Dogfood

Repo `loop-engineering` chạy chính các pattern của mình trên chính nó:

| Loop | Level | Automation | Notes |
|------|-------|------------|-------|
| Daily Triage | L1 | ✅ `daily-triage.yml` | Weekdays; updates `STATE.md` + `loop-run-log.md` |
| Changelog Drafter | L1 | ✅ `changelog-drafter.yml` | Mondays; mở release-prep issue |
| Star History | L1 | ✅ `update-star-history.yml` | Daily; auto-PR |
| Validate + Audit | L1 | ✅ `validate-patterns.yml`, `audit.yml` | Readiness score trên PRs |
| Dependabot | L1 | ✅ `.github/dependabot.yml` | Weekly npm + Actions |
| PR Babysitter | L2 | ⏸ Manual | Worktrees cho fixes; verifier required |
| Dependency Sweeper | L2 | ⏸ Dependabot only | Patch-only |
| CI Sweeper | L2 | ⏸ Partial | Reacts qua failing validate/audit |

### 2. Stories Thực Tế (Thắng Và Thất Bại Trung Thực)

Repo có thư mục `stories/` ghi cả wins lẫn failures — bài học quý nhất:

- **CI Sweeper: Infinite Flaky Test** — `stories/ci-sweeper-infinite-flaky-test.md`: bài học về việc không auto-fix flakes.
- **Why We Killed CI Sweeper** — `stories/why-we-killed-ci-sweeper.md`: khi nào kill một loop.
- **Score Climbs Then Budget Burns** — `stories/score-climbs-then-budget-burns.md`: token budget vượt khỏi tầm kiểm soát.
- **Multi-Loop Collision** — `stories/multi-loop-collision.md`: hai loops đánh nhau trên cùng branch.
- **The Verifier Problem** — `stories/quant-loop-the-verifier-problem.md`: verifier theater trong thực tế.

### 3. Example Implementations Theo Tool

- **Grok**: `/loop 1d Run loop-triage. Update STATE.md.` — `examples/grok/daily-triage.md`
- **Claude Code**: `/loop 1d Run $loop-triage...report only` — `examples/claude-code/`
- **Codex**: Automations tab, daily prompt + Triage inbox — `examples/codex/`
- **Opencode**: CLI-first loops: cron/systemd + `opencode run`, skills, worktrees — `examples/opencode/`
- **GitHub Actions**: event-driven CI sweeper — `examples/github-actions/`

---

## Tài Liệu Tham Khảo

### Bài Viết & Nguồn

- [Cobus Greyling — Loop Engineering (Substack)](https://cobusgreyling.substack.com/p/loop-engineering) — khái niệm, primitives, Grok mapping
- [Addy Osmani — Loop Engineering](https://addyosmani.com/blog/loop-engineering/) — "Build the loop like someone who intends to stay the engineer"
- [loop-engineering — GitHub](https://github.com/cobusgreyling/loop-engineering) — reference repo, patterns, starters, tools
- [Goal Engineering](https://github.com/cobusgreyling/goal-engineering) — loops phát hiện, goals hoàn thành
- [Memory Engineering](https://github.com/cobusgreyling/memory-engineering) — ngừng giải thích lại repo
- [Harness Foundry](https://github.com/cobusgreyling/harness-foundry) — versioned runtime stack
- [Outerloop](https://github.com/cobusgreyling/outerloop) — evidence → verdict → answerability
- [Fleet Engineering](https://github.com/cobusgreyling/fleet-engineering) — quản trị population agents

### Frameworks & Tools

- **loop** (front door) — `npx @cobusgreyling/loop init | doctor | status | audit | cost`
- **loop-audit** — Loop Readiness Score CLI
- **loop-cost** — token spend estimator
- **loop-sync** — drift detection giữa STATE.md và LOOP.md
- **loop-context** — stateful memory + circuit breaker
- **loop-worktree** — isolated worktree management
- **loop-gate** — mechanical denylist + auto-merge enforcement
- **loop-sandbox / loop-swarm** — ephemeral isolation + consensus
- **loop-mcp-server** — patterns/skills/state/budget như MCP resources

Chi tiết từng tool: [07-tools](07-tools/).

---

> **"Hệ thống tốt nhất không phải là hệ thống không bao giờ sai — mà là hệ thống sửa sai nhanh nhất."**

> *"Build the loop. But build it like someone who intends to stay the engineer, not just the person who presses go."* — Addy Osmani

---

*Bài viết thuộc [AI Coding Skills Framework](../..) — Module XII: Loop Engineering*
