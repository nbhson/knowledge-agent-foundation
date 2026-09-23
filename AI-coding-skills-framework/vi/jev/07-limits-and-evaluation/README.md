# 🛑 07. Giới Hạn & Đánh Giá

> Phần này liệt kê **Jev không làm được gì**, làm rõ **type-safety ≠ correctness**, hướng dẫn **state hygiene**, **đánh giá trước khi production**, **tuning threshold**, **observability**, **anti-patterns**, và flowchart **khi nào không dùng Jev**. Đọc [README.md](../README.md) trước để có bối cảnh tổng quan Module XIV.

---

## 1. Jev Không Làm Được Gì

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Jev là **System One Model** cho quyết định có schema biết trước — nó **không sinh text, không giải thích, không viết tool args, không đọc file, không xử lý ảnh**, và các bài toán **arithmetic / counting / date comparison** nên giữ trong code.
> **Ẩn dụ/so sánh:** Jev là **đèn giao thông**, không phải **người hướng dẫn** — đèn sáng xanh/vàng/đỏ cực nhanh và đáng tin trong phạm vi đèn, nhưng không thể chỉ đường cho bạn hay giải thích vì sao đèn chuyển màu.
> **Vì sao quan trọng:** Mỗi lần giao sai việc cho Jev (đòi nó viết, tính, giải thích) bạn sẽ thất bại theo cách khó debug nhất: API vẫn trả kết quả *hợp lệ* nhưng **vô nghĩa cho việc đó** — vì nó không sinh text, chỉ trả typed result.

### 1.1 Bảng Giới Hạn Lớn

| Jev KHÔNG... | Lý do | Thay bằng |
|---------------|-------|-----------|
| **Sinh text** | Không text/token generation — chỉ trả Choice/Score/Noul | **LLM** viết |
| **Giải thích / reasoning visible** | Trả probability + confidence, không chuỗi suy luận | LLM giải thích *dựa trên* kết quả Jev |
| **Viết tool arguments** | Không sinh text args → `ToolCallProposed` → fallback | **FallbackModel (LLM)** |
| **Đọc file** | API nhận `state` là string/JSON/array do **code bạn** chuẩn bị | Code đọc file → put vào state |
| **Xử lý ảnh** | Không multimodal input | Pipeline vision riêng / LLM multimodal |
| **Arithmetic / counting / date comparison** | Bài toán chính xác thuần toán — sai số không có chỗ trong calibrated decision | **Code** tính (Python/SQL) |
| **Vượt 64k token context** | Tổng 32k state + longest question; vượt → `ModelHTTPError: max_tokens_exceeded` | Cắt state, tách questions |

### 1.2 "Đọc Sao Cho Dễ"

```
┌────────────────────────────────────────────────────────────────────────┐
│                                                                        │
│    Jev = ĐÈN GIAO THÔNG            KHÔNG PHẢI NGƯỜI HƯỚNG DẪN         │
│                                                                        │
│    ✅ Đèn giao thông làm:          ❌ Người hướng dẫn làm:            │
│       • sáng xanh/vàng/đỏ             • chỉ đường chi tiết            │
│       • trong 70-500ms                • giải thích "vì sao"           │
│       • typed, bounded                • mở bản đồ (đọc file)         │
│       • calibrated (0.8 ≈ 80%)        • tính khoảng cách (arithmetic) │
│       • gần như free                   • viết lời dẫn (text)          │
│                                                                        │
│    → Jev PHÂN LOẠI thế giới vào schema bạn cho.                       │
│    → Code / LLM / người làm phần còn lại.                             │
└────────────────────────────────────────────────────────────────────────┘
```

### 1.3 Code: Giữ Toán Trong Code

