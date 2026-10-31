# ❓ FAQ — RTK — Đo tiết kiệm (Câu hỏi thật, dễ hiểu)

Nếu câu hỏi chưa rõ, đọc phần được nêu trong ngoặc vuông ở `../README.md`.

---

## 04-savings/README.md

### Q13. `rtk gain` báo giảm 82% — vậy tôi có thật sự tiết kiệm 82% tiền không? [→ § Hiểu Đúng Con Số]

**Bạn sẽ thấy**

Chạy `rtk gain` — lệnh in báo cáo tiết kiệm — ra kết quả thế này:

```
$ rtk gain
Commands run: 342
Raw bytes avoided: 1.2 MB
Estimated tokens saved: ~300k
Reduction: 82%
```

Giải nghĩa từng dòng: `Commands run: 342` = đã có 342 lệnh chạy qua RTK. `Raw bytes avoided: 1.2 MB` = 1,2 MB output không phải in ra. `Estimated tokens saved: ~300k` = ước lượng 300.000 token được bớt. `Reduction: 82%` = output bị cắt 82%.

Nhìn dễ hiểu là hơn 80% chi phí đã bớt. Nhưng con số token ở đây là ước lượng theo `bytes / 4` — RTK chia số byte cho 4, không có tokenizer (bộ đếm token thật). Và RTK đo **giảm output của lệnh bash**, không phải giảm hóa đơn token.

**Vì sao**

Vì output của lệnh chỉ là một phần của token đầu vào. Phần còn lại là prompt hệ thống, lịch sử hội thoại, và chính output của model — RTK không đụng tới. Vì vậy mức giảm bị pha loãng qua từng tầng khi tính tới hóa đơn cuối cùng.

Chuỗi tính tiền đi thế này: output của lệnh bash bị cắt 82% ở khâu đầu → phần còn lại thành token đầu vào của model → nhưng token đầu vào đó vẫn phải chia sẻ chỗ với prompt và lịch sử → và output của model vẫn tính tiền như bình thường. Ba tầng sau không hề được RTK chạm vào.

**Làm gì**

1. Đọc `Reduction` như thước đo chất lượng nén — con số này đáng tin cậy.
2. Đọc `Estimated tokens saved` như ước lượng, vì nó không có tokenizer thật mà chia cho 4.
3. Đừng dùng `rtk gain` để cam kết giảm X% chi phí với sếp hoặc khách hàng.
4. Muốn con số gần với thực tế hơn, hãy đo cả hai đầu: so sánh hoá đơn tháng có và không có RTK.
5. Khi báo cáo nội bộ, ghi rõ "giảm output 82%" chứ đừng ghi "giảm token 82%".

> 📄 **Code ví dụ:** [`examples/01-q13-rtk-gain-bao-giam-82-vay-toi.sh`](examples/01-q13-rtk-gain-bao-giam-82-vay-toi.sh)

**Kiểm tra**

Chạy `rtk gain` hai lần cách nhau một ngày làm việc: `Commands run` phải tăng, `Reduction` phải nằm trong khoảng 70–90%. Nếu `Commands run` không đổi thì hook không chạy, và bạn đang đọc số liệu của một bộ đo rỗng.

> **Tóm gọn 1 câu:** 82% là mức cắt output của lệnh bash — đáng tin, nhưng hóa đơn cuối chỉ giảm ít hơn vì prompt, lịch sử và output của model không nằm trong phép đo.

---

### Q14. `rtk discover` nói có lệnh "0% reduction" — có nghĩa là RTK vô dụng không? [→ § Lệnh Đo Lường]

**Bạn sẽ thấy**

Chạy `rtk discover` — lệnh tìm các lệnh chưa được nén — ra kết quả thế này:

```
$ rtk discover
Found 5 commands with 0% reduction:
  - terraform plan      (12 calls)
  - kubectl apply       (8 calls)
  - ansible-playbook    (6 calls)
Consider `rtk init` for these or add custom TOML filters.
```

Giải nghĩa: "0% reduction" = lệnh này chạy qua RTK mà output không bị cắt tí nào. Số trong ngoặc = số lần đã gọi, ví dụ `terraform plan` đã bị gọi 12 lần. `TOML filters` = bộ lọc viết riêng bằng file cấu hình TOML. `rtk init` = lệnh cài hook tự động.

Có 5 lệnh bị nén 0% — nghĩa là chúng chạy ra y hệt bản gốc. Riêng `terraform plan` đã bị gọi 12 lần.

Danh sách này có thứ tự ưu tiên rất rõ: số lần gọi càng nhiều thì càng đáng để lấy công để nén. 12 lần `terraform plan` tiêu tốn nhiều hơn 6 lần `ansible-playbook`, dù hai lệnh đều đang ở 0%.

**Vì sao**

Vì RTK chỉ nén được những lệnh nó đã biết cách lọc. Lệnh chưa có bộ lọc thì đi qua nguyên vẹn — không phải RTK hỏng, mà là khoản tiết kiệm chưa được khai thác. Vì vậy `rtk discover` là danh sách việc cần làm, không phải bảng điểm.

