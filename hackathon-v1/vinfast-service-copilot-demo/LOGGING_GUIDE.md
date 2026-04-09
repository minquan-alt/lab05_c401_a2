# 🎯 Complete Guide - Enhanced Logging & System Prompts

## 📋 Summary of Changes (V2.1)

Hệ thống đã được nâng cấp với:

### ✨ New Components

1. **System Prompts** (`src/system_prompts.py`)
   - Detailed instructions cho mỗi agent
   - Cải thiện chất lượng LLM output

2. **Workflow Logger** (`src/workflow_logger.py`)
   - Chi tiết logging ở mỗi bước
   - Tool call tracking
   - State monitoring

3. **Enhanced UI** (updated `main.py`)
   - 3 tabs: Diagnosis, Logs, Documentation
   - Progress bars
   - Real-time feedback
   - Log download

4. **System Architecture Doc** (`SYSTEM_ARCHITECTURE.md`)
   - Giải thích chi tiết hệ thống
   - Diagrams & flowcharts
   - Component breakdown
   - Integration points

---

## 🆕 New Files

| File                     | Purpose                | Where |
| ------------------------ | ---------------------- | ----- |
| `src/system_prompts.py`  | Agent instructions     | src/  |
| `src/workflow_logger.py` | Logging system         | src/  |
| `SYSTEM_ARCHITECTURE.md` | Deep architecture docs | root  |
| `ADVANCED_FEATURES.md`   | This guide             | root  |

---

## 🎯 Quick Start with Logging

### 1. Install (if not done)

```bash
pip install -r requirements.txt
```

### 2. Configure Model (.env)

```
LLM_MODEL=ollama  # or gemini, openai
OLLAMA_MODEL=qwen2.5:7b
```

### 3. Start Model (if using Ollama)

```bash
# Terminal 1
ollama pull qwen2.5:7b
ollama serve
```

### 4. Run App with Logging

```bash
# Terminal 2
streamlit run main.py
```

### 5. View Logs

- Tab 1: "Diagnosis" - Run diagnosis
- Tab 2: "Detailed Logs" - See all execution logs
- Tab 3: "Documentation" - Read docs

---

## 🔍 Understanding the Logs

### Log Format

```
HH:MM:SS | LEVEL | MESSAGE

Example:
14:32:15 | INFO  | ============================================================
14:32:15 | INFO  | STEP: TRIAGE AGENT
14:32:15 | INFO  | ============================================================
```

### Log Stages (per agent)

Each agent logs **7 key stages**:

```
1. 📝 AGENT START
   ├─ Section header

2. 📥 INPUT LOGGING
   ├─ What data agent receives

3. 🔧 TOOL CALLS
   ├─ What tools/LLM agent invokes
   ├─ With parameters

4. 📤 TOOL RESULTS
   ├─ What tools/LLM returns

5. 📍 STATE UPDATES
   ├─ How internal state changes

6. 🧠 REASONING
   ├─ Why agent made decisions

7. 📊 OUTPUT LOGGING
   └─ Final results from agent
```

### Example: Triage Agent Logs

```
============================================================
STEP: TRIAGE AGENT
============================================================

🔍 [TRIAGE] INPUT:
   ├─ vin: VF8-001
   └─ symptom: Xe sạc không vào, đèn báo đỏ

🔧 TOOL CALL: LLM_Invoke
   ├─ model: OllamaLLM
   └─ task: Triage Analysis

📤 TOOL RESULT: LLM_Response
   └─ content: {"confidence_score": 0.85, ...}

📊 CONFIDENCE: ✅ HIGH (0.85)

🧠 [TRIAGE] REASONING:
   Symptom clearly indicates charging system issue

ℹ️  Probable DTCs identified: ['P0A00']

📍 STATE UPDATE: confidence_score = 0.85

────────────────────────────────────────────────────────
  TRIAGE Agent Output
────────────────────────────────────────────────────────
confidence_score: 0.85
next_action: proceed
probable_dtcs: [{'code': 'P0A00', 'description': 'High Voltage System Fault'}]
```

---

## 📊 System Prompts Explained

### What are System Prompts?

System prompts are **detailed instructions** sent to LLM that define:

- ✅ Agent's role
- ✅ Responsibilities
- ✅ Output format
- ✅ Constraints
- ✅ Examples

