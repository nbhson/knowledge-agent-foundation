# ❓ FAQ — Loop Engineering tổng quan (loop là gì, bắt đầu ở đâu, khác harness ra sao)

Nếu câu hỏi chưa rõ, đọc phần được nêu trong ngoặc vuông.

Từ viết tắt dùng trong file: **harness** = môi trường một agent chạy (công cụ, ngữ cảnh, quyền); **prompt** = câu lệnh bạn gõ; **CI** = hệ thống kiểm tra tự động khi đẩy code; **L1/L2/L3** = ba mức tự chủ của loop; **triage** = bước xếp hạng việc theo mức ưu tiên.

---

## Q1. "Loop" trong AI coding nghĩa là gì, khác gõ prompt thường ở chỗ nào? [→ Câu Chuyện Mở Đầu + Tổng Quan]

**Bạn sẽ thấy**

Bạn dành cả buổi sáng như sau: gõ prompt, chờ agent chạy xong, đọc kết quả, thấy chưa ổn, sửa prompt, gõ lại. Tới bữa trưa bạn đã hỏi cùng một câu "chỗ này sao lại lỗi null" ba lần. Agent cứ lặp lại cùng một kiểu sai lầm.

**Vì sao**

Hình dung việc thuê một đầu bếp mới: ngày đầu bạn nếm, nói "quá mặn"; hôm sau anh ta nấu lại, bạn nói "ít mặn hơn nhưng thiếu ngọt"; ngày thứ ba món gần hoàn hảo. Vấn đề không phải đầu bếp giỏi hay dở — mà là mỗi lần sửa đều cần **bạn đứng đó nếm thử**. Loop chính là cách để bạn chỉ viết một lần: "nếm, nếm lại, điều chỉnh", thay vì nếm thủ công từng bữa.

Điểm mấu chốt: loop không chỉ gọi agent, mà có **trạng thái nhớ được giữa các lần chạy**. Một cuộc hội thoại bị đóng lúc 5 giờ chiều, loop vẫn biết hôm qua nó đã thử gì, đã thất bại ở đâu, và lần này nên làm gì khác.

**Làm gì**

1. Nghĩ về loop như một dây chuyền sản xuất, không phải như một câu chat: lịch chạy, bước triage, lưu trạng thái, chỗ làm việc riêng, người viết, người kiểm, cổng duyệt của con người.
2. Mỗi lần chạy phải đọc trạng thái ở đầu và ghi lại ở cuối. Không ghi thì loop quên mọi thứ.
3. Viết quy tắc dừng trước khi viết phần tự động.
4. Đo bằng điểm sẵn sàng, không bằng cảm giác "chắc ổn".

```
prompt : bạn gõ từng lệnh, agent làm từng việc
harness: môi trường 1 agent chạy (công cụ, ngữ cảnh, quyền)
loop   : harness + lịch chạy + trạng thái + chuỗi kiểm chứng
```

**Kiểm tra**

Đóng hết phiên chat rồi chạy loop lần nữa: nó phải biết đã làm gì, không hỏi lại từ đầu.

---

## Q2. Loop khác harness khác chỗ nào — tôi đang xài harness, có cần thêm loop không? [→ Phân biệt quan trọng]

**Bạn sẽ thấy**

Bạn đã dựng xong một harness: agent có đủ công cụ, biết giới hạn quyền, chạy trong sandbox. Bạn tưởng đã xong. Nhưng khi bạn rời máy, không có gì chạy cả; agent không tự quay lại lúc 3 giờ sáng để xem có việc gì mới.

**Vì sao**

Harness trả lời câu hỏi "một agent chạy được những gì và được phép làm gì". Loop trả lời câu hỏi "ai chạy, chạy lúc nào, chạy lại lần nữa thì biết gì, và ai xác nhận là xong". Nói ngắn gọn:

| Bạn đã có | Bạn còn thiếu khi lên loop |
|---|---|
| Công cụ, quyền, sandbox | Lịch chạy định kỳ (cron, hẹn giờ CI) |
| Cấu hình một phiên | Trạng thái bền vững giữa các lần chạy |
| Agent giỏi một việc | Chuỗi kiểm chứng: người viết tách khỏi người duyệt |
| Bạn ngồi quyết định | Cổng duyệt của người ở đúng chỗ, ngân sách, nút dừng |

**Làm gì**

1. Nếu bạn vẫn phải ngồi gõ prompt mỗi sáng và muốn hệ thống tự phát hiện việc — bạn cần loop.
2. Nếu mục tiêu chỉ là một phiên làm việc sâu với nhiều công cụ, harness là đủ, chưa cần loop.
3. Xếp chồng, không thay thế: loop lấy harness làm nền rồi thêm lịch, trạng thái và chuỗi kiểm chứng bên trên.
4. Khi lên loop, phần khó nhất vẫn là harness — đừng làm vội cả hai cùng lúc.

**Kiểm tra**

Viết một câu: "Nếu tôi không ngồi trước máy, việc này có tự chạy không?" Trả lời không thì bạn đang dùng harness, chưa có loop.

---

## Q3. Có nên bật loop tự chạy 24/7 không, không cần ngồi canh? [→ Autonomy Levels + Case Studies]

**Bạn sẽ thấy**

Loop đã chạy được, bạn muốn bật lên mức cao nhất để nó tự lo hết. Đồng thời trong repo tham chiếu, các loop mức L2 đều để dừng: PR Babysitter ở trạng thái chỉ chạy tay, CI Sweeper chạy một phần, Dependency Sweeper chỉ nhận bản vá. Có cả một bài viết tên "Why We Killed CI Sweeper".

**Vì sao**