```python
# ❌ SAI — đừng hỏi Jev những câu này
jev_decide(state, {"days_until_due": {"type": "score", ...}})   # date compare
jev_decide(state, {"line_count": {"type": "choice", ...}})       # counting
jev_decide(state, {"sum": {"type": "choice", ...}})              # arithmetic

# ✅ ĐÚNG — code tính, Jev phân loại kết quả nếu cần schema
from datetime import date
days_left = (due_date - date.today()).days           # arithmetic trong code
result = jev_decide(
    state=f"Invoice {id} due {due_date}, today {date.today()}, amount {amt}.",
    questions={"urgency": {"type": "choice", "options": ["overdue", "due_soon", "ok"]}},
)                                                     # Jev phân loại MỌI TRẠNG THÁI
```

---

## 2. Type-Safety ≠ Correctness

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Type safety chỉ **đóng không gian answer** — output luôn nằm trong options/levels bạn định nghĩa, không "phát minh" option ngoài schema. Nhưng **nội dung chọn vẫn có thể sai**, đôi khi với **confidence cao**. Đây là hai trục độc lập: *hình dạng đúng* ≠ *nội dung đúng*.
> **Ẩn dụ/so sánh:** Giống **trắc nghiệm có đáp án điền sẵn trên phiếu** — bạn không thể viết đáp án lạ ngoài 4 ô A/B/C/D (type safe), nhưng **vẫn tô sai ô** (incorrect). Phiếu đẹp không đảm bảo trắc nghiệm đúng.
> **Vì sao quan trọng:** Câu quote cần nhớ — **"type safety is not factual correctness"** (Almeida / Hacker News discussion). Mọi design phải thừa nhận: *A closed answer space stops out-of-schema inventions; it does not guarantee the selected category is correct.*

### 2.1 Hai Trục Độc Lập

```
                    Nội dung ĐÚNG          Nội dung SAI
                 ┌────────────────────┬────────────────────┐
   Trong schema  │  Ideal: chọn đúng  │  VẪN XẢY RA:       │
   (type safe)   │  option với conf   │  chọn SAI option    │
                 │  phù hợp           │  trong schema —      │
                 │                    │  đôi khi conf CAO    │
                 ├────────────────────┼────────────────────┤
   Ngoài schema  │  (không có - Jev   │  LLM hallucination: │
   (không safe)  │   luôn đóng shape) │  bịa option lạ      │
                 └────────────────────┴────────────────────┘

   Jev eliminate cột "Ngoài schema" — nhưng ô SAI-trong-schema vẫn tồn tại.
```

### 2.2 Điềm Cảnh Cụ Thể

| Hiện tượng | Giải thích |
|-----------|-----------|
| Jev chọn sai với confidence 0.9 | Phân phối **peak sai chỗ** — model tập trung nhầm option; confidence đo độ tập trung, không đo đúng |
| Type safe nhưng sai class | Label definitions overlap / ambiguous → model forced chọn 1 trong các ô mơ hồ |
| "Không bao giờ hallucinate option" | Đúng — nhưng đó chỉ là **hình dạng**, không phải **sự thật** |

