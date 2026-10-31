# 🔐 Harness 15. Approval Gates — Human-in-the-Loop Cho Hành Động Không Đảo Ngược Được

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

> Phần này kể một tình huống có thật. Nó cho thấy approval gate cứu chuyện gì: một hành
> động xóa dữ liệu không thể hoàn tác, diễn ra lúc 3 giờ sáng, không ai can.

3 giờ 47 phút sáng. Một run migration đã chạy sáu tiếng. Agent đang ở lượt thứ 214, tự
tin tách một retry `db.migrate` đang treo — `db.migrate` là lệnh thay đổi cấu trúc
database — vì cho rằng nó "kẹt ở mấy bước tăng dần". Rồi agent tự vẽ ra một lộ trình cứu
hộ: `ALTER TABLE users DROP COLUMN mfa_secret`. Đây là lệnh SQL xóa cột `mfa_secret`
khỏi bảng `users`; dữ liệu trong cột mất luôn, không lấy lại được. Lý do: một check bên
dưới báo column đang `NOT NULL` mà không có default, thế là logic "gỡ blocker" trong đầu
agent thắng thế.

Column đó chứa 2,1 triệu lượt đăng ký MFA. Không có backup. Hành động này không đảo
ngược được, mang tính huỷ diệt, mà lại còn *sai lè*.

Thứ cứu cả đội khỏi một headline incident hôm đó chỉ là một quyết định harness chọn từ
sớm: **gắn tag `prod-auth` ngay lúc plan, cho run đóng băng, và đưa cho human xem bằng
chứng "trước"**, chứ không phải nghe mô hình kể lại. Gate nổ. Anh human trực lúc 3:47
sáng nhìn cái diff 12 dòng, nói "không", gõ thêm lý do, rồi hai mươi phút sau agent tự
replan đi đường vòng — *mà chưa từng chạm vào cái column đó*.

Gate không làm agent thông minh hơn. Nó giúp cả harness *an toàn ngay cả khi sai* — mà
với hệ tự trị, đây là tính chất đáng tiền nhất. Mọi pha hành động quá tự tin suýt gây
hoạ mà human chặn kịp đều vô hình trong metrics, chẳng tốn xu nào, và đó chính là toàn
bộ ý nghĩa của gate.

> **Tóm gọn 1 câu:** Gate ép agent dừng và trình bằng chứng trước khi làm điều không
> thể hoàn tác — nhờ vậy một sai lầm 3 giờ sáng chỉ tốn hai mươi phút replan, không
> phải mất dữ liệu.

### Vì Sao Approval Gates Là Bắt Buộc?

> Phần này trả lời: vì sao phải bắt người thật duyệt, thay vì tin agent? Câu trả lời nằm
> ở phép tính rủi ro bên dưới.

> *"Một agent tự tin xin được credential production lúc 3 giờ sáng và được nhận, không
> phải là agent. Đó là một khẩu pháo không cần nạp đạn."*

#### Phép tính của sự sai lầm tự tin

LLM agent sai với tỉ lệ không hề nhỏ và *không bao giờ biết mình sai* — các nghiên cứu
calibration (đo xem mức tự tin có khớp với mức đúng thật không) liên tục cho thấy
overconfidence tăng theo độ dài context và độ sâu plan (→ 10.5).

Cách đọc bảng này: mỗi dòng là một loại hành động agent có thể gọi. Cột giữa = xác suất quyết định sai; cột phải = mức thiệt hại nếu sai. Ví dụ: `edit_file` sai thì sửa lại qua git được; còn `db.migrate` trên prod sai thì cấu trúc database không quay lại được.

| Hành động | Tỉ lệ sai của *quyết định* | Nếu sai, blast radius |
|-----------|------------------------------|------------------------|
| `edit_file` trong `src/` | cao (API hallucinate, sai file) | đảo ngược cục bộ qua git |
| `db.migrate` trên prod | thấp nhưng *thảm khốc khi sai* | schema không thể undo, giờ rollback |
| `user.delete` / đổi IAM | hiếm | vĩnh viễn, danh tính + compliance |
| `git push --force` | tần suất thấp, độ mới cao | lịch sử chung bị viết lại, blast đa repo |

Chú thích nhanh: *schema* = cấu trúc bảng/cột của database; *rollback* = quay lại trạng thái trước; *IAM* = hệ phân quyền trên cloud; `git push --force` = ghi đè luôn lịch sử commit trên repo remote, mất bản backup.

Mấy kiểu hỏng làm chết công ty thường không phải loại hay gặp — mà là loại hiếm nhưng
một khi dính thì chi phí "gánh" hết cả phân phối. Gate chính là *lính gác cho cái đuôi
đắt đỏ đó*, mà lại gần như miễn phí ở cái đuôi rẻ hay gặp (tier `read` thì auto-approve).

Còn một lực thứ hai, tinh tế hơn: **một gate có human ngồi trong vòng lặp sẽ thay đổi
luôn cách agent hành xử, chứ không chỉ đổi kết quả.** Khi mô hình biết hành động không
đảo ngược được sẽ có bên thứ hai nhìn vào, audit được, nó sẽ thận trọng hơn thấy rõ —
bớt hẳn kiểu tự "ứng biến" ra lộ trình huỷ diệt vì biết plan sẽ bị *mang ra trình*, chứ
không phải cứ thế chạy. Gate vừa là hàng rào, vừa là lời răn đe từ trước.

#### Triết lý cốt lõi

Approval **không** phải "hỏi human mọi thứ" và **không** phải "không bao giờ hỏi." Nó
là: *tag rủi ro lúc plan, khoanh blast radius bằng bằng chứng bắt buộc, và để lỗi kêu
to và audit được thay vì lặng lẽ và đắt đỏ.* Gate nên là điểm hệ thống *được thiết kế
để fail* (hỏng một cách được kiểm soát) — để khi agent sai — và nó sẽ sai — thì sự sai
đó rẻ và hiển nhiên.

> **Tóm gọn 1 câu:** Agent sai thường và không biết mình sai, nên mọi hành động
> hiếm-nhưng-đắt (đổi DB, xóa user, force-push) phải qua người thật duyệt — gate gần
> như miễn phí ở việc thường ngày, cứu mạng ở việc hiếm gặp.

## Overview

> Phần này mô tả approval gate hoạt động thế nào từ đầu đến cuối: agent muốn làm gì →
> xếp tier rủi ro → gate mở → người duyệt → run chạy tiếp hay đi đường khác.

> **📌 Khái Niệm Cốt Lõi**
>
> - **Khái niệm:** Approval gate là điểm dừng trước hành động không đảo ngược được hoặc
>   blast radius lớn: execution đóng băng, human thấy *cái gì / vì sao / ảnh hưởng /
>   rollback*, run chỉ tiếp tục khi approve (hoặc replan khi deny/timeout).
> - **So sánh:** Như két ngân hàng cần hai chìa — agent giữ một (plan), human giữ một
>   (phán đoán). Một chìa không mở được gì.
> - **Vì sao quan trọng:** Agent sai với vẻ tự tin. Không gate, một `prod.db.drop()`
>   (lệnh xóa cả database production) hay `git push --force` (ghi đè lịch sử commit trên
>   repo remote) hallucinate lúc 3 giờ sáng thành incident. Gate là bảo hiểm incident
>   rẻ nhất cả harness.

**Approval Gates** là phòng điều khiển cho những hành động mà "giá của sai lầm" vượt
quá "độ tin cậy khi quyết" của agent. Nó đi cặp rất đẹp với sandbox: sandbox (→ 12)
khoanh vùng *agent được phép làm gì*, còn gate quyết định *cái gì thì một human đáng
tin phải nhìn qua trước khi cho chạy*. Một cái là trần kỹ thuật, một cái là hợp đồng
niềm tin.

Sơ đồ dưới đây là vòng đời của một gate, đọc từ trên xuống:

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

Giải thích nhanh: *diff preview* = xem trước thay đổi từng dòng; *tier* = mức rủi ro; *checkpoint* = điểm lưu trạng thái để chạy lại từ đó; *verdict* = kết quả duyệt (approve/deny); *page on-call* = gọi người trực ca chịu trách nhiệm sự cố.

**Gate có cả một vòng đời, chứ không phải cái nút bấm Có/Không:** một `request()`, ba
outcome đã chốt (`approved` / `denied` / `expired`), một audit trail, không có nhánh nào
đi chui. Implementation nào không trả lời được "ai, cái gì, khi nào, vì sao cho *mọi
hành động không đảo ngược*" thì đó chưa phải hệ approval — mới chỉ là cái nút bấm có
thêm bước.

> **Tóm gọn 1 câu:** Approval gate là vòng đời có quản: xếp tier rủi ro → dựng bằng
> chứng → đóng băng run → người thật duyệt → chạy tiếp, replan, hoặc hết giờ tính là
> bị từ chối.

