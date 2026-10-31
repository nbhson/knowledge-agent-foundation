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

> Phần này kể một tình huống thật để bạn thấy compaction (nén ngữ cảnh = rút gọn
> nội dung trong "bộ nhớ tạm" của agent) giải quyết vấn đề gì, và vì sao làm ẩu
> thì nguy hiểm hơn không làm.

Tới lượt thứ 47. "Lượt" (turn) = một vòng agent gọi tool rồi nhận kết quả. Agent đang giữa một cuộc refactor (viết lại code mà không đổi hành vi): 31 tool call, bốn file đã viết lại, hai bộ test đã chạy. Đâu đó giữa chừng còn một stack trace (bảng lỗi in ra kèm các dòng code gây lỗi) gây rối. Context window (cửa sổ ngữ cảnh = giới hạn số token — đơn vị chữ — mà model đọc được trong một lượt) lúc này đã 96%. Tool result kế tiếp dài 4.000 token mà chỗ trống thì không còn.

Lúc này cả đội chỉ còn ba lựa chọn, mà lựa chọn nào cũng dở:

1. **Để nó chết.** Run (một phiên agent chạy từ đầu tới cuối) chết ở lượt 47 với lỗi
   "vượt độ dài context". Người dùng thấy "có gì đó sai" sau 20 phút.
2. **Cắt bừa.** Bỏ các message cũ nhất. Agent mất đặc tả nhiệm vụ được giao ở lượt 1 —
   "đặc tả nhiệm vụ" = bản mô tả phải làm gì, chuẩn xong ra sao. Nó đọc lại một file đã
   đọc ở lượt 12 (vì *kết quả* đã mất nhưng *bản sửa* vẫn còn), và tự tin sinh ra một
   patch (mảnh vá code) huỷ chính công sức của nó ở lượt 30.
3. **Tóm tắt mọi thứ như nhau.** Nén toàn bộ transcript (biên bản toàn bộ hội thoại)
   thành một đoạn. Đoạn đó nhắc stack trace và bỏ mất định nghĩa nhiệm vụ, nên agent
   giải quyết nhầm vấn đề một cách trôi chảy.

**Không cái nào trong ba cách trên là "compaction" cả.** Compaction đúng nghĩa giống như dọn vali có nguyên tắc: một điều kiện kích hoạt rõ ràng, một pin set gồm những thứ "cấm đụng vào" (pin set = danh sách các mục được "ghim" lại, không bao giờ bị loại), một hàm utility quyết định cái gì đi tiếp (utility = điểm số đo độ hữu ích), và một resume block dựng lại trạng thái run theo cấu trúc cố định (resume block = bản tóm tắt có khuôn mẫu để agent "tỉnh dậy" tiếp tục việc). Làm đúng bốn thứ đó thì lượt 47 chỉ là chuyện nhỏ. Làm ẩu thì lỗi cực kỳ *khó thấy* — run vẫn *chạy xong*, chỉ là xong... sai nhiệm vụ.

> **Tóm gọn 1 câu:** Khi context gần đầy, agent có ba cách chết hỏng tệ (chết hẳn, cắt bừa, tóm tắt bừa) — compaction đúng nghĩa là dọn dẹp có nguyên tắc: có điều kiện kích hoạt, có danh sách "ghim" không được mất, có điểm ưu tiên, và có bản tóm tắt có khuôn mẫu để tiếp tục.

### Vì Sao Compaction Là Bắt Buộc?

> *"Bất kỳ agent nào không sống sót được chính context window của nó là một demo,
> không phải một sản phẩm."*

#### Phép tính

> Cách đọc bảng này: cột "Ngân sách" là giới hạn context của model (số token tối đa
> model đọc được); "Input mỗi lượt" là số token trung bình gửi đi mỗi lượt; "Số lượt
> trước khi cạn" là ngân sách chia cho input — tức agent chạy được bao nhiêu lượt rồi
> chết. Ví dụ: 200k ÷ 6k ≈ 33 lượt.

| Ngân sách | Input mỗi lượt | Số lượt trước khi cạn | Với trigger 70% + compaction |
|-----------|-----------------|------------------------|-------------------------------|
| 200k (lớn) | ~6k | ~33 | không giới hạn |
| 128k (điển hình) | ~4k | ~32 | không giới hạn |
| 32k (nhỏ/local) | ~2k | ~16 | không giới hạn |

**Chữ "không giới hạn" chính là điểm ăn tiền.** "Trigger 70%" = khi context đầy 70% thì
tự động nén lại, chừa 30% trống. Compaction không phải món tối ưu cho vui; nó là cơ chế biến một context cố định thành một run dài vô tận. Nó cũng là thứ giúp checkpoint-resume của `07-workflow` chạy được (→ 07 §13; checkpoint-resume = lưu lại điểm dừng để chạy tiếp sau đó), giúp việc giao nốt cho sub-agent ở `09-multi-agent` thành hiện thực (→ 09 §16.2; sub-agent = agent con được agent chính thuê làm việc phụ), và giúp loop budget của `10-automation` siết được (→ 10 §17.3; loop budget = trần số vòng lặp) — vì món nào cũng cần một run sống lâu hơn một context window.

#### Hiệu ứng bậc hai

> "Hiệu ứng bậc hai" = những lợi ích/rủi ro ngoài mục đích chính (chống chết vì trần
> context). Ba mục dưới đây là ba mặt: tiền, chất lượng, và khả năng truy vết lỗi.

- **Chi phí.** Compaction giảm mạnh input token mỗi lượt trên run dài, vì một resume block 60 KB thay cho 180 KB lịch sử. Các đội thường thấy giảm 40–70% chi phí trên các run quá 30 lượt.
- **Chất lượng.** Compaction *có thể* làm giảm chất lượng — đó là điều §5–7 nói tới. Làm cẩu thả thì nó tệ hơn hẳn việc không compaction, vì mô hình sẽ tự tin suy luận trên một bản tóm tắt bị hao hụt (nghĩa là tóm tắt thiếu chi tiết nhưng trông vẫn có vẻ đầy đủ).
- **Khả năng audit.** Compaction sinh ra một event `compaction` (→ 13; event = bản ghi sự kiện) ghi lại chính xác điều gì được giữ, điều gì bị loại. Một harness mà bạn không dựng lại được mô hình đã mất gì là một harness bạn không debug được (harness = khung chương trình điều phối agent).

> **Tóm gọn 1 câu:** Compaction biến context giới hạn thành run chạy vô hạn, giảm 40–70% chi phí, nhưng làm ẩu thì giết chất lượng — nên mọi lần nén phải được ghi log để kiểm tra lại được.

## Overview

> **📌 Khái Niệm Cốt Lõi**
>
> - **Khái niệm:** Compaction là **tổng hợp có trigger**: khi context vượt ngưỡng, các span giá trị thấp được thay bằng một resume block có cấu trúc thay vì đâm vào trần token. **Pruning** là người bạn đồng hành — quyết định *cái gì* đi trước theo utility, không theo recency.
> - **So sánh:** Như xếp vali nhỏ cho chuyến đi dài. Vali tràn thì không quăng bừa; bạn có quy tắc (đồ vệ sinh ở lại, hoá đơn cũ đi) và để lại danh sách những gì đã bỏ.
> - **Vì sao quan trọng:** Mọi run agent dài đều chết nếu không compaction: tràn context, sụp chất lượng kiểu lost-in-the-middle, và hoá đơn token gấp 3–5× vì gửi lại tool output chết. Compaction ở 70% giữ run sống vô hạn với chi phí phẳng.

**Context Compaction** là thứ giúp một context window bé xíu "gánh" được một run dài bất tận. Đây cũng là phần hay bị làm qua loa nhất trong các agent harness, và hễ làm ẩu là trả giá đắt nhất.

> Đọc sơ đồ dưới đây: khung trên là context *trước* khi nén — gần đầy 188k/200k token,
> mọi thứ ngoài system + goal đều bị coi là "có thể bỏ" (evictable). Khung dưới là
> *sau* khi nén: các mục quan trọng được ghim (PIN), phần còn lại đúc thành một
> RESUME BLOCK nhỏ 280 token, và 3 lượt gần nhất giữ nguyên văn để agent đỡ "mất nhịp".

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

> Cách đọc bảng này: mỗi dòng là một mảnh bắt buộc của compaction. Cột "Hỏng thế nào
> nếu thiếu" mô tả hậu quả khi bỏ đúng mảnh đó. Ví dụ: thiếu hàng 2 (pin set) → bản
> tóm tắt loại mất định nghĩa nhiệm vụ → agent làm sai bài mà vẫn tưởng mình đúng.

| # | Thành phần | Hỏng thế nào nếu thiếu |
|---|-----------|------------------------|
| 1 | **Trigger** | Run chết ở trần |
| 2 | **Pin set** | Định nghĩa nhiệm vụ bị loại; agent giải sai bài |
| 3 | **Xếp hạng utility** | FIFO loại mất goal, giữ lại `ls` của hôm qua |
| 4 | **Resume block** | Agent tỉnh dậy không có trạng thái, đọc lại mọi thứ, hoá đơn gấp ba |
| 5 | **Write-back memory** *(thường bị bỏ sót)* | Quyết định biến mất cùng span bị loại và không bao giờ được lưu |

