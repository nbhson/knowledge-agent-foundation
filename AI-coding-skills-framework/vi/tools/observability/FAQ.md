# ❓ FAQ — Observability (chuyện thật, dễ hiểu)

Observability = khả năng nhìn thấy bên trong hệ thống đang chạy: nó tốn bao nhiêu token, bước nào chậm, bước nào hỏng. FAQ này trả lời bằng tình huống thật.

Câu hỏi nào khó hiểu thì đọc `README.md` phần trong ngoặc vuông.

---

## Q1. LangSmith, Langfuse, Helicone, OpenLLMetry, W&B — chọn cái nào? [→ Tổng Quan Các Công Cụ]

**Bạn sẽ thấy**

Năm công cụ, năm kiểu can thiệp khác nhau — chọn sai thì phải sửa code hoặc không thấy được thứ bạn cần:

Cách đọc bảng này: cột "Công cụ" là tên sản phẩm; cột "Cách gắn vào" là việc bạn phải làm để nối nó vào dự án (ví dụ "đổi địa chỉ API" = sửa một biến cấu hình, không đụng code); cột "Hợp nhất khi" là tình huống nên chọn nó.

| Công cụ | Nhà phát hành | Cách gắn vào | Hợp nhất khi |
|---|---|---|---|
| Helicone | Helicone | đổi địa chỉ API | đa framework, cần số tiền ngay |
| Langfuse | Langfuse | SDK / OTel export | self-host, privacy-sensitive, muốn chuẩn gen-ai |
| LangSmith | LangChain | callback | đã dùng LangChain |
| OpenLLMetry | Traceloop | OpenTelemetry | nhiều nhà cung cấp, đã có hệ giám sát |
| W&B | W&B | theo dõi thí nghiệm | nghiên cứu ML, so sánh nhiều lần chạy |

Giải nghĩa thuật ngữ trong bảng: SDK = bộ thư viện cài vào code; OTel export = đẩy dữ liệu theo chuẩn OpenTelemetry (chuẩn ghi vết mở, dùng chung được nhiều công cụ); self-host = tự chạy server trên máy mình, dữ liệu không gửi ra ngoài; callback = hàm bạn truyền vào để nó được gọi khi có sự kiện; proxy = server đứng giữa bạn và API.

**Vì sao**

Vì khác biệt nằm ở chỗ **bạn phải sửa gì**. Helicone là một proxy: đổi `OPENAI_API_BASE` sang `https://oai.helicone.ai/v1` là xong, không đụng dòng code nào — nhưng nó chỉ thấy lời gọi mô hình, không thấy từng bước trong chuỗi xử lý. Langfuse là open source, chạy self-hosted được nên phù hợp khi dữ liệu không được gửi ra ngoài, đồng thời hỗ trợ OTel GenAI semantic conventions — trace theo chuẩn này đọc được ở cả Jaeger, Grafana, Datadog. LangSmith thấy được cả chuỗi bước `retrieve → build → agent → tools`, nhưng đòi bạn truyền callback vào mô hình.

OpenLLMetry nằm giữa: dùng chuẩn OpenTelemetry nên đẩy dữ liệu sang Jaeger, Grafana, Datadog đều được. W&B mạnh về so sánh kết quả giữa nhiều lần thử.

Giải nghĩa thêm: trace = bản ghi từng bước của một lần chạy, như video hành trình của request; Jaeger/Grafana/Datadog = ba bảng điều khiển giám sát phổ biến; semantic conventions = bộ tên trường dữ liệu thống nhất (ví dụ `genai.prompt_tokens`), nên backend nào đọc cũng hiểu.

**Làm gì**

1. Bắt đầu bằng Helicone — nhanh nhất, đổi hai biến môi trường là có số liệu chi phí ngay. Biến môi trường = biến cấu hình đặt ngoài code, trong terminal hoặc file `.env`.
2. Cần self-host hoặc privacy-sensitive → dùng Langfuse, nó theo chuẩn OTel GenAI.
3. Dùng LangChain thì chuyển sang LangSmith để xem được từng bước trong chuỗi.
4. Đã có hệ giám sát sẵn (Grafana, Datadog) thì dùng OpenLLMetry để không phải dựng thêm dashboard riêng. Dashboard = bảng điều khiển hiển thị số liệu.
5. Đang làm nghiên cứu, so sánh nhiều biến thể thì dùng W&B.
6. Chỉ ghi lại những trường bạn thật sự dùng để quyết định, ví dụ `session_id`, `user_id`, `tool_name`.

