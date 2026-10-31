# 🧩 02. Bảy Production Patterns

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Nói ngắn gọn, một "production pattern" là **mẫu vòng lặp đã có người dùng thật và chạy ổn ngoài thực tế** — có sẵn scheduler, skills, state, cách kiểm chứng và cách bàn giao cho con người. Thay vì tự vẽ loop từ đầu, bạn chỉ cần chọn mẫu hợp nhất rồi chạy `loop init` để dựng khung.
> **Hình dung cho dễ:** Cứ như **gọi món ở quán quen** — bạn không cần tự nghĩ công thức; bếp (repo loop-engineering) đã nấu thử, đã bán cho khách thật, và ghi chú rõ "món này cay (tốn token), món này lành cho người mới (L1)". Việc của bạn chỉ là chọn món hợp với mình.
> **Vì sao đáng quan tâm:** Mỗi chi tiết trong các pattern này (chạy bao lâu một lần, tốn bao nhiêu token, hay hỏng theo kiểu gì) đều là bài học trả bằng tiền thật, không phải lý thuyết suông. Bạn dùng lại kinh nghiệm đó để khỏi vấp đúng 7 cái hố mà người đi trước đã gặp.

> Dưới đây là **7 mẫu loop dùng được thật ngoài production**. Mỗi mẫu trả lời ngắn gọn: giải quyết việc gì, chạy bao lâu một lần, cần skills/state nào, kiểm chứng ra sao, bàn giao cho con người thế nào, cùng vài lưu ý riêng theo từng tool.

## Bảng Tổng Hợp

**Cách đọc bảng này:** mỗi dòng là một pattern; cột "Cadence" là nhịp chạy (từ nhanh nhất 5–15 phút tới chậm nhất 1 ngày); cột "Level khởi đầu" là mức tự chủ nên bắt đầu (L1 = chỉ báo cáo, L2 = tự sửa có người kiểm); cột "Token cost" là chi phí mỗi lần chạy. Ví dụ, dòng CI Sweeper: chạy mỗi 5–15 phút, bắt đầu ở L2, và đắt nhất (very high).

| Pattern | Cadence | Level khởi đầu | Token cost |
|---------|---------|---------------|------------|
| [Daily Triage](daily-triage.md) | 1d–2h | **L1** report | Low |
| [PR Babysitter](pr-babysitter.md) | 5–15m | L1 watch | High |
| [CI Sweeper](ci-sweeper.md) | 5–15m | L2 cautious | Very high |
| [Dependency Sweeper](dependency-sweeper.md) | 6h–1d | L2 patch-only | Medium |
| [Changelog Drafter](changelog-drafter.md) | 1d or tag | **L1** draft | Low |
| [Post-Merge Cleanup](post-merge-cleanup.md) | 1d–6h | **L1** off-peak | Low |
| [Issue Triage](issue-triage.md) | 2h–1d | **L1** propose-only | Low |

## Pattern Picker — Chọn Loop Nào?

> **Đọc bảng này thế nào:** Bạn chỉ cần trả lời một câu "chỗ nào đang đau nhất lúc này?" rồi đi theo nhánh tương ứng. Nếu đau hai chỗ cùng lúc, đọc tiếp `Overlap Rules` để biết loop nào chạy chung được với loop nào.

```
What hurts right now?
  ├── CI red? ──► CI Sweeper
  ├── PRs stalling? ──► PR Babysitter
  ├── Morning chaos / noisy issues? ──► Daily Triage + Issue Triage
  ├── Dependabot / CVE noise? ──► Dependency Sweeper
  ├── Merge debt / TODOs piling up? ──► Post-Merge Cleanup
  ├── Release notes stale? ──► Changelog Drafter
  └── Tight token budget? ──► Changelog Drafter / Daily Triage (L1)
```

Đọc ví dụ một nhánh: "CI red?" nghĩa là CI đang đỏ (test thất bại trên nhánh chính) → chọn CI Sweeper. "PRs stalling?" là PR đang nằm ì không ai duyệt → chọn PR Babysitter (loop trông chờ PR).

### Cost-aware Picks

**Cách đọc bảng này:** mỗi dòng là một hoàn cảnh của bạn; cột "Nên chọn" là pattern an toàn-không đốt tiền; cột "Tránh" là pattern nên hoãn đến khi có ngân sách và cơ chế thoát sớm. Ví dụ: repo hobby tài chính eo hẹp thì chạy Changelog Drafter + Daily Triage (rẻ), đừng bật CI Sweeper mỗi 5 phút.

| Situation | Nên chọn | Tránh (cho đến khi có budget + early-exit) |
|-----------|----------|---------------------------------------------|
| Hobby / plan eo hẹp | Changelog Drafter, Daily Triage (L1), Post-Merge | CI Sweeper ở 5m, PR Babysitter ở 5m |
| CI đang đỏ | CI Sweeper ở **15m+** với early-exit | Full triage mỗi 5m khi main xanh |
| Nhiều PR mở | PR Babysitter 10–15m, L1 watch trước | L2 fix loops trên mọi tick |
| Tuần release | Changelog Drafter daily | Dependency Sweeper + CI Sweeper unattended |

### Overlap Rules

**Cách đọc bảng này:** mỗi dòng là một cặp loop có thể "đụng độ" khi chạy chung, và "Rule" là luật hòa nhau. Ví dụ: CI Sweeper và PR Babysitter cùng muốn sửa lỗi CI — luật là chỉ CI Sweeper được sở hữu failing checks (các check đang đỏ), PR Babysitter không được sửa lại cùng branch trong cùng giờ.

