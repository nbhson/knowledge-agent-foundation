# ❓ FAQ — Lập kế hoạch & phân rã công việc (chuyện thật, dễ hiểu)

Nếu câu hỏi khó hiểu thì đọc `README.md` phần được nêu trong ngoặc vuông.

---

## Q1. Agent tôi cứ làm sai rồi làm lại y hệt, không tiến được — xử lý thế nào? [→ §14.2]

**Bạn sẽ thấy**

Sau ba lần thử y hệt, agent vẫn ra kết quả y hệt. Chi phí token đã cạn mà tình huống không
đổi. Trường hợp nặng hơn: nó dừng hẳn vì đã tốn quá 80% ngân sách và bị đóng băng.

**Vì sao**

"Thử lại" chỉ hợp lý với lỗi tạm thời — mất mạng, quá tải máy chủ, hết thời gian chờ. Còn
lỗi do cách chia việc sai thì phải chia lại, chứ thử lại chỉ tốn thêm tiền.

| Tín hiệu | Thử lại | Chia lại | Hỏi người |
|---|---|---|---|
| Lỗi tạm thời, dưới 3 lần | có | — | — |
| Cùng một việc hỏng 3 lần | — | có | — |
| Độ tin cậy kế hoạch dưới 0,4 | — | thêm việc hỏi lại | — |
| Hành động không hoàn tác được | — | — | có |
| Đã dùng hơn 80% ngân sách | — | — | có, kèm tóm tắt |

**Làm gì**

1. Phân loại mọi lỗi trước khi quyết định: tạm thời (nội dung lỗi chứa "timeout", "429",
   "econnreset") thì thử lại; còn lại thì chia lại.
2. Giới hạn cứng: tối đa 3 lần thử lại, tối đa 2 lần chia lại, sau đó bắt buộc chuyển sang
   hỏi người.
3. Mỗi lần chuyển hướng đều ghi log: số lần thử, loại lỗi, quyết định, và lý do.
4. Khi hỏi người, kèm theo tóm tắt những gì đã thử để họ ra quyết định, không phải đoán mò.

```python
if state.get("transient") and state.get("attempts", 0) < 3: return "retry"
if state.get("status") == "failed": return "replan"
if state.get("replans", 0) >= 2 or state.get("tokens", 0) > MAX_TOKENS * 0.8:
    return "escalate"
return "done"
```

**Kiểm tra**

Cài bộ kiểm thử với các lỗi giả lập: hết thời gian chờ phải ra "thử lại"; lỗi cú pháp phải
ra "chia lại"; vượt trần chi phí phải ra "hỏi người". Cả ba phải đúng, và không trường hợp
nào vòng lặp quá số lần cho phép.

---

## Q2. Nó tự xoá dữ liệu người dùng / deploy production mà không hỏi — có chặn được không? [→ §14.3]

**Bạn sẽ thấy**

Bạn chỉ yêu cầu "dọn tài liệu cũ", và agent tới bước xoá bản ghi khách hàng hoặc đẩy code
lên môi trường thật. Bước đó nằm đúng trong kế hoạch, nên không có gì để ngăn.

**Vì sao**

Quyền phải được gán **lúc lập kế hoạch**, dựa trên bán kính ảnh hưởng lấy từ chính sách
thật — chứ không phải đoán trong đầu kế hoạch rồi quyết định lúc chạy.

**Làm gì**

1. Gắn nhãn rủi ro ngay khi phân rã việc: `db.migrate`, `prod.deploy`, `user.delete`,
   `external.send` thuộc nhóm rủi ro cao hoặc không thể hoàn tác. Việc không có nhãn thì
   mức thấp và không bao giờ chặn.
2. Lấy danh sách tài nguyên bị chạm tới từ chính sách sandbox, không phải từ phỏng đoán.
3. **Người duyệt từ chối thì phải chia lại, không thử lại** cùng việc đó — thử lại sẽ lặp
   vô hạn. Ghi lại lý do từ chối.
4. Nếu không có phản hồi trong thời hạn thì coi như từ chối, và tuyệt đối không tự thông
   qua.
5. Ghi nhật ký duyệt: ai duyệt, lúc nào, mã băm của bản diff. Phần định nghĩa về hạn số
   giờ và luật hai-người thuộc module `15-approval-gates`.

