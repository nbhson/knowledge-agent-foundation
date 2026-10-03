# ❓ FAQ — Nén ngữ cảnh (compaction): chuyện thật, dễ hiểu

Nếu câu hỏi chưa rõ, đọc phần được nêu trong ngoặc vuông.

---

## Q1. Agent chạy tầm 40 lượt là dừng, báo lỗi "context length exceeded" — phải làm gì? [→ §2 Policy Trigger]

**Bạn sẽ thấy**

Run chết ở lượt 47 với lỗi độ dài ngữ cảnh, sau khi đã viết lại 4 file và chạy 2 bộ test. Khi mở log ra xem, ngữ cảnh đã ở 96% *trước khi* chết, và kết quả lệnh kế tiếp dài 4.000 token, không vừa. Người dùng ngồi đợi 20 phút rồi mới biết "có gì đó sai".

**Vì sao**

Vì không có gì tự nén lại. Cửa sổ ngữ cảnh là con số cứng (200k, 128k hay 32k token), còn mỗi lượt agent thêm vài nghìn token. Phép tính: với ngân sách 128k và mỗi lượt khoảng 4k token thì hết hạn ở lượt 32; với 32k thì chỉ còn 16 lượt. Bật nén ở mốc 90% là sai — một lần đọc file 30 KB ăn mất 8% ngân sách trong *một* lượt, nên 90% + 8% = 98%, và lượt kế tiếp là tràn.

**Làm gì**

1. Bật nén tự động khi dùng trên **70%** ngân sách, hoặc quá **20 lượt** — cái nào tới trước.
2. Luôn chừa 30% trống, đủ chứa 2–3 kết quả lệnh kế tiếp.
3. Dùng **một** bộ code cho cả hai đường: bấm tay và tự động. Claude Code làm vậy — người dùng gõ `/compact` nhận đúng chất lượng như đường tự động, không có trải nghiệm hạng hai.
4. Đừng bật ở 50%: quá hăng hái, mỗi run nén 2 lần, tốn lời gọi mô hình lẫn chất lượng.
5. Nén ở **ranh giới nhiệm vụ** (giữa hai việc), không nén giữa một việc đang dở.
6. Tuyệt đối không để mô hình tự quyết "có nên nén không" — hỏi nó thì nó trả lời "không, tôi ổn" khi đang giữ 195k token.

```typescript
export const COMPACT_AT = 0.70, MAX_TURNS = 20;
export function shouldCompact(used: number, budget: number, turns: number): boolean {
  return used / budget > COMPACT_AT || turns > MAX_TURNS;
}
```

**Kiểm tra**

Đo `ratio = token_trước ÷ token_sau` sau mỗi lần nén; dưới **1,5** khi ngữ cảnh lớn là bộ nén đang hỏng. Sau khi bật nén, nếu vẫn còn tỉ lệ run chết vì độ dài ngữ cảnh thì đó là lỗi cấu hình, không phải lỗi mô hình.

---

## Q2. Tôi cắt bỏ lịch sử cũ cho nhẹ, xong agent quên mất yêu cầu ban đầu và đọc lại file nó vừa sửa — tại sao? [→ §3 Pin set, §4 Pruning theo utility]

**Bạn sẽ thấy**

Sau lần nén, agent đọc lại một file đã đọc ở lượt 12 (vì *kết quả* đã mất nhưng *bản sửa* của nó vẫn còn), rồi sinh ra một bản vá hủy đúng công sức nó bỏ ra ở lượt 30. Run vẫn kết thúc "thành công". Mở log thấy nó giữ lại 3 lần `ls` ở lượt 38–40 và vứt bỏ ràng buộc "không thêm dependency" ở lượt 12 — vốn chỉ 80 token mà vẫn còn hiệu lực.

**Vì sao**

Vì cách loại "cũ nhất đi trước" giả định giá trị suy giảm theo tuổi. Trong một lượt sửa code thì sai: lượt 1 (mục tiêu) cách đây 4 giờ vẫn là điều kiện quyết định kết quả đúng hay sai. Giá trị nằm ở quan hệ với việc đang làm, không nằm ở tuổi. Và giữ lại `ls` chỉ vì nó "gần đây" là lãng phí token nơi cần nhất.

