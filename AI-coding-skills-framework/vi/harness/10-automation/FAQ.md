# ❓ FAQ — Automation (Câu hỏi thật, dễ hiểu)

Nếu câu hỏi chưa rõ, đọc `README.md` phần được nêu trong ngoặc vuông.

---

## Q1. Pipeline của tôi báo xanh nhưng deploy lên production thì hỏng — làm sao bắt được? [→ §9.1 Anti-pattern 2 · §15.1 Silent Failures · §2.2]

**Bạn sẽ thấy**

Job cuối cùng báo `success`, Slack gửi "✅ Deployed" — nhưng vài phút sau khách báo trang lỗi. Không có ai biết lỗi đó bắt đầu từ lúc nào, chỉ biết nó "xảy ra sau khi deploy".

**Vì sao**

Đây là anti-pattern "silent failure" (lỗi âm thầm): pipeline chỉ kiểm tra code **trước** khi deploy, không kiểm tra **sau**. Một bài test vẫn xanh không có nghĩa dịch vụ đã chạy được — sai cấu hình, thiếu biến môi trường, image sai tag... đều vẫn để test xanh.

**Làm gì**

1. Thêm bước kiểm tra sau khi deploy, ngay trong pipeline: chờ 30 giây cho dịch vụ khởi động rồi gọi endpoint `/health`, không gọi được thì dừng luôn.
2. Chạy bộ test từ đầu đến cuối (E2E) trên môi trường staging trước khi lên production.
3. Deploy theo kiểu canary: mới cho 10% lưu lượng người dùng, giữ nguyên 90% còn lại. Trong 5 phút quan sát tỉ lệ lỗi và độ trễ, hỏng thì tự quay về bản cũ.
4. Cổng chặn (gate) phải là điều kiện bắt buộc, không phải ghi chú. Trong workflow mẫu, deploy chỉ chạy khi `github.ref == 'refs/heads/main'`; sai nhánh thì không deploy dù test xanh.

```bash
sleep 30
curl -f https://staging.example.com/health || exit 1
npm run test:e2e -- --baseUrl=https://staging.example.com
```

**Kiểm tra**

Cố tình deploy một bản hỏng (ví dụ đổi cổng kết nối sai) và xác nhận pipeline đỏ ở đúng bước kiểm tra sau deploy, không phải đỏ sau khi khách báo lỗi. Nếu vẫn xanh, bạn chưa có kiểm tra sau deploy.

---

## Q2. Cho AI tự sửa lỗi rồi tự quay về bản cũ được không — hay nó sẽ lặp vô hạn? [→ §17.1 · §17.3]

**Bạn sẽ thấy**

Một agent tự sửa code, chạy lại test vẫn đỏ, lại sửa, lại đỏ... Mỗi vòng tiêu một ít tiền gọi mô hình. Không có chặn nào, bạn chỉ biết khi nhìn lại hóa đơn.

**Vì sao**

Vòng lặp tự phục hồi là một hệ quy trình với vốn hạn mức: số vòng, số tiền, thời gian, số lần gọi công cụ. Không đặt trần thì "tự sửa" và "đốt tiền" chỉ là hai mặt của cùng một cơ chế.

**Làm gì**

1. Gắn một ngân sách vòng lặp cho mọi job tự phục hồi: tối đa 10 vòng, tối đa 5 USD, tối đa 300.000 mili giây (5 phút), tối đa 50 lần gọi công cụ.
2. Vòng lặp dừng ở điều kiện đầu tiên xảy ra: thành công, hết ngân sách, hoặc 3 vòng liên tiếp không cải thiện.
3. Hết ngân sách thì **đóng băng và mở sự cố** kèm toàn bộ dấu vết, tuyệt đối không thử lại lặng lẽ.
4. Deploy cũng phải có cổng canary gắn số liệu thật, không phụ thuộc mắt người: lỗi tăng quá 2 điểm phần trăm liên tục 3 phút, hoặc độ trễ p99 vượt mục tiêu quá 5 phút → dừng và lùi.
5. Diễn tập việc rollback hằng tháng (gọi là game day) để biết nút lùi thật sự chạy.

```python
def decide(baseline: dict, canary: dict) -> str:
    if canary["smoke_failures"] > 0 or canary["sev1_firing"]:
        return "ROLLBACK: smoke/sev1"
    if canary["error_rate"] > 0.02:
        return "ROLLBACK: error_rate"
    return "PROMOTE"
```

**Kiểm tra**

Đặt ngân sách cực thấp (2 vòng) rồi cho một task cố ý không giải được. Kết quả mong đợi: dừng đúng ở vòng 2, mở sự cố, log in ra số vòng / tiền / độ trễ, và **không** có lần gọi thứ ba.

---

## Q3. Secret của tôi bị in ra log khi agent chạy pipeline — xử lý thế nào? [→ §17.2 · §9.1 Anti-pattern 3]

**Bạn sẽ thấy**

Trong log của một job tự động xuất hiện dòng kiểu `docker login` kèm mật khẩu, hoặc khoá dạng `sk-...`, `ghp_...`, `AKIA...`. Khoá nằm trong kho tra cứu của team, ai cũng đọc được.

**Vì sao**

Secret hay bị dán vào code cấu hình, nằm trong cấu hình riêng trên giao diện web, hoặc lọt vào transcript của agent. Chỉ một trong ba chỗ đó là chỗ lưu đúng; hai chỗ còn lại là chỗ rò.

**Làm gì**