Glossary cho bảng: "FIFO" = First In First Out, loại cái cũ nhất trước; "`ls`" = lệnh
liệt kê file, output rất rẻ tiền và có thể chạy lại; "span" = một mảnh nội dung trong
context (một message, một tool result); "write-back memory" = lưu thông tin quan trọng
vào kho nhớ dài hạn trước khi nó bị xoá khỏi context.

> **Tóm gọn 1 câu:** Compaction = trigger nén ở ngưỡng + ghim các thứ cốt lõi + xếp hạng loại theo độ hữu ích + bản tóm tắt có khuôn mẫu + lưu hết vào memory dài hạn; thiếu mảnh nào là hỏng mảnh đó.

## Mục Lục Chi Tiết

> Cách đọc bảng này: cột "#" là số thứ tự mục, "Chủ đề" là tên (kèm link — bấm để
> nhảy tới), "Mô tả" là nội dung chính của mục đó trong một dòng. Ví dụ: mục 2 giải
> thích compaction nên chạy lúc nào và vì sao chọn ngưỡng 70%.

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

> **Tóm gọn 1 câu:** Bảng trên là bản đồ 16 mục của tài liệu — từ định nghĩa, cách
> kích hoạt, đến hiện thực, kiểm thử và các case study sản phẩm thật.

---

## 1. Định Nghĩa & Thuật Ngữ

> Phần này định nghĩa các từ chuyên dụng sẽ dùng xuyên suốt tài liệu, và tách compaction thành hai họ kỹ thuật (tóm tắt vs cắt bỏ). Đọc phần này trước thì các phần sau đỡ phải giải thích lại.

### 1.1 Các thuật ngữ cốt lõi

> Cách đọc bảng này: cột "Thuật ngữ" là tên gọi; "Định nghĩa" là nghĩa ngắn; "Hỏng
> khi…" là tình huống cho thấy bạn đang làm sai thuật ngữ đó. Ví dụ: "Compaction
> ratio" là tỉ lệ token trước ÷ sau; nếu nhỏ hơn 1,5 trên context lớn thì bản tóm
> tắt đang nén yếu (thường do summarizer — bộ tóm tắt — đang hoạt động kém).

| Thuật ngữ | Định nghĩa | Hỏng khi… |
|-----------|-----------|-----------|
| **Auto-compaction** | Tổng hợp có trigger khi `used > ngưỡng`; span evictable được thay bằng resume summary | thiếu trigger → run chết |
| **Resume block** | Struct ≤300 token: `Goal / Decisions / Open / Repro / Next` + `evicted_span_ids` | không ràng buộc → phình thành vấn đề mới |
| **Trajectory-aware pruning** | Thứ tự loại suy ra từ execution graph (giữ critical path, bỏ nhánh chết) | chỉ recency → mất goal |
| **Compaction ratio** | `tokens_before ÷ tokens_after` — chỉ số sức khoẻ | <1,5 với context lớn → summarizer đang hỏng |
| **Pin set** | Lõi không evictable: system, goal, ràng buộc, diff đang mở, lỗi cuối | vắng mặt → đặc tả nhiệm vụ bị loại |
| **Write-back** | Lưu resume + quyết định + việc còn mở vào memory **trước khi** chúng rời context | bỏ qua → quyết định mất vĩnh viễn |
| **Lost in the middle** | Độ chính xác giảm khi thông tin quan trọng nằm giữa context | bỏ qua → pinning trở nên tuỳ ý |

Glossary nhanh cho các từ trong bảng: **evictable** = "có thể bị đuổi" tức được phép
xóa khi cần chỗ; **struct** = dữ liệu có khuôn cố định các trường; **execution graph**
= đồ thị "cái gì làm trước, cái gì làm sau" của run; **critical path** = chuỗi bước
bắt buộc phải xong thì nhiệm vụ mới xong; **ràng buộc (constraint)** = điều kiện cấm,
ví dụ "không thêm thư viện mới"; **diff** = bảng so sánh code cũ/sau sửa.

> **Tóm gọn 1 câu:** Bảy thuật ngữ trên là từ vựng của cả module — nắm chắc "pin set" (ghim lại), "evictable" (được phép bỏ) và "write-back" (lưu trước khi bỏ) là đi được 80% đường.

### 1.2 Hai Họ Kỹ Thuật: Summarization và Pruning

> Phần này nói rõ hai cách rút gọn context khác nhau ra sao, và vì sao bạn cần cả hai
> chứ không chọn một. **Summarization** = nén một mảnh thành bản tóm tắt ngắn hơn;
> **pruning** = xoá hẳn mảnh đó đi.

Hai cách này bổ trợ cho nhau, chứ không phải hai món để bạn chọn một trong hai — và nhầm lẫn chỗ này chính là gốc rễ của hầu hết bản hiện thực dở tệ.

| | **Summarization** | **Pruning** |
|---|------------------|------------|
| **Làm gì** | Nén một span thành văn xuôi | Bỏ hẳn một span |
| **Khi nào** | Span cần dùng nhưng quá lớn | Span không cần dùng |
| **Bằng cách nào** | Mô hình tóm tắt, hoặc template xác định | Chấm utility + loại |
| **Chi phí** | Lời gọi LLM (~1–3 s) hoặc template | miễn phí |
| **Rủi ro** | Mất chi tiết, tóm tắt bịa | Mất thông tin trông như không cần |
| **Áp cho** | Tool output cũ, file đọc dài | Nhánh thất bại, diff bị thay thế, chit-chat |

Chú giải bảng: hàng "Chi phí" — lời gọi LLM nghĩa là phải gửi thêm một request tới
model để tóm tắt, tốn vài giây và tiền token; hàng "Rủi ro" — "tóm tắt bịa" nghĩa là
model có thể sáng tạo ra chi tiết không có thật; hàng "Áp cho" — "nhánh thất bại" là
một hướng đi agent đã thử và bỏ.

**Nhớ thứ tự vàng:** prune trước cho gọn (miễn phí, lại không mất thông tin của nhánh chết), rồi mới tóm tắt phần còn lại quá lớn (tốn tiền gọi LLM, lại hao hụt). Đội nào làm ngược — tóm tắt trước rồi mới prune — thì vừa mất oan gần 40% chi phí, vừa giữ lại ít thông tin hơn.

> **Tóm gọn 1 câu:** Prune (xoá hẳn thứ vô dụng) làm trước vì miễn phí; summarize (nén có mất mát) làm sau cho phần còn lại quá lớn — đảo thứ tự là vừa tốn tiền vừa mất thông tin.

---

## 2. Policy Trigger

> Phần này trả lời câu hỏi "nén vào lúc nào?" — chọn ngưỡng nào, theo cách nào. Chọn sai lúc nén là mất thông tin nhiều nhất.

### 2.1 Vì Sao 70% Chứ Không Phải 90%

> Sơ đồ dưới đây là thang đo mức đầy của context (0–100% ngân sách token). Mỗi mốc
> kèm nhận xét: nên hay không nên nén tại đó.

```
100% ──── trần cứng: chính request thất bại. Không phục hồi được, không log được.
 90% ──── "gần đủ" — nhưng tool result kế tiếp thường vượt 10% ngân sách.
 70% ──── chừa 30% headroom: 2-3 lượt tool result kế tiếp vừa mà không phải compact lại.
 50% ──── hăng hái quá: 2 lần compaction mỗi run, tốn chất lượng, tốn lời gọi LLM.
```

Lỗi ở mốc 90% rất cụ thể mà đội nào cũng từng dính: một cú `read_file` 30 KB ngốn hết 8% cửa sổ 200k chỉ trong *một* step. Trigger ở 90%, nhận thêm một kết quả 8%, giờ bạn đã ở 98% — và kết quả *kế tiếp* tràn, buộc phải compact ngay giữa chừng task, trong lúc chẳng còn mấy chỗ để tóm tắt cho ra hồn. Compaction mà làm trong lúc bị dí deadline thì đúng là lúc dễ mất thông tin nhất.

**Quy tắc: trigger khi bạn vẫn còn đủ khả năng tóm tắt cho tử tế.**

> **Tóm gọn 1 câu:** Nén ở 70% (chứ không phải 90%) vì cần chừa 30% đất cho vài kết quả tool to tới bất ngờ — nén lúc gần tràn là lúc dễ mất thông tin nhất.

### 2.2 Các Chiến Lược Trigger

> Cách đọc bảng này: mỗi dòng là một cách quyết định "giờ nén chưa?". Cột "Quy tắc"
> là điều kiện trong code; cột "Dùng khi" là trường hợp nên chọn. Ví dụ: chiến lược
> "Ngưỡng" nghĩa là cứ khi context dùng quá 70% ngân sách thì nén — đơn giản nhất,
> phù hợp làm mặc định.

| Chiến lược | Quy tắc | Dùng khi |
|------------|---------|----------|
| **Ngưỡng** | `used / budget > 0.70` | mặc định, đơn giản, dự đoán được |
| **Số lượt** | `turns > 20` | ước tính token không đáng tin; chốt chặn rẻ |
| **Tốc độ tăng** | compact khi `used` tăng >25% trong 3 lượt | phát hiện vòng lặp tool |
| **Biên task** | compact giữa các task, không ở giữa một task | session nhiều task; giữ nguyên suy luận của một task |
| **Kích thước bước kế** | compact khi `est(next_result) > headroom` | ngân sách chật (32k) |

