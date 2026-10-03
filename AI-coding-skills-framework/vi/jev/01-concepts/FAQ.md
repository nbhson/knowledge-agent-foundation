# ❓ FAQ — Jev Là Gì (khái niệm, ranh giới với mô hình lớn)

Nếu câu hỏi chưa rõ, đọc phần được nêu trong ngoặc vuông.

---

## Q1. "System One model" nghĩa là gì — khác mô hình lớn ở chỗ nào? [→ §2 System One vs System Two]

**Bạn sẽ thấy**

Bạn đọc tài liệu và thấy Jev được gọi là mô hình "System One", còn mô hình lớn là "System Two". Bạn không hiểu tên gọi đó từ đâu, nên không biết khi nào nên chọn cái nào — và cứ chọn nhầm rồi lại sửa lại.

**Vì sao**

Tên gọi lấy từ lý thuyết hai quá trình trong sách *Thinking, Fast and Slow* của Daniel Kahneman. **System One** là suy nghĩ nhanh, tự động, không cần lý lẽ — như cách tay bạn rụt lại trước khi não kịp nghĩ "nóng". **System Two** là suy nghĩ chậm, có lập luận từng bước, tốn sức. Mô hình lớn chạy như System Two: viết lập luận, tốn 3–329 giây. Jev được thiết kế cho System One: quyết định nhỏ có cấu trúc, không cần lời giải thích, 70–500 mili-giây.

**Làm gì**

Dùng ba câu hỏi tự kiểm trước khi gọi bất kỳ mô hình nào:

1. Đáp án có nằm trong một danh sách giá trị tôi đã biết trước không? → có thì Jev.
2. Người đọc kết quả là mắt tôi hay là `if/switch` trong code? → code thì Jev.
3. Tôi có cần phần "tại sao" không? → cần thì mô hình lớn, vì Jev trả quyết định kèm xác suất chứ không trả lý do.

Một khác biệt nữa ít ai để ý: Jev được huấn luyện bằng RLCD (tối ưu xác suất theo kết quả thật), còn mô hình lớn dùng RLHF (tối ưu theo sở thích con người). Đây là lý do xác suất của Jev dùng làm ngưỡng trong code được, còn xác suất của mô hình lớn thì không.

**Kiểm tra**

Vẽ lại ba tầng trên giấy: **code cứng** (chắc chắn 100%, không hiểu ngữ nghĩa) → **Jev** (hiểu ngữ nghĩa hẹp, có xác suất thật) → **mô hình lớn** (hiểu rộng, chậm, xác suất không đáng tin). Mỗi yêu cầu trong backlog của bạn nên rơi vào đúng một tầng. Nếu phần lớn rơi tầng giữa thì bạn đang trả tiền không cần thiết.

---

## Q2. Tại sao Jev bỏ luôn khả năng viết văn bản mà vẫn dùng được? [→ §5 Vì sao bỏ generate text]

**Bạn sẽ thấy**

Bạn giao cho Jev viết một đoạn giải thích ngắn, và nó không trả về gì đọc được. Bạn thấy hàng loạt tính năng bị cắt bỏ: không viết được, không kể chuyện, không tự tạo câu trả lời mới. Trực giác bảo đây là một mô hình bị cắt cụt.

**Vì sao**

Người thiết kế Jev coi việc bỏ văn bản tự do là một **đánh đổi có chủ đích**. Chính sự linh hoạt sinh văn bản tự do là nguồn của ba vấn đề: nó có thể bịa ra ngoài danh sách bạn định nghĩa, JSON sinh ra hay hỏng khiến bạn phải dò bằng regex, và nó chấm từng từ một nên chậm. Đổi lại bạn nhận được bốn thứ: câu trả lời luôn có kiểu, nhiều câu hỏi được chấm song song trong một lượt, xác suất khớp với kết quả thật, và không cần đoạn trích xuất nào.

**Làm gì**