> 📄 **Code ví dụ:** [`examples/01-q1-langsmith-langfuse-helicone-openllmetry-w-b-chon.sh`](examples/01-q1-langsmith-langfuse-helicone-openllmetry-w-b-chon.sh)

**Kiểm tra**

Gọi một lượt thật, mở bảng điều khiển và xác nhận thấy đúng số token đã dùng. Không thấy dữ liệu thì kiểm tra địa chỉ API có thực sự trỏ qua proxy không.

> **Tóm gọn 1 câu:** Chọn theo chỗ bạn phải sửa — Helicone chỉ cần đổi địa chỉ API, Langfuse khi cần tự host dữ liệu, LangSmith khi dùng LangChain, OpenLLMetry khi đã có hệ giám sát, W&B khi so sánh thí nghiệm.

---

## Q2. Loop đang ăn 50.000 token mỗi lượt thay vì 10.000 — biết chỗ nào phình không? [→ Case Studies Thực Tế — Phát Hiện Token Leak]

Token = đơn vị văn bản mà mô hình tính tiền và tính ngữ cảnh; 10.000 token ≈ 30 trang chữ. Loop = vòng lặp agent chạy tự động.

**Bạn sẽ thấy**

Một vòng lặp tên `ci-sweeper`, chạy 5 lần mỗi ngày. Bình thường mỗi lượt hết khoảng 10.000 token, nhưng có lúc lên 50.000. Không rõ nguyên nhân.

Biểu đồ token theo lần gọi cho thấy: lượt thứ 3 luôn gọi `read_file` **15 lần với cùng một file**. `read_file` = tool đọc nội dung file.

**Vì sao**

Vì không có ghi nhận thì bạn đang đoán mò. Nguyên nhân thường gặp nhất là thiếu chỉ dẫn về việc tái dùng kết quả: mỗi lần gặp lại file đó, agent lại đọc từ đầu vì không biết nội dung đã nằm trong ngữ cảnh. Token leak = token rò rỉ — bị tiêu vô ích lặp đi lặp lại, như vòi nước nhỏ giọt.

**Làm gì**

1. Bật theo dõi từng lần gọi công cụ, ghi cả ba trường: tên công cụ, số token đầu vào, tổng token phiên.
2. Tìm các lần gọi lặp lại cùng một tham số trong một phiên — đây là dấu hiệu rò token (token leak). Tham số = giá trị truyền vào lệnh, ví dụ tên file.
3. Thêm chỉ dẫn tái dùng vào prompt: nội dung file đã nằm trong ngữ cảnh thì không đọc lại. Prompt = văn bản chỉ dẫn cho agent.
4. Đo lại sau khi sửa prompt.
5. Nếu vẫn còn, kiểm tra đầu ra của công cụ có bị cắt bớt im lặng không — một tệp 2MB bị cắt còn vài dòng mà không báo, agent sẽ tưởng đã đọc hết và đọc lại.

```text
Trước: lượt #3 → read_file × 15 cùng 1 file
Sau : thêm "reuse file contents if already in context"
Kết quả: giảm 40% token
```

Đoạn này nghĩa là: trước khi sửa, agent đọc cùng một file 15 lần; sau khi thêm một câu chỉ dẫn "nội dung đã có trong ngữ cảnh thì đừng đọc lại", token giảm 40%.

**Kiểm tra**

Chạy lại cùng kịch bản 10 lượt. Token trung bình phải giảm về gần mức cũ, và số lần gọi `read_file` lặp trong một phiên phải về 0.

> **Tóm gọn 1 câu:** Ghi lại từng lần gọi tool để thấy việc lặp; nguyên nhân thường là agent đọc lại thứ đã có trong ngữ cảnh — sửa bằng một câu chỉ dẫn tái dùng.

---

