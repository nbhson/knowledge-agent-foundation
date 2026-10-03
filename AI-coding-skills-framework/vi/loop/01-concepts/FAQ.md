# ❓ FAQ — Loop Engineering (những câu người thật hay hỏi)

Câu hỏi nào khó hiểu thì đọc phần trong ngoặc vuông.

---

## Q1. Sáng nào cũng phải gõ prompt cho agent, có cách nào cho nó tự chạy không? [→ §1. Loop Engineering Là Gì?]

**Bạn sẽ thấy**

Bạn ngồi gõ "vào repo, đọc log CI đỏ, sửa đi", đợi ba phút, đọc kết quả, gõ tiếp "giờ chạy test lại". Ngày mai làm lại từ đầu — không nhớ hôm qua đã thử phương án nào, không có lịch sử, không có ai kiểm xem lần sửa đó có thật sự đúng không. Cuối tuần bạn kiệt vì bạn là nút thắt của mọi việc.

**Vì sao**

Cách dùng phổ biến gọi là gõ từng lệnh một: bạn là người điều phối, agent chỉ là công cụ gọi một lần rồi ngồi chờ. Loop Engineering đảo ngược lại — hệ thống tự phát hiện việc cần làm, tự phân công, tự kiểm chứng, tự nhớ trạng thái. Nó giống thiết kế dây chuyền nhà máy hơn là thợ thủ công làm từng món.

**Làm gì**

1. **Viết mục tiêu trong đúng một câu**: loop này hoàn thành điều gì?
2. **Chọn nhịp chạy**: ví dụ `/loop 1d "quét CI đỏ, báo cáo"`. Không có nhịp thì bạn chỉ có một lần chạy đơn lẻ, không phải loop.
3. **Chỗ nhớ bền**: một file `STATE.md` trong repo, đọc ở đầu mỗi lần chạy, ghi kết quả ở cuối.
4. **Tách người viết và người kiểm**: agent này viết code, agent kia chạy test rồi mới cho đi tiếp.
5. **Chừa cổng cho người**: việc rủi ro cao thì dừng lại chờ bạn quyết.

```text
GÕ TAY:      Bạn ─prompt► Agent ─kết quả► Bạn ─prompt► Agent ...
LOOP:  Scheduler ─► Triage ─► đọc/ghi STATE ─► Worktree cô lập
       ─► Implementer ─► Verifier ─► cổng người duyệt ─► Commit
```

**Kiểm tra**

Đợi qua hai chu kỳ nhịp chạy mà bạn không phải gõ thêm lệnh nào. Mở `STATE.md` phải trả lời được ba câu: đang làm gì, lần trước thử gì và ra sao, cái gì đang chờ người.

---

## Q2. Loop chạy xong báo "không làm gì", tôi tưởng nó treo — thật ra sao? [→ §3.1 Vòng Đời Một Run]

**Bạn sẽ thấy**

Mở log thấy một lần chạy kết thúc sau 8 giây, không có dòng lỗi nào, `actions_taken: 0`, `tokens_estimate: 5000`. Nhưng hóa ra mỗi lần chạy vẫn dựng lại đủ bộ sub-agent nên vẫn bị trừ tiền. Tệ hơn: trong `STATE.md` có ba mục đã xử lý xong từ tuần trước vẫn nằm đó, nên loop cứ thấy "có việc" rồi lại làm lại việc cũ.

**Vì sao**

Một lần chạy đi qua nhiều trạng thái, và `IdleNoop` (không có gì để làm) là một nhánh bình thường chứ không phải lỗi. Vấn đề nằm chỗ khác: nếu vòng quét được viết kiểu "chạy hết bộ phận rồi mới kết luận không có việc" thì lần nào cũng tốn hàng chục nghìn token, và nếu không dọn state thì danh sách phình ra và loop tưởng mình bị bỏ quên.

**Làm gì**

1. Thêm nhánh thoát sớm: quét xong thấy danh sách rỗng là dừng ngay, dưới 5.000 token.
2. Mỗi run phải **dọn** mục đã xong hoặc đã đóng khỏi state, không dọn thì state phình mãi.
3. Ghi rõ trạng thái kết thúc vào log, phân biệt "không có việc" với "có việc nhưng hết ngân sách".
4. Chỉ lập worktree khi state báo có việc cụ thể, không lập trước cho có.

```text
Scheduled → LoadingContext → RunningTriage → WorkingInWorktree → Verifying
  LoadingContext → BlockedBudget    (hết token)
  RunningTriage → IdleNoop          (không có gì để làm)
  Verifying → AwaitingHumanGate → Applied / Rejected
  (mọi trạng thái cuối) → Logged
```

**Kiểm tra**

Đặt watchlist rỗng rồi chạy một nhịp: log phải ghi `IdleNoop`, `tokens_estimate` dưới 5.000, và không còn thư mục worktree nào bị bỏ lại trong repo.

---

## Q3. Tôi có nên cho loop tự sửa code không cần ngồi canh ngay từ đầu không? [→ §4. Mức Tự Chủ L1 → L3]

**Bạn sẽ thấy**

Bạn nghe nói "L3 là chạy không cần người" nên bật luôn cho một loop mới. Ngày thứ ba, nó tự sửa file cấu hình đăng nhập, tự merge, hỏng prod lúc 2h sáng, và bạn không biết nó đã quyết gì.

**Vì sao**

