# 🔌 03. API & Tích Hợp

> Phần này hướng dẫn **gọi Jev lần đầu**: endpoint & xác thực, cấu trúc **request/response** đầy đủ, **SDK chính thức**, và các integration — **Pydantic AI**, **LangChain**, **OpenRouter** — cùng **giới hạn & mã lỗi** thường gặp. Đọc [02-primitives](../02-primitives/) trước nếu bạn chưa rõ ba question types.

---

## 1. Endpoint & Xác Thực

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Jev expose **một endpoint duy nhất**: `POST https://api.typesafe.ai/v1/systemone`, xác thực bằng **Bearer API key**. Model version hiện tại là **jev-1.13.0**, dùng alias **jev-latest** để luôn nhận bản mới nhất.
> **Ẩn dụ/so sánh:** Giống **một function call trên cloud** — một URL, một key, một body JSON. Không streaming, không conversation, không multi-turn — mỗi request là **một lần decide độc lập**.
> **Vì sao quan trọng:** Bề mặt API nhỏ = integration nhanh. Nhưng cũng có nghĩa **stateless hoàn toàn** — bạn tự quản context (state) ở bên ngoài; xem [04-calibration](../04-calibration/) về state hygiene.

### 1.1 Cấu Trúc Endpoint

```
POST https://api.typesafe.ai/v1/systemone
Authorization: Bearer <TYPESAFE_API_KEY>
Content-Type: application/json

{
  "model":     "jev-latest",          ← hoặc "jev-1.13.0"
  "state":     "...",                 ← string / JSON object / array of text
  "questions": { ... }                ← named map of typed questions
}
```

```
┌──────────────────────────────────────────────────────────────┐
│  MODEL ALIASES                                               │
│                                                              │
│  jev-latest  ─────────►  jev-1.13.0   (alias, auto-roll)     │
│  jev-1.13.0  ─────────►  pin version (production: PIN!)      │
│                                                              │
│  Early access:   15/09/2026                                  │
│  Public:         20/09/2026 (no waitlist)                    │
└──────────────────────────────────────────────────────────────┘
```

### 1.2 Xác Thực

```
# Environment
export TYPESAFE_API_KEY="tsk_..."

# Header
Authorization: Bearer $TYPESAFE_API_KEY

# Lỗi xác thực thường gặp: 401 (sai key) / 403 (key không có scope)
```

> **Gợi ý production**: pin `jev-1.13.0` (không dùng alias) để tránh thay đổi âm thầm khi TypeSafe roll `jev-latest`; upgrade chủ động khi đọc changelog.

---

## 2. Request & Response

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Request = `{model, state, questions}`. **questions** là named map — mỗi key là **tên answer** bạn sẽ đọc về sau, mỗi value là một primitive (Choice / Score / Noul). Response trả về **`answers.<name>.<primitive>`** kèm probabilities và confidence — **tất cả questions trong 1 pass song song**.
> **Ẩn dụ/so sánh:** Như **phiếu trả lời có chấm tròn sẵn**: bạn in sẵn câu hỏi (questions), Jev tô đen đáp án (selected / score / p) và ghi **độ tập trung** bên cạnh. Bạn không "đọc văn bản trả lời" — bạn **đọc phiếu**.
> **Vì sao quan trọng:** Response shape cố định theo primitive → code unpack typed, không regex. Nhớ rằng thêm questions gần như **không đổi latency**, chỉ thêm input tokens ($0.042/M) — gom hết vào 1 request.

### 2.1 Ví Dụ Request Đầy Đủ — 3 Questions

```json
POST /v1/systemone
Authorization: Bearer tsk_...
{
  "model": "jev-latest",
  "state": {
    "ticket": {
      "id": 4821,
      "body": "I was charged twice for my Pro plan this month. I want a refund of the duplicate charge ASAP, I'm really frustrated.",
      "channel": "email",
      "history_count": 3
    },
    "account": { "tier": "pro", "tenure_days": 400 }
  },
  "questions": {
    "team": {
      "type": "choice",
      "choices": ["billing", "tech", "account", "other"],
      "description": "Which team owns this ticket?"
    },
    "refund_requested": {
      "type": "noul",
      "description": "Does the customer explicitly request a refund?"
    },
    "urgency": {
      "type": "score",
      "levels": [
        { "level": 1, "label": "low" },
        { "level": 2, "label": "medium" },
        { "level": 3, "label": "high" },
        { "level": 4, "label": "critical" }
      ],
      "description": "Urgency of handling this ticket"
    }
  }
}
```

