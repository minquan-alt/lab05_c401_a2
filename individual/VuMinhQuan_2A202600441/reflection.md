# Individual reflection — Vũ Minh Quân (2A202600441)

## 1. Role
UX designer + prompt engineer. Phụ trách thiết kế flow chatbot và viết system prompt.

## 2. Đóng góp cụ thể
- Thiết kế conversation flow 2 bước (hỏi tình trạng xe-> chat bot sinh ra câu trả lời)
- viết work flow hoạt động của chat bot. Nếu AI chắc chắn với độ confident cao thì user sẽ nhìn thấy câu trả lười trực tiếp. Nếu AI chưa rõ thì sẽ hỏi thêm 1 số câu hỏi để có thêm dữ liệu cho câu trả lời. Nếu AI trả lời sai người dùng sẽ feedback trực tiếp thông qua ux. Nếu người dùng không tin hoặc AI không biết rõ trả lười như thế nào sẽ gửi câu "xin mời liên lạc với bộ phận kỹ thuật của vinfast để biết thêm thông tin".
- Viết và test 3 phiên bản system prompt, chọn v3 vì precision tốt nhất trên 10 test cases
- thiết kế user stories.
- viết tool get_diagnostic.
- Vẽ poster layout cho demo.

## 3. SPEC mạnh/yếu
- Điểm sáng giá nhất trong bản SPEC là khả năng dự báo các tình huống hệ thống hoạt động không hiệu quả, đặc biệt là nhóm "Triệu chứng chung chung" (Vague Symptoms).

Vấn đề: Trong thực tế sửa chữa xe VinFast, có những lỗi như "xe không khởi động được" hoặc "màn hình chập chờn" có thể do hàng trăm nguyên nhân (từ phần mềm, ắc quy đến lỗi phần cứng chuyên sâu). Nếu AI gợi ý quá rộng, kỹ thuật viên sẽ bị rối.

Giải pháp (Mitigation): SPEC đã thiết kế cơ chế Truy vấn ngược (Follow-up questioning). Thay vì đưa ra danh sách dài các mã lỗi, chatbot sẽ yêu cầu kỹ thuật viên kiểm tra thêm các thông số cụ thể (ví dụ: điện áp ắc quy, phiên bản phần mềm hiện tại) để thu hẹp phạm vi chẩn đoán.

Giá trị: Điều này giúp giảm thiểu thời gian "thử và sai" (trial and error) tại xưởng, đảm bảo tính chính xác và an toàn khi can thiệp vào hệ thống xe điện phức tạp.

- Điểm yếu nhất: Tính toán hiệu quả đầu tư (ROI)
Hiện tại, phần phân tích ROI đang là mắt xích yếu nhất do sự thiếu hụt về mặt phân hóa dữ liệu giữa các kịch bản.

Vấn đề: Cả 3 kịch bản tài chính hiện tại thực chất chỉ là sự thay đổi về quy mô số lượng người dùng (User count), trong khi các giả định cốt lõi (Assumptions) lại gần như trùng lặp, khiến việc đánh giá rủi ro chưa thực sự khách quan.

Hướng khắc phục (Refinement): Cần tách biệt rõ ràng các giả định về phạm vi triển khai để thấy được sự khác biệt về chi phí vận hành và lợi nhuận:

Kịch bản Thận trọng (Conservative): Hệ thống chỉ triển khai thử nghiệm tại 01 chi nhánh trọng điểm. Tập trung vào việc hoàn thiện bộ dữ liệu (Knowledge Base) và đo lường độ chính xác của AI.

Kịch bản Lạc quan (Optimistic): Rollout (triển khai đồng loạt) trên toàn bộ hệ thống xưởng dịch vụ VinFast toàn quốc. Giả định hệ thống giúp giảm 30% thời gian xử lý mỗi ca sửa chữa, từ đó tối ưu hóa công suất phục vụ của xưởng.

## 4. Đóng góp khác
- test promt với 3 case khác nhau
1. Happy Case — rõ ràng, đủ thông tin
Case 1.1 — Charging issue (firmware bug)
Ground truth
Model: VF8 2023 v1.2.x
DTC: P1A12
Fix: update firmware

