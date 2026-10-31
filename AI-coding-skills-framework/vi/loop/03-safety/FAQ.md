# ❓ FAQ — Safety & Loop Design Checklist (những câu người thật hay hỏi)

Câu hỏi nào khó hiểu thì đọc phần trong ngoặc vuông — nó trỏ tới mục tương ứng trong README an toàn.

---

## Q1. Loop của tôi tự mở file `.env` và file chứa khoá rồi sửa — chặn ở đâu cho chắc? [→ §2.1. Path Denylist]

Phần này giải thích cách chặn loop đụng vào file nhạy cảm (chứa mật khẩu, khoá API). `.env` = file chứa biến môi trường, thường có mật khẩu và khoá.

**Bạn sẽ thấy**

Một lần chạy, loop tự sửa `.env` đổi địa chỉ database, có lần lại đụng tới thư mục `auth/` (đăng nhập) và `k8s/production/` (hạ tầng chạy thật). Diff lên pull request thấy dòng khoá bị thay bằng giá trị rỗng. "Diff" = tập thay đổi. Không có lỗi nào được ghi ra — với loop, đó chỉ là "sửa file bình thường".

**Vì sao**

Danh sách cấm chỉ nằm trong hướng dẫn bằng lời thì chỉ là lời khuyên, model có thể quên hoặc làm sai. Muốn chắc thì phải **cưỡng chế bằng máy**: đọc danh sách cấm từ một file cấu hình riêng mà loop không tự ý sửa được. Đây gọi là denylist ("danh sách đen" = danh sách file tuyệt đối không được đụng).

**Làm gì**

1. **Liệt kê đường dẫn cấm** trong file cấu hình: biến môi trường, thư mục khoá và thông tin đăng nhập, hạ tầng, thanh toán, và thư mục di chuyển cơ sở dữ liệu ("migrations" = các file đổi cấu trúc database).
2. **Ghi luôn vào skill sửa code** một câu chỉ thị không được đụng vào các tệp khớp mẫu ("khớp mẫu" = tên file khớp với pattern như `*.env*`), phải báo người kèm ngữ cảnh.
3. **Cho công cụ kiểm tra bắt buộc** trước mọi lần gộp. Lệnh này trả về mã thoát `2` ("exit code" = con số chương trình trả về khi kết thúc, `2` ở đây nghĩa là "chặn lại, cần người") và `0` nghĩa là đi tiếp.
4. **Chỉ mở ngoại lệ khi có lý do rõ ràng**, ví dụ một loop riêng chỉ lo di chuyển cơ sở dữ liệu mới được phép chạm `migrations`.

```text
.env, .env.*, **/secrets/**, **/credentials/**, **/*_key*, **/*_secret*
.terraform/**, k8s/production/**, **/migrations/**, auth/**, payments/**, billing/**
```

Cách đọc danh sách trên: mỗi phần tử là một "pattern" (mẫu tên). `**/secrets/**` = thư mục nào có tên `secrets` ở bất kỳ đâu; `*_key*` = file nào có chữ "key" trong tên.

> 📄 **Code ví dụ:** [`examples/01-q1-loop-cua-toi-tu-mo-file-env.sh`](examples/01-q1-loop-cua-toi-tu-mo-file-env.sh)

**Kiểm tra**

Đưa một tệp trong danh sách cấm vào tập các tệp đã đổi và chạy lệnh trên: phải ra mã thoát `2`. Sau đó xác nhận lệnh đọc danh sách cấm từ file cấu hình — không phải từ việc "loop đã đọc hướng dẫn chưa", vì lời chỉ dẫn trong prompt là thứ model có thể quên.

> **Tóm gọn 1 câu:** Danh sách file cấm phải nằm trong file cấu hình và được lệnh kiểm tra cưỡng chế bằng máy — đừng trông chờ model tự nhớ.

---

## Q2. Tôi muốn cho loop tự gộp pull request, làm vậy có an toàn không? [→ §2.2. Auto-Merge Policy]

Phần này giải thích có nên để loop tự bấm "merge" (gộp code vào nhánh chính) hay không. Pull request (PR) = đề nghị gộp code.

