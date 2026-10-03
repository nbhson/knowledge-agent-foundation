# ❓ FAQ — Loop Patterns (Câu hỏi thật, dễ hiểu)

Nếu câu hỏi chưa rõ, đọc phần được nêu trong ngoặc vuông.

*Chữ viết tắt dùng trong file: CI = hệ thống kiểm thử tự động; PR (pull request) = yêu cầu gộp code; L1 = chỉ báo cáo, L2 = đề xuất sửa, L3 = tự quyết; flake = test lúc đỏ lúc xanh không rõ lý do; worktree = bản sao thư mục code riêng để làm việc không ảnh hưởng bản chính; cadence = chu kỳ chạy lặp.*

---

## README.md

### Q1. Sáng thứ hai mở máy: CI đỏ, issue mới ùn 30 cái, có PR mở 4 ngày chưa ai đụng — nên bật loop nào trước? [→ Pattern Picker]

**Bạn sẽ thấy**

Bảng tổng hợp 7 pattern, mỗi dòng có 3 con số: chu kỳ chạy, mức khởi đầu, chi phí token.

| Pattern | Cadence | Level | Token cost |
|---|---|---|---|
| Daily Triage | 1d–2h | L1 report | Low |
| PR Babysitter | 5–15m | L1 watch | High |
| CI Sweeper | 5–15m | L2 cautious | Very high |
| Issue Triage | 2h–1d | L1 propose-only | Low |

Mức khởi đầu chính là quyền của loop: L1 chỉ báo cáo, L2 mới đề xuất sửa, L3 tự quyết. Cột cuối là mức độ đắt khi chạy.

**Vì sao**

Mỗi pattern giải quyết đúng một loại đau khác nhau. Bật sai loop tốn tiền mà không dập được lửa: CI Sweeper không xử lý issue nhiều, Daily Triage không sửa được test đỏ. Ngoài ra có luật cứng: **không bao giờ nhảy lên L3 với một pattern mới trên repo thật**.

**Làm gì**

1. Trả lời đúng một câu: "thứ đang đau nhức ngay lúc này là gì?". Cây quyết định trong README có nhánh **Morning chaos / noisy issues?** → chọn Daily Triage + Issue Triage.
2. Scaffold (dựng khung sẵn) bằng một câu lệnh, `--tool` đổi theo công cụ bạn dùng: `grok`, `claude`, `opencode`, `codex`.

```bash
npx @cobusgreyling/loop init . --pattern daily-triage --tool grok
```

3. Chạy **một tuần ở chế độ chỉ báo cáo** (`report-only`) trước khi bật sửa. 4. Kiểm tra cấu hình rồi mới lên lịch chạy tự động.

**Kiểm tra**

Sau 1 tuần, mở `STATE.md` phải thấy mục `High Priority` và `Watch List` có nội dung thật; câu hỏi "lúc này cái gì đang cháy?" phải trả lời được trong 1 lần đọc, không phải mở 4 tab Slack/GitHub. Chạy `npx @cobusgreyling/loop audit . --suggest` xem nó còn ý kiến gì chưa xử lý.

---

### Q2. Token có hạn, mỗi ngày chỉ dám dùng khoảng 100k — chọn pattern nào cho an toàn? [→ Cost-aware Picks]

**Bạn sẽ thấy**

Bảng "Cost-aware Picks" liệt kê tình huống nên chọn gì và **nên tránh gì cho tới khi có budget**. Với khoản nhỏ, các loop chạy 5 phút một lần là cái tên đầu tiên bị gạch.

| Tình huống | Nên chọn | Nên tránh |
|---|---|---|
| Kế hoạch miễn phí / eo hẹn | Changelog Drafter, Daily Triage (L1), Post-Merge | CI Sweeper 5m, PR Babysitter 5m |
| CI đang đỏ | CI Sweeper 15m+ kèm thoát sớm | Full triage mỗi 5m khi main xanh |
| Đang trong tuần release | Changelog Drafter mỗi ngày | Cho 2 loop nặng chạy không người trông |

Con số cụ thể của Daily Triage: không có việc gì để làm ~5k token; quét trọn vẹn ở L1 ~50k; có bước sửa kèm kiểm tra ~200k. Trần khuyến nghị mỗi ngày: 100k token.

**Vì sao**

Chi phí không nằm ở số lần chạy mà ở việc loop có tự sửa hay không. Quét chỉ đọc rẻ; mở worktree, nhờ người viết code, rồi người kiểm tra là con đường đắt nhất. L1 có sẵn "early exit" (thoát sớm): hết việc thì dừng, đó là lý do 5k token cho lần chạy rỗng.

**Làm gì**

1. Tính trước bằng công cụ có sẵn, đừng đoán bằng cảm giác.
2. Giữ Daily Triage ở chu kỳ 1 ngày, mức L1: 1 lần chạy ~50k là nằm trong trần.
3. Muốn CI Sweeper thì bắt buộc kéo chu kỳ lên 15 phút trở lên và bật thoát sớm.

```bash
npx @cobusgreyling/loop cost --pattern daily-triage --cadence 1d --level L1
```

**Kiểm tra**

Đọc lại con số "Tokens/run" của từng pattern và cộng lại theo chu kỳ bạn định đặt. Nếu tổng vượt trần 100k/ngày thì phải hoặc giãn chu kỳ, hoặc hạ một loop xuống L1 — không được giữ nguyên số tiền rồi chỉ hy vọng loop "nhiều khi chạy không thấy gì".

---

### Q3. Tôi bật cả CI Sweeper và PR Babysitter, hai cái cùng sửa một nhánh thì sao? [→ Overlap Rules]

**Bạn sẽ thấy**

Hai loop mở hai worktree trên cùng một nhánh, đẩy hai commit sửa cùng một dòng, rồi bạn phải tự ghép tay. Hoặc tệ hơn: Dependency Sweeper nâng version giữa lúc CI Sweeper đang sửa test → CI đỏ vì lý do hoàn toàn khác.

| Cặp loop | Luật phải tuân |
|---|---|
| CI Sweeper + PR Babysitter | CI Sweeper giữ chủ PR đang fail; PR Babysitter không re-fix cùng nhánh trong cùng giờ |
| Daily Triage + bất kỳ | Triage chỉ báo cáo, loop action mới thực thi; L1 không auto-fix |
| Dependency + CI Sweeper | Dừng Dependency Sweeper khi CI trên main đang đỏ |
| Post-Merge + PR Babysitter | Post-Merge chỉ chạy ngoài giờ cao |

**Vì sao**

Các pattern được thiết kế để chạy **cùng nhau**, không phải để cạnh tranh. Khi hai loop cùng ghi vào một nhánh, "ai thắng" phụ thuộc thứ tự chạy — tức là ngẫu nhiên theo phút trong đồng hồ. Kết quả là nhánh nhiều commit rác và CI đỏ vòng lặp.

**Làm gì**

