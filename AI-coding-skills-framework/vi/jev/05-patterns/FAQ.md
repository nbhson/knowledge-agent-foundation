# ❓ FAQ — Bốn Kiểu Việc Thật Với Jev Trong Production

Nếu câu hỏi chưa rõ, đọc phần được nêu trong ngoặc vuông.

---

## Q1. Tôi mới bắt đầu — nên áp dụng kiểu nào trước? [→ §2 Routing & triage]

**Bạn sẽ thấy**

Bạn đọc "năm kiểu mẫu áp dụng" và không biết bắt đầu từ đâu. Bạn thử làm luôn cái khó nhất — kiểm tra toàn bộ kết quả của mô hình lớn — rồi nhận ra hàng đợi hỗ trợ không còn ai xử lý vì độ trễ cộng dồn.

**Vì sao**

Định tuyến và phân loại là cái dễ nhất để đo, dễ để hủy bỏ, và giải quyết ngay phần đau nhất: phân một món vào một trong vài nhóm đã biết trước, rồi quyết định mức ưu tiên. Mỗi món chỉ cần một câu chọn (nhóm) và một câu chấm điểm (mức ưu tiên), tổng độ trễ dưới khoảng nửa giây kể cả thời gian mạng — đủ cho hộp thư trực tiếp.

**Làm gì**

1. Bắt đầu từ một hàng đợi cụ thể, ví dụ nhóm `billing`, `tech_support`, `sales`, `churn_risk`.
2. Một câu chọn cho nhóm, một câu chấm điểm 4 mức `p0`–`p3` cho mức ưu tiên, gửi trong **một** lượt gọi.
3. Đặt ngưỡng khác nhau cho hai câu: nhóm cần tự chuyển ở 0.8, mức ưu tiên ở 0.7.
4. Chỉ gửi phần liệu liên quan — tiêu đề và phần đầu nội dung, đừng gửi cả chuỗi hội thoại.

```python
q = decide(state=ticket_text, questions={"queue":    {"type": "choice"},
                                         "priority": {"type": "score"}})
if q["queue_confidence"] >= 0.8 and q["priority_confidence"] >= 0.7:
    auto_route(q["queue"], q["priority"])   # vùng cao: tự làm
elif q["queue_confidence"] >= 0.5:
    suggest_to_agent(q)                      # vùng vừa: gợi ý, người duyệt
else:
    human_triage(ticket_text, q)            # vùng thấp: người xử lý
```

**Kiểm tra**

Đo tỉ lệ định tuyến đúng trên 200 ticket đã có nhãn, cộng với tỉ lệ phần trăm được xử lý tự động. Nếu độ đúng cao mà tỉ lệ tự động quá thấp, ngưỡng của bạn đang chặt quá; nếu ngược lại thì đang lỏng quá.

---

## Q2. Tôi có 100.000 bản ghi cần phân loại — có nổi không? [→ §3 Classification & map-reduce]

**Bạn sẽ thấy**

Con số khách hàng của bạn đã lên vài triệu dòng, và ai đó đề xuất "chạy phân loại cho từng dòng". Bạn làm phép tính chi phí theo thói quen của mô hình lớn và thấy con số không khả thi.

**Vì sao**

Phép tính đó dựa trên giá của một loại công cụ khác. Jev tính theo 0.042 USD mỗi triệu token đầu vào, phần đầu ra miễn phí. Với một bản ghi có trạng thái ngắn, chi phí cho cả trăm nghìn bản ghi vẫn rất nhỏ. Điểm cần nhớ: **độ trễ luôn tính theo từng quyết định** (70–500ms), không tăng theo số bản ghi — nên bạn có thể chạy song song để kéo tổng thời gian chờ xuống.

**Làm gì**

1. Tách thành hai bước: **lập bản đồ** là gọi Jev cho từng bản ghi, **gộp lại** là tổng hợp kết quả.
2. Dùng gọi bất đồng bộ trong từng lô 50 bản ghi để các lượt gọi chạy cùng lúc.
3. Ở bước gộp: chia nhóm theo độ tự tin (≥ 0.8 thì nhận luôn, dưới ngưỡng thì vào hàng chờ xem lại) và tính tỉ lệ phủ.
4. Đặt trạng thái nhỏ cho mỗi bản ghi — không gộp cả tập dữ liệu vào một lượt gọi.