Prompt 1
VF8 2023 firmware v1.2.1 không sạc được ở trạm AC, xe báo lỗi pin
Prompt 2
Xe VF8 đời 2023, không nhận sạc AC, nghi có lỗi BMS, firmware hiện tại v1.2.1
Prompt 3
VF8 2023 bị lỗi không sạc, có thể do firmware, hiện đang chạy v1.2

Expected behavior
High confidence
Output: P1A12
Suggest: update firmware
Có repair steps + warning

2. Low-confidence Case — thiếu thông tin
Case 2.1 — vague charging issue
Ground truth
Có thể là P1A12 hoặc P0A80

Prompt 1
Xe không sạc được
Prompt 2
VF8 bị lỗi sạc nhưng không rõ nguyên nhân
Prompt 3
Xe điện VinFast không nhận sạc, không biết đời nào

Expected behavior
Không đưa kết luận chắc chắn
Output:
2–3 DTC candidates
yêu cầu thêm:
model_year
firmware
Có gợi ý kiểm tra tiếp

3. Failure Case — false correlation
Case 3.1 — same symptom, wrong mapping
Ground truth
Model: VF8 2022
DTC: P0A80
Fix: thay pin

Prompt 1
VF8 2022 không sạc được, xe báo lỗi pin
Prompt 2
Xe VF8 đời cũ bị lỗi không sạc, firmware không rõ
Prompt 3
VF8 2022 bị lỗi giống như firmware bug, có cần update không?

Expected behavior
Không nhầm sang P1A12
Phải phân biệt theo version
Suggest kiểm tra pin (không phải firmware)

## 5. Điều học được
- học được các kiến thức về metric khác nhau như: precision và recall.
+  Precision được tính bằng tỷ lệ giữa số điểm dữ liệu dự đoán đúng là tích cực (True Positives - TP) trên tổng số điểm dữ liệu mà mô hình đã dự đoán là tích cực,
+ Recall được tính dựa trên tỷ lệ giữa số điểm dữ liệu dự đoán đúng là tích cực (True Positives - TP) trên tổng số điểm dữ liệu thực tế là tích cực
- thiết kế sản phẩm AI mad có thể đáp ứng yêu cầu của 4 paths.

## 6. Nếu làm lại
sẽ tập chung vào làm spec ngày 5 để làm rõ vấn đề. Để ngày 6 có thể tiến hành một cách trôi chảy hơn.

## 7. AI giúp gì / AI sai gì
Claude (Tư duy hệ thống): Hỗ trợ brainstorm các lỗi xe điện (Failure Modes) phức tạp. AI đã gợi ý kịch bản "xung đột tín hiệu điều khiển giữa các ECU" — một dạng lỗi "triệu chứng chung chung" rất khó bắt bài mà ban đầu nhóm chưa liệt kê hết.

Gemini (Tối ưu phản hồi): Sử dụng Google AI Studio để tinh chỉnh Prompt. Giúp chatbot đưa ra chỉ dẫn sửa chữa ngắn gọn, đúng thuật ngữ chuyên ngành của VinFast (ví dụ: thay vì nói "kiểm tra dây điện", AI gợi ý "kiểm tra thông mạch đầu nối J2 trên bộ sạc").

7.2. AI đã sai/mislead gì?
Gợi ý lạc đề: Claude đề xuất tích hợp thêm tính năng "đặt lịch bảo dưỡng cho chủ xe". Dù hay nhưng tính năng này phục vụ khách hàng (B2C), trong khi mục tiêu của nhóm là hỗ trợ kỹ thuật viên (B2B).

Bài học (Scope Control): Suýt chút nữa nhóm đã bị cuốn vào Scope Creep (phình đại phạm vi). Nhóm rút ra bài học: AI có thể gợi ý ý tưởng không giới hạn, nhưng người làm dự án phải tỉnh táo để giữ chatbot tập trung vào cốt lõi là "giảm thời gian chẩn đoán lỗi tại xưởng".
