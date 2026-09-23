# 🧭 05. Patterns — Xây Dựng Quyết Định Production

> Phần này tổng hợp **4 target workloads** và **5 production patterns** của Jev — routing/triage, classification at scale, gating agent actions, verifying LLM output (verified cascade), ranking & filtering — cùng **map-reduce**. Mỗi pattern gồm mô tả, khái niệm card, code mẫu, và bảng lưu ý. Đọc [README.md](../README.md) trước để có bối cảnh tổng quan Module XIV.

---

## 1. Tổng Quan

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Patterns ở đây là **các hình thức lắp ghép Jev vào pipeline thật** — mỗi pattern ánh xạ một loại quyết định lặp lại (route, classify, gate, verify, rank) sang primitives của Jev (Choice / Score / Noul), luôn kèm theo **threshold band** quyết định auto-act hay escalate.
> **Ẩn dụ/so sánh:** Giống **bộ công cụ của thợ mộc** — Jev là cái máy cưa (một năng lực duy nhất: cắt quyết định nhanh và chính xác), còn 5 patterns là các **cách lắp máy** vào từng việc: cưa đường thẳng (classify), chặn an toàn (gate), so phẳng (verify)... Cùng một máy, nhiều jig.
> **Vì sao quan trọng:** Biết pattern = biết **đặt câu hỏi nào, primitive nào, ngưỡng nào** cho từng bài toán — thay vì bịa API call mỗi lần. Rule chung: **"Jev decides, code acts, LLM writes."**

### 1.1 Bảng 4 Workloads × 5 Patterns

| # | Target workload | Patterns tương ứng | Primitive thường dùng |
|---|-----------------|--------------------|-----------------------|
| 1 | **Decision steps trong workflows** | Routing/Triage · Gating | Choice · Noul |
| 2 | **Map-reduce over datasets** | Classification at scale · Ranking & Filtering | Choice · Score |
| 3 | **Real-time apps** | Routing (latency-critical) | Choice · Noul (70–500ms) |
| 4 | **Verification of LLM output** | Verified Cascade (verify) | Noul · Score |

### 1.2 Workflow Chung Của Mọi Pattern

```
┌────────────────────────────────────────────────────────────────────────┐
│                    SHARED DECISION WORKFLOW                            │
│                                                                        │
│   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐              │
│   │ Gather state │──►│ Jev decide   │──►│ Read answer  │              │
│   │ (nhỏ, liên   │   │ (parallel,   │   │ + probs +    │              │
│   │  quan)       │   │  70-500ms)   │   │  confidence) │              │
│   └──────────────┘   └──────────────┘   └──────┬───────┘              │
│                                                 │                      │
│                                    ┌────────────▼────────────┐        │
│                                    │ So confidence/threshold  │        │
│                                    │ (per-question band)      │        │
│                                    └───┬──────────┬───────┬───┘        │
│                                        │          │       │            │
│                              HIGH ─────┘   MEDIUM ┘       └── LOW      │
│                              code acts    confirm       escalate       │
│                                        │                              │
│                                        ▼                              │
│                              ┌──────────────────┐                     │
│                              │ LLM chỉ được gọi │                     │
│                              │ khi cần TEXT      │                     │
│                              └──────────────────┘                     │
└────────────────────────────────────────────────────────────────────────┘
```

**Latency & cost nhắc lại**: 70–500ms mỗi decision; $0.042/1M input tokens, free output; thêm questions hầu như không đổi latency (cộng dồn parallel trong một pass). Nhờ rẻ + nhanh mà các pattern classification-at-scale mới khả thi.

---

