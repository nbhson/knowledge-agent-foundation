# 🎯 04. Calibration — Xác Suất Thành Thật

> Phần này giải thích **xác suất được calibrate nghĩa là gì**, tại sao **confidence ≠ xác suất đúng**, cách **đọc distribution thay vì chỉ xem đáp án**, cũng như **thresholding & bands** để biến xác suất thành hành động production. Đọc [README.md](../README.md) trước để có bối cảnh tổng quan về Module XIV — Jev & System One Models.

---

## 1. Xác Suất Được Calibrate Nghĩa Là Gì?

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Calibration (tính được hiệu chỉnh) nghĩa là **xác suất bạn báo ra khớp với tần suất thực tế**. Nếu Jev nói "câu này đúng với xác suất 0.8" trên hàng nghìn câu hỏi, thì khoảng ~80% trong số đó thực sự đúng. Đây là *"epistemically honest probabilities"* — xác suất trung thực với những gì mô hình thực sự biết.
> **Ẩn dụ/so sánh:** Giống **một người thợ đo may có thước đo đúng chuẩn** — khi anh ta nói "cái này dài 10cm", kiểm lại thì đúng 10cm. Người đo tệ (overconfidence) thì nói "10cm" nhưng thực tế dao động 6–14cm: nghe tự tin nhưng không đáng tin.
> **Vì sao quan trọng:** Mọi downstream logic — auto-act khi tự tin, escalate khi mơ hồ — đều đứng trên giả định "số 0.8 nghĩa là 0.8". Nếu xác suất không calibrate, toàn bộ pipeline thresholding trở thành ảo giác.

### 1.1 LLM Overconfidence vs Jev Calibration

LLM thường **overconfidence**: sinh ra văn bản với giọng điệu chắc nịch ngay cả khi sai, và "token probability" không trực tiếp tương ứng với độ đúng của câu trả lời tổng thể. Jev được tối ưu để xác suất của nó **khớp với outcome thực tế**:

```
┌─────────────────────────────────────────────────────────────────┐
│                    CALIBRATION SO SÁNH                          │
│                                                                  │
│  LLM:   "Chắc chắn 99%!"  ──►  thực tế đúng ~60-70% (hay thấp) │
│         overconfidence, giọng điệu ≠ xác suất                   │
│                                                                  │
│  Jev:   P = 0.8           ──►  thực tế đúng ~80%                │
│         xác suất được tối ưu chống lại outcome                   │
└─────────────────────────────────────────────────────────────────┘
```

Điểm then chốt: **~80% câu trả lời được chấm điểm 0.8 là đúng** — đây là số đo calibration, không phải slogan.

### 1.2 Bảng So Sánh RLHF vs RLVR vs RLCD

Jev được train bằng **RLCD (Reinforcement Learning for Calibrated Decisions)** — thứ làm nên sự khác biệt trong cách xác suất hình thành:

| Thuật toán | Tối ưu cái gì? | Nhược điểm với quyết định |
|------------|----------------|---------------------------|
| **RLHF** | Preferences của con người ("cái này hay hơn") | Xác suất phản ánh sở thích, không phản ánh outcome; hay overconfident |
| **RLVR** | Verification đúng/sai (rule-based rewards) | Tốt hơn cho correctness, nhưng vẫn thiếu tín hiệu "biên độ" xác suất |
| **RLCD** | **Probabilities tối ưu chống lại outcomes** | Không cần human preferences; xác suất = dự đoán điều gì sẽ xảy ra → calibrate |

Jev **không phải LLM** — không sinh text, không token generation. Nó là transformer-based, train trên synthetic data qua RLCD: **kết quả cuối cùng của một quyết định** (outcome) là phần thưởng, chứ không phải "người thích câu trả lời nào". Nhờ vậy xác suất đầu ra là **thông kê về thế giới**, không phải về văn phong.

---

