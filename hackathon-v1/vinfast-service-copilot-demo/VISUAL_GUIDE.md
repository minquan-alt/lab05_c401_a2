# VinFast Service Copilot - Visual Guide

## 🎬 Demo Flow Diagram

```
┌──────────────────────────────────────────────────────────────┐
│  User Interface (Streamlit)                                  │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ Input Form:                                            │  │
│  │ • VIN: VF8-001                                         │  │
│  │ • Symptom: "Xe sạc không vào, đèn báo đỏ"             │  │
│  │ [Chẩn đoán Button]                                     │  │
│  └────────┬───────────────────────────────────────────────┘  │
└───────────┼──────────────────────────────────────────────────┘
            │
            ▼
┌──────────────────────────────────────────────────────────────┐
│  LLM Selection Layer (llm_config.py)                         │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ Check .env: LLM_MODEL = "ollama"                       │ │
│  │ Initialize: OllamaLLM(qwen2.5:7b)                      │ │
│  └────────────────┬──────────────────────────────────────┘ │
└───────────────────┼──────────────────────────────────────────┘
                    │
        ┌───────────┴──────────┬─────────────┐
        │                      │             │
        ▼                      ▼             ▼
    ┌────────┐             ┌────────┐   ┌────────┐
    │ Ollama │             │Gemini  │   │OpenAI  │
    │ Local  │             │ Free   │   │ Paid   │
    └───┬────┘             └───┬────┘   └───┬────┘
        │                      │             │
        └──────────┬───────────┴─────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────────────────────┐
│  Workflow Execution (LangGraph)                              │
│                                                              │
│  Step 1: TRIAGE AGENT                                       │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Input: "Xe sạc không vào, đèn báo đỏ"              │   │
│  │ Process: Analyze symptom, extract keywords           │   │
│  │ Output: probable_dtcs = [P0A00]                      │   │
│  │         confidence_score = 0.85                      │   │
│  └──────────────────────────────────────────────────────┘   │
│                          ▼                                    │
│  Step 2: RAG AGENT                                          │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Input: probable_dtcs, symptom                        │   │
│  │ Retrieve:                                            │   │
│  │  • SM: P0A00 details → High Voltage System Fault     │   │
│  │  • KB: Similar cases, TSB bulletins                  │   │
│  │ Output: retrieved_info = [SM data, KB insights]      │   │
│  └──────────────────────────────────────────────────────┘   │
│                          ▼                                    │
│  Step 3: PLANNER AGENT                                      │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Input: retrieved_info, safety standards              │   │
│  │ Generate:                                            │   │
│  │  • Tools needed: Multimeter, Insulated gloves        │   │
│  │  • Repair steps: 1. Disconnect HV... 2. Check...    │   │
│  │  • Safety notes: Never work live on HV               │   │
│  │ Output: repair_plan (detailed checklist)             │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
└──────────────┬───────────────────────────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────────────────────────┐
│  Display Results (Streamlit)                                 │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ ✅ Chẩn đoán hoàn thành!                              │  │
│  │                                                        │  │
│  │ Thông tin chẩn đoán:                                  │  │
│  │  • Điểm tin cậy: 0.85                                │  │
│  │  • Mã lỗi: P0A00 - High Voltage System Fault         │  │
│  │                                                        │  │
│  │ Kế hoạch sửa chữa:                                    │  │
│  │  1. Disconnect high voltage battery                  │  │
│  │  2. Check high voltage connections                   │  │
│  │  3. Inspect charging cable                           │  │
│  │  ...                                                  │  │
│  └────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
```

---

## 📊 Comparison Table

### Model Selection Visualization

```
        Local?  │  Speed  │ Quality │ Cost   │ Better for
─────────────────────────────────────────────────────────
Ollama   ✅     │   🟡    │   🟢    │   $0   │ Dev/Testing
Gemini   ❌     │   🟢    │   🟢    │   $0   │ Demo/Light
OpenAI   ❌     │   🟢    │   🟢    │   $$   │ Production

Legend:
  ✅ = Yes   ❌ = No
  🟡 = Medium   🟢 = Good/Fast
```

---

## 🔄 State Flow

```
Initial State:
{
  "vin": "VF8-001",
  "symptom": "Xe sạc không vào, đèn báo đỏ",
  "probable_dtcs": [],
  "retrieved_info": [],
  "repair_plan": "",
  "confidence_score": 0.0,
  "next_action": ""
}
        │
        │ After Triage Agent
        ▼
{
  ...
  "probable_dtcs": [{"code": "P0A00", "description": "High Voltage System Fault"}],
  "confidence_score": 0.85,
  "next_action": "proceed"
}
        │
        │ After RAG Agent
        ▼
{
  ...
  "retrieved_info": [
    "SM: P0A00 - High Voltage System Fault - Check connections...",
    "KB: TSB-001 - Similar issue reported, solution: Update firmware...",
    "Synthesis: Most likely is connector issue, secondary is firmware..."
  ]
}
        │
        │ After Planner Agent
        ▼
{
  ...
  "repair_plan": "REPAIR CHECKLIST:\n1. Safety First...\n2. Tools Needed...\n3. Steps..."
}
```

---

## 💡 Configuration Decision Tree

```
                How do you want to run?
                        │
        ┌───────────────┼───────────────┐
        │               │               │
    On my PC        On a server      Streamlit Cloud
        │               │               │
        ▼               ▼               ▼
    OLLAMA          GEMINI/          GEMINI
                    OPENAI       (easiest setup!)
        │               │               │
        │               │               │
    Local only    Needs API Key    GitHub + Cloud
    4GB RAM       1GB RAM          0 local setup
    Setup: 5m     Setup: 2m        Setup: 1m
```

