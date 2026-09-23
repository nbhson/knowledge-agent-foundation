# 🔬 01. Khái Niệm — Jev & System One Models

> Phần này giải thích **Jev là gì**, vì sao nó **không phải LLM**, sự khác biệt giữa **System One và System Two** theo Kahneman, **lịch sử & tên gọi**, **kiến trúc tổng quan**, lý do **bỏ generate text**, khi nào **dùng / không dùng**, và **vai trò trong hệ sinh thái agent**. Đọc [README.md](../README.md) trước để có bối cảnh tổng quan Module XIV.

---

## 1. Jev Là Gì?

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Jev là **non-generative decision model** — mô hình **không sinh text** do TypeSafe AI phát hành; nhận **unstructured state** (string / JSON / array of text) và trả về **typed probabilistic decisions** kèm phân phối xác suất — được TypeSafe gọi là *"frontier-intelligence function call"*.
> **Ẩn dụ/so sánh:** Giống **một function call có kiểu trả về** thay vì một chatbot: `decide(state, questions) → answers`. Hay như **đèn giao thông** — bạn không nhờ đèn giao thông "kể chuyện về lý do nên đi"; nó chỉ trả về **đỏ / xanh** kèm xác suất, và phần mềm dùng ngay được.
> **Vì sao quan trọng:** Hầu hết bước trong workflow agent chỉ cần *"quyết định này là gì, tự tin bao nhiêu"* — không cần văn xuôi. Jev trả lời đúng nhu cầu đó với latency 70-500ms và giá $0.042/M input tokens, output free.

### 1.1 Định Nghĩa Một Dòng

```
┌──────────────────────────────────────────────────────────────────┐
│  JEV = "frontier-intelligence function call"                     │
│                                                                  │
│  Unstructured state in  ──►  Typed probabilistic decisions out   │
│  (string / JSON / array)      (Choice / Score / Noul + probs)    │
└──────────────────────────────────────────────────────────────────┘
```

**Jev KHÔNG phải LLM:**

| Tính chất | LLM | Jev |
|-----------|-----|-----|
| Sinh text / token | ✅ Có | ❌ Không |
| Output | Văn xuôi / code | Typed decisions + xác suất |
| Dùng cho | Con người đọc | **Phần mềm consume trực tiếp** |
| Cần parse JSON | Thường (regex / tool-use) | Không — output đã có kiểu |
| Latency | 3-329s | 70-500ms |

### 1.2 Phiên Bản Hiện Tại

```
Early access (invite):  15/09/2026
Public (no waitlist):   20/09/2026
Version hiện tại:       jev-1.13.0   (alias: jev-latest)
API:                    POST https://api.typesafe.ai/v1/systemone
```

---

## 2. System One vs System Two (Kahneman)

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Jev đặt tên theo **dual-process theory** trong *Thinking, Fast and Slow* của Daniel Kahneman — **System 1** = suy nghĩ nhanh, trực giác, tự động, nhiều lần mỗi ngày; **System 2** = suy nghĩ chậm, thận trọng, có lý do, tốn sức. LLM frontier vận hành như **System 2** (viết lập luận từng bước); Jev được thiết kế cho **System 1** — quyết định nhanh, có cấu trúc, không cần lời giải thích.
> **Ẩn dụ/so sánh:** Khi bạn chạm vào lò nóng, **System 1** rụt tay lại **trước khi System 2 kịp nói "nóng"**. Jev là cú rụt tay đó của agent: gate, route, classify trong 70-500ms. LLM là phần bạn **ngồi giải thích sau đó**.
> **Vì sao quan trọng:** Sai lầm thiết kế phổ biến là gọi System 2 cho việc của System 1 — vừa chậm vừa đắt. Phân chia đúng hai lớp cho agent latency thấp, chi phí thấp, và **calibrated** (xác suất match outcome).

### 2.1 Bảng So Sánh LLM vs Jev