## 2. confidence ≠ Xác Suất Đúng

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** `confidence` (Choice/Score) là **độ tập trung của phân phối xác suất** — phân phối càng "peaked" (nhọn) thì confidence càng tiến gần 1.0. Nó là **margin** (biên độ), **không phải** xác suất câu trả lời đúng. Với Noul, `confidence = |p − 0.5| × 2`.
> **Ẩn dụ/so sánh:** Giống **độ rõ của tiếng radio**: confidence cao = tín hiệu rõ ràng đến mức hầu như không có nhiễu. Nhưng tín hiệu rõ ràng **không đảm bảo trạm đang phát đúng bài bạn muốn** — có thể tín hiệu rõ nhưng sai đài. "Confidence là độ rõ ràng, không phải độ đúng."
> **Vì sao quan trọng:** Nhầm confidence = probability of correctness dẫn đến hai sai lầm chết người: (1) auto-act trên confidence 0.95 của một câu trả lời **sai trong schema**; (2) escalate vô ích vì nghĩ "confidence thấp = chắc sai" trong khi đó chỉ là phân phối flat vì input mơ hồ.

### 2.1 Choice & Score — Confidence Là Độ Tập Trung Phân Phối

```
Phân phối PEAKED (confidence cao ≈ 1.0):     Phân phối FLAT (confidence thấp):

  option A ████████████████████ 0.92           option A ████ 0.28
  option B ██ 0.05                             option B ███ 0.26
  option C █ 0.03                              option C ███ 0.24
                                               option D ██ 0.22
  → độ tập trung cao → confidence ≈ 0.9       → dàn trải → confidence thấp
  → NHƯNG option A vẫn có thể SAI!             → mơ hồ thật sự (ambiguity)
```

**Điều quan trọng nhất**: Jev có thể chọn một đáp án **sai nhưng nằm trong schema** với confidence cao. Type safety chỉ đóng hình dạng output — không đảm bảo nội dung đúng. Confidence đo *"mô hình có rõ ràng không"*, không đo *"mô hình có đúng không"*.

### 2.2 Noul — Confidence Là Margin Từ 0.5

Với Noul (yes/no), `P(yes)` nằm trong [0, 1] và confidence được tính bằng **khoảng cách tới 0.5**:

```
confidence = |p − 0.5| × 2

  p = 0.01  →  |0.01 − 0.5| × 2 = 0.98   → confidence rất cao (gần như chắc NO)
  p = 0.45  →  |0.45 − 0.5| × 2 = 0.10   → confidence rất thấp (gần cân bằng)
  p = 0.99  →  |0.99 − 0.5| × 2 = 0.98   → confidence rất cao (gần như chắc YES)
  p = 0.50  →  |0.50 − 0.5| × 2 = 0.00   → cân bằng hoàn toàn
```

**P gần 0.5 = balanced, KHÔNG PHẢI "medium/trung bình"** — nghĩa là mô hình phân vân thật sự giữa yes và no, không phải "trung bình có". Noul **không có confidence riêng** — confidence suy ra trực tiếp từ margin này.

### 2.3 Tóm Tắt Ba Khái Niệm Dễ Nhầm

| Khái niệm | Đo cái gì? | Không đo cái gì? |
|-----------|-----------|-------------------|
| **probability (P)** | Xác suất outcome xảy ra (Choice/Score: phân phối trên options; Noul: P(yes)) | — |
| **confidence (Choice/Score)** | Độ tập trung/phân phối (peaked → 1.0) | Không phải P(đúng) |
| **confidence (Noul)** | Margin từ 0.5: \|p−0.5\|×2 | Không phải P(đúng) riêng biệt |

> **A closed answer space stops out-of-schema inventions; it does not guarantee the selected category is correct.**

---

