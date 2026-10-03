# ❓ FAQ — Chọn đúng công cụ và gọi MCP (chuyện thật, dễ hiểu)

Nếu câu hỏi chưa rõ, đọc phần được nêu trong ngoặc vuông.

---

## README.md

### Q1. Agent tôi có 50 công cụ, nó cứ "dùng búa đập kính" — sửa sao? [→ §1 Tool Registry + §2 Intent Classification]

**Bạn sẽ thấy**

Agent có đủ dụng cụ trong tay nhưng chọn sai. Hỏi *"BHYT cho người lao động là gì"* thì nó lại gọi `execute_python` tự chịu chết, hoặc gọi `web_search` để tra một câu chỉ nằm trong database nội bộ. Hậu quả: token cháy, kết quả sai, đôi khi là hành động không hoàn tác được.

Ba con số trong tài liệu cho thấy độ nghiêm trọng: chọn tool có cấu trúc giảm **60%** số lần gọi tool thất bại; có bước phân loại ý định trước thì độ chính xác chọn tool nhảy từ **65% lên 92%**; giới hạn 50 kết quả tìm kiếm cộng kiểm tra tham số làm tỉ lệ thành công của SWE-agent tăng **64%**.

**Vì sao**

LLM không thiếu khả năng — nó thiếu *đường đi*. Cho cả 50 định nghĩa công cụ vào prompt rồi bắt nó tự chọn là mời nó đoán mò. Mô tả tool viết mơ hồ thì nó không có gì để bám vào.

**Làm gì**

1. Khai một hồ sơ đầy đủ cho mỗi công cụ: mô tả dùng để làm gì, tham số kèm kiểu, `category`, `tags`, `requires_permission`, `timeout_seconds`, `cost_per_call`.
2. Chia ý định thành nhóm cố định và gắn sẵn nhóm công cụ ứng với. Gặp "tính" / "calculate" / "bao nhiêu" thì vào nhóm `calculator`, `execute_python`, `data_analysis`.
3. Tách bước phân loại ý định khỏi bước chọn công cụ. Không có bước này thì mọi câu hỏi đều đi thẳng vào bộ chọn.
4. Đánh dấu công cụ nguy hiểm ngay từ lúc đăng ký: `sql_query`, `execute_python`, `write_file` đều để `requires_permission="elevated"`.
5. Ghi lại tỉ lệ thành công và độ trễ sau mỗi lần gọi, rồi xếp hạng theo `success_rate / avg_latency_ms`.

```python
registry.register(ToolDefinition(
    name="vector_search",
    description="Tìm kiếm ngữ nghĩa trong cơ sở dữ liệu vector",
    parameters={"query": {"type": "string", "required": True},
                "top_k": {"type": "integer", "default": 5}},
    category="search", tags=["semantic", "vector"],
))
```

**Kiểm tra**

Bốn bài kiểm tra mẫu phải xanh: "Tìm thông tin về BHYT" ra `intent == "search"`; "Tính 15% của 5000000" ra `calculate`; "Xin chào!" rơi vào `chat` và không gọi công cụ nào; "Đọc file và chạy test" tách ra **2** ý định. Rồi chạy 200 câu thật lấy từ log người dùng và đo tỉ lệ chọn đúng.

---

### Q2. Cùng một câu hỏi, đôi khi gọi đúng công cụ, đôi khi gọi sai — làm sao ổn định? [→ §2.1 Multi-Strategy Intent Classifier]

**Bạn sẽ thấy**

Câu *"tìm file cấu hình của dự án"* chạy lần 1 ra `read_file`, lần 2 lại ra `git_status`. Không có lỗi nào được báo, không lần gọi nào trả về lỗi — nhưng kết quả mỗi lần một kiểu và bạn không đo được độ ổn định.

