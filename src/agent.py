from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from tools import search_flights, search_hotels, calculate_budget
from dotenv import load_dotenv
import os
import json
import re

load_dotenv()

# 1. Đọc System Prompt
with open("system_prompt.txt", "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()

# 2. Khai báo State
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]

# 3. Khởi tạo LLM và Tools
tools_list = [search_flights, search_hotels, calculate_budget]

base_url = os.getenv("OLLAMA_BASE_URL")
api_key = os.getenv("OLLAMA_API_KEY")
model_name = os.getenv("OLLAMA_MODEL")
llm = ChatOpenAI(
    base_url=base_url,
    api_key=api_key,
    model=model_name,
    temperature=0.1,
    max_tokens=1024
)
llm_with_tools = llm.bind_tools(tools_list)

# Map tên tool -> hàm thực thi
TOOL_MAP = {
    "search_flights": search_flights,
    "search_hotels": search_hotels,
    "calculate_budget": calculate_budget,
}

MAX_TOOL_ITERATIONS = 5  # Giới hạn số lần gọi tool liên tiếp, tránh loop vô hạn

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

    for iteration in range(MAX_TOOL_ITERATIONS):
        print(f"\n--- Iteration {iteration + 1}/{MAX_TOOL_ITERATIONS} ---")

        response = llm_with_tools.invoke(messages)
        content = response.content

        # === LOGGING ===
        print(f"[DEBUG] tool_calls: {response.tool_calls}")
        print(f"[DEBUG] content (100 chars): {repr(content[:100])}")

        # ── A. Native tool calling (model hỗ trợ chuẩn, VD: llama3.1) ──
        if response.tool_calls:
            for tc in response.tool_calls:
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

                # Nhồi kết quả vào conversation history
                # Dùng HumanMessage thay vì ToolMessage — Qwen2.5-Coder hiểu format này tốt hơn
                messages.append(AIMessage(content=content))
                messages.append(HumanMessage(
                    content=f"[Hệ thống đã gọi {tool_name} và nhận được kết quả]:\n{tool_result}\n\nHãy tiếp tục phân tích. Nếu cần thêm thông tin, hãy gọi tool tiếp. Nếu đã đủ, hãy tổng hợp và trả lời người dùng."
                ))
                continue  # Lặp lại để LLM xử lý bước tiếp theo

        # ── C. Không phát hiện tool call → Đây là câu trả lời cuối cùng ──
        print("💬 Trả lời trực tiếp (kết thúc vòng lặp)")
        return {"messages": [AIMessage(content=content)]}

    # Đã hết số lần lặp → trả về kết quả cuối
    print("⚠️ Đã đạt giới hạn iterations, trả về kết quả hiện tại")
    return {"messages": [AIMessage(content=response.content)]}


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
    print("TravelBuddy – Trợ lý Du lịch Thông minh")
    print("      Gõ 'quit' để thoát")
    print("=" * 60)

    while True:
        user_input = input("\nBạn: ").strip()
        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit", "q"):
            break

        print("\nTravelBuddy đang suy nghĩ...")
        result = graph.invoke({"messages": [("human", user_input)]})
        final = result["messages"][-1]
        print(f"\nTravelBuddy: {final.content}")

# --- KẾT THÚC CODE agent.py ---

