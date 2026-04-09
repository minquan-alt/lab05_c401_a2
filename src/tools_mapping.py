"""Central registry for agent tools.

When adding/removing a tool, only edit this file.
Agent imports:
  - TOOLS: list of tool callables for llm.bind_tools(...)
  - TOOL_MAP: name -> tool callable for dispatch
"""

from tools.search_flights import search_flights
from tools.search_hotels import search_hotels
from tools.calculate_budget import calculate_budget

# Add new tools here (single source of truth)
TOOLS = [search_flights, search_hotels, calculate_budget]


def _tool_name(t) -> str:
    return getattr(t, "name", None) or getattr(t, "__name__", None) or str(t)


# Auto-build dispatch table from TOOLS
TOOL_MAP = {_tool_name(t): t for t in TOOLS}
