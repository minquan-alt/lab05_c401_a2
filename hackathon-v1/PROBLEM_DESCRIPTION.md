# VinFast Service Copilot – Chẩn đoán Xe điện thông minh (Demo Version)

---

# 1. Bối cảnh dự án

Xe điện có mức độ phần mềm hóa và điện tử hóa cao vượt trội so với xe xăng, dẫn đến quy trình chẩn đoán trở nên phức tạp và phụ thuộc nhiều vào dữ liệu phần mềm.

| Chỉ số       | Xe xăng            | Xe điện                          |
| ------------ | ------------------ | -------------------------------- |
| Số lượng ECU | ~20–30             | 70–120                           |
| Bản chất lỗi | Cơ khí chiếm đa số | Điện – Phần mềm chiếm đa số      |
| Tài liệu     | Ít thay đổi        | Firmware & TSB cập nhật liên tục |

---

# 2. Các vấn đề cốt lõi (Pain Points)

Hệ thống tập trung giải quyết các rào cản hiện tại của Kỹ thuật viên (KTV) tại xưởng dịch vụ:

- **Tài liệu quá lớn:** Cẩm nang sửa chữa (Service Manual) dài 1000–5000 trang PDF khiến việc tra cứu thủ công mất 30–120 phút mỗi ca.
- **Phụ thuộc kinh nghiệm:** KTV mới khó suy luận mã lỗi (DTC) từ triệu chứng (Symptom) mơ hồ.
- **Bỏ sót thông tin:** 80% lỗi thực tế đã có trong các bản tin kỹ thuật (TSB) nhưng thường bị KTV bỏ qua.
- **Tỷ lệ sửa lỗi lần đầu thấp:** Chẩn đoán sai dẫn đến xe phải quay lại bảo hành nhiều lần.

---

# 3. Kiến trúc Giải pháp (Solution Architecture)

Hệ thống được xây dựng trên nền tảng **Agentic RAG** điều phối bởi **LangGraph**, sử dụng dữ liệu giả lập (Mock Data) được tạo ra bởi AI phục vụ mục đích demo.

## 3.1 Nguồn dữ liệu (Data Sources)

Hệ thống "lục kho" đồng thời hai loại tài liệu chính:

### Service Manual (SM) – Kho dữ liệu tĩnh

Chứa:

- Thông số kỹ thuật
- Sơ đồ mạch điện
- Quy trình tháo lắp chuẩn

### Knowledge Base (KB) – Kho dữ liệu động

Chứa:

- Technical Service Bulletin (TSB)
- Lịch sử sửa chữa
- Phản hồi thực tế từ KTV

→ Cho phép AI học tập liên tục.

---

## 3.2 Các tính năng chính (Core Features)

### Feature 1 – Chẩn đoán & Truy xuất tích hợp

- Suy luận mã lỗi từ ngôn ngữ tự nhiên
- Trích xuất đúng phân đoạn tài liệu SM/KB liên quan

### Feature 2 – Sinh kế hoạch chẩn đoán & Checklist

- Tạo lộ trình kiểm tra tối ưu
- Đưa ra bước đo kiểm chi tiết
- Cảnh báo an toàn khi thao tác

---

# 4. Thiết kế Workflow với LangGraph

Hệ thống hoạt động theo mô hình **Stateful Graph**, cho phép rẽ nhánh dựa trên độ tự tin của AI.

---

## 4.1 Cấu trúc thư mục đề xuất

```plaintext
vinfast-service-copilot/
├── mock_data/
│   ├── sm_mock.json          # Dữ liệu cẩm nang giả lập
│   └── kb_mock.json          # Dữ liệu TSB & Lịch sử giả lập
├── src/
│   ├── agents/               # Logic của từng Agent (Triage, RAG, Planner)
│   ├── tools/                # Mock Tools để truy xuất file JSON
│   ├── graph/                # Định nghĩa State và Workflow LangGraph
│   └── main.py               # Entry point cho demo
└── README.md
```

---

## 4.2 Các Node và Logic thực thi

### Triage Node

- Phân tích triệu chứng
- Nếu thiếu thông tin (Low-confidence) → hỏi ngược lại KTV

### RAG Node

- Truy xuất đồng thời trên SM và KB
- Tổng hợp tài liệu để đưa ra chẩn đoán chính xác

### Planning Node

- Sinh checklist sửa chữa chi tiết
- Bao gồm dụng cụ, bước thực hiện, lưu ý an toàn

### Correction Node

- Tiếp nhận phản hồi sau sửa chữa
- Cập nhật kiến thức vào kho tri thức (Feedback Loop)

---

# 5. Phân tích 4 Paths (User Stories)

Hệ thống được thiết kế để xử lý mọi tình huống thực tế tại xưởng:

| Path               | Mô tả                                                                      |
| ------------------ | -------------------------------------------------------------------------- |
| **Happy**          | AI xác định đúng bệnh, hiển thị quy trình sửa từ SM và mẹo từ TSB          |
| **Low-confidence** | AI phân vân giữa nhiều nguyên nhân → yêu cầu đo điện áp để thu hẹp phạm vi |
| **Failure**        | Tài liệu không khớp thực tế → chuyển sang hỗ trợ thủ công                  |
| **Correction**     | KTV sửa theo cách khác hiệu quả hơn → nhập dữ liệu để AI học               |

---

# 6. Giá trị kỳ vọng

| Chỉ số                    | Hiện tại    | Sau Copilot |
| ------------------------- | ----------- | ----------- |
| Thời gian chẩn đoán       | 60–120 phút | 2–5 phút    |
| Thời gian đào tạo KTV mới | 6 tháng     | 1–2 tháng   |
| Tỷ lệ sửa đúng lần đầu    | ~65%        | >90%        |

---

**VinFast Service Copilot hướng tới chuẩn hóa quy trình dịch vụ, giảm phụ thuộc kinh nghiệm cá nhân và nâng cao hiệu suất sửa chữa xe điện.**
