# 🔌 03. API & Tích Hợp

> Phần này hướng dẫn **gọi Jev lần đầu**: endpoint & xác thực, cấu trúc **request/response** đầy đủ, **SDK chính thức**, và các integration — **Pydantic AI**, **LangChain**, **OpenRouter** — cùng **giới hạn & mã lỗi** thường gặp. Đọc [02-primitives](../02-primitives/) trước nếu bạn chưa rõ ba question types.

> **Cách đọc phần này:** *endpoint* = địa chỉ URL để gửi yêu cầu tới; *request/response* = gói dữ liệu gửi đi và nhận về; *SDK* = thư viện có sẵn giúp bạn gọi API mà không tự viết mã HTTP; *integration* = cách nối Jev vào công cụ bạn đã dùng (Pydantic AI, LangChain, OpenRouter).

---

## 1. Endpoint & Xác Thực

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Jev chỉ có **một endpoint duy nhất**: `POST https://api.typesafe.ai/v1/systemone`, xác thực bằng **Bearer API key**. Phiên bản hiện tại là **jev-1.13.0**, bạn có thể dùng alias **jev-latest** để luôn nhận bản mới nhất.
> **Ẩn dụ/so sánh:** Giống như **gọi một hàm trên cloud** — một URL, một key, một body JSON. Không streaming, không hội thoại nhiều lượt — mỗi request là **một lần quyết định độc lập**.
> **Vì sao quan trọng:** API rất gọn nên tích hợp nhanh. Nhưng bù lại nó **không nhớ trạng thái** — bạn phải tự quản lý context (state) ở phía ngoài; xem thêm [04-calibration](../04-calibration/) về cách giữ state sạch.

Giải nghĩa nhanh các thuật ngữ: `POST` = loại yêu cầu HTTP dùng để gửi dữ liệu; **Bearer API key** = cách xác thực bằng cách đính kèm chuỗi khóa bí mật (`tsk_...`) vào tiêu đề yêu cầu, như quẹt thẻ trước cửa; **alias** = tên giả trỏ tới phiên bản thật (`jev-latest` → `jev-1.13.0`); **state** = dữ liệu bạn đưa vào để Jev phán đoán.

> **Tóm gọn 1 câu:** Jev là một URL duy nhất, gọi bằng khóa bí mật, mỗi lần gọi là một quyết định độc lập và API không nhớ gì giữa hai lần gọi.

### 1.1 Cấu Trúc Endpoint

Phần này mô tả: một lần gọi gồm địa chỉ, khóa xác thực, và nội dung JSON — đây là thứ bạn cần chuẩn bị cho lần gọi đầu tiên.

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

Cách đọc khối trên: dòng `POST ...` là địa chỉ gửi yêu cầu tới; dòng `Authorization` là nơi đặt khóa (`Bearer <key>` = đính kèm khóa sau chữ "Bearer"); khối JSON là nội dung — `model` chọn phiên bản, `state` là dữ liệu phán đoán, `questions` là các câu hỏi có kiểu (mỗi câu trả về một đáp án có tên để bạn đọc về sau).

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

Cách đọc sơ đồ trên: `jev-latest` là **tên bí danh** — tự động trỏ sang bản mới nhất mỗi khi TypeSafe cập nhật; `jev-1.13.0` là **ghim phiên bản** (pin = chốt cứng số bản, không đổi). Production nên ghim, vì bí danh đổi bản lúc nào bạn không biết.

> **Tóm gọn 1 câu:** Một lần gọi = địa chỉ + khóa trong tiêu đề + JSON gồm model, state (dữ liệu), questions (câu hỏi có tên và kiểu).

### 1.2 Xác Thực

Phần này cho biết cách gửi khóa xác thực và hai mã lỗi hay gặp khi khóa sai.

```
# Environment
export TYPESAFE_API_KEY="tsk_..."

# Header
Authorization: Bearer $TYPESAFE_API_KEY

# Lỗi xác thực thường gặp: 401 (sai key) / 403 (key không có scope)
```

Cách đọc: dòng `export` lưu khóa vào biến môi trường (biến hệ thống của phiên làm việc, tránh viết khóa cứng trong code); dòng `Authorization` gắn khóa vào mỗi yêu cầu. `401` = máy chủ không nhận khóa (sai hoặc thiếu); `403` = khóa đúng nhưng **không có quyền** cho việc này (scope = phạm vi quyền của khóa).

