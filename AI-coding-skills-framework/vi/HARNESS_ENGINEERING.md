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

---

## 1. Giới Thiệu

Trong kỷ nguyên AI, các mô hình ngôn ngữ lớn (LLM) phát triển rất nhanh — từ GPT-3, GPT-4, Claude tới Gemini, model nào cũng ngày càng thông minh hơn. Nhưng có một câu hỏi đáng suy nghĩ: **cùng một model, sao có ứng dụng chạy rất tốt, có ứng dụng lại chưa hiệu quả?**

Câu trả lời nằm ở **Harness Engineering** — thay vì cố làm model giỏi hơn, bạn xây nguyên **hệ sinh thái quanh nó**: tools, permissions, memory, feedback loops, guardrails, quản lý context.

### Bối Cảnh

Khi Mitchell Hashimoto (người sáng lập HashiCorp, tác giả Terraform) nói *"Prompt Engineering đã chết"* và đưa ra khái niệm **Harness Engineering**, ông đã mở ra một góc nhìn mới về cách làm ứng dụng AI. Thay vì cố viết prompt thật hay, ta tập trung xây hẳn một hệ thống để AI làm việc hiệu quả.

### Mục Đích Của Tài Liệu

Tài liệu này giúp bạn có cái nhìn toàn diện về Harness Engineering, gồm:
- Định nghĩa và triết lý cốt lõi
- So sánh với các kỹ thuật trước đó (Prompt Engineering, Context Engineering)
- Các thành phần và nguyên tắc thiết kế
- Case studies từ các công ty hàng đầu (Princeton NLP, Anthropic)
- Best practices và hướng dẫn triển khai thực tế

---

## 2. Harness Engineering Là Gì?

### Định Nghĩa

**Harness Engineering** là cách xây nguyên **"môi trường sống" cho một model AI** — gồm tools, quyền truy cập, memory, feedback loops, guardrails, quản lý context — thay vì can thiệp vào bản thân model.

Nói một cách đơn giản:
- **Mô hình AI** là thứ **suy nghĩ**
- **Harness** là thứ mà AI **suy nghĩ về**
- Và chính **Harness** mới quyết định **chất lượng đầu ra cuối cùng**

### Triết Lý Cốt Lõi

> *"Mỗi khi agent mắc lỗi, bạn không cầu nguyện nó làm tốt hơn lần sau – bạn xây dựng một giải pháp hệ thống để nó không bao giờ mắc lỗi đó nữa"*

Triết lý này nhấn mạnh vào:

1. **Systematic Solutions over Prayers**: Thay vì hy vọng AI sẽ "học" từ lỗi, bạn xây dựng cơ chế hệ thống ngăn chặn lỗi đó tái diễn.

2. **Infrastructure over Instructions**: Thay vì viết prompt dài dòng hướng dẫn AI làm gì, bạn xây dựng cơ sở hạ tầng hạn chế những gì AI có thể làm.

3. **Design over Training**: Thay vì fine-tune mô hình, bạn thiết kế môi trường hoạt động của mô hình.

### Ví Dụ Minh Họa

Hãy tưởng tượng bạn có một AI coding assistant:

**❌ Cách tiếp cận cũ (Prompt Engineering):**
```
"Hãy viết code Python. Đảm bảo code của bạn không có lỗi cú pháp. 
Kiểm tra kỹ trước khi trả về. Nếu có lỗi, hãy sửa..."
```

**✅ Cách tiếp cận mới (Harness Engineering):**

<details>
<summary><b>JavaScript Code (Click to expand/collapse)</b></summary>

> 📄 **Code ví dụ:** [`examples/01-vi-du-minh-hoa.js`](examples/01-vi-du-minh-hoa.js)

</details>

Trong ví dụ trên, thay vì "nhờ" AI cẩn thận giúp mình, bạn xây hẳn một hệ thống **không cho phép** AI trả về code bị lỗi.

### So Sánh Với Các Khái Niệm Khác

| Khía cạnh | Prompt Engineering | Context Engineering | Harness Engineering |
|-----------|-------------------|---------------------|---------------------|
| **Focus** | Cách hỏi | Dữ liệu đầu vào | Toàn bộ hệ thống |
| **Mục tiêu** | Câu prompt tốt hơn | Context phù hợp hơn | Môi trường tốt hơn |
| **Ví dụ** | Viết email | Đính kèm file | Thiết kế văn phòng + quy trình |
| **Kiểm soát** | Thấp | Trung bình | Cao |
| **Tính bền vững** | Thấp | Trung bình | Cao |