## Q3. Làm sao biết công cụ nào chậm, chỗ nào hỏng? [→ Case Studies Thực Tế — Tool Latency SLO]

Latency = độ trễ — thời gian chờ từ lúc gọi đến lúc có kết quả. SLO = Service Level Objective — mức cam kết dịch vụ, tức ngưỡng "chấp nhận được" mà bạn tự đặt.

**Bạn sẽ thấy**

Danh bạ công cụ đã có sẵn ba số đo theo `harness/06`: `avg_latency_ms`, `success_rate`, `total_calls`. Nghĩa là: độ trễ trung bình tính bằng mili giây (1.000 ms = 1 giây), tỉ lệ lần gọi thành công, và tổng số lượt gọi. Nhưng bạn đang nhìn chúng rời rạc, không ai cảnh báo khi chỉ số xấu đi.

**Vì sao**

Vì ba chỉ số này chỉ có giá trị khi có ngưỡng (SLO — mức cam kết dịch vụ) đi kèm. Biết `vector_search` mất 1.200 mili giây chưa nói lên điều gì; biết rằng vượt 2.000 mili giây thì bật cảnh báo thì mới hành động được. `vector_search` = tool tìm kiếm theo ý nghĩa trong cơ sở dữ liệu vector.

Số liệu thật để bắt đầu: cảnh báo khi truy vấn vector vượt 2.000 mili giây; cảnh báo khi `execute_python` có tỉ lệ thành công dưới 0,95. Truy vấn = câu hỏi gửi tới hệ thống; `execute_python` = tool chạy code Python.

**Làm gì**

1. Ghi số đo sau **mỗi** lần gọi, không chỉ gom theo phiên — nếu chỉ gom cuối phiên thì bạn không biết lỗi xảy ra ở bước nào.
2. Đặt hai ngưỡng cảnh báo: độ trễ trung bình theo từng công cụ, và tỉ lệ thành công theo từng công cụ.
3. Nối cảnh báo vào kênh bạn thật sự nhìn, không phải một bảng điều khiển ai cũng quên.
4. Khi có cảnh báo, mở trace của phiên đó để xem chuỗi bước — công cụ chậm thường do đầu vào quá lớn, không phải do nó bị lỗi.
5. Đo cả số lần gọi: `total_calls` tăng bất thường là dấu hiệu agent đang lặp vô ích.

> 📄 **Code ví dụ:** [`examples/02-q3-lam-sao-biet-cong-cu-nao-cham.py`](examples/02-q3-lam-sao-biet-cong-cu-nao-cham.py)

**Kiểm tra**

Cố tình làm một công cụ chậm lên vài giây, xem cảnh báo có bắn. Tắt công cụ đó đi và xem tỉ lệ thành công có rơi xuống dưới ngưỡng không.

> **Tóm gọn 1 câu:** Ghi chỉ số sau mỗi lần gọi tool, đặt ngưỡng cảnh báo cụ thể theo công cụ, và nối cảnh báo vào kênh bạn thật sự nhìn.

---

## Q4. Không muốn sửa một dòng code nào thì chọn cách nào? [→ Helicone — Proxy Không Cần Sửa Code]

**Bạn sẽ thấy**

Một codebase dài, đụng vào chỗ gọi mô hình là phải đợi duyệt kéo dài tuần. Bạn vẫn muốn biết tuần này hết bao nhiêu tiền và request nào chậm. Request = một lời gọi gửi tới API mô hình.

**Vì sao**

Vì Helicone đứng giữa, không cần bạn can thiệp. Toàn bộ lời gọi mô hình đi qua địa chỉ của nó nên nó nhìn thấy tất cả: số tiền, độ trễ, số request, tỉ lệ lỗi — mà không đụng dòng code nào trong dự án.

Đổi lại, nó **chỉ thấy lời gọi mô hình**. Nó không biết bên trong chuỗi xử lý đã gọi công cụ nào, công cụ nào trả về rỗng. Đó là ranh giới của cách làm này.

**Làm gì**

