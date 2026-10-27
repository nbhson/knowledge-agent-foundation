# 📊 04. Đo Lường Token Đã Tiết Kiệm — Savings

> RTK không chỉ nén output — nó còn **đo luôn** xem bạn tiết kiệm được bao nhiêu token. Đây là cầu nối sang module `11-evaluation` của harness: muốn biết harness chạy hiệu quả tới đâu thì phải có số liệu cụ thể.

## Lệnh Đo Lường

| Lệnh | Mục đích |
|------|----------|
| `rtk gain` | Tổng quan token đã tiết kiệm |
| `rtk gain --graph` | Biểu đồ ASCII 30 ngày gần nhất |
| `rtk gain --history` | Lịch sử commands gần đây |
| `rtk gain --daily` | Phân tích theo ngày |
| `rtk gain --all --format json` | JSON export cho dashboards |
| `rtk discover` | Tìm các lệnh chưa được tối ưu (cơ hội tiết kiệm còn bỏ sót) |
| `rtk discover --all --since 7` | Tất cả projects, 7 ngày qua |
| `rtk session` | Mức độ áp dụng RTK qua các sessions gần đây |

## Hiểu Đúng Con Số

> ⚠️ **Quan trọng**: RTK đo **bash output reduction**, không phải giảm hóa đơn token toàn phần.

```
Bash output ──► Input tokens ──► Hóa đơn
     │               │               │
   Cắt 90%      (một phần của      (chỉ một phần
    ở đây         input, cùng         hóa đơn,
    ✅ ✅ ✅      prompt, system,   output cũng
                  history)           tính tiền)
```

- Token counts RTK báo cáo ước lượng `bytes / 4` — không có tokenizer.
- **Phần trăm giảm đáng tin cậy**, con số token tuyệt đối chỉ xấp xỉ.
- Mức giảm thực tế pha loãng qua từng tầng khi tính hóa đơn cuối.

## Ví Dụ Báo Cáo

```bash
$ rtk gain
Commands run: 342
Raw bytes avoided: 1.2 MB
Estimated tokens saved: ~300k
Reduction: 82%
```

```bash
$ rtk discover
Found 5 commands with 0% reduction:
  - terraform plan      (12 calls)
  - kubectl apply       (8 calls)
  - ansible-playbook    (6 calls)
Consider `rtk init` for these or add custom TOML filters.
```

## Liên Kết Với Harness Evaluation

| Harness `11-evaluation` concept | RTK tương ứng |
|----------------------------------|---------------|
| Đo lường hiệu quả agent | `rtk gain` — token saved |
| Tìm cơ hội cải thiện | `rtk discover` — 0% reduction commands |
| Automated metrics | `rtk gain --all --format json` — feed dashboard |
| Continuous improvement | `rtk session` — adoption check |

## Benchmark Của RTK

| Command | Output thô | Output RTK | Giảm |
|---------|-----------|------------|------|
| `ls -la` | 45 lines | 12 lines | ~73% |
| `git push` | 15 lines | `ok main` | ~93% |
| `cargo test` (fail) | 200+ lines | ~20 lines | ~90% |
| `ruff check` | Nhiều dòng | Grouped | ~80% |
| `docker ps` | Nhiều cột | Essential only | ~70%+ |

## Lưu Ý Khi Đo Lường

- Thỉnh thoảng chạy `rtk gain` để theo dõi xu hướng (đúng tinh thần module `11-evaluation` — đo liên tục).
- `rtk discover` chỉ ra lệnh nào chưa được filter — đó là chỗ bạn còn bổ sung custom TOML filters được.
- Telemetry mặc định **tắt** — RTK không gửi số liệu của bạn đi đâu nếu bạn không opt-in.

---

*Trở về [rtk/README.md](../)* · Trước: [03 — Patterns](../03-patterns/) · Tiếp theo: [05 — Troubleshooting](../05-troubleshooting/)