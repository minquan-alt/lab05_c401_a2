from langchain_core.tools import tool
import json
from pathlib import Path

DIAGNOSTIC_FILE = Path(__file__).resolve().parents[1] / "data" / "diagnostic_manual.json"

@tool
def get_diagnostic(dtc_list: list[str], model: str, model_year: int, firmware: str):
    """
    Lookup diagnostics by candidate DTC list and strict version metadata.
    """
    with open(DIAGNOSTIC_FILE, "r", encoding="utf-8") as f:
        diagnostic_data = json.load(f)

    diagnostics = []
    for dtc in dtc_list:
        found = None
        for record in diagnostic_data:
            applicable = record.get("applicable", {})
            if (
                record.get("dtc") == dtc
                and applicable.get("model") == model
                and applicable.get("model_year") == model_year
                and applicable.get("firmware") == firmware
            ):
                found = {
                    "dtc": dtc,
                    "possible_causes": record.get("possible_causes", []),
                    "diagnostic_steps": record.get("diagnostic_steps", []),
                }
                break

        if found is None:
            found = {
                "dtc": dtc,
                "possible_causes": [],
                "diagnostic_steps": [],
            }
        diagnostics.append(found)

    return {"diagnostics": diagnostics}
