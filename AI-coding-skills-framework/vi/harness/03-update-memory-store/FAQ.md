# ❓ FAQ — Ghi ngược và cập nhật kho bộ nhớ (chuyện thật, dễ hiểu)

Nếu câu hỏi khó hiểu thì đọc phần được nêu trong ngoặc vuông.

> **Cách đọc FAQ này:** mỗi câu trả lời có 4 khối — **Bạn sẽ thấy** (triệu chứng), **Vì sao** (gốc rễ), **Làm gì** (các bước), **Kiểm tra** (cách xác nhận đã hết bệnh).

---

## README.md

*(Bảy câu hỏi dưới đây lấy từ `README.md` của module "ghi ngược và cập nhật kho bộ nhớ" — module dạy agent cách ghi nhớ thông tin giữa các phiên làm việc.)*

## Q1. Mỗi phiên mới nó lại hỏi tôi đúng những gì đã nói — làm sao cho nó nhớ? [→ §1.1, §6.1]

> **Bối cảnh:** phiên = một lần mở chat làm việc với agent; muốn nó nhớ từ phiên trước thì cần một kho bộ nhớ bền.

**Bạn sẽ thấy**

Phiên thứ ba bạn lại giới thiệu lại nghề của mình và lại dặn "nhớ dùng tiếng Việt". Số liệu
trong tài liệu: chỉ riêng việc ghi nhớ đúng chỗ giảm 68% số câu hỏi lặp giữa các phiên, và
doanh nghiệp không có cơ chế này tốn 2,3 lần thời gian cho các việc lặp lại vì AI phải học
lại từ đầu.

**Vì sao**

Chỉ ghi lại thôi thì bộ nhớ phình và nhiễu; còn không ghi thì mọi phiên bắt đầu từ con số
0. Cần hai chiều: ghi đúng thứ đáng giữ, và ghi vào đúng chỗ để phiên sau đọc lại được.
Nhớ được mà đọc lại sai chỗ thì tệ hơn là không nhớ, vì model sẽ tin vào một ghi chú
đã lỗi thời.

**Làm gì**

1. Chia bộ nhớ thành ba tầng, mỗi tầng một độ sống: **phiên hiện tại** (thoáng qua,
   đóng chat là mất), **dự án** (bền, lưu ở tệp `CLAUDE.md` ở thư mục gốc — file
   ghi chú chung của cả dự án), **toàn cục** (dùng chung cả khi sang dự án khác).
2. Trong `CLAUDE.md` giữ đúng bốn mục: quy ước (luật viết code), kiến trúc (cấu trúc
   dự án), quyết định đã chốt kèm lý do, và những lối đã dính (lỗi đã từng gặp để đỡ dính lại).
3. Chỉ ghi lại thứ làm thay đổi trạng thái: thông tin người dùng, kiến thức mới phát hiện,
   hoặc phản hồi khi họ nói "câu trả lời trước sai rồi".
4. Mọi thao tác ghi đều đẩy một dòng vào nhật ký sự kiện, kèm thời điểm và dữ liệu đã sửa
   (nhật ký sự kiện = sổ ghi chép từng thay đổi, để lần sau truy vết được ai sửa gì lúc nào).

> 📄 **Code ví dụ:** [`examples/01-q1-moi-phien-moi-no-lai-hoi-toi.py`](examples/01-q1-moi-phien-moi-no-lai-hoi-toi.py)

**Kiểm tra**

Mở một phiên mới và hỏi lại ba thứ đã nói ở phiên cũ. Sau đó đo tỉ lệ câu hỏi lặp trước và
sau khi bật cơ chế này; mục tiêu là giảm rõ rệt chứ không phải giảm một chút.

> **Tóm gọn 1 câu:** Chia bộ nhớ thành 3 tầng (phiên/dự án/toàn cục), chỉ ghi cái thật sự đổi trạng thái vào `CLAUDE.md`, và đo tỉ lệ câu hỏi lặp để biết có hiệu quả hay không.

---

## Q2. Trong bộ nhớ tôi có cả "BHYT 4,5%" và "BHYT 5%", bot trả lời lúc này lúc kia? [→ §2.1, §12.3]

> **Bối cảnh:** BHYT = bảo hiểm y tế; đây là ví dụ về dữ liệu cũ mới trộn lẫn trong kho khiến bot trả lời thiếu nhất quán.

**Bạn sẽ thấy**