---

## 3. Ba Giai Đoạn Tiến Hóa Của Kỹ Nghệ AI

Để hiểu rõ hơn về Harness Engineering, mình cùng nhìn lại quá trình làm AI đã đi qua những chặng nào nhé:

### 3.1. Prompt Engineering (2022-2024)

**Focus**: *"Hỏi AI thế nào cho đúng?"*

**Đặc điểm:**
- Tập trung vào việc viết câu prompt tốt
- Sử dụng các kỹ thuật: few-shot learning, chain-of-thought, role-playing
- Phụ thuộc nhiều vào "nghệ thuật" viết prompt

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

---

### 3.2. Context Engineering (2025)

**Focus**: *"Đưa thông tin gì để AI trả lời tốt?"*

**Đặc điểm:**
- Tập trung vào việc cung cấp đúng dữ liệu đầu vào
- Sử dụng RAG (Retrieval Augmented Generation)
- Quản lý context window hiệu quả
- Tích hợp knowledge bases

**Ví dụ:**

<details>
<summary><b>JavaScript Code (Click to expand/collapse)</b></summary>

> 📄 **Code ví dụ:** [`examples/02-3-2-context-engineering-2025.js`](examples/02-3-2-context-engineering-2025.js)

</details>

**Ưu điểm:**
- Cải thiện độ chính xác
- Giảm hallucination
- Có thể scale với dữ liệu lớn

**Hạn chế:**
- Vẫn phụ thuộc vào chất lượng context
- Chưa kiểm soát được hành vi của AI
- Khó xử lý các tình huống phức tạp

**So sánh:** Giống như đính kèm đúng file vào email - bạn cung cấp đủ thông tin cần thiết.

---

### 3.3. Harness Engineering (2026+)

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
- Dễ debug và maintain
- Có thể mở rộng và tái sử dụng
- Kết quả ổn định và đáng tin cậy

**So sánh:** Giống như thiết kế cả văn phòng và quy trình làm việc - bạn tạo ra một hệ sinh thái hoàn chỉnh.

---

### So Sánh Tổng Quan

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

### Insight Quan Trọng

> **"Prompt Engineering chưa chết, nhưng nó không còn đủ"**

Mỗi giai đoạn không thay thế hoàn toàn giai đoạn trước, mà bổ sung thêm một layer kiểm soát:
- Bạn vẫn cần **prompt tốt** (Prompt Engineering)
- Bạn vẫn cần **context phù hợp** (Context Engineering)
- Nhưng bạn cần thêm **hệ thống hoàn chỉnh** (Harness Engineering)

---

## 4. Tại Sao Harness Engineering Quan Trọng?

### 4.1. Tối Ưu Hiệu Suất Vượt Trội

**Nghiên cứu từ Princeton NLP** (paper SWE-agent) đã chứng minh một phát hiện đột phá:

> Chỉ cần thay đổi cách thiết kế **"giao diện/môi trường"** (ACI - Agent-Computer Interface), hiệu suất của AI có thể **tăng tới 64%** mà không cần nâng cấp mô hình.

**Kết quả thực nghiệm:**

| Cách tiếp cận | Success Rate | Improvement |
|---------------|--------------|-------------|
| Baseline (no harness) | 12.5% | - |
| With optimized harness | 20.5% | +64% |

**Điều này nghĩa là gì?**
- Thiết kế harness đôi khi còn quan trọng hơn chọn model
- Lợi nhuận trên công sức bỏ ra cao hơn hẳn so với train/fine-tune model mới
- Làm được ngay, không cần tài nguyên khủng

---

### 4.2. Mô Hình Chỉ Là Công Cụ, Hệ Thống Mới Quyết Định Kết Quả

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

**Ví dụ thực tế:**

Cùng một mô hình Claude 3.5 Sonnet:
- **Cursor IDE**: Rất hiệu quả trong coding
- **Random chatbot**: Không tốt lắm

➜ **Điều khác biệt?** Harness design của Cursor!

---

### 4.3. Kiểm Soát và Đáng Tin Cậy

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

