# 🧭 05. Patterns — Xây Dựng Quyết Định Production

> Phần này tổng hợp **4 target workloads** và **5 production patterns** của Jev — routing/triage, classification at scale, gating agent actions, verifying LLM output (verified cascade), ranking & filtering — cùng **map-reduce**. Mỗi pattern gồm mô tả, khái niệm card, code mẫu, và bảng lưu ý. Đọc [README.md](../README.md) trước để có bối cảnh tổng quan Module XIV.

> **Cách đọc phần này:** *pattern* = kiểu mẫu lắp ghép lặp lại được; *routing/triage* = phân loại rồi điều hướng; *gating* = chặn/cho qua qua một cổng kiểm tra; *verified cascade* = kiểm tra đầu ra của LLM trước khi dùng; *ranking & filtering* = xếp hạng và lọc; *map-reduce* = xử lý từng bản ghi riêng rẽ rồi gộp kết quả; *workload* = dạng khối lượng công việc.

---

## 1. Tổng Quan

Phần này định hình toàn bộ chương: pattern là gì, có bao nhiêu cái, và quy trình chung mà tất cả đều đi qua.

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Patterns ở đây là **các hình thức lắp ghép Jev vào pipeline thật** — mỗi pattern ánh xạ một loại quyết định lặp lại (route, classify, gate, verify, rank) sang primitives của Jev (Choice / Score / Noul), luôn kèm theo **threshold band** quyết định auto-act hay escalate.
> **Ẩn dụ/so sánh:** Giống **bộ công cụ của thợ mộc** — Jev là cái máy cưa (một năng lực duy nhất: cắt quyết định nhanh và chính xác), còn 5 patterns là các **cách lắp máy** vào từng việc: cưa đường thẳng (classify), chặn an toàn (gate), so phẳng (verify)... Cùng một máy, nhiều jig.
> **Vì sao quan trọng:** Biết pattern = biết **đặt câu hỏi nào, primitive nào, ngưỡng nào** cho từng bài toán — thay vì bịa API call mỗi lần. Rule chung: **"Jev decides, code acts, LLM writes."**

Giải nghĩa: **primitive** = một trong ba kiểu câu hỏi của Jev (Choice / Score / Noul); **jig** (trong ẩn dụ) = đồ gá — dụng cụ giữ vật để máy làm đúng việc; **threshold band** = dải ngưỡng quyết định tự làm hay chuyển người.

### 1.1 Bảng 4 Workloads × 5 Patterns

Cách đọc bảng này: cột **#** là số thứ tự workload (dạng khối lượng công việc); cột **Target workload** là loại việc thật trong production; cột **Patterns tương ứng** chỉ ra pattern nào xử lý được việc đó; cột **Primitive thường dùng** là kiểu câu hỏi nên dùng. Ví dụ, hàng 1 nghĩa là: nếu bạn có bước quyết định trong workflow, dùng routing/triage hoặc gating, với câu hỏi kiểu Choice (chọn một) hoặc Noul (có/không).

| # | Target workload | Patterns tương ứng | Primitive thường dùng |
|---|-----------------|--------------------|-----------------------|
| 1 | **Decision steps trong workflows** | Routing/Triage · Gating | Choice · Noul |
| 2 | **Map-reduce over datasets** | Classification at scale · Ranking & Filtering | Choice · Score |
| 3 | **Real-time apps** | Routing (latency-critical) | Choice · Noul (70–500ms) |
| 4 | **Verification of LLM output** | Verified Cascade (verify) | Noul · Score |

> **Tóm gọn 1 câu:** Bảng trên nối mỗi loại việc thật với pattern và kiểu câu hỏi phù hợp — đọc hàng khớp bài toán của bạn trước, rồi đi tới mục pattern đó.

### 1.2 Workflow Chung Của Mọi Pattern

Phần này vẽ quy trình chung mà cả năm pattern đều đi qua — học một lần, áp dụng cho mọi pattern.

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

