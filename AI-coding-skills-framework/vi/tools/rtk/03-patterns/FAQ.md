# ❓ FAQ — RTK — 03-patterns (Câu hỏi thật, dễ hiểu)

Nếu câu hỏi chưa rõ, đọc phần được nêu trong ngoặc vuông ở `../README.md`.

---

## 03-patterns/README.md

### Q13. Tôi mới cài RTK lần đầu, nên bật pattern nào trước? [→ § First Pattern Recommendation]

**Bạn sẽ thấy**

Sau khi chạy `rtk init -g`, bạn có tới 4 pattern cùng lúc trong bảng tổng hợp: Git Speedup (~70–93% giảm output), Test Only Failures (~90%), File Smart Read (~60–90%), Build & Lint Compact (~75–85%). Agent bắt đầu gọi `rtk git status`, `rtk read`, `rtk tsc` xen kẽ nhau, và bạn không biết nên kiểm tra cái nào trước, hay một cái hỏng thì do đâu.

**Vì sao**

Vì cả 4 pattern đều đúng cả, nhưng mức rủi ro khác nhau. Git Speedup là pattern nền tảng, chỉ thay đổi cách hiển thị kết quả git (không đụng code của bạn), nên hỏng thì cũng chỉ hỏng kiểu "tôi không đọc được diff chi tiết" chứ không làm mất dữ liệu. Ba pattern kia chạm vào test, build, lint — nơi mà một lần nén quá tay có thể khiến agent kết luận sai.

**Làm gì**

1. Bật Git Speedup trước, rồi để ba cái kia ở trạng thái chưa kiểm chứng. Nó "an toàn, dễ verify", và áp dụng cho mọi phiên làm việc với git — tức là mọi phiên.
2. Kiểm tra bằng cách đối chiếu thô: chạy `git status` bình thường, rồi `rtk git status`, so kết quả hai bên.
3. Chỉ bật thêm Test Only Failures khi CI đang đỏ hoặc bạn đang debug regression; File Smart Read khi bạn lạc trong repo lớn.
4. Sau mỗi bật, chạy `rtk gain` để xem token đã tiết kiệm thật là bao nhiêu.

```bash
rtk init -g                 # bật hook cho tool của bạn
git status                  # output thô, để đối chiếu
rtk git status              # output đã nén
rtk gain                    # xem đã tiết kiệm được bao nhiêu
```

**Kiểm tra**

Sau bước 2, `rtk git status` phải cho đúng số file theo từng trạng thái (đã sửa, chưa theo dõi…) như bản thô, chỉ khác ở chỗ gọn hơn. Sau bước 4, `rtk gain` phải báo `Reduction` khác 0 — nếu vẫn là 0% thì hook chưa ăn, xem lại Q1 ở phần `05-troubleshooting`.

---

### Q14. Agent cứ gọi `git status` rồi `cargo test`, mỗi lần ăn hết context của tôi — nên dùng pattern nào? [→ § Pattern Picker]

**Bạn sẽ thấy**

Bạn mở log của một phiên làm việc và thấy agent đọc `git status` (dài), `git log -n 10` (dài), `cargo test` (hàng trăm dòng), `cat` một file 800 dòng — rồi hết token. Bạn không biết vì sao bốn thứ đó lại đáng quan tâm hơn ba thứ khác, và cũng không biết bắt đầu từ đâu.

**Vì sao**

Vì "ngốn context" có nhiều kiểu khác nhau, và mỗi kiểu cần một cách nén khác nhau. README có sẵn một cây quyết định, chọn theo câu hỏi: nếu đau vì git thì Git Speedup; đau vì test output thì Test Only Failures; đau vì agent đọc cả file lớn thì File Smart Read; đau vì build/lint dài dòng thì Build & Lint Compact. Nếu đau vì cả bốn thì không cần tự chọn nữa.

**Làm gì**

