# 🎯 Advanced Features - Logging & System Prompts

## 📝 What's New in V2.1

[Lần nâng cấp này thêm]:

1. ✅ **Detailed Logging** - Xem log ở mỗi bước reasoning
2. ✅ **System Prompts** - Hướng dẫn LLM chính xác hơn
3. ✅ **Enhanced UI** - Tabs, progress bars, better visualization
4. ✅ **Deep Architecture Docs** - Giải thích chi tiết hệ thống

---

## 📊 New Files Created

### 1. `src/system_prompts.py`

Contains system prompts for each agent

**Includes:**

- `TRIAGE_SYSTEM_PROMPT` - Instructions for triage agent
- `RAG_SYSTEM_PROMPT` - Instructions for RAG agent
- `PLANNER_SYSTEM_PROMPT` - Instructions for planning agent
- Helper functions: `get_triage_prompt()`, `get_rag_prompt()`, `get_planner_prompt()`

**Example Usage:**

```python
from system_prompts import get_triage_prompt

prompt = get_triage_prompt(symptom)
# Returns: System prompt + user symptom
```

### 2. `src/workflow_logger.py`

Enhanced logging system with detailed output

**Key Classes:**

- `WorkflowLogger` - Main logging class with methods for:
  - `step()` - Log workflow stage
  - `reasoning()` - Log agent reasoning
  - `tool_call()` - Log tool invocation
  - `tool_result()` - Log tool output
  - `state_update()` - Log state changes
  - `confidence()` - Log confidence scores
  - `success()`, `warning()`, `error()` - Status logging

**Example Usage:**

```python
from workflow_logger import workflow_logger, log_agent_input

workflow_logger.section("TRIAGE AGENT")
log_agent_input("TRIAGE", {"symptom": "..."})
workflow_logger.tool_call("LLM_Invoke", {"model": "Ollama"})
workflow_logger.confidence(0.85)
```

### 3. `SYSTEM_ARCHITECTURE.md`

Comprehensive system architecture documentation

**Sections:**

- System Overview with diagrams
- File Structure & Responsibility Matrix
- Execution Flow (high-level & detailed)
- Component Details (State, LLM, Agents, Logging)
- Data Model & State Transitions
- Agent Workflow (Triage, RAG, Planner)
- Logging System details
- Integration Points
- Performance Analysis
- Security & Future Enhancements

---

## 🔍 Enhanced Execution Flow

### Before (Silent)

```
User Input
  ↓
[Processing...]
  ↓
Display Results
```

### After (Verbose)

```
User Input
  ↓
═══════════════════════════════════════
TRIAGE AGENT
═══════════════════════════════════════
  🔧 TOOL CALL: LLM_Invoke
  ├─ model: OllamaLLM
  └─ task: Triage Analysis

  📤 TOOL RESULT: LLM_Response
  ├─ content: {"confidence_score": 0.85...

  📊 CONFIDENCE: ✅ HIGH (0.85)
  🧠 REASONING: Symptom clearly indicates...

  ═══════════════════════════════════════
  RAG AGENT
  ═══════════════════════════════════════
  📚 Retrieving Service Manual Data
  🔧 TOOL CALL: get_sm_details
  ├─ dtc_code: P0A00

  📤 TOOL RESULT: get_sm_details
  └─ status: Found

  ... [more detailed logs]

Display Results
```

---

## 🎨 Enhanced UI (main.py)

### New Features:

1. **Sidebar Configuration**
   - Shows current LLM model
   - Quick test cases
   - Keyboard shortcuts

2. **3-Tab Layout**
   - 🔍 **Diagnosis** - Main diagnosis interface
   - 📊 **Detailed Logs** - View all execution logs
   - 📚 **Documentation** - Quick access to docs

3. **Progress Indicators**
   - Progress bar during execution
   - Status updates at each stage
   - Real-time feedback

4. **Better Result Display**
   - Metrics cards (Confidence, DTCs, Data)
   - Organized columns
   - Expandable sections
   - Download logs button

---

## 🧠 System Prompts Explained

### Why System Prompts Matter?

System prompts define **agent personality and behavior**:

**Triage Agent:**

```
You are a professional triage agent...
RESPONSIBILITIES:
1. Normalize natural language symptoms
2. Extract relevant keywords
3. Assess confidence level
...
OUTPUT FORMAT: Return JSON with confidence_score, next_action, etc.
```

This tells LLM:

- ✅ What role to play
- ✅ What to do
- ✅ How to format output
- ✅ What's expected

### How It Works?

```python
# Before (generic):
"Analyze this symptom and return JSON"

# After (specific):
"You are a professional triage agent...
Symptom: Xe sạc không vào
Analyze according to:
1. Normalize symptoms
2. Extract keywords
3. Assess confidence
Return JSON with {...}"
```

