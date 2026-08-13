# 🎙️ Live Talk / Dry-run Interview Harness

> Trong thế giới AI-native, việc test khả năng tư duy không chỉ nằm ở code. Chúng ta cần **"Live Talk"** - một môi trường để AI đóng vai trò người phỏng vấn (Interviewer), đặt ra các tình huống thực tế để stress-test khả năng đối thoại, lập luận và nhất quán của con người.

## 1. Vấn đề: Tại sao cần Dry-run Interview với AI?

Con người thường có xu hướng chuẩn bị kịch bản sẵn (scripted). Khi đối mặt với tình huống bất ngờ từ một người phỏng vấn thông minh và sắc bén (AI), chúng ta dễ dàng bộc lộ lỗ hổng trong tư duy.

```
Interview Stress Level
Prepared (Scripted)   ████                  20%
Live (AI-Interviewer) ████████████████████  100%
```

> AI là người phỏng vấn hoàn hảo: Không mệt mỏi, đặt câu hỏi logic, khách quan, và luôn xoáy sâu vào các điểm yếu (edge cases).

## 2. Định nghĩa: Live Talk / Dry-run Interview Harness

Đây là một framework nơi **AI đóng vai trò Người phỏng vấn** (Interviewer), thiết kế các kịch bản phỏng vấn kỹ thuật trực tiếp để đánh giá con người.

Mục tiêu không phải là "trả lời đúng", mà là **"phản ứng logic"** với các thay đổi giả định (hypothetical scenarios) do AI đưa ra.

### Luồng hoạt động (Simulation Loop)
```
┌─────────────────────────────────┐
│ Interviewer (AI)                │
├─────────────────────────────────┤
│ 1. Đưa tình huống thực tế       │
│ 2. Đặt áp lực (đổi yêu cầu)     │
│ 3. Đánh giá câu trả lời        │
└─────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│ Interviewee (Human)             │
├─────────────────────────────────┤
│ 1. Tiếp nhận ngữ cảnh           │
│ 2. Trả lời/Giải pháp            │
│ 3. Phản biện & điều chỉnh       │
└─────────────────────────────────┘
```

## 3. Cách tiếp cận: Phân loại tình huống & Stress test

AI (Interviewer) đánh giá con người qua 4 cấp độ áp lực:

### A. Situational (Tình huống)
- AI đưa ra yêu cầu giải quyết vấn đề với constraint cụ thể (memory, speed).
- Đánh giá khả năng ưu tiên (Trade-offs) của con người.

### B. Adaptive (Thích ứng)
- AI bất ngờ thay đổi yêu cầu giữa chừng.
- Đánh giá khả năng giữ vững logic cũ hoặc tái cấu trúc (refactor) nhanh của con người.

### C. Technical Deep-dive (Phản biện)
- AI đặt câu hỏi xoáy sâu vào tại sao lại dùng công nghệ/thuật toán đó.
- Đánh giá khả năng defend quan điểm kỹ thuật của con người.

### D. Cultural/Behavioral (Hành vi)
- AI mô phỏng tình huống xung đột với team hoặc lỗi trong production.
- Đánh giá sự trung thực, cách giải quyết xung đột (accountability) của con người.

## 4. Công thức đánh giá: Candidate Score (AI chấm)

`Candidate Score = Logic Soundness × Adaptive Speed × Clarity`

## 5. Hướng Prototype (MVP)

MVP tập trung vào khả năng "đưa tình huống bất ngờ" và "đánh giá phản ứng".

**Các bước MVP:**
1. Setup Prompt: Khởi tạo persona cho AI (Interviewer) và kịch bản phỏng vấn.
2. Interaction: Thực hiện 3-5 vòng đối thoại (AI đưa câu hỏi -> Human trả lời -> AI phản biện).
3. Evaluation: AI tự tổng hợp và chấm điểm dựa trên tiêu chí.
4. Feedback Loop: Cải thiện kịch bản phỏng vấn dựa trên kết quả.
