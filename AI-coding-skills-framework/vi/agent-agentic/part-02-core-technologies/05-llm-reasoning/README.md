# 🧠 Module 5. LLM & Reasoning

> ## 📑 Mục Lục
>
> - [Câu Chuyện Mở Đầu](#câu-chuyện-mở-đầu)
> - [1. LLM hoạt động như thế nào?](#1-llm-hoạt-động-như-thế-nào)
> - [2. Tokens & Context Window](#2-tokens--context-window)
> - [3. System Prompt / User Prompt / Assistant Message](#3-system-prompt--user-prompt--assistant-message)
> - [4. Inference & Generation](#4-inference--generation)
> - [5. Temperature, Top-P, Max Tokens](#5-temperature-top-p-max-tokens)
> - [6. Chain-of-Thought (CoT)](#6-chain-of-thought-cot)
> - [7. Structured Output / JSON Mode](#7-structured-output--json-mode)
> - [8. Function Calling / Tool Calling](#8-function-calling--tool-calling)
> - [9. Model Limitations & Hallucination](#9-model-limitations--hallucination)
> - [Tóm Tắt & Checklist](#tóm-tắt--checklist)

---

## Câu Chuyện Mở Đầu

Bạn nhắn với một con bot hỗ trợ: *"Tôi muốn hoàn tiền đơn hàng #10234 vừa mua hôm qua."* Bot đáp trả một câu hoàn chỉnh, lịch sự, đúng yêu cầu — như thể nó "hiểu" mọi thứ. Nhưng sự thật nằm bên trong: **LLM không "hiểu" theo nghĩa con người — nó chỉ cực kỳ giỏi dự đoán từ tiếp theo.**

Cả module này sẽ bóc tách **LLM (Large Language Model)** từ góc nhìn của một người làm Agent: nó hoạt động thế nào, bị giới hạn ra sao, và làm cách nào để *điều khiển* nó cho ra đúng thứ mình muốn.

> **Tóm gọn 1 câu:** LLM là *máy dự đoán từ tiếp theo* cực giỏi — không "hiểu" như người, nhưng nói năng đủ tự nhiên để làm ta tưởng nó hiểu.

---

## 1. LLM hoạt động như thế nào?

Không cần code, không cần công thức. Chỉ cần hình dung về **Transformer** — kiến trúc mạng nơ-ron mà mọi LLM hiện đại (ChatGPT, Claude, Gemini...) đều dùng.

### Self-Attention: "chú ý" đúng chỗ

Trái tim của Transformer là **Self-Attention** — khả năng **tự đánh giá mức độ liên quan giữa mỗi từ với các từ còn lại trong câu.** Với câu *"Con [XXX] ngồi cạnh bàn, nó kêu meo meo"*, khi gặp chữ "nó", model tự hỏi "nó" là cái gì → nhận ra "nó" gắn với "con [XXX]" hơn là "bàn" → nhờ vậy giữ đúng ngữ cảnh khi sinh từ tiếp theo ("meo meo" ⇒ con mèo).

### Hai pha: Học (training) và Suy luận (inference)

- **Training (huấn luyện):** model "đọc" hàng nghìn tỷ từ trên internet, tinh chỉnh hàng tỷ tham số để dự đoán chính xác — giống một người đọc cả thư viện rồi *bắt chước* cách viết.
- **Inference (suy luận):** lúc bạn hỏi, model chạy các phép tính qua mạng nơ-ron để **chọn từ khả dĩ nhất** cho vị trí kế tiếp, rồi lặp lại từng token một cho đến khi ra chuỗi hoàn chỉnh.

> **Tóm gọn 1 câu:** LLM = một mạng nơ-ron kiểu Transformer với cơ chế *tự chú ý* (attention) — đã "đọc" rất nhiều văn bản khi học, và khi bạn hỏi thì *dự đoán từ tiếp theo* hết token này đến token khác.

---

## 2. Tokens & Context Window

### Token là gì?

**Token** là đơn vị nhỏ nhất mà LLM đọc/viết — không phải chữ cái, không hẳn là từ. Thường **1 token ≈ ¾ từ tiếng Anh** (hoặc 1–2 chữ tiếng Việt, 1 ký tự Trung).

Ví dụ: từ *"agent"* có thể là 1 token; cụm *"reasoning"* có thể tách thành `reason` + `ing` = 2 token.

Hai hệ quả thực tế: **giá API** tính theo token (đọc vào và sinh ra đều tính), và **giới hạn độ dài** prompt phụ thuộc token chứ không phải số từ, số dòng.

### Context Window — "cái bàn làm việc" của LLM

**Context Window (cửa sổ ngữ cảnh)** là **lượng token tối đa model nhìn được trong một lần xử lý**. Nó giống một cái bàn nhỏ: đặt được bao nhiêu đồ, model "nhìn thấy" bấy nhiêu.

- Cuộc trò chuyện + toàn bộ tài liệu đính kèm đều phải nằm gọn trên "cái bàn" này.
- Mỗi model có số cụ thể: 8k, 32k, 128k, 200k token...
- Giống trí nhớ ngắn hạn: hết "bàn" là **quên** — phần ngoài cửa sổ không tồn tại với model.

> **Tóm gọn 1 câu:** Token là đơn vị tính độ dài của LLM (≈ ¾ từ), còn Context Window giống *cái bàn làm việc* — chỉ những gì trên bàn model mới "thấy" được, ra ngoài là quên.

---

## 3. System Prompt / User Prompt / Assistant Message

Khi bạn trò chuyện với LLM qua API (hoặc bất kỳ app nào), thứ thật sự được gửi đi **không phải một câu hỏi đơn lẻ, mà là một danh sách message với 3 vai trò**:

| Message | Vai trò | Ví dụ |
|---|---|---|
| **System Prompt** | *Bối cảnh + luật chung* — vai trò, giọng điệu, quy tắc cho cả phiên; do nhà phát triển đặt, người dùng thường không thấy | "Bạn là trợ lý hỗ trợ khách của shop X. Luôn trả lời tiếng Việt, không bịa giá." |
| **User Prompt** | *Yêu cầu của người dùng* — câu hỏi, mệnh lệnh, dữ liệu thô | "Đơn hàng #10234 muốn hoàn tiền." |
| **Assistant Message** | *Câu trả lời của model* — nối vào lịch sử, làm ngữ cảnh cho lượt sau | "Dạ, anh cho thêm mã xác nhận được không ạ?" |

*Cách đọc bảng: System đặt "luật chơi", User đưa yêu cầu, Assistant là phản hồi — cứ thế lặp lại tạo thành hội thoại.*

### Vì sao phân biệt 3 loại này quan trọng với Agent?

Vì **prompt engineering thực chất là sắp xếp 3 vai này đúng chỗ**: System ổn định → đảm bảo model "xưng danh" và tuân thủ quy tắc cả phiên; User rõ ràng → hạn chế hiểu lầm; lịch sử Assistant → làm ngữ cảnh cho model nói tiếp mạch lạc.

> **Tóm gọn 1 câu:** Cuộc hội thoại với LLM là chuỗi message gồm System (luật chơi), User (yêu cầu), Assistant (phản hồi) — ai đặt đúng vai trò thì model "đóng vai" đúng.

---

## 4. Inference & Generation

**Inference (suy luận)** là thuật ngữ chỉ **một lần model chạy để tạo ra phản hồi** — từ lúc nhận prompt đến lúc trả về kết quả.

### Quá trình "Generation" diễn ra như thế nào?

Model nhận danh sách message (Mục 3), Transformer xử lý qua nhiều lớp mạng nơ-ron, tính **xác suất cho từng token tiếp theo**, chọn token có xác suất cao nhất theo chiến lược (temperature, top-p — Mục 5), ghép vào chuỗi rồi **lặp lại** đến khi gặp token kết thúc (EOS) hoặc đạt `max_tokens`.

Nói gọn: **Generation = vòng lặp "lấy chuỗi hiện tại → dự đoán token kế → nối vào → lặp lại".** Hệ quả: **cùng một prompt, model có thể trả lời khác nhau** mỗi lần chạy — không ổn định như chương trình thường.

> **Tóm gọn 1 câu:** Inference là một lần model "chạy" để sinh văn bản — bằng vòng lặp dự đoán từng token và nối lại, nên kết quả có thể không giống nhau giữa các lần.

---

## 5. Temperature, Top-P, Max Tokens

Model không chỉ có "prompt" — còn có **các tham số điều khiển** cách nó chọn từ. Ba tham số quan trọng nhất:

| Tham số | Nó làm gì? | Giá trị thấp | Giá trị cao | Dùng khi nào |
|---|---|---|---|---|
| **Temperature** | Mức độ "sáng tạo"/ngẫu nhiên khi chọn token | 0–0.3: chắc chắn, lặp lại, dễ đoán | 0.8–1.5: đa dạng, sáng tạo, dễ "lạc đề" | Thấp cho giải thích/kết luận; cao cho viết văn/brainstorm |
| **Top-P (nucleus)** | Chỉ chọn từ trong nhóm từ có tổng xác suất ≤ P | Thấp: hẹp và "chắc" | Cao: mở rộng vùng xét, linh hoạt | Thấp khi cần kết quả nghiêm túc |
| **Max Tokens** | Trần số token tối đa được sinh ra | Ngắn cho câu trả lời ngắn | Dài cho báo cáo/code | Đặt vừa đủ để tiết kiệm chi phí |

*Cách đọc bảng: Temperature và Top-P cùng kiểm soát "độ liều" của output; Max Tokens chỉ chặn độ dài, không đổi tính chất nội dung.*

### Mối quan hệ dễ nhầm

- **Temperature vs Top-P:** cùng quản "độ random", nhưng Temperature theo *độ*, Top-P theo *tập token được xét* — nhiều nơi khuyên **chỉ tinh chỉnh một trong hai**, không cả hai.
- **Max Tokens là "phanh khẩn cấp":** prompt dài có thể khiến model hết quyền sinh giữa chừng — hãy cấp đủ và theo dõi.

> **Tóm gọn 1 câu:** Temperature và Top-P cùng điều khiển độ "sáng tạo/liều lĩnh" của câu trả lời, còn Max Tokens là giới hạn độ dài — thấp thì ổn định, cao thì phong phú nhưng khó đoán.

---

## 6. Chain-of-Thought (CoT)

### Ý tưởng: "nghĩ ra tiếng" trước khi trả lời

Một bài toán ngắn:

- *Hỏi thẳng:* "Một cửa hàng có 12 quả táo, bán 5, rồi nhập thêm 9. Còn bao nhiêu?" — model trả lời ngay `16`. Có thể đúng, có thể vội vàng sai.
- *Nói nó trình bày từng bước:* "Bước 1: 12 − 5 = 7. Bước 2: 7 + 9 = 16." — kết quả **chắc chắn và dễ kiểm tra**.

**Chain-of-Thought (CoT)** = kỹ thuật **yêu cầu model suy luận từng bước, hiện ra lý luận trung gian trước khi kết luận** — thay vì nhảy thẳng tới đáp án. Khi "nghĩ ra tiếng", model thực chất *phân bổ thêm tính toán* cho bài toán khó → đúng hơn; người dùng *đọc được chuỗi suy luận* → dễ phát hiện lỗi logic giữa chừng. Có thể kết hợp **Few-shot CoT**: cho 1–2 ví dụ mẫu "Bước 1... Bước 2..." rồi bảo model làm theo.

> **Tóm gọn 1 câu:** Chain-of-Thought = bắt model *viết ra các bước suy luận* trước khi kết luận — vừa đúng hơn, vừa dễ kiểm tra lỗi hơn khi xây Agent.

---

## 7. Structured Output / JSON Mode

### Vấn đề

Agent cần model trả về **dữ liệu có cấu trúc** (JSON, bảng) để code xử lý tiếp — chứ không phải đoạn văn xuôi. Trả về văn xuôi bừa bãi thì chương trình không parse được.

### Giải pháp: Structured Output / JSON Mode

- **JSON Mode:** tham số/API cho phép đảm bảo **output luôn là JSON hợp lệ** theo schema ta khai báo.
- **Structured Output:** chặt hơn nữa — ta khai báo schema (tên field, kiểu dữ liệu) và model **chỉ được** trả về đúng schema đó.

Ví dụ: yêu cầu trích xuất thông tin đơn hàng:

```json
{ "order_id": "10234", "customer": "An", "status": "pending", "amount": 199000 }
```

### Mẹo thực tế

- Luôn khai báo schema **ngay trong System Prompt** (tên field, kiểu, ví dụ) để model làm đúng ngay lượt đầu.
- Văn xuôi, lời giải thích thì gom riêng vào một field như `summary` — còn `JSON Mode` giữ phần máy-đọc được.
- Thêm **bước validate** trong code: parse lỗi thì gửi lại lỗi cho model sửa, thay vì chấp nhận output sai.

> **Tóm gọn 1 câu:** JSON Mode / Structured Output buộc model trả về *đúng định dạng dữ liệu có cấu trúc* mà code của ta đọc được — nền tảng cho Agent làm việc với dữ liệu tự động.

---

## 8. Function Calling / Tool Calling

### Ý tưởng

LLM chỉ sinh văn bản — nhưng ta muốn model *kích hoạt code thật* (gọi API, đọc file, truy vấn DB). **Function / Tool Calling** làm việc đó theo 4 bước:

1. Ta khai báo danh sách **tools** (tên, mô tả, tham số) bằng JSON schema.
2. Khi cần, model **không tự chạy** code — chỉ **trả về một "lời gọi" có cấu trúc**: tên function + đối số.
3. Code của ta (vòng lặp Agent) **thực thi** lệnh đó, lấy kết quả thật.
4. Kết quả được gửi ngược lại cho model như một message mới → model tiếp tục suy luận.

### Vòng lặp nhỏ đó chính là nền của Agent

- Model: "Tôi cần kiểm tra đơn #10234" → trả về: `check_order(order_id="10234")`.
- Code chạy hàm → nhận `{"status": "refunded"}` → model thấy kết quả → soạn câu trả lời cuối cho khách.

> **Tóm gọn 1 câu:** Tool Calling = model *đề xuất* lời gọi hàm (tên + đối số), code của ta chạy thật rồi đưa kết quả về — chính là nhịp tim của mọi Agent.

---

## 9. Model Limitations & Hallucination

### Model có những giới hạn gì?

- **Không nhớ ngoài context window** — hết "cái bàn" là quên (Mục 2).
- **Không biết tin tức mới** nếu không được cung cấp — kiến thức thường cắt ở mốc huấn luyện cố định.
- **Không có ý chí và cảm nhận thực tế** — chỉ "tái tạo" kiến thức thống kê, và trả lời tự tin không đi kèm độ đúng.

### Hallucination — "bịa" thông tin

**Hallucination** là khi model **sinh ra thông tin sai, không có thật, nhưng trình bày rất thuyết phục.** Đó không phải lỗi hiếm — nó là *hệ quả tự nhiên* của mô hình dự đoán xác suất: model không biết "đúng/sai", chỉ biết "hợp văn phong".

Ví dụ: model khẳng định chắc nịch một API không tồn tại, hoặc bịa một trích dẫn sách.

### Cách giảm thiểu (không xóa được hoàn toàn)

- **Cấp ngữ cảnh có thật** (RAG — truy xuất tài liệu) để model "dựa" vào thay vì nhớ; yêu cầu **trích nguồn** rồi tự đối chiếu.
- **Hạ temperature** — giảm "sáng tạo bịa".
- **Kiểm chứng bằng code** — với Agent, luôn để model *gọi tool/đọc dữ liệu thật* thay vì tự nhớ; thiết kế bước xác minh của con người (human-in-the-loop) cho việc quan trọng.

> **Tóm gọn 1 câu:** LLM vừa quên ngoài context, vừa hay *"bịa tự tin"* (hallucination) — muốn giảm thiểu thì cấp ngữ liệu thật, hạ nhiệt độ và luôn kiểm chứng quan trọng trong luồng xử lý.

---

## Tóm Tắt & Checklist

### Nội dung đã học trong module này

1. **LLM** là máy dự đoán từ tiếp theo, chạy trên kiến trúc Transformer với cơ chế *self-attention*.
2. **Token** là đơn vị đo (≈ ¾ từ); **Context Window** là "cái bàn" giới hạn những gì model thấy.
3. Cuộc hội thoại gồm **System (luật) / User (yêu cầu) / Assistant (phản hồi)** — prompt engineering là sắp xếp đúng ba vai này.
4. **Inference/Generation** là vòng lặp: dự đoán từng token → nối vào → lặp lại.
5. **Temperature / Top-P / Max Tokens** điều khiển độ sáng tạo và độ dài câu trả lời.
6. **Chain-of-Thought** cho model viết ra lý luận từng bước — đúng hơn và dễ kiểm tra.
7. **Structured Output / JSON Mode** buộc model trả về dữ liệu có cấu trúc để code đọc được.
8. **Function/Tool Calling** = model đề xuất lời gọi hàm, code chạy thật — nền tảng của Agent.
9. **Hallucination** = model "bịa" tự tin — giảm thiểu bằng ngữ liệu thật + kiểm chứng.

### Checklist tự kiểm tra

Bạn đã nắm được khi có thể trả lời lưu loát các câu hỏi sau:

- [ ] Giải thích được "LLM là máy dự đoán từ tiếp theo" bằng lời bình thường?
- [ ] Nói được token là gì và vì sao Context Window có giới hạn?
- [ ] Phân biệt được System Prompt / User Prompt / Assistant Message và vai trò của từng loại?
- [ ] Kể tên 3 tham số điều khiển output và ảnh hưởng của chúng lên kết quả?
- [ ] Giải thích được Chain-of-Thought giúp model đúng hơn như thế nào?
- [ ] Giải thích được vì sao JSON Mode quan trọng với Agent?
- [ ] Nói đúng bản chất của Tool Calling: model *đề xuất*, code *chạy thật*?
- [ ] Kể được ít nhất 2 cách giảm thiểu hallucination?

---

## Tóm Gọn Toàn Module

> **Một câu để nhớ mãi:** LLM là *máy dự đoán từ tiếp theo* chạy trên Transformer — ta điều khiển nó bằng cách sắp đúng System/User/Assistant, chỉnh Temperature & Max Tokens, bắt nó nghĩ từng bước (CoT), ép đúng định dạng (JSON), trao công cụ thật (Tool Calling) — và luôn nhớ nó có thể *bịa* nên phải kiểm chứng.

**Đi tiếp:** Module 6 sẽ mở rộng tư duy này lên một bậc — *Agentic Patterns*: cách tổ chức vòng lặp suy nghĩ–hành động (reasoning–acting loops), ReAct, và các mẫu thiết kế để biến một LLM đơn lẻ thành một Agent vận hành bền bỉ thay bạn.
