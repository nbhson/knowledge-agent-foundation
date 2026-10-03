# ❓ FAQ — MCP Ecosystem (chuyện thật, dễ hiểu)

Nếu câu hỏi nào khó hiểu thì đọc `../README.md` phần trong ngoặc vuông.

---

## Q1. MCP là cái gì, khác gì với tự viết adapter cho từng tool? [→ Câu Chuyện Mở Đầu, MCP Là Gì?]

**Bạn sẽ thấy**

Bạn cần agent đọc GitHub, đọc database, đọc file. Bạn đang viết ba đoạn code riêng: một cho GitHub, một cho database, một cho file. Mỗi lần thêm tool mới lại viết tiếp một đoạn, mỗi đoạn một kiểu, không dùng lại được cho ứng dụng khác.

**Vì sao**

Cái bạn đang làm chính là vấn đề MCP sinh ra để giải quyết. Trước MCP, mỗi ứng dụng phải tự viết tích hợp riêng cho từng công cụ. MCP là một giao thức thống nhất (dùng JSON-RPC — một định dạng tin nhắn chuẩn), nên bạn viết **một** MCP server cho công cụ của mình, rồi mọi ứng dụng hỗ trợ MCP đều dùng được. README gọi nó là "USB-C của công cụ AI": một chuẩn, mọi thiết bị.

| Khái niệm | Vai trò |
|---|---|
| MCP Server | Chỗ cung cấp tool và dữ liệu |
| MCP Client | Ứng dụng AI tiêu thụ (Cline, Claude Desktop, VS Code) |
| Tools | Hành động server thực thi, agent gọi như hàm |
| Resources | Dữ liệu server phơi bày ra làm ngữ cảnh |

**Làm gì**

1. Trước khi viết adapter mới, hỏi đã có MCP server nào làm việc đó chưa — thường là đã có.
2. Nếu công cụ là của riêng bạn, viết một MCP server thay vì một adapter khóa chặt vào một ứng dụng.
3. Hiểu chỗ nào quyết định dùng tool: đó là `harness/06-decide-tools-mcp`. MCP chỉ là đường ống, không phải bộ não.

**Kiểm tra**

Thử bỏ adapter cũ, nối cùng công cụ đó qua MCP server vào một ứng dụng khác. Nếu chạy được thì bạn đã mua lại được tính dùng lại; nếu không, hãy xem chỗ nào bạn vẫn gắn cứng tên ứng dụng.

---

## Q2. Tool với Resource khác nhau thế nào, tôi nên đặt cái gì ở đâu? [→ MCP Là Gì?]

**Bạn sẽ thấy**

Bạn không biết nên đưa thứ gì vào đâu. Kết quả là bạn đưa hết dữ liệu vào tool, và mỗi lần agent cần một thông tin đơn giản thì phải "gọi" cái gì đó, mỗi lượt gọi đều tốn token và chờ đợi.

**Vì sao**

Tools là **hành động**: agent chủ động gọi, có thể thay đổi thế giới (ghi issue, tạo nhánh, chạy lệnh). Resources là **dữ liệu**: server phơi bày ra cho agent đọc lấy làm ngữ cảnh. Nếu bạn đóng gói một file cấu hình tĩnh thành tool, agent phải gọi mỗi lần chỉ để đọc — lãng phí và chậm.

**Làm gì**

1. Chỉ thành tool khi thao tác **ghi** hoặc **tốn thời gian thực sự**: tạo issue, gán nhãn, chạy truy vấn.
2. Đưa dữ liệu tĩnh vào resources: danh sách file, mô tả repo, tài liệu, lịch sử.
3. Đặt tên tool theo động từ hành động để agent không nhầm với dữ liệu.
4. Nhớ mỗi lượt gọi tool đều là một bước quyết định của agent — đừng biến việc đọc dữ liệu thành chuỗi lượt gọi.

**Kiểm tra**

Lấy một tác vụ chỉ cần đọc (ví dụ xem nội dung issue đang mở) và đếm số lượt gọi tool. Nếu phải gọi nhiều lượt chỉ để ghép dữ liệu, hãy xem lại xem phần nào nên là resources.

---

## Q3. Thêm MCP server mới vào dự án tôi thế nào, đụng tên tool thì sao? [→ Nhanh Chóng Thêm MCP Server Khác]

**Bạn sẽ thấy**

Bạn thêm hai server: một cái có sẵn từ trước, một cái do bạn tự cài. Sau đó agent báo lỗi kiểu tên tool trùng nhau, hoặc một server không chạy lên là toàn bộ danh sách tool biến mất.

**Vì sao**

Cấu hình nằm trong một khối duy nhất, mỗi server một mục có tên. Hai server đặt trùng tên sẽ đè lên nhau. Còn `npx` với cờ `-y` nghĩa là tự động tải và chạy package đó lúc khởi động — nếu server đó hỏng hoặc mất mạng, phần khởi động dừng lại và bạn mất luôn cả những server vốn đang chạy tốt.

**Làm gì**