Cách đọc khối trên: trái sang phải — thu thập state (nhỏ, chỉ dữ liệu liên quan) → Jev quyết trong 70–500ms → đọc đáp án + xác suất + độ tự tin → so với ngưỡng của từng câu hỏi → rẽ vào ba band (HIGH = code tự làm, MEDIUM = hỏi xác nhận, LOW = chuyển người); LLM chỉ được gọi ở cuối nếu cần sinh văn bản.

**Nhắc lại về độ trễ và chi phí**: mỗi quyết định mất 70–500ms; giá $0.042 cho 1M input tokens, output miễn phí; thêm câu hỏi gần như không làm tăng độ trễ (vì chạy song song trong một lượt). Chính nhờ rẻ và nhanh mà các pattern phân loại ở quy mô lớn mới khả thi.

> **Tóm gọn 1 câu:** Mọi pattern đi cùng một quy trình: state → Jev quyết → đọc phân phối → so ngược → ba band; LLM chỉ vào cuộc khi cần văn bản.

---

## 2. Routing & Triage

Phần này mô tả pattern phổ biến nhất: phân một mục (ticket, tin nhắn) vào đúng nhóm và mức ưu tiên.

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Routing/Triage = phân một item (ticket, message, request) vào **một trong các channel/queue/team/priority** đã biết trước. Gọi Jev với 1 **Choice** (team/queue) + 1 **Score** (priority) cho mỗi item.
> **Ẩn dụ/so sánh:** Giống **lễ tân bệnh viện** — nhìn bệnh nhân, phân loại vào khoa (Choice) và mức khẩn (Score: cấp cứu / khẩn / thường) trong vài trăm mili-giây, rồi hành động. Lễ tân không cần viết gì, chỉ cần **chọn đúng ô**.
> **Vì sao quan trọng:** Đây là pattern phổ biến nhất và dễ khởi động nhất — mỗi ticket một lượt decide, độ trễ mạng cộng thêm vẫn giữ tổng dưới ~500ms, đủ cho real-time inbox.

Giải nghĩa: **item** = một đơn vị công việc (ticket, tin nhắn, yêu cầu); **queue/channel** = hàng đợi hoặc kênh xử lý (ví dụ nhóm billing, nhóm kỹ thuật); **real-time inbox** = hộp thư xử lý ngay khi nhận.

> **Tóm gọn 1 câu:** Routing/Triage = lễ tân bệnh viện phiên bản máy: một câu chọn khoa, một câu chấm mức khẩn, xong trong dưới nửa giây.

### 2.1 Ví Dụ: Support Ticket → Team / Queue / Priority

Phần này vẽ luồng cụ thể cho một ticket hỗ trợ: hai câu hỏi, ba nhánh band.

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

