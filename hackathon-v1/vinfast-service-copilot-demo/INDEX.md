# 📚 Documentation Index - Bảng Mục Lục

## Bắt đầu nhanh 🚀

- **[QUICK_START.md](QUICK_START.md)** - 3 bước chạy demo ngay
- **[test_llm_config.py](test_llm_config.py)** - Test LLM configuration

## Hướng dẫn Chi tiết 📖

- **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Hướng dẫn cài đặt từng model (Ollama, Gemini, OpenAI)
- **[README.md](README.md)** - Tổng quan hệ thống
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Kiến trúc kỹ thuật

## Deployment & Scaling 🌐

- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Deploy lên production (Docker, AWS, GCP, Streamlit Cloud)

## Thay đổi gần đây ✨

- **[UPDATE_SUMMARY.md](UPDATE_SUMMARY.md)** - Tóm tắt các cập nhật multi-LLM

---

## 🎯 Chọn tài liệu phù hợp

### Nếu bạn muốn...

| Mục tiêu            | Tài liệu                                           |
| ------------------- | -------------------------------------------------- |
| Chạy demo ngay      | [QUICK_START.md](QUICK_START.md)                   |
| Cài Ollama chi tiết | [SETUP_GUIDE.md](SETUP_GUIDE.md) - Option 1        |
| Cài Gemini chi tiết | [SETUP_GUIDE.md](SETUP_GUIDE.md) - Option 2        |
| Cài OpenAI chi tiết | [SETUP_GUIDE.md](SETUP_GUIDE.md) - Option 3        |
| Hiểu kiến trúc      | [ARCHITECTURE.md](ARCHITECTURE.md)                 |
| Deploy lên server   | [DEPLOYMENT.md](DEPLOYMENT.md)                     |
| Troubleshoot        | [SETUP_GUIDE.md](SETUP_GUIDE.md) - Troubleshooting |

---

## 📁 Cấu trúc Thư mục Dự Án

```
vinfast-service-copilot-demo/
│
├── 📄 DOCUMENTATION
│   ├── QUICK_START.md          ← START HERE! 🚀
│   ├── SETUP_GUIDE.md          ← Chi tiết cho mỗi model
│   ├── README.md               ← General overview
│   ├── ARCHITECTURE.md         ← Technical details
│   ├── DEPLOYMENT.md           ← Production deployment
│   ├── UPDATE_SUMMARY.md       ← Recent updates
│   └── INDEX.md                ← File này
│
├── 📁 mock_data/
│   ├── service_manual_mock.json
│   └── knowledge_base_mock.json
│
├── 📁 src/
│   ├── llm_config.py           ✨ NEW - Multi-LLM support
│   ├── agents/
│   │   ├── triage_agent.py     ✏️ Updated
│   │   ├── rag_agent.py        ✏️ Updated
│   │   └── planner_agent.py    ✏️ Updated
│   ├── tools/
│   │   └── mock_tools.py
│   ├── graph/
│   │   ├── state.py
│   │   └── workflow.py
│   └── main.py                 (Old entry point)
│
├── 🐍 main.py                  ← Main entry point
├── ⚙️ .env                      ← Configuration
├── 📦 requirements.txt          ← Dependencies
├── 🧪 test_llm_config.py       ← Test script
└── 📋 files above
```

---

## 🎓 Feature Summary

### Core Features

- ✅ **Multi-LLM Support**: Ollama, Google Gemini, OpenAI
- ✅ **LangGraph Workflow**: Stateful agent orchestration
- ✅ **Agentic RAG**: Triage → RAG → Planner agents
- ✅ **Mock Data**: Service Manual + Knowledge Base
- ✅ **Streamlit UI**: Web-based interface

### New Features (Latest Update)

- ✨ **Dynamic LLM Selection**: Choose model via .env
- ✨ **Ollama Support**: qwen2.5:7b local inference
- ✨ **Gemini Support**: Free Google Gemini API
- ✨ **Easy Model Switching**: No code changes needed
- ✨ **Test Script**: Verify LLM configuration

---

## ⚡ Quick Commands

### Install & Run (Ollama Default)

```bash
pip install -r requirements.txt
# Terminal 1: Start Ollama
ollama serve &
# Terminal 2: Run app
streamlit run main.py
```

### Switch to Gemini

```bash
# Edit .env
echo "LLM_MODEL=gemini" > .env
echo "GOOGLE_API_KEY=ai_XXXX" >> .env
# Run
streamlit run main.py
```

### Test Configuration

```bash
python test_llm_config.py
```

### Deploy with Docker

```bash
docker build -t vinfast-copilot .
docker run -p 8501:8501 vinfast-copilot
```

---

## 🔗 External Resources

- **Streamlit**: https://streamlit.io
- **LangChain**: https://python.langchain.com
- **Ollama**: https://ollama.ai
- **Google Gemini**: https://ai.google.dev
- **OpenAI API**: https://platform.openai.com

---

## 💬 FAQ

**Q: Which model should I use?**

> Use Ollama for local development, Gemini for demos, OpenAI for production.

**Q: Can I switch models without restarting?**

> Hãy restart Streamlit sau khi thay đổi .env.

**Q: What if Ollama is too slow?**

> Try Gemini (free tier) or OpenAI (paid but faster).

**Q: Can I add more models?**

> Yes! Edit `src/llm_config.py` and add your LLM.

**Q: Is the system secure?**

> Yes, API keys are in .env (not in code). Ollama runs locally.

---

## 🚀 Next Steps

1. **First time?** → Start with [QUICK_START.md](QUICK_START.md)
2. **Having issues?** → Check [SETUP_GUIDE.md](SETUP_GUIDE.md) Troubleshooting section
3. **Ready for production?** → Read [DEPLOYMENT.md](DEPLOYMENT.md)
4. **Want to understand?** → Study [ARCHITECTURE.md](ARCHITECTURE.md)

---

## 📊 Status

| Component          | Status      |
| ------------------ | ----------- |
| Ollama Integration | ✅ Ready    |
| Gemini Integration | ✅ Ready    |
| OpenAI Integration | ✅ Ready    |
| Demo App           | ✅ Ready    |
| Documentation      | ✅ Complete |
| Test Suite         | ✅ Complete |
| Docker Support     | ✅ Ready    |

---

## 📞 Support

If you need help:

1. Check the relevant documentation file above
2. Run `python test_llm_config.py` to diagnose issues
3. Read the Troubleshooting section in [SETUP_GUIDE.md](SETUP_GUIDE.md)

Happy coding! 🎉
