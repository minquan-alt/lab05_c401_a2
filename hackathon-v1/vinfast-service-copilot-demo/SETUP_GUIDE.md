# Hướng dẫn Chi tiết - Chọn Model LLM

## 🚀 Giới thiệu

Hệ thống VinFast Service Copilot hỗ trợ 3 loại mô hình AI:

- **Ollama (qwen2.5:7b)** - Chạy cục bộ trên máy tính
- **Google Gemini** - API miễn phí từ Google
- **OpenAI (GPT-3.5)** - API trả phí từ OpenAI

---

## Option 1️⃣: Ollama (qwen2.5:7b) - Chạy trên máy [Được khuyến nghị]

### Tại sao chọn Ollama?

✅ Chạy hoàn toàn trên máy (không cần kết nối mạng để suy luận)
✅ Miễn phí 100%
✅ Bảo mật dữ liệu (không gửi lên cloud)
✅ Tốc độ hợp lý cho các tác vụ diagnostic

### Cách cài đặt

#### Bước 1: Cài Ollama

1. Tải Ollama từ: https://ollama.ai
2. Cài đặt ứng dụng theo hướng dẫn

#### Bước 2: Pull model qwen2.5:7b

```bash
ollama pull qwen2.5:7b
```

Lần đầu tiên sẽ mất vài phút để download model (~4GB)

#### Bước 3: Chạy Ollama

```bash
ollama serve
```

Cần giữ cửa sổ này mở khi chạy demo

#### Bước 4: Cấu hình .env

Mở file `.env` trong thư mục `vinfast-service-copilot-demo`:

```
LLM_MODEL=ollama
OLLAMA_MODEL=qwen2.5:7b
OLLAMA_BASE_URL=http://localhost:11434
```

#### Bước 5: Chạy demo

```bash
cd vinfast-service-copilot-demo
streamlit run main.py
```

---

## Option 2️⃣: Google Gemini - Free API

### Tại sao chọn Gemini?

✅ Miễn phí với một số yêu cầu
✅ Chất lượng cao (sử dụng Gemini Pro)
✅ Không cần cài đặt bổ sung
✅ Nhanh chóng

### Cách cài đặt

#### Bước 1: Lấy API Key

1. Vào https://ai.google.dev
2. Click "Get API Key"
3. Tạo project hoặc chọn project hiện có
4. Sao chép API Key

#### Bước 2: Cấu hình .env

```
LLM_MODEL=gemini
GOOGLE_API_KEY=ai_XXXXXXXXXXXXXXXXXXXX
```

#### Bước 3: Chạy demo

```bash
streamlit run main.py
```

---

## Option 3️⃣: OpenAI (GPT-3.5)

### Tại sao chọn OpenAI?

✅ Chất lượng tốt nhất
✅ Yên tâm về tính ổn định
✅ Hỗ trợ mạnh mẽ

### Nhược điểm

❌ Cần API Key (trả phí)
❌ Gửi dữ liệu lên cloud

### Cách cài đặt

#### Bước 1: Lấy API Key

1. Vào https://platform.openai.com
2. Tạo API Key trong Settings
3. Sao chép API Key

#### Bước 2: Cấu hình .env

```
LLM_MODEL=openai
OPENAI_API_KEY=sk-XXXXXXXXXXXXXXXXXXXXXXXX
```

#### Bước 3: Chạy demo

```bash
streamlit run main.py
```

---

## 🔄 Chuyển đổi Model

Để chuyển đổi model, chỉ cần:

1. Chỉnh sửa file `.env`
2. Thay đổi giá trị `LLM_MODEL` thành: `ollama`, `gemini`, hoặc `openai`
3. Restart ứng dụng Streamlit (Ctrl+C và chạy lại)

Ví dụ:

```
# Từ Ollama sang Gemini
LLM_MODEL=gemini
GOOGLE_API_KEY=ai_XXXXXXXXXXXX
```

---

## 🐛 Troubleshooting

### Vấn đề: "ModuleNotFoundError: No module named 'ollama'"

**Giải pháp:** Cài đặt langchain-ollama

```bash
pip install langchain-ollama
```

### Vấn đề: "Connection refused" khi dùng Ollama

**Giải pháp:**

1. Kiểm tra Ollama đang chạy: `ollama serve`
2. Kiểm tra port 11434 có mở không

### Vấn đề: "Invalid API Key" khi dùng Gemini

**Giải pháp:**

1. Kiểm tra lại API Key
2. Đảm bảo API được enable trong Google Cloud Console

### Vấn đề: Model không hoạt động sau khi cập nhật .env

**Giải pháp:**

1. Thoát Streamlit (Ctrl+C)
2. Chạy lại: `streamlit run main.py`

---

## 📊 So sánh Chi tiết

| Tiêu chí        | Ollama            | Gemini           | OpenAI          |
| --------------- | ----------------- | ---------------- | --------------- |
| Giá             | Miễn phí          | Miễn phí/Trả phí | Trả phí         |
| Tốc độ          | Trung bình        | Rất nhanh        | Rất nhanh       |
| Chất lượng      | Tốt               | Xuất sắc         | Xuất sắc        |
| Yêu cầu CPU     | Cao (6GB+ RAM)    | Thấp             | Thấp            |
| Bảo mật dữ liệu | Tối cao           | Trung bình       | Trung bình      |
| Cấu hình        | Phức tạp          | Đơn giản         | Đơn giản        |
| Dành cho        | Local development | Production free  | Production paid |

---

## 💡 Khuyến nghị

- **Cho development địa phương**: Dùng **Ollama**
- **Cho demo hoặc bản dùng thử**: Dùng **Google Gemini**
- **Cho production với budget**: Dùng **OpenAI**

---

## 📞 Cần giúp?

Nếu gặp vấn đề, hãy:

1. Kiểm tra file `.env` đã cấu hình đúng
2. Kiểm tra logs trong Streamlit
3. Đảm bảo module cần thiết đã cài: `pip install -r requirements.txt`