---

## 🧩 Component Interaction

```
┌─────────────────────────────────────────────────────────────────┐
│                       Main App (Streamlit)                       │
│                                                                  │
│  ┌──────────────────┐    ┌──────────────────┐                  │
│  │  User Interface  │◄───┤ Graph Workflow   │                  │
│  │  (Forms, Tables) │    │ (Agents execute) │                  │
│  └──────────────────┘    └────────┬─────────┘                  │
│                                   │                             │
│                    ┌──────────────┼──────────────┐              │
│                    │              │              │              │
│             ┌──────▼────┐  ┌──────▼────┐  ┌────▼──────┐       │
│             │LLM Config │  │  Agents   │  │Mock Data  │       │
│             │ (Dynamic) │  │(Triage...)│  │(SM, KB)   │       │
│             └────┬──────┘  └───────────┘  └───────────┘       │
│                  │                                             │
│          ┌───────┴─────────┐                                   │
│          │                 │                                   │
│      ┌───▼──┐          ┌───▼──┐                               │
│      │Ollama│          │Gemini│  ◄─► (API)                   │
│      │(Local)          │(Cloud)                               │
│      └───────┘         └───────┘                              │
│                                                                │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🎯 Use Case Paths

### Path 1: Happy Path ✅

```
User Input: "Sạc không vào"
    │
    ▼
Triage: Confidence = 0.8 ✓ (Proceed)
    │
    ▼
RAG: Found P0A00 in SM ✓
    │
    ▼
Planner: Created repair checklist ✓
    │
    ▼
Display: Success page
```

### Path 2: Low Confidence ⚠️

```
User Input: "Xe có vấn đề"
    │
    ▼
Triage: Confidence = 0.3 ✗ (Need more info)
    │
    ▼
Request: "Bạn hãy describe kỹ và cụ thể hơn"
    │
    ▼
Loop back to Triage
```

### Path 3: Information Not Found ❌

```
Input: DTCs found
    │
    ▼
RAG: Search SM - Found nothing
    │
    ▼
RAG: Search KB - No related cases
    │
    ▼
Display: "Need technical support"
```

---

## 📈 Performance Metrics

```
                Ollama    Gemini    OpenAI
First Response  ~3s       ~1s       ~1s
Per request     ~1-2s     ~0.5s     ~0.5s
Throughput      Low       High      High
Cost/1000req    $0        $0-$5     $1-$5
```

---

## 🚀 Deployment Architecture

```
Development:
┌─────────────────┐
│  Your Machine   │
│  ┌───────────┐  │
│  │Ollama     │  │
│  │Streamlit  │  │
│  │main.py    │  │
│  └───────────┘  │
└─────────────────┘

Production:
┌───────────────────────────────────┐
│         Load Balancer             │
└───────────┬───────────────────────┘
            │
    ┌───────┴─────────┐
    │                 │
┌───▼────┐       ┌───▼────┐
│Instance1│       │Instance2│
│Streamlit│       │Streamlit│
│+ Gemini │       │+ Gemini │
└────────┘       └────────┘
    │                 │
    └────────┬────────┘
             │
         ┌───▼────┐
         │Database│
         │(Cache) │
         └────────┘
```

---

## 🔐 Security Flow

```
User Input
    │
    ▼
.env (API Keys)
    │
    └──▶ Protected (not in code)
    │
    └──▶ Only loaded at runtime
    │
    └──▶ Not logged or exported
    │
    ▼
LLM (Ollama local OR Gemini/OpenAI API)
    │
    ▼
Response (displayed to user)
```

---

## 📱 UI Layout

```
┌─────────────────────────────────────────────────────┐
│  VinFast Service Copilot - AI Chatbot Demo         │
│  Hệ thống chẩn đoán xe điện thông minh...          │
┌─────────────────────────────────────────────────────┐
│ 🤖 Model hiện tại: qwen2.5:7b (ollama)             │
└─────────────────────────────────────────────────────┘
│                                                     │
│ ┌─┌─ Mã xe (VIN) ─────────────────────────────────┐│
│ │ │[VF8-001____________________]                   ││
│ │ └─────────────────────────────────────────────────┤
│ │                                                   │
│ │ ┌─ Mô tả triệu chứng ───────────────────────────┐│
│ │ │ [Xe sạc không vào, đèn báo đỏ__________]      ││
│ │ │ [____________________________________]         ││
│ │ └────────────────────────────────────────────────┤
│ │                     [Chẩn đoán]               │
│ │                                                  │
│ └──────────────────────────────────────────────────┘
│
│ ┌─ Thông tin chẩn đoán ────────────────────────────┐
│ │ Điểm tin cậy: 0.85                              │
│ │ Mã lỗi dự đoán:                                 │
│ │ - P0A00: High Voltage System Fault              │
│ └─────────────────────────────────────────────────┘
│
│ ┌─ Kế hoạch sửa chữa ───────────────────────────────┐
│ │ REPAIR CHECKLIST:                               │
│ │ 1. Safety First: Disconnect HV battery          │
│ │ 2. Tools: Multimeter, Insulated gloves          │
│ │ 3. Steps:...                                    │
│ └─────────────────────────────────────────────────┘
└─────────────────────────────────────────────────────┘
```

Happy coding! 🚀