## 3. Đọc Distribution Thay Vì Chỉ Xem Đáp Án

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** API Jev trả về **cả phân phối đầy đủ** trên mọi option (Choice) hay mọi level (Score), không chỉ option thắng. Đọc phân phối cho phép bạn nhận ra **ambiguity** (mơ hồ), near-ties (gần hòa), và margin — thay vì xử lý kết quả như một label cứng.
> **Ẩn dụ/so sánh:** Giống **bảng tỷ lệ bầu cử thay vì chỉ tên người thắng** — 51% vs 49% khác hoàn toàn 90% vs 10% dù cùng một người thắng. Chỉ nhìn "ai thắng" là bỏ đi toàn bộ câu chuyện.
> **Vì sao quan trọng:** Flat distribution là tín hiệu escalate tự nhiên nhất: khi hai option gần bằng nhau, hệ thống nên đưa người vào thay vì auto-act. Nếu chỉ đọc `selected`, bạn vứt bỏ chính signal này.

### 3.1 Hai Loại Kết Quả Cần Phân Biệt

```
┌── PEAKED (đọc để AUTO-ACT) ──────────┐  ┌── FLAT (đọc để ESCALATE) ──────────┐
│                                       │  │                                     │
│  billing_issue  ████████████████ 0.86 │  │  billing_issue  ████████ 0.31       │
│  refund_request ███ 0.08              │  │  refund_request ███████ 0.29        │
│  general        ██ 0.06               │  │  general        ██████ 0.24         │
│                                       │  │  account_access ████ 0.16           │
│  selected = billing_issue             │  │                                     │
│  confidence ≈ cao                     │  │  selected = billing_issue (nhưng...) │
│  → Hành động được                     │  │  confidence ≈ thấp                   │
│                                       │  │  → Hỏi người / thêm context         │
└───────────────────────────────────────┘  └─────────────────────────────────────┘
```

### 3.2 Những Gì Phân Phối Cho Biết Mà Label Không Cho

- **Margin**: chênh lệch giữa option thắng và option nhì — margin mỏng = rủi ro.
- **Ambiguity**: phân phối flat = input không đủ để phân biệt — cần thêm state.
- **Ambiguity tập trung ở đâu**: nếu 0.4/0.4 giữa 2 option, câu hỏi có thể poorly designed (2 option overlap).
- **Multimodal**: phân phối nhọn ở 2 đỉnh xa nhau = có thể input chứa 2 chủ đề trộn lẫn.

**Code mẫu** đọc cả distribution:

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
import requests

API = "https://api.typesafe.ai/v1/systemone"
HEADERS = {
    "Authorization": "Bearer <YOUR_KEY>",
    "Content-Type": "application/json",
}

def decide(model: str, state, questions: dict) -> dict:
    resp = requests.post(
        API,
        headers=HEADERS,
        json={"model": model, "state": state, "questions": questions},
        timeout=5,
    )
    resp.raise_for_status()
    return resp.json()

def read_distribution(answer: dict) -> dict:
    """
    Trích xuất phân phối đầy đủ từ một Choice answer.
    answer chứa: selected + full distribution (probabilities trên options).
    """
    probs = answer.get("probabilities", {})
    ranked = sorted(probs.items(), key=lambda kv: kv[1], reverse=True)
    top, second = ranked[0], ranked[1] if len(ranked) > 1 else (None, 0.0)
    margin = (top[1] - second[1]) if second[0] is not None else top[1]
    return {
        "selected": top[0],
        "top_p": top[1],
        "margin": margin,
        "flat": margin < 0.15,          # gần hòa → escalate
        "full": dict(ranked),
    }

result = decide(
    model="jev-1.13.0",
    state="Khách hàng phản ánh bị trừ tiền 2 lần cho cùng một đơn hàng #4821.",
    questions={
        "ticket_type": {
            "type": "choice",
            "options": ["billing_issue", "refund_request", "general", "account_access"],
        }
    },
)

analysis = read_distribution(result["answers"]["ticket_type"])
print(analysis)
# {'selected': 'billing_issue', 'top_p': 0.86, 'margin': 0.78,
#  'flat': False, 'full': {...}}

if analysis["flat"]:
    escalate_to_human(analysis)          # phân phối flat → đừng auto-act
else:
    route_ticket(analysis["selected"])   # peaked → hành động được
