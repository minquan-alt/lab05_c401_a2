from tools import calculate_budget, search_flights, search_hotels

# Tools list for LLM binding
TOOLS = [search_flights, search_hotels, calculate_budget]

# Dispatch table for execution by name
TOOL_MAP = {
    "search_flights": search_flights,
    "search_hotels": search_hotels,
    "calculate_budget": calculate_budget,
}