1. Chọn một người **sở hữu** mỗi mối đau: PR fail là của CI Sweeper, PR lâu không động là của PR Babysitter.
2. Mỗi skill ghi trong file cấu hình một danh sách nhánh được phép chạm tới (branch allowlist) — không có danh sách thì loop có thể sửa nhầm cả `main`.
3. Với Daily Triage: nó **báo cáo**, các loop action **thực thi**. Triage ở L1 tuyệt đối không auto-fix.
4. Trước tuần release: chỉ bật Changelog Drafter mỗi ngày, tắt các loop nặng chạy không người trông.

**Kiểm tra**

Đếm số worktree mở cùng lúc: mỗi nhánh chỉ nên có một chủ. Xem lịch chạy có chồng nhau giữa CI Sweeper (15m) và PR Babysitter (10–15m) trên cùng một nhánh không; nếu có thì dời lịch hoặc tắt bớt một cái.

---

### Q4. Tôi mới bắt đầu, cài 7 loop cùng lúc thì có nên không? [→ Cách Dùng Một Pattern / First Loop Recommendation]

**Bạn sẽ thấy**

Một thư mục `.loop/` lớn lên nhanh, nhiều cron cùng kêu, và bạn không biết loop nào sinh ra dòng log mình vừa đọc. README có câu rất dứt khoát: nếu chưa chắc, hãy bắt đầu bằng **Daily Triage ở L1** — nó dạy kỷ luật quản lý trạng thái mà **không có rủi ro auto-merge** (tự động gộp code).

**Vì sao**

Mỗi loop thêm một lớp trạng thái, một bộ skill và một lịch chạy. Bảy loop cùng lúc là bảy nguồn sự thật, và mọi kinh nghiệm trong README đều được đo bằng tiền thật trên repo thật — nghĩa là đã có người vấp trước và ghi lại. Bạn không cần vấp lại.

**Làm gì**

1. Chọn **một** pattern. Bảy bước trong README đúng thứ tự: chọn pattern → scaffold → copy skill từ `templates/` nếu cần tuỳ biến → đặt lịch → chạy report-only một tuần → audit.
2. Tuần đầu chỉ bật đặt lịch, **không** bật sửa.
3. Đọc cảnh báo ở `04-operating/` về đường nâng cấp mức trước khi muốn đi từ L1 lên L2.
4. Quy tắc vàng cần thuộc: **không nhảy L3 cho pattern mới trên production repo**.

```bash
npx @cobusgreyling/loop init . --pattern daily-triage --tool claude
npx @cobusgreyling/loop audit . --suggest
```

**Kiểm tra**

Sau một tuần, đo bằng đúng ba câu hỏi trong README: bao lâu từ lúc "có thứ gì hỏng" đến lúc người ta biết; có bao nhiêu buổi sáng `STATE.md` khớp với những gì bạn tự tìm được; số tin nhắn kiểu "cái gì đang cháy?" có giảm không. Nếu cả ba đều tệ thì loop chưa đáng tin — dừng, sửa cấu hình, đừng bật thêm loop thứ hai.

---

## daily-triage.md

### Q5. `STATE.md` ngày nào cũng phình ra, đọc không nổi — cắt bằng cách nào? [→ State / Failure Modes]

**Bạn sẽ thấy**

File state lớn dần vì các mục đã xong không bị xoá. Sau vài tuần, phần `High Priority` chứa 40 mục trong đó 35 mục đã merge từ lâu. Vòng lặp không còn giúp bạn thấy đâu là việc cần làm hôm nay.

**Vì sao**

`STATE.md` được ví như **xương sống trí nhớ** của loop. Khi nó phình, loop đọc nhiều context thừa mỗi lần chạy → tốn token và làm nhiễu. Failure mode được ghi rõ trong README của pattern: "State file lớn vô hạn" → phải prune (dọn) mục đã merge/đóng **mỗi lần chạy**.

**Làm gì**

1. Bắt buộc cập nhật 3 trường mỗi run: `Last run`, trạng thái + hành động cuối cùng của từng mục, và các quyết định của người đã ghi đè ý loop.
2. Cuối mỗi vòng, **prune** mục đã resolved/merged khỏi state.
3. Mục nào lặp lại hoặc chỉ là ồn (ví dụ PR của Dependabot) đẩy vào khu vực riêng để loop biết là đã bỏ qua.

```markdown
Last run: 2026-06-09 08:15 UTC
## High Priority
- [ ] #1241 — test lúc đỏ lúc xanh trong auth flow
  Loop action: Đã mở worktree, đề xuất fix, chờ người duyệt PR
## Watch List
- PR #1238 mở 4 ngày không có hoạt động
## Recent Noise (bỏ qua lần này)
- PR của Dependabot (đã có automation riêng)
```

**Kiểm tra**

Đếm số mục trong `High Priority` sau mỗi tuần: phải là con số nhỏ, vài chục là nhiều. Mỗi mục ở đó phải trả lời được "lần chạy gần nhất loop đã làm gì với nó?" mà không cần đọc log.

---

### Q6. Sau khi bật auto-fix, loop sửa nhầm thứ không quan trọng — chặn thế nào? [→ Verification Strategy]

**Bạn sẽ thấy**

Một thay đổi nhỏ, đúng hợp lý theo máy, nhưng không phải thứ bạn muốn làm: loop đụng vào code không liên quan để "cho xanh", và chính người viết code tự đánh dấu xong việc — không hề có ai kiểm tra lại.

**Vì sao**

Pattern này chia 3 giai đoạn. Ở giai đoạn 1 chỉ có báo cáo, người đọc `STATE.md`. Từ giai đoạn 2 trở đi có hai vai trò tách biệt: **người viết (implementer)** và **người kiểm tra (verifier)** — người viết **không bao giờ tự đánh dấu done**, verifier phải xác nhận đúng phạm vi sửa và test. Thêm một ranh giới nữa: skill triage **chỉ báo hiệu (signal only), không được tự bịa việc kiến trúc**.

**Làm gì**

1. Chạy report-only 1–2 tuần trước, với câu lệnh cấm auto-fix viết ngay trong prompt lịch chạy.
2. Khi bật sửa, luôn đi theo chuỗi: worktree → implementer → verifier. Không bỏ qua verifier.
3. Khi không chắc ưu tiên: ghi thẳng vào state là cần người quyết, đừng đoán.

```bash
/loop 1d Run $loop-triage and update STATE.md. Do not auto-fix on first week — report only.
```

**Kiểm tra**

Mỗi lần chạy ở giai đoạn 2+ phải thấy **hai** dấu vết riêng biệt: một bản sửa, một kết luận kiểm tra. Thiếu một trong hai nghĩa là chuỗi bị cắt. Ngoài ra loop phải báo riêng những mục nó **không** tự quyết được.

---

### Q7. Đêm có thứ hỏng mà sáng hôm sau mới biết — làm sao nhận ra? [→ Failure Modes]

**Bạn sẽ thấy**

Buổi sáng bạn đọc `STATE.md` và thấy mọi thứ bình thường, trong khi đêm qua `main` đã đỏ từ 2 giờ sáng. Báo cáo chạy lúc 8h lại nói "không có gì hỏng" vì dữ liệu 24 giờ nó đọc không ra.

