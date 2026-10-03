# ❓ FAQ — Toàn cảnh harness (15 module): chuyện thật, dễ hiểu

Nếu câu hỏi chưa rõ, đọc phần được nêu trong ngoặc vuông.

---

## Q1. Harness là cái gì vậy? Tôi gọi LLM một lần là xong, cần gì 15 module? [→ §1, §3]

**Bạn sẽ thấy**

Bạn dựng một chatbot tìm kiếm: nhúng câu hỏi, tìm 50 tài liệu, chấm lại còn 5 tài liệu nhất, ghép vào prompt, gọi mô hình ngôn ngữ (LLM), trả lời. Nó chạy đẹp. Nhưng khi khách báo "lỗi đăng nhập", nó gọi một lần rồi hỏi lại: "bạn muốn tôi sửa file nào?"

**Vì sao**

Vì `prompt → completion` chỉ là một lần gọi đơn lẻ. **Harness là tất cả những gì quanh nó** biến lần gọi đó thành `request → kết quả đã được kiểm chứng`: lấy dữ liệu, xếp vào cửa sổ ngữ cảnh, chia kế hoạch, chọn công cụ, chạy, kiểm tra, rồi mới trả kết quả. RAG (tìm kiếm + sinh câu trả lời) chỉ chiếm 3 bước đầu trong sơ đồ.

**Làm gì**

1. Nhìn theo **vòng đời một request**: `01` lấy tri thức → `02` dựng ngữ cảnh → `04` chia kế hoạch + `08` đơn vị việc → `05` dựng prompt → `06` chọn công cụ → `07` chạy → `11` chấm điểm → `03` ghi nhớ.
2. Phân biệt hai vòng. Vòng trong (runtime tự quản lý): `LLM → gọi công cụ → quan sát → LLM → … → dừng`. Vòng ngoài (bạn sở hữu): `kế hoạch → chạy → kiểm tra → sửa → lưu → đo`.
3. Đừng chờ đủ 15 module mới chạy. `11` (đánh giá) là bắt buộc từ ngày đầu: không đo thì không biết mình có tiến bộ hay chỉ *cảm thấy* có.
4. Nếu RAG của bạn chạy **một lần rồi hết**, đó là chatbot trả lời tốt, không phải agent làm việc. RAG phải chạy lại mỗi nhiệm vụ và mỗi lần kế hoạch bị sửa.

**Kiểm tra**

Thử một yêu cầu cần 5 bước trở lên (sửa code rồi chạy test). Nếu hệ thống hỏi "tiếp theo bạn muốn tôi làm gì", bạn đang có chatbot chứ chưa có harness.

---

## Q2. Có phải xây đủ 15 module không, và bắt đầu từ đâu? [→ §5 Đọc thư mục này thế nào]

**Bạn sẽ thấy**

15 thư mục, ngỡ không biết bắt đầu từ chỗ nào. Người mới thường đọc `01` trước vì "retrieve" nghe hợp lý nhất, đọc xong thì vẫn không biết mình đang xây cái gì.

**Vì sao**

Vì 15 module **không phải 15 bước nối tiếp**. `01–11` là các stage của một pipeline; `12–15` là 4 module *xuyên suốt*, bọc quanh mọi stage. `01` không "chạy trước" `08` theo nghĩa phụ thuộc — ngược lại, `08-task` (đơn vị việc) là thứ mọi stage khác phải trả kết quả về. Guardrails và phân quyền vốn **không phải một stage**; chúng bọc lấy mọi mũi tên trong sơ đồ.

**Làm gì**

1. **Bản tối thiểu để chạy được**: `02 + 05 + 06 + 07 + 11`. Thêm `01`/`03` khi cần nhớ lâu, thêm `04`/`08` khi nhiệm vụ phức tạp, `09`/`10` làm cuối cùng.
2. **Nếu học để hiểu**, đọc theo thứ tự: `08` → `07` → `02` → `06` → `01` → `03` → `04` → `05` → `11` → `10` → `09`, rồi cross-cutting `12` → `13` → `14` → `15`.
3. **Nếu đang gặp sự cố**: `08` là module mỏng nhất nhưng nếu hiểu sai thì mọi thứ lệch. Bắt đầu debug ở đó.

