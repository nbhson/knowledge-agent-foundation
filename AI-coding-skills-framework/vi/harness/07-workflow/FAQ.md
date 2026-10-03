# ❓ FAQ — Workflow và plugin (chuyện thật, dễ hiểu)

Nếu câu hỏi chưa rõ, đọc phần được nêu trong ngoặc vuông.

---

## README.md

### Q1. Chạy giữa chừng thì lỗi, phải làm lại từ đầu cả chuỗi — sửa sao? [→ §4.1 Retry Strategies]

**Bạn sẽ thấy**

Một workflow nhiều bước chạy tới bước 4 thì dịch vụ ngoài trả lỗi mạng. Bạn thử lại ngay lập tức — và lần này 20 request của bạn cùng đổ xuống một server vốn đã quá tải, khiến nó sập hẳn thay vì hồi phục. Vài phút sau cả 20 đều thất bại.

**Vì sao**

Thử lại ngay lập tức và cố định không chỉ vô dụng mà còn gây hại. Khi nhiều người cùng làm một việc trong cùng một khoảnh khắc, họ dồn đúng một lúc — thuật ngữ gọi là "đàn bò lao tới". Hai cơ chế trong tài liệu chống đúng việc này: nghỉ tăng dần và cộng thêm khoảng nhiễu ngẫu nhiên.

**Làm gì**

1. Cho mỗi bước một trần số lần thử. Mặc định trong tài liệu là 3 lần, không có trần là lỗi.
2. Nghỉ tăng dần giữa các lần: 1s → 2s → 4s, và có trần 60 giây để không chờ vô hạn.
3. Cộng khoảng nhiễu ngẫu nhiên vào thời gian chờ — nhân với một số ngẫu nhiên trong khoảng 0,5 đến 1,5. Hai ứng dụng lỗi cùng lúc sẽ không còn trùng nhịp.
4. Khi hết số lần thử thì ném một lỗi riêng nói rõ "đã hết 3 lần, lỗi cuối cùng là gì", thay vì trả về lỗi cuối cùng trần trụi.
5. Chỉ thử lại lỗi *tạm thời*. Lỗi sai tham số hay sai quyền thì thử lại 3 lần cũng vẫn hỏng.

```python
wait = backoff_factor * (2 ** (attempt - 1))
wait = min(wait * (0.5 + random.random()), max_backoff)   # có nhiễu
```

**Kiểm tra**

Mô phỏng một dịch vụ luôn lỗi 2 lần rồi thành công: workflow phải đi qua sau 3 lần gọi. Mô phỏng 10 tiến trình cùng gọi vào một dịch vụ chỉ chịu được 3 request mỗi giây: không được có lần thử nào đều đặn trùng nhịp. Và kiểm tra lỗi cuối cùng trả về có nêu rõ số lần đã thử.

---

### Q2. Một dịch vụ chết làm cả hàng đợi workflow kẹt theo — chặn sao? [→ §4.2 Circuit Breaker Pattern]

**Bạn sẽ thấy**

Một API bên ngoài trả về lỗi. Workflow của bạn vẫn tiếp tục gọi nó hàng trăm lần, mỗi lần đều thất bại sau khoảng 30 giây chờ. Kết quả là mọi bước sau bị xếp hàng chờ một dịch vụ đã chết, và bạn mất nhiều phút chỉ để nghe thông báo "timeout" lặp lại.

**Vì sao**

Thử lại chữa được lỗi tạm thời, nhưng không chữa được lỗi khi dịch vụ đã chết hẳn. Với dịch vụ đã chết, gọi tiếp chỉ tốn thời gian và làm nghẽn lan truyền. Cần một lớp trên nữa: ngắt dòng điện khi dòng lỗi quá dày — đó chính là "cầu chì".

**Làm gì**

1. Cài một cầu chì quanh **mỗi dịch vụ ngoài**, không phải quanh cả workflow. Đặt ngưỡng 5 lần lỗi liên tiếp thì ngắt.
2. Ngắt thì **chặn ngay** mọi lời gọi tiếp theo, không phải chờ thử rồi mới biết. Thông báo lỗi phải kèm số giây còn phải chờ.
3. Sau 30 giâi thì mở nửa để thử lại đúng **1 lần** — đừng mở cho cả đàn.
4. Chỉ khi lần thử đó **thành công** và thành công liên tiếp (tài liệu dùng ngưỡng 2) mới đóng lại cầu chì, đặt bộ đếm lỗi về 0.
5. Ghi lại mọi lần chuyển trạng thái kèm số lỗi tích luỹ. Danh sách này là manh mối duy nhất biết dịch vụ nào đang chết.

