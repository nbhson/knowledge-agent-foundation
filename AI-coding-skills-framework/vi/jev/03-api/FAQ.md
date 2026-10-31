# ❓ FAQ — Gọi Jev & Tích Hợp Vào Dự án Của Bạn

Nếu câu hỏi chưa rõ, đọc phần được nêu trong ngoặc vuông.

> **Tài liệu này nói về gì:** cách gọi Jev thật (endpoint = địa chỉ máy chủ nhận request; xác thực bằng API key), xử lý các lỗi hay gặp, và chọn thư viện tích hợp phù hợp.

---

## Q1. Gọi Jev lần đầu thì làm gì, khóa và địa chỉ ở đâu? [→ §1 Endpoint & xác thực]

**Bạn sẽ thấy**

Bạn mới bắt đầu và muốn xem Jev thật sự trả về cái gì. Bạn mở tài liệu, thấy một địa chỉ duy nhất, không có hội thoại nhiều lượt, không có luồng dữ liệu, không có endpoint riêng cho từng việc. Bạn không biết đó là thiếu tính năng hay là bạn đang gọi sai cách.

**Vì sao**

Jev cố tình chỉ có **một** điểm giao diện: `POST https://api.typesafe.ai/v1/systemone` (POST = kiểu HTTP request gửi dữ liệu đi; endpoint = địa chỉ duy nhất nhận lời gọi), xác thực bằng khóa dạng `tsk_...` trong phần đầu `Authorization: Bearer` (Bearer = kiểu xác thực: kèm khóa trong phần đầu của request). Không có hội thoại nhiều lượt nghĩa là **bạn phải tự giữ phần ngữ cảnh**: lượt sau bạn gửi lại trạng thái, Jev không nhớ lượt trước. Đây không phải hạn chế cần vượt, nó là cách bạn kiểm soát được dữ liệu đưa vào.

**Làm gì**

1. Đặt khóa vào biến môi trường `TYPESAFE_API_KEY`, không viết thẳng vào mã nguồn.
2. Gửi đúng ba phần: tên mô hình, phần `state` (chuỗi, JSON, hoặc mảng chữ), và `questions` là một bản tra cứu có tên.
3. Trong production, **ghim** `jev-1.13.0` thay vì dùng bí danh `jev-latest`, để không bị nâng cấp âm thầm.
4. Ghi nhận `request_id` trả về cùng mọi quyết định — không có nó thì không truy vết được sự cố.

> 📄 **Code ví dụ:** [`examples/01-q1-goi-jev-lan-au-thi-lam-gi.sh`](examples/01-q1-goi-jev-lan-au-thi-lam-gi.sh)

Hai mã lỗi xác thực bạn sẽ gặp sớm: **401** là sai hoặc thiếu khóa, **403** là khóa không có quyền hoặc mô hình chưa được bật. Sửa bằng cách kiểm tra lại phần đầu `Authorization`.

**Kiểm tra**

Gọi một lượt với ba câu hỏi (một chọn, một chấm điểm, một có/không) và xác nhận phản hồi có đủ ba nhánh kết quả, đồng thời trường `usage.output_tokens` bằng `0` — dấu hiệu bạn không phải trả tiền cho phần đầu ra.

> **Tóm gọn 1 câu:** Jev chỉ có một endpoint và xác thực bằng khóa `tsk_...` đặt trong biến môi trường (không viết vào code); production phải ghim phiên bản `jev-1.13.0` và luôn lưu `request_id` để truy vết.

---

## Q2. Tôi khai một trường boolean không kèm mô tả, thì báo `UserError` — tại sao? [→ §4.3 Các trường hợp đặc biệt]

**Bạn sẽ thấy**

Trong Pydantic AI, bạn định nghĩa một mô hình kết quả có trường `urgent: bool` không kèm mô tả (Pydantic AI = thư viện Python khai báo kiểu dữ liệu đầu ra cho agent). Chạy thì nhận `UserError` (UserError = lỗi do cách dùng sai của bạn, không phải lỗi hệ thống). Bạn thử bỏ trường `bool` thay bằng `str` thì chạy được. Bạn đang phân vân đây là lỗi trong thư viện.

**Vì sao**

Đây là chốt chặn có chủ đích, không phải lỗi. Trong `TypeSafeModel`, kiểu `bool` được ánh xạ thành câu hỏi có/không (Noul), mà một câu hỏi có/không bắt buộc phải là một **mệnh đề** — phải biết rõ hỏi điều gì. Trường boolean trần không có mệnh đề nào để chấm, nên thư viện từ chối. Ngược lại, `str` hay `Enum` không bị ràng buộc này.

**Làm gì**

