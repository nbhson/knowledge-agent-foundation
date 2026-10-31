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

*Phần này giải vì sao cần bộ công cụ dòng lệnh cho loop. Loop = vòng lặp: agent chạy lặp đi lặp lại nhiều phiên cho tới khi xong việc.*

Hãy hình dung thế này: bạn đã dựng xong một harness chỉn chu trong `harness/` — đủ context, memory, guardrails, evaluation. Bạn cũng đã tin loop là cách vận hành đúng. Nhưng ngặt một nỗi là mỗi loop lại phải **dựng tay từ đầu**: tạo `STATE.md` (file trạng thái), `LOOP.md` (file cấu hình loop), budget files (file ngân sách token), safety config (cấu hình an toàn), worktree isolation (cách ly bản làm việc bằng git worktree)...

Có một nỗi đau thầm lặng ở đây: dự án mới nào bạn cũng **gõ lại cùng một bộ khung**, rồi thả cho các loop chạy tự do — không chấm điểm, không phát hiện drift (drift = trôi dần: nội dung file lệch khỏi thực tế sau thời gian dài), không có gate bắt buộc (gate = cổng chặn). Tới lúc nhiều loop chạy song song là chúng giẫm chân lên nhau ngay.

> *"Loops don't need to be hand-coded from scratch — there's an open-source CLI ecosystem supporting each phase."*

**Loop CLI** (`@cobusgreyling/loop-*`) là bộ công cụ dòng lệnh hiện thực hóa toàn bộ lý thuyết vòng lặp: từ init scaffold (dựng khung), chấm điểm readiness (điểm sẵn sàng), ước lượng token, phát hiện drift, đến cưỡng chế cơ học (chặn bằng code) và cô lập sandbox (chạy trong môi trường biệt lập).

> **Tóm gọn 1 câu:** Loop CLI thay việc dựng tay khung loop mỗi dự án bằng một bộ lệnh: init khung trong 1 phút, chấm điểm, đo tiền, chặn sai và cách ly khi chạy.

### Tại Sao Loop CLI Quan Trọng?

*Bốn lý do, mỗi dòng một tính năng. Ví dụ dòng 1: một lệnh init thay 30 phút tạo file thủ công.*

> **"A loop without tooling is a ritual. A loop with tooling is an engineering discipline."**

*Cách đọc bảng này: cột "Lý do" là tính năng, cột "Giải thích" là lệnh nào làm việc đó và ra sao.*

| # | Lý do | Giải thích |
|---|-------|------------|
| 1 | **Scaffold chuẩn hóa** | `loop init` tạo đúng cấu trúc skills/state/budget files — không còn "viết lại từ đầu" mỗi dự án |
| 2 | **Đo lường được** | `loop audit` chấm điểm Loop Readiness L0→L3; `loop cost` ước lượng token trước khi chạy |
| 3 | **Cưỡng chế cơ học** | `loop gate` enforce path denylist/allowlist từ config — không phụ thuộc việc agent có đọc safety file không |
| 4 | **An toàn đa loop** | `loop worktree` + `loop sandbox` cô lập từng attempt, `loop swarm` yêu cầu consensus trước khi chấp nhận edits |

*(Chú giải: attempt = một lần thử chạy; consensus = nhiều agent phải đồng ý giống nhau; enforce = cưỡng chế bằng code; denylist/allowlist = danh sách cấm/cho phép.)*

> **Tóm gọn 1 câu:** Loop CLI biến loop từ nghi thức tự giác thành kỷ luật đo được: khung chuẩn, điểm số, cổng chặn cứng, và cách ly giữa các lần chạy.

### Quan Hệ Với Harness

*Phần này định vị Loop CLI giữa hai nhánh kiến thức trong repo, rồi đối chiếu từng lệnh với module harness.*

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

*(Chú giải: Harness Runtime = khả năng chạy thật của hệ thống; MCP protocol = chuẩn kết nối công cụ.)*