---

### 4.4. Scalability và Maintainability

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

---

### 4.5. Giảm Chi Phí Đáng Kể

**Cost Savings từ Harness Engineering:**

1. **Giảm token usage**
   - Context compression
   - Smart caching
   - Efficient tool calling
   - **Tiết kiệm: 40-60% cost**

2. **Giảm error rate**
   - Automatic validation
   - Built-in guardrails
   - **Giảm: 70-80% failed requests**

3. **Tăng development speed**
   - Reusable components
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

---

### 4.6. Competitive Advantage

Khi các model AI na ná nhau, **Harness Engineering chính là con hào cạnh tranh** của bạn:

- **Anthropic**: Harness siêu đẳng (theo leak code của Claude)
- **Cursor**: Harness tối ưu cho coding
- **Perplexity**: Harness tốt cho search & research

➜ Đây là lý do tại sao họ dẫn đầu thị trường!

---

### Tóm Lại

Harness Engineering quan trọng vì:

1. ✅ **Tăng hiệu suất 64%+** (theo nghiên cứu Princeton)
2. ✅ **Tạo competitive advantage** khi mô hình trở thành commodity
3. ✅ **Kiểm soát và đáng tin cậy** hơn nhiều
4. ✅ **Scale và maintain dễ dàng**
5. ✅ **Tiết kiệm 40-60% chi phí**
6. ✅ **Tăng tốc development 3-5x**

> **"In the age of AI commoditization, your harness is your moat"**

---

## 5. Các Thành Phần Cốt Lõi Của Harness

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

**Mục đích**: Định nghĩa những gì AI có thể **làm**

**Ví dụ:**

<details>
<summary><b>TypeScript Code (Click to expand/collapse)</b></summary>

> 📄 **Code ví dụ:** [`examples/07-5-1-tools-cong-cu-tay-chan.ts`](examples/07-5-1-tools-cong-cu-tay-chan.ts)

</details>

**Best Practices:**
- ✅ Giới hạn scope của mỗi tool (single responsibility)
- ✅ Validation đầu vào và đầu ra
- ✅ Clear error messages
- ✅ Idempotent khi có thể
- ❌ Tránh tools quá mạnh (e.g., "execute_any_command")

---

### 5.2. Memory (Bộ Nhớ) - "Não"

**Mục đích**: Quản lý thông tin AI cần **nhớ**

**3 Loại Memory:**

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
- ✅ Context compression khi cần
- ✅ Prioritize relevant memories
- ✅ Clear working memory sau task
- ✅ Separate concerns (short/long/working)

---

### 5.3. Context Management (Quản Lý Ngữ Cảnh) - "Hệ Tuần Hoàn"

**Mục đích**: Đảm bảo AI luôn có đúng thông tin tại đúng thời điểm

**5 Cấp Độ Context (theo Anthropic):**

<details>
<summary><b>TypeScript Code (Click to expand/collapse)</b></summary>

> 📄 **Code ví dụ:** [`examples/10-5-3-context-management-quan-ly-ngu-canh.ts`](examples/10-5-3-context-management-quan-ly-ngu-canh.ts)

</details>

**Context Optimization Strategies:**

<details>
<summary><b>TypeScript Code (Click to expand/collapse)</b></summary>

> 📄 **Code ví dụ:** [`examples/11-5-3-context-management-quan-ly-ngu-canh.ts`](examples/11-5-3-context-management-quan-ly-ngu-canh.ts)

</details>

---


#### Vậy Can Thiệp Vào Đâu?

Câu hỏi của bạn: **"Làm sao can thiệp vào giữa prompt và LLM?"**

Đây chính là core của RAG. Luồng thực tế là:

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

<details>
<summary><b>Coding mẫu — 10 dòng là xong (Click để xem)</b></summary>

> 📄 **Code ví dụ:** [`examples/12-vay-can-thiep-vao-au.py`](examples/12-vay-can-thiep-vao-au.py)
</details>

Chốt lại: **Bạn không sửa LLM, bạn sửa PROMPT trước khi gửi.**

<br>

#### Làm Sao Để Đoạn Code Đó Tự Động Chạy?

Câu hỏi thực tế là: **"Tôi có code rồi, nhưng làm sao để nó tự chạy giữa prompt và LLM?"**