```python
async def classify_one(client, record):
    r = await client.post(API, headers=HEADERS, json={
        "model": "jev-1.13.0", "state": record["text"],
        "questions": {"tag": {"type": "choice", "options": TAGS}}}, timeout=5)
    a = r.json()["answers"]["tag"]
    return {"id": record["id"], "tag": a["selected"], "confidence": a["confidence"]}

# gọi song song theo lô 50, mỗi lượt vẫn 70–500ms
```

**Kiểm tra**

Chạy thử 1.000 bản ghi, đo ba thứ: tổng thời gian chờ, tổng chi phí, và tỉ lệ phần trăm vào hàng chờ xem lại. Ba con số này là cơ sở để bạn trình kế hoạch cho quản lý.

---

## Q3. Tôi muốn chặn agent xóa file — đặt cổng kiểm tra bằng Jev có đủ an toàn không? [→ §4 Gating agent actions]

**Bạn sẽ thấy**

Agent của bạn đề xuất lệnh xóa tệp dữ liệu trong thư mục production. Bạn nghĩ đến việc hỏi Jev "người dùng có cho phép xóa tệp này không" rồi cho chạy nếu câu trả lời là có. Một tuần sau, có một lần tệp bị xóa khi người dùng thực ra chỉ muốn xem.

**Vì sao**

Đây là điểm dễ hiểu sai nhất khi dùng Jev trong an toàn. Jev **phân loại theo chính sách bạn đưa vào**, nó không phải máy phán xét an toàn tuyệt đối, và không kiểm tra logic nền tảng. Với câu hỏi có/không, nếu `p` = 0.94 thì độ chắc chắn là 0.88 — hợp lý. Nhưng nếu `p` = 0.55 thì độ chắc chắn chỉ 0.10: mô hình gần như không biết, và câu trả lời "có" lúc đó không có giá trị gì.

**Làm gì**

1. Đặt hai điều kiện cùng lúc, không dựa riêng vào xác suất: `p ≥ 0.6` **và** độ chắc chắn `|p − 0.5|×2 ≥ 0.5`.
2. Khi không đạt, **chặn** rồi chuyển sang luồng phê duyệt của con người, không chạy thử rồi mới hỏi.
3. Giữ nguyên lớp phân quyền thật là nguồn quyền cuối cùng. Jev chỉ là tín hiệu phân loại nhanh bổ sung cho những trường hợp luật tĩnh không phủ hết.
4. Mô tả tiêu chí "khi nào được coi là có" ngay trong câu hỏi.

```python
def gate(conversation, tool_name, tool_args, p_threshold=0.6, conf_threshold=0.5):
    ans = decide(state=f"{conversation}\nTool: {tool_name}\nArgs: {tool_args}",
                 questions={"authorized": {"type": "noul"}})
    p, conf = ans["p"], abs(ans["p"] - 0.5) * 2
    if p >= p_threshold and conf >= conf_threshold:
        return True                       # cho qua
    request_human_approval(tool_name, tool_args, p, conf)   # chặn + hỏi người
    return False
```

**Kiểm tra**

Đo tỉ lệ chặn sai (hỏi người mà không cần) và tỉ lệ cho qua sai (không hỏi mà nên hỏi) riêng biệt trên 100 tình huống thật. Nếu tỉ lệ cho qua sai bằng 0 thì cổng đang chỉ là hình thức.

---

## Q4. Tôi muốn kiểm tra kết quả mô hình lớn trước khi dùng — làm sao cho rẻ? [→ §5 Verify LLM output]

**Bạn sẽ thấy**

Bạn đang cho mô hình lớn viết câu trả lời khách hàng dựa trên tài liệu chính sách. Bạn muốn một bước kiểm tra "câu trả lời có bám đúng chính sách không", nhưng lần thử đầu tiên là gọi thêm một mô hình lớn để đánh giá — và hóa đơn nhân đôi.

**Vì sao**

Cách rẻ nhất là đảo chiều vai trò: **Jev đọc và phán, mô hình lớn chỉ viết**. Bước kiểm tra là một câu có/không trên trạng thái gồm chính sách và bản nháp, kèm một câu chấm điểm mức nghiêm trọng nếu hỏng. Mỗi lần kiểm tra tốn 70–500 mili-giây và gần như không tốn token đầu ra — đủ rẻ để chạy ở tần suất cao trong mọi vòng lặp. Hãy nhớ giới hạn của cách này: nó phán theo **văn bản chính sách bạn nhét vào trạng thái**, nên chính sách mơ hồ thì kết quả kiểm tra cũng mơ hồ.