Cách đọc khối trên: văn bản ticket → Jev trả hai đáp án — `queue` (chọn 1 trong 4 nhóm: billing/tech/sales/churn, kèm xác suất) và `priority` (chấm 4 mức p0–p3, điểm có thể lọt giữa hai mức); sau đó rẽ theo band: tự chuyển, gợi ý cho agent xác nhận, hoặc chuyển người phân loại.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/01-2-1-vi-du-support-ticket-team-queue.py`](examples/01-2-1-vi-du-support-ticket-team-queue.py)

</details>

> **Tóm gọn 1 câu:** Một ticket → hai câu hỏi (nhóm + ưu tiên) → ba nhánh theo band — code mẫu ở trên chạy được nguyên luồng này.

### 2.2 Lưu Ý

Cách đọc bảng này: cột **Điểm** là khía cạnh cần chú ý (kiểu câu hỏi, ngưỡng, độ trễ…); cột **Guidance** là khuyến nghị cụ thể. Ví dụ, hàng `Distribution` nghĩa là: luôn đọc trường `probabilities` — nếu hai nhóm gần hòa nhau (0.35/0.33) thì escalate, bất kể nhãn trả về là gì.

| Điểm | Guidance |
|------|----------|
| Primitive | 1 Choice (queue) + 1 Score (priority) — thêm questions không đáng kể latency |
| Threshold | Queue: auto-route ≥ 0.8 · Priority: ≥ 0.7 · dưới đó confirm |
| Latency | Jev 70–500ms + network → vẫn thoải mái cho inbox real-time |
| State hygiene | Gửi **phần ticket liên quan** (subject + body đã cắt), đừng gửi toàn bộ history thread |
| Distribution | Đọc `probabilities` — nếu queue near-tie (0.35/0.33) → escalate bất kể label |

> **Tóm gọn 1 câu:** Năm lưu ý của routing: đúng primitive, ngưỡng 0.8/0.7, gửi ít dữ liệu liên quan thôi, và luôn soi phân phối để bắt gần hòa.

---

## 3. Classification & Tagging Ở Scale

Phần này nói về việc phân loại **toàn bộ** dataset — hàng nghìn tới hàng triệu bản ghi — và vì sao nó khả thi về giá.

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Chạy classification trên **mọi record/row** trong dataset vì chi phí quá rẻ ($0.042/1M input tokens, free output) và mọi câu evaluate **parallel trong một pass**. Output là label sẵn nằm trong schema — không cần parse text, không cần cleanup.
> **Ẩn dụ/so sánh:** Giống **máy phân loại thư công nghiệp** — mỗi lá thư đi qua trong vài chục mili-giây, gắn nhãn sẵn, không cần người đọc. Lợi thế xuất hiện khi **số lượng lớn**: map từng record, reduce gộp lại.
> **Vì sao quan trọng:** LLM cho việc này vừa đắt vừa chậm, lại còn phải parse text; Jev trả label typed ngay, kết hợp được với **map-reduce** để xử lý dataset lớn trong khi latency luôn tính theo **per-decision** (không tăng theo số record).

Giải nghĩa: **record/row** = một dòng/bản ghi trong dữ liệu; **parse text** = bóc giá trị từ văn bản tự do bằng regex/viết tay — Jev không cần bước này; **typed label** = nhãn nằm sẵn trong kiểu dữ liệu đã khai báo.

> **Tóm gọn 1 câu:** Phân loại ở scale khả thi vì rẻ ($0.042/M token, output miễn phí) và trả nhãn có kiểu ngay — không parse, không dọn text.

### 3.1 Kết Hợp Với Map-Reduce

Phần này vẽ cách chia công việc: bước map xử lý từng bản ghi riêng rẽ, bước reduce gộp kết quả lại.

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

Cách đọc khối trên: trên — dataset N bản ghi, mỗi bản ghi gửi đi riêng với state riêng và nhận nhãn + xác suất; dưới — bước REDUCE gộp lại: bỏ phiếu theo nhóm độ tự tin (majority vote = đếm nhiều ý nhất thắng), tính thống kê (xác suất trung bình từng lớp), và đẩy các bản ghi tự tin thấp sang hàng chờ xem lại.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/02-3-1-ket-hop-voi-map-reduce.py`](examples/02-3-1-ket-hop-voi-map-reduce.py)

</details>

> **Tóm gọn 1 câu:** Map = mỗi bản ghi một lượt gọi chạy song song; Reduce = gộp nhãn, bỏ phiếu theo độ tự tin, và chuyển bản ghi mờ hồ sang hàng xem lại.

### 3.2 Lưu Ý

Cách đọc bảng này: cột **Điểm** là khía cạnh (primitive, quy mô, chi phí…); cột **Guidance** là khuyến nghị. Ví dụ, hàng `Scale` nghĩa là: thêm bản ghi chỉ làm tăng chi phí token theo đường thẳng — thời gian chờ cho một quyết định không hề tăng.

| Điểm | Guidance |
|------|----------|
| Primitive | Choice (labels) hoặc Score (ordered severity) |
| Scale | Thêm records → tăng token cost linear, **không** tăng per-decision latency |
| Combine | MAP per-record → REDUCE gộp; record low-confidence đi queue review |
| Threshold | Auto-tag ≥ 0.8; dưới đó vào `needs_review` |
| Cost | $0.042/1M input → 100k records với state ngắn vẫn rất rẻ |

