# ❓ FAQ — AutoGen (chuyện thật, dễ hiểu)

Nếu câu hỏi nào khó hiểu thì đọc `../README.md` phần trong ngoặc vuông.

---

## Q1. Một agent ôm hết việc cũng chạy được, sao phải tách nhiều agent? [→ Câu Chuyện Mở Đầu]

**Bạn sẽ thấy**

Agent của bạn làm cả ba việc: lấy kiến thức cũ, lên kế hoạch, viết code, tự review lại. Chạy thì chạy được, nhưng ba dấu hiệu chững lại rõ ràng: context đầy trước khi làm nửa việc, một lỗi nhỏ ở giữa làm hỏng cả chuỗi phía sau, và bạn không biết phần nào hỏng để sửa prompt cho đúng chỗ.

**Vì sao**

README gọi trạng thái đó là "đơn khối": một agent ôm đồng thời nhiều vai. Muốn sửa vai "review" thì sửa chung system prompt, và vai "viết code" cũng đổi theo. AutoGen tách bằng hội thoại — mỗi agent là một `ConversableAgent` riêng, có system prompt riêng, truyền kết quả cho nhau qua message thay vì dùng chung một đầu óc.

| Vai trong AutoGen | Đúng phần nào của harness |
|---|---|
| PlannerAgent | harness/04 plan/decompose |
| AssistantAgent | harness/05 prompt/response |
| UserProxyAgent | harness/06 tool execution |
| CriticAgent + GroupChat | harness/11 + harness/09 |

**Làm gì**

1. Liệt kê các việc agent của bạn đang làm, rồi gán mỗi việc cho một agent riêng.
2. Làm `UserProxyAgent` đóng vai harness: tự gọi công cụ, tự nhận kết quả, tự đi tiếp.

```python
harness = UserProxyAgent(
    name="harness",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    code_execution_config={"work_dir": "coding"},
)
```

3. Thêm `CriticAgent` để bắt lỗi thay vì để agent tự chấm điểm cho mình.
4. Nhiều agent hơn thì gom vào `GroupChat` — xem Q3.

**Kiểm tra**

Chạy bản một agent, ghi lại số token và số lần trả lời sai. Sau đó tách Planner + Critic, chạy lại đúng task đó. Nếu số token tăng nhưng số lần phải sửa tay giảm thì việc tách đang đáng tiền; nếu token tăng mà kết quả y như cũ thì vai bạn tạo ra chưa khác biệt, đổi cách chia.

---

## Q2. Các agent nói chuyện với nhau mãi không dừng, token đốt từng phút — chặn ở đâu? [→ Code Mẫu Từ HARNESS_ENGINEERING.md]

**Bạn sẽ thấy**

Hai agent cứ ping qua lọt lại: assistant sinh code, harness chạy code, code lỗi, assistant giải thích, harness chạy lại... Một task đáng lẽ 2 phút thành 15 phút. Có lần đổi mô hình là tốn gấp bốn số tiền. Bạn cũng không biết lượt nào thì ngừng, vì không có mốc nào được đặt ra.

**Vì sao**

`human_input_mode="NEVER"` biến `UserProxyAgent` thành harness tự điều hành: không ai hỏi, nên nó chỉ dừng khi có điều kiện dừng. Hai điều kiện dừng trong README là `max_consecutive_auto_reply` cho hội thoại hai agent, và `max_round` cho hội thoại nhiều agent qua `GroupChat`. Không đặt con số này thì vòng lặp không bao giờ tự thoát.

**Làm gì**

1. Đặt trần cho mỗi cuộc hội thoại ngay lúc khởi tạo, không đợi tới khi cháy.
2. Bắt đầu từ con số nhỏ: `max_consecutive_auto_reply=10`, `max_round=20` như README dùng. Tăng dần khi thấy task thật cần nhiều hơn.
3. Với task sửa lỗi, đặt trần thấp hơn và thêm điều kiện dừng riêng: "critic nói hài lòng thì dừng".

```python
group_chat = GroupChat(
    agents=[planner, assistant, critic, executor],
    messages=[],
    max_round=20,
    speaker_selection_method="auto",
)
```

4. Nếu lượt nói tăng không dừng, xem lại xem agent nào không có đầu ra rõ ràng để lượt sau biết mình xong chưa.

**Kiểm tra**

Chạy lại đúng task từng đổi trần `max_round` và ghi số lượt thực tế. Số lượt phải luôn dừng dưới trần, và báo cáo cuối phải có số lượt + lý do dừng. Nếu báo cáo thiếu lý do dừng thì trần chỉ đang cắt ngẫu nhiên, chưa phải điều kiện dừng thật.

---

## Q3. Trong hội thoại nhiều agent, ai được quyền nói trước? [→ GroupChat — Nhiều Agent]

**Bạn sẽ thấy**

Bạn có bốn agent (planner, coder, critic, executor) nhưng không biết lượt nói sẽ đi vòng hay sẽ tới đúng người cần. Có lần coder chưa có kế hoạch đã bắt tay viết code. Có lần planner nói suốt, không ai làm được gì.

**Vì sao**

`GroupChat` không tự biết ai nên nói khi nào — nó cần một quy tắc chọn người nói, gọi là `speaker_selection_method`. Đây chính là vai trò điều phối của harness ở multi-agent: manager quyết định lượt, các agent còn lại đóng vai nhân viên.

**Làm gì**