**Vì sao**

Triage chỉ bắt được những gì **nằm trong cửa sổ nó đọc** — mặc định là 24 giờ. Chạy một lần lúc 8h sáng nghĩa là có tới 6 giờ đêm không ai canh, và failure mode "missed overnight failures" được liệt kê rõ trong README của pattern.

**Làm gì**

1. Bật chạy ngay khi có sự kiện (`fireImmediately: true`) thay vì chờ đến đúng giờ lịch.
2. Tách lịch: chạy một lần đầu ngày, một lệnh giữa ngày. Cửa sổ 24 giờ không còn là thứ duy nhất che chỗ trống.
3. Nếu team không dùng giao diện dòng lệnh, đặt một workflow GitHub Actions theo cron `0 8 * * 1-5` (8h sáng, thứ Hai đến thứ Sáu).

```bash
/loop 2h Run the loop-triage skill. Append high-priority items to STATE.md.
```

4. Trong prompt, nhấn: mọi mục mơ hồ thì đánh dấu cần người xem, đừng tự quyết.

**Kiểm tra**

Cố tình làm đỏ `main` lúc 3h sáng, rồi xem lần chạy kế tiếp có ghi nó vào `High Priority` không. Lặp lại thử ở giờ thường để chắc chắn đường sự kiện cũng hoạt động, không chỉ đường lịch.

---

### Q8. Một ngày Daily Triage tốn bao nhiêu token, và chạy 2 giờ một lần có chịu nổi không? [→ Cost Profile]

**Bạn sẽ thấy**

Bảng chi phí có 3 dòng, mỗi lần chạy lặp lại tốn khoảng 50k token ở mức L1 — chạy 12 lần một ngày là 600k, vượt xa trần 100k khuyến nghị.

| Tình huống | Token mỗi lần chạy |
|---|---|
| Không có việc | ~5k |
| Triage trọn vẹn (L1) | ~50k |
| Có sửa kèm kiểm tra (L2) | ~200k |

Cadence khuyên dùng: 1 ngày–2 giờ. Trần khuyến nghị mỗi ngày: 100k token.

**Vì sao**

Cadence và mức quyền là hai thứ nhân với nhau trong chi phí. Chính nhánh "assisted fix" mới đắt: mở worktree, người viết, người kiểm tra. Nếu bạn chạy 2 giờ một lần, phải giữ nguyên L1 — nếu vô tình bật L2 thì con số 200k nhân lên 12 là 2,4 triệu token/ngày.

**Làm gì**

1. Đo trước bằng công cụ `cost`, không suy đoán.
2. Chạy 2 giờ một lần thì đòi hỏi phần lớn lần chạy phải là lần rỗng (~5k), nghĩa là phần lớn thời gian không có gì để làm.

```bash
npx @cobusgreyling/loop cost --pattern daily-triage --cadence 2h --level L1
```

3. Nếu tổng vượt trần: giãn về 1 ngày một lần, hoặc giữ L1 và giới hạn việc xử lý mỗi lần chạy.

**Kiểm tra**

Sau 7 ngày, lấy tổng token thực tế chia cho số lần chạy thật. Nếu bình quân vượt ~50k mà lý do không phải "không có việc", hãy xem lại xem có vô tình bật bước sửa không.

---

## issue-triage.md

### Q9. Có issue viết tay kiểu "app chậm quá", không đủ thông tin — loop có tự đoán không? [→ How the Loop Runs]

**Bạn sẽ thấy**

Issue #1311 chỉ có một dòng: *"app slow"*. Loop ghi vào state là `[Ambiguous]`, rồi chạy skill `loop-intake` để **hỏi thêm trong chính issue đó** hoặc nâng cấp lên người xử lý — chứ không đoán xem lỗi ở đâu.

**Vì sao**

Có những issue **không đủ dữ liệu để kiểm chứng kết quả**: không biết trước sửa xong thì "chậm" có còn không, thì không có tiêu chuẩn pass/fail. Failure mode "đoán mò issue mơ hồ" được ghi rõ, và cách chữa duy nhất là: hỏi thêm hoặc nâng cấp — **không guess**. Skill triage chỉ làm signal, không được bịa việc kiến trúc.

**Làm gì**

1. Phân loại trước: bug / feature / câu hỏi / trùng / cũ.
2. Nếu mơ hồ thì gọi `loop-intake` (skill xử lý intake) để hỏi bổ sung hoặc escalate — tuyệt đối không điền chỗ trống bằng phỏng đoán.
3. Nếu đủ rõ thì mới ghi hành động đề xuất vào state.
4. Ghi rõ trong state lý do phân loại, không ghi trần.

```markdown
#1310 — auth timeout — [High, actionable] — đề xuất: tái hiện rồi sửa
#1311 — "app slow" — [Mơ hồ] — loop-intake: đã comment hỏi thêm
#1312 — trùng #1305 — [Dup] — đề xuất: đóng
```

**Kiểm tra**

Đọc lại các mục `[Mơ hồ]`: mỗi mục phải có câu hỏi đã hỏi thật trong issue, và ngày người báo lại. Mục nào đứng yên quá 3 ngày thì đưa sang hàng chờ người xử lý.

---

### Q10. Issue trùng nhau chồng lên nhau và issue cũ đã không ai đụng tới — xử lý sao? [→ State / Classify]

**Bạn sẽ thấy**

Hai mô tả gần như giống nhau cùng mở trong ngày, và một loạt issue từ 8 tháng trước. Loop đẩy tất cả vào cùng một danh sách, bạn phải tự đi lọc lại mỗi sáng.

**Vì sao**

Phân loại `duplicate` và `stale` chính là hai nhãn để loop cắt tải cho con người. Không có chúng, "issue mới" và "issue cũ đã chết" lẫn vào nhau, và danh sách phình ra mỗi ngày — đúng failure mode "overwhelm với nhiều issues".

**Làm gì**

1. Với mỗi issue mới/cập nhật trong 24 giờ: gắn một nhãn trong năm nhãn trên.
2. Ghi **bằng chứng** cho mỗi kết luận: link issue và lý do phân loại. Không có bằng chứng thì coi như chưa phân loại.
3. Ưu tiên theo mức độ nghiêm trọng, và giới hạn số issue xử lý trong một lần chạy.
3. Đưa issue ồn (Dependabot, câu hỏi lặp) vào khu vực bỏ qua để lần sau khỏi đọc lại.

```bash
npx @cobusgreyling/loop cost --pattern issue-triage --cadence 2h --level L1
```

**Kiểm tra**

Đo tỷ lệ phân loại đúng: phần lớn mục không bị phải làm lại ở lần chạy sau. Thêm một mốc thời gian: từ lúc issue mới xuất hiện tới lúc nó có nhãn + hành động đề xuất phải tính được bằng giờ, không phải bằng ngày.

---

### Q11. Issue rõ ràng, dễ sửa, mà loop vẫn không sửa — có phí không? [→ Verification Strategy]

