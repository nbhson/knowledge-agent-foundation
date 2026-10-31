# Agent Skills: đóng gói bí kíp cho agent, dùng khi cần mới mở

> Phụ lục cho `harness/05` + `harness/06` + `loop/01`.
> Spec chuẩn đọc ở đây: https://agentskills.io/specification

> **Đọc trang này để làm gì:** tài liệu dạy cách gói mỗi "bí kíp" (skill) thành một thư mục riêng — agent chỉ đọc tên + mô tả cho rẻ, việc nào khớp mới mở toàn bộ hướng dẫn ra.
>
> **Từ khóa nhanh:** *skill* = gói hướng dẫn cho một loại việc cụ thể; *token* = đơn vị tính chữ mà model đọc, tốn tiền theo lượng; *spec* = đặc tả chuẩn.

## Hãy tưởng tượng thế này

Phần này giải thích skill là gì bằng ví dụ bếp núc.

Skill giống như một **công thức nấu ăn** dán trong bếp. Bình thường bạn không cần
đọc hết 100 công thức. Bạn chỉ cần nhìn **tên món + dòng mô tả** ngoài bìa
là biết món nào hợp với bữa tối nay. Khi đã chọn món, bạn mới mở công thức đó ra
xem chi tiết, và chỉ khi cần mới lôi thêm dụng cụ hay nguyên liệu kèm theo.

Agent cũng vậy. Thay vì nhồi mọi quy ước vào prompt (vừa tốn token vừa loãng),
ta tách mỗi bí kíp thành một thư mục skill. Agent chỉ đọc lướt tên + mô tả,
thấy việc nào khớp mới mở ra đọc tiếp.

> **Tóm gọn 1 câu:** Skill = công thức nấu ăn: ngoài bìa chỉ có tên + mô tả (rẻ), vào trong mới có hướng dẫn chi tiết — đọc khi cần, không nhồi vào prompt.

## Một skill gồm những gì?

Phần này mô tả cấu trúc thư mục của một skill và agent đọc nó theo 3 lớp nào.

```
skill-name/
├── SKILL.md          # Bắt buộc: "bìa + công thức" — thông tin + hướng dẫn
├── scripts/          # Tuỳ chọn: code chạy được (python, bash, js...)
├── references/       # Tuỳ chọn: tài liệu đọc thêm khi cần
├── assets/           # Tuỳ chọn: mẫu có sẵn, ảnh, schema...
```

Agent mở theo 3 lớp, lớp nào cần mới mở lớp đó:

Cách đọc bảng này: cột **Lớp** là mức "mở bao nhiêu" của skill; cột **Khi nào mở?** là thời điểm agent đọc lớp đó; cột **Tốn bao nhiêu?** là chi phí token. Ví dụ, lớp 1: tên + mô tả được đọc lướt ở *mọi* phiên, chỉ tốn ~50–100 tokens cho mỗi skill.

| Lớp | Khi nào mở? | Tốn bao nhiêu? |
|---|---|---|
| Tên + mô tả (`name` + `description`) | Mọi phiên làm việc đều đọc lướt | Rất nhẹ, ~50–100 tokens/skill — để 100 skill cũng không sao |
| Toàn bộ `SKILL.md` | Chỉ khi mô tả khớp với việc đang làm | Nên giữ dưới ~5.000 tokens, viết gọn, ví dụ cụ thể |
| File trong `scripts/references/assets` | Chỉ khi hướng dẫn bảo "mở file này" hoặc "chạy script này" | Chỉ tốn khi thật sự dùng |

> **Tóm gọn 1 câu:** Skill = một thư mục với `SKILL.md` bắt buộc + các file phụ tuỳ chọn; agent đọc theo 3 lớp từ nhẹ đến nặng, lớp nào cần mới mở.

## Viết SKILL.md sao cho đúng?

Phần này nói luật viết file `SKILL.md` — "tấm bìa + công thức" của skill.

File này gồm 2 phần: **phần khai báo** (YAML ở đầu — YAML là định dạng ghi cấu hình
dạng danh sách `tên: giá trị`) + **phần hướng dẫn** (Markdown bên dưới).
Khai báo chỉ cho phép đúng 6 field này, đừng tự chế thêm:

Cách đọc bảng này: cột **Field** là tên mục khai báo; cột **Bắt buộc?** cho biết bỏ được hay không; cột **Viết sao cho đúng?** là luật và ví dụ. Ví dụ, field `name`: bắt buộc, phải trùng đúng tên thư mục skill.