Trong kho có tới năm bản ghi về cùng một mức đóng, ba bản trùng nhau và một bản mới hơn
về mức đóng. Bot trả lời 4,5% ở câu này, 5% ở câu sau, và không giải thích vì sao.

**Vì sao**

Tích lũy dữ liệu không kiểm soát tạo ra nhiễu, không phải tín hiệu. Quy trình dọn (gộp bản
trùng, thay bản cũ bằng bản mới, xử lý bản mâu thuẫn) là phần bị bỏ qua nhiều nhất.

**Làm gì**

1. Chạy dọn theo nhịp, không chạy theo từng lần ghi: khi số ghi chưa gộp vượt 500, hoặc
   mỗi giờ một lần, hoặc khi tỉ lệ xung đột vượt 5%, hoặc khi có phản hồi tiêu cực về
   một sự thật. (Xung đột = hai bản ghi cùng nói về một việc nhưng giá trị khác nhau.)
2. Bên trong một lượt dọn: khử trùng trước (gộp nếu độ gần ≥ 0,9 — tức hai bản ghi
   giống nhau từ 90% trở lên thì coi là một), rồi phát hiện mâu
   thuẫn (cùng chủ thể + vị thu mà giá trị khác nhau).
3. Giải quyết theo thứ tự: mới hơn được chỉ thắng nếu độ tin cậy của nguồn mới **không thấp
   hơn** nguồn cũ; nếu không thì nguồn đáng tin hơn thắng; nếu vẫn không phân được thì hỏi
   người dùng.
4. Giữ lại **cả hai** phiên bản cùng quan hệ "thay thế" — không bao giờ ghi đè âm thầm
   (ghi đè âm thầm = xóa bản cũ mà không ai biết; giữ cả hai thì còn đường truy vết).

> 📄 **Code ví dụ:** [`examples/02-q2-trong-bo-nho-toi-co-ca-bhyt.ts`](examples/02-q2-trong-bo-nho-toi-co-ca-bhyt.ts)

**Kiểm tra**

Sau mỗi lượt dọn, đọc báo cáo: số bản đã gộp, số xung đột đã giải quyết, số bản đã xoá.
Trong báo cáo tổng hợp, chuỗi `merged/deleted/removed` (số bản đã gộp/đã xoá/đã bỏ) phải khác 0 sau vài tuần chạy; nếu
luôn bằng 0 thì cơ chế dọn chưa thật sự chạy.

> **Tóm gọn 1 câu:** Đừng dọn theo từng lần ghi — hẹn giờ dọn theo lô: gộp bản giống nhau, phát hiện bản mâu thuẫn, luôn giữ cả hai phiên bản thay vì xóa thầm.

---

## Q3. Ghi bộ nhớ chậm làm bot lag, có cách ghi sau rồi xả ngầm không? [→ §7.1, §12.5]

> **Bối cảnh:** lag = chậm; "ghi sau rồi xả ngầm" = trả lời người dùng ngay trước, ghi dữ liệu xuống kho trong nền sau đó.

**Bạn sẽ thấy**

Mỗi lần người dùng sửa một thông tin, bot phải chờ ghi xuống kho mới trả lời được. Lượng ghi
lớn thì độ trễ cộng dồn thành vấn đề người dùng nhận ra ngay: một đoạn hội thoại dài có thể
vài chục lần ghi, và chỉ một lần trong số đó là chậm cũng đủ để câu trả lời bị trễ.

**Vì sao**

Ghi đồng bộ đặt độ bền của kho trước mọi trải nghiệm người dùng. Có hai lựa chọn: chờ cho
xong, hoặc ghi tạm rồi xả nền.

**Làm gì**

1. Ghi vào bộ nhớ đệm trước, trả lời ngay; một luồng nền xả xuống kho theo lô (mặc định
   5 giây một lần hoặc 100 bản ghi một lô). (Bộ nhớ đệm = chỗ tạm trong RAM; xả = ghi hẳn xuống kho chính.)
2. Chấp nhận đánh đổi: nếu chương trình sập giữa chừng thì mất phần chưa xả. Muốn giữ
   được thì ghi tạm vào nhật ký trước khi báo "đã nhận".
3. Chỉ báo đã nhận sau khi ghi xong cả nhật ký lẫn kho chính; hàng đợi thử lại dùng khoá
   chống ghi trùng theo dạng `tenant:doc_hash` (khoá = nhãn duy nhất ghép tên khách + mã băm
   của tài liệu, giúp hệ thống nhận ra "ghi này rồi" để không ghi hai lần).
