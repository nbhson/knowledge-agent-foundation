# ❓ FAQ — Ba Kiểu Câu Hỏi: Chọn, Chấm Điểm, Có/Không

Nếu câu hỏi chưa rõ, đọc phần được nêu trong ngoặc vuông.

> **Tài liệu này nói về gì:** Jev nhận câu hỏi theo ba kiểu (Choice = chọn 1, Score = chấm điểm theo thang, Noul = có/không). File này dạy cách chọn đúng kiểu và đọc đúng kết quả trả về.

---

## Q1. Tôi cần phân loại ticket và cấp độ ưu tiên — dùng Choice, Score hay Noul? [→ §6.1 Bảng quyết định]

**Bạn sẽ thấy**

Bạn thiết kế một màn hình phân loại yêu cầu hỗ trợ và không biết nên hỏi Jev kiểu nào. Bạn thử hỏi "mức độ khẩn cấp" bằng kiểu chọn một giá trị, rồi nhận ra hóa đơn tháng đó có quá nửa là "khẩn cấp" — không dùng được để xử lý gì.

**Vì sao**

Có ba kiểu câu hỏi và mỗi kiểu trả về một hình dạng khác nhau:

Cách đọc bảng này: cột **Kiểu** là tên primitive (primitive = kiểu câu hỏi cơ bản); cột **Bạn định nghĩa trước** là thứ bạn khai báo khi tạo câu hỏi; cột **Nhận về** là kết quả Jev trả. Ví dụ, Choice với 4 giá trị trả về 1 giá trị được chọn kèm xác suất của cả 4 giá trị.

| Kiểu | Bạn định nghĩa trước | Nhận về |
|---|---|---|
| **Choice** (chọn) | Tối đa 255 giá trị | 1 giá trị + xác suất mọi giá trị + độ tự tin |
| **Score** (chấm điểm) | Thang có thứ tự, 2–10 mức | Điểm có trọng số + xác suất từng mức |
| **Noul** (có/không) | Một mệnh đề | Xác suất có đúng không, từ 0 đến 1 |

Quy tắc chọn rất ngắn: đáp án là **một trong tập đã đóng** → Choice. Có **thứ tự, mức độ** → Score. Là **nhị phân** → Noul.

**Làm gì**

1. Nhóm ticket vào đội nào → Choice với `["billing", "tech", "account", "other"]`.
2. Cấp độ ưu tiên → Score với 4 mức `p0` đến `p3`.
3. Có cần hoàn tiền không → Noul với câu hỏi "Khách có yêu cầu hoàn tiền không?".
4. Đặt cả ba câu hỏi trong **một** lượt gọi vì chúng được chấm song song.

> 📄 **Code ví dụ:** [`examples/01-q1-toi-can-phan-loai-ticket-va-cap.py`](examples/01-q1-toi-can-phan-loai-ticket-va-cap.py)

Khi phân loại văn bản do người dùng viết, hãy luôn kèm giá trị `"other"`. Nhưng nếu `"other"` thắng với xác suất cao, đó không phải tín hiệu "chưa rõ" — đó là tín hiệu **bộ danh mục của bạn đang thiếu**. Ngược lại, khi chỉ định tuyến giữa các nhánh workflow đã biết trước thì bỏ `"other"` được.

**Kiểm tra**

Nhìn tỉ lệ xác suất của `"other"` trong 200 ticket thật. Trên 10% là dấu hiệu bộ nhãn chưa bao phủ.

> **Tóm gọn 1 câu:** Chọn kiểu theo hình dạng đáp án — một trong danh sách đã đóng thì dùng Choice, có thứ tự/mức độ thì dùng Score, có/không thì dùng Noul — và đặt cả ba câu trong một lượt gọi cho chạy song song.

---

## Q2. Tôi khai 4 mức nhưng Jev trả về điểm 3.4 — lỗi hay đúng? [→ §3.1 Cách hoạt động]

**Bạn sẽ thấy**

Bạn khai bốn mức `p0, p1, p2, p3` và Jev trả về `score: 3.4` kèm phân phối `{1: 0.01, 2: 0.05, 3: 0.51, 4: 0.43}`. Code của bạn vốn giả định số nguyên nên bạn thêm `int()` và biến 3.4 thành 3. Đồng nghiệp bảo bạn làm mất thông tin.

**Vì sao**

Score trả về **giá trị kỳ vọng** của phân phối trên thang (giá trị kỳ vọng = trung bình có tính trọng số xác suất, nên có thể ra số lẻ), không phải mức được chấm điểm. Khi phân phối dồn một bên, điểm gần đúng số nguyên; khi phân phối nằm giữa hai mức, điểm nằm giữa. Trong ví dụ trên: 51% cho mức 3 và 43% cho mức 4 kéo điểm lên 3.4 — đó là thông tin quý giá, vì nó nói khách đang ở **đúng ranh giới** giữa p2 và p3, mức mà ngưỡng cố định không phân biệt được.