## 2. Routing & Triage

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Routing/Triage = phân một item (ticket, message, request) vào **một trong các channel/queue/team/priority** đã biết trước. Gọi Jev với 1 **Choice** (team/queue) + 1 **Score** (priority) cho mỗi item.
> **Ẩn dụ/so sánh:** Giống **lễ tân bệnh viện** — nhìn bệnh nhân, phân loại vào khoa (Choice) và mức khẩn (Score: cấp cứu / khẩn / thường) trong vài trăm mili-giây, rồi hành động. Lễ tân không cần viết gì, chỉ cần **chọn đúng ô**.
> **Vì sao quan trọng:** Đây là pattern phổ biến nhất và dễ khởi động nhất — mỗi ticket một lượt decide, độ trễ mạng cộng thêm vẫn giữ tổng dưới ~500ms, đủ cho real-time inbox.

### 2.1 Ví Dụ: Support Ticket → Team / Queue / Priority

```
Ticket text ──► Jev ──┬── queue   = Choice [billing | tech | sales | churn]
                      │             probabilities + confidence
                      └── priority = Score [p0 | p1 | p2 | p3]
                                     probability-weighted score
                                        │
                                        ▼
                              band HIGH  → auto-route
                              band MEDIUM→ suggest cho agent confirm
                              band LOW   → human triage
```

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
import requests

API = "https://api.typesafe.ai/v1/systemone"
HEADERS = {"Authorization": "Bearer <KEY>", "Content-Type": "application/json"}

QUEUES = ["billing", "tech_support", "sales", "churn_risk"]
PRIORITY_LEVELS = ["p0", "p1", "p2", "p3"]


def triage_ticket(ticket_text: str) -> dict:
    resp = requests.post(
        API,
        headers=HEADERS,
        json={
            "model": "jev-1.13.0",
            "state": ticket_text,
            "questions": {
                "queue": {"type": "choice", "options": QUEUES},
                "priority": {"type": "score", "levels": PRIORITY_LEVELS},
            },
        },
        timeout=5,
    )
    resp.raise_for_status()
    data = resp.json()
    q = data["answers"]["queue"]
    p = data["answers"]["priority"]

    return {
        "queue": q["selected"],
        "queue_probs": q.get("probabilities", {}),
        "queue_confidence": q.get("confidence", 0.0),
        # Score: probability-weighted score có thể NGỒI GIỮA 2 level
        "priority": p.get("score", p.get("selected")),
        "priority_confidence": p.get("confidence", 0.0),
        "request_id": data.get("request_id"),
    }


def route(ticket_text: str) -> None:
    result = triage_ticket(ticket_text)
    if result["queue_confidence"] >= 0.8 and result["priority_confidence"] >= 0.7:
        auto_route(result["queue"], result["priority"])   # HIGH band
    elif result["queue_confidence"] >= 0.5:
        suggest_to_agent(result)                          # MEDIUM band
    else:
        human_triage(ticket_text, result)                 # LOW band
```

</details>

### 2.2 Lưu Ý

| Điểm | Guidance |
|------|----------|
| Primitive | 1 Choice (queue) + 1 Score (priority) — thêm questions không đáng kể latency |
| Threshold | Queue: auto-route ≥ 0.8 · Priority: ≥ 0.7 · dưới đó confirm |
| Latency | Jev 70–500ms + network → vẫn thoải mái cho inbox real-time |
| State hygiene | Gửi **phần ticket liên quan** (subject + body đã cắt), đừng gửi toàn bộ history thread |
| Distribution | Đọc `probabilities` — nếu queue near-tie (0.35/0.33) → escalate bất kể label |

---

## 3. Classification & Tagging Ở Scale

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Chạy classification trên **mọi record/row** trong dataset vì chi phí quá rẻ ($0.042/1M input tokens, free output) và mọi câu evaluate **parallel trong một pass**. Output là label sẵn nằm trong schema — không cần parse text, không cần cleanup.
> **Ẩn dụ/so sánh:** Giống **máy phân loại thư công nghiệp** — mỗi lá thư đi qua trong vài chục mili-giây, gắn nhãn sẵn, không cần người đọc. Lợi thế xuất hiện khi **số lượng lớn**: map từng record, reduce gộp lại.
> **Vì sao quan trọng:** LLM cho việc này vừa đắt vừa chậm, lại còn phải parse text; Jev trả label typed ngay, kết hợp được với **map-reduce** để xử lý dataset lớn trong khi latency luôn tính theo **per-decision** (không tăng theo số record).

### 3.1 Kết Hợp Với Map-Reduce

```
   Dataset (N records)
        │
        ▼  MAP: mỗi record → state riêng, decide song song
   ┌─────────┐ ┌─────────┐ ┌─────────┐       ┌─────────┐
   │ record1 │ │ record2 │ │ record3 │  ...  │ recordN │
   │  Jev    │ │  Jev    │ │  Jev    │       │  Jev    │
   │ label+P │ │ label+P │ │ label+P │       │ label+P │
   └────┬────┘ └────┬────┘ └────┬────┘       └────┬────┘
        │           │           │                  │
        ▼           ▼           ▼                  ▼
   ┌────────────────────────────────────────────────────┐
   │  REDUCE: gộp labels + probabilities               │
   │  • majority vote theo bucket confidence            │
   │  • aggregate stats (P trung bình per class)        │
   │  • escalate các record có confidence thấp          │
   └────────────────────────────────────────────────────┘
