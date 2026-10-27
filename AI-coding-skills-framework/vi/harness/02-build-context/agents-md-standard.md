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

## Mở rộng 10/2026 — Precedence & Ví dụ Monorepo

> Bổ sung bảng precedence giữa các "tờ nội quy" per-tool, và một skeleton
> `AGENTS.md` hoàn chỉnh cho monorepo để copy nhanh.

### 1. Precedence: một nguồn sự thật, nhiều biến thể

`AGENTS.md` là **chuẩn mở** (agents.md, do Agentic AI Foundation thuộc Linux
Foundation giữ). `CLAUDE.md`, `GEMINI.md`, `copilot-instructions.md` là **biến thể
per-tool** — cùng một bản chất, khác tên file mà từng công cụ tìm đọc:

| File | Vai trò | Nên chứa gì |
|------|---------|-------------|
| `AGENTS.md` | **Gốc** — chuẩn open (Linux Foundation), ~23 công cụ đọc | Toàn bộ nội quy thật, đầy đủ |
| `CLAUDE.md` | Biến thể per-tool (Claude Code đọc trước AGENTS.md) | Tóm tắt / symlink / import từ gốc |
| `GEMINI.md` | Biến thể per-tool | Tóm tắt / symlink / import từ gốc |
| `.github/copilot-instructions.md` | Biến thể per-tool (Copilot) | Tóm tắt + `include-custom-instructions` |

**Nguyên tắc: một nguồn duy nhất.** Nội quy thật chỉ tồn tại trong `AGENTS.md`;
các file per-tool chỉ là tóm tắt, symlink hoặc tham chiếu về nó. Copy nguyên văn
cùng một nội dung vào cả hai là tạo hai nguồn sự thật — sẽ lệch nhau, và lúc lệch
thì không ai biết nguồn nào mới đúng.

### 2. Ví dụ: `AGENTS.md` Skeleton Cho Monorepo

```markdown
# AGENTS.md — acme-monorepo

## Overview
Monorepo pnpm: apps/ (ứng dụng deployable) + packages/ (thư viện dùng chung)
+ scripts/ (vận hành). Agent sửa file ở đâu thì đọc AGENTS.md gần nhất ở đó.

## Global Rules (áp dụng mọi package)
- Package manager: pnpm — KHÔNG dùng npm/yarn, KHÔNG sửa pnpm-lock.yaml tay.
- Node 22, TypeScript strict — không tắt `strict` trong tsconfig con.
- Commit: conventional commits (`feat:`, `fix:`, `chore:`).
- KHÔNG force-push, KHÔNG deploy mà không qua CI.

## Build & Test
- Build tất cả: `pnpm -r build` · Test tất cả: `pnpm -r test`
- Test một package: `pnpm --filter <pkg> test`

## apps/web
Next.js 15; route handler nằm trong `app/api/`. KHÔNG import chéo từ apps/admin.
Chi tiết riêng: xem `apps/web/AGENTS.md`.

## packages/ui
Design system React + CSS modules. KHÔNG thêm dependency mới nếu chưa hỏi.
Mọi component phải có story + test.

## scripts/
Chạy với Node, KHÔNG `curl | sh`. Script đụng DB prod phải nhận connection
string từ env — tuyệt đối không hardcode credential.
```

Cấu trúc precedence khi đặt file này vào monorepo:

```
acme-monorepo/
├── AGENTS.md            ← root: overview + global rules (mọi agent đều đọc)
├── apps/web/AGENTS.md   ← ghi đè/bổ sung cho package web
├── packages/ui/AGENTS.md
└── scripts/AGENTS.md
```

### 3. Nhắc Lại Hai Quy Tắc Đã Nêu

1. **"File gần nhất thắng"** với nested: agent sửa `apps/web/src/x.ts` thì nghe
   `apps/web/AGENTS.md` trước, root `AGENTS.md` chỉ là nền chung. Đặt rule
   package-specific vào file gần nhất, đừng nhồi hết lên root.
2. **Stale AGENTS.md = bug.** Đổi lệnh build, đổi stack, đổi cấu trúc thư mục mà
   quên sửa `AGENTS.md` là agent làm sai *một cách rất tự tin* — như phần
   [Bảo trì](#bảo-trì-coi-tờ-nội-quy-hết-hạn-là-bug) ở trên. Sửa file này qua PR,
   cùng PR với code nó mô tả.

### 4. Liên Kết

- [README.md](README.md) — module Harness 02 (Build Context), nơi file này là phụ lục.
- [AGENT_SYSTEM_ARCHITECTURE.md](../../AGENT_SYSTEM_ARCHITECTURE.md) — tổng thể kiến trúc 9 layer.
