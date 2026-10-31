# 🤝 06. Jev + LLM — Phân Chia Lao Động

> Phần này giải thích cách **kết hợp Jev với LLM** trong cùng một hệ thống: hai-brain model, model routing, tool-call gateway, fallback model (Pydantic AI), và vị trí của Jev trong **harness**, **loop**, và **graph** — cùng các anti-pattern cần tránh. Đọc [README.md](../README.md) trước để có bối cảnh tổng quan Module XIV.

> **Cách đọc phần này:** *two-brain model* = mô hình "hai bộ não" — một não quyết nhanh (Jev), một não viết (LLM); *routing* = chọn model nào chạy; *gateway* = cổng kiểm tra trước khi công cụ chạy; *fallback model* = model dự phòng nhận việc khi Jev không làm được; *anti-pattern* = lỗi thiết kế lặp đi lặp lại hay gặp.

---

## 1. Two-Brain Model — Jev Decides, LLM Writes

Phần này đặt nền cho cả chương: chia việc giữa Jev và LLM theo loại công việc, không theo sở thích.

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** *"Jev decides, LLM writes"* — Jev xử lý **quyết định** (chọn option, chấm điểm yes/no trong schema biết trước), LLM xử lý **ngôn ngữ** (sinh text, giải thích, viết code, soạn email). Chiến lược mở rộng: *"Jev routes and verifies, LLM provides the language."*
> **Ẩn dụ/so sánh:** Giống **bộ não hai nửa**: System One (Jev — nhanh, trực giác, chọn hướng) và System Two ngôn ngữ (LLM — chậm hơn, viết ra lời). Theo Kahneman, Jev là *System One Model* đầu tiên: fast & intuitive; LLM đảm nhận phần slow & deliberate khi cần text.
> **Vì sao quan trọng:** Jev vừa rẻ ($0.042/1M input, output miễn phí) vừa nhanh (70–500ms) — **hỏi Jev thường xuyên** gần như không tốn gì. LLM đắt và chậm hơn — **chỉ gọi LLM khi thật sự cần sinh text**. Chia việc đúng giúp tiết kiệm chi phí gấp nhiều lần và giảm độ trễ ở hầu hết các bước trung gian.

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

Cách đọc khối trên: cột trái — Jev nhận các việc quyết định (định tuyến, phân loại, chấm điểm, cổng có/không, verify, xếp hạng) và **không sinh text, không token output**; cột phải — LLM nhận các việc ngôn ngữ (sinh text, giải thích, viết code, tóm tắt, viết tham số tool) và **không quyết định thay Jev**; dưới cùng — code thực thi kết hợp cả hai (business rules = luật nghiệp vụ của bạn).

Cách đọc bảng dưới: cột **Việc cần làm** là công việc cụ thể; cột **Ai làm?** chỉ định model nhận việc, kèm primitive trong ngoặc; cột **Vì sao** giải thích lý do phân công. Ví dụ, hàng đầu tiên nghĩa là: chọn queue/label là việc của Jev vì danh sách lựa chọn biết trước, chạy 70–500ms, gần như miễn phí.

| Việc cần làm | Ai làm? | Vì sao |
|--------------|---------|--------|
| Chọn queue/label/option | **Jev** (Choice) | Schema biết trước, 70–500ms, gần free |
| Yes/no authorize / verify | **Jev** (Noul) | Margin \|p−0.5\|×2, calibrated |
| Chấm điểm mức độ | **Jev** (Score) | Weighted score + distribution |
| Sinh câu trả lời cho khách | **LLM** | Cần text |
| Giải thích "tại sao" | **LLM** (từ kết quả Jev) | Jev không giải thích |
| Viết argument phức tạp cho tool | **LLM** | Jev không sinh tool args |
| Routing model selection | **Jev** → chọn LLM nào | Jev gate trước, LLM chạy sau |

> **Tóm gọn 1 câu:** Jev nhận mọi việc quyết định trong schema, LLM nhận mọi việc cần văn bản — hỏi Jev bao nhiêu cũng được, gọi LLM phải có lý do.

