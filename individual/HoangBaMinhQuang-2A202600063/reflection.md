# Individual reflection — Hoàng Bá Minh Quang (2A202600063)

## 1. Role
AI Infrastructure & Tools Design: Thiết kế pipeline và orchestration cho hệ thống AI; định nghĩa logic và workflow, đồng thời xây dựng và thử nghiệm các tools/prototype để validate và cải thiện system reliability.

## 2. Đóng góp cụ thể
- Thiết kế pipeline và orchestration cho hệ thống:
Input → Intent Extraction → Input Validation → 
get_repair_history → get_diagnostic → compute_confidence → 
retrieve_manual → Output

- Phát triển và tối ưu tools:
Xây dựng các tools như get_repair_history, compute_confidence
Iterate dựa trên failure cases trong quá trình testing
Thiết kế cơ chế fallback cho non-happy paths:
Khi hệ thống thiếu thông tin nhưng vẫn cần đưa ra recommendation
Áp dụng chiến lược constraint relaxation (Strict → Looser):
Bắt đầu với điều kiện chặt (high precision)
Nếu không đủ dữ liệu → nới lỏng dần để vẫn đảm bảo output khả dụng
## 3. SPEC mạnh/yếu
- Mạnh nhất: Xác định rõ failure mode “triệu chứng chung chung” dẫn đến output quá rộng; từ đó thiết kế mitigation bằng cách trigger follow-up question để thu hẹp không gian chẩn đoán.
- Yếu nhất: Hệ thống đã xác định các evaluation metrics (precision, recall) và thực hiện kiểm thử thủ công trên một số case tiêu biểu, tuy nhiên chưa xây dựng được bộ test đủ lớn và chưa có các con số định lượng cụ thể để đánh giá hiệu năng một cách hệ thống.

## 4. Đóng góp khác
- Thực hiện kiểm thử prompt với nhiều trường hợp triệu chứng khác nhau, ghi log và phân tích kết quả để cải thiện chất lượng output
- Hỗ trợ team làm rõ bài toán và định hướng giải pháp, đặc biệt trong việc xác định flow hệ thống và các failure cases chính

## 5. Điều học được
Em học được ở hackathon rất nhiều điều. Thứ nhất, teamwork rất quan trọng; việc phối hợp và giao tiếp với nhau hiệu quả là điều kiện tiên quyết để giải quyết được bài toán. Thứ hai, thiết kế failure cases là tư duy không thể thiếu trong xây dựng sản phẩm. Nó giúp em đưa từ 1 ý tưởng hay thành 1 sản phẩm thực tế. Mặc dù, bài toán chỉ vẫn đang nằm ở prototype nhưng em cảm nhận được thiết kế failure cases đúng giúp cho sản phẩm có chiều sâu hơn rất nhiều. Cuối cùng chính là MVP Canvas, thật ra là MVP Canvas em cũng đã được học trong những buổi trước đó cũng như cũng thực hành tạo ra nó rồi; nhưng phải đến buổi hackathon thì em mới nhận thấy được giá trị của MVP Canvas, nó giúp em thu hẹp scope hơn rất nhiều và giải quyết painpoint của bài toán chuẩn và sâu hơn rất nhiều.

## 6. Nếu làm lại
Nếu làm lại, em sẽ bắt đầu kiểm thử prompt và xây dựng test cases sớm hơn thay vì đợi đến giai đoạn cuối. Việc test muộn khiến số vòng iterate bị hạn chế và chưa tối ưu được chất lượng output. Ngoài ra, em sẽ xây dựng một bộ evaluation dataset có cấu trúc ngay từ đầu để có thể theo dõi sự cải thiện của hệ thống một cách định lượng qua từng iteration.

## 7. AI giúp gì / AI sai gì
- **Giúp:** Giúp: Sử dụng ChatGPT để brainstorm các failure modes, giúp nhóm phát hiện thêm những trường hợp mà ban đầu chưa nghĩ tới. Ngoài ra, sử dụng Gemini để kiểm thử prompt nhanh, hỗ trợ iterate hệ thống hiệu quả hơn.
- **Sai/mislead:** ChatGPT khi cung cấp giải pháp dựa trên SPEC + MVP Canvas thì hiểu sâu được hệ thống và như chiều sâu của bài toán, vì vậy nếu không kiểm tra kỹ thì tụi em đã không bao quát được bài toán