> **Tóm gọn 1 câu:** Năm lưu ý của classification ở scale: Choice hoặc Score, chi phí tăng tuyến tính, map-reduce gộp kết quả, auto-tag ở 0.8, và giá không phải rào cản.

---

## 4. Gating Agent Actions

Phần này nói về cách đặt "cửa an toàn" trước những hành động của agent có thể gây hại.

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Gating = đặt một **cánh cửa Noul trước tool call phá hoại** — Jev trả P(yes) cho câu "hành động này có được phép / an toàn theo policy không", code block call nếu confidence dưới threshold hoặc P(yes) thấp. Liên hệ trực tiếp với **LangChain AutoModeMiddleware**.
> **Ẩn dụ/so sánh:** Giống **khóa cửa an toàn trước phòng máy chủ** — người tới (agent) phải quẹt thẻ (Noul check) trước khi bước vào. Quẹt thẻ không đảm bảo họ là người tốt, nhưng **không quẹt thì ai cũng vào được**.
> **Vì sao quan trọng:** Agent autonomous càng cao, số tool call có side-effect (xoá file, gọi API, charge) càng nhiều. Một gate millisecond-level rẻ hơn nhiều so với một sự cố. Tuy nhiên: **Jev không đánh giá an toàn tuyệt đối** — nó phân loại theo schema bạn cung cấp, không phải là security oracle.

Giải nghĩa: **side-effect** = tác dụng phụ — hành động làm thay đổi thế giới thật (xoá file, tính tiền, gửi mail) chứ không chỉ đọc dữ liệu; **security oracle** = "thần phán an toàn" — nguồn phán xét đúng tuyệt đối (Jev không phải cái đó); **agent autonomous** = agent tự hành động ít cần người duyệt.

> **Tóm gọn 1 câu:** Gating = quẹt thẻ trước phòng máy chủ: một câu có/không trước tool call gây hại, rẻ hơn mọi sự cố — nhưng nó là phân loại, không phải phán xét an toàn tuyệt đối.

### 4.1 Ví Dụ: Gate Trước Khi Gọi Tool Phá Hoại

Phần này vẽ luồng chặn cụ thể: agent muốn xóa file, gate hỏi có/không, rồi rẽ cho/chặn.

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