Chú giải: "Số lượt" = đếm số lượt chạy, quá 20 thì nén — dùng khi không đo token được;
"Tốc độ tăng" = context phình quá nhanh thường là agent bị kẹt lặp một tool; "Biên
task" = nén ngay lúc vừa xong việc này chuẩn bị sang việc khác; "Kích thước bước kế" =
ước lượng kết quả tool kế tiếp to hơn chỗ trống thì nén trước.

Khuyến nghị production: **ngưỡng HOẶC số lượt**, cái nào tới trước, cộng thêm
compaction tại biên task khi plan (→ 08) có đường nối tự nhiên. Tốc độ tăng là một
cảnh báo hữu ích cho "run này đang lặp" (→ 10 §17.3).

**Không bao giờ để mô hình quyết định.** Compaction là policy của harness, tính từ
số token đo được. Một mô hình được hỏi "có nên compact không?" sẽ trả lời "không,
tôi ổn" khi đang giữ 195k token.

> **Tóm gọn 1 câu:** Chọn trigger theo ngưỡng 70% hoặc số lượt 20 (cái nào tới trước), nén tại biên task khi được — và tuyệt đối đừng hỏi model xem có nên nén không, nó sẽ nói "tôi ổn".

---

## 3. Pin Set — Thứ Gì Phải Sống Sót

> Phần này trả lời câu hỏi "cái gì thì cấm bỏ dù context có đầy tới cổ?" — đó chính là pin set.

### 3.1 Pinned và Evictable

Pin set trả lời đúng một câu hỏi: "mất nó thì run có làm sai không?". Hễ mất mà làm đổi cả *nhiệm vụ* chứ không chỉ đổi *khẩu vị* — thì pin lại, khỏi bàn.

> Cách đọc bảng này: cột trái là các mục được **ghim** (pinned = không bao giờ bị xoá
> khỏi context); cột phải là các mục **được phép bỏ** (evictable) và nằm trong thứ tự
> ưu tiên xoá. Ví dụ: system prompt luôn được ghim; còn output lệnh `ls` cũ hơn 3 lượt
> thì bỏ được — muốn xem lại cứ chạy lại lệnh đó.

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

Chú giải từng mục khó: "Task spec + definition of done" = bản mô tả việc và tiêu chí
xong việc; "retrieved chunk có score <0,3" = đoạn văn tự tìm được từ kho nhớ nhưng
điểm liên quan thấp; "invariant" = luật bất biến của nhiệm vụ, ví dụ "không đổi API
công khai"; "approval đang chờ" = lần người dùng cho phép đang đợi duyệt (→ 15);
"schema output" = khuôn mẫu dữ liệu model phải trả ra; "con trỏ tới memory bền" =
tham chiếu tới chỗ dữ liệu dài hạn được lưu (chỉ giữ địa chỉ, không giữ nguyên dữ
liệu); "tool stdout" = dòng chữ tool in ra.

**Mẹo nhỏ mà hay bị quên:** "tín hiệu lỗi cuối" chỉ được pin *khi loop còn đang chạy*. Loop xong rồi thì lỗi đó thành evictable. Cứ pin mãi thì pin set của bạn sẽ phình to dần cho tới lúc vượt ngân sách — một kiểu hỏng khác, mà lại hỏng trong im lặng.

> **Tóm gọn 1 câu:** Ghim lại mọi thứ mà mất đi là agent làm sai nhiệm vụ (goal, ràng buộc, diff đang sửa, lỗi đang xử lý) và cứ để phần còn lại vào hàng chờ bị xoá — nhưng ghim xong việc rồi thì phải "bỏ ghim" để pin set không phình vô tận.

### 3.2 Pin Set

> Phần này nói cách hiện thực pin set trong code: suy ra tự động hay gõ tay?

> 📄 **Code ví dụ:** [`examples/01-3-2-pin-set.ts`](examples/01-3-2-pin-set.ts)

**Quy tắc gọn nhẹ: pin set là thứ suy ra tự động, đừng gõ tay.** Nó tính từ plan, loop đang chạy và danh sách gate đang chờ — nên công việc xong tới đâu là nó tự co lại tới đó, thay vì phình ra mãi.

> **Tóm gọn 1 câu:** Đừng viết danh sách ghim tay — hãy để code tự suy ra từ kế hoạch, vòng lặp đang chạy và các phê duyệt đang chờ, thì nó sẽ tự co lại khi việc xong.

---

## 4. Pruning Theo Utility

> Phần này trả lời "nếu phải bỏ thì bỏ trước cái nào?" — câu trả lời là bỏ theo điểm
> hữu ích (utility), không phải bỏ theo tuổi (cũ nhất đi trước).

### 4.1 Vì Sao Chỉ Recency Là Không Đủ

"Chỉ recency" = chỉ xét độ mới: cái cũ nhất thì loại trước (còn gọi là FIFO). Giả định
này cho rằng giá trị suy giảm theo tuổi. Trong trajectory agent (chuỗi các bước agent
đã đi), điều đó không đúng:

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
đây. Agent sau đó tự suy ra một dependency vi phạm ràng buộc đang có hiệu lực (nghĩa
là nó tự "bịa" một thư viện không được phép dùng, vì không còn thấy dòng cấm).

### 4.2 Chấm Utility Nhận Thức Trajectory

> Phần này đưa ra công thức tính điểm hữu ích cho từng mảnh context, để xếp thứ tự xoá.

```
utility = 0.30·recency + 0.40·structural_reachability + 0.30·failure_signal
```

> Cách đọc bảng này: mỗi dòng là một thành phần của công thức trên, chiếm đúng tỉ lệ
> trọng số ghi trong công thức (30% + 40% + 30% = 100%). Ví dụ: "recency" chiếm 30%
> và tính bằng công thức `exp(-turns_old / 12)` — tức mảnh càng cũ (turns_old càng
> lớn) thì điểm này càng giảm về 0.

| Thành phần | Ý nghĩa | Cách tính |
|------------|---------|----------|
| `recency` | Tuổi chuẩn hoá: `exp(-turns_old / 12)` | rẻ, chặn cũ hoá vô hạn |
| `structural_reachability` | Span này có nằm trên critical path tới goal hiện tại không? | BFS trên plan graph (→ 04) từ task đang hoạt động; span nuôi một node *đang chờ* điểm cao, span nuôi node *đã xong* điểm thấp |
| `failure_signal` | Span có mang lỗi mà loop đang săn không? | so khớp chuỗi/trace với lỗi cuối của loop (xem §8.3) |

Chú giải: "BFS" = duyệt đồ thị từng lớp (breadth-first search) — ở đây nghĩa là đi từ
task đang làm, lần theo các bước nó phụ thuộc; "span nuôi một node" = mảnh context đó
là đầu vào để làm bước đó; "so khớp chuỗi/trace" = kiểm tra lỗi trong mảnh có trùng
với lỗi vòng lặp đang xử lý hay không.

Rồi loại dần theo utility từ thấp lên cao, không bao giờ lấn vào ngân sách. Điểm mấu chốt là **thứ tự này chạy trên plan graph, chứ không phải trên danh sách message** — đó là lý do nó cần `08` và `04` chống lưng mới phát huy tác dụng.

> 📄 **Code ví dụ:** [`examples/02-4-2-cham-utility-nhan-thuc-trajectory.ts`](examples/02-4-2-cham-utility-nhan-thuc-trajectory.ts)

> **Tóm gọn 1 câu:** Chấm điểm mỗi mảnh context bằng 30% độ mới + 40% vị trí trên lộ trình tới goal + 30% độ liên quan tới lỗi đang xử lý, rồi xoá từ điểm thấp nhất lên — vì cái cũ chưa chắc là cái vô dụng.

### 4.3 Thu Gọn, Đừng Xoá

> Phần này nói hai kỹ thuật giữ thông tin mà vẫn tiết kiệm token: gộp nội dung lặp
> lại, và ghi một dòng duy nhất cho những nhánh đã bỏ.

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

Sơ đồ đọc thế nào: 6 lần chạy `npm test` fail (exit 1 = lệnh báo lỗi) ở 6 lượt liên
tiếp được gộp thành một dòng 24 token, giữ lại thông tin đã thử 6 lần và lỗi cuối cùng
là gì.

> **Tóm gọn 1 câu:** Thay vì xoá trắng, hãy gộp các lần thử trùng nhau thành một dòng và ghi một dòng chú thích cho nhánh đã bỏ — mất 30 lần ít token hơn mà không mất thông tin.

---

## 5. Resume Block

> Phần này định nghĩa bản tóm tắt dùng để "tỉnh dậy sau nén" trông như thế nào và đạt
> chuẩn ra sao. Đây là sản phẩm đầu ra quan trọng nhất của compaction.

### 5.1 Định Dạng

Key cố định, ngân sách cứng, kiểm được bằng máy ("key" = tên trường cố định, như
`Goal:` hay `Next:` — luôn xuất hiện đúng chỗ nên code đọc được):

