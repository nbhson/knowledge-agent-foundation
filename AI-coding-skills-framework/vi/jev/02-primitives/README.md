# 🧩 02. Ba Primitives — Choice, Score, Noul

> Phần này đi sâu vào **ba question types (primitives)** của Jev — **Choice**, **Score**, **Noul** — cùng **cấu trúc request**, cách **đánh giá song song**, và **bảng chọn đúng primitive**. Đọc [01-concepts](../01-concepts/) trước nếu bạn chưa nắm Jev là gì.

---

## 1. Cấu Trúc Request

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Mọi request Jev có dạng `{model, state, questions}` — **state** là material (string / JSON / array of text), **questions** là named map các typed questions. Mỗi question là một trong ba primitive: **Choice** (chọn 1 từ closed set), **Score** (điểm trên ordinal scale), **Noul** (yes/no).
> **Ẩn dụ/so sánh:** Giống **bài thi trắc nghiệm**: state là **đề bài**, questions là **các câu hỏi** (mỗi câu có format trả lời riêng), và Jev **chấm hết một lần**, trả phiếu điểm kèm **phân phối xác suất** cho từng câu.
> **Vì sao quan trọng:** Ba primitive phủ **gần như mọi quyết định nhỏ** trong workflow. Hiểu đúng từng loại — cái nó trả về, cái nó *không* trả về — là nền tảng để viết threshold và route đúng.

### 1.1 Bảng Tổng Hợp Ba Primitive

```
┌───────────┬────────────────────────────┬─────────────────────────────────────┐
│ Primitive │ Purpose                    │ Returns                             │
├───────────┼────────────────────────────┼─────────────────────────────────────┤
│  Choice   │ Pick 1 từ closed set       │ selected option                     │
│           │ bạn định nghĩa             │ + full probability distribution      │
│           │ (≤ 255 options)            │ + confidence                        │
├───────────┼────────────────────────────┼─────────────────────────────────────┤
│  Score    │ Ordered scale 2-10 levels  │ probability-weighted score           │
│           │ bạn mô tả                  │ (CÓ THỂ nằm GIỮA 2 levels)          │
│           │                            │ + per-level probabilities            │
│           │                            │ + confidence                        │
├───────────┼────────────────────────────┼─────────────────────────────────────┤
│  Noul     │ Yes/no proposition         │ probability of yes ∈ [0, 1]          │
│           │                            │ + certainty INTRINSIC (margin)       │
│           │                            │ — KHÔNG có confidence riêng          │
└───────────┴────────────────────────────┴─────────────────────────────────────┘
```

### 1.2 Request Skeleton

```
POST /v1/systemone
{
  "model":   "jev-latest",
  "state":   "…string / JSON / array of text…",
  "questions": {
    "<tên1>": { …primitive 1… },
    "<tên2>": { …primitive 2… },
    "<tên3>": { …primitive 3… }
  }
}
```

Tất cả questions được evaluate **song song trong 1 pass** — xem §5.

---

## 2. Choice — Chọn Một Từ Closed Set

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Choice cho Jev chọn **đúng 1 option** từ tập **bạn đóng lại** (tối đa **255 options**), và trả về **selected option + full probability distribution + confidence**. Answer space đóng → không thể trả về thứ ngoài danh sách.
> **Ẩn dụ/so sánh:** Giống **menu nhà hàng**: khách không thể gọi món không có trong menu — dù họ "muốn" món gì đó khác, nhà hàng chỉ trả về **một món trong menu** kèm xác suất của **tất cả các món**. Menu là schema của bạn.
> **Vì sao quan trọng:** Choice là primitive phổ biến nhất: routing, classification, intent detection, team assignment... Full distribution (không chỉ top-1) cho phép **route hai nhánh** hoặc **kết hợp nhiều model**, confidence cho biết **khi nào tin top-1**.

### 2.1 Cách Hoạt Động

```
Bạn ĐỊNH NGHĨA closed set:   ["billing", "tech", "account", "other"]
                                    │
state + question ──────────────────┤
                                    ▼
Jev trả về:
{
  "choice":  "tech",                  ← selected option (luôn thuộc set)
  "probs":   { billing: 0.06,         ← FULL distribution
               tech:    0.87,
               account: 0.05,
               other:   0.02 },
  "confidence": 0.82                  ← độ tập trung của distribution
}
```

- **≤ 255 options** — đủ cho mọi taxonomy realisttic.
- **confidence ≠ P(đúng)**: với Choice/Score, confidence là **distribution tập trung到 mức nào** (peaked → cao, flat → thấp). Chi tiết: [04-calibration](../04-calibration/).