```

</details>

---

## 4. Thresholding & Bands

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Thresholding là **chuyển xác suất/confidence thành hành động** bằng cách so với các ngưỡng (bands): cao → code auto-acts, trung bình → confirm/thêm context, thấp → route sang người hoặc hệ thống khác (LLM). Đây là "pháp luật" của luồng quyết định.
> **Ẩn dụ/so sánh:** Giống **đèn giao thông** cho dữ liệu: xanh = đi (auto-act), vàng = dừng lại kiểm tra (confirm), đỏ = nhường quyền cho người (escalate). Không đèn thì xe chạy hỗn loạn; đèn sai thì tai nạn.
> **Vì sao quan trọng:** Không threshold = mọi kết quả Jev treated như nhau — hoặc auto-act liều lĩnh trên mọi câu, hoặc escalate mọi câu và mất hết lợi thế tốc độ. Band phải được **chọn từ labelled data của bạn**, không phải chốt cứng từ đầu.

### 4.1 Ba Band Hướng Dẫn

```
┌────────────────────────────────────────────────────────────────────────┐
│                    CONFIDENCE BANDS                                    │
│                                                                        │
│   HIGH            │ MEDIUM          │ LOW                              │
│   (≥ ~0.8)        │ (~0.5–0.8)      │ (< ~0.5)                         │
│                    │                  │                                  │
│   Code AUTO-ACTS  │ Confirm với      │ Route to HUMAN                   │
│   trên kết quả    │ user / lấy thêm  │ hoặc another system / LLM        │
│                    │ context          │                                  │
│   VD: route ticket │ VD: hiện option  │ VD: escalate ticket mơ hồ,       │
│   vào queue ngay   │ cho user xác nhận│ hỏi lại LLM với prompt đầy đủ    │
└────────────────────────────────────────────────────────────────────────┘
```

| Band | Ngưỡng gợi ý | Hành động | Ví dụ |
|------|--------------|-----------|-------|
| **High** | ≥ ~0.8 | Auto-act | Route ticket, apply label, cho tool call chạy |
| **Medium** | ~0.5–0.8 | Confirm / thêm context | Hiện kết quả cho user duyệt, bổ sung state |
| **Low** | < ~0.5 | Escalate | Human review, fallback sang LLM, retry với state khác |

> Ngưỡng cụ thể **phải tune từ labelled data của bạn** — 0.8 chỉ là starting point mang tính guidance.

### 4.2 Cách Chọn Threshold Từ Labelled Data

```
1. Thu thập labelled examples (input → correct answer) từ domain của bạn
2. Chạy Jev trên từng example → ghi (probabilities, outcome)
3. Vẽ calibration curve: bucket theo P, đo % đúng thực tế
4. Chọn threshold theo tolerance rủi ro:
     - Auto-act được phép sai bao nhiêu? → đặt high-band sao cho precision đủ
     - Escalate tốn bao nhiêu human time? → đặt low-band cân bằng load
5. Áp dụng per-question threshold nếu các câu hỏi có risk khác nhau
```

**Per-question threshold**: một câu routing vô hại có thể auto-act ở 0.7, trong khi câu gating hành động phá hoại cần 0.95+. Không phải mọi question dùng chung một band.

### 4.3 Pipeline Threshold Chuẩn

```
                    ┌──────────────────┐
   state ──────────►│   Jev decide     │
   questions ──────►│  (parallel,      │
                    │   70-500ms)      │
                    └────────┬─────────┘
                             │ answer + probabilities + confidence
                             ▼
                    ┌──────────────────┐
                    │  Đọc answer      │
                    │  + distribution  │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐     ┌─────────────────────┐
                    │  So confidence   │     │  Nếu flat/near-tie │
                    │  với threshold   ├────►│  → escalate bất     │
                    │  (per-question)  │     │    kể confidence    │
                    └────────┬─────────┘     └─────────────────────┘
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
         HIGH (auto)    MEDIUM (confirm)  LOW (escalate)
         code acts      user / context    human / LLM
