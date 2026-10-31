# MCP bản 2026-07-28: bỏ kiểu "nhớ mặt khách", chuyển sang stateless

> Đây là phụ lục cho `README.md` §3 và §17.3.
> Spec mới nhất: `2026-07-28` (chốt ngày 28-07-2026). Hai bản cũ bạn có thể gặp là `2025-06-18` và `2025-11-25`.
> Link gốc: https://modelcontextprotocol.io/specification/latest

> **Từ khóa nhanh:** *MCP* = Model Context Protocol, ngôn ngữ chung để agent gọi công cụ ngoài (database, API...); *stateful* = server nhớ phiên của bạn giữa các lần gọi; *stateless* = server không nhớ gì, mỗi request tự đủ thông tin; *request* = một lần gửi yêu cầu tới server.

## Nói ngắn gọn là gì?

Phần này giải thích thay đổi lớn nhất của bản MCP mới: bỏ "nhớ phiên", chuyển sang mỗi request tự lo liệu.

Trước đây MCP làm việc kiểu "nhớ mặt khách quen": lần đầu client phải chào hỏi
(`initialize` — tin nhắn bắt tay đầu tiên), server mở một phiên (session) và nhớ bạn là ai qua header `Mcp-Session-Id`
(header = dòng thông tin kèm theo mỗi request). Mọi request sau đó đều dựa vào trí nhớ đó. Cách này khó scale (scale = phóng
to hệ thống phục vụ nhiều người hơn): request sau bắt buộc
phải về đúng server cũ (sticky — như gọi món xong phải đứng chờ đúng quầy cũ), server chết là mất trí nhớ.

Bản `2026-07-28` đổi sang kiểu "mỗi phiếu order đều đầy đủ thông tin":
mỗi request tự mang theo version + khả năng của client trong `_meta` (vùng dữ liệu tự mô tả đính kèm request).
Server nào nhận cũng xử lý được, khỏi cần nhớ gì trước đó. Nhờ vậy dễ scale ngang (thêm máy là thêm sức chứa),
dễ đặt sau load balancer (bộ chia đều request ra nhiều server), và model cũng suy luận mạch nhiều bước tốt hơn
vì state hiện rõ trong request chứ không giấu trong server.

> **Tóm gọn 1 câu:** MCP mới bỏ chế độ "server nhớ phiên" — mỗi request tự khai báo đầy đủ, nên thêm server thoải mái và không sợ mất trí nhớ khi server chết.

## Trước và sau, nhìn một bảng là hiểu

Phần này so sánh từng điểm giữa bản cũ và bản mới.

Cách đọc bảng này: cột **Trước đây** là cách MCP cũ (`2025-11-25` trở về trước) làm; cột **Bây giờ** là cách bản `2026-07-28` làm. Ví dụ, dòng đầu: bản cũ bắt buộc gửi tin "chào hỏi" trước, bản mới thì bỏ hẳn — gửi request là làm luôn.

| Trước đây (stateful, tới `2025-11-25`) | Bây giờ (`2026-07-28`, stateless) |
|---|---|
| Phải chào hỏi `initialize` trước khi làm gì | Bỏ hẳn. Mỗi request tự khai báo, làm luôn |
| Server nhớ bạn qua `Mcp-Session-Id`, phải sticky | Bỏ. Request nào cũng độc lập, server nào cũng được |
| `tools/list` khác nhau tùy connection | Response ghi rõ `ttlMs` (cache bao lâu) + `cacheScope` (share được không) — cứ thế mà cache |
| Không có header định tuyến | POST bắt buộc kèm `Mcp-Method` + `Mcp-Name`. Header lệch với body là bị từ chối — để gateway định tuyến mà không cần mở body |
| SSE còn resume bằng `Last-Event-ID` | Bỏ khỏi Streamable HTTP cho gọn |
| Tasks nằm trong core | Dời ra extension `io.modelcontextprotocol/tasks`, ai cần thì bật |
| `result` muốn trả sao cũng được | Phải ghi rõ `resultType: "complete"` (xong) hay `"input_required"` (cần hỏi thêm mới xong). Server cũ không có field này thì hiểu ngầm là `"complete"` |
| Lỗi "không thấy resource" là `-32002` | Đổi sang `-32602 (Invalid Params)` theo chuẩn JSON-RPC. Code cũ hardcode `-32002` sẽ miss |
| Không quy ước trace | Dùng chuẩn W3C trong `_meta`: `traceparent`, `tracestate`, `baggage` — cắm thẳng vào OpenTelemetry |
| Thương lượng version một lần lúc chào hỏi | Thương lượng từng request: gửi `_meta["io.modelcontextprotocol/protocolVersion"]` + header `MCP-Protocol-Version`. Sai version là nhận `UnsupportedProtocolVersionError` kèm danh sách version server hỗ trợ |

Giải nghĩa thêm vài dòng: `SSE` = Server-Sent Events, kênh đẩy dữ liệu liên tục từ server; `Last-Event-ID` = mốc để nhận tiếp dòng bị đứt; `Tasks` = tính năng chạy việc nền; `ttlMs` = số mili giây được phép cache (lưu tạm kết quả); `traceparent/tracestate/baggage` = các cặp mã theo chuẩn W3C để nối vết một request chạy qua nhiều hệ thống.

> **Tóm gọn 1 câu:** Bản mới bỏ chào hỏi, bỏ session-id, thêm header định tuyến, cache theo `ttlMs/cacheScope`, dời Tasks ra extension, đổi mã lỗi sang `-32602` và gắn trace chuẩn W3C.

