# Hooks: đặt bảo vệ ở các cửa, việc nào qua cũng phải kiểm

> Phụ lục cho `harness/07` + `harness/10`.
> Tài liệu gốc: GitHub Docs "Use hooks with Copilot agents / CLI".

## Tưởng tượng thế này

Instruction là **lời dặn**: "nhớ format code trước khi commit nhé" — agent có thể quên.
Hooks là **bảo vệ đứng ở cửa**: trước khi tool chạy (`preToolUse`) thì chặn lại kiểm tra,
sau khi chạy xong (`postToolUse`) thì kiểm tra lần nữa. Muốn quên cũng không được.

Một phiên làm việc của agent có nhiều "cửa" như vậy:
mở đầu (`sessionStart`), user gửi tin (`userPromptSubmitted`),
trước/sau mỗi tool (`preToolUse`/`postToolUse`), lỗi (`errorOccurred`),
kết thúc (`sessionEnd`). Bản CLI còn thêm `agentStop`.

## Viết hook thế nào?

Mỗi mục đích một file `NAME.json` đặt trong `.github/hooks/`
(cloud agent bắt buộc file phải nằm trên nhánh mặc định).
CLI thì đọc từ thư mục đang làm việc. Viết xong nhớ 2 việc:
kiểm tra JSON bằng `jq . NAME.json` và cấp quyền chạy `chmod +x script.sh`.

Khung chuẩn:

```json
{
  "version": 1,
  "hooks": {
    "sessionStart": [],
    "sessionEnd": [],
    "userPromptSubmitted": [],
    "preToolUse": [],
    "postToolUse": [],
    "errorOccurred": []
  }
}
```

Mỗi hook là một lệnh cụ thể. Nhớ ghi **cả hai** `bash` (cho Linux/macOS)
và `powershell` (cho Windows) để máy nào cũng chạy được:

```json
{
  "type": "command",
  "bash": "./scripts/log-prompt.sh",
  "powershell": "./scripts/log-prompt.ps1",
  "cwd": "scripts",
  "env": { "LOG_LEVEL": "INFO" },
  "timeoutSec": 10
}
```

Ngoài chạy script local, hook còn có thể POST JSON tới một URL (HTTP hooks).

## Mỗi cửa dùng để làm gì?

- **`preToolUse` — cửa quan trọng nhất.** Hook nhận stdin JSON gồm
  `toolName` (tool gì) + `toolArgs` (định làm gì), rồi trả về quyết định:
  `deny` (cấm), `ask` (hỏi người), hoặc sửa lại `modifiedArgs`/`updatedInput`
  hay thêm `additionalContext`. Dùng để làm approval gate, chặn lộ secret,
  kiểm tra vùng ảnh hưởng. Ví dụ: cấm `edit/create` khi chưa có file phê duyệt.
- **`postToolUse` — cửa dọn dẹp.** Chạy formatter, cập nhật manifest hash,
  trigger test sau khi tool xong.
- **`userPromptSubmitted` / `sessionStart` / `sessionEnd` — cửa ghi sổ.**
  Bơm thêm context đầu phiên, ghi audit log cuối phiên.
  Log này chính là đầu vào cho `harness/13-trajectory-observability`.
- **Custom agent** có thể khai báo hooks ngay trong file agent (inline `hooks:`)
  hoặc xin dùng hooks chung của repo. Mặc định file hooks lạ không tự load —
  phải opt-in khi đã tin thư mục đó.

## Tự test ở máy mình trước

Giả lập một lần gọi tool rồi pipe vào script, xem nó trả về JSON có đúng không:

```bash
echo '{"timestamp":1704614400000,"cwd":"/tmp","toolName":"bash","toolArgs":"{\"command\":\"ls\"}"}' | ./my-hook.sh
```

Ba lỗi hay gặp: file không nằm trong `.github/hooks/`, thiếu `"version": 1`,
script chưa `chmod +x`. Với cửa phê duyệt thì nhớ nguyên tắc
**fail-closed**: lỗi hay timeout là cấm, không cho qua (timeout-deny).
