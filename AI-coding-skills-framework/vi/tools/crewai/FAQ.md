# ❓ FAQ — CrewAI (chuyện thật, dễ hiểu)

Nếu câu hỏi nào khó hiểu thì đọc `../README.md` phần trong ngoặc vuông.

---

## Q1. AutoGen với CrewAI — tôi nên chọn cái nào? [→ Câu Chuyện Mở Đầu]

**Bạn sẽ thấy**

Bạn cần một agent duy nhất lo việc nhỏ lặp đi lặp lại, hoặc một nhóm agent phải chia việc. Cả hai framework đều giải quyết chuyện "nhiều agent cùng làm một việc", nên nhìn vào tài liệu thì thấy giống nhau và không biết chọn cái nào.

**Vì sao**

Khác biệt nằm ở cách chúng nghĩ về một agent đơn vị. AutoGen lấy **cuộc trò chuyện** làm đơn vị: các agent gửi message cho nhau và kết quả là những gì chúng nghe được. CrewAI lấy **vai trò** làm đơn vị: mỗi `Agent` có role, goal, backstory; mỗi `Task` có mô tả và đầu ra mong đợi; các agent nằm chung trong một `Crew` có `process` quyết định thứ tự. Nếu việc của bạn có sẵn danh sách việc cần làm thì CrewAI viết ra giống bảng công việc. Nếu bạn lại muốn các agent thảo luận tự do thì AutoGen hợp hơn.

| Bạn đang cần | Chọn |
|---|---|
| Tranh luận tự do giữa các agent, agent tự sửa code | AutoGen |
| Danh sách vai trò + nhiệm vụ rõ ràng, chạy theo pipeline | CrewAI |
| Một agent duy nhất, không cần khung nào | Không cần framework nào |

**Làm gì**

1. Trả lời: "tôi có sẵn danh sách vai trò và nhiệm vụ không?" Có → CrewAI. Không → AutoGen.
2. Nhớ cả hai framework đều cho sẵn một mảnh code mẫu trong `HARNESS_ENGINEERING.md` mục 9.1 — đọc đoạn đó trước khi cài gì cả.
3. Đừng học cả hai lúc một. Chọn một, chạy được case thật, rồi mới đổi.
4. Cả hai đều cần phần đo token và phần đánh giá kết quả — xem `tools/observability/` và `tools/evaluation/`.

**Kiểm tra**

Chạy cùng một task nhỏ (ví dụ "viết và review một hàm") trên cả hai. So số token dùng, số lần phải sửa tay, và độ dài code cấu hình để chạy được. Framework nào ít code hơn mà vẫn ra kết quả tốt hơn thì giữ lại, không cần lý thuyết.

---

## Q2. `Process.sequential` với `Process.hierarchical` — khác nhau thế nào, dùng cái nào? [→ Process: Sequential vs Hierarchical]

**Bạn sẽ thấy**

Bạn có ba agent và ba nhiệm vụ. Chạy `sequential` thì thứ tự cố định plan → code → review, ai cũng nói đúng một lượt. Nhưng khi reviewer báo lỗi, không ai quay lại coder — luồng vẫn đi tiếp. Muốn sửa thì phải tự viết lại logic vòng lặp.

**Vì sao**

`sequential` là đường ống một chiều: nó map với harness/07 workflow, và thứ tự là thứ bạn khai báo lúc định nghĩa, không ai thay đổi được giữa chừng. `hierarchical` bổ sung một agent quản lý, agent này tự giao nhiệm vụ cho agent khác — đó là harness/09 multi-agent. Nếu bài toán của bạn có nhánh quyết định thì phải dùng bản hierarchical, vì sequential không có chỗ để quyết định.

**Làm gì**

1. Bắt đầu bằng `sequential`: nhanh nhất để thấy khung chạy đúng không.
2. Cần quay lại sửa thì chuyển `hierarchical`, khai báo thêm manager.

```python
harness = Crew(
    agents=[executor, reviewer],
    tasks=[execute_task, review_task],
    process=Process.hierarchical,
    manager_agent=manager,   # đóng vai harness orchestrator
    manager_llm=llm,
)
```

3. Nhớ đời thường: manager cũng tốn token và cũng có thể giao sai. Chỉ thêm manager khi bạn thật sự cần quyết định động, không phải vì nghe hay.
4. Ghi lại thứ tự thực thi mỗi lần chạy để thấy luồng có đúng không.

**Kiểm tra**

Chạy một task có lỗi thật (reviewer chắc chắn phải báo lỗi). Với `sequential`, hãy xác nhận kết quả vẫn là sản phẩm chưa sửa — đó là giới hạn của đường ống, không phải bug. Chuyển sang `hierarchical` và xác nhận luồng có quay lại coder.

---

## Q3. Viết `expected_output` như nào để agent không ra kết quả rác? [→ Tổng Quan, Case Studies 1]

**Bạn sẽ thấy**

Agent làm xong việc nhưng trả về một đoạn văn dài, đúng nhưng không theo hình dạng bạn cần. Task tiếp theo là task sau vẫn phải cắt chuỗi mới dùng được, và mỗi lần làm khác nhau một chút.

**Vì sao**

`Task` có đúng ba trường quan trọng: `description` (việc cần làm), `expected_output` (kết quả mong đợi), và `agent` (giao cho ai). `expected_output` không phải ghi chú cho bạn — đó là hợp đồng mà agent căn cứ để tự biết mình đã đủ hay chưa. Viết chung chung kiểu "một danh sách" thì agent tự hiểu theo cách riêng của nó, và bạn không có gì để kiểm tra.

