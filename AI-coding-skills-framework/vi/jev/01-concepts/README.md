# 🔬 01. Khái Niệm — Jev & System One Models

> Phần này giải thích **Jev là gì**, vì sao nó **không phải LLM**, sự khác biệt giữa **System One và System Two** theo Kahneman, **lịch sử & tên gọi**, **kiến trúc tổng quan**, lý do **bỏ generate text**, khi nào **dùng / không dùng**, và **vai trò trong hệ sinh thái agent**. Đọc [README.md](../README.md) trước để có bối cảnh tổng quan Module XIV.

---

## 1. Jev Là Gì?

Phần này trả lời câu hỏi nền tảng nhất: Jev thực chất là gì, và vì sao nó không phải một mô hình chat.

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Jev là **non-generative decision model** — mô hình **không sinh text** do TypeSafe AI phát hành; nhận **unstructured state** (string / JSON / array of text) và trả về **typed probabilistic decisions** kèm phân phối xác suất — được TypeSafe gọi là *"frontier-intelligence function call"*.
> **Ẩn dụ/so sánh:** Giống **một function call có kiểu trả về** thay vì một chatbot: `decide(state, questions) → answers`. Hay như **đèn giao thông** — bạn không nhờ đèn giao thông "kể chuyện về lý do nên đi"; nó chỉ trả về **đỏ / xanh** kèm xác suất, và phần mềm dùng ngay được.
> **Vì sao quan trọng:** Hầu hết bước trong workflow agent chỉ cần *"quyết định này là gì, tự tin bao nhiêu"* — không cần văn xuôi. Jev trả lời đúng nhu cầu đó với latency 70-500ms và giá $0.042/M input tokens, output free.

> **Tóm gọn 1 câu:** Jev là mô hình ra quyết định chứ không phải chatbot: dữ liệu thô đi vào, quyết định có kiểu kèm xác suất đi ra.

Dịch nôm các từ khó: **non-generative** = không sinh ra chữ mới, chỉ chọn từ các lựa chọn có sẵn; **unstructured state** = dữ liệu thô chưa định dạng (đoạn văn, JSON, mảng dòng chữ); **typed decisions** = kết quả luôn đúng kiểu dữ liệu bạn khai trước (kiểu `Choice`, `Score`, v.v.); **phân phối xác suất** = mức tin cậy của từng lựa chọn, tổng bằng 100%.

### 1.1 Định Nghĩa Một Dòng

```
┌──────────────────────────────────────────────────────────────────┐
│  JEV = "frontier-intelligence function call"                     │
│                                                                  │
│  Unstructured state in  ──►  Typed probabilistic decisions out   │
│  (string / JSON / array)      (Choice / Score / Noul + probs)    │
└──────────────────────────────────────────────────────────────────┘
```

> **Tóm gọn 1 câu (1.1):** Một dòng đủ hiểu: Jev nhận dữ liệu thô đi vào, trả quyết định có kiểu + xác suất đi ra — như một hàm có kiểu trả về chứ không phải một chatbot.

**Jev KHÔNG phải LLM:**

Cách đọc bảng này: cột **Tính chất** là điểm so sánh; cột **LLM** là mô hình ngôn ngữ lớn làm thế nào; cột **Jev** làm thế nào. Ví dụ, dòng "Sinh text": LLM có, Jev không.

| Tính chất | LLM | Jev |
|-----------|-----|-----|
| Sinh text / token | ✅ Có | ❌ Không |
| Output | Văn xuôi / code | Typed decisions + xác suất |
| Dùng cho | Con người đọc | **Phần mềm consume trực tiếp** |
| Cần parse JSON | Thường (regex / tool-use) | Không — output đã có kiểu |
| Latency | 3-329s | 70-500ms |

> **Tóm gọn 1 câu:** Jev là "function call thông minh": nhận dữ liệu thô, trả về quyết định đúng kiểu kèm xác suất, dùng trực tiếp trong code — không sinh chữ, không cần dò JSON, nhanh gấp nghìn lần LLM.

### 1.2 Phiên Bản Hiện Tại

```
Early access (invite):  15/09/2026
Public (no waitlist):   20/09/2026
Version hiện tại:       jev-1.13.0   (alias: jev-latest)
API:                    POST https://api.typesafe.ai/v1/systemone
```

> **Tóm gọn 1 câu (1.2):** Jev chỉ dùng được qua API của TypeSafe (mô hình `jev-1.13.0`); "alias: jev-latest" = tên thay thế luôn trỏ tới bản mới nhất.

---

