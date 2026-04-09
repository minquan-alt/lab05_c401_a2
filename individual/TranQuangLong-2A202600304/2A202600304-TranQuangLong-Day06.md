# Individual reflection — [Trần Quang Long - 2A202600304]
## 1. Role
**AI Product Analyst & Prompt Architect.** Phụ trách xây dựng mô hình kinh tế (ROI), định hình chiến lược sản phẩm (Canvas) và thiết lập các quy tắc an toàn (Guardrails) cho hệ thống Prompt.

## 2. Đóng góp cụ thể
- **Thiết kế ROI & Business Case:** Xây dựng bảng tính ROI cho 3 kịch bản (Conservative, Realistic, Optimistic), chứng minh khả năng tiết kiệm chi phí thông qua việc giảm 15 phút tra cứu mỗi lượt cho KTV.
- **Xây dựng Safety Guardrails cho Prompt:** Trực tiếp soạn thảo các quy tắc nghiêm ngặt về an toàn điện cao áp (HV), lực siết (torque) và yêu cầu trích dẫn (citation). Đây là "xương sống" để AI không đưa ra các chỉ dẫn gây nguy hiểm tính mạng.
- **Cấu trúc hóa dữ liệu đầu vào:** Thiết lập bộ lọc thông tin bắt buộc (Model, Year, Firmware, Mileage) giúp AI thu hẹp phạm vi chẩn đoán, giảm thiểu sai sót do lệch phiên bản xe.

## 3. SPEC mạnh/yếu
- **Mạnh nhất: Failure Modes & Mitigation.** Nhờ việc tập trung sâu vào an toàn kỹ thuật, phần này được đầu tư rất kỹ, giải quyết được nỗi lo lớn nhất của VinFast về hallucination.
- **Yếu nhất: ROI Assumptions.** Các giả định về thời gian tiết kiệm (15 phút/lượt) vẫn mang tính lý thuyết và chưa có dữ liệu thực tế từ xưởng để kiểm chứng. Nếu có thêm thời gian, mình sẽ thực hiện khảo sát nhanh với 1-2 KTV thực thụ để lấy con số baseline chuẩn hơn (có lẽ sẽ hơi khó lấy dữ liệu vì xe Vinfast rất tốt và rất ít hỏng).

## 4. Đóng góp khác
- **Debug & Khắc phục Vòng lặp Agent:** Phát hiện và xử lý lỗi AI rơi vào vòng lặp vô tận khi gọi tool trên model Gemini 3.1 Flash Lite. Tham gia cấu trúc lại luồng ReAct để AI biết điểm dừng sau khi đã có dữ liệu.
- **Hỗ trợ Triage Logic:** Phối hợp cùng nhóm dev để định nghĩa khi nào AI nên đưa ra nhiều giả thuyết (multiple hypotheses) thay vì kết luận duy nhất, nhằm tránh thiên kiến xác nhận (automation bias).

## 5. Điều học được
- Trước đây mình nghĩ AI chỉ cần trả lời đúng là đủ. Qua hackathon này, mình nhận ra với các ngành đặc thù như sửa chữa xe điện, **"Biết nói không" (I don't know)** và **"Cung cấp bằng chứng" (Citation)** còn quan trọng hơn việc trả lời nhanh. AI không chỉ là công cụ tạo nội dung, nó phải là một hệ thống có kiểm soát (controlled system).
- Qua khảo sát với các nhóm đối thủ (trong zone và ngoài zone), mình còn nhận thấy AI rất hay có xu hướng generalize câu trả lời theo thông tin được train sẵn ở base model thay vì trả lời theo đúng yêu cầu. Ngoài ra, dù cùng một hệ thống design AI, các model khác nhau sẽ đưa ra behavior khác nhau và câu trả lời khác nhau.
- Hơn nữa, bắt ép AI không nhảy ra out-of-scope vẫn là một điều quan trọng chưa nhóm nào làm hoàn hảo hẳn được. Chính bản thân mình khi làm system prompt và tools cũng bug lòi mắt.

## 6. Nếu làm lại
Mình sẽ xây dựng một **"Cơ chế kiểm tra chéo" (Cross-check layer)** bằng mã code cứng cho các thông số critical như lực siết ốc (torque). Thay vì chỉ dặn AI qua prompt (vốn vẫn có xác suất fail), mình sẽ dùng regex hoặc một database nhỏ để filter các thông số này trước khi hiển thị cho KTV, đảm bảo an toàn tuyệt đối 100%.

## 7. AI giúp gì / AI sai gì
- **Giúp:** Claude và Gemini rất mạnh trong việc gợi ý các kịch bản ROI và các rủi ro kỹ thuật (như lệch firmware ECU) mà người ngoài ngành có thể bỏ sót. AI giúp cấu trúc hóa bảng SPEC từ những ý tưởng rời rạc rất nhanh.
- **Sai/mislead:** Khi được hỏi về các thông số an toàn trước khi có prompt rules chặt chẽ, AI thường xuyên tự bịa ra (hallucinate) các mức điện áp và lực siết nghe rất thuyết phục nhưng sai lệch hoàn toàn, hơn nữa còn generalize nhiều thông tin trong câu trả lời không đi theo dummy data. Bài học: AI rất giỏi sáng tạo nhưng rất tệ trong việc tự nhận ra giới hạn kiến thức của chính mình.