**Làm gì**

1. **Ghim (pin)** những thứ mất đi thì sai *nhiệm vụ*: system prompt, yêu cầu + tiêu chí xong, chỉ dẫn cuối của người dùng, diff đang sửa, ràng buộc từ kế hoạch, lỗi cuối của vòng lặp đang chạy, approval đang chờ, hình dạng kết quả cần trả về.
2. **Chấm điểm để loại**, không loại theo tuổi. Ba thành phần: mới/cũ (0,30), span này có đang nuôi một việc *đang chờ* trong đồ thị kế hoạch không (0,40), span này có chứa dòng lỗi mà vòng lặp đang săn không (0,30).
3. **Ghim bằng suy ra, không ghim tay** — tính từ kế hoạch, vòng lặp đang chạy, danh sách gate đang chờ. Ghim tay thì tập pin phình đơn điệu và cuối cùng tự vượt ngân sách.
4. Lỗi của vòng lặp chỉ được ghim **khi vòng lặp chưa xong**; xong rồi thì nó phải trở lại loại được.
5. **Gộp các lần thử lại y hệt**: 6 lần `npm test` (exit 1) thành một dòng `retry 6×, last_err: E2BIG at test_refresh_rotation` — 18k token còn 24 token, dòng lỗi cuối giữ nguyên văn.

```typescript
const recency = Math.exp(-(now - s.turn) / 12);
const reachable = serves.some(t => plan.pendingIds.includes(t)) ? 1.0 : 0.1;
return 0.30 * recency + 0.40 * reachable + 0.30 * failure;
```

**Kiểm tra**

Chạy bộ bất biến cho **mọi** lần nén đã ghi, trong CI đêm: không span ghim nào bị loại; tổng token còn lại không vượt ngân sách; danh sách span bị loại khớp đúng danh sách audit. Nếu một run chỉ hỏng ngay sau lúc nén, đó là tập pin đang thiếu thứ gì đó.

---

## Q3. Nén xong agent quên mất các quyết định đã giao trước đó, nhưng run vẫn báo "xong" — chặn được không? [→ §6 Contract Compaction↔Memory]

**Bạn sẽ thấy**

Ở lượt 12 người dùng nói: "dùng kho phiên dùng chung, nhưng token JWT v1 vẫn phải chạy". Ở lượt 40 agent chốt một quyết định khác. Sau lần nén, agent không biết mình đã quyết định gì và tự suy ra lại — kết quả là một codebase lệch nhẹ so với thiết kế đã được duyệt bốn mươi phút trước. Run báo thành công, không một dòng cảnh báo nào.

**Vì sao**

Vì nén xoá thứ khỏi ngữ cảnh, và nội dung bên trong nó chưa từng được lưu ở đâu cả. Đây là ranh giới giữa *ngữ cảnh tạm* và *bộ nhớ bền* — hỏng nhiều hơn mọi hợp đồng khác trong hệ production. Quyết định ở lượt 12 sẽ còn cần cho một lần chạy khác tuần sau, nên nó thuộc về bộ nhớ bền chứ không thuộc về ngữ cảnh. Ranh giới không phải "quan trọng với không quan trọng", mà là **"sau lần chạy này còn cần không?"**

**Làm gì**

1. **Ghi xuống trước, xoá sau** — đúng thứ tự 6 bước: chọn span để loại → trích nội dung bền (quyết định, việc còn mở, ràng buộc, sở thích người dùng) → **lưu vào bộ nhớ** → phát sự kiện audit → thay bằng resume block → chạy tiếp.
2. Lưu với `fsync` (đẩy dữ liệu xuống đĩa trước khi trả về), gắn cả mã khách và mã nhiệm vụ.
3. Bước 3 lỗi thì **huỷ bước 5**. Không phải ghi cảnh báo rồi đi tiếp — phải dừng thật. Một lần nén làm mất quyết định tệ hơn một lần run dừng lại với lỗi rõ ràng.
4. Phát sự kiện `compaction` ghi lại: đã giữ id nào, đã loại id nào, `ratio`, mã băm của resume block.
5. Phần còn dùng được nhưng quá lớn (kết quả lệnh chết) thì **tóm tắt thay vì bỏ hẳn**.
6. Nhánh đã bỏ vẫn giữ một dòng lý do: `nhánh t3 (vector cache) bị loại: thêm 400ms p99` — rẻ, và chặn agent quay lại vùng đó.