| Trạng thái | Nghĩa là |
|---|---|
| `CLOSED` | Bình thường, vẫn gọi |
| `OPEN` | Đủ lỗi, chặn không cho gọi |
| `HALF_OPEN` | Hết thời gian chờ, thử đúng 1 lần |

**Kiểm tra**

Làm một dịch vụ luôn lỗi: sau 5 lần gọi, lần thứ 6 phải bị từ chối ngay với thông điểp có số giây chờ. Chờ hết 30 giây rồi cho dịch vụ hoạt động trở lại: phải mất đúng 2 lần thành công mới đóng lại. Thử lại với dịch vụ vẫn chết: nó phải quay lại `OPEN` chứ không kẹt vô hạn ở `HALF_OPEN`.

---

### Q3. Bước 4 hỏng sau khi 3 bước đã thành công — làm sao hoàn tác? [→ §4.3 Saga Pattern]

**Bạn sẽ thấy**

Workflow đặt vé máy bay → đặt khách sạn → trả bảo hiểm → xác nhận. Bước 3 thất bại. Tiền khách sạn đã bị trừ, vé máy bay đã ra khỏi tài khoản, nhưng hệ thống báo "thất bại" và dừng — bạn phải tự đi hoàn tiền khách sạn bằng tay.

**Vì sao**

Không thể xoá được một giao dịch đã xảy ra với dịch vụ bên ngoài. Cách duy nhất là bù lại bằng một giao dịch ngược lại. Mỗi bước phải đi kèm một bước hoàn tác, và khi bước nào hỏng thì chạy ngược các bước hoàn tác của những bước đã thành công trước đó — theo thứ tự ngược.

**Làm gì**

1. Khai mỗi bước gồm hai phần: hành động chính và hành động bù (compensation). Bước nào cũng phải có cả hai, kể cả bước đầu tiên.
2. Hành động bù phải **lặp lại được** — chạy hai lần vẫn cho cùng kết quả, vì có khi nó bị gọi lại.
3. Chạy bù theo đúng thứ tự ngược: hỏng ở bước 3 thì bù bước 2 trước, bước 1 sau.
4. Bù cũng cần số lần thử riêng. Nếu bù hỏng, ghi lại rõ bước nào không hoàn tác được thay vì im lặng.
5. Ghi rõ vào nhật ký từng lần bù: bước nào, hành động gì, kết quả ra sao.

```python
@dataclass
class SagaStep:
    name: str
    action: Callable
    compensation: Callable   # hàm hoàn tác, chạy khi bước sau hỏng
    max_retries: int = 3
```

**Kiểm tra**

Mô phỏng hỏng ở từng bước một và xác nhận thứ tự hoàn tác là ngược lại đúng thứ tự đã chạy. Thêm một lần chạy trong đó bước hoàn tác đầu tiên hỏng: hệ thống phải báo tên bước không hoàn tác được. Cuối cùng, chạy một ca hoàn toàn thành công và xác nhận không có bước bù nào bị kích hoạt.

---

### Q4. Khởi động lại máy là agent mất sạch tiến độ — làm sao nhớ? [→ §13.2 Checkpoint-Resume]

**Bạn sẽ thấy**

Workflow đang ở bước 12/20 thì container bị giết (lệnh `kill -9`). Mở lại, mọi thứ bắt đầu lại từ bước 1. Bạn vừa mất 10 phút gọi mô hình, vừa có nguy cơ bước 5 làm tác dụng phụ lần thứ hai.

**Vì sao**

Workflow chạy trong bộ nhớ thì bị giết là mất trắng. Muốn tiếp tục được thì phải **ghi xuống đĩa liên tục** và phải ghi **trước** khi bước đó được coi là xong — không ghi sau thì một lần giết đúng giữa chừng vẫn mất thông tin.

**Làm gì**

1. Ghi sổ trước: mỗi khi một bước xong, thêm một dòng `{seq, stepId, inputHash, status, outputRef}` vào tệp nhật ký, rồi mới chuyển sang bước sau.
2. Định kỳ chụp ảnh trạng thái (snapshot) — không cần mỗi bước, cứ sau mỗi N bước. Lưu thành JSON hoặc SQLite ở máy local.
3. Khi khởi động lại: đọc ảnh trạng thái → phát lại phần đuôi nhật ký → bỏ qua bước đã xong → chạy tiếp bước đang dở.
4. Giữ mã lần chạy (`runId`) **ổn định qua mọi lần khởi động lại**. Đổi mã là toàn bộ nhật ký cũ mất hiệu lực.
5. Kết quả một bước vượt 64KB thì không nhét vào nhật ký — lưu ra kho kết quả riêng và chỉ ghi mã tham chiếu.