## Mục Lục Chi Tiết

Cách đọc bảng này: cột "#" là số thứ tự mục, cột "Chủ đề" là tên mục, cột "Mô tả" là nội dung chính của mục đó. Ví dụ: mục 2 (Risk tier) trả lời câu hỏi "cái gì cần gate".

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

> **Tóm gọn 1 câu:** Tài liệu đi theo thứ tự: định nghĩa → xếp rủi ro → dựng payload →
> xử lý deny/timeout → gắn vào engine → ghi log → chăm UX → code → test → bài học thực
> tế → checklist.

---

## 1. Định Nghĩa & Thuật Ngữ

> Phần này định nghĩa các thuật ngữ cốt lõi, để các mục sau dùng lại cho gọn mà không
> hiểu nhầm.

### 1.1 Các Thuật Ngữ Cốt Lõi

Cách đọc bảng này: cột "Thuật ngữ" là tên gọi; cột "Định nghĩa" là nghĩa dễ hiểu kèm ví dụ; cột "Hỏng khi…" là lỗi phổ biến làm thuật ngữ đó mất tác dụng. Ví dụ: approval gate chỉ lưu trong bộ nhớ (RAM) thì process restart là mất, chẳng còn gate nào.

| Thuật ngữ | Định nghĩa | Hỏng khi… |
|-----------|-----------|-----------|
| **Approval gate** | Node workflow ở trạng thái `WAITING_APPROVAL`; persist, notify, resume khi có verdict | chỉ trong memory → mất khi restart |
| **Blast radius** | Tập tài nguyên bị ảnh hưởng nếu action chạy (file, DB, env, user) — liệt kê rõ ràng | mơ hồ ("đồ prod") → human không đánh giá được |
| **Dry-run** | Preview không side effect của action (plan diff, `terraform plan`, `--dry-run`) — bắt buộc trong gate payload | bỏ qua → approval là mù |
| **Timeout-deny** | Hết TTL không verdict → tính là **deny** (fail closed), không bao giờ là approve | fail-open → "tôi định approve mà" |
| **Two-person rule** | Người đề xuất ≠ người duyệt; một second human độc lập quyết định | tự duyệt → thành không có gate |
| **Deny → replan** | Deny ghi `reason` và trigger replanning loại nhánh bị deny (→ 04 §14.2) | deny → retry lại → lặp vô hạn |
| **Approval event** | Mọi request + verdict được ghi vào trajectory thành `approval_request` / `approval_verdict` (→ 13) | không trace → review sau incident bất khả thi |

Gloss nhanh: *persist* = lưu xuống đĩa, sống sót qua restart; *node workflow* = một bước trong quy trình; *side effect* = tác động ra thế giới thật (ghi file, đổi DB); *TTL* = thời gian sống (hết TTL = hết hạn chờ); *fail closed* = không chắc thì chặn; *fail open* = không chắc thì mở; *trajectory* = nhật ký từng bước của run; *trace* = dấu vết để lần lại từng bước.

> **Tóm gọn 1 câu:** Bảy thuật ngữ cốt lõi — gate là điểm dừng có lưu trạng thái, blast
> radius là vùng bị ảnh hưởng, dry-run là chạy thử không tác động thật, và mọi quyết
> định đều được ghi lại.

### 1.2 Hai Họ Kỹ Thuật: Hard Block vs Advisory Signal

> Phần này tách hai cơ chế hay bị trộn lẫn: một cái *chặn hẳn* (hard block), một cái
> *chỉ cảnh báo* (advisory signal). Trộn hai cái là lỗi phổ biến nhất khi làm gate.

Có hai *cơ chế khác nhau* trông thì giống nhau mà hay bị trộn lẫn, trộn là đau:

Cách đọc bảng này: so sánh hard block (chặn hẳn run) với advisory signal (chỉ cảnh báo) theo từng tiêu chí ở cột trái. Ví dụ: hard block bỏ qua thì run không đi tiếp; advisory signal bỏ qua thì run vẫn chạy kèm ghi chú.

| | **Hard block (gate)** | **Advisory signal** |
|---|---|---|
| **Làm gì** | Đóng băng run tới khi có verdict | Cảnh báo user, vẫn chạy tiếp |
| **State machine** | `request → WAITING_APPROVAL → settle` | banner / toast / dòng bôi màu |
| **Dùng cho** | Hành động không đảo ngược, tốn kém, blast lớn | Pattern nghi vấn-nhưng-đảo ngược được |
| **Nếu bỏ qua** | run không đi tiếp | run đi tiếp kèm ghi chú hiển thị |
| **Audit** | record request + verdict đầy đủ | tùy chọn, thường không có |
| **Chi phí** | attention của human, latency thật | gần trừ không |
| **Nguy hiểm** | over-gate → approval fatigue (→ 7.1) | under-gate → incident kiểu "chúng tôi đã cảnh báo" |

Chú thích: *state machine* = các trạng thái và luồng chuyển của gate; *banner/toast* =
thông báo nổi trên màn hình; *latency* = thời gian chờ thêm; *approval fatigue* = mệt
mỏi ra quyết định, duyệt theo phản xạ (→ 7.1).

