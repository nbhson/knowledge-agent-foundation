# 🤝 06. Jev + LLM — Phân Chia Lao Động

> Phần này giải thích cách **kết hợp Jev với LLM** trong cùng một hệ thống: hai-brain model, model routing, tool-call gateway, fallback model (Pydantic AI), và vị trí của Jev trong **harness**, **loop**, và **graph** — cùng các anti-pattern cần tránh. Đọc [README.md](../README.md) trước để có bối cảnh tổng quan Module XIV.

---

## 1. Two-Brain Model — Jev Decides, LLM Writes

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** *"Jev decides, LLM writes"* — Jev xử lý **quyết định** (chọn option, chấm điểm yes/no trong schema biết trước), LLM xử lý **ngôn ngữ** (sinh text, giải thích, viết code, soạn email). Chiến lược mở rộng: *"Jev routes and verifies, LLM provides the language."*
> **Ẩn dụ/so sánh:** Giống **bộ não hai nửa**: System One (Jev — nhanh, trực giác, chọn hướng) và System Two ngôn ngữ (LLM — chậm hơn, viết ra lời). Theo Kahneman, Jev là *System One Model* đầu tiên: fast & intuitive; LLM đảm nhận phần slow & deliberate khi cần text.
> **Vì sao quan trọng:** Jev rẻ ($0.042/1M input, free output) và nhanh (70–500ms) — **hỏi Jev mọi lúc** gần như free. LLM đắt và chậm hơn — **gọi LLM khi thực sự cần text**. Phân chia đúng tiết kiệm chi phí orders of magnitude và giảm latency phần lớn các bước trung gian.

### 1.1 Bảng Phân Vai

```
┌────────────────────────────────────────────────────────────────────────┐
│                    TWO-BRAIN DIVISION OF LABOR                         │
│                                                                        │
│   JEV (System One)                  LLM (language brain)               │
│   ┌──────────────────────┐          ┌──────────────────────────┐       │
│   │ 🧭 DECISION — màu xanh│          │ ✍️ LANGUAGE              │       │
│   │  • route / triage     │          │  • sinh text / email     │       │
│   │  • classify / score   │          │  • giải thích kết quả    │       │
│   │  • yes/no gate        │          │  • viết code / patch     │       │
│   │  • verify grounded?   │          │  • tóm tắt / dịch        │       │
│   │  • rank / filter      │          │  • argument cho tool     │       │
│   │                       │          │    (text→args)           │       │
│   │  Không sinh text      │          │  Không quyết định        │       │
│   │  Không token output   │          │    thay Jev được         │       │
│   └──────────┬────────────┘          └────────────┬─────────────┘       │
│              │  quyết định                         │  văn bản           │
│              └──────────────┬─────────────────────┘                    │
│                             ▼                                          │
│              ┌──────────────────────────────┐                          │
│              │ CODE ACTS: business rules    │                          │
│              │ áp kết quả Jev + text LLM   │                          │
│              └──────────────────────────────┘                          │
└────────────────────────────────────────────────────────────────────────┘
```

| Việc cần làm | Ai làm? | Vì sao |
|--------------|---------|--------|
| Chọn queue/label/option | **Jev** (Choice) | Schema biết trước, 70–500ms, gần free |
| Yes/no authorize / verify | **Jev** (Noul) | Margin \|p−0.5\|×2, calibrated |
| Chấm điểm mức độ | **Jev** (Score) | Weighted score + distribution |
| Sinh câu trả lời cho khách | **LLM** | Cần text |
| Giải thích "tại sao" | **LLM** (từ kết quả Jev) | Jev không giải thích |
| Viết argument phức tạp cho tool | **LLM** | Jev không sinh tool args |
| Routing model selection | **Jev** → chọn LLM nào | Jev gate trước, LLM chạy sau |

### 1.2 Nguyên Tắc Chi Phí / Latency

```
   Hỏi Jev:     $0.042/1M input · free output · 70-500ms
                 → HỎI MỌI LÚC được — thêm questions gần như free latency

   Gọi LLM:     đắt hơn nhiều · chậm hơn · sinh token
                 → GỌI KHI CẦN TEXT — mỗi lần gọi là tiền + thời gian

   Kết quả:     Jev ở mọi bước trung gian, LLM chỉ ở terminal "viết"
                 → ~2 orders of magnitude efficient hơn nếu chỉ dùng LLM
```

