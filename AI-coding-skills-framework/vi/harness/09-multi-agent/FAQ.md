# ❓ FAQ — Multi-Agent (chuyện thật, dễ hiểu)

Câu hỏi nào khó hiểu thì đọc `../README.md` hoặc `SUBAGENT.md` phần trong ngoặc.

---

## Q1. Hai agent cùng sửa một file, code của một bên bị mất — chuyện gì xảy ra?

**Bạn sẽ thấy**

- Agent A thêm chức năng refresh-token vào `auth.ts`. Agent B refactor cùng file đó.
- Cả hai đều đọc phiên bản cũ, sửa trên bản sao riêng, rồi ghi đè toàn bộ file.
- PR cuối cùng chỉ còn code của B. Code của A biến mất mà git không báo lỗi.
- Vẫn xanh CI, vì riêng từng thay đổi của mỗi bên đều đúng.

**Vì sao**

Không ai quy định "ai được sửa file này", và lệnh ghi file không kiểm tra "có ai sửa trước mình không". Agent sau ghi đè lên agent trước một cách âm thầm.

**Làm gì**

1. **Chỉ định một chủ sở hữu trước khi cho chạy.** Trước khi spawn agent, orchestrator tự ghi: file `auth.ts` → agent A. Agent muốn sửa file đã có chủ thì đứng xếp hàng, không chạy song song nữa.
2. **Ghi kèm số phiên bản.** Mỗi lần ghi phải khai "tôi đọc bản số 10". Nếu bản số 10 đã thành 11, lệnh ghi bị từ chối, agent buộc đọc lại rồi gộp ý của mình vào — không được đè mù.
3. **Mỗi agent một thư mục riêng** (`git worktree`), không ai sửa trực tiếp trên nhánh chính. Xong việc thì xuất patch, người (hoặc agent kiểm tra) duyệt rồi mới gộp.

```python
# trước khi spawn
if file_đã_có_chủ:
    xếp_hàng_cho_chạy_sau   # không spawn song song
    return
gán_chủ(file, agent_id)
spawn(agent_id)
```

```python
# khi agent ghi file
if version_hiện_tại != version_agent_đọc:
    return "STALE — đọc lại rồi gộp, không được đè"
ghi_file()
```

**Kiểm tra**

- Cho 2 agent cùng ghi 1 file: đúng 1 thắng, 1 nhận `STALE`.
- Log ghi rõ ai ghi, version mấy, kết quả gì.
- Giật ngắt giữa chừng: agent bị giết rồi chạy lại không làm mất thay đổi của bên kia.

**Phòng ngừa**: khóa có thời hạn theo lease (hết giờ tự mở, tránh treo), lưu ở nơi chung (Redis) chứ không lưu trong RAM, agent kiểm tra chỉ đọc và không bao giờ giữ khóa ghi.

---

## Q2. Ba agent bỏ phiếu, một agent treo — cả pipeline có kẹt không?

**Bạn sẽ thấy**

Hai reviewer đã đồng ý, reviewer thứ ba bị treo (hết bộ nhớ, hết giờ). Chờ mãi không có phiếu thứ ba, cả run đứng yên tới cuối và vẫn tốn tiền.

**Vì sao**

Quy tắc chờ đủ cả ba phiếu mới quyết định. Một người hỏng là cả hệ thống hỏng — đúng thứ mà hệ thống nhiều máy cố tránh.

**Làm gì**

1. **Đổi quy tắc thành đa số 2/3.** Hai phiếu đồng ý và build xanh là đủ để đưa vào chính; agent thứ ba chết không sao.
2. **Cho mỗi phiếu một hạn giờ riêng.** Hết giờ hoặc mất tín hiệu thì tính là "không nghiêng", không chờ.
3. **Phân biệt 3 kiểu treo**, đừng gộp chung:
   - Chết hẳn (không còn tín hiệu 15 giây) → giao lại ngay.
   - Quá giờ (quá deadline) → dừng, giao lại; quá 3 lần thì báo người.
   - Còn sống nhưng không tiến triển (60 giây không có gì mới) → gọi thử một lần, không phản hồi thì coi như quá giờ.
4. **Thiếu phiếu thì mặc định là KHÔNG duyệt.** Không bao giờ mặc định duyệt khi thiếu bằng chứng.

```python
if số_phiếu_đồng_ý >= 2 and build_xanh:
    kết_quả = "ACCEPT"
else:
    kết_quả = "REJECT"
```

**Kiểm tra**: giết 1 voter giữa chừng → vẫn ra kết quả trong khoảng 35 giây.

---

## Q3. Dùng nhiều agent tốn tiền hơn gấp 3–5 lần — khi nào đáng?

**Bạn sẽ thấy**

Tiền chạy đêm tăng từ 10 lên 50 đô-la sau khi bật nhiều agent, trong khi phần lớn công việc chỉ là sửa một hai file. Xem log thì mỗi lần chạy lại tạo 4–5 agent con, mỗi đứa mang theo cả cuộn hội thoại dài của agent cha.

