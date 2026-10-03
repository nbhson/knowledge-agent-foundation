# ❓ FAQ — Chia Việc Giữa Jev Và Mô Hình Lớn

Nếu câu hỏi chưa rõ, đọc phần được nêu trong ngoặc vuông.

---

## Q1. Trong một request, tôi nên cho mô hình nào xử lý? [→ §1.1, §1.2 Bảng phân vai]

**Bạn sẽ thấy**

Cùng một lượt xử lý khiếu nại của khách, bạn gọi mô hình lớn ba lần: một lần để đoán thuộc phòng ban nào, một lần để xem có cần hoàn tiền không, một lần để viết email. Ba lượt đó tốn 5–15 giây và một khoản tiền không nhỏ, trong khi hai lượt đầu là quyết định có/không cơ bản.

**Vì sao**

Cách chia việc đúng là dựa trên **hình dạng kết quả cần có**, không phải độ nổi tiếng của công cụ. Jev nhận quyết định: chọn lựa chọn trong danh sách đóng, chấm điểm mức độ, cổng có/không — trong 70–500 mili-giây với giá 0.042 USD mỗi triệu token đầu vào và phần đầu ra miễn phí, nên hỏi lúc nào cũng được. Mô hình lớn nhận ngôn ngữ: sinh văn bản, viết code, soạn tham số cho công cụ, giải thích kết quả. Mỗi lần gọi mô hình lớn là một lần tốn tiền và tốn thời gian.

| Việc | Ai làm |
|---|---|
| Chọn nhóm / nhãn | Jev |
| Cổng có/không | Jev |
| Chấm mức độ | Jev |
| Viết email, viết code | Mô hình lớn |
| Giải thích "tại sao" | Mô hình lớn, dựa trên kết quả Jev |

**Làm gì**

1. Áp dụng câu một: **Jev quyết định, mô hình lớn viết, code thực thi.**
2. Gộp hai lượt quyết định thành một lượt gọi duy nhất — chúng được chấm song song.
3. Chỉ gọi mô hình lớn sau khi đã có quyết định của Jev, và truyền cả xác suất xuống để nó viết cho đúng hướng.
4. Khi cần biết "tại sao", đừng hỏi Jev — hãy đưa kết quả và xác suất của nó cho mô hình lớn diễn giải.

```python
d = jev.ask(state=ticket_text, questions={
    "team":   {"type": "choice", "choices": ["billing", "tech", "account"]},
    "refund": {"type": "noul", "description": "Khách có yêu cầu hoàn tiền không?"}})
draft = llm.write(ticket_text, team=d["team"], refund_p=d["refund"].p)
```

**Kiểm tra**

Đếm số lượt gọi mô hình lớn trước và sau trên 100 tác vụ thật. Mục tiêu là số lượt đó giảm mạnh, chỉ còn ở những chỗ thật sự cần văn bản.

---

## Q2. Tôi có thể để Jev giữ quyền cho phép hay chặn công cụ không? [→ §3 Tool-call gateway]

**Bạn sẽ thấy**

Agent của bạn đề xuất gọi công cụ xóa dữ liệu. Bạn cho ý tưởng đặt một bước hỏi Jev trước mỗi lần gọi công cụ: được phép không, rồi mới cho chạy. Một tuần sau bạn tự hỏi liệu bước này có thật sự bảo vệ hay chỉ tạo cảm giác an toàn.

**Vì sao**

Đây là tầng trung gian rất đáng có: nhanh (70–500ms) nên không cản luồng thật, và xác suất có hiệu chỉnh nên ngưỡng mới có nghĩa. Nhưng cần hiểu đúng vai trò: Jev là **tín hiệu phân loại trên ngữ cảnh**, còn **quyền cho phép hay chặn cuối cùng vẫn nằm ở lớp phân quyền thật** — danh sách chặn, điều kiện quyền, người duyệt. Nó bổ sung cho những trường hợp luật tĩnh không phủ hết, chứ không thay thế lớp đó.

**Làm gì**

1. Bọc mọi công cụ có tác dụng phụ (xoá, ghi, gửi, tính phí) bằng một cổng kiểm tra có/không.
2. Ghép trạng thái gồm lịch sử hội thoại, tên công cụ và tham số.
3. Ba nhánh: xác suất cao thì cho chạy; vừa thì hỏi xác nhận người dùng; thấp thì chặn và chuyển sang luồng phê duyệt.
4. Yêu cầu cả hai điều kiện, không chỉ một: xác suất ≥ 0.6 **và** độ chắc chắn ≥ 0.5.

```python
def gateway(context, tool, p_threshold=0.6):
    ans = decide(state=f"Context:\n{context}\nTool: {tool['name']}\nArgs: {tool.get('args', {})}",
                 questions={"authorized": {"type": "noul"}})
    p, conf = ans["p"], abs(ans["p"] - 0.5) * 2
    if p >= p_threshold and conf >= 0.5:
        return True, {"p": p, "conf": conf}     # cho chạy
    approval_request(tool, {"p": p, "conf": conf})   # lớp phân quyền thật
    return False, {"p": p, "conf": conf}
```

**Kiểm tra**