**Bạn sẽ thấy**

Không có dòng commit nào do loop này tạo ra. Nó chỉ xếp loại và gợi ý. Chính README ghi thẳng: mức của pattern này là **L1 propose-only** — chỉ phân loại và gợi ý, **không sửa code**.

**Vì sao**

Vì một phân loại sai sẽ thành một sửa sai, mà lúc đó bạn phải đọc diff thay vì đọc báo cáo. Với giá một lần chạy ~40k token (không có việc ~5k), bạn rẻ hơn nhiều khi để loop đoán sai rồi sửa. Chuỗi được thiết kế thành ba chặng: **Issue Triage phân loại → Daily Triage ưu tiên → loop action thực thi**.

**Làm gì**

1. Đừng bật chế độ sửa ở pattern này. Đưa việc thực thi sang loop chuyên trách.
2. Chuỗi chuẩn phải bắt đầu từ đây vì nó ít rủi ro nhất, rất hợp làm cặp đầu tiên cùng Daily Triage.
3. Việc nào chuyển lên người: feature cần quyết định sản phẩm; issue mơ hồ đã hỏi vẫn chưa rõ; issue nghiêm trọng chưa có người nhận; và **vấn đề bảo mật thì báo động ngay**, không chờ lần chạy kế.

**Kiểm tra**

Chạy thử một tuần rồi kiểm tra: `git log` không có commit nào do loop tạo, nhưng `issue-triage-state.md` lại có mục `Needs Human` có nội dung thật. Trong state phải tồn tại cả mục "chờ người" — nếu mục đó luôn rỗng thì loop đang âm thầm tự quyết, sai thiết kế.

---

## ci-sweeper.md

### Q12. Bật CI Sweeper 5 phút một lần, hoá đơn token nhảy dựng đứng — làm sao? [→ Cost Profile]

**Bạn sẽ thấy**

| Tình huống | Token mỗi lần chạy |
|---|---|
| CI xanh (không làm gì) | ~5k (**bắt buộc**) |
| Phân loại lỗi | ~50k |
| Thử sửa (L2) | ~200k |

Cadence 5–15 phút, mức rất tốn kém, trần khuyến nghị 1 triệu token/ngày, và câu cảnh báo: ở chu kỳ 15 phút mà không bật thoát sớm thì trường hợp xấu nhất vượt **5 triệu token mỗi ngày**.

**Vì sao**

Chu kỳ 15 phút là 96 lần chạy mỗi ngày. Nếu mỗi lần đều đi trọn đường "đề xuất sửa" (~200k) thì con số 19 triệu là chuyện thường, chứ không phải chuyện hiếm. Vì vậy pattern này được đánh dấu **early exit required** — CI xanh thì chỉ có con số 5k, không được chạy tiếp.

**Làm gì**

1. CI đang đỏ thì kéo chu kỳ lên **15 phút trở lý**; 5 phút chỉ dành cho lúc đang giao hàng.
2. Thay vòng quét định kỳ, dùng GitHub Action bắn sự kiện `workflow_run` khi có job fail — nhanh hơn polling (hỏi thăm định kỳ).
3. Về đêm không ai trông thì giãn còn 30–60 phút.
4. Tạm dừng loop khi vượt số failure xử lý được trong một lần chạy, rồi gộp bản sửa thành đợt.

```bash
npx @cobusgreyling/loop cost --pattern ci-sweeper --cadence 15m --level L2
```

**Kiểm tra**

Đo tỉ lệ lần chạy rỗng: ở lúc CI xanh phải gần 5k. Đặt cảnh báo khi vượt 1 triệu token/ngày. Đo cả thời gian trung bình từ lúc CI đỏ tới bản sửa đầu tiên — đó mới là chỉ số cho biết loop có đáng tiền không.

---

### Q13. Có test lúc đỏ lúc xanh, loop sửa đi sửa lại mãi — nhận ra flake bằng cách nào? [→ Failure Modes / Verification]

**Bạn sẽ thấy**

Cùng một job `test-auth` đỏ rồi xanh, đỏ rồi xanh, mỗi lần loop lại mở worktree và đề xuất một bản sửa khác. Chỉ số "cùng job fail lại trong vòng 48 giờ" bắn lên cao.

**Vì sao**

Quy tắc nhận diện rất cụ thể và rất dễ kiểm tra: **nếu cùng một test đỏ rồi xanh khi chạy lại mà không có thay đổi code nào thì không được auto-fix**. Đó là định nghĩa flake mà pattern dùng. Luật: test vào hạng Watch, **không tự sửa** — sửa bừa còn tệ hơn để yên.

**Làm gì**

1. Trước khi mở worktree, phân loại lỗi thành ba nhóm: flake, hồi quy thật, hay hạ tầng.
2. Nếu là flake: đưa vào Watch, hoặc cách ly (chạy riêng) / tạm bỏ qua — **kèm một phiếu việc theo dõi**, không lặng lẽ bỏ.
3. Nếu chạm hạ tầng (máy chạy bị hết bộ nhớ, registry sập, thiếu secret): dừng lại và chuyển người, đừng sửa code.
4. Nếu là hồi qui thật: mới đi tiếp chuỗi worktree → implementer → verifier.

```markdown
### main @ abc1234
- Job: test-auth
- Lỗi: AssertionError trong test_refresh_token_expiry
- Attempts: 1/3
- Last action: fix tối thiểu trong worktree fix/ci-auth-refresh
```

**Kiểm tra**

So sánh hash commit giữa lần đỏ đầu và lần xanh sau: nếu không đổi, loop phải ghi "flake". Trong 7 ngày, không được có vụ nào đề xuất sửa cho một job đã tự xanh mà không đổi code.

---

### Q14. Loop đã thử sửa 3 lần vẫn đỏ — có nên thử lần thứ 4? [→ loop-guard / Human Handoff]

**Bạn sẽ thấy**

Trong state: `Attempts: 3/3`. Lần chạy kế tiếp loop lại đề xuất cách sửa thứ tư, cùng một job, cùng một lỗi. Mỗi lần đều tiêu ~200k token.

**Vì sao**

Đây chính là failure mode "sửa triệu chứng": CI xanh nhưng nguyên nhân gốc chưa đi đâu, lần sau lại đỏ. Pattern có sẵn công cụ chặn: skill `loop-guard` là **circuit breaker** (cầu dao), ghi mỗi lần thử vào file `loop-ledger.json`, và khi cùng một lỗi tái diễn đủ số lần hoặc vượt giới hạn thì **trip — ngắt — rồi escalate**, kèm tóm tắt context đã cắt gọn.

**Làm gì**

1. Đặt trần số lần thử (ví dụ 3). Không có trần thì không có cầu dao.
2. Khi chạm trần: **ngừng thử**, gửi lên người kèm tóm tắt context đã cắt bớt, thay vì đẩy thêm một bản sửa nữa.
3. Cũng phải chuyển người ngay nếu: lỗi hạ tầng, bản sửa chạm hơn **5 file** hoặc đụng phần lõi, test liên quan bảo mật, hoặc cần cách ly một flake.
4. Khi đã xong, dọn khỏi danh sách và lưu lại lịch sử 7 ngày.