**Kiểm tra**

Bản tối thiểu 5 module phải trả lời được 5 câu: nhiệm vụ này cần gì, chạy ở đâu, gọi công cụ nào, chạy xong thì tin gì, và làm sao biết nó đúng. Trả lời không đủ 5 câu thì chưa xong.

---

## Q3. Run báo "thành công" nhưng kết quả sai, không ai biết nó hỏng ở bước nào — làm sao? [→ §3 Lifecycle, §4 Ba contract dùng chung]

**Bạn sẽ thấy**

Run "Fix login bug" kết thúc với trạng thái thành công, nhưng agent sửa nhầm file và test vẫn đỏ. Không có gì trong log chỉ ra nó đọc sai ngữ cảnh, gọi sai công cụ, hay bị chấm sai tiêu chí.

**Vì sao**

Vì nếu không ghi lại từng bước, bạn chỉ còn prompt đầu vào và kết quả cuối — mọi thứ giữa hai đó là màu đen. Người ta hay quay về "thử lại với prompt khác", tức là đoán mò trên một hệ thống không quan sát được.

**Làm gì**

1. **Mọi bước đều phát ra sự kiện**, và sự kiện là nguồn sự thật duy nhất. Trường tối thiểu: `id`, `sessionId`, `parentTaskId`, `ts`, `kind` (`prompt` / `tool_call` / `tool_result` / `plan` / `eval` / `memory_write` / `approval`), `payload`.
2. Từ một run hỏng, **dựng lại đúng nó** thay vì chạy lại: fork (rẽ nhánh) từ đúng điểm, giữ nguyên một `sessionId`.
3. Đi theo thứ tự khi debug: đọc lại sự kiện để khoanh vùng stage hỏng, rồi mới sửa stage đó. Ba nghi phạm theo thứ tự: `02` (ngữ cảnh sai?), `06` (sai công cụ?), `11` (sai tiêu chí chấm?).
4. Dùng **ba hợp đồng chung** làm mốc nối khi tra cứu: sự kiện trajectory; ngữ cảnh đã dựng (có `budget: { limit, used }` để thấy ngữ cảnh có bị ép không); và node việc (có `idempotencyKey` để biết bước nào đã chạy rồi).

**Kiểm tra**

Một run bất kỳ phải dựng lại được từ log: đúng prompt nào, đúng lời gọi công cụ nào, đúng kết quả nào, bao nhiêu token. Run nào không dựng lại được thì chưa đạt.

---

## Q4. RAG của tôi đã xong, có cần mấy module phía sau không? [→ §3.1 RAG pipeline nằm ở đâu]

**Bạn sẽ thấy**

Pipeline của bạn đúng chuẩn: tìm lại → chấm lại → ghép prompt → gọi LLM. Nhưng khi người dùng yêu cầu "sửa lỗi này rồi chạy test", hệ thống báo là không làm được vì không có công cụ nào cả.

**Vì sao**

Vì RAG **kết thúc đúng ở lần gọi LLM đầu tiên**. Từ đó trở đi là phần harness tiếp quản: `04` lập kế hoạch, `06` chọn và kiểm soát công cụ, `07` chạy, `11` chấm, `03` ghi lại. Thiếu phần đó thì mô hình chỉ có thể *nói* chứ không *làm*.

**Làm gì**

1. Nhớ đúng vị trí từng mảng: tìm lại (①) và chấm lại (②) thuộc `01`; dựng ngữ cảnh (③) thuộc `02` + `05`; từ đó là `04 → 06 → 07 → 08 → 11 → 03`.
2. RAG **không chạy một lần**: mỗi task mới, mỗi lần kế hoạch bị sửa, đều phải tìm lại từ đầu.
3. Nếu sản phẩm chỉ cần trả lời câu hỏi thì `01 + 02 + 05 + 11` là đủ — nhưng hãy chấp nhận đó là chatbot.
4. Khi cần "làm" thì chuyển sang bản tối thiểu `02 + 05 + 06 + 07 + 11`.

**Kiểm tra**

Đưa một yêu cầu cần thao tác (sửa file rồi chạy test) vào hệ thống. Nếu nó trả lời bằng văn bản thay vì làm, bạn mới dừng ở RAG.

