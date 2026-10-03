# ❓ FAQ — Evaluation (chuyện thật, dễ hiểu)

Câu hỏi nào khó hiểu thì đọc `README.md` phần trong ngoặc vuông.

---

## Q1. PromptFoo, Deepeval, Ragas — chọn cái nào? [→ Tổng Quan Các Công Cụ]

**Bạn sẽ thấy**

Bạn muốn biết việc đổi prompt từ "bạn là assistant hữu ích" sang "bạn là senior engineer" có thật sự tốt hơn không. Ba công cụ trả lời ba kiểu câu hỏi khác nhau:

| Công cụ | Hỏi được câu nào | Cách dùng |
|---|---|---|
| PromptFoo | prompt này có tốt hơn prompt kia không | file cấu hình + so sánh bảng |
| Deepeval | câu trả lời này có đúng và đủ không | viết test như pytest |
| Ragas | phần truy xuất tài liệu có tốt không | chỉ dùng cho RAG |

**Vì sao**

Vì chúng đo những thứ khác nhau. PromptFoo chạy ở tầng ứng dụng: bạn đưa vào một bộ câu hỏi mẫu, nó chạy hết lên các biến thể prompt và các model khác nhau rồi xếp bảng. Deepeval viết test theo kiểu pytest, dùng các chỉ số có mô hình ngôn ngữ chấm điểm. Ragas chỉ dành cho hệ thống có truy xuất tài liệu, đo ba thứ: câu trả lời có bám đúng tài liệu không, có liên quan câu hỏi không, các đoạn tài liệu lấy ra có đủ và đúng không.

**Làm gì**

1. Bắt đầu bằng PromptFoo — nhanh nhất để trả lời câu "đổi prompt có tốt hơn không", và nó chạy local.
2. Chuyển sang Deepeval khi bạn muốn đánh giá nằm trong bộ test tự động, theo kiểu `assert_test`.
3. Chỉ thêm Ragas khi thật sự dùng RAG; không có truy xuất thì Ragas không có gì để đo.
4. Dùng cả ba cùng lúc cũng được: PromptFoo cho prompt, Ragas cho phần truy xuất, Deepeval cho kiểm thử định kỳ.

```yaml
tests:
  - vars: { input: "Long technical document..." }
    assert:
      - type: contains
        value: "key concept"
      - type: cost
        threshold: 0.05
```

**Kiểm tra**

Chạy cùng một bộ câu hỏi mẫu qua PromptFoo rồi xem bảng so sánh. Nếu bảng hiện đủ cột điểm, chi phí và độ trễ cho từng cặp prompt-model, công cụ đang hoạt động.

---

## Q2. Cần bao nhiêu câu test để bắt đầu? [→ Lộ Trình Đề Xuất]

**Bạn sẽ thấy**

Bạn mở thư mục `02-setup` và thấy ghi `(TODO)`. Bạn ngồi viết 300 câu hỏi, viết xong thì không muốn chạy vì tốn tiền.

**Vì sao**

Vì bộ test nhỏ mà chạy mỗi lần thì bạn còn dám sửa prompt. Bộ test lớn thì bạn chạy một lần rồi bỏ, và khi đó nó không còn tác dụng gì. Lộ trình gợi ý **20 đến 50 câu**, tập trung vào một nhiệm vụ chính.

Số lượng quan trọng hơn hình thức: 30 câu phủ đúng các tình huống thật có giá trị hơn 300 câu sinh tự động.

**Làm gì**

1. Lấy 30 câu hỏi thật đã dùng với hệ thống, ưu tiên loại người dùng hay gặp nhất.
2. Thêm các câu hỏi xấu: hỏi ngoài phạm vi, hỏi mơ hồ, hỏi có dấu hiệu tiêm nội dung (prompt injection).
3. Viết sẵn câu trả lời chuẩn cho những câu có đáp án khách quan như câu tra cứu thông tin.
4. Khoảng 1/3 bộ để lại cho kiểm thử, **không** dùng để tinh chỉnh — nếu không bạn chỉ đang học thuộc bộ test của mình.
5. Đo xem chạy hết bộ mất bao nhiêu tiền một lần, rồi quyết định có chạy mỗi lần commit hay theo đêm hay không.

**Kiểm tra**

Chạy bộ test hai lần trên cùng một mã phiên bản. Điểm phải giống hệt nhau. Nếu lệch, bạn đang chấm điểm bằng mô hình không ổn định và cần sửa cách chấm trước khi tin vào con số.

---

## Q3. Chạy eval tốn tiền — có kiểm soát được không? [→ PromptFoo — Config-Driven Eval]

**Bạn sẽ thấy**

Bạn định chạy 4 prompt × 2 model × 50 câu = 400 lượt gọi mỗi lần kiểm thử. Hóa ra số tiền lớn hơn ngân sách chạy ứng dụng cả tháng.

**Vì sao**

Vì eval là công việc lặp lại. Ứng dụng chạy mỗi ngày vài trăm lượt, còn eval chạy vài trăm lượt mỗi lần bạn đổi prompt. Không kiểm soát thì tiền sẽ hết vào bộ test chứ không vào sản phẩm.

