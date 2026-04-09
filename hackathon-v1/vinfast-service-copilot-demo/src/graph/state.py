from typing import Annotated, List, TypedDict
from operator import add

class AgentState(TypedDict):
    vin: str  # Mã định danh xe
    symptom: str  # Triệu chứng KTV nhập vào
    probable_dtcs: List[dict]  # Mã lỗi dự đoán (DTC)
    retrieved_info: Annotated[List[str], add]  # Thông tin trích xuất từ SM/KB
    repair_plan: str  # Kế hoạch sửa chữa cuối cùng
    confidence_score: float  # Điểm tin cậy (để rẽ nhánh)
    next_action: str  # Điều hướng luồng tiếp theo

    # Interactive workflow fields
    additional_questions: List[str]  # Câu hỏi bổ sung khi confidence thấp
    needs_more_info: bool  # Cờ cần thêm thông tin
    feedback_questions: List[str]  # Câu hỏi feedback sau sửa chữa
    vin_data: dict  # Dữ liệu cụ thể theo VIN