```typescript
this.ckpt({ runId, key, status: "ok",
            val: JSON.stringify(out).slice(0, 64_000), at: Date.now() });
```

**Kiểm tra**

Chạy một workflow dài, giữa bước 8 thì `kill -9`. Khởi động lại với **cùng `runId`** và xác nhận nó bắt đầu từ bước 9, không phải bước 1. Đổi `runId` và xác nhận nó chạy lại từ đầu — đúng như thiết kế. Sau đó kiểm tra một bước ghi file chạy đúng một lần, không phải hai.

---

### Q5. Chạy lại một bước là ghi trùng dữ liệu, hàng đợi thì nổ — chặn sao? [→ §13.3 Idempotency + Backpressure + Deadline]

**Bạn sẽ thấy**

Hai triệu chứng xuất hiện cùng lúc. Một: bạn chạy lại một bước ghi hóa đơn, và khách bị tính tiền **hai lần**. Hai: bạn bật 20 bước song song, bộ nhớ tăng vọt rồi tiến trình bị hệ điều hành giết.

**Vì sao**

Đây là hai lỗi khác nhau cùng một nguyên nhân gốc: hệ thống không biết "công việc này đã làm rồi" và không biết "đã đến giới hạn". Khóa là chống chạy hai lần; hạn mức là chống dồn ép.

**Làm gì**

1. Khoá chống chạy hai lần = mã bước + mã băm đầu vào (+ số lần thử tối đa). Cùng khoá trong thời hạn lưu trữ thì trả lại kết quả đã lưu, không gọi lại.
2. Chỉ bắt buộc khoá cho việc **ghi**. Việc đọc không cần, và bắt khoá cả đọc sẽ làm chậm hệ thống vô ích.
3. Đặt khoá một hạn (TTL) hợp lý. Giữ vĩnh viễn thì bộ nhớ phình và lần sửa sai sẽ không bao giờ chạy lại được.
4. Đặt trần song song toàn cục bằng một tín hiệu đếm (semaphore), tài liệu gợi ý 4-8. Giới hạn riêng độ dài hàng đợi, ví dụ 100.
5. Khi hàng đợi đầy, ném lỗi chuyên biệt để bên gọi biết phải thử lại sau — **không** được tăng hàng đợi vô hạn, đó chính là cách tự giết mình.
6. Mỗi lần chạy có **một** mốc hết giờ duy nhất. Mỗi bước nhận phần thời gian còn lại trừ chút đệm, và truyền xuống qua `AbortSignal.timeout`. Tuyệt đối không âm thầm nới thêm.

```python
key = f"{runId}:{step.id}:{hashlib.sha256(json.dumps(inputs).encode()).hexdigest()}"
if cached is not None:
    return cached                      # đã làm rồi, trả lại kết quả cũ
```

**Kiểm tra**

Gọi lại một bước ghi đúng hai lần với cùng khoá và xác nhận hệ thống ngoài chỉ nhận **một** lần ghi. Đặt trần song song 4 rồi bắn 10 bước cùng lúc: phải thấy 4 chạy trước, phần còn lại phải chờ, và không lần nào phải chờ quá độ dài hàng đợi cho phép. Cuối cùng, đặt hết giờ ngắn và xác nhận tín hiệu huỷ truyền tới từng bước chứ không phải chỉ bước ngoài cùng.

---

### Q6. Workflow 30 bước chạy xong không biết hỏng ở đâu — làm sao thấy? [→ §5 Observability]

**Bạn sẽ thấy**

Nhật ký của bạn có 20.000 dòng chữ tự do, trộn lẫn mọi lần chạy. Khi nó chậm bất thường bạn không biết là bước nào chậm, khi nó lỗi bạn không biết lỗi lan từ đâu ra. Mỗi lần điều tra là đọc lại toàn bộ tệp log.

**Vì sao**

Nhật ký dạng văn bản tự do không lọc được. Ba loại dữ liệu tách bạch là chìa khoá: **log** (có cấu trúc, dạng JSON) để tìm chuyện gì xảy ra, **số đo** (metric) để biết bao nhiêu và bao lâu, và **dấu vết** (trace) với một mã duy nhất để biết chúng thuộc cùng một lần chạy nào.

**Làm gì**

