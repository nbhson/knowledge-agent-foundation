# ❓ FAQ — Observability (chuyện thật, dễ hiểu)

Câu hỏi nào khó hiểu thì đọc `README.md` phần trong ngoặc vuông.

---

## Q1. LangSmith, Helicone, OpenLLMetry, W&B — chọn cái nào? [→ Tổng Quan Các Công Cụ]

**Bạn sẽ thấy**

Bốn công cụ, bốn kiểu can thiệp khác nhau — chọn sai thì phải sửa code hoặc không thấy được thứ bạn cần:

| Công cụ | Nhà phát hành | Cách gắn vào | Hợp nhất khi |
|---|---|---|---|
| Helicone | Helicone | đổi địa chỉ API | đa framework, cần số tiền ngay |
| LangSmith | LangChain | callback | đã dùng LangChain |
| OpenLLMetry | Traceloop | OpenTelemetry | nhiều nhà cung cấp, đã có hệ giám sát |
| W&B | W&B | theo dõi thí nghiệm | nghiên cứu ML, so sány nhiều lần chạy |

**Vì sao**

Vì khác biệt nằm ở chỗ **bạn phải sửa gì**. Helicone là một proxy: đổi `OPENAI_API_BASE` sang `https://oai.helicone.ai/v1` là xong, không đụng dòng code nào — nhưng nó chỉ thấy lời gọi mô hình, không thấy từng bước trong chuỗi xử lý. LangSmith thấy được cả chuỗi bước `retrieve → build → agent → tools`, nhưng đòi bạn truyền callback vào mô hình.

OpenLLMetry nằm giữa: dùng chuẩn OpenTelemetry nên đẩy dữ liệu sang Jaeger, Grafana, Datadog đều được. W&B mạnh về so sánh kết quả giữa nhiều lần thử.

**Làm gì**

1. Bắt đầu bằng Helicone — nhanh nhất, đổi hai biến môi trường là có số liệu chi phí ngay.
2. Dùng LangChain thì chuyển sang LangSmith để xem được từng bước trong chuỗi.
3. Đã có hệ giám sát sẵn (Grafana, Datadog) thì dùng OpenLLMetry để không phải dựng thêm dashboard riêng.
4. Đang làm nghiên cứu, so sánh nhiều biến thể thì dùng W&B.
5. Chỉ ghi lại những trường bạn thật sự dùng để quyết định, ví dụ `session_id`, `user_id`, `tool_name`.

```bash
export OPENAI_API_BASE="https://oai.helicone.ai/v1"
export HELICONE_API_KEY="sk-helicone-..."
```

**Kiểm tra**

Gọi một lượt thật, mở bảng điều khiển và xác nhận thấy đúng số token đã dùng. Không thấy dữ liệu thì kiểm tra địa chỉ API có thực sự trỏ qua proxy không.

---

## Q2. Loop đang ăn 50.000 token mỗi lượt thay vì 10.000 — biết chỗ nào phình không? [→ Case Studies Thực Tế — Phát Hiện Token Leak]

**Bạn sẽ thấy**

Một vòng lặp tên `ci-sweeper`, chạy 5 lần mỗi ngày. Bình thường mỗi lượt hết khoảng 10.000 token, nhưng có lúc lên 50.000. Không rõ nguyên nhân.

Biểu đồ token theo lần gọi cho thấy: lượt thứ 3 luôn gọi `read_file` **15 lần với cùng một file**.

**Vì sao**

Vì không có ghi nhận thì bạn đang đoán mò. Nguyên nhân thường gặp nhất là thiếu chỉ dẫn về việc tái dùng kết quả: mỗi lần gặp lại file đó, agent lại đọc từ đầu vì không biết nội dung đã nằm trong ngữ cảnh.

**Làm gì**

1. Bật theo dõi từng lần gọi công cụ, ghi cả ba trường: tên công cụ, số token đầu vào, tổng token phiên.
2. Tìm các lần gọi lặp lại cùng một tham số trong một phiên — đây là dấu hiệu rò token (token leak).
3. Thêm chỉ dẫn tái dùng vào prompt: nội dung file đã nằm trong ngữ cảnh thì không đọc lại.
4. Đo lại sau khi sửa prompt.
5. Nếu vẫn còn, kiểm tra đầu ra của công cụ có bị cắt bớt im lặng không — một tệp 2MB bị cắt còn vài dòng mà không báo, agent sẽ tưởng đã đọc hết và đọc lại.

```text
Trước: lượt #3 → read_file × 15 cùng 1 file
Sau : thêm "reuse file contents if already in context"
Kết quả: giảm 40% token
```

**Kiểm tra**

Chạy lại cùng kịch bản 10 lượt. Token trung bình phải giảm về gần mức cũ, và số lần gọi `read_file` lặp trong một phiên phải về 0.

---

## Q3. Làm sao biết công cụ nào chậm, chỗ nào hỏng? [→ Case Studies Thực Tế — Tool Latency SLO]

**Bạn sẽ thấy**

Danh bạ công cụ đã có sẵn ba số đo theo `harness/06`: `avg_latency_ms`, `success_rate`, `total_calls`. Nhưng bạn đang nhìn chúng rời rạc, không ai cảnh báo khi chỉ số xấu đi.

**Vì sao**

Vì ba chỉ số này chỉ có giá trị khi có ngưỡng (SLO — mức cam kết dịch vụ) đi kèm. Biết `vector_search` mất 1.200 mili giây chưa nói lên điều gì; biết rằng vượt 2.000 mili giây thì bật cảnh báo thì mới hành động được.