1. Đọc cây quyết định trong README và tự trả lời "cái nào đang đau nhất lúc này", chọn đúng một nhánh.
2. Nếu bạn dùng cả bốn, cài hook toàn cục `rtk init -g` — RTK tự định tuyến theo từng lệnh, agent không cần gọi thủ công.
3. Nếu bạn loạn vì cái nào cũng "High" token cost, hãy bắt đầu từ Test Only Failures: nó giảm mạnh nhất (~90%) vì pass tests bị gom thành một con số.
4. Ghép pattern thì không phải lo xung đột: `rtk read` cho file, `rtk git` cho git, hai cái chạy song song không tranh nhau.

```bash
rtk init -g        # áp dụng tất cả pattern, không cần gọi tay
```

**Kiểm tra**

Sau khi bật hook, gọi `git status` (không gõ `rtk`) vẫn ra output đã nén — nghĩa là đường đi qua hook đã đúng. Chạy `rtk gain` sau một ngày làm việc: nếu `Reduction` vẫn dưới 50% thì agent đang chạy lệnh bị loại trong `exclude_commands`, cần xem lại cấu hình.

---

### Q15. Tôi có ít token, CI đang đỏ, repo mới vào lạ — bật gì, và cái gì nên tránh? [→ § Cost-aware Picks]

**Bạn sẽ thấy**

Bạn đang cần tiết kiệm từng token, đồng thời phải tìm ra test nào fail để sửa, và đồng thời cần hiểu một repo vài chục nghìn dòng. Ba việc đó đè lên ba pattern khác nhau. Nếu bật hết một lượt thì tốn kém cấu hình, nếu chọn sai thì tốn token vô ích.

**Vì sao**

Vì mỗi pattern phục vụ một loại đau khác nhau, và README có sẵn bảng ghép tình huống với lựa chọn nên dùng và thứ nên tránh. Nguyên tắc là: khi CI đỏ, thứ giúp bạn tiết kiệm token phải là thứ giúp bạn *tìm ra lỗi*, chứ không phải thứ chạy cho tròn.

**Làm gì**

1. Token eo hẹp → chọn Git Speedup cho `git push`/`git status` (giảm ~70–93%), và **tránh** bật Test Only Failures cho mọi lần chạy — bản thân việc rút gọn cũng tốn token.
2. CI đang đỏ → Test Only Failures là lựa chọn đúng, và **tránh** để agent xem full test output mỗi lần.
3. Repo lớn, ít quen thuộc → File Smart Read, và **tránh** `cat` toàn bộ file; dùng `rtk find` + `rtk grep` để lần theo.
4. Build chạy thường xuyên → Build & Lint Compact, thay vì giữ nguyên output chi tiết.

```bash
rtk read src/harness/loop.rs       # xem cấu trúc, không phải toàn bộ nội dung
rtk grep "handleToolCall" .        # tìm chỗ cần sửa
rtk cargo test                     # chỉ còn failure
```

**Kiểm tra**

Chạy `rtk discover` sau vài ngày: lệnh nào có `0% reduction` mà bạn vẫn hay dùng thì đó chính là khoản tiết kiệm còn bỏ sót. Nếu `Commands run` không tăng dù bạn làm việc nhiều, hook chưa bắt — kiểm tra lại `rtk init -g`.

---

## 03-patterns/git-speedup.md

### Q13. `git push` của tôc in ra 15 dòng, RTK gom còn đúng `ok main` — có mất thông tin gì không? [→ § Ví Dụ Thực Tế]

**Bạn sẽ thấy**

Bản thô dài 15 dòng và đầy những dòng như `Enumerating objects: 5, done.`, `Counting objects: 100% (5/5), done.`, `Delta compression using up to 8 threads`. Bản RTK chỉ còn một dòng `ok main`. Đối với `git add` và `git commit` thì gần như triệt tiêu: `git add` chỉ còn `ok`, `git commit` còn `ok abc1234` — giảm khoảng 95%.

**Vì sao**

Vì những dòng đó là tiến trình của git kể cho bạn nghe, không phải kết quả. Bạn không cần biết git nén delta bằng bao nhiêu luồng để biết việc đẩy lên nhánh `main` đã xong. Pattern này nén tới ~93% cho `git push`, ~90% cho `git pull` (ra `ok 3 files +10 -2`), nên ngay cả output nén vẫn giữ lại đủ thông tin dùng được.

**Làm gì**

