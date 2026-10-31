# ❓ FAQ — Multi-Loop Coordination (những câu người thật hay hỏi)

Câu hỏi nào khó hiểu thì đọc phần trong ngoặc vuông — nó trỏ tới mục tương ứng trong README phối hợp nhiều loop. "Loop" = vòng lặp tự động chạy việc theo lịch.

---

## Q1. Tôi có 2 cái loop cùng sửa một nhánh, rồi thành đụng độ — chuyện này xử lý sao? [→ §5. Collision Detection]

Phần này giải thích cách chặn hai loop cùng sửa một nhánh git. "Branch/nhánh" = phiên bản code riêng để làm việc tạm thời; "collision" = va chạm.

**Bạn sẽ thấy**

Loop dọn CI (quét lỗi test tự động) và loop theo dõi pull request cùng nhảy vào nhánh `fix/auth-refresh` trong vòng năm phút. Kết quả là một bản vá ghép cục mở, chạy test đỏ, và cả hai báo "thành công".

**Vì sao**

Nguyên tắc thứ nhất của multi-loop là **mỗi nhánh chỉ có một chủ sở hữu tại một thời điểm** — tối đa một loop được quyền thay đổi một nhánh trong mỗi giờ. Nếu chỉ dựa vào "đọc file trạng thái rồi tự đối chiếu", vẫn có khe hở giữa thời điểm đọc và thời điểm hành động — hai loop đọc cùng lúc, cả hai thấy "chưa ai làm", rồi cả hai làm.

**Làm gì**

1. **Cho mỗi loop ghi trường `acting_on`** trong file trạng thái của nó, ghi rõ nhánh hoặc mã pull request đang xử lý — như treo biển "tôi đang làm việc này".
2. **Trước khi mở một lần sửa**, loop phải đọc các file trạng thái của các kiểu loop khác; nếu trùng `acting_on` thì bỏ qua và ghi một dòng vào file log chạy.
3. **Khoá bằng cơ chế thật thay vì bằng kỷ luật**: lấy khoá ("lock" = quyền giữ nguyên tài nguyên, ai giữ khoá thì người khác phải chờ) với tên chủ sở hữu là tên kiểu loop, và nhả khoá sau khi xong.
4. **Nhớ điểm yếu**: lệnh tạo worktree (bản sao tạm của repo để sửa code an toàn) **không** tự kiểm tra khoá, nên hai lệnh lấy và nhả phải được đặt cạnh nhau trong một kịch bản điều khiển duy nhất.

> 📄 **Code ví dụ:** [`examples/01-q1-toi-co-2-cai-loop-cung-sua.sh`](examples/01-q1-toi-co-2-cai-loop-cung-sua.sh)

**Kiểm tra**

Cho hai loop cùng thử xử lý một nhánh: một cái được phép, cái còn lại phải bỏ qua và ghi lý do vào file log chạy. Sau khi cái thứ nhất nhả khoá, lần chạy kế tiếp phải lấy được khoá.

> **Tóm gọn 1 câu:** Một nhánh một chủ: mỗi loop ghi `acting_on` lên state, đọc state của nhau trước khi làm, và dùng khoá hẳn hoi thay vì dựa vào tự giác.

---

## Q2. Hai loop cùng thấy một pull request hỏng, ai được quyền làm trước? [→ §3. Priority Khi Loops Xung Đột]

Phần này giải thích cách xếp thứ tự ưu tiên khi nhiều loop muốn làm cùng một việc. "Pull request (PR)" = đề nghị gộp code vào nhánh chính.

**Bạn sẽ thấy**

CI đỏ trên nhánh chính, mọi thứ bị chặn vì không ai gộp được ("CI đỏ" = hệ thống test tự động thất bại). Nhưng loop nâng cấp thư viện vẫn tự tạo pull request mới mỗi 6 giờ, và loop báo cáo hằng ngày cứ xếp hàng việc cũ lên đầu danh sách.

**Vì sao**

Khi hai loop muốn làm cùng một thứ, kẻ nào cháy hơn sẽ thắng. Loop làm CI đỏ chặn tất cả, vì repo không ai gộp được thì mọi việc khác đều vô nghĩa. Cần một thang ưu tiên đọc từ trên xuống, loop ở dưới tự nhường.

**Làm gì**

1. **Ghi thang ưu tiên vào tài liệu gốc của dự án** để mọi loop cùng đọc, không ai tự chế thêm.
2. **Đặt loop dọn CI ở đầu thang**, vì nó chặn mọi thứ khác.
3. **Cho loop báo cáo đứng cuối** ở mức chỉ-báo-cáo: nó không cạnh tranh với loop hành động, chỉ điều phối.
4. **Cho loop ưu tiên thấp tự dừng khi điều kiện chặn xuất hiện**, ví dụ nhánh chính đang đỏ thì loop nâng cấp thư viện không chạy.

