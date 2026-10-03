# ❓ FAQ — Cổng duyệt (approval gates): chuyện thật, dễ hiểu

Nếu câu hỏi chưa rõ, đọc phần được nêu trong ngoặc vuông.

---

## Q1. Agent lúc 3h47 sáng tự sinh lệnh xoá cột trên production — chặn ở đâu? [→ §2 Risk Tier, §3 Gate Payload]

**Bạn sẽ thấy**

Lượt 214 của một run kéo dài sáu tiếng. Agent thấy một kiểm tra báo cột `NOT NULL` không có giá trị mặc định, mô hình "gỡ blocker" của nó thắng, nên dựng lộ trình cứu hộ bằng `ALTER TABLE users DROP COLUMN mfa_secret`. Cột đó chứa **2,1 triệu** bản ghi đăng ký xác thực hai lớp, không có bản sao lưu, và không có bản ghi hồi. Hành động không đảo ngược được và sai.

**Vì sao**

Vì cơ hội sai luôn tồn tại, và agent sai mà không biết mình sai. Tỉ lệ sai *cao* với `edit_file` trong `src/` nhưng hậu quả đảo ngược được bằng git; với `db.migrate` trên production thì tỉ lệ sai *thấp hơn* nhưng hậu quả không hoàn tác được. Nên không thể dùng một ngưỡng "rủi ro bao nhiêu" chung cho mọi việc.

**Làm gì**

1. Gắn mức rủi ro **lúc lập kế hoạch**, lấy từ bảng rủi ro toàn cục — không bao giờ để mô hình tự hạ mức cho mình.

| Mức | Ví dụ | Cách xử lý |
|---|---|---|
| `read` | đọc file, tìm kiếm | tự động duyệt, chỉ ghi log |
| `write` | sửa file trong `src/`, chạy test | xem diff + một cú bấm, hết hạn 5 phút |
| `elevated` | `db.migrate`, `deploy`, `push --force` | gõ lại xác nhận + chạy thử + lệnh hoàn tác, hết hạn 30 phút |
| `prod-auth` | đổi quyền, xoay khoá, xoá dữ liệu production | hai người duyệt + báo kênh sự cố, 4 giờ |

2. **Buộc payload có đủ bốn thứ**: diff, blast radius (danh sách tài nguyên bị chạm), kết quả chạy thử, lệnh hoàn tác đã test. Thiếu một trường thì gate không mở — đây là điều kiện kỹ thuật, không phải sự tử tế.
3. Liệt kê blast radius **từ sổ đăng ký, không để mô hình viết**: `prod-db.host=postgres-5a2f`, `database=users size=2.1M rows`, `migration lock ~4s`, `0 down migrations`. Nói chung chung kiểu "đồ production" thì con người không đánh giá được.
4. Hiển thị cả chi phí (tiền, thời gian) — nhưng chi phí là **một dòng** trong payload, không phải blast radius.
5. Ghi nhớ ranh giới với module 12: sandbox khoanh *agent được làm gì*, gate quyết *một con người đáng tin phải thấy gì trước khi nó xảy ra*.

**Kiểm tra**

Chạy lại một payload thiếu phần chạy thử → phải ném lỗi ngay. Mã băm (sha256) của diff lúc duyệt phải bằng mã băm của diff lúc thực thi; lệch là sự cố cứng, tự báo động.

---

## Q2. Để ngỏ không trả lời, có nên cho agent chạy tiếp không? [→ §4 Timeout, Deny & Escalation]

**Bạn sẽ thấy**

Một gate mức `elevated` nằm chờ từ 22h. Sáng hôm sau người duyệt mở laptop và thấy run đã tự chạy tiếp, migration đã lên production. Biến thể tệ hơn: gate hết hạn và hệ thống coi như không có gì xảy ra, run trông như đang kẹt.

**Vì sao**

Vì nếu hết hạn được hiểu là "cho qua", thì gate chỉ là một gợi ý có chân. Còn nếu đồng hồ hết hạn nằm trong phiên giao diện, đóng laptop là kéo dài đời sống gate — nên đồng hồ phải chạy trong **engine**, không phải trong ứng dụng web.

**Làm gì**

