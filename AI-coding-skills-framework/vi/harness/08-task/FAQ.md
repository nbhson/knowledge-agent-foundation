# ❓ FAQ — Quản lý công việc cho agent (chuyện thật, dễ hiểu)

Nếu câu hỏi chưa rõ, đọc phần được nêu trong ngoặc vuông. (Ví dụ `[→ §1 Task Classification]` nghĩa là: mở `README.md` tới mục 1 để đọc chi tiết.)
Mỗi câu trả lời gồm 4 phần: **Bạn sẽ thấy** (triệu chứng), **Vì sao** (gốc rễ), **Làm gì** (cách xử lý), **Kiểm tra** (cách biết đã xử lý đúng).

---

## README.md

> Nhóm câu hỏi về cách giao việc cho agent: phân loại, chia nhỏ, xếp thứ tự, ước lượng token, và xử lý yêu cầu mơ hồ.
> (Token = đơn vị đo văn bản mà model đọc/viết; khoảng 0,75 từ tiếng Anh, hoặc vài ký tự tiếng Việt.)

### Q1. Tôi giao "refactor auth, thêm test, update docs, rồi deploy" — nó làm loạn cả lên, xử sao? [→ §1 Task Classification + §1.3 Decision Tree]

**Bạn sẽ thấy**

Agent nhận cả bốn việc một lúc và làm theo đúng thứ tự bạn gõ: nó refactor xong thì deploy, rồi mới thêm test và cập nhật tài liệu. Kết quả là code chưa từng được kiểm tra đã lên môi trường thật. Bạn phải sửa tay từ đầu.

**Vì sao**

Bốn việc đó khác nhau về bản chất và khác nhau về thứ tự bắt buộc, nhưng agent không có bước "chẩn đoán" nào cả. Nếu không tách ra, nó sẽ coi cả bốn là một việc duy nhất và tự suy luận thứ tự — mà suy luận thì không có bảo đảm gì.

**Làm gì**

1. Chấm đoạn yêu cầu theo **5 nhóm**: viết code mới, sửa code, phân tích code, viết tài liệu, viết test. Mỗi nhóm có chiến lược riêng, đừng dùng chung một cách.
2. Sau đó đo độ phức tạp theo quy mô: dưới 50 dòng là *tầm nhỏ*; 200-500 dòng / 3-5 file là *tầm vừa*; trên 15 file là *tầm lớn*.
3. Dùng cây quyết định có sẵn: yêu cầu còn mơ hồ → hỏi lại trước; nhỏ hơn 500 token → làm luôn một phát; lớn hơn thì mới tách nhỏ rồi chọn chạy tuần tự (lần lượt từng việc), song song (cùng lúc), hay theo TDD (Test-Driven Development — viết test trước, viết code sau để thỏa test).
4. Với việc ghi vào hệ thống thật (deploy, gửi email, xoá dữ liệu), tách nó thành công việc riêng có điều kiện phụ thuộc: chỉ chạy khi *kiểm tra* đã xanh.
5. Đính kèm tiêu chí nghiệm thu cho mỗi việc nhỏ, nếu không bạn không biết nó làm đúng chưa.

> 📄 **Code ví dụ:** [`examples/01-q1-toi-giao-refactor-auth-them-test-update.py`](examples/01-q1-toi-giao-refactor-auth-them-test-update.py)

**Kiểm tra**

Chạy lại câu *"Refactor module auth, thêm test, update docs, rồi deploy"* và xác nhận nó ra ít nhất bốn việc riêng, mỗi việc có nhóm và độ phức tạp riêng. Sau đó thử một việc nhỏ dưới 500 token: nó phải được chạy thẳng, không bị tách thêm. Cuối cùng, xác nhận không có công việc ghi vào hệ thống thật nào chạy trước khi bước kiểm tra hoàn tất.

> **Tóm gọn 1 câu:** Giao việc lẫn lộn là agent tự đoán thứ tự — hãy phân loại theo 5 nhóm, đo độ phức tạp, tách việc ghi vào hệ thống thật ra riêng, và gắn tiêu chí nghiệm thu cho từng việc.

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
4. Dùng lát dọc cho tính năng (vertical slice — mỗi lát là một mảnh mỏng nhưng chạy được thật từ đầu tới cuối, ví dụ "đăng nhập với 1 tài khoản" thay vì "làm hết tầng database trước"), không phải một tầng chưa xong.
5. Khi chưa chắc, chọn kiểu dò thử trước (spike — khoanh một khoảng thời gian ngắn chỉ để nghiên cứu và trả lời câu hỏi, không để làm sản phẩm): khoanh 1-2 giờ nghiên cứu rồi mới quyết định làm theo hướng nào.
6. Đặt thời hạn cho mỗi việc nhỏ và định kỳ làm mới ngữ cảnh, thay vì để một việc chạy vô tận.

