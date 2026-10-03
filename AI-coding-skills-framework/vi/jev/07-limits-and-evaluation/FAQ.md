# ❓ FAQ — Jev Không Làm Được Gì, Và Đo Thế Nào Trước Khi Lên Production

Nếu câu hỏi chưa rõ, đọc phần được nêu trong ngoặc vuông.

---

## Q1. Tôi giao việc cho Jev mà nó không làm được — xử lý sao? [→ §1.1, §1.3 Giới hạn]

**Bạn sẽ thấy**

Bạn hỏi Jev đọc nội dung một tệp để tóm tắt, hoặc hỏi nó "còn bao nhiêu ngày nữa thì đến hạn", hoặc đưa ảnh chụp màn hình lỗi vào. API vẫn trả về kết quả hợp lệ, **không báo lỗi** — nhưng kết quả đó vô dụng cho việc bạn cần. Không có thông báo nào kiểu "tôi không làm được việc này".

**Vì sao**

Đây là hậu quả của việc bề mặt kết quả quá gọn: Jev không sinh văn bản, không tự đọc tệp, không xử lý ảnh, và các phép so sánh ngày cũng như phép cộng đếm thuần toán nên để trong code. Vì không có trường "tôi thất bại", bạn phải **tự đặt đúng việc** trước khi gọi. Nếu không, bạn sẽ mất thời gian gỡ lỗi một thứ vốn không thể hoạt động.

**Làm gì**

1. Đọc tệp trong code rồi đưa nội dung đã lọc vào phần trạng thái — đừng mong Jev tự mở.
2. Tính phép trừ ngày, tổng tiền, số dòng trong code; nếu cần phân loại kết quả tính được thì mới nhờ Jev phân loại.
3. Ảnh thì xử lý bằng pipeline thị giác riêng trước, rồi đưa phần chữ đã trích ra cho Jev.
4. Viết hàm bao bọc có điều kiện chặn từ đầu: nếu yêu cầu cần văn bản, cần đọc tệp, hay cần phép tính thì chuyển sang công cụ khác ngay, đừng gọi Jev.

```python
from datetime import date
days_left = (due_date - date.today()).days     # code tính
ans = decide(state=f"Hóa đơn {inv} đến hạn {due_date}, hôm nay {date.today()}",
             questions={"status": {"type": "choice",
                                   "options": ["overdue", "due_soon", "ok"]}})
```

**Kiểm tra**

Duyệt 30 tác vụ trong backlog, tự đánh dấu tác vụ nào cần văn bản, tác vụ nào cần đọc tệp, tác vụ nào cần tính toán. Nếu còn tác vụ loại đó trong danh sách gọi Jev, hãy dời chúng sang đúng công cụ.

---

## Q2. Kết quả luôn đúng kiểu dữ liệu mà vẫn phân loại sai — giải thích sao? [→ §2 Type-safety ≠ correctness]

**Bạn sẽ thấy**

Một nhãn nằm ngoài danh sách của bạn chưa bao giờ xuất hiện, nên bạn tin là đã an toàn. Nhưng bạn đối chiếu với dữ liệu thật và thấy một phần đáng kể bị gán sai nhóm — đôi khi với độ tự tin cao. Bạn kết luận "vậy thì type-safe chỉ là hình thức".

**Vì sao**

Bạn đang gộp hai trục độc lập. **Hình dạng đúng** nghĩa là kết quả luôn nằm trong danh sách bạn định nghĩa, không bao giờ bịa ra lựa chọn lạ — điểm này Jev đảm bảo tuyệt đối. **Nội dung đúng** nghĩa là chọn đúng lựa chọn đó — điểm này không ai đảm bảo. Mô hình có thể tập trung xác suất nhầm vào một nhóm rõ ràng. Hãy nhớ câu chốt: an toàn kiểu dừng ở việc không phát minh ra ngoài danh sách, nó không bảo đảm nhóm được chọn là đúng.

**Làm gì**