Chỗ dễ sập bẫy nhất là xài lẫn hai món: biến advisory signal thành hard block (mỗi
`npm install` cũng bắt click một cái → human mỏi tay bấm cho qua → tới gate *thật* cũng
bấm theo quán tính), hoặc biến hard block thành advisory signal ("xác nhận cho vui chứ
run vẫn chạy"). Nhớ giúp một câu: mỗi action chọn một kiểu. Gate là gate, ra gate.

> **Tóm gọn 1 câu:** Hard block chặn run đến khi có người duyệt; advisory signal chỉ
> cảnh báo rồi vẫn chạy — mỗi hành động phải chọn đúng một kiểu, đừng trộn.

---

## 2. Risk Tier — Cái Gì Cần Gate?

> Phần này trả lời: hành động nào cần gate, nghiêm tới mức nào? Câu trả lời là xếp mọi
> hành động vào 4 mức rủi ro (tier) từ thấp đến cao.

### 2.1 Phân Nhóm Tier

Cách đọc bảng này: cột "Tier" là mức rủi ro (thấp → critical); cột "Ví dụ" là các hành động thuộc mức đó; cột "Gate" là cách hệ thống xử lý. Ví dụ: `read` thì chạy luôn và chỉ ghi log; `prod-auth` thì phải có hai người duyệt.

| Tier | Ví dụ | Gate |
|------|----------|------|
| `read` (thấp) | `read_file`, `grep`, `list`, `view` | Auto-approve, chỉ log |
| `write` (trung bình) | `edit_file` trong `src/`, `run_tests`, commit local | Diff preview + approve một click, hết hạn 5 phút |
| `elevated` (cao) | `db.migrate`, `deploy`, `user.delete`, `external.send`, `push --force`, `rm -rf` | Typed confirm + lý do + dry-run + lệnh rollback, hết hạn 30 phút |
| `prod-auth` (critical) | Đổi IAM, xoay secret, xóa dữ liệu prod, hành động payment/legal | Two-person rule (người đề xuất ≠ người duyệt) + báo kênh incident, 4h + page |

Chú thích: *typed confirm* = phải gõ tay tên hành động để xác nhận (không phải bấm
nút); *xoay secret* = đổi mật khẩu/key hệ thống; `rm -rf` = xóa sạch thư mục và mọi thứ
bên trong; *page* = gửi cảnh báo khẩn đến điện thoại người trực.

**Tier là tính chất của *lớp hành động*, chứ không phải của từng lời gọi riêng lẻ.**
Push lên feature branch là `write`; force-push lên `main` là `elevated`; force-push lên
nhánh `release/*` xài chung là `prod-auth`. Bảng map nằm trong permission/risk
(`permission.ts`), cập nhật lúc review — không bao giờ để model tự suy ra từng message.

> **Tóm gọn 1 câu:** Bốn tier rủi ro — `read` tự chạy, `write` duyệt nhẹ, `elevated`
> duyệt kỹ kèm dry-run, `prod-auth` cần hai người — và tier gắn với *lớp hành động*,
> không phải từng lời gọi.

### 2.2 Tag Tier Lúc Plan

> Phần này giải thích lúc nào tier được gán: ngay khi lập kế hoạch (plan), chứ không
> phải lúc thực thi. Gán sớm là để model không tự hạ mức rủi ro của chính mình.

Tier được gán **lúc plan** (→ 04 §14.3), không phải lúc thực thi:

1. Planner phát ra mỗi task/tool kèm một trường `tier` tường minh.
2. Engine kiểm tra tier với một risk table toàn cục trước khi step dựng payload.
3. Model không thể tự hạ tier — yêu cầu "chạy nó như `write` thôi" không phải đường
   policy hợp lệ; đổi tag là thay đổi policy, phải đến từ chủ sở hữu risk table.

> **Quy tắc:** *agent đề xuất, engine enforce, human override chỉ qua một lý do được
> ghi lại.* Tag-lúc-plan là thứ làm cho ba chiều tách rời đó khả thi — không có nó, mô
> hình tự chọn gờ giảm tốc của chính mình và chọn cái nó có thể phớt lờ.

Sơ đồ dưới đây cho thấy tier đi qua ba pha: lúc lập plan, lúc dựng payload, lúc thực thi:

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

> **Tóm gọn 1 câu:** Tier gán lúc lập kế hoạch từ một bảng rủi ro chung; agent chỉ đề
> xuất, engine kiểm tra, muốn đổi tier thì phải là người chủ bảng rủi ro và để lại lý
> do ghi log.

### 2.3 Liệt Kê Blast Radius

> Phần này nói về việc liệt kê *vùng ảnh hưởng* (blast radius) — thành phần quan trọng
> nhất của gate payload: người duyệt phải biết chính xác action này chạm vào những gì.

Gate payload xịn hay dở ăn nhau ở chỗ liệt kê blast radius có chính xác không. Hệ thống
phải tự liệt kê từ registry sandbox/policy (→ 12 §6) xem action này chạm đúng vào tài
nguyên nào, chứ đừng để model tự kể:

```
ACTION:   db.migrate 20260719_add_mfa_cols (tier: elevated)
BLAST:    prod-db.host=postgres-5a2f (primary, không replica cho schema này)
          database=users  size=2.1M rows
          table migration lock ~4s (cửa sổ downtime: ok)
          0 down migrations — KHÔNG đảo ngược được bởi engine migration
          microservices liên kết: auth-svc (read), consent-svc (write)
```

Giải thích nhanh: *lock ~4s* = bảng bị khóa khoảng 4 giây; *down migrations* = script quay ngược lại migration (0 nghĩa là không có, tức không thể undo bằng công cụ migration); *replica* = bản sao database chỉ đọc.

Cách đọc bảng này: mỗi dòng là một kiểu liệt kê blast radius sai. Cột "Ví dụ" là cách sai xuất hiện; cột "Cách sửa" là giải pháp. Ví dụ: chỉ nói "sửa prod database" là quá thô — cần db, host, size, thời gian khóa chính xác.

| Lỗi | Ví dụ | Cách sửa |
|---------|---------|-----|
| Quá thô | "sửa prod database" | db, host, size, lock estimate chính xác |
| Thiếu blast | quên service liên kết | liệt kê theo registry, không do model viết |
| Nhầm với cost | "tốn $0.40" nhưng không có lock time | cost là một *dòng* trong payload, không phải blast radius |
| Rollback không chứng minh | "rollback: revert migration" không test | trường `rollback` phải mang lệnh/hash đã test |

> **Tóm gọn 1 câu:** Blast radius phải do hệ thống tự liệt kê từ registry (chính xác
> tới db, host, số dòng, thời gian khóa), không phải do model kể — kể thiếu hoặc kể
> sai thì người duyệt đang mù.

---

## 3. Gate Payload — Human Thấy Gì

> Phần này mô tả "tờ giấy trình duyệt": những gì người thật nhìn thấy khi gate mở, và
> quy tắc bằng chứng bắt buộc trước khi tờ giấy ấy được phát.

### 3.1 Các Trường Của Payload

Đây là một payload mẫu — người duyệt nhìn đúng khối thông tin này:

```
ACTION:   db.migrate (tier: elevated)
TASK:     auth-refactor / step 3 (trajectory: traj_x, event: evt_41)
DIFF:     +ALTER TABLE users ADD COLUMN mfa_secret TEXT (12 lines…)
BLAST:    prod-db.users (2.1M rows), lock ~4s, 0 down migrations
DRY-RUN:  ✓ shadow-migrate passed (3.8s), rollback tested
ROLLBACK: db.migrate down v48 (lệnh đính kèm, đã test 2h trước)
COST:     ~$0.40, ~90s                       [Approve] [Deny + reason]
```

Mỗi trường trong payload phải **suy ra từ bằng chứng**, chứ đừng để model ngồi kể chuyện:

Cách đọc bảng này: cột "Trường" là mục thông tin trong payload; cột "Nguồn" là dữ liệu thật sinh ra nó; cột "Thiếu →" là hậu quả nếu thiếu. Ví dụ: thiếu `DIFF` thì người duyệt không biết mình duyệt thay đổi nào — approve là mù.

| Trường | Nguồn | Thiếu → |
|-------|--------|----------|
| `ACTION` + `tier` | tag tier của step (→ 2.2) | gate không dựng được |
| `TASK` + link trajectory | node plan graph + span id (→ 04, 13) | review sau incident không replay được |
| `DIFF` | lệnh/diff thực đã materialize | approve là mù |
| `BLAST` | liệt kê theo registry (→ 2.3) | human đánh giá thấp |
| `DRY-RUN` | *output* của dry-run, nối hash | approve là hành động đức tin |
| `ROLLBACK` | lệnh rollback đã test + thời điểm test | approve cam kết vào sự không thể undo |
| `COST` | token/tiền/thời gian ước tính | human không so được lựa chọn |

> **Tóm gọn 1 câu:** Payload là "tờ giấy trình duyệt" gồm 7 trường (làm gì, thuộc task
> nào, diff, vùng ảnh hưởng, dry-run, rollback, chi phí) — mỗi trường phải sinh ra từ
> dữ liệu thật, không phải lời kể của model.

### 3.2 Quy Tắc Bằng Chứng Bắt Buộc

> Phần này nói về invariant quan trọng nhất: thiếu bằng chứng thì gate không mở, hành
> động bị chặn. Đây là điều làm approval khác với hỏi cho có.

> **Không dry-run → không gate → action bị chặn.** Gate từ chối mở nếu bất kỳ trường
> bằng chứng bắt buộc nào rỗng. Đây *không* phải sự tử tế về UX — đây là invariant làm
> cho approval khác với sự đồng thuận (consent).

Về mặt implementation, đây là hàm validate chạy *trước* khi `request()` được gọi:

> 📄 **Code ví dụ:** [`examples/01-3-2-quy-tac-bang-chung-bat-buoc.ts`](examples/01-3-2-quy-tac-bang-chung-bat-buoc.ts)

Một `request()` với mảng `missing` không rỗng sẽ ném lỗi; run **không thể** đi tiếp tới
khi bằng chứng tồn tại. Các đội cho phép "approve anyway" trên payload sai consistently
phát hiện ra rằng nút approve thành *phương tiện đăng bài cho hành động chưa được xem
xét*.

Payload bản thân nó cũng là một trajectory event (→ 13), nên lúc review sau incident
bạn replay đúng cái human đã thấy hôm đó — kể cả output dry-run đã biện minh (hoặc
không biện minh nổi) cho verdict.

> **Tóm gọn 1 câu:** Thiếu bất kỳ trường bằng chứng nào thì gate không mở và action bị
> chặn — nút "approve anyway" là con đường nhanh nhất biến approval thành hình thức.

---

## 4. Ngữ Nghĩa Timeout, Deny & Escalation

> Phần này chốt các kết cục của gate: khi người duyệt trả lời, khi họ im lặng, và khi
> gate treo quá lâu thì gọi ai.

### 4.1 Bốn Outcome

Cách đọc bảng này: cột "Outcome" là kết cục của gate; cột "Ý nghĩa" giải thích khi nào xảy ra; cột "Trạng thái tiếp theo" là hệ thống làm gì sau đó. Ví dụ: hết giờ chờ mà không ai trả lời (`expired`) thì xử lý *giống như bị từ chối* — không bao giờ tính là được duyệt.

| Outcome | Ý nghĩa | Trạng thái tiếp theo |
|---------|---------|-----------|
| `approved` | human xác minh bằng chứng, run tiếp tục | chạy tiếp trên cùng `runId`, idempotency cache bỏ qua các step đã xong |
| `denied` | human từ chối kèm lý do | task mark `blocked(denied)`, replan loại nhánh |
| `expired` | không verdict trong TTL | xử lý *đúng như deny* (fail closed), trừ khi được escalate |
| `escalated` | TTL vượt ngưỡng và đã page on-call | TTL mới, chuỗi delegation được ghi |

State machine nhỏ và đóng; bất kỳ implementation nào "sinh ra" outcome mới lúc runtime
(ví dụ *"user nói ok trên Slack"*) là lỗ hổng policy, không phải tính năng.

> **Tóm gọn 1 câu:** Gate chỉ có đúng bốn kết cục — duyệt, từ chối, hết giờ (tính như
> từ chối), hoặc leo thang — mọi kết cục "ngoài danh sách" đều là lỗ hổng.

### 4.2 Timeout-Deny (Fail Closed)

> Phần này nói về quy tắc hết giờ: chờ mãi không được trả lời thì gate phải tự chặn,
> không được tự duyệt hộ.

Thời gian chờ theo tier: `write` 5 phút · `elevated` 30 phút · `prod-auth` 4h + page.

- Hết hạn mark task `blocked(approval-timeout)` — trạng thái riêng biệt với `denied`,
  vì *hành động kế tiếp* khác nhau (xem 4.3).
- **Fail closed, không bao giờ fail open.** Hết hạn không bao giờ được diễn giải thành
  approve. Ngoại lệ duy nhất cần có chữ ký policy tường minh: cửa sổ deploy unattended
  trong giờ đóng cửa, với timeout được tài liệu hóa là "hết hạn = rollback + page".
- Đồng hồ hết hạn chạy trong *engine*, không phải trong phiên UI. Đóng laptop review
  không thể kéo dài đời sống của gate.

> 📄 **Code ví dụ:** [`examples/02-4-2-timeout-deny-fail-closed.ts`](examples/02-4-2-timeout-deny-fail-closed.ts)

> **Tóm gọn 1 câu:** Hết giờ chờ thì gate tự tính là bị từ chối và đóng run lại —
> không bao giờ "hết giờ = duyệt luôn", vì im lặng không phải sự đồng ý.

### 4.3 Deny → Replan, Không Retry

> Phần này nói về phía sau một lời từ chối: agent phải đi đường khác (replan), chứ
> không hỏi lại y hệt.

- Ghi `reason` — đây là artifact audit *giá trị nhất* trong cả gate: nó cho planner sau
  biết human từ chối thứ gì, và deny lặp lại cùng lý do là tín hiệu sản phẩm (agent cứ
  đề xuất thứ đội không muốn).
- Trigger replanning loại nhánh bị deny (→ 04 §14.2). Không bao giờ hỏi lại cùng payload
  hai lần. Nếu *cùng* plan có thể thỏa mãn deny theo cách khác, planner phát plan mới;
  plan mới sinh gate mới chỉ khi action mới lại cao tier.
- Hỏi lại y hệt hành động sau deny là lý do **#1** khiến hệ approval trở nên đáng khinh,
  và lý do **#1** khiến user bypass bằng việc approve "chỉ để hết ồn."

> **Tóm gọn 1 câu:** Bị từ chối thì ghi lại lý do, vẽ lại kế hoạch bỏ nhánh đó — tuyệt
> đối không hỏi lại cùng một hành động, vì hỏi lại luyện cho người duyệt bấm cho qua.

### 4.4 Escalation & Ủy Quyền

> Phần này nói về việc gate treo quá lâu: gọi ai lên xử lý, và ai được ủy quyền duyệt
> hộ ai.

- **Page on-call** nếu `elevated` treo gate >15 phút trong giờ prod (hoặc >T cho
  non-prod, cấu hình được). Run đóng băng nguyên vẹn tại checkpoint (→ 07 §13);
  checkpoint chính là tính chất an toàn làm cho escalation miễn phí.
- **Ủy quyền approve** được phép (on-call → secondary) — nhưng *ủy quyền tách biệt với
  two-person rule*: delegating thông báo không biến một approver thành hai. Với
  `prod-auth`, delegation giữ nguyên yêu cầu hai người (proposer + một approver độc lập);
  nó có thể đổi *ai* là approver, không bao giờ đổi *bao nhiêu*.
- Mỗi chặng của chuỗi escalation (`paged_oncall` → `delegated_to:x` → `approved`) là một
  mục audit. Chuỗi đó là thứ làm "ai thực sự quyết định?" trả lời được khi bị soát.

> **Tóm gọn 1 câu:** Gate treo quá lâu thì gọi người trực; ủy quyền được nhưng chỉ đổi
> *ai* duyệt, không bao giờ giảm số người phải duyệt — và cả chuỗi đó đều được ghi log.

---

## 5. Tích Hợp Engine (Pause / Resume)

> Phần này nói về mặt kỹ thuật: engine "đóng băng" run thế nào khi gate mở, và chạy lại
> thế nào sau khi được duyệt — kể cả khi process đã chết giữa chừng.

### 5.1 API Gatekeeper

Đây là bề mặt API của Gatekeeper — đối tượng quản lý mọi gate: tạo gate, nhận verdict,
trả về trạng thái.

> 📄 **Code ví dụ:** [`examples/03-5-1-api-gatekeeper.ts`](examples/03-5-1-api-gatekeeper.ts)

> **Tóm gọn 1 câu:** Gatekeeper là API duy nhất điều phối gate: `request()` mở gate,
> `settle()` ghi kết quả duyệt — mọi thứ khác đi qua nó.

### 5.2 Giao Thức PAUSED

Engine **không** "chờ đợi." Nó throw một `PAUSED:<key>` có kiểu sau khi checkpoint —
nghĩa là engine dừng hẳn và ném ra một thông báo "run đang tạm dừng tại gate này", thay
vì đứng đó chờ:

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

Đọc sơ đồ: run tới lượt 214, thấy tier cao → lưu checkpoint → mở gate → ném `PAUSED`.
Sau đó hoặc process restart rồi nạp lại gate, hoặc human duyệt → `resume(runId)` chạy
lại từ cache các lượt đã xong.

> **Tóm gọn 1 câu:** Engine không chờ đợi — nó lưu checkpoint rồi ném `PAUSED:<key>` và
> dừng hẳn; người duyệt "giao kết quả" cho gate, run sống sót qua cả việc process chết.

### 5.3 Resume & Idempotency

> Phần này nói về việc chạy lại run sau khi duyệt: chạy đúng một lần, không lặp tác
> động, không hỏi lại.

- Resume gọi lại run với **cùng `runId`**; step đã xong hit idempotency cache và skip
  (→ 07 §13, 08 §11). Không gì thực thi lại, không gì hỏi lại.
- Bản thân action được gate lại chạy **chỉ sau** approval, đúng một lần — checkpoint nằm
  *trước* action, nên resume chạy lại action, không phải băng qua ranh giới.
- Idempotency của *approval*: settle cùng key hai lần là no-op (`if (!g || g.verdict)
  return`). Một cú "approve" click kép không thể chạy migration hai lần.

> **Tóm gọn 1 câu:** Resume chạy lại từ checkpoint với cùng `runId`; các bước đã xong
> được bỏ qua nhờ idempotency cache, nên click duyệt hai lần cũng không chạy migration
> hai lần.

### 5.4 Enforce Two-Person Rule

> Phần này nói về việc *bắt buộc* hai người khác nhau cho tier `prod-auth`: quy tắc nằm
> trong code gate, không phải trong giao diện.

Gate `prod-auth` yêu cầu một đôi mắt human thứ hai có danh tính khác người đề xuất:

> 📄 **Code ví dụ:** [`examples/04-5-4-enforce-two-person-rule.ts`](examples/04-5-4-enforce-two-person-rule.ts)

Người đề xuất được ghi lúc `request()` (chính step sinh ra gate). Quy tắc được enforce
*trong* `tryApprove`, nên không có đường mô hình vòng qua. Cố tự duyệt không im lặng —
nó được audit như một policy event, chính nó là tín hiệu hành vi kỳ lạ đáng theo dõi.

> **Tóm gọn 1 câu:** Với `prod-auth`, người duyệt phải khác người đề xuất — quy tắc được
> kiểm tra ngay trong hàm duyệt của gate, và mọi cố tự duyệt đều bị ghi lại làm bằng
> chứng hành vi đáng ngờ.

---

## 6. Audit Log

> Phần này nói về sổ ghi chép của gate: mỗi lần mở gate và mỗi lần duyệt đều được ghi
> thành bản ghi không sửa được, để sau này lần lại được.

### 6.1 Record

Mỗi gate ghi record bất biến (không sửa, không xóa): `{key, tier, actor(proposer),
approver, verdict, reason, diffHash, dryRunHash, at}` → trajectory store (→ 13) + SIEM.
*SIEM* = hệ tập trung log bảo mật của công ty để truy vết.

Cách đọc bảng này: cột "Trường" là tên dữ liệu trong bản ghi; cột "Ý nghĩa" giải thích nó là gì; cột "Cần cho" là việc nào dùng tới nó. Ví dụ: `diffHash` là "vân tay" của diff đã hiển thị, dùng để chứng minh người ta duyệt đúng thay đổi đó.

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

> **Tóm gọn 1 câu:** Mọi gate để lại một bản ghi không sửa được — ai đề xuất, ai duyệt,
> duyệt cái gì (qua hash) — nên "tôi duyệt một thứ khác với thứ được hiển thị" là không
> thể xảy ra lặng lẽ.

### 6.2 Phát Hiện Vi Phạm Policy

> Phần này nói về các kiểm tra tự động chạy trên dòng audit: biến sổ ghi thành cảm biến
> báo vi phạm quy tắc.

Các check tự động trên dòng audit:

- Gate approve **không** có `dryRunHash` → vi phạm policy, flag + page (trừ khi lớp hành
  động nằm trong allowlist "no-dry-run" tường minh, bản thân allowlist phải được duyệt).
- `approver === actor` trên gate `prod-auth` → vi phạm (tự duyệt).
- Verdict ghi **sau khi** action đã chạm tài nguyên → vi phạm (approval mất thứ tự).
- Timeout-deny mà tiếp theo là một *request giống hệt* trong vòng X phút → vi phạm
  deny→no-retry (→ 4.3).

Nhịp review hàng quý: approval rate theo tier, wait trung vị (thời gian chờ duyệt nằm
giữa danh sách xếp hạng — không bị số ngoại lệ kéo lệch), override incidents, độ sâu
chuỗi delegation.

> 🔑 **Highlight Policy / Permission:** đây là **cảm biến tuân thủ policy** — biến audit
> log (§6.1) thành verdict policy có thể enforce (thiếu dry-run evidence, tự duyệt,
> approval mất thứ tự, deny→retry). Kết hợp `12-sandbox-execution` (deny-by-default) và
> `06` §8 (RBAC) thành vòng policy đầy đủ: decide → enforce → audit → detect.

Mục đích review không phải kiểm soát — nó là *trí tuệ thiết kế*: một tier với approval
rate 98% và wait trung vị 30 giây không được đọc, nó bị stamp máy móc (duệt theo phản
xạ), và gate đã thành kịch (→ 14).

> **Tóm gọn 1 câu:** Audit log không chỉ để xem lại — các check tự động báo động khi
> thấy duyệt thiếu bằng chứng, tự duyệt, duyệt sai thứ tự, hoặc hỏi lại sau khi bị từ
> chối.

---

## 7. UX Cho Human-in-the-Loop

> Phần này nói về trải nghiệm của *người duyệt*: nếu hỏi quá nhiều và hỏi phiền, họ sẽ
> duyệt theo phản xạ và gate mất tác dụng.

### 7.1 Batching & Mệt Mỏi Ra Quyết Định

Human là tài nguyên hiếm và đắt, nên mục tiêu thiết kế gói gọn trong một câu: *tốn ít
"token attention" của con người nhất cho mỗi quyết định an toàn*.

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

> **Tóm gọn 1 câu:** Sức chú ý của người duyệt là tài nguyên khan hiếm — gộp các quyết
> định nhỏ, cho đủ ngữ cảnh, và đo dấu hiệu mệt mỏi (duệt nhanh hơn, nhiều hơn) để kịp
> nâng thanh gate.

### 7.2 Kênh Thông Báo

Cách đọc bảng này: cột "Tier" là mức rủi ro; cột "Kênh" là nơi thông báo được gửi; cột "Giọng" là mức khẩn cấp của thông báo. Ví dụ: `prod-auth` gửi vào kênh incident và gọi điện/page, vì đó là việc khẩn nhất.

| Tier | Kênh | Giọng |
|------|---------|------|
| `write` | in-app/PR comment; lặng lẽ, gộp | thông tin |
| `elevated` | push + email, có thể hành động | cần chú ý, ngân sách 30 phút |
| `prod-auth` | kênh incident + page; two-person | escalation, TTL 4h |

Mỗi thông báo mang *cùng* payload mà UI hiển thị (diff, blast, dry-run hash) — không
kênh nào cắt bớt bằng chứng, vì kênh bị cắt bớt lặng lẽ hạ chất lượng quyết định. Việc
giao thông báo được trace (`notification_sent` event → 13) để "human không bao giờ thấy
nó" là một claim kiểm chứng được, không phải lời bào chữa.

> **Tóm gọn 1 câu:** Càng rủi ro thì kênh thông báo càng khẩn, nhưng mọi kênh đều phải
> mang đủ bằng chứng và được ghi nhận đã gửi — không được lược bớt.

---

## 8. Implementation TypeScript

> Phần này là code chạy được: các kiểu dữ liệu, Gatekeeper có lưu trữ, cách gắn vào vòng
> lặp engine, và phiên bản hai người duyệt.

### 8.1 Types

Đây là các kiểu dữ liệu nền (gate, verdict, payload) mà mọi phần khác dùng chung.

> 📄 **Code ví dụ:** [`examples/05-8-1-types.ts`](examples/05-8-1-types.ts)

> **Tóm gọn 1 câu:** Mọi thứ bắt đầu từ các kiểu dữ liệu rõ ràng cho gate và verdict —
> đây là hợp đồng mà các phần sau cùng tuân theo.

### 8.2 Gatekeeper Có Persist

<details>
<summary>TypeScript Code — Gatekeeper có persist + reload + audit (bấm để mở/thu gọn)</summary>

> 📄 **Code ví dụ:** [`examples/06-8-2-gatekeeper-co-persist.ts`](examples/06-8-2-gatekeeper-co-persist.ts)

</details>

Code này cho thấy Gatekeeper lưu gate xuống đĩa (persist), nạp lại khi restart (reload),
và ghi audit.

> **Tóm gọn 1 câu:** Gatekeeper thật phải lưu gate xuống đĩa và nạp lại được khi
> restart — gate chỉ trong bộ nhớ là gate mất trí nhớ.

### 8.3 Tích Hợp Vòng Lặp Engine

> 📄 **Code ví dụ:** [`examples/07-8-3-tich-hop-vong-lap-engine.ts`](examples/07-8-3-tich-hop-vong-lap-engine.ts)

Chỗ này engine **không chừa** cửa nào khác: không tồn tại nhánh kiểu model "hỏi cho tử
tế" rồi đi tiếp. Con đường duy nhất qua được cú throw là verdict đã persist từ
Gatekeeper — toàn bộ chuyện toàn vẹn nằm ở chỗ đó.

> **Tóm gọn 1 câu:** Trong vòng lặp engine, chỉ tồn tại đúng một con đường qua gate là
> verdict đã lưu từ Gatekeeper — không có nhánh tắt nào khác.

### 8.4 Two-Person Gatekeeper

> 📄 **Code ví dụ:** [`examples/08-8-4-two-person-gatekeeper.ts`](examples/08-8-4-two-person-gatekeeper.ts)

> **Tóm gọn 1 câu:** Đây là phiên bản Gatekeeper cấm tự duyệt: người duyệt phải khác
> người đề xuất, kiểm tra ngay trong hàm duyệt.

---

## 9. Kiểm Thử Approval Gates

> Phần này nói về cách test gate: bất biến phải luôn đúng, hợp đồng giữa các phần, và
> bộ số liệu hồi quy phát hiện gate "hỏng thầm lặng".

### 9.1 Test Bất Biến

*Test bất biến* = kiểm tra các tính chất phải luôn đúng với mọi gate trong production.

> 📄 **Code ví dụ:** [`examples/09-9-1-test-bat-bien.ts`](examples/09-9-1-test-bat-bien.ts)

Chạy nhóm này trên **mọi gate đã ghi trong production** (giống §9.1 của → 13): suite
bất biến rẻ và bắt regression mà unit test không bao giờ bắt — ví dụ timer không sống
sót qua restart.

> **Tóm gọn 1 câu:** Chạy bộ test bất biến trên mọi gate thật để bắt những lỗi mà test
> đơn vị không thấy, như timer mất khi restart.

### 9.2 Contract Test

*Contract test* = kiểm tra cam kết giữa hai thành phần (gate ↔ engine): gọi A thì B phải
phản ứng thế nào.

> 📄 **Code ví dụ:** [`examples/10-9-2-contract-test.ts`](examples/10-9-2-contract-test.ts)

Test restart là test đội thường bỏ, và nó chứng minh gate là *control bảo mật bền* chứ
không phải một object memory (đối tượng chỉ sống trong RAM).

> **Tóm gọn 1 câu:** Contract test chứng minh gate là chốt an toàn bền vững — nhất là
> test restart, thứ cho thấy gate sống sót qua process chết.

### 9.3 Bộ Hồi Quy

*Bộ hồi quy* = tập truy vấn chạy định kỳ để phát hiện gate hỏng âm thầm.

> 📄 **Code ví dụ:** [`examples/11-9-3-bo-hoi-quy.sql`](examples/11-9-3-bo-hoi-quy.sql)

Thêm cả hai vào catalog query ban đêm (→ 13 §6). Approval-rate drift (tỉ lệ duyệt tăng
dần một cách bất thường) là metric hạng nhất: slope tăng là tín hiệu fatigue đã xuất
hiện và bằng chứng đang bị stamp máy móc — *trước* incident mà sự stamp máy móc cuối
cùng gây ra.

> **Tóm gọn 1 câu:** Chạy truy vấn hồi quy mỗi đêm để bắt dấu hiệu mệt mỏi (tỉ lệ duyệt
> tăng, chờ duyệt ngắn đi) trước khi nó biến thành incident.

---

## 10. Case Study Thực Tế

> Phần này học từ các công cụ có thật: Claude Code, Aider, OpenHands, Devin, và một
> nghiên cứu tâm lý. Mỗi case rút ra một bài học áp dụng trực tiếp được.

### 10.1 Claude Code — Permission Mode & Xác Nhận

Các permission mode của Claude Code (acceptEdits / bypassPermissions / plan mode /
sandbox) ánh xạ gần như một-một lên tier taxonomy: edit file và shell command được
permission bởi một consent stream (luồng xác nhận), và `/permissions` là đường "escalate
lên read bằng tay, kèm lý do." Ba bài học:

1. **Phân quyền theo lớp hành động, không theo mức trust.** User tin một *command* (một
   tool call đã bóc suy luận của model ra), không phải "agent" như một persona. Đây là
   lý do tiering edit (`write`) tách khỏi deploy (`elevated`) đọc đúng.
2. **Model học ranh giới consent.** Agent quan sát gate sẽ tự điều chỉnh plan — chúng
   ngừng *đề xuất* force-push khi harness tin cậy cho chúng thấy ranh giới đỏ. Hiệu ứng
   răn đe là thật (phần "Triết lý cốt lõi").
3. **Manual opt-out tồn tại và được audit.** "Always allow" /
   `--dangerously-skip-permissions` là lối thoát hiểm được tài liệu hóa và bảo vệ bằng
   flag; *mặc định* vẫn gated. Harness không có lối thoát đó fail trong khủng hoảng,
   nhưng lối thoát không bao giờ được là mặc định.

> **Tóm gọn 1 câu:** Bài học từ Claude Code: phân quyền theo từng lớp hành động, để
> model thấy được ranh giới để tự nề nếp, và lối thoát hiểm phải có tài liệu, không bao
> giờ là mặc định.

### 10.2 Aider — Read/Write Mode Như Deny-By-Default

Chữ ký của Aider là việc prompt mode read/write tường minh: user chạy nó *không* cùng
`--no-verify-edits` và chọn hẳn full-write (`--yes-always`) khi họ quyết. Đó là hai
quyết định thiết kế mà mọi gate loop nên copy:

1. **Mặc định là gated, và việc gated nhìn thấy được.** Nhìn thấy model sẽ edit file
   chính là consent cho một *lớp* hành động, không phải cơn bão click từng lời gọi.
2. **Nó đi cặp với --auto-test và git history.** Mỗi edit là một event diffable,
   reversible, git-tracked — nên tier *giữa* có thể auto-approve trong khi tier *không
   đảo ngược* vẫn gate. Bài học: tier write nên tốn gần như không gì, vì lưới an toàn
   thật là reversibility (git + test), và gate thật được giữ cho những thứ git/test
   không undo được.

> **Tóm gọn 1 câu:** Bài học từ Aider: mặc định là bị khóa và ai cũng nhìn thấy điều
> đó; việc bình thường (sửa file, chạy test) đã có git lưới an toàn nên duyệt nhẹ, giữ
> gate thật cho thứ git không hoàn tác được.

### 10.3 OpenHands — Confirmation Mode

OpenHands (trước là OpenDevin) phơi một chiến lược confirmation tỉ mỉ cho MCP và code
actions — "xác nhận mọi action" vs "xác nhận thay đổi lớn" vs "không bao giờ" — ánh xạ
sang gate `write` và `elevated`. Punchline nghiên cứu nó minh họa: confirmation theo
*từng action* ("xác nhận mọi thay đổi") là ergonomics tệ nhất vì nó luyện rubber-stamp
(duệt theo phản xạ); harness nên mô hình confirmation ở độ hạt của plan-segment (mỗi
đoạn plan một lần) với batching (→ 7.1), không phải theo từng tool call.

> **Tóm gọn 1 câu:** Bài học từ OpenHands: xác nhận từng hành động nhỏ là cách nhanh
> nhất luyện người dùng duệt vô thức — xác nhận theo *đoạn kế hoạch*, không phải từng
> tool call.

### 10.4 Devin — Giám Sát Không Đồng Bộ

Agent không đồng bộ (run dài, không giám sát) ép *gate phải di chuyển.* Devin đưa panel
"tôi đang làm gì / yêu cầu tôi approve" mà human poll (chủ động xem lại) thay vì bị ngắt
giữa chừng — gate là *checkpoint bạn nhặt được*, không phải ping mà bạn phải thức dậy.
Failure mode của nó quen thuộc: run càng dài, human càng ít đọc trước khi approve. Câu
trả lời thiết kế nằm trong module này là timeout-deny (→ 4.2) cộng fatigue metric
(→ 9.3): giám sát không đồng bộ chỉ an toàn khi một gate chưa được trả lời *fail closed
và page*, thay vì lặng lẽ chờ vô hạn.

> **Tóm gọn 1 câu:** Bài học từ Devin: với agent chạy dài không cần giám sát, gate phải
> là "bảng chờ bạn ghé xem" kèm cơ chế hết giờ — không được chờ lặng lẽ vô hạn.

### 10.5 Nghiên Cứu Delegation Người-Máy — Automation Bias

*Automation bias* = xu hướng người tin máy móc mù quáng: thấy máy đề xuất là gật. Nghiên
cứu tâm lý về automation bias (automation complacency, ví dụ Parasuraman & Manzey, 2010)
là nền tảng thực nghiệm cho mọi quy tắc ở đây: human over-trust gợi ý của hệ tự động,
under-monitor, và — quan trọng — *false alarm bào mòn sự tỉnh táo*. Kết luận ở mức
harness:

- Nếu gate nổ với thứ vô hại, human ngừng kiểm tra thứ thật (đường cong cry-wolf, §14).
- Bằng chứng thắng kể chuyện: human có dry-run hash và diff phân biệt đáng tin hơn đo
  được so với human có tóm tắt kiểu "tin tôi, tôi đã kiểm tra."
- Two-person rule tồn tại vì *một* human trong trạng thái 3 giờ sáng sau incident đúng
  là setup của automation bias: mệt, tin, và approve.

> **Tóm gọn 1 câu:** Nghiên cứu xác nhận ba điều: cảnh báo giả làm con người ngừng cảnh
> giác, bằng chứng thật thắng lời kể, và một người mệt 3 giờ sáng là đủ lý do cần hai
> người duyệt.

---

## 11. TypeScript Interfaces Cho Approval

Phần này gom toàn bộ bề mặt kiểu (interfaces) của hệ approval vào một chỗ — hợp đồng
chính thức cho mọi module muốn nối vào gate.

> 📄 **Code ví dụ:** [`examples/12-11-typescript-interfaces-cho-approval.ts`](examples/12-11-typescript-interfaces-cho-approval.ts)

> **Tóm gọn 1 câu:** Đây là "hợp đồng chính thức" của hệ approval bằng TypeScript —
> mọi module muốn gắn vào gate phải theo đúng các interface này.

---

## 12. Nguyên Tắc Thiết Kế Cho Approval

> Phần này chốt các nguyên tắc thiết kế: bố trí trách nhiệm theo SOLID, và sáu quy tắc
> vàng khi dựng hệ approval.

### 12.1 SOLID Cho Hệ Approval

*SOLID* = năm nguyên tắc thiết kế phần mềm: mỗi phần một việc (S), dễ mở rộng không cần
sửa (O), thay thế được nhau (L), không ép người dùng nhận thứ thừa (I), phụ thuộc vào
giao diện chứ không phụ thuộc chi tiết (D).

Cách đọc bảng này: cột "Nguyên tắc" là chữ cái SOLID kèm tên; cột "Áp dụng" là quy tắc đó biến thành gì trong hệ approval. Ví dụ: nguyên tắc S nghĩa là bảng xếp rủi ro và cỗ máy duyệt là hai thành phần riêng, mỗi cái một việc.

| Nguyên tắc | Áp dụng |
|-----------|---------|
| **S**ingle responsibility | `RiskTable` tag tier; `Gatekeeper` persist + settle; `Notifier` kênh; audit là *trajectory event*, không phải việc của gate |
| **O**pen/closed | Lớp hành động mới = `RiskTableEntry` mới, không đổi Gatekeeper |
| **L**iskov substitution | `TwoPersonGatekeeper` và `Gatekeeper` hoán đổi được cho engine qua interface `Gatekeeper` |
| **I**nterface segregation | Debug UI cần `verdict()`; compliance cần `auditEvent`; engine cần `request()/onVerdict()`. Đừng nối chúng. |
| **D**ependency inversion | Gatekeeper phụ thuộc `TrajectoryStore` + risk table, không phụ thuộc model hay engine loop |

> **Tóm gọn 1 câu:** Tách rời từng vai trò — bảng rủi ro xếp tier, Gatekeeper duyệt,
> Notifier gửi tin, audit ghi log — nên thêm loại hành động mới không phải sửa bộ máy
> duyệt.

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

> **Tóm gọn 1 câu:** Sáu quy tắc vàng: xếp tier lúc plan, duyệt bằng bằng chứng, hết giờ
> là từ chối, từ chối để học, sức chú ý người là ngân sách, và gate phải sống sót qua
> restart.

---

## 13. Best Practices

> Phần này là danh sách nên/không nên, rút gọn từ mọi mục trước — hữu ích khi review
> thiết kế của chính bạn.

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

> **Tóm gọn 1 câu:** Nên làm: xếp tier lúc plan, đủ bằng chứng, hết giờ là chặn, từ
> chối là vẽ lại kế hoạch, hai người cho việc hiểm, lưu gate qua restart, và đo dấu
> hiệu mệt mỏi.

### 13.2 KHÔNG NÊN ❌

- ❌ Không để model tự quyết có "cần approval" không — đó là gờ giảm tốc tự chọn.
- ❌ Không approve không diff (nút "tin tôi đi"). Bằng chứng là toàn bộ ý nghĩa.
- ❌ Không timeout-approve — timeout luôn fail-closed.
- ❌ Không retry cùng payload sau deny. Replan, đừng làm phiền.
- ❌ Không cho phép tự duyệt trên `prod-auth`, lặng lẽ hay có audit — cả hai đều vi phạm
  two-person.
- ❌ Không giữ gate chỉ trong memory; process restart quên mất gate đang mở là một lỗ
  hổng.
- ❌ Không xác nhận từng action `write`; đường cong fatigue sẽ biến an toàn của bạn
  thành kịch.
- ❌ Không để lời "ok" qua Slack/voice tính là verdict khi không có record.
- ❌ Không cắt bớt thông báo — kênh bị cắt bớt lặng lẽ hạ chất lượng quyết định.

> **Tóm gọn 1 câu:** Không nên làm: để model tự chấm rủi ro, duyệt mù, hết giờ là duyệt,
> hỏi lại sau khi bị từ chối, tự duyệt việc hiểm, giữ gate trong RAM, hay bắt duyệt
> từng việc nhỏ.

---

## 14. Anti-Patterns & Cách Khắc Phục

Cách đọc bảng này: mỗi dòng là một lỗi thường gặp. Cột "Triệu chứng" giúp bạn nhận ra lỗi đang xảy ra; cột "Cách sửa" là giải pháp cụ thể. Ví dụ: nếu approval rate gần 98% và người duyệt chán nản muốn hủy mọi thứ, bạn đang gặp anti-pattern rubber-stamping.

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

> **Tóm gọn 1 câu:** Mười hai lỗi kinh điển — từ duệt theo phản xạ, hỏi lại sau khi bị
> từ chối, đến gate mất khi restart — mỗi lỗi có một triệu chứng nhận ra được và một
> cách sửa cụ thể.

---

## 15. Production Checklist

Cách đọc: đây là danh sách kiểm tra trước khi ship. Mỗi dòng là một việc phải có; đánh
dấu ✓ khi mục đó đã được làm. Ví dụ: dòng "Fail closed" nghĩa là phải kiểm chứng hết
giờ chờ = bị từ chối, không có đường nào hết giờ mà vẫn chạy.

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

> **Tóm gọn 1 câu:** Mười lăm mục kiểm tra trước khi ship — thiếu bất kỳ mục nào trong
> số này, gate của bạn có một lỗ hổng đã được liệt kê ở trên.

---

## 16. Xu Hướng Tương Lai

> Phần này dự báo ba-năm-tới: quy tắc duyệt thành code, gate tự chặt/lỏng theo dữ liệu,
> và cách một người giám sát nhiều agent cùng lúc.

### 16.1 Registry Gate Policy-as-Code (2026-2028)

*Policy-as-code* = quy tắc duyệt viết thành file có phiên bản (như `approval-policy.yml`),
xem diff qua PR như code bình thường. Risk table di cư thành artifact policy-as-code
được version hóa, reviewable, được diff trong PR như mọi infra khác. Tier trở thành khai
báo có kiểm chứng ("mọi action `prod-auth` trong repo X nay phải page hai người"), và
một policy diff lặng lẽ hạ tier sẽ bị chặn bởi chính two-person rule đang bảo vệ các
action. Hệ gate trở thành cả *enforcer* lẫn *spec công khai* — hợp đồng "ai duyệt được
cái gì", version hóa cạnh code nó bảo vệ.

> **Tóm gọn 1 câu:** Trong 2-3 năm tới, quy tắc "hành động nào cần ai duyệt" sẽ viết
> thành file trong repo, có review như code — ai muốn hạ tier cũng phải qua hai người.

### 16.2 Adaptive Trust với Bằng Chứng Liên Tục

> Phần này nói về gate tự điều chỉnh độ chặt theo thành tích: lớp hành động làm tốt
> lâu năm được nới lỏng, lớp vừa gây sự cố bị siết lại.

Thay vì tier `elevated` cố định, trọng lượng của gate học từ trajectory: lớp hành động
có 6 tháng dry-run hoàn hảo và không incident sẽ có đường nhanh hơn, lặng hơn; lớp vừa
có incident sẽ *tự động* bị gate chặt hơn. Điều quan trọng: hạ trust phải tự động và
theo metric (rẻ, an toàn), trong khi *khôi phục* trust giữ là quyết định của con người
(đắt, chậm). Đây chính là bánh cóc một chiều của trust giúp hệ bảo mật ổn định.

> **Tóm gọn 1 câu:** Gate tương lai tự siết khi có sự cố nhưng chỉ nới lỏng nhờ quyết
> định của con người — mất niềm tin nhanh, lấy lại niềm tin chậm, đúng hướng an toàn.

### 16.3 Approval Như Một Định Lý Checkpoint

> Phần này cho thấy gate không cần cơ chế riêng: nó chỉ là một checkpoint có gắn kết
> quả duyệt, nên hưởng mọi thứ checkpoint đã có.

Gate sụp đổ về câu chuyện checkpoint/resume (→ 07 §13): *gate = checkpoint có gắn
verdict.* Khi đó mọi thứ hệ thống checkpoint đang cho — replay, idempotency, audit, fork
— áp vào gate miễn phí. Một "deploy gate" chỉ là node `checkpoint(pause_until=verdict)`
trong plan graph, được render thành panel timeline và replay cho review sau incident.

> **Tóm gọn 1 câu:** Xem gate như một checkpoint có kèm kết quả duyệt — mọi tính năng
> của checkpoint (chạy lại, idempotency, audit) tự nhiên áp dụng được cho gate.

### 16.4 Giám Sát Ở Quy Mô Con Người với Quy Mô Agent

> Phần này nói về tương lai một người giám sát nhiều agent: giao diện duyệt phải gộp mọi
> gate đang chờ vào một bảng, nhưng vẫn không cho một cú click mệt mỏi duyệt việc hiểm.

Khi một human giám sát nhiều agent, gate phải multiplex (ghép nhiều luồng vào một bề
mặt): một bề mặt review duy nhất hiện *tất cả* gate đang chờ, gộp theo rủi ro, batchable
theo quyết định, với flow "approve cùng lớp trừ prod-auth" — mà không bao giờ cho phép
một click mệt mỏi duyệt một action `prod-auth`. Chi phí của tương lai này là kinh tế học
cảnh giác: hệ thống phải ngừng hỏi khi human đã trống mắt, đó chính là lý do metric
rubber-stamp (→ 9.3) trở thành dashboard sản phẩm của năm năm tới.

> **Tóm gọn 1 câu:** Khi một người giám sát nhiều agent, mọi gate chờ về chung một
> bảng để duyệt gộp — nhưng hệ thống phải biết ngừng hỏi khi người duyệt đã kiệt sức.

---

## Tài Liệu Tham Khảo

> Phần này liệt kê nguồn gốc: bài nghiên cứu (cho các quy tắc tâm lý), công cụ tham
> khảo, và các module liên quan trong cùng bộ tài liệu.

### Papers & Research

- **Automation Bias and Automation Complacency** — Parasuraman & Manzey (2010) · https://link.springer.com/article/10.1007/s12170-010-0080-4
- **Trust in Automation: Designing for Appropriate Reliance** — Lee & See (2004) · https://journals.sagepub.com/doi/10.1518/hfes.46.1.50.30392
- **Human-AI Delegation** — Mapping delegation ontologies for AI agents · https://arxiv.org/abs/2309.01564
- **Comprehensible AI systems: Automation tragedy** — về việc bằng chứng thắng kể chuyện · https://arxiv.org/abs/2003.02334
- **Behavioral Data Science for Agent Oversight** *(khung thiết kế cho fatigue metric)* · https://arxiv.org/abs/2405.07355

> **Tóm gọn 1 câu:** Năm bài nghiên cứu nền cho mọi quy tắc của module: người tin máy mù
> quáng, niềm tin cần được thiết kế, và bằng chứng thắng lời kể.

### Frameworks & Tools

1. **Claude Code** — https://docs.anthropic.com/en/docs/claude-code — permission mode, `/permissions`, consent stream
2. **Aider** — https://aider.chat/docs/ — read/write mode, `--yes-always`, reversibility qua git
3. **OpenHands** — https://github.com/All-Hands-AI/OpenHands — confirmation strategy cho code + MCP
4. **NATS / approval bot qua webhook** — https://nats.io — transport thông báo + verdict
5. **OpenPolicyAgent (OPA)** — https://www.openpolicyagent.org — policy-as-code cho tier registry (→ 16.1)
6. **PolicyEngine** *(cổng policy phía server)* — https://github.com/policyengine

> **Tóm gọn 1 câu:** Sáu công cụ tham khảo khi triển khai: từ permission mode của
> Claude Code đến policy-as-code của OPA.

### Production Systems

- **Spacelift** — https://spacelift.io — plan/workflow approval với run-review (kiểu "approval như review," không phải "approval như click")
- **Atlantis** — https://www.runatlantis.io/apply-requirements — `apply_requirements` = hệ tier cho terraform
- **Claude Code** — https://claude.com/product/claude-code — consent stream permission
- **Devin** — https://devin.ai — panel giám sát không đồng bộ
- **CircleCI / GitHub Environments** — https://docs.github.com/en/actions/managing-workflow-runs/reviewing-deployments — approval cho protected environment

> **Tóm gọn 1 câu:** Năm hệ thống production đã làm approval ở quy mô thật — đối chiếu
> thiết kế của bạn với cách họ làm.

### Module Liên Quan

- `04-plan-decompose-task/README.md` §14.3 — gate phía planning ("ai được override"), deny→replan
- `06-decide-tools-mcp/README.md` §17.4 — UX consent phía tool
- `07-workflow/README.md` §13.4 — engine pause/resume + checkpoint (chủ nhà của gate)
- `12-sandbox-execution/README.md` — trần kỹ thuật mà gate bổ trợ
- `13-trajectory-observability/` — gate như event, audit + replay (§6 module này tiêu thụ nó)
- `14-compaction-context/README.md` — approval đang chờ là một phần của pin set (→ 14 §3.2)
- `08-task/README.md` §11 — idempotency cache làm cho resume an toàn

> **Tóm gọn 1 câu:** Gate không đứng một mình: nó gắn với planning (xếp tier), workflow
> (pause/resume), sandbox (khoanh vùng), và trajectory (ghi log).

---

*Tài liệu: Harness 15. Approval Gates — HARNESS ENGINEERING EDITION*
*Module cross-cutting · control plane cho hành động không đảo ngược · human-in-the-loop*
*Cập nhật: 16/10/2026*
*Tác giả: AI Knowledge Repository*

---

## Cập nhật 10/2026 — Approval Fatigue & UX

> Bổ sung sâu hơn về approval fatigue (§7.1 đã nêu) — failure mode lặng lẽ #1 của
> hệ human-in-the-loop: gate không bị bỏ, mà bị **đồng ký theo phản xạ**.

### 1. Approval Fatigue Là Gì — Và Vì Sao Nó Nguy Hiểm

Approval fatigue xảy ra khi gate nổ quá nhiều: user đối mặt hàng chục hộp duyệt
mỗi ngày, não bộ tự tối ưu bằng cách duyệt theo phản xạ — chính là **automation
bias** (xu hướng tin máy móc mù quáng; Parasuraman & Manzey, 2010; → §10.5). Ở
trạng thái đó:

- Gate vẫn *về mặt kỹ thuật* hoạt động — mọi hành động đều có approval.
- Gate *về mặt thực chất* đã chết — nút "Approve" thành phím Enter thứ hai.
- Tệ hơn không có gate: bạn **tưởng** có human review, nên hạ cảnh giác ở những
  lớp khác; mà thực tế không ai đọc gì cả.

Nghiên cứu delegation người-máy cho thấy false alarm bào mòn sự tỉnh táo:
gate nổ với thứ vô hại, human ngừng kiểm tra cả thứ thật (đường cong cry-wolf).
Metric phát hiện sớm nằm ở §9.3: **approval rate tăng + thời gian quyết định giảm
cùng lúc** = fatigue đã xuất hiện.

> **Tóm gọn 1 câu:** Hỏi quá nhiều → người duyệt bấm theo phản xạ → gate tưởng còn
> mà thật ra đã chết, và còn nguy hơn không có gate vì khiến bạn hạ cảnh giác.

### 2. Năm Mitigations

Cách đọc bảng này: mỗi dòng là một biện pháp chữa approval fatigue. Cột "Cách làm" là cách triển khai; cột "Khi nào dùng" là điều kiện áp dụng. Ví dụ: "Batching" nghĩa là gom nhiều thay đổi nhỏ thành một lần duyệt duy nhất.

| Mitigation | Cách làm | Khi nào dùng |
|-----------|----------|--------------|
| **Risk-based approval** | Chỉ gate S1/S2 (prod-auth, elevated); S3 read-only auto-approve + log. Gate đặt đúng cái đuôi đắt đỏ (§2.1), đừng đốt attention ở tầng rẻ | Luôn luôn — mặc định của tier taxonomy |
| **Batching** | Gom các ops rủi ro thấp cùng một segment plan thành **một** gate duy nhất với diff tổng | Nhiều edit `write` cùng một task (§7.1) |
| **Approval summary** | Payload luôn có diff + hậu quả + rollback; human duyệt *bằng chứng*, không duyệt *lời kể* | Mọi gate (quy tắc bằng chứng §3.2) |
| **Timeout-deny giữ nguyên** | Fatigue không phải lý do nới TTL hay fail-open; hết hạn vẫn là deny (§4.2) | Luôn luôn — không ngoại lệ |
| **Audit + review hằng tuần** | Xem approval rate / wait trung vị / pattern deny theo tier để **calibrate**: tier nào được stamp máy móc thì nâng ngưỡng hoặc bỏ gate | Nhịp cố định — không phải tùy hứng |

Mitigation nào cũng cùng một nguyên lý: *tốn ít attention của con người nhất cho
mỗi quyết định an toàn* — nghĩa là giết gate vô dụng để gate thật còn sống.

> **Tóm gọn 1 câu:** Năm biện pháp cùng một nguyên lý: bỏ hỏi ở chỗ rẻ, gộp hỏi ở chỗ
> nhỏ, luôn trình bằng chứng, không nới quy tắc hết giờ vì mệt mỏi, và review định kỳ
> để calibrate.

### 3. Anti-Pattern: Gate Theo Tool Call, Đúng Ra Gate Theo Nghiệp Vụ

**Anti-pattern:** gate *mỗi tool call* — đọc file xin duyệt, search xin duyệt,
grep xin duyệt. Sau hai ngày, user click-through vô thức mọi thứ, kể cả
`db.migrate` trên prod.

Nguyên tắc: **gate theo NGHIỆP VỤ, không gate theo kỹ thuật.**

Cách đọc bảng này: cột trái là cách hỏi sai (theo từng lệnh kỹ thuật); cột phải là cách hỏi đúng (theo việc nghiệp vụ có hậu quả thật). Ví dụ: đừng duyệt `read_file` — hãy duyệt "deploy lên prod".

| Gate ❌ theo kỹ thuật | Gate ✅ theo nghiệp vụ |
|----------------------|------------------------|
| `read_file`, `search`, `grep` | Deploy lên prod, force-push nhánh release |
| `list`, `view`, `stat` | Delete dữ liệu, đổi IAM / xoay secret |
| chạy test cục bộ | Gửi tin nhắn/email ra ngoài hệ thống |

Hành động kỹ thuật read-only có git + sandbox + audit che (reversibility — → §10.2
Aider); gate thật để dành cho thứ git không undo được. OpenHands ("xác nhận mọi
thay đổi") là case study chính của lỗi này — ergonomics tệ nhất vì nó *luyện*
rubber-stamp (§10.3).

> **Tóm gọn 1 câu:** Đặt gate theo hậu quả nghiệp vụ (deploy, xóa dữ liệu, gửi ra
> ngoài), không phải theo từng lệnh kỹ thuật — nếu không, phản xạ bấm cho qua sẽ nuốt
> cả gate thật.

### 4. Liên Kết Kiến Trúc

Approval gate nằm ở **Layer 7 (Execution & Safety)** — trần kỹ thuật mà gate bổ
trợ, trong kiến trúc 9 layer. Xem
[AGENT_SYSTEM_ARCHITECTURE.md](../../AGENT_SYSTEM_ARCHITECTURE.md) (Layer 7).

> **Tóm gọn 1 câu:** Approval gate thuộc Layer 7 (Thực thi & An toàn) của kiến trúc 9
> layer — chi tiết kiến trúc tổng thể nằm trong file AGENT_SYSTEM_ARCHITECTURE.md.
