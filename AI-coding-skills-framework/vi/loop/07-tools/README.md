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

Giải nghĩa: **skills** = file chỉ dẫn cách làm việc cho agent; **budget file** = file ghi hạn mức token; **composable runtime stack** = bộ khung chạy có phiên bản, lắp ghép được với nhau.

> **Tóm gọn 1 câu:** `init` dựng khung loop cho repo (skills, state, ngân sách) và `doctor` khám sức khoẻ rồi chỉ ra 3 việc cần làm tiếp — hãy bắt đầu mọi dự án loop từ đây thay vì tự dựng tay.

---

## 2. loop-audit — Loop Readiness Score

> **Đọc sao cho dễ:** `audit` là "chấm điểm bài kiểm tra vận hành" — cho bạn con số 0–100 thể hiện mức sẵn sàng production. Giống điểm tín nhiệm tín dụng: điểm thấp thì khoan để loop tự chạy, điểm cao dần lên khi bạn dựng khung đúng cách.

> 📄 **Code ví dụ:** [`examples/02-2-loop-audit-loop-readiness-score.sh`](examples/02-2-loop-audit-loop-readiness-score.sh)

Chấm điểm **Loop Readiness** (L0→L3) cho project của bạn — con số chạy từ ~10 lên 100 khi bạn dựng khung đúng các phần. Gồm constraints, governance và **Harness Runtime** (v1.7). Giữ ở **L3** cho đến khi có `loop-budget.md`, `loop-run-log.md`, và mục budget trong LOOP.md.

Giải nghĩa: **L0→L3** = thang mức tự chủ, L0 là chưa chạy, L3 là tự chạy không cần người; **constraints** = các ràng buộc bắt buộc; **governance** = bộ quy tắc quản trị ai được phép làm gì.

> **Tóm gọn 1 câu:** `audit` là điểm 0–100 đo loop đã sẵn sàng chạy thật chưa — điểm cao mới dám mở mức tự chủ cao, và L3 chỉ mở khi đã đủ file ngân sách, nhật ký chạy, và mục ngân sách trong LOOP.md.

---

## 3. loop-cost — Ước Tính Token

> 📄 **Code ví dụ:** [`examples/03-3-loop-cost-uoc-tinh-token.sh`](examples/03-3-loop-cost-uoc-tinh-token.sh)

Ước lượng token spend **trước khi lên lịch chạy** — để không bất ngờ với bill tuần sau. Xem chi tiết budget rules trong [04-operating](../04-operating/).

> **Tóm gọn 1 câu:** `loop-cost` trả lời câu hỏi "loop này chạy mỗi ngày tốn bao nhiêu tiền" trước khi bạn đặt lịch, thay vì để hóa đơn cuối tuần tự trả lời.

---

## 4. loop-sync — Phát Hiện Drift

> 📄 **Code ví dụ:** [`examples/04-4-loop-sync-phat-hien-drift.sh`](examples/04-4-loop-sync-phat-hien-drift.sh)

Phát hiện lệch giữa `STATE.md` và `LOOP.md` — hai file mô tả trạng thái và cấu hình loop nhưng có thể lệch nhau dần theo thời gian.

Giải nghĩa: **drift** = hai bản ghi từng khớp nhau rồi từ từ khác đi, như đồng hồ bỏ lên sai mỗi ngày.

> **Tóm gọn 1 câu:** `loop-sync` là người so hai cuốn sổ — cấu hình trong `LOOP.md` và trạng thái trong `STATE.md` — và cảnh báo khi chúng kể hai chuyện khác nhau.

---

## 5. loop-context — Memory + Circuit Breaker

> 📄 **Code ví dụ:** [`examples/05-5-loop-context-memory-circuit-breaker.sh`](examples/05-5-loop-context-memory-circuit-breaker.sh)

Bộ nhớ có trạng thái và cầu dao tự ngắt cho các run dài. Giúp context không phình vô hạn qua nhiều vòng lặp.

Giải nghĩa: **circuit breaker** = cầu dao điện: khi ngữ cảnh (context) vượt ngưỡng thì tự ngắt thay vì để model bị "tràn" và trả lời loạn.

> **Tóm gọn 1 câu:** `loop-context` giữ cho ngữ cảnh của run dài không phình vô hạn — quá ngưỡng thì ngắt và chuyển người, giống cầu dao điện ngắt trước khi cháy.

---

## 6. loop-worktree — Cô Lập Thay Đổi

> **Đọc sao cho dễ:** `worktree` là "phòng thực hành riêng" cho mỗi lần thử fix — agent sửa trong phòng riêng, hỏng thì bỏ phòng đó, không ảnh hưởng tới code chính. Kèm thêm `lock/unlock` để các loop không vào cùng chỗ cùng lúc.

