# 🎯 04. Calibration — Xác Suất Thành Thật

> Phần này giải thích **xác suất được calibrate nghĩa là gì**, tại sao **confidence ≠ xác suất đúng**, cách **đọc distribution thay vì chỉ xem đáp án**, cũng như **thresholding & bands** để biến xác suất thành hành động production. Đọc [README.md](../README.md) trước để có bối cảnh tổng quan về Module XIV — Jev & System One Models.

> **Cách đọc phần này:** *calibrate* = hiệu chỉnh, tức con số nói ra khớp với thực tế; *distribution* = phân phối xác suất trên tất cả lựa chọn; *threshold* = ngưỡng, con số ranh giới để quyết định tự làm hay chuyển người; *band* = dải (cao/vừa/thấp) gom quanh một ngưỡng.

---

## 1. Xác Suất Được Calibrate Nghĩa Là Gì?

Phần này trả lời câu hỏi nền tảng: con số xác suất của Jev có "nói thật" không — và vì sao điều đó quyết định mọi logic phía sau.

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Calibration (hiệu chỉnh xác suất) nghĩa là **con số xác suất đưa ra khớp với tần suất đúng ngoài thực tế**. Nếu Jev nói "câu này đúng với xác suất 0.8" trên hàng nghìn câu hỏi, thì khoảng ~80% trong số đó thực sự đúng. Đây chính là *"epistemically honest probabilities"* — xác suất nói thật với những gì mô hình thực sự biết.
> **Ẩn dụ/so sánh:** Giống **một người thợ đo may có thước đo đúng chuẩn** — khi anh ta nói "cái này dài 10cm", kiểm lại thì đúng 10cm. Người đo tệ (overconfidence) thì nói "10cm" nhưng thực tế dao động 6–14cm: nghe tự tin nhưng không đáng tin.
> **Vì sao quan trọng:** Mọi downstream logic — auto-act khi tự tin, escalate khi mơ hồ — đều đứng trên giả định "số 0.8 nghĩa là 0.8". Nếu xác suất không calibrate, toàn bộ pipeline thresholding trở thành ảo giác.

Giải nghĩa: **downstream logic** = các bước xử lý phía sau trong pipeline (chuỗi xử lý nối tiếp); **auto-act** = code tự hành động không hỏi người; **escalate** = chuyển người hoặc hệ thống khác; **overconfidence** = tự tin quá mức — nói "10cm" nhưng đo ra 6–14cm.

> **Tóm gọn 1 câu:** Calibrate nghĩa là nói 0.8 thì thật sự đúng ~80% — mọi ngưỡng tự động đều đổ sập nếu con số này không thật.

### 1.1 LLM Overconfidence vs Jev Calibration

Phần này so sánh trực diện: mô hình ngôn ngữ lớn (LLM) thường tự tin quá mức, còn Jev được tối ưu để con số khớp thực tế.

LLM thường **overconfidence**: sinh ra văn bản với giọng điệu chắc nịch ngay cả khi sai, và "token probability" không trực tiếp tương ứng với độ đúng của câu trả lời tổng thể. Jev được tối ưu để xác suất của nó **khớp với outcome thực tế**:

```
┌─────────────────────────────────────────────────────────────────┐
│                    CALIBRATION SO SÁNH                          │
│                                                                  │
│  LLM:   "Chắc chắn 99%!"  ──►  thực tế đúng ~60-70% (hay thấp) │
│         overconfidence, giọng điệu ≠ xác suất                   │
│                                                                  │
│  Jev:   P = 0.8           ──►  thực tế đúng ~80%                │
│         xác suất được tối ưu chống lại outcome                   │
└─────────────────────────────────────────────────────────────────┘
```

Điểm then chốt: **~80% câu trả lời được chấm điểm 0.8 là đúng** — đây là số đo calibration, không phải slogan.

Cách đọc sơ đồ trên: hai hàng so cách huấn luyện khác nhau — LLM được khen vì giọng tự tin (nên tự tin quá), Jev được chấm theo kết quả thật (nên số khớp thực tế).

> **Tóm gọn 1 câu:** LLM nói "chắc chắn 99%" nhưng đo ra ~60–70% đúng; Jev nói 0.8 thì đo ra ~80% đúng — đó là calibration.

### 1.2 Bảng So Sánh RLHF vs RLVR vs RLCD