> **Tóm gọn 1 câu:** harness/ dạy lý thuyết, loop/ dạy cách vận hành, còn Loop CLI là công cụ chạy thật — mỗi lệnh tương ứng một module harness.

## Tổng Quan Các Lệnh

*Nine lệnh chia theo nhóm việc: dựng khung, đo lường, chặn sai, cách ly. Mỗi mục một lệnh, kèm code ví dụ.*

### 1. Front Door — `loop init / doctor / status`

*Bộ lệnh mở cửa: init dựng khung, doctor soi lỗi, status xem tình trạng.*

> 📄 **Code ví dụ:** [`examples/01-1-front-door-loop-init-doctor-status.sh`](examples/01-1-front-door-loop-init-doctor-status.sh)

`loop init` dựng sẵn skills + state + budget files rồi in ra **Loop Ready score** kèm lệnh loop đầu tiên để bạn chạy thử. `loop doctor` gom audit + sync + file checks thành **top-3 việc nên làm tiếp theo**. Muốn đổi tool thì chỉnh `--tool` sang `claude`, `codex` hoặc `opencode`.

> **Tóm gọn 1 câu:** Ba lệnh đầu tiên luôn là: `loop init` (dựng khung), `loop doctor` (3 việc cần làm), `loop status` (xem tình trạng).

### 2. `loop audit` — Loop Readiness Score

*Lệnh chấm điểm độ sẵn sàng của vòng lặp. Càng chuẩn càng nhiều điểm.*

> 📄 **Code ví dụ:** [`examples/02-2-loop-audit-loop-readiness-score.sh`](examples/02-2-loop-audit-loop-readiness-score.sh)

Chấm **Loop Readiness** (L0→L3) — scaffold càng chuẩn thì điểm càng nhích dần từ ~10 lên 100. Chấm cả constraints + governance + **Harness Runtime** (v1.7). Muốn chạm **L3** thì cần có đủ `loop-budget.md`, `loop-run-log.md` và budget section trong LOOP.md.

*(Chú giải: constraints = ràng buộc an toàn; governance = cơ chế quản trị như nhật ký, ngân sách.)*

> **Tóm gọn 1 câu:** `loop audit` cho bạn một con số biết loop đã đủ kỷ luật chưa — muốn L3 phải có đủ file ngân sách và nhật ký.

### 3. `loop cost` — Ước Lượng Token

*Lệnh đoán chi phí trước khi chạy, để khỏi giật mình nhìn hóa đơn.*

> 📄 **Code ví dụ:** [`examples/03-3-loop-cost-uoc-luong-token.sh`](examples/03-3-loop-cost-uoc-luong-token.sh)

Áng chừng token sẽ tốn **trước khi bạn đặt lịch chạy** — để tuần sau khỏi giật mình nhìn bill.

> **Tóm gọn 1 câu:** `loop cost` = máy tính tiền chạy trước: cho mẫu, tần suất, mức độ — nhận con số token dự kiến.

### 4. `loop sync` — Phát Hiện Drift

*Lệnh so hai file trạng thái để bắt chỗ lệch nhau (drift = trôi dần khỏi thực tế).*

> 📄 **Code ví dụ:** [`examples/04-4-loop-sync-phat-hien-drift.sh`](examples/04-4-loop-sync-phat-hien-drift.sh)

Soi chỗ lệch giữa `STATE.md` và `LOOP.md` — hai file này chạy một thời gian là rất dễ trôi khỏi nhau.

> **Tóm gọn 1 câu:** `loop sync` chỉ ra chỗ hai file trạng thái đã lệch nhau — chạy định kỳ để phát hiện trôi sớm.

### 5. `loop context` — Memory + Circuit Breaker

*Lệnh quản lý bộ nhớ làm việc và ngắt khi quá tải.*

> 📄 **Code ví dụ:** [`examples/05-5-loop-context-memory-circuit-breaker.sh`](examples/05-5-loop-context-memory-circuit-breaker.sh)

