# 📊 04. Đo Lường Token Đã Tiết Kiệm — Savings

> RTK không chỉ nén output — nó còn **đo luôn** xem bạn tiết kiệm được bao nhiêu token. Đây là cầu nối sang module `11-evaluation` của harness: muốn biết harness chạy hiệu quả tới đâu thì phải có số liệu cụ thể.

> Phần này giải thích: có những lệnh đo nào, con số chúng báo nghĩa là gì, và cách đưa số liệu vào báo cáo.

**Giải thích nhanh các từ khóa**: token = đơn vị chữ mà model đọc/tính tiền. `rtk gain` = lệnh in báo cáo tiết kiệm. JSON = định dạng dữ liệu có cấu trúc, dashboard đọc được. Telemetry = cơ chế gửi số liệu đi đâu đó ngoài máy.

## Lệnh Đo Lường

Cách đọc bảng này: cột **Lệnh** là lệnh gõ vào terminal; cột **Mục đích** là nó cho bạn cái gì. Ví dụ dòng đầu: `rtk gain` in ra tổng quan số token đã bớt; dòng cuối `rtk session` cho biết agent có đang dùng RTK đều đặn hay không.

| Lệnh | Mục đích |
|------|----------|
| `rtk gain` | Tổng quan token đã tiết kiệm |
| `rtk gain --graph` | Biểu đồ ASCII 30 ngày gần nhất (vẽ bằng ký tự, xem ngay trong terminal) |
| `rtk gain --history` | Lịch sử commands gần đây |
| `rtk gain --daily` | Phân tích theo ngày |
| `rtk gain --all --format json` | JSON export cho dashboards (xuất dữ liệu cho dashboard đọc) |
| `rtk discover` | Tìm các lệnh chưa được tối ưu (cơ hội tiết kiệm còn bỏ sót) |
| `rtk discover --all --since 7` | Tất cả projects, 7 ngày qua |
| `rtk session` | Mức độ áp dụng RTK qua các sessions gần đây |

"0% reduction" = lệnh chạy qua RTK mà output không bị cắt tí nào.

> **Tóm gọn 1 câu:** `rtk gain` nhóm lệnh dùng để xem/xuất số liệu; `rtk discover` và `rtk session` nhóm lệnh dùng để tìm chỗ chưa tận dụng được RTK.

## Hiểu Đúng Con Số

Phần này giải thích số liệu RTK báo nói gì thật — tránh hiểu lầm "82% giảm output" thành "82% giảm tiền". (bash output reduction = mức cắt phần in ra từ lệnh shell; tokenizer = bộ đếm token thật của model.)

> ⚠️ **Quan trọng**: RTK đo **bash output reduction**, không phải giảm hóa đơn token toàn phần.

```
Bash output ──► Input tokens ──► Hóa đơn
     │               │               │
   Cắt 90%      (một phần của      (chỉ một phần
    ở đây         input, cùng         hóa đơn,
     ✅ ✅ ✅      prompt, system,   output cũng
                   history)           tính tiền)
```

Cách đọc sơ đồ: RTK cắt 90% ở khâu đầu (bash output). Nhưng hóa đơn gồm cả prompt hệ thống, lịch sử hội thoại và output của model — những phần RTK không đụng tới. Nên mức giảm ở khâu đầu bị pha loãng khi tính ra tiền.

- Token counts RTK báo cáo ước lượng `bytes / 4` — không có tokenizer; chia byte cho 4 chỉ là quy ước xấp xỉ.
- **Phần trăm giảm đáng tin cậy**, con số token tuyệt đối chỉ xấp xỉ.
- Mức giảm thực tế pha loãng qua từng tầng khi tính hóa đơn cuối.

> **Tóm gọn 1 câu:** Tin con số % giảm output, đừng tin con số token tuyệt đối, và đừng quy đổi thẳng ra % hóa đơn.

## Ví Dụ Báo Cáo

Phần này trỏ tới script chạy thật để bạn xem `rtk gain` in ra cái gì trước khi tự chạy.

