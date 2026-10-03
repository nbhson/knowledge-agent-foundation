# ❓ FAQ — RTK — Đo tiết kiệm (Câu hỏi thật, dễ hiểu)

Nếu câu hỏi chưa rõ, đọc phần được nêu trong ngoặc vuông ở `../README.md`.

---

## 04-savings/README.md

### Q13. `rtk gain` báo giảm 82% — vậy tôi có thật sự tiết kiệm 82% tiền không? [→ § Hiểu Đúng Con Số]

**Bạn sẽ thấy**

```
$ rtk gain
Commands run: 342
Raw bytes avoided: 1.2 MB
Estimated tokens saved: ~300k
Reduction: 82%
```

Nhìn dễ hiểu là hơn 80% chi phí đã bớt. Nhưng con số token ở đây là ước lượng theo `bytes / 4`, và RTK đo **giảm output của lệnh bash**, không phải giảm hóa đơn token.

**Vì sao**

Vì output của lệnh chỉ là một phần của token đầu vào. Phần còn lại là prompt hệ thống, lịch sử hội thoại, và chính output của model — RTK không đụng tới. Vì vậy mức giảm bị pha loãng qua từng tầng khi tính tới hóa đơn cuối cùng.

Chuỗi tính tiền đi thế này: output của lệnh bash bị cắt 82% ở khâu đầu → phần còn lại thành token đầu vào của model → nhưng token đầu vào đó vẫn phải chia sẻ chỗ với prompt và lịch sử → và output của model vẫn tính tiền như bình thường. Ba tầng sau không hề được RTK chạm vào.

**Làm gì**

1. Đọc `Reduction` như thước đo chất lượng nén — con số này đáng tin cậy.
2. Đọc `Estimated tokens saved` như ước lượng, vì nó không có tokenizer thật mà chia cho 4.
3. Đừng dùng `rtk gain` để cam kết giảm X% chi phí với sếp hoặc khách hàng.
4. Muốn con số gần với thực tế hơn, hãy đo cả hai đầu: so sánh hoá đơn tháng có và không có RTK.
5. Khi báo cáo nội bộ, ghi rõ "giảm output 82%" chứ đừng ghi "giảm token 82%".

```bash
rtk gain              # tổng quan
rtk gain --graph      # biểu đồ ASCII 30 ngày gần nhất
rtk gain --daily      # phân tích theo ngày
```

**Kiểm tra**

Chạy `rtk gain` hai lần cách nhau một ngày làm việc: `Commands run` phải tăng, `Reduction` phải nằm trong khoảng 70–90%. Nếu `Commands run` không đổi thì hook không chạy, và bạn đang đọc số liệu của một bộ đo rỗng.

---

### Q14. `rtk discover` nói có lệnh "0% reduction" — có nghĩa là RTK vô dụng không? [→ § Lệnh Đo Lường]

**Bạn sẽ thấy**

```
$ rtk discover
Found 5 commands with 0% reduction:
  - terraform plan      (12 calls)
  - kubectl apply       (8 calls)
  - ansible-playbook    (6 calls)
Consider `rtk init` for these or add custom TOML filters.
```

Có 5 lệnh bị nén 0% — nghĩa là chúng chạy ra y hệt bản gốc. Riêng `terraform plan` đã bị gọi 12 lần.

Danh sách này có thứ tự ưu tiên rất rõ: số lần gọi càng nhiều thì càng đáng để lấy công để nén. 12 lần `terraform plan` tiêu tốn nhiều hơn 6 lần `ansible-playbook`, dù hai lệnh đều đang ở 0%.

**Vì sao**

Vì RTK chỉ nén được những lệnh nó đã biết cách lọc. Lệnh chưa có bộ lọc thì đi qua nguyên vẹn — không phải RTK hỏng, mà là khoản tiết kiệm chưa được khai thác. Vì vậy `rtk discover` là danh sách việc cần làm, không phải bảng điểm.