1. Đặt địa chỉ cơ sở API sang proxy và khoá nhận diện bằng biến môi trường, đặt ở nơi chỉ môi trường chạy được đọc. Khoá nhận diện (API key) = mật khẩu giúp hệ thống biết bạn là ai.
2. Dùng nó để trả lời ba câu hỏi trước khi đầu tư thêm: tiền tăng ở đâu, request nào chậm bất thường, tỉ lệ lỗi là bao nhiêu.
3. Nếu cần xem sâu từng bước trong chuỗi, bổ sung callback theo dõi ở tầng trên — proxy không làm được việc đó.
4. Đừng đưa khoá API vào mã nguồn; biến môi trường phải nằm ở file bị bỏ qua khi commit. Commit = ghi thay đổi vào git; file bị bỏ qua (`.gitignore`) là file không được lưu vào git.
5. Kiểm tra phần đạt dữ liệu: nội dung request của bạn có chứa dữ liệu nhạy cảm cần lọc không.

**Kiểm tra**

Gọi mô hình một lần và xem trong bảng điều khiển có đúng một lượt với đúng số token. Sau đó tắt biến môi trường, gọi lại — lượt đó phải không xuất hiện, chứng tỏ đường đi đã đúng qua proxy.

> **Tóm gọn 1 câu:** Helicone là proxy đứng giữa — chỉ cần đổi địa chỉ API là đo được tiền, độ trễ và tỉ lệ lỗi; đổi lại nó không nhìn thấy từng bước bên trong chuỗi xử lý.

---

## Q5. Đặt luật lưu log ở đây được không? [→ Quan Hệ Với Harness]

Log = bản ghi sự kiện; hợp đồng = bộ quy tắc bắt buộc mọi bên phải theo, như format dữ liệu và thời gian lưu.

**Bạn sẽ thấy**

Bạn muốn quy định: mỗi phiên phải lưu 30 ngày, mỗi trường phải có `session_id`, và không được ghi khoá bí mật. Chữ này xuất hiện trong README của công cụ bạn đang cân nhắc. `session_id` = mã định danh phiên làm việc, dùng để nối các bản ghi về cùng một lượt chạy.

**Vì sao**

Vì thư mục này là **danh mục công cụ**, không phải hợp đồng của hệ thống. Hợp đồng chuẩn về sự kiện — hệ phát ra điều gì, cấu trúc `TrajectoryEvent` dạng nào, khoá nối bản ghi, thời gian lưu, cách lọc dữ liệu nhạy cảm — thuộc về `harness/13-trajectory-observability`. `TrajectoryEvent` = bản ghi một bước trong hành trình của agent; khoá nối bản ghi = trường chung giúp ghép các bản ghi lại với nhau (như số hóa đơn nối các dòng hàng).

Một thư viện ghi log có thể tuân thủ chuẩn đó, nhưng chuẩn không nằm ở thư viện.

**Làm gì**

1. Chốt hợp đồng sự kiện ở `harness/13-trajectory-observability` trước, rồi mới chọn công cụ.
2. Chọn công cụ ở đây theo tiêu chí: có xuất được theo chuẩn OpenTelemetry không, có hỗ trợ lọc dữ liệu nhạy cảm không, có giới hạn thời gian lưu theo yêu cầu không. Redaction = che/lọc dữ liệu nhạy cảm (khoá, mật khẩu) trước khi ghi.
3. Nếu bạn đang định nghĩa cấu trúc trường dữ liệu của sự kiện trong cấu hình công cụ, đó là dấu hiệu đang đặt nhầm chỗ.
4. Gắn khoá nối bản ghi (`session_id`) xuyên suốt từ đầu phiên tới từng lần gọi, nếu không các bản ghi sẽ không nối được với nhau.
5. Kiểm tra xem công cụ có lưu nội dung request không — nếu có, đó là dữ liệu nhạy cảm đang nằm ngoài hệ thống của bạn.

**Kiểm tra**

Đổi công cụ từ A sang B. Nếu hợp đồng sự kiện nằm ở đúng chỗ, chỉ cần sửa cấu hình kết nối. Nếu phải sửa lại code phát sự kiện, thì bạn đang đặt hợp đồng nhầm chỗ.

> **Tóm gọn 1 câu:** Luật về log (lưu bao lâu, schema gì, lọc gì) thuộc về harness/13 — thư mục này chỉ chọn công cụ tuân theo luật đó.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: README.md.*