```

**Lưu ý**: ngay cả khi confidence cao, một phân phối **flat bất thường** (margin rất mỏng giữa 2 option) vẫn nên trigger escalate — confidence và margin nên được đọc **cùng nhau**.

---

## 5. Code Pipeline Mẫu

Pipeline hoàn chỉnh: gọi Jev → đọc probabilities + confidence → so threshold → act / confirm / escalate.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
import requests
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, Optional

API = "https://api.typesafe.ai/v1/systemone"
MODEL = "jev-1.13.0"  # alias: jev-latest
HEADERS = {"Authorization": "Bearer <YOUR_KEY>", "Content-Type": "application/json"}


class Band(Enum):
    HIGH = "high"        # auto-act
    MEDIUM = "medium"    # confirm / more context
    LOW = "low"          # escalate to human / LLM


@dataclass
class Decision:
    question: str
    selected: Any
    probabilities: Dict[str, float]
    confidence: float
    band: Band
    request_id: Optional[str]
    model_version: str


def noul_confidence(p_yes: float) -> float:
    """Noul confidence = margin từ 0.5."""
    return abs(p_yes - 0.5) * 2


def classify_band(confidence: float, high_t: float, low_t: float) -> Band:
    if confidence >= high_t:
        return Band.HIGH
    if confidence >= low_t:
        return Band.MEDIUM
    return Band.LOW


def ask_jev(state: str, questions: dict) -> dict:
    resp = requests.post(
        API,
        headers=HEADERS,
        json={"model": MODEL, "state": state, "questions": questions},
        timeout=5,
    )
    resp.raise_for_status()
    return resp.json()


def decide_with_bands(
    state: str,
    questions: dict,
    thresholds: Dict[str, tuple] = None,
) -> list[Decision]:
    """
    thresholds: {question_name: (low_t, high_t)} — per-question.
    Mặc định: low=0.5, high=0.8 (guidance, tune từ labelled data).
    """
    thresholds = thresholds or {}
    payload = ask_jev(state, questions)
    request_id = payload.get("request_id")
    decisions = []

    for name, ans in payload.get("answers", {}).items():
        low_t, high_t = thresholds.get(name, (0.5, 0.8))

        if ans.get("type") == "noul" or "p_yes" in ans:
            # Noul: confidence = |p - 0.5| * 2
            p_yes = ans.get("p_yes", ans.get("probability_yes", 0.5))
            selected = p_yes >= 0.5
            confidence = noul_confidence(p_yes)
            probs = {"yes": p_yes, "no": 1 - p_yes}
        else:
            # Choice / Score
            probs = ans.get("probabilities", {})
            selected = ans.get("selected")
            confidence = ans.get("confidence", 0.0)

        band = classify_band(confidence, high_t, low_t)
        decisions.append(Decision(
            question=name,
            selected=selected,
            probabilities=probs,
            confidence=confidence,
            band=band,
            request_id=request_id,
            model_version=MODEL,
        ))
    return decisions


def act(state: str, questions: dict) -> None:
    for d in decide_with_bands(state, questions):
        if d.band is Band.HIGH:
            auto_act(d.selected)                 # code tự hành động
        elif d.band is Band.MEDIUM:
            confirm_with_user(d)                 # hiện cho user xác nhận
        else:
            escalate_to_human_or_llm(d)          # route sang người / LLM


# --- Ví dụ: routing ticket ---
questions = {
    "queue": {
        "type": "choice",
        "options": ["billing", "tech_support", "sales", "churn_risk"],
    },
    "priority": {
        "type": "score",
        "levels": ["p0", "p1", "p2", "p3"],
    },
}
# act(ticket_text, questions)
```

</details>

---