**Làm gì**

1. Viết `expected_output` là một mẫu cụ thể có thể kiểm tra bằng máy, không phải một cảm xúc. Ví dụ "danh sách task dạng `- [ ] mô tả`", không phải "kế hoạch chi tiết".
2. Nêu rõ định dạng và ranh giới: có bao nhiêu mục, mỗi mục một dòng, không kèm giải thích.
3. Mỗi nhiệm vụ chỉ nhận **một** agent. Muốn kết quả tốt hơn thì tách thành nhiệm vụ khác, không nhồi nhiều kỳ vọng vào một.
4. Agent cuối cùng trong chuỗi nên có nhiệm vụ chỉ ra vấn đề còn lại, để luồng có điểm dừng rõ ràng.

**Kiểm tra**

Đưa ba bản trả về từ ba lần chạy cùng một task. Nếu cả ba đều khớp mẫu `expected_output` mà không cần bạn sửa tay, thì mô tả đã đủ cụ thể. Còn nếu phải tay chỉnh, sửa `expected_output` chứ đừng sửa lời nhắc đi sửa output.

---

## Q4. Cho tôi duyệt ở đúng chỗ nhạy cảm trong chuỗi — làm sao? [→ Human-in-the-Loop]

**Bạn sẽ thấy**

Bạn không muốn ngồi xem cả tá nhiệm vụ, chỉ muốn có tiếng nói ở bước deploy hoặc bước ghi vào dữ liệu thật. Nhưng mỗi lần agent dừng hỏi cũng mất thời gian, và có lần nó hỏi cả ở những việc vô nghĩa.

**Vì sao**

CrewAI đặt cờ `human_input` trên từng `Task`, nên quyền hỏi gắn thẳng vào một nhiệm vụ chứ không phải cả crew. Đây là điểm khác biệt thực dụng so với việc bật tắt ở cấp agent: chỉ một bước dừng, phần còn lại chạy tự do.

**Làm gì**

1. Chỉ gắn `human_input=True` cho nhiệm vụ có tác dụng thật ra ngoài: phát hành, ghi vào production, gửi thông báo cho khách.
2. Các nhiệm vụ còn lại để mặc định, đừng gắn — mỗi lần dừng là một vòng đợi.

```python
task = Task(
    description="Deploy to production",
    expected_output="Deployment confirmation",
    human_input=True,  # dừng lại chờ xác nhận
)
```

3. Viết `expected_output` cho nhiệm vụ này là bằng chứng (mã phiên bản, thời điểm), để sau khi duyệt bạn có thứ để tra lại.
4. Cấu hình danh sách thao tác tự động duyệt (`autoApprove`) ở lớp MCP phải để rỗng cho tới khi bạn đã thấy đúng những gì mình định cho phép.
5. Ghi lại ai duyệt và duyệt cái gì, kèm thời điểm. Bản ghi này là thứ duy nhất phân biệt được "tôi cho phép" với "tôi quên chặt".

**Kiểm tra**

Chạy một crew có cả nhiệm vụ nhạy cảm lẫn nhiệm vụ thường. Xác nhận crew chỉ dừng đúng một lần, đúng nhiệm vụ nhạy cảm, và bằng chứng sau khi chạy khớp với những gì bạn vừa duyệt.

---

## Q5. Crew chạy xong nhưng kết quả không như ý — lỗi ở vai hay ở nhiệm vụ? [→ Quan Hệ Với Harness]

**Bạn sẽ thấy**

Crew chạy không lỗi, không treo, nhưng kết quả lệch. Agent làm đúng việc được giao nhưng việc đó không giúp ích cho bạn — chẳng hạn reviewer "duyệt" xong vẫn có lỗi logic, hoặc coder viết ra thứ chạy được nhưng không đúng ý người dùng.

**Vì sao**

Vì trong CrewAI có ba tầng độc lập nhau và mỗi tầm hỏng theo cách khác. `Agent` có role, goal, backstory — định nghĩa **agent là ai**, quyết định nó suy nghĩ thế nào. `Task` có description, expected_output — định nghĩa **việc và hình dạng kết quả**. `Crew` có process — định nghĩa **thứ tự**. Sửa nhầm tầng là cách mất thời gian phổ biến nhất: đổi `process` không bao giờ sửa được một `goal` viết mơ hồ.

| Bạn muốn agent nghĩ khác | Sửa ở đâu |
|---|---|
| Nó không quan tâm đúng việc | `goal` + `backstory` |
| Nó làm sai hình dạng kết quả | `expected_output` |
| Nó không làm đúng thứ tự | `process` của `Crew` |
| Nó thiếu khả năng hành động | danh sách tools của Agent |

**Làm gì**

1. Đọc lại `goal` của từng agent. Nếu hai agent có `goal` gần như giống nhau, hội thoại sẽ thành nói cho vui và không ai dẫn đầu.
2. Viết lại `expected_output` của nhiệm vụ đích thành mẫu kiểm được.
3. Đừng sửa `process` khi nghi vấn nằm ở cách nghĩ của agent.
4. Thêm `tools` cho agent cần hành động — README đặt `tools=[code_editor]` đúng cho vai Coder, vì vai đó nhiều lẽ phải sửa code.

**Kiểm tra**

Chạy lại từng nhiệm vụ **một mình**, không cả crew, và so kết quả với bản chạy đầy đủ. Nếu chạy đơn vẫn sai thì lỗi nằm ở role hoặc expected_output. Nếu chạy đơn đúng mà chạy cả crew sai thì lỗi nằm ở `process` hoặc ở output được truyền sang nhiệm vụ sau.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: README.md.*