Chi tiết đáng chú ý: hệ thống có **10 nhóm ý định**, mỗi nhóm liệt kê từ khoá xen tiếng Việt và tiếng Anh (nhóm `search`: "tìm", "search", "tra cứu", "lookup", "find"). Đếm từ khoá trùng rồi cộng điểm là dễ chọi nhóm điểm cao chứ không phải nhóm đúng nghĩa.

**Vì sao**

Tài liệu bày ba tầng: dò từ khoá (nhanh, rẻ), gọi mô hình để phân tích (đắt hơn, chính xác hơn), và hỗn hợp. Chạy riêng tầng 1 thì câu nhiều nghĩa rơi về nhóm điểm cao nhất, chứ không phải nhóm người dùng thật sự cần.

**Làm gì**

1. Bắt đầu bằng tầng dò từ khoá; chỉ lên tầng gọi mô hình khi **độ tin cậy dưới 0,7** — đúng ngưỡng nằm trong mã nguồn tham chiếu.
2. Nếu cả hai tầng cùng kết luận một ý định thì gộp độ tin cậy thành **0,95**. Ngược lại thì lấy kết luận của tầng gọi mô hình.
3. Tách câu nhiều ý định trước khi phân loại, bằng các từ nối `và`, `and`, `rồi`, `then`, `sau đó`; bỏ qua mảnh nào dưới 3 ký tự.
4. Ghi lại điểm của *mọi* nhóm chứ không chỉ nhóm thắng. Khi có người kêu sai, bạn thấy ngay nhóm nào bị chấm sai.
5. Nếu tầng gọi mô hình trả về JSON hỏng, rơi về tầng dò từ khoá thay vì báo lỗi.

```python
rule = self.classify_rule_based(query)
if rule["confidence"] >= 0.7:
    return rule
llm = self.classify_llm_based(query)
return llm if llm.get("confidence", 0) > rule["confidence"] else rule
```

**Kiểm tra**

Chạy bộ câu mẫu có gắn nhãn sẵn và đo riêng ba mức: tầng 1 một mình, hợp hai tầng, và tầng 2 một mình. Mục tiêu là tầng 1 đạt khoảng 90%, hợp hai tầng vượt 92%. Nếu hợp hai tầng không tốt hơn tầng 1 thì tầng 2 đang chỉ làm tốn tiền.

---

### Q3. Công cụ báo "Invalid parameters" rồi cứ thử lại mãi — xử sao? [→ §4 Tool Executor + §13 Best Practices]

**Bạn sẽ thấy**

Log đầy dòng kiểu `Invalid parameters: ['Missing required param: query']`, rồi `Failed after 3 attempts: Timeout after 30s`. Những lần gọi y hệt vẫn tiếp tục chạy vì không ai chặn ở cửa. Kết quả: một task vốn đã hỏng tốn thêm 3 lượt gọi, kéo dài độ trễ và làm nễn rate limit.

Sáu thông báo lỗi cần phân biệt được, không gộp làm một:

| Lỗi trả về | Nghĩa là |
|---|---|
| `Tool not found` | Sai tên, hoặc chưa đăng ký |
| `Tool deprecated. Use 'X' instead.` | Đã bị thay, có công cụ thay thế |
| `Invalid parameters: [...]` | Thiếu hoặc sai kiểu tham số |
| `Permission denied: ...` | Người dùng không đủ quyền |
| `Rate limit exceeded: 60s` | Vượt tần suất cho phép |
| `Failed after 3 attempts: ...` | Đã hết số lần thử |

**Vì sao**

"Bỏ qua kiểm tra tham số" và "cho thử lại không giới hạn" nằm ngay trong danh sách DON'T của chính tài liệu này. Thử lại vô hạn không làm lỗi biến mất — nó chỉ làm ví tiền của bạn biến mất.

**Làm gì**

