# 🔬 01. Khái Niệm Cốt Lõi — Loop Engineering

> Phần này kể cho bạn nghe **Loop Engineering thực ra là gì**, gồm **5 mảnh ghép + memory** nào ráp thành mọi vòng loop, một vòng loop chạy qua những trạm nào, các **mức tự chủ L1–L3**, và cách **mấy vòng loop lồng vào nhau**. Nếu chưa đọc thì ghé [README.md](../README.md) trước để có bức tranh chung nhé.

---

## 1. Loop Engineering Là Gì?

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Loop Engineering là cách bạn thiết kế **hệ điều khiển** cho AI coding agents — để nó tự biết việc ở đâu, tự chia việc, tự kiểm tra lại, tự nhớ trạng thái — chứ bạn không phải ngồi gõ từng prompt một.
> **Ẩn dụ/so sánh:** Cứ hình dung một **xưởng may thay vì một bác thợ may**: bác thợ thì tự cắt từng cái áo; còn chủ xưởng thì dựng băng chuyền (scheduler), sắm máy móc (agents), đặt khâu kiểm hàng (verifiers), thuê kho giữ vải (state). Bạn chuyển từ vai bác thợ sang vai người dựng xưởng.
> **Vì sao quan trọng:** Gõ prompt tay thì vui lúc đầu nhưng nhanh đuối — vì mọi việc đều chờ bạn ra lệnh. Có loop, agent cứ thế làm đều tay, còn bạn chỉ xuất hiện ở mấy ngã ba cần mình gật đầu (human gates).

### 1.1 Từ Prompt Đến Loop

Cách xài AI coding agent quen thuộc hiện nay là kiểu *gõ prompt theo hứng*: mở agent lên, gõ một câu, chờ nó trả lời. Xong việc là xong, lần sau lại bắt đầu từ con số 0 — không nhớ gì, không lưu gì, cũng chẳng có ai kiểm tra lại cho tử tế.

Loop Engineering rẽ sang hướng khác hẳn:

```
AD-HOC PROMPTING:
  Bạn ──prompt──► Agent ──kết quả──► Bạn (đọc, đánh giá)
  Bạn ──prompt──► Agent ──kết quả──► Bạn (đọc, đánh giá)
  ... lặp lại vô tận, không hệ thống

LOOP ENGINEERING:
  Scheduler ──fire──► Triage Skill ──đọc/write──► STATE / Memory
       │                                              │
       ▼                                              ▼
  Isolated Worktree ◄──── Implementer ──patch──► Verifier
       │                                              │
       ▼                                              ▼
  MCP / Git / Tickets ◄──── Human Gate? ──► Commit / PR / Escalate
```

**Vai của bạn cũng đổi theo**: trước đây bạn là *người gõ prompt*, giờ bạn thành *người thiết kế vòng lặp*. Bạn viết skill (gom kiến thức lại), vẽ sẵn khung state, chọn nhịp chạy, và giữ cho mình quyền chốt ở mấy **cửa kiểm tra của con người**.

### 1.2 Harness vs Loop

Chỗ này nhiều bạn hay lẫn lộn, nên mình tách bạch một chút. Harness và Loop là hai thứ khác nhau:

```
Harness = single session setup
  → tools, context, permissions, rules mà MỘT agent có trong MỘT phiên

Loop    = harness + schedule + state + verification chain
  → hệ thống điều phối NHIỀU harness runs theo thời gian
```

Mấy module VII–XI trong framework này lo dựng từng món đồ trong harness. Còn module XII này (loop) lo **xếp chúng chạy đều theo thời gian**: khi nào chạy, nhớ gì qua mỗi lần chạy, và ai kiểm tra chéo ai.

### 1.3 Loop Là Một Recursive Goal

Nói gọn, một loop là một **mục tiêu biết tự lặp lại**: bạn nói rõ "đích đến là gì", rồi để agent tự xoay vòng (nhờ sub-agents và trí nhớ ngoài) cho tới khi **xong việc hoặc biết đường nhờ con người**.

```
Loop = Define purpose → Iterate → Done / Escalate to human
```

---

## 2. Năm Building Blocks + Memory

