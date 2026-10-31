# ❓ FAQ — Đọc Xác Suất Thật, Đặt Ngưỡng Đúng

Nếu câu hỏi chưa rõ, đọc phần được nêu trong ngoặc vuông. Giải nghĩa nhanh: **confidence** = độ tự tin (mức tập trung của phân phối, không phải xác suất đúng); **ngưỡng (threshold)** = con số ranh giới, vượt thì tự hành động; **escalate** = chuyển cho người hoặc hệ thống khác xử lý.

---

## Q1. Độ tự tin 0.9 nghĩa là 90% đúng — đúng không? [→ §2 confidence ≠ xác suất đúng]

**Bạn sẽ thấy**

Bạn nhận `confidence: 0.9` cho câu chọn và tự động route. Sau đó bạn mở dữ liệu kiểm tra và thấy trong nhóm có độ tự tin từ 0.9 trở lên chỉ khoảng 65% là đúng thật. Bạn tăng ngưỡng lên 0.95 thì vẫn không cải thiện nhiều.

**Vì sao**

Đây là hiểu lầm phổ biến nhất về Jev. Với kiểu chọn và kiểu chấm điểm, `confidence` đo **mức tập trung của phân phối xác suất** — mô hình có *rõ ràng* không, không phải có *đúng* không. Hình dung nó như độ rõ của tiếng radio: tín hiệu rõ ràng nghĩa là không nhiễu, nhưng rõ ràng không bảo đảm đang phát đúng đài bạn cần. Với câu hỏi có/không, độ chắc chắn tính bằng khoảng cách tới 0.5. Cả hai đều là **biên độ**, không phải xác suất đúng.

**Làm gì**

1. Đừng dùng `confidence` làm đại lượng đúng duy nhất — dùng nó cho **việc định tuyến**, còn độ đúng thì đo bằng bộ dữ liệu có nhãn của chính bạn.
2. Đọc thêm **phân phối đầy đủ**, không chỉ giá trị đã chọn. Chênh lệch giữa top-1 và top-2 mỏng là tín hiệu mơ hồ thật.
3. Đặt ngưỡng cao hơn chỉ giải quyết một phần vấn đề: phân phối có thể **nhọn nhầm chỗ** — mô hình rất chắc về một đáp án sai.
4. Ghi nhớ câu này khi thiết kế: an toàn kiểu dừng ở việc không bịa ra đáp án ngoài danh sách, **không** bảo đảm đáp án đó đúng.

```text
Chọn/điểm : confidence = phân phối nhọn đến mức nào → cao khi dữ liệu rõ
Có/không  : chắc chắn = |p − 0.5| × 2               → cao khi p xa 0.5
Cả hai    : đều là biên độ, không phải xác suất đúng
```

Cách đọc khối trên: hàng 1 — với câu chọn/chấm điểm, confidence đo phân phối có "nhọn" không; hàng 2 — với câu có/không, độ chắc chắn tính bằng công thức `|p − 0.5| × 2` (p càng xa 0.5 càng chắc); hàng 3 — cả hai đều là **biên độ**, không phải xác suất đúng.

**Kiểm tra**

Trên bộ dữ liệu có nhãn, vẽ đường hiệu chỉnh: chia theo xác suất rồi đo tỉ lệ đúng thực tế từng nhóm. Nếu đường nằm chéo qua điểm 0/0 và 1/1 thì xác suất đang trung thực với độ đúng. (Đường hiệu chỉnh = biểu đồ so xác suất dự đoán với tỉ lệ đúng đo được; 0/0 và 1/1 = điểm gốc và điểm đỉnh của đường chéo chuẩn.)

> **Tóm gọn 1 câu:** Confidence 0.9 chỉ nghĩa là "phân phối rất nhọn", không phải 90% đúng — độ đúng phải đo bằng bộ dữ liệu có nhãn của chính bạn.

---

## Q2. Mô hình lớn nói "chắc chắn 99%" nhưng tôi đo ra chỉ đúng 60–70% — giải thích sao? [→ §1.1, §1.2 RLHF vs RLVR vs RLCD]