**Làm gì**

1. Chặn chi phí ngay trong khẳng định: một lượt gọi không được vượt ngân sách.
2. Chạy bộ nhỏ ở cục bộ trước; chỉ đưa lên mô hình đắt khi điểm số chênh lệch thật sự.
3. Chạy bộ đầy đủ theo lịch đêm, chạy bộ con theo mỗi lần commit.
4. So sánh một biến thể tại một thời điểm, đừng so sánh 6 biến thể cùng lúc.

```yaml
prompts:
  - "Summarize: {{input}}"
providers:
  - openai:gpt-4
  - anthropic:claude-3-5-sonnet
assert:
  - type: cost
    threshold: 0.05   # mỗi prompt ≤ 0.05 USD
```

**Kiểm tra**

Đặt ngưỡng chi phí xuống thấp có chủ ý, ví dụ 0,01 USD, rồi chạy lại: kết quả phải đỏ và cho biết vượt ngân sách. Nếu vẫn xanh thì khẳng định chi phí chưa thực sự hoạt động.

---

## Q4. Thêm phần truy xuất tài liệu có cải thiện thật không? [→ Ragas — RAG-Specific Metrics]

**Bạn sẽ thấy**

Sau khi thêm RAG với lấy 5 đoạn tài liệu nhiều nhất, câu trả lời có vẻ hay hơn. Nhưng bạn không chắc đó là do phần truy xuất hay chỉ do câu hỏi dễ.

**Vì sao**

Vì khoảng trắng dữ liệu của RAG là câu hỏi khó nhất: khi câu trả lời sai, bạn không biết lỗi ở khâu lấy tài liệu hay ở khâu trả lời. Ba chỉ số của Ragas tách hai nguyên nhân đó ra:

| Chỉ số | Đo cái gì | Lỗi nói lên gì |
|---|---|---|
| `faithfulness` | câu trả lời có đúng với đoạn tài liệu không | model bịa hoặc tài liệu sai |
| `answer_relevancy` | câu trả lời có liên quan câu hỏi không | tìm nhầm tài liệu |
| `context_precision` | các đoạn lấy ra có đúng và đủ không | truy xuất kém |

Chỉ số `context_precision` thấp trong khi `faithfulness` cao là kết luận rõ ràng: phần truy xuất hỏng, còn mô hình vẫn trả lời đúng với những gì nó được đưa.

**Làm gì**

1. Chạy Ragas trên một tập câu hỏi có đáp án, trước và sau khi bật RAG.
2. Đọc cả ba chỉ số cùng lúc, đừng chỉ nhìn một cái.
3. Nếu `context_precision` thấp, tăng lượng đoạn lấy ra hoặc cải thiện cách cắt đoạn trước khi đổi mô hình.
4. Nếu `faithfulness` thấp, vấn đề nằm ở chỉ dẫn cho mô hình kèm đoạn tài liệu, không phải ở tìm kiếm.

```python
results = evaluate(dataset,
  metrics=[faithfulness, answer_relevancy, context_precision])
```

**Kiểm tra**

Chủ ý làm sai một đoạn trả lời cho một câu hỏi, rồi chạy lại: `faithfulness` phải tụt. Nếu không tụt thì chỉ số đang không đo đúng thứ.

---

## Q5. Làm sao biết hôm nay mình tạo ra bản tệ hơn hôm qua? [→ Case Studies Thực Tế — Regression Detection Trong CI]

**Bạn sẽ thấy**

Bạn đổi câu lệnh trong prompt, thấy câu trả lời tự nhiên hơn, và định phát hành. Ba ngày sau có người báo cáo chức năng cũ hỏng.

**Vì sao**

Vì "tự nhiên hơn" không phải số liệu. Những đổi thay đổi cải thiện việc này làm hỏng việc khác — ví dụ câu lệnh "bạn luôn trả lời chi tiết nhất có thể" làm câu trả lời dài dòng và lạc đề, điểm rơi từ 82% xuống 74%.

Mục tiêu của bài đánh giá không phải chứng minh hệ thống tốt, mà là phát hiện nó xấu đi.

**Làm gì**

1. Chốt một mốc đo: ví dụ prompt gốc đạt 82%, đặt làm chuẩn so sánh.
2. Cho bộ đánh giá chạy tự động mỗi khi bạn đổi prompt, rồi so với mốc đó.
3. Đặt ngưỡng chặn: giảm quá 5% làm đỏ bước kiểm tra, không cho phát hành.
4. Khi đỏ, đọc bảng so sánh để xem biến nào làm điểm rơi.

```yaml
steps:
  - run: promptfoo eval --share
  - run: promptfoo regression-check
  # fail CI nếu accuracy giảm > 5%
```

**Kiểm tra**

Cố tình thêm một câu lệnh làm câu trả lời dài dòng vào prompt rồi chạy lại. Hệ thống phải đỏ và con số phải rơi. Nếu vẫn xanh thì mốc so sánh chưa được lưu đúng chỗ.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: README.md.*