# ❓ FAQ — LangChain / LangGraph (chuyện thật, dễ hiểu)

Nếu câu hỏi nào khó hiểu thì đọc `../README.md` phần trong ngoặc vuông.

---

## Q1. Tôi cần cả LangChain lẫn LangGraph không, hay cài một cái là đủ? [→ Tổng Quan]

**Bạn sẽ thấy**

Bạn chỉ muốn làm một việc đơn giản: hỏi tài liệu của công ty và trả lời. Nhưng tài liệu hướng dẫn nhắm hai tên package và còn nói tới `StateGraph`, `add_conditional_edges`, `MemorySaver` — bạn không biết cái nào là bắt buộc, cái nào để sau.

**Vì sao**

Hai tên này là hai tầng khác nhau. LangChain là lớp nền: bọc model (`ChatOpenAI`, `ChatAnthropic`), định nghĩa tool (`@langchain/core/tools`), template prompt, retriever, và lịch sử hội thoại (`InMemoryChatMessageHistory`). LangGraph là lớp điều phối: nó cầu nối các thứ trên thành một **đồ thị có trạng thái** (`StateGraph`) — mỗi node là một phần của harness, có cạnh điều kiện và có vòng lặp. Cài LangGraph là đã có sẵn phần nền bạn cần, nên gần như không có tình huống phải chọn "chỉ LangChain".

**Làm gì**

1. Muốn nhanh, chỉ một lượt gọi: dùng phần nền, không cần `StateGraph`.

```typescript
import { DynamicStructuredTool } from "@langchain/core/tools";
const search = new DynamicStructuredTool({
  name: "search", description: "Search the web",
  func: async (input) => { /* ... */ },
});
```

2. Muốn agent tự lặp lại: tool → kết quả → lại nghĩ → có thể gọi tool tiếp, thì phải có `StateGraph` với một cạnh quay về. Đây là khác biệt lớn nhất so với việc gọi model một lần rồi tự kết thúc.
3. Chỉ nhớ trong một phiên làm việc: `InMemoryChatMessageHistory` là đủ. Muốn nhớ xuyên phiên và cần dừng giữa chừng rồi tổi tụi lại: `MemorySaver`.
4. Không cài sẵn mấy trăm gói tích hợp; chỉ cài những gói bạn dùng.

**Kiểm tra**

Chạy hai bản cùng một task: bản một lượt gọi, bản có `StateGraph`. Xác nhận bản `StateGraph` thật sự quay lại node model sau khi node tool trả kết quả — nếu chỉ chạy node tool rồi kết thúc thì đồ thị của bạn chưa có vòng lặp.

---

## Q2. Vòng lặp trong `StateGraph` không dừng, cứ chạy mãi — debug ở đâu? [→ LangGraph (Orchestration)]

**Bạn sẽ thấy**

Agent gọi tool, nhận kết quả, lại gọi tool, lại nhận kết quả... Mỗi vòng đều trông hợp lý ("tôi cần thêm dữ liệu"), nhưng không bao giờ tới đáp án. Token tăng đều đặn, câu trả lời cuối cùng không bao giờ xuất hiện.

**Vì sao**

Vì trong đồ thị có **hai loại cạnh khác nhau** và nếu lẫn lộn thì không có đường thoát. Cạnh thường (`add_edge`) là đi thẳng, không kiểm tra gì — đi sai là chạy vòng mãi. Cạnh điều kiện (`add_conditional_edges`) là chỗ duy nhất để quyết định dừng: hàm `should_continue` trả về `"tools"` thì sang node tool, trả về `END` thì hết. Nếu `should_continue` luôn trả `"tools"`, hoặc lời gọi tool vẫn trả về kết quả giống lần trước khiến agent nghĩ chưa xong, thì đồ thị không có đường về `END`.

**Làm gì**

1. Kiểm tra `should_continue` có nhánh `END` thật không, và điều kiện dừng có dựa trên tiến trình thật chứ không phải cảm giác.
2. Tách rõ hai cạnh: node agent kết thúc bằng cạnh điều kiện, node tool quay về agent bằng cạnh thường.

```python
graph.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})
graph.add_edge("tools", "agent")   # vòng lặp — giống loop/
```

3. Đặt trần số lượt cho đồ thị. Nếu trần không có, một agent hỏi lại cùng một thứ sẽ đốt hết ngân sách.
4. Kiểm tra công cụ có trả về thông tin "không tìm thấy gì" không. Công cụ luôn trả kết quả có vẻ hữu ích là nguyên nhân vòng lặp vô hạn phổ biến nhất.
5. Nếu vòng lặp dài hơn 2 vòng mà chưa có kết quả, hãy coi đó là lỗi dữ liệu hoặc lỗi công cụ, không phải lỗi model.

**Kiểm tra**

Chạy một task đã biết đáp án, đặt trần thấp như 5 lượt, và ghi lại trạng thái sau mỗi vòng. Lần gần nhất phải có lý do dừng ghi lại được. Nếu không có lý do dừng mà bị cắt bởi trần, hệ thống của bạn chưa biết khi nào đã xong.

---

## Q3. Harness RAG thì gắn `Retriever` và nén context vào node nào? [→ Case Studies 1, Quan Hệ Với Harness]

**Bạn sẽ thấy**

Bạn đã có cơ sở dữ liệu tài liệu nhưng agent trả lời sai. Câu hỏi không tìm thấy gì, hoặc tìm thấy 40 đoạn văn dài thếch đi vào model và lời đáp chìm giữa đống đó.

**Vì sao**