**Kiểm tra**

Mở `loop-ledger.json`: số lần thử cho mỗi job phải không vượt trần, và mọi job chạm trần đều phải xuất hiện trong danh sách chờ người xử lý kèm link. Tỷ lệ cùng job fail lại trong 48 giờ phải giảm dần — đó là bằng chứng cầu dao đang hoạt động.

---

### Q15. CI xanh rồi mà không ai tin, và loop sửa nhầm cả nhánh chính — xử lý thế nào? [→ Verification Strategy / Failure Modes]

**Bạn sẽ thấy**

Một bản sửa làm CI xanh, nhưng bên tranh đổi nhiều thứ ngoài phạm vi: đổi luôn cấu hình, sửa file không liên quan để "cho qua". Cùng lúc, có nhánh khác bị loop đụng vào khi không nằm trong danh sách được phép.

**Vì sao**

Verifier ở đây **bắt buộc** chạy test trong worktree trước khi duyệt, và bao gồm ba câu hỏi: fix có thật sự xử lý lỗi không, có thay đổi ngoài phạm vi không, test có chạy qua ở máy không. Còn implementer thì **không được merge** — chỉ được đề xuất. Failure mode "sửa nhầm nhánh" được chặn bằng cách ghi rõ danh sách nhánh được phép trong từng skill.

**Làm gì**

1. Mỗi skill phải có branch allowlist rõ ràng; loop chỉ được sửa trong danh sách đó.
2. Bắt buộc có người kiểm tra chạy test trong worktree trước khi duyệt — không có ngoại lệ "CI xanh là được".
3. Implementer chỉ mở PR hoặc comment đề xuất, không tự gộp.
4. Sau khi merge, loop ghi vào mục đã xử lý: ví dụ `main @ def5678 — lint fix merged qua PR #1250`.

**Kiểm tra**

Mỗi PR do loop tạo phải có phần kết luận của verifier nêu rõ kết quả chạy test. Tỷ lệ "sửa xong không cần người can thiệp" chỉ nên tính cho các ca đơn giản — nếu con số này cao bất thường, nhiều khả năng verifier chưa thật sự kiểm tra gì.
## dependency-sweeper.md

### Q16. Bot báo hàng chục lỗ hổng bảo mật mỗi ngày mà không ai đụng tới — tự xử lý phần dễ được không? [→ § How the Loop Runs (Typical Cycle)]

**Bạn sẽ thấy**

Bảng cảnh báo phình to mỗi ngày. Cảnh báo cũ nằm chồng lên cảnh báo mới, cả nhóm đã quen bỏ qua. Ví dụ mục cần xử lý: `lodash 4.17.20 → 4.17.21` — mã `CVE-2023-XXXX` là mã định danh một lỗ hổng đã được công bố, mức `low` là mức rủi ro thấp. Đến khi báo chí đưa tin về một lỗ hổng, không ai biết repo của mình có dính hay không.

**Vì sao**

Cái này cố tình chia làm hai phần: Dependabot (bot của GitHub) chỉ **phát hiện**, còn sweeper lo phần **vá và kiểm chứng**. Bật mỗi Dependabot thì cảnh báo cứ tích tụ. Vá tay từng cái thì lại tốn công cho mấy bản vá chỉ khác một dòng số.

**Làm gì**

1. Bật cả hai: Dependabot để phát hiện, `dependency-sweeper` để vá.
2. Chỉ cho loop tự vá loại an toàn: lỗ hổng rủi ro thấp, bản vá chỉ nâng phiên bản, và trong 30 ngày đầu tiên phát hiện.
3. Mỗi lần vá đi theo 3 bước: mở worktree (bản sao riêng của repo để thử) → implementer vá → verifier chạy `npm ci && npm test` (cài lại toàn bộ gói rồi chạy hết test).
4. Xong thì mở pull request (PR) để **người** merge — loop không tự merge.
5. Xong vụ đó thì dọn luôn cảnh báo đã xử lý khỏi danh sách.

```bash
/loop 1d          # 6h–1d cũng được
npm ci && npm test # verifier bắt buộc trong worktree
```

**Kiểm tra**

Đo ba thứ: thời gian từ lúc cảnh báo lỗ hổng xuất hiện đến lúc bản vá được merge; tỉ lệ cảnh báo được xử lý xong mà không cần người (chỉ tính loại rủi ro thấp); và số lần bản vá làm hỏng build — mục tiêu là 0.

---

### Q17. Nó có tự nâng phiên bản lớn (kiểu openssl 1.1 → 3.0) không — tự nâng có phá production không? [→ § Human Handoff Points]

**Bạn sẽ thấy**

Trong danh sách việc của loop xuất hiện đúng một dòng rồi đứng yên: `openssl 1.1 → 3.0 (major, breaking) — waiting human decision`. Không có PR nào được mở. Nếu bạn tự nâng, log đầy lỗi kiểu "module not found" vì cách dùng thư viện đã đổi hẳn.

**Vì sao**

Nâng phiên bản lớn (major) gần như luôn kèm thay đổi phá vỡ (breaking): hàm bị đổi tên, tham số bị bỏ. Đó là việc phải sửa code ứng dụng, không phải đổi một dòng số. Thêm nữa có **denylist** — danh sách gói cấm tự động đụng vào: bảo mật, đăng nhập, thanh toán, hạ tầng.

**Làm gì**

1. Để loop chỉ vá loại "chỉ nâng phiên bản"; mọi thứ còn lại phải dừng lại và chờ người.
2. Cấu hình denylist ít nhất gồm: `openssl`, thư viện xác thực, thư viện thanh toán, gói hạ tầng.
3. Nếu alert đòi phải sửa code chứ không chỉ đổi số phiên bản → cũng chuyển người, đừng để loop tự sửa.
4. Lỗ hổng chưa có bản vá rõ ràng → chuyển người luôn.
5. Ghi việc đang chờ vào file state để không mất dấu qua các lần chạy.

```markdown
## Denylisted (human required)
- openssl 1.1 → 3.0 (major, breaking) — waiting human decision
```

**Kiểm tra**

Chạy thử với một cảnh báo major giả lập: kết quả phải là dòng "waiting human decision", không có PR nào mở ra, và state phải ghi lại việc này.

---

### Q18. Loop chạy lúc 3h sáng rồi bị tắt — lần sau nó làm lại từ đầu hay nhớ việc đã làm? [→ § State]

**Bạn sẽ thấy**

Trong file state có mục `In-flight` (đang làm dở): `lodash 4.17.20 → 4.17.21 (CVE-2023-XXXX, low) — worktree open — verifier PASS — PR #1260`. Tức có một PR đã mở nhưng chưa ai merge.

**Vì sao**

Mỗi lần chạy là một lần đọc cảnh báo từ đầu. Không có file state (file nhớ việc) thì loop không phân biệt được "việc này chưa làm" với "việc này xong rồi, đang chờ người merge" — hậu quả là mở hai PR cho cùng một bản vá.