**Bạn sẽ thấy**

Bạn dùng một mô hình lớn cho bước phê duyệt câu trả lời. Nó tự báo độ tin cậy rất cao, giọng điệu chắc nịch, nhưng khi bạn đối chiếu với kết quả đúng thực tế thì con số thấp hơn nhiều. Bạn đang nghi ngờ bộ dữ liệu đánh giá của mình có sai.

**Vì sao**

Không phải dữ liệu sai — đây là hệ quả của cách huấn luyện. Mô hình lớn được tối ưu bằng RLHF, tức theo **sở thích của con người** khi đọc câu trả lời, chứ không theo kết quả đúng/sai. Giọng điệi tự tin là thứ con người thích, nên nó được tối ưu. Thêm nữa, xác suất từng từ trong mô hình lớn không cộng lại thành độ đúng của cả câu trả lời, nên bạn không thể dùng nó làm ngưỡng.

Jev được tối ưu bằng RLCD, tức theo **kết quả thật** của quyết định, trên dữ liệu tổng hợp. Vì vậy con số đo được là: khoảng 80% các câu được chấm điểm 0.8 thật sự đúng. Đó là số đo, không phải lời quảng cáo.

**Làm gì**

1. Đừng dùng độ tự tin tự báo của mô hình lớn làm ngưỡng ở bất cứ đâu.
2. Nếu cần một ngưỡng máy đọc được, hãy lấy nó từ lớp quyết định có kiểu — nơi xác suất được tối ưu theo kết quả thật.
3. Nếu bắt buộc dùng mô hình lớn làm lớp phê duyệt, hãy tự đo độ đúng theo từng nhóm độ tin cậy thay vì tin lời nó nói.
4. Nhớ đây là con số **trung bình**: miền của bạn có thể lệch, nên vẫn phải đo lại trên dữ liệu của bạn.

```text
Mô hình lớn: "chắc chắn 99%"  → thực tế đúng ~60–70%  (tối ưu theo sở thích)
Jev        : xác suất 0.8      → thực tế đúng ~80%     (tối ưu theo kết quả)
```

Cách đọc khối trên: hai hàng so sánh cách hai loại model được huấn luyện — mô hình lớn được khen vì giọng tự tin (nên tự tin quá), còn Jev được chấm theo kết quả thật (nên số nói ra khớp thực tế). **RLHF** = huấn luyện theo sở thích của con người; **RLVR** = huấn luyện theo kiểm tra đúng/sai; **RLCD** = cách Jev được huấn luyện, tối ưu xác suất khớp kết quả thật.

**Kiểm tra**

Chạy 300 câu hỏi có nhãn từ miền của bạn qua cả Jev lẫn lớp phê duyệt hiện tại, rồi so độ đúng trong nhóm điểm cao. Con số nào gần 80% hơn thì lớp đó đáng tin hơn cho ngưỡng tự động.

> **Tóm gọn 1 câu:** Mô hình lớn tự báo 99% nhưng đo chỉ ra 60–70% vì nó được huấn luyện theo sở thích con người; Jev báo 0.8 thì đúng ~80% vì được huấn luyện theo kết quả thật.

---

## Q3. Câu có/không không có trường độ tự tin — code của tôi đọc ra gì? [→ §2.2, §2.3]

**Bạn sẽ thấy**

Bạn viết một hàm đọc kết quả chung cho cả ba kiểu câu hỏi, lấy trường `confidence`. Với câu có/không, trường đó vắng mặt và hàm của bạn trả về `0.0` — mọi câu có/không rơi vào nhánh thấp nhất, kể cả những câu chắc chắn tuyệt đối.

**Vì sao**