## 2. System One vs System Two (Kahneman)

Phần này giải thích cái tên "System One" — vì nó quyết định khi nào bạn nên chọn Jev, khi nào chọn LLM.

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Jev đặt tên theo **dual-process theory** trong *Thinking, Fast and Slow* của Daniel Kahneman — **System 1** = suy nghĩ nhanh, trực giác, tự động, nhiều lần mỗi ngày; **System 2** = suy nghĩ chậm, thận trọng, có lý do, tốn sức. LLM frontier vận hành như **System 2** (viết lập luận từng bước); Jev được thiết kế cho **System 1** — quyết định nhanh, có cấu trúc, không cần lời giải thích.
> **Ẩn dụ/so sánh:** Khi bạn chạm vào lò nóng, **System 1** rụt tay lại **trước khi System 2 kịp nói "nóng"**. Jev là cú rụt tay đó của agent: gate, route, classify trong 70-500ms. LLM là phần bạn **ngồi giải thích sau đó**.
> **Vì sao quan trọng:** Sai lầm thiết kế phổ biến là gọi System 2 cho việc của System 1 — vừa chậm vừa đắt. Phân chia đúng hai lớp cho agent latency thấp, chi phí thấp, và **calibrated** (xác suất match outcome).

> **Tóm gọn 1 câu (§2):** Tên "System One/Two" mượn từ Kahneman: LLM là suy nghĩ chậm có lý lẽ, Jev là phản xạ nhanh — phân đúng lớp để vừa nhanh vừa rẻ.

### 2.1 Bảng So Sánh LLM vs Jev

Bảng dưới là bản ASCII (vẽ bằng ký tự) trong khung code — đọc như một bảng thường: cột trái là điểm so sánh, cột giữa là LLM, cột phải là Jev.

Từ khó cần dịch: **RLHF** = huấn luyện theo sở thích con người; **RLCD** = huấn luyện theo kết quả thật; **autoregressive** = sinh chữ từng token một, tuần tự; **calibrated** = "xác suất nói ra khớp tỉ lệ đúng thật" — nói 80% thì đúng 80% số lần.

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

> **Tóm gọn 1 câu (2.1):** LLM sinh text tuần tự, chậm (3–329s), xác suất "tự tin" không đáng tin; Jev chấm song song, nhanh (70–500ms), xác suất khớp thực tế.

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

Sơ đồ trên đọc từ trên xuống: dữ liệu vào → một "bộ định tuyến" hỏi "cần quyết định nhỏ nhanh không?" → đúng thì gọi Jev, không thì gọi LLM; và khi LLM viết xong, Jev đứng chốt kiểm tra lại.

**Quy tắc phân công**: *Jev decide, LLM write* (chi tiết ở [06-jev-and-llm](../06-jev-and-llm/)) — Jev quyết, LLM viết.

> **Tóm gọn 1 câu:** Chia việc theo hình dạng đáp án: quyết định nhỏ có cấu trúc cho Jev (System 1), sinh văn bản và lập luận mở cho LLM (System 2) — gọi nhầm lớp vừa chậm vừa đắt.

---

## 3. Lịch Sử & Tên Gọi

Phần này kể công ty đứng sau Jev và ý nghĩa cái tên — hữu ích khi bạn cần đánh giá mức tin cậy và rủi ro phụ thuộc.

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** TypeSafe AI là AI lab **stealth ~2 năm** (thành lập 2024, San Francisco), công bố lần đầu cùng Jev tháng 9/2026 với seed round **$40M do DCVC dẫn dắt**. Founder: **Diogo Almeida** (CEO, ex-OpenAI — RLHF, InstructGPT, ChatGPT, GPT-4), **Erik Gafni**, **Sasha Sheng**; team đến từ OpenAI, Google Brain, Meta/FAIR, Stripe, Airbnb, Plaid, Docker.
> **Ẩn dụ/so sánh:** Giống **startup "thủ công kim hoàn trong bóng tối"** suốt 2 năm rồi ra sản phẩm chín muồi một lần — không preview rầm rộ, mà launch với product + pricing + docs ngay.
> **Vì sao quan trọng:** Bối cảnh giải thích tại sao Jev **không publish weights/paper**: chiến lược product-first, API-first — khác với norm open-weight của research lab. Cũng giải thích vì sao integration được đầu tư kỹ (SDK, LangChain, Pydantic, OpenRouter) ngay ngày đầu.

> **Tóm gọn 1 câu (§3):** TypeSafe AI là lab ẩn danh ~2 năm, ra mắt Jev 9/2026 kèm vòng vốn $40M; chiến lược product-first giải thích vì sao không có weights hay paper công khai.