### 2.2 Response Shape

```json
{
  "answers": {
    "team": {
      "choice": "billing",
      "probabilities": { "billing": 0.93, "tech": 0.04, "account": 0.02, "other": 0.01 },
      "confidence": 0.87
    },
    "refund_requested": {
      "noul": true,
      "p": 0.96,
      "certainty": 0.92
    },
    "urgency": {
      "score": 3.4,
      "legend": { "1": "low", "2": "medium", "3": "high", "4": "critical" },
      "distribution": { "1": 0.01, "2": 0.05, "3": 0.51, "4": 0.43 },
      "confidence": 0.55
    }
  },
  "usage": { "input_tokens": 214, "output_tokens": 0 }
}
```

### 2.3 Đọc Response — Bảng Map Sang Code

```
┌──────────────────┬──────────────────────────────┬───────────────────────┐
│ Field            │ Nghĩa                        │ Dùng trong code       │
├──────────────────┼──────────────────────────────┼───────────────────────┤
│ choice           │ option đã chọn               │ switch/route          │
│ probabilities    │ full distribution            │ multi-branch, other   │
│ confidence       │ độ tập trung distribution    │ threshold (Choice/    │
│                  │  (NOT P(đúng))               │  Score) — xem 04      │
├──────────────────┼──────────────────────────────┼───────────────────────┤
│ noul             │ boolean đã chọn              │ if/else               │
│ p                │ probability of YES (0-1)     │ threshold vs 0.5      │
│ certainty        │ |p-0.5|×2 (intrinsic)        │ gate margin           │
├──────────────────┼──────────────────────────────┼───────────────────────┤
│ score            │ prob-weighted (CÓ THỂ giữa   │ score >= x (KHÔNG     │
│                  │  2 levels, vd 3.4)           │  int() blind)         │
│ legend           │ label từng level             │ display / mapping     │
│ distribution     │ per-level probabilities      │ phân tích side-info   │
└──────────────────┴──────────────────────────────┴───────────────────────┘
```

### 2.4 Một Lần Gọi — Cả Ba Cùng Lúc (Minh Hoạ Parallel)

```
                        ┌── q "team.choice"         ──► choice + probs
state + 3 questions ────┼── q "refund_requested.noul" ──► noul + p
                        └── q "urgency.score"        ──► score + dist
                              │
                              └── 1 PASS SONG SONG ──► 70-500ms
```

---

## 3. SDK Chính Thức

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** TypeSafe phát hành **Python SDK** và **JavaScript SDK** chính thức — wrap cùng một endpoint, trả typed objects. Khi stack của bạn đã đi qua **OpenRouter** (một key nhiều model), bạn cũng có thể **đặt base URL của OpenRouter** và vẫn dùng SDK/TS SDK.
> **Ẩn dụ/so sánh:** Như **client HTTP có typed models** — bạn không tự map JSON; SDK trả object có attribute (`answer.choice`, `answer.p`) giống ORM.
> **Vì sao quan trọng:** SDK chuẩn hoá error handling và typing — tránh sai sót tay khi unpack response, nhất là khi bạn đọc `confidence` vs `certainty` cho từng primitive (nhầm hai khái niệm này là bug âm thầm nguy hiểm — [04-calibration](../04-calibration/)).

### 3.1 Quickstart

<details>
<summary>Python — Quickstart (Click to expand/collapse)</summary>