Đây là mấy **viên gạch nền** mà vòng loop nào cũng có. Tên tool rồi sẽ đổi (hôm nay là Grok, mai là Claude Code, Codex, Cursor, Opencode...), nhưng việc mà từng viên gạch phải làm thì vẫn vậy.

| Primitive | Job trong Loop |
|-----------|----------------|
| **Automations / Scheduling** | Phát hiện + triage theo nhịp |
| **Worktrees** | Thực thi song song an toàn |
| **Skills** | Kiến thức dự án bền vững |
| **Plugins & Connectors** | Vươn vào tools thật (MCP) |
| **Sub-agents** | Tách maker / checker |
| **+ Memory / State** | Xương sống bền vững ngoài mọi hội thoại |

```
┌───────────────────────────────────────────────────────────────┐
│               NĂM BUILDING BLOCKS + MEMORY                     │
│                                                               │
│  ┌─────────────┐ ┌───────────┐ ┌──────────┐ ┌──────────────┐ │
│  │ Automations │ │ Worktrees │ │  Skills  │ │Plugins & Conn│ │
│  │ / Scheduling│ │ (cô lập)  │ │(knowledge)│ │  (MCP)       │ │
│  └──────┬──────┘ └─────┬─────┘ └────┬─────┘ └──────┬───────┘ │
│         └───────────────┼────────────┼──────────────┘        │
│                         ▼            ▼                        │
│              ┌────────────────────────────────────┐          │
│              │   SUB-AGENTS (Maker / Checker)      │          │
│              └────────────────────────────────────┘          │
│                         │                                     │
│                         ▼                                     │
│              ┌────────────────────────────────────┐          │
│              │   MEMORY / STATE (bền vững)         │          │
│              └────────────────────────────────────┘          │
└───────────────────────────────────────────────────────────────┘
```

### 2.1 Automations / Scheduling

Đây là nhịp tim của loop. **Không có lịch chạy tự động, thì bạn chỉ có một lần chạy lẻ tẻ.**

Mấy kiểu hẹn giờ hay gặp ngoài đời:
- `/loop [interval] <prompt>` (Grok, Claude Code)
- Scheduled tasks / cron trong Claude Code
- GitHub Actions + repository dispatch
- `/goal` — chạy cho đến khi một điều kiện kiểm chứng được thoả
- Custom harness schedulers

Lúc chọn cách hẹn giờ, bạn nhớ ngó bốn thứ này: **chạy mỗi bao lâu (interval), có chạy ngay phát đầu không, chạy một lần hay chạy hoài, và có sống sót qua restart không (durable).**

### 2.2 Worktrees

Muốn chạy song song mà không dẫm chân nhau thì nhờ món này.

Bạn thử tưởng tượng hai agent cùng thò tay sửa một file một lúc là thấy cảnh rối ngay. Git worktrees (hoặc kiểu checkout cách ly tương tự) cho mỗi agent một **góc làm việc riêng** — xài chung lịch sử, nhưng bàn làm việc thì ai nấy giữ.

```
Agent A (worktree 1)  ──►  sửa fix/ci-auth-refresh
Agent B (worktree 2)  ──►  sửa fix/issue-1241
         └────── cùng chia sẻ history ──────┘
```

**Dọn dẹp sau khi làm xong quan trọng lắm** — việc xong hay cần nhờ người là phải xóa worktree cho gọn. Tool `loop-worktree` sinh ra để làm việc đó cho chuẩn: mỗi lần thử một worktree riêng, ghi vào manifest để theo dõi, dọn sạch khi bị reject hoặc cần escalate.

### 2.3 Skills

Nếu ví state là cuốn sổ ghi việc, thì skills là cuốn **sổ ghi ý định** lâu dài.

Một skill (`SKILL.md` + `scripts/`/`references/`/`assets` theo chuẩn Agent Skills — xem `harness/05-prompt-builder/agent-skills-spec.md`) gói ghém giùm bạn:
- Quy ước dự án
- "Chúng tôi không làm theo cách này vì sự cố X"
- Lệnh build/test/lint
- Tiêu chuẩn review
- Kiến thức domain

**Không có skills**, mỗi lần chạy loop lại đoán mò từ đầu → thế là **nợ ý định (intent debt)** chồng chất.

```
Skills = "Conventions viết một lần, đọc mọi lần chạy"
```

### 2.4 Plugins & Connectors (MCP)