**Bạn sẽ thấy**

Bạn bật tự gộp cho một loop dọn nhẹ. Trong vòng ba ngày nó gộp luôn một thay đổi hành vi ("thay đổi hành vi" = code làm app chạy khác trước), một lần nâng cấp thư viện, và một thay đổi file khoá hạ tầng — không cần bạn xem, không có ai bình duyệt.

**Vì sao**

Mặc định phải là **không tự gộp**. Chỉ khi có một danh sách cho phép được ghi rõ bằng chữ thì thao tác gộp mới được xem là ngoại lệ. Danh sách đó gọi là allowlist ("danh sách trắng" = chỉ những thứ liệt kê mới được làm) — nó là chính sách quyền gộp, nên phải nằm trong kho mã, có người review, và được máy kiểm tra trước mỗi lần gộp.

**Làm gì**

1. **Để mặc định từ chối**: không có danh sách cho phép thì không gộp gì cả.
2. **Chỉ cho phép thay đổi vô hại**: sửa lỗi chính tả trong comment và tài liệu, sắp xếp thứ tự câu lệnh import ("import" = dòng khai báo dùng thư viện ở đầu file), tự sửa lỗi kiểm tra định dạng chỉ trong tệp kiểm thử.
3. **Cấm tuyệt đối**: đổi hành vi, nâng phiên bản thư viện, thay đổi file khoá phiên bản ("lockfile" = file ghi "đóng băng" đúng phiên bản các thư viện để mọi máy cài giống nhau), và mọi đường dẫn nằm trong danh sách cấm.
4. **Ghi danh sách cho phép vào một tệp riêng** cạnh hướng dẫn dự án, để ai cũng thấy và cũng chỉnh được.

| Được gộp tự động | Không bao giờ gộp tự động |
|---|---|
| Lỗi chính tả trong comment, tài liệu | Thay đổi hành vi sản phẩm |
| Sắp xếp thứ tự import | Nâng phiên bản thư viện phụ thuộc |
| Cấu hình nằm trong thư mục tài liệu được cho phép | Thay đổi file khoá phiên bản |

Cách đọc bảng: cột trái = loại thay đổi an toàn đến mức máy tự gộp được; cột phải = loại thay đổi lúc nào cũng phải có người duyệt, vì sai một dòng là hỏng app hoặc hỏng hạ tầng.

**Kiểm tra**

Bật tự gộp ở chế độ mặc định: lệnh kiểm tra cổng ("gate" = cổng duyệt bắt buộc trước khi đi tiếp) phải chặn một pull request chỉ sửa lỗi chính tả, vì nó không có trong danh sách cho phép. Chỉ khi đường dẫn nằm trong danh sách thì mới qua được.

> **Tóm gọn 1 câu:** Mặc định cấm tự gộp; chỉ những thay đổi vô hại nằm trong allowlist ghi rõ mới được gộp, và máy phải kiểm tra trước mỗi lần gộp.

---

## Q3. Hết ngân sách token rồi agent có tự nâng hạn mức lên không? [→ §2.4. Human Gates]

Phần này giải thích cách giữ trần chi phí. "Token" = đơn vị tính dữ liệu vào/ra của mô hình, tức là đơn vị tính tiền. "Ngân sách" = số token tối đa được tiêu trong ngày.

**Bạn sẽ thấy**

Hết ngân sách giữa lúc loop đang chạy, bạn thấy nó báo cáo rồi tự tăng hạn mức lên gấp đôi và chạy tiếp. Hoặc tệ hơn: bạn mở file ngân sách ra thấy con số đã bị sửa mà không ai sửa.

**Vì sao**

Nếu agent tự nâng trần, thì trần đó không còn là giới hạn nữa. Hạn mức chỉ có tác dụng khi **người** là người nới. Agent chỉ được phép *xin*, không được phép *tự lấy* — đây là một "human gate" (cổng người duyệt = điểm bắt buộc người bấm duyệt trước khi đi tiếp).

**Làm gì**

