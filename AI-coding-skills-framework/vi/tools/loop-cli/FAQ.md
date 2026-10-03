# ❓ FAQ — Loop CLI (chuyện thật, dễ hiểu)

Câu hỏi nào khó hiểu thì đọc `README.md` phần trong ngoặc vuông.

---

## Q1. Lần đầu cài thì dùng lệnh nào trước? [→ Front Door — `loop init / doctor / status`]

**Bạn sẽ thấy**

Bạn vừa viết xong một hệ thống xử lý tác vụ tự động (harness) và muốn chạy nó như một vòng lặp có kỷ luật. Nhưng mỗi dự án mới bạn lại phải tự tạo các file trạng thái, file ngân sách token, cấu hình an toàn.

**Vì sao**

Vì lệnh đầu tiên là `loop init` — nó tạo sẵn toàn bộ khung. Cụ thể là: các thư mục kỹ năng (skills), file `STATE.md`, file `LOOP.md`, các file ngân sách. Sau đó in ra điểm sẵn sàng của vòng lặp và gợi ý lệnh vòng lặp đầu tiên nên chạy.

**Làm gì**

1. Chạy `loop init` với mẫu vòng lặp bạn cần và tên công cụ AI bạn dùng.
2. Chạy `loop doctor` ngay sau đó — lệnh này gộp kiểm tra toàn bộ và trả về **3 việc nên làm tiếp theo**.
3. Chạy `loop status` bất cứ lúc nào để xem trạng thái hiện tại.
4. Muốn khung nhiều phiên bản hơn thì thêm cờ `--with-foundry`.
5. Nếu đã dùng bản tách riêng cũ (`loop-init`) thì không cần đổi, chúng cho kết quả tương đương.

```bash
npx @cobusgreyling/loop init . --pattern daily-triage --tool grok
npx @cobusgreyling/loop doctor .
npx @cobusgreyling/loop status .
```

**Kiểm tra**

Sau khi chạy `loop init`, thư mục phải có file `STATE.md` và `LOOP.md`. Nếu không, lệnh chạy sai thư mục đích.

---

## Q2. Điểm "Loop Readiness" dùng để làm gì? [→ `loop audit` — Loop Readiness Score]

**Bạn sẽ thấy**

Sau khi khởi tạo, bạn có điểm khoảng 10. Người khác chạy cùng dự án đó có điểm 100.

**Vì sao**

Vì điểm này đo xem vòng lặp của bạn đã đủ nguyên tắc chưa, theo bốn mức từ L0 đến L3. Nó chấm ba phần: các ràng buộc (constraints), cơ chế quản trị (governance), và khả năng chạy thật của hệ thống (Harness Runtime).

Điểm thấp nghĩa là vòng lặp chạy được nhưng chưa có đường lui, chưa có nhật ký, chưa có ngân sách — nghĩa là khi nó đi sai thì bạn không biết nó đi sai từ đâu.

**Làm gì**

1. Chạy `loop audit` với cờ gợi ý để nhận luôn danh sách việc cần làm.
2. Nhớ rằng điểm bị chặn ở mức L3 cho tới khi có đủ ba thứ: file `loop-budget.md`, file `loop-run-log.md`, và phần khai báo ngân sách trong `LOOP.md`.
3. Với cổng chặn ở mức thấp, đừng ép lên L3 bằng cách sửa điểm — hãy bổ sung thiếu thật.
4. Chạy lại sau mỗi lần bổ sung, theo dõi điểm tăng dần.

```bash
npx @cobusgreyling/loop audit . --suggest
```

**Kiểm tra**

Cố tình xoá `loop-run-log.md` rồi chạy lại. Điểm phải tụt và phải nhắc tới đúng file đó — nếu không, phần quản trị chưa thực sự được chấm.

---

## Q3. Agent không đọc file an toàn thì sao? [→ `loop gate` — Cưỡng Chế Cơ Học]

**Bạn sẽ thấy**

Bạn có một file cấu hình an toàn liệt kê những đường dẫn agent không được chạm tới, nhưng đã có lần agent vô tình sửa đúng những file đó.

**Vì sao**

Vì đó là lời hứa bằng văn bản, không phải ràng buộc kỹ thuật. Agent có thể đọc, có thể quên, có thể bỏ qua. Lệnh `loop gate` kiểm tra bằng cơ chế: nó đọc danh sách cấm và danh sách cho phép từ file cấu hình `gate.yaml`, rồi quyết định bằng mã. Không phụ thuộc vào việc agent có chịu đọc file hay không.

Khác biệt này là toàn bộ ý nghĩa của cổng chặn. Vòng lặp không có cổng chặn thì chỉ là một lời đề nghị.

**Làm gì**