Ba mức tự chủ không phải cấp bậc khen thưởng, mà là **giấy phép an toàn** theo mức độ tin cậy bạn đã tích lũy được. Bỏ qua mức đầu để nhảy thẳng lên mức cuối là cách nhanh nhất để loop phá production trước khi bạn kịp hiểu nó.

**Làm gì**

1. **Tuần đầu chỉ báo cáo** (L1): quét rồi ghi ra danh sách, tuyệt đối không tự sửa gì.
2. **Khi điểm chấm điểm ổn và bạn đồng ý** thì lên L2: cho tự sửa lỗi nhỏ, nhưng bắt buộc có agent kiểm và làm trong thư mục riêng.
3. **Chỉ khi đã có danh sách cấm đường dẫn, ngân sách, và cổng người duyệt** mới lên L3.
4. **Có đường lui**: sự cố hoặc chi phí tăng vọt thì hạ một bậc, không cần viết lại từ đầu.

| Mức | Loop làm gì | Bộ phần cần có |
|---|---|---|
| L0 | Chỉ ghi lại ý định | Mục tiêu, phạm vi |
| L1 | Quét rồi ghi state, không tự hành động | Lịch chạy, triage skill, state |
| L2 | Tự sửa lỗi nhỏ, có người kiểm | Worktree, verifier, giới hạn lần thử |
| L3 | Chạy không cần người nhìn | Tất cả, cộng cấm đường dẫn, ngân sách, cổng duyệt |

**Quy tắc vàng**: đừng bao giờ nhảy thẳng lên L3 cho một kiểu loop mới trên repo production.

**Kiểm tra**

Trước khi lên L3, phải trả lời được: điểm chấm điểm L2 đã tốt bao lâu, có cơ chế dừng khẩn được ghi ở đâu, và có file nào trong repo mà loop tuyệt đối không được chạm vào không.

---

## Q4. "Cấm thử vô hạn" — đặt ở tầng nào mới đúng? [→ §5. Loop Taxonomy]

**Bạn sẽ thấy**

Agent bị kẹt: cùng một lỗi test, thử lại 47 lần, mỗi lần đều lỗi y hệt. Nhưng ngược lại, có lần nó bỏ cuộc sau một lần thử khi lỗi chỉ là mạng chậm.

**Vì sao**

Một loop lớn chứa các vòng lặp nhỏ hơn ở năm tầng tốc độ khác nhau, nằm lồng trong nhau như lớp hành tây. Đặt guardrail sai tầng là không có tác dụng: cấm retry vô hạn là việc của tầng thực thi tính bằng giây, không phải của tầng ngoài tính bằng ngày.

**Làm gì**

1. **Tầng trong cùng** (mili-giây): suy nghĩ → hành động → quan sát → rút kinh nghiệm. Quá nhanh để can thiệp, không cần rào chắn.
2. **Tầng thực thi** (giây): xử lý lỗi tức thời — thử lại có chờ dần, cắt cầu dao khi lỗi lặp, đặt trần cứng số lần thử rồi **báo người**.
3. **Tầng kiểm chứng**: viết → test → sửa → test lại, do một agent khác đảm nhiệm.
4. **Tầng phản hồi**: sau mỗi run ghi lại chỗ sai, chỗ lặp, một điều chỉnh cho lần sau.
5. **Tầng ngoài** (ngày/tuần): cải thiện cả hệ thống, đo loop có đang tốt lên không.

**Kiểm tra**

Mô phỏng một lỗi không bao giờ hết: loop phải dừng sau đúng số lần thử đã đặt trần, ghi lý do vào state, rồi báo người — không phải cứ thử tiếp.

---

## Q5. Loop cứ đoán sai phong cách code, sửa xong lại bị nó sửa ngược — làm sao? [→ §6.1 Intent Debt]

**Bạn sẽ thấy**

Loop thêm comment theo kiểu của dự án khác, đổi tên biến theo kiểu mới, viết hàm dài 300 dòng. Bạn sửa tay xong, lần sau nó lại làm y hệt. Đây là kiểu phờn chán ai cũng gặp: mỗi lần chạy nó bắt đầu từ trang trắng.

**Vì sao**

Model không có trí nhớ dài hạn qua các lần gọi. Phần ý định của dự án bị bỏ trống thì được lấp bằng những phỏng đoán tự tin — mà phỏng đoán thì hay sai. Khoản nợ đó gọi là **nợ ý định**.

**Làm gì**

1. **Ghi quy ước vào một skill** (thường là file `SKILL.md` cùng script và tài liệu tham chiếu): cách đặt tên, lệnh build/test/lint, tiêu chuẩn review.
2. **Ghi cả những thứ không làm**: "chúng tôi không làm theo cách X vì sự cố Y".
3. **Skill là bộ nhớ ý định** — viết một lần, đọc mọi lần chạy. Thiếu nó thì loop tự suy ra mọi thứ từ đầu ở mỗi lần chạy.
4. **Đo lại** bằng cách xem còn bao nhiêu việc phải sửa tay sau mỗi lần chạy.

```text
Skills = "Quy ước viết một lần, đọc mọi lần chạy"
```

**Kiểm tra**

Giao một việc mà quy ước đã viết rõ trong skill (ví dụ quy tắc đặt tên test file). Nếu loop vẫn viết sai, thì skill chưa đủ cụ thể hoặc chưa được nạp vào ngữ cảnh lúc chạy.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: README.md.*