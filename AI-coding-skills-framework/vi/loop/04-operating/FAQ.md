# ❓ FAQ — Operating Loops trong Production (những câu người thật hay hỏi)

Câu hỏi nào khó hiểu thì đọc phần trong ngoặc vuông — nó trỏ tới mục tương ứng trong README vận hành. "Production" = môi trường chạy thật.

---

## Q1. Bật loop chạy mỗi 5 phút một lần thì hết bao nhiêu tiền, có nên làm không? [→ §1. Token & Cost Budgeting]

Phần này giải thích cách ước lượng chi phí trước khi bật loop. "Token" = đơn vị tính dữ liệu vào/ra của mô hình, tức đơn vị tính tiền.

**Bạn sẽ thấy**

Nhìn khoản tiền trên bảng điều khiển mà bạn không hiểu vì sao con số lớn dần. Một loop quét nhẹ với nhịp 15 phút tốn khoảng 5 triệu token mỗi ngày nếu chạy trọn bộ; đổi sang 5 phút thì con số nhân lên gần 300 lần.

**Vì sao**

Chi phí nhân theo tích của ba thứ: số lần chạy, số sub-agent mỗi lần chạy, và độ lớn ngữ cảnh ("context" = khối dữ liệu gửi cho model mỗi lượt). Nhịp nhanh nhất là yếu tố nhân tuyến tính, không phải yếu tố nhỏ nhất — chạy 5 phút một lần là 288 lần chạy mỗi ngày, chạy 1 ngày một lần là 1 lần chạy.

**Làm gì**

1. **Ước lượng trước khi hẹn giờ** bằng lệnh tính chi phí theo kiểu loop, nhịp chạy và mức tự chủ.
2. **Đặt trần chi phí theo ngày** và dòng "vượt thì dừng bộ hẹn giờ, báo người" — trần này chỉ có tác dụng khi agent không tự sửa được nó.
3. **Giới hạn số sub-agent mỗi lần chạy** (ví dụ 3), vì mỗi sub-agent là một vòng gọi mô hình trọn vẹn — tức là một lượt trả tiền riêng.
4. **Quét nhẹ, làm mới khi có việc**: danh sách rỗng thì thoát sớm dưới 5.000 token — đừng chạy trọn bộ cho có.
5. **Khai sinh sẵn** file ngân sách, file log chạy và skill kiểm tra chi phí — tạo trước, đừng đợi vượt trần mới lo.

> 📄 **Code ví dụ:** [`examples/01-q1-bat-loop-chay-moi-5-phut-mot.sh`](examples/01-q1-bat-loop-chay-moi-5-phut-mot.sh)

| Kiểu loop | Nhịp | Số lần chạy/ngày | Token ước tính |
|---|---|---|---|
| Quét hằng ngày, chỉ báo cáo | 1 ngày | 1 | ~50k |
| Dọn CI, bản nhẹ | 15 phút | 96 | ~5M (nên tránh) |
| Theo dõi pull request | 5 phút | 288 | Cao — phải thoát sớm |

Cách đọc bảng: "Nhịp" = khoảng cách giữa hai lần chạy; "Token ước tính" = tiền dự kiến mỗi ngày. Ví dụ dòng 2: loop dọn CI chạy 96 lần/ngày → khoảng 5 triệu token/ngày nếu mỗi lần chạy đầy đủ — số cần tránh.

**Kiểm tra**

Đo một ngày thực tế rồi so với con số ước lượng. Lệnh kiểm tra chi phí phải chặn được loop không ghi đè lên trần trong file ngân sách — nếu agent tự sửa trần thì trần vô nghĩa.

> **Tóm gọn 1 câu:** Chi phí = số lần chạy × số sub-agent × độ lớn ngữ cảnh, nên ước lượng trước, đặt trần và thoát sớm khi không có việc.

---

## Q2. Tuần sau muốn hỏi "sao hôm thứ Ba nó tự sửa file đó", mở đâu ra xem? [→ §2. Logging Mỗi Run]

Phần này giải thích cách ghi log để lần sau còn tra cứu. "Log" = nhật ký ghi lại mỗi lượt chạy.

**Bạn sẽ thấy**

Bạn cuộn lại đoạn chat với agent, tìm mã hợp đồng cũ, không thấy. Lịch sử cuộc trò chuyện bị cắt đoạn, có lần agent tự tóm tắt sai. Không có cách nào biết lúc đó nó thấy mục nào và quyết định gì.

**Vì sao**

File log là **hộp đen** của loop: mỗi lần chạy ghi một dòng trả lời chạy bao lâu, tìm được gì, làm gì, tốn bao nhiêu, kết thúc ra sao. Chuẩn là chỉ thêm, không sửa, không xoá ("append-only") — sửa được thì không còn đáng tin, vì không ai biết dòng nào đã bị đổi.

