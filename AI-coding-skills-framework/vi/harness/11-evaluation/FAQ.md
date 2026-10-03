# ❓ FAQ — Evaluation (Câu hỏi thật, dễ hiểu)

Nếu câu hỏi chưa rõ, đọc phần được nêu trong ngoặc vuông. Câu hỏi được nhóm theo tên file nguồn.

---

## Nhóm 1 — Từ file `README.md`

## Q1. Model tôi đạt 92% ở HumanEval nhưng chỉ 53% ở SWE-bench — model tôi dở hay bài benchmark khó? [→ §3.3 · §10.1]

**Bạn sẽ thấy**

Cùng một model, hai con số lệch nhau gần 40 điểm. Bảng so sánh trong tài liệu cho ví dụ rất rõ: Claude đạt 92% Pass@1 ở HumanEval nhưng chỉ 48% ở SWE-bench Lite và 53% ở SWE-bench Verified.

**Vì sao**

Hai bộ đề đo hai năng lực khác nhau. HumanEval là "viết một hàm đơn lẻ theo đề bài", còn SWE-bench là "đọc mô tả một lỗi thật từ GitHub, tìm đúng file, vá đúng chỗ, và không làm hỏng những test đang xanh" — trên 2.294 lỗi thật.

| Bộ đề | Dạng bài | Điều khó nhất |
|---|---|---|
| HumanEval | 1 hàm, có test ngay | Viết đúng thuật toán |
| SWE-bench | vá lỗi trong repo thật | Tìm đúng chỗ, không phá bài cũ |
| MBPP+ | bài lập trình ngắn, nhiều test | Bao phủ nhiều trường hợp |
| LiveCodeBench | đề mới hằng tuần | Không học trước đề |

**Làm gì**

1. Đừng dùng một con số để kết luận về model. Chọn bộ đề **giống việc thật bạn giao cho nó**.
2. Nếu đội bạn sửa lỗi trong dự án nội bộ, hãy tự dựng 10 bài đại diện cho đúng domain của mình (ví dụ "sửa lỗi con trỏ null trong `UserService.getProfile`") và chấm mỗi ngày — đây là mẫu pipeline của một đội 20 lập trình viên trong tài liệu.
3. Khi đổi model, so hai bảng cùng lúc: chất lượng và chi phí. Bảng Aider cho thấy DeepSeek V3 đạt 92% chất lượng của GPT-4o nhưng chỉ tốn 11% chi phí.
4. Tách hai khái niệm: điểm **đúng/sai** và điểm **chạy được ổn không**. Chỉ dùng cái thứ hai để quyết định đưa vào production.

**Kiểm tra**

Chạy cùng 10 bài của đội bạn lên cả hai model, so **cả** tỉ lệ pass lẫn token trung bình mỗi bài. Nếu chênh lệch nhỏ hơn 5 điểm, hãy chọn theo giá.

---

## Q2. Đổi prompt xong agent quên làm đúng những việc cũ — phát hiện bằng cách nào? [→ §4.3 · §9.1 DO/DON'T]

**Bạn sẽ thấy**

Sau một lần sửa prompt, điểm trung bình trên bài mới tăng, nhưng ba bài cũ tụt mạnh. Bạn chỉ thấy điểm chung, không thấy bài nào tụt.

**Vì sao**

Cải tiến một chỗ thường làm hỏng chỗ khác — đây là đánh đổi có thật, không phải lỗi ngẫu nhiên. Nếu bạn chỉ đo bộ bài mới, sự đánh đổi này vĩnh viễn bị giấu.

**Làm gì**

1. Lưu sẵn **bài giải chuẩn** (golden answer) cho từng task, đã được xác minh làm đúng.
2. Chốt một **baseline** — điểm hiện tại của mỗi bài — rồi không sửa nữa.
3. Sau mỗi lần đổi prompt, chạy lại **toàn bộ** bộ, không chỉ bài mới.
4. Ngưỡng cảnh báo là tụt quá 10 điểm ở một bài nào đó thì báo `REGRESSION`. Tăng quá 10 điểm thì ghi vào danh sách cải tiến, để biết nên giữ thay đổi nào.
5. Có `validator` (hàm kiểm tra kết quả) thì chấm 100 hoặc 0 cho chắc; không có thì mới so độ giống nhau theo từ khoá.