Một vòng loop chỉ biết đọc file trong máy thì cũng giống người làm việc mà không có điện thoại — hơi tù.

Có connectors, loop mới thò tay ra thế giới thật được:
- Đọc/cập nhật tickets Linear / Jira
- Đăng lên Slack / Discord
- Query databases / internal APIs
- Tạo branch và PR trên GitHub
- Trigger deploys / runbooks

Dạo này **MCP (Model Context Protocol)** thành kiểu ổ cắm chung — đồ cắm viết cho tool này thường bê sang tool khác xài được luôn.

### 2.5 Sub-agents — Maker / Checker Split

Đây là kiểu chia vai **đáng tiền nhất** nếu bạn muốn loop chạy mà vẫn tin được.

Người vừa nấu ăn mà tự chấm món mình nấu thì điểm lúc nào chẳng cao. Nên mình cho một agent khác (đôi khi xài model xịn hơn, lúc nào cũng khác hướng dẫn) đứng ra **nếm lại món đó**.

```
Implementer (Maker) ──patch──► Verifier (Checker) ──approve/reject──►
   Không bao giờ tự chấm         "Tìm lý do để REJECT"              Commit / PR
   điểm chính mình
```

Mấy kiểu chia vai hay gặp:
- Explorer → Implementer → Verifier
- Implementer → Security reviewer
- Implementer → Test writer + runner

Với mấy loop **chạy lúc không có ai ngó (unattended)**, ông verifier chính là lý do để bạn dám đi ngủ mà vẫn yên tâm phần nào.

### 2.6 Memory / State

Bản chất model là mau quên — qua turn khác, session khác là quên sạch.

Nên loop **kiểu gì cũng phải có chỗ ghi chép bền** để lần sau quay lại còn nhớ:
- `STATE.md` hoặc `LOOP-STATE.json` trong repo
- Một section riêng của Linear board / GitHub Project
- Một row database nhỏ

Một cuốn sổ state tốt thì mở ra trả lời được ngay:
- Chúng ta đang làm gì?
- Lần trước thử gì, kết quả ra sao?
- Cái gì đang chờ con người?

> **State file thường là artifact quan trọng nhất mà loop tạo ra.**

---

## 3. Anatomy of a Loop

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Anatomy of a Loop là "bản vẽ giải phẫu" một vòng lặp — liệt kê các trạm cố định mà lần chạy nào cũng phải đi qua: từ lúc chuông báo thức reo (scheduler), tới lúc phân loại việc (triage), làm trong phòng riêng (worktree), kiểm hàng, rồi giao cho người hoặc bấm nút commit.
> **Ẩn dụ/so sánh:** Cứ nghĩ tới **dây chuyền ráp xe hơi** — chiếc xe phải đi qua từng trạm đúng thứ tự: nạp đồ (context), phân loại (triage), ráp trong khu riêng (worktree), kiểm định (verifier), rồi mới xuất xưởng hoặc quay về kho (commit / escalate). Bỏ một trạm là xe ra xưởng mà chưa ai kiểm thắng.
> **Vì sao quan trọng:** Tờ bản vẽ này là thứ bạn lôi ra mỗi lần thiết kế loop mới. Tụi mình thấy chỉ cần đảo thứ tự hai trạm thôi là loop từ an toàn thành nguy hiểm ngay — kiểu như nhất định phải làm trong worktree cách ly rồi mới cho kiểm chứng, không làm ngược lại được.

Một vòng chạy đầy đủ thường đi như vầy:

```
┌──────────────────────────────────────────────────────────────────────┐
│ Schedule / Automation ──► Triage Skill                               │
│     │                          │                                     │
│     │                          ▼                                     │
│     │                   Read + Write STATE / Memory                  │
│     │                          │                                     │
│     │                          ▼                                     │
│     │                  Isolated Worktree                             │
│     │                          │                                     │
│     │                          ▼                                     │
│     │                  Implementer Sub-agent                         │
│     │                          │                                     │
│     │                          ▼                                     │
│     │                  Verifier Sub-agent (tests + gates)            │
│     │                          │                                     │
│     │                          ▼                                     │
│     │                  MCP / Git / Tickets                           │
│     │                          │                                     │
│     │                          ▼                                     │
│     │                  Human Gate?                                   │
│     └── safe/allowlisted ──► Commit / PR / Action                    │
│     └── risky/ambiguous ────► Escalate to human (full context)       │
└──────────────────────────────────────────────────────────────────────┘
```