### 1.2 Nguyên Tắc Chi Phí / Latency

Phần này quy các nguyên tắc trên thành hai dòng so sánh chi phí và thời gian.

```
   Hỏi Jev:     $0.042/1M input · free output · 70-500ms
                 → HỎI MỌI LÚC được — thêm questions gần như free latency

   Gọi LLM:     đắt hơn nhiều · chậm hơn · sinh token
                 → GỌI KHI CẦN TEXT — mỗi lần gọi là tiền + thời gian

   Kết quả:     Jev ở mọi bước trung gian, LLM chỉ ở terminal "viết"
                 → ~2 orders of magnitude efficient hơn nếu chỉ dùng LLM
```

Cách đọc khối trên: ba khối — hỏi Jev quá rẻ và nhanh (thêm câu hỏi gần như miễn phí vì chạy song song); gọi LLM đắt và chậm (mỗi token là tiền); kết luận — đặt Jev ở mọi bước trung gian, LLM chỉ ở bước cuối "viết". **2 orders of magnitude** = gấp ~100 lần hiệu quả.

> **Tóm gọn 1 câu:** Jev rẻ và nhanh nên hỏi mọi lúc được; LLM đắt và chậm nên chỉ gọi khi cần văn bản — chênh lệch hiệu quả tới ~100 lần.

---

## 2. Model Routing — Jev Chọn LLM Nào

Phần này mô tả pattern "chọn model theo độ khó": Jev đánh giá yêu cầu trước, rồi quyết định model nào xử lý.

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Middleware dùng Jev **đánh giá request trước** (Choice về độ khó / loại task) rồi **chọn model**: request đơn giản → model rẻ/nhanh, request phức tạp → model mạnh. Jev **gắn từ đầu** pipeline; probabilities được **giữ trong agent state** để các bước sau đọc lại.
> **Ẩn dụ/so sánh:** Giống **lễ tân phân phòng khám** — bác sĩ thường khám trước (Jev, vài trăm ms), nếu bệnh nặng mới chuyển bác sĩ chuyên khoa (LLM mạnh). Không cần chuyên khoa khám cho mọi bệnh nhân.
> **Vì sao quan trọng:** Không routing → mọi request chạy trên model đắt nhất = lãng phí; routing bằng LLM khác thì chính routing cũng tốn tiền/giây. Jev routing gần free và đủ nhanh cho pre-dispatch.

Giải nghĩa: **middleware** = bước chen giữa người dùng và pipeline; **pre-dispatch** = bước phân loại trước khi điều phối; **agent state** = kho dữ liệu phiên làm việc của agent, các bước sau đọc lại được.

> **Tóm gọn 1 câu:** Jev đứng đầu pipeline chấm độ khó trong vài trăm ms: yêu cầu đơn giản → model rẻ, phức tạp → model mạnh, không chắc → model mạnh mặc định.

### 2.1 Kiến Trúc Routing Middleware

Phần này vẽ kiến trúc: một câu hỏi độ khó, ba đường rẽ tới ba loại model.

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

> 📄 **Code ví dụ:** [`examples/01-2-1-kien-truc-routing-middleware.py`](examples/01-2-1-kien-truc-routing-middleware.py)

</details>

### 2.2 Lưu Ý

Cách đọc bảng này: cột **Điểm** là khía cạnh (vị trí, state, band, tích hợp); cột **Guidance** là khuyến nghị. Ví dụ, hàng `State` nghĩa là: lưu xác suất, độ tự tin và request_id vào agent state để các bước sau kiểm tra lại (audit = kiểm tra vết) hoặc dùng tiếp (cascade = chuỗi xử lý).

| Điểm | Guidance |
|------|----------|
| Vị trí | Middleware **gắn đầu** — trước mọi LLM call |
| State | Giữ `probs`, `confidence`, `request_id` trong agent state để audit/cascade |
| Band LOW | Confidence thấp → chọn model mạnh mặc định, không routing "tiết kiệm" |
| Integration | Tương tự pattern **routing middleware** trong LangChain (TypeSafeClassifier) |