### 2.2 Khi Nào Thêm Option "Other"

```
Có "other":   taxonomy không bao phủ hết  → Jev có chỗ để "từ chối"
              nhưng other cao = signal taxonomy của bạn SAI — xem lại

Không "other": bạn CHẮC 100% state luôn rơi vào set
              (rare — thường chỉ khi set sinh từ code, không từ ngữ nghĩa)

Gợi ý TypeSafe: include "other" khi classifying text người dùng;
                omit khi routing giữa các nhánh workflow đã biết trước
```

### 2.3 Code Sample

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
import typesafe

client = typesafe.Client(api_key="...")

state = """
Ticket #4821: "I was charged twice for my Pro plan this month,
please refund the duplicate charge."
"""

resp = client.ask(
    model="jev-latest",
    state=state,
    questions={
        "team": {
            "type": "choice",
            "choices": ["billing", "tech", "account", "other"],
            "description": "Which team owns this ticket?",
        },
        "channel": {
            "type": "choice",
            "choices": ["self_serve", "human_agent", "callback"],
            "description": "Best resolution channel?",
        },
    },
)

team = resp.answers["team"]
print(team.choice)        # "billing"
print(team.confidence)    # 0.91  (distribution tập trung)
print(team.probabilities) # {"billing": 0.91, "tech": 0.05, ...}

# Dùng full distribution để route 2 nhánh nếu muốn:
p = team.probabilities
if p["billing"] > 0.6:
    route_billing_agent()
elif p["other"] > 0.3:
    escalate_human()      # other cao → taxonomy có vấn đề
else:
    route_generic_queue()
```

</details>

### 2.4 Liên Hệ Pydantic `Enum` / `Literal`

```
Pydantic:  team: Literal["billing", "tech", "account"]
           → model trả đúng literal (typed, closed)
Jev:       choice: [...]                       → trả đúng option (closed)
           + distribution + confidence           → bonus mà Literal không có

Ý nghĩa: Choice = Literal/KnownClass + CALIBRATED ODDS đi kèm.
         Bạn giữ typing của Pydantic, và có thêm threshold-based routing.
```

### 2.5 Ưu / Nhược

```
✅ Đúng 1 từ set — không thể sai type
✅ Full distribution → routing đa nhánh, "other"-detection
✅ ≤255 options đủ mọi taxonomy
❌ Bạn phải ĐỊNH NGHĨA set trước (không discover classes mới)
❌ Confidence ≠ probability of correctness (đọc [04-calibration])
```

---

## 3. Score — Điểm Trên Ordinal Scale

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Score để bạn định nghĩa **ordered scale từ 2 đến 10 levels**; Jev trả về **probability-weighted score** — một số **CÓ THỂ NẰM GIỮA hai level** (vd **1.4** giữa level 1 và 2) — kèm **per-level probabilities** và **confidence**. Score model hóa được **degree** mà Choice không model hóa được.
> **Ẩn dụ/so sánh:** Giống **thermometer**: bạn không hỏi "khách hàng đang nóng giận hay không?" (Choice) mà hỏi "nóng bao nhiêu?" — kim có thể dừng ở **36.7°C**, không phải chỉ ở các vạch khắc. Levels là vạch, score là kim.
> **Vì sao quan trọng:** Rất nhiều quyết định thực tế là **ordinal, không binary**: mức độ nghiêm trọng, mức độ khẩn cấp, chất lượng câu trả lời, nhiệt tình của khách. Ép chúng vào boolean mất đi đúng thông tin cần cho ngưỡng.

### 3.1 Cách Hoạt Động — Và Tại Sao Có Số Lẻ

```
Bạn ĐỊNH NGHĨA ordered scale (2-10 levels), ví dụ 3 levels:
  1 = calm
  2 = frustrated
  3 = very angry

Jev trả về:
{
  "score": 1.4,                    ← prob-weighted; NẰM GIỮA level 1 & 2
  "legend": { 1: "calm", 2: "frustrated", 3: "very angry" },
  "distribution": { 1: 0.72, 2: 0.24, 3: 0.04 },
  "confidence": 0.68
}

ĐỌC 1.4: người dùng phần lớn "calm" (0.72) nhưng có tín hiệu
         nghiêng nhẹ về "frustrated" → score tụ về 1.4, không phải 1.
         Ép về int() sẽ MẤT thông tin này.
