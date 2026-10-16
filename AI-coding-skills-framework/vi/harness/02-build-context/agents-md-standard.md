# AGENTS.md: tờ nội quy dán ở cửa cho agent mới vào

> Phụ lục cho `harness/02` + `loop/01`.
> Chuẩn mở: https://agents.md · Đơn vị giữ chuẩn: Agentic AI Foundation (thuộc Linux Foundation).
> Khoảng 23 công cụ đã hỗ trợ. Claude Code đọc `CLAUDE.md` trước, nếu không có mới đọc `AGENTS.md` — nên giữ một symlink cho chắc.

## Tưởng tượng thế này

Bạn thuê một bạn trợ lý mới vào repo. Thay vì mỗi lần phải dặn lại
"build bằng lệnh gì, test bằng lệnh gì, tuyệt đối đừng đụng vào đâu",
bạn dán một **tờ nội quy ở cửa**: ngắn, rõ, ai vào cũng đọc.
`AGENTS.md` chính là tờ nội quy đó, nhưng viết cho agent đọc.

## Quy ước đơn giản

- **Một tờ ở gốc repo** là đủ cho project nhỏ: `AGENTS.md` đặt ở root.
- **Monorepo thì mỗi phòng một tờ:** mỗi package có thêm `AGENTS.md` riêng.
  Agent sửa file ở đâu thì nghe tờ gần nhất ở đó (**file gần nhất thắng**).
- Viết Markdown thường, không field bắt buộc. Chỉ cần trả lời:
  build/test thế nào, convention ra sao, vùng cấm ở đâu.
- File này đi cùng code, sửa qua PR như code. Đổi lệnh build mà quên sửa tờ này
  là agent chạy sai ngay.
- Lời bạn gõ trực tiếp trong chat luôn thắng mọi file. File chỉ là mặc định.

## Mẫu gọn để copy

```markdown
# AGENTS.md — tên-project
## Build & Run — `pnpm install`, `pnpm dev`, `pnpm build`
## Testing — `pnpm test`, chạy 1 file: `pnpm test -- path/to/test.ts`
## Conventions — ...
## Boundaries — KHÔNG sửa package.json nếu chưa hỏi
```

Mục `Boundaries` rất quan trọng: ghi rõ việc gì cấm agent tự làm
(ví dụ `NEVER... without asking`).

## Đừng nhét mọi thứ vào một file — chia ra thế này

| File | Giống như | Khi nào đọc? |
|---|---|---|
| `AGENTS.md` / `CLAUDE.md` / `GEMINI.md` | Nội quy công ty, ai cũng phải thuộc | Mọi phiên làm việc |
| `SKILL.md` trong `.agents/skills/*/` | Sổ tay quy trình từng việc | Chỉ khi việc khớp mô tả |
| `*.prompt.md` | Phiếu việc nhỏ, điền input là chạy | Khi gọi slash command |
| `*.agent.md` | Thuê chuyên gia ngoài cho việc khó | Khi bạn chọn hoặc agent chính gọi |
| `.github/hooks/*.json` | Khóa cửa + chuông báo động | Khi tới mốc vòng đời (trước/sau khi chạy tool...) |

Hai mẹo thực tế:

1. Chạy `ln -s AGENTS.md CLAUDE.md` để Claude Code và các tool khác đọc chung một nguồn.
2. Với Copilot, custom agent muốn đọc chung instruction thì bật `include-custom-instructions: true`.
   Đừng copy nguyên văn cùng một nội dung vào cả `copilot-instructions.md` lẫn `CLAUDE.md` — vừa tốn token vừa dễ lệch.

## Bảo trì: coi tờ nội quy hết hạn là bug

Mỗi lần đổi lệnh build/test, đổi stack, đổi cấu trúc thư mục — mở `AGENTS.md` ra sửa ngay.
Tờ nội quy cũ còn hại hơn không có, vì agent sẽ làm sai một cách rất tự tin.
