# ❓ FAQ — RTK (Câu hỏi thật, dễ hiểu)

Nếu câu hỏi chưa rõ, đọc phần được nêu trong ngoặc vuông.

---

## README.md

### Q1. RTK là cái gì, cài vào có đáng không — nó thực sự cắt được bao nhiêu output? [→ Câu Chuyện Mở Đầu, Case Studies Thực Tế]

**Bạn sẽ thấy**

Agent của bạn chạy `git status`, `cargo test`, `ls -la` và mỗi lệnh trả về hàng trăm dòng. Giữa đống đó, dòng lỗi thật chỉ chiếm vài dòng và dễ bị chìm. Repo `rtk-ai/rtk` tự dùng thử công cụ của chính nó trên 16 AI coding tool (Claude Code, Cursor, Gemini CLI, Codex, Cline...) và đo ra:

| Lệnh | Output thô | Output qua RTK | Giảm |
|---|---|---|---|
| `ls -la` | 45 dòng | 12 dòng | ~73% |
| `git push` | 15 dòng | `ok main` | ~93% |
| `cargo test` (fail) | 200+ dòng | ~20 dòng | ~90% |
| `docker ps` | nhiều cột | chỉ cột cần thiết | ~70%+ |

**Vì sao**

RTK (Rust Token Killer) là một CLI proxy viết bằng Rust, chèn vào giữa agent và lệnh shell, cắt tới **90% bash output** trước khi nó chạm vào ngữ cảnh của LLM. Một binary duy nhất, hỗ trợ 100+ lệnh (git, cargo, npm, pytest, docker, kubectl, aws...), overhead dưới 10ms. Nén bằng 4 chiến lược: lọc noise, gom nhóm, cắt bớt phần thừa, gộp dòng lặp.

**Làm gì**

1. Trước khi cài, xem lệnh nào trong dự án bạn hay chạy nhất và output dài bao nhiêu dòng. `cargo test` và `git push` thường là hai thủ phạm lớn nhất.
2. Cài rồi tích hợp, đo lại để so sánh số dòng trước/sau:

```bash
brew install rtk
rtk init -g          # Claude Code / GitHub Copilot
rtk --version        # rtk 0.x.x
rtk gain             # dashboard token đã tiết kiệm
```

3. Nếu dự án bạn chủ yếu chạy `ls` với vài chục file, lợi ích sẽ ít hơn — đừng kỳ vọng con số 90%.

**Kiểm tra**

Mở `rtk gain` sau vài chục lệnh và xem bảng token đã tiết kiệm. Thử cùng một lệnh có và không có RTK, đếm dòng output thô bằng `| wc -l` rồi so với bảng ở trên.

---

### Q2. RTK có phải một phần của harness không — tại sao nó nằm trong `tools/` chứ không phải trong `harness/`? [→ RTK Có Phải Là Một Phần Của Harness Không?]

**Bạn sẽ thấy**

Bạn đọc [HARNESS_ENGINEERING.md](../../HARNESS_ENGINEERING.md) thấy harness gồm **7 components**, tưởng RTK phải là một module như `harness/01-11`. Nhưng tài liệu nói rõ: RTK là **công cụ thực thi cụ thể** (Rust binary), không phải knowledge module — nên nó sống trong nhánh `tools/`, cùng convention với `harness/` và `loop/`.

Về mặt khái niệm thì **CÓ — RTK thuộc Component #3, Context Management** (nhánh Context Optimization / Token Reduction), và liên quan phụ tới hai component khác:

| Component | Vai trò | RTK liên quan? |
|---|---|---|
| **Context Management** | AI luôn có đúng thông tin đúng lúc | Trực tiếp — nén Immediate Context (Level 5) |
| **Tools** | Định nghĩa AI được làm gì | Gián tiếp — tool proxy quanh shell |
| **Evaluation** | Đo lường hiệu quả | Gián tiếp — `rtk gain`, `rtk discover` |

**Vì sao**

RTK hiện thực hoá lý thuyết đã viết sẵn trong các module của harness: `harness/02-build-context` (nén context ở tầng Immediate Context), `harness/06-decide-tools-mcp` (thiết kế tool proxy), `harness/11-evaluation` (đo token saved). Kiến trúc vẫn là 7 components; `tools/` nay là nơi tập trung các công cụ hiện thực hoá toàn bộ 7 component đó.

**Làm gì**

1. Đọc `harness/02-build-context` trước để biết "Immediate Context (Level 5)" nằm ở tầng nào trong hệ thống context.
2. Nhớ mapping: `02-build-context` (chính), `06-decide-tools-mcp` (tool proxy), `11-evaluation` (đo).
3. Đừng tìm RTK trong `harness/01-11` — nó không nằm ở đó, đừng kết luận là thiếu tài liệu.
4. Khi lập kế hoạch giảm chi phí, đối chiếu với mục tiêu "Giảm Chi Phí 40-60%" trong HARNESS_ENGINEERING.md.

**Kiểm tra**

Mở `tools/README.md` để xem nhánh Tools tổng quan, và mở `tools/rtk/README.md` phần mapping — nếu bạn chỉ ra được module harness tương ứng cho RTK thì đã hiểu đúng chỗ nó đứng.

---

### Q3. Lần đầu đọc RTK — nên đọc file nào trước, thư mục nào để làm cái gì? [→ Lộ Trình Học, Lộ Trình Đề Xuất]

**Bạn sẽ thấy**

Thư mục `rtk/` có 5 thư mục con: `01-concepts/` (kiến trúc hook, 4 chiến lược nén, tee recovery), `02-setup/` (cài đặt + tích hợp 16 AI tool), `03-patterns/` (4 pattern production), `04-savings/` (đo lường token), `05-troubleshooting/` (lỗi thường gặp). Người mới hay mở thẳng `03-patterns/` rồi hỏng, vì chưa biết hook hoạt động thế nào.

Lộ trình đề xuất gồm 6 bước: đọc README → `01-concepts/` → `02-setup/` → bắt đầu với pattern Git Speedup trong `03-patterns/` → đo bằng `rtk gain` ở `04-savings/` → khi có sự cố thì đọc `05-troubleshooting/`.

**Vì sao**

Mỗi thư mục chứa một file `README.md`, đồng nhất với convention của `harness/` và `loop/`. Pattern (mẫu dùng) chỉ chạy được sau khi bạn hiểu hook và cấu hình, nên bước 2 và 3 không nên bỏ.

**Làm gì**

1. Chọn đúng file theo việc bạn đang làm, không đọc tuần tự tất cả:

| Bạn muốn... | Đọc |
|---|---|
| Hiểu RTK hoạt động thế nào | `01-concepts/` |
| Cài + gắn vào AI tool của bạn | `02-setup/` |
| Làm git nhanh hơn | `03-patterns/git-speedup.md` |
| Chỉ xem test nào fail | `03-patterns/test-only-failures.md` |
| Đo token đã tiết kiệm | `04-savings/` |
| Lệnh bị rewrite sai | `05-troubleshooting/` |

2. Nếu mới bắt đầu, làm đúng thứ tự 6 bước trên, dừng sau bước 2 để xác nhận bạn hiểu cơ chế.
3. Sau khi cài, đo trước khi đọc `04-savings/` — có số liệu thật thì tài liệu dễ nhớ hơn.

**Kiểm tra**

Bạn trả lời được ba câu thì coi như nắm: hook rewrite xảy ra ở bước nào, tee recovery lưu file ở đâu, và lệnh nào đo được token đã tiết kiệm.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: README.md. Câu hỏi chi tiết cho từng thư mục con nằm trong `FAQ.md` của thư mục con đó.*