```
┌─────────────────┬──────────────────────────┬──────────────────────────┐
│                 │  LLM (System Two)        │  JEV (System One)        │
├─────────────────┼──────────────────────────┼──────────────────────────┤
│ Main job        │  Sinh text có nghĩa      │  Trả typed decision      │
│ Post-training   │  RLHF / instructions     │  RLCD (calibrated vs     │
│                 │  (human preferences)     │  outcomes, synthetic     │
│                 │                          │  data only)              │
│ Sampling        │  Autoregressive token    │  Parallel question pass  │
│                 │  by token                │  (1 pass, song song)     │
│ Output          │  Text / tokens           │  Typed answers + probs   │
│ Output shape    │  Mở (open-ended)         │  Đóng (closed schema)    │
│ Uncertainty     │  "Tự tin 90%" không      │  Calibrated: ~80% câu    │
│                 │  calibrated              │  trả lời @0.8 là đúng    │
│ Latency         │  3-329s                  │  70-500ms                │
│ Price           │  Theo token sinh ra      │  $0.042/M in, output free│
│ Best fit        │  Chat, code, viết, giải │  Route, classify, gate,  │
│                 │  thích, brainstorm       │  score, verify           │
└─────────────────┴──────────────────────────┴──────────────────────────┘
```

### 2.2 Ngữ Cảnh: Khi Nào Gọi System 1, Khi Nào Gọi System 2

```
State (ticket, message, row, output của LLM)
        │
        ▼
   ┌─────────┐   "Cần quyết định nhỏ, có cấu trúc, nhanh?"
   │  ROUTER │──────────────────────────────── YES ──► JEV (System 1)
   └─────────┘                                        typed + calibrated
        │ NO
        ▼
   "Cần sinh văn bản, code, giải thích, làm việc mở?"
        │
        ▼
   LLM (System 2)  ── output ──► JEV verify (Noul/Choice) ──► emit / escalate
```

**Quy tắc phân công**: *Jev decide, LLM write* (chi tiết ở [06-jev-and-llm](../06-jev-and-llm/)).

---

## 3. Lịch Sử & Tên Gọi

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** TypeSafe AI là AI lab **stealth ~2 năm** (thành lập 2024, San Francisco), công bố lần đầu cùng Jev tháng 9/2026 với seed round **$40M do DCVC dẫn dắt**. Founder: **Diogo Almeida** (CEO, ex-OpenAI — RLHF, InstructGPT, ChatGPT, GPT-4), **Erik Gafni**, **Sasha Sheng**; team đến từ OpenAI, Google Brain, Meta/FAIR, Stripe, Airbnb, Plaid, Docker.
> **Ẩn dụ/so sánh:** Giống **startup "thủ công kim hoàn trong bóng tối"** suốt 2 năm rồi ra sản phẩm chín muồi một lần — không preview rầm rộ, mà launch với product + pricing + docs ngay.
> **Vì sao quan trọng:** Bối cảnh giải thích tại sao Jev **không publish weights/paper**: chiến lược product-first, API-first — khác với norm open-weight của research lab. Cũng giải thích vì sao integration được đầu tư kỹ (SDK, LangChain, Pydantic, OpenRouter) ngay ngày đầu.

### 3.1 Dòng Thời Gian

```
2024          ── TypeSafe AI thành lập (SF), stealth mode
                founders: Diogo Almeida (CEO, ex-OpenAI), Erik Gafni, Sasha Sheng
   │
   ▼
~2 năm stealth ── team từ OpenAI, Google Brain, Meta/FAIR,
                Stripe, Airbnb, Plaid, Docker xây dựng Jev + RLCD
   │
   ▼
Launch 2026    ── Seed $40M do DCVC dẫn dắt
                Early access: 15/09/2026 (invite)
                Public, no waitlist: 20/09/2026
                Jev — first "System One Model"
```

### 3.2 Tại Sao Gọi Là "Jev"?

Tên lấy theo **William Stanley Jevons** (kinh tế gia thế kỷ 19) và **Jevons paradox**:

```
Jevons paradox (1865):
  Cải thiện hiệu suất than ──► GIẢM giá mỗi đơn vị
                            ──► nhưng TĂNG tổng tiêu thụ than

TypeSafe extrapolate (2026):
  Machine intelligence rẻ hơn + nhanh hơn ──► mỗi quyết định rẻ hơn
                                            ──► nhưng deploy RỘNG HƠN rất nhiều
  → "cheaper machine intelligence → far wider deployment"
```

Ý tưởng: khi quyết định có kiểu **gần như miễn phí và 70-500ms**, người ta đặt nó vào **mọi nơi** — từng row trong database, từng message, từng tool call — thay vì chỉ vài điểm昂贵 trong pipeline.

