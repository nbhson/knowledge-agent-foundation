# ❓ FAQ — Jev & System One Models (những câu người thật hay hỏi)

Nếu câu hỏi chưa rõ, đọc phần được nêu trong ngoặc vuông.

---

## Q1. Tôi đang gọi mô hình lớn chỉ để dán nhãn ticket — có cách nào rẻ và nhanh hơn không? [→ Tổng quan]

**Bạn sẽ thấy**

Agent của bạn chạy vài nghìn lần mỗi giờ, mỗi lần chỉ hỏi hai thứ: "ticket này thuộc team nào" và "khách có yêu cầu hoàn tiền không". Mỗi lần gọi mô hình lớn, bạn chờ 3–329 giây, rồi còn phải dò JSON bằng biểu thức thông thường (regex) và xử lý lỗi parse khoảng 5% số lần. Mô hình viết ra 500 từ văn xuôi chỉ để rồi bị bạn cắt bỏ, giữ lại đúng một danh sách JSON.

**Vì sao**

Bạn đang thuê một nhà văn để điền vào ô checkbox. Việc này là quyết định nhỏ, có cấu trúc, chạy lặp lại hàng nghìn lần — đúng dạng việc mà Jev sinh ra để làm. Jev nhanh hơn 40–200 lần, rẻ hơn khoảng 400 lần (tức khoảng 2 cấp độ magnitude), trả lời trong 70–500 mili-giây với giá 0.042 USD cho 1 triệu token đầu vào, phần đầu ra miễn phí.

**Làm gì**

1. Tách pipeline thành hai lớp: lớp quyết định dùng Jev, lớp viết văn bản mới dùng mô hình lớn.
2. Chuyển các bước "chỉ cần chọn/chấm/kiểm" sang Jev: phân loại, định tuyến, cổng an toàn, chấm điểm.
3. Gom nhiều câu hỏi vào **một** lần gọi — chúng được chấm song song nên gần như không tăng độ trễ.
4. Đặt ngưỡng ở 0.8: khoảng 80% câu được chấm điểm 0.8 thật sự đúng.

```python
resp = client.ask(model="jev-1.13.0", state=ticket_text, questions={
    "team":   {"type": "choice", "choices": ["billing", "tech", "account", "other"]},
    "refund": {"type": "noul", "description": "Khách có yêu cầu hoàn tiền không?"},
})
if resp.answers["refund"].p >= 0.85:
    open_refund_flow()
```

**Kiểm tra**

Đo độ trễ trung bình của một lần quyết định trước và sau khi đổi, tỉ lệ lỗi parse JSON, và tỉ lệ câu có độ tự tin dưới 0.5 (đây là số ca phải chuyển cho người xử lý).

---

## Q2. Jev có phải là mô hình ngôn ngữ không — có thay thế được mô hình lớn của tôi không? [→ Tổng quan]

**Bạn sẽ thấy**

Bạn gửi yêu cầu "viết email xin lỗi khách hàng" và nhận về một nhãn. Hoặc bạn hỏi "câu trả lời này sai chỗ nào" và không có lý do nào được trả về — chỉ có một con số xác suất và câu trả lời đúng kiểu.

**Vì sao**

Jev **không sinh văn bản, không sinh token**. Nó nhận trạng thái đầu vào dạng chuỗi, JSON hay mảng chữ, và trả về quyết định có kiểu kèm phân phối xác suất. Nó cũng được huấn luyện khác: mô hình lớn tối ưu theo sở thích con người (RLHF — "cách diễn đạt này hay hơn"), còn Jev tối ưu xác suất theo kết quả thật (RLCD — "đáp án này có đúng không"). Hệ quả trực tiếp: Jev không viết được, nhưng xác suất của nó dùng làm ngưỡng trong code thì đáng tin.

**Làm gì**

Chọn công cụ theo **hình dạng của câu trả lời**, không theo độ nổi tiếng của công cụ:

| Việc cần làm | Dùng | Lý do |
|---|---|---|
| Định tuyến, phân loại, cổng kiểm tra | Jev | 70–500ms, xác suất dùng làm ngưỡng |
| Chấm mức độ (điểm số) | Jev | Trả cả phân phối theo từng mức |
| Viết email, viết code, giải thích | Mô hình lớn | Cần sinh văn bản |
| Cộng, đếm, so sánh ngày | Code thuần | Cả hai mô hình đều không đáng tin |

Quy tắc hành động: **Jev quyết định, mô hình lớn viết, code thực thi.**

**Kiểm tra**

Lấy 20 request thật từ log của bạn, tự phân loại xem cái nào cần văn bản và cái nào không. Nếu không request nào cần văn bản mà bạn vẫn gọi mô hình lớn, đó là tiền đang đốt.

---

## Q3. Jev có đáng tin không — nó có bao giờ chọn sai không? [→ Tổng quan]

**Bạn sẽ thấy**

Một ticket kỹ thuật rõ ràng bị Jev gán vào nhóm "kế toán" với độ tự tin 0.93 — cao hơn hẳn so với nhóm "kỹ thuật" cũng đang có xác suất không thấp. Code của bạn thấy confidence cao nên tự động route, và ticket đi sai nhóm.

**Vì sao**