```python
baseline = self.baselines.get(test["id"], 50.0)
if score < baseline - 10:      # tụt quá 10 điểm → REGRESSION
    regressions.append({"id": test["id"], "delta": score - baseline})
elif score > baseline + 10:    # tăng quá 10 điểm → ghi nhận cải tiến
    improvements.append({"id": test["id"], "delta": score - baseline})
```

**Kiểm tra**

Cố tình sửa prompt theo hướng xấu. Bộ regression phải báo đỏ và nêu đúng **id bài nào** tụt, bao nhiêu điểm. Chỉ báo "điểm chung giảm" là chưa đủ.

---

## Q3. Agent pass hết bài test nhưng phí 30 lần gọi công cụ — có nên phạt không? [→ §15.1 · §2.2]

**Bạn sẽ thấy**

Một run pass: 30 lần gọi công cụ, chỉ 8 lần thực sự hữu ích; 42 bước trong khi bài tham chiếu trung vị chỉ 12. Điểm "pass" của bạn vẫn là xanh.

**Vì sao**

Chấm pass/fail chỉ nhìn kết quả cuối. Nó không phân biệt một agent đi thẳng với một agent vừa đi vừa lạc, xoay vòng rồi **may rủi ro** cũng ra kết quả đúng. Ở production, cái thứ hai tốn tiền và còn giữ nguyên độ rủi ro.

**Làm gì**

Chấm cả **đường đi**, không chỉ đích đến. Bốn số đo kèm theo:

| Số đo | Cách tính | Mục tiêu |
|---|---|---|
| Hiệu quả bước | bước tham chiếu ÷ bước thật (trần 1.0) | ≥ 0.7 |
| Độ chính xác công cụ | lời gọi hữu ích ÷ tổng lời gọi | ≥ 0.6 |
| Khả năng tự phục hồi | lỗi tự sửa ÷ tổng đợt lỗi | ≥ 0.5 |
| Lần ghi bị hoàn tác | lần ghi bị hoàn tác ÷ tổng lần ghi | ≤ 0.2 |

Tổng: `trajectory_score = 0.5·pass + 0.2·hiệu quả + 0.15·độ chính xác + 0.15·khả năng phục hồi`, và dùng điểm này làm cổng CI ở mức **≥ 0.65**.

Đừng quên ghi log đủ 5 thành phần mỗi bước: suy nghĩ, công cụ, tham số, kết quả, chi phí.

**Kiểm tra**

Chạy lại run 42 bước ở ví dụ trên tài liệu — nó pass nhưng hiệu quả chỉ 12/42 ≈ 0.29, độ chính xác 8/30 ≈ 0.27, nên `trajectory_score` phải dưới 0.65 và bị chặn. Run 14 bước phải vượt cổng.

---

## Q4. Đổi sang model đắt hơn, điểm chỉ +2% nhưng tiền tăng gấp 4 — nên đổi không? [→ §15.3]

**Bạn sẽ thấy**

Ba lựa chọn định tuyến (route) trả về ba bảng kết quả rất khác nhau: model nhỏ có pass 52%, dây chuyền nhỏ-rồi-lớn có pass 71%, chỉ dùng model lớn có pass 74% — nhưng chi phí mỗi nghìn bài lần lượt là 18 USD, 46 USD và 210 USD.

**Vì sao**

Nhìn pass% sẽ bảo bạn chọn hàng 74% và không thấy rằng nó đắt gấp 4,6 lần. Chi phí phải được chia cho **số bài thực sự giải được**, không phải cho tổng số bài.

**Làm gì**

1. Tính `$ mỗi bài đạt = tổng chi phí đánh giá ÷ số bài đạt`.
2. Với ba route trên: 0,035 USD — 0,065 USD — 0,284 USD. Hàng giữa thắng rõ: pass cao hơn 19 điểm mà vẫn rẻ hơn 4,4 lần so với hàng cuối.
3. Kiến trúc đáng cân nhắc: **task dùng model nhỏ, chỉ leo thang lên model lớn khi đang sai**. Đây là dây chuyền nhỏ-rồi-lớn ở hàng giữa.
4. Đặt quy tắc nâng cấp bằng số: chỉ nâng khi **cả hai** điều kiện đúng — pass tăng ≥ +2 điểm phần trăm **và** `$ mỗi bài đạt` tăng ≤ +10%.

**Kiểm tra**

Trước khi đổi, chạy cùng một bộ 100 bài trên route cũ và route mới, rồi in ra ba cột: pass%, `$ mỗi bài đạt`, tổng token. Nếu chỉ một trong hai cột đầu đi qua quy tắc, giữ route cũ.