1. Chỉ lưu secret trong kho quản lý (Vault, kho secret của đám mây). Tuyệt đối không để trong repo, không để trong cấu hình riêng trên web, không để trong transcript.
2. Giới hạn phạm vi: tách theo môi trường (`dev` / `staging` / `prod`) và theo từng dịch vụ. Agent chỉ nhận khoá ngắn hạn, không bao giờ cầm khoá production dài hạn.
3. Nạp vào lúc chạy bằng biến môi trường hoặc file gắn vào; phần `${SECRET:arn…}` do chương trình deploy giải, không phải mô hình ngôn ngữ giải.
4. Xoay vòng tự động mỗi 30–90 ngày, và xoay ngay khi xảy ra sự cố. Có phiên bản `vN` và cửa sổ hỗ trợ kép để không làm hỏng hệ thống đang chạy.
5. Ghi lại mỗi lần đọc (ai đọc, đọc gì, lúc nào) và che giá trị trong log.

```bash
# Che mọi giá trị có hình dạng khoá trong log CI
--mask "gh[pousr]_[A-Za-z0-9]{20,}" --mask "AKIA[0-9A-Z]{16}"
```

**Kiểm tra**

Quét toàn bộ log của 30 ngày gần nhất bằng các mẫu hình dạng khoá. Kết quả phải bằng 0. Khác 0 là sự cố dữ liệu, không phải việc dọn dẹp thường lệ.

---

## Q4. Job chạy định kỳ của tôi bị chạy trùng, deploy đè lên nhau — chặn kiểu gì? [→ §17.4 · §7 Scheduled Tasks]

**Bạn sẽ thấy**

Job đêm chạy 23:58 lại bị kích hoạt lúc 00:01, hai bản chạy song song trên cùng một cơ sở dữ liệu. Hoặc job thứ ba bị bỏ rơi rồi dồn lại chạy một lượt.

**Vì sao**

Lịch (cron) chỉ nói *khi nào bắt đầu*, không nói *lần chạy trước đã xong chưa*. Không có khoá chống chạy trùng và không có khoá chống chồng lấn thì mọi job đều có thể chạy đôi.

**Làm gì**

1. Khoá chống chạy trùng: `idempotency key = tên job + đầu kỳ`, ví dụ `nightly-e2e#2026-09-28`. Handler kiểm tra kho đã-xong trước khi hành động; mọi tác dụng phụ cũng ghi kèm khoá này.
2. Chính sách chồng lấn: `concurrencyPolicy: Forbid` — nếu lần chạy trước còn đang chạy thì lần này bỏ qua. Chỉ dùng `Replace` cho tác vụ đồng bộ dữ liệu đọc rẻ tiền.
3. Đặt `activeDeadlineSeconds` và `startingDeadlineSeconds` để job kẹt không dồn đống, bị giết theo hạn và lần sau không gánh quá khứ.
4. Cho phép bù lỡ (`failedJobsHistoryLimit: 3`) nhưng khoang window bị lỡ chỉ chạy lại nếu được đánh dấu rõ `backfill: true`.

```python
key = f"{task_name}#{window_start.isoformat()}"   # nightly-e2e#2026-09-28
if key in done_store:          # đã chạy rồi → bỏ qua, không chạy lại lần nữa
    return "skipped"
run()
done_store.add(key)
```

**Kiểm tra**

Kích hoạt thủ công cùng một job hai lần trong 5 giây. Lần đầu chạy, lần sau phải trả về `skipped`. Đổi ngày (qua kỳ mới) thì job phải chạy lại bình thường.

---

## Q5. Test của tôi chạy hơn 30 phút nên cả team bỏ qua kết quả — có cách nào không? [→ §9.1 Anti-pattern 5 & 6 · Best Practices 5 · §14.1 Testing Automation Harness]

**Bạn sẽ thấy**

Dev đẩy code, 25 phút sau mới biết test đỏ. Đến lúc đó họ đã làm việc khác. Kết quả cuối cùng: có bài test chạy lúc thì xanh lúc thì đỏ, cả team dần dần không tin CI nữa.

**Vì sao**

Hai nguyên nhân độc lập cộng lại. Thứ nhất là pipeline quá dài và chạy tuần tự. Thứ hai là test không ổn định (flaky) — lỗi ngẫu nhiên do chạy song song, dữ liệu test ngẫu nhiên, phụ thuộc mạng. Một bài flaky làm hỏng uy tín của cả pipeline.

**Làm gì**

1. Đặt mục tiêu thời gian: CI dưới 10 phút, CD dưới 30 phút. Quá mốc thì tách nhỏ.
2. Chạy song song theo ma trận phiên bản thay vì tuần tự, và cache thư viện phụ thuộc giữa các lần chạy.
3. Tách pipeline: một đường chỉ kiểm tra (lint → kiểm tra kiểu → test), một đường riêng để đưa lên staging.
4. Dậy test không ổn định trước khi nó làm hỏng uy tín: cô lập phụ thuộc ngoài (giả lập, chặn), dùng dữ liệu cố định, thêm độ trễ ngẫu nhiên nhỏ khi thử lại mạng.
5. Tách bài flaky sang làn riêng cho tới khi sửa xong, và đánh dấu trong báo cáo thay vì cho nó chặn cả pipeline.

```yaml
- name: Bài test chưa ổn định (không chặn deploy)
  continue-on-error: true
  run: pytest -m flaky --junitxml=flaky.xml
```

**Kiểm tra**

Chạy lại pipeline cũ 10 lần và đo thời gian trung vị. Dưới 10 phút là đạt. Song song, kiểm tra danh sách làn `flaky/` có ngắn lại sau mỗi lần sửa không.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: `README.md`.*