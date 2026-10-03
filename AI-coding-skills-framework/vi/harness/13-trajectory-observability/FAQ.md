# ❓ FAQ — Trajectory & Observability (Câu hỏi thật, dễ hiểu)

Nếu câu hỏi chưa rõ, đọc `README.md` phần được nêu trong ngoặc vuông.

---

## Q1. Agent xoá file của tôi, 40 phút sau mới biết — giờ làm sao biết nó xoá lúc nào? [→ §1 Contract · §2.1 Hình Dạng Một Run · §4.2 Năm Câu Hỏi]

**Bạn sẽ thấy**

Ticket của khách: *"Agent xoá `src/auth/middleware.ts`, tôi báo lại sau 40 phút. Tại sao?"* Bạn có lời model nói (chat log), một đoạn log CI, và cảm giác chung "nó đang dọn code auth". Bạn không nói được lệnh xoá nằm ở lượt nào.

**Vì sao**

Chat log ghi lại điều mô hình **nói**, không phải điều nó **làm**. Không có nhật ký hành động thì bất kỳ bài post-mortem nào cũng chỉ là phỏng đoán.

**Làm gì**

1. Mọi module trong hệ thống đều ghi vào **một** nơi: một sự kiện (event) chỉ-append, mỗi sự kiện có số thứ tự `seq` liền mạch, có `sessionId`, `parentTaskId`, `actor` (ai làm: model hay người), thời điểm, và nội dung đã che khoá.
2. Cặp `tool_call` với `tool_result` luôn đi kèm. Một `tool_call` không có `tool_result` là một bước đã bị treo.
3. Truy vấn lại phiên đó bằng một câu lệnh, không cần đoán:

```sql
SELECT seq, kind, payload->>'tool' AS tool, payload->>'path' AS path
FROM trajectory
WHERE session_id = 'ses_44a' AND payload->>'path' LIKE '%middleware%'
ORDER BY seq;
-- seq 31: read_file  src/auth/middleware.ts  → 4.1KB
-- seq 32: edit_file  (patch applied)
-- seq 33: write_file  ← lệnh xoá
-- seq 34: eval        "tests pass" (thật — không còn gì import nó)
```

4. Các câu hỏi tiếp theo tự trả lời lấy nhau: nó xoá vì `seq 29` ghi "các export không ai dùng"; hoàn tác được không vì `seq 33` có ghi `git worktree`.

**Kiểm tra**

Lấy một phiên đã chạy và trả lời năm câu hỏi: nó **làm** gì, nó **thấy** gì, nó **tin** gì, nó **hỏng** ở đâu, **giám khảo** nói gì. Nếu cả năm đều có câu trả lời từ dữ liệu thì hệ thống đã dùng được.

---

## Q2. Tôi đã có chat log với lời model rồi — có cần thêm trajectory nữa không? [→ §13.2 KHÔNG NÊN · §14 Anti-Patterns · §6.1 Catalog Query]

**Bạn sẽ thấy**

Bảng dashboard hiển thị correctness 82%, quality 75%, composite score 81/100. Nhưng số token tiêu thụ và số bước thì không ai giải thích được, và câu hỏi "vì sao tháng trước hóa đơn tăng gấp ba" thì không query nào trả lời được.

**Vì sao**

Vì bạn đang lưu **lời nói** chứ không lưu **dấu vết hành động**. Thiếu `seq` thì không biết mất một lần ghi hay chỉ mất một suy nghĩ; thiếu `parentTaskId` thì mọi sự kiện đều mồ côi, nối vào nhau không được. Thiếu `model` và `tokens` ở từng bước thì không có cách nào quy chi phí.

**Làm gì**

1. Bổ sung những trường mà mọi truy vấn sau này đều cần: `id` theo kiểu sắp xếp được (ULID), `seq`, `sessionId`, `parentTaskId`, `actor`, `tokens`, `latencyMs`, `model`, `costUsd`, và `fingerprint` (dấu vân tay của prompt).
2. Chỉ-append: **không** sửa event cũ. Cách đính chính là thêm một sự kiện mới (`plan_revision`), không phải ghi đè.
3. Với sự kiện nhạy cảm, dùng giá trị trung thực chỉ-append. Không có giá trị trung thực thì mọi kết luận rút ra — kể cả kết luận về chi phí — đều đáng ngờ.
4. Chỉ `fsync` (ghi cưỡng bức xuống đĩa) cho phần quyết định: phê duyệt, ghi nhớ, kết quả đánh giá, và hai đầu phiên. Phần còn lại đẩy ra sau, tối đa 100 mili giây.
5. Sau khi đủ dữ liệu, phần lớn chỉ số chỉ cần một câu SQL: hiệu quả bước, độ chính xác công cụ, tỉ lệ tự phục hồi, hay phát hiện lặp (cùng một mã lệnh lặp từ 3 lần trong một phiên).