```python
# pip install typesafe
import os
import typesafe

client = typesafe.Client(api_key=os.environ["TYPESAFE_API_KEY"])

resp = client.ask(
    model="jev-1.13.0",                     # pin version trong production
    state="Ticket: charged twice, want refund, very frustrated.",
    questions={
        "team": {
            "type": "choice",
            "choices": ["billing", "tech", "account", "other"],
            "description": "Which team owns this ticket?",
        },
        "refund_requested": {
            "type": "noul",
            "description": "Does the customer explicitly request a refund?",
        },
        "urgency": {
            "type": "score",
            "levels": [
                {"level": 1, "label": "low"},
                {"level": 2, "label": "medium"},
                {"level": 3, "label": "high"},
                {"level": 4, "label": "critical"},
            ],
            "description": "Urgency of handling this ticket",
        },
    },
)

team = resp.answers["team"]
if team.confidence > 0.7 and team.choice != "other":
    route(team.choice)
else:
    escalate_human(team.probabilities)

refund = resp.answers["refund_requested"]
if refund.p >= 0.85:
    open_refund_flow()
elif abs(refund.p - 0.5) < 0.1:
    ask_human()          # margin nhỏ → Jev gần như không biết

urgency = resp.answers["urgency"]
if urgency.score >= 3.5:
    page_oncall()
```

</details>

<details>
<summary>JavaScript — Quickstart (Click to expand/collapse)</summary>

```javascript
// npm install @typesafe/sdk
import { TypeSafe } from "@typesafe/sdk";

const client = new TypeSafe({ apiKey: process.env.TYPESAFE_API_KEY });

const resp = await client.ask({
  model: "jev-1.13.0",
  state: "Ticket: charged twice, want refund, very frustrated.",
  questions: {
    team: {
      type: "choice",
      choices: ["billing", "tech", "account", "other"],
      description: "Which team owns this ticket?",
    },
    refund_requested: {
      type: "noul",
      description: "Does the customer explicitly request a refund?",
    },
    urgency: {
      type: "score",
      levels: [
        { level: 1, label: "low" },
        { level: 2, label: "medium" },
        { level: 3, label: "high" },
        { level: 4, label: "critical" },
      ],
      description: "Urgency of handling this ticket",
    },
  },
});

const team = resp.answers.team;
console.log(team.choice, team.confidence, team.probabilities);
```

</details>

### 3.2 Đổi Base URL Sang OpenRouter

```
# Khi stack đã có OpenRouter key — dùng lại SDK, chỉ đổi base URL
TYPESAFE_API_KEY=<openrouter_key>
TYPESAFE_BASE_URL=https://openrouter.ai/api/alpha

# → SDK gọi /decisions trên OpenRouter thay vì api.typesafe.ai
# Model name: "typesafe/jev-1.13" (xem §6)
```

---

## 4. Pydantic AI — TypeSafeModel

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Pydantic AI tích hợp Jev qua **`TypeSafeModel`**: **mỗi field của `output_type` trở thành một question** cho Jev; **`field description` = text câu hỏi**; **`docstring`/`instructions` = framing**. Output là Pydantic object typed — không sinh text, không parse.
> **Ẩn dụ/so sánh:** Giống **biến dataclass thành phiếu hỏi**: mỗi annotation (`team: str`) là một ô tròn Jev phải tô; description là đề bài cho ô đó; docstring là hướng dẫn chung cho cả bài.
> **Vì sao quan trọng:** Đây là mô hình **NGƯỢC thói quen prompting** — câu hỏi sống trên **type**, không sống trong prompt string. TypeSafe gọi đây là *concept quan trọng nhất* của integration: **put the question on the field, not in the prompt**. (Tương ứng best practice §6 ở [02-primitives](../02-primitives/).)

### 4.1 Mapping output_type → Questions

```
┌───────────────────────────────┬──────────────────────────────────────┐
│ Pydantic AI                   │ Jev                                  │
├───────────────────────────────┼──────────────────────────────────────┤
│ Mỗi field của output_type     │ → MỘT question                      │
│ field description             │ → câu hỏi text (description)        │
│ docstring / instructions      │ → framing cho toàn bộ request       │
│ field type (Enum/Literal/bool)│ → primitive tương ứng               │
│   bool                        │   → Noul                            │
│   Literal / Enum              │   → Choice (closed set)             │
│   int/float w/ levels         │   → Score                           │
│ list[field]                   │ → FAN-OUT: mỗi phần tử 1 question   │
│ nested model                  │ → nested question (outer.inner)     │
└───────────────────────────────┴──────────────────────────────────────┘
```

### 4.2 Ví Dụ

<details>
<summary>Python — TypeSafeModel (Click to expand/collapse)</summary>