---

## 2. Model Routing — Jev Chọn LLM Nào

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Middleware dùng Jev **đánh giá request trước** (Choice về độ khó / loại task) rồi **chọn model**: request đơn giản → model rẻ/nhanh, request phức tạp → model mạnh. Jev **gắn từ đầu** pipeline; probabilities được **giữ trong agent state** để các bước sau đọc lại.
> **Ẩn dụ/so sánh:** Giống **lễ tân phân phòng khám** — bác sĩ thường khám trước (Jev, vài trăm ms), nếu bệnh nặng mới chuyển bác sĩ chuyên khoa (LLM mạnh). Không cần chuyên khoa khám cho mọi bệnh nhân.
> **Vì sao quan trọng:** Không routing → mọi request chạy trên model đắt nhất = lãng phí; routing bằng LLM khác thì chính routing cũng tốn tiền/giây. Jev routing gần free và đủ nhanh cho pre-dispatch.

### 2.1 Kiến Trúc Routing Middleware

```
   User request
        │
        ▼
┌───────────────────────────────────────────────┐
│  Jev routing middleware (gắn ĐẦU pipeline)     │
│  Choice: difficulty = [simple | moderate |     │
│                        complex]                │
│  + probabilities, confidence                   │
│  → lưu vào agent state                         │
└──────────────────┬────────────────────────────┘
                   │
       ┌───────────┼───────────────┐
       ▼           ▼               ▼
   simple       moderate        complex
   (p cao)      (p cao)         (p cao)
       │           │               │
       ▼           ▼               ▼
   fast/cheap  mid model      strong model
   model                            │
       │           │               │
       └───────────┴───────┬───────┘
                           ▼
              LLM sinh text → code act

   Confidence thấp (band LOW) → escalate / dùng model mạnh mặc định
```

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
import requests
from dataclasses import dataclass, field
from typing import Any, Dict

API = "https://api.typesafe.ai/v1/systemone"
HEADERS = {"Authorization": "Bearer <KEY>", "Content-Type": "application/json"}

MODEL_TIERS = {
    "simple":   "cheap-fast-model",     # VD: small/haiku-class
    "moderate": "mid-model",
    "complex":  "strong-model",         # VD: opus/ frontier-class
}


@dataclass
class AgentState:
    """Agent state — probabilities được GIỮ ĐÂY cho các bước sau."""
    data: Dict[str, Any] = field(default_factory=dict)

    def set_routing(self, difficulty: str, probs: Dict[str, float],
                    confidence: float, request_id: str):
        self.data["routing"] = {
            "difficulty": difficulty,
            "probs": probs,
            "confidence": confidence,
            "request_id": request_id,
        }


def route_request(user_request: str, state: AgentState) -> str:
    """Gắn từ ĐẦU pipeline: Jev chọn tier → trả về model name."""
    resp = requests.post(
        API,
        headers=HEADERS,
        json={
            "model": "jev-1.13.0",
            "state": user_request,
            "questions": {
                "difficulty": {
                    "type": "choice",
                    "options": ["simple", "moderate", "complex"],
                }
            },
        },
        timeout=5,
    )
    resp.raise_for_status()
    data = resp.json()
    ans = data["answers"]["difficulty"]
    confidence = ans.get("confidence", 0.0)

    state.set_routing(
        difficulty=ans["selected"],
        probs=ans.get("probabilities", {}),
        confidence=confidence,
        request_id=data.get("request_id", ""),
    )

    # Band LOW → không tin routing → mặc định model mạnh (an toàn)
    if confidence < 0.5:
        return MODEL_TIERS["complex"]
    return MODEL_TIERS[ans["selected"]]


def handle(user_request: str) -> str:
    state = AgentState()
    model = route_request(user_request, state)       # Jev decide (rẻ, nhanh)
    draft = call_llm(model, user_request)            # LLM viết (cần text)
    return draft
