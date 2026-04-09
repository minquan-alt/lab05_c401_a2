from tools import (
    validate_input,
    get_repair_history,
    get_diagnostic,
    compute_confidence,
    retrieve_manual,
)

# Tools list for LLM binding
TOOLS = [
    validate_input,
    get_repair_history,
    get_diagnostic,
    compute_confidence,
    retrieve_manual,
]

# Dispatch table for execution by name
TOOL_MAP = {
    "validate_input": validate_input,
    "get_repair_history": get_repair_history,
    "get_diagnostic": get_diagnostic,
    "compute_confidence": compute_confidence,
    "retrieve_manual": retrieve_manual,
}
