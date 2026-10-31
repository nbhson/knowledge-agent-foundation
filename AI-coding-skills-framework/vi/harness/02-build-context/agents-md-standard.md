# AGENTS.md: tờ nội quy dán ở cửa cho agent mới vào

> Phụ lục cho `harness/02` + `loop/01`.
> Chuẩn mở: https://agents.md · Đơn vị giữ chuẩn: Agentic AI Foundation (thuộc Linux Foundation).
> Khoảng 23 công cụ đã hỗ trợ. Claude Code đọc `CLAUDE.md` trước, nếu không có mới đọc `AGENTS.md` — nên giữ một symlink cho chắc.

> **Từ khóa nhanh:** *agent* = phần mềm AI tự đọc code và tự chạy lệnh thay bạn. *Repo* = kho mã nguồn của dự án. *Symlink* = "đường tắt" tới file khác — tạo một file tên `CLAUDE.md` mà nội dung thật nằm ở `AGENTS.md`, đổi chỗ nào cũng cập nhật cùng lúc.

## Tưởng tượng thế này

Phần này giải thích `AGENTS.md` là gì, bằng một ví dụ đời thường.

Bạn thuê một bạn trợ lý mới vào repo. Thay vì mỗi lần phải dặn lại
"build bằng lệnh gì, test bằng lệnh gì, tuyệt đối đừng đụng vào đâu",
bạn dán một **tờ nội quy ở cửa**: ngắn, rõ, ai vào cũng đọc.
`AGENTS.md` chính là tờ nội quy đó, nhưng viết cho agent đọc.

> **Tóm gọn 1 câu:** `AGENTS.md` = tờ nội quy đặt ở cửa repo, để agent mới vào biết luật chơi mà không cần bạn nhắc lại.

## Quy ước đơn giản

Phần này nói cách đặt và viết file, gồm 5 luật ngắn.

- **Một tờ ở gốc repo là đủ cho project nhỏ:** `AGENTS.md` đặt ở root
  (root = thư mục gốc cao nhất của repo).
- **Monorepo thì mỗi phòng một tờ:** monorepo = một repo chứa nhiều package/con-dự-án.
  Mỗi package có thêm `AGENTS.md` riêng.
  Agent sửa file ở đâu thì nghe tờ gần nhất ở đó (**file gần nhất thắng**).
- Viết Markdown thường, không field bắt buộc. Chỉ cần trả lời:
  build/test thế nào, convention (quy ước viết code chung của team) ra sao, vùng cấm ở đâu.
- File này đi cùng code, sửa qua PR như code (PR = pull request,
  đề nghị gộp code sau khi người khác duyệt). Đổi lệnh build mà quên sửa tờ này
  là agent chạy sai ngay.
- Lời bạn gõ trực tiếp trong chat luôn thắng mọi file. File chỉ là mặc định.

> **Tóm gọn 1 câu:** Một tờ ở gốc cho dự án nhỏ, mỗi package một tờ cho monorepo, ghi rõ build/test/convention/vùng cấm, và lời bạn gõ trong chat luôn có quyền cao nhất.

## Mẫu gọn để copy

Phần này cho một mẫu ngắn để bắt đầu, chỉ 5 dòng.

```markdown
# AGENTS.md — tên-project
## Build & Run — `pnpm install`, `pnpm dev`, `pnpm build`
## Testing — `pnpm test`, chạy 1 file: `pnpm test -- path/to/test.ts`
## Conventions — ...
## Boundaries — KHÔNG sửa package.json nếu chưa hỏi
```

Mục `Boundaries` (vùng cấm) rất quan trọng: ghi rõ việc gì cấm agent tự làm
(ví dụ `NEVER... without asking` = "tuyệt đối không... nếu chưa hỏi").
`pnpm` = trình quản lý package thay cho npm/yarn; các dòng sau dấu `—` là lệnh chạy cụ thể.

> **Tóm gọn 1 câu:** Copy mẫu 5 dòng trên, và đừng quên mục `Boundaries` — đó là chỗ cấm agent tự ý làm việc nguy hiểm.