Có hai thứ hay bị gộp làm một. Thứ nhất là **an toàn kiểu**: câu trả lời luôn nằm trong danh sách bạn định nghĩa, không bao giờ bịa ra lựa chọn lạ — điểm này Jev đảm bảo tuyệt đối. Thứ hai là **đúng nội dung**: chọn đúng lựa chọn đó — điểm này Jev không hứa gì. Độ tự tin đo **mức tập trung của phân phối xác suất** (câu trả lời có dứt khoát không), chứ không đo mức đúng. Nó có thể dứt khoát mà sai.

**Làm gì**

1. Đọc cả phân phối, không chỉ lựa chọn đứng đầu. Chênh lệch giữa top-1 và top-2 mỏng là tín hiệu phải hỏi người.
2. Đặt ngưỡng theo mức rủi ro: nhóm cũng nguy hiểm thì ngưỡng cao hơn.
3. Không bỏ bước kiểm tra chỉ vì "kết quả có kiểu đúng rồi".
4. Luôn có nhánh chuyển người khi độ tự tin thấp — kể cả khi nó không thấp.

```python
probs = answer["probabilities"]
top = max(probs.values())
second = sorted(probs.values())[-2]
if top - second < 0.15:      # gần hòa → đừng tự quyết
    escalate_to_human(probs)
else:
    route(answer["selected"])
```

**Kiểm tra**

Trên 200–500 mẫu đã gán nhãn đúng của đội bạn, đếm xem trong số ca có độ tự tin trên 0.8 thì bao nhiêu phần trăm thật sự đúng. Nếu con số này lệch xa 80%, ngưỡng của bạn phải nâng lên.

---

## Q4. Tôi muốn đưa Jev vào agent đang chạy — chèn vào đâu? [→ Tổng quan]

**Bạn sẽ thấy**

Mọi bước trong agent của bạn đều gọi mô hình lớn: quyết định dùng công cụ nào, kiểm tra kết quả có đạt không, chọn nhánh tiếp theo. Một lượt đơn giản mất 5–10 giây, và không có chỗ nào để hỏi người khi nghi ngờ.

**Vì sao**

Trong một hệ thống agent có ba tầng quyết định, và tầng giữa đang bị bỏ trống. Tầng dưới là **code cứng**: so trạng thái, dùng biểu thức thông thường hay câu SQL — chắc chắn 100% nhưng không hiểu ngữ nghĩa. Tầng trên là **mô hình lớn**: hiểu ngữ nghĩa rộng nhưng chậm, đắt và xác suất "tự tin" không đáng tin. Jev lấp khoảng giữa: hiểu ngữ nghĩa nhưng có kiểu, có xác suất thật, chạy 70–500ms.

**Làm gì**

1. Chèn một lớp quyết định ngay sau bước code làm sạch và trích xuất dữ liệu.
2. Từ lớp đó, rẽ ba nhánh: độ tự tin cao thì code tự làm; vừa phải thì hỏi xác nhận; thấp thì chuyển người.
3. Chỉ gọi mô hình lớn ở nhánh cần sinh văn bản, và sau khi sinh xong thì quay lại Jev để kiểm tra trước khi dùng.

```
dữ liệu thô → [code: làm sạch, tách số] → [Jev: quyết định có kiểu]
   → cao: code tự chạy   → vừa: xin xác nhận   → thấp: chuyển người
   → cần văn bản: [mô hình lớn viết] → [Jev kiểm tra] → dùng / làm lại
```

**Kiểm tra**

Số lượt gọi mô hình lớn mỗi 100 tác vụ trước và sau khi chèn lớp Jev. Mục tiêu là phần lớn các lượt rẻ và nhanh, chỉ giữ lại mô hình lớn cho đúng những chỗ thật sự cần văn bản.

---

## Q5. Tôi muốn dùng thử — có những đường nào để tích hợp, không phải tự viết HTTP? [→ Tổng quan]

**Bạn sẽ thấy**

Bạn đang phân vân giữa việc tự gọi HTTP thuần, dùng thư viện có sẵn cho lập trình viên (SDK), hay nhét vào framework agent mà bạn đã có sẵn.

**Vì sao**

Jev chỉ có **một** điểm giao diện: `POST https://api.typesafe.ai/v1/systemone`, xác thực bằng khóa dạng `tsk_...`, không có hội thoại nhiều lượt, không có luồng. Bề mặt nhỏ như vậy là lý do tích hợp nhanh — và cũng là lý do bạn phải tự giữ phần ngữ cảnh ở bên ngoài.

**Làm gì**

Chọn theo stack sẵn có của bạn:

| Bạn đang dùng | Dùng gì |
|---|---|
| Python, muốn nhanh nhất | Thư viện `typesafe` (`client.ask`) |
| Node hoặc TypeScript | Thư viện `@typesafe/sdk` |
| Pydantic AI | `TypeSafeModel` + `output_type` |
| LangChain | `TypeSafeClassifier.invoke()` |
| Đã có một khóa cho nhiều model | OpenRouter, model `typesafe/jev-1.13` |
| Quyết định nằm trong truy vấn cơ sở dữ liệu | Spice AI, gọi Jev từ SQL |

Trong production, **ghim phiên bản** `jev-1.13.0` thay vì dùng bí danh `jev-latest`, để không bị thay đổi âm thầm.

**Kiểm tra**

Gọi thử một request có ba câu hỏi (một chọn, một chấm điểm, một có/không) và xác nhận phản hồi trả về đủ ba trường tương ứng, đồng thời thấy trường `usage.output_tokens` bằng 0.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: README.md.*