Có 4 cách, tùy vào thiết lập của bạn:

---

**Cách 1 — Wrapper API (Đơn giản nhất, dùng cho mọi app)**

Bạn viết một server nhỏ làm **proxy**, app chat gọi vào proxy này, proxy tự động retrieve context rồi mới gọi LLM.

```
App Chat (bất kỳ) ──► PROXY BẠN VIẾT ──► Ollama API
                          │
                          ├── Nhận prompt từ app
                          ├── Search Vector DB
                          ├── Ghép context vào prompt
                          └── Gửi prompt đã augment tới Ollama
```

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

| Cách | Khi nào dùng | Độ khó |
|------|-------------|--------|
| **Proxy server** | App chat bất kỳ (web, mobile, desktop) | ⭐⭐ |
| **Function wrapper** | Code Python tự viết | ⭐ |
| **Open WebUI** | Đã xài Open WebUI | ⭐ (không code) |
| **LangChain/LlamaIndex** | Production, cần nhiều tính năng | ⭐⭐⭐ |

<br>

> **📌 Key Concepts:**
> - **Semantic Search** hiểu ý nghĩa, không chỉ khớp từ khóa
> - **Vector Embedding** biến text thành dãy số (vector) để máy tính so sánh
> - **Similarity** đo khoảng cách giữa các vector trong không gian nhiều chiều
> - **Chunking** chia nhỏ documents trước khi embed
> - **Vector Database** lưu trữ và tìm kiếm vector nhanh chóng

---

### 5.4. Guardrails (Rào Cản) - "Hệ Miễn Dịch"

**Mục đích**: Ngăn chặn hành vi không mong muốn

**Các Loại Guardrails:**

<details>
<summary><b>TypeScript Code (Click to expand/collapse)</b></summary>

> 📄 **Code ví dụ:** [`examples/16-5-4-guardrails-rao-can-he-mien-dich.ts`](examples/16-5-4-guardrails-rao-can-he-mien-dich.ts)

</details>

**Ví dụ Implementation:**

<details>
<summary><b>TypeScript Code (Click to expand/collapse)</b></summary>

> 📄 **Code ví dụ:** [`examples/17-5-4-guardrails-rao-can-he-mien-dich.ts`](examples/17-5-4-guardrails-rao-can-he-mien-dich.ts)

</details>

---

### 5.5. Feedback Loops (Vòng Lặp Phản Hồi) - "Cảm Giác"

**Mục đích**: Tự động học và cải thiện từ kết quả

<details>
<summary><b>TypeScript Code (Click to expand/collapse)</b></summary>

> 📄 **Code ví dụ:** [`examples/18-5-5-feedback-loops-vong-lap-phan-hoi.ts`](examples/18-5-5-feedback-loops-vong-lap-phan-hoi.ts)

</details>

**Example:**

<details>
<summary><b>TypeScript Code (Click to expand/collapse)</b></summary>

> 📄 **Code ví dụ:** [`examples/19-5-5-feedback-loops-vong-lap-phan-hoi.ts`](examples/19-5-5-feedback-loops-vong-lap-phan-hoi.ts)

</details>

---

### 5.6. Permissions (Quyền Hạn) - "Xương"

**Mục đích**: Định nghĩa AI được phép làm gì, ở đâu, khi nào

<details>
<summary><b>TypeScript Code (Click to expand/collapse)</b></summary>

> 📄 **Code ví dụ:** [`examples/20-5-6-permissions-quyen-han-xuong.ts`](examples/20-5-6-permissions-quyen-han-xuong.ts)

</details>

---

### 5.7. Orchestration (Điều Phối) - "Hệ Thần Kinh"

**Mục đích**: Điều phối tất cả các thành phần hoạt động hài hòa

<details>
<summary><b>TypeScript Code (Click to expand/collapse)</b></summary>

> 📄 **Code ví dụ:** [`examples/21-5-7-orchestration-ieu-phoi-he-than-kinh.ts`](examples/21-5-7-orchestration-ieu-phoi-he-than-kinh.ts)

</details>

---

### Tích Hợp Tất Cả

<details>
<summary><b>Tích Hợp Tất Cả (Click to expand/collapse)</b></summary>

> 📄 **Code ví dụ:** [`examples/22-tich-hop-tat-ca.ts`](examples/22-tich-hop-tat-ca.ts)