```typescript
const o = compact(spans, budget, goal, pins, plan, loop);
await memory.persist(o.writeBack.facts, { fsync: true });   // bền TRƯỚC khi loại
await traj.append({ kind: "compaction", payload: {
  keptIds: o.kept.map(s => s.id), evictedIds: o.dropped, ratio: o.ratio } });
return o;
```

**Kiểm tra**

Bài test đáng giá nhất của cả module: **tắt nơi lưu trí nhớ**, chạy một lần nén, và yêu cầu run phải từ chối đi tiếp. Kiểm tra thêm: danh sách span bị loại có bằng số quyết định đã ghi xuống bộ nhớ không.

---

## Q4. Resume block mình viết đọc lên thấy đủ cả, nhưng agent vẫn làm sai bước kế tiếp — kiểm sao? [→ §5 Resume block, §7 Prompt, §9.2 Kiểm thử]

**Bạn sẽ thấy**

Một resume block ghi: "chúng ta đang refactor authentication và gặp vài vấn đề cần xử lý". Đọc lên có vẻ đầy đủ, nhưng agent sau đó không biết phải làm gì, đọc lại từ đầu, và hoá đơn token gấp ba. Đây là cách phổ biến nhất khiến nén âm thầm phá một run.

**Vì sao**

Vì tiêu chuẩn nghiệm thu không phải "đọc lên có đủ không" mà là **"một agent mới với ngữ cảnh rỗng có làm đúng bước kế tiếp không"**. Nghiên cứu *lost in the middle* (Liu et al., 2023) cho thấy mô hình đọc đáng tin hơn ở đầu và cuối một ngữ cảnh dài, và hay **làm tệ hơn** với ngữ cảnh đã tóm tắt so với ngữ cảnh bị cắt — vì bản tóm tắt trôi chảy tạo ấn tượng sai về độ phủ.

**Làm gì**

1. **Khoá key cố định**, vì code (không chỉ mô hình) đọc lại nó: `Goal`, `Decisions`, `Open`, `Repro`, `Next`, `Invariants`, `Evicted`. Một parser lấy `Open[]` để dựng lại danh sách việc đang chờ, `Repro` để gieo lại vòng thử, `Evicted[]` để ghi bộ nhớ và phát sự kiện audit. Văn xuôi tự do phá cả ba.
2. **Trần cứng 300 token**, ép trong code. `Decisions` tối đa 5 cái, mỗi cái 25 từ; `Invariants` tối đa 5; vượt trần thì cắt bớt có chừng.
3. **Chép ràng buộc ra cả đầu và cuối prompt** (header/footer), nguyên văn. Đặt ở hai nơi nghĩa là dù bộ tóm tắt chỉ giữ 80% token thì ràng buộc vẫn còn.
4. **Pin giá trị thô, không diễn giải lại**: `timeoutMs: 30000`, không phải "khoảng 30 giây". Giữ nguyên văn dòng lỗi cuối trong `Repro`. Giữ nguyên văn diff — tóm tắt một bản vá gần như vô dụng vì giá trị nằm ở đúng những byte của nó.
5. Bố cục prompt: header là bất biến, giữa là ngữ cảnh tùy ý bị loại, cuối là nhắc lại bất biến.

```typescript
export function resumeIsSufficient(b: ResumeBlock): boolean {
  return b.goal.length > 0 && b.open.length > 0
      && b.repro.command.length > 0 && b.next.length > 0
      && countTokens(b) <= 300;
}
```

**Kiểm tra**

Chạy **agent lạnh**: chỉ truyền system prompt + resume block, rồi so hành động kế tiếp với một agent được đầy đủ ngữ cảnh gốc — phải bằng nhau. Chạy bộ hồi quy hằng đêm so điểm eval của run có nén với run không nén; điểm tụt ngay sau lúc nén là bằng chứng tập pin sai.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: README.md.*
