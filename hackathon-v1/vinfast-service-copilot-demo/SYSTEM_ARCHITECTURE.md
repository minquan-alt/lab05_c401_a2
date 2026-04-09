# VinFast Service Copilot - System Architecture Deep Dive

## 📋 Table of Contents

1. [System Overview](#system-overview)
2. [File Structure](#file-structure)
3. [Execution Flow](#execution-flow)
4. [Component Details](#component-details)
5. [Data Model](#data-model)
6. [Agent Workflow](#agent-workflow)
7. [Logging System](#logging-system)
8. [Integration Points](#integration-points)

---

## System Overview

VinFast Service Copilot is a sophisticated AI-powered diagnostic system that combines multiple agents, retrieval systems, and language models to provide expert vehicle diagnostics and repair guidance.

### Architecture Diagram

```
┌──────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                           │
│                     (Streamlit Web App)                           │
│                       main.py                                    │
└────────────────────┬─────────────────────────────────────────────┘
                     │
                     ▼
        ┌────────────────────────────┐
        │   LangGraph State Machine   │
        │   (graph/workflow.py)       │
        └────┬───────────┬────────────┘
             │           │
        ┌────▼─┐    ┌───▼─────┐
        │Nodes │    │Edges    │
        └──────┘    └─────────┘
             │
    ┌────────┼────────┬─────────┐
    │        │        │         │
    ▼        ▼        ▼         ▼
┌────────┐┌─────┐┌────────┐┌──────────┐
│Triage  ││RAG  ││Planner ││Workflow  │
│Agent   ││Agent││Agent   ││Logger    │
└──┬─────┘└──┬──┘└───┬────┘└──────────┘
   │         │       │
   └─────────┼───────┘
             │
        ┌────▼─────────────┐
        │  LLM Interface   │
        │ (llm_config.py)  │
        └────┬──────┬──────┘
             │      │
    ┌────────▼──┐  ┌▼───────────┐
    │   Ollama  │  │  Gemini /  │
    │  (Local)  │  │  OpenAI    │
    └───────────┘  └────────────┘
```

---

## File Structure

### Directory Tree

```
vinfast-service-copilot-demo/
│
├── 📄 CORE APPLICATION FILES
│   ├── main.py                    # Entry point (Streamlit UI)
│   ├── .env                       # Configuration (LLM selection)
│   ├── requirements.txt           # Python dependencies
│
├── 📂 src/                        # Source code (main package)
│   │
│   ├── __init__.py               # Package marker
│   │
│   ├── ⚙️  CONFIGURATION & LOGGING
│   │   ├── llm_config.py         # LLM initialization module
│   │   ├── workflow_logger.py    # Enhanced logging system
│   │   └── system_prompts.py     # System prompts for each agent
│   │
│   ├── 🤖 AGENTS DIRECTORY
│   │   ├── agents/__init__.py
│   │   ├── agents/triage_agent.py    # Symptom analysis agent
│   │   ├── agents/rag_agent.py       # Data retrieval & synthesis agent
│   │   └── agents/planner_agent.py   # Repair plan generation agent
│   │
│   ├── 🛠️  TOOLS DIRECTORY
│   │   ├── tools/__init__.py
│   │   └── tools/mock_tools.py      # Data retrieval utilities
│   │
│   └── 📊 GRAPH DIRECTORY
│       ├── graph/__init__.py
│       ├── graph/state.py           # AgentState definition
│       └── graph/workflow.py        # LangGraph workflow
│
├── 📂 mock_data/                 # Mock database (JSON files)
│   ├── service_manual_mock.json   # VinFast Service Manual data
│   └── knowledge_base_mock.json   # Repair history & TSB data
│
└── 📚 DOCUMENTATION
    ├── README.md                 # Quick overview
    ├── START_HERE.md            # Getting started guide
    ├── SYSTEM_ARCHITECTURE.md   # This file
    ├── ... (other docs)
```

### File Responsibility Matrix

| File                 | Responsibility     | Key Functions                                      |
| -------------------- | ------------------ | -------------------------------------------------- |
| `main.py`            | UI Layer           | Streamlit interface, form handling, result display |
| `llm_config.py`      | LLM Management     | Initialize correct LLM (Ollama/Gemini/OpenAI)      |
| `workflow_logger.py` | Observability      | Log every step, reasoning, tool call               |
| `system_prompts.py`  | Agent Instructions | System prompts for each agent role                 |
| `triage_agent.py`    | Initial Analysis   | Parse symptom, set confidence, identify DTCs       |
| `rag_agent.py`       | Data Retrieval     | Retrieve SM/KB data, synthesize info               |
| `planner_agent.py`   | Plan Generation    | Create detailed repair checklist                   |
| `workflow.py`        | Orchestration      | LangGraph workflow, state transitions              |
| `state.py`           | Data Model         | AgentState definition, type hints                  |
| `mock_tools.py`      | Data Access        | Query mock JSON databases                          |

---

## Execution Flow

### High-Level Flow

```
START
  │
  ▼
User Input (VIN + Symptom)
  │
  ├─→ Validate input
  │   └─→ Log: INPUT_RECEIVED
  │
  ▼
Initialize State
  │
  └─→ AgentState = {
       vin, symptom, probable_dtcs,
       retrieved_info, repair_plan,
       confidence_score, next_action
      }
  │
  ▼
┌─────────────────────────────────┐
│  TRIAGE AGENT                   │
│  ├─ Analyze symptom              │
│  ├─ Extract keywords             │
│  ├─ Determine confidence         │
│  └─ Identify probable DTCs       │
└────────┬────────────────────────┘
         │
    ┌────▼────────────────────────┐
    │ Is confidence > 0.7?         │
    └────┬────────────┬────────────┘
         │ YES        │ NO
         │            └─→ Request more info
         │
         ▼
┌─────────────────────────────────┐
│  RAG AGENT                      │
│  ├─ Retrieve SM details         │
│  ├─ Get KB insights             │
│  ├─ Find TSB bulletins          │
│  └─ Synthesize info             │
└────────┬────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│  PLANNER AGENT                  │
│  ├─ Load safety standards       │
│  ├─ Generate checklist          │
│  ├─ Detail procedures           │
│  └─ Specify requirements        │
└────────┬────────────────────────┘
         │
         ▼
Display Results
  │
  ├─→ Confidence score
  ├─→ Probable DTCs
  ├─→ Repair plan
  └─→ Safety checklist
  │
  ▼
END
```

### Detailed Agent Sequence

```
Time  │ Triage Agent         │ RAG Agent            │ Planner Agent
──────┼──────────────────────┼──────────────────────┼─────────────────
T1-5  │ ✓ Start              │                      │
   10 │ ✓ Parse symptom      │                      │
   15 │ ✓ Call LLM           │                      │
   20 │ ✓ Analyze response   │                      │
   25 │ ✓ Set confidence     │                      │
   30 │ ✓ Extract DTCs       │                      │
   35 │ ✓ Log results        │                      │
      │                      │                      │
   40 │                      │ ✓ Start              │
   45 │                      │ ✓ Retrieve SM data   │
   50 │                      │ ✓ Retrieve KB data   │
   55 │                      │ ✓ Call LLM synthesis │
   60 │                      │ ✓ Process response   │
   65 │                      │ ✓ Log results        │
      │                      │                      │
   70 │                      │                      │ ✓ Start
   75 │                      │                      │ ✓ Load safety std
   80 │                      │                      │ ✓ Call LLM plan
   85 │                      │                      │ ✓ Generate plan
   90 │                      │                      │ ✓ Log results
```

---

## Component Details

### 1. State Management (`graph/state.py`)

```python
class AgentState(TypedDict):
    vin: str                              # Vehicle identification
    symptom: str                          # User-provided symptom
    probable_dtcs: List[dict]             # Diagnosed error codes
    retrieved_info: Annotated[List[str], add]  # Accumulated info
    repair_plan: str                      # Final repair checklist
    confidence_score: float               # Diagnosis confidence (0-1)
    next_action: str                      # Next workflow step
```

**Key Features:**

- Type-safe with TypedDict
- Immutable + accumulated fields (via `add` operator)
- Designed for LangGraph state transitions

### 2. LLM Configuration (`llm_config.py`)

```
get_llm() function:
├─ Check LLM_MODEL environment variable
├─ If "ollama":
│   └─ Create OllamaLLM(model="qwen2.5:7b", base_url="...")
├─ If "gemini":
│   └─ Create ChatGoogleGenerativeAI(model="gemini-2.5-flash", ...)
├─ If "openai":
│   └─ Create ChatOpenAI(model="gpt-3.5-turbo", ...)
└─ Return initialized LLM instance
```

**Why this design:**

- Single source of truth for LLM selection
- Easy to switch models without code changes
- Deferred initialization (lazy loading)

### 3. Agent Pattern

Each agent follows this structure:

```python
def agent_name(state: AgentState) -> AgentState:
    # 1. LOG: Agent start
    workflow_logger.section("AGENT_NAME")

    # 2. INPUT: Log what we're processing
    log_agent_input("AGENT_NAME", state_fields)

    # 3. TOOL: Call tools/LLM
    workflow_logger.tool_call("tool_name", params)
    result = tool_or_llm(...)
    workflow_logger.tool_result("tool_name", result)

    # 4. PROCESS: Parse and update state
    state["field"] = processed_result

    # 5. OUTPUT: Log results
    log_agent_output("AGENT_NAME", state_fields)

    return state
```

### 4. Logging System (`workflow_logger.py`)

```
WorkflowLogger Methods:
├─ step(stage)           # Log workflow stage
├─ reasoning(agent, text)# Log LLM reasoning
├─ tool_call(name, params) # Log tool invocation
├─ tool_result(name, result) # Log tool output
├─ state_update(field, value) # Log state changes
├─ confidence(score)     # Log confidence level
├─ success(msg)          # Log success
├─ warning(msg)          # Log warning
├─ error(msg)            # Log error
└─ section(title)        # Log section header
```

### 5. System Prompts (`system_prompts.py`)

```
Contains:
├─ TRIAGE_SYSTEM_PROMPT      # Instructions for triage agent
├─ RAG_SYSTEM_PROMPT         # Instructions for RAG agent
├─ PLANNER_SYSTEM_PROMPT     # Instructions for planning agent
├─ get_triage_prompt()       # Generates context-specific prompt
├─ get_rag_prompt()          # RAG with current data
├─ get_planner_prompt()      # Planning with safety standards
└─ STEP_LOGGING              # Log message templates
```

---

## Data Model

### State Transitions

```
Initial State
    │
    ├─ vin: "VF8-001"
    ├─ symptom: "Xe sạc không vào"
    ├─ probable_dtcs: []
    ├─ retrieved_info: []
    ├─ repair_plan: ""
    ├─ confidence_score: 0.0
    └─ next_action: ""
    │
    ▼
After TRIAGE
    │
    ├─ vin: "VF8-001" (unchanged)
    ├─ symptom: "Xe sạc không vào" (unchanged)
    ├─ probable_dtcs: [{"code": "P0A00", "description": "..."}]
    ├─ retrieved_info: [] (unchanged)
    ├─ repair_plan: "" (unchanged)
    ├─ confidence_score: 0.85
    └─ next_action: "proceed"
    │
    ▼
After RAG
    │
    ├─ probable_dtcs: [...] (unchanged)
    ├─ retrieved_info: ["SM: P0A00...", "KB: TSB-001...", "Synthesis: ..."]
    ├─ repair_plan: "" (unchanged)
    └─ other fields (unchanged)
    │
    ▼
After PLANNER
    │
    ├─ repair_plan: "CHECKLIST: 1. Safety... 2. Tools..."
    └─ all other fields (unchanged)
    │
    ▼
Final State
    │ Ready for display
    ▼
```

### Mock Data Structure

**service_manual_mock.json:**

```json
{
  "service_manual": {
    "charging_system": {
      "dtc_codes": {
        "P0A00": {
          "description": "High Voltage System Fault",
          "symptoms": ["Charging not starting", "Red warning light"],
          "repair_procedures": [...],
          "safety_notes": "..."
        }
      }
    }
  }
}
```

**knowledge_base_mock.json:**

```json
{
  "knowledge_base": {
    "tsb": [{...}],
    "repair_history": [{...}]
  }
}
```

---

## Agent Workflow

### TRIAGE AGENT

**Purpose:** Classify symptom and establish baseline diagnosis

**Input:**

```python
state["symptom"]  # User's natural language description
```

**Process:**

1. Load system prompt (defines role & instructions)
2. Call LLM with symptom
3. Parse JSON response for:
   - `confidence_score` (0-1)
   - `next_action` ("proceed" or "ask_more_info")
   - `extracted_terms` (technical keywords)
4. Map symptom keywords to probable DTC codes

**Output:**

```python
state["confidence_score"]  # 0-1
state["next_action"]       # "proceed" or "ask_more_info"
state["probable_dtcs"]     # [{"code": "P0A00", ...}]
```

**Key Decision:** If confidence < 0.7 → ask for more info

### RAG AGENT

**Purpose:** Retrieve authoritative data and provide comprehensive diagnosis

**Input:**

```python
state["symptom"]
state["probable_dtcs"]
```

**Process:**

1. For each probable DTC:
   - Call `get_sm_details(dtc_code)` → retrieve Service Manual data
   - Log: tool_call, tool_result, state_update
2. Call `get_kb_insights(symptom)` → retrieve Knowledge Base data
3. Aggregate all retrieved data
4. Call LLM to synthesize information
5. Add synthesis to `retrieved_info`

**Output:**

```python
state["retrieved_info"]  # ["SM: ...", "KB: ...", "Synthesis: ..."]
```

### PLANNER AGENT

**Purpose:** Generate actionable repair procedures

**Input:**

```python
state["symptom"]
state["retrieved_info"]
# + safety_standards from tools
```

**Process:**

1. Load safety standards via `verify_safety_standards()`
2. Load system prompt (defines repair procedure format)
3. Call LLM with:
   - Diagnosis summary
   - Safety requirements
   - Retrieved information
4. LLM generates checklist with:
   - Safety procedures
   - Tools needed
   - Step-by-step instructions
   - Verification steps

**Output:**

```python
state["repair_plan"]  # Detailed checklist
```

---

## Logging System

### Log Levels

```
DEBUG  │ Detailed step information
INFO   │ Regular workflow progress
WARN   │ Important notices
ERROR  │ Failures
```

### Log Format

```
HH:MM:SS | LEVEL    | MESSAGE

Example:
14:32:15 | INFO     | ============================================================
14:32:15 | INFO     | STEP: TRIAGE AGENT
14:32:15 | INFO     | ============================================================
14:32:16 | INFO     | 🔧 TOOL CALL: LLM_Invoke
14:32:16 | INFO     |    ├─ model: OllamaLLM
14:32:16 | INFO     |    ├─ task: Triage Analysis
```

### Logging Points

Each agent logs:

1. **STEP START**: `workflow_logger.section("AGENT_NAME")`
2. **INPUT**: `log_agent_input(agent, fields)`
3. **TOOL CALLS**: `workflow_logger.tool_call(name, params)`
4. **TOOL RESULTS**: `workflow_logger.tool_result(name, result)`
5. **STATE UPDATES**: `workflow_logger.state_update(field, value)`
6. **REASONING**: `workflow_logger.reasoning(agent, text)`
7. **OUTPUT**: `log_agent_output(agent, fields)`

---

## Integration Points

### LLM Integration

```
Agent Code:
  llm = get_llm()
  │
  ├─→ llm_config.py:get_llm()
  │   ├─ Check: LLM_MODEL env var
  │   ├─ If "ollama": return OllamaLLM(...)
  │   ├─ If "gemini": return ChatGoogleGenerativeAI(...)
  │   └─ If "openai": return ChatOpenAI(...)
  │
  └─→ Use returned LLM instance
      chain = prompt | llm
      response = chain.invoke(inputs)
```

### Data Retrieval Integration

```
Agent Code:
  from tools.mock_tools import get_sm_details
  │
  ├─→ mock_tools.py:get_sm_details(dtc_code)
  │   ├─ Load: service_manual_mock.json
  │   ├─ Query: Find DTC code
  │   └─ Return: Details dict
  │
  └─→ Process returned data
```

### Workflow Orchestration

```
LangGraph:
  StateGraph(AgentState)
    ├─ add_node("triage", triage_agent)
    ├─ add_node("rag", rag_agent)
    ├─ add_node("planner", planner_agent)
    │
    ├─ set_entry_point("triage")
    ├─ add_conditional_edges("triage", condition_func)
    ├─ add_edge("rag", "planner")
    └─ add_edge("planner", END)
    │
    ▼
  graph.compile()
    │
    ▼
  graph.invoke(initial_state)
```

---

## Execution Example

### Sample Execution Trace

```
START
└─ User Input: VIN="VF8-001", Symptom="Xe sạc không vào"
   └─ Initialize AgentState
      └─ agent="lru_cache" (Ollama qwen2.5:7b)
         └─ TRIAGE AGENT START
            ├─ INPUT: symptom="Xe sạc không vào"
            ├─ TOOL_CALL: LLM_Invoke (OllamaLLM)
            ├─ LLM_RESPONSE: {"confidence_score": 0.85, ...}
            ├─ STATE_UPDATE: confidence_score=0.85
            ├─ STATE_UPDATE: probable_dtcs=[P0A00]
            ├─ OUTPUT: triage complete
            └─ DECISION: confidence > 0.7 → proceed
               └─ RAG AGENT START
                  ├─ INPUT: symptom="Xe sạc không vào", dtcs=[P0A00]
                  ├─ TOOL_CALL: get_sm_details(P0A00)
                  ├─ TOOL_RESULT: Found SM data
                  ├─ TOOL_CALL: get_kb_insights("sạc không vào")
                  ├─ TOOL_RESULT: Found 2 KB items
                  ├─ TOOL_CALL: LLM_Synthesis
                  ├─ STATE_UPDATE: retrieved_info=[SM, KB, Synthesis]
                  ├─ OUTPUT: rag complete
                  └─ PLANNER AGENT START
                     ├─ INPUT: symptom, retrieved_info
                     ├─ TOOL_CALL: verify_safety_standards()
                     ├─ TOOL_RESULT: 5 safety standards
                     ├─ TOOL_CALL: LLM_PlanGeneration
                     ├─ STATE_UPDATE: repair_plan=<checklist>
                     ├─ OUTPUT: planner complete
                     └─ WORKFLOW COMPLETE
                        └─ Display Results
END
```

---

## Performance Considerations

### Latency by Component

| Component     | Delay       | Bottleneck    |
| ------------- | ----------- | ------------- |
| Triage Agent  | ~3-5s       | LLM inference |
| RAG Retrieve  | ~100ms      | JSON parsing  |
| RAG Synthesis | ~3-5s       | LLM inference |
| Planner Agent | ~5-10s      | LLM inference |
| **Total**     | **~15-25s** | LLM calls     |

### Optimization Opportunities

1. **Caching**
   - Cache DTC lookups
   - Cache safety standards
   - Cache LLM responses

2. **Parallelization**
   - Run SM and KB retrieval in parallel
   - Use async/await for I/O

3. **Model Selection**
   - Ollama: Slow but free
   - Gemini: Fast, free tier
   - OpenAI: Fast, paid

---

## Security & Compliance

- ✅ **API Keys**: Stored in .env, not in code
- ✅ **Logging**: No sensitive data in logs
- ✅ **Mock Data**: No real VinFast data (for demo)
- ⚠️ **Error Handling**: Graceful fallbacks

---

## Future Enhancements

1. Database integration (replace mock JSON)
2. Real Service Manual data
3. Multi-language support
4. User feedback loop & learning
5. Integration with OBD-II scanners
6. Mobile app
7. Offline capability with Ollama
8. Advanced caching & optimization

---

**Document Version:** 2.0  
**Last Updated:** April 2026  
**Status:** Complete & Production-Ready