1. **Hết hạn luôn = từ chối** (fail closed). `write` 5 phút, `elevated` 30 phút, `prod-auth` 4 giờ rồi báo người trực.
2. Đánh dấu task ở trạng thái riêng `blocked(approval-timeout)`, **khác hẳn** `denied`, vì hành động tiếp theo khác nhau: deny thì lập lại kế hoạch, timeout thì loại nhánh và ghi sự kiện cảnh báo.
3. Không bao giờ diễn giải hết hạn thành approve. Ngoại lệ duy nhất được phép là cửa sổ triển khai ngoài giờ, và nó phải được viết thành policy có chữ ký, mặc định là "hết hạn = hoàn tác + báo người".
4. Ghim trạng thái gate đang chờ vào tập pin của module 14, để việc nén ngữ cảnh không làm mất nó giữa chừng.
5. Nếu gate mức `elevated` treo quá 15 phút trong giờ production thì gọi người trực. Run đứng yên nguyên vẹn tại checkpoint — chính cái đứng yên đó làm cho việc gọi người gần như miễn phí.
6. Ghi từng chặng của chuỗi chuyển báo: `paged_oncall` → `delegated_to:alice` → `approved`. Chuỗi đó là thứ khiến câu hỏi "thực sự ai đã quyết?" trả lời được.

```typescript
export function onExpire(key: string, g: Gate): void {
  g.verdict = "expired";
  traj.append({ kind: "approval_verdict",
    payload: { key, verdict: "expired", reason: "ttl_elapsed", at: Date.now() } });
  plan.markBlocked(g.taskId, "approval-timeout");
  replanner.excludeBranch(g.taskId);
}
```

**Kiểm tra**

Chạy test: mở gate → giết tiến trình → khởi động lại → đợi qua mốc hạn → verdict phải là `expired`. Test này bắt được loại lỗi đội thường bỏ: đồng hồ chết mỗi lần restart.

---

## Q3. Tôi bấm "Từ chối" rồi nó lại đưa lại đúng yêu cầu cũ, mãi mới chịu làm khác — sửa sao? [→ §4.3 Deny → Replan]

**Bạn sẽ thấy**

Bạn từ chối một thay đổi lược đồ dữ liệu, gõ lý do "chưa cần, giữ cột cũ". Hai mươi giây sau agent đưa lại **đúng payload đó**, chỉ khác mô tả. Sau ba lần bạn bấm "duyệt cho xong" để nó im — và từ đó gate chỉ còn làm trang trí.

**Vì sao**

Vì một lần từ chối không phản hồi lại thì không dạy được gì. **Lý do bạn gõ là artifact giá trị nhất** trong cả hệ thống gate: nó cho bộ lập kế hoạch biết con người từ chối cái gì, và giúp đưa chỉ dẫn đó vào bộ nhớ bền. Nếu cùng một lý do bị từ chối lặp lại, đó là tín hiệu sản phẩm — agent cứ đề xuất thứ đội không muốn — chứ không phải lỗi kỹ thuật.

**Làm gì**

1. **Bắt buộc lý do**, lưu vào sự kiện audit.
2. Deny phải kích hoạt **lập lại kế hoạch và loại nhánh** đó. Không bao giờ gửi lại nguyên xi một payload.
3. Nếu cùng kế hoạch thỏa mãn được bằng cách khác, bộ lập kế hoạch phải sinh kế hoạch mới; chỉ khi action mới thực sự ở mức cao hơn thì mới sinh gate mới.
4. Hỏi lại y hệt sau deny là lý do số một khiến người dùng bấm duyệt "chỉ để hết ồn" — tức là hệ thống tự tay phá hệ thống.
5. Cấm đường ngoại lệ "sinh thêm loại verdict lúc chạy" (coi tin nhắn Slack hay lời nói là duyệt). Chỉ `settle()` mới được ghi verdict. Bất kỳ kiểu nào "sinh ra" verdict mới lúc chạy đều là lỗ hổng policy, không phải tính năng.

**Kiểm tra**

Sau deny, hệ thống phải gọi loại bỏ nhánh **đúng một lần**. Nếu trong 5 phút sau xuất hiện một yêu cầu trùng khớp hoàn toàn với payload vừa bị từ chối, ghi cờ vi phạm "deny rồi hỏi lại" và báo động.

---

## Q4. Gate mở lúc 22h, máy restart, sáng ra thấy gate biến mất — nguy hiểm cỡ nào? [→ §5 Tích hợp Engine, §5.3 Idempotency]

**Bạn sẽ thấy**

Run vẫn ở trạng thái chờ duyệt. Bạn khởi động lại dịch vụ để vá một lỗi khác. Run tiếp tục chạy, không còn ai hỏi. Đây là lỗ hổng, không phải lỗi hiển thị: **gate trong RAM là một cơ chế kiểm soát an toàn bị mất trí nhớ.**

**Vì sao**