1. Gán mỗi lần chạy một mã duy nhất (`trace_id`), rồi truyền mã đó xuyên suốt mọi bước. Đây là thứ cho phép bạn lọc ra đúng một lần chạy giữa hàng nghìn lần.
2. Với mỗi bước, mở một khoảng thời gian (span) cha–con theo đúng thứ bậc thật: bước cha chứa các bước con. Nhờ vậy bạn dựng lại được toàn bộ hành trình.
3. Ghi log ở dạng JSON có trường cố định: tên workflow, tên bước, trạng thái, thời điểm, thời lượng, dữ liệu kèm theo. Không có mẫu cố định thì không lọc nổi.
4. Ghi mỗi bước **hai dòng**: một dòng `start`, một dòng kết quả (`success` hoặc `error` kèm thông điệp lỗi). Nhờ vậy bước chết treo cũng lộ ra.
5. Tính độ trễ theo ba mốc chứ không chỉ trung bình: p50, p95, p99. Trung bình che mất đúng cái đuôi chậm — p95 mới là trải nghiệm thật.

```python
summary = {"p50": sorted_vals[n // 2],
           "p95": sorted_vals[int(n * 0.95)],
           "p99": sorted_vals[int(n * 0.99)]}
```

**Kiểm tra**

Chạy 100 lần và xác nhận lọc theo `trace_id` ra đúng một lần chạy đầy đủ các bước. Cố tình làm một bước chậm 5 giây và xác nhận nó hiện rõ ở p95 chứ không bị trung bình nuốt mất. Rồi giết một bước đang chạy và xác nhận trong log xuất hiện dòng `start` không có dòng kết quả — đó chính là dấu hiệu bước bị treo.

---

### Q7. Muốn dừng lại chờ người duyệt giữa chừng rồi chạy tiếp — làm sao? [→ §13.4 Node phê duyệt / Tạm Dừng-Tiếp Tục]

**Bạn sẽ thấy**

Workflow đã tạo xong nhánh mới và sắp chạy lệnh triển khai. Bạn muốn hỏi đồng nghiệp duyệt, nhưng không có cách nào dừng giữa chừng — hoặc bạn dừng thật rồi mất toàn bộ tiến độ, hoặc bạn cho chạy luôn rồi huỷ tay sau.

**Vì sao**

Dừng giữa chừng theo kiểu "thoát ra rồi quay lại" là mất trắng, vì trạng thái nằm trong bộ nhớ. Muốn dừng mà không mất gì thì lúc dừng phải **ghi trạng thái xuống đĩa trước, rồi mới báo ra ngoài** — ngược thứ tự thì vẫn mất dữ liệu.

**Làm gì**

1. Đánh dấu bước cần duyệt bằng một cờ. Khi chạy tới bước đó, đưa lần chạy vào trạng thái `WAITING_APPROVAL`.
2. **Ghi checkpoint bền trước**, rồi mới phát tín hiệu `PAUSED:<mã bước>` ra ngoài. Không bao giờ báo dừng trước khi lưu.
3. Xử lý ba trường hợp sau khi dừng: được duyệt, bị từ chối, và hết thời gian chờ. Không để trường hợp thứ ba chỉ xảy ra trong đầu.
4. Chạy lại bằng **cùng `runId`** để các bước đã xong được bỏ qua và bước đang chờ được mở lại.
5. Ghi lại cả yêu cầu duyệt lẫn phán quyết, ai quyết, lúc nào, với nội dung gì.

```typescript
if (s.needsApproval && this.approvals.get(key) !== "ok") {
  this.ckpt({ runId, key, status: "waiting_approval", at: Date.now() });
  throw new Error(`PAUSED:${s.id}: awaiting approval`);
}
```

**Kiểm tra**

Cho workflow dừng ở bước duyệt rồi khởi động lại tiến trình: xác nhận bước đó vẫn ở `WAITING_APPROVAL` chứ không chạy lại. Duyệt rồi chạy lại: nó đi tiếp từ bước sau. Từ chối: nó bỏ qua nhánh đó và tiếp tục phần còn lại. Không phản hồi gì: nó dừng hẳn chứ không chạy âm thầm.

## cordis-kernel-plugin.md

### Q8. Code của tôi mỗi lần sửa một chức năng là phải sửa 5 file — có cách nào cắm thêm mà không đụng vào cả rồng? [→ §2 Kiến Trúc Micro-Kernel + §5 Kernel Engine]

**Bạn sẽ thấy**

Bạn thêm một tính năng nhỏ: mỗi lượt gọi công cụ đều cần ghi lại nhật ký. Bạn phải sửa ở điểm khởi tạo, ở vòng lặp gọi công cụ, ở nơi xử lý kết quả, ở phần khởi tạo phiên, và ở nơi dọn dẹp khi kết thúc. Một thay đổi nhỏ, năm chỗ sửa.

**Vì sao**