1. Thêm mô tả cho **mọi** trường boolean trong mô hình kết quả.
2. Nhớ ánh xạ kiểu: `bool` → có/không, `Literal`/`Enum` → Choice, số nguyên kèm mức → Score.
3. Đặt câu hỏi vào mô tả trường, đặt khung chung vào phần chỉ dẫn — đừng trộn hai thứ.
4. Danh sách trường sẽ tự động lan toả: mỗi phần tử của một danh sách trở thành một câu hỏi riêng, chạy song song.

> 📄 **Code ví dụ:** [`examples/02-q2-toi-khai-mot-truong-boolean-khong-kem.py`](examples/02-q2-toi-khai-mot-truong-boolean-khong-kem.py)

**Kiểm tra**

Chạy kiểm tra tự động trên mọi mô hình kết quả của bạn: quét tìm trường kiểu `bool` không có `description` và fail nếu còn. Đây là loại lỗi dễ tái phát khi thêm trường mới.

> **Tóm gọn 1 câu:** `UserError` với trường boolean là chốt chặn có chủ đích: câu hỏi có/không phải là mệnh đề rõ ràng — hãy thêm mô tả cho mọi trường `bool` trong mô hình kết quả.

---

## Q3. Tôi gặp `ModelHTTPError: max_tokens_exceeded` — sửa thế nào? [→ §7.1, §7.2 Giới hạn và mã lỗi]

**Bạn sẽ thấy**

Request của bạn thất bại với `ModelHTTPError` và mã `max_tokens_exceeded`. Bạn tăng thời gian chờ, thử lại ba lần, vẫn lỗi. Đồng nghiệp bảo "chắc chắn lại mạng" — nhưng mạng vẫn ổn, và lỗi lặp đúng y hệt mỗi lần.

**Vì sao**

Đây là chặn theo kích thước đầu vào, không phải lỗi mạng. Giới hạn là **64 nghìn token tổng** cho trạng thái cộng câu hỏi, trong đó phần trạng thái tối đa 32 nghìn token cộng thêm câu hỏi dài nhất. Vượt ngưỡng là hỏng cứng, không có cảnh báo mềm trước. Nếu bạn thử lại mù thì chỉ tốn thêm token mà không bao giờ qua được.

**Làm gì**

1. Cắt phần không liên quan khỏi trạng thái: bỏ toàn bộ lịch sử hội thoại, chữ ký thư, nhật ký gỡ lỗi, HTML thừa, siêu dữ liệu không dùng.
2. Tóm tắt trong code trước khi gửi — đừng gửi cả tệp log.
3. Rút gọn câu hỏi dài bất thường.
4. Khi vẫn lỗi, **giảm trạng thái**, tuyệt đối không retry mù.

> 📄 **Code ví dụ:** [`examples/03-q3-toi-gap-modelhttperror-max-tokens-exceeded-sua.py`](examples/03-q3-toi-gap-modelhttperror-max-tokens-exceeded-sua.py)

Kèm theo đó, hãy ghi nhớ những việc Jev cố ý không làm, để không mất thời gian thử lại: không sinh văn bản, không viết tham số cho công cụ, không tự đọc tệp, không so sánh ngày hay tính toán. Phép tính và so sánh ngày nên để trong code. Lỗi khác ít gặp hơn: lỗi `ToolCallProposed` là dấu hiệu bạn đang để Jev viết tham số cho công cụ — đó là việc của mô hình lớn phía sau.

**Kiểm tra**

Thêm một bước kiểm tra kích thước trước khi gọi: nếu phần trạng thái ước lượng vượt 30 nghìn token thì chặn và yêu cầu rút gọn. Chạy lại bộ kiểm tra này mỗi khi đổi cách lấy dữ liệu đầu vào.

> **Tóm gọn 1 câu:** `max_tokens_exceeded` là chặn cứng theo kích thước đầu vào (trần 64k token, state tối đa 32k), không phải lỗi mạng — cắt phần thừa và tóm tắt trong code, tuyệt đối đừng retry mù.

---

## Q4. Tôi đã có một khóa cho nhiều mô hình — có phải tạo thêm khóa không? [→ §6 OpenRouter]

**Bạn sẽ thấy**

Đội của bạn đã chuẩn hoá một nhà cung cấp trung gian và dùng một khóa duy nhất cho mọi mô hình (nhà cung cấp trung gian ở đây là OpenRouter — nơi bán lẻ nhiều mô hình qua một khóa). Bạn không muốn thêm một khóa thứ hai vào kho bí mật, và cũng không muốn phải sửa lại toàn bộ lớp gọi mô hình.

**Vì sao**