```

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
import asyncio
from typing import Any

import httpx

API = "https://api.typesafe.ai/v1/systemone"
HEADERS = {"Authorization": "Bearer <KEY>", "Content-Type": "application/json"}
MODEL = "jev-1.13.0"

TAGS = ["bug", "feature_request", "question", "docs", "spam"]


async def classify_one(client: httpx.AsyncClient, record: dict) -> dict:
    """MAP: một record → một label + probability."""
    resp = await client.post(
        API,
        headers=HEADERS,
        json={
            "model": MODEL,
            "state": record["text"],            # state nhỏ, liên quan
            "questions": {
                "tag": {"type": "choice", "options": TAGS},
            },
        },
        timeout=5,
    )
    resp.raise_for_status()
    data = resp.json()
    ans = data["answers"]["tag"]
    return {
        "id": record["id"],
        "tag": ans["selected"],
        "p": ans.get("probabilities", {}).get(ans["selected"], 0.0),
        "confidence": ans.get("confidence", 0.0),
        "request_id": data.get("request_id"),
    }


async def classify_dataset(records: list[dict], batch: int = 50) -> list[dict]:
    """MAP song song từng batch, trả về labels đã phân loại."""
    results: list[dict] = []
    async with httpx.AsyncClient() as client:
        for i in range(0, len(records), batch):
            chunk = records[i : i + batch]
            # Async song song trong chunk — mỗi decide vẫn ~70-500ms
            results.extend(await asyncio.gather(
                *[classify_one(client, r) for r in chunk]
            ))
    return results


def reduce(results: list[dict]) -> dict:
    """REDUCE: gộp kết quả + tách bucket confidence."""
    auto, review = [], []
    for r in results:
        (auto if r["confidence"] >= 0.8 else review).append(r)
    return {
        "auto_tagged": auto,
        "needs_review": review,
        "coverage": len(auto) / max(len(results), 1),
    }


# dataset = load_records()
# summary = reduce(asyncio.run(classify_dataset(dataset)))
```

</details>

### 3.2 Lưu Ý

| Điểm | Guidance |
|------|----------|
| Primitive | Choice (labels) hoặc Score (ordered severity) |
| Scale | Thêm records → tăng token cost linear, **không** tăng per-decision latency |
| Combine | MAP per-record → REDUCE gộp; record low-confidence đi queue review |
| Threshold | Auto-tag ≥ 0.8; dưới đó vào `needs_review` |
| Cost | $0.042/1M input → 100k records với state ngắn vẫn rất rẻ |

---