1. Không bỏ bước kiểm tra chỉ vì "kết quả có kiểu rồi".
2. Nghiên cứu lại **định nghĩa các nhãn**: nếu hai nhãn chồng lấn, mô hình buộc phải chọn một trong những ô mơ hồ, và độ tự tin thấp là tín hiệu đúng chứ không phải lỗi.
3. Vẫn giữ bước phê duyệt sau khi sinh, và vẫn giữ vùng chuyển người — kể cả ở vùng độ tự tin cao.
4. Đo riêng độ đúng theo từng nhãn để tìm nhãn nào hay bị chọn sai nhất.

**Kiểm tra**

Tính độ đúng riêng cho từng nhãn trên bộ dữ liệu kiểm tra. Nếu một nhãn có độ đúng thấp bất thường, nguyên nhân gần như luôn là mô tả nhãn chồng lấn, không phải mô hình hỏng.

---

## Q3. Trước khi lên production, tôi cần đo những gì? [→ §4 Đánh giá trước khi production]

**Bạn sẽ thấy**

Bạn đọc tài liệu nói "khoảng 80% câu chấm 0.8 là đúng" và định dùng luôn ngưỡng đó. Trước khi lên production, một đồng nghiệp hỏi: con số đó đo trên tập dữ liệu nào? Bạn không trả lời được.

**Vì sao**

Con số đó là số đo trung bình, còn miền của bạn có thể lệch. Đặc biệt, ngưỡng 0.6 cho quyết định gọi công cụ được chọn trên **một tập ticket hỗ trợ nội bộ nhỏ**, chưa được kiểm chứng rộng. Không đo trước thì bạn đang triển khai bằng hy vọng, và mọi ngưỡng sau đó cũng không có cơ sở để điều chỉnh.

**Làm gì**

1. Thu thập mẫu **từ dữ liệu của chính bạn**, có nhãn vàng do người có chuyên môn chấm.
2. Chạy Jev trên từng mẫu, ghi cặp (xác suất, đúng/sai).
3. Vẽ đường hiệu chỉnh: chia theo xác suất, đo tỉ lệ đúng thực tế mỗi nhóm, tính sai số hiệu chỉnh trung bình.
4. Tách một tập giữ lại chưa dùng để kiểm tra, tránh việc vừa dùng vừa kiểm trên cùng một tập.

Các đại lượng nên theo dõi:

| Đại lượng | Trả lời câu hỏi |
|---|---|
| Sai số hiệu chỉnh | Xác suất 0.8 có đúng ~80% không? |
| Độ đúng theo nhãn | Nhãn nào hay bị chọn sai? |
| Tỉ lệ gần hòa | Bao nhiêu % có biên độ mỏng? |
| Độ phủ và độ chính xác | Ở ngưỡng t, bao nhiêu % tự xử lý và đúng bao nhiêu? |

**Kiểm tra**

Ngưỡng trong môi trường thật phải bằng hoặc cao hơn ngưỡng bạn chọn sau khi đo. Nếu bạn phải đặt nhỏ hơn để "chạy cho có", hãy ghi lại lý do và kèm cờ cảnh báo.

---

## Q4. Ngưỡng 0.6 và 0.8 mặc định có dùng luôn được không? [→ §5 Tuning threshold]

**Bạn sẽ thấy**

Bạn đặt ngưỡng mặc định 0.6 cho quyết định gọi công cụ. Sau khi chạy, đội vận hành báo chỉ một phần nhỏ công việc được tự động, phần lớn phải chuyển người. Bạn hạ xuống 0.4 để "tăng tỉ lệ tự động" và gặp sự cố.

**Vì sao**

Con số mặc định là **điểm khởi đầu, không phải giá trị đã kiểm chứng** cho miền của bạn. Sai ngưỡng gây tổn thất theo hai hướng ngược nhau, và cả hai đều rất đắt. Quá thấp thì hành động sai gây sự cố. Quá cao thì dồn hết về người, mất hết lợi ích về tốc độ và chi phí. Không có ngưỡng nào đúng cho mọi miền — và khi mức rủi ro của các câu hỏi khác nhau, ngưỡng phải khác nhau theo từng câu.

**Làm gì**