# state.data["routing"] giờ chứa probs + confidence — các bước sau đọc lại
```

</details>

### 2.2 Lưu Ý

| Điểm | Guidance |
|------|----------|
| Vị trí | Middleware **gắn đầu** — trước mọi LLM call |
| State | Giữ `probs`, `confidence`, `request_id` trong agent state để audit/cascade |
| Band LOW | Confidence thấp → chọn model mạnh mặc định, không routing "tiết kiệm" |
| Integration | Tương tự pattern **routing middleware** trong LangChain (TypeSafeClassifier) |

---

## 3. Tool-Call Gateway — Jev Gate Trước Khi Tool Chạy

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Jev gate **trước khi tool thực thi**: mỗi tool call đi qua một Noul check (authorize/safe theo context), call dưới threshold bị **block** và chuyển sang approval flow. Đây là tầng trung gian giữa *ý định của agent* và *side-effect thật*.
> **Ẩn dụ/so sánh:** Giống **chốt an ninh giữa hành lang văn phòng và phòng họp tài chính** — badge quẹt không hợp lệ thì cửa không mở, bất kể agent "nghĩ" mình được vào.
> **Vì sao quan trọng:** Kết nối trực tiếp với **Auth/approval**: mọi tool có side-effect (xoá, charge, gửi) đều phải qua gateway. Jev nhanh enough (70–500ms) để không cản luồng real-time, và calibrated đủ để threshold có nghĩa.

### 3.1 Gateway Pipeline

```
   Agent định gọi tool(name, args)
        │
        ▼
┌────────────────────────────┐
│  Jev tool-call gateway     │
│  Noul: "authorize?"        │
│  p_yes + confidence        │
└─────────────┬──────────────┘
              │
   ┌──────────┼──────────────────┐
   ▼          ▼                  ▼
 p_yes HIGH  MEDIUM            LOW / conf thấp
 allow       → confirm         → BLOCK
 tool chạy   (user approve)    │
                               ▼
                     ┌──────────────────────┐
                     │ Auth / approval flow │
                     │ • human click allow  │
                     │ • policy engine      │
                     │ • denylist check     │
                     └──────────────────────┘
```

**Điểm kết nối Auth/approval**: Jev là *signal phân loại*, còn **quyền allow/deny cuối cùng** nằm ở lớp auth thật (permissions, denylist, human gate). Jev **không thay thế auth** — nó bổ sung judgment nhanh trên context mà rule tĩnh không cover được.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
import requests

API = "https://api.typesafe.ai/v1/systemone"
HEADERS = {"Authorization": "Bearer <KEY>", "Content-Type": "application/json"}


def tool_call_gateway(context: str, tool: dict,
                      p_threshold: float = 0.6) -> tuple[bool, dict]:
    """
    Trả về (allowed, meta).
    allowed=False → chuyển approval flow, KHÔNG chạy tool.
    """
    state = (
        f"Context:\n{context}\n\n"
        f"Tool: {tool['name']}\nArgs: {tool.get('args', {})}"
    )
    resp = requests.post(
        API,
        headers=HEADERS,
        json={
            "model": "jev-1.13.0",
            "state": state,
            "questions": {"authorized": {"type": "noul"}},
        },
        timeout=5,
    )
    resp.raise_for_status()
    ans = resp.json()["answers"]["authorized"]
    p_yes = ans.get("p_yes", 0.5)
    conf = abs(p_yes - 0.5) * 2
    meta = {"p_yes": p_yes, "confidence": conf,
            "request_id": resp.json().get("request_id")}

    if p_yes >= p_threshold and conf >= 0.5:
        return True, meta                      # allow → tool chạy

    # block → approval flow (auth layer thật quyết định tiếp)
    approval_request(tool, meta)               # human / policy engine
    return False, meta
```

</details>

---

