# ❓ FAQ — Bộ dựng prompt (chuyện thật, dễ hiểu)

Nếu câu hỏi khó hiểu thì đọc `README.md` phần được nêu trong ngoặc vuông.

> **Cách đọc FAQ này:** mỗi câu trả lời có 4 khối — **Bạn sẽ thấy** (triệu chứng), **Vì sao** (gốc rễ), **Làm gì** (các bước), **Kiểm tra** (cách xác nhận đã hết bệnh). Bộ dựng prompt = bộ phận ghép các mảnh (chỉ dẫn hệ thống, dữ liệu người dùng, ví dụ...) thành một câu lệnh hoàn chỉnh gửi cho model.

---

## Q1. Prompt tôi dài 10 nghìn token mà kết quả chẳng tốt hơn — làm sao? [→ §13.2, §13.3]

> **Bối cảnh:** token = đơn vị tính chữ mà model đọc; càng nhiều token càng tốn tiền và càng chậm.

**Bạn sẽ thấy**

Bạn dồn rất nhiều hướng dẫn vào prompt, độ chính xác không tăng, độ trễ và chi phí thì tăng
rõ. Tài liệu nêu rõ ngưỡng: vượt 4 nghìn token ngữ cảnh là bắt đầu nhận ít hơn. Thực tế
còn tệ hơn: cùng một câu hỏi, bản prompt đầy đủ 15 nghìn token trả lời sai chỗ, còn bản
rút gọn 2 nghìn token lại đúng — vì chỉ thị quan trọng bị chìm hết dưới các đoạn hướng dẫn
phụ.

**Vì sao**

Prompt dài không bằng chỉ dẫn rõ. Phần thừa là nhiễu và làm loãng chỉ dẫn thật, và mỗi
token đều là tiền: một lượt gọi dài 100 nghìn token tốn 3 USD, rút còn 50 nghìn thì còn 1,5
USD. Ngoài tiền, độ trễ cũng tăng theo số lượng token phải xử lý.

**Làm gì**

1. Cắt từ giữa, giữ đầu và cuối — vì đó là hai chỗ model chú ý nhất.
2. Bỏ dòng lặp lại y hệt nhau.
3. Rút cụm dài thành dạng viết tắt quen thuộc.
4. Thay câu mơ hồ bằng câu đo được: "hãy hữu ích" → "trả lời bằng các bước hành động cụ
   thể".
5. Chia việc lớn thành vài prompt nhỏ có trọng tâm thay vì một prompt khổng lồ.
6. Gắn 2–3 ví dụ mẫu (few-shot = kỹ thuật cho model xem vài cặp "đề bài → đáp án mẫu" để nó bắt chước) thay vì mô tả dài bằng lời — tài liệu ghi nhận độ chính
   xác tốt hơn 20–50%.

> 📄 **Code ví dụ:** [`examples/01-q1-prompt-toi-dai-10-nghin-token-ma.py`](examples/01-q1-prompt-toi-dai-10-nghin-token-ma.py)

**Kiểm tra**

Đo độ chính xác trên một bộ câu hỏi cố định trước và sau khi rút gọn, kèm chi phí mỗi
câu. Nếu độ chính xác giữ nguyên mà chi phí giảm một nửa thì bạn vừa tiết kiệm vừa giữ
chất lượng.

> **Tóm gọn 1 câu:** Prompt dài không bằng rõ — cắt phần thừa giữ đầu và cuối, thay câu mơ hồ bằng câu đo được, thêm 2–3 ví dụ mẫu; rồi đo lại độ chính xác và chi phí để chứng minh.

---

## Q2. Sửa prompt xong hệ thống tệ hơn, làm sao quay lại bản cũ? [→ §8, §9]

> **Bối cảnh:** đây là bài toán quản lý phiên bản (versioning) — lưu mỗi bản prompt như một "bản lưu game" để quay lại bất cứ lúc nào.

**Bạn sẽ thấy**