> **Tóm gọn 1 câu:** Bốn lưu ý của routing: middleware gắn đầu trước mọi LLM call, lưu probs+confidence+request_id vào state, band LOW dùng model mạnh, và tái dùng TypeSafeClassifier của LangChain.

---

## 3. Tool-Call Gateway — Jev Gate Trước Khi Tool Chạy

Phần này mô tả cổng kiểm tra đặt giữa ý định của agent và hành động thật.

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Jev gate **trước khi tool thực thi**: mỗi tool call đi qua một Noul check (authorize/safe theo context), call dưới threshold bị **block** và chuyển sang approval flow. Đây là tầng trung gian giữa *ý định của agent* và *side-effect thật*.
> **Ẩn dụ/so sánh:** Giống **chốt an ninh giữa hành lang văn phòng và phòng họp tài chính** — badge quẹt không hợp lệ thì cửa không mở, bất kể agent "nghĩ" mình được vào.
> **Vì sao quan trọng:** Kết nối trực tiếp với **Auth/approval**: mọi tool có side-effect (xoá, charge, gửi) đều phải qua gateway. Jev nhanh enough (70–500ms) để không cản luồng real-time, và calibrated đủ để threshold có nghĩa.

Giải nghĩa: **side-effect** = làm thay đổi thế giới thật (xoá, tính tiền, gửi); **threshold có nghĩa** = con số ngưỡng phản ánh đúng thực tế vì xác suất đã được hiệu chỉnh; **denylist** = danh sách cấm — các mục bị chặn sẵn.

> **Tóm gọn 1 câu:** Gateway = chốt an ninh: mỗi tool gây thay đổi phải qua một câu có/không của Jev, và quyền quyết cuối vẫn nằm ở lớp auth thật.

### 3.1 Gateway Pipeline

Phần này vẽ luồng ba nhánh của cổng: cho chạy, hỏi xác nhận, hoặc chặn hẳn.

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

**Điểm kết nối Auth/approval**: Jev là *signal phân loại*, còn **quyền allow/deny cuối cùng** nằm ở lớp auth thật (permissions, denylist, human gate). Jev **không thay thế auth** — nó bổ sung judgment nhanh trên context mà rule tĩnh không cover được. (Human gate = bước có người duyệt bắt buộc.)

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/02-3-1-gateway-pipeline.py`](examples/02-3-1-gateway-pipeline.py)

</details>

> **Tóm gọn 1 câu:** Ba nhánh của gateway: cho chạy / hỏi xác nhận / chặn sang luồng duyệt — và Jev bổ trợ lớp auth, không thay thế nó.

---

## 4. Fallback Model — LLM Đứng Sau Jev (Pydantic AI)

Phần này giải thích cơ chế dự phòng trong Pydantic AI: khi Jev kẹt, LLM đứng sau nhận xử lý cả bước.

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Trong **Pydantic AI**, `TypeSafeModel` đặt câu hỏi qua Jev; khi tool cần Jev không xử lý được, **`FallbackModel`** (một LLM) **nhận cả bước** thay Jev. Hai chế độ: tool **không args** → Jev pick tool và gọi; tool **có args** → `ToolCallProposed` raises `ModelAPIError` → FallbackModel (LLM) làm toàn bộ bước với tư cách model chính.
> **Ẩn dụ/so sánh:** Giống **quầy tiếp vấn**: Jev là nhân viên nhanh xử lý hồ sơ chuẩn (chọn form có sẵn); khi hồ sơ phức tạp cần viết tự do, nhân viên bấm chuông gọi **quản lý (LLM)** — quản lý tiếp quản toàn bộ ca việc đó, không phải chỉ phần lẻ.
> **Vì sao quan trọng:** Đây là pattern **"Jev routes, LLM fallback"** chính thức: threshold `typesafe_tool_call_threshold` mặc định **0.6** quyết định lúc nào Jev tự quyết vs lúc nào chuyển LLM. Biết hai nhánh (no-arg vs arg tool) để thiết kế tool signatures đúng.

Giải nghĩa: **tool signature** = cách khai báo tên và tham số của công cụ; **no-arg tool** = công cụ không cần tham số (ví dụ `get_time()`); **arg tool** = công cụ cần tham số (ví dụ `delete_file(path=...)`); **raises `ModelAPIError`** = ném ra lỗi kiểu "lỗi API model" — tín hiệu để chuyển model dự phòng.

> **Tóm gọn 1 câu:** Hai nhánh: tool không tham số thì Jev gọi thẳng khi tự tin ≥ 0.6; tool có tham số thì Jev kẹt — LLM dự phòng nhận toàn bộ bước.

### 4.1 Hai Nhánh Trong Pydantic AI

Phần này vẽ sơ đồ hai nhánh trong chi tiết.

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

Cách đọc khối trên: một bước có tool rẽ hai nhánh — tool **không** tham số: Jev chọn tool trên danh sách, tự tin ≥ 0.6 thì gọi thẳng, xong; tool **có** tham số: Jev không viết được tham số (không sinh text) → ném lỗi `ToolCallProposed`/`ModelAPIError` → `FallbackModel` (LLM) nhận **cả bước**, sinh tham số và gọi tool. Kết quả: Jev quyết phần schema, LLM trám phần text.

### 4.2 Ví Dụ Code

Phần này chứa code mẫu cài đặt `TypeSafeModel` + `FallbackModel`, kèm sơ đồ tóm tắt luồng.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/03-4-2-vi-du-code.py`](examples/03-4-2-vi-du-code.py)

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