## 4. Fallback Model — LLM Đứng Sau Jev (Pydantic AI)

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Trong **Pydantic AI**, `TypeSafeModel` đặt câu hỏi qua Jev; khi tool cần Jev không xử lý được, **`FallbackModel`** (một LLM) **nhận cả bước** thay Jev. Hai chế độ: tool **không args** → Jev pick tool và gọi; tool **có args** → `ToolCallProposed` raises `ModelAPIError` → FallbackModel (LLM) làm toàn bộ bước với tư cách model chính.
> **Ẩn dụ/so sánh:** Giống **quầy tiếp vấn**: Jev là nhân viên nhanh xử lý hồ sơ chuẩn (chọn form có sẵn); khi hồ sơ phức tạp cần viết tự do, nhân viên bấm chuông gọi **quản lý (LLM)** — quản lý tiếp quản toàn bộ ca việc đó, không phải chỉ phần lẻ.
> **Vì sao quan trọng:** Đây là pattern **"Jev routes, LLM fallback"** chính thức: threshold `typesafe_tool_call_threshold` mặc định **0.6** quyết định lúc nào Jev tự quyết vs lúc nào chuyển LLM. Biết hai nhánh (no-arg vs arg tool) để thiết kế tool signatures đúng.

### 4.1 Hai Nhánh Trong Pydantic AI

```
┌─────────────────────────────────────────────────────────────────────────┐
│  TypeSafeModel (Jev) + FallbackModel (LLM)                               │
│                                                                          │
│   Bước có TOOL                                                            │
│     │                                                                     │
│     ├── Tool KHÔNG args ──────────────────────────────────────────────┐  │
│     │     Jev pick "tool nào được gọi" (Choice trên danh sách tool)   │  │
│     │     confidence ≥ typesafe_tool_call_threshold (mặc định 0.6)    │  │
│     │     → Jev chọn → tool gọi không tham số → xong                 │  │
│     │                                                                │  │
│     └── Tool CÓ args ─────────────────────────────────────────────┐  │  │
│           Jev không sinh được tool arguments (không text/token)   │  │  │
│           → ToolCallProposed → ModelAPIError                      │  │  │
│           → FallbackModel (LLM) nhận CẢ BƯỚC                      │  │  │
│           → LLM sinh args + gọi tool → tiếp tục                  │  │  │
│                                                                  │  │  │
│   Kết quả: LLM đứng SAU Jev — Jev quyết phần schema,             │  │  │
│   LLM trám phần text. Threshold 0.6 = starting point.            ◄──┘  │
└─────────────────────────────────────────────────────────────────────────┘
```

### 4.2 Ví Dụ Code

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
# Pydantic AI + TypeSafe integration (minh hoạ kiến trúc)
from pydantic_ai import Agent
# from pydantic_ai.models.typesafe import TypeSafeModel
# from pydantic_ai.models.fallback import FallbackModel

# --- Cấu hình kiến trúc ---
# primary   = TypeSafeModel('jev-1.13.0')      # Jev decide trước
# fallback  = FallbackModel('some-llm')          # LLM nhận cả bước khi Jev kẹt
# agent     = Agent(model=primary + fallback)    # (giả định) composition
#
# typesafe_tool_call_threshold = 0.6            # mặc định — TUNE từ labelled data


# --- Tool KHÔNG args: Jev pick và gọi ---
@agent.tool_plain
def refresh_dashboard() -> str:
    """Không tham số — Jev chọn tool này (hoặc tool khác) từ danh sách,
    nếu confidence ≥ 0.6 thì gọi thẳng, KHÔNG cần LLM sinh args."""
    return render_dashboard()


# --- Tool CÓ args: Jev không sinh args được ---
@agent.tool_plain
def search_docs(query: str, top_k: int = 5) -> list[str]:
    """Có args → Jev không generate được text args.
    Flow: ToolCallProposed → ModelAPIError → FallbackModel (LLM)
    LLM (fallback) đảm nhận CẢ BƯỚC: đọc context, sinh query, gọi tool."""
    return vector_search(query, top_k)


# --- Điều chỉnh threshold từ labelled data của bạn ---
# Cao hơn → ít handoff sang LLM hơn, nhưng đúng hơn KHI handoff xảy ra.
# agent/settings.typesafe_tool_call_threshold = 0.75   # sau khi tune
```

**Đọc flow lại một lần:**

```
Input ──► TypeSafeModel (Jev)
            │
            ├─ answer thuần (Choice/Score/Noul) ──► trả kết quả (rẻ, nhanh)
            │
            ├─ tool không args, conf ≥ 0.6 ──────► Jev pick → tool chạy
            │
            └─ tool CÓ args ──► ToolCallProposed
                                ──► ModelAPIError
                                ──► FallbackModel (LLM) nhận cả BƯỚC
                                    ──► LLM sinh args / text → tool chạy
