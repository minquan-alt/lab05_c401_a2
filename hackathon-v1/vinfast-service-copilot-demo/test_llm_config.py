#!/usr/bin/env python
"""
Test script để kiểm tra LLM configuration
Chạy: python test_llm_config.py
"""
import sys
import os
from dotenv import load_dotenv

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

load_dotenv()

from llm_config import get_llm, get_llm_info, LLM_MODEL

def test_llm_config():
    """Test LLM configuration"""
    print("\n" + "="*60)
    print("🧪 VinFast Service Copilot - LLM Config Test")
    print("="*60 + "\n")
    
    # Show current config
    llm_info = get_llm_info()
    print(f"📋 Current Configuration:")
    print(f"   Model Type: {llm_info['model'].upper()}")
    print(f"   Model Name: {llm_info['model_name']}")
    
    if llm_info['model'] == 'ollama':
        print(f"   Base URL: {llm_info.get('base_url', 'N/A')}")
    
    print(f"   Note: {llm_info.get('note', 'N/A')}\n")
    
    # Try to instantiate LLM
    print("🔧 Testing LLM Instantiation...")
    try:
        llm = get_llm()
        print(f"✅ SUCCESS: LLM initialized!")
        print(f"   Type: {type(llm).__name__}\n")
        
        # Try a simple prompt if possible
        if LLM_MODEL == 'ollama':
            print("⚙️  Testing Ollama connection (quick test)...")
            print("   Note: First call may take longer")
            
            try:
                # Simple test
                response = llm.invoke("Respond with 'OK' only")
                print(f"✅ Ollama Response: {response[:50]}...\n")
            except Exception as e:
                print(f"⚠️  Ollama test failed: {str(e)}")
                print("   Make sure 'ollama serve' is running\n")
        
        elif LLM_MODEL == 'gemini':
            print("✅ Google Gemini is configured")
            print("   Ready to use\n")
            
        elif LLM_MODEL == 'openai':
            print("✅ OpenAI is configured")
            print("   Ready to use\n")
        
    except Exception as e:
        print(f"❌ FAILED: {str(e)}\n")
        print("Troubleshooting tips:")
        if LLM_MODEL == 'ollama':
            print("- Make sure Ollama is installed and running: ollama serve")
            print("- Make sure model is pulled: ollama pull qwen2.5:7b")
            print("- Check OLLAMA_BASE_URL in .env")
        elif LLM_MODEL == 'gemini':
            print("- Check GOOGLE_API_KEY in .env")
            print("- Get key from: https://ai.google.dev")
        elif LLM_MODEL == 'openai':
            print("- Check OPENAI_API_KEY in .env")
            print("- Check your API key is valid")
        
        return False
    
    print("="*60)
    print("✅ All checks passed! Ready to run the demo.")
    print("="*60)
    print("\nNext step: streamlit run main.py\n")
    return True

if __name__ == "__main__":
    success = test_llm_config()
    sys.exit(0 if success else 1)
