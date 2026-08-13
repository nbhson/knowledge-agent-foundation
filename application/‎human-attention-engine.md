# 🧠 Human Attention Engine

> Trong kỷ nguyên AI tạo code, **human attention** (sự chú ý của con người) chính là tài nguyên khan hiếm nhất.

## 1. Vấn đề: AI tạo code nhanh, nhưng con người là bottleneck

AI tối ưu tốc độ generation:
```
Code generation
████████████████████  100x
```

Nhưng khả năng con người hiểu code:
```
Code understanding
████                  1x
```

> Đây chính là **bottleneck**. Con người không còn đủ bandwidth để hiểu hết code AI tạo ra.

## 2. Định nghĩa: Human Attention Engine

Đừng xây "AI Code Reviewer" (chỉ đưa ra comment thông thường), hãy xây **Human Attention Engine**.

Nó trả lời câu hỏi:
> *"Trong 10,000 dòng code này, con người cần dành sự chú ý vào **200 dòng nào**?"*

### Cách framework hoạt động (Intercept PR)
```
┌─────────────────────────────────────┐
│ AI Change Intelligence              │
├─────────────────────────────────────┤
│ 12,481 lines changed                │
│                                     │
│ Semantic changes: 17                │
│ Critical changes: 3                 │
│ High-risk changes: 6                │
│ Mechanical changes: 8,421           │
│                                     │
│ Human attention required: ~580 lines│
│ Review reduction: 95.35%            │
└─────────────────────────────────────┘
```

> Đây mới là **product** mang lại giá trị khác biệt.

## 3. Cách tiếp cận: Phân loại & Ưu tiên
Hệ thống sử dụng **Semantic Compression** để nén PR và đánh giá điểm **Attention Score** dựa trên:

### Phân loại Thay đổi
- **Mechanical** (formatting, rename, imports): Tự động bỏ qua.
- **Structural** (new component, dependency): Review nhẹ.
- **Behavioral** (logic, API, DB): Review sâu.
- **Critical** (payment, auth, security): Bắt buộc review kỹ.

#### A. Mechanical

- formatting
- rename
- generated types
- imports
- boilerplate
- lock files

> → **Don't spend human attention**

#### B. Structural

- new component
- new service
- new abstraction
- new dependency

> → **Light review**

#### C. Behavioral

- business logic
- validation
- state transition
- API behavior
- database behavior

> → **Deep review**

#### D. Critical

- authentication
- authorization
- payment
- financial calculation
- data deletion
- production infrastructure
- security

> → **Mandatory human review**

### Công thức Attention Score (Gợi ý)
`Attention Score = Business Impact × Change Risk × AI Confidence`

## 4. Trải nghiệm người dùng (Workflow mới)

### Review Queue (Task Scheduler cho Human Attention)

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

Reviewer xử lý:
```
Review #1 → Review #2 → Review #3 → Approve
```

### Context Assembly
Framework tự assemble thông tin context thay vì bắt reviewer tìm kiếm:
```
┌─────────────────────────────────┐
│ calculateTotal()                │
├─────────────────────────────────┤
│ Called by: 7 services           │
│ Business rule: Order total      │
│ Changed behavior: Tax moved     │
│ API impact: POST /checkout      │
└─────────────────────────────────┘
```
> Reviewer có **context đúng lúc**. Đây là *"attention optimization"*.

### Progressive Disclosure
> Không nên đập toàn bộ code vào mặt reviewer.

```
Summary → Semantic change → Risk → Context → Code
```
> Human chỉ đi sâu khi cần.

## 5. Metric cốt lõi: Semantic Review Complexity
Thay vì dùng `LOC/PR`, hãy dùng `Semantic Review Complexity` hoặc `Human Review Load (minutes/PR)` để đo lường hiệu suất thực tế của team trong kỷ nguyên AI-native.

## 6. Hướng Prototype (MVP)
MVP cần chứng minh: **"Với một PR 10,000 dòng do AI tạo ra, tôi có thể chỉ ra chính xác 100 dòng thực sự cần developer review."**

**Các bước MVP:**
1. Parse Diff từ GitHub PR.
2. Detection: Phân loại các Semantic Changes.
3. Classification: Tính toán mức độ Risk.
4. Output: Tạo Review Queue cho người dùng.
