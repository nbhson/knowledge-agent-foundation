# 🧠 Human Attention Engine

> Trong kỷ nguyên AI tạo code, **human attention** chính là tài nguyên khan hiếm nhất.

---

## Mở đầu: AI tạo code → Human Attention trở thành bottleneck

Không phải:

> “AI review code cho developer.”

Mà là:

> **AI đã làm cho code generation trở nên rẻ, nhưng human review vẫn đắt.**

Vì vậy cần một hệ thống tối ưu hóa **“human attention”** dành riêng cho AI-generated code.

Và nếu làm đúng, nó có thể trở thành một lớp nằm giữa **AI coding agent** và **Git/PR**.

---

## 1. Vấn đề cốt lõi: AI tạo code nhanh hơn tốc độ con người có thể hiểu

### Workflow hiện tại

```
Developer
   ↓
Prompt
   ↓
AI Agent
   ↓
5,000 LOC
   ↓
Pull Request
   ↓
Human Review
   ↓
Merge
```

### AI tối ưu

```
Code generation
████████████████████  100x
```

Nhưng human:

```
Code understanding
████                  1x
```

> Đây chính là **bottleneck**.

Nếu AI tạo 10,000 dòng nhưng reviewer chỉ có 30 phút thì không thể review 10,000 dòng với cùng mức độ attention.

Vấn đề không phải:

> AI không biết viết code.

Mà là:

> **Con người không còn đủ bandwidth để hiểu code AI vừa tạo.**

---

## 2. Đừng xây "AI Code Reviewer"

Thị trường đã có quá nhiều:

- AI PR Review
- AI Code Review
- AI Bug Detection
- AI Security Review

Nếu framework của chúng ta chỉ làm:

> *"Tôi đọc PR và cho bạn 10 comments."*

→ **không đủ khác biệt.**

Tôi sẽ định nghĩa product là:

### 🔑 Human Attention Engine

Nó trả lời:

> *"Trong 10,000 dòng code này, con người cần dành sự chú ý vào **200 dòng nào**?"*

Đây là sự khác biệt rất lớn.

---

## 3. Ví dụ cụ thể

### AI tạo PR

**PR #1829**

- `12,481 lines changed`
- `243 files changed`

### Reviewer mở GitHub

```
Files changed
────────────────────

+1,231 lines
+892 lines
+421 lines
...
```

Con người nhìn vào:

> 😵

### Framework của chúng ta intercept PR

```
┌─────────────────────────────────────┐
│ AI Change Intelligence               │
├─────────────────────────────────────┤
│                                     │
│ 12,481 lines changed                │
│                                     │
│ Semantic changes: 17                │
│ Critical changes: 3                 │
│ High-risk changes: 6               │
│ Mechanical changes: 8,421          │
│                                     │
│ Human attention required:           │
│ ~180 lines                          │
│                                     │
│ Review reduction: 98.5%             │
└─────────────────────────────────────┘
```

> Đây mới là **product**.

---

## 4. Nó phải "compress" PR theo semantic meaning

### Ví dụ AI tạo

```
+ import PaymentService
+ import PaymentRepository
+ import PaymentValidator
+ import PaymentLogger
...
+ 1,500 lines
```

### Traditional review

> đọc **1,500 dòng**.

### Human Attention Engine

---

**Semantic Change #1**

- **Payment flow introduced**
- **Impact:** `HIGH`
- **Review:** `PaymentService.processPayment()`
- **Reason:** Changes financial state.

---

**Semantic Change #2**

- **New validation layer**
- **Impact:** `MEDIUM`
- **Review:** `PaymentValidator.validate()`
- **Reason:** Changes which payments are accepted.

---

**Semantic Change #3**

- **Refactoring**
- **Impact:** `LOW`
- **Review:** No business behavior change detected.

---

Reviewer không còn review:

```
file
```

mà review:

```
meaningful change
```

---

## 5. Tôi sẽ chia PR thành 4 loại

### A. Mechanical

- formatting
- rename
- generated types
- imports
- boilerplate
- lock files

> → **Don't spend human attention**

### B. Structural

- new component
- new service
- new abstraction
- new dependency

> → **Light review**

### C. Behavioral

- business logic
- validation
- state transition
- API behavior
- database behavior

> → **Deep review**

### D. Critical

- authentication
- authorization
- payment
- financial calculation
- data deletion
- production infrastructure
- security

> → **Mandatory human review**

---

## 6. Attention Score

Đây là một primitive quan trọng.

Mỗi change có:

### 🔢 Attention Score

Ví dụ:

```
Payment calculation
██████████████████ 94

Auth middleware
████████████████ 87

Database migration
██████████████ 81

UI component
██████ 36

Type definition
██ 12

Formatting
░ 1
```

> **Nhưng score không đơn giản dựa vào số dòng.**

Ví dụ:

```js
amount = price * quantity;
```

chỉ **1 dòng** — nhưng:

> **Business impact = cực kỳ cao.**

Ngược lại:

> `2,000 lines generated types`

có thể gần như:

> **zero human attention.**

Đây là điểm rất quan trọng.

---

## 7. Attention Score nên được tính từ nhiều chiều

### Ví dụ công thức

```
Attention Score =
    Business Impact
  × Change Risk
  × Uncertainty
  × Dependency Impact
  × AI Confidence
  × Historical Risk
```

Không nhất thiết phải dùng đúng công thức này, nhưng architecture có thể có các dimensions:

### Business Criticality

| Domain | Score |
|--------|-------|
| Payment | 10 |
| Authentication | 10 |
| Profile | 3 |
| UI animation | 1 |

### Change Type

| Type | Level |
|------|-------|
| Financial logic | HIGH |
| API contract | HIGH |
| DB migration | HIGH |
| Refactoring | LOW |
| Formatting | VERY LOW |

### Dependency Blast Radius

| Consumers | Risk |
|-----------|------|
| 1 consumer | LOW |
| 10 consumers | MEDIUM |
| 100 consumers | HIGH |

### Historical Failure

> Nếu đoạn code này trước đây thường gây bug → **Risk ↑**

### AI Confidence

AI agent nói:

> *"I am 95% confident."*

không nên được tin tuyệt đối — nhưng có thể dùng như một **signal**.

---

## 8. Quan trọng hơn: "Why should I care?"

### Reviewer click

```
PaymentService.ts
```

### Framework

```
WHY THIS MATTERS

This change modifies:

1. Payment authorization
2. Retry behavior
3. Transaction state

Affected:
- Checkout
- Refund
- Invoice

Historical:
3 incidents involved this module.

Required attention:
HIGH
```

> Reviewer không cần tự tìm context.
> **Context được đưa đến reviewer.**

---

## 9. Context Assembly

Đây có thể là phần LLM mạnh nhất.

Khi reviewer nhìn:

```js
calculateTotal()
```

thay vì chỉ show:

```js
function calculateTotal(...) {}
```

framework tự assemble:

```
┌─────────────────────────────────┐
│ calculateTotal()                │
├─────────────────────────────────┤
│ Called by: 7 services           │
│                                 │
│ Business rule:                 │
│ Order total = items + tax       │
│                                 │
│ Changed behavior:              │
│ Tax calculation moved earlier  │
│                                 │
│ API impact:                    │
│ POST /checkout                 │
│                                 │
│ Tests affected: 4              │
│                                 │
│ Previous incidents: 2          │
└─────────────────────────────────┘
```

> Reviewer có **context đúng lúc**.
> Đây là *"attention optimization"*.

---

## 10. Một tính năng rất mạnh: Review Queue

### Thay vì

```
PR
 ↓
Files
 ↓
Human đọc từ trên xuống
```

### Framework tạo

```
Review Queue

1. 🔴 Payment calculation
2. 🔴 Auth middleware
3. 🟠 DB migration
4. 🟠 API contract
5. 🟡 Cache behavior
6. 🟢 UI changes
7. ⚪ Generated types
```

### Reviewer xử lý

```
Review #1
↓
Review #2
↓
Review #3
↓
Approve
```

> Đây gần giống: **task scheduler cho human attention.**

---

## 11. Một bước rất thú vị: Progressive Disclosure

> Không nên đập toàn bộ code vào mặt reviewer.

```
Level 1: What changed?
   ↓
Level 2: Why does it matter?
   ↓
Level 3: What behavior changed?
   ↓
Level 4: Show relevant code.
   ↓
Level 5: Show supporting context.
   ↓
Level 6: Open full diff.
```

Tức là:

```
Summary
   ↓
Semantic change
   ↓
Risk
   ↓
Context
   ↓
Code
```

> Human chỉ đi sâu khi cần.

---

## 12. Đây cũng giải quyết vấn đề "AI PR quá lớn"

### Ví dụ PR size

```
100 LOC
500 LOC
5,000 LOC
50,000 LOC
```

> Không nên có rule: `PR > 500 LOC = bad.`

Bởi AI có thể generate:

```
20,000 LOC
```

nhưng semantic change chỉ là:

```
3 business decisions
```

### Framework nói

```
20,000 LOC
Semantic complexity:   LOW
Human review:          ~12 minutes
```

### Ngược lại

```
150 LOC
Semantic complexity:   VERY HIGH
Human review:          ~60 minutes
```

> Đây là metric mới: **Semantic Review Complexity.**
> Tôi rất thích concept này.

---

## 13. Một metric có thể trở thành core của framework: Human Review Load

### Ví dụ

**PR #1829**

| Metric | Value |
|--------|-------|
| Lines changed | 12,481 |
| Files | 243 |
| Semantic changes | 17 |
| Critical changes | 3 |
| **Review Load** | **42 minutes** |
| Confidence | 91% |

### Sau một thời gian team có