### 3.1 Dòng Thời Gian

Dòng thời gian vẽ bằng ASCII trong khung code dưới đây, đọc từ trên xuống: 2024 thành lập → ~2 năm im lặng → ra mắt tháng 9/2026 kèm vòng gọi vốn đầu tiên 40 triệu USD.

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

> **Tóm gọn 1 câu (3.1):** TypeSafe AI làm thầm lặng ~2 năm (2024–2026) rồi ra mắt Jev kèm vòng vốn hạt giống $40M — không preview, chỉ product + API hoàn chỉnh.

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

Ý tưởng: khi một quyết định có kiểu **gần như miễn phí mà chỉ mất 70-500ms**, người ta sẽ đặt nó vào **khắp mọi nơi** — từng dòng trong database, từng message, từng tool call — thay vì chỉ dùng ở vài điểm đắt đỏ trong pipeline.

> **Tóm gọn 1 câu (3.2):** Tên "Jev" nhắc tới nghịch lý Jevons: quyết định càng rẻ và càng nhanh, người ta càng đặt nó vào càng nhiều chỗ — nên tổng mức dùng lại tăng vọt.

---

## 4. Kiến Trúc Tổng Quan

Phần này mô tả bên trong Jev vận hành thế nào — bạn cần nắm vì nó giải thích mọi con số hiệu năng ở các phần sau.

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Kiến trúc Jev: **state + questions** đi vào model **transformer-based** được train **độc quyền trên synthetic data** bằng **RLCD** — tất cả questions được evaluate **song song trong một pass** — trả về answers có kiểu kèm phân phối xác suất. **Không publish weights, không publish paper.**
> **Ẩn dụ/so sánh:** Giống **một phòng thí nghiệm với N shooter cùng bắn một lần** (parallel pass) thay vì một xạ thủ bắn tuần tự từng viên (autoregressive). Hoặc như **bài thi trắc nghiệm nhiều câu**: một lần lướt state, chấm **tất cả câu cùng lúc**.
> **Vì sao quan trọng:** Parallel pass giải thích trực tiếp vì sao **thêm question gần như không đổi latency** — chỉ thêm chi phí token input. Đây là lever quan trọng nhất khi thiết kế request (xem [02-primitives](../02-primitives/) §5).

> **Tóm gọn 1 câu (§4):** Jev = transformer huấn luyện bằng RLCD trên dữ liệu tổng hợp, chấm mọi câu hỏi song song trong một lượt — đây là nguồn của mọi con số hiệu năng.

### 4.1 Sơ Đồ Kiến Trúc

Sơ đồ ASCII dưới đây đọc từ trên xuống: `state` (dữ liệu) và `questions` (câu hỏi) đi vào một mô hình transformer (kiến trúc mạng như GPT), xử lý tất cả câu hỏi song song trong một lượt, rồi nhả answers có kiểu kèm xác suất.

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

> **Tóm gọn 1 câu (4.1):** Jev = transformer chạy một lượt duy nhất, chấm song song mọi câu hỏi trên dữ liệu huấn luyện tổng hợp (synthetic data = dữ liệu do máy tự tạo, không phải dữ liệu người thật); hạn chế: chỉ nhận text, không làm toán/đếm/ngày, trần 64k token.

### 4.2 RLCD — Khác Gì RLHF?

Phần này so sánh hai cách huấn luyện — đây là lý do xác suất của Jev dùng được làm ngưỡng còn của LLM thì không.

```
RLHF (LLM):    output ──► human preference ("hay hơn")
               → calibrated? KHÔNG BAO GIỜ đảm bảo

RLCD (Jev):     output + question ──► OUTCOME thực tế ("đúng/sai")
               → probabilities MATCH outcomes
               → ~80% câu trả lời điểm 0.8 là đúng
```

RLCD là lý do **confidence của Jev dùng được làm ngưỡng trong code** — thứ mà self-reported confidence của LLM không làm được (xem [04-calibration](../04-calibration/)).

> **Tóm gọn 1 câu (4.2):** RLHF học theo "câu này hay hơn" do người chấm; RLCD học theo đúng/sai đo được từ thực tế — nên xác suất của Jev trung thực và dùng làm ngưỡng code được.

---

## 5. Vì Sao Bỏ Generate Text?