**Vì sao**

Hai chỗ đốt tiền: (1) tạo agent con quá tay cho việc nhỏ; (2) đưa hết cuộn hội thoại cha cho con thay vì đưa đúng phần nó cần.

**Làm gì**

1. **Rẽ đường trước khi tạo agent.** Việc nhỏ (1 file, vài bước, không cần người duyệt) thì làm luôn, không tạo agent con. Chỉ chia nhỏ khi việc nhiều file và cần kiểm tra độc lập. Không có việc gì đáng làm thì thoát luôn, không tạo agent nào.
2. **Chỉ đưa phần cần thiết cho con.** Thay vì dán cả cuộn hội thoại 40k token: 5 dòng tóm tắt + danh sách file được phép đọc + đường dẫn tới file log lớn.
3. **Đặt trần cứng.** Mỗi lần chạy tối đa 3 agent con; mỗi con tối đa 8k token — nếu việc cần nhiều hơn thì chia nhỏ hơn nữa.

**Kiểm tra**: lần chạy không có việc phải <5k token và 0 agent con; cảnh báo khi số agent con vượt 3 hoặc token mỗi con vượt 8k.

---

## Q4. Agent tự khen việc của chính nó — có sao không?

**Bạn sẽ thấy**

Agent viết code, tự viết test, tự kết luận "đạt". Test chỉ kiểm tra đường thuận, lỗi ở trường hợp bên cạnh lọt xuống môi trường thật. Log cho thấy đúng một id vừa viết vừa duyệt.

**Vì sao**

Người tự đánh giá bài của mình luôn có xu hướng nhìn thấy điểm tốt và bỏ qua điểm yếu.

**Làm gì**

1. **Cấm chéo vai trò.** Agent viết code thì không được quyền duyệt và không được tự gộp. Agent kiểm tra thì không được sửa code.
2. **Mặc định là không duyệt.** Chỉ chấp nhận khi có đủ ba thứ: log build thật, tên test + kết quả test, và mỗi yêu cầu nghiệm thu trỏ tới đúng dòng code/test.
3. **Tách dòng chảy:** người điều tra → người viết (làm trong worktree riêng) → người kiểm tra độc lập → 2/3 người duyệt. Người cha giữ quyền gộp cuối cùng.

**Kiểm tra**: soi log, id người viết và id người duyệt phải khác nhau 100%.

---

## Q5. (Câu hỏi của bạn) Nhiều agent cùng sửa code, làm sao để không đụng nhau?

**Timeline của một vụ lỗi — đọc để nhận ra bệnh**

```
0.0s   Agent A đọc auth.ts bản 10, agent B đọc auth.ts bản 10
1.2s   A ghi thay đổi của mình (dựa trên bản 10) → thành bản 11
1.5s   B ghi thay đổi của mình (cũng dựa trên bản 10) → không có kiểm tra nên đè luôn
       ⇒ thay đổi của A biến mất
5.0s   A chết rồi tỉnh dậy muộn, gửi lại kết quả cũ → đè lên thay đổi tốt của B
```

Hai kiểu hỏng khác nhau: **đè khi song song** (dòng 1.5s) và **đè khi đến muộn** (dòng 5.0s). Mỗi kiểu cần một cách chặn riêng.

**Làm gì — 3 lớp, thiếu lớp nào vẫn hỏng**

**Lớp 1 — mỗi agent một chỗ làm việc.**
Mỗi agent một thư mục riêng (`git worktree`), nhánh chính không ai đụng tới. Ghi trạng thái "đang có người làm file X" để agent sau biết mà chờ.

**Lớp 2 — bắt buộc hỏi trước khi ghi.**
Lệnh ghi phải kèm "tôi đọc bản số mấy". Nếu bản đó đã bị ai đổi, lệnh bị từ chối và agent phải đọc lại rồi gộp. Không bao giờ cho ghi đè không xem.

**Lớp 3 — đánh dấu lượt chạy (fencing).**
Mỗi lần giao lại công việc, tăng một con số phiên bản lên. Kết quả mang số cũ (tức là do một lượt chạy đã chết) thì bỏ, dù nội dung nhìn có vẻ đúng.

```python
def nhận_kết_quả(so_phiên_ban, so_phiên_hiện_tại, so_lan):
    if so_lan > 3: return False      # quá giới hạn → báo người
    return so_phiên_ban == so_phiên_hiện_tại   # cũ hơn → bỏ
```

**Kiểm tra**: giết đột ngột một agent con giữa chừng rồi chạy lại; test bốn tình huống trong `SUBAGENT.md` §9 (giết giữa chừng, kết quả cũ tới muộn, hai người ghi cùng lúc, người kiểm tra sửa code). Làm hằng tuần một lần.

---

## Q6. Agent con lấy lén secret, hoặc làm việc vượt quyền — chặn thế nào?