---

## Q5. Dùng LLM khác làm giám khảo (judge) chấm điểm — tin được không? [→ §4.2 · §15.4]

**Bạn sẽ thấy**

Bạn nhờ một model mạnh chấm code của model khác theo 5 chiều (đúng, chất lượng, hiệu quả, bền, đầy đủ), thang 1–10. Điểm nhìn rất hợp lý. Nhưng cùng một đoạn code, chạy hai lần cho hai điểm khác nhau.

**Vì sao**

Giám khảo cũng là mô hình: nó có tính ngẫu nhiên, có thể **bịa** lý do, và có xu hướng thưởng cho câu trả lời **dài hơn** chứ không phải **đúng hơn**. Nó còn có thiên kiến vị trí: bản "A" đứng trước thường được chấm cao hơn.

**Làm gì**

1. Dùng judge cho những thứ máy chấm khó: khả năng đọc code, thiết kế, sự rõ ràng. **Không** dùng nó thay test tự động cho tính đúng đắn.
2. Bắt buộc judge trả về JSON có cấu trúc: mỗi chiều một `score` và một `reason` dài đúng một câu, cộng `suggestions`. Parse thất bại thì tính là hỏng, không được cho điểm 0 âm thầm.
3. **Hiệu chuẩn với con người mỗi quý**: lấy mẫu 100–200 bài cho người chấm mù (không thấy điểm của judge), rồi tính hệ số tương đồng Cohen.
4. Ngưỡng cứng: `κ ≥ 0.7` trước khi được phép gác làm cổng chặn. Thấp hơn thì sửa lại tiêu chí chấm và thêm ví dụ mẫu — **không bao giờ** hạ chuẩn.
5. Kiểm tra thiên kiến: đảo thứ tự A/B và chấm lại, đo độ lệch. Lệch lớn thì bỏ phần so sánh cặp, chỉ dùng chấm điểm độc lập.

**Kiểm tra**

Chấm mù 100 bài, tính `κ` theo từng chiều. In cả độ lệch do đảo thứ tự. Báo cáo điểm số kèm hai con số này, không báo cáo điểm đơn thuần.

---

## Q6. Bài benchmark của tôi nằm trong dữ liệu huấn luyện của model — làm sao biết? [→ §15.2 · §10.3]

**Bạn sẽ thấy**

Model của bạn bỗng tăng vọt điểm ở một bộ benchmark cũ, trong khi điểm ở bài mới không đổi. Bảng điểm trong tài liệu cũng có dòng "Human" để trống ở một số bộ — dấu hiệu dữ liệu không công khai.

**Vì sao**

Bài benchmark cũ, ai cũng có trong tay, rất dễ nằm trong dữ liệu huấn luyện của model. Đó gọi là **rò rỉ dữ liệu** (contamination). Và bộ đề tĩnh còn thêm vấn đề khác: nó lỗi thời theo thời gian và dễ bị "chơi" cho điểm.

**Làm gì**

1. Cách ly mọi task mà lời giải hoặc văn bản mô tả lỗi có thể xuất hiện trước mốc cắt huấn luyện; gắn thẻ `leak_risk: high` và loại khỏi con số chính, báo cáo riêng.
2. Ghim `seed` và đặt `temperature = 0` cho bộ regression. Với eval ngẫu nhiên, chạy **3 lần** và báo cáo trung bình ± độ lệch — một lần chạy không đủ.
3. Cách ly môi trường: container hoặc hệ thống tệp mới cho mỗi task, không dùng cache chung giữa các task, chặn mạng trừ kho gói trong danh sách cho phép.
4. Băm (hash) bộ dữ liệu và ghi mã commit của môi trường vào **mọi** báo cáo — không có nó thì không chứng minh được báo cáo cũ chạy trên đúng dữ liệu.
5. Giảm rủi ro theo hướng LiveCodeBench: lấy đề mới hằng tuần từ nền tảng thi đấu lập trình, qua bốn bước cào → loại trùng → kiểm tra → chạy, và có sẵn bước phát hiện rò rỉ.

**Kiểm tra**

Chạy một tập bài **tự viết** cho dự án của bạn, chưa từng công khai. Nếu điểm model giảm mạnh so với bài công khai, đó là dấu hiệu bạn đã đo bài nhớ chứ không phải bài làm.