```

**Quy tắc**: score = kỳ vọng (expectation) của phân phối trên scale. Phân phối **một bên** → score gần integer; **phân tán giữa hai level** → score ở giữa. **Không bao giờ làm tròn blind** trước khi đọc distribution.

### 3.2 Bảng Thang Điển Hình

```
┌──────────────────────────┬─────────┬──────────────────────────────┐
│ Domain                   │ Levels  │ Legend (ví dụ)               │
├──────────────────────────┼─────────┼──────────────────────────────┤
│ Customer emotion         │ 3       │ calm → frustrated → angry    │
│ Ticket severity          │ 5       │ sev1 … sev5                  │
│ Urgency                  │ 4       │ low → med → high → critical  │
│ Answer quality (verify)  │ 3       │ bad → ok → good              │
│ Deal risk                │ 5       │ none → low → … → fatal       │
└──────────────────────────┴─────────┴──────────────────────────────┘
Nguyên tắc: 2-10 levels; giữ mô tả mỗi level SẮC (state là material,
không phải instructions — xem §6).
```

### 3.3 Code Sample

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
import typesafe

client = typesafe.Client(api_key="...")

state = """
Conversation snippet (support):
User: "This is the THIRD time this month. I've wasted two hours
on hold already. Fix it or I'm gone."
"""

resp = client.ask(
    model="jev-latest",
    state=state,
    questions={
        "urgency": {
            "type": "score",
            "levels": [
                {"level": 1, "label": "low"},
                {"level": 2, "label": "medium"},
                {"level": 3, "label": "high"},
                {"level": 4, "label": "critical"},
            ],
            "description": "Urgency of this conversation",
        },
    },
)

u = resp.answers["urgency"]
print(u.score)          # e.g. 3.4  (giữa high và critical)
print(u.distribution)   # {1: 0.01, 2: 0.04, 3: 0.52, 4: 0.43}
print(u.confidence)     # 0.58

# Threshold dựa trên score, không int() blind:
if u.score >= 3.5 and u.confidence > 0.5:
    page_oncall()               # critical + đủ tự tin
elif u.score >= 2.5:
    bump_priority_queue()
else:
    standard_queue()
```

</details>

---

## 4. Noul — Yes / No

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Noul nhận một **proposition** và trả về **probability of yes ∈ [0, 1]**. **Certainty là intrinsic** — không có confidence field riêng: certainty chính là **margin = |p − 0.5| × 2**. (False trả lời từ p=0.01 báo **0.98** certainty; từ p=0.45 chỉ báo **0.10**.)
> **Ẩn dụ/so sánh:** Giống **một công tắc analog thay vì digital** — không chỉ "bật/tắt", mà *"bật bao nhiêu phần trăm"*. p=0.5 là công tắc **ở giữa**, không phải *"medium"*.
> **Vì sao quan trọng:** Noul là primitive của **gates và verification** — "ticket này có refund không?", "output này có vi phạm policy không?". Margin cho bạn **ngưỡng hành động** mà không cần confidence phụ: `p` xa 0.5 → act, gần 0.5 → escalate.

### 4.1 Cách Hoạt Động — Và Bẫy "Medium"

```
Proposition (description của bạn):
  "Does this message request a refund?"

Jev trả về:
{
  "noul": false,
  "p": 0.03,          ← probability of YES = 0.03 → near-certain NO
  "certainty": 0.94   ← |0.03 - 0.5| × 2 = 0.94
}

BA SỐ ĐỌC NHAU:
  p = 0.03   → almost certainly NO
  p = 0.45   → "khó nói" — CERTAINTY 0.10, KHÔNG PHẢI "medium confidence"
  p = 0.97   → almost certainly YES

⚠️ BÃY: gần 0.5 = CÂN BẰNG (gần như không biết), KHÔNG PHẢI "medium".
   Đừng map p≈0.5 vào nhánh "medium → ask confirm vì model khá chắc" —
   nó chắc chắn ở mức GẦN NHƯ KHÔNG BIẾT. Xử lý như low / escalate.
```

**Criteria yes/no tùy chọn**: bạn có thể thêm hướng dẫn tiêu chí trong question (khi nào tính là yes) — nhưng hãy nhớ **state là material, không phải prompt**: criteria rõ ràng nên nằm trong description của proposition, còn framing tổng quát nằm ở instructions (xem §6).

### 4.2 Công Thức Margin

```
certainty = |p − 0.5| × 2

p = 0.01 (False)  → certainty 0.98    ← cực tự tin NO
p = 0.45 (False)  → certainty 0.10    ← hầu như không biết
p = 0.50          → certainty 0.00    ← điểm mù hoàn toàn
p = 0.55 (True)   → certainty 0.10    ← hầu như không biết
p = 0.99 (True)   → certainty 0.98    ← cực tự tin YES

So với Choice/Score: confidence = độ tập trung của distribution.
Noul:                  certainty   = margin khỏi 0.5 (intrinsic).
```