1. Cho lệnh thực thi đi đúng thứ tự: tìm công cụ → kiểm tra đã ngừng dùng chưa → kiểm tra tham số → kiểm tra quyền → kiểm tra tần suất → mới chạy. Sai bước nào dừng bước đó, đừng chạy thử rồi mới thấy hỏng.
2. Chỉ thử lại lỗi *tạm thời* (mạng, hết giờ). Sai tham số thì thử lại vô nghĩa, kết quả y hệt.
3. Giới hạn số lần thử theo từng công cụ (`max_retries`, mặc định 3) và nghỉ giữa các lần theo kiểu nhân đôi: 0,5s → 1s → 2s, có trần 5 giây.
4. Chỉ thử lại lỗi hết giờ với việc **đọc**. Việc ghi file hay gửi email phải có khoá chống chạy hai lần.
5. Ghi lại mọi lần gọi — kể cả lần hỏng — vào sổ để `get_stats()` báo được tỉ lệ thành công và chi phí theo từng công cụ.

**Kiểm tra**

Bốn bài kiểm tra mẫu phải xanh: gọi công cụ không tồn tại thì `success` là `False` và chuỗi lỗi chứa `not found`; gọi `vector_search` không truyền tham số thì chứa `Invalid parameters`; hai lần gọi `calculator` thì `total_calls` bằng 2; gọi một công cụ đã ngừng dùng phải trả về đúng tên công cụ thay thế.

---

### Q4. Nó xoá file nhầm / ghi đè code tôi đang làm dở — chặn được không? [→ §8 Permission System]

**Bạn sẽ thấy**

Agent đọc `write_file` với một đường dẫn sai và ghi đè mất file bạn đang sửa. Không có cảnh báo nào trước đó. Lớp kiểm tra duy nhất lúc đó là "user có nhắc rõ là được ghi không" — mà mô hình không phải lúc nào cũng nhắc rõ.

**Vì sao**

Phân quyền theo vai trò (RBAC — cơ chế cho phép mỗi vai trò được dùng một tập quyền khác nhau) là lớp bảo vệ độc lập với ý thức của mô hình. Ba công cụ nguy hiểm nhất trong bộ mặc định — `sql_query`, `execute_python`, `write_file` — đều đánh dấu `requires_permission="elevated"` ngay từ lúc đăng ký.

**Làm gì**

1. Gán vai trò cho từng người và giữ bảng ánh xạ vai trò → quyền ở đúng một chỗ:

| Vai trò | Quyền có được |
|---|---|
| `guest` | `public` |
| `user` | `public`, `standard` |
| `power_user` | `public`, `standard`, `elevated` |
| `admin` | cả bốn loại |

2. Kiểm tra quyền **trước** khi thực thi, và nói rõ lý do chứ không chỉ "bị từ chối": `Role 'user' does not have 'elevated' permission`.
3. Người không xác định thì coi như `guest` — tuyệt đối không coi như admin.
4. Ghi vào sổ kiểm toán *mọi* lần quyết định, kể cả lần cho phép: ai hỏi, cần quyền gì, vai trò gì, kết quả, thời điểm.
5. Khi cần nâng quyền, cấp riêng cho đúng người (`grant_permission`) thay vì nới cả vai trò.

```python
role = self.user_roles.get(user_id, "guest")
perms = set(ROLE_PERMISSIONS.get(role, ["public"]) + custom.get(user_id, []))
return {"allowed": required_permission in perms}
```

**Kiểm tra**

Bốn bài kiểm tra phải xanh: `user` dùng được `standard`; `user` bị chặn `elevated`; `admin` qua được mọi thứ; sau khi `grant_permission("user1", "elevated")` thì `user1` qua được. Sổ kiểm toán phải có cả bản ghi `allowed: false` chứ không chỉ bản ghi thành công.

---

### Q5. Nó gọi công cụ liên tục làm cháy ví / bị API khoá IP — chặn sao? [→ §9 Rate Limiting + §17.3 Quy tắc MCP]

**Bạn sẽ thấy**

Một vòng lặp gọi cùng một công cụ hàng trăm lần trong 60 giây. Nhà cung cấp dịch vụ chặn IP, mọi thứ dừng lại. Ngay cả khi chưa bị chặn, tiền cũng đi nhanh hơn dự kiến vì không có trần nào cả.