```python
from enum import Enum
from pydantic import BaseModel, Field
from pydantic_ai import Agent
from pydantic_ai.models.typesafe import TypeSafeModel

class Team(str, Enum):
    BILLING = "billing"
    TECH = "tech"
    ACCOUNT = "account"
    OTHER = "other"

class Triage(BaseModel):
    """Classify by the PRIMARY owning team, not the first mention."""

    team: Team = Field(
        description="Which team owns this ticket?"     # ← câu hỏi
    )
    refund_requested: bool = Field(
        description="Does the customer explicitly request a refund?"
    )
    urgency: int = Field(
        description="Urgency of handling this ticket",
        # score levels do TypeSafeModel map từ schema/config
    )

agent = Agent(TypeSafeModel("jev-1.13.0"), output_type=Triage)

result = agent.run_sync(
    "Ticket #4821: charged twice, want refund, very frustrated."
)
print(result.output.team)             # Team.BILLING — typed, closed
print(result.output.refund_requested) # True
```

</details>

### 4.3 Các Trường Hợp Đặc Biệt

```
1. LIST FAN-OUT
   items: list[ItemDecision]     → mỗi phần tử = 1 question
   → gom fan-out vào 1 pass (xem 02-primitives §5.2)

2. NESTED MODELS
   class Out(BaseModel):
       ticket: TicketDecision    → questions nhắm ticket.*
       (dotted: "ticket.team" v.v.)

3. INSTRUCTIONS CHO SINGLE QUESTION
   framing dùng chung đặt ở agent instructions;
   câu hỏi cụ thể đặt ở field description — không trộn lẫn

4. ⚠️ UserError: bool trần không có field description
   urgent: bool            ← KHÔNG có description → UserError
   urgent: bool = Field(
       description="Is this urgent?"   ← BẮT BUỘC với bool
   )
   Lý do: bool → Noul = một proposition; không description =
   không proposition để Jev chấm. Đây là guardrail cố ý.
```

### 4.4 Tools Kèm Theo — Tool-Call Threshold

```
┌──────────────────────────────────────────────────────────────────────┐
│  Khi agent ĐÍNH kèm tools, MỌI request mang thêm 1 question:        │
│    "which of these does the text call for?"                         │
│                                                                      │
│  typesafe_tool_call_threshold = 0.6    (mặc định)                   │
│                                                                      │
│  tool KHÔNG có arguments  ──► Jev pick ≥ 0.6 → GỌI TRỰC TIẾP       │
│                              (được gọi ngay trên lựa chọn của Jev)   │
│                                                                      │
│  tool CÓ arguments        ──► dừng ở ToolCallProposed               │
│                              (một loại ModelAPIError)                │
│                              → FallbackModel (LLM đứng SAU Jev)      │
│                                nhận nguyên cả step và xử lý         │
│                                                                      │
│  Pattern: Jev decides tool/threshold → LLM viết arguments khi cần   │
└──────────────────────────────────────────────────────────────────────┘
```

<details>
<summary>Python — FallbackModel (Click to expand/collapse)</summary>

```python
from pydantic_ai.models.fallback import FallbackModel
from pydantic_ai.models.typesafe import TypeSafeModel
from pydantic_ai.models.openai import OpenAIModel

# Jev phía trước (nhanh, rẻ, decide tool/threshold);
# LLM phía sau cho các step cần sinh text / tool arguments
model = FallbackModel(
    TypeSafeModel("jev-1.13.0"),
    OpenAIModel("gpt-5"),                  # fallback khi ToolCallProposed
)

agent = Agent(model, output_type=Triage, tools=[lookup_user, refund_flow])
```

</details>

---

## 5. LangChain — TypeSafeClassifier

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** LangChain tích hợp Jev qua **`TypeSafeClassifier`** — một classifier model nhận **cùng state + questions** qua **`.invoke()`**, trả typed answers. Dễ nhét vào chain/middleware hiện có (routing, risk gate) thay vì đổi cả stack.
> **Ẩn dụ/so sánh:** Như **thay router Wi-Fi cũ bằng router nhanh hơn** — cùng dây mạng, cùng giao thức, chỉ phần xử lý packet nhanh và calibrated hơn.
> **Vì sao quan trọng:** Routing / triage / AutoMode gate là System One-shaped — dùng LLM ở đây là chậm và đắt. TypeSafeClassifier cho bạn **typed answer trong 70-500ms** ngay trong chain LangChain.

