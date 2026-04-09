VinFast Service Copilot - LangGraph & Agentic RAG Architecture (Demo)

1. Tổng quan hệ thống
   Hệ thống sử dụng LangGraph để xây dựng một quy trình chẩn đoán có trạng thái (stateful workflow), giúp Kỹ thuật viên (KTV) đi từ triệu chứng ban đầu đến kế hoạch sửa chữa chi tiết.

Feature 1: Chẩn đoán & Truy xuất giải pháp tích hợp.

Feature 2: Sinh kế hoạch chẩn đoán & Checklist sửa chữa.

2. Kiến trúc thư mục (Folder Structure)
   Vì đây là bản demo không sử dụng database, chúng ta sẽ lưu trữ tài liệu (SM và KB) dưới dạng tệp JSON/Markdown để AI dễ dàng truy xuất thông qua các hàm Python đơn giản.

Plaintext
vinfast-service-copilot-demo/
├── mock_data/
│ ├── service_manual_mock.json # Chứa quy trình chuẩn, thông số kỹ thuật
│ └── knowledge_base_mock.json # Chứa TSB và lịch sử sửa chữa giả lập
├── src/
│ ├── agents/
│ │ ├── triage_agent.py # Phân tích triệu chứng ban đầu
│ │ ├── rag_agent.py # Truy xuất & Suy luận (Feature 1)
│ │ └── planner_agent.py # Sinh Checklist (Feature 2)
│ ├── tools/
│ │ └── mock_tools.py # Các hàm tìm kiếm dữ liệu trong tệp JSON
│ ├── graph/
│ │ ├── state.py # Định nghĩa AgentState (Pydantic/TypedDict)
│ │ └── workflow.py # Định nghĩa các Node và Edges của LangGraph
│ └── main.py # Điểm khởi chạy demo
├── .env # Lưu API Key (OpenAI/Anthropic)
└── requirements.txt

3. Định nghĩa AgentState (Trạng thái luồng)
   Trạng thái là trái tim của LangGraph, giúp dữ liệu được tích lũy và luân chuyển giữa các Agent.

Python
from typing import Annotated, List, TypedDict
from operator import add

class AgentState(TypedDict):
vin: str # Mã định danh xe
symptom: str # Triệu chứng KTV nhập vào
probable_dtcs: List[dict] # Mã lỗi dự đoán (DTC)
retrieved_info: Annotated[List[str], add] # Thông tin trích xuất từ SM/KB
repair_plan: str # Kế hoạch sửa chữa cuối cùng
confidence_score: float # Điểm tin cậy (để rẽ nhánh)
next_action: str # Điều hướng luồng tiếp theo

4. Luồng thực thi (Workflow Nodes)

Node 1: Triage Agent (Phân loại)
Nhiệm vụ: Tiếp nhận triệu chứng, chuẩn hóa ngôn ngữ tự nhiên thành các từ khóa kỹ thuật.

Logic rẽ nhánh: \* Nếu thông tin đủ: Chuyển sang RAG_Agent.

Nếu mơ hồ (Low-confidence): Quay lại hỏi KTV để bổ sung thông tin (vòng lặp).

Node 2: RAG Agent (Suy luận & Truy xuất)
Nhiệm vụ: Tìm kiếm đồng thời trong service_manual_mock.json và knowledge_base_mock.json.

Dữ liệu: Kết hợp quy trình chuẩn của hãng với các bản tin TSB mới nhất để đưa ra mã lỗi (DTC) dự kiến.

Node 3: Planner Agent (Sinh kế hoạch)
Nhiệm vụ: Tổng hợp các mảnh thông tin thành một Checklist hoàn chỉnh: Dụng cụ cần dùng -> Các bước đo kiểm -> Lưu ý an toàn điện cao áp.

Node 4: Feedback Agent (Hiệu chỉnh)
Nhiệm vụ: Nhận phản hồi từ KTV (Correction Path). Nếu KTV báo "Failure", Agent sẽ ghi nhận cách sửa thực tế và cập nhật vào biến retrieved_info để "học" ngay trong phiên làm việc đó.

5. Các Tool định nghĩa cho Demo (Mock Tools)
   Thay vì gọi database, các tool này sẽ đọc trực tiếp từ tệp JSON được AI generate sẵn:

get_sm_details(dtc_code): Trả về hướng dẫn tháo lắp và thông số kỹ thuật chuẩn từ service_manual_mock.json.

get_kb_insights(symptom): Trả về các ca sửa chữa tương tự hoặc TSB liên quan từ knowledge_base_mock.json.

verify_safety_standards(): Trả về danh sách kiểm tra an toàn bắt buộc khi làm việc với pin xe điện.

6. Chiến lược giả lập dữ liệu (Mocking Strategy)
   Vì bạn muốn AI tự generate tài liệu, quy trình demo sẽ như sau:

Giai đoạn chuẩn bị (Setup): Sử dụng LLM (GPT/Claude) với một prompt chuyên dụng để tạo ra 2 tệp JSON lớn mô phỏng dữ liệu của VinFast (ví dụ: các mã lỗi liên quan đến sạc, pin, phần mềm ADAS).

Giai đoạn thực thi (Execution): \* KTV nhập: "Xe VF8 sạc không vào, đèn báo đỏ".

LangGraph sẽ điều phối các Agent "lục tìm" trong 2 tệp JSON này như thể đang truy vấn một Vector Database thực thụ.

7. Các bước để xây dựng hoàn chỉnh
   Generate Dữ liệu: Tạo các tệp Mock Data dựa trên cấu trúc mô tả trong dự án.

Định nghĩa Graph: Sử dụng langgraph.graph.StateGraph để nối các Node (Triage -> RAG -> Planner).

Thiết lập Edges: Cài đặt conditional_edges để xử lý các trường hợp Failure hoặc Low-confidence (quay lại Node Triage).

Chạy Main: Khởi tạo trạng thái ban đầu và gọi graph.stream() để quan sát cách các Agent trao đổi thông tin với nhau.
