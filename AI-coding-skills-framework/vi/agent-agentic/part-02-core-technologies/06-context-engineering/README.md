# 📋 Module 6. Context Engineering

> ## 📑 Mục Lục
>
> - [Câu Chuyện Mở Đầu](#câu-chuyện-mở-đầu)
> - [1. Prompt Engineering vs Context Engineering](#1-prompt-engineering-vs-context-engineering)
> - [2. Context Window Management](#2-context-window-management)
> - [3. Context Assembly](#3-context-assembly)
> - [4. Context Compression](#4-context-compression)
> - [5. Context Retrieval](#5-context-retrieval)
> - [6. Short-term Context](#6-short-term-context)
> - [7. Long-term Context](#7-long-term-context)
> - [8. Working Context](#8-working-context)
> - [9. Context Overflow](#9-context-overflow)
> - [10. Context Isolation](#10-context-isolation)
> - [Sơ đồ: Context Flow](#sơ-đồ-context-flow)
> - [Bảng So Sánh: Ba Loại Context](#bảng-so-sánh-ba-loại-context)
> - [Tóm Tắt & Checklist](#tóm-tắt--checklist)

---

## Câu Chuyện Mở Đầu

Bạn đang nói chuyện với một trợ lý AI:

- *"Tôi đang làm dự án app giao đồ ăn."*
- *"Đang thiết kế UX cho màn hình đặt hàng."*

Rồi bạn hỏi tiếp: *"Gợi ý giúp tôi cách thiết kế nút 'Xác nhận đơn'?"*

Kết quả? Trợ lý **quên mất** bạn đang nói về app giao đồ ăn. Nó đưa gợi ý chung chung — có thể đúng, nhưng **không liên quan**, vì nó không còn nhớ bối cảnh dự án của bạn.

Đây chính là điều **Context Engineering** xử lý: không chỉ viết prompt hay, mà còn **đưa đúng thông tin nền vào đúng lúc**, đúng cách — để LLM "hiểu" bạn đang ở đâu và đang cần gì.

> **Tóm gọn 1 câu:** Prompt là câu hỏi; Context là bối cảnh — prompt hay mà thiếu context đúng thì LLM vẫn lạc lõng.

---

## 1. Prompt Engineering vs Context Engineering

Nhiều người nhầm lẫn hai khái niệm này:

- **Prompt Engineering** = viết câu lệnh tốt hơn cho LLM. Tập trung vào *từ ngữ*, *cấu trúc*, *format* của prompt.
- **Context Engineering** = thiết kế toàn bộ thông tin nền quanh prompt. Tập trung vào *nội dung* nào được bơm vào, *từ đâu*, *khi nào*, *ở dạng nào*.

So sánh trực tiếp:

| Tiêu chí | Prompt Engineering | Context Engineering |
|---|---|---|
| **Trọng tâm** | Câu lệnh (instruction) | Thông tin nền (background) |
| **Hỏi gì?** | LLM nên *làm gì*? | LLM nên *biết gì*? |
| **Thành phần** | Roles, few-shot, format | Tài liệu, lịch sử, bộ nhớ |
| **Ví dụ** | "Bạn là chuyên gia pháp lý" | Kèm hợp đồng, luật, hồ sơ vụ việc |

**Tóm lại:** Prompt là *hướng dẫn* (nói LLM làm gì); Context là *thông tin nền* (cho LLM chất liệu để làm đúng). Hai thứ bổ trợ nhau — prompt hay mà thiếu context thì "chỉ tay không có đồ", context đầy mà prompt mơ hồ thì LLM không biết dùng context thế nào.

> **Tóm gọn 1 câu:** Prompt Engineering quyết định LLM *làm gì*; Context Engineering quyết định LLM *biết gì* khi làm — prompt là chân, context là tay; cần cả hai mới làm được việc.

---

## 2. Context Window Management

Mỗi LLM có một **context window** — giới hạn số token nó có thể "nhìn thấy" trong một lần xử lý. Ví dụ phổ biến:

- **128K token** — GPT-4o, Claude 3.5 Sonnet.
- **200K token** — Claude 3.7, Gemini Advanced.
- **1M token** — Gemini 1.5 Pro (thử nghiệm).

**Context Window Management** = kỹ thuật quản lý số lượng thông tin đưa vào cửa sổ đó — vừa đủ để làm việc, vừa không thừa để tránh tốn token và tránh tràn.

### Tại sao phải "quản lý"? Không quản lý thì sao?

| Vấn đề | Hệ quả |
|---|---|
| **Tràn cửa sổ** | LLM cắt bỏ phần cũ; mất thông tin quan trọng |
| **Tốn token** | Chi phí API tăng vọt, tốc độ chậm hơn |
| **Nhiễu (noise)** | Thông tin thừa làm LLM khó suy luận đúng |

### Các chiến lược quản lý

1. **Ước lượng token trước khi gửi** — dùng bộ đếm token, không phải đếm ký tự.
2. **Ưu tiên quan trọng nhất đặt gần cuối** — vì LLM nhớ phần cuối tốt nhất.
3. **Giữ phần cần, cắt phần thừa** — không nhồi toàn bộ lịch sử; theo dõi % cửa sổ đã dùng trước mỗi lượt.

> **Tóm gọn 1 câu:** Context window là "bàn làm việc" có giới hạn của LLM — quản lý tốt là biết cái gì để lên bàn, cái gì cất đi, kẻo bàn tràn thì rơi mất đồ quý.
---

## 3. Context Assembly

**Context Assembly** = ghép nhiều nguồn thông tin lại thành một prompt hoàn chỉnh — "lắp ráp bối cảnh" cho LLM.

Thứ tự ghép phổ biến: **System prompt → Lịch sử gần đây → Tài liệu truy xuất → Câu hỏi người dùng** (đặt cuối để gần phần sinh văn bản nhất).

### Các nguồn thông tin thường được ghép:

| Nguồn | Ví dụ | Dùng khi nào |
|---|---|---|
| **User message** | Câu hỏi mới nhất | Luôn |
| **System prompt** | Vai trò, luật lệ | Luôn |
| **Lịch sử hội thoại** | Các lượt chat trước | Hội thoại nhiều lượt |
| **Bộ nhớ / tài liệu** | Docs, kết quả công cụ | Khi cần thông tin nền |

### Nguyên tắc vàng

- **Rõ ràng từng khối** — dùng nhãn để LLM phân biệt các vùng.
- **Không trùng lặp** — thông tin đưa 2 lần làm tốn token và gây nhiễu.
- **Luôn đánh dấu nguồn** — để LLM trích dẫn và tin tưởng đúng.

> **Tóm gọn 1 câu:** Context Assembly là "trộn salad" — gom các nguyên liệu thông tin, cắt gọn, bày theo thứ tự hợp lý, rồi mới phục vụ LLM một đĩa sẵn sàng suy nghĩ.

---

## 4. Context Compression

**Context Compression** = nén context dài thành bản ngắn hơn mà vẫn giữ ý quan trọng — giống nén ảnh: cỡ nhỏ hơn, nội dung vẫn nhận ra.

### Hai kiểu nén chính:

| Kiểu | Cách làm | Ưu | Nhược |
|---|---|---|---|
| **Nén trích (extractive)** | Chỉ giữ các câu quan trọng nhất, giữ nguyên văn | Không bịa, nhanh | Có thể rời rạc, mất mạch |
| **Nén tóm lược (abstractive)** | Dùng LLM viết lại thành đoạn tóm tắt mới | Gọn, có mạch | Tốn thêm 1 lần LLM; có thể mất chi tiết |

### Kỹ thuật nén phổ biến

1. **Tóm tắt hội thoại cũ** — khi chat quá dài, tóm những lượt đầu thành "Tóm tắt trước đó: ...".
2. **Trích key information** — chỉ giữ tên, số liệu, quyết định, deadline — bỏ câu chữ trang trí.
3. **Chunking + đánh giá** — chia tài liệu thành chunk, chấm điểm, giữ chunk quan trọng nhất.

> Nguyên tắc nhỏ: **giữ "kết luận", bỏ "quá trình"** — LLM cần điểm mấu chốt, không cần từng bước chi tiết của chuyện cũ.

> **Tóm gọn 1 câu:** Context Compression là "đóng gói cẩn thận" — gói nhỏ lại, giữ những gì cốt lõi, bỏ phần lặt vặt, để cửa sổ có chỗ cho thông tin mới.

---

## 5. Context Retrieval

**Context Retrieval** = tìm và lấy đúng context **phù hợp** từ bộ nhớ / tài liệu khi cần, thay vì nhồi hết vào cửa sổ — giống "ông chủ thông minh" chỉ lấy đúng hồ sơ liên quan đến câu hỏi hiện tại.

### Luồng retrieval điển hình

Câu hỏi → Chuyển thành truy vấn (query) → Tìm trong kho → Lấy top-k kết quả liên quan nhất → Đưa vào prompt cùng câu hỏi.

### Các phương pháp tìm kiếm context:

| Phương pháp | Nguyên lý | Dùng khi nào |
|---|---|---|
| **Keyword search** | Tìm theo từ khóa khớp | Từ rõ ràng, tài liệu có từ trùng |
| **Semantic search** | Tìm theo ý nghĩa (vector embedding) | Câu hỏi không khớp từ nhưng cùng ý |
| **Hybrid** | Kết hợp cả hai | Hầu hết ứng dụng thực tế |

Retrieval tốt cần 2 chữ: **đúng** (kết quả liên quan thật sự, không trùng từ ngẫu nhiên) và **đủ** (lấy đủ mảnh cần thiết để trả lời).

> Lưu ý: retrieval khác compression — compression lấy *những gì đã có* làm ngắn lại; retrieval là *đi tìm trong kho* những gì phù hợp (chi tiết RAG ở module sau).

> **Tóm gọn 1 câu:** Context Retrieval là "thủ thư": thay vì mang cả thư viện lên bàn, nó đi lôi đúng đoạn tài liệu liên quan đến câu hỏi của bạn.
---

## 6. Short-term Context

**Short-term Context** = ngữ cảnh **trong một phiên** — những gì đã xảy ra từ đầu hội thoại đến hiện tại.

Ví dụ: bạn chat với agent về "lên kế hoạch marketing", các lượt sau nhắc "chiến dịch sắp ra mắt" — agent hiểu ngay nhờ *đoạn đối thoại trước đó* nằm trong short-term context.

### Đặc điểm:

- **Phạm vi:** Một phiên — mở phiên mới là hết.
- **Nguồn:** Lịch sử lượt chat, kết quả công cụ vừa chạy.
- **Dung lượng:** Giới hạn trong context window → dễ tràn nếu phiên dài.

### Quản lý ra sao?

- Giữ các lượt gần nhất (10–20 lượt), tóm tắt phần xa hơn.
- Ưu tiên lượt mới nhất — người dùng hay điều chỉnh ý giữa chừng.

> **Tóm gọn 1 câu:** Short-term context là "trí nhớ phiên" — nó nhớ cuộc trò chuyện đang diễn ra để câu tiếp theo không đánh mất mạch, nhưng đóng phiên là trôi đi.

---

## 7. Long-term Context

**Long-term Context** = ngữ cảnh **được lưu qua nhiều phiên** — thông tin về người dùng, dự án, quyết định từ lâu vẫn sẵn sàng được gợi lại.

Ví dụ: tháng trước bạn có phiên "đặt mục tiêu công ty 2026". Hôm nay mở phiên mới hỏi agent "mục tiêu quý 1 của tôi là gì?" — agent trả lời được nhờ **long-term memory** (học chi tiết ở Module 7).

### Đặc điểm:

- **Phạm vi:** Nhiều phiên, kéo dài theo thời gian.
- **Nguồn:** Bộ nhớ lưu trữ ngoài (database, file, vector store).
- **Dung lượng:** Gần như không giới hạn — vấn đề là *lấy đúng* khi cần; độ tươi thấp, có thể cũ.

> So sánh chi tiết 3 loại context trong **Bảng So Sánh** ở cuối module.

> **Tóm gọn 1 câu:** Long-term context là "cuốn sổ ghi chép" — mở phiên mới vẫn nhớ bạn là ai, dự án nào, đã quyết định gì; chỉ khổ cái nỗi là đôi khi sổ cũ, phải kiểm tra lại.

---

## 8. Working Context

**Working Context** = ngữ cảnh **agent đang dùng để suy nghĩ và ra quyết định tại thời điểm đang hành động** — tổng hợp mọi thông tin đang "mở trên bàn làm việc" ngay lúc này.

### Đặc điểm:

- **Năng động:** Thay đổi từng bước — mỗi lần dùng công cụ xong, bàn làm việc được cập nhật.
- **Ngắn hạn:** Tồn tại trong khoảng thời gian thực hiện tác vụ; nằm trong context window — bàn quá bừa thì phải dọn.
- **Chất lượng quyết định phụ thuộc nó:** Dọn bàn tốt → suy nghĩ sạch; bàn bừa → suy luận lẫn lộn.

### Việc cần làm với working context:

1. **Giữ gọn** — chỉ giữ thứ liên quan đến mục tiêu hiện tại; việc xong thì cất khỏi bàn.
2. **Cập nhật liên tục** — ghi kết quả công cụ mới; nếu bị cắt giữa bước thì có bản ghi để tiếp tục (checkpoint).

> **Tóm gọn 1 câu:** Working context là "bàn làm việc hiện tại" của agent — mọi thứ nó đang mở để suy nghĩ; bàn càng gọn đúng thứ cần, quyết định càng chính xác.

---

## 9. Context Overflow

**Context Overflow** = khi tổng thông tin cần đưa vào **vượt quá giới hạn context window**. Người mới hay gặp: nhồi cả file dài, toàn bộ lịch sử chat, nhiều tài liệu — rồi prompt "vỡ".

Chuyện gì xảy ra?

- **Cắt giữa chừng (truncation)** — LLM/API cắt phần đầu hoặc giữa: mất thông tin quan trọng, trả lời sai.
- **"Giữa bị quên" (lost in the middle)** — LLM nhớ đầu-cuối tốt hơn giữa: thông tin nằm giữa bị bỏ quên.
- **Suy luận kém hoặc lỗi** — cửa sổ gần đầy gây nhiễu, trả lời lạc đề; vượt hẳn thì API từ chối xử lý.

Cách phòng tránh:

1. **Đếm token trước khi gửi** — không đoán mò bằng ký tự.
2. **Cắt giảm chủ động** — dùng compression, ưu tiên, chia nhỏ (chunking).
3. **Retrieval thay vì đổ hết** — chỉ lấy phần liên quan (Mục 5); theo dõi mức đầy và tự tóm tắt khi sắp tới ngưỡng.

> **Tóm gọn 1 câu:** Context Overflow là khi "bàn làm việc" bị đầy quá mức — đồ quý rơi mất, agent phải trả lời bằng những gì còn sót lại thay vì những gì đáng lẽ phải thấy.
---

## 10. Context Isolation

**Context Isolation** = giữ context của agent này **tách biệt**, không trộn với context của agent khác — rất quan trọng trong hệ multi-agent (nhiều agent chạy cùng lúc, mỗi agent chỉ "thấy" đúng ngữ cảnh của mình).

### Vì sao phải cô lập context?

| Lý do | Ví dụ thực tế |
|---|---|
| **Quyền riêng tư & bảo mật** | Agent A không được đọc hồ sơ khách hàng của Agent B |
| **Tránh nhiễu & lộ dữ liệu** | Agent xử lý hóa đơn không cần biết chat tán gẫu; hai khách hàng không tráo hồ sơ cho nhau |
| **Tin cậy & audit** | Biết chính xác agent nào dùng dữ liệu gì, khi nào |

### Các lỗi thường gặp khi không cô lập:

- **Shared buffer / global prompt:** Mọi agent dùng chung 1 kho context → nhiễu chéo, lộ dữ liệu.
- **Key trùng / session dùng chung:** Lưu context theo key không đủ riêng, hoặc một session bị nhiều agent đọc/ghi → ghi đè, mạch hội thoại lẫn lộn.

### Cách làm đúng:

1. **Phân vùng (namespacing)** — mỗi agent có vùng riêng: `<agent_id>/<session_id>/<thread_id>`.
2. **Giới hạn quyền (scoping)** — chỉ cấp cho agent những context nó được phép truy cập.
3. **Tách lịch sử** — mỗi phiên/thread có lịch sử riêng, không dùng chung.

> **Tóm gọn 1 câu:** Context Isolation là "mỗi người một gian phòng" — agent nào xài ngữ cảnh nấy, không mở cửa lẫn nhau, để khỏi nghe lén, khỏi lộn đồ và khỏi làm hỏng việc của người bên cạnh.

---

## Sơ đồ: Context Flow

Một agent hoàn chỉnh dẫn context theo dòng chảy sau — từ yêu cầu ban đầu đến lúc LLM sinh kết quả:

```
                        ┌────────────────────────────────────────────┐
                        │                NGUỒN CONTEXT               │
                        │  User  ·  Memory  ·  Docs / KB  ·  Tools   │
                        └───────────────────┬────────────────────────┘
                                            │
                                            ▼
                                ┌───────────────────────┐
                                │  5. CONTEXT RETRIEVAL │  ← tìm & lấy đúng cái cần
                                └───────────┬───────────┘
                                            │
                                            ▼
                                ┌───────────────────────┐
                                │  3. CONTEXT ASSEMBLY  │  ← ghép các nguồn thành 1 prompt
                                └───────────┬───────────┘
                                            │
                                            ▼
                                ┌───────────────────────┐
                                │  4. CONTEXT COMPRESSION│  ← nén gọn nếu vượt giới hạn
                                └───────────┬───────────┘
                                            │
                                            ▼
                                ┌───────────────────────┐
                                │ 2. CONTEXT WINDOW (LLM)│  ← cửa sổ hữu hạn: quản lý & tránh tràn
                                └───────────┬───────────┘
                                            │
                                            ▼
                                     ┌──────────────┐
                                     │     LLM      │  → Sinh ra KẾT QUẢ / HÀNH ĐỘNG
                                     └──────────────┘
```

Cách đọc sơ đồ — đi từ trên xuống:

1. **Retrieval** (Mục 5) chọn ra từ nguồn những gì liên quan.
2. **Assembly** (Mục 3) ghép chúng thành prompt thống nhất.
3. **Compression** (Mục 4) nén lại nếu vượt giới hạn → đưa vào **Context Window** (Mục 2, 9).
4. Cuối cùng **LLM** đọc tất cả và tạo kết quả.

> **Tóm gọn 1 câu:** Dòng chảy context là "lấy → ghép → nén → đưa vào đầu LLM" — làm đúng cả bốn khâu thì agent hiểu đúng và trả lời đúng.

---

## Bảng So Sánh: Short-term vs Long-term vs Working Context

| Tiêu chí | **Short-term** | **Long-term** | **Working** |
|---|---|---|---|
| **Vòng đời** | Trong 1 phiên | Qua nhiều phiên | Trong lúc thực hiện tác vụ |
| **Chứa ở đâu** | Trong prompt / cửa sổ | Bộ nhớ ngoài (DB, file, vector) | Trên "bàn làm việc" hiện tại |
| **Độ tươi** | Rất tươi (mới nhất) | Có thể cũ, cần kiểm tra | Sống động theo từng bước |
| **Dung lượng** | Giới hạn trong window | Gần như vô hạn | Giới hạn trong window |
| **Ví dụ** | "Tôi vừa nói về app giao đồ ăn" | "Anh tên Sơn, dự án ChipCart" | "Tôi đang đọc file hợp đồng + ghi chú" |
| **Mục đích chính** | Giữ mạch hội thoại | Nhớ về người & lịch sử lâu dài | Hỗ trợ quyết định ngay bây giờ |

*Cách đọc bảng: mỗi cột là một loại context — khác nhau ở vòng đời, nơi chứa và mục đích; ba loại cùng hoạt động song song trong một agent.*

> **Tóm gọn 1 câu:** Short-term nhớ "đang nói gì", Long-term nhớ "từng biết gì", Working đang nắm "giờ đang dùng gì" — ba lớp bổ sung nhau, không thay thế nhau.
---

## Tóm Tắt & Checklist

### Nội dung đã học trong module này

1. **Prompt Engineering vs Context Engineering** — prompt là hướng dẫn (làm gì), context là thông tin nền (biết gì); cần cả hai.
2. **Context Window Management** — cửa sổ hữu hạn của LLM; phải ưu tiên, đếm token, cắt bớt để không tràn.
3. **Context Assembly** — ghép nhiều nguồn (user, memory, docs, tools) thành một prompt thống nhất, có thứ tự.
4. **Context Compression** — nén context dài thành ngắn (trích hoặc tóm lược) giữ thông tin quan trọng.
5. **Context Retrieval** — tìm và lấy đúng context liên quan từ bộ nhớ/tài liệu — đúng và đủ.
6. **Short-term Context** — ngữ cảnh trong một phiên; giữ mạch hội thoại.
7. **Long-term Context** — ngữ cảnh qua nhiều phiên; nhớ về người và lịch sử dài hạn.
8. **Working Context** — ngữ cảnh "bàn làm việc" hiện tại agent đang dùng để suy nghĩ.
9. **Context Overflow** — khi context vượt giới hạn: truncation, lost-in-the-middle, lỗi, suy luận kém.
10. **Context Isolation** — giữ context mỗi agent tách biệt, tránh nhiễu và lộ dữ liệu trong multi-agent.

### Checklist tự kiểm tra

Bạn đã nắm được khi có thể trả lời lưu loát các câu hỏi sau:

- [ ] Phân biệt được Prompt Engineering và Context Engineering bằng một ví dụ?
- [ ] Giải thích vì sao phải quản lý context window và 2 cách phòng tránh overflow?
- [ ] Kể đúng thứ tự dòng chảy context: Retrieval → Assembly → Compression → LLM?
- [ ] Nêu khác biệt giữa nén trích (extractive) và nén tóm lược (abstractive)?
- [ ] Giải thích "retrieval" khác "compression" thế nào bằng lời của bạn?
- [ ] Phân biệt được short-term, long-term và working context với 1 ví dụ mỗi loại?
- [ ] Mô tả được 2 hậu quả của context overflow?
- [ ] Giải thích tại sao multi-agent cần context isolation?
- [ ] Đọc ngược sơ đồ Context Flow và giải thích từng bước?

---

## Tóm Gọn Toàn Module

> **Một câu để nhớ mãi:** Context Engineering là nghệ thuật **đưa đúng thông tin nền vào đúng lúc, trong giới hạn cửa sổ có hạn** — biết lấy (retrieval), ghép (assembly), nén (compression) và giữ gìn (isolation) để LLM lúc nào cũng "thấy" được đúng thứ cần thấy.

**Đi tiếp:** Module 7 — **Memory Engineering** — sẽ dạy bạn *làm cho agent nhớ lâu*: cách lưu trữ, tổ chức và gợi lại trí nhớ (ngắn hạn, dài hạn, chủ động), và mối liên hệ mật thiết giữa memory và context — thứ đã được làm quen trong module này.