**Làm gì**

1. **Không bao giờ** làm tròn mù quáng trước khi nhìn phân phối.
2. So ngưỡng trên số thập phân: `score >= 3.5` mới báo động, thay vì `score >= 3`.
3. Khi gần ngưỡng, bắt buộc có nhánh hỏi xác nhận thay vì tự quyết.
4. Bản dịch nhãn: `legend` cho biết mỗi mức là gì, nên bạn không cần tự lập bảng tra ở nơi khác.

> 📄 **Code ví dụ:** [`examples/02-q2-toi-khai-4-muc-nhung-jev-tra.py`](examples/02-q2-toi-khai-4-muc-nhung-jev-tra.py)

Cẩn thận một điểm khác: mô tả mỗi mức phải **sắc**. Nếu bạn viết `p1: hơi gấp` và `p2: khá gấp` mà không có tiêu chí phân biệt, mô hình không có gốc để phân phối ra sao. Thay bằng tiêu chí quan sát được: `p1: khách nhắc lần thứ hai, chưa nêu hạn chót`.

**Kiểm tra**

Thử 20 mẫu ở giữa hai mức và xem điểm có nhảy đúng khoảng giữa không. Nếu điểm luôn trùng số nguyên, mô tả mức của bạn đang chồng lấn.

> **Tóm gọn 1 câu:** Điểm 3.4 không phải lỗi — đó là giá trị kỳ vọng của phân phối, nói bạn đang đứng giữa hai mức; hãy so ngưỡng trên số thập phân và đừng làm tròn mù quáng.

---

## Q3. Noul trả về 0.45 — tôi xử lý như "trung bình" hay như "không biết"? [→ §4.1, §4.2]

**Bạn sẽ thấy**

Câu hỏi "Khoản thanh toán này có thể bị lỗi không?" trả về `p: 0.45`. Bạn có đoạn code cũ xử lý ba nhánh: chắc có (từ 0.6 trở lên), trung bình (0.4 đến 0.6), chắc không. Nhánh "trung bình" bảo toàn người dùng — và đó chính là chỗ sai.

**Vì sao**

Với câu hỏi có/không, mô hình **không có trường độ tự tin riêng**. Thứ duy nhất đo được là **khoảng cách tới 0.5**, được gọi là mức chắc chắn và tính bằng công thức `mức chắc chắn = |p − 0.5| × 2`. Với `p = 0.45` thì mức chắc chắn chỉ là 0.10 — tức mô hình **gần như không biết**. Nó đang phân vân thật sự, chứ không phải "nghiêng về không nhưng chưa chắc". Nhánh "trung bình, vẫn khá chắc" là bằng chứng nghe có vẻ hợp lý nhất mà lại là nguy hiểm nhất.

**Làm gì**

1. Tính mức chắc chắn thay vì đoán từ xa: `abs(p - 0.5) * 2`.
2. Nếu mức chắc chắn thấp (dưới 0.2 tức `p` nằm trong khoảng 0.4–0.6) → coi như **không biết**, đưa sang người hoặc LLM.
3. Dùng hai điều kiện cùng lúc cho cổng an toàn: `p ≥ 0.85` **và** mức chắc chắn cao mới cho qua.
4. Nhớ ba số đọc không giống nhau: 0.03 là gần như chắc không, 0.45 là gần như không biết, 0.97 là gần như chắc có.

> 📄 **Code ví dụ:** [`examples/03-q3-noul-tra-ve-0-45-toi-xu.py`](examples/03-q3-noul-tra-ve-0-45-toi-xu.py)

**Kiểm tra**

Cố tình dựng 20 mẫu câu hỏi thật sự mơ hồ (ví dụ văn bản trống, hai nội dung trái chiều) và xác nhận `p` của chúng dồn quanh 0.5. Nếu `p` không bao giờ gần 0.5, mô hình đang "quá tự tin" với câu hỏi đó và ngưỡng của bạn chưa có ý nghĩa.

> **Tóm gọn 1 câu:** 0.45 nghĩa là "gần như không biết" chứ không phải "trung bình" — đo mức chắc chắn bằng `|p − 0.5| × 2`, thấp dưới 0.2 thì đưa sang người hoặc LLM.

---

## Q4. Tôi thêm mười câu hỏi vào một lượt gọi — có bị chậm hơn không? [→ §5 Đánh giá song song]

Phần này về lever hiệu năng lớn nhất của Jev: chấm song song mọi câu hỏi trong một lượt.

**Bạn sẽ thấy**

Bạn cần mười quyết định cho mỗi ticket: phân loại, độc hại, có vi phạm chính sách không, mức độ khẩn cấp, ngôn ngữ, có thông tin cá nhân không… Bản nháp đầu tiên của bạn gửi mười lượt gọi tuần tự và tổng thời gian chờ là 3–4 giây. Dự án sắp lên production.