Một memory manager có trạng thái kèm circuit breaker cho các run dài hơi. Hiểu đơn giản là giữ cho context khỏi phình vô hạn sau nhiều vòng lặp.

*(Chú giải: circuit breaker = cầu chì tự ngắt — khi context quá dài thì cắt bớt thay vì để tràn.)*

> **Tóm gọn 1 câu:** `loop context` giữ bộ nhớ agent gọn qua nhiều vòng — có cầu chì tự ngắt khi context sắp tràn.

### 6. `loop worktree` — Cô Lập Thay Đổi

*Lệnh cho mỗi lần chạy một bản làm việc git riêng, khỏi đè lên nhau.*

> 📄 **Code ví dụ:** [`examples/06-6-loop-worktree-co-lap-thay-oi.sh`](examples/06-6-loop-worktree-co-lap-thay-oi.sh)

Đứng ra quản lý các git worktree cách ly (worktree = một bản sao thư mục làm việc của repo, gắn với nhánh riêng) — mỗi attempt một worktree riêng, theo dõi qua manifest, xong việc (reject/escalate) thì dọn. Có kèm `lock`/`unlock` để nhiều loop khỏi giành nhau.

> **Tóm gọn 1 câu:** `loop worktree` mỗi lần thử một nhánh riêng, xong (hoặc bị từ chối) thì dọn — nhiều loop chạy song song không đè lên nhau.

### 7. `loop gate` — Cưỡng Chế Cơ Học

*Lệnh chặn bằng code những thay đổi nằm ngoài vùng cho phép.*

> 📄 **Code ví dụ:** [`examples/07-7-loop-gate-cuong-che-co-hoc.sh`](examples/07-7-loop-gate-cuong-che-co-hoc.sh)

Bắt buộc **bằng cơ chế** path denylist + auto-merge allowlist đọc từ `gate.yaml`. Exit `2` là escalate (leo thang — cần người quyết), `0` là cho đi tiếp — cùng convention với `loop-context --check` nên bạn chain chúng lại được (chain = nối chuỗi các lệnh, lệnh sau chỉ chạy khi lệnh trước cho qua).

> **Tóm gọn 1 câu:** `loop gate` là chốt chặn bằng code: sai đường dẫn từ gate.yaml là bị giữ lại — không phụ thuộc agent có "tự giác" hay không.

### 8. `loop sandbox` & `loop swarm` — Cô Lập + Consensus

*Hai lệnh cho môi trường nhiều agent: một cái cách ly thay đổi, một cái bắt đồng thuận.*

> 📄 **Code ví dụ:** [`examples/08-8-loop-sandbox-loop-swarm-co-lap-consensus.sh`](examples/08-8-loop-sandbox-loop-swarm-co-lap-consensus.sh)

- **loop-sandbox**: bắt changes thành reviewable patch files trước khi apply (patch file = file ghi lại các thay đổi, xem được trước khi áp).
- **loop-swarm**: multi-agent consensus — yêu cầu **byte-identical patch consensus** giữa các runs (byte-identical = giống hệt nhau từng byte; tức là mọi agent phải ra kết quả y hệt nhau mới được chấp nhận).

> **Tóm gọn 1 câu:** sandbox biến thay đổi thành file vá chờ duyệt; swarm đòi các agent ra kết quả giống hệt nhau từng byte trước khi nhận.

### 9. Loop MCP Server

*Lệnh mở tài liệu loop thành tài nguyên MCP để agent đọc khi cần, khỏi nhét hết vào prompt.*

> 📄 **Code ví dụ:** [`examples/09-9-loop-mcp-server.sh`](examples/09-9-loop-mcp-server.sh)

Patterns/skills/state/budget/safety docs như MCP resources — giảm prompt stuffing (prompt stuffing = nhét quá nhiều chữ vào prompt, tốn token và loãng ý). Reference config: `examples/mcp/loop-engineering.mcp.json`.

> **Tóm gọn 1 câu:** Loop MCP Server để agent "mở tài liệu đọc khi cần" thay vì dồn hết vào prompt — nhẹ hơn và rẻ hơn.