## 4. Gating Agent Actions

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Gating = đặt một **cánh cửa Noul trước tool call phá hoại** — Jev trả P(yes) cho câu "hành động này có được phép / an toàn theo policy không", code block call nếu confidence dưới threshold hoặc P(yes) thấp. Liên hệ trực tiếp với **LangChain AutoModeMiddleware**.
> **Ẩn dụ/so sánh:** Giống **khóa cửa an toàn trước phòng máy chủ** — người tới (agent) phải quẹt thẻ (Noul check) trước khi bước vào. Quẹt thẻ không đảm bảo họ là người tốt, nhưng **không quẹt thì ai cũng vào được**.
> **Vì sao quan trọng:** Agent autonomous càng cao, số tool call có side-effect (xoá file, gọi API, charge) càng nhiều. Một gate millisecond-level rẻ hơn nhiều so với một sự cố. Tuy nhiên: **Jev không đánh giá an toàn tuyệt đối** — nó phân loại theo schema bạn cung cấp, không phải là security oracle.

### 4.1 Ví Dụ: Gate Trước Khi Gọi Tool Phá Hoại

```
Agent muốn gọi: delete_file(path="/prod/data/users.csv")
        │
        ▼
┌──────────────────────────────────────────────┐
│  Noul gate: "user có authorize xoá file       │
│  này không, theo conversation context?"       │
│                                               │
│  state = conversation context + tool intent   │
│  p_yes = 0.94, confidence = 0.88  → HIGH      │
│  p_yes = 0.55, confidence = 0.10  → LOW       │
└──────────────┬───────────────────────────────┘
               │
       p_yes ≥ threshold & confidence HIGH
               │
       ┌───────┴────────┐
       ▼                ▼
    ALLOW            BLOCK / ESCALATE
  tool chạy         → hỏi user xác nhận
                     → hoặc Human-in-the-loop
```

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
import requests

API = "https://api.typesafe.ai/v1/systemone"
HEADERS = {"Authorization": "Bearer <KEY>", "Content-Type": "application/json"}


def noul_confidence(p_yes: float) -> float:
    return abs(p_yes - 0.5) * 2


def gate_tool_call(
    conversation_context: str,
    tool_name: str,
    tool_args: dict,
    p_threshold: float = 0.6,
    conf_threshold: float = 0.5,
) -> bool:
    """
    Trả về True nếu tool được phép chạy.
    KHÔNG dựa mỗi p_yes — đọc cả confidence (margin).
    """
    state = (
        f"Conversation:\n{conversation_context}\n\n"
        f"Tool the agent wants to call: {tool_name}\n"
        f"Arguments: {tool_args}"
    )
    resp = requests.post(
        API,
        headers=HEADERS,
        json={
            "model": "jev-1.13.0",
            "state": state,
            "questions": {
                # Noul: yes/no — không có confidence riêng,
                # confidence = |p - 0.5| * 2
                "authorized": {"type": "noul"},
            },
        },
        timeout=5,
    )
    resp.raise_for_status()
    ans = resp.json()["answers"]["authorized"]
    p_yes = ans.get("p_yes", ans.get("probability_yes", 0.5))
    conf = noul_confidence(p_yes)

    if p_yes >= p_threshold and conf >= conf_threshold:
        return True                      # allow
    # block → human approval hoặc deny
    request_human_approval(tool_name, tool_args, p_yes, conf)
    return False


# Giống tinh thần LangChain AutoModeMiddleware:
# middleware wrap tool, decide allow/block trước khi tool thực thi.
def auto_mode_middleware(tool_call, context) -> bool:
    return gate_tool_call(
        conversation_context=context,
        tool_name=tool_call["name"],
        tool_args=tool_call["args"],
    )