## Đừng nhét mọi thứ vào một file — chia ra thế này

Phần này phân biệt 5 loại file hướng dẫn, vì mỗi loại có mục đích và thời điểm đọc khác nhau.

Cách đọc bảng này: cột **File** là tên file/tên loại file; cột **Giống như** là hình ảnh đời thường để dễ nhớ; cột **Khi nào đọc?** là lúc agent sẽ mở nó ra. Ví dụ, dòng đầu: nội quy `AGENTS.md` thì agent đọc ở *mọi* phiên làm việc.

| File | Giống như | Khi nào đọc? |
|---|---|---|
| `AGENTS.md` / `CLAUDE.md` / `GEMINI.md` | Nội quy công ty, ai cũng phải thuộc | Mọi phiên làm việc |
| `SKILL.md` trong `.agents/skills/*/` | Sổ tay quy trình từng việc | Chỉ khi việc khớp mô tả |
| `*.prompt.md` | Phiếu việc nhỏ, điền input là chạy | Khi gọi slash command |
| `*.agent.md` | Thuê chuyên gia ngoài cho việc khó | Khi bạn chọn hoặc agent chính gọi |
| `.github/hooks/*.json` | Khóa cửa + chuông báo động | Khi tới mốc vòng đời (trước/sau khi chạy tool...) |

Giải nghĩa thêm: `SKILL.md` = file mô tả một "kỹ năng" (xem `05-prompt-builder/agent-skills-spec.md`);
`*.prompt.md` = file lệnh tắt kiểu `/làm-điều-gì-đó`; `hooks` = móc chạy lệnh tự động tại các mốc như "trước/sau khi gọi tool".

Hai mẹo thực tế:

1. Chạy `ln -s AGENTS.md CLAUDE.md` (lệnh tạo symlink — `CLAUDE.md` thành "cửa" thứ hai cùng nhìn vào `AGENTS.md`) để Claude Code và các tool khác đọc chung một nguồn.
2. Với Copilot, custom agent muốn đọc chung instruction thì bật `include-custom-instructions: true` (công khai các chỉ dẫn chung cho agent tự tạo).
   Đừng copy nguyên văn cùng một nội dung vào cả `copilot-instructions.md` lẫn `CLAUDE.md` — vừa tốn token (token = đơn vị tính chữ mà model đọc, càng nhiều càng tốn tiền) vừa dễ lệch.

> **Tóm gọn 1 câu:** Nội quy nền để một file, quy trình riêng để skill, lệnh tắt để prompt file, và đừng copy-dán trùng nội dung — hãy symlink hoặc tham chiếu.

## Bảo trì: coi tờ nội quy hết hạn là bug

Phần này nói việc giữ file luôn đúng. "Stale" = nội dung cũ, không còn đúng thực tế.

Mỗi lần đổi lệnh build/test, đổi stack (bộ công nghệ của dự án), đổi cấu trúc thư mục — mở `AGENTS.md` ra sửa ngay.
Tờ nội quy cũ còn hại hơn không có, vì agent sẽ làm sai một cách rất tự tin.

> **Tóm gọn 1 câu:** Nội quy sai còn nguy hiểm hơn không có — đổi gì trong dự án thì sửa `AGENTS.md` ngay trong cùng PR.

## Mở rộng 10/2026 — Precedence & Ví dụ Monorepo

> Bổ sung bảng precedence giữa các "tờ nội quy" per-tool, và một skeleton
> `AGENTS.md` hoàn chỉnh cho monorepo để copy nhanh.

### 1. Precedence: một nguồn sự thật, nhiều biến thể

Phần này trả lời: khi nhiều công cụ tìm nhiều tên file khác nhau, nội dung nào "gốc"?