```
Goal:<một dòng — nhiệm vụ, không phải kế hoạch>
Decisions:[D1: …][D2: …][D3: …]        ≤5, mỗi cái ≤25 từ
Open:[t5: …][t6: …]                    task đang chờ kèm ID (→ 08)
Repro:<lệnh chính xác + dòng lỗi cuối>
Next:<đúng một hành động kế tiếp>
Invariants:[…]                          ≤5 ràng buộc được pin
Evicted:[danh sách span-id]            để audit + dựng lại
```

Đọc khung trên: `Goal` = nhiệm vụ là gì (một dòng); `Decisions` = các quyết định đã
chốt, tối đa 5 cái, mỗi cái dưới 25 từ; `Open` = các việc chưa làm kèm mã việc (t5,
t6…); `Repro` = lệnh chạy lại được + dòng lỗi cuối cùng; `Next` = đúng một việc làm
kế tiếp; `Invariants` = các luật không được vi phạm; `Evicted` = danh sách các mảnh
đã bị xoá, để sau này kiểm tra lại (audit) hoặc dựng lại.

**Vì sao key phải cố định:** resume block được đọc lại bởi *code*, không chỉ bởi mô
hình. Một parser lấy `Open[]` để dựng lại danh sách task chờ, `Repro` để gieo lại retry,
và `Evicted[]` để write-back vào memory và phát event audit. Văn xuôi tự do phá cả ba (parser = chương trình đọc văn bản theo khuôn để lấy dữ liệu).

### 5.2 Chuẩn Chất Lượng

> Phần này đưa tiêu chí "thế nào là bản tóm tắt đạt" — câu trả lời ngắn gọn: một
> agent hoàn toàn mới phải đọc xong biết làm gì tiếp.

Một resume block đạt chuẩn khi một **agent mới toanh với context trống trơn** vẫn đọc xong mà biết phải làm bước kế tiếp là gì. Cách test chuẩn nhất cũng là cách đó:

> 📄 **Code ví dụ:** [`examples/03-5-2-chuan-chat-luong.ts`](examples/03-5-2-chuan-chat-luong.ts)

Một block ghi "chúng ta đang refactor authentication và gặp vài vấn đề" fail mọi dòng
trên. Nó *có vẻ* giàu thông tin và vô dụng — đây là cách phổ biến nhất để compaction âm
thầm phá một run.

> **Tóm gọn 1 câu:** Resume block đạt chuẩn là block có trường cố định, dưới 300 token, và một agent với context rỗng đọc xong vẫn biết chính xác bước tiếp theo phải làm gì.

---

## 6. Contract Compaction↔Memory

> Phần này vẽ ranh giới giữa hai kho: context tạm (mất theo run) và memory bền (sống
> qua nhiều run) — và nói về hợp đồng (contract = cam kết giữa hai bên) hay vỡ nhất
> giữa chúng.

### 6.1 Ranh Giới

> Cách đọc bảng này: cột trái là dữ liệu mà **context tạm** (module 02) sở hữu — chết
> theo run; cột phải là dữ liệu mà **memory bền** (module 03) sở hữu — phải sống qua
> nhiều run. Ví dụ: output thô của tool chỉ cần trong run này, nhưng một quyết định
> thiết kế tuần sau vẫn cần, nên nó thuộc memory.

| Tạm — context sở hữu (→ 02) | Bền — memory sở hữu (→ 03) |
|------------------------------|---------------------------|
| Tool stdout thô | Fact đã pin |
| Body của retrieved chunk | Quyết định và lý do của nó |
| Phiên bản file đã bị thay thế | TODO còn mở |
| Chit-chat | Sở thích người dùng |
| Nhánh chết | **Resume block** |
| — | Invariant / ràng buộc |

Chú giải: "fact đã pin" = thông tin đã được xác nhận là đúng và ghim lại; "body của
retrieved chunk" = nguyên văn đoạn văn lấy từ kho nhớ; "nhánh chết" = hướng đi đã thử
và bỏ; hàng cuối cột trái trống "—" nghĩa là không có gì tương đương — invariant
*luôn* thuộc memory. Lưu ý dòng "Resume block": nó thuộc memory, tức là phải được lưu
vào kho bền chứ không chỉ nằm trong context.

Ranh giới này không phải chuyện "quan trọng hay không". Nó là câu hỏi **"qua khỏi run này còn cần nữa không?"**. Tool stdout ở lượt 4 có thể cần tới lượt 44, nhưng qua lượt 60 thì hết vai — đó là việc của context. Còn một quyết định ở lượt 12 mà tuần sau một *run khác* vẫn cần — đó là việc của memory.

> **Tóm gọn 1 câu:** Chia dữ liệu theo câu hỏi "run sau còn cần không?" — còn thì đẩy vào memory bền, không còn thì để trong context cho compaction xoá; resume block luôn thuộc bên memory.

### 6.2 Contract Hay Vỡ Nhất Trong Production

> Phần này mô tả lỗi nghiêm trọng nhất trong thực tế: nén xong nhưng quên lưu thông
> tin quan trọng vào memory, và cách trình tự 6 bước dưới đây chặn điều đó.

**Lỗi:** compaction loại một span, và thông tin bên trong nó chưa bao giờ được lưu. Lượt
sau, mô hình không biết vì sao mình đã quyết định điều đó, và tự suy ra khác đi. Run
*thành công* và codebase lệch nhẹ so với thiết kế mà người dùng đã đồng ý bốn mươi
phút trước.

**Quy tắc sống còn:** write-back **trước khi** loại. Không phải sau, không phải "để mai tính" — mà là trước. Trình tự chuẩn:

```
1. chọn span để loại (utility tăng dần)
2. trích nội dung bền: quyết định, việc còn mở, invariant, sở thích người dùng
3. lưu vào memory (scope tenant + task)                    ← fsync (→ 13)
4. phát event compaction: { keptIds, evictedIds, ratio, resumeHash }
5. thay span bị loại bằng resume block
6. tiếp tục run
```

Đọc trình tự: bước 1 = xếp thứ tự xoá từ điểm utility thấp nhất; bước 2 = moi ra phần
phải sống lâu từ mảnh sắp xoá; bước 3 = ghi xuống memory, "fsync" = lệnh ép dữ liệu
thật sự ghi xuống đĩa (không chỉ nằm trong RAM); bước 4 = ghi một sự kiện kiểm tra lại
được, gồm danh sách giữ/bỏ, tỉ lệ nén và "hash" (vân tay) của bản tóm tắt.

Bước 3 thất bại thì phải huỷ bước 5. Không phải log một cảnh báo — phải huỷ. Một
compaction đánh mất một quyết định đã tạo ra một run không thể tin, và cách rẻ nhất
để làm điều đó bất khả thi là làm nó *fail thật to*.

**Bài kiểm chứng** nằm ở §9.2, và nó là bài test đáng giá nhất của cả module: tắt
memory backend, chạy một compaction, và assert run từ chối đi tiếp (assert = câu lệnh
kiểm tra "điều này bắt buộc phải đúng, không đúng là báo lỗi").

> **Tóm gọn 1 câu:** Trước khi xoá bất cứ thứ gì khỏi context, phải lưu phần quan trọng vào memory bền trước — và nếu việc lưu thất bại thì hủy toàn bộ lần nén, đừng chạy tiếp.

---

## 7. Prompt Chống Chịu Compaction

> Phần này dạy cách *viết prompt* (đoạn chỉ dẫn gửi cho model) sao cho dù bị nén mất
> một phần thì những luật quan trọng vẫn sống sót.

### 7.1 Header / Body / Footer

Compaction kiểu gì cũng hao hụt ít nhiều, nên hãy thiết kế prompt sao cho "sống sót" được qua nó — giống như gói đồ dễ vỡ mà vẫn đi đường dài được:

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

Đọc khung trên: **HEADER** = phần đầu, chứa luật bất biến và yêu cầu đầu ra — "invariant"
= điều cấm thay đổi (không thêm thư viện, giữ tương thích, không đổi API công khai);
"unified diff" = định dạng bảng so sánh code cũ/mới chuẩn của git; "migration" = ghi
chú chuyển đổi sang cấu trúc mới. **BODY** = phần giữa, chứa toàn bộ ngữ cảnh tra
cứu (file, kết quả tool) — đây là phần cho phép nén thoải mái. **FOOTER** = phần cuối,
lặp lại các luật của HEADER một lần nữa.

**Cơ sở thực nghiệm** là kết quả lost-in-the-middle (§10.5): mô hình chú ý đáng tin
cậy nhất ở đầu và cuối một context dài. Đặt invariant ở cả hai nơi nghĩa là một
summarizer chỉ giữ phần đầu *và* phần cuối vẫn giữ được ràng buộc — và một summarizer
giữ 80% token giữ chúng gần như chắc chắn.

> **Tóm gọn 1 câu:** Đặt các luật bất biến ở cả đầu lẫn cuối prompt (HEADER/FOOTER), phần giữa dành cho ngữ cảnh được phép nén — vì model chỉ chú ý đáng tin cậy ở hai đầu context.

### 7.2 Cái Gì Bị Summarizer Bỏ

> Phần này liệt kê các thứ model thường làm rơi khi tóm tắt, và cách giữ chúng an toàn.
> "Summarizer" = bộ tóm tắt (thường là chính model LLM nhận lệnh nén).

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

> **Tóm gọn 1 câu:** Model tóm tắt hay rơi mất mệnh đề phủ định, con số và ID — nên giữ chúng nguyên văn ở HEADER/FOOTER hoặc trong các trường cố định của resume block, đừng bao giờ để nó được "diễn giải lại".