### 5.1 Cơ Bản

<details>
<summary>Python — TypeSafeClassifier (Click to expand/collapse)</summary>

```python
from langchain.typesafe import TypeSafeClassifier

clf = TypeSafeClassifier(
    model="jev-1.13.0",
    api_key=os.environ["TYPESAFE_API_KEY"],
)

answers = clf.invoke({
    "state": "Ticket #4821: charged twice, want refund.",
    "questions": {
        "intent": {
            "type": "choice",
            "choices": ["billing", "tech", "account", "other"],
            "description": "Primary intent of this message?",
        },
        "toxic": {
            "type": "noul",
            "description": "Is this message abusive or toxic?",
        },
    },
})

print(answers["intent"].choice)     # → routing branch
if answers["toxic"].p >= 0.9:
    hold_for_moderation()
```

</details>

### 5.2 Trong Agent Middleware

```
┌──────────────────────────────────────────────────────────────────┐
│  ROUTING MIDDLEWARE                                              │
│  inbound msg ─► TypeSafeClassifier ─► route to agent branch      │
│                                                                      │
│  AUTOMODE MIDDLEWARE (AutoModeMiddleware)                       │
│  proposed tool call ─► classifier risk ─►                     │
│        risk low  ─► allow auto-execute                         │
│        risk high ─► BLOCK tool call (chặn trước khi chạy)      │
│                                                                      │
│  Cả hai: System One-shaped → Jev, không LLM                    │
└──────────────────────────────────────────────────────────────────┘
```

---

## 6. OpenRouter

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Jev có sẵn trên OpenRouter qua endpoint decisions riêng: `POST https://openrouter.ai/api/alpha/decisions`, model **`typesafe/jev-1.13`**. Áp dụng khi bạn **muốn một key gọi nhiều model** — không thêm key TypeSafe riêng.
> **Ẩn dụ/so sánh:** Như **hub điện multi-socket** — một ổ cắm (một key), nhiều thiết bị (nhiều model), Jev là một socket nữa trong hub.
> **Vì sao quan trọng:** Giảm operational overhead cho team đã standardise OpenRouter; cũng là đường migrate dễ — sau này muốn switch sang key TypeSafe trực tiếp chỉ đổi base URL.

### 6.1 Gọi Trực Tiếp Qua OpenRouter

```json
POST https://openrouter.ai/api/alpha/decisions
Authorization: Bearer <OPENROUTER_API_KEY>
Content-Type: application/json

{
  "model": "typesafe/jev-1.13",
  "state": "...",
  "questions": { ... }
}
```

### 6.2 Qua TypeSafe TS SDK + OpenRouter Base URL

```javascript
const client = new TypeSafe({
  apiKey: process.env.OPENROUTER_API_KEY,
  baseURL: "https://openrouter.ai/api/alpha",
});
// model: "typesafe/jev-1.13" (hoặc alias tương đương)
```

### 6.3 Khi Nào Chọn Đường Nào

```
Muốn 1 key cho MỌI model (LLM + Jev)   ──► OpenRouter
Muốn latency/ính trực tiếp TypeSafe,   ──► api.typesafe.ai
pin jev-1.13.0, quyền config RLCD-ish      (SDK chính thức)
```

---

## 7. Giới Hạn & Lỗi

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** jev-1.13 là **text input only**: không generate text, không viết tool arguments, không đọc file; **giữ arithmetic, counting, date comparison trong code**. Context limit **64k tokens** tổng cho state + questions (**32k cho state** cộng **câu hỏi dài nhất**) — vượt quá báo `ModelHTTPError (max_tokens_exceeded)`.
> **Ẩn dụ/so sánh:** Như **một thẩm phán chỉ đọc được hồ sơ giấy tới 64k chữ** — hết trang là stop, không phải đọc thêm; và thẩm phán **không tự tay viết bản án text** — chỉ phán quyết có/không/điểm.
> **Vì sao quan trọng:** Đây là **non-goals cố ý** (không phải bug sắp fix). Thiết kế sai kỳ vọng = outage + billed tokens vô ích. Bảng lỗi dưới đây nên được **dán vào runbook** của team.

### 7.1 Non-Goals Của jev-1.13

