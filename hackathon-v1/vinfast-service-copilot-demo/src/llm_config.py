"""
LLM Configuration Module
Supports: Ollama (qwen2.5:7b), Google Gemini, OpenAI
"""
import os
from dotenv import load_dotenv

load_dotenv()

# LLM_MODEL = os.getenv("LLM_MODEL", "ollama").lower()
LLM_MODEL = "gemini"

def get_llm():
    """Get configured LLM instance based on environment variable."""
    
    if LLM_MODEL == "ollama":
        from langchain_ollama import OllamaLLM
        
        ollama_model = os.getenv("OLLAMA_MODEL", "qwen2.5:7b")
        ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        
        return OllamaLLM(
            model=ollama_model,
            base_url=ollama_base_url,
            temperature=0.1
        )
    
    elif LLM_MODEL == "gemini":
        from langchain_google_genai import ChatGoogleGenerativeAI
        
        google_api_key = os.getenv("GOOGLE_API_KEY")
        if not google_api_key:
            raise ValueError("GOOGLE_API_KEY not found in .env file")
        
        return ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=google_api_key,
            temperature=0.1
        )
    
    elif LLM_MODEL == "openai":
        from langchain_openai import ChatOpenAI
        
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            raise ValueError("OPENAI_API_KEY not found in .env file")
        
        return ChatOpenAI(
            model="gpt-3.5-turbo",
            api_key=openai_api_key,
            temperature=0.1
        )
    
    else:
        raise ValueError(f"Unknown LLM_MODEL: {LLM_MODEL}. Choose from: ollama, gemini, openai")

def get_llm_info():
    """Get information about the currently configured LLM."""
    if LLM_MODEL == "ollama":
        return {
            "model": LLM_MODEL,
            "model_name": os.getenv("OLLAMA_MODEL", "qwen2.5:7b"),
            "base_url": os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
            "note": "Make sure Ollama is running and model is pulled"
        }
    elif LLM_MODEL == "gemini":
        return {
            "model": LLM_MODEL,
            "model_name": "gemini-2.5-flash",
            "note": "Requires GOOGLE_API_KEY in .env"
        }
    elif LLM_MODEL == "openai":
        return {
            "model": LLM_MODEL,
            "model_name": "gpt-3.5-turbo",
            "note": "Requires OPENAI_API_KEY in .env"
        }