| Combination | Rule |
|-------------|------|
| CI Sweeper + PR Babysitter | CI Sweeper sở hữu failing checks; PR Babysitter không re-fix cùng branch trong cùng giờ |
| Daily Triage + bất kỳ | Daily Triage reports; action loops execute. Triage không auto-fix ở L1 |
| Dependency Sweeper + CI Sweeper | Pause Dependency Sweeper khi CI đỏ trên main |
| Post-Merge + PR Babysitter | Post-Merge chạy off-peak only (off-peak = ngoài giờ cao điểm) |
| Changelog Drafter + bất kỳ | Changelog Drafter read-mostly, an toàn; không auto-publish |

## First Loop Recommendation

Nếu bạn còn phân vân chưa biết bắt đầu từ đâu, cứ chọn **Daily Triage ở L1**. Loop này giúp bạn làm quen với nếp ghi state mà không lo nó tự merge linh tinh.

> **Tóm gọn 1 câu:** Mẫu an toàn để bắt đầu là Daily Triage ở mức L1 (chỉ báo cáo): bạn học cách loop ghi sổ mà không lo nó tự đụng tay vào code.

## Cách Dùng Một Pattern

1. **Chọn mẫu**: nhìn bảng hoặc cây quyết định ở trên.
2. **Dựng khung**: `npx @cobusgreyling/loop init . --pattern <name> --tool grok` (hoặc `--tool claude` / `--tool opencode` / `--tool codex`). Lệnh này tạo sẵn bộ khung file của pattern trong thư mục hiện tại, gắn với tool bạn chọn.
3. **Chép thêm skills** từ `templates/` nếu bạn muốn tùy biến thêm.
4. **Gắn lịch chạy** (`/loop`, `scheduler_create`, GitHub Action, Codex Automation).
5. **Tuần đầu cứ chạy ở L1 report-only** rồi hãy mở thêm quyền tự sửa.
6. **Chấm điểm lại**: `npx @cobusgreyling/loop audit . --suggest` (audit = khảo sát repo và gợi ý cải thiện).

> **Nhớ kỹ**: đừng nhảy thẳng lên L3 cho mẫu mới trên repo production. Xem [04-operating](../04-operating/) để biết lộ trình nâng cấp từ từ.

> **Tóm gọn 1 câu:** Quy trình 6 bước: chọn mẫu → dựng khung bằng lệnh init → thêm skills → gắn lịch → tuần đầu chỉ report → audit và nâng dần.

## Cập nhật 10/2026 — Portability: Patterns Không Gắn Vendor CLI

> **⚠️ Lưu ý quan trọng**
>
> Các pattern trong thư mục này đang tham chiếu CLI `@cobusgreyling/loop-*` trong các ví dụ. Đây là **ví dụ cụ thể để dễ hình dung**, KHÔNG phải dependency bắt buộc (dependency = thư viện/lệnh bắt buộc phải cài). Bạn có thể triển khai bất kỳ pattern nào bằng scheduler / toolchain khác mà vẫn giữ nguyên quy trình, metrics và safety gates.

### Mapping Pattern → Thay Thế Không Cần Vendor CLI

**Cách đọc bảng này:** cột trái là pattern gốc; cột phải là cách làm y hệt việc đó bằng công cụ có sẵn, không cần CLI riêng. Ví dụ: Daily Triage có thể chạy bằng GitHub Actions cron (lịch hẹn giờ của GitHub) + gắn nhãn issue.

| Pattern | Thay thế không cần vendor CLI |
|---------|-------------------------------|
| Daily Triage | GitHub Actions cron + issue labels |
| PR Babysitter | GitHub Actions + `gh` CLI |
| CI Sweeper | CI webhook + bot |
| Dependency Sweeper | Dependabot / Renovate |
| Changelog Drafter | git-cliff / release-drafter |
| Issue Triage | issue-labeler bot |

### Nguyên Tắc

**Pattern = quy trình + metrics + safety gates; CLI chỉ là một implementation.** Bất kỳ scheduler nào — cron, Temporal, Airflow, GitHub Actions, Kestra — đều implement được các pattern này, miễn là bạn giữ đúng ba thành phần cốt lõi ở trên.

> **Tóm gọn 1 câu:** Cái quan trọng là quy trình + chỉ số + cổng an toàn; công cụ chạy (CLI, cron, bot) chỉ là phương tiện, đổi được thoải mái.

### Checklist Chuyển Đổi

Khi port một pattern sang scheduler khác (port = chuyển sang nền tảng khác):

1. **Tách logic khỏi CLI** — quy trình (những gì loop làm) phải độc lập với tool gọi nó.
2. **Giữ exit code convention** — `0` = proceed, `2` = escalate, để control scripts nối tiếp được bất kể scheduler (exit code = mã số script trả ra khi kết thúc để báo thành công/lỗi).
3. **Giữ `STATE.md` + run log JSON schema** — state và log là hợp đồng giữa các lần chạy, không đổi theo tool.
4. **Test dry-run 1 tuần** trước khi cut-over — chạy song song ở chế độ report-only để xác nhận metrics khớp trước khi tắt hệ thống cũ (dry-run = chạy thử không tác động thật; cut-over = chuyển hẳn sang hệ thống mới).

> **Tóm gọn 1 câu:** Khi đổi scheduler: tách logic khỏi CLI, giữ nguyên exit code và schema state/log, rồi chạy thử song song 1 tuần trước khi tắt hệ thống cũ.
