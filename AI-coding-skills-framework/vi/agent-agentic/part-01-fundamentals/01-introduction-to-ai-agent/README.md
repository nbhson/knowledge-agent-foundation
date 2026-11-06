# 🧠 Module 1. Introduction to AI Agent

> ## 📑 Mục Lục
>
> - [Câu Chuyện Mở Đầu](#câu-chuyện-mở-đầu)
> - [1. AI là gì?](#1-ai-là-gì)
> - [2. AI, Machine Learning, Deep Learning — Ba Tầng Khác Nhau](#2-ai-machine-learning-deep-learning--ba-tầng-khác-nhau)
> - [3. LLM là gì?](#3-llm-là-gì)
> - [4. AI Chatbot vs AI Assistant vs AI Agent](#4-ai-chatbot-vs-ai-assistant-vs-ai-agent)
> - [5. Agent là gì?](#5-agent-là-gì)
>   - [5.1 Agent trong Computer Science](#51-agent-trong-computer-science)
>   - [5.2 Agent trong LLM-based AI](#52-agent-trong-llm-based-ai)
> - [6. AI Agent khác gì một chương trình thông thường?](#6-ai-agent-khác-gì-một-chương-trình-thông-thường)
> - [7. Tại sao LLM không tự động trở thành Agent?](#7-tại-sao-llm-không-tự-động-trở-thành-agent)
> - [8. Các ứng dụng thực tế của AI Agent](#8-các-ứng-dụng-thực-tế-của-ai-agent)
> - [Tóm Tắt & Checklist](#tóm-tắt--checklist)

---

## Câu Chuyện Mở Đầu

Bạn hãy tưởng tượng hai người trợ lý làm việc trong cùng một công ty:

- **Người trợ lý A:** Bạn nói *"tìm giúp tôi báo cáo doanh thu quý 3"*, anh ta lục máy tính, mở đúng 3 file Excel, chép số liệu, dán vào email, rồi hỏi lại *"tôi gửi cho Giám đốc hay soạn nháp trước?"*. Một mình anh ta lo trọn vẹn: tìm → đọc → suy nghĩ → soạn → định dạng → trình duyệt → gửi.
- **Người trợ lý B:** Cũng câu nói đó, anh ta chỉ đáp: *"Báo cáo quý 3 nằm ở thư mục Finance, anh mở file Q3.xlsx là thấy."* Rồi ngồi yên, không giúp gì thêm.

Cả hai đều "thông minh", đều hiểu yêu cầu. Nhưng **chỉ người trợ lý A mới đáng gọi là một Agent** — vì anh ta *tự mình hành động* để hoàn thành việc, chứ không chỉ trả lời.

Đây chính là điểm khác biệt cốt lõi mà cả module sẽ đi sâu: **"biết nói" ≠ "biết làm".**

> **Tóm gọn 1 câu:** LLM giỏi *trả lời*, Agent giỏi *hành động* — nhận mục tiêu của bạn rồi tự tìm cách hoàn thành.

---

## 1. AI là gì?

Với người mới, AI (Artificial Intelligence — trí tuệ nhân tạo) dễ bị hiểu là "thứ gì đó biết suy nghĩ như con người". Thực tế đơn giản hơn:

> **AI là máy tính làm được những việc mà bình thường cần trí thông minh con người** — đọc hiểu, nhận diện ảnh, nói chuyện, dự đoán, ra quyết định.

Ngày nay AI đã ở khắp nơi: trợ lý giọng nói, gợi ý phim, lọc spam, dịch máy... Bạn dùng hằng ngày mà nhiều khi không để ý.

Có một cách chia AI thành hai nhóm rất hữu ích khi học về Agent:

- **Narrow AI (AI hẹp):** giỏi một việc cụ thể — dò mã độc, đánh cờ, nhận diện khuôn mặt. Đây là toàn bộ AI đang tồn tại hiện nay, kể cả ChatGPT.
- **General AI / AGI (AI tổng quát):** làm được mọi việc như con người. Đây là mục tiêu nghiên cứu lâu dài, hiện **chưa có** thật.

> **Tóm gọn 1 câu:** AI = máy làm việc cần trí thông minh; hiện tại mới chỉ có AI hẹp — giỏi từng việc một, chưa có AGI thật sự.

*Chú thích nhanh: AGI = Artificial General Intelligence — AI có khả năng hiểu và học bất kỳ nhiệm vụ trí tuệ nào như con người.*

---

## 2. AI, Machine Learning, Deep Learning — Ba Tầng Khác Nhau

Trên các bài báo công nghệ, ba thuật ngữ này hay bị dùng lẫn lộn. Thực ra chúng là **ba vòng tròn lồng nhau**:

- **AI** là vòng ngoài cùng — mục tiêu lớn: máy thông minh.
- **Machine Learning (ML)** là một cách đạt AI — thay vì con người viết quy tắc, **máy tự học từ dữ liệu**.
- **Deep Learning (DL)** là một nhánh của ML — dùng **mạng nơ-ron nhiều tầng** (neural network), học được các mẫu cực kỳ phức tạp. LLM (như GPT, Claude) nằm trong nhánh này.

| Tầng | Là gì? | Ví dụ |
|------|--------|-------|
| **AI** | Lĩnh vực rộng: mọi kỹ thuật làm máy "thông minh" | Cờ vua máy, trợ lý ảo, xe tự hành |
| **Machine Learning** | Máy *tự học quy luật từ dữ liệu*, không cần người lập trình từng bước | Chặn spam email, gợi ý sản phẩm |
| **Deep Learning** | ML dùng mạng nơ-ron nhiều lớp; học mẫu phức tạp từ lượng dữ liệu khổng lồ | GPT, Claude, Gemini — dịch máy, giọng nói |

*Cách đọc bảng: mỗi dòng là một tầng — đọc từ trên xuống, DL nằm trong ML, ML nằm trong AI.*

> **Tóm gọn 1 câu:** AI là mục tiêu, ML là cách học từ dữ liệu, DL là cách học sâu bằng mạng nơ-ron — và LLM chính là sản phẩm tiêu biểu của DL.

---

## 3. LLM là gì?

LLM = **Large Language Model** (mô hình ngôn ngữ lớn) — "bộ não" đằng sau ChatGPT, Claude, Gemini.

Một cách gần gũi để hiểu: LLM là **một chương trình khổng lồ đã "đọc" một lượng văn bản cực kỳ lớn trên internet** (hàng nghìn tỷ từ) và học được cách dùng từ ngữ. Khi bạn hỏi, nó dự đoán từ tiếp theo một cách thông minh để tạo ra câu trả lời tự nhiên.

Điều quan trọng cần nhớ với người mới:

- LLM **chỉ giỏi một việc: sinh văn bản** (đôi khi kèm đọc hiểu, lập luận, viết code).
- LLM **không tự làm được việc ngoài đời**: không tự mở file, không tự gọi API, không tự chạy code.
- LLM **không có trạng thái**: nó không "nhớ" gì giữa các lần hỏi nếu bạn không cung cấp bối cảnh (vấn đề về *memory* — sẽ học ở Module 7).

> **Tóm gọn 1 câu:** LLM là máy "dự đoán chữ" cực giỏi — nó nói và suy nghĩ, nhưng tay chân (mở file, gọi API, chạy code) thì phải người khác cung cấp.

*Chú thích nhanh: "token" = đơn vị mà LLM đọc — khoảng ¾ một từ tiếng Anh. Ví dụ từ "agent" có thể là 1–2 token. Bạn sẽ học chi tiết ở Module 5.*

---

## 4. AI Chatbot vs AI Assistant vs AI Agent

Trước khi định nghĩa Agent, phải gỡ rối ba cái tên thường bị dùng thay cho nhau. Cách dễ nhớ nhất là nhìn theo **mức độ tự hành động**:

| | **AI Chatbot** | **AI Assistant** | **AI Agent** |
|---|---|---|---|
| **Hành động chính** | Trả lời hội thoại | Trả lời + làm theo yêu cầu | Tự lập kế hoạch và hoàn thành mục tiêu |
| **Có dùng công cụ?** | Ít / không | Có, theo từng lệnh | Có, và **tự chọn** lệnh nào, lúc nào |
| **Ai ra quyết định?** | Người dùng | Người dùng | Agent (trong phạm vi cho phép) |
| **Nhớ lâu?** | Trong phiên chat | Trong phiên + vài thiết lập | Bộ nhớ nhiều tầng (học ở Module 7) |
| **Ví dụ** | Web hỗ trợ khách hàng | Siri, Alexa, Google Assistant | Claude Code, auto-deal triage, research agent |

*Cách đọc bảng: từ trái sang phải, độ "biết làm" tăng dần.*

Lưu ý ranh giới không cứng nhắc — một *Assistant* có thể nâng cấp thành *Agent* khi mở rộng khả năng tự quyết định. Nhưng phân biệt cốt lõi vẫn là:

- **Chatbot** trả lời. **Assistant** làm theo lệnh. **Agent** *chủ động hoàn thành mục tiêu*.

> **Tóm gọn 1 câu:** Chatbot biết nói, Assistant biết vâng lời từng việc, Agent biết "tự lo" cả một việc từ đầu đến cuối.

---

## 5. Agent là gì?

Thuật ngữ "agent" không phải mới. Vì cụm "AI Agent" đang hot, nhiều người hiểu sai. Thật ra có **hai nghĩa lịch sử**, và ta cần cả hai:

### 5.1 Agent trong Computer Science

Trong khoa học máy tính, một **agent** (tác tử) là:

> **Một thực thể tự động bên trong một môi trường — nó "nhận biết" môi trường qua cảm biến (sensors), "quyết định" sẽ làm gì, rồi "tác động" lại môi trường qua thiết bị hành động (actuators).**

Ví dụ kinh điển: **xe hút bụi tự động (Roomba)**.

- **Môi trường:** căn phòng.
- **Cảm biến:** cảm biến va chạm, cảm biến bụi.
- **Quyết định:** bám theo tường, xoay khi gặp vật cản.
- **Hành động:** lăn bánh, chạy máy hút.

Nó vận hành theo chu trình **Perceive → Decide → Act → (quan sát kết quả) → lặp lại** — cái gọi là *perception-action loop* (vòng lặp nhận thức–hành động). Đây chính là **nền tảng của mọi agent**, kể cả agent AI hiện đại.

### 5.2 Agent trong LLM-based AI

Agent trong thế giới AI Agent (như nội dung khóa này) là sự mở rộng đúng logic đó, nhưng **"bộ não" thay bằng LLM**:

> **AI Agent = một chương trình mà LLM làm "bộ não" — có thể tự suy nghĩ, lập kế hoạch, dùng công cụ (tools), ghi nhớ (memory), và thực thi nhiều bước lặp đi lặp lại cho đến khi hoàn thành mục tiêu.**

Định nghĩa ngắn gọn của ngành (đồng thuận Anthropic, Simon Willison, 2026):

> *"An agent is an LLM autonomously using tools in a loop."*
> (Agent là một LLM tự chủ dùng công cụ trong một vòng lặp.)

So sánh hai khái niệm:

| | Agent trong Computer Science | AI Agent (LLM-based) |
|---|---|---|
| **Bộ não** | Luật if/else, bảng quyết định | LLM (mô hình ngôn ngữ lớn) |
| **Môi trường** | Phòng, ngã tư, thiết bị... | File, ứng dụng, web, API, terminal... |
| **Cảm biến (nhận biết)** | Cảm biến vật lý | Đọc file, tìm kiếm, gọi API, xem web |
| **Hành động (tác động)** | Bánh xe, cánh tay robot | Gọi công cụ, ghi file, chạy code, gửi tin |
| **Suy luận** | Có hạn / theo quy tắc | Phong phú, linh hoạt theo ngữ cảnh |

> **Tóm gọn 1 câu:** "Agent" cổ điển là thực thể nhận biết–quyết định–hành động trong môi trường; AI Agent ngày nay dùng LLM làm bộ não cho vòng lặp ấy — biết suy nghĩ, dùng công cụ và tự chạy nhiều bước đến khi xong việc.

---

## 6. AI Agent khác gì một chương trình thông thường?

"Chương trình thông thường" ở đây là phần mềm truyền thống: chạy theo một kịch bản cố định, input nào ra output đấy, lặp lại y hệt. Không có lập trình viên nào viết một phần mềm "mở file, xem nội dung, rồi *tự quyết định* ghi gì vào chỗ nào" — vì không thể đoán trước mọi tình huống.

| Đặc điểm | Chương trình thông thường | AI Agent |
|---|---|---|
| **Suy luận** | Không — chỉ chạy luật đã lập trình | Có — dùng LLM suy luận theo từng bước |
| **Kế hoạch** | Được viết sẵn từ trước | Tự lập, tự điều chỉnh giữa chừng |
| **Chọn hành động** | Code-biết-trước | Agent tự chọn trên bàn công cụ |
| **Có thể thất bại tinh tế** | Khó (ra lỗi cứng) | Có — có thể sai logic giống người, rồi tự sửa |
| **Thích ứng sự cố** | Gần như không | Có — quan sát kết quả, xoay hướng |
| **Nhớ giữa các lần chạy** | Không (resettable) | Có — nhờ memory (Module 7) |

Ví dụ minh họa cho sự khác biệt:

- **Chương trình thường (email bot):** mỗi email tới → nó đọc tiêu đề → nếu có từ "phản hồi" thì đánh dấu → gửi vào thư mục support. Làm mãi một việc, đơn giản, không sai.
- **AI Agent (support agent):** nhận email "khách khiếu nại hóa đơn quá cao" → *hiểu* nội dung → *kiểm tra* cơ sở dữ liệu hóa đơn → *đối chiếu* giá với hợp đồng → *soạn* email giải thích → *nếu* chưa đủ thuyết phục thì *tự tìm* thêm thông tin → gửi. Mỗi email là một "chặng đường" khác nhau.

> **Tóm gọn 1 câu:** Chương trình thường chạy đúng kịch bản viết sẵn; Agent *tự suy nghĩ, tự chọn hành động và tự thích nghi* — giống một nhân viên thông minh hơn là một cỗ máy theo quy trình.

---

## 7. Tại sao LLM không tự động trở thành Agent?

Đây là sai lầm phổ biến nhất của người mới: *"ChatGPT thông minh vậy, chắc nó là agent rồi."* Không phải. Một LLM cô lập **thiếu 3 thứ** để thành agent:

| Thứ còn thiếu | Mô tả | Sẽ học ở đâu trong khóa |
|---|---|---|
| **Công cụ (tools)** | LLM không tự mở file, gọi API, chạy code — phải có người "gắn tay chân" | Module 8 |
| **Bộ nhớ (memory)** | LLM không nhớ giữa các phiên — phải có hệ thống lưu trữ ngoài | Module 7 |
| **Vòng lặp & cơ chế điều khiển (loop + orchestrator)** | LLM chỉ trả lời một lần — phải có "người chỉ huy" cho nó lặp: suy nghĩ → hành động → kiểm tra → suy nghĩ tiếp | Module 3, 9 |

Nghĩ theo ví dụ câu chuyện mở đầu: **LLM là người trợ lý B** (giỏi tư vấn), còn một *Agent* là trợ lý B **được lắp thêm** tay (tools), sổ ghi nhớ (memory), và một "sếp" chỉ đạo vòng lặp làm việc (orchestrator) — để biến thành **người trợ lý A**.

> **Tóm gọn 1 câu:** LLM mới chỉ là "bộ não" — muốn thành Agent phải lắp thêm tay chân (tools), trí nhớ (memory) và người chỉ huy vòng lặp (orchestration); thiếu một trong ba thì chỉ là chatbot giỏi.

---

## 8. Các ứng dụng thực tế của AI Agent

Để tăng độ "thực tế", đây là những nơi AI Agent đang được dùng thật trong sản xuất (không phải demo):

### 8.1 Lập trình & phát triển phần mềm
- **Coding agent:** tự phân tích task, sửa code nhiều file, chạy test, hồi phục khi gặp lỗi (ví dụ: Claude Code, GitHub Copilot agent, Cursor).
- **Auto code review:** tự rà soát pull request, tìm lỗi bảo mật, đề nghị cải tiến.

### 8.2 Vận hành & ops
- **Support/triage agent:** đọc ticket, phân loại mức độ, soạn câu trả lời, tự động điều phối tới đúng team.
- **Incident agent:** giám sát hệ thống, khi có cảnh báo thì tự điều tra log và đề xuất / thực thi cách xử lý.

### 8.3 Dữ liệu & kiến thức
- **Research agent:** nhận câu hỏi "so sánh X và Y", chạy nhiều hướng tìm kiếm song song, gộp thành báo cáo có trích dẫn.
- **Knowledge-base agent:** tự cập nhật tài liệu, gom dữ liệu rời rạc thành tri thức có cấu trúc.

### 8.4 Kinh doanh & giao tiếp
- **Email/meeting agent:** đọc thư, trả lời, đặt lịch họp, tóm tắt cuộc họp và gửi action items.
- **Sales agent:** điều hướng khách hàng trong quy trình chào bán, chấm điểm khả năng mua dựa trên dữ liệu.

> **Tóm gọn 1 câu:** Agent đang "được thuê" ở khắp nơi — viết code, xử lý ticket, nghiên cứu, chăm sóc khách hàng — bất kỳ đâu có việc lặp lại nhiều bước, đòi hỏi suy nghĩ và thích nghi.

---

## Tóm Tắt & Checklist

### Nội dung đã học trong module này

1. **AI** = máy làm việc cần trí thông minh; AI → ML → DL là ba vòng tròn lồng nhau.
2. **LLM** là "máy dự đoán chữ" cực giỏi — chỉ giỏi sinh văn bản, không tự hành động ngoài đời.
3. **Chatbot trả lời → Assistant vâng lời từng việc → Agent tự lo cả việc.**
4. **Agent** (computer science) = nhận biết → quyết định → hành động trong môi trường; **AI Agent** = dùng LLM làm bộ não cho vòng lặp đó.
5. **Agent ≠ chương trình thường** — biết suy luận, tự lập kế hoạch, tự chọn hành động, thích ứng sự cố.
6. **LLM chưa phải Agent** — thiếu tools, memory, và loop/orchestrator.

### Checklist tự kiểm tra

Bạn đã nắm được khi có thể trả lời lưu loát các câu hỏi sau:

- [ ] Giải thích cho người khác: AI, Machine Learning, Deep Learning khác nhau thế nào?
- [ ] Phân biệt được AI Chatbot vs AI Assistant vs AI Agent bằng một ví dụ?
- [ ] Định nghĩa được "agent" theo nghĩa Computer Science (perceive → decide → act)?
- [ ] Trình bày được định nghĩa ngắn: "AI Agent = LLM tự chủ dùng công cụ trong vòng lặp"?
- [ ] Giải thích tại sao ChatGPT chỉ là chatbot, chưa phải agent theo nghĩa này khóa dạy?
- [ ] Kể được 2–3 ứng dụng Agent đang dùng thật ngoài đời?

---

## Tóm Gọn Toàn Module

> **Một câu để nhớ mãi:** LLM là bộ não giỏi nói; **Agent** là bộ não đó được gắn thêm tay chân, trí nhớ và vòng lặp chỉ huy — để không chỉ *trả lời* mà còn *tự làm* việc đến cùng.

**Đi tiếp:** Module 2 sẽ làm rõ *Agentic AI* — khi "tính agent" (tự chủ, có mục tiêu, chia chuỗi hành động) trở thành triết lý thiết kế của cả một hệ thống, cùng các khái niệm thường đi kèm (autonomy, agentic workflow, human-in-the-loop...).
