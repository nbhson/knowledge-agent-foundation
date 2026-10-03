# ❓ FAQ — Tools (chọn cái nào, bắt đầu từ đâu)

Nếu câu hỏi nào khó hiểu thì đọc `README.md` phần trong ngoặc vuông.

---

## Q1. Trong `tools/` có 9 thư mục con, tôi nên bắt đầu từ cái nào? [→ Lộ Trình Học]

**Bạn sẽ thấy**

Bạn mở thư mục này và thấy 9 thư mục con: `rtk`, `loop-cli`, `langchain`, `autogen`, `crewai`, `vector-db`, `mcp-ecosystem`, `guardrails`, `observability`, `evaluation`. Bạn không biết cái nào là nền, cái nào là gia vị, và bắt đầu từ đâu để không phí công học vô ích.

**Vì sao**

Vì 9 cái đó không cùng cấp: chúng phục vụ 4 nhóm vai trò khác nhau — công cụ tối ưu môi trường, framework viết harness, vector DB cho trí nhớ, và hệ sinh thái MCP cho kết nối tool — cộng thêm hai tầng chất lượng là an toàn và đo lường. Lộ trình 6 giai đoạn trong README xếp theo đúng thứ tự đó, và bắt đầu sai giai đoạn thì mọi giai đoạn sau đều xây trên nền chưa có.

**Làm gì**

1. Giai đoạn 1 — cài `rtk`. Đây là thứ cho hiệu quả ngay lập tức, không cần viết code.
2. Giai đoạn 2 — chọn một framework trong ba cái (xem Q3), thêm `vector-db` cho trí nhớ.
3. Giai đoạn 3–4 — `mcp-ecosystem` rồi `guardrails`.
4. Giai đoạn 5–6 — `observability` + `evaluation`, cuối cùng mới tới `loop-cli`.

```
GĐ1: rtk → GĐ2: framework + vector-db → GĐ3: mcp-ecosystem
→ GĐ4: guardrails → GĐ5: observability + evaluation → GĐ6: loop-cli
```

**Kiểm tra**

Sau giai đoạn 1, đo lượng token tiết kiệm được từ các lệnh lặp lại (xem Q6). Nếu chưa đo được gì thì đừng đi tiếp — bạn sẽ không biết các thay đổi sau giúp hay làm hại.

---

## Q2. Có phải tôi phải cài hết 9 cái không? [→ Lộ Trình Học, Tại Sao Tools Quan Trọng?]

**Bạn sẽ thấy**

Bạn nhìn cây thư mục đầy đủ và thấy cả framework, cả vector DB, cả MCP, cả tầng đo lường, rồi kết luận phải lấy hết. Cài xong thì dự án nặng, khởi động chậm, và bạn không dùng tới hai phần ba.

**Vì sao**

Vì đây là **bản đồ** chứ không phải **đề bài**. Lý do chính để có thư mục này là tách kiến thức khỏi công cụ: `harness/` giữ kiến thức, `loop/` giữ vòng lặp, `tools/` giữ phần cài đặt. Nhưng cái bạn lấy từ đây phải theo nhu cầu, không phải theo danh sách. Ba cái framework cùng làm một việc là lựa chọn, không phải ba cái đều cần.

| Bạn đang ở đâu | Chỉ cần |
|---|---|
| Mới bắt đầu, muốn thấy hiệu quả ngay | `rtk` |
| Đã có harness, muốn kết nối tool | `mcp-ecosystem` |
| Đã chạy thật, sợ hỏng ngoài dự kiến | `guardrails`, `evaluation` |
| Đã ổn định, mới đến giờ tự động hoá | `loop-cli` |

**Làm gì**

1. Chọn theo bảng trên, cài tối đa hai thứ mỗi lần.
2. Thêm framework khi đã có việc cụ thể cần orchestration — không cài trước cho "có sẵn".
3. Mỗi thư mục con đều có `README.md` riêng và cùng một bộ mục `01-concepts` → `05-troubleshooting`. Đọc `README.md` của thư mục đó, không cần đọc cả 9.
4. Ghi lại bạn đang dùng cái nào, để lần sau không phải dò lại.