**Hệ quả thiết kế:**
- Đừng bỏ verification chỉ vì "output type-safe rồi".
- Verified cascade ([05](../05-patterns/)) + eval ([§4](#4-đánh-giá-trước-khi-production)) vẫn bắt buộc.
- Confidence band + fallback vẫn cần — kể cả band HIGH ([04](../04-calibration/)).

> **Quote:** *"Type safety is not factual correctness."* — Diogo Almeida / discussion HN
>
> **Quote:** *"A closed answer space stops out-of-schema inventions; it does not guarantee the selected category is correct."*

---

## 3. State Hygiene

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** State hygiene = duy trì **state nhỏ, liên quan, gọn trong latency budget**. Accuracy **tụt khi state chứa detail thừa** (unrelated detail làm nhiễu calibrated decision). Đây là input quality issue — không phải threshold issue.
> **Ẩn dụ/so sánh:** Giống **tầm nhìn của người soát bài** — dán kèm 20 trang không liên quan, họ đọc hết thì chậm và dễ chọn nhầm; chỉ đưa đúng đoạn cần soát thì nhanh và chính xác.
> **Vì sao quan trọng:** State là **input duy nhất** Jev có. State bẩn → probability sai ngay cả khi model calibration tốt. Và state thừa cũng **tốn token** ($0.042/1M) và **rìa 64k limit** (32k state + longest question → `ModelHTTPError: max_tokens_exceeded`).

### 3.1 Nguyên Tắc

```
┌─────────────────────────────────────────────────────────────────────┐
│                     STATE HYGIENE CHECKLIST                          │
│                                                                      │
│  ✅ NÊN:                                                            │
│     • Cắt chỉ phần context LIÊN QUAN tới câu hỏi                   │
│     • Summarize/extract trước khi put vào state                     │
│     • Giữ trong budget: 32k tokens state + longest question ≤ 64k   │
│     • Mỗi question group có state riêng nhỏ (parallel vẫn free)     │
│     • Test: accuracy với state đầy vs state cắt — đo chênh lệch    │
│                                                                      │
│  ❌ KHÔNG NÊN:                                                      │
│     • Ném toàn bộ conversation history / file dump vào state        │
│     • Trộn unrelated detail (log debug, HTML thừa, metadata thừa)   │
│     • Giữ state cũ không prune (PII + cost + drift)                 │
│     • Vượt 64k → ModelHTTPError: max_tokens_exceeded                │
└─────────────────────────────────────────────────────────────────────┘
```

### 3.2 Ví Dụ: Chọn Đúng Đoạn Context

```python
# ❌ SAI — dump toàn bộ repo/file (thừa, dễ vượt budget, accuracy tụt)
state = open("huge_log.txt").read()                     # 40k tokens unrelated

# ✅ ĐÚNG — extract đoạn LIÊN QUAN tới question trước
def build_state(ticket: dict, question: str) -> str:
    # Chỉ phần subject + body đã cắt, bỏ quoted history / signatures
    core = f"{ticket['subject']}\n{ticket['body'][:1500]}"
    return core                                          # nhỏ, liên quan

# Với map-reduce: mỗi record 1 state nhỏ — không cần gộp dataset vào 1 state
# Với questions khác nhau: tách state nếu material khác nhau
#   state_Q1 = extract_for("queue")     ← song song, gần free
#   state_Q2 = extract_for("priority")
```

### 3.3 Đo Ảnh Hưởng Của State

| Experiment | Kỳ vọng |
|-----------|---------|
| State sạch vs state + 30% noise unrelated | Accuracy / confidence distribution lệch → confirm hygiene matter |
| State vượt budget | `ModelHTTPError: max_tokens_exceeded` — fail cứng, không warn soft |
| State PII đầy đủ trong log | Vi phạm privacy — tách storage ([§6](#6-observability-trong-production)) |

---

## 4. Đánh Giá Trước Khi Production

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** **Test trên labelled examples của bạn** — không tin benchmark tổng quát cho domain cụ thể. Đo **calibration thực tế** (prob đã báo vs outcome thật) và **per-class accuracy** trước khi để Jev auto-act. Bắt buộc trước mọi production rollout.
> **Ẩn dụ/so sánh:** Giống **thử thùng nước mới lắp trong nhà** — mở van xem rò rỉ chỗ nào trước khi tin nó cả năm. Eval set = xả nước thử.
> **Vì sao quan trọng:** Guidance 0.8→80% là trung bình; **domain của bạn có thể lệch**. Threshold 0.6 tool-call được chọn trên **một support-ticket set nội bộ nhỏ** — chưa validated cho trường hợp của bạn. Không eval = đang deploy hy vọng.

### 4.1 Xây Eval Set

```
1. Thu thập labelled examples TỪ DATA CỦA BẠN
   (input như production → correct answer do expert/gold label)
2. Chạy Jev trên từng example → ghi (probabilities, confidence, prediction)
3. So prediction vs gold label → các metric dưới đây
4. Với Choice/Score: vẽ calibration curve (bucket P, % đúng thực tế)
5. Tune threshold từ curve → set band HIGH/MEDIUM/LOW
6. Chạy lại holdout — tránh tune & test cùng 1 set
```

### 4.2 Bảng Metrics

| Metric | Câu trả lời | Công thức / cách đọc |
|--------|-------------|----------------------|
| **Calibration (ECE)** | P 0.8 có đúng ~80% không? | Bucket theo P, trung bình \|P − %correct\| |
| **Per-class accuracy** | Class nào Jev hay chọn sai? | Accuracy riêng từng label |
| **Confidence distribution** | Band nào quá nặng LOW/HIGH? | Histogram confidence trên eval set |
| **Near-tie rate** | Bao nhiêu % kết quả margin mỏng? | % (top1 − top2) < ε |
| **Coverage @ threshold** | Ở conf ≥ t, auto-act được bao nhiêu %? | % examples trên ngưỡng |
| **Precision @ auto-act** | Trong phần auto-act, bao nhiêu đúng? | % correct trong bucket HIGH |
| **Escalate load** | Human chịu bao nhiêu ticket? | % dưới threshold |

> **Lưu ý:** danh sách fan-out và nested questions **chưa được đo chuẩn** (chưa có benchmark standard) — nếu dùng, tự đo riêng trên eval set của bạn, đừng so sánh chéo với numbers bên ngoài.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
from collections import defaultdict


def calibration_report(pairs: list[tuple[float, bool]], buckets: int = 10) -> dict:
    """
    pairs = [(predicted_probability_of_selected, was_correct), ...]
    Trả về bảng calibration + ECE.
    """
    bucketed: dict[int, list[bool]] = defaultdict(list)
    for p, correct in pairs:
        b = min(int(p * buckets), buckets - 1)
        bucketed[b].append(correct)

    rows, ece = [], 0.0
    total = sum(len(v) for v in bucketed.values()) or 1
    for b in sorted(bucketed):
        ps = [(b + 0.5) / buckets] * len(bucketed[b])
        p_avg = sum(ps) / len(ps)
        acc = sum(bucketed[b]) / len(bucketed[b])
        n = len(bucketed[b])
        ece += (n / total) * abs(p_avg - acc)
        rows.append({"bucket": f"{b}/{buckets}", "mean_p": round(p_avg, 3),
                     "accuracy": round(acc, 3), "n": n})
    return {"rows": rows, "ece": round(ece, 4)}


def per_class_accuracy(results: list[dict]) -> dict:
    """results = [{gold, pred}, ...] → accuracy từng class."""
    stats = defaultdict(lambda: {"correct": 0, "total": 0})
    for r in results:
        stats[r["gold"]]["total"] += 1
        if r["gold"] == r["pred"]:
            stats[r["gold"]]["correct"] += 1
    return {
        k: {"accuracy": round(v["correct"] / max(v["total"], 1), 3),
            "n": v["total"]}
        for k, v in stats.items()
    }
```

</details>

---

## 5. Tuning Threshold

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** `typesafe_tool_call_threshold` mặc định **0.6** chỉ là **starting point** — nó được chọn trên **một support-ticket set nội bộ nhỏ**, chưa được validate rộng. Tradeoff: **higher → hand off less, and is right more often when it does** (cao hơn → ít handoff hơn, và đúng hơn khi nó handoff). Tune từ **labelled data của bạn**.
> **Ẩn dụ/so sánh:** Giống **cài nhiệt độ điều hòa** — 24°C là mặc định nhà sản xuất; nhà bạn hướng tây thì phải chỉnh. Chọn sai thì vẫn "chạy được" nhưng tốn tiền và không ai thoải mái.
> **Vì sao quan trọng:** Threshold sai tạo hai loại tổn thất ngược nhau: quá thấp → auto-act sai (incident); quá cao → escalate tràn (mất benefit speed/cost, human ngập). Chỉ labelled data của bạn cân được hai bên.

### 5.1 Tradeoff Curve

```
   threshold
       ▲
       │  cao ──► ít handoff hơn         │ higher hand off less,
       │         precision khi handoff ↑  │ and is right more often
       │         nhưng coverage auto-act ↓│ when it does
       │                                  │
       │  thấp ─► nhiều auto-act hơn      │
       │         coverage ↑ nhưng risk ↑  │
       │         human load ↓ nhưng incident ↑
       └──────────────────────────────────► risk tolerance
```

### 5.2 Quy Trình Tune

| Bước | Hành động |
|------|-----------|
| 1 | Chuẩn bị labelled tickets/records (gold answers + outcomes) |
| 2 | Chạy Jev → ghi (confidence, prediction, outcome) |
| 3 | Với mỗi ngưỡng t candidate: tính **precision @ auto-act** và **coverage** |
| 4 | Chọn t sao cho precision ≥ yêu cầu risk (VD 95%) với coverage tốt nhất |
| 5 | **Per-question threshold** — câu gating nguy hiểm cần t cao hơn câu routing vô hại |
| 6 | Log ngưỡng đã áp + outcome → re-tune định kỳ (drift) |

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
def tune_threshold(eval_rows: list[dict],
                   min_precision: float = 0.95) -> dict:
    """
    eval_rows: [{confidence, correct}, ...]  — correct = outcome thật
    Chọn threshold THẤP NHẤT đạt min_precision (tối đa coverage).
    """
    rows = sorted(eval_rows, key=lambda r: r["confidence"], reverse=True)
    best = None
    for i in range(1, len(rows) + 1):
        bucket = rows[:i]                       # confidence >= rows[i-1]
        precision = sum(r["correct"] for r in bucket) / len(bucket)
        threshold = bucket[-1]["confidence"]
        if precision >= min_precision:
            best = {                            # giữ threshold thấp nhất
                "threshold": threshold,
                "precision": round(precision, 3),
                "coverage": round(len(bucket) / len(rows), 3),
            }
        else:
            break                               # thêm case → precision rơi
    return best or {"threshold": 1.0, "precision": None, "coverage": 0.0}


# Áp dụng:
# tuned = tune_threshold(eval_rows, min_precision=0.95)
# settings.typesafe_tool_call_threshold = tuned["threshold"]
#   thay vì mặc định 0.6 chưa validated cho domain bạn
```

</details>

### 5.3 Ghi Nhớ

- Mặc định **0.6 = starting point, not validated** cho use case của bạn.
- Higher threshold → **hand off less, right more often when it does** — nhưng coverage auto-act giảm; cân cả hai axis.
- Tune **per-question** thay vì một số global khi risk các câu khác nhau.

---

## 6. Observability Trong Production

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Observability = log đủ để **tái lập và audit mọi quyết định** (request_id, question names, probabilities, threshold, model version, outcome), theo dõi **confidence drift** theo thời gian, và **không log state** (PII). Đây là "decision audit trail" sống.
> **Ẩn dụ/so sánh:** Giống **hồ sơ bay của máy bay** — mọi thao tác được ghi để phân tích sau này; nhưng không ghi toàn bộ hành khách (PII) vào hộp đen công khai.
> **Vì sao quan trọng:** Không có audit trail thì: incident không truy vết được; calibration không đo được (thiếu outcome link); drift không phát hiện; và rò rỉ PII nếu vô tình log state.

### 6.1 Decision Audit Trail

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    DECISION AUDIT TRAIL                                  │
│                                                                          │
│  request ──► ┌──────────────────────────────────────┐                    │
│  (state,     │ 1. request_id          ← từ Jev resp │                   │
│   questions) │ 2. question_names                     │                   │
│              │ 3. probabilities (full distribution)  │                   │
│              │ 4. confidence          per answer     │                   │
│              │ 5. threshold + band applied           │                   │
│              │ 6. model_version       jev-1.13.0     │                   │
│              │ 7. action taken        allow/route/…  │                   │
│              │ 8. outcome (backfill)  gold label     │                   │
│              │ 9. timestamp                         │                   │
│              └──────────────┬───────────────────────┘                   │
│                             │                                            │
│          KHÔNG GHI: state (raw) — PII                                   │
│          (hash/redact nếu bắt buộc debug, storage riêng ACL)            │
│                             │                                            │
│                             ▼                                            │
│              ┌──────────────────────────────┐                           │
│              │ Query được:                  │                           │
│              │ • "ticket #4821 sao route?"  │                           │
│              │ • calibration curve / drift  │                           │
│              │ • threshold đã áp hôm đó     │                           │
│              └──────────────────────────────┘                           │
└─────────────────────────────────────────────────────────────────────────┘
```

### 6.2 Checklist Production

| Thành phần | Làm gì |
|-----------|--------|
| **Log** | request_id · question names · probabilities · confidence · threshold/band · model version · outcome · timestamp |
| **Không log** | state raw · full text input (PII) |
| **Drift watch** | Theo dõi distribution của confidence + % band theo thời gian — lệch bất thường → input drift / version change |
| **Calibration rollup** | Định kỳ gộp (probability ↔ outcome) → ECE per class |
| **Version pin** | Ghi `jev-1.13.0` cụ thể (đừng chỉ `jev-latest` khi audit) — alias đổi được, số version không |
| **PII** | State chứa PII → tách vault/storage; log chỉ metadata |

Xem chi tiết mẫu log entry: [04 — Logging & Observability](../04-calibration/#6-logging--observability).

---

## 7. Anti-Patterns

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Danh sách các cách **sai phổ biến** khi đưa Jev vào production — mỗi cái dẫn đến một mode thất bại im lặng (silent failure): kết quả sai nhưng hệ thống tin tưởng.
> **Ẩn dụ/so sánh:** Giống **8 lỗ hổng trên bo mạch** — máy vẫn chạy, đến lúc nào đó cháy.
> **Vì sao quan trọng:** Hầu hết incident với Jev không đến từ model "dở" mà đến từ **kỳ vọng sai** (coi nó là oracle) và **thiếu fallback/eval**.

| # | Anti-pattern | Vì sao sai | Thay bằng |
|---|-------------|-----------|-----------|
| 1 | **Dùng Jev như oracle** | Nó calibrated cho schema biết trước, không phải sự thật tuyệt đối | Type-safe ≠ correct ([§2](#2-type-safety--correctness)) |
| 2 | **Đòi explanation từ Jev** | API không trả reasoning chain | LLM giải thích *sau* khi có kết quả Jev |
| 3 | **Câu hỏi multi-factor** (1 Choice gộp 5 tiêu chí) | Phân phối flat → confidence thấp triền miên, auto-act ít | Tách nhiều questions (parallel, gần free) |
| 4 | **Nhét question vào prompt** (state = "chọn A hay B") | State phải là **material**, câu hỏi goes into `questions` | `state=data`, `questions=choice` |
| 5 | **Tin confidence cao mù quáng** | Confidence = độ tập trung, kể cả khi sai trong schema | Luôn có fallback + band rules ([04](../04-calibration/)) |
| 6 | **Không fallback khi low confidence** | Band LOW mà vẫn auto-act = auto-incident | Escalate human / LLM / retry |
| 7 | **Bỏ qua eval** | Dùng 0.6/0.8 mặc định, không đo domain thật | Eval set + calibration curve ([§4](#4-đánh-giá-trước-khi-production)) |
| 8 | **Không hygiene state** | Detail thừa → accuracy tụt + vượt 64k → `max_tokens_exceeded` | State nhỏ, liên quan ([§3](#3-state-hygiene)) |
| 9 | **Dùng Jev để gửi mail / charge / xoá** (tool side-effect) | Jev **phân loại** — không phán xét an toàn tuyệt đối, không sinh args | Gating Noul + auth layer + LLM args ([05 §4](../05-patterns/), [06 §3](../06-jev-and-llm/)) |

---

## 8. Khi Nào Không Dùng Jev

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Quy tắc chọn công cụ: **cần text → LLM**; **cần chính xác toán/đếm/ngày → code**; **cần judgment nhanh trong schema biết trước → Jev**. Đây không phải ranking "tool nào tốt" mà là **phân công theo năng lực**.
> **Ẩn dụ/so sánh:** Giống chọn dụng cụ nhà bếp — dao gọt (Jev cắt quyết định), máy xay (LLM xay text), cân điện tử (code đính chính xác). Dùng dao để cân → hỏng cả dao lẫn cân.
> **Vì sao quan trọng:** Mỗi lần chọn sai tool, bạn mất cả hai: vừa không đạt việc (Jev không viết được text), vừa tốn tiền (gọi LLM cho việc 5ms routing).

### 8.1 Flowchart Chọn Công Cụ

```
                    ┌─────────────────────────┐
                    │  Bắt đầu: cần gì?       │
                    └────────────┬────────────┘
                                 │
              ┌──────────────────┼──────────────────┐
              ▼                  ▼                  ▼
     Cần TEXT / giải thích  Cần tính chính xác  Cần judgment NHANH
     / sinh args / đọc file  (arithmetic, count,  trong schema BIẾT TRƯỚC
              │               date compare)        (route, classify,
              ▼                  │                 gate, verify, rank)
     ┌─────────────────┐        ▼                  │
     │      LLM        │  ┌──────────┐             ▼
     │  (writes /      │  │   CODE   │   ┌──────────────────────┐
     │   explanations) │  │ (Python/ │   │        JEV           │
     └─────────────────┘  │  SQL)    │   │  System One Model    │
                          └──────────┘   │  Choice/Score/Noul   │
                                         │  70-500ms · calibrated│
                                         └──────────────────────┘

     KẾT HỢP THƯỜNG: Jev decide → threshold → (cần text?) → LLM viết
                     mọi side-effect tool → code + auth + optional Jev gate
```

### 8.2 Bảng Quyết Định Nhanh

| Tình huống | Dùng | Vì sao |
|-----------|------|--------|
| Route ticket vào queue | **Jev** | Schema fixed, 70–500ms, free-ish |
| Gate "authorize xoá?" | **Jev Noul** + auth layer | Margin-based, calibrated; auth giữ quyền cuối |
| Viết email trả khách | **LLM** | Cần text |
| Giải thích "tại sao chọn queue này" | **LLM** (từ probs Jev) | Jev không giải thích |
| Tính days-left / tổng tiền | **Code** | Chính xác tuyệt đối |
| Đọc file / log | **Code** → put vào state | Jev không đọc file |
| Verify draft có grounded policy | **Jev Noul** (state = policy + draft) | Yes/no trong schema, nhanh |
| Sinh tool args phức tạp | **FallbackModel (LLM)** | Jev không sinh text args |
| Re-rank 20 passage theo relevance | **Jev Score** + code sort | Song song, rẻ |
| Không có schema / exploratory | **LLM** | Jev cần answer space đóng |

---

> *"Biết giới hạn của công cụ là bước đầu của engineering. Jev decide — code act — LLM write — và bạn giữ quyền override ở mọi band."*

---

*Trở về [README](../README.md) — tổng quan Module XIV*

*Trước đó: [06 — Jev + LLM: Phân Chia Lao Động](../06-jev-and-llm/)*