```

</details>

### 4.3 Lưu Ý

| Điểm | Guidance |
|------|----------|
| Threshold | `typesafe_tool_call_threshold` mặc định **0.6** — starting point, không phải validated; tune từ labelled tickets/data |
| Higher threshold | Ít handoff hơn, nhưng **đúng hơn khi nó hand off** |
| No-arg tool | Jev pick được → không tốn LLM call |
| Arg tool | Jev kẹt → FallbackModel nhận **cả bước** (không chỉ phần args) |
| Design tip | Tách tool thành no-arg khi có thể → maximize Jev coverage |

---

## 5. Jev Trong Harness

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Gắn Jev vào các **bước quyết định của harness**: retrieve (chọn nguồn), decide tools (chọn tool set), workflow gates (điều kiện chuyển bước). Jev là **semantic decision layer** nằm giữa raw context và hành động của agent.
> **Ẩn dụ/so sánh:** Giống **người điều phối trong xưởng**: không tự hàn (LLM viết), nhưng quyết định *bộ phận nào nhận việc* và *bước nào được sang bước tiếp* — trong vài chục mili-giây mỗi quyết định.
> **Vì sao quan trọng:** Harness có nhiều bước **quyết định nhịp cao** (mọi tool selection, mọi gate) — dùng LLM cho từng bước đó vừa chậm vừa đắt. Jev làm các bước này gần free; LLM chỉ viết khi cần text.

### 5.1 Jev Tại Các Điểm Quyết Định Trong Harness

```
┌──────────────────────────────────────────────────────────────────────┐
│                     JEV INSIDE A HARNESS                              │
│                                                                       │
│  Context ──► [RETRIEVE: Jev chọn nguồn/segment — Choice]             │
│                    │                                                  │
│                    ▼                                                  │
│              [DECIDE TOOLS: Jev chọn tool set — Choice] ◄── harness  │
│                    │                                     /06-decide-  │
│                    ▼                                     tools-mcp    │
│              [WORKFLOW GATE: Jev pass/fail chuyển bước — Noul] ◄──── harness
│                    │                                        /07-workflow
│              HIGH band: auto-advance                                       │
│              LOW  band: escalate / LLM-as-judge                            │
│                    │                                                       │
│                    ▼                                                       │
│              [LLM WRITES: sinh text / code cho bước được phép]             │
└──────────────────────────────────────────────────────────────────────┘
```

**Cross-link chi tiết:**

| Bước harness | Jev làm gì | Doc |
|--------------|-----------|-----|
| Decide tools / MCP | Chọn tool phù hợp context (Choice trên tool list) | [harness/06-decide-tools-mcp](../../harness/06-decide-tools-mcp/) |
| Workflow transitions | Gate điều kiện next step (Noul + threshold) | [harness/07-workflow](../../harness/07-workflow/) |

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
import requests

API = "https://api.typesafe.ai/v1/systemone"
HEADERS = {"Authorization": "Bearer <KEY>", "Content-Type": "application/json"}


def decide_tools(harness_context: str, available_tools: list[str]) -> dict:
    """Harness step: Jev chọn tool set (Choice) thay vì LLM đọc & chọn."""
    resp = requests.post(
        API,
        headers=HEADERS,
        json={
            "model": "jev-1.13.0",
            "state": harness_context,
            "questions": {
                "tool_choice": {"type": "choice", "options": available_tools},
            },
        },
        timeout=5,
    )
    resp.raise_for_status()
    ans = resp.json()["answers"]["tool_choice"]
    if ans.get("confidence", 0) < 0.5:
        return {"action": "escalate", "reason": "low confidence tool select"}
    return {"action": "use", "tool": ans["selected"],
            "probs": ans.get("probabilities", {})}


def workflow_gate(step_result: str, policy: str) -> bool:
    """Harness step: Noul gate — bước sau có được chạy không."""
    resp = requests.post(
        API,
        headers=HEADERS,
        json={
            "model": "jev-1.13.0",
            "state": f"Policy:\n{policy}\n\nStep result:\n{step_result}",
            "questions": {"ready_for_next": {"type": "noul"}},
        },
        timeout=5,
    )
    resp.raise_for_status()
    p = resp.json()["answers"]["ready_for_next"].get("p_yes", 0.5)
    return p >= 0.7 and abs(p - 0.5) * 2 >= 0.5
```