1. Chấp nhận rằng Jev là một **lớp quyết định**, không phải một lớp viết. Tách nó khỏi mọi chỗ cần văn bản.
2. Tận dụng lợi thế song song: gom 10 câu hỏi vào một lượt gọi vẫn chỉ 70–500ms, trong khi 10 lượt gọi tuần tự thì nhân đôi gấp.
3. Bù lại chỗ bị mất bằng mô hình lớn, theo đúng thứ tự: quyết định trước, viết sau.
4. Khi cần biết "tại sao", đừng hỏi Jev — hỏi mô hình lớn dựa trên kết quả Jev vừa trả.

```text
mất đi: giải thích · văn xuôi · dùng chung · sinh tool arguments · >64k token
giữ lại: đúng kiểu · không bịa ngoài danh sách · câu hỏi chạy song song
         · xác suất khớp kết quả thật · không cần dò JSON
```

**Kiểm tra**

Đo trên 100 yêu cầu thật của bạn: tỉ lệ lần gọi mô hình lớn đã giảm bao nhiêu phần trăm, và tỉ lệ JSON hỏng từng phải xử lý là bao nhiêu. Hai con số đó là lý do kỹ thuật để giải thích cho đồng nghiệp.

---

## Q3. Jev đáp ứng trong 70–500ms — tại sao chỗ nào 200ms, chỗ nào 4 giây? [→ §1.1, §4 Kiến trúc]

**Bạn sẽ thấy**

Bạn đo được vài lượt gọi trả về sau 90 mili-giây, vài lượt khác mất 3 giây. Đôi lúc bạn gửi một `state` dài khoảng 40 nghìn token và nhận về lỗi `ModelHTTPError` với mã `max_tokens_exceeded` — không phải lỗi mạng, mà là chặn cứng.

**Vì sao**

Có hai lý do tách biệt. Thứ nhất, khoảng 70–500ms là dải đo được, không phải cam kết cứng; độ trễ phụ thuộc kích thước đầu vào. Thứ hai, còn một giới hạn cứng: **tổng 64 nghìn token** cho trạng thái cộng câu hỏi, trong đó phần trạng thái chiếm tối đa 32 nghìn token cộng phần câu hỏi dài nhất. Vượt ngưỡng là hỏng cứng, không phải báo nhẹ.

Điểm quen thuộc khiến nhiều người tưởng sai: Jev chấm **mọi câu hỏi song song trong một lượt qua duy nhất**. Nên thêm câu hỏi gần như không tăng độ trễ, chỉ tăng tiền theo token đầu vào. Nếu bạn thấy độ trễ nhân theo số câu hỏi, khả năng cao bạn đang gọi tuần tự — hãy gom lại.

**Làm gì**

1. Cắt phần không liên quan ra khỏi trạng thái: bỏ toàn bộ lịch sử hội thoại, chữ ký email, nhật ký gỡ lỗi, HTML thừa.
2. Tóm tắt trong code trước khi gửi, đừng gửi cả tệp log 40 nghìn token.
3. Gom mọi câu hỏi của một bước vào một lượt gọi.
4. Khi gặp `max_tokens_exceeded`, giảm trạng thái — **đừng thử lại mù**.

```python
r = requests.post(API, headers=HEADERS, json={
    "model": "jev-1.13.0",
    "state": core,                       # đã cắt còn phần liên quan
    "questions": questions,              # tất cả trong 1 pass
}, timeout=5)
```

**Kiểm tra**

Đếm số token ước lượng của trạng thái trước khi gửi và từ chối nếu vượt 30 nghìn. Đo độ trễ theo nhóm kích thước đầu vào để biết dải thật của hệ thống bạn, thay vì tin con số trung bình trên tài liệu.

---

## Q4. Nên dùng Jev ở đâu và không nên ở đâu? [→ §6 Khi nào dùng / không dùng]

**Bạn sẽ thấy**

Bạn đã thử đưa Jev vào một tác vụ tổng hợp "viết lại đoạn này cho ngắn gọn và thân thiện hơn". Kết quả trả về vẫn đúng kiểu dữ liệu, không báo lỗi, nhưng vô dụng — không có chữ nào để đọc. Hoặc bạn hỏi nó "tổng số dòng trong tệp là bao nhiêu" và nhận một nhãn không liên quan.

