# VinFast Service Copilot - LLM Integration Architecture

## System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   Streamlit Web UI                       │
│                  (main.py)                              │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│         LLM Configuration Layer                         │
│  src/llm_config.py - get_llm()                         │
└────┬──────────┬──────────┬─────────────────────────────┘
     │          │          │
     ▼          ▼          ▼
 ┌────────┐┌────────┐┌──────────┐
 │ Ollama ││Gemini  ││ OpenAI   │
 │  Local ││ Free   ││ Paid     │
 └────┬───┘└───┬────┘└────┬─────┘
      │        │          │
      ▼        ▼          ▼
┌─────────────────────────────────────┐
│    Agents Layer                     │
│  ├─ Triage Agent                   │
│  ├─ RAG Agent                      │
│  └─ Planner Agent                  │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│    Mock Data / Tools                │
│  ├─ service_manual_mock.json        │
│  ├─ knowledge_base_mock.json        │
│  └─ mock_tools.py                   │
└─────────────────────────────────────┘
```

## Environment Variables Configuration

### .env File Structure

```
# [REQUIRED] Choose one: ollama, gemini, openai
LLM_MODEL=ollama

# [IF using Ollama]
OLLAMA_MODEL=qwen2.5:7b
OLLAMA_BASE_URL=http://localhost:11434

# [IF using Gemini]
GOOGLE_API_KEY=ai_XXXXXXXXXXXX

# [IF using OpenAI]
OPENAI_API_KEY=sk-XXXXXXXXXXXX
```

## Workflow Data Flow

```
User Input (VIN + Symptom)
         │
         ▼
    Triage Agent ──► get_llm() ──┐
         │                        │
         ├──────────┬─────────────┤
         │          │             │
    Probable DTCs   Confidence    Config
         │          │             │
         ▼          ▼             ▼
    [Ollama/Gemini/OpenAI LLM]
         │
         ▼
    RAG Agent ──► Retrieve Data
         │        SM + KB
         ├──────────┐
         │          │
    Retrieved Info  Combined
         │          Knowledge
         ▼
    Planner Agent ──► Generate
         │            Repair Plan
         │
         ├─ Safety Checklist
         ├─ Repair Procedures
         ├─ Testing Steps
         │
         ▼
    Display Results
```

## Adding New LLM Support

To add a new LLM (e.g., Claude, LLaMA):

1. **Update .env**:

   ```
   LLM_MODEL=claude
   ANTHROPIC_API_KEY=...
   ```

2. **Update llm_config.py**:

   ```python
   elif LLM_MODEL == "claude":
       from langchain_anthropic import ChatAnthropic
       return ChatAnthropic(
           model="claude-3-sonnet",
           api_key=os.getenv("ANTHROPIC_API_KEY"),
           temperature=0.1
       )
   ```

3. **Update agents** (they already use get_llm(), no changes needed!)

## Model Characteristics

### Ollama (qwen2.5:7b)

- **Type**: Local LLM
- **Size**: 7B parameters
- **Speed**: Medium (depends on PC)
- **Quality**: Good for diagnostic tasks
- **Cost**: Free
- **Use case**: Development, privacy-critical

### Google Gemini

- **Type**: Cloud API
- **Model**: gemini-2.5-flash
- **Speed**: Very Fast
- **Quality**: Excellent
- **Cost**: Free tier available
- **Use case**: Demos, prototyping

### OpenAI (GPT-3.5)

- **Type**: Cloud API
- **Model**: gpt-3.5-turbo
- **Speed**: Very Fast
- **Quality**: Excellent
- **Cost**: Pay-per-token
- **Use case**: Production systems

## Files Modified for Multi-LLM Support

```
src/
├── llm_config.py          [NEW] - LLM factory
├── agents/
│   ├── triage_agent.py    [UPDATED] - uses get_llm()
│   ├── rag_agent.py       [UPDATED] - uses get_llm()
│   └── planner_agent.py   [UPDATED] - uses get_llm()
├── main.py                [UPDATED] - shows model info
└── ...

.env                        [UPDATED] - multi-model config
requirements.txt           [UPDATED] - new dependencies
README.md                  [UPDATED] - setup instructions
SETUP_GUIDE.md            [NEW] - detailed guide
QUICK_START.md            [NEW] - quick start
```

## Switching Models at Runtime

The system automatically selects the correct LLM based on `.env` configuration. No code changes needed!

```bash
# Just change .env
LLM_MODEL=gemini

# Restart Streamlit
streamlit run main.py
```

Done! It will now use Gemini instead of Ollama.