**Làm gì**

1. Ghép trạng thái gồm tài liệu chính sách và bản nháp cần kiểm tra.
2. Hỏi hai câu: một câu có/không "có bám đúng chính sách không", một câu chấm điểm 4 mức mức vi phạm.
3. Cho qua khi xác suất ≥ 0.7 **và** độ chắc chắn ≥ 0.5; nếu không thì viết lại tối đa hai lần, hết lượt thì chuyển người.
4. Khi độ chắc chắn thấp, coi như mô hình không biết → chuyển người, **không** bắt nó viết lại.

```python
def verify_draft(policy_text, draft):
    ans = decide(state=f"Policy:\n{policy_text}\n\nDraft:\n{draft}", questions={
        "grounded":  {"type": "noul"},
        "severity":  {"type": "score",
                      "levels": ["none", "minor", "major", "critical"]}})
    p = ans["grounded"]["p"]; conf = abs(p - 0.5) * 2
    return {"pass": p >= 0.7 and conf >= 0.5, "confidence": conf,
            "severity": ans["severity"]["score"]}
```

Có ba chỗ đặt cược bước kiểm tra này: sau mỗi kết quả công cụ và mỗi sản phẩm tạo ra trước khi đi bước sau; làm bộ lọc nhanh trước khi chạy bộ kiểm thử đầy đủ trong vòng lặp; và kiểm tra nội dung thay đổi trước khi hợp nhất. Một điều tuyệt đối đừng làm: đòi Jev giải thích vì sao bản nháp sai — nó chỉ trả điểm và xác suất, phần giải thích là việc của mô hình lớn.

**Kiểm tra**

Đo tỉ lệ bản nháp bị chặn oan và tỉ lệ bản nháp hỏng lọt qua, trên 100 cặp (chính sách, bản nháp) thật của bạn. Bước kiểm tra chỉ đáng giữ nếu tỉ lệ lọt oan thấp hơn tỉ lệ hỏng lọt qua.

---

## Q5. Tôi lấy 20 đoạn văn từ hệ thống tìm kiếm, Jev có xếp hạng lại được không? [→ §6 Ranking & filtering]

**Bạn sẽ thấy**

Hệ thống của bạn lấy 20 đoạn văn làm ứng viên rồi đưa hết vào ngữ cảnh cho mô hình lớn. Bạn muốn thu hẹp còn 3 đoạn tốt nhất trước khi gọi mô hình lớn, để tiết kiệm tiền và tránh ngữ cảnh nhiễu.

**Vì sao**

Jev làm được, và hợp với hệ thống tìm kiếm dựa trên truy xuất (RAG) vì hai lý do: xếp hạng chạy song song nên vài trăm mili-giây cho mỗi ứng viên, và điểm trả về là **giá trị liên tục** — có thể nằm giữa hai mức — nên phân biệt được 3.4 với 3.1, điều mà một nhãn cứng không làm được.

**Làm gì**

1. Định nghĩa thang mức có thứ tự, ví dụ bốn mức `irrelevant`, `weak`, `relevant`, `strong`.
2. Trạng thái gồm câu hỏi của người dùng cộng đoạn ứng viên.
3. Sắp xếp giảm dần theo điểm, rồi lọc bỏ ứng viên dưới ngưỡng tối thiểu.
4. Giữ những ứng viên có độ tự tin thấp nhưng **đánh dấu lại** — điểm cao mà độ tự tin thấp thì thứ hạng rất dễ bị xếp sai.

```python
def rerank(query, passages, min_score=1.5):
    scored = [dict(score_candidate(query, p), passage=p) for p in passages]
    scored.sort(key=lambda r: r["score"], reverse=True)
    return [r for r in scored if r["score"] >= min_score]
```

**Kiểm tra**

Đo trên 50 câu hỏi có đoạn văn đúng đã biết: đoạn văn đúng có nằm trong 3 đoạn đầu sau khi xếp hạng không. So sánh con số này với việc đưa cả 20 đoạn cho mô hình lớn — nếu không tốt hơn, đừng giữ bước xếp hạng.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: README.md.*