---

## 4. Kiến Trúc Tổng Quan

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Kiến trúc Jev: **state + questions** đi vào model **transformer-based** được train **độc quyền trên synthetic data** bằng **RLCD** — tất cả questions được evaluate **song song trong một pass** — trả về answers có kiểu kèm phân phối xác suất. **Không publish weights, không publish paper.**
> **Ẩn dụ/so sánh:** Giống **một phòng thí nghiệm với N shooter cùng bắn một lần** (parallel pass) thay vì một xạ thủ bắn tuần tự từng viên (autoregressive). Hoặc như **bài thi trắc nghiệm nhiều câu**: một lần lướt state, chấm **tất cả câu cùng lúc**.
> **Vì sao quan trọng:** Parallel pass giải thích trực tiếp vì sao **thêm question gần như không đổi latency** — chỉ thêm chi phí token input. Đây là lever quan trọng nhất khi thiết kế request (xem [02-primitives](../02-primitives/) §5).

### 4.1 Sơ Đồ Kiến Trúc

```
┌──────────────────────────────────────────────────────────────────┐
│                        JEV ARCHITECTURE                          │
│                                                                  │
│  state                          questions                        │
│  (string / JSON / array)        (named map of typed questions)   │
│         │                              │                          │
│         └──────────────┬───────────────┘                          │
│                        ▼                                          │
│         ┌──────────────────────────────────┐                      │
│         │  Transformer (closed answer      │                      │
│         │  space — không sinh text)        │                      │
│         │                                  │                      │
│         │  Training:                       │                      │
│         │  • Synthetic data exclusively    │                      │
│         │  • RLCD: probabilities           │                      │
│         │    optimized vs OUTCOMES         │                      │
│         │    (khác RLHF = vs preference)   │                      │
│         └──────────────┬───────────────────┘                      │
│                        ▼                                          │
│         ┌──────────────────────────────────┐                      │
│         │  ONE PASS — tất cả questions     │                      │
│         │  evaluated song song             │                      │
│         │  thêm question ≈ không đổi       │                      │
│         │  latency (chỉ thêm input tokens) │                      │
│         └──────────────┬───────────────────┘                      │
│                        ▼                                          │
│         answers: { name → {choice|score|noul, probs, confidence}} │
└──────────────────────────────────────────────────────────────────┘

Hạn chế kiến trúc (jev-1.13):
  ✗ text input only — không generate text, không viết tool args, không đọc file
  ✗ arithmetic / counting / date comparison → giữ trong code
  ✗ context: 64k tokens tổng (32k state + câu hỏi dài nhất) → ModelHTTPError
      (max_tokens_exceeded)
```

### 4.2 RLCD — Khác Gì RLHF?

```
RLHF (LLM):    output ──► human preference ("hay hơn")
               → calibrated? KHÔNG BAO GIỜ đảm bảo

RLCD (Jev):     output + question ──► OUTCOME thực tế ("đúng/sai")
               → probabilities MATCH outcomes
               → ~80% câu trả lời điểm 0.8 là đúng
```

RLCD là lý do **confidence của Jev dùng được làm ngưỡng trong code** — thứ mà self-reported confidence của LLM không làm được (xem [04-calibration](../04-calibration/)).

---

## 5. Vì Sao Bỏ Generate Text?

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** *"Giving up strings gives superpowers"* — từ bỏ text tự do (strings) là **trade-off có chủ đích** để đổi lấy: **type safety** (không hallucinate ngoài schema), **parallelism** (nhiều question một pass), **calibration** (xác suất match outcome), và **không cần parse**.
> **Ẩn dụ/so sánh:** Giống **đổ khuôn (mold)** thay vì **đắp đất sét**: đất sét (text) tạo được mọi hình dạng nhưng mỗi lần lệch form, mẻ góc; khuôn (closed schema) chỉ đúc được các hình đã định — nhưng **mỗi lần ra đúng form, không bao giờ vỡ**.
> **Vì sao quan trọng:** Đây là quyết định thiết kế triệt để nhất của Jev. LLM flexibility chính là nguồn hallucination + parse fragility + latency. Bỏ flexibility, bạn có hệ thống **deterministic về hình dạng, probabilistic về nội dung**.