Cách đọc sơ đồ trên: đầu vào vào `TypeSafeModel` (Jev) rồi rẽ ba: đáp án thuần (Choice/Score/Noul) → trả kết quả ngay (rẻ, nhanh); tool không tham số và tự tin ≥ 0.6 → Jev chọn và tool chạy; tool có tham số → lỗi → LLM dự phòng nhận cả bước.

</details>

> **Tóm gọn 1 câu:** Code mẫu và sơ đồ trên cho thấy đủ hai nhánh — Jev xử lý nhanh phần chuẩn, LLM dự phòng nhận cả bước phần có tham số.

### 4.3 Lưu Ý

Cách đọc bảng này: cột **Điểm** là khía cạnh (ngưỡng, hai loại tool, mẹo thiết kế); cột **Guidance** là khuyến nghị. Ví dụ, hàng `Higher threshold` nghĩa là: nâng ngưỡng thì Jev ít nhường việc hơn, nhưng mỗi lần nhường thì nhường đúng hơn.

| Điểm | Guidance |
|------|----------|
| Threshold | `typesafe_tool_call_threshold` mặc định **0.6** — starting point, không phải validated; tune từ labelled tickets/data |
| Higher threshold | Ít handoff hơn, nhưng **đúng hơn khi nó hand off** |
| No-arg tool | Jev pick được → không tốn LLM call |
| Arg tool | Jev kẹt → FallbackModel nhận **cả bước** (không chỉ phần args) |
| Design tip | Tách tool thành no-arg khi có thể → maximize Jev coverage |

> **Tóm gọn 1 câu:** Ngưỡng 0.6 chỉ là điểm khởi đầu; thiết kế công cụ không tham số càng nhiều thì Jev càng gánh được nhiều mà không tốn lượt gọi LLM.

---

## 5. Jev Trong Harness

