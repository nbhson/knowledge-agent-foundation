# ❓ FAQ — RTK — Khái niệm (Câu hỏi thật, dễ hiểu)

RTK = tool nén output của lệnh bash để agent tốn ít token hơn. FAQ này giải đáp thắc mắc về khái niệm của nó.

Nếu câu hỏi chưa rõ, đọc phần được nêu trong ngoặc vuông ở `../README.md`.

---

## 01-concepts/README.md

### Q4. Agent tôi đọc file bằng tool `Read`/`Grep`/`Glob` — sao RTK không nén được, phải làm gì? [→ Giới Hạn Quan Trọng (Scope)]

`Read`/`Grep`/`Glob` là ba tool có sẵn của Claude Code: đọc file, tìm theo nội dung, tìm theo tên file. Hook = móc chặn tự động chạy trước khi lệnh bash thực thi.

**Bạn sẽ thấy**

Bạn cài hook xong, `git status` qua bash gọn xẹo (45 dòng còn 12), nhưng những lúc agent đọc file bằng tool `Read`, tìm bằng `Grep`, liệt kê bằng `Glob` thì output vẫn dài nguyên xi. Không thấy dấu hiệu RTK hoạt động ở những lần đó.

**Vì sao**

Hook chỉ chạy trên **Bash tool calls**. Các tool built-in của Claude Code (`Read`, `Grep`, `Glob`) không đi qua hook nên không bị auto-rewrite. Nghĩa là RTK chỉ nén được output của lệnh gõ vào shell, không nén được output của tool có sẵn.

Ngoài ra RTK đo **giảm bash output**, không phải giảm hóa đơn token toàn phần — input tokens chỉ là một phần của bill. Và RTK không thay thế việc nén context: nó tối ưu tầng Immediate Context (output của lệnh), còn system instructions, task context, domain knowledge, conversation history vẫn do harness xử lý ở module `02-build-context`.

Giải nghĩa: Immediate Context = dữ liệu vừa xuất hiện ngay trước mắt agent (kết quả lệnh vừa chạy); system instructions = chỉ dẫn hệ thống; task context = thông tin về việc đang làm; domain knowledge = kiến thức chuyên ngành; conversation history = nội dung các lượt trò chuyện trước.

**Làm gì**

1. Khi muốn nén, dạy agent dùng lệnh shell thay vì tool built-in: `cat`/`head`/`tail` (xem file từ đầu/cuối), `rg`/`grep` (tìm theo nội dung), `find` (tìm theo tên).
2. Hoặc gọi thẳng các lệnh của RTK: `rtk read`, `rtk grep`, `rtk find`.
3. Nhớ phạm vi: RTK tối ưu tầng Immediate Context, không tối ưu các tầng context khác.

> 📄 **Code ví dụ:** [`examples/01-q4-agent-toi-oc-file-bang-tool-read.sh`](examples/01-q4-agent-toi-oc-file-bang-tool-read.sh)

**Kiểm tra**

Chạy `rtk gain` rồi `rtk discover` để xem những lệnh nào đã được đo. Nếu một workflow của bạn toàn dùng tool built-in, hãy chuyển sang `rtk read`/`rtk grep` rồi đo lại để thấy khác biệt.

> **Tóm gọn 1 câu:** RTK chỉ nén output của lệnh bash, không nén được tool `Read`/`Grep`/`Glob` của Claude Code — muốn nén thì dùng lệnh shell hoặc `rtk read`/`rtk grep`/`rtk find`.

---

### Q5. `cargo test` fail mà RTK chỉ in 2 dòng — có phải chạy lại cả test không? [→ Khi Lệnh Fail: Tee Recovery]

`cargo test` = lệnh chạy test của Rust. Tee recovery = cơ chế "tách bản sao" output đầy đủ lưu vào file trước khi nén.

**Bạn sẽ thấy**

Lệnh fail lại ra đúng hai dòng, kèm đường dẫn tới file log:

```
FAILED: 2/15 tests
[full output: ~/.local/share/rtk/tee/1707753600_cargo_test.log]
```

Tên file dạng `<số giây>_<tên lệnh>.log` — số giây là thời điểm chạy, tính từ 1/1/1970, nên các lần chạy không ghi đè nhau. Bạn (và agent) chỉ nhận 2 dòng thay vì 200+ dòng log gốc.

**Vì sao**

Đây là tính năng **tee recovery**: khi lệnh fail, RTK lưu toàn bộ output thô vào `~/.local/share/rtk/tee/` để agent đọc lại mà không cần chạy lại lệnh — `cargo test` chạy lại có thể mất vài phút.

**Làm gì**

1. Đọc file log được trỏ tới trong dòng thứ hai, đừng kết luận nguyên nhân chỉ từ 1 dòng tóm tắt.
2. Chỉnh mức lưu trong `config.toml` (file cấu hình của RTK) nếu muốn:

> 📄 **Code ví dụ:** [`examples/02-q5-cargo-test-fail-ma-rtk-chi-in.toml`](examples/02-q5-cargo-test-fail-ma-rtk-chi-in.toml)

3. `mode = "always"` lưu cả khi pass (repo lớn sẽ sinh nhiều file hơn); `mode = "never"` để không ghi gì.

**Kiểm tra**

Cố tình làm một test fail, xác nhận file log xuất hiện trong `~/.local/share/rtk/tee/`, rồi đối chiếu số dòng trong log với dòng `FAILED: 2/15 tests` để chắc là đủ thông tin.

> **Tóm gọn 1 câu:** Hai dòng đó là bản tóm tắt có chủ đích — log đầy đủ đã được lưu sẵn tại đường dẫn in kèm, đọc lại file đó thay vì chạy lại test.

---