---

## 8. Implementation TypeScript

> Phần này trỏ tới code hiện thực compaction bằng TypeScript (ngôn ngữ lập trình của
> hầu hết agent harness). Mỗi mục là một file ví dụ trong thư mục `examples/` — mở file
> để xem code đầy đủ kèm chú thích.

### 8.1 Types

> Định nghĩa các kiểu dữ liệu (types = khuôn dữ liệu, ví dụ "Span", "ResumeBlock")
> mà toàn bộ hệ compaction dùng chung.

> 📄 **Code ví dụ:** [`examples/04-8-1-types.ts`](examples/04-8-1-types.ts)

### 8.2 shouldCompact + compact()

> Hai hàm lõi: `shouldCompact()` quyết định "giờ nén chưa?", `compact()` thực hiện
> việc nén (ghim → chấm điểm → xoá → tạo resume block).

<details>
<summary>TypeScript Code — trigger + pin + prune theo utility + resume (Click để mở rộng/thu gọn)</summary>

> 📄 **Code ví dụ:** [`examples/05-8-2-shouldcompact-compact.ts`](examples/05-8-2-shouldcompact-compact.ts)

</details>

### 8.3 Bộ Chấm Utility Theo Trajectory

> Hiện thực công thức chấm điểm utility ở §4.2 — đầu vào là các span và plan graph,
> đầu ra là điểm số để xếp thứ tự xoá.

> 📄 **Code ví dụ:** [`examples/06-8-3-bo-cham-utility-theo-trajectory.ts`](examples/06-8-3-bo-cham-utility-theo-trajectory.ts)

### 8.4 Builder Cho Resume Block

> Hàm dựng resume block đúng khuôn §5.1, kèm trần 300 token ép buộc.

> 📄 **Code ví dụ:** [`examples/07-8-4-builder-cho-resume-block.ts`](examples/07-8-4-builder-cho-resume-block.ts)

### 8.5 Write-Back Vào Memory

> Hiện thực bước 3 của trình tự §6.2: lưu quyết định, việc còn mở, invariant vào
> memory bền *trước* khi xoá khỏi context.

> 📄 **Code ví dụ:** [`examples/08-8-5-write-back-vao-memory.ts`](examples/08-8-5-write-back-vao-memory.ts)

> **Tóm gọn 1 câu:** Hệ compaction gồm 5 mảnh code: types chung, hàm kích hoạt + nén, bộ chấm điểm, builder dựng resume block, và hàm lưu vào memory — mỗi mảnh có một file ví dụ riêng để bạn đọc theo thứ tự.

---

## 9. Kiểm Thử Compaction

> Phần này nói cách test compaction. Có ba tầng: bất biến (luôn đúng), contract
> (cam kết giữa hai module), và hồi quy chất lượng (chất lượng có tụt không).

### 9.1 Test Bất Biến

> "Test bất biến" = kiểm tra những điều bắt buộc luôn đúng sau mọi lần nén, ví dụ:
> các mục trong pin set chưa bao giờ bị xoá.

> 📄 **Code ví dụ:** [`examples/09-9-1-test-bat-bien.ts`](examples/09-9-1-test-bat-bien.ts)

Chạy các test này cho **mọi** trajectory đã ghi có compaction, trong CI đêm. Trajectory
thật bắt được các trường hợp biên mà dữ liệu tổng hợp không bao giờ bắt (CI = hệ thống
tự chạy test sau mỗi lần lưu code; "biên" = trường hợp lắt nhét dễ làm code sai).

### 9.2 Contract Test Quan Trọng Nhất

> Đây là bài test quan trọng nhất của cả module: tắt memory đi, thử nén — hệ phải
> từ chối, không được nén.

> 📄 **Code ví dụ:** [`examples/10-9-2-contract-test-quan-trong-nhat.ts`](examples/10-9-2-contract-test-quan-trong-nhat.ts)

Test thứ hai là tiêu chuẩn nghiệm thu thực sự của cả module. Nó cũng là test mà phần
lớn đội bỏ qua, và là test đã bắt được sự cố lượt 47 ở phần đầu tài liệu.

### 9.3 Bộ Hồi Quy Chất Lượng

> "Hồi quy" (regression) = so sánh chất lượng trước/sau một thay đổi để bắt sự tụt.
> Phần này đo xem run có còn thành công sau khi nén không.

Theo dõi, mỗi lần compaction, run có còn thành công không. Nếu chất lượng giảm sau
compaction, pin set sai — và đây chính là phép đo tìm ra điều đó:

> 📄 **Code ví dụ:** [`examples/11-9-3-bo-hoi-quy-chat-luong.sql`](examples/11-9-3-bo-hoi-quy-chat-luong.sql)

Một run cụ thể chỉ fail khi có compaction ngay trước thất bại là tín hiệu mạnh nhất
cho thấy pin set đang thiếu thứ gì đó.

> **Tóm gọn 1 câu:** Ba tầng test: bất biến chạy đêm trên dữ liệu thật, contract test "tắt memory phải nén không nổi" (quan trọng nhất), và hồi quy so sánh tỉ lệ thành công trước/sau nén để bắt pin set thiếu.

---

## 10. Case Study Thực Tế

> Phần này xem 5 sản phẩm/nghiên cứu thật xử lý compaction thế nào, để rút bài học cho
> hệ của bạn: Claude Code, Aider, Devin, Letta/MemGPT và nghiên cứu "Lost in the Middle".

### 10.1 Claude Code — /compact và Auto-Compact

Coding agent của Anthropic trình bày compaction vừa là **lệnh của người dùng**
(`/compact` — gõ lệnh này để nén ngay khi muốn) vừa là **trigger tự động** khi mức sử dụng context cao. Ba lựa chọn thiết
kế đáng học:

1. **Đường thủ công và tự động dùng chung một implementation.** Người dùng gặp vấn đề
   bằng tay nhận đúng chất lượng mà đường tự động tạo ra — không có trải nghiệm hạng hai,
   và chỉ một đường code để kiểm thử.
2. **Người dùng nhìn thấy và điều khiển được ngân sách.** Đưa mức sử dụng context ra ngoài
   biến compaction thành một phần nhìn thấy được của workflow thay vì một ẩn thuật tự
   nhiên (workflow = chuỗi công việc).
3. **Compaction được trình bày như một checkpoint.** Người dùng hiểu "context đã được
   nén; đây là những gì tôi nhớ" vì nó được diễn đạt như một điểm lưu, không phải một
   thao tác cắt bớt ẩn.

> **Tóm gọn 1 câu:** Claude Code dạy ba điều: đường nén tay và nén tự động phải dùng chung một code, cho người dùng thấy mức đầy context, và thông báo nén như một "điểm lưu" thay vì cắt khoét ngầm.

### 10.2 Aider — Repo Map + History Digest

Aider là công cụ lập trình AI chạy trong terminal. `repo map` của nó là hình thức thuần khiết nhất của pin set: một chỉ mục gọn, luôn
hiện diện, về cấu trúc repository (đường dẫn file, chữ ký, tên class/hàm) sống sót mọi
lần loại. Mô hình hiếm khi cần toàn bộ thân file để điều hướng — nó cần *biết file tồn
tại và bên trong có gì*.

History digest của nó chính là resume block: một bản tóm tắt có cấu trúc về hướng đi của
cuộc hội thoại, với các bản sửa được giữ *nguyên văn*. Bài học là về **cái gì cần giữ
thô**: diff mới là phần không thể thay thế. Một bản tóm tắt của diff gần như vô dụng,
vì giá trị của một diff nằm ở đúng những byte của nó.

> **Tóm gọn 1 câu:** Aider chứng minh hai mảnh nên giữ nguyên: bản đồ cấu trúc repo (để điều hướng) và diff sửa code ở dạng thô — tóm tắt diff là mất luôn giá trị của nó.

### 10.3 Devin — Quản Lý Context Cho Run Dài

Devin là agent tự trị (agent tự làm việc nhiều bước mà không cần con người ra lệnh từng
việc). Các coding agent tự trị chạy hàng chục phút liên tục gặp giới hạn context liên tục,
và xử lý nó như một thao tác thường lệ chứ không phải ngoại lệ:

- **Context theo phạm vi task.** Mỗi task trong plan có cửa sổ context riêng; việc hoàn
  thành một task *chính là* một biên compaction. Đây là trigger "biên task" ở §2.2, và
  là biến thể sạch nhất khi plan có các đường nối rõ ràng.
- **Tóm tắt tiến độ thành artifact.** Mỗi task tạo ra một bản tóm tắt được ghi vào hồ
  sơ session, không chỉ giữ trong context. Artifact đó là thứ con người đọc để review
  run, và là thứ một run sau nạp lại nếu nó resume.
- **Output test được giữ có cấu trúc, không tóm tắt.** Tên test fail và assertion (câu
  điều kiện "kỳ vọng X ra giá trị Y") được giữ chính xác; các stack frame xung quanh bị bỏ.

> **Tóm gọn 1 câu:** Devin nén theo mốc xong việc (mỗi task là một điểm nén), ghi bản tóm tắt tiến độ ra file bên ngoài để xem lại, và giữ tên test/lỗi nguyên văn thay vì tóm tắt.

