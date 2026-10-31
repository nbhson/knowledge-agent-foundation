# Harness Engineering - Kỹ Thuật Thiết Kế Hệ Thống Xung Quanh AI Agents

> **"Mỗi khi agent mắc lỗi, bạn không cầu nguyện nó làm tốt hơn lần sau – bạn xây dựng một giải pháp hệ thống để nó không bao giờ mắc lỗi đó nữa"**  
> — Mitchell Hashimoto (Founder of HashiCorp, Creator of Terraform)

---

## Mục Lục

- [Harness Engineering - Kỹ Thuật Thiết Kế Hệ Thống Xung Quanh AI Agents](#harness-engineering---kỹ-thuật-thiết-kế-hệ-thống-xung-quanh-ai-agents)
  - [Mục Lục](#mục-lục)
  - [1. Giới Thiệu](#1-giới-thiệu)
    - [Bối Cảnh](#bối-cảnh)
    - [Mục Đích Của Tài Liệu](#mục-đích-của-tài-liệu)
  - [2. Harness Engineering Là Gì?](#2-harness-engineering-là-gì)
    - [Định Nghĩa](#định-nghĩa)
    - [Triết Lý Cốt Lõi](#triết-lý-cốt-lõi)
    - [Ví Dụ Minh Họa](#ví-dụ-minh-họa)
    - [So Sánh Với Các Khái Niệm Khác](#so-sánh-với-các-khái-niệm-khác)
  - [3. Ba Giai Đoạn Tiến Hóa Của Kỹ Nghệ AI](#3-ba-giai-đoạn-tiến-hóa-của-kỹ-nghệ-ai)
    - [3.1. Prompt Engineering (2022-2024)](#31-prompt-engineering-2022-2024)
    - [3.2. Context Engineering (2025)](#32-context-engineering-2025)
    - [3.3. Harness Engineering (2026+)](#33-harness-engineering-2026)
    - [So Sánh Tổng Quan](#so-sánh-tổng-quan)
    - [Insight Quan Trọng](#insight-quan-trọng)
  - [4. Tại Sao Harness Engineering Quan Trọng?](#4-tại-sao-harness-engineering-quan-trọng)
    - [4.1. Tối Ưu Hiệu Suất Vượt Trội](#41-tối-ưu-hiệu-suất-vượt-trội)
    - [4.2. Mô Hình Chỉ Là Công Cụ, Hệ Thống Mới Quyết Định Kết Quả](#42-mô-hình-chỉ-là-công-cụ-hệ-thống-mới-quyết-định-kết-quả)
    - [4.3. Kiểm Soát và Đáng Tin Cậy](#43-kiểm-soát-và-đáng-tin-cậy)
    - [4.4. Scalability và Maintainability](#44-scalability-và-maintainability)
    - [4.5. Giảm Chi Phí Đáng Kể](#45-giảm-chi-phí-đáng-kể)
    - [4.6. Competitive Advantage](#46-competitive-advantage)
    - [Tóm Lại](#tóm-lại)
  - [5. Các Thành Phần Cốt Lõi Của Harness](#5-các-thành-phần-cốt-lõi-của-harness)
    - [5.1. Tools (Công Cụ) - "Tay Chân"](#51-tools-công-cụ---tay-chân)
    - [5.2. Memory (Bộ Nhớ) - "Não"](#52-memory-bộ-nhớ---não)
    - [5.3. Context Management (Quản Lý Ngữ Cảnh) - "Hệ Tuần Hoàn"](#53-context-management-quản-lý-ngữ-cảnh---hệ-tuần-hoàn)
      - [Vậy Can Thiệp Vào Đâu?](#vậy-can-thiệp-vào-đâu)
      - [Làm Sao Để Đoạn Code Đó Tự Động Chạy?](#làm-sao-để-đoạn-code-đó-tự-động-chạy)
    - [5.4. Guardrails (Rào Cản) - "Hệ Miễn Dịch"](#54-guardrails-rào-cản---hệ-miễn-dịch)
    - [5.5. Feedback Loops (Vòng Lặp Phản Hồi) - "Cảm Giác"](#55-feedback-loops-vòng-lặp-phản-hồi---cảm-giác)
    - [5.6. Permissions (Quyền Hạn) - "Xương"](#56-permissions-quyền-hạn---xương)
    - [5.7. Orchestration (Điều Phối) - "Hệ Thần Kinh"](#57-orchestration-điều-phối---hệ-thần-kinh)
    - [Tích Hợp Tất Cả](#tích-hợp-tất-cả)
    - [Tích Hợp Component Với Modules Trong Repo](#tích-hợp-component-với-modules-trong-repo)
      - [Bảng Mapping Chi Tiết](#bảng-mapping-chi-tiết)
  - [🔭 Toàn Cảnh: Harness Engineering — AI Coding Skills Framework](#-toàn-cảnh-harness-engineering--ai-coding-skills-framework)
    - [Kiến Trúc Tổng Thể: 7 Components → 15 Modules](#kiến-trúc-tổng-thể-7-components--15-modules)
    - [6.2. Anthropic Multi-Agent Architecture](#62-anthropic-multi-agent-architecture)
    - [6.3. Claude Code Leak - Hệ Thống Harness Siêu Đẳng](#63-claude-code-leak---hệ-thống-harness-siêu-đẳng)
      - [A. Quản lý Context 5 Cấp Độ](#a-quản-lý-context-5-cấp-độ)
      - [B. Bộ Nhớ 3 Tầng với Auto-Optimization](#b-bộ-nhớ-3-tầng-với-auto-optimization)
      - [C. Phân Quyền Tool Chặt Chẽ](#c-phân-quyền-tool-chặt-chẽ)
      - [D. Tone Detection với Regex (!)](#d-tone-detection-với-regex-)
    - [6.4. Cursor IDE - Harness Tối Ưu Cho Coding](#64-cursor-ide---harness-tối-ưu-cho-coding)
    - [6.5. DeepSeek Harness — Micro-Kernel \& Trajectory Traceability Framework](#65-deepseek-harness--micro-kernel--trajectory-traceability-framework)
      - [A. Kiến Trúc Micro-Kernel \& Ecosystem Plugin](#a-kiến-trúc-micro-kernel--ecosystem-plugin)
      - [B. 4 Runtime Modes Phân Hóa](#b-4-runtime-modes-phân-hóa)
      - [C. Trajectory Traceability Engine (Session Event Stream \& Branching)](#c-trajectory-traceability-engine-session-event-stream--branching)
      - [D. Code Mode SDK \& Sandboxed Execution](#d-code-mode-sdk--sandboxed-execution)
      - [E. Minimal Benchmark Harness Cho Đánh Giá Năng Lực AI](#e-minimal-benchmark-harness-cho-đánh-giá-năng-lực-ai)
    - [Bài Học Chung Từ Các Case Studies](#bài-học-chung-từ-các-case-studies)
  - [7. Nguyên Tắc Thiết Kế Harness](#7-nguyên-tắc-thiết-kế-harness)
    - [7.1. Nguyên Tắc SOLID Cho Harness](#71-nguyên-tắc-solid-cho-harness)
    - [7.2. The 10 Commandments of Harness Engineering](#72-the-10-commandments-of-harness-engineering)
    - [7.3. The Harness Design Pattern](#73-the-harness-design-pattern)
  - [8. Best Practices](#8-best-practices)
    - [8.1. Tool Design](#81-tool-design)
    - [8.2. Memory Management](#82-memory-management)
    - [8.3. Context Building](#83-context-building)
    - [8.4. Guardrails](#84-guardrails)
    - [8.5. Testing Harness](#85-testing-harness)
  - [9. Công Cụ và Framework](#9-công-cụ-và-framework)
    - [9.1. Frameworks Phổ Biến](#91-frameworks-phổ-biến)
    - [9.2. Công Cụ Hỗ Trợ](#92-công-cụ-hỗ-trợ)
    - [9.3. Starter Template](#93-starter-template)
  - [10. Tương Lai Của Harness Engineering](#10-tương-lai-của-harness-engineering)
    - [10.1. Xu Hướng 2026-2028](#101-xu-hướng-2026-2028)
    - [10.2. Thách Thức Phía Trước](#102-thách-thức-phía-trước)
    - [10.3. Lời Khuyên Cho Tương Lai](#103-lời-khuyên-cho-tương-lai)
  - [11. Tài Liệu Tham Khảo](#11-tài-liệu-tham-khảo)
    - [Papers \& Research](#papers--research)
    - [Frameworks \& Tools](#frameworks--tools)
    - [Communities](#communities)
    - [Blogs \& Resources](#blogs--resources)
    - [Courses \& Tutorials](#courses--tutorials)

> **Tóm gọn 1 câu:** Tài liệu gồm 11 phần: lý thuyết (1–4), 7 thành phần harness (5), ánh xạ sang framework (🔭), case studies (6), nguyên tắc và best practices (7–8), công cụ (9), tương lai (10), tài liệu tham khảo (11).

---

## 1. Giới Thiệu

Trong kỷ nguyên AI, các mô hình ngôn ngữ lớn (LLM — Large Language Model, tức các model AI "hiểu và sinh ra văn bản" như GPT-4, Claude, Gemini) phát triển rất nhanh — từ GPT-3, GPT-4, Claude tới Gemini, model nào cũng ngày càng thông minh hơn. Nhưng có một câu hỏi đáng suy nghĩ: **cùng một model, sao có ứng dụng chạy rất tốt, có ứng dụng lại chưa hiệu quả?**

Câu trả lời nằm ở **Harness Engineering** — Harness nghĩa là "bộ dây an toàn/dây cương": thay vì cố làm model giỏi hơn, bạn xây nguyên **hệ sinh thái quanh nó**: tools, permissions, memory, feedback loops, guardrails, quản lý context (từng khái niệm này được giải thích kỹ ở mục 5).

### Bối Cảnh

Khi Mitchell Hashimoto (người sáng lập HashiCorp — công ty làm Terraform, công cụ viết "hạ tầng" máy chủ dưới dạng code — tác giả Terraform) nói *"Prompt Engineering đã chết"* và đưa ra khái niệm **Harness Engineering**, ông đã mở ra một góc nhìn mới về cách làm ứng dụng AI. Thay vì cố viết prompt thật hay (prompt = câu lệnh/nhắn tin bạn gửi cho AI), ta tập trung xây hẳn một hệ thống để AI làm việc hiệu quả.

> **Tóm gọn 1 câu:** Một chuyên gia phần mềm lão làng tuyên bố: đừng dỗ dành model bằng từ ngữ — hãy xây hệ thống bao quanh nó.

### Mục Đích Của Tài Liệu

Tài liệu này giúp bạn có cái nhìn toàn diện về Harness Engineering, gồm:
- Định nghĩa và triết lý cốt lõi
- So sánh với các kỹ thuật trước đó (Prompt Engineering, Context Engineering)
- Các thành phần và nguyên tắc thiết kế
- Case studies từ các công ty hàng đầu (Princeton NLP, Anthropic)
- Best practices và hướng dẫn triển khai thực tế

> **Tóm gọn 1 câu:** Model AI giỏi chưa đủ — cái quyết định ứng dụng chạy tốt hay dở là cả hệ thống bao quanh model (harness), và đó chính là thứ tài liệu này dạy bạn cách xây.

---

## 2. Harness Engineering Là Gì?

Mục này giải thích Harness Engineering là gì, triết lý đằng sau, và nó khác gì các cách làm AI trước đó — để bạn có "từ điển chung" trước khi đi vào chi tiết.

### Định Nghĩa

**Harness Engineering** là cách xây nguyên **"môi trường sống" cho một model AI** — gồm tools, quyền truy cập, memory, feedback loops, guardrails, quản lý context — thay vì can thiệp vào bản thân model.

Nói một cách đơn giản:
- **Mô hình AI** là thứ **suy nghĩ** — giống bộ não
- **Harness** là thứ mà AI **suy nghĩ về** — giống cơ thể, mắt tai, tay chân và luật lệ nơi làm việc
- Và chính **Harness** mới quyết định **chất lượng đầu ra cuối cùng** — não giỏi mà làm việc trong môi trường tệ thì kết quả vẫn tệ

Ví dụ cho dễ hình dung: cùng một nhân viên giỏi (model), đặt vào công ty có quy trình rõ ràng, công cụ tốt (harness tốt) thì hiệu suất cao; đặt vào chỗ loạn xạ thì hiệu suất thấp — dù người vẫn là người đó.

> **Tóm gọn 1 câu:** Harness = "môi trường sống" của model (tools, quyền, nhớ, rào cản); model chỉ nghĩ, harness quyết định kết quả.

### Triết Lý Cốt Lõi

> *"Mỗi khi agent mắc lỗi, bạn không cầu nguyện nó làm tốt hơn lần sau – bạn xây dựng một giải pháp hệ thống để nó không bao giờ mắc lỗi đó nữa"*

(agent = chương trình AI tự hành động theo mục tiêu; lỗi ở đây ví dụ như agent xóa nhầm file, hay trả lời sai dữ liệu.)

Triết lý này nhấn mạnh vào:

1. **Systematic Solutions over Prayers**: Thay vì hy vọng AI sẽ "học" từ lỗi, bạn xây dựng cơ chế hệ thống ngăn chặn lỗi đó tái diễn. Ví dụ: agent từng xóa nhầm file → thay vì dặn dò trong prompt, bạn chặn lệnh xóa ở tầng hệ thống.

2. **Infrastructure over Instructions**: Thay vì viết prompt dài dòng hướng dẫn AI làm gì, bạn xây dựng cơ sở hạ tầng hạn chế những gì AI có thể làm. (Infrastructure = hạ tầng: tool, quyền hạn, cơ chế kiểm tra được cài sẵn trong code.)

3. **Design over Training**: Thay vì fine-tune mô hình (fine-tune = huấn luyện lại model trên dữ liệu riêng, tốn tiền và GPU), bạn thiết kế môi trường hoạt động của mô hình — việc này làm được ngay hôm nay, không cần máy chủ khủng.

> **Tóm gọn 1 câu:** Ba chữ "over" một ý: giải pháp hệ thống thắng lời cầu nguyện, hạ tầng thắng lời dặn, thiết kế môi trường thắng huấn luyện lại model.

### Ví Dụ Minh Họa

Mục này cho thấy khác biệt cụ thể giữa "nhờ vả" và "xây hệ thống". Hãy tưởng tượng bạn có một AI coding assistant:

**❌ Cách tiếp cận cũ (Prompt Engineering):**
```
"Hãy viết code Python. Đảm bảo code của bạn không có lỗi cú pháp. 
Kiểm tra kỹ trước khi trả về. Nếu có lỗi, hãy sửa..."
```
(Lỗi cú pháp = code viết sai ngữ pháp ngôn ngữ lập trình, ví dụ thiếu dấu `:` cuối dòng `if` trong Python.)

**✅ Cách tiếp cận mới (Harness Engineering):**

<details>
<summary><b>JavaScript Code (Click to expand/collapse)</b></summary>

> 📄 **Code ví dụ:** [`examples/01-vi-du-minh-hoa.js`](examples/01-vi-du-minh-hoa.js)

</details>

Trong ví dụ trên, thay vì "nhờ" AI cẩn thận giúp mình, bạn xây hẳn một hệ thống **không cho phép** AI trả về code bị lỗi — code chạy qua bộ kiểm tra tự động trước khi tới tay bạn, lỗi thì bị chặn lại.

> **Tóm gọn 1 câu:** Cách cũ "nhờ" AI cẩn thận; cách mới xây bộ kiểm tra tự động chặn code lỗi trước khi nó kịp ra ngoài.

### So Sánh Với Các Khái Niệm Khác

Cách đọc bảng này: mỗi hàng so sánh 3 kỹ thuật theo một khía cạnh; cột bên trái là tên khía cạnh. Ví dụ, hàng **"Focus"** nghĩa là: Prompt Engineering chỉ lo "cách hỏi", Context Engineering lo "dữ liệu đưa vào", còn Harness Engineering lo "toàn bộ hệ thống".

| Khía cạnh | Prompt Engineering | Context Engineering | Harness Engineering |
|-----------|-------------------|---------------------|---------------------|
| **Focus** | Cách hỏi | Dữ liệu đầu vào | Toàn bộ hệ thống |
| **Mục tiêu** | Câu prompt tốt hơn | Context phù hợp hơn | Môi trường tốt hơn |
| **Ví dụ** | Viết email | Đính kèm file | Thiết kế văn phòng + quy trình |
| **Kiểm soát** | Thấp | Trung bình | Cao |
| **Tính bền vững** | Thấp | Trung bình | Cao |

(context = toàn bộ thông tin model nhìn thấy khi trả lời; "kiểm soát" cao nghĩa là bạn đoán trước được và điều khiển được hành vi của AI.)

> **Tóm gọn 1 câu:** Harness Engineering = xây môi trường (tools, quyền, bộ nhớ, rào cản) quanh model thay vì vá model, vì chính môi trường mới quyết định chất lượng đầu ra.

---

## 3. Ba Giai Đoạn Tiến Hóa Của Kỹ Nghệ AI

Mục này kể lại 3 "thời đại" của kỹ nghệ AI: mỗi thời đại giải quyết điểm yếu của thời đại trước. Hiểu được dòng chảy này, bạn sẽ hiểu vì sao Harness Engineering xuất hiện và nó bổ sung gì.

Để hiểu rõ hơn về Harness Engineering, mình cùng nhìn lại quá trình làm AI đã đi qua những chặng nào nhé:

### 3.1. Prompt Engineering (2022-2024)

**Focus**: *"Hỏi AI thế nào cho đúng?"*

**Đặc điểm:**
- Tập trung vào việc viết câu prompt tốt
- Sử dụng các kỹ thuật: few-shot learning, chain-of-thought, role-playing
- Phụ thuộc nhiều vào "nghệ thuật" viết prompt

Giải thích nhanh các thuật ngữ:
- **Few-shot learning**: đưa vài ví dụ mẫu vào prompt để AI "bắt chước". Ví dụ: cho 2-3 cặp câu hỏi→trả lời đúng định dạng, AI sẽ trả lời đúng định dạng đó.
- **Chain-of-thought**: yêu cầu AI suy nghĩ từng bước ("Think step by step") thay vì nhảy đến đáp án.
- **Role-playing**: giao vai cho AI ("Bạn là chuyên gia pháp lý...") để câu trả lời đúng giọng và đúng chuyên môn.

**Ví dụ:**
```
User: "Act as a senior Python developer. Write a function to..."
User: "Think step by step..."
User: "Here are some examples: ..."
```

**Hạn chế:**
- Khó mở rộng và duy trì
- Kết quả không ổn định
- Khó debug khi có lỗi
- Phụ thuộc quá nhiều vào cách diễn đạt

**So sánh:** Giống như viết email - bạn lo lắng về từng từ, từng câu.

> **Tóm gọn 1 câu:** Thời kỳ đầu, mọi hy vọng đặt vào việc "viết câu lệnh hay hơn" — nhưng câu chữ hay không sửa được việc AI thiếu thông tin và thiếu rào cản.

---

### 3.2. Context Engineering (2025)

Mục này giải thích "thời đại thứ hai": người ta nhận ra AI trả lời sai phần lớn vì **thiếu đúng thông tin**, nên thay vì dỗ dành, ta tập trung cấp dữ liệu cho nó.

**Focus**: *"Đưa thông tin gì để AI trả lời tốt?"*

**Đặc điểm:**
- Tập trung vào việc cung cấp đúng dữ liệu đầu vào
- Sử dụng RAG (Retrieval Augmented Generation — kỹ thuật "tra tài liệu rồi mới trả lời": trước khi hỏi AI, hệ thống tự tìm các đoạn văn bản liên quan trong kho tài liệu và ghép vào prompt)
- Quản lý context window hiệu quả (context window = "bộ nhớ tạm" của model, đo bằng số token — token ≈ một từ/miếng chữ; vượt quá giới hạn này là model "quên" phần đầu)
- Tích hợp knowledge bases (kho tri thức — ví dụ toàn bộ tài liệu nội bộ công ty)

**Ví dụ:**

<details>
<summary><b>JavaScript Code (Click to expand/collapse)</b></summary>

> 📄 **Code ví dụ:** [`examples/02-3-2-context-engineering-2025.js`](examples/02-3-2-context-engineering-2025.js)

</details>

**Ưu điểm:**
- Cải thiện độ chính xác
- Giảm hallucination (hallucination = model "tỉa" — bịa ra thông tin nghe có vẻ đúng nhưng sai, ví dụ trích dẫn quy định không tồn tại)
- Có thể scale với dữ liệu lớn

**Hạn chế:**
- Vẫn phụ thuộc vào chất lượng context
- Chưa kiểm soát được hành vi của AI
- Khó xử lý các tình huống phức tạp

**So sánh:** Giống như đính kèm đúng file vào email - bạn cung cấp đủ thông tin cần thiết.

> **Tóm gọn 1 câu:** Context Engineering = cấp đúng dữ liệu cho AI (điển hình là RAG) để nó đỡ bịa, nhưng vẫn chưa kiểm soát được hành vi của nó.

---

### 3.3. Harness Engineering (2026+)

Mục này giải thích "thời đại thứ ba" — nơi ta không chỉ lo câu chữ hay dữ liệu, mà thiết kế **toàn bộ môi trường** AI hoạt động trong đó.

**Focus**: *"Toàn bộ hệ thống quanh AI vận hành ra sao?"*

**Đặc điểm:**
- Thiết kế toàn bộ môi trường hoạt động
- Tích hợp tools, memory, guardrails
- Kiểm soát chặt chẽ hành vi của AI
- Tự động xử lý lỗi và tối ưu hóa

**Ví dụ:**

<details>
<summary><b>JavaScript Code (Click to expand/collapse)</b></summary>

> 📄 **Code ví dụ:** [`examples/03-3-3-harness-engineering-2026.js`](examples/03-3-3-harness-engineering-2026.js)

</details>

**Ưu điểm:**
- Kiểm soát hoàn toàn hành vi AI
- Dễ debug và maintain (maintain = bảo trì: sửa lỗi, nâng cấp về sau mà không vỡ hệ thống)
- Có thể mở rộng và tái sử dụng
- Kết quả ổn định và đáng tin cậy

**So sánh:** Giống như thiết kế cả văn phòng và quy trình làm việc - bạn tạo ra một hệ sinh thái hoàn chỉnh.

> **Tóm gọn 1 câu:** Harness Engineering = thiết kế cả "văn phòng" (tools, quyền, quy trình, rào cản) để AI làm việc, thay vì chỉ lo câu hỏi và dữ liệu.

---

### So Sánh Tổng Quan

Sơ đồ dưới đây tóm tắt 3 thời đại theo thứ tự thời gian (đọc từ trên xuống): mỗi khung là một kỹ thuật, kèm câu hỏi trung tâm và mức kiểm soát — ⭐ càng nhiều thì càng kiểm soát được hành vi AI.

```
┌─────────────────────────────────────────────────────────────┐
│                    TIẾN HÓA KỸ NGHỆ AI                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  2022-2024: PROMPT ENGINEERING                              │
│  ┌─────────────────────────────────┐                       │
│  │ "Làm sao hỏi cho đúng?"         │                       │
│  │ Focus: Câu prompt                │                       │
│  │ Control: ⭐ Thấp                 │                       │
│  └─────────────────────────────────┘                       │
│                    │                                        │
│                    ▼                                        │
│  2025: CONTEXT ENGINEERING                                  │
│  ┌─────────────────────────────────┐                       │
│  │ "Đưa thông tin gì?"             │                       │
│  │ Focus: Dữ liệu đầu vào          │                       │
│  │ Control: ⭐⭐ Trung bình         │                       │
│  └─────────────────────────────────┘                       │
│                    │                                        │
│                    ▼                                        │
│  2026+: HARNESS ENGINEERING                                 │
│  ┌─────────────────────────────────┐                       │
│  │ "Hệ thống hoạt động ra sao?"   │                       │
│  │ Focus: Toàn bộ môi trường       │                       │
│  │ Control: ⭐⭐⭐⭐⭐ Cao          │                       │
│  └─────────────────────────────────┘                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

> **Tóm gọn 1 câu:** Đọc từ trên xuống: càng về sau, vòng kiểm soát càng rộng — từ câu chữ, đến dữ liệu, đến cả hệ thống.

### Insight Quan Trọng

Mục này trả lời một hiểu lầm phổ biến: "Harness thay thế prompt engineering luôn à?" — Không đâu.

> **"Prompt Engineering chưa chết, nhưng nó không còn đủ"**

Mỗi giai đoạn không thay thế hoàn toàn giai đoạn trước, mà bổ sung thêm một layer kiểm soát (layer = tầng, như tầng của một tòa nhà — tầng mới dựng lên trên tầng cũ, không đập tầng cũ đi):
- Bạn vẫn cần **prompt tốt** (Prompt Engineering)
- Bạn vẫn cần **context phù hợp** (Context Engineering)
- Nhưng bạn cần thêm **hệ thống hoàn chỉnh** (Harness Engineering)

> **Tóm gọn 1 câu:** Ba kỹ thuật xếp lớp chứ không thay nhau — prompt hay + dữ liệu đúng + hệ thống chặt là bộ ba đầy đủ.

---

## 4. Tại Sao Harness Engineering Quan Trọng?

Mục này trả lời câu hỏi "tại sao phải bỏ công xây harness?" bằng số liệu thật: hiệu suất tăng bao nhiêu, chi phí giảm bao nhiêu, và lợi thế cạnh tranh nằm ở đâu.

### 4.1. Tối Ưu Hiệu Suất Vượt Trội

**Nghiên cứu từ Princeton NLP** (paper SWE-agent) đã chứng minh một phát hiện đột phá:

> Chỉ cần thay đổi cách thiết kế **"giao diện/môi trường"** (ACI - Agent-Computer Interface, tức "bộ điều khiển" mà agent dùng để đụng vào máy tính: xem file, tìm kiếm, sửa file...), hiệu suất của AI có thể **tăng tới 64%** mà không cần nâng cấp mô hình.

(ACI đối với agent giống bàn phím + màn hình đối với bạn: giao diện tệ thì người giỏi cũng làm chậm.)

**Kết quả thực nghiệm:**

Cách đọc bảng này: hàng 1 là nhóm đối chứng (không can thiệp gì), hàng 2 là nhóm được cải thiện ACI; cột "Success Rate" là % bài toán agent tự sửa được; cột "Improvement" là mức tăng tương đối so với baseline.

| Cách tiếp cận | Success Rate | Improvement |
|---------------|--------------|-------------|
| Baseline (no harness) | 12.5% | - |
| With optimized harness | 20.5% | +64% |

(20.5% so với 12.5% là tăng tương đối 64% — tức tăng gấp 1.64 lần, chứ không phải tăng lên 64%.)

**Điều này nghĩa là gì?**
- Thiết kế harness đôi khi còn quan trọng hơn chọn model
- Lợi nhuận trên công sức bỏ ra cao hơn hẳn so với train/fine-tune model mới (fine-tune = huấn luyện lại model, cần dữ liệu + GPU đắt đỏ)
- Làm được ngay, không cần tài nguyên khủng

> **Tóm gọn 1 câu:** Cải thiện "bộ điều khiển" (ACI) tăng 64% hiệu suất mà không đụng vào model — bằng chứng đầu tiên cho thấy harness quan trọng ngang model.

---

### 4.2. Mô Hình Chỉ Là Công Cụ, Hệ Thống Mới Quyết Định Kết Quả

Mục này giải thích hiện tượng "hàng hóa hóa" model và vì sao lợi thế cạnh tranh dời về phía harness.

**Thực tế của thị trường AI:**

```
┌──────────────────────────────────────────────────────┐
│  COMMODITIZATION OF AI MODELS                        │
├──────────────────────────────────────────────────────┤
│                                                      │
│  2023: GPT-4 là "vua"                                │
│  2024: Claude 3, Gemini Ultra cạnh tranh             │
│  2025: Nhiều mô hình tương đương nhau                │
│  2026: Mô hình trở thành "hàng hóa" (commodity)      │
│                                                      │
│  ➜ Sự khác biệt không còn ở mô hình                 │
│  ➜ Sự khác biệt nằm ở HARNESS                       │
│                                                      │
└──────────────────────────────────────────────────────┘
```

(commodity = hàng hóa phổ thông: ai cũng mua được, chất lượng na ná — như điện hay nước máy, không ai "ăn đong" vì dùng điện của hãng này. Khi model thành commodity, chọn model nào cũng gần như vậy, nên điểm khác biệt phải nằm ở chỗ khác.)

**Ví dụ thực tế:**

Cùng một mô hình Claude 3.5 Sonnet:
- **Cursor IDE**: Rất hiệu quả trong coding
- **Random chatbot**: Không tốt lắm

➜ **Điều khác biệt?** Harness design của Cursor!

> **Tóm gọn 1 câu:** Khi model nào cũng ngang nhau, sản phẩm nào có harness tốt hơn sẽ thắng — model là nguyên liệu, harness là nhà bếp.

---

### 4.3. Kiểm Soát và Đáng Tin Cậy

Mục này cho thấy harness giúp bạn "đò được" hành vi của AI: lỗi bị chặn ở tầng hệ thống chứ không phụ thuộc vào lời hứa của model.

**Vấn đề với approach cũ:**

<details>
<summary><b>JavaScript Code (Click to expand/collapse)</b></summary>

> 📄 **Code ví dụ:** [`examples/04-4-3-kiem-soat-va-ang-tin-cay.js`](examples/04-4-3-kiem-soat-va-ang-tin-cay.js)

</details>

**Với Harness Engineering:**

<details>
<summary><b>JavaScript Code (Click to expand/collapse)</b></summary>

> 📄 **Code ví dụ:** [`examples/05-4-3-kiem-soat-va-ang-tin-cay.js`](examples/05-4-3-kiem-soat-va-ang-tin-cay.js)

</details>

> **Tóm gọn 1 câu:** Harness biến "hy vọng AI tự kiểm tra" thành "hệ thống tự kiểm tra thay AI" — kiểm soát được thì mới tin được.

---

### 4.4. Scalability và Maintainability

Mục này nói về 2 thứ hay bỏ quên khi demo chạy đẹp: scale (mở rộng lên nhiều agent) và maintain (bảo trì về sau). 

**Kịch bản thực tế:**

Bạn có 10 AI agents trong hệ thống. Bạn phát hiện một lỗi bảo mật:

**❌ Không có Harness:**
```
- Phải update 10 prompts khác nhau
- Phải test lại 10 agents
- Không chắc đã fix hết chưa
- Mất 2-3 ngày
```

**✅ Có Harness:**

<details>
<summary><b>JavaScript Code (Click to expand/collapse)</b></summary>

> 📄 **Code ví dụ:** [`examples/06-4-4-scalability-va-maintainability.js`](examples/06-4-4-scalability-va-maintainability.js)

</details>

> **Tóm gọn 1 câu:** Sửa lỗi ở 1 chỗ (harness) thay vì 10 chỗ (10 prompts) — hệ thống lớn thì không có harness là ác mộng bảo trì.

---

### 4.5. Giảm Chi Phí Đáng Kể

Mục này tính "harness đáng tiền" theo 3 mảng: ít tốn token, ít lỗi, và làm nhanh hơn.

**Cost Savings từ Harness Engineering:**

(token = đơn vị chữ model xử lý; bạn trả tiền API theo số token.)

1. **Giảm token usage**
   - Context compression (nén ngữ cảnh — gom nội dung dài thành tóm tắt ngắn trước khi gửi model)
   - Smart caching (cache = nhớ kết quả đã tính để dùng lại, khỏi tính lại từ đầu)
   - Efficient tool calling
   - **Tiết kiệm: 40-60% cost**

2. **Giảm error rate**
   - Automatic validation (tự kiểm tra đầu vào/đầu ra bằng code, không phải người)
   - Built-in guardrails
   - **Giảm: 70-80% failed requests**

3. **Tăng development speed**
   - Reusable components (component dùng lại được cho nhiều dự án)
   - Clear architecture
   - **Tăng: 3-5x faster development**

**Ví dụ tính toán:**

```
Dự án AI Agent truyền thống:
- API cost: $2,000/month
- Development time: 3 months
- Error handling: 40 hours/month
Total: ~$30,000 (3 months)

Với Harness Engineering:
- API cost: $800/month (giảm 60%)
- Development time: 1 month (reuse harness)
- Error handling: 5 hours/month (tự động)
Total: ~$12,000 (3 months)

➜ Savings: $18,000 (60%)
```

> **Tóm gọn 1 câu:** Harness tốn công xây một lần nhưng tiết kiệm 40-60% tiền API, giảm tới 80% request lỗi và làm việc nhanh hơn 3-5 lần.

---

### 4.6. Competitive Advantage

Mục này trả lời: "Mình không thi lấy gì? Câu trả lời: harness chính là con hào bảo vệ doanh nghiệp."

Khi các model AI na ná nhau, **Harness Engineering chính là con hào cạnh tranh** (moat — thuật ngữ kinh doanh chỉ thứ đối thủ khó bắt chước, như hào nước quanh thành trì) của bạn:

- **Anthropic**: Harness siêu đẳng (theo leak code của Claude)
- **Cursor**: Harness tối ưu cho coding
- **Perplexity**: Harness tốt cho search & research

➜ Đây là lý do tại sao họ dẫn đầu thị trường!

> **Tóm gọn 1 câu:** Model ai cũng thuê được, nhưng harness công ty bạn tự xây là thứ đối thủ không copy một sớm một chiều.

---

### Tóm Lại

Phần này gói lại 6 lý do đã trình bày ở các mục 4.1–4.6.

Harness Engineering quan trọng vì:

1. ✅ **Tăng hiệu suất 64%+** (theo nghiên cứu Princeton)
2. ✅ **Tạo competitive advantage** khi mô hình trở thành commodity
3. ✅ **Kiểm soát và đáng tin cậy** hơn nhiều
4. ✅ **Scale và maintain dễ dàng**
5. ✅ **Tiết kiệm 40-60% chi phí**
6. ✅ **Tăng tốc development 3-5x**

> **"In the age of AI commoditization, your harness is your moat"**
> (Tạm dịch: "Trong thời đại model thành hàng hóa, harness chính là con hào của bạn")

> **Tóm gọn 1 câu:** Harness Engineering đáng đầu tư vì nó tăng 64% hiệu suất, giảm 40-60% chi phí, dễ bảo trì, và là lợi thế cạnh tranh khi model ai cũng có.

---

## 5. Các Thành Phần Cốt Lõi Của Harness

Mục này là "bản đồ cơ thể" của harness: giải thích lần lượt 7 thành phần, mỗi thành phần làm nhiệm vụ gì và gồm những gì.

Một harness đầy đủ gồm 7 mảnh ghép. Bạn cứ hình dung chúng như các "cơ quan" trong cơ thể nhé:

```
┌─────────────────────────────────────────────────────────┐
│              KIẾN TRÚC HARNESS HOÀN CHỈNH               │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────┐      ┌─────────────┐                 │
│  │   TOOLS     │◄────►│   MEMORY    │                 │
│  │  (Tay chân) │      │ (Bộ não)    │                 │
│  └─────────────┘      └─────────────┘                 │
│         ▲                    ▲                         │
│         │                    │                         │
│         ▼                    ▼                         │
│  ┌─────────────────────────────────┐                  │
│  │      CONTEXT MANAGEMENT         │                  │
│  │      (Hệ thống tuần hoàn)       │                  │
│  └─────────────────────────────────┘                  │
│         ▲                    ▲                         │
│         │                    │                         │
│  ┌─────────────┐      ┌─────────────┐                 │
│  │ GUARDRAILS  │      │  FEEDBACK   │                 │
│  │(Hệ miễn dịch)│      │(Cảm giác)   │                 │
│  └─────────────┘      └─────────────┘                 │
│         ▲                    ▲                         │
│         │                    │                         │
│  ┌─────────────┐      ┌─────────────┐                 │
│  │ PERMISSIONS │      │ ORCHESTRATION│                │
│  │  (Xương)    │      │(Hệ thần kinh)│                │
│  └─────────────┘      └─────────────┘                 │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

### 5.1. Tools (Công Cụ) - "Tay Chân"

Mục này giải thích "tay chân" của AI: Tools là những hàm bạn định nghĩa để agent gọi ra và tác động ra thế giới ngoài (đọc file, gọi API, tra database...). Không có tool, AI chỉ biết nói chứ không biết làm.

**Mục đích**: Định nghĩa những gì AI có thể **làm**

**Ví dụ:**

<details>
<summary><b>TypeScript Code (Click to expand/collapse)</b></summary>

> 📄 **Code ví dụ:** [`examples/07-5-1-tools-cong-cu-tay-chan.ts`](examples/07-5-1-tools-cong-cu-tay-chan.ts)

</details>

**Best Practices:**

Cách đọc: dấu ✅ là điều nên làm, ❌ là điều nên tránh.

- ✅ Giới hạn scope của mỗi tool (single responsibility — mỗi tool chỉ làm đúng một việc, ví dụ tool "đọc file" không kiêm luôn "xóa file")
- ✅ Validation đầu vào và đầu ra (validation = kiểm tra dữ liệu trước khi dùng: tên file có tồn tại không, số trang có hợp lệ không)
- ✅ Clear error messages (khi tool lỗi, thông báo phải nói rõ sai gì để AI biết cách sửa — "File not found: reports/q3.md" thì tốt hơn "Error")
- ✅ Idempotent khi có thể (idempotent = gọi nhiều lần vẫn cho cùng một kết quả — ví dụ "đặt file thành nội dung X" an toàn hơn "thêm 1 dòng vào cuối file", vì gọi 2 lần không làm hỏng gì)
- ❌ Tránh tools quá mạnh (e.g., "execute_any_command")

> **Tóm gọn 1 câu:** Tool = tay chân của AI; thiết kế tool nhỏ, kiểm tra dữ liệu vào/ra, báo lỗi rõ ràng — đừng đưa cho AI một cây búa đập được mọi thứ.

---

### 5.2. Memory (Bộ Nhớ) - "Não"

Mục này giải thích AI "nhớ gì" và "nhớ trong bao lâu": bộ nhớ ngắn hạn cho cuộc trò chuyện hiện tại, bộ nhớ dài hạn cho kiến thức, và bộ nhớ làm việc cho task đang chạy.

**Mục đích**: Quản lý thông tin AI cần **nhớ**

**3 Loại Memory:**

Giải thích nhanh trước khi xem code:
- **Short-term memory**: nhớ trong 1 cuộc hội thoại — khi bạn đóng chat là mất (như ghi nhớ trong lúc nói chuyện điện thoại).
- **Long-term memory**: nhớ vĩnh viễn qua nhiều phiên — lưu ở file/database (như sổ tay hay database của công ty).
- **Working memory**: nhớ tạm cho task đang chạy — ví dụ danh sách việc cần làm của task này, xong task là dọn sạch.

<details>
<summary><b>TypeScript Code (Click to expand/collapse)</b></summary>

> 📄 **Code ví dụ:** [`examples/08-5-2-memory-bo-nho-nao.ts`](examples/08-5-2-memory-bo-nho-nao.ts)

</details>

**Ví dụ Implementation:**

<details>
<summary><b>TypeScript Code (Click to expand/collapse)</b></summary>

> 📄 **Code ví dụ:** [`examples/09-5-2-memory-bo-nho-nao.ts`](examples/09-5-2-memory-bo-nho-nao.ts)

</details>

**Best Practices:**
- ✅ Context compression khi cần (nén ngữ cảnh — thay vì giữ 50 tin nhắn cũ nguyên văn, gom lại thành 5 dòng tóm tắt)
- ✅ Prioritize relevant memories (ưu tiên nhớ thứ liên quan đến việc đang làm, bỏ thứ không liên quan)
- ✅ Clear working memory sau task (dọn bộ nhớ tạm sau mỗi task — không dọn là dữ liệu rác chất đống và tốn token)
- ✅ Separate concerns (short/long/working) (tách 3 loại nhớ ra riêng, đừng nhét chung một chỗ)

> **Tóm gọn 1 câu:** Memory = bộ não của AI, chia 3 tầng (ngắn hạn/dài hạn/làm việc); nhớ đúng thứ, đúng lúc, và dọn dẹp sau mỗi task.

---

### 5.3. Context Management (Quản Lý Ngữ Cảnh) - "Hệ Tuần Hoàn"

Mục này giải thích "máu" chảy trong hệ thống như thế nào: context là toàn bộ thông tin model nhìn thấy ở một thời điểm, và context management là việc đảm bảo thông tin đó đúng, đủ, không quá tải.

**Mục đích**: Đảm bảo AI luôn có đúng thông tin tại đúng thời điểm

**5 Cấp Độ Context (theo Anthropic):**

Sơ cấp — 5 cấp này là 5 "lớp thông tin" xếp từ chung đến riêng:
1. System (luật chơi cố định của toàn hệ thống) → 2. Task (nội dung công việc hiện tại) → 3. Domain (kiến thức chuyên ngành) → 4. Chat (lịch sử hội thoại) → 5. Immediate (tin nhắn vừa gửi).

<details>
<summary><b>TypeScript Code (Click to expand/collapse)</b></summary>

> 📄 **Code ví dụ:** [`examples/10-5-3-context-management-quan-ly-ngu-canh.ts`](examples/10-5-3-context-management-quan-ly-ngu-canh.ts)

</details>

**Context Optimization Strategies:**

(Các chiến lược "trả giá ít token hơn cho cùng chất lượng": nén, cache, chọn lọc, sắp xếp ưu tiên.)

<details>
<summary><b>TypeScript Code (Click to expand/collapse)</b></summary>

> 📄 **Code ví dụ:** [`examples/11-5-3-context-management-quan-ly-ngu-canh.ts`](examples/11-5-3-context-management-quan-ly-ngu-canh.ts)

</details>

---


#### Vậy Can Thiệp Vào Đâu?

Phần này trả lời câu hỏi kinh điển của người mới làm RAG: "Code của mình chen vào đâu giữa người dùng và model?" — và câu trả lời là: chen vào **trước khi prompt rời khỏi app của bạn**.

Câu hỏi của bạn: **"Làm sao can thiệp vào giữa prompt và LLM?"**

Đây chính là core của RAG. Luồng thực tế là (đọc sơ đồ từ trên xuống: ① người dùng hỏi → ② code bạn viết đi tìm tài liệu liên quan → ③ ghép tài liệu vào prompt → ④ model trả lời có cơ sở):

```
① User gõ: "BHYT có chi trả bệnh tim không?"
        │
        ▼
② Bạn viết code INTERCEPT prompt này
        │
        ├── Gửi prompt đi SEARCH Vector DB (biến nó thành câu query)
        │      └── Vector DB trả về: [chunk_liên_quan_1, chunk_liên_quan_2, ...]
        │
        ▼
③ Bạn GHÉP retrieved chunks vào prompt gốc:
        │
        │   Prompt cuối tới LLM:
        │   ┌─────────────────────────────────────────────┐
        │   │ System: Dùng thông tin sau để trả lời:      │
        │   │                                             │
        │   │ [Context từ Vector DB]                      │
        │   │ • BHYT chi trả 80-100% chi phí tùy tuyến   │
        │   │ • Bệnh tim mạch thuộc danh mục BHYT        │
        │   │                                             │
        │   │ User: BHYT có chi trả bệnh tim không?      │
        │   └─────────────────────────────────────────────┘
        │
        ▼
④ LLM nhận prompt ĐÃ CÓ context → trả lời chính xác
```

Giải nghĩa từng thuật ngữ trong sơ đồ:
- **Vector DB** = database chuyên lưu "vector" (dãy số biểu diễn ý nghĩa của văn bản) để tra theo ý nghĩa, không cần đúng từng chữ.
- **Chunk** = mẩu tài liệu nhỏ (ví dụ cắt 1 file 50 trang thành từng đoạn ~500 chữ) — tra cứu mẩu nhỏ thì nhanh và khớp hơn cả file.
- **Retrieved chunks** = các mẩu tài liệu mà máy tìm ra được, xem như "tài liệu tham khảo" cho prompt.

<details>
<summary><b>Coding mẫu — 10 dòng là xong (Click để xem)</b></summary>

> 📄 **Code ví dụ:** [`examples/12-vay-can-thiep-vao-au.py`](examples/12-vay-can-thiep-vao-au.py)
</details>

Chốt lại: **Bạn không sửa LLM, bạn sửa PROMPT trước khi gửi.**

> **Tóm gọn 1 câu:** RAG = chặn prompt trước khi nó tới model, tự tra kho tài liệu lấy các đoạn liên quan, ghép vào prompt rồi mới gửi — model không đổi, thông tin đổi.

<br>

#### Làm Sao Để Đoạn Code Đó Tự Động Chạy?

Phần này giải thích 4 cách "cắm" đoạn code RAG trên vào hệ thống thật, từ dễ đến khó — chọn đúng cách theo app bạn đang có.

Có 4 cách, tùy vào thiết lập của bạn:

---

**Cách 1 — Wrapper API (Đơn giản nhất, dùng cho mọi app)**

(Wrapper = "lớp bọc": một server nhỏ đứng giữa hai bên, nắm nhận-g xử lý rồi chuyển tiếp.)

Bạn viết một server nhỏ làm **proxy**, app chat gọi vào proxy này, proxy tự động retrieve context rồi mới gọi LLM.

```
App Chat (bất kỳ) ──► PROXY BẠN VIẾT ──► Ollama API
                          │
                          ├── Nhận prompt từ app
                          ├── Search Vector DB
                          ├── Ghép context vào prompt
                          └── Gửi prompt đã augment tới Ollama
```

(Ollama = phần mềm chạy model AI trên máy bạn, qua địa chỉ localhost:11434; augment = "làm giàu" prompt bằng dữ liệu tìm thêm được.)

<details>
<summary><b>Code mẫu — proxy server bằng Flask (Click để xem)</b></summary>

> 📄 **Code ví dụ:** [`examples/13-lam-sao-e-oan-code-o-tu-ong.py`](examples/13-lam-sao-e-oan-code-o-tu-ong.py)

**Cách dùng:** Trong app chat, thay vì gọi `localhost:11434`, bạn gọi `localhost:5000/api/chat`. Tự động có RAG.
</details>

---

**Cách 2 — Function Wrapper (Dùng trong code Python của bạn)**

<details>
<summary><b>Code mẫu — Function Wrapper (Click để xem)</b></summary>

Nếu bạn tự viết app Python, chỉ cần wrap hàm gọi LLM:

<details>
<summary><b>Python Code (Click to expand/collapse)</b></summary>

> 📄 **Code ví dụ:** [`examples/14-lam-sao-e-oan-code-o-tu-ong.py`](examples/14-lam-sao-e-oan-code-o-tu-ong.py)

</details>
</details>

---

**Cách 3 — Open WebUI (Không cần code)**

Nếu bạn dùng [Open WebUI](https://openwebui.com/), nó đã có sẵn cơ chế:

```
Settings → Documents → Upload file → 
Khi chat: @mention file đó → tự động RAG
```

Hoặc dùng tính năng **Pipeline** của Open WebUI để viết filter middleware.

---

**Cách 4 — LangChain / LlamaIndex (Framework chuyên nghiệp)**

<details>
<summary><b>Code mẫu — LangChain (Click để xem)</b></summary>

> 📄 **Code ví dụ:** [`examples/15-lam-sao-e-oan-code-o-tu-ong.py`](examples/15-lam-sao-e-oan-code-o-tu-ong.py)
</details>

---

**Tóm lại: Bạn chỉ cần chọn 1 trong 4 cách:**

Cách đọc bảng này: mỗi hàng là một cách triển khai; cột "Khi nào dùng" cho biết tình huống phù hợp; cột "Độ khó" — ⭐ càng ít càng dễ.

| Cách | Khi nào dùng | Độ khó |
|------|-------------|--------|
| **Proxy server** | App chat bất kỳ (web, mobile, desktop) | ⭐⭐ |
| **Function wrapper** | Code Python tự viết | ⭐ |
| **Open WebUI** | Đã xài Open WebUI | ⭐ (không code) |
| **LangChain/LlamaIndex** | Production, cần nhiều tính năng | ⭐⭐⭐ |

<br>

> **📌 Key Concepts:**
> - **Semantic Search** — tìm kiếm hiểu ý nghĩa, không chỉ khớp từ khóa. Ví dụ: hỏi "xe 4 bánh chở 7 người" vẫn ra kết quả "xe 7 chỗ" dù không có từ nào trùng.
> - **Vector Embedding** — biến text thành dãy số (vector) để máy tính so sánh. Text nghĩa gần nhau thì dãy số gần nhau.
> - **Similarity** — đo khoảng cách giữa các vector trong không gian nhiều chiều; càng gần càng giống nghĩa.
> - **Chunking** — chia nhỏ documents trước khi embed (ví dụ cắt file 50 trang thành từng đoạn ~500 chữ) để tra cứu khớp hơn.
> - **Vector Database** — loại database chuyên lưu vector và tìm vector gần nhau thật nhanh.

> **Tóm gọn 1 câu:** Context Management = "hệ tuần hoàn" đưa đúng thông tin đúng lúc cho AI — kỹ thuật nền là RAG (chặn prompt, tra kho tài liệu, ghép vào), và bạn có 4 cách cắm RAG vào hệ thống, chọn theo app đang có.

---

### 5.4. Guardrails (Rào Cản) - "Hệ Miễn Dịch"

Mục này giải thích "hệ miễn dịch" của harness: guardrails là các chốt kiểm tra tự động — kịp chặn prompt nguy hiểm đi vào, chặn output sai/không an toàn đi ra.

**Mục đích**: Ngăn chặn hành vi không mong muốn

**Các Loại Guardrails:**

Tóm tắt trước khi xem code, các loại thường gặp gồm:
- **Input guardrail**: soi prompt trước khi cho vào model — chặn từ ngữ cấm, thông tin nhạy cảm (số thẻ, mật khẩu), hoặc prompt injection (kỹ thuật "nhét lệnh giấu" vào câu hỏi để lừa model làm điều ngoài ý muốn).
- **Output guardrail**: soi câu trả lời trước khi đưa ra người dùng — chặn nội dung bậy, code lỗi, dữ liệu sai format.

<details>
<summary><b>TypeScript Code (Click to expand/collapse)</b></summary>

> 📄 **Code ví dụ:** [`examples/16-5-4-guardrails-rao-can-he-mien-dich.ts`](examples/16-5-4-guardrails-rao-can-he-mien-dich.ts)

</details>

**Ví dụ Implementation:**

<details>
<summary><b>TypeScript Code (Click to expand/collapse)</b></summary>

> 📄 **Code ví dụ:** [`examples/17-5-4-guardrails-rao-can-he-mien-dich.ts`](examples/17-5-4-guardrails-rao-can-he-mien-dich.ts)

</details>

> **Tóm gọn 1 câu:** Guardrails = hệ miễn dịch: hai lớp chốt kiểm tra tự động, một lớp soi "vào" (chặn prompt độc/hại), một lớp soi "ra" (chặn trả lời sai/không an toàn).

---

### 5.5. Feedback Loops (Vòng Lặp Phản Hồi) - "Cảm Giác"

Mục này giải thích cách hệ thống "cảm nhận" được mình đang làm tốt hay dở: đo kết quả → sửa → đo lại, lặp liên tục thay vì chờ con người nhìn ra.

**Mục đích**: Tự động học và cải thiện từ kết quả

(Vòng lặp điển hình: chạy task → kiểm tra kết quả bằng code (test tự động, chấm điểm, so quy tắc) → nếu hỏng thì đưa lỗi lại cho agent tự sửa → chạy lại. Giống như trình biên dịch báo lỗi khi bạn bấm build, không phải chờ reviewer đọc cả nghìn dòng.)

<details>
<summary><b>TypeScript Code (Click to expand/collapse)</b></summary>

> 📄 **Code ví dụ:** [`examples/18-5-5-feedback-loops-vong-lap-phan-hoi.ts`](examples/18-5-5-feedback-loops-vong-lap-phan-hoi.ts)

</details>

**Example:**

<details>
<summary><b>TypeScript Code (Click to expand/collapse)</b></summary>

> 📄 **Code ví dụ:** [`examples/19-5-5-feedback-loops-vong-lap-phan-hoi.ts`](examples/19-5-5-feedback-loops-vong-lap-phan-hoi.ts)

</details>

> **Tóm gọn 1 câu:** Feedback loops = "cảm giác" giúp agent biết mình sai ngay: đo kết quả bằng code, sai thì tự sửa rồi chạy lại, không cần người canh chừng.

---

### 5.6. Permissions (Quyền Hạn) - "Xương"

Mục này giải thích "bộ xương" giữ trật tự: quy định AI được làm gì, ở đâu, khi nào — trước cả khi nghĩ tới tools hay prompt.

**Mục đích**: Định nghĩa AI được phép làm gì, ở đâu, khi nào

Ví dụ đời thường: nhân viên mới được cấp chìa khóa phòng nào, mở server nào — đó là permissions. Cho AI quyền "đọc mọi file, chỉ ghi trong thư mục drafts/" là một cấu hình permissions.

<details>
<summary><b>TypeScript Code (Click to expand/collapse)</b></summary>

> 📄 **Code ví dụ:** [`examples/20-5-6-permissions-quyen-han-xuong.ts`](examples/20-5-6-permissions-quyen-han-xuong.ts)

</details>

> **Tóm gọn 1 câu:** Permissions = xương sống phân quyền: khai báo rõ AI được đọc/ghi/xóa gì, ở đâu, khi nào — mặc định là cấm, mở đúng chỗ cần.

---

### 5.7. Orchestration (Điều Phối) - "Hệ Thần Kinh"

Mục này giải thích "hệ thần kinh": ai gọi ai, làm gì trước làm gì sau, khi lỗi thì đi nhánh nào — orchestration là thành phần gắn tất cả lại thành một luồng.

**Mục đích**: Điều phối tất cả các thành phần hoạt động hài hòa

(Ví dụ: user gửi yêu cầu → orchestration gọi agent phân tích → gọi agent viết code → gọi tool chạy test → nếu test hỏng thì quay lại bước sửa. Nó là "chỉ huy dàn nhạc", không tự chơi nhạc nhưng quyết định ai chơi khi nào.)

<details>
<summary><b>TypeScript Code (Click to expand/collapse)</b></summary>

> 📄 **Code ví dụ:** [`examples/21-5-7-orchestration-ieu-phoi-he-than-kinh.ts`](examples/21-5-7-orchestration-ieu-phoi-he-than-kinh.ts)

</details>

> **Tóm gọn 1 câu:** Orchestration = hệ thần kinh điều phối: quyết định thứ tự bước, ai gọi ai, lỗi thì đi hướng nào — thiếu nó thì 6 thành phần kia chỉ là đồ nằm im.

---

### Tích Hợp Tất Cả

Phần này cho thấy 7 thành phần ghép với nhau trong một hệ thống hoàn chỉnh trông như thế nào.

<details>
<summary><b>Tích Hợp Tất Cả (Click to expand/collapse)</b></summary>

> 📄 **Code ví dụ:** [`examples/22-tich-hop-tat-ca.ts`](examples/22-tich-hop-tat-ca.ts)

</details>

> **Tóm gọn 1 câu:** Bảy thành phần không chạy riêng lẻ — code tổng hợp ở file ví dụ cho thấy chúng cắm vào nhau thành một agent hoàn chỉnh.

---

### Tích Hợp Component Với Modules Trong Repo

Phần này nối lý thuyết (7 components ở trên) với thực tế repo này: mỗi component được "hiện thực hóa" bằng module nào trong AI Coding Skills Framework. Đọc xong bạn biết cần mở file nào để xem code thật.

Mỗi thành phần của Harness tương ứng trực tiếp với các module trong **AI Coding Skills Framework**. Đây là cách các component gắn với thực tế ra sao:

```
┌─────────────────────────────────────────────────────────────────────┐
│                    HARNESS → MODULE MAPPING                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────┐      ┌─────────────────────────────────────┐     │
│  │   TOOLS     │ ───► │ 06-decide-tools-mcp                 │     │
│  │  (Tay chân) │      │ Tool selection & MCP integration     │     │
│  └─────────────┘      └─────────────────────────────────────┘     │
│                                                                     │
│  ┌─────────────┐      ┌─────────────────────────────────────┐     │
│  │   MEMORY    │ ───► │ 01-retrieve-memory-knowledge        │     │
│  │  (Bộ não)   │      │ 03-update-memory-store               │     │
│  └─────────────┘      └─────────────────────────────────────┘     │
│                                                                     │
│  ┌─────────────┐      ┌─────────────────────────────────────┐     │
│  │   CONTEXT   │ ───► │ 02-build-context                    │     │
│  │ (Tuần hoàn) │      │ Context building & management       │     │
│  └─────────────┘      └─────────────────────────────────────┘     │
│                                                                     │
│  ┌─────────────┐      ┌─────────────────────────────────────┐     │
│  │ GUARDRAILS  │ ───► │ 05-prompt-builder (Guardrails)      │     │
│  │(Miễn dịch) │      │ 11-evaluation (validation)           │     │
│  └─────────────┘      └─────────────────────────────────────┘     │
│                                                                     │
│  ┌─────────────┐      ┌─────────────────────────────────────┐     │
│  │  FEEDBACK   │ ───► │ 07-workflow (retry, loop patterns)  │     │
│  │ (Cảm giác)  │      │ 11-evaluation (metrics & feedback)  │     │
│  └─────────────┘      └─────────────────────────────────────┘     │
│                                                                     │
│  ┌─────────────┐      ┌─────────────────────────────────────┐     │
│  │ PERMISSIONS │ ───► │ 06-decide-tools-mcp (tool perms)    │     │
│  │   (Xương)   │      │ 10-automation (access control)       │     │
│  └─────────────┘      └─────────────────────────────────────┘     │
│                                                                     │
│  ┌─────────────┐      ┌─────────────────────────────────────┐     │
│  │ ORCHESTRATION│───►│ 07-workflow (workflow engine)         │     │
│  │(Thần kinh)  │      │ 09-multi-agent (agent coordination)  │     │
│  └─────────────┘      │ 04-plan-decompose-task (planning)    │     │
│                        │ 08-task (task management)             │     │
│                        └─────────────────────────────────────┘     │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

#### Bảng Mapping Chi Tiết

Cách đọc bảng này: cột "Component" là 7 mảnh ghép của harness; cột "Analogies" là cách ví von với cơ thể người; cột "Modules trong Repo" là thư mục code thực tế trong framework bạn có thể mở ra xem; cột "Mô tả" nói ngắn gọn module đó làm gì. Ví dụ, hàng đầu tiên: component **Tools** ("tay chân") được hiện thực bằng module `06-decide-tools-mcp`.

| Component | Analogies | Modules trong Repo | Mô tả |
|-----------|-----------|-------------------|-------|
| **Tools** | "Tay chân" | `06-decide-tools-mcp` | Định nghĩa AI có thể dùng công cụ gì, tích hợp MCP |
| **Memory** | "Bộ não" | `01-retrieve-memory-knowledge`, `03-update-memory-store` | Nhớ & truy xuất kiến thức, cập nhật bộ nhớ |
| **Context Management** | "Hệ tuần hoàn" | `02-build-context` | Xây dựng ngữ cảnh phù hợp cho từng task |
| **Guardrails** | "Hệ miễn dịch" | `05-prompt-builder`, `11-evaluation` | Rào cản bảo vệ, kiểm tra đầu vào/đầu ra |
| **Feedback Loops** | "Cảm giác" | `07-workflow`, `11-evaluation` | Vòng lặp phản hồi, retry, đánh giá chất lượng |
| **Permissions** | "Xương" | `06-decide-tools-mcp`, `10-automation` | Phân quyền truy cập tài nguyên |
| **Orchestration** | "Hệ thần kinh" | `07-workflow`, `09-multi-agent`, `04-plan-decompose-task`, `08-task` | Điều phối tất cả thành phần hoạt động hài hòa |

(MCP = Model Context Protocol — giao thức mở để AI gọi tool của bên thứ ba theo chuẩn chung, như "ổ cắm điện thống nhất" cho tools.)

> **Insight**: Prompt Engineering (`05-prompt-builder`) không phải là một component riêng biệt của Harness — nó là **kỹ thuật nền tảng** được tích hợp xuyên suốt nhiều components: System Prompt trong Orchestration, Few-shot trong Context Management, Structured Output trong Guardrails.

> **Tóm gọn 1 câu:** 7 components của harness đều có module code thật trong repo tương ứng — lý thuyết ở trên và thực hành trong framework nối thẳng vào nhau.

---

## 🔭 Toàn Cảnh: Harness Engineering — AI Coding Skills Framework

Phần này vẽ bức tranh "tổng thể một lần cuối": tất cả những gì đã học ở mục 1–5 xếp vào một kiến trúc duy nhất, cùng 15 module của framework. Đọc kỹ sơ đồ ở đây, bạn sẽ không bị lạc khi vào các mục case studies.

### Kiến Trúc Tổng Thể: 7 Components → 15 Modules

Mục này giải thích kiến trúc tổng thể: 7 components học ở mục 5 phân bổ vào 15 module ra sao.

Sơ đồ dưới đây cho thấy **toàn bộ hệ thống Harness Engineering** và cách nó ánh xạ tới **15 modules** trong AI Coding Skills Framework — module `01`–`11` là các giai đoạn pipeline, còn `12`–`15` là mặt phẳng kiểm soát xuyên module mà tất cả đều phụ thuộc vào:

(pipeline = chuỗi công đoạn chạy tuần tự, như dây chuyền sản xuất: lấy dữ liệu → xử lý → trả kết quả. "Mặt phẳng kiểm soát xuyên module" = các module không thuộc bước nào cụ thể, mà là tiêu chuẩn mà MỌI bước phải đạt — ví dụ sandbox hay approval gate dùng ở bất kỳ giai đoạn nào.)

```
╔══════════════════════════════════════════════════════════════════════════════════════╗
║              AI CODING SKILLS FRAMEWORK — TOÀN CẢNH HARNESS ENGINEERING              ║
║                 Architecture Overview: 7 Components → 15 Modules                    ║
╚══════════════════════════════════════════════════════════════════════════════════════╝

                         TIẾN HÓA: 3 KỶ NGUYÊN AI ENGINEERING

 ┌──────────────────────────┐   ┌──────────────────────────┐   ┌──────────────────────┐
 │  PROMPT ENGINEERING      │   │  CONTEXT ENGINEERING     │   │  HARNESS ENGINEERING  │
 │  (2022-2024)             │──►│  (2025)                  │──►│  (2026+)              │
 │  "Cách hỏi cho đúng"     │   │  "Đưa thông tin gì"     │   │  "Thiết kế cả hệ thống"│
 │  Mức kiểm soát: ★☆☆      │   │  Mức kiểm soát: ★★☆     │   │  Mức kiểm soát: ★★★   │
 └──────────────────────────┘   └──────────────────────────┘   └──────────┬───────────┘
                                                                           │
              ┌────────────────────────────────────────────────────────────┘
              ▼

 ┌─────────────────────────────────────────────────────────────────────────────────────┐
 │                              HARNESS — TOÀN BỘ HỆ THỐNG                              │
 │                                                                                      │
 │                         ┌──────────────────────────────────┐                        │
 │                         │     🧠 ORCHESTRATION              │                        │
 │                         │     (Hệ thần kinh — Điều phối)    │                        │
 │                         │                                    │                        │
 │                         │  ┌────────┐ ┌────────┐ ┌────────┐ │                        │
 │                         │  │04-plan │ │07-work │ │08-task │ │                        │
 │                         │  │decom-  │ │ -flow  │ │ (task  │ │                        │
 │                         │  │pose    │ │(work-  │ │ mgmt)  │ │                        │
 │                         │  │(kế     │ │ flow)  │ │        │ │                        │
 │                         │  │hoạch)  │ │        │ │        │ │                        │
 │                         │  └────────┘ └────────┘ └────────┘ │                        │
 │                         │  ┌─────────────────────────────┐  │                        │
 │                         │  │ 09-multi-agent (phối hợp)   │  │                        │
 │                         │  └─────────────────────────────┘  │                        │
 │                         └────────────┬─────────────────────┘                        │
 │                                      │                                               │
 │                                      ▼                                               │
 │                         ┌──────────────────────────────────┐                        │
 │                         │     📚 MEMORY (BỘ NÃO)            │                        │
 │                         │     ─── RAG PIPELINE ───          │                        │
 │                         │                                    │                        │
 │                         │  ┌──────────────────────────────┐ │                        │
 │                         │  │ ① RETRIEVE (01-retrieve)     │ │                        │
 │                         │  │  ┌────────┐ ┌────────┐      │ │                        │
 │                         │  │  │Semantic│ │Keyword │      │ │                        │
 │                         │  │  │Search  │ │BM25    │      │ │                        │
 │                         │  │  │(vector)│ │        │      │ │                        │
 │                         │  │  └────────┘ └────────┘      │ │                        │
 │                         │  │  ┌────────┐ ┌────────┐      │ │                        │
 │                         │  │  │K-Graph │ │Hybrid  │      │ │                        │
 │                         │  │  │Retrieve│ │(RRF)   │      │ │                        │
 │                         │  │  └────────┘ └────────┘      │ │                        │
 │                         │  └──────────────────────────────┘ │                        │
 │                         │  ┌──────────────────────────────┐ │                        │
 │                         │  │ ② RE-RANK + BUILD CONTEXT    │ │                        │
 │                         │  │  ├── Cross-Encoder scoring   │ │                        │
 │                         │  │  └── 02-build-context        │ │                        │
 │                         │  └──────────────────────────────┘ │                        │
 │                         │  ┌──────────────────────────────┐ │                        │
 │                         │  │ ③ UPDATE (03-update-memory)  │ │                        │
 │                         │  └──────────────────────────────┘ │                        │
 │                         └────────────┬─────────────────────┘                        │
 │                                      │                                               │
 │                                      ▼                                               │
 │                         ┌──────────────────────────────────┐                        │
 │                         │     🔄 CONTEXT MANAGEMENT         │                        │
 │                         │     (Hệ tuần hoàn — 5 cấp độ)    │                        │
 │                         │                                    │                        │
 │                         │  ┌──────┐ ┌──────┐ ┌──────┐      │                        │
 │                         │  │Level1│ │Level2│ │Level3│      │                        │
 │                         │  │System│ │Task  │ │Domain│      │                        │
 │                         │  └──────┘ └──────┘ └──────┘      │                        │
 │                         │  ┌──────┐ ┌──────┐               │                        │
 │                         │  │Level4│ │Level5│               │                        │
 │                         │  │Chat  │ │Immed │               │                        │
 │                         │  └──────┘ └──────┘               │                        │
 │                         │  Module: 02-build-context         │                        │
 │                         │  Module: 05-prompt-builder       │                        │
 │                         └────────────┬─────────────────────┘                        │
 │                                      │                                               │
 │            ┌─────────────────────────┼─────────────────────────┐                    │
 │            │                         │                         │                    │
 │            ▼                         ▼                         ▼                    │
 │  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐                 │
 │  │ 🛠️ TOOLS         │  │ 🛡️ GUARDRAILS   │  │ 🔁 FEEDBACK     │                 │
 │  │ (Tay chân)       │  │ (Hệ miễn dịch)   │  │ LOOPS (Cảm giác) │                 │
 │  │                   │  │                   │  │                   │                 │
 │  │ 06-decide-tools   │  │ Input validation │  │ 07-workflow      │                 │
 │  │ MCP integration   │  │ Output validation│  │ (retry patterns) │                 │
 │  │ Tool validation   │  │ Security checks  │  │ 11-evaluation     │                 │
 │  │                   │  │ Prompt injection │  │ (metrics)         │                 │
 │  │                   │  │ detection        │  │ loop/ (cấp cao)  │                 │
 │  └──────────────────┘  └──────────────────┘  └──────────────────┘                 │
 │            │                         │                         │                    │
 │            └─────────────────────────┼─────────────────────────┘                    │
 │                                      │                                               │
 │                                      ▼                                               │
 │                         ┌──────────────────────────────────┐                        │
 │                         │     🔒 PERMISSIONS (Xương)        │                        │
 │                         │                                    │                        │
 │                         │  ┌──────────────┐ ┌────────────┐ │                        │
 │                         │  │ File Access  │ │ Network    │ │                        │
 │                         │  │ Control      │ │ Restrictions│ │                        │
 │                         │  │ (10-auto)    │ │ (06-tools) │ │                        │
 │                         │  └──────────────┘ └────────────┘ │                        │
 │                         │  ┌──────────────────────────────┐ │                        │
 │                         │  │ Cách Ly & Ranh Giới           │ │                        │
 │                         │  │ Thực Thi   → 12-sandbox      │ │                        │
 │                         │  │ Cổng Duyệt  → 15             │ │                        │
 │                         │  └──────────────────────────────┘ │                        │
 │                         └──────────────────────────────────┘                        │
 │                                      │                                               │
 │                                      ▼                                               │
 │                         ┌──────────────────────────────────┐                        │
 │                         │     🤖 LLM + RESPONSE            │                        │
 │                         │     (Mô hình AI + Phản hồi)      │                        │
 │                         │     ← Đầu ra cuối cùng           │                        │
 │                         └──────────────────────────────────┘                        │
 └─────────────────────────────────────────────────────────────────────────────────────┘

                        ════════════════════════════════════
                         MODULES CỐT LÕI TRONG FRAMEWORK

  ┌────────────────────────────────────────────────────────────────────────────────┐
  │  01  ── retrieve-memory-knowledge (Truy xuất & Bộ nhớ — pipeline RAG)          │
  │  02  ── build-context             (Quản lý Context — 5 cấp)                    │
  │  03  ── update-memory-store       (Cập nhật Bộ nhớ — lưu tri thức mới)         │
  │  04  ── plan-decompose-task       (Lập kế hoạch — phân rã nhiệm vụ)            │
  │  05  ── prompt-builder            (Prompt + Guardrail)                         │
  │  06  ── decide-tools-mcp          (Tool + Quyền + MCP)                         │
  │  07  ── workflow                  (Workflow + Vòng Lặp Phản Hồi)               │
  │  08  ── task                      (Quản lý Nhiệm Vụ)                           │
  │  09  ── multi-agent               (Điều Phối Agent)                            │
  │  10  ── automation                (Tự Động Hoá + Kiểm Soát Truy Cập)           │
  │  11  ── evaluation                (Đánh Giá + Số Đo)                           │
  │  12  ── sandbox-execution         (Sandbox — cách ly & ranh giới thực thi)     │
  │  13  ── trajectory-observability  (Trajectory — xương sống quan sát)           │
  │  14  ── compaction-context        (Nén Context — quản lý cửa sổ context)       │
  │  15  ── approval-gates            (Cổng Duyệt — human-in-the-loop)             │
  └────────────────────────────────────────────────────────────────────────────────┘

                         ┌──────────────────────────────────────────────┐
                         │   MẶT PHẲNG KIỂM SOÁT XUYÊN MODULE (12–15)   │
                         │   Không phải một giai đoạn pipeline — mà là    │
                         │   nền tảng mà mọi module ở trên phải đáp ứng. │
                         │                                              │
                         │  12 sandbox      → ranh giới cách ly          │
                         │  13 trajectory   → quan sát được, replay được│
                         │  14 compaction   → kiểm soát context lớn dần  │
                         │  15 approval     → gate thao tác không đảo ngược│
                         │                                              │
                         │  Mỗi module là chuẩn cho câu hỏi của riêng nó;│
                         │  module khác chỉ trỏ tới, không lặp lại.      │
                         └──────────────────────────────────────────────┘

 ══════════════════════════════════════════════════════════════════════════════════

 PHÂN TÍCH MỐI QUAN HỆ:
 - Harness ≈ TOÀN BỘ khung bên ngoài (bao gồm 7 components)
 - RAG Pipeline (01) ≈ 1 phần của MEMORY component — Thành phần "Bộ não"
- 15 modules ≈ 15 kỹ năng cụ thể; module 01–11 là các giai đoạn pipeline, còn
   module 12–15 là mặt phẳng kiểm soát xuyên module mà tất cả đều phụ thuộc vào
 - Prompt Engineering (05) ≈ Kỹ thuật nền tảng, nằm xuyên suốt nhiều components
 - Vòng lặp cải thiện KHÔNG phải là harness/12. Nó nằm ở phần `loop/` cấp cao nhất
   của framework; harness/12 là cách ly sandbox.

 TỶ LỆ BAO PHỦ CỦA TỪNG MODULE TRONG HARNESS:
 ┌─────────────────────────────────────────────────────────────────────────┐
 │  01-retrieve-memory     ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░  85%   │
 │  02-build-context       ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░  70%   │
 │  03-update-memory       ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░░░░░░░  50%   │
 │  04-plan-decompose      ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░░░░░  55%   │
 │  05-prompt-builder      ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░  60%   │
 │  06-decide-tools        ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░  75%   │
 │  07-workflow            ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░  80%   │
 │  08-task                ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░░░░░░  45%   │
 │  09-multi-agent         ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░  65%   │
 │  10-automation          ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░░░░░░░░░  40%   │
 │  11-evaluation          ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░  70%   │
 │  ── mặt phẳng kiểm soát xuyên module — mọi giai đoạn trên đều phụ thuộc ── │
 │  12-sandbox-execution   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░  75%   │
 │  13-trajectory-obser   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░  80%   │
 │  14-compaction-context  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░░  65%   │
 │  15-approval-gates      ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░  70%   │
 └─────────────────────────────────────────────────────────────────────────┘

**Tóm lại:**

Cách đọc bảng này: nó phân biệt "RAG" (một kỹ thuật riêng lẻ bạn đã thấy ở mục 5.3) với "Harness" (toàn bộ hệ thống). Ví dụ, hàng "Phạm vi": RAG chỉ là 1 kỹ thuật lấy tài liệu, còn Harness là cả 7 components + 15 modules.

| Khía cạnh | RAG Pipeline (01) | Harness Engineering (Toàn bộ) |
|-----------|-------------------|-------------------------------|
| **Phạm vi** | 1 kỹ thuật: retrieve + augment | 7 components, 15 modules |
| **Vai trò** | Cung cấp kiến thức cho LLM | Kiểm soát mọi thứ AI có thể làm |
| **Tỷ lệ bao phủ** | ~85% của Memory component | 100% toàn bộ hệ thống |
| **Quan hệ** | Là 1 phần của Memory | Là tổng thể bao hàm RAG |

> **Tóm gọn 1 câu:** RAG chỉ là một mảnh (khoảng 85% của component Memory), còn Harness Engineering là cả tòa nhà 7 components – 15 modules bao trùm nó.

---

## 6. Case Studies Thực Tế

Mục này xem 5 team/sản phẩm thật đã xây harness thế nào. Đọc để thấy lý thuyết ở trên hiện hình trong các hệ thống đã được kiểm chứng.

Các case dưới đây cho thấy các team lớn đã dùng Harness Engineering thế nào để đạt kết quả vượt trội.

---

### 6.1. SWE-agent (Princeton NLP)

Phần này là case study nổi tiếng nhất — chính là nghiên cứu đưa ra con số +64% ở mục 4.1, đây là cách họ làm ra nó.

**Bối cảnh**: team Princeton NLP làm một agent tự sửa GitHub issues.

(GitHub issue = "phiếu ghi lỗi/đề xuất" trên GitHub, nơi người dùng báo rằng code có chỗ hỏng.)

**Vấn đề lúc đầu**:
- Tỉ lệ thành công chỉ 12.5% với cách làm baseline
- Agent hay "đi lạc" trong codebase
- Kết quả tìm kiếm trả về quá nhiều, đọc không xuể
- Không biết đâu mới là thông tin quan trọng

**Giải pháp Harness Engineering**:

<details>
<summary><b>TypeScript Code (Click to expand/collapse)</b></summary>

```typescript
// 1. GIỚI HẠN OUTPUT CỦA TOOLS
const searchTool = {
  name: "search_file",
  execute: async (pattern: string) => {
    const results = await grep(pattern);
    // ❌ Trước: Trả về toàn bộ
    // ✅ Sau: Giới hạn 50 kết quả đầu
    return results.slice(0, 50);
  }
};

// 2. VIEWER THÔNG MINH
const fileViewer = {
  name: "view_file",
  context: {
    showLineNumbers: true,
    contextLines: 100,  // Chỉ hiện 100 dòng tại 1 thời điểm
    highlightRelevant: true
  },
  execute: async (file: string, startLine: number) => {
    // Thay vì load toàn bộ file (có thể 1000+ dòng)
    // Chỉ load 100 dòng xung quanh vùng quan tâm
    return loadFileWindow(file, startLine, 100);
  }
};

// 3. TÍCH HỢP LINTER REALTIME
const editTool = {
  name: "edit_file",
  execute: async (file: string, changes: Change[]) => {
    const newContent = applyChanges(file, changes);
    
    // Tự động check syntax ngay lập tức
    const lintResult = await linter.check(newContent);
    
    if (lintResult.errors.length > 0) {
      // Không cho phép save file có lỗi
      return {
        success: false,
        errors: lintResult.errors,
        message: "Please fix syntax errors before proceeding"
      };
    }
    
    await saveFile(file, newContent);
    return { success: true };
  }
};

// 4. NÉN LỊCH SỬ CHAT
const memoryManager = {
  compressHistory: async () => {
    if (history.length > 20) {
      // Summarize old conversations
      const old = history.slice(0, -10);
      const summary = await summarize(old);
      history = [
        { role: 'system', content: summary },
        ...history.slice(-10)
      ];
    }
  }
};
```

</details>

Bốn ý chính trong code trên, diễn giải bằng lời: (1) **giới hạn output tool** — tìm kiếm chỉ trả tối đa 50 kết quả để agent không bị "chìm trong kết quả"; (2) **viewer thông minh** — mỗi lần chỉ mở 100 dòng quanh vị trí cần xem, không load cả file nghìn dòng; (3) **linter realtime** — linter = công cụ rà lỗi code tự động; mỗi lần agent sửa file là linter rà ngay, có lỗi thì không cho lưu; (4) **nén lịch sử chat** — hội thoại dài hơn 20 tin thì gom 10 tin cũ thành bản tóm tắt, giữ nhẹ đầu vào cho model.

**Kết quả**:
- Tỉ lệ thành công tăng từ **12.5% → 20.5%** (+64%)
- Thời gian xử lý một issue giảm 40%
- Lượng token tốn giảm 30%

**Key Insights**:
> "Không phải mô hình yếu, mà môi trường không được thiết kế tốt"

> **Tóm gọn 1 câu:** SWE-agent không đổi model, chỉ đổi "bộ điều khiển" (giới hạn kết quả tìm, mở file theo cửa sổ, chặn lưu code lỗi, nén lịch sử) — và hiệu suất tăng 64%.

---

### 6.2. Anthropic Multi-Agent Architecture

Phần này giải thích cách Anthropic chia việc cho nhiều agent (multi-agent) thay vì ép một agent làm tất cả — điển hình của nguyên tắc "Chia để trị".

**Bối cảnh**: Anthropic phát triển Claude Code để tạo các ứng dụng phức tạp (games, DAW, etc.)

(DAW = Digital Audio Workstation — phần mềm phóng/soạn nhạc chuyên nghiệp, ví dụ như GarageBand, Logic Pro.)

**Vấn đề ban đầu**:
- Single agent làm quá nhiều việc cùng lúc → overwhelmed (single agent = một AI một mình đảm nhận từ đầu tới cuối; "overwhelmed" = quá tải, lúng túng khi context dài và việc nhiều)
- Agent dừng lại quá sớm (chưa hoàn thành)
- Hoặc tiếp tục quá lâu (không biết khi nào dừng)

**Giải pháp: Multi-Agent Orchestration**

<details>
<summary><b>TypeScript Code (Click to expand/collapse)</b></summary>

> 📄 **Code ví dụ:** [`examples/23-6-2-anthropic-multi-agent-architecture.ts`](examples/23-6-2-anthropic-multi-agent-architecture.ts)

</details>

**Đặc điểm của từng Agent**:

<details>
<summary><b>TypeScript Code (Click to expand/collapse)</b></summary>

> 📄 **Code ví dụ:** [`examples/24-6-2-anthropic-multi-agent-architecture.ts`](examples/24-6-2-anthropic-multi-agent-architecture.ts)

</details>

**Kết quả**:
- Có thể tạo các ứng dụng phức tạp: 2D games, DAW (Digital Audio Workstation)
- Success rate cao hơn 80% so với single-agent
- Code quality tốt hơn nhờ evaluation loop

**Key Insights**:
> "Chia để trị - Mỗi agent tập trung vào một nhiệm vụ cụ thể"

> **Tóm gọn 1 câu:** Thay vì một agent ôm hết cho tới khi quá tải, Anthropic chia việc cho nhiều agent chuyên trách (planner/generator/...) — hiệu quả cao hơn 80% so với một mình một agent.

---

### 6.3. Claude Code Leak - Hệ Thống Harness Siêu Đẳng

Phần này "soi" vào hệ thống harness thật của một sản phẩm nổi tiếng qua mã nguồn bị lộ — xem các kỹ thuật học ở mục 5 được dùng ngoài đời ra sao.

**Bối cảnh**: Vào 2026, source code của Claude Code bị leak vô tình, hé lộ kiến trúc harness cực kỳ tinh vi.

**Phát hiện chính**:

#### A. Quản lý Context 5 Cấp Độ

<details>
<summary><b>A. Quản lý Context 5 Cấp Độ (Click to expand/collapse)</b></summary>

> 📄 **Code ví dụ:** [`examples/25-a-quan-ly-context-5-cap-o.ts`](examples/25-a-quan-ly-context-5-cap-o.ts)

</details>

#### B. Bộ Nhớ 3 Tầng với Auto-Optimization

<details>
<summary><b>B. Bộ Nhớ 3 Tầng với Auto-Optimization (Click to expand/collapse)</b></summary>

> 📄 **Code ví dụ:** [`examples/26-b-bo-nho-3-tang-voi-auto-optimization.ts`](examples/26-b-bo-nho-3-tang-voi-auto-optimization.ts)

</details>

#### C. Phân Quyền Tool Chặt Chẽ

<details>
<summary><b>C. Phân Quyền Tool Chặt Chẽ (Click to expand/collapse)</b></summary>

> 📄 **Code ví dụ:** [`examples/27-c-phan-quyen-tool-chat-che.ts`](examples/27-c-phan-quyen-tool-chat-che.ts)

</details>

#### D. Tone Detection với Regex (!)

<details>
<summary><b>D. Tone Detection với Regex (!) (Click to expand/collapse)</b></summary>

> 📄 **Code ví dụ:** [`examples/28-d-tone-detection-voi-regex.ts`](examples/28-d-tone-detection-voi-regex.ts)

</details>

**Kết quả**:
- Claude Code trở thành một trong những AI coding assistant tốt nhất
- User satisfaction rate > 90%
- Retention rate cao

**Key Insights**:
> "Devil is in the details - Mỗi chi tiết nhỏ trong harness đều được optimize kỹ lưỡng"

> **Tóm gọn 1 câu:** Mã nguồn lộ ra cho thấy sản phẩm hàng đầu thắng bằng từng chi tiết nhỏ: 5 tầng context, bộ nhớ 3 tầng tự tối ưu, phân quyền tool chặt, thậm chí đo "giọng điệu" người dùng bằng regex.

---

### 6.4. Cursor IDE - Harness Tối Ưu Cho Coding

Phần này xem harness của Cursor — sản phẩm phổ biến số 1 trong hỗ trợ code — thắng nhờ những thiết kế nào.

**Đặc điểm nổi bật**:

<details>
<summary><b>TypeScript Code (Click to expand/collapse)</b></summary>

> 📄 **Code ví dụ:** [`examples/29-6-4-cursor-ide-harness-toi-uu-cho.ts`](examples/29-6-4-cursor-ide-harness-toi-uu-cho.ts)

</details>

**Kết quả**:
- Trở thành coding assistant được yêu thích nhất
- NPS (Net Promoter Score) > 70
- Nhiều developers chuyển từ GitHub Copilot sang Cursor

(NPS = điểm đo mức độ "có sẵn lòng giới thiệu sản phẩm cho người khác", thang −100 đến +100; trên 70 là rất cao — đa số phần mềm nằm quanh 30-40.)

> **Tóm gọn 1 câu:** Cursor chứng minh harness hướng "trải nghiệm người dùng" (gợi ý mượt, sửa nhỏ từng bước, sandbox an toàn) là thứ kéo developer từ Copilot qua bên mình.

---

### 6.5. DeepSeek Harness — Micro-Kernel & Trajectory Traceability Framework

Phần này giới thiệu một harness "thế hệ mới" với 2 ý lớn: mọi thứ là plugin (micro-kernel) và mọi hành động đều ghi lại được, tua lại được (trajectory traceability).

DeepSeek Harness đại diện cho thế hệ AI Agent Harness siêu mở rộng dựa trên triết lý **"Agent = Model + Harness"** và **"Everything is a Plugin"**. Được xây dựng trên nền tảng micro-kernel Cordis, DeepSeek Harness biến mọi thành phần của Agent (tools, context, memory, sub-agents) thành các plugins độc lập có thể tháo lắp linh hoạt.

(micro-kernel = lõi chương trình cực nhỏ chỉ làm việc điều phối, còn mọi tính năng đều là plugin cắm vào — như ổ điện đa năng: lõi là ổ cắm, mọi thiết bị là phích. Trajectory = "quỹ đạo": chuỗi đầy đủ các sự kiện agent đã làm trong một phiên.)

#### A. Kiến Trúc Micro-Kernel & Ecosystem Plugin
- **Cordis Core Framework**: Quản lý vòng đời plugin qua 4 giai đoạn (`init`, `attach`, `ready`, `detach`) — tức một plugin có 4 trạng thái rõ ràng: khởi tạo → gắn vào hệ thống → sẵn sàng dùng → tháo ra, như cắm/rút phích điện an toàn.
- **Context Service Registry**: Sử dụng `ctx.provide()` và `ctx.inject()` cho phép các plugins đăng ký và tiêu thụ service độc lập (như logger, llmProvider, memoryStore) — hiểu đơn giản: plugin A "báo" là tôi có service này, plugin B "xin" dùng mà cần biết A tồn tại ở đâu.
- **Xem hướng dẫn chi tiết**: [`harness/07-workflow/cordis-kernel-plugin.md`](./harness/07-workflow/cordis-kernel-plugin.md)

#### B. 4 Runtime Modes Phân Hóa
DeepSeek Harness thiết kế 4 môi trường thực thi chuyên biệt phù hợp với mọi nhu cầu (runtime mode = "chế độ chạy" — cùng một hệ thống nhưng khởi động theo cấu hình khác nhau cho mục đích khác nhau):
1. **Standard Mode**: Full-featured interactive CLI/GUI agent với đầy đủ MCP tools và middleware guardrails. (CLI = giao diện dòng lệnh; GUI = giao diện đồ họa.)
2. **Code Mode**: Chạy qua SDK (`@deepseek-ai/dsh`), gộp nhiều tool calls thành 1 kịch bản code duy nhất, giảm 70-90% latency và token cost. (SDK = bộ thư viện để lập trình viên gọi; latency = độ trễ, thời gian chờ phản hồi.)
3. **Minimal Benchmark Mode**: Môi trường tối giản chỉ có 2 tools (`bash`, `editor`) và minimal prompt để đánh giá năng lực suy luận nguyên bản của LLM — loại bỏ hết "phụ trợ" để đo đúng sức model.
4. **Creator Inspector Mode**: Runtime trực quan hóa timeline, cho phép inspect context state và chỉnh sửa preset agent (inspect = xem ngấu nghiến trạng thái bên trong; preset = bộ cấu hình cài sẵn).

#### C. Trajectory Traceability Engine (Session Event Stream & Branching)
- **Append-Only Event Log**: Mọi diễn biến session (Prompt, Reason, Tool Call, Output) được lưu dưới dạng chuỗi sự kiện không thể sửa đổi (`SessionEventStream`) — append-only = chỉ được ghi thêm, không được sửa/xóa gì đã ghi, như sổ kế toán bút chì đỏ: muốn "sửa" thì ghi thêm dòng bù trừ, nhờ vậy luôn truy ra được chuyện gì đã xảy ra.
- **Time-Travel Replay & Forking**: Khả năng "tạm dừng" session tại bất kỳ bước nào, khôi phục trạng thái context (`replayToStep`) và rẽ nhánh (`forkSession`) để thử nghiệm giải pháp khác mà không làm hỏng session gốc — giống "save game" rồi load lại để thử đường đi khác.
- **Xem hướng dẫn chi tiết**: [`harness/03-update-memory-store/trajectory-fork-replay.md`](./harness/03-update-memory-store/trajectory-fork-replay.md)

#### D. Code Mode SDK & Sandboxed Execution
- Khắc phục nhược điểm latency của multi-turn tool calling truyền thống (multi-turn = mỗi lần gọi 1 tool là 1 vòng qua lại với model, tốn thời gian và token). LLM nhận diện kịch bản phức tạp và sinh ra mã lệnh TypeScript/Python gọi SDK `@deepseek-ai/dsh`.
- Kịch bản chạy trong Node.js `vm` sandbox an toàn (sandbox = "hộp cát": môi trường cách ly, code chạy trong đó không đụng được ra ngoài hệ thống thật — như nhà kính cho trẻ chơi đất, bẩn thì chỉ bẩn trong nhà kính), thực thi hàng chục thao tác ghi/đọc/build trong 1 turn duy nhất.
- **Xem hướng dẫn chi tiết**: [`harness/06-decide-tools-mcp/code-mode-sdk.md`](./harness/06-decide-tools-mcp/code-mode-sdk.md)

#### E. Minimal Benchmark Harness Cho Đánh Giá Năng Lực AI
- Cách ly hoàn toàn nhiễu từ framework phức tạp (nhiễu = đóng góp của tools/ràng buộc làm điểm số không còn phản ánh đúng năng lực model). Cho phép thực hiện đánh giá benchmark (như SWE-bench — bộ đề thi chuẩn gồm hàng nghìn bài sửa lỗi thật trên GitHub) với độ chính xác cao và độ lặp lại tuyệt đối.
- **Xem hướng dẫn chi tiết**: [`harness/11-evaluation/minimal-benchmark-harness.md`](./harness/11-evaluation/minimal-benchmark-harness.md)

> **Tóm gọn 1 câu:** DeepSeek Harness xây harness như "hệ điều hành": lõi nhỏ (micro-kernel), mọi thứ là plugin tháo lắp được, 4 chế độ chạy cho 4 nhu cầu, và mọi hành động đều được ghi log append-only để tua lại/rẽ nhánh bất cứ lúc nào.

---

### Bài Học Chung Từ Các Case Studies

Phần này xếp 5 case studies vào một bảng để thấy: kỹ thuật nào được ai dùng, và đâu là công thức chung.

Cách đọc bảng này: mỗi **hàng** là một kỹ thuật harness (ví dụ "Giới hạn output" = giới hạn số kết quả tool trả về); mỗi **cột** là một case study đã học ở trên; ô có ✅ nghĩa là case đó dùng kỹ thuật này, ô trống nghĩa là không dùng. Ví dụ, ô giao nhau hàng "Multi-agent" × cột "Anthropic" ✅ 3 agents nghĩa là: Anthropic dùng 3 agent chuyên trách.

| Lesson | SWE-agent | Anthropic | Claude Leak | Cursor | DeepSeek Harness |
|--------|-----------|-----------|-------------|--------|------------------|
| **Giới hạn output** | ✅ 50 results max | - | - | - | ✅ Stream limits |
| **Multi-agent** | - | ✅ 3 agents | ✅ Planner/Generator | - | ✅ Cordis Micro-Kernel |
| **Context layers** | ✅ 3 levels | - | ✅ 5 levels | ✅ Smart context | ✅ Service Registry |
| **Memory tiers** | ✅ Compression | - | ✅ 3 tiers | - | ✅ Session Event Stream |
| **Tool permissions** | - | - | ✅ Strict | ✅ Sandbox | ✅ VM Sandbox & SDK |
| **User feedback** | - | ✅ Evaluation | ✅ Tone detection | ✅ Suggestions | ✅ Creator Inspector |
| **Incremental** | - | - | - | ✅ Smart edits | ✅ Code Mode Single-turn |
| **Time-Travel / Fork** | - | - | - | - | ✅ Replay & Branching |

(Hàng "Incremental" = làm việc theo bước nhỏ tăng dần thay vì làm một phát từ đầu tới cuối; "Time-Travel / Fork" = tua lại và rẽ nhánh phiên làm việc, đã giải thích ở 6.5C.)

**Nguyên tắc chung**:
1. ✅ **Constraints enable creativity** - Giới hạn giúp AI tập trung
2. ✅ **Layered architecture** - Chia nhỏ vấn đề
3. ✅ **Feedback loops** - Học từ kết quả
4. ✅ **User-centric design** - Luôn nghĩ về UX
5. ✅ **Obsess over details** - Mọi chi tiết đều quan trọng

> **Tóm gọn 1 câu:** Năm hệ thống thành công tuy khác nhau nhưng dùng chung một công thức: giới hạn cho gọn, chia tầng cho dễ sửa, đo lường để tự học, và chăm chút từng chi tiết cho người dùng.

---

## 7. Nguyên Tắc Thiết Kế Harness

Mục này đưa ra các "quy tắc vàng" khi thiết kế harness: 5 nguyên tắc SOLID (mượn từ kỹ nghệ phần mềm), 10 điều răn, và một design pattern mẫu.

### 7.1. Nguyên Tắc SOLID Cho Harness

(SOLID là bộ 5 nguyên tắc thiết kế phần mềm kinh điển, đặt tên theo chữ cái đầu của 5 nguyên tắc.)

**1. Single Responsibility**
- Mỗi tool chỉ làm một việc duy nhất (ví dụ: tool "search_file" chỉ tìm, không kiêm đọc nội dung)
- Mỗi component có một lý do để thay đổi

**2. Open/Closed**
- Harness mở cho mở rộng (thêm tools, guardrails) — thêm tính năng không phải đập đi làm lại
- Đóng cho sửa đổi (core logic ổn định) — phần lõi không bị phá vỡ mỗi lần thêm thứ mới

**3. Liskov Substitution**
- Tools có thể thay thế cho nhau — đổi tool này ra tool kia mà hệ thống vẫn chạy (ví dụ đổi Google Search sang Bing Search, cùng interface)
- Cùng interface, khác implementation (interface = "hợp đồng" về tên hàm và tham số; implementation = phần code thực hiện bên trong)

**4. Interface Segregation**
- Không ép AI sử dụng tools không cần thiết — agent dịch thuật không cần tool "delete_database"
- Chỉ expose những gì cần (expose = để lộ ra cho AI thấy và gọi được)

**5. Dependency Inversion**
- Depend on abstractions, not implementations (phụ thuộc vào "chỗ hứng" chung chứ không cắm cứng vào một nhà cung cấp — ví dụ code gọi "kho vector chung" chứ không gọi thẳng "Pinecone", sau này đổi Qdrant chỉ thay 1 lớp)
- Dễ dàng swap components (swap = hoán đổi)

> **Tóm gọn 1 câu:** SOLID cho harness = mỗi mảnh làm đúng một việc, thêm thứ mới không phá phần cũ, và thay thế linh hoạt nhờ "hợp đồng" (interface) rõ ràng.

---

### 7.2. The 10 Commandments of Harness Engineering

Mục này là 10 điều răn — 10 câu châm ngôn cần in đầu khi thiết kế harness. Mỗi điều có vế tiếng Anh (dễ nhớ) và lời giải nghĩa tiếng Việt.

```
1. Thou shall LIMIT, not GUIDE
   → Giới hạn những gì AI có thể làm, đừng chỉ hướng dẫn

2. Thou shall VALIDATE, not HOPE
   → Validation mọi input/output, đừng hy vọng AI làm đúng

3. Thou shall DESIGN, not TRAIN
   → Thiết kế môi trường, đừng chỉ train mô hình

4. Thou shall CONSTRAIN, not INSTRUCT
   → Tạo constraints, đừng viết instructions dài dòng

5. Thou shall AUTOMATE, not MANUAL
   → Tự động hóa checks, đừng để user phải check

6. Thou shall FAIL FAST, not SLOW
   → Phát hiện lỗi sớm, đừng để lỗi lan rộng

7. Thou shall LOG EVERYTHING
   → Log mọi action để debug và improve

8. Thou shall ITERATE, not PERFECT
   → Ship và improve, đừng chờ perfect

9. Thou shall MEASURE, not GUESS
   → Measure metrics, đừng đoán

10. Thou shall OBSESS OVER UX
    → User experience là ưu tiên số 1
```

Điểm giống nhau của cả 10 điều: luôn chọn phương án **có thể kiểm chứng bằng máy** (code chặn, code đo) thay vì phương án **dựa vào niềm tin** (lời dặn, phỏng đoán, chờ hoàn hảo).

> **Tóm gọn 1 câu:** 10 điều răn quy về một ý: thay niềm tin bằng cơ chế — giới hạn thay hướng dẫn, kiểm tra thay hy vọng, đo đếm thay đoán mò.

---

### 7.3. The Harness Design Pattern

Mục này đưa ra một "design pattern" — bản thiết kế mẫu có sẵn để bạn chép khung vào dự án của mình thay vì tự vẽ từ đầu.

<details>
<summary><b>7.3. The Harness Design Pattern (Click to expand/collapse)</b></summary>

> 📄 **Code ví dụ:** [`examples/30-7-3-the-harness-design-pattern.ts`](examples/30-7-3-the-harness-design-pattern.ts)

</details>

> **Tóm gọn 1 câu:** Tinh thần chung của mục 7: đừng tin — hãy kiểm chứng bằng hệ thống (giới hạn, xác thực, đo lường, tự động hóa), và dùng bản thiết kế mẫu ở 7.3 để bắt đầu nhanh.

---

## 8. Best Practices

Mục này là "danh sách kiểm tra" (checklist) khi làm thật: 5 mảng hành động nên làm (✅ DO) và nên tránh (❌ DON'T). Giữ nguyên tiếng Anh kèm giải nghĩa tiếng Việt.

### 8.1. Tool Design

(Thiết kế tools — phần "tay chân" ở mục 5.1.)

✅ **DO:**
- Keep tools small and focused — tool nhỏ, làm đúng một việc
- Validate inputs và outputs — kiểm tra dữ liệu vào/ra bằng code
- Provide clear error messages — báo lỗi rõ ràng, có đủ thông tin để sửa
- Make tools idempotent when possible — gọi lại nhiều lần không gây hại thêm
- Include examples in descriptions — ghi ví dụ cách dùng ngay trong mô tả tool để AI đọc hiểu

❌ **DON'T:**
- Create "god tools" that do everything — không làm tool "thần thánh" ôm mọi việc
- Trust AI to validate itself — đừng tin AI tự kiểm tra mình
- Use vague error messages — đừng báo lỗi mơ hồ kiểu "Something went wrong"
- Allow destructive operations without confirmation — thao tác phá hủy (xóa file, xóa database) phải chờ người xác nhận

> **Tóm gọn 1 câu:** Tool tốt = nhỏ, kiểm tra dữ liệu, báo lỗi rõ, gọi lại an toàn; tool xấu = ôm hết việc, tin AI tự soát, lỗi mơ hồ, xóa mà không hỏi.

### 8.2. Memory Management

(Quản lý bộ nhớ — phần "não" ở mục 5.2.)

✅ **DO:**
- Compress context regularly — nén context định kỳ (gom tin nhắn cũ thành tóm tắt)
- Prioritize relevant information — ưu tiên giữ thông tin liên quan
- Clear working memory after tasks — dọn bộ nhớ tạm sau mỗi task
- Use tiered storage (hot/warm/cold) — lưu theo tầng độ "nóng": hay dùng để gần, ít dùng lưu xa (giống data nóng/lạnh trong data engineering)

❌ **DON'T:**
- Keep entire conversation history — đừng giữ nguyên vẹn toàn bộ hội thoại
- Load unnecessary data — đừng nạp dữ liệu không cần
- Mix different types of memory — đừng trộn lẫn 3 loại nhớ
- Forget to clean up — đừng quên dọn dẹp

> **Tóm gọn 1 câu:** Bộ nhớ tốt = nén thường xuyên, giữ thứ liên quan, dọn sau mỗi task, phân tầng lưu trữ; bộ nhớ xấu = giữ hết mọi thứ rồi để nó "óc" (hao token) và loạn.

### 8.3. Context Building

(Xây dựng context — phần "hệ tuần hoàn" ở mục 5.3.)

✅ **DO:**
- Layer context by priority — xếp context thành từng lớp theo độ ưu tiên (quan trọng nhất ở đầu)
- Include only relevant information — chỉ đưa thông tin liên quan
- Monitor token usage — theo dõi mức tiêu thụ token liên tục
- Compress when approaching limits — sắp chạm giới hạn context window thì nén ngay

❌ **DON'T:**
- Include everything — đừng nhét mọi thứ vào
- Ignore token limits — đừng coi thường giới hạn token (vượt là model "quên" phần đầu)
- Use static context — đừng dùng context tĩnh không đổi theo từng tình huống
- Forget immediate context — đừng bỏ sót thông tin vừa phát sinh (tin nhắn mới nhất, lỗi vừa gặp)

> **Tóm gọn 1 câu:** Xây context như xếp ba lô: thứ cần nhất để trên cùng, chỉ mang thứ cần dùng, canh trọng lượng (token) và gom bớt khi sắp quá tải.

### 8.4. Guardrails

(Rào cản — phần "hệ miễn dịch" ở mục 5.4.)

✅ **DO:**
- Validate at multiple layers — kiểm tra ở nhiều tầng (từ chối prompt, từ chối output)
- Check both input and output — soi cả đầu vào lẫn đầu ra
- Fail fast and clearly — lỗi thì dừng sớm và nói rõ lý do
- Log all violations — ghi log mọi lần vi phạm để phân tích sau

❌ **DON'T:**
- Rely only on prompts — đừng dựa vào lời dặn trong prompt làm rào cản duy nhất (AI có thể bỏ qua)
- Skip validation steps — đừng bỏ bước kiểm tra cho nhanh
- Hide errors from users — đừng giấu lỗi khỏi người dùng
- Trust without verifying — đừng tin mà không kiểm chứng

> **Tóm gọn 1 câu:** Guardrail tốt = nhiều tầng kiểm tra, soi cả vào lẫn ra, dừng sớm, log đầy đủ; rào cản duy nhất bằng lời dặn trong prompt thì không đáng tin.

### 8.5. Testing Harness

(Kiểm thử chính harness — tức kiểm tra xem "bộ khung" của bạn có hoạt động đúng không.)

<details>
<summary><b>8.5. Testing Harness (Click to expand/collapse)</b></summary>

> 📄 **Code ví dụ:** [`examples/31-8-5-testing-harness.ts`](examples/31-8-5-testing-harness.ts)

</details>

> **Tóm gọn 1 câu:** Harness cũng là code nên cũng phải được kiểm thử — ví dụ ở file ví dụ cho thấy cách test xem tools, guardrails và permissions có chặn đúng như thiết kế không.

---

## 9. Công Cụ và Framework

Mục này giới thiệu "hộp đồ nghề": các framework dựng agent và các tool hỗ trợ theo từng nhu cầu, kèm khung khởi động (starter template).

### 9.1. Frameworks Phổ Biến

(Framework = bộ khung code viết sẵn: bạn lắp logic vào, nó lo phần móng như gọi model, quản lý hội thoại, chạy tools.)

**LangChain / LangGraph**

(LangChain = framework đa năng nhất để nối model với tools/dữ liệu; LangGraph = phiên bản vẽ workflow dạng đồ thị — mỗi bước là một node, cho phép rẽ nhánh và lặp.)

<details>
<summary><b>TypeScript Code (Click to expand/collapse)</b></summary>

> 📄 **Code ví dụ:** [`examples/32-9-1-frameworks-pho-bien.ts`](examples/32-9-1-frameworks-pho-bien.ts)

</details>

**AutoGen (Microsoft)**

(AutoGen = framework chuyên về nhiều agent nói chuyện với nhau để giải quyết việc — như một nhóm chat có nhiều chuyên viên.)

<details>
<summary><b>Python Code (Click to expand/collapse)</b></summary>

> 📄 **Code ví dụ:** [`examples/33-9-1-frameworks-pho-bien.py`](examples/33-9-1-frameworks-pho-bien.py)

</details>

**CrewAI**

(CrewAI = framework đóng gói theo kiểu "đội làm việc": mỗi agent có vai (role), mục tiêu (goal), và backstory (hồ sơ nền) — dễ mô tả tổ chức.)

<details>
<summary><b>Python Code (Click to expand/collapse)</b></summary>

> 📄 **Code ví dụ:** [`examples/34-9-1-frameworks-pho-bien.py`](examples/34-9-1-frameworks-pho-bien.py)

</details>

> **Tóm gọn 1 câu:** Ba framework đại diện cho 3 phong cách: LangChain/LangGraph linh hoạt theo workflow, AutoGen mạnh về agent hội thoại với nhau, CrewAI dễ dùng theo kiểu "giao đội việc".

---

### 9.2. Công Cụ Hỗ Trợ

Mục này là "danh bạ phụ tùng": 4 nhóm công cụ, mỗi nhóm giải quyết một vấn đề của harness.

**Vector Databases** (kho dữ liệu tìm theo ý nghĩa — phục vụ RAG):
- Pinecone
- Chroma
- Weaviate
- Qdrant

**Monitoring & Logging** (theo dõi và ghi log: xem mỗi request tốn bao nhiêu token, chạy chậm ở đâu, lỗi gì):
- LangSmith
- Weights & Biases
- Helicone
- OpenLLMetry

**Guardrails** (thư viện sẵn làm rào cản kiểm tra input/output):
- Guardrails AI
- NeMo Guardrails (NVIDIA)
- LlamaGuard (Meta)

**Testing** (kiểm thử prompt và chất lượng đầu ra tự động):
- PromptFoo
- Deepeval
- Ragas

> **Tóm gọn 1 câu:** Bạn không phải tự làm mọi thứ từ con số không: có sẵn kho vector (cho RAG), công cụ giám sát (cho log/đo), thư viện guardrail (cho rào cản) và công cụ test (kiểm thử prompt) — chọn theo nhu cầu từng mảng.

---

### 9.3. Starter Template

Mục này cho bạn một "khung nhà mẫu" — template khởi động ghép sẵn các thành phần cơ bản, để dự án đầu tiên không phải bắt đầu từ file trắng.

<details>
<summary><b>9.3. Starter Template (Click to expand/collapse)</b></summary>

> 📄 **Code ví dụ:** [`examples/35-9-3-starter-template.ts`](examples/35-9-3-starter-template.ts)

</details>

> **Tóm gọn 1 câu:** Framework chọn 1 để dựng khung, công cụ hỗ trợ bổ sung từng mảng (tìm kiếm, giám sát, rào cản, kiểm thử), còn starter template cho bạn khởi động có sẵn móng.

---

## 10. Tương Lai Của Harness Engineering

Mục này nhìn về phía trước: 5 xu hướng sắp tới, các thử thách còn phải vượt, và lời khuyên để bạn không bị bỏ lại.

### 10.1. Xu Hướng 2026-2028

**1. Self-Optimizing Harnesses**
- Harness tự động điều chỉnh parameters (parameters = các thông số cấu hình, ví dụ ngưỡng nén context, số lượng kết quả tìm kiếm tối đa)
- A/B testing tự động (A/B testing = chạy 2 phiên bản cho 2 nhóm người dùng cùng lúc để so xem bản nào tốt hơn)
- Continuous learning from usage

**2. Harness-as-a-Service**
- Cloud platforms cung cấp pre-built harnesses (pre-built = dựng sẵn, thuê là dùng)
- Plug-and-play harness components
- Marketplace cho harness templates (marketplace = chợ mua bán mẫu dựng sẵn)

**3. Visual Harness Builders**
- No-code tools để design harness (no-code = thiết kế bằng kéo-thả, không cần viết code)
- Visual workflow editors
- Drag-and-drop tool composition

**4. Cross-Model Harnesses**
- Một harness chạy trên nhiều models
- Automatic model switching based on task
- Cost-optimized model routing (routing = điều hướng: việc khó chạy model mạnh, việc dễ chạy model rẻ)

**5. Regulatory Compliance Harnesses**
- Built-in GDPR, HIPAA compliance (GDPR = luật bảo vệ dữ liệu cá nhân của EU; HIPAA = luật bảo vệ dữ liệu y tế của Mỹ; compliance = tuân thủ luật)
- Audit trails tự động (audit trail = "vệt kiểm toán": hồ sơ ghi lại ai đã làm gì, khi nào — phục vụ thanh tra)
- Explainability baked in (explainability = giải thích được: hệ thống trả lời được "vì sao AI đưa ra kết quả này")

> **Tóm gọn 1 câu:** 5 năm tới harness sẽ tự tối ưu hóa, được bán như dịch vụ, dựng bằng kéo-thả, chạy đa model, và tích hợp sẵn việc tuân thủ pháp luật.

---

### 10.2. Thách Thức Phía Trước

Mục này cân bằng lại bức tranh "hồng" ở trên bằng những khó khăn thật, chia theo 3 nhóm: kỹ thuật, kinh doanh, nghiên cứu.

**Technical Challenges:**
- Standardization across platforms (standardization = chuẩn hóa: mỗi platform một kiểu, chưa có chuẩn chung)
- Interoperability between harnesses (interoperability = khả năng các harness của bên khác "nói chuyện" được với nhau)
- Performance optimization at scale
- Security và privacy

**Business Challenges:**
- ROI measurement (ROI = Return on Investment, tỷ lệ "bỏ 1 đồng thu về bao nhiêu")
- Team skill gaps (đội ngũ còn thiếu kỹ năng mới)
- Legacy system integration (legacy system = hệ thống cũ đang chạy, khó ghép với công nghệ mới)
- Changing regulations

**Research Challenges:**
- Optimal harness architecture patterns
- Automated harness generation
- Harness testing methodologies
- Cross-domain transferability (một harness xây cho lĩnh vực này có dùng lại được cho lĩnh vực khác không)

> **Tóm gọn 1 câu:** Còn 3 hàng rào: kỹ thuật (thiếu chuẩn chung), kinh doanh (đo được lời chưa, đội ngũ có đủ không) và nghiên cứu (chưa có "công thức" harness tối ưu).

---

### 10.3. Lời Khuyên Cho Tương Lai

Mục này là 5 gợi ý hành động — đọc xong làm ngay được, không nói suông.

```
1. Start Simple
   → Đừng over-engineer từ đầu (over-engineer = làm quá mức cần thiết, thêm thứ chưa cần)
   → Build MVP harness first (MVP = Minimum Viable Product, bản nhỏ nhất dùng được)

2. Measure Everything
   → Track metrics từ ngày 1 (metrics = các con số đo lường, ví dụ tỉ lệ thành công, token/tuần)
   → Data-driven optimization

3. Stay Updated
   → Field đang phát triển nhanh
   → Follow best practices

4. Share Knowledge
   → Open source harness components
   → Build community

5. Think Long-term
   → Harness là infrastructure
   → Invest in maintainability (maintainability = khả năng bảo trì về sau)
```

> **Tóm gọn 1 câu:** Lời khuyên cốt lõi: bắt đầu nhỏ, đo từ ngày đầu, cập nhật liên tục, chia sẻ cùng cộng đồng, và coi harness là hạ tầng dài hạn chứ không phải thí nghiệm ngắn hạn.

---

## 11. Tài Liệu Tham Khảo

Mục này là nguồn để đào sâu: bài báo nghiên cứu, framework/công cụ, cộng đồng, blog và khóa học. Chỉ cần 2-3 nguồn đầu tiên cũng đủ để bắt đầu.

### Papers & Research

(Paper = bài báo nghiên cứu học thuật, thường đăng trên arXiv — kho lưu trữ bài nghiên cứu mở miễn phí.)

1. **SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering**
   - Princeton NLP Lab
   - https://arxiv.org/abs/2405.15793

2. **The Rise of AI Agents and the Importance of Harness Engineering**
   - Mitchell Hashimoto, HashiCorp
   - https://www.youtube.com/watch?v=example

3. **Building Reliable AI Agents with Guardrails**
   - Anthropic Research
   - https://www.anthropic.com/research

> **Tóm gọn 1 câu:** Paper SWE-agent ở trên là nguồn gốc của con số +64% được viện dẫn khắp tài liệu.

### Frameworks & Tools

1. **LangChain** - https://langchain.com
2. **LangGraph** - https://langchain-ai.github.io/langgraph/
3. **AutoGen** - https://microsoft.github.io/autogen/
4. **CrewAI** - https://www.crewai.com
5. **Guardrails AI** - https://www.guardrailsai.com

> **Tóm gọn 1 câu:** 5 framework nêu ở mục 9 đều có trang chủ với tài liệu hướng dẫn tại các link trên.

### Communities

(Cộng đồng nơi hỏi đáp và theo dõi tin tức nhanh nhất.)

1. **LangChain Discord** - Active community
2. **r/LangChain** - Reddit discussions
3. **AI Engineers** - Slack community
4. **HuggingFace Forums** - Technical discussions

> **Tóm gọn 1 câu:** Kẹt kỹ thuật thì hỏi 4 cộng đồng trên — Discord và Reddit là nơi phản hồi nhanh nhất.

### Blogs & Resources

1. **Anthropic Blog** - https://www.anthropic.com/news
2. **OpenAI Cookbook** - https://cookbook.openai.com
3. **LangChain Blog** - https://blog.langchain.dev
4. **Mitchell Hashimoto's Blog** - https://mitchellh.com

> **Tóm gọn 1 câu:** 4 blog trên là nơi công bố kỹ thuật mới trước tiên — đặc biệt OpenAI Cookbook có code mẫu chép được dùng ngay.

### Courses & Tutorials

1. **DeepLearning.AI - Building AI Agents**
2. **LangChain Academy**
3. **Anthropic Prompt Engineering**
4. **Microsoft AutoGen Tutorial**

> **Tóm gọn 1 câu:** Nếu chỉ đọc một thứ, hãy đọc paper SWE-agent của Princeton — nó là nền tảng thực nghiệm của toàn bộ tài liệu này.

---

**Kết Luận**

Harness Engineering không chỉ là một xu hướng công nghệ — nó là sự chuyển đổi góc nhìn trong cách chúng ta xây dựng ứng dụng AI. Khi các mô hình AI ngày càng mạnh và dần trở thành "hàng hóa phổ thông", khả năng thiết kế một harness tốt sẽ là yếu tố quyết định thành công.

> **"The model thinks. The harness shapes what it thinks about. And the harness determines the quality of the final output."**
> (Tạm dịch: "Model là người suy nghĩ. Harness định hình nó suy nghĩ về điều gì. Và harness quyết định chất lượng đầu ra cuối cùng.")

Hãy bắt đầu từ hôm nay — không cần hoàn hảo, chỉ cần bắt đầu. Cứ build, đo lường, học hỏi rồi cải thiện dần. Harness Engineering là một hành trình, không phải đích đến.

> **Tóm gọn 1 câu:** Trong thế giới model ai cũng có, người thắng cuộc là người xây harness tốt nhất — nên bắt đầu hôm nay, nhỏ thôi, nhưng bắt đầu.

**Happy Building! 🚀**

---

**Ngày cập nhật:** 16/10/2026  
**Tác giả:** AI Knowledge Repository