---

## Q5. Module nào hay bị bỏ qua, coi là phụ? [→ §2 Bản đồ, §7 Gap đã biết]

**Bạn sẽ thấy**

Đội làm xong 11 stage rồi bỏ qua 4 module cuối vì "đó là hạ tầng, tính sau". Vài tuần sau agent bị treo vì ngữ cảnh tràn, không ai biết lúc nén đã bỏ mất những gì, và một lần `deploy` chạy không hỏi ai.

**Vì sao**

Vì `12–15` không nằm trên đường chính của sơ đồ nên trông như phụ. Nhưng chúng bọc **mọi** mũi tên: sandbox (`12`) là trần kỹ thuật, quan sát (`13`) là đôi mắt, compaction (`14`) là điều kiện để một run sống, approval (`15`) là cửa dừng có chủ đích.

**Làm gì**

1. Đừng bỏ `13` và `14` trước tiên: không có `13` thì `14` không audit được; không có `14` thì mọi run dài đều chết.
2. `12` và `15` là hai module "cho thiệt" — thiếu một thì hệ thống vẫn chạy nhưng nhiều kém hẳn.
3. Dễ đặt nhầm là `08-task`: nó mỏng nhất, nhưng là đơn vị mọi thứ khác phải trả về.
4. Biết trước phần **chưa có module nào sở hữu** để khỏi tưởng đã phủ: quét dữ liệu cá nhân / khoá bí mật, cách ly giữa các khách hàng, và mục tiêu chi phí theo từng nhiệm vụ.

**Kiểm tra**

Lập một checklist 15 dòng, đánh dấu cái nào bạn thực sự có và cái nào mới chỉ có tên. Bốn module `12–15` còn trống là tín hiệu sớm của ba loại sự cố nặng nhất.

---

## Q6. Khi agent làm sai, làm sao biết là do harness hay do model? [→ §3, §4]

**Bạn sẽ thấy**

Một yêu cầu fail. Bạn đổi prompt thử lại, vẫn fail. Đổi sang model khác, vẫn fail. Không biết nên sửa code hay đổi mô hình — và cả hai đều tốn hàng tuần.

**Vì sao**

Vì nếu không đo riêng từng tầng, mọi lỗi đều bị quy về "model". Nhưng phần lớn lỗi thật nằm ở tầng harness: ngữ cảnh sai, công cụ không có, tiêu chí chấm sai, run không ghi lại gì để mà debug.

**Làm gì**

1. Chạy lại **cùng một yêu cầu, cùng prompt giống hệt, cùng model, 3 lần**. Nếu model đáp 3 kiểu khác nhau thì đây là bài toán mô hình — và nó đòi `11` đo được.
2. Nếu **mọi run** đều dính cùng một kiểu lỗi, đó là lỗi harness. Sáu dấu hiệu thường gặp:

| Dấu hiệu bạn thấy | Module đáng nghi |
|---|---|
| Chết ở lượt ~40, báo ngữ cảnh đầy | `14` |
| Quên yêu cầu ban đầu sau khi làm việc dài | `14` |
| Lệnh nguy hiểm chạy không hỏi, hoặc không bị chặn | `12` + `15` |
| Không tra lại được một run đã qua | `13` |
| Đọc nhầm tài liệu, trả lời sai nguồn | `01` + `02` |
| Báo "xong" nhưng test vẫn đỏ | `11` |

3. Kiểm tra ba hợp đồng chung: mọi sự kiện có `id`, `sessionId`, `kind` không; ngữ cảnh đã dựng có bao giờ vượt `budget.limit` không; `idempotencyKey` có chống chạy lại không.
4. Nhớ một điềm xấu: **run kết thúc với trạng thái thành công không phải bằng chứng đúng** — đúng loại lỗi mà nén ngữ cảnh sinh ra nhiều nhất.

**Kiểm tra**

Bộ hồi quy chạy đêm trên bản ghi thật. Khi có một fail cụ thể, tra bản ghi đó và chỉ ra được stage hỏng trong vòng 15 phút. Không làm được thì `13` chưa xong.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: README.md.*
