# 🗜️ Harness 14. Context Compaction

> ## 📑 Mục Lục
>
> - [Opening Story](#opening-story)
> - [Vì Sao Compaction Là Bắt Buộc?](#vì-sao-compaction-là-bắt-buộc)
> - [Overview](#overview)
> - [Mục Lục Chi Tiết](#mục-lục-chi-tiết)
> - [1. Định Nghĩa & Thuật Ngữ](#1-định-nghĩa--thuật-ngữ)
>   - [1.1 Các thuật ngữ cốt lõi](#11-các-thuật-ngữ-cốt-lõi)
>   - [1.2 Hai họ kỹ thuật: Summarization và Pruning](#12-hai-họ-kỹ-thuật-summarization-và-pruning)
> - [2. Policy Trigger](#2-policy-trigger)
>   - [2.1 Vì sao 70% chứ không phải 90%](#21-vì-sao-70-chứ-không-phải-90)
>   - [2.2 Các chiến lược trigger](#22-các-chiến-lược-trigger)
> - [3. Pin Set — Thứ Gì Phải Sống Sót](#3-pin-set--thứ-gì-phải-sống-sót)
>   - [3.1 Pinned và evictable](#31-pinned-và-evictable)
>   - [3.2 Pin set](#32-pin-set)
> - [4. Pruning Theo Utility](#4-pruning-theo-utility)
>   - [4.1 Vì sao chỉ recency là không đủ](#41-vì-sao-chỉ-recency-là-không-đủ)
>   - [4.2 Chấm utility nhận thức trajectory](#42-chấm-utility-nhận-thức-trajectory)
>   - [4.3 Thu gọn, đừng xoá](#43-thu-gọn-đừng-xoá)
> - [5. Resume Block](#5-resume-block)
>   - [5.1 Định dạng](#51-định-dạng)
>   - [5.2 Chuẩn chất lượng](#52-chuẩn-chất-lượng)
> - [6. Contract Compaction↔Memory](#6-contract-compactionmemory)
>   - [6.1 Ranh giới](#61-ranh-giới)
>   - [6.2 Contract hay vỡ nhất trong production](#62-contract-hay-vỡ-nhất-trong-production)
> - [7. Prompt Chống Chịu Compaction](#7-prompt-chống-chịu-compaction)
>   - [7.1 Header / Body / Footer](#71-header--body--footer)
>   - [7.2 Cái gì bị summarizer bỏ](#72-cái-gì-bị-summarizer-bỏ)
> - [8. Implementation TypeScript](#8-implementation-typescript)
>   - [8.1 Types](#81-types)
>   - [8.2 shouldCompact + compact()](#82-shouldcompact--compact)
>   - [8.3 Bộ chấm utility theo trajectory](#83-bộ-chấm-utility-theo-trajectory)
>   - [8.4 Builder cho resume block](#84-builder-cho-resume-block)
>   - [8.5 Write-back vào memory](#85-write-back-vào-memory)
> - [9. Kiểm Thử Compaction](#9-kiểm-thử-compaction)
>   - [9.1 Test bất biến](#91-test-bất-biến)
>   - [9.2 Contract test quan trọng nhất](#92-contract-test-quan-trọng-nhất)
>   - [9.3 Bộ hồi quy chất lượng](#93-bộ-hồi-quy-chất-lượng)
> - [10. Case Study Thực Tế](#10-case-study-thực-tế)
>   - [10.1 Claude Code — /compact và Auto-Compact](#101-claude-code--compact-và-auto-compact)
>   - [10.2 Aider — Repo Map + History Digest](#102-aider--repo-map--history-digest)
>   - [10.3 Devin — Quản Lý Context Cho Run Dài](#103-devin--quản-lý-context-cho-run-dài)
>   - [10.4 Letta / MemGPT — Memory phân tầng như context ảo](#104-letta--memgpt--memory-phân-tầng-như-context-ảo)
>   - [10.5 Lost in the Middle — Nghiên cứu đứng sau pinning](#105-lost-in-the-middle--nghiên-cứu-đứng-sau-pinning)
> - [11. TypeScript Interfaces Cho Compaction](#11-typescript-interfaces-cho-compaction)
> - [12. Nguyên Tắc Thiết Kế Cho Compaction](#12-nguyên-tắc-thiết-kế-cho-compaction)
>   - [12.1 SOLID cho quản lý context](#121-solid-cho-quản-lý-context)
>   - [12.2 Sáu nguyên tắc thiết kế](#122-sáu-nguyên-tắc-thiết-kế)
> - [13. Best Practices](#13-best-practices)
>   - [13.1 NÊN ✅](#131-nên-)
>   - [13.2 KHÔNG NÊN ❌](#132-không-nên-)
> - [14. Anti-Patterns & Cách Khắc Phục](#14-anti-patterns--cách-khắc-phục)
> - [15. Production Checklist](#15-production-checklist)
> - [16. Xu Hướng Tương Lai](#16-xu-hướng-tương-lai)
> - [Tài Liệu Tham Khảo](#tài-liệu-tham-khảo)
>
> **Module cross-cutting.** Compaction là lý do một agent chạy được vài giờ thay vì
> vài phút. Module này sở hữu ranh giới giữa *context tạm* (→ 02) và *memory bền*
> (→ 03) — contract giữa hai bên này bị vi phạm nhiều hơn bất kỳ contract nào khác
> trong hệ production.

---

### Opening Story

Lượt thứ 47. Agent đang giữa một cuộc refactor: 31 tool call, bốn file được viết lại,
hai bộ test đã chạy, một stack trace gây rối nằm ở đâu đó giữa chừng. Context window
đang ở 96%. Tool result kế tiếp dài 4.000 token và không vừa.

Giờ đội có ba lựa chọn tệ và không có lựa chọn tốt nào:

1. **Để nó chết.** Run chết ở lượt 47 với lỗi độ dài context. Người dùng thấy "có
   gì đó sai" sau 20 phút.
2. **Cắt bừa.** Bỏ các message cũ nhất. Agent mất đặc tả nhiệm vụ được giao ở lượt 1,
   đọc lại một file đã đọc ở lượt 12 (vì *kết quả* đã mất nhưng *bản sửa* vẫn còn), và
   tự tin sinh ra một patch huỷ chính công sức của nó ở lượt 30.
3. **Tóm tắt mọi thứ như nhau.** Nén toàn bộ transcript thành một đoạn. Đoạn đó nhắc
   stack trace và bỏ mất định nghĩa nhiệm vụ, nên agent giải quyết nhầm vấn đề một
   cách trôi chảy.

**Không cái nào trong ba là "compaction".** Compaction là một *policy*: một điều kiện
kích hoạt, một pin set gồm những thứ không bao giờ được loại, một hàm utility quyết
định cái gì đi tiếp theo, và một resume block dựng lại trạng thái của run theo cấu
trúc cố định. Làm đúng bốn thứ đó thì lượt 47 trở nên tầm thường. Làm sai thì lỗi
*vô hình* — run *hoàn thành*, chỉ là hoàn thành sai nhiệm vụ.

### Vì Sao Compaction Là Bắt Buộc?

> *"Bất kỳ agent nào không sống sót được chính context window của nó là một demo,
> không phải một sản phẩm."*

#### Phép tính

| Ngân sách | Input mỗi lượt | Số lượt trước khi cạn | Với trigger 70% + compaction |
|-----------|-----------------|------------------------|-------------------------------|
| 200k (lớn) | ~6k | ~33 | không giới hạn |
| 128k (điển hình) | ~4k | ~32 | không giới hạn |
| 32k (nhỏ/local) | ~2k | ~16 | không giới hạn |

**Không giới hạn** chính là điểm. Compaction không phải tối ưu hoá; nó là cơ chế biến
context cố định thành một run dài không giới hạn. Nó cũng là thứ làm cho
checkpoint-resume của `07-workflow` khả thi (→ 07 §13), giao nốt sub-agent ở
`09-multi-agent` trở thành hiện thực (→ 09 §16.2), và loop budget của
`10-automation` có thể ép được (→ 10 §17.3) — mỗi thứ đều cần một run sống lâu hơn
một context window.

#### Hiệu ứng bậc hai

- **Chi phí.** Compaction giảm mạnh input token mỗi lượt trên run dài, vì một resume block 60 KB thay cho 180 KB lịch sử. Các đội thường thấy giảm 40–70% chi phí trên các run quá 30 lượt.
- **Chất lượng.** Compaction *có thể* làm giảm chất lượng — đó là điều §5–7 nói tới. Làm cẩu thả thì nó tệ hơn hẳn việc không compaction, vì mô hình sẽ tự tin suy luận trên một bản tóm tắt bị hao hụt.
- **Khả năng audit.** Compaction sinh ra một event `compaction` (→ 13) ghi lại chính xác điều gì được giữ, điều gì bị loại. Một harness mà bạn không dựng lại được mô hình đã mất gì là một harness bạn không debug được.

## Overview

> **📌 Khái Niệm Cốt Lõi**
>
> - **Khái niệm:** Compaction là **tổng hợp có trigger**: khi context vượt ngưỡng, các span giá trị thấp được thay bằng một resume block có cấu trúc thay vì đâm vào trần token. **Pruning** là người bạn đồng hành — quyết định *cái gì* đi trước theo utility, không theo recency.
> - **So sánh:** Như xếp vali nhỏ cho chuyến đi dài. Vali tràn thì không quăng bừa; bạn có quy tắc (đồ vệ sinh ở lại, hoá đơn cũ đi) và để lại danh sách những gì đã bỏ.
> - **Vì sao quan trọng:** Mọi run agent dài đều chết nếu không compaction: tràn context, sụp chất lượng kiểu lost-in-the-middle, và hoá đơn token gấp 3–5× vì gửi lại tool output chết. Compaction ở 70% giữ run sống vô hạn với chi phí phẳng.

**Context Compaction** là thứ cho phép một context window cố định gánh một run không
giới hạn. Đây là phần ít được thiết kế nhất trong hầu hết agent harness, và cũng là
phần tốn kém nhất khi làm sai.

```
TRƯỚC compaction (188k trên ngân sách 200k)
┌──────────────────────────────────────────────────────────────┐
│ [system] [goal] [lượt 1..46: 31 tool call, 4 edit, test]     │
│ ▲ pinned   ▲ mọi thứ ở đây đều evictable — 178k              │
└──────────────────────────────────────────────────────────────┘
              │ trigger: dùng > 70% ngân sách
              ▼
SAU compaction (74k trên ngân sách 200k)
┌──────────────────────────────────────────────────────────────┐
│ [system] [goal] [PIN: 3 quyết định mở] [PIN: lỗi cuối]    │
│ ┌──────────────────────────────────────────────────────────┐ │
│ │ RESUME BLOCK (280 token)                                │ │
│ │ Goal: refactor auth middleware dùng shared session       │ │
│ │ Decisions: session store = redis; giữ shim jwt compat    │ │
│ │ Open: [t5] cập nhật 3 call site; [t6] chạy integration  │ │
│ │ Repro: npm test -- auth → FAIL test_refresh_rotation     │ │
│ │ Next: sửa refresh rotation, rồi t5, t6                  │ │
│ │ Evicted: [span id 7,12,18,22,29,31,…,46] (74 span)     │ │
│ └──────────────────────────────────────────────────────────┘ │
│ [3 lượt gần nhất nguyên văn] ← đuôi recency vẫn đọc được  │
└──────────────────────────────────────────────────────────────┘
```

**Bốn thành phần, và thiếu một là bug:**

| # | Thành phần | Hỏng thế nào nếu thiếu |
|---|-----------|------------------------|
| 1 | **Trigger** | Run chết ở trần |
| 2 | **Pin set** | Định nghĩa nhiệm vụ bị loại; agent giải sai bài |
| 3 | **Xếp hạng utility** | FIFO loại mất goal, giữ lại `ls` của hôm qua |
| 4 | **Resume block** | Agent tỉnh dậy không có trạng thái, đọc lại mọi thứ, hoá đơn gấp ba |
| 5 | **Write-back memory** *(thường bị bỏ sót)* | Quyết định biến mất cùng span bị loại và không bao giờ được lưu |

## Mục Lục Chi Tiết

| # | Chủ đề | Mô tả |
|---|-------|-------|
| 1 | [Định nghĩa](#1-định-nghĩa--thuật-ngữ) | Thuật ngữ và hai họ kỹ thuật |
| 2 | [Policy trigger](#2-policy-trigger) | Khi nào, và vì sao 70% |
| 3 | [Pin set](#3-pin-set--thứ-gì-phải-sống-sót) | Cái gì không bao giờ bị loại |
| 4 | [Pruning theo utility](#4-pruning-theo-utility) | Loại nhận thức trajectory |
| 5 | [Resume block](#5-resume-block) | Định dạng và chuẩn chất lượng |
| 6 | [Contract với memory](#6-contract-compactionmemory) | Contract hay vỡ nhất |
| 7 | [Prompt compaction-safe](#7-prompt-chống-chịu-compaction) | Sống sót qua tổng hợp |
| 8 | [Implementation](#8-implementation-typescript) | Compaction chạy được |
| 9 | [Kiểm thử](#9-kiểm-thử-compaction) | Bất biến + contract test |
| 10 | [Case study](#10-case-study-thực-tế) | Claude Code, Aider, Devin, Letta, lost-in-the-middle |
| 11 | [TypeScript Interfaces](#11-typescript-interfaces-cho-compaction) | Toàn bộ bề mặt kiểu |
| 12 | [Nguyên tắc thiết kế](#12-nguyên-tắc-thiết-kế-cho-compaction) | SOLID cho context |
| 13 | [Best practices](#13-best-practices) | NÊN / KHÔNG NÊN |
| 14 | [Anti-patterns](#14-anti-patterns--cách-khắc-phục) | Lỗi thường gặp |
| 15 | [Production checklist](#15-production-checklist) | Cổng ship |
| 16 | [Xu hướng tương lai](#16-xu-hướng-tương-lai) | 2026-2028 |

---

## 1. Định Nghĩa & Thuật Ngữ

### 1.1 Các thuật ngữ cốt lõi

| Thuật ngữ | Định nghĩa | Hỏng khi… |
|-----------|-----------|-----------|
| **Auto-compaction** | Tổng hợp có trigger khi `used > ngưỡng`; span evictable được thay bằng resume summary | thiếu trigger → run chết |
| **Resume block** | Struct ≤300 token: `Goal / Decisions / Open / Repro / Next` + `evicted_span_ids` | không ràng buộc → phình thành vấn đề mới |
| **Trajectory-aware pruning** | Thứ tự loại suy ra từ execution graph (giữ critical path, bỏ nhánh chết) | chỉ recency → mất goal |
| **Compaction ratio** | `tokens_before ÷ tokens_after` — chỉ số sức khoẻ | <1,5 với context lớn → summarizer đang hỏng |
| **Pin set** | Lõi không evictable: system, goal, ràng buộc, diff đang mở, lỗi cuối | vắng mặt → đặc tả nhiệm vụ bị loại |
| **Write-back** | Lưu resume + quyết định + việc còn mở vào memory **trước khi** chúng rời context | bỏ qua → quyết định mất vĩnh viễn |
| **Lost in the middle** | Độ chính xác giảm khi thông tin quan trọng nằm giữa context | bỏ qua → pinning trở nên tuỳ ý |

### 1.2 Hai Họ Kỹ Thuật: Summarization và Pruning

Chúng bổ trợ nhau, không phải hai lựa chọn thay thế, và nhầm lẫn chúng là gốc rễ của
phần lớn hiện thực tệ.

| | **Summarization** | **Pruning** |
|---|------------------|------------|
| **Làm gì** | Nén một span thành văn xuôi | Bỏ hẳn một span |
| **Khi nào** | Span cần dùng nhưng quá lớn | Span không cần dùng |
| **Bằng cách nào** | Mô hình tóm tắt, hoặc template xác định | Chấm utility + loại |
| **Chi phí** | Lời gọi LLM (~1–3 s) hoặc template | miễn phí |
| **Rủi ro** | Mất chi tiết, tóm tắt bịa | Mất thông tin trông như không cần |
| **Áp cho** | Tool output cũ, file đọc dài | Nhánh thất bại, diff bị thay thế, chit-chat |

**Thứ tự rất quan trọng:** prune trước (miễn phí, không mất thông tin của nhánh chết),
rồi mới tóm tắt phần còn lại quá lớn (tốn kém, có hao hụt). Các đội tóm tắt trước rồi
mới prune không bao giờ trả được gần 40% chi phí và vẫn giữ nhiều thông tin hơn.

---

## 2. Policy Trigger

### 2.1 Vì Sao 70% Chứ Không Phải 90%

```
100% ──── trần cứng: chính request thất bại. Không phục hồi được, không log được.
 90% ──── "gần đủ" — nhưng tool result kế tiếp thường vượt 10% ngân sách.
 70% ──── chừa 30% headroom: 2-3 lượt tool result kế tiếp vừa mà không phải compact lại.
 50% ──── hăng hái quá: 2 lần compaction mỗi run, tốn chất lượng, tốn lời gọi LLM.
```

Lỗi ở mốc 90% rất cụ thể và rất thường gặp: một lần `read_file` 30 KB tiêu 8% của cửa
sổ 200k trong *một* step. Trigger ở 90%, nhận một kết quả 8%, giờ ở 98% — và kết quả
*kế tiếp* tràn, buộc phải compact lại giữa chừng task, với ít chỗ để tóm tắt cho ra
hàng. Compaction dưới áp lực đúng là lúc bạn không thể chịu sự hao hụt.

**Quy tắc: trigger khi bạn vẫn còn đủ khả năng tóm tắt cho tử tế.**

### 2.2 Các Chiến Lược Trigger

| Chiến lược | Quy tắc | Dùng khi |
|------------|---------|----------|
| **Ngưỡng** | `used / budget > 0.70` | mặc định, đơn giản, dự đoán được |
| **Số lượt** | `turns > 20` | ước tính token không đáng tin; chốt chặn rẻ |
| **Tốc độ tăng** | compact khi `used` tăng >25% trong 3 lượt | phát hiện vòng lặp tool |
| **Biên task** | compact giữa các task, không ở giữa một task | session nhiều task; giữ nguyên suy luận của một task |
| **Kích thước bước kế** | compact khi `est(next_result) > headroom` | ngân sách chật (32k) |

Khuyến nghị production: **ngưỡng HOẶC số lượt**, cái nào tới trước, cộng thêm
compaction tại biên task khi plan (→ 08) có đường nối tự nhiên. Tốc độ tăng là một
cảnh báo hữu ích cho "run này đang lặp" (→ 10 §17.3).

**Không bao giờ để mô hình quyết định.** Compaction là policy của harness, tính từ
số token đo được. Một mô hình được hỏi "có nên compact không?" sẽ trả lời "không,
tôi ổn" khi đang giữ 195k token.

---

## 3. Pin Set — Thứ Gì Phải Sống Sót

### 3.1 Pinned và Evictable

Pin set trả lời câu hỏi: "mất nó thì run có sai không?". Bất cứ thứ gì mà việc mất nó
làm thay đổi *nhiệm vụ* chứ không phải *khẩu vị* — thì pin.

| Pinned (không bao giờ loại) | Evictable (theo thứ tự loại) |
|----------------------------|------------------------------|
| System prompt | Tool stdout cũ hơn 3 lượt |
| Task spec + definition of done | Phiên bản file bị thay thế bởi edit sau |
| Chỉ dẫn gần nhất của user | Retrieved chunk có score <0,3 |
| Diff đang được sửa | Chit-chat, chào hỏi, bình luận meta |
| Invariant / ràng buộc từ plan | `ls`/`cat` lặp lại cùng một file |
| Tín hiệu lỗi cuối của loop đang chạy | Nhánh giả thuyết đã bỏ |
| Trạng thái approval đang chờ (→ 15) | Approval đã hết hạn, đã có verdict |
| Schema output mô hình phải tạo ra | Lịch sử của một subtask đã xong |
| Con trỏ tới memory bền | Tool output chết tốn token (tóm tắt, không bỏ hẳn) |

**Tinh tế:** "tín hiệu lỗi cuối" được pin *chỉ cho loop đang hoạt động*. Khi loop đã
được giải quyết, lỗi đó trở thành evictable. Pin nó vĩnh viễn nghĩa là pin set của bạn
tăng đơn điệu và cuối cùng vượt ngân sách — một kiểu hỏng khác, và âm thầm.

### 3.2 Pin Set

```typescript
export interface PinSet {
  tenantId: string;                   // khoá định tuyến + nhất quán (→ 05 §17.5)
  system: true;                       // luôn luôn
  goal: true;                         // task spec + definition of done
  invariants: string[];               // ≤5 ràng buộc từ plan (→ 05 §17.5)
  activeDiffPaths: string[];          // file có edit chưa commit
  lastUserMessage: true;              // chỉ dẫn gần nhất thắng
  activeLoopFailure?: { cmd: string; error: string };   // chỉ khi loop chưa xong
  pendingApprovals: string[];         // gate key đang chờ verdict (→ 15)
  schema: true;                       // hình dạng câu trả lời cuối
}

export function isPinned(span: ContextSpan, pins: PinSet, planState: PlanState): boolean {
  if (span.role === "system" || span.kind === "goal" || span.kind === "schema") return true;
  if (span.kind === "user" && span.id === pins.lastUserMessage) return true;
  if (span.kind === "invariant") return true;
  if (span.kind === "diff" && pins.activeDiffPaths.includes(span.path!)) return true;
  if (span.kind === "failure" && planState.activeLoopUnresolved) return true;
  if (span.kind === "approval" && pins.pendingApprovals.includes(span.gateKey!)) return true;
  return false;
}
```

**Quy tắc: pin set được suy ra, không thao tác tay.** Nó tính từ plan, loop đang hoạt
động, và danh sách gate đang chờ — nên tự co lại khi công việc hoàn thành thay vì phình
ra.

---

## 4. Pruning Theo Utility

### 4.1 Vì Sao Chỉ Recency Là Không Đủ

Giả định FIFO/loại cái cũ nhất rằng giá trị suy giảm theo tuổi. Trong trajectory agent,
điều đó không đúng:

```
lượt  1  [goal]                          ← 2k token, pinned, 4 giờ trước
lượt  2  [plan]                          ← 1k token, pinned
lượt  3  [đọc package.json]              ← 3k token, vô dụng lúc này
lượt  4  [tool output 40KB]              ← cần cho lượt 44
lượt 12  [ràng buộc: "không thêm dep"]   ← 80 token, vẫn còn hiệu lực
lượt 44  [edit]                          ← pinned
```

Loại các span cũ không pinned sẽ loại output ở lượt 4 và ràng buộc ở lượt 12 — một
cái vô dụng, một cái chí mạng — và giữ lại ba lần `ls` ở các lượt 38–40 vì chúng gần
đây. Agent sau đó tự suy ra một dependency vi phạm ràng buộc đang có hiệu lực.

### 4.2 Chấm Utility Nhận Thức Trajectory

```
utility = 0.30·recency + 0.40·structural_reachability + 0.30·failure_signal
```

| Thành phần | Ý nghĩa | Cách tính |
|------------|---------|----------|
| `recency` | Tuổi chuẩn hoá: `exp(-turns_old / 12)` | rẻ, chặn cũ hoá vô hạn |
| `structural_reachability` | Span này có nằm trên critical path tới goal hiện tại không? | BFS trên plan graph (→ 04) từ task đang hoạt động; span nuôi một node *đang chờ* điểm cao, span nuôi node *đã xong* điểm thấp |
| `failure_signal` | Span có mang lỗi mà loop đang săn không? | so khớp chuỗi/trace với lỗi cuối của loop (xem §8.3) |

Rồi loại theo utility tăng dần, không bao giờ vượt ngân sách. Quan trọng là **thứ tự
này hoạt động trên plan graph, không phải trên danh sách message** — đó là lý do nó
cần `08` và `04` để hữu ích.

```typescript
/** Cài đặt tham chiếu: §8.3. Tín hiệu lỗi cuối của loop đáng 0.30 — thiếu nó, một
 *  run mắc kẹt trong vòng retry sẽ chấm mọi span điểm giống nhau. */
export function utility(span: ContextSpan, plan: PlanGraph, loop: ActiveLoop | null, now: number): number {
  const recency = Math.exp(-(now - span.turn) / 12);
  const serves = span.producedFor ?? [];
  const reachable = serves.length === 0 ? 0.4
    : serves.some(t => plan.pendingIds.includes(t))      ? 1.0    // vẫn cần
    : serves.every(t => plan.completedIds.includes(t))    ? 0.1    // nhánh đã xong
    : 0.4;                                                       // song song / chưa rõ
  const failure = loop?.unresolved && span.text?.includes(firstLine(loop.error)) ? 1 : 0;
  return 0.30 * recency + 0.40 * reachable + 0.30 * failure;
}
```

### 4.3 Thu Gọn, Đừng Xoá

Hai tinh chỉnh phân biệt một hiện thực tốt với một hiện thực "chạy được":

1. **Gộp các retry giống hệt nhau.** Ba lần `npm test` thất bại giống nhau trở thành
   `retried 3×, last_err: E2BIG at test_refresh_rotation`. Thông tin quan trọng (nó
   fail, lý do, đã retry) còn lại với 1/30 chi phí.
2. **Tóm tắt trước khi bỏ nhánh chết.** Một nhánh đã xong không *vô nghĩa* — nó giải
   thích vì sao agent giờ ở chỗ khác. Một dòng: `nhánh t3 (vector cache) bị loại: thêm
   400ms p99`. Rẻ, và ngăn agent đi lại vùng đó.

```
lượt 38,39,40:  npm test (exit 1)  ──┐
lượt 41,42,43:  npm test (exit 1)  ──┼──▶  [retry 6×, last_err: E2BIG @ test_refresh_rotation]
lượt  44:        npm test (exit 1)  ──┘        (từ lượt 38, 18k token → 24 token)
```

---

## 5. Resume Block

### 5.1 Định Dạng

Key cố định, ngân sách cứng, kiểm được bằng máy:

```
Goal:<một dòng — nhiệm vụ, không phải kế hoạch>
Decisions:[D1: …][D2: …][D3: …]        ≤5, mỗi cái ≤25 từ
Open:[t5: …][t6: …]                    task đang chờ kèm ID (→ 08)
Repro:<lệnh chính xác + dòng lỗi cuối>
Next:<đúng một hành động kế tiếp>
Invariants:[…]                          ≤5 ràng buộc được pin
Evicted:[danh sách span-id]            để audit + dựng lại
```

**Vì sao key phải cố định:** resume block được đọc lại bởi *code*, không chỉ bởi mô
hình. Một parser lấy `Open[]` để dựng lại danh sách task chờ, `Repro` để gieo lại retry,
và `Evicted[]` để write-back vào memory và phát event audit. Văn xuôi tự do phá cả ba.

### 5.2 Chuẩn Chất Lượng

Một resume block tốt khi một **agent mới với context rỗng** có thể tiếp tục run và làm
đúng bước kế tiếp. Kiểm thử đúng bằng cách đó:

```typescript
/** Bài test chấp nhận cho một resume block: agent lạnh có đi tiếp được không? */
export function resumeIsSufficient(block: ResumeBlock, nextAction: string): boolean {
  return block.goal.length > 0                                    // không mục đích thì không có nhiệm vụ
      && block.open.length > 0                                    // phải biết còn việc gì
      && block.repro.command.length > 0                           // phải lặp lại được lỗi
      && block.next.length > 0                                    // phải biết làm gì tiếp
      && countTokens(block) <= 300;                               // ngân sách cứng
}
```

Một block ghi "chúng ta đang refactor authentication và gặp vài vấn đề" fail mọi dòng
trên. Nó *có vẻ* giàu thông tin và vô dụng — đây là cách phổ biến nhất để compaction âm
thầm phá một run.

---

## 6. Contract Compaction↔Memory

### 6.1 Ranh Giới

| Tạm — context sở hữu (→ 02) | Bền — memory sở hữu (→ 03) |
|------------------------------|---------------------------|
| Tool stdout thô | Fact đã pin |
| Body của retrieved chunk | Quyết định và lý do của nó |
| Phiên bản file đã bị thay thế | TODO còn mở |
| Chit-chat | Sở thích người dùng |
| Nhánh chết | **Resume block** |
| — | Invariant / ràng buộc |

Ranh giới không phải "quan trọng vs không quan trọng". Nó là **"sau run này còn cần
không?"**. Tool stdout ở lượt 4 có thể cần ở lượt 44, nhưng không cần sau lượt 60 — đó
là việc của context. Một quyết định ở lượt 12 sẽ cần cho một *run khác* tuần sau — đó
là việc của memory.

### 6.2 Contract Hay Vỡ Nhất Trong Production

**Lỗi:** compaction loại một span, và thông tin bên trong nó chưa bao giờ được lưu. Lượt
sau, mô hình không biết vì sao mình đã quyết định điều đó, và tự suy ra khác đi. Run
*thành công* và codebase lệch nhẹ so với thiết kế mà người dùng đã đồng ý bốn mươi
phút trước.

**Quy tắc:** write-back **trước khi** loại. Không phải sau, không phải "để sau" —
trước. Trình tự:

```
1. chọn span để loại (utility tăng dần)
2. trích nội dung bền: quyết định, việc còn mở, invariant, sở thích người dùng
3. lưu vào memory (scope tenant + task)                    ← fsync (→ 13)
4. phát event compaction: { keptIds, evictedIds, ratio, resumeHash }
5. thay span bị loại bằng resume block
6. tiếp tục run
```

Bước 3 thất bại thì phải huỷ bước 5. Không phải log một cảnh báo — phải huỷ. Một
compaction đánh mất một quyết định đã tạo ra một run không thể tin, và cách rẻ nhất
để làm điều đó bất khả thi là làm nó *fail thật to*.

**Bài kiểm chứng** nằm ở §9.2, và nó là bài test đáng giá nhất của cả module: tắt
memory backend, chạy một compaction, và assert run từ chối đi tiếp.

---

## 7. Prompt Chống Chịu Compaction

### 7.1 Header / Body / Footer

Compaction có hao hụt, nên hãy thiết kế prompt để sống sót qua nó:

```
[HEADER — invariant, luôn được giữ]
  Bạn đang refactor auth middleware sang shared session store.
  Invariant: (1) không thêm dependency runtime (2) token JWT v1 vẫn phải validate
  (3) không đổi bề mặt API công khai.
  Output: một unified diff + một đoạn ghi chú migration.

[BODY — context truy xuất, được loại tuỳ ý]
  … 12 chunk, 4 thân file, 31 tool output …

[FOOTER — nhắc lại invariant]
  Nhắc trước khi trả lời: không thêm dep; giữ tương thích JWT v1; output phải là
  diff rồi tới ghi chú migration.
```

**Cơ sở thực nghiệm** là kết quả lost-in-the-middle (§10.5): mô hình chú ý đáng tin
cậy nhất ở đầu và cuối một context dài. Đặt invariant ở cả hai nơi nghĩa là một
summarizer chỉ giữ phần đầu *và* phần cuối vẫn giữ được ràng buộc — và một summarizer
giữ 80% token giữ chúng gần như chắc chắn.

### 7.2 Cái Gì Bị Summarizer Bỏ

Biết các kiểu hỏng cho biết cần pin gì:

| Thường bị bỏ | Cách khắc phục |
|---------------|---------------|
| Mệnh đề phủ định ("KHÔNG thêm dep") | Đặt ở HEADER + FOOTER, nguyên văn |
| Số (timeout, số lượng, giới hạn) | Pin giá trị chính xác; không diễn giải lại |
| ID và tên (task id, đường dẫn file) | Giữ dạng thô trong `Open[]`, không để trong văn xuôi |
| Cấu trúc tool output (trường nào hỏng) | `Repro` giữ dòng lỗi thô |
| Sự bất định ("tôi nghĩ", "chắc là") | Pin *chỉ dẫn user cuối* — thường mang nó |
| Ràng buộc thứ tự (X trước Y) | `Next` nói rõ thứ tự |

Quy tắc chung: **diễn giải là nơi độ chính xác chết.** Một summarizer được yêu cầu
"nén lại" sẽ viết "timeout khoảng 30 giây" thay vì `timeoutMs: 30000`. Hãy pin giá
trị thô; để phần tóm tắt giải thích quanh nó.

---

## 8. Implementation TypeScript

### 8.1 Types

```typescript
export interface ContextSpan {
  id: string;                    // span_01H…  — đơn vị bị loại
  kind: "system" | "goal" | "schema" | "invariant" | "user" | "assistant"
      | "tool_output" | "diff" | "failure" | "approval" | "chitchat" | "branch";
  role: "system" | "user" | "assistant" | "tool";
  turn: number;
  tokens: number;
  text?: string;
  path?: string;                 // cho span diff
  tool?: string;
  gateKey?: string;              // cho span approval
  producedFor?: string[];        // các task id span này phục vụ (plan graph, → 08)
  keep?: boolean;                // pin cứng, thắng điểm chấm
}

export interface ResumeBlock {
  goal: string;
  decisions: string[];           // ≤5
  open: { taskId: string; title: string }[];
  repro: { command: string; error: string };
  next: string;
  invariants: string[];
  evicted: string[];             // span id
}
```

### 8.2 shouldCompact + compact()

<details>
<summary>TypeScript Code — trigger + pin + prune theo utility + resume (Click để mở rộng/thu gọn)</summary>

```typescript
export const COMPACT_AT = 0.70, RESUME_BUDGET = 300, MAX_TURNS = 20;

export function shouldCompact(used: number, budget: number, turns: number): boolean {
  return used / budget > COMPACT_AT || turns > MAX_TURNS;
}

export interface CompactOutcome {
  kept: ContextSpan[]; resume: ResumeBlock;
  ratio: number; dropped: string[]; writeBack: DurableExtract;
}

export function compact(
  spans: ContextSpan[], budget: number, goal: string,
  pins: PinSet, plan: PlanGraph, activeLoop: ActiveLoop | null,
): CompactOutcome {
  // 1. Pin set trước — không bao giờ là ứng viên bị loại, bất kể điểm số.
  const pinned = spans.filter(s => isPinned(s, pins, plan.state));
  const now = maxTurn(spans);
  const activeTask = plan.activeTask ?? null;   // task mà resume block phải tiếp tục

  // 2. Phần còn lại xếp theo utility nhận thức trajectory, cao xuống thấp.
  const rest = spans.filter(s => !isPinned(s, pins, plan.state))
    .map(s => ({ s, u: utility(s, plan, activeLoop, now) }))
    .sort((a, b) => b.u - a.u);

  // 3. Lấp ngân sách từ trên xuống.
  let used = pinned.reduce((n, s) => n + s.tokens, 0) + RESUME_BUDGET;
  const kept = [...pinned];
  for (const { s } of rest) if (used + s.tokens <= budget) { kept.push(s); used += s.tokens; }

  // 4. Gộp retry giống hệt thay vì bỏ hẳn.
  const { kept: collapsed, resumeHints } = collapseRetries(kept);

  // 5. Trích nội dung bền từ những gì sắp đi.
  const dropped = spans.filter(s => !collapsed.some(k => k.id === s.id));
  const writeBack = extractDurable(dropped, goal);

  // 6. Resume block có cấu trúc, dựng từ nội dung bền + trạng thái plan.
  const resume: ResumeBlock = {
    goal,
    decisions: writeBack.decisions.slice(0, 5),
    open: plan.pending(activeTask).map(t => ({ taskId: t.id, title: t.title })),
    repro: activeLoop
      ? { command: activeLoop.command, error: firstLine(activeLoop.error) }
      : { command: plan.reproCommand(activeTask), error: plan.lastError(activeTask) },
    next: plan.nextAction(activeTask),
    invariants: pins.invariants,
    evicted: dropped.map(s => s.id),
  };
  resumeHints.forEach(h => resume.decisions.push(h));   // "retry 6×, last_err: …"

  return {
    kept: collapsed, resume, writeBack,
    dropped: dropped.map(s => s.id),
    ratio: totalTokens(spans) / (used || 1),
  };
}
```

</details>

### 8.3 Bộ Chấm Utility Theo Trajectory

```typescript
export interface ActiveLoop { command: string; error: string; unresolved: boolean }

/** 0.30 recency + 0.40 structural reachability + 0.30 failure signal.
 *  Thành phần giữa là lý do compaction cần plan graph (→ 04/08): nó biết
 *  span nào vẫn đang nuôi một node *đang chờ*. */
export function utility(s: ContextSpan, plan: PlanGraph, loop: ActiveLoop | null, now: number): number {
  const recency = Math.exp(-(now - s.turn) / 12);

  const serves = s.producedFor ?? [];
  const reachable = serves.length === 0 ? 0.4
    : serves.some(t => plan.pendingIds.includes(t))      ? 1.0    // vẫn cần
    : serves.every(t => plan.completedIds.includes(t))    ? 0.1    // nhánh đã xong
    : 0.4;                                                       // song song / chưa biết

  const failure = loop?.unresolved && s.text?.includes(firstLine(loop.error)) ? 1 : 0;

  return 0.30 * recency + 0.40 * reachable + 0.30 * failure;
}

/** N lần gọi thất bại giống hệt → 1 dòng. 18k token → 24. */
export function collapseRetries(spans: ContextSpan[]): { kept: ContextSpan[]; resumeHints: string[] } {
  const groups = new Map<string, ContextSpan[]>();
  for (const s of spans.filter(s => s.kind === "tool_output" || s.kind === "failure")) {
    const key = `${s.tool}:${s.kind}`;
    (groups.get(key) ?? groups.set(key, []).get(key)!).push(s);
  }
  const hints: string[] = [];
  const drop = new Set<string>();
  for (const [, g] of groups) {
    if (g.length < 3) continue;
    const last = g[g.length - 1]!;
    drop.add(last.id);
    for (const s of g.slice(0, -1)) drop.add(s.id);
    hints.push(`retry ${g.length}× (${g[0]!.turn}→${last.turn}): ${firstLine(last.text ?? "")}`);
  }
  return { kept: spans.filter(s => !drop.has(s.id)), resumeHints: hints };
}
```

### 8.4 Builder Cho Resume Block

```typescript
export function buildResume(o: {
  goal: string; decisions: string[]; pending: Task[]; lastCmd: string; lastErr: string;
  invariants: string[]; evicted: string[];
}): ResumeBlock {
  const b: ResumeBlock = {
    goal: o.goal.slice(0, 200),
    decisions: o.decisions.slice(0, 5).map(d => d.slice(0, 200)),
    open: o.pending.map(t => ({ taskId: t.id, title: t.title.slice(0, 80) })),
    repro: { command: o.lastCmd.slice(0, 200), error: firstLine(o.lastErr).slice(0, 200) },
    next: o.pending[0] ? `Tiếp tục với ${o.pending[0].id}: ${o.pending[0].title}` : "Tóm tắt và bàn giao",
    invariants: o.invariants.slice(0, 5),
    evicted: o.evicted,
  };
  const t = countTokens(b);
  if (t > RESUME_BUDGET) {                                  // ngân sách cứng, được ép
    b.decisions = b.decisions.slice(0, 3);
    b.invariants = b.invariants.slice(0, 3);
    b.open = b.open.slice(0, 8);
    b.evicted = b.evicted.slice(0, 40);
  }
  return b;
}

export function renderResume(b: ResumeBlock): string {
  return [
    `Goal: ${b.goal}`,
    `Decisions: ${b.decisions.map(d => `[${d}]`).join("") || "[không có]"}`,
    `Open: ${b.open.map(t => `[${t.taskId}: ${t.title}]`).join("") || "[không có]"}`,
    `Repro: ${b.repro.command} → ${b.repro.error}`,
    `Next: ${b.next}`,
    `Invariants: ${b.invariants.join(" | ")} || "(chưa khai báo)"}`,
    `Evicted: [${b.evicted.join(",")}]`,
  ].join("\n");
}
```

### 8.5 Write-Back Vào Memory

```typescript
/** PHẢI chạy trước khi các span bị loại được bỏ đi. Lỗi ở đây phải huỷ
 *  compaction — một run lặng lẽ mất quyết định tệ hơn một run dừng lại
 *  với một lỗi rõ ràng. */
export async function writeBackAndCompact(
  spans: ContextSpan[], budget: number, memory: MemoryStore, traj: TrajectorySink,
  pins: PinSet, plan: PlanGraph, loop: ActiveLoop | null, goal: string,
): Promise<CompactOutcome> {
  const o = compact(spans, budget, goal, pins, plan, loop);

  const facts = o.writeBack.facts.map(f => ({ ...f, tenantId: pins.tenantId, taskId: plan.activeTask }));
  await memory.persist(facts, { fsync: true });          // bền TRƯỚC khi loại

  await traj.append({                                       // → 13
    kind: "compaction", parentTaskId: plan.activeTask,
    payload: { keptIds: o.kept.map(s => s.id), evictedIds: o.dropped, ratio: o.ratio,
               resumeHash: hash(renderResume(o.resume)), factsWritten: facts.length },
    tokens: { in: totalTokens(spans), out: countTokens(o.resume) },
  });

  return o;
}
```

---

## 9. Kiểm Thử Compaction

### 9.1 Test Bất Biến

```typescript
export function assertInvariants(o: CompactOutcome, budget: number): void {
  const keptIds = new Set(o.kept.map(s => s.id));

  for (const p of PINNED_KINDS)                                            // (1) pin sống
    if (o.dropped.some(id => kindOf(id) === p)) throw new Error(`đã loại span pinned ${p}`);

  if (totalTokens(o.kept) > budget) throw new Error("vượt ngân sách");   // (2) vừa ngân sách
  if (countTokens(o.resume) > RESUME_BUDGET) throw new Error("resume quá lớn");
  if (!resumeIsSufficient(o.resume, o.resume.next)) throw new Error("resume không đủ");
  if (o.resume.evicted.length !== o.dropped.length) throw new Error("lệch danh sách audit");
  if (o.ratio < 1.2) throw new Error(`ratio yếu ${o.ratio.toFixed(2)}`); // (3) có compact thật
  for (const s of o.kept) if (!keptIds.has(s.id)) throw new Error("kept/evicted chồng nhau");
}
```

Chạy các test này cho **mọi** trajectory đã ghi có compaction, trong CI đêm. Trajectory
thật bắt được các trường hợp biên mà dữ liệu tổng hợp không bao giờ bắt.

### 9.2 Contract Test Quan Trọng Nhất

```typescript
/** Nếu memory chết, compaction KHÔNG ĐƯỢC âm thầm tiếp tục. */
it("từ chối loại quyết định chưa lưu", async () => {
  const spans = realTrajectorySpans();                     // 40 message gồm 4 quyết định
  const memory = brokenMemoryStore();                     // persist() luôn ném lỗi
  await expect(writeBackAndCompact(spans, 12_000, memory, sink, pins, plan, null, goal))
    .rejects.toThrow(/memory unavailable/);
  expect(spans.length).toBe(40);                           // không có gì bị loại
});

it("agent lạnh đi tiếp được chỉ từ resume block", async () => {
  const o = await writeBackAndCompact(realTrajectorySpans(), 12_000, mem, sink, pins, plan, loop, goal);
  const cold = await runAgent({ context: [systemPrompt, renderResume(o.resume)], tools });
  const warm = await runAgent({ context: originalSpans, tools });
  expect(await nextActionOf(cold)).toBe(await nextActionOf(warm));   // cùng hành động kế
});
```

Test thứ hai là tiêu chuẩn nghiệm thu thực sự của cả module. Nó cũng là test mà phần
lớn đội bỏ qua, và là test đã bắt được sự cố lượt 47 ở phần đầu tài liệu.

### 9.3 Bộ Hồi Quy Chất Lượng

Theo dõi, mỗi lần compaction, run có còn thành công không. Nếu chất lượng giảm sau
compaction, pin set sai — và đây chính là phép đo tìm ra điều đó:

```sql
SELECT s.kind, AVG(e.payload->>'score') AS score_after_compaction, COUNT(*) AS runs
FROM trajectory c
JOIN trajectory e ON e.session_id = c.session_id AND e.kind = 'eval'
JOIN trajectory s ON s.session_id = c.session_id AND s.kind = 'session_start'
WHERE c.kind = 'compaction'
GROUP BY s.kind ORDER BY score_after_compaction;
```

Một run cụ thể chỉ fail khi có compaction ngay trước thất bại là tín hiệu mạnh nhất
cho thấy pin set đang thiếu thứ gì đó.

---

## 10. Case Study Thực Tế

### 10.1 Claude Code — /compact và Auto-Compact

Coding agent của Anthropic trình bày compaction vừa là **lệnh của người dùng**
(`/compact`) vừa là **trigger tự động** khi mức sử dụng context cao. Ba lựa chọn thiết
kế đáng học:

1. **Đường thủ công và tự động dùng chung một implementation.** Người dùng gặp vấn đề
   bằng tay nhận đúng chất lượng mà đường tự động tạo ra — không có trải nghiệm hạng hai,
   và chỉ một đường code để kiểm thử.
2. **Người dùng nhìn thấy và điều khiển được ngân sách.** Đưa mức sử dụng context ra ngoài
   biến compaction thành một phần nhìn thấy được của workflow thay vì một ẩn thuật tự
   nhiên.
3. **Compaction được trình bày như một checkpoint.** Người dùng hiểu "context đã được
   nén; đây là những gì tôi nhớ" vì nó được diễn đạt như một điểm lưu, không phải một
   thao tác cắt bớt ẩn.

### 10.2 Aider — Repo Map + History Digest

`repo map` của Aider là hình thức thuần khiết nhất của pin set: một chỉ mục gọn, luôn
hiện diện, về cấu trúc repository (đường dẫn file, chữ ký, tên class/hàm) sống sót mọi
lần loại. Mô hình hiếm khi cần toàn bộ thân file để điều hướng — nó cần *biết file tồn
tại và bên trong có gì*.

History digest của nó chính là resume block: một bản tóm tắt có cấu trúc về hướng đi của
cuộc hội thoại, với các bản sửa được giữ *nguyên văn*. Bài học là về **cái gì cần giữ
thô**: diff mới là phần không thể thay thế. Một bản tóm tắt của diff gần như vô dụng,
vì giá trị của một diff nằm ở đúng những byte của nó.

### 10.3 Devin — Quản Lý Context Cho Run Dài

Các coding agent tự trị chạy hàng chục phút liên tục gặp giới hạn context liên tục,
và xử lý nó như một thao tác thường lệ chứ không phải ngoại lệ:

- **Context theo phạm vi task.** Mỗi task trong plan có cửa sổ context riêng; việc hoàn
  thành một task *chính là* một biên compaction. Đây là trigger "biên task" ở §2.2, và
  là biến thể sạch nhất khi plan có các đường nối rõ ràng.
- **Tóm tắt tiến độ thành artifact.** Mỗi task tạo ra một bản tóm tắt được ghi vào hồ
  sơ session, không chỉ giữ trong context. Artifact đó là thứ con người đọc để review
  run, và là thứ một run sau nạp lại nếu nó resume.
- **Output test được giữ có cấu trúc, không tóm tắt.** Tên test fail và assertion được
  giữ chính xác; các stack frame xung quanh bị bỏ.

### 10.4 Letta / MemGPT — Memory Phân Tầng Như Context Ảo

Bài báo MemGPT định khung lại compaction như một **kiến trúc memory** thay vì một thủ
thuật tổng hợp: mô hình có một "bộ nhớ làm việc" nhỏ trong context và một kho lớn bên
ngoài, và nó phát lệnh tool tường minh để load/tháo thông tin. Agent tự quyết định cái
gì cư trú.

Đây là một mô hình mạnh hơn cho cùng một bài toán, và nó làm ranh giới memory↔context
trở nên tường minh thay vì ẩn. Cái giá phải trả: quyết định phân trang do một mô hình
ngẫu nhiên đưa ra, nên bạn vẫn cần pin set xác định bên dưới làm sàn. Mẫu production
hình thành: **phân trang kiểu Letta để chọn *cái gì* cần load, pinning xác định cho
*cái gì tuyệt đối không được mất*.**

### 10.5 Lost in the Middle — Nghiên Cứu Đứng Sau Pinning

Liu et al. (2023) chỉ ra rằng hiệu năng transformer suy giảm mạnh khi thông tin liên
quan nằm ở *giữa* một context dài, trong khi đầu và cuối được chú ý đáng tin cậy. Hai
hệ quả trực tiếp cho thiết kế compaction:

1. **Cấu trúc prompt HEADER/FOOTER** (§7.1) không phải mê tín — nó khai thác hồ sơ
   chú ý đo được.
2. **Pruning nên dồn về phía trước.** Nội dung cũ (rơi vào giữa context sau khi nội
   dung mới được nối vào) là thứ rẻ nhất để bỏ, đó là lý do `recency` chỉ chiếm 30%
   trong hàm utility — các thành phần đồ thị mới là thứ chi phối.

Bài báo cũng giải thích một kết quả thực nghiệm gây bối rối: mô hình thường *làm tệ
hơn* với context đã tóm tắt so với context bị cắt bớt, vì một bản tóm tắt trôi chảy
tạo ấn tượng sai về độ phủ. Vì vậy tiêu chuẩn ở §5.2 là đánh giá block bằng khả năng
tiếp tục từ agent lạnh, không phải bằng cách đọc nó.

---

## 11. TypeScript Interfaces Cho Compaction

```typescript
// ── Context ────────────────────────────────────────────────────────────────
export interface ContextSpan {
  id: string;
  kind: "system" | "goal" | "schema" | "invariant" | "user" | "assistant"
      | "tool_output" | "diff" | "failure" | "approval" | "chitchat" | "branch";
  role: "system" | "user" | "assistant" | "tool";
  turn: number; tokens: number;
  text?: string; path?: string; tool?: string; gateKey?: string;
  producedFor?: string[];      // các task id được phục vụ (plan graph, → 08)
  keep?: boolean;              // pin cứng
}

// ── Policy ─────────────────────────────────────────────────────────────────
export interface CompactionPolicy {
  triggerRatio: number;        // 0.70
  maxTurns: number;            // 20
  resumeBudgetTokens: number;  // 300
  minRatio: number;            // 1.2 — dưới ngưỡng này coi như compaction "hỏng"
  weights: { recency: number; reachability: number; failure: number };
  collapseRetryThreshold: number;  // 3
}
export const DEFAULT_POLICY: CompactionPolicy = {
  triggerRatio: 0.70, maxTurns: 20, resumeBudgetTokens: 300, minRatio: 1.2,
  weights: { recency: 0.30, reachability: 0.40, failure: 0.30 },
  collapseRetryThreshold: 3,
};

// ── Pin set ────────────────────────────────────────────────────────────────
export interface PinSet {
  tenantId: string; system: true; goal: true; schema: true;
  lastUserMessage: true; invariants: string[];
  activeDiffPaths: string[]; pendingApprovals: string[];   // → 15
}

// ── Resume ─────────────────────────────────────────────────────────────────
export interface ResumeBlock {
  goal: string; decisions: string[];
  open: { taskId: string; title: string }[];
  repro: { command: string; error: string };
  next: string; invariants: string[]; evicted: string[];
}

// ── Outcome ────────────────────────────────────────────────────────────────
export interface DurableExtract {
  facts: { key: string; value: string; kind: "decision" | "constraint" | "preference" | "todo" }[];
}
export interface CompactOutcome {
  kept: ContextSpan[]; resume: ResumeBlock; ratio: number;
  dropped: string[]; writeBack: DurableExtract;
}

// ── Compactor ──────────────────────────────────────────────────────────────
export interface Compactor {
  shouldCompact(used: number, budget: number, turns: number): boolean;
  compact(spans: ContextSpan[], budget: number, goal: string, pins: PinSet,
          plan: PlanGraph, loop: ActiveLoop | null): CompactOutcome;
  buildResume(input: ResumeInput): ResumeBlock;
  render(b: ResumeBlock): string;
  /** PHẢI persist trước khi trả về. Lỗi ở đây phải huỷ compaction. */
  writeBackAndCompact(spans: ContextSpan[], budget: number, memory: MemoryStore,
                      traj: TrajectorySink, pins: PinSet, plan: PlanGraph,
                      loop: ActiveLoop | null, goal: string): Promise<CompactOutcome>;
}

// ── Test surface ───────────────────────────────────────────────────────────
export interface CompactionInvariant { name: string; assert(o: CompactOutcome, budget: number): void }
export interface ColdStartTest {
  name: string; spans: ContextSpan[]; budget: number;
  expectSameNextAction: boolean;
}
```

---

## 12. Nguyên Tắc Thiết Kế Cho Compaction

### 12.1 SOLID Cho Quản Lý Context

| Nguyên tắc | Áp dụng |
|------------|---------|
| **S**ingle responsibility | `Compactor` quyết định cái gì đi; `MemoryStore` lưu; `TrajectorySink` ghi. Không cái nào tóm tắt văn xuôi — đó là một dependency `Summarizer`. |
| **O**pen/closed | Chiến lược loại khác là `CompactionPolicy` + bộ chấm mới, không phải viết lại compactor. |
| **L**iskov substitution | Các implementation `MemoryStore` (Postgres, vector DB, file) thay thế được nhau; hợp đồng write-back giống hệt. |
| **I**nterface segregation | Bộ lắp context cần `shouldCompact()`; công cụ debug cần `render()`. Đừng bắt debug tooling phụ thuộc plan graph. |
| **D**ependency inversion | Compaction phụ thuộc `PlanGraph` như một interface, nên một đồ thị tổng hợp chạy được trong unit test mà không cần planner. |

### 12.2 Sáu Nguyên Tắc Thiết Kế

1. **Prune trước, tóm tắt sau.** Bỏ nhánh chết là miễn phí và không mất thông tin; tóm tắt là tốn kém và có hao hụt. Làm sai thứ tự tốn tiền và thông tin.
2. **Pin bằng suy ra, không bằng tay.** Pin set tính từ plan, loop đang hoạt động, và danh sách gate chờ — nên nó co lại khi công việc xong thay vì phình ra cho tới khi vỡ ngân sách.
3. **Ngân sách là trần cứng.** 300 token cho resume block, 70% để trigger. Cả hai được ép trong code, cả hai được assert trong test.
4. **Persist trước khi loại, hoặc đừng loại.** Compaction không write-back được thì huỷ. Một run lặng lẽ mất quyết định tệ hơn một run dừng lại với lỗi.
5. **Policy xác định.** Trigger, pin, và thứ tự loại đều tính từ trạng thái đo được. Mô hình không bao giờ quyết định nó quên gì.
6. **Hợp đồng là với một agent lạnh.** Chỉ nhận một resume block khi một agent mới với context rỗng hành động đúng bước kế tiếp từ nó.

---

## 13. Best Practices

### 13.1 NÊN ✅

- Trigger ở 70% sử dụng hoặc 20 lượt, cái nào tới trước; chừa 30% headroom cho tool result kế tiếp.
- Pin system, goal, invariant, diff đang hoạt động, chỉ dẫn user cuối, và lỗi của loop chưa giải quyết.
- Để pin của loop đã giải quyết trở thành evictable; pin set không tăng đơn điệu.
- Xếp hạng loại theo reachability trên plan graph, không theo tuổi.
- Gộp 3+ lần retry giống hệt thành một dòng, giữ nguyên văn lỗi cuối.
- Giới hạn resume block 300 token với key cố định, và assert trong CI.
- Persist quyết định, việc còn mở, invariant vào memory với `fsync` **trước khi** loại.
- Phát event `compaction` với `keptIds`, `evictedIds`, `ratio` (→ 13).
- Test bằng agent lạnh: cùng hành động kế tiếp từ resume block như từ context đầy đủ.

### 13.2 KHÔNG NÊN ❌

- ❌ Không trigger ở 90% rồi hy vọng kết quả kế tiếp vừa. Nó sẽ không vừa, và bạn compact dưới áp lực — lúc tệ nhất để chịu hao hụt.
- ❌ Không dùng loại FIFO/oldest-first. Nó giữ `ls` của hôm qua và bỏ định nghĩa nhiệm vụ.
- ❌ Không để mô hình quyết định khi nào compact.
- ❌ Không tóm tắt toàn bộ transcript khi phần lớn nó là nhánh chết.
- ❌ Không diễn giải lại các giá trị được pin (số, ID, ràng buộc phủ định). Diễn giải là nơi độ chính xác chết.
- ❌ Không để pin set tăng đơn điệu. Pin của loop đã giải quyết phải thành evictable.
- ❌ Không write-back vào memory "để sau". Sau là khi quyết định đã mất rồi.
- ❌ Không coi một bản tóm tắt trôi chảy là bằng chứng về độ phủ. Hãy test bằng khả năng tiếp tục từ agent lạnh.
- ❌ Không compact giữa một task khi plan có đường nối tự nhiên — hãy compact tại đường nối.

---

## 14. Anti-Patterns & Cách Khắc Phục

| Anti-pattern | Triệu chứng | Cách sửa |
|--------------|------------|---------|
| **Cắt bừa** | Agent đọc lại file đã edit, huỷ chính công sức của nó | Pin set + resume block |
| **Loại FIFO** | Mất đặc tả nhiệm vụ, giữ lại output `ls` | Xếp hạng utility theo plan graph |
| **Tóm tắt đồng đều** | Stack trace còn, phát biểu mục tiêu mất | Pin goal; chỉ tóm tắt output chết quá lớn |
| **Compaction ở 95%** | Tổng hợp chạy dưới áp lực và mất chi tiết | Trigger ở 70% |
| **Write-back thất bại lặng lẽ** | Quyết định không lưu; run "thành công" một cách lệch | Huỷ compaction khi persist lỗi |
| **Mô hình tự quyết compaction** | Mô hình trả lời "không" ở 195k token | Policy xác định từ số token đo được |
| **Resume block không trần** | Resume phình thành 2k token, compaction thành vấn đề mới | Trần cứng 300 token có cắt bớt |
| **Pin set đơn điệu** | Pin vượt ngân sách; mọi thứ suy giảm lặng lẽ | Suy ra pin; pin của loop đã xong phải hết hạn |
| **Diễn giải invariant** | "Khoảng 30 giây" thay vì `timeoutMs: 30000` | Pin giá trị thô; văn xuôi đi quanh nó |
| **Không audit compaction** | Chất lượng giảm sau compaction; không ai biết vì sao | Phát event; theo dõi eval sau compaction |
| **Không test khởi động lạnh** | Block đọc rất hay và vô dụng | Test tiếp tục bằng agent lạnh trong CI |

---

## 15. Production Checklist

- [ ] **Trigger** — 70% sử dụng HOẶC 20 lượt; xác định, tính từ token đo được
- [ ] **Headroom** — chừa 30%; một tool result lớn không thể gây dây chuyền compact
- [ ] **Pin set** — system, goal, schema, invariant, diff đang hoạt động, chỉ dẫn user cuối, lỗi loop chưa giải quyết, approval đang chờ
- [ ] **Hết hạn pin** — pin của loop đã xong trở thành evictable; pin set không tăng đơn điệu
- [ ] **Thứ tự loại** — reachability trên plan graph có trọng số ≥ recency; không FIFO
- [ ] **Gộp retry** — 3+ lời gọi giống hệt gộp thành một dòng, giữ nguyên văn lỗi cuối
- [ ] **Resume block** — key cố định, ≤300 token, assert trong CI, `evicted[]` để audit
- [ ] **Write-back** — fact được persist với `fsync` trước khi loại; lỗi thì huỷ compaction
- [ ] **Audit** — event `compaction` với `keptIds`, `evictedIds`, `ratio`, `resumeHash` (→ 13)
- [ ] **Giám sát ratio** — cảnh báo khi ratio < 1,5 với context lớn
- [ ] **Cấu trúc prompt** — invariant HEADER/FOOTER; giá trị thô được pin, không diễn giải
- [ ] **Kiểm thử** — bất biến cho mọi compaction đã ghi; test agent lạnh; test memory chết
- [ ] **Theo dõi chất lượng** — eval score sau compaction được so với run không compact

---

## 16. Xu Hướng Tương Lai

### 16.1 Compaction Nhận Thức Cấu Trúc (2026-2028)

- **Tóm tắt plan, không tóm tắt transcript.** Nếu plan graph (→ 04) cộng resume block đã đủ để quyết định hành động kế tiếp, transcript là thừa — một mục tiêu compaction nhỏ hơn nhiều và đáng tin hơn.
- **Policy loại được học.** Huấn luyện hàm utility trên dữ liệu span nào thực sự đi trước kết quả thành công so với thất bại, thay vì tự đặt tay trọng số ba thành phần.
- **Prefetch trong lúc tóm tắt.** Chính lời gọi summarizer đã biết bước kế cần gì; hãy để nó phát ra một `prefetch` kèm resume block, để lượt sau bắt đầu với context đúng đã sẵn sàng.

### 16.2 Compaction Có Thể Kiểm Chứng

Compaction xấu xa theo bản chất, và hôm nay không gì chứng minh được thứ được giữ lại
là quan trọng. Hai hướng: **đo độ phủ** (tỉ lệ fact *liên quan tới goal* còn sống, đo
trên bộ eval), và **danh sách loại có thể audit** (`evicted[]` đã tồn tại; bước tiếp
theo là làm nó truy vấn được, để "chúng ta đánh mất gì" là một câu hỏi một query
trước khi nó thành incident).

### 16.3 Compaction Như Một Loại Step Chính Thức

Khi một plan chứa các node `compact` tường minh — tại đường nối task, trước thao tác
rủi ro, trước khi chuyển context cho một sub-agent (→ 09 §16.2) — compaction thôi là
một phản ứng khẩn cấp với ngưỡng và trở thành một phần được thiết kế của quá trình thực
thi. Đó là khác biệt giữa một agent sống sót được các run dài và một agent chỉ đơn
giản là may mắn.

### 16.4 Vượt Qua Giới Hạn Của Tổng Hợp

- **Đưa trạng thái ra ngoài.** Chuyển trạng thái lớn (test fixture, thân file) sang một kho và chỉ giữ handle trong context. Dạng mạnh nhất của compaction không phải tóm tắt dữ liệu — mà là không bao giờ đặt nó vào đó.
- **Cư trú phân tầng kiểu MemGPT**, với pin set xác định làm sàn bên dưới các quyết định phân trang của mô hình.

---

## Tài Liệu Tham Khảo

### Papers & Research

- **Lost in the Middle: How Language Models Use Long Contexts** — Liu et al., 2023 · https://arxiv.org/abs/2307.03172
- **MemGPT: Towards LLMs as Operating Systems** — Packer et al., 2023 · https://arxiv.org/abs/2310.08560
- **LongLoRA: Efficient Fine-tuning of Long-Context Large Language Models** · https://arxiv.org/abs/2309.12307
- **StreamingLLM: Efficient Streaming Language Models with Attention Sinks** — Xiao et al., 2023 · https://arxiv.org/abs/2309.17453
- **SWE-agent: Agent-Computer Interfaces for Automated Software Engineering** · https://arxiv.org/abs/2405.15793
- **A Survey on LLM-based Software Engineering Agents** · https://arxiv.org/abs/2402.06530

### Frameworks & Tools

1. **Anthropic Claude Code** — https://docs.anthropic.com/en/docs/claude-code — `/compact` và auto-compact
2. **Aider** — https://aider.chat/docs/ — repo map + history digest
3. **Letta (MemGPT)** — https://docs.letta.com/ — memory phân tầng
4. **LangGraph** — https://langchain-ai.github.io/langgraph/ — mẫu node summarization
5. **tiktoken** — https://github.com/openai/tiktoken — đếm token chính xác cho trigger
6. **LiteLLM** — https://docs.litellm.ai/ — đếm token cho từng lời gọi

### Production Systems

- **Claude Code** — https://claude.com/product/claude-code — compaction thủ công + tự động, ngân sách nhìn thấy được
- **Aider** — https://aider.chat — repository map làm pin set thường trực
- **Letta** — https://letta.com — memory như context ảo
- **Devin** — https://devin.ai — context theo phạm vi task

### Module Liên Quan

- `02-build-context/README.md` §16 — phía tạm của contract (assembly, marking, fan-out)
- `03-update-memory-store/README.md` §12 — phía bền (đích write-back, GDPR, retrieval)
- `04-plan-decompose-task/README.md` — plan graph làm chấm reachability khả thi
- `05-prompt-builder/README.md` §17.5 — cấu trúc invariant HEADER/FOOTER
- `07-workflow/README.md` §13.4 — compaction như một loại step chính thức của engine
- `09-multi-agent/README.md` §16.2 — compaction trước khi chuyển context cho sub-agent
- `10-automation/README.md` §17.3 — loop budget, mà compaction giữ cho phải chăng
- `13-trajectory-observability/README.md` — event `compaction` và dấu vết audit của nó
- `15-approval-gates/README.md` — approval đang chờ là một phần của pin set

---

*Tài liệu: Harness 14. Context Compaction — HARNESS ENGINEERING EDITION*
*Module cross-cutting · thứ cho phép một context window cố định gánh một run không giới hạn*
*Cập nhật: 19/07/2026*
*Tác giả: AI Knowledge Repository*