Khi nghiệp vụ nằm trực tiếp trong lõi, mọi tính năng mới đều phải chen vào lõi. Kiến trúc hạt nhân vi mô đảo ngược điều đó: lõi chỉ giữ ba việc — quản lý vòng đời, tra cứu dịch vụ, và phát sự kiện. Mọi thứ khác là plugin.

**Làm gì**

1. Một plugin chỉ cần hai hàm: tên và `apply(ctx)`. Trong `apply` nó đăng ký dịch vụ hoặc đăng ký hàm lắng nghe sự kiện.
2. Các plugin **không import trực tiếp vào nhau**. Chúng lấy dịch vụ của nhau qua lõi: `ctx.inject('ten-dich-vu')`. Đây là nguyên tắc quan trọng nhất của kiến trúc này.
3. Việc ghi nhật ký là một plugin trung gian độc lập: nó chỉ đăng ký hàm lắng nghe sự kiện `before-tool-call`, không biết công cụ là gì.
4. Đặt trạng thái vào lõi qua `ctx.provide()` chứ đừng dùng biến toàn cục — nếu không hai plugin sẽ tranh nhau ghi đè.
5. Khi gỡ một plugin, lõi phải tự dọn các hàm lắng nghe và giải phóng tài nguyên đã khai trong `apply`.

```typescript
const LoggerPlugin = {
  name: 'logger-plugin',
  apply: (ctx: Context) => {
    ctx.on('before-tool-call', (toolName: string) =>
      console.log(`[Event Stream] About to call tool: ${toolName}`));
  }
};
```

**Kiểm tra**

Đếm số file phải sửa khi thêm một tính năng có ghi nhật ký: nếu là 1 file plugin và 1 dòng khai báo nạp thì kiến trúc đang đúng. Thử xoá plugin đó và xác nhận không còn dòng nhật ký nào được ghi. Rồi nạp lại và xác nhận nhật ký quay lại mà không cần sửa lõi.

---

### Q9. Muốn chạy thử agent mà không cho nó toàn bộ công cụ — làm sao? [→ §4 Bốn Runtime Modes]

**Bạn sẽ thấy**

Bạn muốn biết mô hình có thật sự giỏi hay chỉ giỏi nhờ hệ thống công cụ. Nhưng khi bật cả bộ công cụ đầy đủ kèm lời dẫn dài vài trang, bạn không phân biệt được kết quả đến từ đâu.

**Vì sao**

Vì cùng một mô hình có thể tốt ở một chế độ và tệ ở chế độ khác, chỉ vì lượng hỗ trợ khác nhau. Cùng một bài kiểm tra, chạy hai lần với hai lượng hỗ trợ khác nhau là hai phép so sánh khác nhau.

**Làm gì**

1. Định nghĩa bốn chế độ chạy, mỗi chế độ là một plugin riêng nên bật/tắt được:
   - **Standard** — đủ bộ công cụ (file, tìm kiếm, git, trình duyệt, MCP) cho phiên tương tác nhiều lượt.
   - **Code Mode** — nạp plugin thực thi bằng SDK, gọi công cụ trong một lượt thay vì nhiều lượt.
   - **Minimal** — nạp plugin môi trường tối giản, chỉ mở đúng **hai** công cụ `bash` và `editor`, bỏ hết lời dẫn dài.
   - **Creator** — nạp plugin kiểm tra trạng thái, xem và sửa lời dẫn dài, xuất bản bộ cấu hình.
2. Dùng **Minimal** khi muốn đo năng lực suy luận gốc của mô hình trên một bài đo như SWE-bench. Công cụ và lời dẫn phải giống nhau cho mọi mô hình bạn so sánh.
3. Dùng **Standard** khi bạn thực sự cần một trợ lý làm việc.
4. Nguyên tắc chung: nếu không nói rõ chế độ nào được dùng thì kết quả không so sánh được với ai.
5. Ghi tên chế độ vào kết quả chạy. Bản báo cáo không ghi chế độ là bằng chứng không dùng được.

```typescript
// Cấu trúc thư mục phản ánh đúng triết lý: mỗi chế độ là một plugin
packages/{core, dsh, runtime-standard, runtime-code, runtime-minimal, web-ui}
```

**Kiểm tra**

Chạy cùng một bài toán ở chế độ Minimal và Standard, lưu lại tên chế độ cùng kết quả. Đổi sang một mô hình khác và chạy lại y hệt: lần này sự khác biệt là của mô hình, không phải của lời dẫn dài. Kiểm tra thêm rằng ở chế độ Minimal, danh sách công cụ trả về đúng hai mục.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: `README.md`, `cordis-kernel-plugin.md`.*
