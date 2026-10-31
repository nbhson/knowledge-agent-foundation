# 🛡️ Guardrails — Lớp An Toàn Cho Harness Tool Calls

> ## 📑 Mục Lục
>
> - [Câu Chuyện Mở Đầu](#câu-chuyện-mở-đầu)
> - [Tại Sao Guardrails Quan Trọng?](#tại-sao-guardrails-quan-trọng)
> - [Quan Hệ Với Harness](#quan-hệ-với-harness)
> - [Tổng Quan Các Guardrails](#tổng-quan-các-guardrails)
> - [Lộ Trình Học (Cấu Trúc Thư Mục)](#lộ-trình-học-cấu-trúc-thư-mục)
> - [Case Studies Thực Tế](#case-studies-thực-tế)
> - [Tài Liệu Tham Khảo](#tài-liệu-tham-khảo)

---

### Câu Chuyện Mở Đầu

*Phần này giải thích guardrails là gì và vì sao cần thiết. Guardrails = thanh chắn an toàn đứng trước mỗi hành động của agent.*

Hãy hình dung thế này: harness của bạn đang cầm trong tay cả `write_file` (ghi file), `execute_python` (chạy code Python), `send_notification` (gửi thông báo), `sql_query` (truy vấn cơ sở dữ liệu). Chỉ cần agent hiểu sai prompt một chút là có thể gọi nhầm `write_file` vào chỗ như... `/etc/passwd` (file tài khoản nhạy cảm của Linux). Hoặc bắn `send_notification` tới cả trăm lần. Hoặc cho `execute_python` chạy lệnh xóa sạch dữ liệu.

LLM vốn không có khái niệm "lỡ tay là toi" — nó chỉ sinh text. **Guardrails là lớp kiểm soát đứng trước đó**, chặn harness làm điều không nên làm ngay trước khi hành động diễn ra.

> *"The model proposes. The guardrail disposes."*

> **Tóm gọn 1 câu:** Agent chỉ biết sinh text, không biết việc của nó có hại hay không — guardrails là lớp chặn đứng trước, kịp ngăn lệnh ghi sai chỗ hoặc chạy sai lệnh trước khi nó xảy ra.

### Tại Sao Guardrails Quan Trọng?

*Phần này liệt kê bốn việc lớp guardrails làm trong pipeline (pipeline = dây chuyền xử lý) của harness/06.*

> Trong harness/06-decide-tools-mcp — mọi tool call đều phải đi qua `GUARDRAILS CHECK`: *"Validate permission, safety, rate limit"*.

*Cách đọc bảng này: cột "Lý do" là tính năng, cột "Giải thích" là ví dụ nó ngăn được gì. Ví dụ, dòng 3: rate limiting giới hạn số lần gọi mỗi phút, chặn agent spam lệnh.*

| # | Lý do | Giải thích |
|---|-------|------------|
| 1 | **Chặn side effects** | Ngăn `write_file` vào vùng cấm, `execute_python` lệnh nguy hiểm |
| 2 | **Permission enforcement** | Tool có `requires_permission="elevated"` → cần approve |
| 3 | **Rate limiting** | `rate_limit_per_minute=60` — chặn agent gọi tool spam |
| 4 | **Output validation** | Kiểm tra output phạm quy trước khi trả vào context |

*(Chú giải: side effect = tác dụng phụ bên ngoài như ghi file hay gửi mail; `elevated` = mức quyền cao cần người duyệt (approve); output validation = soát kết quả trả về trước khi đưa vào ngữ cảnh.)*

> **Tóm gọn 1 câu:** Guardrails làm bốn việc: chặn hành động nguy hiểm, bắt duyệt người, giới hạn tần suất, và soát đầu ra — tất cả trước khi tác động xảy ra.

### Quan Hệ Với Harness

*Phần này vạch ranh giới trách nhiệm: thư mục này quản lý gì, harness quản lý gì — đọc kỹ để không đặt luật sai chỗ.*

> **Thư mục này là catalog sản phẩm, không phải policy của harness.**
> Mỗi mục bên dưới là một *thư viện cụ thể* mà bạn có thể chọn dùng. Policy **chuẩn về uỷ
> quyền và cách ly** — risk tier, payload bắt buộc cho cổng, timeout-deny (fail closed),
> luật hai-người, giao thức `PAUSED:` — thuộc sở hữu của
> [`harness/15-approval-gates`](../../harness/15-approval-gates/README.md), còn **cơ chế
> cách ly** thuộc về
> [`harness/12-sandbox-execution`](../../harness/12-sandbox-execution/README.md).
> Một thư viện guardrail *kiểm tra*; nó không quyết định cái gì được phép. Nếu bạn đang nghĩ
> ra một risk tier ở đây, nó thuộc về `15`.

*(Chú giải: policy = bộ luật vận hành; risk tier = phân loại mức rủi ro (thấp/trung/cao); timeout-deny = hết giờ chờ duyệt thì coi như từ chối; luật hai-người = việc quan trọng phải hai người gật; catalog = danh mục hàng để chọn, không phải nơi định luật.)*

*Đoạn sau là bản đồ đối chiếu: vế trái là thư viện guardrail, vế phải là module harness nó phục vụ.*

```
┌────────────────────────────────────────────────────────────┐
│  GUARDRAILS MAP VS HARNESS COMPONENTS                      │
│                                                            │
│  harness/15-approval-gates    → POLICY chuẩn + giao thức   │
│                                  PAUSED: (giữ policy)      │
│  harness/12-sandbox-execution → tier cách ly chuẩn         │
│                                                            │
│  Guardrails AI            → harness/06 (tool input/output) │
│  NeMo Guardrails (NVIDIA) → harness/07 (workflow rails)    │
│  LlamaGuard (Meta)        → harness/05 (prompt safety)     │
│  Permission/rate limit    → harness/06 (decide tools)      │
└────────────────────────────────────────────────────────────┘
```

*Đoạn dưới đây là thứ tự các bước một lệnh gọi công cụ đi qua — guardrail đứng ngay trước bước thực thi.*

```
Tool Decision Pipeline (từ harness/06):
  User Query → Intent → Tool Selector → Parameter Extractor
      → ❯ GUARDRAILS CHECK (validate permission, safety, rate limit)
      → Tool Executor → Result Processor
```

*(Chú giải: User Query = câu hỏi người dùng; Intent = nhận diện ý định; Tool Selector = chọn công cụ; Parameter Extractor = bóc tham số; Tool Executor = máy thực thi lệnh.)*

> **Tóm gọn 1 câu:** Thư viện guardrail chỉ là "đôi mắt kiểm tra" trong pipeline — còn luật cho phép hay cấm thuộc harness/15, và vùng cách ly thuộc harness/12.

## Tổng Quan Các Guardrails

*Ba thư viện ba vị trí canh gác. Chúng bổ trợ nhau chứ không thay thế nhau.*

*Cách đọc bảng này: cột "Loại" cho biết thư viện hoạt động theo kiểu gì — quy tắc (open-source) hay model AI chuyên phân loại (model-based).*

| Guardrail | Nhà phát hành | Loại | Đặc điểm nổi bật |
|-----------|--------------|------|------------------|
| **Guardrails AI** | Guardrails AI | Open-source | Validators cho input/output, can thiệp structured |
| **NeMo Guardrails** | NVIDIA | Open-source | Rails: input, dialog, retrieval, execution |
| **LlamaGuard** | Meta | Model-based | LLM classifier chuyên phát hiện prompt/response nguy hiểm |

*(Chú giải: validator = bộ kiểm tra "giá trị này hợp lệ không"; rails = đường ray — định sẵn luồng hội thoại được đi đâu; classifier = bộ phân loại trả nhãn như safe/unsafe.)*

> **Tóm gọn 1 câu:** Guardrails AI soi tham số từng tool call, NeMo quản cả luồng hội thoại, LlamaGuard phân loại nội dung — đặt chúng ở ba lớp khác nhau.

### Guardrails AI — Validate Input/Output

*Thư viện chặn tham số sai và đầu ra phạm quy. Rẻ nhất nên đặt lớp đầu tiên.*

> 📄 **Code ví dụ:** [`examples/01-guardrails-ai-validate-input-output.py`](examples/01-guardrails-ai-validate-input-output.py)

> **Tóm gọn 1 câu:** Guardrails AI = bộ luật cứng kiểm tra input/output của mỗi tool call — rẻ, nhanh, chạy mọi lượt.

### NeMo Guardrails — Rails Mô Hình Hóa Luồng

*NeMo mô hình hóa cả luồng hội thoại thành các "rails" (đường ray): khai báo cặp hỏi-đáp được phép trong file cấu hình.*

> 📄 **Code ví dụ:** [`examples/02-nemo-guardrails-rails-mo-hinh-hoa-luong.py`](examples/02-nemo-guardrails-rails-mo-hinh-hoa-luong.py)

> **Tóm gọn 1 câu:** NeMo đặt đường ray quanh cả cuộc hội thoại — chủ đề ngoài luồng khai báo là bị chặn ngay.

### LlamaGuard — Model-Based Safety Classifier

*LlamaGuard là một AI chuyên phân loại nội dung an toàn hay không (classifier = bộ phân loại).*

> 📄 **Code ví dụ:** [`examples/03-llamaguard-model-based-safety-classifier.py`](examples/03-llamaguard-model-based-safety-classifier.py)

> **Tóm gọn 1 câu:** LlamaGuard đọc nội dung và trả nhãn safe/unsafe — đắt hơn quy tắc, nhưng bắt được nội dung nguy hiểm mà quy tắc không thấy.

### Permission & Rate Limit Trong Harness (harness/06)

*Hai công tắc dựng sẵn trong harness: duyệt người và chặn spam lệnh.*

> 📄 **Code ví dụ:** [`examples/04-permission-rate-limit-trong-harness-harness-06.py`](examples/04-permission-rate-limit-trong-harness-harness-06.py)

> **Tóm gọn 1 câu:** Mỗi tool khai báo sẵn mức quyền và giới hạn tần suất — hai con số này được kiểm tra tự động trước mỗi lần gọi.

## Lộ Trình Học (Cấu Trúc Thư Mục)

*Bản đồ thư mục và thứ tự học. Chữ (TODO) nghĩa là mục còn bỏ trống.*

```
guardrails/
├── README.md            ← BẠN ĐANG Ở ĐÂY — tổng quan + lộ trình
├── 01-concepts/         ← (TODO) Validators, rails, prompt safety, permission checks
├── 02-setup/            ← (TODO) Cài Guardrails AI / NeMo / LlamaGuard
├── 03-patterns/         ← (TODO) Tool-level guard, workflow rails, PII filtering
├── 04-savings/          ← (TODO) Giảm thiểu chi phí do hành động sai
└── 05-troubleshooting/  ← (TODO) False positive, override, bypass
```

*(Chú giải: PII filtering = lọc dữ liệu cá nhân như số CMND, email; false positive = chặn oan việc làm đúng; override/bypass = cách tắt luật hoặc lách qua luật.)*

### Lộ Trình Đề Xuất

*Năm bước từ hiểu pipeline tới đủ cả các lớp chắn.*

```
Bước 1: Hiểu tool decision pipeline + guardrail position (harness/06)
   ↓
Bước 2: Cài Guardrails AI — validate tool parameters (02-setup)
   ↓
Bước 3: Thêm permission + rate limit cho ToolDefinition (03-patterns)
   ↓
Bước 4: Nâng cấp NeMo Rails cho workflow-level (03-patterns)
   ↓
Bước 5: LlamaGuard cho prompt safety (04-savings đo lường)
```

*Cách đọc bảng này: cột trái là điều bạn muốn làm, cột phải là tài liệu nên mở.*

| Bạn muốn... | Đọc |
|-------------|-----|
| Tool decision pipeline | [harness/06-decide-tools-mcp](../../harness/06-decide-tools-mcp/) |
| Permission system | [harness/08-task](../../harness/08-task/) |
| Safe automation | [harness/10-automation](../../harness/10-automation/) |
| Loop safety | [loop/03-safety](../../loop/03-safety/) |
| Loop gate (cơ học) | [tools/loop-cli](../loop-cli/) |

> **Tóm gọn 1 câu:** Lắp lớp chắn theo thứ tự từ rẻ đến đắt: hiểu pipeline → validate tham số → thêm permission/rate limit → rails hội thoại → phân loại nội dung.

## Case Studies Thực Tế

*Hai tình huống thật: chặn hư hại do tool, và kết hợp duyệt người với giới hạn tần suất.*

### 1. Chặn Tool Damage

*Tình huống: agent định ghi file vào vùng cấm — guardrail chặn trước khi lệnh thực thi.*

> 📄 **Code ví dụ:** [`examples/05-1-chan-tool-damage.py`](examples/05-1-chan-tool-damage.py)

> **Tóm gọn 1 câu:** Chặn hư hại là ứng dụng đầu tiên nên làm: allowlist đường dẫn + từ chối mọi lệnh lạ.

### 2. Rate Limit + Elevated Permission

*Tình huống: kết hợp hai công tắc — hành động nhạy cảm cần người duyệt, lệnh lặp nhiều thì chặn.*

> 📄 **Code ví dụ:** [`examples/06-2-rate-limit-elevated-permission.py`](examples/06-2-rate-limit-elevated-permission.py)

> **Tóm gọn 1 câu:** Duyệt người (elevated) và chặn spam (rate limit) bổ sung nhau — một cái chống sai phép, một cái chống lặp vô nghĩa.

## Tài Liệu Tham Khảo

*Link gốc của ba thư viện guardrail.*

- **Guardrails AI**: https://www.guardrailsai.com
- **NeMo Guardrails (NVIDIA)**: https://github.com/NVIDIA/NeMo-Guardrails
- **LlamaGuard (Meta)**: https://ai.meta.com/research/publications/llama-guard

### Liên Kết Sang Nhánh Khác

*Cách đọc: mỗi dòng là tài liệu liên quan, sau gạch ngang là lý do nên mở nó.*

- [harness/06-decide-tools-mcp](../../harness/06-decide-tools-mcp/) — Guardrails check trong pipeline
- [HARNESS_ENGINEERING.md](../../HARNESS_ENGINEERING.md) — Section 9.2 (danh sách guardrails)
- [tools/loop-cli](../loop-cli/) — `loop gate` enforce cơ học
- [tools/langchain](../langchain/) — Guardrails trong agent loops

> **Tóm gọn 1 câu:** Luật và cổng duyệt nằm ở harness/15 và harness/06; thư mục này chỉ giúp bạn chọn đúng thư viện kiểm tra.

---

> **"A harness without guardrails is a loaded weapon pointed at production."**

---

## ⚠️ Cập nhật 10/2026: Guardrails AI Hub — Thay Đổi Lớn 2026

*Phần này cập nhật thay đổi cách cài đặt Guardrails AI năm 2026 để bạn không theo hướng dẫn cũ.*

**Guardrails AI** vẫn phát triển tích cực, nhưng có 2 thay đổi quan trọng:

1. **Validators chuyển sang PyPI chuẩn (7/2026):**Validators không còn qua Guardrails Hub hosted nữa — giờ cài trực tiếp bằng `pip` (pip = trình cài package của Python; PyPI = kho package chính thức của Python). Remote inferencing đã ngừng.

> 📄 **Code ví dụ:** [`examples/07-cap-nhat-10-2026-guardrails-ai-hub-thay.py`](examples/07-cap-nhat-10-2026-guardrails-ai-hub-thay.py)

2. **PyPI 0.6.x vẫn active** — framework core vẫn dùng được. Nếu cần thay thế nhẹ hơn:

*Cách đọc bảng này: cột "Thay thế" là phương án thay, cột "Lý do" nói khi nào nên chọn nó.*

| Thay thế | Lý do | Link |
|----------|-------|------|
| **Pydantic Validators** | Nhẹ, built-in Python, không cần thêm dependency | https://docs.pydantic.dev/ |
| **NeMo Guardrails** | NVIDIA, open-source, active development | https://github.com/NVIDIA/NeMo-Guardrails |
| **Llama Guard** | Meta, model-based classifier, chạy local | https://ai.meta.com/research/llama-guard |

*(Chú giải: built-in = có sẵn trong Python; dependency = thư viện phụ thuộc phải cài thêm.)*

> **Tóm gọn 1 câu:** Từ 7/2026 validators cài thẳng qua pip thay vì Guardrails Hub — dùng bản 0.6.x vẫn ổn, hoặc chuyển sang Pydantic/NeMo/Llama Guard nếu cần phương án khác.

*Bài viết thuộc [AI Coding Skills Framework](../..) — nhánh Tools — guardrails*