Kiểu có/không **không có** trường độ tự tin riêng, vì với câu hỏi nhị phân thì độ chắc chắn đã nằm sẵn trong xác suất: nó chính là khoảng cách từ 0.5, cộng thêm hai lần. Ba giá trị cần phân biệt: `p` là xác suất câu trả lời là "có"; `certainty` là biên độ `|p − 0.5| × 2`; và ở kiểu chọn/chấm điểm thì `confidence` là độ nhọn của phân phối. Còn một cái bẫy nữa: `p` gần 0.5 là **cân bằng**, tức gần như không biết — không phải "trung bình nhưng vẫn chắc".

**Làm gì**

1. Tính độ chắc chắn thủ công: `abs(p - 0.5) * 2`.
2. Dùng hai điều kiện độc lập cho cổng an toàn: `p ≥ 0.85` **và** độ chắc chắn cao mới cho qua.
3. Khi độ chắc chắn thấp, coi như mô hình không biết → hỏi người hoặc đưa sang mô hình lớn, tuyệt đối không tự xử lý.
4. Viết một hàm phân loại khu vực duy nhất, dùng chung cho cả ba kiểu câu hỏi.

> 📄 **Code ví dụ:** [`examples/01-q3-cau-co-khong-khong-co-truong-o.py`](examples/01-q3-cau-co-khong-khong-co-truong-o.py)

**Kiểm tra**

Viết kiểm thử cho hàm phân loại khu vực với bốn đầu vào cố định: 0.01, 0.45, 0.50 và 0.99. Kết quả mong đợi phải là: chắc không, không biết, không biết, chắc có. Nếu 0.45 rơi vào nhánh "trung bình" thì hàm đang sai. (Hàm phân loại khu vực = hàm nhận p, trả về "tự xử lý / hỏi xác nhận / chuyển người".)

> **Tóm gọn 1 câu:** Câu có/không không có trường confidence riêng — hãy tự tính `|p − 0.5| × 2`; p gần 0.5 nghĩa là mô hình không biết, không phải "trung bình".

---

## Q4. Ngưỡng nào là chuẩn — dùng 0.8 hay 0.5? [→ §4.1, §4.2 Ba khu vực]

**Bạn sẽ thấy**

Bạn đọc "khoảng 80% câu chấm 0.8 là đúng" rồi đặt ngưỡng 0.8 và chạy lên production. Sau một tuần, đội vận hành báo họ ngập hàng đầu vì quá nhiều ticket bị chuyển sang người. Nếu bạn hạ ngưỡng xuống 0.5 thì lại có ticket bị xử lý sai.

**Vì sao**

Con số 0.8 là **điểm khởi đầu mang tính gợi ý**, không phải giá trị đã kiểm chứng cho miền của bạn. Ba khu vực chuẩn dùng để chuyển xác suất thành hành động: cao (từ khoảng 0.8) thì code tự làm; vừa (khoảng 0.5 đến 0.8) thì hỏi xác nhận hoặc bổ sung ngữ cảnh; thấp (dưới 0.5) thì chuyển người hoặc hệ thống khác. Chọn sai vùng gây tổn thất theo **hai hướng ngược nhau**: ngưỡng thấp quá thì hành động sai gây sự cố; ngưỡng cao quá thì dồn hết về người, mất hết lợi ích tốc độ.

**Làm gì**

1. Chuẩn bị mẫu đã gán nhãn từ chính dữ liệu của bạn, chạy Jev, ghi lại cặp (xác suất, đúng/sai).
2. Vẽ đường hiệu chỉnh: chia theo xác suất, đo tỉ lệ đúng thực tế mỗi nhóm.
3. Chọn ngưỡng theo mức rủi ro chịu được: hỏi "auto-act được sai bao nhiêu phần trăm?" rồi đặt vùng cao cho vừa đạt, và hỏi "chuyển người tốn bao nhiêu giờ người?" rồi đặt vùng thấp.
4. **Đặt ngưỡng riêng cho từng câu hỏi** khi mức rủi ro khác nhau.

> 📄 **Code ví dụ:** [`examples/02-q4-nguong-nao-la-chuan-dung-0-8.py`](examples/02-q4-nguong-nao-la-chuan-dung-0-8.py)

