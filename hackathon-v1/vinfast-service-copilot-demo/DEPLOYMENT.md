# Production Deployment Guide

## 🚀 Deployment Options

VinFast Service Copilot hỗ trợ nhiều cách deploy tùy thuộc vào model LLM và hạ tầng của bạn.

---

## Option 1: Deploy với Ollama (Chạy trên máy chủ)

### Yêu cầu

- Server với ít nhất 6GB RAM
- Python 3.13+
- Ollama installed

### Bước Deploy

```bash
# 1. Clone/Copy project
git clone <repo> vinfast-copilot
cd vinfast-copilot

# 2. Cài dependencies
pip install -r requirements.txt

# 3. Cấu hình .env
echo "LLM_MODEL=ollama" > .env
echo "OLLAMA_MODEL=qwen2.5:7b" >> .env
echo "OLLAMA_BASE_URL=http://localhost:11434" >> .env

# 4. Chạy Ollama (background)
nohup ollama serve &

# 5. Pull model
ollama pull qwen2.5:7b

# 6. Chạy Streamlit
streamlit run main.py --server.port 8501 --server.address 0.0.0.0
```

### Monitoring

```bash
# Kiểm tra Ollama status
curl http://localhost:11434/api/tags

# Kiểm tra Streamlit logs
tail -f ~/.streamlit/logs/*.log
```

---

## Option 2: Deploy với Google Gemini (Cloud API)

### Yêu cầu

- Google Account
- API Key từ https://ai.google.dev
- Server với 1GB+ RAM

### Bước Deploy

```bash
# 1. Setup project
git clone <repo> vinfast-copilot
cd vinfast-copilot

# 2. Cài dependencies
pip install -r requirements.txt

# 3. Cấu hình .env
echo "LLM_MODEL=gemini" > .env
echo "GOOGLE_API_KEY=ai_XXXXXXXXXXXX" >> .env

# 4. Chạy Streamlit
streamlit run main.py --server.port 8501 --server.address 0.0.0.0
```

### Advantages

✅ Chạy trên cloud/lightweight server
✅ Không cần GPU/CPU mạnh
✅ Tự động scale
✅ Minimal maintenance

---

## Option 3: Deploy với Docker

### Dockerfile cho Ollama

```dockerfile
FROM python:3.13-slim

WORKDIR /app

# Install Ollama
RUN curl https://ollama.ai/install.sh | sh

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Expose ports
EXPOSE 8501 11434

# Start Ollama and Streamlit
CMD ollama serve & streamlit run main.py --server.port 8501 --server.address 0.0.0.0
```

### Build & Run

```bash
docker build -t vinfast-copilot .
docker run -p 8501:8501 -p 11434:11434 vinfast-copilot
```

---

## Option 4: Deploy trên Streamlit Cloud (Gemini)

### Yêu cầu

- Streamlit Cloud Account
- GitHub Repository
- Google API Key

### Bước Deploy

1. **Push code lên GitHub**

   ```bash
   git add .
   git commit -m "Deploy to Streamlit Cloud"
   git push origin main
   ```

2. **Deploy trên Streamlit Cloud**
   - Vào https://share.streamlit.io
   - Click "New app"
   - Chọn repository, branch, file
   - Click "Deploy"

3. **Cấu hình secrets**
   - Vào Settings > Secrets
   - Thêm:

   ```
   GOOGLE_API_KEY = "ai_XXXXXXXXXXXX"
   LLM_MODEL = "gemini"
   ```

4. **Xong!** App sẽ deploy tự động

---

## Option 5: Deploy trên AWS/GCP/Azure

### AWS avec Gemini