**Vì sao**

Giới hạn tần suất không phải tuỳ chọn trang trí — nó là phao cứu sinh bảo vệ chi phí. Mặc định trong tài liệu là **60 lần/phút mỗi công cụ**, cửa sổ 60 giây. Nhưng giới hạn chỉ đặt ở tầng công cụ thì các lần gọi qua kết nối MCP từ xa vẫn không được tính.

**Làm gì**

1. Giới hạn theo cửa sổ trượt: xoá bản ghi cũ hơn 60 giây rồi mới đếm. Cách này không để lại "vết sẹp" ở ranh giới phút như cách đếm cố định.
2. Khi chặn, trả về **số giây còn phải chờ** tính từ bản ghi cũ nhất, không chỉ nói "bị chặn". Agent mới biết nên đợi hay đi làm việc khác.
3. Đặt trần thấp hơn cho công cụ tốn tiền hoặc nặng: `sql_query`, `execute_python` không nên dùng chung trần 60 với `calculator`.
4. Ở cổng MCP từ xa, chặn thêm: mỗi lần gọi tối đa **30 giây**, kết quả tối đa **128KB**, tham số gửi đi tối đa **32KB**.
5. Cài nhớ kết quả: cùng công cụ, cùng tham số, trong 60 giây thì trả lại kết quả đã lưu. Lấy mã băm của tham số làm khoá.

```python
records = [t for t in records if now - t < 60]   # cửa sổ trượt
if len(records) >= limit:
    return {"allowed": False,
            "retry_after": round(60 - (now - records[0]), 1)}
```

**Kiểm tra**

Đặt trần 3 lần/phút rồi gọi 4 lần: ba lần đầu `allowed` là `True`, lần thứ tư phải có `retry_after` trong kết quả. Kiểm tra thêm hai điều: lần gọi MCP vượt 128KB phải bị cắt kèm dòng `[truncated: result cap 128k]`, và lần gọi lại y hệt trong 60 giây phải được đánh dấu là dùng bộ nhớ đệm.

---

### Q6. Thêm một công cụ mới thì phải sửa code ở mấy chỗ — có cách nào ít sửa không? [→ §10.1 TypeScript Interfaces + §1.1 Tool Registry]

**Bạn sẽ thấy**

Bạn vừa thêm một công cụ đọc Jira. Kết quả là phải sửa danh sách nhóm ý định, sửa chỗ trích tham số, sửa chỗ xuất danh sách công cụ, sửa chỗ đo chi phí — bốn nơi. Lần sau thêm công cụ thứ hai lại sửa tiếp bốn nơi nữa.

**Vì sao**

Khi mỗi công cụ có nhiều khai báo rải rác ở các module khác nhau, công cụ mới luôn kéo theo sửa code. Một hợp đồng (interface) cố định gom hết về một chỗ và biến việc thêm mới thành việc chỉ thêm một mục.

**Làm gì**

1. Chốt một interface cho hệ thống quyết định công cụ, đủ bốn nhóm: quản lý công cụ (đăng ký / lấy / liệt kê / tìm), phân loại ý định, thực thi (đơn, chuỗi, song song), và lớp bảo vệ (kiểm tra quyền, giới hạn tần suất) cùng `getStats`.
2. Mỗi công cụ khai hết thông tin trong một hồ sơ duy nhất: `name`, `description`, `parameters`, `category`, `version`, `requiresAuth`, `requiresPermission`, `rateLimitPerMinute`, `timeoutSeconds`, `maxRetries`, `costPerCall`.
3. Cung cấp sẵn hai hàm xuất: một theo kiểu gọi hàm của OpenAI (`type: function`), một theo kiểu MCP (`inputSchema`). Nhờ vậy đổi nhà cung cấp mô hình không phải sửa từng công cụ.
4. Giữ một điểm vào duy nhất cho mọi lần gọi: kiểm tra quyền → kiểm tra tần suất → thực thi → ghi số liệu. Không để đường tắt nào bỏ qua bước đầu.
5. Bắt đầu từ bộ công cụ mặc định có sẵn rồi thêm của bạn, đừng viết lại từ đầu.