Một lưu ý quan trọng: ngay cả khi độ tự tin cao, một phân phối **bất thường phẳng** — hai lựa chọn gần bằng nhau — vẫn nên chuyển người. Độ tự tin và biên độ phải được đọc **cùng nhau**, không thay nhau. (Biên độ = chênh lệch giữa lựa chọn đứng đầu và lựa chọn nhì; mỏng nghĩa là phân vân thật.)

**Kiểm tra**

Trước mỗi lần đổi ngưỡng, chạy lại báo cáo đo trên bộ kiểm đánh giá và so hai con số: tỉ lệ đúng trong nhóm tự động, và tỉ lệ phần trăm được xử lý tự động. Bạn cần cả hai, không được hy sinh cái này cho cái kia.

> **Tóm gọn 1 câu:** 0.8 chỉ là điểm khởi đầu — hãy đo trên dữ liệu có nhãn của bạn và đặt ngưỡng riêng cho từng câu hỏi theo mức rủi ro.

---

## Q5. Tôi có nên ghi toàn bộ dữ liệu đầu vào vào nhật ký để tiện gỡ lỗi? [→ §6 Logging & observability]

**Bạn sẽ thấy**

Hai tuần sau một sự cố, câu hỏi lớn nhất của team là "ticket số 4821 tại sao lại bị tự định tuyến sai". Bạn mở nhật ký và thấy chỉ có một dòng "đã định tuyến". Không có xác suất, không có ngưỡng, không có phiên bản mô hình, không có kết quả thật.

**Vì sao**

Nhật ký quyết định chỉ có giá trị khi **nối được xác suất với kết quả thật**. Nếu bạn ghi cả hai, bạn có thể đo độ hiệu chỉnh trên chính miền của mình, điều chỉnh ngưỡng khi nhóm "tự tin cao" thực tế chỉ đúng 70%, phát hiện trôi dữ liệu khi phân phối độ tự tin lệch theo thời gian, và trả lời câu hỏi về một ca cụ thể. Nhưng có một ranh giới đỏ: phần dữ liệu đầu vào có thể chứa thông tin cá nhân — email, tên, số điện thoại, dữ liệu khách hàng. Ghi nó vào nhật ký là rò rỉ dữ liệu.

**Làm gì**

1. Ghi vào nhật ký: mã yêu cầu, tên các câu hỏi, phân phối xác suất đầy đủ, độ tự tin, ngưỡng và vùng đã áp dụng, phiên bản mô hình, hành động đã thực hiện, kết quả thật, thời điểm.
2. **Không** ghi phần dữ liệu đầu vào thô.
3. Nếu buộc phải gỡ lỗi dữ liệu đầu vào, hãy băm (hash) hoặc che thông tin nhạy cảm, hoặc lưu ở nơi có kiểm soát truy cập riêng.
4. Ghi số phiên bản mô hình cụ thể, đừng chỉ ghi `jev-latest` — bí danh đổi được, số phiên bản thì không.

> 📄 **Code ví dụ:** [`examples/03-q5-toi-co-nen-ghi-toan-bo-du.py`](examples/03-q5-toi-co-nen-ghi-toan-bo-du.py)

**Kiểm tra**

Thử một ca giả lập: đọc nhật ký ngẫu nhiên 10 dòng và xác định được mã yêu cầu, ngưỡng đã dùng và hành động đã thực hiện. Nếu phải mở dữ liệu đầu vào mới trả lời được, nhật ký của bạn đang thiếu. (Giả lập = dựng tình huống không có dữ liệu thật; băm (hash) = biến dữ liệu thành chuỗi không đọc ngược lại được; che (redact) = xóa/che thông tin nhạy cảm.)

> **Tóm gọn 1 câu:** Ghi đủ xác suất, ngưỡng, phiên bản model và kết quả thật để truy vết — nhưng tuyệt đối không ghi dữ liệu đầu vào thô vì có thể chứa thông tin cá nhân.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: README.md.*