| Ưu tiên | Kiểu loop | Vì sao |
|---|---|---|
| 1 | Dọn CI | Nhánh chính đỏ chặn mọi thứ |
| 2 | Theo dõi pull request | Pull request đang mở thì nhạy thời gian |
| 3 | Dọn thư viện phụ thuộc | Dừng lại khi CI đỏ |
| 4 | Dọn sau khi gộp | Chạy giờ thấp, ít gấp nhất |
| 5 | Báo cáo hằng ngày | Chỉ báo cáo, điều phối cái khác |

Cách đọc bảng: số "Ưu tiên" nhỏ hơn = được đi trước khi có va chạm. Ví dụ hàng 1: khi CI đỏ, loop dọn CI được làm trước vì nó làm nhánh chính sống lại được.

**Kiểm tra**

Lên kế hoạch nhịp chạy trong tài liệu gốc và xác nhận mỗi dòng có điều kiện bỏ qua ghi kèm. Cho nhánh chính đỏ thì loop ưu tiên 3 và 5 phải không mở pull request mới.

> **Tóm gọn 1 câu:** Viết thang ưu tiên cố định vào tài liệu chung: việc chặn mọi người thì đi trước, việc chờ được thì nhường và tự dừng khi điều kiện chặn xuất hiện.

---

## Q3. Mỗi loop nên ghi trạng thái vào file nào, có nên dùng chung một file? [→ §2. Recommended State Layout]

Phần này giải thích cách chia file trạng thái ("state" = file ghi trí nhớ giữa các lần chạy) cho từng loop.

**Bạn sẽ thấy**

Tất cả loop ghi vào chung `STATE.md`. Đến lượt loop dọn CI, nó dọn mục của loop theo dõi pull request vì tưởng đó là việc cũ đã xong. Hoặc tệ hơn, hai loop cùng ghi một dòng, một bên bị đè mất.

**Vì sao**

Nguyên tắc thứ hai: **mỗi loop một file trạng thái riêng**. `STATE.md` dành cho loop báo cáo hằng ngày và hộp thư chờ người; các loop hành động mỗi loop một tệp riêng — ghi chung là mời gọi ghi đè và xoá nhầm.

**Làm gì**

1. **Tách file theo vai trò**: một file cho việc báo cáo, một file cho từng loop hành động, một file ghi các bản cập nhật thư viện đang bay, một file ghi việc dọn dẹp tồn đọng.
2. **Một file log chung, chỉ thêm không sửa**, dùng để quan sát toàn cục — log chung giúp bạn thấy cả bức tranh nhiều loop.
3. **Quy định rõ rằng mỗi lần chạy phải đọc và ghi cùng một kho chứa** — bảng công việc trên Linear hoặc GitHub Projects cũng thay thế được cho các file này, miễn là điểm đọc và ghi là một.
4. **Chép cùng một danh sách đường dẫn cấm vào tài liệu của mọi loop**, không có ngoại lệ — một loop được đi đường tắt thì cả hệ thống có lỗ.

```text
STATE.md                     # báo cáo hằng ngày + hộp thư chờ người
pr-babysitter-state.md       # theo dõi pull request
ci-sweeper-state.md          # lỗi CI đang tồn + số lần đã thử
dependency-sweeper-state.md  # cập nhật thư viện đang dở
post-merge-state.md          # việc dọn tồn đọng
loop-run-log.md              # log chỉ-thêm, quan sát toàn cục
```

Cách đọc danh sách: mỗi dòng là một file và vai trò của nó. Chỉ `STATE.md` (báo cáo) và `loop-run-log.md` (log chung) dùng chung; còn lại mỗi loop một file riêng.

**Kiểm tra**

Cho mỗi loop chạy một lần rồi đếm số file được tạo. Nếu một loop ghi vào file của loop khác thì chưa đúng ranh giới. Cũng phải xác nhận danh sách đường dẫn cấm giống hệt nhau trong tài liệu của cả ba loop.

> **Tóm gọn 1 câu:** Mỗi loop một file state riêng, chung một file log chỉ-thêm — ghi chung một file là mời gọi hai loop đè dữ liệu của nhau.

---

## Q4. Loop A và loop B cùng thấy một việc mơ hồ, đẩy cho tôi ở đâu? [→ §6. Human Inbox]

Phần này giải cách gom mọi thứ cần người xử lý vào đúng một chỗ. "Mơ hồ" = việc không đủ thông tin để loop tự quyết.

**Bạn sẽ thấy**

Hai loop cùng ghi vào hai chỗ khác nhau: một cái ghi vào `STATE.md`, một cái đăng bình luận lên pull request. Cuối ngày bạn phải đọc cả hai nơi, và có một việc bị báo động hai lần.

**Vì sao**