> 📄 **Code ví dụ:** [`examples/01-vi-du-bao-cao.sh`](examples/01-vi-du-bao-cao.sh)

> 📄 **Code ví dụ:** [`examples/02-vi-du-bao-cao.sh`](examples/02-vi-du-bao-cao.sh)

> **Tóm gọn 1 câu:** Hai script ví dụ cho bạn thấy báo cáo thật trông thế nào — xem trước rồi mới đo trên repo của mình.

## Liên Kết Với Harness Evaluation

Phần này nối từng khái niệm đo lường của harness (module `11-evaluation`) với lệnh RTK tương ứng.

Cách đọc bảng này: cột **Harness `11-evaluation` concept** là điều harness muốn đo; cột **RTK tương ứng** là lệnh đáp ứng điều đó. Ví dụ dòng đầu: harness cần đo hiệu quả agent — `rtk gain` cung cấp con số token saved. ("Automated metrics" = số đo lấy tự động, không chạy tay; "adoption check" = kiểm tra agent có thực dùng RTK không.)

| Harness `11-evaluation` concept | RTK tương ứng |
|----------------------------------|---------------|
| Đo lường hiệu quả agent | `rtk gain` — token saved |
| Tìm cơ hội cải thiện | `rtk discover` — 0% reduction commands |
| Automated metrics | `rtk gain --all --format json` — feed dashboard |
| Continuous improvement | `rtk session` — adoption check |

> **Tóm gọn 1 câu:** Mỗi nguyên tắc đánh giá của harness đều có một lệnh RTK tương ứng — đo, tìm cơ hội, xuất số liệu, kiểm tra mức áp dụng.

## Benchmark Của RTK

Phần này cho bạn mốc so sánh: cùng một lệnh, chạy thường ra bao nhiêu dòng, chạy qua RTK ra bao nhiêu.

Cách đọc bảng này: cột **Command** là lệnh đo; cột **Output thô** là số dòng nếu chạy trực tiếp; cột **Output RTK** là số dòng khi chạy qua RTK; cột **Giảm** là % cắt bớt. Ví dụ dòng đầu: `ls -la` từ 45 dòng xuống 12 dòng — bớt ~73%. (`ls -la` = liệt kê file kèm quyền/dung lượng; `ruff check` = kiểm tra code Python, "Grouped" = gom lỗi theo loại; `docker ps` = liệt kê container đang chạy, "Essential only" = chỉ giữ cột cần thiết.)

| Command | Output thô | Output RTK | Giảm |
|---------|-----------|------------|------|
| `ls -la` | 45 lines | 12 lines | ~73% |
| `git push` | 15 lines | `ok main` | ~93% |
| `cargo test` (fail) | 200+ lines | ~20 lines | ~90% |
| `ruff check` | Nhiều dòng | Grouped | ~80% |
| `docker ps` | Nhiều cột | Essential only | ~70%+ |

> **Tóm gọn 1 câu:** Đây là các mốc tham chiếu — lệnh nào output càng dài và càng chạy nhiều lần thì nén càng có lãi.

## Lưu Ý Khi Đo Lường

Ba việc nên làm để số liệu đo được giữ đúng và an toàn:

- Thỉnh thoảng chạy `rtk gain` để theo dõi xu hướng (đúng tinh thần module `11-evaluation` — đo liên tục).
- `rtk discover` chỉ ra lệnh nào chưa được filter — đó là chỗ bạn còn bổ sung custom TOML filters được. (filter = bộ lọc cắt output; TOML = định dạng file cấu hình.)
- Telemetry mặc định **tắt** — RTK không gửi số liệu của bạn đi đâu nếu bạn không opt-in. (opt-in = tự mình bật.)

> **Tóm gọn 1 câu:** Đo định kỳ, bổ sung bộ lọc cho lệnh còn 0%, và yên tâm rằng số liệu của bạn không bị gửi đi đâu.

---

*Trở về [rtk/README.md](../)* · Trước: [03 — Patterns](../03-patterns/) · Tiếp theo: [05 — Troubleshooting](../05-troubleshooting/)
