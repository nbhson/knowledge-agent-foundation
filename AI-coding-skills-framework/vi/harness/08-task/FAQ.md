# ❓ FAQ — Quản lý công việc cho agent (chuyện thật, dễ hiểu)

Nếu câu hỏi chưa rõ, đọc phần được nêu trong ngoặc vuông.

---

## README.md

### Q1. Tôi giao "refactor auth, thêm test, update docs, rồi deploy" — nó làm loạn cả lên, xử sao? [→ §1 Task Classification + §1.3 Decision Tree]

**Bạn sẽ thấy**

Agent nhận cả bốn việc một lúc và làm theo đúng thứ tự bạn gõ: nó refactor xong thì deploy, rồi mới thêm test và cập nhật tài liệu. Kết quả là code chưa từng được kiểm tra đã lên môi trường thật. Bạn phải sửa tay từ đầu.

**Vì sao**

Bốn việc đó khác nhau về bản chất và khác nhau về thứ tự bắt buộc, nhưng agent không có bước "chẩn đoán" nào cả. Nếu không tách ra, nó sẽ coi cả bốn là một việc duy nhất và tự suy luận thứ tự — mà suy luận thì không có bảo đảm gì.

**Làm gì**

1. Chấm đoạn yêu cầu theo **5 nhóm**: viết code mới, sửa code, phân tích code, viết tài liệu, viết test. Mỗi nhóm có chiến lược riêng, đừng dùng chung một cách.
2. Sau đó đo độ phức tạp theo quy mô: dưới 50 dòng là *tầm nhỏ*; 200-500 dòng / 3-5 file là *tầm vừa*; trên 15 file là *tầm lớn*.
3. Dùng cây quyết định có sẵn: yêu cầu còn mơ hồ → hỏi lại trước; nhỏ hơn 500 token → làm luôn một phát; lớn hơn thì mới tách nhỏ rồi chọn chạy tuần tự, song song hay theo TDD.
4. Với việc ghi vào hệ thống thật (deploy, gửi email, xoá dữ liệu), tách nó thành công việc riêng có điều kiện phụ thuộc: chỉ chạy khi *kiểm tra* đã xanh.
5. Đính kèm tiêu chí nghiệm thu cho mỗi việc nhỏ, nếu không bạn không biết nó làm đúng chưa.

```python
if any(k in task.description.lower() for k in ["fix", "bug", "refactor"]):
    task.category = TaskCategory.MODIFICATION
task.priority = 5        # 1 = cao nhất, 10 = thấp nhất
```

**Kiểm tra**

Chạy lại câu *"Refactor module auth, thêm test, update docs, rồi deploy"* và xác nhận nó ra ít nhất bốn việc riêng, mỗi việc có nhóm và độ phức tạp riêng. Sau đó thử một việc nhỏ dưới 500 token: nó phải được chạy thẳng, không bị tách thêm. Cuối cùng, xác nhận không có công việc ghi vào hệ thống thật nào chạy trước khi bước kiểm tra hoàn tất.

---

### Q2. Task to quá, agent làm đến giữa thì quên mất yêu cầu ban đầu — chia nhỏ thế nào? [→ §2 Task Decomposition + §8.1 Anti-Patterns]

**Bạn sẽ thấy**

Một công việc ước lượng hơn 20.000 token. Agent làm được một nửa rồi bắt đầu sửa nhầm ở chỗ không liên quan, và báo cáo xong nhưng bạn phải đọc lại toàn bộ để xác minh.

**Vì sao**

Độ phức tạp quá mức là lỗi số một trong danh sách anti-pattern. Vấn đề không chỉ là nhiều việc — mà là ngữ cảnh làm việc phình to, đẩy phần quan trọng nhất (ý định ban đầu) ra khỏi vùng nhớ tập trung. Tài liệu gọi đây là "trôi ngữ cảnh".

**Làm gì**

1. Cắt sao cho mỗi việc nhỏ **dưới 5.000 token**. Trần thực tế dễ sống với nhất là 100-5.000 token.
2. Cũng đừng cắt quá nhỏ. Việc dưới 500 token là chi phí quản lý nặng hơn phần lợi — có bộ phát hiện riêng bắt loại lỗi này.
3. Chọn đúng kiểu cắt theo bản chất việc:
   - Tuần tự khi bước sau bắt buộc cần bước trước.
   - Song song rồi gộp khi các phần độc lập nhau.
   - Theo lớp (cơ sở dữ liệu → giao diện → nghiệp vụ) khi việc trải nhiều tầng.