```python
if risk in ("high", "irreversible") and not approved(plan, sub, inputs):
    return {"status": "blocked", "reason": "approval-denied"}  # → replan
# timeout không có phản hồi = deny, không phải approve
```

**Kiểm tra**

Gắn thử một việc loại `prod.deploy` và xác nhận nó bị chặn khi chưa duyệt, còn việc loại
`low` vẫn chạy bình thường. Chặn không được thì nhãn rủi ro đang bị gán sai chỗ.

---

## Q3. Chạy lại cùng một kế hoạch thì nó làm trùng việc đã làm — xử lý ra sao? [→ §14.4]

**Bạn sẽ thấy**

Agent treo giữa chừng, bạn chạy lại, và nó tạo thêm một bản ghi trùng với bản đã tạo
thành công lúc trước. Hoặc một nhánh hỏng làm cả nhiệm vụ bị báo thất bại, dù 6 việc
con đã xong.

**Vì sao**

Nếu mỗi việc con không có dấu vân tay ổn định thì lần chạy sau không biết lần trước đã làm
chưa. Và nếu trạng thái chỉ có "xong" hoặc "hỏng" thì mất một nhánh sẽ kéo sập cả những
nhánh không liên quan.

**Làm gì**

1. Khoá chống ghi trùng theo công thức `plan_id:subtask_id:hash(các đầu vào chuẩn hoá)`.
   Trước khi chạy, tra kho kết quả: có rồi thì trả lại kết quả cũ.
2. Mỗi việc có tác dụng phụ phải đăng ký một hàm hoàn tác, dùng khi huỷ giữa chừng.
3. Đánh dấu từng nút đồ thị công việc là xong, hỏng hoặc bỏ qua — không gộp thành trạng
   thái chung.
4. Khi một nút hỏng: tiếp tục các nhánh độc lập, bỏ qua những nút phụ thuộc vào nó, và trả
   về kèm cờ "hoàn thành một phần" cùng danh sách đã xong và đã hỏng.

```python
k = idem_key(plan, sub, inputs)
if k in store: return store[k]          # phát lại = không tác dụng phụ lần hai
out = fn(inputs); store[k] = {"status": "ok", "out": out}
```

**Kiểm tra**

Chạy cùng một việc con ba lần liên tiếp và đếm số bản ghi thực sự tạo ra — phải bằng 1.
Sau đó cố tình làm hỏng một nút giữa đồ thị và xác nhận các nút độc lập vẫn chạy.

---

## Q4. Kế hoạch nở ra như cây khổng lồ rồi cháy token — có trần không? [→ §14.5]

**Bạn sẽ thấy**

Cứ mỗi lần sửa code là agent sinh ra thêm 20 việc con, mỗi việc lại sinh 20 việc nữa.
Chạy được vài phút thì đã hết ngân sách token và hết giờ.

**Vì sao**

Phân rã không tự dừng. Nếu không đặt trần cứng, chi phí tăng theo cấp số nhân chứ không
phải tuyến tính — đây là loại sự cố làm cháy tài khoản nhanh nhất.

**Làm gì**

1. Trần cứng cho việc chia: độ sâu tối đa 4, mỗi nút mở rộng tối đa 5, tổng số việc con
   tối đa 25. Lệnh chia vượt độ sâu thì trả về nguyên bản việc đó, không cắt tiếp.
2. Với kỹ thuật dò nhánh (Tree of Thoughts): tối đa 3 nhánh, 9 lần mở rộng; nhánh điểm
   dưới 0,3 sau 2 bước thì cắt.
3. Trần toàn cục: 100 nghìn token cho một kế hoạch và 50 lượt gọi công cụ.
4. Ở mốc 80% thì cảnh báo; ở mốc 100% thì đóng băng và chuyển sang hỏi người, kèm tóm
   tắt kết quả tốt nhất tính được.

```python
MAX_DEPTH, MAX_FANOUT, MAX_TOKENS = 4, 5, 100_000
if state.get("tokens", 0) > MAX_TOKENS * 0.8: return "escalate"
```

**Kiểm tra**

Đưa một yêu cầu cố tình rộng ("làm lại toàn bộ hệ thống") vào và đo: số việc con, độ sâu
tối đa, tổng token, số lượt gọi công cụ. Cả bốn con số phải nằm dưới trần; vượt trần thì
phải thấy yêu cầu hỏi người thay vì chạy tiếp.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: `README.md`.*
