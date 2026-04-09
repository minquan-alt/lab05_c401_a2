# Reflection - Đỗ Lê Thành Nhân (2A202600361)

## 1. Role cụ thể trong nhóm
**AI Architect & Prompt Engineer**: Chịu trách nhiệm thiết kế logic "bộ não" cho Agent (thông qua Mini AI SPEC) và trực tiếp lập trình cơ chế điều phối suy luận (Reasoning Loop) trong code.

## 2. Phần phụ trách cụ thể
- **Thiết kế Mini AI SPEC**: Định nghĩa mô hình "Proactive Detective" và quy trình chẩn đoán 3 bước.
  - *Output*: `NhomC401-A2-Day6/SPEC.md` ==section Mini-SPEC==
- **Xây dựng System Prompt v2.0**: Chuẩn hóa quy tắc hành xử cho Agent, tích hợp logic chẩn đoán 3 bước và an toàn HV.
  - *Output*: `src/system_prompt.txt` (Hệ thống Rules: Proactive Detective, Cảnh báo an toàn HV, và Format phản hồi 5 phần chuẩn kỹ thuật).
- **Xử lý khi tool trả kết quả rỗng**: Tự động gợi ý hướng đi khác khi kết quả tìm kiếm tài liệu bị rỗng, giúp hệ thống không bị "treo" về mặt logic trước người dùng.
  - *Output*: Logic `Empty Result Handling` trực tiếp trong hàm `agent_node` tại file `src/agent.py`.

```python
# Logic tự sửa lỗi khi kết quả tool rỗng
if "[]" in result_str or "not found" in result_str.lower():
    feedback_msg = f"Kết quả từ {tool_name} rỗng. Hãy thử gọi get_diagnostic trực tiếp với triệu chứng."
```

## 3. SPEC phần nào mạnh nhất, phần nào yếu nhất? Vì sao?
- **Mạnh nhất**: Phần **Diagnostic Loop (3 Steps)**. Vì nó tạo ra một "khung xương" logic cực kỳ chặt chẽ, buộc AI phải đi từ dữ liệu lịch sử sửa chữa đến tài liệu kỹ thuật SM, giảm thiểu tối đa sự sai lệch trong chẩn đoán.
- **Yếu nhất**: Phần **Learning Signal / Feedback Loop**. Vì hiện tại đây mới chỉ là định nghĩa logic về SPEC, chưa có code thực thi để tự động cập nhật Vector DB từ phản hồi của KTV ngay lập tức.

## 4. Đóng góp cụ thể khác
- **Debug & Refactor Agent Loop**: Phát hiện và xử lý lỗi Agent bị "quên" context của xe qua các iterations. Tôi đã đóng góp logic `Context Refinement` vào `agent.py` để tự động "tiêm" lại thông tin xe vào mỗi vòng lặp mà không làm code bị rối.
- **Tăng tính bền bỉ cho Agent**: Thêm logic nhắc nhở AI gợi ý hướng đi khác khi kết quả tìm kiếm tài liệu bị rỗng, giúp hệ thống không bị "treo" về mặt logic trước người dùng.

## 5. 1 điều học được trong hackathon mà trước đó chưa biết
Qua trải nghiệm trong hackathon lần này mình cảm thấy từ lý thuyết đến thực hành là 2 câu chuyện khác nhau. Hiểu sâu bài toán và vạch ra kế hoạch chi tiết để triển khai từng module là bài học quan trọng nhất mà mình học được. Oke thời đại AI có thể bùng nổ, nhà nhà người người Vibe code nhưng cuối cùng thì ai hiểu bài toán đủ sâu và tìm ra cách giải quyết cũng như thi công phần nền thật vững thì vẫn là cốt lõi mà chúng ta cần hướng đến trong thời đại này. Cảm ơn những người bạn xung quanh đã cho tôi góc nhìn mới về cách tiếp cận, cách học và ý tưởng táo bạo, hơn thế nữa là không ngại dấn thân để biến nó thành thực tế và tranh luận nó với nhau.Cảm ơn!


## 6. Nếu làm lại, đổi gì?
Tôi sẽ triển khai thêm tính năng **"Multi-Step Search Expansion"**. Cụ thể: Nếu tìm mã lỗi (DTC) không ra kết quả, code sẽ tự động sử dụng LLM để "dịch" triệu chứng sang các thuật ngữ kỹ thuật phổ biến hơn trước khi gọi tool tìm kiếm lại lần 2, thay vì chỉ báo kết quả rỗng.

## 7. AI giúp gì? AI sai/mislead ở đâu?
- **AI giúp gì**: Hỗ trợ cực tốt trong việc cấu trúc lại ý tưởng SPEC thành văn bản chuyên nghiệp và sinh ra các đoạn code xử lý chuỗi JSON/Regex phức tạp để trích xuất ngữ cảnh xe.
- **AI sai/mislead**: AI đôi khi "mất dấu" (mislead) về cấu trúc file thực tế của dự án, đề xuất các thay đổi logic có thể gây phá vỡ code của các thành viên khác (ví dụ: nhầm lẫn giữa Native Tool Calling của OpenAI và vòng lặp Fallback cho Qwen2.5-Coder:7B). Tôi đã phải kiểm tra thủ công để đảm bảo code đóng góp là "non-breaking".