```

</details>

### 4.2 Lưu Ý

| Điểm | Guidance |
|------|----------|
| Primitive | **Noul** — yes/no authorize; confidence = \|p−0.5\|×2 |
| Threshold | p_yes ≥ ~0.6 **và** confidence ≥ 0.5 (starting point — tune từ labelled data) |
| Caveat | Jev **không** phải security judgment tuyệt đối — nó phân loại theo policy text bạn cho, không audit logic nền tảng (MITRE-ish: classification ≠ safety proof) |
| Liên hệ | LangChain **AutoModeMiddleware** — wrap risky tool calls |
| Fallback | Block → hiển thị context đầy đủ cho human approve/deny |

---

## 5. Verify LLM Output (Verified Cascade)

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Verified Cascade = **LLM draft trước, Jev check sau** — LLM sinh nội dung, Jev (Noul/Score) đánh giá draft có *grounded theo policy text* không, pass thì dùng còn fail thì fallback/regenerate. Jev ở đây là **người soát bài nhanh**, không phải người viết.
> **Ẩn dụ/so sánh:** Giống **biên tập viên duyệt bản thảo của phóng viên** — phóng viên viết (LLM), biên tập viên đọc và chấm "đạt/không đạt" theo cẩm nang (Jev), không đạt thì trả lại viết lại. Biên tập viên không viết bài thay — chỉ **phán**.
> **Vì sao quan trọng:** Đây là pattern gắn với **4th target workload** (verification of LLM output) và là cách rẻ nhất để thêm kiểm soát chất lượng: mỗi lần verify là 70–500ms và gần như free token output — chạy được trong harness/loop với tần suất cao.

### 5.1 Chuỗi Verified Cascade

```
┌────────────┐    ┌──────────────────┐    ┌─────────────────────┐
│ LLM draft  │───►│ Jev check        │───►│ Noul grounded?      │
│ (writes)   │    │ (state = policy  │    │  p_yes + confidence │
│            │    │  + draft)        │    └──────┬──────┬───────┘
└────────────┘    └──────────────────┘           │      │
                                          PASS   │      │  FAIL
                                          (band  │      │  (hoặc low conf)
                                          HIGH)  │      │
                                          ▼      │      ▼
                                  ┌──────────┐   │  ┌──────────────────┐
                                  │ Dùng     │   │  │ Fallback:        │
                                  │ draft    │   │  │ retry / stricter │
                                  │ → ship   │   │  │ prompt / human   │
                                  └──────────┘   │  └──────────────────┘
                                                 │
                                    MEDIUM band: confirm với người
```

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
import requests

API = "https://api.typesafe.ai/v1/systemone"
HEADERS = {"Authorization": "Bearer <KEY>", "Content-Type": "application/json"}


def verify_draft(policy_text: str, draft: str) -> dict:
    """
    Jev check: draft có grounded theo policy_text không?
    Noul → P(yes), confidence = |p-0.5|*2
    """
    state = (
        f"Policy document:\n{policy_text}\n\n"
        f"Draft output to check:\n{draft}"
    )
    resp = requests.post(
        API,
        headers=HEADERS,
        json={
            "model": "jev-1.13.0",
            "state": state,
            "questions": {
                "grounded": {"type": "noul"},          # có grounded policy?
                "severity": {                           # mức vi phạm nếu fail
                    "type": "score",
                    "levels": ["none", "minor", "major", "critical"],
                },
            },
        },
        timeout=5,
    )
    resp.raise_for_status()
    ans = resp.json()["answers"]
    p_yes = ans["grounded"].get("p_yes", 0.5)
    conf = abs(p_yes - 0.5) * 2
    return {
        "pass": p_yes >= 0.7 and conf >= 0.5,
        "p_yes": p_yes,
        "confidence": conf,
        "severity": ans["severity"].get("score"),
    }


def verified_cascade(policy_text: str, draft: str, max_retries: int = 2) -> str:
    """LLM writes → Jev verifies → pass/fail → fallback."""
    for attempt in range(max_retries + 1):
        v = verify_draft(policy_text, draft)
        if v["pass"] and v["severity"] in (0, "none", None):
            return draft                          # ship
        if v["confidence"] < 0.5:
            escalate_to_human(draft, v)           # Jev mơ hồ → người
            return draft
        draft = llm_regenerate(policy_text, draft, v)   # fail → viết lại
    escalate_to_human(draft, {"reason": "max retries"})
    return draft
```