1. **Ghi trần vào một file ngân sách riêng** kèm dòng "vượt thì dừng toàn bộ bộ hẹn giờ và báo người".
2. **Cấm quyền tự nâng**: chỉ người review mới sửa được con số đó.
3. **Cho agent một kênh xin thêm**: một skill riêng chỉ gửi đề nghị, nêu rõ đã dùng bao nhiêu và việc gì đang dở.
4. **Chuẩn bị sẵn các trường hợp phải dừng chờ người**: an toàn, đăng nhập, thanh toán, dữ liệu cá nhân ("PII" = thông tin nhận diện cá nhân như địa chỉ, số CMND), hạ tầng chạy thật, nâng thư viện, thay đổi quá 10 tệp, và lần thứ ba thất bại trên cùng một việc.

```markdown
## Ngân sách loop — Dự án X
- Tối đa token/ngày: 2M
- Vượt thì: dừng bộ hẹn giờ, báo người
- Tối đa số sub-agent mỗi lần chạy: 3
```

Cách đọc ví dụ: "2M" = 2 triệu token mỗi ngày; "sub-agent" = agent con do loop triệu gọi, mỗi cái là một vòng gọi mô hình tốn tiền riêng.

**Kiểm tra**

Chạy một loop có ngân sách thấp cho tới khi vượt trần: nó phải dừng lại, ghi vào state (file trạng thái), và **file ngân sách phải không đổi một byte** ("một byte" = nhấn mạnh: không một ký tự nào bị sửa). Sau đó kiểm tra có một đề nghị tăng ngân sách được ghi lại đúng phạm vi và cần người bấm duyệt.

> **Tóm gọn 1 câu:** Trần ngân sách chỉ là giới hạn thật khi agent không tự sửa được nó — agent chỉ xin, người mới nới.

---

## Q4. Bot của loop nên có quyền gì trên GitHub, Slack, database? [→ §2.3. MCP Connector Least Privilege]

Phần này giải thích cách cấp quyền cho bot của loop. "Connector" = điểm nối ra hệ thống ngoài (GitHub, Slack, database). "MCP" = giao thức chuẩn để agent gọi các hệ thống ngoài.

**Bạn sẽ thấy**

Token của bot nằm trong cấu hình loop và nó có quyền rộng hơn nhiều so với việc loop thực sự làm. "Token" ở đây = chuỗi khoá xác thực dùng để gọi API. Loop chỉ cần đọc trạng thái hợp đồng, nhưng token vẫn gộp được, xoá được, và đăng vào mọi kênh.

**Vì sao**

Connector là điểm nối ra hệ thống bên ngoài. Nguyên tắc ở đây là **đặc quyền tối thiểu** ("least privilege" = cấp đúng ít quyền nhất đủ để làm việc, không hơn): mỗi connector chỉ nhận đúng phần đọc và ghi cần thiết, trên một danh tính riêng — không dùng chung tài khoản cá nhân của bạn.

**Làm gì**

1. **Chia quyền theo từng connector**, đọc và ghi tách riêng.
2. **Dùng tài khoản bot riêng, token riêng, phạm vi tối thiểu** — không dùng token của bạn, vì token bạn thường có quyền quá lớn.
3. **Khoá database**: loop không được ghi vào database chạy thật — ghi nhầm là mất dữ liệu người dùng thật.
4. **Khoá kênh chat**: chỉ được đăng vào đúng một kênh dành riêng cho việc leo thang ("escalation" = đẩy việc khẩn lên cho người).
5. **Ghi rõ bot là ai** trên mọi bình luận pull request, để người đọc phân biệt được người với máy.

| Connector | Được đọc | Được ghi |
|---|---|---|
| GitHub | Vấn đề, pull request, trạng thái kiểm tra | Bình luận, nhãn; không gộp mặc định |
| Linear | Vấn đề của nhóm | Bình luận, trạng thái; không xoá |
| Slack | Lịch sử kênh | Chỉ đăng vào kênh `#loop-escalations` |
| Database | Không | Không ghi vào chạy thật |