Cách đọc khối trên: agent đề xuất gọi `delete_file(path="/prod/data/users.csv")`; gate hỏi "người dùng có cho phép xoá file này không, theo ngữ cảnh hội thoại?" bằng câu có/không (Noul); nếu p_yes và confidence đều cao → cho chạy; thấp → chặn và hỏi người (Human-in-the-loop = có người duyệt trong vòng xử lý).

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/03-4-1-vi-du-gate-truoc-khi-goi.py`](examples/03-4-1-vi-du-gate-truoc-khi-goi.py)

</details>

> **Tóm gọn 1 câu:** Mọi tool phá hoại đi qua một câu có/không: p và độ chắc chắn đủ cao thì chạy, không thì chặn và hỏi người.

### 4.2 Lưu Ý

Cách đọc bảng này: cột **Điểm** là khía cạnh (primitive, ngưỡng, hạn chế…); cột **Guidance** là khuyến nghị. Ví dụ, hàng `Caveat` nghĩa là: Jev phân loại theo văn bản chính sách bạn đưa vào — nó không kiểm tra logic nền tảng, nên classification ≠ chứng minh an toàn.

| Điểm | Guidance |
|------|----------|
| Primitive | **Noul** — yes/no authorize; confidence = \|p−0.5\|×2 |
| Threshold | p_yes ≥ ~0.6 **và** confidence ≥ 0.5 (starting point — tune từ labelled data) |
| Caveat | Jev **không** phải security judgment tuyệt đối — nó phân loại theo policy text bạn cho, không audit logic nền tảng (MITRE-ish: classification ≠ safety proof) |
| Liên hệ | LangChain **AutoModeMiddleware** — wrap risky tool calls |
| Fallback | Block → hiển thị context đầy đủ cho human approve/deny |

> **Tóm gọn 1 câu:** Năm lưu ý của gating: dùng Noul, hai điều kiện cùng lúc (p ≥ 0.6 và confidence ≥ 0.5), không coi là security oracle, nối với AutoModeMiddleware, và khi chặn thì đưa toàn bộ ngữ cảnh cho người quyết.

---

## 5. Verify LLM Output (Verified Cascade)

Phần này mô tả pattern kiểm tra đầu ra của LLM: LLM viết trước, Jev soát sau — rẻ để chạy thường xuyên.

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Verified Cascade = **LLM draft trước, Jev check sau** — LLM sinh nội dung, Jev (Noul/Score) đánh giá draft có *grounded theo policy text* không, pass thì dùng còn fail thì fallback/regenerate. Jev ở đây là **người soát bài nhanh**, không phải người viết.
> **Ẩn dụ/so sánh:** Giống **biên tập viên duyệt bản thảo của phóng viên** — phóng viên viết (LLM), biên tập viên đọc và chấm "đạt/không đạt" theo cẩm nang (Jev), không đạt thì trả lại viết lại. Biên tập viên không viết bài thay — chỉ **phán**.
> **Vì sao quan trọng:** Đây là pattern gắn với **4th target workload** (verification of LLM output) và là cách rẻ nhất để thêm kiểm soát chất lượng: mỗi lần verify là 70–500ms và gần như free token output — chạy được trong harness/loop với tần suất cao.

Giải nghĩa: **draft** = bản nháp LLM vừa sinh ra; **grounded** = có căn cứ — nội dung bám đúng văn bản chính sách/tài liệu đưa vào state; **harness** = khung điều phối chạy agent (xem thư mục `harness/`); **loop** = vòng lặp agent tự chạy nhiều bước; **fallback/regenerate** = phương án dự phòng hoặc yêu cầu viết lại.

> **Tóm gọn 1 câu:** Verified Cascade = biên tập viên duyệt bản thảo: LLM viết, Jev chấm "đạt/không đạt" theo chính sách trong 70–500ms, không đạt thì viết lại hoặc chuyển người.

### 5.1 Chuỗi Verified Cascade

Phần này vẽ chuỗi đầy đủ: draft → check → ba nhánh kết quả.

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

> 📄 **Code ví dụ:** [`examples/04-5-1-chuoi-verified-cascade.py`](examples/04-5-1-chuoi-verified-cascade.py)

</details>

> **Tóm gọn 1 câu:** Chuỗi cascade: draft → Jev chấm grounded → ba nhánh (dùng / hỏi người / viết lại hoặc chuyển người) — mỗi vòng kiểm chỉ tốn vài trăm ms.

### 5.2 Ứng Dụng Trong Harness / Loop

Cách đọc bảng này: cột **Nơi** là vị trí áp dụng trong hệ thống; cột **Vai trò verified cascade** là việc Jev kiểm tra ở đó. Ví dụ, hàng **CI** nghĩa là: trước khi merge, Jev kiểm tra commit message/changelog có bám đúng các thay đổi (diff) không.

| Nơi | Vai trò verified cascade |
|-----|--------------------------|
| **Harness** | Sau mỗi tool result / mỗi artifact: Jev check pass/fail trước khi tới bước sau ([harness](../../harness/)) |
| **Loop** | Verifier sub-agent dùng Jev cho **fast pre-screen** (Jev pass → tests đầy đủ; Jev fail → reject sớm) ([loop/01-concepts](../../loop/01-concepts/)) |
| **CI** | Check commit message / changelog có grounded với diff không, trước khi merge |

> **Tóm gọn 1 câu:** Ba chỗ đặt verified cascade: trong harness sau mỗi kết quả công cụ, trong loop làm màn soát nhanh trước test đầy đủ, và trong CI trước khi merge.

### 5.3 Lưu Ý

Cách đọc bảng này: cột **Điểm** là khía cạnh (primitive, ngưỡng, hạn chế…); cột **Guidance** là khuyến nghị. Ví dụ, hàng `Caveat` nghĩa là: Jev chấm theo chính sách bạn nhét vào state — chính sách mơ hồ thì kết quả kiểm tra cũng mơ hồ, nên chất lượng state quyết định chất lượng verify.

| Điểm | Guidance |
|------|----------|
| Primitive | Noul (grounded?) + Score (severity nếu fail) |
| Threshold | p_yes ≥ 0.7 + confidence ≥ 0.5 — **hoặc** dùng Score severity = none để pass |
| Caveat | Jev check theo **policy text trong state** — policy mơ hồ → verify mơ hồ. State hygiene quyết định chất lượng verify |
| Anti-pattern | Đòi Jev "giải thích tại sao draft sai" — nó chỉ trả score/probability |

> **Tóm gọn 1 câu:** Noul + Score là bộ đôi verify; ngưỡng gợi ý p ≥ 0.7 và confidence ≥ 0.5; và đừng đòi Jev giải thích — giải thích là việc của LLM.

---

## 6. Ranking & Filtering

Phần này mô tả pattern xếp hạng: dùng điểm số liên tục để sắp thứ tự và lọc bỏ phần kém.

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Ranking & Filtering = dùng **Score** (ordered levels) để chấm điểm từng candidate rồi **sort**, hoặc filter bỏ candidate dưới ngưỡng. Probability-weighted score có thể **ngồi giữa 2 level** — liên tục hơn label cứng, tốt cho so sánh thứ hạng.
> **Ẩn dụ/so sánh:** Giống **ban giám khảo chấm thi với rubric 4 mức** — mỗi bài được đặt vào mức (hoặc giữa 2 mức do weighted), rồi xếp hạng theo điểm. Không cần viết lời bình, chỉ cần **điểm + thứ tự**.
> **Vì sao quan trọng:** Đặc biệt mạnh trong **RAG pipeline**: sau retriever trả 20 đoạn, Jev re-rank shortlist theo relevance levels trong vài trăm ms/đoạn — kết hợp được map-reduce và rẻ hơn LLM re-rankers.

Giải nghĩa: **candidate** = ứng viên — đoạn văn/record đang được chấm; **re-rank** = xếp hạng lại; **retriever** = bộ truy xuất lấy đoạn văn từ nguồn dữ liệu; **shortlist** = danh sách rút gọn; **relevance levels** = các mức độ liên quan có thứ tự.

> **Tóm gọn 1 câu:** Ranking = ban giám khảo chấm thi: Score chấm từng ứng viên, sort giảm dần, lọc dưới ngưỡng — điểm liên tục phân biệt được 3.4 với 3.1.

### 6.1 Score Levels Cho Re-Ranking

Phần này vẽ luồng chấm điểm và sắp xếp cho danh sách ứng viên từ retriever.

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

Cách đọc khối trên: trên — mỗi ứng viên được chấm song song, nhận điểm (3.4, 1.8, 3.1 — có thể lọt giữa hai mức vì là trung bình có trọng số) và độ tự tin; dưới — sort giảm dần theo điểm, lọc bỏ điểm dưới ngưỡng, ứng viên điểm cao nhưng độ tự tin thấp thì giữ lại nhưng đánh dấu cần xem lại.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/05-6-1-score-levels-cho-re-ranking.py`](examples/05-6-1-score-levels-cho-re-ranking.py)

