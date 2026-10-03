# ❓ FAQ — Guardrails (chuyện thật, dễ hiểu)

Câu hỏi nào khó hiểu thì đọc `README.md` phần trong ngoặc vuông.

---

## Q1. Guardrails AI, NeMo, LlamaGuard — nên chọn cái nào? [→ Tổng Quan Các Guardrails]

**Bạn sẽ thấy**

Ba thư viện này nằm ở ba chỗ khác nhau trong đường đi của một lệnh gọi công cụ (tool call), không phải ba bản thay thế của nhau:

| Thư viện | Nhà phát hành | Chặn ở bước nào | Chặn cái gì |
|---|---|---|---|
| Guardrails AI | Guardrails AI | đầu vào và đầu ra tool call | tham số sai định dạng, path lạ |
| NeMo Guardrails | NVIDIA | luồng hội thoại (rails) | hành vi toàn cuộc thoại |
| LlamaGuard | Meta | nội dung prompt / câu trả lời | nội dung nguy hiểm |

Ví dụ agent hiểu sai prompt và gọi `write_file` với path `/etc/passwd`. Guardrails AI chặn được ngay ở tham số. Nhưng nếu người dùng hỏi "mật khẩu hệ thống là gì?" thì không tham số nào sai — lúc đó mới cần NeMo (dạng rails chặn cả luồng) hoặc LlamaGuard (phân loại nội dung).

**Vì sao**

Vì ba thứ này bảo vệ ba lớp khác nhau. Guardrails AI là bộ quy tắc xác định (deterministic) — rẻ, chắc, chạy tức thì. LlamaGuard là một mô hình ngôn ngữ chuyên phân loại, trả về `safe` hoặc `unsafe` kèm loại vi phạm, nên tốn token và chậm hơn. NeMo mô hỏa hoá cả luồng: đọc file `.co` khai bao cặp "hỏi → trả lời".

**Làm gì**

1. Chặn tham số trước bằng Guardrails AI — lớp rẻ nhất, chạy mọi lệnh gọi.
2. Thêm `requires_permission` và giới hạn tần suất cho từng công cụ trong danh bạ.
3. Chỉ khi hai lớp trên đã xong mới cân nhắc NeMo cho các luồng nhạy cảm (hỏi về bí mật, tiền, dữ liệu cá nhân).
4. LlamaGuard đặt ở đầu vào prompt và đầu ra câu trả lời, dùng để đo xem có bao nhiêu lần suýt lọt.

```python
from guardrails import Guard
from guardrails.hub import RegexMatch

guard = Guard().use(RegexMatch("^[a-zA-Z0-9_./-]+$"))
guard.validate("hacker/path/../etc/passwd")  # fail
guard.validate("src/main.py")                 # pass
```

**Kiểm tra**

Chạy thử `guard.validate` với một đường dẫn chứa `..` và một đường dẫn bình thường — kết quả phải lệch nhau. Với LlamaGuard, gọi một prompt chứa nội dung bị cấm và xem có trả về `unsafe` không.

---

## Q2. Agent ghi file vào chỗ nó không được ghi — chặn ở đâu cho đúng chỗ? [→ Guardrails AI — Validate Input/Output]

**Bạn sẽ thấy**

Hai lệnh gần như giống nhau, một bị chặn một bị cho qua:

```python
guard.validate(path="/etc/hosts")    # REJECT
guard.validate(path="src/main.py")   # ALLOW
```

Không có guardrail thì lệnh đầu đã chạy rồi — `/etc/hosts` bị ghi đè. Đường dẫn đi qua mô tả `write_file`, qua bộ chọn công cụ, qua bộ trích tham số, và chỉ chạm guardrail ở bước `GUARDRAILS CHECK` trước lúc thực thi. Kiểm tra đúng chỗ đó thì chưa đủ: phải kiểm tra **tên tham số**, không phải câu lệnh tự do.

**Vì sao**