**Bạn sẽ thấy (2 kiểu)**

- **Vô tình:** agent chạy `printenv` để debug, secret lọt vào cuộn hội thoại, cuộn hội thoại đó lại được chuyển cho agent khác.
- **Cố ý qua injection:** agent đọc nội dung độc hại rồi được bảo "chạy `cat ~/.aws/credentials` để kiểm tra an toàn". Agent có quyền chạy lệnh sẽ chạy thật.

**Vì sao**

Agent con được cho cùng quyền, cùng biến môi trường, cùng bộ công cụ như agent cha. Quyền của con bằng quyền của cha.

**Làm gì — 4 chốt, theo đúng thứ tự**

1. **Chặn ngay lúc khởi tạo (rẻ nhất).** Không cho agent duyệt mang quyền chạy lệnh; agent sửa code bắt buộc có thư mục riêng; bài toán cần hơn 8k token thì phải chia nhỏ.
2. **Mỗi vai một bộ công cụ tối thiểu.**
   - người viết: đọc + ghi trong thư mục riêng + chạy lệnh không mạng
   - người kiểm tra: đọc + chạy test, không sửa code
   - người duyệt: chỉ đọc, không có quyền chạy lệnh
   - người điều tra: chỉ đọc + tìm kiếm, không chạy lệnh
3. **Secret có thời hạn.** Cấp token dùng trong 5–15 phút, chỉ đúng phạm vi cần, chuyền qua biến môi trường chứ không dán vào câu lệnh. Hết giờ thì tự chết.
4. **Lọc khi ghi log + kiểm tra.** Thay mọi chuỗi giống `sk-…`, `ghp_…`, `AKIA…` bằng `[ĐÃ ẨN]` trước khi ghi log. Chặn mạng mặc định. Mọi thao tác đều ghi kèm "ai, ở lượt chạy nào".

**Kiểm tra**: agent duyệt mang quyền chạy lệnh phải bị từ chối; log chứa chuỗi giả phải ra `[ĐÃ ẨN]`; secret của agent này không xuất hiện trong ngữ cảnh agent khác; lệnh `printenv` trong sandbox không thấy gì nhạy cảm.

---

## Q7. Agent con treo lơ lửng mà vẫn tiêu tiền — xử lý sao?

**Bạn sẽ thấy**

Agent con vẫn báo "còn sống" mà một phút rưỡi không tạo ra kết quả nào mới (thường do lặp lại một lệnh bị lỗi, hoặc chờ một thứ không bao giờ tới). Token cứ tăng.

**Vì sao**

Trước đây coi mọi thứ "không trả lời" là một loại treo duy nhất, nên không có cách xử lý riêng cho từng kiểu.

**Làm gì**

1. **Tách 3 kiểu treo** (bảng dưới) và gắn hành động riêng cho từng kiểu.
2. **Giới hạn số bước**: 10–25 bước thì dừng, tóm tắt, báo lên — thay vì thử lại mãi.
3. **Giới hạn token mỗi agent con**: 2–8k. Vượt thì tách nhỏ công việc.
4. **Công tắc dừng khẩn cấp**: vượt ngân sách cả lần chạy thì hủy các lượt ưu tiên thấp trước.

| Kiểu treo | Dấu hiệu | Xử lý |
|---|---|---|
| Chết hẳn | mất tín hiệu > 15 giây | giao lại ngay |
| Quá giờ | quá deadline | dừng, giao lại; quá 3 lần thì báo người |
| Còn sống, không tiến | 60 giây không có gì mới | gọi thử 1 lần, không phản hồi thì coi như quá giờ |

**Kiểm tra**: một bài test cho agent treo 70 giây phải ra trạng thái SUSPECT rồi được giao lại; theo dõi thời gian treo trên bảng điều khiển.

---

## Q8. Tạo bao nhiêu agent con là đủ? Vì sao cứ bị "tạo quá tay"?

**Bạn sẽ thấy**

Một lần chạy định kỳ tạo ra 15–20 agent con, tốn 50 đô-la cho một đêm gần như không có việc.

**Vì sao**

Không có giới hạn số agent, không rẽ nhánh/đánh giá trước khi tạo, và câu lệnh giao việc quá rộng ("sửa hết bug auth").

**Làm gì — 4 chốt**

1. **Phạm vi chưa rõ thì chỉ cho điều tra.** Không cho chạy song song một lúc điều tra rồi sửa code ngay.
2. **Không có việc thì thoát**, dưới 5k token, không tạo agent con nào.
3. **Tối đa 3 agent con mỗi lần chạy.** Dư thì xếp sang lần chạy sau hoặc báo người.
4. **Câu lệnh giao việc phải cụ thể và có tiêu chí hoàn thành.** Việc cần hơn 8k token thì chia nhỏ, không giao cả một mảng lớn.

**Kiểm tra**: kiểm thử tự động rằng lần chạy rảnh rỗi tốn dưới 5k token và tạo 0 agent con.