Cách đọc bảng: mỗi dòng là một hệ thống bot nối vào; cột "Được đọc"/"Được ghi" = quyền tối đa bot được có. Ví dụ dòng GitHub: bot đọc được issue và PR, chỉ được comment và gắn nhãn — không được gộp code.

**Kiểm tra**

Liệt kê những gì bot làm được bằng token hiện tại: nếu có một hành động trong danh sách không được phép mà bot vẫn làm được, thì phạm vi token đang rộng hơn chính sách — phải thu hẹp lại.

> **Tóm gọn 1 câu:** Mỗi connector dùng token riêng với quyền tối thiểu — loop chỉ được đọc/ghi đúng phần việc của nó, trên tài khoản bot, không phải tài khoản của bạn.

---

## Q5. Tôi có 5 cái loop, làm sao biết cái nào đã an toàn để chạy không cần ngồi canh? [→ §1. Loop Design Checklist]

Phần này giải thích cách chấm điểm loop để quyết định mức tự chủ. "Chạy không cần ngồi canh" = chạy tự động mà không có người nhìn từng lượt (mức L3).

**Bạn sẽ thấy**

Bạn chấm điểm 10 phần kiểm tra nhưng không biết điểm bao nhiêu thì được chạy tự do. Rồi bạn phát hiện cả 5 loop đang ghi chung một file trạng thái ("state" = file lưu trí nhớ giữa các lần chạy), và loop kiểm chứng lại là chính session đã viết code — tức là agent vừa viết vừa tự duyệt, không có người thứ hai kiểm.

**Vì sao**

Vòng lặp phân bố 10 phần thành bốn mức sẵn sàng (L0→L3). Nếu một loop thiếu phần kiểm chứng thì nó chưa đủ tư cách chạy không người trông coi — chấm điểm phải thành thật, không nâng điểm cho dễ nhìn.

**Làm gì**

1. **Chấm theo 10 phần**: mục đích và phạm vi, lịch chạy, skill, tách người viết–người kiểm, state, bàn giao cho người, connector, chi phí và giới hạn, quan sát được, an toàn.
2. **Nhớ dấu hiệu phải dừng ngay**, không cần chấm điểm cũng biết là chưa an toàn (liệt kê ở dưới).
3. **Bắt buộc cho mức cao nhất**: có danh sách cấm đường dẫn, tự gộp tắt hoặc giới hạn chặt, phạm vi connector đã review, cổng người duyệt và nút dừng khẩn ("kill switch" = nút tắt ngay mọi loop) đều được viết ra.

| Mức sẵn sàng | Mô tả | Cần có phần nào |
|---|---|---|
| L0 — Bản nháp | Mới chỉ có ý định | Phần 1 |
| L1 — Báo cáo | Quét rồi ghi state, không tự hành động | Phần 1–3, 5 |
| L2 — Có hỗ trợ | Tự sửa lỗi nhỏ, có người kiểm | Phần 1–7 |
| L3 — Không cần trông coi | Chạy tự do | Tất cả |

Cách đọc bảng: "Mức sẵn sàng" = bậc tự chủ của loop, càng lên cao càng cần nhiều phần checklist đạt. Ví dụ L1 nghĩa là loop chỉ quét và ghi kết quả, mọi hành động đều chờ người.

**Dấu hiệu phải dừng**: cùng một pull request đã hơn 3 lần tự sửa mà không tiến triển; agent kiểm chứng lại là cùng một phiên với người viết; không có file trạng thái nên mỗi lần chạy đều mất trí nhớ; thông báo spam mọi lần chạy dù không có gì; tự gộp bật mà không có danh sách cho phép.

**Kiểm tra**

Chấm điểm từng loop theo 10 phần và ghi kết quả cạnh tên loop. Bất kỳ loop nào dính một trong năm dấu hiệu phải dừng thì giữ ở mức thấp hơn, kể cả khi tổng điểm trông cao.

> **Tóm gọn 1 câu:** Chấm điểm loop thành thật theo 10 phần checklist, xếp vào mức L0–L3 tương ứng — mức càng cao cần càng nhiều bằng chứng an toàn, và có dấu hiệu đỏ thì hạ mức.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: README.md.*