> **Gợi ý production**: pin `jev-1.13.0` (không dùng alias) để tránh thay đổi âm thầm khi TypeSafe roll `jev-latest`; upgrade chủ động khi đọc changelog.

> **Tóm gọn 1 câu:** Đặt khóa vào biến môi trường, gắn vào tiêu đề `Authorization: Bearer`; 401 nghĩa là khóa sai, 403 nghĩa là khóa không có quyền.

---

## 2. Request & Response

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Request = `{model, state, questions}`. **questions** là named map — mỗi key là **tên answer** bạn sẽ đọc về sau, mỗi value là một primitive (Choice / Score / Noul). Response trả về **`answers.<name>.<primitive>`** kèm probabilities và confidence — **tất cả questions trong 1 pass song song**.
> **Ẩn dụ/so sánh:** Như **phiếu trả lời có chấm tròn sẵn**: bạn in sẵn câu hỏi (questions), Jev tô đen đáp án (selected / score / p) và ghi **độ tập trung** bên cạnh. Bạn không "đọc văn bản trả lời" — bạn **đọc phiếu**.
> **Vì sao quan trọng:** Response shape cố định theo primitive → code unpack typed, không regex. Nhớ rằng thêm questions gần như **không đổi latency**, chỉ thêm input tokens ($0.042/M) — gom hết vào 1 request.

Giải nghĩa: **named map** = đối tượng JSON có tên đặt sẵn cho từng câu hỏi, ví dụ `team` là tên và bạn đọc kết quả về sau qua `answers.team`; **primitive** = một trong ba kiểu câu hỏi (Choice / Score / Noul — chi tiết ở [02-primitives](../02-primitives/)); **probabilities** = phần trăm rơi vào từng lựa chọn; **confidence** = mức độ tập trung của phân phối, **không phải** xác suất đúng (xem [04-calibration](../04-calibration/)).

> **Tóm gọn 1 câu:** Gửi một đống câu hỏi cùng lúc, nhận về từng đáp án có tên kèm xác suất và độ tự tin — như một phiếu trả lời chấm tròn sẵn.

### 2.1 Ví Dụ Request Đầy Đủ — 3 Questions

Phần này trỏ tới file mẫu: một request thật gồm ba câu hỏi (chọn nhóm, có/không hoàn tiền, chấm mức khẩn) để bạn sao chép và sửa.

> 📄 **Code ví dụ:** [`examples/01-2-1-vi-du-request-ay-u-3.json`](examples/01-2-1-vi-du-request-ay-u-3.json)

> **Tóm gọn 1 câu:** File JSON mẫu ở trên là bản request hoàn chỉnh — copy về, đổi state và questions theo bài của bạn.

### 2.2 Response Shape

Phần này trỏ tới file mẫu: hình dạng dữ liệu trả về cho từng kiểu câu hỏi (choice, noul, score).

> 📄 **Code ví dụ:** [`examples/02-2-2-response-shape.json`](examples/02-2-2-response-shape.json)

> **Tóm gọn 1 câu:** File JSON mẫu cho thấy response trả về gì cho mỗi primitive — đọc nó trước khi viết code unpack.

### 2.3 Đọc Response — Bảng Map Sang Code

Cách đọc bảng này: cột **Field** là tên trường trong response; cột **Nghĩa** giải thích trường đó nói lên điều gì; cột **Dùng trong code** là chỗ bạn nên dùng nó. Ví dụ, dòng `choice` nghĩa là: trường `choice` chứa lựa chọn đã chọn, và bạn dùng nó trong câu lệnh rẽ nhánh (switch/route) của code.

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

Giải nghĩa thêm: **distribution** = phân phối xác suất trên tất cả lựa chọn, không chỉ lựa chọn thắng; **intrinsic** = tính từ chính p, không cần đo thêm; **prob-weighted** = điểm tính theo trọng số xác suất nên có thể lọt giữa hai mức (ví dụ 3.4, nằm giữa mức 3 và mức 4). Hàng **confidence** nhấn mạnh: đây **không phải** xác suất đúng.

> **Tóm gọn 1 câu:** Bảng trên là từ điển chuyển trường response thành code: choice/p/score để quyết, probabilities/distribution để phát hiện mơ hồ, confidence/certainty để đặt ngưỡng.