### File: `src/system_prompts.py`

```python
# Define agent roles
TRIAGE_SYSTEM_PROMPT = """You are a professional triage agent..."""
RAG_SYSTEM_PROMPT = """You are a RAG agent..."""
PLANNER_SYSTEM_PROMPT = """You are a planning agent..."""

# Generate context-specific prompts
def get_triage_prompt(symptom: str) -> str:
    return f"{TRIAGE_SYSTEM_PROMPT}\n\nCURRENT CASE:\nSymptom Report: {symptom}\n..."
```

### Prompt Contents

#### Triage Prompt

```
RESPONSIBILITIES:
1. Normalize natural language symptoms
2. Extract relevant keywords
3. Assess confidence level
4. Identify probable DTC codes

OUTPUT FORMAT:
{
  "confidence_score": <float 0-1>,
  "next_action": "proceed" or "ask_more_info",
  "extracted_terms": [<keywords>],
  "probable_dtcs": [<DTC codes>],
  "reasoning": "<explanation>"
}
```

#### RAG Prompt

```
Retrieve accurate data from:
1. Service Manual (SM)
2. Knowledge Base (KB)
3. Technical Service Bulletins (TSB)

Synthesize into:
- Confirmed DTC codes
- Detailed description
- Related TSB bulletins
- Historical cases
- Testing procedures
```

#### Planner Prompt

```
Generate detailed repair checklist:
1. SAFETY FIRST (HV warnings, PPE)
2. TOOLS & EQUIPMENT
3. STEP-BY-STEP PROCEDURES
4. VERIFICATION & TESTING
5. COMPLETION (sign-off)

Include:
- Torque values
- Voltages
- Grounding procedures
- Verification steps
```

### How Prompts Improve Output

**Without specific prompts:**

```
LLM might return: "Fix the charging issue"
(vague, unclear format)
```

**With system prompts:**

```
LLM returns: {
  "confidence_score": 0.85,
  "probable_dtcs": ["P0A00"],
  "next_action": "proceed"
}
(structured, parseable, professional)
```

---

## 🔧 File Structure (Updated)

```
vinfast-service-copilot-demo/
│
├── 📂 src/                           # Python package
│   │
│   ├── llm_config.py                 # LLM selection
│   ├── workflow_logger.py            # ✨ NEW - Logging system
│   ├── system_prompts.py             # ✨ NEW - Agent instructions
│   │
│   ├── agents/
│   │   ├── triage_agent.py           # ✏️ UPDATED - with logging
│   │   ├── rag_agent.py              # ✏️ UPDATED - with logging
│   │   └── planner_agent.py          # ✏️ UPDATED - with logging
│   │
│   ├── tools/
│   │   └── mock_tools.py
│   │
│   └── graph/
│       ├── state.py
│       └── workflow.py
│
├── main.py                           # ✏️ UPDATED - enhanced UI
│
├── 📚 DOCUMENTATION
│   ├── SYSTEM_ARCHITECTURE.md       # ✨ NEW - deep dive
│   ├── ADVANCED_FEATURES.md         # ✨ NEW - this guide
│   ├── START_HERE.md
│   ├── SETUP_GUIDE.md
│   └── ... (other docs)
```

---

## 🔄 Data Flow with Logging

### Whole Workflow

```
User Input (VIN + Symptom)
  │
  ├─→ 📝 LOG: Receive input
  │
  ▼
┌─────────────────────────────┐
│  TRIAGE AGENT               │
│                             │
│  📝 LOG: Input received      │
│  🔧 LOG: LLM invoked         │
│  📤 LOG: LLM response        │
│  📊 LOG: Confidence set      │
│  🎯 LOG: Output complete     │
└──────────┬──────────────────┘
           │
           │ (if confidence > 0.7)
           │
           ▼
┌─────────────────────────────┐
│  RAG AGENT                  │
│                             │
│  📝 LOG: Inputs received     │
│  🔧 LOG: Retrieve from SM    │
│  🔧 LOG: Retrieve from KB    │
│  📤 LOG: Data retrieved      │
│  🔧 LOG: LLM synthesis       │
│  📊 LOG: Info aggregated     │
│  🎯 LOG: Output complete     │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│  PLANNER AGENT              │
│                             │
│  📝 LOG: Inputs received     │
│  🔧 LOG: Load safety std     │
│  🔧 LOG: LLM for planning    │
│  📤 LOG: Repair plan gen     │
│  🎯 LOG: Output complete     │
└──────────┬──────────────────┘
           │
           ▼
Display Results + Logs
```