**Làm gì**

1. Cấu hình loop ghi vào `dependency-sweeper-state.md`.
2. Mỗi lần bắt đầu: đọc state trước, rồi mới đọc cảnh báo mới.
3. Mỗi việc đang dở phải ghi 5 thứ: tên gói, phiên bản cũ → mới, worktree còn mở không, verifier pass hay chưa, số PR đã mở.
4. Chỉ gỡ mục khỏi danh sách khi nó đã merge hoặc cảnh báo đã hết hiệu lực.

```markdown
## In-flight
- lodash 4.17.20 → 4.17.21 (CVE-2023-XXXX, low) — worktree open
  verifier PASS — PR #1260
```

**Kiểm tra**

Chạy loop 2 lần liên tiếp khi còn PR chưa merge: lần hai phải bỏ qua việc cũ, số PR mới mở phải bằng 0.

---

### Q19. Chạy 6 giờ một lần thì tốn bao nhiêu, và lúc CI đang đỏ thì có nên cho chạy không? [→ § Cost Profile]

**Bạn sẽ thấy**

Một lần chạy không có gì để làm tốn khoảng 5k token; lần chỉ đọc và phân loại cảnh báo khoảng 20k; lần thực sự vá kèm kiểm chứng nhảy lên khoảng 150k. Rồi có ngày nhánh chính đang đỏ CI (bộ kiểm tra tự động) vì một thay đổi khác.

**Vì sao**

Phần tốn tiền nằm ở bước kiểm chứng: `npm ci && npm test` cài lại toàn bộ gói rồi chạy hết test — đó là lý do không được bỏ bước này, vì đổi phiên bản thường phá build một cách ngầm. Còn khi nhánh chính đang đỏ, PR mới cứ chồng thêm lỗi lên lỗi, khó phân biệt lỗi của ai.

**Làm gì**

1. Đặt trần ngân sách 500k token/ngày cho loop này (mức trung bình trong nhóm bảy pattern).
2. Xem chi phí trước khi bật:

```bash
npx @cobusgreyling/loop cost --pattern dependency-sweeper --cadence 1d --level L2
# no-op ~5k · triage ~20k · patch+verify ~150k · cap 500k/ngày
```

3. Khi CI đỏ trên nhánh chính → tạm dừng loop cho tới khi xanh.
4. Nhiều lỗ hổng cùng lúc → ưu tiên theo mức nghiêm trọng, gom theo tuần thay vì mở một loạt PR.

**Kiểm tra**

Sau một tuần chạy, xem báo cáo chi phí. Vượt 500k/ngày là dấu hiệu nhịp chạy quá dày hoặc có PR chưa merge bị vá lại.

---

## pr-babysitter.md

### Q20. PR của tôi mở 2 ngày chưa ai review — tự nhắc mà không spam được không? [→ § How the Loop Runs (Typical Cycle)]

**Bạn sẽ thấy**

Trong state có dòng: `PR #1250 — fix/ci-auth-refresh — CI: pending — review: 2/3 — stale 4h`. Nghĩa là PR đã có 2 trong 3 người duyệt đồng ý nhưng vẫn treo lơ lửng, và loop ghi lại `Loop action: Nudge comment sent. Waiting review.` (`nudge` = lời nhắc nhẹ).

**Vì sao**

Một PR tự nó không kêu to. Không ai nhắc thì nó nằm đó tới khi tác giả tự hỏi. Nhưng nhắc sai cách thì thành spam: nhắc mỗi 5 phút khiến cả nhóm tắt thông báo, rồi lần sau nhắc cũng chẳng ai đọc.

**Làm gì**

1. Nhịp chạy: `/loop 10–15m` trong giờ làm việc; khi đang giao hàng dồn dập và có nhiều PR bị bỏ rơi thì rút còn `/loop 5m`.
2. Chỉ nhắc khi PR quá hạn (`stale`): ví dụ không có hoạt động nào trong N giờ.
3. Mỗi PR tối đa một lời nhắc trong một ngày — nhắc lặp lại là lỗi, không phải tính năng.
4. Nhắc **người duyệt** qua comment hoặc nhãn, đừng nhắc tác giả.
5. Ghi lại đã nhắc gì trong state, để lần sau không nhắc lại.

```markdown
## Active PRs
- PR #1250 — fix/ci-auth-refresh — CI: pending — review: 2/3 — stale 4h
  Loop action: Nudge comment sent. Waiting review.
```

**Kiểm tra**

Theo dõi thời gian trung bình từ lúc PR bị bỏ rơi tới lúc có người review. Và kiểm tra không có ngày nào hai lời nhắc cho cùng một PR.

---

### Q21. Nó có tự sửa lỗi CI đỏ giùm không — rồi có tự merge không? [→ § Verification Strategy]

**Bạn sẽ thấy**

Với PR hỏng test, state ghi: `PR #1248 — dep bump lodash — CI: red (test-auth)` rồi `Worktree opened. Fix proposed. Verifier PASS. Waiting human.` Loop đã đề xuất xong bản vá, người vẫn phải merge.

**Vì sao**

Nhắc đúng là chưa đủ — rất nhiều PR chỉ chết vì một test đỏ mà ai cũng sửa được trong 5 phút. Nhưng để tự merge là chuyển quyền quyết định sang máy, và một bản vá "làm test xanh nhưng sai ý nghĩa" sẽ lọt thẳng vào nhánh chính.

**Làm gì**

1. Để loop phân loại lỗi trước; chỉ xử lý lỗi sửa được rõ ràng, kiểu test thiếu import hay snapshot cũ.
2. Chuỗi xử lý: worktree → implementer đề xuất bản vá → verifier chạy test trong worktree đó.
3. **Không auto-merge mặc định.** Implementer chỉ đề xuất, người quyết định bấm merge.
4. Nếu verifier từ chối (REJECT) → dọn worktree, ghi lại đây là lần thử thứ mấy.
5. Quá 3 lần thử trên cùng một PR → chuyển người.

```text
CI đỏ → phân loại → worktree → đề xuất sửa → verifier chạy test
  └─ từ chối → dọn worktree · ghi số lần thử · quá 3 lần → chuyển người
```

**Kiểm tra**

Đo tỉ lệ PR CI đỏ được dọn xong mà không cần người (chỉ tính lỗi nhỏ), và xác nhận không có PR nào của loop được merge tự động.

---

### Q22. PR bị conflict hoặc cần rebase — loop có tự giải quyết không, ai chọn khi hai bên đều hợp lý? [→ § Human Handoff Points]

**Bạn sẽ thấy**

PR cần rebase (đặt lại commit trên nền mới) vì nhánh chính đã có thay đổi. Khi loop mở worktree thì git báo conflict. Có khi conflict nằm đúng ở phần xử lý thanh toán hoặc đăng nhập.

**Vì sao**