```
┌──────────────────────────────────────────────┬───────────────────────┐
│  JEV KHÔNG...                                 │  THAY BẰNG            │
├──────────────────────────────────────────────┼───────────────────────┤
│  generate text                                │  LLM                  │
│  write tool arguments                         │  LLM / FallbackModel  │
│  read files / không có tool use filesystem    │  code đọc file trước  │
│  arithmetic / counting / date comparison      │  code thuần           │
│  nhận input > 64k tokens (state+questions)    │  tinh giản state      │
│  state > 32k tokens (với câu hỏi dài nhất)   │  lọc detail thừa       │
│  multi-turn / conversation memory             │  bạn quản state        │
└──────────────────────────────────────────────┴───────────────────────┘
```

### 7.2 Bảng Mã Lỗi Thường Gặp

```
┌───────────────────────┬──────────────────────────┬─────────────────────┐
│  Lỗi / Mã             │  Nguyên nhân             │  Cách xử lý         │
├───────────────────────┼──────────────────────────┼─────────────────────┤
│  ModelHTTPError       │  state+questions vượt    │  cắt state; gom     │
│  max_tokens_exceeded  │  64k (32k state +        │  questions; drop    │
│                       │  câu hỏi dài nhất)      │  detail thừa        │
├───────────────────────┼──────────────────────────┼─────────────────────┤
│  401 Unauthorized     │  sai / thiếu API key     │  check Bearer header│
├───────────────────────┼──────────────────────────┼─────────────────────┤
│  403 Forbidden        │  key không scope /       │  cấp lại key /      │
│                       │  model chưa enable      │  verify access      │
├───────────────────────┼──────────────────────────┼─────────────────────┤
│  UserError            │  bool trần KHÔNG có      │  thêm field         │
│  (Pydantic AI)        │  field description       │  description        │
│                       │  (= không proposition)   │  (xem §4.3)         │
├───────────────────────┼──────────────────────────┼─────────────────────┤
│  ToolCallProposed     │  tool CÓ arguments qua   │  FallbackModel      │
│  (ModelAPIError)      │  Jev, threshold pass     │  (LLM) xử lý step   │
├───────────────────────┼──────────────────────────┼─────────────────────┤
│  timeout / 5xx hiếm   │  network / service      │  retry có backoff;  │
│                       │                          │  đây là API thật     │
└───────────────────────┴──────────────────────────┴─────────────────────┘
```

### 7.3 Checklist Trước Khi Go-Live

```
□ Pin model "jev-1.13.0" (không alias) cho production
□ State sạch, relevant — không detail thừa (state hygiene)
□ Mọi bool field trong output_type CÓ field description
□ Threshold confidence/certainty/p định nghĩa + test (xem 04-calibration)
□ Low-confidence path có nhánh escalate (không rơi None)
□ Arithmetic / date / counting ở CODE, không ở questions
□ Error path xử lý max_tokens_exceeded (giảm state, không retry mù)
□ Tool-call threshold typesafe_tool_call_threshold (0.6) đã review
   với cách team dùng tools
□ Eval: đo accuracy + calibration trên data thật (xem 07)
```

---

## 8. Bảng Tích Hợp Tổng Hợp

```
┌──────────────────┬────────────────────────────────┬─────────────────────┐
│  Integration     │  Entry point                   │  Phù hợp khi        │
├──────────────────┼────────────────────────────────┼─────────────────────┤
│  REST API        │  POST /v1/systemone            │  mọi stack          │
│  Python SDK      │  typesafe.Client.ask()         │  services Python    │
│  JavaScript SDK  │  client.ask()                  │  services Node/TS   │
│  Pydantic AI     │  TypeSafeModel + output_type   │  typed agents       │
│  LangChain       │  TypeSafeClassifier.invoke()   │  chain / middleware │
│  OpenRouter      │  /alpha/decisions (1 key)      │  multi-model stack  │
│  Spice AI        │  Jev từ SQL                    │  decisions trong data│
│  Refix           │  runtime tooling               │  dev workflow       │
└──────────────────┴────────────────────────────────┴─────────────────────┘
```

---

*Tiếp theo: [04 — Calibration](../04-calibration/)*

*Trở về [README](../README.md) — tổng quan Module XIV*