Phần này cho biết đặt Jev ở đâu trong khung điều phối agent (harness) để các bước quyết định lặp lại không phải dùng LLM.

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Gắn Jev vào các **bước quyết định của harness**: retrieve (chọn nguồn), decide tools (chọn tool set), workflow gates (điều kiện chuyển bước). Jev là **semantic decision layer** nằm giữa raw context và hành động của agent.
> **Ẩn dụ/so sánh:** Giống **người điều phối trong xưởng**: không tự hàn (LLM viết), nhưng quyết định *bộ phận nào nhận việc* và *bước nào được sang bước tiếp* — trong vài chục mili-giây mỗi quyết định.
> **Vì sao quan trọng:** Harness có nhiều bước **quyết định nhịp cao** (mọi tool selection, mọi gate) — dùng LLM cho từng bước đó vừa chậm vừa đắt. Jev làm các bước này gần free; LLM chỉ viết khi cần text.

Giải nghĩa: **retrieve** = bước chọn nguồn dữ liệu lấy ra; **workflow gate** = cửa kiểm tra điều kiện trước khi chuyển bước; **semantic decision layer** = tầng quyết định dựa trên ý nghĩa nội dung (không phải cú pháp hay vị trí).

> **Tóm gọn 1 câu:** Trong harness, Jev là tầng quyết định giữa dữ liệu thô và hành động: chọn nguồn, chọn bộ tool, và gate chuyển bước — gần miễn phí, LLM chỉ viết.

### 5.1 Jev Tại Các Điểm Quyết Định Trong Harness

Phần này vẽ ba điểm đặt Jev trong harness, theo thứ tự chạy.

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

Cách đọc khối trên: ba điểm quyết định theo thứ tự — (1) RETRIEVE: Jev chọn nguồn/đoạn dữ liệu nào lấy ra (Choice); (2) DECIDE TOOLS: Jev chọn bộ tool nào phù hợp (Choice); (3) WORKFLOW GATE: Jev chấm pass/fail trước khi chuyển bước (Noul), tự động nếu band HIGH, escalate hoặc LLM-as-judge nếu band LOW; sau cùng LLM viết phần văn bản/code của bước được phép. (**LLM-as-judge** = dùng LLM làm người chấm thay Jev khi cần suy luận sâu.)

Cách đọc bảng cross-link dưới: cột **Bước harness** là tên bước; cột **Jev làm gì** là vai trò cụ thể; cột **Doc** trỏ tới tài liệu chi tiết của bước đó.