### 10.4 Letta / MemGPT — Memory Phân Tầng Như Context Ảo

Letta (tên sản phẩm của nghiên cứu MemGPT) xử lý context như hệ điều hành xử lý RAM:
dữ liệu nhỏ nằm trong "RAM" (context), dữ liệu lớn nằm ngoài ở "đĩa" (kho memory).
Bài báo MemGPT định khung lại compaction như một **kiến trúc memory** thay vì một thủ
thuật tổng hợp: mô hình có một "bộ nhớ làm việc" nhỏ trong context và một kho lớn bên
ngoài, và nó phát lệnh tool tường minh để load/tháo thông tin. Agent tự quyết định cái
gì cư trú.

Đây là một mô hình mạnh hơn cho cùng một bài toán, và nó làm ranh giới memory↔context
trở nên tường minh thay vì ẩn. Cái giá phải trả: quyết định phân trang do một mô hình
ngẫu nhiên đưa ra, nên bạn vẫn cần pin set xác định bên dưới làm sàn. Mẫu production
hình thành: **phân trang kiểu Letta để chọn *cái gì* cần load, pinning xác định cho
*cái gì tuyệt đối không được mất*.**

> **Tóm gọn 1 câu:** MemGPT/Letta cho model tự load/tháo dữ liệu như hệ điều hành quản lý RAM — mạnh, nhưng vẫn cần một pin set cứng bên dưới để thứ sống còn không bao giờ bị tháo nhầm.

### 10.5 Lost in the Middle — Nghiên Cứu Đứng Sau Pinning

Đây là bài nghiên cứu khoa học giải thích *vì sao* các thiết kế ở trên lại tốt: model
đọc context dài kiểu "đầu và cuối rõ, giữa mơ".

Liu et al. (2023) chỉ ra rằng hiệu năng transformer (kiến trúc model ngôn ngữ) suy giảm mạnh khi thông tin liên
quan nằm ở *giữa* một context dài, trong khi đầu và cuối được chú ý đáng tin cậy. Hai
hệ quả trực tiếp cho thiết kế compaction:

1. **Cấu trúc prompt HEADER/FOOTER** (§7.1) không phải mê tín — nó khai thác hồ sơ
   chú ý đo được.
2. **Pruning nên dồn về phía trước.** Nội dung cũ (rơi vào giữa context sau khi nội
   dung mới được nối vào) là thứ rẻ nhất để bỏ, đó là lý do `recency` chỉ chiếm 30%
   trong hàm utility — các thành phần đồ thị mới là thứ chi phối.

Bài báo cũng giải thích một kết quả thực nghiệm gây bối rối: mô hình thường *làm tệ
hơn* với context đã tóm tắt so với context bị cắt bớt, vì một bản tóm tắt trôi chảy
tạo ấn tượng sai về độ phủ (nghĩa là model tưởng bản tóm tắt đã đủ thông tin, trong
khi nó còn thiếu). Vì vậy tiêu chuẩn ở §5.2 là đánh giá block bằng khả năng
tiếp tục từ agent lạnh, không phải bằng cách đọc nó.

> **Tóm gọn 1 câu:** Nghiên cứu "Lost in the Middle" chứng minh model chú ý kém ở giữa context — đó là lý do HEADER/FOOTER giữ luật ở hai đầu và nội dung cũ giữa context là ứng viên xoá rẻ nhất.

---

## 11. TypeScript Interfaces Cho Compaction

> Phần này gom toàn bộ "bề mặt kiểu" (interface = hợp đồng mô tả dữ liệu và hàm mà
> các module phải theo) của hệ compaction vào một file ví dụ duy nhất, để bạn xem bức
> tranh trọn vẹn một chỗ.

> 📄 **Code ví dụ:** [`examples/12-11-typescript-interfaces-cho-compaction.ts`](examples/12-11-typescript-interfaces-cho-compaction.ts)

> **Tóm gọn 1 câu:** Mở file ví dụ trên để xem toàn bộ interface của compaction — đây là "bản vẽ kỹ thuật" trước khi đọc các nguyên tắc thiết kế ở phần sau.

---

## 12. Nguyên Tắc Thiết Kế Cho Compaction

> Phần này chắt lọc mọi thứ phía trên thành các nguyên tắc khi thiết kế: một bảng
> SOLID (5 nguyên tắc thiết kế phần mềm kinh điển) và 6 nguyên tắc riêng cho compaction.

### 12.1 SOLID Cho Quản Lý Context

> Cách đọc bảng này: cột trái là chữ cái đầu của nguyên tắc SOLID (S-O-L-I-D), cột
> phải là nó áp vào compaction ra sao. Ví dụ: "S" = một class chỉ làm một việc — ở đây
> compactor chỉ quyết định cái gì bị bỏ, không tự tóm tắt văn bản.

| Nguyên tắc | Áp dụng |
|------------|---------|
| **S**ingle responsibility | `Compactor` quyết định cái gì đi; `MemoryStore` lưu; `TrajectorySink` ghi. Không cái nào tóm tắt văn xuôi — đó là một dependency `Summarizer`. |
| **O**pen/closed | Chiến lược loại khác là `CompactionPolicy` + bộ chấm mới, không phải viết lại compactor. |
| **L**iskov substitution | Các implementation `MemoryStore` (Postgres, vector DB, file) thay thế được nhau; hợp đồng write-back giống hệt. |
| **I**nterface segregation | Bộ lắp context cần `shouldCompact()`; công cụ debug cần `render()`. Đừng bắt debug tooling phụ thuộc plan graph. |
| **D**ependency inversion | Compaction phụ thuộc `PlanGraph` như một interface, nên một đồ thị tổng hợp chạy được trong unit test mà không cần planner. |

Chú giải các tên trong bảng: `Compactor` = module thực hiện nén; `MemoryStore` = kho
lưu memory bền (Postgres = cơ sở dữ liệu phổ biến; vector DB = kho dữ liệu tìm theo
ý nghĩa); `TrajectorySink` = nơi ghi lại chuỗi bước chạy; `CompactionPolicy` = đối
tượng chứa chiến lược nén thay thế được; `PlanGraph` = đồ thị kế hoạch; `planner` =
module sinh kế hoạch.

### 12.2 Sáu Nguyên Tắc Thiết Kế

> Sáu quy tắc dưới đây là "tấm chân lý" rút ra từ toàn bộ module — nếu chỉ nhớ 6 dòng
> từ tài liệu này, hãy nhớ chúng.

1. **Prune trước, tóm tắt sau.** Bỏ nhánh chết là miễn phí và không mất thông tin; tóm tắt là tốn kém và có hao hụt. Làm sai thứ tự tốn tiền và thông tin.
2. **Pin bằng suy ra, không bằng tay.** Pin set tính từ plan, loop đang hoạt động, và danh sách gate chờ — nên nó co lại khi công việc xong thay vì phình ra cho tới khi vỡ ngân sách.
3. **Ngân sách là trần cứng.** 300 token cho resume block, 70% để trigger. Cả hai được ép trong code, cả hai được assert trong test.
4. **Persist trước khi loại, hoặc đừng loại.** Compaction không write-back được thì huỷ. Một run lặng lẽ mất quyết định tệ hơn một run dừng lại với lỗi.
5. **Policy xác định.** Trigger, pin, và thứ tự loại đều tính từ trạng thái đo được. Mô hình không bao giờ quyết định nó quên gì.
6. **Hợp đồng là với một agent lạnh.** Chỉ nhận một resume block khi một agent mới với context rỗng hành động đúng bước kế tiếp từ nó.

> **Tóm gọn 1 câu:** Sáu nguyên tắc cần nhớ: xoá trước tóm tắt sau, ghim tự động, trần cứng 70%/300 token, lưu trước khi xoá, mọi quyết định từ số đo được, và chuẩn nghiệm thu là "agent mới đọc xong biết làm gì".

---

## 13. Best Practices

> Phần này là danh sách nên/không nên rút gọn từ mọi phần trước — dùng như tài liệu
> tra nhanh khi hiện thực.

### 13.1 NÊN ✅

> Mỗi dòng là một việc nên làm; số/ngưỡng có thể tra lại ở phần tương ứng.

- Trigger ở 70% sử dụng hoặc 20 lượt, cái nào tới trước; chừa 30% headroom cho tool result kế tiếp.
- Pin system, goal, invariant, diff đang hoạt động, chỉ dẫn user cuối, và lỗi của loop chưa giải quyết.
- Để pin của loop đã giải quyết trở thành evictable; pin set không tăng đơn điệu (tức là không chỉ dài ra mà không co lại).
- Xếp hạng loại theo reachability trên plan graph, không theo tuổi (reachability = bước đó có nằm trên lộ trình tới goal không).
- Gộp 3+ lần retry giống hệt thành một dòng, giữ nguyên văn lỗi cuối.
- Giới hạn resume block 300 token với key cố định, và assert trong CI.
- Persist quyết định, việc còn mở, invariant vào memory với `fsync` **trước khi** loại.
- Phát event `compaction` với `keptIds`, `evictedIds`, `ratio` (→ 13).
- Test bằng agent lạnh: cùng hành động kế tiếp từ resume block như từ context đầy đủ.

### 13.2 KHÔNG NÊN ❌

