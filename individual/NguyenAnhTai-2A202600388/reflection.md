# Individual reflection — Nguyễn Anh Tài (2A202600388)

## 1. Role

User stories + Agent.py. Phụ trách thiết kế kiến trúc Agentic Workflow và logic chẩn đoán kỹ thuật từ triệu chứng xe (Symptom) sang mã lỗi (DTC).

## 2. Đóng góp cụ thể

- Phối hợp thiết kế agent_node sử dụng vòng lặp ReAct tự chứa (Max 5 iterations), hỗ trợ song song cả Native Tool Calling (cho model mạnh) và Fallback JSON Parsing (cho model yếu như Qwen2.5-Coder chạy cục bộ)
- System Prompt: Viết và tinh chỉnh prompt điều hướng AI chỉ sử dụng dữ liệu từ công cụ, không tự suy diễn mã lỗi để đảm bảo an toàn kỹ thuật.
- Xây dựng hàm hỗ trợ parse input và match với tài liệu

## 3. SPEC mạnh/yếu

- Mạnh nhất:Khả năng xử lý Failure Modes của Model. Nếu LLM không hỗ trợ tool_calls chuẩn, hàm \_parse_tool_call_from_text vẫn cứu được lệnh gọi bằng cách parse regex JSON từ content.
- Yếu nhất: độ trễ, do sử dụng model nhẹ kết hợp với việc loop qua nhiều tool. cần tối ưu bằng các chạy song song các tool không phụ thuộc

## 4. Đóng góp khác

- thử các test-case và chỉnh sửa system_prompt
- Kiểm thử thực tế trên 20 kịch bản lỗi xe VinFast khác nhau để căn chỉnh regex cho firmware.

## 5. Điều học được

Trước khi làm dự án này, tôi nghĩ Agent chỉ là gọi một hàm. Sau khi viết agent_node, tôi hiểu rằng "Deterministic fallback" (quy trình định hướng dự phòng) là sống còn cho các hệ thống chuyên gia. AI có thể sáng tạo, nhưng quy trình kỹ thuật ô tô phải tuân thủ nghiêm ngặt. Việc kết hợp giữa sự linh hoạt của ReAct và sự chặt chẽ của Pipeline truyền thống giúp hệ thống vừa thông minh vừa đáng tin cậy

## 6. Nếu làm lại

Tôi sẽ triển khai thêm Semantic Cache. Đối với các triệu chứng phổ biến (VD: "VF8 không sạc được pin"), hệ thống có thể trả về kết quả ngay từ cache thay vì chạy lại toàn bộ pipeline chẩn đoán, giúp giảm chi phí tính toán và tăng tốc độ phản hồi.

## 7. AI giúp gì / AI sai gì

- **Giúp:** :Sử dụng GitHub Copilot để viết nhanh các hàm. Dùng ChatGPT để brainstorm các tiêu chí tính toán độ tin cậy dựa trên mức độ khớp của mã lỗi và tinh chỉnh system prompt.. fdadsf
- **Sai/mislead:** AI đưa ra các hàm không chính xác, nối các tools/node không hợp lý; giao diện có vài lỗi UI. Tạo user stories với scope quá rộng.
- Bài học: Agent thông minh nhất là Agent biết khi nào nên dừng suy nghĩ để chạy theo một quy trình định hướng đã được kiểm chứng.