| Field | Bắt buộc? | Viết sao cho đúng? |
|---|---|---|
| `name` | Có | ≤64 ký tự, chữ thường + số + gạch ngang, không `-` ở đầu/cuối, không `--`, **trùng tên thư mục**. Ví dụ: `pdf-processing` |
| `description` | Có | ≤1024 ký tự. Ghi **làm gì + khi nào dùng**. Luôn có cụm `Use when ...`. Ví dụ: `Extract PDF text, fill forms, merge files. Use when handling PDFs.` |
| `license` | Không | Tên ngắn gọn, ví dụ `Apache-2.0` |
| `compatibility` | Không | ≤500 ký tự. Ghi môi trường cần có, ví dụ `needs network, needs python3` |
| `metadata` | Không | Bảng `tên → giá trị` cho thông tin thêm, ví dụ `author`, `version` |
| `allowed-tools` | Không | Liệt kê tool được phép chạy sẵn, cách nhau bằng dấu cách. Còn thử nghiệm, mỗi tool hỗ trợ khác nhau. Ví dụ: `Bash(git:*) Read` |

Ví dụ tối thiểu chạy được (xem thêm bản EN):

```markdown
---
name: pdf-processing
description: Extract PDF text, fill forms, merge files. Use when handling PDFs.
license: Apache-2.0
metadata:
  author: example-org
  version: "1.0"
---

# Xử lý PDF
...các bước làm, ví dụ, lỗi hay gặp...
```

Mẹo: nếu phân vân có nên cho skill chạy shell (lệnh terminal) sẵn không, thì **đừng cho**.
Để agent phải hỏi bạn trước khi chạy lệnh terminal — an toàn hơn nhiều.

> **Tóm gọn 1 câu:** Chỉ dùng đúng 6 field khai báo trên, `description` luôn có cụm `Use when ...`, và đừng cho skill chạy shell sẵn — để nó hỏi trước.

## Khi nào dùng skill, khi nào dùng thứ khác?

Phần này phân biệt skill với 4 khái niệm hay bị nhầm, bằng cách so "việc gì thì hợp cái nào".

Nhiều người mới hay nhầm 4 khái niệm này. Nhớ đơn giản thế này:

- **Việc chung, lúc nào cũng cần** (coding style, quy ước repo) → ghi vào
  instruction/`AGENTS.md`, đừng làm skill.
- **Việc chuyên biệt, thỉnh thoảng mới cần** (xử lý PDF, debug pipeline) → làm skill.
- **Skill hay prompt?** Việc nhiều bước + có file/script kèm theo → skill.
  Việc nhỏ gọn, chỉ cần điền vài input → prompt (slash command).
- **Skill hay custom agent?** Các bước dùng chung một bộ tool → skill là đủ.
  Cần cách ly (subagent trả về một kết quả gọn) hoặc mỗi giai đoạn cấm tool khác nhau → custom agent.
- **Instruction hay hooks?** Instruction là "dặn dò" — agent có thể quên.
  Hooks là "khóa cửa" — chạy bằng shell ở các mốc vòng đời, chặn được hẳn.
  Xem thêm `harness/07-workflow/hooks-standard.md`.
- **Đừng viết lại `AGENTS.md` trong skill.** `AGENTS.md` là nội quy nền, lúc nào cũng áp dụng.
  Skill là quy trình riêng, khi cần mới mở. Xem `harness/02-build-context/agents-md-standard.md`.

> **Tóm gọn 1 câu:** Việc chung → `AGENTS.md`; việc nhiều bước có file kèm → skill; việc nhỏ điền input → prompt (slash command); cần cách ly → custom agent; cần chặn cứng → hooks.

## Hai lưu ý an toàn

1. **Skill lạ = code lạ.** Skill từ nguồn không tin cậy có thể chứa lệnh nguy hiểm
   mà agent sẽ chạy. Luôn đọc qua trước khi cài, nhất là thư mục `scripts/`.
2. **Một nguồn duy nhất.** Đặt skill ở `.agents/skills/` (chuẩn chung, tool nào cũng đọc được).
   Đừng copy thành 3 bản `.agents/`, `.github/`, `.claude/` rồi lệch nhau lúc nào không hay.

> **Tóm gọn 1 câu:** Việc chung để instruction, việc chuyên biệt có file kèm để skill; skill lạ phải đọc trước khi cài, và để đúng một nơi duy nhất là `.agents/skills/`.