Một lý do phụ cũng thường gặp: một số project có cấu hình riêng, và bộ lọc chỉ áp dụng cho project đã khai báo cấu hình đó. Lệnh chạy trong project mới sẽ không được lọc dù đúng lệnh đó.

**Làm gì**

1. Với lệnh cần output đầy đủ (như `terraform plan` — bản kế hoạch hạ tầng dùng để xem trước khi áp), đừng nén — hãy thêm vào `exclude_commands` (danh sách lệnh được miễn nén) và công nhận là không tiết kiệm được ở lệnh đó.
2. Với lệnh chỉ cần giảm nhẹ, viết bộ lọc riêng trong TOML cấu hình.
3. Chạy `rtk discover --all --since 7` để xem cơ hội trong 7 ngày qua, không chỉ project hiện tại.
4. Dùng `rtk session` để xem mức độ áp dụng RTK qua các phiên gần đây — nếu tỉ lệ thấp, vấn đề nằm ở agent chưa dùng hook.
5. Nếu lệnh vẫn 0% sau khi thêm bộ lọc, kiểm tra lại phần cấu hình riêng cho project của bạn.

> 📄 **Code ví dụ:** [`examples/02-q14-rtk-discover-noi-co-lenh-0-reduction.sh`](examples/02-q14-rtk-discover-noi-co-lenh-0-reduction.sh)

**Kiểm tra**

Sau khi thêm bộ lọc mới, chạy lại `rtk discover` và xác nhận lệnh đó không còn nằm trong danh sách 0%. Nếu vẫn còn, hãy kiểm tra lệnh có nằm trong `exclude_commands` không.

> **Tóm gọn 1 câu:** "0% reduction" không phải RTK hỏng — đó là danh sách lệnh chưa có bộ lọc, xếp theo số lần gọi để bạn biết chỗ nào khai thác tiếp trước.

---

### Q15. Tôi muốn đưa số liệu tiết kiệm lên dashboard của team — làm sao? [→ § Liên Kết Với Harness Evaluation]

**Bạn sẽ thấy**

Bạn có `rtk gain` nhưng số liệu nằm trong terminal, không lên được biểu đồ. Bạn cũng muốn xuất JSON (định dạng dữ liệu mà dashboard đọc được) cho hệ thống báo cáo, và muốn có số đo liên tục thay vì chạy tay mỗi tuần.

Bảng benchmark đi kèm trong tài liệu cũng cho bạn mốc so sánh nhanh — benchmark = số đo tham chiếu khi chạy cùng một lệnh: `ls -la` từ 45 dòng xuống 12 dòng (~73%), `git push` từ 15 dòng xuống `ok main` (~93%), `cargo test` khi fail từ hơn 200 dòng xuống khoảng 20 dòng (~90%), `ruff check` (lỗi kiểm tra code Python) gom theo nhóm (~80%), `docker ps` (danh sách container đang chạy) chỉ giữ cột cần thiết (~70%+).

**Vì sao**

Vì đây là đúng vai trò của RTK trong bộ đánh giá của harness: biến "tôi tiết kiệm được bao nhiêu" thành số đo có thể theo dõi liên tục, thay vì cảm tính. Có số đo rồi thì mới biết một tuần đó tốn tiền vì lỗi cấu hình hay vì repo thật sự phình to.

**Làm gì**

1. Dùng `rtk gain --all --format json` để xuất JSON làm nguồn dữ liệu cho dashboard.
2. Dùng `rtk gain --history` để xem các lệnh gần đây kèm mức giảm — dùng để truy vết khi con số tổng giảm.
3. Dùng `rtk gain --graph` cho biểu đồ ASCII 30 ngày gần nhất, tiện nhắc trong status report. (ASCII graph = biểu đồ vẽ bằng ký tự, xem được ngay trong terminal.)
4. Dùng `rtk gain --daily` khi cần xem ngày nào lệch chuẩn — thường là ngày bạn mới chạy lệnh nặng chưa có bộ lọc.
5. Chạy `rtk gain` định kỳ (mỗi ngày hoặc mỗi tuần) giống nguyên tắc đo lường liên tục.

> 📄 **Code ví dụ:** [`examples/03-q15-toi-muon-ua-so-lieu-tiet-kiem.sh`](examples/03-q15-toi-muon-ua-so-lieu-tiet-kiem.sh)

**Kiểm tra**

Mở file JSON xuất ra và kiểm tra có các trường tổng lệnh, số byte đã tránh, số token ước lượng và tỉ lệ giảm. Telemetry (chế độ gửi số liệu đi đâu đó) mặc định tắt, nên số liệu của bạn không đi đâu; nếu muốn chặn tuyệt đối thì đặt `RTK_TELEMETRY_DISABLED=1`.

> **Tóm gọn 1 câu:** Lấy dữ liệu từ `rtk gain --format json` đẩy lên dashboard, chạy định kỳ — có số đo liên tục thì mới phân biệt được "tốn tiền vì cấu hình sai" với "tốn tiền vì repo lớn thật".

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: 04-savings/README.md.*