```typescript
interface ToolDefinition {
  name: string; description: string;
  parameters: Record<string, ParameterDef>;
  requiresPermission: string;
  rateLimitPerMinute: number; timeoutSeconds: number;
  maxRetries: number; costPerCall: number;
}
```

**Kiểm tra**

Thử một công cụ mới: chỉ thêm một mục đăng ký, không sửa file nào khác, rồi xác nhận nó xuất hiện trong cả hai định dạng xuất ra, được tìm thấy bởi tìm kiếm theo từ khoá, và bị chặn đúng khi người dùng thiếu quyền.

---

### Q7. Chạy cả tuần, agent vẫn hay chọn cái công cụ chậm nhất — nó tự học được không? [→ §15.1 Tool Learning]

**Bạn sẽ thấy**

Bạn có 6 công cụ tìm kiếm. Sau 1000 lượt dùng, công cụ nhanh nhất và ổn định nhất vẫn ít được chọn hơn công cụ hay lỗi, vì mô hình không có gì để biết. Số liệu thống kê đã có sẵn trong registry nhưng không ai dùng.

**Vì sao**

Hồ sơ công cụ đã lưu `success_rate` và `avg_latency_ms`, cả hai được cập nhật liên tục sau mỗi lần gọi. Thiếu mắt xích cuối cùng: dùng số liệu đó để xếp hạng lúc chọn.

**Làm gì**

1. Ghi lại mỗi lần dùng: loại công việc, tên công cụ, tham số, thành công hay không, độ trễ. Dùng khoá `loại công việc:công cụ` làm chỉ số.
2. Chấm điểm ứng viên bằng công thức `tỉ lệ thành công × (1 − độ trễ quy đổi)`, trong đó phần độ trễ chia cho 1000 và có trần một.
3. Công cụ **chưa từng dùng** cho điểm trung bình 0,5 — đủ để thử, nhưng không đủ để thắng công cụ đã chứng minh tốt.
4. Cho điểm trượt dần, không nhảy đột ngột: cập nhật độ trễ trung bình theo hệ số 0,1 cho lần mới.
5. Dùng cùng cách tính đó cho hàm tìm kiếm của registry để thứ hạng nhất quán ở cả hai nơi.

```python
rate = s["success_count"] / s["total_count"]
penalty = min(s["avg_latency"] / 1000, 1)
score = rate * (1 - penalty) if s["total_count"] else 0.5
```

**Kiểm tra**

Chạy lại hàm xếp hạng sau 500 lượt thật với một loại công việc cố định: công cụ đứng đầu phải là công cụ có tỉ lệ thành công cao nhất trong nhóm. Thử tiếp bằng cách cố tình làm một công cụ chậm đi 5 lần và xem thứ hạng có đổi không.

## code-mode-sdk.md

### Q8. Một việc 5 bước phải chờ 10-15 giây, làm sao nhanh hơn? [→ §1 Bối Cảnh + §2 Lợi Ích Cốt Lõi]

**Bạn sẽ thấy**

Một việc rất cơ bản: tìm tất cả file `.ts`, đọc từng file, thay tên một hàm cũ, chạy trình kiểm tra lỗi. Tài liệu mô tả nó thành **5 lượt** qua lại, mỗi lượt mất 1-3 giây gọi mô hình, tổng cộng 10-15 giây. Lịch sử trò chuyện còn phải gửi lại toàn bộ mỗi lượt nên token phình to.

**Vì sao**

Ở kiểu gọi công cụ thông thường, mô hình không có vòng lặp, không có điều kiện, không có bắt lỗi giữa chừng — nó chỉ suy luận từng bước một bằng ngôn ngữ. Kiểu code mode cho nó viết một chương trình duy nhất thay vì trả lời bằng JSON từng bước.