---

## Nhóm 2 — Từ file `minimal-benchmark-harness.md`

## Q7. Model của tôi giỏi code nhưng điểm benchmark thấp — do prompt quá dài hay do framework? [→ §1 Bối Cảnh & Động Cơ · §2 Triết Lý]

**Bạn sẽ thấy**

Bạn dựng một đường đo điểm cho agent của mình. Kết quả: agent chỉ giải được 30% bài. Bạn không biết vấn đề nằm ở model hay ở cách bạc đường.

**Vì sao**

Ba tầng trung gian hay làm nhiễu kết quả hơn model. Một: system prompt dài trên 2.000 token định hướng hành vi quá mức. Hai: các tầng truy xuất (RAG), gộp nhớ, hay lớp chặn an toàn tự sửa câu trả lời của model. Ba: quá nhiều công cụ rườm rà làm model chọn sai công cụ. Không tách ra thì không bao giờ trả lời được câu hỏi cốt lõi: model giỏi suy luận thật, hay framework đang bịt điểm yếu?

**Làm gì**

Chạy một lần đo ở **chế độ tối giản** để đo năng lực gốc, theo đúng công thức:

```
Harness tối giản = system prompt tối giản
                 + không có tầng trung gian nào
                 + đúng 2 công cụ: bash và editor
```

1. System prompt dưới 100 token, chỉ nói đúng việc: làm kỹ sư lập trình, giải vấn đề bằng `bash` và `editor`, xong thì in ra `COMPLETE_TASK`.
2. Chỉ cấp hai công cụ. `bash` nhận đúng một tham số `command`. `editor` có `command` giới hạn trong ba giá trị `view`, `create`, `str_replace`.
3. Gọi thẳng model, không đi qua truy xuất hay gộp nhớ.
4. Đo lại bốn số: Pass@1 (tỉ lệ giải đúng ngay lần đầu), số lượt trung bình mỗi bài, tỉ lệ gọi công cụ sai tham số, và token tiêu tốn mỗi bài đạt.

**Kiểm tra**

Nếu điểm ở chế độ tối giản **thấp hơn** điểm ở đường đầy đủ, framework của bạn đang giúp agent, đừng vội bỏ. Nếu điểm cao hơn, framework đang làm hỏng năng lực thật — và đó mới là thứ bạn cần sửa.

---

## Q8. Tự dựng một đường đo điểm tối giản thì cần tối thiểu những gì? [→ §4 Bộ Công Cụ · §5 Benchmark Runner · §6 Metrics · §7 Guardrails]

**Bạn sẽ thấy**

Bạn muốn tự viết đường đo cho đội mình, không dùng framework sẵn có. Bạn cần biết tối thiểu những mảnh gì thì kết quả mới đáng tin.

**Vì sao**

Bộ đo tối giản không cần nhiều thứ, nhưng thiếu một mảnh thì con số thành ảo. Ba lỗi làm hỏng kết quả thường gặp nhất: rò rỉ đáp án qua system prompt, dùng lại ký ức của phiên trước, và cho các bài dùng chung thư mục làm việc.

**Làm gì**

1. **Cấu trúc một bài**: `id`, `problemStatement`, `repoPath`, `testCommand`. Bốn trường này đủ.
2. **Vòng lặp**: giới hạn 20 lượt mặc định, dừng sớm khi model in ra `COMPLETE_TASK`. Mỗi lượt ghi lại vào log để sau này truy ngược.
3. **Chấm bằng test khách quan**, không chấm bằng mô hình: chạy `testCommand`, coi là đạt khi mã thoát (exit code) bằng 0.
4. **Ba luật cách ly bắt buộc**: reset container sạch trước mỗi bài; không nạp dữ liệu phiên trước; đặt thời gian chặn chặt cho lệnh `bash` (ví dụ 5 phút mỗi bài) để không bị treo.
5. **Cấm tuyệt đối** đưa lời giải hay gợi ý vào system prompt của đường đo, và cấm cho các bài dùng chung thư mục làm việc — nếu không, tác dụng phụ của bài này sẽ làm sai bài kia.

**Kiểm tra**

Cố tình dùng chung thư mục làm việc cho hai bài liên tiếp và xem kết quả bài sau có đổi không. Nếu có, đường đo của bạn đang rò rỉ trạng thái giữa các bài và phải sửa lại từ đầu.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: `README.md`, `minimal-benchmark-harness.md`.*