1. Với mỗi ngưỡng ứng viên, tính **độ chính xác trong nhóm tự xử lý** và **độ phủ**.
2. Chọn ngưỡng **thấp nhất** vẫn đạt độ chính xác theo yêu cầu rủi ro — thường là 95% — để tối đa hoá độ phủ.
3. Đặt ngưỡng riêng theo câu hỏi: câu định tuyến vô hại có thể tự xử lý ở 0.7; câu cho phép hành động phá hại cần tới 0.95.
4. Ghi lại ngưỡng đã áp dụng cùng kết quả thật vào nhật ký, và định kỳ điều chỉnh lại khi dữ liệu đầu vào thay đổi.

```python
rows = sorted(rows, key=lambda r: r["confidence"], reverse=True)
best = None
for i in range(1, len(rows) + 1):
    bucket = rows[:i]
    prec = sum(r["correct"] for r in bucket) / len(bucket)
    if prec < min_precision:
        break                      # thêm mẫu thì độ chính xác tụt
    best = {"threshold": bucket[-1]["confidence"], "precision": prec}
```

Mỗi lần tăng ngưỡng, bạn đánh đổi: ít chuyển giao hơn và chuyển giao đúng hơn, nhưng độ phủ tự xử lý giảm. Cả hai trục đều phải đo, không được bỏ cái nào.

**Kiểm tra**

Trước mỗi lần đổi ngưỡng, chạy lại báo cáo đo trên tập kiểm tra và lưu lại **cả hai** con số: độ chính xác và độ phủ. Một con số đơn lẻ không đủ để ra quyết định.

---

## Q5. Khi có sự cố, tôi truy vết không ra — nhật ký thiếu gì? [→ §6 Observability trong production]

**Bạn sẽ thấy**

Sự cố: ba mươi ticket bị định tuyến sai trong một giờ. Bạn mở nhật ký và thấy đúng một dòng cho mỗi ticket, ghi "đã định tuyến" rồi hết. Bạn không biết xác suất lúc đó là bao nhiêu, ngưỡng đã dùng là bao nhiêu, mô hình phiên bản nào, và kết quả thật ra sao.

**Vì sao**

Nhật ký quyết định chỉ có giá trị khi nó **tái lập được một ca** và **nối được xác suất với kết quả thật**. Thiếu liên kết đó thì bạn không đo được độ hiệu chỉnh trên miền của mình, không điều chỉnh được ngưỡng, và không phát hiện được trôi dữ liệu khi phân phối độ tự tin lệch dần theo thời gian. Có một ranh giới đỏ nữa: phần dữ liệu đầu vào có thể chứa thông tin cá nhân — email, tên, số điện thoại. Ghi thô vào nhật ký là rò rỉ dữ liệu cá nhân.

**Làm gì**

1. Ghi đủ chín trường cho mỗi quyết định: mã yêu cầu, tên câu hỏi, phân phối xác suất đầy đủ, độ tự tin, ngưỡng và vùng đã áp dụng, phiên bản mô hình, hành động đã thực hiện, kết quả thật, thời điểm.
2. **Không** ghi phần dữ liệu đầu vào thô; nếu buộc phải gỡ lỗi thì băm (hash) hoặc che thông tin nhạy cảm, hoặc lưu nơi riêng có kiểm soát truy cập.
3. Ghi số phiên bản mô hình cụ thể — đừng chỉ ghi `jev-latest`, vì bí danh đổi được còn số phiên bản thì không.
4. Theo dõi phân phối độ tự tin và tỉ lệ từng vùng theo thời gian; lệch bất thường là dấu hiệu dữ liệu đầu vào đổi hoặc mô hình đổi phiên bản.
5. Định kỳ gộp cặp (xác suất, kết quả) thành báo cáo hiệu chỉnh theo từng nhãn.

```python
entry = {"ts": ts, "request_id": rid, "questions": names,
         "probabilities": probs, "confidence": round(conf, 4),
         "threshold_low": lo, "threshold_high": hi, "band": band,
         "model": "jev-1.13.0", "outcome": outcome}   # không kèm dữ liệu đầu vào
```

**Kiểm tra**

Chọn ngẫu nhiên 10 dòng nhật ký và trả lời ba câu: ca này dùng mã yêu cầu nào, ngưỡng nào đã áp dụng, hành động là gì. Nếu phải mở dữ liệu đầu vào mới trả lời được, nhật ký của bạn đang thiếu trường.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: README.md.*
