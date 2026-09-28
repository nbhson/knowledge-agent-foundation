# 🔐 XV. Approval Gates — Human-in-the-Loop Cho Hành Động Không Đảo Ngược Được

> ## 📑 Mục Lục
>
> - [Opening Story](#opening-story)
> - [Vì Sao Approval Gates Là Bắt Buộc?](#vì-sao-approval-gates-là-bắt-buộc)
> - [Overview](#overview)
> - [Mục Lục Chi Tiết](#mục-lục-chi-tiết)
> - [1. Định Nghĩa & Thuật Ngữ](#1-định-nghĩa--thuật-ngữ)
>   - [1.1 Các thuật ngữ cốt lõi](#11-các-thuật-ngữ-cốt-lõi)
>   - [1.2 Hai họ kỹ thuật: Hard Block vs Advisory Signal](#12-hai-họ-kỹ-thuật-hard-block-vs-advisory-signal)
> - [2. Risk Tier — Cái Gì Cần Gate?](#2-risk-tier--cái-gì-cần-gate)
>   - [2.1 Phân nhóm tier](#21-phân-nhóm-tier)
>   - [2.2 Tag tier lúc plan](#22-tag-tier-lúc-plan)
>   - [2.3 Liệt kê blast radius](#23-liệt-kê-blast-radius)
> - [3. Gate Payload — Human Thấy Gì](#3-gate-payload--human-thấy-gì)
>   - [3.1 Các trường của payload](#31-các-trường-của-payload)
>   - [3.2 Quy tắc bằng chứng bắt buộc](#32-quy-tắc-bằng-chứng-bắt-buộc)
> - [4. Ngữ Nghĩa Timeout, Deny & Escalation](#4-ngữ-nghĩa-timeout-deny--escalation)
>   - [4.1 Bốn outcome](#41-bốn-outcome)
>   - [4.2 Timeout-deny (fail closed)](#42-timeout-deny-fail-closed)
>   - [4.3 Deny → replan, không retry](#43-deny--replan-không-retry)
>   - [4.4 Escalation & ủy quyền](#44-escalation--ủy-quyền)
> - [5. Tích Hợp Engine (Pause / Resume)](#5-tích-hợp-engine-pause--resume)
>   - [5.1 API Gatekeeper](#51-api-gatekeeper)
>   - [5.2 Giao thức PAUSED](#52-giao-thức-paused)
>   - [5.3 Resume & idempotency](#53-resume--idempotency)
>   - [5.4 Enforce two-person rule](#54-enforce-two-person-rule)
> - [6. Audit Log](#6-audit-log)
>   - [6.1 Record](#61-record)
>   - [6.2 Phát hiện vi phạm policy](#62-phát-hiện-vi-phạm-policy)
> - [7. UX Cho Human-in-the-Loop](#7-ux-cho-human-in-the-loop)
>   - [7.1 Batching & mệt mỏi ra quyết định](#71-batching--mệt-mỏi-ra-quyết-định)
>   - [7.2 Kênh thông báo](#72-kênh-thông-báo)
> - [8. Implementation TypeScript](#8-implementation-typescript)
>   - [8.1 Types](#81-types)
>   - [8.2 Gatekeeper có persist](#82-gatekeeper-có-persist)
>   - [8.3 Tích hợp vòng lặp engine](#83-tích-hợp-vòng-lặp-engine)
>   - [8.4 Two-person gatekeeper](#84-two-person-gatekeeper)
> - [9. Kiểm Thử Approval Gates](#9-kiểm-thử-approval-gates)
>   - [9.1 Test bất biến](#91-test-bất-biến)
>   - [9.2 Contract test](#92-contract-test)
>   - [9.3 Bộ hồi quy](#93-bộ-hồi-quy)
> - [10. Case Study Thực Tế](#10-case-study-thực-tế)
>   - [10.1 Claude Code — Permission mode & xác nhận](#101-claude-code--permission-mode--xác-nhận)
>   - [10.2 Aider — Read/Write mode như deny-by-default](#102-aider--readwrite-mode-như-deny-by-default)
>   - [10.3 OpenHands — Confirmation mode](#103-openhands--confirmation-mode)
>   - [10.4 Devin — Giám sát không đồng bộ](#104-devin--giám-sát-không-đồng-bộ)
>   - [10.5 Nghiên cứu delegation người-máy — automation bias](#105-nghiên-cứu-delegation-người-máy--automation-bias)
> - [11. TypeScript Interfaces Cho Approval](#11-typescript-interfaces-cho-approval)
> - [12. Nguyên Tắc Thiết Kế Cho Approval](#12-nguyên-tắc-thiết-kế-cho-approval)
>   - [12.1 SOLID cho hệ approval](#121-solid-cho-hệ-approval)
>   - [12.2 Sáu nguyên tắc thiết kế](#122-sáu-nguyên-tắc-thiết-kế)
> - [13. Best Practices](#13-best-practices)
>   - [13.1 NÊN ✅](#131-nên-)
>   - [13.2 KHÔNG NÊN ❌](#132-không-nên-)
> - [14. Anti-Patterns & Cách Khắc Phục](#14-anti-patterns--cách-khắc-phục)
> - [15. Production Checklist](#15-production-checklist)
> - [16. Xu Hướng Tương Lai](#16-xu-hướng-tương-lai)
> - [Tài Liệu Tham Khảo](#tài-liệu-tham-khảo)
>
> **Module cross-cutting.** Approval gate là nơi duy nhất trong harness mà con người tham
> gia vào *vòng thực thi*, không chỉ phần setup. Mọi module khác giả định run có thể tự
> quyết và tự hành động; module này lắp cửa dừng có chủ đích — bảo hiểm incident rẻ nhất
> của cả harness (→ 12 §1.2, → 06 §17.4).

---

### Opening Story

3 giờ 47 phút sáng. Một run migration đã chạy sáu tiếng. Agent, tự tin và đang ở lượt
thứ 214, vừa tách một retry `db.migrate` đang treo và cho rằng nó "kẹt ở các bước tăng
dần," nên nó dựng một lộ trình cứu hộ: `ALTER TABLE users DROP COLUMN mfa_secret` — vì
một check ở dưới báo column đang `NOT NULL` không có default, và mô hình "gỡ blocker"
của agent thắng.

Column đó chứa 2,1 triệu enrollment MFA. Không có backup. Hành động đó không đảo ngược
được, mang tính hủy diệt, và *sai*.

Thứ phân biệt chuyện này với một headline incident là một quyết định harness chọn sớm
hơn: **tag `prod-auth` lúc plan, đóng băng run, và cho human thấy bằng chứng "trước",**
không phải suy luận của mô hình. Gate nổ. Human lúc 3:47 sáng nhìn một diff 12 dòng, nói
"không", gõ một lý do, và hai mươi phút sau agent replan quanh thay đổi đó — *mà chưa
từng chạm tới column*.

Gate không làm agent thông minh hơn. Nó làm harness *an toàn khi sai* — đây là tính
chất duy nhất đáng có với hệ tự trị. Mọi hành động quá tự tin suýt xảy ra mà human chặn
lại đều vô hình trong metrics, tốn không xu nào, và là toàn bộ ý nghĩa.

### Vì Sao Approval Gates Là Bắt Buộc?

> *"Một agent tự tin xin được credential production lúc 3 giờ sáng và được nhận, không
> phải là agent. Đó là một khẩu pháo không cần nạp đạn."*

#### Phép tính của sự sai lầm tự tin

LLM agent sai với tỉ lệ không hề nhỏ và *không bao giờ biết mình sai* — các nghiên cứu
calibration liên tục cho thấy overconfidence tăng theo độ dài context và độ sâu plan
(→ 10.5). Đặt điều đó vào blast radius của các hành động agent được yêu cầu thực hiện:

| Hành động | Tỉ lệ sai của *quyết định* | Nếu sai, blast radius |
|-----------|------------------------------|------------------------|
| `edit_file` trong `src/` | cao (API hallucinate, sai file) | đảo ngược cục bộ qua git |
| `db.migrate` trên prod | thấp nhưng *thảm khốc khi sai* | schema không thể undo, giờ rollback |
| `user.delete` / đổi IAM | hiếm | vĩnh viễn, danh tính + compliance |
| `git push --force` | tần suất thấp, độ mới cao | lịch sử chung bị viết lại, blast đa repo |

Các failure mode giết công ty không phải là loại thường gặp — mà là loại hiếm có chi
phí áp đảo toàn bộ phân phối. Gate là một *lính gác ở đuôi đắt tiền*, và nó gần như
không tốn gì trên đuôi rẻ và thường gặp (tier `read` auto-approve).

Lực thứ hai, tinh tế hơn: **một gate human-in-the-loop thay đổi hành vi agent, không chỉ
kết quả.** Mô hình được dạy rằng hành động không đảo ngược cần có approval nhìn thấy
được, audit được, từ bên thứ hai, suy luận sẽ thận trọng hơn một cách đo được — chúng
ngừng "ứng biến" lộ trình hủy diệt vì biết plan sẽ được *trình ra*, không chỉ thực thi.
Gate là răn đe trước khi là tường lửa.

#### Triết lý cốt lõi

Approval **không** phải "hỏi human mọi thứ" và **không** phải "không bao giờ hỏi." Nó
là: *tag rủi ro lúc plan, khoanh blast radius bằng bằng chứng bắt buộc, và để lỗi kêu
to và audit được thay vì lặng lẽ và đắt đỏ.* Gate nên là điểm hệ thống *được thiết kế
để fail* — để khi agent sai — và nó sẽ sai — thì sự sai đó rẻ và hiển nhiên.

## Overview

> **📌 Khái Niệm Cốt Lõi**
>
> - **Khái niệm:** Approval gate là điểm dừng trước hành động không đảo ngược được hoặc blast radius lớn: execution đóng băng, human thấy *cái gì / vì sao / ảnh hưởng / rollback*, run chỉ tiếp tục khi approve (hoặc replan khi deny/timeout).
> - **So sánh:** Như két ngân hàng cần hai chìa — agent giữ một (plan), human giữ một (phán đoán). Một chìa không mở được gì.
> - **Vì sao quan trọng:** Agent sai với vẻ tự tin. Không gate, một `prod.db.drop()` hay `git push --force` hallucinate lúc 3 giờ sáng thành incident. Gate là bảo hiểm incident rẻ nhất cả harness.

**Approval Gates** là control plane cho các hành động có chi phí hỏng hóc vượt độ tin
cậy quyết định của agent. Chúng bổ trợ trực tiếp cho sandbox: sandbox (→ 12) khoanh
*agent có thể làm gì*, gate quyết *một human đáng tin phải thấy gì trước khi nó xảy ra*.
Một là trần kỹ thuật; một là hợp đồng xã hội.

```
AGENT MUỐN HÀNH ĐỘNG
     │
     ▼
┌──────────────────────────────────────────────┐
│ CHECK TIER lúc plan (→ 04 §14.3)             │
│ read        → auto-approve, chỉ log          │
│ write       → diff preview + 1 click, 5 phút │
│ elevated    → typed confirm + dry-run        │
│               + rollback, 30 phút            │
│ prod-auth   → TWO-PERSON rule, 4h + page     │
└──────────────────────────────────────────────┘
     │ nếu tier ≥ write
     ▼
┌──────────────────────────────────────────────┐
│ GATE MỞ                                     │
│ 1. payload được dựng (cái gì/vì sao/blast/   │
│    rollback)                                 │
│ 2. engine PAUSED tại checkpoint (→ 07 §13)   │
│ 3. cuộc đua timeout-deny được nạp đạn        │
│ 4. ghi audit record (nối hash, → 13)         │
└──────────────────────────────────────────────┘
     │
     ▼
 HUMAN -> approve ──────────────▶ resume cùng runId
       │  -> deny + lý do ───────▶ replan loại nhánh
       │  -> không verdict ─────▶ timeout → deny (fail closed)
       │  -> escalated ────────▶ page on-call, ủy quyền kèm trail
```

**Gate có vòng đời, không phải boolean:** một `request()`, ba outcome đã chốt
(`approved` / `denied` / `expired`), một audit trail, không nhánh lặng lẽ. Bất kỳ
implementation nào không trả lời được "ai, cái gì, khi nào, vì sao *cho mọi hành động
không đảo ngược*" đều không phải hệ approval — nó là một nút bấm có thêm bước.

## Mục Lục Chi Tiết

| # | Chủ đề | Mô tả |
|---|-------|-------|
| 1 | [Định nghĩa](#1-định-nghĩa--thuật-ngữ) | Thuật ngữ và hai họ kỹ thuật |
| 2 | [Risk tier](#2-risk-tier--cái-gì-cần-gate) | Cái gì cần gate, tag lúc plan |
| 3 | [Gate payload](#3-gate-payload--human-thấy-gì) | Human thấy gì, bằng chứng bắt buộc |
| 4 | [Timeout & deny](#4-ngữ-nghĩa-timeout-deny--escalation) | Fail-closed, replan, escalation |
| 5 | [Pause / resume](#5-tích-hợp-engine-pause--resume) | Tích hợp engine, giao thức PAUSED, idempotency |
| 6 | [Audit log](#6-audit-log) | Record bất biến và vi phạm policy |
| 7 | [UX human](#7-ux-cho-human-in-the-loop) | Batching, mệt mỏi ra quyết định, thông báo |
| 8 | [Implementation](#8-implementation-typescript) | Gatekeeper chạy được + vòng lặp engine |
| 9 | [Kiểm thử](#9-kiểm-thử-approval-gates) | Bất biến + contract test |
| 10 | [Case study](#10-case-study-thực-tế) | Claude Code, Aider, OpenHands, Devin, automation bias |
| 11 | [TypeScript Interfaces](#11-typescript-interfaces-cho-approval) | Toàn bộ bề mặt kiểu |
| 12 | [Nguyên tắc thiết kế](#12-nguyên-tắc-thiết-kế-cho-approval) | SOLID cho approval |
| 13 | [Best practices](#13-best-practices) | NÊN / KHÔNG NÊN |
| 14 | [Anti-patterns](#14-anti-patterns--cách-khắc-phục) | Lỗi thường gặp |
| 15 | [Production checklist](#15-production-checklist) | Cổng ship |
| 16 | [Xu hướng tương lai](#16-xu-hướng-tương-lai) | 2026-2028 |

---

## 1. Định Nghĩa & Thuật Ngữ

### 1.1 Các Thuật Ngữ Cốt Lõi

| Thuật ngữ | Định nghĩa | Hỏng khi… |
|-----------|-----------|-----------|
| **Approval gate** | Node workflow ở trạng thái `WAITING_APPROVAL`; persist, notify, resume khi có verdict | chỉ trong memory → mất khi restart |
| **Blast radius** | Tập tài nguyên bị ảnh hưởng nếu action chạy (file, DB, env, user) — liệt kê rõ ràng | mơ hồ ("đồ prod") → human không đánh giá được |
| **Dry-run** | Preview không side effect của action (plan diff, `terraform plan`, `--dry-run`) — bắt buộc trong gate payload | bỏ qua → approval là mù |
| **Timeout-deny** | Hết TTL không verdict → tính là **deny** (fail closed), không bao giờ là approve | fail-open → "tôi định approve mà" |
| **Two-person rule** | Người đề xuất ≠ người duyệt; một second human độc lập quyết định | tự duyệt → thành không có gate |
| **Deny → replan** | Deny ghi `reason` và trigger replanning loại nhánh bị deny (→ 04 §14.2) | deny → retry lại → lặp vô hạn |
| **Approval event** | Mọi request + verdict được ghi vào trajectory thành `approval_request` / `approval_verdict` (→ 13) | không trace → review sau incident bất khả thi |

### 1.2 Hai Họ Kỹ Thuật: Hard Block vs Advisory Signal

Có hai *cơ chế khác nhau* trông giống nhau và thường bị trộn lẫn, gây hại:

| | **Hard block (gate)** | **Advisory signal** |
|---|---|---|
| **Làm gì** | Đóng băng run tới khi có verdict | Cảnh báo user, vẫn chạy tiếp |
| **State machine** | `request → WAITING_APPROVAL → settle` | banner / toast / dòng bôi màu |
| **Dùng cho** | Hành động không đảo ngược, tốn kém, blast lớn | Pattern nghi vấn-nhưng-đảo ngược được |
| **Nếu bỏ qua** | run không đi tiếp | run đi tiếp kèm ghi chú hiển thị |
| **Audit** | record request + verdict đầy đủ | tùy chọn, thường không có |
| **Chi phí** | attention của human, latency thật | gần trừ không |
| **Nguy hiểm** | over-gate → approval fatigue (→ 7.1) | under-gate → incident kiểu "chúng tôi đã cảnh báo" |

Cái bẫy là trộn hai thứ: biến advisory signal thành hard block (mỗi `npm install` thành
một click → human stamp máy móc → gate *thật* bị approve theo muscle memory), hoặc biến
hard block thành advisory signal ("xác nhận nhưng run vẫn chạy"). Chọn một cho mỗi action.
Gate là gate là gate.

---

## 2. Risk Tier — Cái Gì Cần Gate?

### 2.1 Phân Nhóm Tier

| Tier | Ví dụ | Gate |
|------|----------|------|
| `read` (thấp) | `read_file`, `grep`, `list`, `view` | Auto-approve, chỉ log |
| `write` (trung bình) | `edit_file` trong `src/`, `run_tests`, commit local | Diff preview + approve một click, hết hạn 5 phút |
| `elevated` (cao) | `db.migrate`, `deploy`, `user.delete`, `external.send`, `push --force`, `rm -rf` | Typed confirm + lý do + dry-run + lệnh rollback, hết hạn 30 phút |
| `prod-auth` (critical) | Đổi IAM, xoay secret, xóa dữ liệu prod, hành động payment/legal | Two-person rule (người đề xuất ≠ người duyệt) + báo kênh incident, 4h + page |

**Tier là thuộc tính của *lớp hành động*, không phải của từng lời gọi.** Push lên feature
branch là `write`; force-push lên `main` là `elevated`; force-push lên branch `release/*`
dùng chung là `prod-auth`. Mapping nằm trong bảng permission/risk (`permission.ts`), được
cập nhật trong review — không bao giờ suy ra từng message bởi mô hình.

### 2.2 Tag Tier Lúc Plan

Tier được gán **lúc plan** (→ 04 §14.3), không phải lúc thực thi:

1. Planner phát ra mỗi task/tool kèm một trường `tier` tường minh.
2. Engine kiểm tra tier với một risk table toàn cục trước khi step dựng payload.
3. Model không thể tự hạ tier — yêu cầu "chạy nó như `write` thôi" không phải đường
   policy hợp lệ; đổi tag là thay đổi policy, phải đến từ chủ sở hữu risk table.

> **Quy tắc:** *agent đề xuất, engine enforce, human override chỉ qua một lý do được
> ghi lại.* Tag-lúc-plan là thứ làm cho ba chiều tách rời đó khả thi — không có nó, mô
> hình tự chọn gờ giảm tốc của chính mình và chọn cái nó có thể phớt lờ.

```
Lúc plan (→ 04)      Lúc dựng (→ 08)          Lúc thực thi (→ 07)
┌────────────────┐   ┌─────────────────┐        ┌─────────────────────┐
│ task 3          │   │ toolbox (→ 06)   │        │ task 3 tới,         │
│  tier write      │   │  tier từ         │        │ check risk table    │
│ task 5          │   │  permission.ts   │        │ tier=write ok       │
│  tier elevated   │──▶│  + per-role      │───────▶│ task 5 tier=elevated│
│ task 8          │   │  override        │        │ → GATE REQUESTED    │
│  tier prod-auth  │   │  (audited)       │        └─────────────────────┘
└────────────────┘   └─────────────────┘
```

### 2.3 Liệt Kê Blast Radius

Gate payload chỉ tốt ngang độ chính xác của việc liệt kê blast radius. Hệ thống phải
liệt kê, từ registry sandbox/policy (→ 12 §6), tập chính xác các tài nguyên action chạm
tới:

```
ACTION:   db.migrate 20260719_add_mfa_cols (tier: elevated)
BLAST:    prod-db.host=postgres-5a2f (primary, không replica cho schema này)
          database=users  size=2.1M rows
          table migration lock ~4s (cửa sổ downtime: ok)
          0 down migrations — KHÔNG đảo ngược được bởi engine migration
          microservices liên kết: auth-svc (read), consent-svc (write)
```

Các kiểu hỏng của việc liệt kê:

| Lỗi | Ví dụ | Cách sửa |
|---------|---------|-----|
| Quá thô | "sửa prod database" | db, host, size, lock estimate chính xác |
| Thiếu blast | quên service liên kết | liệt kê theo registry, không do model viết |
| Nhầm với cost | "tốn $0.40" nhưng không có lock time | cost là một *dòng* trong payload, không phải blast radius |
| Rollback không chứng minh | "rollback: revert migration" không test | trường `rollback` phải mang lệnh/hash đã test |

---

## 3. Gate Payload — Human Thấy Gì

### 3.1 Các Trường Của Payload

```
ACTION:   db.migrate (tier: elevated)
TASK:     auth-refactor / step 3 (trajectory: traj_x, event: evt_41)
DIFF:     +ALTER TABLE users ADD COLUMN mfa_secret TEXT (12 lines…)
BLAST:    prod-db.users (2.1M rows), lock ~4s, 0 down migrations
DRY-RUN:  ✓ shadow-migrate passed (3.8s), rollback tested
ROLLBACK: db.migrate down v48 (lệnh đính kèm, đã test 2h trước)
COST:     ~$0.40, ~90s                       [Approve] [Deny + reason]
```

Mỗi trường phải **suy ra từ bằng chứng**, không phải kể chuyện:

| Trường | Nguồn | Thiếu → |
|-------|--------|----------|
| `ACTION` + `tier` | tag tier của step (→ 2.2) | gate không dựng được |
| `TASK` + link trajectory | node plan graph + span id (→ 04, 13) | review sau incident không replay được |
| `DIFF` | lệnh/diff thực đã materialize | approve là mù |
| `BLAST` | liệt kê theo registry (→ 2.3) | human đánh giá thấp |
| `DRY-RUN` | *output* của dry-run, nối hash | approve là hành động đức tin |
| `ROLLBACK` | lệnh rollback đã test + thời điểm test | approve cam kết vào sự không thể undo |
| `COST` | token/tiền/thời gian ước tính | human không so được lựa chọn |

### 3.2 Quy Tắc Bằng Chứng Bắt Buộc

> **Không dry-run → không gate → action bị chặn.** Gate từ chối mở nếu bất kỳ trường
> bằng chứng bắt buộc nào rỗng. Đây *không* phải sự tử tế về UX — đây là invariant làm
> cho approval khác với sự đồng thuận (consent).

Về mặt implementation, đây là hàm validate chạy *trước* khi `request()` được gọi:

```typescript
export function validatePayload(r: GateRequest): string[] {
  const missing: string[] = [];
  if (!r.diff)                  missing.push("diff");
  if (r.blastRadius.length === 0) missing.push("blastRadius");
  if (!r.dryRun)                missing.push("dryRun");      // bằng chứng, không phải tóm tắt
  if (!r.rollback)              missing.push("rollback");
  if (!r.expiresAt || r.expiresAt <= Date.now()) missing.push("expiresAt");
  return missing;
}
```

Một `request()` với mảng `missing` không rỗng sẽ ném lỗi; run **không thể** đi tiếp tới
khi bằng chứng tồn tại. Các đội cho phép "approve anyway" trên payload sai consistently
phát hiện ra rằng nút approve thành *phương tiện đăng bài cho hành động chưa được xem xét*.

Payload bản thân nó là trajectory event (→ 13), nên review sau incident replay đúng cái
human đã thấy — kể cả output dry-run đã biện minh (hoặc không biện minh được) cho verdict.

---

## 4. Ngữ Nghĩa Timeout, Deny & Escalation

### 4.1 Bốn Outcome

| Outcome | Ý nghĩa | Trạng thái tiếp theo |
|---------|---------|-----------|
| `approved` | human xác minh bằng chứng, run tiếp tục | chạy tiếp trên cùng `runId`, idempotency cache bỏ qua các step đã xong |
| `denied` | human từ chối kèm lý do | task mark `blocked(denied)`, replan loại nhánh |
| `expired` | không verdict trong TTL | xử lý *đúng như deny* (fail closed), trừ khi được escalate |
| `escalated` | TTL vượt ngưỡng và đã page on-call | TTL mới, chuỗi delegation được ghi |

State machine nhỏ và đóng; bất kỳ implementation nào "sinh ra" outcome mới lúc runtime
(ví dụ *"user nói ok trên Slack"*) là lỗ hổng policy, không phải tính năng.

### 4.2 Timeout-Deny (Fail Closed)

`write` 5 phút · `elevated` 30 phút · `prod-auth` 4h + page.

- Hết hạn mark task `blocked(approval-timeout)` — trạng thái riêng biệt với `denied`,
  vì *hành động kế tiếp* khác nhau (xem 4.3).
- **Fail closed, không bao giờ fail open.** Hết hạn không bao giờ được diễn giải thành
  approve. Ngoại lệ duy nhất cần có chữ ký policy tường minh: cửa sổ deploy unattended
  trong giờ đóng cửa, với timeout được tài liệu hóa là "hết hạn = rollback + page".
- Đồng hồ hết hạn chạy trong *engine*, không phải trong phiên UI. Đóng laptop review
  không thể kéo dài đời sống của gate.

```typescript
// hậu quả fail-closed của việc hết hạn
export function onExpire(key: string, g: Gate): void {
  g.verdict = "expired";
  traj.append({ kind: "approval_verdict", payload: { key, verdict: "expired",
    reason: "ttl_elapsed", at: Date.now() } });
  plan.markBlocked(g.taskId, "approval-timeout");
  replanner.excludeBranch(g.taskId);   // → 04 §14.2
}
```

### 4.3 Deny → Replan, Không Retry

- Ghi `reason` — đây là artifact audit *giá trị nhất* trong cả gate: nó cho planner sau
  biết human từ chối thứ gì, và deny lặp lại cùng lý do là tín hiệu sản phẩm (agent cứ
  đề xuất thứ đội không muốn).
- Trigger replanning loại nhánh bị deny (→ 04 §14.2). Không bao giờ hỏi lại cùng payload
  hai lần. Nếu *cùng* plan có thể thỏa mãn deny theo cách khác, planner phát plan mới;
  plan mới sinh gate mới chỉ khi action mới lại cao tier.
- Hỏi lại y hệt hành động sau deny là lý do **#1** khiến hệ approval trở nên đáng khinh,
  và lý do **#1** khiến user bypass bằng việc approve "chỉ để hết ồn."

### 4.4 Escalation & Ủy Quyền

- **Page on-call** nếu `elevated` treo gate >15 phút trong giờ prod (hoặc >T cho
  non-prod, cấu hình được). Run đóng băng nguyên vẹn tại checkpoint (→ 07 §13);
  checkpoint chính là tính chất an toàn làm cho escalation miễn phí.
- **Ủy quyền approve** được phép (on-call → secondary) — nhưng *ủy quyền tách biệt với
  two-person rule*: delegating thông báo không biến một approver thành hai. Với
  `prod-auth`, delegation giữ nguyên yêu cầu hai người (proposer + một approver độc lập);
  nó có thể đổi *ai* là approver, không bao giờ đổi *bao nhiêu*.
- Mỗi chặng của chuỗi escalation (`paged_oncall` → `delegated_to:x` → `approved`) là một
  mục audit. Chuỗi đó là thứ làm "ai thực sự quyết định?" trả lời được khi bị soát.

---

## 5. Tích Hợp Engine (Pause / Resume)

### 5.1 API Gatekeeper

```typescript
type Verdict = "approved" | "denied" | "expired";
interface GateRequest {
  key: string; tier: "write" | "elevated" | "prod-auth";
  summary: string; diff: string; blastRadius: string[];
  dryRun: string; rollback: string; expiresAt: number;
}
export class Gatekeeper {
  private gates = new Map<string, { req: GateRequest; verdict?: Verdict }>();
  request(r: GateRequest): void {
    ensureValid(r);                          // quy tắc bằng chứng bắt buộc (§3.2)
    this.gates.set(r.key, { req: r });       // engine throws PAUSED:<key>
    setTimeout(() => this.settle(r.key, "expired"), r.expiresAt - Date.now());
  }
  settle(key: string, v: Verdict, by = "human"): void {
    const g = this.gates.get(key); if (!g || g.verdict) return;  // một verdict thắng
    g.verdict = v; // audit: { key, v, by, at: Date.now() } → trajectory (→ 13)
  }
  verdict(key: string): Verdict | undefined { return this.gates.get(key)?.verdict; }
}
// Engine loop: trước khi chạy gated step → gatekeeper.request(...) → checkpoint
// → throw PAUSED → verdict approved: resume; denied/expired: mark blocked → replan.
```

### 5.2 Giao Thức PAUSED

Engine **không** "chờ đợi." Nó throw một `PAUSED:<key>` có kiểu sau khi checkpoint:

- **Checkpoint trước, rồi mới throw.** Mọi step đã xong nằm trong idempotency cache và
  trajectory store (→ 07 §13, → 13). Pause *không* checkpoint nghĩa là resume không phân
  biệt được "chưa từng chạy" với "chạy rồi dở chừng."
- `PAUSED:<key>` truyền lên driver/CLI/UI như một state hạng nhất, không phải lỗi. Cú
  "approve" của human là *giao verdict*, không phải khởi động lại.
- **Run object sống tiếp.** Gate sống sót qua chết process: khi restart, Gatekeeper nạp
  lại các gate đang mở từ trajectory store, nạp lại timer, và mọi run vẫn dính ở
  checkpoint `WAITING_APPROVAL` sẽ resume hoặc expire đúng cách.

```
turn 214  pre_gate_check ──────▶ tier=elevated
    │
    ▼
checkpoint(runId, "t214")      ──▶ trajectory: snapshot_link
    │
    ▼
gatekeeper.request(key=gate_9a3f, …)
    │ phát approval_request { key, tier, diffHash, dryRunHash, expiresAt }
    │ ghi audit record
    │ throw PAUSED:gate_9a3f
    │
    ▼       [process restart? nạp lại gate đang mở, nạp lại timer]
    │
    ▼   human settle gate_9a3f = approved
    │
    ▼
resume(runId) ──▶ replay cache hit cho t1..t214 ──▶ t215 đi tiếp
    (hoặc)    ──▶ denied/expired ──▶ mark blocked → replan (→ 04 §14.2)
```

### 5.3 Resume & Idempotency

- Resume gọi lại run với **cùng `runId`**; step đã xong hit idempotency cache và skip
  (→ 07 §13, 08 §11). Không gì thực thi lại, không gì hỏi lại.
- Bản thân action được gate lại chạy **chỉ sau** approval, đúng một lần — checkpoint nằm
  *trước* action, nên resume chạy lại action, không phải băng qua ranh giới.
- Idempotency của *approval*: settle cùng key hai lần là no-op (`if (!g || g.verdict)
  return`). Một cú "approve" click kép không thể chạy migration hai lần.

### 5.4 Enforce Two-Person Rule

Gate `prod-auth` yêu cầu một đôi mắt human thứ hai có danh tính khác người đề xuất:

```typescript
// engine từ chối materialize action tới khi một human KHÁC approve
export function tryApprove(key: string, approverId: string, reason?: string): boolean {
  const g = gates.get(key); if (!g || g.verdict) return false;
  if (g.req.actorId === approverId) {
    traj.warn({ kind: "approval_policy", payload: { key, detail: "self_approval_rejected" } });
    return false;                                  // proposer ≠ approver, cứng
  }
  gates.get(key)!.actorApproval = approverId;      // human độc lập thứ hai xác nhận
}
```

Người đề xuất được ghi lúc `request()` (chính step sinh ra gate). Quy tắc được enforce
*trong* `tryApprove`, nên không có đường mô hình vòng qua. Cố tự duyệt không im lặng —
nó được audit như một policy event, chính nó là tín hiệu hành vi kỳ lạ đáng theo dõi.

---

## 6. Audit Log

### 6.1 Record

Mỗi gate ghi record bất biến: `{key, tier, actor(proposer), approver, verdict, reason,
diffHash, dryRunHash, at}` → trajectory store (→ 13) + SIEM.

| Trường | Ý nghĩa | Cần cho |
|-------|---------|-------------|
| `key` | gate id không tiết lộ | join request/verdict |
| `tier` | risk tier | approval-rate analytics (→ 9.3) |
| `actor` | người đề xuất (ai trigger run) | two-person rule |
| `approver` | ai settle | chuỗi delegation, two-person rule |
| `verdict` | approved/denied/expired | outcome analytics |
| `reason` | text tự do của human | replan input, tín hiệu sản phẩm |
| `diffHash` | hash của diff đã hiển thị | chứng minh đã approve cái gì |
| `dryRunHash` | hash của bằng chứng dry-run đã hiển thị | chứng minh bằng chứng tồn tại |
| `at` | timestamp | latency, pattern theo giờ |

Cặp `diffHash`/`dryRunHash` là trái tim của audit: nó làm cho việc "approve một *hành
động khác* với hành động được hiển thị" không thể rửa tiền. Nếu payload dựng lúc request
hash ra X mà hành động thực thi hash ra Y ≠ X, đó là incident cứng, được flag tự động.

### 6.2 Phát Hiện Vi Phạm Policy

Các check tự động trên dòng audit:

- Gate approve **không** có `dryRunHash` → vi phạm policy, flag + page (trừ khi lớp hành
  động nằm trong allowlist "no-dry-run" tường minh, bản thân allowlist phải được duyệt).
- `approver === actor` trên gate `prod-auth` → vi phạm (tự duyệt).
- Verdict ghi **sau khi** action đã chạm tài nguyên → vi phạm (approval mất thứ tự).
- Timeout-deny mà tiếp theo là một *request giống hệt* trong vòng X phút → vi phạm
  deny→no-retry (→ 4.3).

Nhịp review hàng quý: approval rate theo tier, wait trung vị, override incidents, độ sâu
chuỗi delegation. Mục đích review không phải kiểm soát — nó là *trí tuệ thiết kế*: một
tier với approval rate 98% và wait trung vị 30 giây không được đọc, nó bị stamp máy móc,
và gate đã thành kịch (→ 14).

---

## 7. UX Cho Human-in-the-Loop

### 7.1 Batching & Mệt Mỏi Ra Quyết Định

Human là tài nguyên khan hiếm và đắt; mục tiêu thiết kế là *tối thiểu token attention của
con người trên mỗi quyết định an toàn*.

- **Một thông báo cho mỗi quyết định**, không phải mỗi action — gộp các edit tier
  `write` thành một diff review được khi chúng thuộc cùng một step.
- **Context, không phải chuyện vặt.** Hiện *task nó thuộc về*, *pha của plan*, *lần thử
  trước* — để một cú "deploy" approve trong lúc run đã diễn tập đọc khác với một cú
  deploy giữa refactor.
- **Hướng dẫn mặc định**: payload nên làm cho quyết định *đúng* thành dễ nhất. Nếu câu
  trả lời đúng thường là "deny", đường approve tốn nhiều friction hơn, không phải ít
  (typed confirm + reason trên `prod-auth`).
- **Mệt mỏi là failure mode lặng lẽ #1** — đo như approval rate tăng cùng thời gian
  quyết định giảm. Khi điều đó xảy ra, gate không còn bảo vệ; nó đang tool đồng ký. Sửa
  bằng cách *nâng* thanh tier, không phải bỏ gate.

### 7.2 Kênh Thông Báo

| Tier | Kênh | Giọng |
|------|---------|------|
| `write` | in-app/PR comment; lặng lẽ, gộp | thông tin |
| `elevated` | push + email, có thể hành động | cần chú ý, ngân sách 30 phút |
| `prod-auth` | kênh incident + page; two-person | escalation, TTL 4h |

Mỗi thông báo mang *cùng* payload mà UI hiển thị (diff, blast, dry-run hash) — không kênh
nào cắt bớt bằng chứng, vì kênh bị cắt bớt lặng lẽ hạ chất lượng quyết định. Việc giao
thông báo được trace (`notification_sent` event → 13) để "human không bao giờ thấy nó"
là một claim kiểm chứng được, không phải lời bào chữa.

---

## 8. Implementation TypeScript

### 8.1 Types

```typescript
export type Tier = "read" | "write" | "elevated" | "prod-auth";
export type Verdict = "approved" | "denied" | "expired";
export type GateState =
  | { status: "waiting" }
  | { status: "settled"; verdict: Verdict; by: string; at: number };

export interface Gate {
  key: string;
  taskId: string;                 // node plan graph (→ 04)
  runId: string;                  // cho resume idempotency (→ 07 §13)
  tier: Tier;
  actorId: string;                // proposer (two-person rule)
  summary: string;
  diff: string;
  blastRadius: string[];
  dryRun: string;
  rollback: string;
  diffHash: string;
  dryRunHash: string;
  createdAt: number;
  expiresAt: number;
  state: GateState;
}

export interface RiskTableEntry {
  action: string;                 // registry key, ví dụ "db.migrate"
  defaultTier: Tier;
  paths?: RegExp[];               // ví dụ force-push trên "release/*"
  noDryRunAllowlist?: boolean;    // bản thân phải được duyệt policy
}
```

### 8.2 Gatekeeper Có Persist

<details>
<summary>TypeScript Code — Gatekeeper có persist + reload + audit (bấm để mở/thu gọn)</summary>

```typescript
import { randomBytes, createHash } from "node:crypto";

export class Gatekeeper {
  private gates = new Map<string, Gate>();
  constructor(
    private store: TrajectoryStore,          // audit/độ bền (→ 13)
    private risk: RiskTableEntry[],          // registry tier
  ) {
    this.reloadOpen();                       // sống sót qua restart
  }

  private key(): string { return `gate_${randomBytes(4).toString("hex")}`; }

  /** Validate tier + bằng chứng, persist, nạp đạn timer fail-closed. */
  request(input: Omit<Gate, "key" | "state" | "createdAt" | "diffHash">
      | { diff: string; dryRun: string }): Gate {
    const missing = validatePayload(input);              // §3.2 bằng chứng bắt buộc
    if (missing.length) throw new Error(`gate missing evidence: ${missing.join(",")}`);
    const gate: Gate = {
      ...input, key: this.key(), createdAt: Date.now(), state: { status: "waiting" },
      diffHash: createHash("sha256").update(input.diff).digest("hex"),
      dryRunHash: createHash("sha256").update(input.dryRun).digest("hex"),
    };
    this.gates.set(gate.key, gate);
    this.store.append({ kind: "approval_request", payload: gate });
    this.armTimer(gate);
    return gate;
  }

  private armTimer(g: Gate): void {
    const ms = g.expiresAt - Date.now();
    setTimeout(() => this.settle(g.key, "expired", "timer"), Math.max(0, ms));
  }

  /** Một verdict thắng. Tự duyệt trên prod-auth bị từ chối và được audit. */
  settle(key: string, v: Verdict, by: string, reason?: string): boolean {
    const g = this.gates.get(key);
    if (!g || g.state.status === "settled") return false;
    if (v === "approved" && g.tier === "prod-auth" && by === g.actorId) {
      this.store.append({ kind: "approval_policy", payload: { key, detail: "self_approval_rejected" } });
      return false;
    }
    g.state = { status: "settled", verdict: v, by, at: Date.now() };
    this.store.append({ kind: "approval_verdict",
      payload: { key, verdict: v, by, reason, diffHash: g.diffHash, dryRunHash: g.dryRunHash } });
    return true;
  }

  verdict(key: string): Verdict | undefined {
    return this.gates.get(key)?.state.status === "settled"
      ? (this.gates.get(key)!.state as { verdict: Verdict }).verdict : undefined;
  }

  private reloadOpen(): void {
    for (const ev of this.store.query({ kind: "approval_request" })) {
      if (!this.verdict(ev.payload.key)) {                    // gate đang mở → nạp lại timer
        const g = ev.payload as Gate;
        this.gates.set(g.key, g);
        this.armTimer(g);
      }
    }
  }
}
```

</details>

### 8.3 Tích Hợp Vòng Lặp Engine

```typescript
export async function runStep(step: Step, ctx: Ctx): Promise<void> {
  const tier = resolveTier(step, ctx.risk);                  // §2.1 rule, không phải model
  await checkpoint(ctx, step);                               // (→ 07 §13) TRƯỚC khi throw

  if (tier === "read") { await step.run(ctx); return; }      // auto-approve, chỉ log

  const gate = ctx.gates.request({ taskId: step.id, runId: ctx.runId, tier,
    actorId: ctx.actorId, summary: step.summary, diff: step.renderDiff(),
    blastRadius: step.blastRadius(ctx), dryRun: await step.dryRun(ctx),
    rollback: step.rollback(ctx) });
  await ctx.notify(gate);                                    // §7.2

  throw new Paused(`PAUSED:${gate.key}`);                    // đóng băng, audit thấy nó

  // được driver resume sau khi có verdict:
  //   verdict=approved → hàm này trả về, step.run() thực thi đúng một lần
  //   verdict=denied/expired → markBlocked → replanner.excludeBranch(step.id)
}
```

Chú ý vòng lặp engine **không có** gì: không nhánh nào model "hỏi cho tử tế" rồi đi
tiếp. Đường duy nhất qua được throw là verdict đã persist từ Gatekeeper — đó là toàn bộ
chuyện toàn vẹn.

### 8.4 Two-Person Gatekeeper

```typescript
// wrap Gatekeeper cho prod-auth: hai human approve độc lập, persist
export class TwoPersonGatekeeper {
  constructor(private inner: Gatekeeper) {}
  request(g: Omit<Gate, "key" | "state" | "createdAt" | "diffHash"
        | "dryRunHash">): Gate {
    const gate = this.inner.request(g);
    return gate;   // approval yêu cầu MỘT actor khác: settle() enforce ≠ actor
  }
  // settle() trong Gatekeeper cơ sở đã từ chối actorId === approver cho prod-auth.
  // Tất cả thay đổi nằm ở UI + TTL (4h) + page. Invariant ở một chỗ duy nhất.
}
```

---

## 9. Kiểm Thử Approval Gates

### 9.1 Test Bất Biến

```typescript
export function assertGateInvariants(...gates: Gate[]): void {
  for (const g of gates) {
    // 1 — settled đúng một lần
    if (g.state.status === "settled" && g.state.at < g.createdAt) throw new Error("verdict before creation");
    // 2 — bằng chứng bắt buộc
    if (g.state.status === "settled" && g.state.verdict === "approved" && !g.dryRunHash) throw new Error("approved without dry-run hash");
    // 3 — fail closed
    if (g.expiresAt < Date.now() && g.state.status === "waiting") throw new Error("expired gate still waiting (timer lost)");
    // 4 — two-person rule
    if (g.tier === "prod-auth" && g.state.status === "settled" && g.state.verdict === "approved"
        && g.state.by === g.actorId) throw new Error("self-approval on prod-auth");
    // 5 — mất thứ tự: verdict không được có trước bằng chứng đang được review
    if (typeof g.diffHash === "string" && g.diffHash === "" ) throw new Error("empty diff hash");
  }
}
```

Chạy nhóm này trên **mọi gate đã ghi trong production** (giống §9.1 của → 13): suite bất
biến rẻ và bắt regression mà unit test không bao giờ bắt — ví dụ timer không sống sót qua
restart.

### 9.2 Contract Test

```typescript
describe("Gatekeeper contract", () => {
  it("validate bằng chứng trước khi mở", () => {
    expect(() => gates.request({ ...noDryRun })).toThrow(/missing evidence/);
  });

  it("settle đúng một lần", async () => {
    const g = gates.request(validGate);
    gates.settle(g.key, "approved", "alice");
    gates.settle(g.key, "denied", "alice");                  // lời gọi thứ hai là no-op
    expect(gates.verdict(g.key)).toBe("approved");
  });

  it("sống sót qua restart và nạp lại expiry", async () => {
    const g = gates.request(validGate);
    const fresh = new Gatekeeper(store, risk);               // nạp lại gate đang mở
    expect(fresh.verdict(g.key)).toBeUndefined();
    await vi.advanceTimersByTimeAsync(g.expiresAt - Date.now() + 1);
    expect(fresh.verdict(g.key)).toBe("expired");            // fail closed
  });

  it("từ chối tự duyệt trên prod-auth", () => {
    const g = gates.request(validGateProdAuth);
    expect(gates.settle(g.key, "approved", g.actorId)).toBe(false);
  });

  it("phục hồi run sau approve và replan sau deny", async () => {
    const approved = gates.request(gate1); gates.settle(approved.key, "approved", "bob");
    const denied   = gates.request(gate2); gates.settle(denied.key, "denied", "bob", "not today");
    expect(resume(runId, approved.key)).toExecExactlyOnce(stepAtKey(approved.key));
    expect(plan.exclude).toHaveBeenCalledWith(denied.taskId);   // deny → replan, không retry
  });
});
```

Test restart là test đội thường bỏ, và nó chứng minh gate là *control bảo mật bền* chứ
không phải một object memory.

### 9.3 Bộ Hồi Quy

```sql
-- approval rate + wait trung vị theo tier (bộ phát hiện rubber-stamp, §7.1)
SELECT tier,
       COUNT(*) FILTER (WHERE verdict='approved')::float / COUNT(*) AS approval_rate,
       percentile_disc(0.5) WITHIN GROUP (ORDER BY (verdict_time - request_time)) AS median_wait
FROM approval_verdict v JOIN approval_request r ON r.key = v.key
GROUP BY tier ORDER BY tier;

-- approval mất thứ tự (verdict ghi sau khi action đã chạm thứ gì đó)
SELECT * FROM approval_verdict v
JOIN trajectory a ON a.payload->>'key' = v.key AND a.kind = 'action_started'
WHERE v.recorded_at < a.recorded_at;
```

Thêm cả hai vào catalog query ban đêm (→ 13 §6). Approval-rate drift là metric hạng
nhất: slope tăng là tín hiệu fatigue đã xuất hiện và bằng chứng đang bị stamp máy móc —
*trước* incident mà sự stamp máy móc cuối cùng gây ra.

---

## 10. Case Study Thực Tế

### 10.1 Claude Code — Permission Mode & Xác Nhận

Các permission mode của Claude Code (acceptEdits / bypassPermissions / plan mode /
sandbox) ánh xạ gần như một-một lên tier taxonomy: edit file và shell command được
permission bởi một consent stream, và `/permissions` là đường "escalate lên read bằng
tay, kèm lý do." Ba bài học:

1. **Phân quyền theo lớp hành động, không theo mức trust.** User tin một *command* (một
   tool call đã bóc suy luận của model ra), không phải "agent" như một persona. Đây là lý
   do tiering edit (`write`) tách khỏi deploy (`elevated`) đọc đúng.
2. **Model học ranh giới consent.** Agent quan sát gate sẽ tự điều chỉnh plan — chúng
   ngừng *đề xuất* force-push khi harness tin cậy cho chúng thấy ranh giới đỏ. Hiệu ứng
   răn đe là thật (phần "Triết lý cốt lõi").
3. **Manual opt-out tồn tại và được audit.** "Always allow" /
   `--dangerously-skip-permissions` là lối thoát hiểm được tài liệu hóa và bảo vệ bằng
   flag; *mặc định* vẫn gated. Harness không có lối thoát đó fail trong khủng hoảng,
   nhưng lối thoát không bao giờ được là mặc định.

### 10.2 Aider — Read/Write Mode Như Deny-By-Default

Chữ ký của Aider là việc prompt mode read/write tường minh: user chạy nó *không* cùng
`--no-verify-edits` và chọn hẳn full-write (`--yes-always`) khi họ quyết. Đó là hai quyết
định thiết kế mà mọi gate loop nên copy:

1. **Mặc định là gated, và việc gated nhìn thấy được.** Nhìn thấy model sẽ edit file
   chính là consent cho một *lớp* hành động, không phải cơn bão click từng lời gọi.
2. **Nó đi cặp với --auto-test và git history.** Mỗi edit là một event diffable,
   reversible, git-tracked — nên tier *giữa* có thể auto-approve trong khi tier
   *không đảo ngược* vẫn gate. Bài học: tier write nên tốn gần như không gì, vì lưới an
   toàn thật là reversibility (git + test), và gate thật được giữ cho những thứ git/test
   không undo được.

### 10.3 OpenHands — Confirmation Mode

OpenHands (trước là OpenDevin) phơi một chiến lược confirmation tỉ mỉ cho MCP và code
actions — "xác nhận mọi action" vs "xác nhận thay đổi lớn" vs "không bao giờ" — ánh xạ
sang gate `write` và `elevated`. Punchline nghiên cứu nó minh họa: confirmation theo
*từng action* ("xác nhận mọi thay đổi") là ergonomics tệ nhất vì nó luyện rubber-stamp;
harness nên mô hình confirmation ở độ hạt của plan-segment với batching (→ 7.1), không
phải theo từng tool call.

### 10.4 Devin — Giám Sát Không Đồng Bộ

Agent không đồng bộ (run dài, không giám sát) ép *gate phải di chuyển.* Devin đưa panel
"tôi đang làm gì / yêu cầu tôi approve" mà human poll thay vì bị ngắt giữa chừng — gate
là *checkpoint bạn nhặt được*, không phải ping mà bạn phải thức dậy. Failure mode của nó
quen thuộc: run càng dài, human càng ít đọc trước khi approve. Câu trả lời thiết kế nằm
trong module này là timeout-deny (→ 4.2) cộng fatigue metric (→ 9.3): giám sát không đồng
bộ chỉ an toàn khi một gate chưa được trả lời *fail closed và page*, thay vì lặng lẽ chờ
vô hạn.

### 10.5 Nghiên Cứu Delegation Người-Máy — Automation Bias

Nghiên cứu tâm lý về automation bias (automation complacency, ví dụ Parasuraman & Manzey,
2010) là nền tảng thực nghiệm cho mọi quy tắc ở đây: human over-trust gợi ý của hệ tự
động, under-monitor, và — quan trọng — *false alarm bào mòn sự tỉnh táo*. Kết luận ở mức
harness:

- Nếu gate nổ với thứ vô hại, human ngừng kiểm tra thứ thật (đường cong cry-wolf, §14).
- Bằng chứng thắng kể chuyện: human có dry-run hash và diff phân biệt đáng tin hơn đo được
  so với human có tóm tắt kiểu "tin tôi, tôi đã kiểm tra."
- Two-person rule tồn tại vì *một* human trong trạng thái 3 giờ sáng sau incident đúng
  là setup của automation bias: mệt, tin, và approve.

---

## 11. TypeScript Interfaces Cho Approval

```typescript
// ── The Gate ───────────────────────────────────────────────────────────────
export type Tier = "read" | "write" | "elevated" | "prod-auth";
export type Verdict = "approved" | "denied" | "expired";
export type GateState =
  | { status: "waiting" }
  | { status: "settled"; verdict: Verdict; by: string; at: number };

export interface Gate {
  key: string;
  taskId: string;            // node plan graph (→ 04)
  runId: string;             // resume idempotency (→ 07 §13)
  tier: Tier;
  actorId: string;           // proposer — neo của two-person rule
  summary: string;
  diff: string;
  blastRadius: string[];
  dryRun: string;
  rollback: string;
  diffHash: string;
  dryRunHash: string;
  createdAt: number;
  expiresAt: number;
  state: GateState;
}

// ── Risk Registry ──────────────────────────────────────────────────────────
export interface RiskTableEntry {
  action: string;
  defaultTier: Tier;
  paths?: RegExp[];
  noDryRunAllowlist?: boolean;
}
export interface RoleRiskMatrix {
  role: string;               // → 12 §6 policy per-role
  entries: RiskTableEntry[];
  override?: { action: string; tier: Tier; reason: string; approvedBy: string; at: number };
}

// ── Gatekeeper ─────────────────────────────────────────────────────────────
export interface Gatekeeper {
  request(input: GateRequestInput): Gate;
  settle(key: string, v: Verdict, by: string, reason?: string): boolean;
  verdict(key: string): Verdict | undefined;
  armed(key: string): boolean;
}
export interface GateEngineContract {
  before(action: Step): Tier;              // enforcement của tag-plan (§2.2)
  request(input: GateRequestInput): Gate;  // throw PAUSED:<key> sau checkpoint
  onVerdict(key: string, v: Verdict): void; // approved→resume; denied/expired→replan
}

// ── Audit ──────────────────────────────────────────────────────────────────
export interface ApprovalAuditEvent {
  kind: "approval_request" | "approval_verdict" | "approval_policy" | "notification_sent";
  payload: { key: string; tier: Tier; actorId: string; approver?: string;
             verdict?: Verdict; reason?: string; diffHash?: string; dryRunHash?: string;
             by?: string; at: number };
  sessionId: string; taskId: string;     // join keys (→ 13 §4)
  tokens: { in: number; out: number };
}

// ── Test surface ───────────────────────────────────────────────────────────
export interface GateInvariant { name: string; assert(g: Gate): void }
export interface FatigueMetric { tier: Tier; approvalRate: number; medianWaitMs: number }
```

---

## 12. Nguyên Tắc Thiết Kế Cho Approval

### 12.1 SOLID Cho Hệ Approval

| Nguyên tắc | Áp dụng |
|-----------|---------|
| **S**ingle responsibility | `RiskTable` tag tier; `Gatekeeper` persist + settle; `Notifier` kênh; audit là *trajectory event*, không phải việc của gate |
| **O**pen/closed | Lớp hành động mới = `RiskTableEntry` mới, không đổi Gatekeeper |
| **L**iskov substitution | `TwoPersonGatekeeper` và `Gatekeeper` hoán đổi được cho engine qua interface `Gatekeeper` |
| **I**nterface segregation | Debug UI cần `verdict()`; compliance cần `auditEvent`; engine cần `request()/onVerdict()`. Đừng nối chúng. |
| **D**ependency inversion | Gatekeeper phụ thuộc `TrajectoryStore` + risk table, không phụ thuộc model hay engine loop |

### 12.2 Sáu Nguyên Tắc Thiết Kế

1. **Tag lúc plan, enforce lúc chạy.** Tier là quyết định registry lúc plan (→ 04 §14.3);
   engine là bộ enforce đần thôi. Cái nhìn của model về tier của chính nó chỉ là tư vấn.
2. **Bằng chứng thắng kể chuyện.** Diff, blast radius, dry-run, rollback — từng cái
   hashable, từng cái bắt buộc. Approve không bằng chứng là vi phạm policy do cấu trúc.
3. **Fail closed & kêu to.** Timeout = deny. Gate hết hạn không page = bug. Giá của an
   toàn là bị đánh thức; đó là cả thỏa thuận.
4. **Deny dạy; approve chứng minh.** Lý do deny nuôi planner; approval tạo trail có
   kiểm chứng. Không một ai hoạt động được thiếu record của người kia.
5. **Attention của human là ngân sách.** Thiết kế gate như tài nguyên khan: batch, tier,
   hướng dẫn mặc định, và đo approval rate/wait để một gate hóa kịch bị bắt bởi metric
   (→ 9.3) trước khi nó tốn một incident.
6. **Gate phải sống sót qua restart.** Persist, nạp lại được, timer nạp lại được. Gate
   in-memory là một control bảo mật bị mất trí nhớ.

---

## 13. Best Practices

### 13.1 NÊN ✅

- Tag tier lúc plan từ một risk registry; engine enforce, không bao giờ để model.
- Payload bắt buộc diff + blast radius + dry-run + rollback; gate từ chối mở khi thiếu.
- Fail closed: timeout → deny, với trạng thái `blocked(approval-timeout)` riêng.
- Deny → replan loại nhánh; lý do được ghi nuôi planner (→ 04 §14.2).
- Giữ two-person rule cho `prod-auth`, enforce *trong* `settle`, không phải trong UI.
- Persist gate, nạp lại qua restart, nạp lại timer hết hạn.
- Ghi mọi request/verdict thành trajectory event kèm `diffHash`/`dryRunHash` (→ 13).
- Gộp review tier `write` để giữ attention của human cho các quyết định cần nó (§7.1).
- Đo approval rate + wait trung vị mỗi tier và coi drift là tín hiệu incident.
- Test đường restart: mở gate, giết process, restart, verdict vẫn được enforce.

### 13.2 KHÔNG NÊN ❌

- ❌ Không để model tự quyết có "cần approval" không — đó là gờ giảm tốc tự chọn.
- ❌ Không approve không diff (nút "tin tôi đi"). Bằng chứng là toàn bộ ý nghĩa.
- ❌ Không timeout-approve — timeout luôn fail-closed.
- ❌ Không retry cùng payload sau deny. Replan, đừng làm phiền.
- ❌ Không cho phép tự duyệt trên `prod-auth`, lặng lẽ hay có audit — cả hai đều vi phạm two-person.
- ❌ Không giữ gate chỉ trong memory; process restart quên mất gate đang mở là một lỗ hổng.
- ❌ Không xác nhận từng action `write`; đường cong fatigue sẽ biến an toàn của bạn thành kịch.
- ❌ Không để lời "ok" qua Slack/voice tính là verdict khi không có record.
- ❌ Không cắt bớt thông báo — kênh bị cắt bớt lặng lẽ hạ chất lượng quyết định.

---

## 14. Anti-Patterns & Cách Khắc Phục

| Anti-pattern | Triệu chứng | Cách sửa |
|--------------|---------|---------|
| **Rubber-stamping** | approval rate 98% + wait trung vị <10s | nâng thanh tier; gộp write; yêu cầu typed confirm (→ 9.3) |
| **Fail-open timeout** | "well, cuối cùng thì nó cũng approve" | không bao giờ expire-to-approve; expired = deny + page |
| **Deny → retry loop** | cùng payload bị hỏi lại, human nổi khùng | deny → replan, không bao giờ gửi lại hành động giống hệt |
| **Tự duyệt** | proposer tự approve prod-auth của mình | enforce `by !== actorId` *trong* `settle`, audit mọi cố duyệt |
| **Gate in-memory** | process restart dựng map rỗng mới tinh | reload từ trajectory, nạp lại timer (§8.2) |
| **Không bằng chứng** | gate mở với tóm tắt mà không có dry-run hash | `validatePayload` throw; action blocked tại gate (→ 3.2) |
| **Xác nhận từng action** | một click mỗi action `write`, human ngừng chú ý | gộp + tier, xác nhận ở độ hạt plan-segment (→ 7.1) |
| **Tier do model tự đặt** | agent "biết" nó rủi ro và hỏi tử tế | tier từ risk registry, engine-enforced (→ 2.2) |
| **Gate không checkpoint** | resume chạy lại ranh giới đã băng qua | checkpoint *trước* gate, resume từ cache (→ 5.2, 07 §13) |
| **Approval kiểu Slack vibes** | "ok" bằng giọng nói/kênh, không record | notification ≠ verdict; verdict chỉ qua `settle()` (→ 7.2) |
| **Gate hết hạn không page** | deadlock lặng lẽ, run "trông như kẹt" | vượt TTL thì escalate; run đóng băng giữ checkpoint |
| **Fatigue không đo** | slope approval rate tăng, không metric | fatigue metric trong catalog ban đêm (→ 9.3) |

---

## 15. Production Checklist

- [ ] **Tier tag lúc plan** từ risk registry; model không tự chọn tier (→ 2.2)
- [ ] **Blast radius liệt kê** theo registry cho mọi action được gated (→ 2.3)
- [ ] **Payload đầy đủ:** diff + blast + dry-run + rollback, từng cái hashable (→ 3.2)
- [ ] **Fail closed:** hết hạn → deny với trạng thái blocked riêng; không đường fail-open (→ 4.2)
- [ ] **Deny → replan** loại nhánh; không retry cùng payload (→ 4.3)
- [ ] **Chuỗi escalation** định nghĩa cho từng tier; delegation được audit (→ 4.4)
- [ ] **Pause/resume đã test** gồm restart process: gate đang mở nạp lại + nạp lại timer (→ 5.2, 8.2)
- [ ] **Resume idempotent**: cùng `runId`, idempotency cache bỏ qua step đã xong, action gated chạy đúng một lần (→ 5.3)
- [ ] **Two-person rule** enforce *trong* `settle` cho `prod-auth`; tự duyệt bị từ chối + audit (→ 5.4)
- [ ] **Audit bất biến**: event request/verdict nối hash → trajectory + SIEM (→ 6.1)
- [ ] **Vi phạm policy auto-flag** (approve-thiếu-dry-run, mất thứ tự, tự duyệt) (→ 6.2)
- [ ] **UX batching** — tier write được gộp; ngân sách attention của human được đo (→ 7.1)
- [ ] **Kênh thông báo** mang đầy đủ bằng chứng, giao hàng được trace (→ 7.2)
- [ ] **Test suite** — bất biến trên mọi gate đã ghi + contract test restart + fatigue metric (→ 9)
- [ ] **Nhịp review** — review approval-rate/wait hàng quý; drift = báo động (→ 9.3)

---

## 16. Xu Hướng Tương Lai

### 16.1 Registry Gate Policy-as-Code (2026-2028)

Risk table di cư thành artifact policy-as-code được version hóa, reviewable
(`approval-policy.yml`), được diff trong PR như mọi infra khác. Tier trở thành khai báo
có kiểm chứng ("mọi action `prod-auth` trong repo X nay phải page hai người"), và một
policy diff lặng lẽ hạ tier sẽ bị chặn bởi chính two-person rule đang bảo vệ các action.
Hệ gate trở thành cả *enforcer* lẫn *spec công khai* — hợp đồng "ai duyệt được cái gì",
version hóa cạnh code nó bảo vệ.

### 16.2 Adaptive Trust với Bằng Chứng Liên Tục

Thay vì tier `elevated` cố định, trọng lượng của gate học từ trajectory: lớp hành động
có 6 tháng dry-run hoàn hảo và không incident sẽ có đường nhanh hơn, lặng hơn; lớp vừa có
incident sẽ *tự động* bị gate chặt hơn. Điều quan trọng: hạ trust phải tự động và theo
metric (rẻ, an toàn), trong khi *khôi phục* trust giữ là quyết định của con người (đắt,
chậm). Đây chính là bánh cóc một chiều của trust giúp hệ bảo mật ổn định.

### 16.3 Approval Như Một Định Lý Checkpoint

Gate sụp đổ về câu chuyện checkpoint/resume (→ 07 §13): *gate = checkpoint có gắn
verdict.* Khi đó mọi thứ hệ thống checkpoint đang cho — replay, idempotency, audit, fork
— áp vào gate miễn phí. Một "deploy gate" chỉ là node `checkpoint(pause_until=verdict)`
trong plan graph, được render thành panel timeline và replay cho review sau incident.

### 16.4 Giám Sát Ở Quy Mô Con Người với Quy Mô Agent

Khi một human giám sát nhiều agent, gate phải multiplex: một bề mặt review duy nhất hiện
*tất cả* gate đang chờ, gộp theo rủi ro, batchable theo quyết định, với flow "approve
cùng lớp trừ prod-auth" — mà không bao giờ cho phép một click mệt mỏi duyệt một action
`prod-auth`. Chi phí của tương lai này là kinh tế học cảnh giác: hệ thống phải ngừng hỏi
khi human đã trống mắt, đó chính là lý do metric rubber-stamp (→ 9.3) trở thành dashboard
sản phẩm của năm năm tới.

---

## Tài Liệu Tham Khảo

### Papers & Research

- **Automation Bias and Automation Complacency** — Parasuraman & Manzey (2010) · https://link.springer.com/article/10.1007/s12170-010-0080-4
- **Trust in Automation: Designing for Appropriate Reliance** — Lee & See (2004) · https://journals.sagepub.com/doi/10.1518/hfes.46.1.50.30392
- **Human-AI Delegation** — Mapping delegation ontologies for AI agents · https://arxiv.org/abs/2309.01564
- **Comprehensible AI systems: Automation tragedy** — về việc bằng chứng thắng kể chuyện · https://arxiv.org/abs/2003.02334
- **Behavioral Data Science for Agent Oversight** *(khung thiết kế cho fatigue metric)* · https://arxiv.org/abs/2405.07355

### Frameworks & Tools

1. **Claude Code** — https://docs.anthropic.com/en/docs/claude-code — permission mode, `/permissions`, consent stream
2. **Aider** — https://aider.chat/docs/ — read/write mode, `--yes-always`, reversibility qua git
3. **OpenHands** — https://github.com/All-Hands-AI/OpenHands — confirmation strategy cho code + MCP
4. **NATS / approval bot qua webhook** — https://nats.io — transport thông báo + verdict
5. **OpenPolicyAgent (OPA)** — https://www.openpolicyagent.org — policy-as-code cho tier registry (→ 16.1)
6. **PolicyEngine** *(cổng policy phía server)* — https://github.com/policyengine

### Production Systems

- **Spacelift** — https://spacelift.io — plan/workflow approval với run-review (kiểu "approval như review," không phải "approval như click")
- **Atlantis** — https://www.runatlantis.io/apply-requirements — `apply_requirements` = hệ tier cho terraform
- **Claude Code** — https://claude.com/product/claude-code — consent stream permission
- **Devin** — https://devin.ai — panel giám sát không đồng bộ
- **CircleCI / GitHub Environments** — https://docs.github.com/en/actions/managing-workflow-runs/reviewing-deployments — approval cho protected environment

### Module Liên Quan

- `04-plan-decompose-task/README.md` §14.3 — gate phía planning ("ai được override"), deny→replan
- `06-decide-tools-mcp/README.md` §17.4 — UX consent phía tool
- `07-workflow/README.md` §13.4 — engine pause/resume + checkpoint (chủ nhà của gate)
- `12-sandbox-execution/README.md` — trần kỹ thuật mà gate bổ trợ
- `13-trajectory-observability/` — gate như event, audit + replay (§6 module này tiêu thụ nó)
- `14-compaction-context/README.md` — approval đang chờ là một phần của pin set (→ 14 §3.2)
- `08-execute-task/README.md` §11 — idempotency cache làm cho resume an toàn

---

*Tài liệu: XV. Approval Gates — HARNESS ENGINEERING EDITION*
*Module cross-cutting · control plane cho hành động không đảo ngược · human-in-the-loop*
*Cập nhật: 19/07/2026*
*Tác giả: AI Knowledge Repository*