**Kiểm tra**

Sau mỗi lần thêm, chạy task thật của bạn. Thứ bạn không dùng đến mà vẫn phải cấu hình (khoá, biến môi trường, endpoint) thì đó là thừa — gỡ ra.

---

## Q3. LangChain, AutoGen, CrewAI — chọn cái nào cho hệ thống của tôi? [→ Nhóm 2 — Framework]

**Bạn sẽ thấy**

Bạn cần một agent vừa trả lời câu hỏi, vừa gọi tool, vừa tự sửa code. Ba tài liệu framework đều viết rất hay, và cả ba đều nói là làm được việc đó.

**Vì sao**

Vì cả ba đều đúng, khác nhau ở đơn vị tổ chức. LangChain/LangGraph tổ chức thành **đồ thị có trạng thái**: mỗi node là một phần của harness, có cạnh điều kiện và vòng lặp — hợp nhất khi luồng của bạn đã biết trước. AutoGen tổ chức thành **cuộc trò chuyện** giữa các agent, mọi agent đều gọi được tool — hợp khi bạn muốn các vai trò thảo luận và tự sửa. CrewAI tổ chức thành **bảng công việc**: role, goal, backstory cho từng agent, cùng một `Crew` có `process` tuần tự hoặc có manager.

**Làm gì**

1. Biết trước luồng công việc → LangChain/LangGraph, vẽ `StateGraph` trước khi viết code.
2. Cần các agent tự tranh luận, tự chạy code, tự sửa → AutoGen, đặt `max_consecutive_auto_reply` và `max_round`.
3. Cần vai trò rõ ràng và thứ tự cố định → CrewAI với `Process.sequential`; cần quyết định động thì `Process.hierarchical`.
4. Dùng một cái thôi. Cả ba cùng chạy trong một dự án là ba nơi sửa lỗi cho cùng một việc.

**Kiểm tra**

Chạy cùng một task trên hai framework ứng viên, so số token, số lần phải sửa tay, và số dòng code để chạy được. Framework thắng là cái giúp bạn đổi ý nhanh nhất khi có lỗi — không phải cái viết code ngắn nhất.

---

## Q4. Có cái nào hay bị bỏ qua mà lại rất quan trọng không? [→ Nhóm 1, Tầng Security, Tầng Quality]

**Bạn sẽ thấy**

Bạn đã cài framework, đã có trí nhớ vector, đã nối MCP server, và hệ thống chạy. Bạn tưởng đã xong. Nhưng một lần agent chạy lệnh sai làm hỏng dữ liệu thật, và không có gì chặn; một lần bạn đổi prompt là chất lượng tụt mà không ai biết.

**Vì sao**

Vì framework, vector DB và MCP đều là **thứ làm việc**. Còn `guardrails`, `observability` và `evaluation` là thứ làm việc đó **đáng tin**: chặn tác dụng phụ trước khi nó xảy ra, và phát hiện hỏng trước khi người dùng thấy. `loop-cli` cũng hay bị quên, dù nó mới là chỗ bọc gate trong CI và cô lập bằng worktree. Bốn thư mục đó không thấy kết quả ngay nên không ai cài.

**Làm gì**

1. `guardrails` — kiểm tra mọi lượt gọi tool trước khi chạy: quyền, giới hạn tần suất, chặn nội dung.
2. `evaluation` — có bộ kiểm thử chạy trong CI để chặn hồi quy (khi chất lượng tụt sau một thay đổi).
3. `observability` — ghi lại chi phí và độ trễ từng lần gọi tool để có cái để so.
4. `loop-cli` — đặt gate trong CI và chạy loop trong worktree riêng.

**Kiểm tra**

Cố tình làm thay đổi làm kết quả tệ đi một chút: bộ `evaluation` phải đỏ và chặn được việc phát hành. Nếu không có gì đỏ, bạn đang chạy mà không có cảm biến.

---

## Q5. Vector DB khác MCP thế nào — hai cái có phải làm cùng một việc không? [→ Nhóm 3 — Vector DBs, Nhóm 4 — MCP Ecosystem]