### 2.4 Một Lần Gọi — Cả Ba Cùng Lúc (Minh Hoạ Parallel)

Phần này minh hoạ: ba câu hỏi gửi trong **một** lượt gọi và được chấm **song song**, nên thêm câu hỏi gần như không làm chậm.

```
                        ┌── q "team.choice"         ──► choice + probs
state + 3 questions ────┼── q "refund_requested.noul" ──► noul + p
                        └── q "urgency.score"        ──► score + dist
                              │
                              └── 1 PASS SONG SONG ──► 70-500ms
```

Cách đọc sơ đồ: từ một cặp state + 3 questions, ba câu được chấm đồng thời trong một lượt ("1 pass song song") và trả kết quả sau 70–500 mili-giây — thay vì xếp hàng chờ từng câu.

> **Tóm gọn 1 câu:** Gom hết câu hỏi vào một lượt gọi — chúng được chấm song song trong 70–500ms, thêm câu hỏi gần như miễn phí về thời gian.

---

## 3. SDK Chính Thức

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** TypeSafe phát hành **Python SDK** và **JavaScript SDK** chính thức — wrap cùng một endpoint, trả typed objects. Khi stack của bạn đã đi qua **OpenRouter** (một key nhiều model), bạn cũng có thể **đặt base URL của OpenRouter** và vẫn dùng SDK/TS SDK.
> **Ẩn dụ/so sánh:** Như **client HTTP có typed models** — bạn không tự map JSON; SDK trả object có attribute (`answer.choice`, `answer.p`) giống ORM.
> **Vì sao quan trọng:** SDK chuẩn hoá error handling và typing — tránh sai sót tay khi unpack response, nhất là khi bạn đọc `confidence` vs `certainty` cho từng primitive (nhầm hai khái niệm này là bug âm thầm nguy hiểm — [04-calibration](../04-calibration/)).

Giải nghĩa: **typed objects** = object có thuộc tính đặt tên sẵn (`answer.choice`, `answer.p`), trình biên dịch/IDE biết kiểu nên bạn không tự bấm chuỗi JSON; **base URL** = địa chỉ gốc mà SDK gọi tới — đổi địa chỉ này là SDK gọi tới nơi khác mà không đổi code. **ORM** (so sánh trong ẩn dụ) = thư viện cho phép đọc dữ liệu như object thay vì viết câu SQL tay.

> **Tóm gọn 1 câu:** SDK giúp bạn đọc kết quả như object có kiểu thay vì tự bóc JSON tay — ít lỗi, và cùng SDK dùng được cho cả TypeSafe lẫn OpenRouter.

### 3.1 Quickstart

Phần này chứa hai đoạn code chạy ngay được — một cho Python, một cho JavaScript. Bấm vào tiêu đề để mở.

<details>
<summary>Python — Quickstart (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/03-3-1-quickstart.py`](examples/03-3-1-quickstart.py)

</details>

<details>
<summary>JavaScript — Quickstart (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/04-3-1-quickstart.js`](examples/04-3-1-quickstart.js)

</details>

> **Tóm gọn 1 câu:** Hai file quickstart ở trên là đường ngắn nhất để gọi Jev lần đầu — copy, đặt khóa, chạy.

### 3.2 Đổi Base URL Sang OpenRouter

Phần này cho biết: nếu đội bạn đã trả tiền OpenRouter, bạn dùng lại SDK nhưng trỏ nó sang địa chỉ OpenRouter.

```
# Khi stack đã có OpenRouter key — dùng lại SDK, chỉ đổi base URL
TYPESAFE_API_KEY=<openrouter_key>
TYPESAFE_BASE_URL=https://openrouter.ai/api/alpha

# → SDK gọi /decisions trên OpenRouter thay vì api.typesafe.ai
# Model name: "typesafe/jev-1.13" (xem §6)
```

Cách đọc khối trên: thay khóa TypeSafe bằng khóa OpenRouter và đổi `TYPESAFE_BASE_URL` sang địa chỉ OpenRouter; SDK sẽ gọi tới `/decisions` của OpenRouter. Model khi đó phải viết đủ nhà cung cấp: `typesafe/jev-1.13`.

> **Tóm gọn 1 câu:** Đổi đúng hai biến (khóa + base URL) là SDK chạy qua OpenRouter — không cần sửa code.

---