4. Đặt mục tiêu độ trễ ghi: trung vị dưới 80 mili giây (nửa số lần ghi nhanh hơn con số này),
   mốc 99% dưới 300 mili giây; việc
   gộp nặng đẩy ra ngoài đường chính.

> 📄 **Code ví dụ:** [`examples/03-q3-ghi-bo-nho-cham-lam-bot-lag.py`](examples/03-q3-ghi-bo-nho-cham-lam-bot-lag.py)

**Kiểm tra**

Đặt cảnh báo khi tỉ lệ lỗi ghi vượt 1% hoặc hàng đợi nghẽn quá 10 nghìn mục. Tắt đột ngột
chương trình giữa lúc đang xả để kiểm tra cơ chế thử lại có thực sự giữ được dữ liệu.

> **Tóm gọn 1 câu:** Trả lời người dùng ngay, ghi kho sau trong nền theo lô — và bù lại bằng nhật ký + hàng đợi thử lại để sập máy không mất dữ liệu.

---

## Q4. Khách yêu cầu xoá dữ liệu, tôi xoá trong DB nhưng kho vector vẫn còn — sạch hết thế nào? [→ §12.2, §12.6]

> **Bối cảnh:** kho vector = chỉ mục tìm kiếm theo ý nghĩa (embed dữ liệu thành các con số để tra cứu nhanh); xoá DB chính không tự xoá được chỉ mục này.

**Bạn sẽ thấy**

Bản ghi trong cơ sở dữ liệu chính đã mất, nhưng kết quả tìm kiếm vẫn trả về đoạn cũ, và bản
sao lưu vẫn giữ. Với yêu cầu bảo vệ dữ liệu cá nhân (GDPR), đây là vi phạm thật.

**Vì sao**

Dữ liệu nằm ở nhiều nơi khác nhau: kho chính, chỉ mục vector, đồ thị kiến thức, nhật ký
sự kiện, và bản sao lưu. Xoá một chỗ không phải xoá dữ liệu.

**Làm gì**

1. Đặt hạn sống theo từng lớp: phiên 24 giờ thì xoá; ký ức sự kiện 30–90 ngày thì lưu
   sang kho lạnh (kho lạnh = lưu trữ rẻ, hiếm khi tra); sự thật không đặt hạn nhưng phải có ngày hết hiệu lực và nguồn.
2. Dùng khoá phân vùng theo khách trên mọi bảng và mọi vùng chỉ mục, rồi chặn ở cả tầng
   ứng dụng lẫn tầng chính sách cơ sở dữ liệu (khoá phân vùng = mỗi khách dữ liệu ở ngăn
   riêng, xoá một khách không đụng khách khác).
3. Luồng xoá chuẩn: đánh dấu → xoá vector + đồ thị + nhật ký (đã tẩy) → dọn bản sao lưu
   trong 30 ngày → trả biên nhận xoá có mã, phạm vi và mốc thời gian. (Đánh dấu = tombstone,
   ghi "bản này đã chết"; tẩy/redact = xóa thông tin nhạy cảm nhưng giữ lại vỏ sự kiện.)
4. Cam kết thời gian xử lý 24 giờ, và quét lưu trữ lạnh trước khi xoá cứng
   (xoá cứng = xoá hẳn, không phục hồi được).

```text
DELETE /memory?user=X
  → tombstone → xoá vector + KG + log (redact)
  → vacuum backup ≤30d
  → {"deletion_receipt": {id, scope, ts}}
```

*(Đọc lệnh trên: yêu cầu xoá dữ liệu khách X → đánh dấu tombstone → xoá khỏi kho vector, đồ thị kiến thức (KG), nhật ký (chỉ xóa phần nhạy cảm) → dọn bản sao lưu trong vòng 30 ngày → trả về "biên nhận xoá" gồm mã, phạm vi, thời điểm.)*

**Kiểm tra**

Chạy một truy vấn mẫu sau khi xoá, cả ở kho chính lẫn kho vector: phải không còn kết quả nào.
Mỗi đêm chạy truy vấn thăm dòng liên khách; phát hiện trả về dữ liệu khác là sự cố bảo
mật, không phải lỗi nhỏ.

> **Tóm gọn 1 câu:** Xoá dữ liệu một khách là xoá ở *tất cả* nơi nó nằm (DB, vector, đồ thị, log, backup) trong 24 giờ, và phải trả lại biên nhận xoá làm bằng chứng.

