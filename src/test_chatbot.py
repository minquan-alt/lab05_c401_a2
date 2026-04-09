import os 
from dotenv import load_dotenv
from langchain_groq import ChatGroq

# Load biến môi trường (nếu có dùng trong .env)
load_dotenv()

def test_qwen_ollama():
    print("Đang kết nối tới Ollama local...")
    
    # Lấy cấu hình từ .env
    base_url = os.getenv("OLLAMA_BASE_URL")
    api_key = os.getenv("OLLAMA_API_KEY")
    model_name = os.getenv("OLLAMA_MODEL")

    # Khởi tạo ChatOpenAI trỏ tới local Ollama (OpenAI compatible)
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

    # Test gọi model
    prompt = input("Nhập câu hỏi: ")    
    
    try:
        response = llm.invoke(prompt)
        text = response.content if hasattr(response, 'content') else str(response)
        print("🤖 Response từ Qwen2.5-Coder:")
        print(text)
    except Exception as e:
        print(f"❌ Lỗi khi gọi model: {e}")

if __name__ == "__main__":
    test_qwen_ollama()