4. Dùng lát dọc cho tính năng: mỗi lát là một phần chạy được thật, không phải một tầng chưa xong.
5. Khi chưa chắc, chọn kiểu dò thử trước (spike): khoanh một khoảng 1-2 giờ để nghiên cứu rồi mới quyết định làm theo hướng nào.
6. Đặt thời hạn cho mỗi việc nhỏ và định kỳ làm mới ngữ cảnh, thay vì để một việc chạy vô tận.

**Kiểm tra**

Đo lại tổng số token ước lượng sau khi tách: tổng không nên giảm quá 10% (cắt quá nhỏ thì phình chi phí quản lý). Mỗi việc nhỏ phải nằm trong khoảng 500-5.000 token. Rồi chạy có bộ đếm thời gian: không việc nhỏ nào vượt thời hạn đã đặt.

---

### Q3. Hai việc chờ lẫn nhau, agent đứng hình không chạy — chặn sao? [→ §5.1 Task Dependency Graph]

**Bạn sẽ thấy**

Agent báo "đang chờ" mãi không tiến. Nguyên nhân là hai việc đã được gán phụ thuộc chéo nhau: việc A cần kết quả B, B cần kết quả A. Cả hai đều hợp lý khi nhìn riêng, và cùng hợp lý khi đặt cạnh nhau.

**Vì sao**

Phụ thuộc chéo tạo ra một vòng tròn trong đồ thị. Bộ xếp thứ tự hiểu rồi nhưng không có bước nào sẵn sàng chạy, nên nó chờ mãi. Tài liệu gọi đây là kẹt chết và xếp nó là lỗi số tư.

**Làm gì**

1. Ghi phụ thuộc theo một quy ước duy nhất: "A → B" nghĩa là A phải xong trước B. Không dùng hai chiều cho cùng một quan hệ.
2. Chạy kiểm tra vòng tròn **trước** khi bắt đầu, không phải sau khi đã kẹt. Dùng duyệt đệ quy có đánh dấu đang xét.
3. Khi sắp xếp thứ tự chạy, nếu thuật toán trả về ít hơn số việc thì đó là bằng chứng chắc chắn có vòng tròn — báo tên đúng các việc trong vòng đó.
4. Tận dụng cùng dữ liệu đó để tách nhóm chạy song song: tất cả việc không còn phụ thuộc gì thì gom vào một nhóm.
5. Sửa gốc chứ không cắt tuỳ tiện: nếu phải cắt một cạnh, hãy hỏi việc nào thật sự cần việc nào.
6. Ghi rõ cái phụ thuộc đó trong mô tả việc, để sau này người khác hiểu vì sao thứ tự là vậy.

```python
if len(order) != len(self.tasks):
    raise ValueError("Cycle detected in task dependencies")
```

**Kiểm tra**

Dựng cố ý một vòng tròn A→B→C→A và xác nhận kiểm tra phát hiện ra trước khi có việc nào chạy, kèm tên cả ba. Sau đó bỏ một cạnh và xác nhận thứ tự chạy ra đúng, đồng thời danh sách nhóm song song tách đúng các việc độc lập.

---

### Q4. Không biết trước cần bao nhiêu token, đến giữa chừng thì hết chỗ — làm sao? [→ §7 Estimation + §10 Token Budget Management]

**Bạn sẽ thấy**

Cứ mỗi phiên là một cục di chuyển: agent làm được một đôi việc rồi tự dừng giữa chừng, câu trả lời bị cắt cụt. Bạn phải làm lại phiên mới mỗi lần và vẫn không biết trước nên chia việc thế nào.

**Vì sao**

Không có con số nào để chia. Nếu bạn đoán rồi chia mù, bạn sẽ hoặc chia quá nhỏ (lãng phí) hoặc gom quá nhiều (tràn). Cả hai đều tệ hơn việc có một bảng giá tham khảo.

**Làm gì**

1. Dùng bảng giá kinh nghiệm theo loại việc và độ phức tạp:

| Loại việc | Token ước lượng |
|---|---|
| Sửa bug (đơn giản / phức tạp) | 1.000-3.000 / 3.000-8.000 |
| Tính năng mới (nhỏ / lớn) | 3.000-6.000 / 6.000-15.000 |
| Viết test | 2.000-6.000 |
| Điều tra lỗi | 3.000-10.000 |
| Chuyển đổi hệ thống | 5.000-20.000 |