Ba mức tự chủ nâng dần: **L1 — chỉ báo cáo**, loop chạy và ghi kết quả, không đụng code; **L2 — có trợ giúp**, loop được phép sửa nhưng người vẫn phải duyệt; **L3 — không cần người canh**, tự quyết định và tự gộp. Nguyên nhân dừng ở L2 thường không phải vì L3 nguy hiểm về kỹ thuật, mà vì loop chạy sai hướng thì không ai nhận ra.

Dấu hiệu đáng lo nhất không nằm ở lỗi, mà ở hành vi: câu "cứ để loop lo" và bạn không còn ý kiến gì về tính đúng của code. Người viết vòng lặp phải vẫn là người kỹ sư.

**Làm gì**

1. Bắt đầu bằng L1 trong một tuần: loop chỉ báo cáo, bạn chỉ đánh giá độ chính xác của phần triage.
2. Chỉ lên L2 khi độ chính xác đã đo được và chấp nhận được.
3. L3 chỉ dành cho việc thật sự nhàm: có mẫu lệnh rõ, có danh sách cấm tuyệt đối, có log chạy.
4. Đặt tiêu chí dừng viết bằng chữ, không để bằng cảm giác.
5. Để hạn mức token theo ngày như một công tắc tự động cắt.

```
L1 Báo cáo ──► L2 Có người duyệt ──► L3 Không cần người canh
```

**Kiểm tra**

Sau một tuần ở L1, bạn phải trả lời được: loop xếp hạng sai bao nhiêu việc? Nếu không trả lời được, chưa được lên L2.

---

## Q4. Tôi mới bắt đầu, nên chọn loop nào và đi theo thứ tự nào? [→ Lộ Trình Học + Case Studies]

**Bạn sẽ thấy**

Có bảy pattern trong repo nhưng chọn cái nào trước thì bạn vẫn phân vân. Bạn sợ chọn phải thứ tốn hàng trăm giờ trước khi biết nó có chạy hay không.

**Vì sao**

Thứ tự học được chọn để rủi ro tăng dần: đọc tổng quan, nắm khái niệm, chọn một pattern, làm phần an toàn, làm phần vận hành, rồi mới mở rộng. Trong repo tham chiếu, ba loop đầu tiên đều ở mức L1 và tần suất rất thưa: triage hằng ngày chỉ trong ngày làm việc, soạn changelog một lần mỗi thứ Hai, cập nhật lịch sử sao mỗi ngày. Dependabot chạy mỗi tuần.

**Làm gì**

1. Chọn Daily Triage ở mức L1 làm loop đầu tiên — rẻ, chạy nhanh, cho kết quả nhìn thấy được.
2. Không vội tới phần sửa code; phần an toàn và phần vận hành phải xong trước khi đặt lịch thật.
3. Chỉ khi đã chạy ổn một loop thì mới mở rộng sang loop thứ hai.
4. Dùng công cụ CLI để dựng khung thay vì tự chép tay các file.
5. Bắt đầu bằng công cụ agent bạn đang dùng hằng ngày.

```
Bước 1  README tổng quan
Bước 2  01-concepts  — năm khối + mức L1-L3
Bước 3  02-patterns   — chọn Daily Triage L1
Bước 4  03-safety     — danh sách cấm, cổng duyệt người
Bước 5  04-operating  — ngân sách + log chạy
Bước 6  05 + 06       — nhiều loop, sai lầm thường gặp
Bước 7  07-tools      — dựng khung, chấm điểm
```

**Kiểm tra**

Sau hai tuần bạn phải trả lời được: loop chạy lúc mấy giờ, báo cáo gì, tốn bao nhiêu token, dừng bằng cách nào. Trả lời được cả bốn thì mới sang loop thứ hai.

---

## Q5. Tin bằng chứng nào rằng loop này đáng làm, không phải chỉ là thời thơm? [→ Tại Sao Loop Engineering Quan Trọng]

**Bạn sẽ thấy**

Bạn sắp đầu tư công sức thiết kế loop, và cần một lý do đứng vững hơn cảm giác. Nguồn tham chiếu đưa ra ba con số, chỉ khác nhau về nguồn.

**Vì sao**

Hai con số đo tác dụng: agent có vòng lặp phản hồi có cấu trúc giảm 52% lỗi lặp lại so với agent không có loop; vòng lặp tự cải thiện trong Claude Code tăng 38% chất lượng code trên bộ benchmark SWE-bench. Con số thứ ba không phải nghiên cứu, mà là bằng chứng thực tế từ chính repo: quy trình chấm điểm chạy trên mọi lần đẩy code và tăng lên 5.5 nghìn sao trong sáu tháng.

Điểm đáng chú ý nhất trong cả ba: hiệu quả đến từ **vòng lặp có cấu trúc**, không phải từ việc dùng model mạnh hơn. Và câu trả lời của người đã làm thật rất dứt khoát: họ không còn gõ prompt cho Claude nữa, các loop của họ gọi Claude và tự biết phải làm gì.

**Làm gì**

1. Đo trước và sau trên chính repo của bạn: số vòng lặp lại cùng một lỗi trong một tuần.
2. Theo dõi tỷ lệ việc triage sai — đây là con số quyết định có lên mức L2 hay không.
3. Ghi lại cả điểm lẫn chi phí cùng lúc; một điểm cao mà tiền vọt lên là dấu hiệu nguy.
4. Kéo dài thử nghiệm đủ lâu để có dữ liệu, không kết luận sau ba ngày.

**Kiểm tra**

Sau hai tuần, bạn phải có bảng so sánh trước/sau về số vòng lặp lại, số việc triage sai, và tổng token đã dùng.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: README.md.*