Phần này giải thích vì sao xác suất của Jev khác mô hình lớn: do phương pháp huấn luyện khác nhau. Cách đọc bảng: cột **Thuật toán** là tên phương pháp huấn luyện; cột **Tối ưu cái gì?** nói phương pháp đó chấm điểm model theo tiêu chí nào; cột **Nhược điểm với quyết định** là hệ quả xấu khi dùng cho quyết định. Ví dụ, hàng **RLHF** nghĩa là: model được khen khi con người thích câu trả lời — nên xác suất phản ánh thị hiếu, không phản ánh đúng/sai.

Jev được train bằng **RLCD (Reinforcement Learning for Calibrated Decisions)** — thứ làm nên sự khác biệt trong cách xác suất hình thành:

| Thuật toán | Tối ưu cái gì? | Nhược điểm với quyết định |
|------------|----------------|---------------------------|
| **RLHF** | Preferences của con người ("cái này hay hơn") | Xác suất phản ánh sở thích, không phản ánh outcome; hay overconfident |
| **RLVR** | Verification đúng/sai (rule-based rewards) | Tốt hơn cho correctness, nhưng vẫn thiếu tín hiệu "biên độ" xác suất |
| **RLCD** | **Probabilities tối ưu chống lại outcomes** | Không cần human preferences; xác suất = dự đoán điều gì sẽ xảy ra → calibrate |

Jev **không phải LLM** — không sinh text, không token generation. Nó là transformer-based, train trên synthetic data qua RLCD: **kết quả cuối cùng của một quyết định** (outcome) là phần thưởng, chứ không phải "người thích câu trả lời nào". Nhờ vậy xác suất đầu ra là **thông kê về thế giới**, không phải về văn phong.

Giải nghĩa: **synthetic data** = dữ liệu do máy tự sinh ra để huấn luyện, không phải dữ liệu người thật; **token generation** = sinh văn bản từng mảnh chữ như LLM; **outcome** = kết quả thật của quyết định (đúng/sai, có xảy ra không).

> **Tóm gọn 1 câu:** RLCD huấn luyện Jev theo kết quả thật nên xác suất của nó là dự đoán về thế giới — trong khi RLHF huấn luyện theo thị hiếu người đọc nên xác suất chỉ phản ánh văn phong.

---

## 2. confidence ≠ Xác Suất Đúng

Phần này phân biệt hai khái niệm hay bị gộp làm một: độ tự tin (phân phối có nhọn không) và xác suất đúng (đáp án có đúng không). Nhầm hai cái này là nguồn gốc của những bug nguy hiểm nhất.

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** `confidence` (Choice/Score) là **độ tập trung của phân phối xác suất** — phân phối càng "peaked" (nhọn) thì confidence càng tiến gần 1.0. Nó là **margin** (biên độ), **không phải** xác suất câu trả lời đúng. Với Noul, `confidence = |p − 0.5| × 2`.
> **Ẩn dụ/so sánh:** Giống **độ rõ của tiếng radio**: confidence cao = tín hiệu rõ ràng đến mức hầu như không có nhiễu. Nhưng tín hiệu rõ ràng **không đảm bảo trạm đang phát đúng bài bạn muốn** — có thể tín hiệu rõ nhưng sai đài. "Confidence là độ rõ ràng, không phải độ đúng."
> **Vì sao quan trọng:** Nhầm confidence = probability of correctness dẫn đến hai sai lầm chết người: (1) auto-act trên confidence 0.95 của một câu trả lời **sai trong schema**; (2) escalate vô ích vì nghĩ "confidence thấp = chắc sai" trong khi đó chỉ là phân phối flat vì input mơ hồ.

Giải nghĩa: **margin (biên độ)** = độ chênh giữa hai lựa chọn đứng đầu; **schema** = danh sách lựa chọn/khung kết quả bạn định nghĩa trước; **flat** = phẳng — xác suất dàn đều, không nhọn về đâu.

> **Tóm gọn 1 câu:** Confidence đo "mô hình có rõ ràng không", không đo "mô hình có đúng không" — rõ ràng vẫn có thể sai.

### 2.1 Choice & Score — Confidence Là Độ Tập Trung Phân Phối

Phần này vẽ hai tình huống đối lập: phân phối nhọn (tự tin cao) và phân phối phẳng (mơ hồ) — và cảnh báo cả hai đều có thể sai.