</details>

---

### Tích Hợp Component Với Modules Trong Repo

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

| Component | Analogies | Modules trong Repo | Mô tả |
|-----------|-----------|-------------------|-------|
| **Tools** | "Tay chân" | `06-decide-tools-mcp` | Định nghĩa AI có thể dùng công cụ gì, tích hợp MCP |
| **Memory** | "Bộ não" | `01-retrieve-memory-knowledge`, `03-update-memory-store` | Nhớ & truy xuất kiến thức, cập nhật bộ nhớ |
| **Context Management** | "Hệ tuần hoàn" | `02-build-context` | Xây dựng ngữ cảnh phù hợp cho từng task |
| **Guardrails** | "Hệ miễn dịch" | `05-prompt-builder`, `11-evaluation` | Rào cản bảo vệ, kiểm tra đầu vào/đầu ra |
| **Feedback Loops** | "Cảm giác" | `07-workflow`, `11-evaluation` | Vòng lặp phản hồi, retry, đánh giá chất lượng |
| **Permissions** | "Xương" | `06-decide-tools-mcp`, `10-automation` | Phân quyền truy cập tài nguyên |
| **Orchestration** | "Hệ thần kinh" | `07-workflow`, `09-multi-agent`, `04-plan-decompose-task`, `08-task` | Điều phối tất cả thành phần hoạt động hài hòa |

> **Insight**: Prompt Engineering (`05-prompt-builder`) không phải là một component riêng biệt của Harness — nó là **kỹ thuật nền tảng** được tích hợp xuyên suốt nhiều components: System Prompt trong Orchestration, Few-shot trong Context Management, Structured Output trong Guardrails.

---

## 🔭 Toàn Cảnh: Harness Engineering — AI Coding Skills Framework

### Kiến Trúc Tổng Thể: 7 Components → 15 Modules

Sơ đồ dưới đây cho thấy **toàn bộ hệ thống Harness Engineering** và cách nó ánh xạ tới **15 modules** trong AI Coding Skills Framework — module `01`–`11` là các giai đoạn pipeline, còn `12`–`15` là mặt phẳng kiểm soát xuyên module mà tất cả đều phụ thuộc vào:

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
| Khía cạnh | RAG Pipeline (01) | Harness Engineering (Toàn bộ) |
|-----------|-------------------|-------------------------------|
| **Phạm vi** | 1 kỹ thuật: retrieve + augment | 7 components, 15 modules |
| **Vai trò** | Cung cấp kiến thức cho LLM | Kiểm soát mọi thứ AI có thể làm |
| **Tỷ lệ bao phủ** | ~85% của Memory component | 100% toàn bộ hệ thống |
| **Quan hệ** | Là 1 phần của Memory | Là tổng thể bao hàm RAG |

---

## 6. Case Studies Thực Tế

Các case dưới đây cho thấy các team lớn đã dùng Harness Engineering thế nào để đạt kết quả vượt trội.

---

### 6.1. SWE-agent (Princeton NLP)

**Bối cảnh**: team Princeton NLP làm một agent tự sửa GitHub issues.

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

**Kết quả**:
- Tỉ lệ thành công tăng từ **12.5% → 20.5%** (+64%)
- Thời gian xử lý một issue giảm 40%
- Lượng token tốn giảm 30%

**Key Insights**:
> "Không phải mô hình yếu, mà môi trường không được thiết kế tốt"

---

### 6.2. Anthropic Multi-Agent Architecture

**Bối cảnh**: Anthropic phát triển Claude Code để tạo các ứng dụng phức tạp (games, DAW, etc.)

**Vấn đề ban đầu**:
- Single agent làm quá nhiều việc cùng lúc → overwhelmed
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

---

### 6.3. Claude Code Leak - Hệ Thống Harness Siêu Đẳng

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

---

### 6.4. Cursor IDE - Harness Tối Ưu Cho Coding

**Đặc điểm nổi bật**:

<details>
<summary><b>TypeScript Code (Click to expand/collapse)</b></summary>

> 📄 **Code ví dụ:** [`examples/29-6-4-cursor-ide-harness-toi-uu-cho.ts`](examples/29-6-4-cursor-ide-harness-toi-uu-cho.ts)

</details>