## 4. Pydantic AI — TypeSafeModel

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Pydantic AI tích hợp Jev qua **`TypeSafeModel`**: **mỗi field của `output_type` trở thành một question** cho Jev; **`field description` = text câu hỏi**; **`docstring`/`instructions` = framing**. Output là Pydantic object typed — không sinh text, không parse.
> **Ẩn dụ/so sánh:** Giống **biến dataclass thành phiếu hỏi**: mỗi annotation (`team: str`) là một ô tròn Jev phải tô; description là đề bài cho ô đó; docstring là hướng dẫn chung cho cả bài.
> **Vì sao quan trọng:** Đây là mô hình **NGƯỢC thói quen prompting** — câu hỏi sống trên **type**, không sống trong prompt string. TypeSafe gọi đây là *concept quan trọng nhất* của integration: **put the question on the field, not in the prompt**. (Tương ứng best practice §6 ở [02-primitives](../02-primitives/).)

Giải nghĩa: **Pydantic AI** = framework Python cho agent, nơi bạn khai báo cấu trúc kết quả bằng class; **output_type** = class mô tả kết quả đầu ra mong muốn; **field** = một dòng thuộc tính trong class (ví dụ `team: str`); **field description** = dòng chú thích giải nghĩa cho field đó (viết trong `Field(description=...)`); **docstring** = chuỗi mô tả ngay dưới dòng `class`; **framing** = khung chung định hướng cách chấm cho toàn bộ yêu cầu.

> **Tóm gọn 1 câu:** Mỗi field trong class kết quả trở thành một câu hỏi cho Jev — câu hỏi nằm trên kiểu dữ liệu, không nằm trong prompt.

### 4.1 Mapping output_type → Questions

Cách đọc bảng này: cột trái là thứ bạn khai trong Pydantic AI; cột phải là thứ nó trở thành trong request Jev. Ví dụ, một field kiểu `bool` (đúng/sai) sẽ thành một câu hỏi Noul (kiểu có/không).

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

Giải nghĩa thêm: **Literal/Enum** = kiểu chỉ cho phép vài giá trị liệt kê sẵn (ví dụ `Literal["billing","tech","sales"]`) → thành câu hỏi Choice; **FAN-OUT** = một danh sách field sinh ra nhiều câu hỏi, mỗi phần tử một câu; **nested model** = class nằm trong class, câu hỏi con đặt tên dạng chấm (`outer.inner`).

> **Tóm gọn 1 câu:** Bảng trên là bản đồ chuyển đổi: field → câu hỏi, kiểu dữ liệu → primitive, docstring → khung chung.

### 4.2 Ví Dụ

Phần này chứa code mẫu Python khai `TypeSafeModel` với output_type thật. Bấm vào để mở.

<details>
<summary>Python — TypeSafeModel (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/05-4-2-vi-du.py`](examples/05-4-2-vi-du.py)

</details>

> **Tóm gọn 1 câu:** File mẫu ở trên cho thấy cả quy trình: khai class kết quả → Jev tự sinh câu hỏi → nhận lại object có kiểu.

### 4.3 Các Trường Hợp Đặc Biệt

Phần này nói về bốn tình huống hay gặp khi khai output_type; tình huống thứ tư là lỗi bắt buộc sửa.

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

Giải nghĩa khối trên: **LIST FAN-OUT** = danh sách field tạo nhiều câu hỏi trong một lượt; **NESTED MODELS** = class con tạo câu hỏi dạng chấm (`ticket.team`); mục 3 nhắc phân vai — hướng dẫn chung để ở instructions của agent, câu hỏi cụ thể để ở description; mục 4 là lỗi: field `bool` **bắt buộc** có description, vì Noul chấm một mệnh đề (proposition = câu phát biểu có thể đúng/sai) — thiếu description tức là không có mệnh đề nào để chấm. `UserError` = lỗi từ phía cách khai của bạn, không phải lỗi máy chủ.

> **Tóm gọn 1 câu:** Danh sách sinh nhiều câu hỏi, class lồng nhau sinh câu hỏi dạng chấm, và field bool bắt buộc có description — thiếu là bị từ chối ngay.

### 4.4 Tools Kèm Theo — Tool-Call Threshold

Phần này giải thích: khi agent có kèm tools, Jev tự thêm một câu hỏi "tool nào được gọi" và một ngưỡng quyết định hành vi.

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

Giải nghĩa: **arguments** = tham số của tool (ví dụ `delete_file(path=...)` cần `path`); **threshold 0.6** = mức tự tin tối thiểu để Jev tự chọn tool; **ToolCallProposed** = loại lỗi tín hiệu "Jev chọn được tool nhưng không viết được tham số"; **FallbackModel** = LLM đứng sau Jev nhận xử lý thay; **step** = toàn bộ bước làm việc hiện tại, không chỉ phần tham số.

<details>
<summary>Python — FallbackModel (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/06-4-4-tools-kem-theo-tool-call-threshold.py`](examples/06-4-4-tools-kem-theo-tool-call-threshold.py)