## Lộ Trình Học (Cấu Trúc Thư Mục)

*Bản đồ thư mục và thứ tự học. Chữ (TODO) nghĩa là mục còn bỏ trống.*

```
loop-cli/
├── README.md            ← BẠN ĐANG Ở ĐÂY — tổng quan + lộ trình
├── 01-concepts/         ← (TODO) Kiến trúc loop-*: plugin system, run ledger, state files
├── 02-setup/            ← (TODO) Cài đặt + scaffold dự án đầu tiên bằng loop init
├── 03-patterns/         ← (TODO) Kết hợp với loop/02-patterns (triage, sweeper, babysitter)
├── 04-savings/          ← (TODO) Đo token tiết kiệm, Loop Ready score tăng
└── 05-troubleshooting/  ← (TODO) Drift, gate false-positive, worktree conflicts
```

*(Chú giải: run ledger = sổ ghi từng lần chạy; triage = phân loại việc theo mức ưu tiên; sweeper/babysitter = các mẫu loop dọn dẹp / trông chừng; false-positive = chặn oan.)*

### Lộ Trình Đề Xuất

*Năm bước từ hiểu hệ sinh thái tới có gate trong CI.*

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

*Cách đọc bảng này: cột trái là điều bạn muốn làm, cột phải là tài liệu nên mở.*

| Bạn muốn... | Đọc |
|-------------|-----|
| Hiểu ecosystem loop-* | [loop/07-tools](../../loop/07-tools/) |
| Hiểu loop concepts | [loop/01-concepts](../../loop/01-concepts/) |
| An toàn nhiều loop | [loop/03-safety](../../loop/03-safety/) + [loop/05-multi-loop](../../loop/05-multi-loop/) |
| Chống anti-patterns | [loop/06-anti-patterns](../../loop/06-anti-patterns/) |

> **Tóm gọn 1 câu:** Đi theo 5 bước: hiểu ecosystem → init dự án đầu → doctor nhận việc cần làm → audit lấy điểm → cắm gate vào CI.

## Case Studies Thực Tế

*Hai tình huống thật: so lúc có và không có tooling, và phối hợp nhiều loop.*

### 1. Từ Manual Loop → Loop Tooling

*Cách đọc bảng này: so từng giai đoạn — cột giữa là cách làm thủ công, cột phải là cách làm bằng Loop CLI. Ví dụ, dòng Scaffold: 30 phút tạo tay rút còn dưới 1 phút.*

| Giai đoạn | Không có Loop CLI | Có Loop CLI |
|-----------|-------------------|-------------|
| Scaffold | Tạo tay STATE.md, LOOP.md, budgets (~30 phút) | `loop init .` (< 1 phút) |
| Chấm điểm | Không có cách đo | `loop audit` → score ~10→100 |
| Ngăn merge sai | Dựa vào agent đọc safety file | `loop gate` — cơ học, không bỏ lỡ |
| Nhiều attempt | Commit ồn ào lên main | `loop worktree` — cô lập từng attempt |
| Nhiều agents | Giẫm chân nhau | `loop-swarm` — byte-identical consensus |

### 2. Multi-Loop Coordination

*Tình huống: nhiều loop phối hợp trong một dự án — ai làm phần nào, chặn nhau ở đâu.*

> 📄 **Code ví dụ:** [`examples/10-2-multi-loop-coordination.sh`](examples/10-2-multi-loop-coordination.sh)

> **Tóm gọn 1 câu:** Bảng trên là bằng chứng tăng từng giai đoạn — công cụ hóa loop rút ngắn thời gian và thay "lời hứa an toàn" bằng cổng chặn cứng.

## Multi-Agent Loops Hiện Đại (2025) — Bối Cảnh

*Phần này đặt Loop CLI cạnh các chuẩn multi-agent bên ngoài để bạn biết nó đứng ở đâu.*