**Kết quả**:
- Trở thành coding assistant được yêu thích nhất
- NPS (Net Promoter Score) > 70
- Nhiều developers chuyển từ GitHub Copilot sang Cursor

---

### 6.5. DeepSeek Harness — Micro-Kernel & Trajectory Traceability Framework

DeepSeek Harness đại diện cho thế hệ AI Agent Harness siêu mở rộng dựa trên triết lý **"Agent = Model + Harness"** và **"Everything is a Plugin"**. Được xây dựng trên nền tảng micro-kernel Cordis, DeepSeek Harness biến mọi thành phần của Agent (tools, context, memory, sub-agents) thành các plugins độc lập có thể tháo lắp linh hoạt.

#### A. Kiến Trúc Micro-Kernel & Ecosystem Plugin
- **Cordis Core Framework**: Quản lý vòng đời plugin qua 4 giai đoạn (`init`, `attach`, `ready`, `detach`).
- **Context Service Registry**: Sử dụng `ctx.provide()` và `ctx.inject()` cho phép các plugins đăng ký và tiêu thụ service độc lập (như logger, llmProvider, memoryStore).
- **Xem hướng dẫn chi tiết**: [`harness/07-workflow/cordis-kernel-plugin.md`](./harness/07-workflow/cordis-kernel-plugin.md)

#### B. 4 Runtime Modes Phân Hóa
DeepSeek Harness thiết kế 4 môi trường thực thi chuyên biệt phù hợp với mọi nhu cầu:
1. **Standard Mode**: Full-featured interactive CLI/GUI agent với đầy đủ MCP tools và middleware guardrails.
2. **Code Mode**: Chạy qua SDK (`@deepseek-ai/dsh`), gộp nhiều tool calls thành 1 kịch bản code duy nhất, giảm 70-90% latency và token cost.
3. **Minimal Benchmark Mode**: Môi trường tối giản chỉ có 2 tools (`bash`, `editor`) và minimal prompt để đánh giá năng lực suy luận nguyên bản của LLM.
4. **Creator Inspector Mode**: Runtime trực quan hóa timeline, cho phép inspect context state và chỉnh sửa preset agent.

#### C. Trajectory Traceability Engine (Session Event Stream & Branching)
- **Append-Only Event Log**: Mọi diễn biến session (Prompt, Reason, Tool Call, Output) được lưu dưới dạng chuỗi sự kiện không thể sửa đổi (`SessionEventStream`).
- **Time-Travel Replay & Forking**: Khả năng "tạm dừng" session tại bất kỳ bước nào, khôi phục trạng thái context (`replayToStep`) và rẽ nhánh (`forkSession`) để thử nghiệm giải pháp khác mà không làm hỏng session gốc.
- **Xem hướng dẫn chi tiết**: [`harness/03-update-memory-store/trajectory-fork-replay.md`](./harness/03-update-memory-store/trajectory-fork-replay.md)

#### D. Code Mode SDK & Sandboxed Execution
- Khắc phục nhược điểm latency của multi-turn tool calling truyền thống. LLM nhận diện kịch bản phức tạp và sinh ra mã lệnh TypeScript/Python gọi SDK `@deepseek-ai/dsh`.
- Kịch bản chạy trong Node.js `vm` sandbox an toàn, thực thi hàng chục thao tác ghi/đọc/build trong 1 turn duy nhất.
- **Xem hướng dẫn chi tiết**: [`harness/06-decide-tools-mcp/code-mode-sdk.md`](./harness/06-decide-tools-mcp/code-mode-sdk.md)

#### E. Minimal Benchmark Harness Cho Đánh Giá Năng Lực AI
- Cách ly hoàn toàn nhiễu từ framework phức tạp. Cho phép thực hiện đánh giá benchmark (như SWE-bench) với độ chính xác cao và độ lặp lại tuyệt đối.
- **Xem hướng dẫn chi tiết**: [`harness/11-evaluation/minimal-benchmark-harness.md`](./harness/11-evaluation/minimal-benchmark-harness.md)

---

### Bài Học Chung Từ Các Case Studies

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

**Nguyên tắc chung**:
1. ✅ **Constraints enable creativity** - Giới hạn giúp AI tập trung
2. ✅ **Layered architecture** - Chia nhỏ vấn đề
3. ✅ **Feedback loops** - Học từ kết quả
4. ✅ **User-centric design** - Luôn nghĩ về UX
5. ✅ **Obsess over details** - Mọi chi tiết đều quan trọng