Conflict là chỗ duy nhất máy không có tiêu chí đúng/sai rõ ràng: hai bên đều hợp lý, chọn sai có thể mất tiền thật. Nên đây là điểm bàn giao bắt buộc, không phải tuỳ chọn. Trong state, việc đó phải nhìn ra ngay là đang chờ người.

**Làm gì**

1. Git báo conflict → dừng, tuyệt đối không tự chọn một bên.
2. Tóm tắt hai phương án và đưa vào báo cáo cho người quyết.
3. Chuyển người luôn khi: sửa chạm hơn 5 file, đụng thay đổi bảo mật, quá 3 lần thử cùng một PR, hoặc có conflict.
4. Ghi số lần thử vào state để không thử vô hạn.

```markdown
- PR #1248 — dep bump lodash — CI: red (test-auth)
  Loop action: Fix proposed (attempt 2/3). Verifier REJECT → escalate.
```

**Kiểm tra**

Bài kiểm tra phải xác nhận một PR đang conflict không bao giờ bị tự merge, và mọi lần chuyển người đều kèm số lần thử trong state.

---

### Q23. Chạy 5 phút một lần mà có nhiều PR — cháy token không, có bị hai loop đụng nhau không? [→ § Failure Modes & Mitigations]

**Bạn sẽ thấy**

Tổng chi phí ngày tăng vọt dù phần lớn thời gian loop không làm gì. Và đôi khi một PR bị sửa hai lần bởi hai lần chạy chồng nhau.

**Vì sao**

Đây là pattern tốn token nhất trong nhóm bảy: mỗi lần chạy đều phải quét danh sách PR và trạng thái CI. Chi phí nhân lên theo số phút chia cho nhịp chạy. Nếu không có cơ chế thoát sớm (early exit) thì bạn đang trả tiền cho những lần chạy không có việc.

**Làm gì**

1. Luôn bật early exit: mọi PR đang ổn thì kết thúc ngay, đừng chạy tiếp.
2. Giới hạn số PR mà loop được phép xử lý trong một lần chạy.
3. Ghi trường `acting_on` trong state, và dùng khoá worktree (`lock`) để một PR chỉ có một loop động vào.
4. Đặt trần 2M token/ngày — cao nhất trong nhóm, vì nhịp chạy ngắn nhất.

```bash
npx @cobusgreyling/loop cost --pattern pr-babysitter --cadence 10m --level L1
# no-op ~5k · watch+nudge ~30k · fix attempt ~200k · cap 2M/ngày
```

**Kiểm tra**

Cho chạy 1 giờ ở mức chỉ xem (L1) khi không có việc gì — token phải ở mức gần no-op. Thử cho hai loop cùng chạy trên một PR và xác nhận chỉ một bên được ghi trạng thái.

---

## changelog-drafter.md

### Q24. Sắp release mà không biết bản này có gì — gom tự động từ lịch sử merge được không? [→ § How the Loop Runs (Typical Cycle)]

**Bạn sẽ thấy**

Một file `RELEASE_NOTES_DRAFT.md` tự xuất hiện, tóm tắt từ lần tag (mốc đánh dấu phiên bản) gần nhất: `Since last tag: v1.4.0 — Merged PRs: 42 — Breaking: 2 — Features: 15 — Fixes: 20`.

**Vì sao**

Thông tin release nằm rải rác ở hàng chục PR, mỗi người nhớ một phần. Lúc cần viết release notes thì phải lục lại từng PR — thường mất hơn một giờ và vẫn sót.

**Làm gì**

1. Chạy `/loop 1d` trong tuần chuẩn bị release, hoặc chạy thủ công / theo tag khi tới giờ.
2. Loop xác định mốc cuối (tag hoặc release gần nhất), rồi gom các PR đã merge cùng commit từ mốc đó.
3. Nhóm thành 5 nhóm: breaking (thay đổi phá vỡ), feature, fix, docs, deps.
4. Ghi ra `RELEASE_NOTES_DRAFT.md` rồi dừng lại — chưa publish.

```markdown
## Since last tag: v1.4.0
- Merged PRs: 42   - Breaking: 2
- Features: 15     - Fixes: 20
- Draft: RELEASE_NOTES_DRAFT.md (chờ human approve)
```

**Kiểm tra**

So số PR đã merge kể từ tag với số mục trong draft. Lệch là thiếu mục, phải bổ sung trước khi phát hành.

---

### Q25. Nó có tự đăng release notes lên trang release và tự tăng số phiên bản không? [→ § Verification Strategy]

**Bạn sẽ thấy**

Sau khi bạn duyệt draft, vẫn phải tự bấm phát hành. Số phiên bản (major/minor/patch — bậc thay đổi) cũng phải tự chọn. Loop không đụng vào cả hai.

**Vì sao**

Đây là pattern "chủ yếu chỉ đọc": không sửa code, không merge, nên được phép chạy cùng các loop khác. Nhưng phát hành ra ngoài là việc không hoàn tác được. Đặc biệt khi có 2 thay đổi phá vỡ, bắt buộc phải có người quyết định chúng thuộc phiên bản nào.

**Làm gì**

1. Cố định ở mức "chỉ soạn thảo" (L1); người duyệt trước khi phát hành.
2. Không bao giờ tự cập nhật file `CHANGELOG` hay tạo release.
3. Mỗi mục trong draft phải truy được về một PR hoặc issue — đó là cách kiểm tra từng dòng nhanh nhất.
4. Người quyết định bậc phiên bản và phần làm nổi bật các thay đổi phá vỡ.

```text
PR đã merge + commit → nhóm breaking/feature/fix/docs/deps
→ RELEASE_NOTES_DRAFT.md → NGƯỜI duyệt → phát hành (người làm)
```

**Kiểm tra**

Mọi mục trong draft phải có số PR/issue đi kèm. Chạy loop không cấp quyền phát hành phải không tạo ra release nào trên GitHub.

---

### Q26. Bật loop này 24/7 có tốn không, có an toàn khi chạy cùng loop khác không? [→ § Cost Profile]

**Bạn sẽ thấy**

Một lần chạy có việc thật tốn khoảng 30k token; ngày không có commit mới thì chỉ khoảng 3k. Nhịp chạy 1 ngày một lần, hoặc kích hoạt theo tag.

**Vì sao**

Vì nó gần như chỉ đọc và không tự xuất bản, đây là người bạn đồng hành ít rủi ro nhất trong nhóm — chạy song song với bất kỳ loop nào khác mà không cạnh tranh quyền. Nhờ vậy, đây là lựa chọn hợp lý khi ngân sách token eo hẹp.

**Làm gì**

1. Đặt trần 50k token/ngày — mức thấp nhất trong nhóm bảy pattern.
2. Nhịp chạy 1 ngày, hoặc kích hoạt theo tag khi chuẩn bị release.
3. Để loop chạy ở chế độ no-op (không làm gì) khi một ngày không có commit mới.
4. Theo dõi hai chỉ số: thời gian từ lúc bắt đầu chuẩn bị release tới lúc có draft, và tỉ lệ mục trong draft không phải sửa tay.