> Mỗi dòng là một lỗi hay gặp, kèm lý do ở ngay sau vạch gạch.

- ❌ Không trigger ở 90% rồi hy vọng kết quả kế tiếp vừa. Nó sẽ không vừa, và bạn compact dưới áp lực — lúc tệ nhất để chịu hao hụt.
- ❌ Không dùng loại FIFO/oldest-first. Nó giữ `ls` của hôm qua và bỏ định nghĩa nhiệm vụ.
- ❌ Không để mô hình quyết định khi nào compact.
- ❌ Không tóm tắt toàn bộ transcript khi phần lớn nó là nhánh chết.
- ❌ Không diễn giải lại các giá trị được pin (số, ID, ràng buộc phủ định). Diễn giải là nơi độ chính xác chết.
- ❌ Không để pin set tăng đơn điệu. Pin của loop đã giải quyết phải thành evictable.
- ❌ Không write-back vào memory "để sau". Sau là khi quyết định đã mất rồi.
- ❌ Không coi một bản tóm tắt trôi chảy là bằng chứng về độ phủ. Hãy test bằng khả năng tiếp tục từ agent lạnh.
- ❌ Không compact giữa một task khi plan có đường nối tự nhiên — hãy compact tại đường nối.

> **Tóm gọn 1 câu:** Tóm tắt toàn bộ phần NÊN/KHÔNG NÊN: nén ở 70% hoặc 20 lượt, ghim thứ sống còn, xoá theo độ hữu ích, lưu vào memory trước khi xoá — và đừng nén ở 90%, đừng dùng FIFO, đừng để model tự quyết.

---

## 14. Anti-Patterns & Cách Khắc Phục

> "Anti-pattern" = mô hình làm sai hay gặp, có tên để gọi cho nhanh. Cách đọc bảng
> này: cột "Triệu chứng" là dấu hiệu bạn thấy khi hệ đang dính lỗi đó; "Cách sửa" là
> phương thuốc. Ví dụ: anti-pattern "Compaction ở 95%" — triệu chứng là bản tóm tắt
> mất chi tiết vì nén khi đã quá sát trần; sửa bằng cách dời trigger xuống 70%.

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

Chú giải từ khó: "persist" = lưu xuống bộ nhớ bền; "đơn điệu" ở đây = chỉ tăng không
giảm; "eval" = bộ đánh giá tự động chấm chất lượng đầu ra; "khởi động lạnh" (cold
start) = khởi động với context hoàn toàn trống.

> **Tóm gọn 1 câu:** Bảng trên là 11 lỗi hay gặp nhất khi làm compaction, mỗi lỗi có triệu chứng để nhận ra và cách sửa đã đề cập ở các phần trước — tra theo triệu chứng bạn đang thấy.

---

## 15. Production Checklist

> Checklist = danh sách soát trước khi đưa vào chạy thật (production). Mỗi dòng là
> một mục cần kiểm; phần sau vạch gạch là tiêu chí đạt. Ví dụ: "Trigger" đạt khi hệ
> tự nén ở 70% hoặc 20 lượt, tính từ số token đo được chứ không phải đoán.

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

> **Tóm gọn 1 câu:** Trước khi ship, soát 13 mục trên — đủ trigger, đủ pin, đúng thứ tự xoá, resume block có trần, ghi nhớ trước khi xoá, có log kiểm tra và có test chạy thật.

---

## 16. Xu Hướng Tương Lai

> Phần này dự đoán compaction sẽ đi về đâu trong giai đoạn 2026–2028 — đọc để biết
> hướng thiết kế đáng "đặt cược" theo.

### 16.1 Compaction Nhận Thức Cấu Trúc (2026-2028)

> "Nhận thức cấu trúc" = nén dựa trên cấu trúc nhiệm vụ (kế hoạch, đồ thị) thay vì
> nén dòng hội thoại trơn.

- **Tóm tắt plan, không tóm tắt transcript.** Nếu plan graph (→ 04) cộng resume block đã đủ để quyết định hành động kế tiếp, transcript là thừa — một mục tiêu compaction nhỏ hơn nhiều và đáng tin hơn.
- **Policy loại được học.** Huấn luyện hàm utility trên dữ liệu span nào thực sự đi trước kết quả thành công so với thất bại, thay vì tự đặt tay trọng số ba thành phần.
- **Prefetch trong lúc tóm tắt.** Chính lời gọi summarizer đã biết bước kế cần gì; hãy để nó phát ra một `prefetch` (tải trước dữ liệu cho bước kế) kèm resume block, để lượt sau bắt đầu với context đúng đã sẵn sàng.

### 16.2 Compaction Có Thể Kiểm Chứng

> "Kiểm chứng" (verifiable) = chứng minh được bằng số liệu, không phải cảm tính. Phần
> này nói về làm sao biết được nén đã giữ đúng thứ cần giữ.

Compaction xấu xa theo bản chất, và hôm nay không gì chứng minh được thứ được giữ lại
là quan trọng. Hai hướng: **đo độ phủ** (tỉ lệ fact *liên quan tới goal* còn sống, đo
trên bộ eval), và **danh sách loại có thể audit** (`evicted[]` đã tồn tại; bước tiếp
theo là làm nó truy vấn được, để "chúng ta đánh mất gì" là một câu hỏi một query
trước khi nó thành incident — incident = sự cố thật trong vận hành).

### 16.3 Compaction Như Một Loại Step Chính Thức

> Phần này nói về việc biến nén từ phản ứng khẩn cấp thành một bước được lên kế hoạch
> sẵn trong kế hoạch (plan) của agent.

Khi một plan chứa các node `compact` tường minh — tại đường nối task, trước thao tác
rủi ro, trước khi chuyển context cho một sub-agent (→ 09 §16.2) — compaction thôi là
một phản ứng khẩn cấp với ngưỡng và trở thành một phần được thiết kế của quá trình thực
thi. Đó là khác biệt giữa một agent sống sót được các run dài và một agent chỉ đơn
giản là may mắn.

### 16.4 Vượt Qua Giới Hạn Của Tổng Hợp

> Phần này nói về cách "ăn gian" bài toán nén: đừng đặt dữ liệu to vào context ngay
> từ đầu.

- **Đưa trạng thái ra ngoài.** Chuyển trạng thái lớn (test fixture — dữ liệu mẫu cho
  test, thân file) sang một kho và chỉ giữ handle (tham chiếu/địa chỉ) trong context. Dạng mạnh nhất của compaction không phải tóm tắt dữ liệu — mà là không bao giờ đặt nó vào đó.
- **Cư trú phân tầng kiểu MemGPT**, với pin set xác định làm sàn bên dưới các quyết định phân trang của mô hình.

> **Tóm gọn 1 câu:** Tương lai của compaction: nén theo kế hoạch thay vì hội thoại, học thứ tự xoá từ dữ liệu, đo được độ phủ, nén như một bước có chủ đích trong plan — và tối ưu nhất là đừng đặt dữ liệu to vào context từ đầu.

---

## Tài Liệu Tham Khảo

> Phần này liệt kê nguồn đọc thêm: bài nghiên cứu (link arXiv), công cụ/framework,
> các hệ production đã nói ở case study, và các module liên quan trong repo này.
> Giữ nguyên link — bấm để đọc nguồn gốc.

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

Chú giải nhanh: tiktoken và LiteLLM là hai thư viện giúp *đếm token chính xác* — quan
trọng vì trigger 70% phải tính từ số đo được, không phải ước lượng.

### Production Systems

- **Claude Code** — https://claude.com/product/claude-code — compaction thủ công + tự động, ngân sách nhìn thấy được
- **Aider** — https://aider.chat — repository map làm pin set thường trực
- **Letta** — https://letta.com — memory như context ảo
- **Devin** — https://devin.ai — context theo phạm vi task

### Module Liên Quan

> Đây là các module khác trong repo liên quan tới compaction; số § là mục trong
> module đó. Ví dụ: `07-workflow/README.md` §13.4 = mục 13.4 của module Workflow.

- `02-build-context/README.md` §16 — phía tạm của contract (assembly, marking, fan-out)
- `03-update-memory-store/README.md` §12 — phía bền (đích write-back, GDPR, retrieval)
- `04-plan-decompose-task/README.md` — plan graph làm chấm reachability khả thi
- `05-prompt-builder/README.md` §17.5 — cấu trúc invariant HEADER/FOOTER
- `07-workflow/README.md` §13.4 — compaction như một loại step chính thức của engine
- `09-multi-agent/README.md` §16.2 — compaction trước khi chuyển context cho sub-agent
- `10-automation/README.md` §17.3 — loop budget, mà compaction giữ cho phải chăng
- `13-trajectory-observability/README.md` — event `compaction` và dấu vết audit của nó
- `15-approval-gates/README.md` — approval đang chờ là một phần của pin set

> **Tóm gọn 1 câu:** Mọi khẳng định trong tài liệu này đều có nguồn ở trên — đọc nghiên cứu "Lost in the Middle" và MemGPT trước nếu muốn đi sâu, hoặc trỏ thẳng tới module liên quan nếu đang hiện thực.

---

*Tài liệu: Harness 14. Context Compaction — HARNESS ENGINEERING EDITION*
*Module cross-cutting · thứ cho phép một context window cố định gánh một run không giới hạn*
*Cập nhật: 16/10/2026*
*Tác giả: AI Knowledge Repository*