### 3.1 Vòng Đời Một Run

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** "Vòng đời một run" là hành trình của một lần chạy (run) — từ lúc chuông reo cho tới lúc ghi dòng tổng kết vào sổ. Nó giống cái bảng trạng thái treo trước cửa, nhìn vào là biết run đang đứng ở đâu.
> **Ẩn dụ/so sánh:** Như **một chuyến bay có nhiều chặng**: máy bay phải đi qua từng điểm — cất cánh (Scheduled), bay vào vùng lặng thì đáp gọn (RunningTriage → IdleNoop khi không có việc), hạ cánh đẹp (Applied) hoặc bay chờ vì cần người cho phép (AwaitingHumanGate). Không có chuyện nhảy cóc.
> **Vì sao quan trọng:** Nhìn trạng thái là biết loop đang bận gì và **vì sao nó im re** — nhiều khi bạn thắc mắc "sao nó chẳng làm gì", mở ra thấy mỗi chữ `IdleNoop` là hiểu ngay: à, hôm nay không có việc.

Mỗi run được lên lịch đi qua các trạng thái sau, kết thúc bằng một log entry bền vững:

```
Scheduled → LoadingContext → RunningTriage → WorkingInWorktree → Verifying
     │              │              │
     │              ├──► BlockedBudget (budget exceeded)
     │              └──► RunningTriage
     │                              └──► IdleNoop (không có gì để làm)
     │
     Verifying → AwaitingHumanGate → Applied / Rejected
           │            └──► Failed
           │
           └──► (mọi trạng thái cuối) → Logged → [*]
```

**Chỗ cần nhớ**: `IdleNoop` là chuyện bình thường — thấy watchlist trống thì loop nên **rút lui gọn nhẹ (< 5k tokens)**, chứ đừng lôi cả dàn sub-agent ra chạy cho tốn.

### 3.2 Loop Orchestration Engine

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Loop Orchestration Engine là "bác quản lý" bằng code — một lớp điều phối đứng giữa, đảm bảo lần chạy nào cũng đi đúng bài: mở sổ state ra đọc, phân loại việc, làm trong worktree có người kiểm, rồi ghi sổ lại. Đoạn code dưới là **bản mẫu để học**, bạn không cần chép y chang, chỉ cần nắm mấy chỗ ra quyết định quan trọng.
> **Ẩn dụ/so sánh:** Như **bác trực thang máy trong tòa nhà**: bác không sửa được tòa nhà, nhưng bác quyết khi nào mở cửa (trigger), đi tầng nào (triage), dừng cho ai ra vào (human gate), và ghi lại ai đã đi đâu (log). Mọi chuyện qua một cửa nên khó lọt sổ.
> **Vì sao quan trọng:** Mấy luật quan trọng nhất đều nằm ở đây: verifier mà lăn tăn thì **mặc định REJECT**, thử **tối đa 3 lần là phải nhờ người** (không retry tới sáng), và **ghi log kiểu chỉ thêm không xóa** để mai mốt bạn còn trả lời được "sao hôm thứ Ba nó lại làm thế?". Lúc đọc code, bạn chỉ cần tự hỏi 3 câu: *sổ state đọc ở đâu? ai chấm điểm? khi nào thì dừng?*

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/01-3-2-loop-orchestration-engine.py`](examples/01-3-2-loop-orchestration-engine.py)

</details>

---

## 4. Mức Tự Chủ L1 → L2 → L3

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Mức tự chủ (autonomy level) là "bằng lái" của loop — cho biết nó được tự làm tới đâu: từ L0 (mới ghi ý định ra giấy), L1 (đi quan sát rồi về báo cáo), L2 (được sửa mấy lỗi nhỏ có người kiểm lại), tới L3 (tự chạy không cần bạn ngó). Đây không phải huy chương để khoe, mà là **giấy phép theo độ tin cậy**.
> **Ẩn dụ/so sánh:** Như **dạy người mới lái xe**: L1 là "ngồi ghế phụ, chỉ được báo đường" — thấy ổ gà thì nói chứ không được đánh lái; L2 là "tự lái mấy đường quen, có thầy ngồi cạnh"; L3 là "ôm xe chạy tỉnh một mình" — chỉ khi bạn đã thấy tay lái cứng qua nhiều tuần.
> **Vì sao quan trọng:** Đốt cháy giai đoạn từ L1 lên thẳng L3 là cách nhanh nhất để loop "đốt" luôn production trước khi bạn hiểu nó làm gì. Cái thang này bắt bạn gom đủ **bằng chứng chạy ngon** rồi mới nới tay dần.

Đừng ai mở loop **chạy tự do (unattended)** ngay từ ngày đầu tiên. Ba nấc này là lộ trình đi từng bước cho chắc chân:

```
L1 REPORT-ONLY ──► L2 ASSISTED ──► L3 UNATTENDED
  Triage → state     Small auto-fixes   Chạy không có bạn theo dõi
  Không auto-action  Với verifier       Cần denylist + budget + gates
  Tuần 1 đầu tiên    + worktree         + max attempts