</details>

> **Tóm gọn 1 câu:** Chấm từng ứng viên song song bằng Score, sort theo điểm, lọc dưới ngưỡng — và ứng viên điểm cao mà độ tự tin thấp phải được đánh dấu.

### 6.2 Lưu Ý

Cách đọc bảng này: cột **Điểm** là khía cạnh (primitive, kết hợp, RAG, hạn chế); cột **Guidance** là khuyến nghị. Ví dụ, hàng `Caveat` nghĩa là: sort theo điểm, nhưng khi độ tự tin thấp thì thứ hạng dễ trượt sai — phải cảnh báo người đọc.

| Điểm | Guidance |
|------|----------|
| Primitive | Score (ordered levels) — weighted score liên tục để sort |
| Combine | Filter (score < t) + sort (desc) + low-confidence flags |
| RAG | Jev re-rank → LLM chỉ nhận top-K passage → rẻ hơn, context gọn hơn |
| Caveat | Sort theo **score**, nhưng cảnh báo khi confidence thấp — candidate score cao conf thấp có thể trượt thứ hạng sai |

> **Tóm gọn 1 câu:** Bốn lưu ý của ranking: dùng Score liên tục để sort, kết hợp filter + sort + đánh dấu, ưu tiên cho RAG để rẻ và gọn context, và cảnh báo candidate tự tin thấp.