---

## Cập nhật 10/2026 — Compaction Theo Anthropic (09/2025)

> Phần bổ sung này tóm tắt hướng dẫn chính thức mới nhất của Anthropic về compaction
> (bài "Effective context engineering for AI agents", 09/2025). Nó trả lời hai câu
> hỏi thực dụng: nên bỏ gì trước, và viết prompt nén thế nào cho tốt.

> Bổ sung từ bài **"Effective context engineering for AI agents"** (Anthropic, 09/2025) —
> hướng dẫn cụ thể hơn về cách viết compaction prompt và những gì thực sự an toàn để loại bỏ.

### 1. Tool Result Clearing — Compaction "Lighter Touch" Nhất

> "Tool result clearing" = xoá/ghé nhẹ lên kết quả cũ của tool thay vì nén cả hội
> thoại. "Lighter touch" = cách can thiệp nhẹ nhất.

**Tool result cũ** là ứng viên loại bỏ an toàn nhất vì: nó đã từng được *đọc*
(không phải trôi nổi) và chỉ chứa *trạng thái trung gian* — không phải quyết định,
không phải invariant, không phải định nghĩa nhiệm vụ.

Nói cách khác, **tool result clearing là dạng compaction nhẹ nhất (lightest touch)**
mà vẫn hợp lý. Nếu bạn chưa làm gì về compaction, bắt đầu từ đây — nó đã được
Anthropic đưa thành tính năng chính thức **"Context Management"** trên Claude
Developer Platform.

Nguyên tắc: deep trong lịch sử hội thoại (old tool results) đã phục vụ xong mục đích,
model đã extract thông tin cần thiết từ nó rồi — **raw result giờ chỉ chiếm chỗ**.

> **Tóm gọn 1 câu:** Bắt đầu làm compaction từ việc xoá kết quả tool cũ — đây là cách nén nhẹ nhất, an toàn nhất, vì model đã đọc và chắt lọc xong thông tin cần thiết từ nó rồi.

### 2. Compaction Prompt Tuning — Bắt Đầu Từ Recall, Rồi Iterate Precision

> Phần này dạy quy trình hai pha để viết prompt cho bộ tóm tắt. "Recall" = độ phủ
> (bắt được bao nhiêu thông tin quan trọng); "precision" = độ chính xác (ít rác thừa
> bao nhiêu). Cứ nhớ: thiếu còn tệ hơn thừa ở pha đầu.

Anthropic khuyến nghị quy trình 2 pha để viết compaction prompt:

1. **Pha 1 — Maximize recall:** Yêu cầu summarizer capture **mọi thông tin quan trọng**
   trước. Chưa cần gọn — miễn sao không bỏ sót gì. Lỗi này (thêm thừa) rẻ hơn
   lỗi kia (bỏ sót cần thiết).
2. **Pha 2 — Iterate precision:** Sau khi prompt đạt recall 100%, lần lượt thử
   bỏ thông tin "có vẻ superfluous" (thừa thãi) và kiểm tra run có còn đúng không. Lặp cho
   tới khi precision cao mà không mất recall.

**Những thứ PHẢI giữ** (trong mọi compaction):

- Architectural decisions đã đưa ra (các quyết định kiến trúc, ví dụ "dùng Redis lưu session")
- Unresolved bugs (bug nào đang mở, tại sao)
- Implementation details đang dùng (chi tiết hiện thực đang áp dụng)
- Current task state — mục tiêu + tiến độ + bước kế tiếp

**Những thứ CÓ THỂ bỏ:**

- Raw tool outputs cũ (đã đọc rồi, không còn cần)
- Tool definitions đã đọc rồi (model không cần nhắc lại cách dùng tool)
- Messages đã summarized ở lần compact trước

> **Tóm gọn 1 câu:** Viết prompt nén theo 2 pha: pha 1 bắt đủ mọi thông tin quan trọng (quyết định, bug mở, trạng thái việc), pha 2 mới cắt bớt dần phần thừa — và luôn giữ nguyên các thứ trong danh sách "PHẢI giữ".

### 3. Contract Với Module 02-Build-Context

> Phần này nói compaction gắn vào module 02 (dựng context) ở đâu: đó là trường
> `history` trong cấu trúc `BuiltContext` — và danh sách ghim xuất phát từ đúng chỗ đó.

Compaction output là **trường `history`** trong cấu trúc `BuiltContext` (module 02).
Pin set bắt nguồn từ ranh giới đó:

- **Pin set tuyệt đối** = `system` + `goal` — hai phần không bao giờ cắt, bất kể
  compaction nào xảy ra.
- Mọi phần khác của `BuiltContext` (`retrieved`, `immediate`, `history`) đều nằm
  trong danh sách evictable và tuân theo thứ tự loại theo utility (§4).

```
BuiltContext (→ 02)
├── system  ───────────────────► PIN (không bao giờ cắt)
├── goal    ───────────────────► PIN (không bao giờ cắt)
├── retrieved ─────────────────► evictable (theo utility)
├── history ────────────────────► evictable (theo utility) ← COMPACTION ĐỔ VÀO ĐÂY
└── immediate ─────────────────► evictable (theo utility)
```

Đọc sơ đồ: `BuiltContext` là "khay" ngữ cảnh được ghép mỗi lượt — `system` (chỉ dẫn
hệ thống) và `goal` (mục tiêu) luôn được ghim; `retrieved` (đoạn lấy từ kho nhớ),
`history` (lịch sử hội thoại — nơi kết quả nén đổ vào) và `immediate` (thông tin
ngay trong lượt này) đều được phép nén/xoá theo điểm utility.

> **Tóm gọn 1 câu:** Kết quả nén sống trong trường `history` của `BuiltContext`; chỉ `system` và `goal` là không bao giờ bị cắt — mọi phần khác đều chịu luật nén theo utility.

### 4. Bảng "Giữ vs Bỏ"

> Cách đọc bảng này: cột trái là thứ **không bao giờ bỏ**; cột phải là thứ **bỏ được
> sau khi model đã đọc/extract xong**. Ví dụ: quyết định kiến trúc ở trái — giữ mãi;
> raw tool output cũ ở phải — bỏ thoải mái.

| Giữ (không bao giờ bỏ) | Bỏ được (sau khi đọc xong) |
|------------------------|----------------------------|
| Architectural decisions | Raw tool outputs cũ |
| Unresolved bugs + stack trace | Tool definitions đã đọc |
| Current task state (goal, progress, next step) | Messages đã summarized ở lần trước |
| File paths đang làm việc | Nhánh thất bại đã giải quyết |
| Invariants / ràng buộc (HEADER/FOOTER, → §7) | Chit-chat, greeting |

**Quy tắc nhớ nhanh:** "loại cái cần tới **sau** khi loại cái cần tới **trước**" —
tool result là cái cần tới trước (bạn đọc để extract thông tin), nên sau khi extract
xong nó thành "không cần nữa" và rơi vào nhóm bỏ được.

> **Tóm gọn 1 câu:** Ghi nhớ 2 cột: quyết định, bug mở, trạng thái việc, đường dẫn file, ràng buộc thì giữ mãi; tool output cũ, định nghĩa tool đã đọc và tin nhắn đã tóm tắt thì bỏ được.

### 5. Code Mẫu — should_compact + compact

> Đây là bản ví dụ bằng Python (thay vì TypeScript ở §8) hiện thực cùng hai hàm:
> kiểm tra "nén chưa?" và thực hiện nén, kèm chính sách giữ 5 file gần nhất.

<details>
<summary>Python Code — should_compact + compact với giữ 5 files gần nhất (Click to mở rộng/thu gọn)</summary>

> 📄 **Code ví dụ:** [`examples/13-5-code-mau-should-compact-compact.py`](examples/13-5-code-mau-should-compact-compact.py)

</details>

> **Tóm gọn 1 câu:** Mở file ví dụ Python trên để xem bản hiện thực gọn của hai hàm `should_compact` + `compact` — phù hợp nếu hệ của bạn viết bằng Python thay vì TypeScript.

### 6. Liên Quan Trong Repo

> Phần này trỏ tới 2 tài liệu khác trong repo có liên quan trực tiếp — đọc kèm để
> thấy bức tranh toàn cảnh.

- [02-build-context](../02-build-context/README.md) — Compaction output là trường
  `history` trong `BuiltContext`; hybrid pre-computed + just-in-time retrieval đi cùng
  compaction để context luôn có signal cao.
- [AGENT_SYSTEM_ARCHITECTURE.md](../../AGENT_SYSTEM_ARCHITECTURE.md) — **Layer 3**
  (build context) ghép với **Layer 4** (compaction/memory) trong kiến trúc agent.

Chú giải: "hybrid pre-computed + just-in-time retrieval" = kết hợp lấy sẵn thông tin
tính trước với lấy đúng lúc cần; "Layer 3 / Layer 4" = tầng số 3 và 4 trong bản đồ
kiến trúc agent của tài liệu chính.

> **Tóm gọn 1 câu:** Kết quả nén sống trong trường `history` của `BuiltContext` (module 02), và trong bản đồ kiến trúc tổng, compaction nằm ở tầng 4 — ghép với tầng 3 là tầng dựng context.
