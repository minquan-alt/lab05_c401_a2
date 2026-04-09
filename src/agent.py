from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from tools_mapping import TOOLS, TOOL_MAP
from dotenv import load_dotenv
import os
import json
import re
from pathlib import Path

load_dotenv()

# 1. Đọc System Prompt
SYSTEM_PROMPT_FILE = Path(__file__).resolve().parent / "system_prompt.txt"
with open(SYSTEM_PROMPT_FILE, "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()

# 2. Khai báo State
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]

# 3. Khởi tạo LLM và Tools
tools_list = TOOLS

def _normalize_openai_base_url(url: str | None) -> str:
    """Normalize Ollama base URL for OpenAI-compatible endpoints."""
    if not url:
        return "http://127.0.0.1:11434/v1"
    normalized = url.rstrip("/")
    return normalized if normalized.endswith("/v1") else f"{normalized}/v1"


base_url = _normalize_openai_base_url(os.getenv("OLLAMA_BASE_URL"))
api_key = os.getenv("OLLAMA_API_KEY", "ollama")
model_name = os.getenv("OLLAMA_MODEL", "qwen2.5-coder:7b")
llm = ChatOpenAI(
    base_url=base_url,
    api_key=api_key,
    model=model_name,
    temperature=0.1,
    max_tokens=1024
)
llm_with_tools = llm.bind_tools(tools_list)

# Map tên tool -> hàm thực thi
# (centralized in tools_mapping.py)

MAX_TOOL_ITERATIONS = 5  # Giới hạn số lần gọi tool liên tiếp, tránh loop vô hạn
MAX_HISTORY_PAIRS = 3


def _build_recent_context_messages(chat_history: list[tuple[str, str]], user_text: str) -> list[tuple[str, str]]:
    """
    Keep the latest N user-assistant pairs as context and append current user input.
    """
    recent = chat_history[-(MAX_HISTORY_PAIRS * 2):]
    return recent + [("human", user_text)]


def _latest_user_text(messages: list) -> str:
    for m in reversed(messages):
        if isinstance(m, HumanMessage):
            return str(m.content)
        if isinstance(m, tuple) and len(m) >= 2 and str(m[0]).lower() in {"human", "user"}:
            return str(m[1])
    return ""


def _is_smalltalk(text: str) -> bool:
    normalized = text.strip().lower()
    words = normalized.split()
    if len(words) > 5:
        return False
    return normalized in {
        "chào",
        "chao",
        "hello",
        "hi",
        "xin chào",
        "alo",
    }


def _extract_vehicle_context_regex(user_text: str) -> dict:
    model_match = re.search(r"\b(VF\d+)\b", user_text, re.IGNORECASE)
    year_match = re.search(r"\b(20\d{2})\b", user_text)
    firmware_match = re.search(
        r"\b(?:firmware|fw)\b[^0-9v]{0,30}(?:v)?\s*([0-9]+(?:\.[0-9]+){1,3})\b",
        user_text,
        re.IGNORECASE,
    )

    model = model_match.group(1).upper() if model_match else None
    model_year = int(year_match.group(1)) if year_match else None
    firmware = f"v{firmware_match.group(1)}" if firmware_match else None

    cleaned = re.sub(r"\b(VF\d+)\b", "", user_text, flags=re.IGNORECASE)
    cleaned = re.sub(r"\b20\d{2}\b", "", cleaned)
    cleaned = re.sub(
        r"\b(?:firmware|fw)\b[^0-9v]{0,30}(?:v)?\s*[0-9]+(?:\.[0-9]+){1,3}\b",
        "",
        cleaned,
        flags=re.IGNORECASE,
    )
    cleaned = re.sub(r"\s+", " ", cleaned).strip(" ,.-")
    symptom = cleaned or user_text.strip()

    return {
        "model": model,
        "model_year": model_year,
        "firmware": firmware,
        "symptom": symptom,
    }


