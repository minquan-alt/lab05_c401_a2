"""
Additional Workflow Nodes for Interactive Diagnostics
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from graph.state import AgentState
from llm_config import get_llm
from workflow_logger import workflow_logger, log_agent_input, log_agent_output
from tools.mock_tools import get_vin_specific_data

def ask_info_node(state: AgentState) -> AgentState:
    """Ask technician for additional information when confidence is low."""

    workflow_logger.section("ASK MORE INFO NODE")
    state["current_stage"] = "ask_info"
    log_agent_input("ASK_INFO", {
        "current_confidence": state.get("confidence_score", 0),
        "symptom": state["symptom"]
    })

    # Track ask-info attempts to avoid repeated loops
    state["ask_info_attempts"] = state.get("ask_info_attempts", 0) + 1

    # Generate questions based on current state
    questions = []

    if state.get("confidence_score", 0) < 0.7 and state["ask_info_attempts"] == 1:
        symptom_lower = state["symptom"].lower()

        # Add specific questions based on symptom
        if any(word in symptom_lower for word in ["charge", "sạc", "charging"]):
            questions.extend([
                "Mã lỗi cụ thể xuất hiện trên màn hình là gì?",
                "Đèn báo hiệu màu gì khi sạc (xanh/đỏ/vàng)?",
                "Thời điểm nào vấn đề xảy ra (đầu/between/cuối quá trình sạc)?",
                "Đã thử sạc ở trạm khác chưa?"
            ])
        elif any(word in symptom_lower for word in ["battery", "pin", "ắc quy"]):
            questions.extend([
                "Mức pin hiện tại là bao nhiêu %?",
                "Vấn đề xảy ra khi pin dưới mức nào?",
                "Đã thay pin hay cập nhật phần mềm gần đây?"
            ])
        elif any(word in symptom_lower for word in ["motor", "động cơ", "power"]):
            questions.extend([
                "Vấn đề xảy ra khi xe đứng yên hay đang chạy?",
                "Âm thanh lạ từ động cơ (kêu/ồn/rung)?",
                "Hệ thống lái có hoạt động bình thường?"
            ])

        # General questions
        questions.extend([
            "Xe đã đi được bao nhiêu km?",
            "Đã có sửa chữa gì gần đây?"
        ])

    state["additional_questions"] = questions
    state["needs_more_info"] = bool(questions)

    if questions:
        workflow_logger.info(f"Generated {len(questions)} questions for technician")
        for i, q in enumerate(questions[:3]):  # Log first 3 questions
            workflow_logger.info(f"  ❓ {q}")
    else:
        workflow_logger.info("Không còn câu hỏi bổ sung. Tiếp tục phân tích với dữ liệu hiện có.")

    log_agent_output("ASK_INFO", {
        "questions_count": len(questions),
        "needs_more_info": True
    })

    return state

def feedback_node(state: AgentState) -> AgentState:
    """Collect feedback and update knowledge base for continuous learning."""

    workflow_logger.section("FEEDBACK NODE")
    state["current_stage"] = "feedback"
    log_agent_input("FEEDBACK", {
        "vin": state["vin"],
        "final_diagnosis": state.get("repair_plan", "")[:100]
    })

    # Get VIN-specific data for context
    workflow_logger.tool_call("get_vin_specific_data", {"vin": state["vin"]})
    vin_data = get_vin_specific_data(state["vin"])
    workflow_logger.tool_result("get_vin_specific_data", {
        "firmware": vin_data.get("firmware_version"),
        "recall_status": vin_data.get("recall_campaign")
    })

    # Generate feedback questions
    feedback_questions = [
        "Kết quả chẩn đoán có chính xác không?",
        "Quy trình sửa chữa có hiệu quả?",
        "Thời gian thực hiện có hợp lý?",
        "Có lưu ý gì thêm cho trường hợp tương tự?"
    ]

    state["feedback_questions"] = feedback_questions
    state["vin_data"] = vin_data

    workflow_logger.info("Feedback collection initiated for continuous learning")
    workflow_logger.info(f"VIN {state['vin']} data: Firmware {vin_data.get('firmware_version', 'Unknown')}")

    if vin_data.get("recall_campaign"):
        workflow_logger.warning(f"⚠️  Vehicle {state['vin']} is under recall: {vin_data.get('recall_reason', '')}")

    log_agent_output("FEEDBACK", {
        "feedback_questions_count": len(feedback_questions),
        "vin_data_available": bool(vin_data.get("firmware_version") != "Unknown")
    })

    return state