> 📄 **Code ví dụ:** [`examples/06-6-loop-worktree-co-lap-thay-oi.sh`](examples/06-6-loop-worktree-co-lap-thay-oi.sh)

Quản lý git worktree riêng cho mỗi lần thử fix — một worktree cho mỗi attempt, theo dõi trong manifest, dọn khi reject/escalate. Kèm `lock`/`unlock` cho multi-loop coordination (xem [05-multi-loop](../05-multi-loop/)).

Giải nghĩa: **manifest** = sổ theo dõi các worktree đang mở; **attempt** = một lượt thử sửa; **reject/escalate** = bỏ lượt thử hoặc chuyển cho người.

> **Tóm gọn 1 câu:** `loop-worktree` cho mỗi lượt thử fix một phòng riêng trong git — hỏng thì bỏ phòng, code chính không bị đụng — và `lock/unlock` để hai loop không cùng vào một phòng.

---

## 7. loop-gate — Cưỡng Chế Cơ Học

> 📄 **Code ví dụ:** [`examples/07-7-loop-gate-cuong-che-co-hoc.sh`](examples/07-7-loop-gate-cuong-che-co-hoc.sh)

Cưỡng chế **bằng máy** path denylist và auto-merge allowlist từ `gate.yaml` — không phụ thuộc vào việc loop có đọc file safety hay không. Exit `2` là escalate, `0` là proceed — cùng quy ước mà `loop-context --check` dùng, nên control scripts nối tiếp được cả hai.

Giải nghĩa: **gate.yaml** = file cấu hình ghi rõ đường dẫn nào cấm, đường dẫn nào được tự gộp; **exit code** = số lệnh trả về khi thoát (0 = được đi, 2 = cấm và chuyển người).

> **Tóm gọn 1 câu:** `loop-gate` là cổng duyệt bằng máy: nó chặn hành động sai đường dẫn dựa trên `gate.yaml`, không dựa vào "hy vọng model đọc đúng lời nhắc" — exit 0 là được đi, exit 2 là chuyển người.

---

## 8. loop-sandbox & loop-swarm — Cô Lập + Consensus

> 📄 **Code ví dụ:** [`examples/08-8-loop-sandbox-loop-swarm-co-lap-consensus.sh`](examples/08-8-loop-sandbox-loop-swarm-co-lap-consensus.sh)

- **loop-sandbox**: git worktree tách biệt tạm thời cho từng lượt chạy agent đơn lẻ. Gom changes thành patch files để review trước khi áp vào.
- **loop-swarm**: sandbox lấy đồng thuận từ nhiều agent qua các lượt `loop-sandbox` chạy nối tiếp. Chỉ chấp nhận edits khi các lượt cho ra patch **giống nhau từng byte**.

Giải nghĩa: **patch file** = file ghi lại phần code thay đổi, đọc được trước khi áp; **consensus (đồng thuận)** = nhiều agent cùng ra một kết quả thì mới tin.

> **Tóm gọn 1 câu:** `loop-sandbox` biến mỗi lượt chạy thành một bản vá đọc được trước khi áp, còn `loop-swarm` yêu cầu nhiều agent ra cùng một bản vá giống nhau từng byte mới chấp nhận — hai lớp an toàn chồng lên nhau.

---

## 9. Các Tool Khác

Cách đọc bảng này: mỗi dòng là một tool phụ trợ, cột "Mô tả" nói nó làm gì, cột "Lệnh" là cách chạy nó. Ví dụ, `loop-mcp-server` biến tài liệu patterns thành nguồn dữ liệu agent truy vấn được, thay vì phải nhồi cả đống văn bản vào prompt.

| Tool | Mô tả | Lệnh |
|------|-------|------|
| **loop-action** | GitHub Composite Action chạy loops trong CI | `uses: cobusgreyling/loop-engineering/tools/loop-action@main` |
| **loop-mcp-server** | Patterns/skills/state/budget/safety docs như MCP resources | `npx @cobusgreyling/loop-mcp-server` |
| **loop-cost** | Token spend estimator | `npx @cobusgreyling/loop-cost` |

Giải nghĩa: **GitHub Composite Action** = gói các bước CI đóng sẵn thành một action để gọi lại; **MCP resources** = dữ liệu agent đọc được qua chuẩn MCP.

**Reference MCP server**: repo có sẵn `tools/mcp-server/` — patterns, skills, state, budget, safety docs thành MCP resources truy vấn được lúc chạy (đỡ nhồi prompt). Ví dụ config: `examples/mcp/loop-engineering.mcp.json`.

