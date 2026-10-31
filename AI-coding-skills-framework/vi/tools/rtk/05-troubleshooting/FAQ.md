# ❓ FAQ — RTK — Xử lý lỗi (Câu hỏi thật, dễ hiểu)

Nếu câu hỏi chưa rõ, đọc phần được nêu trong ngoặc vuông ở `../README.md`.

---

## 05-troubleshooting/README.md

### Q13. Chạy `rtk init` rồi mà lệnh không bị nén, hoặc báo `Binary 'rg' not found on PATH` — lỗi ở đâu? [→ § Bảng Failure Modes]

**Bạn sẽ thấy**

Hai triệu chứng khác nhau nhưng hay bị gộp làm một:

- `git status` vẫn ra bản thao đầy đủ, dù đã chạy `rtk init`. (bản thao = bản nguyên gốc, chưa cắt gì.)
- Một lệnh nén báo `Binary 'rg' not found on PATH`. (rg = ripgrep, công cụ tìm kiếm nhanh; PATH = danh sách thư mục hệ thống tra để tìm lệnh — không thấy tức là chưa cài.)

Ngoài ra, tool của bạn có sẵn `Read`, `Grep`, `Glob` — những công cụ tích hợp này **không đi qua hook**, nên chúng luôn ra bản gốc dù RTK đã bật. (hook = cái chặn tự động đổi lệnh bash thành `rtk ...`.)

**Vì sao**

Vì hook chỉ ảnh hành lên lệnh chạy qua bash. Sau `rtk init` mà không restart lại AI tool thì tiến trình cũ vẫn giữ cấu hình cũ. Còn `rg` (ripgrep) là công cụ tìm kiếm nhanh mà một số bộ lọc của RTK gọi tới — thiếu nó thì bộ lọc không chạy được.

**Làm gì**

1. Restart lại AI tool sau khi chạy `rtk init`, rồi thử lại `git status`.
2. Với lệnh không bị nén, hãy thử `rtk` gõ tay: nếu gõ tay ra bản nén thì vấn đề ở hook, không ở RTK.
3. Nếu báo thiếu `rg`, cài ripgrep bằng trình quản lý gói của hệ điều hành. (trình quản lý gói = công cụ cài phần mềm, ví dụ `brew` trên macOS.)
4. Muốn công cụ tích hợp cũng được nén, hãy chuyển sang dùng lệnh shell hoặc gọi trực tiếp `rtk read` / `rtk grep`.

> 📄 **Code ví dụ:** [`examples/01-q13-chay-rtk-init-roi-ma-lenh-khong.sh`](examples/01-q13-chay-rtk-init-roi-ma-lenh-khong.sh)

**Kiểm tra**

Sau khi restart, gõ `git status` (không gõ `rtk`) và xem output có gọn lại không. Nếu vẫn dài, chạy `rtk gain --history`: nếu lệnh đó không xuất hiện trong lịch sử thì hook chưa bắt.

> **Tóm gọn 1 câu:** Lệnh không nén thường do chưa restart tool sau khi cài hook; còn lỗi `rg` chỉ là thiếu ripgrep — cài thêm là xong.

---

### Q14. `cargo install rtk` xong rồi `rtk gain` báo lỗi — tôi cài nhầm package gì rồi? [→ § Bảng Failure Modes]

**Bạn sẽ thấy**

Bạn gõ `cargo install rtk` (cargo = trình cài package của Rust, package = gói mã nguồn) vì đọc hướng dẫn nói cài bằng cargo. Kết quả là `rtk gain` không chạy, hoặc báo sai. Hoặc bạn cài đúng tên nhưng vẫn lỗi. Trên Windows có thêm một triệu chứng nữa: hook kiểu shell cũ, xảy ra ở bản nhỏ hơn 0.37.2.

**Vì sao**

Vì trên crates.io (kho package của Rust) có **trùng tên**: gói `rtk` đã tồn tại và thuộc về một dự án khác — "Rust Type Kit". Cài theo tên sẽ đúng vào chỗ đó, nên bạn có một lệnh tên `rtk` nhưng không phải RTK bạn cần. Lệnh sẽ chạy được, nhưng không có `gain`, không có `discover`, không có hook nào cả.

**Làm gì**