</details>

> **Tóm gọn 1 câu:** Jev chọn tool khi tự tin đạt 0.6; tool nào cần tham số thì Jev không viết được — LLM đứng sau nhận cả bước.

---

## 5. LangChain — TypeSafeClassifier

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** LangChain tích hợp Jev qua **`TypeSafeClassifier`** — một classifier model nhận **cùng state + questions** qua **`.invoke()`**, trả typed answers. Dễ nhét vào chain/middleware hiện có (routing, risk gate) thay vì đổi cả stack.
> **Ẩn dụ/so sánh:** Như **thay router Wi-Fi cũ bằng router nhanh hơn** — cùng dây mạng, cùng giao thức, chỉ phần xử lý packet nhanh và calibrated hơn.
> **Vì sao quan trọng:** Routing / triage / AutoMode gate là System One-shaped — dùng LLM ở đây là chậm và đắt. TypeSafeClassifier cho bạn **typed answer trong 70-500ms** ngay trong chain LangChain.

Giải nghĩa: **LangChain** = framework Python để lắp các bước xử lý ngôn ngữ thành chuỗi (chain); **`.invoke()`** = hàm chuẩn của LangChain để chạy một model/step với dữ liệu vào; **middleware** = bước chen giữa hai bước trong luồng xử lý; **risk gate** = cửa kiểm tra rủi ro trước khi cho hành động chạy.

> **Tóm gọn 1 câu:** TypeSafeClassifier là "model" LangChain trả đáp án có kiểu trong 70–500ms — cắm thẳng vào chain hiện có mà không đổi stack.

### 5.1 Cơ Bản

Phần này chứa code mẫu Python dùng TypeSafeClassifier cơ bản. Bấm vào để mở.