### 5.1 Cái Gì Mất Đi vs Cái Gì Được

```
          LLM (strings)                    JEV (no strings)
   ─────────────────────────        ─────────────────────────────
   ✦ Mọi output đều "được"         ✦ Không thể sai TYPE
   ✦ Giải thích, narrative          ✦ Không hallucinate ngoài schema
   ✦ General-purpose                ✦ Parallel questions / 1 pass
                                     ✦ Calibrated probabilities
   ✗ Có thể hallucinate             ✦ Không cần regex-parse JSON
   ✗ Parse JSON hay fail            ✗ Không sinh text / tool args
   ✗ Tuần tự, slow (3-329s)         ✗ Output space đóng (bạn phải
   ✗ Overconfidence không calibrated   ĐỊNH NGHĨA choices từ trước
```

### 5.2 "Superpowers" Cụ Thể

```
1. TYPE-SAFE       ──► answer luôn thuộc schema bạn định nghĩa
                     (không JSON hỏng, không hallucinated keys)
2. PARALLEL        ──► N questions, 1 pass, thêm question ≈ không thêm latency
3. CALIBRATED      ──► confidence dùng trực tiếp làm THRESHOLD trong code
4. NO PARSING      ──► typed object trả về, dùng ngay — không extractor
```

---

## 6. Khi Nào Dùng / Không Dùng

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Jev **không thay thế LLM** — nó bổ sung lớp **System One** bên dưới lớp **System Two**. Dùng Jev khi output là **quyết định có cấu trúc**; dùng LLM khi output là **văn bản, code, hay reasoning mở**. Dùng cả hai khi pipeline cần **decide → write → verify**.
> **Ẩn dụ/so sánh:** **Jev là phản xạ**, **LLM là lý trí**. Phản xạ không viết được bức thư, lý trí không rụt tay kịp khi chạm lò — bạn cần cả hai.
> **Vì sao quan trọng:** Gọi nhầm lớp = tốn tiền + chậm (LLM cho việc của System 1) hoặc **không an toàn / không calibrated** (Jev cho việc cần sinh text). Bảng dưới là "phễu chọn model" bạn nên dán cạnh bàn làm việc.

### 6.1 Bảng Quyết Định Lớn

```
┌──────────────────────────────┬───────────────┬──────────────┐
│  Bạn cần...                  │  Dùng         │  Vì sao      │
├──────────────────────────────┼───────────────┼──────────────┤
│ Phân loại / route / gate     │  JEV          │  70-500ms,   │
│ (Choice / Score / Noul)      │  (System 1)   │  calibrated  │
├──────────────────────────────┼───────────────┼──────────────┤
│ Chấm điểm / ranking ordinal │  JEV Score    │  prob-weight │
│                              │               │  + per-level │
├──────────────────────────────┼───────────────┼──────────────┤
│ Yes/no verification gate     │  JEV Noul     │  P(yes) 0-1  │
│                              │               │  dùng làm    │
│                              │               │  threshold   │
├──────────────────────────────┼───────────────┼──────────────┤
│ Sinh text / code / email     │  LLM          │  Jev không   │
│                              │  (System 2)   │  generate    │
├──────────────────────────────┼───────────────┼──────────────┤
│ Reasoning mở, brainstorm,    │  LLM          │  open-ended  │
│ giải thích dài               │               │              │
├──────────────────────────────┼───────────────┼──────────────┤
│ Viết rồi KIỂM TRA            │  LLM + JEV    │  decide-write│
│                              │               │  -verify     │
├──────────────────────────────┼───────────────┼──────────────┤
│ Toán, đếm, so sánh ngày      │  CODE thuần   │  cả 2 đều    │
│                              │               │  không đáng tin│
└──────────────────────────────┴───────────────┴──────────────┘
```

### 6.2 "Đọc Sao Cho Dễ"

- **Câu trả lời là một trong vài giá trị bạn đã biết trước** → Jev. (Bạn không thể biết trước mọi câu trả lời có thể xảy ra với text tự do — đó là việc của LLM.)
- **Bạn sẽ đọc output bằng mắt** → LLM.
- **Code sẽ đọc output bằng `if/switch`** → Jev.
- **Bạn cần "tại sao" (explanation)** → LLM (hoặc escalate con người); Jev trả *decision + odds*, không trả rationale.
- **Latency budget < 1s** → Jev gần như luôn.