```bash
npx @cobusgreyling/loop cost --pattern changelog-drafter --cadence 1d --level L1
# draft ~30k · no-op ~3k · cap 50k/ngày
```

**Kiểm tra**

Sau một chu kỳ release, đếm số mục trong draft phải sửa tay. Càng nhiều càng cho thấy quy ước phân loại của dự án bạn chưa viết rõ.

---

## post-merge-cleanup.md

### Q27. Vừa merge xong còn để lại TODO/FIXME và nhánh cũ — ai dọn? [→ § How the Loop Runs (Typical Cycle)]

**Bạn sẽ thấy**

Repo có `auth/service.py` chứa 3 dòng `TODO` do chính PR vừa merge bỏ lại, và nhánh `fix/ci-auth-refresh` đã merge nhưng chưa xoá. Danh sách việc của loop ghi rõ từng mục kèm hành động.

**Vì sao**

Việc dọn sau merge không ai nhận, vì nó không thuộc PR nào. Để lâu thì repo rối, và người mới không biết dòng TODO còn hiệu lực hay đã bỏ. Đây cũng là kiểu "nợ" (merge debt) chỉ tăng chứ không tự trả.

**Làm gì**

1. Sau mỗi đợt merge, loop đọc lịch sử gần đây bằng `git log` rồi lập danh sách việc dọn: TODO/FIXME mới, code chết, nhánh tồn đọng sau merge.
2. Việc nhỏ và rõ ràng: worktree → đề xuất sửa → verifier → PR.
3. Việc mơ hồ (không rõ còn dùng không) → ghi vào backlog và cờ cho người, đừng tự quyết.
4. Gỡ mục khỏi backlog khi nó đã merge.

```markdown
## Cleanup Backlog
- [ ] PR #1255 để lại TODO trong `auth/service.py` (3 TODOs)
  Loop action: Draft fix proposed. Waiting human review.
- [ ] Branch fix/ci-auth-refresh chưa xoá sau merge
  Loop action: Suggest delete.
```

**Kiểm tra**

Số TODO/FIXME mới mỗi ngày phải giảm dần; và đo tỉ lệ PR dọn dẹp được merge mà không phải sửa lại.

---

### Q28. Nó có xoá nhầm code của tôi không — có được refactor và đổi hành vi không? [→ § Verification Strategy]

**Bạn sẽ thấy**

PR dọn dẹp mà loop đề xuất chỉ nên là sửa nhỏ: không refactor (viết lại cấu trúc), không đổi hành vi. Khi không chắc một đoạn code còn được dùng, PR phải dừng lại chờ người.

**Vì sao**

Một PR "dọn dẹp" mà thay đổi hành vi không phải dọn dẹp — nó là một đợt refactor núp dưới tên khác, và việc đó phải có người chịu trách nhiệm. Xoá code "chắc là không dùng" mà hóa ra vẫn có đường gọi động (gọi bằng tên) là mất chức năng âm thầm.

**Làm gì**

1. Giới hạn nghiêm: chỉ sửa nhỏ, không refactor, không đổi hành vi.
2. Verifier phải soi "diff nhỏ nhất có thể" — không được đụng vào file không liên quan.
3. Code chết mà bạn không chắc còn dùng → để người quyết, không tự xoá.
4. Nhánh cần xoá cưỡng bức (`force-delete`) → cũng để người quyết.
5. Dọn nhiều hơn N file trong một lượt → coi là việc mới, ghi backlog.

```text
TODO/FIXME mới · code chết · nhánh tồn đọng sau merge
├─ nhỏ và rõ  → worktree → verifier (diff nhỏ nhất) → PR
└─ mơ hồ      → ghi backlog, cờ cho người
```

**Kiểm tra**

Mỗi PR của loop phải có diff nhỏ và chạy đủ test. Có bất kỳ thay đổi hành vi nào thì phải bị chặn và chuyển người.

---

### Q29. Chạy lúc 9 giờ sáng được không — có đụng vào lúc đang release không? [→ § Scheduling]

**Bạn sẽ thấy**

Loop này được xếp chạy vào giờ thấp điểm (off-peak), ví dụ 22:00 hoặc cuối tuần. Nếu bạn ép chạy cùng lúc với PR Babysitter thì hai loop bắt đầu đụng việc dọn trên cùng một nhánh.

**Vì sao**

Dọn dẹp là việc không gấp, nhưng lại đụng vào file đang được người khác sửa. Chạy vào giờ vắng thì giảm xung đột. Và có một quy tắc cứng trong bộ pattern: Post-Merge Cleanup chỉ chạy off-peak, không chạy song song với PR Babysitter.

**Làm gì**

1. Đặt lịch `/loop 1d–6h` nhưng chỉ trong khung off-peak đã chọn.
2. Tuyệt đối không chạy song song với PR Babysitter.
3. Đang có release hoặc lúc bảo trì → dừng loop.
4. Vẫn cần khoá worktree để không đụng loop khác.

```bash
# ví dụ khung giờ an toàn
/loop 22:00 daily
```

**Kiểm tra**

Xem nhật ký các lần chạy phải nằm trong khung off-peak; khi PR Babysitter đang chạy thì loop dọn dẹp phải tự dừng.

---

### Q30. Chạy 6 giờ một lần thì tốn bao nhiêu, và làm sao biết nó có ích? [→ § Cost Profile]

**Bạn sẽ thấy**

Lần không có gì dọn tốn khoảng 5k token; lần thực sự dọn (quét rồi sửa nhỏ) nhảy lên khoảng 100k. Trần đề xuất 200k token/ngày.

**Vì sao**

Đây là pattern rẻ (mức thấp trong nhóm), nhưng lợi ích của nó là tích luỹ và khó nhìn thấy trong ngày. Nếu không đo, bạn sẽ tưởng nó vô dụng và tắt đi — rồi nợ dọn dẹp quay lại đúng lúc bạn cần giao hàng gấp.

**Làm gì**

1. Đặt trần 200k token/ngày, nhịp 1 ngày một lần là đủ.
2. Đo ba chỉ số: số TODO/FIXME mới mỗi ngày (đang giảm = loop hoạt động), tỉ lệ PR dọn dẹp không phải sửa lại, và điểm "sạch" của repo (ít nhánh tồn đọng, ít code chết).
3. Đo trước 2 tuần để có mốc so sánh.
4. Xem chi phí bằng lệnh dưới trước khi tăng nhịp.

```bash
npx @cobusgreyling/loop cost --pattern post-merge-cleanup --cadence 1d --level L1
# no-op ~5k · cleanup L1→L2 ~100k · cap 200k/ngày
```

**Kiểm tra**

Nếu đường biểu đồ TODO/FIXME đi xuống sau 2 tuần thì loop đang ăn mừng đúng. Nếu đi ngang mà vẫn tốn ~100k mỗi lần thì nó đang đề xuất việc bạn không merge.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: README.md, daily-triage.md, issue-triage.md, ci-sweeper.md, dependency-sweeper.md, pr-babysitter.md, changelog-drafter.md, post-merge-cleanup.md.*
