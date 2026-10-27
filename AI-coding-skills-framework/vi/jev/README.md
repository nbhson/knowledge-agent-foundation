# ⚡ XIV. Jev & System One Models

> ## 📑 Mục Lục
>
> - [Câu Chuyện Mở Đầu](#câu-chuyện-mở-đầu)
> - [Tại Sao Jev & System One Models Quan Trọng?](#tại-sao-jev--system-one-models-quan-trọng)
> - [Tổng Quan](#tổng-quan)
> - [Lộ Trình Học (Cấu Trúc Thư Mục)](#lộ-trình-học-cấu-trúc-thư-mục)
> - [Case Studies Thực Tế](#case-studies-thực-tế)
> - [Tài Liệu Tham Khảo](#tài-liệu-tham-khảo)

---

### Câu Chuyện Mở Đầu

Cứ tưởng tượng thế này cho dễ: bạn bị trầy xước đầu gối sơ sơ, mà lại gọi nguyên **ê-kíp mổ cấp cứu** — nào là bác sĩ gây mê, bác sĩ chính, y tá, xe cấp cứu — chỉ để... dán một miếng băng cá nhân. Hay bạn mời hẳn một **đầu bếp Michelin** về chỉ để **đun hộ ấm nước sôi**. Về lý thuyết thì vẫn xong việc — nhưng đúng là vừa tốn kém vừa lãng phí.

Mà trớ trêu là hàng nghìn hệ thống AI bây giờ cũng đang làm y chang vậy: mỗi lần agent chỉ cần **xếp loại một cái ticket**, **kiểm tra một điều kiện cho qua hay không**, hay **chấm điểm một câu trả lời** — là lại lôi hẳn một **LLM frontier** ra. Con mô hình viết tràng giang 500 tokens văn xuôi chỉ để trả về một danh sách JSON, rồi regex parse trật hết 5% số lần. Vừa đắt, vừa chờ vài giây mới xong, mà độ chắc chắn thì... hên xui.

Nhất là khi agent của bạn chạy **hàng nghìn lần mỗi giờ** mà chỉ cần biết *"quyết định này là gì, chắc chắn tới đâu"* — thì chuyện **bắt nó sinh cả đoạn văn đúng là tốn quá**. Lúc này bạn không cần một nhà văn. Bạn cần một **phản xạ kiểu hệ thần kinh** — nhanh, gọn, trúng.

> *"Frontier intelligence belongs inside function calls — unstructured state in, typed probabilistic decisions out."*
> — **TypeSafe AI, Introducing System One Models and Jev (2026)**

> *"Jev không viết gì cả. Nó chỉ quyết định — nhanh, đúng chuẩn, và kèm xác suất bạn xài được ngay."*

Nói gọn, **Jev** là mô hình đầu tiên trên thế giới thuộc lớp **System One Models** — sinh ra để lo mấy **quyết định nhỏ, nhanh, có cấu trúc** (kiểu System 1) mà phần mềm nuốt được ngay, thay vì sinh văn bản dài cho con người đọc (kiểu System 2).

### Tại Sao Jev & System One Models Quan Trọng?

> **"Don't generate a decision. Sample one."**

#### 3 Bằng Chứng Khoa Học & Thực Tiễn

| # | Nghiên Cứu / Nguồn | Phát Hiện Quan trọng |
|---|---------------------|-----------------------|
| 1 | **TypeSafe AI (2026)** | Jev nhanh hơn **40-200×** và hiệu quả hơn **~2 cấp độ magnitude** (~400× rẻ hơn) so với frontier LLMs trên các task System One-shaped |
| 2 | **TypeSafe AI (2026)** | Latency end-to-end **70-500ms** so với **3-329s** của frontier LLMs — vừa đủ nhanh cho real-time UX và high-throughput pipelines |
| 3 | **RLCD Calibration (TypeSafe, 2026)** | Nhờ Reinforcement Learning for Calibrated Decisions: **~80%** các câu trả lời được chấm điểm **0.8** là **đúng** — xác suất match thực tế, không phải self-report |

#### Triết lý cốt lõi:

```
System One Models = Decisions mà software dùng trực tiếp
                  → Nhanh + Rẻ + Calibrated
                  → Không hallucinate ngoài schema
```

**Phân biệt quan trọng:**

```
LLM    = Sinh TEXT cho con người (chat, code, có thể hallucinate)
Jev    = Trả TYPED DECISION cho phần mềm (Choice / Score / Noul + xác suất)
                          ↑
         Jev KHÔNG phải LLM: không generate text/token,
         không RLHF (human preferences) — RLCD (outcomes)

LLM + Jev = BỔ SUNG nhau, không thay thế:
         Jev decide → LLM viết (code, email, giải thích)
```

**Liên hệ với framework này cho dễ nhớ**: nếu Module XII (Loop) là *ông điều phối*, Module XIII (Graph) là *cái kho tri thức*, thì **Jev chính là tay quyết định (decision layer)** — chỗ mà Loop gọi tới để *xếp loại, gác cổng, rẽ nhánh, chấm điểm* trước khi để LLM viết (viết code, viết câu trả lời) hoặc trước khi code tự hành động. Jev giống như **người gác cổng bên trong** Harness vậy: `state → Jev → typed answer → code acts / escalate`.

**Analogies**: Kể kiểu đời thường thì **LLM giống anh thư ký viết văn rất giỏi** — giao gì cũng viết được, kể cả chuyện chỉ cần khoanh A hay B. Còn **Jev giống con chim bói cá** — đậu yên trên cành, mắt nhìn mặt nước, thấy cá là *lao xuống bắt* trong tích tắc: một cú phản xạ chuyên biệt, khỏi cần viết nguyên bài luận rồi mới quyết. Hay nói kiểu khác: **LLM như anh hướng dẫn viên kể chuyện cả ngày** (vui thì vui, mà mệt, đắt, thỉnh thoảng còn bịa); **Jev như cái đèn giao thông** — đỏ thì dừng, xanh thì đi, quyết trong mili-giây mà gần như lúc nào cũng đúng.

**Nếu bỏ qua**: Nói thẳng là bạn sẽ trả tiền frontier LLM cho từng cái ticket con con; agent cứ mỗi quyết định lại bắt chờ 3-300s; code thì phải **lấy regex đi parse JSON** mà vẫn lỗi lên lỗi xuống; và mấy con số kiểu "tự tin 90%" của LLM thực ra toàn là **tự tin ảo chưa qua kiểm chứng** — vì tụi nó được tối ưu theo sở thích con người, chứ không theo kết quả thật.

## Tổng Quan

Kể đơn giản thế này: **System One Models** là một lớp mô hình mới — **không sinh văn bản**, mà nuốt **đầu vào lộn xộn** (string / JSON / array) rồi nhả ra **quyết định có kiểu, kèm xác suất** — tức là các đáp án dạng Choice / Score / Noul, có luôn phân phối xác suất và độ tự tin, để phần mềm **cầm lấy mà chạy luôn**, khỏi cần parse.

Còn Jev là mô hình đầu tiên của TypeSafe AI — xài **transformers** được train **toàn bằng synthetic data** với món **RLCD** (Reinforcement Learning for Calibrated Decisions): xác suất của nó được rèn **theo kết quả thật**, chứ không theo kiểu "con người thích câu nào" như RLHF.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     ⚡ SYSTEM ONE MODELS — JEV                           │
│                                                                         │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │  INPUT                                                            │  │
│  │  state: string / JSON / array of text    (material để judged)     │  │
│  │  questions: named map of typed questions (Choice/Score/Noul)      │  │
│  └──────────────────────────┬────────────────────────────────────────┘  │
│                             │                                           │
│                             ▼                                           │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │  JEV MODEL (jev-1.13.0 / jev-latest)                              │  │
│  │  Transformer · Synthetic data · RLCD-calibrated                   │  │
│  │  All questions evaluated in PARALLEL, one pass                    │  │
│  │  70-500ms · $0.042/M input tokens · output free                   │  │
│  └──────────────────────────┬────────────────────────────────────────┘  │
│                             │                                           │
│                             ▼                                           │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │  TYPED ANSWERS                                                    │  │
│  │  choice: selected option + full distribution + confidence         │  │
│  │  score:  probability-weighted score + per-level probs + conf      │  │
│  │  noul:   P(yes) 0-1 · certainty là intrinsic (margin |p-0.5|·2)  │  │
│  └──────────────────────────┬────────────────────────────────────────┘  │
│                             │                                           │
│              ┌──────────────┼──────────────┬──────────────┐            │
│              ▼              ▼              ▼              ▼            │
│        ┌──────────┐  ┌────────────┐  ┌──────────┐  ┌────────────┐     │
│        │ threshold│  │ route/gate │  │ escalate │  │ LLM viết   │     │
│        │ → code   │  │ → workflow │  │ → human  │  │ (verify)   │     │
│        │ tự chạy  │  │ branch     │  │ nếu low  │  │ cascade    │     │
│        └──────────┘  └────────────┘  └──────────┘  └────────────┘     │
│                                                                         │
│  TÍCH HỢP:                                                              │
│  ┌────────────┐ ┌────────────┐ ┌──────────────┐ ┌───────────────────┐   │
│  │ REST API   │ │ SDK        │ │ LangChain    │ │ Pydantic AI       │   │
│  │ /systemone │ │ Python / JS│ │ TypeSafe     │ │ TypeSafeModel     │   │
│  └────────────┘ └────────────┘ │ Classifier   │ └───────────────────┘   │
│  ┌────────────┐ ┌────────────┐ └──────────────┘ ┌───────────────────┐   │
│  │ OpenRouter │ │ Spice AI   │                  │ Refix             │   │
│  │ /decisions │ │ (từ SQL)   │                  │                   │   │
│  └────────────┘ └────────────┘                  └───────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘
```

Điểm mấu chốt cần nhớ: vì **không gian đáp án đóng kín (closed answer space)** nên Jev **không thể bịa ra thứ nằm ngoài schema** (khỏi lo sai type, hỏng JSON). Nhưng nó **vẫn có thể chọn nhầm đáp án nằm trong schema** — đôi khi còn tự tin hẳn hoi. **Đúng kiểu dữ liệu (type safety) không có nghĩa là đúng sự thật** (xem [07-limits-and-evaluation](07-limits-and-evaluation/)).

## Lộ Trình Học (Cấu Trúc Thư Mục)

Module XIV này được chia thành **7 module nhỏ** — cách chia giống hệt bên `harness/`, `loop/`, `graph/` cho dễ theo dõi (mỗi module là một thư mục `NN-name/README.md`).

```
jev/
├── README.md                 ← BẠN ĐANG Ở ĐÂY — tổng quan + lộ trình + case studies
├── 01-concepts/              ← Jev là gì, System 1 vs 2, lịch sử, kiến trúc, khi nào dùng
├── 02-primitives/            ← Ba primitive: Choice, Score, Noul + chọn đúng primitive
├── 03-api/                   ← Endpoint, request/response, SDK, Pydantic AI, LangChain, OpenRouter
├── 04-calibration/           ← RLCD, confidence bands, cách đọc xác suất, state hygiene
├── 05-patterns/              ← 4 workload: decision steps, map-reduce, real-time, verification
├── 06-jev-and-llm            ← Phân công Jev vs LLM: cascade, verified generation, khi nào gọi ai
└── 07-limits-and-evaluation/ ← Giới hạn 64k, lỗi, non-goals, cách eval quyết định
```

> Mỗi thư mục đều có một file `README.md` riêng — đúng chuẩn như bên `harness/`, `loop/` và `graph/` thôi, mở ra là quen ngay.

### Lộ Trình Đề Xuất

```
Bước 1: Đọc README.md này để hiểu bối cảnh
   ↓
Bước 2: 01-concepts/ — nắm Jev là gì, System 1 vs 2, kiến trúc
   ↓
Bước 3: 02-primitives/ — thành thạo Choice, Score, Noul
   ↓
Bước 4: 03-api/ — gọi API + tích hợp SDK / Pydantic AI / LangChain
   ↓
Bước 5: 04-calibration/ — đọc confidence đúng cách + state hygiene
   ↓
Bước 6: 05-patterns/ + 06-jev-and-llm — 4 workload + phân công Jev/LLM
   ↓
Bước 7: 07-limits-and-evaluation/ — biết Jev không làm được gì, eval quyết định
```

| Bạn muốn... | Đọc |
|-------------|-----|
| Hiểu Jev là gì, vì sao không phải LLM | [01-concepts](01-concepts/) |
| Chọn giữa Choice / Score / Noul | [02-primitives](02-primitives/) |
| Gọi REST API / SDK / Pydantic AI / LangChain | [03-api](03-api/) |
| Đọc confidence & calibration đúng cách | [04-calibration](04-calibration/) |
| Áp dụng 4 workload production | [05-patterns](05-patterns/) |
| Phân công Jev vs LLM trong cùng pipeline | [06-jev-and-llm](06-jev-and-llm/) |
| Biết giới hạn, lỗi hay gặp, cách eval | [07-limits-and-evaluation](07-limits-and-evaluation/) |

---

## Case Studies Thực Tế

### 1. LangChain — Agent Routing với TypeSafeClassifier + AutoMode

Bên LangChain cắm Jev vào qua **`TypeSafeClassifier`** — hiểu nôm na là một bộ xếp loại xài Jev làm máy, nhận `state` + `questions` qua `.invoke()` là nhả đáp án:

```
User message ──► TypeSafeClassifier ──► {intent: "billing", risk: "low", ...}
                        │
                        ▼
              Middleware agent routing:
                intent=billing  → billing agent
                intent=tech     → support agent
              AutoModeMiddleware:
                risk=high       → CHẶN tool call rủi ro
                risk=low        → cho phép auto-execute
```

**Nói dễ hiểu**: mấy chuyện rẽ nhánh, gác cổng rủi ro vốn là việc kiểu System One — Jev trả đáp án đúng chuẩn chỉ trong 70-500ms, khỏi cần bắt LLM viết JSON rồi parse lại cho mệt.

### 2. Pydantic AI — Agent Chỉ-Quyết-Định với TypeSafeModel

Bên Pydantic AI thì cắm qua **`TypeSafeModel`**: mỗi **field trong `output_type`** coi như **một câu hỏi** dành cho Jev; `field description` chính là **câu hỏi**, còn `docstring/instructions` là **phông nền**. Con agent kiểu này chỉ lo quyết, trả về object đúng kiểu, không viết lách lan man.

### 3. OpenRouter — Một API Key Gọi Jev

Đi qua OpenRouter thì gọn lắm: `POST https://openrouter.ai/api/alpha/decisions` với model `typesafe/jev-1.13` — hoặc trỏ base URL sang rồi xài TypeSafe TS SDK như bình thường. Cách này hợp khi team bạn **đã xài OpenRouter** cho nhiều model rồi, khỏi cần thêm một key riêng cho mệt.

### 4. Verified Cascade — LLM Dùng, Jev Duyệt

Đây là kiểu xài phổ biến nhất: LLM cứ sinh output như thường (code, câu trả lời) → **Jev đứng sau kiểm lại** bằng mấy câu hỏi Noul/Choice ngay trên output đó (`is_safe`, `matches_schema`, `tone`) → qua thì cho ra, rớt thì đẩy người duyệt hoặc chạy lại. Kiểu này Jev là **anh bảo vệ có kiểm chứng**, còn LLM là **tay thợ viết**.

### 5. Spice AI — Gọi Jev Từ SQL

Spice AI chơi hẳn kiểu gọi Jev **ngay trong câu SQL** — quyết định nằm luôn trong luồng query (rẽ nhánh, chấm điểm, gắn cờ) mà khỏi phải vòng qua service layer: `state` lấy từ row, `questions` định nghĩa sẵn, đáp án đúng kiểu trả về join tiếp được luôn.

---

## Tài Liệu Tham Khảo

### Bài Viết & Nguồn

- [TypeSafe AI — Introducing System One Models and Jev](https://typesafe.ai/blog) — bài ra mắt chính thức: System One, Jev, RLCD
- [LangChain — Building a harness with Jev](https://blog.langchain.com) — TypeSafeClassifier trong agent harness + AutoModeMiddleware
- [Wikipedia — Jev (AI model)](https://en.wikipedia.org/wiki/Jev_(AI_model)) — lịch sử, kiến trúc, controversies
- [Pydantic AI Docs — TypeSafeModel](https://ai.pydantic.dev) — output_type → questions, framing, tool-call threshold
- [OpenRouter Blog — Jev on /decisions](https://openrouter.ai/blog) — alpha decisions endpoint
- [Refix — Jev explainer](https://refix.com) — explainer cho developer
- [Spice AI — Jev from SQL](https://spice.ai) — gọi Jev trong query layer

### Frameworks & Tools

- **TypeSafe Python SDK** — `pip install typesafe` — client chính thức
- **TypeSafe JavaScript SDK** — `npm install typesafe` — client chính thức
- **LangChain** — `TypeSafeClassifier` — classification / routing trong chain
- **Pydantic AI** — `TypeSafeModel` — typed decisions làm model output
- **OpenRouter** — `typesafe/jev-1.13` trên `/alpha/decisions`
- **Spice AI** — Jev Native SQL functions
- **Refix** — developer tooling quanh Jev

Chi tiết từng module: [01-concepts](01-concepts/) → [07-limits-and-evaluation](07-limits-and-evaluation/).

---

> **"An LLM gives you words. Jev gives you a decision — with the odds attached."**

> *"Every time you ask a frontier model to 'just classify this', you're paying a novelist to fill out a checkbox. System One Models are the checkbox."*

---

*Bài viết thuộc [AI Coding Skills Framework](../..) — Module XIV: Jev & System One Models*