1. Chấp nhận bản nén cho các thao tác xác nhận kết quả: add, commit, push, pull. Đây là chỗ lợi rõ nhất.
2. Nếu bạn cần kiểm tra cụ thể sau khi push, đừng đoán từ `ok main` — chạy lệnh kiểm tra riêng (`git status`, `git log -n 1`).
3. Với `git pull`, đọc kỹ phần `3 files +10 -2`: đây là thông tin duy nhất bạn cần để quyết định có xem diff hay không.
4. Nếu một script của bạn phụ thuộc định dạng gốc, đừng đoán — thêm lệnh vào `exclude_commands` trong `config.toml`.

```bash
rtk git add .
rtk git commit -m "fix: đổi timeout mặc định"
rtk git push
# ok main
```

**Kiểm tra**

Sau khi push, `git status` phải báo sạch (không còn nhánh chưa đẩy). Nếu bản nén báo `ok` nhưng trạng thái thật khác, hãy thêm `git push` vào `exclude_commands` rồi thử lại — đó là bằng chứng nén đang bỏ sót thông tin quan trọng.

---

### Q14. Agent cần xem diff chi tiết để sửa đúng một chỗ, nhưng `git diff` bị nén lại — làm sao? [→ § Lưu Ý]

**Bạn sẽ thấy**

Agent nói "tôi cần diff đầy đủ" nhưng lệnh `git diff` trả về bản rút gọn: context bị giảm, phần header bị bỏ. Mức giảm là khoảng 75%. Nếu có pipeline kiểu `git diff | grep foo` thì định dạng nén làm kết quả tìm kiếm không còn đúng.

**Vì sao**

Vì `rtk git diff` cố tình bỏ phần không cần thiết để agent nhìn thấy phần thay đổi nhanh hơn, nhưng đó là đánh đổi một chiều. Nhưng RTK hoạt động ở tầng hook, nghĩa là bạn luôn có đường vòng: gọi lệnh gốc, hoặc loại lệnh đó ra khỏi danh sách bị nén.

**Làm gì**

1. Khi cần diff đầy đủ, cho agent gọi `git diff` trực tiếp, không đi qua tiền tố `rtk`.
2. Nếu muốn cả phiên đều có diff thô, thêm `git diff` vào `exclude_commands` trong `~/.config/rtk/config.toml` — đừng tắt cả hook.
3. Với pipeline `| grep`, hãy kiểm tra lại trước khi tin kết quả: định dạng nén có thể làm từ khoá nằm ngoài đoạn đã giữ.
4. Nhớ nguyên tắc vàng của RTK: việc rewrite là trong suốt, nên loại lệnh riêng luôn an toàn hơn tắt tổng.

```toml
# ~/.config/rtk/config.toml
[hooks]
exclude_commands = ["git diff", "git diff --stat"]
```

**Kiểm tra**

Chạy `git diff` sau khi thêm `exclude_commands`: phải ra đầy đủ cả phần context 3 dòng trước và sau mỗi khối thay đổi. Nếu vẫn bị nén, bạn có thể đã sửa sai file cấu hình hoặc chưa restart lại AI tool.

---

### Q15. `git status`, `git log`, `git diff`, `git add`, `git commit`, `git push`, `git pull` — mỗi cái giảm bao nhiêu? [→ § Lệnh & Mức Giảm]

**Bạn sẽ thấy**

Bảng dưới đây là con số bạn có thể dùng để ước lượng trước khi bật. Chênh lệch rất lớn giữa các lệnh: `git add` giảm ~95%, còn `git log -n 10` chỉ giảm ~70% vì phải giữ lại hash, tên tác giả và tiêu đề commit.

| Lệnh gốc | Lệnh RTK | Còn lại | Giảm |
|---|---|---|---|
| `git status` | `rtk git status` | thống kê gọn, gom theo trạng thái | ~80% |
| `git log -n 10` | `rtk git log -n 10` | hash + tác giả + tiêu đề | ~70% |

**Vì sao**