2. Áp dụng quy tắc ngón tay cái: một dòng code khoảng 5-10 token, một dòng chú thích khoảng 8-12, một định nghĩa hàm khoảng 20-50.
3. Tự động hoá bằng công thức: lấy con số gốc theo độ phức tạp, nhân với hệ số theo loại việc (viết tài liệu rẻ bằng 0,4 lần so với viết code mới), cộng thêm 500 token cho mỗi file bị đụng tới.
4. Chia ngân sách cửa sổ ngữ cảnh 128K thành 4 phần và giữ lại phần dự phòng: lời dẫn hệ thống khoảng 5.000, ngữ cảnh dự án khoảng 30.000, ngữ cảnh việc khoảng 20.000, bộ nhớ làm việc khoảng 50.000, dự phòng khoảng 23.000.
5. Trước khi bắt đầu mỗi việc nhỏ, hỏi còn bao nhiêu token; **dưới 20% thì dọn ngay** — tóm tắt ngữ cảnh cũ, bỏ file không còn liên quan, làm nốt việc đang dở rồi mở phiên mới.
6. Giữ một khoảng đệm tối thiểu bất biến. Con số "còn lại" phải trừ khoản đệm trước, không được hỏi tới đâu trừ tới đó.

```python
base = BASE_TOKENS[task.complexity]            # vd MODERATE = 5000
value = base * CATEGORY_MULTIPLIERS[task.category] + 500 * len(task.files_involved)
```

**Kiểm tra**

Chạy bộ phát hiện lỗi trước khi bắt đầu: nếu một việc có ước lượng 0 thì báo thiếu ước lượng; nếu vượt 20.000 token thì báo quá lớn và đề nghị tách dưới 5.000 mỗi việc. Sau đó đo thực tế trên 10 việc cùng loại và đối chiếu với ước lượng — lệch quá một nửa là bảng giá cần sửa.

---

### Q5. Sếp giao mơ hồ kiểu "cải thiện code đi" — có cách nào bắt agent hỏi lại không? [→ §8.1 Anti-Patterns + §8.2 Anti-Pattern Detector]

**Bạn sẽ thấy**

Agent nhận câu *"cải thiện code đi"* và bắt đầu sửa loạn. Mười phút sau nó báo xong, nhưng không ai biết "cải thiện" ở đây là gì — và không có cách nào đánh giá kết quả.

**Vì sao**

Đây là lỗi số hai trong danh sách anti-pattern: mô tả mơ hồ. Bộ phát hiện trong tài liệu liệt kê sẵn những từ khoá như `improve`, `optimize`, `clean`, `better`, `refactor`, `make it work`, `fix it` — gặp từ nào mà không có tiêu chí kiểm chứng thì coi là mơ hồ.

**Làm gì**

1. Chạy bộ phát hiện lỗi **trước khi** bắt đầu, lúc còn sớm để sửa. Đợi đến lúc agent sửa xong mới phát hiện là đã mất tiền.
2. Với mô tả mơ hồ, bắt buộc thêm tiêu chí nghiệm thu cụ thể trước khi cho chạy.
3. Nếu câu lệnh chứa từ nối kiểu "rồi", "sau đó", "và" — tách thành từng việc riêng, mỗi việc một tiêu chí nghiệm thu riêng.
4. Thiếu ước lượng token cũng là lỗi, dù mức độ thấp — không có con số thì không kiểm soát được chi phí.
5. Nhiều hơn 5 phụ thuộc là dấu hiệu việc đó quá tải hoặc nên tách ra.
6. Với việc sửa code mà chưa xác định được file nào bị đụng, dừng lại quét mã trước — đừng đoán.

```python
vague = ["improve", "optimize", "clean", "better",
         "refactor", "make it work", "fix it"]
if any(k in task.description.lower() for k in vague) and not task.verification_criteria:
    issues.append({"pattern": "AMBIGUOUS_TASK", "severity": "MEDIUM"})
```

**Kiểm tra**

Chạy bộ phát hiện với câu "cải thiện code đi" và xác nhận nó báo đúng lỗi mơ hồ. Chạy với một việc sửa code không khai file nào bị đụng và xác nhận nó báo lỗi phạm vi thiếu. Cuối cùng, xác nhận một việc có mô tả rõ và đủ tiêu chí nghiệm thu thì không bị báo lỗi nào.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: `README.md`.*
