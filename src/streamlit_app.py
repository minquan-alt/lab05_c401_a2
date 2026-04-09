import streamlit as st
from agent import graph, _build_recent_context_messages


st.set_page_config(
    page_title="VinFast Service Copilot",
    page_icon="🚗",
    layout="wide",
)

st.title("🚗 VinFast Service Copilot")
st.caption("Symptom → DTC → Repair (SQLite + Agentic pipeline)")

with st.sidebar:
    st.subheader("Hướng dẫn")
    st.markdown(
        "- Nhập triệu chứng bằng tiếng Việt.\n"
        "- Nên thêm `model`, `model_year`, `firmware` để kết quả chính xác hơn.\n"
        "- Hệ thống vẫn đưa candidate khi thiếu metadata."
    )
    if st.button("Xóa lịch sử chat"):
        st.session_state.messages = []
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_prompt = st.chat_input("Ví dụ: VF8 2023 firmware v1.2.1 không sạc được ở trạm AC")
if user_prompt:
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    with st.chat_message("assistant"):
        with st.spinner("Copilot đang phân tích chẩn đoán..."):
            pair_history = []
            for msg in st.session_state.messages:
                role = "human" if msg["role"] == "user" else "ai"
                pair_history.append((role, msg["content"]))
            context_messages = _build_recent_context_messages(pair_history, user_prompt)
            result = graph.invoke({"messages": context_messages})
            final = result["messages"][-1]
            answer = final.content if hasattr(final, "content") else str(final)
            st.markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})