Đo riêng hai loại lỗi: số lần cho qua mà lẽ ra phải hỏi, và số lần hỏi mà lẽ ra không cần. Cổng chỉ đáng giữ nếu số lần cho qua sai bằng không.

---

## Q3. Công cụ của tôi cần tham số, Jev không tạo được — xử lý sao? [→ §4 Fallback model]

**Bạn sẽ thấy**

Trong Pydantic AI, bạn khai agent với `TypeSafeModel` của Jev và một vài công cụ. Công cụ không tham số chạy rất ổn. Nhưng công cụ có tham số thì Jev báo lỗi `ToolCallProposed` — một loại `ModelAPIError` — và toàn bộ lượt dừng lại.

**Vì sao**

Đây là hệ quả trực tiếp của việc Jev không sinh văn bản: nó không thể viết ra chuỗi tham số cho một công cụ. Người thiết kế xử lý bằng cách đặt một ngưỡng `typesafe_tool_call_threshold` (mặc định 0.6) và một mô hình dự phòng phía sau. Khi công cụ **không** có tham số và độ tự tin đạt ngưỡng, Jev chọn công cụ và gọi thẳng. Khi công cụ **có** tham số, Jev bị kẹt, lỗi được ném ra, và mô hình lớn phía sau nhận **cả bước** — không chỉ phần tham số.

**Làm gì**

1. Bọc mô hình theo thứ tự: Jev trước, mô hình lớn sau, qua `FallbackModel`.
2. Thiết kế chữ ký công cụ theo hướng **càng ít tham số càng tốt** — công cụ không tham số được Jev gọi trực tiếp, không tốn lượt gọi mô hình lớn.
3. Nâng ngưỡng lên khi bạn muốn Jev chuyển giao ít hơn nhưng chuyển đúng hơn; hạ nếu bạn muốn tiết kiệm hơn. Mặc định 0.6 chỉ là điểm khởi đầu.
4. Giữ `FallbackModel` đúng vai: khi được gọi thì nó làm **toàn bộ bước**, đọc ngữ cảnh, sinh tham số và gọi công cụ.

```python
from pydantic_ai.models.fallback import FallbackModel

model = FallbackModel(
    TypeSafeModel("jev-1.13.0"),    # quyết định trước, nhanh và rẻ
    OpenAIModel("gpt-5"),           # nhận cả bước khi Jev kẹt
)
agent = Agent(model, output_type=Triage, tools=[refresh_dashboard])
```

**Kiểm tra**

Đếm trong 200 lượt thật có bao nhiêu lượt bị chuyển sang mô hình lớn, và trong số đó bao nhiêu do công cụ **có tham số**. Nếu tỉ lệ chuyển giao cao, hãy rà lại chữ ký các công cụ để tăng tỉ lệ được Jev xử lý trực tiếp.

---

## Q4. Tôi ghép Jev với mô hình lớn sai chỗ nào? [→ §7 Anti-patterns]

**Bạn sẽ thấy**

Hệ thống của bạn chạy được, không báo lỗi, nhưng kết quả kém hơn kỳ vọng và bạn không chỉ ra được nguyên nhân. Bạn nghi ngờ Jev không tốt, nên định bỏ nó.

**Vì sao**

Phần lớn trường hợp là do bốn lỗi thiết kế lặp lại. Một: nhét câu hỏi vào phần dữ liệu đầu vào — viết "hãy chọn nhóm nào" vào đó rồi mong nhận câu trả lời. Phần dữ liệu là **nguyên liệu để phán đoán**, không phải chỗ gõ hướng dẫn. Hai: tin độ tự tin cao mà không có đường lùi — độ tự tin cao không có nghĩa là đúng. Ba: gộp nhiều tiêu chí vào một câu hỏi, khiến phân phối bị loãng và độ tự tin luôn thấp. Bốn: chỉ đọc nhãn đã chọn, bỏ qua phân phối, nên không thấy được tình huống gần hòa.

**Làm gì**

1. Chuyển câu hỏi vào đúng chỗ: phần dữ liệu chỉ chứa dữ liệu, câu hỏi nằm ở cấu trúc câu hỏi, khung chung nằm ở phần chỉ dẫn.
2. Tách một câu gộp năm tiêu chí thành năm câu — chạy song song nên gần như không tốn thêm độ trễ.
3. Bắt buộc có nhánh lùi ở mọi vùng độ tự tin, kể cả vùng cao.
4. Luôn tính chênh lệch giữa hai lựa chọn đứng đầu; dưới 0.15 thì chuyển người bất kể nhãn là gì.

```python
def decide_or_fallback(state, questions):
    ans = jev_decide(state, questions)["answers"]["queue"]
    conf = ans["confidence"]
    if conf >= 0.8:
        return {"by": "jev", "value": ans["selected"]}
    if conf >= 0.5:
        return {"by": "jev", "value": ans["selected"], "needs_confirm": True}
    return {"by": "llm_or_human", "value": llm_decide(state, questions)}
```

**Kiểm tra**

Đo tỉ lệ ca có/không trong phần dữ liệu đầu vào (phải bằng 0), và tỉ lệ câu hỏi gộp nhiều tiêu chí (nên tách hết). Hai phép đo này bắt được hai lỗi phổ biến nhất trong vài phút.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: README.md.*