Phần này giải thích quyết định thiết kế mạo hiểm nhất của Jev: cắt hoàn toàn khả năng viết chữ, và nhận lại được gì.

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** *"Giving up strings gives superpowers"* — từ bỏ text tự do (strings) là **trade-off có chủ đích** để đổi lấy: **type safety** (không hallucinate ngoài schema), **parallelism** (nhiều question một pass), **calibration** (xác suất match outcome), và **không cần parse**.
> **Ẩn dụ/so sánh:** Giống **đổ khuôn (mold)** thay vì **đắp đất sét**: đất sét (text) tạo được mọi hình dạng nhưng mỗi lần lệch form, mẻ góc; khuôn (closed schema) chỉ đúc được các hình đã định — nhưng **mỗi lần ra đúng form, không bao giờ vỡ**.
> **Vì sao quan trọng:** Đây là quyết định thiết kế triệt để nhất của Jev. LLM flexibility chính là nguồn hallucination + parse fragility + latency. Bỏ flexibility, bạn có hệ thống **deterministic về hình dạng, probabilistic về nội dung**.

> **Tóm gọn 1 câu (§5):** Bỏ sinh text là đánh đổi có chủ đích: flexibility của LLM chính là nguồn hallucination, JSON hỏng và chậm — Jev đổi nó lấy hình dạng đầu ra cố định.

### 5.1 Cái Gì Mất Đi vs Cái Gì Được

Hai cột ASCII dưới đây đối chiếu: cột trái là LLM (sinh text tự do), cột phải là Jev. Dấu ✦/✅ = điểm mạnh, ✗ = điểm yếu.

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

> **Tóm gọn 1 câu (5.1):** Đổi tính linh hoạt lấy độ chắc — Jev mất khả năng viết tự do, đổi lại không sai kiểu, không bịa ngoài danh sách, chạy song song, xác suất đáng tin, không cần dò JSON.

### 5.2 "Superpowers" Cụ Thể

```
1. TYPE-SAFE       ──► answer luôn thuộc schema bạn định nghĩa
                     (không JSON hỏng, không hallucinated keys)
2. PARALLEL        ──► N questions, 1 pass, thêm question ≈ không thêm latency
3. CALIBRATED      ──► confidence dùng trực tiếp làm THRESHOLD trong code
4. NO PARSING      ──► typed object trả về, dùng ngay — không extractor
```

> **Tóm gọn 1 câu (5.2):** Bốn "siêu năng lực" đổi lại: đúng kiểu schema, chấm song song, xác suất dùng làm ngưỡng, và trả về object dùng ngay không cần bộ trích xuất (extractor = đoạn code dò/kéo dữ liệu khỏi văn bản).

---

## 6. Khi Nào Dùng / Không Dùng

Phần này là "phễu chọn model": nhìn vào loại việc của bạn và chọn Jev, LLM, hay code thuần.

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Jev **không thay thế LLM** — nó bổ sung lớp **System One** bên dưới lớp **System Two**. Dùng Jev khi output là **quyết định có cấu trúc**; dùng LLM khi output là **văn bản, code, hay reasoning mở**. Dùng cả hai khi pipeline cần **decide → write → verify**.
> **Ẩn dụ/so sánh:** **Jev là phản xạ**, **LLM là lý trí**. Phản xạ không viết được bức thư, lý trí không rụt tay kịp khi chạm lò — bạn cần cả hai.
> **Vì sao quan trọng:** Gọi nhầm lớp = tốn tiền + chậm (LLM cho việc của System 1) hoặc **không an toàn / không calibrated** (Jev cho việc cần sinh text). Bảng dưới là "phễu chọn model" bạn nên dán cạnh bàn làm việc.

> **Tóm gọn 1 câu (§6):** Jev không thay LLM mà bổ sung lớp phản xạ bên dưới lớp lý trí — chọn sai lớp là tốn tiền + chậm hoặc không an toàn.

### 6.1 Bảng Quyết Định Lớn

Bảng ASCII dưới đây: cột **Bạn cần...** là loại việc; cột **Dùng** là công cụ nên chọn (JEV / LLM / CODE thuần); cột **Vì sao** là lý do ngắn.

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

> **Tóm gọn 1 câu (6.1):** Quyết định có cấu trúc → Jev; sinh text và lập luận mở → LLM; toán, đếm, so sánh ngày → code thuần (cả hai mô hình đều không đáng tin cho việc này).

### 6.2 "Đọc Sao Cho Dễ"