---

## 7. Map-Reduce Cuối Cùng

Phần này tổng quát hóa pattern map-reduce đã thấy ở §3 — khung chung để quét cả dataset.

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Map-reduce pattern tổng quát: **mỗi record một decision (map)**, sau đó **gộp kết quả (reduce)** — vote theo bucket confidence, aggregate xác suất, hoặc chuyển low-confidence sang hàng đợi review. **Latency luôn tính theo per-decision** (70–500ms), không tăng theo số record.
> **Ẩn dụ/so sánh:** Giống **đội công chứng viên** — mỗi người xử lý một tập hồ sơ song song (map), trưởng nhóm ký tổng hợp (reduce). Thêm công chứng viên không làm mỗi hồ sơ chậm lại.
> **Vì sao quan trọng:** Đây là lý do Jev fit **workload #2 (map-reduce over datasets)**: chi phí $0.042/1M input + free output + parallel-in-one-pass nội bộ cho nhiều questions → quét toàn bộ dataset là chuyện bình thường.

Giải nghĩa: **aggregate** = tổng hợp (tính %, trung bình); **wall-clock** = thời gian thực đo đồng hồ, phụ thuộc bạn chạy song song bao nhiêu luồng.

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

Cách đọc khối trên: bước MAP — mỗi bản ghi chạy song song, trả nhãn + xác suất + độ tự tin; bước REDUCE — chia bucket theo độ tự tin (tự làm / hàng xem lại / escalate), tổng hợp số liệu (% mỗi lớp, xác suất trung bình, so với mốc ban đầu để phát hiện trôi), và ghi log đủ để audit nhưng không ghi state.

| Thành phần | Quyết định |
|-----------|------------|
| **Map** | state nhỏ/record · questions tối giản · async batch (xem §3) |
| **Reduce** | bucket theo confidence · majority/weighted vote · enqueue review |
| **Latency** | per-decision 70–500ms — tổng wall-clock phụ thuộc batch concurrency |
| **Cost** | $0.042/1M input, free output — scale N record không nổ budget |
| **Eval** | log probs ↔ outcome để tính calibration trên dataset thật |

Cách đọc bảng trên: cột **Thành phần** là bộ phận của pattern; cột **Quyết định** là lựa chọn thiết kế cho bộ phận đó. Ví dụ, hàng **Reduce** nghĩa là: ở bước gộp, hãy chia nhóm theo độ tự tin, bỏ phiếu theo đa số hoặc trọng số, và đẩy phần mờ hồ vào hàng đợi xem lại (enqueue review = thêm vào hàng đợi).

> **Tóm gọn 1 câu:** Map-reduce tổng quát: mỗi bản ghi một quyết định song song, rồi gộp theo độ tự tin — thêm bản ghi không làm quyết định nào chậm đi.

---

> *"Jev decides, code acts, LLM writes — mọi pattern production đều là một biến thể của câu này."*

---

*Trở về [README](../README.md) — tổng quan Module XIV*

*Tiếp theo: [06 — Jev + LLM: Phân Chia Lao Động](../06-jev-and-llm/) →*

*Trước đó: [04 — Calibration: Xác Suất Thành Thật](../04-calibration/)*