<details>
<summary>Python — TypeSafeClassifier (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/07-5-1-co-ban.py`](examples/07-5-1-co-ban.py)

</details>

> **Tóm gọn 1 câu:** File mẫu ở trên cho thấy cách gọi TypeSafeClassifier qua `.invoke()` — tương tự gọi model LangChain khác.

### 5.2 Trong Agent Middleware

Phần này cho biết hai vị trí hay đặt classifier nhất trong luồng agent: định tuyến lúc nhận tin, và chặn hành động rủi ro trước khi chạy.

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

Giải nghĩa: **ROUTING MIDDLEWARE** = tin nhắn vào → classifier phân loại → chuyển tới nhánh agent đúng việc; **AutoModeMiddleware** = bộ đếm trong LangChain chặn tool call đề xuất, hỏi classifier "rủi ro không?": rủi ro thấp thì cho tự chạy, rủi ro cao thì chặn trước khi tool kịp chạy; **System One-shaped** = việc mang hình dạng quyết định nhanh có kiểu — đúng sở trường của Jev, không phải của LLM.

> **Tóm gọn 1 câu:** Hai chỗ đặt classifier: định tuyến tin nhắn lúc vào, và chặn tool rủi ro trước khi chạy — cả hai đều dùng Jev thay LLM.

---

## 6. OpenRouter

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Jev có sẵn trên OpenRouter qua endpoint decisions riêng: `POST https://openrouter.ai/api/alpha/decisions`, model **`typesafe/jev-1.13`**. Áp dụng khi bạn **muốn một key gọi nhiều model** — không thêm key TypeSafe riêng.
> **Ẩn dụ/so sánh:** Như **hub điện multi-socket** — một ổ cắm (một key), nhiều thiết bị (nhiều model), Jev là một socket nữa trong hub.
> **Vì sao quan trọng:** Giảm operational overhead cho team đã standardise OpenRouter; cũng là đường migrate dễ — sau này muốn switch sang key TypeSafe trực tiếp chỉ đổi base URL.

Giải nghĩa: **OpenRouter** = dịch vụ "một khóa gọi nhiều model AI" — bạn chỉ giữ một khóa và một hóa đơn; **endpoint `/decisions`** = địa chỉ riêng của OpenRouter cho các yêu cầu quyết định kiểu Jev; **base URL** = địa chỉ gốc SDK gọi tới (đổi nó là đổi nhà cung cấp mà không sửa code).

> **Tóm gọn 1 câu:** Nếu đội bạn đã dùng OpenRouter, Jev chỉ là thêm một model trong hub có sẵn — cùng một khóa, không cần khóa TypeSafe riêng.

### 6.1 Gọi Trực Tiếp Qua OpenRouter

Phần này trỏ tới file mẫu: gọi thẳng endpoint `/decisions` của OpenRouter bằng HTTP thuần, không qua SDK.

> 📄 **Code ví dụ:** [`examples/08-6-1-goi-truc-tiep-qua-openrouter.json`](examples/08-6-1-goi-truc-tiep-qua-openrouter.json)

> **Tóm gọn 1 câu:** File mẫu JSON cho thấy cách gọi thẳng OpenRouter — đúng cấu trúc như gọi TypeSafe, chỉ khác địa chỉ và tên model.

### 6.2 Qua TypeSafe TS SDK + OpenRouter Base URL

Phần này trỏ tới file mẫu: dùng SDK chính thức của TypeSafe nhưng trỏ sang OpenRouter — giữ code cũ, đổi khóa và base URL.

> 📄 **Code ví dụ:** [`examples/09-6-2-qua-typesafe-ts-sdk-openrouter-base.js`](examples/09-6-2-qua-typesafe-ts-sdk-openrouter-base.js)

> **Tóm gọn 1 câu:** Giữ SDK, đổi khóa + base URL là chạy qua OpenRouter — đây là đường chuyển ngược về TypeSafe dễ nhất sau này.

### 6.3 Khi Nào Chọn Đường Nào

Phần này tóm tắt tiêu chí chọn: một khóa cho tất cả model, hay kiểm soát trực tiếp với TypeSafe.

```
Muốn 1 key cho MỌI model (LLM + Jev)   ──► OpenRouter
Muốn latency/ính trực tiếp TypeSafe,   ──► api.typesafe.ai
pin jev-1.13.0, quyền config RLCD-ish      (SDK chính thức)
```

Giải nghĩa: **latency/ính trực tiếp** = đi thẳng TypeSafe thì ít khâu chuyển tiếp hơn; **pin** = ghim phiên bản; **RLCD-ish config** = các tùy chọn phía TypeSafe liên quan cách tối ưu xác suất (viết ngắn gọn là "RLCD-ish").

> **Tóm gọn 1 câu:** Muốn một khóa chung cho mọi model thì dùng OpenRouter; muốn kiểm soát phiên bản và độ trễ trực tiếp thì gọi TypeSafe bằng SDK chính thức.

---

## 7. Giới Hạn & Lỗi

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** jev-1.13 là **text input only**: không generate text, không viết tool arguments, không đọc file; **giữ arithmetic, counting, date comparison trong code**. Context limit **64k tokens** tổng cho state + questions (**32k cho state** cộng **câu hỏi dài nhất**) — vượt quá báo `ModelHTTPError (max_tokens_exceeded)`.
> **Ẩn dụ/so sánh:** Như **một thẩm phán chỉ đọc được hồ sơ giấy tới 64k chữ** — hết trang là stop, không phải đọc thêm; và thẩm phán **không tự tay viết bản án text** — chỉ phán quyết có/không/điểm.
> **Vì sao quan trọng:** Đây là **non-goals cố ý** (không phải bug sắp fix). Thiết kế sai kỳ vọng = outage + billed tokens vô ích. Bảng lỗi dưới đây nên được **dán vào runbook** của team.

Giải nghĩa: **non-goal** = điều sản phẩm cố tình không làm, không phải thiếu sót; **outage** = sự cố hệ thống ngừng phục vụ; **runbook** = sổ tay vận hành để đọc nhanh khi có sự cố; **64k tokens** = giới hạn ~64 nghìn "từ chiếc" của model — vượt là bị từ chối; **`ModelHTTPError (max_tokens_exceeded)`** = mã lỗi báo "nội dung vượt giới hạn".

> **Tóm gọn 1 câu:** Jev 1.13 chỉ đọc chữ, không viết và không tính toán — gửi đúng thể loại việc cho nó, và để giới hạn 64k token vào runbook của team.

### 7.1 Non-Goals Của jev-1.13

Cách đọc bảng này: cột trái là những việc Jev **không** làm (cố ý, không phải lỗi); cột phải là thứ bạn dùng thay thế. Ví dụ, hàng đầu tiên: Jev không sinh văn bản — việc đó thuộc về LLM.

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

Giải nghĩa thêm: **arithmetic / counting / date comparison** = cộng trừ nhân chia, đếm số lượng, so sánh ngày tháng — việc của code, không phải của Jev; **multi-turn / conversation memory** = hội thoại nhiều lượt có nhớ — bạn phải tự giữ state và gửi lại mỗi lần.

> **Tóm gọn 1 câu:** Bảng trên là danh sách "đừng giao việc này cho Jev": chữ, tham số, file, phép tính, quá 64k token, và trí nhớ hội thoại — mỗi mục đều có bên thay thế rõ ràng.

### 7.2 Bảng Mã Lỗi Thường Gặp

Cách đọc bảng này: cột **Lỗi / Mã** là tên lỗi bạn gặp trong code hoặc log; cột **Nguyên nhân** giải thích vì sao lỗi xảy ra; cột **Cách xử lý** là việc cần làm. Ví dụ, hàng `401 Unauthorized` nghĩa là: khóa sai hoặc thiếu — kiểm tra tiêu đề `Authorization: Bearer`.

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

Giải nghĩa thêm: **backoff** = thử lại sau với khoảng chờ tăng dần (1s, 2s, 4s…) thay vì dồn dập; **5xx** = mã lỗi máy chủ (không phải lỗi của bạn); **threshold pass** = độ tự tin đạt ngưỡng 0.6 nhưng tool có tham số nên Jev vẫn không gọi được.

> **Tóm gọn 1 câu:** Sáu lỗi trong bảng trên đều có nguyên nhân và cách xử lý rõ — dán bảng này vào runbook là đội xử lý sự cố không phải đoán mò.

### 7.3 Checklist Trước Khi Go-Live

Phần này là danh sách việc cần tick hết trước khi mở Jev cho người dùng thật (go-live = chạy production).

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

Giải nghĩa: **state hygiene** = vệ sinh dữ liệu đầu vào — chỉ gửi phần liên quan; **escalate** = chuyển người hoặc hệ thống khác khi tự tin thấp; **retry mù** = thử lại y nguyên không sửa gì — gần như luôn gặp lại cùng lỗi; **eval** = bộ đánh giá có số đo.

> **Tóm gọn 1 câu:** Chín mục checklist trên là điều kiện tối thiểu để go-live an toàn — thiếu mục nào thì có thêm một rủi ro âm thầm.

---

## 8. Bảng Tích Hợp Tổng Hợp

Phần này là mục lục chọn đường: một bảng so sánh mọi cách nối Jev vào hệ thống của bạn.

Cách đọc bảng này: cột **Integration** là tên cách tích hợp; cột **Entry point** là hàm/địa chỉ bạn gọi; cột **Phù hợp khi** cho biết nên chọn cách đó trong hoàn cảnh nào. Ví dụ, hàng `Python SDK` nghĩa là: nếu service của bạn viết bằng Python, dùng `typesafe.Client.ask()`.

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

Giải nghĩa: **REST API** = gọi HTTP thuần, ngôn ngữ nào cũng được; **Node/TS** = JavaScript/TypeScript phía máy chủ; **typed agents** = agent cần kết quả có kiểu chặt (Pydantic); **Spice AI** = gọi Jev ngay trong câu SQL trên dữ liệu; **Refix** = công cụ runtime cho quy trình phát triển (dev workflow = việc hằng ngày của dev).

> **Tóm gọn 1 câu:** Bảng trên là menu chọn cách tích hợp — REST cho mọi stack, SDK cho từng ngôn ngữ, framework cho agent, OpenRouter cho stack đa model.

---

*Tiếp theo: [04 — Calibration](../04-calibration/)*

*Trở về [README](../README.md) — tổng quan Module XIV*
