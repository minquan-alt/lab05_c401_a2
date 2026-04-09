# VinFast Service Copilot - AI Chatbot Demo

Hệ thống chẩn đoán xe điện thông minh sử dụng LangGraph & Agentic RAG.

## Cài đặt và Chạy

### 1. Cài đặt dependencies:

```bash
pip install -r requirements.txt
```

### 2. Chọn Model LLM

Hệ thống hỗ trợ 3 loại model: **Ollama (qwen2.5:7b)**, **Google Gemini**, hoặc **OpenAI**.

#### **Option A: Ollama (qwen2.5:7b)** - Chạy trên máy [Recommended]

1. **Cài đặt Ollama** từ https://ollama.ai
2. **Pull model qwen2.5:7b:**

```bash
ollama pull qwen2.5:7b
```

3. **Chạy Ollama:**

```bash
ollama serve
```

4. **Cấu hình .env:**

```
LLM_MODEL=ollama
OLLAMA_MODEL=qwen2.5:7b
OLLAMA_BASE_URL=http://localhost:11434
```

#### **Option B: Google Gemini** - Free API

1. **Lấy API key** từ https://ai.google.dev
2. **Cấu hình .env:**

```
LLM_MODEL=gemini
GOOGLE_API_KEY=your_google_gemini_api_key_here
```

#### **Option C: OpenAI**

1. **Lấy API key** từ https://platform.openai.com
2. **Cấu hình .env:**

```
LLM_MODEL=openai
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Chạy demo:

```bash
streamlit run main.py
```

4. **Truy cập:** Mở trình duyệt và vào `http://localhost:8501`

## Kiến trúc

- **LangGraph**: Điều phối workflow stateful
- **Agents**: Triage, RAG, Planner
- **Mock Data**: Giả lập Service Manual và Knowledge Base
- **Streamlit**: Giao diện web demo
- **Multi-LLM Support**: Ollama, Gemini, OpenAI

## Cách sử dụng

1. Nhập mã xe (VIN) và triệu chứng
2. Nhấn "Chẩn đoán"
3. Hệ thống sẽ phân tích và đưa ra kế hoạch sửa chữa

## Demo Scenarios

- **Happy Path**: "Xe VF8 sạc không vào, đèn báo đỏ"
- **Low Confidence**: Triệu chứng mơ hồ
- **Failure**: Thông tin không khớp
- **Correction**: Phản hồi từ KTV

## So sánh các Model

| Model               | Tốc độ    | Chất lượng | Yêu cầu                 |
| ------------------- | --------- | ---------- | ----------------------- |
| Ollama (qwen2.5:7b) | Nhanh     | Tốt        | Máy tính mạnh + 4GB RAM |
| Google Gemini       | Rất nhanh | Xuất sắc   | API key miễn phí        |
| OpenAI (GPT-3.5)    | Rất nhanh | Xuất sắc   | Trả phí                 |
