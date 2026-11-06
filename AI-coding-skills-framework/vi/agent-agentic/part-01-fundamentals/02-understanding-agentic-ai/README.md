# 🤖 Module 2. Understanding Agentic AI

> ## 📑 Mục Lục
>
> - [Câu Chuyện Mở Đầu](#câu-chuyện-mở-đầu)
> - [1. Agentic AI là gì?](#1-agentic-ai-là-gì)
> - [2. Agent vs Agentic AI](#2-agent-vs-agentic-ai)
> - [3. Agentic Workflow là gì?](#3-agentic-workflow-là-gì)
> - [4. Autonomous AI là gì?](#4-autonomous-ai-là-gì)
> - [5. AI Automation vs Agentic Automation](#5-ai-automation-vs-agentic-automation)
> - [6. Reactive vs Proactive Agent](#6-reactive-vs-proactive-agent)
> - [7. Single-Agent vs Multi-Agent](#7-single-agent-vs-multi-agent)
> - [8. Human-in-the-loop vs Human-out-of-the-loop](#8-human-in-the-loop-vs-human-out-of-the-loop)
> - [9. Mức Độ Tự Chủ (Autonomy Levels)](#9-mức-độ-tự-chủ-autonomy-levels)
> - [Tóm Tắt & Checklist](#tóm-tắt--checklist)

---

## Câu Chuyện Mở Đầu

Hãy tưởng tượng hai nhà hàng, mỗi nơi mua một "bếp máy" cực thông minh để nấu giúp các món đặc sản:

- **Nhà hàng A:** Bếp máy chạy theo một **công thức được lập trình từ trước**. Nhận đơn "phở bò" → mở đúng tủ lạnh số 3 → lấy đúng 200g thịt → nấu đúng 6 phút → bê ra. Hôm nào thiếu thịt bò thì **nó đứng im báo lỗi**, kêu đầu bếp xuống gỡ rối. Món nào cũng ra y hệt — nhưng chỉ đúng trong kịch bản đã dựng sẵn.
- **Nhà hàng B:** Bếp máy **hiểu mục tiêu** là "phục vụ khách món ngon đúng giờ". Trước giờ cao điểm nó **chủ động** rà tủ lạnh, thấy thiếu thịt bò thì **tự đề xuất** thay bằng gà, **lập kế hoạch** nấu sẵn món rau, đến khi nêm nếm hơi mặn thì **tự điều chỉnh**. Chỉ những món đắt tiền, hỏng một cái là phí cả buổi — nó mới **hỏi lại đầu bếp trước khi làm**.

Cả hai đều "tự nấu". Nhưng nhà hàng A chỉ **tự làm theo kịch bản** (automation), còn nhà hàng B có **tính agentic** — tự đưa ra quyết định, tự lập kế hoạch, tự điều chỉnh, và biết lúc nào phải dừng lại nhờ người duyệt.

> **Tóm gọn 1 câu:** Module này trả lời cho một câu: khi nào AI của bạn chỉ là "cỗ máy chạy đúng kịch bản", và khi nào nó thực sự **tự chủ** — nhận mục tiêu, tự quyết cách làm, tự sửa sai giữa đường.

---

## 1. Agentic AI là gì?

Ở Module 1 ta biết một **Agent** là *một chương trình* — một LLM tự chủ dùng công cụ trong vòng lặp. Vậy **Agentic AI** là gì, và vì sao lại cần thêm một thuật ngữ mới?

**Agentic AI** không chỉ là một chương trình đơn lẻ. Đó là **một khuynh hướng thiết kế** — cách ta nghĩ về AI như một "tác nhân chủ động" thay vì một "cỗ máy trả lời". Một hệ thống được gọi là *agentic* khi nó có ba khả năng:

- **Tự quyết định hành động:** không làm đúng theo từng lệnh, mà tự chọn bước tiếp theo để đạt mục tiêu (chọn công cụ nào, gọi API nào, xử lý file nào).
- **Tự lập kế hoạch:** chia mục tiêu lớn thành chuỗi việc nhỏ có thứ tự, thậm chí tự lên lịch thực hiện.
- **Tự điều chỉnh:** quan sát kết quả từng bước, nếu sai hướng thì đổi kế hoạch, thử cách khác, rút kinh nghiệm.

Ngược lại, một hệ thống *không* agentic dù có dùng LLM thì vẫn chạy theo lối "hỏi – đáp": bạn đưa input, nó trả output, rồi dừng. Nó không tự quyết điều gì ngoài phạm vi câu hỏi.

> **Tóm gọn 1 câu:** Agentic AI = triết lý xây AI có *ý chí*: tự quyết hành động, tự lập kế hoạch, tự sửa sai — hướng tới mục tiêu chứ không chờ từng lệnh.

---
## 2. Agent vs Agentic AI

Đây là cặp dễ nhầm nhất khi mới học. Hai chữ giống nhau, nhưng khác tầng:

- **Agent** là **một chương trình cụ thể** — một đối tượng bạn cài đặt, chạy, tắt. Ví dụ: một `research agent`, một con bot tự sửa bug trong repo. Nó có tên, có file code, có config riêng.
- **Agentic AI** là **triết lý / khuynh hướng thiết kế** — một cách suy nghĩ về cách xây AI nói chung. Bạn có thể có một hệ thống "agentic" mà bên trong chẳng có cái agent đẹp đẽ nào cả (chỉ là một LLM được bọc trong vòng lặp quyết định).

Dễ nhớ bằng phép so sánh:

| | **Agent** | **Agentic AI** |
|---|---|---|
| **Bản chất** | Một thực thể / chương trình cụ thể | Một đặc tính / triết lý thiết kế |
| **Trả lời câu hỏi** | "Cái gì đang chạy?" → con bot X | "Cách nào?" → tự chủ, có mục tiêu |
| **Đếm được?** | Có — "3 agent đang chạy" | Không — "hệ thống này có tính agentic" |
| **Ví dụ** | Claude Code, một triage bot | Thiết kế một pipeline cho AI tự điều chỉnh |

*Cách đọc: dòng trên là thứ cụ thể đang chạy; dòng dưới là cách thiết kế nó.*

Nói đơn giản: **Agent là danh từ, Agentic là tính từ.** Bạn build *agent*, và bạn build chúng theo khuynh hướng *agentic*.

> **Tóm gọn 1 câu:** Agent = một chương trình cụ thể (danh từ); Agentic = triết lý xây AI tự chủ, có mục tiêu (tính từ) — bạn dùng triết lý agentic để thiết kế các agent.

---

## 3. Agentic Workflow là gì?

**Agentic Workflow** là một *quy trình làm việc* mang tính agentic: thay vì chạy một lần "input → output", nó là **một chuỗi nhiều bước, có thể lặp lại, và mỗi bước đều có sự tự quyết định**.

Ba đặc điểm phân biệt:

- **Nhiều bước lặp:** suy nghĩ → hành động → quan sát kết quả → quyết định bước kế — vòng lặp này lặp đi lặp lại tới khi đạt mục tiêu hoặc bỏ cuộc.
- **Tự quyết giữa chừng:** công cụ nào, thứ tự nào, dừng khi nào — đều do hệ thống tự chọn, không được viết cứng từ trước.
- **Thích nghi:** gặp lỗi thì không chết, mà đổi hướng, thử cách khác.

Ví dụ so sánh để dễ hình dung:

- **Workflow thường:** "Đọc email → nếu có đính kèm PDF thì lưu vào Drive → gửi email xác nhận." Mỗi email trị như nhau, làm mãi một kiểu.
- **Agentic workflow:** "Nhận mục tiêu 'dọn hòm thư quý' → phân loại từng email → email khiếu nại thì tự tìm hóa đơn liên quan để đối chiếu → trả lời theo từng dạng khách → nếu thiếu thông tin thì tự hỏi lại → cuối cùng tổng kết." Mỗi email là một "con đường" riêng, tự quyết, tự kiểm.

Đây là mảnh ghép lý thuyết quan trọng vì toàn bộ Part III của giáo trình (các *workflow patterns*, thiết kế planning, decision making) chính là nói về cách xây những quy trình này — bạn **sẽ học kỹ ở Module 9–12**.

> **Tóm gọn 1 câu:** Agentic workflow = một quy trình gồm nhiều bước lặp, mỗi bước hệ thống tự quyết định và tự điều chỉnh, chạy đến khi hoàn thành mục tiêu.

---

## 4. Autonomous AI là gì?

**Autonomous AI** (AI tự trị / tự hành) là AI **tự hành động mà không cần con người can thiệp liên tục**. Từ "autonomy" nghĩa là *tự chủ, tự cai quản* — như xe tự lái, drone tự bay: vào nhiệm vụ là tự lo, người chỉ can thiệp khi có sự cố lớn hoặc khi cần duyệt bước rủi ro.

Cần phân biệt hai khái niệm hay đi cùng nhau:

- **Autonomy (tự trị)** nói về *ai ra quyết định*: hệ thống có được tự chọn bước đi, hay phải chờ lệnh/duyệt?
- **Agentic (agentic)** nói về *cách hành động*: hệ thống có lập kế hoạch, dùng công cụ, thích nghi với mục tiêu hay không?

Một hệ thống có thể tự trị nhưng không agentic (một con robot làm đúng một việc lặp lại trên dây chuyền, tự chạy không ai xem — tự trị nhưng không biết lập kế hoạch). Và ngược lại, một hệ thống rất agentic (mưu mô lập kế hoạch giỏi) nhưng lại bị gò vào mức tự chủ thấp — mỗi bước đều phải hỏi người duyệt.

**Điểm mấu chốt:** autonomy là một **thang đo, không phải công tắc bật/tắt**. "Bao nhiêu tự chủ" mới là câu hỏi đúng — và đó chính là nội dung của Mục 9 ở cuối module này.

> **Tóm gọn 1 câu:** Autonomous AI = AI tự hành động không cần can thiệp liên tục; autonomy là thang đo "ai quyết định" — tách biệt với tính agentic là "hành động thế nào".

---
## 5. AI Automation vs Agentic Automation

**AI Automation** (tự động hóa bằng AI) và **Agentic Automation** (tự động hóa agentic) nghe na ná nhau, nhưng khác nhau đúng ở đặc tính đã bàn: *kịch bản cố định* vs *tự chọn hành động*.

- **AI Automation:** dùng AI/thuật toán bên trong một *luồng cố định đã được định nghĩa từ trước*. AI giúp xử lý từng chặng, nhưng **ai làm gì, làm theo thứ tự nào thì coder đã vẽ sẵn**. Ví dụ: một pipeline tự chuyển chữ ký hóa đơn — AI đọc hóa đơn, nhưng bước sau luôn là "ghi vào bảng", bước sau nữa luôn là "gửi mail". Nếu sự kiện nằm ngoài kịch bản, pipeline **dừng hoặc rơi vào nhánh xử lý mặc định**.
- **Agentic Automation:** hệ thống **tự chọn hành động tiếp theo** dựa trên quan sát, có thể đổi thứ tự, đổi công cụ, thậm chí đổi cả kế hoạch ban đầu khi gặp tình huống mới. Ví dụ: một agent xử lý khiếu nại — gặp email mơ hồ thì tự quyết "cần hỏi lại khách", gặp email rõ ràng thì tự giải quyết luôn.

Bảng so sánh nhanh:

| | **AI Automation** | **Agentic Automation** |
|---|---|---|
| **Kịch bản** | Cố định, viết từ trước | Tự sinh, tự điều chỉnh |
| **Ai chọn bước kế?** | Nhà phát triển | Hệ thống (agent) |
| **Bước ngoài dự kiến** | Dừng / theo nhánh mặc định | Tự quyết cách mới |
| **Phù hợp** | Quy trình ổn định, nhiều lần | Tác vụ biến động, ít lặp y hệt |
| **Chi phí vận hành** | Thấp, dễ đoán | Cao hơn, khó đoán hơn |

> **Tóm gọn 1 câu:** AI Automation chạy theo kịch bản cố định (AI là tay làm trong dây chuyền), còn Agentic Automation để AI tự chọn bước đi — phù hợp việc khó lường, ít lặp lại.

---

## 6. Reactive vs Proactive Agent

Cách phân loại này nói về **thời điểm agent bắt đầu hành động**:

- **Reactive Agent (phản ứng):** *phản ứng theo kích thích từ môi trường*. Có sự kiện mới → mới xử lý. Ví dụ: bot trả lời ticket — chỉ hoạt động khi có ticket mới. Nó không làm gì nếu không có gì xảy ra.
- **Proactive Agent (chủ động):** *chủ động hành động để dự đoán và ngăn ngừa vấn đề*, không chờ sự kiện xảy ra. Ví dụ: agent giám sát hệ thống — chủ động quét log, nhận ra dấu hiệu sắp đầy đĩa và tự dọn trước khi xảy ra sự cố, hoặc chủ động đề xuất việc cần làm khi không ai nhờ.

| | **Reactive Agent** | **Proactive Agent** |
|---|---|---|
| **Bắt đầu khi nào?** | Có kích thích / sự kiện tới | Tự khởi động, theo lịch hoặc dự đoán |
| **Mục tiêu** | Đáp ứng đúng, xử lý nhanh | Phòng ngừa, tận dụng cơ hội |
| **Ví dụ** | Bot xử lý email mới | Agent rà lỗi bảo mật định kỳ |
| **Rủi ro** | Bỏ sót việc chưa có kích thích | Tốn chi phí khi chạy không cần thiết |
| **Thường đi với** | Tác vụ "hỏi–đáp" theo yêu cầu | Loop chạy theo lịch, giám sát 24/7 |

*Cách đọc: Reactor chờ tín hiệu, Proactor tự đi phát hiện tín hiệu.* Trong thực tế hai trạng thái không loại trừ nhau — nhiều hệ thống phản ứng nhanh với cảnh báo (reactive) *và* định kỳ tự rà soát (proactive).

> **Tóm gọn 1 câu:** Reactive agent chờ "khách gọi" mới làm; Proactive agent tự "mở cửa hàng" trước, chủ động dự đoán và ngăn ngừa vấn đề.

---
## 7. Single-Agent vs Multi-Agent

Câu hỏi ở đây là kiến trúc: **một agent cáng hết mọi việc**, hay **nhiều agent chia việc, phối hợp với nhau**.

- **Single-Agent (đơn agent):** một agent đảm nhận cả quy trình — tự phân tích, tự lập kế hoạch, tự gọi công cụ. Đơn giản, dễ debug, chi phí dễ đoán. Phù hợp tác vụ vừa, một luồng xử lý.
- **Multi-Agent (đa agent):** nhiều agent, mỗi con một vai — ví dụ một *supervisor* chia việc, một *researcher* đi tìm thông tin, một *writer* soạn nội dung, một *reviewer* kiểm tra rồi gửi ngược lại. Mạnh cho tác vụ lớn, nhiều chuyên môn khác nhau, nhưng phức tạp hơn hẳn: phải lo giao tiếp, tránh lặp việc, xử lý mâu thuẫn kết quả.

| | **Single-Agent** | **Multi-Agent** |
|---|---|---|
| **Số "người làm"** | 1 | Nhiều, mỗi con một vai |
| **Độ phức tạp** | Thấp, dễ debug | Cao — phải lo giao tiếp & phối hợp |
| **Chuyên môn hóa** | Hạn chế | Tốt — mỗi agent giỏi một việc |
| **Chi phí** | Dễ đoán | Khó đoán, dễ dư thừa |
| **Khi nào dùng** | Tác vụ vừa, một luồng | Tác vụ lớn, nhiều mảng khác nhau |

*Cách đọc: đơn agent = một người đa năng; đa agent = một đội ngũ chuyên môn hóa, cần người điều phối.*

Lưu ý: **đừng vội chọn multi-agent.** Cộng đồng thường khuyên đi từ single-agent trước; chỉ tách nhiều agent khi thực sự cần chuyên môn hóa hoặc giảm tải. Bạn **sẽ học chi tiết sự phối hợp, phân quyền (delegation), giao tiếp giữa các agent ở Module 12** — và cách dựng chúng bằng framework ở Module 13.

> **Tóm gọn 1 câu:** Single-agent = một người làm hết mọi việc; multi-agent = đội ngũ chuyên môn hóa phối hợp với nhau — bắt đầu từ single-agent, chỉ lên multi-agent khi thật cần.

---

## 8. Human-in-the-loop vs Human-out-of-the-loop

Câu hỏi đặt ra: **người có nằm trong vòng lặp ra quyết định không?**

- **Human-in-the-loop (HiL):** con người **ở trong vòng lặp** — agent có thể đề xuất, làm nháp, nhưng **bước quan trọng phải có người duyệt** (human approval) trước khi thực thi. Ví dụ: agent soạn email trả lời khách nhưng phải để người gật đầu mới gửi.
- **Human-out-of-the-loop (HoL):** con người **đứng ngoài vòng lặp** — agent thực thi tới cùng, chỉ người được thông báo kết quả (hoặc người không cần tham dự gì). Ví dụ: agent chạy test tự sửa bug nhỏ trên repo phụ rồi tự tạo PR; không ai chặn giữa chừng.

Bảng so sánh giúp chọn đúng khi nào dùng gì:

| | **Human-in-the-loop** | **Human-out-of-the-loop** |
|---|---|---|
| **Ai quyết bước rủi ro?** | Con người duyệt trước khi làm | Agent tự quyết, tự thực thi |
| **Tốc độ** | Chậm hơn (chờ người) | Nhanh, liên tục |
| **An toàn / kiểm soát** | Cao — người gác cổng | Thấp hơn — phải có guardrail bù |
| **Tốn công người** | Cao (ngồi duyệt) | Thấp (chỉ xem báo cáo) |
| **Dùng khi** | Việc rủi ro cao, sai khó hồi phục | Việc lặp nhỏ, hậu quả thấp, đã chứng minh ổn |

*Cách đọc: HiL đánh đổi tốc độ lấy an toàn; HoL đánh đổi an toàn lấy tốc độ — nên pha trộn: trong một hệ thống, bước rủi ro để HiL, bước an toàn để HoL.*

Điểm cốt lõi: HiL vs HoL không phải "tốt hay xấu" — mà là **lựa chọn đánh đổi theo mức rủi ro**. Đây chính là nền tảng để hiểu *Autonomy Levels* ngay sau đây.

> **Tóm gọn 1 câu:** HiL = người duyệt các bước quan trọng trước khi agent thực thi; HoL = agent tự chạy, người chỉ xem kết quả — chọn theo mức rủi ro và khả năng hồi phục.

---
## 9. Mức Độ Tự Chủ (Autonomy Levels)

Gom toàn bộ các khái niệm trên lại bằng một **thang đo tự chủ**: cho agent được tự làm tới đâu. Khái niệm này không chỉ là lý thuyết — trong repo này, phần **Loop Engineering** (`loop/`) đã dùng chính thang này làm "bằng lái" cho các loop chạy tự động. Tham khảo `loop/01-concepts` (Mức Tự Chủ L1 → L2 → L3).

Thang phổ biến nhất được dùng xuyên suốt giáo trình:

| Mức | Tên | Agent được làm gì? | Ví dụ |
|---|---|---|---|
| **L0** | Draft | Chỉ ghi ý định, chưa hành động | Ghi kế hoạch việc hôm nay |
| **L1** | Report-only | Chỉ quan sát rồi báo cáo; **không tự sửa, không tự hành động** | Loop rà số issue, chỉ liệt kê lên |
| **L2** | Assisted | Hành động **có duyệt** — tự đề xuất, tự làm nháp, người kiểm lại | Agent sửa bug nhỏ, tạo PR chờ người duyệt |
| **L3** | Unattended | Tự chạy **không cần can thiệp**, tự quyết, tự thực thi | Agent tự dọn log, tự gộp PR khi test xanh |

*Cách đọc: đi từ trên xuống, quyền tự quyết tăng dần; L1 chỉ báo cáo, L2 hành động có duyệt (đúng phái Human-in-the-loop), L3 tự chạy (đúng phái Human-out-of-the-loop).*

Ba nguyên tắc quan trọng để không "đốt nhà":

- **Tự chủ là giấy phép kiếm bằng bằng chứng, không phải huy chương.** Không ai bật L3 ngay ngày đầu. Phải qua L1 vài tuần cho ổn định, rồi L2, khi đủ tin cậy mới lên L3.
- **Lên từng nấc, hạ cũng từng nấc.** Có sự cố, chi phí tăng vọt → hạ ngay về mức thấp hơn. Luôn có đường lui (kill switch).
- **Mức tự chủ ≠ mức kỹ năng.** Agent làm giỏi một việc ở L3 vẫn có thể chưa được phép chạm việc khác. Tự chủ cao phải đi kèm guardrail (denylist, ngân sách, giới hạn thử lại).

Ví dụ thực tế để rõ: một *PR babysitter* có thể bắt đầu ở **L1** (mỗi 10 phút xem PR mới, chỉ báo cáo và gợi ý), lên **L2** (soạn được patch nhỏ nhưng để người duyệt), và chỉ lên **L3** khi đã chứng minh qua nhiều tuần không gây hại — chạy tự động cả đêm không ai canh.

> **Tóm gọn 1 câu:** Autonomy Levels là thang L0→L3 đo "agent được tự làm tới đâu": L1 chỉ báo cáo, L2 hành động có duyệt, L3 tự chạy — nâng cấp bằng bằng chứng, luôn có đường hạ cấp khi có sự cố.

---

## Tóm Tắt & Checklist

### Nội dung đã học trong module này

1. **Agentic AI** là triết lý xây AI có ý chí: tự quyết định hành động, tự lập kế hoạch, tự điều chỉnh.
2. **Agent** là chương trình cụ thể (danh từ); **Agentic AI** là triết lý thiết kế (tính từ).
3. **Agentic workflow** là chuỗi nhiều bước lặp, mỗi bước tự quyết định và thích nghi.
4. **Autonomous AI** tự hành động không cần can thiệp liên tục — autonomy là thang đo "ai quyết định".
5. **Agentic automation ≠ AI automation** (tự chọn hành động vs chạy kịch bản cố định); **reactive ≠ proactive** (chờ kích thích vs chủ động dự đoán).
6. **Single vs multi-agent** và **HiL vs HoL** là những quyết định kiến trúc — được "chốt" bằng **Autonomy Levels L1–L3**.

### Checklist tự kiểm tra

Bạn đã nắm được khi có thể trả lời lưu loát các câu hỏi sau:

- [ ] Giải thích được điểm khác giữa "một Agent" và "Agentic AI" bằng ví dụ của riêng bạn?
- [ ] Vẽ phác được một *agentic workflow* gồm 3–4 bước có tự quyết định và tự điều chỉnh?
- [ ] Phân biệt được AI Automation và Agentic Automation bằng một tình huống cụ thể?
- [ ] Cho 2 ví dụ reactive agent và 2 ví dụ proactive agent ngoài đời thực?
- [ ] Giải thích khi nào nên dùng Human-in-the-loop và khi nào chấp nhận Human-out-of-the-loop?
- [ ] Sắp xếp được một tác vụ của bạn vào đúng mức L1 / L2 / L3 và nêu lý do?

---

## Tóm Gọn Toàn Module

> **Một câu để nhớ mãi:** Module 1 cho bạn một *Agent*; module này cho bạn *tính agentic* — triết lý để AI tự quyết, tự lập kế hoạch, tự sửa sai. Và "tự chủ" không phải công tắc bật/tắt, mà là thang **L1 báo cáo → L2 có duyệt → L3 tự chạy** — lên bằng bằng chứng, hạ ngay khi có sự cố.

**Đi tiếp:** Module 3 sẽ mở "tủ động cơ" — **Agent Lifecycle & Core Principles** (Perceive → Reason → Plan → Act → Observe), vòng lặp phản hồi, hành vi hướng mục tiêu và điều kiện dừng — những khối cơ bản biến "ý chí agentic" thành một agent thực sự biết chạy.