1. Tạo file `gate.yaml` liệt kê các đường dẫn cấm và các đường dẫn được phép tự động gộp.
2. Chạy kiểm tra cổng chặn ngay trong quy trình kiểm tra tự động (CI), trước bước gộp.
3. Đọc mã thoát: **2 = cần leo thang**, **0 = được tiếp tục**.
4. Vì dùng chung quy ước mã thoát với lệnh kiểm tra ngữ cảnh, nên hai lệnh này nối tiếp được với nhau trong một chuỗi.

```bash
npx @cobusgreyling/loop gate check --action auto-merge --paths src/,tests/
# exit 2 = escalate, exit 0 = proceed
```

**Kiểm tra**

Chạy cổng chặn với một đường dẫn nằm trong danh sách cấm. Mã thoát phải là 2 và CI phải đỏ. Nếu mã thoát là 0 thì cấu hình chưa được nạp.

---

## Q4. Chạy nhiều vòng lặp song song thì giẫm chân nhau — xử lý sao? [→ `loop worktree`, `loop sandbox`, `loop swarm`]

**Bạn sẽ thấy**

Ba người cùng chạy vòng lặp trong một kho mã. Tất cả đều ghi thẳng vào nhánh chính. Kết quả: lịch sử commit lộn xộn, có phần không ai biết do ai sinh ra, không sửa được.

**Vì sao**

Vì một vòng lặp tự động không biết người khác đang làm gì. Cách chữa bằng công cụ là **cách ly từng lần chạy**: mỗi lần thử có một cây làm việc riêng (git worktree riêng), theo dõi trong một bản ghi, tự dọn khi bị từ chối hoặc khi cần leo thang.

Với phần nhiều agent, công cụ còn yêu cầu các lần chạy phải cho **bản vá giống hệt nhau từng byte** trước khi được chấp nhận. Không giống nhau thì không thỏa thuận được, phải làm lại.

**Làm gì**

1. Mỗi lần thử một worktree, đặt tên theo mã lần chạy và mẫu vòng lặp.
2. Dùng lệnh khoá để nhiều vòng lặp không ghi cùng một nhánh một lúc.
3. Chạy thử trong môi trường tạm và bắt thay đổi thành tệp vá để xem xét trước khi áp dụng.
4. Trước bước gộp, chạy cổng chặn với danh sách đường dẫn cụ thể.
5. Dọn worktree khi lần thử bị từ chối hoặc phải leo thang, không để tích tụ.

```bash
npx @cobusgreyling/loop-worktree create --run-id fix-123 --pattern post-merge-cleanup
npx @cobusgreyling/loop-worktree lock --scope refs/heads/main
npx @cobusgreyling/loop-sandbox run -- <cmd>
```

**Kiểm tra**

Chạy hai vòng lặp cùng lúc trên cùng một nhánh. Lệnh khoá phải khiến vòng lặp thứ hai bị chặn, và nhánh chính phải không nhận commit trực tiếp nào.

---

## Q5. Biết trước vòng lặp này tốn bao nhiêu tiền không? [→ `loop cost` — Ước Lượng Token]

**Bạn sẽ thấy**

Bạn định hẹn một vòng lặp chạy mỗi 15 phút. Một tuần sau hoá đơn tăng vọt mà bạn không biết vì sao.

**Vì sao**

Vì ước lượng từ trải nghiệm gần đúng nhưng không đủ — lệnh `loop cost` ước lượng mức tiêu token **trước khi** bạn hẹn lịch. Nó nhận ba đầu vào: mẫu vòng lặp, tần suất chạy, và mức độ (L2).

Cách so sánh: tạo khung thủ công mất khoảng 30 phút mỗi dự án; `loop init` xong dưới 1 phút.

**Làm gì**

1. Trước khi hẹn lịch, chạy lệnh ước lượng với mẫu, tần suất và mức độ tương ứng.
2. So sánh con số ước lượng với hóa đơn thực tế sau một tuần. Lệch nhiều là do mẫu vòng lặp chạy khác dự kiến.
3. Nếu vòng lặp chạy dài, dùng `loop context` kèm chế độ kiểm tra và tệp nhật ký chạy để ngữ cảnh không phình vô hạn qua nhiều vòng.
4. Đặt ngân sách token vào `LOOP.md` — đây cũng là điều kiện để điểm sẵn sàng lên tới mức L3.

```bash
npx @cobusgreyling/loop cost --pattern ci-sweeper --cadence 15m --level L2
npx @cobusgreyling/loop context --check --ledger run.json
```

**Kiểm tra**

Chạy lệnh ước lượng hai lần với hai tần suất khác nhau, ví dụ 15 phút và 15 giờ: con số phải thay đổi theo đúng tỉ lệ. Nếu y hệt nhau thì lệnh đang bỏ qua tần suất.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: README.md.*