Vì mức giảm phụ thuộc vào lệnh gốc xuất ra nhiều "phần tử rác" đến mức nào. Lệnh chỉ cần báo một sự kiện thì nén gần như tuyệt đối; lệnh phải mang cả ngữ cảnh thì phần giữ lại lớn hơn, nên phần trăm giảm thấp hơn — nhưng số dòng thực tế vẫn giảm rõ.

**Làm gì**

1. Bật Git Speedup trước vì nó áp dụng cho cả 7 lệnh này, không cần chọn lệnh nào.
2. Dùng `git add`, `git commit`, `git push` là nơi lợi nhất — gần 95% output là thông tin thừa với bạn.
3. Với `git log`, hãy giữ tham số `-n 10` thay vì để git in ra cả lịch sử.
4. Nếu muốn biết chính xác trên repo của bạn, chạy `rtk gain --history` để xem lệnh nào đã bị nén và tiết kiệm bao nhiêu.

**Kiểm tra**

Đối chiếu một lệnh bất kỳ: đếm số dòng output thô, rồi đếm số dòng bản RTK, tính tỉ lệ giảm theo công thức `(thô − nén) / thô`. Con số phải nằm gần vùng 70–95% trong bảng. Lệnh nào lệch xa thì kiểm tra xem nó có nằm trong `exclude_commands` không.

---

## 03-patterns/build-lint-compact.md

### Q13. `tsc` in ra hàng trăm dòng `error TS2322`, `error TS2554` — làm sao cho agent thấy đúng chỗ đang hỏng? [→ § Ví Dụ Thực Tế]

**Bạn sẽ thấy**

Bản thô lặp đi lặp lại cặp thông tin: `src/harness/context.ts(42,9):` rồi dòng dưới là `error TS2322: Type 'string' ...`; tiếp `src/harness/loop.ts(18,5):` rồi `error TS2554: Expected 2 args ...`. Bản RTK gộp lại: tên file một lần, rồi `L42  TS2322  Type mismatch` ngay bên dưới.

**Vì sao**

Vì định dạng thô của trình kiểm tra kiểu (type-checker) tốn nhiều dòng cho thông tin lặp lại: mỗi lỗi lại phải nhắc lại tên file. Gom theo file thì mỗi tên file chỉ xuất hiện một lần, còn mã lỗi và dòng vẫn giữ nguyên — nên vẫn sửa được mà ngắn hơn khoảng 85%.

**Làm gì**

1. Dùng `rtk tsc` thay cho `tsc` khi bạn chỉ cần biết "có lỗi ở đâu", không cần lời giải thích dài của compiler.
2. Với Rust, dùng `rtk cargo build` (~80%) và `rtk cargo clippy` (~80%).
3. Với các linter khác: `rtk lint` cho `eslint` (gom theo rule/file), `rtk ruff check` và `rtk golangci-lint run` (ra JSON, ~80–85%).
4. Nếu bạn cần nguyên văn thông điệp gốc của compiler để tra cứu, gọi `tsc` trực tiếp.

```bash
rtk tsc
# src/harness/context.ts
#   L42  TS2322  Type mismatch
# src/harness/loop.ts
#   L18  TS2554  Expected 2 args
```

**Kiểm tra**

Đếm số lỗi trong cả hai bản: phải bằng nhau, chỉ khác cách trình bày. Sau đó mở đúng `L42` trong `src/harness/context.ts` và xem lỗi có thật không — nếu dòng trong bản nén lệch, đó là tín hiệu formatter bị bỏ sót.

---

### Q14. `ruff`, `rubocop`, `golangci-lint` cần JSON mới chạy được — RTK có cần tôi cấu hình gì không? [→ § Lưu Ý]

**Bạn sẽ thấy**

Ba linter này mặc định in ra JSON, không phải văn bản cho người đọc. Nếu RTK không đọc đúng định dạng, nó sẽ không gom được gì và bạn thấy output vẫn dài như cũ. Với `rspec` (framework test của Ruby) cũng vậy — nó chỉ giảm khoảng 60% vì còn phần pass, và cần `rspec` đã cấu hình formatter.

**Vì sao**

Vì RTK parse output rồi mới nén. Nó phải nói đúng ngôn ngữ với công cụ bên dưới, và với vài công cụ ngôn ngữ đó là JSON. Đây không phải lỗi RTK — đây là điều kiện để lọc hoạt động.

