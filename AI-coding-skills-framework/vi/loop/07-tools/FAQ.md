# ❓ FAQ — Bộ công cụ CLI cho loop (tạo mới, chấm điểm, ước chi phí, chặn an toàn)

Nếu câu hỏi chưa rõ, đọc phần được nêu trong ngoặc vuông.

Từ viết tắt dùng trong file: **CLI** = chương trình chạy bằng dòng lệnh; **MCP** = cách để agent đọc dữ liệu của công cụ ngoài (ở đây là tài liệu của loop); **denylist / allowlist** = danh sách cấm / danh sách được phép; **git worktree** = một bản sao riêng của repo để thử sửa mà không đụng code chính.

---

## Q1. Mới bắt đầu thì tự dựng loop bằng tay hay dùng CLI có sẵn? [→ §1 Front Door]

**Bạn sẽ thấy**

Bạn mở repo lúc 9 giờ sáng, muốn thử một loop triage hằng ngày, và bốn lựa chọn hiện ra trong đầu: tự tạo skill, tự tạo file state, tự viết file ngân sách, tự làm lịch chạy. Sau một buổi sáng, bạn có một loop chạy được nhưng không biết mình đã bỏ sót phần nào.

**Vì sao**

Loop không chỉ là một câu lệnh agent. Nó gồm ít nhất năm khối: tự động hoá (lịch chạy), worktree, skill, kết nối công cụ, sub-agent và state. Dựng tay nghĩa là bạn phải tự nhớ đủ các thành phần đó — và sai sót thường nằm đúng ở phần an toàn.

**Làm gì**

1. Bắt đầu từ cửa chính (front door): một lệnh làm cả ba việc khởi tạo, khám sức khoẻ, xem trạng thái.
2. Truyền sẵn pattern và công cụ agent bạn dùng.
3. Chạy `doctor` ngay sau đó, làm theo đúng 3 việc nó liệt kê.
4. Chỉ thêm harness có phiên bản (`--with-foundry`) khi loop đã thật sự chạy ổn.
5. `loop-init` cũ vẫn chạy được, nên repo cũ không phải đổi.

```
npx @cobusgreyling/loop init . --pattern daily-triage --tool grok
npx @cobusgreyling/loop doctor .
npx @cobusgreyling/loop init . --pattern daily-triage --tool claude --with-foundry
```

**Kiểm tra**

Lệnh `init` phải in ra điểm sẵn sàng (Loop Ready score) và câu lệnh loop đầu tiên để chạy. Sau đó `doctor` phải ra đúng 3 việc tiếp theo, không phải danh sách 20 việc.

---

## Q2. Điểm Loop Ready của tôi 12/100 — làm sao lên 80? [→ §2 loop-audit]

**Bạn sẽ thấy**

Một con số chạy từ khoảng 10 lên 100 khi bạn dựng đủ các phần. Ngay cả khi bạn đã có đầy đủ kỹ năng và state, điểm vẫn bị chặn ở mức L3 (chạy không cần người canh) cho tới khi có đủ ba thứ mà điểm ngưỡng không báo rõ.

**Vì sao**

`audit` chấm điểm theo các ràng buộc vận hành, quản trị và môi trường chạy (Harness Runtime, bản v1.7). Riêng phần L3 được giới hạn cứng: chỉ mở khi đã có `loop-budget.md`, `loop-run-log.md`, và một phần ngân sách trong `LOOP.md`.

**Làm gì**

1. Chạy audit kèm gợi ý sửa, để có danh sách việc cụ thể.
2. Tạo `loop-budget.md` với hạn mức token theo ngày và điều kiện dừng.
3. Bắt đầu ghi `loop-run-log.md` ngay từ lần chạy đầu, append mỗi lần.
4. Thêm phần ngân sách vào `LOOP.md` — đây là điều kiện thứ ba, hay bị bỏ sót nhất.
5. Chỉ nghĩ tới bước 80+ sau khi chạy thật ở mức L1 một tuần.

```
npx @cobusgreyling/loop audit . --suggest
# Nếu audit recommend Foundry: score mạnh nhưng thiếu .foundry/stack.yaml
```

**Kiểm tra**

Chạy lại audit sau mỗi lần thêm một file. Điểm phải tăng theo từng bước, và mức L3 chỉ mở khi cả ba điều kiện trên cùng tồn tại.

---

## Q3. Cho loop chạy ci-sweeper mỗi 15 phút ở mức L2 — tốn bao nhiêu tiền? [→ §3 loop-cost]

**Bạn sẽ thấy**

Bạn sắp đặt lịch một loop quét CI (hệ thống kiểm tra tự động) chạy mỗi 15 phút ở mức L2 (có người duyệt), và bạn không có cách nào biết trước hóa đơn cuối tuần. Đây là lúc nhiều người bị sốc: một tháng sau mới thấy con số.

**Vì sao**

Mỗi lần chạy là một chuỗi sub-agent, mỗi sub-agent đọc log CI, diff, và trạng thái. Nhân với 96 lần chạy mỗi ngày thì sai số nhỏ cũng thành con số lớn. Yếu tố khuếch đại lớn nhất là lịch chạy dưới một phút và việc retry lại cả dây chuyền khi gặp lỗi mạng tạm thời.

