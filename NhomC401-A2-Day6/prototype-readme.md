# Prototype — VinFast Service Copilot

## Mô tả
Chatbot hỗ trợ Kỹ thuật viên (KTV) nhập thông tin xe (Model, Firmware) và mô tả triệu chứng. AI sẽ phân tích, gợi ý top 3 mã lỗi (DTC) khả dĩ kèm xác suất (Confidence score). Khi KTV chọn 1 mã lỗi, AI trích xuất hướng dẫn sửa chữa từ Service Manual kèm theo cảnh báo an toàn điện cao áp (HV) bắt buộc. KTV có thể xác nhận hiệu quả hoặc feedback sửa lỗi.

## Level: Working prototype
- UI build bằng Streamlit
- Flow chạy thật (Agentic workflow): KTV nhập triệu chứng → AI tự động gọi Tool tra cứu lịch sử sửa chữa → Trích xuất Service Manual → Trả kết quả + Cảnh báo an toàn.

## Links
- Github: https://github.com/minquan-alt/lab05_c401_a2/tree/main/src

## Tools
- UI: Streamlit (Python web app) / Terminal Console.
- AI: Qwen2.5-Coder (main), Google Gemini 2.0 Flash (fallback)
- Prompt: System prompt định hướng "Safety-first" + Mock Database (các file JSON giả lập Lịch sử chẩn đoán và Service Manual của xe điện VF)

## Phân công
| Thành viên | Phần | Output |
|-----------|------|--------|
| Quang |Top 3 failure, agent.py, tools.py|SPEC, agent.py, tools.py|
| Long |Canvas, ROI, System Prompt|SPEC, system_prompt.txt|
| Nhân |Mini AI SPEC, System Prompt|SPEC, system_prompt.txt|
| Tài |User Stories, agent.py|SPEC, agent.py|
| Quân |User Stories, tool get_diagnostic|SPEC, tools.py|
| Huy |Metrics & Eval, System Prompt|SPEC, system_prompt.txt|