---

## trajectory-fork-replay.md

*(Ba câu hỏi dưới đây lấy từ tài liệu "truy vết phiên làm việc, rẽ nhánh và chạy lại" — dạy cách tua lại, thử nhánh khác, và phục hồi sau sự cố.)*

## Q5. Agent sai ở bước 15, tôi muốn thử lại từ bước 12 mà không mất cả phiên? [→ §4.1, §4.2]

> **Bối cảnh:** fork = tách nhánh — tạo một bản sao đường đi từ bước 12 trở đi, giữ nguyên phần trước.

**Bạn sẽ thấy**

Cách duy nhất bạn có là xoá hết phiên và làm lại từ đầu, mất thời gian và mất phần đã làm
đúng. Bạn không biết sai ở bước nào vì nhật ký chỉ lưu lời thoại, không lưu các bước ẩn.

**Vì sao**

Hệ thống lưu như một danh sách tin nhắn phẳng thì không có điểm móc. Muốn rẽ nhánh hay tua
lại, bạn cần một dòng sự kiện chỉ ghi thêm, không sửa (append-only), với số thứ tự liên
tục không lỗ hổng.

**Làm gì**

1. Ghi mọi hành động thành sự kiện có mã định danh, mốc thời gian và số thứ tự: nhập yêu
   cầu, bơm ngữ cảnh, suy luận, gọi công cụ, kết quả, mốc dừng. (Sự kiện = một dòng trong
   sổ ghi chép; bơm ngữ cảnh = chèn thông tin nền vào trước khi model trả lời.)
2. Khi muốn thử nhánh khác: phát lại tới sự kiện đích rồi tạo phiên con, dùng chung
   phần tiền tố (tiền tố = các sự kiện từ đầu tới bước 12, dùng chung thay vì chép lại).
3. Ghi việc rẽ nhánh thành một sự kiện `checkpoint` có trường `forkedFrom: {atSeq, by}`
   (checkpoint = điểm cắm cờ; `forkedFrom` = ghi rõ "nhánh này rẽ ra từ số thứ tự nào, do ai"),
   chứ không phải một bản sao ngầm.
4. **Đăng ký phần tiền tố vào kho trước khi ghi thêm sự kiện** — ghi trước sẽ tạo số thứ
   tự 0 trùng với sự kiện đầu tiên vừa sao chép, đúng thứ mà hàm phát hiện sự kiện mồ côi
   sẽ bắt. (Sự kiện mồ côi = sự kiện không nối được vào dòng thời gian, như người không chứng minh được nguồn gốc.)

> 📄 **Code ví dụ:** [`examples/04-q5-agent-sai-o-buoc-15-toi-muon.ts`](examples/04-q5-agent-sai-o-buoc-15-toi-muon.ts)

**Kiểm tra**

Sau khi rẽ nhánh, chạy phát hiện sự kiện mồ côi trên cả phiên gốc lẫn phiên mới: danh
sách số thứ tự phải liên tục từ 0, không thiếu và không lặp.

> **Tóm gọn 1 câu:** Ghi phiên thành chuỗi sự kiện có số thứ tự thì mới fork được — rẽ nhánh từ sự kiện đích, dùng chung tiền tố, và đăng ký tiền tố vào kho trước khi ghi sự kiện mới.

---

## Q6. Phát lại (replay) có chạy lại lệnh xoá file không? [→ §4.1, §3]

> **Bối cảnh:** replay = chạy lại một phiên cũ để xem chuyện gì đã xảy ra; câu hỏi là liệu nó có làm *thật* những việc nguy hiểm như xóa file.

**Bạn sẽ thấy**

Bạn muốn xem lại phiên hôm qua để tìm lý do sai. Nhưng nếu phát lại chạy thật mọi lệnh
từng chạy thì bạn đang xem lại một lần phá hủy thứ hai — xoá file, deploy, gửi email.

**Vì sao**

Có hai kiểu phát lại: phát lại xác định (tái dựng từ kết quả đã ghi, không gọi lại model
hay chạy lại lệnh) và phát lại trực tiếp (giữ lịch sử công cụ nhưng gọi lại model thế hệ
mới để so sánh). Chọn nhầm là tai nạn.

**Làm gì**

1. Mặc định là phát lại xác định: một lời gọi công cụ có dấu vân tay (fingerprint = mã
   băm nhận dạng gồm tên lệnh + tham số + môi trường) khớp với
   kết quả đã ghi thì tái dùng kết quả đã ghi, không thực thi lại.