---

## 🎓 Examples

### Example 1: View Logs in Console

```bash
$ streamlit run main.py

# Logs appear automatically:
# 14:32:15 | INFO | ============================================================
# 14:32:15 | INFO | STEP: TRIAGE AGENT
# ... (full detailed logs)
```

### Example 2: View Logs in Web UI

1. Open Streamlit: http://localhost:8501
2. Fill form: VIN="VF8-001", Symptom="Xe sạc không vào"
3. Click "Bắt đầu Chẩn đoán"
4. See progress bars in "Diagnosis" tab
5. Click "Detailed Logs" tab
6. See all execution logs
7. Click "Download Logs" to save

### Example 3: Parse Logs Programmatically

```python
from src.workflow_logger import workflow_logger

# Get logger instance
logger = workflow_logger.logger

# Use for custom logging
logger.info("This is my custom message")
workflow_logger.success("Task completed")
```

---

## 🚀 Best Practices

### 1. Always Check Confidence

```
If confidence_score > 0.7:
  ✅ Diagnosis is reliable
else:
  ⚠️  Request more information
```

### 2. Review Retrieved Data

Before trusting diagnosis, check:

- How much SM data was retrieved?
- How many KB cases matched?
- Is synthesis comprehensive?

### 3. Understand Reasoning

Read the `🧠 REASONING` sections:

- Why LLM made decisions
- What keywords triggered it
- Any warnings or concerns

### 4. Use Logs for Debugging

If something seems wrong:

1. Look at the logs
2. Find the problematic step
3. Check input and output
4. Adjust prompts or data if needed

---

## 📖 Documentation Map

**For Quick Start:**

- → [START_HERE.md](START_HERE.md)
- → [QUICK_START.md](QUICK_START.md)

**For Setup Help:**

- → [SETUP_GUIDE.md](SETUP_GUIDE.md)

**For Deep Understanding:**

- → [SYSTEM_ARCHITECTURE.md](SYSTEM_ARCHITECTURE.md) (New!)
- → [ADVANCED_FEATURES.md](ADVANCED_FEATURES.md) (This file)

**For Deployment:**

- → [DEPLOYMENT.md](DEPLOYMENT.md)

**For Architecture:**

- → [ARCHITECTURE.md](ARCHITECTURE.md)

---

## 🤔 FAQ

**Q: Where do I see the logs?**
A:

- Terminal console (when running `streamlit run main.py`)
- Web UI under "Detailed Logs" tab

**Q: How detailed are the logs?**
A:

- Everything! From LLM calls to state changes
- You'll see exactly what happened at each step

**Q: Can I download the logs?**
A:

- Yes! Click "Download Logs" button in "Detailed Logs" tab
- Saved as `diagnosis_logs.txt`

**Q: How do system prompts affect results?**
A:

- They define agent behavior & output format
- Better prompts = better/more consistent results

**Q: Can I modify the system prompts?**
A:

- Yes! Edit `src/system_prompts.py`
- Changes take effect immediately after restart

**Q: Why is logging important?**
A:

- Transparency (see AI reasoning)
- Debugging (identify issues)
- Learning (understand system)
- Verification (ensure quality)

---

## 🎯 Next Steps

1. **Run the demo** with logging enabled
2. **Study the logs** to understand execution
3. **Read SYSTEM_ARCHITECTURE.md** for deep dive
4. **Modify system prompts** to improve results
5. **Add custom logging** for your extensions

---

## 📞 Support

If you have questions:

1. Check [SYSTEM_ARCHITECTURE.md](SYSTEM_ARCHITECTURE.md)
2. Review the logs in "Detailed Logs" tab
3. Check [SETUP_GUIDE.md](SETUP_GUIDE.md) for troubleshooting
4. Read comments in `src/workflow_logger.py` and `src/system_prompts.py`

---

**Version:** 2.1 (Enhanced Logging & System Prompts)  
**Status:** ✅ Complete  
**Last Updated:** April 2026