```
Phân phối PEAKED (confidence cao ≈ 1.0):     Phân phối FLAT (confidence thấp):

  option A ████████████████████ 0.92           option A ████ 0.28
  option B ██ 0.05                             option B ███ 0.26
  option C █ 0.03                              option C ███ 0.24
                                               option D ██ 0.22
  → độ tập trung cao → confidence ≈ 0.9       → dàn trải → confidence thấp
  → NHƯNG option A vẫn có thể SAI!             → mơ hồ thật sự (ambiguity)
```

Cách đọc khối trên: cột trái — 0.92 dồn về option A, còn lại rất nhỏ → phân phối nhọn, confidence cao; cột phải — bốn option xấp xỉ nhau (0.28/0.26/0.24/0.22) → phân phối phẳng, confidence thấp, mơ hồ thật. Ghi nhớ dòng "NHƯNG option A vẫn có thể SAI": nhọn không có nghĩa là đúng.

**Điều quan trọng nhất**: Jev có thể chọn một đáp án **sai nhưng nằm trong schema** với confidence cao. Type safety chỉ đóng hình dạng output — không đảm bảo nội dung đúng. Confidence đo *"mô hình có rõ ràng không"*, không đo *"mô hình có đúng không"*. (**Type safety** = đảm bảo kết quả luôn nằm trong các kiểu/lựa chọn bạn khai báo — không bao giờ bịa lựa chọn lạ.)

> **Tóm gọn 1 câu:** Phân phối nhọn cho confidence cao nhưng đáp án vẫn có thể sai; phân phối phẳng là tín hiệu mơ hồ thật cần escalate.

### 2.2 Noul — Confidence Là Margin Từ 0.5

Phần này giải thích cách tính độ tự tin cho câu hỏi có/không: khoảng cách từ p tới 0.5.

Với Noul (yes/no), `P(yes)` nằm trong [0, 1] và confidence được tính bằng **khoảng cách tới 0.5**:

```
confidence = |p − 0.5| × 2

  p = 0.01  →  |0.01 − 0.5| × 2 = 0.98   → confidence rất cao (gần như chắc NO)
  p = 0.45  →  |0.45 − 0.5| × 2 = 0.10   → confidence rất thấp (gần cân bằng)
  p = 0.99  →  |0.99 − 0.5| × 2 = 0.98   → confidence rất cao (gần như chắc YES)
  p = 0.50  →  |0.50 − 0.5| × 2 = 0.00   → cân bằng hoàn toàn
```

Cách đọc khối trên: mỗi dòng tính công thức cho một giá trị p cụ thể. p = 0.01 → gần như chắc NO; p = 0.99 → gần như chắc YES; p = 0.45 và p = 0.50 → gần 0.5, tức **không biết** — không phải "trung bình".

**P gần 0.5 = balanced, KHÔNG PHẢI "medium/trung bình"** — nghĩa là mô hình phân vân thật sự giữa yes và no, không phải "trung bình có". Noul **không có confidence riêng** — confidence suy ra trực tiếp từ margin này.

> **Tóm gọn 1 câu:** Với câu có/không, độ tự tin = `|p − 0.5| × 2`; p gần 0.5 nghĩa là phân vân thật sự, không phải "trung bình".

### 2.3 Tóm Tắt Ba Khái Niệm Dễ Nhầm

Cách đọc bảng này: cột **Khái niệm** là tên thuật ngữ; cột **Đo cái gì?** nói nó đo điều gì; cột **Không đo cái gì?** cảnh báo điều nó KHÔNG đo. Ví dụ, hàng `confidence (Choice/Score)` nghĩa là: với câu chọn/chấm điểm, confidence đo độ nhọn của phân phối — và tuyệt đối không phải xác suất đúng.

| Khái niệm | Đo cái gì? | Không đo cái gì? |
|-----------|-----------|-------------------|
| **probability (P)** | Xác suất outcome xảy ra (Choice/Score: phân phối trên options; Noul: P(yes)) | — |
| **confidence (Choice/Score)** | Độ tập trung/phân phối (peaked → 1.0) | Không phải P(đúng) |
| **confidence (Noul)** | Margin từ 0.5: \|p−0.5\|×2 | Không phải P(đúng) riêng biệt |

> **A closed answer space stops out-of-schema inventions; it does not guarantee the selected category is correct.**

(Câu trên nghĩa là: danh sách lựa chọn đóng chỉ chặn việc bịa đáp án ngoài danh sách — nó **không** đảm bảo đáp án được chọn là đúng.)