Vì cách làm sai phổ biến là engine "chờ": nó giữ một biến trong bộ nhớ và chờ. Nhưng engine phải **ghi checkpoint rồi mới báo tạm dừng**, nếu không thì lúc resume không phân biệt được "chưa từng chạy" với "đã chạy dở rồi". Mọi step đã xong phải nằm trong bộ nhớ đệm chống chạy lại và trong nơi lưu sự kiện.

**Làm gì**

1. Thứ tự bắt buộc: kiểm tra mức rủi ro → **ghi checkpoint** → mở gate → phát thông báo → **mới** báo tạm dừng. Đảo thứ tự là lỗi.
2. Gate và cả đồng hồ hết hạn phải nằm trong nơi lưu sự kiện. Lúc khởi động, quét lại mọi gate chưa có verdict, nạp lại chúng và **nạp lại đồng hồ**.
3. Mã tạm dừng truyền lên driver / dòng lệnh / giao diện như một **trạng thái hạng nhất, không phải lỗi**. Cú bấm "duyệt" của con người là *giao verdict*, không phải khởi động lại run.
4. Resume với **cùng mã run**; các step đã xong trúng bộ nhớ đệm nên bị bỏ qua, không chạy lại, không hỏi lại.
5. Action được gate chạy **đúng một lần** sau khi duyệt — vì checkpoint nằm *trước* action, nên resume chạy lại action chứ không băng qua ranh giới.
6. Ghi verdict trùng key hai lần là no-op: bấm đúp không được chạy migration hai lần.

```typescript
private reloadOpen(): void {
  for (const ev of this.store.query({ kind: "approval_request" }))
    if (!this.verdict(ev.payload.key)) {
      this.gates.set(ev.payload.key, ev.payload);
      this.armTimer(ev.payload);            // nạp lại đồng hồ hết hạn
    }
}
```

**Kiểm tra**

Test bắt buộc: mở gate → giết tiến trình → khởi động lại → verdict phải vẫn còn hiệu lực và đồng hồ hết hạn vẫn chạy. Test thứ hai: resume sau khi duyệt phải **thực thi đúng một lần**, không phải hai.

---

## Q5. Team tôi duyệt 98% trong 10 giây — gate còn tác dụng gì nữa? [→ §7 UX, §9.3 Bộ hồi quy]

**Bạn sẽ thấy**

Báo cáo cuối quý cho thấy tỉ lệ duyệt 98% và thời gian chờ trung vị 30 giây ở *mọi* mức rủi ro, kể cả `prod-auth`. Không ai đọc payload nữa. Sự cố xảy ra đúng ở action mà mọi người tưởng đã được duyệt.

**Vì sao**

Vì **mệt mỏi ra quyết định là kiểu hỏng thầm lặng số một**: đo thấy tỉ lệ duyệt tăng đồng thời với thời gian quyết định giảm. Nghiên cứu *automation bias* (Parasuraman & Manzey, 2010) gọi tên đúng thứ này: con người học được rằng cảnh báo thường báo động giả, nên ngừng kiểm tra thứ thật. Ba loại bằng chứng có độ tin cậy khác nhau — dry-run + diff đo được thắng một lời giải thích kiểu "tin tôi, tôi đã kiểm tra".

**Làm gì**

1. **Đo tỉ lệ duyệt và thời gian chờ trung vị theo từng mức**, chạy trong danh mục truy vấn hằng đêm. Độ dốc tăng là cảnh báo, đến trước sự cố.
2. Sửa bằng cách **nâng thanh độ khó, không phải bỏ gate**: gộp các sửa file mức `write` thành một lần xem diff duy nhất; bắt gõ lại xác nhận ở mức cao.
3. Để đường mặc định dẫn tới đáp án an toàn: nếu câu trả lời đúng thường là "từ chối", thì đường duyệt phải nhiều ma sát hơn, không phải ít hơn.
4. Xác nhận ở **độ hạt đoạn kế hoạch**, không phải từng lời gọi công cụ — xác nhận từng action là cách nhanh nhất để luyện thói quen bấm máy móc.
5. Gửi kèm bốn trường bằng chứng **nguyên vẹn qua mọi kênh**; kênh bị cắt bớt lặng lẽ hạ chất lượng quyết định. Ghi sự kiện "đã gửi thông báo" để câu "con người không bao giờ thấy nó" là điều kiểm chứng được, không phải lời bào chữa.
6. Một gate hết hạn mà không ai báo là **lỗi**, không phải chuyện vận hành bình thường.

**Kiểm tra**

Chạy hằng tuần câu hỏi so sánh tỉ lệ duyệt theo từng mức. Bất kỳ mức nào có tỉ lệ 98% và thời gian chờ dưới 10 giây phải bị đánh dấu là "đã chết" và kéo lại ngay.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: README.md.*