Precedence = thứ tự ưu tiên. `AGENTS.md` là **chuẩn mở** (agents.md, do Agentic AI Foundation thuộc Linux
Foundation giữ — nghĩa là bất kỳ công ty nào cũng được dùng, có tổ chức trung lập giữ chuẩn). `CLAUDE.md`, `GEMINI.md`, `copilot-instructions.md` là **biến thể
per-tool** — cùng một bản chất, khác tên file mà từng công cụ tìm đọc:

Cách đọc bảng này: cột **File** là tên file mỗi công cụ tìm; cột **Vai trò** cho biết file đó là "gốc" hay chỉ biến thể; cột **Nên chứa gì** là nội dung khuyên dùng. Ví dụ: `AGENTS.md` là gốc chứa nội quy đầy đủ, còn `CLAUDE.md` chỉ cần là bản tóm tắt hoặc symlink trỏ về gốc.

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

> **Tóm gọn 1 câu:** Việc nội quy thật đúng một chỗ (`AGENTS.md`); `CLAUDE.md`, `GEMINI.md`, copilot-instructions chỉ là cửa phụ trỏ về đó — tránh hai nguồn sự thật.

### 2. Ví dụ: `AGENTS.md` Skeleton Cho Monorepo

Phần này cho một khung sườn (skeleton = bản mẫu chưa lấp nội dung) hoàn chỉnh
cho monorepo — copy về và sửa tên, lệnh cho đúng dự án của bạn. Trong khung:
`pnpm -r build` = build toàn bộ các package; `--filter <pkg>` = chỉ chạy cho một package.

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

Giải nghĩa vài dòng trong khung: `force-push` = ghi đè lịch sử commit trên repo remote (mất backup);
`hardcode credential` = dán mật khẩu ngay trong code thay vì đọc từ biến môi trường (env);
`deployable` = ứng dụng có thể triển khai chạy thật.

Cấu trúc precedence khi đặt file này vào monorepo (mũi tên cho biết file nào quản vùng nào):

```
acme-monorepo/
├── AGENTS.md            ← root: overview + global rules (mọi agent đều đọc)
├── apps/web/AGENTS.md   ← ghi đè/bổ sung cho package web
├── packages/ui/AGENTS.md
└── scripts/AGENTS.md
```

> **Tóm gọn 1 câu:** Copy khung sườn trên cho monorepo: luật chung đặt ở root, luật riêng của từng package đặt trong `AGENTS.md` của package đó.

### 3. Nhắc Lại Hai Quy Tắc Đã Nêu

Phần này nhắc lại hai luật dễ quên nhất của cả tài liệu.

1. **"File gần nhất thắng"** với nested (nested = file lồng nhau theo thư mục): agent sửa `apps/web/src/x.ts` thì nghe
   `apps/web/AGENTS.md` trước, root `AGENTS.md` chỉ là nền chung. Đặt rule
   package-specific (riêng cho package đó) vào file gần nhất, đừng nhồi hết lên root.
2. **Stale AGENTS.md = bug.** Đổi lệnh build, đổi stack, đổi cấu trúc thư mục mà
   quên sửa `AGENTS.md` là agent làm sai *một cách rất tự tin* — như phần
   [Bảo trì](#bảo-trì-coi-tờ-nội-quy-hết-hạn-là-bug) ở trên. Sửa file này qua PR,
   cùng PR với code nó mô tả.

> **Tóm gọn 1 câu:** Luật gần nhất thắng khi file lồng nhau, và nội quy hết hạn là bug phải sửa trong cùng PR với code.

### 4. Liên Kết

Phần này trỏ tới các tài liệu liên quan để đọc tiếp.

- [README.md](README.md) — module Harness 02 (Build Context), nơi file này là phụ lục.
- [AGENT_SYSTEM_ARCHITECTURE.md](../../AGENT_SYSTEM_ARCHITECTURE.md) — tổng thể kiến trúc 9 layer.

> **Tóm gọn 1 câu:** Đọc README của Harness 02 để hiểu bối cảnh, và AGENT_SYSTEM_ARCHITECTURE để thấy chỗ `AGENTS.md` ngồi trong tổng thể.