---

## 7. Nguyên Tắc Thiết Kế Harness

### 7.1. Nguyên Tắc SOLID Cho Harness

**1. Single Responsibility**
- Mỗi tool chỉ làm một việc duy nhất
- Mỗi component có một lý do để thay đổi

**2. Open/Closed**
- Harness mở cho mở rộng (thêm tools, guardrails)
- Đóng cho sửa đổi (core logic ổn định)

**3. Liskov Substitution**
- Tools có thể thay thế cho nhau
- Cùng interface, khác implementation

**4. Interface Segregation**
- Không ép AI sử dụng tools không cần thiết
- Chỉ expose những gì cần

**5. Dependency Inversion**
- Depend on abstractions, not implementations
- Dễ dàng swap components

---

### 7.2. The 10 Commandments of Harness Engineering

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

---

### 7.3. The Harness Design Pattern

<details>
<summary><b>7.3. The Harness Design Pattern (Click to expand/collapse)</b></summary>

> 📄 **Code ví dụ:** [`examples/30-7-3-the-harness-design-pattern.ts`](examples/30-7-3-the-harness-design-pattern.ts)

</details>

---

## 8. Best Practices

### 8.1. Tool Design

✅ **DO:**
- Keep tools small and focused
- Validate inputs và outputs
- Provide clear error messages
- Make tools idempotent when possible
- Include examples in descriptions

❌ **DON'T:**
- Create "god tools" that do everything
- Trust AI to validate itself
- Use vague error messages
- Allow destructive operations without confirmation

### 8.2. Memory Management

✅ **DO:**
- Compress context regularly
- Prioritize relevant information
- Clear working memory after tasks
- Use tiered storage (hot/warm/cold)

❌ **DON'T:**
- Keep entire conversation history
- Load unnecessary data
- Mix different types of memory
- Forget to clean up

### 8.3. Context Building

✅ **DO:**
- Layer context by priority
- Include only relevant information
- Monitor token usage
- Compress when approaching limits

❌ **DON'T:**
- Include everything
- Ignore token limits
- Use static context
- Forget immediate context

### 8.4. Guardrails

✅ **DO:**
- Validate at multiple layers
- Check both input and output
- Fail fast and clearly
- Log all violations

❌ **DON'T:**
- Rely only on prompts
- Skip validation steps
- Hide errors from users
- Trust without verifying

### 8.5. Testing Harness

<details>
<summary><b>8.5. Testing Harness (Click to expand/collapse)</b></summary>

> 📄 **Code ví dụ:** [`examples/31-8-5-testing-harness.ts`](examples/31-8-5-testing-harness.ts)

</details>

---

## 9. Công Cụ và Framework

### 9.1. Frameworks Phổ Biến

**LangChain / LangGraph**

<details>
<summary><b>TypeScript Code (Click to expand/collapse)</b></summary>

> 📄 **Code ví dụ:** [`examples/32-9-1-frameworks-pho-bien.ts`](examples/32-9-1-frameworks-pho-bien.ts)

</details>

**AutoGen (Microsoft)**

<details>
<summary><b>Python Code (Click to expand/collapse)</b></summary>

> 📄 **Code ví dụ:** [`examples/33-9-1-frameworks-pho-bien.py`](examples/33-9-1-frameworks-pho-bien.py)

</details>

**CrewAI**

<details>
<summary><b>Python Code (Click to expand/collapse)</b></summary>

> 📄 **Code ví dụ:** [`examples/34-9-1-frameworks-pho-bien.py`](examples/34-9-1-frameworks-pho-bien.py)

</details>

---

### 9.2. Công Cụ Hỗ Trợ

**Vector Databases:**
- Pinecone
- Chroma
- Weaviate
- Qdrant

**Monitoring & Logging:**
- LangSmith
- Weights & Biases
- Helicone
- OpenLLMetry

**Guardrails:**
- Guardrails AI
- NeMo Guardrails (NVIDIA)
- LlamaGuard (Meta)

**Testing:**
- PromptFoo
- Deepeval
- Ragas

---

### 9.3. Starter Template