---

## 7. Vai Trò Trong Hệ Sinh Thái Agent

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Trong một agent system, tồn tại một **continuum phán đoán**: **deterministic code** (rule cứng, 100% deterministic) → **Jev** (narrow semantic judgment, calibrated) → **LLM** (language & broad reasoning, không calibrated). Jev lấp khoảng trống giữa *"rule đủ"* và *"cần LLM"* — lớp **quyết định ngữ nghĩa hẹp**.
> **Ẩn dụ/so sánh:** Giống **lớp quyết định trong một toà nhà**: bảo vệ cửa (code: allowlist), **thám tử kiểm tra thẻ ra vào** (Jev: "người này có nên vào không? — calibrated"), và **chuyên gia tư vấn** (LLM: phân tích tình huống phức tạp). Không ai trong ba người làm thay việc của người kia.
> **Vì sao quan trọng:** Đa số agent ngày nay **nhảy cóc** từ code cứng sang LLM — mọi thứ đều qua LLM, chậm và đắt. Jev là lớp missing middle: **semantic nhưng typed, probabilistic nhưng calibrated, nhanh và rẻ** — biến "System One-shaped task" khỏi danh sách việc của LLM.

### 7.1 Continuum Phán Đoán

```
DETERMINISTIC CODE          JEV (System 1)           LLM (System 2)
─────────────────           ──────────────           ──────────────
if status == "open"         "ticket này thuộc      "Viết migration
regex / SQL rules           team nào? tự tin bao    script cho thay
threshold cố định           nhiêu?" — 70-500ms,     đổi schema users
                            calibrated              kèm giải thích"
        │                          │                        │
        ▼                          ▼                        ▼
  100% deterministic        narrow semantic         broad reasoning
  không hiểu ngữ nghĩa      judgment, typed,        open-ended text
                            calibrated odds
```

### 7.2 Jev Trong Pipeline Agent Kiểu

```
        ┌──────────────────────────────────────────────────────┐
        │                    HARNESS (Modules VII-XI)          │
        │  tools · context · permissions · memory              │
        │                                                      │
        │   event / row / message                              │
        │        │                                             │
        │        ▼                                             │
        │   [CODE] sanitize, extract, arithmetic               │
        │        │                                             │
        │        ▼                                             │
        │   [JEV]  state + questions ──► typed decisions       │
        │        │                                             │
        │        ├─ high  ──► code acts / auto-route           │
        │        ├─ medium ──► ask confirm / more context      │
        │        └─ low   ──► escalate human                   │
        │        │                                             │
        │        ▼ (khi cần sinh text)                         │
        │   [LLM]  viết code / email / response               │
        │        │                                             │
        │        ▼                                             │
        │   [JEV]  verify output LLM (Noul/Choice gates)       │
        │        │                                             │
        │        ▼                                             │
        │   [LOOP] (Module XII) điều phối lại nếu fail        │
        │   [GRAPH](Module XIII) lưu tri thức đã kiểm chứng   │
        └──────────────────────────────────────────────────────┘
```

**Tóm lại vai trò**: Jev là **nơi agent ra quyết định** — điểm mà từ *"dữ liệu thô"* chuyển thành *"hành động có kiểu, có ngưỡng, có calibrated odds"* — trước khi LLM viết, trước khi code chạy, và trước khi loop lặp lại.

---

## 8. Tổng Kết — Một Đoạn

Jev không cạnh tranh LLM; nó **gỡ bớt việc cho LLM**. Bằng cách đóng answer space và tối ưu xác suất với RLCD, Jev biến các quyết định nhỏ — classify, gate, score, route — thành **function calls có kiểu** trong 70-500ms, với odds dùng được làm ngưỡng. Một agent thiết kế đúng sẽ gọi Jev **hàng nghìn lần mỗi giờ** cho System 1, và chỉ gọi LLM **khi thực sự cần viết** — rồi lại gọi Jev để verify.

```
Choose the model by the SHAPE of the answer:
  open-ended text  → LLM
  typed decision   → JEV
```

---

*Tiếp theo: [02 — Ba Primitives](../02-primitives/)*

*Trở về [README](../README.md) — tổng quan Module XIV*