Một lý do phụ cũng thường gặp: một số project có cấu hình riêng, và bộ lọc chỉ áp dụng cho project đã khai báo cấu hình đó. Lệnh chạy trong project mới sẽ không được lọc dù đúng lệnh đó.

**Làm gì**

1. Với lệnh cần output đầy đủ (như `terraform plan`), đừng nén — hãy thêm vào `exclude_commands` và công nhận là không tiết kiệm được ở lệnh đó.
2. Với lệnh chỉ cần giảm nhẹ, viết bộ lọc riêng trong TOML cấu hình.
3. Chạy `rtk discover --all --since 7` để xem cơ hội trong 7 ngày qua, không chỉ project hiện tại.
4. Dùng `rtk session` để xem mức độ áp dụng RTK qua các phiên gần đây — nếu tỉ lệ thấp, vấn đề nằm ở agent chưa dùng hook.
5. Nếu lệnh vẫn 0% sau khi thêm bộ lọc, kiểm tra lại phần cấu hình riêng cho project của bạn.

```bash
rtk discover
rtk discover --all --since 7
rtk session
```

**Kiểm tra**

Sau khi thêm bộ lọc mới, chạy lại `rtk discover` và xác nhận lệnh đó không còn nằm trong danh sách 0%. Nếu vẫn còn, hãy kiểm tra lệnh có nằm trong `exclude_commands` không.

---

### Q15. Tôi muốn đưa số liệu tiết kiệm lên dashboard của team — làm sao? [→ § Liên Kết Với Harness Evaluation]

**Bạn sẽ thấy**

Bạn có `rtk gain` nhưng số liệu nằm trong terminal, không lên được biểu đồ. Bạn cũng muốn xuất JSON cho hệ thống báo cáo, và muốn có số đo liên tục thay vì chạy tay mỗi tuần.

Bảng benchmark đi kèm trong tài liệu cũng cho bạn mốc so sánh nhanh: `ls -la` từ 45 dòng xuống 12 dòng (~73%), `git push` từ 15 dòng xuống `ok main` (~93%), `cargo test` khi fail từ hơn 200 dòng xuống khoảng 20 dòng (~90%), `ruff check` gom theo nhóm (~80%), `docker ps` chỉ giữ cột cần thiết (~70%+).

**Vì sao**

Vì đây là đúng vai trò của RTK trong bộ đánh giá của harness: biến "tôi tiết kiệm được bao nhiêu" thành số đo có thể theo dõi liên tục, thay vì cảm tính. Có số đo rồi thì mới biết một tuần đó tốn tiền vì lỗi cấu hình hay vì repo thật sự phình to.

**Làm gì**

1. Dùng `rtk gain --all --format json` để xuất JSON làm nguồn dữ liệu cho dashboard.
2. Dùng `rtk gain --history` để xem các lệnh gần đây kèm mức giảm — dùng để truy vết khi con số tổng giảm.
3. Dùng `rtk gain --graph` cho biểu đồ ASCII 30 ngày gần nhất, tiện nhắc trong status report.
4. Dùng `rtk gain --daily` khi cần xem ngày nào lệch chuẩn — thường là ngày bạn mới chạy lệnh nặng chưa có bộ lọc.
5. Chạy `rtk gain` định kỳ (mỗi ngày hoặc mỗi tuần) giống nguyên tắc đo lường liên tục.

```bash
rtk gain --all --format json > rtk-gain.json
rtk gain --graph
rtk gain --history
```

**Kiểm tra**

Mở file JSON xuất ra và kiểm tra có các trường tổng lệnh, số byte đã tránh, số token ước lượng và tỉ lệ giảm. Telemetry mặc định tắt, nên số liệu của bạn không đi đâu; nếu muốn chặn tuyệt đối thì đặt `RTK_TELEMETRY_DISABLED=1`.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: 04-savings/README.md.*