**Vì sao**

Đây là đòn bẩy thiết kế lớn nhất của Jev và nhiều người bỏ qua. Toàn bộ câu hỏi trong một lượt gọi được chấm **song song trong một lượt qua duy nhất**, nên thêm câu hỏi gần như **không đổi độ trễ** — chỉ thêm chi phí token đầu vào, với mức 0.042 USD mỗi triệu token. Mười câu trong một lượt vẫn 70–500ms; mười lượt gọi tuần tự thì nhân mười lần độ trễ.

**Làm gì**

1. Gom **toàn bộ** quyết định của một bước vào một lượt gọi, không tách vì "cho dễ đọc".
2. Với danh sách dài, sinh câu hỏi động theo chỉ số phần tử: `{f"classify_{i}": ...}` — vẫn một lượt qua, vẫn song song.
3. Nếu danh sách quá lớn không vừa một lượt thì chia thành nhiều lượt **chạy song song**, không phải chạy tuần tự.
4. Tận dụng tên câu hỏi có dấu chấm để ánh xạ về đúng đường dẫn trong JSON, ví dụ `ticket.body.toxic`.

> 📄 **Code ví dụ:** [`examples/04-q4-toi-them-muoi-cau-hoi-vao-mot.py`](examples/04-q4-toi-them-muoi-cau-hoi-vao-mot.py)

**Kiểm tra**

Đo độ trễ khi gửi 1 câu, 5 câu và 20 câu trên cùng một trạng thái. Nếu con số thứ ba lớn hơn thứ nhất gấp đôi, nghĩa là bạn đang gọi tuần tự chứ không gom.

> **Tóm gọn 1 câu:** Thêm câu hỏi vào một lượt gọi gần như không tăng độ trễ (chấm song song trong một lượt qua) — chỉ tăng tiền theo token đầu vào, nên hãy gom mọi quyết định của một bước vào một request.

---

## Q5. Tôi nhét câu "nếu khó hãy chọn other" vào phần dữ liệu — sai không? [→ §6.2 Đâu là câu hỏi, đâu là framing]

Phần này về cách bày dữ liệu đúng chỗ: câu hỏi nằm ở đâu, hướng dẫn chung nằm ở đâu, và phần dữ liệu phải giữ sạch.

**Bạn sẽ thấy**

Bạn dùng thói quen viết lời dẫn của mô hình lớn: dán một đoạn hướng dẫn vào đầu, rồi mới đến dữ liệu thật. Với Jev, kết quả trả về vẫn đúng kiểu nhưng độ tự tin thấp hơn hẳn so với lúc bạn không viết hướng dẫn đó.

**Vì sao**

Với Jev, phần dữ liệu đầu vào là **hồ sơ vụ án**, không phải chỗ để viết hướng dẫn. Bạn viết vào đó câu "hãy trả lời như sau" thì hồ sơ bị bẩn, mô hình bị nhiễu vì nội dung không liên quan, và phân phối xác suất bị loãng ra. Đúng chỗ là: **câu hỏi sống trên kiểu dữ liệu của bạn** (trường `description`), **khung đánh giá sống ở phần chỉ dẫn chung** (mức instruction), và **phần dữ liệu giữ sạch**.

**Làm gì**

1. Chuyển mọi câu hỏi từ phần dữ liệu sang trường `description` của từng câu hỏi.
2. Với câu hỏi có/không, đặt tiêu chí "khi nào thì tính là có" vào `description` chứ không vào dữ liệu.
3. Đặt framing chung của cả nhóm vào phần chỉ dẫn, áp cho mọi câu hỏi trong nhóm.
4. Dọn phần dữ liệu: bỏ hướng dẫn thừa, giữ nguyên tắc chỉ phần liên quan.

> 📄 **Code ví dụ:** [`examples/05-q5-toi-nhet-cau-neu-kho-hay-chon.py`](examples/05-q5-toi-nhet-cau-neu-kho-hay-chon.py)

Quy tắc rút gọn: **đặt câu hỏi lên kiểu, đặt khung vào chỉ dẫn, giữ dữ liệu làm nguyên liệu.**

**Kiểm tra**

Chạy 50 mẫu có sẵn với hai biến thể: một bản có hướng dẫn nhét trong dữ liệu, một bản sạch. So độ tự tin trung bình của hai bản — bản sạch phải cao hơn rõ rệt.

> **Tóm gọn 1 câu:** Phần dữ liệu (state) là "hồ sơ vụ án" phải giữ sạch — đặt câu hỏi lên trường `description`, đặt khung đánh giá vào phần instructions, không nhét hướng dẫn kiểu prompt vào giữa dữ liệu.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: README.md.*