**Kiểm tra**

Chạy truy vấn "tìm bước đắt nhất" và "tìm `tool_call` không có `tool_result`". Nếu cả hai đều trả về kết quả có nghĩa, bạn đã có nền để debug và tính tiền.

---

## Q3. Log lớn quá, lưu toàn bộ thì tốn tiền — giữ lại bao nhiêu, bỏ gì? [→ §5.1 Các Tầng Hot/Warm/Cold · §7.3 Chiến Lược Sampling]

**Bạn sẽ thấy**

Một phiên bình thường có khoảng vài chục sự kiện; `prompt` và `context_assembly` chiếm phần lớn dung lượng, còn `tool_call` và `tool_result` là phần bạn thực sự cần để debug.

**Vì sao**

Ghi đủ chi tiết cho mọi thứ ở mọi nơi là vừa đắt vừa ít giá trị nhất sáu tuần sau. Kết quả của công cụ dài là thứ nặng nhất mà ít ai đọc lại.

**Làm gì**

1. Chia bốn tầng theo tuổi: **nóng** 0–7 ngày giữ nguyên tất cả; **ấm** 7–90 ngày thay mọi nội dung vượt 4KB bằng một con trỏ, phần còn lại để nguyên; **lạnh** 90 ngày–1 năm chỉ giữ số tổng hợp (số bước, token, chi phí, độ trễ, kết quả chấm); **xoá** theo thời hạn của khách.
2. Với tầng ấm, giữ kèm một dấu vân tay của kết quả (stdoutHash) để vẫn kiểm chứng được mà không tốn dung lượng.
3. Chọn mức lấy mẫu (sampling) theo lớp tín hiệu: lỗi, phê duyệt, thao tác trên production — **100%**; điểm đánh giá dưới 0,6 — 100%; ghi thành công — 20%; lệnh đọc thành công — 5%; câu hệ thống ở bình thường — 1%.
4. **Luôn giữ bộ đếm ở 100%** kể cả khi bỏ nội dung. Log đã lấy mẫu mà vẫn có số tổng hợp thì trả lời được câu hỏi mục tiêu dịch vụ; lấy mẫu mà không có số tổng hợp thì không trả lời được gì.

**Kiểm tra**

Mô phỏng 10.000 phiên: so dung lượng và số tiền trước/sau khi áp tầng + lấy mẫu. Sau đó hỏi lại ba câu: bao nhiêu bước trung bình mỗi phiên, tỉ lệ tự phục hồi, tổng chi phí theo model. Cả ba phải vẫn trả lời được.

---

## Q4. Tôi sợ log của agent lộ khoá hay dữ liệu khách hàng — làm gì? [→ §5.2 Redaction Lúc Emit · §5.3 Cô Lập Tenant & GDPR]

**Bạn sẽ thấy**

Một sự kiện có nội dung chứa khoá dạng `sk-…`, token GitHub, khóa riêng tư, email khách, số thẻ. Nếu log này đọc lại được thì bất kỳ ai có quyền đọc log đều có khoá.

**Vì sao**

Nếu che khoá (redaction) lúc **đọc** thì đã thua: bảng gốc vẫn chứa dữ liệu thật, và bảng gốc luôn bị đọc bởi các câu lệnh tra cứu tạm. Che khi **ghi** là biến đổi vĩnh viễn trước khi nó chạm đĩa.

**Làm gì**

1. Che ngay lúc ghi, theo các mẫu hình dạng: khoá API `sk-`, token GitHub, mã truy cập AWS `AKIA`, khối khóa riêng tư, email, số thẻ.
2. Ghi lại **số lần đã che** vào chính sự kiện. Con số bất thường tăng vọt ở một khách hàng là dấu hiệu có việc.
3. Đặt `tenantId` trên mọi sự kiện và **từ chối ghi** nếu thiếu — không phải cảnh báo rồi vẫn ghi. Bật bảo mật theo hàng (row-level security) hoặc tách kho riêng cho từng khách; tra cứu chéo khách phải trả về rỗng.
4. Đường xoá theo quy định bảo vệ dữ liệu phải gỡ cả bốn nơi: sự kiện nhật ký, số tổng hợp lạnh, báo cáo dẫn xuất, và mọi bản ghi cache đã tính toán. Sau đó phát một **biên nhận xoá** lưu bất biến, ghi rõ số phiên và số sự kiện đã gỡ.
5. Giới hạn kích thước: một nội dung sự kiện tối đa 64KB, vượt ngưỡng thì chỉ lưu một con trỏ.

**Kiểm tra**

Chạy câu lệnh kiểm tra hằng quý trên kho tầng ấm, đếm số chuỗi khớp mẫu khoá. Phải bằng 0. Khác 0 là sự cố dữ liệu, cần xử lý ngay chứ không phải việc dọn dẹp cuối tuần.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: `README.md`.*