<details>
<summary><b>9.3. Starter Template (Click to expand/collapse)</b></summary>

> 📄 **Code ví dụ:** [`examples/35-9-3-starter-template.ts`](examples/35-9-3-starter-template.ts)

</details>

---

## 10. Tương Lai Của Harness Engineering

### 10.1. Xu Hướng 2026-2028

**1. Self-Optimizing Harnesses**
- Harness tự động điều chỉnh parameters
- A/B testing tự động
- Continuous learning from usage

**2. Harness-as-a-Service**
- Cloud platforms cung cấp pre-built harnesses
- Plug-and-play harness components
- Marketplace cho harness templates

**3. Visual Harness Builders**
- No-code tools để design harness
- Visual workflow editors
- Drag-and-drop tool composition

**4. Cross-Model Harnesses**
- Một harness chạy trên nhiều models
- Automatic model switching based on task
- Cost-optimized model routing

**5. Regulatory Compliance Harnesses**
- Built-in GDPR, HIPAA compliance
- Audit trails tự động
- Explainability baked in

---

### 10.2. Thách Thức Phía Trước

**Technical Challenges:**
- Standardization across platforms
- Interoperability between harnesses
- Performance optimization at scale
- Security và privacy

**Business Challenges:**
- ROI measurement
- Team skill gaps
- Legacy system integration
- Changing regulations

**Research Challenges:**
- Optimal harness architecture patterns
- Automated harness generation
- Harness testing methodologies
- Cross-domain transferability

---

### 10.3. Lời Khuyên Cho Tương Lai

```
1. Start Simple
   → Đừng over-engineer từ đầu
   → Build MVP harness first

2. Measure Everything
   → Track metrics từ ngày 1
   → Data-driven optimization

3. Stay Updated
   → Field đang phát triển nhanh
   → Follow best practices

4. Share Knowledge
   → Open source harness components
   → Build community

5. Think Long-term
   → Harness là infrastructure
   → Invest in maintainability
```

---

## 11. Tài Liệu Tham Khảo

### Papers & Research

1. **SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering**
   - Princeton NLP Lab
   - https://arxiv.org/abs/2405.15793

2. **The Rise of AI Agents and the Importance of Harness Engineering**
   - Mitchell Hashimoto, HashiCorp
   - https://www.youtube.com/watch?v=example

3. **Building Reliable AI Agents with Guardrails**
   - Anthropic Research
   - https://www.anthropic.com/research

### Frameworks & Tools

1. **LangChain** - https://langchain.com
2. **LangGraph** - https://langchain-ai.github.io/langgraph/
3. **AutoGen** - https://microsoft.github.io/autogen/
4. **CrewAI** - https://www.crewai.com
5. **Guardrails AI** - https://www.guardrailsai.com

### Communities

1. **LangChain Discord** - Active community
2. **r/LangChain** - Reddit discussions
3. **AI Engineers** - Slack community
4. **HuggingFace Forums** - Technical discussions

### Blogs & Resources

1. **Anthropic Blog** - https://www.anthropic.com/news
2. **OpenAI Cookbook** - https://cookbook.openai.com
3. **LangChain Blog** - https://blog.langchain.dev
4. **Mitchell Hashimoto's Blog** - https://mitchellh.com

### Courses & Tutorials

1. **DeepLearning.AI - Building AI Agents**
2. **LangChain Academy**
3. **Anthropic Prompt Engineering**
4. **Microsoft AutoGen Tutorial**

---

**Kết Luận**

Harness Engineering không chỉ là một xu hướng công nghệ — nó là sự chuyển đổi góc nhìn trong cách chúng ta xây dựng ứng dụng AI. Khi các mô hình AI ngày càng mạnh và dần trở thành "hàng hóa phổ thông", khả năng thiết kế một harness tốt sẽ là yếu tố quyết định thành công.

> **"The model thinks. The harness shapes what it thinks about. And the harness determines the quality of the final output."**

Hãy bắt đầu từ hôm nay — không cần hoàn hảo, chỉ cần bắt đầu. Cứ build, đo lường, học hỏi rồi cải thiện dần. Harness Engineering là một hành trình, không phải đích đến.

**Happy Building! 🚀**

---

**Ngày cập nhật:** 16/10/2026  
**Tác giả:** AI Knowledge Repository