**Kiểm tra**

Đo lại tổng số token ước lượng sau khi tách: tổng không nên giảm quá 10% (cắt quá nhỏ thì phình chi phí quản lý). Mỗi việc nhỏ phải nằm trong khoảng 500-5.000 token. Rồi chạy có bộ đếm thời gian: không việc nhỏ nào vượt thời hạn đã đặt.

> **Tóm gọn 1 câu:** Việc to làm agent "trôi ngữ cảnh" — cắt mỗi mảnh 500-5.000 token, chọn kiểu cắt theo quan hệ giữa các bước, và cắt dọc theo tính năng thay vì cắt theo tầng kỹ thuật.

---

### Q3. Hai việc chờ lẫn nhau, agent đứng hình không chạy — chặn sao? [→ §5.1 Task Dependency Graph]

**Bạn sẽ thấy**

Agent báo "đang chờ" mãi không tiến. Nguyên nhân là hai việc đã được gán phụ thuộc chéo nhau: việc A cần kết quả B, B cần kết quả A. Cả hai đều hợp lý khi nhìn riêng, và cùng hợp lý khi đặt cạnh nhau.

**Vì sao**

Phụ thuộc chéo tạo ra một vòng tròn trong đồ thị. Bộ xếp thứ tự hiểu rồi nhưng không có bước nào sẵn sàng chạy, nên nó chờ mãi. Tài liệu gọi đây là kẹt chết và xếp nó là lỗi số tư.

**Làm gì**

1. Ghi phụ thuộc theo một quy ước duy nhất: "A → B" nghĩa là A phải xong trước B. Không dùng hai chiều cho cùng một quan hệ.
2. Chạy kiểm tra vòng tròn **trước** khi bắt đầu, không phải sau khi đã kẹt. Dùng duyệt đệ quy có đánh dấu đang xét (đi theo chuỗi "A cần B, B cần C..." từ từng việc, đánh dấu mỗi việc đang xét; nếu đường đi quay lại gặp một việc đang xét là có vòng tròn).
3. Khi sắp xếp thứ tự chạy, nếu thuật toán trả về ít hơn số việc thì đó là bằng chứng chắc chắn có vòng tròn — báo tên đúng các việc trong vòng đó.
4. Tận dụng cùng dữ liệu đó để tách nhóm chạy song song: tất cả việc không còn phụ thuộc gì thì gom vào một nhóm.
5. Sửa gốc chứ không cắt tuỳ tiện: nếu phải cắt một cạnh (một mối quan hệ "cần trước"), hãy hỏi việc nào thật sự cần việc nào.
6. Ghi rõ cái phụ thuộc đó trong mô tả việc, để sau này người khác hiểu vì sao thứ tự là vậy.

> 📄 **Code ví dụ:** [`examples/02-q3-hai-viec-cho-lan-nhau-agent-ung.py`](examples/02-q3-hai-viec-cho-lan-nhau-agent-ung.py)

**Kiểm tra**

Dựng cố ý một vòng tròn A→B→C→A và xác nhận kiểm tra phát hiện ra trước khi có việc nào chạy, kèm tên cả ba. Sau đó bỏ một cạnh và xác nhận thứ tự chạy ra đúng, đồng thời danh sách nhóm song song tách đúng các việc độc lập.

> **Tóm gọn 1 câu:** Phụ thuộc chéo tạo vòng tròn và kẹt chết cả hệ — ghi quan hệ một chiều duy nhất, kiểm tra vòng tròn trước khi chạy, và cắt cạnh sai chứ không cắt bừa.

---

### Q4. Không biết trước cần bao nhiêu token, đến giữa chừng thì hết chỗ — làm sao? [→ §7 Estimation + §10 Token Budget Management]

**Bạn sẽ thấy**

Cứ mỗi phiên là một cục di chuyển: agent làm được một đôi việc rồi tự dừng giữa chừng, câu trả lời bị cắt cụt. Bạn phải làm lại phiên mới mỗi lần và vẫn không biết trước nên chia việc thế nào.

**Vì sao**

Không có con số nào để chia. Nếu bạn đoán rồi chia mù, bạn sẽ hoặc chia quá nhỏ (lãng phí) hoặc gom quá nhiều (tràn). Cả hai đều tệ hơn việc có một bảng giá tham khảo.

**Làm gì**

1. Dùng bảng giá kinh nghiệm theo loại việc và độ phức tạp.

