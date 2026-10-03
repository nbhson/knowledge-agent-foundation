# ❓ FAQ — Loop hỏng thật (10 sai lầm + cách loop thực sự hỏng)

Nếu câu hỏi chưa rõ, đọc phần được nêu trong ngoặc vuông.

Từ viết tắt dùng trong file: **CI** = hệ thống chạy kiểm tra tự động khi bạn đẩy code; **verifier** = phần kiểm chứng kết quả (người hoặc agent khác); **state** = file lưu trạng thái giữa các lần chạy; **denylist** = danh sách file tuyệt đối không được đụng.

---

## Q1. Loop cứ sửa đi sửa lại cùng một lỗi, 5 lần chưa xong — dừng thế nào? [→ §2.1 Infinite Fix Loop + anti-pattern #2]

**Bạn sẽ thấy**

Cùng một yêu cầu gộp code (pull request) bị loop vá lại liên tục: lần 1 CI đỏ, lần 2 CI vẫn đỏ, lần 3 CI xanh nhưng một bộ test khác lại đỏ. Mỗi vòng lặp đẩy thêm một lượng lớn token vào tài khoản. Loop không bao giờ dừng, vì trong cấu hình không có chỗ nào buộc nó phải dừng. Mức độ thiệt hại: **S2 — có hại**, tức code sai có thể lọt vào nhánh chính.

**Vì sao**

Không có trần số lần thử (hard cap) nghĩa là câu "cứ thử tới khi CI xanh" không bao giờ thoát. Ba nguyên nhân gốc hay gặp: verifier quá yếu; verifier chạy cùng phiên với người viết nên nhìn mọi thứ đều ổn; và chẩn đoán sai nguyên nhân — loop đang chữa triệu chứng chứ không phải bệnh. Test chạy lúc được lúc không (flaky test) rất dễ bị nhầm thành lỗi mới.

**Làm gì**

1. Đặt trần cứng, ví dụ 3 lần thử. Lần thứ 3 vẫn đỏ thì dừng và chuyển việc.
2. Ghi số lần thử vào `STATE.md` ngay từ lần đầu, để loop tự biết mình đã tới đâu.
3. Tách verifier khỏi người viết: khác model hoặc khác mức cố gắng (effort), và đổi câu lệnh sang kiểu "tìm lý do để từ chối".
4. Test không ổn định phải được phân loại riêng, không đưa vào danh sách lỗi cần sửa.
5. Khi chuyển việc, đính kèm đủ bối cảnh: log CI, diff, số lần thử, đường dẫn file.

```
so_lan = state.read("attempt_count") + 1
state.write("attempt_count", so_lan)
if so_lan >= 3:
    escalate(section="High Priority (chờ người)", append_to="STATE.md")
    return
```

**Kiểm tra**

Đặt trần 3 rồi cố tình tạo một lỗi không sửa được. Xem loop có dừng đúng lần thứ 3 và có ghi vào mục "chờ người" trong `STATE.md` không. Trong `loop-run-log.md` phải thấy số lần thử tăng đều mỗi lần chạy.

---

## Q2. Cho chính agent đó viết code rồi tự duyệt, thậm chí tự gộp — có ổn không? [→ anti-pattern #1, #9 + §2.3 Verifier Theater]

**Bạn sẽ thấy**

Verifier báo "duyệt" trong khi CI vẫn đỏ, hoặc người review mở code ra thấy lỗi bảo mật mà loop vẫn tự gộp vào nhánh chính. Nguy hiểm nhất là loop được phép tự gộp: một lỗi bảo mật hoặc lỗi logic nghiệp vụ đi qua được vì verifier yếu. Mức độ: **S2**, và có thể lên **S3** (sự cố bảo mật, mất dữ liệu).

**Vì sao**

Đây là cái bẫy tự xác nhận: cùng một model, cùng bối cảnh, vừa viết vừa duyệt thì nó bảo vệ chính cách viết của mình. Câu lệnh kiểm chứng mơ hồ kiểu "nhìn có ổn không" cũng khiến nó gật đầu cho hết. Tệ hơn, có verifier không hề chạy test, chỉ đọc diff.

**Làm gì**

1. Tách verifier thành sub-agent hoặc model riêng, stance mặc định là TỪ CHỐI.
2. Buộc verifier chạy test và lint, rồi bắt nó trích ra dòng output thật — không nhận phán quyết suông.
3. Không bao giờ cho loop tự gộp khi chưa có danh sách đường dẫn được phép (allowlist) tường minh; đường dẫn nằm trong danh sách cấm (denylist) thì bắt buộc có người gộp tay.
4. Với việc chạy không cần người canh (unattended), dùng model mạnh hơn cho phần kiểm chứng.
5. Mỗi lần chạy phải ghi thêm vào `loop-run-log.md`, không chỉ có `STATE.md`.

```
verifier_prompt = "Tìm lý do để TỪ CHỐI bản diff này. Chạy test và lint,
                   trích dòng output thật. Không có output = không duyệt."
allow_auto_merge = paths ⊆ allowlist(trong gate.yaml)
```

**Kiểm tra**

Cố tình tạo một bản diff có lỗi rõ ràng và đưa cho verifier duyệt. Nếu nó vẫn duyệt thì verifier đang làm trò. Thử gộp file nằm trong denylist, phải bị chặn và báo cho người.

---

## Q3. Bot ping tôi mỗi 5 phút, cả team đã tắt bot — giờ làm sao? [→ §2.4 Notification Fatigue + anti-pattern #7]

**Bạn sẽ thấy**