```

| Level | Mô tả | Checklist |
|-------|-------|-----------|
| **L0 — Draft** | Chỉ có ý định được ghi chép | §1 (purpose & scope) |
| **L1 — Report** | Triage → state, không auto-action | §1–3, §5 |
| **L2 — Assisted** | Auto-fix nhỏ với verifier | §1–7 |
| **L3 — Unattended** | Chạy không cần bạn nhìn | Tất cả sections |

**Luật bất thành văn**: pattern nào mới toanh thì đừng thả thẳng lên L3 trên repo production.

```
L1 ──► L2: audit score lên + human OK
L2 ──► L3: denylist + budget + gates đã chứng minh
L3 ──► L2: incident hoặc cost spike
L2 ──► L1: kill switch
```

---

## 5. Loop Taxonomy — Các Vòng Lặp Lồng Nhau

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Loop taxonomy là cách mấy vòng lặp **ngồi lồng trong nhau** theo 5 nhịp nhanh chậm — từ vòng nghĩ trong đầu agent (tính bằng mili-giây) tới vòng cải tiến cả hệ thống (tính bằng ngày/tuần). Đừng nhìn chúng như 5 món rời nhau; hãy nhìn như **5 lớp hành tây bọc lấy nhau**.
> **Ẩn dụ/so sánh:** Như **một buổi hòa nhạc**: ngón tay kéo đàn của từng nghệ sĩ là nhịp nhanh nhất (inner loop, mili-giây), cả bài nhạc đánh lại khi lệch nhịp là tầng giữa (execution loop), còn chuyện mùa sau diễn bản nào là quyết định chậm nhất (outer loop). Nhạc trưởng không kè từng ngón tay — anh chọn tầng nào cần luật riêng của tầng đó.
> **Vì sao quan trọng:** Luật phải đặt đúng tầng: cấm retry vô hạn là chuyện của **execution loop** (tốc độ mili-giây), chứ không phải của **outer loop** (tốc độ ngày). Hiểu taxonomy là biết vòng nào nhanh, vòng nào chậm, vòng nào cần người chấm, vòng nào chỉ cần người gật đầu.

Nhìn ở tầm thiết kế hệ thống, vòng loop lớn nào cũng chứa mấy vòng nhỏ bên trong. Nắm được taxonomy này, bạn sẽ biết **đặt guardrail ở đâu cho đúng chỗ**.

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│  OUTER LOOP (cross-task, ngày/tuần)                                 │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │  LEARNING LOOP (per-task, giờ)                                 │  │
│  │  ┌─────────────────────────────────────────────────────────┐  │  │
│  │  │  EXECUTION LOOP (per-action, giây)                      │  │  │
│  │  │  ┌───────────────────────────────────────────────────┐  │  │  │
│  │  │  │  INNER LOOP (per-step, ms)                        │  │  │  │
│  │  │  │  Think ──► Act ──► Observe ──► Reflect            │  │  │  │
│  │  │  │     ▲                              │              │  │  │  │
│  │  │  │     └──────────────────────────────┘              │  │  │  │
│  │  │  │                                                   │  │  │  │
│  │  │  │  Execute ──► Retry ──► Verify ──► Escalate        │  │  │  │
│  │  │  └───────────────────────────────────────────────────┘  │  │  │
│  │  └─────────────────────────────────────────────────────────┘  │  │
│  │                                                               │  │
│  │  Task 1 ──► Task 2 ──► Task 3 ──► ... ──► Optimize           │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 5.1 Inner Loop

Đây là vòng chạy nhanh nhất — diễn ra ngay trong đầu agent. Agent kiểu "lẩm bẩm một mình" trước khi ra tay: Think → Act → Observe → Reflect.

**Kể cho dễ nhớ:** như **người chơi cờ nghĩ trước khi đặt quân** — ngắm bàn cờ (Think), đi một nước (Act), nhìn đối thủ phản ứng (Observe), rút ra bài học (Reflect). Vòng này nhanh tới mức bạn không chen vào được: không cần viết script, không cần gắn guardrail — nó là "phản xạ" của agent.

### 5.2 Execution Loop

Vòng này lo chuyện "lỡ làm lỗi thì sao" — sao cho agent không bỏ cuộc quá sớm, mà cũng **đừng cố đấm ăn xôi mãi**. Mấy chiêu quen thuộc: thử lại có nghỉ giữa hiệp (retry with backoff), cầu dao ngắt mạch (circuit breaker), hẹn giờ cắt (timeout). Luật quan trọng nhất: **thử quá số lần là phải nhờ người (hard cap → escalate)**.

**Kể cho dễ nhớ:** như **đi rút tiền ATM** — máy báo lỗi thì bấm lại một hai lần là phải; chứ đứng bấm liền 50 lần thì hơi căng. Execution loop cho thử vài lần có nghỉ, rồi ngắt cầu dao (circuit breaker) và gọi người ra coi (escalate).

### 5.3 Validation Loop

Vòng này hỏi một câu rất đời: "code chạy thiệt chưa, hay mới chạy trên giấy?". Công thức là Write → Test → Fix → Re-test. Khi chạy production, khâu này nằm ở **ông verifier** — người khác ông viết code — chạy test trong worktree cách ly.

**Kể cho dễ nhớ:** như **bác đầu bếp nếm món trước khi bưng ra** — nấu xong (Write), nếm thử (Test), mặn thì thêm nước (Fix), rồi nếm lại (Re-test). Nhờ người khác nếm giùm nên không bị kiểu "món mình nấu lúc nào cũng ngon".

### 5.4 Feedback Loop

Đây là sợi dây nối hôm qua với ngày mai — lấy kết quả cũ để lần sau làm khôn hơn. Công thức là Collect metrics → Analyze → Optimize → Apply. Mỗi lần chạy xong nên có dòng **tự kiểm điểm**: cái nào báo nhầm, cái nào lặp lại, lần sau sửa một chỗ nào.

**Kể cho dễ nhớ:** như **cái máy lạnh có cảm biến nhiệt** — đo phòng mấy độ (Collect), thấy nóng quá (Analyze), chỉnh xuống thêm hai độ (Optimize), mai mốt nhớ mở sẵn mức đó (Apply). Thiếu vòng này thì loop chạy hoài mà không khôn lên chút nào.

### 5.5 Outer Loop

Vòng này chạy chậm (ngày/tuần), lo chuyện lớn: **cả hệ thống có đang tốt lên không** — prompt có cần sửa, pattern nào ăn khách, chỉ số đi lên hay đi xuống. Đây cũng là chỗ bạn ghé vào nhiều nhất.

**Kể cho dễ nhớ:** như **buổi họp tổng kết cuối tuần của đội bóng** — không sửa từng cú sút (đó là việc của HLV trong trận), mà nhìn cả mùa: chiến thuật nào ra bàn, ai cần đổi vị trí. Ngồi họp kiểu này đều thì bạn sẽ thấy sớm nếu "đội mình đang đá xuống".

---

## 6. Concepts & Vocabulary

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Đây là cuốn "từ điển bỏ túi" của dân làm loop — mấy từ trừu tượng nghe đâu cũng gặp khi nói về agents: nợ ý định (intent debt), nợ hiểu biết (comprehension debt), buông xuôi nhận thức (cognitive surrender), thuế điều phối (orchestration tax)... Biết gọi tên thì lúc sự cố tới bạn chỉ mặt được ngay.
> **Ẩn dụ/so sánh:** Như **mấy từ bên tâm lý học** — ngày xưa chưa có chữ "burnout", ai đuối cũng chỉ biết nói "mệt quá". Có chữ rồi thì nhận ra sớm, chữa đúng bệnh. Mấy khái niệm dưới đây cũng là kiểu "burnout" của thế giới agent vậy.
> **Vì sao quan trọng:** Nhiều ca debug loop "khó hiểu" thực ra đều rơi vào một trong mấy món này. Học thuộc mặt chúng trước khi sang [06 — Anti-Patterns](../06-anti-patterns/) — kiểu như biết mặt đối thủ trước khi ra sân.

### 6.1 Intent Debt

Mỗi phiên mới, agent mở mắt ra với **cái đầu trống rỗng**. Chỗ nào thiếu ý định là nó tự đoán cho đầy — mà đoán thì hay trật, lại còn rất tự tin. **Skills** là cách trả món nợ này: ghi sẵn quy ước, các bước build, mấy kiểu "nhà mình không làm thế" — viết một lần, lần nào chạy cũng lôi ra đọc.

### 6.2 Comprehension Debt

Khoảng cách giữa "code đang có trong repo" và "thứ bạn thật sự hiểu". Loop chạy càng nhanh, code đẻ càng nhiều mà không phải tay bạn viết — **món nợ hiểu biết cứ lớn dần nếu bạn không đọc lại đồ loop đẻ ra**.

> *"Velocity up, but no one can explain recent changes; review becomes rubber-stamp."*

### 6.3 Cognitive Surrender

Cái bẫy ngọt ngào là để loop chạy riết rồi **mình khỏi cần nghĩ nữa**. Thiết kế loop để nó gánh việc nặng cho mình nghĩ chuyện khó hơn — đó là dùng đúng. Còn dùng loop để khỏi phải nghĩ gì hết — đó là buông xuôi. Cùng một nút bấm, hai kết cục khác nhau.

### 6.4 Orchestration Tax

Cái giá phải trả khi bạn điều nhiều agent chạy song song: sức đọc review, va chạm lúc merge, đầu óc nhảy qua lại giữa các việc. **Worktrees** gỡ được va chạm máy móc; còn trần hấp thụ thì vẫn là bạn — một lúc bạn gánh được bao nhiêu loop cùng chạy.

### 6.5 Code Agent Orchestra / Adversarial Review

Kiểu chia vai kinh điển: mỗi agent một việc (đi thám thính, viết code, kiểm tra). Luật sắt là **người viết không được tự chấm bài của mình** — nhất là với mấy loop chạy lúc không ai ngó.

---

## 7. Tương Lai Loop Engineering

### Xu Hướng

```
┌─────────────────────────────────────────────────────────────┐
│                 LOOP ENGINEERING EVOLUTION                    │
│                                                              │
│  2024-2025: Manual prompting → first loops                  │
│       → Ad-hoc agents, no state, no verifiers                │
│                                                              │
│  2025-2026: Production loop frameworks                      │
│       → Patterns, starters, readiness scores                │
│       → Denylist, budget, human gates (loop-engineering)    │
│       → Cross-tool primitives (Grok, Claude, Codex, ...)    │
│                                                              │
│  2027: Self-verifying & self-tuning loops                   │
│       → Loops that adjust cadence by signal quality         │
│       → Cross-task learning at scale                        │
│       → Multi-agent loop coordination (fleet)               │
│                                                              │
│  2028: Autonomous improvement with human governance         │
│       → Loops that design new loops                         │
│       → Human-in-the-loop for strategic decisions only      │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Research Directions

1. **Goal vs Loop** — loops phát hiện việc ongoing; goals hoàn thành bounded tasks (`/goal`). Ranh giới mờ dần.
2. **Multi-Agent Loop Coordination** — nhiều agents chia sẻ loop insights, cải thiện tập thể.
3. **Self-Tuning Parameters** — loops tự điều chỉnh cadence/budget theo signal quality.
4. **Loop Compression** — giảm số iterations cần thiết bằng predicted outcomes.
5. **Ethical Loop Constraints** — đảm bảo loops không tạo harmful feedback cycles.

---

*Tiếp theo: [02 — Bảy Production Patterns](../02-patterns/) → [03 — Safety & Loop Design Checklist](../03-safety/)*