| Bước harness | Jev làm gì | Doc |
|--------------|-----------|-----|
| Decide tools / MCP | Chọn tool phù hợp context (Choice trên tool list) | [harness/06-decide-tools-mcp](../../harness/06-decide-tools-mcp/) |
| Workflow transitions | Gate điều kiện next step (Noul + threshold) | [harness/07-workflow](../../harness/07-workflow/) |

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/04-5-1-jev-tai-cac-iem-quyet-inh.py`](examples/04-5-1-jev-tai-cac-iem-quyet-inh.py)

</details>

> **Tóm gọn 1 câu:** Ba điểm đặt Jev trong harness: chọn nguồn, chọn bộ tool, gate chuyển bước — chi tiết từng bước ở hai doc cross-link phía trên.

---

## 6. Jev Trong Loop & Graph

Phần này mở rộng cùng ý tưởng sang hai cấu trúc khác: vòng lặp thực thi (loop) và bản đồ quan hệ (graph).

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Trong **loop**, Jev đảm nhận các **decision steps** (triage loop nào chạy, verify artifact có pass không); trong **graph**, Jev là **decision layer** trên node/edge — phân loại tri thức, gate transition, không thay thế traversal hay storage.
> **Ẩn dụ/so sánh:** Loop là **dây chuyền tự chạy** — Jev là công tắc quyết định *máy nào chạy* và *lô nào đạt chuẩn*. Graph là **bản đồ quan hệ** — Jev là **người gác cổng** phân loại tin nhắn đi qua bản đồ, không phải người vẽ bản đồ.
> **Vì sao quan trọng:** Cả loop và graph đều có nhiều bước quyết định nhịp cao; gắn Jev đúng chỗ (triage + verify) giúp loop/graph **nhanh và rẻ** ở tầng điều khiển, giữ LLM cho phần viết.

Giải nghĩa: **artifact** = sản phẩm trung gian agent tạo ra (patch, file, báo cáo); **traversal** = việc đi qua các node/edge của graph; **node/edge** = điểm và đường nối trong bản đồ quan hệ; **subgraph** = phần của graph được chọn ra.

> **Tóm gọn 1 câu:** Trong loop và graph, Jev là công tắc và gác cổng ở tầng điều khiển — quyết nhanh cái nào chạy, cái nào đạt — còn LLM giữ phần viết.

### 6.1 Jev Trong Execution Loop

Phần này vẽ một vòng lặp thực thi có Jev ở hai điểm: triage đầu vòng và verify trước khi test.

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

Cách đọc khối trên: lịch chạy kích hoạt → Jev triage "loop nào có việc?" (band HIGH tự chạy, LOW bỏ qua/escalate) → worktree + LLM viết patch → Jev soát nhanh "patch có căn cứ không?" → đạt thì chạy test đầy đủ, hỏng thì từ chối sớm → cuối cùng người duyệt rồi commit. (**Worktree** = bản sao làm việc tách ra của repo; **patch** = thay đổi code đề xuất.)

**Pattern chính**: **verified cascade trong loop** — Jev làm pre-screen nhanh (70–500ms) trước khi tốn resources chạy full test suite. Jev fail → reject ngay, không mời verifier LLM to. Cross-link: [loop/01-concepts — execution loop & anatomy](../../loop/01-concepts/) (maker/checker split — Jev đóng vai checker *tốc độ cao* tầng đầu). (**Maker/checker split** = nguyên tắc người làm khác người kiểm; **pre-screen** = soát nhanh trước.)

> **Tóm gọn 1 câu:** Trong loop, Jev đứng ở triage đầu vòng và pre-screen cuối vòng — patch hỏng bị từ chối ngay trước khi tốn tiền chạy test đầy đủ.

### 6.2 Jev Trong Graph

Phần này vẽ lớp quyết định đặt trên graph: phân loại node, gate edge, chấm điểm đường đi.

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

Cách đọc khối trên: mỗi node/edge của graph được Jev phân loại nhanh (Choice), chặn cho/không đi qua (Noul), và chấm độ liên quan (Score); graph store và việc đi qua graph (Neo4j, NetworkX — phần mềm lưu/vẽ đồ thị) **không đổi**; cuối cùng LLM viết câu trả lời dựa trên phần graph được chọn.

Jev **không đọc graph, không traverse** — nó phân loại *metadata / context trích xuất từ node* thành quyết định. Xem [graph](../../graph/) để hiểu nền tảng graph engineering; Jev là lớp quyết định mỏng đặt trên trên.

### 6.3 Bảng Vị Trí Jev

Cách đọc bảng này: cột **Framework** là cấu trúc hệ thống; cột **Jev ở đâu** là vai trò cụ thể trong cấu trúc đó; cột **Cross-link** trỏ tới tài liệu chi tiết. Ví dụ, hàng **Loop** nghĩa là: trong vòng lặp thực thi, Jev làm triage và pre-screen verify.

| Framework | Jev ở đâu | Cross-link |
|-----------|-----------|------------|
| **Loop** | Triage (chọn loop/pattern), verify pre-screen (Noul/Score) | [loop/01-concepts](../../loop/01-concepts/) |
| **Graph** | Decision layer: classify nodes, gate edges, score paths | [graph](../../graph/) |
| **Harness** | Retrieve / decide tools / workflow gates | [harness/06](../../harness/06-decide-tools-mcp/), [07](../../harness/07-workflow/) |
| **Verified cascade** | Draft check trong mọi framework trên | Pattern [05](../05-patterns/) |

> **Tóm gọn 1 câu:** Bảng trên tổng kết bốn nơi đặt Jev — loop, graph, harness, verified cascade — với cross-link tới doc chi tiết tương ứng.

---

## 7. Anti-Patterns Khi Kết Hợp

Phần này tổng hợp tám lỗi thiết kế hay gặp khi ghép Jev với LLM — học để tránh khỏi đầu.

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Các lỗi thiết kế phổ biến khi ghép Jev + LLM — chủ yếu xuất phát từ **đảo vai trò** (đòi Jev viết, đẩy quyết định vào prompt) hoặc **tin tưởng sai chỗ** (confidence mù quáng không fallback).
> **Ẩn dụ/so sánh:** Giống **đeo găng tay boxing để gõ bàn phím** — dụng cụ không sai, nhưng dùng sai việc thì vừa hỏng việc vừa mỏi tay.
> **Vì sao quan trọng:** Mỗi anti-pattern dưới đây đều dẫn đến: kết quả sai khó phát hiện, cost không giảm, hoặc hệ thống "có vẻ thông minh" nhưng không calibrate.

### 7.1 Bảng Anti-Patterns

Cách đọc bảng này: cột **#** là số thứ tự (để viện dẫn lại cho gọn); cột **Anti-pattern** là tên lỗi; cột **Triệu chứng** là dấu hiệu bạn đang mắc; cột **Sửa thế nào** là cách chữa. Ví dụ, hàng 1 nghĩa là: nếu bạn cố "hỏi" Jev để viết email thì không có output — vì Jev không sinh text; việc đó thuộc về LLM.

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

> **Tóm gọn 1 câu:** Tám anti-pattern đều quy về hai gốc: đảo vai trò (đòi Jev viết, đẩy câu hỏi vào state) và tin tưởng sai chỗ (confidence mù quáng, không fallback, không đo).

### 7.2 Mã Hóa Anti-Pattern #2 — State Là Material

Phần này minh họa trực quan lỗi #2: state là dữ liệu nguyên liệu, không phải chỗ gõ hướng dẫn.

```
   ❌ SAI:  state = "Hãy chọn queue: billing hay tech? Trả lời A/B."
            → biến Jev/LLM thành prompt-questioner, không có material

   ✅ ĐÚNG: state    = "Ticket: Tôi bị trừ tiền 2 lần cho đơn #4821..."
            questions = {"queue": {type: choice, options: [...]}}
            → state là dữ liệu, questions là câu hỏi
