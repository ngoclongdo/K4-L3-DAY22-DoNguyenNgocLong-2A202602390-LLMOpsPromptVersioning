# Báo Cáo Phân Tích Thực Nghiệm: Prompt V1 vs Prompt V2 (RAGAS Evaluation)

Tài liệu này cung cấp bản phân tích định lượng và định tính nhằm so sánh hiệu năng giữa hai phiên bản prompt trong hệ thống RAG phục vụ Day 22 Lab.

---

## 1. Kết Quả Định Lượng (Quantitative Metrics)

Đánh giá được thực hiện tự động qua framework **RAGAS** với 50 cặp câu hỏi - đáp chuẩn (`QA_PAIRS`), sử dụng model `gemma-4-26b-a4b-it` (Google GenAI) và embedding model `models/gemini-embedding-001`.

| Metric | Prompt V1 (Concise) | Prompt V2 (Expert Analysis) | Winner | Nhận xét |
| :--- | :---: | :---: | :---: | :--- |
| **Faithfulness** | **0.9880** ⭐ | 0.9828 ⭐ | **← V1** | Cả hai phiên bản đều vượt trội mục tiêu ($\ge 0.8$), không có hiện tượng ảo giác (hallucination). |
| **Answer Relevancy** | **0.8189** | 0.8099 | **← V1** | V1 trả lời trực diện, ngắn gọn trong 2-4 câu nên độ tập trung vào câu hỏi cao hơn. |
| **Context Recall** | 0.9722 | **1.0000** ⭐ | **← V2** | V2 đạt điểm số tuyệt đối 100%, phản ánh khả năng thu thập đầy đủ toàn bộ thông tin chuẩn. |
| **Context Precision** | **0.9952** | 0.9567 | **← V1** | Retriever xếp hạng các đoạn văn bản có độ liên quan cao nhất ở các vị trí đầu. |

---

## 2. Phân Tích Định Tính (Qualitative Analysis)

### Prompt V1 — Phong cách súc tích (Concise Assistant)
- **Thiết kế Prompt**: Yêu cầu câu trả lời ngắn gọn (2–4 câu), trực diện và tuyệt đối bám sát ngữ cảnh.
- **Ưu điểm**:
  - Tốc độ phản hồi nhanh, tiết kiệm đáng kể token đầu ra.
  - Độ chính xác sự thật rất cao (**Faithfulness = 0.9880**), hạn chế tối đa việc thêm các câu dẫn giải dư thừa.
  - Tương thích tốt cho các giao diện chatbot tra cứu nhanh, FAQ trên thiết bị di động.
- **Hạn chế**:
  - Đôi khi bỏ sót một số ý chi tiết mang tính bổ trợ trong các câu hỏi phức tạp.

### Prompt V2 — Phong cách chuyên gia (Senior AI Analyst)
- **Thiết kế Prompt**: Đóng vai chuyên gia phân tích cấp cao, cấu trúc mạch lạc, phân tích đa chiều và logic từ 3–5 câu hoặc chia mục rõ ràng.
- **Ưu điểm**:
  - Đạt điểm số tuyệt đối ở độ bao quát thông tin (**Context Recall = 1.0000**), câu trả lời đầy đủ ngữ cảnh và mang tính học thuật cao.
  - Văn phong chuyên nghiệp, phù hợp với hệ thống báo cáo kỹ thuật, tài liệu phân tích hoặc hỗ trợ nghiên cứu.
- **Hạn chế**:
  - Token tiêu thụ nhiều hơn V1, độ dài câu trả lời lớn hơn.

---

## 3. Kết Luận & Khuyến Nghị Vận Hành

1. **Khuyến nghị sử dụng**:
   - Dùng **Prompt V1** làm mặc định cho các truy vấn tra cứu định nghĩa, khái niệm ngắn và hỗ trợ khách hàng thông thường để tối ưu chi phí và độ trễ.
   - Định tuyến người dùng sang **Prompt V2** khi hệ thống nhận diện các câu hỏi dạng so sánh, giải thích cơ chế chuyên sâu hoặc yêu cầu phân tích tổng hợp.
2. **Tuân thủ tiêu chí Rubric**:
   - Điểm số `faithfulness` của cả hai phiên bản đều đạt $\ge 0.8$ (đạt $0.9880$ và $0.9828$).
   - Dữ liệu đánh giá chi tiết được đồng bộ đầy đủ tại [03_ragas_report.json](03_ragas_report.json).
