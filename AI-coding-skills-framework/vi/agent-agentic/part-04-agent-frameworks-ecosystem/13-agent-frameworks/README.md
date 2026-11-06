# 🧩 Module 13. Agent Frameworks

> ## 📑 Mục Lục
>
> - [Câu Chuyện Mở Đầu](#câu-chuyện-mở-đầu)
> - [1. Nhà Hàng Nấu Từ Đầu vs Dùng Nguyên Liệu Đóng Gói](#1-nhà-hàng-nấu-từ-đầu-vs-dùng-nguyên-liệu-đóng-gói)
> - [2. Build Agent from Scratch — Nấu Từ Đầu](#2-build-agent-from-scratch--nấu-từ-đầu)
> - [3. Framework là gì?](#3-framework-là-gì)
> - [4. So Sánh 5 Framework Lớn](#4-so-sánh-5-framework-lớn)
> - [5. Framework vs Runtime vs SDK](#5-framework-vs-runtime-vs-sdk)
> - [6. Khi Nào Dùng Framework, Khi Nào Tự Xây?](#6-khi-nào-dùng-framework-khi-nào-tự-xây)
> - [Tóm Tắt & Checklist](#tóm-tắt--checklist)

---

## Câu Chuyện Mở Đầu

Hãy tưởng tượng hai nhà hàng trong cùng một khu phố, cùng phục vụ một món bò bít tết:

- **Nhà hàng A (nấu từ đầu):** Đầu bếp tự mua thịt từ lò giết mổ, tự tẩm ướp, tự làm sốt từ bơ và hành, tự nướng trên bếp than, tự chế biến món phụ. Kiểm soát được **100% từng chi tiết** — vị, độ chín, nguồn gốc nguyên liệu. Nhưng để mở một nhà hàng như thế thì **tốn thời gian và chi phí cực lớn**, và đầu bếp phải giỏi đủ mọi khâu.
- **Nhà hàng B (dùng nguyên liệu đóng gói):** Đầu bếp mua sốt, gia vị, thậm chí cả phần thịt đã tẩm sẵn từ các nhà cung cấp đóng gói sẵn. **Mở nhanh, dễ vận hành**, món nào cũng ra được. Nhưng hương vị **khó khác biệt** so với đối thủ, và mỗi khi nhà cung cấp đổi công thức thì món ăn cũng đổi theo — không kiểm soát được.

Trong thế giới AI Agent cũng y hệt: bạn có thể **tự tay lắp ráp một agent từ những mảnh ghép cơ bản** (LLM, tools, memory, vòng lặp) — gọi là *Build Agent from Scratch*; hoặc **dùng một framework** đã đóng gói sẵn các mảnh ghép đó (LangChain, LangGraph, CrewAI, AutoGen, OpenAI Agents SDK).

> **Tóm gọn 1 câu:** Tự xây agent từ đầu giống nấu ăn từ đầu — kiểm soát trọn vẹn nhưng tốn công; còn dùng framework giống dùng nguyên liệu đóng gói — ra món nhanh, nhưng bị lệ thuộc vào "công thức" của người khác.

---
## 1. Nhà Hàng Nấu Từ Đầu vs Dùng Nguyên Liệu Đóng Gói

Quan sát kỹ hơn hai cách làm, ta rút ra được ba tiêu chí quyết định, và chúng áp dụng y hệt khi chọn giữa *tự xây agent* và *dùng framework*:

| Tiêu chí | Nấu từ đầu (From Scratch) | Nguyên liệu đóng gói (Framework) |
|---|---|---|
| **Thời gian ra món** | Lâu — phải chuẩn bị mọi khâu | Nhanh — lắp ghép là xong |
| **Mức kiểm soát** | 100% — chỉnh được từng chi tiết | Hạn chế — theo "công thức" có sẵn |
| **Phụ thuộc bên ngoài** | Thấp — tự lo nguyên liệu | Cao — đổi nhà cung cấp là món đổi vị |
| **Công sức bảo trì** | Tự lo mọi thứ, nhiều việc vặt | Nhà cung cấp lo phần lớn |
| **Khác biệt sản phẩm** | Cao — dễ tạo "vị riêng" | Thấp — nhiều nhà hàng cùng một vị |
| **Hợp khi nào** | Món đặc biệt, ngân sách dồi dào, muốn làm lâu dài | Món phổ thông, cần ra mắt nhanh, đội ngũ nhỏ |

Nhà hàng giỏi thường **kết hợp cả hai**: dùng gia vị đóng gói cho món phụ, nhưng tự làm món chính — đúng như cách đội ngũ kỹ thuật giỏi *dùng framework cho phần cốt lõi chứng minh ý tưởng, nhưng tự xây phần lõi làm nên sự khác biệt*.

> **Tóm gọn 1 câu:** Không có "cách nào luôn đúng" — chỉ có câu hỏi *"bạn đang cần ra món nhanh hay muốn tạo vị riêng?"*

---

## 2. Build Agent from Scratch — Nấu Từ Đầu

Trước khi bàn tới framework, phải hiểu **thành phần cốt lõi của một agent** — vì framework nào cũng chỉ là cách đóng gói những thành phần này:

1. **Bộ não (LLM):** mô hình ngôn ngữ lớn — suy luận và ra quyết định (GPT, Claude, Gemini...).
2. **Công cụ (Tools):** hàm cho agent gọi ra ngoài — tìm kiếm, đọc file, gọi API, chạy code (học ở Module 8).
3. **Bộ nhớ (Memory):** lưu ngữ cảnh và ký ức giữa các bước (học ở Module 7).
4. **Vòng lặp (Agent Loop):** vòng lặp *suy nghĩ → hành động → quan sát kết quả → suy nghĩ tiếp* cho đến khi hoàn thành mục tiêu.

Một agent "từ đầu" theo nghĩa đơn giản nhất có thể được viết bằng **vài chục dòng code** lặp đi lặp lại lời gọi LLM và thực thi công cụ:

```
while chưa hoàn thành mục tiêu:
    bước_tiếp_theo = LLM(suy_nghĩ, ngữ_cảnh, danh_sách_công_cụ)
    if bước_tiếp_theo == "gọi_công_cụ":
        kết_quả = thực_thi(bước_tiếp_theo.tên, bước_tiếp_theo.tham_số)
        thêm kết_quả vào ngữ_cảnh
    elif bước_tiếp_theo == "trả_lời":
        trả về lời giải đáp cuối cùng
```

Đây chính là **"hello world" của mọi agent** — và chính là điều các framework đóng gói thành công thức có sẵn. Hiểu được vòng lặp này là **nền tảng để đánh giá mọi framework** ở phần sau.

> **Tóm gọn 1 câu:** Agent từ đầu chỉ gồm LLM + Tools + Memory + Agent Loop; nắm được vòng lặp cơ bản này là bạn đã hiểu mọi framework — vì framework chỉ là "món ăn đóng gói" từ đúng các nguyên liệu này.

---
## 3. Framework là gì?

**Framework (khung chương trình)** trong thế giới agent là:

> **Một bộ code có sẵn, đóng gói sẵn các mảnh ghép cần thiết để xây agent — bạn chỉ việc lắp theo API của nó thay vì viết từng chi tiết từ đầu.**

Thay vì tự viết vòng lặp, tự quản lý lời gọi LLM, tự nối các công cụ... bạn khai báo: *"đây là LLM tôi dùng, đây là tools của tôi, đây là bộ nhớ của tôi"* — và framework lo phần còn lại: gọi LLM, nối chuỗi, quản lý trạng thái, retry, log...

Hầu hết framework hiện đại đều cung cấp ba thứ chung:

- **Chuẩn hóa cách gọi LLM** — một API thống nhất để đổi model mà không phải sửa lại code.
- **Hệ thống tools/integrations** — sẵn hàng trăm bộ kết nối tới các dịch vụ phổ biến.
- **Orchestration** — kiểu nối các bước: chuỗi tuyến tính, vòng lặp, nhiều agent phối hợp.

Đi kèm framework thường có cả một **hệ sinh thái**: tài liệu, cộng đồng, mẫu code, công cụ debug — cũng như rủi ro: *thư viện lỗi thời, breaking change, hiệu năng ngầm, và "vendor lock-in"* (bị khóa vào một hệ sinh thái).

> **Tóm gọn 1 câu:** Framework là "bộ công thức đóng gói" — bạn khai báo nguyên liệu (LLM, tools, memory), framework lo việc nấu (gọi model, nối bước, quản lý trạng thái).

---

## 4. So Sánh 5 Framework Lớn

Đến đây, hãy nhìn năm framework phổ biến nhất hiện nay cạnh nhau. (Lưu ý: thị trường thay đổi nhanh — đây là bức ảnh chụp năm 2026.)

| Tên | Người tạo | Mô hình | Mạnh | Yếu | Dùng khi |
|---|---|---|---|---|---|
| **LangChain** | Harrison Chase (2022) | Orchestration đa năng: chuỗi (chain), tools, memory, tích hợp hàng trăm dịch vụ | Hệ sinh thái khổng lồ, tài liệu phong phú, linh hoạt | Phức tạp, dễ "over-engineering", API tầng lớp chồng nhau, hay breaking change | Cần nhanh chóng nối nhiều tích hợp; prototype lớn; soi mói nhiều dịch vụ |
| **LangGraph** | Cùng nhóm LangChain (2024) | Graph có trạng thái: agent như đồ thị các node/edge, có state machine | Kiểm soát flow rõ ràng, dễ debug, hỗ trợ vòng lặp và checkpoints | Học dốc hơn LangChain, vì graph nên boilerplate nhiều | Agent phức tạp cần kiểm soát luồng, có trạng thái lâu dài, production |
| **CrewAI** | João Moura (2023) | Role-based: tạo "team" gồm nhiều agent mang vai trò (role), chia task | Dễ học, viết code gần với tự nhiên, tư duy team/role tự nhiên | Ít kiểm soát luồng tinh vi, cồng kềnh với agent đơn giản | Cần nhiều agent phân vai phối hợp như một team (research + writer + critic...) |
| **AutoGen** | Microsoft (2023 / AutoGen v0.4+) | Multi-agent hội thoại: các agent trò chuyện/lập luận với nhau | Phù hợp nghiên cứu multi-agent, mạnh về convo-driven, hậu thuẫn từ Microsoft | API hay đổi, khái niệm trừu tượng hóa cao, khó gỡ lỗi | Nghiên cứu/bài toán multi-agent đối thoại; so sánh các "đấu trí" giữa agent |
| **OpenAI Agents SDK** | OpenAI (2025) | Agent + Handoff: agent gọn nhẹ, "trả lại" (handoff) công việc cho agent khác | Đơn giản, hiện đại, sinh thái OpenAI, chi phí thấp để khởi động | Gắn với hệ OpenAI material, ít plugins, mới nên hệ sinh thái còn mỏng | Muốn agent đơn giản, hiệu quả; đã ở hệ OpenAI; cần lên production nhanh |

*Cách đọc bảng: "Mô hình" là cách framework tư duy về agent — đây chính là yếu tố quyết định bạn chọn cái nào.*

> **Tóm gọn 1 câu:** LangChain/LangGraph mạnh về orchestration linh hoạt, CrewAI tư duy "đội nhóm vai trò", AutoGen tư duy "nhiều agent trò chuyện", OpenAI Agents SDK gọn nhẹ modern — chọn theo *cách bạn muốn tư duy* về agent.

---
## 5. Framework vs Runtime vs SDK

Ba khái niệm hay bị lẫn nhau. Rõ ràng trước để không chọn nhầm:

| Tiêu chí | **Framework** | **Runtime** | **SDK** |
|---|---|---|---|
| **Định nghĩa ngắn** | "Nhà hàng đóng gói" — bộ công thức có sẵn | "Bếp ga" — môi trường chạy thực sự | "Bộ dao nĩa" — thư viện code dùng trong bếp |
| **Bạn viết gì?** | Khai báo cấu hình, lắp ghép components | Chỉ chạy, không viết nhiều | Viết code để gọi API thư viện |
| **Ai lo?** | Bạn chọn nguyên liệu và cách nấu | Runtime (ví dụ: vLLM, Ollama) lo việc chạy model | SDK lo giao diện gọi; bạn lo logic |
| **Ví dụ** | LangChain, CrewAI, AutoGen | vLLM, Ollama, Hugging Face TGI, Claude API runtime | OpenAI SDK, Anthropic SDK, Google AI SDK |
| **Vai trò** | **Thiết kế** agent (design-time) | **Chạy** model (run-time) | **Giao tiếp** với dịch vụ (integration) |

**Phân biệt bằng ví dụ thực tế:**

- **Bạn dùng vLLM (Runtime)** → để model chạy trên máy chủ mình, không phải qua API.
- **Bạn dùng OpenAI SDK (SDK)** → để gọi API của OpenAI từ Python/JS.
- **Bạn dùng LangChain hoặc CrewAI (Framework)** → để thiết kế agent xem dùng LLM nào, gọi tool gì, theo luồng nào.

Cả ba **không loại trừ nhau** — trong một hệ thống production, bạn thường dùng: Framework (thiết kế) + Runtime (chạy model) + SDK (giao tiếp API). Ví dụ: CrewAI gọi model qua vLLM qua OpenAI SDK.

> **Tóm gọn 1 câu:** Framework chọn *cách nấu*, Runtime cho *ngọn lửa nấu*, SDK là *dao thớt* — trong bếp thực sự bạn cần cả ba, không loại trừ.

---

## 6. Khi Nào Dùng Framework, Khi Nào Tự Xây?

Đây là câu hỏi không có đáp án duy nhất đúng — câu trả lời phụ thuộc vào **tình huống cụ thể** của bạn. Dùng bảng sau để tự đánh giá:

| Tình huống | Khuyến nghị | Lý do |
|---|---|---|
| **Bạn cần prove concept nhanh (POC) trong vài ngày** | ✅ Dùng framework (LangChain hoặc CrewAI) | Framework cho phép ghép nhanh các mảnh, ra POC ngay |
| **Agent đơn giản, 1 LLM + 3 tools, ít logic** | ⚠️ Có thể tự xây nhẹ | Dùng framework cho món đơn giản là dùng dao mổ trâu giết gà |
| **Cần nhiều agent phối hợp theo vai trò** | ✅ Dùng CrewAI hoặc LangGraph | Tư duy team/graph của framework giảm boilerplate đáng kể |
| **Bạn cần kiểm soát trạng thái ở tầng sâu, debug chi tiết** | ✅ LangGraph hoặc tự xây | Graph-based cho phép trace từng node; tự xây cho debug sâu nhất |
| **Bạn cần tích hợp sâu vào hệ thống cũ, ít thay đổi** | ⚠️ Tự xây hoặc SDK nhẹ | Framework tạo thêm lớp phụ thuộc; hệ thống cũ thường cần kiểm soát chặt |
| **Đội ngũ nhỏ, cần lên production nhanh** | ✅ Dùng framework (OpenAI Agents SDK) | SDK gọn, ít boilerplate, dễ maintain |
| **Bạn muốn học sâu cách agent hoạt động** | ✅ Tự xây từ đầu | Hiểu từng mảnh ghép trước, rồi dùng framework sau sẽ tốt hơn nhiều |
| **Bạn cần tối ưu hiệu năng cực kỳ, giảm latency** | ⚠️ Tự xây hoặc framework + tuning | Framework thêm overhead; tự xây cho tối ưu sát nhất |
| **Nghiên cứu multi-agent, muốn thử nghiệm kiến trúc mới** | ✅ AutoGen hoặc tự xây | AutoGen mạnh về hội thoại multi-agent; tự xây khi cần thử điều không có sẵn |
| **Dự án cần bảo trì dài hạn, team lớn** | ⚠️ Cân nhắc kỹ: framework có đỡ nổi không? | Framework có thể thành nỗi đau khi breaking change; cần đánh giá độ trưởng thành |

**Quy tắc đúc kết:**

- Dùng framework khi **thời gian quan trọng hơn kiểm soát**.
- Tự xây khi **kiểm soát quan trọng hơn thời gian** hoặc khi bạn đang **học**.
- **Luôn hiểu ít nhất một framework bên trong** — không phải để dùng, mà để hiểu mối liên hệ giữa các mảnh ghép.

> **Tóm gọn 1 câu:** Dùng framework khi cần nhanh, tự xây khi cần kiểm soát — nhưng luôn hiểu ít nhất một framework bên trong để biết cách các mảnh ghép kết nối với nhau.

---
## Tóm Tắt & Checklist

### Nội dung đã học trong module này

1. **Build Agent from Scratch** nghĩa là tự lắp ghép bốn mảnh ghép cốt lõi: LLM (bộ não), Tools (tay chân), Memory (trí nhớ), và Agent Loop (vòng lặp suy nghĩ → hành động → quan sát → lặp).
2. **Framework** đóng gói những mảnh ghép này thành API và công thức có sẵn — giúp ra món nhanh nhưng đánh đổi bằng mức kiểm soát và khả năng khác biệt.
3. **5 framework lớn** có mỗi cách tư duy riêng: LangChain (orchestration đa năng), LangGraph (graph trạng thái), CrewAI (đội nhóm vai trò), AutoGen (multi-agent hội thoại), OpenAI Agents SDK (gọn hiện đại).
4. **Framework ≠ Runtime ≠ SDK** — ba khái niệm phục vụ ba mục đích khác nhau và thường dùng kết hợp với nhau trong một hệ thống production.
5. **Chọn framework khi** cần prove concept nhanh, cần agent phức tạp, hoặc đội ngũ nhỏ cần lên production nhanh.
6. **Chọn tự xây khi** cần kiểm soát sâu, tối ưu hiệu năng, hoặc đang học để hiểu cách các mảnh ghép kết nối bên trong.

### Checklist tự kiểm tra

Bạn đã nắm được khi có thể trả lời lưu loát các câu hỏi sau:

- [ ] Trình bày được bốn thành phần cốt lõi của một agent và vòng lặp của chúng?
- [ ] Giải thích được "framework" nghĩa là gì bằng một câu chuyện cụ thể (ví dụ: nhà hàng)?
- [ ] So sánh được năm framework (LangChain, LangGraph, CrewAI, AutoGen, OpenAI Agents SDK) theo điểm mạnh, yếu, và tình huống dùng?
- [ ] Phân biệt được Framework vs Runtime vs SDK bằng ví dụ thực tế?
- [ ] Đưa ra được quyết định dùng framework hay tự xây dựa trên tình huống cụ thể của dự án?
- [ ] Giải thích được tại sao hiểu Build Agent from Scratch vẫn quan trọng dù bạn định dùng framework?

---

## Tóm Gọn Toàn Module

> **Một câu để nhớ mãi:** Framework là "công thức đóng gói" giúp bạn nấu agent nhanh; tự xây là "nấu từ đầu" cho bạn kiểm soát trọn vẹn — nhưng dù chọn cách nào, hiểu các mảnh ghép cốt lõi (LLM, Tools, Memory, Loop) mới là điều thực sự quan trọng.

**Đi tiếp:** Module 14 sẽ giới thiệu **MCP — Model Context Protocol** — giao thức chuẩn để agent giao tiếp với các công cụ và nguồn dữ liệu bên ngoài một cách nhất quán, an toàn và có kiểm soát. Đây là bước tiến lớn giúp hệ sinh thái agent không còn phải "tự chế" kết nối mỗi lần.