## 6. Logging & Observability

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Logging cho decision pipeline = ghi lại **đủ thông tin để tái lập và audit một quyết định**: request id, question names, probabilities, confidence, threshold áp dụng, model version, và outcome thật (sau này). Confidence là **signal để threshold**; log là **bằng chứng để audit**.
> **Ẩn dụ/so sánh:** Giống **hồ sơ phẫu thuật** — không ghi nội dung con người (state/PII), nhưng ghi bác sĩ nào, phương pháp nào, ngưỡng nào, và kết quả ra sao, để khi có biến chứng thì truy vết được.
> **Vì sao quan trọng:** Không log → hai tháng sau bạn không giải thích được "tại sao ticket này bị auto-route sai?", và không thể tune threshold vì mất linkage giữa probability khi quyết định với outcome thực tế.

### 6.1 Checklist Log

```
┌─────────────────────────────────────────────────────────────────────┐
│                   DECISION AUDIT LOG                                │
│                                                                     │
│  ✅ LOG:                                                            │
│     • request_id            (từ response Jev)                      │
│     • question names        (tên các questions đã hỏi)             │
│     • probabilities          (phân phối đầy đủ)                    │
│     • confidence             (per answer)                           │
│     • threshold / band       (ngưỡng đã áp, high/medium/low)       │
│     • model version          (jev-1.13.0 / jev-latest)             │
│     • outcome                (label thật, phản hồi user, ...)       │
│     • timestamp                                                   │
│                                                                     │
│  ❌ KHÔNG LOG:                                                      │
│     • state (raw)             ← có thể chứa PII                    │
│     • full text input         ← customer data, emails, ...         │
│                                                                     │
│  ⚠️  Nếu cần debug state: hash/redact trước, hoặc giữ trong        │
│     storage có access control riêng                                 │
└─────────────────────────────────────────────────────────────────────┘
```

### 6.2 Mẫu Log Entry

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
import json
import time
from typing import Any, Dict


def log_decision(
    request_id: str,
    question_names: list[str],
    probabilities: Dict[str, float],
    confidence: float,
    threshold: tuple[float, float],
    band: str,
    model_version: str,
    outcome: Any = None,
) -> str:
    """
    Ghi MỘT decision entry. KHÔNG nhận state — caller chỉ pass metadata.
    """
    entry = {
        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "request_id": request_id,
        "questions": question_names,
        "probabilities": probabilities,      # phân phối đầy đủ
        "confidence": round(confidence, 4),
        "threshold_low": threshold[0],
        "threshold_high": threshold[1],
        "band": band,                        # high / medium / low
        "model": model_version,
        "outcome": outcome,                  # điền sau khi biết kết quả thật
    }
    line = json.dumps(entry, ensure_ascii=False)
    # Append vào decision log (file / warehouse) — KHÔNG chứa state
    with open("decisions.jsonl", "a") as f:
        f.write(line + "\n")
    return line


def backfill_outcome(request_id: str, outcome: Any):
    """Sau khi biết kết quả thật → ghi đè outcome để tính calibration."""
    # Trong practice: update row trong DB theo request_id
    ...
```

</details>

### 6.3 Vì Sao Outcome Quan Trọng

Log chỉ có nghĩa khi **liên kết được probability ↔ outcome**. Với cặp `(probabilities, outcome)` bạn có thể:

1. **Đo calibration thực tế** trên domain của bạn (không chỉ tin 0.8 → 80%).
2. **Tune threshold**: nếu band high (≥0.8) thực tế chỉ đúng 70% → nâng ngưỡng.
3. **Phát hiện drift**: confidence distribution lệch theo thời gian = input distribution thay đổi hoặc model version đổi.
4. **Audit khi incident**: "ticket #4821 bị auto-route sai vì confidence 0.82 nhưng outcome = sai" → truy vết được cả request_id lẫn ngưỡng.

---

> *"Confidence là signal để bạn quyết định auto-act hay escalate — không phải lý do để ngừng suy nghĩ."*

---

*Trở về [README](../README.md) — tổng quan Module XIV*

*Tiếp theo: [05 — Patterns: Xây Dựng Quyết Định Production](../05-patterns/) →*

*Trước đó: [03 — Confidence & Probability](../03-confidence/)*
