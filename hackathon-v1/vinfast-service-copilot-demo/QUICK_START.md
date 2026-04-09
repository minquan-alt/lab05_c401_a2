# Quick Start - Bắt đầu nhanh

## 3 bước để chạy demo Ngay lập tức

### 1️⃣ Chọn Model Fast Track

#### ✅ Nhanh nhất (Gemini - 2 phút)

```bash
# Copy-paste vào .env
LLM_MODEL=gemini
GOOGLE_API_KEY=YOUR_GEMINI_KEY_FROM_ai.google.dev
```

#### 💻 Chạy trên máy (Ollama - 5 phút setup)

```bash
# Terminal 1: Cài Ollama
ollama pull qwen2.5:7b
ollama serve

# Terminal 2: Chạy demo
cd vinfast-service-copilot-demo
streamlit run main.py
```

### 2️⃣ Install & Run

```bash
# Nếu chưa cài packages
pip install -r requirements.txt

# Chạy demo
streamlit run main.py
```

### 3️⃣ Truy cập

Mở browser: **http://localhost:8501**

---

## Test Case Thử

Nhập vào form:

**VIN:** `VF8-001`

**Triệu chứng:** `Xe VF8 sạc không vào, đèn báo đỏ`

Nhấn "Chẩn đoán" và xem kết quả!

---

## Xác minh Model

Khi chạy demo, bạn sẽ thấy dòng:

```
🤖 Model hiện tại: qwen2.5:7b (ollama)
```

Hoặc:

```
🤖 Model hiện tại: gemini-2.5-flash (gemini)
```

---

## Troubleshoot Nhanh

| Lỗi                     | Giải pháp                                        |
| ----------------------- | ------------------------------------------------ |
| Port 8501 đang dùng     | Chạy: `streamlit run main.py --server.port 8502` |
| Ollama Connection Error | `ollama serve` đang chạy chưa?                   |
| ImportError             | `pip install -r requirements.txt`                |
| API Key Invalid         | Copy đúng key từ trang chính thức                |

---

## File Cấu hình Quan trọng

- **.env** - Chứa model config
- **src/llm_config.py** - Logic chọn model
- **SETUP_GUIDE.md** - Hướng dẫn chi tiết
- **main.py** - Entry point chính