Better prompts = Better outputs!

---

## 📊 Logging Architecture

### Log Levels

```
┌─────────────────┬──────────────┐
│ Level    │ Usage               │
├──────────┼─────────────────────┤
│ DEBUG    │ Detailed step info   │
│ INFO     │ Regular progress     │
│ WARNING  │ Important notices    │
│ ERROR    │ Failures            │
└──────────┴─────────────────────┘
```

### Logging Points in Agents

Each agent logs **7 stages**:

```python
1. workflow_logger.section("AGENT_NAME")
   └─ Agent start marker

2. log_agent_input("AGENT_NAME", inputs)
   └─ What data agent receives

3. workflow_logger.tool_call("tool_name", params)
   └─ Tool being invoked

4. workflow_logger.tool_result("tool_name", result)
   └─ Tool response

5. workflow_logger.state_update("field", value)
   └─ State changes

6. workflow_logger.reasoning("agent", text)
   └─ Agent reasoning/thinking

7. log_agent_output("AGENT_NAME", outputs)
   └─ Agent final output
```

### Example Log Output

```
14:32:15 | INFO     | ============================================================
14:32:15 | INFO     | STEP: TRIAGE AGENT
14:32:15 | INFO     | ============================================================
14:32:15 | INFO     | 🔍 [TRIAGE] INPUT:
14:32:15 | INFO     |    ├─ vin: VF8-001
14:32:15 | INFO     |    └─ symptom: Xe sạc không vào
14:32:16 | INFO     | 🔧 TOOL CALL: LLM_Invoke
14:32:16 | INFO     |    ├─ model: OllamaLLM
14:32:16 | INFO     |    ├─ task: Triage Analysis
14:32:18 | INFO     | 📤 TOOL RESULT: LLM_Response
14:32:18 | INFO     |    ├─ content: {"confidence_score": 0.85...
14:32:18 | INFO     | 📊 CONFIDENCE: ✅ HIGH (0.85)
14:32:18 | INFO     | 🧠 [TRIAGE] REASONING:
14:32:18 | INFO     |    Symptom clearly indicates charging system issue
14:32:18 | INFO     |    Probable DTC: P0A00 (High Voltage System Fault)
```

---

## 🔄 Data Flow with Logging

### Before Processing

```
State: {
  vin: "VF8-001",
  symptom: "Xe sạc không vào",
  probable_dtcs: [],
  retrieved_info: [],
  repair_plan: "",
  confidence_score: 0.0
}
```

### During Processing (with logs)

```
📝 LOG: INPUT - symptom received
🔧 LOG: TOOL_CALL - LLM invoked
📤 LOG: TOOL_RESULT - confidence=0.85
📍 LOG: STATE_UPDATE - probable_dtcs=[P0A00]
```

### After Processing

```
State: {
  vin: "VF8-001",
  symptom: "Xe sạc không vào",
  probable_dtcs: [{"code": "P0A00", ...}],
  retrieved_info: ["SM: P0A00...", "KB: ..."],
  repair_plan: "CHECKLIST: 1. Safety... 2. Tools...",
  confidence_score: 0.85
}
```

---

## 🎯 How to Use Logging

### View Logs in Terminal

```bash
streamlit run main.py
# Logs appear in terminal console
```

### View Logs in UI

1. Run diagnosis in "Diagnosis" tab
2. Switch to "Detailed Logs" tab
3. See all execution logs
4. Click "Download Logs" to save

### Use Logs for Debugging

```
1. Run diagnosis
2. Check "Detailed Logs" tab
3. Look for errors/warnings
4. Identify problematic steps
5. Debug accordingly
```

---

## 📖 Architecture Documentation

### What's in SYSTEM_ARCHITECTURE.md?

1. **System Overview** - Big picture explanation
2. **File Structure** - What each file does
3. **Execution Flow** - How code runs
4. **Component Details** - Deep dive into pieces
5. **Data Model** - State & transitions
6. **Agent Workflow** - What each agent does
7. **Logging System** - How logging works
8. **Integration Points** - How parts connect
9. **Performance** - Timing & optimization
10. **Diagrams** - Visual representations

### Key Diagrams Included

```
✅ Architecture Diagram
✅ Execution Flow Chart
✅ Agent Sequence Diagram
✅ State Transition Diagram
✅ Data Flow Diagram
✅ Integration Points
```

---

## 🚀 How to Run with Full Logging

### Step 1: Prepare Environment

```bash
cd vinfast-service-copilot-demo
pip install -r requirements.txt
```

### Step 2: Start Ollama (or use Gemini)

```bash
# Terminal 1: Start Ollama
ollama pull qwen2.5:7b
ollama serve
```

