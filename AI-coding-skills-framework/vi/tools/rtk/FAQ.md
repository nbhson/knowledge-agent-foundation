# ❓ FAQ — RTK (Câu hỏi thật, dễ hiểu)

Nếu câu hỏi chưa rõ, đọc phần được nêu trong ngoặc vuông.

---

## README.md

### Q1. RTK là cái gì, cài vào có đáng không — nó thực sự cắt được bao nhiêu output? [→ Câu Chuyện Mở Đầu, Case Studies Thực Tế]

**Bạn sẽ thấy**

Agent của bạn chạy `git status` (báo file nào đã sửa), `cargo test` (chạy test Rust), `ls -la` (liệt kê file) và mỗi lệnh trả về hàng trăm dòng. Giữa đống đó, dòng lỗi thật chỉ chiếm vài dòng và dễ bị chìm. Repo `rtk-ai/rtk` tự dùng thử công cụ của chính nó trên 16 AI coding tool (Claude Code, Cursor, Gemini CLI, Codex, Cline...) và đo ra:

Cách đọc bảng này: cột **Lệnh** là lệnh được đo; cột **Output thô** là số dòng nếu chạy trực tiếp; cột **Output qua RTK** là số dòng khi chạy qua RTK; cột **Giảm** là % cắt bớt. Ví dụ dòng `git push`: 15 dòng tiến trình chỉ còn `ok main` — bớt ~93%.

| Lệnh | Output thô | Output qua RTK | Giảm |
|---|---|---|---|
| `ls -la` | 45 dòng | 12 dòng | ~73% |
| `git push` | 15 dòng | `ok main` | ~93% |
| `cargo test` (fail) | 200+ dòng | ~20 dòng | ~90% |
| `docker ps` | nhiều cột | chỉ cột cần thiết | ~70%+ |

**Vì sao**

RTK (Rust Token Killer) là một CLI proxy (chương trình đứng giữa agent và lệnh shell) viết bằng Rust, chèn vào giữa agent và lệnh shell, cắt tới **90% bash output** trước khi nó chạm vào ngữ cảnh của LLM (mô hình ngôn ngữ). Một binary duy nhất (một file chương trình), hỗ trợ 100+ lệnh (git, cargo, npm, pytest, docker, kubectl, aws...), overhead dưới 10ms (độ trễ thêm vào, không đáng kể). Nén bằng 4 chiến lược: lọc noise (bỏ phần rác), gom nhóm, cắt bớt phần thừa, gộp dòng lặp.

**Làm gì**

1. Trước khi cài, xem lệnh nào trong dự án bạn hay chạy nhất và output dài bao nhiêu dòng. `cargo test` và `git push` thường là hai thủ phạm lớn nhất.
2. Cài rồi tích hợp, đo lại để so sánh số dòng trước/sau:

> 📄 **Code ví dụ:** [`examples/01-q1-rtk-la-cai-gi-cai-vao-co.sh`](examples/01-q1-rtk-la-cai-gi-cai-vao-co.sh)

3. Nếu dự án bạn chủ yếu chạy `ls` với vài chục file, lợi ích sẽ ít hơn — đừng kỳ vọng con số 90%.

**Kiểm tra**

Mở `rtk gain` (lệnh in báo cáo tiết kiệm) sau vài chục lệnh và xem bảng token đã tiết kiệm. Thử cùng một lệnh có và không có RTK, đếm dòng output thô bằng `| wc -l` (đếm số dòng) rồi so với bảng ở trên.

> **Tóm gọn 1 câu:** RTK đứng giữa agent và shell để cắt tới 90% output lệnh — lệnh output càng dài (test, push, log) càng có lãi, đáng cài cho repo lớn.

---

### Q2. RTK có phải một phần của harness không — tại sao nó nằm trong `tools/` chứ không phải trong `harness/`? [→ RTK Có Phải Là Một Phần Của Harness Không?]

**Bạn sẽ thấy**

Bạn đọc [HARNESS_ENGINEERING.md](../../HARNESS_ENGINEERING.md) thấy harness (bộ khung điều khiển agent) gồm **7 components** (thành phần), tưởng RTK phải là một module như `harness/01-11`. Nhưng tài liệu nói rõ: RTK là **công cụ thực thi cụ thể** (Rust binary — file chương trình chạy được), không phải knowledge module (module kiến thức) — nên nó sống trong nhánh `tools/`, cùng convention (quy ước cấu trúc) với `harness/` và `loop/`.

Về mặt khái niệm thì **CÓ — RTK thuộc Component #3, Context Management** (quản lý ngữ cảnh đưa vào model), dưới nhánh Context Optimization / Token Reduction (tối ưu context / giảm token), và liên quan phụ tới hai component khác:

Cách đọc bảng này: cột **Component** là thành phần của harness; cột **Vai trò** là nhiệm vụ của nó; cột **RTK liên quan?** cho biết mức dính dáng. Ví dụ dòng đầu: Context Management cần AI có đúng thông tin đúng lúc — RTK phục vụ trực tiếp bằng cách nén context.

| Component | Vai trò | RTK liên quan? |
|---|---|---|
| **Context Management** | AI luôn có đúng thông tin đúng lúc | Trực tiếp — nén Immediate Context (Level 5) |
| **Tools** | Định nghĩa AI được làm gì | Gián tiếp — tool proxy quanh shell |
| **Evaluation** | Đo lường hiệu quả | Gián tiếp — `rtk gain`, `rtk discover` |

**Vì sao**

RTK hiện thực hoá lý thuyết đã viết sẵn trong các module của harness: `harness/02-build-context` (nén context ở tầng Immediate Context — tầng context model đọc trực tiếp), `harness/06-decide-tools-mcp` (thiết kế tool proxy — proxy = người đứng giữa thay gọi lệnh), `harness/11-evaluation` (đo token saved). Kiến trúc vẫn là 7 components; `tools/` nay là nơi tập trung các công cụ hiện thực hoá toàn bộ 7 component đó.

**Làm gì**

1. Đọc `harness/02-build-context` trước để biết "Immediate Context (Level 5)" nằm ở tầng nào trong hệ thống context.
2. Nhớ mapping (bảng đối chiếu): `02-build-context` (chính), `06-decide-tools-mcp` (tool proxy), `11-evaluation` (đo).
3. Đừng tìm RTK trong `harness/01-11` — nó không nằm ở đó, đừng kết luận là thiếu tài liệu.
4. Khi lập kế hoạch giảm chi phí, đối chiếu với mục tiêu "Giảm Chi Phí 40-60%" trong HARNESS_ENGINEERING.md.

**Kiểm tra**

Mở `tools/README.md` để xem nhánh Tools tổng quan, và mở `tools/rtk/README.md` phần mapping — nếu bạn chỉ ra được module harness tương ứng cho RTK thì đã hiểu đúng chỗ nó đứng.

> **Tóm gọn 1 câu:** RTK không phải module kiến thức trong `harness/` mà là công cụ thực thi — nhưng về khái niệm, nó hiện thực hóa Component #3 (Context Management) của harness.

---

### Q3. Lần đầu đọc RTK — nên đọc file nào trước, thư mục nào để làm cái gì? [→ Lộ Trình Học, Lộ Trình Đề Xuất]

**Bạn sẽ thấy**

Thư mục `rtk/` có 5 thư mục con: `01-concepts/` (kiến trúc hook, 4 chiến lược nén, tee recovery), `02-setup/` (cài đặt + tích hợp 16 AI tool), `03-patterns/` (4 pattern production), `04-savings/` (đo lường token), `05-troubleshooting/` (lỗi thường gặp). Người mới hay mở thẳng `03-patterns/` rồi hỏng, vì chưa biết hook (cái chặn tự đổi lệnh thành `rtk ...`) hoạt động thế nào.

Lộ trình đề xuất gồm 6 bước: đọc README → `01-concepts/` → `02-setup/` → bắt đầu với pattern Git Speedup trong `03-patterns/` → đo bằng `rtk gain` ở `04-savings/` → khi có sự cố thì đọc `05-troubleshooting/`.

**Vì sao**

Mỗi thư mục chứa một file `README.md`, đồng nhất với convention của `harness/` và `loop/`. Pattern (mẫu dùng) chỉ chạy được sau khi bạn hiểu hook và cấu hình, nên bước 2 và 3 không nên bỏ.

**Làm gì**

1. Chọn đúng file theo việc bạn đang làm, không đọc tuần tự tất cả:

Cách đọc bảng này: cột **Bạn muốn...** là việc bạn cần làm; cột **Đọc** là file/thư mục cần mở. Ví dụ dòng cuối: lệnh bị đổi sai thì mở `05-troubleshooting/`.

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

Bạn trả lời được ba câu thì coi như nắm: hook rewrite xảy ra ở bước nào, tee recovery (cơ chế lưu output đầy đủ ra log khi lệnh fail) lưu file ở đâu, và lệnh nào đo được token đã tiết kiệm.

> **Tóm gọn 1 câu:** Đọc theo thứ tự 6 bước — hiểu hook trước (`01-concepts/`), cài xong (`02-setup/`) rồi mới áp pattern; đừng nhảy thẳng vào pattern như người mới hay làm.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: README.md. Câu hỏi chi tiết cho từng thư mục con nằm trong `FAQ.md` của thư mục con đó.*