## Giờ gọi server thế nào?

Cách nhanh nhất: hỏi trước `server/discover` — server nào chuẩn mới đều
BẮT BUỘC hỗ trợ lệnh này. Nó trả về một gói: tôi hỗ trợ version nào,
tôi có khả năng gì, tôi là ai. Biết rồi thì gọi cho chắc.

Lười thì khỏi hỏi trước cũng được: cứ gửi request luôn, nếu sai version
server sẽ báo `UnsupportedProtocolVersionError`, mình đọc danh sách rồi gửi lại.
Nhớ giữ đường lui cho server/client cũ kiểu handshake (`2025-11-25`),
và đừng hardcode `-32002` nữa (hardcode = "đóng đinh" con số vào code).

> **Tóm gọn 1 câu:** Gọi `server/discover` hỏi trước là chắc chắn nhất; lười thì gửi thẳng và xử lý lỗi sai version bằng cách đọc danh sách server trả về rồi gửi lại.

## Rules production viết lại cho dễ nhớ

Phần này gom 6 luật cần thiết khi chạy thật (production = hệ thống phục vụ người dùng thật).

1. **Version tính theo từng request, không theo connection.** Cache `tools/list`
   theo `ttlMs/cacheScope` server trả về (không có thì fallback 5–15 phút).
   Gặp `426`, tool lạ, hay lỗi version là xóa cache ngay.
2. **Headers luôn đủ 3 món:** `MCP-Protocol-Version`, `Mcp-Method`, `Mcp-Name`.
   Header tùy biến từ tool param thì đi theo tiền tố `x-mcp-header-*`.
3. **Cần nhớ gì qua nhiều bước thì cầm tay chỉ việc:** server tự đẻ một cái handle
   (mã phiếu) rồi bắt client gửi kèm như argument thường (SEP-2567 — số hiệu đề xuất
   trong đặc tả MCP).
   Tuyệt đối không trông chờ "server tự nhớ giùm".
4. **Auth làm cho đàng hoàng:** OAuth kiểu Resource Server + metadata (OAuth = chuẩn
   cấp quyền truy cập bằng token),
   Resource Indicators (RFC 8707 — chuẩn giới hạn token dùng cho đúng tài nguyên), kiểm tra `iss` (RFC 9207 — chuẩn xác nhận token do ai phát).
   Xoay key định kỳ, log thì che `Bearer` đi (Bearer = loại token xác thực, lộ là mất quyền).
5. **Trần cũ vẫn giữ:** `timeout 30s` (hết 30 giây là bỏ),
   `result ≤128KB`, `args ≤32KB`,
   validate args trước khi gửi (validate = kiểm tra dữ liệu hợp lệ). Streaming thì vừa nhận chunk (mảnh dữ liệu) vừa cộng dồn,
   quá trần hoặc idle 10s (im 10 giây) là cắt, client cancel là dừng.
6. **Trace xuyên suốt:** mang `traceparent/tracestate/baggage` trong `_meta`
   để gateway (cửa ngõ trung gian) và backend (hệ thống phía sau) nối trace OpenTelemetry (chuẩn theo dõi vết request) được với nhau.

> **Tóm gọn 1 câu:** Sáu luật: version theo từng request, đủ 3 headers, cần nhớ thì dùng handle, auth chuẩn OAuth, giữ trần timeout/kích thước cũ, và gắn mã trace xuyên suốt.

## Sửa code client thế nào? (patch cho §17.3)

Trước đây hay POST vào `${url}/tools/call` với `v = "2025-06-18"`.
Giờ POST thẳng vào endpoint MCP, mặc định `v = "2026-07-28"`,
kèm 3 headers mới + `_meta` trong body. Code đầy đủ nằm ở bản EN;
bên dưới là ý chính:

- Mặc định version mới, nhưng giữ một nhánh fallback `"2025-06-18"` cho server cũ.
- Gặp `426` nghĩa là lệch version: gọi `server/discover` rồi thử lại.
- Gặp `UnsupportedProtocolVersionError` thì đọc `supported` trong error rồi thử lại,
  đừng cố gửi tiếp.

> **Tóm gọn 1 câu:** Mặc định version `2026-07-28` kèm 3 headers mới và `_meta`, giữ nhánh fallback bản cũ, và gặp lỗi version thì đọc danh sách server trả về rồi gửi lại.

## Checklist trước khi bảo "xong"

Phần này là danh sách 5 việc phải hoàn thành trước khi đóng vụ migrate (chuyển sang bản mới).

- [ ] Đã thử `server/discover` hoặc đã xử lý retry khi sai version
- [ ] Không còn chỗ nào dựa vào `Mcp-Session-Id` hay `initialize`
- [ ] Chỗ bắt lỗi `-32002` đã chuyển sang `-32602`
- [ ] Tasks đã đưa sau cổng extension, không gọi như core nữa
- [ ] Trace `_meta` đã đi xuyên qua gateway

> **Tóm gọn 1 câu:** Xong migrate khi cả 5 ô trên đều tích được: có discover/retry, hết lệ thuộc session-id, đổi mã lỗi sang `-32602`, Tasks xuống extension, trace đi hết đường.

*(Ghi chú checklist: `Mcp-Session-Id`/`initialize` = cơ chế "nhớ phiên" bản cũ; `-32002` → `-32602` = đổi mã lỗi "không thấy resource" sang mã chuẩn JSON-RPC.)*