> **Tóm gọn 1 câu:** Ba khái niệm cần tách: p là xác suất, confidence là độ nhọn, certainty là biên độ — không cái nào trong số đó là "xác suất đúng".

---

## 3. Đọc Distribution Thay Vì Chỉ Xem Đáp Án

Phần này nói về cách đọc kết quả "nâng cấp": đừng chỉ nhìn đáp án thắng, hãy đọc cả phân phối — vì đó là nơi giấu tín hiệu mơ hồ.

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** API Jev trả về **cả phân phối đầy đủ** trên mọi option (Choice) hay mọi level (Score), không chỉ option thắng. Đọc phân phối cho phép bạn nhận ra **ambiguity** (mơ hồ), near-ties (gần hòa), và margin — thay vì xử lý kết quả như một label cứng.
> **Ẩn dụ/so sánh:** Giống **bảng tỷ lệ bầu cử thay vì chỉ tên người thắng** — 51% vs 49% khác hoàn toàn 90% vs 10% dù cùng một người thắng. Chỉ nhìn "ai thắng" là bỏ đi toàn bộ câu chuyện.
> **Vì sao quan trọng:** Flat distribution là tín hiệu escalate tự nhiên nhất: khi hai option gần bằng nhau, hệ thống nên đưa người vào thay vì auto-act. Nếu chỉ đọc `selected`, bạn vứt bỏ chính signal này.

Giải nghĩa: **near-tie (gần hòa)** = hai lựa chọn chênh nhau rất ít (ví dụ 0.31 vs 0.29); **ambiguity** = mơ hồ — dữ liệu đầu vào không đủ để phân biệt; **`selected`** = trường chứa lựa chọn thắng trong response.

> **Tóm gọn 1 câu:** API trả về cả phân phối đầy đủ — 51%/49% khác hẳn 90%/10% dù cùng một người thắng, và tình huống gần hòa chính là lúc cần escalate.

### 3.1 Hai Loại Kết Quả Cần Phân Biệt

Phần này vẽ hai tình huống cùng một lựa chọn thắng nhưng cách đọc khác nhau: một bên hành động được, một bên phải hỏi người.

```
┌── PEAKED (đọc để AUTO-ACT) ──────────┐  ┌── FLAT (đọc để ESCALATE) ──────────┐
│                                       │  │                                     │
│  billing_issue  ████████████████ 0.86 │  │  billing_issue  ████████ 0.31       │
│  refund_request ███ 0.08              │  │  refund_request ███████ 0.29        │
│  general        ██ 0.06               │  │  general        ██████ 0.24         │
│                                       │  │  account_access ████ 0.16           │
│  selected = billing_issue             │  │                                     │
│  confidence ≈ cao                     │  │  selected = billing_issue (nhưng...) │
│  → Hành động được                     │  │  confidence ≈ thấp                   │
│                                       │  │  → Hỏi người / thêm context         │
└───────────────────────────────────────┘  └─────────────────────────────────────┘
```

Cách đọc khối trên: cột trái — 0.86 dồn về `billing_issue`, margin dày → auto-act được; cột phải — 0.31 vs 0.29, gần hòa → cùng một "selected" nhưng phải hỏi người/thêm context trước khi hành động.

> **Tóm gọn 1 câu:** Cùng một nhãn thắng nhưng phân phối nhọn thì tự làm, phân phối phẳng thì phải escalate — nên luôn đọc cả hai.

### 3.2 Những Gì Phân Phối Cho Biết Mà Label Không Cho

Phần này liệt kê bốn tín hiệu chỉ phân phối mới cung cấp, không thể thấy được từ nhãn thắng. Giải nghĩa: **multimodal** = phân phối có hai đỉnh nhọn tách xa nhau — dấu hiệu dữ liệu chứa hai chủ đề trộn lẫn.

- **Margin**: chênh lệch giữa option thắng và option nhì — margin mỏng = rủi ro.
- **Ambiguity**: phân phối flat = input không đủ để phân biệt — cần thêm state.
- **Ambiguity tập trung ở đâu**: nếu 0.4/0.4 giữa 2 option, câu hỏi có thể poorly designed (2 option overlap).
- **Multimodal**: phân phối nhọn ở 2 đỉnh xa nhau = có thể input chứa 2 chủ đề trộn lẫn.