**Làm gì**

1. Chạy công cụ ước tính chi phí trước khi đặt lịch, truyền đúng pattern, nhịp chạy và mức.
2. Chạy thử ở mức L1 một tuần để lấy số thực tế, rồi nhân lên.
3. Đặt hạn mức token theo ngày; vượt hạn mức thì loop tự tạm dừng.
4. Cho lượt triage rẻ tiền chạy trước; danh sách rỗng thì không vào chuỗi agent đầy đủ.
5. Dùng công cụ quản lý ngữ cảnh khi phiên chạy dài, kèm ngưỡng ngắt mạch bảo vệ.

```
npx @cobusgreyling/loop cost --pattern ci-sweeper --cadence 15m --level L2
npx @cobusgreyling/loop context --check --ledger run.json
```

**Kiểm tra**

Số ước tính phải khớp với hóa đơn tuần đầu trong khoảng 30%. Nếu lệch, hãy xem lại nhịp chạy và số lần retry trước khi tăng nhịp.

---

## Q4. `STATE.md` và `LOOP.md` lệch nhau, loop cứ làm theo file sai — làm sao biết? [→ §4 loop-sync + §5 loop-context]

**Bạn sẽ thấy**

Bạn sửa tay `LOOP.md` để giảm nhịp chạy và thêm một mức kiểm chứng, nhưng `STATE.md` vẫn mô tả cấu hình cũ. Loop đọc hai file này ở hai chỗ khác nhau và chạy theo bản sai. Triệu chứng điển hình là bạn đã giảm nhịp nhưng hóa đơn không giảm.

**Vì sao**

Hai file phục vụ hai vai trò khác nhau: một file là cấu hình, một file là trạng thái, và theo thời gian chúng lệch nhau. Nếu không có bước phát hiện lệch (drift detection), bạn chỉ biết khi hóa đơn hoặc sự cố tới nơi.

**Làm gì**

1. Chạy phát hiện lệch trước mỗi lần đổi cấu hình.
2. Ghi thời điểm chạy gần nhất vào state để biết dữ liệu có cũ không.
3. Dùng công cụ quản lý bối cảnh cho phiên chạy dài, để ngữ cảnh không phình vô hạn qua nhiều vòng lặp.
4. Canh ngữ cảnh với một ngưỡng ngắt mạch: quá ngưỡng thì dừng và chuyển người.
5. Cấu hình sửa xong thì cập nhật cả hai file trong cùng một lần commit.

```
npx @cobusgreyling/loop sync .
npx @cobusgreyling/loop context --check --ledger run.json
```

**Kiểm tra**

Cố tình đổi `LOOP.md` mà không đụng `STATE.md`, chạy `sync` phải báo lệch và nêu đúng dòng nào lệch.

---

## Q5. Loop tự gộp code chạm file cấm — chặn bằng cách nào mà không phải "hy vọng nó đọc file an toàn"? [→ §6 loop-worktree, §7 loop-gate, §8 loop-sandbox / loop-swarm]

**Bạn sẽ thấy**

Loop tự gộp thay đổi vào nhánh chính, chạm vào file nằm trong danh sách cấm. Nếu chỉ dựa vào prompt bảo "đừng chạm file này" thì chỉ cần một lần quên là xong. Bạn cần lớp chặn không phụ thuộc vào việc model có đọc đúng hay không.

**Vì sao**

Chỉ dẫn bằng văn bản là điều khoản ước tính, còn lệnh thoát ra (exit code) là điều khoản bắt buộc. Nguyên tắc ở đây rất đơn giản: những gì con người hay lơi (nối khoá, chặn danh sách cấm) thì giao cho công cụ cưỡng chế.

**Làm gì**

1. Mỗi lần thử sửa, tạo một worktree riêng; hỏng thì bỏ worktree đó, code chính không bị chạm.
2. Dùng khoá `lock`/`unlock` để hai loop không vào cùng một chỗ.
3. Chạy lệnh `gate check` trước mỗi hành động gộp hoặc tự động hoá, truyền danh sách đường dẫn.
4. Với nhiều agent, yêu cầu bản vá giống hệt nhau byte-for-byte giữa các lần chạy mới chấp nhận.
5. Bắt thay đổi thành file bản vá để người xem đọc được trước khi áp dụng.

```
npx @cobusgreyling/loop-worktree create --run-id <id> --pattern <p>
npx @cobusgreyling/loop gate check --action auto-merge --paths <f1,f2,...>
npx @cobusgreyling/loop-sandbox run -- <cmd>    # exit 2 = chuyển người, 0 = được đi
```

**Kiểm tra**

Đưa một file trong danh sách cấm vào tham số `--paths`: lệnh phải trả về exit 2 và không có thay đổi nào lên nhánh chính. Với hai loop cùng một nhánh, phải thấy khoá worktree thay vì hai thay đổi chồng lên nhau.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: README.md.*