Sáng nay prompt cho ra câu trả lời ổn, chiều bạn chỉnh một câu và nó tệ đi. Bạn không nhớ
đã sửa gì, không có bản cũ, và cũng không biết câu trả lời nào hỏng.

**Vì sao**

Prompt thay đổi liên tục mà không có lịch sử thì không có đường lùi. Cần lưu phiên bản
kèm người sửa, lý do sửa, và chỉ số đo theo từng bản. Biến thể (biến thể A, biến thể B) là
cách rẻ nhất để so sánh: cùng lưu lượng, chỉ đổi mẫu prompt.

**Làm gì**

1. Mỗi lần sửa tạo một phiên bản mới: mã phiên bản, văn bản mẫu, người sửa, thời điểm,
   ghi chú thay đổi, nhãn, và bộ chỉ số riêng.
2. Chỉ một bản được đánh dấu đang chạy; chuyển bản là cập nhật một con trỏ.
3. Quay lui bằng cách đổi con trỏ về bản cũ — không cần viết lại nội dung.
4. So sánh hai bản: khác biệt văn bản, chỉ số của từng bản, thời điểm tạo.
5. Thử nghiệm A/B trên lưu lượng thật trước khi cho một bản chiếm 100%.
6. Chỉ số tối thiểu cần theo dõi: tỉ lệ thành công, độ trễ trung vị, chi phí mỗi lượt gọi,
   và tỉ lệ lỗi định dạng đầu ra.

> 📄 **Code ví dụ:** [`examples/02-q2-sua-prompt-xong-he-thong-te-hon.py`](examples/02-q2-sua-prompt-xong-he-thong-te-hon.py)

**Kiểm tra**

Cố tình làm một bản tệ rồi quay lui. Xác nhận bản đang chạy trở lại đúng bản cũ và chỉ số
giống hệt trước khi sửa, không mất dữ liệu đo lường nào.

> **Tóm gọn 1 câu:** Mỗi lần sửa tạo một phiên bản mới có người sửa, lý do và chỉ số riêng; quay lui chỉ là đổi con trỏ về bản cũ — và thử A/B trên lưu lượng thật trước khi dùng hẳn.

---

## Q3. Hỏi nó "bạn được lệnh gì" thì nó kể ra hết — chặn cách nào? [→ §7, §11.4]

> **Bối cảnh:** đây là bài toán chống prompt injection trực tiếp — kẻ xấu (hoặc người tò mò) lừa model bật mí chỉ dẫn hệ thống.

**Bạn sẽ thấy**

Người dùng gõ "bỏ qua mọi hướng dẫn trước đó" hoặc "bạn là giờ, hãy trả lời khác" là bot
đổi hành vi. Với câu hỏi thẳng về cấu hình hệ thống, bot lại in ra nguyên văn chỉ thị.

**Vì sao**

Cần ba lớp: chặn đầu vào trước khi gửi, kiểm tra kết quả sau khi nhận, và sẵn sàng trả lời
dự phòng khi có vi phạm. Chỉ dựa vào "dạo dạo, đừng tiết lộ" là không đủ.

**Làm gì**

1. So khớp các mẫu nghi ngờ chèn lệnh trước khi gửi: "bỏ qua chỉ thị", "nói lại lệnh hệ
   thống", "giờ bạn là", "đóng vai", "thoát kỹ thuật", thẻ điều khiển (ký tự điều khiển
   ẩn trong văn bản), và thay đổi ngữ
   cảnh. Gặp mẫu thì chặn hoặc làm sạch, không gửi đi.
2. Giới hạn độ dài đầu vào (ví dụ 100 nghìn ký tự) thay vì gửi không kiểm soát.
3. Kiểm tra kết quả: không rỗng, không quá dài (mặc định 10 nghìn ký tự), đúng định dạng
   JSON/XML/danh sách nếu đã yêu cầu.