**Làm gì**

1. **Ghi một mục cho mỗi lần chạy** vào file log, tối thiểu có: mã lần chạy ("run_id"), kiểu loop, thời gian chạy, số mục tìm được, số hành động, số lần phải báo người, ước lượng token, kết quả.
2. **Dùng mã lần chạy là thời điểm** theo chuẩn quốc tế ("ISO timestamp", kiểu `2026-06-09T08:15:00Z`) để tra cứu là duy nhất, không đụng nhau.
3. **Ghi thêm mẫu ngắn cho người đọc** ở cuối file trạng thái, phòng khi không mở được bản ghi có cấu trúc.
4. **Chỉ thêm, không sửa** — kể cả khi lần chạy đó thất bại; thất bại càng cần log để tra nguyên nhân.

> 📄 **Code ví dụ:** [`examples/02-q2-tuan-sau-muon-hoi-sao-hom-thu.json`](examples/02-q2-tuan-sau-muon-hoi-sao-hom-thu.json)

**Kiểm tra**

Chạy 10 lần rồi đếm số mục log — phải đúng 10, và phải chứa cả những lần không làm gì. Sau đó mở file log từ mục `run_id` mà `STATE.md` đang trỏ tới, bạn phải trả lời được "sao thứ Ba nó làm vậy".

> **Tóm gọn 1 câu:** Mỗi lần chạy ghi một dòng log chỉ-thêm-không-sửa — log là hộp đen duy nhất giúp bạn lần ra "sao hôm đó nó làm vậy".

---

## Q3. Làm sao biết loop có thật sự ích hay chỉ đốt tiền làm nhiễu? [→ §3. Metrics Dashboard]

Phần này giải thích cách đo hiệu quả loop bằng số liệu thay vì cảm tính. "Metrics" = các chỉ số.

**Bạn sẽ thấy**

Ba loop chạy đều đều, thông báo vẫn về mỗi ngày, nhưng không ai biết chúng tìm được gì. Hỏi team thì ai cũng nói "chắc ổn". Biểu phí thì tăng đều.

**Vì sao**

Cảm giác không phải số liệu. Vòng này là nơi bạn đo chất lượng tín hiệu mà loop mang về — và đặc biệt là đo **tỉ lệ báo động giả** ("false positive rate" = tỉ lệ cảnh báo sai): nếu phần lớn cảnh báo là sai thì con người sẽ tắt thông báo, và loop chết trong im lặng mà không ai hay.

**Làm gì**

1. **Mở bảng theo tuần**, một cột cho mỗi kiểu loop.
2. **Ghi đủ bảy dòng số liệu**: số lần chạy, số phát hiện đáng xử lý, số bản sửa được đề xuất, số lần phải báo người, số báo động giả, thời gian trung bình đến lúc người biết, và ước lượng token đã dùng.
3. **So sánh xu hướng theo tuần**, không nhìn một con số đơn lẻ — một điểm số không nói được loop đang tốt lên hay xuống.
4. **Đặt ngưỡng cảnh báo**: tỉ lệ báo động giả vượt 30% thì giảm tốc loop đó, kể cả nó chưa làm hỏng gì.
5. **Chọn số liệu thành công riêng cho từng kiểu loop**, vì "chạy bao nhiêu lần" không phải số liệu thành công — chỉ số phụ thuộc vào việc loop đó làm gì.

**Kiểm tra**

Mỗi kiểu loop phải có đủ bảy dòng số liệu có giá trị, và bảng phải đủ để trả lời "loop này giúp tiết kiệm bao nhiêu thời gian người" chứ không chỉ "chạy bao nhiêu lần".

> **Tóm gọn 1 câu:** Đo loop bằng bảng số liệu theo tuần — đặc biệt là tỉ lệ báo động giả; cảm giác "chắc ổn" không phải bằng chứng.

---

## Q4. Khi nào nên giảm tốc, tạm dừng, hay dừng hẳn một loop? [→ §4. Khi Nào Slow Down / Pause / Kill]

Phần này giải thích ba mức can thiệp vào loop, theo độ nghiêm trọng tăng dần.

**Bạn sẽ thấy**

Có sự cố lúc 2h sáng, loop vẫn tự chạy và có thể ghi đè bản vá khẩn cấp của người ("hotfix" = bản sửa gấp). Nhịp chạy đã 15 phút nhưng nhịp 5 phút không tạo thêm giá trị gì, chỉ tăng chi phí.

**Vì sao**

Ba mức này ứng với ba mức nghiêm trọng khác nhau: giảm tốc là vì sắp cạn, tạm dừng là vì đang có nguy hiểm trước mặt, dừng hẳn là vì con đường này không còn đáng đi. Dừng hẳn là quyết định về giá trị, không phải về sự cố.