### Step 3: Run Streamlit App

```bash
# Terminal 2: Run app
streamlit run main.py
```

### Step 4: Use App with Logging

1. **Diagnosis Tab**: Enter VIN and symptom
2. **Click "Bắt đầu Chẩn đoán"**
3. **See progress** with status updates
4. **Switch to "Detailed Logs" tab**
5. **View complete execution trace**
6. **Download logs if needed**

---

## 🎓 Example: Understanding Logs

### Scenario: Diagnose Charging Issue

**Input:**

```
VIN: VF8-001
Symptom: "Xe sạc không vào, đèn báo đỏ"
```

**Terminal Output (Logs):**

```
14:32:15 | INFO | ============================================================
14:32:15 | INFO | STEP: TRIAGE AGENT
14:32:15 | INFO | ============================================================
14:32:15 | INFO | 🔍 [TRIAGE] INPUT:
14:32:15 | INFO |    ├─ vin: VF8-001
14:32:15 | INFO |    └─ symptom: Xe sạc không vào, đèn báo đỏ
14:32:16 | INFO | 🔧 TOOL CALL: LLM_Invoke
14:32:16 | INFO |    ├─ model: OllamaLLM
14:32:16 | INFO |    ├─ task: Triage Analysis
14:32:20 | INFO | 📤 TOOL RESULT: LLM_Response
14:32:20 | INFO |    ├─ content: {"confidence_score": 0.92, "next_action": "proceed"...}
14:32:20 | INFO | 📊 CONFIDENCE: ✅ HIGH (0.92)
14:32:20 | INFO | ℹ️  Probable DTCs identified: ['P0A00']
14:32:20 | INFO | ────────────────────────────────────────────────────────
14:32:20 | INFO |   RAG AGENT INPUT
14:32:20 | INFO | ────────────────────────────────────────────────────────
14:32:20 | INFO | symptom: Xe sạc không vào, đèn báo đỏ
14:32:20 | INFO | probable_dtcs: [{'code': 'P0A00', 'description': 'High Voltage System Fault'}]
14:32:21 | INFO | 📚 Retrieving Service Manual Data
14:32:21 | INFO | 🔧 TOOL CALL: get_sm_details
14:32:21 | INFO |    ├─ dtc_code: P0A00
14:32:21 | INFO | 📤 TOOL RESULT: get_sm_details
14:32:21 | INFO |    ├─ status: Found
14:32:21 | INFO |    ├─ dtc: P0A00
14:32:21 | INFO | 📍 STATE UPDATE: SM Data for P0A00 = High Voltage System...
14:32:21 | INFO | 📚 Retrieving Knowledge Base Data
14:32:21 | INFO | 🔧 TOOL CALL: get_kb_insights
14:32:21 | INFO |    ├─ symptom: Xe sạc không vào, đèn báo đỏ
14:32:21 | INFO | 📤 TOOL RESULT: get_kb_insights
14:32:21 | INFO |    ├─ count: 2
14:32:21 | INFO | 📊 Data Summary:
14:32:21 | INFO |    Service Manual entries: 1
14:32:21 | INFO |    Knowledge Base entries: 2
14:32:24 | INFO | 🔧 TOOL CALL: LLM_Synthesis
14:32:24 | INFO |    ├─ model: OllamaLLM
14:32:24 | INFO |    ├─ retrieved_items: 3
14:32:28 | INFO | 🧠 [RAG] REASONING: Based on the retrieved information...
14:32:28 | INFO | ✅ SUCCESS: Repair plan generated successfully
```

**What This Tells Us:**

- ✅ Triage completed successfully
- ✅ High confidence (0.92)
- ✅ Identified P0A00 DTC
- ✅ Retrieved 1 SM entry + 2 KB entries
- ✅ LLM synthesized data correctly
- ✅ Ready for planner phase

---

## 💡 Benefits of Enhanced Logging

1. **Debugging** - Identify exactly where things go wrong
2. **Learning** - Understand how AI agents work
3. **Transparency** - See what LLM receives & produces
4. **Optimization** - Identify slow components
5. **Quality** - Verify AI reasoning is sound
6. **Documentation** - Automatic audit trail
7. **Training** - Learn from real executions

---

## 📚 Next Steps

1. **Read SYSTEM_ARCHITECTURE.md** - Full system explanation
2. **Run demo with logging** - See real-time logs
3. **Study log patterns** - Understand execution flow
4. **Try different symptoms** - See how logs vary
5. **Modify prompts** - Improve AI responses
6. **Add custom tools** - Extend functionality

---

**Version:** 2.1  
**Date:** April 2026  
**Status:** ✅ Complete with Enhanced Logging & Documentation