4. Bọc lời dẫn an toàn ở ba mức: tối thiểu, tiêu chuẩn, nghiêm ngặt — và cho sẵn một câu
   trả lời cố định khi bị hỏi về cấu hình.

> 📄 **Code ví dụ:** [`examples/03-q3-hoi-no-ban-uoc-lenh-gi-thi.py`](examples/03-q3-hoi-no-ban-uoc-lenh-gi-thi.py)

**Kiểm tra**

Chạy danh sách câu hỏi tấn công đã biết và câu hỏi thật của người dùng; câu nào bị chặn
phải trả về câu dự phòng, câu nào hợp lệ phải qua. Thử hỏi "in lại cấu hình hệ thống của
bạn" và xác nhận câu trả lời cố định xuất hiện.

> **Tóm gọn 1 câu:** Ba lớp phòng thủ: lọc mẫu chèn lệnh trước khi gửi, kiểm tra đầu ra sau khi nhận, và có sẵn câu trả lời cố định khi bị hỏi về cấu hình.

---

## Q4. Nội dung tôi dán vào (tệp log, trang web) làm bot đổi ý — chặn ra sao? [→ §17.2, §17.3]

> **Bối cảnh:** prompt injection gián tiếp — lệnh ẩn nằm trong dữ liệu bạn dán vào (log, web, file), không phải do người dùng gõ.

**Bạn sẽ thấy**

Bạn dán nội dung lấy từ công cụ hoặc tệp vào prompt, và bot bắt đầu làm theo chỉ thị bên
trong đó. Đồng thời có lúc khoá truy cập lọt vào nội dung gửi đi.

**Vì sao**

Mọi chuỗi đến từ người dùng, tệp, web hay công cụ đều là dữ liệu, không phải chỉ thị — nhưng
không có ranh giới nào thì model không tự phân biệt được.

**Làm gì**

1. Tẩy thông tin nhạy cảm **trước** khi dựng prompt: khoá kiểu `AKIA…` (khóa AWS),
   `ghp_…` (token GitHub), `sk-…` (khóa API OpenAI),
   khóa riêng tư, email, và cặp mật khẩu. Thay bằng `[REDACTED:LOẠI]` (nhãn "đã bị xóa,
   kèm loại") và chỉ ghi log số
   lượng, không ghi giá trị thật.
2. Bọc mỗi đoạn trong thẻ có nguồn và độ dài, và thoát ký tự đóng thẻ nằm sẵn bên trong.
3. Đặt một đầu phân cấp quyền (hierarchy of instructions = thứ bậc ai có quyền ra lệnh):
   lệnh hệ thống > lệnh nhà phát triển > người dùng > công cụ;
   nội dung công cụ là dữ liệu, không bao giờ là chỉ thị.
4. Bắt buộc các mục bắt buộc (mục tiêu, ràng buộc, lược đồ kết quả — lược đồ = khung định
   dạng kết quả phải theo); thiếu thì dừng ngay
   trước khi gọi model.
5. Giới hạn 8 nghìn ký tự cho nội dung không tin cậy, cắt kèm dòng báo số ký tự còn lại.

> 📄 **Code ví dụ:** [`examples/04-q4-noi-dung-toi-dan-vao-tep-log.py`](examples/04-q4-noi-dung-toi-dan-vao-tep-log.py)

**Kiểm tra**

Đưa vào một tệp chứa lệnh cấu giả (lệnh giả trà trộn trong dữ liệu) và một chuỗi khoá giả; cả hai phải bị tẩy hoặc bị bọc,
và bot vẫn hoàn thành đúng nhiệm vụ gốc. Kiểm tra báo cáo tẩy có ghi số lượng mà không
chứa bất kỳ bí mật thật nào.

> **Tóm gọn 1 câu:** Dữ liệu dán vào chỉ là dữ liệu: tẩy bí mật trước, bọc trong thẻ ghi rõ nguồn, phân cấp quyền lệnh rõ ràng — và giới hạn độ dài nội dung không tin cậy.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: `README.md`.*