**Làm gì**

1. Bảo đảm linter thật sự xuất JSON. Nếu không, hãy chuyển sang định dạng JSON trước khi chạy.
2. Với `rspec`, kiểm tra đã bật formatter JSON chưa; không có thì RTK chỉ nén được phần dễ nén.
3. Cài `rg` (ripgrep): một số bộ lọc của RTK gọi tới nó. Thiếu `rg` thì gặp lỗi `Binary 'rg' not found on PATH`.
4. Với `next build`: lệnh này có nhiều giai đoạn, RTK giữ lại log ở các bước quan trọng khi build fail — đừng ngạc nhiên vì output không đều.

```bash
brew install ripgrep          # macOS
winget install BurntSushi.ripgrep.MSVC   # Windows
ruff check --format json .    # đảm bảo linter xuất JSON
```

**Kiểm tra**

Chạy `ruff check` qua RTK và kiểm tra output có đúng là JSON đã gom theo rule và file. Chạy `rtk gain --history` xem lệnh này có bằng 0% reduction không; nếu có, hãy chuyển formatter sang JSON rồi thử lại.

---

### Q15. Mức giảm của build và lint khác nhau ra sao, pattern này dùng cho công cụ nào? [→ § Lệnh & Mức Giảm]

**Bạn sẽ thấy**

Các mức giảm trong nhóm này không đều nhau, và đều dưới mức ~90% mà bạn có ở nhóm test. `rubocop` thấp nhất (~60%+), còn `tsc`, `golangci-lint` cao nhất (~85%). Mức trung bình của cả nhóm là khoảng 75–85%.

| Lệnh gốc | Lệnh RTK | Còn lại | Giảm |
|---|---|---|---|
| `rubocop` | `rtk rubocop` | JSON | ~60%+ |
| `next build` | `rtk next build` | bản nén | ~75% |
| `tsc` | `rtk tsc` | lỗi TS gom theo file | ~85% |

**Vì sao**

Vì lượng "nhiễu" trong output build khác nhau. Lint thường có hàng trăm dòng cảnh báo lặp lại cùng một rule nên nén được nhiều; `next build` có log nhiều giai đoạn nên phần phải giữ lại lớn hơn; `rubocop` ra JSON nên mật độ thông tin trong mỗi dòng đã cao hơn, cắt khó hơn.

**Làm gì**

1. Bật nhóm này khi build hoặc lint chạy thường xuyên, và khi CI đỏ vì lỗi compile/lint.
2. Cũng nên bật khi bạn vừa sửa code xong và muốn biết có gì hỏng mà không cần đọc log dài.
3. Ưu tiên `rtk tsc` và `rtk golangci-lint run` vì giảm mạnh nhất.
4. Đừng kỳ vọng mức ~90% ở đây; nếu bạn cần nén mạnh hơn hãy ghép với Test Only Failures cho phần test.

```bash
rtk cargo build
rtk cargo clippy
rtk tsc
rtk lint
rtk prettier --check .   # chỉ còn file cần format, ~75%
rtk sbt compile         # chỉ còn lỗi biên dịch, ~75%
```

**Kiểm tra**

Với mỗi công cụ, đếm số lỗi/cảnh báo thật trong cả hai bản — phải khớp. Sau đó mở CI lần chạy thật gần nhất và xem log có ngắn lại không; nếu log CI không đổi, thì CI chưa đi qua hook.

---

## 03-patterns/file-smart-read.md

### Q13. File 1.240 dòng, agent `cat` hết chỉ để tìm một hàm — `rtk read` cho tôi thấy cái gì? [→ § Ví Dụ Thực Tế]

**Bạn sẽ thấy**

`cat` một file Rust 1.240 dòng trả về đúng 1.240 dòng, và agent phải đọc hết chúng chỉ để biết cấu trúc. Chạy `rtk read file.rs -l aggressive` thì nhận được dòng tiêu đề `File: src/harness/context.rs (1,240 lines)` kèm chữ ký và vị trí:

```text
File: src/harness/context.rs (1,240 lines)
  pub struct ContextManager            // L42
    fn build(&mut self, ctx: Ctx)      // L45
    fn compress(&self) -> Result       // L210
    fn limit(&self) -> TokenBudget     // L390
```

**Vì sao**

Vì phần agent cần lúc đầu thường chỉ là "file này có gì, hàm nào nằm ở dòng nào". Thân hàm thì chưa cần đọc ngay. Đây chính là ý tưởng chỉ đưa phần cần thiết vào ngữ cảnh — cùng cách lấy chữ ký hàm trong module `02-build-context` của harness. Mức giảm ở chế độ aggressive là hơn 90%.

**Làm gì**

1. Cho agent chạy `rtk read <file>` để nắm cấu trúc trước, rồi mới đọc chi tiết đúng vùng cần sửa.
2. Dùng `-l aggressive` khi file rất lớn và bạn chỉ cần bản đồ hàm.
3. Muốn tìm nhanh hơn nữa: `rtk find "*.rs" .` (~70%), `rtk grep "pattern" .` (~75%) và `rtk smart file.rs` — cho tóm tắt heuristic 2 dòng (~95%).
4. Đừng dùng `rtk diff` để so sánh file khi bạn cần nội dung: lệnh đó ra diff rút gọn (~75%), và thoát với mã 1 nếu hai file khác nhau.

**Kiểm tra**

Sau khi có danh sách chữ ký, thử mở đúng dòng được ghi kèm (ví dụ `L210`) bằng `cat` thường: nội dung phải khớp với tên hàm. Nếu lệch dòng, báo đó là lỗi trích xuất chữ ký chứ không phải lỗi của bạn.

---

### Q14. Dùng `-l aggressive` có an toàn không — tôi cần sửa đúng một dòng cụ thể thì sao? [→ § Lưu Ý]

**Bạn sẽ thấy**

Bạn yên tâm khi thấy output gọn gàng, rồi bảo agent "sửa dòng đó giúp tôi". Vấn đề: `rtk read` trả về **cấu trúc**, không phải nội dung đầy đủ, và ở chế độ aggressive thân hàm bị bỏ hẳn. Agent không nhìn thấy nội dung thật của dòng cần sửa.

**Vì sao**

Vì đây là đánh đổi có chủ đích: bỏ thân hàm để tiết kiệm hơn 90%, đổi lại mất thứ bạn cần đúng lúc sửa. README nói rõ `rtk read` không tương đương `cat`, và khi cần nội dung chính xác thì vẫn phải dùng `cat` hoặc công cụ đọc file trực tiếp.

**Làm gì**

1. Đừng cấm `-l aggressive` — chỉ đừng dùng nó cho việc sửa code.
2. Để agent gọi `cat` hoặc `read_file` trực tiếp khi đã biết cần sửa dòng nào, rồi mới quay lại `rtk read` để kiểm tra không phá vỡ chữ ký.
3. Nếu muốn chắc chắn hơn nữa, thêm các lệnh `cat`/`sed` vào `exclude_commands` — tuy nhiên cách này bỏ lỡ phần tiết kiệm lớn nhất của pattern.
4. Nhớ nguyên tắc: pattern này hiện thực hoá kỹ thuật trích xuất chữ ký hàm — tức là công cụ *tìm hiểu*, không phải công cụ *sửa*.

```bash
rtk read src/harness/context.rs -l aggressive  # xem bản đồ
cat src/harness/context.rs | sed -n '205,215p'  # xem đúng vùng cần sửa
```

**Kiểm tra**

Sau khi sửa, chạy `rtk read <file>` lại: danh sách chữ ký phải không đổi trừ khi bạn cố ý đổi chữ ký. Nếu một hàm biến mất khỏi danh sách, hãy xem lại thay đổi của bạn.

---

### Q15. Một file nén được bao nhiêu, và các lệnh tìm kiếm đi kèm thì sao? [→ § Lệnh & Mức Giảm]

**Bạn sẽ thấy**

Các mức giảm trong nhóm đọc file trải rộng từ ~60% đến hơn 95%. Cùng một lệnh `cat` nhưng chế độ khác nhau cho kết quả rất khác: `rtk read` khoảng 60–90%, thêm `-l aggressive` thì hơn 90%.