2. Mọi bước có tác dụng phụ (side effect = hành động làm thay đổi thế giới bên ngoài,
   ví dụ xóa file, gửi email, deploy) phải được bảo vệ bằng khoá chống ghi trùng từ
   `07-workflow` §13.3, kể cả khi bạn cố ý chạy lại.
3. Muốn so sánh model mới với model cũ thì dùng phát lại trực tiếp, và chỉ cho phép trên
   các bước không gây tác dụng phụ.
4. Nếu kết quả phát lại lệch với bản ghi, hãy ghi cả hai lại — dấu vân tay phải bao gồm
   cấu hình môi trường và tham số, không chỉ tên lệnh.

```text
tool_call có fingerprint == kết quả đã ghi  →  dùng lại kết quả đã ghi
tool_call lệch                                →  ghi cả hai, không sửa bản gốc
bước có side effect                           →  bắt buộc có idempotency key
```

*(Đọc khối trên: lệnh gọi trùng dấu vân tay với kết quả cũ thì dùng lại kết quả cũ; lệch thì ghi thêm mà không sửa bản gốc; bước nào làm thay đổi bên ngoài thì bắt buộc có idempotency key — nhãn chống chạy-hai-lần.)*

**Kiểm tra**

Chọn một phiên có ít nhất một bước xoá file, chạy phát lại trong môi trường cào (môi trường
giả lập, không đụng dữ liệu thật), và xác
nhận không có tệp nào bị xoá cũng như không có lời gọi mạng nào đi ra.

> **Tóm gọn 1 câu:** Replay mặc định chỉ "chiếu phim lại" từ kết quả đã ghi — không chạy thật lệnh nào, và bước có side effect bắt buộc phải có idempotency key.

---

## Q7. Máy chết giữa chừng rồi chạy lại, tôi sợ nó làm trùng việc đã xong? [→ §4.3, §5, §7]

> **Bối cảnh:** đây là bài toán resume — tiếp tục phiên từ chỗ bị rớt mà không làm lại việc đã xong.

**Bạn sẽ thấy**

Sau khi khởi động lại, agent bắt đầu lại từ một mốc không rõ, hoặc thực hiện lại một thao tác
đã thành công trước đó. Nguyên nhân phổ biến nhất: lưu kết quả công cụ nhưng không lưu
cấu hình và tham số, nên lịch sử không tái hiện được.

**Vì sao**

Trạng thái được phục hồi bằng cách phát lại chuỗi sự kiện. Nếu một sự kiện ghi mất, hoặc
thứ tự sự kiện có lỗ hổng, thì bộ dựng trạng thái sẽ bỏ sót hoặc làm lặp.

**Làm gì**

1. Trạng thái phiên phải nằm trên đĩa hoặc cơ sở dữ liệu, không nằm trong bộ nhớ
   (bộ nhớ RAM mất ngay khi tắt máy; đĩa/DB thì giữ được).
2. Khi tiếp tục, nạp mốc dừng cuối cùng, đọc các sự kiện ghi sau thời điểm treo, rồi suy
   ra tập bước đã hoàn thành để bỏ qua.
3. Bỏ qua chỉ an toàn khi có khoá chống ghi trùng (idempotency key); mỗi bước hoàn thành phải được ghi nhận.
4. Ghi mốc dừng sau mỗi cột mốc quan trọng (xong pha lập kế hoạch, xong pha tái cấu trúc)
   để dễ rẽ nhánh.
5. Không để sự kiện nào thiếu `actor` (ai/thứ gì làm ra sự kiện đó) hoặc thiếu mã nhiệm vụ cha — thiếu là mồ côi, không
   ai truy vết nổi.

> 📄 **Code ví dụ:** [`examples/05-q7-may-chet-giua-chung-roi-chay-lai.ts`](examples/05-q7-may-chet-giua-chung-roi-chay-lai.ts)

**Kiểm tra**

Giết cứng tiến trình giữa lúc đang chạy rồi khởi động lại. Chạy phát hiện sự kiện mồ côi:
danh sách phải rỗng. Xác nhận các thao tác đã thành công trước đó không chạy lại lần nữa.

> **Tóm gọn 1 câu:** Ghi trạng thái xuống đĩa liên tục và mỗi bước hoàn thành có dấu nhớ — thì chết máy giữa chừng cũng resume được mà không làm trùng việc gì.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: `README.md`, `trajectory-fork-replay.md`.*