**Code mẫu** đọc cả distribution:

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/01-3-2-nhung-gi-phan-phoi-cho-biet.py`](examples/01-3-2-nhung-gi-phan-phoi-cho-biet.py)

</details>

> **Tóm gọn 1 câu:** Phân phối cho bạn margin, độ mơ hồ, chỗ thiết kế câu hỏi kém, và dữ liệu trộn lẫn — bốn tín hiệu mà nhãn thắng không bao giờ cho.

---

## 4. Thresholding & Bands

Phần này là "luật giao thông" của luồng quyết định: quy ước rõ xác suất cỡ nào thì tự làm, cỡ nào thì hỏi, cỡ nào thì chuyển người.

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Thresholding là **chuyển xác suất/confidence thành hành động** bằng cách so với các ngưỡng (bands): cao → code auto-acts, trung bình → confirm/thêm context, thấp → route sang người hoặc hệ thống khác (LLM). Đây là "pháp luật" của luồng quyết định.
> **Ẩn dụ/so sánh:** Giống **đèn giao thông** cho dữ liệu: xanh = đi (auto-act), vàng = dừng lại kiểm tra (confirm), đỏ = nhường quyền cho người (escalate). Không đèn thì xe chạy hỗn loạn; đèn sai thì tai nạn.
> **Vì sao quan trọng:** Không threshold = mọi kết quả Jev treated như nhau — hoặc auto-act liều lĩnh trên mọi câu, hoặc escalate mọi câu và mất hết lợi thế tốc độ. Band phải được **chọn từ labelled data của bạn**, không phải chốt cứng từ đầu.

Giải nghĩa: **labelled data** = dữ liệu đã có người gán đáp án đúng để đối chiếu; **band** = dải giá trị (cao/vừa/thấp) quy định hành động.

> **Tóm gọn 1 câu:** Thresholding là bộ đèn giao thông: xanh = tự làm, vàng = hỏi lại, đỏ = chuyển người — và đèn phải được hiệu chỉnh từ dữ liệu thật của bạn.

### 4.1 Ba Band Hướng Dẫn

Phần này định nghĩa ba dải chuẩn kèm ngưỡng gợi ý. Cách đọc khung dưới: HIGH/MEDIUM/LOW là ba dải confidence; số trong ngoặc là khoảng ngưỡng gợi ý; mỗi dải có một hành động kèm ví dụ.

```
┌────────────────────────────────────────────────────────────────────────┐
│                    CONFIDENCE BANDS                                    │
│                                                                        │
│   HIGH            │ MEDIUM          │ LOW                              │
│   (≥ ~0.8)        │ (~0.5–0.8)      │ (< ~0.5)                         │
│                    │                  │                                  │
│   Code AUTO-ACTS  │ Confirm với      │ Route to HUMAN                   │
│   trên kết quả    │ user / lấy thêm  │ hoặc another system / LLM        │
│                    │ context          │                                  │
│   VD: route ticket │ VD: hiện option  │ VD: escalate ticket mơ hồ,       │
│   vào queue ngay   │ cho user xác nhận│ hỏi lại LLM với prompt đầy đủ    │
└────────────────────────────────────────────────────────────────────────┘
```

Bảng dưới đây nói lại nội dung trên theo từng hàng — cách đọc: cột **Band** là tên dải; cột **Ngưỡng gợi ý** là khoảng confidence; cột **Hành động** là việc code nên làm; cột **Ví dụ** là tình huống minh hoạ. Ví dụ, hàng **Medium** nghĩa là: confidence từ 0.5 tới 0.8 thì hiện kết quả cho người dùng duyệt hoặc bổ sung thêm state, chưa tự hành động.

| Band | Ngưỡng gợi ý | Hành động | Ví dụ |
|------|--------------|-----------|-------|
| **High** | ≥ ~0.8 | Auto-act | Route ticket, apply label, cho tool call chạy |
| **Medium** | ~0.5–0.8 | Confirm / thêm context | Hiện kết quả cho user duyệt, bổ sung state |
| **Low** | < ~0.5 | Escalate | Human review, fallback sang LLM, retry với state khác |

> Ngưỡng cụ thể **phải tune từ labelled data của bạn** — 0.8 chỉ là starting point mang tính guidance.

> **Tóm gọn 1 câu:** Ba band chuẩn: ≥ ~0.8 tự làm, ~0.5–0.8 hỏi xác nhận, < ~0.5 chuyển người — ngưỡng thật phải tune từ dữ liệu có nhãn của bạn.

### 4.2 Cách Chọn Threshold Từ Labelled Data

Phần này là quy trình 5 bước để chọn ngưỡng bằng số liệu thay vì cảm tính.

```
1. Thu thập labelled examples (input → correct answer) từ domain của bạn
2. Chạy Jev trên từng example → ghi (probabilities, outcome)
3. Vẽ calibration curve: bucket theo P, đo % đúng thực tế
4. Chọn threshold theo tolerance rủi ro:
     - Auto-act được phép sai bao nhiêu? → đặt high-band sao cho precision đủ
     - Escalate tốn bao nhiêu human time? → đặt low-band cân bằng load