| Lệnh gốc | Lệnh RTK | Còn lại | Giảm |
|---|---|---|---|
| `cat file.rs` | `rtk read file.rs` | chữ ký + cấu trúc | ~60–90% |
| `cat file.rs` | `rtk read file.rs -l aggressive` | chỉ chữ ký, bỏ thân | ~90%+ |
| `head file.rs` | `rtk smart file.rs` | tóm tắt 2 dòng | ~95% |
| `find` | `rtk find "*.rs" .` | kết quả gọn | ~70% |

**Vì sao**

Vì mức giảm phụ thuộc bạn hỏi câu nào. `rtk smart` chỉ trả lời "file này làm gì" nên phải bỏ gần hết nội dung — đó là ~95%. Còn `rtk read` bình thường còn giữ một phần thân hàm nên ở mức thấp hơn. Biết câu nào cần câu nào là cách tiết kiệm đúng chỗ, không phải cứ nén mạnh là tốt.

**Làm gì**

1. Chọn chế độ theo mục đích: đang tìm hiểu thì aggressive; đang chuẩn bị sửa thì chế độ thường.
2. Ghép ba lệnh cho một lượt khám phá repo: `rtk find` → `rtk grep` → `rtk read` (hoặc `rtk smart` nếu chỉ cần bản tóm tắt).
3. So sánh file bằng `rtk diff file1 file2` (~75%); nhớ mã thoát là 1 khi hai file khác nhau, nên đừng bảo shell `&&` chạy tiếp một lệnh sau đó.
4. Khi mọi thứ đã xong, mở file thật bằng `cat` để có nội dung đầy đủ.

**Kiểm tra**

Chạy `rtk gain --history` và tìm các lệnh `read`/`find`/`grep` của bạn — nếu đang làm việc trong repo có file 1000+ dòng mà `Reduction` dưới 50%, nghĩa là agent vẫn đang đọc file bằng `cat` thay vì qua RTK.

---

## 03-patterns/test-only-failures.md

### Q13. Test fail, agent lạc trong 200 dòng `... ok` — RTK gom lại thế nào? [→ § Ví Dụ Thực Tế]

**Bạn sẽ thấy**

Bản thô của `cargo test` lúc fail dài hơn 200 dòng: `running 15 tests`, rồi hàng loạt `test utils::test_parse ... ok`, `test utils::test_format ... ok`. Bản RTK còn khoảng 20 dòng, đầu là `FAILED: 2/15 tests`, tiếp là tên test lỗi và chỗ panic: `test_edge_case: assertion failed`, `test_overflow: panic at utils.rs:18`.

**Vì sao**

Vì phần lớn output của một lần chạy test là những dòng báo *thành công* — chúng xác nhận thứ không cần sửa. Gom chúng thành một con số giữ nguyên thông tin quan trọng (2/15 fail) và bỏ hết phần thừa, nên mức giảm đạt khoảng 90% trên cả `cargo test`, `npm test`, `pytest`, `go test`, `jest`, `vitest`, và lệnh tổng quát `rtk test <cmd>`.

**Làm gì**

1. Chạy test bình thường khi đang debug, hoặc khi bạn chỉ muốn biết có bao nhiêu test fail.
2. Để ý hai dòng đầu tiên của output RTK: tỉ lệ fail và danh sách tên test lỗi. Đó là bản đồ để bắt đầu.
3. Với `go test`, RTK parse NDJSON (mỗi dòng một đối tượng JSON) rồi chỉ giữ failure. Với `pytest`, traceback được cắt bớt.
4. Với `rspec` mức giảm chỉ ~60% vì phần pass vẫn còn, nên cần `rspec` bật formatter JSON trước.

```bash
rtk cargo test
# FAILED: 2/15 tests
#   test_edge_case: assertion failed
#   test_overflow: panic at utils.rs:18
```

**Kiểm tra**

So số lượng test fail giữa bản thô và bản RTK — phải khớp. Nếu bản RTK báo `FAILED: 0/15` trong khi CI đỏ, hãy chạy `rtk gain --history` xem lệnh test có bị nén trước hay không.