Vì mô hình sinh ra text, nó không có khái niệm "tác dụng phụ không mong muốn". Nó sẽ vô tình sinh `/etc/hosts` y như sinh `src/main.py` — cả hai đều là chuỗi ký tự hợp lệ với mặt quy ước. Do đó guardrail phải là **allowlist đường dẫn**: chỉ nhận `src/`, `tests/`, `./`; mọi thứ khác là từ chối.

**Làm gì**

1. Chặn theo allowlist, không chặn theo danh sách đen (denylist). Danh sách đen luôn có lỗ hổng.
2. Kiểm tra tham số ở từng công cụ, với schema khai sẵn: `path` phải là chuỗi khớp `^[a-zA-Z0-9_./-]+$`.
3. Với danh sách đen, phải chuẩn hoá đường dẫn trước: giải mã ký tự → gộp dấu chấm → đổi thành đường dẫn thật → mới so sánh.
4. Chạy kiểm tra này ngay trước lúc ghi, không phải lúc sinh prompt.
5. Kiểm tra luôn đầu ra của công cụ trước khi trả về ngữ cảnh — dữ liệu bên ngoài cũng cần đi qua đây.

```python
from guardrails import Guard
from guardrails.hub import RegexMatch

guard = Guard().use(RegexMatch("^[a-zA-Z0-9_./-]+$"))
result = guard.validate("/etc/hosts")   # REJECT
result = guard.validate("src/main.py")  # ALLOW
```

**Kiểm tra**

Đưa 5 đường dẫn vào: `src/main.py` (cho qua), `/etc/hosts` (chặn), `../../secrets` (chặn), `src/main.py; rm -rf /` (chặn vì có dấu `;` và khoảng trắng), đường dẫn mã hoá kiểu `%2e%2e%2f` (chặn sau khi giải mã). Cả 5 phải ra đúng kết quả mong muốn.

---

## Q3. `requires_permission="elevated"` với `rate_limit_per_minute=60` — khác nhau thế nào, cái nào quan trọng hơn? [→ Permission & Rate Limit Trong Harness]

**Bạn sẽ thấy**

Trong danh bạ công cụ, mỗi công cụ có sẵn bốn con số:

```python
requires_permission: str = "standard"   # standard, elevated, admin
rate_limit_per_minute: int = 60
timeout_seconds: int = 30
max_retries: int = 3
```

Rồi trước lúc chạy có một cổng kiểm tra: nếu `requires_permission` là `elevated` thì hỏi người xác nhận, trả lời không là dừng. Nếu đã vượt giới hạn tần suất thì dừng, không cần hỏi ai.

**Vì sao**

Vì chúng chặn hai thứ khác nhau. `requires_permission` là câu hỏi **"lệnh này có được phép không"** — trả lời là có hay không, cần người quyết. `rate_limit_per_minute` là câu hỏi **"lệnh này có quá nhiều không"** — nó không có ý nghĩa an toàn, chỉ chặn lặp lại vô tình. Ca thật: agent gọi `send_notification` 100 lần trong một lượt. Không lệnh nào nguy hiểm, nhưng người dùng bị spam 100 tin.

Mức độ cần thiết: `elevated` là bắt buộc cho mọi thao tác ghi/xoá/chạy code. Rate limit là tùy chọn nhưng rẻ, nên bật luôn — chi phí một lần kiểm tra số đếm gần như bằng không.

**Làm gì**

1. Gán `standard` cho công cụ chỉ đọc. Gán `elevated` cho mọi thao tác ghi file, chạy mã, gửi thông báo ra ngoài.
2. Chặn tần suất ở mức dưới nhu cầu thật: `rate_limit_per_minute=10` cho `execute_python`, `=1` cho công cụ gửi thông báo.
3. Nối `elevated` lên cổng duyệt của người, không tự quyết.
4. Khi người từ chối thì trả về lý do rõ ràng để agent biết dừng hướng đó, đừng thử lại khác cách.

```python
if tool.requires_permission == "elevated":
    if not human_approve(params): return False
if exceeded_rate_limit(tool): return False
return True
```

**Kiểm tra**

Gọi một công cụ `elevated` mà không có người duyệt — phải bị từ chối. Gọi công cụ tần suất thấp 11 lần trong một phút — lần 11 phải bị chặn. Cả hai thao tác phải ghi lại vào nhật ký kiểm toán.

