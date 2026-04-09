from langchain_core.tools import tool
import json

DIAGNOSTIC_FILE = "C:\\Users\\NCQHuy\\Desktop\\AIThucChien\\LopSang\\Day6\\lab05_c401_a2\\src\\data\\diagnostic_manual.json"

@tool
def get_diagnostic(dtc: str) -> str:
    with open(DIAGNOSTIC_FILE, "r") as f:
        diagnostic_data = json.load(f)

    for d in diagnostic_data:
        if d["dtc"] == dtc:
            return d

    return "Diagnostic information not found for the provided DTC."