Cách đọc bảng này: cột **Loại việc** là dạng công việc bạn định giao (số trong ngoặc là mức độ dễ/khó); cột **Token ước lượng** là kinh nghiệm lượng token thường tiêu tốn — lấy làm cơ sở chia nhỏ việc. Ví dụ: sửa bug đơn giản tốn khoảng 1.000-3.000 token, còn chuyển đổi cả hệ thống có thể tốn tới 20.000.

| Loại việc | Token ước lượng |
|---|---|
| Sửa bug (đơn giản / phức tạp) | 1.000-3.000 / 3.000-8.000 |
| Tính năng mới (nhỏ / lớn) | 3.000-6.000 / 6.000-15.000 |
| Viết test | 2.000-6.000 |
| Điều tra lỗi | 3.000-10.000 |
| Chuyển đổi hệ thống | 5.000-20.000 |

2. Áp dụng quy tắc ngón tay cái (rule of thumb — con số ước chừng để tính nhanh, không phải chuẩn tuyệt đối): một dòng code khoảng 5-10 token, một dòng chú thích khoảng 8-12, một định nghĩa hàm khoảng 20-50.
3. Tự động hoá bằng công thức: lấy con số gốc theo độ phức tạp, nhân với hệ số theo loại việc (viết tài liệu rẻ bằng 0,4 lần so với viết code mới), cộng thêm 500 token cho mỗi file bị đụng tới.
4. Chia ngân sách cửa sổ ngữ cảnh 128K (context window — giới hạn "bộ nhớ hội thoại" của model, 128K = khoảng 128.000 token) thành 4 phần và giữ lại phần dự phòng: lời dẫn hệ thống khoảng 5.000, ngữ cảnh dự án khoảng 30.000, ngữ cảnh việc khoảng 20.000, bộ nhớ làm việc khoảng 50.000, dự phòng khoảng 23.000.
5. Trước khi bắt đầu mỗi việc nhỏ, hỏi còn bao nhiêu token; **dưới 20% thì dọn ngay** — tóm tắt ngữ cảnh cũ, bỏ file không còn liên quan, làm nốt việc đang dở rồi mở phiên mới.
6. Giữ một khoảng đệm tối thiểu bất biến. Con số "còn lại" phải trừ khoản đệm trước, không được hỏi tới đâu trừ tới đó.

> 📄 **Code ví dụ:** [`examples/03-q4-khong-biet-truoc-can-bao-nhieu-token.py`](examples/03-q4-khong-biet-truoc-can-bao-nhieu-token.py)

**Kiểm tra**

Chạy bộ phát hiện lỗi trước khi bắt đầu: nếu một việc có ước lượng 0 thì báo thiếu ước lượng; nếu vượt 20.000 token thì báo quá lớn và đề nghị tách dưới 5.000 mỗi việc. Sau đó đo thực tế trên 10 việc cùng loại và đối chiếu với ước lượng — lệch quá một nửa là bảng giá cần sửa.

> **Tóm gọn 1 câu:** Đừng chia việc theo cảm tính — tra bảng giá token theo loại việc, chia cửa sổ ngữ cảnh thành các khoản có dự phòng, và khi còn dưới 20% ngân sách thì dọn ngữ cảnh ngay.

---

### Q5. Sếp giao mơ hồ kiểu "cải thiện code đi" — có cách nào bắt agent hỏi lại không? [→ §8.1 Anti-Patterns + §8.2 Anti-Pattern Detector]

> Thuật ngữ: **anti-pattern** = lỗi làm đi làm lại mà ai cũng mắc, đã có tên để dễ gọi ra; **bộ phát hiện lỗi** = bước tự động quét mô tả việc trước khi cho agent chạy; **tiêu chí nghiệm thu** = điều kiện "đạt" phải kiểm chứng được (ví dụ: "test đăng nhập chạy xanh").

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

> 📄 **Code ví dụ:** [`examples/04-q5-sep-giao-mo-ho-kieu-cai-thien.py`](examples/04-q5-sep-giao-mo-ho-kieu-cai-thien.py)

**Kiểm tra**

Chạy bộ phát hiện với câu "cải thiện code đi" và xác nhận nó báo đúng lỗi mơ hồ. Chạy với một việc sửa code không khai file nào bị đụng và xác nhận nó báo lỗi phạm vi thiếu. Cuối cùng, xác nhận một việc có mô tả rõ và đủ tiêu chí nghiệm thu thì không bị báo lỗi nào.

> **Tóm gọn 1 câu:** Yêu cầu mơ hồ + không tiêu chí nghiệm thu = agent sửa bừa mà không ai chấm được — chạy bộ phát hiện lỗi trước khi chạy, bắt buộc có tiêu chí cụ thể, và tách các việc nối nhau bằng "rồi"/"và".

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: `README.md`.*