5. Áp dụng per-question threshold nếu các câu hỏi có risk khác nhau
```

Giải nghĩa: **calibration curve** = đường hiệu chỉnh — chia dữ liệu theo khoảng xác suất rồi đo tỉ lệ đúng thật của từng khoảng; **precision** = tỉ lệ đúng trong nhóm được tự xử lý; **tolerance rủi ro** = mức sai bạn chấp nhận được.

**Per-question threshold**: một câu routing vô hại có thể auto-act ở 0.7, trong khi câu gating hành động phá hoại cần 0.95+. Không phải mọi question dùng chung một band.

> **Tóm gọn 1 câu:** Quy trình 5 bước: thu thập → chạy Jev → vẽ đường hiệu chỉnh → chọn ngưỡng theo mức rủi ro → đặt riêng theo từng câu hỏi.

### 4.3 Pipeline Threshold Chuẩn

Phần này vẽ luồng xử lý chuẩn từ lúc gọi Jev đến lúc hành động — dùng làm khung tham chiếu khi viết code.

```
                    ┌──────────────────┐
   state ──────────►│   Jev decide     │
   questions ──────►│  (parallel,      │
                    │   70-500ms)      │
                    └────────┬─────────┘
                             │ answer + probabilities + confidence
                             ▼
                    ┌──────────────────┐
                    │  Đọc answer      │
                    │  + distribution  │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐     ┌─────────────────────┐
                    │  So confidence   │     │  Nếu flat/near-tie │
                    │  với threshold   ├────►│  → escalate bất     │
                    │  (per-question)  │     │    kể confidence    │
                    └────────┬─────────┘     └─────────────────────┘
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
         HIGH (auto)    MEDIUM (confirm)  LOW (escalate)
         code acts      user / context    human / LLM
```

**Lưu ý**: ngay cả khi confidence cao, một phân phối **flat bất thường** (margin rất mỏng giữa 2 option) vẫn nên trigger escalate — confidence và margin nên được đọc **cùng nhau**.

Cách đọc khối pipeline ở trên: từ trên xuống — gọi Jev (song song, 70–500ms), đọc đáp án kèm phân phối, so confidence với ngưỡng của từng câu hỏi; nhánh phải là đường "thoát hiểm": phân phối phẳng/gần hòa thì escalate ngay bất kể confidence; cuối cùng rẽ theo ba band ở §4.1.

> **Tóm gọn 1 câu:** Pipeline chuẩn: Jev quyết → đọc phân phối → so ngưỡng per-question → rẽ vào ba band, và phân phối phẳng luôn thắng lời confidence cao.

---

## 5. Code Pipeline Mẫu

Phần này là đoạn code Python hoàn chỉnh chạy được: gọi Jev → đọc probabilities + confidence → so threshold → act / confirm / escalate. Dùng làm khung bắt đầu cho hệ thống của bạn.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/02-5-code-pipeline-mau.py`](examples/02-5-code-pipeline-mau.py)

</details>

> **Tóm gọn 1 câu:** File mẫu ở trên gộp cả bài: gọi Jev, đọc phân phối, so ngưỡng, rẽ ba nhánh — copy về và sửa theo nghiệp vụ của bạn.

---

## 6. Logging & Observability

Phần này nói về việc ghi nhật ký cho các quyết định: ghi gì, không ghi gì, và vì sao điều đó quyết định khả năng sửa lỗi về sau. (**Observability** = khả năng quan sát được bên trong hệ thống đang chạy qua log/số liệu.)

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Logging cho decision pipeline = ghi lại **đủ thông tin để tái lập và audit một quyết định**: request id, question names, probabilities, confidence, threshold áp dụng, model version, và outcome thật (sau này). Confidence là **signal để threshold**; log là **bằng chứng để audit**.
> **Ẩn dụ/so sánh:** Giống **hồ sơ phẫu thuật** — không ghi nội dung con người (state/PII), nhưng ghi bác sĩ nào, phương pháp nào, ngưỡng nào, và kết quả ra sao, để khi có biến chứng thì truy vết được.
> **Vì sao quan trọng:** Không log → hai tháng sau bạn không giải thích được "tại sao ticket này bị auto-route sai?", và không thể tune threshold vì mất linkage giữa probability khi quyết định với outcome thực tế.