```
Human Review Load / PR
```

thay vì:

```
LOC / PR
```

> Đây là một metric phù hợp với **AI-native development** hơn LOC.

---

## 14. Framework có thể học từ reviewer

Đây là phần cực hay.

### Reviewer

```
AI marked this HIGH.
Human: Not important.
```

hoặc:

```
AI marked this LOW.
Human: Actually critical.
```

### Framework học

```
Reviewer behavior
        ↓
Attention model
        ↓
Team-specific calibration
```

### Ví dụ

| Team | Pattern | Mức độ |
|------|---------|--------|
| Team Payment | payment calculation | → extremely high |
| Team UI | animation | → low |
| Team Security | auth middleware | → critical |

> Nó trở thành: **Team-specific Human Attention Model.**

---

## 15. Và cuối cùng: AI không được tự approve

Đây là triết lý rất quan trọng.

Framework không nói:

> *"AI says it's safe → merge."*

Ngược lại:

```
AI
 ↓
Analyze
 ↓
Compress
 ↓
Prioritize
 ↓
Explain
 ↓
Human
 ↓
Approve / Reject
```

> AI **không thay thế reviewer.**
> AI giúp reviewer sử dụng **attention hiệu quả hơn**.

---

## 16. Tôi sẽ biến nó thành một framework như thế này

### Tên tạm

> **ReviewLens**

### CLI

```bash
reviewlens analyze
```

### Output

```
ReviewLens
────────────────────────────

PR #1829

12,481 LOC changed
243 files

Semantic Changes        17
Critical                 3
High                     6
Medium                   5
Low                      3

Human Review Load
████████░░ 42 min

Estimated without ReviewLens:
4h 32m

Attention reduction:
84%
```

### Sau đó

```bash
reviewlens review
```

mở UI:

```
┌─────────────────────────────────────────────┐
│ REVIEW QUEUE                                │
├─────────────────────────────────────────────┤
│                                             │
│ 🔴 Payment calculation              94      │
│ 🔴 Auth middleware                  89      │
│ 🔴 DB migration                     86      │
│                                             │
│ 🟠 Retry behavior                   72      │
│ 🟠 API contract                     68      │
│                                             │
│ 🟢 Generated types                  11      │
│ 🟢 Formatting                       2       │
│                                             │
└─────────────────────────────────────────────┘
```

### Click vào một item

```
Payment calculation
────────────────────────────

WHAT CHANGED
Tax calculation moved before discount.

WHY IT MATTERS
Changes final invoice amount.

AFFECTED
Checkout
Invoice
Refund

RISK
94 / 100

RECOMMENDED REVIEW
payment/calculator.ts:42-61

RELATED
PR #1821
INC-291
Test: payment-tax.spec.ts
```

---

## 17. Và nó không nhất thiết chỉ dành cho PR

Đây là chỗ tôi nghĩ framework có thể lớn lên.

### Có 4 mode

```
              ReviewLens
                  │
    ┌─────────────┼─────────────┐
    ↓             ↓             ↓
  IDE            PR          Commit
    │             │             │
    ↓             ↓             ↓
Live Review   Human Review   Pre-commit
```

### Thậm chí

```
AI Agent
   ↓
Generate code
   ↓
ReviewLens
   ↓
Semantic analysis
   ↓
Human attention map
   ↓
Developer review
   ↓
Git
```

---

## 18. Và đây mới là thesis tôi nghĩ rất mạnh

Không phải:

> *"AI writes code."*

Mà:

> **"AI has made code generation abundant. Human attention is now the scarce resource."**

### Từ đó

**Traditional Software Engineering**

| Resource | Status |
|----------|--------|
| CPU | scarce |
| Memory | scarce |
| Network | scarce |
| Developer | scarce |

**AI Software Engineering**

| Resource | Status |
|----------|--------|
| Code | abundant |
| PRs | abundant |
| Changes | abundant |
| Agents | abundant |

```
Human attention
      ↓
    SCARCE
```

### Vậy framework của bạn không phải là

> AI Code Reviewer.

### Nó là

> 🏗️ **Human Attention Infrastructure for AI-Native Software Development**

---

## 🚀 Hướng prototype thực tế

Và tôi nghĩ đây là một hướng đáng prototype thật, đặc biệt nếu bắt đầu cực nhỏ:

```
GitHub PR
   ↓
Diff
   ↓
Semantic Change Detection
   ↓
Risk Classification
   ↓
Review Queue
   ↓
Human
```

> Chưa cần agent, chưa cần memory, chưa cần knowledge graph, chưa cần RAG phức tạp.

### MVP chỉ cần chứng minh một câu

> **"Một PR 10,000 dòng do AI tạo ra — tôi có thể chỉ cho developer 100 dòng thực sự cần họ đọc."**

Nếu chứng minh được câu này bằng benchmark thực tế, lúc đó chúng ta mới có cơ sở mở rộng thành framework lớn.