```bash
# 1. Create EC2 instance
# - t3.micro (free tier eligible)
# - Ubuntu 22.04

# 2. SSH vào instance
ssh -i key.pem ubuntu@instance-ip

# 3. Setup
sudo apt update && sudo apt install python3-pip
git clone <repo>
cd vinfast-copilot
pip install -r requirements.txt

# 4. Run as service
sudo systemctl edit streamlit.service
# [Unit]
# Description=VinFast Service Copilot
# After=network.target
#
# [Service]
# Type=simple
# User=ubuntu
# WorkingDirectory=/home/ubuntu/vinfast-copilot
# Environment="LLM_MODEL=gemini"
# Environment="GOOGLE_API_KEY=ai_XXXX"
# ExecStart=/usr/bin/python3 -m streamlit run main.py --server.port 8501
# Restart=always
#
# [Install]
# WantedBy=multi-user.target

sudo systemctl start streamlit.service
```

### GCP App Engine

```yaml
# app.yaml
runtime: python313

env: standard

entrypoint: streamlit run main.py --server.port 8080

env_variables:
  LLM_MODEL: "gemini"

includes:
  - !include secrets.yaml
```

```bash
gcloud app deploy
```

---

## Performance Optimization

### Database Caching (Optional)

```python
# Thêm vào mock_tools.py để cache
import functools

@functools.lru_cache(maxsize=128)
def get_sm_details(dtc_code: str):
    # Cached retrieval
    ...
```

### Rate Limiting (cho Gemini)

```python
from langchain_core.rate_limiters import InMemoryRateLimiter

rate_limiter = InMemoryRateLimiter(
    requests_per_second=10,
    check_every_n_seconds=0.1,
)

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    rate_limiter=rate_limiter
)
```

### Load Balancing (Multi-instance)

```bash
# Chạy multiple instances
streamlit run main.py --server.port 8501 &
streamlit run main.py --server.port 8502 &
streamlit run main.py --server.port 8503 &

# Dùng nginx để load balance
# upstream streamlit {
#     server localhost:8501;
#     server localhost:8502;
#     server localhost:8503;
# }
```

---

## Monitoring & Logging

### Setup Logging

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/var/log/vinfast-copilot.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
```

### Health Check

```python
@app.get("/health")
def health_check():
    try:
        llm = get_llm()
        return {"status": "healthy", "model": LLM_MODEL}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}
```

---

## Cost Estimates

| Option          | Setup Cost     | Monthly         | Best For        |
| --------------- | -------------- | --------------- | --------------- |
| Ollama Local    | $0             | $0              | Dev, Testing    |
| Gemini Free     | $0             | $0 (limited)    | Demo            |
| Gemini Paid     | $0             | ~$20-100        | Production      |
| AWS t3.micro    | $0 (free tier) | ~$8-20          | Small scale     |
| Streamlit Cloud | $0             | Free/Paid tiers | Easy deployment |

---

## Scaling Strategy

### Phase 1: MVP (Gemini Free)

- Streamlit Cloud + Gemini Free Tier
- Test with real users
- Monitor usage

### Phase 2: Growth (Ollama or Gemini Paid)

- Deploy Ollama on dedicated server
- OR upgrade to Gemini paid
- Add caching/database

### Phase 3: Production

- Kubernetes deployment
- Multiple LLM instances
- Load balancing
- Full monitoring

---

## Troubleshooting Deployment

| Issue                     | Solution                                   |
| ------------------------- | ------------------------------------------ |
| Port 8501 in use          | `streamlit run main.py --server.port 8502` |
| API Key errors            | Check secrets in cloud platform            |
| Ollama connection timeout | Ensure Ollama service is running           |
| Memory issues             | Increase server RAM or use Gemini          |
| Slow responses            | Add caching, optimize prompts              |

---

## Security Checklist

- [ ] Never hardcode API keys (use .env/secrets)
- [ ] Use HTTPS in production
- [ ] Set proper firewall rules
- [ ] Monitor API usage for abuse
- [ ] Regular backups
- [ ] Update dependencies regularly
- [ ] Use environment variables for sensitive data
- [ ] Enable error logging without exposing sensitive info

---

## Support & Resources

- **Streamlit Docs**: https://docs.streamlit.io
- **LangChain Docs**: https://python.langchain.com
- **Ollama Docs**: https://ollama.ai
- **Google Gemini API**: https://ai.google.dev
- **OpenAI Docs**: https://platform.openai.com/docs