Slack hoặc email nhận thông báo liên tục, tần suất khoảng 5 phút một lần. Sau một tuần team tắt im lặng bot. Hệ quả nặng hơn vẻ ngoài: những lần thật sự cần người quyết định cũng nằm trong đống thông báo bị bỏ qua. Mức độ đi từ **S1 (lãng phí thời gian, vô hại)** lên **S2 (mất cảnh báo thật)**.

**Vì sao**

Thông báo được gửi cho *mọi* lần chạy, thay vì chỉ cho *những phát hiện cần người quyết định*. Ngưỡng "mức cao" đặt quá thấp nên cả những việc nhỏ cũng leo lên đỉnh. Gốc rễ còn nằm ở chỗ không có nút tắt: loop chạy 24/7 mà không có tiêu chí dừng.

**Làm gì**

1. Chỉ báo khi cần quyết định của người: có thay đổi đề xuất, có lần thử hết trần, có việc nằm quá 24 giờ chưa ai xử lý.
2. Với loop chỉ báo cáo (report-only, mức L1), dùng chế độ tóm tắt theo ngày thay vì ping từng lần.
3. Siết lại luật xếp mức ưu tiên trong phần triage, không nâng hết lên "cao".
4. Ghi rõ điều kiện tạm dừng và dừng hẳn (pause/kill) vào file `LOOP.md`, kèm mẫu ngân sách.
5. Đo lại sau một tuần: bao nhiêu thông báo gửi, bao nhiêu được mở ra đọc.

**Kiểm tra**

Trong một tuần chạy thật, số thông báo phải giảm rõ và không có thông báo nào không hành động được. Mọi việc nằm trong mục "chờ người" quá 24 giờ đều phải sinh một cảnh báo.

---

## Q4. `STATE.md` toàn trỏ tới PR đã merge, ticket đã đóng — loop đang làm việc trên cái bóng? [→ §2.2 State Rot + §2.5 Token Burn]

**Bạn sẽ thấy**

File `STATE.md` liệt kê những yêu cầu gộp code đã được merge từ lâu, những ticket đã đóng, nhánh đã xoá. Loop đọc danh sách này rồi hành xử theo, đôi khi lại sửa file trên nhánh không còn tồn tại. Song song, hóa đơn token tăng vọt: loop vẫn chạy đầy đủ chuỗi sub-agent cho những việc rỗng. Mức độ: **S1** rồi tới **S2** khi loop hành động trên dữ liệu giả.

**Vì sao**

Không có bước dọn dẹp (prune) cuối mỗi lần chạy, và state không được đọc lại ở đầu lần chạy. Khi nhiều loop cùng ghi vào một file không có cấu trúc (schema), nội dung lẫn lộn và thêm rác. Phía chi phí: nhịp chạy dưới một phút với sub-agent nặng, không thoát sớm khi danh sách việc đã rỗng, và retry cả cả dây chuyền khi gặp lỗi mạng tạm thời.

**Làm gì**

1. Cuối mỗi lần chạy, xoá các mục đã merge hoặc đã đóng khỏi `STATE.md`.
2. Đầu mỗi lần chạy, kiểm tra `Last run` và kiểm tra lại các mã định danh còn sống không.
3. Tách state: mỗi pattern một file riêng, hoặc chia mục rõ ràng kèm luật dọn.
4. Chạy một lượt triage rẻ tiền trước; nếu danh sách rỗng thì dừng, không vào chuỗi agent đầy đủ.
5. Đặt ngân sách token theo ngày; vượt ngân sách thì tạm dừng loop, hết việc thì xoá lịch chạy.

**Kiểm tra**

Giả lập 3 mục đã đóng trong `STATE.md`, chạy loop một lần, xem chúng có biến mất không. Khi danh sách rỗng, log phải cho thấy lượt triage rẻ và không có lần gọi sub-agent nào.

---

## Q5. Loop tự refactor cả mấy module không liên quan, đụng cả file migration database — chặn thế nào? [→ §2.6 Over-Reach + anti-pattern #9]

**Bạn sẽ thấy**

Một việc nhỏ như sửa lỗi null check kéo theo diff 40 file: refactor cả module không liên quan, "sửa" vấn đề thiết kế, chạm vào file cấm. Đây là đường đi ngắn nhất từ lỗi nhỏ tới sự cố production. Mức độ: **S2**, leo thẳng lên **S3** nếu file bị đụng là migration, cấu hình hạ tầng hoặc khoá.

**Vì sao**

Kỹ năng "sửa nhỏ nhất" của agent quá dễ dãi; không có danh sách đường dẫn được phép và bị cấm; và phần triage xếp nhầm việc kiến trúc vào mức "ưu tiên cao". Khi phần triage sai, loop không có tầng kiểm tra phía sau để chặn.

**Làm gì**

1. Khai danh sách cấm trong chính kỹ năng (skill) chứ không để trong prompt yếu.
2. Áp nguyên tắc "diff nhỏ nhất có thể"; verifier kiểm tra lại danh sách file đã bị chạm.
3. Để triage chỉ được tín hiệu (báo cáo), không được tự động giao việc kiến trúc.
4. Không tự gộp cho bất kỳ file nào nằm trong danh sách cấm.
5. Nếu nhiều loop chạy song song, mỗi loop sửa trong một git worktree riêng và ghi khoá "PR #1234 — đang xử lý" vào state.

**Kiểm tra**

Một nhiệm vụ nhỏ mà không liên quan phải cho diff dưới 5 file. Chạm file trong danh sách cấm thì bị chặn và báo lên. Khi hai loop cùng một nhánh, phải thấy khoá worktree chứ không phải hai thay đổi chồng lên nhau.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: README.md.*