</details>

---

## 6. Jev Trong Loop & Graph

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Trong **loop**, Jev đảm nhận các **decision steps** (triage loop nào chạy, verify artifact có pass không); trong **graph**, Jev là **decision layer** trên node/edge — phân loại tri thức, gate transition, không thay thế traversal hay storage.
> **Ẩn dụ/so sánh:** Loop là **dây chuyền tự chạy** — Jev là công tắc quyết định *máy nào chạy* và *lô nào đạt chuẩn*. Graph là **bản đồ quan hệ** — Jev là **người gác cổng** phân loại tin nhắn đi qua bản đồ, không phải người vẽ bản đồ.
> **Vì sao quan trọng:** Cả loop và graph đều có nhiều bước quyết định nhịp cao; gắn Jev đúng chỗ (triage + verify) giúp loop/graph **nhanh và rẻ** ở tầng điều khiển, giữ LLM cho phần viết.

### 6.1 Jev Trong Execution Loop

```
   Schedule fires
        │
        ▼
   ┌───────────────────────────────────────────────────────┐
   │  TRIAGE (Jev Choice): loop nào có việc?              │
   │  confidence HIGH → auto-run · LOW → bỏ qua/escalate  │
   └───────────────────┬───────────────────────────────────┘
                       ▼
        Worktree → Implementer (LLM writes) → patch
                       │
                       ▼
        VERIFIER pre-screen (Jev Noul/Score): patch grounded?
                       │
              ┌────────┴─────────┐
           PASS (band HIGH)    FAIL / LOW conf
              │                    │
              ▼                    ▼
        tests đầy đủ          reject sớm / retry
              │
              ▼
        Human gate → commit / escalate
```

**Pattern chính**: **verified cascade trong loop** — Jev làm pre-screen nhanh (70–500ms) trước khi tốn resources chạy full test suite. Jev fail → reject ngay, không mời verifier LLM to. Cross-link: [loop/01-concepts — execution loop & anatomy](../../loop/01-concepts/) (maker/checker split — Jev đóng vai checker *tốc độ cao* tầng đầu).

### 6.2 Jev Trong Graph

```
   Graph nodes (tri thức)
        │
        ▼  mỗi node/edge một classification nhanh
   ┌────────────────────────────────────────────┐
   │  DECISION LAYER (Jev):                     │
   │  • phân loại node (Choice)                 │
   │  • gate edge traversal (Noul)              │
   │  • score độ liên quan path (Score)         │
   └───────────────────┬────────────────────────┘
                       ▼
   Graph store / traversal (Neo4j, NetworkX...) — KHÔNG đổi
                       │
                       ▼
   LLM viết câu trả lời dựa trên subgraph được chọn
```

Jev **không đọc graph, không traverse** — nó phân loại *metadata / context trích xuất từ node* thành quyết định. Xem [graph](../../graph/) để hiểu nền tảng graph engineering; Jev là lớp quyết định mỏng đặt trên trên.

### 6.3 Bảng Vị Trí Jev

| Framework | Jev ở đâu | Cross-link |
|-----------|-----------|------------|
| **Loop** | Triage (chọn loop/pattern), verify pre-screen (Noul/Score) | [loop/01-concepts](../../loop/01-concepts/) |
| **Graph** | Decision layer: classify nodes, gate edges, score paths | [graph](../../graph/) |
| **Harness** | Retrieve / decide tools / workflow gates | [harness/06](../../harness/06-decide-tools-mcp/), [07](../../harness/07-workflow/) |
| **Verified cascade** | Draft check trong mọi framework trên | Pattern [05](../05-patterns/) |

---

