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

Hãy tưởng tượng bạn bị trầy đầu gối. Bạn gọi **cả đội phẫu thuật khẩn cấp** — gây mê, bác sĩ chính, y tá, xe cấp cứu — chỉ để... dán một miếng băng cá nhân. Hoặc bạn thuê một **đầu bếp Michelin** chỉ để **đun nước sôi**. Cả hai đều *hiệu quả về mặt kỹ thuật* — và cả hai đều **hoàn toàn phí phạm**.

Đó chính xác là những gì đang diễn ra trong hàng nghìn hệ thống AI ngày nay: mỗi khi agent cần **phân loại một ticket**, **kiểm tra một điều kiện xác nhận**, hay **chấm điểm một câu trả lời** — nó gọi một **LLM frontier**. Mô hình viết 500 tokens văn xuôi để trả về một danh sách JSON mà regex parse lỗi 5% số lần. Chi phí cao, latency vài giây, và xác suất thì... ai biết được.

Khi agent của bạn chạy **hàng nghìn lần mỗi giờ** chỉ để cần *"quyết định này là gì và tự tin bao nhiêu"* — **sinh text là tốn kém**. Bạn không cần một nhà văn. Bạn cần một **hệ thần kinh phản xạ**.

> *"Frontier intelligence belongs inside function calls — unstructured state in, typed probabilistic decisions out."*
> — **TypeSafe AI, Introducing System One Models and Jev (2026)**

> *"Jev không viết gì cả. Nó chỉ quyết định — nhanh, đúng chuẩn, và với xác suất bạn dùng được ngay."*

**Jev** là mô hình đầu tiên thế giới thuộc lớp **System One Models** — được thiết kế riêng cho các **quyết định nhỏ, nhanh, có cấu trúc** (System 1) mà phần mềm tiêu thụ trực tiếp, thay vì sinh văn bản cho con người đọc (System 2).

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

**Liên hệ framework này**: Nếu Module XII (Loop) là *hệ thống điều phối* và Module XIII (Graph) là *substrate tri thức*, thì **Jev là lớp quyết định (decision layer)** — nơi một Loop gọi model để *phân loại, gate, route, score* trước khi LLM viết (viết code, viết response) hoặc trước khi code tự hành động. Jev là **internal gatekeeper** trong Harness: `state → Jev → typed answer → code acts / escalate`.

**Analogies**: **LLM là một thư ký giỏi viết văn** — bạn giao việc gì nó cũng viết được, kể cả việc chỉ cần chọn A hay B. **Jev là một con chim bói cá** — ngồi trên cành, nhìn nước, và *tung người bắt cá* trong tích tắc: một phản xạ chuyên biệt, không cần đọc thành bài luận trước khi quyết định. Hoặc: **LLM là hướng dẫn viên du lịch kể chuyện cả ngày** (mệt, đắt, đôi khi bịa); **Jev là đèn giao thông** — đỏ dừng, xanh đi, quyết định trong mili-giây với xác suất gần như luôn đúng.

**Nếu bỏ qua**: Bạn trả tiền frontier LLM cho từng classify-ticket nhỏ; agent chờ 3-300s mỗi quyết định; code phải **parse JSON bằng regex** và vẫn fail; và mọi xác suất "tự tin 90%" của LLM đều là **overconfidence không calibrated** — vì chúng được tối ưu theo human preference, không theo outcome.

## Tổng Quan

**System One Models** là lớp mô hình mới: **không sinh text**, mà nhận **state không có cấu trúc** (string / JSON / array) và trả về **typed probabilistic decisions** — các quyết định có kiểu (Choice / Score / Noul) kèm **phân phối xác suất** và **confidence**, để phần mềm **hành động trực tiếp** không cần parse.

Jev là mô hình đầu tiên của TypeSafe AI — dùng **transformers** được train **hoàn toàn trên synthetic data** với **RLCD** (Reinforcement Learning for Calibrated Decisions): xác suất được tối ưu **chống lại outcome**, không chống lại human preference (khác RLHF).

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

Điểm mấu chốt: **closed answer space** → Jev **không thể hallucinate ra ngoài schema** (không type errors, không JSON hỏng). Nhưng nó **vẫn có thể chọn sai answer nằm trong schema** — đôi khi với confidence cao. **Type safety ≠ factual correctness** (xem [07-limits-and-evaluation](07-limits-and-evaluation/)).

## Lộ Trình Học (Cấu Trúc Thư Mục)

Module XIV được chia thành **7 modules chuyên đề** — đồng nhất với convention của `harness/`, `loop/`, `graph/` (mỗi module là `NN-name/README.md`).

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

> Mỗi thư mục chứa một `README.md` — đồng nhất với convention của `harness/`, `loop/` và `graph/`.

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

LangChain tích hợp Jev qua **`TypeSafeClassifier`** — một classifier dùng Jev làm backbone, nhận `state` + `questions` qua `.invoke()`:

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

**Ý nghĩa**: routing và risk-gating là System One-shaped tasks — Jev trả typed answer trong 70-500ms, thay vì LLM sinh JSON rồi parse.

### 2. Pydantic AI — Agent Chỉ-Quyết-Định với TypeSafeModel

Pydantic AI tích hợp qua **`TypeSafeModel`**: mỗi **field của `output_type`** trở thành **một question** cho Jev; `field description` là **câu hỏi**; `docstring/instructions` là **framing**. Agent chỉ-decide trả typed object, không sinh text.

### 3. OpenRouter — Một API Key Gọi Jev

Qua OpenRouter: `POST https://openrouter.ai/api/alpha/decisions` với model `typesafe/jev-1.13` — hoặc set base URL và dùng TypeSafe TS SDK. Áp dụng khi stack của bạn **đã có OpenRouter** cho nhiều model, không muốn thêm một key riêng.

### 4. Verified Cascade — LLM Dùng, Jev Duyệt

Pattern phổ biến nhất: LLM sinh output (code, response) → **Jev verify** bằng các Noul/Choice questions trên chính output đó (`is_safe`, `matches_schema`, `tone`) → pass thì emit, fail thì escalate/retry. Jev là **gatekeeper calibrated**, LLM là **generator**.

### 5. Spice AI — Gọi Jev Từ SQL

Spice AI cho phép gọi Jev **trực tiếp từ SQL** — quyết định nằm ngay trong query pipeline (route, score, flag) mà không cần qu vòng service layer: `state` từ row, `questions` định nghĩa sẵn, typed answer trả về join tiếp.

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
