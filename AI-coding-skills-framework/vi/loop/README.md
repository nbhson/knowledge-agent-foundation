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

Tưởng tượng bạn mới thuê một anh đầu bếp. Ngày đầu anh ấy nấu hơi mặn — bạn nếm rồi góp ý *"bớt muối chút nhé"*.
Hôm sau anh ấy nêm vừa hơn nhưng lại nhạt vị ngọt — bạn lại nếm, lại góp ý. Tới ngày thứ ba thì món ăn gần như tròn vị.

Giờ thử đổi cảnh: mỗi bữa ăn bạn đều phải đứng kè kè trong bếp, đọc từng bước cho đầu bếp làm theo.
Vài hôm là đuối — mà đó lại đúng là cách nhiều người đang xài AI coding agent mỗi ngày:
**gõ prompt, ngồi chờ, đọc code, sửa prompt, gõ lại từ đầu.**

> *"You shouldn't be prompting coding agents anymore. You should be designing loops that prompt your agents."*
> — **Peter Steinberger**

> *"I don't prompt Claude anymore. I have loops running that prompt Claude and figuring out what to do. My job is to write loops."*
> — **Boris Cherny** (Head of Claude Code, Anthropic)

**Loop Engineering** nôm na là nghề thiết kế **bộ máy tự chạy** — bộ máy biết tự tìm việc cần làm, tự chia việc,
tự kiểm tra thành phẩm, tự giữ sổ sách — để bạn khỏi phải gõ từng câu lệnh. Điểm ăn tiền đã chuyển chỗ:
từ *viết prompt cho khéo* sang *vẽ vòng lặp cho khôn*.

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

Nói theo kiểu đời thường thì Loop Engineering giống **mở một xưởng nhỏ** — bạn không tự tay lắp từng con ốc;
bạn lo dây chuyền (scheduler), sắm máy móc (agents), đặt máy kiểm hàng (verifiers), dựng kho giữ đồ (state).
Còn **Cognitive Surrender** là lúc bạn đứng nhìn dây chuyền chạy vù vù mà quên mất mình mới là người vẽ ra nó,
thấy sai cũng không buồn sửa.

**Nếu không làm thế này**: bạn sẽ kẹt cả buổi trong cảnh gõ đi gõ lại cùng một kiểu prompt, agent thì ngã đúng
một cái hố hết lần này tới lần khác, token đốt tiền vô ích, mà cuối cùng chẳng đọng lại quy trình nào xài lại được.

## Tổng Quan

**Loop Engineering** là cách vẽ ra những **vòng lặp có nề nếp** để AI agent tự phát hiện việc, tự xắn tay làm,
tự soi lại kết quả, rồi tự khôn lên sau mỗi vòng — chạy đều theo lịch (cadence), kéo dài qua nhiều phiên (sessions),
với **cuốn sổ cái trạng thái** nằm ngoài bất kỳ đoạn chat nào, tắt máy mở lại vẫn còn.

So với Module VII (Workflow) chỉ lo xếp ngay ngắn một đường ống chạy một lần, Loop Engineering lo chuyện dài hơi hơn:
vòng lặp **tự nuôi sống chính nó** — agent làm xong một task chưa phải xong chuyện, nó còn phải **tự hỏi
việc nào đáng làm tiếp, tự kiểm hàng, rồi mang bài học đó qua vòng sau**.

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

Module XII được chẻ thành **từng file chuyên đề** cho dễ nhai từng miếng — cách chia này đi theo cấu trúc
tài liệu của repo `loop-engineering`:

```
loop/
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

Repo `loop-engineering` đem chính mấy pattern của mình ra xài trên thân mình, kiểu "nhà trồng được gì ăn nấy":

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

Repo có nguyên thư mục `stories/` ghi lại cả pha ăn mừng lẫn pha ngã sấp mặt — phần đáng tiền nhất để học khôn:

- **CI Sweeper: Infinite Flaky Test** — `stories/ci-sweeper-infinite-flaky-test.md`: bài học về việc không auto-fix flakes.
- **Why We Killed CI Sweeper** — `stories/why-we-killed-ci-sweeper.md`: khi nào kill một loop.
- **Score Climbs Then Budget Burns** — `stories/score-climbs-then-budget-burns.md`: token budget vượt khỏi tầm kiểm soát.
- **Multi-Loop Collision** — `stories/multi-loop-collision.md`: hai loops đánh nhau trên cùng branch.
- **The Verifier Problem** — `stories/quant-loop-the-verifier-problem.md`: verifier theater trong thực tế.

### 3. Example Implementations Theo Tool

Mỗi nhà một kiểu bếp, mỗi tool một cách chạy loop — mở đúng file ví dụ là thấy ngay cách làm:

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

Muốn vọc từng món thì ghé: [07-tools](07-tools/).

---

> **"Hệ thống tốt nhất không phải là hệ thống không bao giờ sai — mà là hệ thống sửa sai nhanh nhất."**

> *"Build the loop. But build it like someone who intends to stay the engineer, not just the person who presses go."* — Addy Osmani

---

*Bài viết thuộc [AI Coding Skills Framework](../..) — Module XII: Loop Engineering*
