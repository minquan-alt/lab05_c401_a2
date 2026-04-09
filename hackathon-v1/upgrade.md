Đề xuất Cải tiến Hệ thống VinFast Service Copilot (Demo Version)

Tài liệu này phân tích các điểm hạn chế hiện tại trong mã nguồn và đề xuất các chỉnh sửa cụ thể cho Agents, Workflow và Mock Data nhằm nâng cấp hệ thống từ demo pipeline thành Agentic Expert System.

1. Cải tiến các Agent (Node Logic)
   1.1 Triage Agent (triage_agent.py)
   ❌ Vấn đề hiện tại

Logic xác định mã lỗi DTC đang hardcode bằng if/else:

if "charging" in symptom:
dtc = "P0xxx"

Điều này:

Không tận dụng khả năng reasoning của LLM
Không mở rộng được
Không scale theo dữ liệu
✅ Đề xuất cải tiến

Bước 1 — Dùng LLM trích xuất tín hiệu kỹ thuật

LLM cần trích xuất:

hệ thống nghi ngờ (battery / motor / inverter / charging)
từ khóa kỹ thuật

Ví dụ output mong muốn:

{
"suspected_systems": ["battery", "charging"],
"keywords": ["cannot charge", "slow charging"]
}

Bước 2 — Tạo Tool tra cứu DTC

Tạo tool mới:

search_dtc_by_symptom()

Thay vì gán cứng, agent sẽ:

trích xuất keywords bằng LLM
gọi tool tra service_manual_mock.json
trả về danh sách DTC tiềm năng

👉 Triage trở thành reasoning + tool use.

1.2 RAG Agent (rag_agent.py)
❌ Vấn đề hiện tại

Nếu không có DTC → Agent không thể truy vấn Service Manual.

Pipeline bị gãy.

✅ Đề xuất: Cross Retrieval Strategy

Cho phép truy vấn theo 2 chế độ:

Mode Khi nào dùng
DTC search Có DTC
System keyword search Không có DTC

Nếu không có DTC:

dùng suspected_systems
tìm các quy trình kiểm tra tổng quát

Ví dụ:

"battery system diagnostic procedure"

👉 Workflow không bị dừng sớm.

1.3 Planner Agent (planner_agent.py)
❌ Vấn đề hiện tại

Output là free text → khó hiển thị UI.

✅ Đề xuất: Structured Markdown Output

Bắt buộc LLM trả về Checklist Markdown:

## 🔧 Tools Required

- Multimeter
- OBD Scanner

## 🔎 Diagnostic Steps

1. Measure battery voltage
2. Check connector pins

## 📊 Expected Values

- Voltage: 350–400V

👉 UI có thể render đẹp + dễ parse.

2. Tối ưu hóa Workflow (workflow.py)

Hiện tại workflow kết thúc khi confidence thấp.
Điều này chưa đạt chuẩn Agentic Workflow.

2.1 Thêm Node “Ask More Info”
❌ Hiện tại
confidence thấp → END
✅ Mới
confidence thấp → hỏi thêm thông tin → quay lại triage

Ví dụ câu hỏi:

Tiếng kêu khi xe đứng yên hay di chuyển?
Lỗi xuất hiện khi pin dưới 20%?

👉 Tạo interactive diagnostic loop.

2.2 Feedback / Correction Loop
❌ Vấn đề

ARCHITECTURE.md có nhắc Correction Path nhưng chưa có node.

✅ Thêm Node update_knowledge_base

Sau khi sửa xong:

KTV xác nhận kết quả thực tế
Agent lưu vào knowledge_base_mock.json

👉 Bắt đầu hình thành Data Flywheel.

3. Nâng cấp Mock Data

Để demo khả năng reasoning, cần thêm dữ liệu có xung đột.

3.1 Xung đột tài liệu (RAG reasoning demo)

Ví dụ:

Service Manual Knowledge Base (TSB)
Thay pin HV Chỉ cần cập nhật firmware

👉 Agent phải ưu tiên:

TSB mới hơn
dữ liệu thực tế
3.2 VIN-Specific Data

Thêm trường:

{
"vin": "...",
"firmware_version": "1.0.3",
"recall_campaign": true
}

Agent có thể reasoning:

xe có thuộc diện recall không
có cần update software không 4. Workflow đề xuất (LangGraph)
def create_workflow():
workflow = StateGraph(AgentState)

    workflow.add_node("triage", triage_agent)
    workflow.add_node("rag", rag_agent)
    workflow.add_node("planner", planner_agent)
    workflow.add_node("ask_info", ask_info_node)
    workflow.add_node("save_feedback", feedback_node)

    def triage_routing(state):
        if state["confidence_score"] > 0.7:
            return "rag"
        return "ask_info"

    workflow.add_conditional_edges("triage", triage_routing)
    workflow.add_edge("ask_info", "triage")
    workflow.add_edge("rag", "planner")
    workflow.add_edge("planner", "save_feedback")
    workflow.add_edge("save_feedback", END)

    return workflow.compile()

5. Kết luận

Sau cải tiến, hệ thống sẽ chuyển từ:

Pipeline tra cứu
→ thành
Agentic Expert System

Hệ thống mới có khả năng:

suy luận
đặt câu hỏi
kiểm chứng
tự học từ thực tế