Giải nghĩa: **audit** = kiểm tra lại vết sau sự việc; **linkage** = sự nối kết giữa xác suất lúc quyết định và kết quả thật về sau; **PII** = thông tin cá nhân (email, tên, số điện thoại).

> **Tóm gọn 1 câu:** Log là bằng chứng để tái lập và audit một quyết định — không có nó thì không tune ngưỡng được và không giải thích được sự cố.

### 6.1 Checklist Log

Cách đọc khung dưới: phần ✅ LOG là các trường **nên** ghi vào nhật ký cho mỗi quyết định; phần ❌ KHÔNG LOG là những thứ **cấm** ghi; phần ⚠️ là quy tắc ngoại lệ khi buộc phải gỡ lỗi dữ liệu đầu vào.

```
┌─────────────────────────────────────────────────────────────────────┐
│                   DECISION AUDIT LOG                                │
│                                                                     │
│  ✅ LOG:                                                            │
│     • request_id            (từ response Jev)                      │
│     • question names        (tên các questions đã hỏi)             │
│     • probabilities          (phân phối đầy đủ)                    │
│     • confidence             (per answer)                           │
│     • threshold / band       (ngưỡng đã áp, high/medium/low)       │
│     • model version          (jev-1.13.0 / jev-latest)             │
│     • outcome                (label thật, phản hồi user, ...)       │
│     • timestamp                                                   │
│                                                                     │
│  ❌ KHÔNG LOG:                                                      │
│     • state (raw)             ← có thể chứa PII                    │
│     • full text input         ← customer data, emails, ...         │
│                                                                     │
│  ⚠️  Nếu cần debug state: hash/redact trước, hoặc giữ trong        │
│     storage có access control riêng                                 │
└─────────────────────────────────────────────────────────────────────┘
```

Giải nghĩa: **hash/redact** = băm (biến thành chuỗi không đọc ngược lại được) hoặc che thông tin nhạy cảm; **access control** = kiểm soát truy cập — chỉ người được phép mới đọc được.

> **Tóm gọn 1 câu:** Ghi đủ tám trường để tái lập quyết định, nhưng không bao giờ ghi state hay văn bản thô vì chứa thông tin cá nhân.

### 6.2 Mẫu Log Entry

Phần này là code mẫu Python ghi một dòng nhật ký quyết định đúng chuẩn checklist trên.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/03-6-2-mau-log-entry.py`](examples/03-6-2-mau-log-entry.py)

</details>

### 6.3 Vì Sao Outcome Quan Trọng

Log chỉ có nghĩa khi **liên kết được probability ↔ outcome**. Với cặp `(probabilities, outcome)` bạn có thể:

1. **Đo calibration thực tế** trên domain của bạn (không chỉ tin 0.8 → 80%).
2. **Tune threshold**: nếu band high (≥0.8) thực tế chỉ đúng 70% → nâng ngưỡng.
3. **Phát hiện drift**: confidence distribution lệch theo thời gian = input distribution thay đổi hoặc model version đổi.
4. **Audit khi incident**: "ticket #4821 bị auto-route sai vì confidence 0.82 nhưng outcome = sai" → truy vết được cả request_id lẫn ngưỡng.

Giải nghĩa: **drift (trôi)** = dữ liệu đầu vào hoặc hành vi model thay đổi dần theo thời gian — thấy qua phân phối confidence lệch dần.

> **Tóm gọn 1 câu:** Cặp (xác suất, kết quả thật) trong log cho phép đo calibration, tune ngưỡng, phát hiện trôi dữ liệu và truy vết sự cố.

---

> *"Confidence là signal để bạn quyết định auto-act hay escalate — không phải lý do để ngừng suy nghĩ."*

---

*Trở về [README](../README.md) — tổng quan Module XIV*

*Tiếp theo: [05 — Patterns: Xây Dựng Quyết Định Production](../05-patterns/) →*

*Trước đó: [02 — Ba Primitives — Choice, Score, Noul](../02-primitives/)*