- **Câu trả lời là một trong vài giá trị bạn đã biết trước** → Jev. (Bạn không thể biết trước mọi câu trả lời có thể xảy ra với text tự do — đó là việc của LLM.)
- **Bạn sẽ đọc output bằng mắt** → LLM.
- **Code sẽ đọc output bằng `if/switch`** → Jev.
- **Bạn cần "tại sao" (explanation)** → LLM (hoặc escalate con người); Jev trả *decision + odds*, không trả rationale.
- **Latency budget < 1s** → Jev gần như luôn.

> **Tóm gọn 1 câu (6.2):** Mẹo nhanh: đáp án nằm trong danh sách đã biết trước → Jev; đọc bằng mắt người → LLM; đọc bằng `if/switch` trong code → Jev; cần "tại sao" → LLM.

---

## 7. Vai Trò Trong Hệ Sinh Thái Agent

Phần này đặt Jev vào bức tranh lớn của một agent: nó đứng ở đâu giữa code cứng và LLM.

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Trong một agent system, tồn tại một **continuum phán đoán**: **deterministic code** (rule cứng, 100% deterministic) → **Jev** (narrow semantic judgment, calibrated) → **LLM** (language & broad reasoning, không calibrated). Jev lấp khoảng trống giữa *"rule đủ"* và *"cần LLM"* — lớp **quyết định ngữ nghĩa hẹp**.
> **Ẩn dụ/so sánh:** Giống **lớp quyết định trong một toà nhà**: bảo vệ cửa (code: allowlist), **thám tử kiểm tra thẻ ra vào** (Jev: "người này có nên vào không? — calibrated"), và **chuyên gia tư vấn** (LLM: phân tích tình huống phức tạp). Không ai trong ba người làm thay việc của người kia.
> **Vì sao quan trọng:** Đa số agent ngày nay **nhảy cóc** từ code cứng sang LLM — mọi thứ đều qua LLM, chậm và đắt. Jev là lớp missing middle: **semantic nhưng typed, probabilistic nhưng calibrated, nhanh và rẻ** — biến "System One-shaped task" khỏi danh sách việc của LLM.

> **Tóm gọn 1 câu (§7):** Jev lấp khoảng trống giữa code cứng và LLM — lớp "missing middle" mà đa số agent đang nhảy cóc qua, khiến mọi thứ đều chậm và đắt.

### 7.1 Continuum Phán Đoán

Sơ đồ ASCII dưới đây so ba tầng từ trái sang phải: code cứng (100% chắc chắn nhưng không hiểu ngữ nghĩa), Jev (hiểu ngữ nghĩa hẹp + có xác suất đáng tin), LLM (hiểu rộng, sinh chữ, chậm).

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

> **Tóm gọn 1 câu (7.1):** Ba tầng phán đoán: code cứng cho luật chắc chắn 100%, Jev cho quyết định ngữ nghĩa hẹp cần xác suất đáng tin, LLM cho lập luận rộng — mỗi yêu cầu nên rơi đúng một tầng.

### 7.2 Jev Trong Pipeline Agent Kiểu

Sơ đồ dưới đây đặt Jev vào một pipeline agent hoàn chỉnh: dữ liệu → code xử lý sơ bộ → Jev quyết → hành động tùy mức tin cậy → LLM viết khi cần → Jev kiểm tra lại kết quả LLM.

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

> **Tóm gọn 1 câu (7.2):** Trong pipeline agent, Jev đứng tại điểm ra quyết định: tin cao thì code tự hành động, tin thấp thì hỏi xác nhận hoặc chuyển người — và LLM chỉ xuất hiện khi cần viết.

---

## 8. Tổng Kết — Một Đoạn

Phần này gói lại toàn bộ file thành một đoạn duy nhất.

Jev không cạnh tranh LLM; nó **gỡ bớt việc cho LLM**. Bằng cách đóng answer space và tối ưu xác suất với RLCD, Jev biến các quyết định nhỏ — classify, gate, score, route — thành **function calls có kiểu** trong 70-500ms, với odds dùng được làm ngưỡng. Một agent thiết kế đúng sẽ gọi Jev **hàng nghìn lần mỗi giờ** cho System 1, và chỉ gọi LLM **khi thực sự cần viết** — rồi lại gọi Jev để verify.

```
Choose the model by the SHAPE of the answer:
  open-ended text  → LLM
  typed decision   → JEV
```

> **Tóm gọn 1 câu (§8):** Jev không thay LLM mà gỡ bớt việc cho LLM: chọn model theo hình dạng đáp án — văn bản mở → LLM, quyết định có kiểu → Jev.

---

*Tiếp theo: [02 — Ba Primitives](../02-primitives/)*

*Trở về [README](../README.md) — tổng quan Module XIV*