> **Tóm gọn 1 câu:** Ba tool phụ trợ còn lại đưa loop vào CI, biến tài liệu thành nguồn truy vấn qua MCP, và ước chi phí — dùng khi cần, không bắt buộc.

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

Cách đọc bảng: sơ đồ trên là năm tầng xếp từ trái sang phải — memory (nhớ), loop (quy trình), runtime (khung chạy), govern (kiểm soát), fleet (quản cả đàn agent). Bảng dưới nói từng tầng cho bạn gì và lệnh bắt đầu. Ví dụ, tầng "Fleet" cho bạn registry (danh mục agent) và kill switch (nút dừng toàn bộ).

### Companion Projects

Cách đọc bảng: mỗi dòng là một dự án cùng nhà, cột mô tả cho biết nó bù phần nào cho loop-engineering. Ví dụ, Fleet Engineering quản cả đàn agent với nút dừng khẩn.

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

> **Tóm gọn 1 câu:** Thêm memory khi agent hay quên giữa các phiên, thêm fleet khi cả team có nhiều agent, và sau khi đạt Loop Ready 80+ thì đóng gói loop thành harness có phiên bản.

---

## Cập nhật 10/2026 — Alternative Toolchain & So Sánh

Phần này giải thích rằng các CLI `loop-*` chỉ là một cách chạy loop — còn có nhiều "bộ lên lịch" (scheduler) khác, và bảng dưới giúp bạn chọn đúng cỡ.

### So Sánh Loop Scheduling Approaches

Cách đọc bảng này: mỗi dòng là một cách lên lịch chạy loop, cột "Đặc điểm" nói mạnh yếu, cột "Phù hợp khi" nói dùng cho ai. Ví dụ, cron là cách đơn giản nhất; Temporal là cách chạy dài hạn mà dừng rồi chạy tiếp không mất dữ liệu.

| Approach | Đặc điểm | Phù hợp khi |
|----------|----------|-------------|
| **Shell script + cron** | Đơn giản nhất, no deps, chạy ngay trên máy bạn | Loop cá nhân, demo, môi trường đã có cron |
| **GitHub Actions** | Hosted, free tier, event-driven (cron + trigger theo PR/issue) | Loop gắn với repo, team nhỏ muốn zero infra |
| **Temporal** | Durable execution, checkpoint/resume native | Long-running agents — dừng/tiếp tục không mất state |
| **Airflow** | Data pipelines, DAG phức tạp, dependency graph | Pipeline dữ liệu/ML nhiều bước phụ thuộc nhau |
| **Python asyncio scheduler** (in-process) | Chạy trong cùng process với app | Hundreds of loops trong một service tự quản |

Giải nghĩa: **cron** = trình hẹn giờ có sẵn trên Linux/macOS; **hosted** = chạy trên máy chủ của dịch vụ, không tự lo hạ tầng; **durable execution** = chạy bền: dừng giữa chừng rồi tiếp tục không mất công việc đã làm; **checkpoint/resume** = lưu điểm dừng và chạy tiếp từ điểm đó; **DAG** = đồ thị các bước có hướng, bước sau đợi bước trước; **asyncio** = thư viện Python chạy nhiều việc song song trong một chương trình.

### Khi Nào Chọn Gì

- **Mỗi ngày 1–2 runs** → cron hoặc GitHub Actions là đủ, đừng phức tạp hoá.
- **Cần checkpoint/resume dài hạn** → Temporal — durable execution sinh ra cho việc này.
- **ML / data pipeline** → Airflow với DAG rõ ràng từng bước.
- **Hundreds of loops** → dedicated orchestrator (Kestra, Temporal, fleet-engineering).

> **📌 Lưu ý:** Các CLI `loop-*` giới thiệu ở trên hiện tại là **một lựa chọn**, không phải bắt buộc. Các pattern ở [02-patterns](../02-patterns/) chạy được trên **mọi scheduler** trong bảng ở trên — pattern là quy trình + metrics + safety gates, scheduler chỉ là cách thức kích hoạt.

> **Tóm gọn 1 câu:** Chọn scheduler theo cỡ bài toán — chạy ít lần dùng cron/GitHub Actions, chạy dài và cần dừng-tiếp dùng Temporal, pipeline dữ liệu dùng Airflow, hàng trăm loop mới cần orchestrator riêng.

### Xem Thêm

- [harness — 10. Automation](../../harness/10-automation/README.md) — scheduler patterns chi tiết.
- [AGENT_SYSTEM_ARCHITECTURE.md](../../AGENT_SYSTEM_ARCHITECTURE.md) — Layer 5 (automation trong tổng thể kiến trúc).

---

*Trở về [README](../README.md) — tổng quan Module XII*
