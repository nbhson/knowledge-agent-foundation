# Hooks: đặt bảo vệ ở các cửa, việc nào qua cũng phải kiểm

> Phụ lục cho `harness/07` + `harness/10`.
> Tài liệu gốc: GitHub Docs "Use hooks with Copilot agents / CLI".

## Tưởng tượng thế này

> Phần này giải thích hooks là gì và khác gì với instruction — hiểu chỗ này thì hiểu toàn bộ file.

Instruction là **lời dặn**: "nhớ format code trước khi commit nhé" — agent có thể quên.
Hooks là **bảo vệ đứng ở cửa**: trước khi tool chạy (`preToolUse` — hook có tên nghĩa là "trước khi dùng tool") thì chặn lại kiểm tra,
sau khi chạy xong (`postToolUse` — "sau khi dùng tool") thì kiểm tra lần nữa. Muốn quên cũng không được.

Một phiên làm việc của agent có nhiều "cửa" như vậy:
mở đầu (`sessionStart` — phiên bắt đầu), user gửi tin (`userPromptSubmitted` — người dùng vừa nhập câu lệnh),
trước/sau mỗi tool (`preToolUse`/`postToolUse`), lỗi (`errorOccurred` — có lỗi xảy ra),
kết thúc (`sessionEnd` — phiên kết thúc). Bản CLI (chạy bằng dòng lệnh) còn thêm `agentStop` (agent vừa dừng).

> **Tóm gọn 1 câu:** Instruction là lời dặn có thể quên; hook là chốt kiểm bắt buộc đặt trước/sau mỗi cửa của phiên làm việc.

## Viết hook thế nào?

> Phần này giải thích đặt file hook ở đâu, viết gì bên trong, và kiểm tra ra sao.

Mỗi mục đích một file `NAME.json` đặt trong `.github/hooks/` (thư mục hooks của repo — mỗi file JSON là một hook)
(cloud agent bắt buộc file phải nằm trên nhánh mặc định).
CLI thì đọc từ thư mục đang làm việc. Viết xong nhớ 2 việc:
kiểm tra JSON bằng `jq . NAME.json` (`jq` = công cụ đọc/xử lý JSON; lệnh này in file ra để nhìn file có sai cú pháp không) và cấp quyền chạy `chmod +x script.sh` (cho phép script được thực thi).

Khung chuẩn:

> 📄 **Code ví dụ:** [`examples/01-viet-hook-the-nao.json`](examples/01-viet-hook-the-nao.json)

Mỗi hook là một lệnh cụ thể. Nhớ ghi **cả hai** `bash` (cho Linux/macOS)
và `powershell` (cho Windows) để máy nào cũng chạy được:

> 📄 **Code ví dụ:** [`examples/02-viet-hook-the-nao.json`](examples/02-viet-hook-the-nao.json)

Ngoài chạy script local (script nằm ngay trên máy), hook còn có thể POST JSON tới một URL (HTTP hooks — gửi gói JSON tới một địa chỉ web để hệ thống khác xử lý).

> **Tóm gọn 1 câu:** Mỗi hook là một file JSON trong `.github/hooks/`, khai báo lệnh chạy được (viết cho cả bash và PowerShell), và có thể là script local hoặc HTTP call.

## Mỗi cửa dùng để làm gì?

> Phần này giải thích từng loại hook dùng để làm gì — đọc theo từng "cửa".

- **`preToolUse` — cửa quan trọng nhất.** Hook nhận stdin JSON (dữ liệu JSON được bơm vào script qua luồng nhập chuẩn) gồm
  `toolName` (tool gì) + `toolArgs` (định làm gì — các tham số), rồi trả về quyết định:
  `deny` (cấm), `ask` (hỏi người), hoặc sửa lại `modifiedArgs`/`updatedInput` (đổi tham số trước khi chạy)
  hay thêm `additionalContext` (bơm thêm thông tin cho agent). Dùng để làm approval gate (cổng duyệt — phải được cho phép mới chạy), chặn lộ secret,
  kiểm tra vùng ảnh hưởng. Ví dụ: cấm `edit/create` khi chưa có file phê duyệt.
- **`postToolUse` — cửa dọn dẹp.** Chạy formatter (công cụ tự sắp lại code đẹp), cập nhật manifest hash (vân tay của file để biết file có đổi không),
  trigger test (kích hoạt chạy test) sau khi tool xong.
- **`userPromptSubmitted` / `sessionStart` / `sessionEnd` — cửa ghi sổ.**
  Bơm thêm context đầu phiên, ghi audit log (nhật ký kiểm tra) cuối phiên.
  Log này chính là đầu vào cho `harness/13-trajectory-observability`.
- **Custom agent** (agent tự định nghĩa) có thể khai báo hooks ngay trong file agent (inline `hooks:`)
  hoặc xin dùng hooks chung của repo. Mặc định file hooks lạ không tự load —
  phải opt-in (tự bật, chấp nhận trước) khi đã tin thư mục đó.

> **Tóm gọn 1 câu:** `preToolUse` là chốt duyệt quan trọng nhất (cấm/hỏi/sửa tham số), `postToolUse` lo dọn dẹp, các cửa còn lại lo bơm context và ghi sổ.

## Tự test ở máy mình trước

> Phần này giải thích cách thử hook ở máy mình trước khi đưa lên repo.

Giả lập một lần gọi tool rồi pipe vào script (pipe = đưa dữ liệu từ lệnh này sang lệnh kia bằng ký tự `|`), xem nó trả về JSON có đúng không:

> 📄 **Code ví dụ:** [`examples/03-tu-test-o-may-minh-truoc.sh`](examples/03-tu-test-o-may-minh-truoc.sh)

Ba lỗi hay gặp: file không nằm trong `.github/hooks/`, thiếu `"version": 1` (trường khai báo phiên bản định dạng hook),
script chưa `chmod +x`. Với cửa phê duyệt thì nhớ nguyên tắc
**fail-closed**: lỗi hay timeout là cấm, không cho qua (timeout-deny — "hết giờ coi như cấm"; fail-closed = "khi nghi ngờ thì chặn, không mở").

> **Tóm gọn 1 câu:** Test hook trước khi up bằng cách bơm JSON mẫu vào script; nhớ 3 lỗi kinh điển (sai thư mục, thiếu `version`, chưa `chmod +x`) và nguyên tắc fail-closed: nghi ngờ là cấm.