**Bạn sẽ thấy**

Bạn thấy `vector-db/` và `mcp-ecosystem/` đều ghi tới `harness/06`, rồi tưởng chúng là hai lựa chọn cho cùng một thứ. Nhưng README lại nói vector DB cho harness 01, 02, 03 còn MCP cho harness 06.

**Vì sao**

Vì chúng ở hai đầu khác nhau của đường ống. Vector DB (Chroma, Pinecone, Qdrant, Weaviate) giữ **kiến thức đã học**: embedding, tìm kiếm theo nghĩa, và lớp trí nhớ ấm (Tier 2 Warm Memory) cho harness 01–03. MCP là **đường ống kết nối**: một chuẩn chung để lấy công cụ và dữ liệu từ bên ngoài vào, nơi harness 06 quyết định dùng gì rồi thực thi. Vector DB trả lời "cái gì liên quan tới câu hỏi này"; MCP trả lời "làm việc này bằng cách gọi cái gì".

**Làm gì**

1. Dùng vector DB khi cần agent nhớ và tra cứu kiến thức đã nạp vào.
2. Dùng MCP khi cần agent chạm vào hệ thống đang sống ngoài repo: GitHub, database, dịch vụ nội bộ.
3. Cả hai dùng chung được: một vector DB cũng có thể được phơi ra thành MCP server, và khi đó nó trở thành một nguồn tool trong danh mục.
4. Đừng dựng vector DB chỉ để "có sẵn cho tương lai" — nếu chưa có gì để tra thì nó chỉ tốn chi phí vận hành.

**Kiểm tra**

Viết hai câu hỏi thử: một câu hỏi có câu trả lời nằm trong tài liệu đã nạp (đường vector DB), một việc cần hành động lên hệ thống bên ngoài (đường MCP). Cả hai phải đi qua đúng đường của nó, không lẫn.

---

## Q6. RTK cắt được bao nhiêu token, có đáng cài không? [→ Case Studies 3 — Kết Quả Đo Lường RTK]

**Bạn sẽ thấy**

Mỗi lần agent chạy `ls`, `git push`, `cargo test` là vài trăm dòng text nằm trong context, phần lớn là tiếng ồn. Bạn muốn biết con số cụ thể trước khi quyết định cài, thay vì chỉ nghe "tiết kiệm token".

**Vì sao**

Vì ý tưởng của RTK rất đơn giản: nó đứng giữa, cắt và bóp méo output của lệnh dòng lệnh trước khi nó chạm vào mô hình. README liệt kê số liệu đo được cho từng lệnh, và đó là cơ sở để quyết định chứ không phải lời quảng cáo.

| Lệnh | Output thô | Qua RTK | Giảm |
|---|---|---|---|
| `ls -la` (45 dòng) | 45 dòng | 12 dòng (cây + số file) | ~73% |
| `git push` (15 dòng) | 15 dòng | `ok main` (1 dòng) | ~93% |
| `cargo test` (>200 dòng, fail) | >200 dòng | `FAILED: 2/15 tests` | ~90% |
| `ruff check` | nhiều dòng | gom theo luật / theo file | ~80% |

**Làm gì**

1. Chọn lệnh hay lặp lại nhất trong dự án của bạn — thường là `git status`, `git push`, kiểm tra lint, chạy test.
2. Cài RTK, tích hợp theo đúng AI tool bạn dùng. README nêu 16 công cụ được hỗ trợ, phần lớn qua cơ chế hook.
3. Đo trước và sau trên cùng task thật của bạn, đừng đo trên ví dụ.
4. Hãy nhớ điểm mấu chốt: cắt bớt phải **không giấu** việc mình đã cắt. Nếu còn 12.481 dòng nữa thì phải ghi ra, không cắt kiểu im lặng.

**Kiểm tra**

Chạy một task có nhiều lệnh lặp lại và so token trước/sau. Con số giảm nhưng kết quả cuối phù hợp ý bạn nghĩa là RTK đang cắt đúng chỗ. Nếu agent bỏ sót lỗi quan trọng, hãy xem lại chiến lược nén ở `rtk/01-concepts/`.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: README.md.*