### Q6. Con số "giảm 90%" có chính xác không, hay chỉ là quảng cáo? [→ Bốn Chiến Lược Nén]

**Bạn sẽ thấy**

README hứa cắt tới 90% bash output. Nhưng 01-concepts kèm một ghi chú quan trọng: **RTK không phải tokenizer**, nó chỉ ước lượng `bytes / 4`. Nghĩa là nó nén theo dòng và theo byte, không đếm token thật của mô hình — 1 token ≈ 4 ký tự là con số xấp xỉ cho tiếng Anh.

Bốn chiến lược nén:

Cách đọc bảng này: cột "Chiến lược" là tên cách nén; cột "Làm gì" giải thích nó bỏ/giữ gì; cột "Ví dụ" cho thấy kết quả trên một lệnh thật.

| # | Chiến lược | Làm gì | Ví dụ |
|---|---|---|---|
| 1 | Smart Filtering | Bỏ noise: comment, khoảng trắng, boilerplate | `git push` → `ok main` |
| 2 | Grouping | Gom mục tương tự (file theo thư mục, lỗi theo loại) | `ls` → tree kèm số file |
| 3 | Truncation | Giữ phần quan trọng, cắt phần thừa | `git diff` → bỏ headers |
| 4 | Deduplication | Gộp log lặp thành số lần | `docker logs` → `×42 repeated line` |

Noise = phần rác không mang thông tin; boilerplate = dòng mẫu lặp lại máy móc; `×42 repeated line` = dòng này lặp 42 lần, in một lần thay vì 42.

**Vì sao**

Tỷ lệ phần trăm đáng tin, nhưng **số token tuyệt đối chỉ là xấp xỉ**. Có lệnh giảm tới ~93% (`git push`), có lệnh chỉ ~70%+ (`docker ps`, vì phải giữ lại các cột cần thiết). Lệnh vốn đã ngắn thì không giảm được bao nhiêu.

**Làm gì**

1. Tin phần trăm, đừng tin số token tuyệt đối khi lập ngân sách.
2. Đo trên chính dự án của bạn bằng `rtk gain`, so sánh trước/sau khi cài.
3. Ưu tiên lệnh dài và chạy thường xuyên: `cargo test`, `docker logs`, `ruff check` (~80%) sẽ đem lại nhiều hơn `git status`.
4. Đừng kỳ vọng `docker ps` giảm 90% — tài liệu ghi rõ chỉ "essential only" (chỉ giữ phần cần thiết).

**Kiểm tra**

Chạy cùng một lệnh trước và sau khi cài, đếm dòng output thô bằng `| wc -l` (đếm số dòng), rồi so với số dòng RTK trả về. Lặp lại vài tuần một lần qua `rtk gain`.

> **Tóm gọn 1 câu:** Phần trăm giảm đáng tin còn số token là ước lượng (bytes ÷ 4) — hãy đo trên chính dự án của bạn bằng `rtk gain`.

---

### Q7. Cài RTK có rủi ro gì không — nó có gửi code, khoá hay dữ liệu của tôi đi đâu không? [→ Câu Hỏi Thường Gặp (Concepts Level)]

Secrets = thông tin bí mật (khoá API, mật khẩu); env vars = biến môi trường (biến cấu hình ngoài code); telemetry = dữ liệu sử dụng gửi về nhà sản xuất.

**Bạn sẽ thấy**

Bạn ngờ ngợ: RTK chạy lệnh thật rồi lọc output, nên nó có cơ hội chạm vào `.env`, `git diff` chứa khoá, hay log `kubectl` có thông tin nhạy cảm. Với dự án của công ty, đây là câu hỏi bắt buộc phải trả lời trước khi đưa vào CI (hệ chạy test tự động). `.env` = file chứa khoá cấu hình; `kubectl` = lệnh điều khiển Kubernetes (hệ chạy container).

**Vì sao**

Theo tài liệu, RTK **không collect source code, file paths, secrets, env vars**, và telemetry mặc định tắt. Riêng bộ lọc cho lệnh AWS còn chủ động strip (loại bỏ) secrets khỏi output trước khi trả về cho agent. Cấu hình và log nằm ở `~/.config/rtk/config.toml` (macOS: `~/Library/Application Support/rtk/config.toml`) và `~/.local/share/rtk/tee/`.

**Làm gì**

1. Để nguyên telemetry ở trạng thái mặc định tắt; nếu muốn chắc chắn, đọc hướng dẫn configuration trên trang rtk-ai.app.
2. Loại những lệnh không muốn bị rewrite khỏi phạm vi nén (qua `exclude_commands` trong file cấu hình):

> 📄 **Code ví dụ:** [`examples/03-q7-cai-rtk-co-rui-ro-gi-khong.toml`](examples/03-q7-cai-rtk-co-rui-ro-gi-khong.toml)

3. Với repo có `.env` hoặc khoá: đừng để agent `cat .env` qua RTK; hãy lọc ở tầng dự án của bạn.
4. Cài ở phạm vi project (`rtk init --agent ...`) thay vì global nếu chỉ muốn thử trên một repo. Project = chỉ repo đang mở; global = áp dụng mọi repo trên máy.

**Kiểm tra**

Đọc `~/.config/rtk/config.toml` xem có bật telemetry không. Thử một lệnh `rtk` cho lệnh AWS có dữ liệu nhạy cảm và xem secret có bị ẩn đi. Sau khi chạy vài lệnh, kiểm tra thư mục `~/.local/share/rtk/tee/` xem có ghi gì bạn không mong muốn.

> **Tóm gọn 1 câu:** RTK không thu thập code, khoá hay dữ liệu của bạn và telemetry mặc định tắt — nếu vẫn lo, hãy loại các lệnh nhạy cảm khỏi phạm vi nén bằng `exclude_commands`.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: 01-concepts/README.md.*
