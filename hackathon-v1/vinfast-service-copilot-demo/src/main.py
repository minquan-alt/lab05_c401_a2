import streamlit as st
import os
import sys
from dotenv import load_dotenv

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import modules
from graph.workflow import create_workflow
from graph.state import AgentState

# Load environment variables
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

st.title("🚗 VinFast Service Copilot - Interactive AI Diagnostics")
st.markdown("Hệ thống chẩn đoán xe điện thông minh với khả năng tương tác")

# Initialize session state for workflow
if 'workflow_state' not in st.session_state:
    st.session_state.workflow_state = None
if 'iteration_count' not in st.session_state:
    st.session_state.iteration_count = 0

# Input form
with st.form("diagnosis_form"):
    vin = st.text_input("Mã xe (VIN)", placeholder="VF8-001", value="VF8-001")
    symptom = st.text_area("Mô tả triệu chứng", placeholder="Xe VF8 sạc không vào, đèn báo đỏ")
    submitted = st.form_submit_button("🚀 Bắt đầu Chẩn đoán")

# Interactive diagnostic loop
if submitted and symptom:
    st.session_state.iteration_count += 1

    # Initialize state for first iteration
    if st.session_state.iteration_count == 1:
        initial_state: AgentState = {
            "vin": vin,
            "symptom": symptom,
            "probable_dtcs": [],
            "retrieved_info": [],
            "repair_plan": "",
            "confidence_score": 0.0,
            "next_action": "",
            "additional_questions": [],
            "needs_more_info": False,
            "feedback_questions": [],
            "vin_data": {}
        }
        st.session_state.workflow_state = initial_state

    # Create and run workflow
    graph = create_workflow()

    with st.spinner("Đang phân tích..."):
        result = graph.invoke(st.session_state.workflow_state)

    # Update session state
    st.session_state.workflow_state = result

    # Display results based on workflow state
    if result.get("needs_more_info", False):
        # Ask for more information
        st.warning("⚠️ Cần thêm thông tin để chẩn đoán chính xác hơn")

        st.subheader("❓ Câu hỏi bổ sung:")
        questions = result.get("additional_questions", [])

        # Collect answers
        answers = {}
        for i, question in enumerate(questions):
            answers[f"q_{i}"] = st.text_input(question, key=f"q_{i}_{st.session_state.iteration_count}")

        if st.button("📤 Gửi câu trả lời", key=f"submit_answers_{st.session_state.iteration_count}"):
            # Update symptom with additional information
            additional_info = []
            for i, question in enumerate(questions):
                answer = answers.get(f"q_{i}", "").strip()
                if answer:
                    additional_info.append(f"{question}: {answer}")

            if additional_info:
                updated_symptom = result["symptom"] + "\n\nThông tin bổ sung:\n" + "\n".join(additional_info)
                st.session_state.workflow_state["symptom"] = updated_symptom
                st.session_state.workflow_state["needs_more_info"] = False
                st.rerun()

    elif result.get("repair_plan"):
        # Final results
        st.success("✅ Chẩn đoán hoàn thành!")

        # Display comprehensive results
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📊 Thông tin chẩn đoán")
            st.metric("Điểm tin cậy", f"{result['confidence_score']:.2f}")
            st.metric("Số mã lỗi", len(result.get('probable_dtcs', [])))

            if result.get('probable_dtcs'):
                st.write("**Mã lỗi dự đoán:**")
                for dtc in result['probable_dtcs']:
                    st.write(f"- `{dtc['code']}`: {dtc['description']}")

        with col2:
            st.subheader("🔧 Kế hoạch sửa chữa")
            if result['repair_plan']:
                # Parse markdown structure
                plan_lines = result['repair_plan'].split('\n')
                for line in plan_lines[:20]:  # Show first 20 lines
                    if line.strip():
                        st.write(line)
                if len(plan_lines) > 20:
                    st.write("... (xem đầy đủ bên dưới)")

        # Full repair plan
        with st.expander("📋 Chi tiết kế hoạch sửa chữa"):
            st.markdown(result['repair_plan'])

        # VIN-specific information
        if result.get('vin_data'):
            vin_data = result['vin_data']
            with st.expander("📋 Thông tin xe cụ thể"):
                st.write(f"**Firmware:** {vin_data.get('firmware_version', 'Unknown')}")
                st.write(f"**Lần service cuối:** {vin_data.get('last_service', 'Unknown')}")
                if vin_data.get('recall_campaign'):
                    st.error(f"⚠️ Xe đang trong chương trình thu hồi: {vin_data.get('recall_reason', '')}")
                if vin_data.get('known_issues'):
                    st.warning("**Vấn đề đã biết:**")
                    for issue in vin_data['known_issues']:
                        st.write(f"- {issue}")

        # Feedback collection
        if result.get('feedback_questions'):
            st.subheader("📝 Phản hồi sau sửa chữa")
            st.info("Vui lòng trả lời để giúp hệ thống học hỏi và cải thiện")

            feedback_answers = {}
            for i, question in enumerate(result['feedback_questions']):
                feedback_answers[f"fb_{i}"] = st.text_input(
                    question,
                    key=f"fb_{i}_{st.session_state.iteration_count}"
                )

            if st.button("💾 Gửi phản hồi", key=f"submit_feedback_{st.session_state.iteration_count}"):
                st.success("✅ Cảm ơn phản hồi! Hệ thống sẽ học hỏi từ kinh nghiệm này.")
                # In real app, would save to knowledge base

    else:
        # Intermediate state - show progress
        st.info("🔄 Đang xử lý...")

        if result.get('probable_dtcs'):
            st.subheader("🔍 Mã lỗi tìm thấy:")
            for dtc in result['probable_dtcs']:
                st.write(f"- {dtc['code']}: {dtc['description']}")

# Reset button
if st.button("🔄 Chẩn đoán mới"):
    st.session_state.workflow_state = None
    st.session_state.iteration_count = 0
    st.rerun()

# Instructions
with st.expander("📖 Hướng dẫn sử dụng"):
    st.markdown("""
    **Cách sử dụng:**
    1. Nhập mã xe (VIN) và mô tả triệu chứng chi tiết
    2. Nhấn "Bắt đầu Chẩn đoán"
    3. Nếu hệ thống cần thêm thông tin, hãy trả lời các câu hỏi
    4. Xem kết quả chẩn đoán và kế hoạch sửa chữa
    5. Gửi phản hồi để giúp hệ thống cải thiện

    **Tính năng mới:**
    - 🔄 **Chẩn đoán tương tác**: Hỏi thêm khi cần thiết
    - 📊 **Điểm tin cậy**: Đánh giá độ chính xác
    - 📋 **Kế hoạch có cấu trúc**: Dễ theo dõi
    - 📈 **Học máy**: Cải thiện từ phản hồi
    """)