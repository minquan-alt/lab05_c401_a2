import streamlit as st
import os
import sys
import logging
from io import StringIO
from dotenv import load_dotenv

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import modules
from src.graph.workflow import create_workflow
from src.llm_config import get_llm_info
from src.workflow_logger import workflow_logger

# Load environment variables
load_dotenv()

# Configure page
st.set_page_config(
    page_title="VinFast Service Copilot",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🚗 VinFast Service Copilot - AI Chatbot Demo")
st.markdown("Hệ thống chẩn đoán xe điện thông minh sử dụng **LangGraph** & **Agentic RAG**")

# Sidebar - Configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Display LLM info
    llm_info = get_llm_info()
    st.write(f"🤖 **Model:** {llm_info['model_name']}")
    st.write(f"📍 **Type:** {llm_info['model'].upper()}")
    
    if llm_info['model'] == 'ollama':
        st.write(f"🔗 **URL:** {llm_info.get('base_url', 'N/A')}")
    
    st.info(f"ℹ️ {llm_info.get('note', 'N/A')}")
    
    # Show keyboard shortcuts
    st.markdown("---")
    st.subheader("⌨️ Local Test Cases")
    
    test_cases = {
        "Charging Issue": "Xe VF8 sạc không vào, đèn báo đỏ",
        "Battery Issue": "Pin yếu, xe chạy không được xa",
        "Motor Issue": "Xe mất công suất, không đi được",
    }
    
    if st.button("📋 Copy Quick Test"):
        st.info("Nhấn một case dưới đây để copy")

# Main content - Two tabs
tab1, tab2, tab3 = st.tabs(["🔍 Diagnosis", "📊 Detailed Logs", "📚 Documentation"])

with tab1:
    st.subheader("Nhập thông tin xe và triệu chứng")
    
    # Input form
    with st.form("diagnosis_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            vin = st.text_input("Mã xe (VIN)", placeholder="VF8-001", value="VF8-001")
        
        with col2:
            model = st.selectbox("Model xe", ["VF8", "VF9", "VF e34"])
        
        symptom = st.text_area(
            "Mô tả triệu chứng", 
            placeholder="Xe VF8 sạc không vào, đèn báo đỏ",
            height=100
        )
        
        submitted = st.form_submit_button("🔍 Bắt đầu Chẩn đoán", use_container_width=True)

    if submitted and symptom:
        # Capture logs
        log_capture = StringIO()
        log_handler = logging.StreamHandler(log_capture)
        log_handler.setFormatter(
            logging.Formatter('%(asctime)s | %(levelname)-8s | %(message)s', datefmt='%H:%M:%S')
        )
        workflow_logger.logger.addHandler(log_handler)
        
        try:
            # Initialize state
            initial_state = {
                "vin": vin,
                "symptom": symptom,
                "probable_dtcs": [],
                "retrieved_info": [],
                "repair_plan": "",
                "confidence_score": 0.0,
                "next_action": ""
            }
            
            # Create and run workflow
            workflow_logger.section("INITIALIZING WORKFLOW")
            workflow_logger.info(f"VIN: {vin}")
            workflow_logger.info(f"Model: {model}")
            workflow_logger.info(f"Symptom: {symptom}")
            
            graph = create_workflow()
            
            # Progress indicator
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            status_text.info("⏳ Đang tải LLM Model...")
            progress_bar.progress(20)
            
            status_text.info("🔍 TRIAGE: Phân tích triệu chứng...")
            progress_bar.progress(35)
            
            status_text.info("📖 RAG: Truy xuất dữ liệu...")
            progress_bar.progress(65)
            
            status_text.info("🔧 PLANNER: Sinh kế hoạch sửa chữa...")
            progress_bar.progress(90)
            
            # Run the workflow
            result = graph.invoke(initial_state)
            
            progress_bar.progress(100)
            status_text.success("✅ Chẩn đoán hoàn thành!")
            
            # Display results in columns
            st.markdown("---")
            st.subheader("📋 Kết Quả Chẩn Đoán")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Điểm Tin Cậy", f"{result['confidence_score']:.2f}", 
                         delta="✅ Cao" if result['confidence_score'] > 0.7 else "⚠️ Thấp")
            
            with col2:
                st.metric("Mã Lỗi", len(result['probable_dtcs']), 
                         delta=f"{[d['code'] for d in result['probable_dtcs'][:1]]}")
            
            with col3:
                st.metric("Dữ Liệu Truy Xuất", len(result['retrieved_info']), 
                         delta="SM + KB + Synthesis")
            
            # Columns for detailed results
            st.markdown("---")
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("🔍 Thông Tin Chẩn Đoán")
                
                st.write(f"**📊 Độ Tin Cậy:** {result['confidence_score']:.1%}")
                
                if result['probable_dtcs']:
                    st.write("**🚨 Mã Lỗi Dự Đoán:**")
                    for dtc in result['probable_dtcs']:
                        with st.container():
                            col_code, col_desc = st.columns([1, 3])
                            with col_code:
                                st.code(dtc['code'], language=None)
                            with col_desc:
                                st.write(f"*{dtc['description']}*")
                else:
                    st.warning("Không có mã lỗi được xác định")
            
            with col2:
                st.subheader("🔧 Kế Hoạch Sửa Chữa")
                
                if result['repair_plan']:
                    st.markdown(result['repair_plan'])
                else:
                    st.warning("Không có kế hoạch sửa chữa được tạo.")
            
            # Retrieved information section
            if result['retrieved_info']:
                st.markdown("---")
                st.subheader("📚 Thông Tin Tham Khảo")
                
                with st.expander("📖 Xem Chi Tiết Dữ Liệu Truy Xuất", expanded=False):
                    for i, info in enumerate(result['retrieved_info'], 1):
                        st.write(f"**[{i}]** {info[:200]}..." if len(info) > 200 else f"**[{i}]** {info}")
            
            # Store logs for detailed tab
            st.session_state['last_logs'] = log_capture.getvalue()
            
        except Exception as e:
            st.error(f"❌ Lỗi trong quá trình chẩn đoán: {str(e)}")
            workflow_logger.error(f"Workflow error: {e}")
            st.session_state['last_logs'] = log_capture.getvalue()
        
        finally:
            workflow_logger.logger.removeHandler(log_handler)

    elif submitted and not symptom:
        st.error("❌ Vui lòng nhập triệu chứng!")

with tab2:
    st.subheader("📊 Detailed Execution Logs")
    
    st.info("""
    📝 Xem log chi tiết của từng bước thực thi:
    - Triage Agent: Phân tích triệu chứng
    - RAG Agent: Truy xuất dữ liệu
    - Planner Agent: Sinh kế hoạch
    - LLM Calls: Gọi model AI
    """)
    
    if 'last_logs' in st.session_state and st.session_state['last_logs']:
        # Display logs
        st.code(st.session_state['last_logs'], language='log')
        
        # Download logs
        st.download_button(
            label="⬇️ Download Logs",
            data=st.session_state['last_logs'],
            file_name="diagnosis_logs.txt",
            mime="text/plain"
        )
    else:
        st.warning("Chưa có log nào. Hãy chạy chẩn đoán để xem log chi tiết.")

with tab3:
    st.subheader("📚 Documentation")
    
    docs = {
        "🚀 Quick Start": "START_HERE.md",
        "📖 Setup Guide": "SETUP_GUIDE.md",
        "🏗️ System Architecture": "SYSTEM_ARCHITECTURE.md",
        "📊 Architecture Diagram": "ARCHITECTURE.md",
        "🔧 Deployment": "DEPLOYMENT.md",
    }
    
    st.write("**Chọn tài liệu để đọc:**")
    
    for title, filename in docs.items():
        if os.path.exists(f"{os.path.dirname(__file__)}/{filename}"):
            with st.expander(title):
                try:
                    with open(f"{os.path.dirname(__file__)}/{filename}", "r", encoding="utf-8") as f:
                        content = f.read()
                        st.markdown(content[:2000] + "..." if len(content) > 2000 else content)
                except Exception as e:
                    st.error(f"Lỗi đọc file: {e}")

# Footer
st.markdown("---")
st.markdown("""
**VinFast Service Copilot v2.0** | 
🤖 Multi-LLM Support (Ollama, Gemini, OpenAI) | 
📊 LangGraph Workflow | 
🔍 Agentic RAG
""")
st.markdown("Hệ thống sẽ phân tích và đưa ra kế hoạch sửa chữa")