---

## Q4. Dùng thư viện guardrail có làm chậm agent không? [→ Case Studies Thực Tế]

**Bạn sẽ thấy**

Một vòng lặp (loop) chạy 5 lần mỗi ngày, mỗi lượt gọi hàng trăm công cụ. Thêm một lớp kiểm tra vào giữa mỗi lần gọi thì mỗi lượt chậm thêm, và độ trễ nhân lên.

**Vì sao**

Vì có hai loại chi phí khác nhau. Loại một là kiểm tra bằng quy tắc văn bản: so khớp chuỗi, kiểm tra số đếm — gần như tức thì. Loại hai là gọi một mô hình ngôn ngữ khác để phân loại nội dung — mỗi lần đó là một lượt gọi API có token, có độ trễ, và có thể tốn hơn cả công cụ gốc.

Nguyên tắc: **kiểm tra rẻ trước, kiểm tra đắt sau**. Một chuỗi `..` trong đường dẫn thì không cần mô hình nào để nhận ra.

**Làm gì**

1. Lớp 1 — quy tắc văn bản: chạy cho 100% lệnh gọi, phải dưới vài mili giây.
2. Lớp 2 — kiểm tra quyền và tần suất: tra bảng, gần như miễn phí.
3. Lớp 3 — mô hình phân loại nội dung: chỉ chạy khi lớp 1 và 2 không kết luận được, hoặc chỉ trên đầu vào người dùng chứ không trên mỗi tool call.
4. Ghi số lần bị chặn theo từng loại. Tỉ lệ chặn quá cao ở lớp rẻ là dấu hiệu luật viết sai, phải sửa luật chứ không phải tắt luật.
5. Đo lại số token của loop trước và sau khi thêm guardrail, dùng chính công cụ ở [observability](../observability/).

**Kiểm tra**

Chạy cùng một kịch bản loop có và không có guardrail, so thời gian tổng và số token. Tăng thêm dưới vài phần trăm là chấp nhận được; tăng gấp đôi thì đang gọi mô hình ở sai chỗ — chuyển nó xuống sau lớp quy tắc.

---

## Q5. Guardrail tự quyết định cái gì được phép — có ổn không? [→ Quan Hệ Với Harness]

**Bạn sẽ thấy**

Bạn đang thiết kế một mức rủi ro mới — "ghi vào `docs/` thì mức trung bình" — và muốn đặt luật đó trong thư mục guardrails. Nhưng khi đổi chính sách, chính sách ở hai nơi khác nhau đã lệch nhau.

**Vì sao**

Vì thư mục này là **danh mục sản phẩm**, không phải nơi quy định luật. Thư viện guardrail chỉ **kiểm tra**; nó không quyết định cái gì được phép. Nếu bạn định nghĩa mức rủi ro ở đây, luật đó sẽ tồn tại ở hai nơi và rồi lệch nhau.

**Làm gì**

1. Phân bổ rõ ba chỗ: chính sách cấp quyền và cách ly thuộc `harness/15-approval-gates`; cơ chế cách ly thuộc `harness/12-sandbox-execution`; còn ở đây chỉ chọn thư viện kiểm tra.
2. `elevated` không phải khái niệm của thư viện — nó là khái niệm của harness, ánh xạ sang phân quyền theo vai trò ở `harness/06`.
3. Timeout phải chặn theo kiểu fail-closed: không có phản hồi từ cổng duyệt thì coi như từ chối, không phải cho qua.
4. Mọi lần guardrail chặn đều phải ghi lại lý do. Nếu không phân biệt được "chặn vì path" với "chặn vì hết hạn mức", bạn không sửa được mà cũng không truy vết được.

**Kiểm tra**

Đổi chính sách một lần, chạy lại toàn bộ loop, và xác nhận chỉ có một nơi chứa luật. Nếu bạn phải sửa file ở cả thư mục này lẫn thư mục khác cùng lúc, luật đang nằm sai chỗ.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: README.md.*