---

### Q14. Bản tóm tắt chỉ 20 dòng, tôi cần xem log gốc — đọc ở đâu? [→ § Khi lệnh fail, RTK lưu toàn bộ output thô]

**Bạn sẽ thấy**

Khi lệnh fail, RTK in thêm hai dòng:

```text
FAILED: 2/15 tests
[full output: ~/.local/share/rtk/tee/1707753600_cargo_test.log]
```

Đường dẫn đó trỏ tới một file log trên máy bạn chứa **toàn bộ** output thô của lần chạy đó. Bạn không cần chạy lại test (cũng không nên, vì mỗi lần chạy lại là một lần tốn token và thời gian).

**Vì sao**

Vì nén và lưu giữ là hai việc khác nhau: bản nén dùng để agent đọc nhanh, bản gốc dùng để xác minh. Người chọn chính sách là người duyệt nên phải có đường quay lại bản gốc trước khi hành động — đây là cùng ý với cơ chế guardrail của harness.

**Làm gì**

1. Khi output RTK chỉ nói "còn N dòng nữa" hoặc trỏ đường dẫn file log, hãy đọc file log đó trực tiếp thay vì chạy lại lệnh.
2. Chỉ đọc phần liên quan (test nào fail, stack trace của nó) — không cần đọc cả log.
3. Đây cũng là cách giải quyết tình huống output quan trọng bị nén quá: xem log gốc của lần chạy đó, rồi thêm lệnh vào `exclude_commands` nếu tình trạng lặp lại.
4. Nhớ tên file log có dấu thời gian ở đầu tên (`1707753600`), nên các lần chạy khác nhau không ghi đè lẫn nhau.

```bash
cat ~/.local/share/rtk/tee/1707753600_cargo_test.log | grep -A 20 "test_overflow"
```

**Kiểm tra**

Mở file log được in ra và tìm lại đúng dòng `test_overflow: panic at utils.rs:18` mà bản nén đã hiện. Nếu có, cơ chế tee đang hoạt động và bạn có thể tin bản tóm tắt.

---

### Q15. Test fail một lần rồi tôi bảo agent sửa — có nên tin không? [→ § Lưu Ý]

**Bạn sẽ thấy**

Bạn chạy test, một test fail, agent nhảy ngay vào sửa. Rồi test vẫn fail với lý do khác, và bạn đã mất hai vòng lặp. Đây là tình huống rất phổ biến với test không ổn định — flaky test: chạy lần này fail, chạy lần sau pass, không có thay đổi code nào.

**Vì sao**

Vì pattern này chỉ giúp bạn **thấy** failure nhanh hơn, chứ không quyết định cái gì đúng/sai. Quyết định sửa vẫn thuộc về bạn hoặc agent, theo đúng nguyên tắc feedback loop có guardrail: một lần đỏ chưa đủ bằng chứng.

**Làm gì**

1. Đừng auto-sửa chỉ dựa trên một lần fail. Hãy chạy lại đúng test đó một lần nữa trước.
2. Khi cần chạy lại mà không muốn lãng phí token, dùng bản log gốc đã lưu để so sánh thay đổi giữa hai lần chạy.
3. Nếu hai lần chạy cho kết quả khác nhau, coi đó là dấu hiệu flaky — đừng sửa code cho tới khi hiểu vì sao không ổn định.
4. Nếu nghi ngờ regression do một thay đổi của bạn, dùng `rtk test <cmd>` để lấy danh sách fail gọn, rồi đối chiếu với log thô.

```bash
rtk cargo test test_overflow     # lần 1
rtk cargo test test_overflow     # lần 2 — kết quả khác thì là flaky
```

**Kiểm tra**

Trước khi cho phép sửa, hãy chạy lại test đó ít nhất một lần nữa và xác nhận fail lặp lại đúng chỗ. Nếu lần chạy thứ hai pass, hãy ghi lại là flaky và chuyển sang test khác thay vì sửa mù.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: 03-patterns/*.md, 03-patterns/*.md, 03-patterns/*.md, 03-patterns/*.md, 03-patterns/*.md.*