def _extract_vehicle_context_llm(user_text: str) -> dict | None:
    extraction_prompt = (
        "Trích xuất thông tin xe từ input người dùng và trả về JSON hợp lệ DUY NHẤT, không thêm text khác.\n"
        "Schema bắt buộc:\n"
        "{\n"
        '  "model": string|null,\n'
        '  "model_year": integer|null,\n'
        '  "firmware": string|null,\n'
        '  "symptom": string\n'
        "}\n"
        "Rules:\n"
        "- model ví dụ VF8, VF9.\n"
        "- model_year chỉ là năm 4 chữ số.\n"
        "- firmware chuẩn hóa dạng vX.Y.Z nếu có.\n"
        "- symptom là phần mô tả sự cố còn lại.\n"
        "- Nếu không chắc chắn thì để null (trừ symptom luôn là chuỗi).\n\n"
        f"User input: {user_text}"
    )

    response = llm.invoke([HumanMessage(content=extraction_prompt)])
    content = response.content if hasattr(response, "content") else str(response)
    if not isinstance(content, str):
        return None

    candidate = content.strip()
    fence_match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", candidate, re.DOTALL)
    if fence_match:
        candidate = fence_match.group(1).strip()

    json_match = re.search(r"\{.*\}", candidate, re.DOTALL)
    if json_match:
        candidate = json_match.group(0).strip()

    try:
        parsed = json.loads(candidate)
    except json.JSONDecodeError:
        return None

    if not isinstance(parsed, dict):
        return None

    model = parsed.get("model")
    model_year = parsed.get("model_year")
    firmware = parsed.get("firmware")
    symptom = parsed.get("symptom")

    if model is not None:
        model = str(model).upper().strip()
    if model_year is not None:
        try:
            model_year = int(model_year)
        except (TypeError, ValueError):
            model_year = None
    if firmware is not None:
        firmware = str(firmware).strip().lower()
        if firmware and not firmware.startswith("v"):
            firmware = f"v{firmware}"
    if not isinstance(symptom, str) or not symptom.strip():
        symptom = user_text.strip()

    return {
        "model": model or None,
        "model_year": model_year,
        "firmware": firmware or None,
        "symptom": symptom.strip(),
    }


def _extract_vehicle_context(user_text: str) -> dict:
    llm_ctx = _extract_vehicle_context_llm(user_text)
    if llm_ctx:
        print("[DEBUG] context extracted by LLM structured output.")
        return llm_ctx
    print("[DEBUG] LLM extraction failed, fallback to regex.")
    return _extract_vehicle_context_regex(user_text)


def _run_deterministic_pipeline(user_text: str) -> str:
    ctx = _extract_vehicle_context(user_text)
    print(f"[DEBUG] extracted_context: {ctx}")

    validate_result = TOOL_MAP["validate_input"].invoke(
        {
            "model": ctx["model"],
            "model_year": ctx["model_year"],
            "firmware": ctx["firmware"],
        }
    )
    print(f"[DEBUG] validate_input: {validate_result}")
    missing = validate_result.get("missing_fields", []) if not validate_result.get("valid", False) else []

    history_result = TOOL_MAP["get_repair_history"].invoke(
        {
            "symptom": ctx["symptom"],
            "model": ctx["model"],
            "model_year": ctx["model_year"],
            "firmware": ctx["firmware"],
        }
    )
    candidates = history_result.get("candidates", [])
    dtc_list = [c["dtc"] for c in candidates if c.get("dtc")]
    print(f"[DEBUG] get_repair_history: {history_result}")

    if not dtc_list:
        print("[DEBUG] repair_history không có DTC, fallback diagnostic theo context.")
    diagnostic_result = TOOL_MAP["get_diagnostic"].invoke(
        {
            "dtc_list": dtc_list,
            "model": ctx["model"],
            "model_year": ctx["model_year"],
            "firmware": ctx["firmware"],
        }
    )
    diagnostics = diagnostic_result.get("diagnostics", [])
    print(f"[DEBUG] get_diagnostic: {diagnostic_result}")

    confidence_result = TOOL_MAP["compute_confidence"].invoke(
        {
            "candidates": candidates,
            "diagnostics": diagnostics,
        }
    )
    print(f"[DEBUG] compute_confidence: {confidence_result}")

    warnings = []
    if missing:
        warnings.append(
            "Thiếu thông tin metadata: "
            + ", ".join(missing)
            + ". Candidate được suy ra theo chế độ nới lỏng điều kiện."
        )
    if not candidates:
        warnings.append("Không tìm thấy lịch sử sửa chữa khớp mạnh; candidate có thể dựa nhiều hơn vào diagnostic.")

    manual_result = {"documents": []}
    can_fetch_manual = (
        bool(ctx.get("model"))
        and ctx.get("model_year") is not None
        and bool(ctx.get("firmware"))
    )
    if confidence_result.get("decision") == "high" and confidence_result.get("selected_dtc") and can_fetch_manual:
        manual_result = TOOL_MAP["retrieve_manual"].invoke(
            {
                "query": f"{ctx['symptom']} {confidence_result['selected_dtc']}",
                "model": ctx["model"],
                "model_year": ctx["model_year"],
                "firmware": ctx["firmware"],
            }
        )
        print(f"[DEBUG] retrieve_manual: {manual_result}")
    elif confidence_result.get("decision") == "high" and confidence_result.get("selected_dtc") and not can_fetch_manual:
        print("[DEBUG] skip retrieve_manual: thiếu metadata để gọi manual.")

    synthesis_input = HumanMessage(
        content=(
            "Bạn PHẢI chỉ sử dụng dữ liệu tool dưới đây, không tự suy diễn thêm.\n\n"
            f"USER_INPUT: {user_text}\n"
            f"PARSED_CONTEXT: {json.dumps(ctx, ensure_ascii=False)}\n"
            f"VALIDATE_INPUT: {json.dumps(validate_result, ensure_ascii=False)}\n"
            f"REPAIR_HISTORY: {json.dumps(history_result, ensure_ascii=False)}\n"
            f"DIAGNOSTIC: {json.dumps(diagnostic_result, ensure_ascii=False)}\n"
            f"CONFIDENCE: {json.dumps(confidence_result, ensure_ascii=False)}\n"
            f"MANUAL: {json.dumps(manual_result, ensure_ascii=False)}\n\n"
            f"WARNINGS: {json.dumps(warnings, ensure_ascii=False)}\n\n"
            "BẮT BUỘC: không xuất trường confidence trong câu trả lời người dùng.\n"
            "Nếu CONFIDENCE.selected_dtc có giá trị thì dùng giá trị đó cho mục dtc (không để null).\n"
            "Nếu WARNINGS không rỗng, phải nêu rõ ở phần tóm tắt rằng thông tin đầu vào chưa đủ/chưa chuẩn nhưng vẫn đưa candidate tham khảo.\n"
            "Hãy trả lời theo đúng format mục 1..5 trong system prompt."
        )
    )
    final_response = llm.invoke([SystemMessage(content=SYSTEM_PROMPT), synthesis_input])
    return final_response.content if hasattr(final_response, "content") else str(final_response)