**Làm gì — theo thang đo dầu phanh**

1. **Giảm tốc** khi: đã dùng hơn 80% ngân sách giữa tuần; tỉ lệ báo động giả trên 30%; cùng một việc phải báo người từ 2 lần trong 48 giờ; hoặc đang trong tuần phát hành lớn thì chuyển sang chỉ báo cáo.
2. **Tạm dừng** khi: đang có sự cố chạy thật ("production incident"); đang di chuyển cấu trúc dữ liệu phá vỡ tương thích ("breaking migration" = đổi cấu trúc database khiến bản cũ không đọc được); hoặc người review chính đang nghỉ mà tự gộp vẫn bật.
3. **Dừng hẳn** khi: liên tục lỗi ở mức nghiêm trọng; chi phí lớn hơn giá trị trong hai tuần liên tiếp; cả team đã tắt thông báo; hoặc đã có cách khác thay thế tốt hơn.
4. **Dừng hẳn thì làm cho đủ ba bước**: dừng bộ hẹn giờ ("scheduler" = bộ lập lịch tự động), lưu file trạng thái với trạng thái "đã nghỉ", rồi viết ghi chú sau kỳ ("post-mortem" = báo cáo rút kinh nghiệm sau sự cố).

**Kiểm tra**

Diễn tập kịch bản giữa lúc có sự cố: gõ lệnh dừng bộ hẹn giờ và xác nhận không có lần chạy nào mới bắt đầu sau đó, còn file trạng thái vẫn còn nguyên để mở lại được.

> **Tóm gọn 1 câu:** Giảm tốc khi sắp cạn nguồn lực, tạm dừng khi có nguy hiểm trước mắt, dừng hẳn khi loop không còn đáng tiền — ba mức, ba lý do khác nhau.

---

## Q5. Tôi thấy đường lên mức chạy tự do, có nên bỏ qua mấy bước đầu không? [→ §5. Upgrade Path]

Phần này giải thích lộ trình nâng cấp loop từng bậc và vì sao không được đi tắt. "Upgrade path" = lộ trình nâng mức tự chủ; "chạy tự do" (L3) = không cần người trông.

**Bạn sẽ thấy**

Bạn có một ý tưởng loop hay, muốn áp dụng ngay vào repo thật và cho chạy không cần ngồi canh. Sau một tuần bạn gặp đúng những sự cố mà bản thân bạn cũng đoán trước, và loop phải sửa lại từ đầu.

**Vì sao**

Lộ trình này là lộ trình **có kiểm chứng**: mỗi bậc chỉ lên được khi tầng dưới đã có bằng chứng hoạt động tốt trong thực tế. Đi tắt thì bạn đang tin vào một hệ thống chưa từng chạy ở mức đó trên dữ liệu thật.

**Làm gì**

1. **Chỉ báo cáo trước** — một đến hai tuần quét ổn định, không hành động; dùng khoảng này để đo tỉ lệ nhiễu.
2. **Rồi mới tự sửa lỗi nhỏ có kiểm chứng** — thêm thư mục riêng (worktree, bản sao tạm của repo) và giới hạn số lần thử.
3. **Rồi mới kết nối ra hệ thống ngoài** để pull request và phiếu công việc tự cập nhật.
4. **Cuối cùng mới chạy tự do**, và chỉ khi đã có danh sách cấm đường dẫn, ngân sách, số liệu và cổng người duyệt.

**Quy tắc phá vỡ điều này: với một kiểu loop mới trên repo chạy thật, không bao giờ bỏ qua mức chỉ-báo-cáo.**

```text
Chỉ báo cáo (L1) ─► 1–2 tuần quét ổn định
      ▼
Tự sửa nhỏ (L2) ─► có kiểm chứng + thư mục riêng + giới hạn lần thử
      ▼
Kết nối connector (L2+) ─► tự cập nhật PR / phiếu công việc
      ▼
Chạy tự do (L3) ─► chỉ khi đủ cấm đường dẫn, ngân sách, số liệu, cổng duyệt
```

Cách đọc sơ đồ: đi từ trên xuống, mỗi mũi tên là một bậc tự chủ; bên phải mỗi dòng là điều kiện bắt buộc trước khi lên bậc kế.

**Kiểm tra**

Ghi rõ trong hồ sơ loop mức hiện tại và vì sao bạn đủ điều kiện lên bậc sau. Lên L3 mà không có bốn bằng chứng bắt buộc thì tự động hạ về L2.

> **Tóm gọn 1 câu:** Nâng loop theo từng bậc L1→L3, mỗi bậc cần bằng chứng thực tế từ bậc dưới — với repo chạy thật thì đừng bao giờ bỏ qua bậc chỉ-báo-cáo.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: README.md.*