1. Bắt đầu với `speaker_selection_method="auto"` (manager chọn theo ngữ cảnh) — README ghi rõ nó để nhà quản lý quyết định.
2. Muốn kiểm soát chặt, chuyển `"round_robin"`: ai cũng được nói một lần theo thứ tự cố định. Dễ đoán, nhưng lãng phí lượt cho người không liên quan.
3. Có khi cần biểu quyết thì dùng `"vote"`.
4. Gán `max_round` như Q2, và luôn ghi lại tên người nói mỗi lượt để sau này biết lỗi do ai.

**Kiểm tra**

In ra danh sách người nói theo thứ tự lượt, xem nó có khớp với trình tự mong muốn không. Chạy thử cả ba cách trên cùng một task và so số lượt + kết quả cuối. `"auto"` thắng khi lượt nói ít biến động; `"round_robin"` thắng khi bạn cần kết quả lặp lại được giữa các lần chạy.

---

## Q4. `human_input_mode="NEVER"` với `"TERMINATE"` khác nhau thế nào? [→ Human-in-the-Loop Cho Phép Thay Đổi Nhạy Cảm]

**Bạn sẽ thấy**

Hai dòng cấu hình chỉ khác một từ, nhưng hành vi khác hẳn. Một cái để agent chạy không cần bạn, một cái vẫn chạy tự do nhưng sẽ dừng ở đúng chỗ cần xác nhận.

**Vì sao**

`"NEVER"` nghĩa là không bao giờ hỏi người — phù hợp khi bạn muốn chạy không giám sát (chạy hàng loạt, chạy trong test). `"TERMINATE"` nghĩa là "chỉ dừng khi thật sự cần": các bước thường vẫn tự đi, nhưng bước nhạy cảm thì chờ bạn. Chọn sai thì hoặc bạn ngồi canh cả trăm lượt không cần, hoặc agent tự đổng ý với việc xoá dữ liệu.

**Làm gì**

1. Mặc định `"NEVER"` cho phần viết code, chạy test, đọc file.
2. Dùng `"TERMINATE"` cho bất kỳ bước nào đụng production, phát hành, xoá, hoặc gửi ra ngoài.

```python
sensitive_harness = UserProxyAgent(
    name="harness",
    human_input_mode="TERMINATE",  # chỉ dừng khi cần xác nhận
    code_execution_config=False     # tắt chạy code luôn
)
```

3. Kết hợp `code_execution_config=False` ở agent nhạy cảm: agent đó chỉ được đề xuất, không được tự chạy.
4. Ghi lại ở bản ghi kiểm toán lúc nào đã hỏi, ai trả lời gì.
5. Nhớ giới hạn tiến trình này không cứu được bạn khỏi lỗi cấu hình: nếu đặt sai chế độ, agent sẽ hỏi những việc vô nghĩa và bạn sẽ dần tắt phần hỏi đi cho khỏi phiền — lúc đó quyền đã vô hiệu mà không có gì báo.

**Kiểm tra**

Chạy một task có bước nhạy cảm với cả hai chế độ. `"NEVER"` phải chạy trọn không dừng; `"TERMINATE"` phải dừng đúng bước nhạy cảm và chờ. Nếu `"TERMINATE"` vẫn chạy trọn, nghĩa là cấu hình chưa được đặt đúng chỗ. Đếm số lần phải bấm xác nhận trên cả 20 task: nếu tỷ lệ lượt hỏi/nghỉ cảnh vượt quá 1 phần 5, cấu hình đang hỏi nhiều hơn mức cần.

---

## Q5. Cho agent chạy code thật trên máy tôi — lỡ nó xoá file thì sao? [→ Code Mẫu Từ HARNESS_ENGINEERING.md]

**Bạn sẽ thấy**

Agent viết xong code và muốn tự chạy để biết có lỗi không. Chạy trực tiếp trên máy của bạn thì một lệnh gõ sai là mất công sức cả tuần: code chạy ở đúng chỗ bạn đang làm việc, không có giới hạn, không có nhật ký đầy đủ.

**Vì sao**

README chỉ ra điểm mấu chốt: `UserProxyAgent` mạnh vì nó là người thực thi, nhưng sức mạnh đó cũng là rủi ro. Tham số `code_execution_config` quyết định code chạy ở đâu. Khi nó chạy trong thư mục riêng, việc cần giám sát chuyển sang tầng sandbox (đọc `../../harness/12-sandbox-execution/`) — đó là lớp giới hạn thiệt hại, không phải lớp lọc lỗi.

**Làm gì**

1. Luôn trỏ `code_execution_config` vào một thư mục riêng, ví dụ `{"work_dir": "coding"}` — không để mặc định rơi vào thư mục dự án đang mở.
2. Bọc lớp thực thi trong sandbox: `--network=none`, `--memory=512m`, `--pids-limit=64`, có giới hạn thời gian.
3. Agent duyệt (người quyết định chạy lệnh) không cần quyền này; chỉ agent viết code mới chạy được, và chạy trong hộp.
4. Agent nào không cần chạy code thì tắt hẳn: `code_execution_config=False`.

**Kiểm tra**

Cố tình cho agent chạy `rm -rf` trong thư mục làm việc và `printenv`: cái thứ nhất phải bị chặn, cái thứ hai không được thấy khoá nào. Xác nhận thư mục làm việc của bạn không đổi file nào sau cả lần chạy.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: README.md.*