**Làm gì**

1. Để mô hình viết một đoạn TypeScript gọi bộ công cụ qua một SDK duy nhất, thay vì N lần hỏi-đáp.
2. Cấp sẵn SDK có đủ ba nhóm: đọc/ghi/tìm file, chạy lệnh hệ thống, và gọi công cụ qua MCP.
3. Chạy đoạn mã đó trong môi trường cách ly, không cho gọi mạng, giới hạn thời gian chạy và bộ nhớ.
4. Bắt mọi dòng `console.log` trong mã thành nhật ký, để bạn thấy nó làm gì thay vì một màn hình trắng.
5. Tóm tắt: tài liệu ước lượng giảm khoảng **80%** độ trễ và chi phí token; phần case study nói **70-90%**.

```typescript
import { tools } from '@deepseek-ai/dsh';
const files = await tools.findFiles('src/**/*.ts');
for (const file of files) {
  const c = await tools.readFile(file);
  if (c.includes('legacyFetch'))
    await tools.writeFile(file, c.replace(/legacyFetch/g, 'modernFetch'));
}
```

**Kiểm tra**

Chạy đúng ví dụ trên một kho mã thật và so với cách làm 5 lượt: đếm số lượt tương tác, tổng thời gian, tổng token đầu vào. Sau đó xác nhận nhật ký vẫn cho thấy từng file đã đọc và lệnh kiểm tra lỗi trả về đúng kết quả.

---

### Q9. Cho mô hình tự viết code gọi công cụ — có an toàn không? [→ §7 Best Practices & Security Guardrails]

**Bạn sẽ thấy**

Mã do mô hình sinh ra có thể ghi mọi đường dẫn, chạy lệnh hệ thống tuỳ ý, hoặc kết nối ra ngoài. Nếu bạn chạy nó bằng `eval()` hay `vm.runInThisContext()`, mã đó chạy với **đúng quyền của tiến trình chính** — tức là quyền của chính bạn.

**Vì sao**

Code mode là cách **đóng gói**, không phải ranh giới an toàn. Nó gom nhiều lượt gọi thành một lần để nhanh hơn, nhưng không làm mọi lần gọi bên trong trở nên an toàn hơn. Chỉ có cách chạy trong môi trường cô lập mới tạo ra khác biệt đó.

**Làm gì**

1. Chạy mã trong vùng tách biệt: container, luồng riêng, hoặc `vm` của Node.js. Tuyệt đối không `eval()`, không `vm.runInThisContext()`.
2. Tắt mạng mặc định; chỉ mở khi công cụ thật sự cần, và khai tên miền được phép.
3. Đặt giới hạn: thời gian chạy, bộ nhớ, số lệnh hệ thống tối đa. Giá trị mẫu trong tài liệu: 30.000 ms, 128MB, gộp tối đa 10 lệnh mỗi lượt.
4. Kiểm tra cú pháp và phân tích tĩnh trước khi chạy thật — đừng chạy thử rồi mới xem có lỗi cú pháp không.
5. Khi mã gặp thao tác không thể đảo ngược, nó phải dừng lại và hỏi, chứ không tự quyết. Cơ chế tạm dừng dùng thông điệp `PAUSED:`.
6. Yêu cầu mọi bước quan trọng đều có `console.log` để lần sau còn truy vết được.

```typescript
const ctx = vm.createContext({ dsh: this.sdk, console, setTimeout });
const s = new vm.Script(`(async () => { ${code} })();`);
return s.runInContext(ctx, { timeout: 30000 });
```

**Kiểm tra**

Cố tình cho mã viết ra `/etc/passwd`, gọi một tên miền ngoài danh sách, và chạy vòng lặp vô hạn: cả ba phải bị chặn hoặc bị giết. Rồi kiểm tra một lần gọi thao tác ghi xoá đã đi qua cổng hỏi và đã để lại bản ghi ai-duyệt-gì.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: `README.md`, `code-mode-sdk.md`.*