Vì lấy tài liệu và làm gọn tài liệu là **hai việc khác nhau ở hai node khác nhau**. Node lấy kiến thức (harness/01) gọi retriever và trả về danh sách đoạn văn thô — càng nhiều càng tốt để không bỏ sót. Node dựng context (harness/02) mới là chỗ phải lọc và nén lại. Làm hai việc này chung một node là nguyên nhân điển hình làm RAG "quên" hoặc "chìm". `ContextualCompressionRetriever` sinh ra đúng để cắt phần thừa trước khi tốn token.

**Làm gì**

1. Node `retrieve`: lấy thật nhiều, không cắt — cắt ở đây là mất dữ liệu không thể khôi phục.
2. Node `build`: nén lại, giữ đúng phần liên quan, chuẩn bị cho prompt.
3. Node prompt (harness/05): dán các đoạn đã nén vào `ChatPromptTemplate`.
4. Nếu câu hỏi ngoài phạm vi tài liệu, hãy để agent nói không biết thay vì đoán.

**Làm gì — lắp vào node nào**

```
harness/01-retrieve → Chroma retriever (xem tools/vector-db/)
harness/02-build    → ContextualCompressionRetriever (nén context)
harness/05-prompt   → ChatPromptTemplate với retrieved docs
harness/06-tool     → ToolNode gọi web_search, query_db
```

**Kiểm tra**

Đặt câu hỏi có câu trả lời nằm ngoài tài liệu. Agent phải nói không có thông tin, không được bịa dựa trên các đoạn văn được lấy về. Đặt câu hỏi có đáp án và so số đoạn văn đi vào prompt trước và sau khi nén.

---

## Q4. "700+ integrations" — có phải tôi phải cài hết không? [→ Tại Sao LangChain Quan Trọng]

**Bạn sẽ thấy**

Câu quảng cáo của framework là có hơn 700 tích hợp sẵn. Bạn bắt đầu lo: cài cái gì trước, cái nào thật sự cần, và có phải thiếu một cái nào đó là dự án hỏng không.

**Vì sao**

Vì con số 700 đếm **số tích hợp có sẵn trong hệ sinh thái**, không phải số thứ bạn phải cài. Điều bạn thật sự cần cho một harness chỉ khoảng bảy thứ, và mỗi thứ đã có một module cụ thể. Một agent viết code chỉ cần vài món, cài thêm chỉ làm chậm dự án và mở rộng bề mặt lỗi.

| Phần harness | Chỉ cần thứ này |
|---|---|
| 01, 03 memory | `MemorySaver`, `InMemoryChatMessageHistory` |
| 02 dựng context | `ContextualCompressionRetriever` |
| 05 sinh prompt | `ChatPromptTemplate` |
| 06 chọn & chạy tool | `ToolNode`, `DynamicStructuredTool` |

**Làm gì**

1. Cài đúng số thứ trong bảng trên. Không cài hết.
2. Chỉ thêm gói khi bạn thật sự cần: vector DB, trình theo dõi, adapter MCP.
3. Mỗi tích hợp mới là thêm một chỗ có thể hỏng và thêm một chỗ phải theo dõi. Không dùng thì đừng cài.
4. Ghi lại danh sách gói đang dùng cùng phiên bản, vì cập nhật framework hay làm đổi cách gọi.

**Kiểm tra**

Thử xoá (không cài) các gói tích hợp không dùng rồi chạy lại task thật của bạn. Nếu vẫn chạy, bạn đang cài thừa. Nếu hỏng, hãy xem hỏng vì tích hợp bị dùng ngầm — đó là dấu hiệu kiến trúc của bạn phụ thuộc vào thứ không kiểm soát.

---

## Q5. Tài liệu vừa có code TypeScript vừa có Python — nên học ngôn ngữ nào? [→ Tổng Quan, Lộ Trình Học]

**Bạn sẽ thấy**

Trong cùng một tài liệu, ví dụ dựng tool viết bằng TypeScript còn ví dụ vẽ đồ thị viết bằng Python. Bạn đang phân vân nên chọn ngôn ngữ nào để đi tiếp, và sợ chọn sai rồi phải làm lại.

**Vì sao**

Hai ví dụ khác nhau về nơi chúng được dùng. Phần định nghĩa tool và gọi model được viết bằng TypeScript (dùng `import { ChatOpenAI } from "@langchain/openai"`), vì đó là phần hay nằm cạnh code sản phẩm. Phần điều phối đồ thị được viết bằng Python (dùng `from langgraph.graph import StateGraph, END`), vì đó là phần hay nằm cạnh script chạy thử và phân tích. Không có mâu thuẫn — chỉ là mỗi tầng được viết bằng ngôn ngữ quen thuộc với người làm việc đó.

**Làm gì**

1. Chọn theo dự án của bạn: dự án web/JavaScript thì TypeScript; dự án Python hoặc làm phân tích thì Python.
2. Đừng dùng hai ngôn ngữ cho cùng một tầng chức năng — một harness hỗn hợp là hai lần số lỗi.
3. Trước khi cài, đọc đoạn code mẫu TypeScript trong `HARNESS_ENGINEERING.md` mục 9.1 — sẵn có, đừng viết lại từ đầu.
4. Bắt đầu ở tầng đơn giản nhất (`llm` + `tools` + `memory`), rồi mới chuyển sang `StateGraph` khi cần vòng lặp.

**Kiểm tra**

Chạy đoạn ví dụ tối thiểu bằng ngôn ngữ bạn chọn: một lời gọi model cộng với một tool. Nếu tool trả về kết quả và mô hình đọc được kết quả đó, bạn đã có nền để viết `StateGraph` sau đó.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: README.md.*