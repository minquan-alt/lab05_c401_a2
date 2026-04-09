import os 
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Load biến môi trường (nếu có dùng trong .env)
load_dotenv()

def test_qwen_ollama():
    print("Đang kết nối tới Ollama local...")
    
    # Lấy cấu hình từ .env
    base_url = os.getenv("OLLAMA_BASE_URL")
    api_key = os.getenv("OLLAMA_API_KEY")
    model_name = os.getenv("OLLAMA_MODEL")

    # Khởi tạo ChatOpenAI trỏ tới local Ollama (OpenAI compatible)
    llm = ChatOpenAI(
        base_url=base_url,
        api_key=api_key, # Cần thiết lập key bất kỳ để bypass check của thư viện
        model=model_name,
        temperature=0.7,
        max_tokens=256
    )

    # Test gọi model
    prompt = input("Nhập câu hỏi: ")    
    
    try:
        response = llm.invoke(prompt)
        print("🤖 Response từ Qwen2.5-Coder:")
        print(response.content)
    except Exception as e:
        print(f"❌ Lỗi khi gọi model: {e}")

if __name__ == "__main__":
    test_qwen_ollama()