</details>

### 5.2 Ứng Dụng Trong Harness / Loop

| Nơi | Vai trò verified cascade |
|-----|--------------------------|
| **Harness** | Sau mỗi tool result / mỗi artifact: Jev check pass/fail trước khi tới bước sau ([harness](../../harness/)) |
| **Loop** | Verifier sub-agent dùng Jev cho **fast pre-screen** (Jev pass → tests đầy đủ; Jev fail → reject sớm) ([loop/01-concepts](../../loop/01-concepts/)) |
| **CI** | Check commit message / changelog có grounded với diff không, trước khi merge |

### 5.3 Lưu Ý

| Điểm | Guidance |
|------|----------|
| Primitive | Noul (grounded?) + Score (severity nếu fail) |
| Threshold | p_yes ≥ 0.7 + confidence ≥ 0.5 — **hoặc** dùng Score severity = none để pass |
| Caveat | Jev check theo **policy text trong state** — policy mơ hồ → verify mơ hồ. State hygiene quyết định chất lượng verify |
| Anti-pattern | Đòi Jev "giải thích tại sao draft sai" — nó chỉ trả score/probability |

---

## 6. Ranking & Filtering

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Ranking & Filtering = dùng **Score** (ordered levels) để chấm điểm từng candidate rồi **sort**, hoặc filter bỏ candidate dưới ngưỡng. Probability-weighted score có thể **ngồi giữa 2 level** — liên tục hơn label cứng, tốt cho so sánh thứ hạng.
> **Ẩn dụ/so sánh:** Giống **ban giám khảo chấm thi với rubric 4 mức** — mỗi bài được đặt vào mức (hoặc giữa 2 mức do weighted), rồi xếp hạng theo điểm. Không cần viết lời bình, chỉ cần **điểm + thứ tự**.
> **Vì sao quan trọng:** Đặc biệt mạnh trong **RAG pipeline**: sau retriever trả 20 đoạn, Jev re-rank shortlist theo relevance levels trong vài trăm ms/đoạn — kết hợp được map-reduce và rẻ hơn LLM re-rankers.

### 6.1 Score Levels Cho Re-Ranking

```
   Candidates (từ retriever / DB query)
        │
        ▼  Mỗi candidate → Score decision (parallel)
   ┌────────────┐  ┌────────────┐  ┌────────────┐
   │ candidate A│  │ candidate B│  │ candidate C│
   │ score 3.4  │  │ score 1.8  │  │ score 3.1  │   (weight avg có thể
   │ conf 0.85  │  │ conf 0.60  │  │ conf 0.72  │    nằm GIỮA levels)
   └─────┬──────┘  └─────┬──────┘  └─────┬──────┘
         │               │               │
         ▼               ▼               ▼
   ┌──────────────────────────────────────────────┐
   │  SORT desc theo score → [A(3.4), C(3.1), B] │
   │  FILTER: score < threshold → loại / đẩy cuối │
   │  confidence thấp → giữ nhưng đánh dấu review │
   └──────────────────────────────────────────────┘
```

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
import requests
from typing import List

API = "https://api.typesafe.ai/v1/systemone"
HEADERS = {"Authorization": "Bearer <KEY>", "Content-Type": "application/json"}

RELEVANCE_LEVELS = ["irrelevant", "weak", "relevant", "strong"]


