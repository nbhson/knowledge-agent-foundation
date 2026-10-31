# 🧬 Sub-Agent — Spec vòng đời, spawn, quyền và ngân sách

> Companion của `README.md` (đặc biệt §16 Chịu lỗi / Messaging / Isolation).
> Tổng hợp quy ước từ `loop/01-concepts` (§2.5 Maker/Checker), `loop/02-patterns/*`,
> `loop/04-operating`, `loop/06-anti-patterns` và ví dụ Claude Code ở `README.md §16.5`.

> ## 📑 Mục Lục
>
> - [Tổng Quan](#tổng-quan) - [Nội Dung](#nội-dung)
> - [1. Định nghĩa](#1-định-nghĩa)
> - [2. Taxonomy vai trò](#2-taxonomy-vai-trò)
> - [3. Vòng đời](#3-vòng-đời)
> - [4. Spawn API](#4-spawn-api-contract-tối-thiểu)
> - [5. Context và memory](#5-context-và-memory)
> - [6. Cách ly và secret](#6-cách-ly-và-secret)
> - [7. Gộp kết quả](#7-gộp-kết-quả)
> - [8. Budget và cost guard](#8-budget--cost-guards)
> - [9. Kiểm thử sub-agent](#9-kiểm-thử-sub-agent)
> - [10. Anti-pattern](#10-anti-pattern--giải-pháp)
> - [11. Triển khai thực tế](#11-triển-khai-thực-tế)
> - [12. Checklist](#12-checklist--triển-khai-production)
> - [Best Practices](#best-practices) - [Tài liệu tham khảo](#tài-liệu-tham-khảo)
>
> ---

### Câu Chuyện Mở Đầu

> Phần này dùng một câu chuyện để hình dung sub-agent là gì — đọc xong câu chuyện là hiểu được định nghĩa.

Hãy tưởng tượng một **chiến dịch đặc nhiệm**. Chỉ huy (parent) không tự xông vào mọi tòa nhà. Bà cử **tổ trinh sát** (researcher) vẽ địa hình, **tổ đột nhập** (implementer) mở một cánh cửa, và **thanh tra** (verifier) xác nhận đã an toàn. Mỗi tổ chỉ nhận một mẩu bản đồ — không phải toàn bộ kế hoạch tác chiến — một khung giờ, và một quy tắc: báo cáo về, không tự ý hành động.

**Sub-agent chính là tổ đặc nhiệm đó.** Không có nhiệm vụ hẹp + bản đồ cắt gọn + budget riêng + deadline (lease), đó không phải đặc nhiệm — chỉ là tiếng ồn trong cùng một phòng.

> **Tóm gọn 1 câu:** Sub-agent là "tổ đặc nhiệm" được cha giao một việc hẹp, một mẩu context, một ngân sách, và một khung giờ — không thỏa 4 điều đó thì không nên gọi là sub-agent.

### Vì Sao Spec Này Quan Trọng?

> Phần này nêu hậu quả nếu dùng sub-agent thiếu kỷ luật, kèm số liệu minh chứng.

> *"Parent mà thiếu kỷ luật sub-agent giống người quản lý forward cả inbox cho mọi thực tập sinh — ai cũng ngợp, không ai chịu trách nhiệm."*

Cách đọc bảng này: cột **#** là số thứ tự; cột **Nghiên cứu** là nguồn (ai nghiên cứu, năm nào); cột **Phát hiện chính** là con số minh chứng của nguồn đó. Ví dụ: dòng 1 nghĩa là Anthropic đo được cách ly sub-agent làm giảm ~70% rủi ro agent làm vượt quyền.

| # | Nghiên cứu | Phát hiện chính |
|---|-----------|-----------------|
| 1 | **Anthropic — Claude Code (2025)** | Subagent cách ly giảm rủi ro leo thang đặc quyền ~70% |
| 2 | **Google DeepMind (2025)** | Tách maker/checker giảm phê duyệt bừa (rubber-stamp) ~45% |
| 3 | **LangGraph (2025)** | Lease + heartbeat + requeue idempotent phục hồi ~90% subtask crash |

Giải nghĩa ba từ trong dòng 3: **lease** = "hợp đồng thuê" giữ quyền có thời hạn; **heartbeat** = tín hiệu "tôi còn sống" gửi định kỳ; **requeue idempotent** = xếp lại việc vào hàng đợi sao cho chạy lại nhiều lần vẫn cho cùng kết quả, không hỏng dữ liệu.

```
Sub-Agent = Vai trò hẹp + Context cắt gọn + Tool thu hẹp + Budget riêng + Lease + Kiểm tra độc lập
```

> **Tóm gọn 1 câu:** Sub-agent có giá trị khi và chỉ khi nó bị "siết" đúng 6 thứ — vai trò hẹp, context gọn, tool ít, budget riêng, lease, và được bên khác kiểm tra.

## Tổng Quan

> Phần này tóm tắt định nghĩa và sơ đồ tương tác giữa agent cha và sub-agent.

> **📌 Khái Niệm Cơ Bản**
>
> - **Khái niệm:** Sub-Agent là agent con cho **một task hẹp**, chạy cùng harness với **context cắt gọn, tool thu hẹp, budget riêng, lease**.
> - **Ẩn dụ:** Như ticket trong bếp — một đầu bếp, một mẩu công thức, một timer. Timer reo → ticket được giao lại, đĩa cũ bỏ (fencing).
> - **Vì sao quan trọng:** Thiếu contract này, sub-agent phình context, rò secret, ghi đè file lẫn nhau, tự duyệt việc yếu kém.

```
┌───────────────────────────────────────────────────────────────┐
│  PARENT (full ctx, mọi tool) ──spawn(spec)──► SUB-AGENT       │
│    files[] + summary │ tools[] │ budget │ lease │ worktree    │
│                      └── artifact + transcript ──► aggregate   │
└───────────────────────────────────────────────────────────────┘
```

Đọc sơ đồ thế nào? Bên trái là parent với full context. Mũi tên là `spawn(SubAgentSpec)` chỉ mang files + summary + tool allow-list + budget + lease. Bên phải là sub-agent trong worktree của nó. Mũi tên về là artifact + transcript gọn đưa vào bộ gộp (checker/quorum). Không có gì khác chảy ngược về.

(Giải nghĩa: **spec** = bản đặc tả — hồ sơ mô tả sub-agent sẽ làm gì; **allow-list** = danh sách trắng, chỉ những thứ được liệt kê mới được dùng; **worktree** = thư mục làm việc riêng của git; **artifact** = sản phẩm đầu ra (file/patch/báo cáo); **transcript** = bản ghi hội thoại; **quorum** = số phiếu tối thiểu để ra quyết định.)

> **Tóm gọn 1 câu:** Parent đưa đi đúng mẩu context và quyền tối thiểu; sub-agent làm xong trả về artifact + bản ghi gọn — không gì khác chảy hai chiều.

## Nội Dung

> Cách đọc bảng này: đây là mục lục chi tiết — cột **#** và **Chủ đề** là các mục bên dưới; cột **Ý chính** tóm ý của mục đó. Ví dụ: mục 3 "Vòng đời" nói về các trạng thái spawn → chạy → xong hoặc treo.

| # | Chủ đề | Ý chính |
|---|-------|----------|
| 1 | [Định nghĩa](#1-định-nghĩa) | Agent vs sub-agent vs loop vs function call |
| 2 | [Vai trò](#2-taxonomy-vai-trò) | implementer / verifier / reviewer / researcher |
| 3 | [Vòng đời](#3-vòng-đời) | spawn → heartbeat → done / DEAD / TIMED_OUT / SUSPECT |
| 4 | [Spawn API](#4-spawn-api-contract-tối-thiểu) | Contract tối thiểu + validation + ví dụ |
| 5 | [Context/Memory](#5-context-và-memory) | Scratchpad riêng + blackboard có version |
| 6 | [Cách ly/Secret](#6-cách-ly-và-secret) | Tool tối thiểu theo role + lease ngắn |
| 7 | [Gộp KQ](#7-gộp-kết-quả) | Maker/checker + quorum + giới hạn message |
| 8 | [Budget](#8-budget--cost-guards) | Tối đa 3 spawn/run + kill switch |
| 9 | [Kiểm thử](#9-kiểm-thử-sub-agent) | Unit + chaos drill |
| 10 | [Anti-pattern](#10-anti-pattern--giải-pháp) | 8 cái bẫy |
| 11 | [Thực tế](#11-triển-khai-thực-tế) | Claude Code, triage loop |
| 12 | [Checklist](#12-checklist--triển-khai-production) | Cổng xuất xưởng |

---

## 1. Định nghĩa

> Phần này vẽ ranh giới: cái nào là Agent, cái nào là Sub-agent, cái nào KHÔNG phải sub-agent.

> **📌 Khái Niệm Cơ Bản**
>
> - **Khái niệm:** Ranh giới cứng — **Agent** sở hữu task + full loop; **Sub-agent** sở hữu đúng một task hẹp dưới lease; **Loop** là lịch cron; function call không có lease/budget/tool.
> - **Ẩn dụ:** Agent = quản lý; sub-agent = đầu bếp với một ticket; loop = lịch ca; function call = đưa dao mà không đưa ticket.
> - **Vì sao quan trọng:** Gọi mọi thứ là "sub-agent" sẽ mất fencing và verify — việc bị ghi đè, secret rò rỉ.

### 1.1 Bảng so sánh

Cách đọc bảng này: mỗi dòng là một "thực thể" (loại thành phần); các cột cho biết thực thể đó sở hữu gì và bị giới hạn gì. Ví dụ: dòng **Sub-agent** chỉ sở hữu một task hẹp, context bị cắt gọn, và phải có verifier độc lập — khác hẳn dòng **Agent** đầy đủ quyền.

| Thực thể | Sở hữu | Context | Tool | Budget | Lease | Verifier |
|---|---|---|---|---|---|---|
| **Agent** | task + memory, full harness (01→11) | đầy đủ | rộng | lớn | deadline riêng | bên ngoài |
| **Sub-agent** | **một task hẹp** | **cắt gọn (files[] + summary)** | **allow-list** | **budget nhỏ riêng** | **leaseId + deadline + maxAttempts** | **độc lập** |
| **Loop** | lịch (cron), mỗi run có thể spawn | watchlist state | tool triage | trần mỗi run (<5k nếu idle) | deadline run | cổng state |
| Function call | không (trả giá trị) | chỉ args | scope callee | budget caller | không | caller |

* **Agent**: thực thể chạy full vòng harness (01→11), sở hữu task và memory.
* **Sub-agent**: agent con được cha/orchestrator spawn cho **một task hẹp**, chạy cùng harness nhưng với **context cắt gọn + tool thu hẹp + budget riêng + lease**.
* **Loop**: vòng lặp định kỳ (cron) có thể spawn sub-agents mỗi run (`loop/05-multi-loop`).

Quy tắc phân biệt: nếu không có lease + deadline + budget riêng + tool allow-list riêng, đó không phải sub-agent mà chỉ là một function call.

> **Tóm gọn 1 câu:** Sub-agent được định nghĩa bằng những giới hạn của nó — thiếu lease, deadline, budget riêng hay allow-list thì đó chỉ là một function call khoác tên khác.

### 1.2 Guard kiểm tra contract

<details>
<summary>Python — loại sub-agent giả</summary>

> 📄 **Code ví dụ:** [`examples/01-1-2-guard-kiem-tra-contract.py`](examples/01-1-2-guard-kiem-tra-contract.py)

</details>

---

## 2. Taxonomy vai trò

> Phần này chia sub-agent thành 4 vai trò, mỗi vai một bộ tool tối thiểu — đây chính là "biên đặc quyền".

> **📌 Khái Niệm Cơ Bản**
>
> - **Khái niệm:** Bốn vai trò hẹp — maker viết, checker test, reviewer chấm diff, researcher báo fact. Mỗi role chỉ nhận tool tối thiểu.
> - **Ẩn dụ:** Như tòa soạn — phóng viên thu thập, người viết soạn, biên tập cắt gọt, kiểm chứng fact. Không bao giờ để người viết tự kiểm chứng mình.
> - **Vì sao quan trọng:** Cặp role + tool chính là biên đặc quyền. Cùng một agent vừa implement vừa verify = confirmation bias.

### 2.1 Ma trận vai trò

Cách đọc bảng này: mỗi dòng là một vai trò; cột **Việc** là nhiệm vụ chính; cột **Không được làm** là điều cấm; cột **Tool** là bộ công cụ tối thiểu được cấp. Ví dụ: `implementer` được viết code trong worktree nhưng không được tự merge hay tự verify.

| Vai trò | Việc | Không được làm | Tool (từ 12-sandbox §6) |
|---|---|---|---|
| `implementer` / `maker` | Viết code trong worktree được giao | Tự merge, tự verify cuối | shell sandbox (không net), FS ghi có phạm vi |
| `verifier` / `checker` | Chạy test, gates, chấm rubric (mặc định REJECT) | Sửa code trực tiếp (chỉ comment) | test runner, FS đọc, không ghi |
| `reviewer` | Review diff, severity Blocker/Major/Minor | Chạy shell, ghi file ngoài comment | FS chỉ đọc, không shell |
| `researcher` / `triage` | Đọc code/docs, trả facts + citations `file:line` | Đổi behavior, ghi memory dài hạn | FS chỉ đọc + search, không exec |

Anti-pattern cấm (`loop/06-anti-patterns`): cùng một agent vừa implement vừa verify → test yếu bị rubber-stamp (duyệt bừa, gật đầu cho qua mà không soi).

> **Tóm gọn 1 câu:** Bốn vai — người viết, người kiểm, người duyệt, người điều tra — mỗi vai một bộ tool tối thiểu, và tuyệt đối không để một agent vừa viết vừa tự kiểm.

### 2.2 Định nghĩa chi tiết từng role

<details>
<summary>Python — spec từng role kèm DoD</summary>

> 📄 **Code ví dụ:** [`examples/02-2-2-inh-nghia-chi-tiet-tung-role.py`](examples/02-2-2-inh-nghia-chi-tiet-tung-role.py)

</details>

---

## 3. Vòng đời

> Phần này giải thích sub-agent sống và chết ra sao: tín hiệu "còn sống", giới hạn giờ, và cách xử lý khi treo.

> **📌 Khái Niệm Cơ Bản**
>
> - **Khái niệm:** Mỗi sub-agent sống dưới một lease: heartbeat chứng minh còn sống, deadline giới hạn chi phí, detector treo bắt stall im lặng, fencing khiến kết quả cũ trễ thành vô hại.
> - **Ẩn dụ:** Như đồng hồ taxi + GPS — tài xế ping vị trí mỗi 5s; mất ping 15s = mất tích; hết giờ = hủy chuyến; tài xế mới nhận số ticket mới (fencing).
> - **Vì sao quan trọng:** Không có fencing + requeue idempotent, agent zombie tỉnh dậy trễ sẽ ghi đè việc tốt.

### 3.1 Máy trạng thái vòng đời

Sơ đồ là một luồng một chiều với một vòng retry duy nhất: spawn mang spec §4, heartbeat tick mỗi 5s kèm progress stream, done trả artifact + transcript gọn. Nhánh lỗi: DEAD (mất heartbeat >15s), TIMED_OUT (quá deadline), SUSPECT (còn sống nhưng không tiến triển >60s). Requeue tăng fencing token + attempt và đính transcript cũ; quá 3 attempts thì escalate human / fail closed.

(Giải nghĩa: **fencing token** = số lượt chạy, tăng mỗi lần giao lại — kết quả mang số cũ thì bỏ; **escalate** = báo người thật xử lý; **fail closed** = nghi ngờ thì chặn, không cho qua.)

```text
spawn (kèm spec §4) → heartbeat 5s → progress stream
  → done (trả artifact + transcript gọn)
  → fault: DEAD (mất heartbeat >15s) / TIMED_OUT (quá deadline) / SUSPECT (sống nhưng không tiến triển >60s)
  → requeue (fencing token++, attempt++, đính kèm transcript cũ) → quá 3 attempts → escalate human / fail closed
```

```
┌─────────┐  heartbeat 5s   ┌──────────┐  artifact  ┌──────┐
│  SPAWN  │────────────────►│ RUNNING  │───────────►│ DONE │
│ spec §4 │  progress stream│ lease    │  transcript│      │
└────┬────┘                 └────┬─────┘            └──────┘
     │  DEAD / TIMED_OUT /       │ SUSPECT (>60s không tiến triển)
     │  SUSPECT                  ▼
     │                     ┌──────────┐  attempt++ ┌──────────┐
     └────────────────────►│ REQUEUE  │───────────►│ ESCALATE │
        fencing token++     │ idempotent│  >3 lần    │ human    │
        transcript cũ       └──────────┘            └──────────┘
```

* Mỗi task có `lease_id + deadlineMs + max_attempts` (mặc định deadline 300s, max 3).
* Supervisor phi trạng thái, backed by queue (Redis/BullMQ); worker phải idempotent để requeue retry an toàn. Quorum judges/voters: 2f+1 chịu f lỗi, cần majority (vd 2/3).
* Chi tiết implementation: `README.md §16.1–16.2` (code mẫu heartbeat + reassignment).

> **Tóm gọn 1 câu:** Mỗi sub-agent sống dưới lease: heartbeat 5 giây chứng minh còn sống, 3 trạng thái hỏng (DEAD / TIMED_OUT / SUSPECT) đều đổ về requeue có fencing, quá 3 lần thì báo người.

### 3.2 Supervisor heartbeat

<details>
<summary>Python — lease + heartbeat + fencing</summary>

> 📄 **Code ví dụ:** [`examples/03-3-2-supervisor-heartbeat.py`](examples/03-3-2-supervisor-heartbeat.py)

</details>

---

## 4. Spawn API (contract tối thiểu)

> Phần này giải thích "hợp đồng" tối thiểu khi tạo sub-agent: đưa cho nó cái gì, và không được đưa cái gì.

> **📌 Khái Niệm Cơ Bản**
>
> - **Khái niệm:** Spawn chỉ mang context hẹp đủ dùng: allow-list file + ref artifact + summary cha cắt gọn — không bao giờ dump full.
> - **Ẩn dụ:** Như đưa thợ sửa ống nước bản vẽ một phòng tắm, không phải bản đồ cống cả thành phố.
> - **Vì sao quan trọng:** Dump full context nhân token mỗi spawn và rò secret/prompt vào mọi agent con.

### 4.1 Interface spawn

> 📄 **Code ví dụ:** [`examples/04-4-1-interface-spawn.ts`](examples/04-4-1-interface-spawn.ts)

### 4.2 Validation và ví dụ spawn

<details>
<summary>TypeScript — validate + hai ví dụ spawn</summary>

> 📄 **Code ví dụ:** [`examples/05-4-2-validation-va-vi-du-spawn.ts`](examples/05-4-2-validation-va-vi-du-spawn.ts)

</details>

### 4.3 Quy tắc spawn và cost guard

Quy tắc spawn (`loop/04-operating`): triage rẻ trước, chỉ spawn khi state báo actionable; watchlist rỗng → exit <5k tokens, không spawn. **Tối đa 3 sub-agents/run** mặc định.

Cách đọc bảng này: cột **Quy tắc** là tình huống; cột **Ngưỡng** là điều kiện kích hoạt; cột **Hành động** là việc hệ thống phải làm. Ví dụ: run đang rảnh (watchlist rỗng) thì thoát sớm dưới 5k token và không tạo agent nào.

| Quy tắc | Ngưỡng | Hành động |
|---|---|---|
| Run idle | watchlist rỗng | exit <5k tokens, không spawn |
| Trần fan-out | >3 spawn được yêu cầu | queue phần dư, escalate hoặc run sau |
| Trần budget | child >8k tokens | tách goal thành 2+ task hẹp hơn |
| Triage trước | scope chưa rõ | researcher trước implementer |

> **Tóm gọn 1 câu:** Spawn là hành động tốn tiền nên phải có cổng: việc rảnh thì thoát sớm, tối đa 3 con mỗi lần chạy, con nào cần hơn 8k token thì tách nhỏ, và điều tra trước khi sửa.

---

## 5. Context và memory

> Phần này giải thích sub-agent ghi chú của mình ở đâu và chia sẻ kết quả thế nào để không ghi đè nhau.

> **📌 Khái Niệm Cơ Bản**
>
> - **Khái niệm:** Scratchpad giữ riêng; chỉ diff/fact publish lên blackboard có version qua CAS. Single-writer mỗi file/section chống race ghi đè.
> - **Ẩn dụ:** Như Google Docs suggestion — mỗi người soạn riêng, chỉ edit được duyệt mới land, edit concurrent thì merge thay vì đè bừa.
> - **Vì sao quan trọng:** Ghi đè mù là bug mất dữ liệu #1 của multi-agent.

(Giải nghĩa: **scratchpad** = giấy nháp riêng của từng agent; **blackboard** = bảng thông báo chung; **CAS** (compare-and-swap) = ghi chỉ khi dữ liệu chưa bị ai đổi — như "ghi đè có điều kiện"; **diff** = bản ghi thay đổi; **single-writer** = một thời điểm chỉ một người được ghi một file.)

### 5.1 Riêng tư mặc định + blackboard

* **Riêng tư theo mặc định:** mỗi sub-agent có scratchpad riêng; chỉ publish diff/fact lên blackboard chung qua `blackboard.write(key, value, expectedVersion)` (CAS, đọc lại + merge khi lệch version, không ghi đè mù).
* **Single-writer:** orchestrator gán quyền sở hữu file/section (vd chỉ `coder` ghi `auth.ts`).
* **Namespace:** key theo `agent_id/task_id/*`; đọc chéo qua projection trong allow-list, không rò prompt/secret thô (`README.md §16.3`).

### 5.2 CAS + single-writer + namespace

<details>
<summary>Python — blackboard có version với CAS</summary>

> 📄 **Code ví dụ:** [`examples/06-5-2-cas-single-writer-namespace.py`](examples/06-5-2-cas-single-writer-namespace.py)

</details>

Handoff tốt vs xấu (handoff = bàn giao việc từ cha sang con):

Cách đọc bảng: cột trái là cách làm **xấu** (đưa quá nhiều — tốn token và rò rỉ); cột phải là cách **tốt** (đưa đúng phần cần). Ví dụ: thay vì dán cả log 40k token, chỉ đưa tóm tắt 5 dòng kèm tham chiếu tới file log.

| ❌ Xấu (dump full) | ✅ Tốt (cắt gọn) |
|---|---|
| Dán 40k-token log cha | parentSummary 5 dòng + 2 files + 1 artifact ref |
| Inline log test 2MB | Artifact ref `s3://.../logs` + hash + 20 dòng fail đầu |
| Share secret thô | Lease scope ngắn + env injection, redact trong log |

> **Tóm gọn 1 câu:** Mỗi sub-agent có giấy nháp riêng, chỉ chia sẻ kết quả qua bảng chung có kiểm tra phiên bản (CAS) — và khi bàn giao thì đưa tóm tắt + tham chiếu, không bao giờ dump cả log.

---

## 6. Cách ly và secret

> **📌 Khái Niệm Cơ Bản**
>
> - **Khái niệm:** Mỗi role phân giải ra cùng một sandbox policy dù chạy solo hay swarm; secret là lease ngắn theo từng agent, không bao giờ share context.
> - **Ẩn dụ:** Như thẻ khóa khách sạn — mỗi thẻ mở một phòng, hết hạn khi checkout, thẻ master không rời quầy lễ tân.
> - **Vì sao quan trọng:** Một agent con quá quyền có thể rò cả repo + secret của run.

### 6.1 Ma trận tool tối thiểu

Cách đọc bảng này: mỗi dòng là một vai trò; các cột cho biết vai đó được phép làm gì với file (FS), lệnh (Shell), mạng (Network), và điều kiện thêm. Ví dụ: `verifier` chỉ được đọc file và chạy test, không được sửa code.

* Cơ chế tier/controls/runner thuộc `12-sandbox-execution` §2–§6; riêng multi/sub-agent bổ sung: **tool tối thiểu theo role** (reviewer chỉ FS đọc, không shell; coder shell sandbox không net), tra cứu cùng ma trận role để solo và swarm phân giải ra cùng policy

> 🔑 **Highlight Policy / Permission:** grant tool cho sub-agent chỉ là **projection permission, không phải policy mới** — mỗi role kế thừa tool tối thiểu từ `12-sandbox-execution` §6, grant nào ngoài ma trận đều bị deny ở validation lúc spawn (§4). (lệch là bug leo thang đặc quyền). (Hiểu đơn giản: cấp tool cho sub-agent không phải là "chế quyền mới" mà chỉ là "chiếu" phần được phép của ma trận ra; xin thừa thì bị chặn ngay lúc spawn.)
* Egress chặn mặc định, allow-list domain từng agent; mọi I/O tool audit kèm `agent_id + lease_id`. (Egress = luồng dữ liệu đi ra ngoài; chặn mặc định nghĩa là không kết nối được tới đâu trừ khi được liệt kê.)
* Code-editing sub-agents: `isolation: worktree` + lock/queue trong state (`"PR #1234 — worktree in progress"`) để tránh hai sub-agents sửa cùng files.

| Role | FS | Shell | Network | Thêm |
|---|---|---|---|---|
| implementer | ghi có phạm vi (worktree) | sandbox, không net | chặn mặc định | bắt buộc worktree lock |
| verifier | đọc + output test | chỉ test runner | chặn mặc định | không được sửa code |
| reviewer | chỉ đọc | không | chặn mặc định | chỉ API comment |
| researcher | chỉ đọc + search | không | allow-list docs | không ghi memory |

> **Tóm gọn 1 câu:** Quyền của sub-agent là "chiếu" từ ma trận role→tool có sẵn, không tự sinh — network chặn mặc định, secret là thẻ khóa khách sạn hết hạn theo lượt, và ai sửa code thì phải có worktree riêng.

### 6.2 Lease secret và audit

* Secret là **lease theo từng agent** (token ngắn hạn theo scope, 5–15p, env injection), supervisor redact `sk-*, ghp_*, AWS_*` khỏi log/transcript; secret của agent này không bao giờ xuất hiện trong context agent khác (`README.md §16.4`).

<details>
<summary>Python — redact + secret theo scope</summary>

> 📄 **Code ví dụ:** [`examples/07-6-2-lease-secret-va-audit.py`](examples/07-6-2-lease-secret-va-audit.py)

</details>

> **Tóm gọn 1 câu:** Secret là "thẻ khóa khách sạn": cấp ngắn hạn 5–15 phút, đúng phạm vi, nạp qua biến môi trường, và luôn bị che trong log.

---

## 7. Gộp kết quả

> Phần này giải thích kết quả của sub-agent được kiểm tra và gộp vào kết quả cuối thế nào.

> **📌 Khái Niệm Cơ Bản**
>
> - **Khái niệm:** Output của maker không đáng tin cho tới khi checker độc lập hoặc quorum duyệt; message nhỏ, có thứ tự, dedupe.
> - **Ẩn dụ:** Như phản biện khoa học — tác giả nộp, hai reviewer vote, editor (aggregator) quyết; phụ lục quá khổ thành link bổ sung (artifact ref).
> - **Vì sao quan trọng:** Tự duyệt việc của mình sinh drift; message không giới hạn thổi phồng context và đảo thứ tự kết quả.

### 7.1 Maker / checker và quorum

* Maker/checker: implementer xong → verifier độc lập chạy test/gates; verdict mặc định REJECT cho tới khi bằng chứng đủ (build OK, test OK, AC trace).
* Quorum: reviewer vote 2-of-3; một voter crash không chặn merge.

<details>
<summary>Python — aggregator quorum</summary>

> 📄 **Code ví dụ:** [`examples/08-7-1-maker-checker-va-quorum.py`](examples/08-7-1-maker-checker-va-quorum.py)

</details>

### 7.2 Đảm bảo messaging

* Payload: header 64KB + body 512KB; lớn hơn → artifact ref. Message có `msg_id` (dedupe), FIFO theo từng task (từ chối `seq` sai thứ tự), request/reply timeout 30s. (Giải nghĩa: **payload** = gói dữ liệu; **dedupe** = loại bỏ tin trùng; **FIFO** = vào trước ra trước — giữ đúng thứ tự.)

Cách đọc bảng này: cột **Đảm bảo** là tính chất phải có của tin nhắn; cột **Cơ chế** là cách thực hiện; cột **Giới hạn** là điều kiện/chỗ yếu. Ví dụ: tin trùng bị loại nhờ so tập `msg_id`.

| Đảm bảo | Cơ chế | Giới hạn |
|---|---|---|
| Dedupe | tập `msg_id` | bỏ trùng |
| Thứ tự | `seq` FIFO mỗi task | từ chối gap/sai thứ tự |
| Kích thước | trần header/body | tràn → artifact ref |
| Liveness | timeout req/reply 30s | timeout → SUSPECT → requeue |

> **Tóm gọn 1 câu:** Kết quả chỉ được gộp khi qua checker độc lập hoặc đa số phiếu; còn tin nhắn giữa các agent thì nhỏ gọn, có mã chống trùng, đúng thứ tự, và quá hạn 30 giây coi như treo.

---

## 8. Budget & cost guards

> Phần này giải thích các "van giới hạn" ngăn sub-agent đốt tiền.

> **📌 Khái Niệm Cơ Bản**
>
> - **Khái niệm:** Mỗi spawn tiêu từ một phong bì có trần; run idle tiêu gần như không; việc quá budget thì tách thay vì phình.
> - **Ẩn dụ:** Như đoàn phim — mỗi cảnh có budget; không có footage actionable → đóng máy sớm, cho crew về.
> - **Vì sao quan trọng:** Fan-out không giới hạn là cách nhanh nhất đốt $50 cho một run cron no-op.

Cách đọc bảng này: cột **Guard** là chốt kiểm soát; cột **Mặc định** là con số/giá trị khởi điểm; cột **Hành vi** là việc hệ thống làm khi chạm chốt. Ví dụ: một lần chạy tối đa 3 sub-agent, dư thì xếp hàng hoặc dời sang lần sau.

| Guard | Mặc định | Hành vi |
|---|---|---|
| Tối đa spawn / run | 3 | queue hoặc dời phần dư |
| Thoát idle | <5k tokens | chỉ triage, không spawn |
| Budget child | 2–8k tokens | tách task nếu lớn hơn |
| Trần step | 10–25 steps | dừng → tóm tắt → escalate |
| Timeout | 120–300s | TIMED_OUT → requeue (max 3) |
| Kill switch | vượt budget run | hủy lease ưu tiên thấp nhất trước |

<details>
<summary>Python — guard budget</summary>

> 📄 **Code ví dụ:** [`examples/09-8-budget-cost-guards.py`](examples/09-8-budget-cost-guards.py)

</details>

> **Tóm gọn 1 câu:** Mỗi spawn tiêu từ một "phong bì" có trần — 3 con mỗi lần chạy, 2–8k token mỗi con, 10–25 bước, 120–300 giây — và có kill switch hủy phần ưu tiên thấp trước khi vượt ngân sách.

---

## 9. Kiểm thử sub-agent

> **📌 Khái Niệm Cơ Bản**
>
> - **Khái niệm:** Test contract, không chỉ test model — validation, fencing, CAS, redaction, phục hồi crash đều có test xác định.
> - **Vì sao quan trọng:** Bug sub-agent là bug concurrency + bảo mật; chỉ lộ khi crash/reorder/input đối kháng.

Cách đọc bảng này: cột **#** là số thứ tự; cột **Test** là tình huống cần thử; cột **Kỳ vọng** là kết quả đúng phải xảy ra. Ví dụ: test số 6 chèn khoá giả `ghp_fake123` vào log — kết quả đúng là chuỗi đó bị che.

| # | Test | Kỳ vọng |
|---|---|---|
| 1 | `validateSpec` từ chối implementer thiếu worktree | danh sách lỗi non-empty |
| 2 | Reviewer có tool `shell` | bị từ chối |
| 3 | Kill child giữa run (mất heartbeat 15s) | DEAD → requeue kèm token++ |
| 4 | Kết quả token cũ tới trễ | bị loại (fencing) |
| 5 | Hai writer cùng key, cùng version | một CAS thắng, một retry |
| 6 | Log chứa `ghp_fake123` | bị redact |
| 7 | Payload kết quả 2MB | artifact ref, không inline |
| 8 | `seq` sai thứ tự | bị từ chối |
| 9 | Verifier sửa code | policy từ chối |
| 10 | Run watchlist idle | <5k tokens, zero spawn |

<details>
<summary>Python — test fencing + CAS</summary>

> 📄 **Code ví dụ:** [`examples/10-9-kiem-thu-sub-agent.py`](examples/10-9-kiem-thu-sub-agent.py)

</details>

> **Tóm gọn 1 câu:** Test sub-agent là test "hợp đồng", không phải test model: 10 tình huống đối kháng (treo, trễ, ghi đè, rò khoá...) đều phải cho kết quả đúng như bảng.

---

## 10. Anti-pattern & giải pháp

> **📌 Khái Niệm Cơ Bản**
>
> - **Khái niệm:** Hầu hết lỗi sub-agent là vi phạm contract với tên ngây thơ: "share hết đi", "tự verify cũng được", "thêm một spawn nữa".
> - **Vì sao quan trọng:** Gọi tên bẫy + fix biến kiến thức truyền miệng thành checklist gate được.

Cách đọc bảng này: cột **Anti-Pattern** là tên cái bẫy; cột **Triệu chứng** là dấu hiệu nhận ra trong log/số liệu; cột **Fix** là cách sửa. Ví dụ: "God child" là sub-agent bị nhồi cả context của cha — nhận ra qua 40k token mỗi lần spawn.

| # | Anti-Pattern | Triệu chứng | Fix |
|---|---|---|---|
| 1 | God child (dump full context) | 40k tokens/spawn | files[] + summary + artifact ref |
| 2 | Tự verify | test yếu vẫn pass | verifier độc lập, mặc định REJECT |
| 3 | Spawn storm | 20 child, bùng $ | max 3/run + queue |
| 4 | Scratchpad chung | fact bị ghi đè | pad riêng + blackboard CAS |
| 5 | Tuồn secret | key trong log child | lease từng agent + redact |
| 6 | Zombie write | kết quả trễ đè fix tốt | check fencing token |
| 7 | Tool creep (reviewer + shell) | `rm -rf` bất ngờ | cổng ma trận role→tool |
| 8 | Treo im lặng | sống, 0 tiến triển, đốt budget | detector SUSPECT 60s + deadline |

> **Tóm gọn 1 câu:** 8 cái bẫy đều là vi phạm contract với cái tên nghe vô hại — nhận ra qua triệu chứng trong log, và fix luôn có sẵn trong bảng.

---

## 11. Triển khai thực tế

> Phần này cho 3 ví dụ thật: cách Claude Code làm, một vòng triage ban đêm, và một "đội debug" 3 agent.

### 11.1 Claude Code — Explore Subagents (Anthropic, 2025)

Explore agent của Claude Code là researcher: nặng đọc, hạn chế ghi, spawn để hỏi đáp codebase. Bài học copy về đây: **tool hẹp + context cắt gọn + gộp độc lập** — child không bao giờ merge, parent quyết.

> 📄 **Code ví dụ:** [`examples/11-11-1-claude-code-explore-subagents-anthropic-2025.py`](examples/11-11-1-claude-code-explore-subagents-anthropic-2025.py)

### 11.2 Loop triage đêm (kiểu `loop/05-multi-loop`)

```text
cron 02:00 → triage (rẻ) → watchlist rỗng? exit <5k
  → else spawn ≤3: researcher ×1 → implementer ×1 (worktree) → verifier ×1
  → quorum 2-of-3 → artifact PR → state ghi lease + verdict
```

Chỉ spawn khi state báo actionable; ngược lại exit rẻ. Đây là cost guard `loop/04-operating` áp cho sub-agent.

### 11.3 Debug Squad (từ README §7.3)

Một researcher khoanh vùng path fail kèm citations, một implementer patch trong worktree, một verifier tái hiện before/after. Shared memory chỉ giữ test fail + artifact ref — không bao giờ full log.

> **Tóm gọn 1 câu:** Ba ví dụ thật cùng một công thức: tool hẹp + context cắt gọn + kiểm tra độc lập — child không bao giờ tự gộp kết quả, luôn là parent quyết.

---

## 12. Checklist & triển khai production

> Phần này là danh sách kiểm tra trước khi cho sub-agent chạy thật. Mục `[ ]` = chưa đánh dấu; đánh dấu khi đã làm và đã kiểm chứng.

### 12.1 Cổng pre-spawn

[ ] Spec đủ §4 (role hẹp, context cắt gọn, tool allow-list, worktree nếu sửa code, budget/timeout/lease) [ ] heartbeat + deadline + detector treo [ ] fencing token khi requeue

### 12.2 Cổng an toàn và chi phí

[ ] max 3 attempts + đường escalate [ ] CAS + single-writer + namespace [ ] secret lease ngắn + redaction + không leak chéo [ ] max 3 spawns/run + kill switch [ ] verifier độc lập, không tự verify

### 12.3 Checklist triển khai

Cách đọc bảng này: cột **Lĩnh vực** là khía cạnh hệ thống cần kiểm; cột **Check** là điều kiện "đạt" của khía cạnh đó. Ví dụ: phần Supervisor đạt khi nó không giữ trạng thái trong bộ nhớ và chạy lại được an toàn.

| Lĩnh vực | Check |
|---|---|
| Supervisor | phi trạng thái, queue-backed, worker idempotent |
| Observability | mọi I/O tool gắn `agent_id + lease_id`; dashboard heartbeat |
| Audit | test redact secret xanh; egress deny-default |
| Rollback | fencing bật; kết quả cũ bị loại |
| Chi phí | trần run + trần từng child + idle-exit đã verify |

> **Tóm gọn 1 câu:** Trước khi chạy production, đi hết 3 cổng: spec đủ thứ, an toàn + chi phí có chốt, và 5 lĩnh vực vận hành đạt check.

---

## Best Practices

> Phần này gom 10 nguyên tắc ngắn — bản "cheat sheet" của toàn bộ spec trên.

1. **Triage trước spawn** — scope chưa rõ thì researcher trước.
2. **Một ticket mỗi child** — tách goal rộng; từ chối child >8k-token.
3. **Cắt context mạnh tay** — summary + ref hơn dump.
4. **Buộc role vào tool** — phân giải từ một ma trận (12-sandbox §6).
5. **Cách ly edit** — worktree + lock mỗi child sửa code.
6. **Mặc định REJECT** — verifier cần build + test + AC trace.
7. **Fence mọi thứ** — check token mỗi kết quả trễ.
8. **Lease secret** — scope 5–15p, env injection, redact log.
9. **Trần message** — payload lớn dùng ref thay inline.
10. **Idle thì exit rẻ** — <5k tokens, zero spawn.

> **Tóm gọn 1 câu:** Nếu chỉ nhớ một dòng: siết mọi thứ sub-agent nhận (context, tool, budget, thời gian) và buộc bên thứ ba kiểm tra kết quả của nó.

## Tài Liệu Tham Khảo

### Frameworks

* Claude Code — subagent tool + permission modes (Anthropic, 2025)
* LangGraph — Supervisor + worker + checkpointing
* AutoGen / CrewAI — ủy quyền theo role (`tools/`)

### Research & Papers

* Anthropic: tool-use + ủy quyền tối thiểu (2025)
* DeepMind: workflow có cấu trúc −45% failure (2025)

### Production Systems

* `README.md §16` — mẫu heartbeat, messaging, isolation
* `12-sandbox-execution §2–§6` — tier, control, ma trận policy role
* `loop/04-operating` — cost guard; `loop/06-anti-patterns` — tách maker/checker
* `08-task` — vòng đời TaskNode link qua `taskId`

### Architecture Patterns

* Maker/Checker, Judge quorum (2f+1), Blackboard (CAS), Lease + Fencing, Worktree isolation

(Giải nghĩa nhanh các pattern: **Maker/Checker** = người viết / người kiểm tách riêng; **Judge quorum 2f+1** = đủ 2f+1 giám khảo để chịu được f cái hỏng; **Blackboard CAS** = bảng chung ghi có kiểm tra phiên bản; **Lease + Fencing** = quyền có hạn dùng + số lượt để loại kết quả cũ; **Worktree isolation** = mỗi agent một thư mục làm việc riêng.)

> **Tóm gọn 1 câu:** Đây là các nguồn để đi sâu thêm; 5 pattern nêu ở cuối là những "hạt nhân ý tưởng" mà toàn bộ spec trên được ghép từ đó.