def _parse_tool_call_from_text(text: str):
    """
    Fallback: nếu model không hỗ trợ native tool_calls,
    tìm JSON có dạng {"name": "...", "arguments": {...}} trong content.
    """
    pattern = r'\{[^{}]*"name"\s*:\s*"[^"]+"\s*,[^{}]*"arguments"\s*:\s*\{[^{}]*\}[^{}]*\}'
    match = re.search(pattern, text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass
    return None


# 4. Agent Node — Vòng lặp ReAct tự chứa
def agent_node(state: AgentState):
    """
    Thay vì dùng ToolNode + tools_condition (cần native tool_calls),
    node này tự lặp: gọi LLM → phát hiện tool call → thực thi → nhồi kết quả → gọi LLM lại.
    Dừng khi LLM trả lời trực tiếp (không có JSON tool call) hoặc hết MAX_TOOL_ITERATIONS.
    """
    messages = list(state["messages"])

    # Thêm system prompt nếu chưa có
    if not any(isinstance(m, SystemMessage) for m in messages):
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + messages

    def _get_response_content(response):
        if isinstance(response, str):
            return response
        if hasattr(response, "content"):
            return response.content
        if hasattr(response, "text"):
            return response.text
        if hasattr(response, "output_text"):
            return response.output_text
        return str(response)

    for iteration in range(MAX_TOOL_ITERATIONS):
        print(f"\n--- Iteration {iteration + 1}/{MAX_TOOL_ITERATIONS} ---")

        # --- LOGIC : Context Refinement ---
        # Tự động nhắc nhở context xe nếu có dữ liệu trích xuất được từ history
        user_text = _latest_user_text(messages)
        ctx = _extract_vehicle_context(user_text)
        if ctx.get("model"):
            ctx_hint = f"[Ngữ cảnh hiện tại: Model {ctx['model']}, Year {ctx['model_year'] or 'N/A'}, FW {ctx['firmware'] or 'N/A'}]"
            if not any(ctx_hint in str(m.content) for m in messages[-2:]):
                messages.append(HumanMessage(content=f"{ctx_hint} Hãy dựa vào thông tin này để gọi tool chính xác."))

        response = llm_with_tools.invoke(messages)
        content = _get_response_content(response)

        # === LOGGING ===
        print(f"[DEBUG] tool_calls: {getattr(response, 'tool_calls', None)}")
        print(f"[DEBUG] content (100 chars): {repr(content[:100])}")

        # ── A. Native tool calling (model hỗ trợ chuẩn, VD: llama3.1) ──
        tool_calls = getattr(response, 'tool_calls', None)
        if tool_calls:
            for tc in tool_calls:
                tool_name = tc["name"]
                tool_args = tc["args"]
                tool_fn = TOOL_MAP.get(tool_name)
                if tool_fn:
                    print(f"✅ Native Tool: {tool_name}({tool_args})")
                    tool_result = tool_fn.invoke(tool_args)
                    print(f"📦 Kết quả:\n{tool_result}\n")
                    # Thêm kết quả vào lịch sử dưới dạng HumanMessage (model nào cũng hiểu)
                    messages.append(response)
                    messages.append(HumanMessage(content=f"[Kết quả từ {tool_name}]:\n{tool_result}"))
            continue  # Lặp lại để LLM quyết định bước tiếp theo

        # ── B. Fallback: parse JSON tool call từ content text ──
        parsed = _parse_tool_call_from_text(content)
        if parsed:
            tool_name = parsed.get("name")
            tool_args = parsed.get("arguments", {})
            tool_fn = TOOL_MAP.get(tool_name)

            if tool_fn:
                print(f"🔧 [Fallback] Gọi tool: {tool_name}({tool_args})")
                tool_result = tool_fn.invoke(tool_args)
                print(f"📦 Kết quả:\n{tool_result}\n")

                # --- LOGIC: Xử lý kết quả rỗng ---
                result_str = str(tool_result)
                if "[]" in result_str or "{}" in result_str or "not found" in result_str.lower():
                    feedback_msg = (
                        f"[Hệ thống]: Kết quả từ {tool_name} không có dữ liệu khớp. "
                        "Hãy thử một từ khóa khác, hoặc nếu bạn đang tìm mã lỗi (DTC), "
                        "hãy thử gọi get_diagnostic trực tiếp với triệu chứng để tìm nguyên nhân thay thế."
                    )
                else:
                    feedback_msg = f"[Hệ thống đã gọi {tool_name} và nhận được kết quả]:\n{tool_result}\n\nHãy tiếp tục phân tích theo SPEC."

                messages.append(AIMessage(content=content))
                messages.append(HumanMessage(content=feedback_msg))
                continue  # Lặp lại để LLM xử lý bước tiếp theo

        # ── C. Không phát hiện tool call → fallback deterministic pipeline (non-smalltalk) ──
        if iteration == 0:
            user_text = _latest_user_text(messages)
            if user_text and not _is_smalltalk(user_text):
                print("⚙️ Không có tool_calls native, chạy deterministic pipeline.")
                final_text = _run_deterministic_pipeline(user_text)
                return {"messages": [AIMessage(content=final_text)]}

        # ── D. Không phát hiện tool call → Đây là câu trả lời cuối cùng ──
        print("💬 Trả lời trực tiếp (kết thúc vòng lặp)")
        return {"messages": [AIMessage(content=content)]}

    # Đã hết số lần lặp → trả về kết quả cuối
    print("⚠️ Đã đạt giới hạn iterations, trả về kết quả hiện tại")
    return {"messages": [AIMessage(content=_get_response_content(response))]}


# 5. Xây dựng Graph — Đơn giản: START → agent → END
#    Toàn bộ logic tool đã nằm trong agent_node, không cần ToolNode
builder = StateGraph(AgentState)
builder.add_node("agent", agent_node)
builder.add_edge(START, "agent")
builder.add_edge("agent", END)

graph = builder.compile()


# 6. Chat loop
if __name__ == "__main__":
    print("=" * 60)
    print("VinFast Service Copilot – Symptom → DTC → Repair")
    print("      Gõ 'quit' để thoát")
    print("=" * 60)

    chat_history: list[tuple[str, str]] = []
    while True:
        user_input = input("\nBạn: ").strip()
        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit", "q"):
            break

        print("\nCopilot đang phân tích chẩn đoán...")
        context_messages = _build_recent_context_messages(chat_history, user_input)
        result = graph.invoke({"messages": context_messages})
        final = result["messages"][-1]
        answer = final.content if hasattr(final, "content") else str(final)
        print(f"\nCopilot: {answer}")

        chat_history.append(("human", user_input))
        chat_history.append(("ai", answer))

# --- KẾT THÚC CODE agent.py ---