Loop CLI ở trên tập trung vào **vận hành loop đơn + đa loop an toàn**. Bên ngoài, hệ sinh thái multi-agent đã chuẩn hóa một số khái niệm nên biết để định vị loop-* đúng chỗ:

*Cách đọc bảng này: cột "Khái niệm" là thuật ngữ thịnh hành, cột "Là gì" giải thích ngắn, cột "Liên hệ với loop-*" nối nó với lệnh cụ thể. Ví dụ, ReAct = vòng nghĩ → làm → quan sát lặp lại, chính là một attempt trong loop worktree.*

| Khái niệm | Là gì | Liên hệ với loop-* |
|-----------|-------|---------------------|
| **ReAct pattern** | Vòng Reason → Act → Observe lặp tới khi xong việc | Mỗi attempt trong `loop worktree` chính là một vòng ReAct có gác cổng |
| **Agent loop (OpenAI Agents SDK)** | Agent + Runner tự quản turn, tool call, handoffs | `loop init` scaffold chính là khung quanh một agent loop như vậy |
| **AutoGPT-style autonomous loops** | Agent tự chia mục tiêu thành task, chạy liên tục | `loop gate` + budget files chính là cơ chế giữ các loop kiểu này không chạy trôi |
| **A2A protocol (Google, 2025)** | Chuẩn mở cho agent ↔ agent giao tiếp, handoff qua server | `loop-swarm` consensus là một cách khắt khe hơn để agent trao đổi kết quả |

*(Chú giải: handoff = chuyển việc cho agent khác; turn = một lượt hội thoại.)*

**Đọc thế nào**: các chuẩn này (OpenAI Agents SDK, A2A) định nghĩa *giao thức giữa các agent*; loop-* định nghĩa *kỷ luật vận hành quanh agent*. Hai tầng bổ sung cho nhau — khi nối loop-* với agent SDK bên ngoài, `loop gate` vẫn là điểm chặn cuối trước khi edits được merge.

Refs: [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/) · [A2A protocol](https://github.com/a2aproject/a2a)

> **Tóm gọn 1 câu:** Các chuẩn bên ngoài lo giao tiếp giữa các agent; loop-* lo kỷ luật vận hành — nối được với nhau và gate vẫn là chốt chặn cuối.

## Tài Liệu Tham Khảo

*Link gốc và các repo liên quan của hệ sinh thái loop.*

### Nguồn Chính

- **Repo gốc**: https://github.com/cobusgreyling/loop-engineering
- **Ecosystem stack**: memory-engineering → loop-engineering → harness-foundry → outerloop → fleet-engineering
- **Companion**: [harness-foundry](https://github.com/cobusgreyling/harness-foundry), [outerloop](https://github.com/cobusgreyling/outerloop), [goal-engineering](https://github.com/cobusgreyling/goal-engineering)
- **OpenAI Agents SDK**: https://openai.github.io/openai-agents-python/ — agent loop + handoffs chuẩn 2025
- **A2A protocol**: https://github.com/a2aproject/a2a — chuẩn agent-to-agent (Google, 2025, đã donate cho Linux Foundation)
- **ReAct paper**: https://arxiv.org/abs/2210.03629

### Liên Kết Sang Nhánh Khác

*Cách đọc: mỗi dòng là tài liệu liên quan, sau gạch ngang là lý do nên mở nó.*

- [loop/07-tools](../../loop/07-tools/) — Bảng đầy đủ các tool loop-* trong nhánh loop/
- [HARNESS_ENGINEERING.md](../../HARNESS_ENGINEERING.md) — Harness Runtime là gì
- [harness/10-automation](../../harness/10-automation/) — Automation component (loop gate, CI)

> **Tóm gọn 1 câu:** Repo gốc là loop-engineering trên GitHub; tài liệu hệ sinh thái đầy đủ nằm ở loop/07-tools và HARNESS_ENGINEERING.md.

---

> **"A loop without a gate is a suggestion. A loop with a gate is a system."**

---

*Bài viết thuộc [AI Coding Skills Framework](../..) — nhánh Tools — loop-cli*