1. Gỡ gói cài nhầm rồi cài đúng từ kho mã nguồn của RTK bằng địa chỉ git. (cài từ git = lấy trực tiếp từ repo chính chủ, không qua kho package chung.)
2. Sau khi cài lại, kiểm tra phiên bản để chắc chắn đang chạy đúng binary. (binary = file chương trình chạy được.)
3. Trên Windows, chạy lại `rtk init -g` để chuyển sang hook dùng binary native, thay cho hook kiểu shell cũ (hiện tượng này chỉ xảy ra ở bản dưới 0.37.2). (`-g` = global, áp dụng cho mọi project.)
4. Nếu vẫn lỗi, kiểm tra đường dẫn binary đang được gọi có trỏ tới kho git mới không — có thể bản cũ vẫn nằm trước trong PATH. (PATH = danh sách thư mục hệ thống tra để tìm lệnh; bản cũ nằm trước sẽ được gọi trước.)
5. Nếu lệnh quan trọng vẫn bị nén quá mức, thêm vào `exclude_commands` (danh sách lệnh được miễn nén) thay vì cài lại.

> 📄 **Code ví dụ:** [`examples/02-q14-cargo-install-rtk-xong-roi-rtk-gain.sh`](examples/02-q14-cargo-install-rtk-xong-roi-rtk-gain.sh)

**Kiểm tra**

Chạy `rtk gain` sau khi cài: phải ra bảng `Commands run` / `Raw bytes avoided` / `Estimated tokens saved` / `Reduction`. Nếu vẫn lỗi, hãy xem đường dẫn binary đang được gọi có trỏ tới kho git mới không.

> **Tóm gọn 1 câu:** `cargo install rtk` cài nhầm package trùng tên "Rust Type Kit" — phải gỡ và cài lại từ repo git chính chủ của RTK.

---

### Q15. Khi nào nên thêm lệnh vào `exclude_commands`, khi nào nên tắt hẳn RTK? [→ § Quy Tắc Exclude & Khi Nào Nên Tắt RTK]

**Bạn sẽ thấy**

Một lệnh quan trọng bị nén quá mức: bạn không còn đọc được chi tiết cần thiết. Một pipeline `| grep` trả về kết quả sai vì định dạng đã bị đổi (pipeline `|` = lấy output lệnh trước làm input lệnh sau — script cần đúng định dạng gốc để đọc được). Script CI parse output theo định dạng gốc nên vỡ (CI = hệ thống tự chạy kiểm tra sau mỗi lần commit; parse = đọc output theo máy). Có lúc bạn chỉ đang debug một tool và cần bản raw thuần.

**Vì sao**

Vì nén là biến đổi, còn một số việc cần bản gốc tuyệt đối. RTK xử lý việc này bằng hai mức: loại từng lệnh ra khỏi danh sách nén (qua `exclude_commands` — danh sách lệnh được miễn nén, khai báo trong `config.toml`), hoặc tháo hook hoàn toàn. Mức nhỏ hơn gần như luôn đủ và giữ nguyên lợi ích của các lệnh khác.

**Làm gì**

1. Thêm vào `exclude_commands` khi cần output **đầy đủ chính xác** (ví dụ `git diff` chi tiết, `terraform plan` — bản kế hoạch hạ tầng xem trước khi áp).
2. Thêm vào `exclude_commands` khi lệnh **không nên bị rewrite** vì có tác dụng phụ nguy hiểm — ví dụ `curl` tải nhị phân (tải file thực thi về máy), `playwright` (điều khiển trình duyệt).
3. Thêm vào `exclude_commands` khi pipeline hoặc script của bạn phụ thuộc định dạng output gốc.
4. Chỉ tháo hook khi bạn đang debug output chính xác của một tool và cần bản raw; hoặc lệnh có tác dụng phụ quan trọng mà bạn muốn thấy đủ log.

> 📄 **Code ví dụ:** [`examples/03-q15-khi-nao-nen-them-lenh-vao-exclude.toml`](examples/03-q15-khi-nao-nen-them-lenh-vao-exclude.toml)

> 📄 **Code ví dụ:** [`examples/04-q15-khi-nao-nen-them-lenh-vao-exclude.sh`](examples/04-q15-khi-nao-nen-them-lenh-vao-exclude.sh)

**Kiểm tra**

Sau khi thêm `exclude_commands`, chạy lại lệnh đó và xác nhận output khớp bản thao chạy trực tiếp. Chạy `rtk gain` để đảm bảo `Reduction` không sụt mạnh — nếu tụt lớn, bạn đã loại nhầm lệnh đang nén tốt.

> **Tóm gọn 1 câu:** Loại từng lệnh khỏi nén (`exclude_commands`) trước, tắt hẳn RTK chỉ khi đang debug cần bản raw — miễn nén từng lệnh gần như luôn đủ.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: 05-troubleshooting/README.md.*