### 4.3 Dùng Cho Gate / Verify

```
                state (hoặc LLM output)
                        │
                        ▼
              Noul: "Passes policy?"
                        │
        ┌───────────────┼────────────────┐
        ▼               ▼                ▼
   p ≥ 0.85        0.6 ≤ p < 0.85      p < 0.6
   CERTAIN YES     leaning             uncertain
        │               │                │
        ▼               ▼                ▼
  auto-APPROVE    ask confirm /      REJECT or
  (code acts)     more context       escalate human
```

### 4.4 Code Sample

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
import typesafe

client = typesafe.Client(api_key="...")

llm_output = """Sure! I'll just go ahead and delete all user
records to free up space. No backup needed here."""

resp = client.ask(
    model="jev-latest",
    state=llm_output,
    questions={
        "destructive": {
            "type": "noul",
            "description": (
                "Does this proposed action irreversibly destroy "
                "production data without backup?"
            ),
        },
        "policy_ok": {
            "type": "noul",
            "description": "Is this output safe to ship to the user?",
        },
    },
)

d = resp.answers["destructive"]
p_yes = d.p                 # probability of YES
certainty = d.certainty     # |p - 0.5| * 2

if p_yes >= 0.85:
    block_and_escalate()    # almost-certainly destructive
elif abs(p_yes - 0.5) < 0.1:
    ask_human()             # margin ~0 → Jev gần như KHÔNG BIẾT
else:
    review_queue()
```

</details>

---

## 5. Đánh Giá Song Song

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Tất cả questions trong một request được evaluate **song song trong MỘT pass** — thêm question **gần như không đổi latency**, chỉ **thêm chi phí input tokens**. Đây là lever thiết kế quan trọng nhất của Jev.
> **Ẩn dụ/so sánh:** Giống **một sĩ quan đọc một hồ sơ rồi trả lời N câu hỏi trên nó cùng lúc** — anh ta không đọc lại hồ sơ cho từng câu. Thêm câu hỏi = thêm vài giây hỏi nhỏ, không phải thêm một lần đọc mới.
> **Vì sao quan trọng:** Trong thực tế, bạn nên **gom tất cả quyết định của một bước vào MỘT request** — 10 questions vẫn ~70-500ms, trong khi 10 requests tuần tự sẽ nhân latency.

### 5.1 Tại Sao Nhanh

```
WRONG (10 requests tuần tự):          RIGHT (1 request song song):
  req1 ──► 70-500ms                     ┌ q1 ┐
  req2 ──► 70-500ms                     ├ q2 ┤
  req3 ──► 70-500ms                     ├ .. ┤── 1 pass ──► 70-500ms
  ...                                   ├ q9 ┤   (tất cả
  req10 ─► 70-500ms                     └ q10┘    song song)
  ≈ 10 × latency
```

- **Latency**: gần như bất biến với số question (chỉ thêm marginal cost).
- **Chi phí**: tăng tuyến tính với **input tokens** ($0.042/M) — output free.
- **Thiết kế**: gom nhiều quyết định cùng state vào 1 request = tối ưu cả hai.

### 5.2 Fan-Out Danh sách (List → Nhiều Option / Nhiều Noul)

```
State = mảng items (rows, messages, docs):
  state = [item_1, item_2, ..., item_n]

Cách 1 — ONE request, questions per item (khi n vừa phải):
  questions = { f"classify_{i}": choice(...) for i in range(n) }
  → 1 pass, song song, 1 lần trả

Cách 2 — batch nhiều request (khi n rất lớn — map-reduce):
  chunks of items ──► N requests song song ──► aggregate answers
  → xem [05-patterns](../05-patterns/) workload #2
```

### 5.3 Nested Fields (`outer.inner`)

```
State JSON:
{
  "ticket": { "body": "...", "channel": "email", "history": [...] },
  "user":   { "tier": "pro", "tenure_days": 400 }
}

Questions có thể nhắm field con bằng dotted name:
  questions = {
    "ticket.body.toxic":      noul(...),
    "user.tier.plan_choice":  choice(...),
  }

→ Jev đọc state cấu trúc, trả answers theo tên bạn đặt.
   Dùng dotted name để answers tự map về đúng đường dẫn
   khi bạn unpack vào code.