Khi việc tìm được quá mơ hồ để kiểm chứng "đã xong" thành hay không, nguyên tắc là loop **hỏi lại hoặc báo người**, tuyệt đối không đoán. Nhưng "báo người" cũng cần một chỗ duy nhất, nếu không bạn sẽ nhận thông báo trùng — và chỗ đó là hộp thư chờ người ("human inbox").

**Làm gì**

1. **Một hộp thư chung dành cho con người**, là một mục riêng trong file trạng thái, dành cho việc mơ hồ hoặc việc tranh chấp giữa các loop.
2. **Ghi rõ ai đang tranh chấp**, ví dụ hai loop cùng cờ một mã pull request, để người chọn đúng chủ sở hữu. "Cờ" ("flag") = đánh dấu cần chú ý.
3. **Chỉ báo khi thật sự cần người hành động**, không báo mỗi lần chạy — thông báo spam khiến cả team tắt hết, và loop chết trong im lặng.
4. **Để người ghi quyết định ngược lại vào trạng thái**, để loop lần sau không hỏi lại.

```markdown
## Hộp thư chờ người (mơ hồ / tranh chấp giữa các loop)
- [ ] Pull request #42: loop dọn CI và loop theo dõi PR đều cờ — người chọn chủ sở hữu
```

Cách đọc ví dụ: đây là một mục trong file state — PR #42 bị hai loop cùng đánh dấu, người phải chọn ai xử lý; chọn xong ghi lại để các loop lần sau biết.

**Kiểm tra**

Cho một loop gặp đầu vào quá mơ hồ để kiểm chứng. Nó phải hỏi lại hoặc đẩy xuống hộp thư chung, không được tự đoán rồi sửa. Mọi quyết định của người phải được ghi lại để loop lần sau đọc được.

> **Tóm gọn 1 câu:** Tất cả việc mơ hồ và tranh chấp đổ về đúng một hộp thư chờ người — nhiều chỗ nhận việc là mời gọi bỏ sót và báo động trùng.

---

## Q5. Lần đầu chạy nhiều loop, nên bật mấy cái cùng lúc? [→ §7. Safe Three-Loop Setup]

Phần này giải cách khởi động nhiều loop an toàn — nên bật từng cái một, không bật hàng loạt.

**Bạn sẽ thấy**

Bạn bật cả bốn loop cùng lúc trong tuần đầu. Không có kiểm chứng nào hoạt động tốt, chưa có số liệu, chưa có giới hạn lần thử — rồi phải dừng cả bốn cùng một lúc để dọn dẹp.

**Vì sao**

Chạy nhiều loop trong một repo hoàn toàn bình thường. Cái nguy hiểm là chạy chúng **không có ranh giới**, không phải là chạy nhiều. Và độ tin cậy của một loop chỉ tích lũy được qua thời gian, chứ không bật lên bằng số lượng.

**Làm gì**

1. **Chọn ba loop với mức thận trọng tăng dần**: một loop chỉ báo cáo hằng ngày ở mức thấp, một loop theo dõi pull request ở mức có kiểm chứng chạy mỗi 10 phút, một loop dọn sau khi gộp chạy giờ thấp.
2. **Ghi nhịp chạy vào tài liệu gốc của dự án** để mọi loop cùng đọc, kèm điều kiện bỏ qua.
3. **Thêm loop dọn CI chỉ sau khi** loop theo dõi pull request đã chứng minh được giới hạn lần thử và bước kiểm chứng trong hai tuần.
4. **Dùng chung ngân sách token gộp**, không để mỗi loop tự tính một nửa mà không ai thấy tổng — tổng chi phí mới là thứ đâm thủng túi bạn.

| Loop | Mức | Nhịp chạy |
|---|---|---|
| Báo cáo hằng ngày | L1 | 1 ngày |
| Theo dõi pull request | L2 | 10 phút |
| Dọn sau khi gộp | L1 → L2 | 1 ngày, giờ thấp điểm |

Cách đọc bảng: bộ ba loop an toàn để bắt đầu; "Mức" = bậc tự chủ (L1 = chỉ báo cáo, L2 = tự sửa nhỏ có người kiểm); "Nhịp chạy" = tần suất. Ví dụ dòng 2: loop theo dõi PR được phép tự sửa nhỏ nhưng mỗi 10 phút một lượt và có verifier kiểm.

**Kiểm tra**

Sau hai tuần, xác nhận loop theo dõi pull request có bằng chứng đã giới hạn lần thử và có người kiểm hoạt động. Chỉ khi điều đó đúng thì mới bật thêm loop dọn CI, và cả ba phải dùng chung một danh sách đường dẫn cấm.

> **Tóm gọn 1 câu:** Bắt đầu đúng ba loop: một báo cáo, một theo dõi PR, một dọn sau merge — bật thêm loop mới chỉ khi loop cũ đã chứng minh đáng tin trong hai tuần.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: README.md.*