## 7. Anti-Patterns Khi Kết Hợp

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Các lỗi thiết kế phổ biến khi ghép Jev + LLM — chủ yếu xuất phát từ **đảo vai trò** (đòi Jev viết, đẩy quyết định vào prompt) hoặc **tin tưởng sai chỗ** (confidence mù quáng không fallback).
> **Ẩn dụ/so sánh:** Giống **đeo găng tay boxing để gõ bàn phím** — dụng cụ không sai, nhưng dùng sai việc thì vừa hỏng việc vừa mỏi tay.
> **Vì sao quan trọng:** Mỗi anti-pattern dưới đây đều dẫn đến: kết quả sai khó phát hiện, cost không giảm, hoặc hệ thống "có vẻ thông minh" nhưng không calibrate.

### 7.1 Bảng Anti-Patterns

| # | Anti-pattern | Triệu chứng | Sửa thế nào |
|---|-------------|--------------|-------------|
| 1 | **Dùng Jev cho việc cần text** | Cố "hỏi" Jev để sinh email/explanation → không có output text | LLM viết; Jev chỉ decide |
| 2 | **Đặt câu hỏi vào prompt** | Nhét "chọn A hay B" vào state/prompt rồi expect LLM/Jev "nói" | State = **material** (dữ liệu đầu vào); câu hỏi đi vào `questions`, không vào prompt |
| 3 | **Tin confidence cao mù quáng** | auto-act mọi confidence ≥ 0.9 mà không có fallback | Luôn có nhánh escalate/fallback; confidence ≠ truth (xem [04](../04-calibration/)) |
| 4 | **Không có fallback khi low confidence** | Band LOW mà code vẫn tự xử | Route human / LLM / retry với state khác |
| 5 | **Đòi Jev giải thích** | Expect reasoning chain từ API chỉ trả probability | Explanation là việc của LLM *sau* khi có kết quả Jev |
| 6 | **Câu hỏi multi-factor** | Một Choice gộp 5 tiêu chí → confidence thấp triền miên | Tách thành nhiều questions parallel (miễn phí latency) |
| 7 | **Chỉ đọc label, bỏ distribution** | Không thấy near-tie/ambiguity | Luôn đọc probabilities + margin |
| 8 | **Không eval / không tune threshold** | Dùng 0.6/0.8 mặc định mãi, không log outcome | Eval set + calibration curve từ data thật ([07](../07-limits-and-evaluation/)) |

### 7.2 Mã Hóa Anti-Pattern #2 — State Là Material

```
   ❌ SAI:  state = "Hãy chọn queue: billing hay tech? Trả lời A/B."
            → biến Jev/LLM thành prompt-questioner, không có material

   ✅ ĐÚNG: state    = "Ticket: Tôi bị trừ tiền 2 lần cho đơn #4821..."
            questions = {"queue": {type: choice, options: [...]}}
            → state là dữ liệu, questions là câu hỏi
```

### 7.3 Mã Hóa Anti-Pattern #3/#4 — Fallback Bắt Buộc

```python
# Mẫu nhỏ nhấn mạnh: confidence cao VẪN cần đường fallback tổng thể
def decide_or_fallback(state: str, questions: dict) -> dict:
    result = jev_decide(state, questions)          # 70–500ms, rẻ
    ans = result["answers"]["queue"]
    conf = ans.get("confidence", 0)

    if conf >= 0.8:
        return {"by": "jev", "value": ans["selected"], "conf": conf}
    if conf >= 0.5:
        return {"by": "jev", "value": ans["selected"],
                "conf": conf, "needs_confirm": True}

    # LOW band — KHÔNG tin Jev ở đây → fallback LLM / human
    return {"by": "llm_or_human", "value": llm_decide(state, questions),
            "conf": None, "reason": "low confidence band"}
```

---

> *"Jev là lớp quyết định trong phần mềm bình thường: state vào, kết quả typed có giới hạn ra, business rules hành động. LLM viết phần còn lại."*

---

*Trở về [README](../README.md) — tổng quan Module XIV*

*Tiếp theo: [07 — Giới Hạn & Đánh Giá](../07-limits-and-evaluation/) →*

*Trước đó: [05 — Patterns: Xây Dựng Quyết Định Production](../05-patterns/)*