**Vì sao**

Hai sai lầm đối xứng, mỗi sai lầm đều tốn tiền theo một kiểu khác nhau. Giao việc cần sinh văn bản cho Jev là **tốn tiền mà không có kết quả**. Giao việc tính toán chính xác cho Jev là **có kết quả nhưng sai** — và chỗ này nguy hiểm hơn vì nhìn bề ngoài rất bình thường.

**Làm gì**

Dán bảng này cạnh bàn làm việc:

| Bạn cần | Dùng |
|---|---|
| Chọn một giữa vài giá trị đã biết trước | Jev |
| Cổng có/không trước hành động | Jev |
| Mức độ trên thang đã định nghĩa | Jev |
| Sinh văn bản, viết code, viết email | Mô hình lớn |
| Lập luận mở, brainstorm, giải thích dài | Mô hình lớn |
| Cộng, trừ, đếm số, so sánh ngày | Code thuần |

1. Chỉ giao cho Jev việc có **đáp án đóng**.
2. Giữ mọi phép tính và so sánh ngày ở trong code.
3. Nếu một tác vụ cần cả văn bản lẫn quyết định, tách thành hai bước nối tiếp.

**Kiểm tra**

Lấy 30 tác vụ thật trong backlog, tự gạo mỗi cái vào "đáp án đóng" hay "cần văn bản" hay "tính toán". Kiểm tra lại những cái bạn đang giao cho Jev có thật sự nằm trong nhóm đáp án đóng không.

---

## Q5. Tôi có tự chạy được Jev trên máy mình không? [→ §3 Lịch sử & tên gọi]

**Bạn sẽ thấy**

Bạn tìm trên mạng và không thấy tệp trọng số (weights) của Jev, cũng không thấy bài báo khoa học nào. Trong khi mọi mô hình mở khác đều tải về chạy được. Điều này khiến bạn lo rằng mình đang phụ thuộc vào một nhà cung cấp không kiểm soát được.

**Vì sao**

Đây là lựa chọn chiến lược có chủ đích, không phải thiếu sót. Công ty TypeSafe AI hoạt động khoảng hai năm trong im lặng, tuyển người từ các nơi như OpenAI, Google Brain, Meta, Stripe, Docker, rồi công bố sản phẩm vào tháng 9/2026 với khoản tiền hạt giống 40 triệu USD do DCVC dẫn dắt. Họ chọn **sản phẩm trước, giao diện lập trình trước** — nên không phát hành trọng số, không phát hành bài báo, và đầu tư nặng vào tích hợp sẵn ngay ngày đầu. Tên "Jev" lấy từ nhà kinh tế gia William Stanley Jevons và nghịch lý Jevons: máy móc rẻ hơn thì tổng chi phí lại tăng.

**Làm gì**

1. Chấp nhận rằng bạn dùng **một điểm giao diện duy nhất** qua HTTP, và mọi thứ vận hành ngoài mạng.
2. Giảm rủi ro phụ thuộc bằng cách **ghim phiên bản** `jev-1.13.0` thay vì bí danh `jev-latest`, để có thể chủ động nâng cấp sau khi đọc ghi chú phát hành.
3. Bọc toàn bộ lời gọi trong một module nội bộ duy nhất của dự án, để khi giao diện đổi bạn chỉ sửa một chỗ.
4. Ghi lại phiên bản mô hình vào nhật ký quyết định, không chỉ ghi "jev-latest".

```python
MODEL = "jev-1.13.0"   # ghim phiên bản, không dùng alias trong production
resp = client.ask(model=MODEL, state=core, questions=questions)
```

**Kiểm tra**

Trong nhật ký quyết định, mỗi dòng phải có đủ số phiên bản mô hình và mã yêu cầu (`request_id`). Không có hai trường này thì không truy vết được sự cố sau này.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: README.md.*