```

Cách đọc khối trên: ❌ SAI — state chứa câu lệnh "Hãy chọn queue..." làm model thành "người đọc đề trong dữ liệu", không có nguyên liệu để phán; ✅ ĐÚNG — state chứa nội dung ticket thật, câu hỏi nằm trong `questions` với kiểu rõ ràng (options = danh sách lựa chọn).

> **Tóm gọn 1 câu:** State chỉ chứa dữ liệu nguyên liệu; câu hỏi luôn nằm trong `questions` — trộn hai cái là lỗi phổ biến nhất.

### 7.3 Mã Hóa Anti-Pattern #3/#4 — Fallback Bắt Buộc

Phần này chứa code mẫu cài đặt nhánh dự phòng bắt buộc cho hai lỗi #3 (tin confidence mù quáng) và #4 (không có fallback).

> 📄 **Code ví dụ:** [`examples/05-7-3-ma-hoa-anti-pattern-3-4.py`](examples/05-7-3-ma-hoa-anti-pattern-3-4.py)

</details>

> **Tóm gọn 1 câu:** Hai lỗi #3/#4 được sửa bằng quy tắc bất di bất dịch: mọi vùng độ tự tin — kể cả cao nhất — phải có nhánh dự phòng rõ ràng.

---

> *"Jev là lớp quyết định trong phần mềm bình thường: state vào, kết quả typed có giới hạn ra, business rules hành động. LLM viết phần còn lại."*

---

*Trở về [README](../README.md) — tổng quan Module XIV*

*Tiếp theo: [07 — Giới Hạn & Đánh Giá](../07-limits-and-evaluation/) →*

*Trước đó: [05 — Patterns: Xây Dựng Quyết Định Production](../05-patterns/)*