def score_candidate(query: str, passage: str) -> dict:
    state = f"User query:\n{query}\n\nCandidate passage:\n{passage}"
    resp = requests.post(
        API,
        headers=HEADERS,
        json={
            "model": "jev-1.13.0",
            "state": state,
            "questions": {
                "relevance": {"type": "score", "levels": RELEVANCE_LEVELS},
            },
        },
        timeout=5,
    )
    resp.raise_for_status()
    ans = resp.json()["answers"]["relevance"]
    return {
        # probability-weighted score — có thể nằm giữa 2 level
        "score": ans.get("score", ans.get("selected")),
        "confidence": ans.get("confidence", 0.0),
        "probabilities": ans.get("probabilities", {}),
    }


def rerank(query: str, passages: List[str], min_score: float = 1.5) -> List[dict]:
    scored = []
    for p in passages:                          # production: async/map-reduce
        r = score_candidate(query, p)
        r["passage"] = p
        scored.append(r)
    # Sort desc theo weighted score
    scored.sort(key=lambda r: r["score"], reverse=True)
    # Filter: dưới min_score → loại khỏi top-K
    return [r for r in scored if r["score"] >= min_score]


# VD RAG: shortlist = rerank(query, retriever.top20(query), min_score=2.0)
# → lấy 3 passage cao nhất để LLM viết câu trả lời
```

</details>

### 6.2 Lưu Ý

| Điểm | Guidance |
|------|----------|
| Primitive | Score (ordered levels) — weighted score liên tục để sort |
| Combine | Filter (score < t) + sort (desc) + low-confidence flags |
| RAG | Jev re-rank → LLM chỉ nhận top-K passage → rẻ hơn, context gọn hơn |
| Caveat | Sort theo **score**, nhưng cảnh báo khi confidence thấp — candidate score cao conf thấp có thể trượt thứ hạng sai |

---

## 7. Map-Reduce Cuối Cùng

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Map-reduce pattern tổng quát: **mỗi record một decision (map)**, sau đó **gộp kết quả (reduce)** — vote theo bucket confidence, aggregate xác suất, hoặc chuyển low-confidence sang hàng đợi review. **Latency luôn tính theo per-decision** (70–500ms), không tăng theo số record.
> **Ẩn dụ/so sánh:** Giống **đội công chứng viên** — mỗi người xử lý một tập hồ sơ song song (map), trưởng nhóm ký tổng hợp (reduce). Thêm công chứng viên không làm mỗi hồ sơ chậm lại.
> **Vì sao quan trọng:** Đây là lý do Jev fit **workload #2 (map-reduce over datasets)**: chi phí $0.042/1M input + free output + parallel-in-one-pass nội bộ cho nhiều questions → quét toàn bộ dataset là chuyện bình thường.

```
   MAP (song song, per-decision ~70-500ms):
   record_i ──► Jev ──► (label_i, probs_i, conf_i)
                                   │
   REDUCE:                         ▼
   ┌──────────────────────────────────────────────────┐
   │ • Bucket: conf ≥ HIGH → auto                      │
   │ •          LOW ≤ conf < HIGH → review queue       │
   │ •          conf < LOW → escalate / retry state    │
   │ • Aggregate: % mỗi class, P TB, drift so baseline │
   │ • Log: request_id + probs + outcome (không state) │
   └──────────────────────────────────────────────────┘
```

| Thành phần | Quyết định |
|-----------|------------|
| **Map** | state nhỏ/record · questions tối giản · async batch (xem §3) |
| **Reduce** | bucket theo confidence · majority/weighted vote · enqueue review |
| **Latency** | per-decision 70–500ms — tổng wall-clock phụ thuộc batch concurrency |
| **Cost** | $0.042/1M input, free output — scale N record không nổ budget |
| **Eval** | log probs ↔ outcome để tính calibration trên dataset thật |

---

> *"Jev decides, code acts, LLM writes — mọi pattern production đều là một biến thể của câu này."*

---

*Trở về [README](../README.md) — tổng quan Module XIV*

*Tiếp theo: [06 — Jev + LLM: Phân Chia Lao Động](../06-jev-and-llm/) →*

*Trước đó: [04 — Calibration: Xác Suất Thành Thật](../04-calibration/)*