1. Đặt tên khác nhau cho mỗi server, không đụng tên server có sẵn.
2. Đặt tên tool theo kèm nguồn để tránh trùng: ví dụ `github_search_code`, không phải `search`.
3. Thêm mỗi server kèm phần quyền riêng qua biến môi trường, không ghi khoá thẳng vào cấu hình.
4. Cân nhắc bỏ cờ `-y` ở máy chạy thật để phải duyệt trước khi tải code lạ.

```jsonc
{
  "mcpServers": {
    "github.com/github/github-mcp-server": { /* đã có */ },
    "my-custom-tool": {
      "command": "npx",
      "args": ["-y", "@my-org/my-mcp-server"],
      "env": { "API_KEY": "${API_KEY}" }
    } } }
```

5. Kiểm tra từng server một, không bật cả lô.

**Kiểm tra**

Bật lại từng server và đếm số tool xuất hiện sau mỗi lần. Nếu thêm server mới làm giảm số tool của server cũ, hãy kiểm tra trùng tên. Nếu một server hỏng làm mất hết tool, hãy bật `disabled` cho riêng server đó thay vì sửa cả cấu hình.

---

## Q4. Tool lấy từ MCP server thì có an toàn không, có cần lớp bảo vệ không? [→ Case Studies 2, Quan Hệ Với Harness]

**Bạn sẽ thấy**

Bạn đăng ký một tool từ MCP server vào danh mục tool của agent. Không lâu sau đó, agent gọi tool đó liên tục, mỗi phút hàng chục lượt, và có lượt ghi vào dữ liệu thật mà bạn không có ý định cho phép.

**Vì sao**

Vì thêm một tool vào danh mục không đồng nghĩa với việc cho phép dùng nó không. Trong cách đăng ký mẫu của README, mỗi tool mang theo chính sách riêng: mức quyền, số lượt gọi tối đa mỗi phút, và nguồn của nó là gì. Thiếu mấy trường đó, tool MCP nằm cùng hàng với công cụ nội bộ và không bị phân biệt. Mô tả trả về từ server cũng là dữ liệu, không phải chỉ dẫn — xem `../../harness/12-sandbox-execution/`.

**Làm gì**

1. Khi đăng ký tool từ MCP, điền đủ mức quyền và giới hạn tần suất.

```python
registry.register(ToolDefinition(
    name="github_search_code", source="mcp:github",
    description="Tìm code trong GitHub repos",
    parameters={"query": {"type": "string", "required": True}},
    requires_permission="standard", rate_limit_per_minute=30,
))
```

2. Giữ `autoApprove` trong cấu hình MCP ở dạng danh sách rỗng cho tới khi bạn thật sự duyệt tay từng loại thao tác.
3. Tool ghi dữ liệu thật thì tách quyền riêng, không dùng chung với tool chỉ đọc.
4. Với quyền ghi, đặt giới hạn tần suất thấp hơn và bắt buộc có bước duyệt.

**Kiểm tra**

Chạy một lượt gọi trần vượt quá giới hạn phải bị chặn và ghi vào nhật ký. Thử một thao tác ghi xem có bắt buộc duyệt không. Kiểm tra mọi thao tác ghi đều để lại dấu vết: ai gọi, lúc nào, ghi vào đâu.

---

## Q5. MCP server chết, treo hoặc báo lỗi xác thực — xử lý ở đâu? [→ 05-troubleshooting (TODO), Nhanh Chóng Thêm MCP Server Khác]

**Bạn sẽ thấy**

Hôm qua agent gọi tool từ GitHub chạy bình thường. Sáng nay không có tool nào hiện ra, và thông báo lỗi chung chung. Hoặc tệ hơn: tool xuất hiện nhưng mọi lượt gọi đều thất bại vì thiếu khoá.

**Vì sao**

Cấu hình MCP có ba nút điều khiển thường bị bỏ qua: `disabled` (tắt server), `autoApprove` (danh sách thao tác được duyệt tự động), và phần `env` nơi khoá được đọc từ biến môi trường. Nếu server bị tắt có chủ đích từ phiên trước, bạn sẽ không thấy bất kỳ tool nào. Nếu khoá không có trong môi trường, chuỗi `${API_KEY}` sẽ rỗng và lượt gọi thất bại ngay từ đầu. Đây là lý do thất bại nhiều hơn là lỗi protocol.

**Làm gì**

1. Kiểm tra `disabled` có đang là `true` không, trước khi nghĩ tới lỗi kỹ thuật.
2. Kiểm tra khoá có thật sự được nạp vào môi trường — mở shell của bạn và in tên biến (không in giá trị).
3. Cấp đúng phạm vi quyền: đọc repo không cần quyền ghi issue.
4. Với server chạy bằng `npx`, đặt thời gian chờ đủ dài vì lần đầu phải tải package.
5. Ghi lại lỗi của từng server riêng để biết chuyện gì hỏng, thay vì chỉ thấy "tool không hoạt động".

**Kiểm tra**

Bật tắt có chủ đích một server rồi khởi động lại: phải thấy đúng nhóm tool biến mất, không phải toàn bộ danh sách. Thử gọi một tool khi bỏ trống khoá: lỗi phải nói rõ là thiếu xác thực, không phải lỗi chung chung.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: README.md.*