```

---

## 6. Chọn Đúng Primitive

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Bảng quyết định: **routing / classification → Choice**; **ordinal rating / mức độ → Score**; **boolean gate / verify → Noul**. Và best practice TypeSafe: **câu hỏi đặt trên field / output type, framing đặt trên instructions** — **đừng nhét question vào prompt**; state chỉ là **material để judged**, không phải chỗ gõ hướng dẫn cho model.
> **Ẩn dụ/so sánh:** Giống **phán của toà**: state là **hồ sơ vụ án** (material), question là **câu hỏi thẩm phán hỏi**, và **không ai viết hướng dẫn "hãy trả lời theo hướng này" vào giữa hồ sơ** — hướng dẫn (instructions) nằm ở **quy trình tố tụng** riêng.
> **Vì sao quan trọng:** Nhét instructions vào state làm **bẩn material** → accuracy giảm (state hygiene, xem [07-limits](../07-limits-and-evaluation/)). Đặt đúng chỗ → questions sắc, framing nhất quán, answers dễ map về typed output.

### 6.1 Bảng Quyết Định

```
┌───────────────────────────────┬────────────┬───────────────────────────┐
│ Bạn cần...                    │ Primitive  │ Ví dụ                     │
├───────────────────────────────┼────────────┼───────────────────────────┤
│ Chọn 1 giữa vài nhánh        │ CHOICE     │ team routing, intent,     │
│ (taxonomy đã đóng)            │            │ channel selection, plan  │
├───────────────────────────────┼────────────┼───────────────────────────┤
│ Thang ordinal / rating /      │ SCORE      │ severity, urgency,        │
│ mức độ (2-10 levels)          │            │ sentiment degree, quality │
├───────────────────────────────┼────────────┼───────────────────────────┤
│ Yes/no, gate, verify,         │ NOUL       │ policy pass?, refund      │
│ có/không                      │            │ requested?, safe to ship? │
└───────────────────────────────┴────────────┴───────────────────────────┘

Nghịch lý nhỏ: "bao nhiêu mức vui vẻ?" → SCORE, không phải
choice(vui/vừa/buồn) — vì bạn muốn PHÂN PHỐI, không chỉ nhãn.
```

### 6.2 TypeSafe Best Practice — Đâu Là Câu Hỏi, Đâu Là Framing

```
┌──────────────────────────────────────────────────────────────────────┐
│  state          = MATERIAL để judged (dữ liệu, ví dụ, hồ sơ)        │
│                   → sạch, relevant, không instructions               │
│                                                                      │
│  question       = NGAY TRÊN field / output type của bạn              │
│  description    = chính là CÂU HỎI ("Which team owns this?")        │
│                   → đây là "concept quan trọng nhất":               │
│                     câu hỏi sống trên TYPE, không sống trong prompt │
│                                                                      │
│  instructions   = FRAMING (bối cảnh, tiêu chí chung, tone)          │
│                   → đặt ở instruction level của request/model,       │
│                     áp cho tất cả questions trong frame đó           │
└──────────────────────────────────────────────────────────────────────┘

❌ SAI (thói quen prompting):
   state = "Bạn là bộ phân loại ticket. Hãy trả lời: team nào?
            Nếu khó hãy chọn other. [RỒI MỚI] Ticket #4821: ..."

✅ ĐUNG:
   state        = "Ticket #4821: I was charged twice ..."
   questions.team.description = "Which team owns this ticket?"
   questions.team.choices     = ["billing", "tech", "account", "other"]
   instructions = "Classify by primary owning team, not first mention."
```

> **Quy tắc tóm tắt**: *Put the question on the type. Put the framing in the instructions. Keep the state as material.* Đây cũng là mô hình **output_type → questions** mà Pydantic AI `TypeSafeModel` tự động hoá — xem [03-api](../03-api/) §4.

### 6.3 Checklist Chọn Primitive

```
□ Đáp án có ĐÓNG trước không?          → không → LLM (xem 06-jev-and-llm)
□ Đúng 1 trong tập xác định?          → Choice
□ Có thứ tự / mức độ?                 → Score (2-10 levels, mô tả sắc)
□ Có phải nhị phân + cần margin?      → Noul
□ Cần "tại sao"?                      → không phải Jev — LLM / human
□ State có dính instructions thừa?    → dọn (state hygiene)
□ Gom được nhiều question 1 request?  → GOM (parallel, tiết kiệm latency)
```

---

*Tiếp theo: [03 — API & Tích Hợp](../03-api/)*

*Trở về [README](../README.md) — tổng quan Module XIV*