Jev đã có sẵn trên nhà cung cấp trung gian đó qua một điểm giao diện riêng cho quyết định: `POST https://openrouter.ai/api/alpha/decisions`, với tên mô hình `typesafe/jev-1.13`. Nghĩa là khóa hiện có của bạn vẫn dùng được, không cần khóa mới. Có hai lý do để đi đường này: giảm việc vận hành cho đội đã chuẩn hoá sẵn, và đây cũng là đường chuyển đổi dễ — sau này muốn dùng khóa trực tiếp của TypeSafe thì chỉ đổi địa chỉ nền tảng.

**Làm gì**

1. Nếu dự án đã có lớp gọi mô hình tập trung, chỉ cần trỏ địa chỉ nền tảng và đổi tên mô hình.
2. Nếu gọi trực tiếp bằng HTTP, thay URL và giữ nguyên phần đầu `Bearer`.
3. Chọn đường này khi bạn muốn **một** khóa cho mọi mô hình.
4. Chọn gọi thẳng khi cần độ trễ và tính hành trực tốt nhất, cùng khả năng ghim phiên bản mô hình chặt chẽ hơn.

> 📄 **Code ví dụ:** [`examples/04-q4-toi-a-co-mot-khoa-cho-nhieu.sh`](examples/04-q4-toi-a-co-mot-khoa-cho-nhieu.sh)

**Kiểm tra**

Gọi thử qua đường trung gian và so kết quả với một lượt gọi thẳng cùng nội dung: danh sách xác suất và giá trị đã chọn phải khớp. Nếu lệch, kiểm tra lại tên mô hình và địa chỉ nền tảng.

> **Tóm gọn 1 câu:** Không cần khóa mới — Jev có sẵn trên OpenRouter (`POST /api/alpha/decisions`, tên mô hình `typesafe/jev-1.13`); chọn đường trung gian cho dễ vận hành, chọn gọi thẳng cho độ trễ và ghim phiên bản chặt nhất.

---

## Q5. Tôi nên dùng thư viện nào — Python, JS, LangChain, hay gọi trực tiếp? [→ §3, §8 Bảng tích hợp]

**Bạn sẽ thấy**

Bạn đang phân vân giữa bốn lựa chọn và sợ chọn sai rồi phải viết lại. Một đồng nghiệp bảo "cứ gọi thẳng cho dễ", người khác bảo "nhét vào framework sẵn có đi".

**Vì sao**

Mọi lựa chọn đều bọc cùng một điểm giao diện; khác nhau ở chỗ chúng chuẩn hoá việc đóng gói kết quả và xử lý lỗi. Thư viện chính thức có lợi thế lớn nhất: nó trả về đúng trường của từng kiểu câu hỏi, nên bạn không phải nhớ `confidence` thuộc kiểu chọn và chấm điểm, còn kiểu có/không thì không có trường đó mà chỉ có `p`. Nhầm hai khái niệm này là một lỗi âm thầm — code vẫn chạy, kết quả thì sai.

**Làm gì**

1. Bảng tra cứu nhanh: REST API — mọi nền tảng; thư viện Python — dịch vụ Python; thư viện JS — dịch vụ Node/TypeScript.
2. Pydantic AI (`TypeSafeModel`) khi bạn muốn agent có kiểu đầu ra rõ ràng.
3. LangChain (`TypeSafeClassifier`) khi đã có chuỗi hoặc tầng trung gian và chỉ cần thay phần phân loại.
4. Spice AI khi quyết định nằm ngay trong truy vấn cơ sở dữ liệu, không cần vòng qua tầng dịch vụ.

> 📄 **Code ví dụ:** [`examples/05-q5-toi-nen-dung-thu-vien-nao-python.py`](examples/05-q5-toi-nen-dung-thu-vien-nao-python.py)

Trước khi lên production, đi qua danh sách kiểm tra: đã ghim phiên bản chưa; phần trạng thái đã sạch chưa; mọi trường boolean đã có mô tả chưa; ngưỡng đã định nghĩa và có kiểm thử chưa; nhánh độ tự tin thấp có đường chuyển người chưa; đường xử lý lỗi quá kích thước đã có chưa.

**Kiểm tra**

Viết một bài kiểm tra tự động cho từng kiểu câu hỏi, khẳng định đúng tên trường được đọc ra. Điều này bắt được lỗi đổi tên trường khi bạn nâng cấp thư viện.

> **Tóm gọn 1 câu:** Chọn theo nhu cầu: gọi thẳng cho mọi nền tảng, thư viện Python/JS cho dịch vụ tương ứng, Pydantic AI cho agent có kiểu rõ ràng, LangChain cho chuỗi sẵn có — và nhớ rằng confidence (Choice/Score) khác p (Noul).

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: README.md.*