Số liệu thật để bắt đầu: cảnh báo khi truy vấn vector vượt 2.000 mili giây; cảnh báo khi `execute_python` có tỉ lệ thành công dưới 0,95.

**Làm gì**

1. Ghi số đo sau **mỗi** lần gọi, không chỉ gom theo phiên — nếu chỉ gom cuối phiên thì bạn không biết lỗi xảy ra ở bước nào.
2. Đặt hai ngưỡng cảnh báo: độ trễ trung bình theo từng công cụ, và tỉ lệ thành công theo từng công cụ.
3. Nối cảnh báo vào kênh bạn thật sự nhìn, không phải một bảng điều khiển ai cũng quên.
4. Khi có cảnh báo, mở trace của phiên đó để xem chuỗi bước — công cụ chậm thường do đầu vào quá lớn, không phải do nó bị lỗi.
5. Đo cả số lần gọi: `total_calls` tăng bất thường là dấu hiệu agent đang lặp vô ích.

```python
tool.update_metrics(latency_ms=1200, success=True)
# Cảnh báo: vector_search.avg_latency_ms > 2000
# Cảnh báo: execute_python.success_rate < 0.95
```

**Kiểm tra**

Cố tình làm một công cụ chậm lên vài giây, xem cảnh báo có bắn. Tắt công cụ đó đi và xem tỉ lệ thành công có rơi xuống dưới ngưỡng không.

---

## Q4. Không muốn sửa một dòng code nào thì chọn cách nào? [→ Helicone — Proxy Không Cần Sửa Code]

**Bạn sẽ thấy**

Một codebase dài, đụng vào chỗ gọi mô hình là phải đợi duyệt kéo dài tuần. Bạn vẫn muốn biết tuần này hết bao nhiêu tiền và request nào chậm.

**Vì sao**

Vì Helicone đứng giữa, không cần bạn can thiệp. Toàn bộ lời gọi mô hình đi qua địa chỉ của nó nên nó nhìn thấy tất cả: số tiền, độ trễ, số request, tỉ lệ lỗi — mà không đụng dòng code nào trong dự án.

Đổi lại, nó **chỉ thấy lời gọi mô hình**. Nó không biết bên trong chuỗi xử lý đã gọi công cụ nào, công cụ nào trả về rỗng. Đó là ranh giới của cách làm này.

**Làm gì**

1. Đặt địa chỉ cơ sở API sang proxy và khoá nhận diện bằng biến môi trường, đặt ở nơi chỉ môi trường chạy được đọc.
2. Dùng nó để trả lời ba câu hỏi trước khi đầu tư thêm: tiền tăng ở đâu, request nào chậm bất thường, tỉ lệ lỗi là bao nhiêu.
3. Nếu cần xem sâu từng bước trong chuỗi, bổ sung callback theo dõi ở tầng trên — proxy không làm được việc đó.
4. Đừng đưa khoá API vào mã nguồn; biến môi trường phải nằm ở file bị bỏ qua khi commit.
5. Kiểm tra phần đạt dữ liệu: nội dung request của bạn có chứa dữ liệu nhạy cảm cần lọc không.

**Kiểm tra**

Gọi mô hình một lần và xem trong bảng điều khiển có đúng một lượt với đúng số token. Sau đó tắt biến môi trường, gọi lại — lượt đó phải không xuất hiện, chứng tỏ đường đi đã đúng qua proxy.

---

## Q5. Đặt luật lưu log ở đây được không? [→ Quan Hệ Với Harness]

**Bạn sẽ thấy**

Bạn muốn quy định: mỗi phiên phải lưu 30 ngày, mỗi trường phải có `session_id`, và không được ghi khoá bí mật. Chữ này xuất hiện trong README của công cụ bạn đang cân nhắc.

**Vì sao**

Vì thư mục này là **danh mục công cụ**, không phải hợp đồng của hệ thống. Hợp đồng chuẩn về sự kiện — hệ phát ra điều gì, cấu trúc `TrajectoryEvent` dạng nào, khoá nối bản ghi, thời gian lưu, cách lọc dữ liệu nhạy cảm — thuộc về `harness/13-trajectory-observability`.

Một thư viện ghi log có thể tuân thủ chuẩn đó, nhưng chuẩn không nằm ở thư viện.

**Làm gì**

1. Chốt hợp đồng sự kiện ở `harness/13-trajectory-observability` trước, rồi mới chọn công cụ.
2. Chọn công cụ ở đây theo tiêu chí: có xuất được theo chuẩn OpenTelemetry không, có hỗ trợ lọc dữ liệu nhạy cảm không, có giới hạn thời gian lưu theo yêu cầu không.
3. Nếu bạn đang định nghĩa cấu trúc trường dữ liệu của sự kiện trong cấu hình công cụ, đó là dấu hiệu đang đặt nhầm chỗ.
4. Gắn khoá nối bản ghi (`session_id`) xuyên suốt từ đầu phiên tới từng lần gọi, nếu không các bản ghi sẽ không nối được với nhau.
5. Kiểm tra xem công cụ có lưu nội dung request không — nếu có, đó là dữ liệu nhạy cảm đang nằm ngoài hệ thống của bạn.

**Kiểm tra**

Đổi công cụ từ A sang B. Nếu hợp đồng sự kiện nằm ở đúng chỗ, chỉ cần sửa cấu hình kết nối. Nếu phải sửa lại code phát sự kiện, thì bạn đang đặt hợp đồng nhầm chỗ.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: README.md.*